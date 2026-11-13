# -*- coding: utf-8 -*-
import os, sys

part5_code = '''
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
'''

with open('scripts/build_upgraded_pdf_generator.py', 'a', encoding='utf-8') as f:
    f.write(part5_code)
print("Part 5 appended! Entire upgraded generator assembled in scripts/build_upgraded_pdf_generator.py")
