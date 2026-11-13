"""
Numeros Vision — Business Direction Intelligence & Existing Business Alignment API Router
Implements Sections 1.A and 1.B of the Master Build Specification:
- /api/v1/business/startup-evaluate
- /api/v1/business/existing-diagnose
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Literal

from app.engine.monetization_alignment_engine import get_tool_monetization_payload
from app.engine.business_direction_engine import (
    BusinessDirectionEngine,
    FounderProfile,
    CandidateBusinessOption,
)

router = APIRouter(prefix="/api/v1/business", tags=["Business Direction & Alignment"])
engine = BusinessDirectionEngine()


class StartupEvaluateRequest(BaseModel):
    founder_name: str
    skills: List[str]
    experience_years: int
    capital_band: Literal["bootstrapped", "seed_10k_50k", "growth_50k_250k", "institutional_250k_plus"]
    location: str
    risk_tolerance: Literal["low", "moderate", "aggressive"]
    operating_preference: Literal["hands_on_operations", "digital_remote", "hybrid_management"]
    founder_dob: Optional[str] = None
    idea_name: str
    activity_description: str
    revenue_model: str
    customer_segment: str
    delivery_channel: str
    estimated_startup_capital_required: Literal["bootstrapped", "seed_10k_50k", "growth_50k_250k", "institutional_250k_plus"] = "seed_10k_50k"


class ExistingDiagnoseRequest(BaseModel):
    legal_name: str
    trading_name: str
    products_services: str
    current_constraints: List[str] = Field(default_factory=list)
    performance_challenges: List[str] = Field(default_factory=list)
    logo_color_preference: Optional[str] = "#C9A227"


@router.post("/startup-evaluate")
async def evaluate_startup(req: StartupEvaluateRequest):
    """
    Section 1.A: Evaluates a candidate startup business idea.
    Keeps practical business viability strictly separate from traditional numerology/astrology.
    """
    founder = FounderProfile(
        name=req.founder_name,
        skills=req.skills,
        experience_years=req.experience_years,
        capital_band=req.capital_band,
        location=req.location,
        risk_tolerance=req.risk_tolerance,
        operating_preference=req.operating_preference,
        dob=req.founder_dob,
    )
    option = CandidateBusinessOption(
        idea_id=f"opt_{req.idea_name.lower().replace(' ', '_')}",
        name=req.idea_name,
        activity_description=req.activity_description,
        revenue_model=req.revenue_model,
        customer_segment=req.customer_segment,
        delivery_channel=req.delivery_channel,
        estimated_startup_capital_required=req.estimated_startup_capital_required,
    )

    result = engine.evaluate_startup_option(founder, option)

    return {
        "idea_id": result.idea_id,
        "business_name": result.business_name,
        "commercial_viability": {
            "skill_match": result.commercial_viability.skill_match,
            "capital_sufficient": result.commercial_viability.capital_sufficient,
            "operational_complexity": result.commercial_viability.operational_complexity,
            "regulatory_feasibility": result.commercial_viability.regulatory_feasibility,
            "findings": result.commercial_viability.findings,
        },
        "traditional_alignment": {
            "framework": result.traditional_alignment.framework,
            "alignment_status": result.traditional_alignment.alignment_status,
            "candidate_archetypes": result.traditional_alignment.candidate_archetypes,
            "name_compound": result.traditional_alignment.name_compound,
            "name_single": result.traditional_alignment.name_single,
            "reasons": result.traditional_alignment.reasons,
            "conflicts": result.traditional_alignment.conflicts,
            "unknowns": result.traditional_alignment.unknowns,
            "letter_breakdown": getattr(result.traditional_alignment, "letter_breakdown", []),
            "compound_profile": getattr(result.traditional_alignment, "compound_profile", {}),
            "founder_synergy": getattr(result.traditional_alignment, "founder_synergy", {}),
            "balanced_spelling_recommendations": getattr(result.traditional_alignment, "balanced_spelling_recommendations", []),
            "vastu_and_operational_remedies": getattr(result.traditional_alignment, "vastu_and_operational_remedies", {}),
        },
        "synthesis_recommendation": result.synthesis_recommendation,
        "next_steps": result.next_steps,
        "mandatory_disclaimer": result.mandatory_disclaimer,
        "monetization_gate": get_tool_monetization_payload(
            tool_key="business_alignment",
            entity_name=result.business_name,
            compound=result.traditional_alignment.name_compound,
            root=result.traditional_alignment.name_single,
            status=result.traditional_alignment.alignment_status,
        ),
    }


@router.post("/existing-diagnose")
async def diagnose_existing(req: ExistingDiagnoseRequest):
    """
    Section 1.B: Diagnostic for operating businesses.
    Separates fixed constraints from changeable factors, prioritizes practical improvements first,
    and provides optional traditional remedies with cost/risk disclosure.
    """
    diag = engine.diagnose_existing_business(
        legal_name=req.legal_name,
        trading_name=req.trading_name,
        products_services=req.products_services,
        current_constraints=req.current_constraints,
        performance_challenges=req.performance_challenges,
        logo_color_preference=req.logo_color_preference or "#C9A227",
    )
    diag["monetization_gate"] = get_tool_monetization_payload(
        tool_key="business_alignment",
        entity_name=req.trading_name or req.legal_name,
        compound=diag.get("trading_name_compound", 55),
        root=diag.get("trading_name_root", 1),
        status=diag.get("diagnosis_verdict", "ALIGNED"),
    )
    return diag


@router.get("/startup-evaluate")
@router.get("/existing-diagnose")
@router.get("/")
@router.get("")
async def get_business_tool_redirect(request: Request):
    """
    Gracefully handles GET requests by redirecting browser users directly to the
    interactive Business Alignment & Direction tool interface.
    """
    accept = request.headers.get("accept", "")
    if "text/html" in accept or "*/*" in accept or not accept:
        return RedirectResponse(url="/tools/business-alignment", status_code=303)
    return JSONResponse({
        "status": "info",
        "message": "Business Alignment API is active. Use POST with a JSON payload or visit the web interface at /tools/business-alignment",
        "web_url": "/tools/business-alignment",
        "supported_methods": ["POST"]
    })
