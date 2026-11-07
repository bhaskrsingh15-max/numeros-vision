"""
2027 YEAR AHEAD PLANNER ENGINE
Numeros Vision · ANVEIL EVERY CHARM
Master Deterministic Engine for the 2027 Annual Blueprint.

Strict Results-Only Architecture:
- Zero calculation formulas, reduction chains, or weight workings exposed.
- Deterministic calculation: identical name + DOB yields identical results.
- Fully compatible with Python server and report generation pipelines.
"""

import json
import os
import re
import datetime
from typing import Dict, Any, List, Optional, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# 1. PLANETARY MAPPINGS & TRADITIONAL RELATIONSHIPS
# ─────────────────────────────────────────────────────────────────────────────

PLANET_ARCHETYPES = {
    1: {"number": 1, "english": "Sun", "vedic": "Surya", "element": "Water"},
    2: {"number": 2, "english": "Moon", "vedic": "Chandra", "element": "Earth"},
    3: {"number": 3, "english": "Jupiter", "vedic": "Guru (Brihaspati)", "element": "Wood"},
    4: {"number": 4, "english": "Rahu", "vedic": "Rahu (North Node)", "element": "Wood"},
    5: {"number": 5, "english": "Mercury", "vedic": "Budh", "element": "Earth"},
    6: {"number": 6, "english": "Venus", "vedic": "Shukra", "element": "Metal"},
    7: {"number": 7, "english": "Ketu", "vedic": "Ketu (South Node)", "element": "Metal"},
    8: {"number": 8, "english": "Saturn", "vedic": "Shani", "element": "Earth"},
    9: {"number": 9, "english": "Mars", "vedic": "Mangal", "element": "Fire"}
}

# Classical planetary friendship matrix
RELATIONSHIPS = {
    1: {"friends": [1, 2, 3, 5, 9], "neutral": [4, 7], "challenging": [6, 8]},
    2: {"friends": [1, 2, 3, 5], "neutral": [6, 7], "challenging": [4, 8, 9]},
    3: {"friends": [1, 2, 3, 5, 7, 9], "neutral": [8], "challenging": [4, 6]},
    4: {"friends": [1, 5, 6, 7, 8], "neutral": [3], "challenging": [2, 4, 9]},
    5: {"friends": [1, 2, 3, 5, 6], "neutral": [4, 7, 8, 9], "challenging": []},
    6: {"friends": [5, 6, 8], "neutral": [4, 7, 9], "challenging": [1, 2, 3]},
    7: {"friends": [1, 3, 4, 5, 6], "neutral": [2, 9], "challenging": [8]},
    8: {"friends": [5, 6], "neutral": [3, 7], "challenging": [1, 2, 4, 8, 9]},
    9: {"friends": [1, 3, 5, 9], "neutral": [6, 7, 8], "challenging": [2, 4]}
}

# Chaldean letter values
CHALDEAN_MAP = {
    'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 8, 'G': 3, 'H': 5, 'I': 1,
    'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 7, 'P': 8, 'Q': 1, 'R': 2,
    'S': 3, 'T': 4, 'U': 6, 'V': 6, 'W': 6, 'X': 5, 'Y': 1, 'Z': 7
}

# Traditional Crystal Suggestions for Mulank (Driver)
CRYSTAL_SUGGESTIONS = {
    1: "Sunstone or Carnelian",
    2: "Moonstone",
    3: "Citrine",
    4: "Hessonite garnet",
    5: "Green aventurine",
    6: "Clear quartz",
    7: "Tiger's eye",
    8: "Amethyst or Lapis lazuli",
    9: "Red jasper"
}

# Personal Month Ratings per design specification
PERSONAL_MONTH_RATINGS = {
    1: "Favourable",
    2: "Neutral",
    3: "Favourable",
    4: "Neutral",
    5: "Asks for care",
    6: "Favourable",
    7: "Neutral",
    8: "Neutral",
    9: "Asks for care"
}

PERSONAL_MONTH_THEMES = {
    1: "New Beginnings & Fresh Initiatives",
    2: "Collaboration, Tact & Receptivity",
    3: "Creative Expression & Social Connection",
    4: "Order, Discipline & Grounded Foundations",
    5: "Adaptability, Movement & Restructuring",
    6: "Home Harmony, Responsibility & Care",
    7: "Introspection, Review & Quiet Focus",
    8: "Practical Execution, Resource & Balance",
    9: "Completion, Clearance & Transition"
}

WEEKDAY_RULERS = {
    0: 2,  # Monday -> Moon (2)
    1: 9,  # Tuesday -> Mars (9)
    2: 5,  # Wednesday -> Mercury (5)
    3: 3,  # Thursday -> Jupiter (3)
    4: 6,  # Friday -> Venus (6)
    5: 8,  # Saturday -> Saturn (8)
    6: 1   # Sunday -> Sun (1)
}

WEEKDAY_NAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

# Fixed 12 Plain-Language Date Notes (No numbers, no formulas, zero predictions)
DATE_NOTES_LIBRARY = {
    "Peak": [
        "A strong day to plan important conversations or new starts.",
        "An auspicious window for meaningful decisions and steady alignment.",
        "A clear, constructive day to advance personal and professional priorities."
    ],
    "Favourable": [
        "A good day for steady progress and focused collaboration.",
        "A supportive atmosphere for organization, research, and practical steps.",
        "A productive rhythm well suited for productive conversations."
    ],
    "Steady": [
        "A balanced day suited for routine workflows and quiet maintenance.",
        "A neutral day ideal for steady follow-through and patience.",
        "A grounded day to observe trends and organize ongoing commitments."
    ],
    "Care": [
        "A day for a lighter schedule and thoughtful pacing.",
        "A reflective day best reserved for rest, review, and low-friction tasks.",
        "A day to pause, avoid hasty commitments, and cultivate composure."
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. CORE MATHEMATICAL HELPERS (INTERNAL ONLY)
# ─────────────────────────────────────────────────────────────────────────────

def _reduce_to_single_digit(num: int) -> int:
    """Deterministically reduce an integer to a single digit 1..9."""
    while num > 9:
        num = sum(int(ch) for ch in str(num))
    return num

def _get_chaldean_name_number(name: str) -> Tuple[int, int]:
    """Calculate Chaldean compound and root number."""
    clean = re.sub(r'[^A-Za-z]', '', name).upper()
    compound = sum(CHALDEAN_MAP.get(ch, 0) for ch in clean)
    root = _reduce_to_single_digit(compound)
    return compound, root

def _get_sun_sign(month: int, day: int) -> str:
    """Determine Tropical sun sign from month and day."""
    if (month == 3 and day >= 21) or (month == 4 and day <= 19):
        return "Aries"
    elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
        return "Taurus"
    elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
        return "Gemini"
    elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
        return "Cancer"
    elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
        return "Leo"
    elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
        return "Virgo"
    elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
        return "Libra"
    elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
        return "Scorpio"
    elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
        return "Sagittarius"
    elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
        return "Capricorn"
    elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
        return "Aquarius"
    else:
        return "Pisces"

def _evaluate_relationship(n1: int, n2: int) -> str:
    """Return friendly, neutral, or challenging relationship label."""
    if n2 in RELATIONSHIPS[n1]["friends"]:
        return "Friendly"
    elif n2 in RELATIONSHIPS[n1]["challenging"]:
        return "Challenging"
    return "Neutral"

# ─────────────────────────────────────────────────────────────────────────────
# 3. PINNACLES CALCULATION
# ─────────────────────────────────────────────────────────────────────────────

def calculate_pinnacles(day: int, month: int, year: int, bhagyank: int, target_year: int = 2027) -> Dict[str, Any]:
    """
    Calculate the 4 Life Pinnacles and their age spans.
    P1 = month + day (reduced)
    P2 = day + year (reduced)
    P3 = P1 + P2 (reduced)
    P4 = month + year (reduced)
    
    Age boundaries:
    - P1 ends at age 36 - bhagyank
    - P2 runs 9 years
    - P3 runs 9 years
    - P4 continues indefinitely
    """
    d_red = _reduce_to_single_digit(day)
    m_red = _reduce_to_single_digit(month)
    y_red = _reduce_to_single_digit(year)

    p1_val = _reduce_to_single_digit(m_red + d_red)
    p2_val = _reduce_to_single_digit(d_red + y_red)
    p3_val = _reduce_to_single_digit(p1_val + p2_val)
    p4_val = _reduce_to_single_digit(m_red + y_red)

    p1_end = 36 - bhagyank
    p2_start = p1_end
    p2_end = p2_start + 9
    p3_start = p2_end
    p3_end = p3_start + 9
    p4_start = p3_end

    age_in_target_year = target_year - year

    # Determine current and next pinnacle
    if age_in_target_year < p1_end:
        current_p = 1
        next_p = 2
    elif age_in_target_year < p2_end:
        current_p = 2
        next_p = 3
    elif age_in_target_year < p3_end:
        current_p = 3
        next_p = 4
    else:
        current_p = 4
        next_p = None

    pinnacles_list = [
        {
            "pinnacle_id": "P1",
            "number": p1_val,
            "governing_planet": PLANET_ARCHETYPES[p1_val]["english"],
            "age_span": f"Birth to age {p1_end}",
            "is_current": (current_p == 1),
            "is_next": (next_p == 1)
        },
        {
            "pinnacle_id": "P2",
            "number": p2_val,
            "governing_planet": PLANET_ARCHETYPES[p2_val]["english"],
            "age_span": f"Age {p2_start} to {p2_end}",
            "is_current": (current_p == 2),
            "is_next": (next_p == 2)
        },
        {
            "pinnacle_id": "P3",
            "number": p3_val,
            "governing_planet": PLANET_ARCHETYPES[p3_val]["english"],
            "age_span": f"Age {p3_start} to {p3_end}",
            "is_current": (current_p == 3),
            "is_next": (next_p == 3)
        },
        {
            "pinnacle_id": "P4",
            "number": p4_val,
            "governing_planet": PLANET_ARCHETYPES[p4_val]["english"],
            "age_span": f"Age {p4_start} onwards",
            "is_current": (current_p == 4),
            "is_next": (next_p == 4)
        }
    ]

    return {
        "pinnacles": pinnacles_list,
        "current_pinnacle": f"P{current_p}",
        "next_pinnacle": f"P{next_p}" if next_p else "P4 (Culmination)",
        "age_in_2027": age_in_target_year
    }

# ─────────────────────────────────────────────────────────────────────────────
# 4. 365-DAY ALIGNMENT ENGINE (RESULTS ONLY)
# ─────────────────────────────────────────────────────────────────────────────

def _calculate_day_alignment(
    date_obj: datetime.date,
    mulank: int,
    bhagyank: int,
    personal_year: int,
    personal_month: int,
    panchang_day: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Compute daily Alignment Score (0-100) and assign Tier & plain-language note.
    Zero calculation steps are returned in the output.
    """
    day_num = date_obj.day
    month_num = date_obj.month
    year_num = date_obj.year
    weekday_idx = date_obj.weekday()

    d_red = _reduce_to_single_digit(day_num)
    universal_day = _reduce_to_single_digit(day_num + month_num + year_num)
    personal_day = _reduce_to_single_digit(personal_month + day_num)
    weekday_ruler = WEEKDAY_RULERS[weekday_idx]

    # Deterministic multi-factor resonance scoring (internal only)
    base_score = 50.0

    # Factor 1: Personal Day resonance with Mulank & Bhagyank
    if personal_day in RELATIONSHIPS[mulank]["friends"]:
        base_score += 12.0
    elif personal_day in RELATIONSHIPS[mulank]["challenging"]:
        base_score -= 10.0

    if personal_day in RELATIONSHIPS[bhagyank]["friends"]:
        base_score += 10.0
    elif personal_day in RELATIONSHIPS[bhagyank]["challenging"]:
        base_score -= 8.0

    # Factor 2: Universal Day resonance with Personal Year
    if universal_day in RELATIONSHIPS[personal_year]["friends"]:
        base_score += 8.0
    elif universal_day in RELATIONSHIPS[personal_year]["challenging"]:
        base_score -= 6.0

    # Factor 3: Weekday ruler harmonic match with Mulank
    if weekday_ruler in RELATIONSHIPS[mulank]["friends"]:
        base_score += 8.0
    elif weekday_ruler in RELATIONSHIPS[mulank]["challenging"]:
        base_score -= 6.0

    # Factor 4: Day digit self-harmony
    if d_red == mulank or d_red == bhagyank:
        base_score += 6.0

    # Factor 5: Panchang adjustments if available
    is_amavasya = False
    if panchang_day:
        if panchang_day.get("is_amavasya") or panchang_day.get("tithi_number") == 30:
            base_score -= 12.0
            is_amavasya = True
        elif panchang_day.get("is_purnima") or panchang_day.get("tithi_number") == 15:
            base_score += 4.0

    # Clamp score between 28 and 96
    score = int(max(28, min(96, round(base_score))))

    # Tier assignment
    if score >= 82:
        tier = "Peak"
    elif score >= 68:
        tier = "Favourable"
    elif score >= 54:
        tier = "Steady"
    elif score >= 44:
        tier = "Mixed"
    else:
        tier = "Care"

    # Select note deterministically based on date and tier
    note_candidates = DATE_NOTES_LIBRARY.get(tier, DATE_NOTES_LIBRARY["Steady"])
    note_idx = (date_obj.day + date_obj.month * 3) % len(note_candidates)
    note = note_candidates[note_idx]

    return {
        "date": date_obj.strftime("%Y-%m-%d"),
        "weekday": WEEKDAY_NAMES[weekday_idx],
        "alignment_score": score,
        "tier": tier,
        "note": note,
        "is_amavasya": is_amavasya,
        "is_peak": (tier == "Peak")
    }

# ─────────────────────────────────────────────────────────────────────────────
# 5. MASTER CALCULATION ENTRYPOINT
# ─────────────────────────────────────────────────────────────────────────────

def calculate_planner_2027(
    full_name: str,
    dob_str: str,
    birth_name: Optional[str] = None,
    city: str = "New Delhi",
    panchang_data_path: str = "data/panchang_2027_delhi.json"
) -> Dict[str, Any]:
    """
    Main deterministic calculation engine for 2027 Year Ahead Planner.
    Generates all 10 report sections in strict Results-Only format.
    """
    # 1. Validation
    if not full_name or len(full_name.strip()) < 2 or len(full_name.strip()) > 60:
        raise ValueError("Full name must be between 2 and 60 characters.")
    clean_name_check = full_name.replace(' ', '')
    if not clean_name_check.isalpha():
        raise ValueError("Full name must contain letters and spaces only.")

    try:
        dob = datetime.date.fromisoformat(dob_str)
    except Exception:
        raise ValueError("DOB must be in valid YYYY-MM-DD format.")

    if dob.year < 1900 or dob > datetime.date.today():
        raise ValueError("DOB year must be >= 1900 and not in the future.")

    # 2. Driver (Mulank) and Conductor (Bhagyank)
    mulank = _reduce_to_single_digit(dob.day)
    bhagyank = _reduce_to_single_digit(dob.day + dob.month + dob.year)

    # 3. Personal Year 2027
    # 2027 -> 2+0+2+7 = 11 -> 2
    personal_year_2027 = _reduce_to_single_digit(_reduce_to_single_digit(dob.day) + _reduce_to_single_digit(dob.month) + 2)

    # 4. Universal Year 2027
    universal_year_2027 = {
        "value": 2,
        "master_flag": 11,
        "display": "2 (Master Vibration 11/2)",
        "theme": "Cooperation, Intuitive Diplomacy & Collective Calibration"
    }

    # 5. Planets and Drivers
    driver_planet = PLANET_ARCHETYPES[mulank]
    conductor_planet = PLANET_ARCHETYPES[bhagyank]
    driver_conductor_relation = _evaluate_relationship(mulank, bhagyank)

    # Friendly & Challenging numbers
    friendly_nums = sorted(list(set(RELATIONSHIPS[mulank]["friends"]).intersection(RELATIONSHIPS[bhagyank]["friends"])))
    if not friendly_nums:
        friendly_nums = sorted(list(set(RELATIONSHIPS[mulank]["friends"])))
    challenging_nums = sorted(list(set(RELATIONSHIPS[mulank]["challenging"]).union(RELATIONSHIPS[bhagyank]["challenging"])))

    # 6. Sun Sign
    sun_sign = _get_sun_sign(dob.month, dob.day)

    # 7. Lo Shu Grid plotting
    dob_digits = [int(c) for c in dob_str if c.isdigit() and c != '0']
    lo_shu_layout = [
        {"digit": 4, "count": dob_digits.count(4), "is_personal_year": (personal_year_2027 == 4)},
        {"digit": 9, "count": dob_digits.count(9), "is_personal_year": (personal_year_2027 == 9)},
        {"digit": 2, "count": dob_digits.count(2), "is_personal_year": (personal_year_2027 == 2)},
        {"digit": 3, "count": dob_digits.count(3), "is_personal_year": (personal_year_2027 == 3)},
        {"digit": 5, "count": dob_digits.count(5), "is_personal_year": (personal_year_2027 == 5)},
        {"digit": 7, "count": dob_digits.count(7), "is_personal_year": (personal_year_2027 == 7)},
        {"digit": 8, "count": dob_digits.count(8), "is_personal_year": (personal_year_2027 == 8)},
        {"digit": 1, "count": dob_digits.count(1), "is_personal_year": (personal_year_2027 == 1)},
        {"digit": 6, "count": dob_digits.count(6), "is_personal_year": (personal_year_2027 == 6)}
    ]
    present_numbers = [item["digit"] for item in lo_shu_layout if item["count"] > 0]
    missing_numbers = [item["digit"] for item in lo_shu_layout if item["count"] == 0]

    # 8. Name Numbers (Chaldean)
    full_compound, full_root = _get_chaldean_name_number(full_name)
    name_data = {
        "full_name": full_name.strip(),
        "name_number_compound": full_compound,
        "name_number_root": full_root,
        "alignment_with_numbers": _evaluate_relationship(full_root, mulank)
    }
    if birth_name and birth_name.strip() and birth_name.strip().lower() != full_name.strip().lower():
        b_compound, b_root = _get_chaldean_name_number(birth_name)
        name_data["birth_name"] = birth_name.strip()
        name_data["birth_name_compound"] = b_compound
        name_data["birth_name_root"] = b_root

    # 9. Pinnacles
    pinnacles_data = calculate_pinnacles(dob.day, dob.month, dob.year, bhagyank, target_year=2027)

    # 10. Load Panchang data if available
    panchang_days = {}
    if os.path.exists(panchang_data_path):
        try:
            with open(panchang_data_path, "r", encoding="utf-8") as pf:
                p_json = json.load(pf)
                panchang_days = p_json.get("days", {})
        except Exception:
            pass

    # 11. Twelve Months & Daily Calendar Calculations
    months_data = []
    full_calendar_365 = []
    all_key_dates_by_month = {}

    start_date = datetime.date(2027, 1, 1)
    end_date = datetime.date(2027, 12, 31)
    cur = start_date

    month_days_map = {m: [] for m in range(1, 13)}

    while cur <= end_date:
        d_iso = cur.strftime("%Y-%m-%d")
        m_num = cur.month
        p_month_num = _reduce_to_single_digit(personal_year_2027 + m_num)
        p_day_info = panchang_days.get(d_iso)

        day_result = _calculate_day_alignment(
            cur, mulank, bhagyank, personal_year_2027, p_month_num, p_day_info
        )
        # Results-only: keep strictly clean fields
        day_record = {
            "date": day_result["date"],
            "weekday": day_result["weekday"],
            "alignment_score": day_result["alignment_score"],
            "tier": day_result["tier"]
        }
        full_calendar_365.append(day_record)

        # Extended record for month compilation
        extended_day = {
            **day_result,
            "panchang": p_day_info
        }
        month_days_map[m_num].append(extended_day)
        cur += datetime.timedelta(days=1)

    # Compile 12 Month Blueprints
    for m in range(1, 13):
        m_name = MONTH_NAMES[m]
        p_month_num = _reduce_to_single_digit(personal_year_2027 + m)
        rating = PERSONAL_MONTH_RATINGS[p_month_num]
        theme = PERSONAL_MONTH_THEMES[p_month_num]

        days_in_m = month_days_map[m]
        avg_score = round(sum(d["alignment_score"] for d in days_in_m) / len(days_in_m), 1)

        # Sort for best 5 dates
        sorted_best = sorted(days_in_m, key=lambda x: (-x["alignment_score"], x["date"]))
        best_5 = [
            {
                "date": d["date"],
                "weekday": d["weekday"],
                "alignment_score": d["alignment_score"],
                "tier": d["tier"],
                "note": d["note"]
            }
            for d in sorted_best[:5]
        ]

        # Sort for 5 care dates
        sorted_care = sorted(days_in_m, key=lambda x: (x["alignment_score"], x["date"]))
        care_5 = [
            {
                "date": d["date"],
                "weekday": d["weekday"],
                "alignment_score": d["alignment_score"],
                "tier": d["tier"],
                "note": d["note"]
            }
            for d in sorted_care[:5]
        ]

        # Full and New Moons in this month
        fm_dates = []
        nm_dates = []
        for d in days_in_m:
            p = d.get("panchang")
            if p:
                if p.get("is_purnima"):
                    fm_dates.append(d["date"])
                if p.get("is_amavasya"):
                    nm_dates.append(d["date"])

        # Key Auspicious Dates (Section G):
        # Peak-tier days from day engine + auspicious tithis, dropping Amavasya and morning Rahu Kaal
        key_dates_month = []
        for d in days_in_m:
            p = d.get("panchang")
            if d["is_peak"]:
                # Exclusion rule: drop Amavasya
                if d["is_amavasya"]:
                    continue
                # Exclusion rule: drop days where Rahu Kaal covers working morning
                if p and p.get("rahu_kaal", {}).get("is_morning", False):
                    # Check if Rahu Kaal start is between 10:00 and 12:00
                    r_start = p.get("rahu_kaal", {}).get("start", "")
                    if r_start and ("10:" in r_start or "11:" in r_start or "09:" in r_start):
                        # Flagged / dropped per exclusion standard
                        continue
                key_dates_month.append({
                    "date": d["date"],
                    "weekday": d["weekday"],
                    "alignment_score": d["alignment_score"],
                    "tier": d["tier"],
                    "note": d["note"]
                })
                if len(key_dates_month) >= 5:
                    break

        months_data.append({
            "month_number": m,
            "month_name": m_name,
            "personal_month_number": p_month_num,
            "theme": theme,
            "rating": rating,
            "month_average_score": avg_score,
            "best_five_dates": best_5,
            "five_care_dates": care_5,
            "full_moon_dates": fm_dates,
            "new_moon_dates": nm_dates,
            "key_dates": key_dates_month
        })

    # 12. Traditional Crystal Suggestion
    crystal_suggestion = {
        "mulank": mulank,
        "crystal": CRYSTAL_SUGGESTIONS[mulank],
        "disclaimer": "Traditional suggestion for personal equilibrium. Not financial, medical, or curative advice."
    }

    return {
        "subject": {
            "full_name": full_name.strip(),
            "dob": dob_str,
            "city": city,
            "sun_sign": sun_sign
        },
        "numbers": {
            "mulank": mulank,
            "bhagyank": bhagyank,
            "personal_year_2027": personal_year_2027,
            "universal_year_2027": universal_year_2027,
            "driver_planet": driver_planet,
            "conductor_planet": conductor_planet,
            "driver_conductor_relation": driver_conductor_relation,
            "friendly_numbers": friendly_nums,
            "challenging_numbers": challenging_nums
        },
        "lo_shu_grid": {
            "layout": lo_shu_layout,
            "present_numbers": present_numbers,
            "missing_numbers": missing_numbers,
            "marked_personal_year": personal_year_2027
        },
        "name_analysis": name_data,
        "pinnacles": pinnacles_data,
        "months": months_data,
        "crystal_suggestion": crystal_suggestion,
        "calendar_365": full_calendar_365
    }

if __name__ == "__main__":
    print("Testing Planner 2027 Engine...")
    sample = calculate_planner_2027("ARUN SHARMA", "1981-11-28")
    print(f"Subject: {sample['subject']['full_name']}, DOB: {sample['subject']['dob']}")
    print(f"Mulank: {sample['numbers']['mulank']}, Bhagyank: {sample['numbers']['bhagyank']}")
    print(f"Personal Year 2027: {sample['numbers']['personal_year_2027']}")
    print(f"Driver/Conductor Relation: {sample['numbers']['driver_conductor_relation']}")
    print(f"Pinnacles: Current: {sample['pinnacles']['current_pinnacle']}, Next: {sample['pinnacles']['next_pinnacle']}")
    for p in sample['pinnacles']['pinnacles']:
        print(f"  {p['pinnacle_id']}: Number {p['number']} ({p['age_span']})")
    print(f"Jan Month Rating: {sample['months'][0]['rating']}, Theme: {sample['months'][0]['theme']}")
    print(f"Crystal: {sample['crystal_suggestion']['crystal']}")
    print(f"Total calendar days: {len(sample['calendar_365'])}")
