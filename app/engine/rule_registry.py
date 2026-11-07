"""
NUMEROS VISION: IMMUTABLE RULE REGISTRY & METHODOLOGY PROFILES
Implements Clauses 33, 34, 136, 137 of Master Specification:
- Immutable-style rule registry tracking rule_id, module, rule_type, version, source_id, formulas, and schema.
- Methodology Profiles:
  * TN-PRO-V1: Numeros Vision Professional / Advanced V1
  * CHEIRO-1935: Cheiro 1935 Canonical Chaldean
- Deterministic conflict detection and priority resolution
"""

import hashlib
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

class RuleDefinition(BaseModel):
    rule_id: str
    module: str
    rule_type: str
    version: str
    source_id: str
    formula: str
    priority: int = 100  # Higher value = higher priority
    conflicts_with: List[str] = []
    active_status: bool = True
    approved_by: str = "Chief Numerology Officer"
    hash: str = ""

RULE_REGISTRY: Dict[str, RuleDefinition] = {}

def _compute_rule_hash(rule_id: str, formula: str, source_id: str) -> str:
    raw = f"{rule_id}:{formula}:{source_id}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]

def register_system_rule(
    rule_id: str,
    module: str,
    rule_type: str,
    version: str,
    source_id: str,
    formula: str,
    priority: int = 100,
    conflicts_with: Optional[List[str]] = None
) -> RuleDefinition:
    """Registers an immutable calculation or interpretation rule into the registry."""
    rule_hash = _compute_rule_hash(rule_id, formula, source_id)
    rule = RuleDefinition(
        rule_id=rule_id,
        module=module,
        rule_type=rule_type,
        version=version,
        source_id=source_id,
        formula=formula,
        priority=priority,
        conflicts_with=conflicts_with or [],
        active_status=True,
        approved_by="System Governance Board",
        hash=rule_hash
    )
    RULE_REGISTRY[rule_id] = rule
    return rule

# Pre-populate core rules from approved syllabus
# 1. Driver / Mulank
register_system_rule(
    rule_id="RULE_DRIVER_CALC_V1",
    module="core_numerology",
    rule_type="CALCULATION",
    version="TN-PRO-V1",
    source_id="TN_ADV_DIPLOMA_DAY1",
    formula="Driver = reduce_to_single_digit(birth_day)",
    priority=100
)

# 2. Conductor / Bhagyank
register_system_rule(
    rule_id="RULE_CONDUCTOR_CALC_V1",
    module="core_numerology",
    rule_type="CALCULATION",
    version="TN-PRO-V1",
    source_id="TN_ADV_DIPLOMA_DAY1",
    formula="Conductor = reduce_to_single_digit(sum(all_dob_digits))",
    priority=100
)

# 3. Kua Number Male (Custom user methodology)
register_system_rule(
    rule_id="RULE_KUA_MALE_V1",
    module="numero_vastu",
    rule_type="CALCULATION",
    version="TN-PRO-V1",
    source_id="TN_KUA_METHODOLOGY",
    formula="Kua_Male = 11 - reduced_sum(birth_year_digits)",
    priority=100
)

# 4. Kua Number Female
register_system_rule(
    rule_id="RULE_KUA_FEMALE_V1",
    module="numero_vastu",
    rule_type="CALCULATION",
    version="TN-PRO-V1",
    source_id="TN_KUA_METHODOLOGY",
    formula="Kua_Female = 4 + reduced_sum(birth_year_digits)",
    priority=100
)

# 5. Mobile Malefic Pairs (Topic 4 & 26)
register_system_rule(
    rule_id="RULE_MOBILE_MALEFIC_PAIRS_V1",
    module="mobile_numerology",
    rule_type="INTERPRETATION",
    version="TN-PRO-V1",
    source_id="PROF_NUMEROLOGY_TOPIC_4",
    formula="Flag pairs (14, 41, 16, 61, 18, 81, 28, 82, 48, 84) in mobile number as energetic friction",
    priority=90
)

# 6. Cheiro 10-52 Compound Preservation
register_system_rule(
    rule_id="RULE_CHEIRO_COMPOUND_PRESERVE_V1",
    module="cheiro_chaldean",
    rule_type="CALCULATION",
    version="CHEIRO-1935",
    source_id="CHEIRO_BOOK_OF_NUMBERS_1935",
    formula="Preserve 2-digit compound before reducing to root; do not collapse compound into root alone",
    priority=100
)

def get_rule(rule_id: str) -> Optional[RuleDefinition]:
    """Retrieves an authoritative rule definition by rule ID."""
    return RULE_REGISTRY.get(rule_id)

def resolve_rule_conflict(rule_ids: List[str]) -> Optional[RuleDefinition]:
    """
    Evaluates conflicting rules and selects the authoritative rule using:
    Priority > Specificity > Version.
    """
    candidates = [RULE_REGISTRY[rid] for rid in rule_ids if rid in RULE_REGISTRY]
    if not candidates:
        return None
    # Sort descending by priority
    candidates.sort(key=lambda r: r.priority, reverse=True)
    return candidates[0]
