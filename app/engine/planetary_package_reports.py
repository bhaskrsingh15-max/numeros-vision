"""
PLANETARY & HARMONIC DOMAIN REPORT GENERATOR
Numeros Vision — ANVEIL EVERY CHARM

Generates tailored, publication-ready problem-based solution reports for all 5 Planetary Domains:
1. Venus (Shukra) · Harmonic Root 6: Sacred Union & Spousal Bond (₹105 → ₹489 → ₹5,100)
2. Mercury (Budh) · Harmonic Root 5: Commercial Velocity & Market Flow (₹149 → ₹599 → ₹5,999)
3. Sun (Surya) · Harmonic Root 1: Executive Authority & Sovereignty (₹199 → ₹550 → ₹5,500)
4. Mercury/Venus · Harmonic Root 5 & 6: Global Horizon & Relocation (₹149 → ₹489 → ₹5,100)
5. Jupiter (Guru) · Harmonic Root 3: Higher Calling & Mentorship (₹120 → ₹570 → ₹4,800)

Strict Quality Standards:
- Zero technical astrology jargon
- Clear root-cause explanation of the seeker's friction
- Actionable problem-based solutions matching package level (2-Page, 12-Page, 35-Page)
- Deterministic calculation alignment with Driver, Conductor, Lo Shu, and Chaldean Name
"""

from typing import Dict, Any, Optional
from app.engine.diplomatic_narrative_engine import sanitize_text
from app.engine.lo_shu import generate_loshu_grid_markdown
from app.engine.core_matrix_engine import calculate_age_numerology

def is_planetary_package(tier: str) -> bool:
    t = tier.lower().strip()
    return any(t.startswith(prefix) for prefix in [
        "report_union", "report_commerce", "report_authority",
        "report_relocation", "report_dharma",
        "union_", "commerce_", "authority_", "relocation_", "dharma_"
    ])

def generate_planetary_domain_report(
    clean_tier: str,
    clean_name: str,
    day: int,
    month: int,
    year: int,
    driver: int,
    conductor: int,
    driver_planet: str,
    conductor_planet: str,
    profile_summary: Dict[str, Any]
) -> Dict[str, Any]:
    """Generates tailored problem-based reports for planetary domain packages."""
    t = clean_tier.lower().strip()

    # Determine domain & sub-tier (tripwire, master, sovereign)
    if "tripwire" in t or t.endswith("_2p"):
        level = "tripwire"
    elif "sovereign" in t or t.endswith("_35p"):
        level = "sovereign"
    else:
        level = "master"

    if "union" in t:
        res = _generate_union_report(level, clean_name, day, month, year, driver, conductor, driver_planet, conductor_planet, profile_summary)
    elif "commerce" in t:
        res = _generate_commerce_report(level, clean_name, day, month, year, driver, conductor, driver_planet, conductor_planet, profile_summary)
    elif "authority" in t:
        res = _generate_authority_report(level, clean_name, day, month, year, driver, conductor, driver_planet, conductor_planet, profile_summary)
    elif "relocation" in t:
        res = _generate_relocation_report(level, clean_name, day, month, year, driver, conductor, driver_planet, conductor_planet, profile_summary)
    elif "dharma" in t:
        res = _generate_dharma_report(level, clean_name, day, month, year, driver, conductor, driver_planet, conductor_planet, profile_summary)
    else:
        res = _generate_union_report("master", clean_name, day, month, year, driver, conductor, driver_planet, conductor_planet, profile_summary)

    # In every report, the Lo Shu birth chart must always be there
    loshu_chart_md = generate_loshu_grid_markdown(day, month, year)
    age_data = calculate_age_numerology(day, month, year)
    age_md = (
        f"### Chronological Age Milestone & Planetary Resonance\n"
        f"**Milestone:** {age_data['age_years']} Years Completed (Navigating Year {age_data['running_year']}) | "
        f"**Input Compound {age_data['compound_age']} ➔ Output Root {age_data['root_age']} ({age_data['root_planet']})**\n\n"
        f"• **Current Energetic Lesson:** {age_data['input_characteristics']['description']}\n"
        f"• **Manifestation Focus:** {age_data['output_characteristics']['manifestation']}\n"
        f"• **Karmic Alignment:** {age_data['gap_analysis']['diagnosis']}"
    )
    combined_foundational_md = f"{loshu_chart_md}\n\n{age_md}"
    if "Natal Lo Shu Grid Birth Chart" not in res.get("report_markdown", ""):
        md = res.get("report_markdown", "")
        # Insert after the title header section
        parts = md.split("\n\n", 2)
        if len(parts) >= 3:
            res["report_markdown"] = parts[0] + "\n\n" + parts[1] + "\n\n" + combined_foundational_md + "\n\n" + parts[2]
        else:
            res["report_markdown"] = md + "\n\n" + combined_foundational_md
    return res


# ─────────────────────────────────────────────────────────────────────────────
# 1. VENUS (SHUKRA) — SACRED UNION & SPOUSAL BOND (ROOT 6)
# ─────────────────────────────────────────────────────────────────────────────
def _generate_union_report(level: str, name: str, day: int, month: int, year: int, driver: int, conductor: int, d_planet: str, c_planet: str, profile: dict) -> dict:
    if level == "tripwire":
        sections = [
            f"# Marital Harmony & Spousal Gap Unblocker\n**Prepared for:** {name} | **Harmonic Root:** 6 (Venus Opulence) | **Format:** 3-Page Action Plan\n",
            "## 1. Relationship Energetic Alignment & Friction Root Cause",
            (
                f"Welcome, {name}. Your core matrix blends the primary drive of Root {driver} ({d_planet}) with Life Path {conductor}. "
                f"In partnerships, this creates a high standard for loyalty and deep emotional expectations. "
                f"Current relationship friction arises not from lack of affection, but from mismatched communication pacing. "
                f"When expectations are left unexpressed, subtle emotional distance builds up. "
                f"Venusian energy thrives on beauty, softness, and deliberate recognition."
            ),
            "## 2. Immediate Spousal Harmony Checklist",
            (
                "• **The 3-Minute Daily Reconnection:** Spend 3 uninterrupted minutes every evening sharing one genuine appreciation with your partner.\n"
                "• **De-escalate Evening Discussions:** Avoid discussing domestic finances, responsibilities, or sensitive topics after 9:00 PM.\n"
                "• **Eliminate Sharp Expressions:** Replace critical tones with collaborative phrasing: 'How can we solve this together?'"
            ),
            "## 3. Friday Sattvic Attunement & Venusian Vibration",
            (
                "• **Auspicious Color:** Wear soft white, pastel cream, or rose pink every Friday.\n"
                "• **Sensory Harmony:** Introduce natural sandalwood or pure rose aroma in your primary living space on Friday mornings.\n"
                "• **Shared Sweetness:** Offer sweet white fruit or kheer to loved ones on Friday evenings to sweeten the vibrational aura."
            ),
            "## 4. Lucky Relationship Direction & Sacred Communication Ritual",
            (
                "• **Harmonic Bedroom Direction:** Ensure your primary sleeping space is aligned with your head toward South or East.\n"
                "• **North-West Air Fluidity:** Keep the North-West area of your bedroom completely clutter-free to maintain ease of emotional dialogue."
            )
        ]
        return {
            "tier": "report_union_tripwire",
            "tier_display": "Marital Harmony Gap Unblocker (3-Page Action Guide)",
            "domain": "Love, Marriage & Spousal Harmony",
            "planet": "Venus (Shukra)",
            "harmonic_root": 6,
            "price_inr": 105,
            "price_usd": 6.00,
            "profile": profile,
            "page_target": "3 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }

    elif level == "master":
        sections = [
            f"# Sacred Union & Luxury Relationship Dossier\n**Client:** {name} | **Edition:** Master 12-Chapter Dossier with Royal Gold Seals\n",
            "## Chapter 1: Foundational Relational Architecture",
            (
                f"Your natal blueprint combines the distinctive willpower of Root {driver} ({d_planet}) with Path {conductor} ({c_planet}). "
                f"Under Harmonic Root 6 (Venus), your relationship capacity is structured for enduring devotion, mutual harmony, and domestic prosperity. "
                f"This dossier analyzes your primary relational planes, identifies unconscious friction triggers, and provides verified sacred methods to restore warmth."
            ),
            "## Chapter 2: Thought & Emotional Plane Lo Shu Synergy",
            (
                "Analysis of your 3×3 energetic matrix reveals key dynamics:\n"
                "• **The Emotional Axis (Plane 2-7-6):** Indicates deep feeling and sensitivity to subtle partner nuances.\n"
                "• **The Communication Channel:** Requires conscious grounding to prevent over-analyzing innocent silences.\n"
                "• **Balancing Protocol:** Introducing pure silver and soft white elements anchors emotional stability."
            ),
            "## Chapter 3: Current Relationship Transit & Timing Radar",
            (
                "• **Current Calibration Cycle:** You are navigating a cycle that encourages deepening emotional honesty and resolving past unspoken grievances.\n"
                "• **Upcoming Harmonization Window:** The upcoming cycle activates high warmth, mutual travel, and restored romantic vitality.\n"
                "• **Favorable Decision Dates:** Fridays falling on dates reducing to 3, 6, or 9 represent optimal moments for joint commitments."
            ),
            "## Chapter 4: Ishta Devata Sadhana & Consecrated Beej Mantra",
            (
                "To attract gentle Venusian grace into your domestic sanctuary:\n"
                "• **Sacred Sound Vibration:** Recite the gentle Venus attunement sound (*Om Shukraya Namaha*) 11 times every Friday morning.\n"
                "• **Sanctuary Setup:** Place a clean silver vessel filled with fresh water and white flowers in the South-East or North-West corner."
            ),
            "## Chapter 5: 12-Month Milestone Windows",
            (
                "• **Months 1–3:** Internal clearing, open dialogue, and shared recreational outings.\n"
                "• **Months 4–8:** Breakthrough in mutual trust, major domestic upgrade, or auspicious family milestone.\n"
                "• **Months 9–12:** Harmonious compounding of mutual prosperity and relationship security."
            ),
            "## Chapter 6: Safe Non-Commercial Harmonization Protocol",
            (
                "1. **Morning Light Focus:** Spend 5 minutes daily facing East together in quiet contemplation.\n"
                "2. **Auspicious Palette:** Wear pastel shades on social outings; avoid harsh charcoal on intimate dates.\n"
                "3. **Loving Compassion:** Donate white rice or milk to community sanctuaries on auspicious Fridays."
            )
        ]
        return {
            "tier": "report_union_master",
            "tier_display": "Sacred Union & Luxury Dossier (12-Page Master Report)",
            "domain": "Love, Marriage & Spousal Harmony",
            "planet": "Venus (Shukra)",
            "harmonic_root": 6,
            "price_inr": 489,
            "price_usd": 24.00,
            "profile": profile,
            "page_target": "12 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }

    else:  # sovereign
        sections = [
            f"# Sovereign Couple Destiny & Marriage Synchronization Blueprint\n**Client:** {name} | **Edition:** 32-Page Master Life Transformation Blueprint\n",
            "## Chapter 1: The Sovereign Couple Architecture",
            (
                f"Welcome, {name}. This 32-page sovereign dossier represents our highest level of relational synchronization. "
                f"Grounded in classical Chaldean acoustics, Core Driver-Conductor vectors, and Five-Element Lo Shu equilibrium, "
                f"this blueprint harmonizes your lifetime marital destiny."
            ),
            "## Chapter 2: Dual Synastry Cross-Matching & Harmonic Vector Matrix",
            (
                f"Examining your Root {driver} ({d_planet}) alongside partner dynamics reveals the exact karmic intersections. "
                "Where mental friction was once perceived, this matrix reveals complementary strengths. "
                "One partner provides executive vision, while the other provides commercial caution and domestic grounding."
            ),
            "## Chapter 3: Chaldean Legal & Calling Name Harmonization",
            (
                "Your calling name vibration sets the continuous acoustic backdrop for your household:\n"
                "• **Calling Name Audit:** Ensuring your daily domestic address vibrates to auspicious Number 1, 5, or 6.\n"
                "• **Spelling Optimization:** Minor vowel adjustment recommendations to neutralize compound friction numbers."
            ),
            "## Chapter 4: 5-Year Multi-Decade Relationship Roadmap",
            (
                "• **Year 1:** Deep reconciliation, household re-anchoring, and shared emotional renewal.\n"
                "• **Years 2–3:** Joint asset accumulation, auspicious property decisions, and family stability.\n"
                "• **Years 4–5:** Spiritual maturity, high societal respect, and harmonic legacy creation."
            ),
            "## Chapter 5: Sacred Couple Bedroom Vastu & Directional Geometries",
            (
                "• Master bed orientation with head strictly South or East.\n"
                "• Total elimination of mirrors directly facing the resting bed.\n"
                "• Warm illumination with soft rose and amber night tones."
            )
        ]
        return {
            "tier": "report_union_sovereign",
            "tier_display": "Sovereign Couple Destiny Blueprint (32-Page Master Roadmap)",
            "domain": "Love, Marriage & Spousal Harmony",
            "planet": "Venus (Shukra)",
            "harmonic_root": 6,
            "price_inr": 5100,
            "price_usd": 150.00,
            "profile": profile,
            "page_target": "32 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }


# ─────────────────────────────────────────────────────────────────────────────
# 2. MERCURY (BUDH) — COMMERCIAL VELOCITY & MARKET FLOW (ROOT 5)
# ─────────────────────────────────────────────────────────────────────────────
def _generate_commerce_report(level: str, name: str, day: int, month: int, year: int, driver: int, conductor: int, d_planet: str, c_planet: str, profile: dict) -> dict:
    if level == "tripwire":
        sections = [
            f"# Cash Flow Gap & Commercial Velocity Unblocker\n**Prepared for:** {name} | **Harmonic Root:** 5 (Mercury Velocity) | **Format:** 3-Page Action Plan\n",
            "## 1. Missing Number 5 & Cash Drainage Audit",
            (
                f"Welcome, {name}. Your natal matrix governed by Root {driver} and Path {conductor} carries strong ambition. "
                f"However, financial stagnation or cash drainage occurs when the central communication plane lacks fluidity. "
                f"Money is an energetic exchange governed by Mercury (Budh). When contracts are ambiguous or invoicing is delayed, cash velocity drops."
            ),
            "## 2. Rapid Commercial Negotiation Timing Windows",
            (
                "• **Prime Negotiation Days:** Schedule major client pitches, salary reviews, or debtor calls on Wednesdays between 10:00 AM and 1:30 PM.\n"
                "• **Written Invoice Precision:** Never send vague estimates; document clear milestone deliverables with explicit net-15 payment terms."
            ),
            "## 3. Wednesday Green Attunement & Cash Fluidity",
            (
                "• **Auspicious Color:** Wear emerald green, mint, or turquoise on Wednesdays.\n"
                "• **Green Food & Vitality:** Consume fresh green vegetables and mint tea every Wednesday morning to harmonize Mercurial frequency."
            ),
            "## 4. North Commercial Facing Vector",
            (
                "• **Desk Direction:** Ensure your primary work desk faces North (the direction of financial inflow).\n"
                "• **Cash Box / Ledger Orientation:** Keep your financial records or invoice drawer in the North corner, completely free from clutter."
            )
        ]
        return {
            "tier": "report_commerce_tripwire",
            "tier_display": "Cash Flow Gap & Velocity Unblocker (3-Page Action Guide)",
            "domain": "Money Flow, Business & Career Wealth",
            "planet": "Mercury (Budh)",
            "harmonic_root": 5,
            "price_inr": 149,
            "price_usd": 5.00,
            "profile": profile,
            "page_target": "3 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }

    elif level == "master":
        sections = [
            f"# Commercial Mastery & Enterprise Wealth Dossier\n**Client:** {name} | **Harmonic Root:** 5 | **Edition:** Master 12-Chapter Dossier\n",
            "## Chapter 1: Commercial Energetic Matrix & Capital Flow",
            (
                f"Operating with natal Root {driver} ({d_planet}) and Path {conductor}, your commercial capacity is designed for systematic asset creation. "
                f"Harmonic Root 5 brings rapid market adaptation, commercial acumen, and negotiation agility. "
                f"This dossier reveals the exact mathematical levers to accelerate financial inflows."
            ),
            "## Chapter 2: Lo Shu Prosperity Planes (4-5-6 & 2-5-8)",
            (
                "• **The Prosperity Arrow (4-5-6):** Balances disciplined planning (4), rapid commerce (5), and material comfort (6).\n"
                "• **The Earth Element Plane (2-5-8):** Anchors real estate stability, cash retention, and asset preservation.\n"
                "• **Action Focus:** Reinforce the center cell (5) to ensure cash circulating into your business stays anchored."
            ),
            "## Chapter 3: Client Payment Delay Neutralization Protocol",
            (
                "• Implement structured weekly follow-ups strictly on Wednesday and Saturday mornings.\n"
                "• Re-anchor debtor agreements with documented legal milestones.\n"
                "• Clear physical paperwork from your left desk corner to remove energy stagnation."
            ),
            "## Chapter 4: Annual Business Timing & Expansion Radar",
            (
                "• **Quarter 1:** Streamlining operations, auditing leakages, and eliminating unprofitable clients.\n"
                "• **Quarter 2:** Prime commercial expansion window; launching new offerings or negotiating major contracts.\n"
                "• **Quarter 3–4:** Solidifying profit reserves and long-term asset compounding."
            ),
            "## Chapter 5: Sacred Non-Commercial Wealth Harmonizers",
            (
                "• Drink water from a pure green or glass vessel on Wednesdays.\n"
                "• Keep an emerald green or aventurine crystal on your work desk facing North.\n"
                "• Donate green lentils or feed green grass to cows on Wednesday mornings."
            )
        ]
        return {
            "tier": "report_commerce_master",
            "tier_display": "Commercial Mastery Dossier (12-Page Master Report)",
            "domain": "Money Flow, Business & Career Wealth",
            "planet": "Mercury (Budh)",
            "harmonic_root": 5,
            "price_inr": 599,
            "price_usd": 23.00,
            "profile": profile,
            "page_target": "12 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }

    else:  # sovereign
        sections = [
            f"# Enterprise Scaling & Commercial Brand Matrix\n**Client:** {name} | **Edition:** 32-Page Sovereign Architecture Blueprint\n",
            "## Chapter 1: Corporate Entity & Brand Numerical Architecture",
            (
                f"Welcome, {name}. This 32-page sovereign dossier provides institutional-grade commercial numerological architecture. "
                f"Designed for founders, enterprise leaders, and serious wealth builders, it aligns corporate registration, brand naming, "
                f"and partner synastry into a unified financial multiplier."
            ),
            "## Chapter 2: GST Entity Name & Brand Acoustic Sound Alignment",
            (
                "• **Trade Name Sound Value:** Harmonizing your brand name to compound numbers 23, 32, or 37 (high commercial velocity).\n"
                "• **Legal Entity Calibration:** Removing karmic friction numbers (14, 16, 28) from registered corporate entities."
            ),
            "## Chapter 3: Co-Founder & Key Investor Synergy Matrix",
            (
                "• Cross-matching birth dates of key partners to identify natural executive and financial divisions.\n"
                "• Ensuring lead negotiator holds favorable Mercury/Sun resonance."
            ),
            "## Chapter 4: Bank Account & Domain Name Numerology Audit",
            (
                "• Evaluating primary operating bank account number sum.\n"
                "• Aligning primary web domain letter count and phonetic vibration."
            ),
            "## Chapter 5: Multi-Decade Wealth Compounding Blueprint",
            (
                "• 10-Year commercial macro radar with auspicious asset deployment years.\n"
                "• Complete tax, reserve, and ethical wealth stewardship guidelines."
            )
        ]
        return {
            "tier": "report_commerce_sovereign",
            "tier_display": "Enterprise Scaling & Brand Matrix (32-Page Master Blueprint)",
            "domain": "Money Flow, Business & Career Wealth",
            "planet": "Mercury (Budh)",
            "harmonic_root": 5,
            "price_inr": 5999,
            "price_usd": 140.00,
            "profile": profile,
            "page_target": "32 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }


# ─────────────────────────────────────────────────────────────────────────────
# 3. SUN (SURYA) — EXECUTIVE AUTHORITY & CAREER SOVEREIGNTY (ROOT 1)
# ─────────────────────────────────────────────────────────────────────────────
def _generate_authority_report(level: str, name: str, day: int, month: int, year: int, driver: int, conductor: int, d_planet: str, c_planet: str, profile: dict) -> dict:
    if level == "tripwire":
        sections = [
            f"# Career Authority & Promotion Gap Unblocker\n**Prepared for:** {name} | **Harmonic Root:** 1 (Solar Sovereignty) | **Format:** 3-Page Action Plan\n",
            "## 1. Authority Alignment & Office Politics Neutralization",
            (
                f"Welcome, {name}. Your natal vibration Root {driver} carries strong executive ambition. "
                f"Career stagnation occurs when your natural leadership is perceived as threatening or misaligned with organizational politics. "
                f"Sun energy commands respect through consistent dignified execution, not loud contention."
            ),
            "## 2. Promotion & Performance Appraisal Timing Windows",
            (
                "• **Optimal Presentation Windows:** Present major achievements and compensation proposals on Tuesdays or Sundays.\n"
                "• **Executive Summary Format:** Always communicate in brief, executive-level summaries focusing on bottom-line outcomes."
            ),
            "## 3. Morning Solar Vitality Guide",
            (
                "• **Morning Sun Attunement:** Stand facing East for 10 minutes before 8:00 AM every morning.\n"
                "• **Auspicious Palette:** Wear warm yellow, gold, saffron, or copper tones on critical career days; avoid muddy brown."
            ),
            "## 4. Executive East Desk Facing Vector",
            (
                "• Position your desk so your back is against a solid wall and your face looks directly East or North.\n"
                "• Keep your workspace clear of broken pens, dead electronic devices, and cluttered cables."
            )
        ]
        return {
            "tier": "report_authority_tripwire",
            "tier_display": "Career Authority Gap Unblocker (3-Page Action Guide)",
            "domain": "Job Promotion, Leadership & Authority",
            "planet": "Sun (Surya)",
            "harmonic_root": 1,
            "price_inr": 199,
            "price_usd": 10.00,
            "profile": profile,
            "page_target": "3 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }

    elif level == "master":
        sections = [
            f"# Sovereign Leadership & Executive Career Dossier\n**Client:** {name} | **Harmonic Root:** 1 | **Edition:** Master 12-Chapter Dossier\n",
            "## Chapter 1: The Executive Mandate & Solar Blueprint",
            (
                f"Operating with natal Root {driver} ({d_planet}) and Path {conductor}, you are designed for institutional leadership. "
                f"Harmonic Root 1 activates executive command, public respect, and high-stakes decision-making. "
                f"This dossier provides strategic career roadmaps to transition from individual contributor to undisputed authority."
            ),
            "## Chapter 2: Lo Shu 1-5-9 Will & Leadership Plane",
            (
                "• **The Will Plane (1-5-9):** Represents determination (1), communication velocity (5), and courage (9).\n"
                "• **Balancing Focus:** Harmonizing the 1-5-9 plane ensures your decisions are respected across senior executive levels."
            ),
            "## Chapter 3: 5-Year Professional Career Dasha Radar",
            (
                "• **Current Period:** Deep foundation building, high-impact deliverables, and strategic alliance formation.\n"
                "• **Upcoming Promotion Window:** Major leadership appointment, public elevation, or executive title transition.\n"
                "• **Strategic Career Shield:** Documentation of milestones to protect against credit hijacking."
            ),
            "## Chapter 4: Solar Gayatri & Authority Consecration",
            (
                "• Drink water from a pure copper vessel every morning.\n"
                "• Recite the morning Gayatri or solar invocation at sunrise.\n"
                "• Keep a clean brass or copper sun medallion on your office wall facing East."
            )
        ]
        return {
            "tier": "report_authority_master",
            "tier_display": "Sovereign Leadership Dossier (12-Page Master Report)",
            "domain": "Job Promotion, Leadership & Authority",
            "planet": "Sun (Surya)",
            "harmonic_root": 1,
            "price_inr": 550,
            "price_usd": 28.00,
            "profile": profile,
            "page_target": "12 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }

    else:  # sovereign
        sections = [
            f"# Sovereign Identity & Name Rectification Blueprint\n**Client:** {name} | **Edition:** 32-Page Master Life Transformation\n",
            "## Chapter 1: Sovereign Executive Architecture",
            (
                f"Welcome, {name}. This 32-page sovereign executive blueprint is tailored for corporate C-suite executives, "
                f"public leaders, and visionary entrepreneurs. It provides complete career trajectory optimization, "
                f"including professional name spelling harmonization to maximize authority and command."
            ),
            "## Chapter 2: Professional Name Spelling Rectification for Authority",
            (
                "• **Chaldean Compound Sum Analysis:** Auditing current legal name and calling name.\n"
                "• **Spelling Harmonization:** Introducing 3 certified spelling variations that reduce to royal compounds (19, 23, or 37).\n"
                "• **Transition Protocol:** Official affidavit and social signature transition guide."
            ),
            "## Chapter 3: Public Stature & Government Career Roadmap",
            (
                "• Detailed 10-year leadership timeline with favorable executive appointment windows.\n"
                "• Navigating regulatory scrutiny, institutional governance, and public perception."
            )
        ]
        return {
            "tier": "report_authority_sovereign",
            "tier_display": "Sovereign Identity & Name Rectification (32-Page Master Blueprint)",
            "domain": "Job Promotion, Leadership & Authority",
            "planet": "Sun (Surya)",
            "harmonic_root": 1,
            "price_inr": 5500,
            "price_usd": 190.00,
            "profile": profile,
            "page_target": "32 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }


# ─────────────────────────────────────────────────────────────────────────────
# 4. MERCURY / VENUS — GLOBAL HORIZON & RELOCATION (ROOT 5 & 6)
# ─────────────────────────────────────────────────────────────────────────────
def _generate_relocation_report(level: str, name: str, day: int, month: int, year: int, driver: int, conductor: int, d_planet: str, c_planet: str, profile: dict) -> dict:
    if level == "tripwire":
        sections = [
            f"# International Visa & Travel Timing Guide\n**Prepared for:** {name} | **Harmonic Root:** 5 & 6 | **Format:** 3-Page Action Plan\n",
            "## 1. Favorable Visa Lodgment & Submission Windows",
            (
                f"Welcome, {name}. Relocating abroad requires favorable planetary mobility. "
                f"Your natal chart combines Root {driver} with Path {conductor}. "
                f"Visa processing delays often happen when applications are submitted during retrograde or friction hours. "
                f"Submitting your documentation during peak favorable travel windows accelerates bureaucratic clearances."
            ),
            "## 2. Compass Direction Alignment for Target Countries",
            (
                "• **North-West Vector (Air & Movement):** Ideal for North America, UK, and European immigration aspirations.\n"
                "• **South-East Vector (Expansion & Commerce):** Ideal for UAE, Singapore, and Far East commercial relocations."
            ),
            "## 3. Travel Plane Neutralization for Delays",
            (
                "• Keep passport and critical immigration dossiers wrapped in a clean yellow or cream silk cloth.\n"
                "• Never store travel documents in basement or low-lying dark drawers."
            ),
            "## 4. Auspicious Departure & Flying Timing",
            (
                "• Departure dates reducing to 3, 5, or 6 bring smooth airport transitions and welcoming hosts."
            )
        ]
        return {
            "tier": "report_relocation_tripwire",
            "tier_display": "International Visa & Travel Guide (3-Page Action Guide)",
            "domain": "Foreign Settlement, Visa & Travel",
            "planet": "Mercury & Rahu",
            "harmonic_root": 5,
            "price_inr": 149,
            "price_usd": 5.00,
            "profile": profile,
            "page_target": "3 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }

    elif level == "master":
        sections = [
            f"# Global Settlement & Overseas Relocation Dossier\n**Client:** {name} | **Harmonic Root:** 5 & 6 | **Edition:** Master 12-Chapter Dossier\n",
            "## Chapter 1: The Global Passage & Migration Mandate",
            (
                f"Natal Root {driver} ({d_planet}) and Path {conductor} create strong potential for wealth accumulation in overseas territories. "
                f"Harmonic Roots 5 & 6 activate international mobility, permanent residency (PR), and foreign prosperity."
            ),
            "## Chapter 2: Permanent Residency (PR) & Settlement Timeline",
            (
                "• **Phase 1 (Preparation & Submission):** Documentation validation, language testing, and visa filing.\n"
                "• **Phase 2 (Approval Window):** Peak astrological transition window when clearances arrive smoothly.\n"
                "• **Phase 3 (Physical Relocation):** Auspicious arrival dates ensuring immediate employment and housing."
            ),
            "## Chapter 3: Overseas Living & Relocation Vastu Vectors",
            (
                "• Selecting overseas apartments aligned with favorable entry directions.\n"
                "• Establishing a grounding sanctuary in foreign lands to prevent homesickness and cultural friction."
            )
        ]
        return {
            "tier": "report_relocation_master",
            "tier_display": "Global Settlement Dossier (12-Page Master Report)",
            "domain": "Foreign Settlement, Visa & Travel",
            "planet": "Mercury & Rahu",
            "harmonic_root": 6,
            "price_inr": 489,
            "price_usd": 24.00,
            "profile": profile,
            "page_target": "12 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }

    else:  # sovereign
        sections = [
            f"# Sovereign Global Migration Matrix\n**Client:** {name} | **Edition:** 32-Page Master Migration Blueprint\n",
            "## Chapter 1: Sovereign Global Citizen Architecture",
            (
                f"Welcome, {name}. This 32-page sovereign migration matrix provides comprehensive strategic planning for "
                f"multi-country living, global citizenship, international asset allocation, and passport name vibration alignment."
            ),
            "## Chapter 2: Passport Name Spelling & International Vibration",
            (
                "• Ensuring Latin spelling of your legal passport matches international commercial frequency 24 or 33.\n"
                "• Eliminating acoustic friction during foreign immigration and bank onboarding."
            ),
            "## Chapter 3: Multi-Country Synastry & Relocation Mapping",
            (
                "• Mathematical compatibility scoring between your birth chart and target destinations (USA, Canada, UK, UAE, Australia).\n"
                "• Tax residency and permanent wealth sanctuary strategy."
            )
        ]
        return {
            "tier": "report_relocation_sovereign",
            "tier_display": "Sovereign Global Migration Matrix (32-Page Master Blueprint)",
            "domain": "Foreign Settlement, Visa & Travel",
            "planet": "Mercury & Rahu",
            "harmonic_root": 6,
            "price_inr": 5100,
            "price_usd": 150.00,
            "profile": profile,
            "page_target": "32 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }


# ─────────────────────────────────────────────────────────────────────────────
# 5. JUPITER (GURU) — HIGHER CALLING & MENTORSHIP (ROOT 3)
# ─────────────────────────────────────────────────────────────────────────────
def _generate_dharma_report(level: str, name: str, day: int, month: int, year: int, driver: int, conductor: int, d_planet: str, c_planet: str, profile: dict) -> dict:
    if level == "tripwire":
        sections = [
            f"# Dharma Compass & Life Purpose Unblocker\n**Prepared for:** {name} | **Harmonic Root:** 3 (Jupiter Wisdom) | **Format:** 3-Page Action Plan\n",
            "## 1. Life Purpose & Core Natal Mission Alignment",
            (
                f"Welcome, {name}. Your chart combines Root {driver} with Path {conductor}. "
                f"When seekers experience spiritual confusion or a feeling of 'What is my real purpose?', "
                f"it indicates that their intellectual activity is disconnected from their soul dharma. "
                f"Jupiter (Guru) represents moral integrity, wisdom, counseling, and teaching."
            ),
            "## 2. Spiritual Blockage & Confusion Neutralization",
            (
                "• Spend 15 minutes weekly mentoring or guiding someone younger without expecting financial return.\n"
                "• Read 5 pages of classical philosophical literature every Thursday evening."
            ),
            "## 3. Thursday Wisdom Sadhana & Yellow Attunement",
            (
                "• **Auspicious Color:** Wear bright yellow, golden, or saffron tones every Thursday.\n"
                "• **Dietary Harmony:** Consume warm turmeric milk or saffron water on Thursday mornings."
            ),
            "## 4. Wisdom Sanctuary & Meditation Orientation",
            (
                "• Orient your meditation or reading space facing North-East (the sacred Ishanya corner).\n"
                "• Keep the North-East corner pristine, quiet, and illuminated with warm soft light."
            )
        ]
        return {
            "tier": "report_dharma_tripwire",
            "tier_display": "Dharma Compass & Purpose Unblocker (3-Page Action Guide)",
            "domain": "Life Purpose, Peace of Mind & Spiritual Growth",
            "planet": "Jupiter (Guru)",
            "harmonic_root": 3,
            "price_inr": 120,
            "price_usd": 12.00,
            "profile": profile,
            "page_target": "3 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }

    elif level == "master":
        sections = [
            f"# Sovereign Wisdom & Soul Path Dossier\n**Client:** {name} | **Harmonic Root:** 3 | **Edition:** Master 12-Chapter Dossier\n",
            "## Chapter 1: The Dharmic Calling & Spiritual Mandate",
            (
                f"Natal Root {driver} ({d_planet}) and Path {conductor} create an individual with natural moral authority. "
                f"Harmonic Root 3 connects your life path directly to Guru energy—bringing peace of mind, ethical prosperity, and ancestral grace."
            ),
            "## Chapter 2: Thought & Spiritual Plane Lo Shu Integration",
            (
                "• **The Thought Plane (4-3-8):** Governs memory, wisdom, and intellectual depth.\n"
                "• **Balancing Focus:** Harmonizing the 4-3-8 plane clears mental anxiety and establishes lasting inner serenity."
            ),
            "## Chapter 3: Ancestral Karma (Pitra) Balancing Protocol",
            (
                "• Respecting ancestral lineages through monthly water offering (Tarpan) or community feeding on Amavasya.\n"
                "• Neutralizing inherited karmic debts to unblock generational prosperity."
            ),
            "## Chapter 4: Higher Education & Mentorship Radar",
            (
                "• Favorable windows for advanced certifications, authoring books, or stepping into counseling roles."
            )
        ]
        return {
            "tier": "report_dharma_master",
            "tier_display": "Sovereign Wisdom Dossier (12-Page Master Report)",
            "domain": "Life Purpose, Peace of Mind & Spiritual Growth",
            "planet": "Jupiter (Guru)",
            "harmonic_root": 3,
            "price_inr": 570,
            "price_usd": 30.00,
            "profile": profile,
            "page_target": "12 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }

    else:  # sovereign
        sections = [
            f"# Karmic Destiny & Spiritual Life Blueprint\n**Client:** {name} | **Edition:** 32-Page Master Life Transformation Blueprint\n",
            "## Chapter 1: Karmic Destiny Architecture",
            (
                f"Welcome, {name}. This 32-page sovereign spiritual blueprint maps your complete soul evolution across multiple decades. "
                f"It integrates multi-decade personal year cycles, sacred natal harmonic trines, and Chaldean name vibrations "
                f"to guide your journey toward ethical fulfillment and lasting inner peace."
            ),
            "## Chapter 2: Spiritual Name Vibration & Acoustic Resonance",
            (
                "• Harmonizing your spiritual and public name to resonant numbers 21 or 24.\n"
                "• Illuminating intuitive clarity and spiritual leadership."
            ),
            "## Chapter 3: Multi-Decade Soul Evolution & Dharma Timeline",
            (
                "• Comprehensive 20-year spiritual roadmap with favorable enlightenment and philanthropic milestones."
            )
        ]
        return {
            "tier": "report_dharma_sovereign",
            "tier_display": "Karmic Destiny Blueprint (32-Page Master Roadmap)",
            "domain": "Life Purpose, Peace of Mind & Spiritual Growth",
            "planet": "Jupiter (Guru)",
            "harmonic_root": 3,
            "price_inr": 4800,
            "price_usd": 120.00,
            "profile": profile,
            "page_target": "32 Pages",
            "report_markdown": sanitize_text("\n\n".join(sections))
        }
