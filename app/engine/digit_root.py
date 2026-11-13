"""
app/engine/digit_root.py
========================
Single canonical digital-root reduction module for all Numeros Vision Python runtimes
(Core Matrix Engine, Charm AI, PDF Report Generator, Chaldean & Pythagorean Calculators).

Universal Rule (applies everywhere, zero exceptions):
    digit_root(n) = 1 + (n - 1) % 9   for n > 0
    digit_root(n) = 0                 for n <= 0

Master numbers (11, 22, 33) are NEVER preserved; every derived number (Driver/Mulank,
Bhagyank/Life Path, Name number, Personal Year, Personal Month, Personal Day, Pinnacle,
and cycle numbers) reduces strictly to a single digit 1..9.
"""

from datetime import date
from typing import Any, Dict, List, Optional, Tuple

PERSONAL_CYCLES_LABEL = "Personal Year / Month / Day"

PLANET_MAP_1_TO_9: Dict[int, Dict[str, str]] = {
    1: {"english": "Sun", "india": "Surya (Sun)", "international": "Sun (Surya)"},
    2: {"english": "Moon", "india": "Chandra (Moon)", "international": "Moon (Chandra)"},
    3: {"english": "Jupiter", "india": "Guru (Jupiter)", "international": "Jupiter (Guru)"},
    4: {"english": "Rahu", "india": "Rahu (North Node)", "international": "Rahu (North Node)"},
    5: {"english": "Mercury", "india": "Budh (Mercury)", "international": "Mercury (Budh)"},
    6: {"english": "Venus", "india": "Shukra (Venus)", "international": "Venus (Shukra)"},
    7: {"english": "Ketu", "india": "Ketu (South Node)", "international": "Ketu (South Node)"},
    8: {"english": "Saturn", "india": "Shani (Saturn)", "international": "Saturn (Shani)"},
    9: {"english": "Mars", "india": "Mangal (Mars)", "international": "Mars (Mangal)"},
}

LO_SHU_EIGHT_PLANES: List[Dict[str, Any]] = [
    {"id": "thought", "name": "Thought", "digits": [4, 3, 8]},
    {"id": "will", "name": "Will", "digits": [9, 5, 1]},
    {"id": "action", "name": "Action", "digits": [2, 7, 6]},
    {"id": "mental", "name": "Mental", "digits": [4, 9, 2]},
    {"id": "emotional", "name": "Emotional", "digits": [3, 5, 7]},
    {"id": "practical", "name": "Practical", "digits": [8, 1, 6]},
    {"id": "golden_raj_yoga", "name": "Golden Raj Yoga", "digits": [4, 5, 6]},
    {"id": "silver_raj_yoga", "name": "Silver Raj Yoga", "digits": [2, 5, 8]},
]

CHALDEAN_LETTER_VALUES: Dict[str, int] = {
    "A": 1, "I": 1, "J": 1, "Q": 1, "Y": 1,
    "B": 2, "C": 2, "K": 2, "R": 2,
    "G": 3, "L": 3, "S": 3,
    "D": 4, "M": 4, "T": 4,
    "E": 5, "H": 5, "N": 5, "X": 5,
    "U": 6, "V": 6, "W": 6,
    "O": 7, "Z": 7,
    "F": 8, "P": 8,
}

PYTHAGOREAN_LETTER_VALUES: Dict[str, int] = {
    "A": 1, "J": 1, "S": 1,
    "B": 2, "K": 2, "T": 2,
    "C": 3, "L": 3, "U": 3,
    "D": 4, "M": 4, "V": 4,
    "E": 5, "N": 5, "W": 5,
    "F": 6, "O": 6, "X": 6,
    "G": 7, "P": 7, "Y": 7,
    "H": 8, "Q": 8, "Z": 8,
    "I": 9, "R": 9,
}


def digit_root(n: int) -> int:
    """
    Canonical single-digit reduction:
        digit_root(n) = 1 + (n - 1) % 9   for n > 0
        digit_root(n) = 0                 for n <= 0
    Never preserves 11, 22, or 33.
    """
    val = int(n)
    return 1 + ((val - 1) % 9) if val > 0 else 0


def sum_digits_str(text: str) -> int:
    """Sums all ASCII decimal digits ('0'-'9') in `text`."""
    return sum(ord(ch) - 48 for ch in str(text) if "0" <= ch <= "9")


def calc_driver(day: int) -> int:
    """Driver / Mulank / Birth Day number (day of birth reduced strictly to 1..9)."""
    return digit_root(int(day))


def calc_bhagyank(day: int, month: int, year: int) -> int:
    """Bhagyank / Life Path number (all digits of full DDMMYYYY DOB reduced strictly to 1..9)."""
    dob_digits = f"{int(day):02d}{int(month):02d}{int(year):04d}"
    return digit_root(sum_digits_str(dob_digits))


def calc_personal_year(day: int, month: int, target_year: int) -> int:
    """
    Personal Year number:
        PY = digit_root(sum_digits(day) + sum_digits(month) + sum_digits(target_year))
    Strictly 1..9 (multiples of 9 return 9, never 0; 11/22/33 never retained).
    """
    py_digits = f"{int(day):02d}{int(month):02d}{int(target_year):04d}"
    return digit_root(sum_digits_str(py_digits))


def calc_personal_month(personal_year: int, calendar_month: int) -> int:
    """
    Personal Month number:
        PM = digit_root(PY + calendar_month)
    Strictly 1..9 (multiples of 9 return 9, never 0; 11/22/33 never retained).
    """
    return digit_root(int(personal_year) + int(calendar_month))


def calc_personal_day(
    personal_year: int,
    personal_month: int,
    target_day: int,
    target_month: int,
    target_year: int,
) -> int:
    """
    Personal Day number:
        PD = digit_root(PY_output + PM_output + sum_digits(DDMMYYYY_of_target_date))
    Strictly 1..9 (multiples of 9 return 9, never 0; 11/22/33 never retained).
    Verified reference points:
      - DOB 07-09-1980, 17/01/2026 -> PY 8, PM 9, date_digits 19 -> 8+9+19=36 -> PD 9
      - DOB 17-02-1963, 12/11/2026 -> PY 2, PM 4, date_digits 15 -> 2+4+15=21 -> PD 3
    """
    date_digits = f"{int(target_day):02d}{int(target_month):02d}{int(target_year):04d}"
    return digit_root(int(personal_year) + int(personal_month) + sum_digits_str(date_digits))


def calc_personal_cycles_for_date(
    birth_day: int,
    birth_month: int,
    target_dt: Optional[date] = None,
) -> Dict[str, Any]:
    """
    Canonical Personal Year / Month / Day bundle for any calendar date.
    Label is strictly 'Personal Year / Month / Day' (never called 'Dasha').
    """
    dt = target_dt or date.today()
    py = calc_personal_year(birth_day, birth_month, dt.year)
    pm = calc_personal_month(py, dt.month)
    pd = calc_personal_day(py, pm, dt.day, dt.month, dt.year)
    return {
        "label": PERSONAL_CYCLES_LABEL,
        "target_date": dt.isoformat(),
        "personal_year": py,
        "personal_month": pm,
        "personal_day": pd,
    }


def calc_compound_steps(raw_total: int) -> Dict[str, Any]:
    """
    Computes the step-by-step reduction chain as an informational note only
    (e.g. 29 -> '29, then 11, then 2'). Final value is strictly 1..9 (or 0 if <= 0).
    """
    val = int(raw_total)
    if val <= 0:
        return {"raw_sum": 0, "steps": [0], "final": 0, "note": None}
    steps: List[int] = [val]
    curr = val
    while curr > 9:
        curr = sum_digits_str(str(curr))
        steps.append(curr)
    note = ", then ".join(str(s) for s in steps) if len(steps) > 1 else None
    return {
        "raw_sum": val,
        "steps": steps,
        "final": steps[-1],
        "note": note,
    }


def calc_loshu_dob_only(day: int, month: int, year: int) -> Dict[str, Any]:
    """
    Canonical Lo Shu Grid from DOB digits ONLY (non-zero DDMMYYYY).
    Mulank (Driver), Bhagyank (Conductor), and Kua are NEVER added to the grid.
    """
    dob_str = f"{int(day):02d}{int(month):02d}{int(year):04d}"
    counts: Dict[int, int] = {d: 0 for d in range(1, 10)}
    for ch in dob_str:
        if "1" <= ch <= "9":
            counts[ord(ch) - 48] += 1

    present = [d for d in range(1, 10) if counts[d] > 0]
    missing = [d for d in range(1, 10) if counts[d] == 0]
    repeated = {d: counts[d] for d in range(1, 10) if counts[d] >= 2}

    planes: Dict[str, Dict[str, Any]] = {}
    for pl in LO_SHU_EIGHT_PLANES:
        present_in_plane = [d for d in pl["digits"] if counts[d] > 0]
        missing_in_plane = [d for d in pl["digits"] if counts[d] == 0]
        cnt_present = len(present_in_plane)
        planes[pl["id"]] = {
            "id": pl["id"],
            "name": pl["name"],
            "digits": list(pl["digits"]),
            "present_count": cnt_present,
            "fraction": f"{cnt_present}/3",
            "is_complete": cnt_present == 3,
            "present_digits": present_in_plane,
            "missing_digits": missing_in_plane,
        }

    return {
        "dob_digits_str": dob_str,
        "counts": counts,
        "present": present,
        "missing": missing,
        "repeated": repeated,
        "planes": planes,
    }


def calc_chaldean_name_number(name: str) -> Tuple[int, int]:
    """
    Returns (compound_sum, single_digit_root) using the canonical Chaldean table.
    When `name` contains at least one ASCII letter, `single_digit_root` is strictly 1..9.
    """
    clean = "".join(ch.upper() for ch in str(name or "") if "A" <= ch.upper() <= "Z")
    compound = sum(CHALDEAN_LETTER_VALUES.get(ch, 0) for ch in clean)
    return compound, digit_root(compound)


def calc_pythagorean_name_number(name: str) -> Tuple[int, int]:
    """
    Returns (compound_sum, single_digit_root) using the sequential 1..9 Pythagorean table.
    When `name` contains at least one ASCII letter, `single_digit_root` is strictly 1..9.
    """
    clean = "".join(ch.upper() for ch in str(name or "") if "A" <= ch.upper() <= "Z")
    compound = sum(PYTHAGOREAN_LETTER_VALUES.get(ch, 0) for ch in clean)
    return compound, digit_root(compound)
