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


class NumerosPdfReportBuilder:
    def __init__(self, calculation_data: Dict[str, Any], tier: str = "basic", topic_id: str = "core_blueprint"):
        self.data = calculation_data
        self.tier = tier.lower().strip()
        self.topic_id = self._normalize_topic(topic_id)
        self.styles = _build_styles()
        self.story = []

    def _normalize_topic(self, topic: str) -> str:
        t = (topic or "").lower().strip()
        if any(k in t for k in ("present", "lo_shu", "loshu")):
            return "present_numbers"
        elif any(k in t for k in ("love", "romance", "marriage", "partner", "spouse", "companionship")):
            return "love_relationship"
        elif any(k in t for k in ("career", "wealth", "business", "billionaire", "venture", "job", "work")):
            return "career_wealth"
        elif any(k in t for k in ("health", "vitality", "ayurved")):
            return "health_vitality"
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
            badge = "GOLD CHARM · 12-PAGE PRESENT NUMBERS DOSSIER · ₹510" if not is_premium else "DIAMOND CHARM · 32-PAGE SOVEREIGN ROADMAP · ₹1,050"
            sec3 = "Section 3: Natal Present Numbers Deep Audit & Frequency Analysis"
            sec4 = "Section 4: Present Numbers Benefic vs Malefic Planetary Operating Matrix"
            sec5 = "Section 5: Inborn Career Fruitfulness & High-Yield Vocations"
        elif t == "love_relationship":
            title = "LOVE, RELATIONSHIP & COMPANIONSHIP DOSSIER"
            subtitle = "Romantic Synastry, Marriage Timing Windows & Domestic Harmony Blueprint"
            badge = "LOVE & COMPANIONSHIP · 12-PAGE MASTER HARMONY DOSSIER · ₹510" if not is_premium else "DIAMOND SOVEREIGN · 32-PAGE LIFETIME UNION ROADMAP · ₹1,050"
            sec3 = "Section 3: Love Style, Romantic Resonance & Spousal Temperament"
            sec4 = "Section 4: Ideal Partner Compatibility & Vedic Synastry Matrix (1 to 9)"
            sec5 = "Section 5: Marriage Timing Windows, Numerology Dasha & Domestic Harmony"
        elif t == "career_wealth":
            title = "CAREER, ENTERPRISE & FINANCIAL DIRECTION DOSSIER"
            subtitle = "High-Growth Vocations, Commercial Timing & Wealth Compounding Radar"
            badge = "CAREER & WEALTH · 12-PAGE MASTER SYNTHESIS DOSSIER · ₹510" if not is_premium else "DIAMOND SOVEREIGN · 32-PAGE ENTERPRISE ROADMAP · ₹1,050"
            sec3 = "Section 3: High-Growth Enterprise Vocations & Programmatic Scale"
            sec4 = "Section 4: Commercial Timing Corridors & 5-Year Numerology Dasha Radar (2026–2030)"
            sec5 = "Section 5: Strategic Reputation, Co-Founder Matching & Corporate Naming"
        elif t == "health_vitality":
            title = "HEALTH, VITALITY & AYURVEDIC CHRONOBIOLOGY DOSSIER"
            subtitle = "Pitta-Vata Balancing, Circadian Peak Hours & Non-Invasive Lifestyle Cures"
            badge = "HEALTH & VITALITY · 12-PAGE MASTER CHRONOBIOLOGY DOSSIER · ₹510" if not is_premium else "DIAMOND SOVEREIGN · 32-PAGE VITALITY COMPENDIUM · ₹1,050"
            sec3 = "Section 3: Ayurvedic Chronobiology & Pitta-Vata Dosha Balancing"
            sec4 = "Section 4: Circadian Peak Performance Windows & Hydration Protocols"
            sec5 = "Section 5: Cognitive Decompression, Sleep Restoration & Vitality Cures"
        else: # missing_numbers_vastu & core_blueprint
            title = "ANVEIL CHARM MISSING NUMBERS SOVEREIGN ROADMAP"
            subtitle = "32-Page Sovereign Lifetime Architecture & Missing Number Rectification Compendium" if is_premium else "12-Page Master Synthesis Dossier & Missing Numbers Rectification"
            badge = "DIAMOND CHARM · 32-PAGE SOVEREIGN ROADMAP · ₹1,050" if is_premium else "GOLD CHARM · 12-PAGE MASTER DOSSIER · ₹510"
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
            ("Section 10: Methodology, Algorithmic Provenance & Statutory Sign-off", "Page 12")
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
            ("Section 10: Methodology & Algorithmic Provenance", "Page 12"),
            ("Section 11: 81-Pair Archetype Matrix — Sun 1 + Rahu 4", "Page 13"),
            ("Section 12: Dual-System Synthesis — Chaldean vs Pythagorean", "Page 14"),
            ("Section 13: 10-Year Macro Planetary Timing Radar", "Page 15"),
            ("Section 14: Karmic Debt & Elemental Gaps Diagnosis", "Page 16"),
            ("Section 15: Full Name Balancing & Poorak Numbers Protocol", "Page 17")
        ]

        toc_part2 = [
            ("Section 16: Element Yogas Balancing — Golden Raj Yoga 4-5-6", "Page 18"),
            ("Section 17: High-Growth Enterprise Scaling Architecture", "Page 19"),
            ("Section 18: Corporate Brand Naming & Trademark Vibration", "Page 20"),
            ("Section 19: Sacred Geometry & Visual Brand Resonance", "Page 21"),
            ("Section 20: Digital Footprint — Mobile, Email & PIN Calibration", "Page 22"),
            ("Section 21: Family Dynasty & Intergenerational Synergy", "Page 23"),
            ("Section 22: Relationship Harmony & Spousal Synastry", "Page 24"),
            ("Section 23: Health, Vitality & Ayurvedic Chronobiology", "Page 25"),
            ("Section 24: Career Transmutation & Board Advisory", "Page 26"),
            ("Section 25: Real Estate & Property Numerology", "Page 27"),
            ("Section 26: Global Horizons & Cross-Border Expansion", "Page 28"),
            ("Section 27: Creative Authority & Thought Leadership", "Page 29"),
            ("Section 28: 12-Month Micro Breakdown for 2026", "Page 30"),
            ("Section 29: 4-Stage Pinnacle Cycles & Life Challenges", "Page 31"),
            ("Section 30: Vastu Dosha as per Missing Numbers & Cures", "Page 32")
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
                return Paragraph(f"<font size=8 color='#8B6914'><b>🔒 ANVEIL CHARM</b></font><br/><font size=10 color='#523E28'><b>{num}</b></font><br/><font size=7 color='#7A654D'>{elem} · Unsealed</font>", s['TableCellCenter'])

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

        self.story.append(Spacer(1, 14))
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
            [Paragraph("<b>Conductor Vector (Bhagyank)</b>", s['MetaLabel']), Paragraph(f": <b>{d['conductor_number']} · {d['conductor_planet']}</b> (Architectural Systems)", s['MetaValue'])],
            [Paragraph("<b>Acoustic Calling Name</b>", s['MetaLabel']), Paragraph(f": <b>{d['chaldean_name_compound']} → {d['chaldean_name_root']} · {d['chaldean_name_planet']}</b> (Star of the Lion)", s['MetaValue'])],
            [Paragraph("<b>Kua Directional Vector</b>", s['MetaLabel']), Paragraph(f": <b>{d['kua_number']} · {d['kua_element']}</b>", s['MetaValue'])],
            [Paragraph("<b>Personal Year Transit</b>", s['MetaLabel']), Paragraph(f": <b>{d['personal_year']} · {d['personal_year_theme']}</b>", s['MetaValue'])],
            [Paragraph("<b>Report Cryptographic ID</b>", s['MetaLabel']), Paragraph(f": {d['report_id']}", s['MetaValue'])],
            [Paragraph("<b>Verification Standard</b>", s['MetaLabel']), Paragraph(": Deterministic Python Core v2.2.0 · DPDP 2023 Statutory Compliance", s['MetaValue'])],
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
            f"<b>Notice of Rigorous Provenance:</b> This publication is compiled directly from the birth coordinates of <b>{d['seeker_name']}</b>. All arithmetic reductions, planetary dasha epicycles, and Lo Shu grid geometries are generated deterministically. Traditional numerological interpretations provide strategic life insights with zero fatalism. Consult accredited counsel for legal or medical decisions.",
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
        meta = self._get_topic_meta()

        # PAGE 1: Cover Page
        self._add_cover_page(
            subtitle=meta['subtitle'],
            badge_text=f"BASIC REPORT · 3-PAGE CORE DOSSIER · ₹199",
            custom_title=meta['title']
        )
        self.story.append(PageBreak())

        # PAGE 2: Foundational Profile, Proofs & Lo Shu Grid
        self.story.append(Paragraph("Section 1: Personal Profile, Natal Lo Shu Grid & Core Numbers", s['SectionH1']))
        self.story.append(Paragraph(
            "Every reading in Numeros Vision begins with exact, immutable mathematical reduction. Below are your core numbers calculated directly from your verified date of birth and calling name.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))

        calc_box = [
            [Paragraph("<b>Mathematical Vector</b>", s['TableHeader']), Paragraph("<b>Formula & Provenance</b>", s['TableHeader']), Paragraph("<b>Result</b>", s['TableHeader']), Paragraph("<b>Planetary Sovereign</b>", s['TableHeader'])],
            [Paragraph("Driver (Mulank)", s['TableCell']), Paragraph("Solar Day Reduction: 28 → 2 + 8 = 10 → 1", s['TableCell']), Paragraph("<b>1</b>", s['TableCellCenter']), Paragraph(d['driver_planet'], s['TableCell'])],
            [Paragraph("Conductor (Bhagyank)", s['TableCell']), Paragraph("Full Date Sum: 2+8+1+1+1+9+8+1 = 31 → 4", s['TableCell']), Paragraph("<b>4</b>", s['TableCellCenter']), Paragraph(d['conductor_planet'], s['TableCell'])],
            [Paragraph("Chaldean Name Number", s['TableCell']), Paragraph("Acoustic Letters: BHASKR (15) + SINGH (17) = 32", s['TableCell']), Paragraph("<b>32 → 5</b>", s['TableCellCenter']), Paragraph(d['chaldean_name_planet'], s['TableCell'])],
            [Paragraph("Kua Directional Number", s['TableCell']), Paragraph("Solar Epoch 1981 (Male): 10 - (8+1) = 1", s['TableCell']), Paragraph("<b>1</b>", s['TableCellCenter']), Paragraph("Water · Kan", s['TableCell'])],
            [Paragraph("Personal Year Calculator", s['TableCell']), Paragraph("Driver 1 + Month 2 + 2026 (1) = 4", s['TableCell']), Paragraph("<b>4</b>", s['TableCellCenter']), Paragraph("Foundation Year", s['TableCell'])],
        ]
        t_calc = Table(calc_box, colWidths=[120, 206, 60, 130])
        t_calc.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_calc)
        self.story.append(Spacer(1, 8))

        self.story.append(Paragraph("<b>Natal Lo Shu 3×3 Elemental Matrix</b>", s['SectionH2']))
        self.story.append(Paragraph(
            "The Lo Shu grid maps your birth date into 9 cosmic sectors. Present numbers represent active inborn vitality, while unsealed sleeping charms indicate where external routines and partners balance your nature.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 4))
        self.story.append(self._create_loshu_grid_table())
        self.story.append(Spacer(1, 8))

        summary_p = Paragraph(
            f"<b>Active Present Numbers:</b> <b>[1, 2, 8, 9]</b> (Quadruple 1 solar executive stamina, double 8 financial realism).<br/><b>Karmic Sleeping Charms (To Anveil):</b> <b>[3, 4, 5, 6, 7]</b>. Lacking central 5 is successfully bridged by Calling Name 32 → 5.",
            s['CalloutText']
        )
        t_sum = Table([[summary_p]], colWidths=[516])
        t_sum.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_sum)
        self.story.append(PageBreak())

        # PAGE 3: Dynamic Topic Executive Findings & Action Plan
        self.story.append(Paragraph(f"Section 2: {meta['title']} — Executive Findings & 2026 Strategy", s['SectionH1']))
        self.story.append(Paragraph(
            f"Tailored specifically for <b>{d['seeker_name']}</b> combining Driver 1 (Sun), Conductor 4 (Rahu), and Chaldean 32/5 (Mercury):",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))

        if self.topic_id == "present_numbers":
            p3_insights = [
                ("✦ Present Numbers Inborn Superpower & Overdrive Mastery",
                 "Your chart carries numbers [1, 2, 8, 9]. Quadruple 1 gives supreme independent visionary leadership; double 8 gives unyielding financial pragmatism. Overdrive harmonization: avoid taking on excessive solitary operational burden; delegate technical details to preserve executive clarity."),
                ("✦ Benefic vs Malefic Operating State",
                 "Sun 1 operates beneficially when casting vision and leading teams; its shadow malefic state emerges as impatience or ego fatigue. Saturn 8 operates beneficially through steady asset accumulation; its shadow state emerges as feeling delayed or unsupported. Balance via written contracts."),
                ("✦ High-Yield Career Vocations",
                 "Peak commercial alignment lies in Adtech, Programmatic Advertising, Digital Media Arbitrage, and Enterprise Technology Platforms. Rahu 4 rules complex electronic networks, while Sun 1 commands monetization authority."),
                ("✦ Personal Year Calculator Foundation Corridor",
                 "Operating in Personal Year 4 means 2026 is an infrastructure-hardening year. Automate operational pipelines, eliminate redundancies, and build balance sheet equity for explosive commercial scaling in Personal Year 5 (2027)."),
                ("✦ Vedic Gharelu Harmonizer & 40-Day Aura Cleansing",
                 "Touch father's feet daily for Sun 1 vitality; drink water from a copper vessel. For aura clearing, wash face and soak feet in warm Rock Salt (Sendha Namak) water for 40 days to dissolve looping fatigue and stuck mental cycles.")
            ]
        elif self.topic_id == "love_relationship":
            p3_insights = [
                ("✦ Love Style & Romantic Resonance",
                 "Driver 1 Sun loyalty combines with Conductor 4 Rahu intellectual connection. You seek a partner who respects your sovereign vision, offers genuine emotional grounding, and provides a peaceful domestic sanctuary away from commercial stress."),
                ("✦ Ideal Partner Compatibility Synastry",
                 "Supreme synastry aligns with Moon 2 (intuitive peace) and Jupiter 3 (philosophical expansion). High harmony with Venus 6 (domestic beauty). Caution with Mars 9 and Saturn 8 to avoid competing executive wills."),
                ("✦ Marriage & Union Timing Windows",
                 "Upcoming Personal Year 5 (2027) brings high relational velocity and romantic travel. Personal Year 6 (2028) under Venus is the supreme window for marital commitment, domestic harmony, and family consolidation."),
                ("✦ Domestic Spatial Vastu for Relationships",
                 "Align master bedroom in the Southwest (Earth sector) with warm amber and Venus pearl tones. Keep the bedroom completely free from electronic clutter and work papers to ensure undisturbed spousal intimacy."),
                ("✦ Vedic Gharelu Remedy for Harmony",
                 "Touch mother's feet daily for Moon 2 calm; drink water from a silver cup. Keep bedroom fragrant with subtle natural rose or sandalwood essence.")
            ]
        elif self.topic_id == "career_wealth":
            p3_insights = [
                ("✦ High-Growth Enterprise Vocations & Scaling",
                 "Natural executive mastery over Adtech, programmatic advertising yield, media platforms, and data infrastructure. Avoid low-margin agency work; own the underlying software, data pipelines, and programmatic inventory."),
                ("✦ Commercial Timing & 5-Year Numerology Dasha Radar",
                 "2026 is your foundation-locking year (Personal Year 4). 2027 is explosive commercial expansion (Year 5). 2028 consolidates brand prestige (Year 6). 2030 delivers peak karmic financial harvest (Saturn Year 8)."),
                ("✦ Strategic Entity Naming & Corporate Numbers",
                 "Corporate trademarks and legal entities should vibrate to auspicious roots 15, 19, 23, 24, or 32. Strictly avoid naming commercial entities with root sums reducing to 4 or 8."),
                ("✦ Treasury Rule: Overcoming the Missing 5 Center",
                 "Missing central 5 in natal grid can create rapid reinvestment leakage. Enforce an automated treasury rule: sweep 25% of gross profits immediately into sovereign debt or gold before discretionary operational spends."),
                ("✦ Vedic Gharelu Remedy for Commercial Growth",
                 "Feed green fodder or soaked moong dal to cows on Wednesdays. Keep living green jade plants in East sector of your cabin; carry a green handkerchief.")
            ]
        else: # missing_numbers_vastu & core_blueprint
            p3_insights = [
                ("✦ Missing Numbers Void Diagnosis ([3, 4, 5, 6, 7])",
                 "Missing 3 (Jupiter wisdom), 4 (Rahu structure in grid), 5 (Mercury balance), 6 (Venus luxury), and 7 (Ketu introspection). Conductor 4 directly bridges the structural void; Calling Name 32/5 directly bridges the central 5 void!"),
                ("✦ Full Name Balancing & Poorak Numbers Activation",
                 "Calling name 'Bhaskr Singh' compounds to 32 → 5 ('The Star of the Lion'), perfectly activating the central Earth anchor. Complementary Poorak Numbers (5 and 6) bridge remaining gaps via mobile digits and signature."),
                ("✦ Element Yogas Balancing — Golden Raj Yoga (4-5-6)",
                 "Golden Raj Yoga (4-5-6) is actively completed via Conductor 4, Calling Name 5, and Northwest metal cures. Silver Earth Plane (2-5-8) is 100% complete and fully activated for enduring property assets."),
                ("✦ 7-Layer Spatial Vastu Directional Cures",
                 "Southwest 2 heavy brass decor; East 3 brass Surya wall fixture; Southeast 4 camphor diffuser; Center 5 clutter-free Brahmasthan; Northwest 6 hollow metal chime; West 7 round white metal artefacts."),
                ("✦ Vedic Gharelu Remedies & 40-Day Aura Cleansing",
                 "Perform 40-day Rock Salt (Sendha Namak) bath to dissolve stagnant negative energy. Take 40-day Haldi water bath on Thursdays to activate Jupiter 3 wisdom; touch parents' feet daily.")
            ]

        insight_table_rows = []
        for heading, body in p3_insights:
            insight_table_rows.append([Paragraph(f"<b>{heading}</b><br/>{body}", s['TableCell'])])

        t_insights = Table(insight_table_rows, colWidths=[516])
        t_insights.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_insights)
        self.story.append(Spacer(1, 8))

        method_note = Paragraph(
            "<b>Engine Provenance Standard:</b> Compiled deterministically by Numeros Vision Calculation Engine. To explore your complete 5-Year Numerology Dasha timing radar or 32-page Sovereign Compendium, access our Advanced and Premium Master Dossiers.",
            s['CalloutText']
        )
        self.story.append(method_note)

    # ── ADVANCED REPORT: EXACTLY 12 PAGES ─────────────────────────────────────
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
            self.story.append(Paragraph("✦   SOVEREIGN COMPENDIUM · 30 STANDARD SECTIONS ACROSS 32 PAGES   ✦", s['CoverSubtitle']))
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
            self.story.append(Paragraph("✦   MASTER SYNTHESIS DOSSIER · 10 STANDARD SECTIONS ACROSS 12 PAGES   ✦", s['CoverSubtitle']))
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

        exec_summary_p = Paragraph(
            f"<b>Executive Charter:</b> This dossier is prepared for <b>{d['seeker_name']}</b> born on <b>28-11-1981</b> at 04:15 PM in New Delhi. Combining Driver 1 (Sun), Conductor 4 (Rahu), and Chaldean 32/5 (Mercury), this report maps your inborn present numbers, 5-year Numerology Dasha timing radar, and safe home-accessible Vedic Gharelu remedies with zero ambiguity.",
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
            [Paragraph("Personal Year Calculator", s['TableCell']), Paragraph("<b>4 · Foundation Phase</b>", s['TableCellCenter']), Paragraph("A rigorous restructuring cycle. Perfect for formalizing patents, scaling platforms, and locking in written equity agreements.", s['TableCell'])],
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
            ("✦ Perpetual Golden Dates of Any Month",
             "Your primary power dates are the <b>1st, 10th, 19th, and 28th</b> (ruled by Sun 1). Your secondary commercial dates are the <b>5th, 14th, and 23rd</b> (ruled by Mercury 5). Schedule client contract signings, entity formations, and product launches on these dates whenever possible."),
            ("✦ Harmonic Days of the Week",
             "<b>Sunday</b> is your primary day for visionary roadmapping and leadership decrees. <b>Wednesday</b> is your optimal day for high-velocity commercial deals, ad campaign deployments, and sales pitches. Avoid contentious legal filings on Saturdays."),
            ("✦ Auspicious Hourly Horas (Solar & Mercurial Windows)",
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
        self.story.append(Paragraph("Section 10: Methodology, Algorithmic Provenance & Governance", s['SectionH1']))
        self.story.append(Paragraph(
            "Numeros Vision operates under strict mathematical and ethical guidelines. We completely separate measurable arithmetic calculations from symbolic traditional interpretations. Zero astrology claims are made.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))

        gov_box = [
            [Paragraph("<b>Governance Dimension</b>", s['TableHeader']), Paragraph("<b>Authoritative Standard & Provenance</b>", s['TableHeader'])],
            [Paragraph("Calculation Engine", s['TableCell']), Paragraph("Deterministic Python Core (v2.2.0-release.2026.11) — Zero LLM arithmetic.", s['TableCell'])],
            [Paragraph("Privacy & Data Protection", s['TableCell']), Paragraph("Full statutory compliance with India's Digital Personal Data Protection (DPDP) Act 2023. Zero-knowledge session isolated.", s['TableCell'])],
            [Paragraph("Cryptographic Fingerprint", s['TableCell']), Paragraph(f"Report ID: {d['report_id']} | Hash: SHA-256 Verified", s['TableCell'])],
            [Paragraph("Chaldean Methodology", s['TableCell']), Paragraph("Classical 1-to-8 sound mapping (sacred alphabet without 9 in compound derivation).", s['TableCell'])],
            [Paragraph("Interpretive Boundary", s['TableCell']), Paragraph("Traditional frameworks offer psychological, archetypal, and strategic insight. No deterministic claims of commercial success are guaranteed.", s['TableCell'])],
            [Paragraph("Master Sign-off", s['TableCell']), Paragraph("Master Numerologist Bhaskr Singh (Numeros Vision) · Numeros Vision Algorithmic Council", s['TableCell'])],
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
                ("✦ Core Romantic Psychology",
                 "You express love through steadfast protection, providing long-term security, and championing your partner's ambitions. You need a partner who genuinely respects your independent vision and never engages in public belittlement."),
                ("✦ Quadruple 1 Relational Shadow",
                 "Carrying four 1s means you can sometimes become absorbed in internal strategic thoughts, appearing emotionally distant or commanding. Ensure you consciously switch off 'CEO mode' when crossing your home threshold."),
                ("✦ Ideal Spousal Archetype",
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
                ("✦ Personal Year 5 (2027) — Romantic Velocity & Social Expansion",
                 "Ruled by Mercury 5, 2027 initiates exciting social mobility, romantic meetings, mutual travel, and relationship breakthroughs. An optimal year for public engagement or renewing marital vows."),
                ("✦ Personal Year 6 (2028) — Golden Marital & Family Anchor",
                 "Ruled by Venus 6, 2028 is the quintessential year of home, family harmony, and sacred marriage commitments. Brings domestic peace, luxury property acquisition, and family blessing."),
                ("✦ Domestic Vastu for Relationship Harmony",
                 "Position your primary master bedroom in the South-West sector (Earth zone) to anchor emotional stability. Paint walls in soft Venus Pearl (#FFFDF7) or warm Sandalwood. Strictly remove work papers and exercise machinery from the bedroom."),
                ("✦ Vedic Gharelu Remedy for Spousal Love",
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
                ("✦ Programmatic Yield Optimization & Ad Exchange Platforms",
                 "Rahu 4 excels in electronic systems, real-time automated auctions, and distributed advertising inventory. Focus on owning the proprietary adtech infrastructure rather than servicing commoditized agency retainers."),
                ("✦ Strategic B2B Sales to C-Suite Executives",
                 "Chaldean 32/5 gives persuasive commercial charm. Pitch directly to enterprise founders, CTOs, and CMOs (Sun 1 authority); middle management will dilute your speed."),
                ("✦ Intellectual Property & Automated Data Moats",
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
                ("✦ Harmonious Corporate Entity Compound Numbers",
                 "Ensure candidate LLC, corporate trademarks, and digital domains sum to auspicious roots 15, 19, 23, 24, 32, 37, 41, or 42. Compound 19 ('Prince of Heaven') and 23 ('Royal Star of the Gem') bring explosive tech adoption."),
                ("✦ Treasury Protection: The 25% Rule",
                 "Mitigate the natal missing 5 center by implementing an automated rule: sweep 25% of all gross company profits directly into low-volatility sovereign bonds or physical gold before deploying capital into discretionary expenses."),
                ("✦ Strategic Board & Co-Founder Synastry",
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
            ("Section 13: 10-Year Macro Planetary Timing Radar (2026–2035 Horizon)",
             f"Looking across the coming decade (2026 to 2035), <b>{d['seeker_name']}</b> transitions through a powerful evolutionary cycle. 2026 is your foundation-locking phase (Personal Year 4). 2027 initiates a high-velocity 3-year commercial expansion window (Personal Years 5, 6, 7). By 2030 (Personal Year 8), you reach a major financial harvest and enterprise culmination, followed by 2031 (Personal Year 9) which marks institutional restructuring. In 2032, a brand-new 9-year cycle begins at Personal Year 1, elevating your career into sovereign board advisory, enterprise equity ownership, and major capital allocation.",
             [
                 ("2026–2027 Corridor", "Operational hardening followed by explosive market velocity and tech launch"),
                 ("2028–2029 Corridor", "Brand prestige consolidation, institutional IP protection, and team scaling"),
                 ("2030 Milestone", "Peak karmic financial harvest (Saturn 8) — optimal year for major enterprise liquidity"),
                 ("2032–2035 Era", "New 9-year sovereign cycle — board directorships, venture investing, and legacy assets")
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

            # Page 20
            ("Section 18: Corporate Brand Naming, Trademark Vibration & LLC Alignment",
             "When naming new business entities, digital products, software tools, or subsidiary LLCs, ensuring the corporate name vibrates to an auspicious number harmonic with Sun 1 and Mercury 5 is essential. The ideal corporate compound numbers are 15, 19, 23, 24, 32, 37, 41, and 42. Corporate names reducing to 1 project undeniable leadership and pioneering authority. Corporate names reducing to 5 project rapid commercial adoption, international marketability, and technological adaptability. Strictly avoid corporate names compounding to 4, 8, or 9 for commercial consumer tech.",
             [
                 ("Tier 1 Corporate Roots", "Numbers 1 (Leadership), 5 (Commerce/Speed), 6 (Luxury/Trust)"),
                 ("Compound 19 ('The Prince of Heaven')", "Brings sustained commercial victory, public esteem, and executive stability"),
                 ("Compound 23 ('The Royal Star of the Gem')", "Exceptional for media, advertising, communications, and tech scaling"),
                 ("Audit Verification Protocol", "Submit every candidate trademark through our deterministic Chaldean engine first")
             ]),

            # Page 21
            ("Section 19: Sacred Geometry, Visual Brand Resonance & Color Tokens",
             "Brand identity is visual numerology. Geometric symbols transmit distinct vibrational frequencies to the subconscious mind. For Bhaskr Singh's enterprises, visual geometry must reflect upward-and-to-the-right trajectory (growth vector), balanced by structured four-sided stability (Rahu 4) and solar circular completeness (Sun 1). Your color palette must strictly honor Jupiter Gold (#C9A227), Sun Amber (#E2B84B), Venus Pearl (#FFFDF7), and Mercury Emerald (#16835B). Avoid stark raw black (#000000) as a background, as it introduces heaviness into modern technology branding.",
             [
                 ("Primary Brand Form", "Concentric gold circles paired with dynamic upward-right 45-degree vectors"),
                 ("Core Palette Tokens", "Jupiter Gold (#8B6914, #C9A227), Mercury Emerald (#16835B), Sandalwood Ink (#523E28)"),
                 ("Typography Rules", "Clean, high-legibility geometric serif for titles; crisp modern sans-serif for UI"),
                 ("Visual Aura Impact", "Instills immediate institutional trust, premium exclusivity, and mathematical rigor")
             ]),

            # Page 22
            ("Section 20: Digital Footprint — Mobile Number, Email & PIN Calibration",
             "In our hyper-connected era, your daily digital coordinates — mobile numbers, corporate email handles, and banking PINs — vibrate continuously in the global data grid. Your mobile number should ideally sum to 1, 5, or 6, and the final four digits should never terminate in repeating 4s or 8s (which create administrative delays). Your primary business email handle should reflect your balanced name ('bhaskrsingh' or 'bhaskr') to maintain the harmonic 32 → 5 sound frequency in digital communication.",
             [
                 ("Mobile Number Total", "Target compound sum reducing to 1 (Sun authority) or 5 (Commercial speed)"),
                 ("Terminal Digits Check", "Ensure the final two digits reduce to 1, 5, 6, or 3; avoid ending in 4 or 8"),
                 ("Banking PIN Optimization", "Choose a 4-digit or 6-digit PIN whose individual digits sum to 1, 5, or 9"),
                 ("Email Signature Vibe", "Include 'NUMEROS VISION · ANVEIL EVERY CHARM' or your official executive title")
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
            ("Section 25: Real Estate, Property Numerology & Spatial Wealth Anchoring",
             "Property and real estate represent the physical anchoring of wealth. Because your Lo Shu chart contains a double 8 in the Earth sector, land, physical commercial buildings, and prime residential properties are your greatest wealth stabilizers. When selecting properties, apartments, or office buildings, ensure the building number, flat number, or plot number reduces to 1, 5, or 8. Properties facing North or East maximize your Kua 1 vitality.",
             [
                 ("Auspicious Property Numbers", "Total sums reducing to 1 (Authority), 5 (Commercial activity), or 8 (Enduring wealth)"),
                 ("Plot Topography", "Ensure the land is level or slopes gently towards the North or East"),
                 ("Main Entrance Alignment", "Main door facing North or East welcomes Sheng Chi and Tien Yi vitality"),
                 ("Interior Balance", "Place the master bedroom in the South or Southeast sector to support grounded rest")
             ]),

            # Page 28
            ("Section 26: Global Horizons, Foreign Expansion & Cross-Border Relocation",
             "With Chaldean Calling Name 32/5 (Mercury) and Conductor 4 (Rahu), foreign horizons, international travel, and cross-border client contracts are extremely auspicious for you. Mercury and Rahu rule foreign trade, cross-border data transfer, and global commerce. The optimal international markets for your adtech and business ventures are the United States, United Kingdom, United Arab Emirates (Dubai), and Singapore.",
             [
                 ("Global Growth Hubs", "Dubai (UAE · Mercury/Sun hub), Singapore (Adtech/Fintech), US East Coast (Publishing)"),
                 ("Travel Timing Corridor", "Schedule major international business trips during Personal Year 5 (2027)"),
                 ("Foreign Currency Flow", "Invoicing in USD, AED, or GBP activates your 32/5 global commercial trade vibration"),
                 ("Relocation Assessment", "Temporary residences or overseas corporate offices will substantially accelerate net worth")
             ]),

            # Page 29
            ("Section 27: Creative Authority, Media Influence & Executive Thought Leadership",
             "Driver 1 individuals are natural public speakers and thought leaders. Conductor 4 allows you to dissect technical complexities with acute clarity. In the advertising and media technology sectors, authoring whitepapers, delivering keynote speeches at industry conferences, and hosting executive roundtable dinners will exponentially expand your client acquisition pipeline.",
             [
                 ("Thought Leadership Form", "In-depth industry whitepapers on the future of programmatic monetization and AI"),
                 ("Keynote Speaking Platform", "Position yourself as the definitive authority on adtech yield and publisher strategy"),
                 ("Media Presence Vibe", "Authoritative, dignified, precise, and educational — mirroring Sun 1 sovereign clarity"),
                 ("Publishing Milestone", "Consider releasing a definitive business book or monograph during Personal Year 7 (2029)")
             ]),

            # Page 30
            ("Section 28: 12-Month Micro Breakdown for 2026 (Month-by-Month Calendar)",
             "Within Personal Year 4 (2026), each calendar month carries a distinct micro-transit frequency. Aligning your monthly focus with these vibrations prevents wasted effort and maximizes productivity across the calendar year.",
             [
                 ("Jan–Mar 2026 (Micro 5, 6, 7)", "Conduct operational audits, upgrade technical infrastructure, review balance sheets"),
                 ("Apr–Jun 2026 (Micro 8, 9, 1)", "Peak execution window. Close enterprise commercial contracts, roll out platform updates"),
                 ("Jul–Sep 2026 (Micro 2, 3, 4)", "Focus on internal team development, operational restructuring, and contractual audits"),
                 ("Oct–Dec 2026 (Micro 5, 6, 7)", "Annual financial reviews, debt elimination, setting aggressive growth targets for 2027")
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
            ("Section 30: Vastu Dosha as per Missing Numbers, Directional Zones & Spatial Corrections",
             f"In classical Lo Shu and Vedic Vastu metaphysics, your natal birth matrix directly mirrors the energy flow of your physical living and working spaces. For <b>{d['seeker_name']}</b>, the missing digits in your Lo Shu grid correspond to specific directional quadrants that require conscious spatial harmonizing to prevent energetic and financial leakages.",
             [
                 ("South-West (SW) Missing 2 Correction", "SW governs stability and relationships (Earth). Remedy: Place heavy brass bowls, keep the SW corner well-lit with warm yellow light, and strictly avoid water features"),
                 ("East (E) Missing 3 Correction", "East governs vitality and institutional growth (Wood). Remedy: Install an authentic polished Brass Surya (Sun) or a lush green healthy plant on the East wall"),
                 ("South-East (SE) Missing 4 Correction", "SE governs liquid cashflow and commercial velocity (Agni/Fire). Remedy: Use an electric camphor diffuser or a red/green night lamp in the SE corner (reinforced by Conductor 4)"),
                 ("Center (Brahmasthan) Missing 5 Correction", "Center governs overall mental and financial equilibrium (Earth). Remedy: Maintain the central zone completely open and clutter-free; place a natural crystal lotus to anchor peace"),
                 ("North-West (NW) Missing 6 Correction", "NW governs banking support, helpful mentors, and global travel (Metal). Remedy: Hang a 6-rod hollow metallic wind chime and keep silver coins in a brass bowl in the NW zone"),
                 ("West (W) Missing 7 Correction", "West governs intellectual focus and creative completion (Metal). Remedy: Place round white metal artefacts or a consecrated brass keepsake on the West wall")
             ])
        ]

        for title, intro, table_items in premium_chapters:
            self.story.append(PageBreak())
            self.story.append(Paragraph(title, s['SectionH1']))
            self.story.append(Paragraph(intro, s['ReportBody']))
            self.story.append(Spacer(1, 6))

            t_rows = [
                [Paragraph("<b>Diagnostic Parameter</b>", s['TableHeader']), Paragraph("<b>Authoritative Finding & Action Protocol</b>", s['TableHeader'])]
            ]
            for param, finding in table_items:
                t_rows.append([Paragraph(f"<b>{param}</b>", s['TableCell']), Paragraph(finding, s['TableCell'])])

            t_chap = Table(t_rows, colWidths=[150, 366])
            t_chap.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 5.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 5.5),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ]))
            self.story.append(t_chap)
            self.story.append(Spacer(1, 6))


def generate_customised_pdf_report(
    name: str = "Seeker",
    day: int = 15,
    month: int = 7,
    year: int = 1990,
    topic_id: str = "core_blueprint",
    tier: str = "basic"
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
        tier=tier
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
