"""
NUMEROS VISION & ASKNUMEROAI — OBSERVABILITY, WORKFLOW TRACING & COST ACCOUNTING
Specification: AI Cost and Token Optimization Architecture (Sections 12, 13 & 14)

Key Capabilities:
1. Complete Workflow Tracing:
   Captures per-workflow tokens, tiered model costs (USD & INR), cache hit status,
   retrieval costs, and execution duration.
2. Real-Time Cost Governance & Metrics:
   Provides total AI cost, cost per successful workflow, token consumption breakdown,
   and deterministic bypass savings.
3. Pre-Inference Budget Controls:
   Validates estimated token usage against task-level and user-plan limits before calling models.
4. Graceful Degradation:
   Falls back Smoothly to deterministic zero-cost templates when budgets are constrained.
"""

import time
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from pydantic import BaseModel, Field

from app.engine.model_router import (
    ModelTier,
    TaskType,
    ModelSpec,
    MODEL_REGISTRY,
    TASK_BUDGETS,
    USD_TO_INR_RATE,
    model_router
)
from app.engine.cost_optimized_cache import cost_cache, CacheTier
from app.engine.ai_cost_and_security import check_and_meter_usage, PLAN_TOKEN_LIMITS


class WorkflowTrace(BaseModel):
    workflow_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    task_type: str
    model_tier: str
    model_name: str
    user_id: Optional[str] = "anonymous"
    input_tokens: int = 0
    output_tokens: int = 0
    cached_input_tokens: int = 0
    model_cost_usd: float = 0.0
    model_cost_inr: float = 0.0
    retrieval_cost_usd: float = 0.0
    cache_hit: bool = False
    cache_tier: Optional[str] = None
    duration_ms: float = 0.0
    status: str = "success"  # "success", "budget_degraded", "escalated", "error"
    error_message: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class CostAccountingService:
    """
    Central accounting engine tracking AI inference costs, token consumption,
    and cost-per-workflow optimization metrics.
    """

    def __init__(self, inr_rate: float = USD_TO_INR_RATE, max_traces: int = 5000):
        self.inr_rate = inr_rate
        self.max_traces = max_traces
        self._traces: Dict[str, WorkflowTrace] = {}

        # Aggregated telemetry
        self.aggregated_metrics = {
            "total_workflows": 0,
            "successful_workflows": 0,
            "budget_degraded_workflows": 0,
            "escalated_workflows": 0,
            "failed_workflows": 0,
            "total_input_tokens": 0,
            "total_output_tokens": 0,
            "total_cached_input_tokens": 0,
            "total_model_cost_usd": 0.0,
            "total_model_cost_inr": 0.0,
            "total_retrieval_cost_usd": 0.0,
            "cache_hits_count": 0,
            "deterministic_bypass_count": 0,
            "deterministic_savings_usd": 0.0,
            "deterministic_savings_inr": 0.0,
            "by_task_type": {t.value: {"count": 0, "cost_usd": 0.0, "tokens": 0} for t in TaskType},
            "by_model_tier": {m.value: {"count": 0, "cost_usd": 0.0, "tokens": 0} for m in ModelTier},
        }

    def record_trace(self, trace: WorkflowTrace) -> str:
        """Records a completed workflow trace and updates aggregate cost meters."""
        if len(self._traces) >= self.max_traces:
            # Drop oldest trace
            oldest_id = next(iter(self._traces))
            del self._traces[oldest_id]

        self._traces[trace.workflow_id] = trace

        # Update aggregates
        self.aggregated_metrics["total_workflows"] += 1
        if trace.status == "success":
            self.aggregated_metrics["successful_workflows"] += 1
        elif trace.status == "budget_degraded":
            self.aggregated_metrics["budget_degraded_workflows"] += 1
        elif trace.status == "escalated":
            self.aggregated_metrics["escalated_workflows"] += 1
        elif trace.status == "error":
            self.aggregated_metrics["failed_workflows"] += 1

        self.aggregated_metrics["total_input_tokens"] += trace.input_tokens
        self.aggregated_metrics["total_output_tokens"] += trace.output_tokens
        self.aggregated_metrics["total_cached_input_tokens"] += trace.cached_input_tokens

        self.aggregated_metrics["total_model_cost_usd"] = round(
            self.aggregated_metrics["total_model_cost_usd"] + trace.model_cost_usd, 6
        )
        self.aggregated_metrics["total_model_cost_inr"] = round(
            self.aggregated_metrics["total_model_cost_inr"] + trace.model_cost_inr, 4
        )
        self.aggregated_metrics["total_retrieval_cost_usd"] = round(
            self.aggregated_metrics["total_retrieval_cost_usd"] + trace.retrieval_cost_usd, 6
        )

        if trace.cache_hit:
            self.aggregated_metrics["cache_hits_count"] += 1

        if trace.model_tier == ModelTier.DETERMINISTIC.value:
            self.aggregated_metrics["deterministic_bypass_count"] += 1
            # Benchmark saving: each calculation bypass saves ~0.0025 USD compared to standard LLM call
            savings = 0.0025
            self.aggregated_metrics["deterministic_savings_usd"] = round(
                self.aggregated_metrics["deterministic_savings_usd"] + savings, 6
            )
            self.aggregated_metrics["deterministic_savings_inr"] = round(
                self.aggregated_metrics["deterministic_savings_usd"] * self.inr_rate, 4
            )

        # By task type
        tt = trace.task_type
        if tt in self.aggregated_metrics["by_task_type"]:
            self.aggregated_metrics["by_task_type"][tt]["count"] += 1
            self.aggregated_metrics["by_task_type"][tt]["cost_usd"] = round(
                self.aggregated_metrics["by_task_type"][tt]["cost_usd"] + trace.model_cost_usd, 6
            )
            self.aggregated_metrics["by_task_type"][tt]["tokens"] += (trace.input_tokens + trace.output_tokens)

        # By model tier
        mt = trace.model_tier
        if mt in self.aggregated_metrics["by_model_tier"]:
            self.aggregated_metrics["by_model_tier"][mt]["count"] += 1
            self.aggregated_metrics["by_model_tier"][mt]["cost_usd"] = round(
                self.aggregated_metrics["by_model_tier"][mt]["cost_usd"] + trace.model_cost_usd, 6
            )
            self.aggregated_metrics["by_model_tier"][mt]["tokens"] += (trace.input_tokens + trace.output_tokens)

        return trace.workflow_id

    def get_trace(self, workflow_id: str) -> Optional[WorkflowTrace]:
        """Fetches a specific workflow trace by ID."""
        return self._traces.get(workflow_id)

    def validate_task_budget(
        self,
        task_type: TaskType,
        estimated_input_tokens: int,
        estimated_output_tokens: int,
        user_plan: str = "free",
        user_id: str = "anonymous"
    ) -> Dict[str, Any]:
        """
        Pre-inference gate verifying token limits against task-level and user subscription caps.
        Returns governance decision: 'proceed', 'degrade_to_deterministic', or 'reject'.
        """
        budget_spec = TASK_BUDGETS.get(task_type, TASK_BUDGETS[TaskType.BASIC_INTERPRETATION])
        total_estimated = estimated_input_tokens + estimated_output_tokens

        # Deterministic calculations always pass
        if task_type == TaskType.DETERMINISTIC_CALCULATION:
            return {
                "allowed": True,
                "action": "proceed",
                "recommended_tier": ModelTier.DETERMINISTIC.value,
                "estimated_cost_usd": 0.0,
                "reason": "Deterministic calculation executes in application code at zero cost."
            }

        # Check task budget caps
        max_task_tokens = budget_spec["max_input_tokens"] + budget_spec["max_output_tokens"]
        if total_estimated > (max_task_tokens * 1.5):
            # Exceeds task cap significantly: degrade gracefully
            return {
                "allowed": True,
                "action": "degrade_to_deterministic",
                "recommended_tier": ModelTier.DETERMINISTIC.value,
                "estimated_cost_usd": 0.0,
                "reason": f"Estimated tokens ({total_estimated}) exceed maximum budget cap for {task_type.value}. Falling back to zero-cost deterministic synthesis."
            }

        # Check user-level plan budget
        model_spec = model_router.select_model(task_type, user_plan)
        cost_est = model_router.estimate_cost(model_spec, estimated_input_tokens, estimated_output_tokens)

        # Check if plan limit is exhausted
        user_allowed = check_and_meter_usage(user_id, total_estimated, user_plan)
        if not user_allowed:
            return {
                "allowed": True,
                "action": "degrade_to_deterministic",
                "recommended_tier": ModelTier.DETERMINISTIC.value,
                "estimated_cost_usd": 0.0,
                "reason": f"Subscription plan limit reached for user {user_id}. Degrading to zero-cost deterministic engine."
            }

        return {
            "allowed": True,
            "action": "proceed",
            "recommended_tier": model_spec.tier.value,
            "model_id": model_spec.model_id,
            "estimated_cost_usd": cost_est["total_cost_usd"],
            "estimated_cost_inr": cost_est["total_cost_inr"],
            "reason": "Request complies with task budget and user subscription quota."
        }

    def get_metrics_summary(self) -> Dict[str, Any]:
        """
        Returns full observability report adhering to Section 12 & 14 specifications.
        """
        successful = self.aggregated_metrics["successful_workflows"]
        total_cost_usd = self.aggregated_metrics["total_model_cost_usd"]
        cost_per_successful_workflow_usd = (
            round(total_cost_usd / successful, 6) if successful > 0 else 0.0
        )
        cost_per_successful_workflow_inr = round(
            cost_per_successful_workflow_usd * self.inr_rate, 4
        )

        cache_stats = cost_cache.get_stats()

        return {
            "overview": {
                "total_workflows": self.aggregated_metrics["total_workflows"],
                "successful_workflows": successful,
                "budget_degraded_workflows": self.aggregated_metrics["budget_degraded_workflows"],
                "escalated_workflows": self.aggregated_metrics["escalated_workflows"],
                "failed_workflows": self.aggregated_metrics["failed_workflows"],
                "success_rate_pct": (
                    round((successful / self.aggregated_metrics["total_workflows"] * 100.0), 2)
                    if self.aggregated_metrics["total_workflows"] > 0 else 100.0
                ),
            },
            "token_consumption": {
                "total_input_tokens": self.aggregated_metrics["total_input_tokens"],
                "total_output_tokens": self.aggregated_metrics["total_output_tokens"],
                "total_cached_input_tokens": self.aggregated_metrics["total_cached_input_tokens"],
                "total_billable_tokens": (
                    self.aggregated_metrics["total_input_tokens"] +
                    self.aggregated_metrics["total_output_tokens"]
                ),
            },
            "financials": {
                "total_ai_cost_usd": total_cost_usd,
                "total_ai_cost_inr": self.aggregated_metrics["total_model_cost_inr"],
                "cost_per_successful_workflow_usd": cost_per_successful_workflow_usd,
                "cost_per_successful_workflow_inr": cost_per_successful_workflow_inr,
                "currency_rate_usd_to_inr": self.inr_rate,
            },
            "optimization_savings": {
                "deterministic_bypass_count": self.aggregated_metrics["deterministic_bypass_count"],
                "deterministic_savings_usd": self.aggregated_metrics["deterministic_savings_usd"],
                "deterministic_savings_inr": self.aggregated_metrics["deterministic_savings_inr"],
                "cache_tokens_saved": cache_stats["overall"]["tokens_saved"],
                "cache_savings_usd": cache_stats["overall"]["cost_saved_usd"],
                "cache_savings_inr": cache_stats["overall"]["cost_saved_inr"],
                "cache_hit_rate_pct": cache_stats["overall"]["hit_rate_pct"],
                "total_combined_savings_usd": round(
                    self.aggregated_metrics["deterministic_savings_usd"] + cache_stats["overall"]["cost_saved_usd"], 6
                ),
                "total_combined_savings_inr": round(
                    self.aggregated_metrics["deterministic_savings_inr"] + cache_stats["overall"]["cost_saved_inr"], 4
                ),
            },
            "breakdown": {
                "by_task_type": self.aggregated_metrics["by_task_type"],
                "by_model_tier": self.aggregated_metrics["by_model_tier"],
            }
        }


# Global accounting service singleton
cost_accounting = CostAccountingService()
