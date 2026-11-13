"""
app.seo.images.diagram_renderer
Deterministic Visual Diagram and Chart Renderer for Numeros Vision.

In strict compliance with Section 7.2:
"When a diagram contains numerical values, directional labels, formulas or grid positions,
generate or render the visual from validated structured data whenever feasible.
Do not rely on an image model to reproduce exact mathematical or technical labels correctly.
For charts, use the actual validated dataset and a deterministic chart renderer.
Do not ask an image model to invent chart values."
"""

import io
import os
import hashlib
from typing import Dict, Any, List, Tuple, Optional
from PIL import Image, ImageDraw, ImageFont

# Brand Design Tokens (Venus Pearl & Jupiter Gold Luxury System - Strictly Zero Black)
COLOR_BG_DARK = "#FFFDF7"       # Canvas: Venus Pearl (#FFFDF7)
COLOR_BG_CARD = "#FFFFFF"       # Cards: Pure White
COLOR_GOLD = "#C9A227"          # Primary Jupiter Gold
COLOR_GOLD_LIGHT = "#8B6914"    # Deep Antique Gold for prominent numbers
COLOR_CREAM = "#523E28"         # Primary Titles/Labels: Sacred Bronze (Zero Black)
COLOR_MUTED = "#7A654D"         # Subtitles/Descriptions: Warm Medium Bronze (WCAG AA 4.6:1)
COLOR_BORDER = "#D8C59D"        # Borders: Soft Warm Gold
COLOR_ACCENT = "#16835B"        # Accents: Mercury Emerald
COLOR_INACTIVE = "#F7F3EA"      # Inactive elements: Soft Warm Cream Mid

def _get_font(size: int, serif: bool = True) -> ImageFont.ImageFont:
    """Safely loads appropriate system font or defaults gracefully."""
    font_candidates = []
    if serif:
        font_candidates = [
            "C:/Windows/Fonts/georgia.ttf",
            "C:/Windows/Fonts/times.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
        ]
    else:
        font_candidates = [
            "C:/Windows/Fonts/segoeui.ttf",
            "C:/Windows/Fonts/arial.ttf",
            "C:/Windows/Fonts/calibri.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()

class DeterministicDiagramRenderer:
    """Generates mathematically accurate numerological diagrams in SVG, WebP, and PNG formats."""

    @classmethod
    def render_lo_shu_grid(
        cls,
        active_numbers: Optional[List[int]] = None,
        title: str = "Lo Shu Magic Square Energy Grid",
        subtitle: str = "Traditional 3x3 Planetary Matrix & Energetic Planes",
        width: int = 1200,
        height: int = 675
    ) -> Dict[str, Any]:
        """
        Renders the canonical 3x3 Lo Shu Magic Square:
        Row 1: [4, 9, 2] (Mental Plane)
        Row 2: [3, 5, 7] (Emotional Plane)
        Row 3: [8, 1, 6] (Practical Plane)
        """
        if active_numbers is None:
            # Default: all standard numbers present
            active_set = {1, 2, 3, 4, 5, 6, 7, 8, 9}
        else:
            active_set = set(active_numbers)

        grid_matrix = [
            [(4, "Wood / SE", "Mental"), (9, "Fire / South", "Mental"), (2, "Earth / SW", "Mental")],
            [(3, "Wood / East", "Emotional"), (5, "Earth / Center", "Emotional"), (7, "Metal / West", "Emotional")],
            [(8, "Earth / NE", "Practical"), (1, "Water / North", "Practical"), (6, "Metal / NW", "Practical")]
        ]

        # 1. Raster Rendering with Pillow
        img = Image.new("RGB", (width, height), color=COLOR_BG_DARK)
        draw = ImageDraw.Draw(img)

        # Border & Title Accents
        draw.rectangle([(20, 20), (width - 20, height - 20)], outline=COLOR_BORDER, width=2)
        draw.rectangle([(26, 26), (width - 26, height - 26)], outline=COLOR_GOLD, width=1)

        font_brand = _get_font(20, serif=True)
        font_title = _get_font(34, serif=True)
        font_sub = _get_font(18, serif=False)
        font_cell_num = _get_font(64, serif=True)
        font_cell_meta = _get_font(14, serif=False)
        font_plane = _get_font(14, serif=False)

        # Brand header
        draw.text((60, 45), "NUMEROS VISION", fill=COLOR_GOLD, font=font_brand)
        draw.text((60, 80), title, fill=COLOR_CREAM, font=font_title)
        draw.text((60, 125), subtitle, fill=COLOR_MUTED, font=font_sub)

        # Grid Coordinates
        grid_start_x = 220
        grid_start_y = 175
        cell_size = 135
        cell_gap = 14

        # Planes Annotation Labels (Horizontal)
        planes_h = ["Mental Plane (4,9,2)", "Emotional Plane (3,5,7)", "Practical Plane (8,1,6)"]
        for row_idx, plane_name in enumerate(planes_h):
            py = grid_start_y + row_idx * (cell_size + cell_gap) + (cell_size // 2) - 8
            draw.text((grid_start_x + 3 * (cell_size + cell_gap) + 20, py), f"-> {plane_name}", fill=COLOR_GOLD_LIGHT, font=font_plane)

        # Draw Cells
        for r_idx, row in enumerate(grid_matrix):
            for c_idx, (num, element, plane) in enumerate(row):
                x1 = grid_start_x + c_idx * (cell_size + cell_gap)
                y1 = grid_start_y + r_idx * (cell_size + cell_gap)
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                is_active = num in active_set
                bg_color = COLOR_BG_CARD if is_active else COLOR_INACTIVE
                border_color = COLOR_GOLD if is_active else COLOR_BORDER
                text_color = COLOR_GOLD_LIGHT if is_active else COLOR_MUTED

                draw.rectangle([(x1, y1), (x2, y2)], fill=bg_color, outline=border_color, width=2)

                # Number centering
                num_str = str(num)
                bbox = font_cell_num.getbbox(num_str)
                text_w = bbox[2] - bbox[0]
                text_h = bbox[3] - bbox[1]
                num_x = x1 + (cell_size - text_w) // 2
                num_y = y1 + (cell_size - text_h) // 2 - 10
                draw.text((num_x, num_y), num_str, fill=text_color, font=font_cell_num)

                # Subtitle (Element / Direction)
                el_bbox = font_cell_meta.getbbox(element)
                el_w = el_bbox[2] - el_bbox[0]
                draw.text((x1 + (cell_size - el_w) // 2, y2 - 24), element, fill=COLOR_MUTED if not is_active else COLOR_CREAM, font=font_cell_meta)

        # Footer Authority Stamp
        draw.text((60, height - 55), "Verified Deterministic Lo Shu Engine | Zero-Hallucination Matrix | Numeros Vision", fill=COLOR_MUTED, font=_get_font(14, serif=False))

        # 2. Vector SVG Generation
        svg_cells = []
        for r_idx, row in enumerate(grid_matrix):
            for c_idx, (num, element, plane) in enumerate(row):
                x = grid_start_x + c_idx * (cell_size + cell_gap)
                y = grid_start_y + r_idx * (cell_size + cell_gap)
                is_active = num in active_set
                bg = COLOR_BG_CARD if is_active else COLOR_INACTIVE
                stroke = COLOR_GOLD if is_active else COLOR_BORDER
                fill_color = COLOR_GOLD_LIGHT if is_active else COLOR_MUTED
                svg_cells.append(
                    f'<rect x="{x}" y="{y}" width="{cell_size}" height="{cell_size}" rx="6" fill="{bg}" stroke="{stroke}" stroke-width="2"/>'
                    f'<text x="{x + cell_size/2}" y="{y + cell_size/2 + 10}" text-anchor="middle" font-family="Georgia, serif" font-size="56" font-weight="bold" fill="{fill_color}">{num}</text>'
                    f'<text x="{x + cell_size/2}" y="{y + cell_size - 14}" text-anchor="middle" font-family="Segoe UI, sans-serif" font-size="12" fill="{COLOR_CREAM}">{element}</text>'
                )

        svg_markup = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="100%" height="auto">
  <rect width="{width}" height="{height}" fill="{COLOR_BG_DARK}"/>
  <rect x="20" y="20" width="{width - 40}" height="{height - 40}" fill="none" stroke="{COLOR_BORDER}" stroke-width="2"/>
  <rect x="26" y="26" width="{width - 52}" height="{height - 52}" fill="none" stroke="{COLOR_GOLD}" stroke-width="1"/>
  <text x="60" y="60" font-family="Georgia, serif" font-size="20" fill="{COLOR_GOLD}" letter-spacing="2">NUMEROS VISION</text>
  <text x="60" y="105" font-family="Georgia, serif" font-size="34" font-weight="bold" fill="{COLOR_CREAM}">{title}</text>
  <text x="60" y="135" font-family="Segoe UI, sans-serif" font-size="16" fill="{COLOR_MUTED}">{subtitle}</text>
  {"".join(svg_cells)}
  <text x="60" y="{height - 40}" font-family="Segoe UI, sans-serif" font-size="13" fill="{COLOR_MUTED}">Verified Deterministic Lo Shu Engine | Zero-Hallucination Matrix | Numeros Vision</text>
</svg>'''

        # Encode WebP and PNG
        buf_webp = io.BytesIO()
        img.save(buf_webp, format="WEBP", quality=84, method=6)
        webp_bytes = buf_webp.getvalue()

        buf_png = io.BytesIO()
        img.save(buf_png, format="PNG", optimize=True)
        png_bytes = buf_png.getvalue()

        content_hash = hashlib.sha256(webp_bytes).hexdigest()

        return {
            "diagram_type": "LO_SHU_GRID",
            "width": width,
            "height": height,
            "svg": svg_markup,
            "webp_bytes": webp_bytes,
            "png_bytes": png_bytes,
            "content_hash": content_hash,
            "active_numbers": list(active_set)
        }

    @classmethod
    def render_chaldean_sound_matrix(
        cls,
        title: str = "Chaldean Planetary Sound & Vibration Matrix",
        subtitle: str = "Deterministic 1-to-8 Phonetic Letter Frequencies (Number 9 Sacred)",
        width: int = 1200,
        height: int = 675
    ) -> Dict[str, Any]:
        """
        Renders the canonical Chaldean sound matrix:
        1: A, I, J, Q, Y (Sun)
        2: B, K, R (Moon)
        3: C, G, L, S (Jupiter)
        4: D, M, T (Rahu / Uranus)
        5: E, H, N, X (Mercury)
        6: U, V, W (Venus)
        7: O, Z (Ketu / Neptune)
        8: F, P (Saturn)
        (Number 9 is held sacred in Chaldean tradition)
        """
        matrix_data = [
            (1, "Sun", ["A", "I", "J", "Q", "Y"], "Creative Vitality"),
            (2, "Moon", ["B", "K", "R"], "Intuitive Diplomacy"),
            (3, "Jupiter", ["C", "G", "L", "S"], "Wisdom & Order"),
            (4, "Rahu / Uranus", ["D", "M", "T"], "Individual Magnetism"),
            (5, "Mercury", ["E", "H", "N", "X"], "Versatile Intelligence"),
            (6, "Venus", ["U", "V", "W"], "Harmony & Romance"),
            (7, "Ketu / Neptune", ["O", "Z"], "Mystical Perception"),
            (8, "Saturn", ["F", "P"], "Karmic Endurance")
        ]

        img = Image.new("RGB", (width, height), color=COLOR_BG_DARK)
        draw = ImageDraw.Draw(img)

        # Borders
        draw.rectangle([(20, 20), (width - 20, height - 20)], outline=COLOR_BORDER, width=2)
        draw.rectangle([(26, 26), (width - 26, height - 26)], outline=COLOR_GOLD, width=1)

        draw.text((60, 45), "NUMEROS VISION | CHALDEAN CANONICAL SYSTEM", fill=COLOR_GOLD, font=_get_font(18, serif=True))
        draw.text((60, 80), title, fill=COLOR_CREAM, font=_get_font(32, serif=True))
        draw.text((60, 125), subtitle, fill=COLOR_MUTED, font=_get_font(16, serif=False))

        # Render 8 Columns
        start_x = 55
        start_y = 175
        col_w = 125
        col_gap = 13
        card_h = 390

        font_num = _get_font(38, serif=True)
        font_planet = _get_font(13, serif=False)
        font_letters = _get_font(20, serif=True)
        font_keyword = _get_font(11, serif=False)

        for idx, (num, planet, letters, keyword) in enumerate(matrix_data):
            x = start_x + idx * (col_w + col_gap)
            y = start_y

            # Card background
            draw.rectangle([(x, y), (x + col_w, y + card_h)], fill=COLOR_BG_CARD, outline=COLOR_GOLD, width=1)
            # Header pill
            draw.rectangle([(x, y), (x + col_w, y + 65)], fill=COLOR_INACTIVE)
            draw.text((x + (col_w // 2) - 12, y + 12), str(num), fill=COLOR_GOLD_LIGHT, font=font_num)

            # Planet Ruler
            p_bbox = font_planet.getbbox(planet)
            pw = p_bbox[2] - p_bbox[0]
            draw.text((x + (col_w - pw) // 2, y + 78), planet, fill=COLOR_CREAM, font=font_planet)

            # Divider line
            draw.line([(x + 15, y + 105), (x + col_w - 15, y + 105)], fill=COLOR_BORDER, width=1)

            # Letter list
            draw.text((x + 18, y + 115), "Vibration Letters:", fill=COLOR_MUTED, font=_get_font(11, serif=False))
            letters_str = ", ".join(letters)
            draw.text((x + 18, y + 138), letters_str, fill=COLOR_GOLD, font=font_letters)

            # Archetype keyword at bottom
            draw.text((x + 12, y + card_h - 40), keyword, fill=COLOR_MUTED, font=font_keyword)

        # Footer notice regarding sacred 9
        draw.text((60, height - 55), "Note: Number 9 is omitted from name conversion in Chaldean Numerology as a sacred vibration. | Numeros Vision", fill=COLOR_MUTED, font=_get_font(13, serif=False))

        # WebP and PNG
        buf_webp = io.BytesIO()
        img.save(buf_webp, format="WEBP", quality=84, method=6)
        webp_bytes = buf_webp.getvalue()

        buf_png = io.BytesIO()
        img.save(buf_png, format="PNG", optimize=True)
        png_bytes = buf_png.getvalue()

        return {
            "diagram_type": "CHALDEAN_SOUND_MATRIX",
            "width": width,
            "height": height,
            "webp_bytes": webp_bytes,
            "png_bytes": png_bytes,
            "content_hash": hashlib.sha256(webp_bytes).hexdigest()
        }

    @classmethod
    def render_compound_seal(
        cls,
        compound_num: int,
        root_num: int,
        title: str,
        archetype: str,
        keywords: List[str],
        width: int = 1200,
        height: int = 675
    ) -> Dict[str, Any]:
        """
        Renders a luxury esoteric compound number seal (e.g. Compound 14, 19, 21, 24).
        """
        img = Image.new("RGB", (width, height), color=COLOR_BG_DARK)
        draw = ImageDraw.Draw(img)

        # Luxury Double Border
        draw.rectangle([(20, 20), (width - 20, height - 20)], outline=COLOR_BORDER, width=2)
        draw.rectangle([(26, 26), (width - 26, height - 26)], outline=COLOR_GOLD, width=1)

        draw.text((60, 45), "NUMEROS VISION | CANONICAL ESOTERIC EMBLEM", fill=COLOR_GOLD, font=_get_font(18, serif=True))
        draw.text((60, 80), f"Compound Vibration {compound_num}: {title}", fill=COLOR_CREAM, font=_get_font(32, serif=True))
        draw.text((60, 125), f"Esoteric Archetype: {archetype} (Root Vibration: {root_num})", fill=COLOR_MUTED, font=_get_font(16, serif=False))

        # Central Golden Seal (Circular badge)
        cx = width // 2
        cy = 360
        r_outer = 150
        r_inner = 138

        draw.ellipse([(cx - r_outer, cy - r_outer), (cx + r_outer, cy + r_outer)], outline=COLOR_GOLD, width=2)
        draw.ellipse([(cx - r_inner, cy - r_inner), (cx + r_inner, cy + r_inner)], outline=COLOR_BORDER, width=1)
        draw.ellipse([(cx - r_inner + 4, cy - r_inner + 4), (cx + r_inner - 4, cy + r_inner - 4)], fill=COLOR_BG_CARD)

        # Huge Compound Number
        c_font = _get_font(88, serif=True)
        c_str = str(compound_num)
        bbox = c_font.getbbox(c_str)
        cw = bbox[2] - bbox[0]
        ch = bbox[3] - bbox[1]
        draw.text((cx - cw // 2, cy - ch // 2 - 25), c_str, fill=COLOR_GOLD_LIGHT, font=c_font)

        # Root vibration pill below number
        root_str = f"Root -> {root_num}"
        rf_font = _get_font(16, serif=False)
        r_bbox = rf_font.getbbox(root_str)
        rw = r_bbox[2] - r_bbox[0]
        draw.text((cx - rw // 2, cy + 45), root_str, fill=COLOR_CREAM, font=rf_font)

        # Left / Right informational panels
        panel_y = 230
        panel_h = 240
        panel_w = 280

        # Left: Symbolic Meaning
        draw.rectangle([(80, panel_y), (80 + panel_w, panel_y + panel_h)], fill=COLOR_BG_CARD, outline=COLOR_BORDER)
        draw.text((100, panel_y + 20), "Symbolic Meaning", fill=COLOR_GOLD, font=_get_font(16, serif=True))
        draw.text((100, panel_y + 55), f"Archetype: {archetype}", fill=COLOR_CREAM, font=_get_font(14, serif=False))
        draw.text((100, panel_y + 90), "Keywords:", fill=COLOR_MUTED, font=_get_font(13, serif=False))
        for k_idx, kw in enumerate(keywords[:4]):
            draw.text((115, panel_y + 115 + k_idx * 25), f"* {kw}", fill=COLOR_GOLD_LIGHT, font=_get_font(13, serif=False))

        # Right: Traditional Calculation
        draw.rectangle([(width - 80 - panel_w, panel_y), (width - 80, panel_y + panel_h)], fill=COLOR_BG_CARD, outline=COLOR_BORDER)
        draw.text((width - 60 - panel_w, panel_y + 20), "Reduction Mechanism", fill=COLOR_GOLD, font=_get_font(16, serif=True))
        digits = [int(d) for d in str(compound_num)]
        formula_str = f"{' + '.join(str(d) for d in digits)} = {root_num}"
        draw.text((width - 60 - panel_w, panel_y + 55), f"Formula: {formula_str}", fill=COLOR_CREAM, font=_get_font(14, serif=False))
        draw.text((width - 60 - panel_w, panel_y + 90), "Planetary Influence:", fill=COLOR_MUTED, font=_get_font(13, serif=False))
        draw.text((width - 60 - panel_w, panel_y + 115), "Primary: Combined Astral Forces", fill=COLOR_GOLD_LIGHT, font=_get_font(13, serif=False))
        draw.text((width - 60 - panel_w, panel_y + 140), "Root: Governing Single Digit", fill=COLOR_CREAM, font=_get_font(13, serif=False))

        # Footer
        draw.text((60, height - 55), "Traditional Esoteric Meaning Preserved | Unaltered Mathematical Reduction | Numeros Vision", fill=COLOR_MUTED, font=_get_font(13, serif=False))

        # WebP and PNG
        buf_webp = io.BytesIO()
        img.save(buf_webp, format="WEBP", quality=84, method=6)
        webp_bytes = buf_webp.getvalue()

        buf_png = io.BytesIO()
        img.save(buf_png, format="PNG", optimize=True)
        png_bytes = buf_png.getvalue()

        return {
            "diagram_type": "COMPOUND_SEAL",
            "compound_num": compound_num,
            "root_num": root_num,
            "width": width,
            "height": height,
            "webp_bytes": webp_bytes,
            "png_bytes": png_bytes,
            "content_hash": hashlib.sha256(webp_bytes).hexdigest()
        }
