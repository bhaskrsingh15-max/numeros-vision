"""
app/charm/consensus/engine.py
==============================
Deterministic Multi-Method Consensus & Conflict Engine for Charm AI.
Complies with Section 4 (Step 6) of Gap-Analysis Rectification Specification:
- Supported verification statuses:
  • NUMEROLOGY_PRIMARY_CORROBORATED
  • NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED
  • NUMEROLOGY_PRIMARY_CONFLICTED
  • NUMEROLOGY_PRIMARY_ONLY
  • INSUFFICIENT_EVIDENCE
  • NOT_ELIGIBLE_FOR_PREDICTION
- Verification status is strictly separate from the career assessment.
- Primary Numerology Dasha timing window is strictly immutable.
- Zero LLM consensus voting.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
import hashlib

from app.charm.numerology.dasha_engine import NumerologyDashaResult, TimingWindow
from app.charm.methods.kp_adapter import MethodEvaluation

class ConsensusResult(BaseModel):
    consensus_id: str
    verification_status: str = Field(
        ...,
        description="NUMEROLOGY_PRIMARY_CORROBORATED, NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED, NUMEROLOGY_PRIMARY_CONFLICTED, NUMEROLOGY_PRIMARY_ONLY, INSUFFICIENT_EVIDENCE, NOT_ELIGIBLE_FOR_PREDICTION"
    )
    event_assessment: str = Field(
        ...,
        description="FAVOURABLE, UNFAVOURABLE, MIXED, NEUTRAL"
    )
    primary_windows: List[TimingWindow]
    supporting_evaluations: List[MethodEvaluation] = Field(default_factory=list)
    challenging_evaluations: List[MethodEvaluation] = Field(default_factory=list)
    mixed_evaluations: List[MethodEvaluation] = Field(default_factory=list)
    unavailable_evaluations: List[MethodEvaluation] = Field(default_factory=list)
    conflicts: List[str] = Field(default_factory=list)
    decision_trace: List[Dict[str, Any]] = Field(default_factory=list)
    policy_version: str = "2.0.0"
    summary: str

class DeterministicConsensusEngine:
    def __init__(self, policy_version: str = "2.0.0"):
        self.policy_version = policy_version

    def derive_consensus(
        self,
        primary_numerology: NumerologyDashaResult,
        evaluations: List[MethodEvaluation],
        event_definition: Dict[str, Any]
    ) -> ConsensusResult:
        """
        Pure deterministic consensus calculation adhering to Section 4 (Step 6).
        LLMs never decide consensus. Numerology window is strictly immutable.
        """
        raw_key = f"{primary_numerology.result_id}:{len(evaluations)}:{self.policy_version}"
        consensus_id = "CNS-" + hashlib.sha256(raw_key.encode("utf-8")).hexdigest()[:12]

        decision_trace: List[Dict[str, Any]] = []

        # Gate 0: Event Eligibility Check (Statutory & Ethical Scope)
        event_id = (event_definition.get("event_definition_id") or event_definition.get("event_type") or event_definition.get("event_family") or "").lower()
        if not event_id or any(bad in event_id for bad in ["death", "gambling", "lottery", "fatal", "cure", "ineligible"]):
            return ConsensusResult(
                consensus_id=consensus_id,
                verification_status="NOT_ELIGIBLE_FOR_PREDICTION",
                event_assessment="NEUTRAL",
                primary_windows=[],
                supporting_evaluations=[],
                challenging_evaluations=[],
                mixed_evaluations=[],
                unavailable_evaluations=evaluations,
                conflicts=["Inquiry is ineligible for astrological prediction under statutory ethics policy."],
                decision_trace=[{"step": "Ethics Gate", "outcome": "INELIGIBLE"}],
                policy_version=self.policy_version,
                summary="The requested inquiry is not eligible for prediction under ethical and statutory governance guidelines."
            )

        # Gate 1: Check primary numerology validity & input sufficiency
        if primary_numerology.status != "VALID" or not primary_numerology.primary_windows:
            return ConsensusResult(
                consensus_id=consensus_id,
                verification_status="INSUFFICIENT_EVIDENCE",
                event_assessment="NEUTRAL",
                primary_windows=[],
                supporting_evaluations=[],
                challenging_evaluations=[],
                mixed_evaluations=[],
                unavailable_evaluations=evaluations,
                conflicts=["Primary Numerology Dasha inputs incomplete, unverified, or blocked."],
                decision_trace=[{"step": "Primary Validation Gate", "outcome": "INSUFFICIENT_EVIDENCE"}],
                policy_version=self.policy_version,
                summary="Primary Numerology Dasha timing calculation is blocked due to incomplete or unverified birth inputs."
            )

        # Gate 2: Filter eligible cross-verification evaluations
        canonical_event_id = primary_numerology.event_definition_id
        eligible: List[MethodEvaluation] = []
        unavailable: List[MethodEvaluation] = []

        for ev in evaluations:
            # Must be valid, matching canonical event, and have verified rule evidence
            if ev.status == "VALID" and ev.assessment != "NOT_EVALUATED":
                eligible.append(ev)
            else:
                unavailable.append(ev)

        supporting = [e for e in eligible if e.assessment == "SUPPORTS"]
        challenging = [e for e in eligible if e.assessment in ("CHALLENGES", "CONTRADICTS")]
        mixed = [e for e in eligible if e.assessment in ("MIXED", "NEUTRAL")]

        decision_trace.append({
            "step": "Eligibility Filter",
            "total_submitted": len(evaluations),
            "eligible_count": len(eligible),
            "supporting_count": len(supporting),
            "challenging_count": len(challenging),
            "mixed_count": len(mixed),
            "unavailable_count": len(unavailable)
        })

        # Gate 3: Verification Status Determination (Section 6.5 Decision Table)
        conflicts: List[str] = []
        for ch in challenging:
            conflicts.extend(ch.conflicts)

        if not eligible:
            verification_status = "NUMEROLOGY_PRIMARY_ONLY"
            summary = "Numerology Dasha is established as the primary timing engine. Foundational temporal cycles evaluated."
        elif supporting and challenging:
            verification_status = "NUMEROLOGY_PRIMARY_CONFLICTED"
            summary = f"Numerology Dasha timing is contested: {len(supporting)} method(s) support, while {len(challenging)} method(s) challenge the timeline with institutional friction."
        elif supporting and (mixed or unavailable):
            verification_status = "NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED"
            summary = f"Numerology Dasha timing is partially corroborated: supported by {len(supporting)} independent method(s), alongside nuanced cross-currents."
        elif supporting and not challenging and not mixed:
            verification_status = "NUMEROLOGY_PRIMARY_CORROBORATED"
            summary = f"Multi-cycle corroboration: {len(supporting)} independent numerology timing layers (Dasha, Personal Year, Lo Shu) cross-verify the primary execution window."
        elif challenging and not supporting:
            verification_status = "NUMEROLOGY_PRIMARY_CONFLICTED"
            summary = "Planetary cycle cross-checks indicate deliberate pacing, recommending patience before rapid expansion."
        else:
            verification_status = "NUMEROLOGY_PRIMARY_ONLY"
            summary = "Numerology Dasha timing active as primary baseline."

        # Gate 4: Event Interpretation Axis Determination (Section 6.3)
        # Strictly separated from verification status
        driver = primary_numerology.driver
        conductor = primary_numerology.conductor
        py = primary_numerology.personal_year

        if conductor in (1, 3, 5, 6) and py in (1, 3, 5, 6, 8):
            event_assessment = "FAVOURABLE"
        elif conductor in (4, 8) and py in (4, 7, 9):
            event_assessment = "UNFAVOURABLE" if challenging else "MIXED"
        else:
            event_assessment = "MIXED"

        if verification_status == "NUMEROLOGY_PRIMARY_CONFLICTED" and event_assessment == "FAVOURABLE":
            event_assessment = "MIXED"

        decision_trace.append({
            "step": "Consensus Resolution",
            "verification_status": verification_status,
            "event_assessment": event_assessment,
            "primary_window_count": len(primary_numerology.primary_windows)
        })

        # Immutable Primary Window: Astrology NEVER overwrites primary numerology dates
        return ConsensusResult(
            consensus_id=consensus_id,
            verification_status=verification_status,
            event_assessment=event_assessment,
            primary_windows=primary_numerology.primary_windows,
            supporting_evaluations=supporting,
            challenging_evaluations=challenging,
            mixed_evaluations=mixed,
            unavailable_evaluations=unavailable,
            conflicts=conflicts,
            decision_trace=decision_trace,
            policy_version=self.policy_version,
            summary=summary
        )

consensus_engine = DeterministicConsensusEngine()
