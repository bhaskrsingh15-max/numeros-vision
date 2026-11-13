# -*- coding: utf-8 -*-
import os, sys

part4_code = '''
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
'''

with open('scripts/build_upgraded_pdf_generator.py', 'a', encoding='utf-8') as f:
    f.write(part4_code)
print("Part 4 appended to scripts/build_upgraded_pdf_generator.py")
