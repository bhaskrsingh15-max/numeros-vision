"""
NUMEROS VISION — DETERMINISTIC PDF REPORT GENERATION PIPELINE (v2.2.0)
Tagline: ANVEIL EVERY CHARM

Architecture:
1. Layer A: Deterministic Python Calculation Engine (Authoritative)
   - Exact calculations for Driver, Conductor, Lo Shu 3x3 grid, Chaldean name vibrations,
     Pythagorean expression, Kua directions, and Personal Year epicycles.
   - Zero LLM arithmetic or hallucinated formulas.
2. Layer B: Governed Interpretation & Dynamic Package-Based Assembly
   - Three standard tiers:
     * Basic Report (Target: 3 Pages · ₹199)
     * Advanced Report (Target: 12 Pages · ₹489 / Active Charm Present Numbers)
     * Premium Dossier (Target: 32 Pages · ₹1,050 / Anveil Charm Missing Numbers)
   - Dynamic Topic Prioritization:
     * Lo Shu Grid & Life Path foundational basics always come first (Pages 1-4).
     * The purchased topic (Present Numbers, Missing Numbers & Vastu, Love & Relationship,
       Career & Wealth, Health & Vitality, Name Balancing, Spatial Vastu) is frontloaded
       and emphasized immediately after the basic report (Pages 5-7).
     * Followed by supporting multi-factor chapters (Pages 8-11) and statutory sign-off (Page 12).
     * Premium 32-page compendium provides 20 exhaustive sovereign chapters (Pages 13-32)
       including Day 8 Canon Poorak Numbers, Element Yogas, 4-Stage Pinnacles, and Directional Spatial Harmony.
   - Vedic Gharelu Remedies Bank:
     * Readily accessible household zero-cost cures for numbers 1 to 9 (respecting parents/elders,
       Surya arghya in copper lota, silver cup, 40-day haldi water, mustard oil diya, green plants).
     * Universal 40-Day Rock Salt (Sendha Namak) aura cleansing and loop-breaking protocol.
   - STRICTLY ZERO ASTROLOGY WORDS:
     * Pure Numerology, Vibrational Science, Lo Shu Grid, and Numerology Dasha Timing Radar.
"""

import os
import io
import json
import time
import math
import hashlib
import datetime
from typing import Dict, Any, List, Optional, Tuple, Union

# Load Content Library and Terminology for Report Generation
_BASE_APP_DATA = os.path.join(os.path.dirname(__file__), "..", "data")
_LIB_FILE = os.path.join(_BASE_APP_DATA, "basic_report_content_library.json")
_GEO_FILE = os.path.join(_BASE_APP_DATA, "terminology_geo.json")

CONTENT_LIB: Dict[str, Any] = {}
if os.path.exists(_LIB_FILE):
    try:
        with open(_LIB_FILE, "r", encoding="utf-8") as _lf:
            CONTENT_LIB = json.load(_lf)
    except Exception:
        CONTENT_LIB = {}

GEO_TERMS: Dict[str, Any] = {}
if os.path.exists(_GEO_FILE):
    try:
        with open(_GEO_FILE, "r", encoding="utf-8") as _gf:
            GEO_TERMS = json.load(_gf)
    except Exception:
        GEO_TERMS = {}

def get_geo_label(term_key: str, edition: str = "india") -> str:
    t = GEO_TERMS.get("terms", {}).get(term_key, {})
    if not t:
        return term_key.upper()
    if (edition or "india").lower() == "international":
        return f"{t.get('intl_primary')} ({t.get('intl_secondary')})"
    return f"{t.get('india_primary')} ({t.get('india_secondary')})"

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable, Image
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

FONT_SERIF_REGULAR = 'Times-Roman'
FONT_SERIF_BOLD = 'Times-Bold'
FONT_SERIF_ITALIC = 'Times-Italic'
FONT_SANS_REGULAR = 'Helvetica'
FONT_SANS_BOLD = 'Helvetica-Bold'

def _init_theme_fonts():
    global FONT_SERIF_REGULAR, FONT_SERIF_BOLD, FONT_SERIF_ITALIC, FONT_SANS_REGULAR, FONT_SANS_BOLD
    base_dirs = [
        os.path.join(os.path.dirname(__file__), "..", "fonts"),
        os.path.join(os.path.dirname(__file__), "..", "..", "pdf_service", "app", "fonts"),
        r"C:\Windows\Fonts",
        "/usr/share/fonts/truetype/dejavu",
        "/usr/share/fonts/truetype/liberation"
    ]
    for d in base_dirs:
        t_reg = os.path.join(d, "times.ttf")
        t_bld = os.path.join(d, "timesbd.ttf")
        t_itl = os.path.join(d, "timesi.ttf")
        if os.path.exists(t_reg):
            try:
                pdfmetrics.registerFont(TTFont('ThemeSerif', t_reg))
                FONT_SERIF_REGULAR = 'ThemeSerif'
                if os.path.exists(t_bld):
                    pdfmetrics.registerFont(TTFont('ThemeSerif-Bold', t_bld))
                    FONT_SERIF_BOLD = 'ThemeSerif-Bold'
                else:
                    FONT_SERIF_BOLD = 'ThemeSerif'
                if os.path.exists(t_itl):
                    pdfmetrics.registerFont(TTFont('ThemeSerif-Italic', t_itl))
                    FONT_SERIF_ITALIC = 'ThemeSerif-Italic'
                else:
                    FONT_SERIF_ITALIC = 'ThemeSerif'
                break
            except Exception:
                pass
    for d in base_dirs:
        a_reg = os.path.join(d, "arial.ttf")
        a_bld = os.path.join(d, "arialbd.ttf")
        if os.path.exists(a_reg):
            try:
                pdfmetrics.registerFont(TTFont('ThemeSans', a_reg))
                FONT_SANS_REGULAR = 'ThemeSans'
                if os.path.exists(a_bld):
                    pdfmetrics.registerFont(TTFont('ThemeSans-Bold', a_bld))
                    FONT_SANS_BOLD = 'ThemeSans-Bold'
                else:
                    FONT_SANS_BOLD = 'ThemeSans'
                break
            except Exception:
                pass

_init_theme_fonts()

# Classical Accuracy Imports
from app.engine.core_matrix_engine import (
    calculate_driver,
    calculate_conductor,
    calculate_conductor_details,
    calculate_chaldean_name,
    generate_core_matrix_profile
)
from app.config.pricing_config import REPORT_TIERS, SUPPORTED_REPORT_TOPICS
from app.engine.vedic_gharelu_remedies import (
    PLANETARY_GHARELU_REMEDIES,
    UNIVERSAL_AURA_CLEANSING,
    get_gharelu_remedies_for_chart
)
from app.engine.complementary_poorak_engine import (
    DAY8_QUALITY_COMPLEMENTARY_REGISTRY,
    calculate_complementary_poorak
)
from app.engine.forecast_engine import (
    generate_detailed_annual_matrix,
    calculate_blessing_years
)
from app.engine.asset_numerology_engine import (
    analyze_mobile_number,
    analyze_vehicle_number,
    analyze_property_number
)

# ── BRAND COLOR PALETTE ──────────────────────────────────────────────────
COLOR_PEARL_BG   = colors.HexColor("#FFFDF7")
COLOR_PEARL_MID  = colors.HexColor("#F7F3EA")
COLOR_GOLD_DARK  = colors.HexColor("#8B6914")
COLOR_GOLD       = colors.HexColor("#C9A227")
COLOR_GOLD_LIGHT = colors.HexColor("#E2B84B")
COLOR_INK_DARK   = colors.HexColor("#523E28")
COLOR_INK_MUTED  = colors.HexColor("#7A654D")
COLOR_EMERALD    = colors.HexColor("#16835B")
COLOR_BORDER     = colors.HexColor("#EEDDB8")
COLOR_CARD_BG    = colors.HexColor("#FFFFFF")
COLOR_RED_ALERT  = colors.HexColor("#A13030")

# ── TYPOGRAPHY & STYLES ───────────────────────────────────────────────────
def _build_styles() -> Dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=base['Normal'],
        fontName=FONT_SERIF_BOLD,
        fontSize=24,
        leading=28,
        textColor=COLOR_GOLD_DARK,
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=base['Normal'],
        fontName=FONT_SERIF_REGULAR,
        fontSize=10,
        leading=14,
        textColor=COLOR_INK_MUTED,
        alignment=1,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=base['Normal'],
        fontName=FONT_SERIF_BOLD,
        fontSize=14,
        leading=17,
        textColor=COLOR_GOLD_DARK,
        spaceBefore=0,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=base['Normal'],
        fontName=FONT_SERIF_BOLD,
        fontSize=10.5,
        leading=13,
        textColor=COLOR_INK_DARK,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=base['Normal'],
        fontName=FONT_SERIF_REGULAR,
        fontSize=8.5,
        leading=11.5,
        textColor=COLOR_INK_DARK,
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        'ReportBodyBold',
        parent=body_style,
        fontName=FONT_SERIF_BOLD
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=base['Normal'],
        fontName=FONT_SERIF_BOLD,
        fontSize=8.5,
        leading=11,
        textColor=COLOR_GOLD_DARK
    )

    meta_val = ParagraphStyle(
        'MetaValue',
        parent=base['Normal'],
        fontName=FONT_SERIF_REGULAR,
        fontSize=8.5,
        leading=11,
        textColor=COLOR_INK_DARK
    )

    tbl_header = ParagraphStyle(
        'TableHeader',
        parent=base['Normal'],
        fontName=FONT_SERIF_BOLD,
        fontSize=8.5,
        leading=11,
        textColor=COLOR_GOLD_DARK,
        alignment=1
    )

    tbl_cell = ParagraphStyle(
        'TableCell',
        parent=base['Normal'],
        fontName=FONT_SERIF_REGULAR,
        fontSize=8.2,
        leading=11,
        textColor=COLOR_INK_DARK
    )

    tbl_cell_dense = ParagraphStyle(
        'TableCellDense',
        parent=base['Normal'],
        fontName=FONT_SERIF_REGULAR,
        fontSize=7.2,
        leading=9.2,
        textColor=COLOR_INK_DARK
    )

    tbl_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=tbl_cell,
        alignment=1
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=base['Normal'],
        fontName=FONT_SERIF_ITALIC,
        fontSize=8.5,
        leading=12,
        textColor=COLOR_INK_DARK
    )

    return {
        'CoverTitle': title_style,
        'CoverSubtitle': subtitle_style,
        'SectionH1': h1_style,
        'SectionH2': h2_style,
        'ReportBody': body_style,
        'ReportBodyBold': body_bold,
        'MetaLabel': meta_label,
        'MetaValue': meta_val,
        'TableHeader': tbl_header,
        'TableCell': tbl_cell,
        'TableCellDense': tbl_cell_dense,
        'TableCellCenter': tbl_cell_center,
        'CalloutText': callout_style
    }

# ── CANVAS & BACKGROUND MANAGEMENT ────────────────────────────────────────
def draw_page_background(canvas_obj, doc):
    canvas_obj.saveState()
    w, h = doc.pagesize
    # 1. Background tint
    canvas_obj.setFillColor(COLOR_PEARL_BG)
    canvas_obj.rect(0, 0, w, h, fill=1, stroke=0)

    # 2. Celestial Geometric Watermark
    cx, cy = w / 2.0, h / 2.0
    canvas_obj.saveState()
    canvas_obj.setStrokeColor(colors.Color(0.79, 0.64, 0.15, alpha=0.065))
    canvas_obj.setLineWidth(0.6)
    canvas_obj.circle(cx, cy, 60, stroke=1, fill=0)
    canvas_obj.circle(cx, cy, 100, stroke=1, fill=0)
    canvas_obj.circle(cx, cy, 145, stroke=1, fill=0)
    for i in range(16):
        ang = i * (2.0 * math.pi / 16.0)
        canvas_obj.line(cx + 65 * math.cos(ang), cy + 65 * math.sin(ang),
                        cx + 140 * math.cos(ang), cy + 140 * math.sin(ang))

    # Inner 8-pointed star yantra
    canvas_obj.setStrokeColor(colors.Color(0.55, 0.41, 0.08, alpha=0.075))
    canvas_obj.setLineWidth(0.8)
    canvas_obj.rect(cx - 20, cy - 20, 40, 40, stroke=1, fill=0)
    canvas_obj.rect(cx - 14, cy - 14, 28, 28, stroke=1, fill=0)

    # 3. Official Logo Mark Image Watermark (Approved centered watermark at 7% opacity)
    logo_file = os.path.join(os.path.dirname(__file__), "..", "assets", "nv-logo-mark.png")
    if not os.path.exists(logo_file):
        logo_file = os.path.join(os.path.dirname(__file__), "..", "static", "logos", "nv-logo-mark.png")
    if not os.path.exists(logo_file):
        logo_file = os.path.join("app", "static", "logos", "nv-logo-mark.png")
    if not os.path.exists(logo_file):
        logo_file = os.path.join("pdf_service", "app", "assets", "nv-logo-mark.png")

    if os.path.exists(logo_file):
        try:
            canvas_obj.setFillAlpha(0.07)  # 7% opacity (within approved 6-8% band)
            img_size = 220
            canvas_obj.drawImage(logo_file, cx - img_size / 2, cy - img_size / 2,
                                 width=img_size, height=img_size, mask='auto',
                                 preserveAspectRatio=True)
        except Exception:
            pass

    canvas_obj.restoreState()
    canvas_obj.restoreState()


class NumerosReportCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages: int):
        self.saveState()
        w, h = self._pagesize

        # 1. Luxury Double Gold Document Frame
        self.setStrokeColor(COLOR_GOLD)
        self.setLineWidth(1.1)
        self.rect(18, 18, w - 36, h - 36, stroke=1, fill=0)

        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.rect(21, 21, w - 42, h - 42, stroke=1, fill=0)

        # 2. Running Header
        logo_icon = os.path.join(os.path.dirname(__file__), "..", "static", "logos", "nv-logo-mark.png")
        if not os.path.exists(logo_icon):
            logo_icon = os.path.join("app", "static", "logos", "anveil-charm-square.png")
        if os.path.exists(logo_icon):
            try:
                self.drawImage(logo_icon, 34, h - 31, width=13, height=13, mask='auto', preserveAspectRatio=True)
            except Exception:
                pass

        self.setFont(FONT_SERIF_BOLD, 8)
        self.setFillColor(COLOR_GOLD_DARK)
        self.drawString(51, h - 28, "NUMEROS VISION")

        self.setFont(FONT_SERIF_ITALIC, 7.5)
        self.setFillColor(COLOR_INK_MUTED)
        self.drawString(136, h - 28, "·   ANVEIL EVERY CHARM")

        self.setFont(FONT_SERIF_REGULAR, 7.5)
        if total_pages == 3:
            self.setFillColor(COLOR_EMERALD)
            if self._pageNumber == 1:
                self.drawRightString(w - 34, h - 28, "BASIC 3-PAGE EDITION · PAGE 1 · FOUNDATIONAL PROFILE")
            elif self._pageNumber == 2:
                self.drawRightString(w - 34, h - 28, "BASIC 3-PAGE EDITION · PAGE 2 · 8 ELEMENTAL PLANES & RAJ YOGAS")
            else:
                self.drawRightString(w - 34, h - 28, "BASIC 3-PAGE EDITION · PAGE 3 · 5-ELEMENT BALANCING & ROADMAP")
        else:
            self.setFillColor(COLOR_INK_MUTED)
            if self._pageNumber > 1:
                self.drawRightString(w - 34, h - 28, "CONFIDENTIAL EXECUTIVE DOSSIER")

        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(34, h - 33, w - 34, h - 33)

        # 3. Running Footer
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(34, 38, w - 34, 38)

        self.setFont(FONT_SERIF_REGULAR, 7.5)
        self.setFillColor(COLOR_INK_MUTED)
        self.drawString(34, 26, "Numeros Vision — ANVEIL EVERY CHARM")

        self.setFont(FONT_SERIF_BOLD, 8)
        self.setFillColor(COLOR_GOLD_DARK)
        self.drawCentredString(w / 2.0, 26, "— VERIFIED ROYAL SEAL —")

        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(w - 34, 26, page_str)

        self.restoreState()


# ── DETERMINISTIC CALCULATION ENGINE ───────────────────────────────────────
def run_deterministic_calculation(
    name: str,
    day: int,
    month: int,
    year: int,
    topic_id: str = "core_blueprint",
    tier: str = "basic",
    mobile_number: Optional[str] = None,
    vehicle_number: Optional[str] = None,
    property_number: Optional[str] = None,
    purchase_date: Optional[Union[str, datetime.date, datetime.datetime]] = None,
    purchase_year: Optional[int] = None,
    gender: Optional[str] = "male",
    edition: str = "india"
) -> Dict[str, Any]:
    clean_name = name.strip() or "Seeker"

    # 1. Driver & Conductor (Core Matrix Engine canonical rule)
    driver = calculate_driver(day)
    conductor_details = calculate_conductor_details(day, month, year)
    conductor = conductor_details["conductor_raw"]
    conductor_root = conductor_details["conductor_root"]
    conductor_display = conductor_details["conductor_display"]

    # 2. Chaldean Name Reduction
    chaldean_res = calculate_chaldean_name(clean_name)
    c_compound = chaldean_res.get("compound", 32)
    c_root = chaldean_res.get("root", 5)

    # 3. Pythagorean Name Reduction
    pyth_map = {
        'A':1,'J':1,'S':1, 'B':2,'K':2,'T':2, 'C':3,'L':3,'U':3,
        'D':4,'M':4,'V':4, 'E':5,'N':5,'W':5, 'F':6,'O':6,'X':6,
        'G':7,'P':7,'Y':7, 'H':8,'Q':8,'Z':8, 'I':9,'R':9
    }
    pyth_sum = sum(pyth_map.get(ch, 0) for ch in clean_name.upper() if ch.isalpha())
    p_temp = pyth_sum
    while p_temp > 9 and p_temp not in (11, 22, 33):
        p_temp = sum(int(d) for d in str(p_temp))
    pyth_root = sum(int(d) for d in str(p_temp)) if p_temp > 9 else p_temp

    # 4. Kua Number (Male 1981: 10 - sum(8+1=9) = 1)
    y_sum = sum(int(d) for d in str(year)[-2:])
    while y_sum > 9:
        y_sum = sum(int(d) for d in str(y_sum))
    kua = 10 - y_sum
    if kua <= 0: kua += 9

    # Resolve purchase / target year dynamically from purchase_date / purchase_year / datetime.now()
    if purchase_year:
        target_year = int(purchase_year)
    elif purchase_date:
        if isinstance(purchase_date, (datetime.date, datetime.datetime)):
            target_year = purchase_date.year
        elif isinstance(purchase_date, str):
            clean_date = purchase_date.strip()[:10]
            try:
                target_year = datetime.date.fromisoformat(clean_date).year
            except Exception:
                target_year = datetime.datetime.now().year
        else:
            target_year = datetime.datetime.now().year
    else:
        target_year = datetime.datetime.now().year

    # 5. Personal Year: (Day + Month + target_year)
    py_sum = driver + (sum(int(d) for d in str(month))) + (sum(int(d) for d in str(target_year)))
    while py_sum > 9:
        py_sum = sum(int(d) for d in str(py_sum))
    personal_year = py_sum

    # 6. Lo Shu Digits & Counts
    dob_digits = [int(d) for d in f"{day:02d}{month:02d}{year}" if d != '0']
    counts = {i: 0 for i in range(1, 10)}
    for d in dob_digits:
        counts[d] += 1
    present_numbers = [k for k, v in counts.items() if v > 0]
    missing_numbers = [k for k, v in counts.items() if v == 0]

    # Lo Shu Planes Definition
    planes = [
        ("Mental Plane (4-9-2)", [4, 9, 2]),
        ("Emotional Plane (3-5-7)", [3, 5, 7]),
        ("Practical Plane (8-1-6)", [8, 1, 6]),
        ("Thought Plane (4-3-8)", [4, 3, 8]),
        ("Will Plane (9-5-1)", [9, 5, 1]),
        ("Action Plane (2-7-6)", [2, 7, 6]),
        ("Golden Silver Wealth (4-5-6)", [4, 5, 6]),
        ("Silver Property (2-5-8)", [2, 5, 8])
    ]
    completed_planes = [p for p in planes if all(x in present_numbers for x in p[1])]

    PLANETS = {
        1: "Sun (Surya)",
        2: "Moon (Chandra)",
        3: "Jupiter (Brihaspati)",
        4: "Rahu (North Node)",
        5: "Mercury (Budh)",
        6: "Venus (Shukra)",
        7: "Ketu (South Node)",
        8: "Saturn (Shani)",
        9: "Mars (Mangal)"
    }

    report_id = "NV-" + hashlib.sha256(f"{clean_name}:{day}-{month}-{year}:{tier}:{topic_id}".encode()).hexdigest()[:10].upper()
    dob_formatted = f"{day:02d}-{month:02d}-{year}"

    # Poorak Number Calculation (Complementary Key uses reduced root 1..9)
    poorak_info = calculate_complementary_poorak(driver, conductor_root, missing_numbers)

    # Gharelu Vedic Remedies Calculation
    gharelu_remedies = get_gharelu_remedies_for_chart(driver, conductor_root, present_numbers, missing_numbers)

    # 7. Asset & Digital Identifiers Analysis
    mobile_res = analyze_mobile_number(mobile_number, driver, conductor_root) if mobile_number else None
    vehicle_res = analyze_vehicle_number(vehicle_number, driver, conductor_root) if vehicle_number else None
    property_res = analyze_property_number(property_number, driver, conductor_root) if property_number else None

    # 8. Annual 12-Month Matrix & Blessing Years
    current_year = target_year
    current_age = max(18, current_year - year)
    annual_matrix = generate_detailed_annual_matrix(day, month, current_year)
    blessing_data = calculate_blessing_years(day, month, year, current_age)

    return {
        "current_year": current_year,
        "target_year": current_year,
        "personal_year": personal_year,
        "personal_year_theme": annual_matrix.get("personal_year_theme") or PERSONAL_YEAR_INTERPRETATIONS.get(personal_year, {}).get("theme", "Foundation & Structural Infrastructure"),
        "personal_year_label": f"Personal Year {personal_year}",
        "annual_matrix": annual_matrix,
        "blessing_years": blessing_data,
        "mobile_number": mobile_number,
        "mobile_analysis": mobile_res,
        "vehicle_number": vehicle_number,
        "vehicle_analysis": vehicle_res,
        "property_number": property_number,
        "property_analysis": property_res,
        "report_id": report_id,
        "seeker_name": clean_name,
        "day": day,
        "month": month,
        "year": year,
        "dob_formatted": dob_formatted,
        "driver_number": driver,
        "driver_planet": PLANETS.get(driver, "Sun (Surya)"),
        "conductor_number": conductor,
        "conductor_root": conductor_root,
        "conductor_display": conductor_display,
        "conductor_planet": PLANETS.get(conductor_root, "Sun (Surya)"),
        "chaldean_name_compound": c_compound,
        "chaldean_name_root": c_root,
        "chaldean_name_planet": PLANETS.get(c_root, "Mercury"),
        "pythagorean_name_root": pyth_root,
        "pythagorean_name_planet": PLANETS.get(pyth_root, "Saturn"),
        "kua_number": kua,
        "kua_element": "Water · Kan (East Group)",
        "personal_year": personal_year,
        "personal_year_theme": "Foundation & Structural Infrastructure",
        "counts": counts,
        "present_numbers": present_numbers,
        "missing_numbers": missing_numbers,
        "completed_planes": completed_planes,
        "poorak_info": poorak_info,
        "gharelu_remedies": gharelu_remedies,
        "topic_id": topic_id,
        "tier": tier,
        "gender": (gender or "male"),
        "edition": (edition or "india")
    }


class NumerosPdfReportBuilder:
    def __init__(self, calculation_data: Dict[str, Any], tier: str = "basic", topic_id: str = "core_blueprint"):
        self.data = calculation_data
        self.tier = tier.lower().strip()
        self.topic_id = self._normalize_topic(topic_id)
        self.styles = _build_styles()
        self.story = []
        try:
            from app.engine.nv_psychology_engine import nv_think_engine
            self.nv_think = nv_think_engine.evaluate_chart_synthesis(
                driver=self.data.get('driver', 1),
                conductor=self.data.get('conductor', 4),
                loshu_counts=self.data.get('loshu_counts', {}),
                active_planes=self.data.get('active_planes', []),
                missing_numbers=self.data.get('missing_numbers', []),
                user_environment="Executive / Professional Career Context"
            )
        except Exception:
            self.nv_think = {}

    def _normalize_topic(self, topic: str) -> str:
        t = (topic or "").lower().strip()
        is_advanced_only = self.tier in ("advanced", "report_advanced", "master", "report_master")
        if any(k in t for k in ("present", "lo_shu", "loshu")):
            return "present_numbers"
        elif any(k in t for k in ("love", "romance", "marriage", "partner", "spouse", "companionship")):
            return "love_relationship"
        elif any(k in t for k in ("career", "wealth", "business", "billionaire", "venture", "job", "work")):
            return "career_wealth"
        elif any(k in t for k in ("health", "vitality", "ayurved")):
            return "health_vitality"
        elif is_advanced_only:
            # In the 12-page Advanced Master Dossier (Rs 489), Enabled/Present Numbers in Depth
            # is the default analytical focus; Missing Numbers in Depth and Full Name Balancing
            # are exclusively in the 32-page Premium Sovereign Blueprint (Rs 1,050).
            return "present_numbers"
        elif any(k in t for k in ("name", "spelling", "acoustic")):
            return "name_balancing"
        elif any(k in t for k in ("vastu", "spatial", "feng_shui", "property")):
            return "vastu_spatial"
        else:
            return "missing_numbers_vastu"

    def _get_topic_meta(self) -> Dict[str, Any]:
        t = self.topic_id
        is_premium = self.tier in ("premium", "report_premium", "divine", "roadmap", "report_divine")
        is_advanced = self.tier in ("advanced", "report_advanced", "master", "report_master")

        if t == "present_numbers":
            title = "ACTIVE CHARM PRESENT NUMBERS REPORT"
            subtitle = "12-Page Present Numbers Master Dossier · Benefic vs Malefic & Inborn Career Mastery" if not is_premium else "32-Page Sovereign Roadmap · Complete Natal Numbers Compendium"
            badge = "ADVANCED MASTER DOSSIER · 12-PAGE PRESENT NUMBERS DOSSIER · ₹489" if not is_premium else "PREMIUM SOVEREIGN BLUEPRINT · 32-PAGE SOVEREIGN ROADMAP · ₹1,050"
            sec3 = "Section 3: Natal Present Numbers Deep Audit & Frequency Analysis"
            sec4 = "Section 4: Present Numbers Benefic vs Malefic Planetary Operating Matrix"
            sec5 = "Section 5: Inborn Career Fruitfulness & High-Yield Vocations"
        elif t == "love_relationship":
            title = "LOVE, RELATIONSHIP & COMPANIONSHIP DOSSIER"
            subtitle = "Romantic Synastry, Marriage Timing Windows & Domestic Harmony Blueprint"
            badge = "ADVANCED MASTER DOSSIER · LOVE & COMPANIONSHIP (12 PAGES · ₹489)" if not is_premium else "PREMIUM SOVEREIGN BLUEPRINT · LIFETIME UNION ROADMAP (32 PAGES · ₹1,050)"
            sec3 = "Section 3: Love Style, Romantic Resonance & Spousal Temperament"
            sec4 = "Section 4: Ideal Partner Compatibility & Vedic Synastry Matrix (1 to 9)"
            sec5 = "Section 5: Marriage Timing Windows, Numerology Dasha & Domestic Harmony"
        elif t == "career_wealth":
            title = "CAREER, ENTERPRISE & FINANCIAL DIRECTION DOSSIER"
            subtitle = "High-Growth Vocations, Commercial Timing & Wealth Compounding Radar"
            badge = "ADVANCED MASTER DOSSIER · CAREER & WEALTH (12 PAGES · ₹489)" if not is_premium else "PREMIUM SOVEREIGN BLUEPRINT · ENTERPRISE ROADMAP (32 PAGES · ₹1,050)"
            sec3 = "Section 3: High-Growth Enterprise Vocations & Programmatic Scale"
            sec4 = f"Section 4: Commercial Timing Corridors & 5-Year Numerology Dasha Radar ({self.data.get('current_year', datetime.datetime.now().year)}–{self.data.get('current_year', datetime.datetime.now().year)+4})"
        
            sec5 = "Section 5: Strategic Reputation, Co-Founder Matching & Corporate Naming"
        elif t == "health_vitality":
            title = "HEALTH, VITALITY & AYURVEDIC CHRONOBIOLOGY DOSSIER"
            subtitle = "Pitta-Vata Balancing, Circadian Peak Hours & Non-Invasive Lifestyle Cures"
            badge = "ADVANCED MASTER DOSSIER · HEALTH & VITALITY (12 PAGES · ₹489)" if not is_premium else "PREMIUM SOVEREIGN BLUEPRINT · VITALITY COMPENDIUM (32 PAGES · ₹1,050)"
            sec3 = "Section 3: Ayurvedic Chronobiology & Pitta-Vata Dosha Balancing"
            sec4 = "Section 4: Circadian Peak Performance Windows & Hydration Protocols"
            sec5 = "Section 5: Cognitive Decompression, Sleep Restoration & Vitality Cures"
        else: # missing_numbers_vastu & core_blueprint
            title = "ANVEIL CHARM MISSING NUMBERS SOVEREIGN ROADMAP"
            subtitle = "32-Page Sovereign Lifetime Architecture & Missing Number Rectification Compendium" if is_premium else "12-Page Master Synthesis Dossier & Missing Numbers Rectification"
            badge = "PREMIUM SOVEREIGN BLUEPRINT · 32-PAGE SOVEREIGN ROADMAP · ₹1,050" if is_premium else "ADVANCED MASTER DOSSIER · 12-PAGE MASTER DOSSIER · ₹489"
            sec3 = "Section 3: Missing Numbers Deep Void Diagnosis & Elemental Gaps"
            sec4 = "Section 4: Name Balancing, Acoustic Spelling & Poorak Numbers Activation"
            sec5 = "Section 5: Element Yogas Balancing — Golden Raj Yoga & Silver Earth Plane"

        toc_12 = [
            ("Section 1: Executive Summary & Destiny Signature", "Page 3"),
            ("Section 2: Natal Lo Shu 3×3 Grid & 8 Elemental Planes", "Page 4"),
            (sec3, "Page 5"),
            (sec4, "Page 6"),
            (sec5, "Page 7"),
            ("Section 6: Interpersonal Synergy, Co-Founder Matching & Synastry", "Page 8"),
            ("Section 7: Auspicious Initiation Windows & Muhurat Timing", "Page 9"),
            ("Section 8: Vedic Gharelu Remedies Bank & 40-Day Aura Cleansing", "Page 10"),
            ("Section 9: Spatial Feng Shui & Kua Number 1 Directional Blueprint", "Page 11"),
            ("Section 10: Methodology, Authentic Standards & Ethical Guidance", "Page 12")
        ]

        toc_part1 = [
            ("Section 1: Executive Summary & Destiny Signature", "Page 3"),
            ("Section 2: Natal Lo Shu 3×3 Grid & 8 Elemental Planes", "Page 4"),
            (sec3, "Page 5"),
            (sec4, "Page 6"),
            (sec5, "Page 7"),
            ("Section 6: Interpersonal Synergy & Co-Founder Matching", "Page 8"),
            ("Section 7: Auspicious Initiation Windows & Muhurat Timing", "Page 9"),
            ("Section 8: Vedic Gharelu Remedies Bank & Aura Cleansing", "Page 10"),
            ("Section 9: Spatial Feng Shui & Kua 1 Directional Blueprint", "Page 11"),
            ("Section 10: Methodology & Authentic Standards", "Page 12"),
            ("Section 11: 81-Pair Archetype Matrix — Sun 1 + Rahu 4", "Page 13"),
            ("Section 12: Dual-System Synthesis — Chaldean vs Pythagorean", "Page 14"),
            ("Section 13: 10-Year Macro Planetary Timing Radar", "Page 15"),
            ("Section 14: Karmic Debt & Elemental Gaps Diagnosis", "Page 16"),
            ("Section 15: Full Name Balancing & Poorak Numbers Protocol", "Page 17")
        ]

        toc_part2 = [
            ("Section 16: Element Yogas Balancing — Golden Raj Yoga 4-5-6", "Page 18"),
            ("Section 17: High-Growth Enterprise Scaling Architecture", "Page 19"),
            ("Section 18: Month-by-Month Auspicious Timing & Monthly Remedies Radar", "Page 20"),
            ("Section 19: Your Angel Numbers, Sacred Synchronicity & Divine Signals", "Page 21"),
            ("Section 20: Digital Footprint — Mobile, Email & PIN Calibration", "Page 22"),
            ("Section 21: Family Dynasty & Intergenerational Synergy", "Page 23"),
            ("Section 22: Relationship Harmony & Spousal Synastry", "Page 24"),
            ("Section 23: Health, Vitality & Ayurvedic Chronobiology", "Page 25"),
            ("Section 24: Career Transmutation & Board Advisory", "Page 26"),
            ("Section 25: Real Estate, Vehicle & Property / Flat Harmonization", "Page 27"),
            ("Section 26: Global Horizons & Cross-Border Expansion", "Page 28"),
            ("Section 27: Creative Authority & Thought Leadership", "Page 29"),
            ("Section 28: Blessing Years Timeline & Auspicious Life Milestone Transitions", "Page 30"),
            ("Section 29: 4-Stage Pinnacle Cycles & Life Challenges", "Page 31"),
            ("Section 30: Your Favourable Directions, Spatial Harmony & Elemental Alignment", "Page 32")
        ]

        return {
            "title": title,
            "subtitle": subtitle,
            "badge": badge,
            "sec3": sec3,
            "sec4": sec4,
            "sec5": sec5,
            "toc_12": toc_12,
            "toc_part1": toc_part1,
            "toc_part2": toc_part2
        }

    def build(self) -> bytes:
        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=38,
            rightMargin=38,
            topMargin=46,
            bottomMargin=46
        )

        if self.tier in ("basic", "report_basic", "report_essential"):
            self._assemble_basic_3_pages()
        elif self.tier in ("advanced", "report_advanced", "master", "report_master"):
            self._assemble_advanced_12_pages()
        elif self.tier in ("premium", "report_premium", "divine", "roadmap", "report_divine"):
            self._assemble_premium_32_pages()
        else:
            self._assemble_basic_3_pages()

        doc.build(
            self.story,
            canvasmaker=NumerosReportCanvas,
            onFirstPage=draw_page_background,
            onLaterPages=draw_page_background
        )
        return buf.getvalue()

    def _create_loshu_grid_table(self) -> Table:
        s = self.styles
        cnts = self.data["counts"]

        def cell_txt(num, elem):
            c = cnts.get(num, 0)
            if c > 0:
                repeated = str(num) * c
                return Paragraph(f"<font size=11 color='#8B6914'><b>{repeated}</b></font><br/><font size=7 color='#16835B'><b>Present ×{c}</b></font><br/><font size=7 color='#7A654D'>{elem}</font>", s['TableCellCenter'])
            else:
                return Paragraph(f"<font size=8 color='#8B6914'><b>OPEN · ANVEIL CHARM</b></font><br/><font size=10 color='#523E28'><b>{num}</b></font><br/><font size=7 color='#7A654D'>{elem} · Unsealed</font>", s['TableCellCenter'])

        grid_data = [
            [cell_txt(4, "Wood · Wealth"), cell_txt(9, "Fire · Fame"), cell_txt(2, "Earth · Marriage")],
            [cell_txt(3, "Wood · Family"), cell_txt(5, "Earth · Center"), cell_txt(7, "Metal · Creativity")],
            [cell_txt(8, "Earth · Knowledge"), cell_txt(1, "Water · Career"), cell_txt(6, "Metal · Luxury")]
        ]

        t = Table(grid_data, colWidths=[172, 172, 172], rowHeights=[44, 44, 44])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
            ('BOX', (0,0), (-1,-1), 1.5, COLOR_GOLD),
            ('INNERGRID', (0,0), (-1,-1), 0.8, COLOR_BORDER),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ]))
        return t

    def _add_cover_page(self, subtitle: str, badge_text: str, custom_title: Optional[str] = None):
        s = self.styles
        d = self.data

        self.story.append(Spacer(1, 6))
        logo_path = os.path.join(os.path.dirname(__file__), "..", "static", "logos", "nv-logo-mark.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join("app", "static", "logos", "nv-logo-mark.png")
        if os.path.exists(logo_path):
            img_tbl = Table([[Image(logo_path, width=54, height=54)]], colWidths=[516], hAlign='CENTER')
            img_tbl.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ]))
            self.story.append(img_tbl)

        self.story.append(Paragraph("NUMEROS VISION", s['CoverTitle']))
        sub_heading = custom_title or "ANVEIL EVERY CHARM · CLASSICAL NUMEROLOGICAL ARCHITECTURE"
        self.story.append(Paragraph(sub_heading, s['CoverSubtitle']))
        self.story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_GOLD, spaceBefore=4, spaceAfter=14))

        badge_table = Table([[
            Paragraph(f"<font size=9 color='#8B6914'><b>{badge_text}</b></font>", s['TableCellCenter'])
        ]], colWidths=[516])
        badge_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 1, COLOR_GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        self.story.append(badge_table)
        self.story.append(Spacer(1, 24))

        meta_rows = [
            [Paragraph("<b>Recipient Full Name</b>", s['MetaLabel']), Paragraph(f": <b>{d['seeker_name']}</b>", s['MetaValue'])],
            [Paragraph("<b>Verified Date of Birth</b>", s['MetaLabel']), Paragraph(f": {d['dob_formatted']} (Recorded at 04:15 PM, New Delhi)", s['MetaValue'])],
            [Paragraph("<b>Driver Vector (Mulank)</b>", s['MetaLabel']), Paragraph(f": <b>{d['driver_number']} · {d['driver_planet']}</b> (Solar Executive Will)", s['MetaValue'])],
            [Paragraph("<b>Conductor Vector (Bhagyank)</b>", s['MetaLabel']), Paragraph(f": <b>{d.get('conductor_display', d['conductor_number'])} · {d['conductor_planet']}</b> (Architectural Systems)", s['MetaValue'])],
            [Paragraph("<b>Acoustic Calling Name</b>", s['MetaLabel']), Paragraph(f": <b>{d['chaldean_name_compound']} → {d['chaldean_name_root']} · {d['chaldean_name_planet']}</b> (Star of the Lion)", s['MetaValue'])],
            [Paragraph("<b>Kua Directional Vector</b>", s['MetaLabel']), Paragraph(f": <b>{d['kua_number']} · {d['kua_element']}</b>", s['MetaValue'])],
            [Paragraph("<b>Personal Year Transit</b>", s['MetaLabel']), Paragraph(f": <b>{d['personal_year']} · {d['personal_year_theme']}</b>", s['MetaValue'])],
            [Paragraph("<b>Report Verification ID</b>", s['MetaLabel']), Paragraph(f": {d['report_id']}", s['MetaValue'])],
            [Paragraph("<b>Verification Standard</b>", s['MetaLabel']), Paragraph(": Authentic Numerology Matrix · Verified & Confidential", s['MetaValue'])],
        ]
        t_meta = Table(meta_rows, colWidths=[170, 346])
        t_meta.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1.2, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        self.story.append(t_meta)
        self.story.append(Spacer(1, 24))

        callout_p = Paragraph(
            f"<b>Authentic Methodology Notice:</b> This personalized publication is calculated directly from the birth coordinates of <b>{d['seeker_name']}</b>. All number calculations, dasha cycles, and Lo Shu grid mappings follow classical numerology standards. Interpretations provide positive, practical life insights without fatalism or superstition. Consult accredited professionals for legal or medical advice.",
            s['CalloutText']
        )
        t_callout = Table([[callout_p]], colWidths=[516])
        t_callout.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
        ]))
        self.story.append(t_callout)

    # ── BASIC REPORT: EXACTLY 3 PAGES ─────────────────────────────────────────
    def _assemble_basic_3_pages(self):

        s = self.styles
        d = self.data
        cnts = d.get("counts", {})
        missing = d.get("missing_numbers", [])
        driver = d.get("driver_number", 1)
        conductor = d.get("conductor_number", 4)
        conductor_root = d.get("conductor_root", 4)
        c_root = d.get("chaldean_name_root", 5)
        c_compound = d.get("chaldean_name_compound", 32)
        kua = d.get("kua_number", 1)
        gender = d.get("gender", "male")
        edition = d.get("edition", "india")
        name = d.get("seeker_name", "Seeker").upper()
        dob = d.get("dob_formatted", "1981-11-28")
        day_num = d.get("day", 28)
        py = d.get("personal_year", 4)

        # Styles
        s_top_star = ParagraphStyle('TopStar', parent=s['ReportBody'], fontName=FONT_SERIF_BOLD, fontSize=8, leading=10, textColor=COLOR_GOLD_DARK, alignment=1)
        s_name = ParagraphStyle('Name', parent=s['ReportBody'], fontName=FONT_SERIF_BOLD, fontSize=20, leading=23, textColor=COLOR_GOLD_DARK, alignment=1)
        s_sub = ParagraphStyle('Sub', parent=s['ReportBody'], fontName=FONT_SERIF_REGULAR, fontSize=9, leading=11, textColor=COLOR_INK_DARK, alignment=1)

        s_pill_lbl = ParagraphStyle('PillLbl', parent=s['ReportBody'], fontName=FONT_SERIF_REGULAR, fontSize=6.5, leading=8.5, textColor=COLOR_INK_MUTED, alignment=1)
        s_card_h = ParagraphStyle('CardH', parent=s['ReportBody'], fontName=FONT_SERIF_BOLD, fontSize=8, leading=10, textColor=COLOR_GOLD_DARK)
        s_card_txt = ParagraphStyle('CardTxt', parent=s['ReportBody'], fontName=FONT_SERIF_REGULAR, fontSize=7.5, leading=10, textColor=COLOR_INK_DARK)
        s_cell_sub = ParagraphStyle('CellSub', parent=s['ReportBody'], fontName=FONT_SERIF_REGULAR, fontSize=6.5, leading=8, textColor=COLOR_INK_MUTED, alignment=1)
        s_gap_item = ParagraphStyle('GapItem', parent=s['ReportBody'], fontName=FONT_SERIF_REGULAR, fontSize=7, leading=9.5, textColor=COLOR_INK_DARK)
        s_alert = ParagraphStyle('Alert', parent=s['ReportBody'], fontName=FONT_SERIF_BOLD, fontSize=7, leading=9.5, textColor=COLOR_RED_ALERT)

        # ── PAGE 1: Foundational Profile, Readings & Lo Shu Grid ──
        self.story.append(Paragraph("BASIC REPORT · ELEMENT BALANCING &amp; FOUNDATIONAL BLUEPRINT", s_top_star))
        self.story.append(Spacer(1, 1))
        self.story.append(Paragraph(name, s_name))
        self.story.append(Spacer(1, 1))
        self.story.append(Paragraph(f"Foundational Planetary Frequency &amp; Lo Shu Grid Matrix ({edition.title()} Edition)", s_sub))
        self.story.append(Spacer(1, 2))

        logo_mark = os.path.join("app", "static", "logos", "nv-logo-mark.png")
        if not os.path.exists(logo_mark):
            logo_mark = os.path.join("app", "static", "logos", "anveil-charm-square.png")
        if os.path.exists(logo_mark):
            img_tbl = Table([[Image(logo_mark, width=32, height=32)]], colWidths=[520], hAlign='CENTER')
            img_tbl.setStyle(TableStyle([
                ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 1),
            ]))
            self.story.append(img_tbl)

        def _planet_geo(n: int) -> str:
            mapping = {
                1: "Sun (Surya)" if edition != "international" else "Sun",
                2: "Moon (Chandra)" if edition != "international" else "Moon",
                3: get_geo_label('guru', edition),
                4: get_geo_label('rahu', edition),
                5: get_geo_label('budh', edition),
                6: get_geo_label('shukra', edition),
                7: get_geo_label('ketu', edition),
                8: "Shani (Saturn)" if edition != "international" else "Saturn (Shani)",
                9: "Mangal (Mars)" if edition != "international" else "Mars (Mangal)",
            }
            return mapping.get(n, "Planetary Indicator")

        # 4 Metric Pills with Geo-Switching
        pills_data = [
            [
                Paragraph(f"{get_geo_label('driver', edition).upper()}<br/><font size=9.5 color='#16835B'><b>{driver} · {_planet_geo(driver)}</b></font>", s_pill_lbl),
                Paragraph(f"{get_geo_label('conductor', edition).upper()}<br/><font size=9.5 color='#16835B'><b>{d.get('conductor_display', conductor)} · {_planet_geo(conductor_root)}</b></font>", s_pill_lbl),
                Paragraph(f"{get_geo_label('kua', edition).upper()}<br/><font size=9.5 color='#16835B'><b>{kua} ({d.get('kua_element', 'East Group').split('·')[0].strip()})</b></font>", s_pill_lbl),
                Paragraph(f"{get_geo_label('calling_name', edition).upper()}<br/><font size=9.5 color='#16835B'><b>{c_root} ({c_compound})</b></font>", s_pill_lbl),
            ]
        ]
        t_pills = Table(pills_data, colWidths=[130, 130, 130, 130], rowHeights=[30])
        t_pills.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        self.story.append(t_pills)
        self.story.append(Spacer(1, 4))

        # Core Specific Readings from Content Library
        bd_read = CONTENT_LIB['topics']['birth_day'].get(str(driver), {}).get('depth_1_basic', {}).get('text', '')
        lp_entry = CONTENT_LIB['topics']['life_path'].get(str(conductor)) or CONTENT_LIB['topics']['life_path'].get(str(conductor_root), {})
        lp_read = lp_entry.get('depth_1_basic', {}).get('text', '')
        name_read = CONTENT_LIB['topics']['name_number'].get(str(c_root), {}).get('depth_1_basic', {}).get('text', '')
        dc_key = f"{driver}_{conductor_root}"
        dc_info = CONTENT_LIB['topics']['driver_conductor'].get(dc_key, {})
        dc_summary = dc_info.get('depth_1_basic', {}).get('summary', '')
        dc_rel = dc_info.get('relationship_type', 'Neutral')
        dc_rating = dc_info.get('star_rating', 3.5)

        readings_table = [
            [Paragraph(f"<b>• {get_geo_label('driver', edition)} {driver}:</b> {bd_read}", s_card_txt)],
            [Paragraph(f"<b>• {get_geo_label('conductor', edition)} {d.get('conductor_display', conductor)}:</b> {lp_read}", s_card_txt)],
            [Paragraph(f"<b>• {get_geo_label('calling_name', edition)} {c_root} ({c_compound}):</b> {name_read}", s_card_txt)],
            [Paragraph(f"<b>• {driver}–{conductor_root} Relationship ({dc_rel} · {dc_rating}/5):</b> {dc_summary}", s_card_txt)],
        ]
        t_readings = Table(readings_table, colWidths=[520])
        t_readings.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_PEARL_BG),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_readings)
        self.story.append(Spacer(1, 4))

        # Centered Lo Shu Grid
        self.story.append(Paragraph(f"<font size=8.5 color='#8B6914'><b>{get_geo_label('loshu_grid', edition).upper()} &amp; ELEMENTAL FREQUENCIES</b></font>", s_top_star))
        self.story.append(Spacer(1, 2))

        def ls_cell(num, elem):
            c = cnts.get(num, 0)
            if c == 0:
                return Paragraph(f"<font size=6 color='#A13030'><b>OPEN</b></font><br/><font size=10 color='#8C827A'><b>{num}</b></font><br/><font size=6 color='#7A654D'>{elem}</font>", s_cell_sub)
            else:
                rep = str(num) * c
                return Paragraph(f"<font size=6 color='#16835B'><b>×{c}</b></font><br/><font size=10 color='#523E28'><b>{rep}</b></font><br/><font size=6 color='#7A654D'>{elem}</font>", s_cell_sub)

        grid_rows = [
            [ls_cell(4, "Wood"), ls_cell(9, "Fire"), ls_cell(2, "Earth")],
            [ls_cell(3, "Wood"), ls_cell(5, "Earth"), ls_cell(7, "Metal")],
            [ls_cell(8, "Earth"), ls_cell(1, "Water"), ls_cell(6, "Metal")]
        ]
        t_loshu = Table(grid_rows, colWidths=[65, 65, 65], rowHeights=[32, 32, 32], hAlign='CENTER')
        t_loshu.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1.2, COLOR_GOLD),
            ('INNERGRID', (0,0), (-1,-1), 0.6, COLOR_BORDER),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        self.story.append(t_loshu)
        self.story.append(Spacer(1, 4))

        # Natal Gap Analysis Card
        gap_items = []
        GAP_MAP = {
            1: "Water · Sun: Keep written daily priorities and practice steady, clear self-expression.",
            2: "Earth · Moon: Build unhurried listening habits and supportive team check-ins.",
            3: f"Wood · {get_geo_label('guru', edition)}: Set aside regular study blocks and share practical knowledge.",
            4: f"Wood · {get_geo_label('rahu', edition)}: Keep checklists, tidy folders, and consistent weekly routines.",
            5: f"Earth · {get_geo_label('budh', edition)} / {get_geo_label('brahmasthan', edition)}: Keep midday pauses and steady task transitions.",
            6: f"Metal · {get_geo_label('shukra', edition)}: Maintain an uncluttered home corner and unhurried family time.",
            7: f"Metal · {get_geo_label('ketu', edition)}: Set aside quiet reading and reflection notes each week.",
            8: "Earth · Saturn: Track commitments in writing and review progress calmly each week.",
            9: "Fire · Mars: Break projects into small milestones so begun work reaches completion."
        }
        for m_num in missing:
            p_desc = GAP_MAP.get(m_num, "Open grid position suited to steady daily habit balance.")
            gap_items.append(Paragraph(f"<b>• Open {m_num}:</b> {p_desc}", s_gap_item))

        golden_missing = [n for n in (4, 5, 6) if n in missing]
        if golden_missing:
            gap_items.append(Paragraph(f"<b>▲ {get_geo_label('golden_raj_yoga', edition)} — Open Positions ({', '.join(str(n) for n in golden_missing)}):</b> Focus on steady planning and follow-through routines.", s_alert))
        else:
            gap_items.append(Paragraph(f"<b>• {get_geo_label('golden_raj_yoga', edition)} — Complete (4-5-6 Present):</b> Keep structured weekly reviews to sustain balanced momentum.", s_gap_item))

        gap_header_tbl = Table([
            [Paragraph(f"<b>• {get_geo_label('missing_numbers', edition).upper()} OVERVIEW ({dob})</b>", s_card_h),
             Paragraph(f"<font color='#A13030'><b>{len(missing)} OPEN POSITIONS</b></font>", ParagraphStyle('Badge', parent=s_card_h, alignment=2))]
        ], colWidths=[360, 150])
        gap_header_tbl.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE'), ('TOPPADDING', (0,0), (-1,-1), 0), ('BOTTOMPADDING', (0,0), (-1,-1), 0)]))

        gap_table_content = [
            [gap_header_tbl],
            [Paragraph(f"For <b>{d['seeker_name']}</b> ({dob}), open birth-date positions are <b>[{', '.join(str(n) for n in missing) or 'None'}]</b>, guiding the everyday habit focus below:", s_card_txt)],
        ]
        for item in gap_items:
            gap_table_content.append([item])

        t_gap = Table(gap_table_content, colWidths=[520])
        t_gap.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_gap)

        # ── PAGE 2: 8 Elemental Planes & 5-Element Equilibrium Audit ──
        self.story.append(PageBreak())
        self.story.append(Paragraph(f"8 PLANES OF {get_geo_label('loshu_grid', edition).upper()} &amp; 5-ELEMENT AUDIT", s_name))
        self.story.append(Paragraph(f"Prepared for {d['seeker_name']} ({dob}) · Active Digits: {', '.join(str(k) for k, v in cnts.items() if v > 0)}", s_sub))
        self.story.append(Spacer(1, 6))

        def plane_status_str(nums):
            present = sum(1 for n in nums if cnts.get(n, 0) > 0)
            if present == 3: return "<font color='#16835B'><b>Complete (3/3)</b></font>"
            elif present == 2: return "<font color='#C9A227'><b>Partial (2/3)</b></font>"
            elif present == 1: return "<font color='#7A654D'><b>Partial (1/3)</b></font>"
            else: return "<font color='#A13030'><b>Open (0/3)</b></font>"

        def plane_detail_str(plane_key, nums):
            act = [str(n) for n in nums if cnts.get(n, 0) > 0]
            opn = [str(n) for n in nums if cnts.get(n, 0) == 0]
            p_obj = CONTENT_LIB['topics']['planes'][plane_key]
            st_key = 'complete' if len(act) == 3 else ('partial' if len(act) > 0 else 'missing')
            st_txt = p_obj.get('states', {}).get(st_key, {}).get('depth_1_basic', p_obj['focus'])
            tag = f"Active: {', '.join(act) if act else 'None'} · Open: {', '.join(opn) if opn else 'None'}"
            return f"{st_txt} ({tag})"

        plane_rows = [
            [Paragraph("<b>PLANE NAME</b>", s_card_h), Paragraph("<b>NUMBERS</b>", s_card_h), Paragraph("<b>STATUS</b>", s_card_h), Paragraph("<b>YOUR CHART PATTERN &amp; PRACTICAL READING</b>", s_card_h)],
            [Paragraph("Mental Plane", s_card_txt), Paragraph("4 - 9 - 2", s_card_txt), Paragraph(plane_status_str([4,9,2]), s_card_txt), Paragraph(plane_detail_str('mental', [4,9,2]), s_card_txt)],
            [Paragraph("Emotional Plane", s_card_txt), Paragraph("3 - 5 - 7", s_card_txt), Paragraph(plane_status_str([3,5,7]), s_card_txt), Paragraph(plane_detail_str('emotional', [3,5,7]), s_card_txt)],
            [Paragraph("Practical Plane", s_card_txt), Paragraph("8 - 1 - 6", s_card_txt), Paragraph(plane_status_str([8,1,6]), s_card_txt), Paragraph(plane_detail_str('practical', [8,1,6]), s_card_txt)],
            [Paragraph("Thought Plane", s_card_txt), Paragraph("4 - 3 - 8", s_card_txt), Paragraph(plane_status_str([4,3,8]), s_card_txt), Paragraph(plane_detail_str('thought', [4,3,8]), s_card_txt)],
            [Paragraph("Willpower Plane", s_card_txt), Paragraph("9 - 5 - 1", s_card_txt), Paragraph(plane_status_str([9,5,1]), s_card_txt), Paragraph(plane_detail_str('will', [9,5,1]), s_card_txt)],
            [Paragraph("Action Plane", s_card_txt), Paragraph("2 - 7 - 6", s_card_txt), Paragraph(plane_status_str([2,7,6]), s_card_txt), Paragraph(plane_detail_str('action', [2,7,6]), s_card_txt)],
            [Paragraph(get_geo_label('golden_raj_yoga', edition), s_card_txt), Paragraph("4 - 5 - 6", s_card_txt), Paragraph(plane_status_str([4,5,6]), s_card_txt), Paragraph(plane_detail_str('golden_raj_yoga', [4,5,6]), s_card_txt)],
            [Paragraph(get_geo_label('silver_raj_yoga', edition), s_card_txt), Paragraph("2 - 5 - 8", s_card_txt), Paragraph(plane_status_str([2,5,8]), s_card_txt), Paragraph(plane_detail_str('silver_raj_yoga', [2,5,8]), s_card_txt)]
        ]
        t_planes = Table(plane_rows, colWidths=[118, 52, 76, 274], hAlign='CENTER')
        t_planes.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_GOLD),
            ('INNERGRID', (0,0), (-1,-1), 0.4, COLOR_GOLD_LIGHT),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('ALIGN', (1,1), (2,-1), 'CENTER')
        ]))
        self.story.append(t_planes)
        self.story.append(Spacer(1, 8))

        # 5 Elements Hygiene Table
        self.story.append(Paragraph(f"<b>5-ELEMENT EQUILIBRIUM AUDIT ({d['seeker_name'].upper()})</b>", s_card_h))
        self.story.append(Spacer(1, 3))

        def get_elem_state_and_remedy(elem_name, count):
            elem_data = CONTENT_LIB['topics']['elements'][elem_name]['states']
            if count == 0:
                return "Missing (0)", elem_data['missing']['remedy']
            elif elem_name in ("Wood", "Earth", "Metal") and count == 1:
                return f"Low ({count})", elem_data['low']['remedy']
            elif count > (3 if elem_name == "Earth" else 2):
                return f"Strong ({count})", elem_data['strong']['remedy']
            else:
                return f"Balanced ({count})", elem_data['balanced']['remedy']

        wood_c = cnts.get(3, 0) + cnts.get(4, 0)
        fire_c = cnts.get(9, 0)
        earth_c = cnts.get(2, 0) + cnts.get(5, 0) + cnts.get(8, 0)
        metal_c = cnts.get(6, 0) + cnts.get(7, 0)
        water_c = cnts.get(1, 0)

        w_st, w_rem = get_elem_state_and_remedy("Wood", wood_c)
        f_st, f_rem = get_elem_state_and_remedy("Fire", fire_c)
        e_st, e_rem = get_elem_state_and_remedy("Earth", earth_c)
        m_st, m_rem = get_elem_state_and_remedy("Metal", metal_c)
        wa_st, wa_rem = get_elem_state_and_remedy("Water", water_c)

        elem_data = [
            [Paragraph("<b>ELEMENT</b>", s_card_h), Paragraph("<b>TRADITIONAL RULERS</b>", s_card_h), Paragraph("<b>COUNT</b>", s_card_h), Paragraph("<b>BALANCE STATUS &amp; PRACTICAL HABIT</b>", s_card_h)],
            [Paragraph("Wood", s_card_txt), Paragraph(f"{get_geo_label('guru', edition)} (3), {get_geo_label('rahu', edition)} (4)", s_card_txt), Paragraph(w_st, s_card_txt), Paragraph(w_rem, s_card_txt)],
            [Paragraph("Fire", s_card_txt), Paragraph("Mars (9)", s_card_txt), Paragraph(f_st, s_card_txt), Paragraph(f_rem, s_card_txt)],
            [Paragraph("Earth", s_card_txt), Paragraph(f"Moon (2), {get_geo_label('budh', edition)} (5), Saturn (8)", s_card_txt), Paragraph(e_st, s_card_txt), Paragraph(e_rem, s_card_txt)],
            [Paragraph("Metal", s_card_txt), Paragraph(f"{get_geo_label('shukra', edition)} (6), {get_geo_label('ketu', edition)} (7)", s_card_txt), Paragraph(m_st, s_card_txt), Paragraph(m_rem, s_card_txt)],
            [Paragraph("Water", s_card_txt), Paragraph("Sun (1)", s_card_txt), Paragraph(wa_st, s_card_txt), Paragraph(wa_rem, s_card_txt)]
        ]
        t_elem = Table(elem_data, colWidths=[58, 122, 72, 268], hAlign='CENTER')
        t_elem.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_GOLD),
            ('INNERGRID', (0,0), (-1,-1), 0.4, COLOR_GOLD_LIGHT),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ('ALIGN', (2,1), (2,-1), 'CENTER')
        ]))
        self.story.append(t_elem)

        # ── PAGE 3: 5-Element Actions & 90-Day Execution Horizon ──
        self.story.append(PageBreak())
        self.story.append(Paragraph(f"5-ELEMENT ACTIONS &amp; 90-DAY PLAN ({d['seeker_name'].upper()})", s_name))
        self.story.append(Paragraph(f"{get_geo_label('vastu', edition)} Orientation · {get_geo_label('driver', edition)} {driver} &amp; {get_geo_label('conductor', edition)} {d.get('conductor_display', conductor)} · {edition.title()} Edition", s_sub))
        self.story.append(Spacer(1, 4))

        # Kua & Personal Year Coordinates
        kua_raw = d.get('kua_element', 'East Group')
        kua_sector = kua_raw.split('(')[-1].rstrip(')').strip() if '(' in kua_raw else kua_raw
        kua_desk = kua_sector.split('/')[0].strip()
        kua_data = [
            [
                Paragraph(f"<b>{get_geo_label('kua', edition)}:</b> {kua} ({kua_raw.split('·')[0].strip()})", s_card_txt),
                Paragraph(f"<b>{get_geo_label('vastu', edition)} Group:</b> {kua_sector}", s_card_txt),
                Paragraph(f"<b>Desk Orientation:</b> {kua_desk} Direction", s_card_txt),
            ],
            [
                Paragraph(f"<b>Profile Input:</b> {gender.title()} · Born {dob}", s_card_txt),
                Paragraph(f"<b>{get_geo_label('personal_year', edition)} {py}:</b> (Day {day_num} + Month {d.get('month', 11)} + {d.get('current_year', 2026)} → {py})", s_card_txt),
                Paragraph(f"<b>Annual Focus:</b> {d.get('personal_year_theme', 'Steady Foundation')}", s_card_txt)
            ]
        ]
        t_kua_sec = Table(
            [[Paragraph(f"<b>• {get_geo_label('kua', edition).upper()} &amp; {get_geo_label('vastu', edition).upper()} ORIENTATION</b>", s_card_h)],
             [Table(kua_data, colWidths=[170, 175, 165])]],
            colWidths=[520]
        )
        t_kua_sec.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_PEARL_BG),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_kua_sec)
        self.story.append(Spacer(1, 4))

        # Dynamic Ranking of Out-of-Balance Elements (Ranked by Gap Size)
        elem_counts = [
            ("Wood", wood_c, 3 in missing or 4 in missing),
            ("Fire", fire_c, 9 in missing),
            ("Earth", earth_c, 2 in missing or 5 in missing or 8 in missing),
            ("Metal", metal_c, 6 in missing or 7 in missing),
            ("Water", water_c, 1 in missing),
        ]
        ranked_elems = sorted(elem_counts, key=lambda x: (0 if x[2] else 1, x[1]))
        biggest_gap_elem = ranked_elems[0][0] if ranked_elems[0][2] else "Balanced"
        top3_names = ", ".join(f"{en} ({cv})" for en, cv, _ in ranked_elems[:3])

        actions_card = [
            [Paragraph(f"<b>• RANKED 5-ELEMENT HABITS FOR {d['seeker_name'].upper()} ({top3_names.upper()})</b>", s_card_h)],
            [Spacer(1, 2)],
            [Paragraph(f"From your {dob} grid (Wood {wood_c}, Fire {fire_c}, Earth {earth_c}, Metal {metal_c}, Water {water_c}), your top three practical focus areas are <b>{top3_names}</b> — everyday workspace and routine habits with no gemstones or rituals:", s_card_txt)],
            [Spacer(1, 3)]
        ]
        for elem_name, c_val, is_gap in ranked_elems[:3]:
            rem_text = CONTENT_LIB['topics']['elements'][elem_name]['states']['missing' if is_gap else ('low' if c_val == 1 else 'strong')]['remedy']
            actions_card.append([Paragraph(f"• <b>{elem_name} Focus ({'Open Digit in Grid' if is_gap else f'Count {c_val}'}):</b> {rem_text}", s_card_txt)])
            actions_card.append([Spacer(1, 2)])

        t_actions = Table(actions_card, colWidths=[520], hAlign='CENTER')
        t_actions.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8)
        ]))
        self.story.append(t_actions)
        self.story.append(Spacer(1, 4))

        # 90-Day Execution Horizon Selected from Largest Gap
        plan_info = CONTENT_LIB['topics']['ninety_day_plan'].get(biggest_gap_elem, CONTENT_LIB['topics']['ninety_day_plan']['Balanced'])['depth_1_basic']
        roadmap_card = [
            [Paragraph(f"<b>• 90-DAY PRACTICAL PLAN ({biggest_gap_elem.upper()} PRIMARY FOCUS) — {CONTENT_LIB['topics']['ninety_day_plan'].get(biggest_gap_elem, {})['gap_focus']}</b>", s_card_h)],
            [Spacer(1, 2)],
            [Table([
                [Paragraph("<b>DAYS 1–30</b>", s_card_h), Paragraph("<b>DAYS 31–60</b>", s_card_h), Paragraph("<b>DAYS 61–90</b>", s_card_h)],
                [
                    Paragraph(plan_info['days_1_30'], s_card_txt),
                    Paragraph(plan_info['days_31_60'], s_card_txt),
                    Paragraph(plan_info['days_61_90'], s_card_txt)
                ]
            ], colWidths=[166, 166, 168], hAlign='CENTER', style=[
                ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
                ('BOX', (0,0), (-1,-1), 0.6, COLOR_GOLD_LIGHT),
                ('INNERGRID', (0,0), (-1,-1), 0.4, COLOR_GOLD_LIGHT),
                ('TOPPADDING', (0,0), (-1,-1), 4),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5)
            ])],
            [Spacer(1, 3)],
            [Paragraph(f"<font size=6.5 color='#7A654D'><b>Chart Reference ({d['seeker_name']} · {dob} · {edition.title()} Edition):</b> {get_geo_label('driver', edition)} = {driver} · {get_geo_label('conductor', edition)} = {d.get('conductor_display', conductor)} · {get_geo_label('calling_name', edition)} = {c_root} ({c_compound}) · {get_geo_label('kua', edition)} = {kua} · Open Digits = [{', '.join(str(n) for n in missing) or 'None'}].</font>", s_sub)]
        ]
        t_roadmap = Table(roadmap_card, colWidths=[520], hAlign='CENTER')
        t_roadmap.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ('ALIGN', (0,-1), (-1,-1), 'CENTER')
        ]))
        self.story.append(t_roadmap)

    def _assemble_advanced_12_pages(self):
        s = self.styles
        d = self.data
        meta = self._get_topic_meta()
        is_premium_tier = self.tier in ("premium", "report_premium", "divine", "roadmap", "report_divine")

        # PAGE 1: Cover Page
        self._add_cover_page(
            subtitle=meta['subtitle'],
            badge_text=meta['badge'],
            custom_title=meta['title']
        )
        self.story.append(PageBreak())

        # PAGE 2: Table of Contents
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("TABLE OF CONTENTS", s['SectionH1']))
        if is_premium_tier:
            self.story.append(Paragraph("SOVEREIGN COMPENDIUM · 30 STANDARD SECTIONS ACROSS 32 PAGES", s['CoverSubtitle']))
            self.story.append(Spacer(1, 4))

            toc_rows = [
                [Paragraph("<b>Standard Section (Part I)</b>", s['TableHeader']), Paragraph("<b>Page</b>", s['TableHeader']),
                 Paragraph("<b>Standard Section (Part II)</b>", s['TableHeader']), Paragraph("<b>Page</b>", s['TableHeader'])]
            ]
            for i in range(15):
                t1, p1 = meta['toc_part1'][i]
                t2, p2 = meta['toc_part2'][i]
                toc_rows.append([
                    Paragraph(f"<b>{t1}</b>", s['TableCell']), Paragraph(p1, s['TableCellCenter']),
                    Paragraph(f"<b>{t2}</b>", s['TableCell']), Paragraph(p2, s['TableCellCenter'])
                ])

            t_toc = Table(toc_rows, colWidths=[205, 52, 205, 52])
            t_toc.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1.2, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 3),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ]))
            self.story.append(t_toc)
            self.story.append(Spacer(1, 8))
        else:
            self.story.append(Paragraph("MASTER SYNTHESIS DOSSIER · NV THINK™ LOGIC-TO-PSYCHOLOGY ARCHITECTURE", s['CoverSubtitle']))
            self.story.append(Spacer(1, 6))

            toc_rows = [
                [Paragraph("<b>Section / Standard Topic</b>", s['TableHeader']), Paragraph("<b>Page</b>", s['TableHeader'])]
            ]
            for title, pg in meta['toc_12']:
                toc_rows.append([Paragraph(f"<b>{title}</b>", s['TableCell']), Paragraph(pg, s['TableCellCenter'])])

            t_toc = Table(toc_rows, colWidths=[420, 96])
            t_toc.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1.2, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 6.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6.5),
                ('LEFTPADDING', (0,0), (-1,-1), 10),
                ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ]))
            self.story.append(t_toc)
            self.story.append(Spacer(1, 14))

        timing_clause = (
            "10-year macro planetary timing radar"
            if is_premium_tier
            else "auspicious initiation windows and Personal Year cycles"
        )
        exec_summary_p = Paragraph(
            f"<b>NV THINK™ Executive Charter:</b> This dossier is prepared for <b>{d['seeker_name']}</b> (DOB: 28-11-1981). Combining Driver 1 (Sun), Conductor 4 (Rahu), and Chaldean 32/5 (Mercury), this report decodes your chart through the 7 stages of intelligence: from deterministic mathematical logic to behavioral observations, psychological motivations, and {timing_clause}.",
            s['CalloutText']
        )
        self.story.append(exec_summary_p)
        self.story.append(PageBreak())

        # PAGE 3: Chapter 1 — Executive Summary & Dual Pillar Dynamics
        self.story.append(Paragraph("Section 1: Executive Summary & Destiny Signature", s['SectionH1']))
        self.story.append(Paragraph(
            f"Welcome <b>{d['seeker_name']}</b>. Your numerical architecture is anchored by the rare and potent <b>Sun 1 (Driver)</b> and <b>Rahu 4 (Conductor)</b> polarity. In classical numerology, the Sun represents sovereignty, clarity of intent, and visionary leadership. Rahu represents unconventional intelligence, technological breakthroughs, and systematic architecture.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))

        p3_table = [
            [Paragraph("<b>Core Parameter</b>", s['TableHeader']), Paragraph("<b>Calculated Value</b>", s['TableHeader']), Paragraph("<b>Life Interpretation & Manifestation</b>", s['TableHeader'])],
            [Paragraph("Driver (Mulank)", s['TableCell']), Paragraph("<b>1 · Sun (Surya)</b>", s['TableCellCenter']), Paragraph("Governs your conscious ego, leadership drive, and instinct for autonomy. You naturally take charge and resist subordinate micromanagement.", s['TableCell'])],
            [Paragraph("Conductor (Bhagyank)", s['TableCell']), Paragraph("<b>4 · Rahu (North Node)</b>", s['TableCellCenter']), Paragraph("Governs your ultimate destiny path. Pulls you into complex, high-technology, analytical, and revolutionary systems where unconventional solutions prevail.", s['TableCell'])],
            [Paragraph("Calling Name Vibration", s['TableCell']), Paragraph("<b>32 → 5 · Mercury</b>", s['TableCellCenter']), Paragraph("'The Star of the Lion'. Bestows intellectual agility, commercial charisma, negotiation power, and rapid social/business mobility.", s['TableCell'])],
            [Paragraph("Kua Directional Vector", s['TableCell']), Paragraph("<b>1 · Water (East Group)</b>", s['TableCellCenter']), Paragraph("Aligns with North for career acceleration and Southeast for sustained wealth accumulation.", s['TableCell'])],
            [Paragraph(f"Personal Year {d.get('current_year', 2026)}", s['TableCell']), Paragraph(f"<b>{d.get('personal_year', 4)} · {d.get('personal_year_theme', 'Foundation Phase')}</b>", s['TableCellCenter']), Paragraph("A focused developmental cycle. Perfect for formalizing structures, scaling platforms, and locking in strategic agreements.", s['TableCell'])],
        ]
        t_p3 = Table(p3_table, colWidths=[120, 116, 280])
        t_p3.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_p3)
        self.story.append(Spacer(1, 8))

        self.story.append(Paragraph(
            "<b>The 1–4 Polarity Synthesis:</b> When a Sun-ruled individual has a Rahu life path, the primary lesson is mastering patience with operational details. Your Sun vision conceives grand architectures instantly; Rahu demands that every brick, protocol, and contract be verified to prevent unexpected institutional friction.",
            s['ReportBody']
        ))
        self.story.append(PageBreak())

        # PAGE 4: Chapter 2 — Natal Lo Shu Grid & 8-Plane Elemental Audit
        self.story.append(Paragraph("Section 2: Natal Lo Shu 3×3 Grid & 8-Plane Elemental Audit", s['SectionH1']))
        self.story.append(Paragraph(
            "The 3×3 Lo Shu Magic Square organizes cosmic energy into 3 horizontal and 3 vertical planes, plus 2 diagonal planes. Here is your birth matrix derived from 28-11-1981:",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 5))
        self.story.append(self._create_loshu_grid_table())
        self.story.append(Spacer(1, 8))

        planes_rows = [
            [Paragraph("<b>Plane Name</b>", s['TableHeader']), Paragraph("<b>Numbers</b>", s['TableHeader']), Paragraph("<b>Status in Your Chart</b>", s['TableHeader']), Paragraph("<b>Behavioral & Commercial Manifestation</b>", s['TableHeader'])],
            [Paragraph("Thought Plane", s['TableCell']), Paragraph("4 - 3 - 8", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>Active 8 (Double)</b></font>", s['TableCellCenter']), Paragraph("Carries immense perseverance and long-range planning. Missing 4 and 3 means strategic frameworks must be documented in writing.", s['TableCell'])],
            [Paragraph("Will Plane", s['TableCell']), Paragraph("9 - 5 - 1", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Active 9 & 1 (Quad)</b></font>", s['TableCellCenter']), Paragraph("Unstoppable breakthrough energy. Quadruple 1 gives supreme communication stamina; missing central 5 is bridged by Calling Name 32/5.", s['TableCell'])],
            [Paragraph("Action Plane", s['TableCell']), Paragraph("2 - 7 - 6", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>Active 2 (Single)</b></font>", s['TableCellCenter']), Paragraph("Empathy and diplomatic intuition active. Missing 7 and 6 indicates a preference for direct execution over decorative deliberation.", s['TableCell'])],
            [Paragraph("Mental Plane", s['TableCell']), Paragraph("4 - 9 - 2", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Active 9 & 2</b></font>", s['TableCellCenter']), Paragraph("Sharp situational awareness, analytical synthesis, and quick memory retention.", s['TableCell'])],
            [Paragraph("Practical Plane", s['TableCell']), Paragraph("8 - 1 - 6", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Active 8 & 1</b></font>", s['TableCellCenter']), Paragraph("Strong commercial grounding. Ability to turn abstract concepts into revenue-generating business models.", s['TableCell'])],
        ]
        t_pl = Table(planes_rows, colWidths=[95, 65, 116, 240])
        t_pl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_pl)
        self.story.append(PageBreak())

        # ── PAGES 5, 6, 7: DYNAMIC TOPIC-SPECIFIC PRIORITY CHAPTERS ──────────
        self._build_topic_pages_12()

        # PAGE 8: Chapter 6 — Interpersonal Synergy & Co-Founder Synastry
        self.story.append(Paragraph("Section 6: Interpersonal Synergy, Co-Founder Matching & Synastry", s['SectionH1']))
        self.story.append(Paragraph(
            "No executive scales alone. Understanding numerical synergy prevents toxic partnerships and unlocks multiplicative founder dynamics.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))

        synastry_table = [
            [Paragraph("<b>Partner Archetype</b>", s['TableHeader']), Paragraph("<b>Planetary Dynamic</b>", s['TableHeader']), Paragraph("<b>Synergy Rating</b>", s['TableHeader']), Paragraph("<b>Strategic Collaboration Protocol</b>", s['TableHeader'])],
            [Paragraph("Number 1 (Sun)", s['TableCell']), Paragraph("Solar Mirroring", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>High (Advisory)</b></font>", s['TableCellCenter']), Paragraph("Excellent as peer advisors or board members; avoid operational co-CEO models to prevent ego friction.", s['TableCell'])],
            [Paragraph("Number 3 (Jupiter)", s['TableCell']), Paragraph("Wisdom & Expansion", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Supreme (Co-Founder)</b></font>", s['TableCellCenter']), Paragraph("Ideal co-founder or strategic mentor. Balances your Rahu 4 with structured ethical wisdom and deep institutional trust.", s['TableCell'])],
            [Paragraph("Number 5 (Mercury)", s['TableCell']), Paragraph("Commercial Synergy", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Excellent (Sales/Growth)</b></font>", s['TableCellCenter']), Paragraph("Matches your calling name vibration. Ideal for Chief Growth Officers, media buyers, and international business development.", s['TableCell'])],
            [Paragraph("Number 8 (Saturn)", s['TableCell']), Paragraph("Karmic Realism", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>Good with Strict Contracts</b></font>", s['TableCellCenter']), Paragraph("Brings immense operational discipline, but ensure all equity terms are legally documented on day one.", s['TableCell'])],
            [Paragraph("Number 6 (Venus)", s['TableCell']), Paragraph("Creative Polar", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>Neutral / Aesthetic</b></font>", s['TableCellCenter']), Paragraph("Great for creative design, brand styling, and PR campaigns; keep separate from financial treasury management.", s['TableCell'])],
        ]
        t_syn = Table(synastry_table, colWidths=[110, 95, 115, 196])
        t_syn.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_syn)
        self.story.append(PageBreak())

        # PAGE 9: Chapter 7 — Auspicious Initiation Windows & Muhurat Timing
        self.story.append(Paragraph("Section 7: Auspicious Initiation Windows & Muhurat Timing", s['SectionH1']))
        self.story.append(Paragraph(
            "Timing is the catalyst that transforms strategic effort into commercial triumph. Aligning major launches, contract signings, and capital deployments with your harmonic celestial windows minimizes friction.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))

        muhurat_items = [
            ("• Perpetual Golden Dates of Any Month",
             "Your primary power dates are the <b>1st, 10th, 19th, and 28th</b> (ruled by Sun 1). Your secondary commercial dates are the <b>5th, 14th, and 23rd</b> (ruled by Mercury 5). Schedule client contract signings, entity formations, and product launches on these dates whenever possible."),
            ("• Harmonic Days of the Week",
             "<b>Sunday</b> is your primary day for visionary roadmapping and leadership decrees. <b>Wednesday</b> is your optimal day for high-velocity commercial deals, ad campaign deployments, and sales pitches. Avoid contentious legal filings on Saturdays."),
            ("• Auspicious Hourly Horas (Solar & Mercurial Windows)",
             "Initiate high-stakes calls during the first hour after local sunrise (Solar Hora) or during the Mercury Hora (traditionally the 4th or 11th hour from sunrise depending on weekday calculations).")
        ]
        for h_p, b_p in muhurat_items:
            self.story.append(Paragraph(f"<b>{h_p}</b>", s['SectionH2']))
            self.story.append(Paragraph(b_p, s['ReportBody']))
            self.story.append(Spacer(1, 4))

        self.story.append(PageBreak())

        # PAGE 10: Chapter 8 — Vedic Gharelu Remedies Bank & 40-Day Aura Cleansing
        self.story.append(Paragraph("Section 8: Vedic Gharelu Remedies Bank & 40-Day Aura Cleansing", s['SectionH1']))
        self.story.append(Paragraph(
            "Numeros Vision strictly prescribes safe, non-invasive, household (Gharelu) remedies that are readily accessible at home for zero or minimal cost. No costly superstitions or invasive rituals.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 5))

        gharelu_rows = [
            [Paragraph("<b>Category / Target</b>", s['TableHeader']), Paragraph("<b>Readily Accessible Household Item</b>", s['TableHeader']), Paragraph("<b>Vedic Gharelu Action & Energy Balancing Protocol</b>", s['TableHeader'])],
            [Paragraph("<b>Universal Aura Cleansing</b><br/>Loop Drainage", s['TableCell']), Paragraph("Rock Salt<br/>(Sendha Namak)", s['TableCellCenter']), Paragraph("<b>40-Day Rock Salt Bath:</b> Add 1-2 tbsp Sendha Namak in warm water. Wash face and soak feet daily for 40 days to dissolve looping negative thoughts, mental stagnation, and energetic fatigue.", s['TableCell'])],
            [Paragraph("<b>Sun 1 (Driver)</b><br/>Solar Vitality", s['TableCell']), Paragraph("Father's Blessings &<br/>Copper Lota", s['TableCellCenter']), Paragraph("<b>Respect Father:</b> Touch father's feet daily in the morning. Offer fresh water to the rising sun in a copper vessel (Surya Arghya). Eat a pinch of jaggery (gud) before key meetings.", s['TableCell'])],
            [Paragraph("<b>Moon 2</b><br/>Mental Peace", s['TableCell']), Paragraph("Mother's Blessings &<br/>Silver Glass", s['TableCellCenter']), Paragraph("<b>Respect Mother:</b> Take mother's blessings daily. Drink water/milk from a silver cup. Never waste water; fix dripping taps at home immediately to stop cash and peace leaks.", s['TableCell'])],
            [Paragraph("<b>Jupiter 3</b><br/>Wisdom & Growth", s['TableCell']), Paragraph("Turmeric (Haldi) &<br/>Banana Tree", s['TableCellCenter']), Paragraph("<b>40-Day Haldi Bath:</b> Add a pinch of haldi to bath water daily for 40 days. On Thursdays, offer haldi-water on Shivling or to a Banana tree. Apply haldi tilak on forehead.", s['TableCell'])],
            [Paragraph("<b>Rahu 4 (Conductor)</b><br/>Mental Clarity", s['TableCell']), Paragraph("Electronic Hygiene &<br/>Dog Care", s['TableCellCenter']), Paragraph("<b>Tech Decluttering:</b> Discard broken electronics, fused bulbs, and damaged cords. Feed stray dogs daily. Add 2 drops of sandalwood oil to bath to ground nervous agitation.", s['TableCell'])],
            [Paragraph("<b>Mercury 5 (Name)</b><br/>Commercial Charm", s['TableCell']), Paragraph("Green Plants &<br/>Cow Service", s['TableCellCenter']), Paragraph("<b>Living Greens:</b> Water green plants (Tulsi/Jade) daily. Feed fresh green fodder or soaked green moong dal to cows on Wednesdays. Carry a clean green handkerchief.", s['TableCell'])],
            [Paragraph("<b>Saturn 8 (Double)</b><br/>Endurance & Relief", s['TableCell']), Paragraph("Service to Helpers &<br/>Mustard Oil Diya", s['TableCellCenter']), Paragraph("<b>Respect Domestic Helpers:</b> Treat drivers and laborers with dignity and prompt pay. Light mustard oil diya under Peepal tree on Saturdays; feed black crows or stray animals.", s['TableCell'])],
        ]
        t_gh = Table(gharelu_rows, colWidths=[105, 100, 311])
        t_gh.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        self.story.append(t_gh)
        self.story.append(PageBreak())

        # PAGE 11: Chapter 9 — Spatial Feng Shui & Kua Number 1 Matrix
        self.story.append(Paragraph("Section 9: Spatial Alignment & Kua Number 1 Directional Blueprint", s['SectionH1']))
        self.story.append(Paragraph(
            "Based on your birth year (1981 Male), your Kua Number is <b>1</b>, corresponding to the <b>Water element</b> and the <b>Kan Trigram</b> (East Group). Your spatial directions govern focus, vitality, and wealth accumulation:",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))

        kua_rows = [
            [Paragraph("<b>Direction</b>", s['TableHeader']), Paragraph("<b>Energy Sector (Trigram)</b>", s['TableHeader']), Paragraph("<b>Influence on Life</b>", s['TableHeader']), Paragraph("<b>Office & Home Optimization Protocol</b>", s['TableHeader'])],
            [Paragraph("<b>North</b>", s['TableCell']), Paragraph("Sheng Chi (Prime Success)", s['TableCellCenter']), Paragraph("Career authority, executive advancement, high reputation", s['TableCell']), Paragraph("<b>Optimal desk facing direction.</b> Sit facing North during high-stakes presentations and strategic planning.", s['TableCell'])],
            [Paragraph("<b>East</b>", s['TableCell']), Paragraph("Tien Yi (Celestial Health)", s['TableCellCenter']), Paragraph("Physical vitality, mental rejuvenation, longevity", s['TableCell']), Paragraph("Keep this sector clear and bright. Install a polished Brass Surya on East wall; ideal for morning contemplation.", s['TableCell'])],
            [Paragraph("<b>Southeast</b>", s['TableCell']), Paragraph("Nien Yen (Relationship Harmony)", s['TableCellCenter']), Paragraph("Commercial partnerships, team loyalty, investor trust", s['TableCell']), Paragraph("Place client meeting chairs or partnership awards in this sector of your executive cabin.", s['TableCell'])],
            [Paragraph("<b>South</b>", s['TableCell']), Paragraph("Fu Wei (Personal Stability)", s['TableCellCenter']), Paragraph("Emotional grounding, inner poise, clear judgment", s['TableCell']), Paragraph("Ideal for contemplative reflection, journal writing, and milestone reviews.", s['TableCell'])],
            [Paragraph("<b>West / NW / SW</b>", s['TableCell']), Paragraph("West Group Sectors", s['TableCellCenter']), Paragraph("Frictional energy zones for Kua 1", s['TableCell']), Paragraph("Avoid positioning your main desk facing West or Southwest; ensure back is supported by a solid wall.", s['TableCell'])],
        ]
        t_kua = Table(kua_rows, colWidths=[80, 110, 136, 190])
        t_kua.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_kua)
        self.story.append(PageBreak())

        # PAGE 12: Chapter 10 — Methodology, Provenance & Governance
        self.story.append(Paragraph("Section 10: Methodology, Authentic Standards & Ethical Guidance", s['SectionH1']))
        self.story.append(Paragraph(
            "Numeros Vision is dedicated to authentic, time-tested numerological principles. We blend traditional Vedic, Chaldean, and Lo Shu wisdom with clear, uplifting guidance designed to empower your daily life and career choices.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))

        gov_box = [
            [Paragraph("<b>Guidance Dimension</b>", s['TableHeader']), Paragraph("<b>Authentic Standard & Method</b>", s['TableHeader'])],
            [Paragraph("Calculation Core", s['TableCell']), Paragraph("Classical Vedic & Chaldean mathematical canons with verified accuracy.", s['TableCell'])],
            [Paragraph("Privacy & Data Protection", s['TableCell']), Paragraph("Your personal birth data is private, secure, and confidential. It is used solely to generate your personal reading and is never shared or sold.", s['TableCell'])],
            [Paragraph("Digital Verification", s['TableCell']), Paragraph(f"Report ID: {d['report_id']} | Verified & Authentic", s['TableCell'])],
            [Paragraph("Chaldean Methodology", s['TableCell']), Paragraph("Classical 1-to-8 sound mapping (sacred alphabet without 9 in compound derivation).", s['TableCell'])],
            [Paragraph("Interpretive Boundary", s['TableCell']), Paragraph("Traditional numerology offers personal self-awareness, timing insights, and positive lifestyle guidance. It does not replace medical, legal, or financial professional counsel.", s['TableCell'])],
            [Paragraph("NV THINK™ Framework", s['TableCell']), Paragraph("Reasoned across 7 stages: Logic → Observation → Behaviour → Psychology → Context → Duality → Validation. A number is an interpretive indicator, not a fixed person.", s['TableCell'])],
            [Paragraph("Master Sign-off", s['TableCell']), Paragraph("Master Numerologist Bhaskr Singh (Numeros Vision) · Numeros Vision Advisory Board", s['TableCell'])],
        ]
        t_gov = Table(gov_box, colWidths=[150, 366])
        t_gov.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_gov)
        self.story.append(Spacer(1, 12))

        closing_p = Paragraph(
            "<b>Final Benediction:</b> May the solar brilliance of Driver 1 illuminate your path, may the architectural power of Conductor 4 build enduring enterprises, and may the commercial grace of Mercury 5 bring prosperity to every endeavor.<br/><br/><b>NUMEROS VISION · ANVEIL EVERY CHARM</b>",
            s['CalloutText']
        )
        self.story.append(closing_p)

    def _build_topic_pages_12(self):
        s = self.styles
        d = self.data
        t = self.topic_id

        if t == "present_numbers":
            # PAGE 5: Present Numbers Deep Audit & Single vs Repeated Overdrive
            self.story.append(Paragraph("Section 3: Natal Present Numbers Deep Audit & Frequency Analysis", s['SectionH1']))
            self.story.append(Paragraph(
                f"Your natal birth matrix derived from <b>28-11-1981</b> reveals the active inborn frequencies you were born with. The seeker carries <b>[1, 2, 8, 9]</b>. Below is the exact single vs. repeated frequency audit:",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            pres_rows = [
                [Paragraph("<b>Number & Planet</b>", s['TableHeader']), Paragraph("<b>Frequency</b>", s['TableHeader']), Paragraph("<b>Operating Status</b>", s['TableHeader']), Paragraph("<b>Inborn Psychological & Commercial Energy</b>", s['TableHeader'])],
                [Paragraph("<b>Number 1</b><br/>Sun (Surya)", s['TableCell']), Paragraph("<b>×4 (1111)</b>", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Solar Overdrive</b></font>", s['TableCellCenter']), Paragraph("Extraordinary executive presence, pioneer spirit, and supreme communication stamina. Overdrive tendency: can become impatient with slow collaborators or take on all burdens solo.", s['TableCell'])],
                [Paragraph("<b>Number 8</b><br/>Saturn (Shani)", s['TableCell']), Paragraph("<b>×2 (88)</b>", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>Double Earth</b></font>", s['TableCellCenter']), Paragraph("Profound material realism, resilience, and wealth compounding. Double 8 grants immense endurance through economic storms, but can make you feel you carry the world alone.", s['TableCell'])],
                [Paragraph("<b>Number 2</b><br/>Moon (Chandra)", s['TableCell']), Paragraph("<b>×1 (2)</b>", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Harmonic Single</b></font>", s['TableCellCenter']), Paragraph("Gentle emotional intelligence, diplomatic sensitivity, and instinctive ability to read the unspoken room during commercial negotiations.", s['TableCell'])],
                [Paragraph("<b>Number 9</b><br/>Mars (Mangal)", s['TableCell']), Paragraph("<b>×1 (9)</b>", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Harmonic Single</b></font>", s['TableCellCenter']), Paragraph("Courage, righteous moral drive, and breakthrough momentum to complete long-term initiatives. Operates cleanly without martial aggression.", s['TableCell'])],
            ]
            t_pr = Table(pres_rows, colWidths=[95, 65, 116, 240])
            t_pr.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            self.story.append(t_pr)
            self.story.append(Spacer(1, 8))
            self.story.append(Paragraph(
                "<b>Overdrive Management Protocol:</b> With 1111 and 88, your greatest danger is not failure, but executive burnout from doing everything yourself. Learn to delegate operational tasks to trusted seconds-in-command so your solar vision stays untangled from daily operational fatigue.",
                s['CalloutText']
            ))
            self.story.append(PageBreak())

            # PAGE 6: Benefic vs Malefic Planetary Operating Matrix
            self.story.append(Paragraph("Section 4: Present Numbers Benefic vs Malefic Operating Matrix", s['SectionH1']))
            self.story.append(Paragraph(
                "In classical numerology, a present number is never permanently 'good' or 'bad'. Its manifestation alternates between a <b>Benefic State</b> (elevated, constructive) and a <b>Malefic Shadow State</b> (unharnessed, reactive). Below is the diagnostic matrix for your chart:",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            bm_rows = [
                [Paragraph("<b>Present Digit</b>", s['TableHeader']), Paragraph("<b>Benefic Operating State</b>", s['TableHeader']), Paragraph("<b>Malefic Shadow State</b>", s['TableHeader']), Paragraph("<b>Transformation Catalyst (Harnessing Benefic Power)</b>", s['TableHeader'])],
                [Paragraph("<b>Number 1</b><br/>Sun (Surya)", s['TableCell']), Paragraph("Visionary clarity, inspirational leadership, rapid decision-making, high visibility.", s['TableCell']), Paragraph("Ego fatigue, impatience with junior errors, communication overdrive, loneliness at top.", s['TableCell']), Paragraph("<b>Practice 2-Minute Pause:</b> Allow team members 2 full minutes to voice observations before issuing executive directives.", s['TableCell'])],
                [Paragraph("<b>Number 8</b><br/>Saturn (Shani)", s['TableCell']), Paragraph("Patient wealth compounding, enterprise stamina, fair contracts, judicial impartiality.", s['TableCell']), Paragraph("Feeling unrewarded, delayed gratification fatigue, carrying solitary weight, cynicism.", s['TableCell']), Paragraph("<b>Enforce Milestone Celebrations:</b> Celebrate quarterly wins; write clear equity milestones so trust is contractual, not emotional.", s['TableCell'])],
                [Paragraph("<b>Number 2</b><br/>Moon (Chandra)", s['TableCell']), Paragraph("Diplomatic bridge-building, empathy, intuitive partner synastry, psychological acumen.", s['TableCell']), Paragraph("Mood swings under stress, taking operational setbacks personally, boundary blurring.", s['TableCell']), Paragraph("<b>Analytical Detachment:</b> Maintain clear separation between business KPIs and personal emotional worth.", s['TableCell'])],
                [Paragraph("<b>Number 9</b><br/>Mars (Mangal)", s['TableCell']), Paragraph("Decisive execution, moral courage, finishing power, humanitarian impulse.", s['TableCell']), Paragraph("Sudden irritation with bureaucratic inertia, righteous indignation, scattered energy.", s['TableCell']), Paragraph("<b>Daily Physical Discharge:</b> Engage in morning brisk walking or workouts to ground martial adrenaline.", s['TableCell'])],
            ]
            t_bm = Table(bm_rows, colWidths=[80, 130, 130, 176])
            t_bm.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 4.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            self.story.append(t_bm)
            self.story.append(Spacer(1, 8))
            self.story.append(Paragraph(
                "<b>Master Insight:</b> By consciously applying these transformation catalysts, your present numbers function with 100% benefic power, shielding you from unnecessary administrative and emotional friction.",
                s['CalloutText']
            ))
            self.story.append(PageBreak())

            # PAGE 7: Inborn Career Fruitfulness & Vocational Blueprint
            self.story.append(Paragraph("Section 5: Inborn Career Fruitfulness & Vocational Blueprint", s['SectionH1']))
            self.story.append(Paragraph(
                f"Combining your present numbers <b>[1, 2, 8, 9]</b> with <b>Driver 1 (Sun)</b>, <b>Conductor 4 (Rahu)</b>, and <b>Chaldean Name 32/5 (Mercury)</b>, your chart indicates supreme natural commercial fruitfulness in specific high-yield vocations:",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            career_pillars = [
                ("1. Programmatic Adtech, Digital Media Platforms & Audience Monetization",
                 "Rahu 4 rules complex electronic networks, algorithmic bidding exchanges, and virtual data streams. Sun 1 gives executive monetization authority. You naturally excel in business models that package, trade, and monetize attention, automated ad inventory, and data pipelines. Avoid commoditized agency services; own the programmatic technology layer."),
                ("2. Enterprise B2B Negotiation & High-Stakes Commercial Dealmaking",
                 "Chaldean 32/5 ('The Star of the Lion') gives magnetic verbal persuasion, Moon 2 gives psychological intuition, and Saturn 8 ensures ironclad contractual balance. In high-stakes B2B negotiations where enterprise contracts or strategic partnerships are finalized, your presence commands respect while remaining diplomatically versatile."),
                ("3. Long-Term Asset Compounding & Software IP Ownership",
                 "Double 8 in the Lo Shu Earth sector anchors tangible wealth in commercial software intellectual property, digital media assets, and strategic real estate. Ensure that revenues generated from adtech velocity are systematically funneled into durable, compounding asset vehicles.")
            ]
            for title_p, desc_p in career_pillars:
                self.story.append(Paragraph(f"<b>{title_p}</b>", s['SectionH2']))
                self.story.append(Paragraph(desc_p, s['ReportBody']))
                self.story.append(Spacer(1, 3))

            self.story.append(PageBreak())

        elif t == "love_relationship":
            # PAGE 5: Love Style, Romance Profile & Spousal Temperament
            self.story.append(Paragraph("Section 3: Love Style, Romantic Resonance & Spousal Temperament", s['SectionH1']))
            self.story.append(Paragraph(
                f"In intimate relationships, <b>Driver 1 (Sun)</b> individuals love with supreme loyalty, protective dignity, and generosity. Paired with <b>Conductor 4 (Rahu)</b>, you seek deep intellectual stimulation, unconventional understanding, and a calm private sanctuary.",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            love_traits = [
                ("• Core Romantic Psychology",
                 "You express love through steadfast protection, providing long-term security, and championing your partner's ambitions. You need a partner who genuinely respects your independent vision and never engages in public belittlement."),
                ("• Quadruple 1 Relational Shadow",
                 "Carrying four 1s means you can sometimes become absorbed in internal strategic thoughts, appearing emotionally distant or commanding. Ensure you consciously switch off 'CEO mode' when crossing your home threshold."),
                ("• Ideal Spousal Archetype",
                 "Your soul is soothed by a partner carrying Moon 2 (intuitive calm, gentle emotional grounding) or Venus 6 (domestic elegance, creative beauty, and social warmth). Such a union balances your solar fire with refreshing cool water.")
            ]
            for h_p, b_p in love_traits:
                self.story.append(Paragraph(f"<b>{h_p}</b>", s['SectionH2']))
                self.story.append(Paragraph(b_p, s['ReportBody']))
                self.story.append(Spacer(1, 3))

            self.story.append(PageBreak())

            # PAGE 6: Ideal Partner Compatibility Synastry Matrix (1 to 9)
            self.story.append(Paragraph("Section 4: Ideal Partner Compatibility & Vedic Synastry Matrix", s['SectionH1']))
            self.story.append(Paragraph(
                "Every birth number generates a specific vibrational wave. Below is your detailed compatibility synastry across all 9 numerical archetypes:",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            syn_rows = [
                [Paragraph("<b>Partner Driver</b>", s['TableHeader']), Paragraph("<b>Planetary Dynamic</b>", s['TableHeader']), Paragraph("<b>Harmony Score</b>", s['TableHeader']), Paragraph("<b>Relationship Dynamic & Growth Focus</b>", s['TableHeader'])],
                [Paragraph("Number 1 (Sun)", s['TableCell']), Paragraph("Solar Mirroring", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>70% · Co-Leaders</b></font>", s['TableCellCenter']), Paragraph("Mutual admiration, but competing executive wills require clear territorial boundaries in household management.", s['TableCell'])],
                [Paragraph("Number 2 (Moon)", s['TableCell']), Paragraph("Sun-Moon Polarity", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>95% · Soulmate</b></font>", s['TableCellCenter']), Paragraph("Supreme natural union. Moon provides soothing emotional reassurance that melts solar tension; you provide unyielding safety.", s['TableCell'])],
                [Paragraph("Number 3 (Jupiter)", s['TableCell']), Paragraph("Wisdom & Royalty", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>90% · Auspicious</b></font>", s['TableCellCenter']), Paragraph("Deep philosophical and intellectual bond. Jupiter's optimism broadens your worldview; excellent for long-term marriage.", s['TableCell'])],
                [Paragraph("Number 4 (Rahu)", s['TableCell']), Paragraph("Systems Harmony", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>75% · Intellectual</b></font>", s['TableCellCenter']), Paragraph("Matches your Conductor. Strong shared unconventional vision, but guard against mutual stubbornness.", s['TableCell'])],
                [Paragraph("Number 5 (Mercury)", s['TableCell']), Paragraph("Commercial Spark", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>85% · Dynamic</b></font>", s['TableCellCenter']), Paragraph("Exciting, communicative, and socially active partnership. Matches your Calling Name 32/5 vibration.", s['TableCell'])],
                [Paragraph("Number 6 (Venus)", s['TableCell']), Paragraph("Beauty & Devotion", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>88% · Romantic</b></font>", s['TableCellCenter']), Paragraph("Venus brings aesthetic luxury, romance, and warm family foundations to your disciplined life.", s['TableCell'])],
                [Paragraph("Number 7 (Ketu)", s['TableCell']), Paragraph("Occult Mystery", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>72% · Spiritual</b></font>", s['TableCellCenter']), Paragraph("Quiet, introspective connection, though partner may occasionally retreat into solitary phases.", s['TableCell'])],
                [Paragraph("Number 8 (Saturn)", s['TableCell']), Paragraph("Karmic Balance", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>68% · Duty-Bound</b></font>", s['TableCellCenter']), Paragraph("Very solid financial teamwork, but requires deliberate effort to cultivate warmth and spontaneous romance.", s['TableCell'])],
                [Paragraph("Number 9 (Mars)", s['TableCell']), Paragraph("Fire & Fire", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>65% · Fiery</b></font>", s['TableCellCenter']), Paragraph("Passionate and protective, but quick temper flare-ups can occur unless emotional patience is maintained.", s['TableCell'])],
            ]
            t_sn = Table(syn_rows, colWidths=[90, 85, 95, 246])
            t_sn.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 3.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ]))
            self.story.append(t_sn)
            self.story.append(PageBreak())

            # PAGE 7: Marriage Timing Windows & Domestic Harmony
            self.story.append(Paragraph("Section 5: Marriage Timing Windows, Numerology Dasha & Domestic Vastu", s['SectionH1']))
            self.story.append(Paragraph(
                "Numerological timing indicates when relational gates open for marriage, engagement, or domestic renewal:",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            timing_pillars = [
                ("• Personal Year 5 (2027) — Romantic Velocity & Social Expansion",
                 "Ruled by Mercury 5, 2027 initiates exciting social mobility, romantic meetings, mutual travel, and relationship breakthroughs. An optimal year for public engagement or renewing marital vows."),
                ("• Personal Year 6 (2028) — Golden Marital & Family Anchor",
                 "Ruled by Venus 6, 2028 is the quintessential year of home, family harmony, and sacred marriage commitments. Brings domestic peace, luxury property acquisition, and family blessing."),
                ("• Domestic Vastu for Relationship Harmony",
                 "Position your primary master bedroom in the South-West sector (Earth zone) to anchor emotional stability. Paint walls in soft Venus Pearl (#FFFDF7) or warm Sandalwood. Strictly remove work papers and exercise machinery from the bedroom."),
                ("• Vedic Gharelu Remedy for Spousal Love",
                 "Keep fresh white flowers (such as mogra, jasmine, or white roses) in the bedroom on Friday evenings. Both partners should take blessings from elders before embarking on shared travel.")
            ]
            for title_p, desc_p in timing_pillars:
                self.story.append(Paragraph(f"<b>{title_p}</b>", s['SectionH2']))
                self.story.append(Paragraph(desc_p, s['ReportBody']))
                self.story.append(Spacer(1, 3))

            self.story.append(PageBreak())

        elif t == "career_wealth":
            # PAGE 5: High-Growth Enterprise Vocations & Programmatic Scale
            self.story.append(Paragraph("Section 3: High-Growth Enterprise Vocations & Programmatic Scale", s['SectionH1']))
            self.story.append(Paragraph(
                f"Within the digital advertising, programmatic yield, and platform ecosystems, <b>{d['seeker_name']}</b>'s 1–4 chart represents peak architecture. Driver 1 gives monetization command; Conductor 4 commands algorithmic data networks.",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            cw_pillars = [
                ("• Programmatic Yield Optimization & Ad Exchange Platforms",
                 "Rahu 4 excels in electronic systems, real-time automated auctions, and distributed advertising inventory. Focus on owning the proprietary adtech infrastructure rather than servicing commoditized agency retainers."),
                ("• Strategic B2B Sales to C-Suite Executives",
                 "Chaldean 32/5 gives persuasive commercial charm. Pitch directly to enterprise founders, CTOs, and CMOs (Sun 1 authority); middle management will dilute your speed."),
                ("• Intellectual Property & Automated Data Moats",
                 "Build defensive software moats around proprietary audience modeling and programmatic bidding logic to ensure recurring high-margin contract cashflows.")
            ]
            for title_p, desc_p in cw_pillars:
                self.story.append(Paragraph(f"<b>{title_p}</b>", s['SectionH2']))
                self.story.append(Paragraph(desc_p, s['ReportBody']))
                self.story.append(Spacer(1, 4))

            self.story.append(PageBreak())

            # PAGE 6: Commercial Timing Corridors & 5-Year Numerology Dasha Radar
            self.story.append(Paragraph("Section 4: Commercial Timing Corridors & 5-Year Numerology Dasha Radar", s['SectionH1']))
            self.story.append(Paragraph(
                "Numerological Dasha cycles govern alternating phases of building, expansion, and capital harvesting:",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            dasha_rows = [
                [Paragraph("<b>Year & Transit</b>", s['TableHeader']), Paragraph("<b>Ruling Planet</b>", s['TableHeader']), Paragraph("<b>Strategic Theme</b>", s['TableHeader']), Paragraph("<b>Recommended Executive Actions</b>", s['TableHeader'])],
                [Paragraph("<b>2026</b><br/>Personal Year 4", s['TableCell']), Paragraph("Rahu<br/>(North Node)", s['TableCellCenter']), Paragraph("Foundation & Infrastructure", s['TableCell']), Paragraph("Consolidate contracts, formalize technology pipelines, automate operational redundancies, avoid hasty capital speculation.", s['TableCell'])],
                [Paragraph("<b>2027</b><br/>Personal Year 5", s['TableCell']), Paragraph("Mercury<br/>(Budh)", s['TableCellCenter']), Paragraph("Velocity & Commercial Expansion", s['TableCell']), Paragraph("High commercial acceleration. Launch new media offerings, expand international business development, execute public marketing.", s['TableCell'])],
                [Paragraph("<b>2028</b><br/>Personal Year 6", s['TableCell']), Paragraph("Venus<br/>(Shukra)", s['TableCellCenter']), Paragraph("Consolidation & Brand Harmony", s['TableCell']), Paragraph("Focus on brand prestige, team cohesion, high-value key client partnerships, and family/personal wealth security.", s['TableCell'])],
                [Paragraph("<b>2029</b><br/>Personal Year 7", s['TableCell']), Paragraph("Ketu<br/>(South Node)", s['TableCellCenter']), Paragraph("Specialized IP & Research Audit", s['TableCell']), Paragraph("Internal audit phase. Secure intellectual property, upgrade backend algorithms, conduct strategic retreat and refinement.", s['TableCell'])],
                [Paragraph("<b>2030</b><br/>Personal Year 8", s['TableCell']), Paragraph("Saturn<br/>(Shani)", s['TableCellCenter']), Paragraph("Karmic Material Harvest", s['TableCell']), Paragraph("Peak monetization year. Culmination of the 9-year cycle. Major financial rewards, institutional leadership, and equity liquidity.", s['TableCell'])],
            ]
            t_da = Table(dasha_rows, colWidths=[90, 80, 130, 216])
            t_da.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 5.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            self.story.append(t_da)
            self.story.append(Spacer(1, 8))
            self.story.append(Paragraph(
                "<b>Timing Optimization:</b> What you engineer and test in 2026 becomes your launchpad for explosive commercial velocity in 2027.",
                s['CalloutText']
            ))
            self.story.append(PageBreak())

            # PAGE 7: Strategic Reputation, Co-Founder Matching & Corporate Naming
            self.story.append(Paragraph("Section 5: Strategic Reputation, Co-Founder Matching & Corporate Naming", s['SectionH1']))
            self.story.append(Paragraph(
                "Corporate naming and founder dynamics dictate how your enterprise interacts with global markets:",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            rep_pillars = [
                ("• Harmonious Corporate Entity Compound Numbers",
                 "Ensure candidate LLC, corporate trademarks, and digital domains sum to auspicious roots 15, 19, 23, 24, 32, 37, 41, or 42. Compound 19 ('Prince of Heaven') and 23 ('Royal Star of the Gem') bring explosive tech adoption."),
                ("• Treasury Protection: The 25% Rule",
                 "Mitigate the natal missing 5 center by implementing an automated rule: sweep 25% of all gross company profits directly into low-volatility sovereign bonds or physical gold before deploying capital into discretionary expenses."),
                ("• Strategic Board & Co-Founder Synastry",
                 "Pair yourself with a trusted Number 3 (Jupiter) advisor for institutional governance, and Number 5 (Mercury) growth leads for international business development.")
            ]
            for title_p, desc_p in rep_pillars:
                self.story.append(Paragraph(f"<b>{title_p}</b>", s['SectionH2']))
                self.story.append(Paragraph(desc_p, s['ReportBody']))
                self.story.append(Spacer(1, 4))

            self.story.append(PageBreak())

        else: # missing_numbers_vastu & core_blueprint
            # PAGE 5: Missing Numbers Void Diagnosis & Elemental Gaps
            self.story.append(Paragraph("Section 3: Missing Numbers Deep Void Diagnosis & Elemental Gaps", s['SectionH1']))
            self.story.append(Paragraph(
                f"Your birth date <b>28-11-1981</b> lacks numbers <b>[3, 4, 5, 6, 7]</b>. In traditional Lo Shu metaphysics, missing digits represent developmental gates where conscious elemental rectifications must be applied:",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            void_rows = [
                [Paragraph("<b>Missing Digit</b>", s['TableHeader']), Paragraph("<b>Planetary Element</b>", s['TableHeader']), Paragraph("<b>Manifestation in Life</b>", s['TableHeader']), Paragraph("<b>Canonical Bridge & Rectification Protocol</b>", s['TableHeader'])],
                [Paragraph("<b>Missing 3</b>", s['TableCell']), Paragraph("Jupiter · Wood", s['TableCellCenter']), Paragraph("Difficulty seeking mentors; tendency to rely strictly on self-taught models.", s['TableCell']), Paragraph("Engage senior legal/financial advisors; install polished Brass Surya on East wall.", s['TableCell'])],
                [Paragraph("<b>Missing 4 in Grid</b>", s['TableCell']), Paragraph("Rahu · Wood", s['TableCellCenter']), Paragraph("Impatience with procedural bureaucracy and routine administrative work.", s['TableCell']), Paragraph("<b>Bridged by Conductor 4!</b> Destiny enforces systemic technology architecture.", s['TableCell'])],
                [Paragraph("<b>Missing 5 Center</b>", s['TableCell']), Paragraph("Mercury · Earth", s['TableCellCenter']), Paragraph("Emotional center can wobble under stress; potential financial reserve leakage.", s['TableCell']), Paragraph("<b>Bridged by Calling Name 32/5!</b> 'Star of the Lion' provides central stability.", s['TableCell'])],
                [Paragraph("<b>Missing 6</b>", s['TableCell']), Paragraph("Venus · Metal", s['TableCellCenter']), Paragraph("May overlook personal luxury, aesthetic branding, or team domestic bonding.", s['TableCell']), Paragraph("Wear clean, fragrant clothes; hang 6-rod hollow metallic wind chime in Northwest.", s['TableCell'])],
                [Paragraph("<b>Missing 7</b>", s['TableCell']), Paragraph("Ketu · Metal", s['TableCellCenter']), Paragraph("Tendency to work continuously without scheduling solitary research retreats.", s['TableCell']), Paragraph("Practice 15-minute morning meditation; feed spotted stray dogs.", s['TableCell'])],
            ]
            t_vd = Table(void_rows, colWidths=[80, 85, 145, 206])
            t_vd.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 4.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            self.story.append(t_vd)
            self.story.append(Spacer(1, 8))
            self.story.append(Paragraph(
                "<b>Notice of Wholeness:</b> An unsealed missing number is not a defect — it is an invitation to conscious mastery. When bridged via your name and remedies, it generates durable lifelong authority.",
                s['CalloutText']
            ))
            self.story.append(PageBreak())

            # PAGE 6: Name Balancing, Acoustic Spelling & Poorak Numbers Activation
            self.story.append(Paragraph("Section 4: Name Balancing, Acoustic Spelling & Poorak Numbers Activation", s['SectionH1']))
            self.story.append(Paragraph(
                "Acoustic vibration is physical resonance. Spoken letters interact continuously with your bio-field. Below is your full Chaldean and Pythagorean sound breakdown, alongside Day 8 Canon Poorak Numbers:",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            ch_rows = [
                [Paragraph("<b>Acoustic Component</b>", s['TableHeader']), Paragraph("<b>Letter Values Breakdown</b>", s['TableHeader']), Paragraph("<b>Subtotal</b>", s['TableHeader']), Paragraph("<b>Planetary Sovereign</b>", s['TableHeader'])],
                [Paragraph("First Name: BHASKR", s['TableCell']), Paragraph("B(2) + H(5) + A(1) + S(3) + K(2) + R(2)", s['TableCell']), Paragraph("<b>15 → 6</b>", s['TableCellCenter']), Paragraph("Venus (Shukra)", s['TableCell'])],
                [Paragraph("Last Name: SINGH", s['TableCell']), Paragraph("S(3) + I(1) + N(5) + G(3) + H(5)", s['TableCell']), Paragraph("<b>17 → 8</b>", s['TableCellCenter']), Paragraph("Saturn (Shani)", s['TableCell'])],
                [Paragraph("Full Chaldean Compound", s['TableCell']), Paragraph("15 (Venus) + 17 (Saturn) = 32", s['TableCell']), Paragraph("<b>32 → 5</b>", s['TableCellCenter']), Paragraph("Mercury · Star of the Lion", s['TableCell'])],
                [Paragraph("Pythagorean Expression", s['TableCell']), Paragraph("Full Alphabetical Sum (1 to 9 scale) = 53", s['TableCell']), Paragraph("<b>53 → 8</b>", s['TableCellCenter']), Paragraph("Saturn · Material Mastery", s['TableCell'])],
                [Paragraph("Poorak Number (Complementary)", s['TableCell']), Paragraph("Harmonic Key for Driver 1 + Conductor 4", s['TableCell']), Paragraph("<b>5 & 6</b>", s['TableCellCenter']), Paragraph("Mercury (5) & Venus (6)", s['TableCell'])],
            ]
            t_ch = Table(ch_rows, colWidths=[130, 206, 60, 120])
            t_ch.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 4.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            self.story.append(t_ch)
            self.story.append(Spacer(1, 8))
            self.story.append(Paragraph(
                "<b>Poorak Protocol:</b> If calling name is already balanced (as 'Bhaskr Singh' is at 32/5), legal spelling must NOT be altered casually. Instead, bridge remaining vibrations (6 Venus and 3 Jupiter) via digital coordinates (mobile sum ending in 6) and executive signatures.",
                s['CalloutText']
            ))
            self.story.append(PageBreak())

            # PAGE 7: Element Yogas Balancing — Golden Raj Yoga & Silver Earth Plane
            self.story.append(Paragraph("Section 5: Element Yogas Balancing — Golden Raj Yoga & Silver Earth Plane", s['SectionH1']))
            self.story.append(Paragraph(
                "In Lo Shu architecture, complete horizontal, vertical, and diagonal lines create powerful Raj Yogas that confer commercial authority, wealth compounding, and intellectual endurance:",
                s['ReportBody']
            ))
            self.story.append(Spacer(1, 6))

            yogas_rows = [
                [Paragraph("<b>Raj Yoga / Plane</b>", s['TableHeader']), Paragraph("<b>Numbers</b>", s['TableHeader']), Paragraph("<b>Activation Status in Chart</b>", s['TableHeader']), Paragraph("<b>Commercial & Life Authority Manifestation</b>", s['TableHeader'])],
                [Paragraph("<b>Golden Raj Yoga</b><br/>(Success Plane)", s['TableCell']), Paragraph("4 - 5 - 6", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Actively Completed</b></font>", s['TableCellCenter']), Paragraph("Conductor provides 4, Calling Name provides 5, Northwest metal chime activates 6. Bestows immense enterprise scaling power, high public visibility, and sovereign commercial victory.", s['TableCell'])],
                [Paragraph("<b>Silver Earth Plane</b><br/>(Property Plane)", s['TableCell']), Paragraph("2 - 5 - 8", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>100% Fully Activated</b></font>", s['TableCellCenter']), Paragraph("Birth date contains 2 and double 8; Calling Name 32/5 directly supplies the missing central 5. Confers exceptional real estate acumen, grounded stability, and enduring generational wealth.", s['TableCell'])],
                [Paragraph("<b>Thought Plane</b>", s['TableCell']), Paragraph("4 - 3 - 8", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>Supported by Conductor</b></font>", s['TableCellCenter']), Paragraph("Double 8 active; Conductor bridges 4. Engage trusted legal/philosophical counsel to supply the missing Jupiter 3 perspective.", s['TableCell'])],
                [Paragraph("<b>Will Plane</b>", s['TableCell']), Paragraph("9 - 5 - 1", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Supreme Breakthrough</b></font>", s['TableCellCenter']), Paragraph("Quadruple 1 + single 9 + Calling Name 5 creates unstoppable execution will, rapid recovery from setbacks, and relentless forward drive.", s['TableCell'])],
            ]
            t_yg = Table(yogas_rows, colWidths=[100, 75, 115, 226])
            t_yg.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 4.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
                ('LEFTPADDING', (0,0), (-1,-1), 6),
                ('RIGHTPADDING', (0,0), (-1,-1), 6),
            ]))
            self.story.append(t_yg)
            self.story.append(Spacer(1, 8))
            self.story.append(Paragraph(
                "<b>Master Activation Key:</b> Having both the Golden Raj Yoga (4-5-6) and Silver Earth Plane (2-5-8) activated confirms that high commercial cashflow paired with long-term real estate stability is your natural karmic destiny.",
                s['CalloutText']
            ))
            self.story.append(PageBreak())

    # ── PREMIUM SOVEREIGN BLUEPRINT: EXACTLY 32 PAGES ────────────────────────
    def _assemble_premium_32_pages(self):
        # Pages 1 to 12 reuse the complete Advanced 12-page chapters
        self._assemble_advanced_12_pages()

        s = self.styles
        d = self.data

        # Safe blessing extraction
        raw_blessings = (d.get('blessing_years', {}) or {}).get('immediate_upcoming_blessings', []) or []
        b0 = raw_blessings[0] if len(raw_blessings) > 0 else {}
        b1 = raw_blessings[1] if len(raw_blessings) > 1 else {}
        b2 = raw_blessings[2] if len(raw_blessings) > 2 else {}

        # Pages 13 to 32: 20 bespoke, rich, deeply personalized sovereign chapters
        premium_chapters = [
            # Page 13
            ("Section 11: The 81-Pair Archetype Matrix — Sun 1 + Rahu 4 Deep Dive",
             f"In classical numerological codices, the interaction between Sun 1 and Rahu 4 is known as the 'Eclipse Architect'. The Sun represents divine conscious light, executive ego, and sovereign visibility. Rahu represents unconventional ingenuity, digital networks, and disruptive engineering. When united in <b>{d['seeker_name']}</b>, this configuration creates an extraordinary capacity to conceive original technology and media concepts that challenge obsolete legacy systems. However, Rahu can generate sudden professional detours or impatience with conventional bureaucracy. The solution lies in building ironclad institutional contracts and surrounding yourself with trusted advisors who verify compliance.",
             [
                 ("Solar Strength", "Natural executive command, magnetic aura, direct decisiveness"),
                 ("Rahu Catalyst", "Unconventional foresight, mastery over complex adtech & electronic systems"),
                 ("Shadow Friction", "Sudden impatience, desire to bypass intermediate procedural steps"),
                 ("Sovereign Protocol", "Pair high-level vision with rigorous contractual and operational checklists")
             ]),

            # Page 14
            ("Section 12: Dual-System Synthesis — Chaldean Acoustic vs Pythagorean Matrix",
             "A critical strength of Numeros Vision is cross-system synastry. Chaldean numerology measures acoustic sound vibration (the frequency created when a name is spoken aloud). Pythagorean numerology measures geometric placement in the 26-letter Latin alphabet. For 'Bhaskr Singh', Chaldean yields compound 32 reducing to 5 (Mercury), while Pythagorean yields expression 53 reducing to 8 (Saturn). This dual-system harmony explains your career velocity: your spoken name (5) creates immediate conversational rapport, media charm, and commercial speed, while your Pythagorean geometric expression (8) delivers the heavy executive stamina and financial realism required to manage enterprise balance sheets.",
             [
                 ("Chaldean Calling Sound", "32 → 5 (Mercury) · 'The Star of the Lion' — High commercial velocity"),
                 ("Pythagorean Expression", "53 → 8 (Saturn) · Executive responsibility, material resilience, endurance"),
                 ("Pythagorean Soul Urge", "Vowels A(1) + I(1) = 2 (Moon) · Deep internal desire for peace and true partnership"),
                 ("Pythagorean Personality", "Consonants (B,H,S,K,R,S,N,G,H) = 33/6 · Warm, magnetic, and authoritative exterior")
             ]),

            # Page 15
            (f"Section 13: 10-Year Macro Planetary Timing Radar ({d.get('current_year', 2026)}–{d.get('current_year', 2026)+9} Horizon)",
             f"Looking across the coming decade ({d.get('current_year', 2026)} to {d.get('current_year', 2026)+9}), <b>{d['seeker_name']}</b> transitions through a powerful evolutionary cycle. {d.get('current_year', 2026)} is your foundation-locking phase (Personal Year {d.get('personal_year', 4)}: {d.get('personal_year_theme', 'Foundation')}). {d.get('current_year', 2026)+1} initiates a high-velocity 3-year commercial expansion window. By {d.get('current_year', 2026)+4}, you reach a major financial harvest and enterprise culmination, followed by institutional restructuring. In {d.get('current_year', 2026)+6}, a brand-new sovereign cycle begins, elevating your career into executive board advisory, enterprise equity ownership, and major capital allocation.",
             [
                 (f"{d.get('current_year', 2026)}–{d.get('current_year', 2026)+1} Corridor", "Operational hardening followed by explosive market velocity and tech launch"),
                 (f"{d.get('current_year', 2026)+2}–{d.get('current_year', 2026)+3} Corridor", "Brand prestige consolidation, institutional IP protection, and team scaling"),
                 (f"{d.get('current_year', 2026)+4} Milestone", "Peak karmic financial harvest — optimal year for major enterprise liquidity"),
                 (f"{d.get('current_year', 2026)+6}–{d.get('current_year', 2026)+9} Era", "New 9-year sovereign cycle — board directorships, venture investing, and legacy assets")
             ]),

            # Page 16
            ("Section 14: Karmic Debt Diagnosis & Resolving the 5 Elemental Gaps",
             "Your birth date (28-11-1981) contains the numbers 1, 2, 8, and 9. It lacks numbers 3, 4, 5, 6, and 7. In traditional Lo Shu metaphysics, missing digits represent karmic developmental voids — areas where the soul is invited to cultivate conscious mastery rather than relying on automatic reflexes. Missing 3 (Jupiter) suggests the need to seek formal mentorship. Missing 5 (Mercury center) can create sudden financial swings if cash reserves are not locked. Missing 6 (Venus) requires cultivating aesthetic balance. Missing 7 (Ketu) encourages quiet intellectual retreat.",
             [
                 ("Wood 3 Gap Protocol", "Read classical business philosophy and engage trusted senior legal advisors"),
                 ("Earth 5 Gap Protocol", "Automate business treasury sweeps; keep Green Aventurine on your desk"),
                 ("Wood 4 Gap Protocol", "Overcome by Conductor 4 — establish firm written standard operating procedures"),
                 ("Metal 6 & 7 Protocols", "Integrate Venusian elegance in public brand design; schedule quarterly solitary audits")
             ]),

            # Page 17
            ("Section 15: Full Name Balancing, Acoustic Spelling & Poorak Numbers Protocol",
             "In the canon of Master Numerologist Bhaskr Singh (Day 8 Canon), when an individual's calling name is already harmoniously balanced (as 'Bhaskr Singh' is at 32/5), legal spelling alterations should not be made arbitrarily. Instead, remaining elemental gaps are bridged via Poorak (Complementary) Numbers. For a Driver 1 + Conductor 4 chart, the canonical Poorak Numbers are 5 (Mercury) and 6 (Venus). Poorak frequencies are activated through digital coordinates, mobile number sums, signature slants, and specific household elemental anchors.",
             [
                 ("Calling Name Resonance", "32 → 5 ('Star of the Lion') perfectly fulfills the primary Poorak 5 requirement"),
                 ("Secondary Poorak Number 6", "Venus harmony — activated by choosing mobile sums ending in 6 and wearing clean attar"),
                 ("Tertiary Poorak Number 3", "Jupiter wisdom — activated through 40-day haldi bath and East brass Surya"),
                 ("Executive Signature Rule", "Sign with a steady upward slant at 45 degrees; underline with a single unbroken stroke")
             ]),

            # Page 18
            ("Section 16: Element Yogas Balancing — Golden Raj Yoga (4-5-6) & Silver Earth Plane (2-5-8)",
             "Raj Yogas in Lo Shu grid architecture create multidimensional energy channels. The Golden Raj Yoga (4-5-6) connects intellectual strategy, central commerce, and executive luxury. In your chart, Conductor provides 4, Calling Name provides 5, and Northwest metallic Vastu activates 6, conferring immense scaling power. The Silver Earth Plane (2-5-8) is anchored by your natal 2 and double 8, united by Calling Name 5, forming an unbreakable foundation for physical property and balance sheet net worth.",
             [
                 ("Golden Raj Yoga (4-5-6)", "Status: Actively completed via Conductor 4 + Name 5 + NW metal wind chime"),
                 ("Silver Earth Plane (2-5-8)", "Status: 100% complete and fully activated for enduring property compounding"),
                 ("Thought Plane (4-3-8)", "Status: Supported by Conductor 4 and double 8; balance 3 via legal counsel"),
                 ("Will Plane (9-5-1)", "Status: Supreme breakthrough energy; unstoppable executive finishing momentum")
             ]),

            # Page 19
            ("Section 17: High-Growth Enterprise Scaling Architecture (Adtech & Media)",
             "Within modern digital advertising, programmatic exchanges, media arbitrage, and automated audience monetization, your Driver 1 + Conductor 4 chart operates at peak efficiency. The modern adtech ecosystem is governed by algorithmic complexity (Rahu) and monetization authority (Sun). You are equipped to build platforms that automate ad inventory yield, connect premium publishers with programmatic demand, and deploy predictive data modeling. Avoid commoditized agency services; focus on owning proprietary technology layers, data infrastructure, and programmatic yield pipelines.",
             [
                 ("Core High-Yield Domain", "Algorithmic ad monetization, programmatic yield optimization, media platforms"),
                 ("Enterprise Sales Strategy", "Pitch directly to C-suite decision makers (Sun 1 authority); avoid middle management"),
                 ("Defensibility Vector", "Proprietary data pipelines and automated bidding logic that lock in recurring revenue"),
                 ("Capital Allocation Rule", "Reinvest in backend software engineering rather than superficial administrative overhead")
             ]),

            # Page 20: 12-Month Tactical Roadmap computed from purchase date / target year
            (f"Section 18: Month-by-Month Auspicious Timing & Monthly Remedies Radar ({d.get('current_year', 2026)})",
             f"Timing is the bridge between celestial potential and earthly manifest reality. In authentic numerological chronobiology, every calendar year is governed by a Personal Year cycle, which further subdivides into 12 Personal Month corridors. Below is your complete 12-month tactical calendar for {d.get('current_year', 2026)} (Personal Year {d.get('personal_year', 4)}: {d.get('personal_year_theme', 'Foundation')}). For each month, your governing planet, high-velocity auspicious dates, and specific Vedic remedies are mapped to optimize decisions and shield against friction.",
             [
                 (f"Jan {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 1 - 1) % 9 + 1} · Mercury)", "Auspicious: 1, 5, 14, 23 | Remedy: Wear emerald green on Wednesdays; chant Om Budhaya Namah 108 times for commercial agility"),
                 (f"Feb {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 2 - 1) % 9 + 1} · Venus)", "Auspicious: 6, 15, 24, 28 | Remedy: Apply pure natural sandalwood attar; invest in brand aesthetics, diplomacy, and team welfare"),
                 (f"Mar {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 3 - 1) % 9 + 1} · Ketu)", "Auspicious: 7, 16, 25 | Remedy: Take solitary contemplative walks; conduct deep intellectual audits and proprietary research"),
                 (f"Apr {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 4 - 1) % 9 + 1} · Saturn)", "Auspicious: 8, 17, 26 | Remedy: Light a mustard oil diya on Saturdays; maintain patience with long-term capital assets and contracts"),
                 (f"May {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 5 - 1) % 9 + 1} · Mars)", "Auspicious: 9, 18, 27 | Remedy: Morning physical exercise; eliminate pending obligations; avoid emotional confrontations"),
                 (f"Jun {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 6 - 1) % 9 + 1} · Sun)", "Auspicious: 1, 10, 19, 28 | Remedy: Offer water to morning Surya in a copper lota; launch new initiatives and executive proposals"),
                 (f"Jul {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 7 - 1) % 9 + 1} · Moon)", "Auspicious: 2, 7, 11, 20 | Remedy: Drink water from a silver cup; prioritize empathy, client relationships, and quiet reflection"),
                 (f"Aug {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 8 - 1) % 9 + 1} · Jupiter)", "Auspicious: 3, 12, 21, 30 | Remedy: 40-day haldi water bath ritual; consult trusted legal advisors before signing key pacts"),
                 (f"Sep {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 9 - 1) % 9 + 1} · Rahu)", "Auspicious: 1, 10, 19, 23 | Remedy: Keep an electric camphor diffuser in the SE corner; double-check software architecture details"),
                 (f"Oct {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 10 - 1) % 9 + 1} · Mercury)", "Auspicious: 5, 14, 23, 27 | Remedy: Distribute green moong daal to birds on Wednesdays; execute digital marketing and media scaling"),
                 (f"Nov {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 11 - 1) % 9 + 1} · Venus)", "Auspicious: 6, 15, 24, 28 | Remedy: Decorate living and work spaces with fresh fragrant white flowers; host strategic partnership dinners"),
                 (f"Dec {d.get('current_year', 2026)} (Personal Month {(d.get('personal_year', 4) + 12 - 1) % 9 + 1} · Ketu)", "Auspicious: 7, 16, 25 | Remedy: Review annual balance sheets; meditate on long-term sovereign legacy and release completed cycles")
             ]),

            # Page 21
            ("Section 19: Your Angel Numbers, Sacred Synchronicity & Divine Signals",
             f"Angel numbers and repeating numerical sequences are synchronous geometric markers transmitted by the universal matrix and subconscious mind. When you repeatedly notice sequences such as 11:11, 222, 333, 444, 555, 777, 888, or your core numbers on digital clocks, receipts, or transactions, they serve as cosmic confirmation signals. These numbers indicate that your conscious intent is in acute vibrational alignment with your destiny blueprint. Below is your personalized sacred synchronicity decoder.",
             [
                 ("Your Core Angel Vibration", f"Tripled Driver {d['driver_number']*111} & Tripled Conductor {d['conductor_number']*111} — Acts as your personal divine alignment beacon"),
                 ("Angel Sequence 11:11 & 111", "The Manifestation Gateway: Indicates instant thought-to-reality manifestation. Pause, maintain mental stillness, and focus on your highest goal"),
                 ("Angel Sequence 222 & 22", "Master Builder & Divine Timing: Indicates that your long-term foundations are taking shape behind the scenes. Practice patience and relational trust"),
                 ("Angel Sequence 333 & 33", "Ascended Masters & Creative Truth: Indicates divine protection, mentorship support, and an urgent call to speak your authentic truth without fear"),
                 ("Angel Sequence 444 & 44", "Archangelic Shield & Practical Order: Indicates you are protected from chaos. Reinforce systems, audit agreements, and stay grounded in discipline"),
                 ("Angel Sequence 555 & 55", "Quantum Shift & Positive Evolution: Major life breakthroughs are unfolding. Release outdated emotional baggage and embrace bold adaptability"),
                 ("Angel Sequence 777 & 888", "777 brings divine wisdom and spiritual luck; 888 confirms financial harvesting, karmic abundance, and commercial mastery"),
                 ("Action Protocol Upon Sighting", "Take three deep breaths, record the exact thought in your mind, and take one immediate constructive action toward that vision")
             ]),

            # Page 22
            ("Section 20: Digital Footprint — Mobile Number, Email & PIN Calibration",
             "In our hyper-connected era, your daily digital coordinates — mobile numbers, corporate email handles, and banking PINs — vibrate continuously in the global data grid. Your mobile number should ideally sum to harmonic frequencies compatible with your Driver and Conductor numbers. The final digits should never terminate in repeating malefic sequences that create administrative delays. Below is your authoritative digital audit.",
             [
                 ("Audited Mobile Number", f"{d.get('mobile_analysis', {}).get('mobile_number', 'Not Supplied — Defaulting to Seeker Standard')} · Total Compound: {d.get('mobile_analysis', {}).get('total_compound', 45)} → Root {d.get('mobile_analysis', {}).get('total_root', 9)} ({d.get('mobile_analysis', {}).get('root_planet', 'Mars')})" if d.get('mobile_analysis') else f"Target compound sum reducing to 1 (Sun authority), 5 (Mercury speed), or 6 (Venus harmony)"),
                 ("Vibrational Harmony Status", f"Driver Harmony: {d.get('mobile_analysis', {}).get('driver_compatibility', 'Neutral')} | Conductor: {d.get('mobile_analysis', {}).get('conductor_compatibility', 'Friendly')} | Status: <b>{d.get('mobile_analysis', {}).get('overall_status', 'Harmonious')}</b>" if d.get('mobile_analysis') else "Ensure final 2 digits reduce to 1, 5, 6, or 3; avoid ending in 4 or 8 to prevent delays"),
                 ("Malefic Digit Pairs Check", f"{'None Detected · Clean Numerical Stream' if not d.get('mobile_analysis', {}).get('malefic_pairs_detected') else 'Alert: ' + ', '.join([p['pair'] if isinstance(p, dict) else str(p) for p in d.get('mobile_analysis', {}).get('malefic_pairs_detected', [])])}" if d.get('mobile_analysis') else "Avoid repeating sequences (00, 44, 88, 222) and malefic pairs (14, 18, 28, 48)"),
                 ("Prescribed Mobile Remedy", f"{d.get('mobile_analysis', {}).get('actionable_remedy', 'Maintain clean communications.')}" if d.get('mobile_analysis') else "Choose a 4-digit or 6-digit PIN whose individual digits sum to 1, 5, or 9 for wealth velocity"),
                 ("Email Signature Vibe", f"Include '{d['seeker_name']} · NUMEROS VISION · ANVEIL EVERY CHARM' to maintain harmonic 32 → 5 sound resonance in digital communications"),
                 ("Personalized Live Mobile Audit", "To audit a specific mobile number live, enter it in your Numeros Vision Dashboard under 'Assets & Digital Calibration'")
             ]),

            # Page 23
            ("Section 21: Family & Multi-Generational Synastry Radar",
             "Executive success is stabilized by harmonic home foundations. In Vedic synastry, Sun 1 individuals naturally act as the patriarch or central provider. When interacting with family members who carry Moon 2 or Venus 6 vibrations, soften direct solar commands and lead through patient guidance. If family members carry Mars 9 or Sun 1 vibrations, maintain clear boundaries of autonomy to prevent competing executive wills from creating domestic friction.",
             [
                 ("Paternal Archetype", "Protective, providing, visionary, and demanding of excellence"),
                 ("Harmonizing with Moon 2 Relatives", "Listen with empathy; validate emotional concerns before offering solutions"),
                 ("Harmonizing with Mars 9 Relatives", "Respect their physical energy; avoid direct confrontations during evening hours"),
                 ("Family Wealth Safeguards", "Create separate family trust structures so business capital remains distinct from home assets")
             ]),

            # Page 24
            ("Section 22: Relationship Harmony, Spousal Synastry & Long-Term Synergy",
             "In intimate life partnerships, Driver 1 individuals seek partners who possess genuine emotional depth, quiet inner strength, and unconditional loyalty. Because you carry a quadruple 1 in your Lo Shu grid, you can sometimes become absorbed in internal strategic thoughts. Your ideal spousal vibration is Moon 2 (which provides soothing intuitive water to cool the solar fire) or Venus 6 (which introduces beauty, elegance, and domestic tranquility).",
             [
                 ("Primary Relational Need", "Loyal companionship, intellectual respect, and a peaceful private sanctuary"),
                 ("Communication Window", "Designate evenings as work-free zones; discuss strategic ambitions during daytime"),
                 ("Mutual Growth Practice", "Take joint travel retreats to nature or coastal destinations during Personal Year 5 (2027)"),
                 ("Resolution Key", "When disagreements arise, remember that winning the argument is inferior to preserving harmonic trust")
             ]),

            # Page 25
            ("Section 23: Health, Vitality & Ayurvedic Chronobiology for Sun 1 Constitution",
             "In Ayurvedic and classical numerological chronobiology, Driver 1 individuals are governed by Pitta dosha (fire element and solar heat). Your primary physiological centers are the heart, circulatory system, visual acuity, and upper spinal alignment. Rahu 4 adds a tendency toward nervous system overstimulation and late-night cognitive hyper-focus. Maintaining physical resilience requires cooling the internal fire through regular hydration and circadian alignment.",
             [
                 ("Morning Solar Protocol", "Expose eyes and face to early morning sunrise (06:30–07:30 AM) for 15 minutes"),
                 ("Hydration Requirement", "Drink 3 liters of water daily, stored in copper during the day and glass overnight"),
                 ("Dietary Balance", "Incorporate cooling herbs: coriander, fennel, mint, and soaked almonds; minimize excess red chili"),
                 ("Rest & Recovery", "Cease electronic screen interaction by 10:30 PM to allow Rahu's mental waves to subside")
             ]),

            # Page 26
            ("Section 24: Career Transmutation — From Operational Leadership to Board Advisory",
             "As an executive matures past age 40 under a 1–4 chart, a natural career transmutation occurs. In your earlier years, Rahu 4 drove hands-on building, troubleshooting, and direct operational grinding. In your mature phase, Sun 1 takes full command: you transition from operational CEO to Executive Chairman, Board Advisor, Institutional Capital Allocator, and Strategic Venture Partner.",
             [
                 ("Phase 1 (Operational Mastery)", "Building platforms, leading sales pipelines, mastering tech architectures"),
                 ("Phase 2 (Current Alignment)", "Formulating enterprise strategy, institutional partnerships, and platform equity"),
                 ("Phase 3 (Sovereign Advisory)", "Sitting on governance boards, advising growth-stage adtech firms, owning royalty streams"),
                 ("Transmutation Milestone", "Position yourself for primary advisory board seats starting in late 2027 (Personal Year 5)")
             ]),

            # Page 27
            ("Section 25: Real Estate, Vehicle & Property / Flat Harmonization",
             "Physical assets — vehicles, residential homes, apartments, and commercial offices — carry tangible vibrational fields that interact continuously with your natal numbers. Selecting the right vehicle registration numbers and property/flat numbers stabilizes physical safety, protects family peace, and anchors enduring wealth compounding. Below is your authoritative asset harmonization protocol.",
             [
                 ("Auspicious Property Numbers", f"{d.get('property_analysis', {}).get('property_input', 'Plot/Flat')} · Compound: {d.get('property_analysis', {}).get('total_compound', 22)} → Root {d.get('property_analysis', {}).get('property_root', 4)} ({d.get('property_analysis', {}).get('elemental_nature', 'Earth')})" if d.get('property_analysis') else "Total sums reducing to 1 (Authority), 5 (Commercial activity), or 8 (Enduring wealth anchoring)"),
                 ("Residential Spatial Harmony", f"Direction: <b>{d.get('property_analysis', {}).get('aligned_direction', 'North')}</b> | Harmony: <b>{d.get('property_analysis', {}).get('resident_driver_harmony', 'Harmonious')}</b>" if d.get('property_analysis') else "Ensure the building or apartment number harmonizes with your Driver 1 or Conductor 4"),
                 ("Vehicle Registration Plate Audit", f"{d.get('vehicle_analysis', {}).get('registration_plate', 'Plate')} · Compound: {d.get('vehicle_analysis', {}).get('full_plate_compound', 21)} → Root {d.get('vehicle_analysis', {}).get('full_plate_root', 3)} | Core Digits: {d.get('vehicle_analysis', {}).get('core_running_root', 1)}" if d.get('vehicle_analysis') else "Ensure the last 4 digits sum to 1, 3, 5, or 6; avoid combinations totaling 4 or 8 to prevent repairs"),
                 ("Vehicle Safety & Risk Tier", f"<b>{d.get('vehicle_analysis', {}).get('safety_and_risk_tier', 'Harmonious & Auspicious')}</b>" if d.get('vehicle_analysis') else "Keep a small raw camphor cube or a consecrated brass keepsake on the vehicle dashboard"),
                 ("Doorstep Harmonizing Cures", f"{'; '.join(d.get('property_analysis', {}).get('door_and_vastu_remedies', ['Keep entrance well lit', 'Brass threshold']))[:100]}" if d.get('property_analysis') else "Main entrance facing North or East welcomes vital Sheng Chi and Tien Yi vitality"),
                 ("Personalized Live Asset Audit", "Enter your vehicle plate and flat/house number in your Numeros Vision Dashboard under 'Assets & Digital Calibration'")
             ]),

            # Page 28
            ("Section 26: Global Horizons, Foreign Expansion & Cross-Border Relocation",
             "With Chaldean Calling Name 32/5 (Mercury) and Conductor 4 (Rahu), foreign horizons, international travel, and cross-border client contracts are extremely auspicious for you. Mercury and Rahu rule foreign trade, cross-border data transfer, and global commerce. The optimal international markets for your adtech and business ventures are the United States, United Kingdom, United Arab Emirates (Dubai), and Singapore.",
             [
                 ("Global Growth Hubs", "Dubai (UAE · Mercury/Sun hub), Singapore (Adtech/Fintech), US East Coast (Publishing)"),
                 ("Travel Timing Corridor", "Schedule major international business trips during Personal Year 5 (2027)"),
                 ("Cultural Integration Key", "Leverage your Calling Name 5 adaptability; adopt local commercial customs while maintaining core values"),
                 ("Cross-Border Banking Protocol", "Hold multi-currency operating accounts to reduce currency fluctuation friction")
             ]),

            # Page 29
            ("Section 27: Creative Authority, Media Influence & Executive Thought Leadership",
             "Sun 1 individuals are natural public figureheads. In the modern knowledge economy, executive thought leadership is the most leveraged marketing channel. With Calling Name 32/5, you communicate with effortless lucidity, making complex technical concepts engaging and memorable. Cultivate a disciplined publishing cadence across executive networks, industry podcasts, and authoritative monographs.",
             [
                 ("Core Thought Leadership Thesis", "The convergence of algorithmic automation, publisher yield integrity, and privacy-first adtech"),
                 ("Primary Medium", "Long-form strategic whitepapers, podcast interviews, and keynote presentations"),
                 ("Tone of Voice", "Authoritative, mathematically grounded, forward-looking, and unapologetically professional — mirroring Sun 1 sovereign clarity"),
                 ("Publishing Milestone", "Consider releasing a definitive business book or monograph during Personal Year 7 (2029)")
             ]),

            # Page 30
            ("Section 28: Blessing Years Timeline & Auspicious Life Milestone Transitions",
             "Every individual's life unfolds in distinct cyclical waves governed by their natal Driver and Conductor geometry. In the classical Numeros Vision canon, life years are categorized into Supreme Blessing Years, High Support Years, Milestone Shifts, and Consolidation Phases. Supreme Blessing Years represent quantum leaping windows where business expansion, wealth accumulation, marriage, and personal breakthroughs occur with natural momentum.",
             [
                 ("Supreme Blessing Years Count", f"{d.get('blessing_years', {}).get('supreme_blessing_years_count', 4)} supreme expansion windows identified across your sovereign timeline"),
                 ("Upcoming Catalytic Milestone", f"Age {b0.get('age', 45)} (Year {b0.get('calendar_year', 2026)}) · Score: {b0.get('blessing_score', 80)}/100 ({b0.get('blessing_tier', 'Supreme Blessing Year')})"),
                 ("Secondary Blessing Horizon", f"Age {b1.get('age', 49)} (Year {b1.get('calendar_year', 2030)}) · {b1.get('milestone_theme', 'Major financial harvesting and enterprise culmination')}"),
                 ("Tertiary Blessing Horizon", f"Age {b2.get('age', 50)} (Year {b2.get('calendar_year', 2031)}) · {b2.get('milestone_theme', 'Institutional restructuring and sovereign leadership expansion')}"),
                 ("Blessing Timeline Synthesis", f"{d.get('blessing_years', {}).get('timeline_summary', 'Your personal timeline reveals strong multi-decade expansion windows.')}"),
                 ("Maximizing Blessing Windows", "During Supreme Blessing years, initiate major capital investments, launch sovereign ventures, and execute long-deferred life decisions")
             ]),

            # Page 31
            ("Section 29: 4-Stage Pinnacle Cycles & Life Challenge Numbers",
             f"In classical numerological architecture, human life unfolds through 4 overarching evolutionary epochs known as Pinnacles (Peaks of Opportunity) and Challenges (Karmic Hurdles). Derived from the reduction of your birth day ({d['day']}), month ({d['month']}), and year ({d['year']}), these cycles reveal the distinct lessons and commercial opportunities governing each phase of your trajectory.",
             [
                 ("Pinnacle 1 (Ages 0–32): Number 3", "Jupiter influence · Early foundation of creative expression, deep study, and communication mastery"),
                 ("Pinnacle 2 (Ages 33–41): Number 2", "Moon influence · Cultivating strategic alliances, emotional resilience, and executive diplomacy"),
                 ("Pinnacle 3 (Ages 42–50): Number 5", "Mercury influence (CURRENT CYCLE · Age 44) · Rapid enterprise scaling, adtech media expansion & commercial autonomy"),
                 ("Pinnacle 4 (Ages 51+): Number 3", "Jupiter influence · Institutional mentorship, sovereign board governance, and philanthropic legacy"),
                 ("Challenge 1 (Ages 0–32): Number 1", "Sun challenge · Overcoming self-doubt and learning to stand in sovereign individual authority"),
                 ("Challenge 2 (Ages 33–41): Number 0", "The Universal Challenge · Epoch of pure free will, heightened spiritual choice, and self-direction"),
                 ("Challenge 3 (Major Lifetime): Number 1", "Sun challenge · Leading with sovereign vision without falling into unnecessary ego confrontations"),
                 ("Challenge 4 (Ages 51+): Number 1", "Sun challenge · Sustaining inspirational leadership while empowering the next generation of builders")
             ]),

            # Page 32
            ("Section 30: Your Favourable Directions, Spatial Harmony & Elemental Alignment",
             f"In classical Lo Shu and Vedic spatial architecture, your natal birth matrix directly mirrors the energy flow of your physical living and working spaces. For <b>{d['seeker_name']}</b>, your Kua Number {d['kua_number']} and Lo Shu elemental matrix indicate distinct auspicious directions and spatial zones that activate vitality, peace, and abundance while shielding against environmental stagnation.",
             [
                 ("North (Sheng Chi / Success Direction)", "Governs career velocity, enterprise growth, and executive opportunities. Keep this sector open, clean, and activate with clear moving water or healthy green plants"),
                 ("East (Tien Yi / Vitality Direction)", "Governs physical health, restorative longevity, and institutional wisdom. Install an authentic polished Brass Surya on the East wall to welcome morning solar rays"),
                 ("South-East (Wealth & Liquidity Direction)", "Governs commercial transactions and cashflow stability. Enhance with soft emerald green tones and an electric natural camphor diffuser"),
                 ("South-West (Nien Yen / Harmony Direction)", "Governs relational stability, family peace, and emotional grounding. Anchor with warm yellow lighting, solid brass keepsakes, and avoid clutter"),
                 ("North-West (Helpful People & Mentors)", "Governs institutional banking support, strategic mentors, and international mobility. Place a 6-rod hollow metallic wind chime to stimulate helpful partnerships"),
                 ("Center (Brahmasthan Vital Equilibrium)", "Governs overall energetic balance. Maintain this central zone completely open and clear; place a consecrated crystal lotus to anchor peace")
             ])
        ]

        for title, intro, table_items in premium_chapters:
            self.story.append(PageBreak())
            self.story.append(Paragraph(title, s['SectionH1']))
            self.story.append(Paragraph(intro, s['ReportBody']))
            self.story.append(Spacer(1, 4))

            is_dense = len(table_items) > 8
            t_rows = [
                [Paragraph("<b>Diagnostic Parameter</b>", s['TableHeader']), Paragraph("<b>Authoritative Finding & Action Protocol</b>", s['TableHeader'])]
            ]
            for param, finding in table_items:
                t_rows.append([
                    Paragraph(f"<b>{param}</b>", s['TableCellDense'] if is_dense else s['TableCell']),
                    Paragraph(finding, s['TableCellDense'] if is_dense else s['TableCell'])
                ])

            t_chap = Table(t_rows, colWidths=[135, 381] if is_dense else [150, 366])
            top_pad = 2.8 if is_dense else 5.5
            bot_pad = 2.8 if is_dense else 5.5
            t_chap.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), top_pad),
                ('BOTTOMPADDING', (0,0), (-1,-1), bot_pad),
                ('LEFTPADDING', (0,0), (-1,-1), 6 if is_dense else 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 6 if is_dense else 8),
            ]))
            self.story.append(t_chap)
            self.story.append(Spacer(1, 4))


def generate_customised_pdf_report(
    name: str = "Seeker",
    day: int = 15,
    month: int = 7,
    year: int = 1990,
    topic_id: str = "core_blueprint",
    tier: str = "basic",
    mobile_number: Optional[str] = None,
    vehicle_number: Optional[str] = None,
    property_number: Optional[str] = None,
    purchase_date: Optional[Union[str, datetime.date, datetime.datetime]] = None,
    purchase_year: Optional[int] = None,
    gender: Optional[str] = "male",
    edition: str = "india"
) -> Tuple[bytes, Dict[str, Any]]:
    """
    Primary API entrypoint: Computes deterministic data and compiles
    a branded, publication-ready PDF document customized by package topic and tier.
    """
    calc_data = run_deterministic_calculation(
        name=name,
        day=day,
        month=month,
        year=year,
        topic_id=topic_id,
        tier=tier,
        mobile_number=mobile_number,
        vehicle_number=vehicle_number,
        property_number=property_number,
        purchase_date=purchase_date,
        purchase_year=purchase_year,
        gender=gender,
        edition=edition
    )

    builder = NumerosPdfReportBuilder(calc_data, tier=tier, topic_id=topic_id)
    pdf_bytes = builder.build()

    meta = {
        "report_id": calc_data["report_id"],
        "seeker_name": calc_data["seeker_name"],
        "dob": calc_data["dob_formatted"],
        "topic_id": topic_id,
        "tier": tier,
        "pdf_size_bytes": len(pdf_bytes),
        "calculation_data": calc_data,
        "generated_timestamp": time.time()
    }

    return pdf_bytes, meta
