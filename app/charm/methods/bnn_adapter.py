"""
app/charm/methods/bnn_adapter.py
=================================
Bhrigu Nandi Nadi (BNN) Independent Cross-Verification Adapter.
Complies with Section 5.3 of Master Specification v2.0.
"""

from typing import Dict, Any, List, Optional
import hashlib

from app.charm.methods.kp_adapter import MethodEvaluation
from app.charm.rag.source_governor import source_governor
from app.engine.bnn_numerology_engine import evaluate_bnn_numerology_profile

class BNNMethodAdapter:
    def __init__(self):
        self.method_id = "BNN_NADI"
        self.version = "1.0.0"

    def evaluate(
        self,
        event_definition: Dict[str, Any],
        profile_facts: Dict[str, Any],
        chart_facts: Dict[str, Any],
        hypothesis_window: Optional[Dict[str, Any]] = None
    ) -> MethodEvaluation:
        event_id = event_definition.get("event_definition_id", "career_growth")
        driver = profile_facts.get("driver", 1)
        conductor = profile_facts.get("conductor", 1)
        day = profile_facts.get("day", 15)
        month = profile_facts.get("month", 8)
        year = profile_facts.get("year", 1990)
        name = profile_facts.get("name", "Seeker")

        eval_id = "EVAL-BNN-" + hashlib.sha256(f"{event_id}:{driver}:{conductor}".encode("utf-8")).hexdigest()[:10]

        # Use verified BNN pair logic from bnn_numerology_engine
        bnn_prof = evaluate_bnn_numerology_profile(day, month, year, name)
        primary_pair = bnn_prof.get("primary_pair_analysis", {})
        harmony = primary_pair.get("harmony", "Neutral")

        if "Auspicious" in harmony or "Harmonious" in harmony:
            assessment = "SUPPORTS"
            summary = f"BNN Karaka Harmony ({primary_pair.get('title', 'Planetary Flow')}) indicates natural confluence of Karma and Jeeva."
        elif "Challenging" in harmony or "Malefic" in harmony:
            assessment = "CHALLENGES"
            summary = f"BNN Karaka Tension: {primary_pair.get('title', 'Karmic Axis')} requires deliberate elemental balancing."
        else:
            assessment = "MIXED"
            summary = f"BNN Baseline Flow: {primary_pair.get('archetype', 'Balanced Energy')} progresses through steady compounding."

        rule_evidence = source_governor.retrieve_method_evidence(
            method_id=self.method_id,
            query="Bhrigu Nandi Nadi Saturn Karma Jupiter Jeeva Conjunction",
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
                "label": f"BNN Karaka Alignment: {primary_pair.get('archetype', 'Core Flow')}",
                "assessment": assessment,
                "pair_title": primary_pair.get("title", "")
            }],
            rule_evidence=rule_evidence,
            calculation_fact_ids=[chart_facts.get("snapshot_id", "SNAP-DEFAULT")],
            conflicts=[] if assessment != "CHALLENGES" else ["BNN Karaka indicates karmic friction requiring patient remediation."],
            limitations=["BNN evaluation utilizes two-planet Karaka conjunction rules; 3-planet trinal modifiers add specialized refinement."],
            status="VALID"
        )

bnn_adapter = BNNMethodAdapter()
