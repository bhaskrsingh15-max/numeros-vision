"""
CORE MATRIX NUMEROLOGY ENGINE
Numeros Vision — ANVEIL EVERY CHARM

Comprehensive, deterministic engine providing:
1. Core Matrix Calculations: Driver (Mulank), Conductor (Bhagyank), Kua Number, Name Number (Chaldean & Pythagorean).
2. Karmic Debt Numbers Detection: 13, 14, 16, 19.
3. Master Numbers Detection: 11, 22, 33.
4. Dasha & Antardasha Cycles: Mahadasha, Antardasha, Personal Year (PY), Personal Month (PM), Personal Day (PD).
5. Elements Balancing (5 Elements): Wood (3,4), Fire (9), Earth (2,5,8), Metal (6,7), Water (1).
6. Malefic & Benefic Repeat Numbers in the Grid & Mobile.
7. Missing Numbers in the Core Matrix & Practical Elemental Remedies.
8. Common Life Domain Predictions & Practical Remedies (Gemstone/Crystals, Color Therapy, Vastu Directions).
"""

from typing import Dict, Any, List, Optional
import datetime

from app.engine.kua import (
    KUA_METADATA,
    KUA_NEEDS_GENDER_TEXT,
    KUA_RULE_TEXT,
    calculate_kua_details,
    calculate_kua_number as _canonical_calculate_kua_number,
)

# ── 1. Planetary Rulers & Core Vibrations ───────────────────────────────────────
PLANETARY_MATRIX = {
    1: {"planet": "Sun", "element": "Water", "color": "Gold, Orange, Copper", "direction": "North", "nature": "Executive leadership, self-reliance, vital force"},
    2: {"planet": "Moon", "element": "Earth", "color": "White, Cream, Silver", "direction": "South-West", "nature": "Intuition, diplomatic harmony, mental calm"},
    3: {"planet": "Jupiter", "element": "Wood", "color": "Yellow, Saffron, Amber", "direction": "East", "nature": "Expansion, wisdom, mentorship, moral vision"},
    4: {"planet": "Uranus / Rahu", "element": "Wood", "color": "Electric Blue, Grey, Khaki", "direction": "South-East", "nature": "Strategic innovation, unconventional intellect, structures"},
    5: {"planet": "Mercury", "element": "Earth", "color": "Emerald Green, Turquoise", "direction": "Center", "nature": "Commercial acumen, versatility, networking, rapid balance"},
    6: {"planet": "Venus", "element": "Metal", "color": "Diamond White, Soft Pink, Cream", "direction": "North-West", "nature": "Luxury, creative refinement, relationship cohesion"},
    7: {"planet": "Neptune / Ketu", "element": "Metal", "color": "Pastel Green, Light Grey, Lavender", "direction": "West", "nature": "Deep research, spiritual insight, analytical detachment"},
    8: {"planet": "Saturn", "element": "Earth", "color": "Dark Blue, Navy, Charcoal", "direction": "North-East", "nature": "Discipline, compounding perseverance, karmic integrity"},
    9: {"planet": "Mars", "element": "Fire", "color": "Red, Rose, Coral", "direction": "South", "nature": "Dynamic courage, decisive execution, humanitarian drive"}
}

# ── 2. Five Elements Mapping ──────────────────────────────────────────────────
ELEMENT_RULES = {
    "Water": {"numbers": [1], "qualities": "Career flow, intellectual depth, fluid communication", "deficient_remedy": "Place clean flowing water / small fountain in North; use blue/white hues."},
    "Wood": {"numbers": [3, 4], "qualities": "Expansion, family harmony, long-range planning, health", "deficient_remedy": "Keep healthy green plants in East/South-East; use natural wood items."},
    "Fire": {"numbers": [9], "qualities": "Fame, reputation, passion, recognition, dynamic enthusiasm", "deficient_remedy": "Ensure bright illumination in South; use warm lighting or coral/red accents."},
    "Earth": {"numbers": [2, 5, 8], "qualities": "Stability, centeredness, real estate, patience, grounding", "deficient_remedy": "Keep natural crystals, terracotta, or yellow stones in Center/South-West."},
    "Metal": {"numbers": [6, 7], "qualities": "Discernment, helpful friends, luxury, spiritual intuition", "deficient_remedy": "Use brass/silver accents, metallic wind chime, or white quartz in West/North-West."}
}

# ── 3. Chaldean Letter Values ─────────────────────────────────────────────────
CHALDEAN_VALUES = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'C': 2, 'K': 2, 'R': 2,
    'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
}

from app.engine.digit_root import (
    digit_root,
    calc_driver as _canonical_calc_driver,
    calc_bhagyank as _canonical_calc_bhagyank,
    calc_personal_year as _canonical_calc_personal_year,
    calc_personal_month as _canonical_calc_personal_month,
    calc_personal_day as _canonical_calc_personal_day,
)

KARMIC_DEBT_NUMBERS = {13, 14, 16, 19}
MASTER_NUMBERS: set[int] = set()

# ── 4. Calculation Utilities ──────────────────────────────────────────────────
def reduce_to_single_digit(n: int) -> int:
    """Canonical single-digit reduction 1..9 via shared digit_root (never preserves 11/22/33)."""
    return digit_root(int(n))

def calculate_driver(day: int) -> int:
    """Driver (Mulank): day of birth reduced strictly to single digit 1-9."""
    return _canonical_calc_driver(day)

def calculate_conductor(day: int, month: int, year: int) -> int:
    """Conductor (Bhagyank): sum of all DOB digits reduced strictly to single digit 1-9."""
    return _canonical_calc_bhagyank(day, month, year)

def calculate_conductor_details(day: int, month: int, year: int) -> Dict[str, Any]:
    """
    Canonical Core Matrix Conductor (Bhagyank) details:
    - conductor_raw: reduced single digit 1-9 (never 11, 22, 33)
    - conductor_root: reduced single digit 1-9
    - conductor_display: '1'..'9'
    - conductor_planet: planet from the reduced digit (root)
    """
    root = _canonical_calc_bhagyank(day, month, year)
    display = str(root)
    planet_short = {
        1: "Sun",
        2: "Moon",
        3: "Jupiter",
        4: "Rahu",
        5: "Mercury",
        6: "Venus",
        7: "Ketu",
        8: "Saturn",
        9: "Mars"
    }.get(root, "Sun")
    return {
        "conductor_raw": root,
        "conductor_root": root,
        "conductor_display": display,
        "conductor_planet": planet_short,
        "is_master": False
    }

def calculate_kua_number(year: int, gender: Optional[str] = None) -> Optional[int]:
    """
    Canonical century-invariant Kua calculation:
    x = single-digit sum of all 4 digits of calendar birth year.
    Male: 11 - x -> single digit (5 -> 2).
    Female: 4 + x -> single digit (5 -> 8).
    Missing gender returns None (never guesses).
    """
    return _canonical_calculate_kua_number(year, gender)

# ── Angelic Resonance Matrix (Vibrational Synchronicities) ─────────────────────
ANGEL_NUMBERS_BY_ROOT = {
    1: {"angel_sequence": "111 & 1010", "title": "Divine Awakening & New Manifestations", "message": "Your creative willpower and thoughts are rapidly materializing. Maintain focus on high-integrity goals."},
    2: {"angel_sequence": "222 & 1212", "title": "Angelic Harmony & Divine Timing", "message": "Patience and emotional equilibrium are blessed. Trust the divine unfolding in partnerships and personal life."},
    3: {"angel_sequence": "333 & 123", "title": "Ascended Master Grace & Creative Expansion", "message": "Enlightened guides amplify your self-expression, mentorship ability, and joy. Speak your truth freely."},
    4: {"angel_sequence": "444 & 1414", "title": "Angelic Shield & Structural Support", "message": "Guardian angels surround and protect your efforts. Your steady labor is establishing lasting earthly security."},
    5: {"angel_sequence": "555 & 1055", "title": "Positive Evolution & Breakthrough Liberty", "message": "Transformational winds are clearing outdated limits. Welcome dynamic change and seize fresh horizons."},
    6: {"angel_sequence": "666 (Harmonized) & 1616", "title": "Heart Concord, Family Peace & Material Grace", "message": "Domestic warmth and unconditional love are protected. Trust that daily needs are gracefully provided for."},
    7: {"angel_sequence": "777 & 1717", "title": "Spiritual Illumination & Miraculous Protection", "message": "You walk the path of profound inner wisdom. Deep mystical insight, intuition, and divine favor guide you."},
    8: {"angel_sequence": "888 & 1818", "title": "Infinite Prosperity & Karmic Harvest", "message": "The infinite loop of wealth and cosmic justice is active. Past ethical endurance manifests as compounding reward."},
    9: {"angel_sequence": "999 & 1919", "title": "Sacred Completion & Higher Calling", "message": "An old chapter closes to awaken your grand humanitarian purpose. Step forward into your higher leadership calling."}
}

# ── Cosmic Directional Science & Prosperous Orientations ─────────────────────
KUA_CHARACTERISTICS = {
    1: {
        "group": "East Group",
        "element": "Water",
        "energy_archetype": "Flowing Water & Intuitive Clarity",
        "wealth_direction": "South-East (Prosperous Expansion Vector)",
        "health_direction": "East (Vitality & Healing Alignment)",
        "relationship_direction": "South (Harmonious Union & Love Alignment)",
        "clarity_direction": "North (Inner Peace & Wisdom Sanctuary)",
        "traits": "Deep strategic intuition, fluid adaptability, communicative clarity, diplomacy."
    },
    2: {
        "group": "West Group",
        "element": "Earth",
        "energy_archetype": "Nourishing Earth & Deep Grounding",
        "wealth_direction": "North-East (Prosperous Expansion Vector)",
        "health_direction": "West (Vitality & Healing Alignment)",
        "relationship_direction": "North-West (Harmonious Union & Love Alignment)",
        "clarity_direction": "South-West (Inner Peace & Wisdom Sanctuary)",
        "traits": "Maternal nourishment, steady patience, grounding real estate instincts, endurance."
    },
    3: {
        "group": "East Group",
        "element": "Wood",
        "energy_archetype": "Pioneering Wood & Radiant Growth",
        "wealth_direction": "South (Prosperous Expansion Vector)",
        "health_direction": "North (Vitality & Healing Alignment)",
        "relationship_direction": "South-East (Harmonious Union & Love Alignment)",
        "clarity_direction": "East (Inner Peace & Wisdom Sanctuary)",
        "traits": "Dynamic growth, pioneering courage, righteous ambition, expansive mentorship."
    },
    4: {
        "group": "East Group",
        "element": "Wood",
        "energy_archetype": "Gentle Breeze & Creative Inspiration",
        "wealth_direction": "North (Prosperous Expansion Vector)",
        "health_direction": "South (Vitality & Healing Alignment)",
        "relationship_direction": "East (Harmonious Union & Love Alignment)",
        "clarity_direction": "South-East (Inner Peace & Wisdom Sanctuary)",
        "traits": "Creative versatility, flexible communication, international networking, gentle persistence."
    },
    5: {
        "group": "Central Earth",
        "element": "Earth",
        "energy_archetype": "Universal Center & Supreme Equilibrium",
        "wealth_direction": "North-East (Male Alignment) / South-West (Female Alignment)",
        "health_direction": "West (Male Alignment) / North-West (Female Alignment)",
        "relationship_direction": "North-West (Male Alignment) / West (Female Alignment)",
        "clarity_direction": "South-West (Male Alignment) / North-East (Female Alignment)",
        "traits": "Central anchor, supreme balance, diplomatic mediation between opposing currents."
    },
    6: {
        "group": "West Group",
        "element": "Metal",
        "energy_archetype": "Radiant Metal & Sovereign Wisdom",
        "wealth_direction": "West (Prosperous Expansion Vector)",
        "health_direction": "North-East (Vitality & Healing Alignment)",
        "relationship_direction": "South-West (Harmonious Union & Love Alignment)",
        "clarity_direction": "North-West (Inner Peace & Wisdom Sanctuary)",
        "traits": "Executive authority, paternal wisdom, high ethical standards, structured leadership."
    },
    7: {
        "group": "West Group",
        "element": "Metal",
        "energy_archetype": "Refined Metal & Magnetic Joy",
        "wealth_direction": "North-West (Prosperous Expansion Vector)",
        "health_direction": "South-West (Vitality & Healing Alignment)",
        "relationship_direction": "North-East (Harmonious Union & Love Alignment)",
        "clarity_direction": "West (Inner Peace & Wisdom Sanctuary)",
        "traits": "Joyful expression, persuasive speech, artistic charisma, financial magnetism."
    },
    8: {
        "group": "West Group",
        "element": "Earth",
        "energy_archetype": "Steadfast Mountain & Asset Stability",
        "wealth_direction": "South-West (Prosperous Expansion Vector)",
        "health_direction": "North-West (Vitality & Healing Alignment)",
        "relationship_direction": "West (Harmonious Union & Love Alignment)",
        "clarity_direction": "North-East (Inner Peace & Wisdom Sanctuary)",
        "traits": "Mountain-like stability, deep contemplative focus, steady accumulation of assets."
    },
    9: {
        "group": "East Group",
        "element": "Fire",
        "energy_archetype": "Luminous Fire & Solar Illumination",
        "wealth_direction": "East (Prosperous Expansion Vector)",
        "health_direction": "South-East (Vitality & Healing Alignment)",
        "relationship_direction": "North (Harmonious Union & Love Alignment)",
        "clarity_direction": "South (Inner Peace & Wisdom Sanctuary)",
        "traits": "Radiant illumination, public fame, inspirational clarity, humanitarian passion."
    }
}

def get_kua_profile(year: int, gender: Optional[str] = None) -> Dict[str, Any]:
    """Generates complete prosperous direction characteristics and energy group from canonical Kua."""
    details = calculate_kua_details(year, gender)
    kua = details["kua_number"]
    if kua is None:
        angel_info = ANGEL_NUMBERS_BY_ROOT[1]
        return {
            "status": "NEEDS_GENDER",
            "kua_number": None,
            "kua_display": KUA_NEEDS_GENDER_TEXT,
            "energy_group": KUA_NEEDS_GENDER_TEXT,
            "element": KUA_NEEDS_GENDER_TEXT,
            "trigram": KUA_NEEDS_GENDER_TEXT,
            "element_group": KUA_NEEDS_GENDER_TEXT,
            "desk_direction": KUA_NEEDS_GENDER_TEXT,
            "energy_archetype": KUA_NEEDS_GENDER_TEXT,
            "wealth_direction": KUA_NEEDS_GENDER_TEXT,
            "health_direction": KUA_NEEDS_GENDER_TEXT,
            "relationship_direction": KUA_NEEDS_GENDER_TEXT,
            "clarity_direction": KUA_NEEDS_GENDER_TEXT,
            "core_traits": KUA_NEEDS_GENDER_TEXT,
            "rule_note": KUA_RULE_TEXT,
            "angel_number_resonance": {
                "angel_sequence": angel_info["angel_sequence"],
                "title": angel_info["title"],
                "guidance": angel_info["message"]
            },
            "prosperous_orientation_summary": f"{KUA_NEEDS_GENDER_TEXT}. ({KUA_RULE_TEXT})"
        }

    char = KUA_CHARACTERISTICS.get(kua, KUA_CHARACTERISTICS[1])
    angel_info = ANGEL_NUMBERS_BY_ROOT.get(kua, ANGEL_NUMBERS_BY_ROOT[1])
    return {
        "status": "OK",
        "kua_number": kua,
        "kua_display": str(kua),
        "energy_group": details["group"],
        "element": details["element"],
        "trigram": details["trigram"],
        "element_group": details["element_group"],
        "desk_direction": details["desk_direction"],
        "energy_archetype": char["energy_archetype"],
        "wealth_direction": details["wealth_direction"],
        "health_direction": details["health_direction"],
        "relationship_direction": details["relationship_direction"],
        "clarity_direction": details["clarity_direction"],
        "core_traits": char["traits"],
        "rule_note": KUA_RULE_TEXT,
        "angel_number_resonance": {
            "angel_sequence": angel_info["angel_sequence"],
            "title": angel_info["title"],
            "guidance": angel_info["message"]
        },
        "prosperous_orientation_summary": (
            f"As per your personal chart reading ({KUA_RULE_TEXT.lower()}), your primary prosperous direction is {details['wealth_direction']}. "
            f"Aligning your workstation facing this direction supports steady professional focus, "
            f"while facing {details['health_direction']} supports restorative equilibrium."
        )
    }

def calculate_chaldean_name(name: str) -> Dict[str, Any]:
    clean = "".join(c.upper() for c in name if c.isalpha())
    compound = sum(CHALDEAN_VALUES.get(c, 0) for c in clean)
    single = reduce_to_single_digit(compound)
    is_karmic = compound in KARMIC_DEBT_NUMBERS
    return {
        "compound_sum": compound,
        "compound_number": compound,
        "compound": compound,
        "single_root": single,
        "single_digit": single,
        "root": single,
        "root_number": single,
        "is_karmic": is_karmic,
        "is_master": False
    }

# ── 5. Dasha & Personal Cycles ────────────────────────────────────────────────
def calculate_dasha_cycles(day: int, month: int, year: int, current_age: int = 30) -> Dict[str, Any]:
    today = datetime.date.today()
    current_year = today.year
    
    # Personal Year: Day + Month + Current Year (strictly reduced 1..9)
    personal_year = _canonical_calc_personal_year(day, month, current_year)
    
    # Personal Month: Personal Year + Current Month
    personal_month = _canonical_calc_personal_month(personal_year, today.month)
    
    # Personal Day: PY output + PM output + date digits (strictly reduced 1..9)
    personal_day = _canonical_calc_personal_day(personal_year, personal_month, today.day, today.month, today.year)
    
    # Mahadasha: 9-year cycle ruler based on Driver + age progression
    driver = calculate_driver(day)
    cycle_offset = (current_age // 9) % 9
    mahadasha_num = ((driver - 1 + cycle_offset) % 9) + 1
    antardasha_num = ((mahadasha_num - 1 + (current_age % 9)) % 9) + 1
    
    m_info = PLANETARY_MATRIX.get(mahadasha_num, PLANETARY_MATRIX[1])
    a_info = PLANETARY_MATRIX.get(antardasha_num, PLANETARY_MATRIX[1])
    
    return {
        "personal_year": personal_year,
        "personal_month": personal_month,
        "personal_day": personal_day,
        "mahadasha_number": mahadasha_num,
        "mahadasha_planet": m_info["planet"],
        "antardasha_number": antardasha_num,
        "antardasha_planet": a_info["planet"],
        "current_cycle_guidance": f"Personal Year {personal_year} in {m_info['planet']} Mahadasha ({a_info['planet']} sub-period). Focus on {m_info['nature']}."
    }

# ── 6. Elements Balancing Analysis ────────────────────────────────────────────
def analyze_elements_balancing(day: int, month: int, year: int) -> Dict[str, Any]:
    dob_str = f"{day:02d}{month:02d}{year:04d}"
    digits = [int(d) for d in dob_str if d != '0']
    
    element_counts = {"Water": 0, "Wood": 0, "Fire": 0, "Earth": 0, "Metal": 0}
    for d in digits:
        for elem, data in ELEMENT_RULES.items():
            if d in data["numbers"]:
                element_counts[elem] += 1
                
    balanced_elements = [elem for elem, count in element_counts.items() if count in [1, 2]]
    excess_elements = [elem for elem, count in element_counts.items() if count >= 3]
    deficient_elements = [elem for elem, count in element_counts.items() if count == 0]
    
    remedial_actions = []
    for def_elem in deficient_elements:
        remedial_actions.append({
            "element": def_elem,
            "status": "Deficient / Missing",
            "qualities": ELEMENT_RULES[def_elem]["qualities"],
            "balancing_remedy": ELEMENT_RULES[def_elem]["deficient_remedy"]
        })
        
    return {
        "element_counts": element_counts,
        "balanced": balanced_elements,
        "excess": excess_elements,
        "deficient": deficient_elements,
        "element_remedies": remedial_actions
    }

# ── 7. Repeat Numbers Analysis (Benefic vs Malefic) ───────────────────────────
def analyze_repeat_numbers(day: int, month: int, year: int) -> Dict[str, Any]:
    dob_str = f"{day:02d}{month:02d}{year:04d}"
    digits = [int(d) for d in dob_str if d != '0']
    counts = {}
    for d in digits:
        counts[d] = counts.get(d, 0) + 1
        
    repeat_evaluations = []
    for num, count in sorted(counts.items()):
        p_info = PLANETARY_MATRIX.get(num, PLANETARY_MATRIX[1])
        if count == 1:
            eval_type = "Harmonious"
            description = f"Number {num} ({p_info['planet']}) appears once: balanced, clear expression of {p_info['nature']}."
        elif count == 2:
            eval_type = "Benefic Amplification"
            description = f"Number {num} ({p_info['planet']}) appears twice: strong creative and intuitive strength."
        elif count == 3:
            eval_type = "Intense / Dual Potential"
            description = f"Number {num} ({p_info['planet']}) appears 3 times: high energy requiring conscious grounding to avoid hyper-sensitivity."
        else:
            eval_type = "Malefic Over-Concentration"
            description = f"Number {num} ({p_info['planet']}) appears {count} times: heavy energy excess requiring elemental counter-balancing."
            
        repeat_evaluations.append({
            "number": num,
            "frequency": count,
            "planet": p_info["planet"],
            "type": eval_type,
            "analysis": description
        })
        
    return {
        "counts": counts,
        "evaluations": repeat_evaluations
    }

# ── 8. Missing Numbers in the Core Matrix & Practical Remedies ───────────────
def analyze_missing_numbers(day: int, month: int, year: int) -> List[Dict[str, Any]]:
    dob_str = f"{day:02d}{month:02d}{year:04d}"
    present = set(int(d) for d in dob_str if d != '0')
    missing = sorted(list(set(range(1, 10)) - present))
    
    missing_cards = []
    for m in missing:
        p_info = PLANETARY_MATRIX.get(m, PLANETARY_MATRIX[1])
        elem_remedy = ELEMENT_RULES.get(p_info["element"], {}).get("deficient_remedy", "")
        missing_cards.append({
            "number": m,
            "planet": p_info["planet"],
            "element": p_info["element"],
            "direction": p_info["direction"],
            "primary_color": p_info["color"],
            "remedy": f"Integrate {p_info['element']} element in the {p_info['direction']} sector. Use {p_info['color']} accessories and {elem_remedy}"
        })
    return missing_cards

# ── 9. Karmic & Master Numbers Assessment ─────────────────────────────────────
def assess_karmic_and_master(day: int, month: int, year: int, name: str = "") -> Dict[str, Any]:
    karmic_detected = []
    master_detected = []
    
    # Day check
    if day in KARMIC_DEBT_NUMBERS:
        karmic_detected.append({"source": "Birth Day", "number": day, "lesson": f"Karmic Debt Number {day}: requires disciplined patience and integrity in personal expression."})
    if day in MASTER_NUMBERS:
        master_detected.append({"source": "Birth Day", "number": day, "gift": f"Master Number {day}: elevated intuitive vision and leadership calling."})
        
    # Full Life Path check
    total_lp = sum(int(d) for d in f"{day:02d}{month:02d}{year:04d}")
    if total_lp in KARMIC_DEBT_NUMBERS:
        karmic_detected.append({"source": "Life Path Total", "number": total_lp, "lesson": f"Karmic Debt Number {total_lp}: transformation through conscious service."})
    if total_lp in MASTER_NUMBERS:
        master_detected.append({"source": "Life Path Total", "number": total_lp, "gift": f"Master Number {total_lp}: high vibration mission of societal inspiration."})
        
    # Name check
    if name:
        name_info = calculate_chaldean_name(name)
        if name_info["is_karmic"]:
            karmic_detected.append({"source": "Name Compound", "number": name_info["compound_sum"], "lesson": f"Karmic Name Compound {name_info['compound_sum']}: adjust spelling to reach an auspicious compound (such as 19, 23, 24, 27, 32, 37, 41, 45, 46)."})
        if name_info["is_master"]:
            master_detected.append({"source": "Name Vibration", "number": name_info["single_root"], "gift": f"Master Name Root {name_info['single_root']}: magnetic authority and far-reaching influence."})
            
    return {
        "has_karmic_debt": len(karmic_detected) > 0,
        "karmic_details": karmic_detected,
        "has_master_number": len(master_detected) > 0,
        "master_details": master_detected
    }

# ── 10. Planetary Friendship Taxonomy (Mitra, Sama, Shatru) ──────────────────
PLANETARY_FRIENDSHIP = {
    1: {  # Sun
        "planet": "Sun (Surya)",
        "friends": [1, 2, 3, 5, 9],
        "neutral": [4, 7],
        "enemies": [6, 8],
        "lucky_days": ["Sunday"],
        "lucky_colors": ["Gold", "Orange", "Copper", "Warm Yellow"],
        "avoid_colors": ["Black", "Dark Blue"],
        "gemstone": "Ruby or Sunstone in Copper/Gold",
        "vastu_direction": "East"
    },
    2: {  # Moon
        "planet": "Moon (Chandra)",
        "friends": [1, 2, 3, 5],
        "neutral": [6, 7],
        "enemies": [4, 8, 9],
        "lucky_days": ["Monday"],
        "lucky_colors": ["White", "Cream", "Silver", "Pearl"],
        "avoid_colors": ["Dark Red", "Jet Black"],
        "gemstone": "Natural Pearl or Moonstone in Silver",
        "vastu_direction": "North-West"
    },
    3: {  # Jupiter
        "planet": "Jupiter (Guru)",
        "friends": [1, 2, 3, 5, 7, 9],
        "neutral": [8],
        "enemies": [4, 6],
        "lucky_days": ["Thursday"],
        "lucky_colors": ["Bright Yellow", "Saffron", "Golden", "Amber"],
        "avoid_colors": ["Dark Blue", "Harsh Pink"],
        "gemstone": "Yellow Sapphire or Citrine in Brass/Gold",
        "vastu_direction": "North-East"
    },
    4: {  # Rahu
        "planet": "Rahu (North Node)",
        "friends": [1, 5, 6, 7, 8],
        "neutral": [3],
        "enemies": [2, 4, 9],
        "lucky_days": ["Wednesday", "Saturday"],
        "lucky_colors": ["Electric Blue", "Grey", "Khaki", "Silver"],
        "avoid_colors": ["Fiery Red", "Deep Crimson"],
        "gemstone": "Solid Silver Square or Hessonite (Gomed)",
        "vastu_direction": "South-West"
    },
    5: {  # Mercury
        "planet": "Mercury (Budha)",
        "friends": [1, 2, 3, 5, 6],
        "neutral": [4, 7, 8, 9],
        "enemies": [],  # Mercury has no natural enemies; friendly polymath
        "lucky_days": ["Wednesday"],
        "lucky_colors": ["Emerald Green", "Light Turquoise", "Mint Green"],
        "avoid_colors": ["Harsh Blood Red"],
        "gemstone": "Emerald or Green Aventurine in Silver/Gold",
        "vastu_direction": "North"
    },
    6: {  # Venus
        "planet": "Venus (Shukra)",
        "friends": [5, 6, 8],
        "neutral": [4, 7, 9],
        "enemies": [1, 2, 3],
        "lucky_days": ["Friday"],
        "lucky_colors": ["Diamond White", "Soft Pink", "Cream", "Pastel Blue"],
        "avoid_colors": ["Muddy Yellow", "Charcoal Black"],
        "gemstone": "Diamond, White Zircon, or Clear Quartz in Silver",
        "vastu_direction": "South-East"
    },
    7: {  # Ketu
        "planet": "Ketu (South Node)",
        "friends": [1, 3, 4, 5, 6],
        "neutral": [2, 9],
        "enemies": [8],
        "lucky_days": ["Thursday", "Tuesday"],
        "lucky_colors": ["Pastel Green", "Light Grey", "Smoky Lavender"],
        "avoid_colors": ["Jet Black", "Dark Brown"],
        "gemstone": "Cat's Eye (Lehsuniya) or Tiger's Eye in Silver",
        "vastu_direction": "North-East / Center"
    },
    8: {  # Saturn
        "planet": "Saturn (Shani)",
        "friends": [5, 6],
        "neutral": [3, 7],
        "enemies": [1, 2, 4, 8, 9],
        "lucky_days": ["Saturday"],
        "lucky_colors": ["Dark Navy Blue", "Charcoal", "Steel Grey"],
        "avoid_colors": ["Bright Crimson Red", "Pure Lemon Yellow"],
        "gemstone": "Blue Sapphire, Amethyst, or Iron Ring",
        "vastu_direction": "West"
    },
    9: {  # Mars
        "planet": "Mars (Mangal)",
        "friends": [1, 3, 5, 9],
        "neutral": [6, 7, 8],
        "enemies": [2, 4],
        "lucky_days": ["Tuesday"],
        "lucky_colors": ["Rose Coral", "Bright Scarlet", "Copper Orange"],
        "avoid_colors": ["Jet Black", "Dark Navy Blue"],
        "gemstone": "Red Coral or Carnelian in Copper/Silver",
        "vastu_direction": "South"
    }
}

# ── 11. Poorak Number (Complementary / Harmonizing Bridge Number) ─────────────
def calculate_poorak_number(driver: int, conductor: int, missing_numbers: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    Calculates the Poorak (पूरक अंक / Complementary & Harmonizing Number):
    1. If Driver and Conductor have friction, identifies the mutual peace-maker planet.
    2. If Driver and Conductor are friendly, identifies the prime missing number that completes the Lo Shu grid.
    3. Provides specific harmonizing actions and elemental bridging rituals.
    """
    d_friends = set(PLANETARY_FRIENDSHIP.get(driver, {}).get("friends", []))
    c_friends = set(PLANETARY_FRIENDSHIP.get(conductor, {}).get("friends", []))
    mutual_friends = list(d_friends.intersection(c_friends))
    
    d_enemies = set(PLANETARY_FRIENDSHIP.get(driver, {}).get("enemies", []))
    is_friction = conductor in d_enemies or driver in set(PLANETARY_FRIENDSHIP.get(conductor, {}).get("enemies", []))
    
    if is_friction:
        pair_set = {driver, conductor}
        if pair_set == {1, 8}:
            poorak = 5
            rationale = "Number 5 (Mercury) neutralizes intense Sun-Saturn friction by introducing analytical flexibility, diplomacy, and commercial balance."
        elif pair_set == {2, 8}:
            poorak = 5
            rationale = "Number 5 (Mercury) stabilizes Moon's emotional anxiety from Saturnian coldness through rational communication and commercial focus."
        elif pair_set == {3, 6}:
            poorak = 7
            rationale = "Number 7 (Ketu) reconciles spiritual Jupiter and material Venus by transmuting luxury into sacred philanthropy and high diagnostic insight."
        elif pair_set == {4, 9}:
            poorak = 6
            rationale = "Number 6 (Venus) cools down Rahu-Mars volatile combustion with diplomatic charm, aesthetic refinement, and graceful pacing."
        else:
            poorak = mutual_friends[0] if mutual_friends else 5
            rationale = f"Number {poorak} serves as the mutual friend reconciling the tension between Driver {driver} and Conductor {conductor}."
    else:
        if missing_numbers and 5 in missing_numbers:
            poorak = 5
            rationale = "Number 5 fills the central Earth anchor of your Lo Shu Grid, providing unshakable emotional stability and financial compounding."
        elif missing_numbers and 6 in missing_numbers:
            poorak = 6
            rationale = "Number 6 completes your luxury and supportive networks plane, attracting high-net-worth mentors and material comfort."
        elif mutual_friends:
            poorak = mutual_friends[0]
            rationale = f"Number {poorak} ({PLANETARY_MATRIX.get(poorak, {}).get('planet')}) acts as the supreme cosmic amplifier for your harmonious Driver-Conductor alliance."
        else:
            poorak = 5
            rationale = "Number 5 (Mercury) acts as the universal stabilizer for mental agility and trade prosperity."
            
    p_info = PLANETARY_MATRIX.get(poorak, PLANETARY_MATRIX[5])
    return {
        "poorak_number": poorak,
        "poorak_planet": p_info["planet"],
        "poorak_element": p_info["element"],
        "poorak_color": p_info["color"],
        "poorak_direction": p_info["direction"],
        "is_friction_resolution": is_friction,
        "rationale": rationale,
        "harmonizing_ritual": f"Incorporate {p_info['color'].split(',')[0]} accents and display a {p_info['element']} symbol in the {p_info['direction']} sector of your primary room."
    }

# ── 12. Speculative & Lottery Lucky Numbers Matrix ────────────────────────────
def calculate_speculative_lottery_numbers(
    driver: int, 
    conductor: int, 
    kua: Optional[int] = None, 
    missing_numbers: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    Generates high-resonance speculative, investment, and lottery numbers.
    CORE ESOTERIC LAW: Numbers that are NOT present in the Lo Shu Grid (missing numbers) 
    become the Lottery Numbers. In sacred numerology, numbers absent from the birth chart 
    represent unmanifested cosmic voids; activating them through speculative picks and 
    lottery tickets magnetically draws dormant wealth frequencies, unexpected windfalls, 
    and energetic equilibrium.
    """
    COMPOUND_SETS = {
        1: [10, 19, 23, 28, 37, 46, 55],
        2: [11, 20, 24, 29, 38, 47, 56],
        3: [12, 21, 27, 30, 39, 48, 57],
        4: [13, 22, 31, 37, 40, 49, 58],
        5: [14, 15, 23, 32, 41, 50, 59],
        6: [15, 24, 33, 42, 51, 60, 69],
        7: [16, 25, 34, 43, 52, 61, 70],
        8: [17, 26, 35, 44, 53, 62, 71],
        9: [18, 27, 36, 45, 54, 63, 72]
    }
    
    # Core Logic: Lottery Numbers are specifically the numbers NOT present in the Lo Shu Grid
    if missing_numbers is not None and len(missing_numbers) > 0:
        lottery_singles = sorted(list(set(missing_numbers)))
    else:
        # Fallback if grid has no missing numbers (rare full grid)
        d_friends = PLANETARY_FRIENDSHIP.get(driver, {}).get("friends", [1, 5])
        c_friends = PLANETARY_FRIENDSHIP.get(conductor, {}).get("friends", [1, 5])
        shared = [n for n in d_friends if n in c_friends]
        seed_nums = [driver, conductor] + ([kua] if isinstance(kua, int) and 1 <= kua <= 9 else [])
        lottery_singles = sorted(list(set(seed_nums + (shared[:2] if shared else [5]))))

    # Auspicious Compound Lottery Numbers corresponding to the missing/lottery numbers
    comp_pool = []
    for num in lottery_singles:
        comp_pool.extend(COMPOUND_SETS.get(num, [])[:2])
    if not comp_pool:
        comp_pool = [14, 15, 23, 24, 32, 33, 41, 42]
    auspicious_compounds = sorted(list(set(comp_pool)))

    # Fortunate calendar dates for speculative choices (dates reducing to lottery numbers)
    fortunate_dates = []
    for num in lottery_singles:
        for offset in [0, 9, 18]:
            d = num + offset
            if 1 <= d <= 31:
                fortunate_dates.append(d)
    fortunate_dates = sorted(list(set(fortunate_dates)))

    # Curated lottery ticket sets (3-digit, 4-digit, 5-digit combinations from missing numbers)
    speculative_combinations = []
    if len(lottery_singles) >= 3:
        speculative_combinations.append(lottery_singles[:3])
    if len(lottery_singles) >= 4:
        speculative_combinations.append(lottery_singles[:4])
    if len(lottery_singles) >= 5:
        speculative_combinations.append(lottery_singles[:5])
    if not speculative_combinations:
        speculative_combinations.append(lottery_singles)

    return {
        "lottery_numbers": lottery_singles,
        "lottery_single_digits": lottery_singles,
        "speculative_single_digits": lottery_singles,
        "missing_grid_numbers": lottery_singles,
        "primary_lucky_number": driver,
        "secondary_lucky_number": conductor,
        "directional_kua_lucky": kua,
        "auspicious_compound_lottery_numbers": auspicious_compounds,
        "fortunate_dates_of_month": fortunate_dates,
        "lottery_ticket_combinations": speculative_combinations,
        "lottery_rule": "The numbers NOT present in your Lo Shu Grid become your Lottery Numbers.",
        "guidance": "In sacred Lo Shu Grid numerology, numbers absent from your birth grid represent unmanifested cosmic voids. Selecting these missing numbers in speculative games, lotteries, and lucky picks activates dormant wealth frequencies and draws unexpected abundance."
    }

# ── 13. Vastu & Cosmic Prosperity Directional Synthesis ───────────────────────────
def synthesize_vastu_and_kua_directions(driver: int, conductor: int, kua_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Synthesizes the subject's 4 prosperous cosmic directions as per their chart reading
    with Driver and Conductor planetary Vastu orientations and Angelic resonance.
    """
    d_dir = PLANETARY_FRIENDSHIP.get(driver, {}).get("vastu_direction", "East")
    c_dir = PLANETARY_FRIENDSHIP.get(conductor, {}).get("vastu_direction", "North")
    
    wealth_dir = kua_profile.get("wealth_direction", "South-East (Prosperous Expansion Vector)")
    health_dir = kua_profile.get("health_direction", "East (Vitality & Healing Alignment)")
    rel_dir = kua_profile.get("relationship_direction", "South (Harmonious Union & Love Alignment)")
    clarity_dir = kua_profile.get("clarity_direction", "North (Inner Peace & Wisdom Sanctuary)")
    
    clean_w = wealth_dir.split('(')[0].strip()
    clean_h = health_dir.split('(')[0].strip()
    clean_r = rel_dir.split('(')[0].strip()
    clean_c = clarity_dir.split('(')[0].strip()
    
    angel_info = ANGEL_NUMBERS_BY_ROOT.get(driver, ANGEL_NUMBERS_BY_ROOT[1])

    return {
        "energy_orientation_group": kua_profile.get("energy_group", "East Group"),
        "kua_energy_group": kua_profile.get("energy_group", "East Group"),
        "angel_number_resonance": {
            "primary_angel_numbers": angel_info["angel_sequence"],
            "angelic_title": angel_info["title"],
            "guidance_message": angel_info["message"]
        },
        "wealth_and_career_apex": {
            "prosperous_direction": wealth_dir,
            "primary_sheng_chi": wealth_dir,  # Backward-compatibility alias
            "reinforcing_planetary_direction": d_dir,
            "action": f"Position your primary executive workspace facing {clean_w}. Display an energizing {PLANETARY_MATRIX.get(driver, {}).get('element')} symbol in the {d_dir} sector to activate prosperity and cash flow as per your chart reading."
        },
        "health_and_vitality_anchor": {
            "vitality_direction": health_dir,
            "primary_tien_yi": health_dir,  # Backward-compatibility alias
            "action": f"Align the headboard of your bed towards {clean_h} during sleep to accelerate cellular recovery, vitality, and mental serenity."
        },
        "relationship_and_family_harmony": {
            "harmony_direction": rel_dir,
            "primary_nien_yen": rel_dir,  # Backward-compatibility alias
            "action": f"Place joint family or partner symbols in the {clean_r} sector to protect domestic peace, emotional warmth, and mutual trust."
        },
        "mental_stability_and_focus": {
            "clarity_direction": clarity_dir,
            "primary_fu_wei": clarity_dir,  # Backward-compatibility alias
            "action": f"Meditate, read, or conduct strategic planning facing {clean_c} to maintain steady emotional equilibrium and clear decision-making."
        },
        "cosmic_and_angelic_guidance": (
            "As per your personal chart reading and angelic prosperity blueprint, aligning your workspace, "
            "meditation zone, and resting orientations with these natural electromagnetic vectors harmonizes "
            "your biological rhythm with celestial expansion and protective grace."
        )
    }


# ── 13B. Age Number Numerology (Input & Output Characteristics) ───────────────
def calculate_age_numerology(
    day: int,
    month: int,
    year: int,
    ref_date: Optional[datetime.date] = None,
    missing_numbers: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    Calculates completed age and compound/root age numerological characteristics:
    - Input Characteristics: Compound Age Number (active psychological and situational forces)
    - Output Characteristics: Reduced Root Age Number (karmic harvest and ruling planetary lesson)
    - Gap Analysis Finding: Interaction between the Age Root and natal Lo Shu missing numbers.
    """
    if ref_date is None:
        ref_date = datetime.date(2026, 10, 20)  # Standard platform reference date

    try:
        birth_date = datetime.date(year, month, day)
        age = ref_date.year - birth_date.year
        if (ref_date.month, ref_date.day) < (birth_date.month, birth_date.day):
            age -= 1
        if age < 0:
            age = 0
    except Exception:
        age = max(0, ref_date.year - year)

    running_year = age + 1
    compound_age = age
    digits = [int(d) for d in str(compound_age)] if compound_age > 0 else [0]
    sum_total = sum(digits)
    root_age = reduce_to_single_digit(sum_total) if sum_total > 0 else 1

    AGE_PLANETARY_RULERS = {
        1: {"planet": "Sun (Surya)", "archetype": "The Solar Pioneer"},
        2: {"planet": "Moon (Chandra)", "archetype": "The Lunar Harmonizer"},
        3: {"planet": "Jupiter (Guru)", "archetype": "The Wisdom Teacher"},
        4: {"planet": "Rahu (North Node)", "archetype": "The Master Architect"},
        5: {"planet": "Mercury (Budh)", "archetype": "The Velocity Pioneer"},
        6: {"planet": "Venus (Shukra)", "archetype": "The Harmonizer of Abundance"},
        7: {"planet": "Ketu (South Node)", "archetype": "The Spiritual Disciple"},
        8: {"planet": "Saturn (Shani)", "archetype": "The Karmic Sovereign"},
        9: {"planet": "Mars (Mangal)", "archetype": "The Courageous Champion"}
    }
    ruler_info = AGE_PLANETARY_RULERS.get(root_age, {"planet": "Universal Force", "archetype": "Awakening"})
    root_planet = ruler_info.get("planet", "Universal Force")

    # Classical Compound Age Profiles (Input Characteristics)
    COMPOUND_AGE_PROFILES = {
        18: "Compound 18 (Sun 1 + Saturn 8): Maturation trial. Transition from youthful impulse to structured independence.",
        21: "Compound 21 (Moon 2 + Sun 1): Crown of the Magi. Creative ambition, emotional clarity, and expanding personal influence.",
        28: "Compound 28 (Moon 2 + Saturn 8): Trust & responsibility trial. Navigating partnership friction and financial discipline.",
        32: "Compound 32 (Jupiter 3 + Moon 2): Communication magnetic gateway. Networking, mentorship, and commercial alignment.",
        33: "Compound 33 (Master Double 3): Sacred expression. Altruism, teaching, high-level creative synthesis.",
        35: "Compound 35 (Jupiter 3 + Mercury 5): Commercial velocity. Strategic business expansion, agility, and financial diversification.",
        36: "Compound 36 (Jupiter 3 + Venus 6): Harmonic abundance. Family joy, artistic fulfillment, and stabilized domestic luxury.",
        40: "Compound 40 (Rahu 4 + Void 0): Foundational reset. Eliminating obsolete patterns; restructuring life pillars.",
        41: "Compound 41 (Rahu 4 + Sun 1): Sovereign rebuilding. Asserting leadership authority through systematic innovation.",
        42: "Compound 42 (Rahu 4 + Moon 2): Emotional structural balance. Reconciling domestic security with career obligations.",
        43: "Compound 43 (Rahu 4 + Jupiter 3): Strategic wisdom. Turning hard-earned experience into institutional influence.",
        44: "Compound 44 (Master Double 4 Rahu): Master Material Architect. Demands unwavering discipline, methodical execution, and zero shortcuts. Eliminating speculative illusions to build enduring wealth and family security.",
        45: "Compound 45 (Rahu 4 + Mercury 5): Commercial breakthrough. Bridging structural stability with sudden market opportunities and travel.",
        46: "Compound 46 (Rahu 4 + Venus 6): Luxury & domestic fortification. Solidifying real estate, high-value investments, and marital harmony.",
        47: "Compound 47 (Rahu 4 + Ketu 7): Philosophical discernment. Balancing pragmatic worldly obligations with deeper spiritual self-inquiry.",
        48: "Compound 48 (Rahu 4 + Saturn 8): Karmic endurance pinnacle. Overcoming bureaucratic or structural hurdles through persistent integrity.",
        49: "Compound 49 (Rahu 4 + Mars 9): Dynamic completion. Decisive closure of an old 9-year paradigm; preparing for visionary rebirth.",
        50: "Compound 50 (Mercury 5 + Void 0): Jubilee freedom. Reclaiming autonomy, exploring new intellectual territory, and joyful adaptability.",
        51: "Compound 51 (Mercury 5 + Sun 1): Executive revitalization. High-level leadership, commercial visibility, and renewed vitality.",
        52: "Compound 52 (Mercury 5 + Moon 2): Intuitive negotiation. Enhancing public relationships and advisory roles.",
        53: "Compound 53 (Mercury 5 + Jupiter 3): Wealth counseling. Sharing financial acumen, writing, or higher advisory governance.",
        54: "Compound 54 (Mercury 5 + Rahu 4): Pragmatic enterprise. Expanding ventures with calculated foresight.",
        55: "Compound 55 (Double 5 Mercury): Velocity & transformation. Rapid technological, intellectual, or geographic adaptation.",
        60: "Compound 60 (Venus 6 + Void 0): Shashti Poorti milestone. Harmonious culmination of domestic dharma and gracious social standing."
    }

    input_desc = COMPOUND_AGE_PROFILES.get(
        compound_age,
        f"Compound Age {compound_age} combines the elemental vibrations of digits {', '.join(str(d) for d in digits)}. "
        f"It creates an active environment focused on balancing practical self-expression with evolving life responsibilities."
    )

    # Output Characteristics (Root Manifestation Lesson)
    OUTPUT_ROOT_PROFILES = {
        1: {
            "title": "Output Root 1 — The Solar Catalyst (Sun / Surya)",
            "archetype": "Sovereign Independence & New Beginnings",
            "manifestation": "This age phase culminates in bold initiative, decisive authority, and stepping into the forefront of your chosen field. Self-reliance and originality bring maximum harvest."
        },
        2: {
            "title": "Output Root 2 — The Lunar Harmonizer (Moon / Chandra)",
            "archetype": "Diplomacy, Patience & Receptivity",
            "manifestation": "This age phase resolves through cooperative partnerships, emotional maturation, and intuitive discernment. Strategic quietude outperforms aggressive forcing."
        },
        3: {
            "title": "Output Root 3 — The Jovian Sage (Jupiter / Guru)",
            "archetype": "Wisdom, Creative Expansion & Teaching",
            "manifestation": "This age phase culminates in intellectual expansion, teaching, advisory recognition, and benevolent fortune. Sharing knowledge multiplies success."
        },
        4: {
            "title": "Output Root 4 — The Rahu Architect (Rahu / North Node)",
            "archetype": "Methodical Systems & Solid Foundations",
            "manifestation": "This age phase culminates in lasting structural order, concrete systems, and enduring discipline. Consistency dissolves chaotic speculation."
        },
        5: {
            "title": "Output Root 5 — The Mercurial Pioneer (Mercury / Budh)",
            "archetype": "Commercial Agility, Freedom & Networking",
            "manifestation": "This age phase culminates in commercial adaptability, swift communication breakthroughs, and expansion through travel and modern technology."
        },
        6: {
            "title": "Output Root 6 — The Venusian Guardian (Venus / Shukra)",
            "archetype": "Family Duty, Luxury & Harmonic Prosperity",
            "manifestation": "This age phase culminates in marital stability, domestic beautification, artistic fulfillment, and graceful stewardship of family assets."
        },
        7: {
            "title": "Output Root 7 — The Ketu Mystic (Ketu / South Node)",
            "archetype": "Spiritual Discernment & Deep Specialization",
            "manifestation": "This age phase resolves through introspection, analytical mastery, and inner alignment. Surface attachments yield to profound spiritual peace."
        },
        8: {
            "title": "Output Root 8 — The Saturnian Sovereign (Saturn / Shani)",
            "archetype": "Executive Governance, Karmic Justice & Durable Wealth",
            "manifestation": "This age phase culminates in the karmic harvest of past perseverance. Saturn rewards unwavering integrity with enduring executive authority and financial compounding."
        },
        9: {
            "title": "Output Root 9 — The Martial Champion (Mars / Mangal)",
            "archetype": "Courageous Completion & Humanitarian Elevation",
            "manifestation": "This age phase culminates in courageously closing outdated karmic chapters, clearing long-standing debts, and asserting humanitarian leadership."
        }
    }

    out_info = OUTPUT_ROOT_PROFILES.get(root_age, OUTPUT_ROOT_PROFILES[1])

    # Gap Interaction Synthesis
    is_missing = (missing_numbers is not None and root_age in missing_numbers)
    if is_missing:
        gap_diagnosis = (
            f"KARMIC VOID ACTIVATION: Number {root_age} ({root_planet}) is missing in your natal Lo Shu Grid. "
            f"Navigating Age {compound_age} (which reduces to Root {root_age}) brings this unsealed energy center to the surface. "
            f"You will face acute lessons in {out_info['archetype'].lower()}. "
            f"Remedial harmonization via your personalized Lucky Charm is essential to prevent energetic leaks."
        )
        gap_status = "UNSEALED_KARMIC_GAP_ACTIVE"
    else:
        gap_diagnosis = (
            f"NATURAL HARMONIC RESONANCE: Number {root_age} ({root_planet}) is actively grounded in your natal matrix. "
            f"During Age {compound_age}, you naturally harness this frequency to achieve sustained compounding."
        )
        gap_status = "NATURALLY_SUPPORTED"

    return {
        "age_years": age,
        "running_year": running_year,
        "compound_age": compound_age,
        "sum_total": sum_total,
        "root_age": root_age,
        "root_planet": root_planet,
        "calculation_formula": f"{compound_age} ➔ {' + '.join(str(d) for d in digits)} = {sum_total}" + (f" ➔ {root_age}" if sum_total > 9 else ""),
        "input_characteristics": {
            "compound_age": compound_age,
            "title": f"Compound Age {compound_age} (Input Characteristics)",
            "description": input_desc
        },
        "output_characteristics": {
            "root_number": root_age,
            "title": out_info["title"],
            "archetype": out_info["archetype"],
            "manifestation": out_info["manifestation"]
        },
        "gap_analysis": {
            "is_missing_in_natal_grid": is_missing,
            "status": gap_status,
            "diagnosis": gap_diagnosis
        }
    }


# ── 14. Comprehensive Master Core Matrix Reading ──────────────────────────────
def generate_core_matrix_profile(
    name: str,
    day: int,
    month: int,
    year: int,
    mobile_number: str = "",
    current_age: Optional[int] = None,
    gender: Optional[str] = None
) -> Dict[str, Any]:
    """
    Unified Core Matrix Numerology generation.
    100% deterministic, free of astrological jargon, strictly grounded in Core Matrix Numerology.
    """
    driver = calculate_driver(day)
    conductor_details = calculate_conductor_details(day, month, year)
    conductor = conductor_details["conductor_raw"]
    conductor_root = conductor_details["conductor_root"]
    conductor_display = conductor_details["conductor_display"]
    kua_profile = get_kua_profile(year, gender)
    kua = kua_profile["kua_number"]
    name_calc = calculate_chaldean_name(name) if name else {"compound_sum": 0, "single_root": 0}
    
    try:
        age = int(current_age) if current_age and int(current_age) > 0 else (datetime.date.today().year - year)
    except (ValueError, TypeError):
        age = datetime.date.today().year - year
    dasha = calculate_dasha_cycles(day, month, year, age)
    elements = analyze_elements_balancing(day, month, year)
    repeats = analyze_repeat_numbers(day, month, year)
    missing = analyze_missing_numbers(day, month, year)
    karmic_master = assess_karmic_and_master(day, month, year, name)
    
    d_planet = PLANETARY_MATRIX.get(driver, PLANETARY_MATRIX[1])
    c_planet = PLANETARY_MATRIX.get(conductor if conductor <= 9 else (sum(int(d) for d in str(conductor)) % 9 or 9), PLANETARY_MATRIX[1])
    
    # Mobile audit
    mobile_audit = {}
    if mobile_number:
        clean_mob = [int(d) for d in mobile_number if d.isdigit()]
        mob_sum = reduce_to_single_digit(sum(clean_mob)) if clean_mob else 0
        malefic_pairs = []
        mob_str = "".join(str(d) for d in clean_mob)
        for pair in ["14", "41", "16", "61", "18", "81", "28", "82", "48", "84"]:
            if pair in mob_str:
                malefic_pairs.append(pair)
        mobile_audit = {
            "mobile_sum": mob_sum,
            "has_malefic_pairs": len(malefic_pairs) > 0,
            "detected_malefic_pairs": malefic_pairs,
            "status": "Requires Tuning" if len(malefic_pairs) > 0 else "Balanced"
        }

    missing_nums = [m["number"] for m in missing]
    poorak_info = calculate_poorak_number(driver, conductor, missing_nums)
    speculative_info = calculate_speculative_lottery_numbers(driver, conductor, kua, missing_numbers=missing_nums)
    vastu_synthesis = synthesize_vastu_and_kua_directions(driver, conductor, kua_profile)
    friendship_matrix = PLANETARY_FRIENDSHIP.get(driver, PLANETARY_FRIENDSHIP[1])
        
    return {
        "system": "Core Matrix Numerology",
        "user_name": name,
        "dob": f"{day:02d}/{month:02d}/{year}",
        "current_age": age,
        "core_numbers": {
            "driver_number": driver,
            "driver_planet": d_planet["planet"],
            "conductor_number": conductor,
            "conductor_root": conductor_root,
            "conductor_display": conductor_display,
            "conductor_planet": c_planet["planet"],
            "kua_number": kua,
            "kua_display": kua_profile.get("kua_display", KUA_NEEDS_GENDER_TEXT),
            "kua_rule_note": KUA_RULE_TEXT,
            "kua_profile": kua_profile,
            "name_number": name_calc.get("single_root"),
            "name_compound": name_calc.get("compound_sum")
        },
        "poorak_number_analysis": poorak_info,
        "speculative_and_lottery_numbers": speculative_info,
        "vastu_directional_synthesis": vastu_synthesis,
        "planetary_friendship_matrix": friendship_matrix,
        "dasha_cycles": dasha,
        "elements_balancing": elements,
        "repeat_numbers_analysis": repeats,
        "missing_numbers_remedies": missing,
        "karmic_and_master_numbers": karmic_master,
        "mobile_numerology": mobile_audit,
        "common_actionable_remedies": {
            "primary_gemstone": d_planet["nature"],
            "fortunate_colors": d_planet["color"],
            "fortunate_direction": d_planet["direction"],
            "daily_balancing_habits": f"Honor the {d_planet['element']} element in the {d_planet['direction']}. Wear {d_planet['color'].split(',')[0]} on high-stakes days."
        }
    }
