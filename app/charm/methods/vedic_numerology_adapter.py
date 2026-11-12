"""
app/charm/methods/vedic_numerology_adapter.py
=============================================
Vedic Sankhya Shastra Independent Cross-Verification Adapter.
Complies with Master Specification v1.0 / Consolidated Specification v1.0.
"""

from typing import Dict, Any, List, Optional
import hashlib
from app.charm.methods.kp_adapter import MethodEvaluation
from app.charm.rag.source_governor import source_governor
from app.engine.vedic_numerology import analyze_vedic_numerology
from app.engine.unified_planetary_numerology_engine import evaluate_sankhya_shastra_compound

class VedicNumerologyMethodAdapter:
    def __init__(self):
        self.method_id = "VEDIC_NUMEROLOGY"
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

        eval_id = "EVAL-VNUM-" + hashlib.sha256(f"{event_id}:{day}:{month}:{year}".encode("utf-8")).hexdigest()[:10]

        vedic_res = analyze_vedic_numerology(day, month, year)
        driver = vedic_res["driver_number"]
        conductor = vedic_res["conductor_number"]
        friends = vedic_res.get("friendly_numbers", [])
        enemies = vedic_res.get("enemy_numbers", [])

        sankhya_compound = evaluate_sankhya_shastra_compound(driver, conductor)

        if conductor in friends or sankhya_compound.get("is_friend", False):
            assessment = "SUPPORTS"
            summary = f"Vedic Sankhya Shastra: Driver {driver} ({vedic_res['driver_planet']}) and Conductor {conductor} ({vedic_res['conductor_planet']}) hold natural friendship and harmonious mutual synergy."
        elif conductor in enemies or sankhya_compound.get("is_enemy", False):
            assessment = "CHALLENGES"
            summary = f"Vedic Sankhya Shastra: Driver {driver} and Conductor {conductor} experience dynamic friction, advising deliberate moderation and structured pauses."
        else:
            assessment = "MIXED"
            summary = f"Vedic Sankhya Shastra: Neutral operational balance between Driver {driver} and Conductor {conductor}."

        rule_evidence = source_governor.retrieve_method_evidence(
            method_id=self.method_id,
            query="Vedic Sankhya Shastra Driver Conductor harmony enemy career",
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
                "label": f"Vedic Sankhya Shastra Synergy (Driver {driver} / Conductor {conductor})",
                "assessment": assessment,
                "summary": summary
            }],
            rule_evidence=rule_evidence,
            calculation_fact_ids=[chart_facts.get("snapshot_id", "SNAP-DEFAULT")],
            conflicts=[] if assessment != "CHALLENGES" else ["Sankhya Shastra indicates contrasting planetary polarities between Driver and Conductor."],
            limitations=["Sankhya Shastra evaluates driver-conductor dynamics; planetary dashas determine acute manifestation timing."],
            status="VALID"
        )

vedic_numerology_adapter = VedicNumerologyMethodAdapter()
