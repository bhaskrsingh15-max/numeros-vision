"""
NUMEROS VISION — WESTERN PYTHAGOREAN NUMEROLOGY ENGINE (METH-PYTH-001)
Implementation Specification | Version 1.0 (Section 3, 5, 6, 16)

Provides deterministic Western Pythagorean calculations:
- Letter Mapping: 1-9 Western table (A=1 ... Z=8)
- Life Path Calculation: 3-tier date reduction (Month, Day, Year) preserving Master Numbers (11, 22, 33)
- Birthday Number: Compound day preserved (1-31) and reduced root (1-9)
- Expression / Destiny Number: All name letters
- Soul Urge / Heart's Desire Number: Vowels (A, E, I, O, U)
- Personality Number: Consonants
- Karmic Debt Numbers: 13, 14, 16, 19 preserved and decoded
- Four Pinnacles & Three Period Cycles
- Method-isolated Western planetary associations (1-Sun, 2-Moon, 3-Jupiter, 4-Uranus, 5-Mercury, 6-Venus, 7-Neptune, 8-Saturn, 9-Mars)
"""

from typing import Dict, Any, List, Optional
import re
import uuid

# 1-9 Western Pythagorean alphabet values
PYTHAGOREAN_LETTER_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
    'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
}

VOWELS = {'A', 'E', 'I', 'O', 'U'}

WESTERN_PLANETARY_MAP = {
    1: {"planet": "Sun", "archetype": "The Leader / Pioneer", "element": "Fire"},
    2: {"planet": "Moon", "archetype": "The Peacemaker / Diplomat", "element": "Water"},
    3: {"planet": "Jupiter", "archetype": "The Creator / Expresser", "element": "Air/Fire"},
    4: {"planet": "Uranus", "archetype": "The Builder / Stabilizer", "element": "Earth"},
    5: {"planet": "Mercury", "archetype": "The Free Spirit / Communicator", "element": "Air"},
    6: {"planet": "Venus", "archetype": "The Nurturer / Caregiver", "element": "Earth/Air"},
    7: {"planet": "Neptune", "archetype": "The Seeker / Analyst", "element": "Water"},
    8: {"planet": "Saturn", "archetype": "The Powerhouse / Executive", "element": "Earth"},
    9: {"planet": "Mars", "archetype": "The Humanitarian / Finisher", "element": "Fire"},
    11: {"planet": "Neptune/Moon", "archetype": "Master Intuitive / Illuminator", "element": "Spiritual Light"},
    22: {"planet": "Uranus/Earth", "archetype": "Master Builder / Architect", "element": "Spiritual Form"},
    33: {"planet": "Venus/Jupiter", "archetype": "Master Teacher / Compassion", "element": "Spiritual Love"}
}

KARMIC_DEBT_MEANINGS = {
    13: {
        "karmic_debt": 13,
        "reduced_root": 4,
        "theme": "Karmic Debt 13/4: Focus, disciplined hard work, overcoming resistance to structure, avoiding shortcuts.",
        "tradition": "Western Pythagorean"
    },
    14: {
        "karmic_debt": 14,
        "reduced_root": 5,
        "theme": "Karmic Debt 14/5: Moderation in freedom, emotional discipline, constructive change without impulsivity.",
        "tradition": "Western Pythagorean"
    },
    16: {
        "karmic_debt": 16,
        "reduced_root": 7,
        "theme": "Karmic Debt 16/7: Spiritual re-evaluation, release of ego illusions, building on genuine internal truth.",
        "tradition": "Western Pythagorean"
    },
    19: {
        "karmic_debt": 19,
        "reduced_root": 1,
        "theme": "Karmic Debt 19/1: Self-reliance balanced with interdependence, leadership through listening and collaboration.",
        "tradition": "Western Pythagorean"
    }
}


def reduce_pythagorean(val: int, preserve_master: bool = True) -> int:
    """Reduces an integer to a single digit (1-9), preserving Master Numbers 11, 22, 33 if requested."""
    while val > 9:
        if preserve_master and val in (11, 22, 33):
            return val
        val = sum(int(d) for d in str(val))
    return val


def calculate_pythagorean_life_path(day: int, month: int, year: int) -> Dict[str, Any]:
    """
    Computes Life Path via standard 3-tier Western reduction:
    1. Reduce month (preserving 11, 22)
    2. Reduce day (preserving 11, 22)
    3. Reduce year (preserving 11, 22)
    4. Sum the three components and reduce, preserving 11, 22, 33.
    """
    r_month = reduce_pythagorean(month)
    r_day = reduce_pythagorean(day)
    r_year = reduce_pythagorean(year)

    intermediate_sum = r_month + r_day + r_year
    final_root = reduce_pythagorean(intermediate_sum, preserve_master=True)
    single_root = reduce_pythagorean(final_root, preserve_master=False)

    is_master = final_root in (11, 22, 33)
    is_karmic = intermediate_sum in KARMIC_DEBT_MEANINGS

    return {
        "original_date": f"{year:04d}-{month:02d}-{day:02d}",
        "month_reduction": r_month,
        "day_reduction": r_day,
        "year_reduction": r_year,
        "intermediate_sum": intermediate_sum,
        "compound_value": intermediate_sum,
        "final_life_path": final_root,
        "single_root": single_root,
        "is_master_number": is_master,
        "is_karmic_debt": is_karmic,
        "karmic_debt_detail": KARMIC_DEBT_MEANINGS.get(intermediate_sum),
        "planetary_association": WESTERN_PLANETARY_MAP.get(final_root, {}),
        "calculation_trace": f"({r_month}) + ({r_day}) + ({r_year}) = {intermediate_sum} -> {final_root}"
    }


def calculate_pythagorean_birthday(day: int) -> Dict[str, Any]:
    """
    Computes Birthday Number from the calendar day of birth.
    Preserves compound day (e.g. 14, 23, 28) and reduced root (1-9).
    """
    single = reduce_pythagorean(day, preserve_master=False)
    is_karmic = day in KARMIC_DEBT_MEANINGS
    return {
        "original_day": day,
        "compound_value": day,
        "reduced_root": single,
        "is_karmic_debt": is_karmic,
        "karmic_debt_detail": KARMIC_DEBT_MEANINGS.get(day),
        "planetary_association": WESTERN_PLANETARY_MAP.get(single, {}),
        "calculation_trace": f"Day {day} -> {single}"
    }


def calculate_pythagorean_name(name: str) -> Dict[str, Any]:
    """
    Calculates Expression, Soul Urge (vowels), and Personality (consonants) numbers.
    """
    clean_name = "".join(c.upper() for c in name if c.isalpha())
    if not clean_name:
        clean_name = "ANON"

    letter_breakdown = []
    total_sum = 0
    vowel_sum = 0
    consonant_sum = 0

    for char in clean_name:
        val = PYTHAGOREAN_LETTER_MAP.get(char, 0)
        is_vowel = char in VOWELS
        letter_breakdown.append({
            "letter": char,
            "value": val,
            "type": "vowel" if is_vowel else "consonant"
        })
        total_sum += val
        if is_vowel:
            vowel_sum += val
        else:
            consonant_sum += val

    expression_root = reduce_pythagorean(total_sum, preserve_master=True)
    soul_urge_root = reduce_pythagorean(vowel_sum, preserve_master=True)
    personality_root = reduce_pythagorean(consonant_sum, preserve_master=True)

    return {
        "full_name": name,
        "clean_name": clean_name,
        "letter_breakdown": letter_breakdown,
        "expression": {
            "compound_sum": total_sum,
            "reduced_root": expression_root,
            "single_root": reduce_pythagorean(expression_root, preserve_master=False),
            "is_master": expression_root in (11, 22, 33),
            "is_karmic": total_sum in KARMIC_DEBT_MEANINGS,
            "planetary_association": WESTERN_PLANETARY_MAP.get(expression_root, {})
        },
        "soul_urge": {
            "compound_sum": vowel_sum,
            "reduced_root": soul_urge_root,
            "single_root": reduce_pythagorean(soul_urge_root, preserve_master=False),
            "is_master": soul_urge_root in (11, 22, 33),
            "planetary_association": WESTERN_PLANETARY_MAP.get(soul_urge_root, {})
        },
        "personality": {
            "compound_sum": consonant_sum,
            "reduced_root": personality_root,
            "single_root": reduce_pythagorean(personality_root, preserve_master=False),
            "is_master": personality_root in (11, 22, 33),
            "planetary_association": WESTERN_PLANETARY_MAP.get(personality_root, {})
        }
    }


def calculate_pythagorean_pinnacles_and_cycles(day: int, month: int, year: int) -> Dict[str, Any]:
    """
    Computes the Four Pinnacles and Three Life Period Cycles.
    - Pinnacle 1 = reduce(month) + reduce(day)
    - Pinnacle 2 = reduce(day) + reduce(year)
    - Pinnacle 3 = reduce(P1 + P2)
    - Pinnacle 4 = reduce(month) + reduce(year)
    """
    r_m = reduce_pythagorean(month, preserve_master=False)
    r_d = reduce_pythagorean(day, preserve_master=False)
    r_y = reduce_pythagorean(year, preserve_master=False)

    p1 = reduce_pythagorean(r_m + r_d, preserve_master=True)
    p2 = reduce_pythagorean(r_d + r_y, preserve_master=True)
    p3 = reduce_pythagorean(p1 + p2, preserve_master=True)
    p4 = reduce_pythagorean(r_m + r_y, preserve_master=True)

    life_path_single = reduce_pythagorean(r_m + r_d + r_y, preserve_master=False)
    p1_end_age = 36 - life_path_single
    p2_end_age = p1_end_age + 9
    p3_end_age = p2_end_age + 9

    return {
        "pinnacles": {
            "first_pinnacle": {"number": p1, "age_range": f"0 to {p1_end_age}"},
            "second_pinnacle": {"number": p2, "age_range": f"{p1_end_age + 1} to {p2_end_age}"},
            "third_pinnacle": {"number": p3, "age_range": f"{p2_end_age + 1} to {p3_end_age}"},
            "fourth_pinnacle": {"number": p4, "age_range": f"{p3_end_age + 1}+"}
        },
        "period_cycles": {
            "first_cycle": {"number": r_m, "focus": "Youth & Formative Development (Month)"},
            "second_cycle": {"number": r_d, "focus": "Productive Mid-Life (Day)"},
            "third_cycle": {"number": r_y, "focus": "Culmination & Wisdom (Year)"}
        }
    }


def analyze_pythagorean_full(day: int, month: int, year: int, name: str = "") -> Dict[str, Any]:
    """
    Full Pythagorean Western numerological audit executing deterministically
    under methodology ID METH-PYTH-001.
    """
    lp = calculate_pythagorean_life_path(day, month, year)
    bd = calculate_pythagorean_birthday(day)
    nm = calculate_pythagorean_name(name) if name else None
    pc = calculate_pythagorean_pinnacles_and_cycles(day, month, year)

    trace_id = f"PYTH-TRC-{uuid.uuid4().hex[:8].upper()}"

    return {
        "methodology_id": "METH-PYTH-001",
        "methodology_name": "Western Pythagorean Numerology",
        "school": "Pythagorean Western Numerology",
        "version": "1.0.0",
        "calculation_trace_id": trace_id,
        "is_deterministic": True,
        "life_path": lp,
        "birthday_number": bd,
        "name_numerology": nm,
        "pinnacles_and_cycles": pc,
        "school_overlap_disclosure": "Pythagorean numerology uses the 1-9 alphabet mapping and month-day-year reduction. Overlap with Chaldean sound frequencies (1-8) is disclosed rather than treated as independent confirmation."
    }
