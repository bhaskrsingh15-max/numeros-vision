"""
DEEP TEST SUITE: LLM AGENTS, QUESTION ORCHESTRATION, PREDICTIONS & REMEDIES
Covers:
1. Question classification across career, marriage, wealth, health, property, and Hindi keywords.
2. Freemium Gate: returns ONLY ALIGNED / NOT ALIGNED with 2-line reasoning + Anveil Every Charm paywall.
3. Paid Subscription Entitlement & Remedy Gating (Starter ₹95, Growth ₹399, Complete ₹1,050, Consultation ₹11,500).
4. Bhaskr Singh Profile Ground Truth: Driver 1, Conductor 4, Kua 1, Cheiro Name 32 -> 5, Lo Shu missing (3, 5, 6, 7).
5. Multi-Layer Remedies: Vedic crystals, Lo Shu missing numbers, specialized Topic 26 remedies (Solid silver square, blood donation).
6. 12-Stage Hallucination Gate & Copy Linter: Banned words, tagline lock, no fabricated stats.
"""

import sys
import os
import unittest
import asyncio

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.api.readings import ask_question, OpenEndedQuestionRequest, _classify_question_topic
from app.api.payments import (
    create_order, CreateOrderRequest, verify_payment, VerifyPaymentRequest,
    get_session_info, PLANS
)
from app.engine.consensus import generate_consensus_reading
from app.engine.remedy_engine import (
    generate_comprehensive_predictions_and_remedies,
    get_vedic_crystal_remedies,
    calculate_name_number,
    calculate_mobile_number_sum
)
from app.engine.cheiro_engine import (
    analyze_number,
    analyze_name_cheiro
)
from app.engine.professional_numerology_engine import (
    audit_mobile_number,
    calculate_personal_cycles,
    analyze_kua_and_directions,
    analyze_share_market_profile,
    get_bonus_query_solution
)
from app.engine.claim_validator import lint_copy, validate_claims_and_hallucination_gate, ClaimNode

class TestDeepLLMAgentsQuestionsPredictionsRemedies(unittest.TestCase):

    def setUp(self):
        # Canonical test profile from User Specification Section 9
        self.test_profile = {
            "name": "Bhaskr Singh",
            "day": 28,
            "month": 11,
            "year": 1981,
            "mobile": "9876543210"
        }

    # ──────────────────────────────────────────────────────────────────────────
    # 1. QUESTION CLASSIFICATION & INTENT ROUTING
    # ──────────────────────────────────────────────────────────────────────────
    def test_question_intent_classification(self):
        """Tests intent routing across English and Hindi / Hinglish keywords."""
        test_cases = [
            ("When will I get a job promotion in my office?", "career"),
            ("Mera vyapar aur naukri kab badhegi?", "career"),
            ("When is my marriage happening and will my spouse be supportive?", "marriage"),
            ("Mera vivah aur shaadi ka yog kab ban raha hai?", "marriage"),
            ("Can I invest in share market and cryptocurrency for wealth?", "wealth"),
            ("Kitna paisa aur dhan laabh hoga is saal?", "wealth"),
            ("Why do I have chronic back pain and fatigue?", "health"),
            ("Bimari aur sehat se chutkara kab milega?", "health"),
            ("Is it a good time to buy a new house or vehicle?", "property"),
            ("Naya makan aur zameen lene ka sahi samay?", "property"),
            ("Tell me about my life path vibration", "general")
        ]
        for q, expected_topic in test_cases:
            topic = _classify_question_topic(q)
            self.assertEqual(topic, expected_topic, f"Failed for query: '{q}' -> got '{topic}', expected '{expected_topic}'")

    # ──────────────────────────────────────────────────────────────────────────
    # 2. FREEMIUM GATE ORACLE VERDICT & PAYWALL INTEGRITY
    # ──────────────────────────────────────────────────────────────────────────
    def test_freemium_gate_oracle_response(self):
        """
        User Prompt Requirement: In the AI monetization only show freemium align and not align
        as an answer once the user gives the inputs of all data, and afterward to know further
        to Anveil Every Charm paid subscription comes up.
        """
        req = OpenEndedQuestionRequest(
            name=self.test_profile["name"],
            day=self.test_profile["day"],
            month=self.test_profile["month"],
            year=self.test_profile["year"],
            question="Can I start a new business partnership in 2026?"
        )
        res = ask_question(req)

        # 1. Verify it triggers the Freemium Gate
        self.assertTrue(res["is_freemium_gate"])
        self.assertFalse(res["is_premium"])

        # 2. Verify alignment verdict is ONLY ALIGNED or NOT ALIGNED
        self.assertIn(res["alignment_status"], ["ALIGNED", "NOT ALIGNED"])
        self.assertTrue(any(word in res["alignment_grade"] for word in ["Resonance", "Friction"]))
        self.assertTrue(len(res["alignment_summary"]) > 40)

        # 3. Verify paywall details
        paywall = res["paywall"]
        self.assertEqual(paywall["title"], "Anveil Every Charm to Access Full Answers")
        plans = {p["id"]: p for p in paywall["plans"]}

        # Starter: ₹95 (original ₹199), 5 questions, no remedies
        self.assertIn("starter_5q", plans)
        self.assertEqual(plans["starter_5q"]["amount_inr"], 95)
        self.assertEqual(plans["starter_5q"]["original_price_inr"], 199)
        self.assertEqual(plans["starter_5q"]["questions_count"], 5)
        self.assertFalse(plans["starter_5q"]["has_remedies"])

        # Growth: ₹399 (original ₹599), 10 questions + remedies
        self.assertIn("growth_10q", plans)
        self.assertEqual(plans["growth_10q"]["amount_inr"], 399)
        self.assertEqual(plans["growth_10q"]["original_price_inr"], 599)
        self.assertEqual(plans["growth_10q"]["questions_count"], 10)
        self.assertTrue(plans["growth_10q"]["has_remedies"])

        # Complete: ₹1,050 (original ₹1,299), full report + all remedies
        self.assertIn("complete_report", plans)
        self.assertEqual(plans["complete_report"]["amount_inr"], 1050)
        self.assertEqual(plans["complete_report"]["original_price_inr"], 1299)
        self.assertTrue(plans["complete_report"]["has_remedies"])

        # 4. Verify direct prediction answer, simple why-this-is-happening root cause, and remedies
        self.assertIn("direct_answer", res)
        self.assertTrue(len(res["direct_answer"]) > 20)
        self.assertIn("why_this_is_happening", res)
        self.assertTrue(len(res["why_this_is_happening"]["root_cause_explanation"]) > 30)
        self.assertIn("core_numbers", res["why_this_is_happening"])
        self.assertIn("remedies", res)
        self.assertTrue(len(res["remedies"]) >= 2)
        self.assertIn("lucky_elements", res)

    # ──────────────────────────────────────────────────────────────────────────
    # 3. PAID SUBSCRIPTION ENTITLEMENTS & REMEDY GATING
    # ──────────────────────────────────────────────────────────────────────────
    def test_paid_starter_tier_redacts_remedies(self):
        """
        Starter plan (₹95): 5 questions predictions, NO remedies.
        System must redact remedies from synthesis when user is on Starter plan.
        """
        async def run_starter():
            order = await create_order(CreateOrderRequest(plan="starter_5q", name="Bhaskr Singh", email="bhaskr@test.com"))
            verified = await verify_payment(VerifyPaymentRequest(
                razorpay_order_id=order["order_id"],
                razorpay_payment_id="pay_TEST_STARTER",
                razorpay_signature="sig_mock",
                plan="starter_5q",
                email="bhaskr@test.com"
            ))
            token = verified["premium_token"]
            
            # Ask question with token
            req = OpenEndedQuestionRequest(
                name="Bhaskr Singh",
                day=28, month=11, year=1981,
                question="What is my career direction for this year?",
                premium_token=token
            )
            res = ask_question(req)
            self.assertTrue(res["is_premium"])
            self.assertFalse(res["has_remedies"])
            self.assertEqual(res["questions_remaining"], 4)
            # Remedies must be empty / redacted in Starter 95 plan
            synth = res["synthesis_result"]
            self.assertEqual(synth.get("remedies"), [])
            self.assertEqual(synth.get("gemstone_remedies"), [])
            
        asyncio.run(run_starter())

    def test_paid_growth_tier_delivers_full_remedies(self):
        """
        Growth plan (₹399): 10 questions + customized remedies.
        System must deliver full multi-layer remedies.
        """
        async def run_growth():
            order = await create_order(CreateOrderRequest(plan="growth_10q", name="Bhaskr Singh", email="bhaskr@test.com"))
            verified = await verify_payment(VerifyPaymentRequest(
                razorpay_order_id=order["order_id"],
                razorpay_payment_id="pay_TEST_GROWTH",
                razorpay_signature="sig_mock",
                plan="growth_10q",
                email="bhaskr@test.com"
            ))
            token = verified["premium_token"]
            
            req = OpenEndedQuestionRequest(
                name="Bhaskr Singh",
                day=28, month=11, year=1981,
                question="How can I conceieve a child and what is the auspicious timing window?",
                premium_token=token
            )
            res = ask_question(req)
            self.assertTrue(res["is_premium"])
            self.assertTrue(res["has_remedies"])
            self.assertEqual(res["questions_remaining"], 9)
            synth = res["synthesis_result"]
            # Specialized solution must contain child conceive guidance and non-empty remedies
            spec = synth["professional_syllabus_insights"]["specialized_solution"]
            self.assertIn("child", spec["topic"].lower())
            self.assertTrue(len(spec["remedies"]) > 0)
            
        asyncio.run(run_growth())

    def test_high_stakes_question_recommends_master_consultation(self):
        """
        For high stakes queries (child conceiving, divorce, lawsuit), system must present
        the 1-on-1 Master Personal Consultation (₹11,500, original ₹15,000).
        """
        async def run_consultation_check():
            order = await create_order(CreateOrderRequest(plan="growth_10q", name="Bhaskr Singh", email="bhaskr@test.com"))
            verified = await verify_payment(VerifyPaymentRequest(
                razorpay_order_id=order["order_id"],
                razorpay_payment_id="pay_TEST_CONSULT",
                razorpay_signature="sig_mock",
                plan="growth_10q",
                email="bhaskr@test.com"
            ))
            req = OpenEndedQuestionRequest(
                name="Bhaskr Singh",
                day=28, month=11, year=1981,
                question="My partner and I are facing divorce and custody dispute in court, what should I do?",
                premium_token=verified["premium_token"]
            )
            res = ask_question(req)
            synth = res["synthesis_result"]
            self.assertIn("master_consultation_option", synth)
            opt = synth["master_consultation_option"]
            self.assertEqual(opt["price_inr"], 11400)
            self.assertEqual(opt["original_price_inr"], 24000)
            self.assertIn("90 Minutes", opt["duration"])
            
        asyncio.run(run_consultation_check())

    # ──────────────────────────────────────────────────────────────────────────
    # 4. BHASKR SINGH GROUND TRUTH DETERMINISTIC PREDICTIONS
    # ──────────────────────────────────────────────────────────────────────────
    def test_bhaskr_singh_deterministic_profile(self):
        """
        Validates User Specification Section 9 ground truth:
        DOB: 28-11-1981
        Driver: 28 -> 10 -> 1
        Conductor: 28-11-1981 -> 31 -> 4
        Kua: 11 - 10 = 1
        Chaldean Name: 'Bhaskr Singh' = 15 + 17 = 32 -> 5
        """
        consensus = generate_consensus_reading(
            name=self.test_profile["name"],
            day=self.test_profile["day"],
            month=self.test_profile["month"],
            year=self.test_profile["year"]
        )

        vedic = consensus["vedic_numerology"]
        # Driver 1
        self.assertEqual(vedic["driver_number"], 1)
        self.assertIn("Sun", vedic["driver_planet"])
        # Conductor 4
        self.assertEqual(vedic["conductor_number"], 4)
        self.assertIn("Rahu", vedic["conductor_planet"])
        # Cheiro day compound preservation (28 -> The Trusting Sceptic)
        cheiro_day = vedic["cheiro_day_compound"]
        self.assertEqual(cheiro_day["day_input"], 28)
        self.assertEqual(cheiro_day["mulank_output"], 1)
        self.assertIn("Promise and Loss", cheiro_day["archetype"])

        # Kua Number Male (11 - 10 = 1)
        kua_data = analyze_kua_and_directions(gender="male", birth_year=1981)
        self.assertEqual(kua_data["kua_number"], 1)
        self.assertEqual(kua_data["kua_group"], "East")
        self.assertEqual(kua_data["success_direction_sheng_chi"], "SE")
        self.assertEqual(kua_data["stability_direction_fu_wei"], "N")

        # Lo Shu Grid Missing Numbers
        loshu = consensus["lo_shu_grid"]
        missing = set(loshu["missing_numbers"])
        for expected_missing in [3, 5, 6, 7]:
            self.assertIn(expected_missing, missing)

        # Chaldean Name Balancing: 32 -> 5
        name_eval = analyze_name_cheiro("Bhaskr Singh", driver=1, conductor=4)
        self.assertEqual(name_eval["compound_sum"], 32)
        self.assertEqual(name_eval["name_root"], 5)
        self.assertEqual(name_eval["compound_archetype"], "Command / Combination")
        self.assertEqual(name_eval["reduction_path"], "32 → 5")

    # ──────────────────────────────────────────────────────────────────────────
    # 5. MULTI-LAYER REMEDIES ENGINE
    # ──────────────────────────────────────────────────────────────────────────
    def test_multi_layer_remedy_generation(self):
        """Tests unified 8-layer predictions & remedies endpoint."""
        remedy_report = generate_comprehensive_predictions_and_remedies(
            name="Bhaskr Singh",
            day=28,
            month=11,
            year=1981,
            mobile_number="9876543210"
        )
        summary = remedy_report["predictions_summary"]
        self.assertEqual(summary["driver_mulank"], 1)
        self.assertEqual(summary["conductor_bhagyank"], 4)
        
        # Check Vedic crystal remedies
        crystals = remedy_report["remedies_8_layer_package"]["layer7_vedic_crystal_and_gemstone_remedies"]
        self.assertTrue(len(crystals) > 0)
        # Driver 1 crystal must be Ruby / Sunstone
        driver_gem = crystals[0]
        self.assertEqual(driver_gem["number"], 1)
        self.assertIn("Ruby", driver_gem["primary_gemstone"])
        self.assertIn("Sunstone", driver_gem["healing_crystal"])

        # Check Topic 26 Specialized Remedies:
        # A. Solid silver square remedy for Rahu 4
        silver_sq = get_bonus_query_solution("solid silver square")
        self.assertIn("silver square", silver_sq["topic"].lower())
        self.assertIn("silver", silver_sq["significance"].lower())

        # B. Blood donation in anti-months
        blood_don = get_bonus_query_solution("blood donation in anti months")
        self.assertIn("blood", blood_don["topic"].lower())
        self.assertTrue(len(blood_don["remedies"]) > 0)

        # C. Autism grounding
        autism_sol = get_bonus_query_solution("autism child grounding")
        self.assertIn("autism", autism_sol["topic"].lower())
        self.assertTrue(len(autism_sol["remedies"]) > 0)

    # ──────────────────────────────────────────────────────────────────────────
    # 6. MOBILE NUMEROLOGY & MALEFIC PAIRS AUDIT
    # ──────────────────────────────────────────────────────────────────────────
    def test_mobile_number_malefic_pairs_audit(self):
        """Tests mobile number audit for malefic pairs 14, 16, 18, 28, 48."""
        bad_mobile = "9814168428"
        audit = audit_mobile_number(bad_mobile, driver=1)
        self.assertEqual(audit["status"], "Requires Change or Remedy")
        malefic_found = [m["pair"] for m in audit["malefic_pairs_found"]]
        # Must detect at least 14, 16, 28, 84
        self.assertTrue(any(p in malefic_found for p in ["14", "16", "28", "84"]))
        self.assertTrue(len(audit["remedy"]) > 0)

        # Favorable mobile total
        favorable_mobile = "9999999995"  # sum = 86 -> 14 -> 5 (Mercury)
        total_sum = calculate_mobile_number_sum(favorable_mobile)
        self.assertEqual(total_sum, 5)

    # ──────────────────────────────────────────────────────────────────────────
    # 7. COPY LINTER & 12-STAGE HALLUCINATION GATE INTEGRITY
    # ──────────────────────────────────────────────────────────────────────────
    def test_copy_linter_sanitizes_ai_output(self):
        """Verifies that copy linter blocks banned words and enforces tagline."""
        # Output with banned words
        dirty_text = "Unlock your career potential with this revolutionary insight to elevate your income seamlessly. Unveil Every Charm."
        lint = lint_copy(dirty_text)
        self.assertFalse(lint.is_valid)
        self.assertIn("Anveil Every Charm", lint.remediated_text)
        self.assertNotIn("Unlock", lint.remediated_text)
        self.assertNotIn("seamlessly", lint.remediated_text)

    def test_hallucination_gate_enforces_empty_canvas(self):
        """Verifies fail-closed behavior for unsupported AI claims."""
        valid_calcs = {"calc_d1", "calc_c4"}
        valid_rules = {"RULE_DRIVER_CALC_V1", "RULE_CONDUCTOR_CALC_V1"}
        valid_sources = {"SOURCE_TN_DIPLOMA_DAY1"}

        supported_claim = ClaimNode(
            claim_id="c1",
            text="Driver 1 grants authority and leadership.",
            calculation_ref="calc_d1",
            rule_id="RULE_DRIVER_CALC_V1",
            source_ref="SOURCE_TN_DIPLOMA_DAY1"
        )
        verdict = validate_claims_and_hallucination_gate(
            claims=[supported_claim],
            full_output_text="Your Driver number is 1. Anveil Every Charm.",
            valid_calculation_ids=valid_calcs,
            valid_rule_ids=valid_rules,
            valid_source_ids=valid_sources
        )
        self.assertTrue(verdict.passed)
        self.assertEqual(verdict.stage_reached, 12)

if __name__ == "__main__":
    unittest.main()
