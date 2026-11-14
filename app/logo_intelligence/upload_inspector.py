# -*- coding: utf-8 -*-
"""
app/logo_intelligence/upload_inspector.py
=========================================
Deterministic Real Logo Upload Inspector for Numeros Vision Logo Intelligence.

Supports:
- SVG (`image/svg+xml`, raw SVG string, or `.svg` bytes)
- PNG (`image/png`)
- JPEG (`image/jpeg`)
- PDF (`application/pdf` via `pymupdf`)

Fixes all Step 1 empirical prototype defects:
1. Fake SVG detection: `<image>` / `data:image/` or `<script>` / inline JS sets `is_vector=False`
   and fails `vector_integrity`.
2. Gradient resolution: resolves `url(#gradId)` against `<linearGradient>` / `<radialGradient>`
   `<stop stop-color="#...">` definitions so gradient-filled SVGs report true sampled hex colours.
3. Both `dominant_colors` and `palette_sampled` are populated identically for UI + API parity.
4. `nothing_cut` structural check: detects open paths (`<line>`, `<polyline>`, `<path>` without
   closing `Z` when `fill="none"`), dashed strokes on primary geometry, and background-coloured
   negative-space stencil bars slicing across `<text>` wordmarks.
5. Real raster & PDF text/colour extraction with explicit `text_confidence` and `colour_confidence`
   plus user-confirmed override fields (`confirmed_text`, `confirmed_primary_color`, etc.).
"""

from __future__ import annotations

import base64
from collections import Counter, deque
import io
import math
import os
import pathlib
import re
import shutil
import subprocess
import tempfile
from typing import Any, Dict, List, Optional, Set, Tuple
import xml.etree.ElementTree as ET

from PIL import Image, ImageDraw, ImageFont

from app.logo_intelligence.rulebook_v1 import (
    EvidenceLabel,
    calculate_contrast_ratio_hex,
    calculate_relative_luminance,
    classify_hex_colour_family,
    hex_to_rgb,
    normalize_hex,
)

try:
    import pymupdf as _pymupdf  # type: ignore
except Exception:
    try:
        import fitz as _pymupdf  # type: ignore
    except Exception:
        _pymupdf = None


NAMED_SVG_COLOURS: Dict[str, str] = {
    "white": "#FFFFFF",
    "black": "#000000",
    "ivory": "#FFFFF0",
    "gold": "#FFD700",
    "red": "#FF0000",
    "navy": "#000080",
    "blue": "#0000FF",
    "green": "#008000",
    "grey": "#808080",
    "gray": "#808080",
    "silver": "#C0C0C0",
    "orange": "#FFA500",
    "purple": "#800080",
    "maroon": "#800000",
    "teal": "#008080",
}

_GLYPH_TEMPLATE_CACHE: Optional[Dict[str, List[List[int]]]] = None


def _strip_data_uri(b64_or_uri: str) -> Tuple[bytes, Optional[str]]:
    raw = (b64_or_uri or "").strip()
    mime_hint: Optional[str] = None
    if raw.startswith("data:"):
        header, _, payload = raw.partition(",")
        m = re.match(r"data:([^;]+)", header, re.IGNORECASE)
        if m:
            mime_hint = m.group(1).strip().lower()
        if ";base64" in header.lower():
            return base64.b64decode(payload), mime_hint
        return payload.encode("utf-8"), mime_hint
    return base64.b64decode(raw), mime_hint


def _parse_colour_token(token: Optional[str], grad_map: Optional[Dict[str, List[str]]] = None) -> List[str]:
    if not token:
        return []
    val = token.strip()
    low = val.lower()
    if low in ("none", "transparent", "inherit", "currentcolor", ""):
        return []
    if low in NAMED_SVG_COLOURS:
        return [NAMED_SVG_COLOURS[low]]
    url_match = re.match(r"url\(\s*#([^)\s]+)\s*\)", val, re.IGNORECASE)
    if url_match and grad_map:
        gid = url_match.group(1)
        return list(grad_map.get(gid, []))
    hex_match = re.match(r"^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$", val)
    if hex_match:
        return [normalize_hex(val)]
    rgb_match = re.match(r"^rgba?\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)", low)
    if rgb_match:
        r, g, b = (min(255, int(rgb_match.group(i))) for i in (1, 2, 3))
        return [f"#{r:02X}{g:02X}{b:02X}"]
    return []


def _parse_inline_style(style_str: str) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for part in (style_str or "").split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            out[k.strip().lower()] = v.strip()
    return out


def _local_tag(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower() if "}" in tag else tag.lower()


def _parse_float(val: Optional[str], default: float = 0.0) -> float:
    if not val:
        return default
    m = re.search(r"-?\d+(?:\.\d+)?", str(val))
    return float(m.group(0)) if m else default


def _parse_translate_y(transform_str: Optional[str]) -> float:
    if not transform_str:
        return 0.0
    m = re.search(r"translate\(\s*(-?\d+(?:\.\d+)?)(?:[\s,]+(-?\d+(?:\.\d+)?))?\s*\)", transform_str)
    if m and m.group(2) is not None:
        return float(m.group(2))
    return 0.0


def _parse_translate_x(transform_str: Optional[str]) -> float:
    if not transform_str:
        return 0.0
    m = re.search(r"translate\(\s*(-?\d+(?:\.\d+)?)", transform_str)
    return float(m.group(1)) if m else 0.0


def _path_is_closed(d_attr: str) -> bool:
    """
    Returns True if every non-empty subpath in `d` ends with `Z` or `z`.
    """
    cleaned = (d_attr or "").strip()
    if not cleaned:
        return True
    subpaths = [sp.strip() for sp in re.split(r"(?=[Mm])", cleaned) if sp.strip()]
    if not subpaths:
        return True
    for sp in subpaths:
        if not sp.endswith(("Z", "z")):
            return False
    return True


def _distinct_brand_colours(hex_list: List[str], bg_hex: str) -> List[str]:
    """
    Deduplicates visually near-identical gradient stops (RGB Euclidean distance < 36)
    so multi-stop metallic gold gradients count as 1 gold colour rather than 4 separate colours,
    while preserving truly distinct colours.
    """
    clusters: List[str] = []
    for hx in hex_list:
        norm = normalize_hex(hx)
        rgb = hex_to_rgb(norm)
        merged = False
        for existing in clusters:
            er, eg, eb = hex_to_rgb(existing)
            if math.sqrt((rgb[0] - er) ** 2 + (rgb[1] - eg) ** 2 + (rgb[2] - eb) ** 2) < 36.0:
                merged = True
                break
        if not merged:
            clusters.append(norm)
    return clusters


def _build_glyph_templates() -> Dict[str, List[List[int]]]:
    global _GLYPH_TEMPLATE_CACHE
    if _GLYPH_TEMPLATE_CACHE is not None:
        return _GLYPH_TEMPLATE_CACHE

    here = pathlib.Path(__file__).resolve()
    font_candidates = [
        here.parents[2] / "pdf_service" / "app" / "fonts" / "arialbd.ttf",
        pathlib.Path.cwd() / "pdf_service" / "app" / "fonts" / "arialbd.ttf",
        pathlib.Path("C:/Windows/Fonts/arialbd.ttf"),
        pathlib.Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ]
    font_obj = None
    for fp in font_candidates:
        if fp.is_file():
            try:
                font_obj = ImageFont.truetype(str(fp), 64)
                break
            except Exception:
                continue
    if font_obj is None:
        _GLYPH_TEMPLATE_CACHE = {}
        return _GLYPH_TEMPLATE_CACHE

    templates: Dict[str, List[List[int]]] = {}
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    for ch in alphabet:
        canvas = Image.new("L", (96, 96), 0)
        draw = ImageDraw.Draw(canvas)
        draw.text((12, 10), ch, fill=255, font=font_obj)
        bbox = canvas.getbbox()
        if not bbox:
            continue
        cropped = canvas.crop(bbox).resize((24, 32), Image.Resampling.BILINEAR)
        px = cropped.tobytes()
        grid = [[1 if px[r * 24 + c] >= 110 else 0 for c in range(24)] for r in range(32)]
        templates[ch] = grid

    _GLYPH_TEMPLATE_CACHE = templates
    return templates


def _ocr_via_tesseract(img: Image.Image) -> Tuple[str, float]:
    tess_bin = shutil.which("tesseract")
    if not tess_bin:
        return "", 0.0
    fd, tmp_path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        rgb_img = img.convert("RGB")
        rgb_img.save(tmp_path, format="PNG")
        proc = subprocess.run(
            [tess_bin, tmp_path, "stdout", "--psm", "6"],
            capture_output=True,
            text=True,
            timeout=8,
            check=False,
        )
        if proc.returncode != 0:
            return "", 0.0
        raw_text = re.sub(r"\s+", " ", (proc.stdout or "").strip())
        cleaned = re.sub(r"^[^A-Za-z0-9]+|[^A-Za-z0-9]+$", "", raw_text)
        if len(cleaned) >= 2:
            return cleaned, 0.88
        return "", 0.0
    except Exception:
        return "", 0.0
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass


def _ocr_via_template_components(img: Image.Image, bg_rgb: Tuple[int, int, int]) -> Tuple[str, float]:
    """
    Deterministic connected-component glyph recognizer for clean geometric sans/bold wordmarks
    when external `tesseract` binary is absent (e.g., Windows dev host).
    Never guesses: returns `("", 0.20)` unless average character IoU >= 0.62 across >= 2 glyphs.
    """
    templates = _build_glyph_templates()
    if not templates:
        return "", 0.20

    rgba = img.convert("RGBA")
    w, h = rgba.size
    if w < 64 or h < 32 or w * h > 2_500_000:
        if w * h > 2_500_000:
            scale = math.sqrt(1_200_000 / float(w * h))
            rgba = rgba.resize((max(64, int(w * scale)), max(32, int(h * scale))), Image.Resampling.BILINEAR)
            w, h = rgba.size
        else:
            return "", 0.20

    raw = rgba.load()
    fg_mask = [[False] * w for _ in range(h)]
    for y in range(h):
        for x in range(w):
            r, g, b, a = raw[x, y]
            if a < 60:
                continue
            dist = math.sqrt((r - bg_rgb[0]) ** 2 + (g - bg_rgb[1]) ** 2 + (b - bg_rgb[2]) ** 2)
            if dist >= 55.0:
                fg_mask[y][x] = True

    visited = [[False] * w for _ in range(h)]
    boxes: List[Tuple[int, int, int, int, int]] = []
    for y in range(h):
        for x in range(w):
            if fg_mask[y][x] and not visited[y][x]:
                q: deque[Tuple[int, int]] = deque([(x, y)])
                visited[y][x] = True
                x0 = x1 = x
                y0 = y1 = y
                area = 0
                while q:
                    cx, cy = q.popleft()
                    area += 1
                    if cx < x0:
                        x0 = cx
                    if cx > x1:
                        x1 = cx
                    if cy < y0:
                        y0 = cy
                    if cy > y1:
                        y1 = cy
                    for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                        if 0 <= nx < w and 0 <= ny < h and fg_mask[ny][nx] and not visited[ny][nx]:
                            visited[ny][nx] = True
                            q.append((nx, ny))
                bw = x1 - x0 + 1
                bh = y1 - y0 + 1
                if area >= 18 and 10 <= bh <= int(h * 0.45) and 2 <= bw <= int(bh * 1.8):
                    boxes.append((x0, y0, x1, y1, area))

    if len(boxes) < 2:
        return "", 0.20

    # Cluster boxes into horizontal baseline rows
    boxes.sort(key=lambda item: (item[1] + item[3]) / 2.0)
    rows: List[List[Tuple[int, int, int, int, int]]] = []
    for bx in boxes:
        cy = (bx[1] + bx[3]) / 2.0
        bh = bx[3] - bx[1] + 1
        placed = False
        for row in rows:
            rcy = sum((it[1] + it[3]) / 2.0 for it in row) / len(row)
            rbh = sum((it[3] - it[1] + 1) for it in row) / len(row)
            if abs(cy - rcy) <= rbh * 0.40 and 0.65 * rbh <= bh <= 1.45 * rbh:
                row.append(bx)
                placed = True
                break
        if not placed:
            rows.append([bx])

    best_text = ""
    best_score = 0.0
    for row in rows:
        if len(row) < 2:
            continue
        row.sort(key=lambda it: it[0])
        med_h = sorted(it[3] - it[1] + 1 for it in row)[len(row) // 2]
        chars: List[str] = []
        scores: List[float] = []
        prev_x1: Optional[int] = None

        for x0, y0, x1, y1, _ in row:
            if prev_x1 is not None and (x0 - prev_x1) > med_h * 0.28:
                chars.append(" ")
            prev_x1 = x1

            bw = x1 - x0 + 1
            bh = y1 - y0 + 1
            sub = Image.new("L", (bw, bh), 0)
            spx = sub.load()
            for yy in range(y0, y1 + 1):
                for xx in range(x0, x1 + 1):
                    if fg_mask[yy][xx]:
                        spx[xx - x0, yy - y0] = 255
            norm_img = sub.resize((24, 32), Image.Resampling.BILINEAR)
            npx = norm_img.tobytes()
            grid = [[1 if npx[r * 24 + c] >= 110 else 0 for c in range(24)] for r in range(32)]

            aspect = bw / float(max(1, bh))
            best_ch = "?"
            best_iou = 0.0
            for ch, tgrid in templates.items():
                if ch in ("I", "1") and aspect > 0.42:
                    continue
                if ch not in ("I", "1", "J", "L") and aspect < 0.25:
                    continue
                inter = 0
                union = 0
                for r in range(32):
                    gr = grid[r]
                    tr = tgrid[r]
                    for c in range(24):
                        gv = gr[c]
                        tv = tr[c]
                        if gv or tv:
                            union += 1
                            if gv and tv:
                                inter += 1
                iou = inter / float(union) if union else 0.0
                if iou > best_iou:
                    best_iou = iou
                    best_ch = ch
            chars.append(best_ch)
            scores.append(best_iou)

        avg_iou = sum(scores) / len(scores) if scores else 0.0
        candidate = "".join(chars).strip()
        if avg_iou >= 0.62 and avg_iou > best_score and len(candidate.replace(" ", "")) >= 2:
            best_score = avg_iou
            best_text = candidate

    if best_text:
        return best_text, round(min(0.94, best_score), 2)
    return "", 0.20


def inspect_svg_logo(svg_content: str) -> Dict[str, Any]:
    raw_svg = (svg_content or "").strip()
    if not raw_svg:
        raise ValueError("SVG content is empty.")
    low_svg = raw_svg.lower()
    if "<!doctype" in low_svg or "<!entity" in low_svg:
        raise ValueError("SVG contains disallowed XML DOCTYPE/ENTITY declarations.")

    has_unsafe_script = bool(
        re.search(r"<\s*script\b", raw_svg, re.IGNORECASE)
        or re.search(r"javascript\s*:", raw_svg, re.IGNORECASE)
        or re.search(r"\bon[a-z]+\s*=", raw_svg, re.IGNORECASE)
    )
    has_embedded_raster = bool(
        re.search(r"<\s*image\b", raw_svg, re.IGNORECASE)
        or re.search(r"data:image/(?:png|jpeg|jpg|webp|gif|bmp)", raw_svg, re.IGNORECASE)
    )

    try:
        root = ET.fromstring(raw_svg)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid SVG XML structure: {exc}") from exc

    has_svg_root = _local_tag(root.tag) == "svg"
    is_vector = bool(has_svg_root and not has_embedded_raster and not has_unsafe_script)

    # Dimensions from viewBox or width/height
    vb = (root.attrib.get("viewBox") or "").strip().replace(",", " ").split()
    if len(vb) == 4:
        width = int(round(_parse_float(vb[2], 512.0)))
        height = int(round(_parse_float(vb[3], 512.0)))
    else:
        width = int(round(_parse_float(root.attrib.get("width"), 512.0)))
        height = int(round(_parse_float(root.attrib.get("height"), 512.0)))

    # 1. Build gradient map (`id -> [stop_hex, ...]`)
    grad_map: Dict[str, List[str]] = {}
    for elem in root.iter():
        tag = _local_tag(elem.tag)
        if tag in ("lineargradient", "radialgradient"):
            gid = (elem.attrib.get("id") or "").strip()
            stops: List[str] = []
            for child in elem:
                if _local_tag(child.tag) == "stop":
                    st_style = _parse_inline_style(child.attrib.get("style", ""))
                    op_str = child.attrib.get("stop-opacity") or st_style.get("stop-opacity")
                    if op_str is not None and _parse_float(op_str, 1.0) <= 0.08:
                        continue
                    sc = child.attrib.get("stop-color") or st_style.get("stop-color")
                    stops.extend(_parse_colour_token(sc))
            if gid and stops:
                # Represent a multi-stop sheen gradient by its median luminance stop (1 colour per gradient)
                stops_sorted = sorted(stops, key=lambda hx: calculate_relative_luminance(hex_to_rgb(hx)))
                grad_map[gid] = [stops_sorted[len(stops_sorted) // 2]]

    # 2. Traverse elements to collect background, foreground colours, text, fonts, open/cut geometry
    bg_hex = "#FFFDF7"
    bg_detected = False
    fg_hexes: List[str] = []
    text_items: List[Tuple[float, str, float, float, str]] = []  # (font_size, text, abs_x, abs_y, fill_hex)
    rects_after_or_all: List[Tuple[int, float, float, float, float, str]] = []
    font_families: Set[str] = set()
    open_form_reasons: List[str] = []

    parent_map = {c: p for p in root.iter() for c in p}

    def _abs_offset(el: ET.Element) -> Tuple[float, float]:
        tx, ty = 0.0, 0.0
        cur: Optional[ET.Element] = el
        while cur is not None:
            tr = cur.attrib.get("transform")
            tx += _parse_translate_x(tr)
            ty += _parse_translate_y(tr)
            cur = parent_map.get(cur)
        return tx, ty

    elem_index = 0
    in_defs_set: Set[ET.Element] = set()
    for elem in root.iter():
        if _local_tag(elem.tag) == "defs":
            for sub in elem.iter():
                in_defs_set.add(sub)

    for elem in root.iter():
        if elem in in_defs_set:
            continue
        elem_index += 1
        tag = _local_tag(elem.tag)
        if tag == "svg":
            continue
        style = _parse_inline_style(elem.attrib.get("style", ""))
        fill_raw = elem.attrib.get("fill") or style.get("fill")
        stroke_raw = elem.attrib.get("stroke") or style.get("stroke")
        dasharray = elem.attrib.get("stroke-dasharray") or style.get("stroke-dasharray")

        fill_cols = _parse_colour_token(fill_raw, grad_map)
        stroke_cols = _parse_colour_token(stroke_raw, grad_map)

        # Detect full-canvas background rect
        if tag == "rect" and not bg_detected:
            rw = elem.attrib.get("width", "")
            rh = elem.attrib.get("height", "")
            rx_pos = _parse_float(elem.attrib.get("x"), 0.0)
            ry_pos = _parse_float(elem.attrib.get("y"), 0.0)
            is_full_w = ("100%" in rw) or (_parse_float(rw, 0.0) >= width * 0.90)
            is_full_h = ("100%" in rh) or (_parse_float(rh, 0.0) >= height * 0.90)
            if is_full_w and is_full_h and rx_pos <= 5 and ry_pos <= 5 and fill_cols:
                bg_hex = fill_cols[0]
                bg_detected = True
                continue

        for c in fill_cols + stroke_cols:
            if c != bg_hex:
                fg_hexes.append(c)

        # Font family extraction
        ff_raw = elem.attrib.get("font-family") or style.get("font-family")
        if ff_raw:
            primary_font = ff_raw.split(",")[0].strip().strip("'\"").lower()
            if primary_font and primary_font not in ("serif", "sans-serif", "monospace", "system-ui"):
                font_families.add(primary_font)

        # Text extraction
        if tag == "text":
            txt = "".join(elem.itertext()).strip()
            if txt:
                fsize = _parse_float(elem.attrib.get("font-size") or style.get("font-size"), 24.0)
                ox, oy = _abs_offset(elem)
                tx = ox + _parse_float(elem.attrib.get("x"), 0.0)
                ty = oy + _parse_float(elem.attrib.get("y"), 0.0)
                tfill = fill_cols[0] if fill_cols else (stroke_cols[0] if stroke_cols else "#523E28")
                text_items.append((fsize, txt, tx, ty, tfill))

        # Track non-canvas rects for negative-space stencil slice check
        if tag == "rect" and fill_cols:
            ox, oy = _abs_offset(elem)
            rx = ox + _parse_float(elem.attrib.get("x"), 0.0)
            ry = oy + _parse_float(elem.attrib.get("y"), 0.0)
            rw_f = _parse_float(elem.attrib.get("width"), 0.0)
            rh_f = _parse_float(elem.attrib.get("height"), 0.0)
            rects_after_or_all.append((elem_index, rx, ry, rw_f, rh_f, fill_cols[0]))

        # Check open contours (`nothing_cut`)
        if tag in ("line", "polyline"):
            open_form_reasons.append(f"Open `<{tag}>` stroke element detected (all shapes must be closed outlines).")
        elif tag == "path":
            d_val = elem.attrib.get("d") or ""
            is_fill_none = (fill_raw is not None and fill_raw.strip().lower() == "none") or (not fill_cols and bool(stroke_cols))
            if not _path_is_closed(d_val):
                if is_fill_none or stroke_cols:
                    open_form_reasons.append("Unclosed `<path>` contour without terminal `Z` detected.")
        if dasharray and str(dasharray).strip().lower() != "none":
            open_form_reasons.append("Fragmented `stroke-dasharray` cut stroke detected.")

    # Check if a background-coloured `<rect>` slices horizontally through the interior of `<text>`
    for fsize, txt, tx, ty, _ in text_items:
        if len(txt) < 2:
            continue
        cap_top = ty - fsize * 0.78
        cap_bot = ty - fsize * 0.10
        est_w = max(fsize * len(txt) * 0.45, 40.0)
        for _, rx, ry, rw_f, rh_f, rfill in rects_after_or_all:
            if normalize_hex(rfill) == normalize_hex(bg_hex) and rw_f >= 20.0 and 1.0 <= rh_f <= fsize * 0.65:
                vert_inside = cap_top <= ry <= cap_bot
                horiz_overlap = (rx < tx + est_w) and (rx + rw_f > tx - est_w * 0.5)
                if vert_inside and horiz_overlap:
                    open_form_reasons.append(
                        f"Negative-space stencil cut bar (`fill={rfill}`) slices through wordmark `{txt}`."
                    )

    # Primary wordmark vs tagline selection
    extracted_lines = [it[1] for it in text_items]
    primary_wordmark = ""
    if text_items:
        multi_char = [it for it in text_items if len(it[1].strip()) >= 2]
        chosen = max(multi_char or text_items, key=lambda it: (it[0], len(it[1])))
        primary_wordmark = chosen[1].strip()

    distinct_fg = _distinct_brand_colours(fg_hexes, bg_hex)
    primary_fg = distinct_fg[0] if distinct_fg else "#523E28"
    accent_fg = distinct_fg[1] if len(distinct_fg) >= 2 else primary_fg
    palette_sampled = distinct_fg + ([bg_hex] if bg_hex not in distinct_fg else [])

    # Contrast measurement: test worst-case active foreground on background AND primary foreground
    symbol_ratios = [calculate_contrast_ratio_hex(c, bg_hex) for c in (distinct_fg[:2] or [primary_fg])]
    primary_contrast = round(calculate_contrast_ratio_hex(primary_fg, bg_hex), 2)
    min_active_contrast = round(min(symbol_ratios), 2)

    # Small text contrast (any `<text>` with font_size < 24px regular / < 18.66px bold)
    small_text_ratios: List[float] = []
    for fsize, txt, _, _, tfill in text_items:
        if fsize < 18.66 and len(txt.strip()) >= 2:
            small_text_ratios.append(calculate_contrast_ratio_hex(tfill, bg_hex))
    small_text_min_contrast = round(min(small_text_ratios), 2) if small_text_ratios else primary_contrast

    # Monochrome luminance separation (grayscale contrast)
    mono_clear = min_active_contrast >= 3.0
    app_icon_clear = (width >= 64 and height >= 48 and min_active_contrast >= 3.0 and len(distinct_fg) <= 3)

    return {
        "format": "SVG",
        "is_vector": is_vector,
        "has_svg_root": has_svg_root,
        "has_embedded_raster": has_embedded_raster,
        "has_unsafe_script": has_unsafe_script,
        "dimensions": {"width": width, "height": height},
        "background_hex": bg_hex,
        "primary_foreground_hex": primary_fg,
        "accent_foreground_hex": accent_fg,
        "dominant_colors": palette_sampled,
        "palette_sampled": palette_sampled,
        "distinct_colour_count": len(palette_sampled),
        "distinct_foreground_count": len(distinct_fg),
        "primary_contrast_ratio": primary_contrast,
        "min_symbol_contrast_ratio": min_active_contrast,
        "small_text_contrast_ratio": small_text_min_contrast,
        "wcag_contrast_estimate": min_active_contrast,
        "extracted_text": primary_wordmark,
        "extracted_text_lines": extracted_lines,
        "text_confidence": 0.99 if primary_wordmark else 0.35,
        "colour_confidence": 0.99 if distinct_fg else 0.60,
        "font_families": sorted(font_families),
        "font_count": len(font_families),
        "nothing_cut_passed": len(open_form_reasons) == 0,
        "open_or_cut_reasons": open_form_reasons,
        "monochrome_clear": mono_clear,
        "app_icon_legible": app_icon_clear,
        "user_corrected": False,
        "evidence_label": EvidenceLabel.MEASURED.value,
    }


def inspect_raster_image(
    img: Image.Image,
    *,
    source_format: str = "PNG",
    is_vector_override: bool = False,
    preset_text: Optional[str] = None,
    preset_text_conf: Optional[float] = None,
) -> Dict[str, Any]:
    rgba = img.convert("RGBA")
    width, height = rgba.size

    # Sample perimeter pixels to determine background colour
    px = rgba.load()
    border_pixels: List[Tuple[int, int, int]] = []
    transparent_border = 0
    total_border = 0
    for x in range(0, width, max(1, width // 64)):
        for y in (0, height - 1):
            total_border += 1
            r, g, b, a = px[x, y]
            if a < 50:
                transparent_border += 1
            else:
                border_pixels.append(((r // 8) * 8, (g // 8) * 8, (b // 8) * 8))
    for y in range(0, height, max(1, height // 64)):
        for x in (0, width - 1):
            total_border += 1
            r, g, b, a = px[x, y]
            if a < 50:
                transparent_border += 1
            else:
                border_pixels.append(((r // 8) * 8, (g // 8) * 8, (b // 8) * 8))

    has_transparency = transparent_border > (total_border * 0.25)
    if border_pixels and not has_transparency:
        bg_q = Counter(border_pixels).most_common(1)[0][0]
        # Refine exact average RGB near `bg_q`
        exact_bg = [
            px[x, 0][:3]
            for x in range(0, width, max(1, width // 64))
            if px[x, 0][3] >= 200
            and abs(px[x, 0][0] - bg_q[0]) <= 12
            and abs(px[x, 0][1] - bg_q[1]) <= 12
            and abs(px[x, 0][2] - bg_q[2]) <= 12
        ]
        if exact_bg:
            br = round(sum(p[0] for p in exact_bg) / len(exact_bg))
            bg = round(sum(p[1] for p in exact_bg) / len(exact_bg))
            bb = round(sum(p[2] for p in exact_bg) / len(exact_bg))
            bg_rgb = (br, bg, bb)
        else:
            bg_rgb = bg_q
        bg_hex = f"#{bg_rgb[0]:02X}{bg_rgb[1]:02X}{bg_rgb[2]:02X}"
    else:
        bg_rgb = (255, 253, 247)
        bg_hex = "#FFFDF7"

    # Sample interior pixels to cluster foreground colours
    step_x = max(1, width // 120)
    step_y = max(1, height // 120)
    fg_counter: Counter[Tuple[int, int, int]] = Counter()
    fg_exact_buckets: Dict[Tuple[int, int, int], List[Tuple[int, int, int]]] = {}
    for y in range(0, height, step_y):
        for x in range(0, width, step_x):
            r, g, b, a = px[x, y]
            if a < 80:
                continue
            dist_bg = math.sqrt((r - bg_rgb[0]) ** 2 + (g - bg_rgb[1]) ** 2 + (b - bg_rgb[2]) ** 2)
            if dist_bg < 32.0:
                continue
            key = ((r // 16) * 16, (g // 16) * 16, (b // 16) * 16)
            fg_counter[key] += 1
            if len(fg_exact_buckets.setdefault(key, [])) < 60:
                fg_exact_buckets[key].append((r, g, b))

    raw_fg_hexes: List[str] = []
    total_fg_hits = sum(fg_counter.values()) or 1
    for key, count in fg_counter.most_common(8):
        if count / float(total_fg_hits) < 0.03 and raw_fg_hexes:
            continue
        samples = fg_exact_buckets[key]
        ar = round(sum(p[0] for p in samples) / len(samples))
        ag = round(sum(p[1] for p in samples) / len(samples))
        ab = round(sum(p[2] for p in samples) / len(samples))
        raw_fg_hexes.append(f"#{ar:02X}{ag:02X}{ab:02X}")

    distinct_fg = _distinct_brand_colours(raw_fg_hexes, bg_hex)
    primary_fg = distinct_fg[0] if distinct_fg else "#523E28"
    accent_fg = distinct_fg[1] if len(distinct_fg) >= 2 else primary_fg
    palette_sampled = distinct_fg[:3] + ([bg_hex] if bg_hex not in distinct_fg[:3] else [])

    symbol_ratios = [calculate_contrast_ratio_hex(c, bg_hex) for c in (distinct_fg[:2] or [primary_fg])]
    primary_contrast = round(calculate_contrast_ratio_hex(primary_fg, bg_hex), 2)
    min_active_contrast = round(min(symbol_ratios), 2)

    # Small-size app-icon legibility gate: master must be >= 64x64 AND 32x32 downscale must preserve contrast
    icon_32 = rgba.resize((32, 32), Image.Resampling.BILINEAR)
    ipx = icon_32.load()
    lums = [
        calculate_relative_luminance(ipx[x, y][:3])
        for y in range(32)
        for x in range(32)
        if ipx[x, y][3] >= 80
    ]
    downscale_contrast = ((max(lums) + 0.05) / (min(lums) + 0.05)) if len(lums) >= 2 else 1.0
    app_icon_legible = bool(width >= 64 and height >= 64 and downscale_contrast >= 2.2 and min_active_contrast >= 3.0)

    # OCR text extraction
    if preset_text is not None:
        extracted_text = preset_text
        text_conf = float(preset_text_conf if preset_text_conf is not None else (0.96 if preset_text else 0.30))
    else:
        extracted_text, text_conf = _ocr_via_tesseract(rgba)
        if not extracted_text:
            extracted_text, text_conf = _ocr_via_template_components(rgba, bg_rgb)

    return {
        "format": source_format.upper(),
        "is_vector": is_vector_override,
        "has_svg_root": False,
        "has_embedded_raster": not is_vector_override,
        "has_unsafe_script": False,
        "has_transparency": has_transparency,
        "dimensions": {"width": width, "height": height},
        "background_hex": bg_hex,
        "primary_foreground_hex": primary_fg,
        "accent_foreground_hex": accent_fg,
        "dominant_colors": palette_sampled,
        "palette_sampled": palette_sampled,
        "distinct_colour_count": len(palette_sampled),
        "distinct_foreground_count": len(distinct_fg),
        "primary_contrast_ratio": primary_contrast,
        "min_symbol_contrast_ratio": min_active_contrast,
        "small_text_contrast_ratio": primary_contrast,
        "wcag_contrast_estimate": min_active_contrast,
        "extracted_text": extracted_text,
        "extracted_text_lines": [extracted_text] if extracted_text else [],
        "text_confidence": round(text_conf, 2),
        "colour_confidence": 0.92 if distinct_fg else 0.55,
        "font_families": [],
        "font_count": 1 if extracted_text else 0,
        "nothing_cut_passed": True,
        "open_or_cut_reasons": [],
        "monochrome_clear": min_active_contrast >= 3.0,
        "app_icon_legible": app_icon_legible,
        "downscale_32px_contrast": round(downscale_contrast, 2),
        "user_corrected": False,
        "evidence_label": EvidenceLabel.MEASURED.value,
    }


def inspect_pdf_logo(pdf_bytes: bytes) -> Dict[str, Any]:
    if _pymupdf is None:
        raise ValueError("PDF inspection module (PyMuPDF) is not available on this server.")
    try:
        doc = _pymupdf.open(stream=pdf_bytes, filetype="pdf")
    except Exception as exc:
        raise ValueError(f"Uploaded file is not a valid PDF document: {exc}") from exc

    if doc.page_count < 1:
        raise ValueError("Uploaded PDF contains zero pages.")

    page = doc[0]
    raw_text = re.sub(r"\s+", " ", (page.get_text("text") or "").strip())
    drawings = page.get_drawings() or []
    embedded_images = page.get_images(full=True) or []
    is_pure_vector_pdf = (len(drawings) > 0 or bool(raw_text)) and len(embedded_images) == 0

    pix = page.get_pixmap(dpi=150, alpha=True)
    pil_img = Image.frombytes("RGBA", (pix.width, pix.height), pix.samples)
    doc.close()

    preset_txt: Optional[str] = raw_text if raw_text else None
    preset_conf: Optional[float] = 0.97 if raw_text else None
    report = inspect_raster_image(
        pil_img,
        source_format="PDF",
        is_vector_override=is_pure_vector_pdf,
        preset_text=preset_txt,
        preset_text_conf=preset_conf,
    )
    report["pdf_vector_drawing_count"] = len(drawings)
    report["pdf_embedded_image_count"] = len(embedded_images)
    return report


def inspect_uploaded_logo(
    *,
    svg_content: Optional[str] = None,
    file_bytes: Optional[bytes] = None,
    image_base64: Optional[str] = None,
    filename: Optional[str] = None,
    mime_type: Optional[str] = None,
    confirmed_text: Optional[str] = None,
    confirmed_primary_color: Optional[str] = None,
    confirmed_accent_color: Optional[str] = None,
    confirmed_bg_color: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Unified upload inspector for SVG, PNG, JPEG, and PDF logo files with
    optional user-confirmed text/colour overrides.
    """
    detected_mime = (mime_type or "").strip().lower()
    fname_low = (filename or "").strip().lower()

    if file_bytes is None and image_base64:
        try:
            file_bytes, uri_mime = _strip_data_uri(image_base64)
            if uri_mime and not detected_mime:
                detected_mime = uri_mime
        except Exception as exc:
            raise ValueError(f"Invalid base64 logo upload payload: {exc}") from exc

    if svg_content and svg_content.strip():
        report = inspect_svg_logo(svg_content)
    elif file_bytes is not None:
        if len(file_bytes) == 0:
            raise ValueError("Uploaded logo file is empty.")
        if len(file_bytes) > 10 * 1024 * 1024:
            raise ValueError("Uploaded logo exceeds the 10 MB maximum file size.")

        head = file_bytes[:512].lstrip()
        if head.startswith(b"%PDF") or detected_mime == "application/pdf" or fname_low.endswith(".pdf"):
            report = inspect_pdf_logo(file_bytes)
        elif (
            head.startswith(b"<svg")
            or (head.startswith(b"<?xml") and b"<svg" in file_bytes[:4096].lower())
            or detected_mime == "image/svg+xml"
            or fname_low.endswith(".svg")
        ):
            report = inspect_svg_logo(file_bytes.decode("utf-8", errors="replace"))
        else:
            try:
                pil_img = Image.open(io.BytesIO(file_bytes))
                pil_fmt = (pil_img.format or "").upper()
            except Exception as exc:
                raise ValueError(
                    "Unsupported or unreadable image format. Please upload PNG, JPEG, PDF, or SVG."
                ) from exc
            if pil_fmt not in ("PNG", "JPEG", "JPG", "MPO"):
                raise ValueError(
                    f"Unsupported image format `{pil_fmt or 'UNKNOWN'}`. Allowed formats: PNG, JPEG, PDF, SVG."
                )
            norm_fmt = "JPEG" if pil_fmt in ("JPEG", "JPG", "MPO") else "PNG"
            report = inspect_raster_image(pil_img, source_format=norm_fmt)
    else:
        raise ValueError("Provide an SVG, PNG, JPEG, or PDF logo file to inspect.")

    # Apply optional user corrections (confidence -> 1.0 when user confirms/overrides)
    user_corrected = False
    if confirmed_text is not None and confirmed_text.strip():
        report["extracted_text"] = confirmed_text.strip()
        report["text_confidence"] = 1.0
        user_corrected = True

    bg_hex = report["background_hex"]
    primary_fg = report["primary_foreground_hex"]
    accent_fg = report["accent_foreground_hex"]

    if confirmed_bg_color and confirmed_bg_color.strip():
        bg_hex = normalize_hex(confirmed_bg_color)
        report["background_hex"] = bg_hex
        user_corrected = True
    if confirmed_primary_color and confirmed_primary_color.strip():
        primary_fg = normalize_hex(confirmed_primary_color)
        report["primary_foreground_hex"] = primary_fg
        user_corrected = True
    if confirmed_accent_color and confirmed_accent_color.strip():
        accent_fg = normalize_hex(confirmed_accent_color)
        report["accent_foreground_hex"] = accent_fg
        user_corrected = True

    if user_corrected:
        fg_list = _distinct_brand_colours([primary_fg, accent_fg], bg_hex)
        palette = fg_list + ([bg_hex] if bg_hex not in fg_list else [])
        report["dominant_colors"] = palette
        report["palette_sampled"] = palette
        report["distinct_colour_count"] = len(palette)
        report["distinct_foreground_count"] = len(fg_list)
        p_ratio = round(calculate_contrast_ratio_hex(primary_fg, bg_hex), 2)
        min_ratio = round(min(calculate_contrast_ratio_hex(c, bg_hex) for c in (fg_list or [primary_fg])), 2)
        report["primary_contrast_ratio"] = p_ratio
        report["min_symbol_contrast_ratio"] = min_ratio
        report["wcag_contrast_estimate"] = min_ratio
        report["colour_confidence"] = 1.0
        report["user_corrected"] = True

    # Attach classified colour families for downstream Layer 1 & Layer 2 checks
    report["classified_palette"] = [
        classify_hex_colour_family(hx) for hx in report["palette_sampled"]
    ]
    return report
