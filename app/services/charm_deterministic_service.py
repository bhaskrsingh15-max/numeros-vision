# -*- coding: utf-8 -*-
"""
app/services/charm_deterministic_service.py
===========================================
Deterministic Charm AI Consultation Service (Phase 3).

Strict Guarantees:
1. Requires valid Gregorian birth date (day, month, year) and non-empty question (HTTP 400 if missing).
   Zero fallback defaults (never 'Seeker', never 28/11/1981, never a sample question).
2. Deterministic calculations ONLY:
   - Driver (Mulank — Birth Day number), Conductor (Bhagyank — Life Path number), and Lo Shu 3x3 counts
     via `app.engine.digit_root`, `app.engine.lo_shu`, and `app.engine.driver_conductor_81_engine`.
   - Personal Year (PY), Personal Month (PM), and Personal Day (PD) by the owner's exact formula:
       PY = digit_root(flat sum of digits of birth day + birth month + target year)
       PM = digit_root(PY + calendar month)
       PD = digit_root(PY + PM + flat sum of digits of full target date DDMMYYYY)
   - Accurate number meanings 1..9 (Personal Year 9 = completion, release, consolidation — never "foundation").
   - Dasha ONLY when actually calculated via `pyswisseph` (`swisseph`) with Lahiri ayanamsha from valid
     birth_time + birth_place; otherwise `None` and zero mention of dasha anywhere.
   - Remedies in exact owner order:
       1. Element balancing
       2. Planet remedies (tiered by package)
       3. Affirmation (tiered by package)
   - Fixed-rule topic classifier answering exclusively about the classified topic.
   - Optional LLM phrasing (`GEMINI_API_KEY`) strictly over calculated facts, guarded by the banned-word
     and copy-compliance filter (zero "VERIFIED", "validated", "certified", "authentic", "guaranteed",
     "legal certification", or outcome/date promises).
"""

from __future__ import annotations

import datetime
import hashlib
import json
import math
import os
import re
import secrets
import time
import urllib.request
from typing import Any, Callable, Dict, List, Optional, Tuple

from app.engine.digit_root import (
    PLANET_MAP_1_TO_9,
    calc_bhagyank,
    calc_driver,
    calc_loshu_dob_only,
    calc_personal_day,
    calc_personal_month,
    calc_personal_year,
    digit_root,
    sum_digits_str,
)
from app.engine.driver_conductor_81_engine import lookup_driver_conductor_81
from app.engine.indication_schema_and_loader import load_remedy_library
from app.engine.indications_engine import format_planet_remedy_pack
from app.engine.layer1_golden_snapshot import extract_ranked_5_element_remedies
from app.engine.lo_shu import analyze_lo_shu_grid

try:
    import swisseph as swe  # type: ignore

    SWISSEPH_AVAILABLE = True
except ImportError:
    swe = None  # type: ignore
    SWISSEPH_AVAILABLE = False

IST_TZ = datetime.timezone(datetime.timedelta(hours=5, minutes=30))

# Banned copy & worker parity filter (case-insensitive)
BANNED_COPY_PATTERN = re.compile(
    r"\b("
    r"verified|validated|certified|authentic|guaranteed|guarantee|guarantees|"
    r"legal\s+certification|prediction|predictions|prescription|prescriptions|"
    r"consecrated|cure|cures|cured|luck|lucks|lucky|exact"
    r")\b"
    r"|will\s+bring|will\s+fix",
    re.IGNORECASE,
)

COPY_REPLACEMENTS: Tuple[Tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\blegal\s+certification\b", re.I), "technical check"),
    (re.compile(r"\bverified\b", re.I), "calculated"),
    (re.compile(r"\bvalidated\b", re.I), "checked"),
    (re.compile(r"\bcertified\b", re.I), "structured"),
    (re.compile(r"\bauthentic\b", re.I), "traditional"),
    (re.compile(r"\bguaranteed\b", re.I), "steady"),
    (re.compile(r"\bguarantees\b", re.I), "supports"),
    (re.compile(r"\bguarantee\b", re.I), "assurance"),
    (re.compile(r"\bpredictions\b", re.I), "indications"),
    (re.compile(r"\bprediction\b", re.I), "indication"),
    (re.compile(r"\bprescriptions\b", re.I), "suggestions"),
    (re.compile(r"\bprescription\b", re.I), "suggestion"),
    (re.compile(r"\bconsecrated\b", re.I), "prepared"),
    (re.compile(r"\bcured\b", re.I), "supported"),
    (re.compile(r"\bcures\b", re.I), "supports"),
    (re.compile(r"\bcure\b", re.I), "support"),
    (re.compile(r"\bgood\s+luck\b", re.I), "supportive rhythm"),
    (re.compile(r"\blucky\b", re.I), "favourable"),
    (re.compile(r"\blucks?\b", re.I), "fortune"),
    (re.compile(r"will\s+bring", re.I), "may support"),
    (re.compile(r"will\s+fix", re.I), "may help steady"),
    (re.compile(r"\bexact\b", re.I), "specific"),
)


BILINGUAL_GLOSSARY: Tuple[Tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bSurya\s+Namaskar\b(?!\s*\()", re.I), "Surya Namaskar (Sun Salutation)"),
    (re.compile(r"\bGayatri\s+Mantra\b(?!\s*\()", re.I), "Gayatri Mantra (Vedic solar hymn)"),
    (re.compile(r"\bHanuman\s+Chalisa\b(?!\s*\()", re.I), "Hanuman Chalisa (devotional forty-verse hymn)"),
    (re.compile(r"\bRudraksha\b(?!\s*\()", re.I), "Rudraksha (sacred prayer seed)"),
    (re.compile(r"\bPranayama\b(?!\s*\()", re.I), "Pranayama (mindful breath regulation)"),
    (re.compile(r"\bTulsi\b(?!\s*\()", re.I), "Tulsi (holy basil)"),
    (re.compile(r"\bVastu\b(?!\s*\()", re.I), "Vastu (traditional spatial directional layout)"),
    (re.compile(r"\bDaan\b(?!\s*\()", re.I), "Daan (charitable giving)"),
    (re.compile(r"\bTilak\b(?!\s*\()", re.I), "Tilak (forehead sandalwood or saffron mark)"),
    (re.compile(r"\bPuja\b(?!\s*\()", re.I), "Puja (prayer observance)"),
)


def normalize_copy_text(text: str) -> str:
    cleaned = str(text or "")
    for pat, repl in COPY_REPLACEMENTS:
        cleaned = pat.sub(repl, cleaned)
    for pat, repl in BILINGUAL_GLOSSARY:
        cleaned = pat.sub(repl, cleaned)
    return cleaned


def has_banned_copy(text: str) -> bool:
    return bool(BANNED_COPY_PATTERN.search(str(text or "")))


# Canonical meanings for 1..9 (Personal Year 9 is strictly completion/release/consolidation, NEVER foundation)
NUMBER_MEANINGS_1_TO_9: Dict[int, Dict[str, str]] = {
    1: {
        "planet_bilingual": "Surya (Sun)",
        "core_quality": "independent initiative, clear ownership, and self-directed starts",
        "cycle_theme": "Initiation and Fresh Starts",
        "cycle_indication": "tends to favour starting well-defined priorities, clarifying personal direction, and taking calm ownership",
    },
    2: {
        "planet_bilingual": "Chandra (Moon)",
        "core_quality": "diplomacy, receptive listening, emotional sensitivity, and patient cooperation",
        "cycle_theme": "Cooperation and Patient Pacing",
        "cycle_indication": "tends to favour steady dialogue, partnership building, and unhurried timing rather than forceful pushes",
    },
    3: {
        "planet_bilingual": "Guru (Jupiter)",
        "core_quality": "structured learning, teaching, advisory wisdom, and articulate expression",
        "cycle_theme": "Learning, Expression, and Mentored Growth",
        "cycle_indication": "tends to favour skill expansion, clear writing or speaking, and seeking sound counsel",
    },
    4: {
        "planet_bilingual": "Rahu (North Lunar Node)",
        "core_quality": "methodical structure, checklists, practical systems, and step-by-step execution",
        "cycle_theme": "Structure, Systems, and Practical Foundation",
        "cycle_indication": "tends to favour disciplined documentation, realistic budgets, and reliable daily systems",
    },
    5: {
        "planet_bilingual": "Budh (Mercury)",
        "core_quality": "adaptability, agile communication, commercial awareness, and balanced versatility",
        "cycle_theme": "Adaptability, Movement, and Communication",
        "cycle_indication": "tends to favour flexible planning, outreach, thoughtful negotiation, and testing practical improvements",
    },
    6: {
        "planet_bilingual": "Shukra (Venus)",
        "core_quality": "responsibility, household harmony, care, and long-term stewardship",
        "cycle_theme": "Responsibility, Harmony, and Stewardship",
        "cycle_indication": "tends to favour nurturing key relationships, honouring commitments, and improving home or workspace balance",
    },
    7: {
        "planet_bilingual": "Ketu (South Lunar Node)",
        "core_quality": "quiet reflection, deep study, research, and inner discernment",
        "cycle_theme": "Reflection, Study, and Inner Discernment",
        "cycle_indication": "tends to favour careful review, specialist study, and unhurried reflection before major commitments",
    },
    8: {
        "planet_bilingual": "Shani (Saturn)",
        "core_quality": "endurance, accountability, fair governance, and patient long-horizon effort",
        "cycle_theme": "Accountability, Endurance, and Steady Governance",
        "cycle_indication": "tends to favour thorough due diligence, consistent effort, and honouring long-term obligations",
    },
    9: {
        "planet_bilingual": "Mangal (Mars)",
        "core_quality": "courage, decisive energy, humanitarian service, and completing open commitments",
        "cycle_theme": "Completion, Release, and Consolidation",
        "cycle_indication": "tends to favour wrapping up unfinished matters, decluttering obligations, and consolidating lessons before the next nine-year cycle begins",
    },
}

CITY_GAZETTEER: Dict[str, Tuple[float, float, float, str]] = {
    "delhi": (28.6139, 77.2090, 5.5, "New Delhi, India"),
    "new delhi": (28.6139, 77.2090, 5.5, "New Delhi, India"),
    "mumbai": (19.0760, 72.8777, 5.5, "Mumbai, India"),
    "bangalore": (12.9716, 77.5946, 5.5, "Bengaluru, India"),
    "bengaluru": (12.9716, 77.5946, 5.5, "Bengaluru, India"),
    "hyderabad": (17.3850, 78.4867, 5.5, "Hyderabad, India"),
    "chennai": (13.0827, 80.2707, 5.5, "Chennai, India"),
    "kolkata": (22.5726, 88.3639, 5.5, "Kolkata, India"),
    "pune": (18.5204, 73.8567, 5.5, "Pune, India"),
    "ahmedabad": (23.0225, 72.5714, 5.5, "Ahmedabad, India"),
    "jaipur": (26.9124, 75.7873, 5.5, "Jaipur, India"),
    "lucknow": (26.8467, 80.9462, 5.5, "Lucknow, India"),
    "chandigarh": (30.7333, 76.7794, 5.5, "Chandigarh, India"),
    "kochi": (9.9816, 76.2999, 5.5, "Kochi, India"),
    "noida": (28.5355, 77.3910, 5.5, "Noida, India"),
    "gurugram": (28.4595, 77.0266, 5.5, "Gurugram, India"),
    "gurgaon": (28.4595, 77.0266, 5.5, "Gurugram, India"),
    "dubai": (25.2048, 55.2708, 4.0, "Dubai, UAE"),
    "singapore": (1.3521, 103.8198, 8.0, "Singapore"),
    "london": (51.5074, -0.1278, 0.0, "London, UK"),
}

VIMSHOTTARI_SEQUENCE: Tuple[Tuple[str, str, int], ...] = (
    ("Ketu", "Ketu (South Lunar Node)", 7),
    ("Venus", "Shukra (Venus)", 20),
    ("Sun", "Surya (Sun)", 6),
    ("Moon", "Chandra (Moon)", 10),
    ("Mars", "Mangal (Mars)", 7),
    ("Rahu", "Rahu (North Lunar Node)", 18),
    ("Jupiter", "Guru (Jupiter)", 16),
    ("Saturn", "Shani (Saturn)", 19),
    ("Mercury", "Budh (Mercury)", 17),
)

NAKSHATRA_NAMES: Tuple[str, ...] = (
    "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
    "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni",
    "Hasta", "Chitra", "Swati", "Vishakha", "Anuradha", "Jyeshtha",
    "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta", "Shatabhisha",
    "Purva Bhadrapada", "Uttara Bhadrapada", "Revati",
)


class CharmInputError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


def validate_and_parse_charm_input(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Strictly validates question and Gregorian birth date.
    Raises CharmInputError (mapped to HTTP 400) when any required field is missing or invalid.
    Never invents default dates, names, or questions.
    """
    raw_q = str(payload.get("question") or payload.get("message") or "").strip()
    if not raw_q:
        raise CharmInputError(
            "QUESTION_REQUIRED",
            "Please enter your question so Charm AI can prepare your reading. No question credit was used.",
        )
    if len(raw_q) > 500:
        raise CharmInputError(
            "QUERY_TOO_LONG",
            "Please keep your question within 500 characters. No question credit was used.",
        )

    d_raw = payload.get("day")
    m_raw = payload.get("month")
    y_raw = payload.get("year")
    dob_str = str(payload.get("dob") or "").strip()

    d: Optional[int] = None
    m: Optional[int] = None
    y: Optional[int] = None

    if d_raw is not None and m_raw is not None and y_raw is not None and str(d_raw) != "" and str(m_raw) != "" and str(y_raw) != "":
        try:
            d = int(d_raw)
            m = int(m_raw)
            y = int(y_raw)
        except (TypeError, ValueError):
            raise CharmInputError(
                "INVALID_DOB",
                "Please enter valid numeric day, month, and year values for your Date of Birth. No question credit was used.",
            )
    elif dob_str:
        cleaned = dob_str.replace("/", "-").replace(".", "-")
        parts = cleaned.split("-")
        if len(parts) == 3:
            try:
                if len(parts[0]) == 4:
                    y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
                else:
                    d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
            except ValueError:
                d, m, y = None, None, None

    if d is None or m is None or y is None:
        raise CharmInputError(
            "DOB_REQUIRED",
            "Please enter your Date of Birth (day, month, and year) before asking a question. No question credit was used.",
        )

    if not (1900 <= y <= 2100):
        raise CharmInputError(
            "INVALID_DOB",
            "Please enter a birth year between 1900 and 2100. No question credit was used.",
        )

    try:
        birth_dt = datetime.date(y, m, d)
    except ValueError:
        raise CharmInputError(
            "INVALID_DOB",
            "The birth date entered is not a valid calendar date. Please check the day and month. No question credit was used.",
        )

    raw_name = str(payload.get("user_name") or payload.get("name") or "").strip()
    if raw_name.lower() in {"seeker", "guest_user", "visitor", "sample"}:
        raw_name = ""

    birth_time = str(payload.get("birth_time") or payload.get("tob") or "").strip() or None
    birth_place = str(payload.get("birth_place") or payload.get("pob") or payload.get("city") or "").strip() or None

    target_date_str = str(payload.get("target_date") or "").strip()
    if target_date_str:
        try:
            target_dt = datetime.date.fromisoformat(target_date_str)
        except ValueError:
            target_dt = datetime.datetime.now(IST_TZ).date()
    else:
        target_dt = datetime.datetime.now(IST_TZ).date()

    return {
        "question": raw_q,
        "day": birth_dt.day,
        "month": birth_dt.month,
        "year": birth_dt.year,
        "birth_date": birth_dt,
        "user_name": raw_name,
        "birth_time": birth_time,
        "birth_place": birth_place,
        "gender": str(payload.get("gender") or "").strip().lower() or None,
        "edition": str(payload.get("edition") or "india").strip().lower(),
        "remedy_style": payload.get("remedy_style"),
        "target_date": target_dt,
    }


def classify_question_topic(question: str) -> Tuple[str, str]:
    """
    Fixed-rule deterministic topic classifier.
    Returns (topic_id, topic_display_label).
    """
    q = question.lower()
    if re.search(
        r"\b(cancer|diabetes|surgery|tumor|tumour|medical\s+diagnosis|prescribe|medication|dosage|cure\s+my|"
        r"lottery|jackpot|betting|gamble|gambling|roulette|crypto\s+price|stock\s+tip|nifty\s+tomorrow|"
        r"share\s+price|when\s+will\s+i\s+die|death\s+date|lifespan|court\s+verdict|win\s+the\s+lawsuit|criminal\s+case)\b",
        q,
    ):
        return "unsupported", "Outside Consultation Scope"
    if re.search(r"\b(marry|marriage|wedding|spouse|husband|wife|engaged|engagement|matrimony|shaadi|nikah|rishta)\b", q):
        return "marriage", "Marriage & Partnership Indications"
    if re.search(r"\b(love|romance|romantic|boyfriend|girlfriend|crush|dating|relationship|partner|breakup|affection|heartbreak)\b", q):
        return "love", "Relationship & Emotional Harmony"
    if re.search(r"\b(property|house|home|flat|apartment|plot|land|real\s+estate|vastu|door\s+number|house\s+number|rent|relocat)\b", q):
        return "property", "Property & Home Alignment"
    if re.search(r"\b(health|sleep|rest|routine|habit|burnout|fatigue|energy|stress|wellness|fitness|diet\s+rhythm)\b", q):
        return "health", "Daily Routine & Wellbeing Habits"
    if re.search(r"\b(money|wealth|finance|financial|income|savings|debt|loan|cashflow|cash\s+flow|revenue|budget|salary|expenses|invest)\b", q):
        return "money", "Financial Pacing & Stewardship"
    if re.search(r"\b(business|startup|company|venture|enterprise|brand|trade|trading|founder|client|shop|agency)\b", q):
        return "business", "Business & Venture Pacing"
    if re.search(r"\b(study|studies|exam|exams|education|college|university|degree|research|scholarship|student|learning)\b", q):
        return "education", "Study, Learning & Preparation"
    if re.search(r"\b(child|children|baby|kids|parenting|son|daughter|family\s+harmony|newborn)\b", q):
        return "children", "Family & Parenting Rhythm"
    if re.search(r"\b(career|job|promotion|profession|work|role|office|interview|leadership|appraisal|resign|switch\s+jobs)\b", q):
        return "career", "Career & Work Indications"
    return "general", "Personal Cycle & Life Indications"


def compute_vimshottari_dasha_if_calculated(
    birth_dt: datetime.date,
    birth_time: Optional[str],
    birth_place: Optional[str],
    target_dt: datetime.date,
) -> Optional[Dict[str, Any]]:
    """
    Computes Vimshottari Mahadasha (planetary major period) and Antardasha (planetary sub-period)
    ONLY when:
      1. `pyswisseph` (`swisseph`) is installed,
      2. `birth_time` (HH:MM) is provided and valid, AND
      3. `birth_place` resolves in `CITY_GAZETTEER`.
    Uses Lahiri (Chitra Paksha) sidereal ayanamsha (`swe.SIDM_LAHIRI`).
    Returns `None` in all other cases so zero uncomputed dasha claims ever appear.
    """
    if not SWISSEPH_AVAILABLE or swe is None or not birth_time or not birth_place:
        return None

    m_time = re.match(r"^(\d{1,2}):(\d{2})(?::(\d{2}))?$", birth_time.strip())
    if not m_time:
        return None
    hh = int(m_time.group(1))
    mm = int(m_time.group(2))
    ss = int(m_time.group(3) or "0")
    if not (0 <= hh <= 23 and 0 <= mm <= 59 and 0 <= ss <= 59):
        return None

    place_key = re.sub(r"\s+", " ", birth_place.strip().lower().split(",")[0].strip())
    geo = CITY_GAZETTEER.get(place_key)
    if geo is None:
        return None

    _lat, _lon, tz_offset_hours, place_label = geo
    local_hours = hh + (mm / 60.0) + (ss / 3600.0)
    ut_hours = local_hours - tz_offset_hours

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    jd_ut = swe.julday(birth_dt.year, birth_dt.month, birth_dt.day, ut_hours)
    calc_res, _ret_flag = swe.calc_ut(jd_ut, swe.MOON, swe.FLG_SWIEPH | swe.FLG_SIDEREAL)
    moon_sid_lon = float(calc_res[0]) % 360.0
    ayanamsha_deg = float(swe.get_ayanamsa_ut(jd_ut))

    nak_span = 360.0 / 27.0  # 13.333333333333334 deg
    nak_index = int(math.floor(moon_sid_lon / nak_span)) % 27
    fraction_elapsed = (moon_sid_lon - (nak_index * nak_span)) / nak_span
    fraction_remaining = max(0.0, min(1.0, 1.0 - fraction_elapsed))

    start_seq_idx = nak_index % 9
    elapsed_days_since_birth = (target_dt - birth_dt).days
    if elapsed_days_since_birth < 0:
        return None

    days_per_year = 365.2425
    cursor_days = 0.0

    # Walk Mahadashas from birth
    for step in range(18):
        seq_idx = (start_seq_idx + step) % 9
        lord_en, lord_bi, full_years = VIMSHOTTARI_SEQUENCE[seq_idx]
        span_years = (full_years * fraction_remaining) if step == 0 else float(full_years)
        span_days = span_years * days_per_year
        maha_start_days = cursor_days - ((full_years - span_years) * days_per_year if step == 0 else 0.0)
        maha_end_days = cursor_days + span_days

        if elapsed_days_since_birth < maha_end_days:
            # Find Antardasha inside full Mahadasha
            antar_cursor = maha_start_days
            active_antar_bi = lord_bi
            for a_step in range(9):
                a_idx = (seq_idx + a_step) % 9
                _a_en, a_bi, a_years = VIMSHOTTARI_SEQUENCE[a_idx]
                a_days = (full_years * a_years / 120.0) * days_per_year
                if elapsed_days_since_birth < antar_cursor + a_days:
                    active_antar_bi = a_bi
                    break
                antar_cursor += a_days

            return {
                "method": "Vimshottari Dasha (120-year lunar Mansion cycle, Lahiri sidereal ayanamsha)",
                "ayanamsha_degrees": round(ayanamsha_deg, 4),
                "moon_sidereal_longitude": round(moon_sid_lon, 4),
                "janma_nakshatra": NAKSHATRA_NAMES[nak_index],
                "birth_place_used": place_label,
                "mahadasha": lord_bi,
                "antardasha": active_antar_bi,
                "summary_line": (
                    f"Calculated from your birth time and {place_label} using Lahiri ayanamsha (sidereal lunar offset): "
                    f"Moon in **{NAKSHATRA_NAMES[nak_index]} Nakshatra (lunar constellation)**, currently in "
                    f"**{lord_bi} Mahadasha (major planetary period)** and **{active_antar_bi} Antardasha (sub-period)**."
                ),
            }
        cursor_days = maha_end_days

    return None


def build_ordered_remedies(
    driver: int,
    conductor: int,
    personal_year: int,
    counts: Dict[int, int],
    missing: List[int],
    entitlement_tier: str,
    edition: str = "india",
    user_remedy_style: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Builds remedies in the exact owner-mandated order, tiered by package:
      1. Element balancing first
      2. Planet remedies second
      3. Affirmation third
    """
    tier_norm = str(entitlement_tier or "charm_free").lower()
    if tier_norm in {"charm_premium", "premium", "report_premium", "planner_2027"}:
        pkg_tier = "premium"
    elif tier_norm in {"charm_paid", "paid", "charm_single", "advanced", "report_advanced"}:
        pkg_tier = "advanced"
    else:
        pkg_tier = "free"

    # 1. Element balancing first
    elem_bundle = extract_ranked_5_element_remedies(counts, missing)
    max_elem = 1 if pkg_tier == "free" else (2 if pkg_tier == "advanced" else 3)
    element_steps: List[Dict[str, Any]] = []
    for item in elem_bundle.get("ranked_top3_remedies", [])[:max_elem]:
        element_steps.append(
            {
                "element": item["element"],
                "count": item["count"],
                "has_open_digit": item["has_open_digit"],
                "guidance": normalize_copy_text(item["remedy"]),
            }
        )

    # 2. Planet remedies second
    remedy_lib = load_remedy_library()
    planet_targets = [driver]
    if pkg_tier in {"advanced", "premium"} and conductor != driver:
        planet_targets.append(conductor)
    if pkg_tier == "premium" and personal_year not in planet_targets:
        planet_targets.append(personal_year)

    planet_packs: List[Dict[str, Any]] = []
    primary_affirmation = ""
    for p_num in planet_targets:
        pack = format_planet_remedy_pack(
            p_num,
            remedy_lib,
            tier=("basic" if pkg_tier == "free" else pkg_tier),
            edition=edition,
            user_remedy_style=user_remedy_style,
            allow_draft=True,
        )
        if not pack:
            continue
        items_limit = 1 if pkg_tier == "free" else (2 if pkg_tier == "advanced" else 3)
        cleaned_items = [
            normalize_copy_text(it["text"])
            for it in pack.get("items", [])[:items_limit]
        ]
        gem_note = None
        if pkg_tier in {"advanced", "premium"} and pack.get("gemstone_info"):
            gem_note = normalize_copy_text(pack["gemstone_info"].get("display_note", ""))
        if not primary_affirmation and pack.get("affirmation"):
            primary_affirmation = normalize_copy_text(pack["affirmation"])
        planet_packs.append(
            {
                "number": p_num,
                "planet": NUMBER_MEANINGS_1_TO_9[p_num]["planet_bilingual"],
                "day_preference": pack.get("day", ""),
                "colour_preferences": pack.get("colours", []),
                "practices": cleaned_items,
                "optional_gemstone_note": gem_note,
            }
        )

    # 3. Affirmation third
    if not primary_affirmation:
        primary_affirmation = (
            f"I bring steady patience, clear focus, and thoughtful action to my daily responsibilities."
        )

    return {
        "package_tier": pkg_tier,
        "order": ["element_balancing", "planet_remedies", "affirmation"],
        "element_balancing": element_steps,
        "planet_remedies": planet_packs,
        "affirmation": primary_affirmation,
    }


def _compose_topic_specific_guidance(
    topic: str,
    driver: int,
    conductor: int,
    py: int,
    pm: int,
    pd: int,
    combo_81: Dict[str, Any],
    present_digits: List[int],
    missing_digits: List[int],
    completed_planes: List[str],
) -> Tuple[str, List[str], str]:
    """
    Produces strictly topic-scoped prose, practical steps, and follow-up question
    grounded in the actual calculated numbers (zero cross-topic leakage).
    """
    drv_info = NUMBER_MEANINGS_1_TO_9[driver]
    cnd_info = NUMBER_MEANINGS_1_TO_9[conductor]
    py_info = NUMBER_MEANINGS_1_TO_9[py]
    pm_info = NUMBER_MEANINGS_1_TO_9[pm]
    pd_info = NUMBER_MEANINGS_1_TO_9[pd]

    synergy_title = normalize_copy_text(combo_81.get("synergy_title", f"{driver}-{conductor} Combination"))
    pos_traits = [normalize_copy_text(t) for t in (combo_81.get("positive_traits") or [])[:2]]
    caution_note = normalize_copy_text(combo_81.get("warnings_and_cautions") or "")
    rec_careers = [normalize_copy_text(c) for c in (combo_81.get("recommended_careers") or [])[:3]]

    present_str = ", ".join(str(x) for x in present_digits) if present_digits else "none"
    missing_str = ", ".join(str(x) for x in missing_digits) if missing_digits else "none"
    planes_note = (
        f"completed Lo Shu planes ({', '.join(completed_planes)})"
        if completed_planes
        else f"present Lo Shu digits ({present_str}) while consciously supporting open digits ({missing_str})"
    )

    if topic == "career":
        career_list = ", ".join(rec_careers) if rec_careers else "structured advisory, management, and execution roles"
        body = (
            f"For **career and professional work**, your **Mulank (Birth Day number) {driver}** ({drv_info['planet_bilingual']}) "
            f"combines with **Bhagyank (Life Path number) {conductor}** ({cnd_info['planet_bilingual']}) under the traditional "
            f"**{synergy_title}** pattern, where strengths such as {', '.join(pos_traits) or drv_info['core_quality']} stand out "
            f"across fields like {career_list}. "
            f"In **Personal Year {py} ({py_info['cycle_theme']})**, **Personal Month {pm}**, and **Personal Day {pd}**, "
            f"your chart {py_info['cycle_indication']}, drawing on your {planes_note}."
        )
        steps = [
            f"Align your current work deliverables with Personal Year {py} ({py_info['cycle_theme'].lower()}) and Personal Month {pm} ({pm_info['cycle_theme'].lower()}).",
            f"Lean on Mulank {driver} ({drv_info['core_quality']}) while keeping written role scope clear. {caution_note}".strip(),
        ]
        follow_up = f"Would you like to look more closely at role changes versus skill building during Personal Month {pm}?"
        return body, steps, follow_up

    if topic == "marriage":
        body = (
            f"For **marriage and long-term partnership**, your **Mulank (Birth Day number) {driver}** ({drv_info['planet_bilingual']}) "
            f"expresses {drv_info['core_quality']}, while **Bhagyank (Life Path number) {conductor}** ({cnd_info['planet_bilingual']}) "
            f"shapes long-term household expectations through {cnd_info['core_quality']}. "
            f"Within **Personal Year {py} ({py_info['cycle_theme']})** and **Personal Month {pm} ({pm_info['cycle_theme']})**, "
            f"this period {py_info['cycle_indication']}. Your {planes_note} indicate that calm, honest family dialogue serves you better than hurried decisions."
        )
        steps = [
            f"Discuss shared domestic priorities, family expectations, and practical responsibilities openly during Personal Month {pm}.",
            f"If you are comparing charts with a prospective spouse or partner, check both birth dates side by side rather than judging one number alone.",
        ]
        follow_up = "Would you like to compare your birth numbers with a partner's Date of Birth for relationship harmony?"
        return body, steps, follow_up

    if topic == "love":
        body = (
            f"For **love and emotional connection**, **Mulank (Birth Day number) {driver}** ({drv_info['planet_bilingual']}) "
            f"brings {drv_info['core_quality']} into closeness, paired with **Bhagyank (Life Path number) {conductor}** ({cnd_info['planet_bilingual']}) "
            f"for {cnd_info['core_quality']}. "
            f"During **Personal Year {py} ({py_info['cycle_theme']})** and **Personal Month {pm}**, your cycle {py_info['cycle_indication']}, "
            f"inviting patient listening alongside your {planes_note}."
        )
        steps = [
            f"Share feelings in plain, steady conversation during Personal Month {pm} ({pm_info['cycle_theme'].lower()}) rather than leaving expectations unspoken.",
            f"Notice when open Lo Shu digits ({missing_str}) make you either rush or hold back emotionally, and pace conversations gently.",
        ]
        follow_up = "Would you like to check compatibility with someone's Date of Birth or focus on communication habits this month?"
        return body, steps, follow_up

    if topic == "property":
        earth_present = [d for d in (2, 5, 8) if d in present_digits]
        body = (
            f"For **property, housing, and home environment**, **Mulank (Birth Day number) {driver}** ({drv_info['planet_bilingual']}) "
            f"and **Bhagyank (Life Path number) {conductor}** ({cnd_info['planet_bilingual']}) work alongside Earth-plane digits "
            f"({', '.join(str(d) for d in earth_present) if earth_present else 'none present from birth date; Earth digits 2, 5, 8 are open'}). "
            f"In **Personal Year {py} ({py_info['cycle_theme']})** and **Personal Month {pm}**, the cycle {py_info['cycle_indication']} — "
            f"encouraging thorough paperwork review, realistic maintenance budgets, and calm inspection before any property commitment."
        )
        steps = [
            f"Check the single-digit sum (1–9) of any flat, plot, or unit number you are considering against Mulank {driver} and Bhagyank {conductor}.",
            f"Use Personal Month {pm} ({pm_info['cycle_theme'].lower()}) to review title documents, budgets, and living comfort without rushing.",
        ]
        follow_up = "Do you have a specific house or flat number you would like checked against your Mulank and Bhagyank?"
        return body, steps, follow_up

    if topic == "health":
        body = (
            f"From a **non-medical daily routine and wellbeing perspective** (never a substitute for medical care), "
            f"**Mulank (Birth Day number) {driver}** ({drv_info['planet_bilingual']}) and **Bhagyank (Life Path number) {conductor}** "
            f"({cnd_info['planet_bilingual']}) respond best when {drv_info['core_quality']} is balanced with regular rest. "
            f"In **Personal Year {py} ({py_info['cycle_theme']})**, **Personal Month {pm}**, and **Personal Day {pd}**, "
            f"your cycle {py_info['cycle_indication']}, reminding you to pace energy steadily."
        )
        steps = [
            f"Keep a consistent sleep-wake hour and hydration habit throughout Personal Month {pm} ({pm_info['cycle_theme'].lower()}).",
            "For any physical symptom or health concern, always consult a qualified medical professional promptly.",
        ]
        follow_up = "Would you like suggestions on structuring your morning and evening routine around your Personal Month rhythm?"
        return body, steps, follow_up

    if topic == "money":
        body = (
            f"For **financial pacing, savings, and resource stewardship**, your **Mulank (Birth Day number) {driver}** ({drv_info['planet_bilingual']}) "
            f"and **Bhagyank (Life Path number) {conductor}** ({cnd_info['planet_bilingual']}) reflect the **{synergy_title}** pattern, "
            f"combining {drv_info['core_quality']} with {cnd_info['core_quality']}. "
            f"In **Personal Year {py} ({py_info['cycle_theme']})** and **Personal Month {pm} ({pm_info['cycle_theme']})**, "
            f"this cycle {py_info['cycle_indication']}, favouring written budgets and sensible reserve buffers over impulsive outlays."
        )
        steps = [
            f"Review monthly cash outflows and savings reserves at the start of Personal Month {pm}.",
            f"Keep written terms and clear repayment or spending limits in view whenever open Lo Shu digits ({missing_str}) tempt rushed spending.",
        ]
        follow_up = f"Would you like to focus on budgeting habits or contract review timing during Personal Year {py}?"
        return body, steps, follow_up

    if topic == "business":
        body = (
            f"For **business and venture operations**, **Mulank (Birth Day number) {driver}** ({drv_info['planet_bilingual']}) "
            f"and **Bhagyank (Life Path number) {conductor}** ({cnd_info['planet_bilingual']}) form **{synergy_title}**, "
            f"highlighting {', '.join(pos_traits) or drv_info['core_quality']}. "
            f"Operating in **Personal Year {py} ({py_info['cycle_theme']})** and **Personal Month {pm}**, your cycle "
            f"{py_info['cycle_indication']} — supporting clear unit economics, customer service consistency, and measured execution."
        )
        steps = [
            f"Pace product, client, or operational milestones to match Personal Year {py} ({py_info['cycle_theme'].lower()}).",
            f"Check your trading or brand name's Chaldean single-digit root (1–9) alongside Mulank {driver} and Bhagyank {conductor}.",
        ]
        follow_up = "Would you like to evaluate a specific trading name or partner birth date for your business?"
        return body, steps, follow_up

    if topic == "education":
        body = (
            f"For **study, exams, and skill preparation**, **Mulank (Birth Day number) {driver}** ({drv_info['planet_bilingual']}) "
            f"brings {drv_info['core_quality']}, while **Bhagyank (Life Path number) {conductor}** ({cnd_info['planet_bilingual']}) "
            f"supports long-horizon retention through {cnd_info['core_quality']}. "
            f"In **Personal Year {py} ({py_info['cycle_theme']})** and **Personal Month {pm}**, your cycle {py_info['cycle_indication']}."
        )
        steps = [
            f"Break syllabus or research goals into focused daily blocks aligned with Personal Month {pm} ({pm_info['cycle_theme'].lower()}).",
            "Pair active recall and written revision notes with regular rest breaks so concentration stays steady.",
        ]
        follow_up = "Would you like to plan a study revision cadence for the coming months of this Personal Year?"
        return body, steps, follow_up

    if topic == "children":
        body = (
            f"For **family rhythm and parenting**, **Mulank (Birth Day number) {driver}** ({drv_info['planet_bilingual']}) "
            f"and **Bhagyank (Life Path number) {conductor}** ({cnd_info['planet_bilingual']}) encourage combining "
            f"{drv_info['core_quality']} with patient warmth ({cnd_info['core_quality']}). "
            f"In **Personal Year {py} ({py_info['cycle_theme']})** and **Personal Month {pm}**, steady household routines help everyone thrive."
        )
        steps = [
            f"Keep predictable study, play, and family conversation times during Personal Month {pm}.",
            "If you are exploring a child's own chart or name alignment, enter the child's Date of Birth separately for a dedicated calculation.",
        ]
        follow_up = "Would you like to check a child's Date of Birth or explore baby-naming numerology?"
        return body, steps, follow_up

    # general
    body = (
        f"Your **Mulank (Birth Day number) {driver}** ({drv_info['planet_bilingual']}) reflects {drv_info['core_quality']}, "
        f"while **Bhagyank (Life Path number) {conductor}** ({cnd_info['planet_bilingual']}) indicates a life path shaped by "
        f"{cnd_info['core_quality']} (**{synergy_title}**). "
        f"Right now you are in **Personal Year {py} ({py_info['cycle_theme']})**, **Personal Month {pm} ({pm_info['cycle_theme']})**, "
        f"and **Personal Day {pd} ({pd_info['cycle_theme']})** — a period that {py_info['cycle_indication']} while drawing on your {planes_note}."
    )
    steps = [
        f"Focus on one clear priority suited to Personal Year {py} ({py_info['cycle_theme'].lower()}) and Personal Month {pm}.",
        f"Apply the ordered element and planetary habits below consistently rather than trying to change everything at once.",
    ]
    follow_up = "Which specific area would you like to explore next — career, marriage, property, health habits, or money?"
    return body, steps, follow_up


def _format_remedies_markdown(remedies: Dict[str, Any]) -> str:
    lines: List[str] = ["**Supportive Remedies (in order):**"]
    # 1. Element balancing
    elem_list = remedies.get("element_balancing") or []
    if elem_list:
        elem_parts = [f"{e['element']} ({e['guidance']})" for e in elem_list]
        lines.append(f"1. **Element Balancing:** {' '.join(elem_parts)}")
    else:
        lines.append("1. **Element Balancing:** Keep a balanced daily connection to natural light, water hydration, and uncluttered space.")

    # 2. Planet remedies
    p_packs = remedies.get("planet_remedies") or []
    if p_packs:
        p_texts: List[str] = []
        for pp in p_packs:
            prac = "; ".join(pp.get("practices") or [])
            col = ", ".join(pp.get("colour_preferences") or [])
            seg = f"Number {pp['number']} — {pp['planet']}"
            if pp.get("day_preference"):
                seg += f" ({pp['day_preference']}"
                if col:
                    seg += f", colours: {col}"
                seg += ")"
            if prac:
                seg += f": {prac}"
            if pp.get("optional_gemstone_note"):
                seg += f" Optional traditional stone note: {pp['optional_gemstone_note']}"
            p_texts.append(seg)
        lines.append(f"2. **Planet Remedies:** {' | '.join(p_texts)}")

    # 3. Affirmation
    aff = remedies.get("affirmation") or ""
    if aff:
        lines.append(f"3. **Affirmation:** *\"{aff}\"*")
    return "\n".join(lines)


def _try_optional_gemini_phrasing(
    facts_summary: Dict[str, Any],
    question: str,
    deterministic_draft: str,
) -> Optional[str]:
    """
    Optional LLM phrasing (`GEMINI_API_KEY`) strictly over already-calculated numbers.
    Never sends PII (no DOB, no name, no email, no phone).
    Rejects immediately if any banned word appears or if core numbers are altered.
    """
    if os.getenv("NV_DISABLE_LIVE_LLM", "").strip().lower() in {"true", "1"}:
        return None
    api_key = (os.getenv("GEMINI_API_KEY") or "").strip()
    if not api_key:
        return None

    model_id = (os.getenv("GEMINI_CHARM_MODEL") or "gemini-2.5-flash").strip()
    sys_prompt = (
        "You are Charm AI for Numeros Vision. Rephrase ONLY the supplied deterministic numerology reading "
        "in warm, clear, respectful language. Keep every calculated number, Lo Shu count, cycle number, "
        "and 1->2->3 remedy order intact. Never invent numbers, dates, colours, directions, or dasha periods. "
        "Always pair Sanskrit/Hindi terms with plain English in parentheses. "
        "Use indication language (may, can, tends to). Never promise outcomes or dates. "
        "Never use the words: verified, validated, certified, authentic, guaranteed, legal certification, "
        "luck, lucky, cure, prediction, prescription, consecrated, exact, will bring, will fix."
    )
    req_body = {
        "system_instruction": {"parts": [{"text": sys_prompt}]},
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 700},
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": json.dumps(
                            {
                                "question_topic": facts_summary.get("topic"),
                                "user_question": question,
                                "calculated_facts": facts_summary,
                                "approved_deterministic_draft": deterministic_draft,
                            },
                            ensure_ascii=False,
                        )
                    }
                ],
            }
        ],
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(req_body).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=6.0) as resp:
            raw = json.loads(resp.read().decode("utf-8"))
        candidates = raw.get("candidates") or []
        if not candidates:
            return None
        parts = ((candidates[0].get("content") or {}).get("parts")) or []
        phrased = "".join(str(p.get("text") or "") for p in parts).strip()
        if not phrased or has_banned_copy(phrased):
            return None
        # Ensure core numbers still appear in phrased output
        for must_num in (
            str(facts_summary["driver"]),
            str(facts_summary["conductor"]),
            str(facts_summary["personal_year"]),
        ):
            if must_num not in phrased:
                return None
        return phrased
    except Exception:
        return None


def run_deterministic_charm_consultation(
    payload: Dict[str, Any],
    *,
    entitlement_tier: str = "charm_free",
    on_stage: Optional[Callable[[Dict[str, Any]], None]] = None,
) -> Dict[str, Any]:
    """
    Executes the full Phase 3 Charm AI consultation deterministically.
    Emits working stages ('calculating', 'analysing', 'preparing your reading') via `on_stage`
    and returns them in `stage_events`.
    """
    parsed = validate_and_parse_charm_input(payload)
    question = parsed["question"]
    day = parsed["day"]
    month = parsed["month"]
    year = parsed["year"]
    birth_dt: datetime.date = parsed["birth_date"]
    target_dt: datetime.date = parsed["target_date"]

    stage_events: List[Dict[str, Any]] = []

    def emit_stage(idx: int, stage_id: str, label: str, status: str, started_ms: float) -> None:
        ev = {
            "stage": stage_id,
            "label": label,
            "status": status,
            "step_index": idx,
            "total_steps": 3,
            "elapsed_ms": max(0, int(round((time.perf_counter() - started_ms) * 1000))),
        }
        stage_events.append(ev)
        if on_stage is not None:
            on_stage(ev)

    topic, topic_display = classify_question_topic(question)
    trace_id = f"NV-TRC-{secrets.token_hex(4).upper()}"
    pred_id = f"charm_{int(time.time() * 1000)}_{secrets.token_hex(3)}"

    if topic == "unsupported":
        return {
            "status": "UNSUPPORTED_TOPIC",
            "code": "UNSUPPORTED_TOPIC",
            "topic": "unsupported",
            "topic_display": topic_display,
            "consensus_status": "UNSUPPORTED_TOPIC",
            "credit_chargeable": False,
            "audit_trace_id": trace_id,
            "prediction_id": pred_id,
            "human_friendly_summary": {
                "headline": "Topic Outside Numerology Consultation Scope",
                "supported_by_report": "Charm AI offers reflective numerology indications for career, marriage, relationships, property, daily habits, education, business, and financial pacing.",
            },
            "assistant_message": {
                "text": (
                    "Charm AI does not provide medical diagnoses or treatments, stock/lottery/gambling tips, "
                    "court outcomes, or lifespan forecasts. **No question credit was used.** "
                    "You are welcome to ask about career pacing, marriage or relationship harmony, property numbers, "
                    "study preparation, financial discipline, or daily routine habits."
                )
            },
            "practical_next_steps": [
                "Consult a qualified medical, legal, or licensed financial professional for clinical, legal, or market decisions.",
                "Ask a question about personal timing cycles, relationship compatibility, or supportive daily habits if helpful.",
            ],
            "follow_up_question": "Would you like to explore your Personal Year indications for career, marriage, property, or finances instead?",
            "stage_events": stage_events,
        }

    # Stage 1: Calculating
    t1 = time.perf_counter()
    emit_stage(1, "calculating", "Calculating your birth numbers, Lo Shu grid, and personal cycles", "started", t1)
    driver = calc_driver(day)
    conductor = calc_bhagyank(day, month, year)
    loshu_dob = calc_loshu_dob_only(day, month, year)
    loshu_full = analyze_lo_shu_grid(day, month, year)
    counts: Dict[int, int] = loshu_dob["counts"]
    nonzero_counts: Dict[str, int] = {str(k): v for k, v in counts.items() if v > 0}
    present_digits: List[int] = loshu_dob["present"]
    missing_digits: List[int] = loshu_dob["missing"]
    completed_planes: List[str] = loshu_full.get("completed_planes", [])

    py = calc_personal_year(day, month, target_dt.year)
    pm = calc_personal_month(py, target_dt.month)
    pd = calc_personal_day(py, pm, target_dt.day, target_dt.month, target_dt.year)

    dasha_info = compute_vimshottari_dasha_if_calculated(
        birth_dt=birth_dt,
        birth_time=parsed["birth_time"],
        birth_place=parsed["birth_place"],
        target_dt=target_dt,
    )
    emit_stage(1, "calculating", "Calculating your birth numbers, Lo Shu grid, and personal cycles", "completed", t1)

    # Stage 2: Analysing
    t2 = time.perf_counter()
    emit_stage(2, "analysing", f"Analysing {topic_display.lower()} and 81-combination indicators", "started", t2)
    combo_81 = lookup_driver_conductor_81(driver, conductor)
    topic_body, next_steps, follow_up = _compose_topic_specific_guidance(
        topic=topic,
        driver=driver,
        conductor=conductor,
        py=py,
        pm=pm,
        pd=pd,
        combo_81=combo_81,
        present_digits=present_digits,
        missing_digits=missing_digits,
        completed_planes=completed_planes,
    )
    remedies = build_ordered_remedies(
        driver=driver,
        conductor=conductor,
        personal_year=py,
        counts=counts,
        missing=missing_digits,
        entitlement_tier=entitlement_tier,
        edition=parsed["edition"],
        user_remedy_style=parsed["remedy_style"],
    )
    emit_stage(2, "analysing", f"Analysing {topic_display.lower()} and 81-combination indicators", "completed", t2)

    # Stage 3: Preparing your reading
    t3 = time.perf_counter()
    emit_stage(3, "preparing_reading", "Preparing your reading", "started", t3)

    drv_meta = NUMBER_MEANINGS_1_TO_9[driver]
    cnd_meta = NUMBER_MEANINGS_1_TO_9[conductor]
    py_meta = NUMBER_MEANINGS_1_TO_9[py]
    pm_meta = NUMBER_MEANINGS_1_TO_9[pm]
    pd_meta = NUMBER_MEANINGS_1_TO_9[pd]

    counts_summary = ", ".join(f"{k}×{v}" for k, v in nonzero_counts.items())
    missing_summary = ", ".join(str(m_dig) for m_dig in missing_digits) if missing_digits else "None"

    sections: List[str] = [
        f"### {topic_display}",
        (
            f"**Calculated Numbers:**\n"
            f"- **Mulank (Birth Day number): {driver}** — {drv_meta['planet_bilingual']} ({drv_meta['core_quality']})\n"
            f"- **Bhagyank (Life Path number): {conductor}** — {cnd_meta['planet_bilingual']} ({cnd_meta['core_quality']})\n"
            f"- **Lo Shu 3×3 Grid Counts:** {counts_summary} (Open digits: {missing_summary})\n"
            f"- **Personal Cycles ({target_dt.isoformat()}):** **Personal Year {py}** ({py_meta['cycle_theme']}) · "
            f"**Personal Month {pm}** ({pm_meta['cycle_theme']}) · **Personal Day {pd}** ({pd_meta['cycle_theme']})"
        ),
    ]

    if dasha_info is not None:
        sections.append(f"**Astronomical Dasha Period:**\n{dasha_info['summary_line']}")

    sections.append(topic_body)
    sections.append(_format_remedies_markdown(remedies))
    sections.append("*Note: Numerology offers traditional symbolic indications for self-reflection and planning, never a promise of specific events or outcomes.*")

    deterministic_text = normalize_copy_text("\n\n".join(sections))

    facts_for_llm = {
        "topic": topic,
        "driver": driver,
        "conductor": conductor,
        "loshu_nonzero_counts": nonzero_counts,
        "loshu_missing_digits": missing_digits,
        "personal_year": py,
        "personal_month": pm,
        "personal_day": pd,
        "personal_year_theme": py_meta["cycle_theme"],
        "dasha_included": dasha_info is not None,
    }
    llm_phrased = _try_optional_gemini_phrasing(facts_for_llm, question, deterministic_text)
    final_text = normalize_copy_text(llm_phrased) if llm_phrased else deterministic_text
    if has_banned_copy(final_text):
        final_text = deterministic_text

    cleaned_steps = [normalize_copy_text(s) for s in next_steps]
    cleaned_followup = normalize_copy_text(follow_up)
    headline = normalize_copy_text(
        f"{topic_display} · Mulank {driver}, Bhagyank {conductor} & Personal Year {py} ({py_meta['cycle_theme']})"
    )

    emit_stage(3, "preparing_reading", "Preparing your reading", "completed", t3)

    consensus_label = "MULTI_SYSTEM_ALIGNED" if dasha_info is not None else "NUMEROLOGY_CALCULATION_READY"

    response: Dict[str, Any] = {
        "status": "ANSWERED",
        "topic": topic,
        "topic_display": topic_display,
        "consensus_status": consensus_label,
        "credit_chargeable": True,
        "entitlement_tier": entitlement_tier,
        "audit_trace_id": trace_id,
        "prediction_id": pred_id,
        "engine_outputs": {
            "driver": driver,
            "conductor": conductor,
            "loshu_counts": {str(k): v for k, v in counts.items()},
            "loshu_nonzero_counts": nonzero_counts,
            "loshu_present": present_digits,
            "loshu_missing": missing_digits,
            "completed_planes": completed_planes,
            "driver_conductor_81": {
                "key": combo_81.get("key"),
                "synergy_title": normalize_copy_text(combo_81.get("synergy_title", "")),
                "relationship_type": combo_81.get("relationship_type"),
                "star_rating": combo_81.get("star_rating"),
            },
            "personal_cycles": {
                "target_date": target_dt.isoformat(),
                "personal_year": py,
                "personal_year_theme": py_meta["cycle_theme"],
                "personal_month": pm,
                "personal_month_theme": pm_meta["cycle_theme"],
                "personal_day": pd,
                "personal_day_theme": pd_meta["cycle_theme"],
            },
        },
        "remedies": remedies,
        "human_friendly_summary": {
            "headline": headline,
            "supported_by_report": (
                f"Calculated from Mulank (Birth Day number) {driver}, Bhagyank (Life Path number) {conductor}, "
                f"Lo Shu grid ({counts_summary}), and Personal Year {py} / Month {pm} / Day {pd}."
            ),
        },
        "assistant_message": {"text": final_text},
        "practical_next_steps": cleaned_steps,
        "follow_up_question": cleaned_followup,
        "missing_requirements": {
            "missing_inputs": (
                []
                if dasha_info is not None
                else [
                    k
                    for k, v in (("birth_time", parsed["birth_time"]), ("birth_place", parsed["birth_place"]))
                    if not v
                ]
            )
        },
        "stage_events": stage_events,
    }
    if dasha_info is not None:
        response["engine_outputs"]["dasha"] = dasha_info
        response["numerology_dasha_result"] = {
            "active_window": f"{dasha_info['mahadasha']} Mahadasha · {dasha_info['antardasha']} Antardasha",
            "mahadasha_planet": dasha_info["mahadasha"],
            "antardasha_planet": dasha_info["antardasha"],
        }
    return response
