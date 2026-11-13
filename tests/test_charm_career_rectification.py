"""
tests/test_charm_career_rectification.py
=========================================
Automated Test Suite for Charm AI Gap-Analysis Rectification.
Verifies all 10 acceptance criteria defined in GAP_ANALYSIS_RECTIFICATION.md:

1. Intent & Horizon Classification:
   - Disambiguates career goals (new job/senior role, promotion, career change, business venture).
   - Separates user-requested forecast horizon (6_months, etc.) from calculated Dasha windows.
2. Missing Data Abstention Standard:
   - Emits INSUFFICIENT_EVIDENCE when birth date is missing.
   - Abstains from date and month predictions.
3. Lo Shu Conflation Prevention:
   - Lo Shu digit presence without birth date does not generate a Dasha window.
   - Provenance records loshu_conflation_guard.
4. Deterministic Consensus Status Coverage:
   - Strictly supports all 6 canonical consensus statuses.
5. Primary Window Immutability:
   - Astrological methods never alter Dasha start/end dates.
6. 7-Tier Human-Friendly Response Hierarchy:
   - Structured takeaway, timing status, supported findings, unconcluded aspects,
     missing input breakdown, practical actions, and single follow-up question.
7. API /api/charm/chat with complete inputs.
8. API /api/charm/chat with missing birth date.
9. Integration via /api/v1/readings/ask (freemium & paid flow).
10. Brand and Design System Compliance (zero #000000, correct brand names).
"""

import os
import unittest
from datetime import date
from fastapi.testclient import TestClient

from app.main import app
from app.charm.intent.event_intent_service import event_intent_service, EventIntent
from app.charm.numerology.dasha_engine import numerology_dasha_engine, NumerologyDashaResult
from app.charm.consensus.engine import consensus_engine, ConsensusResult
from app.charm.methods.kp_adapter import MethodEvaluation
from app.charm.chat.response_composer import charm_chat_orchestrator, CharmChatResponse

class TestCharmCareerRectification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        os.environ.setdefault("CHARM_SERVICE_SECRET", "nv_unit_test_charm_secret")
        cls.charm_headers = {"X-NV-Charm-Secret": os.environ["CHARM_SERVICE_SECRET"]}
        cls.client = TestClient(app)

    # ─────────────────────────────────────────────────────────────────────────
    # 1. INTENT & HORIZON CLASSIFICATION TESTS
    # ─────────────────────────────────────────────────────────────────────────
    def test_intent_career_goal_disambiguation(self):
        """Verify intent parser distinguishes specific career goals."""
        profile = {"day": 15, "month": 8, "year": 1990}

        # Case A: Senior role / new job
        intent_job = event_intent_service.parse_intent(
            "I want a new senior executive job at a tech firm in the next 6 months",
            profile
        )
        self.assertEqual(intent_job.event_type, "new_job_or_senior_role")
        self.assertEqual(intent_job.requested_horizon, "6_months")
        self.assertEqual(intent_job.event_family.lower(), "career")
        self.assertIn("birth_date", intent_job.available_inputs)

        # Case B: Promotion
        intent_promo = event_intent_service.parse_intent(
            "Will I get promoted to Director this year?",
            profile
        )
        self.assertEqual(intent_promo.event_type, "promotion")
        self.assertEqual(intent_promo.requested_horizon, "12_months")

        # Case C: Career Change
        intent_change = event_intent_service.parse_intent(
            "Should I switch fields and change career in the next 3 months?",
            profile
        )
        self.assertEqual(intent_change.event_type, "career_change")
        self.assertEqual(intent_change.requested_horizon, "3_months")

        # Case D: Business Venture
        intent_biz = event_intent_service.parse_intent(
            "I am launching a new startup business venture over the next 24 months",
            profile
        )
        self.assertEqual(intent_biz.event_type, "business_venture")
        self.assertEqual(intent_biz.requested_horizon, "24_months")

    def test_requested_horizon_separation_from_dasha(self):
        """Verify user forecast horizon is tracked independently of Dasha window."""
        profile = {"day": 15, "month": 8, "year": 1990}
        intent = event_intent_service.parse_intent(
            "Looking for a job offer in the next 6 months",
            profile
        )
        # Requested horizon is '6_months'
        self.assertEqual(intent.requested_horizon, "6_months")

        # Now compute Dasha
        dasha = numerology_dasha_engine.evaluate_dasha_hierarchy(
            day=15, month=8, year=1990, event_definition_id="career_growth"
        )
        # Primary window is calendar derived
        self.assertTrue(len(dasha.primary_windows) > 0)
        dasha_win = dasha.primary_windows[0]
        # Dasha window format is YYYY-MM-DD, not "6_months"
        self.assertRegex(dasha_win.start, r"^\d{4}-\d{2}-\d{2}$")
        self.assertRegex(dasha_win.end, r"^\d{4}-\d{2}-\d{2}$")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. MISSING DATA ABSTENTION STANDARD
    # ─────────────────────────────────────────────────────────────────────────
    def test_missing_birth_date_produces_abstention(self):
        """Missing birth date yields INSUFFICIENT_EVIDENCE with empty windows and no date guesses."""
        # Test Dasha engine directly
        dasha_res = numerology_dasha_engine.evaluate_dasha_hierarchy(day=0, month=0, year=0)
        self.assertEqual(dasha_res.status, "INSUFFICIENT_EVIDENCE")
        self.assertEqual(len(dasha_res.primary_windows), 0)
        self.assertEqual(dasha_res.driver, 0)
        self.assertEqual(dasha_res.conductor, 0)
        self.assertTrue(any(t.get("status") == "INSUFFICIENT_EVIDENCE" for t in dasha_res.rule_trace))

        # Test Orchestrator
        resp = charm_chat_orchestrator.process_chat_turn(
            message="When will I get a job offer in the next 6 months?",
            user_name="Raj",
            day=None,
            month=None,
            year=None
        )
        self.assertEqual(resp.status, "INSUFFICIENT_EVIDENCE")
        self.assertEqual(resp.consensus_status, "INSUFFICIENT_EVIDENCE")
        self.assertEqual(len(resp.numerology_dasha_result["primary_windows"]), 0)
        self.assertIn("birth_date", resp.missing_requirements["missing_inputs"])
        self.assertIn("Date of birth", resp.missing_requirements["why_required"])

        # Ensure no date hallucination in assistant message
        text = resp.assistant_message.get("text", "")
        self.assertIn("INSUFFICIENT_EVIDENCE", text)
        self.assertNotIn("2026-08", text)

    # ─────────────────────────────────────────────────────────────────────────
    # 3. LO SHU CONFLATION PREVENTION
    # ─────────────────────────────────────────────────────────────────────────
    def test_loshu_presence_without_dob_does_not_derive_dasha(self):
        """Lo Shu grid digits cannot establish Dasha timing without birth date."""
        mock_loshu = {"digit_counts": {"1": 1, "5": 2, "9": 1}}
        resp = charm_chat_orchestrator.process_chat_turn(
            message="Analyze my career timing based on my Lo Shu grid",
            user_name="Pooja",
            day=None,
            month=None,
            year=None,
            loshu_grid=mock_loshu
        )
        self.assertEqual(resp.status, "INSUFFICIENT_EVIDENCE")
        pred = resp.prediction
        self.assertIsNotNone(pred)
        self.assertIn("loshu_conflation_guard", pred.get("provenance_record", {}))
        self.assertIn("does NOT establish Dasha periods", pred["provenance_record"]["loshu_conflation_guard"])

    # ─────────────────────────────────────────────────────────────────────────
    # 4. DETERMINISTIC CONSENSUS STATUS COVERAGE (ALL 6 STATUSES)
    # ─────────────────────────────────────────────────────────────────────────
    def test_all_six_consensus_statuses(self):
        """Verify all 6 canonical consensus statuses derive deterministically."""
        dasha_valid = numerology_dasha_engine.evaluate_dasha_hierarchy(15, 8, 1990)
        dasha_invalid = numerology_dasha_engine.evaluate_dasha_hierarchy(0, 0, 0)
        event_def = {"event_family": "CAREER", "event_definition_id": "career_growth"}

        # 1. NUMEROLOGY_PRIMARY_CORROBORATED (>= 2 methods support, 0 contradict)
        eval_kp_supp = MethodEvaluation(
            evaluation_id="eval-kp-1",
            method_id="KP_ASTROLOGY",
            assessment="SUPPORTS",
            event_definition_id="career_growth",
            candidate_windows=[]
        )
        eval_vedic_supp = MethodEvaluation(
            evaluation_id="eval-vedic-1",
            method_id="VEDIC_D10_TRANSIT",
            assessment="SUPPORTS",
            event_definition_id="career_growth",
            candidate_windows=[]
        )
        res1 = consensus_engine.derive_consensus(dasha_valid, [eval_kp_supp, eval_vedic_supp], event_def)
        self.assertEqual(res1.verification_status, "NUMEROLOGY_PRIMARY_CORROBORATED")

        # 2. NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED (1 method supports, 0 contradict)
        eval_bnn_neutral = MethodEvaluation(
            evaluation_id="eval-bnn-1",
            method_id="BNN_TRANSIT",
            assessment="NEUTRAL",
            event_definition_id="career_growth",
            candidate_windows=[]
        )
        res2 = consensus_engine.derive_consensus(dasha_valid, [eval_kp_supp, eval_bnn_neutral], event_def)
        self.assertEqual(res2.verification_status, "NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED")

        # 3. NUMEROLOGY_PRIMARY_CONFLICTED (>= 1 contradict)
        eval_kp_opp = MethodEvaluation(
            evaluation_id="eval-kp-2",
            method_id="KP_ASTROLOGY",
            assessment="CONTRADICTS",
            event_definition_id="career_growth",
            candidate_windows=[]
        )
        res3 = consensus_engine.derive_consensus(dasha_valid, [eval_kp_opp, eval_vedic_supp], event_def)
        self.assertEqual(res3.verification_status, "NUMEROLOGY_PRIMARY_CONFLICTED")

        # 4. NUMEROLOGY_PRIMARY_ONLY (no astrologies support or contradict)
        res4 = consensus_engine.derive_consensus(dasha_valid, [eval_bnn_neutral], event_def)
        self.assertEqual(res4.verification_status, "NUMEROLOGY_PRIMARY_ONLY")

        # 5. INSUFFICIENT_EVIDENCE (empty primary windows or missing inputs)
        res5 = consensus_engine.derive_consensus(dasha_invalid, [], event_def)
        self.assertEqual(res5.verification_status, "INSUFFICIENT_EVIDENCE")

        # 6. NOT_ELIGIBLE_FOR_PREDICTION (empty event definition)
        res6 = consensus_engine.derive_consensus(dasha_valid, [], {})
        self.assertEqual(res6.verification_status, "NOT_ELIGIBLE_FOR_PREDICTION")

    # ─────────────────────────────────────────────────────────────────────────
    # 5. PRIMARY DASHA WINDOW IMMUTABILITY
    # ─────────────────────────────────────────────────────────────────────────
    def test_primary_dasha_window_immutability(self):
        """Verify consensus engine never modifies the primary Dasha window dates."""
        dasha_res = numerology_dasha_engine.evaluate_dasha_hierarchy(15, 8, 1990)
        orig_win_start = dasha_res.primary_windows[0].start
        orig_win_end = dasha_res.primary_windows[0].end

        # Introduce astrological evaluations with different candidate windows
        astro_eval = MethodEvaluation(
            evaluation_id="eval-kp-immut",
            method_id="KP_ASTROLOGY",
            assessment="SUPPORTS",
            event_definition_id="career_growth",
            candidate_windows=[{"start": "2026-11-01", "end": "2026-12-31"}]
        )
        consensus = consensus_engine.derive_consensus(
            primary_numerology=dasha_res,
            evaluations=[astro_eval],
            event_definition={"event_family": "CAREER"}
        )

        # Primary window must remain 100% unchanged
        self.assertEqual(consensus.primary_windows[0].start, orig_win_start)
        self.assertEqual(consensus.primary_windows[0].end, orig_win_end)

    # ─────────────────────────────────────────────────────────────────────────
    # 6. 7-TIER HUMAN-FRIENDLY RESPONSE HIERARCHY
    # ─────────────────────────────────────────────────────────────────────────
    def test_seven_tier_human_friendly_model(self):
        """Verify the 7-tier human-friendly summary structure."""
        resp = charm_chat_orchestrator.process_chat_turn(
            message="Will I land a senior executive job in the next 6 months?",
            user_name="Vikram Malhotra",
            day=15,
            month=8,
            year=1990,
            tob="10:30",
            pob="Mumbai"
        )
        hf = resp.human_friendly_summary
        self.assertIsNotNone(hf)
        # Tier 1
        self.assertIn("takeaway", hf)
        self.assertTrue(len(hf["takeaway"]) > 10)
        # Tier 2
        self.assertIn("timing_status", hf)
        self.assertIn("Verification:", hf["timing_status"])
        self.assertIn("Requested Horizon:", hf["timing_status"])
        # Tier 3
        self.assertIn("supported_by_report", hf)
        self.assertIn("Driver 6", hf["supported_by_report"])
        # Tier 4
        self.assertIn("unconcluded_aspects", hf)
        self.assertIn("Lo Shu", hf["unconcluded_aspects"])
        # Tier 5
        self.assertIn("missing_inputs_explanation", hf)
        self.assertIn("15-8-1990", hf["missing_inputs_explanation"])
        # Tier 6
        self.assertIn("practical_actions", hf)
        self.assertTrue(len(hf["practical_actions"]) > 0)
        # Tier 7
        self.assertIn("followup_question", hf)
        self.assertTrue("?" in hf["followup_question"])

    # ─────────────────────────────────────────────────────────────────────────
    # 7. REST API /api/charm/chat COMPLETE INPUTS
    # ─────────────────────────────────────────────────────────────────────────
    def test_api_charm_chat_complete(self):
        """POST /api/charm/chat with valid parameters returns complete 7-tier response."""
        payload = {
            "name": "Aarav Sharma",
            "day": 15,
            "month": 8,
            "year": 1990,
            "tob": "10:30",
            "pob": "New Delhi",
            "message": "When will I get a new leadership position in the next 6 months?"
        }
        res = self.client.post("/api/charm/chat", json=payload, headers=self.charm_headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "ANSWERED")
        self.assertIn("human_friendly_summary", data)
        self.assertIn("career_event_assessment", data)
        self.assertEqual(data["career_event_assessment"]["requested_horizon"], "6_months")
        self.assertEqual(data["career_event_assessment"]["goal"], "new_job_or_senior_role")
        self.assertTrue(len(data["cross_verification"]) > 0)

    # ─────────────────────────────────────────────────────────────────────────
    # 8. REST API /api/charm/chat MISSING BIRTH DATE
    # ─────────────────────────────────────────────────────────────────────────
    def test_api_charm_chat_missing_dob(self):
        """POST /api/charm/chat with missing birth date returns INSUFFICIENT_EVIDENCE."""
        payload = {
            "name": "Anonymous Seeker",
            "message": "Will I get a promotion in 6 months?"
        }
        res = self.client.post("/api/charm/chat", json=payload, headers=self.charm_headers)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(data["consensus_status"], "INSUFFICIENT_EVIDENCE")
        self.assertEqual(len(data["numerology_dasha_result"]["primary_windows"]), 0)
        self.assertIn("birth_date", data["missing_requirements"]["missing_inputs"])

    # ─────────────────────────────────────────────────────────────────────────
    # 9. INTEGRATION VIA /api/v1/readings/ask
    # ─────────────────────────────────────────────────────────────────────────
    def test_readings_ask_endpoint_includes_charm_prediction(self):
        """POST /api/v1/readings/ask returns charm_prediction with human_friendly model."""
        payload = {
            "name": "Aarav Sharma",
            "day": 15,
            "month": 8,
            "year": 1990,
            "tob": "10:30",
            "city": "New Delhi",
            "question": "Is 2026 favorable for my career progression and senior job hunt?",
            "premium_token": "test_master_pass",
            "user_id": "test_user_aarav"
        }
        res = self.client.post("/api/v1/readings/ask", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("charm_prediction", data)
        cp = data["charm_prediction"]
        self.assertIsNotNone(cp)
        self.assertIn("human_friendly", cp)
        self.assertIn("takeaway", cp["human_friendly"])
        self.assertIn("verification_status", cp)

    # ─────────────────────────────────────────────────────────────────────────
    # 10. BRAND AND DESIGN SYSTEM COMPLIANCE
    # ─────────────────────────────────────────────────────────────────────────
    def test_brand_identity_and_zero_raw_black(self):
        """Verify UI template conforms to brand guidelines and contains zero #000000."""
        with open("app/static/charm_ai.html", "r", encoding="utf-8") as f:
            content = f.read()

        # Zero raw black check
        self.assertNotIn("#000000", content, "Violates zero raw black #000000 directive.")

        # Brand Name check
        self.assertIn("NUMEROS VISION", content)
        self.assertIn("ANVEIL EVERY CHARM", content)

        # Header and Footer check
        self.assertIn("nv-header", content)
        self.assertIn("nv-footer", content)

        # 7-Tier markup presence
        self.assertIn("✦ Tier 1: Career Momentum Takeaway", content)
        self.assertIn("✦ Tier 2: Timing Horizon &amp; Verification Status", content)
        self.assertIn("✓ Tier 3: Supported by Verified Findings", content)
        self.assertIn("✦ Tier 4: What Cannot Yet Be Concluded", content)
        self.assertIn("✦ Tier 5: Input &amp; Calculation Provenance", content)
        self.assertIn("✦ Tier 6: Practical Executive Actions", content)
        self.assertIn("✦ Tier 7: Suggested Follow-Up Inquiry", content)

if __name__ == "__main__":
    unittest.main()
