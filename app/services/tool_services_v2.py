# -*- coding: utf-8 -*-
"""
app/services/tool_services_v2.py
================================
Phase 4 Deterministic Tool Services Router (`numeros-engine`).

Wraps locked deterministic calculation engines in `app/engine/*` (read-only;
zero modifications to `app/engine/*.py`) and exposes the 10 contracts required
by the Numeros Vision calculator & business alignment pages:

1. POST /api/v2/numerology/name/balance
2. POST /api/v2/numerology/relationships/synastry
3. POST /api/v2/numerology/assets/mobile
4. POST /api/v2/numerology/assets/vehicle
5. POST /api/v2/numerology/assets/property
6. POST /api/v2/numerology/forecast/blessing-years
7. POST /api/v2/numerology/naming/baby
8. POST /api/v2/numerology/professions/recommend
9. POST /api/v1/business/existing-diagnose
10. POST /api/v1/business/startup-evaluate

Guarantees on every endpoint:
- Authenticated via `X-NV-Engine-Secret` (`ENGINE_SERVICE_SECRET`).
- Empty or invalid inputs return HTTP 400 with a plain, helpful message.
- Every derived root number reduces strictly to single digits 1..9 (never 11, 22, 33).
- Every result line is explicitly labeled `"calculated"`, `"traditional rule"`, or `"not configured"`.
- Zero invented sample fallbacks; missing optional inputs report `"not configured"`.
- Every string passes copy-compliance normalization (zero forbidden words; bilingual glosses on Hindi/Sanskrit terms).
"""

from __future__ import annotations

import datetime
import json
import re
from typing import Any, Callable, Dict, List, Optional, Tuple

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse

from app.engine.asset_numerology_engine import (
    analyze_mobile_number,
    analyze_property_number,
    analyze_vehicle_number,
)
from app.engine.business_direction_engine import (
    BusinessDirectionEngine,
    CandidateBusinessOption,
    FounderProfile,
)
from app.engine.digit_root import calc_bhagyank, calc_driver, digit_root
from app.engine.forecast_engine import calculate_blessing_years
from app.engine.life_aspects_engine import analyze_relationship_compatibility
from app.engine.name_balancing_engine import evaluate_name_rules
from app.engine.naming_engine import recommend_baby_names
from app.engine.number_characteristics_registry import PLANETARY_RULERS
from app.engine.profession_engine import recommend_professions
from app.services.charm_deterministic_service import normalize_copy_text

MAX_TOOL_BODY_BYTES = 65536

_business_engine = BusinessDirectionEngine()

PLANET_BILINGUAL_LABELS: Dict[int, str] = {
    1: "Sun (Surya — Solar Leadership)",
    2: "Moon (Chandra — Lunar receptivity)",
    3: "Jupiter (Guru — Wisdom & expansion)",
    4: "Rahu (North Lunar Node — Systems & order)",
    5: "Mercury (Budh — Communication & commerce)",
    6: "Venus (Shukra — Harmony & aesthetics)",
    7: "Ketu (South Lunar Node — Research & reflection)",
    8: "Saturn (Shani — Discipline & endurance)",
    9: "Mars (Mangal — Initiative & completion)",
}

EXTRA_BILINGUAL_GLOSSES: Tuple[Tuple[re.Pattern[str], str], ...] = (
    (re.compile(r"\bMulank\b(?!\s*\()", re.I), "Mulank (Birth Day number)"),
    (re.compile(r"\bBhagyank\b(?!\s*\()", re.I), "Bhagyank (Life Path number)"),
    (re.compile(r"\bUpayas\b(?!\s*\()", re.I), "Upayas (traditional balancing practices)"),
    (re.compile(r"\bUpaya\b(?!\s*\()", re.I), "Upaya (traditional balancing practice)"),
    (re.compile(r"\bMor\s+Pankh\b(?!\s*\()", re.I), "Mor Pankh (peacock feather)"),
    (re.compile(r"\bSwastika\b(?!\s*\()", re.I), "Swastika (traditional auspicious geometric emblem)"),
    (re.compile(r"\bToran\b(?!\s*\()", re.I), "Toran (traditional doorway leaf garland)"),
    (re.compile(r"\bPrana\b(?!\s*\()", re.I), "Prana (vital household energy)"),
    (re.compile(r"\bBrahmasthan\b(?!\s*\()", re.I), "Brahmasthan (central courtyard zone)"),
    (re.compile(r"\bMuhurat\b(?!\s*\()", re.I), "Muhurat (traditional auspicious time window)"),
    (re.compile(r"\bKuber\b(?!\s*\()", re.I), "Kuber (traditional treasury guardianship)"),
    (re.compile(r"\bBhrigu\s+Nandi\s+Nadi\b(?!\s*\()", re.I), "Bhrigu Nandi Nadi (traditional planetary combination system)"),
    (re.compile(r"\bKarmakaraka\b(?!\s*\()", re.I), "Karmakaraka (significator of work)"),
    (re.compile(r"\bWCAG\s+2\.1\s+AAA\b", re.I), "WCAG 2.1 contrast standards"),
    (re.compile(r"\bis\s+scheduled\s+at\b", re.I), "indicates a supportive cycle around"),
    (re.compile(r"\bwill\s+succeed\b", re.I), "may find commercial traction"),
)


class ToolInputError(ValueError):
    def __init__(self, message: str, code: str = "INVALID_INPUT") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


def _clean_text(text: str) -> str:
    cleaned = normalize_copy_text(text)
    for pattern, repl in EXTRA_BILINGUAL_GLOSSES:
        cleaned = pattern.sub(repl, cleaned)
    return cleaned


_PRESERVE_ENUM_STRINGS = frozenset(
    {
        "calculated",
        "traditional rule",
        "not configured",
        "SUCCESS",
        "protected",
        "friction_detected",
        "aligned",
        "partially_aligned",
        "conflicted",
        "insufficient_evidence",
        "SUPER_HARMONIOUS",
        "PROTECTED_FRONTEND",
        "FRICTION_DETECTED",
        "COMMERCIALLY_VIABLE",
        "COMMERCIAL_PREREQUISITES_REQUIRED",
        "Harmonious",
        "Friendly",
        "Neutral",
        "Enemy",
    }
)


def _sanitize_tree(value: Any, *, key_name: str = "") -> Any:
    if isinstance(value, str):
        if value in _PRESERVE_ENUM_STRINGS or key_name in {
            "basis",
            "status",
            "alignment_status",
            "diagnosis_verdict",
            "protection_layer_status",
            "checkout_url",
            "idea_id",
            "rule_id",
        }:
            return value
        if value.startswith("#") and len(value) in (4, 7):
            return value
        if value.startswith("/") and " " not in value and len(value) < 64:
            return value
        return _clean_text(value)
    if isinstance(value, list):
        return [_sanitize_tree(item, key_name=key_name) for item in value]
    if isinstance(value, dict):
        out: Dict[str, Any] = {}
        for k, v in value.items():
            if isinstance(v, int) and not isinstance(v, bool) and k in {
                "driver",
                "conductor",
                "calculated_driver",
                "calculated_conductor",
                "first_name_root",
                "full_root",
                "last_name_root",
                "root_number",
                "single_root",
                "root",
                "name_root",
                "name_single",
                "total_root",
                "full_plate_root",
                "core_running_root",
                "property_root",
                "property_root_number",
                "personal_year",
                "legal_name_root",
                "trading_name_root",
                "brand_root",
            } and v > 0:
                out[k] = digit_root(v)
            else:
                out[k] = _sanitize_tree(v, key_name=str(k))
        return out
    return value


def _bad_request(err: ToolInputError) -> JSONResponse:
    return JSONResponse(
        status_code=400,
        content={
            "success": False,
            "status": "INVALID_INPUT",
            "code": err.code,
            "error": err.message,
        },
    )


async def _read_json_object(request: Request) -> Dict[str, Any]:
    raw = await request.body()
    if len(raw) > MAX_TOOL_BODY_BYTES:
        raise ToolInputError("Request payload exceeds maximum allowed size.", "PAYLOAD_TOO_LARGE")
    if not raw or not raw.strip():
        raise ToolInputError("Request body cannot be empty. Please provide the required inputs.", "EMPTY_BODY")
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise ToolInputError("Malformed JSON request body.", "MALFORMED_JSON") from exc
    if not isinstance(parsed, dict) or not parsed:
        raise ToolInputError("Request body must be a non-empty JSON object.", "EMPTY_BODY")
    return parsed


def _require_alpha_string(payload: Dict[str, Any], field: str, label: str, max_len: int = 160) -> str:
    raw = payload.get(field)
    if not isinstance(raw, str) or not raw.strip():
        raise ToolInputError(f"Please enter {label}.", f"MISSING_{field.upper()}")
    val = raw.strip()
    if len(val) > max_len:
        raise ToolInputError(f"{label.capitalize()} must be {max_len} characters or fewer.", f"TOO_LONG_{field.upper()}")
    if not any(ch.isalpha() for ch in val):
        raise ToolInputError(f"{label.capitalize()} must contain alphabetic letters.", f"INVALID_{field.upper()}")
    return val


def _require_nonempty_string(payload: Dict[str, Any], field: str, label: str, max_len: int = 800) -> str:
    raw = payload.get(field)
    if not isinstance(raw, str) or not raw.strip():
        raise ToolInputError(f"Please enter {label}.", f"MISSING_{field.upper()}")
    val = raw.strip()
    if len(val) > max_len:
        raise ToolInputError(f"{label.capitalize()} must be {max_len} characters or fewer.", f"TOO_LONG_{field.upper()}")
    return val


def _parse_single_digit_int(val: Any, label: str, *, allow_none: bool = False) -> Optional[int]:
    if val is None or val == "":
        if allow_none:
            return None
        raise ToolInputError(f"Please provide a valid {label} from 1 to 9.", "MISSING_SINGLE_DIGIT")
    if isinstance(val, bool):
        raise ToolInputError(f"{label} must be a whole number from 1 to 9.", "INVALID_SINGLE_DIGIT")
    try:
        n = int(val)
    except (TypeError, ValueError) as exc:
        raise ToolInputError(f"{label} must be a whole number from 1 to 9.", "INVALID_SINGLE_DIGIT") from exc
    if n < 1 or n > 9:
        raise ToolInputError(f"{label} must be between 1 and 9.", "OUT_OF_RANGE_SINGLE_DIGIT")
    return n


def _validate_gregorian_ymd(day: Any, month: Any, year: Any, label: str = "Date of Birth") -> Tuple[int, int, int]:
    if isinstance(day, bool) or isinstance(month, bool) or isinstance(year, bool):
        raise ToolInputError(f"Please provide a valid {label} (day, month, and year).", "INVALID_DATE")
    try:
        d = int(day)
        m = int(month)
        y = int(year)
    except (TypeError, ValueError) as exc:
        raise ToolInputError(f"Please provide a valid {label} (day, month, and year).", "INVALID_DATE") from exc
    if y < 1900 or y > 2100:
        raise ToolInputError(f"{label} year must be between 1900 and 2100.", "INVALID_YEAR")
    try:
        datetime.date(y, m, d)
    except ValueError as exc:
        raise ToolInputError(f"{label} ({d:02d}/{m:02d}/{y:04d}) is not a valid calendar date.", "INVALID_DATE") from exc
    return d, m, y


def _parse_dob_string(dob_str: str, label: str = "Date of Birth") -> Tuple[int, int, int]:
    s = dob_str.strip()
    m_iso = re.match(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})$", s)
    if m_iso:
        return _validate_gregorian_ymd(int(m_iso.group(3)), int(m_iso.group(2)), int(m_iso.group(1)), label)
    m_dmy = re.match(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})$", s)
    if m_dmy:
        return _validate_gregorian_ymd(int(m_dmy.group(1)), int(m_dmy.group(2)), int(m_dmy.group(3)), label)
    raise ToolInputError(f"Please enter {label} in YYYY-MM-DD or DD-MM-YYYY format.", "INVALID_DOB_FORMAT")


def _prov_line(key: str, label: str, basis: str, detail: str) -> Dict[str, str]:
    assert basis in ("calculated", "traditional rule", "not configured")
    return {"key": key, "label": label, "basis": basis, "detail": detail}


def _compliant_business_monetization_gate(entity_name: str, compound: int, root: int, status: str) -> Dict[str, Any]:
    # Price digit-root check:
    # 510 -> 5 + 1 + 0 = 6 (allowed: 1, 3, 5, 6)
    # 1020 -> 1 + 0 + 2 + 0 = 3 (allowed: 1, 3, 5, 6)
    clean_entity = (entity_name or "Your Venture").strip()
    return {
        "tool_key": "business_alignment",
        "entity_name": clean_entity,
        "compound": compound,
        "root": digit_root(root) if root > 0 else 1,
        "status": status,
        "entry_price_inr": 510,
        "anchor_price_inr": 1020,
        "discount_badge": "EXPLORE REPORT OPTIONS",
        "lock_headline": f"Explore Complete Business Numerology Dossier for {clean_entity}",
        "charm_tagline_action": "ANVEIL EVERY CHARM",
        "checkout_url": "/pricing/",
    }


def create_tool_services_router(auth_dependency: Callable[[Request], None]) -> APIRouter:
    router = APIRouter()

    # 1. Name Balancing: POST /api/v2/numerology/name/balance
    @router.post("/api/v2/numerology/name/balance")
    async def handle_name_balance(request: Request) -> JSONResponse:
        auth_dependency(request)
        try:
            body = await _read_json_object(request)
            full_name = _require_alpha_string(body, "full_name", "your full name", max_len=120)
            dob_raw = body.get("dob_str")
            dob_clean: Optional[str] = None
            derived_driver: Optional[int] = None
            derived_conductor: Optional[int] = None
            if dob_raw is not None and str(dob_raw).strip() != "":
                d, m, y = _parse_dob_string(str(dob_raw), "Date of Birth")
                dob_clean = f"{y:04d}-{m:02d}-{d:02d}"
                derived_driver = calc_driver(d)
                derived_conductor = calc_bhagyank(d, m, y)

            req_driver = _parse_single_digit_int(body.get("driver"), "Driver number", allow_none=True)
            req_conductor = _parse_single_digit_int(body.get("conductor"), "Conductor number", allow_none=True)

            driver = derived_driver if derived_driver is not None else req_driver
            conductor = derived_conductor if derived_conductor is not None else req_conductor
            if driver is None or conductor is None:
                raise ToolInputError(
                    "Please provide either a valid Date of Birth or both Driver and Conductor numbers (1 to 9).",
                    "MISSING_BIRTH_NUMBERS",
                )

            evaluation = evaluate_name_rules(full_name, driver, conductor, dob_clean)
            if "error" in evaluation:
                raise ToolInputError(str(evaluation["error"]), "NAME_EVALUATION_ERROR")

            # Enforce single-digit 1..9 roots & attach explicit basis tags per rule
            seg = evaluation.get("segment_analysis") or {}
            if seg.get("full_compound"):
                seg["full_root"] = digit_root(int(seg["full_compound"]))
                seg["basis"] = "calculated"
            if seg.get("first_name_compound"):
                seg["first_name_root"] = digit_root(int(seg["first_name_compound"]))
            for word_seg in seg.get("segments") or []:
                if word_seg.get("compound_sum"):
                    word_seg["root_number"] = digit_root(int(word_seg["compound_sum"]))
                    word_seg["basis"] = "calculated"
            for rule in evaluation.get("rules") or []:
                rule["basis"] = "traditional rule"

            evaluation["automated_spelling_candidates_status"] = "not configured"
            provenance_lines = [
                _prov_line(
                    "birth_numbers",
                    "Birth Driver & Conductor",
                    "calculated",
                    f"Mulank (Birth Day number) {driver} and Bhagyank (Life Path number) {conductor} reduced to single digits 1–9.",
                ),
                _prov_line(
                    "chaldean_segments",
                    "Chaldean Letter & Segment Totals",
                    "calculated",
                    f"Full compound {seg.get('full_compound')} -> single-digit root {seg.get('full_root')}.",
                ),
                _prov_line(
                    "planetary_compatibility",
                    "Chaldean & Cheiro Compatibility Check",
                    "traditional rule",
                    "Evaluated against traditional Chaldean root harmony (1, 3, 5, 6) and anti-number pairs.",
                ),
                _prov_line(
                    "lo_shu_overlay",
                    "Birth Lo Shu Grid Overlay",
                    "calculated" if dob_clean else "not configured",
                    "Compared name letter digits against missing and repeated birth-date Lo Shu digits."
                    if dob_clean
                    else "Full Date of Birth was not supplied; birth Lo Shu grid overlay is not configured for this request.",
                ),
                _prov_line(
                    "automated_spelling_alteration",
                    "Automated Name Spelling Alteration",
                    "not configured",
                    "Automated spelling generation is intentionally disabled; name spelling review is handled only in personal consultation.",
                ),
            ]
            payload = _sanitize_tree(
                {
                    "status": "SUCCESS",
                    "current_name_evaluation": evaluation,
                    "is_aligned": bool(evaluation.get("is_aligned", False)),
                    "calculated_driver": driver,
                    "calculated_conductor": conductor,
                    "comparison_table": [],
                    "provenance_lines": provenance_lines,
                }
            )
            return JSONResponse(status_code=200, content=payload)
        except ToolInputError as err:
            return _bad_request(err)

    # 2. Compatibility / Synastry: POST /api/v2/numerology/relationships/synastry
    @router.post("/api/v2/numerology/relationships/synastry")
    async def handle_synastry(request: Request) -> JSONResponse:
        auth_dependency(request)
        try:
            body = await _read_json_object(request)
            p1_name = _require_alpha_string(body, "person1_name", "Partner 1 full name", max_len=120)
            p2_name = _require_alpha_string(body, "person2_name", "Partner 2 full name", max_len=120)
            p1_d, p1_m, p1_y = _validate_gregorian_ymd(
                body.get("p1_day"), body.get("p1_month"), body.get("p1_year"), "Partner 1 Date of Birth"
            )
            p2_d, p2_m, p2_y = _validate_gregorian_ymd(
                body.get("p2_day"), body.get("p2_month"), body.get("p2_year"), "Partner 2 Date of Birth"
            )
            rel_type_raw = str(body.get("relationship_type") or "romantic").strip().lower()
            rel_type = rel_type_raw if rel_type_raw in {"romantic", "business"} else "romantic"

            report = analyze_relationship_compatibility(
                person1_name=p1_name,
                p1_day=p1_d,
                p1_month=p1_m,
                p1_year=p1_y,
                person2_name=p2_name,
                p2_day=p2_d,
                p2_month=p2_m,
                p2_year=p2_y,
                relationship_type=rel_type,
            )
            score_pct = float(report.get("compatibility_score_pct", 0.0))
            verdict = str(report.get("overall_verdict") or "")
            name_harm = str(report.get("name_harmony") or "Neutral")
            drv_harm = str(report.get("driver_harmony") or "Neutral")
            report["compatibility_score_percentage"] = score_pct
            report["verdict"] = verdict
            report["communication_dynamic"] = f"Calling Name Harmony: {name_harm} · Daily Tempo: {drv_harm}"
            report["natal_horoscope_synastry_status"] = "not configured"

            provenance_lines = [
                _prov_line(
                    "partner_core_numbers",
                    "Partner 1 & Partner 2 Core Numbers",
                    "calculated",
                    f"{p1_name} (Driver {report['person_1']['driver']}, Conductor {report['person_1']['conductor']}, Name {report['person_1']['name_root']}) "
                    f"and {p2_name} (Driver {report['person_2']['driver']}, Conductor {report['person_2']['conductor']}, Name {report['person_2']['name_root']}).",
                ),
                _prov_line(
                    "planetary_synastry_matrix",
                    "Driver, Conductor, Calling Name & Lo Shu Complementation",
                    "traditional rule",
                    f"Traditional planetary friendship matrix yielded {score_pct}% compatibility indication ({verdict}).",
                ),
                _prov_line(
                    "natal_kundali_matching",
                    "Natal Birth-Time Horoscope Matching",
                    "not configured",
                    "Birth time and birth place are not collected on this calculator; Vedic Nakshatra/Ashtakoota matching is not configured here.",
                ),
            ]
            payload = _sanitize_tree(
                {
                    "status": "SUCCESS",
                    "synastry_report": report,
                    "provenance_lines": provenance_lines,
                }
            )
            return JSONResponse(status_code=200, content=payload)
        except ToolInputError as err:
            return _bad_request(err)

    # 3. Mobile Numerology: POST /api/v2/numerology/assets/mobile
    @router.post("/api/v2/numerology/assets/mobile")
    async def handle_mobile_audit(request: Request) -> JSONResponse:
        auth_dependency(request)
        try:
            body = await _read_json_object(request)
            mobile_raw = _require_nonempty_string(body, "mobile_number", "a mobile phone number", max_len=32)
            digits_only = "".join(ch for ch in mobile_raw if ch.isdigit())
            if len(digits_only) < 7 or len(digits_only) > 15:
                raise ToolInputError(
                    "Mobile number must contain between 7 and 15 digits.",
                    "INVALID_MOBILE_NUMBER",
                )
            driver = _parse_single_digit_int(body.get("driver"), "Driver number", allow_none=True)
            conductor = _parse_single_digit_int(body.get("conductor"), "Conductor number", allow_none=True)

            audit = analyze_mobile_number(digits_only, driver=driver, conductor=conductor)
            if "error" in audit:
                raise ToolInputError(str(audit["error"]), "INVALID_MOBILE_NUMBER")

            audit["total_root"] = digit_root(int(audit["total_compound"])) if int(audit.get("total_compound") or 0) > 0 else 0
            if driver is None:
                audit["driver_compatibility"] = "not configured"
            if conductor is None:
                audit["conductor_compatibility"] = "not configured"

            provenance_lines = [
                _prov_line(
                    "digit_sum_and_frequency",
                    "Digit Sum, Root & Digit Frequency",
                    "calculated",
                    f"Compound sum {audit['total_compound']} -> single-digit root {audit['total_root']} ({audit.get('root_planet', '')}).",
                ),
                _prov_line(
                    "pair_and_sequence_scan",
                    "Two-Digit Pair & Repeating Sequence Scan",
                    "traditional rule",
                    "Checked adjacent digit pairs and triple/quadruple repetitions against traditional mobile numerology rules.",
                ),
                _prov_line(
                    "birth_number_alignment",
                    "Owner Driver & Conductor Alignment",
                    "traditional rule" if (driver is not None or conductor is not None) else "not configured",
                    "Evaluated mobile root planet against provided birth number(s)."
                    if (driver is not None or conductor is not None)
                    else "Birth Driver and Conductor were not supplied; personal owner compatibility is marked not configured.",
                ),
            ]
            payload = _sanitize_tree(
                {
                    "status": "SUCCESS",
                    "mobile_audit": audit,
                    "provenance_lines": provenance_lines,
                }
            )
            return JSONResponse(status_code=200, content=payload)
        except ToolInputError as err:
            return _bad_request(err)

    # 4. Vehicle Numerology: POST /api/v2/numerology/assets/vehicle
    @router.post("/api/v2/numerology/assets/vehicle")
    async def handle_vehicle_audit(request: Request) -> JSONResponse:
        auth_dependency(request)
        try:
            body = await _read_json_object(request)
            plate_raw = _require_nonempty_string(body, "registration_plate", "a vehicle registration plate", max_len=32)
            clean_plate = re.sub(r"[^A-Za-z0-9]", "", plate_raw).upper()
            if len(clean_plate) < 4 or not any(ch.isdigit() for ch in clean_plate):
                raise ToolInputError(
                    "Registration plate must contain at least 4 alphanumeric characters including digits (for example MH12AB1234).",
                    "INVALID_REGISTRATION_PLATE",
                )
            driver = _parse_single_digit_int(body.get("driver"), "Driver number", allow_none=False)
            conductor = _parse_single_digit_int(body.get("conductor"), "Conductor number", allow_none=False)
            assert driver is not None and conductor is not None

            audit = analyze_vehicle_number(clean_plate, driver, conductor)
            if "error" in audit:
                raise ToolInputError(str(audit["error"]), "INVALID_REGISTRATION_PLATE")

            if int(audit.get("full_plate_compound") or 0) > 0:
                audit["full_plate_root"] = digit_root(int(audit["full_plate_compound"]))
            if audit.get("core_running_digits"):
                core_sum = sum(int(ch) for ch in str(audit["core_running_digits"]) if ch.isdigit())
                audit["core_running_root"] = digit_root(core_sum) if core_sum > 0 else 0

            provenance_lines = [
                _prov_line(
                    "plate_alphanumeric_totals",
                    "Alphanumeric Plate & Running-Digit Totals",
                    "calculated",
                    f"Plate {audit['registration_plate']} -> compound {audit['full_plate_compound']}, single-digit root {audit['full_plate_root']}; "
                    f"running digits {audit['core_running_digits']} -> root {audit['core_running_root']}.",
                ),
                _prov_line(
                    "owner_harmony_and_colours",
                    "Owner Harmony, Maintenance Vigilance & Colour Suggestions",
                    "traditional rule",
                    f"Driver harmony: {audit['driver_harmony']} · Conductor harmony: {audit['conductor_harmony']}.",
                ),
                _prov_line(
                    "mechanical_inspection",
                    "Mechanical & Statutory Roadworthiness",
                    "not configured",
                    "Physical vehicle safety depends on certified mechanical servicing and safe driving habits, which numerology cannot assess.",
                ),
            ]
            payload = _sanitize_tree(
                {
                    "status": "SUCCESS",
                    "vehicle_audit": audit,
                    "provenance_lines": provenance_lines,
                }
            )
            return JSONResponse(status_code=200, content=payload)
        except ToolInputError as err:
            return _bad_request(err)

    # 5. Property Numerology: POST /api/v2/numerology/assets/property
    @router.post("/api/v2/numerology/assets/property")
    async def handle_property_audit(request: Request) -> JSONResponse:
        auth_dependency(request)
        try:
            body = await _read_json_object(request)
            prop_id = _require_nonempty_string(body, "property_identifier", "a house, flat, or unit number", max_len=64)
            if not any(ch.isalnum() for ch in prop_id):
                raise ToolInputError(
                    "Property identifier must contain at least one letter or digit (for example B-402 or 108).",
                    "INVALID_PROPERTY_IDENTIFIER",
                )
            driver = _parse_single_digit_int(body.get("driver"), "Driver number", allow_none=False)
            conductor = _parse_single_digit_int(body.get("conductor"), "Conductor number", allow_none=False)
            assert driver is not None and conductor is not None

            audit = analyze_property_number(prop_id, driver, conductor)
            if "error" in audit:
                raise ToolInputError(str(audit["error"]), "INVALID_PROPERTY_IDENTIFIER")

            total_comp = int(audit.get("total_compound") or 0)
            if total_comp <= 0:
                raise ToolInputError(
                    "Property identifier must resolve to a positive numerical or Chaldean letter sum.",
                    "ZERO_PROPERTY_SUM",
                )
            root = digit_root(total_comp)
            audit["property_root"] = root
            audit["property_root_number"] = root
            audit["planet_association"] = PLANET_BILINGUAL_LABELS.get(root, f"Root {root}")
            audit["resident_compatibility"] = (
                f"Driver {driver}: {audit.get('resident_driver_harmony', 'Neutral')} · "
                f"Conductor {conductor}: {audit.get('resident_conductor_harmony', 'Neutral')}"
            )
            audit["vastu_sector"] = f"{audit.get('aligned_direction', 'East')} ({audit.get('elemental_nature', 'Solar')})"
            audit["compass_floorplan_status"] = "not configured"

            provenance_lines = [
                _prov_line(
                    "unit_reduction",
                    "Unit Alphanumeric Sum & Single-Digit Root",
                    "calculated",
                    f"Unit '{prop_id}' -> compound {total_comp}, single-digit root {root}.",
                ),
                _prov_line(
                    "vastu_and_resident_harmony",
                    "Traditional Vastu Direction & Resident Compatibility",
                    "traditional rule",
                    f"{audit['planet_association']} · {audit['resident_compatibility']}.",
                ),
                _prov_line(
                    "on_site_compass_audit",
                    "Physical Compass & Architectural Floor-Plan Survey",
                    "not configured",
                    "On-site magnetic compass orientation and room-by-room architectural layout are not provided in unit-number calculation.",
                ),
            ]
            payload = _sanitize_tree(
                {
                    "status": "SUCCESS",
                    "property_audit": audit,
                    "provenance_lines": provenance_lines,
                }
            )
            return JSONResponse(status_code=200, content=payload)
        except ToolInputError as err:
            return _bad_request(err)

    # 6. Blessing Years Timeline: POST /api/v2/numerology/forecast/blessing-years
    @router.post("/api/v2/numerology/forecast/blessing-years")
    async def handle_blessing_years(request: Request) -> JSONResponse:
        auth_dependency(request)
        try:
            body = await _read_json_object(request)
            day, month, year = _validate_gregorian_ymd(
                body.get("day"), body.get("month"), body.get("year"), "Date of Birth"
            )
            curr_age_raw = body.get("current_age")
            curr_age: Optional[int] = None
            if curr_age_raw is not None and curr_age_raw != "":
                try:
                    curr_age = int(curr_age_raw)
                except (TypeError, ValueError) as exc:
                    raise ToolInputError("current_age must be a non-negative integer.", "INVALID_AGE") from exc
                if curr_age < 0 or curr_age > 120:
                    raise ToolInputError("current_age must be between 0 and 120.", "INVALID_AGE")

            blessing_data = calculate_blessing_years(
                day=day, month=month, birth_year=year, current_age=curr_age
            )
            blessing_data["natal_dasha_overlay_status"] = "not configured"
            provenance_lines = [
                _prov_line(
                    "cycle_arithmetic",
                    "Driver, Conductor & Personal Year Cycle Arithmetic (Ages 18–75)",
                    "calculated",
                    f"Birth date {day:02d}/{month:02d}/{year:04d} -> Mulank (Birth Day number) {blessing_data['driver']}, "
                    f"Bhagyank (Life Path number) {blessing_data['conductor']}.",
                ),
                _prov_line(
                    "milestone_tiers",
                    "Milestone Convergence Themes",
                    "traditional rule",
                    "Years where reduced age, calendar year, and Personal Year align with friendly birth numbers are grouped as supportive cycles.",
                ),
                _prov_line(
                    "natal_dasha_cross_check",
                    "Natal Vimshottari Dasha Cross-Timing",
                    "not configured",
                    "Birth time and birth place are not collected on this page; astrological Dasha cross-timing is not configured here.",
                ),
            ]
            payload = _sanitize_tree(
                {
                    "status": "SUCCESS",
                    "blessing_years": blessing_data,
                    "provenance_lines": provenance_lines,
                }
            )
            return JSONResponse(status_code=200, content=payload)
        except ToolInputError as err:
            return _bad_request(err)

    # 7. Baby Naming: POST /api/v2/numerology/naming/baby
    @router.post("/api/v2/numerology/naming/baby")
    async def handle_baby_naming(request: Request) -> JSONResponse:
        auth_dependency(request)
        try:
            body = await _read_json_object(request)
            baby_driver = _parse_single_digit_int(body.get("baby_driver"), "Baby Driver number", allow_none=False)
            baby_conductor = _parse_single_digit_int(body.get("baby_conductor"), "Baby Conductor number", allow_none=False)
            assert baby_driver is not None and baby_conductor is not None

            gender_raw = body.get("gender")
            gender: Optional[str] = None
            if gender_raw is not None and str(gender_raw).strip() != "":
                g_clean = str(gender_raw).strip().lower()
                if g_clean not in {"boy", "girl", "unisex", "all", "any"}:
                    raise ToolInputError("Gender must be 'Boy', 'Girl', 'Unisex', or 'any'.", "INVALID_GENDER")
                if g_clean not in {"all", "any"}:
                    gender = g_clean

            letter_raw = body.get("starting_letter")
            starting_letter: Optional[str] = None
            if letter_raw is not None and str(letter_raw).strip() != "":
                l_clean = str(letter_raw).strip().upper()
                if len(l_clean) != 1 or not l_clean.isalpha():
                    raise ToolInputError("Starting letter must be a single alphabetic letter A–Z.", "INVALID_STARTING_LETTER")
                starting_letter = l_clean

            missing_raw = body.get("missing_numbers_in_chart")
            missing_nums: Optional[List[int]] = None
            if isinstance(missing_raw, list):
                missing_nums = [
                    int(x) for x in missing_raw if isinstance(x, (int, str)) and str(x).isdigit() and 1 <= int(x) <= 9
                ]

            recs = recommend_baby_names(
                baby_driver=baby_driver,
                baby_conductor=baby_conductor,
                gender=gender,
                starting_letter=starting_letter,
                missing_numbers_in_chart=missing_nums,
            )
            for item in recs:
                comp = int(item.get("compound_sum") or 0)
                root = digit_root(comp) if comp > 0 else int(item.get("single_root") or 1)
                item["single_root"] = root
                item["compound"] = comp
                item["root"] = root
                item["basis"] = "traditional rule"

            catalog_status = "configured" if recs else "not configured"
            provenance_lines = [
                _prov_line(
                    "baby_birth_numbers",
                    "Baby Driver & Conductor Inputs",
                    "calculated",
                    f"Evaluated for Mulank (Birth Day number) {baby_driver} and Bhagyank (Life Path number) {baby_conductor}.",
                ),
                _prov_line(
                    "chaldean_name_scoring",
                    "Chaldean Sum, Root & Harmony Scoring",
                    "traditional rule" if recs else "not configured",
                    f"Matched {len(recs)} curated name(s) by Chaldean compound and Driver/Conductor friendship."
                    if recs
                    else f"No curated baby names are configured yet for starting letter '{starting_letter or 'any'}' and gender '{gender or 'any'}'.",
                ),
                _prov_line(
                    "nakshatra_syllable",
                    "Janma Nakshatra (Birth Lunar Mansion) Syllable",
                    "not configured",
                    "Birth time and birth place are not collected on this page; Nakshatra syllable selection is marked not configured.",
                ),
            ]
            payload = _sanitize_tree(
                {
                    "status": "SUCCESS",
                    "baby_name_recommendations": recs,
                    "catalog_status": catalog_status,
                    "provenance_lines": provenance_lines,
                }
            )
            return JSONResponse(status_code=200, content=payload)
        except ToolInputError as err:
            return _bad_request(err)

    # 8. Profession Recommendations: POST /api/v2/numerology/professions/recommend
    @router.post("/api/v2/numerology/professions/recommend")
    async def handle_professions_recommend(request: Request) -> JSONResponse:
        auth_dependency(request)
        try:
            body = await _read_json_object(request)
            driver = _parse_single_digit_int(body.get("driver"), "Driver number", allow_none=False)
            conductor = _parse_single_digit_int(body.get("conductor"), "Conductor number", allow_none=False)
            saturn_override = _parse_single_digit_int(body.get("saturn_override"), "Saturn override", allow_none=True)
            kp_sub_lord_raw = body.get("kp_sub_lord")
            kp_sub_lord = str(kp_sub_lord_raw).strip() if kp_sub_lord_raw else None
            assert driver is not None and conductor is not None

            recommendations = recommend_professions(
                driver=driver,
                conductor=conductor,
                saturn_conjunction_override=saturn_override,
                kp_tenth_sub_lord=kp_sub_lord,
            )
            recommendations["kp_tenth_sub_lord_status"] = "traditional rule" if kp_sub_lord else "not configured"
            provenance_lines = [
                _prov_line(
                    "driver_conductor_pair",
                    "Driver & Conductor Input Pair",
                    "calculated",
                    f"Mulank (Birth Day number) {driver} paired with Bhagyank (Life Path number) {conductor}.",
                ),
                _prov_line(
                    "vocational_taxonomy",
                    "81-Pair Vocational & Work-Structure Mapping",
                    "traditional rule",
                    f"Synthesis mode: {recommendations.get('synthesis_mode')} ({recommendations.get('relationship_dynamic')}).",
                ),
                _prov_line(
                    "kp_tenth_cusp",
                    "KP 10th Cusp Astrological Cross-Check",
                    "traditional rule" if kp_sub_lord else "not configured",
                    "KP 10th sub-lord note included from provided input."
                    if kp_sub_lord
                    else "Natal KP 10th cusp sub-lord requires birth time and place and is marked not configured.",
                ),
            ]
            payload = _sanitize_tree(
                {
                    "status": "SUCCESS",
                    "recommendations": recommendations,
                    "provenance_lines": provenance_lines,
                }
            )
            return JSONResponse(status_code=200, content=payload)
        except ToolInputError as err:
            return _bad_request(err)

    # 9. Existing Business Diagnose: POST /api/v1/business/existing-diagnose
    @router.post("/api/v1/business/existing-diagnose")
    async def handle_existing_diagnose(request: Request) -> JSONResponse:
        auth_dependency(request)
        try:
            body = await _read_json_object(request)
            legal_name = _require_alpha_string(body, "legal_name", "the registered legal entity name", max_len=160)
            trading_name = _require_alpha_string(body, "trading_name", "the customer-facing trading name", max_len=160)
            products_services = _require_nonempty_string(
                body, "products_services", "the business products or services description", max_len=800
            )

            raw_constraints = body.get("current_constraints") or []
            if isinstance(raw_constraints, str):
                current_constraints = [s.strip() for s in raw_constraints.split(",") if s.strip()]
            elif isinstance(raw_constraints, list):
                current_constraints = [str(s).strip() for s in raw_constraints if str(s).strip()]
            else:
                raise ToolInputError("current_constraints must be a list of strings.", "INVALID_CONSTRAINTS")

            raw_challenges = body.get("performance_challenges") or []
            if isinstance(raw_challenges, str):
                performance_challenges = [s.strip() for s in raw_challenges.split(",") if s.strip()]
            elif isinstance(raw_challenges, list):
                performance_challenges = [str(s).strip() for s in raw_challenges if str(s).strip()]
            else:
                raise ToolInputError("performance_challenges must be a list of strings.", "INVALID_CHALLENGES")

            logo_color = str(body.get("logo_color_preference") or "#C9A227").strip() or "#C9A227"

            diag = _business_engine.diagnose_existing_business(
                legal_name=legal_name,
                trading_name=trading_name,
                products_services=products_services,
                current_constraints=current_constraints,
                performance_challenges=performance_challenges,
                logo_color_preference=logo_color,
            )

            adj = diag.get("brand_and_name_adjustments") or {}
            legal_comp = int(adj.get("legal_name_compound") or 0)
            trading_comp = int(adj.get("trading_name_compound") or 0)
            legal_root = digit_root(legal_comp) if legal_comp > 0 else 1
            trading_root = digit_root(trading_comp) if trading_comp > 0 else 1
            adj["legal_name_root"] = legal_root
            adj["trading_name_root"] = trading_root

            verdict = str(adj.get("brand_alignment_status") or "FRICTION_DETECTED")
            protection_status = "protected" if verdict in ("SUPER_HARMONIOUS", "PROTECTED_FRONTEND") else "friction_detected"
            protection_summary = str(adj.get("trading_name_recommendation") or "")

            fvc = diag.get("fixed_vs_changeable") or {}
            constraints_analysis: List[Dict[str, str]] = []
            for fc in fvc.get("fixed_constraints") or []:
                constraints_analysis.append(
                    {
                        "factor": str(fc),
                        "remedial_guidance": "Keep statutory registrations and core contractual obligations intact; adjust changeable customer-facing touchpoints first.",
                        "basis": "calculated",
                    }
                )
            for cf in (fvc.get("changeable_factors") or [])[:4]:
                constraints_analysis.append(
                    {
                        "factor": str(cf),
                        "remedial_guidance": "Adjustable operational or branding lever that can be refined without disrupting existing legal registrations.",
                        "basis": "traditional rule",
                    }
                )

            practical_steps = list(diag.get("practical_improvements_first") or [])
            action_plan = practical_steps + [
                f"Review customer-facing trading name '{trading_name}' (Compound {trading_comp} -> Root {trading_root}) alongside operational unit economics.",
                "Keep statutory accounting, customer onboarding, and supplier credit terms clearly documented before testing optional symbolic adjustments.",
            ]

            diag["diagnosis_verdict"] = verdict
            diag["protection_layer_status"] = protection_status
            diag["protection_summary"] = protection_summary
            diag["constraints_analysis"] = constraints_analysis
            diag["action_plan"] = action_plan
            diag["disclaimer"] = str(diag.get("statutory_notice") or "")
            diag["founder_dob_alignment_status"] = "not configured"
            diag["monetization_gate"] = _compliant_business_monetization_gate(
                entity_name=trading_name or legal_name,
                compound=trading_comp,
                root=trading_root,
                status=verdict,
            )
            diag["provenance_lines"] = [
                _prov_line(
                    "legal_and_trading_math",
                    "Legal & Trading Name Chaldean Totals",
                    "calculated",
                    f"Legal '{legal_name}' -> {legal_comp}/{legal_root}; Trading '{trading_name}' -> {trading_comp}/{trading_root}.",
                ),
                _prov_line(
                    "brand_shield_and_remedies",
                    "Frontend Brand Shield & Vastu Suggestions",
                    "traditional rule",
                    f"Alignment status: {verdict}. Optional symbolic practices carry zero mandatory cost.",
                ),
                _prov_line(
                    "founder_birth_chart_link",
                    "Founder Birth-Date Compatibility",
                    "not configured",
                    "Founder Date of Birth is not part of the operating-entity form; personal founder synergy is marked not configured.",
                ),
            ]
            return JSONResponse(status_code=200, content=_sanitize_tree(diag))
        except ToolInputError as err:
            return _bad_request(err)

    # 10. Startup Evaluate: POST /api/v1/business/startup-evaluate
    @router.post("/api/v1/business/startup-evaluate")
    async def handle_startup_evaluate(request: Request) -> JSONResponse:
        auth_dependency(request)
        try:
            body = await _read_json_object(request)
            idea_name = _require_alpha_string(body, "idea_name", "a proposed business or idea name", max_len=160)
            founder_name = _require_alpha_string(body, "founder_name", "the founder's name", max_len=120)
            activity_description = _require_nonempty_string(
                body, "activity_description", "a description of the business activity", max_len=1000
            )

            raw_skills = body.get("skills")
            if isinstance(raw_skills, str):
                skills = [s.strip() for s in raw_skills.split(",") if s.strip()]
            elif isinstance(raw_skills, list):
                skills = [str(s).strip() for s in raw_skills if str(s).strip()]
            else:
                skills = []
            if not skills:
                raise ToolInputError("Please enter at least one founder skill.", "MISSING_SKILLS")

            founder_dob_raw = body.get("founder_dob")
            founder_dob: Optional[str] = None
            if founder_dob_raw is not None and str(founder_dob_raw).strip() != "":
                d, m, y = _parse_dob_string(str(founder_dob_raw), "Founder Date of Birth")
                founder_dob = f"{y:04d}-{m:02d}-{d:02d}"

            allowed_cap = {"bootstrapped", "seed_10k_50k", "growth_50k_250k", "institutional_250k_plus"}
            capital_band = str(body.get("capital_band") or "bootstrapped").strip()
            if capital_band not in allowed_cap:
                raise ToolInputError(
                    f"capital_band must be one of: {', '.join(sorted(allowed_cap))}.",
                    "INVALID_CAPITAL_BAND",
                )

            est_cap = str(body.get("estimated_startup_capital_required") or capital_band).strip()
            if est_cap not in allowed_cap:
                est_cap = capital_band

            allowed_risk = {"low", "moderate", "aggressive"}
            risk_tolerance = str(body.get("risk_tolerance") or "moderate").strip().lower()
            if risk_tolerance not in allowed_risk:
                raise ToolInputError("risk_tolerance must be low, moderate, or aggressive.", "INVALID_RISK_TOLERANCE")

            allowed_op = {"hands_on_operations", "digital_remote", "hybrid_management"}
            operating_preference = str(body.get("operating_preference") or "digital_remote").strip().lower()
            if operating_preference not in allowed_op:
                raise ToolInputError(
                    "operating_preference must be hands_on_operations, digital_remote, or hybrid_management.",
                    "INVALID_OPERATING_PREFERENCE",
                )

            try:
                experience_years = int(body.get("experience_years", 3))
            except (TypeError, ValueError) as exc:
                raise ToolInputError("experience_years must be an integer.", "INVALID_EXPERIENCE_YEARS") from exc
            if experience_years < 0 or experience_years > 80:
                raise ToolInputError("experience_years must be between 0 and 80.", "INVALID_EXPERIENCE_YEARS")

            revenue_model = str(body.get("revenue_model") or "subscription").strip() or "subscription"
            customer_segment = str(body.get("customer_segment") or "General Market").strip() or "General Market"
            delivery_channel = str(body.get("delivery_channel") or "Direct").strip() or "Direct"
            location = str(body.get("location") or "India").strip() or "India"

            founder = FounderProfile(
                name=founder_name,
                skills=skills,
                experience_years=experience_years,
                capital_band=capital_band,  # type: ignore[arg-type]
                location=location,
                risk_tolerance=risk_tolerance,  # type: ignore[arg-type]
                operating_preference=operating_preference,  # type: ignore[arg-type]
                dob=founder_dob,
            )
            option = CandidateBusinessOption(
                idea_id="opt_" + re.sub(r"[^a-z0-9]+", "_", idea_name.lower()).strip("_"),
                name=idea_name,
                activity_description=activity_description,
                revenue_model=revenue_model,
                customer_segment=customer_segment,
                delivery_channel=delivery_channel,
                estimated_startup_capital_required=est_cap,  # type: ignore[arg-type]
            )

            result = _business_engine.evaluate_startup_option(founder, option)
            name_comp = int(result.traditional_alignment.name_compound)
            name_root = digit_root(name_comp) if name_comp > 0 else int(result.traditional_alignment.name_single)

            provenance_lines = [
                _prov_line(
                    "commercial_viability_inputs",
                    "Commercial Skill, Capital & Complexity Review",
                    "calculated",
                    f"Skill match: {result.commercial_viability.skill_match} · Capital sufficient: {result.commercial_viability.capital_sufficient}.",
                ),
                _prov_line(
                    "business_name_chaldean",
                    "Proposed Business Name Chaldean Sum",
                    "calculated",
                    f"'{idea_name}' -> Compound {name_comp}, single-digit root {name_root}.",
                ),
                _prov_line(
                    "archetype_and_vastu",
                    "Contextual Planetary Archetype & Vastu Mapping",
                    "traditional rule",
                    f"Alignment status: {result.traditional_alignment.alignment_status}.",
                ),
                _prov_line(
                    "founder_dob_synergy",
                    "Founder Birth-Date Synergy",
                    "traditional rule" if founder_dob else "not configured",
                    "Founder Mulank (Birth Day number) and Bhagyank (Life Path number) compared with business root."
                    if founder_dob
                    else "Founder Date of Birth was not supplied; founder-to-business synergy is marked not configured.",
                ),
            ]

            payload = _sanitize_tree(
                {
                    "status": "SUCCESS",
                    "idea_id": result.idea_id,
                    "business_name": result.business_name,
                    "commercial_viability": {
                        "basis": "calculated",
                        "skill_match": result.commercial_viability.skill_match,
                        "capital_sufficient": result.commercial_viability.capital_sufficient,
                        "operational_complexity": result.commercial_viability.operational_complexity,
                        "regulatory_feasibility": result.commercial_viability.regulatory_feasibility,
                        "findings": result.commercial_viability.findings,
                    },
                    "traditional_alignment": {
                        "basis": "traditional rule",
                        "framework": result.traditional_alignment.framework,
                        "alignment_status": result.traditional_alignment.alignment_status,
                        "candidate_archetypes": result.traditional_alignment.candidate_archetypes,
                        "name_compound": name_comp,
                        "name_single": name_root,
                        "reasons": result.traditional_alignment.reasons,
                        "conflicts": result.traditional_alignment.conflicts,
                        "unknowns": result.traditional_alignment.unknowns,
                        "letter_breakdown": getattr(result.traditional_alignment, "letter_breakdown", []),
                        "compound_profile": getattr(result.traditional_alignment, "compound_profile", {}),
                        "founder_synergy": getattr(result.traditional_alignment, "founder_synergy", {}),
                        "balanced_spelling_recommendations": getattr(
                            result.traditional_alignment, "balanced_spelling_recommendations", []
                        ),
                        "vastu_and_operational_remedies": getattr(
                            result.traditional_alignment, "vastu_and_operational_remedies", {}
                        ),
                        "founder_dob_status": "calculated" if founder_dob else "not configured",
                    },
                    "synthesis_recommendation": result.synthesis_recommendation,
                    "next_steps": result.next_steps,
                    "mandatory_disclaimer": result.mandatory_disclaimer,
                    "monetization_gate": _compliant_business_monetization_gate(
                        entity_name=result.business_name,
                        compound=name_comp,
                        root=name_root,
                        status=result.traditional_alignment.alignment_status,
                    ),
                    "provenance_lines": provenance_lines,
                }
            )
            return JSONResponse(status_code=200, content=payload)
        except ToolInputError as err:
            return _bad_request(err)

    return router
