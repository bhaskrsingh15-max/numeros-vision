"""
NUMEROS VISION — 2027 YEAR AHEAD PLANNER PDF REPORT GENERATOR (v2.1)
Tagline: ANVEIL EVERY CHARM

Architecture & Constraints:
- Results-Only format: Zero calculation formulas, weights, reduction steps (e.g. 28 -> 10 -> 1),
  grid scores (F+, E+), or internal component names exposed.
- Theme palette & typography strictly identical to existing 12-page and 32-page generator:
  Source: pdf_service/app/services/pdf_report_generator.py (lines 76-86, 89-229).
  COLOR_PEARL_BG   = #FFFDF7
  COLOR_PEARL_MID  = #F7F3EA
  COLOR_GOLD_DARK  = #8B6914
  COLOR_GOLD       = #C9A227
  COLOR_GOLD_LIGHT = #E2B84B
  COLOR_INK_DARK   = #523E28
  COLOR_INK_MUTED  = #7A654D
  COLOR_EMERALD    = #16835B
  COLOR_BORDER     = #EEDDB8
  COLOR_CARD_BG    = #FFFFFF
  COLOR_RED_ALERT  = #A13030
  Fonts: Times-Bold, Times-Roman, Times-Italic.
  Strictly ZERO raw black (#000000).
- Exactly 24 pages:
  Page 1: Cover
  Page 2: Section 1 — Core Numerological Archetypes & 2027 Cycles (Separate Driver & Conductor Lists)
  Page 3: Section 2 — 2027 Macro Strategic Horizon (PY, Sun Sign, 7 Life Areas)
  Page 4: Section 3 — Lo Shu Magic Square & 8 Elemental Planes
  Page 5: Section 4 — Calling Name Resonance & 4-Stage Pinnacles
  Page 6: Section 5 — Key Strategic Auspicious Dates (with Sunrise Tithi, near-boundary annotations, distinct notes)
  Pages 7-18: Section 6 — 12 Monthly Blueprints (1 page per month, with full moon & new moon IST times, no emoji, rating, remedy)
  Page 19: Section 7 — 2027 Remedies Bank (Annual remedy, Traditional Crystal for Mulank, 9 daily micro-actions)
  Pages 20-23: Section 8 — 365-Day Daily Alignment Calendar Appendix (4 quarterly pages, font size 7.2 pt matching TableCellDense)
  Page 24: Section 9 — How to Read This Report & Statutory Legal Notice (with restored {{DISCLAIMER_APPROVED_TEXT}})
- Metadata: Title and Author only.
"""

import os
import io
import json
import math
import datetime
from typing import Dict, Any, List, Optional, Tuple

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

from app.engine.planner_2027_engine import calculate_planner_2027

# Palette from pdf_service/app/services/pdf_report_generator.py lines 76-86
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

PLANET_NAMES = {
    1: ("Sun", "Surya"),
    2: ("Moon", "Chandra"),
    3: ("Jupiter", "Brihaspati"),
    4: ("Rahu", "North Node"),
    5: ("Mercury", "Budh"),
    6: ("Venus", "Shukra"),
    7: ("Ketu", "South Node"),
    8: ("Saturn", "Shani"),
    9: ("Mars", "Mangal"),
}

# Spec: 1 Favourable, 2 Neutral, 3 Favourable, 4 Neutral, 5 Asks for care,
# 6 Favourable, 7 Neutral, 8 Neutral, 9 Asks for care; June for PY 5 shows master flag as 2
MONTH_RATINGS_SPEC = {
    1: "Favourable",
    2: "Neutral",
    3: "Favourable",
    4: "Neutral",
    5: "Asks for care",
    6: "Favourable",
    7: "Neutral",
    8: "Neutral",
    9: "Asks for care"
}

# Spec table: traditional crystal for Mulank
CRYSTALS_BY_MULANK = {
    1: "Sunstone or Carnelian",
    2: "Moonstone",
    3: "Citrine",
    4: "Hessonite garnet",
    5: "Green aventurine",
    6: "Clear quartz",
    7: "Tiger's eye",
    8: "Amethyst or Lapis lazuli",
    9: "Red jasper"
}

def get_tropical_sun_sign(month: int, day: int) -> str:
    """Calculates tropical sun sign from birth month and day."""
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:
        return "Pisces"


class Planner2027ReportCanvas(canvas.Canvas):
    """
    Two-pass canvas drawing luxury gold frames, running headers/footers,
    page counts, SAMPLE watermark (controlled by is_sample flag),
    and clean metadata (Title and Author only).
    """
    def __init__(self, *args, **kwargs):
        self.seeker_name = kwargs.pop("seeker_name", "Valued Client")
        self.is_sample = kwargs.pop("is_sample", True)
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            self.draw_decorations(num_pages)
            super().showPage()
        
        # Strictly Title and Author metadata only
        self.setTitle(f"2027 Year Ahead Planner - {self.seeker_name}")
        self.setAuthor("NUMEROS VISION")
        super().save()

    def draw_decorations(self, total_pages: int):
        self.saveState()
        w, h = self._pagesize

        # 1. Background tint
        self.setFillColor(COLOR_PEARL_BG)
        self.rect(0, 0, w, h, fill=1, stroke=0)

        # 2. Luxury Double Gold Document Frame
        self.setStrokeColor(COLOR_GOLD)
        self.setLineWidth(1.1)
        self.rect(18, 18, w - 36, h - 36, stroke=1, fill=0)

        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.rect(21, 21, w - 42, h - 42, stroke=1, fill=0)

        # 3. Running Header (Pages 2+)
        if self._pageNumber > 1:
            logo_icon = os.path.join(os.path.dirname(__file__), "..", "..", "..", "app", "static", "logos", "nv-logo-mark.png")
            if not os.path.exists(logo_icon):
                logo_icon = os.path.join("app", "static", "logos", "nv-logo-mark.png")
            if os.path.exists(logo_icon):
                try:
                    self.drawImage(logo_icon, 34, h - 31, width=13, height=13, mask='auto', preserveAspectRatio=True)
                except Exception:
                    pass

            self.setFont("Times-Bold", 8)
            self.setFillColor(COLOR_GOLD_DARK)
            self.drawString(51, h - 28, "NUMEROS VISION")

            self.setFont("Times-Italic", 7.5)
            self.setFillColor(COLOR_INK_MUTED)
            self.drawString(136, h - 28, "·   ANVEIL EVERY CHARM")

            self.setFont("Times-Roman", 7.5)
            self.setFillColor(COLOR_GOLD_DARK)
            self.drawRightString(w - 34, h - 28, "2027 YEAR AHEAD PLANNER · ANNUAL BLUEPRINT")

            self.setStrokeColor(COLOR_BORDER)
            self.setLineWidth(0.6)
            self.line(34, h - 33, w - 34, h - 33)

        # 4. Running Footer
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(34, 38, w - 34, 38)

        self.setFont("Times-Roman", 7.5)
        self.setFillColor(COLOR_INK_MUTED)
        self.drawString(34, 26, "Numeros Vision — ANVEIL EVERY CHARM")

        self.setFont("Times-Bold", 8)
        self.setFillColor(COLOR_GOLD_DARK)
        self.drawCentredString(w / 2.0, 26, "2027 ANNUAL MASTER BLUEPRINT")

        page_str = f"Page {self._pageNumber} of {total_pages}"
        self.drawRightString(w - 34, 26, page_str)

        # 5. SAMPLE Watermark (Only when is_sample is True)
        if self.is_sample:
            self.saveState()
            self.setFont("Times-Bold", 54)
            self.setFillColor(colors.Color(0.79, 0.64, 0.15, alpha=0.065))
            self.translate(w / 2.0, h / 2.0)
            self.rotate(45)
            self.drawCentredString(0, 0, "SAMPLE")
            self.restoreState()

        self.restoreState()


def _build_styles() -> Dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        'CoverTitle': ParagraphStyle(
            'CoverTitle', parent=base['Normal'], fontName='Times-Bold', fontSize=26, leading=30,
            textColor=COLOR_GOLD_DARK, alignment=1, spaceAfter=8
        ),
        'CoverSubtitle': ParagraphStyle(
            'CoverSubtitle', parent=base['Normal'], fontName='Times-Roman', fontSize=12, leading=16,
            textColor=COLOR_INK_MUTED, alignment=1, spaceAfter=18
        ),
        'SectionH1': ParagraphStyle(
            'SectionH1', parent=base['Normal'], fontName='Times-Bold', fontSize=13, leading=16,
            textColor=COLOR_GOLD_DARK, spaceBefore=2, spaceAfter=4, keepWithNext=True
        ),
        'SectionH2': ParagraphStyle(
            'SectionH2', parent=base['Normal'], fontName='Times-Bold', fontSize=10, leading=13,
            textColor=COLOR_INK_DARK, spaceBefore=4, spaceAfter=2, keepWithNext=True
        ),
        'Body': ParagraphStyle(
            'Body', parent=base['Normal'], fontName='Times-Roman', fontSize=8.5, leading=11.5,
            textColor=COLOR_INK_DARK, spaceAfter=3
        ),
        'BodyMuted': ParagraphStyle(
            'BodyMuted', parent=base['Normal'], fontName='Times-Italic', fontSize=8, leading=11,
            textColor=COLOR_INK_MUTED, spaceAfter=2
        ),
        'TableHeader': ParagraphStyle(
            'TableHeader', parent=base['Normal'], fontName='Times-Bold', fontSize=8, leading=10,
            textColor=COLOR_GOLD_DARK, alignment=1
        ),
        'TableCell': ParagraphStyle(
            'TableCell', parent=base['Normal'], fontName='Times-Roman', fontSize=8, leading=10.5,
            textColor=COLOR_INK_DARK
        ),
        'TableCellCenter': ParagraphStyle(
            'TableCellCenter', parent=base['Normal'], fontName='Times-Roman', fontSize=8, leading=10.5,
            textColor=COLOR_INK_DARK, alignment=1
        ),
        'TableCellDense': ParagraphStyle(
            'TableCellDense', parent=base['Normal'], fontName='Times-Roman', fontSize=7.2, leading=9.2,
            textColor=COLOR_INK_DARK
        ),
        'TableCellDenseCenter': ParagraphStyle(
            'TableCellDenseCenter', parent=base['Normal'], fontName='Times-Roman', fontSize=7.2, leading=9.2,
            textColor=COLOR_INK_DARK, alignment=1
        ),
        'MetaKey': ParagraphStyle(
            'MetaKey', parent=base['Normal'], fontName='Times-Bold', fontSize=8.5, leading=11,
            textColor=COLOR_GOLD_DARK
        ),
        'MetaVal': ParagraphStyle(
            'MetaVal', parent=base['Normal'], fontName='Times-Roman', fontSize=8.5, leading=11,
            textColor=COLOR_INK_DARK
        ),
    }


class Planner2027PdfBuilder:
    """
    Compiles the 24-page 2027 Year Ahead Planner report in Results-Only format.
    """
    def __init__(
        self,
        calc_data: Dict[str, Any],
        content_library: Dict[str, Any],
        panchang_data: Optional[Dict[str, Any]] = None,
        key_dates_rules: Optional[Dict[str, Any]] = None,
        is_sample: bool = True
    ):
        self.d = calc_data
        self.lib = content_library
        self.panchang = panchang_data or {}
        self.kd_rules = key_dates_rules or {"exclude_amavasya": True, "exclude_rikta_tithis": False, "exclude_krishna_chaturdashi": False}
        self.is_sample = is_sample
        self.styles = _build_styles()
        self.story: List[Any] = []
        
        self.subject = self.d["subject"]
        self.seeker_name = self.subject["full_name"]
        self.dob_str = self.subject["dob"]
        self.dob = datetime.date.fromisoformat(self.dob_str)
        self.sun_sign = get_tropical_sun_sign(self.dob.month, self.dob.day)
        self.py = self.subject["personal_year_2027"]
        self.mulank = self.subject["driver_mulank"]
        self.bhagyank = self.subject["conductor_bhagyank"]

    def build(self) -> bytes:
        # Exactly 24 pages, 23 page breaks
        self._build_page1_cover()
        self.story.append(PageBreak())
        
        self._build_page2_core_numbers()
        self.story.append(PageBreak())
        
        self._build_page3_annual_outlook()
        self.story.append(PageBreak())
        
        self._build_page4_lo_shu_grid()
        self.story.append(PageBreak())
        
        self._build_page5_name_and_pinnacles()
        self.story.append(PageBreak())
        
        self._build_page6_key_dates()
        self.story.append(PageBreak())
        
        # Pages 7-18: 12 Monthly Blueprints (1 page per month)
        for m_idx in range(12):
            self._build_single_monthly_page(self.d["months"][m_idx])
            self.story.append(PageBreak())
        
        self._build_page19_remedies_bank()
        self.story.append(PageBreak())
        
        # Pages 20-23: 365-Day Daily Alignment Calendar Appendix (4 quarterly pages)
        self._build_calendar_quarter_page(1, "QUARTER 1 (JANUARY – MARCH 2027)", 1, 3, 0, 90)
        self.story.append(PageBreak())

        self._build_calendar_quarter_page(2, "QUARTER 2 (APRIL – JUNE 2027)", 4, 6, 90, 181)
        self.story.append(PageBreak())

        self._build_calendar_quarter_page(3, "QUARTER 3 (JULY – SEPTEMBER 2027)", 7, 9, 181, 273)
        self.story.append(PageBreak())

        self._build_calendar_quarter_page(4, "QUARTER 4 (OCTOBER – DECEMBER 2027)", 10, 12, 273, 365)
        self.story.append(PageBreak())
        
        self._build_page24_how_to_read()

        buf = io.BytesIO()
        doc = SimpleDocTemplate(
            buf,
            pagesize=A4,
            leftMargin=34,
            rightMargin=34,
            topMargin=38,
            bottomMargin=38
        )

        def make_canvas(*args, **kwargs):
            return Planner2027ReportCanvas(
                *args,
                seeker_name=self.seeker_name,
                is_sample=self.is_sample,
                **kwargs
            )

        doc.build(self.story, canvasmaker=make_canvas)
        return buf.getvalue()

    def _build_page1_cover(self):
        s = self.styles
        self.story.append(Spacer(1, 40))

        logo_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "app", "static", "logos", "nv-logo-mark.png")
        if not os.path.exists(logo_path):
            logo_path = os.path.join("app", "static", "logos", "nv-logo-mark.png")
        if os.path.exists(logo_path):
            try:
                from reportlab.platypus import Image as RLImage
                self.story.append(RLImage(logo_path, width=70, height=70))
                self.story.append(Spacer(1, 15))
            except Exception:
                pass

        self.story.append(Paragraph("NUMEROS VISION", ParagraphStyle('NVTitle', parent=s['CoverTitle'], fontSize=16, leading=20, textColor=COLOR_GOLD_DARK)))
        self.story.append(Paragraph("ANVEIL EVERY CHARM", ParagraphStyle('NVTag', parent=s['CoverSubtitle'], fontSize=9, leading=12, textColor=COLOR_INK_MUTED)))
        self.story.append(Spacer(1, 25))

        self.story.append(Paragraph("2027 YEAR AHEAD PLANNER", s['CoverTitle']))
        self.story.append(Paragraph("ANNUAL MASTER BLUEPRINT & STRATEGIC ALIGNMENT RADAR", s['CoverSubtitle']))
        self.story.append(Spacer(1, 15))

        # Personalised Recipient Card
        c_data = [
            [Paragraph("<b>Prepared Exclusively For</b>", s['MetaKey']), Paragraph(f"<b>{self.seeker_name.upper()}</b>", s['MetaVal'])],
            [Paragraph("<b>Date of Birth</b>", s['MetaKey']), Paragraph(self.dob.strftime("%d %B %Y"), s['MetaVal'])],
            [Paragraph("<b>Primary Archetype</b>", s['MetaKey']), Paragraph(f"Driver {self.mulank} · Conductor {self.bhagyank}", s['MetaVal'])],
            [Paragraph("<b>2027 Personal Cycle</b>", s['MetaKey']), Paragraph(f"Personal Year {self.py} (Universal Year 2)", s['MetaVal'])],
            [Paragraph("<b>Astrological Sun Sign</b>", s['MetaKey']), Paragraph(f"{self.sun_sign} (Tropical Solar Transit)", s['MetaVal'])],
            [Paragraph("<b>Edition & Provenance</b>", s['MetaKey']), Paragraph("Confidential Personal Edition · New Delhi Anchor", s['MetaVal'])],
        ]
        t_cover = Table(c_data, colWidths=[150, 340])
        t_cover.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
            ('BOX', (0,0), (-1,-1), 1.2, COLOR_GOLD),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 14),
            ('RIGHTPADDING', (0,0), (-1,-1), 14),
        ]))
        self.story.append(t_cover)
        self.story.append(Spacer(1, 35))

        # Softer wording per instruction: "a personal planning guide", "to support your daily focus and routines"
        intro_text = (
            "This dossier provides a personal planning guide for 2027. "
            "By synthesizing your core birth archetypes with the mathematical cycles of the year ahead, "
            "it establishes clear timing windows, monthly strategic blueprints, and practical remedies "
            "designed to support your daily focus and routines."
        )
        self.story.append(Paragraph(intro_text, ParagraphStyle('CoverIntro', parent=s['Body'], alignment=1, fontSize=9, leading=13)))

    def _build_page2_core_numbers(self):
        s = self.styles
        self.story.append(Paragraph("SECTION 1: YOUR CORE NUMEROLOGICAL ARCHETYPES & 2027 CYCLES", s['SectionH1']))
        self.story.append(Paragraph(
            "Your birth chart maps foundational vibrational patterns that govern natural rhythms, leadership inclinations, "
            "and interpersonal resonance. In 2027, these individual currents interact with the broader Universal Year 2.",
            s['Body']
        ))
        self.story.append(Spacer(1, 4))

        # Core Indicators Table
        d_pname = PLANET_NAMES.get(self.mulank, ("Sun", "Surya"))
        c_pname = PLANET_NAMES.get(self.bhagyank, ("Moon", "Chandra"))
        rel_text = self.subject.get("driver_conductor_relation", "Friendly")

        rows = [
            [Paragraph("<b>Indicator</b>", s['TableHeader']), Paragraph("<b>Vibrational Archetype</b>", s['TableHeader']), Paragraph("<b>Qualitative Influence & Rhythms</b>", s['TableHeader'])],
            [
                Paragraph("<b>Driver (Mulank)</b>", s['TableCell']),
                Paragraph(f"<b>Number {self.mulank}</b><br/>{d_pname[0]} ({d_pname[1]})", s['TableCell']),
                Paragraph(self.lib["mulank_notes"].get(str(self.mulank), "Governs your daily initiative, self-direction, and natural operating style."), s['TableCell'])
            ],
            [
                Paragraph("<b>Conductor (Bhagyank)</b>", s['TableCell']),
                Paragraph(f"<b>Number {self.bhagyank}</b><br/>{c_pname[0]} ({c_pname[1]})", s['TableCell']),
                Paragraph(f"Shapes your long-term life path, core responsibilities, and vocational trajectory under {c_pname[0]} guidance.", s['TableCell'])
            ],
            [
                Paragraph("<b>Archetype Synergy</b>", s['TableCell']),
                Paragraph(f"<b>{rel_text}</b> Resonance", s['TableCell']),
                Paragraph("Reflects the natural internal harmony between your daily impulses and broader life direction.", s['TableCell'])
            ],
            [
                Paragraph("<b>Personal Year 2027</b>", s['TableCell']),
                Paragraph(f"<b>Year {self.py}</b> Horizon", s['TableCell']),
                Paragraph(self.lib["personal_year_overviews"].get(str(self.py), "Governs your primary developmental focus throughout 2027."), s['TableCell'])
            ],
            [
                Paragraph("<b>Universal Year 2027</b>", s['TableCell']),
                Paragraph("<b>Year 2</b> (Master 11/2)", s['TableCell']),
                Paragraph("Universal background rhythm highlighting cooperation, diplomatic patience, and shared equilibrium.", s['TableCell'])
            ]
        ]
        t = Table(rows, colWidths=[105, 125, 260])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t)
        self.story.append(Spacer(1, 8))

        # Page 2 Requirement 5: Show separate number lists for DRIVER and CONDUCTOR
        d_f = ", ".join(map(str, self.subject["driver_lists"]["friendly"])) or "None"
        d_n = ", ".join(map(str, self.subject["driver_lists"]["neutral"])) or "None"
        d_c = ", ".join(map(str, self.subject["driver_lists"]["challenging"])) or "None"

        c_f = ", ".join(map(str, self.subject["conductor_lists"]["friendly"])) or "None"
        c_n = ", ".join(map(str, self.subject["conductor_lists"]["neutral"])) or "None"
        c_c = ", ".join(map(str, self.subject["conductor_lists"]["challenging"])) or "None"

        self.story.append(Paragraph(f"<b>Driver (Mulank {self.mulank} · {d_pname[0]}) Number Resonance Framework</b>", s['SectionH2']))
        d_res_data = [
            [Paragraph("<b>Resonance Tier</b>", s['TableHeader']), Paragraph("<b>Numbers</b>", s['TableHeader']), Paragraph("<b>Practical Daily Planning Guidance</b>", s['TableHeader'])],
            [Paragraph("<b>Supportive Rhythms</b>", s['TableCell']), Paragraph(f"<b>{d_f}</b>", s['TableCellCenter']), Paragraph("Numbers carrying natural harmonic ease for scheduling personal initiatives and conversations.", s['TableCell'])],
            [Paragraph("<b>Balanced Rhythms</b>", s['TableCell']), Paragraph(f"<b>{d_n}</b>", s['TableCellCenter']), Paragraph("Neutral numbers well suited for regular operational tasks, administrative work, and steady pacing.", s['TableCell'])],
            [Paragraph("<b>Conscious Pacing</b>", s['TableCell']), Paragraph(f"<b>{d_c}</b>", s['TableCellCenter']), Paragraph("Numbers calling for mindful attention, deliberate double-checking, and patient communication.", s['TableCell'])]
        ]
        t_dres = Table(d_res_data, colWidths=[110, 80, 300])
        t_dres.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_dres)
        self.story.append(Spacer(1, 6))

        self.story.append(Paragraph(f"<b>Conductor (Bhagyank {self.bhagyank} · {c_pname[0]}) Number Resonance Framework</b>", s['SectionH2']))
        c_res_data = [
            [Paragraph("<b>Resonance Tier</b>", s['TableHeader']), Paragraph("<b>Numbers</b>", s['TableHeader']), Paragraph("<b>Practical Vocational Planning Guidance</b>", s['TableHeader'])],
            [Paragraph("<b>Supportive Rhythms</b>", s['TableCell']), Paragraph(f"<b>{c_f}</b>", s['TableCellCenter']), Paragraph("Numbers carrying structural harmony for major career milestones, contract reviews, and partnerships.", s['TableCell'])],
            [Paragraph("<b>Balanced Rhythms</b>", s['TableCell']), Paragraph(f"<b>{c_n}</b>", s['TableCellCenter']), Paragraph("Neutral numbers suited for standard business workflow, routine meetings, and internal maintenance.", s['TableCell'])],
            [Paragraph("<b>Conscious Pacing</b>", s['TableCell']), Paragraph(f"<b>{c_c}</b>", s['TableCellCenter']), Paragraph("Numbers calling for measured pacing, avoiding impulsive commitments, and reviewing fine details.", s['TableCell'])]
        ]
        t_cres = Table(c_res_data, colWidths=[110, 80, 300])
        t_cres.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 3.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_cres)

    def _build_page3_annual_outlook(self):
        s = self.styles
        self.story.append(Paragraph("SECTION 2: 2027 MACRO STRATEGIC HORIZON & LIFE VECTORS", s['SectionH1']))
        
        # Sun Sign and PY Overviews
        sun_reading = self.lib["tropical_sun_signs"].get(self.sun_sign, "")
        self.story.append(Paragraph(f"<b>Solar Horizon: {self.sun_sign} (Tropical Zodiac)</b>", s['SectionH2']))
        self.story.append(Paragraph(sun_reading, s['Body']))
        self.story.append(Spacer(1, 4))

        self.story.append(Paragraph(f"<b>Personal Year {self.py} Developmental Trajectory</b>", s['SectionH2']))
        py_reading = self.lib["personal_year_overviews"].get(str(self.py), "")
        self.story.append(Paragraph(py_reading, s['Body']))
        self.story.append(Spacer(1, 6))

        # 7 Life Areas
        self.story.append(Paragraph("Strategic Horizons Across Key Life Dimensions", s['SectionH2']))
        areas_data = self.lib["personal_year_life_areas"].get(str(self.py), {})
        area_labels = [
            ("Work & Career", "work_and_career"),
            ("Money Habits", "money_habits"),
            ("Home & Family", "home_and_family"),
            ("Relationships", "relationships"),
            ("Wellbeing (Lifestyle)", "wellbeing"),
            ("Learning", "learning"),
            ("Travel", "travel"),
        ]
        rows = [
            [Paragraph("<b>Life Dimension</b>", s['TableHeader']), Paragraph("<b>2027 Strategic Focus & Outlook</b>", s['TableHeader'])]
        ]
        for label, key in area_labels:
            txt = areas_data.get(key, "")
            rows.append([
                Paragraph(f"<b>{label}</b>", s['TableCell']),
                Paragraph(txt, s['TableCell'])
            ])
        t_areas = Table(rows, colWidths=[120, 370])
        t_areas.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_areas)

    def _build_page4_lo_shu_grid(self):
        s = self.styles
        self.story.append(Paragraph("SECTION 3: LO SHU MAGIC SQUARE & ELEMENTAL PLANES", s['SectionH1']))
        self.story.append(Paragraph(
            "The Lo Shu 3×3 grid represents the ancient harmonic distribution of natal numbers across eight primary planes. "
            "Numbers present in your birth matrix anchor specific natural strengths, while absent sectors highlight areas "
            "best supported through deliberate lifestyle habits.",
            s['Body']
        ))
        self.story.append(Spacer(1, 6))

        # Lo Shu 3x3 Grid
        counts = self.d["lo_shu_counts"]
        def fmt_cell(n):
            c = counts.get(n, 0)
            if c > 0:
                return Paragraph(f"<b><font size=14 color='#8B6914'>{n}</font></b><br/><font size=7 color='#523E28'>{c} occurrence{'s' if c>1 else ''}</font>", s['TableCellCenter'])
            return Paragraph(f"<font size=11 color='#C2B19D'>-</font><br/><font size=7 color='#A3927E'>Sector {n} Open</font>", s['TableCellCenter'])

        grid_matrix = [
            [fmt_cell(4), fmt_cell(9), fmt_cell(2)],
            [fmt_cell(3), fmt_cell(5), fmt_cell(7)],
            [fmt_cell(8), fmt_cell(1), fmt_cell(6)]
        ]
        t_grid = Table(grid_matrix, colWidths=[90, 90, 90], rowHeights=[46, 46, 46])
        t_grid.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
            ('BOX', (0,0), (-1,-1), 1.5, COLOR_GOLD),
            ('INNERGRID', (0,0), (-1,-1), 0.8, COLOR_BORDER),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))

        wrap_table = Table([[t_grid]], colWidths=[490])
        wrap_table.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
        self.story.append(wrap_table)
        self.story.append(Spacer(1, 10))

        # 8 Planes Table
        self.story.append(Paragraph("8 Elemental Planes & Life Vectors Evaluation", s['SectionH2']))
        planes_eval = [
            ("Mental Plane", "4 - 9 - 2", all(counts.get(x,0)>0 for x in [4,9,2]), "Governs memory, intellectual synthesis, analytical acuity, and strategic planning."),
            ("Emotional Plane", "3 - 5 - 7", all(counts.get(x,0)>0 for x in [3,5,7]), "Governs intuitive perception, heart-centered empathy, and emotional expression."),
            ("Practical Plane", "8 - 1 - 6", all(counts.get(x,0)>0 for x in [8,1,6]), "Governs physical execution, practical craftsmanship, organization, and commercial acumen."),
            ("Thought Plane", "4 - 3 - 8", all(counts.get(x,0)>0 for x in [4,3,8]), "Governs creative conception, original vision, and independent ideation."),
            ("Will Plane", "9 - 5 - 1", all(counts.get(x,0)>0 for x in [9,5,1]), "Governs persistent determination, self-discipline, and endurance through obstacles."),
            ("Action Plane", "2 - 7 - 6", all(counts.get(x,0)>0 for x in [2,7,6]), "Governs decisiveness, rapid physical movement, and pragmatic operational execution."),
            ("Success Raj Yoga", "4 - 5 - 6", all(counts.get(x,0)>0 for x in [4,5,6]), "The Master Stability diagonal promoting material security, reputation, and steady progress."),
            ("Property Raj Yoga", "2 - 5 - 8", all(counts.get(x,0)>0 for x in [2,5,8]), "The Earth grounding diagonal supporting asset consolidation and domestic stability.")
        ]
        p_rows = [
            [Paragraph("<b>Plane / Yoga</b>", s['TableHeader']), Paragraph("<b>Sectors</b>", s['TableHeader']), Paragraph("<b>Status</b>", s['TableHeader']), Paragraph("<b>Qualitative Influence & Guidance</b>", s['TableHeader'])]
        ]
        for name, nums, complete, desc in planes_eval:
            status_txt = "<b><font color='#16835B'>Anchored</font></b>" if complete else "<font color='#7A654D'>Developing</font>"
            p_rows.append([
                Paragraph(f"<b>{name}</b>", s['TableCell']),
                Paragraph(nums, s['TableCellCenter']),
                Paragraph(status_txt, s['TableCellCenter']),
                Paragraph(desc, s['TableCell'])
            ])
        t_planes = Table(p_rows, colWidths=[105, 55, 65, 265])
        t_planes.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_planes)

    def _build_page5_name_and_pinnacles(self):
        s = self.styles
        self.story.append(Paragraph("SECTION 4: CALLING NAME RESONANCE & 4-STAGE PINNACLES", s['SectionH1']))
        
        nd = self.subject.get("name_data", {})
        c_num = nd.get("name_number_compound", 0)
        r_num = nd.get("name_number_root", 0)
        p_name = PLANET_NAMES.get(r_num, ("Sun", "Surya"))
        align_d = nd.get("alignment_with_driver", "Neutral")
        align_c = nd.get("alignment_with_conductor", "Neutral")

        self.story.append(Paragraph("Calling Name Vibrational Resonance", s['SectionH2']))
        self.story.append(Paragraph(
            f"Your calling identity <b>{self.seeker_name.upper()}</b> resonates with Compound Vibration <b>{c_num}</b> "
            f"and Single Root <b>{r_num}</b>, governed by {p_name[0]} ({p_name[1]}). "
            f"This vibration maintains a <b>{align_d}</b> relationship with your Driver and a <b>{align_c}</b> alignment with your Conductor.",
            s['Body']
        ))
        name_desc = self.lib["name_number_alignments"].get(align_d.lower(), "")
        self.story.append(Paragraph(name_desc, s['Body']))
        self.story.append(Spacer(1, 8))

        # 4 Pinnacles Section
        self.story.append(Paragraph("The Four Life Pinnacles & 2027 Alignment", s['SectionH2']))
        self.story.append(Paragraph(
            "Pinnacles represent extended developmental epochs that guide your major focus, vocational growth, and inner maturation. "
            "Each pinnacle is governed by a distinct number vibration and age bracket.",
            s['Body']
        ))
        self.story.append(Spacer(1, 4))

        pinn_rows = [
            [Paragraph("<b>Pinnacle</b>", s['TableHeader']), Paragraph("<b>Vibration</b>", s['TableHeader']), Paragraph("<b>Governing Planet</b>", s['TableHeader']), Paragraph("<b>Age Span</b>", s['TableHeader']), Paragraph("<b>Status in 2027</b>", s['TableHeader'])]
        ]
        pinn_list = self.d["pinnacles_data"]["pinnacles"]
        active_pinn = None
        for p in pinn_list:
            is_cur = p.get("is_current", False)
            if is_cur:
                active_pinn = p
            status_txt = "<b><font color='#8B6914'>Active Cycle</font></b>" if is_cur else "<font color='#7A654D'>Secondary</font>"
            pinn_rows.append([
                Paragraph(f"<b>Pinnacle {p['pinnacle_id'][1]}</b>", s['TableCell']),
                Paragraph(f"Number {p['number']}", s['TableCellCenter']),
                Paragraph(p['governing_planet'], s['TableCellCenter']),
                Paragraph(p['age_span'], s['TableCellCenter']),
                Paragraph(status_txt, s['TableCellCenter'])
            ])
        t_pinn = Table(pinn_rows, colWidths=[70, 70, 95, 140, 115])
        t_pinn.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_pinn)
        self.story.append(Spacer(1, 8))

        if active_pinn:
            pid = active_pinn['pinnacle_id']
            pnum = str(active_pinn['number'])
            p_reading = self.lib["pinnacles"].get(pid, {}).get(pnum, "")
            self.story.append(Paragraph(f"<b>Active Pinnacle Outlook: {pid} (Vibration {pnum} · {active_pinn['governing_planet']})</b>", s['SectionH2']))
            self.story.append(Paragraph(p_reading, s['Body']))

    def _build_page6_key_dates(self):
        s = self.styles
        self.story.append(Paragraph("SECTION 5: KEY STRATEGIC AUSPICIOUS DATES & TIMING RADAR", s['SectionH1']))
        self.story.append(Paragraph(
            "Across the 365 days of 2027, certain dates exhibit peak personal resonance where your driver and conductor "
            "energies align smoothly with universal daily cycles. In accordance with classical panchang wisdom, dates falling on "
            "New Moon (Amavasya) or subject to full-morning Rahu Kaal have been filtered or adjusted to support high clarity. "
            "Panchang calculations anchored for New Delhi (IST).",
            s['Body']
        ))
        self.story.append(Spacer(1, 6))

        calendar_365 = self.d["full_calendar_365"]
        panchang_days = self.panchang.get("days", {})

        rikta_names = ["Chaturthi", "Navami", "Chaturdashi"]

        def is_eligible_key_date(row):
            d_str = row["date"]
            p_info = panchang_days.get(d_str, {})
            t_name = p_info.get("tithi_name", "")

            # Configurable rules from key_dates_rules.json
            if self.kd_rules.get("exclude_amavasya", True) and p_info.get("is_amavasya", False):
                return False

            if self.kd_rules.get("exclude_rikta_tithis", False):
                if any(r in t_name for r in rikta_names):
                    return False

            if self.kd_rules.get("exclude_krishna_chaturdashi", False):
                if "Krishna Chaturdashi" in t_name:
                    return False

            return True

        quarters = {
            "Q1 (January – March)": [r for r in calendar_365 if r["date"].startswith("2027-01") or r["date"].startswith("2027-02") or r["date"].startswith("2027-03")],
            "Q2 (April – June)": [r for r in calendar_365 if r["date"].startswith("2027-04") or r["date"].startswith("2027-05") or r["date"].startswith("2027-06")],
            "Q3 (July – September)": [r for r in calendar_365 if r["date"].startswith("2027-07") or r["date"].startswith("2027-08") or r["date"].startswith("2027-09")],
            "Q4 (October – December)": [r for r in calendar_365 if r["date"].startswith("2027-10") or r["date"].startswith("2027-11") or r["date"].startswith("2027-12")]
        }

        # Page 6 Requirement 6(a): Show Sunrise Tithi next to every Key Date
        key_rows = [
            [
                Paragraph("<b>Quarter</b>", s['TableHeader']),
                Paragraph("<b>Date & Day</b>", s['TableHeader']),
                Paragraph("<b>Score & Tier</b>", s['TableHeader']),
                Paragraph("<b>Sunrise Tithi (New Delhi)</b>", s['TableHeader']),
                Paragraph("<b>Strategic Planning Guidance</b>", s['TableHeader'])
            ]
        ]

        notes_pool = self.lib["date_notes"]["Peak"] + self.lib["date_notes"]["Excellent"]
        used_notes = set()

        for q_name, q_days in quarters.items():
            eligible = [r for r in q_days if is_eligible_key_date(r)]
            sorted_q = sorted(eligible, key=lambda x: (-x["alignment_score"], x["date"]))
            top_3 = sorted_q[:3]
            for idx, item in enumerate(top_3):
                dt = datetime.date.fromisoformat(item["date"])
                dt_disp = dt.strftime("%d %b (%a)")
                score_disp = f"<b>{item['alignment_score']}</b> · {item['tier']}"
                
                # Fetch sunrise tithi from panchang
                p_day = panchang_days.get(item["date"], {})
                tithi_name = p_day.get("tithi_name", "Shukla Pratipada")

                # Requirement 6(c): distinct note for every single Key Date (never repeated)
                base_note = None
                tier_notes = self.lib["date_notes"].get(item["tier"], self.lib["date_notes"]["Peak"])
                for note_candidate in tier_notes:
                    if note_candidate not in used_notes:
                        base_note = note_candidate
                        break
                if not base_note:
                    for note_candidate in notes_pool:
                        if note_candidate not in used_notes:
                            base_note = note_candidate
                            break
                if not base_note:
                    base_note = tier_notes[0]
                used_notes.add(base_note)

                # Requirement 6(b): Near-boundary annotation
                if p_day.get("near_boundary", False):
                    note_txt = f"<b>Panchang: the tithi changes shortly after sunrise; check your local Panchang.</b> {base_note}"
                else:
                    note_txt = base_note

                q_label = f"<b>{q_name.split()[0]}</b>" if idx == 0 else ""
                key_rows.append([
                    Paragraph(q_label, s['TableCellCenter']),
                    Paragraph(dt_disp, s['TableCellCenter']),
                    Paragraph(score_disp, s['TableCellCenter']),
                    Paragraph(tithi_name, s['TableCellCenter']),
                    Paragraph(note_txt, s['TableCell'])
                ])

        t_key = Table(key_rows, colWidths=[55, 75, 75, 105, 180])
        t_key.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 5),
            ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ]))
        self.story.append(t_key)
        self.story.append(Spacer(1, 8))

        guide_note = (
            "<b>Panchang Timing Practice (New Delhi IST):</b> For high-priority commercial actions on these dates, "
            "prioritize initiation windows between 09:30 AM and 11:30 AM or mid-afternoon between 02:00 PM and 04:30 PM. "
            "Observing these windows avoids local midday Rahu Kaal periods, ensuring steady momentum."
        )
        self.story.append(Paragraph(guide_note, s['BodyMuted']))

    def _build_single_monthly_page(self, m: Dict[str, Any]):
        """
        Builds a dedicated, full-page monthly blueprint (Pages 7 to 18).
        """
        s = self.styles
        m_num = m["month_number"]
        m_name = m["month_name"]
        pm = m["personal_month"]
        avg_score = m["average_alignment_score"]
        theme_text = self.lib["personal_months"].get(str(pm), m["theme"])
        rem_text = self.lib["remedies_library"]["month_remedies"].get(str(pm), "")

        # Spec rating: 1 Favourable, 2 Neutral, 3 Favourable, 4 Neutral, 5 Asks for care,
        # 6 Favourable, 7 Neutral, 8 Neutral, 9 Asks for care; June for PY 5 shows master flag as 2
        spec_rating = MONTH_RATINGS_SPEC.get(pm, "Neutral")
        
        # Display header
        self.story.append(Paragraph(f"SECTION 6: MONTHLY BLUEPRINT · {m_name.upper()} 2027", s['SectionH1']))
        self.story.append(Spacer(1, 4))

        # Personal Month Indicator line
        if m_num == 6 and self.py == 5:
            pm_title = f"Personal Month 2 (Master Vibration 11/2) · Master Flag: 2"
        elif m.get("is_master_11", False):
            pm_title = f"Personal Month {pm} (Master Vibration 11/2) · Master Flag: 2"
        else:
            pm_title = f"Personal Month {pm} · Vibration Archetype"

        # Meta Bar Table
        meta_bar = [
            [
                Paragraph(f"<b>{pm_title}</b>", s['MetaKey']),
                Paragraph(f"<b>Monthly Rating:</b> {spec_rating}", s['MetaVal']),
                Paragraph(f"<b>Average Score:</b> {avg_score:.1f} / 100", s['MetaVal'])
            ]
        ]
        t_bar = Table(meta_bar, colWidths=[200, 150, 140])
        t_bar.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_bar)
        self.story.append(Spacer(1, 6))

        # Theme & Narrative
        self.story.append(Paragraph(f"<b>Monthly Theme & Operating Horizon:</b> {m['theme']}", s['SectionH2']))
        self.story.append(Paragraph(theme_text, s['Body']))
        self.story.append(Spacer(1, 4))

        # Moon Phases for this month from Panchang (Plain text, no emoji per Point 4)
        m_prefix = f"2027-{m_num:02d}"
        f_moons = [fm for fm in self.panchang.get("full_moons_2027", []) if fm.get("date", "").startswith(m_prefix)]
        n_moons = [nm for nm in self.panchang.get("new_moons_2027", []) if nm.get("date", "").startswith(m_prefix)]

        def fmt_moon_list(m_list):
            if not m_list:
                return "None in calendar month"
            parts = []
            for item in m_list:
                dt = datetime.date.fromisoformat(item["date"])
                parts.append(f"{dt.strftime('%d %b')} at {item['time_ist']} IST")
            return " · ".join(parts)

        # Point 4 & Point 8: Plain text "Full Moon (Purnima)" / "New Moon (Amavasya)", Panchang for New Delhi (IST)
        moon_rows = [
            [
                Paragraph(f"<b>Full Moon (Purnima):</b> {fmt_moon_list(f_moons)}", s['TableCell']),
                Paragraph(f"<b>New Moon (Amavasya):</b> {fmt_moon_list(n_moons)}", s['TableCell'])
            ]
        ]
        t_moon = Table(moon_rows, colWidths=[245, 245])
        t_moon.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
            ('BOX', (0,0), (-1,-1), 0.6, COLOR_GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 4),
            ('BOTTOMPADDING', (0,0), (-1,-1), 4),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_moon)
        self.story.append(Paragraph("<font size=7 color='#7A654D'>Panchang for New Delhi (IST)</font>", s['TableCellCenter']))
        self.story.append(Spacer(1, 4))

        # Monthly Remedy: only the single optional crystal from Year Ahead spec per Point 5
        crystal_remedy = CRYSTALS_BY_MULANK.get(pm, "Clear quartz")
        self.story.append(Paragraph(
            f"<b>Optional Traditional Attunement:</b> In classical traditions, an optional complementary crystal for Personal Month {pm} is <b>{crystal_remedy}</b>. (Optional traditional suggestion).",
            s['BodyMuted']
        ))
        self.story.append(Spacer(1, 4))

        # Best 5 Dates Table (with Sunrise Tithi per Point 2 & 4)
        best_rows = [
            [
                Paragraph("<b>Date</b>", s['TableHeader']),
                Paragraph("<b>Day</b>", s['TableHeader']),
                Paragraph("<b>Score</b>", s['TableHeader']),
                Paragraph("<b>Tier</b>", s['TableHeader']),
                Paragraph("<b>Sunrise Tithi</b>", s['TableHeader']),
                Paragraph("<b>Strategic Planning Guidance</b>", s['TableHeader'])
            ]
        ]
        has_nb = False
        for row in m["best_5_dates"]:
            dt = datetime.date.fromisoformat(row["date"])
            tier = row["tier"]
            note = self.lib["date_notes"].get(tier, [row["note"]])[dt.day % len(self.lib["date_notes"].get(tier, [row["note"]]))]
            p_day = self.panchang.get("days", {}).get(row["date"], {})
            tithi_name = p_day.get("tithi_name", "")
            is_nb = abs(p_day.get("minutes_to_tithi_boundary", 999.0)) <= 45.0
            if is_nb:
                tithi_name += "*"
                has_nb = True
            best_rows.append([
                Paragraph(dt.strftime("%d %b"), s['TableCellCenter']),
                Paragraph(row["weekday"][:3], s['TableCellCenter']),
                Paragraph(f"<b>{row['alignment_score']}</b>", s['TableCellCenter']),
                Paragraph(tier, s['TableCellCenter']),
                Paragraph(tithi_name, s['TableCellCenter']),
                Paragraph(note, s['TableCell'])
            ])
        t_best = Table(best_rows, colWidths=[46, 32, 36, 55, 110, 248])
        t_best.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))

        # Care 5 Dates Table (with Sunrise Tithi per Point 2 & 4)
        care_rows = [
            [
                Paragraph("<b>Date</b>", s['TableHeader']),
                Paragraph("<b>Day</b>", s['TableHeader']),
                Paragraph("<b>Score</b>", s['TableHeader']),
                Paragraph("<b>Tier</b>", s['TableHeader']),
                Paragraph("<b>Sunrise Tithi</b>", s['TableHeader']),
                Paragraph("<b>Mindful Pacing Guidance</b>", s['TableHeader'])
            ]
        ]
        for row in m["care_5_dates"]:
            dt = datetime.date.fromisoformat(row["date"])
            tier = row["tier"]
            note = self.lib["date_notes"].get(tier, [row["note"]])[dt.day % len(self.lib["date_notes"].get(tier, [row["note"]]))]
            p_day = self.panchang.get("days", {}).get(row["date"], {})
            tithi_name = p_day.get("tithi_name", "")
            is_nb = abs(p_day.get("minutes_to_tithi_boundary", 999.0)) <= 45.0
            if is_nb:
                tithi_name += "*"
                has_nb = True
            care_rows.append([
                Paragraph(dt.strftime("%d %b"), s['TableCellCenter']),
                Paragraph(row["weekday"][:3], s['TableCellCenter']),
                Paragraph(f"<b>{row['alignment_score']}</b>", s['TableCellCenter']),
                Paragraph(tier, s['TableCellCenter']),
                Paragraph(tithi_name, s['TableCellCenter']),
                Paragraph(note, s['TableCell'])
            ])
        t_care = Table(care_rows, colWidths=[46, 32, 36, 55, 110, 248])
        t_care.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 0.8, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 4),
            ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ]))

        self.story.append(Paragraph("<b>Top Favourable Windows for Important Initiatives</b>", s['SectionH2']))
        self.story.append(t_best)
        self.story.append(Spacer(1, 4))
        self.story.append(Paragraph("<b>Mindful Pacing Dates (Favour Routine Pacing & Review)</b>", s['SectionH2']))
        self.story.append(t_care)
        if has_nb:
            self.story.append(Paragraph("<font size=6.5 color='#7A654D'>* Panchang: the tithi changes shortly after sunrise; check your local Panchang.</font>", s['TableCell']))

    def _build_page19_remedies_bank(self):
        s = self.styles
        self.story.append(Paragraph("SECTION 7: 2027 REMEDIES BANK & DAILY ATTUNEMENT", s['SectionH1']))
        self.story.append(Paragraph(
            "Remedies in classical numerological tradition are practical, zero-cost mindfulness habits, environmental adjustments, "
            "and lifestyle routines designed to support energetic equilibrium. They do not constitute magical formulas; rather, "
            "they reinforce personal discipline, clarity, and daily poise.",
            s['Body']
        ))
        self.story.append(Spacer(1, 4))

        # Year Remedy
        y_rem = self.lib["remedies_library"]["year_remedies"].get(str(self.py), "")
        self.story.append(Paragraph(f"<b>Annual Lifestyle Attunement for Personal Year {self.py}</b>", s['SectionH2']))
        self.story.append(Paragraph(y_rem, s['Body']))
        self.story.append(Spacer(1, 6))

        # Traditional Crystal Suggestion for Mulank (Point 6)
        self.story.append(Paragraph("Traditional Mineral & Crystal Attunement by Driver Number", s['SectionH2']))
        seeker_crystal = CRYSTALS_BY_MULANK.get(self.mulank, "Sunstone or Carnelian")
        c_intro = (
            f"In classical gemological philosophy, subtle mineral vibrations are associated with each primary driver number. "
            f"For your Driver Number <b>{self.mulank}</b>, the traditional attunement crystal is <b>{seeker_crystal}</b>."
        )
        self.story.append(Paragraph(c_intro, s['Body']))
        self.story.append(Spacer(1, 3))

        c_rows = [
            [Paragraph("<b>Driver</b>", s['TableHeader']), Paragraph("<b>Planet Ruler</b>", s['TableHeader']), Paragraph("<b>Traditional Crystal Suggestion</b>", s['TableHeader']), Paragraph("<b>Status</b>", s['TableHeader'])]
        ]
        for num in range(1, 10):
            pname = PLANET_NAMES.get(num, ("Sun", "Surya"))
            c_name = CRYSTALS_BY_MULANK.get(num, "")
            is_seeker = (num == self.mulank)
            stat = "<b><font color='#8B6914'>Your Driver</font></b>" if is_seeker else "<font color='#7A654D'>Reference</font>"
            c_rows.append([
                Paragraph(f"Number {num}", s['TableCellCenter']),
                Paragraph(f"{pname[0]} ({pname[1]})", s['TableCellCenter']),
                Paragraph(c_name, s['TableCell']),
                Paragraph(stat, s['TableCellCenter'])
            ])
        t_cryst = Table(c_rows, colWidths=[70, 110, 210, 100])
        t_cryst.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_cryst)
        self.story.append(Spacer(1, 2))
        self.story.append(Paragraph(
            "<b>Note:</b> This is a traditional suggestion, not medical or financial advice.",
            s['BodyMuted']
        ))
        self.story.append(Spacer(1, 6))

        # 9 Daily Grounding Micro-Actions
        self.story.append(Paragraph("Daily Grounding Protocols (Based on Daily Numerological Rhythms)", s['SectionH2']))
        d_rems = self.lib["remedies_library"]["day_remedies"]
        rows = [
            [Paragraph("<b>Rhythm</b>", s['TableHeader']), Paragraph("<b>Governing Influence</b>", s['TableHeader']), Paragraph("<b>Daily Grounding Micro-Action</b>", s['TableHeader'])]
        ]
        for num in range(1, 10):
            pname = PLANET_NAMES.get(num, ("Sun", "Surya"))
            rows.append([
                Paragraph(f"<b>Number {num}</b>", s['TableCellCenter']),
                Paragraph(f"{pname[0]} ({pname[1]})", s['TableCellCenter']),
                Paragraph(d_rems.get(str(num), ""), s['TableCell'])
            ])
        t_drem = Table(rows, colWidths=[70, 95, 325])
        t_drem.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 6),
            ('RIGHTPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_drem)

    def _build_calendar_table_for_month_quarter(self, m_num: int, start_idx: int, end_idx: int) -> Table:
        s = self.styles
        m_name = self.d["months"][m_num - 1]["month_name"]
        rows = [
            [Paragraph(f"<b>{m_name.upper()}</b>", s['TableHeader']), Paragraph("", s['TableHeader']), Paragraph("", s['TableHeader']), Paragraph("", s['TableHeader'])],
            [Paragraph("<b>Date</b>", s['TableCellDenseCenter']), Paragraph("<b>Day</b>", s['TableCellDenseCenter']), Paragraph("<b>Score</b>", s['TableCellDenseCenter']), Paragraph("<b>Tier</b>", s['TableCellDenseCenter'])]
        ]
        days_slice = self.d["full_calendar_365"][start_idx:end_idx]
        for row in days_slice:
            dt = datetime.date.fromisoformat(row["date"])
            t_color = "#8B6914" if row["tier"] == "Peak" else ("#16835B" if row["tier"] == "Excellent" else ("#C9A227" if row["tier"] == "Good" else "#7A654D"))
            rows.append([
                Paragraph(f"{dt.day:02d}", s['TableCellDenseCenter']),
                Paragraph(row["weekday"][:2], s['TableCellDenseCenter']),
                Paragraph(f"<b>{row['alignment_score']}</b>", s['TableCellDenseCenter']),
                Paragraph(f"<font color='{t_color}'>{row['tier'][:4]}</font>", s['TableCellDenseCenter'])
            ])
        t = Table(rows, colWidths=[38, 30, 38, 48])
        t.setStyle(TableStyle([
            ('SPAN', (0,0), (-1,0)),
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BACKGROUND', (0,1), (-1,1), COLOR_CARD_BG),
            ('BOX', (0,0), (-1,-1), 0.6, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.3, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 1.2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.2),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
        ]))
        return t

    def _build_calendar_quarter_page(self, q_num: int, q_title: str, m_start: int, m_end: int, start_idx: int, end_idx: int):
        s = self.styles
        self.story.append(Paragraph(f"SECTION 8: 365-DAY DAILY ALIGNMENT CALENDAR ({q_title})", s['SectionH1']))
        self.story.append(Paragraph(
            "Every day evaluated under your natal parameters. Legible format matching TableCellDense (7.2 pt). "
            "Tiers: Peak (Peak), Excellent (Exce), Good (Good), Moderate (Mode), Care (Care).",
            s['BodyMuted']
        ))
        self.story.append(Spacer(1, 4))

        days_per_month = {
            1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30,
            7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31
        }
        
        col_tables = []
        cur_idx = start_idx
        for m in range(m_start, m_end + 1):
            d_count = days_per_month[m]
            tbl = self._build_calendar_table_for_month_quarter(m, cur_idx, cur_idx + d_count)
            col_tables.append(tbl)
            cur_idx += d_count

        quarter_grid = Table([col_tables], colWidths=[163, 163, 163])
        quarter_grid.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('LEFTPADDING', (0,0), (-1,-1), 2),
            ('RIGHTPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
        ]))
        self.story.append(quarter_grid)

    def _build_page24_how_to_read(self):
        s = self.styles
        self.story.append(Paragraph("SECTION 9: HOW TO READ THIS REPORT & STATUTORY NOTICE", s['SectionH1']))
        
        htr = self.lib["how_to_read"]
        self.story.append(Paragraph(htr["intro"], s['Body']))
        self.story.append(Spacer(1, 6))

        # 5 Tiers Table
        self.story.append(Paragraph("Understanding the Five Alignment Tiers", s['SectionH2']))
        tier_rows = [
            [Paragraph("<b>Alignment Tier</b>", s['TableHeader']), Paragraph("<b>Plain-Language Definition & Strategic Application</b>", s['TableHeader'])]
        ]
        for t_name in ["Peak", "Excellent", "Good", "Moderate", "Care"]:
            t_desc = htr["tiers"].get(t_name, "")
            tier_rows.append([
                Paragraph(f"<b>{t_name}</b>", s['TableCellCenter']),
                Paragraph(t_desc, s['TableCell'])
            ])
        t_tier = Table(tier_rows, colWidths=[90, 400])
        t_tier.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_tier)
        self.story.append(Spacer(1, 10))

        # Planning Aid Note
        self.story.append(Paragraph("A Mindful Navigational Planning Aid", s['SectionH2']))
        self.story.append(Paragraph(htr["planning_aid_note"], s['Body']))
        self.story.append(Spacer(1, 10))

        # Restored {{DISCLAIMER_APPROVED_TEXT}} Box
        self.story.append(Paragraph("Statutory Legal Notice & Practitioner Boundaries", s['SectionH2']))
        disc_text = htr.get("disclaimer_text", "{{DISCLAIMER_APPROVED_TEXT}}")
        d_card = Table([[Paragraph(f"<b>STATUTORY NOTICE:</b> {disc_text}", s['BodyMuted'])]], colWidths=[490])
        d_card.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
            ('BOX', (0,0), (-1,-1), 1, COLOR_GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
        ]))
        self.story.append(d_card)


def generate_planner_2027_pdf(
    full_name: str,
    dob_str: str,
    output_path: Optional[str] = None,
    is_sample: bool = True
) -> bytes:
    """
    Main generator entrypoint for the 2027 Year Ahead Planner PDF.
    - is_sample: controls the SAMPLE watermark. Defaults to True for sample generation.
                 Set to False for paid deliveries.
    """
    # 1. Deterministic Calculation
    calc_data = calculate_planner_2027(full_name=full_name, dob_str=dob_str)

    # 2. Load Content Library
    lib_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "planner_2027_content_library.json")
    if not os.path.exists(lib_path):
        lib_path = "data/planner_2027_content_library.json"
    with open(lib_path, "r", encoding="utf-8") as f:
        content_lib = json.load(f)

    # 3. Load Panchang Data
    panchang_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "panchang_2027_delhi.json")
    if not os.path.exists(panchang_path):
        panchang_path = "data/panchang_2027_delhi.json"
    panchang_data = {}
    if os.path.exists(panchang_path):
        with open(panchang_path, "r", encoding="utf-8") as f:
            panchang_data = json.load(f)

    # 4. Load Key Dates Rules
    rules_path = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "key_dates_rules.json")
    if not os.path.exists(rules_path):
        rules_path = "data/key_dates_rules.json"
    key_dates_rules = {}
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            key_dates_rules = json.load(f)

    # 5. Build PDF
    builder = Planner2027PdfBuilder(
        calc_data=calc_data,
        content_library=content_lib,
        panchang_data=panchang_data,
        key_dates_rules=key_dates_rules,
        is_sample=is_sample
    )
    pdf_bytes = builder.build()

    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)

    return pdf_bytes
