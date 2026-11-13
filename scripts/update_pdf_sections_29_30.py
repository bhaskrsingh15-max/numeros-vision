import re
import os

print("--- 1. Updating app/services/pdf_report_generator.py ---")

with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    pdf_code = f.read()

# 1. Update _assemble_advanced_12_pages cover & TOC for premium
old_cover_toc = '''        # PAGE 1: Cover
        self._add_cover_page(
            subtitle="12-Page Master Synthesis Dossier & Multi-Factor Roadmap",
            badge_text="ADVANCED REPORT · 12-PAGE MASTER DOSSIER · FULL MULTI-FACTOR RADAR"
        )
        self.story.append(PageBreak())

        # PAGE 2: Table of Contents
        self.story.append(Spacer(1, 10))
        self.story.append(Paragraph("TABLE OF CONTENTS", s['SectionH1']))
        self.story.append(Paragraph("✦   PERSONAL DESTINY BLUEPRINT · 12-PAGE MASTER SYNTHESIS   ✦", s['CoverSubtitle']))
        self.story.append(Spacer(1, 10))

        toc_items = [
            ("Section 1: Executive Summary & Destiny Signature", "Page 3"),
            ("Section 2: Natal Lo Shu 3×3 Grid & 8-Plane Elemental Audit", "Page 4"),
            ("Section 3: Chaldean & Pythagorean Sound Frequency Matrix", "Page 5"),
            ("Section 4: 5-Year Cosmic Dasha & Planetary Timing Radar (2026–2030)", "Page 6"),
            ("Section 5: Career, Enterprise & Financial Direction in Adtech & Media", "Page 7"),
            ("Section 6: Interpersonal Synergy, Co-Founder Matching & Synastry", "Page 8"),
            ("Section 7: Auspicious Initiation Windows & Muhurat Timing", "Page 9"),
            ("Section 8: 7-Layer Holistic Planetary Remedial System", "Page 10"),
            ("Section 9: Spatial Feng Shui & Kua Number 1 Directional Blueprint", "Page 11"),
            ("Section 10: Methodology, Algorithmic Provenance & Statutory Sign-off", "Page 12")
        ]

        toc_rows = [
            [Paragraph("<b>Section / Standard Topic</b>", s['TableHeader']), Paragraph("<b>Page</b>", s['TableHeader'])]
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
        self.story.append(Spacer(1, 18))'''

new_cover_toc = '''        # PAGE 1: Cover
        is_premium_tier = self.tier in ("premium", "report_premium", "divine", "roadmap", "report_divine")
        if is_premium_tier:
            self._add_cover_page(
                subtitle="32-Page Divine Sovereign Lifetime Architecture & Analytical Compendium",
                badge_text="PREMIUM REPORT · 32-PAGE SOVEREIGN ROADMAP · COMPLETE NUMEROLOGICAL COMPENDIUM"
            )
        else:
            self._add_cover_page(
                subtitle="12-Page Master Synthesis Dossier & Multi-Factor Roadmap",
                badge_text="ADVANCED REPORT · 12-PAGE MASTER DOSSIER · FULL MULTI-FACTOR RADAR"
            )
        self.story.append(PageBreak())

        # PAGE 2: Table of Contents
        self.story.append(Spacer(1, 6))
        self.story.append(Paragraph("TABLE OF CONTENTS", s['SectionH1']))
        if is_premium_tier:
            self.story.append(Paragraph("✦   SOVEREIGN COMPENDIUM · 30 STANDARD SECTIONS ACROSS 32 PAGES   ✦", s['CoverSubtitle']))
            self.story.append(Spacer(1, 6))

            toc_part1 = [
                ("Section 1: Executive Summary & Destiny Signature", "Page 3"),
                ("Section 2: Natal Lo Shu 3×3 Grid & 8 Elemental Planes", "Page 4"),
                ("Section 3: Chaldean & Pythagorean Sound Frequency Matrix", "Page 5"),
                ("Section 4: 5-Year Cosmic Dasha & Planetary Timing Radar", "Page 6"),
                ("Section 5: Career, Enterprise & Financial Direction", "Page 7"),
                ("Section 6: Interpersonal Synergy & Co-Founder Matching", "Page 8"),
                ("Section 7: Auspicious Initiation Windows & Muhurat Timing", "Page 9"),
                ("Section 8: 7-Layer Holistic Planetary Remedial System", "Page 10"),
                ("Section 9: Spatial Feng Shui & Kua 1 Directional Blueprint", "Page 11"),
                ("Section 10: Methodology & Algorithmic Provenance", "Page 12"),
                ("Section 11: 81-Pair Archetype Matrix — Sun 1 + Rahu 4", "Page 13"),
                ("Section 12: Dual-System Synthesis — Chaldean vs Pythagorean", "Page 14"),
                ("Section 13: 10-Year Macro Planetary Timing Radar", "Page 15"),
                ("Section 14: Karmic Debt & Elemental Gaps Diagnosis", "Page 16"),
                ("Section 15: High-Growth Enterprise Scaling Architecture", "Page 17")
            ]
            toc_part2 = [
                ("Section 16: Financial Compounding & Asset Anchoring", "Page 18"),
                ("Section 17: Co-Founder, Partner & Investor Dynamics", "Page 19"),
                ("Section 18: Strategic Reputation & Public Branding", "Page 20"),
                ("Section 19: Family Dynasty & Intergenerational Synergy", "Page 21"),
                ("Section 20: Relationship Harmony & Spousal Synastry", "Page 22"),
                ("Section 21: Health, Vitality & Ayurvedic Chronobiology", "Page 23"),
                ("Section 22: Career Transmutation & Board Advisory", "Page 24"),
                ("Section 23: Digital Identity, Mobile & Cyber Resonance", "Page 25"),
                ("Section 24: Global Horizons & Cross-Border Expansion", "Page 26"),
                ("Section 25: Creative Authority & Executive Leadership", "Page 27"),
                ("Section 26: 12-Month Micro Breakdown for 2026", "Page 28"),
                ("Section 27: High-Stakes Decision Protocol & Horas", "Page 29"),
                ("Section 28: Comprehensive Remedial Handbook", "Page 30"),
                ("Section 29: 4-Stage Pinnacle Cycles & Life Challenges", "Page 31"),
                ("Section 30: Vastu Dosha as per Missing Numbers & Cures", "Page 32")
            ]

            toc_rows = [
                [Paragraph("<b>Standard Section (Part I)</b>", s['TableHeader']), Paragraph("<b>Page</b>", s['TableHeader']),
                 Paragraph("<b>Standard Section (Part II)</b>", s['TableHeader']), Paragraph("<b>Page</b>", s['TableHeader'])]
            ]
            for i in range(15):
                t1, p1 = toc_part1[i]
                t2, p2 = toc_part2[i]
                toc_rows.append([
                    Paragraph(f"<b>{t1}</b>", s['TableCell']), Paragraph(p1, s['TableCellCenter']),
                    Paragraph(f"<b>{t2}</b>", s['TableCell']), Paragraph(p2, s['TableCellCenter'])
                ])

            t_toc = Table(toc_rows, colWidths=[205, 52, 205, 52])
            t_toc.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.white),
                ('BOX', (0,0), (-1,-1), 1.2, COLOR_BORDER),
                ('INNERGRID', (0,0), (-1,-1), 0.5, COLOR_BORDER),
                ('TOPPADDING', (0,0), (-1,-1), 3.5),
                ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
                ('LEFTPADDING', (0,0), (-1,-1), 5),
                ('RIGHTPADDING', (0,0), (-1,-1), 5),
            ]))
            self.story.append(t_toc)
            self.story.append(Spacer(1, 10))
        else:
            self.story.append(Paragraph("✦   PERSONAL DESTINY BLUEPRINT · 12-PAGE MASTER SYNTHESIS   ✦", s['CoverSubtitle']))
            self.story.append(Spacer(1, 10))

            toc_items = [
                ("Section 1: Executive Summary & Destiny Signature", "Page 3"),
                ("Section 2: Natal Lo Shu 3×3 Grid & 8-Plane Elemental Audit", "Page 4"),
                ("Section 3: Chaldean & Pythagorean Sound Frequency Matrix", "Page 5"),
                ("Section 4: 5-Year Cosmic Dasha & Planetary Timing Radar (2026–2030)", "Page 6"),
                ("Section 5: Career, Enterprise & Financial Direction in Adtech & Media", "Page 7"),
                ("Section 6: Interpersonal Synergy, Co-Founder Matching & Synastry", "Page 8"),
                ("Section 7: Auspicious Initiation Windows & Muhurat Timing", "Page 9"),
                ("Section 8: 7-Layer Holistic Planetary Remedial System", "Page 10"),
                ("Section 9: Spatial Feng Shui & Kua Number 1 Directional Blueprint", "Page 11"),
                ("Section 10: Methodology, Algorithmic Provenance & Statutory Sign-off", "Page 12")
            ]

            toc_rows = [
                [Paragraph("<b>Section / Standard Topic</b>", s['TableHeader']), Paragraph("<b>Page</b>", s['TableHeader'])]
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
            self.story.append(Spacer(1, 18))'''

if old_cover_toc in pdf_code:
    pdf_code = pdf_code.replace(old_cover_toc, new_cover_toc)
    print("Cover & TOC in pdf_report_generator.py replaced successfully!")
else:
    print("WARNING: old_cover_toc not found in pdf_report_generator.py")

# 2. Replace Section 29 and Section 30 in premium_chapters
old_sec_29_30 = '''            # Page 31
            ("Section 29: Annual Executive Self-Audit & Contemplative Framework",
             "True sovereignty requires consistent self-mastery. Once every year on or near your birthday (28 November), conduct this 5-point executive self-audit to recalibrate your personal and professional trajectory.",
             [
                 ("Audit 1: Strategic Vision", "Did my major business initiatives in the past 12 months reflect sovereign Sun 1 leadership?"),
                 ("Audit 2: Structural Integrity", "Were my contractual frameworks and technology systems hardened to withstand market shocks?"),
                 ("Audit 3: Financial Reserves", "Did I maintain the 25% automated liquid reserve rule to protect against cash volatility?"),
                 ("Audit 4: Personal Vitality", "Did I honor my morning Solar protocols and maintain physical health and mental poise?"),
                 ("Audit 5: Legacy & Ethics", "Did my commercial endeavors elevate the industry and uphold unwavering ethical rigor?")
             ]),

            # Page 32
            ("Section 30: Exhaustive Mathematical Appendix & Algorithmic Proofs",
             f"This final technical appendix documents the complete deterministic mathematical reduction proofs for <b>{d['seeker_name']}</b>, ensuring absolute provenance and verifiable repeatability under DPDP Act 2023.",
             [
                 ("Solar Day Proof", "28 = 2 + 8 = 10 → 1 + 0 = 1 (Sun / Surya — Sovereign Executive Root)"),
                 ("Total Date Proof", "2+8+1+1+1+9+8+1 = 31 → 3 + 1 = 4 (Rahu / North Node — Macro Conductor)"),
                 ("Chaldean Sound Proof", "B(2)+H(5)+A(1)+S(3)+K(2)+R(2) = 15; S(3)+I(1)+N(5)+G(3)+H(5) = 17; Total = 32 → 5"),
                 ("Pythagorean Proof", "B(2)+H(8)+A(1)+S(1)+K(2)+R(9) = 23; S(1)+I(9)+N(5)+G(7)+H(8) = 30; Total = 53 → 8"),
                 ("Kua Proof (1981 Male)", "1981: 8 + 1 = 9; Male Formula: 10 - 9 = 1 (Water / Kan · East Group)"),
                 ("Engine Certification", f"Numeros Vision Deterministic Engine v2.1.0 · Dossier ID: {d['report_id']} · SHA-256 Verified")
             ])'''

new_sec_29_30 = '''            # Page 31
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
                 ("West (W) Missing 7 Correction", "West governs intellectual focus and creative completion (Metal). Remedy: Place round white metal artefacts or a consecrated Ganesh/Ketu Yantra on the West wall")
             ])'''

if old_sec_29_30 in pdf_code:
    pdf_code = pdf_code.replace(old_sec_29_30, new_sec_29_30)
    print("Section 29 and Section 30 in pdf_report_generator.py replaced successfully!")
else:
    print("WARNING: old_sec_29_30 not found in pdf_report_generator.py")

with open('app/services/pdf_report_generator.py', 'w', encoding='utf-8') as f:
    f.write(pdf_code)

print("Saved app/services/pdf_report_generator.py successfully!")
