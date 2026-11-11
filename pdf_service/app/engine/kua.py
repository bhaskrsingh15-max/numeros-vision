"""
NUMEROS VISION — CANONICAL KUA CALCULATION & DIRECTIONAL DERIVATION ENGINE
===========================================================================
Approved Formula (Deterministic Engine Authority):
1. Sum all four digits of the calendar birth year, reduce to a single digit = x.
   [Calendar birth year (1 Jan – 31 Dec) — CONFIRMED.]
2. Male: 11 - x, then reduce to a single digit.
   Female: 4 + x, then reduce to a single digit.
   Same rule across every century; zero pre/post-2000 branching.
3. Kua 5 maps to 2 for male and 8 for female [CONFIRMED].
4. Derive Element, Trigram, East/West Group, and Directional Sectors strictly
   from the final Kua number (never hardcode "Water · Kan (East Group)").
5. Missing or unrecognized gender returns status="NEEDS_GENDER" and
   display="Kua needs gender" — never guess or default to male/female.
"""

from typing import Any, Dict, Optional

KUA_RULE_TEXT = "Calculated from your birth year and gender"
KUA_NEEDS_GENDER_TEXT = "Kua needs gender"

KUA_METADATA: Dict[int, Dict[str, Any]] = {
    1: {
        "element": "Water",
        "trigram": "Kan",
        "group": "East Group",
        "group_short": "East",
        "element_group": "Water · Kan (East Group)",
        "element_group_clean": "Water · East Group",
        "desk_direction": "South-East",
        "success": "SE",
        "health": "E",
        "relationship": "S",
        "stability": "N",
        "avoid": ["W", "NW", "SW", "NE"],
        "wealth_direction": "South-East (Prosperous Expansion Vector)",
        "health_direction": "East (Vitality & Healing Alignment)",
        "relationship_direction": "South (Harmonious Union & Love Alignment)",
        "clarity_direction": "North (Inner Peace & Wisdom Sanctuary)",
        "energy_archetype": "Flowing Water & Intuitive Clarity",
        "traits": "Deep strategic intuition, fluid adaptability, communicative clarity, diplomacy.",
    },
    2: {
        "element": "Earth",
        "trigram": "Kun",
        "group": "West Group",
        "group_short": "West",
        "element_group": "Earth · Kun (West Group)",
        "element_group_clean": "Earth · West Group",
        "desk_direction": "North-East",
        "success": "NE",
        "health": "W",
        "relationship": "NW",
        "stability": "SW",
        "avoid": ["N", "S", "E", "SE"],
        "wealth_direction": "North-East (Prosperous Expansion Vector)",
        "health_direction": "West (Vitality & Healing Alignment)",
        "relationship_direction": "North-West (Harmonious Union & Love Alignment)",
        "clarity_direction": "South-West (Inner Peace & Wisdom Sanctuary)",
        "energy_archetype": "Nourishing Earth & Deep Grounding",
        "traits": "Steady patience, grounding real estate instincts, diplomatic endurance.",
    },
    3: {
        "element": "Wood",
        "trigram": "Zhen",
        "group": "East Group",
        "group_short": "East",
        "element_group": "Wood · Zhen (East Group)",
        "element_group_clean": "Wood · East Group",
        "desk_direction": "South",
        "success": "S",
        "health": "N",
        "relationship": "SE",
        "stability": "E",
        "avoid": ["W", "NW", "SW", "NE"],
        "wealth_direction": "South (Prosperous Expansion Vector)",
        "health_direction": "North (Vitality & Healing Alignment)",
        "relationship_direction": "South-East (Harmonious Union & Love Alignment)",
        "clarity_direction": "East (Inner Peace & Wisdom Sanctuary)",
        "energy_archetype": "Pioneering Wood & Radiant Growth",
        "traits": "Dynamic growth, pioneering courage, constructive ambition, expansive mentorship.",
    },
    4: {
        "element": "Wood",
        "trigram": "Xun",
        "group": "East Group",
        "group_short": "East",
        "element_group": "Wood · Xun (East Group)",
        "element_group_clean": "Wood · East Group",
        "desk_direction": "North",
        "success": "N",
        "health": "S",
        "relationship": "E",
        "stability": "SE",
        "avoid": ["W", "NW", "SW", "NE"],
        "wealth_direction": "North (Prosperous Expansion Vector)",
        "health_direction": "South (Vitality & Healing Alignment)",
        "relationship_direction": "East (Harmonious Union & Love Alignment)",
        "clarity_direction": "South-East (Inner Peace & Wisdom Sanctuary)",
        "energy_archetype": "Gentle Wood & Creative Inspiration",
        "traits": "Creative versatility, structured communication, networking, steady persistence.",
    },
    6: {
        "element": "Metal",
        "trigram": "Qian",
        "group": "West Group",
        "group_short": "West",
        "element_group": "Metal · Qian (West Group)",
        "element_group_clean": "Metal · West Group",
        "desk_direction": "West",
        "success": "W",
        "health": "NE",
        "relationship": "SW",
        "stability": "NW",
        "avoid": ["N", "S", "E", "SE"],
        "wealth_direction": "West (Prosperous Expansion Vector)",
        "health_direction": "North-East (Vitality & Healing Alignment)",
        "relationship_direction": "South-West (Harmonious Union & Love Alignment)",
        "clarity_direction": "North-West (Inner Peace & Wisdom Sanctuary)",
        "energy_archetype": "Radiant Metal & Executive Order",
        "traits": "Executive discipline, structured governance, high ethical standards, clear leadership.",
    },
    7: {
        "element": "Metal",
        "trigram": "Dui",
        "group": "West Group",
        "group_short": "West",
        "element_group": "Metal · Dui (West Group)",
        "element_group_clean": "Metal · West Group",
        "desk_direction": "North-West",
        "success": "NW",
        "health": "W",
        "relationship": "NE",
        "stability": "SW",
        "avoid": ["N", "S", "E", "SE"],
        "wealth_direction": "North-West (Prosperous Expansion Vector)",
        "health_direction": "West (Vitality & Healing Alignment)",
        "relationship_direction": "North-East (Harmonious Union & Love Alignment)",
        "clarity_direction": "South-West (Inner Peace & Wisdom Sanctuary)",
        "energy_archetype": "Refined Metal & Articulate Poise",
        "traits": "Articulate expression, persuasive communication, analytical refinement.",
    },
    8: {
        "element": "Earth",
        "trigram": "Gen",
        "group": "West Group",
        "group_short": "West",
        "element_group": "Earth · Gen (West Group)",
        "element_group_clean": "Earth · West Group",
        "desk_direction": "South-West",
        "success": "SW",
        "health": "NW",
        "relationship": "W",
        "stability": "NE",
        "avoid": ["N", "S", "E", "SE"],
        "wealth_direction": "South-West (Prosperous Expansion Vector)",
        "health_direction": "North-West (Vitality & Healing Alignment)",
        "relationship_direction": "West (Harmonious Union & Love Alignment)",
        "clarity_direction": "North-East (Inner Peace & Wisdom Sanctuary)",
        "energy_archetype": "Steadfast Mountain & Asset Stability",
        "traits": "Mountain-like stability, contemplative focus, steady long-horizon accumulation.",
    },
    9: {
        "element": "Fire",
        "trigram": "Li",
        "group": "East Group",
        "group_short": "East",
        "element_group": "Fire · Li (East Group)",
        "element_group_clean": "Fire · East Group",
        "desk_direction": "East",
        "success": "E",
        "health": "SE",
        "relationship": "N",
        "stability": "S",
        "avoid": ["W", "NW", "SW", "NE"],
        "wealth_direction": "East (Prosperous Expansion Vector)",
        "health_direction": "South-East (Vitality & Healing Alignment)",
        "relationship_direction": "North (Harmonious Union & Love Alignment)",
        "clarity_direction": "South (Inner Peace & Wisdom Sanctuary)",
        "energy_archetype": "Luminous Fire & Solar Illumination",
        "traits": "Clear visibility, expressive warmth, inspirational clarity, decisive momentum.",
    },
}


def _reduce_single_digit(n: int) -> int:
    n = abs(int(n))
    while n > 9:
        n = sum(int(ch) for ch in str(n))
    return n


def normalize_kua_gender(gender: Optional[str]) -> Optional[str]:
    """Returns 'male' or 'female' strictly; returns None for missing or ambiguous values."""
    if gender is None:
        return None
    cleaned = str(gender).strip().lower()
    if cleaned in ("male", "m"):
        return "male"
    if cleaned in ("female", "f"):
        return "female"
    return None


def calculate_kua_details(birth_year: int, gender: Optional[str] = None) -> Dict[str, Any]:
    """
    Canonical Kua calculation across all centuries:
      x = reduce_single_digit(sum of all 4 digits of calendar birth_year)
      male:   raw = reduce_single_digit(11 - x); if raw == 5 -> 2
      female: raw = reduce_single_digit(4 + x);  if raw == 5 -> 8
    If gender is missing/unrecognized, never guesses: returns status='NEEDS_GENDER'
    and display='Kua needs gender'.
    """
    if birth_year is None:
        raise ValueError("birth_year is required for Kua calculation")
    yr_int = int(birth_year)
    yr_digits = f"{yr_int:04d}"
    x = _reduce_single_digit(sum(int(ch) for ch in yr_digits if ch.isdigit()))

    norm_gender = normalize_kua_gender(gender)
    if norm_gender is None:
        return {
            "status": "NEEDS_GENDER",
            "kua_number": None,
            "raw_kua": None,
            "remapped_from_five": False,
            "year_digit_root": x,
            "gender": None,
            "display": KUA_NEEDS_GENDER_TEXT,
            "element": None,
            "trigram": None,
            "group": None,
            "group_short": None,
            "element_group": KUA_NEEDS_GENDER_TEXT,
            "element_group_clean": KUA_NEEDS_GENDER_TEXT,
            "desk_direction": KUA_NEEDS_GENDER_TEXT,
            "rule_note": KUA_RULE_TEXT,
            "five_mapping_status": "CONFIRMED_2_MALE_8_FEMALE",
            "year_boundary_status": "CALENDAR_YEAR_CONFIRMED",
        }

    if norm_gender == "male":
        raw_kua = _reduce_single_digit(11 - x)
        final_kua = 2 if raw_kua == 5 else raw_kua
    else:
        raw_kua = _reduce_single_digit(4 + x)
        final_kua = 8 if raw_kua == 5 else raw_kua

    meta = KUA_METADATA[final_kua]
    return {
        "status": "OK",
        "kua_number": final_kua,
        "raw_kua": raw_kua,
        "remapped_from_five": (raw_kua == 5),
        "year_digit_root": x,
        "gender": norm_gender,
        "display": str(final_kua),
        "element": meta["element"],
        "trigram": meta["trigram"],
        "group": meta["group"],
        "group_short": meta["group_short"],
        "element_group": meta["element_group"],
        "element_group_clean": meta["element_group_clean"],
        "desk_direction": meta["desk_direction"],
        "success": meta["success"],
        "health": meta["health"],
        "relationship": meta["relationship"],
        "stability": meta["stability"],
        "avoid": list(meta["avoid"]),
        "wealth_direction": meta["wealth_direction"],
        "health_direction": meta["health_direction"],
        "relationship_direction": meta["relationship_direction"],
        "clarity_direction": meta["clarity_direction"],
        "energy_archetype": meta["energy_archetype"],
        "traits": meta["traits"],
        "rule_note": KUA_RULE_TEXT,
        "five_mapping_status": "CONFIRMED_2_MALE_8_FEMALE",
        "year_boundary_status": "CALENDAR_YEAR_CONFIRMED",
    }


def calculate_kua_number(year: int, gender: Optional[str] = None) -> Optional[int]:
    """Returns integer Kua in {1,2,3,4,6,7,8,9}, or None when gender is missing."""
    return calculate_kua_details(year, gender)["kua_number"]
