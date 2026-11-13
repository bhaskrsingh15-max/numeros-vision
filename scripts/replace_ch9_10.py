import re

with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace from Chapter 9 down to Chapter 11/10
pattern = r'# 10\. Living Environment & Space Alignment.*?self\.story\.append\(Paragraph\("Chapter 1\d: Methodology, Provenance & Governance", s\[\'ChapterH1\'\]\)\)'

replacement = """# 9. Spatial Alignment & 90-Day Execution Roadmap
        self.story.append(Paragraph("Chapter 9: Spatial Alignment & 90-Day Execution Roadmap", s['ChapterH1']))
        self.story.append(Paragraph(
            f"Based on your Kua Number ({d['kua_number']}), directional alignment optimizes vitality and mental focus during active work hours:",
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
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ]))
        self.story.append(t_kua)
        self.story.append(Spacer(1, 8))

        self.story.append(Paragraph("<b>90-Day Strategic Milestone Execution:</b>", s['SectionH2']))
        roadmap = [
            ("Days 1 - 30: Stabilization & Clearing", "Audit current workspace, eliminate energetic clutter, calibrate signature spelling, and establish morning grounding ritual."),
            ("Days 31 - 60: Strategic Alignment", "Initiate outreach during personal year auspicious dates, schedule key meetings on allied days."),
            ("Days 61 - 90: Consolidation & Harvest", "Review financial agreements, strengthen partnership boundaries, and lock in long-term commercial assets.")
        ]
        t_road = Table([[Paragraph(f"<b>{step}</b><br/>{body}", s['TableCell'])] for step, body in roadmap], colWidths=[515])
        t_road.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.white),
            ('BOX', (0,0), (-1,-1), 1, COLOR_BORDER),
            ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ]))
        self.story.append(t_road)
        self.story.append(PageBreak())

        # 10. Methodology, Provenance & Governance Notice
        self.story.append(Paragraph("Chapter 10: Methodology, Provenance & Governance", s['ChapterH1']))"""

new_text, count = re.subn(pattern, replacement, text, flags=re.DOTALL)
print(f"Replaced {count} occurrences")

with open('app/services/pdf_report_generator.py', 'w', encoding='utf-8') as f:
    f.write(new_text)

print("Saved updated pdf_report_generator.py")
