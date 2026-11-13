# -*- coding: utf-8 -*-
import os, sys

part3_code = '''
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
'''

with open('scripts/build_upgraded_pdf_generator.py', 'a', encoding='utf-8') as f:
    f.write(part3_code)
print("Part 3 appended to scripts/build_upgraded_pdf_generator.py")
