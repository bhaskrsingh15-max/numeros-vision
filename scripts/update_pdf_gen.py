import re

with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update NumerosReportCanvas to add math import if not present and watermark in draw_page_decorations
if 'import math' not in content:
    content = 'import math\n' + content

watermark_code = """        # Background tint on every page
        self.setFillColor(COLOR_PEARL_BG)
        self.rect(0, 0, w, h, fill=1, stroke=0)

        # Center-Page Delicate Celestial Watermark (Concentric geometry + 16 rays + diamond)
        self.saveState()
        cx, cy = w / 2.0, h / 2.0
        self.setStrokeColor(colors.Color(0.79, 0.64, 0.15, alpha=0.06))
        self.setLineWidth(0.6)
        self.circle(cx, cy, 60, stroke=1, fill=0)
        self.circle(cx, cy, 100, stroke=1, fill=0)
        self.circle(cx, cy, 145, stroke=1, fill=0)
        for i in range(16):
            ang = i * (2.0 * math.pi / 16.0)
            x1 = cx + 65 * math.cos(ang)
            y1 = cy + 65 * math.sin(ang)
            x2 = cx + 140 * math.cos(ang)
            y2 = cy + 140 * math.sin(ang)
            self.line(x1, y1, x2, y2)
        # Inner 8-pointed star
        self.setStrokeColor(colors.Color(0.55, 0.41, 0.08, alpha=0.08))
        self.setLineWidth(0.8)
        self.rect(cx - 20, cy - 20, 40, 40, stroke=1, fill=0)
        self.rect(cx - 14, cy - 14, 28, 28, stroke=1, fill=0)
        self.restoreState()"""

content = re.sub(
    r'# Background tint on every page\s+self\.setFillColor\(COLOR_PEARL_BG\)\s+self\.rect\(0, 0, w, h, fill=1, stroke=0\)',
    watermark_code,
    content
)

# 2. Add _add_table_of_contents_page method to NumerosPdfReportBuilder
toc_method = """    def _add_table_of_contents_page(self):
        s = self.styles
        d = self.data

        self.story.append(Spacer(1, 15))
        
        toc_title = Paragraph("<b>TABLE OF CONTENTS</b>", ParagraphStyle(
            'TocTitle',
            parent=s['ChapterH1'],
            fontName='Times-Bold',
            fontSize=22,
            leading=26,
            textColor=COLOR_GOLD_DARK,
            alignment=1, # Center
            spaceAfter=6
        ))
        self.story.append(toc_title)

        toc_chip = Paragraph(
            "<font color='#8B6914'>✦ &nbsp; PERSONAL DESTINY BLUEPRINT &nbsp; · &nbsp; 2026 &nbsp; ✦</font>",
            ParagraphStyle('TocChip', parent=s['Badge'], fontName='Times-Bold', fontSize=8.5, leading=11, alignment=1)
        )
        t_chip = Table([[toc_chip]], colWidths=[515])
        t_chip.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_PEARL_MID),
            ('BOX', (0,0), (-1,-1), 1, COLOR_GOLD),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ]))
        self.story.append(t_chip)
        self.story.append(Spacer(1, 16))

        col1_items = [
            ("01", "Destiny Signature & Matrix", "Core Driver, Conductor & Lo Shu 3x3 Grid"),
            ("02", "Lo Shu Elemental Planes", "Evaluation of 6 cosmic planes (Head, Heart, Hands)"),
            ("03", "Chaldean Sound Frequencies", "Letter-by-letter acoustic compound vibration"),
            ("04", "5-Year Cosmic Timing Radar", "Annual personal years and Mahadasha cycles"),
            ("05", "In-Depth Topic Diagnostic", f"Tailored blueprint addressing {d['topic_title']}")
        ]

        col2_items = [
            ("06", "Interpersonal Synergy", "Relationship harmony and partner compatibility"),
            ("07", "Auspicious Initiation Windows", "Optimal timing & Muhurat for major decisions"),
            ("08", "7-Layer Planetary Balance", "Safe non-invasive lifestyle & elemental remedies"),
            ("09", "Spatial & 90-Day Roadmap", "Kua directional vectors & quarterly action milestones"),
            ("10", "Governance & Verification", "Deterministic engine provenance & DPDP 2023 notice")
        ]

        rows = []
        for i in range(5):
            num1, title1, sub1 = col1_items[i]
            num2, title2, sub2 = col2_items[i]

            cell1 = Paragraph(
                f"<font size='14' color='#8B6914'><b>{num1}</b></font> &nbsp; <font size='9'><b><u>{title1.upper()}</u></b></font><br/>"
                f"<font size='7.5' color='#7A654D'><i>{sub1}</i></font>",
                s['TableCell']
            )
            cell2 = Paragraph(
                f"<font size='14' color='#8B6914'><b>{num2}</b></font> &nbsp; <font size='9'><b><u>{title2.upper()}</u></b></font><br/>"
                f"<font size='7.5' color='#7A654D'><i>{sub2}</i></font>",
                s['TableCell']
            )
            rows.append([cell1, cell2])

        t_toc = Table(rows, colWidths=[250, 250])
        t_toc.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), COLOR_CARD_BG),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 12),
            ('BOTTOMPADDING', (0,0), (-1,-1), 12),
            ('LEFTPADDING', (0,0), (-1,-1), 12),
            ('RIGHTPADDING', (0,0), (-1,-1), 12),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ]))
        self.story.append(t_toc)
        self.story.append(Spacer(1, 18))

        toc_footer = Paragraph(
            "<font size='7.5' color='#7A654D'>✦ &nbsp; All chapter calculations generated deterministically by Numeros Vision Engine &nbsp; · &nbsp; <b>numerosvision.com</b> &nbsp; ✦</font>",
            ParagraphStyle('TocFoot', parent=s['Normal'], alignment=1)
        )
        self.story.append(toc_footer)

"""

# Insert _add_table_of_contents_page right before _assemble_advanced_12_pages
content = content.replace("    def _assemble_advanced_12_pages(self):", toc_method + "    def _assemble_advanced_12_pages(self):")

# 3. In _assemble_advanced_12_pages, insert Table of Contents on Page 2 and harmonize Chapter 9 & 10
old_adv_start = """        # 1. Cover
        self._add_cover_page(
            subtitle="12-Page Master Synthesis Dossier & Multi-Factor Roadmap",
            badge_text="ADVANCED REPORT  ·  12-PAGE MASTER DOSSIER"
        )
        self.story.append(PageBreak())

        # 2. Executive Summary & Core Destiny Signature"""

new_adv_start = """        # 1. Cover
        self._add_cover_page(
            subtitle="12-Page Master Synthesis Dossier & Multi-Factor Roadmap",
            badge_text="ADVANCED REPORT  ·  12-PAGE MASTER DOSSIER"
        )
        self.story.append(PageBreak())

        # 2. Table of Contents (Matching Luxury Reference)
        self._add_table_of_contents_page()
        self.story.append(PageBreak())

        # 3. Executive Summary & Core Destiny Signature"""

content = content.replace(old_adv_start, new_adv_start)

# Harmonize Chapter 9 and Chapter 10 into one structured execution page, so total is 12 pages
old_ch9_10 = """        # 10. Living Environment & Space Alignment
        self.story.append(Paragraph("Chapter 9: Space Alignment & Directional Vectors", s['ChapterH1']))
        self.story.append(Paragraph(
            f"Based on your Kua Number ({d['kua_number']}), directional alignment optimizes vitality and mental focus during work hours.",
            s['ReportBody']
        ))
        kua_data = [
            [Paragraph("<b>Wealth / Prosperity Vector:</b>", s['TableHeader']), Paragraph("South-East (Face this direction during key strategic planning)", s['TableCell'])],
            [Paragraph("<b>Vitality & Health Vector:</b>", s['TableHeader']), Paragraph("East (Optimal for sleep headboard orientation)", s['TableCell'])],
            [Paragraph("<b>Relationship Harmony:</b>", s['TableHeader']), Paragraph("South (Ideal for dining and family social spaces)", s['TableCell'])],
            [Paragraph("<b>Clarity & Inner Peace:</b>", s['TableHeader']), Paragraph("North (Meditation and contemplative sanctuary)", s['TableCell'])],
        ]
        t_kua = Table(kua_data, colWidths=[180, 335])
        t_kua.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
        ]))
        self.story.append(t_kua)
        self.story.append(PageBreak())

        # 11. Practical Strategic Action Plan
        self.story.append(Paragraph("Chapter 10: Practical 90-Day Execution Roadmap", s['ChapterH1']))"""

new_ch9_10 = """        # 10. Living Environment, Spatial Alignment & 90-Day Execution Roadmap
        self.story.append(Paragraph("Chapter 9: Spatial Alignment & 90-Day Execution Roadmap", s['ChapterH1']))
        self.story.append(Paragraph(
            f"Based on your Kua Number ({d['kua_number']}), directional orientation optimizes vitality and mental focus during active work hours:",
            s['ReportBody']
        ))
        kua_data = [
            [Paragraph("<b>Wealth / Prosperity Vector:</b>", s['TableHeader']), Paragraph("South-East (Optimal desk orientation for negotiations)", s['TableCell'])],
            [Paragraph("<b>Vitality & Health Vector:</b>", s['TableHeader']), Paragraph("East (Optimal sleep headboard orientation)", s['TableCell'])],
            [Paragraph("<b>Relationship Harmony:</b>", s['TableHeader']), Paragraph("South (Optimal for social, collaborative spaces)", s['TableCell'])],
            [Paragraph("<b>Clarity & Inner Peace:</b>", s['TableHeader']), Paragraph("North (Contemplative & strategic focus zone)", s['TableCell'])],
        ]
        t_kua = Table(kua_data, colWidths=[180, 335])
        t_kua.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_kua)
        self.story.append(Spacer(1, 10))

        self.story.append(Paragraph("<b>Practical 90-Day Milestone Execution:</b>", s['SectionH2']))
        roadmap = [
            ("Days 1 – 30: Stabilization & Clearing", "Audit current workspace, calibrate signature spelling, and establish morning grounding ritual."),
            ("Days 31 – 60: Strategic Alignment", "Initiate outreach during personal year auspicious dates, schedule key meetings on allied days."),
            ("Days 61 – 90: Consolidation & Harvest", "Review financial agreements, strengthen partnership boundaries, and lock in long-term commercial assets.")
        ]
        t_road = Table([[Paragraph(f"<b>{step}</b><br/>{body}", s['TableCell'])] for step, body in roadmap], colWidths=[515])
        t_road.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        self.story.append(t_road)"""

content = content.replace(old_ch9_10, new_ch9_10)

# Replace Chapter 11 with Chapter 10
content = content.replace('Paragraph("Chapter 11: Methodology, Provenance & Governance", s[\'ChapterH1\'])', 'Paragraph("Chapter 10: Methodology, Provenance & Governance", s[\'ChapterH1\'])')

with open('app/services/pdf_report_generator.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Updated app/services/pdf_report_generator.py successfully!")
