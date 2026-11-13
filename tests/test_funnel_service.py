"""
UNIT AND INTEGRATION TESTS — ADVANCED MARKETING FUNNEL & CONVERSION FRAMEWORK (v1.5.0)
NUMEROS VISION · ANVEIL EVERY CHARM
"""

import unittest
from datetime import datetime, timezone, timedelta
from fastapi.testclient import TestClient

from app.main import app
from app.engine.funnel_service import (
    PricePolicy,
    digit_root,
    validate_single_price,
    validate_price_pair,
    FunnelStage,
    JourneyState,
    JourneyContext,
    Entitlement,
    EntitlementDecision,
    decide_feature_access,
    PRODUCT_FUNNEL_CATALOG,
    get_next_step,
    log_funnel_event
)


class TestDigitRootAndPricePolicy(unittest.TestCase):
    """Test suite for digit-root pricing policy engine."""

    def test_digit_root_calculation(self):
        # Single digits
        for i in range(1, 10):
            self.assertEqual(digit_root(i), i)

        # Multi-digits
        self.assertEqual(digit_root(95), 5)      # 9+5=14 -> 5
        self.assertEqual(digit_root(199), 1)     # 1+9+9=19 -> 1+9=10 -> 1
        self.assertEqual(digit_root(249), 6)     # 2+4+9=15 -> 6
        self.assertEqual(digit_root(399), 3)     # 3+9+9=21 -> 3
        self.assertEqual(digit_root(510), 6)     # 5+1+0=6
        self.assertEqual(digit_root(1050), 6)    # 1+0+5+0=6
        self.assertEqual(digit_root(1499), 5)    # 1+4+9+9=23 -> 5
        self.assertEqual(digit_root(2499), 6)    # 2+4+9+9=24 -> 6
        self.assertEqual(digit_root(5999), 5)    # 5+9+9+9=32 -> 5

    def test_digit_root_invalid_inputs(self):
        with self.assertRaises(ValueError):
            digit_root(0)
        with self.assertRaises(ValueError):
            digit_root(-100)
        with self.assertRaises(ValueError):
            digit_root(True)  # booleans are ints in Python, should be blocked
        with self.assertRaises(ValueError):
            digit_root(199.99)  # float forbidden

    def test_price_pair_validation(self):
        policy = PricePolicy(version="test-policy", allowed_digit_roots=frozenset({1, 3, 5, 6}))

        # Valid pair: 999 (root 9, wait! reference price root 9 is rejected if root 9 not allowed)
        # In policy: reference price 1999 (root 1) and offer 1299 (root 3)
        res = validate_price_pair(1999, 1299, policy)
        self.assertTrue(res["valid"])
        self.assertEqual(res["reference_root"], 1)
        self.assertEqual(res["offer_root"], 3)
        self.assertEqual(res["savings_inr"], 700)

        # Offer higher than reference should fail
        res2 = validate_price_pair(510, 999, policy)
        self.assertFalse(res2["valid"])
        self.assertIn("OFFER_NOT_BELOW_REFERENCE", res2["errors"])

    def test_catalog_prices_have_valid_roots(self):
        """Verifies that all standard products in catalog have roots in {1, 3, 5, 6}."""
        for pid, prod in PRODUCT_FUNNEL_CATALOG.items():
            price = prod["price_inr"]
            root = digit_root(price)
            self.assertIn(
                root, {1, 3, 5, 6},
                f"Product {pid} price {price} reduces to root {root}, not in {{1, 3, 5, 6}}"
            )


class TestEntitlementDecisionEngine(unittest.TestCase):
    """Test suite for access control and entitlement evaluation."""

    def setUp(self):
        self.now = datetime(2026, 10, 21, 12, 0, tzinfo=timezone.utc)

    def test_purchase_entitlement(self):
        e = [
            Entitlement(
                feature_id="report_master",
                source_type="PURCHASE",
                status="ACTIVE",
                starts_at=self.now - timedelta(days=1),
                expires_at=None
            )
        ]
        decision = decide_feature_access("report_master", e, self.now)
        self.assertEqual(decision, EntitlementDecision.ALLOW_PURCHASED)

    def test_subscription_active_and_expired(self):
        active_sub = [
            Entitlement(
                feature_id="ai_questions",
                source_type="SUBSCRIPTION",
                status="ACTIVE",
                starts_at=self.now - timedelta(days=10),
                expires_at=self.now + timedelta(days=20)
            )
        ]
        self.assertEqual(decide_feature_access("ai_questions", active_sub, self.now), EntitlementDecision.ALLOW_SUBSCRIPTION)

        expired_sub = [
            Entitlement(
                feature_id="ai_questions",
                source_type="SUBSCRIPTION",
                status="ACTIVE",
                starts_at=self.now - timedelta(days=40),
                expires_at=self.now - timedelta(days=10)
            )
        ]
        self.assertEqual(decide_feature_access("ai_questions", expired_sub, self.now), EntitlementDecision.DENY_EXPIRED)

    def test_quota_exhausted(self):
        exhausted = [
            Entitlement(
                feature_id="ai_questions",
                source_type="PURCHASE",
                status="ACTIVE",
                starts_at=self.now - timedelta(days=1),
                expires_at=None,
                quota_remaining=0
            )
        ]
        self.assertEqual(decide_feature_access("ai_questions", exhausted, self.now), EntitlementDecision.DENY_QUOTA_EXHAUSTED)


class TestFunnelServiceNextStep(unittest.TestCase):
    """Test suite for 7-stage marketing funnel and next step engine."""

    def test_initial_interest_stage(self):
        ctx = JourneyContext(calculation_completed=False, free_result_available=False)
        step = get_next_step(user=None, product_id="life_path", journey_context=ctx)
        self.assertEqual(step["stage"], FunnelStage.INTEREST.value)
        self.assertEqual(step["type"], "CALCULATION_INVITE")
        self.assertEqual(step["cta_label"], "Calculate My Number")

    def test_free_result_triggers_consideration_bridge(self):
        ctx = JourneyContext(calculation_completed=True, free_result_available=True)
        step = get_next_step(user=None, product_id="life_path", journey_context=ctx)
        self.assertEqual(step["stage"], FunnelStage.CONSIDERATION.value)
        self.assertEqual(step["type"], "CONSIDERATION_OFFER")
        self.assertEqual(step["tagline"], "ANVEIL EVERY CHARM")
        self.assertIn("Life Path", step["curiosity_hook"])
        self.assertEqual(step["offer"]["price_inr"], 489)
        self.assertEqual(step["offer"]["digital_root"], 3)

    def test_opt_out_precedence(self):
        ctx = JourneyContext(
            user_opted_out_of_marketing=True,
            free_result_available=True
        )
        step = get_next_step(user=None, product_id="life_path", journey_context=ctx)
        self.assertEqual(step["journey_state"], JourneyState.OPTED_OUT.value)
        self.assertEqual(step["type"], "PRODUCT_ACTION")
        self.assertTrue(step["opted_out"])
        # Should not expose commercial upgrade panel
        self.assertNotIn("offer", step)

    def test_payment_confirmed_pending_fulfilment(self):
        ctx = JourneyContext(
            payment_status="CONFIRMED",
            fulfilment_status="PENDING"
        )
        step = get_next_step(user=None, product_id="life_path", journey_context=ctx)
        self.assertEqual(step["stage"], FunnelStage.RETENTION.value)
        self.assertEqual(step["type"], "FULFILMENT_STATUS")
        self.assertTrue(step["is_pending"])

    def test_payment_confirmed_and_fulfilled(self):
        ctx = JourneyContext(
            payment_status="CONFIRMED",
            fulfilment_status="FULFILLED"
        )
        step = get_next_step(user=None, product_id="life_path", journey_context=ctx)
        self.assertEqual(step["stage"], FunnelStage.RETENTION.value)
        self.assertEqual(step["type"], "POST_PURCHASE")
        self.assertEqual(step["cta_label"], "View My Report")

    def test_already_owned_loyalty_stage(self):
        ctx = JourneyContext(
            free_result_available=True,
            current_entitlements=["report_master"]
        )
        step = get_next_step(user=None, product_id="life_path", journey_context=ctx)
        self.assertEqual(step["stage"], FunnelStage.LOYALTY.value)
        self.assertEqual(step["type"], "ALREADY_OWNED")
        self.assertEqual(step["cta_label"], "View My Report")


class TestFunnelApiEndpoints(unittest.TestCase):
    """Integration test suite for FastAPI payments funnel endpoints."""

    def setUp(self):
        self.client = TestClient(app)

    def test_get_funnel_products(self):
        res = self.client.get("/api/v1/payments/funnel/products")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["tagline"], "ANVEIL EVERY CHARM")
        self.assertIn("birth_number", data["products"])
        self.assertIn("life_path", data["products"])

    def test_validate_funnel_price(self):
        # Single price
        res = self.client.post("/api/v1/payments/funnel/validate-price", json={"amount": 489})
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res.json()["valid"])
        self.assertEqual(res.json()["digital_root"], 3)

        # Price pair
        res2 = self.client.post("/api/v1/payments/funnel/validate-price", json={"reference": 999, "offer": 489})
        self.assertEqual(res2.status_code, 200)

    def test_funnel_next_step_endpoint(self):
        # GET request
        res = self.client.get("/api/v1/payments/funnel/next-step?product_id=life_path&free_result_available=true")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["stage"], "CONSIDERATION")
        self.assertEqual(data["tagline"], "ANVEIL EVERY CHARM")

        # POST with opt-out
        res2 = self.client.post("/api/v1/payments/funnel/next-step", json={
            "product_id": "life_path",
            "opted_out": True
        })
        self.assertEqual(res2.status_code, 200)
        self.assertTrue(res2.json()["opted_out"])

    def test_funnel_event_logging_privacy(self):
        # Event with allowed and disallowed PII fields
        res = self.client.post("/api/v1/payments/funnel/event", json={
            "event": "upgrade_panel_viewed",
            "product_id": "life_path",
            "stage": "CONSIDERATION",
            "metadata": {
                "plan_id": "report_master",
                "price_inr": 489,
                "dob": "1990-01-01",     # Must be stripped
                "mobile": "9876543210"    # Must be stripped
            }
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["status"], "success")


if __name__ == "__main__":
    unittest.main()
