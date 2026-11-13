import sys
import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfgen import canvas
import pypdf

COLOR_PEARL_BG   = colors.HexColor("#FFFDF7")
COLOR_PEARL_MID  = colors.HexColor("#F7F3EA")
COLOR_GOLD_DARK  = colors.HexColor("#8B6914")
COLOR_GOLD       = colors.HexColor("#C9A227")
COLOR_GOLD_LIGHT = colors.HexColor("#E2B84B")
COLOR_INK_DARK   = colors.HexColor("#523E28")
COLOR_INK_MUTED  = colors.HexColor("#7A654D")
COLOR_EMERALD    = colors.HexColor("#16835B")
COLOR_BORDER     = colors.HexColor("#EEDDB8")
COLOR_RED_ALERT  = colors.HexColor("#A13030")

styles = getSampleStyleSheet()

class CustomCanvas(canvas.Canvas):
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, total_pages: int):
        self.saveState()
        w, h = self._pagesize

        # Background
        self.setFillColor(COLOR_PEARL_BG)
        self.rect(0, 0, w, h, fill=1, stroke=0)

        # Double Gold Border Frame
        self.setStrokeColor(COLOR_GOLD)
        self.setLineWidth(1.2)
        self.rect(20, 20, w - 40, h - 40, stroke=1, fill=0)

        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.rect(23, 23, w - 46, h - 46, stroke=1, fill=0)

        # Header
        self.setFont("Times-Bold", 8)
        self.setFillColor(COLOR_GOLD_DARK)
        self.drawString(34, h - 28, "NUMEROS VISION")
        self.setFont("Times-Italic", 7.5)
        self.setFillColor(COLOR_INK_MUTED)
        self.drawString(120, h - 28, "·   ANVEIL EVERY CHARM")

        self.setFont("Times-Roman", 7.5)
        self.setFillColor(COLOR_EMERALD)
        if self._pageNumber == 1:
            self.drawRightString(w - 34, h - 28, "FREE DISCOVERY BLUEPRINT · PAGE 1 · FOUNDATIONAL PROFILE")
        elif self._pageNumber == 2:
            self.drawRightString(w - 34, h - 28, "FORMAT 1 · PAGE 2 · 8 ELEMENTAL PLANES & RAJ YOGAS (LOCKED)")
        else:
            self.drawRightString(w - 34, h - 28, "FORMAT 1 · PAGE 3 · KARMIC MISSING DIGITS & REMEDIES (LOCKED)")

        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(34, h - 33, w - 34, h - 33)

        # Watermark
        cx, cy = w / 2.0, h / 2.0
        self.saveState()
        self.setFont("Times-Bold", 26)
        self.setFillColor(colors.Color(0.79, 0.64, 0.15, alpha=0.045))
        self.drawCentredString(cx, cy + 20, "NUMEROS VISION")
        self.setFont("Times-Roman", 16)
        self.drawCentredString(cx, cy - 10, "ANVEIL EVERY CHARM")
        self.restoreState()

        # Footer
        self.setStrokeColor(COLOR_BORDER)
        self.setLineWidth(0.6)
        self.line(34, 38, w - 34, 38)

        self.setFont("Times-Roman", 7.5)
        self.setFillColor(COLOR_INK_MUTED)
        self.drawString(34, 26, "Numeros Vision — ANVEIL EVERY CHARM")

        self.setFont("Times-Bold", 8)
        self.setFillColor(COLOR_GOLD_DARK)
        self.drawCentredString(w / 2.0, 26, "✦ VERIFIED ROYAL SEAL ✦")

        self.drawRightString(w - 34, 26, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()


doc = SimpleDocTemplate(
    'test_fmt1_output.pdf',
    pagesize=A4,
    leftMargin=34,
    rightMargin=34,
    topMargin=36,
    bottomMargin=42
)

story = []

# Styles
s_top_star = ParagraphStyle('TopStar', parent=styles['Normal'], fontName='Times-Bold', fontSize=8.5, leading=11, textColor=COLOR_GOLD_DARK, alignment=1)
s_name = ParagraphStyle('Name', parent=styles['Normal'], fontName='Times-Bold', fontSize=22, leading=26, textColor=COLOR_GOLD_DARK, alignment=1)
s_sub = ParagraphStyle('Sub', parent=styles['Normal'], fontName='Times-Roman', fontSize=10, leading=13, textColor=COLOR_INK_DARK, alignment=1)

s_pill_lbl = ParagraphStyle('PillLbl', parent=styles['Normal'], fontName='Times-Roman', fontSize=7, leading=9, textColor=COLOR_INK_MUTED, alignment=1)
s_pill_val = ParagraphStyle('PillVal', parent=styles['Normal'], fontName='Times-Bold', fontSize=10, leading=12, textColor=COLOR_EMERALD, alignment=1)

s_card_h = ParagraphStyle('CardH', parent=styles['Normal'], fontName='Times-Bold', fontSize=8.5, leading=11, textColor=COLOR_GOLD_DARK)
s_card_txt = ParagraphStyle('CardTxt', parent=styles['Normal'], fontName='Times-Roman', fontSize=8, leading=11, textColor=COLOR_INK_DARK)

s_cell_gap = ParagraphStyle('CellGap', parent=styles['Normal'], fontName='Times-Bold', fontSize=7.5, leading=9, textColor=COLOR_RED_ALERT, alignment=1)
s_cell_num = ParagraphStyle('CellNum', parent=styles['Normal'], fontName='Times-Bold', fontSize=11, leading=13, textColor=COLOR_INK_DARK, alignment=1)
s_cell_sub = ParagraphStyle('CellSub', parent=styles['Normal'], fontName='Times-Roman', fontSize=7, leading=8.5, textColor=COLOR_INK_MUTED, alignment=1)

s_gap_item = ParagraphStyle('GapItem', parent=styles['Normal'], fontName='Times-Roman', fontSize=7.5, leading=10.5, textColor=COLOR_INK_DARK)
s_alert = ParagraphStyle('Alert', parent=styles['Normal'], fontName='Times-Bold', fontSize=7.5, leading=10, textColor=COLOR_RED_ALERT)

# ── PAGE 1 ────────────────────────────────────────────────────────────────
story.append(Paragraph("✦ FREE CELESTIAL DISCOVERY BLUEPRINT ✦", s_top_star))
story.append(Spacer(1, 2))
story.append(Paragraph("ALEXANDER VANCE", s_name))
story.append(Spacer(1, 2))
story.append(Paragraph("Foundational Planetary Frequency &amp; Lo Shu Grid Matrix", s_sub))
story.append(Spacer(1, 6))

# 4 Metric Pills
pills_data = [
    [
        Paragraph("PSYCHIC (MULANK)<br/><font size=10 color='#16835B'><b>9 · MARS</b></font>", s_pill_lbl),
        Paragraph("DESTINY (BHAGYANK)<br/><font size=10 color='#16835B'><b>2 · MOON</b></font>", s_pill_lbl),
        Paragraph("COSMIC VECTOR<br/><font size=10 color='#16835B'><b>9 (EAST GROUP)</b></font>", s_pill_lbl),
        Paragraph("CALLING NAME<br/><font size=10 color='#16835B'><b>6 (51)</b></font>", s_pill_lbl),
    ]
]
t_pills = Table(pills_data, colWidths=[130, 130, 130, 130], rowHeights=[32])
t_pills.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
    ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
]))
story.append(t_pills)
story.append(Spacer(1, 5))

# Verified Coordinates Box
coords_data = [
    [
        Paragraph("<b>Full Name:</b> Alexander Vance", s_card_txt),
        Paragraph("<b>Date of Birth:</b> 1990-10-18", s_card_txt),
        Paragraph("<b>Day Number:</b> Day 18", s_card_txt),
        Paragraph("<b>Cosmic Archetype:</b> Mars Leadership", s_card_txt),
    ],
    [
        Paragraph("<b>Access Level:</b> Free Discovery Tier", s_card_txt),
        Paragraph("", s_card_txt),
        Paragraph("", s_card_txt),
        Paragraph("", s_card_txt),
    ]
]
t_coords = Table(
    [[Paragraph("<b>✦ VERIFIED CHART COORDINATES</b>", s_card_h)],
     [Table(coords_data, colWidths=[125, 125, 125, 125])]],
    colWidths=[520]
)
t_coords.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), COLOR_PEARL_BG),
    ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
    ('TOPPADDING', (0,0), (-1,-1), 3),
    ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_coords)
story.append(Spacer(1, 5))

# Centered Lo Shu Grid
story.append(Paragraph("<font size=9 color='#8B6914'><b>NATAL LO SHU 3×3 GRID &amp; ELEMENTAL FREQUENCIES</b></font>", s_top_star))
story.append(Spacer(1, 3))

def ls_cell(badge, num, elem, is_gap=False):
    col = '#A13030' if is_gap else '#16835B'
    bg = COLOR_PEARL_MID if is_gap else colors.white
    return Paragraph(f"<font size=7 color='{col}'><b>{badge}</b></font><br/><font size=11 color='#523E28'><b>{num}</b></font><br/><font size=6.5 color='#7A654D'>{elem}</font>", s_cell_sub)

grid_rows = [
    [ls_cell("GAP", "4", "Wood", True), ls_cell("×2", "99", "Fire", False), ls_cell("GAP", "2", "Earth", True)],
    [ls_cell("GAP", "3", "Wood", True), ls_cell("GAP", "5", "Earth", True), ls_cell("GAP", "7", "Metal", True)],
    [ls_cell("×1", "8", "Earth", False), ls_cell("×3", "111", "Water", False), ls_cell("GAP", "6", "Metal", True)]
]
t_loshu = Table(grid_rows, colWidths=[70, 70, 70], rowHeights=[36, 36, 36], hAlign='CENTER')
t_loshu.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ('BOX', (0,0), (-1,-1), 1.2, COLOR_GOLD),
    ('INNERGRID', (0,0), (-1,-1), 0.6, COLOR_BORDER),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('TOPPADDING', (0,0), (-1,-1), 2),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2),
]))
story.append(t_loshu)
story.append(Spacer(1, 5))

# Natal Gap Analysis Card
gap_items = [
    Paragraph("<b>✦ Missing 2 (Moon):</b> Missing 2 (Earth · Moon Intuition): Emotional impatience; relationship friction; feeling ungrounded in team dynamics.", s_gap_item),
    Paragraph("<b>✦ Missing 3 (Jupiter):</b> Missing 3 (Wood · Jupiter Knowledge): Creative stagnation; public expression hesitation; under-leveraging personal expertise.", s_gap_item),
    Paragraph("<b>✦ Missing 4 (Rahu):</b> Missing 4 (Wood · Rahu Vault &amp; Discipline): Structural wealth leak; high revenue struggles to convert into permanent physical assets.", s_gap_item),
    Paragraph("<b>✦ Missing 5 (Mercury):</b> Missing 5 (Earth · Mercury Center / Brahmasthan): Severe instability in focus; career restlessness; emotional oscillation during stress.", s_gap_item),
    Paragraph("<b>✦ Missing 6 (Venus):</b> Missing 6 (Metal · Venus Luxury Vibration): Delayed comfort manifestation; working hard but experiencing friction in family harmony.", s_gap_item),
    Paragraph("<b>✦ Missing 7 (Ketu):</b> Missing 7 (Metal · Ketu Wisdom &amp; Research): Repeating old mistakes; feeling spiritually disconnected; lack of deep analytical anchoring.", s_gap_item),
    Paragraph("<b>▲ Golden Prosperity Plane (4-5-6) Incomplete (Missing: 4, 5, 6):</b> Revenue enters through Driver/Conductor but leaks before compounding.", s_alert),
]

gap_header_tbl = Table([
    [Paragraph("<b>✦ NATAL GAP ANALYSIS (UNLOCKED CHART READING)</b>", s_card_h),
     Paragraph("<font color='#A13030'><b>6 GAPS IDENTIFIED</b></font>", ParagraphStyle('Badge', parent=s_card_h, alignment=2))]
], colWidths=[380, 140])
gap_header_tbl.setStyle(TableStyle([('VALIGN', (0,0), (-1,-1), 'MIDDLE')]))

gap_table_content = [
    [gap_header_tbl],
    [Paragraph("Your birth matrix contains unsealed energetic voids in <b>Missing Numbers: [2, 3, 4, 5, 6, 7]</b>. These voids cause vital momentum and wealth to leak away prematurely:", s_card_txt)],
]
for item in gap_items:
    gap_table_content.append([item])

t_gap = Table(gap_table_content, colWidths=[520])
t_gap.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
    ('TOPPADDING', (0,0), (-1,-1), 2.5),
    ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ('LEFTPADDING', (0,0), (-1,-1), 6),
    ('RIGHTPADDING', (0,0), (-1,-1), 6),
]))
story.append(t_gap)

# ── PAGE 2 ────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("8 ELEMENTAL PLANES &amp; HIDDEN RAJ YOGAS", s_name))
story.append(Paragraph("Cognitive, Will &amp; Action Balance · Sovereign Power Line Audit", s_sub))
story.append(Spacer(1, 14))

lock_card_p2 = [
    [Paragraph("<b>🔒 PREMIUM CHAPTER LOCKED</b>", ParagraphStyle('LockBadge', parent=s_top_star, textColor=COLOR_GOLD_DARK))],
    [Spacer(1, 8)],
    [Paragraph("<b>Activate Your 8-Plane Elemental Strength &amp; Lucky Charm</b>", ParagraphStyle('LockTitle', parent=s_name, fontSize=16, leading=20))],
    [Spacer(1, 6)],
    [Paragraph("Your natal chart contains potent alignments across the Thought, Will, and Action planes. Are your Golden 4-5-6 and Silver 2-5-8 lines fully active, partially dormant, or leaking vital wealth momentum?", s_card_txt)],
    [Spacer(1, 12)],
    [Table([
        [Paragraph("<b>✦ The Seeker's Curiosity Hook:</b><br/>Seekers with your Driver 9 and Conductor 2 combination frequently experience hidden friction in capital retention and career leaps due to unsealed elemental leaks. Activate your personalized Lucky Charm and master dossier to reveal your exact percentage breakdown and energetic activations.", s_card_txt)]
    ], colWidths=[480], style=[
        ('BACKGROUND', (0,0), (-1,-1), COLOR_PEARL_MID),
        ('BOX', (0,0), (-1,-1), 0.8, COLOR_GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ])],
    [Spacer(1, 14)],
    [Table([
        [Paragraph("<font color='white'><b>ANVEIL EVERY CHARM ✦ ACTIVATE LUCKY CHARM DOSSIER (₹510)</b></font>", ParagraphStyle('CTA', parent=s_top_star, textColor=colors.white, fontSize=9.5, leading=12))]
    ], colWidths=[360], hAlign='CENTER', style=[
        ('BACKGROUND', (0,0), (-1,-1), COLOR_GOLD_DARK),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ])],
    [Spacer(1, 8)],
    [Paragraph("<font color='#8B6914'><u>Or Reveal Complete 32-Page Sovereign Blueprint (₹1,050) →</u></font>", s_top_star)],
    [Spacer(1, 6)],
    [Paragraph("<font size=7 color='#7A654D'>Numeros Vision · ANVEIL EVERY CHARM · One-Time Investment · Instant Delivery</font>", s_sub)]
]
t_lock_p2 = Table(lock_card_p2, colWidths=[510], hAlign='CENTER')
t_lock_p2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ('BOX', (0,0), (-1,-1), 1.2, COLOR_GOLD),
    ('TOPPADDING', (0,0), (-1,-1), 16),
    ('BOTTOMPADDING', (0,0), (-1,-1), 16),
    ('LEFTPADDING', (0,0), (-1,-1), 14),
    ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ('ALIGN', (0,0), (-1,-1), 'CENTER')
]))
story.append(t_lock_p2)

# ── PAGE 3 ────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(Paragraph("KARMIC MISSING NUMBERS &amp; 7-LAYER CURES", s_name))
story.append(Paragraph("Vedic Elemental Voids, Safe Remedies &amp; Multi-Year Roadmap", s_sub))
story.append(Spacer(1, 14))

lock_card_p3 = [
    [Paragraph("<b>🔒 SACRED REMEDIES &amp; TIMELINES LOCKED</b>", ParagraphStyle('LockBadge3', parent=s_top_star, textColor=COLOR_GOLD_DARK))],
    [Spacer(1, 8)],
    [Paragraph("<b>Activate Your Planetary Harmonization Remedies &amp; Lucky Charm</b>", ParagraphStyle('LockTitle3', parent=s_name, fontSize=16, leading=20))],
    [Spacer(1, 6)],
    [Paragraph("Your chart lacks digits <b>[ 2, 3, 4, 5, 6, 7 ]</b>. Activating wrong gemstones without planetary conflict neutralization can trigger unexpected delays. Discover your safe, tailored remedies.", s_card_txt)],
    [Spacer(1, 12)],
    [Table([
        [Paragraph("<b>✦ The Seeker's Curiosity Hook:</b><br/>Which specific days, colors, and sacred charitable acts neutralize your karmic debts? When does your next favorable expansion window open in 2026? Activate your full multi-year dasha radar and sacred beej mantra.", s_card_txt)]
    ], colWidths=[480], style=[
        ('BACKGROUND', (0,0), (-1,-1), COLOR_PEARL_MID),
        ('BOX', (0,0), (-1,-1), 0.8, COLOR_GOLD),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ])],
    [Spacer(1, 14)],
    [Table([
        [Paragraph("<font color='white'><b>ANVEIL EVERY CHARM ✦ ACTIVATE LUCKY CHARM DOSSIER (₹510)</b></font>", ParagraphStyle('CTA3', parent=s_top_star, textColor=colors.white, fontSize=9.5, leading=12))]
    ], colWidths=[360], hAlign='CENTER', style=[
        ('BACKGROUND', (0,0), (-1,-1), COLOR_GOLD_DARK),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
    ])],
    [Spacer(1, 8)],
    [Paragraph("<font color='#8B6914'><u>Or Reveal Complete 32-Page Sovereign Blueprint (₹1,050) →</u></font>", s_top_star)],
    [Spacer(1, 6)],
    [Paragraph("<font size=7 color='#7A654D'>Master Brand: Numeros Vision · Tagline: ANVEIL EVERY CHARM · 100% Classical Precision &amp; Security</font>", s_sub)]
]
t_lock_p3 = Table(lock_card_p3, colWidths=[510], hAlign='CENTER')
t_lock_p3.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), colors.white),
    ('BOX', (0,0), (-1,-1), 1.2, COLOR_GOLD),
    ('TOPPADDING', (0,0), (-1,-1), 16),
    ('BOTTOMPADDING', (0,0), (-1,-1), 16),
    ('LEFTPADDING', (0,0), (-1,-1), 14),
    ('RIGHTPADDING', (0,0), (-1,-1), 14),
    ('ALIGN', (0,0), (-1,-1), 'CENTER')
]))
story.append(t_lock_p3)

doc.build(story, canvasmaker=CustomCanvas)

reader = pypdf.PdfReader('test_fmt1_output.pdf')
print("Total pages in generated test PDF:", len(reader.pages))
for i, page in enumerate(reader.pages):
    print(f"Page {i+1} character count:", len(page.extract_text()))
