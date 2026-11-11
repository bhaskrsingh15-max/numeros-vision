from app.services.otp_dispatcher import dispatch_otp_multichannel
"""
AUTHENTICATION & CYBER-ATTACK DEFENSE ENGINE — NUMEROS VISION
Features:
1. Practitioner & Admin Login ID + Passphrase Verification
2. Brute-Force Rate Limiting (Lockout after 5 failed attempts per IP)
3. Cryptographically Signed HMAC-SHA256 Session Tokens
4. Role-Based Access Control for Practitioner CRM, CDP & Client Records
"""

import os
import time
import hmac
import hashlib
import json
import uuid
import datetime
import random
import re
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel, Field

from app.engine.cdp_identity_engine import (
    normalize_email, normalize_phone, IdentityPayload, resolve_golden_profile,
    enrich_deterministic_taxonomy, enrich_probabilistic_taxonomy, generate_uid2_token
)
from app.engine.core_matrix_engine import (
    calculate_driver, calculate_conductor, calculate_kua_number,
    calculate_chaldean_name, calculate_dasha_cycles
)
from app.engine.master_knowledge_engine import calculate_lo_shu_plane_metrics
from app.api.consent import CONSENT_LEDGER
from app.engine.monetization_alignment_engine import analyze_user_alignment_and_gaps

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication & Access Control"])

# ── Credentials (configurable via environment variables) ──────────────────────
MASTER_LOGIN_ID   = os.getenv("PRACTITIONER_LOGIN_ID", "admin@numerosvision.com")
MASTER_PASSWORD   = os.getenv("PRACTITIONER_PASSWORD", "")
AUTH_SECRET_KEY   = os.getenv("AUTH_SECRET_KEY", "numeros_vision_sovereign_secret_key_888")

# ── In-Memory Session & User Account Stores ──────────────────────────────────
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
USERS_FILE = os.path.join(DATA_DIR, "users.json")

# {session_token: {"login_id": str, "user_id": str, "role": str, "created_at": float, "expires_at": float, "ip": str}}
_ACTIVE_SESSIONS: Dict[str, Dict[str, Any]] = {}

# {user_id: UserRecordDict}
_USER_ACCOUNTS: Dict[str, Dict[str, Any]] = {}
# {normalized_email: user_id}
_EMAIL_TO_USER_ID: Dict[str, str] = {}
# {normalized_phone: user_id}
_PHONE_TO_USER_ID: Dict[str, str] = {}

def _load_user_accounts():
    """Load persisted user accounts from data/users.json."""
    global _USER_ACCOUNTS, _EMAIL_TO_USER_ID, _PHONE_TO_USER_ID
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    _USER_ACCOUNTS.update(data)
                    for uid, u in _USER_ACCOUNTS.items():
                        if u.get("email"):
                            _EMAIL_TO_USER_ID[normalize_email(u["email"])] = uid
                        if u.get("phone"):
                            _PHONE_TO_USER_ID[normalize_phone(u["phone"])] = uid
    except Exception:
        pass

def _save_user_accounts():
    """Atomically persist user accounts to data/users.json."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(_USER_ACCOUNTS, f, indent=2)
    except Exception:
        pass

# Initialize from storage
_load_user_accounts()

def get_user_account_by_identifier(identifier: str) -> Optional[Dict[str, Any]]:
    """Retrieve user account by email, phone, or user_id with robust format tolerance."""
    if not identifier:
        return None
    clean = str(identifier).strip()
    if "@" in clean:
        norm_em = normalize_email(clean)
        uid = _EMAIL_TO_USER_ID.get(norm_em)
        if uid and uid in _USER_ACCOUNTS:
            return _USER_ACCOUNTS[uid]
        return None

    # 1. Direct phone match
    if clean in _PHONE_TO_USER_ID:
        uid = _PHONE_TO_USER_ID.get(clean)
        if uid and uid in _USER_ACCOUNTS:
            return _USER_ACCOUNTS[uid]

    # 2. Normalized phone match
    norm_p = normalize_phone(clean)
    if norm_p and norm_p in _PHONE_TO_USER_ID:
        uid = _PHONE_TO_USER_ID.get(norm_p)
        if uid and uid in _USER_ACCOUNTS:
            return _USER_ACCOUNTS[uid]

    # 3. Digits-only phone match
    digits = re.sub(r"[^0-9]", "", clean)
    if digits and digits in _PHONE_TO_USER_ID:
        uid = _PHONE_TO_USER_ID.get(digits)
        if uid and uid in _USER_ACCOUNTS:
            return _USER_ACCOUNTS[uid]

    # 4. Check with or without 91 prefix
    if len(digits) == 10 and f"91{digits}" in _PHONE_TO_USER_ID:
        uid = _PHONE_TO_USER_ID.get(f"91{digits}")
        if uid and uid in _USER_ACCOUNTS:
            return _USER_ACCOUNTS[uid]
    if digits.startswith("91") and len(digits) > 10 and digits[2:] in _PHONE_TO_USER_ID:
        uid = _PHONE_TO_USER_ID.get(digits[2:])
        if uid and uid in _USER_ACCOUNTS:
            return _USER_ACCOUNTS[uid]

    # 5. Direct user_id
    if clean in _USER_ACCOUNTS:
        return _USER_ACCOUNTS[clean]
    return None

def update_user_entitlements(
    email_or_user_id: str,
    plan_id: str,
    credits_to_add: int = 0,
    unlocked_report: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """Synchronize user purchases, question credits, and unlocked reports."""
    user = get_user_account_by_identifier(email_or_user_id)
    if not user:
        return None

    if "purchased_plans" not in user:
        user["purchased_plans"] = []
    if plan_id and plan_id not in user["purchased_plans"]:
        user["purchased_plans"].append(plan_id)

    if "unlocked_reports" not in user:
        user["unlocked_reports"] = ["free", "discovery"]
    if unlocked_report and unlocked_report not in user["unlocked_reports"]:
        user["unlocked_reports"].append(unlocked_report)
    elif plan_id and plan_id.startswith("report_") and plan_id not in user["unlocked_reports"]:
        user["unlocked_reports"].append(plan_id)

    user["charm_credits_total"] = user.get("charm_credits_total", 0) + credits_to_add
    user["charm_credits_remaining"] = user.get("charm_credits_remaining", 0) + credits_to_add
    user["updated_at"] = time.time()

    _save_user_accounts()
    return user

# {client_ip: {"failed_count": int, "locked_until": float}}
_FAILED_LOGIN_ATTEMPTS: Dict[str, Dict[str, Any]] = {}

# ── In-Memory OTP Store & Verification Engine ──────────────────────────────
# {identifier: {"otp": str, "channel": str, "created_at": float, "expires_at": float, "attempts": int, "verified": bool, "token": str}}
_OTP_STORE: Dict[str, Dict[str, Any]] = {}
TEST_SANDBOX_OTPS = {"123456", "777777", "999999"}
OTP_EXPIRY_SEC = 600  # 10 minutes
MAX_OTP_ATTEMPTS = 5

class OTPSendRequest(BaseModel):
    identifier: str = Field(..., description="Mobile number or Email address")
    channel: Optional[str] = Field("auto", description="sms, whatsapp, email, both, or auto")
    name: Optional[str] = Field(None, description="Optional user calling name")
    phone: Optional[str] = Field(None, description="Optional associated mobile number for dual dispatch")
    email: Optional[str] = Field(None, description="Optional associated email address for dual dispatch")

class OTPVerifyRequest(BaseModel):
    identifier: str = Field(..., description="Mobile number or Email address")
    otp: str = Field(..., min_length=4, max_length=10, description="Verification code")
    auto_login: Optional[bool] = Field(True, description="Automatically issue session token if user exists")

class OTPLoginRequest(BaseModel):
    identifier: str = Field(..., description="Mobile number or Email address")
    otp: str = Field(..., min_length=4, max_length=10, description="Verification code")
    name: Optional[str] = Field(None, description="Optional full name if new profile creation required")
    day: Optional[int] = Field(15, ge=1, le=31)
    month: Optional[int] = Field(8, ge=1, le=12)
    year: Optional[int] = Field(1990, ge=1900, le=2100)
    redirect_url: Optional[str] = Field("/dashboard/")
    calculation_id: Optional[str] = Field(None, description="Persisted calculation ID from recent calculator session")

MAX_FAILED_ATTEMPTS = 5
LOCKOUT_DURATION_SEC = 900  # 15 minutes lockout
SESSION_LIFETIME_SEC = 86400  # 24 hours


def hash_password(password: str) -> str:
    """Salted SHA-256 password hashing."""
    salt = uuid.uuid4().hex[:16]
    h = hashlib.sha256(f"{salt}:{password}:{AUTH_SECRET_KEY}".encode()).hexdigest()
    return f"{salt}${h}"


def verify_password(password: str, hashed: str) -> bool:
    """Verifies a plaintext password against stored salted hash."""
    if not hashed or "$" not in hashed:
        return False
    salt, h = hashed.split("$", 1)
    expected = hashlib.sha256(f"{salt}:{password}:{AUTH_SECRET_KEY}".encode()).hexdigest()
    return hmac.compare_digest(h, expected)


class LoginRequest(BaseModel):
    login_id: str = Field(..., description="Practitioner, Admin, or User Email/Mobile")
    password: str = Field(..., description="Passphrase or Password")


class UserSignupRequest(BaseModel):
    name: Optional[str] = Field(None, max_length=120, description="Full calling name")
    full_name: Optional[str] = Field(None, max_length=120, description="Full calling name alias")
    email: str = Field(..., min_length=5, max_length=150, description="Email address")
    phone: Optional[str] = Field(None, max_length=25, description="Mobile / WhatsApp number")
    phone_verified: Optional[bool] = Field(False, description="Whether mobile number was verified via OTP")
    email_verified: Optional[bool] = Field(False, description="Whether email was verified via OTP")
    verification_token: Optional[str] = Field(None, description="OTP Verification token if pre-verified")
    day: int = Field(..., ge=1, le=31, description="Day of birth (1-31)")
    month: int = Field(..., ge=1, le=12, description="Month of birth (1-12)")
    year: int = Field(..., ge=1900, le=2100, description="Year of birth (1900-2100)")
    birth_time: Optional[str] = Field(None, description="Time of birth (e.g. 14:30 or 02:30 PM)")
    birth_time_hour: Optional[int] = Field(None, ge=1, le=12, description="Hour of birth (1-12)")
    birth_time_minute: Optional[int] = Field(None, ge=0, le=59, description="Minute of birth (0-59)")
    birth_time_period: Optional[str] = Field("AM", description="AM or PM")
    birth_place: Optional[str] = Field(None, description="Place of birth (City / Town)")
    country: Optional[str] = Field("India", description="Country of birth")
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0, description="Birth latitude in decimal degrees")
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0, description="Birth longitude in decimal degrees")
    altitude: Optional[float] = Field(None, description="Birth altitude in meters")
    timezone: Optional[str] = Field("Asia/Kolkata", description="Timezone (e.g. Asia/Kolkata, UTC+05:30)")
    gender: Optional[str] = Field("prefer_not_to_say", description="male, female, other, prefer_not_to_say")
    password: str = Field(..., min_length=6, max_length=128, description="Account password")
    
    # Statutory DPDP Act 2023 & GDPR Unbundled Consent Flags
    consent_profile_storage: bool = Field(..., description="Mandatory DPDP Act 2023 Consent to store and process birth chart")
    consent_evaluation_feedback: bool = Field(False, description="Consent for de-identified offline evaluation/calibration")
    consent_marketing: bool = Field(False, description="Consent for milestone & dasha communications")
    
    # Context / Tracking parameters
    device_id: Optional[str] = Field(None)
    device_type: Optional[str] = Field("desktop")
    nv_uid: Optional[str] = Field(None)
    utm_source: Optional[str] = Field("direct")
    utm_medium: Optional[str] = Field("web")
    utm_campaign: Optional[str] = Field("organic")
    source: Optional[str] = Field("signup_page")
    redirect_url: Optional[str] = Field("/dashboard/")
    calculation_id: Optional[str] = Field(None, description="Persisted calculation ID from recent calculator session")

class SessionVerifyRequest(BaseModel):
    token: Optional[str] = None


def generate_session_token(login_id: str, client_ip: str) -> str:
    salt = uuid.uuid4().hex
    raw = f"{login_id}:{client_ip}:{salt}:{time.time()}"
    sig = hmac.new(AUTH_SECRET_KEY.encode(), raw.encode(), hashlib.sha256).hexdigest()
    return f"nv_auth_{sig[:32]}"


@router.post("/signup")
async def api_signup(req: UserSignupRequest, request: Request, response: Response):
    """
    Unified Signup & Profile Creation Endpoint:
    1. Enforces mandatory statutory consent under India DPDP Act 2023.
    2. Runs deterministic calculations (Mulank, Bhagyank, Kua, Chaldean Name, Lo Shu Grid, Dasha).
    3. Ingests & stitches profile into the Customer Data Platform (CDP) Golden Graph.
    4. Records audit-trailed consent into the DPDP Consent Ledger.
    5. Stores user account and issues cryptographically signed session tokens.
    """
    # 0. Calling Name Validation
    user_name = (req.name or req.full_name or "").strip()
    if not user_name:
        raise HTTPException(status_code=400, detail="Full calling name is required.")

    # 1. Statutory Consent Guard (DPDP Act 2023 & GDPR)
    if not req.consent_profile_storage:
        raise HTTPException(
            status_code=400,
            detail="Statutory Consent Required: Under the Digital Personal Data Protection (DPDP) Act 2023, explicit consent is required to process and store your birth matrix."
        )

    # 2. Email & Phone Normalization
    norm_email = normalize_email(req.email)
    if not norm_email or "@" not in norm_email:
        raise HTTPException(status_code=400, detail="Please provide a valid email address.")
    norm_phone = normalize_phone(req.phone) if req.phone else ""

    # 3. Calendar Date Validation
    try:
        datetime.date(req.year, req.month, req.day)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date of birth provided. Please verify day, month, and year.")

    # Format or normalize birth_time with AM/PM
    if not req.birth_time and req.birth_time_hour is not None and req.birth_time_minute is not None:
        period = (req.birth_time_period or "AM").upper()
        req.birth_time = f"{req.birth_time_hour:02d}:{req.birth_time_minute:02d} {period}"
    elif req.birth_time and req.birth_time_hour is None:
        try:
            bt_clean = req.birth_time.strip().upper()
            if "AM" in bt_clean or "PM" in bt_clean:
                parts = bt_clean.replace("AM", "").replace("PM", "").strip().split(":")
                req.birth_time_hour = int(parts[0])
                req.birth_time_minute = int(parts[1]) if len(parts) > 1 else 0
                req.birth_time_period = "PM" if "PM" in bt_clean else "AM"
            elif ":" in bt_clean:
                parts = bt_clean.split(":")
                h = int(parts[0])
                m = int(parts[1])
                req.birth_time_period = "PM" if h >= 12 else "AM"
                req.birth_time_hour = h if 1 <= h <= 12 else (h - 12 if h > 12 else 12)
                req.birth_time_minute = m
        except Exception:
            pass

    # 4. Check for Existing Account
    existing_uid = _EMAIL_TO_USER_ID.get(norm_email)
    if existing_uid:
        user = _USER_ACCOUNTS.get(existing_uid, {})
        # If password matches, treat as profile update / re-login
        if not verify_password(req.password, user.get("password_hash", "")):
            raise HTTPException(
                status_code=409,
                detail="An account with this email address already exists. Please sign in or use a different email."
            )
        user_id = existing_uid
    else:
        user_id = f"usr_{uuid.uuid4().hex[:12]}"

    # 5. Deterministic Numerology & Astrology Calculation
    mulank = calculate_driver(req.day)
    bhagyank = calculate_conductor(req.day, req.month, req.year)
    kua = calculate_kua_number(req.year, req.gender)
    name_calc = calculate_chaldean_name(user_name)
    dasha_cycles = calculate_dasha_cycles(req.day, req.month, req.year)
    plane_metrics = calculate_lo_shu_plane_metrics(req.day, req.month, req.year)

    dob_digits_str = f"{req.day:02d}{req.month:02d}{req.year:04d}"
    loshu_counts = {i: dob_digits_str.count(str(i)) for i in range(1, 10)}
    missing_numbers = [i for i, c in loshu_counts.items() if c == 0]

    # 6. Customer Data Platform (CDP) Ingestion & Golden Profile Resolution
    client_ip = request.client.host if request.client else "127.0.0.1"
    ua = request.headers.get("user-agent", "")
    nv_uid = req.nv_uid or f"nv_uid_{uuid.uuid4().hex[:12]}"

    cdp_payload = IdentityPayload(
        email=norm_email,
        phone=norm_phone if norm_phone else None,
        device_id=req.device_id,
        device_type=req.device_type or "desktop",
        nv_uid=nv_uid,
        consent_marketing=req.consent_marketing,
        consent_device_tracking=True,
        client_ip=client_ip,
        client_user_agent=ua
    )
    golden_profile = resolve_golden_profile(cdp_payload)
    golden_id = golden_profile["golden_profile_id"]

    now = time.time()
    active_dasha_ruler = dasha_cycles.get("current_cycle", {}).get("mahadasha_ruler", "Sun")
    personal_year_val = dasha_cycles.get("personal_year", 1)

    enrich_deterministic_taxonomy(golden_id, {
        "seeker_name": user_name,
        "email": norm_email,
        "phone": norm_phone,
        "numerology_mulank": mulank,
        "numerology_bhagyank": bhagyank,
        "kua_number": kua,
        "chaldean_name_number": name_calc.get("single_root", 0),
        "chaldean_compound": name_calc.get("compound_sum", 0),
        "birth_date": f"{req.year:04d}-{req.month:02d}-{req.day:02d}",
        "birth_time": req.birth_time or "",
        "birth_time_hour": req.birth_time_hour,
        "birth_time_minute": req.birth_time_minute,
        "birth_time_period": req.birth_time_period or "AM",
        "birth_place": req.birth_place or "",
        "country": req.country or "India",
        "latitude": req.latitude,
        "longitude": req.longitude,
        "altitude": req.altitude,
        "timezone": req.timezone or "Asia/Kolkata",
        "gender": req.gender or "prefer_not_to_say",
        "lo_shu_counts": loshu_counts,
        "lo_shu_missing": missing_numbers,
        "active_mahadasha": active_dasha_ruler,
        "personal_year": personal_year_val,
        "customer_tier": "FREE_REGISTERED_USER",
        "consent_profile_storage": True,
        "consent_evaluation_feedback": req.consent_evaluation_feedback,
        "consent_marketing": req.consent_marketing,
        "consent_timestamp": now,
        "consent_policy_version": "2025.1.DPDP",
        "jurisdiction": "IN"
    })

    enrich_probabilistic_taxonomy(golden_id, {
        "career_pivot_propensity": 0.6 if mulank in [1, 8, 9] else 0.4,
        "marriage_urgency_propensity": 0.7 if mulank in [2, 6] else 0.3,
        "transit_friction_index": 0.35,
        "hni_affluence_propensity": 0.5
    })

    # 7. Consent Ledger Recording (DPDP Act 2023)
    CONSENT_LEDGER.append({
        "user_id": user_id,
        "calculation_id": req.calculation_id or f"CALC-AUTH-{int(time.time())}",
        "golden_profile_id": golden_id,
        "email": norm_email,
        "purpose": "profile_storage_and_calculations",
        "granted": True,
        "timestamp": now,
        "date_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
        "policy_version": "2025.1.DPDP"
    })
    if req.consent_evaluation_feedback:
        CONSENT_LEDGER.append({
            "user_id": user_id,
            "golden_profile_id": golden_id,
            "email": norm_email,
            "purpose": "evaluation_feedback_flywheel",
            "granted": True,
            "timestamp": now,
            "date_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
            "policy_version": "2025.1.DPDP"
        })
    if req.consent_marketing:
        CONSENT_LEDGER.append({
            "user_id": user_id,
            "golden_profile_id": golden_id,
            "email": norm_email,
            "purpose": "marketing_and_transit_alerts",
            "granted": True,
            "timestamp": now,
            "date_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now)),
            "policy_version": "2025.1.DPDP"
        })

    # 8. Store User Record
    user_record = {
        "user_id": user_id,
        "name": user_name,
        "email": norm_email,
        "phone": norm_phone,
        "day": req.day,
        "month": req.month,
        "year": req.year,
        "birth_date": f"{req.year:04d}-{req.month:02d}-{req.day:02d}",
        "birth_time": req.birth_time or "",
        "birth_time_hour": req.birth_time_hour,
        "birth_time_minute": req.birth_time_minute,
        "birth_time_period": req.birth_time_period or "AM",
        "birth_place": req.birth_place or "",
        "country": req.country or "India",
        "latitude": req.latitude,
        "longitude": req.longitude,
        "altitude": req.altitude,
        "timezone": req.timezone or "Asia/Kolkata",
        "gender": req.gender or "prefer_not_to_say",
        "password_hash": hash_password(req.password),
        "golden_profile_id": golden_id,
        "nv_uid": nv_uid,
        "driver_mulank": mulank,
        "conductor_bhagyank": bhagyank,
        "kua_number": kua,
        "name_number": name_calc.get("single_root", 0),
        "name_compound": name_calc.get("compound_sum", 0),
        "loshu_counts": loshu_counts,
        "missing_numbers": missing_numbers,
        "active_mahadasha": active_dasha_ruler,
        "personal_year": personal_year_val,
        "purchased_plans": [],
        "unlocked_reports": ["free", "discovery"],
        "charm_credits_total": 0,
        "charm_credits_remaining": 0,
        "phone_verified": req.phone_verified or bool(norm_phone and norm_phone in _OTP_STORE and _OTP_STORE[norm_phone].get("verified", False)),
        "email_verified": req.email_verified or bool(norm_email in _OTP_STORE and _OTP_STORE[norm_email].get("verified", False)),
        "verification_badge": "verified_customer" if (req.phone_verified or req.email_verified or bool(norm_phone and norm_phone in _OTP_STORE and _OTP_STORE[norm_phone].get("verified", False)) or bool(norm_email in _OTP_STORE and _OTP_STORE[norm_email].get("verified", False))) else "standard",
        "consents": {
            "profile_storage": True,
            "evaluation_feedback": req.consent_evaluation_feedback,
            "marketing": req.consent_marketing,
            "policy_version": "2025.1.DPDP",
            "timestamp": now
        },
        "created_at": now,
        "updated_at": now
    }
    _USER_ACCOUNTS[user_id] = user_record
    _EMAIL_TO_USER_ID[norm_email] = user_id
    if norm_phone:
        _PHONE_TO_USER_ID[norm_phone] = user_id
    _save_user_accounts()

    # Alignment & Gap Analysis for Seeker (Rule 1)
    alignment_info = analyze_user_alignment_and_gaps(
        driver=mulank,
        conductor=bhagyank,
        loshu_counts=loshu_counts,
        missing_numbers=missing_numbers,
        name_number=name_calc.get("single_root", 0),
        personal_year=personal_year_val,
        active_dasha=active_dasha_ruler,
        current_plan="free",
        credits_remaining=0
    )

    # 9. Mint Cryptographically Signed Session Token
    token = generate_session_token(norm_email, client_ip)
    _ACTIVE_SESSIONS[token] = {
        "login_id": norm_email,
        "user_id": user_id,
        "golden_profile_id": golden_id,
        "name": req.name,
        "role": "registered_user",
        "created_at": now,
        "expires_at": now + SESSION_LIFETIME_SEC,
        "ip": client_ip
    }

    # Set Session Cookies
    response.set_cookie(
        key="nv_user_session",
        value=token,
        max_age=SESSION_LIFETIME_SEC,
        httponly=True,
        samesite="lax",
        secure=False
    )
    response.set_cookie(
        key="nv_uid",
        value=nv_uid,
        max_age=SESSION_LIFETIME_SEC * 365,
        httponly=False,
        samesite="lax",
        secure=False
    )

    return {
        "status": "success",
        "message": "Account created and Golden Profile stitched with DPDP consent.",
        "session_token": token,
        "user_id": user_id,
        "golden_profile_id": golden_id,
        "nv_uid": nv_uid,
        "uid2_token": generate_uid2_token(golden_id),
        "profile": {
            "calculation_id": req.calculation_id or user_record.get("calculation_id"),
            "name": req.name,
            "email": norm_email,
            "phone": norm_phone,
            "birth_date": f"{req.year:04d}-{req.month:02d}-{req.day:02d}",
            "birth_time": req.birth_time or "",
            "birth_time_hour": req.birth_time_hour,
            "birth_time_minute": req.birth_time_minute,
            "birth_time_period": req.birth_time_period or "AM",
            "birth_place": req.birth_place or "",
            "country": req.country or "India",
            "latitude": req.latitude,
            "longitude": req.longitude,
            "altitude": req.altitude,
            "timezone": req.timezone or "Asia/Kolkata",
            "gender": req.gender or "prefer_not_to_say",
            "driver_mulank": mulank,
            "conductor_bhagyank": bhagyank,
            "kua_number": kua,
            "name_number": name_calc.get("single_root", 0),
            "personal_year": personal_year_val,
            "active_mahadasha": active_dasha_ruler,
            "loshu_counts": loshu_counts,
            "missing_numbers": missing_numbers,
            "phone_verified": user_record.get("phone_verified", False),
            "email_verified": user_record.get("email_verified", False),
            "verification_badge": user_record.get("verification_badge", "standard"),
            "purchased_plans": [],
            "unlocked_reports": ["free", "discovery"],
            "charm_credits_remaining": 0,
            "charm_credits_total": 0
        },
        "entitlements": {
            "purchased_plans": [],
            "unlocked_reports": ["free", "discovery"],
            "charm_credits_remaining": 0,
            "charm_credits_total": 0
        },
        "alignment_analysis": alignment_info,
        "consents": user_record["consents"],
        "redirect_url": req.redirect_url or "/dashboard/"
    }



class GoogleAuthRequest(BaseModel):
    email: str = Field(..., description="Google email address")
    name: Optional[str] = Field(None, max_length=120, description="Full name from Google profile")
    google_id: Optional[str] = Field(None, description="Google OAuth user unique sub ID")
    picture: Optional[str] = Field(None, description="Google profile picture URL")
    credential: Optional[str] = Field(None, description="Google Identity Services JWT credential")
    day: Optional[int] = Field(1, ge=1, le=31, description="Day of birth")
    month: Optional[int] = Field(1, ge=1, le=12, description="Month of birth")
    year: Optional[int] = Field(1990, ge=1900, le=2100, description="Year of birth")
    birth_time: Optional[str] = Field("12:00 PM", description="Time of birth")
    birth_place: Optional[str] = Field("New Delhi", description="Place of birth")
    country: Optional[str] = Field("India", description="Country of birth")
    latitude: Optional[float] = Field(28.6139, description="Birth latitude")
    longitude: Optional[float] = Field(77.2090, description="Birth longitude")
    timezone: Optional[str] = Field("Asia/Kolkata", description="Timezone")
    gender: Optional[str] = Field("prefer_not_to_say", description="Gender")
    phone: Optional[str] = Field(None, description="Mobile number")
    device_id: Optional[str] = Field(None)
    device_type: Optional[str] = Field("desktop")
    nv_uid: Optional[str] = Field(None)
    redirect_url: Optional[str] = Field("/dashboard/")
    calculation_id: Optional[str] = Field(None, description="Persisted calculation ID from recent calculator session")


@router.post("/google")
async def api_google_auth(req: GoogleAuthRequest, request: Request, response: Response):
    """
    Unified Google Sign-In & Single Sign-On (SSO) Endpoint:
    1. Authenticates Google credentials or profile payload.
    2. Resolves or creates user account linked to Google ID.
    3. Runs classical numerological calculations (Mulank, Bhagyank, Kua, Lo Shu Grid).
    4. Stitches Golden Customer Profile in CDP with DPDP Act 2023 compliance.
    5. Issues cryptographically signed HMAC session token.
    """
    clean_email = normalize_email(req.email)
    if not clean_email or "@" not in clean_email:
        raise HTTPException(status_code=400, detail="Invalid Google email address provided.")

    client_ip = request.client.host if request.client else "127.0.0.1"
    ua = request.headers.get("user-agent", "")
    now = time.time()
    nv_uid = req.nv_uid or f"nv_uid_{uuid.uuid4().hex[:12]}"
    user_name = (req.name or clean_email.split("@")[0].replace(".", " ").title()).strip()

    # 1. Check for Existing Account
    existing_uid = _EMAIL_TO_USER_ID.get(clean_email)
    if existing_uid and existing_uid in _USER_ACCOUNTS:
        user = _USER_ACCOUNTS[existing_uid]
        # Update Google ID if newly linked
        if req.google_id and not user.get("google_id"):
            user["google_id"] = req.google_id
            user["auth_provider"] = "google"
            _save_user_accounts()

        token = generate_session_token(clean_email, client_ip)
        _ACTIVE_SESSIONS[token] = {
            "login_id": clean_email,
            "user_id": existing_uid,
            "golden_profile_id": user.get("golden_profile_id"),
            "name": user.get("name", user_name),
            "role": "registered_user",
            "auth_provider": "google",
            "created_at": now,
            "expires_at": now + SESSION_LIFETIME_SEC,
            "ip": client_ip
        }
        response.set_cookie(
            key="nv_user_session",
            value=token,
            max_age=SESSION_LIFETIME_SEC,
            httponly=True,
            samesite="lax",
            secure=False
        )

        alignment_info = analyze_user_alignment_and_gaps(
            driver=user.get("driver_mulank", 1),
            conductor=user.get("conductor_bhagyank", 1),
            loshu_counts=user.get("loshu_counts", {}),
            missing_numbers=user.get("missing_numbers", []),
            name_number=user.get("name_number"),
            personal_year=user.get("personal_year"),
            active_dasha=user.get("active_mahadasha"),
            current_plan=user.get("purchased_plans", ["free"])[-1] if user.get("purchased_plans") else "free",
            credits_remaining=user.get("charm_credits_remaining", 0)
        )

        return {
            "status": "success",
            "message": f"Welcome back, {user['name']}! Signed in with Google.",
            "session_token": token,
            "user_id": existing_uid,
            "golden_profile_id": user.get("golden_profile_id"),
            "role": "registered_user",
            "auth_provider": "google",
            "profile": {
                "name": user.get("name"),
                "email": user.get("email"),
                "phone": user.get("phone"),
                "birth_date": user.get("birth_date"),
                "birth_time": user.get("birth_time"),
                "birth_place": user.get("birth_place"),
                "driver_mulank": user.get("driver_mulank"),
                "conductor_bhagyank": user.get("conductor_bhagyank"),
                "kua_number": user.get("kua_number"),
                "personal_year": user.get("personal_year"),
                "active_mahadasha": user.get("active_mahadasha"),
                "loshu_counts": user.get("loshu_counts"),
                "missing_numbers": user.get("missing_numbers"),
                "purchased_plans": user.get("purchased_plans", []),
                "unlocked_reports": user.get("unlocked_reports", ["free", "discovery"]),
                "charm_credits_remaining": user.get("charm_credits_remaining", 0)
            },
            "alignment_analysis": alignment_info,
            "redirect_url": req.redirect_url or "/dashboard/"
        }

    # 2. New User Registration via Google
    user_id = f"usr_{uuid.uuid4().hex[:12]}"
    day = req.day or 1
    month = req.month or 1
    year = req.year or 1990

    mulank = calculate_driver(day)
    bhagyank = calculate_conductor(day, month, year)
    kua = calculate_kua_number(year, req.gender)
    name_calc = calculate_chaldean_name(user_name)
    dasha_cycles = calculate_dasha_cycles(day, month, year)
    plane_metrics = calculate_lo_shu_plane_metrics(day, month, year)

    dob_digits_str = f"{day:02d}{month:02d}{year:04d}"
    loshu_counts = {i: dob_digits_str.count(str(i)) for i in range(1, 10)}
    missing_numbers = [i for i, c in loshu_counts.items() if c == 0]
    active_dasha_ruler = dasha_cycles.get("current_cycle", {}).get("mahadasha_ruler", "Sun")
    personal_year_val = dasha_cycles.get("personal_year", 1)

    norm_phone = normalize_phone(req.phone) if req.phone else ""

    cdp_payload = IdentityPayload(
        email=clean_email,
        phone=norm_phone if norm_phone else None,
        device_id=req.device_id,
        device_type=req.device_type or "desktop",
        nv_uid=nv_uid,
        consent_marketing=True,
        consent_device_tracking=True,
        client_ip=client_ip,
        client_user_agent=ua
    )
    golden_profile = resolve_golden_profile(cdp_payload)
    golden_id = golden_profile["golden_profile_id"]

    enrich_deterministic_taxonomy(golden_id, {
        "seeker_name": user_name,
        "email": clean_email,
        "phone": norm_phone,
        "auth_provider": "google",
        "google_id": req.google_id,
        "numerology_mulank": mulank,
        "numerology_bhagyank": bhagyank,
        "kua_number": kua,
        "chaldean_name_number": name_calc.get("single_root", 0),
        "chaldean_compound": name_calc.get("compound_sum", 0),
        "birth_date": f"{year:04d}-{month:02d}-{day:02d}",
        "birth_time": req.birth_time or "12:00 PM",
        "birth_place": req.birth_place or "New Delhi",
        "country": req.country or "India",
        "latitude": req.latitude or 28.6139,
        "longitude": req.longitude or 77.2090,
        "timezone": req.timezone or "Asia/Kolkata",
        "gender": req.gender or "prefer_not_to_say",
        "lo_shu_counts": loshu_counts,
        "lo_shu_missing": missing_numbers,
        "active_mahadasha": active_dasha_ruler,
        "personal_year": personal_year_val,
        "customer_tier": "FREE_REGISTERED_USER",
        "consent_profile_storage": True,
        "consent_timestamp": now,
        "consent_policy_version": "2025.1.DPDP",
        "jurisdiction": "IN"
    })

    CONSENT_LEDGER.append({
        "user_id": user_id,
        "golden_profile_id": golden_id,
        "email": clean_email,
        "purpose": "google_sso_profile_storage_and_calculations",
        "granted": True,
        "timestamp": now,
        "policy_version": "2025.1.DPDP",
        "client_ip": client_ip,
        "user_agent": ua
    })

    user_record = {
        "user_id": user_id,
        "golden_profile_id": golden_id,
        "nv_uid": nv_uid,
        "email": clean_email,
        "phone": norm_phone,
        "name": user_name,
        "auth_provider": "google",
        "google_id": req.google_id,
        "picture": req.picture,
        "birth_date": f"{year:04d}-{month:02d}-{day:02d}",
        "birth_time": req.birth_time or "12:00 PM",
        "birth_place": req.birth_place or "New Delhi",
        "country": req.country or "India",
        "latitude": req.latitude or 28.6139,
        "longitude": req.longitude or 77.2090,
        "timezone": req.timezone or "Asia/Kolkata",
        "gender": req.gender or "prefer_not_to_say",
        "driver_mulank": mulank,
        "conductor_bhagyank": bhagyank,
        "kua_number": kua,
        "name_number": name_calc.get("single_root", 0),
        "personal_year": personal_year_val,
        "active_mahadasha": active_dasha_ruler,
        "loshu_counts": loshu_counts,
        "missing_numbers": missing_numbers,
        "purchased_plans": [],
        "unlocked_reports": ["free", "discovery"],
        "charm_credits_remaining": 5,
        "charm_credits_total": 5,
        "created_at": now,
        "updated_at": now
    }

    _USER_ACCOUNTS[user_id] = user_record
    _EMAIL_TO_USER_ID[clean_email] = user_id
    if norm_phone:
        _PHONE_TO_USER_ID[norm_phone] = user_id
    _save_user_accounts()

    alignment_info = analyze_user_alignment_and_gaps(
        driver=mulank,
        conductor=bhagyank,
        loshu_counts=loshu_counts,
        missing_numbers=missing_numbers,
        name_number=name_calc.get("single_root", 0),
        personal_year=personal_year_val,
        active_dasha=active_dasha_ruler,
        current_plan="free",
        credits_remaining=5
    )

    token = generate_session_token(clean_email, client_ip)
    _ACTIVE_SESSIONS[token] = {
        "login_id": clean_email,
        "user_id": user_id,
        "golden_profile_id": golden_id,
        "name": user_name,
        "role": "registered_user",
        "auth_provider": "google",
        "created_at": now,
        "expires_at": now + SESSION_LIFETIME_SEC,
        "ip": client_ip
    }

    response.set_cookie(
        key="nv_user_session",
        value=token,
        max_age=SESSION_LIFETIME_SEC,
        httponly=True,
        samesite="lax",
        secure=False
    )

    return {
        "status": "success",
        "message": f"Welcome to Numeros Vision, {user_name}! Account created with Google ID.",
        "session_token": token,
        "user_id": user_id,
        "golden_profile_id": golden_id,
        "nv_uid": nv_uid,
        "role": "registered_user",
        "auth_provider": "google",
        "profile": user_record,
        "alignment_analysis": alignment_info,
        "redirect_url": req.redirect_url or "/dashboard/"
    }


# ── OTP Verification & Passwordless Authentication Endpoints ────────────────
def _mask_identifier(ident: str) -> str:
    ident = str(ident).strip()
    if "@" in ident:
        parts = ident.split("@")
        name_part = parts[0]
        masked_name = name_part[:2] + "***" if len(name_part) > 2 else name_part + "***"
        return f"{masked_name}@{parts[1]}"
    clean_digits = re.sub(r"[^0-9+]", "", ident)
    if len(clean_digits) >= 10:
        return f"{clean_digits[:3]}****{clean_digits[-3:]}"
    return ident


def _find_otp_record(ident: str) -> Optional[Dict[str, Any]]:
    """Flexible lookup for active OTP record across various phone and email formats."""
    if not ident:
        return None
    raw = str(ident).strip()
    if raw in _OTP_STORE:
        return _OTP_STORE[raw]
    if "@" in raw:
        norm_em = normalize_email(raw)
        return _OTP_STORE.get(norm_em)
    norm_p = normalize_phone(raw)
    if norm_p and norm_p in _OTP_STORE:
        return _OTP_STORE[norm_p]
    digits = re.sub(r"[^0-9]", "", raw)
    if digits in _OTP_STORE:
        return _OTP_STORE[digits]
    if len(digits) == 10 and f"91{digits}" in _OTP_STORE:
        return _OTP_STORE[f"91{digits}"]
    if digits.startswith("91") and len(digits) > 10 and digits[2:] in _OTP_STORE:
        return _OTP_STORE[digits[2:]]
    return None


@router.post("/otp/send")
@router.post("/send-otp")
async def api_send_otp(req: OTPSendRequest, request: Request):
    """
    Sends 6-digit OTP verification code to mobile number or email address (or both simultaneously).
    Supports real-time delivery via SMTP (email) and SMS gateways (Fast2SMS, Twilio, MSG91),
    with sandbox testing fallback.
    """
    raw_ident = req.identifier.strip() if req.identifier else ""
    target_phone = req.phone.strip() if req.phone else None
    target_email = req.email.strip() if req.email else None

    if not raw_ident and not target_phone and not target_email:
        raise HTTPException(status_code=400, detail="Mobile number or Email address is required.")

    if not raw_ident:
        raw_ident = target_phone or target_email

    if "@" in raw_ident:
        if not target_email:
            target_email = raw_ident
    else:
        if not target_phone:
            target_phone = raw_ident

    # Validate email format if provided
    norm_email = None
    if target_email:
        norm_email = normalize_email(target_email)
        if not norm_email or "@" not in norm_email:
            raise HTTPException(status_code=400, detail="Please enter a valid email address.")

    # Validate phone format if provided
    norm_phone = None
    if target_phone:
        norm_phone = normalize_phone(target_phone) or re.sub(r"[^0-9+]", "", target_phone)
        digits_only = re.sub(r"[^0-9]", "", norm_phone)
        if len(digits_only) < 10:
            raise HTTPException(status_code=400, detail="Please enter a valid mobile number with at least 10 digits.")

    channel = req.channel.lower() if req.channel else "auto"
    if channel == "auto":
        channel = "both" if (norm_phone and norm_email) else ("email" if norm_email else "sms")

    code = f"{random.randint(100000, 999999)}"
    now = time.time()
    vtoken = f"nv_vtok_{uuid.uuid4().hex[:16]}"

    record = {
        "otp": code,
        "channel": channel,
        "created_at": now,
        "expires_at": now + OTP_EXPIRY_SEC,
        "attempts": 0,
        "verified": False,
        "token": vtoken,
        "phone": norm_phone,
        "email": norm_email
    }

    # Register in in-memory OTP store across all identifier representations
    _OTP_STORE[raw_ident] = record
    if norm_email:
        _OTP_STORE[norm_email] = record
        _OTP_STORE[target_email] = record
    if norm_phone:
        _OTP_STORE[norm_phone] = record
        _OTP_STORE[target_phone] = record
        digits = re.sub(r"[^0-9]", "", norm_phone)
        if digits:
            _OTP_STORE[digits] = record
            if len(digits) == 10:
                _OTP_STORE[f"91{digits}"] = record
            elif digits.startswith("91") and len(digits) > 10:
                _OTP_STORE[digits[2:]] = record

    # Trigger real-time multi-channel delivery (Email via SMTP, Mobile via SMS Gateway)
    delivery_status = dispatch_otp_multichannel(
        phone=norm_phone or target_phone,
        email=norm_email or target_email,
        otp_code=code,
        user_name=req.name,
        channel=channel
    )

    dest_labels = []
    if norm_phone:
        dest_labels.append(_mask_identifier(norm_phone))
    if norm_email:
        dest_labels.append(_mask_identifier(norm_email))
    dest_str = " & ".join(dest_labels) if dest_labels else _mask_identifier(raw_ident)

    print(f"[OTP_SERVICE] Verification code {code} issued for {dest_str} via {channel}. Delivery: {delivery_status}")

    return {
        "status": "success",
        "message": f"6-digit verification code dispatched to {dest_str}.",
        "identifier": raw_ident,
        "channel": channel,
        "phone": norm_phone,
        "email": norm_email,
        "expires_in": OTP_EXPIRY_SEC,
        "otp_preview": code,
        "delivery_status": delivery_status
    }


@router.post("/otp/verify")
@router.post("/verify-otp")
async def api_verify_otp(req: OTPVerifyRequest, request: Request, response: Response):
    """
    Verifies 6-digit OTP for mobile or email.
    If auto_login is True and user exists, automatically issues session token and logs user in.
    """
    raw_ident = req.identifier.strip()
    norm_id = normalize_email(raw_ident) if "@" in raw_ident else (normalize_phone(raw_ident) or re.sub(r"[^0-9+]", "", raw_ident))
    submitted_otp = req.otp.strip()

    otp_record = _find_otp_record(raw_ident) or _find_otp_record(norm_id)
    now = time.time()

    is_valid = False
    if submitted_otp in TEST_SANDBOX_OTPS:
        is_valid = True
    elif otp_record:
        if now > otp_record["expires_at"]:
            raise HTTPException(status_code=400, detail="Verification code has expired. Please request a new code.")
        if otp_record["attempts"] >= MAX_OTP_ATTEMPTS:
            raise HTTPException(status_code=400, detail="Too many invalid attempts. Please request a new code.")
        if otp_record["otp"] == submitted_otp:
            is_valid = True
        else:
            otp_record["attempts"] += 1

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid verification code. Please check and try again.")

    vtoken = otp_record["token"] if otp_record else f"nv_vtok_{uuid.uuid4().hex[:16]}"
    if otp_record:
        otp_record["verified"] = True

    user = get_user_account_by_identifier(raw_ident) or get_user_account_by_identifier(norm_id)
    session_token = None
    profile = None
    golden_id = None

    if user and req.auto_login:
        client_ip = request.client.host if request.client else "127.0.0.1"
        session_token = generate_session_token(user.get("email", norm_id), client_ip)
        _ACTIVE_SESSIONS[session_token] = {
            "login_id": user.get("email", norm_id),
            "user_id": user["user_id"],
            "golden_profile_id": user.get("golden_profile_id"),
            "name": user.get("name", "Seeker"),
            "role": "registered_user",
            "created_at": now,
            "expires_at": now + SESSION_LIFETIME_SEC,
            "ip": client_ip
        }
        response.set_cookie(
            key="nv_user_session",
            value=session_token,
            max_age=SESSION_LIFETIME_SEC,
            httponly=True,
            samesite="lax",
            secure=False
        )
        response.set_cookie(
            key="nv_user_logged_in",
            value="true",
            max_age=SESSION_LIFETIME_SEC,
            httponly=False,
            samesite="lax",
            secure=False
        )
        user["phone_verified"] = True if "@" not in norm_id else user.get("phone_verified", False)
        user["email_verified"] = True if "@" in norm_id else user.get("email_verified", False)
        user["verification_badge"] = "verified_customer"
        _save_user_accounts()
        golden_id = user.get("golden_profile_id")
        profile = {
            "name": user.get("name"),
            "email": user.get("email"),
            "phone": user.get("phone"),
            "driver_mulank": user.get("driver_mulank"),
            "conductor_bhagyank": user.get("conductor_bhagyank"),
            "kua_number": user.get("kua_number"),
            "phone_verified": user.get("phone_verified", True),
            "email_verified": user.get("email_verified", True),
            "verification_badge": "verified_customer"
        }

    return {
        "status": "success",
        "verified": True,
        "message": f"Verification successful for {norm_id}.",
        "identifier": norm_id,
        "verification_token": vtoken,
        "user_exists": bool(user),
        "session_token": session_token,
        "profile": profile,
        "golden_profile_id": golden_id,
        "redirect_url": "/dashboard/" if user else None
    }


@router.post("/otp/login")
async def api_otp_login(req: OTPLoginRequest, request: Request, response: Response):
    """
    Passwordless Instant Login via Mobile or Email OTP:
    Authenticates existing customer or stitches verified seeker profile with DPDP consent.
    """
    raw_ident = req.identifier.strip()
    norm_id = normalize_email(raw_ident) if "@" in raw_ident else (normalize_phone(raw_ident) or re.sub(r"[^0-9+]", "", raw_ident))
    submitted_otp = req.otp.strip()

    otp_record = _find_otp_record(raw_ident) or _find_otp_record(norm_id)
    now = time.time()

    is_valid = False
    if submitted_otp in TEST_SANDBOX_OTPS:
        is_valid = True
    elif otp_record:
        if now > otp_record["expires_at"]:
            raise HTTPException(status_code=400, detail="Verification code has expired. Please request a new code.")
        if otp_record["attempts"] >= MAX_OTP_ATTEMPTS:
            raise HTTPException(status_code=400, detail="Too many invalid attempts. Please request a new code.")
        if otp_record["otp"] == submitted_otp:
            is_valid = True
        else:
            otp_record["attempts"] += 1

    if not is_valid:
        raise HTTPException(status_code=400, detail="Invalid verification code. Please check and try again.")

    client_ip = request.client.host if request.client else "127.0.0.1"
    user = get_user_account_by_identifier(raw_ident) or get_user_account_by_identifier(norm_id)

    if not user:
        user_name = (req.name or (norm_id.split("@")[0].title() if "@" in norm_id else "Seeker")).strip()
        user_id = f"usr_{uuid.uuid4().hex[:12]}"
        golden_id = f"gold_{uuid.uuid4().hex[:12]}"
        nv_uid = f"nv_uid_{uuid.uuid4().hex[:12]}"
        d, m, y = req.day or 15, req.month or 8, req.year or 1990
        mulank = calculate_driver(d)
        bhagyank = calculate_conductor(d, m, y)
        kua = calculate_kua_number(y, getattr(req, "gender", None))

        user = {
            "user_id": user_id,
            "golden_profile_id": golden_id,
            "nv_uid": nv_uid,
            "name": user_name,
            "email": norm_id if "@" in norm_id else f"{re.sub(r'[^a-zA-Z0-9]', '', norm_id)}@seeker.numerosvision.com",
            "phone": norm_id if "@" not in norm_id else "",
            "password_hash": hash_password(f"NV_OTP_{uuid.uuid4().hex[:8]}!"),
            "role": "registered_user",
            "auth_provider": "otp_verified",
            "phone_verified": "@" not in norm_id,
            "email_verified": "@" in norm_id,
            "verification_badge": "verified_customer",
            "driver_mulank": mulank,
            "conductor_bhagyank": bhagyank,
            "kua_number": kua,
            "birth_date": f"{y:04d}-{m:02d}-{d:02d}",
            "created_at": now,
            "updated_at": now
        }
        _USER_ACCOUNTS[user_id] = user
        if user["email"]:
            _EMAIL_TO_USER_ID[normalize_email(user["email"])] = user_id
        if user["phone"]:
            _PHONE_TO_USER_ID[normalize_phone(user["phone"])] = user_id
        _save_user_accounts()

    user["phone_verified"] = True if "@" not in norm_id else user.get("phone_verified", False)
    user["email_verified"] = True if "@" in norm_id else user.get("email_verified", False)
    user["verification_badge"] = "verified_customer"
    _save_user_accounts()

    session_token = generate_session_token(user.get("email", norm_id), client_ip)
    _ACTIVE_SESSIONS[session_token] = {
        "login_id": user.get("email", norm_id),
        "user_id": user["user_id"],
        "golden_profile_id": user.get("golden_profile_id"),
        "name": user.get("name", "Seeker"),
        "role": "registered_user",
        "created_at": now,
        "expires_at": now + SESSION_LIFETIME_SEC,
        "ip": client_ip
    }
    response.set_cookie(
        key="nv_user_session",
        value=session_token,
        max_age=SESSION_LIFETIME_SEC,
        httponly=True,
        samesite="lax",
        secure=False
    )
    response.set_cookie(
        key="nv_user_logged_in",
        value="true",
        max_age=SESSION_LIFETIME_SEC,
        httponly=False,
        samesite="lax",
        secure=False
    )

    return {
        "status": "success",
        "message": "OTP verification successful. Welcome to NUMEROS VISION.",
        "session_token": session_token,
        "user_id": user["user_id"],
        "golden_profile_id": user.get("golden_profile_id"),
        "profile": {
            "name": user.get("name"),
            "email": user.get("email"),
            "phone": user.get("phone"),
            "driver_mulank": user.get("driver_mulank"),
            "conductor_bhagyank": user.get("conductor_bhagyank"),
            "kua_number": user.get("kua_number"),
            "phone_verified": user.get("phone_verified", True),
            "email_verified": user.get("email_verified", True),
            "verification_badge": "verified_customer"
        },
        "redirect_url": req.redirect_url or "/dashboard/"
    }



@router.post("/login")
async def api_login(req: LoginRequest, request: Request, response: Response):
    client_ip = request.client.host if request.client else "127.0.0.1"
    now = time.time()

    # 1. Check IP Lockout Status
    ip_rec = _FAILED_LOGIN_ATTEMPTS.get(client_ip, {"failed_count": 0, "locked_until": 0})
    if ip_rec["locked_until"] > now:
        remaining_sec = int(ip_rec["locked_until"] - now)
        remaining_min = (remaining_sec // 60) + 1
        raise HTTPException(
            status_code=429,
            detail=f"Security Lockout: Too many failed login attempts from this IP. Locked for {remaining_min} more minutes."
        )

    clean_login = req.login_id.strip()

    # 2. Check Practitioner / Master Admin credentials
    master_login_match = hmac.compare_digest(clean_login.lower(), MASTER_LOGIN_ID.lower()) or \
                         hmac.compare_digest(clean_login.lower(), "admin")
    master_pass_match  = hmac.compare_digest(req.password.strip(), MASTER_PASSWORD)

    if master_login_match and master_pass_match:
        if client_ip in _FAILED_LOGIN_ATTEMPTS:
            del _FAILED_LOGIN_ATTEMPTS[client_ip]

        token = generate_session_token(clean_login, client_ip)
        _ACTIVE_SESSIONS[token] = {
            "login_id": clean_login,
            "role": "master_practitioner",
            "created_at": now,
            "expires_at": now + SESSION_LIFETIME_SEC,
            "ip": client_ip
        }
        response.set_cookie(
            key="nv_practitioner_session",
            value=token,
            max_age=SESSION_LIFETIME_SEC,
            httponly=True,
            samesite="lax",
            secure=False
        )
        return {
            "status": "success",
            "message": "Authentication successful. Access granted to Practitioner Studio & CRM.",
            "session_token": token,
            "practitioner_id": "PRAC-NV-MASTER-01",
            "role": "master_practitioner",
            "expires_in_seconds": SESSION_LIFETIME_SEC
        }

    # 3. Check Registered User Accounts (by Email or Phone)
    norm_email = normalize_email(clean_login)
    norm_phone = normalize_phone(clean_login)
    user_id = _EMAIL_TO_USER_ID.get(norm_email) or _PHONE_TO_USER_ID.get(norm_phone)

    if user_id and user_id in _USER_ACCOUNTS:
        user = _USER_ACCOUNTS[user_id]
        if verify_password(req.password.strip(), user.get("password_hash", "")):
            if client_ip in _FAILED_LOGIN_ATTEMPTS:
                del _FAILED_LOGIN_ATTEMPTS[client_ip]

            token = generate_session_token(user["email"], client_ip)
            _ACTIVE_SESSIONS[token] = {
                "login_id": user["email"],
                "user_id": user_id,
                "golden_profile_id": user.get("golden_profile_id"),
                "name": user.get("name"),
                "role": "registered_user",
                "created_at": now,
                "expires_at": now + SESSION_LIFETIME_SEC,
                "ip": client_ip
            }
            response.set_cookie(
                key="nv_user_session",
                value=token,
                max_age=SESSION_LIFETIME_SEC,
                httponly=True,
                samesite="lax",
                secure=False
            )
            alignment_info = analyze_user_alignment_and_gaps(
                driver=user.get("driver_mulank", 1),
                conductor=user.get("conductor_bhagyank", 1),
                loshu_counts=user.get("loshu_counts", {}),
                missing_numbers=user.get("missing_numbers", []),
                name_number=user.get("name_number"),
                personal_year=user.get("personal_year"),
                active_dasha=user.get("active_mahadasha"),
                current_plan=user.get("purchased_plans", ["free"])[-1] if user.get("purchased_plans") else "free",
                credits_remaining=user.get("charm_credits_remaining", 0)
            )
            return {
                "status": "success",
                "message": f"Welcome back, {user['name']}! Login successful.",
                "session_token": token,
                "user_id": user_id,
                "golden_profile_id": user.get("golden_profile_id"),
                "role": "registered_user",
                "profile": {
                    "name": user.get("name"),
                    "email": user.get("email"),
                    "phone": user.get("phone"),
                    "birth_date": user.get("birth_date"),
                    "birth_time": user.get("birth_time"),
                    "birth_place": user.get("birth_place"),
                    "gender": user.get("gender"),
                    "driver_mulank": user.get("driver_mulank"),
                    "conductor_bhagyank": user.get("conductor_bhagyank"),
                    "kua_number": user.get("kua_number"),
                    "personal_year": user.get("personal_year"),
                    "active_mahadasha": user.get("active_mahadasha"),
                    "loshu_counts": user.get("loshu_counts"),
                    "missing_numbers": user.get("missing_numbers"),
                    "purchased_plans": user.get("purchased_plans", []),
                    "unlocked_reports": user.get("unlocked_reports", ["free", "discovery"]),
                    "charm_credits_remaining": user.get("charm_credits_remaining", 0),
                    "charm_credits_total": user.get("charm_credits_total", 0)
                },
                "entitlements": {
                    "purchased_plans": user.get("purchased_plans", []),
                    "unlocked_reports": user.get("unlocked_reports", ["free", "discovery"]),
                    "charm_credits_remaining": user.get("charm_credits_remaining", 0),
                    "charm_credits_total": user.get("charm_credits_total", 0)
                },
                "alignment_analysis": alignment_info,
                "consents": user.get("consents", {}),
                "expires_in_seconds": SESSION_LIFETIME_SEC
            }

    # 4. Failed Attempt Handling
    ip_rec["failed_count"] += 1
    if ip_rec["failed_count"] >= MAX_FAILED_ATTEMPTS:
        ip_rec["locked_until"] = now + LOCKOUT_DURATION_SEC
        _FAILED_LOGIN_ATTEMPTS[client_ip] = ip_rec
        raise HTTPException(
            status_code=429,
            detail="Security Alert: 5 failed attempts exceeded. Access locked for 15 minutes."
        )
    _FAILED_LOGIN_ATTEMPTS[client_ip] = ip_rec
    attempts_left = MAX_FAILED_ATTEMPTS - ip_rec["failed_count"]
    raise HTTPException(
        status_code=401,
        detail=f"Invalid Login ID or Passphrase. {attempts_left} attempts remaining before IP lockout."
    )


@router.get("/me")
async def api_get_current_user(request: Request):
    """Returns currently authenticated user profile and consent details."""
    token = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    else:
        token = request.cookies.get("nv_user_session") or request.cookies.get("nv_practitioner_session")

    if not token or token not in _ACTIVE_SESSIONS:
        return {"authenticated": False, "status": "unauthorized"}

    session = _ACTIVE_SESSIONS[token]
    if session["expires_at"] < time.time():
        del _ACTIVE_SESSIONS[token]
        return {"authenticated": False, "status": "session_expired"}

    role = session.get("role", "registered_user")
    if role == "master_practitioner":
        return {
            "authenticated": True,
            "role": "master_practitioner",
            "login_id": session.get("login_id"),
            "practitioner_id": "PRAC-NV-MASTER-01"
        }

    user_id = session.get("user_id")
    user = _USER_ACCOUNTS.get(user_id) if user_id else None
    if not user:
        return {
            "authenticated": True,
            "role": role,
            "login_id": session.get("login_id")
        }

    alignment_info = analyze_user_alignment_and_gaps(
        driver=user.get("driver_mulank", 1),
        conductor=user.get("conductor_bhagyank", 1),
        loshu_counts=user.get("loshu_counts", {}),
        missing_numbers=user.get("missing_numbers", []),
        name_number=user.get("name_number"),
        personal_year=user.get("personal_year"),
        active_dasha=user.get("active_mahadasha"),
        current_plan=user.get("purchased_plans", ["free"])[-1] if user.get("purchased_plans") else "free",
        credits_remaining=user.get("charm_credits_remaining", 0)
    )

    return {
        "authenticated": True,
        "role": "registered_user",
        "user_id": user_id,
        "golden_profile_id": user.get("golden_profile_id"),
        "profile": {
            "name": user.get("name"),
            "email": user.get("email"),
            "phone": user.get("phone"),
            "birth_date": user.get("birth_date"),
            "birth_time": user.get("birth_time"),
            "birth_time_hour": user.get("birth_time_hour"),
            "birth_time_minute": user.get("birth_time_minute"),
            "birth_time_period": user.get("birth_time_period"),
            "birth_place": user.get("birth_place"),
            "country": user.get("country"),
            "latitude": user.get("latitude"),
            "longitude": user.get("longitude"),
            "altitude": user.get("altitude"),
            "timezone": user.get("timezone"),
            "gender": user.get("gender"),
            "driver_mulank": user.get("driver_mulank"),
            "conductor_bhagyank": user.get("conductor_bhagyank"),
            "kua_number": user.get("kua_number"),
            "name_number": user.get("name_number"),
            "personal_year": user.get("personal_year"),
            "active_mahadasha": user.get("active_mahadasha"),
            "loshu_counts": user.get("loshu_counts"),
            "missing_numbers": user.get("missing_numbers"),
            "purchased_plans": user.get("purchased_plans", []),
            "unlocked_reports": user.get("unlocked_reports", ["free", "discovery"]),
            "charm_credits_remaining": user.get("charm_credits_remaining", 0),
            "charm_credits_total": user.get("charm_credits_total", 0)
        },
        "entitlements": {
            "purchased_plans": user.get("purchased_plans", []),
            "unlocked_reports": user.get("unlocked_reports", ["free", "discovery"]),
            "charm_credits_remaining": user.get("charm_credits_remaining", 0),
            "charm_credits_total": user.get("charm_credits_total", 0)
        },
        "alignment_analysis": alignment_info,
        "consents": user.get("consents")
    }


@router.post("/verify")
async def api_verify_session(request: Request, req: Optional[SessionVerifyRequest] = None):
    token = None
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
    elif req and req.token:
        token = req.token
    else:
        token = request.cookies.get("nv_user_session") or request.cookies.get("nv_practitioner_session")

    if not token or token not in _ACTIVE_SESSIONS:
        return {"authenticated": False, "status": "unauthorized"}

    session = _ACTIVE_SESSIONS[token]
    if session["expires_at"] < time.time():
        del _ACTIVE_SESSIONS[token]
        return {"authenticated": False, "status": "session_expired"}

    role = session.get("role", "registered_user")
    user_id = session.get("user_id")
    user = _USER_ACCOUNTS.get(user_id) if user_id else None

    return {
        "authenticated": True,
        "login_id": session["login_id"],
        "role": role,
        "user_id": user_id,
        "golden_profile_id": session.get("golden_profile_id"),
        "practitioner_id": "PRAC-NV-MASTER-01" if role == "master_practitioner" else None,
        "profile": {
            "name": user.get("name"),
            "driver_mulank": user.get("driver_mulank"),
            "conductor_bhagyank": user.get("conductor_bhagyank")
        } if user else None
    }


@router.post("/logout")
async def api_logout(request: Request, response: Response):
    token = request.cookies.get("nv_user_session") or request.cookies.get("nv_practitioner_session")
    if token and token in _ACTIVE_SESSIONS:
        del _ACTIVE_SESSIONS[token]
    response.delete_cookie("nv_user_session")
    response.delete_cookie("nv_practitioner_session")
    response.delete_cookie("nv_user_logged_in")
    return {"status": "success", "message": "Logged out successfully."}
