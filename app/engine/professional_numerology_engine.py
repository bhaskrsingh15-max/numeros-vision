"""
DETERMINISTIC PROFESSIONAL NUMEROLOGY ENGINE (40 TOPICS)
Grounding: Professional Numerology Pro Course Notes & Tables, Advanced Study Guides.
Topic 39 (Hora Prediction) is strictly omitted.

Deterministic computations covering:
- Mobile Numerology auditing & malefic combinations (Topic 2)
- Vehicle & House Numerology (Topic 4)
- 81 Driver-Conductor combination taxonomy (Topic 5)
- Repetitive Numbers analysis (Topic 7)
- Kua Number and 8 Compass Directions (Topic 11, 36)
- Master & Karmic Numbers diagnosis (Topic 13, 14)
- Personal Year, Month, Day & Universal Year (Topic 15, 16, 18, 19)
- Marriage & Business Partner Compatibility scoring (Topic 21, 22, 28, 29)
- Bonus queries: Child planning, Autism grounding, Silver Square, Door remedies (Topic 26)
- Career & Share Market suitability (Topic 27, 35)
- Health organ mapping before/after age 40 (Topic 34b)
- Yantra selection & thread pairing (Topic 23, 37, 38)
- Signature guidelines (Topic 40)
"""

from typing import Dict, Any, List, Optional
import datetime
import re

from app.engine.kua import (
    KUA_NEEDS_GENDER_TEXT,
    KUA_RULE_TEXT,
    calculate_kua_details,
)

# ── Planetary Friends / Enemies (Topic 1) ────────────────────────────────────
PLANETARY_RELATIONS = {
    1: {"planet": "Sun", "friends": [1, 2, 3, 5, 9], "enemies": [8], "neutrals": [4, 6, 7]},
    2: {"planet": "Moon", "friends": [1, 2, 3, 5], "enemies": [8, 4, 9], "neutrals": [6, 7]},
    3: {"planet": "Jupiter", "friends": [1, 2, 3, 5, 7, 9], "enemies": [6], "neutrals": [4, 8]},
    4: {"planet": "Rahu", "friends": [1, 5, 6, 7, 8], "enemies": [2, 9, 4], "neutrals": [3]},
    5: {"planet": "Mercury", "friends": [1, 2, 3, 5, 6], "enemies": [], "neutrals": [4, 7, 8, 9]},
    6: {"planet": "Venus", "friends": [5, 6, 8, 4, 7], "enemies": [3], "neutrals": [1, 2, 9]},
    7: {"planet": "Ketu", "friends": [1, 3, 4, 5, 6], "enemies": [8], "neutrals": [2, 7, 9]},
    8: {"planet": "Saturn", "friends": [5, 6, 3], "enemies": [1, 2, 4, 8], "neutrals": [7, 9]},
    9: {"planet": "Mars", "friends": [1, 3, 5, 9], "enemies": [2, 4], "neutrals": [6, 7, 8]}
}

# ── Malefic Mobile Pairs (Topic 2) ───────────────────────────────────────────
MALEFIC_MOBILE_PAIRS = {
    "14": "Attracts loan liabilities, legal notices, health issues, heavy unending hard work.",
    "41": "Attracts loan liabilities, legal notices, health issues, heavy unending hard work.",
    "16": "Spouse health issues, married life friction, income confinement.",
    "61": "Spouse health issues, married life friction, income confinement.",
    "18": "Severe friction between father and son, frequent career disruption, government scrutiny.",
    "81": "Severe friction between father and son, frequent career disruption, government scrutiny.",
    "26": "Break in education, mother-in-law friction, diabetes or hormonal vulnerability.",
    "62": "Break in education, mother-in-law friction, diabetes or hormonal vulnerability.",
    "28": "Vish Yog: heavy hospital expenditures, financial fluctuations, severe emotional grief.",
    "82": "Vish Yog: heavy hospital expenditures, financial fluctuations, severe emotional grief.",
    "34": "Breathing problems, neurological anxiety, limb numbness; dangerous with multiple 8s.",
    "43": "Breathing problems, neurological anxiety, limb numbness; dangerous with multiple 8s.",
    "45": "Court cases, hospital visits, life restrictions.",
    "54": "Court cases, hospital visits, life restrictions.",
    "48": "Blood-related ailments, chronic resistance, lack of sexual pleasure.",
    "84": "Blood-related ailments, chronic resistance, lack of sexual pleasure.",
    "68": "Eye troubles, organ vulnerabilities, friction with multiple 1s in chart.",
    "86": "Eye troubles, organ vulnerabilities, friction with multiple 1s in chart."
}

def audit_mobile_number(mobile_str: str, driver: Optional[int] = None) -> Dict[str, Any]:
    """Audit mobile phone number for malefic pairs, repeating digits, and total vibration."""
    digits = [c for c in mobile_str if c.isdigit()]
    if len(digits) < 10:
        return {"error": "Invalid mobile number. Must contain at least 10 digits."}

    from app.engine.digit_root import digit_root
    raw_sum = sum(int(d) for d in digits)
    total_reduced = digit_root(raw_sum)

    joined = "".join(digits)
    detected_malefics = []
    for pair, desc in MALEFIC_MOBILE_PAIRS.items():
        if pair in joined:
            detected_malefics.append({"pair": pair, "description": desc})

    repeating_issues = []
    for pattern in ["00", "44", "88", "22", "999", "888", "777", "444", "222"]:
        if pattern in joined:
            repeating_issues.append(f"Forbidden repeating sequence '{pattern}' detected.")

    is_friendly_total = True
    if driver and driver in PLANETARY_RELATIONS:
        is_friendly_total = total_reduced in PLANETARY_RELATIONS[driver]["friends"]

    preferred_totals = {
        1: [46, 64, 37, 55],
        3: [66, 39, 30],
        5: [41, 32, 50, 59],
        6: [42, 24, 33, 60]
    }

    status = "Harmonious" if not detected_malefics and is_friendly_total else "Requires Change or Remedy"

    return {
        "mobile_number": "".join(digits),
        "total_compound": raw_sum,
        "total_root": total_reduced,
        "is_friendly_to_driver": is_friendly_total,
        "malefic_pairs_found": detected_malefics,
        "repeating_digit_issues": repeating_issues,
        "status": status,
        "recommended_totals": preferred_totals.get(total_reduced, [41, 32, 37, 42]),
        "remedy": (
            "Phone vibration is harmonious." if status == "Harmonious" else
            "Switch to a number with preferred compound 41, 32 (Root 5) or 37, 46 (Root 1), free of 14, 18, 28, and 48 pairs."
        )
    }

# ── Personal Cycles: PY, PM, PD & Universal Year (Topic 15, 16, 18, 19) ──────
PERSONAL_YEAR_INTERPRETATIONS = {
    1: {"theme": "New Beginnings & Seed Sowing", "planet": "Sun", "guidance": "Start of a fresh 9-year cycle. Take bold initiative, launch projects, exercise leadership. Focus on execution rather than idle planning."},
    2: {"theme": "Root Growing & Patience", "planet": "Moon", "guidance": "Consolidation, cooperation, diplomacy, and team partnerships. Slow down, avoid rash solitary decisions, nurture alliances."},
    3: {"theme": "Sprouting & Creative Expansion", "planet": "Jupiter", "guidance": "Knowledge acquisition, self-expression, social visibility, and travel. Excellent for studies, writing, and spiritual growth."},
    4: {"theme": "Plant Strengthening & Discipline", "planet": "Rahu", "guidance": "Testing year demanding rigorous hard work. Build unshakeable foundations; avoid get-rich-quick temptations and illusions."},
    5: {"theme": "Flowering & Transition", "planet": "Mercury", "guidance": "Year of change, unexpected opportunities, commercial growth, and travel. Auspicious for career pivots and networking."},
    6: {"theme": "Fruit Bearing & Family", "planet": "Venus", "guidance": "Domestic harmony, marriage, family responsibilities, luxury, and artistic pursuits. Prime year for home enhancement and relationships."},
    7: {"theme": "Pruning & Reflection", "planet": "Ketu", "guidance": "Spiritual pause, mental introspection, research, and self-healing. Avoid aggressive financial speculation; invest in learning."},
    8: {"theme": "Harvest & Material Power", "planet": "Saturn", "guidance": "Year of executive authority, business achievement, and financial returns for previous effort. Demands ethical fairness."},
    9: {"theme": "Composting & Completion", "planet": "Mars", "guidance": "Closure, clearing unfinished debts, letting go of what no longer serves. Year of humanitarian service; prepare for next cycle."}
}

def calculate_personal_cycles(day: int, month: int, target_date: Optional[datetime.date] = None) -> Dict[str, Any]:
    """Calculate Personal Year, Personal Month, Personal Day, and Universal Year."""
    target = target_date or datetime.date.today()
    t_day = target.day
    t_month = target.month
    t_year = target.year

    from app.engine.digit_root import (
        PERSONAL_CYCLES_LABEL,
        calc_personal_day,
        calc_personal_month,
        calc_personal_year,
        digit_root,
    )
    # Universal Year
    uy_sum = digit_root(t_year)

    # Personal Year = Day + Month + Target Year (digits reduced 1-9)
    py = calc_personal_year(day, month, t_year)

    # Personal Month = Personal Year + Target Month
    pm = calc_personal_month(py, t_month)

    # Personal Day = Personal Year + Personal Month + Target Date digits (reduced 1-9)
    pd = calc_personal_day(py, pm, t_day, t_month, t_year)

    py_info = PERSONAL_YEAR_INTERPRETATIONS.get(py, {})

    return {
        "target_date": target.isoformat(),
        "universal_year": uy_sum,
        "personal_year": py,
        "personal_year_planet": py_info.get("planet", "Sun"),
        "personal_year_theme": py_info.get("theme", ""),
        "personal_year_guidance": py_info.get("guidance", ""),
        "personal_month": pm,
        "personal_day": pd,
        "actionable_timing_advice": f"You are currently in Personal Year {py} ({py_info.get('theme', '')}) and Personal Month {pm}. Align major contracts and negotiations to Personal Days friendly to your core numbers."
    }

# ── Kua Number & Numero-Vastu Directions (Topic 11, 36) ──────────────────────
def calculate_kua(gender: Optional[str], birth_year: int) -> Optional[int]:
    """
    Calculate Kua number using canonical century-invariant 4-digit formula:
      x = single-digit sum of all 4 digits of calendar birth_year.
      Male: 11 - x -> single digit (5 -> 2).
      Female: 4 + x -> single digit (5 -> 8).
      Missing gender -> None (never guesses).
    """
    return calculate_kua_details(birth_year, gender)["kua_number"]

KUA_DIRECTION_PROFILES = {
    1: {"group": "East", "success": "SE", "health": "E", "relationship": "S", "stability": "N", "avoid": ["W", "NW", "SW", "NE"]},
    2: {"group": "West", "success": "NE", "health": "W", "relationship": "NW", "stability": "SW", "avoid": ["N", "S", "E", "SE"]},
    3: {"group": "East", "success": "S", "health": "N", "relationship": "SE", "stability": "E", "avoid": ["W", "NW", "SW", "NE"]},
    4: {"group": "East", "success": "N", "health": "S", "relationship": "E", "stability": "SE", "avoid": ["W", "NW", "SW", "NE"]},
    6: {"group": "West", "success": "W", "health": "NE", "relationship": "SW", "stability": "NW", "avoid": ["N", "S", "E", "SE"]},
    7: {"group": "West", "success": "NW", "health": "W", "relationship": "NE", "stability": "SW", "avoid": ["N", "S", "E", "SE"]},
    8: {"group": "West", "success": "SW", "health": "NW", "relationship": "W", "stability": "NE", "avoid": ["N", "S", "E", "SE"]},
    9: {"group": "East", "success": "E", "health": "SE", "relationship": "N", "stability": "S", "avoid": ["W", "NW", "SW", "NE"]}
}

def analyze_kua_and_directions(gender: Optional[str], birth_year: int) -> Dict[str, Any]:
    """Retrieve Kua number and favorable Numero-Vastu directions using canonical Kua rules."""
    details = calculate_kua_details(birth_year, gender)
    kua = details["kua_number"]
    if kua is None:
        return {
            "status": "NEEDS_GENDER",
            "kua_number": None,
            "kua_display": KUA_NEEDS_GENDER_TEXT,
            "kua_group": KUA_NEEDS_GENDER_TEXT,
            "kua_element": KUA_NEEDS_GENDER_TEXT,
            "element_group": KUA_NEEDS_GENDER_TEXT,
            "rule_note": KUA_RULE_TEXT,
            "prosperous_direction_wealth": KUA_NEEDS_GENDER_TEXT,
            "vitality_direction_health": KUA_NEEDS_GENDER_TEXT,
            "relationship_direction_harmony": KUA_NEEDS_GENDER_TEXT,
            "stability_direction_peace": KUA_NEEDS_GENDER_TEXT,
            "success_direction_sheng_chi": KUA_NEEDS_GENDER_TEXT,
            "health_direction_tien_yi": KUA_NEEDS_GENDER_TEXT,
            "relationship_direction_nien_yen": KUA_NEEDS_GENDER_TEXT,
            "stability_direction_fu_wei": KUA_NEEDS_GENDER_TEXT,
            "unfavorable_directions_to_avoid": [],
            "vastu_desk_alignment": f"{KUA_NEEDS_GENDER_TEXT}. ({KUA_RULE_TEXT})",
            "angelic_alignment_note": KUA_RULE_TEXT,
        }
    prof = KUA_DIRECTION_PROFILES[kua]
    return {
        "status": "OK",
        "kua_number": kua,
        "kua_display": str(kua),
        "kua_group": prof["group"],
        "kua_element": details["element"],
        "kua_trigram": details["trigram"],
        "element_group": details["element_group"],
        "rule_note": KUA_RULE_TEXT,
        "prosperous_direction_wealth": prof["success"],
        "vitality_direction_health": prof["health"],
        "relationship_direction_harmony": prof["relationship"],
        "stability_direction_peace": prof["stability"],
        # Backward-compatibility aliases
        "success_direction_sheng_chi": prof["success"],
        "health_direction_tien_yi": prof["health"],
        "relationship_direction_nien_yen": prof["relationship"],
        "stability_direction_fu_wei": prof["stability"],
        "unfavorable_directions_to_avoid": prof["avoid"],
        "vastu_desk_alignment": f"As per your personal chart reading ({KUA_RULE_TEXT.lower()}), face {prof['success']} or {prof['health']} while working, creating, or making strategic decisions to support career flow and mental clarity.",
        "angelic_alignment_note": "Your personal chart reading aligns physical workspace orientation toward your favourable cardinal direction."
    }

# ── Marriage & Business Partner Compatibility Scoring (Topic 21, 22, 28, 29) ─
def score_partner_compatibility(
    d1: int, c1: int, loshu1_digits: List[int],
    d2: int, c2: int, loshu2_digits: List[int],
    is_d1_male: bool = True
) -> Dict[str, Any]:
    """
    Computes partner compatibility score using verified weightages from Table 21 & 22:
    - Driver vs Driver both positive: 40%
    - Male Driver stronger than Female: 10%
    - Driver vs Driver neutral: 30%
    - Driver vs Driver anti/enemy: 0% (incompatible irrespective of other points)
    - Complementary pairings (2/9, 2/4, 4/4, 8/8): 20%
    - 5 & 6 presence in both charts: +15% boost (Most compatible couple)
    - 5 & 6 missing in both charts: -20% penalty
    """
    rel1 = PLANETARY_RELATIONS.get(d1, {})
    rel2 = PLANETARY_RELATIONS.get(d2, {})

    is_d2_enemy_to_d1 = d2 in rel1.get("enemies", [])
    is_d1_enemy_to_d2 = d1 in rel2.get("enemies", [])

    if is_d2_enemy_to_d1 or is_d1_enemy_to_d2:
        return {
            "score_pct": 35.0,
            "category": "Anti / Enemy Driver Pairing",
            "is_compatible": False,
            "verdict": "Friction Detected (35%)",
            "analysis": f"Driver {d1} and Driver {d2} are natural enemy numbers. Power struggles and ego friction will dominate unless neutralized by name balancing and mutual conscious adjustments.",
            "remedies": "Balance both partners' names to a neutral mediator (such as Mercury 5). Install a brass Swastika in the living room and sleep with headboards toward favorable Kua directions."
        }

    score = 0.0
    is_d2_friend = d2 in rel1.get("friends", [])
    is_d1_friend = d1 in rel2.get("friends", [])

    if is_d2_friend and is_d1_friend:
        score += 40.0
    else:
        score += 30.0 # neutral

    # Male driver seniority
    if is_d1_male and d1 != d2:
        score += 10.0

    # Complementary pairings bonus
    pair_set = {d1, d2}
    if pair_set in [{2, 9}, {2, 4}, {4, 4}, {8, 8}]:
        score += 15.0

    # 5 & 6 synergy in Lo Shu grids
    has_5_both = (5 in loshu1_digits) and (5 in loshu2_digits)
    has_6_both = (6 in loshu1_digits) and (6 in loshu2_digits)
    lacks_56_both = (5 not in loshu1_digits and 6 not in loshu1_digits) and (5 not in loshu2_digits and 6 not in loshu2_digits)

    if has_5_both and has_6_both:
        score += 15.0 # Most compatible couple
    elif lacks_56_both:
        score -= 15.0

    score = min(max(score, 30.0), 95.0)

    if score >= 75.0:
        cat = "Excellent Match"
    elif score >= 65.0:
        cat = "Best Match"
    elif score >= 55.0:
        cat = "Good Match"
    else:
        cat = "Average Match (Requires Name & Space Balancing)"

    return {
        "score_pct": round(score, 1),
        "category": cat,
        "is_compatible": score >= 55.0,
        "verdict": f"{cat} ({score}%)",
        "has_5_and_6_presence": (has_5_both or has_6_both),
        "analysis": f"Driver {d1} and Driver {d2} possess a base compatibility score of {score}%. " + (
            "The mutual presence of numbers 5 and 6 provides domestic warmth and practical stability."
            if (has_5_both or has_6_both) else
            "Consider bringing Rose Quartz crystals and name balancing to reinforce emotional bonding."
        ),
        "remedies": "Keep a pair of Rose Quartz or brass swans in the South-West bedroom corner to harmonize marital bliss."
    }

# ── Share Market Investment Profile by Driver (Topic 35) ─────────────────────
SHARE_MARKET_PROFILES = {
    1: {
        "style": "Large-Cap Leadership & Sovereign Bonds",
        "favorable_sectors": "Government securities, Gold ETFs, Blue-chip market leaders, Defense, Solar Energy",
        "risk_level": "Moderate",
        "intraday_suitability": "Average; better for swing/positional holdings.",
        "guidance": "Invest in top industry monopolies with authoritative management. Avoid penny stocks."
    },
    2: {
        "style": "Defensive & FMCG / Liquid Holdings",
        "favorable_sectors": "FMCG, Dairy, Shipping, Water treatment, Healthcare, Pharmaceuticals",
        "risk_level": "Low to Moderate",
        "intraday_suitability": "Low; emotional volatility can trigger panic selling.",
        "guidance": "Stick to systematic investment plans (SIPs) in mutual funds. Avoid leveraged trading."
    },
    3: {
        "style": "Strategic Wealth & Blue-Chip Expansion",
        "favorable_sectors": "Banking, Financial Institutions, EdTech, Asset Management, Publishing, Agriculture",
        "risk_level": "Moderate",
        "intraday_suitability": "Good for swing trading; premier for long-term compound wealth.",
        "guidance": "Your Jupiter intellect excels at fundamental analysis. Invest in dividend-paying financial giants."
    },
    4: {
        "style": "High-Tech & Disruptive Innovation",
        "favorable_sectors": "AI, Software, Electric Vehicles, Aerospace, Cybersecurity, Renewable Tech",
        "risk_level": "High Speculative Risk",
        "intraday_suitability": "Caution: High intuition but sudden sharp reversals.",
        "guidance": "Strictly avoid speculative Futures & Options (F&O) with heavy leverage. Set strict stop-losses."
    },
    5: {
        "style": "Premier Market Agility & Intraday Trading",
        "favorable_sectors": "Commercial Banks, FinTech, Media, Telecommunications, Logistics, Index Trading",
        "risk_level": "Dynamic / Agile",
        "intraday_suitability": "Highest suitability. Born trader with rapid profit-booking instinct.",
        "guidance": "Keep green aventurine on your trading desk. Trade with strict discipline and avoid greed."
    },
    6: {
        "style": "Consumer Luxury & Entertainment Growth",
        "favorable_sectors": "Luxury Goods, Hospitality, Tourism, Cosmetics, Media, Entertainment, Automobile",
        "risk_level": "Moderate",
        "intraday_suitability": "Good for momentum trading during festive/consumer quarters.",
        "guidance": "Invest in premium consumer brands and companies providing lifestyle luxury."
    },
    7: {
        "style": "Deep Research & Niche Pharma",
        "favorable_sectors": "Biotech, Pathology, Research Labs, Deep Tech, Niche Metals, Specialized Chemicals",
        "risk_level": "Moderate to High",
        "intraday_suitability": "Low; prefers quiet, thorough fundamental research over ticker noise.",
        "guidance": "Invest only after rigorous due diligence. Avoid following herd hype on social media."
    },
    8: {
        "style": "Infrastructure, Steel, Mining & Long-Term Value",
        "favorable_sectors": "Iron & Steel, Heavy Construction, Real Estate, Mining, Cement, Oil & Gas",
        "risk_level": "Low Speculation / High Long-Term Wealth",
        "intraday_suitability": "Extremely Low. Saturn punishes quick speculation with severe capital erosion.",
        "guidance": "Hold high-quality industrial infrastructure stocks for 5-10+ years. Speculative intraday is strictly discouraged."
    },
    9: {
        "style": "Energy, Defense & High-Stamina Positional",
        "favorable_sectors": "Defense, Military Engineering, Heavy Energy, Power Generation, Medical Devices, Sports",
        "risk_level": "Moderate to High",
        "intraday_suitability": "Moderate; guard against impatient or revenge trading after a loss.",
        "guidance": "Control impulses; maintain trading journal and exit decisively at targets."
    }
}

def analyze_share_market_profile(driver: int, conductor: int) -> Dict[str, Any]:
    """Retrieve deterministic stock market investment guidance based on Driver and Conductor."""
    prof = SHARE_MARKET_PROFILES.get(driver, SHARE_MARKET_PROFILES[5])
    return {
        "driver_number": driver,
        "conductor_number": conductor,
        "trading_style": prof["style"],
        "favorable_sectors": prof["favorable_sectors"],
        "speculative_risk_level": prof["risk_level"],
        "intraday_suitability": prof["intraday_suitability"],
        "strategic_guidance": prof["guidance"],
        "remedy": "Keep a pyramid or Green Aventurine crystal near trading screens to ground emotional impulses."
    }

# ── Bonus Query Solutions: Silver Square, Blood, Child, Autism (Topic 26) ────
def get_bonus_query_solution(query_key: str, profile_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Returns verified master numerology solutions for Topic 26 bonus queries:
    - child_conceive
    - autism_cases
    - silver_square
    - door_remedies
    - blood_remedy
    """
    key = query_key.lower()

    if "autism" in key or "neuro" in key or "speech_delay" in key:
        return {
            "topic": "Autism & Neurodiversity Energetic Support",
            "astrological_numerology_factors": [
                "Mercury (5) governs the central nervous system, speech coordination, and intellect.",
                "Rahu (4) or Ketu (7) affliction can cause sensory overload and communication hesitation."
            ],
            "remedies": [
                "Keep a 99.9% solid pure silver square (1x1 inch) in the child's pillow or clothing pocket for grounding.",
                "Offer green grass or fresh spinach (Palak) to cows on Wednesday mornings.",
                "Keep study and sleeping rooms free of dark blue, black, and harsh synthetic lighting; use soothing pale green.",
                "Drink water stored overnight in a pure copper vessel to balance electrical vitality.",
                "Note: Traditional supportive remedy; must accompany professional pediatric medical care."
            ],
            "recommended_tier": "Master Personal Consultation (₹11,400) for deep-dive child chart alignment."
        }

    elif "child" in key or "conceive" in key or "pregnant" in key:
        return {
            "topic": "Child Conceive & Fertility Alignment",
            "astrological_numerology_factors": [
                "Jupiter (3) - The primary Putrakaraka (significator of children) and wisdom.",
                "Moon (2) - Emotional nurturing, uterine fluid balance, and maternal intuition.",
                "Venus (6) - Reproductive vitality (Shukra Dhatu) and marital warmth."
            ],
            "timing_rules": "Avoid planning conception in Personal Year 4 (Rahu struggle) or Personal Year 9 (closure / heat / surgery). Prime fertility windows occur in Personal Year 2, 3, or 6.",
            "remedies": [
                "Use a mobile number totaling 3 (preferred compounds: 66, 39, or 30).",
                "Husband and wife should donate yellow fruits and bananas to an orphanage on Thursdays.",
                "Place a small idol of Bal Gopal or brass flute in the North-East zone of the home.",
                "Note: Always prioritize medical consultation alongside numerological timing."
            ],
            "recommended_tier": "Master Personal Consultation (₹11,400) for synchronized couple chart analysis."
        }

    elif "silver_square" in key or "silver square" in key:
        return {
            "topic": "Solid Silver Square (Chandi Ka Tukda) Master Remedy",
            "significance": "Silver represents Moon (calmness, mental peace), while the square geometry represents Saturn (structure, grounding). It is the supreme pacifier of Rahu (4).",
            "when_to_use": [
                "When experiencing persistent phantom anxiety, insomnia, or restless overthinking.",
                "When birth chart has Vish Yog (clash of Moon 2 and Saturn 8) or heavy Rahu (4) struggle.",
                "When facing sudden legal threats or unpredictable financial upheavals."
            ],
            "how_to_use": "Obtain a 99.9% pure solid silver square (1x1 inch or 12-15 grams, solid without hole). Wash with raw milk and Gangajal on a Shukla Paksha Monday or Wednesday morning, wrap in yellow or white silk, and carry in wallet or pocket."
        }

    elif "door" in key:
        return {
            "topic": "Vastu Main Door Numerology & Protection",
            "rules": "The main door number should reduce to a number friendly to the primary breadwinner's Driver (preferably 1, 3, 5, or 6).",
            "remedies": [
                "Draw a sacred Swastika using Roli (vermillion) and pure ghee on the outside of the main door frame.",
                "Install a brass or copper threshold strip across the entrance to prevent beneficial Chi from leaking out.",
                "Hang a Toran of 11 or 21 sacred Ashoka or Mango leaves to filter negative vibrational ingress.",
                "Ensure the entrance is brightly illuminated with warm golden light."
            ]
        }

    elif "blood" in key:
        return {
            "topic": "Blood Donation & Planet Balancing Remedy",
            "rules": "Mars (9) rules blood, surgery, and accidental cuts. Afflictions between Mars, Rahu, and Saturn trigger hospitalizations.",
            "remedies": [
                "Voluntarily donate blood at certified medical camps once or twice yearly (or during an 'anti-month' when Personal Month is 9).",
                "This voluntary sacrifice satisfies Mars's blood requirement, immunizing against involuntary injuries and surgeries.",
                "Always verify medical fitness and legal donor standards before donating."
            ]
        }

    return {
        "topic": "Professional Numerology Master Guidance",
        "guidance": "Consult the full 40-topic curriculum rules for tailored planetary balancing."
    }
