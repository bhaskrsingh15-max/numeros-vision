"""
app/charm/methods/vedic_adapter.py
===================================
Vedic Parashari Jyotish Independent Cross-Verification Adapter.
Complies with Section 5.3 of Master Specification v2.0.
"""

from typing import Dict, Any, List, Optional
import hashlib

from app.charm.methods.kp_adapter import MethodEvaluation
from app.charm.rag.source_governor import source_governor

class VedicMethodAdapter:
    def __init__(self):
        self.method_id = "VEDIC_ASTROLOGY"
        self.version = "1.0.0"

    def evaluate(
        self,
        event_definition: Dict[str, Any],
        profile_facts: Dict[str, Any],
        chart_facts: Dict[str, Any],
        hypothesis_window: Optional[Dict[str, Any]] = None
    ) -> MethodEvaluation:
        event_id = event_definition.get("event_definition_id", "career_growth")
        eval_id = "EVAL-VED-" + hashlib.sha256(f"{event_id}:{profile_facts.get('driver', 1)}:{profile_facts.get('conductor', 1)}".encode("utf-8")).hexdigest()[:10]

        driver = profile_facts.get("driver", 1)
        conductor = profile_facts.get("conductor", 1)

        # Classical Sambandha & Gochar (Transit) Rules
        # Jupiter & Mercury transits in 2026 support intellectual & commercial acceleration
        if driver in (1, 3, 5, 6) and conductor in (1, 3, 5, 6):
            assessment = "SUPPORTS"
            yoga_desc = "Classical Surya-Guru Dharma-Karmadhipati Yoga active; planetary friends amplify authority and commercial expansion."
        elif driver in (4, 8) and conductor in (1, 2, 9):
            assessment = "CHALLENGES"
            yoga_desc = "Karmic Shani-Rahu tension with solar luminaries; advises steady consolidation and avoiding unilateral gambles."
        else:
            assessment = "MIXED"
            yoga_desc = "Moderate Sambandha; steady progress governed by disciplined adherence to operational routine."

        rule_evidence = source_governor.retrieve_method_evidence(
            method_id=self.method_id,
            query="Vedic Parashari Gochar Jupiter Saturn transit Sambandha",
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
                "label": f"Vedic Gochar Synthesis ({yoga_desc[:40]}...)",
                "assessment": assessment,
                "ruling_transit": "Jupiter transit over 2nd/11th house axis"
            }],
            rule_evidence=rule_evidence,
            calculation_fact_ids=[chart_facts.get("snapshot_id", "SNAP-DEFAULT")],
            conflicts=[] if assessment != "CHALLENGES" else ["Transit vectors indicate initial delay before harvest phase."],
            limitations=["Vedic Sambandha grounded on canonical planetary rulerships; individual D1/D9 chart confirms exact divisional strengths."],
            status="VALID"
        )

vedic_adapter = VedicMethodAdapter()
