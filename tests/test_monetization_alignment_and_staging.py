"""
TEST SUITE: MONETIZATION ALIGNMENT, ENTITLEMENTS & STAGING REPLICA TEST MODE
Verifies the 3 Rules:
1. Free Report Alignment & Gaps Hook Engine:
   - ALIGNED vs FRICTION_DETECTED polarity check (Driver vs Conductor)
   - Lo Shu missing planes (Golden Prosperity Plane 4-5-6, Brahmasthan 5, etc.)
   - Personalized conversion hooks with official brand tagline "Anveil Every Charm"
   - POST /api/v1/payments/alignment-gap-analysis endpoint
2. Paid Subscription Entitlements, Credit Consumption & Upselling:
   - Free report is accessible without payment
   - Paid tiers (report_master, complete_report, etc.) strictly paywalled (HTTP 402) when unpaid
   - Payment sessions & user account entitlements unlock reports
   - Question prediction quota tracks remaining credits; triggers upscale hooks when credits reach zero
   - Payment verification updates registered user accounts and credit pools
3. Staging Replica Testing Mode:
   - x-staging-test-bypass header & staging_preview parameter grant full replica test access for QA/QC
   - Test master tokens allow bypass in non-production
   - Production protection prevents unauthorized bypasses
"""

import hashlib
import hmac
import os
import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.engine.monetization_alignment_engine import (
    analyze_user_alignment_and_gaps,
    is_staging_bypass_authorized,
    FRIENDLY_PAIRS,
    ENEMY_PAIRS
)
from app.api.payments import (
    get_session_info,
    consume_question,
    check_report_access,
    _verified_payments,
    RAZORPAY_KEY_SECRET
)
from app.api.auth import (
    _USER_ACCOUNTS,
    _EMAIL_TO_USER_ID,
    update_user_entitlements,
    get_user_account_by_identifier
)


class TestMonetizationAlignmentAndStaging(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    # ── RULE 1: ALIGNMENT & GAPS HOOK ENGINE ────────────────────────────────

    def test_alignment_enemy_polarity_friction_detected(self):
        """Driver 1 (Sun) vs Conductor 8 (Saturn) is an active enemy polarity."""
        res = analyze_user_alignment_and_gaps(
            driver=1,
            conductor=8,
            loshu_counts={"1": 2, "8": 1},
            missing_numbers=[2, 3, 4, 5, 6, 7, 9],
            current_plan="free",
            credits_remaining=0
        )
        self.assertEqual(res["alignment_status"], "FRICTION_DETECTED")
        self.assertLess(res["alignment_score"], 60)
        self.assertTrue(res["is_enemy"])
        self.assertFalse(res["is_friendly"])

        # Check detected gaps
        gap_codes = [g["gap_code"] for g in res["detected_gaps"]]
        self.assertIn("POLARITY_DRIVER_CONDUCTOR", gap_codes)
        self.assertIn("GOLDEN_PROSPERITY_GAP", gap_codes)
        self.assertIn("CENTRAL_STABILITY_VOID", gap_codes)

        # Check Tagline CTA presence (AGENTS.md §2 all-caps ANVEIL EVERY CHARM & Phase 0B 510 INR)
        cta = res["primary_cta"]
        self.assertIn("ANVEIL EVERY CHARM", cta["tagline"])
        self.assertIn("ANVEIL EVERY CHARM", cta["button_text"])
        self.assertEqual(cta["amount_inr"], 510)

    def test_alignment_friendly_harmony_detected(self):
        """Driver 1 (Sun) vs Conductor 5 (Mercury) is an auspicious friendly pair."""
        res = analyze_user_alignment_and_gaps(
            driver=1,
            conductor=5,
            loshu_counts={"1": 1, "4": 1, "5": 1, "6": 1, "9": 1},
            missing_numbers=[2, 3, 7, 8],
            current_plan="free",
            credits_remaining=0
        )
        self.assertEqual(res["alignment_status"], "ALIGNED")
        self.assertGreaterEqual(res["alignment_score"], 80)
        self.assertTrue(res["is_friendly"])
        self.assertFalse(res["is_enemy"])
        self.assertEqual(res["golden_plane_gap"], [])  # Has 4, 5, 6 complete!

    def test_api_alignment_gap_analysis_endpoint(self):
        """POST /api/v1/payments/alignment-gap-analysis returns deterministic JSON."""
        payload = {
            "driver": 3,
            "conductor": 6,  # Jupiter vs Venus friction
            "loshu_counts": {"3": 1, "6": 1},
            "missing_numbers": [4, 5],
            "current_plan": "free"
        }
        res = self.client.post("/api/v1/payments/alignment-gap-analysis", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["alignment_status"], "FRICTION_DETECTED")
        self.assertIn("ANVEIL EVERY CHARM", data["primary_cta"]["button_text"])

    # ── RULE 2: PAID SUBSCRIPTIONS, ENTITLEMENTS & CREDIT CONSUMPTION ──────

    def test_free_package_report_always_accessible_with_alignment_hook(self):
        """Free discovery tier must be accessible without payment, enriched with alignment."""
        payload = {
            "name": "Arjun Sharma",
            "day": 10,
            "month": 8,
            "year": 1995,
            "tier": "free",
            "birth_time": "10:15 AM",
            "birth_city": "Delhi"
        }
        res = self.client.post("/api/v1/readings/package-report", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("tier"), "free")
        self.assertIn("alignment_analysis", data)
        self.assertIn("primary_cta", data["alignment_analysis"])
        self.assertIn("ANVEIL EVERY CHARM", data["alignment_analysis"]["primary_cta"]["button_text"])

    def test_paid_report_blocked_when_unpaid(self):
        """Paid tiers (e.g. report_master) must return 402 with gap hook when unpaid."""
        payload = {
            "name": "Priya Patel",
            "day": 17,  # Driver 8
            "month": 1,  # Conductor 1 (8 vs 1 friction)
            "year": 1992,
            "tier": "report_master",
            "birth_time": "02:30 PM",
            "birth_city": "Mumbai"
        }
        res = self.client.post("/api/v1/readings/package-report", json=payload)
        self.assertEqual(res.status_code, 402)
        err = res.json()
        detail = err.get("detail", {})
        self.assertEqual(detail.get("status"), "payment_required")
        self.assertFalse(detail.get("access_granted"))
        self.assertEqual(detail.get("tagline"), "ANVEIL EVERY CHARM")
        self.assertIn("alignment_analysis", detail)
        self.assertIn("ANVEIL EVERY CHARM", detail.get("primary_cta", {}).get("button_text", ""))

    def test_paid_report_unlocked_with_verified_session(self):
        """Paid tiers succeed when a valid premium token for complete_report is provided."""
        # Create verified session in store
        test_token = "nv_test_session_master_9988"
        _verified_payments[test_token] = {
            "plan": "complete_report",
            "plan_name": "Complete Reports & Remedies",
            "questions_remaining": 9999,
            "has_remedies": True,
            "verified_at": 1700000000
        }

        payload = {
            "name": "Priya Patel",
            "day": 17,
            "month": 1,
            "year": 1992,
            "tier": "report_master",
            "premium_token": test_token
        }
        res = self.client.post("/api/v1/readings/package-report", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data.get("access_status", {}).get("authorized"))

    def test_charm_ai_credit_exhaustion_triggers_upsell_package(self):
        """When question credits reach 0, response injects upsell package with tagline CTA."""
        # Setup session with 1 question remaining
        one_q_token = "nv_test_token_1q_exhaust"
        _verified_payments[one_q_token] = {
            "plan": "starter_5q",
            "plan_name": "Starter 5Q",
            "questions_count": 1,
            "questions_remaining": 1,
            "has_remedies": False
        }

        ask_payload = {
            "question": "Will my career move happen this year?",
            "name": "Rohan Mehra",
            "day": 12,
            "month": 4,
            "year": 1990,
            "premium_token": one_q_token
        }
        res = self.client.post("/api/v1/readings/ask", json=ask_payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        
        # Credit was consumed (1 -> 0)
        self.assertEqual(data["questions_remaining"], 0)
        self.assertTrue(data.get("credits_exhausted"))
        
        # Upsell package must be present with brand tagline
        upsell = data.get("upsell_package")
        self.assertIsNotNone(upsell)
        self.assertIn("ANVEIL EVERY CHARM", upsell.get("tagline_cta", ""))

    def test_payment_verify_syncs_user_entitlements(self):
        """Payment verify endpoint updates registered user account with plans and credits."""
        user_email = "test_entitlement_seeker@numerosvision.com"
        # Register user first via signup
        signup_payload = {
            "name": "Entitled Seeker",
            "email": user_email,
            "phone": "+919876543999",
            "day": 15,
            "month": 5,
            "year": 1993,
            "password": "SecurePassword123!",
            "consent_profile_storage": True
        }
        s_res = self.client.post("/api/v1/auth/signup", json=signup_payload)
        self.assertEqual(s_res.status_code, 200)
        user_token = s_res.json()["session_token"]

        # Call payment verify for Charm AI Starter Pack (charm_single: 5 questions) with valid HMAC-SHA256 signature
        ord_id = "order_MOCK_charm_single_12345"
        pay_id = "pay_MOCK_12345678"
        valid_sig = hmac.new(RAZORPAY_KEY_SECRET.encode(), f"{ord_id}|{pay_id}".encode(), hashlib.sha256).hexdigest()
        verify_payload = {
            "razorpay_order_id": ord_id,
            "razorpay_payment_id": pay_id,
            "razorpay_signature": valid_sig,
            "plan": "charm_single",
            "email": user_email
        }
        v_res = self.client.post("/api/v1/payments/verify", json=verify_payload)
        self.assertEqual(v_res.status_code, 200)

        # Inspect /me endpoint for updated entitlements
        me_res = self.client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {user_token}"})
        self.assertEqual(me_res.status_code, 200)
        me_data = me_res.json()
        entitlements = me_data.get("entitlements", {})
        self.assertIn("charm_single", entitlements.get("purchased_plans", []))
        self.assertGreaterEqual(entitlements.get("charm_credits_remaining", 0), 5)

    # ── RULE 3: STAGING REPLICA TEST MODE ───────────────────────────────────

    def test_staging_header_bypasses_report_paywall_in_development(self):
        """x-staging-test-bypass: true allows full replica testing of paid reports."""
        payload = {
            "name": "QA Tester",
            "day": 14,
            "month": 6,
            "year": 1988,
            "tier": "complete_report",
            "birth_time": "09:00 AM",
            "birth_city": "Bengaluru"
        }
        # Without staging header, expect 402
        res_blocked = self.client.post("/api/v1/readings/package-report", json=payload)
        self.assertEqual(res_blocked.status_code, 402)

        # With staging header, expect 200 with complete report
        headers = {"x-staging-test-bypass": "true"}
        res_allowed = self.client.post("/api/v1/readings/package-report", json=payload, headers=headers)
        self.assertEqual(res_allowed.status_code, 200)
        data = res_allowed.json()
        self.assertEqual(data.get("access_status", {}).get("tier"), "complete_report")
        self.assertTrue(data.get("access_status", {}).get("is_staging_preview"))

    def test_staging_query_param_bypasses_report_paywall(self):
        """staging_preview=true query parameter allows replica testing."""
        payload = {
            "name": "QA Tester",
            "day": 14,
            "month": 6,
            "year": 1988,
            "tier": "report_master"
        }
        res = self.client.post("/api/v1/readings/package-report?staging_preview=true", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data.get("access_status", {}).get("authorized"))
        self.assertTrue(data.get("access_status", {}).get("is_staging_preview"))

    def test_staging_test_token_authorizes_bypass(self):
        """Authorized test tokens (e.g. test_master_pass) allow QA access."""
        auth = is_staging_bypass_authorized({}, {}, token="test_master_pass")
        self.assertTrue(auth)

    def test_staging_bypass_strictly_rejected_in_production(self):
        """In production without ALLOW_STAGING_TEST_BYPASS, staging header is rejected."""
        old_env = os.environ.get("ENVIRONMENT")
        old_bypass = os.environ.get("ALLOW_STAGING_TEST_BYPASS")
        try:
            os.environ["ENVIRONMENT"] = "production"
            os.environ["ALLOW_STAGING_TEST_BYPASS"] = "false"
            
            headers = {"x-staging-test-bypass": "true"}
            auth = is_staging_bypass_authorized(headers, {}, token=None)
            self.assertFalse(auth, "Staging bypass must be rejected in strict production environment!")
        finally:
            if old_env is not None:
                os.environ["ENVIRONMENT"] = old_env
            else:
                os.environ.pop("ENVIRONMENT", None)
            if old_bypass is not None:
                os.environ["ALLOW_STAGING_TEST_BYPASS"] = old_bypass
            else:
                os.environ.pop("ALLOW_STAGING_TEST_BYPASS", None)


if __name__ == "__main__":
    unittest.main()
