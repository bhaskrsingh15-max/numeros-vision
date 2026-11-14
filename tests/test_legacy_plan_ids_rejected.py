"""
Verification Suite: Legacy Plan IDs Rejected at create-order (Python FastAPI)
=============================================================================
Proves that retired plan IDs:
  - report_essential, report_master, report_divine, master, divine
  - starter_5q, ai_starter_5q, ai_report_combo
  - growth_10q, ai_growth_15q, ai_power_35q, complete_report
are rejected at both POST /api/v1/payments/create-order and POST /api/create-order
with HTTP 400 (4xx) and zero Razorpay SDK calls.
"""

import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app
from app.config.pricing_config import resolve_sku_price


LEGACY_PLAN_IDS = (
    "report_essential",
    "report_master",
    "report_divine",
    "master",
    "divine",
    "starter_5q",
    "ai_starter_5q",
    "ai_report_combo",
    "growth_10q",
    "ai_growth_15q",
    "ai_power_35q",
    "complete_report",
)


class TestLegacyPlanIdsRejected(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_resolve_sku_price_returns_none_for_legacy_ids(self):
        for legacy_id in LEGACY_PLAN_IDS:
            with self.subTest(legacy_id=legacy_id):
                self.assertIsNone(resolve_sku_price(legacy_id))

    def test_create_order_rejects_legacy_plan_ids_with_400_and_zero_gateway_calls(self):
        with patch("razorpay.Client") as mock_rzp_cls:
            for legacy_id in LEGACY_PLAN_IDS:
                for endpoint in ("/api/v1/payments/create-order", "/api/create-order"):
                    with self.subTest(legacy_id=legacy_id, endpoint=endpoint):
                        resp = self.client.post(
                            endpoint,
                            json={
                                "plan": legacy_id,
                                "name": "Legacy Test User",
                                "email": "legacy@example.com",
                                "mobile": "9876543210",
                            },
                        )
                        self.assertEqual(
                            resp.status_code,
                            400,
                            f"Expected 400 for {legacy_id} on {endpoint}, got {resp.status_code}",
                        )
                        body = resp.json()
                        self.assertFalse(body.get("success", True))
                        self.assertEqual(body.get("code"), "LEGACY_PLAN_ID_REJECTED")

            mock_rzp_cls.assert_not_called()


if __name__ == "__main__":
    unittest.main()
