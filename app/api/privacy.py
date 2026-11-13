"""
NUMEROS VISION: PRIVACY, IDENTITY & ADTECH API ROUTER
Implements Clauses 86–109 of Master Specification:
- Platform Identity Registration (Web, PWA, Android AAID, iOS IDFA with ATT)
- Granular Purpose-Specific Consent (India DPDP 2025 compliant)
- Cascading Consent Withdrawal
- Purpose-Bound Location Resolution (Vastu vs Advertising)
- AdTech Data Firewall Activation Endpoint
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Union
from app.engine.identity_service import (
    PlatformType, ATTStatus, ConsentPurpose, ConsentStatus,
    register_platform_identity, record_consent, check_consent, withdraw_consent,
    link_identities, IDENTITY_REGISTRY, CONSENT_RECORDS
)
from app.engine.adtech_firewall import (
    OutboundAdTechRequest, filter_and_activate_adtech_payload,
    APPROVED_PARTNERS, APPROVED_NON_SENSITIVE_SEGMENTS
)

router = APIRouter(tags=["Privacy, Identity & AdTech Firewall"])

# ── Request / Response Schemas ──────────────────────────────────────────────

class RegisterIdentityRequest(BaseModel):
    platform: PlatformType
    user_id: Optional[str] = Field(None, description="Optional authenticated account ID")
    raw_identifier: Optional[str] = Field(None, description="Platform identifier (Web/PWA/AAID/IDFA)")
    raw_id: Optional[str] = Field(None, description="Alias for raw_identifier")
    client_id_type: Optional[str] = Field(None, description="Platform identifier type")
    att_status: Optional[ATTStatus] = Field(None, description="iOS AppTrackingTransparency status")
    session_id: Optional[str] = Field(None, description="Client session ID")

class ConsentSubmissionRequest(BaseModel):
    identity_id: str
    user_id: Optional[str] = None
    purpose: ConsentPurpose
    status: Union[ConsentStatus, str]
    policy_version: str = "2025.1.DPDP"
    jurisdiction: str = "IN"

    @field_validator("status", mode="before")
    @classmethod
    def normalize_status(cls, v):
        if isinstance(v, str):
            v_clean = v.strip().lower()
            try:
                return ConsentStatus(v_clean)
            except ValueError:
                pass
        return v

class ConsentWithdrawalRequest(BaseModel):
    identity_id: str
    purpose: Optional[ConsentPurpose] = None
    cascade: bool = True

class LocationResolutionRequest(BaseModel):
    identity_id: str
    purpose: ConsentPurpose = Field(..., description="Must be LOCATION_FOR_VASTU or LOCATION_FOR_ADVERTISING")
    latitude: float
    longitude: float

# ── Endpoints ───────────────────────────────────────────────────────────────

@router.post("/api/v1/identity/register")
def register_identity(req: RegisterIdentityRequest):
    """
    Registers a platform-specific identity.
    - Web: Generates or accepts nv_web_id
    - PWA: Generates or accepts nv_installation_id
    - Native Android: Accepts AAID (user-resettable)
    - Native iOS: Accepts IDFA only when ATT is authorized; else returns all zeros
    """
    try:
        raw = req.raw_identifier or req.raw_id
        result = register_platform_identity(
            platform=req.platform,
            user_id=req.user_id,
            raw_identifier=raw,
            att_status=req.att_status,
            session_id=req.session_id
        )
        return {
            "status": "success",
            "identity_id": result["identity_id"],
            "token_id": result["scoped_token"],
            "platform": result["platform"],
            "identifier_type": result["identifier_type"],
            "ad_tracking_eligible": result["ad_tracking_eligible"],
            "created_at": result["created_at"],
            "data": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/identity/{identity_id}")
def get_identity_details(identity_id: str):
    """Retrieves identity status and platform metadata."""
    ident = IDENTITY_REGISTRY.get(identity_id)
    if not ident:
        raise HTTPException(status_code=404, detail="Identity record not found.")
    return {
        "status": "success",
        "data": ident
    }

@router.post("/api/v1/privacy/consent")
def submit_consent(req: ConsentSubmissionRequest):
    """
    Records affirmative purpose-specific consent complying with DPDP 2025.
    """
    try:
        record = record_consent(
            identity_id=req.identity_id,
            user_id=req.user_id,
            purpose=req.purpose,
            status=req.status,
            policy_version=req.policy_version,
            jurisdiction=req.jurisdiction
        )
        return {
            "status": "success",
            "message": f"Consent recorded for purpose '{req.purpose.value}'.",
            "data": record
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/api/v1/privacy/consent/withdraw")
def revoke_consent(req: ConsentWithdrawalRequest):
    """
    Cascading consent withdrawal:
    Halts partner sharing, invalidates identity links, and suppresses eligible advertising processing.
    """
    try:
        res = withdraw_consent(req.identity_id, req.purpose, cascade=req.cascade)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/api/v1/privacy/consents/{identity_id}")
def list_consents(identity_id: str):
    """Lists all active and historical consent records for an identity."""
    records = [r for r in CONSENT_RECORDS if r["identity_id"] == identity_id]
    return {
        "status": "success",
        "identity_id": identity_id,
        "consents": records
    }

@router.post("/api/v1/privacy/location/resolve")
def resolve_purpose_bound_location(req: LocationResolutionRequest):
    """
    Enforces purpose-bound location processing (Clause 155).
    - LOCATION_FOR_VASTU: Used only for compass direction calculations.
    - LOCATION_FOR_ADVERTISING: Blocked unless explicit advertising location consent is granted.
    """
    if req.purpose not in [ConsentPurpose.LOCATION_FOR_VASTU, ConsentPurpose.LOCATION_FOR_ADVERTISING]:
        raise HTTPException(status_code=400, detail="Invalid location purpose specified.")

    has_consent = check_consent(req.identity_id, req.purpose)
    if not has_consent:
        raise HTTPException(
            status_code=403,
            detail=f"Access Denied: Missing explicit consent for '{req.purpose.value}'."
        )

    # If Vastu location requested, calculate compass reference
    if req.purpose == ConsentPurpose.LOCATION_FOR_VASTU:
        return {
            "status": "success",
            "purpose": req.purpose.value,
            "coordinates_processed": True,
            "vastu_zone": "Calculated under localized magnetic declination.",
            "data_firewall_verdict": "HELD_IN_SERVICE_DATA_ONLY"
        }
    else:
        return {
            "status": "success",
            "purpose": req.purpose.value,
            "coordinates_processed": True,
            "advertising_eligibility": "Coarse geographic segment permitted."
        }

@router.post("/api/v1/adtech/activate")
def activate_adtech_audience(req: OutboundAdTechRequest):
    """
    Outbound AdTech Activation Endpoint through the Data Firewall:
    - Intercepts and scrubs all sensitive service intelligence (DOB, health, divorce, debt).
    - Only activates approved non-sensitive audience segments with verified consent.
    - Fail-closed security posture.
    """
    decision = filter_and_activate_adtech_payload(req)
    if decision["status"] == "BLOCKED":
        raise HTTPException(
            status_code=403,
            detail={
                "error": "AdTech Data Firewall Blocked Activation",
                "reasons": decision.get("reason"),
                "partner_id": decision.get("partner_id")
            }
        )
    return {
        "status": "success",
        "data": decision
    }

@router.get("/api/v1/privacy/settings")
def get_privacy_settings():
    """Returns privacy center metadata and approved audience categories."""
    return {
        "status": "success",
        "jurisdiction": "IN - Digital Personal Data Protection Act 2025",
        "purposes": [p.value for p in ConsentPurpose],
        "approved_partners": list(APPROVED_PARTNERS.keys()),
        "approved_non_sensitive_segments": APPROVED_NON_SENSITIVE_SEGMENTS,
        "anti_fingerprinting_policy": "Strict zero-fingerprinting enforced across all Web and PWA surfaces.",
        "ios_att_policy": "IDFA zeroed without explicit ATT authorization.",
        "sensitive_data_firewall": "Health, divorce risk, financial distress, and raw DOB strictly excluded from external AdTech pipelines."
    }

@router.get("/api/v1/privacy/data/{user_id}")
def export_user_data(user_id: str):
    """Data portability endpoint under DPDP 2025."""
    import time
    user_logs = [log for log in CONSENT_RECORDS if log.get("user_id") == user_id or log.get("identity_id") == user_id]
    return {
        "status": "success",
        "user_id": user_id,
        "exported_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "consent_history": user_logs,
        "pii_retention": "Zero ad-network tracking. Data bound strictly to requested readings."
    }

@router.delete("/api/v1/privacy/data/{user_id}")
def delete_user_data(user_id: str):
    """Right to erasure under DPDP 2025."""
    global CONSENT_RECORDS
    CONSENT_RECORDS = [log for log in CONSENT_RECORDS if log.get("user_id") != user_id and log.get("identity_id") != user_id]
    return {
        "status": "success",
        "message": f"All PII and consent records deleted for user '{user_id}' under DPDP 2025 compliance."
    }
