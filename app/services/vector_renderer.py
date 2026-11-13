"""
Numeros Vision — Deterministic Vector Renderer & Typesetting Fallback
Implements Section 17.6 of the Master Build Specification:
Generates true scalable vector graphics (SVG) with clean geometric paths and
deterministic typesetting of the customer-approved wordmark.
Never renames a raster PNG to .svg.
"""

from typing import Dict, Any, Optional, List
import html
from app.services.logo_validator import calculate_contrast_ratio, calculate_relative_luminance, hex_to_rgb


class VectorRenderer:
    """
    Renders pure SVG vector deliverables conforming to the Numeros Vision design system.
    """

    @classmethod
    def render_svg(
        cls,
        exact_wordmark: str,
        symbol_type: str = "geometric_star",
        primary_hex: str = "#C9A227",
        secondary_hex: str = "#FFFDF7",
        accent_hex: str = "#16835B",
        bg_hex: Optional[str] = None,
        variant: str = "horizontal_lockup",  # "icon", "horizontal_lockup", "stacked_lockup"
        theme_mode: str = "light",  # "light", "dark", "monochrome"
        tagline: Optional[str] = None,
    ) -> str:
        """
        Generates production-grade SVG markup.
        """
        escaped_wordmark = html.escape(exact_wordmark.upper())
        escaped_tagline = html.escape((tagline or "ANVEIL EVERY CHARM").upper())

        # Adjust colors for dark or monochrome modes
        if theme_mode == "monochrome":
            primary_hex = "#222222"
            secondary_hex = "#FFFFFF"
            accent_hex = "#444444"
            bg_color = "#FFFFFF" if not bg_hex else bg_hex
        elif theme_mode == "dark":
            bg_color = "#121212" if not bg_hex else bg_hex
            secondary_hex = "#F7F3EA"
        else:
            bg_color = bg_hex if bg_hex else "#FFFDF7"

        # Check text contrast against background; if contrast < 4.5, adjust text color to guaranteed accessible brand ink
        rgb_fg = hex_to_rgb(primary_hex)
        rgb_bg = hex_to_rgb(bg_color)
        contrast = calculate_contrast_ratio(rgb_fg, rgb_bg)
        if contrast < 4.5:
            if calculate_relative_luminance(rgb_bg) > 0.5:
                text_fill = "#523E28"  # Accessible Sandalwood Ink on light pearl
            else:
                text_fill = "#FFFDF7"  # Accessible Venus Pearl on dark
        else:
            text_fill = primary_hex

        # 1. Generate Symbol Paths based on symbol_type
        symbol_svg = cls._generate_symbol_paths(symbol_type, primary_hex, accent_hex)

        # 2. Layout Geometry based on variant
        if variant == "icon":
            view_width, view_height = 800, 800
            content = f"""
            <g transform="translate(400, 400) scale(1.6)">
                {symbol_svg}
            </g>
            """
        elif variant == "stacked_lockup":
            view_width, view_height = 800, 900
            content = f"""
            <g transform="translate(400, 320) scale(1.3)">
                {symbol_svg}
            </g>
            <text x="400" y="660" 
                  text-anchor="middle" 
                  font-family="'Cinzel', 'Trajan Pro', 'Georgia', serif" 
                  font-size="44" 
                  font-weight="700" 
                  letter-spacing="6" 
                  fill="{text_fill}">
                {escaped_wordmark}
            </text>
            <line x1="300" y1="710" x2="500" y2="710" stroke="{accent_hex}" stroke-width="2" opacity="0.6"/>
            """
        else:  # horizontal_lockup default
            view_width, view_height = 1200, 400
            content = f"""
            <g transform="translate(240, 200) scale(0.9)">
                {symbol_svg}
            </g>
            <text x="420" y="215" 
                  font-family="'Cinzel', 'Trajan Pro', 'Georgia', serif" 
                  font-size="52" 
                  font-weight="700" 
                  letter-spacing="6" 
                  fill="{text_fill}">
                {escaped_wordmark}
            </text>
            <text x="425" y="255" 
                  font-family="'Inter', 'Helvetica Neue', sans-serif" 
                  font-size="14" 
                  font-weight="500" 
                  letter-spacing="4" 
                  fill="{accent_hex}" 
                  opacity="0.9">
                {escaped_tagline}
            </text>
            """

        bg_rect = f'<rect width="100%" height="100%" fill="{bg_color}"/>' if bg_color else ""

        svg_markup = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {view_width} {view_height}" width="{view_width}" height="{view_height}">
  <defs>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&amp;family=Inter:wght@400;500&amp;display=swap');
    </style>
  </defs>
  {bg_rect}
  {content}
</svg>"""
        return svg_markup.strip()

    @classmethod
    def _generate_symbol_paths(cls, symbol_type: str, primary_hex: str, accent_hex: str) -> str:
        """Generates clean geometric vector paths centered at origin (0, 0)."""
        if symbol_type == "ascending_peak":
            return f"""
            <polygon points="0,-120 100,80 -100,80" fill="none" stroke="{primary_hex}" stroke-width="12" stroke-linejoin="round"/>
            <polygon points="0,-70 60,60 -60,60" fill="{accent_hex}" opacity="0.85"/>
            <circle cx="0" cy="-140" r="16" fill="{primary_hex}"/>
            """
        elif symbol_type == "solar_crest":
            return f"""
            <circle cx="0" cy="0" r="46" fill="{primary_hex}" />
            <circle cx="0" cy="0" r="28" fill="{accent_hex}" opacity="0.9" />
            <circle cx="0" cy="0" r="12" fill="{primary_hex}" />
            <g stroke="{primary_hex}" stroke-width="6" stroke-linecap="round">
                <line x1="0" y1="-60" x2="0" y2="-105" />
                <line x1="0" y1="60" x2="0" y2="105" />
                <line x1="-60" y1="0" x2="-105" y2="0" />
                <line x1="60" y1="0" x2="105" y2="0" />
                <line x1="-44" y1="-44" x2="-75" y2="-75" />
                <line x1="44" y1="-44" x2="75" y2="-75" />
                <line x1="-44" y1="44" x2="-75" y2="75" />
                <line x1="44" y1="44" x2="75" y2="75" />
            </g>
            <circle cx="0" cy="0" r="115" fill="none" stroke="{accent_hex}" stroke-width="2.5" stroke-dasharray="6 6" opacity="0.7"/>
            """
        elif symbol_type == "mercury_caduceus":
            return f"""
            <path d="M -75 0 C -75 -45, -20 -45, 0 0 C 20 45, 75 45, 75 0 C 75 -45, 20 -45, 0 0 C -20 45, -75 45, -75 0 Z" fill="none" stroke="{primary_hex}" stroke-width="7" stroke-linejoin="round"/>
            <line x1="0" y1="-120" x2="0" y2="105" stroke="{accent_hex}" stroke-width="6" stroke-linecap="round"/>
            <circle cx="0" cy="-125" r="14" fill="{primary_hex}"/>
            <polygon points="-45,-35 -15,-55 -30,-20" fill="{accent_hex}" opacity="0.85"/>
            <polygon points="45,-35 15,-55 30,-20" fill="{accent_hex}" opacity="0.85"/>
            <circle cx="0" cy="115" r="8" fill="{primary_hex}"/>
            """
        elif symbol_type == "golden_triangle":
            return f"""
            <polygon points="0,-120 105,65 -105,65" fill="none" stroke="{primary_hex}" stroke-width="9" stroke-linejoin="round"/>
            <polygon points="0,65 52,-25 -52,-25" fill="none" stroke="{accent_hex}" stroke-width="6" stroke-linejoin="round"/>
            <polygon points="0,-25 26,20 -26,20" fill="{primary_hex}" opacity="0.9"/>
            <circle cx="0" cy="-135" r="10" fill="{accent_hex}"/>
            <circle cx="-120" cy="75" r="10" fill="{accent_hex}"/>
            <circle cx="120" cy="75" r="10" fill="{accent_hex}"/>
            """
        elif symbol_type == "sacred_lotus":
            return f"""
            <path d="M 0 35 C -35 -10, -45 -65, 0 -105 C 45 -65, 35 -10, 0 35 Z" fill="none" stroke="{primary_hex}" stroke-width="7"/>
            <path d="M 0 35 C -65 15, -100 -25, -65 -70 C -30 -35, -10 -10, 0 35 Z" fill="none" stroke="{accent_hex}" stroke-width="5.5"/>
            <path d="M 0 35 C 65 15, 100 -25, 65 -70 C 30 -35, 10 -10, 0 35 Z" fill="none" stroke="{accent_hex}" stroke-width="5.5"/>
            <circle cx="0" cy="40" r="12" fill="{primary_hex}"/>
            <circle cx="0" cy="-35" r="15" fill="{primary_hex}" opacity="0.9"/>
            """
        elif symbol_type == "mars_shield":
            return f"""
            <polygon points="0,-115 85,-40 85,45 0,115 -85,45 -85,-40" fill="none" stroke="{primary_hex}" stroke-width="9" stroke-linejoin="round"/>
            <polygon points="0,-75 55,-25 55,30 0,75 -55,30 -55,-25" fill="{accent_hex}" opacity="0.25"/>
            <polyline points="-45,-10 0,35 45,-10" fill="none" stroke="{primary_hex}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
            <polyline points="-30,-45 0,0 30,-45" fill="none" stroke="{accent_hex}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>
            """
        elif symbol_type == "sacred_mandala":
            return f"""
            <circle cx="0" cy="0" r="110" fill="none" stroke="{primary_hex}" stroke-width="6"/>
            <circle cx="0" cy="0" r="85" fill="none" stroke="{accent_hex}" stroke-width="3" stroke-dasharray="8 6"/>
            <polygon points="0,-95 67,67 -95,-28 95,-28 -67,67" fill="none" stroke="{primary_hex}" stroke-width="5"/>
            <circle cx="0" cy="0" r="22" fill="{primary_hex}"/>
            """
        else:  # geometric_star default
            return f"""
            <polygon points="0,-120 35,-35 120,0 35,35 0,120 -35,35 -120,0 -35,-35" fill="none" stroke="{primary_hex}" stroke-width="8" stroke-linejoin="round"/>
            <circle cx="0" cy="0" r="40" fill="{accent_hex}" opacity="0.9"/>
            <circle cx="0" cy="0" r="14" fill="{primary_hex}"/>
            """
