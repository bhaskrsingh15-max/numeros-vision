# -*- coding: utf-8 -*-
"""
app/logo_intelligence/vector_templates.py
=========================================
Deterministic Pure-SVG Vector Template Engine for Numeros Vision Logo Intelligence (Layer 4).

Guarantees:
1. 100% closed geometric outlines (`<circle>`, `<rect>`, `<polygon>`, `<path d="... Z">`).
   Zero open `<line>`, zero `<polyline>`, zero unclosed `<path>`, zero stencil cuts.
2. Honest rendering: NEVER silently substitutes `#C9A227` with `#523E28` to fake contrast!
   Every user-selected or reconciled colour renders faithfully so Layer 4 hard gates measure true contrast.
3. Roots `2, 4, 7` have `status="NOT_CONFIGURED"` for planetary symbols in `data/logo_rules_v1.json`;
   when no approved symbol is configured or selected, renders clean pure `wordmark` or `lettermark` vector.
4. Maximum 2 font families (`Cinzel` and `Inter`), maximum 3 colours, zero embedded `<image>`, zero `<script>`.
"""

from __future__ import annotations

import html
import re
from typing import Optional

APPROVED_SYMBOL_IDS = frozenset({
    "solar_crest",
    "golden_triangle",
    "mercury_caduceus",
    "sacred_lotus",
    "ascending_peak",
    "mars_shield",
})


def _norm_hex(value: Optional[str], fallback: str) -> str:
    s = (value or "").strip().upper()
    if re.fullmatch(r"#[0-9A-F]{6}", s):
        return s
    if re.fullmatch(r"#[0-9A-F]{3}", s):
        return "#" + "".join(ch * 2 for ch in s[1:])
    return fallback


def _extract_initials(wordmark: str) -> str:
    words = [w for w in re.split(r"\s+", (wordmark or "").strip().upper()) if w]
    letters = [re.sub(r"[^A-Z0-9]", "", w)[:1] for w in words]
    letters = [ch for ch in letters if ch]
    if not letters:
        clean = re.sub(r"[^A-Z0-9]", "", (wordmark or "").upper())
        return clean[:2] or "NV"
    return "".join(letters[:2])


def render_closed_symbol_geometry(
    symbol_id: Optional[str],
    primary_hex: str,
    accent_hex: str,
    bg_hex: str,
    initials: str = "NV",
) -> str:
    """
    Returns closed-outline SVG primitives centered at `(0, 0)` within `[-120..120, -120..120]`.
    Every `<path>` terminates with `Z`; zero `<line>` or `<polyline>` elements are used.
    """
    sym = (symbol_id or "").strip().lower()

    if sym == "solar_crest":
        # Sun (Root 1): 8 closed diamond rays + concentric closed solar discs
        rays = []
        for deg in range(0, 360, 45):
            rays.append(
                f'<polygon points="0,-108 10,-72 0,-62 -10,-72" fill="{primary_hex}" transform="rotate({deg})"/>'
            )
        return (
            "\n".join(rays)
            + f'\n<circle cx="0" cy="0" r="50" fill="{primary_hex}"/>'
            + f'\n<circle cx="0" cy="0" r="30" fill="{bg_hex}"/>'
            + f'\n<circle cx="0" cy="0" r="16" fill="{accent_hex}"/>'
        )

    if sym == "golden_triangle":
        # Jupiter (Root 3): Nested closed equilateral triangles + closed apex circle
        return (
            f'<polygon points="0,-102 94,68 -94,68" fill="{primary_hex}"/>'
            f'<polygon points="0,-68 62,48 -62,48" fill="{bg_hex}"/>'
            f'<polygon points="0,-36 34,30 -34,30" fill="{accent_hex}"/>'
        )

    if sym == "mercury_caduceus":
        # Mercury (Root 5): Closed figure-eight loop + closed central pillar rect + closed wing polygons
        return (
            f'<rect x="-6" y="-96" width="12" height="192" rx="6" fill="{accent_hex}"/>'
            f'<path d="M 0 -10 C -48 -58, -82 -18, -42 18 C -18 38, -6 24, 0 10 C 6 24, 18 38, 42 18 C 82 -18, 48 -58, 0 -10 Z" fill="{primary_hex}"/>'
            f'<polygon points="-18,-62 -76,-84 -54,-46" fill="{accent_hex}"/>'
            f'<polygon points="18,-62 76,-84 54,-46" fill="{accent_hex}"/>'
            f'<circle cx="0" cy="-106" r="13" fill="{primary_hex}"/>'
        )

    if sym == "sacred_lotus":
        # Venus (Root 6): Three closed symmetrical lotus petals + closed basepedestal
        return (
            f'<path d="M -22 36 C -84 18, -96 -42, -38 -68 C -18 -40, -14 -4, -22 36 Z" fill="{accent_hex}"/>'
            f'<path d="M 22 36 C 84 18, 96 -42, 38 -68 C 18 -40, 14 -4, 22 36 Z" fill="{accent_hex}"/>'
            f'<path d="M 0 44 C -44 10, -42 -62, 0 -98 C 42 -62, 44 10, 0 44 Z" fill="{primary_hex}"/>'
            f'<rect x="-56" y="52" width="112" height="14" rx="7" fill="{primary_hex}"/>'
        )

    if sym == "ascending_peak":
        # Saturn (Root 8): Closed structural outer peak + closed inner keystone
        return (
            f'<polygon points="0,-104 98,74 -98,74" fill="{primary_hex}"/>'
            f'<polygon points="0,-64 62,54 -62,54" fill="{bg_hex}"/>'
            f'<polygon points="0,-32 36,42 -36,42" fill="{accent_hex}"/>'
            f'<circle cx="0" cy="-114" r="11" fill="{primary_hex}"/>'
        )

    if sym == "mars_shield":
        # Mars (Root 9): Closed hexagonal valor crest + closed inner chevron polygon
        return (
            f'<polygon points="0,-104 86,-54 86,42 0,104 -86,42 -86,-54" fill="{primary_hex}"/>'
            f'<polygon points="0,-78 64,-38 64,30 0,78 -64,30 -64,-38" fill="{bg_hex}"/>'
            f'<polygon points="0,-44 42,6 22,22 0,-6 -22,22 -42,6" fill="{accent_hex}"/>'
        )

    # Lettermark / Monogram closed seal (used for `lettermark` or roots 2, 4, 7 when badge icon requested)
    safe_init = html.escape(initials[:2])
    return (
        f'<circle cx="0" cy="0" r="92" fill="{primary_hex}"/>'
        f'<circle cx="0" cy="0" r="76" fill="{bg_hex}"/>'
        f'<text x="0" y="18" text-anchor="middle" font-family="Cinzel, Georgia, serif" font-size="54" font-weight="700" fill="{primary_hex}">{safe_init}</text>'
    )


def render_deterministic_logo_svg(
    *,
    exact_wordmark: str,
    symbol_id: Optional[str],
    logo_type: str = "combination_mark",
    variant: str = "horizontal_lockup",
    primary_hex: str = "#523E28",
    accent_hex: str = "#16835B",
    bg_hex: str = "#FFFDF7",
    tagline: Optional[str] = None,
) -> str:
    """
    Renders deterministic pure-SVG markup with exact character preservation,
    closed geometric paths, max 2 fonts (`Cinzel`, `Inter`), and max 3 colours.
    """
    clean_wordmark = (exact_wordmark or "").strip()
    escaped_wordmark = html.escape(clean_wordmark.upper())
    clean_tagline = (tagline or "").strip()
    escaped_tagline = html.escape(clean_tagline.upper()) if clean_tagline else ""

    p_hex = _norm_hex(primary_hex, "#523E28")
    a_hex = _norm_hex(accent_hex, p_hex)
    b_hex = _norm_hex(bg_hex, "#FFFDF7")

    norm_type = (logo_type or "combination_mark").strip().lower()
    norm_variant = (variant or "horizontal_lockup").strip().lower()
    initials = _extract_initials(clean_wordmark)

    has_approved_symbol = bool(symbol_id and symbol_id.strip().lower() in APPROVED_SYMBOL_IDS)
    use_wordmark_only = (norm_type == "wordmark") or (not has_approved_symbol and norm_type != "lettermark" and norm_variant != "icon")

    if norm_variant == "icon":
        vw, vh = 512, 512
        sym_markup = render_closed_symbol_geometry(
            symbol_id if has_approved_symbol else None,
            p_hex,
            a_hex,
            b_hex,
            initials=initials,
        )
        body = (
            f'  <rect width="{vw}" height="{vh}" rx="64" fill="{b_hex}"/>\n'
            f'  <g transform="translate(256, 256) scale(1.65)">\n    {sym_markup}\n  </g>'
        )
    elif use_wordmark_only:
        vw, vh = 960, 320
        tagline_svg = (
            f'\n  <text x="480" y="222" text-anchor="middle" font-family="Inter, sans-serif" '
            f'font-size="18" font-weight="700" letter-spacing="4" fill="{a_hex}">{escaped_tagline}</text>'
            if escaped_tagline
            else ""
        )
        body = (
            f'  <rect width="{vw}" height="{vh}" fill="{b_hex}"/>\n'
            f'  <text x="480" y="162" text-anchor="middle" font-family="Cinzel, Georgia, serif" '
            f'font-size="54" font-weight="700" letter-spacing="5" fill="{p_hex}">{escaped_wordmark}</text>\n'
            f'  <rect x="360" y="184" width="240" height="5" rx="2.5" fill="{a_hex}"/>'
            f'{tagline_svg}'
        )
    elif norm_variant == "stacked_lockup":
        vw, vh = 800, 760
        sym_markup = render_closed_symbol_geometry(
            symbol_id if has_approved_symbol else None,
            p_hex,
            a_hex,
            b_hex,
            initials=initials,
        )
        tagline_svg = (
            f'\n  <text x="400" y="642" text-anchor="middle" font-family="Inter, sans-serif" '
            f'font-size="18" font-weight="700" letter-spacing="4" fill="{a_hex}">{escaped_tagline}</text>'
            if escaped_tagline
            else ""
        )
        body = (
            f'  <rect width="{vw}" height="{vh}" fill="{b_hex}"/>\n'
            f'  <g transform="translate(400, 270) scale(1.25)">\n    {sym_markup}\n  </g>\n'
            f'  <text x="400" y="566" text-anchor="middle" font-family="Cinzel, Georgia, serif" '
            f'font-size="46" font-weight="700" letter-spacing="5" fill="{p_hex}">{escaped_wordmark}</text>\n'
            f'  <rect x="290" y="592" width="220" height="5" rx="2.5" fill="{a_hex}"/>'
            f'{tagline_svg}'
        )
    else:
        vw, vh = 1100, 360
        sym_markup = render_closed_symbol_geometry(
            symbol_id if has_approved_symbol else None,
            p_hex,
            a_hex,
            b_hex,
            initials=initials,
        )
        tagline_svg = (
            f'\n  <text x="364" y="236" font-family="Inter, sans-serif" '
            f'font-size="18" font-weight="700" letter-spacing="4" fill="{a_hex}">{escaped_tagline}</text>'
            if escaped_tagline
            else ""
        )
        body = (
            f'  <rect width="{vw}" height="{vh}" fill="{b_hex}"/>\n'
            f'  <g transform="translate(185, 180) scale(0.95)">\n    {sym_markup}\n  </g>\n'
            f'  <text x="360" y="186" font-family="Cinzel, Georgia, serif" '
            f'font-size="50" font-weight="700" letter-spacing="5" fill="{p_hex}">{escaped_wordmark}</text>'
            f'{tagline_svg}'
        )

    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw} {vh}" width="{vw}" height="{vh}">\n'
        f"{body}\n"
        f"</svg>"
    )
