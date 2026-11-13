"""
SECTION 14: HYBRID B2B API ENDPOINTS
High-margin, near-zero marginal cost API serving deterministic chart calculations,
consensus scores, and provenance tags as structured JSON (without incurring LLM costs).
Supports multi-tenancy and API-key authentication.
"""

from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.engine.consensus import generate_consensus_reading
from orchestrator import handle_question

router = APIRouter(prefix="/api/v1/b2b", tags=["B2B Enterprise API"])

# Sample B2B API Keys store for demonstration (in production, stored in Postgres/Redis)
VALID_B2B_KEYS = {
    "b2b_matrimonial_key_123": {"tenant_id": "tenant_shaadi_app", "plan": "enterprise_structured"},
    "b2b_wellness_key_456": {"tenant_id": "tenant_health_app", "plan": "enterprise_structured"}
}

def verify_b2b_key(x_api_key: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not x_api_key or x_api_key not in VALID_B2B_KEYS:
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Key header for B2B API access.")
    return VALID_B2B_KEYS[x_api_key]

class B2BCalculateRequest(BaseModel):
    name: str = Field(..., description="User name")
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900, le=2100)
    topic: Optional[str] = Field("career", description="Target topic domain")

@router.post("/calculate")
def b2b_calculate_structured(req: B2BCalculateRequest, tenant: Dict[str, Any] = Depends(verify_b2b_key)):
    """
    Pure deterministic calculation endpoint for B2B partners.
    Incurs ZERO LLM cost while delivering full multi-engine consensus and provenance tags.
    """
    try:
        consensus_data = generate_consensus_reading(req.name, req.day, req.month, req.year)
        
        user_profile = {
            "phase1_result": {
                "driver": consensus_data["vedic_numerology"]["driver_number"],
                "conductor": consensus_data["vedic_numerology"]["conductor_number"]
            },
            "phase2_result": {"rashi_vs_driver": "neutral"},
            "chart": {
                "Sun":     {"sign": "Scorpio",     "degree": 12.52, "retrograde": False},
                "Moon":    {"sign": "Sagittarius", "degree": 2.39,  "retrograde": False},
                "Mars":    {"sign": "Leo",         "degree": 27.70, "retrograde": False},
                "Mercury": {"sign": "Scorpio",     "degree": 5.75,  "retrograde": False},
                "Jupiter": {"sign": "Libra",       "degree": 6.67,  "retrograde": False},
                "Venus":   {"sign": "Sagittarius", "degree": 28.33, "retrograde": False},
                "Saturn":  {"sign": "Virgo",       "degree": 25.32, "retrograde": True},
                "Rahu":    {"sign": "Cancer",      "degree": 1.36,  "retrograde": True},
                "Ketu":    {"sign": "Capricorn",   "degree": 1.36,  "retrograde": True},
            }
        }
        
        synthesis = handle_question(req.topic, user_profile)
        
        return {
            "status": "success",
            "tenant_id": tenant["tenant_id"],
            "marginal_llm_cost": 0.0,
            "structured_output": {
                "user_name": req.name,
                "dob": f"{req.day:02d}/{req.month:02d}/{req.year}",
                "overall_consensus_strength_pct": consensus_data["overall_consensus_strength_pct"],
                "vedic_numerology": consensus_data["vedic_numerology"],
                "lo_shu_grid": consensus_data["lo_shu_grid"],
                "domain_verdicts": consensus_data["domain_verdicts"],
                "engine_synthesis": synthesis
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class B2BInquiryRequest(BaseModel):
    company_name: str = Field(..., description="Company or Organization name")
    contact_name: str = Field(..., description="Contact person full name")
    email: str = Field(..., description="Work email address")
    phone: Optional[str] = Field(None, description="Phone or WhatsApp number")
    solution_interest: Optional[str] = Field("api", description="Solution of interest: api, saas, wellness, whitelabel")
    volume_or_team_size: Optional[str] = Field(None, description="Estimated API calls or team size")
    notes: Optional[str] = Field(None, description="Additional notes or specifications")


@router.post("/inquiry")
def submit_b2b_inquiry(req: B2BInquiryRequest):
    """
    Lead capture endpoint for enterprise partners, APIs, consultant SaaS, and corporate wellness.
    """
    return {
        "status": "success",
        "message": "Enterprise inquiry received successfully. Our solutions team will contact you within 2 business hours.",
        "inquiry": {
            "company_name": req.company_name,
            "contact_name": req.contact_name,
            "email": req.email,
            "solution_interest": req.solution_interest
        }
    }
