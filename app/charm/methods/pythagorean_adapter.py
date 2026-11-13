"""
app/charm/methods/pythagorean_adapter.py
========================================
Western Pythagorean Numerology Independent Cross-Verification Adapter.
Complies with Master Specification v1.0 / Consolidated Specification v1.0.
"""

from typing import Dict, Any, List, Optional
import hashlib
from app.charm.methods.kp_adapter import MethodEvaluation
from app.charm.rag.source_governor import source_governor
from app.engine.pythagorean_engine import (
    calculate_pythagorean_life_path,
    calculate_pythagorean_name,
    WESTERN_PLANETARY_MAP,
    KARMIC_DEBT_MEANINGS
)

class PythagoreanMethodAdapter:
    def __init__(self):
        self.method_id = "PYTHAGOREAN_NUMEROLOGY"
        self.version = "1.0.0"

    def evaluate(
        self,
        event_definition: Dict[str, Any],
        profile_facts: Dict[str, Any],
        chart_facts: Dict[str, Any],
        hypothesis_window: Optional[Dict[str, Any]] = None
    ) -> MethodEvaluation:
        event_id = event_definition.get("event_definition_id", "career_growth")
        day = profile_facts.get("day", 15)
        month = profile_facts.get("month", 8)
        year = profile_facts.get("year", 1990)
        name = profile_facts.get("name", "Seeker")

        eval_id = "EVAL-PYTH-" + hashlib.sha256(f"{event_id}:{day}:{month}:{year}".encode("utf-8")).hexdigest()[:10]

        lp_res = calculate_pythagorean_life_path(day, month, year)
        lp_num = lp_res.get("life_path_number", 1)
        is_master = lp_res.get("is_master_number", False)
        is_karmic = lp_res.get("is_karmic_debt", False)

        name_res = calculate_pythagorean_name(name) if name else {}
        expr_num = name_res.get("expression_number", 1)

        # Career & milestone assessment under Western Pythagorean traditions (strict 1-9 reduction)
        favorable_lps = {1, 3, 5, 8}
        if lp_num in favorable_lps and not is_karmic:
            assessment = "SUPPORTS"
            summary = f"Western Life Path {lp_num} ({WESTERN_PLANETARY_MAP.get(lp_num, {}).get('archetype', 'Builder')}) aligns with structured career elevation."
        elif is_karmic:
            assessment = "CHALLENGES"
            kd_val = lp_res.get("karmic_debt_value")
            kd_info = KARMIC_DEBT_MEANINGS.get(kd_val, {})
            summary = f"Karmic Debt {kd_val} indicates foundational learning curve: {kd_info.get('theme', 'Disciplined focus required')}."
        else:
            assessment = "MIXED"
            summary = f"Western Life Path {lp_num} indicates steady, reflective progress."

        rule_evidence = source_governor.retrieve_method_evidence(
            method_id=self.method_id,
            query="Pythagorean Life Path Master Number Karmic Debt career",
            event_type=event_definition.get("event_type", "career"),
            top_k=2
        )

        return MethodEvaluation(
            evaluation_id=eval_id,
            method_id=self.method_id,
            method_version=self.version,
            event_definition_id=event_id,
            assessment=assessment,
            candidate_windows=[{
                "label": f"Western Pythagorean Alignment: Life Path {lp_num}{' (Master Number)' if is_master else ''}",
                "assessment": assessment,
                "summary": summary
            }],
            rule_evidence=rule_evidence,
            calculation_fact_ids=[chart_facts.get("snapshot_id", "SNAP-DEFAULT")],
            conflicts=[] if assessment != "CHALLENGES" else ["Western Pythagorean karmic debt advises disciplined pacing."],
            limitations=["Western Pythagorean analysis evaluates 1-9 letter vibrations and Master Numbers; works independently of Vedic sidereal Nakshatras."],
            status="VALID"
        )

pythagorean_adapter = PythagoreanMethodAdapter()
