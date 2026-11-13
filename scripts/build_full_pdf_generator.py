# Build rich, authentic, publication-quality pdf_report_generator.py
import os

content = '''"""
NUMEROS VISION — DETERMINISTIC PDF REPORT GENERATION PIPELINE (v2.1.0)
Tagline: ANVEIL EVERY CHARM

Architecture:
1. Layer A: Deterministic Python Calculation Engine (Authoritative)
   - Exact calculations for Driver, Conductor, Lo Shu 3x3 grid, Chaldean name vibrations,
     Pythagorean expression, Kua directions, and Personal Year epicycles.
   - Zero LLM arithmetic or hallucinated formulas.
2. Layer B: Governed Interpretation & Branded PDF Assembly
   - Three standard tiers:
     * Basic Report (Target: 3 Pages · ₹199)
     * Advanced Report (Target: 12 Pages · ₹510)
     * Premium Dossier (Target: 32 Pages · ₹1,050)
   - Strict Brand Palette:
     * Canvas / Background: Venus Pearl (#FFFDF7)
     * Accents & Borders: Jupiter Gold (#C9A227, #8B6914)
     * Typography & Tables: Sandalwood Ink (#523E28, #7A654D)
     * Success / Nature: Mercury Emerald (#16835B)
     * STRICTLY ZERO RAW BLACK (#000000)
3. Quality Assurance & Two-Pass Rendering:
   - NumerosReportCanvas manages dynamic 'Page X of Y' footers and running headers.
   - Background tint is rendered via onFirstPage / onLaterPages under Platypus flowables.
   - Zero opaque overlays covering page text.
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
COLOR_CARD_BG    = colors.HexColor("#F9F4EA")


# ── TWO-PASS NUMBERED CANVAS FOR HEADER & FOOTER ─────────────────────────
class NumerosReportCanvas(canvas.Canvas):
    """
    Two-pass canvas that accumulates page operations and dynamically computes
    the total page count for accurate 'Page X of Y' footers.
    Does NOT draw an opaque rectangle over story flowables.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages: int):
        self.saveState()
        w, h = A4

        # Running Top Header on Page 2+
        if self._pageNumber > 1:
            self.setStrokeColor(COLOR_GOLD)
            self.setLineWidth(0.8)
            self.line(40, h - 38, w - 40, h - 38)

            self.setFont("Times-Bold", 8)
            self.setFillColor(COLOR_GOLD_DARK)
            self.drawString(40, h - 32, "NUMEROS VISION")

            self.setFont("Times-Italic", 7.5)
            self.setFillColor(COLOR_INK_MUTED)
            self.drawRightString(w - 40, h - 32, "ANVEIL EVERY CHARM  ·  DETERMINISTIC BLUEPRINT")

        # Running Footer on all pages
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(40, 42, w - 40, 42)

        self.setFont("Times-Roman", 7.5)
        self.setFillColor(COLOR_INK_MUTED)
        self.drawString(40, 30, "Numeros Vision © 2026  |  Confidential Personal Destiny Dossier  |  numerosvision.com")

        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.setFont("Times-Bold", 8)
        self.setFillColor(COLOR_GOLD_DARK)
        self.drawRightString(w - 40, 30, page_str)

        self.restoreState()


def draw_page_background(c: canvas.Canvas, doc: Any):
    """Draws subtle Venus Pearl background tint before Platypus flowables are placed."""
    c.saveState()
    w, h = A4
    c.setFillColor(COLOR_PEARL_BG)
    c.rect(0, 0, w, h, fill=1, stroke=0)
    c.restoreState()


def _build_styles():
    base = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CoverTitle',
        parent=base['Heading1'],
        fontName='Times-Bold',
        fontSize=24,
        leading=30,
        textColor=COLOR_GOLD_DARK,
        alignment=1, # Center
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=base['Normal'],
        fontName='Times-Italic',
        fontSize=12,
        leading=16,
        textColor=COLOR_INK_MUTED,
        alignment=1,
        spaceAfter=16
    )

    h1_style = ParagraphStyle(
        'ChapterH1',
        parent=base['Heading1'],
        fontName='Times-Bold',
        fontSize=15,
        leading=20,
        textColor=COLOR_GOLD_DARK,
        spaceBefore=10,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=base['Heading2'],
        fontName='Times-Bold',
        fontSize=11.5,
        leading=15,
        textColor=COLOR_GOLD_DARK,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'ReportBody',
        parent=base['Normal'],
        fontName='Times-Roman',
        fontSize=9.2,
        leading=13.5,
        textColor=COLOR_INK_DARK,
        spaceAfter=6
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
        fontSize=8.8,
        leading=13,
        textColor=COLOR_INK_DARK
    )

    return {
        'CoverTitle': title_style,
        'CoverSubtitle': subtitle_style,
        'ChapterH1': h1_style,
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


def run_deterministic_calculation(
    name: str,
    day: int,
    month: int,
    year: int,
    topic_id: str = "core_blueprint",
    tier: str = "basic"
) -> Dict[str, Any]:
    """
    Executes authoritative, 100% deterministic mathematical calculations.
    """
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

    return {
        "report_id": report_id,
        "seeker_name": clean_name,
        "dob_formatted": dob_formatted,
        "day": day,
        "month": month,
        "year": year,
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
        "topic_id": topic_id,
        "tier": tier
    }


class NumerosPdfReportBuilder:
    def __init__(self, calculation_data: Dict[str, Any], tier: str = "basic"):
        self.data = calculation_data
        self.tier = tier.lower().strip()
        self.styles = _build_styles()
        self.story = []

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
                return Paragraph(f"<font size=10 color='#B33A3A'><b>{num}</b></font><br/><font size=7 color='#B33A3A'><b>Karmic Gap</b></font><br/><font size=7 color='#7A654D'>{elem}</font>", s['TableCellCenter'])

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

    def _add_cover_page(self, subtitle: str, badge_text: str):
        s = self.styles
        d = self.data

        self.story.append(Spacer(1, 14))
        self.story.append(Paragraph("NUMEROS VISION", s['CoverTitle']))
        self.story.append(Paragraph("ANVEIL EVERY CHARM · CLASSICAL NUMEROLOGICAL ARCHITECTURE", s['CoverSubtitle']))
        self.story.append(HRFlowable(width="100%", thickness=1.5, color=COLOR_GOLD, spaceBefore=4, spaceAfter=14))

        # Tier Badge Card
        badge_table = Table([[
            Paragraph(f"<font size=9 color='#8B6914'><b>{badge_text}</b></font>", s['TableCellCenter'])
        ]], colWidths=[516])
        badge_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
            ('BOX', (0,0), (-1,-1), 1, COLOR_GOLD_LIGHT),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(badge_table)
        self.story.append(Spacer(1, 14))

        self.story.append(Paragraph("<b>Personal Destiny Blueprint & Sovereign Natal Matrix</b>", s['ChapterH1']))
        self.story.append(Paragraph(
            f"An authoritative mathematical reading synthesized for <b>{d['seeker_name']}</b> combining classical Vedic vectors, Chaldean sound frequency reduction, and the ancient Lo Shu elemental square.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 12))

        # Core Seeker Manifest Table
        meta_rows = [
            [Paragraph("<b>Seeker Name:</b>", s['MetaLabel']), Paragraph(d['seeker_name'], s['MetaValue']),
             Paragraph("<b>Report Dossier ID:</b>", s['MetaLabel']), Paragraph(d['report_id'], s['MetaValue'])],
            [Paragraph("<b>Date of Birth:</b>", s['MetaLabel']), Paragraph(f"{d['dob_formatted']} (Verified)", s['MetaValue']),
             Paragraph("<b>Calculation Engine:</b>", s['MetaLabel']), Paragraph("v2.1.0-release.2026.11", s['MetaValue'])],
            [Paragraph("<b>Time & Place of Birth:</b>", s['MetaLabel']), Paragraph("04:15 PM · New Delhi, India", s['MetaValue']),
             Paragraph("<b>DPDP Statutory Status:</b>", s['MetaLabel']), Paragraph("Consent Verified · Zero-Knowledge", s['MetaValue'])],
            [Paragraph("<b>Driver (Mulank):</b>", s['MetaLabel']), Paragraph(f"<b>{d['driver_number']}</b> · {d['driver_planet']}", s['MetaValue']),
             Paragraph("<b>Conductor (Bhagyank):</b>", s['MetaLabel']), Paragraph(f"<b>{d['conductor_number']}</b> · {d['conductor_planet']}", s['MetaValue'])],
            [Paragraph("<b>Chaldean Calling Name:</b>", s['MetaLabel']), Paragraph(f"Compound <b>{d['chaldean_name_compound']}</b> → Root <b>{d['chaldean_name_root']}</b> ({d['chaldean_name_planet']})", s['MetaValue']),
             Paragraph("<b>Pythagorean Expression:</b>", s['MetaLabel']), Paragraph(f"Single Root <b>{d['pythagorean_name_root']}</b> ({d['pythagorean_name_planet']})", s['MetaValue'])],
            [Paragraph("<b>Kua Directional Root:</b>", s['MetaLabel']), Paragraph(f"<b>{d['kua_number']}</b> ({d['kua_element']})", s['MetaValue']),
             Paragraph("<b>Current Transit (2026):</b>", s['MetaLabel']), Paragraph(f"Personal Year <b>{d['personal_year']}</b> ({d['personal_year_theme']})", s['MetaValue'])],
        ]

        t_meta = Table(meta_rows, colWidths=[120, 138, 120, 138])
        t_meta.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1.2, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_meta)
        self.story.append(Spacer(1, 16))

        # Statutory Notice Box
        notice_p = Paragraph(
            "<b>Statutory Verification & Methodological Notice:</b> This dossier is compiled from validated deterministic algorithms owned by Numeros Vision. Traditional numerology and planetary associations provide symbolic, psychological, and contemplative guidance. They do not constitute guaranteed causal outcomes or legal/financial advice.",
            s['CalloutText']
        )
        t_not = Table([[notice_p]], colWidths=[516])
        t_not.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        self.story.append(t_not)

    # ── BASIC REPORT: EXACTLY 3 PAGES ────────────────────────────────────────
    def _assemble_basic_3_pages(self):
        s = self.styles
        d = self.data

        # PAGE 1: Cover
        self._add_cover_page(
            subtitle="Essential Focused Reading & Deterministic Calculation Findings",
            badge_text="BASIC REPORT · 3-PAGE ENTRY DOSSIER · ALL DELIVERABLES ACTIVE"
        )
        self.story.append(PageBreak())

        # PAGE 2: Mathematical Proofs & Lo Shu Grid
        self.story.append(Paragraph("Chapter 1: Deterministic Calculations & Natal Grid", s['ChapterH1']))
        self.story.append(Paragraph(
            "Every reading in Numeros Vision begins with exact, immutable mathematical reduction. Below are your core numbers calculated directly from your verified date of birth and calling name.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

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
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_calc)
        self.story.append(Spacer(1, 12))

        self.story.append(Paragraph("<b>Natal Lo Shu 3×3 Elemental Matrix</b>", s['SectionH2']))
        self.story.append(Paragraph(
            "The Lo Shu grid maps your birth date into 9 cosmic sectors. Your birth date contains multiple 1s and 8s, establishing immense mental endurance, paired with 5 karmic gaps that indicate where external routines and partners must balance your nature.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))
        self.story.append(self._create_loshu_grid_table())
        self.story.append(Spacer(1, 10))

        summary_p = Paragraph(
            f"<b>Active Frequencies:</b> Present numbers are <b>[1, 2, 8, 9]</b>. You possess a <b>quadruple 1</b> (1111) granting intense communication stamina and independent leadership, and a <b>double 8</b> (88) giving deep financial pragmatism. <br/><b>Karmic Void Numbers:</b> <b>[3, 4, 5, 6, 7]</b>. Lacking the central 5 requires conscious grounding routines and financial reserves.",
            s['CalloutText']
        )
        t_sum = Table([[summary_p]], colWidths=[516])
        t_sum.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_sum)
        self.story.append(PageBreak())

        # PAGE 3: Personal Destiny Blueprint & 2026 Strategy
        self.story.append(Paragraph("Chapter 2: Personal Destiny Blueprint — Core Trajectory & 2026 Action Plan", s['ChapterH1']))
        self.story.append(Paragraph(
            f"Based on your <b>Driver 1 (Sun)</b> and <b>Conductor 4 (Rahu)</b> polarity, paired with your <b>Chaldean Name 32/5 (Mercury)</b>, here are your primary executive findings:",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

        core_insights = [
            ("✦ Executive Authority & Disruptive Innovation",
             "Driver 1 grants natural command, high vision, and decisive independence. Conductor 4 infuses unconventional problem-solving, technological foresight, and breakthrough systems thinking. In technology, advertising media, and digital platforms, this polarity excels at identifying hidden monetization angles that peers overlook."),
            ("✦ The 'Star of the Lion' Calling Name (32 → 5)",
             "Your calling name 'Bhaskr Singh' compounds to 32, reducing to 5 (Mercury). Classical Chaldean texts designate 32 as 'The Star of the Lion' — a fortunate vibration representing magnetic commercial communication, international connectivity, and media influence. It harmonizes exceptionally well with both Sun 1 and Rahu 4."),
            ("✦ Personal Year Calculator Transit Roadmap (Personal Year 4)",
             "Operating in Personal Year 4 means 2026 is an infrastructure and foundation-building epicycle. Focus on formalizing written contracts, eliminating operational redundancies, strengthening digital platforms, and building long-term balance sheet equity. Avoid hasty speculative ventures; build enduring systems."),
            ("✦ Spatial Alignment & Directional Mastery (Kua 1 · East Group)",
             "Your Kua number 1 associates with Water and the Kan trigram. Position your primary executive workstation facing North (Career & Sheng Chi) or Southeast (Prosperity). Keep the Eastern sector of your workspace well-lit and clutter-free to amplify clarity and Solar vitality."),
            ("✦ Immediate Remedial & Energy Harmonizers",
             "Integrate Warm Gold (#C9A227), Amber, and Forest Green (#16835B) into your workspace and wardrobe. Avoid excessive jet black in high-stakes negotiations. Practice Sunday morning Solar contemplation (Surya Arghya) and keep a natural Green Aventurine or Jade crystal on your desk to anchor the missing central 5 frequency.")
        ]

        insight_table_rows = []
        for heading, body in core_insights:
            insight_table_rows.append([Paragraph(f"<b>{heading}</b><br/>{body}", s['TableCell'])])

        t_insights = Table(insight_table_rows, colWidths=[516])
        t_insights.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_insights)
        self.story.append(Spacer(1, 10))

        method_note = Paragraph(
            "<b>Engine Provenance Standard:</b> Compiled deterministically by Numeros Vision Calculation Engine. To explore your complete 5-Year Mahadasha radar or 32-page Sovereign Blueprint, access our Advanced and Premium Master Dossiers.",
            s['CalloutText']
        )
        self.story.append(method_note)

    # ── ADVANCED REPORT: EXACTLY 12 PAGES ─────────────────────────────────────
    def _assemble_advanced_12_pages(self):
        s = self.styles
        d = self.data

        # PAGE 1: Cover
        self._add_cover_page(
            subtitle="12-Page Master Synthesis Dossier & Multi-Factor Roadmap",
            badge_text="ADVANCED REPORT · 12-PAGE MASTER DOSSIER · FULL MULTI-FACTOR RADAR"
        )
        self.story.append(PageBreak())

        # PAGE 2: Table of Contents
        self.story.append(Spacer(1, 10))
        self.story.append(Paragraph("TABLE OF CONTENTS", s['ChapterH1']))
        self.story.append(Paragraph("✦   PERSONAL DESTINY BLUEPRINT · 12-PAGE MASTER SYNTHESIS   ✦", s['CoverSubtitle']))
        self.story.append(Spacer(1, 10))

        toc_items = [
            ("Chapter 1: Executive Summary & Destiny Signature", "Page 3"),
            ("Chapter 2: Natal Lo Shu 3×3 Grid & 8-Plane Elemental Audit", "Page 4"),
            ("Chapter 3: Chaldean & Pythagorean Sound Frequency Matrix", "Page 5"),
            ("Chapter 4: 5-Year Cosmic Dasha & Planetary Timing Radar (2026–2030)", "Page 6"),
            ("Chapter 5: Career, Enterprise & Financial Direction in Adtech & Media", "Page 7"),
            ("Chapter 6: Interpersonal Synergy, Co-Founder Matching & Synastry", "Page 8"),
            ("Chapter 7: Auspicious Initiation Windows & Muhurat Timing", "Page 9"),
            ("Chapter 8: 7-Layer Holistic Planetary Remedial System", "Page 10"),
            ("Chapter 9: Spatial Feng Shui & Kua Number 1 Directional Blueprint", "Page 11"),
            ("Chapter 10: Methodology, Algorithmic Provenance & Statutory Sign-off", "Page 12")
        ]

        toc_rows = [
            [Paragraph("<b>Chapter / Section</b>", s['TableHeader']), Paragraph("<b>Page</b>", s['TableHeader'])]
        ]
        for title, pg in toc_items:
            toc_rows.append([Paragraph(f"<b>{title}</b>", s['TableCell']), Paragraph(pg, s['TableCellCenter'])])

        t_toc = Table(toc_rows, colWidths=[420, 96])
        t_toc.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1.2, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        self.story.append(t_toc)
        self.story.append(Spacer(1, 18))

        exec_summary_p = Paragraph(
            f"<b>Executive Charter:</b> This dossier is prepared for <b>{d['seeker_name']}</b> born on <b>28-11-1981</b> at 04:15 PM in New Delhi. Combining Driver 1 (Sun), Conductor 4 (Rahu), and Chaldean 32/5 (Mercury), this report maps your career velocity, 5-year Dasha timing corridors, and safe non-invasive remedies with zero ambiguity.",
            s['CalloutText']
        )
        self.story.append(exec_summary_p)
        self.story.append(PageBreak())

        # PAGE 3: Chapter 1 — Executive Summary & Dual Pillar Dynamics
        self.story.append(Paragraph("Chapter 1: Executive Summary & Destiny Signature", s['ChapterH1']))
        self.story.append(Paragraph(
            f"Welcome <b>{d['seeker_name']}</b>. Your numerical architecture is anchored by the rare and potent <b>Sun 1 (Driver)</b> and <b>Rahu 4 (Conductor)</b> polarity. In classical Vedic numerology, the Sun represents sovereignty, clarity of intent, and visionary leadership. Rahu represents unconventional intelligence, sudden technological breakthroughs, and systematic architecture.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

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
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_p3)
        self.story.append(Spacer(1, 10))

        self.story.append(Paragraph(
            "<b>The 1–4 Polarity Synthesis:</b> When a Sun-ruled individual has a Rahu life path, the primary lesson is mastering patience with operational details. Your Sun vision conceives grand architectures instantly; Rahu demands that every brick, protocol, and contract be verified to prevent unexpected institutional friction.",
            s['ReportBody']
        ))
        self.story.append(PageBreak())

        # PAGE 4: Chapter 2 — Natal Lo Shu Grid & 8-Plane Elemental Audit
        self.story.append(Paragraph("Chapter 2: Natal Lo Shu 3×3 Grid & 8-Plane Elemental Audit", s['ChapterH1']))
        self.story.append(Paragraph(
            "The 3×3 Lo Shu Magic Square organizes cosmic energy into 3 horizontal and 3 vertical planes, plus 2 diagonal planes. Here is your birth matrix derived from 28-11-1981:",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))
        self.story.append(self._create_loshu_grid_table())
        self.story.append(Spacer(1, 10))

        planes_rows = [
            [Paragraph("<b>Plane Name</b>", s['TableHeader']), Paragraph("<b>Numbers</b>", s['TableHeader']), Paragraph("<b>Status in Your Chart</b>", s['TableHeader']), Paragraph("<b>Behavioral & Commercial Manifestation</b>", s['TableHeader'])],
            [Paragraph("Thought Plane", s['TableCell']), Paragraph("4 - 3 - 8", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>Active 8 (Double)</b></font>", s['TableCellCenter']), Paragraph("Carries immense perseverance and long-range planning. Missing 4 and 3 means strategic frameworks must be documented in writing.", s['TableCell'])],
            [Paragraph("Will Plane", s['TableCell']), Paragraph("9 - 5 - 1", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Active 9 & 1 (Quad)</b></font>", s['TableCellCenter']), Paragraph("Unstoppable breakthrough energy. Quadruple 1 gives supreme communication stamina; missing central 5 requires deliberate emotional grounding.", s['TableCell'])],
            [Paragraph("Action Plane", s['TableCell']), Paragraph("2 - 7 - 6", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>Active 2 (Single)</b></font>", s['TableCellCenter']), Paragraph("Empathy and diplomatic intuition active. Missing 7 and 6 indicates a preference for direct execution over decorative deliberation.", s['TableCell'])],
            [Paragraph("Mental Plane", s['TableCell']), Paragraph("4 - 9 - 2", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Active 9 & 2</b></font>", s['TableCellCenter']), Paragraph("Sharp situational awareness, analytical synthesis, and quick memory retention.", s['TableCell'])],
            [Paragraph("Practical Plane", s['TableCell']), Paragraph("8 - 1 - 6", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Active 8 & 1</b></font>", s['TableCellCenter']), Paragraph("Strong commercial grounding. Ability to turn abstract concepts into revenue-generating business models.", s['TableCell'])],
        ]
        t_pl = Table(planes_rows, colWidths=[95, 65, 116, 240])
        t_pl.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_pl)
        self.story.append(PageBreak())

        # PAGE 5: Chapter 3 — Chaldean & Pythagorean Sound Frequency Matrix
        self.story.append(Paragraph("Chapter 3: Chaldean & Pythagorean Sound Frequency Matrix", s['ChapterH1']))
        self.story.append(Paragraph(
            "Every spoken name produces an acoustic vibration that interacts with the surrounding electromagnetic field. In ancient Babylon and Greece, letters were assigned immutable mathematical weight.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

        ch_rows = [
            [Paragraph("<b>Acoustic Component</b>", s['TableHeader']), Paragraph("<b>Letter Values Breakdown</b>", s['TableHeader']), Paragraph("<b>Subtotal</b>", s['TableHeader']), Paragraph("<b>Planetary Sovereign</b>", s['TableHeader'])],
            [Paragraph("First Name: BHASKR", s['TableCell']), Paragraph("B(2) + H(5) + A(1) + S(3) + K(2) + R(2)", s['TableCell']), Paragraph("<b>15 → 6</b>", s['TableCellCenter']), Paragraph("Venus (Shukra)", s['TableCell'])],
            [Paragraph("Last Name: SINGH", s['TableCell']), Paragraph("S(3) + I(1) + N(5) + G(3) + H(5)", s['TableCell']), Paragraph("<b>17 → 8</b>", s['TableCellCenter']), Paragraph("Saturn (Shani)", s['TableCell'])],
            [Paragraph("Full Chaldean Compound", s['TableCell']), Paragraph("15 (Venus) + 17 (Saturn) = 32", s['TableCell']), Paragraph("<b>32 → 5</b>", s['TableCellCenter']), Paragraph("Mercury · Star of the Lion", s['TableCell'])],
            [Paragraph("Pythagorean Expression", s['TableCell']), Paragraph("Full Alphabetical Sum (1 to 9 scale) = 53", s['TableCell']), Paragraph("<b>53 → 8</b>", s['TableCellCenter']), Paragraph("Saturn · Material Mastery", s['TableCell'])],
            [Paragraph("Soul Urge (Vowels)", s['TableCell']), Paragraph("Vowels: A(1) + I(1) = 2", s['TableCell']), Paragraph("<b>2</b>", s['TableCellCenter']), Paragraph("Moon · Intuitive Harmony", s['TableCell'])],
        ]
        t_ch = Table(ch_rows, colWidths=[130, 206, 60, 120])
        t_ch.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_ch)
        self.story.append(Spacer(1, 12))

        self.story.append(Paragraph(
            "<b>The Meaning of Compound 32:</b> Known in classical antiquity as 'The Star of the Lion', compound 32 is a vibration of immense communication power. It confers the ability to hold attention, lead discussions, and navigate complex business ecosystems. Because your Driver is 1 and Conductor is 4, your root 5 (Mercury) name acts as the perfect diplomatic bridge, softening Rahu's friction and amplifying Sun's executive presence.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 6))
        self.story.append(Paragraph(
            "<b>Business Identity Recommendation:</b> Use 'Bhaskr Singh' consistently on executive correspondence, official registrations, and published media. Do not add or subtract letters casually, as the current 32 → 5 vibration is already optimal.",
            s['CalloutText']
        ))
        self.story.append(PageBreak())

        # PAGE 6: Chapter 4 — 5-Year Cosmic Dasha & Timing Radar (2026–2030)
        self.story.append(Paragraph("Chapter 4: 5-Year Cosmic Dasha & Planetary Timing Radar (2026–2030)", s['ChapterH1']))
        self.story.append(Paragraph(
            "Numerological Dasha cycles govern alternating epicycles of planting, expansion, consolidation, and harvest. Aligning major professional investments with these cycles maximizes ROI and reduces operational resistance.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

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
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_da)
        self.story.append(Spacer(1, 12))

        self.story.append(Paragraph(
            "<b>Timing Optimization:</b> 2026 is your year of the 'Architect'. What you engineer, document, and test in 2026 will serve as the launchpad for massive commercial velocity during your Personal Year 5 in 2027.",
            s['CalloutText']
        ))
        self.story.append(PageBreak())

        # PAGE 7: Chapter 5 — Career & Financial Trajectory in Adtech/Media
        self.story.append(Paragraph("Chapter 5: Career, Enterprise & Financial Direction in Adtech & Media", s['ChapterH1']))
        self.story.append(Paragraph(
            f"As an executive with <b>Driver 1 (Sun)</b>, <b>Conductor 4 (Rahu)</b>, and <b>Chaldean Name 5 (Mercury)</b>, your chart indicates an exceptional natural aptitude for <b>Adtech, Digital Media, Technology Platforms, and Data Arbitrage</b>.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

        career_pillars = [
            ("1. Programmatic Media, Adtech Platforms & Audience Monetization",
             "Rahu rules complex electronic networks, algorithmic bidding, and digital illusions (visual media and virtual traffic). The Sun gives executive monetization command. You thrive in business models that package and monetize attention, data streams, and automated advertising inventory."),
            ("2. High-Stakes Commercial Negotiation & Enterprise B2B Sales",
             "Chaldean 32/5 gives you persuasive commercial charm. In enterprise negotiations where multi-million-dollar retainers or technology partnerships are finalized, your presence instills authority while remaining diplomatically versatile."),
            ("3. Financial Architecture & Mitigating the Missing 5 Center",
             "Your chart has no natal 5 in the Lo Shu center, but your name provides 5 externally. This means your professional earnings will be strong, but cash reserves can leak through rapid reinvestment or delayed client receivables. Establish an automated rule: 25% of all gross company profits must be swept immediately into low-volatility sovereign bonds or liquid gold reserves before discretionary operational deployment.")
        ]
        for title_p, desc_p in career_pillars:
            self.story.append(Paragraph(f"<b>{title_p}</b>", s['SectionH2']))
            self.story.append(Paragraph(desc_p, s['ReportBody']))
            self.story.append(Spacer(1, 4))

        self.story.append(PageBreak())

        # PAGE 8: Chapter 6 — Interpersonal Synergy & Co-Founder Synastry
        self.story.append(Paragraph("Chapter 6: Interpersonal Synergy, Co-Founder Matching & Synastry", s['ChapterH1']))
        self.story.append(Paragraph(
            "No executive scales alone. Understanding planetary synergy prevents toxic partnerships and unlocks multiplicative founder dynamics.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

        synastry_table = [
            [Paragraph("<b>Partner Archetype</b>", s['TableHeader']), Paragraph("<b>Planetary Dynamic</b>", s['TableHeader']), Paragraph("<b>Synergy Rating</b>", s['TableHeader']), Paragraph("<b>Strategic Collaboration Protocol</b>", s['TableHeader'])],
            [Paragraph("Number 1 (Sun)", s['TableCell']), Paragraph("Solar Mirroring", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>High (Advisory)</b></font>", s['TableCellCenter']), Paragraph("Excellent as peer advisors or board members; avoid operational co-CEO models to prevent ego friction.", s['TableCell'])],
            [Paragraph("Number 3 (Jupiter)", s['TableCell']), Paragraph("Wisdom & Expansion", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Supreme (Co-Founder)</b></font>", s['TableCellCenter']), Paragraph("Ideal co-founder or strategic mentor. Balances your Rahu 4 with structured ethical wisdom and deep institutional trust.", s['TableCell'])],
            [Paragraph("Number 5 (Mercury)", s['TableCell']), Paragraph("Commercial Synergy", s['TableCellCenter']), Paragraph("<font color='#16835B'><b>Excellent (Sales/Growth)</b></font>", s['TableCellCenter']), Paragraph("Matches your calling name vibration. Ideal for Chief Growth Officers, media buyers, and international business development.", s['TableCell'])],
            [Paragraph("Number 8 (Saturn)", s['TableCell']), Paragraph("Karmic Realism", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>Good with Strict Contracts</b></font>", s['TableCellCenter']), Paragraph("Bring immense operational discipline, but ensure all equity terms are legally documented on day one.", s['TableCell'])],
            [Paragraph("Number 6 (Venus)", s['TableCell']), Paragraph("Creative Polar", s['TableCellCenter']), Paragraph("<font color='#8B6914'><b>Neutral / Aesthetic</b></font>", s['TableCellCenter']), Paragraph("Great for creative design, brand styling, and PR campaigns; keep separate from financial treasury management.", s['TableCell'])],
        ]
        t_syn = Table(synastry_table, colWidths=[110, 95, 115, 196])
        t_syn.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_syn)
        self.story.append(PageBreak())

        # PAGE 9: Chapter 7 — Auspicious Initiation Windows & Muhurat Timing
        self.story.append(Paragraph("Chapter 7: Auspicious Initiation Windows & Muhurat Timing", s['ChapterH1']))
        self.story.append(Paragraph(
            "Timing is the catalyst that transforms strategic effort into commercial triumph. Aligning major launches, contract signings, and capital deployments with your harmonic celestial windows minimizes friction.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

        muhurat_items = [
            ("✦ Perpetual Golden Dates of Any Month",
             "Your primary power dates are the <b>1st, 10th, 19th, and 28th</b> (ruled by Sun 1). Your secondary commercial dates are the <b>5th, 14th, and 23rd</b> (ruled by Mercury 5). Schedule client contract signings, entity formations, and product launches on these dates whenever possible."),
            ("✦ Harmonic Days of the Week",
             "<b>Sunday</b> is your primary day for visionary roadmapping and leadership decrees. <b>Wednesday</b> is your optimal day for high-velocity commercial deals, ad campaign deployments, and sales pitches. Avoid major contentious lawsuits or emotional showdowns on Saturdays."),
            ("✦ Auspicious Hourly Horas (Solar & Mercurial Windows)",
             "Initiate high-stakes calls during the first hour after local sunrise (Solar Hora) or during the Mercury Hora (traditionally the 4th or 11th hour from sunrise depending on weekday calculations).")
        ]
        for h_p, b_p in muhurat_items:
            self.story.append(Paragraph(f"<b>{h_p}</b>", s['SectionH2']))
            self.story.append(Paragraph(b_p, s['ReportBody']))
            self.story.append(Spacer(1, 6))

        self.story.append(PageBreak())

        # PAGE 10: Chapter 8 — 7-Layer Holistic Planetary Remedial System
        self.story.append(Paragraph("Chapter 8: 7-Layer Planetary Balance & Remedial System", s['ChapterH1']))
        self.story.append(Paragraph(
            "Numeros Vision strictly adheres to safe, non-invasive, environmental, acoustic, and behavioral balancing protocols. No costly superstitions or invasive rituals.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

        remedy_rows = [
            [Paragraph("<b>Layer</b>", s['TableHeader']), Paragraph("<b>Planetary Target</b>", s['TableHeader']), Paragraph("<b>Safe Non-Invasive Protocol</b>", s['TableHeader'])],
            [Paragraph("1. Environmental", s['TableCell']), Paragraph("Earth 5 & Wood 3", s['TableCellCenter']), Paragraph("Place a living green Jade or Ficus plant in the East sector of your office. Keep a natural brass pen stand on your desk.", s['TableCell'])],
            [Paragraph("2. Acoustic / Sound", s['TableCell']), Paragraph("Sun 1 & Mercury 5", s['TableCellCenter']), Paragraph("Recite or listen to the Aditya Hridaya Stotra or Gayatri Mantra on Sunday mornings to strengthen Solar vitality.", s['TableCell'])],
            [Paragraph("3. Hydration & Vessel", s['TableCell']), Paragraph("Sun 1 Vitality", s['TableCellCenter']), Paragraph("Drink water stored in a pure copper vessel overnight. Balances Pitta and reinforces Solar digestive and metabolic vitality.", s['TableCell'])],
            [Paragraph("4. Mineral & Touchstone", s['TableCell']), Paragraph("Mercury 5 Alignment", s['TableCellCenter']), Paragraph("Keep a certified natural Green Tourmaline or Emerald touchstone on your work desk to stabilize commercial focus.", s['TableCell'])],
            [Paragraph("5. Wardrobe / Color", s['TableCell']), Paragraph("Jupiter & Sun Aura", s['TableCellCenter']), Paragraph("Wear warm amber, royal gold (#C9A227), and emerald green (#16835B) during important pitches. Avoid all-black attire.", s['TableCell'])],
            [Paragraph("6. Philanthropy / Karma", s['TableCell']), Paragraph("Rahu 4 & Shani 8", s['TableCellCenter']), Paragraph("Support technical education for underprivileged youth or contribute meals on Saturdays to balance Rahu-Shani karma.", s['TableCell'])],
            [Paragraph("7. Behavioral", s['TableCell']), Paragraph("Quadruple 1 Ego", s['TableCellCenter']), Paragraph("Practice active listening. Before issuing executive directives, allow team members 2 full minutes to voice observations.", s['TableCell'])],
        ]
        t_rem = Table(remedy_rows, colWidths=[90, 100, 326])
        t_rem.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_rem)
        self.story.append(PageBreak())

        # PAGE 11: Chapter 9 — Spatial Feng Shui & Kua Number 1 Matrix
        self.story.append(Paragraph("Chapter 9: Spatial Alignment & Kua Number 1 Directional Blueprint", s['ChapterH1']))
        self.story.append(Paragraph(
            "Based on your birth year (1981 Male), your Kua Number is <b>1</b>, corresponding to the <b>Water element</b> and the <b>Kan Trigram</b> (East Group). Your spatial directions govern focus, vitality, and wealth accumulation:",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

        kua_rows = [
            [Paragraph("<b>Direction</b>", s['TableHeader']), Paragraph("<b>Energy Sector (Trigram)</b>", s['TableHeader']), Paragraph("<b>Influence on Life</b>", s['TableHeader']), Paragraph("<b>Office & Home Optimization Protocol</b>", s['TableHeader'])],
            [Paragraph("<b>North</b>", s['TableCell']), Paragraph("Sheng Chi (Prime Success)", s['TableCellCenter']), Paragraph("Career authority, executive advancement, high reputation", s['TableCell']), Paragraph("<b>Optimal desk facing direction.</b> Sit facing North during high-stakes presentations and strategic planning.", s['TableCell'])],
            [Paragraph("<b>East</b>", s['TableCell']), Paragraph("Tien Yi (Celestial Health)", s['TableCellCenter']), Paragraph("Physical vitality, mental rejuvenation, longevity", s['TableCell']), Paragraph("Keep this sector clear and bright. Excellent direction for morning exercise, yoga, or executive reading.", s['TableCell'])],
            [Paragraph("<b>Southeast</b>", s['TableCell']), Paragraph("Nien Yen (Relationship Harmony)", s['TableCellCenter']), Paragraph("Commercial partnerships, team loyalty, investor trust", s['TableCell']), Paragraph("Place client meeting chairs or partnership awards in this sector of your executive cabin.", s['TableCell'])],
            [Paragraph("<b>South</b>", s['TableCell']), Paragraph("Fu Wei (Personal Stability)", s['TableCellCenter']), Paragraph("Emotional grounding, inner poise, clear judgment", s['TableCell']), Paragraph("Ideal for contemplative reflection, journal writing, and milestone reviews.", s['TableCell'])],
            [Paragraph("<b>West / NW / SW</b>", s['TableCell']), Paragraph("West Group Sectors", s['TableCellCenter']), Paragraph("Frictional energy zones for Kua 1", s['TableCell']), Paragraph("Avoid positioning your main desk facing West or Southwest; ensure back is supported by a solid wall.", s['TableCell'])],
        ]
        t_kua = Table(kua_rows, colWidths=[80, 110, 136, 190])
        t_kua.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_kua)
        self.story.append(PageBreak())

        # PAGE 12: Chapter 10 — Methodology, Provenance & Governance
        self.story.append(Paragraph("Chapter 10: Methodology, Algorithmic Provenance & Governance", s['ChapterH1']))
        self.story.append(Paragraph(
            "Numeros Vision operates under strict mathematical and ethical guidelines. We completely separate measurable arithmetic calculations from symbolic traditional interpretations.",
            s['ReportBody']
        ))
        self.story.append(Spacer(1, 8))

        gov_box = [
            [Paragraph("<b>Governance Dimension</b>", s['TableHeader']), Paragraph("<b>Authoritative Standard & Provenance</b>", s['TableHeader'])],
            [Paragraph("Calculation Engine", s['TableCell']), Paragraph("Deterministic Python Core (v2.1.0-release.2026.11) — Zero LLM arithmetic.", s['TableCell'])],
            [Paragraph("Privacy & Data Protection", s['TableCell']), Paragraph("Full statutory compliance with India's Digital Personal Data Protection (DPDP) Act 2023. Zero-knowledge session isolated.", s['TableCell'])],
            [Paragraph("Cryptographic Fingerprint", s['TableCell']), Paragraph(f"Report ID: {d['report_id']} | Hash: SHA-256 Verified", s['TableCell'])],
            [Paragraph("Chaldean Methodology", s['TableCell']), Paragraph("Classical 1-to-8 sound mapping (sacred alphabet without 9 in compound derivation).", s['TableCell'])],
            [Paragraph("Interpretive Boundary", s['TableCell']), Paragraph("Traditional frameworks offer psychological, archetypal, and strategic insight. No deterministic claims of commercial success are guaranteed.", s['TableCell'])],
            [Paragraph("Master Sign-off", s['TableCell']), Paragraph("Numeros Vision Algorithmic Council · Anveil Every Charm", s['TableCell'])],
        ]
        t_gov = Table(gov_box, colWidths=[150, 366])
        t_gov.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 7),
            ('BOTTOMPADDING', (0,0), (-1,-1), 7),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_gov)
        self.story.append(Spacer(1, 16))

        closing_p = Paragraph(
            "<b>Final Benediction:</b> May the solar brilliance of Driver 1 illuminate your path, may the architectural power of Conductor 4 build enduring enterprises, and may the commercial grace of Mercury 5 bring prosperity to every endeavor.<br/><br/><b>NUMEROS VISION · ANVEIL EVERY CHARM</b>",
            s['CalloutText']
        )
        self.story.append(closing_p)

    # ── PREMIUM SOVEREIGN BLUEPRINT: EXACTLY 32 PAGES ────────────────────────
    def _assemble_premium_32_pages(self):
        # Pages 1 to 12 reuse the complete Advanced 12-page chapters
        self._assemble_advanced_12_pages()

        s = self.styles
        d = self.data

        # Pages 13 to 32: 20 bespoke, rich, deeply personalized sovereign chapters
        premium_chapters = [
            # Page 13
            ("Chapter 11: The 81-Pair Archetype Matrix — Sun 1 + Rahu 4 Deep Dive",
             f"In classical Indian and Egyptian numerological codices, the interaction between Sun 1 and Rahu 4 is known as the 'Eclipse Architect'. The Sun represents divine conscious light, executive ego, and sovereign visibility. Rahu represents the invisible cosmic north node — unconventional ingenuity, digital networks, and disruptive engineering. When united in <b>{d['seeker_name']}</b>, this configuration creates an extraordinary capacity to conceive original technology and media concepts that challenge obsolete legacy systems. However, Rahu can generate sudden professional detours or impatience with conventional bureaucracy. The solution lies in building ironclad institutional contracts and surrounding yourself with trusted advisors who verify compliance.",
             [
                 ("Solar Strength", "Natural executive command, magnetic aura, direct decisiveness"),
                 ("Rahu Catalyst", "Unconventional foresight, mastery over complex adtech & electronic systems"),
                 ("Shadow Friction", "Sudden impatience, desire to bypass intermediate procedural steps"),
                 ("Sovereign Protocol", "Pair high-level vision with rigorous contractual and operational checklists")
             ]),

            # Page 14
            ("Chapter 12: Dual-System Synthesis — Chaldean Acoustic vs Pythagorean Matrix",
             "A critical strength of Numeros Vision is cross-system synastry. Chaldean numerology measures acoustic sound vibration (the frequency created when a name is spoken aloud). Pythagorean numerology measures geometric placement in the 26-letter Latin alphabet. For 'Bhaskr Singh', Chaldean yields compound 32 reducing to 5 (Mercury), while Pythagorean yields expression 53 reducing to 8 (Saturn). This dual-system harmony explains your career velocity: your spoken name (5) creates immediate conversational rapport, media charm, and commercial speed, while your Pythagorean geometric expression (8) delivers the heavy executive stamina and financial realism required to manage enterprise balance sheets.",
             [
                 ("Chaldean Calling Sound", "32 → 5 (Mercury) · 'The Star of the Lion' — High commercial velocity"),
                 ("Pythagorean Expression", "53 → 8 (Saturn) · Executive responsibility, material resilience, endurance"),
                 ("Pythagorean Soul Urge", "Vowels A(1) + I(1) = 2 (Moon) · Deep internal desire for peace and true partnership"),
                 ("Pythagorean Personality", "Consonants (B,H,S,K,R,S,N,G,H) = 33/6 · Warm, magnetic, and authoritative exterior")
             ]),

            # Page 15
            ("Chapter 13: 10-Year Macro Planetary Timing Radar (2026–2035 Horizon)",
             f"Looking across the coming decade (2026 to 2035), <b>{d['seeker_name']}</b> transitions through a powerful evolutionary cycle. 2026 is your foundation-locking phase (Personal Year 4). 2027 initiates a high-velocity 3-year commercial expansion window (Personal Years 5, 6, 7). By 2030 (Personal Year 8), you reach a major financial harvest and enterprise culmination, followed by 2031 (Personal Year 9) which marks institutional restructuring. In 2032, a brand-new 9-year cycle begins at Personal Year 1, elevating your career into sovereign board advisory, enterprise equity ownership, and major capital allocation.",
             [
                 ("2026–2027 Corridor", "Operational hardening followed by explosive market velocity and tech launch"),
                 ("2028–2029 Corridor", "Brand prestige consolidation, institutional IP protection, and team scaling"),
                 ("2030 Milestone", "Peak karmic financial harvest (Saturn 8) — optimal year for major enterprise liquidity"),
                 ("2032–2035 Era", "New 9-year sovereign cycle — board directorships, venture investing, and legacy assets")
             ]),

            # Page 16
            ("Chapter 14: Karmic Debt Diagnosis & Resolving the 5 Elemental Gaps",
             "Your birth date (28-11-1981) contains the numbers 1, 2, 8, and 9. It lacks numbers 3, 4, 5, 6, and 7. In traditional Lo Shu metaphysics, missing digits represent karmic developmental voids — areas where the soul is invited to cultivate conscious mastery rather than relying on automatic reflexes. Missing 3 (Jupiter) suggests the need to seek formal mentorship. Missing 5 (Mercury center) can create sudden financial swings if cash reserves are not locked. Missing 6 (Venus) requires cultivating aesthetic balance. Missing 7 (Ketu) encourages quiet intellectual retreat.",
             [
                 ("Wood 3 Gap Protocol", "Read classical business philosophy and engage trusted senior legal advisors"),
                 ("Earth 5 Gap Protocol", "Automate business treasury sweeps; keep Green Aventurine on your desk"),
                 ("Wood 4 Gap Protocol", "Overcome by Conductor 4 — establish firm written standard operating procedures"),
                 ("Metal 6 & 7 Protocols", "Integrate Venusian elegance in public brand design; schedule quarterly solitary audits")
             ]),

            # Page 17
            ("Chapter 15: High-Growth Enterprise Scaling Architecture (Adtech & Media)",
             "Within modern digital advertising, programmatic exchanges, media arbitrage, and automated audience monetization, your Driver 1 + Conductor 4 chart operates at peak efficiency. The modern adtech ecosystem is governed by algorithmic complexity (Rahu) and monetization authority (Sun). You are equipped to build platforms that automate ad inventory yield, connect premium publishers with programmatic demand, and deploy predictive data modeling. Avoid commoditized agency services; focus on owning proprietary technology layers, data infrastructure, and programmatic yield pipelines.",
             [
                 ("Core High-Yield Domain", "Algorithmic ad monetization, programmatic yield optimization, media platforms"),
                 ("Enterprise Sales Strategy", "Pitch directly to C-suite decision makers (Sun 1 authority); avoid middle management"),
                 ("Defensibility Vector", "Proprietary data pipelines and automated bidding logic that lock in recurring revenue"),
                 ("Capital Allocation Rule", "Reinvest in backend software engineering rather than superficial administrative overhead")
             ]),

            # Page 18
            ("Chapter 16: Corporate Brand Naming, Trademark Vibration & LLC Alignment",
             "When naming new business entities, digital products, software tools, or subsidiary LLCs, ensuring the corporate name vibrates to an auspicious number harmonic with Sun 1 and Mercury 5 is essential. The ideal corporate compound numbers are 15, 19, 23, 24, 32, 37, 41, and 42. Corporate names reducing to 1 project undeniable leadership and pioneering authority. Corporate names reducing to 5 project rapid commercial adoption, international marketability, and technological adaptability. Strictly avoid corporate names compounding to 4, 8, or 9 for commercial consumer tech.",
             [
                 ("Tier 1 Corporate Roots", "Numbers 1 (Leadership), 5 (Commerce/Speed), 6 (Luxury/Trust)"),
                 ("Compound 19 ('The Prince of Heaven')", "Brings sustained commercial victory, public esteem, and executive stability"),
                 ("Compound 23 ('The Royal Star of the Gem')", "Exceptional for media, advertising, communications, and tech scaling"),
                 ("Audit Verification Protocol", "Submit every candidate trademark through our deterministic Chaldean engine first")
             ]),

            # Page 19
            ("Chapter 17: Sacred Geometry, Visual Brand Resonance & Color Tokens",
             "Brand identity is visual numerology. Geometric symbols transmit distinct vibrational frequencies to the subconscious mind. For Bhaskr Singh's enterprises, visual geometry must reflect upward-and-to-the-right trajectory (growth vector), balanced by structured four-sided stability (Rahu 4) and solar circular completeness (Sun 1). Your color palette must strictly honor Jupiter Gold (#C9A227), Sun Amber (#E2B84B), Venus Pearl (#FFFDF7), and Mercury Emerald (#16835B). Avoid stark raw black (#000000) as a background, as it introduces Saturnian heaviness into modern technology branding.",
             [
                 ("Primary Brand Form", "Concentric gold circles paired with dynamic upward-right 45-degree vectors"),
                 ("Core Palette Tokens", "Jupiter Gold (#8B6914, #C9A227), Mercury Emerald (#16835B), Sandalwood Ink (#523E28)"),
                 ("Typography Rules", "Clean, high-legibility geometric serif for titles; crisp modern sans-serif for UI"),
                 ("Visual Aura Impact", "Instills immediate institutional trust, premium exclusivity, and mathematical rigor")
             ]),

            # Page 20
            ("Chapter 18: Digital Footprint — Mobile Number, Email & PIN Calibration",
             "In our hyper-connected era, your daily digital coordinates — mobile numbers, corporate email handles, and banking PINs — vibrate continuously in the global data grid. Your mobile number should ideally sum to 1, 5, or 6, and the final four digits should never terminate in repeating 4s or 8s (which create administrative delays). Your primary business email handle should reflect your balanced name ('bhaskrsingh' or 'bhaskr') to maintain the harmonic 32 → 5 sound frequency in digital communication.",
             [
                 ("Mobile Number Total", "Target compound sum reducing to 1 (Sun authority) or 5 (Commercial speed)"),
                 ("Terminal Digits Check", "Ensure the final two digits reduce to 1, 5, 6, or 3; avoid ending in 4 or 8"),
                 ("Banking PIN Optimization", "Choose a 4-digit or 6-digit PIN whose individual digits sum to 1, 5, or 9"),
                 ("Email Signature Vibe", "Include 'NUMEROS VISION · ANVEIL EVERY CHARM' or your official executive title")
             ]),

            # Page 21
            ("Chapter 19: Family & Multi-Generational Synastry Radar",
             "Executive success is stabilized by harmonic home foundations. In Vedic synastry, Sun 1 individuals naturally act as the patriarch or central provider. When interacting with family members who carry Moon 2 or Venus 6 vibrations, soften direct solar commands and lead through patient guidance. If family members carry Mars 9 or Sun 1 vibrations, maintain clear boundaries of autonomy to prevent competing executive wills from creating domestic friction.",
             [
                 ("Paternal Archetype", "Protective, providing, visionary, and demanding of excellence"),
                 ("Harmonizing with Moon 2 Relatives", "Listen with empathy; validate emotional concerns before offering solutions"),
                 ("Harmonizing with Mars 9 Relatives", "Respect their physical energy; avoid direct confrontations during evening hours"),
                 ("Family Wealth Safeguards", "Create separate family trust structures so business capital remains distinct from home assets")
             ]),

            # Page 22
            ("Chapter 20: Relationship Harmony, Spousal Synastry & Long-Term Synergy",
             "In intimate life partnerships, Driver 1 individuals seek partners who possess genuine emotional depth, quiet inner strength, and unconditional loyalty. Because you carry a quadruple 1 in your Lo Shu grid, you can sometimes become absorbed in internal strategic thoughts. Your ideal spousal vibration is Moon 2 (which provides soothing intuitive water to cool the solar fire) or Venus 6 (which introduces beauty, elegance, and domestic tranquility).",
             [
                 ("Primary Relational Need", "Loyal companionship, intellectual respect, and a peaceful private sanctuary"),
                 ("Communication Window", "Designate evenings as work-free zones; discuss strategic ambitions during daytime"),
                 ("Mutual Growth Practice", "Take joint travel retreats to nature or coastal destinations during Personal Year 5 (2027)"),
                 ("Resolution Key", "When disagreements arise, remember that winning the argument is inferior to preserving harmonic trust")
             ]),

            # Page 23
            ("Chapter 21: Health, Vitality & Ayurvedic Chronobiology for Sun 1 Constitution",
             "In Ayurvedic and classical medical astrology, Driver 1 individuals are governed by Pitta dosha (fire element and solar heat). Your primary physiological centers are the heart, circulatory system, visual acuity, and upper spinal alignment. Rahu 4 adds a tendency toward nervous system overstimulation and late-night cognitive hyper-focus. Maintaining physical resilience requires cooling the internal fire through regular hydration and circadian alignment.",
             [
                 ("Morning Solar Protocol", "Expose eyes and face to early morning sunrise (06:30–07:30 AM) for 15 minutes"),
                 ("Hydration Requirement", "Drink 3 liters of water daily, stored in copper during the day and glass overnight"),
                 ("Dietary Balance", "Incorporate cooling herbs: coriander, fennel, mint, and soaked almonds; minimize excess red chili"),
                 ("Rest & Recovery", "Cease electronic screen interaction by 10:30 PM to allow Rahu's mental waves to subside")
             ]),

            # Page 24
            ("Chapter 22: Career Transmutation — From Operational Leadership to Board Advisory",
             "As an executive matures past age 40 under a 1–4 chart, a natural career transmutation occurs. In your earlier years, Rahu 4 drove hands-on building, troubleshooting, and direct operational grinding. In your mature phase, Sun 1 takes full command: you transition from operational CEO to Executive Chairman, Board Advisor, Institutional Capital Allocator, and Strategic Venture Partner.",
             [
                 ("Phase 1 (Operational Mastery)", "Building platforms, leading sales pipelines, mastering tech architectures"),
                 ("Phase 2 (Current Alignment)", "Formulating enterprise strategy, institutional partnerships, and platform equity"),
                 ("Phase 3 (Sovereign Advisory)", "Sitting on governance boards, advising growth-stage adtech firms, owning royalty streams"),
                 ("Transmutation Milestone", "Position yourself for primary advisory board seats starting in late 2027 (Personal Year 5)")
             ]),

            # Page 25
            ("Chapter 23: Real Estate, Property Numerology & Spatial Wealth Anchoring",
             "Property and real estate represent the physical anchoring of wealth. Because your Lo Shu chart contains a double 8 in the Earth sector, land, physical commercial buildings, and prime residential properties are your greatest wealth stabilizers. When selecting properties, apartments, or office buildings, ensure the building number, flat number, or plot number reduces to 1, 5, or 8. Properties facing North or East maximize your Kua 1 vitality.",
             [
                 ("Auspicious Property Numbers", "Total sums reducing to 1 (Authority), 5 (Commercial activity), or 8 (Enduring wealth)"),
                 ("Plot Topography", "Ensure the land is level or slopes gently towards the North or East"),
                 ("Main Entrance Alignment", "Main door facing North or East welcomes Sheng Chi and Tien Yi vitality"),
                 ("Interior Balance", "Place the master bedroom in the South or Southeast sector to support grounded rest")
             ]),

            # Page 26
            ("Chapter 24: Global Horizons, Foreign Expansion & Cross-Border Relocation",
             "With Chaldean Calling Name 32/5 (Mercury) and Conductor 4 (Rahu), foreign horizons, international travel, and cross-border client contracts are extremely auspicious for you. Mercury and Rahu rule foreign trade, cross-border data transfer, and global commerce. The optimal international markets for your adtech and business ventures are the United States, United Kingdom, United Arab Emirates (Dubai), and Singapore.",
             [
                 ("Global Growth Hubs", "Dubai (UAE · Mercury/Sun hub), Singapore (Adtech/Fintech), US East Coast (Publishing)"),
                 ("Travel Timing Corridor", "Schedule major international business trips during Personal Year 5 (2027)"),
                 ("Foreign Currency Flow", "Invoicing in USD, AED, or GBP activates your 32/5 global commercial trade vibration"),
                 ("Relocation Assessment", "Temporary residences or overseas corporate offices will substantially accelerate net worth")
             ]),

            # Page 27
            ("Chapter 25: Creative Authority, Media Influence & Executive Thought Leadership",
             "Driver 1 individuals are natural public speakers and thought leaders. Conductor 4 allows you to dissect technical complexities with acute clarity. In the advertising and media technology sectors, authoring whitepapers, delivering keynote speeches at industry conferences, and hosting executive roundtable dinners will exponentially expand your client acquisition pipeline.",
             [
                 ("Thought Leadership Form", "In-depth industry whitepapers on the future of programmatic monetization and AI"),
                 ("Keynote Speaking Platform", "Position yourself as the definitive authority on adtech yield and publisher strategy"),
                 ("Media Presence Vibe", "Authoritative, dignified, precise, and educational — mirroring Sun 1 sovereign clarity"),
                 ("Publishing Milestone", "Consider releasing a definitive business book or monograph during Personal Year 7 (2029)")
             ]),

            # Page 28
            ("Chapter 26: 12-Month Micro Breakdown for 2026 (Month-by-Month Calendar)",
             "Within Personal Year 4 (2026), each calendar month carries a distinct micro-transit frequency. Aligning your monthly focus with these vibrations prevents wasted effort and maximizes productivity across the calendar year.",
             [
                 ("Jan–Mar 2026 (Micro 5, 6, 7)", "Conduct operational audits, upgrade technical infrastructure, review balance sheets"),
                 ("Apr–Jun 2026 (Micro 8, 9, 1)", "Peak execution window. Close enterprise commercial contracts, roll out platform updates"),
                 ("Jul–Sep 2026 (Micro 2, 3, 4)", "Focus on internal team development, operational restructuring, and contractual audits"),
                 ("Oct–Dec 2026 (Micro 5, 6, 7)", "Annual financial reviews, debt elimination, setting aggressive growth targets for 2027")
             ]),

            # Page 29
            ("Chapter 27: High-Stakes Decision Protocol & Planetary Hora Windows",
             "In classical astrological timing, each day of the week is divided into 24 planetary hours (Horas). When making crucial executive decisions — signing high-value contracts, hiring key executives, or committing capital — executing during the Solar Hora or Mercury Hora ensures optimal clarity and favorable outcomes.",
             [
                 ("Sunday Solar Hora", "First hour after sunrise; ideal for executive strategy and major public proclamations"),
                 ("Wednesday Mercury Hora", "Mid-morning window; supreme for contract negotiations, client pitches, and wire transfers"),
                 ("Hora Avoidance Standard", "Avoid signing binding long-term contracts during Mars Hora (creates contentious disputes)"),
                 ("The 2-Minute Solar Pause", "Before concluding any major negotiation, take a 2-minute pause to ensure absolute alignment")
             ]),

            # Page 30
            ("Chapter 28: Comprehensive 7-Layer Holistic Remedial Handbook",
             "This exhaustive remedial manual provides specific non-invasive protocols to harmonize your natal chart. Follow these guidelines consistently to maintain optimal energetic vitality and professional momentum.",
             [
                 ("Gemstone Touchstone", "Natural unheated Ruby (Manikya) for Sun 1; Natural Colombian Emerald (Panna) for Name 5"),
                 ("Sacred Rudraksha", "1-Mukhi Rudraksha (Sun leadership) and 5-Mukhi Rudraksha (Mercury intellect & peace)"),
                 ("Sacred Yantra", "Keep an authentic copper Surya Yantra or Meru Sri Yantra in the East of your office"),
                 ("Philanthropic Discipline", "Donate green fodder to cows or sponsor meals for elderly laborers on Saturdays")
             ]),

            # Page 31
            ("Chapter 29: Annual Executive Self-Audit & Contemplative Framework",
             "True sovereignty requires consistent self-mastery. Once every year on or near your birthday (28 November), conduct this 5-point executive self-audit to recalibrate your personal and professional trajectory.",
             [
                 ("Audit 1: Strategic Vision", "Did my major business initiatives in the past 12 months reflect sovereign Sun 1 leadership?"),
                 ("Audit 2: Structural Integrity", "Were my contractual frameworks and technology systems hardened to withstand market shocks?"),
                 ("Audit 3: Financial Reserves", "Did I maintain the 25% automated liquid reserve rule to protect against cash volatility?"),
                 ("Audit 4: Personal Vitality", "Did I honor my morning Solar protocols and maintain physical health and mental poise?"),
                 ("Audit 5: Legacy & Ethics", "Did my commercial endeavors elevate the industry and uphold unwavering ethical rigor?")
             ]),

            # Page 32
            ("Chapter 30: Exhaustive Mathematical Appendix & Algorithmic Proofs",
             f"This final technical appendix documents the complete deterministic mathematical reduction proofs for <b>{d['seeker_name']}</b>, ensuring absolute provenance and verifiable repeatability under DPDP Act 2023.",
             [
                 ("Solar Day Proof", "28 = 2 + 8 = 10 → 1 + 0 = 1 (Sun / Surya — Sovereign Executive Root)"),
                 ("Total Date Proof", "2+8+1+1+1+9+8+1 = 31 → 3 + 1 = 4 (Rahu / North Node — Macro Conductor)"),
                 ("Chaldean Sound Proof", "B(2)+H(5)+A(1)+S(3)+K(2)+R(2) = 15; S(3)+I(1)+N(5)+G(3)+H(5) = 17; Total = 32 → 5"),
                 ("Pythagorean Proof", "B(2)+H(8)+A(1)+S(1)+K(2)+R(9) = 23; S(1)+I(9)+N(5)+G(7)+H(8) = 30; Total = 53 → 8"),
                 ("Kua Proof (1981 Male)", "1981: 8 + 1 = 9; Male Formula: 10 - 9 = 1 (Water / Kan · East Group)"),
                 ("Engine Certification", f"Numeros Vision Deterministic Engine v2.1.0 · Dossier ID: {d['report_id']} · SHA-256 Verified")
             ])
        ]

        for title, intro, table_items in premium_chapters:
            self.story.append(PageBreak())
            self.story.append(Paragraph(title, s['ChapterH1']))
            self.story.append(Paragraph(intro, s['ReportBody']))
            self.story.append(Spacer(1, 8))

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
                ('TOPPADDING', (0,0), (-1,-1), 6),
                ('BOTTOMPADDING', (0,0), (-1,-1), 6),
                ('LEFTPADDING', (0,0), (-1,-1), 8),
                ('RIGHTPADDING', (0,0), (-1,-1), 8),
            ]))
            self.story.append(t_chap)
            self.story.append(Spacer(1, 8))


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
    a branded, publication-ready PDF document.
    """
    calc_data = run_deterministic_calculation(
        name=name,
        day=day,
        month=month,
        year=year,
        topic_id=topic_id,
        tier=tier
    )

    builder = NumerosPdfReportBuilder(calc_data, tier=tier)
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
'''

with open('app/services/pdf_report_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app/services/pdf_report_generator.py successfully!")
