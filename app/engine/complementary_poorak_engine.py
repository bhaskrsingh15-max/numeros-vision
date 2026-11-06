# -*- coding: utf-8 -*-
"""
COMPLEMENTARY (POORAK / पूरक) NUMBERS & MASTER KEY 5 ENGINE
Numeros Vision — Master Knowledge Engine (Day 8 Canon)
Calculates the harmonizing peacemaker number, quality-specific complementary support,
and Lo Shu grid completion anchor in strict compliance with AGENTS.md.
"""

from typing import Dict, Any, List, Optional

# ── DAY 8 CANONICAL QUALITY-SPECIFIC COMPLEMENTARY REGISTRY ──────────────────
# Source: Day 8 Transcript & Whiteboard Charts (Numeros Vision)
DAY8_QUALITY_COMPLEMENTARY_REGISTRY: Dict[int, Dict[str, Any]] = {
    1: {
        "subject_number": 1,
        "planet": "Sun (Surya)",
        "complements": [9],
        "supported_qualities": {
            9: "Authority supported by a commander or trusted executor (courage, physical action, military execution)"
        },
        "limitation": "Number 9 provides execution and physical defense, but cannot replace Sun's sovereign vision or administrative royalty.",
        "evidence_type": "source_statement",
        "confidence_status": "approved"
    },
    2: {
        "subject_number": 2,
        "planet": "Moon (Chandra)",
        "complements": [3, 7],
        "supported_qualities": {
            3: "Mind and decision-making supported by knowledge, pedagogical wisdom, and philosophical perspective",
            7: "Mind and decision-making supported by spiritual thinking, intuition, and occult depth"
        },
        "limitation": "Numbers 3 and 7 provide intellectual and spiritual clarity, not maternal emotional warmth or diplomatic gentleness.",
        "evidence_type": "source_statement",
        "confidence_status": "approved"
    },
    3: {
        "subject_number": 3,
        "planet": "Jupiter (Guru)",
        "complements": [7],
        "supported_qualities": {
            7: "Knowledge, education, wisdom, and spirituality supported by deep research and esoteric insight"
        },
        "limitation": "Number 7 provides solitary introspective depth, but lacks Jupiter's broad public preaching and institutional expansion.",
        "evidence_type": "source_statement",
        "confidence_status": "approved"
    },
    4: {
        "subject_number": 4,
        "planet": "Rahu (North Node)",
        "complements": [8],
        "supported_qualities": {
            8: "Discipline and time-related discipline (laborious stamina, legal rigor, systematic perseverance)"
        },
        "limitation": "Instructor explicitly limits the 8-to-4 relationship to discipline; Number 8 does NOT replace Rahu's unconventional system engineering or rapid technical improvisation.",
        "evidence_type": "source_statement",
        "confidence_status": "approved"
    },
    5: {
        "subject_number": 5,
        "planet": "Mercury (Budh) / Master Key",
        "complements": [6],
        "supported_qualities": {
            6: "Balance and relationship-related support, family stability, and supportive social luxury"
        },
        "limitation": "Number 6 provides domestic harmony and aesthetic balance, but does not provide Mercury's central Earth axis or commercial trading agility.",
        "evidence_type": "source_statement",
        "confidence_status": "approved"
    },
    6: {
        "subject_number": 6,
        "planet": "Venus (Shukra)",
        "complements": [5],
        "supported_qualities": {
            5: "Balance, commercial agility, and relationship stabilizer when 6 is absent"
        },
        "limitation": "Number 5 stabilizes relationships through intellect and communication, but cannot manufacture artistic/material luxury without effort.",
        "evidence_type": "source_statement",
        "confidence_status": "approved"
    },
    7: {
        "subject_number": 7,
        "planet": "Ketu (South Node)",
        "complements": [3],
        "supported_qualities": {
            3: "Knowledge, wisdom, and positive fulfillment (mentorship, ethical grounding, public guidance)"
        },
        "limitation": "Number 3 provides outer optimism and guidance, but does not replace Ketu's surgical occult detachment and analytical skepticism.",
        "evidence_type": "source_statement",
        "confidence_status": "approved"
    },
    8: {
        "subject_number": 8,
        "planet": "Saturn (Shani)",
        "complements": [4, 5],
        "supported_qualities": {
            4: "Discipline, structural organization, and practical task execution supported by Rahu's focus",
            5: "Money management, commercial balance, and financial agility supported by Mercury"
        },
        "limitation": "Number 4 provides structural focus and 5 provides financial agility, but neither replaces Saturn's long-term justice karma and compounding endurance.",
        "evidence_type": "source_statement",
        "confidence_status": "approved"
    },
    9: {
        "subject_number": 9,
        "planet": "Mars (Mangal)",
        "complements": [1],
        "supported_qualities": {
            1: "Execution and leadership supported by the king or authority figure (sovereign direction, administrative status)"
        },
        "limitation": "Number 1 gives direction and royal status, but lacks Mars's raw battlefield stamina, hands-on defense, and physical courage.",
        "evidence_type": "source_statement",
        "confidence_status": "approved"
    }
}

POORAK_DATA = {
    "master_poorak_map": {
        1: {
            "complementary": [9],
            "planet": "Mars (Mangal)",
            "role": "Authority supported by a commander or trusted executor (courage, physical action, military execution)."
        },
        2: {
            "complementary": [3, 7],
            "planet": "Jupiter & Ketu",
            "role": "Mind and decision-making supported by knowledge/pedagogy (3) and spiritual thinking/intuition (7)."
        },
        3: {
            "complementary": [7],
            "planet": "Ketu (South Node)",
            "role": "Knowledge, education, wisdom and spirituality supported by deep research and esoteric insight."
        },
        4: {
            "complementary": [8],
            "planet": "Saturn (Shani)",
            "role": "Discipline and time-related discipline (laborious stamina, legal rigor). Limited strictly to discipline; does not replace Rahu's unconventional systems."
        },
        5: {
            "complementary": [6],
            "planet": "Venus (Shukra)",
            "role": "Balance and relationship-related support, family stability, and supportive social luxury."
        },
        6: {
            "complementary": [5],
            "planet": "Mercury (Budh)",
            "role": "Provides witty commercial networking, agile dealmaking, and relationship balance (Day 8: 5 supports 6)."
        },
        7: {
            "complementary": [3],
            "planet": "Jupiter (Guru)",
            "role": "Knowledge, wisdom, and positive fulfillment (mentorship, ethical grounding, public guidance)."
        },
        8: {
            "complementary": [4, 5],
            "planet": "Rahu & Mercury",
            "role": "Discipline supported by 4; money management and balance supported by 5."
        },
        9: {
            "complementary": [1],
            "planet": "Sun (Surya)",
            "role": "Execution and leadership supported by the king or authority figure (sovereign direction, administrative status)."
        }
    },
    "friction_pair_peacemakers": {
        "1_8": {
            "poorak": 5,
            "peacemaker_planet": "Mercury (Budh)",
            "rationale": "Number 5 dissolves Sun-Saturn father-son friction with commerce, diplomacy, and neutral mental agility."
        },
        "8_1": {
            "poorak": 5,
            "peacemaker_planet": "Mercury (Budh)",
            "rationale": "Number 5 dissolves Saturn-Sun authority deadlock through contractual flexibility and commercial compromise."
        },
        "2_4": {
            "poorak": 6,
            "peacemaker_planet": "Venus (Shukra)",
            "rationale": "Number 6 soothes Moon-Rahu eclipse anxiety through aesthetic beauty, domestic harmony, and gentle luxury."
        },
        "4_2": {
            "poorak": 6,
            "peacemaker_planet": "Venus (Shukra)",
            "rationale": "Number 6 softens Rahu-Moon mental turbulence with artistic grace and emotional reassurance."
        },
        "2_8": {
            "poorak": 5,
            "peacemaker_planet": "Mercury (Budh)",
            "rationale": "Number 5 stabilizes Moon-Saturn Vish Yoga depression through active logical communication and commercial focus."
        },
        "8_2": {
            "poorak": 5,
            "peacemaker_planet": "Mercury (Budh)",
            "rationale": "Number 5 overcomes Saturn-Moon chronic delays with energetic adaptability and social networking."
        },
        "2_9": {
            "poorak": 1,
            "peacemaker_planet": "Sun (Surya)",
            "rationale": "Number 1 brings noble sovereign harmony to Moon-Mars fire-water volatility, commanding mutual respect."
        },
        "9_2": {
            "poorak": 1,
            "peacemaker_planet": "Sun (Surya)",
            "rationale": "Number 1 grounds Mars-Moon emotional clashes through dignified executive purpose."
        },
        "3_6": {
            "poorak": 7,
            "peacemaker_planet": "Ketu (South Node)",
            "rationale": "Number 7 reconciles Dev Guru (3) and Daitya Guru (6) by transmuting luxury into sacred philanthropy and high healing insight."
        },
        "6_3": {
            "poorak": 7,
            "peacemaker_planet": "Ketu (South Node)",
            "rationale": "Number 7 harmonizes Venus-Jupiter 36 ka aankda through spiritual detachment and deep holistic research."
        },
        "4_4": {
            "poorak": 6,
            "peacemaker_planet": "Venus (Shukra)",
            "rationale": "Number 6 cools dual Rahu erratic disruptions with domestic peace, artistic elegance, and luxury comfort."
        },
        "4_8": {
            "poorak": 5,
            "peacemaker_planet": "Mercury (Budh)",
            "rationale": "Number 5 breaks Rahu-Saturn dark karmic stagnation through light commercial movement and flexible trading."
        },
        "8_4": {
            "poorak": 5,
            "peacemaker_planet": "Mercury (Budh)",
            "rationale": "Number 5 introduces agile communication to Saturn-Rahu heavy delays, unlocking contractual progress."
        },
        "4_9": {
            "poorak": 6,
            "peacemaker_planet": "Venus (Shukra)",
            "rationale": "Number 6 cools Rahu-Mars Angarak combative tension with diplomatic charm and aesthetic pacing."
        },
        "9_4": {
            "poorak": 6,
            "peacemaker_planet": "Venus (Shukra)",
            "rationale": "Number 6 tempers Mars-Rahu surgical aggression with peaceful luxury and balanced restraint."
        },
        "6_9": {
            "poorak": 5,
            "peacemaker_planet": "Mercury (Budh)",
            "rationale": "Number 5 brings objective balance, clear communication, and commercial focus to high-energy creative drives."
        },
        "9_6": {
            "poorak": 5,
            "peacemaker_planet": "Mercury (Budh)",
            "rationale": "Number 5 harmonizes dynamic passion into structured creative and commercial endeavors."
        },
        "7_7": {
            "poorak": 1,
            "peacemaker_planet": "Sun (Surya)",
            "rationale": "Number 1 brings decisive executive clarity, focused ambition, and clear forward momentum to dual introspective energies."
        },
        "8_8": {
            "poorak": 5,
            "peacemaker_planet": "Mercury (Budh)",
            "rationale": "Number 5 balances deep structural focus with commercial adaptability, social ease, and intellectual lightness."
        },
        "9_9": {
            "poorak": 1,
            "peacemaker_planet": "Sun (Surya)",
            "rationale": "Number 1 channels intense drive and courage into purposeful leadership and impactful public initiatives."
        }
    }
}

PLANET_DETAILS = {
    1: {"planet": "Sun (Surya)", "element": "Water/Fire Core", "color": "Gold, Saffron, Amber", "direction": "North / East"},
    2: {"planet": "Moon (Chandra)", "element": "Earth/Water", "color": "Pearl White, Silver", "direction": "South-West / North-West"},
    3: {"planet": "Jupiter (Guru)", "element": "Wood", "color": "Yellow, Golden Yellow", "direction": "East / North-East"},
    4: {"planet": "Rahu (North Node)", "element": "Wood", "color": "Smoky Blue, Gray", "direction": "South-East"},
    5: {"planet": "Mercury (Budh)", "element": "Earth", "color": "Emerald Green, Mint", "direction": "Center (Brahma Sthana)"},
    6: {"planet": "Venus (Shukra)", "element": "Metal (Gold)", "color": "White, Cream, Rose Gold", "direction": "North-West"},
    7: {"planet": "Ketu (South Node)", "element": "Metal (Silver)", "color": "Silver, Smoky White", "direction": "West"},
    8: {"planet": "Saturn (Shani)", "element": "Earth", "color": "Navy Blue, Charcoal", "direction": "North-East / West"},
    9: {"planet": "Mars (Mangal)", "element": "Fire", "color": "Crimson Red, Maroon", "direction": "South"}
}


def calculate_complementary_poorak(driver: int, conductor: int, missing_numbers: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    Calculates the Poorak (Complementary / Harmonizing) Number:
    1. If Driver and Conductor have friction, identifies the specific peacemaker planet.
    2. If Driver and Conductor are friendly, identifies the prime missing number (5 or 6).
    3. Returns full ritual, colors, vastu direction, and daily practical action.
    """
    key = f"{driver}_{conductor}"
    friction_rules = POORAK_DATA["friction_pair_peacemakers"]
    master_map = POORAK_DATA["master_poorak_map"]
    
    if key in friction_rules:
        item = friction_rules[key]
        p_num = item["poorak"]
        p_info = PLANET_DETAILS.get(p_num, PLANET_DETAILS[5])
        return {
            "poorak_number": p_num,
            "poorak_planet": p_info["planet"],
            "poorak_element": p_info["element"],
            "poorak_color": p_info["color"],
            "poorak_direction": p_info["direction"],
            "is_friction_resolution": True,
            "synergy_type": "Friction Peacemaker Bridge",
            "rationale": item["rationale"],
            "harmonizing_ritual": f"Activate Number {p_num} by incorporating {p_info['color'].split(',')[0]} accents and balancing the {p_info['direction']} sector of your primary room."
        }
    
    # Friendly or Neutral: Check missing numbers or master complementary
    if missing_numbers and 5 in missing_numbers:
        p_num = 5
        rationale = "Number 5 (Mercury) fills the central Earth anchor of your Lo Shu Grid, providing unshakable emotional stability and commercial compounding."
    elif missing_numbers and 6 in missing_numbers:
        p_num = 6
        rationale = "Number 6 (Venus) completes your luxury and supportive networks plane, attracting high-net-worth mentors and material comfort."
    else:
        comp_entry = master_map.get(driver) or master_map.get(str(driver), {})
        comp_list = comp_entry.get("complementary", [5])
        p_num = comp_list[0] if isinstance(comp_list[0], int) else 5
        rationale = comp_entry.get("role", "Serves as the complementary cosmic amplifier for your Driver-Conductor alliance.")
    
    p_info = PLANET_DETAILS.get(p_num, PLANET_DETAILS[5])
    return {
        "poorak_number": p_num,
        "poorak_planet": p_info["planet"],
        "poorak_element": p_info["element"],
        "poorak_color": p_info["color"],
        "poorak_direction": p_info["direction"],
        "is_friction_resolution": False,
        "synergy_type": "Grid Completion & Cosmic Amplifier",
        "rationale": rationale,
        "harmonizing_ritual": f"Activate Number {p_num} by incorporating {p_info['color'].split(',')[0]} accents and balancing the {p_info['direction']} sector of your primary room."
    }


def evaluate_grid_complementary_support(loshu_grid: Dict[int, int]) -> Dict[str, Any]:
    """
    Executes the 6-Step Numeros Vision Day 8 Complementary Support & Master Key 5 Pipeline:
    
    Step 1: Parse and normalize Lo Shu grid digit counts (1-9).
    Step 2: Identify present digits (count > 0) and absent digits (count == 0).
    Step 3: Map absent digits to their Day 8 quality-specific complementary numbers.
    Step 4: Check which complementary numbers are present in the seeker's grid.
    Step 5: Generate qualified interpretations separating supported qualities from missing aspects.
    Step 6: Flag uncompensated areas for approved remedies without claiming direct causality.
    Step 7: Evaluate Master Key 5 rules (general balance, Fighter archetype, 1-5-9 willpower plane,
            and unverified remedy multiplier caveat).
    """
    normalized_grid = {i: int(loshu_grid.get(i, 0)) for i in range(1, 10)}
    present_numbers = [n for n, count in normalized_grid.items() if count > 0]
    absent_numbers = [n for n, count in normalized_grid.items() if count == 0]
    
    analysis_records = []
    uncompensated_numbers = []
    
    for missing_num in absent_numbers:
        meta = DAY8_QUALITY_COMPLEMENTARY_REGISTRY.get(missing_num)
        if not meta:
            continue
        
        complements = meta["complements"]
        active_complements = [c for c in complements if normalized_grid.get(c, 0) > 0]
        supported_qualities = [meta["supported_qualities"][c] for c in active_complements if c in meta["supported_qualities"]]
        
        is_compensated = len(active_complements) > 0
        if not is_compensated:
            uncompensated_numbers.append(missing_num)
            
        analysis_records.append({
            "missing_number": missing_num,
            "planet": meta["planet"],
            "configured_complements": complements,
            "active_complements": active_complements,
            "is_compensated": is_compensated,
            "supported_qualities": supported_qualities,
            "limitation": meta["limitation"],
            "status": "COMPENSATED" if is_compensated else "UNCOMPENSATED",
            "interpretation": (
                f"Although Number {missing_num} ({meta['planet']}) is absent in the Lo Shu grid, "
                f"presence of complementary Number(s) {active_complements} provides support: "
                f"{'; '.join(supported_qualities)}. Note limitation: {meta['limitation']}"
                if is_compensated else
                f"Number {missing_num} ({meta['planet']}) and its complementary partner(s) {complements} "
                f"are both absent. This domain lacks internal grid reinforcement and warrants conscious lifestyle discipline or an approved remedy."
            )
        })
    
    # ── Master Key Number 5 Evaluation ─────────────────────────────────────────
    has_5 = normalized_grid.get(5, 0) > 0
    has_1 = normalized_grid.get(1, 0) > 0
    has_9 = normalized_grid.get(9, 0) > 0
    has_6 = normalized_grid.get(6, 0) > 0
    
    willpower_159_active = has_1 and has_5 and has_9
    missing_6_stabilized = (not has_6) and has_5
    
    master_key_5_report = {
        "is_number_5_present": has_5,
        "frequency": normalized_grid.get(5, 0),
        "fighter_archetype_active": has_5,
        "fighter_archetype_description": (
            "Number 5 in central Earth sector acts as an internal resilience anchor, conferring persistence, "
            "adaptability, and a fighter mindset to navigate challenges without surrender."
            if has_5 else
            "Number 5 absent from central sector; emotional persistence requires conscious grounding routines."
        ),
        "willpower_plane_159": {
            "is_fully_present": willpower_159_active,
            "digits_present": [n for n in [1, 5, 9] if normalized_grid.get(n, 0) > 0],
            "status": "ACTIVE_WILLPOWER_PLANE" if willpower_159_active else "PARTIAL_OR_ABSENT",
            "interpretation": (
                "Numbers 1, 5, and 9 are all present in the Lo Shu grid, activating the Willpower Plane. "
                "The instructor framework describes this as a light activation of decisive willpower and perseverance."
                if willpower_159_active else
                "Willpower plane (1-5-9) is incomplete; native must rely on deliberate habit architectures."
            )
        },
        "missing_6_support": {
            "applies": missing_6_stabilized,
            "description": (
                "Number 6 is absent, but Number 5 is present. In the instructor's framework, Number 5 acts as a "
                "commercial and relational stabilizer to mitigate friction caused by absent 6."
                if missing_6_stabilized else
                "Not applicable."
            )
        },
        "remedy_acceleration_claim": {
            "claim": "Remedies work faster or produce multiplied results when 5 is present.",
            "implementation_treatment": "UNVERIFIED_TEACHING_CLAIM",
            "disclaimer": "Retained as an instructor teaching proposition; strictly NOT presented as a guaranteed or scientifically validated causal outcome."
        }
    }
    
    return {
        "pipeline_version": "1.0.0",
        "system": "Numeros Vision Day 8 Complementary & Master Key 5 Pipeline",
        "present_numbers": present_numbers,
        "absent_numbers": absent_numbers,
        "evaluations": analysis_records,
        "uncompensated_numbers": uncompensated_numbers,
        "master_key_5_evaluation": master_key_5_report,
        "governance_note": (
            "A missing grid number provides input for qualitative interpretation, not empirical proof of life failure. "
            "Complementary support highlights internal compensations without fabricating universal replacement."
        )
    }
