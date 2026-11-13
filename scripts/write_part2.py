# -*- coding: utf-8 -*-
import os, sys

part2_code = '''

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
'''

with open('scripts/build_upgraded_pdf_generator.py', 'a', encoding='utf-8') as f:
    f.write(part2_code)
print("Part 2 appended to scripts/build_upgraded_pdf_generator.py")
