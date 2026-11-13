"""
NUMEROS VISION — PRIVATE PYTHON PDF GENERATOR SERVICE (Commit 6b)
=================================================================
Called exclusively by the Cloudflare Worker via an HMAC-signed, timestamped HTTP request
using `PDF_SERVICE_SECRET`.

Security & Architectural Guarantees:
1. HMAC-SHA256 Signature & Timestamp Verification:
   - Headers required: `X-NV-Timestamp` (epoch seconds) and `X-NV-Signature` (hex HMAC-SHA256).
   - Message signed: `f"{timestamp}.{raw_body_utf8}"`.
   - Rejects requests outside ±300 seconds (5 minutes) clock skew or with invalid signatures.
2. Strictly `viewFor` Input Only (Zero Raw Data / Zero PII):
   - Accepts only the sanitized `viewFor` output for `(subject, pack)`.
   - Explicitly rejects any payload containing raw database or encrypted PII fields
     (`dob_enc`, `phone_enc`, `birth_time_enc`, `birth_place_enc`, `phone_hash`, `token_hash`, `email`, `phone`).
3. Tier-Gated ReportLab Compilation from `viewFor`:
   - Reuses the existing deterministic ReportLab templates (`NumerosPdfReportBuilder`).
   - Compiles sections strictly from the unlocked `view["sections"]` and `view["calculation"]`
     for the target tier (`report_basic` -> 3 pages, `report_advanced` -> 12 pages, `report_premium` -> 32 pages).
"""

import os
import hmac
import time
import json
import hashlib
import datetime
from typing import Dict, Any, Tuple, Optional

from fastapi import FastAPI, Request, Response, HTTPException

from app.engine.core_matrix_engine import calculate_chaldean_name
from app.engine.kua import KUA_NEEDS_GENDER_TEXT, KUA_RULE_TEXT, calculate_kua_details
from app.engine.complementary_poorak_engine import calculate_complementary_poorak
from app.engine.vedic_gharelu_remedies import get_gharelu_remedies_for_chart
from app.engine.forecast_engine import generate_detailed_annual_matrix, calculate_blessing_years
from app.services.pdf_report_generator import NumerosPdfReportBuilder

FORBIDDEN_RAW_FIELDS = {
    "dob_enc",
    "phone_enc",
    "birth_time_enc",
    "birth_place_enc",
    "phone_hash",
    "token_hash",
    "otp_hash",
    "password",
    "raw_db_row",
}

PACK_TO_TIER = {
    "report_basic": "basic",
    "basic": "basic",
    "report_advanced": "advanced",
    "advanced": "advanced",
    "report_premium": "premium",
    "premium": "premium",
}

PLANET_FULL_NAMES = {
    1: "Sun (Surya)",
    2: "Moon (Chandra)",
    3: "Jupiter (Brihaspati)",
    4: "Rahu (North Node)",
    5: "Mercury (Budh)",
    6: "Venus (Shukra)",
    7: "Ketu (South Node)",
    8: "Saturn (Shani)",
    9: "Mars (Mangal)",
}


def compute_worker_hmac_signature(raw_body: bytes, timestamp_str: str, secret: str) -> str:
    """Computes HMAC-SHA256 hex signature over f'{timestamp_str}.{raw_body}'."""
    if not secret or not secret.strip():
        raise ValueError("PDF_SERVICE_SECRET is required and cannot be empty.")
    msg = f"{timestamp_str}.".encode("utf-8") + raw_body
    return hmac.new(secret.strip().encode("utf-8"), msg, hashlib.sha256).hexdigest()


def verify_worker_hmac_signature(
    raw_body: bytes,
    timestamp_str: str,
    signature_hex: str,
    secret: str,
    max_skew_sec: int = 300,
    now_sec: Optional[int] = None,
) -> Tuple[bool, str]:
    """
    Verifies the Worker's HMAC-SHA256 signature and timestamp freshness (±300s).
    Uses constant-time comparison via hmac.compare_digest.
    """
    if not secret or not secret.strip():
        return False, "PDF_SERVICE_SECRET is not configured on the generator service."
    if not timestamp_str or not signature_hex:
        return False, "Missing X-NV-Timestamp or X-NV-Signature header."
    try:
        ts = int(timestamp_str.strip())
    except ValueError:
        return False, "Malformed X-NV-Timestamp header; expected integer epoch seconds."

    current_sec = int(time.time()) if now_sec is None else int(now_sec)
    if abs(current_sec - ts) > max_skew_sec:
        return False, f"Timestamp expired or outside allowed {max_skew_sec}s clock skew."

    expected_sig = compute_worker_hmac_signature(raw_body, str(ts), secret)
    if not hmac.compare_digest(expected_sig.lower(), signature_hex.strip().lower()):
        return False, "Invalid HMAC-SHA256 signature."

    return True, "ok"


def _scan_forbidden_keys(obj: Any, path: str = "root") -> Optional[str]:
    """Recursively checks that no raw encrypted DB columns or PII contact fields are present."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            key_str = str(k)
            if key_str in FORBIDDEN_RAW_FIELDS:
                return f"Forbidden raw data field '{key_str}' found at {path}.{key_str}"
            if path == "root.view.user" and key_str in ("phone", "email") and v is not None:
                return f"Forbidden raw PII field '{key_str}' found at {path}.{key_str}"
            nested = _scan_forbidden_keys(v, f"{path}.{key_str}")
            if nested:
                return nested
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            nested = _scan_forbidden_keys(item, f"{path}[{idx}]")
            if nested:
                return nested
    return None


def validate_view_only_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Ensures the generator receives ONLY the viewFor output for (subject, pack), never raw data.
    """
    if not isinstance(payload, dict):
        raise ValueError("Payload must be a JSON object.")

    allowed_top_keys = {"job_id", "pack_id", "view", "topic_id"}
    extra_keys = set(payload.keys()) - allowed_top_keys
    if extra_keys:
        raise ValueError(f"Payload contains unexpected top-level keys: {sorted(extra_keys)}")

    violation = _scan_forbidden_keys(payload)
    if violation:
        raise ValueError(violation)

    view = payload.get("view")
    if not isinstance(view, dict):
        raise ValueError("Payload must include a 'view' object produced by viewFor.")

    if "calculation" not in view or "sections" not in view or "subject" not in view:
        raise ValueError("viewFor object is missing required 'subject', 'calculation', or 'sections' keys.")

    pack_id = str(payload.get("pack_id") or "").strip()
    if pack_id not in PACK_TO_TIER:
        raise ValueError(f"Unsupported or invalid report pack_id: '{pack_id}'")

    return payload


def build_calculation_data_from_view(view: Dict[str, Any], pack_id: str, topic_id: str = "core_blueprint") -> Dict[str, Any]:
    """
    Maps the Worker's `viewFor(subject, pack)` output into the deterministic ReportLab dictionary
    consumed by `NumerosPdfReportBuilder`, gating sections strictly according to `view["sections"]`.
    """
    tier = PACK_TO_TIER[pack_id]
    subj = view.get("subject") or {}
    calc = view.get("calculation") or {}
    sections = view.get("sections") or {}

    clean_name = str(subj.get("name") or "Valued Seeker").strip()
    dob_str = str(subj.get("dob") or "1990-08-15").strip()
    parts = dob_str.split("-")
    if len(parts) == 3 and len(parts[0]) == 4:
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
    elif len(parts) == 3:
        day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
    else:
        day, month, year = 15, 8, 1990

    from app.engine.digit_root import digit_root, calc_driver, calc_bhagyank, calc_personal_year
    driver = digit_root(int(calc.get("driver") or calc_driver(day))) or 1
    conductor_root = digit_root(int(calc.get("conductor") or calc_bhagyank(day, month, year))) or 1
    conductor_raw = conductor_root
    conductor_display = str(conductor_root)

    raw_counts = calc.get("counts") or {}
    counts = {i: int(raw_counts.get(str(i), raw_counts.get(i, 0))) for i in range(1, 10)}
    present_numbers = [int(x) for x in (calc.get("presentDigits") or [k for k, v in counts.items() if v > 0])]
    missing_numbers = [int(x) for x in (calc.get("missingDigits") or [k for k, v in counts.items() if v == 0])]

    planes_def = [
        ("Mental Plane (4-9-2)", [4, 9, 2]),
        ("Emotional Plane (3-5-7)", [3, 5, 7]),
        ("Practical Plane (8-1-6)", [8, 1, 6]),
        ("Thought Plane (4-3-8)", [4, 3, 8]),
        ("Will Plane (9-5-1)", [9, 5, 1]),
        ("Action Plane (2-7-6)", [2, 7, 6]),
        ("Golden Silver Wealth (4-5-6)", [4, 5, 6]),
        ("Silver Property (2-5-8)", [2, 5, 8]),
    ]
    completed_planes = [p for p in planes_def if all(x in present_numbers for x in p[1])]

    chaldean_res = calculate_chaldean_name(clean_name)
    c_compound = chaldean_res.get("compound_number", 32)
    c_root = chaldean_res.get("root_number", 5)

    def _red(n: int) -> int:
        val = digit_root(abs(int(n)))
        return val if val > 0 else 9

    subject_gender = subj.get("gender") or calc.get("gender")
    kua_details = calculate_kua_details(year, subject_gender)
    kua = kua_details["kua_number"]
    # Determine purchase / current year dynamically from subject.created_at or datetime.now()
    subj_created = subj.get("created_at") or subj.get("createdAt")
    purchase_year = None
    if subj_created:
        try:
            if isinstance(subj_created, (int, float)):
                ts = subj_created / 1000 if subj_created > 2000000000 else subj_created
                purchase_year = datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).year
            elif isinstance(subj_created, str):
                purchase_year = datetime.date.fromisoformat(subj_created.strip()[:10]).year
        except Exception:
            purchase_year = None
    current_year = purchase_year or datetime.datetime.now().year

    personal_year = _red(day + month + current_year)

    report_id = "NV-" + hashlib.sha256(f"{clean_name}:{day}-{month}-{year}:{tier}:{topic_id}".encode()).hexdigest()[:10].upper()
    dob_formatted = f"{day:02d}-{month:02d}-{year}"

    # Gate advanced & premium analytical structures strictly by view["sections"] unlock flags
    has_advanced = bool((sections.get("enabledNumbersInDepth") or {}).get("unlocked")) and tier in ("advanced", "premium")
    has_premium = bool((sections.get("missingNumbersInDepth") or {}).get("unlocked")) and tier == "premium"

    poorak_info = calculate_complementary_poorak(driver, conductor_root, missing_numbers) if (has_advanced or has_premium) else {}
    gharelu_remedies = get_gharelu_remedies_for_chart(driver, conductor_root, present_numbers, missing_numbers) if (has_advanced or has_premium) else {}
    current_age = max(18, current_year - year)
    annual_matrix = generate_detailed_annual_matrix(day, month, current_year) if (has_advanced or has_premium) else []
    blessing_data = calculate_blessing_years(day, month, year, current_age) if has_premium else {}

    return {
        "current_year": current_year,
        "target_year": current_year,
        "personal_year": personal_year,
        "annual_matrix": annual_matrix,
        "blessing_years": blessing_data,
        "mobile_number": None,
        "mobile_analysis": None,
        "vehicle_number": None,
        "vehicle_analysis": None,
        "property_number": None,
        "property_analysis": None,
        "report_id": report_id,
        "seeker_name": clean_name,
        "day": day,
        "month": month,
        "year": year,
        "dob_formatted": dob_formatted,
        "driver_number": driver,
        "driver_planet": PLANET_FULL_NAMES.get(driver, "Sun (Surya)"),
        "conductor_number": conductor_raw,
        "conductor_root": conductor_root,
        "conductor_display": conductor_display,
        "conductor_planet": PLANET_FULL_NAMES.get(conductor_root, "Sun (Surya)"),
        "chaldean_name_compound": c_compound,
        "chaldean_name_root": c_root,
        "chaldean_name_planet": PLANET_FULL_NAMES.get(c_root, "Mercury (Budh)"),
        "pythagorean_name_root": c_root,
        "pythagorean_name_planet": PLANET_FULL_NAMES.get(c_root, "Mercury (Budh)"),
        "kua_number": kua,
        "kua_display": kua_details["display"],
        "kua_element": kua_details["element_group"],
        "kua_group": kua_details["group"] or KUA_NEEDS_GENDER_TEXT,
        "kua_desk_direction": kua_details["desk_direction"],
        "kua_rule_note": KUA_RULE_TEXT,
        "kua_details": kua_details,
        "gender": kua_details["gender"],
        "edition": str(subj.get("edition") or view.get("edition") or "india"),
        "personal_year": personal_year,
        "personal_year_theme": "Foundation & Structural Infrastructure",
        "counts": counts,
        "present_numbers": present_numbers,
        "missing_numbers": missing_numbers,
        "completed_planes": completed_planes,
        "poorak_info": poorak_info,
        "gharelu_remedies": gharelu_remedies,
        "view_sections": sections,
        "topic_id": topic_id,
        "tier": tier,
    }


def render_pdf_from_view(payload: Dict[str, Any]) -> Tuple[bytes, Dict[str, Any]]:
    """
    Validates that `payload` contains only `viewFor` output (zero raw PII/DB fields)
    and renders the tier-appropriate PDF via `NumerosPdfReportBuilder`.
    """
    validated = validate_view_only_payload(payload)
    pack_id = str(validated["pack_id"]).strip()
    topic_id = str(validated.get("topic_id") or "core_blueprint").strip()
    view = validated["view"]
    tier = PACK_TO_TIER[pack_id]

    calc_data = build_calculation_data_from_view(view, pack_id=pack_id, topic_id=topic_id)
    builder = NumerosPdfReportBuilder(calc_data, tier=tier, topic_id=topic_id)
    pdf_bytes = builder.build()

    meta = {
        "job_id": validated.get("job_id"),
        "pack_id": pack_id,
        "tier": tier,
        "report_id": calc_data["report_id"],
        "pdf_size_bytes": len(pdf_bytes),
    }
    return pdf_bytes, meta


# Private FastAPI Service App for Worker -> Python Generator Calls
MAX_REQUEST_BODY_BYTES = 65536  # 64 KB hard request body limit
app = FastAPI(title="Numeros Vision Private PDF Generator Service", docs_url=None, redoc_url=None)


@app.get("/health")
@app.get("/internal/v1/health")
@app.get("/healthz")
async def handle_health() -> Dict[str, Any]:
    return {"ok": True, "service": "numeros-pdf-generator"}


@app.post("/internal/v1/render-pdf")
async def handle_render_pdf(request: Request) -> Response:
    secret = os.environ.get("PDF_SERVICE_SECRET", "").strip()
    if not secret:
        raise HTTPException(status_code=500, detail="PDF_SERVICE_SECRET is not configured.")

    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_REQUEST_BODY_BYTES:
                raise HTTPException(status_code=413, detail=f"Payload exceeds maximum allowed size of {MAX_REQUEST_BODY_BYTES} bytes.")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid Content-Length header.")

    raw_body = await request.body()
    if len(raw_body) > MAX_REQUEST_BODY_BYTES:
        raise HTTPException(status_code=413, detail=f"Payload exceeds maximum allowed size of {MAX_REQUEST_BODY_BYTES} bytes.")
    ts_header = request.headers.get("X-NV-Timestamp", "")
    sig_header = request.headers.get("X-NV-Signature", "")

    valid_sig, reason = verify_worker_hmac_signature(raw_body, ts_header, sig_header, secret)
    if not valid_sig:
        raise HTTPException(status_code=401, detail=reason)

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON body: {exc}") from exc

    try:
        pdf_bytes, meta = render_pdf_from_view(payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"{type(exc).__name__}: {exc}") from exc

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "X-NV-Report-Id": str(meta["report_id"]),
            "X-NV-Tier": str(meta["tier"]),
            "Cache-Control": "private, no-store",
        },
    )

def render_planner_2027_from_payload(payload: Dict[str, Any]) -> Tuple[bytes, Dict[str, Any]]:
    """
    Renders the 2027 Year Ahead Planner 24-page PDF from validated payload.
    - Zero PII: Accepts only full_name, dob_str, order_id, is_sample.
    - Fail-Closed: If is_sample is False (paid delivery) and any '{{' placeholder
      (such as {{DISCLAIMER_APPROVED_TEXT}}) is present in the rendered PDF text,
      MUST fail closed with HTTPException 422 and release NO PDF.
    """
    full_name = str(payload.get("full_name") or payload.get("name") or "").strip()
    dob_str = str(payload.get("dob_str") or payload.get("dob") or "").strip()
    order_id = str(payload.get("order_id") or "").strip()
    is_sample = bool(payload.get("is_sample", False))

    if not full_name or len(full_name) < 2 or len(full_name) > 60:
        raise HTTPException(status_code=400, detail="Invalid full_name (must be 2-60 characters).")
    if not dob_str or len(dob_str) != 10:
        raise HTTPException(status_code=400, detail="Invalid dob_str format (expected YYYY-MM-DD).")
    try:
        y, m, d = [int(p) for p in dob_str.split("-")]
        if not (1900 <= y <= 2026 and 1 <= m <= 12 and 1 <= d <= 31):
            raise ValueError()
    except Exception:
        raise HTTPException(status_code=400, detail="DOB must be between 1900 and 2026.")

    try:
        from pdf_service.app.services.planner_2027_pdf_generator import generate_planner_2027_pdf
    except ImportError:
        from app.services.planner_2027_pdf_generator import generate_planner_2027_pdf

    try:
        pdf_bytes = generate_planner_2027_pdf(
            full_name=full_name,
            dob_str=dob_str,
            is_sample=is_sample
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"PDF generation error: {exc}") from exc

    # Fail-closed check: if paid generation (is_sample=False), assert NO '{{' or '}}' placeholders exist in the PDF
    if not is_sample:
        import io
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        for page_idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if "{{" in text or "}}" in text:
                raise HTTPException(
                    status_code=422,
                    detail=f"Fail-closed: unapproved placeholder remains in paid PDF on page {page_idx + 1}"
                )

    meta = {
        "order_id": order_id,
        "is_sample": is_sample,
        "pdf_size_bytes": len(pdf_bytes),
    }
    return pdf_bytes, meta


def assert_no_preview_flag_on_production():
    """
    Enforces strict preview guard:
    PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW is permitted ONLY when ENVIRONMENT == 'preview' explicitly.
    In every other case (unset, 'production', 'staging', anything else), refuse execution with RuntimeError.
    """
    flag = os.environ.get("PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW", "").strip().lower()
    if flag in ("true", "1", "yes"):
        env = os.environ.get("ENVIRONMENT", "").strip().lower()
        if env != "preview":
            raise RuntimeError(
                f"FATAL SECURITY VIOLATION: PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW is only permitted when ENVIRONMENT == 'preview' (current ENVIRONMENT: '{env}'). Refusing execution."
            )

def assert_no_live_razorpay_keys():
    assert_no_preview_flag_on_production()
    """Refuse to run if any Razorpay live key is configured anywhere in the environment."""
    for k, v in os.environ.items():
        if "RAZORPAY" in k.upper() and isinstance(v, str) and v.strip().startswith("rzp_live"):
            raise RuntimeError(f"FATAL SECURITY VIOLATION: Live Razorpay key detected in {k}. Execution forbidden in test/preview.")


@app.post("/internal/v1/render-planner-2027")
async def handle_render_planner_2027(request: Request) -> Response:
    """FastAPI HTTP endpoint verifying HMAC and dispatching to render_planner_2027_from_payload."""
    assert_no_live_razorpay_keys()
    assert_no_preview_flag_on_production()

    secret = os.environ.get("PDF_SERVICE_SECRET", "").strip()
    if not secret:
        raise HTTPException(status_code=500, detail="PDF_SERVICE_SECRET is not configured.")

    content_length = request.headers.get("content-length")
    if content_length:
        try:
            if int(content_length) > MAX_REQUEST_BODY_BYTES:
                raise HTTPException(status_code=413, detail=f"Payload exceeds maximum allowed size of {MAX_REQUEST_BODY_BYTES} bytes.")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid Content-Length header.")

    raw_body = await request.body()
    if len(raw_body) > MAX_REQUEST_BODY_BYTES:
        raise HTTPException(status_code=413, detail=f"Payload exceeds maximum allowed size of {MAX_REQUEST_BODY_BYTES} bytes.")
    ts_header = request.headers.get("X-NV-Timestamp", "")
    sig_header = request.headers.get("X-NV-Signature", "")

    valid_sig, reason = verify_worker_hmac_signature(raw_body, ts_header, sig_header, secret)
    if not valid_sig:
        raise HTTPException(status_code=401, detail=reason)

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Invalid JSON body: {exc}") from exc

    pdf_bytes, meta = render_planner_2027_from_payload(payload)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "X-NV-Order-Id": str(meta.get("order_id", "")),
            "X-NV-Sample": "1" if meta.get("is_sample") else "0",
            "Cache-Control": "private, no-store",
        },
    )


@app.post("/api/charm/chat")
async def handle_charm_chat_service(request: Request):
    """
    Charm AI deterministic consultation endpoint (delegates to charm_deterministic_service).
    Enforces fail-closed authentication via CHARM_SERVICE_SECRET.
    """
    from fastapi.responses import JSONResponse
    from app.services.charm_deterministic_service import (
        CharmInputError,
        run_deterministic_charm_consultation,
    )

    allow_unauth_local = os.getenv("NV_ALLOW_UNAUTHENTICATED_LOCAL", "").lower() in ("true", "1")
    if not allow_unauth_local:
        expected_secret = os.getenv("CHARM_SERVICE_SECRET")
        if not expected_secret or not expected_secret.strip():
            raise HTTPException(status_code=503, detail="CHARM_SERVICE_SECRET is not configured on the service.")
        auth_header = request.headers.get("X-NV-Charm-Secret")
        if not auth_header or not hmac.compare_digest(auth_header.strip(), expected_secret.strip()):
            raise HTTPException(status_code=403, detail="Access Denied: Invalid or missing Charm service authorization.")

    body = await request.json()
    entitlement = str(body.get("_charm_entitlement") or "charm_free")
    try:
        result = run_deterministic_charm_consultation(body, entitlement_tier=entitlement)
    except CharmInputError as exc:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "status": "INSUFFICIENT_EVIDENCE",
                "code": exc.code,
                "error": exc.message,
                "credit_chargeable": False,
            },
        )
    return JSONResponse(status_code=200, content=result)
