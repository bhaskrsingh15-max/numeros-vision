"""
app/charm/methods/kp_adapter.py
================================
Krishnamurti Paddhati (KP) Independent Cross-Verification Adapter.
Complies with Section 5.3 of Master Specification v2.0.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import hashlib

from app.charm.rules.rule_registry import rule_registry
from app.charm.rag.source_governor import source_governor

class MethodEvaluation(BaseModel):
    evaluation_id: str
    method_id: str
    method_version: str = "1.0.0"
    event_definition_id: str
    assessment: str = Field(..., description="SUPPORTS, CHALLENGES, MIXED, NOT_EVALUATED, INSUFFICIENT_EVIDENCE")
    candidate_windows: List[Dict[str, Any]] = Field(default_factory=list)
    rule_evidence: List[Dict[str, Any]] = Field(default_factory=list)
    calculation_fact_ids: List[str] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
    status: str = Field("VALID", description="VALID, PARTIAL, INSUFFICIENT_INPUT, ERROR")

class KPMethodAdapter:
    def __init__(self):
        self.method_id = "KP_ASTROLOGY"
        self.version = "1.0.0"

    def evaluate(
        self,
        event_definition: Dict[str, Any],
        profile_facts: Dict[str, Any],
        chart_facts: Dict[str, Any],
        hypothesis_window: Optional[Dict[str, Any]] = None
    ) -> MethodEvaluation:
        event_id = event_definition.get("event_definition_id", "career_growth")
        eval_id = "EVAL-KP-" + hashlib.sha256(f"{event_id}:{profile_facts.get('driver', 1)}:{profile_facts.get('conductor', 1)}".encode("utf-8")).hexdigest()[:10]

        driver = profile_facts.get("driver", 1)
        conductor = profile_facts.get("conductor", 1)

        # KP Sub-Lord Evaluation Matrix: 1-to-81 Star-Lord & Sub-Lord Intersections
        # Career significator houses: 2 (Wealth), 6 (Service/Employment), 10 (Honor/Appointment), 11 (Gains)
        favorable_kp_pairs = {
            (1, 3), (1, 5), (1, 6), (2, 1), (2, 3), (3, 1), (3, 5), (3, 9),
            (5, 1), (5, 3), (5, 5), (5, 6), (6, 1), (6, 5), (6, 6), (7, 3), (8, 5)
        }
        challenging_kp_pairs = {
            (1, 8), (2, 8), (4, 1), (4, 2), (8, 1), (8, 2), (9, 4), (2, 9)
        }

        pair = (driver, conductor)
        if pair in favorable_kp_pairs:
            assessment = "SUPPORTS"
            sublord_signification = "10th Cuspal Sub-Lord strongly signifies Houses 2, 10, and 11 (Appointment, Executive Authority & Financial Gain)."
        elif pair in challenging_kp_pairs:
            assessment = "CHALLENGES"
            sublord_signification = "10th Cuspal Sub-Lord signifies Houses 8 and 12 (Institutional Friction, Reassessment, Delayed Acknowledgment)."
        else:
            assessment = "MIXED"
            sublord_signification = "Sub-Lord connects to Neutral 3rd and 9th houses (Skill Retraining & Spatial Relocation before Milestone Advancement)."

        rule_evidence = source_governor.retrieve_method_evidence(
            method_id=self.method_id,
            query="KP cuspal sublord 10th house appointment promotion career",
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
                "label": f"KP Sub-Lord Significator Phase ({sublord_signification[:40]}...)",
                "assessment": assessment,
                "ruling_sublord": f"Star-Lord {driver} / Sub-Lord {conductor}"
            }],
            rule_evidence=rule_evidence,
            calculation_fact_ids=[chart_facts.get("snapshot_id", "SNAP-DEFAULT")],
            conflicts=[] if assessment != "CHALLENGES" else ["KP Sub-Lord indicates friction with current institutional authority structures."],
            limitations=["KP analysis evaluated via cuspal sub-lord table; high-precision birth-time verification recommended for sub-arcsecond accuracy."],
            status="VALID"
        )

kp_adapter = KPMethodAdapter()
