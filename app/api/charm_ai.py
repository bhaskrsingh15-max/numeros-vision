"""
app/api/charm_ai.py
===================
Production-Grade API Router for Charm AI.
Complies with Section 7 and 9 of Master Specification & Rectification Instructions:
- Per-visitor anonymous identity via HttpOnly `nv_visitor_id` cookie (never literal 'guest_user').
- Server-side 3 free credits/day per visitor + IP rate-limit backup.
- Credits deducted ONLY AFTER a successful `ANSWERED` response (never on missing DOB, unsupported topic, or error).
- Zero default profile ('Seeker' or 15/8/1990).
"""

from fastapi import APIRouter, HTTPException, Request, Response, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime, timezone
import hashlib
import hmac
import os
import secrets
import time
import threading

from app.charm.chat.response_composer import charm_chat_orchestrator, CharmChatResponse
from app.charm.outcomes.outcome_service import outcome_service
from app.api.auth import api_get_current_user

router = APIRouter(prefix="/api/charm", tags=["Charm AI Core"])

FREE_DAILY_LIMIT = 3
IP_DAILY_BACKUP_LIMIT = 15
IP_MINUTE_BURST_LIMIT = 8

_VISITOR_CREDIT_LOCK = threading.Lock()
# Key: (visitor_hash, utc_date_str) -> int questions_used
_VISITOR_DAILY_USAGE: Dict[Tuple[str, str], int] = {}
# Key: (ip_hash, utc_date_str) -> int questions_used
_IP_DAILY_USAGE: Dict[Tuple[str, str], int] = {}
# Key: (ip_hash, epoch_minute) -> int requests
_IP_BURST_USAGE: Dict[Tuple[str, int], int] = {}


def reset_charm_usage_ledgers_for_tests() -> None:
    """Test helper to reset in-memory visitor and IP usage counters."""
    with _VISITOR_CREDIT_LOCK:
        _VISITOR_DAILY_USAGE.clear()
        _IP_DAILY_USAGE.clear()
        _IP_BURST_USAGE.clear()


def _utc_day_key() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _hash_identifier(raw_val: str) -> str:
    salt = os.getenv("IP_HASH_SALT", "nv-charm-visitor-salt-v1")
    return hashlib.sha256(f"{raw_val}:{salt}".encode("utf-8")).hexdigest()[:32]


def _extract_client_ip(request: Request) -> str:
    cf_ip = request.headers.get("CF-Connecting-IP")
    if cf_ip and cf_ip.strip():
        return cf_ip.strip()
    xff = request.headers.get("X-Forwarded-For")
    if xff and xff.strip():
        return xff.split(",")[0].strip()
    if request.client and request.client.host:
        return request.client.host
    return "127.0.0.1"


def resolve_or_create_visitor_identity(request: Request) -> Tuple[str, str, bool]:
    """
    Returns (visitor_cookie_id, visitor_hash, is_new_cookie).
    Never returns literal 'guest_user'.
    """
    cookie_val = (request.cookies.get("nv_visitor_id") or "").strip()
    header_val = (request.headers.get("X-NV-Visitor-Hash") or "").strip()
    if header_val and len(header_val) >= 16:
        return cookie_val or f"vis_edge_{header_val[:12]}", header_val[:32], False
    if cookie_val and cookie_val.startswith("vis_") and 12 <= len(cookie_val) <= 80:
        return cookie_val, _hash_identifier(cookie_val), False
    new_id = f"vis_{int(time.time())}_{secrets.token_hex(8)}"
    return new_id, _hash_identifier(new_id), True


def _attach_visitor_cookie(response: Response, visitor_id: str, is_new: bool) -> None:
    if is_new and visitor_id.startswith("vis_"):
        is_prod = os.getenv("ENVIRONMENT", "").lower() == "production"
        response.set_cookie(
            key="nv_visitor_id",
            value=visitor_id,
            max_age=365 * 24 * 3600,
            path="/",
            httponly=True,
            samesite="lax",
            secure=is_prod,
        )


def verify_charm_service_auth(request: Request):
    """
    Authenticates requests to Charm AI service / Gemini backend.
    Fails closed in EVERY environment (production, preview, staging, or unset ENVIRONMENT).
    The ONLY exception is when an explicit local/test bypass flag is set:
    NV_ALLOW_UNAUTHENTICATED_LOCAL=true (strictly never set on Cloud Run or deployed environments).
    """
    allow_unauth_local = os.getenv("NV_ALLOW_UNAUTHENTICATED_LOCAL", "").lower() in ("true", "1")
    if allow_unauth_local:
        return

    expected_secret = os.getenv("CHARM_SERVICE_SECRET")
    if not expected_secret or not expected_secret.strip():
        raise HTTPException(
            status_code=503,
            detail="CHARM_SERVICE_SECRET is not configured on the service."
        )

    auth_header = request.headers.get("X-NV-Charm-Secret")
    if not auth_header or not hmac.compare_digest(auth_header.strip(), expected_secret.strip()):
        raise HTTPException(
            status_code=403,
            detail="Access Denied: Invalid or missing Charm service authorization."
        )


async def get_current_user_optional(request: Request) -> Dict[str, Any]:
    """Extracts authenticated user session or resolves unique anonymous visitor ID."""
    try:
        user_info = await api_get_current_user(request)
        if isinstance(user_info, dict) and user_info.get("authenticated") and user_info.get("user_id"):
            return user_info
    except Exception:
        pass
    vis_id, vis_hash, is_new = resolve_or_create_visitor_identity(request)
    return {
        "authenticated": False,
        "user_id": f"anon_{vis_hash[:16]}",
        "visitor_id": vis_id,
        "visitor_hash": vis_hash,
        "is_new_visitor": is_new,
    }


class CharmChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: Optional[str] = Field(default="", description="User question or inquiry")
    question: Optional[str] = Field(default=None, description="Alternative key for message")
    user_intent: Optional[str] = Field(default=None, description="e.g. new_job_or_senior_role, promotion")
    forecast_horizon: Optional[str] = Field(default=None, description="e.g. 6_months, 12_months")
    name: Optional[str] = ""
    dob: Optional[str] = None  # Format: YYYY-MM-DD or DD/MM/YYYY
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None
    tob: Optional[str] = None
    pob: Optional[str] = None
    city: Optional[str] = None
    loshu_grid: Optional[Dict[str, Any]] = None
    profile_id: Optional[str] = None
    locale: str = "en-IN"
    requested_calculation_systems: Optional[List[str]] = None
    approved_ruleset_version: Optional[str] = "2.1.0"
    consent: Optional[Dict[str, bool]] = Field(default_factory=lambda: {
        "use_profile_for_calculation": True,
        "save_outcome_followups": False
    })


class OutcomeSubmissionRequest(BaseModel):
    prediction_id: str
    outcome_status: str = Field(..., description="OCCURRED_WITHIN_WINDOW, OCCURRED_LATER, DID_NOT_OCCUR_WITHIN_WINDOW, UNSURE, DECLINED")
    user_comment: Optional[str] = None


class FollowupQuestionRequest(BaseModel):
    prediction_id: str
    message: str


def _parse_dob_fields(dob_raw: Optional[str], d: Optional[int], m: Optional[int], y: Optional[int]) -> Tuple[Optional[int], Optional[int], Optional[int]]:
    if d and m and y:
        if 1 <= int(d) <= 31 and 1 <= int(m) <= 12 and 1900 <= int(y) <= 2100:
            return int(d), int(m), int(y)
        return None, None, None
    if dob_raw:
        cleaned = dob_raw.strip().replace("/", "-").replace(".", "-")
        parts = cleaned.split("-")
        if len(parts) == 3:
            try:
                if len(parts[0]) == 4:
                    yr, mo, dy = int(parts[0]), int(parts[1]), int(parts[2])
                else:
                    dy, mo, yr = int(parts[0]), int(parts[1]), int(parts[2])
                if 1 <= dy <= 31 and 1 <= mo <= 12 and 1900 <= yr <= 2100:
                    return dy, mo, yr
            except ValueError:
                pass
    return None, None, None


@router.get("/credits")
async def get_charm_credits(request: Request, response: Response, current_user=Depends(get_current_user_optional)):
    vis_id = current_user.get("visitor_id", "")
    vis_hash = current_user.get("visitor_hash") or _hash_identifier(current_user.get("user_id", "anon"))
    is_new = bool(current_user.get("is_new_visitor"))
    day_key = _utc_day_key()
    with _VISITOR_CREDIT_LOCK:
        used = _VISITOR_DAILY_USAGE.get((vis_hash, day_key), 0)
    remaining = max(0, FREE_DAILY_LIMIT - used)
    _attach_visitor_cookie(response, vis_id, is_new)
    return {
        "success": True,
        "authenticated": bool(current_user.get("authenticated")),
        "free_daily_limit": FREE_DAILY_LIMIT,
        "questions_used_today": used,
        "credits_remaining": remaining,
    }


@router.post("/chat")
async def charm_chat_endpoint(
    req: CharmChatRequest,
    request: Request,
    response: Response,
    current_user=Depends(get_current_user_optional),
    _auth=Depends(verify_charm_service_auth),
):
    """
    Main conversational turn for Charm AI.
    - Enforces per-visitor daily credit cap (3/day) + IP rate-limit backup when not already metered at edge.
    - Deducts a credit ONLY AFTER a successful `ANSWERED` response.
    - Never defaults to 'Seeker' or 15/8/1990.
    """
    user_id = current_user.get("user_id") or "anon_visitor"
    vis_id = current_user.get("visitor_id", "")
    vis_hash = current_user.get("visitor_hash") or _hash_identifier(user_id)
    is_new_vis = bool(current_user.get("is_new_visitor"))

    edge_metered = request.headers.get("X-NV-Upstream-Metered") == "1"
    day_key = _utc_day_key()
    ip_hash = _hash_identifier(_extract_client_ip(request))
    minute_bucket = int(time.time() // 60)

    # Pre-check burst & daily credit limits BEFORE computing (deduction happens ONLY AFTER success)
    if not edge_metered:
        with _VISITOR_CREDIT_LOCK:
            burst_used = _IP_BURST_USAGE.get((ip_hash, minute_bucket), 0)
            if burst_used >= IP_MINUTE_BURST_LIMIT:
                err_resp = JSONResponse(
                    status_code=429,
                    content={
                        "success": False,
                        "code": "RATE_LIMIT_EXCEEDED",
                        "error": "Too many requests from this network. Please wait a minute and try again.",
                        "credits_remaining": max(0, FREE_DAILY_LIMIT - _VISITOR_DAILY_USAGE.get((vis_hash, day_key), 0)),
                    },
                )
                _attach_visitor_cookie(err_resp, vis_id, is_new_vis)
                return err_resp

            vis_used = _VISITOR_DAILY_USAGE.get((vis_hash, day_key), 0)
            ip_used = _IP_DAILY_USAGE.get((ip_hash, day_key), 0)
            if vis_used >= FREE_DAILY_LIMIT or ip_used >= IP_DAILY_BACKUP_LIMIT:
                limit_resp = JSONResponse(
                    status_code=402,
                    content={
                        "success": False,
                        "code": "FREE_CREDITS_EXHAUSTED",
                        "status": "PAYWALL_REQUIRED",
                        "error": "You have used all 3 free Charm AI questions for today.",
                        "credits_remaining": 0,
                        "free_daily_limit": FREE_DAILY_LIMIT,
                        "upgrade_offer": {
                            "pack_id": "charm_single",
                            "name": "Charm AI Starter Pack · 5 Questions",
                            "price_inr": 199,
                            "cta_label": "Unlock 5 Questions · ₹199",
                            "report_pack_id": "report_basic",
                            "report_cta_label": "Anveil my alignments (3-Page PDF)",
                        },
                    },
                )
                _attach_visitor_cookie(limit_resp, vis_id, is_new_vis)
                return limit_resp

    msg = (req.message or req.question or "").strip()
    if not msg:
        with _VISITOR_CREDIT_LOCK:
            rem = max(0, FREE_DAILY_LIMIT - _VISITOR_DAILY_USAGE.get((vis_hash, day_key), 0))
        bad_resp = JSONResponse(
            status_code=400,
            content={
                "success": False,
                "code": "QUESTION_REQUIRED",
                "error": "Please enter a question for Charm AI.",
                "credits_remaining": rem,
            },
        )
        _attach_visitor_cookie(bad_resp, vis_id, is_new_vis)
        return bad_resp

    d, m, y = _parse_dob_fields(req.dob, req.day, req.month, req.year)
    clean_name = (req.name or "").strip()
    if clean_name.lower() == "seeker":
        clean_name = ""

    chat_res: CharmChatResponse = charm_chat_orchestrator.process_chat_turn(
        message=msg,
        user_name=clean_name,
        day=d,
        month=m,
        year=y,
        conversation_id=req.conversation_id,
        user_id=user_id,
        tob=req.tob,
        pob=req.pob or req.city,
        loshu_grid=req.loshu_grid,
    )

    # Deduct 1 credit ONLY when status == "ANSWERED"
    if not edge_metered:
        with _VISITOR_CREDIT_LOCK:
            _IP_BURST_USAGE[(ip_hash, minute_bucket)] = _IP_BURST_USAGE.get((ip_hash, minute_bucket), 0) + 1
            if chat_res.status == "ANSWERED":
                new_used = _VISITOR_DAILY_USAGE.get((vis_hash, day_key), 0) + 1
                _VISITOR_DAILY_USAGE[(vis_hash, day_key)] = new_used
                _IP_DAILY_USAGE[(ip_hash, day_key)] = _IP_DAILY_USAGE.get((ip_hash, day_key), 0) + 1
            else:
                new_used = _VISITOR_DAILY_USAGE.get((vis_hash, day_key), 0)
            chat_res.credits_remaining = max(0, FREE_DAILY_LIMIT - new_used)

    out_payload = chat_res.model_dump()
    json_resp = JSONResponse(status_code=200, content=out_payload)
    _attach_visitor_cookie(json_resp, vis_id, is_new_vis)
    return json_resp


@router.get("/predictions/{prediction_id}/evidence")
async def get_prediction_evidence(prediction_id: str, current_user=Depends(get_current_user_optional)):
    """Returns full audit trace, method evaluations, and exact source locators for a prediction."""
    snapshot = outcome_service.get_snapshot(prediction_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Prediction snapshot not found.")
    return snapshot


@router.post("/outcomes")
async def record_prediction_outcome(req: OutcomeSubmissionRequest, current_user=Depends(get_current_user_optional)):
    """Records voluntary user event outcome for cohort verification."""
    user_id = current_user.get("user_id") or "anon_visitor"
    record = outcome_service.record_outcome(
        prediction_id=req.prediction_id,
        user_id=user_id,
        outcome_status=req.outcome_status,
        user_comment=req.user_comment
    )
    return {
        "status": "success",
        "message": "Outcome recorded successfully. Thank you for contributing to empirical verification.",
        "outcome_id": record.outcome_id
    }


@router.post("/followups")
async def submit_followup(req: FollowupQuestionRequest, current_user=Depends(get_current_user_optional)):
    """Handles follow-up clarifications on an existing prediction."""
    snapshot = outcome_service.get_snapshot(req.prediction_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Original prediction snapshot not found.")

    response = charm_chat_orchestrator.process_chat_turn(
        message=req.message,
        day=snapshot.driver,
        month=1,
        year=2026 - snapshot.personal_year,
        conversation_id=f"CONV-{req.prediction_id}"
    )
    return response
