"""
2027 YEAR AHEAD PLANNER ENGINE
Numeros Vision · ANVEIL EVERY CHARM
Master Deterministic Engine for the 2027 Annual Blueprint.

Authoritative Rules Enforced:
- 100% Deterministic Day-Scoring via Authoritative Reference Engine (ref_engine.py).
- Symmetric 81-pair planetary compatibility grid.
- Python banker's rounding (roundHalfEven) for all deterministic daily scores.
- Strict Results-Only architecture (no reduction formulas, weights, or workings exposed).
- Age spans and exact pinnacle boundary transitions detected within 2027.
- Master vibration 11 flagged for Personal Month (e.g. June for Personal Year 5).
"""

import os
import json
import datetime
import collections
import itertools
from typing import Dict, Any, List, Optional, Tuple

# ─────────────────────────────────────────────────────────────────────────────
# 1. PLANETARY ARCHETYPES & AUTHORITATIVE REFERENCE MATRIX (ref_engine.py)
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

# Authoritative 81-Pair Grid from ref_engine.py
# row = number a, column = number b (1..9); symmetric; conditional pairs scored N
GRID = {
    1: ['F',  'F+', 'F+', 'F',  'F+', 'F+', 'F',  'E+', 'F+'],
    2: ['F+', 'F',  'F',  'E+', 'F+', 'N',  'N',  'E+', 'E+'],
    3: ['F+', 'F',  'F',  'N',  'F+', 'E+', 'N',  'F',  'N'],
    4: ['F',  'E+', 'N',  'N',  'F',  'F+', 'F+', 'N',  'E+'],
    5: ['F+', 'F+', 'F+', 'F',  'F',  'F+', 'F',  'F',  'F'],
    6: ['F+', 'N',  'E+', 'F+', 'F+', 'F',  'F+', 'N',  'N'],
    7: ['F',  'N',  'N',  'F+', 'F',  'F+', 'N',  'N',  'N'],
    8: ['E+', 'E+', 'F',  'N',  'F',  'N',  'N',  'N',  'N'],
    9: ['F+', 'E+', 'N',  'E+', 'F',  'N',  'N',  'N',  'N']
}

SC = {'F+': 2, 'F': 1, 'N': 0, 'E': -1, 'E+': -2}
rel = lambda a, b: SC[GRID[a][b - 1]]
ds = lambda n: sum(map(int, str(n)))

def red(n: int) -> int:
    while n > 9:
        n = ds(n)
    return n

CH = dict(zip("ABCDEFGHIJKLMNOPQRSTUVWXYZ", [1, 2, 3, 4, 5, 8, 3, 5, 1, 1, 2, 3, 4, 5, 7, 8, 1, 2, 3, 4, 6, 6, 6, 5, 1, 7]))
WD = {0: 2, 1: 9, 2: 5, 3: 3, 4: 6, 5: 8, 6: 1}  # Mon..Sun -> ruler number
W = dict(DT=15, DN=15, WD=15, PD=20, PM=10, PY=5, UD=10, UM=10, IH=10)
RW = {k: W[k] for k in ('DT', 'DN', 'WD', 'PD', 'UD', 'UM', 'PM')}
RTOT = sum(RW.values())
WSUM = sum(W.values())
UY = red(ds(2027))  # universal year 2027 -> 2

def person(dob: Tuple[int, int, int], name: str) -> Dict[str, Any]:
    d, m, y = dob
    mul = red(d)
    bha = red(ds(d) + ds(m) + ds(y))
    py = red(ds(d) + ds(m) + ds(2027))
    grid = {int(c) for c in f"{d:02d}{m:02d}{y}" if c != '0'} | {mul, bha}
    letters = {CH[c] for c in name.upper() if c in CH}
    nt = red(sum(CH[c] for c in name.upper() if c in CH))
    return dict(mul=mul, bha=bha, py=py, grid=grid, name=letters | {nt})

def avail(p: Dict[str, Any], x: int) -> float:
    return 1.0 if x in p['grid'] else 0.75 if x in p['name'] else 0.5

def comp_v(p: Dict[str, Any], x: int) -> float:
    rD = 2 if x == p['mul'] else rel(x, p['mul'])
    rC = 2 if x == p['bha'] else rel(x, p['bha'])
    v = (rD + rC) / 2.0
    if v > 0 and x not in (p['mul'], p['bha']):
        v *= avail(p, x)
    return v

def pair_s(a: int, b: int) -> Tuple[float, bool]:
    s = 2.0 if a == b else float(rel(a, b))
    opp = (a != b and a + b == 10)
    if opp:
        s = max(-2.0, s - 0.5)
    return s, opp

def score_day(p: Dict[str, Any], date: datetime.date) -> Dict[str, Any]:
    m, d = date.month, date.day
    pm = red(p['py'] + m)
    pd = red(pm + d)
    um = red(UY + m)
    ud = red(um + d)
    dn = red(d)
    mn = red(m)
    yn = red(ds(2027))
    dt = red(ds(d) + ds(m) + ds(2027))
    wd = WD[date.weekday()]
    nums = dict(DT=dt, DN=dn, WD=wd, PD=pd, PM=pm, PY=p['py'], UD=ud, UM=um)
    H = sum(pair_s(a, b)[0] for a, b in itertools.combinations([dn, mn, yn], 2)) / 3.0
    base = (sum(W[k] * (comp_v(p, x) + 2) / 4.0 for k, x in nums.items()) + W['IH'] * (H + 2) / 4.0) * 100.0 / WSUM
    own = (p['mul'], p['bha'])
    M = sum(RW[k] for k in RW if nums[k] in own) / float(RTOT)
    cnt = collections.Counter(nums[k] for k in RW)
    n, k = max(cnt.items(), key=lambda kv: (kv[1], 1 if kv[0] in own else 0, rel(kv[0], p['mul']) + rel(kv[0], p['bha'])))
    adj = 0
    if k >= 3:
        r = (rel(n, p['mul']) + rel(n, p['bha'])) / 2.0
        if n in own:
            adj = min(15, 5 * (k - 2))
        elif r > 0:
            adj = min(6, 2 * (k - 2))
        elif r < 0:
            adj = -min(15, 5 * (k - 2))
    # Python round() uses banker's rounding (round half to even)
    final_score = max(0, min(100, round(base + 20 * M + adj)))
    return dict(date=date, score=final_score, nums=nums, k=k, rep=n, inputs=[dn, mn, yn])

def year(p: Dict[str, Any]) -> List[Dict[str, Any]]:
    s = datetime.date(2027, 1, 1)
    out = []
    while s.year == 2027:
        out.append(score_day(p, s))
        s += datetime.timedelta(days=1)
    return out

def tiers(ys: List[Dict[str, Any]]) -> Tuple[int, int, int, int]:
    s = sorted(x['score'] for x in ys)
    cut = lambda f: s[int(f * len(s)) - 1]
    return cut(.95), cut(.85), cut(.5), cut(.15)  # Peak>=P95, Excellent>=P85, Good>=P50, Moderate>=P15, else Care

def classify_tier(score: int, p95: int, p85: int, p50: int, p15: int) -> str:
    if score >= p95:
        return "Peak"
    if score >= p85:
        return "Excellent"
    if score >= p50:
        return "Good"
    if score >= p15:
        return "Moderate"
    return "Care"

def lookup_relation(a: int, b: int) -> str:
    code = GRID[a][b - 1]
    if code in ('F+', 'F'):
        return "Friendly"
    if code in ('E', 'E+'):
        return "Challenging"
    return "Neutral"

def get_number_compatibility_lists(num: int) -> Dict[str, List[int]]:
    friendly = []
    neutral = []
    challenging = []
    for b in range(1, 10):
        if b == num:
            continue
        code = GRID[num][b - 1]
        if code in ('F+', 'F'):
            friendly.append(b)
        elif code == 'N':
            neutral.append(b)
        elif code in ('E', 'E+'):
            challenging.append(b)
    return {
        "friendly": friendly,
        "neutral": neutral,
        "challenging": challenging
    }

# ─────────────────────────────────────────────────────────────────────────────
# 2. METADATA, THEMES & NOTE LIBRARIES (RESULTS ONLY)
# ─────────────────────────────────────────────────────────────────────────────

WEEKDAY_NAMES = [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
]

WEEKDAY_SHORT = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

MONTH_NAMES = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

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

DATE_NOTES_LIBRARY = {
    "Peak": [
        "A strong day to plan important conversations or new starts.",
        "An auspicious window for meaningful decisions and steady alignment.",
        "A clear, constructive day to advance personal and professional priorities."
    ],
    "Excellent": [
        "A good day for steady progress and focused collaboration.",
        "A supportive atmosphere for organization, research, and practical steps.",
        "A productive rhythm well suited for productive conversations."
    ],
    "Good": [
        "A balanced day suited for routine workflows and quiet maintenance.",
        "A neutral day ideal for steady follow-through and patience.",
        "A grounded day to observe trends and organize ongoing commitments."
    ],
    "Moderate": [
        "A day for steady pacing, routine administration, and measured focus.",
        "A balanced day best reserved for thoughtful follow-up and review.",
        "A steady day suited for organizing existing work without rushing."
    ],
    "Care": [
        "A day for a lighter schedule and thoughtful pacing.",
        "A reflective day best reserved for rest, review, and low-friction tasks.",
        "A day to pause, avoid hasty commitments, and cultivate composure."
    ]
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. PINNACLES & LIFE CYCLES
# ─────────────────────────────────────────────────────────────────────────────

def calculate_pinnacles(dob: datetime.date, bhagyank: int, target_year: int = 2027) -> Dict[str, Any]:
    day = dob.day
    month = dob.month
    year_num = dob.year

    d_red = red(day)
    m_red = red(month)
    y_red = red(year_num)

    p1_val = red(m_red + d_red)
    p2_val = red(d_red + y_red)
    p3_val = red(p1_val + p2_val)
    p4_val = red(m_red + y_red)

    p1_end = 36 - bhagyank
    p2_start = p1_end
    p2_end = p2_start + 9
    p3_start = p2_end
    p3_end = p3_start + 9
    p4_start = p3_end

    age_jan_1 = target_year - year_num - (1 if (month, day) > (1, 1) else 0)
    age_dec_31 = target_year - year_num

    age_span_str = f"age {age_jan_1} to {age_dec_31}" if age_jan_1 != age_dec_31 else f"age {age_jan_1}"

    def pinnacle_for_age(a: int) -> int:
        if a < p1_end:
            return 1
        elif a < p2_end:
            return 2
        elif a < p3_end:
            return 3
        else:
            return 4

    p_start = pinnacle_for_age(age_jan_1)
    p_end = pinnacle_for_age(age_dec_31)

    boundary_crosses = (p_start != p_end)
    boundary_info = None

    if boundary_crosses:
        change_date_str = f"{target_year}-{month:02d}-{day:02d}"
        boundary_info = {
            "crosses_in_2027": True,
            "date_of_change": change_date_str,
            "transition": f"P{p_start} to P{p_end}",
            "previous_pinnacle": f"P{p_start}",
            "new_pinnacle": f"P{p_end}",
            "description": f"Transitions from Pinnacle P{p_start} to P{p_end} on {change_date_str}"
        }

    pinnacles_list = [
        {
            "pinnacle_id": "P1",
            "number": p1_val,
            "governing_planet": PLANET_ARCHETYPES[p1_val]["english"],
            "age_span": f"Birth to age {p1_end}",
            "is_current": (p_start == 1 or p_end == 1),
            "is_active_start": (p_start == 1),
            "is_active_end": (p_end == 1)
        },
        {
            "pinnacle_id": "P2",
            "number": p2_val,
            "governing_planet": PLANET_ARCHETYPES[p2_val]["english"],
            "age_span": f"Age {p2_start} to {p2_end}",
            "is_current": (p_start == 2 or p_end == 2),
            "is_active_start": (p_start == 2),
            "is_active_end": (p_end == 2)
        },
        {
            "pinnacle_id": "P3",
            "number": p3_val,
            "governing_planet": PLANET_ARCHETYPES[p3_val]["english"],
            "age_span": f"Age {p3_start} to {p3_end}",
            "is_current": (p_start == 3 or p_end == 3),
            "is_active_start": (p_start == 3),
            "is_active_end": (p_end == 3)
        },
        {
            "pinnacle_id": "P4",
            "number": p4_val,
            "governing_planet": PLANET_ARCHETYPES[p4_val]["english"],
            "age_span": f"Age {p4_start} onwards",
            "is_current": (p_start == 4 or p_end == 4),
            "is_active_start": (p_start == 4),
            "is_active_end": (p_end == 4)
        }
    ]

    spans = [
        [0, p1_end],
        [p2_start, p2_end],
        [p3_start, p3_end],
        [p4_start, None]
    ]

    return {
        "pinnacles": pinnacles_list,
        "spans": spans,
        "values": {"P1": p1_val, "P2": p2_val, "P3": p3_val, "P4": p4_val},
        "current_pinnacle": f"P{p_start}",
        "next_pinnacle": f"P{p_end}" if boundary_crosses else (f"P{p_start + 1}" if p_start < 4 else "P4 (Culmination)"),
        "age_on_jan_1": age_jan_1,
        "age_on_dec_31": age_dec_31,
        "age_span_in_2027": age_span_str,
        "boundary_transition": boundary_info
    }

# ─────────────────────────────────────────────────────────────────────────────
# 4. MASTER CALCULATION ENTRYPOINT (RESULTS ONLY)
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
    Generates all report sections in strict Results-Only format.
    """
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

    # 1. Evaluate person via authoritative reference implementation
    dob_tuple = (dob.day, dob.month, dob.year)
    p = person(dob_tuple, full_name)
    mulank = p['mul']
    bhagyank = p['bha']
    personal_year_2027 = p['py']

    # 2. Compatibility Lists & Relationship
    driver_lists = get_number_compatibility_lists(mulank)
    conductor_lists = get_number_compatibility_lists(bhagyank)
    relation = lookup_relation(mulank, bhagyank)

    # 3. Universal Year 2027
    universal_year_2027 = {
        "value": 2,
        "master_flag": 11,
        "display": "2 (Master Vibration 11/2)",
        "theme": "Cooperation, Intuitive Diplomacy & Collective Calibration"
    }

    # 4. Planetary Archetypes
    driver_planet = PLANET_ARCHETYPES[mulank]
    conductor_planet = PLANET_ARCHETYPES[bhagyank]

    # 5. Lo Shu Grid Present and Missing digits + Counts per digit
    dob_str_clean = f"{dob.day:02d}{dob.month:02d}{dob.year}"
    dob_digit_counts = {digit: dob_str_clean.count(str(digit)) for digit in range(1, 10)}
    grid_digits = [int(c) for c in dob_str_clean if c != '0'] + [mulank, bhagyank]
    lo_shu_counts = {digit: grid_digits.count(digit) for digit in range(1, 10)}
    lo_shu_present = sorted(list(p['grid']))
    lo_shu_missing = [d for d in range(1, 10) if d not in p['grid']]

    # 6. Name Numbers
    name_numbers = sorted(list(p['name']))
    full_compound = sum(CH[c] for c in full_name.upper() if c in CH)
    full_root = red(full_compound)

    name_data = {
        "full_name": full_name.strip(),
        "name_number_compound": full_compound,
        "name_number_root": full_root,
        "name_numbers": name_numbers,
        "alignment_with_driver": lookup_relation(full_root, mulank),
        "alignment_with_conductor": lookup_relation(full_root, bhagyank)
    }

    if birth_name and birth_name.strip() and birth_name.strip().lower() != full_name.strip().lower():
        b_p = person(dob_tuple, birth_name)
        b_compound = sum(CH[c] for c in birth_name.upper() if c in CH)
        b_root = red(b_compound)
        name_data["birth_name"] = birth_name.strip()
        name_data["birth_name_compound"] = b_compound
        name_data["birth_name_root"] = b_root
        name_data["birth_name_numbers"] = sorted(list(b_p['name']))
        name_data["birth_name_alignment_with_driver"] = lookup_relation(b_root, mulank)

    # 7. Pinnacles
    pinnacles_data = calculate_pinnacles(dob, bhagyank, target_year=2027)

    # 8. 365 Days Scoring via ref_engine
    ys = year(p)
    p95, p85, p50, p15 = tiers(ys)
    cutoffs = {"P95": p95, "P85": p85, "P50": p50, "P15": p15}

    # Load Panchang data
    panchang_days = {}
    if os.path.exists(panchang_data_path):
        try:
            with open(panchang_data_path, "r", encoding="utf-8") as pf:
                p_json = json.load(pf)
                panchang_days = p_json.get("days", {})
        except Exception:
            pass

    full_calendar_365 = []
    month_days_map = {m: [] for m in range(1, 13)}
    tier_counts = {"Care": 0, "Moderate": 0, "Good": 0, "Excellent": 0, "Peak": 0}

    for d_obj in ys:
        date_curr = d_obj['date']
        score = d_obj['score']
        d_iso = date_curr.strftime("%Y-%m-%d")
        w_idx = date_curr.weekday()
        m_num = date_curr.month
        t_tier = classify_tier(score, p95, p85, p50, p15)
        tier_counts[t_tier] += 1

        notes_candidates = DATE_NOTES_LIBRARY[t_tier]
        note = notes_candidates[(date_curr.day + date_curr.month * 3) % len(notes_candidates)]

        p_day_info = panchang_days.get(d_iso, {})

        day_entry = {
            "date": d_iso,
            "weekday": WEEKDAY_SHORT[w_idx],
            "alignment_score": score,
            "tier": t_tier,
            "note": note,
            "panchang": p_day_info
        }

        full_calendar_365.append(day_entry)
        month_days_map[m_num].append(day_entry)

    # 9. Compile Month Blueprints
    months_data = []
    for m in range(1, 13):
        m_name = MONTH_NAMES[m]
        raw_pm = personal_year_2027 + m
        p_month_num = red(raw_pm)
        is_master_11 = (raw_pm == 11)

        rating = PERSONAL_MONTH_RATINGS[p_month_num]
        theme = PERSONAL_MONTH_THEMES[p_month_num]
        pm_display = "2 (Master Vibration 11/2)" if is_master_11 else str(p_month_num)

        days_in_m = month_days_map[m]
        avg_score = round(sum(d["alignment_score"] for d in days_in_m) / len(days_in_m), 1)

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

        months_data.append({
            "month_number": m,
            "month_name": m_name,
            "personal_month": p_month_num,
            "personal_month_display": pm_display,
            "is_master_11": is_master_11,
            "rating": rating,
            "theme": theme,
            "average_alignment_score": avg_score,
            "best_5_dates": best_5,
            "care_5_dates": care_5,
            "remedies": {
                "color_guidance": f"Harmonic tones for month {m}",
                "phonetic_vibration": f"Vibration attunement {p_month_num}"
            }
        })

    all_scores = [d['score'] for d in ys]

    return {
        "subject": {
            "full_name": full_name.strip(),
            "dob": dob_str,
            "city": city,
            "driver_mulank": mulank,
            "conductor_bhagyank": bhagyank,
            "driver_planet": driver_planet,
            "conductor_planet": conductor_planet,
            "driver_conductor_relation": relation,
            "driver_lists": driver_lists,
            "conductor_lists": conductor_lists,
            "personal_year_2027": personal_year_2027,
            "universal_year_2027": universal_year_2027,
            "lo_shu_present": lo_shu_present,
            "lo_shu_missing": lo_shu_missing,
            "lo_shu_counts": lo_shu_counts,
            "dob_digit_counts": dob_digit_counts,
            "name_data": name_data,
            "crystal_suggestion": CRYSTAL_SUGGESTIONS[mulank]
        },
        "lo_shu_counts": lo_shu_counts,
        "dob_digit_counts": dob_digit_counts,
        "pinnacles_data": pinnacles_data,
        "cutoffs": cutoffs,
        "tier_counts": tier_counts,
        "days_at_100": sum(1 for s in all_scores if s == 100),
        "min": min(all_scores),
        "max": max(all_scores),
        "months": months_data,
        "full_calendar_365": full_calendar_365
    }
