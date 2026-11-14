from dotenv import load_dotenv
load_dotenv(override=True)
"""
Razorpay Payment Integration — Numeros Vision
POST /api/v1/payments/create-order   → create Razorpay order
POST /api/v1/payments/verify         → verify payment signature (called client-side after success)
GET  /api/v1/payments/plans          → public pricing catalogue
"""

import os
import hmac
import hashlib
import json
import time
from typing import Optional, Dict, Any, List, Tuple
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.engine.monetization_alignment_engine import (
    analyze_user_alignment_and_gaps,
    is_staging_bypass_authorized
)
from app.config.pricing_config import (
    resolve_sku_price,
    build_plans_from_packs_json,
    is_notify_me_higher_tiers_enabled,
    REJECTED_LEGACY_PLAN_IDS,
    REPORT_TIERS,
    BUNDLES,
    CHARM_AI_PACKS,
    CONSULTATION_PACKS,
)
from app.engine.funnel_service import (
    PricePolicy,
    digit_root,
    validate_single_price,
    validate_price_pair,
    FunnelStage,
    JourneyState,
    JourneyContext,
    get_next_step,
    log_funnel_event,
    PRODUCT_FUNNEL_CATALOG,
)
from app.api.auth import (
    update_user_entitlements,
    get_user_account_by_identifier,
    _ACTIVE_SESSIONS,
    _USER_ACCOUNTS
)

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])
api_router = APIRouter(prefix="/api", tags=["payments-standard"])

# ── Razorpay credentials (set in environment) ─────────────────────────────
# Test keys:  rzp_test_XXXXXXXXXXXXXXXXXXXX  /  your_test_secret
# Live keys:  rzp_live_XXXXXXXXXXXXXXXXXXXX  /  your_live_secret
RAZORPAY_KEY_ID         = os.getenv("RAZORPAY_KEY_ID", "rzp_test_REPLACE_ME")
RAZORPAY_KEY_SECRET     = os.getenv("RAZORPAY_KEY_SECRET", "REPLACE_ME_SECRET")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", RAZORPAY_KEY_SECRET)

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
SESSIONS_FILE = os.path.join(DATA_DIR, "verified_sessions.json")

# ── Plan catalogue (Single Source of Truth: app/config/packs.json) ─────────
PLANS: Dict[str, Dict[str, Any]] = build_plans_from_packs_json()

# ── Persistent verified-payment session store ──────────────────────────────
_verified_payments: dict = {}

# Cloud-Native Distributed Session Cache (Redis)
REDIS_URL = os.getenv("REDIS_URL")
_redis_client = None
if REDIS_URL:
    try:
        import redis
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    except Exception:
        _redis_client = None

def _load_sessions():
    """Load persisted verified sessions from disk on startup."""
    global _verified_payments
    try:
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    _verified_payments.update(data)
    except Exception:
        pass

def _save_sessions(session_token: Optional[str] = None):
    """Persist verified sessions to disk atomically and sync to Redis if available."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(_verified_payments, f, indent=2)
    except Exception:
        pass

    if _redis_client and session_token and session_token in _verified_payments:
        try:
            _redis_client.set(
                f"session:{session_token}",
                json.dumps(_verified_payments[session_token]),
                ex=86400 * 30  # 30-day session TTL
            )
        except Exception:
            pass

# Initialize on module import
_load_sessions()

def get_session_info(token: str) -> Optional[dict]:
    """Retrieve session info for a given premium/subscription token."""
    if not token:
        return None
    # Local QA test tokens — unconditionally rejected in production and preview
    if token in ("test_master_pass", "test_token", "demo_mode", "admin_test") or token.startswith("test_"):
        env_mode = os.getenv("ENVIRONMENT", "development").lower()
        if env_mode in ("production", "preview"):
            return None
        allow_test = (
            env_mode in ("development", "test", "local")
            or os.getenv("ALLOW_TEST_TOKENS", "false").lower() == "true"
        )
        if not allow_test:
            return None

        return {
            "token": token,
            "plan": "complete_report",
            "plan_name": "Complete Reports & Remedies (Test Access)",
            "questions_remaining": 9999,
            "has_remedies": True,
            "has_btr": True,
            "verified_at": int(time.time()),
            "status": "active"
        }
    if _redis_client:
        try:
            cached = _redis_client.get(f"session:{token}")
            if cached:
                return json.loads(cached)
        except Exception:
            pass
    return _verified_payments.get(token)

def consume_question(token: str) -> bool:
    """Consume 1 question from the quota if available and persist."""
    session = get_session_info(token)
    if not session:
        return False
    # If unlimited (complete plan has 9999)
    if session.get("questions_remaining", 0) > 0:
        session["questions_remaining"] -= 1
        _verified_payments[token] = session
        _save_sessions(token)
        return True
    return False

def record_question_history(token: str, question: str, answer_summary: str = "", topic: str = ""):
    """Record question and answer into session memory for multi-turn conversational context."""
    session = get_session_info(token)
    if not session:
        return
    if "question_history" not in session:
        session["question_history"] = []
    session["question_history"].append({
        "question": question,
        "topic": topic,
        "answer_summary": answer_summary[:300] if answer_summary else "",
        "timestamp": int(time.time())
    })
    _verified_payments[token] = session
    _save_sessions(token)

# ── Request models ─────────────────────────────────────────────────────────
class CreateOrderRequest(BaseModel):
    plan: Optional[str] = None
    plan_id: Optional[str] = None
    name: Optional[str] = ""
    customer_name: Optional[str] = ""
    email: Optional[str] = ""
    customer_email: Optional[str] = ""
    mobile: Optional[str] = ""
    customer_phone: Optional[str] = ""
    amount: Optional[int] = None
    amount_inr: Optional[int] = None
    currency: Optional[str] = "INR"
    receipt: Optional[str] = None

class VerifyPaymentRequest(BaseModel):
    razorpay_order_id:   Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    razorpay_signature:  Optional[str] = None
    plan: Optional[str] = None
    plan_id: Optional[str] = None
    email: Optional[str] = ""
    customer_name: Optional[str] = ""
    customer_phone: Optional[str] = ""

class AlignmentGapRequest(BaseModel):
    driver: Optional[int] = 1
    conductor: Optional[int] = 1
    loshu_counts: Optional[Dict[str, int]] = None
    missing_numbers: Optional[List[int]] = None
    name_number: Optional[int] = None
    personal_year: Optional[int] = None
    active_dasha: Optional[str] = None
    current_plan: Optional[str] = "free"
    credits_remaining: Optional[int] = 0
    token: Optional[str] = None

class FunnelNextStepRequest(BaseModel):
    product_id: Optional[str] = "birth_number"
    calculation_completed: Optional[bool] = False
    free_result_available: Optional[bool] = False
    token: Optional[str] = None
    opted_out: Optional[bool] = False

class PriceValidationRequest(BaseModel):
    reference: Optional[int] = None
    offer: Optional[int] = None
    amount: Optional[int] = None

class FunnelEventRequest(BaseModel):
    event: str
    product_id: Optional[str] = None
    stage: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


PLAN_COVERAGE_HIERARCHY = {
    "complete_report": {
        "complete_report", "complete", "report_master", "report_essential", "report_divine",
        "starter_5q", "starter", "growth_10q", "growth", "free", "discovery"
    },
    "report_divine": {
        "report_divine", "report_master", "report_essential", "complete_report", "free", "discovery"
    },
    "report_master": {
        "report_master", "report_essential", "free", "discovery"
    },
    "report_essential": {
        "report_essential", "free", "discovery"
    },
    "growth_10q": {
        "growth_10q", "growth", "starter_5q", "starter", "free", "discovery"
    },
    "starter_5q": {
        "starter_5q", "starter", "free", "discovery"
    },
    "ai_power_35q": {
        "ai_power_35q", "ai_growth_15q", "ai_starter_5q", "free", "discovery"
    },
    "ai_growth_15q": {
        "ai_growth_15q", "ai_starter_5q", "free", "discovery"
    },
    "ai_starter_5q": {
        "ai_starter_5q", "free", "discovery"
    }
}


def check_report_access(
    requested_tier: str,
    token: Optional[str] = None,
    user_id: Optional[str] = None,
    request: Optional[Request] = None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Gatekeeper for report tiers (Rules 2 & 3):
    1. Free tier is always accessible.
    2. Staging replica mode bypasses paywall for complete QA/QC testing.
    3. Paid tiers check active session token or registered user profile entitlements.
    4. If denied, generates personalized gap analysis and 'ANVEIL EVERY CHARM' CTA.
    """
    clean_tier = requested_tier.lower().strip()
    if clean_tier in ("free", "discovery"):
        return True, "free_tier", None

    # Check Staging Replica Mode bypass
    if request:
        headers = dict(request.headers)
        params = dict(request.query_params)
        if is_staging_bypass_authorized(headers, params, token):
            return True, "staging_replica_bypass", {"staging_mode": True}

    # Check Verified Payment Session
    session = get_session_info(token) if token else None
    if session:
        session_plan = session.get("plan", "")
        covered = PLAN_COVERAGE_HIERARCHY.get(session_plan, {session_plan})
        if clean_tier in covered or session_plan == clean_tier:
            return True, "session_authorized", session

    # Check Registered User Account Entitlements
    user = None
    if user_id:
        user = get_user_account_by_identifier(user_id)
    elif token and token in _ACTIVE_SESSIONS:
        auth_sess = _ACTIVE_SESSIONS[token]
        uid = auth_sess.get("user_id")
        user = _USER_ACCOUNTS.get(uid) if uid else None

    if user:
        unlocked = user.get("unlocked_reports", [])
        if clean_tier in unlocked:
            return True, "user_unlocked_report", user
        for plan in user.get("purchased_plans", []):
            covered = PLAN_COVERAGE_HIERARCHY.get(plan, {plan})
            if clean_tier in covered:
                return True, "user_purchased_plan_covered", user

    # Access Denied: User has not purchased this report tier
    d = user.get("driver_mulank", 1) if user else 1
    c = user.get("conductor_bhagyank", 1) if user else 1
    loshu = user.get("loshu_counts", {}) if user else {}
    missing = user.get("missing_numbers", []) if user else []

    gap_data = analyze_user_alignment_and_gaps(
        driver=d,
        conductor=c,
        loshu_counts=loshu,
        missing_numbers=missing,
        current_plan="free"
    )

    return False, "PAYMENT_REQUIRED", gap_data


# ── Endpoints ──────────────────────────────────────────────────────────────


@router.get("/pricing-catalog")
@api_router.get("/v1/pricing-catalog")
def get_pricing_catalog():
    """Returns authoritative server-side pricing catalog including feature_flags."""
    from app.config.pricing_config import export_pricing_catalog_json
    return json.loads(export_pricing_catalog_json())


class NotifyMeWaitlistRequest(BaseModel):
    email: str
    pack_id: Optional[str] = None
    sku_id: Optional[str] = None
    consent: bool = False
    purpose: Optional[str] = None
    consent_text: Optional[str] = None
    source_page: Optional[str] = "your_reading"


class NotifyMeDeleteRequest(BaseModel):
    email: str
    pack_id: Optional[str] = None
    sku_id: Optional[str] = None


def _normalize_notify_pack(pack_id: str) -> Optional[str]:
    from app.services.waitlist_service import normalize_waitlist_pack_id
    return normalize_waitlist_pack_id(pack_id)


@router.post("/waitlist/notify-me")
@api_router.post("/v1/waitlist/notify-me")
def register_notify_me_waitlist(req: NotifyMeWaitlistRequest):
    """
    Captures DPDP-consented launch notification requests for Advanced/Premium tiers.
    Stores email encrypted with AES-256-GCM (`ivHex:cipherHex`), explicit DPDP consent
    text, stated purpose ("tell me when this report is available"), and 12-month retention.
    Uses `email_sha256` strictly for de-duplication.
    """
    from app.services.waitlist_service import upsert_waitlist_record

    os.makedirs(DATA_DIR, exist_ok=True)
    waitlist_file = os.path.join(DATA_DIR, "waitlist_notify_me.jsonl")
    try:
        return upsert_waitlist_record(
            email=req.email,
            pack_id=req.pack_id or req.sku_id or "",
            consent=req.consent,
            purpose=req.purpose,
            consent_text=req.consent_text,
            source_page=req.source_page or "your_reading",
            storage_path=waitlist_file,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/waitlist/notify-me/delete")
@api_router.post("/v1/waitlist/notify-me/delete")
@router.delete("/waitlist/notify-me")
@api_router.delete("/v1/waitlist/notify-me")
def delete_notify_me_waitlist(req: NotifyMeDeleteRequest):
    """
    DPDP 2023 delete-on-request path: permanently erases stored encrypted email records
    matching the requester's email address (optionally scoped to a specific pack_id).
    """
    from app.services.waitlist_service import delete_waitlist_records

    os.makedirs(DATA_DIR, exist_ok=True)
    waitlist_file = os.path.join(DATA_DIR, "waitlist_notify_me.jsonl")
    try:
        return delete_waitlist_records(
            email=req.email,
            pack_id=req.pack_id or req.sku_id,
            storage_path=waitlist_file,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@api_router.get("/v1/public/loshu-teasers")
def get_public_loshu_teasers():
    """Serves sanitized, browser-safe Lo Shu curiosity teasers (zero paid report prose)."""
    teaser_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "static", "data", "loshu_public_teasers.json")
    )
    if not os.path.exists(teaser_path):
        raise HTTPException(status_code=404, detail="Public Lo Shu teaser slice not found.")
    with open(teaser_path, "r", encoding="utf-8") as fh:
        return json.load(fh)

@router.get("/plans")
def get_plans():
    """Return public pricing catalogue derived strictly from app/config/packs.json."""
    live_plans = build_plans_from_packs_json()
    PLANS.clear()
    PLANS.update(live_plans)

    formatted_plans = {}
    for k, v in live_plans.items():
        offer = v.get("amount_inr")
        orig = v.get("original_price_inr")
        paise = v.get("amount_paise")
        has_discount = (
            isinstance(orig, int)
            and isinstance(offer, int)
            and orig > 0
            and orig > offer
        )
        formatted_plans[k] = {
            "pack_id":            k,
            "name":               v["name"],
            "display_name":       v.get("display_name", v["name"]),
            "amount_inr":         offer,
            "original_price_inr": orig,
            "amount_paise":       paise,
            "struck_mrp_inr":     v.get("struck_mrp_inr"),
            "status":             v.get("status", "inactive"),
            "waitlist_only":      bool(v.get("waitlist_only", False)),
            "display_price_label": v.get("display_price_label"),
            "period":             v["period"],
            "questions_count":    v.get("questions_count", 0),
            "has_remedies":       v.get("has_remedies", False),
            "category":           v.get("category", "report"),
            "list_price_root":    digit_root(orig) if isinstance(orig, int) and orig > 0 else 0,
            "offer_price_root":   digit_root(offer) if isinstance(offer, int) and offer > 0 else 0,
            "savings_inr":        (orig - offer) if has_discount else 0,
            "discount_percent":   round(((orig - offer) / orig) * 100) if has_discount else 0,
            "description":        v.get("description", ""),
            "features":           v.get("features", []),
            "deliverables":       v.get("deliverables", []),
        }

    return {
        "status": "success",
        "success": True,
        "plans": formatted_plans,
        "currency": "INR",
        "razorpay_key": RAZORPAY_KEY_ID,
    }


@router.post("/alignment-gap-analysis")
async def get_alignment_gap_analysis(req: AlignmentGapRequest, request: Request):
    """
    Rule 1 & 2: Deterministic Alignment & Gap Analysis Endpoint.
    Analyzes driver-conductor alignment, Lo Shu missing planes (Golden Plane 4-5-6),
    and generates personalized conversion hooks with 'ANVEIL EVERY CHARM' CTAs.
    """
    driver = req.driver or 1
    conductor = req.conductor or 1
    loshu_counts = req.loshu_counts or {}
    missing_numbers = req.missing_numbers or []
    current_plan = req.current_plan or "free"
    credits_remaining = req.credits_remaining or 0

    token = req.token or request.cookies.get("nv_user_session")
    if token and token in _ACTIVE_SESSIONS:
        sess = _ACTIVE_SESSIONS[token]
        user = _USER_ACCOUNTS.get(sess.get("user_id"))
        if user:
            driver = user.get("driver_mulank", driver)
            conductor = user.get("conductor_bhagyank", conductor)
            loshu_counts = user.get("loshu_counts", loshu_counts)
            missing_numbers = user.get("missing_numbers", missing_numbers)
            credits_remaining = user.get("charm_credits_remaining", credits_remaining)
            purchased = user.get("purchased_plans", [])
            current_plan = purchased[-1] if purchased else "free"

    analysis = analyze_user_alignment_and_gaps(
        driver=driver,
        conductor=conductor,
        loshu_counts=loshu_counts,
        missing_numbers=missing_numbers,
        name_number=req.name_number,
        personal_year=req.personal_year,
        active_dasha=req.active_dasha,
        current_plan=current_plan,
        credits_remaining=credits_remaining
    )
    return analysis


@api_router.get("/planner-2027/price")
def get_planner_2027_price_endpoint():
    """Returns server-side status for 2027 Planner (waitlist-only with zero price until PLANNER_2027_LIVE=true)."""
    from app.config.planner_2027_pricing import get_planner_2027_price
    return get_planner_2027_price()


@api_router.post("/planner-2027/order")
async def create_planner_2027_order_endpoint(request: Request):
    """Server-side guard blocking 2027 Planner order creation until statutory disclaimer is approved."""
    from app.config.planner_2027_pricing import is_planner_2027_live
    if not is_planner_2027_live():
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "code": "PLANNER_WAITLIST_ONLY",
                "error": "Coming soon, notify me. The 2027 Year Ahead Numerology Planner is currently waitlist-only until statutory disclaimer approval.",
                "waitlist_pack_id": "planner_2027",
            },
        )
    body = await request.json()
    order_req = CreateOrderRequest(
        plan="planner_2027",
        name=body.get("full_name") or body.get("name"),
        email=body.get("email"),
        mobile=body.get("phone") or body.get("mobile"),
    )
    return await create_order(order_req)


@router.post("/create-order")
async def create_order(req: CreateOrderRequest):
    """
    Razorpay Standard Web Checkout - Step 1: Create Order.
    Resolves plan strictly from canonical `app/config/packs.json` via `resolve_sku_price()`.
    Rejects unknown/retired plan IDs, waitlist-only packs, and zero/inactive amounts with 4xx.
    """
    raw_plan = (req.plan or req.plan_id or "").strip()
    if not raw_plan:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "code": "MISSING_PLAN_ID",
                "detail": "Missing required plan or pack_id.",
            },
        )
    plan_key = raw_plan.lower()
    if plan_key in REJECTED_LEGACY_PLAN_IDS:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "code": "LEGACY_PLAN_ID_REJECTED",
                "detail": f"Legacy plan_id '{raw_plan}' is retired and not accepted.",
            },
        )
    resolved_sku = resolve_sku_price(plan_key)
    if resolved_sku is None:
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "code": "INVALID_PACK_ID",
                "detail": f"Invalid or retired plan_id: {raw_plan}",
            },
        )

    canonical_sku = resolved_sku["sku_id"]
    if canonical_sku == "planner_2027" and resolved_sku.get("waitlist_only"):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "code": "PLANNER_WAITLIST_ONLY",
                "detail": "Coming soon, notify me. The 2027 Year Ahead Numerology Planner is currently waitlist-only until statutory disclaimer approval.",
                "waitlist_pack_id": "planner_2027",
            },
        )
    if resolved_sku.get("waitlist_only") or resolved_sku.get("status") in ("waitlist", "coming_soon"):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "code": "TIER_WAITLIST_ONLY",
                "detail": "Coming soon, notify me. This report edition is currently waitlist-only; Anveil my alignments is open for immediate checkout.",
            },
        )
    if (
        resolved_sku.get("status") != "active"
        or resolved_sku.get("amount_inr") is None
        or resolved_sku.get("amount_paise") is None
        or int(resolved_sku["amount_paise"]) <= 0
    ):
        return JSONResponse(
            status_code=400,
            content={
                "success": False,
                "code": "NON_PURCHASABLE_PACK",
                "detail": f"Pack '{canonical_sku}' is not purchasable.",
            },
        )

    plan_amount_inr = int(resolved_sku["amount_inr"])
    plan_amount_paise = int(resolved_sku["amount_paise"])
    plan_name = str(resolved_sku.get("name") or canonical_sku)

    if plan_amount_paise < 100:
        raise HTTPException(status_code=400, detail="Amount must be at least 100 paise (₹1.00)")

    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    if not key_id or not key_secret:
        raise HTTPException(
            status_code=500,
            detail="Razorpay payment gateway credentials not configured in server environment."
        )

    customer_name = req.name or req.customer_name or "Valued Seeker"
    customer_email = req.email or req.customer_email or ""
    customer_mobile = req.mobile or req.customer_phone or ""
    receipt = req.receipt or f"nv_{canonical_sku}_{int(time.time())}"
    currency = req.currency or "INR"

    try:
        import razorpay
        import razorpay.errors
        client = razorpay.Client(auth=(key_id, key_secret))
        order = client.order.create({
            "amount":          plan_amount_paise,
            "currency":        currency,
            "receipt":         receipt,
            "payment_capture": 1,
            "notes": {
                "plan":   canonical_sku,
                "name":   customer_name,
                "email":  customer_email,
                "mobile": customer_mobile,
            }
        })
        order_id = order["id"]
    except Exception as e:
        err_str = str(e).lower()
        if "auth" in err_str or "unauthorized" in err_str:
            raise HTTPException(status_code=401, detail=f"Razorpay authentication failed: {str(e)}")
        if "bad request" in err_str:
            raise HTTPException(status_code=400, detail=f"Razorpay rejected order parameters: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to create Razorpay order: {str(e)}")

    return {
        "order_id":    order_id,
        "amount":      plan_amount_paise,
        "amount_inr":  plan_amount_inr,
        "currency":    currency,
        "plan":        canonical_sku,
        "plan_name":   plan_name,
        "key_id":      key_id,
        "key":         key_id,
        "name":        customer_name,
        "email":       customer_email,
        "mobile":      customer_mobile,
        "receipt":     receipt,
    }


@api_router.post("/create-order")
async def api_create_order(req: CreateOrderRequest):
    return await create_order(req)


@router.post("/verify")
async def verify_payment(req: VerifyPaymentRequest):
    """
    Razorpay Standard Web Checkout - Step 3: Verify Signature.
    Algorithm: HMAC-SHA256(order_id + "|" + payment_id, KEY_SECRET)
    Compares generated signature with razorpay_signature.
    Returns success only if signatures match.
    """
    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    if not key_id or not key_secret:
        raise HTTPException(
            status_code=500,
            detail="Razorpay payment gateway credentials not configured in server environment."
        )

    # Error handling: Missing required fields
    if not req.razorpay_order_id or not req.razorpay_payment_id or not req.razorpay_signature:
        raise HTTPException(
            status_code=400,
            detail="Missing required payment verification fields (razorpay_order_id, razorpay_payment_id, razorpay_signature)."
        )

    # Cryptographic HMAC-SHA256 signature verification
    msg = f"{req.razorpay_order_id}|{req.razorpay_payment_id}".encode()
    expected_signature = hmac.new(key_secret.encode(), msg, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_signature, req.razorpay_signature):
        raise HTTPException(
            status_code=400,
            detail="Payment verification failed: Invalid signature. Order will NOT be marked as paid."
        )

    # Payment verified successfully — generate session token and unlock entitlements
    session_token = hashlib.sha256(
        f"{req.razorpay_payment_id}{key_secret}".encode()
    ).hexdigest()[:32]

    plan_key = (req.plan or req.plan_id or "charm_single").strip().lower()
    plan_info = build_plans_from_packs_json().get(plan_key) or PLANS.get(plan_key, {})
    q_count = plan_info.get("questions_count", 5)

    _verified_payments[session_token] = {
        "plan":                plan_key,
        "plan_name":           plan_info.get("name", "Charm AI"),
        "payment_id":          req.razorpay_payment_id,
        "order_id":            req.razorpay_order_id,
        "email":               req.email or "",
        "questions_count":     q_count,
        "questions_remaining": q_count,
        "has_remedies":        plan_info.get("has_remedies", False),
        "verified_at":         int(time.time()),
    }
    _save_sessions()

    # Synchronize entitlements with registered user account if present
    if req.email:
        if plan_key.startswith("bundle_"):
            for inc_rep in plan_info.get("included_reports", []):
                update_user_entitlements(
                    email_or_user_id=req.email,
                    plan_id=inc_rep,
                    credits_to_add=0,
                    unlocked_report=inc_rep
                )
        update_user_entitlements(
            email_or_user_id=req.email,
            plan_id=plan_key,
            credits_to_add=q_count if q_count < 9999 else 9999,
            unlocked_report=plan_key if (plan_key.startswith("report_") or plan_key.startswith("bundle_") or plan_key in ["complete_report", "starter_5q", "growth_10q"]) else None
        )

    # Persist to bookings log
    _persist_payment(req, session_token)

    # Automatically generate official invoice & dispatch email receipt
    generated_inv_id = None
    try:
        from app.api.billing import create_invoice_record, dispatch_invoice_notification, InvoiceCreateRequest
        import threading
        inv_name = getattr(req, 'customer_name', None) or (req.email.split('@')[0].replace('.', ' ').title() if req.email else 'Valued Seeker')
        inv_phone = getattr(req, 'customer_phone', '') or ''
        inv_req = InvoiceCreateRequest(
            order_id=req.razorpay_order_id,
            payment_id=req.razorpay_payment_id,
            customer_name=inv_name,
            customer_email=req.email or '',
            customer_phone=inv_phone,
            plan_id=plan_key,
            amount_inr=int(plan_info.get('amount_inr') or 0),
            payment_method='Razorpay Online Payment'
        )
        invoice_obj = create_invoice_record(inv_req)
        generated_inv_id = invoice_obj.get('invoice_id')
        threading.Thread(target=dispatch_invoice_notification, args=(invoice_obj,), daemon=True).start()
    except Exception as inv_err:
        print(f'[PAYMENT INVOICE GENERATION WARNING] {inv_err}')

    return {
        "status":              "success",
        "verified":            True,
        "message":             "Payment verified successfully.",
        "invoice_id":          generated_inv_id,
        "order_id":            req.razorpay_order_id,
        "payment_id":          req.razorpay_payment_id,
        "premium_token":       session_token,
        "plan":                plan_key,
        "plan_name":           plan_info.get("name", "Numeros Vision"),
        "unlocked_report":     plan_key
    }


@router.post("/verify-payment")
async def router_verify_payment(req: VerifyPaymentRequest):
    return await verify_payment(req)


@api_router.post("/verify-payment")
async def api_verify_payment(req: VerifyPaymentRequest):
    return await verify_payment(req)


@router.get("/status/{session_token}")
def check_status(session_token: str):
    """Check if a session token corresponds to a verified premium payment."""
    record = _verified_payments.get(session_token)
    if not record:
        return {"active": False}
    return {
        "active": True,
        "plan":   record["plan"],
        "email":  record.get("email", ""),
        "questions_remaining": record.get("questions_remaining", 0),
        "has_remedies": record.get("has_remedies", False),
    }


@router.post("/webhook")
async def razorpay_webhook(request: Request):
    """
    Razorpay Server-to-Server Webhook Handler.
    Handles 'payment.captured' and 'order.paid' events.
    Verifies X-Razorpay-Signature using RAZORPAY_WEBHOOK_SECRET.
    """
    raw_body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")

    # Verify signature if secret is configured and not default placeholder
    if RAZORPAY_WEBHOOK_SECRET not in ("REPLACE_ME_SECRET", "REPLACE_WITH_ACTUAL_RAZORPAY_KEY_SECRET"):
        expected_sig = hmac.new(
            RAZORPAY_WEBHOOK_SECRET.encode(),
            raw_body,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(expected_sig, signature):
            raise HTTPException(status_code=400, detail="Invalid webhook signature")

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    event = payload.get("event", "")

    if event in ("payment.captured", "order.paid"):
        payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
        order_entity = payload.get("payload", {}).get("order", {}).get("entity", {})

        payment_id = payment_entity.get("id") or f"pay_wh_{int(time.time())}"
        order_id = payment_entity.get("order_id") or order_entity.get("id") or f"order_wh_{int(time.time())}"
        notes = payment_entity.get("notes") or order_entity.get("notes") or {}
        plan_id = str(notes.get("plan", "charm_single")).strip().lower()
        email = notes.get("email", "")

        # Provision session token
        session_token = hashlib.sha256(
            f"{payment_id}{RAZORPAY_KEY_SECRET}".encode()
        ).hexdigest()[:32]

        plan_info = build_plans_from_packs_json().get(plan_id) or PLANS.get(plan_id, {})
        q_count = plan_info.get("questions_count", 5)

        _verified_payments[session_token] = {
            "plan":                plan_id,
            "plan_name":           plan_info.get("name", "Charm AI"),
            "payment_id":          payment_id,
            "order_id":            order_id,
            "email":               email,
            "questions_count":     q_count,
            "questions_remaining": q_count,
            "has_remedies":        plan_info.get("has_remedies", False),
            "verified_at":         int(time.time()),
            "source":              "webhook",
        }
        _save_sessions()

        if email:
            if plan_id.startswith("bundle_"):
                for inc_rep in plan_info.get("included_reports", []):
                    update_user_entitlements(
                        email_or_user_id=email,
                        plan_id=inc_rep,
                        credits_to_add=0,
                        unlocked_report=inc_rep
                    )
            update_user_entitlements(
                email_or_user_id=email,
                plan_id=plan_id,
                credits_to_add=q_count if q_count < 9999 else 9999,
                unlocked_report=plan_id if (plan_id.startswith("report_") or plan_id.startswith("bundle_") or plan_id in ["complete_report", "starter_5q", "growth_10q"]) else None
            )

        # Log to data/payments.jsonl
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(os.path.join(DATA_DIR, "payments.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "token": session_token,
                    "plan": plan_id,
                    "payment_id": payment_id,
                    "order_id": order_id,
                    "email": email,
                    "source": "webhook",
                    "ts": int(time.time())
                }) + "\n")
        except Exception:
            pass

        return {
            "status": "success",
            "event": event,
            "session_token": session_token,
            "plan": plan_id
        }

    return {"status": "ignored", "event": event}


# ── Funnel & Customer Journey Endpoints (v1.5.0) ──────────────────────────

@router.get("/funnel/products")
def get_funnel_products():
    """Return unified product catalogue with approved funnel hooks, deliverables and CTAs."""
    return {
        "status": "success",
        "tagline": "ANVEIL EVERY CHARM",
        "currency": "INR",
        "products": PRODUCT_FUNNEL_CATALOG
    }


@router.post("/funnel/validate-price")
def validate_funnel_price(req: PriceValidationRequest):
    """
    Validates pricing against brand digit-root policy {1, 3, 5, 6}
    and verifies that offer price is strictly less than reference price.
    """
    if req.reference is not None and req.offer is not None:
        return validate_price_pair(req.reference, req.offer)
    if req.amount is not None:
        return validate_single_price(req.amount)
    raise HTTPException(status_code=400, detail="Must provide either 'amount' or both 'reference' and 'offer'")


@router.api_route("/funnel/next-step", methods=["GET", "POST"])
async def funnel_next_step(
    request: Request,
    product_id: Optional[str] = None,
    calculation_completed: Optional[bool] = None,
    free_result_available: Optional[bool] = None,
    token: Optional[str] = None,
    opted_out: Optional[bool] = None,
):
    """
    Determines seeker's next action in the 7-stage marketing funnel.
    Supports GET query parameters and POST JSON bodies.
    Enforces opt-out precedence and prevents duplicate report sales.
    """
    if request.method == "POST":
        try:
            body = await request.json()
            if isinstance(body, dict):
                product_id = body.get("product_id", product_id)
                calculation_completed = body.get("calculation_completed", calculation_completed)
                free_result_available = body.get("free_result_available", free_result_available)
                token = body.get("token", token)
                opted_out = body.get("opted_out", opted_out)
        except Exception:
            pass

    pid = product_id or "birth_number"
    calc_done = bool(calculation_completed)
    free_res = bool(free_result_available)
    is_opted_out = bool(opted_out)

    sess_token = token or request.cookies.get("nv_user_session") or request.headers.get("x-session-token")
    
    entitlements = []
    payment_status = None
    fulfilment_status = None

    if sess_token and sess_token in _verified_payments:
        rec = _verified_payments[sess_token]
        plan = rec.get("plan", "")
        entitlements.append(plan)
        payment_status = "CONFIRMED"
        fulfilment_status = "FULFILLED"

    context = JourneyContext(
        session_token=sess_token,
        user_opted_out_of_marketing=is_opted_out,
        calculation_completed=calc_done,
        free_result_available=free_res,
        payment_status=payment_status,
        fulfilment_status=fulfilment_status,
        current_entitlements=entitlements
    )

    step = get_next_step(
        user=None,
        product_id=pid,
        journey_context=context
    )
    return step


@router.post("/funnel/event")
async def capture_funnel_event(req: FunnelEventRequest, request: Request):
    """
    Captures privacy-minimised marketing funnel events.
    Rejects sensitive PII (DOB, mobile, credit card numbers).
    """
    sess_id = req.session_id or request.cookies.get("nv_user_session") or "anon"
    success = log_funnel_event(
        event_name=req.event,
        product_id=req.product_id,
        stage=req.stage,
        session_id=sess_id,
        metadata=req.metadata
    )
    return {
        "status": "success" if success else "ignored",
        "event": req.event,
        "logged": success
    }


# ── Internal helpers ───────────────────────────────────────────────────────

def _persist_payment(req: VerifyPaymentRequest, token: str):
    """Append verified payment to bookings.jsonl log."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        record = {
            "token":      token,
            "plan":       req.plan,
            "payment_id": req.razorpay_payment_id,
            "order_id":   req.razorpay_order_id,
            "email":      req.email or "",
            "ts":         int(time.time()),
        }
        with open(os.path.join(DATA_DIR, "payments.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass  # Non-critical — don't block the user response
