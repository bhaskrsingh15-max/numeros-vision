"""
NUMEROS VISION V2 API ROUTER (NV-001 TO NV-026 COMPLETE SUITE)
Benchmark: NumerologySuite Expansion
Exposes deterministic, tested endpoints for all expanded numerology modules.
"""

from fastapi import APIRouter, HTTPException, Query, Body, Request
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import datetime
import hmac
import os

# Engine imports
from app.engine.methodology_registry import METHODOLOGY_REGISTRY, get_methodology
from app.engine.number_characteristics_registry import get_number_profile, NUMBER_REGISTRY
from app.engine.enhanced_lo_shu_engine import (
    build_birth_date_grid,
    build_name_derived_grid,
    compare_name_change_grids
)
from app.engine.name_balancing_engine import (
    calculate_segment_values,
    evaluate_name_rules,
    generate_spelling_candidates,
    generate_candidate_comparison_table
)
from app.engine.profession_engine import recommend_professions
from app.engine.forecast_engine import (
    calculate_blessing_years,
    generate_multi_year_forecast,
    generate_detailed_annual_matrix
)
from app.engine.remedy_rules_engine import select_remedies_and_yantras, YANTRA_CATALOGUE
from app.engine.asset_numerology_engine import (
    analyze_mobile_number,
    analyze_vehicle_number,
    analyze_property_number,
    analyze_bank_account_harmony
)
from app.engine.naming_engine import (
    analyze_business_name,
    recommend_baby_names
)
from app.engine.life_aspects_engine import (
    analyze_relationship_compatibility,
    evaluate_foreign_travel_indicators,
    evaluate_health_and_wellbeing
)
from app.engine.practitioner_engine import (
    register_client_profile,
    add_consultation_session,
    log_prediction,
    record_prediction_outcome,
    get_practitioner_dashboard,
    configure_white_label
)
from app.engine.astrology_correlation_engine import (
    run_multi_astrology_correlation_engine,
    calculate_hourly_planetary_horas,
    correlate_planetary_transits
)

router = APIRouter(prefix="/api/v2/numerology", tags=["NumerologySuite Expansion V2"])


# ── Schemas ───────────────────────────────────────────────────────────────────
class AstrologyCorrelateRequest(BaseModel):
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900, le=2100)
    full_name: str = Field(...)
    target_date: Optional[str] = None

class DailyHoraRequest(BaseModel):
    driver: int = Field(1, ge=1, le=9)
    conductor: int = Field(1, ge=1, le=9)
    target_date: Optional[str] = None

class NameBalanceRequest(BaseModel):
    full_name: str
    driver: Optional[int] = None
    conductor: Optional[int] = None
    dob_str: Optional[str] = None
    custom_candidates: Optional[List[str]] = None

class ProfessionRequest(BaseModel):
    driver: int
    conductor: int
    saturn_override: Optional[int] = None
    kp_sub_lord: Optional[str] = None

class BlessingYearsRequest(BaseModel):
    day: int
    month: int
    year: int
    current_age: Optional[int] = None

class ForecastRequest(BaseModel):
    day: int
    month: int
    year: Optional[int] = None

class RemedyRequest(BaseModel):
    driver: int
    conductor: int
    missing_numbers: Optional[List[int]] = None
    repeated_numbers: Optional[Dict[int, int]] = None
    max_remedies: int = 5

class MobileRequest(BaseModel):
    mobile_number: str
    driver: Optional[int] = None
    conductor: Optional[int] = None

class VehicleRequest(BaseModel):
    registration_plate: str
    driver: int
    conductor: int

class PropertyRequest(BaseModel):
    property_identifier: str
    driver: int
    conductor: int

class BankAccountRequest(BaseModel):
    account_number: str
    driver: int
    conductor: int

class BusinessNameRequest(BaseModel):
    brand_name: str
    owner_driver: int
    owner_conductor: int
    industry_category: str = "technology"
    partner_drivers: Optional[List[int]] = None

class BabyNamingRequest(BaseModel):
    baby_driver: int
    baby_conductor: int
    gender: Optional[str] = None
    starting_letter: Optional[str] = None
    missing_numbers_in_chart: Optional[List[int]] = None

class RelationshipRequest(BaseModel):
    person1_name: str
    p1_day: int
    p1_month: int
    p1_year: int
    person2_name: str
    p2_day: int
    p2_month: int
    p2_year: int
    relationship_type: str = "romantic"

class ForeignTravelRequest(BaseModel):
    day: int
    month: int
    year: int
    target_year: Optional[int] = None

class HealthWellbeingRequest(BaseModel):
    driver: int
    conductor: int
    current_age: Optional[int] = 30


# ── Endpoints ─────────────────────────────────────────────────────────────────

# NV-001: Methodology Registry
@router.get("/methodology-registry")
def list_methodologies():
    """NV-001: Returns the centralized registry of all 8 calculation methodologies."""
    return {"status": "SUCCESS", "methodologies": METHODOLOGY_REGISTRY}


# NV-002: Number Characteristics Registry
@router.get("/number-profile/{number}")
def get_number_characteristics(number: int):
    """NV-002: Retrieves single source of truth profile for numbers 1-9, master 11/22/33, or compound 10-52."""
    profile = get_number_profile(number)
    if not profile:
        raise HTTPException(status_code=404, detail=f"Profile for number {number} not found in registry.")
    return {"status": "SUCCESS", "profile": profile}


# NV-003: Enhanced Lo Shu Analysis
@router.post("/lo-shu/enhanced")
def get_enhanced_lo_shu(day: int, month: int, year: int, name: Optional[str] = None, proposed_name: Optional[str] = None):
    """NV-003: Computes pure birth-date Lo Shu grid, name grid, and before/after comparison."""
    birth_grid = build_birth_date_grid(day, month, year)
    result = {"status": "SUCCESS", "birth_date_grid": birth_grid}
    if name:
        result["name_grid"] = build_name_derived_grid(name)
    if name and proposed_name:
        result["name_change_comparison"] = compare_name_change_grids(day, month, year, name, proposed_name)
    return result


# NV-004: Name Balancing Engine
@router.post("/name/balance")
def analyze_and_balance_name(req: NameBalanceRequest):
    """NV-004: Evaluates name rules, segment breakdown, and generates suggested spellings."""
    driver = req.driver
    conductor = req.conductor
    if (driver is None or conductor is None) and req.dob_str:
        try:
            import re
            nums = [int(n) for n in re.findall(r"\d+", req.dob_str)]
            if len(nums) >= 3:
                if nums[0] > 1900:  # YYYY-MM-DD
                    y, m, d = nums[0], nums[1], nums[2]
                else:  # DD-MM-YYYY
                    d, m, y = nums[0], nums[1], nums[2]

                def reduce_val(val: int) -> int:
                    while val > 9:
                        val = sum(int(digit) for digit in str(val))
                    return val

                if driver is None:
                    driver = reduce_val(d)
                if conductor is None:
                    conductor = reduce_val(sum(int(digit) for digit in f"{d}{m}{y}"))
        except Exception:
            pass

    driver = driver or 1
    conductor = conductor or 1

    evaluation = evaluate_name_rules(req.full_name, driver, conductor, req.dob_str)
    return {
        "status": "SUCCESS",
        "current_name_evaluation": evaluation,
        "is_aligned": evaluation.get("is_aligned", False),
        "calculated_driver": driver,
        "calculated_conductor": conductor
    }


# NV-005: Profession Recommendation Engine
@router.post("/professions/recommend")
def get_profession_recommendations(req: ProfessionRequest):
    """NV-005: Unified career taxonomy mapped across Driver, Conductor, BNN Saturn, and KP."""
    recommendations = recommend_professions(
        driver=req.driver,
        conductor=req.conductor,
        saturn_conjunction_override=req.saturn_override,
        kp_tenth_sub_lord=req.kp_sub_lord
    )
    return {"status": "SUCCESS", "recommendations": recommendations}


# NV-006: Blessing Years Timeline
@router.post("/forecast/blessing-years")
def get_blessing_years(req: BlessingYearsRequest):
    """NV-006: Computes milestone years and timeline from age 18 to 75."""
    blessing_data = calculate_blessing_years(
        day=req.day, month=req.month, birth_year=req.year, current_age=req.current_age
    )
    return {"status": "SUCCESS", "blessing_years": blessing_data}


# NV-007: Personal Cycle Forecasts
@router.post("/forecast/personal-cycles")
def get_personal_cycle_forecasts(req: ForecastRequest):
    """NV-007: Multi-year horizon forecast (4 years) & 12-month annual matrix."""
    multi_year = generate_multi_year_forecast(req.day, req.month, req.year)
    monthly_matrix = generate_detailed_annual_matrix(req.day, req.month, req.year)
    return {
        "status": "SUCCESS",
        "multi_year_horizon": multi_year,
        "annual_monthly_matrix": monthly_matrix
    }


# NV-008 & NV-009: Explainable Remedy Rules & Yantra Selector
@router.post("/remedies/select")
def select_remedies(req: RemedyRequest):
    """NV-008 & NV-009: Curates <= 5 non-conflicting remedies and pairs a sacred Yantra."""
    result = select_remedies_and_yantras(
        driver=req.driver,
        conductor=req.conductor,
        missing_numbers=req.missing_numbers,
        repeated_numbers=req.repeated_numbers,
        max_remedies=req.max_remedies
    )
    return {"status": "SUCCESS", "remedy_prescription": result}


# NV-010: Mobile Number Analysis
@router.post("/assets/mobile")
def audit_mobile(req: MobileRequest):
    """NV-010: Audits mobile phone number for malefic pairs and total vibration."""
    result = analyze_mobile_number(req.mobile_number, req.driver, req.conductor)
    return {"status": "SUCCESS", "mobile_audit": result}


# NV-011: Vehicle Registration Number Analysis
@router.post("/assets/vehicle")
def audit_vehicle(req: VehicleRequest):
    """NV-011: Analyzes license plate letters, digits, owner compatibility and remedies."""
    result = analyze_vehicle_number(req.registration_plate, req.driver, req.conductor)
    return {"status": "SUCCESS", "vehicle_audit": result}


# NV-012: Property Number Analysis
@router.post("/assets/property")
def audit_property(req: PropertyRequest):
    """NV-012: Analyzes unit/house number, Vastu element, and resident harmony."""
    result = analyze_property_number(req.property_identifier, req.driver, req.conductor)
    return {"status": "SUCCESS", "property_audit": result}


# NV-013: Bank Account Number Harmony (Strict Privacy)
@router.post("/assets/bank-account")
def audit_bank_account(req: BankAccountRequest):
    """NV-013: Analyzes wealth vibration with strict privacy (in-memory, masked output)."""
    result = analyze_bank_account_harmony(req.account_number, req.driver, req.conductor)
    return {"status": "SUCCESS", "bank_account_harmony": result}


# NV-014: Business Name Analysis
@router.post("/naming/business")
def audit_business_name(req: BusinessNameRequest):
    """NV-014: Evaluates brand name against owner, partners, and industry classification."""
    result = analyze_business_name(
        brand_name=req.brand_name,
        owner_driver=req.owner_driver,
        owner_conductor=req.owner_conductor,
        industry_category=req.industry_category,
        partner_drivers=req.partner_drivers
    )
    return {"status": "SUCCESS", "business_name_audit": result}


# NV-015: Baby Naming Workflow
@router.post("/naming/baby")
def get_baby_name_recommendations(req: BabyNamingRequest):
    """NV-015: Filters curated baby names by auspiciousness and Lo Shu missing energy fill."""
    result = recommend_baby_names(
        baby_driver=req.baby_driver,
        baby_conductor=req.baby_conductor,
        gender=req.gender,
        starting_letter=req.starting_letter,
        missing_numbers_in_chart=req.missing_numbers_in_chart
    )
    return {"status": "SUCCESS", "baby_name_recommendations": result}


# NV-016: Relationship Synastry
@router.post("/relationships/synastry")
def analyze_synastry(req: RelationshipRequest):
    """NV-016: Comprehensive dual-profile matchmaking and communication suggestions."""
    result = analyze_relationship_compatibility(
        person1_name=req.person1_name,
        p1_day=req.p1_day,
        p1_month=req.p1_month,
        p1_year=req.p1_year,
        person2_name=req.person2_name,
        p2_day=req.p2_day,
        p2_month=req.p2_month,
        p2_year=req.p2_year,
        relationship_type=req.relationship_type
    )
    return {"status": "SUCCESS", "synastry_report": result}


# NV-017: Foreign Travel & Relocation
@router.post("/travel/foreign")
def get_foreign_travel_indicators(req: ForeignTravelRequest):
    """NV-017: Analyzes travel numbers (2, 5, 6, 7), Action Plane, and settlement prospects."""
    result = evaluate_foreign_travel_indicators(req.day, req.month, req.year, req.target_year)
    return {"status": "SUCCESS", "travel_indicators": result}


# NV-018: Health & Wellbeing (Safe Use)
@router.post("/health/wellbeing")
def get_health_and_wellbeing(req: HealthWellbeingRequest):
    """NV-018: Safe, non-diagnostic vitality interpretation and Ayurvedic lifestyle habits."""
    result = evaluate_health_and_wellbeing(req.driver, req.conductor, req.current_age)
    return {"status": "SUCCESS", "wellbeing_analysis": result}


# NV-019 & NV-025: Practitioner Client & Dashboard
@router.get("/practitioner/{practitioner_id}/dashboard")
def get_dashboard(practitioner_id: str):
    """NV-025: Aggregated analytics, consultation volume, and prediction accuracy metrics."""
    dash = get_practitioner_dashboard(practitioner_id)
    return {"status": "SUCCESS", "dashboard": dash}


@router.post("/practitioner/client")
def create_client(
    practitioner_id: str = Body(...),
    full_name: str = Body(...),
    dob_str: str = Body(...),
    gender: str = Body("Unspecified"),
    email: Optional[str] = Body(None),
    phone: Optional[str] = Body(None),
    initial_notes: str = Body("")
):
    """NV-019 & NV-026: Registers client profile with formal DPDP consent logging."""
    client = register_client_profile(
        practitioner_id=practitioner_id,
        full_name=full_name,
        dob_str=dob_str,
        gender=gender,
        email=email,
        phone=phone,
        initial_notes=initial_notes
    )
    return {"status": "SUCCESS", "client": client}


# NV-024: Prediction Outcome Tracking
@router.post("/practitioner/prediction")
def log_prospective_prediction(
    client_id: str = Body(...),
    practitioner_id: str = Body(...),
    prediction_text: str = Body(...),
    category: str = Body("CAREER"),
    start_date: str = Body(...),
    end_date: str = Body(...),
    confidence: str = Body("HIGH")
):
    """NV-024: Registers prospective prediction prior to outcome occurrence."""
    pred = log_prediction(
        client_id=client_id,
        practitioner_id=practitioner_id,
        prediction_text=prediction_text,
        category=category,
        target_period_start=start_date,
        target_period_end=end_date,
        confidence_level=confidence
    )
    return {"status": "SUCCESS", "prediction": pred}


@router.post("/practitioner/prediction/outcome")
def record_outcome(
    prediction_id: str = Body(...),
    outcome_status: str = Body(...), # "FULFILLED", "PARTIALLY_FULFILLED", "UNFULFILLED"
    practitioner_notes: str = Body(...),
    client_confirmed: bool = Body(True)
):
    """NV-024: Records verified outcome preserving original prediction text immutable."""
    outcome = record_prediction_outcome(
        prediction_id=prediction_id,
        outcome_status=outcome_status,
        practitioner_notes=practitioner_notes,
        client_confirmed=client_confirmed
    )
    if "error" in outcome:
        raise HTTPException(status_code=400, detail=outcome["error"])
    return {"status": "SUCCESS", "outcome": outcome}


# NV-022: White-Label Configuration
@router.post("/practitioner/white-label")
def update_white_label(
    practitioner_id: str = Body(...),
    studio_name: str = Body(...),
    practitioner_name: str = Body(...),
    logo_url: str = Body(...),
    contact_email: str = Body(...),
    contact_phone: str = Body(...),
    custom_footer: str = Body(...),
    enabled: bool = Body(True)
):
    """NV-022: Configures practitioner branding for customized client reports."""
    cfg = configure_white_label(
        practitioner_id=practitioner_id,
        studio_name=studio_name,
        practitioner_name=practitioner_name,
        logo_url=logo_url,
        contact_email=contact_email,
        contact_phone=contact_phone,
        custom_footer=custom_footer,
        enabled=enabled
    )
    return {"status": "SUCCESS", "white_label_config": cfg}


# ── NV-027 / CHARM AI: MULTI-ASTROLOGY CORRELATION & TRANSIT SYNTHESIS ────────
@router.post("/astrology/correlate")
def correlate_astrology_disciplines(req: AstrologyCorrelateRequest):
    """
    Multi-Astrology Correlation Engine:
    Cross-checks 6 canonical disciplines:
    1. Vedic Parashari Jyotish (Sambandha & Yogas)
    2. Krishnamurti Paddhati (KP Sub-Lord 81-Matrix)
    3. Lal Kitab (Masnooi Compound Planets & Awakening Ages)
    4. Lo Shu 3x3 Magic Square (8 Planes & Voids)
    5. Classical Chaldean Acoustic Vibration
    6. Real-Time Planetary Transit (Gochar) & 24-Hour Hora Integration

    Synthesizes a 0-100% consensus score and 7-layer safe remedies.
    """
    parsed_date = None
    if req.target_date:
        try:
            parsed_date = datetime.date.fromisoformat(req.target_date)
        except Exception:
            parsed_date = datetime.date.today()

    res = run_multi_astrology_correlation_engine(
        day=req.day,
        month=req.month,
        year=req.year,
        full_name=req.full_name,
        target_date=parsed_date
    )
    return res


@router.get("/astrology/daily-hora")
def get_daily_planetary_horas(
    driver: int = Query(1, ge=1, le=9),
    conductor: int = Query(1, ge=1, le=9),
    target_date: Optional[str] = Query(None)
):
    """
    Calculates the 24-hour executive Chaldean planetary horas starting from 06:00 AM,
    evaluating personalized suitability against native Driver and Conductor numbers.
    """
    parsed_date = None
    if target_date:
        try:
            parsed_date = datetime.date.fromisoformat(target_date)
        except Exception:
            parsed_date = datetime.date.today()
    else:
        parsed_date = datetime.date.today()

    horas = calculate_hourly_planetary_horas(
        target_date=parsed_date,
        driver=driver,
        conductor=conductor
    )
    return {
        "status": "SUCCESS",
        "target_date": parsed_date.strftime("%Y-%m-%d"),
        "driver": driver,
        "conductor": conductor,
        "total_horas": len(horas),
        "favourable_count": len([h for h in horas if h["suitability_code"] == "favourable"]),
        "horas": horas
    }


@router.post("/astrology/daily-hora")
def post_daily_planetary_horas(req: DailyHoraRequest):
    """POST variant of daily-hora for JSON payload clients."""
    parsed_date = None
    if req.target_date:
        try:
            parsed_date = datetime.date.fromisoformat(req.target_date)
        except Exception:
            parsed_date = datetime.date.today()
    else:
        parsed_date = datetime.date.today()

    horas = calculate_hourly_planetary_horas(
        target_date=parsed_date,
        driver=req.driver,
        conductor=req.conductor
    )
    return {
        "status": "SUCCESS",
        "target_date": parsed_date.strftime("%Y-%m-%d"),
        "driver": req.driver,
        "conductor": req.conductor,
        "total_horas": len(horas),
        "favourable_count": len([h for h in horas if h["suitability_code"] == "favourable"]),
        "horas": horas
    }


class IndicationsPreviewRequest(BaseModel):
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900, le=2100)
    gender: Optional[str] = None
    calling_name: Optional[str] = None
    edition: str = "india"
    remedy_style: Optional[str] = None
    requested_tier: Optional[str] = "free"


@router.post("/indications")
async def post_indications_bundle(req: IndicationsPreviewRequest, request: Request):
    """
    Section 16–19 Server-Side Indications, Remedies, 2027 Care Guide & Affirmation/Manifestation API.
    - Enforces server-side entitlement strictly (`free` unless authenticated user / internal signed service grants higher tier).
    - Never returns blurred/fake paid content; when `requested_tier` > actual `entitlement_tier`,
      returns highest allowed content + plain-text `upgrade_note`.
    """
    from app.engine.indications_engine import (
        compute_full_indications_bundle,
        is_layers_2_3_enabled,
        resolve_package_entitlement,
    )

    if not is_layers_2_3_enabled():
        return {
            "status": "FEATURE_DISABLED",
            "layers_2_3_enabled": False,
            "message": "Extended Indications & Care Guide layer is currently behind feature flag.",
        }

    entitled = "free"
    internal_sec = os.environ.get("PDF_SERVICE_SECRET", "").strip()
    hdr_sec = (request.headers.get("X-NV-Internal-Secret") or "").strip()
    hdr_tier = (request.headers.get("X-NV-Entitlement-Tier") or "").strip().lower()
    if internal_sec and hdr_sec and hmac.compare_digest(hdr_sec, internal_sec) and hdr_tier:
        entitled = hdr_tier
    elif request.headers.get("Authorization") or request.cookies.get("nv_user_session") or request.cookies.get("nv_practitioner_session"):
        try:
            from app.api.auth import api_get_current_user
            u = await api_get_current_user(request)
            if isinstance(u, dict) and u.get("authenticated") and u.get("entitlement_tier"):
                entitled = str(u["entitlement_tier"]).lower()
        except Exception:
            entitled = "free"

    bundle = compute_full_indications_bundle(
        day=req.day,
        month=req.month,
        year=req.year,
        gender=req.gender,
        calling_name=req.calling_name,
        edition=req.edition,
        tier=req.requested_tier or "free",
        entitlement_tier=entitled,
        user_remedy_style=req.remedy_style,
    )
    req_norm = resolve_package_entitlement(req.requested_tier or "free")["canonical_tier"]
    ent_norm = resolve_package_entitlement(entitled)["canonical_tier"]
    tier_rank = {"free": 0, "basic": 1, "charm_free": 0, "charm_paid": 2, "advanced": 3, "premium": 4, "planner_2027": 4, "charm_premium": 4}
    pkg_names = {
        "basic": "Anveil My Alignments (Basic)",
        "advanced": "Anveil My Glowing Charms (Advanced)",
        "premium": "Complete Numerology Report (Premium)",
        "planner_2027": "2027 Personalised Numerology Planner",
        "charm_paid": "Charm AI Starter Pack",
    }
    upgrade_note = None
    if tier_rank.get(req_norm, 0) > tier_rank.get(ent_norm, 0):
        upgrade_note = f"A personalised version is included in {pkg_names.get(req_norm, 'Anveil My Glowing Charms (Advanced)')}."

    return {
        "status": "SUCCESS",
        "layers_2_3_enabled": True,
        "entitlement_tier": ent_norm,
        "requested_tier": req_norm,
        "upgrade_note": upgrade_note,
        "bundle": bundle,
    }

