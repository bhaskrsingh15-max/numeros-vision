"""
NUMEROS VISION & ASKNUMEROAI — INTELLIGENT MODEL ROUTER & MODEL REGISTRY
Specification: AI Cost and Token Optimization Architecture (Sections 4, 6, 7 & 10)

Key Capabilities:
1. Deterministic Calculation Bypass:
   Intercepts math queries (Driver, Conductor, Kua, Lo Shu, Name vibration, Mobile, Vehicle)
   and directs them to native deterministic engines at $0.00 cost / 0 LLM tokens.
2. 3-Tier AI Model Registry with Live Pricing:
   - Small Model (Flash / Haiku tier): Fast, ultra-cheap intent routing, FAQ, and short snippets.
   - Standard Model (Pro / Sonnet tier): Comprehensive readings, personal cycles, and matrix interpretation.
   - Premium Model (Ultra / Opus tier): Multi-system synastry, complex astrological-numerology consensus.
3. Pre-Inference Task Budget Caps & Token Limits.
4. Quality-Based Escalation:
   Automatically escalates from Small to Standard tier if response quality/grounding score is below threshold.
5. Graceful Degradation:
   Falls back Smoothly to local zero-cost deterministic synthesis when budgets are exhausted or APIs are offline.
"""

import re
from enum import Enum
from typing import Dict, Any, Optional, Tuple, List
from pydantic import BaseModel


class ModelTier(str, Enum):
    DETERMINISTIC = "deterministic"
    SMALL = "small"
    STANDARD = "standard"
    PREMIUM = "premium"


class TaskType(str, Enum):
    DETERMINISTIC_CALCULATION = "deterministic_calculation"
    FAQ_KNOWLEDGE = "faq_knowledge"
    BASIC_INTERPRETATION = "basic_interpretation"
    COMPREHENSIVE_READING = "comprehensive_reading"
    CROSS_SYSTEM_SYNTHESIS = "cross_system_synthesis"


class ModelSpec(BaseModel):
    tier: ModelTier
    model_id: str
    provider: str
    input_cost_per_1m: float           # USD per 1M billable input tokens
    cached_input_cost_per_1m: float    # USD per 1M cached input tokens
    output_cost_per_1m: float          # USD per 1M billable output tokens
    max_context_tokens: int
    max_output_tokens: int
    typical_latency_ms: int
    description: str


# Live Model Registry with Transparent Pricing (Gemini / Anthropic parity)
MODEL_REGISTRY: Dict[ModelTier, ModelSpec] = {
    ModelTier.DETERMINISTIC: ModelSpec(
        tier=ModelTier.DETERMINISTIC,
        model_id="deterministic-native-engine",
        provider="numeros_vision_core",
        input_cost_per_1m=0.0,
        cached_input_cost_per_1m=0.0,
        output_cost_per_1m=0.0,
        max_context_tokens=0,
        max_output_tokens=0,
        typical_latency_ms=2,
        description="Zero-cost in-memory Python calculation engine. $0.00 API inference cost."
    ),
    ModelTier.SMALL: ModelSpec(
        tier=ModelTier.SMALL,
        model_id="gemini-1.5-flash",
        provider="google",
        input_cost_per_1m=0.15,          # $0.15 / 1M tokens
        cached_input_cost_per_1m=0.0375,  # $0.0375 / 1M tokens (75% discount)
        output_cost_per_1m=0.60,         # $0.60 / 1M tokens
        max_context_tokens=4000,
        max_output_tokens=800,
        typical_latency_ms=250,
        description="Fast, low-cost model for classification, FAQs, query normalization, and quick remedies."
    ),
    ModelTier.STANDARD: ModelSpec(
        tier=ModelTier.STANDARD,
        model_id="gemini-1.5-pro",
        provider="google",
        input_cost_per_1m=1.25,          # $1.25 / 1M tokens
        cached_input_cost_per_1m=0.3125,  # $0.3125 / 1M tokens
        output_cost_per_1m=5.00,         # $5.00 / 1M tokens
        max_context_tokens=16000,
        max_output_tokens=2500,
        typical_latency_ms=750,
        description="High-fidelity model for comprehensive personal chart readings, cycles, and narrative balancing."
    ),
    ModelTier.PREMIUM: ModelSpec(
        tier=ModelTier.PREMIUM,
        model_id="gemini-ultra",
        provider="google",
        input_cost_per_1m=5.00,          # $5.00 / 1M tokens
        cached_input_cost_per_1m=1.25,    # $1.25 / 1M tokens
        output_cost_per_1m=15.00,        # $15.00 / 1M tokens
        max_context_tokens=32000,
        max_output_tokens=4000,
        typical_latency_ms=1800,
        description="Deep reasoning model for multi-tradition cross-verification, synastry, and complex remediation."
    )
}

# Task-level token and budget constraints
TASK_BUDGETS: Dict[TaskType, Dict[str, Any]] = {
    TaskType.DETERMINISTIC_CALCULATION: {
        "max_input_tokens": 0,
        "max_output_tokens": 0,
        "max_cost_usd": 0.000,
        "recommended_tier": ModelTier.DETERMINISTIC
    },
    TaskType.FAQ_KNOWLEDGE: {
        "max_input_tokens": 600,
        "max_output_tokens": 300,
        "max_cost_usd": 0.001,
        "recommended_tier": ModelTier.SMALL
    },
    TaskType.BASIC_INTERPRETATION: {
        "max_input_tokens": 1500,
        "max_output_tokens": 600,
        "max_cost_usd": 0.005,
        "recommended_tier": ModelTier.SMALL
    },
    TaskType.COMPREHENSIVE_READING: {
        "max_input_tokens": 4000,
        "max_output_tokens": 1500,
        "max_cost_usd": 0.020,
        "recommended_tier": ModelTier.STANDARD
    },
    TaskType.CROSS_SYSTEM_SYNTHESIS: {
        "max_input_tokens": 8000,
        "max_output_tokens": 3000,
        "max_cost_usd": 0.050,
        "recommended_tier": ModelTier.PREMIUM
    }
}

USD_TO_INR_RATE = 85.0


# Regex patterns identifying pure deterministic mathematical queries
DETERMINISTIC_MATH_PATTERNS = [
    r"\b(driver|mulank|birth number)\b",
    r"\b(conductor|bhagyank|destiny number|life path)\b",
    r"\b(kua|kua number)\b",
    r"\b(lo shu|loshu|planes? percentage)\b",
    r"\b(compound number|name compound|name vibration|cheiro name|chaldean name|name root)\b",
    r"\b(mobile (audit|number|total|score)|phone number)\b",
    r"\b(vehicle (number|plate|audit)|car number)\b",
    r"\b(house (number|audit)|flat (number|audit))\b",
    r"\b(missing number|repeated number)\b",
]

# Patterns for FAQ or definitions
FAQ_PATTERNS = [
    r"^(what is|who is|explain|define|meaning of|how does)\b.*(numerology|chaldean|lo shu|kua|gemstone)",
    r"^(what are the plans|pricing|how much|cost of report|refund policy)\b",
]


class IntelligentModelRouter:
    """
    Evaluates requests and selects the most cost-efficient execution strategy.
    """

    def __init__(self, inr_rate: float = USD_TO_INR_RATE):
        self.inr_rate = inr_rate

    def classify_task(self, query: str, context: Optional[Dict[str, Any]] = None) -> TaskType:
        """
        Classifies user query into the appropriate task category.
        Strictly prioritizes deterministic math bypass.
        """
        clean_q = query.lower().strip()
        ctx = context or {}

        # 1. Check if request is an explicit calculation request
        is_calc_request = ctx.get("is_calculation_only", False) or ctx.get("calculation_type") is not None
        if is_calc_request:
            return TaskType.DETERMINISTIC_CALCULATION

        # 2. Check deterministic regex patterns
        # If the user only asks "what is my driver number for 15/08/1995" -> DETERMINISTIC_CALCULATION
        has_dob = bool(re.search(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b", clean_q))
        for pat in DETERMINISTIC_MATH_PATTERNS:
            if re.search(pat, clean_q):
                if any(w in clean_q for w in ["calculate", "what is", "find", "tell me my", "value of"]) or not any(w in clean_q for w in ["future", "predict", "synthesize", "reconcile", "explain in detail"]):
                    return TaskType.DETERMINISTIC_CALCULATION

        # 3. Check FAQ patterns
        for pat in FAQ_PATTERNS:
            if re.search(pat, clean_q):
                return TaskType.FAQ_KNOWLEDGE

        # 4. Check for Cross-System Synthesis
        if any(term in clean_q for term in ["synastry", "compare charts", "cross-system", "bnn and kp", "full synthesis", "comprehensive audit"]):
            return TaskType.CROSS_SYSTEM_SYNTHESIS

        # 5. Check for Comprehensive Reading
        if any(term in clean_q for term in ["full report", "detailed prediction", "career and marriage forecast", "complete reading"]):
            return TaskType.COMPREHENSIVE_READING

        # Default: Basic interpretation
        return TaskType.BASIC_INTERPRETATION

    def select_model(
        self,
        task_type: TaskType,
        user_plan: str = "free",
        force_tier: Optional[ModelTier] = None
    ) -> ModelSpec:
        """
        Routes the task to the optimal model tier based on task complexity and user subscription.
        Enforces plan-aware gating to avoid expensive inference for low-tier users.
        """
        if force_tier:
            return MODEL_REGISTRY[force_tier]

        if task_type == TaskType.DETERMINISTIC_CALCULATION:
            return MODEL_REGISTRY[ModelTier.DETERMINISTIC]

        recommended_tier = TASK_BUDGETS[task_type]["recommended_tier"]

        # Plan-aware downgrade / gating for cost containment
        if user_plan == "free":
            # Free tier never uses premium models
            if recommended_tier == ModelTier.PREMIUM:
                return MODEL_REGISTRY[ModelTier.STANDARD]
            elif recommended_tier == ModelTier.STANDARD:
                return MODEL_REGISTRY[ModelTier.SMALL]
            return MODEL_REGISTRY[ModelTier.SMALL]

        if user_plan in ["basic", "starter"]:
            if recommended_tier == ModelTier.PREMIUM:
                return MODEL_REGISTRY[ModelTier.STANDARD]
            return MODEL_REGISTRY[recommended_tier]

        # Growth / Complete / Pro / Enterprise tier gets recommended tier
        return MODEL_REGISTRY[recommended_tier]

    def estimate_cost(
        self,
        model_spec: ModelSpec,
        input_tokens: int,
        output_tokens: int,
        cached_input_tokens: int = 0
    ) -> Dict[str, float]:
        """
        Calculates exact inference cost in USD and INR.
        Distinguishes between standard input tokens and discounted cached input tokens.
        """
        if model_spec.tier == ModelTier.DETERMINISTIC:
            return {
                "input_cost_usd": 0.0,
                "cached_input_cost_usd": 0.0,
                "output_cost_usd": 0.0,
                "total_cost_usd": 0.0,
                "total_cost_inr": 0.0
            }

        billable_fresh_input = max(0, input_tokens - cached_input_tokens)
        input_cost = (billable_fresh_input / 1_000_000.0) * model_spec.input_cost_per_1m
        cached_cost = (cached_input_tokens / 1_000_000.0) * model_spec.cached_input_cost_per_1m
        output_cost = (output_tokens / 1_000_000.0) * model_spec.output_cost_per_1m

        total_usd = input_cost + cached_cost + output_cost
        total_inr = total_usd * self.inr_rate

        return {
            "input_cost_usd": round(input_cost, 6),
            "cached_input_cost_usd": round(cached_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_usd, 6),
            "total_cost_inr": round(total_inr, 4)
        }

    def should_escalate(
        self,
        quality_score: float,
        current_tier: ModelTier,
        consensus_variance: float = 0.0
    ) -> Optional[ModelTier]:
        """
        Evaluates whether an inference outcome requires tier escalation.
        Triggered when quality is below 0.6 or cross-tradition variance is high.
        """
        if current_tier == ModelTier.DETERMINISTIC:
            return None  # Deterministic never escalates

        if current_tier == ModelTier.SMALL:
            if quality_score < 0.60 or consensus_variance > 0.40:
                return ModelTier.STANDARD

        elif current_tier == ModelTier.STANDARD:
            if quality_score < 0.40 or consensus_variance > 0.65:
                return ModelTier.PREMIUM

        return None


# Global singleton router
model_router = IntelligentModelRouter()
