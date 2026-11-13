"""
NUMEROS VISION & ASKNUMEROAI — COST GOVERNANCE & AI OBSERVABILITY API
Endpoints implementing Section 12, 13 & 14 of the Cost Optimization Architecture Specification.

Routes:
- GET  /api/v1/cost/metrics
- GET  /api/v1/cost/workflow-trace/{workflow_id}
- GET  /api/v1/cost/model-registry
- POST /api/v1/cost/budget-check
- POST /api/v1/cost/optimize-query
"""

import time
from typing import Dict, Any, Optional, List
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from app.engine.model_router import (
    ModelTier,
    TaskType,
    MODEL_REGISTRY,
    TASK_BUDGETS,
    model_router
)
from app.engine.cost_optimized_cache import cost_cache, CacheTier
from app.engine.cost_accounting import (
    cost_accounting,
    WorkflowTrace
)
from app.engine.ai_cost_and_security import sanitize_user_input
from app.engine.vedic_numerology import analyze_vedic_numerology
from app.engine.lo_shu import analyze_lo_shu_grid
from app.engine.cheiro_engine import analyze_name_cheiro
from app.engine.professional_numerology_engine import audit_mobile_number
from app.engine.zero_cost_llm import synthesize_zero_cost_narrative

router = APIRouter(prefix="/api/v1/cost", tags=["AI Cost Governance & Observability"])


class BudgetCheckRequest(BaseModel):
    task_type: TaskType
    estimated_input_tokens: int = 500
    estimated_output_tokens: int = 300
    user_plan: str = "free"
    user_id: str = "anonymous"


class OptimizeQueryRequest(BaseModel):
    query: str
    user_id: Optional[str] = "anonymous"
    user_plan: Optional[str] = "free"
    dob: Optional[str] = None           # e.g., "1995-08-15" or "15/08/1995"
    name: Optional[str] = None          # e.g., "Bhaskr Singh"
    mobile: Optional[str] = None        # e.g., "9876543210"
    force_tier: Optional[ModelTier] = None


@router.get("/metrics")
def get_cost_and_usage_metrics():
    """
    Returns real-time AI cost observability, total token counts, cost-per-successful-workflow,
    and optimization savings from deterministic bypass and multi-tier caching.
    """
    return cost_accounting.get_metrics_summary()


@router.get("/workflow-trace/{workflow_id}")
def get_workflow_trace(workflow_id: str):
    """
    Retrieves the execution and cost trace for a specific workflow execution.
    """
    trace = cost_accounting.get_trace(workflow_id)
    if not trace:
        raise HTTPException(status_code=404, detail=f"Workflow trace '{workflow_id}' not found.")
    return trace.model_dump()


@router.get("/model-registry")
def get_model_registry_and_pricing():
    """
    Returns active model tiers, pricing tables (USD & INR per 1M tokens),
    context window caps, and task budget allocations.
    """
    return {
        "models": {k.value: v.model_dump() for k, v in MODEL_REGISTRY.items()},
        "task_budgets": {k.value: v for k, v in TASK_BUDGETS.items()},
        "cache_ttls_seconds": {
            tier.value: cost_cache._stores[tier] for tier in CacheTier
        } if hasattr(cost_cache, "_stores") else {}
    }


@router.post("/budget-check")
def pre_inference_budget_check(req: BudgetCheckRequest):
    """
    Pre-inference validation verifying if the estimated token consumption
    fits within task budget caps and user plan limits.
    """
    decision = cost_accounting.validate_task_budget(
        task_type=req.task_type,
        estimated_input_tokens=req.estimated_input_tokens,
        estimated_output_tokens=req.estimated_output_tokens,
        user_plan=req.user_plan,
        user_id=req.user_id
    )
    return decision


@router.post("/optimize-query")
def optimize_and_route_query(req: OptimizeQueryRequest):
    """
    Executes end-to-end Cost-Optimized Routing:
    1. Input sanitization (defense against prompt injection and IP extraction).
    2. Multi-tier cache lookup (serves repeated questions in <1ms at $0).
    3. Deterministic calculation bypass (computes math in code at $0 cost / 0 tokens).
    4. Task budget checks & intelligent model tier selection.
    5. Complete workflow trace capture.
    """
    start_time = time.time()
    
    # 1. Sanitize input
    try:
        clean_query = sanitize_user_input(req.query)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # 2. Check Cache
    cached_val = cost_cache.get(
        tier=CacheTier.ANSWERS,
        method="optimize_query",
        inputs={"query": clean_query, "dob": req.dob, "name": req.name},
        user_id=req.user_id if req.user_id != "anonymous" else None
    )
    if cached_val:
        elapsed = round((time.time() - start_time) * 1000, 2)
        trace = WorkflowTrace(
            task_type="cached_answer",
            model_tier="cache",
            model_name="cost_optimized_cache",
            user_id=req.user_id,
            input_tokens=0,
            output_tokens=0,
            cached_input_tokens=0,
            model_cost_usd=0.0,
            model_cost_inr=0.0,
            cache_hit=True,
            cache_tier=CacheTier.ANSWERS.value,
            duration_ms=elapsed,
            status="success"
        )
        cost_accounting.record_trace(trace)
        return {
            "workflow_id": trace.workflow_id,
            "source": "cache_hit",
            "tier": "cache",
            "cost_usd": 0.0,
            "duration_ms": elapsed,
            "result": cached_val
        }

    # 3. Classify Task
    context = {"dob": req.dob, "name": req.name, "mobile": req.mobile}
    task_type = model_router.classify_task(clean_query, context)

    # 4. Deterministic Bypass Handling
    if task_type == TaskType.DETERMINISTIC_CALCULATION:
        # Resolve calculations in application code
        calc_result: Dict[str, Any] = {"calculation_type": "deterministic_bypass"}

        if req.dob:
            # Parse day, month, year
            parts = req.dob.replace("/", "-").split("-")
            if len(parts) == 3:
                try:
                    if len(parts[0]) == 4:  # YYYY-MM-DD
                        y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
                    else:  # DD-MM-YYYY
                        d, m, y = int(parts[0]), int(parts[1]), int(parts[2])
                    vedic = analyze_vedic_numerology(d, m, y)
                    lo_shu = analyze_lo_shu_grid(d, m, y)
                    calc_result["vedic"] = vedic
                    calc_result["lo_shu"] = lo_shu
                except Exception:
                    pass

        if req.name:
            calc_result["cheiro_name"] = analyze_name_cheiro(req.name)

        if req.mobile:
            calc_result["mobile_audit"] = audit_mobile_number(req.mobile)

        elapsed = round((time.time() - start_time) * 1000, 2)
        trace = WorkflowTrace(
            task_type=task_type.value,
            model_tier=ModelTier.DETERMINISTIC.value,
            model_name="deterministic-native-engine",
            user_id=req.user_id,
            input_tokens=0,
            output_tokens=0,
            cached_input_tokens=0,
            model_cost_usd=0.0,
            model_cost_inr=0.0,
            cache_hit=False,
            duration_ms=elapsed,
            status="success"
        )
        cost_accounting.record_trace(trace)

        # Store in calculation cache
        cost_cache.set(
            tier=CacheTier.CALCULATIONS,
            method="deterministic_bypass",
            inputs={"query": clean_query, "dob": req.dob, "name": req.name},
            value=calc_result
        )

        return {
            "workflow_id": trace.workflow_id,
            "source": "deterministic_engine",
            "tier": ModelTier.DETERMINISTIC.value,
            "cost_usd": 0.0,
            "duration_ms": elapsed,
            "result": calc_result
        }

    # 5. Non-deterministic / Narrative task: Model routing & Budget check
    model_spec = model_router.select_model(
        task_type=task_type,
        user_plan=req.user_plan or "free",
        force_tier=req.force_tier
    )

    budget_decision = cost_accounting.validate_task_budget(
        task_type=task_type,
        estimated_input_tokens=800,
        estimated_output_tokens=400,
        user_plan=req.user_plan or "free",
        user_id=req.user_id or "anonymous"
    )

    if budget_decision.get("action") == "degrade_to_deterministic":
        # Graceful degradation fallback
        dummy_consensus = {
            "user_name": req.name or "Seeker",
            "vedic_numerology": {"driver_number": 1, "driver_planet": "Sun", "conductor_number": 4, "conductor_planet": "Rahu"},
            "lo_shu_grid": {"completed_planes": []},
            "cheiro_name_analysis": {"compound_archetype": "Harmonic Resonance", "name_root": 6}
        }
        fallback_narrative = synthesize_zero_cost_narrative(dummy_consensus, clean_query)
        elapsed = round((time.time() - start_time) * 1000, 2)

        trace = WorkflowTrace(
            task_type=task_type.value,
            model_tier=ModelTier.DETERMINISTIC.value,
            model_name="graceful_degradation_synthesizer",
            user_id=req.user_id,
            input_tokens=0,
            output_tokens=0,
            cached_input_tokens=0,
            model_cost_usd=0.0,
            model_cost_inr=0.0,
            cache_hit=False,
            duration_ms=elapsed,
            status="budget_degraded"
        )
        cost_accounting.record_trace(trace)

        return {
            "workflow_id": trace.workflow_id,
            "source": "graceful_degradation_fallback",
            "tier": ModelTier.DETERMINISTIC.value,
            "cost_usd": 0.0,
            "duration_ms": elapsed,
            "result": {"narrative": fallback_narrative, "degradation_reason": budget_decision.get("reason")}
        }

    # Simulated optimized inference output
    input_tokens = 750
    output_tokens = 320
    cached_tokens = 250
    cost_est = model_router.estimate_cost(model_spec, input_tokens, output_tokens, cached_tokens)
    elapsed = round((time.time() - start_time) * 1000, 2)

    synthetic_response = {
        "interpretation": f"Numeros Vision analysis for query '{clean_query}': Harmonics align favorably with your core matrix.",
        "model_used": model_spec.model_id,
        "tier": model_spec.tier.value
    }

    trace = WorkflowTrace(
        task_type=task_type.value,
        model_tier=model_spec.tier.value,
        model_name=model_spec.model_id,
        user_id=req.user_id,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        cached_input_tokens=cached_tokens,
        model_cost_usd=cost_est["total_cost_usd"],
        model_cost_inr=cost_est["total_cost_inr"],
        cache_hit=False,
        duration_ms=elapsed,
        status="success"
    )
    cost_accounting.record_trace(trace)

    # Store in answers cache
    cost_cache.set(
        tier=CacheTier.ANSWERS,
        method="optimize_query",
        inputs={"query": clean_query, "dob": req.dob, "name": req.name},
        value=synthetic_response,
        user_id=req.user_id if req.user_id != "anonymous" else None
    )

    return {
        "workflow_id": trace.workflow_id,
        "source": "ai_inference",
        "tier": model_spec.tier.value,
        "model_id": model_spec.model_id,
        "cost_usd": cost_est["total_cost_usd"],
        "cost_inr": cost_est["total_cost_inr"],
        "duration_ms": elapsed,
        "result": synthetic_response
    }
