"""
PACKAGE-WISE DETAILED REPORT GENERATION ENGINE
Numeros Vision — ANVEIL EVERY CHARM

PURPOSE:
Generates complete, publication-ready, detailed customer reports for all 5 product tiers:
1. Free Tier (Discovery Blueprint)
2. Starter Pass (₹95 — 5 In-Depth Questions, Actionable Strategy)
3. Growth Pass (₹399 — 10 Questions + Full Actionable Remedies + Favorable Timelines)
4. Complete Personal Destiny Blueprint Report (₹1,050 — 8-Chapter Comprehensive Master Dossier)
5. 1-on-1 Master Personal Consultation (₹11,400 — Executive Dossier with Birth Time Verification)

ALL REPORTS STRICTLY ADHERE TO DIPLOMATIC HARMONIZATION PRINCIPLES:
- Zero technical astrology/numerology jargon
- No engine or calculation method attribution
- Negative situations diplomatically reframed as temporary energetic blockages
- Immediate practical solutions (networking, budgeting, calm communication, grounding)
- Gentle supportive framing without over-promising or guaranteed cures
- Zero defensive/ugly disclaimers (dignified empowerment standard)
"""

import hashlib
import json
from typing import Dict, Any, List, Optional
from app.engine.diplomatic_narrative_engine import sanitize_text, DOMAIN_ACTION_GUIDANCE, create_diplomatic_narrative
from app.engine.consensus import generate_consensus_reading
from app.engine.question_explanation_engine import generate_simple_explanation_and_remedies
from app.engine.planetary_package_reports import is_planetary_package, generate_planetary_domain_report
from app.engine.core_matrix_engine import calculate_age_numerology
from app.engine.lo_shu import generate_loshu_grid_markdown
from app.engine.lunar_paksha_engine import calculate_shukla_paksha_timing
from app.engine.international_remedy_engine import get_international_planetary_remedies, analyze_english_name_acoustics


def _finalize_report_envelope(
    report: Dict[str, Any],
    clean_tier: str,
    clean_name: str,
    day: int,
    month: int,
    year: int,
    driver: int,
    conductor: int
) -> Dict[str, Any]:
    md = report.get("report_markdown", "")
    if "ANVEIL EVERY CHARM" not in md:
        if "ANVEIL EVERY CHARM" in md:
            md = md.replace("ANVEIL EVERY CHARM", "ANVEIL EVERY CHARM")
        else:
            md = f"**Numeros Vision · ANVEIL EVERY CHARM**\n\n{md}"
    elif "ANVEIL EVERY CHARM" in md:
        md = md.replace("ANVEIL EVERY CHARM", "ANVEIL EVERY CHARM")
    report["report_markdown"] = md

    corpus_release_id = "release-2026.10-v1.3"
    index_generation_id = "bm25-pgvector-10826-v1.3"
    report_id = f"NV-RPT-{hashlib.sha256(f'{clean_tier}:{clean_name}:{day}:{month}:{year}'.encode('utf-8')).hexdigest()[:12].upper()}"
    evidence_pack = {
        "corpus_release_id": corpus_release_id,
        "index_generation_id": index_generation_id,
        "driver_number": driver,
        "conductor_number": conductor,
        "tier": clean_tier,
        "verified_rules_applied": ["RULE_DRIVER_CALC_V1", "RULE_CONDUCTOR_CALC_V1", "RULE_LOSHU_GRID_V1"]
    }
    evidence_pack_hash = hashlib.sha256(json.dumps(evidence_pack, sort_keys=True).encode("utf-8")).hexdigest()
    artifact_hash = hashlib.sha256(md.encode("utf-8")).hexdigest()

    report["report_id"] = report_id
    report["report_version"] = "v1.3"
    report["corpus_release_id"] = corpus_release_id
    report["index_generation_id"] = index_generation_id
    report["evidence_pack"] = evidence_pack
    report["evidence_pack_hash"] = evidence_pack_hash
    report["artifact_hash"] = artifact_hash
    report["reproducibility_mode"] = "deterministic_snapshot"
    return report



def _is_international_client(birth_city: Optional[str], country: Optional[str] = None) -> bool:
    if country:
        return country.strip().upper() not in ["IN", "INDIA"]
    if not birth_city:
        return False
    city_lower = birth_city.lower()
    indian_indicators = [
        "india", "chennai", "mumbai", "delhi", "bangalore", "bengaluru", "kolkata",
        "hyderabad", "pune", "ahmedabad", "jaipur", "surat", "lucknow", "kanpur",
        "nagpur", "indore", "thane", "bhopal", "patna", "vadodara", "ghaziabad",
        "ludhiana", "agra", "nashik", "faridabad", "meerut", "rajkot", "varanasi",
        "srinagar", "aurangabad", "dhanbad", "amritsar", "navi mumbai", "allahabad",
        "ranchi", "howrah", "coimbatore", "jabalpur", "gwalior", "vijayawada",
        "jodhpur", "madurai", "raipur", "kota", "guwahati", "chandigarh", "noida", "gurgaon"
    ]
    return not any(ind in city_lower for ind in indian_indicators)

def _build_international_report_sections(clean_name: str, driver: int, conductor: int, missing_nums: list) -> List[str]:
    data = get_international_planetary_remedies(driver, conductor, missing_nums, clean_name)
    acoustics = data["english_name_acoustics"]
    d_charity = data["primary_charitable_giving"]["driver_charity"]
    c_charity = data["primary_charitable_giving"]["conductor_charity"]
    prayer = data["universal_contemplative_rituals"]["primary_prayer"]
    destiny_prayer = data["universal_contemplative_rituals"]["destiny_prayer"]
    env = data["environmental_harmonizers"]

    first_acc = acoustics["first_name_acoustic"]
    last_acc = acoustics["last_name_acoustic"]

    sections = [
        "## Chapter 8A: English Name Acoustic Calibration & Signature Architecture",
        (
            f"### Spoken Sound Frequency & Personal Brand Resonance\n"
            f"In Western and Chaldean numerological science, your English name functions as a continuous acoustic broadcast:\n\n"
            f"• **First Name Acoustic ({first_acc['word']}):** Vibrates to Compound {first_acc['compound']} ➔ Root {first_acc['root']}. "
            f"This governs how the professional world perceives and receives you during initial communications, meetings, and introductions.\n"
            f"• **Hereditary Foundation ({last_acc['word']}):** Vibrates to Compound {last_acc['compound']} ➔ Root {last_acc['root']}. "
            f"Represents inherited ancestral resilience and structural reputation.\n"
            f"• **Soul Urge (Vowels):** Compound {acoustics['soul_urge_vowels']['compound']} ➔ Root {acoustics['soul_urge_vowels']['root']}. Reflects inner spiritual drives and private desires.\n"
            f"• **Outer Personality Shield (Consonants):** Compound {acoustics['outer_personality_consonants']['compound']} ➔ Root {acoustics['outer_personality_consonants']['root']}. Represents your public presence.\n\n"
            f"**Professional Signature Calibration Protocol:**\n"
            f"{acoustics['signature_guidance']}"
        ),
        "## Chapter 8B: Planetary Balancing via Altruistic Charitable Giving (Targeted Donations)",
        (
            f"### The Universal Law of Karmic Giving (Planetary Dana)\n"
            f"Across global spiritual and philosophical traditions, charitable giving is the most potent, universally verified mechanism "
            f"to harmonize planetary friction without superstition. By extending assistance to the specific human and environmental domains "
            f"governed by your ruling planets, you dissolve energetic bottlenecks:\n\n"
            f"**1. Primary Solar Driver Balancing ({d_charity['planet']}):**\n"
            f"• **Cause Focus:** {d_charity['cause_focus']}\n"
            f"• **Recommended Action:** {d_charity['recommended_action']}\n"
            f"• **Everyday Act of Generosity:** {d_charity['everyday_generosity']}\n"
            f"• **Auspicious Timing:** {d_charity['timing']}\n"
            f"• **Karmic Intention:** *'{d_charity["karmic_intention"]}'*\n\n"
            f"**2. Destiny Conductor Alignment ({c_charity['planet']}):**\n"
            f"• **Cause Focus:** {c_charity['cause_focus']}\n"
            f"• **Recommended Action:** {c_charity['recommended_action']}\n"
            f"• **Auspicious Timing:** {c_charity['timing']}\n"
            f"• **Karmic Intention:** *'{c_charity["karmic_intention"]}'*"
        ),
        "## Chapter 8C: Universal Contemplative Rituals & Inclusive Prayer of Fortitude",
        (
            f"### Non-Sectarian Contemplative Practice\n"
            f"Calibrated to respect and enrich any religious or philosophical worldview (Christian, Jewish, Interfaith, or Contemplative):\n\n"
            f"**1. Morning Light & Evening Candle Ceremony:**\n"
            f"{prayer['candle_ceremony']}\n\n"
            f"**2. Contemplative Prayer of Purpose:**\n"
            f"> *'{prayer["prayer_text"]}'*\n\n"
            f"**3. Destiny Conductor Prayer:**\n"
            f"> *'{destiny_prayer["prayer_text"]}'*\n\n"
            f"**4. Daily Grounding Affirmation:**\n"
            f"> *'{prayer["daily_affirmation"]}'*"
        ),
        "## Chapter 8D: Solfeggio Sound Frequency Tuning & Spatial Environmental Alignment",
        (
            f"### Vibrational Sanctuary Design\n"
            f"• **Harmonic Sound Frequency:** Listen to **{prayer['sound_frequency']}** during morning meditation or deep work sessions to align cellular coherence.\n"
            f"• **Workspace Orientation:** {env['workspace_orientation']}\n"
            f"• **Harmonious Palette:** Emphasize **{env['power_colors']}** in your wardrobe and desk accessories. Minimize **{env['colors_to_minimize']}** during critical negotiation cycles.\n"
            f"• **Prime Day of Power:** Schedule your highest-stakes contracts and launches on **{env['prime_day_of_action']}**."
        )
    ]
    return sections


def generate_package_report(
    name: str,
    day: int,
    month: int,
    year: int,
    package_tier: str,
    birth_time: Optional[str] = "11:10 AM",
    birth_city: Optional[str] = "Chennai",
    user_questions: Optional[List[str]] = None,
    country: Optional[str] = None
) -> Dict[str, Any]:
    """
    Master generator for package-wise detailed reports.
    """
    clean_tier = package_tier.lower().strip()
    clean_name = name.strip().title() if name else "Friend"
    
    # 1. Background Deterministic Engine Execution (Deep Backend Calculation)
    consensus = generate_consensus_reading(clean_name, day, month, year)
    vedic = consensus.get("vedic_numerology", {})
    lo_shu = consensus.get("lo_shu_grid", {})
    cheiro_name = consensus.get("cheiro_name_analysis", {})
    
    driver = vedic.get("driver_number", 8)
    driver_planet = vedic.get("driver_planet", "Saturn")
    conductor = vedic.get("conductor_number", 8)
    conductor_planet = vedic.get("conductor_planet", "Saturn")
    shukla_info = calculate_shukla_paksha_timing(ruling_planet_num=driver)
    
    # Profile Summary
    profile_summary = {
        "client_name": clean_name,
        "date_of_birth": f"{day:02d}-{month:02d}-{year}",
        "birth_time": birth_time or "11:10 AM",
        "birth_place": birth_city or "Chennai",
        "primary_nature": f"{driver_planet} Core Energy (Root {driver})",
        "life_direction": f"{conductor_planet} Guidance (Path {conductor})"
    }

    # ──────────────────────────────────────────────────────────────────────────
    # PLANETARY & HARMONIC DOMAIN PACKAGES (UNION, COMMERCE, AUTHORITY, ETC.)
    # ──────────────────────────────────────────────────────────────────────────
    if is_planetary_package(clean_tier):
        plan_res = generate_planetary_domain_report(
            clean_tier, clean_name, day, month, year,
            driver, conductor, driver_planet, conductor_planet,
            profile_summary
        )
        return _finalize_report_envelope(plan_res, clean_tier, clean_name, day, month, year, driver, conductor)


    # ──────────────────────────────────────────────────────────────────────────
    # TIER: BASIC NUMEROLOGY REPORT (3 PAGES · ₹199 / $19)
    # Standard 13-Section English-Only Report Structure
    # ──────────────────────────────────────────────────────────────────────────
    elif clean_tier in ["report_essential", "essential", "basic", "basic_report"]:
        age_data = calculate_age_numerology(day, month, year)
        dob_digits = [int(d) for d in f"{day:02d}{month:02d}{year}" if d != "0"]
        loshu_counts = {i: dob_digits.count(i) for i in range(1, 10)}
        missing_nums = [i for i in range(1, 10) if loshu_counts[i] == 0]
        
        report_sections = [
            f"# Basic Numerology Report\n**Prepared for:** {clean_name} | **Date of Birth:** {day:02d}-{month:02d}-{year} | **Report Length:** 3 Pages | **Edition:** Executive PDF Deliverable\n",
            "## 1. Report Overview\n"
            f"This Basic Numerology Report provides an executive summary of your calculated foundational numbers, "
            f"the classical calculation methods applied, and an initial interpretation of the key findings. "
            f"It is designed to give you clarity on your core energetic patterns and practical focus areas.",
            
            "## 2. Personal Details and Calculation Inputs\n"
            f"• **Full Name:** {clean_name}\n"
            f"• **Date of Birth:** {day:02d}-{month:02d}-{year}\n"
            f"• **Recorded Birth Time:** {birth_time or '11:10 AM'}\n"
            f"• **Birth City / Location:** {birth_city or 'Chennai'}\n"
            f"• **Calculation Standard:** Classical Vedic (Mulank & Bhagyank) and Lo Shu Mathematical Matrix",
            
            "## 3. Calculation Method\n"
            f"Your foundational calculations are generated deterministically using verified numerological principles:\n"
            f"• **Driver (Mulank):** Derived from the calendar day of birth ({day:02d}) reduced to a single digit: Root {driver} ({driver_planet}).\n"
            f"• **Conductor (Bhagyank / Life Path Number):** Derived from the complete date sum ({day:02d} + {month:02d} + {year}) reduced to a single digit: Path {conductor} ({conductor_planet}).\n"
            f"• **Lo Shu Grid:** Mapping of birth digits into the ancient 3x3 magic square of Saturn to evaluate elemental balance and missing frequencies.",
            
            "## 4. Calculation Summary\n"
            f"• **Driver Number:** {driver} ({driver_planet})\n"
            f"• **Conductor Number:** {conductor} ({conductor_planet})\n"
            f"• **Current Chronological Age Milestone:** {age_data['age_years']} Years Completed (Navigating Year {age_data['running_year']})\n"
            f"• **Age Compound Number:** {age_data['compound_age']} ➔ Root {age_data['root_age']} ({age_data['root_planet']})\n"
            f"• **Missing Numbers in Grid:** {', '.join(map(str, missing_nums)) if missing_nums else 'None'}",
            
            "## 5. Your Numerology Results\n"
            f"Your core chart is anchored by Driver {driver} and Conductor {conductor}. "
            f"This harmonic pairing reflects disciplined craftsmanship, a natural standard for quality, and a commitment to enduring stability. "
            f"You perform best when actions are structured, clear, and grounded in long-term utility.\n\n"
            f"**Natal Lo Shu 3×3 Grid:**\n" + generate_loshu_grid_markdown(day, month, year),
            
            "## 6. Detailed Interpretation\n"
            f"### Primary Drive and Outer Action\n"
            f"Governed by Driver {driver} ({driver_planet}), you initiate tasks with caution, thoroughness, and self-reliance. "
            f"You prefer verified facts over speculative promises and build your reputation on consistent follow-through.\n\n"
            f"### Life Path and Directional Guidance\n"
            f"Your Conductor {conductor} ({conductor_planet}) shapes your broader life trajectory toward institutional or professional leadership. "
            f"You are guided to compound knowledge and resources patiently rather than chasing fleeting shortcuts.",
            
            "## 7. Key Findings\n"
            f"1. **High Structural Stamina:** Strong capacity to navigate demanding multi-year responsibilities.\n"
            f"2. **Deliberate Decision Pacing:** Your best choices occur when given time to deliberate without emotional haste.\n"
            f"3. **Identified Missing Frequencies:** The absence of digits [ {', '.join(map(str, missing_nums)) if missing_nums else 'None'} ] points to temporary energy leaks that can be balanced through focused habits.",
            
            "## 8. Number Relationships and Patterns\n"
            f"The interaction between Driver {driver} and Conductor {conductor} creates a reinforcing resonance. "
            f"Your inner desires and outer life opportunities work toward the same compounding objectives, minimizing internal contradiction. "
            f"Aligning your daily schedule with your core numbers enhances productivity.",
            
            "## 9. Strengths and Areas for Reflection\n"
            f"• **Core Strengths:** Perseverance, organizational discipline, emotional resilience, strategic patience.\n"
            f"• **Areas for Reflection:** Guard against over-rigidity, perfectionist delays, and keeping concerns unexpressed until tension builds up.",
            
            "## 10. Personalised Recommendations\n"
            f"• **Auspicious Palette:** Deep navy, charcoal, silver, and soft cream.\n"
            f"• **Productive Desk Facing:** Orient your primary workspace facing West or North.\n"
            f"• **Weekly Balance Ritual:** Dedicate time each Saturday to organize your environment and review weekly progress calmly.",
            
            "## 11. Additional Analysis\n"
            f"Your running chronological age reflects Compound {age_data['compound_age']} pointing to {age_data['root_planet']} (Root {age_data['root_age']}). "
            f"{age_data['input_characteristics']['description']} "
            f"This confirms that the present period rewards consolidation and systematic restructuring.",
            
            "## 12. Summary and Next Steps\n"
            f"You possess the natural foundations to build enduring success. "
            f"To explore expanded 5-year planetary timelines, Chaldean sound frequency, and multi-layer remedies, "
            f"consider exploring the **Advanced Numerology Report (12 Pages)** or **Premium Numerology Report (32 Pages)**.",
            
            "## 13. Methodology and Limitations\n"
            f"Calculations are based on traditional Vedic numerology and classical Lo Shu grid principles. "
            f"Numerological analysis provides navigational insight and energetic reflection; "
            f"it does not replace personal judgment, legal counsel, or medical advice."
        ]
        
        return _finalize_report_envelope({
            "tier": "report_essential",
            "tier_display": "Basic Numerology Report",
            "price_inr": 199,
            "profile": profile_summary,
            "pages_count": 3,
            "report_markdown": sanitize_text("\n\n".join(report_sections))
        }, clean_tier, clean_name, day, month, year, driver, conductor)
    

    # ──────────────────────────────────────────────────────────────────────────
    # TIER: ADVANCED NUMEROLOGY REPORT (12 PAGES · ₹489 / $39)
    # Standard 13-Section English-Only Report Structure
    # ──────────────────────────────────────────────────────────────────────────
    elif clean_tier in ["report_master", "master", "advanced", "advanced_report"]:
        age_data = calculate_age_numerology(day, month, year)
        dob_digits = [int(d) for d in f"{day:02d}{month:02d}{year}" if d != "0"]
        loshu_counts = {i: dob_digits.count(i) for i in range(1, 10)}
        missing_nums = [i for i in range(1, 10) if loshu_counts[i] == 0]
        expl_career = generate_simple_explanation_and_remedies("Career stability and expansion", driver, conductor, name=clean_name, day=day, month=month, year=year)
        expl_wealth = generate_simple_explanation_and_remedies("Wealth retention and asset compounding", driver, conductor, name=clean_name, day=day, month=month, year=year)

        report_sections = [
            f"# Advanced Numerology Report\n**Prepared for:** {clean_name} | **Date of Birth:** {day:02d}-{month:02d}-{year} | **Report Length:** 12 Pages | **Edition:** Master Synthesis Dossier\n",
            "## 1. Report Overview\n"
            f"Welcome, {clean_name}. This Advanced Numerology Report delivers a comprehensive dual-system synthesis combining "
            f"classical Vedic Numerology, Chaldean sound frequency analysis, Lo Shu directional trines, and the 5-Year Numerology Dasha timeline. "
            f"It provides expanded interpretations, number relationships, and actionable recommendations.",
            
            "## 2. Personal Details and Calculation Inputs\n"
            f"• **Client Full Name:** {clean_name}\n"
            f"• **Date of Birth:** {day:02d}-{month:02d}-{year}\n"
            f"• **Birth Epoch Time:** {birth_time or '11:10 AM'}\n"
            f"• **Birth Location:** {birth_city or 'Chennai'}\n"
            f"• **Analysis Systems:** Vedic Numerology, Chaldean Syllable Analysis, Lo Shu Grid, Directional 1-5-9 Trines, 5-Year Dasha Timing",
            
            "## 3. Calculation Method\n"
            f"This dossier applies a dual-engine mathematical process:\n"
            f"• **Psychic Driver (Mulank):** Computed as single-digit root of day {day:02d}: {driver} ({driver_planet}).\n"
            f"• **Destiny Conductor (Bhagyank):** Computed from full birth date sum: {conductor} ({conductor_planet}).\n"
            f"• **Chaldean Sound Matrix:** Letter frequencies assigned according to the ancient Chaldean alphabet formula (A,I,J,Q,Y=1; B,K,R=2; C,G,L,S=3; D,M,T=4; E,H,N,X=5; U,V,W=6; O,Z=7; F,P=8).\n"
            f"• **Elemental Vector Dynamics:** 1-5-9 Purpose Trine, 2-10 Wealth Trine, and 3-7-11 Action Trine interactions.",
            
            "## 4. Calculation Summary\n"
            f"• **Driver Number:** {driver} ({driver_planet})\n"
            f"• **Conductor Number:** {conductor} ({conductor_planet})\n"
            f"• **Lo Shu Grid Planes:** 8 Structural Planes Analyzed\n"
            f"• **Age Milestone:** {age_data['age_years']} Years Completed (Year {age_data['running_year']}) | Compound {age_data['compound_age']} ➔ Root {age_data['root_age']} ({age_data['root_planet']})\n"
            f"• **Missing Numbers:** [ {', '.join(map(str, missing_nums)) if missing_nums else 'None'} ]",
            
            "## 5. Your Numerology Results\n"
            f"Your chart reflects an exceptional capacity for institutional leadership, executive responsibility, and long-term asset building. "
            f"The dual presence of {driver_planet} and {conductor_planet} grants you natural authority and disciplined execution.\n\n"
            f"**Natal Lo Shu 3×3 Grid:**\n" + generate_loshu_grid_markdown(day, month, year),
            
            "## 6. Detailed Interpretation\n"
            f"### Professional Arc and Executive Authority\n"
            f"{expl_career['direct_answer']}\n\n"
            f"### Financial Retention and Asset Flow\n"
            f"{expl_wealth['direct_answer']}\n\n"
            f"### Personal Year Trajectory\n"
            f"You are navigating an essential consolidation window where methodical groundwork and eliminating liabilities yield compound returns.",
            
            "## 7. Key Findings\n"
            f"1. **Strategic Compounding:** Your greatest successes come from steady craftsmanship rather than speculative pivots.\n"
            f"2. **Communication Calibration:** Clarifying agreements in writing eliminates ambiguity and protects your professional energy.\n"
            f"3. **Remedial Bridging:** Activating your primary favorable colors, metal resonance, and spatial orientations neutralizes identified grid voids.",
            
            "## 8. Number Relationships and Patterns\n"
            f"The interaction between Driver {driver} and Conductor {conductor} forms a harmonious pillar. "
            f"Your inner drive matches your external circumstances, allowing steady accumulation of skills, reputation, and commercial credibility. "
            f"The 1-5-9 directional vector indicates strong purposeful support when working ethically.",
            
            "## 9. Strengths and Areas for Reflection\n"
            f"• **Strengths:** Executive stamina, unwavering perseverance, analytical depth, ethical craftsmanship.\n"
            f"• **Areas for Reflection:** Guard against isolation under stress, excessive skepticism of new opportunities, and delays caused by perfectionism.",
            
            "## 10. Personalised Recommendations\n"
            f"• **7-Layer Remedial Protocol:**\n"
            f"  1. *Color Therapy:* Wear deep navy, charcoal, or cream on major meeting days.\n"
            f"  2. *Spatial Alignment:* Position desk facing North or West for commercial clarity.\n"
            f"  3. *Mindfulness Practice:* Dedicate 10 minutes each morning to quiet intention.\n"
            f"  4. *Weekly Giving:* Offer selfless community service on Saturdays.\n"
            f"  5. *Acoustic Sound:* Use grounding classical sound frequencies during focused work.",
            
            "## 11. Additional Analysis\n"
            f"### 5-Year Numerology Dasha Timing Windows (2026–2030)\n"
            f"• **Phase 1 (Consolidation & Groundwork):** Deepening expertise and upgrading systems.\n"
            f"• **Phase 2 (Expansion & Visibility):** Professional recognition, network growth, and commercial unlock.\n"
            f"• **Phase 3 (Harvest & Compounding):** Solidifying long-term investments and enjoying institutional authority.",
            
            "## 12. Summary and Next Steps\n"
            f"Your Advanced Numerology Report establishes a clear, verified blueprint for sustained momentum. "
            f"For multi-decade timing maps, advanced Dasha sub-periods, family synastry, and alternative name spelling calibrations, "
            f"explore the **Premium Numerology Report (32 Pages)**.",
            
            "## 13. Methodology and Limitations\n"
            f"This analysis integrates Vedic numerological standards, Chaldean acoustic matrices, and Lo Shu grid systems. "
            f"All findings represent navigational guidance and symbolic insights; they do not constitute legal, medical, or financial warranties."
        ]

        if _is_international_client(birth_city):
            intl_sections = _build_international_report_sections(clean_name, driver, conductor, missing_nums)
            report_sections.extend(intl_sections)
            
        return _finalize_report_envelope({
            "tier": "report_master",
            "tier_display": "Advanced Numerology Report",
            "price_inr": 489,
            "profile": profile_summary,
            "pages_count": 12,
            "report_markdown": sanitize_text("\n\n".join(report_sections))
        }, clean_tier, clean_name, day, month, year, driver, conductor)
    
    # ──────────────────────────────────────────────────────────────────────────
    # TIER 1: FREE DISCOVERY READING
    # ──────────────────────────────────────────────────────────────────────────
    if clean_tier in ["free", "freemium", "discovery"]:
        expl = generate_simple_explanation_and_remedies("Career stability and general direction", driver, conductor, name=clean_name, day=day, month=month, year=year)
        
        # Calculate Natal Lo Shu Grid & Gaps
        dob_digits = [int(d) for d in f"{day:02d}{month:02d}{year}" if d != "0"]
        loshu_counts = {i: dob_digits.count(i) for i in range(1, 10)}
        missing_nums = [i for i in range(1, 10) if loshu_counts[i] == 0]
        
        gap_descriptions = {
            1: "Missing 1 (Water · Career & Initiative): Difficulty asserting individuality; hesitation in taking decisive leadership leaps.",
            2: "Missing 2 (Earth · Intuition & Partnership): Emotional impatience; relationship friction; feeling ungrounded in team dynamics.",
            3: "Missing 3 (Wood · Knowledge & Expression): Creative stagnation; public expression hesitation; under-leveraging personal expertise.",
            4: "Missing 4 (Wood · Rahu Vault & Discipline): Structural wealth leak; high revenue struggles to convert into permanent physical assets.",
            5: "Missing 5 (Earth · Cosmic Center / Brahmasthan): Severe instability in focus; career restlessness; emotional oscillation during stress.",
            6: "Missing 6 (Metal · Venus Luxury Vibration): Delayed comfort manifestation; working hard but experiencing friction in family harmony.",
            7: "Missing 7 (Metal · Ketu Wisdom & Research): Repeating old mistakes; feeling spiritually disconnected; lack of deep analytical anchoring.",
            8: "Missing 8 (Earth · Saturn Discipline & Perseverance): Impatience with long-term execution; episodic financial disruptions.",
            9: "Missing 9 (Fire · Mars Energy & Vitality): Low physical momentum; reluctance to stand in the spotlight; courage and drive void."
        }
        
        detected_gaps_md = []
        for m in missing_nums:
            if m in gap_descriptions:
                detected_gaps_md.append(f"• **{gap_descriptions[m]}**")
        
        if not detected_gaps_md:
            detected_gaps_md.append("• **Harmonious Elemental Balance:** All 9 numerical frequencies present; requires transit synchronization.")

        planes_md = []
        if 4 in missing_nums or 5 in missing_nums or 6 in missing_nums:
            planes_md.append("• **Golden Prosperity Plane (4-5-6) Incomplete:** Wealth enters through Driver/Conductor but leaks before compounding.")
        if 2 in missing_nums or 5 in missing_nums or 8 in missing_nums:
            planes_md.append("• **Silver Real Estate Plane (2-5-8) Void:** Periodic delays in property acquisitions and emotional grounding.")
        if 9 in missing_nums or 5 in missing_nums or 1 in missing_nums:
            planes_md.append("• **Will & Persistence Plane (9-5-1) Disrupted:** Difficulty finishing ambitious multi-year projects.")

        # Deterministic Chronological Age Numerology
        age_data = calculate_age_numerology(day, month, year, missing_numbers=missing_nums)

        report_sections = [
            f"# Personal Energy Discovery Blueprint\n**Prepared for:** {clean_name} | **Date of Birth:** {day:02d}-{month:02d}-{year} | **Access Level:** Free Discovery Reading\n",
            "### 1. Foundational Energy Profile",
            (
                f"Welcome, {clean_name}. Your foundational natural frequency is governed by **Psychic Driver {driver}** ({driver_planet}) directing your energy toward **Destiny Conductor {conductor}** ({conductor_planet}). "
                f"You possess natural resilience, a high standard for quality, and a profound capacity for long-term focus. "
                f"Your life path is oriented toward structured compounding and building enduring security."
            ),
            "### 2. Natal Lo Shu 3×3 Grid & Unlocked Gap Analysis",
            (
                f"Your birth date ({day:02d}-{month:02d}-{year}) projects into the sacred 3×3 Lo Shu Matrix as follows:\n\n"
                f"```\n"
                f"┌──────────────┬──────────────┬──────────────┐\n"
                f"│ 4 (Wood) : {loshu_counts[4]} │ 9 (Fire) : {loshu_counts[9]} │ 2 (Earth): {loshu_counts[2]} │\n"
                f"├──────────────┼──────────────┼──────────────┤\n"
                f"│ 3 (Wood) : {loshu_counts[3]} │ 5 (Earth): {loshu_counts[5]} │ 7 (Metal): {loshu_counts[7]} │\n"
                f"├──────────────┼──────────────┼──────────────┤\n"
                f"│ 8 (Earth): {loshu_counts[8]} │ 1 (Water): {loshu_counts[1]} │ 6 (Metal): {loshu_counts[6]} │\n"
                f"└──────────────┴──────────────┴──────────────┘\n"
                f"```\n\n"
                f"**✦ Unlocked Natal Gap Diagnostic Reading:**\n"
                f"Identified Missing Digits: **[ {', '.join(map(str, missing_nums)) if missing_nums else 'None'} ]**\n\n"
                + "\n".join(detected_gaps_md) + "\n\n"
                + (("\n".join(planes_md) + "\n\n") if planes_md else "")
                + "These unsealed voids explain why recurring friction, financial delays, or emotional oscillations emerge even when your conscious intentions are focused."
            ),
            "### 3. Current Age Number Vibrational Frequency",
            (
                f"**Chronological Age Milestone:** {age_data['age_years']} Years Completed (Navigating Year {age_data['running_year']})\n\n"
                f"• **Input Characteristics (Compound Age Number {age_data['compound_age']}):**\n"
                f"  {age_data['input_characteristics']['description']}\n\n"
                f"• **Output Manifestation (Sum Total Root {age_data['root_age']} · {age_data['root_planet']}):**\n"
                f"  {age_data['output_characteristics']['manifestation']}\n\n"
                f"• **Karmic Gap Synthesis:**\n"
                f"  {age_data['gap_analysis']['diagnosis']}"
            ),
            "### 4. The Lucky Charm Activation Hook",
            (
                f"Your Driver {driver} and Conductor {conductor} contain extraordinary innate capacity. However, the elemental voids identified in your Lo Shu grid "
                f"cause vital energy, timing, and wealth to leak away prematurely. Generic advice or generic gemstones cannot seal these voids.\n\n"
                f"To bridge these missing numbers, your chart specifically requires your **Sacred Custom Lucky Charm**—a consecrated synthesis of your "
                f"specific planetary metal alloy, sacred beej mantra sound vibrations, and auspicious wearing orientations calibrated exclusively to your birth matrix."
            ),
            "### 5. 🔒 Personalized Lucky Charm & Deep Remedial Blueprint Locked",
            (
                f"Your bespoke Lucky Charm activation protocol, consecrated planetary metal alloy, sacred beej mantra frequencies, "
                f"and 2026–2030 favorable transit roadmap to neutralize Gap [ {', '.join(map(str, missing_nums)) if missing_nums else 'All'} ] are compiled in your **Master Synthesis Dossier**.\n\n"
                f"**NUMEROS VISION · ANVEIL EVERY CHARM**\n\n"
                f"[ANVEIL EVERY CHARM ✦ Activate Lucky Charm Dossier (₹489)](/checkout/?plan=report_master)"
            )
        ]
        
        return _finalize_report_envelope({
            "tier": "free",
            "tier_display": "Free Discovery Reading",
            "price_inr": 0,
            "profile": profile_summary,
            "report_markdown": sanitize_text("\n\n".join(report_sections))
        }, clean_tier, clean_name, day, month, year, driver, conductor)

    # ──────────────────────────────────────────────────────────────────────────
    # TIER 2: STARTER PASS (₹95 — 5 In-Depth Questions)
    # ──────────────────────────────────────────────────────────────────────────
    elif clean_tier in ["starter", "starter_5q", "5q"]:
        age_data = calculate_age_numerology(day, month, year)
        questions = user_questions or [
            "When will job stability and long-term career growth materialize?",
            "How can I plug financial leakages and retain my earnings?",
            "What is the best way to handle workplace communications and superiors?",
            "Which directional alignment will improve my daily focus and productivity?",
            "When does my next major favorable expansion window open?"
        ]
        
        q_results = []
        for i, q in enumerate(questions[:5], 1):
            expl = generate_simple_explanation_and_remedies(q, driver, conductor, name=clean_name, day=day, month=month, year=year)
            q_results.append(
                f"### Query {i}: {q}\n"
                f"**Navigational Guidance:**\n{expl['direct_answer']}\n\n"
                f"**Why This Phase Is Unfolding:**\n{expl['why_this_is_happening']['root_cause_explanation']}\n\n"
                f"**Strategic Action Focus:**\n"
                f"• Proactive professional diplomacy and documented project clarity.\n"
                f"• Focused mastery in one high-value domain rather than rapid, speculative pivots.\n"
                f"• Consistent, paced follow-through."
            )
            
        report_sections = [
            f"# Starter 5-Question Predictive Guidance\n**Prepared for:** {clean_name} | **Pass Tier:** Starter (₹95)\n",
            "## 1. Executive Summary",
            (
                f"Welcome, {clean_name}. This personalized guidance dossier addresses your 5 primary questions. "
                f"Your chart reflects high capability for enduring leadership and structured growth. "
                f"The answers below outline practical strategies to convert current friction into lasting momentum."
            ),
            "## 2. Natal Lo Shu Grid Birth Chart & Elemental Matrix",
            generate_loshu_grid_markdown(day, month, year),
            "## 3. Chronological Age Frequency & Manifestation Radar",
            (
                f"**Chronological Age Milestone:** {age_data['age_years']} Years Completed (Navigating Year {age_data['running_year']})\n\n"
                f"• **Input Characteristics (Compound Age Number {age_data['compound_age']}):**\n"
                f"  {age_data['input_characteristics']['description']}\n\n"
                f"• **Output Manifestation (Sum Total Root {age_data['root_age']} · {age_data['root_planet']}):**\n"
                f"  {age_data['output_characteristics']['manifestation']}\n\n"
                f"• **Karmic Gap Synthesis & Lo Shu Interaction:**\n"
                f"  {age_data['gap_analysis']['diagnosis']}"
            ),
            "## 4. Your 5 Detailed Query Answers\n" + "\n\n---\n\n".join(q_results),
            "## Next Steps for Enhanced Results",
            (
                "To access personalized, step-by-step physical remedies, gemstone attunement, and spatial energetic balancing, "
                "you can upgrade Smoothly to the **Growth Pass (₹399)** or the **Complete Personal Destiny Blueprint (₹1,050)**."
            )
        ]
        
        return _finalize_report_envelope({
            "tier": "starter_5q",
            "tier_display": "Starter Pass — 5 Questions",
            "price_inr": 95,
            "profile": profile_summary,
            "questions_answered": len(questions[:5]),
            "report_markdown": sanitize_text("\n\n".join(report_sections))
        }, clean_tier, clean_name, day, month, year, driver, conductor)

    # ──────────────────────────────────────────────────────────────────────────
    # TIER 3: GROWTH PASS (₹399 — 10 Questions + Full Multi-Layer Remedies)
    # ──────────────────────────────────────────────────────────────────────────
    elif clean_tier in ["growth", "growth_10q", "10q"]:
        age_data = calculate_age_numerology(day, month, year)
        questions = user_questions or [
            "When will job stability and long-term career growth materialize?",
            "How can I plug financial leakages and retain my earnings?",
            "What is the best way to handle workplace communications and superiors?",
            "Which directional alignment will improve my daily focus and productivity?",
            "When does my next major favorable expansion window open?",
            "How can I enhance emotional harmony and mutual understanding in relationships?",
            "What lifestyle adjustments will protect my energy against mental fatigue?",
            "Is this period favorable for property acquisition or relocation?",
            "How should I navigate strategic partnerships and collaborative investments?",
            "What is the overarching theme of my current personal year cycle?"
        ]

        q_results = []
        for i, q in enumerate(questions[:10], 1):
            expl = generate_simple_explanation_and_remedies(q, driver, conductor, name=clean_name, day=day, month=month, year=year)
            rem_list = expl.get("remedies", [])
            remedy_bullets = "\n".join([f"  - **{r['title']}:** {r['instruction']}" for r in rem_list[:2]]) if rem_list else "  - Practice consistent morning mindfulness and workspace decluttering."
            
            q_results.append(
                f"### Query {i}: {q}\n"
                f"**Navigational Guidance:**\n{expl['direct_answer']}\n\n"
                f"**Energetic Dynamic:**\n{expl['why_this_is_happening']['root_cause_explanation']}\n\n"
                f"**Supportive Lifestyle & Practical Adjustments:**\n{remedy_bullets}"
            )

        report_sections = [
            f"# Growth Guidance & Full Remedies Dossier\n**Prepared for:** {clean_name} | **Pass Tier:** Growth (₹399)\n",
            "## 1. Executive Overview & Energetic Posture",
            (
                f"Welcome, {clean_name}. You are operating in a foundational consolidation cycle. "
                f"Your energetic blueprint carries the formidable perseverance of Root {driver} ({driver_planet}) "
                f"moving toward Path {conductor}. The combination demands integrity, patient craftsmanship, and emotional balance. "
                f"Applying the paired real-world strategies and subtle remedies below clears energetic resistance and enhances your receptivity to upcoming opportunities."
            ),
            "## 2. Natal Lo Shu Grid Birth Chart & Elemental Synergy",
            generate_loshu_grid_markdown(day, month, year),
            "## 3. Chronological Age Frequency & Manifestation Radar",
            (
                f"**Chronological Age Milestone:** {age_data['age_years']} Years Completed (Navigating Year {age_data['running_year']})\n\n"
                f"• **Input Characteristics (Compound Age Number {age_data['compound_age']}):**\n"
                f"  {age_data['input_characteristics']['description']}\n\n"
                f"• **Output Manifestation (Sum Total Root {age_data['root_age']} · {age_data['root_planet']}):**\n"
                f"  {age_data['output_characteristics']['manifestation']}\n\n"
                f"• **Karmic Gap Synthesis & Lo Shu Interaction:**\n"
                f"  {age_data['gap_analysis']['diagnosis']}"
            ),
            "## 4. In-Depth Answers & Tailored Remedies for 10 Key Areas\n" + "\n\n---\n\n".join(q_results),
            "## 5. Comprehensive Energy Alignment Protocol",
            (
                "• **Auspicious Palette:** Incorporate deep navy, charcoal, silver, and soft cream in daily clothing.\n"
                "• **Favorable Timing:** Saturdays and Wednesdays are your prime days for strategic planning, contract reviews, and deep work.\n"
                "• **Spatial Focus:** Place your desk facing West or North to anchor commercial focus and decision-making clarity.\n"
                "• **Harmonic Bridge Practice:** Dedicate 15 minutes weekly to quiet contemplation or community giving to keep energy flowing fluidly.\n\n"
                f"### Sacred Consecration Muhurta (Shukla Paksha Initiation Window)\n{shukla_info['guidance_narrative']}"
            ),
            "## 4. Closing Perspective",
            (
                "Planetary cycles reveal the currents of time, but your thoughtful diplomacy, perseverance, and conscious choices "
                "guide the ship. Carry these practices forward with quiet confidence."
            )
        ]

        return _finalize_report_envelope({
            "tier": "growth_10q",
            "tier_display": "Growth Pass — 10 Questions + Full Remedies",
            "price_inr": 399,
            "profile": profile_summary,
            "questions_answered": len(questions[:10]),
            "report_markdown": sanitize_text("\n\n".join(report_sections))
        }, clean_tier, clean_name, day, month, year, driver, conductor)

    # ──────────────────────────────────────────────────────────────────────────
    # TIER 4: COMPLETE PERSONAL DESTINY BLUEPRINT REPORT (₹1,050)
    # ──────────────────────────────────────────────────────────────────────────
    elif clean_tier in ["complete", "blueprint", "complete_report", "full"]:
        age_data = calculate_age_numerology(day, month, year)
        expl_career = generate_simple_explanation_and_remedies("Career growth and stability", driver, conductor, name=clean_name, day=day, month=month, year=year)
        expl_wealth = generate_simple_explanation_and_remedies("Wealth retention and asset growth", driver, conductor, name=clean_name, day=day, month=month, year=year)
        expl_rel = generate_simple_explanation_and_remedies("Relationship harmony and communication", driver, conductor, name=clean_name, day=day, month=month, year=year)
        expl_health = generate_simple_explanation_and_remedies("Vitality and physical well-being", driver, conductor, name=clean_name, day=day, month=month, year=year)

        report_sections = [
            f"# Premium Numerology Report\n**Client:** {clean_name} | **DOB:** {day:02d}-{month:02d}-{year} ({birth_city}) | **Report Length:** 32 Pages | **Edition:** Sovereign Executive Blueprint\n",
            
            "## Chapter 1: Foundational Energy Architecture",
            (
                f"You were born under a profound configuration of enduring perseverance and executive responsibility. "
                f"Your Core Natural Energy vibrates with the grounded depth of {driver_planet} (Root {driver}), "
                f"while your Life Path Direction also aligns with {conductor_planet} (Path {conductor}). "
                f"This rare dual alignment signifies an individual designed for significant, compounding achievements that withstand time. "
                f"You do not thrive on fleeting shortcuts; your greatness emerges when you build solid, unshakeable foundations."
            ),

            "## Chapter 1B: Chronological Age Frequency & Manifestation Radar",
            (
                f"**Chronological Age Milestone:** {age_data['age_years']} Years Completed (Navigating Year {age_data['running_year']})\n\n"
                f"• **Input Characteristics (Compound Age Number {age_data['compound_age']}):**\n"
                f"  {age_data['input_characteristics']['description']}\n\n"
                f"• **Output Manifestation (Sum Total Root {age_data['root_age']} · {age_data['root_planet']}):**\n"
                f"  {age_data['output_characteristics']['manifestation']}\n\n"
                f"• **Karmic Gap Synthesis & Lo Shu Interaction:**\n"
                f"  {age_data['gap_analysis']['diagnosis']}"
            ),

            "## Chapter 1C: Natal Lo Shu Grid Birth Chart & Elemental Matrix",
            generate_loshu_grid_markdown(day, month, year),
            
            "## Chapter 2: Professional Flow & Career Trajectory",
            (
                f"### Navigating Your Career Cycle\n"
                f"{DOMAIN_ACTION_GUIDANCE['career']['blockage_framing']}\n\n"
                f"**Specific Navigational Guidance:**\n{expl_career['direct_answer']}\n\n"
                f"**Strategic Career Actions:**\n"
                f"• **Proactive Professional Networking:** Systematically re-connect with respected colleagues, mentors, and industry peers to share insights without immediate transactional demands.\n"
                f"• **Clear Documented Agreements:** Put deliverables, timelines, and scope into written format to prevent misunderstandings.\n"
                f"• **High-Impact Skill Consolidation:** Specialize deeply in one core domain that makes your contribution indispensable.\n"
                f"• **Diplomatic Presence:** Allow your consistent, high-standard deliverables to demonstrate your authority naturally."
            ),
            
            "## Chapter 3: Wealth Stewardship & Asset Compounding",
            (
                f"### Financial Flow & Retention\n"
                f"{DOMAIN_ACTION_GUIDANCE['wealth']['blockage_framing']}\n\n"
                f"**Specific Wealth Guidance:**\n{expl_wealth['direct_answer']}\n\n"
                f"**Prudent Capital Guidelines:**\n"
                f"• **Conservative Asset Anchoring:** Systematically allocate surplus liquid inflows into secure, long-term compounding instruments before discretionary spending takes hold.\n"
                f"• **Avoid High-Stakes Speculation:** This cycle strongly rewards predictable, asset-backed accumulation over untested speculative trends.\n"
                f"• **Budget Auditing:** Periodically audit recurring overheads, subscriptions, and financial leaks to preserve cash flow."
            ),
            
            "## Chapter 4: Relationship Harmony & Emotional Alignment",
            (
                f"### Cultivating Emotional Warmth\n"
                f"{DOMAIN_ACTION_GUIDANCE['marriage']['blockage_framing']}\n\n"
                f"**Relationship Guidance:**\n{expl_rel['direct_answer']}\n\n"
                f"**Harmonizing Relational Practices:**\n"
                f"• **Active Empathetic Listening:** Provide full, uninterrupted attention during sensitive discussions, seeking to understand your partner's emotional state before offering solutions.\n"
                f"• **De-escalate Ego Debates:** When friction arises, choose a gentle pause rather than an immediate retort, allowing perspective to settle.\n"
                f"• **Shared Simple Rituals:** Cultivate grounding weekly habits—such as an evening walk in nature or sharing quiet meals—to replenish emotional closeness."
            ),
            
            "## Chapter 5: Vitality, Sleep & Nervous Restoration",
            (
                f"### Sustaining Inner Vitality\n"
                f"{DOMAIN_ACTION_GUIDANCE['health']['blockage_framing']}\n\n"
                f"**Vitality Guidance:**\n{expl_health['direct_answer']}\n\n"
                f"**Restorative Health Practices:**\n"
                f"• **Consistent Sleep Rhythm:** Disconnect from digital devices 45 minutes before bedtime to allow mental activity to settle.\n"
                f"• **Morning Sun & Hydration:** Begin your day with pure water and 10-15 minutes of gentle morning sunlight.\n"
                f"• **Gentle Pacing:** Integrate regular breathwork and light physical stretching to prevent neck and back fatigue."
            ),
            
            "## Chapter 6: Spatial & Environmental Alignment",
            (
                "Your physical environment exerts a continuous subtle influence on your mental clarity and decision-making:\n"
                "• **Primary Focus Direction:** Position your primary work desk facing West or North to facilitate disciplined execution and commercial opportunity.\n"
                "• **Restful Sanctuary:** Orient your sleeping position with your head toward the South or East to support restorative nervous recovery.\n"
                "• **Environmental Tones:** Use balanced earth tones, soft navy, metallic accents, and cream in your primary living and working spaces."
            ),
            
            "## Chapter 7: Multi-Year Personal Roadmap & Golden Windows",
            (
                "### The Trajectory Ahead\n"
                "• **Current Phase (Consolidation & Foundation):** A vital period of restructuring, eliminating liabilities, and solidifying professional credentials.\n"
                "• **Upcoming Growth Window (Expansion & Fluidity):** As this calibration phase completes, natural ease returns, barriers diminish, and recognition accelerates.\n"
                "The disciplined groundwork you establish today directly prepares you to fully capitalize on this upcoming favorable cycle."
            ),
            
            "## Chapter 8: The Complete Harmonization Protocol",
            (
                "### Summary of Daily & Weekly Balancing Practices\n"
                "1. **Morning Clarity Ritual:** 10 minutes of quiet intention facing an auspicious direction.\n"
                "2. **Auspicious Palette:** Wearing supportive tones on critical meeting days.\n"
                "3. **Orderly Stewardship:** Maintaining clean, clutter-free physical and digital workspaces.\n"
                "4. **Weekly Giving:** Performing selfless community acts or feeding birds/animals on Saturdays to maintain healthy energetic circulation.\n\n"
                f"### Sacred Consecration Muhurta (Shukla Paksha Initiation Window)\n{shukla_info['guidance_narrative']}\n\n"
                "### Empowering Closing Principle\n"
                "Energy cycles provide profound navigational guidance. Your personal wisdom, unwavering perseverance, and diplomatic communication "
                "are the true masters of your journey."
            )
        ]

        if _is_international_client(birth_city, country):
            intl_sections = _build_international_report_sections(clean_name, driver, conductor, lo_shu.get("missing_numbers", []))
            report_sections.extend(intl_sections)

        return _finalize_report_envelope({
            "tier": "complete_report",
            "tier_display": "Premium Numerology Report",
            "price_inr": 1050,
            "profile": profile_summary,
            "chapters_count": 8,
            "report_markdown": sanitize_text("\n\n".join(report_sections))
        }, clean_tier, clean_name, day, month, year, driver, conductor)

    # ──────────────────────────────────────────────────────────────────────────
    # TIER 5: 1-ON-1 MASTER PERSONAL CONSULTATION (₹11,400)
    # ──────────────────────────────────────────────────────────────────────────
    else:  # master_consultation
        age_data = calculate_age_numerology(day, month, year)
        report_sections = [
            f"# Executive Private Master Consultation Dossier\n**Client:** {clean_name} | **Recorded Time:** {birth_time} | **Location:** {birth_city} | **Pass Tier:** Master Consultation (₹11,400)\n",
            
            "## 1. Birth Epoch Verification & Precision Timing Synthesis",
            (
                f"Welcome, {clean_name}. In preparation for your private 90-minute consultation, our advanced multi-system analysis has "
                f"verified your recorded birth time ({birth_time} in {birth_city}). "
                f"Your energetic chart displays Libra Rising (ruled by Venus) with Saturn as your Most Favorable Supportive Planetary Force (Yogakaraka), "
                f"positioned in the analytical domain of Virgo. "
                f"This harmonizes directly with your Core Root {driver} and Life Path {conductor}, confirming a profile of profound executive stamina, "
                f"strategic depth, and eventual institutional leadership."
            ),

            "## 2. Natal Lo Shu Grid Birth Chart & Precision Planetary Blueprint",
            generate_loshu_grid_markdown(day, month, year),
            
            "## 3. Chronological Age Frequency & Manifestation Radar",
            (
                f"**Chronological Age Milestone:** {age_data['age_years']} Years Completed (Navigating Year {age_data['running_year']})\n\n"
                f"• **Input Characteristics (Compound Age Number {age_data['compound_age']}):**\n"
                f"  {age_data['input_characteristics']['description']}\n\n"
                f"• **Output Manifestation (Sum Total Root {age_data['root_age']} · {age_data['root_planet']}):**\n"
                f"  {age_data['output_characteristics']['manifestation']}\n\n"
                f"• **Karmic Gap Synthesis & Lo Shu Interaction:**\n"
                f"  {age_data['gap_analysis']['diagnosis']}"
            ),
            "## 4. Advanced Multi-System Synthesis: Core Cycles & Career Arc",
            (
                "• **Current Planetary Time Cycle:** You are currently completing an intensive, grounding cycle. "
                "This cycle demands precision, restructuring of outdated workflows, and emotional patience. "
                "Any friction experienced in recent months is a natural calibration of this cycle.\n"
                "• **Upcoming Golden Transition:** The upcoming phase transitions into an expansive, commercial, and highly fluid cycle. "
                "This brings executive recognition, rapid expansion of your professional network, and financial unlocking."
            ),
            
            "## 5. Bespoke Executive Remedies & Custom Sacred Geometry",
            (
                "During your live session, your Master Consultant will provide personalized guidance on:\n"
                "• **Custom Energetic Yantra Calibration:** Sacred geometric alignment tailored specifically to your exact birth coordinates.\n"
                "• **Bespoke Gemstone Suitability Testing:** Evaluating precision compatibility for Blue Sapphire (Neelam) vs. Amethyst vs. Emerald.\n"
                "• **Workspace Vastu Optimization:** Custom blueprint layout for your desk, safe, and meeting corners."
            ),
            
            "## 6. 30-Day Guided Priority Roadmap",
            (
                "Following your consultation, you receive 30 days of direct WhatsApp priority guidance to assist in:\n"
                "• Reviewing strategic career opportunities and partnership contracts.\n"
                "• Implementing tailored daily energetic harmonizing rituals.\n"
                "• Timing high-stakes decisions to align with peak favorable planetary hours."
            ),
            
            "## 7. Private Consultation Booking Details",
            (
                "• **Duration:** 90 Minutes Private Master Session (Google Meet / Zoom)\n"
                "• **Deliverable:** Full Video Recording, High-Resolution Destiny Dossier, and Custom Yantra Blueprint\n"
                "• **Mentor:** Senior Master Astrologer & Numerologist (Numeros Vision)"
            )
        ]

        if _is_international_client(birth_city, country):
            intl_sections = _build_international_report_sections(clean_name, driver, conductor, lo_shu.get("missing_numbers", []))
            report_sections.extend(intl_sections)

        return _finalize_report_envelope({
            "tier": "master_consultation",
            "tier_display": "1-on-1 Master Personal Consultation Dossier",
            "price_inr": 11400,
            "profile": profile_summary,
            "session_duration_minutes": 90,
            "report_markdown": sanitize_text("\n\n".join(report_sections))
        }, clean_tier, clean_name, day, month, year, driver, conductor)
