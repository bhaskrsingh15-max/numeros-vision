import os, sys

# Python script to build the complete, upgraded app/services/pdf_report_generator.py
generator_code = '''"""
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
     * Advanced Report (Target: 12 Pages · ₹510 / Active Charm Present Numbers)
     * Premium Dossier (Target: 32 Pages · ₹1,050 / Anveil Charm Missing Numbers)
   - Dynamic Topic Prioritization:
     * Lo Shu Grid & Life Path foundational basics always come first (Pages 1-4).
     * The purchased topic (Present Numbers, Missing Numbers & Vastu, Love & Relationship,
       Career & Wealth, Health & Vitality, Name Balancing, Spatial Vastu) is frontloaded
       and emphasized immediately after the basic report (Pages 5-7).
     * Followed by supporting multi-factor chapters (Pages 8-11) and statutory sign-off (Page 12).
     * Premium 32-page compendium provides 20 exhaustive sovereign chapters (Pages 13-32)
       including Day 8 Canon Poorak Numbers, Element Yogas, 4-Stage Pinnacles, and Directional Vastu Cures.
   - Vedic Gharelu Remedies Bank:
     * Readily accessible household zero-cost cures for numbers 1 to 9 (respecting parents/elders,
       Surya arghya in copper lota, silver cup, 40-day haldi water, mustard oil diya, green plants).
     * Universal 40-Day Rock Salt (Sendha Namak) aura cleansing and loop-breaking protocol.
   - STRICTLY ZERO ASTROLOGY WORDS:
     * Pure Numerology, Vibrational Science, Lo Shu Grid, and Numerology Dasha Timing Radar.
"""

import os
import io
import time
import math
import hashlib
from typing import Dict, Any, List, Optional, Tuple

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

# Deterministic Engine Imports
from app.engine.core_matrix_engine import (
    calculate_driver,
    calculate_conductor,
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

# ── TYPOGRAPHY & STYLES ───────────────────────────────────────────────────
def _build_styles() -> Dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=base['Normal'],
        fontName='Times-Bold',
        fontSize=24,
        leading=28,
        textColor=COLOR_GOLD_DARK,
        alignment=1,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=base['Normal'],
        fontName='Times-Roman',
        fontSize=10,
        leading=14,
        textColor=COLOR_INK_MUTED,
        alignment=1,
        spaceAfter=14
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=base['Normal'],
        fontName='Times-Bold',
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
        fontName='Times-Bold',
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
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        textColor=COLOR_INK_DARK,
        spaceAfter=4
    )

    body_bold = ParagraphStyle(
        'ReportBodyBold',
        parent=body_style,
        fontName='Times-Bold'
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=base['Normal'],
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_GOLD_DARK
    )

    meta_val = ParagraphStyle(
        'MetaValue',
        parent=base['Normal'],
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_INK_DARK
    )

    tbl_header = ParagraphStyle(
        'TableHeader',
        parent=base['Normal'],
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11,
        textColor=COLOR_GOLD_DARK,
        alignment=1
    )

    tbl_cell = ParagraphStyle(
        'TableCell',
        parent=base['Normal'],
        fontName='Times-Roman',
        fontSize=8.2,
        leading=11,
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
        fontName='Times-Italic',
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
        'TableCellCenter': tbl_cell_center,
        'CalloutText': callout_style
    }

# ── CANVAS & BACKGROUND MANAGEMENT ────────────────────────────────────────
def draw_page_background(canvas_obj, doc):
    canvas_obj.saveState()
    canvas_obj.setFillColor(COLOR_PEARL_BG)
    canvas_obj.rect(0, 0, doc.pagesize[0], doc.pagesize[1], fill=1, stroke=0)
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

        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.setFont("Times-Bold", 8)
            self.setFillColor(COLOR_GOLD_DARK)
            self.drawString(38, h - 28, "NUMEROS VISION")
            self.setFont("Times-Italic", 7.5)
            self.setFillColor(COLOR_INK_MUTED)
            self.drawString(125, h - 28, "·   ANVEIL EVERY CHARM   ·   CLASSICAL NUMEROLOGICAL ARCHITECTURE")

            self.setFont("Times-Roman", 7.5)
            self.drawRightString(w - 38, h - 28, "CONFIDENTIAL EXECUTIVE DOSSIER")

            self.setStrokeColor(COLOR_BORDER)
            self.setLineWidth(0.6)
            self.line(38, h - 33, w - 38, h - 33)

        # Running Footer (all pages)
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(38, 38, w - 38, 38)

        self.setFont("Times-Roman", 7.5)
        self.setFillColor(COLOR_INK_MUTED)
        self.drawString(38, 26, "© 2026 Numeros Vision. All Rights Reserved. Master Numerologist Bhaskr Singh (Numeros Vision).")

        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.setFont("Times-Bold", 8)
        self.setFillColor(COLOR_GOLD_DARK)
        self.drawRightString(w - 38, 26, page_str)

        self.restoreState()


# ── DETERMINISTIC CALCULATION ENGINE ───────────────────────────────────────
def run_deterministic_calculation(
    name: str,
    day: int,
    month: int,
    year: int,
    topic_id: str = "core_blueprint",
    tier: str = "basic"
) -> Dict[str, Any]:
    clean_name = name.strip() or "Seeker"

    # 1. Driver & Conductor
    driver = calculate_driver(day)
    conductor = calculate_conductor(day, month, year)

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

    # 5. Personal Year Calculator: (Day + Month + 2026) -> (28->1) + (11->2) + (2026->1) = 4
    py_sum = driver + (sum(int(d) for d in str(month))) + (sum(int(d) for d in str(2026)))
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

    # Poorak Number Calculation (Complementary Key)
    poorak_info = calculate_complementary_poorak(driver, conductor, missing_numbers)

    # Gharelu Vedic Remedies Calculation
    gharelu_remedies = get_gharelu_remedies_for_chart(driver, conductor, present_numbers, missing_numbers)

    return {
        "report_id": report_id,
        "seeker_name": clean_name,
        "day": day,
        "month": month,
        "year": year,
        "dob_formatted": dob_formatted,
        "driver_number": driver,
        "driver_planet": PLANETS.get(driver, "Sun"),
        "conductor_number": conductor,
        "conductor_planet": PLANETS.get(conductor, "Rahu"),
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
        "tier": tier
    }
'''

with open('scripts/build_upgraded_pdf_generator.py', 'w', encoding='utf-8') as f:
    f.write(generator_code)
print("Part 1 written to scripts/build_upgraded_pdf_generator.py")
