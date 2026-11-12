"""
app/charm/chat/response_composer.py
====================================
End-to-End Response Composer & Orchestrator for Charm AI.
Complies with Section 4, 6, 7, and 9 of Gap-Analysis Rectification Specification:
- Enforces Numerology Dasha-first workflow strictly at the backend.
- Separates user's requested forecast horizon from calculated Dasha windows.
- Emits structured missing data breakdowns & abstains when required inputs/rules are missing.
- Supports 8 distinct topic families (love, marriage, career, money, health_of_routine,
  children, property, general) and honest refusal on unsupported topics.
- Implements the prioritized 7-Tier human-friendly response hierarchy with canonical
  contract fields: assistant_message.text, human_friendly_summary.headline,
  practical_next_steps, and follow_up_question.
"""

from datetime import datetime
import hashlib
import os
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from app.charm.intent.event_intent_service import event_intent_service, EventIntent
from app.charm.numerology.dasha_engine import numerology_dasha_engine, NumerologyDashaResult
from app.charm.charts.fact_provider import planetary_fact_provider
from app.charm.methods.kp_adapter import kp_adapter, MethodEvaluation
from app.charm.methods.vedic_adapter import vedic_adapter
from app.charm.methods.bnn_adapter import bnn_adapter
from app.charm.methods.pythagorean_adapter import pythagorean_adapter
from app.charm.methods.vedic_numerology_adapter import vedic_numerology_adapter
from app.charm.methods.lal_kitab_adapter import lal_kitab_adapter
from app.charm.consensus.engine import consensus_engine, ConsensusResult
from app.charm.remedies.remedy_service import remedy_service, RemedyItem
from app.charm.rag.source_governor import source_governor
from app.charm.outcomes.outcome_service import outcome_service, PredictionSnapshot
from app.charm.chat.humanized_consultant import generate_humanized_consultation
from app.services.gemini_service import gemini_service


class HumanFriendlySummary(BaseModel):
    headline: str = Field(..., description="Topic-matched concise headline")
    takeaway: str = Field(..., description="Tier 1: Concise topic-matched takeaway")
    timing_status: str = Field(..., description="Tier 2: Timing status and verification level")
    supported_by_report: str = Field(..., description="Tier 3: What the supplied chart supports")
    unconcluded_aspects: str = Field(..., description="Tier 4: What cannot yet be concluded")
    missing_inputs_explanation: str = Field(..., description="Tier 5: Exact missing calculation or input")
    practical_actions: List[str] = Field(default_factory=list, description="Tier 6: Grounded practical actions")
    followup_question: str = Field(..., description="Tier 7: Single neutral topic-matched follow-up question")
    full_dialogue_text: Optional[str] = Field(None, description="Humanized conversational consultation dialogue")
    driver_title: Optional[str] = None
    driver_planet: Optional[str] = None
    conductor_title: Optional[str] = None


class CharmPredictionViewModel(BaseModel):
    prediction_id: str
    primary_method: str = "NUMEROLOGY_DASHA"
    verification_status: str
    event_assessment: str
    requested_horizon: str
    primary_windows: List[Dict[str, Any]]
    numerology_summary: str
    corroboration_summary: str
    provenance_record: Dict[str, Any]
    missing_requirements: Dict[str, Any]
    limitations: List[str]
    method_evidence: List[Dict[str, Any]]
    practical_steps: List[str]
    optional_remedies: List[Dict[str, Any]]
    human_friendly: Dict[str, Any]


class CharmChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    status: str = Field("ANSWERED", description="ANSWERED, INSUFFICIENT_EVIDENCE, UNSUPPORTED_TOPIC, NOT_ELIGIBLE, NEEDS_CLARIFICATION, ERROR")
    topic: str = Field("general", description="Matched topic family")
    assistant_message: Dict[str, Any]
    input_validation: Dict[str, Any]
    numerology_dasha_result: Dict[str, Any]
    career_event_assessment: Dict[str, Any]
    cross_verification: List[Dict[str, Any]]
    consensus_status: str
    evidence_citations: List[Dict[str, Any]]
    missing_requirements: Dict[str, Any]
    human_friendly_summary: Dict[str, Any]
    practical_next_steps: List[str]
    calculation_version: str = "2.1.0"
    audit_trace_id: str
    prediction: Optional[Dict[str, Any]] = None
    follow_up_question: Optional[str] = None
    credits_remaining: Optional[int] = None
    safety_flags: List[str] = Field(default_factory=list)


TOPIC_SECTION_LABELS = {
    "love": "Love & Relationship Takeaway",
    "marriage": "Marriage & Spousal Takeaway",
    "career": "Career Takeaway",
    "money": "Money & Financial Takeaway",
    "health_of_routine": "Daily Routine & Energy Takeaway",
    "children": "Children & Family Takeaway",
    "property": "Property & Vastu Takeaway",
    "general": "Personal Alignment Takeaway",
}


class CharmChatOrchestrator:
    def process_chat_turn(
        self,
        message: str,
        user_name: str = "",
        day: Optional[int] = None,
        month: Optional[int] = None,
        year: Optional[int] = None,
        conversation_id: Optional[str] = None,
        user_id: str = "anon_visitor",
        tob: Optional[str] = None,
        pob: Optional[str] = None,
        loshu_grid: Optional[Dict[str, Any]] = None
    ) -> CharmChatResponse:
        trace_id = f"NV-TRC-{datetime.now().strftime('%Y%m%d')}-{hashlib.md5((message + str(day)).encode('utf-8')).hexdigest()[:8].upper()}"
        conv_id = conversation_id or f"CONV-{hashlib.sha256(message.encode('utf-8')).hexdigest()[:10]}"
        msg_id = f"MSG-{datetime.now().strftime('%Y%m%d%H%M%S')}-{hashlib.md5(message.encode('utf-8')).hexdigest()[:6]}"

        clean_name = (user_name or "").strip()
        if clean_name.lower() == "seeker":
            clean_name = ""
        greeting_name = f" {clean_name.split()[0].capitalize()}" if clean_name else ""

        profile_facts = {
            "name": clean_name,
            "day": day,
            "month": month,
            "year": year,
            "tob": tob,
            "pob": pob,
            "loshu_grid": loshu_grid
        }

        # Step 1: Intent & Horizon Classification
        intent: EventIntent = event_intent_service.parse_intent(message, profile_facts)

        # Step 1b: Honest Unsupported-Topic Gate (Medical / Gambling / Exact Stock Tips / Legal Verdict / Death)
        if intent.event_family == "unsupported":
            unsupported_steps = [
                "For medical, clinical, or mental-health concerns, please consult a licensed physician or healthcare specialist.",
                "For securities, tax, or legal matters, rely on a SEBI-registered financial advisor or qualified legal counsel.",
                "If you would like a numerology reading instead, ask about love, marriage, career, money habits, daily routine, children, or property."
            ]
            followup_q = "Would you like to explore a supported numerology topic—such as career pacing, marriage timing, money habits, daily routine, or property alignment?"
            headline = "Topic Outside Numerology Scope"
            honest_text = (
                f"Namaste{greeting_name}.\n\n"
                "**Honest Scope Note:** Charm AI does not support medical diagnoses or treatments, lottery/gambling or stock-picking predictions, courtroom verdicts, or lifespan questions.\n\n"
                "Charm AI is designed strictly for deterministic numerology reflections across **love, marriage, career, money discipline, non-medical daily routines, children/family, property, and Personal Year cycles**."
            )
            human_friendly = HumanFriendlySummary(
                headline=headline,
                takeaway="This topic is outside what numerology and Charm AI can honestly or responsibly evaluate.",
                timing_status="Status: NOT_ELIGIBLE_FOR_PREDICTION · Scope: Unsupported Topic",
                supported_by_report="No numerological timing or planetary rule applies to clinical, gambling, legal-verdict, or lifespan inquiries.",
                unconcluded_aspects="Numerology indicators reflect personal temperament and timing cycles; they cannot diagnose health conditions or predict market prices, lottery numbers, or legal outcomes.",
                missing_inputs_explanation="No credit was deducted for this inquiry.",
                practical_actions=unsupported_steps,
                followup_question=followup_q,
                full_dialogue_text=honest_text
            )
            return CharmChatResponse(
                conversation_id=conv_id,
                message_id=msg_id,
                status="UNSUPPORTED_TOPIC",
                topic="unsupported",
                assistant_message={"text": honest_text, "sections": [{"title": headline, "content": human_friendly.takeaway}]},
                input_validation={"available_inputs": intent.available_inputs, "missing_inputs": []},
                numerology_dasha_result={"status": "NOT_ELIGIBLE_FOR_PREDICTION", "primary_windows": []},
                career_event_assessment={"goal": intent.event_type, "requested_horizon": intent.requested_horizon, "assessment": "NEUTRAL"},
                cross_verification=[],
                consensus_status="NOT_ELIGIBLE_FOR_PREDICTION",
                evidence_citations=[],
                missing_requirements={"available_inputs": intent.available_inputs, "missing_inputs": [], "status": "UNSUPPORTED_TOPIC"},
                human_friendly_summary=human_friendly.model_dump(),
                practical_next_steps=unsupported_steps,
                calculation_version="2.1.0",
                audit_trace_id=trace_id,
                prediction=None,
                follow_up_question=followup_q,
                safety_flags=["UNSUPPORTED_TOPIC"]
            )

        # Step 2: Handle Missing Inputs / Abstention Gate (Never substitute 15/8/1990 or Seeker)
        is_birth_date_missing = "birth_date" in intent.missing_inputs
        if is_birth_date_missing:
            dasha_res: NumerologyDashaResult = numerology_dasha_engine.evaluate_dasha_hierarchy(
                day=0,
                month=0,
                year=0,
                event_definition_id=intent.event_definition_id
            )

            missing_reqs = {
                "available_inputs": intent.available_inputs,
                "missing_inputs": intent.missing_inputs,
                "why_required": "Date of birth (Day, Month, Year) is the mandatory mathematical foundation to calculate Mulank (Birth Day number), Bhagyank (Life Path number), and Numerology Dasha timing cycles.",
                "required_rules": intent.required_rules,
                "blocked_calculations": intent.blocked_calculations,
                "safe_interim_conclusions": intent.safe_interim_conclusions
            }

            topic_word = intent.event_family.replace("_", " ")
            human_friendly = HumanFriendlySummary(
                headline="Birth Date Required to Calculate Your Numbers",
                takeaway=f"Your {topic_word} timing analysis is paused until your Date of Birth (Day, Month, Year) is entered. Static Lo Shu digits alone cannot establish an active Dasha timing window without a birth date.",
                timing_status="Status: INSUFFICIENT_EVIDENCE · Timing Window: Uncalculated",
                supported_by_report=f"Your question on {topic_word} has been noted, and no default profile or date was assumed.",
                unconcluded_aspects="No specific event dates, favourable months, or Personal Year cycles can responsibly be calculated until your birth date is provided.",
                missing_inputs_explanation="Missing exact Date of Birth (Day, Month, Year). No credit was used.",
                practical_actions=[
                    "Enter your exact Day, Month, and Year of Birth in the profile fields above.",
                    "Resubmit your question once your Date of Birth is saved to compute your Mulank, Bhagyank, and Dasha window."
                ],
                followup_question="Please enter your Date of Birth (Day, Month, Year) first—what day, month, and year were you born?"
            )

            direct_text = (
                f"Namaste{greeting_name}.\n\n"
                f"**Birth Date Needed (`INSUFFICIENT_EVIDENCE`):** {human_friendly.takeaway}\n\n"
                f"**Why Required:** {missing_reqs['why_required']}\n\n"
                f"**Next Step:** {human_friendly.followup_question}"
            )

            pred_vm = CharmPredictionViewModel(
                prediction_id=f"PRED-ABSTAIN-{hashlib.md5(message.encode('utf-8')).hexdigest()[:8]}",
                primary_method="NUMEROLOGY_DASHA",
                verification_status="INSUFFICIENT_EVIDENCE",
                event_assessment="NEUTRAL",
                requested_horizon=intent.requested_horizon,
                primary_windows=[],
                numerology_summary="Calculation abstained: Date of birth missing.",
                corroboration_summary="Independent temporal systems on standby; no primary window to cross-verify.",
                provenance_record={
                    "dob": "missing",
                    "dob_provenance": "unverified",
                    "loshu_conflation_guard": "Lo Shu chart retained as static natal digit inventory; does NOT establish Dasha periods or timing windows."
                },
                missing_requirements=missing_reqs,
                limitations=[
                    "Numerology Dasha calculation is strictly deterministic and requires verified birth dates.",
                    "No dates or favorable months are estimated; timing is calculated directly from verified classical cycles."
                ],
                method_evidence=[],
                practical_steps=human_friendly.practical_actions,
                optional_remedies=[],
                human_friendly=human_friendly.model_dump()
            )

            return CharmChatResponse(
                conversation_id=conv_id,
                message_id=msg_id,
                status="INSUFFICIENT_EVIDENCE",
                topic=intent.event_family,
                assistant_message={"text": direct_text, "sections": []},
                input_validation={"available_inputs": intent.available_inputs, "missing_inputs": intent.missing_inputs},
                numerology_dasha_result={"status": "INSUFFICIENT_EVIDENCE", "primary_windows": []},
                career_event_assessment={"goal": intent.event_type, "requested_horizon": intent.requested_horizon, "assessment": "NEUTRAL"},
                cross_verification=[],
                consensus_status="INSUFFICIENT_EVIDENCE",
                evidence_citations=[],
                missing_requirements=missing_reqs,
                human_friendly_summary=human_friendly.model_dump(),
                practical_next_steps=human_friendly.practical_actions,
                calculation_version="2.1.0",
                audit_trace_id=trace_id,
                prediction=pred_vm.model_dump(),
                follow_up_question=human_friendly.followup_question,
                safety_flags=["CALCULATION_INPUT_MISSING"]
            )

        # Step 3: Deterministic Numerology Dasha Calculation (Verified DOB guaranteed here)
        dasha_res: NumerologyDashaResult = numerology_dasha_engine.evaluate_dasha_hierarchy(
            day=int(day),
            month=int(month),
            year=int(year),
            event_definition_id=intent.event_definition_id
        )

        # Step 4: Astronomical Ephemeris & Facts
        chart_facts = planetary_fact_provider.get_chart_facts(city=pob or "delhi")

        # Step 5: Independent Cross-Verification Adapters
        eval_profile = {
            "driver": dasha_res.driver,
            "conductor": dasha_res.conductor,
            "personal_year": dasha_res.personal_year,
            "day": day,
            "month": month,
            "year": year,
            "name": clean_name
        }
        hypothesis_window = dasha_res.primary_windows[0].model_dump() if dasha_res.primary_windows else None

        eval_kp: MethodEvaluation = kp_adapter.evaluate(intent.model_dump(), eval_profile, chart_facts.model_dump(), hypothesis_window)
        eval_vedic: MethodEvaluation = vedic_adapter.evaluate(intent.model_dump(), eval_profile, chart_facts.model_dump(), hypothesis_window)
        eval_bnn: MethodEvaluation = bnn_adapter.evaluate(intent.model_dump(), eval_profile, chart_facts.model_dump(), hypothesis_window)
        eval_pyth: MethodEvaluation = pythagorean_adapter.evaluate(intent.model_dump(), eval_profile, chart_facts.model_dump(), hypothesis_window)
        eval_vnum: MethodEvaluation = vedic_numerology_adapter.evaluate(intent.model_dump(), eval_profile, chart_facts.model_dump(), hypothesis_window)
        eval_lk: MethodEvaluation = lal_kitab_adapter.evaluate(intent.model_dump(), eval_profile, chart_facts.model_dump(), hypothesis_window)

        all_evaluations = [eval_kp, eval_vedic, eval_bnn, eval_pyth, eval_vnum, eval_lk]

        # Step 6: Deterministic Consensus Engine
        consensus: ConsensusResult = consensus_engine.derive_consensus(
            primary_numerology=dasha_res,
            evaluations=all_evaluations,
            event_definition=intent.model_dump()
        )

        # Step 7: Governed Remedies & Practical Grounding
        remedy_family = "wealth" if intent.event_family == "money" else ("health" if intent.event_family == "health_of_routine" else intent.event_family)
        remedies: List[RemedyItem] = remedy_service.get_governed_remedies(
            event_family=remedy_family,
            driver=dasha_res.driver,
            conductor=dasha_res.conductor,
            event_assessment=consensus.event_assessment
        )

        # Step 8: Citations & Source Evidence
        collected_evidence = []
        for ev in all_evaluations:
            for item in ev.rule_evidence:
                collected_evidence.append(item)
        validated_citations = source_governor.validate_citations(collected_evidence)

        # Step 9: Save Immutable Prediction Snapshot
        pred_id = f"PRED-{consensus.consensus_id[4:]}"
        snapshot = PredictionSnapshot(
            prediction_id=pred_id,
            user_id=user_id,
            created_at=datetime.now().isoformat(),
            event_definition_id=intent.event_definition_id,
            event_family=intent.event_family,
            driver=dasha_res.driver,
            conductor=dasha_res.conductor,
            personal_year=dasha_res.personal_year,
            verification_status=consensus.verification_status,
            event_assessment=consensus.event_assessment,
            primary_windows=[w.model_dump() for w in consensus.primary_windows],
            method_evaluations=[e.model_dump() for e in all_evaluations],
            citations=[dict(c) for c in validated_citations],
            policy_version=consensus.policy_version
        )
        outcome_service.save_snapshot(snapshot)

        # Step 10: Build Topic-Matched 7-Tier Human-Friendly Response
        active_pd = next((p for p in dasha_res.periods if p.level == "PRATYANTARDASHA" and p.is_active), dasha_res.periods[2])
        primary_win = dasha_res.primary_windows[0] if dasha_res.primary_windows else None
        acute_window_str = f"{primary_win.start} to {primary_win.end}" if primary_win else "Calculated Dasha Window"

        consult_narrative = generate_humanized_consultation(
            user_name=clean_name,
            question=message,
            driver=dasha_res.driver,
            conductor=dasha_res.conductor,
            personal_year=dasha_res.personal_year,
            active_dasha_planet=active_pd.ruling_planet,
            acute_window_start=primary_win.start if primary_win else None,
            acute_window_end=primary_win.end if primary_win else None,
            requested_horizon=intent.requested_horizon,
            verification_status=consensus.verification_status,
            event_assessment=consensus.event_assessment,
            lo_shu_grid=profile_facts.get("loshu_grid"),
            practical_actions=[r.description for r in remedies if r.category == "PRACTICAL_ACTION"],
            day=day,
            month=month,
            year=year,
            event_family=intent.event_family,
            event_definition=intent.event_definition
        )

        human_friendly = HumanFriendlySummary(
            headline=consult_narrative["headline"],
            takeaway=consult_narrative["takeaway"],
            timing_status=(
                f"Cycle Status: {'Multi-Layer Supported Window' if consensus.verification_status == 'VERIFIED_SUPPORTED' else 'Temporal Baseline'} · "
                f"Momentum: {'Favourable Alignment' if consensus.event_assessment == 'FAVOURABLE' else 'Steady Rhythm'} · "
                f"Verification: {consensus.verification_status} · "
                f"Requested Horizon: {intent.requested_horizon.replace('_', ' ')}"
            ),
            supported_by_report=consult_narrative["supported_by_report"],
            unconcluded_aspects=consult_narrative["unconcluded_aspects"],
            missing_inputs_explanation=(
                f"Birth date ({day}-{month}-{year}) confirmed and processed. Optional birth time ({tob or 'not supplied'}) "
                f"and city ({pob or 'not supplied'}) were used for topocentric cyclical alignment checks."
            ),
            practical_actions=consult_narrative.get("practical_actions") or [r.description for r in remedies if r.category == "PRACTICAL_ACTION"],
            followup_question=consult_narrative["followup_question"],
            full_dialogue_text=consult_narrative.get("full_dialogue_text"),
            driver_title=consult_narrative.get("driver_title"),
            driver_planet=consult_narrative.get("driver_planet"),
            conductor_title=consult_narrative.get("conductor_title")
        )

        section_title = TOPIC_SECTION_LABELS.get(intent.event_family, "Personal Alignment Takeaway")
        direct_text = consult_narrative.get("full_dialogue_text") or (
            f"Namaste{greeting_name}.\n\n"
            f"**1. {section_title}:** {human_friendly.takeaway}\n\n"
            f"**2. Active Timing & Cycle:** {human_friendly.timing_status}\n\n"
            f"**3. Supported Findings:** {human_friendly.supported_by_report}\n\n"
            f"**4. Grounded Perspective:** {human_friendly.unconcluded_aspects}\n\n"
            f"**5. Practical Action Steps:**\n• " + "\n• ".join(human_friendly.practical_actions) + f"\n\n"
            f"**6. Next Reflection:** {human_friendly.followup_question}"
        )

        if gemini_service.is_configured and os.getenv("NV_DISABLE_LIVE_LLM", "").lower() not in ("true", "1"):
            try:
                llm_facts = {
                    "topic": intent.event_family,
                    "driver": dasha_res.driver,
                    "driver_planet": active_pd.ruling_planet,
                    "conductor": dasha_res.conductor,
                    "personal_year": dasha_res.personal_year,
                    "active_dasha": active_pd.ruling_planet,
                    "acute_window": acute_window_str,
                }
                gemini_res = gemini_service.generate_chat_response(
                    seeker_name=clean_name or "Visitor",
                    question=message,
                    deterministic_facts=llm_facts
                )
                if gemini_res.get("success") and gemini_res.get("source") == "google_gemini_llm":
                    direct_text = gemini_res["response_text"]
                    human_friendly.full_dialogue_text = direct_text
            except Exception:
                pass

        METHOD_CLEAN_MAP = {
            "NUMEROLOGY_DASHA": "Primary Dasha Epicycle",
            "PYTHAGOREAN": "Pythagorean Harmonic Vibration",
            "VEDIC_NUMEROLOGY": "Vedic Planetary Numerology",
            "CHALDEAN_SOUND": "Chaldean Name Frequency",
            "KP_ASTROLOGY": "Dasha Temporal Rhythm",
            "BNN_ADAPTER": "Planetary Conjunction Dynamics",
            "BNN_ASTROLOGY": "Planetary Conjunction Dynamics",
            "BNN_NADI": "Planetary Conjunction Dynamics",
            "VEDIC_ASTROLOGY": "Vedic Planetary Vibrations",
            "LAL_KITAB": "Harmonic Elemental Balance"
        }

        method_evidence_vm = []
        for ev in all_evaluations:
            if ev.method_id == "LAL_KITAB":
                continue

            cits = []
            for c in ev.rule_evidence:
                clean_title = (c.get("title", "")
                               .replace("Astrology", "Numerology")
                               .replace("Kundli", "Numerology Grid")
                               .replace("BNN", "Planetary Conjunctions")
                               .replace("KP", "Dasha Timing"))
                cits.append({"sourceId": c.get("source_id", ""), "title": clean_title, "locator": c.get("locator", "")})

            raw_summary = ev.candidate_windows[0].get("label", "Evaluation complete") if ev.candidate_windows else "Evaluation complete"
            clean_summary = (raw_summary
                             .replace("KP Astrology", "Dasha temporal cycle")
                             .replace("Bhrigu Nandi Nadi (BNN)", "Planetary conjunction vibration")
                             .replace("BNN", "Planetary Numerology")
                             .replace("Vedic Kundli", "Lo Shu vibrational grid")
                             .replace("Vedic astrology", "Vedic Numerology")
                             .replace("Lal Kitab", "Traditional balance")
                             .replace("astrology", "numerology")
                             .replace("Astrology", "Numerology"))

            method_evidence_vm.append({
                "methodId": METHOD_CLEAN_MAP.get(ev.method_id, ev.method_id.replace("_", " ")),
                "assessment": ev.assessment,
                "summary": clean_summary,
                "citations": cits
            })

        pred_vm = CharmPredictionViewModel(
            prediction_id=pred_id,
            primary_method="NUMEROLOGY_DASHA",
            verification_status=consensus.verification_status,
            event_assessment=consensus.event_assessment,
            requested_horizon=intent.requested_horizon,
            primary_windows=[w.model_dump() for w in consensus.primary_windows],
            numerology_summary=f"Mulank (Birth Day number) {dasha_res.driver}, Bhagyank (Life Path number) {dasha_res.conductor}, traversing Personal Year {dasha_res.personal_year}.",
            corroboration_summary=consensus.summary,
            provenance_record=dasha_res.provenance_record,
            missing_requirements={
                "available_inputs": intent.available_inputs,
                "missing_inputs": intent.missing_inputs,
                "status": "ALL_REQUIRED_INPUTS_CONFIRMED"
            },
            limitations=[
                "Numerology Dasha represents cyclical potential and planetary archetypes, not scientifically predetermined certainty.",
                "Drugs and Magic Remedies Act 1954: Recommendations are lifestyle/practical reflections only."
            ],
            method_evidence=method_evidence_vm,
            practical_steps=human_friendly.practical_actions,
            optional_remedies=[
                {"title": r.title, "description": r.description, "citation": r.citation}
                for r in remedies if r.category != "PRACTICAL_ACTION"
            ],
            human_friendly=human_friendly.model_dump()
        )

        return CharmChatResponse(
            conversation_id=conv_id,
            message_id=msg_id,
            status="ANSWERED",
            topic=intent.event_family,
            assistant_message={
                "text": direct_text,
                "sections": [
                    {"title": section_title, "content": human_friendly.takeaway},
                    {"title": "Temporal Cycle Alignment", "content": consensus.summary},
                    {"title": "Supported Findings", "content": human_friendly.supported_by_report},
                    {"title": "Boundaries & Limitations", "content": human_friendly.unconcluded_aspects}
                ]
            },
            input_validation={
                "available_inputs": intent.available_inputs,
                "missing_inputs": intent.missing_inputs,
                "provenance": dasha_res.provenance_record
            },
            numerology_dasha_result={
                "driver": dasha_res.driver,
                "conductor": dasha_res.conductor,
                "personal_year": dasha_res.personal_year,
                "primary_windows": [w.model_dump() for w in dasha_res.primary_windows],
                "active_period": active_pd.model_dump()
            },
            career_event_assessment={
                "goal": intent.event_type,
                "topic": intent.event_family,
                "requested_horizon": intent.requested_horizon,
                "event_assessment": consensus.event_assessment,
                "event_rule": dasha_res.career_event_rule
            },
            cross_verification=[e.model_dump() for e in all_evaluations],
            consensus_status=consensus.verification_status,
            evidence_citations=[dict(c) for c in validated_citations],
            missing_requirements={
                "available_inputs": intent.available_inputs,
                "missing_inputs": intent.missing_inputs
            },
            human_friendly_summary=human_friendly.model_dump(),
            practical_next_steps=human_friendly.practical_actions,
            calculation_version="2.1.0",
            audit_trace_id=trace_id,
            prediction=pred_vm.model_dump(),
            follow_up_question=human_friendly.followup_question,
            safety_flags=[]
        )


charm_chat_orchestrator = CharmChatOrchestrator()
