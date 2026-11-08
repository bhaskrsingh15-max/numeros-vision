"""
app/api/charm_ai.py
===================
Production-Grade API Router for Charm AI.
Complies with Section 7 and 9 of Master Specification & Rectification Instructions.
"""

from fastapi import APIRouter, HTTPException, Request, Depends
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import os
import hmac

from app.charm.chat.response_composer import charm_chat_orchestrator, CharmChatResponse
from app.charm.outcomes.outcome_service import outcome_service
from app.api.auth import api_get_current_user

router = APIRouter(prefix="/api/charm", tags=["Charm AI Core"])

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
    """Helper to extract active user session or default to guest."""
    try:
        user_info = await api_get_current_user(request)
        if isinstance(user_info, dict) and user_info.get("authenticated"):
            return user_info
    except Exception:
        pass
    return {"authenticated": False, "user_id": "guest_user"}

class CharmChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: Optional[str] = Field(default="", description="User question or inquiry")
    question: Optional[str] = Field(default=None, description="Alternative key for message")
    user_intent: Optional[str] = Field(default=None, description="e.g. new_job_or_senior_role, promotion")
    forecast_horizon: Optional[str] = Field(default=None, description="e.g. 6_months, 12_months")
    name: Optional[str] = "Seeker"
    dob: Optional[str] = None  # Format: YYYY-MM-DD
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
    approved_ruleset_version: Optional[str] = "2.0.0"
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

@router.post("/chat", response_model=CharmChatResponse)
async def charm_chat_endpoint(req: CharmChatRequest, request: Request, current_user=Depends(get_current_user_optional), _auth=Depends(verify_charm_service_auth)):
    """
    Main conversational turn for Charm AI.
    Calculates Numerology Dasha first, executes independent cross-verification,
    and returns deterministic consensus and governed remedies.
    """
    user_id = current_user.get("user_id", "guest_user") if current_user else "guest_user"
    
    # Handle DOB parsing if passed as YYYY-MM-DD
    d = req.day
    m = req.month
    y = req.year
    if req.dob and not (d and m and y):
        parts = req.dob.split("-")
        if len(parts) == 3:
            try:
                y = int(parts[0])
                m = int(parts[1])
                d = int(parts[2])
            except ValueError:
                pass
    
    msg = req.message or req.question or "Is 2026 favorable for my career?"
    
    response = charm_chat_orchestrator.process_chat_turn(
        message=msg,
        user_name=req.name or "Seeker",
        day=d,
        month=m,
        year=y,
        conversation_id=req.conversation_id,
        user_id=user_id,
        tob=req.tob,
        pob=req.pob or req.city,
        loshu_grid=req.loshu_grid
    )
    return response

@router.get("/predictions/{prediction_id}/evidence")
async def get_prediction_evidence(prediction_id: str, current_user=Depends(get_current_user_optional)):
    """
    Returns full audit trace, method evaluations, and exact source locators for a prediction.
    """
    snapshot = outcome_service.get_snapshot(prediction_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Prediction snapshot not found.")
    return snapshot

@router.post("/outcomes")
async def record_prediction_outcome(req: OutcomeSubmissionRequest, current_user=Depends(get_current_user_optional)):
    """
    Records voluntary user event outcome for cohort verification.
    Invariant: Does not mutate original prediction snapshot.
    """
    user_id = current_user.get("user_id", "guest_user") if current_user else "guest_user"
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
    """
    Handles follow-up clarifications on an existing prediction.
    """
    snapshot = outcome_service.get_snapshot(req.prediction_id)
    if not snapshot:
        raise HTTPException(status_code=404, detail="Original prediction snapshot not found.")
    
    response = charm_chat_orchestrator.process_chat_turn(
        message=req.message,
        day=snapshot.driver, # fallback
        month=1,
        year=2026 - snapshot.personal_year,
        conversation_id=f"CONV-{req.prediction_id}"
    )
    return response
