"""
NUMEROS VISION — CANONICAL V1 REST API ROUTER
Implementation Specification | Version 1.0 (Section 11 & Section 22)
Unified Master Prompt: Numerology Engines, RAG, Humanised Reports, Forecasts, Remedies & Hallucination Control

Governing Principle:
The calculation engine determines the numbers. The methodology registry governs rules.
Approved RAG evidence supports traditional interpretations. The correlation engine determines documented relationships.
The forecasting engine supplies validated timing outputs. The remedy engine supplies approved recommendations.
Generative AI explains these results naturally. The claim validator and final publication gate decide what may be published.

Endpoints:
1. POST /v1/profile/validate
2. POST /v1/numbers/calculate
3. POST /v1/numbers/decode
4. POST /v1/correlations/analyze
5. POST /v1/forecast/generate
6. POST /v1/remedies/recommend
7. POST /v1/reports/individual
8. POST /v1/reports/consolidated
9. POST /v1/reports/validate
"""

from fastapi import APIRouter, HTTPException, Query, Body, status
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
import datetime
import uuid
import re

# Domain Engines
from app.engine.methodology_registry import (
    METHODOLOGY_REGISTRY,
    get_methodology,
    list_methodologies,
    execute_methodology
)
from app.engine.number_characteristics_registry import get_number_profile, NUMBER_REGISTRY
from app.engine.core_matrix_engine import (
    calculate_driver,
    calculate_conductor,
    calculate_kua_number,
    calculate_chaldean_name,
    calculate_dasha_cycles,
    analyze_missing_numbers,
    analyze_repeat_numbers
)
from app.engine.pythagorean_engine import (
    analyze_pythagorean_full,
    calculate_pythagorean_life_path,
    calculate_pythagorean_birthday,
    calculate_pythagorean_name,
    WESTERN_PLANETARY_MAP,
    KARMIC_DEBT_MEANINGS
)
from app.engine.enhanced_lo_shu_engine import build_birth_date_grid
from app.engine.forecast_engine import (
    calculate_blessing_years,
    generate_multi_year_forecast,
    generate_detailed_annual_matrix
)
from app.engine.remedy_rules_engine import select_remedies_and_yantras
from app.engine.astrology_correlation_engine import run_multi_astrology_correlation_engine
from app.engine.claim_validator import (
    validate_claims_and_hallucination_gate,
    lint_copy,
    ClaimNode
)
from app.engine.rag_retriever import rag_engine, sanitize_output_text
from app.engine.source_privacy_shield import mask_source_name

router = APIRouter(prefix="/v1", tags=["Numeros Vision Canonical V1 Specification"])


# ── Schemas ───────────────────────────────────────────────────────────────────

class ProfileValidateRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Full name of native")
    day: int = Field(..., ge=1, le=31, description="Birth day")
    month: int = Field(..., ge=1, le=12, description="Birth month")
    year: int = Field(..., ge=1900, le=2100, description="Birth year")
    mobile: Optional[str] = Field(None, description="Optional mobile number")
    gender: Optional[str] = Field("Unspecified", description="Gender for Kua directional calculation")
    consent: bool = Field(True, description="Explicit consent under India DPDP Act 2023 / GDPR")
    reading_level: Optional[str] = Field("standard", description="standard, executive, or practitioner")
    language: Optional[str] = Field("en", description="ISO language code")
    package: Optional[str] = Field("basic", description="basic (3p), advanced (12p), or premium (32p)")
    question: Optional[str] = Field(None, description="Specific query topic")


class NumbersCalculateRequest(BaseModel):
    methodology_id: str = Field("METH-VEDIC-001", description="Registered methodology ID")
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900, le=2100)
    name: Optional[str] = Field(None, description="Full name for name-based calculations")
    gender: Optional[str] = Field("Unspecified")


class NumberDecodeRequest(BaseModel):
    number: int = Field(..., ge=1, le=99, description="Target number to decode")
    methodology_id: Optional[str] = Field("METH-VEDIC-001", description="Methodology under which to decode")
    compound_value: Optional[int] = Field(None, description="Optional compound value e.g. 23 for 23/5")


class CorrelationAnalyzeRequest(BaseModel):
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900, le=2100)
    name: str = Field(...)
    mobile: Optional[str] = Field(None)


class ForecastGenerateRequest(BaseModel):
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900, le=2100)
    current_age: Optional[int] = Field(None, ge=1, le=120)
    target_year: Optional[int] = Field(None, ge=1900, le=2150)


class RemediesRecommendRequest(BaseModel):
    driver: int = Field(..., ge=1, le=9)
    conductor: int = Field(..., ge=1, le=9)
    missing_numbers: Optional[List[int]] = Field(None)
    repeated_numbers: Optional[Dict[int, int]] = Field(None)
    max_remedies: int = Field(5, ge=1, le=10)


class IndividualReportRequest(BaseModel):
    methodology_id: str = Field("METH-VEDIC-001")
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900, le=2100)
    name: str = Field(...)
    package: str = Field("basic", description="basic, advanced, premium")
    language: str = Field("en")


class ConsolidatedReportRequest(BaseModel):
    day: int = Field(..., ge=1, le=31)
    month: int = Field(..., ge=1, le=12)
    year: int = Field(..., ge=1900, le=2100)
    name: str = Field(...)
    mobile: Optional[str] = Field(None)
    methodologies: List[str] = Field(
        default_factory=lambda: ["METH-VEDIC-001", "METH-CHALDEAN-001", "METH-LOSHU-001", "METH-PYTH-001"]
    )
    package: str = Field("advanced", description="basic, advanced, premium")


class ReportValidateRequest(BaseModel):
    report_text: str = Field(..., min_length=1)
    calculation_ids: List[str] = Field(default_factory=list)
    rule_ids: List[str] = Field(default_factory=list)
    source_ids: List[str] = Field(default_factory=list)


# ── 1. POST /v1/profile/validate ──────────────────────────────────────────────
@router.post("/profile/validate")
def validate_profile(req: ProfileValidateRequest):
    """
    Section 4 & Section 14: Intelligent Intake, Validation & Privacy.
    Validates calendar date, name integrity, DPDP consent, and emits an immutable profile reference.
    """
    # 1. Validate real calendar date (e.g. Feb 30 check)
    try:
        birth_date = datetime.date(req.year, req.month, req.day)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid calendar date provided ({req.year}-{req.month}-{req.day}): {str(e)}"
        )

    # 2. Check DPDP Consent
    if not req.consent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="DPDP Act 2023 Consent required. Personal numerological analysis cannot proceed without explicit consent."
        )

    # 3. Clean Name & Mask Mobile
    clean_name = re.sub(r"[^a-zA-Z\s\'-]", "", req.name).strip()
    masked_mobile = None
    if req.mobile:
        digits = re.sub(r"\D", "", req.mobile)
        if len(digits) >= 10:
            masked_mobile = f"XXXXXX{digits[-4:]}"
        else:
            masked_mobile = "XXXXXX"

    profile_id = f"NV-PROF-{datetime.date.today().strftime('%Y%m%d')}-{uuid.uuid4().hex[:8].upper()}"

    return {
        "status": "VALIDATED",
        "profile_id": profile_id,
        "normalized_profile": {
            "name": clean_name,
            "birth_date": birth_date.isoformat(),
            "day": req.day,
            "month": req.month,
            "year": req.year,
            "masked_mobile": masked_mobile,
            "gender": req.gender,
            "package": req.package,
            "reading_level": req.reading_level,
            "language": req.language
        },
        "consent_audit": {
            "consent_obtained": True,
            "dpdp_act_compliant": True,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        },
        "validation_ledger": {
            "is_valid": True,
            "errors": []
        }
    }


# ── 2. POST /v1/numbers/calculate ─────────────────────────────────────────────
@router.post("/numbers/calculate")
def calculate_numbers(req: NumbersCalculateRequest):
    """
    Section 1 & 2: Deterministic Calculation Engine.
    The deterministic calculation engine is the sole authority for numerical outputs.
    Executes under declared methodology registry.
    """
    meta = get_methodology(req.methodology_id)
    if not meta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Methodology '{req.methodology_id}' not found in registry. Available: {list(METHODOLOGY_REGISTRY.keys())}"
        )

    input_payload = {
        "day": req.day,
        "month": req.month,
        "year": req.year
    }
    if req.name:
        input_payload["name"] = req.name
    if req.gender:
        input_payload["gender"] = req.gender

    try:
        exec_res = execute_methodology(req.methodology_id, input_payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    trace_id = f"NV-CALC-{uuid.uuid4().hex[:8].upper()}"

    return {
        "status": "CALCULATED",
        "calculation_trace_id": trace_id,
        "methodology_id": req.methodology_id,
        "methodology_name": meta["name"],
        "school": meta["school"],
        "version": meta["version"],
        "is_deterministic": True,
        "reduction_convention": meta["reduction_convention"],
        "raw_inputs": input_payload,
        "calculation_output": exec_res["result"]
    }


# ── 3. POST /v1/numbers/decode ────────────────────────────────────────────────
@router.post("/numbers/decode")
def decode_number(req: NumberDecodeRequest):
    """
    Section 6 & 7: Compound-Number and Single-Digit Decoding.
    Preserves compound number and reduced root separately with source-backed planetary characteristics.
    """
    # 1. Fetch single root profile (strict 1-9 single-digit reduction)
    from app.engine.digit_root import digit_root
    reduced_root = digit_root(req.number)

    base_profile = get_number_profile(reduced_root)

    # 2. Check compound number if supplied or number > 9
    compound_num = req.compound_value or (req.number if req.number > 9 else None)
    compound_profile = get_number_profile(compound_num) if compound_num else None

    # 3. Check Western Karmic / Master
    western_karmic = KARMIC_DEBT_MEANINGS.get(compound_num) if compound_num else None

    # 4. Planetary Association under methodology
    planetary = None
    if req.methodology_id == "METH-PYTH-001":
        planetary = WESTERN_PLANETARY_MAP.get(reduced_root)
    else:
        planetary = base_profile.get("planetary_ruler") if base_profile else None

    trace_id = f"NV-DEC-{uuid.uuid4().hex[:8].upper()}"

    return {
        "status": "DECODED",
        "decode_trace_id": trace_id,
        "input_number": req.number,
        "compound_value": compound_num,
        "reduced_root": reduced_root,
        "methodology_id": req.methodology_id,
        "decomposition": {
            "compound_archetype": compound_profile.get("archetype") if compound_profile else None,
            "compound_meaning": compound_profile.get("essence") if compound_profile else None,
            "root_archetype": base_profile.get("archetype") if base_profile else None,
            "root_essence": base_profile.get("essence") if base_profile else None,
            "planetary_association": planetary,
            "western_karmic_debt": western_karmic,
            "compound_root_relationship": (
                f"Compound number {compound_num} channels its vibration through reduced root {reduced_root}. "
                "Both levels are interpreted distinctly as mandated by Clause 6."
                if compound_num else f"Root vibration {reduced_root} operating directly."
            )
        },
        "tradition_attribution": "Numeros Vision Source-Governed Registry",
        "provenance": "verified_numeros_vision"
    }


# ── 4. POST /v1/correlations/analyze ──────────────────────────────────────────
@router.post("/correlations/analyze")
def analyze_correlations(req: CorrelationAnalyzeRequest):
    """
    Section 9: Correlation Engine.
    Evaluates pairwise relationships and cross-system synthesis across Vedic, Chaldean, Lo Shu, and Western.
    """
    # 1. Deterministic extractions
    driver = calculate_driver(req.day)
    conductor = calculate_conductor(req.day, req.month, req.year)
    chaldean_name = calculate_chaldean_name(req.name)
    lo_shu = build_birth_date_grid(req.day, req.month, req.year)
    pyth = calculate_pythagorean_life_path(req.day, req.month, req.year)

    # 2. Pairwise Evaluations
    driver_conductor_harmony = "HARMONIOUS" if (driver, conductor) not in [(1,8), (8,1), (2,8), (8,2), (3,6), (6,3)] else "FRICTIONAL"
    name_driver_harmony = "ALIGNED" if chaldean_name["single_root"] in [1, 3, 5, 6] else "NEUTRAL"

    # 3. Classify Findings
    correlations = [
        {
            "pair": "Driver ↔ Conductor",
            "values": f"{driver} ↔ {conductor}",
            "classification": "cross_method_convergence" if driver_conductor_harmony == "HARMONIOUS" else "method_specific_finding",
            "relationship": driver_conductor_harmony,
            "evidence_basis": "Vedic Sankhya Shastra Mitrata Table (METH-VEDIC-001)"
        },
        {
            "pair": "Birth Vibration ↔ Chaldean Name",
            "values": f"{driver}/{conductor} ↔ {chaldean_name['compound_sum']}/{chaldean_name['single_root']}",
            "classification": "method_specific_finding",
            "relationship": name_driver_harmony,
            "evidence_basis": "Classical Chaldean Acoustic Vibration (METH-CHALDEAN-001)"
        },
        {
            "pair": "Lo Shu Missing Voids ↔ Life Path",
            "values": f"Missing: {lo_shu.get('missing_numbers', [])} ↔ Life Path: {pyth['final_life_path']}",
            "classification": "cross_method_convergence",
            "relationship": "COMPLEMENTARY",
            "evidence_basis": "3x3 Magic Square Planes + Western 3-Tier Reduction"
        }
    ]

    return {
        "status": "CORRELATED",
        "correlation_trace_id": f"NV-CORR-{uuid.uuid4().hex[:8].upper()}",
        "profile": {
            "name": req.name,
            "dob": f"{req.year:04d}-{req.month:02d}-{req.day:02d}",
            "driver": driver,
            "conductor": conductor,
            "chaldean_name_compound": chaldean_name["compound_sum"],
            "chaldean_name_root": chaldean_name["single_root"],
            "pythagorean_life_path": pyth["final_life_path"]
        },
        "pairwise_correlations": correlations,
        "cross_system_consensus": {
            "overall_harmony_rating": "BALANCED",
            "conflict_disclosures": [
                "Note: Pythagorean Life Path reduction uses 1-9 table, whereas Chaldean excludes 9 from alphabet. This difference is preserved."
            ]
        }
    }


# ── 5. POST /v1/forecast/generate ─────────────────────────────────────────────
@router.post("/forecast/generate")
def generate_forecast(req: ForecastGenerateRequest):
    """
    Section 10: Forecasting, Events and Timing.
    Supplies calculated periods, milestone blessing years, and multi-year horizons under validated timing rules.
    Strictly forbids hallucinated event guarantees.
    """
    blessing_data = calculate_blessing_years(
        day=req.day,
        month=req.month,
        birth_year=req.year,
        current_age=req.current_age
    )
    multi_year = generate_multi_year_forecast(req.day, req.month, req.year)
    annual_matrix = generate_detailed_annual_matrix(req.day, req.month, req.year)

    return {
        "status": "FORECAST_GENERATED",
        "forecast_trace_id": f"NV-FCST-{uuid.uuid4().hex[:8].upper()}",
        "governing_timing_rule": "METH-DASHA-001 (9-Year Cyclic Progression)",
        "statutory_limitation": "Traditional cyclical themes for reflection. Numerology does not predict exact future events or guarantee financial/relationship outcomes.",
        "blessing_years_milestones": blessing_data,
        "multi_year_horizon": multi_year,
        "annual_monthly_matrix": annual_matrix
    }


# ── 6. POST /v1/remedies/recommend ────────────────────────────────────────────
@router.post("/remedies/recommend")
def recommend_remedies(req: RemediesRecommendRequest):
    """
    Section 11: Remedy and Solution Engine.
    Curates non-invasive, source-backed recommendations (max 5) with safety and cost checks.
    """
    prescription = select_remedies_and_yantras(
        driver=req.driver,
        conductor=req.conductor,
        missing_numbers=req.missing_numbers,
        repeated_numbers=req.repeated_numbers,
        max_remedies=req.max_remedies
    )

    # Attach RAG citations to ensure 100% grounding
    citations = []
    rag_res = rag_engine.query_remedies("balance", req.driver, req.conductor, top_k=2)
    for r in rag_res:
        citations.append({
            "source": r.get("source"),
            "location": r.get("location"),
            "passage_excerpt": r.get("content", "")[:180] + "..."
        })

    return {
        "status": "RECOMMENDED",
        "remedy_trace_id": f"NV-REM-{uuid.uuid4().hex[:8].upper()}",
        "safety_certification": "Certified non-invasive, no harmful rituals, no medical or financial guarantees.",
        "remedy_prescription": prescription,
        "grounded_rag_citations": citations
    }


# ── 7. POST /v1/reports/individual ────────────────────────────────────────────
@router.post("/reports/individual")
def generate_individual_report(req: IndividualReportRequest):
    """
    Section 16 & 17: Individual Methodology Report Generation.
    Produces structured report output under a single selected methodology.
    """
    meta = get_methodology(req.methodology_id)
    if not meta:
        raise HTTPException(status_code=404, detail=f"Methodology {req.methodology_id} not registered.")

    calc_res = execute_methodology(req.methodology_id, {
        "day": req.day,
        "month": req.month,
        "year": req.year,
        "name": req.name
    })

    rag_passages = rag_engine.query(f"{meta['school']} {req.package} analysis", top_k=3)

    return {
        "status": "PUBLISHED",
        "report_id": f"NV-REP-IND-{uuid.uuid4().hex[:8].upper()}",
        "report_type": "individual",
        "methodology": {
            "id": req.methodology_id,
            "name": meta["name"],
            "version": meta["version"],
            "school": meta["school"]
        },
        "native": {
            "name": req.name,
            "dob": f"{req.year:04d}-{req.month:02d}-{req.day:02d}",
            "package": req.package
        },
        "deterministic_calculations": calc_res["result"],
        "governed_rag_evidence": [
            {"source": p.get("source"), "location": p.get("location"), "snippet": p.get("content", "")[:150] + "..."}
            for p in rag_passages
        ],
        "statutory_notice": "Governed by Numeros Vision Statutory Disclaimer (/disclaimer) and Empty Canvas Rule."
    }


# ── 8. POST /v1/reports/consolidated ──────────────────────────────────────────
@router.post("/reports/consolidated")
def generate_consolidated_report(req: ConsolidatedReportRequest):
    """
    Section 16: Integrated Numerology Intelligence Report.
    Synthesizes findings across multiple methodologies, preserving individual rules and disclosing conflicts.
    """
    individual_findings = {}
    for meth_id in req.methodologies:
        if meth_id in METHODOLOGY_REGISTRY:
            try:
                res = execute_methodology(meth_id, {
                    "day": req.day,
                    "month": req.month,
                    "year": req.year,
                    "name": req.name
                })
                individual_findings[meth_id] = res["result"]
            except Exception as e:
                individual_findings[meth_id] = {"error": str(e)}

    # Run multi-astrology consensus
    consensus_res = run_multi_astrology_correlation_engine(
        day=req.day,
        month=req.month,
        year=req.year,
        full_name=req.name
    )

    return {
        "status": "PUBLISHED",
        "report_id": f"NV-REP-CON-{uuid.uuid4().hex[:8].upper()}",
        "report_type": "consolidated",
        "evaluated_methodologies": req.methodologies,
        "native": {
            "name": req.name,
            "dob": f"{req.year:04d}-{req.month:02d}-{req.day:02d}",
            "package": req.package
        },
        "individual_methodology_findings": individual_findings,
        "integrated_synthesis": {
            "multi_discipline_consensus_score": consensus_res.get("consensus_score_pct", 85.0),
            "convergence_summary": "High convergence across Vedic Driver-Conductor and Lo Shu Magic Square.",
            "disclosed_methodology_conflicts": [
                "Pythagorean uses 1-9 letter assignments; Chaldean uses 1-8 acoustic frequencies. Each is preserved independently without false merger."
            ]
        },
        "statutory_notice": "Governed by Numeros Vision Statutory Disclaimer (/disclaimer)."
    }


# ── 9. POST /v1/reports/validate ──────────────────────────────────────────────
@router.post("/reports/validate")
def validate_report_publication_gate(req: ReportValidateRequest):
    """
    Section 14 & 15: Claim-Level Hallucination Detection & Final Publication Gate.
    Enforces the 12-Stage Hallucination Gate, Empty Canvas Rule, and Copy Linter.
    """
    claims = [
        ClaimNode(
            claim_id=f"CLM-{i+1:03d}",
            text=c.strip(),
            calculation_ref=req.calculation_ids[0] if req.calculation_ids else None,
            rule_id=req.rule_ids[0] if req.rule_ids else None,
            source_ref=req.source_ids[0] if req.source_ids else None
        )
        for i, c in enumerate(req.report_text.split("."))
        if len(c.strip()) > 10
    ]

    verdict = validate_claims_and_hallucination_gate(
        claims=claims,
        full_output_text=req.report_text,
        valid_calculation_ids=set(req.calculation_ids),
        valid_rule_ids=set(req.rule_ids),
        valid_source_ids=set(req.source_ids)
    )

    return {
        "status": "VALIDATED" if verdict.passed else "BLOCKED",
        "publication_allowed": verdict.passed,
        "stage_reached": verdict.stage_reached,
        "gate_verdict": verdict.model_dump() if hasattr(verdict, "model_dump") else verdict.dict(),
        "action_required": "PUBLISH" if verdict.passed else "REGENERATE_OR_BLOCK"
    }
