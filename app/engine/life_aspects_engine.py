"""
NV-016 to NV-018: LIFE ASPECTS ENGINE
Grounding: Classical Synastry & Compatibility (Topics 21, 22), Planetary Travel Indicators, Holistic Vitality Attunement.

Deterministic capabilities:
1. NV-016 Matchmaking & Comprehensive Relationship Synastry:
   - Driver-Driver, Conductor-Conductor, and Name-Name vibrational alignment
   - Lo Shu Shared Planes and missing energy complementation
   - Potential friction points & diplomatic communication recommendations
   - Comprehensive compatibility score (0-100%) and marital/business verdict.
2. NV-017 Foreign Travel & Relocation Engine:
   - Evaluation of travel numbers (2, 5, 6, 7) and Lo Shu Action Plane (2-7-6)
   - Distinguishes short-term journeys, education abroad, and permanent settlement
   - Current Personal Year travel window calibration and favorable directions.
3. NV-018 Health & Wellbeing Interpretation (Safe Use & Statutory Compliant):
   - Ayurvedic vitality tendencies & organ systems mapped across 1-9
   - Age 40 transition guidance (Topic 34b)
   - Lifestyle, hydration, circadian rhythm, and restorative nutrition
   - STRICT NON-MEDICAL QUALIFICATION compliant with Indian Drugs and Magic Remedies Act 1954.
"""

from typing import Dict, Any, List, Optional, Set
import sys
import os

workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from app.engine.number_characteristics_registry import (
    get_number_profile,
    get_relationship,
    PLANETARY_RULERS
)
from app.engine.cheiro_engine import (
    CHALDEAN_LETTER_VALUES,
    compute_reduction_path
)
from app.engine.professional_numerology_engine import (
    score_partner_compatibility,
    PERSONAL_YEAR_INTERPRETATIONS
)


# ── NV-016 Matchmaking and Relationship Reports ───────────────────────────────
def analyze_relationship_compatibility(
    person1_name: str,
    p1_day: int,
    p1_month: int,
    p1_year: int,
    person2_name: str,
    p2_day: int,
    p2_month: int,
    p2_year: int,
    relationship_type: str = "romantic" # "romantic" or "business"
) -> Dict[str, Any]:
    """
    NV-016 Requirement: Comprehensive Dual-Profile Synastry Report.
    Evaluates Driver, Conductor, Name, and Lo Shu grid synergies.
    """
    # Person 1 reductions
    d1 = sum(int(d) for d in str(p1_day))
    while d1 > 9: d1 = sum(int(d) for d in str(d1))
    c1 = sum(int(d) for d in f"{p1_day:02d}{p1_month:02d}{p1_year}")
    while c1 > 9: c1 = sum(int(d) for d in str(c1))

    # Person 2 reductions
    d2 = sum(int(d) for d in str(p2_day))
    while d2 > 9: d2 = sum(int(d) for d in str(d2))
    c2 = sum(int(d) for d in f"{p2_day:02d}{p2_month:02d}{p2_year}")
    while c2 > 9: c2 = sum(int(d) for d in str(c2))

    # Lo Shu digits
    p1_digits = [int(d) for d in f"{p1_day:02d}{p1_month:02d}{p1_year}" if d != '0'] + [d1, c1]
    p2_digits = [int(d) for d in f"{p2_day:02d}{p2_month:02d}{p2_year}" if d != '0'] + [d2, c2]

    # Name numbers
    clean1 = "".join(c.upper() for c in person1_name if c.isalpha())
    clean2 = "".join(c.upper() for c in person2_name if c.isalpha())
    name1_sum = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean1)
    name2_sum = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean2)
    _, name1_root = compute_reduction_path(name1_sum) if name1_sum else ("0", 1)
    _, name2_root = compute_reduction_path(name2_sum) if name2_sum else ("0", 1)

    # Base score using validated Table 21 & 22 formula
    base_comp = score_partner_compatibility(
        d1=d1, c1=c1, loshu1_digits=p1_digits,
        d2=d2, c2=c2, loshu2_digits=p2_digits
    )

    # Conductor and Name synastry layers
    rel_conductor = get_relationship(c1, c2)
    rel_name = get_relationship(name1_root, name2_root)

    # Fine-tune score with conductor and name resonance
    score = base_comp["score_pct"]
    if rel_conductor["is_friendly"]:
        score = min(score + 5.0, 98.0)
    elif rel_conductor["is_enemy"]:
        score = max(score - 5.0, 30.0)

    if rel_name["is_friendly"]:
        score = min(score + 5.0, 98.0)
    elif rel_name["is_enemy"]:
        score = max(score - 5.0, 30.0)

    # Friction identification
    friction_points = []
    rel_driver = get_relationship(d1, d2)
    if rel_driver["is_enemy"]:
        friction_points.append(f"Driver {d1} and Driver {d2} hold natural ego contrast; requires mutual conscious listening.")
    if rel_conductor["is_enemy"]:
        friction_points.append(f"Conductor {c1} and Conductor {c2} approach long-term goals through different philosophies.")
    if not (5 in p1_digits or 5 in p2_digits):
        friction_points.append("Both charts lack Number 5 (Mercury balance); conversations can swing between extremes.")

    # Mutual complementation
    p1_missing = set(range(1, 10)) - set(p1_digits)
    p2_missing = set(range(1, 10)) - set(p2_digits)
    p1_helps_p2 = sorted(list(p2_missing.intersection(set(p1_digits))))
    p2_helps_p1 = sorted(list(p1_missing.intersection(set(p2_digits))))

    verdict_text = (
        "Supreme Harmonious Synergy (85%+)" if score >= 85 else
        ("Strong Supportive Match (70-84%)" if score >= 70 else
        ("Balanced Match with Growth Opportunities (55-69%)" if score >= 55 else
        "High Friction Pairing / Conscious Mediation Required (<55%)"))
    )

    return {
        "relationship_type": relationship_type,
        "person_1": {"name": person1_name, "driver": d1, "conductor": c1, "name_root": name1_root},
        "person_2": {"name": person2_name, "driver": d2, "conductor": c2, "name_root": name2_root},
        "compatibility_score_pct": round(score, 1),
        "overall_verdict": verdict_text,
        "driver_harmony": rel_driver["relationship"],
        "conductor_harmony": rel_conductor["relationship"],
        "name_harmony": rel_name["relationship"],
        "lo_shu_complementation": {
            "energies_p1_brings_to_p2": p1_helps_p2,
            "energies_p2_brings_to_p1": p2_helps_p1
        },
        "friction_analysis": friction_points if friction_points else ["No major structural friction detected; natural mutual understanding prevails."],
        "diplomatic_communication_suggestions": [
            f"Schedule key discussions on days favorable to both partners (such as Wednesdays or Fridays).",
            f"Respect individual space: {person1_name} values {PLANETARY_RULERS.get(d1, {}).get('planet')} expression, while {person2_name} channels {PLANETARY_RULERS.get(d2, {}).get('planet')} energy.",
            "Avoid discussing sensitive financial or domestic decisions during late evening exhaustion."
        ],
        "remedial_spatial_balancing": base_comp["remedies"]
    }


# ── NV-017 Foreign Travel & Relocation Engine ─────────────────────────────────
def evaluate_foreign_travel_indicators(
    day: int,
    month: int,
    year: int,
    target_year: Optional[int] = None
) -> Dict[str, Any]:
    """
    NV-017 Requirement: Foreign Travel & Relocation Interpretation.
    Evaluates presence of travel indicators:
    - Numbers 5 (Mercury/movement), 6 (Venus/comfort), 7 (Ketu/abroad), 2 (Moon/oceanic transit)
    - Lo Shu Action Plane (2-7-6)
    - Personal Year timing windows (PY 3, 5, 9)
    - Distinguishes short trips vs higher studies vs long-term settlement.
    """
    # Core numbers
    driver = sum(int(d) for d in str(day))
    while driver > 9: driver = sum(int(d) for d in str(driver))
    conductor = sum(int(d) for d in f"{day:02d}{month:02d}{year}")
    while conductor > 9: conductor = sum(int(d) for d in str(conductor))

    dob_digits = [int(d) for d in f"{day:02d}{month:02d}{year}" if d != '0'] + [driver, conductor]
    counts = {d: dob_digits.count(d) for d in range(1, 10)}

    t_year = target_year or 2026
    py_sum = day + month + sum(int(d) for d in str(t_year))
    py = py_sum
    while py > 9: py = sum(int(d) for d in str(py))

    travel_score = 0
    indicators_found = []

    if counts[5] > 0:
        travel_score += 25
        indicators_found.append("Number 5 present: High commercial mobility and agile international networking.")
    if counts[6] > 0:
        travel_score += 20
        indicators_found.append("Number 6 present: Attracted to overseas luxury travel, comfort, and foreign associations.")
    if counts[7] > 0:
        travel_score += 25
        indicators_found.append("Number 7 present: Strong Ketu impulse for crossing borders, research abroad, and spiritual pilgrimage.")
    if counts[2] > 0:
        travel_score += 15
        indicators_found.append("Number 2 present: Lunar water energy facilitating overseas transit across oceans.")

    has_action_plane = (counts[2] > 0 and counts[7] > 0 and counts[6] > 0)
    if has_action_plane:
        travel_score += 15
        indicators_found.append("Action Plane (2-7-6) fully formed: Supreme capacity for actualizing foreign opportunities quickly.")

    # Personal Year Window
    if py == 5:
        py_status = "Prime Catalytic Travel Year"
        py_note = f"Personal Year 5 is the premier cycle for relocation, passport visa processing, and foreign career expansion."
    elif py == 3:
        py_status = "Academic & Growth Travel Year"
        py_note = "Personal Year 3 favors foreign travel for higher degrees, certifications, and cultural learning."
    elif py == 9:
        py_status = "Culmination & Long Journey Year"
        py_note = "Personal Year 9 indicates major distance relocations and completing international assignments."
    else:
        py_status = "Internal Consolidation Year"
        py_note = f"Personal Year {py} focuses primarily on domestic foundations; short-distance trips remain viable."

    # Settlement vs Short Trip
    if travel_score >= 65 and (counts[5] >= 1 and (counts[6] >= 1 or counts[7] >= 1)):
        settlement_potential = "High Long-Term Overseas Settlement Affinity"
        settlement_details = "Chart displays enduring planetary indicators supporting long-term residency or substantial multinational professional postings."
    elif travel_score >= 40:
        settlement_potential = "Frequent International Travel & Medium-Term Stay"
        settlement_details = "Auspicious for multi-month project assignments, study abroad, and frequent business travel, while retaining strong homeland roots."
    else:
        settlement_potential = "Primarily Domestic Grounding with Periodic Leisure Journeys"
        settlement_details = "Career and personal stability flourish predominantly in domestic familiar environments."

    return {
        "birth_date": f"{day:02d}/{month:02d}/{year}",
        "driver": driver,
        "conductor": conductor,
        "target_year": t_year,
        "personal_year": py,
        "overall_travel_potency_score": min(travel_score, 100),
        "settlement_verdict": settlement_potential,
        "settlement_details": settlement_details,
        "current_year_travel_status": py_status,
        "current_year_timing_note": py_note,
        "detected_indicators": indicators_found,
        "favorable_travel_directions": (
            "North-West (international transit zone) and North (commercial prosperity)"
            if driver in [1, 3, 5, 6] else "West and South-West"
        )
    }


# ── NV-018 Health & Wellbeing Interpretation (Safe Use) ───────────────────────
VITALITY_CONSTITUTION_MAP: Dict[int, Dict[str, Any]] = {
    1: {
        "planet": "Sun (Surya)",
        "constitution": "Pitta (Fiery / Metabolic Energy)",
        "focus_areas": "Cardiovascular circulation, spine posture, eye vitality, daylight synthesis.",
        "age_40_guidance": "After age 40, prioritize regular cardiovascular checkups, avoid chronic workaholism, and incorporate cooling, hydrating fruits.",
        "restorative_habits": "Morning solar light walks, pure water in copper vessel, breathwork (Sheetali Pranayama)."
    },
    2: {
        "planet": "Moon (Chandra)",
        "constitution": "Kapha / Vata (Hydration & Fluid Balance)",
        "focus_areas": "Lymphatic balance, digestive rhythm, emotional sleep hygiene, hydration.",
        "age_40_guidance": "After age 40, guard against emotional overeating or insomnia; practice consistent nighttime sleep routines.",
        "restorative_habits": "Drinking warm herbal infusions (tulsi/ginger), avoiding heavy dairy before sleep, mindfulness meditation."
    },
    3: {
        "planet": "Jupiter (Guru)",
        "constitution": "Kapha (Metabolic & Liver Harmony)",
        "focus_areas": "Liver wellness, arterial health, healthy lipid management, dietary balance.",
        "age_40_guidance": "After age 40, moderate rich, sugary, or fried foods; engage in steady brisk daily walking.",
        "restorative_habits": "Intermittent fasting routines, turmeric warm water in the morning, joyful intellectual reading."
    },
    4: {
        "planet": "Rahu",
        "constitution": "Vata (Nervous System & Electro-Magnetic Balance)",
        "focus_areas": "Central nervous system, mental relaxation, respiratory calm, digestive regularity.",
        "age_40_guidance": "After age 40, reduce screen time before bed to prevent nervous overstimulation; maintain predictable meal schedules.",
        "restorative_habits": "Barefoot grounding on natural grass, ashwagandha herbal teas, warm oil foot massages at bedtime."
    },
    5: {
        "planet": "Mercury (Budh)",
        "constitution": "Vata / Pitta (Speed & Nervous Agility)",
        "focus_areas": "Speech stamina, skin hydration, respiratory lungs, nervous reflexes.",
        "age_40_guidance": "After age 40, guard against mental exhaustion from multitasking; schedule dedicated technology detox hours.",
        "restorative_habits": "Regular deep diaphragmatic breathing, eating green leafy vegetables, staying well-hydrated throughout trading/work hours."
    },
    6: {
        "planet": "Venus (Shukra)",
        "constitution": "Kapha / Vata (Sensory Balance & Hormonal Rhythm)",
        "focus_areas": "Kidney balance, throat clarity, reproductive hormonal harmony, skin glow.",
        "age_40_guidance": "After age 40, maintain kidney filtration health with adequate water; avoid excessive luxury overindulgence.",
        "restorative_habits": "Natural rose water face cleansing, gentle yoga, maintaining clean and aesthetically pleasing resting spaces."
    },
    7: {
        "planet": "Ketu",
        "constitution": "Vata (Psychological Tranquility & Subtle Nervous Energy)",
        "focus_areas": "Psychological calm, allergy sensitivity, dream cycle rest, gut-brain axis.",
        "age_40_guidance": "After age 40, prioritize quiet nature walks and avoid absorbing negative social ambiance; nurture gut health with probiotics.",
        "restorative_habits": "Quiet meditation, eating fresh warm home-cooked meals, avoiding cold packaged processed foods."
    },
    8: {
        "planet": "Saturn (Shani)",
        "constitution": "Vata (Structural Bones, Joints & Connective Tissue)",
        "focus_areas": "Bone density, joint lubrication, dental care, lower back ergonomics, leg circulation.",
        "age_40_guidance": "After age 40, incorporate joint mobility exercises, calcium-rich sesame seeds, and ergonomic desk support.",
        "restorative_habits": "Mustard or sesame oil self-massage (Abhyanga), gentle resistance stretching, staying warm in cold seasons."
    },
    9: {
        "planet": "Mars (Mangal)",
        "constitution": "Pitta (Muscular Stamina & Blood Vitality)",
        "focus_areas": "Muscular recovery, blood pressure moderation, body temperature regulation, avoiding rash physical injury.",
        "age_40_guidance": "After age 40, balance high-intensity athletic bursts with cooling yoga; guard against hot temper and high blood pressure.",
        "restorative_habits": "Drinking coconut water, regular hydration, cooling cucumber and mint salads, avoiding spicy foods."
    }
}


def evaluate_health_and_wellbeing(
    driver: int,
    conductor: int,
    current_age: Optional[int] = 30
) -> Dict[str, Any]:
    """
    NV-018 Requirement: Health & Wellbeing Interpretation (Safe Use).
    COMPLIANCE INVARIANT:
    Strictly qualified as lifestyle wellness and traditional vitality indicators.
    Contains zero medical diagnostics or drug recommendations.
    """
    d_vitality = VITALITY_CONSTITUTION_MAP.get(driver, VITALITY_CONSTITUTION_MAP[1])
    c_vitality = VITALITY_CONSTITUTION_MAP.get(conductor, VITALITY_CONSTITUTION_MAP[1])

    is_post_40 = (current_age or 30) >= 40

    return {
        "driver": driver,
        "conductor": conductor,
        "current_age": current_age,
        "is_second_life_phase_active": is_post_40,
        "primary_constitution": d_vitality["constitution"],
        "primary_vitality_system": d_vitality["focus_areas"],
        "destiny_vitality_system": c_vitality["focus_areas"],
        "age_transition_guidance": (
            d_vitality["age_40_guidance"] if is_post_40 else
            f"Currently in foundation phase (under 40). Lay robust habits now: {d_vitality['focus_areas']}."
        ),
        "daily_restorative_habits": [
            d_vitality["restorative_habits"],
            c_vitality["restorative_habits"],
            "Maintain 2.5 to 3 liters of daily pure water intake synchronized with your natural daylight cycle."
        ],
        "statutory_compliance_disclaimer": (
            "IMPORTANT STATUTORY DISCLAIMER: This wellbeing analysis is grounded strictly in classical Indian philosophical "
            "and Ayurvedic lifestyle traditions (Pitta/Kapha/Vata archetypes). It does not constitute medical advice, diagnosis, "
            "treatment, or clinical prescription under the Indian Drugs and Magic Remedies (Objectionable Advertisements) Act 1954 "
            "or medical practitioner regulations. Always consult a qualified, licensed healthcare professional for any medical symptoms or conditions."
        )
    }
