import sys
import os
import unittest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app
from app.api.payments import PLANS

class TestMonetizationPlans(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_all_monetization_tiers_exist(self):
        # 1. Numerology Reports
        self.assertIn("report_essential", PLANS)
        self.assertIn("report_master", PLANS)
        self.assertIn("report_divine", PLANS)
        self.assertEqual(PLANS["report_essential"]["amount_inr"], 199)
        self.assertEqual(PLANS["report_master"]["amount_inr"], 510)
        self.assertEqual(PLANS["report_divine"]["amount_inr"], 1050)

        # 2. AI Question Credits & Subscriptions
        self.assertIn("ai_starter_5q", PLANS)
        self.assertIn("ai_growth_15q", PLANS)
        self.assertIn("ai_power_35q", PLANS)
        self.assertIn("sub_monthly", PLANS)
        self.assertIn("sub_annual", PLANS)
        self.assertEqual(PLANS["ai_starter_5q"]["amount_inr"], 95)
        self.assertEqual(PLANS["sub_monthly"]["amount_inr"], 149)
        self.assertEqual(PLANS["sub_annual"]["amount_inr"], 999)

        # 3. AI + Report Combo
        self.assertIn("ai_report_combo", PLANS)
        self.assertEqual(PLANS["ai_report_combo"]["amount_inr"], 699)

        # 4. Personal & Business Advisories
        self.assertIn("advisory_personal_name", PLANS)
        self.assertIn("advisory_business_name", PLANS)
        self.assertIn("advisory_brand_logo", PLANS)
        self.assertEqual(PLANS["advisory_personal_name"]["amount_inr"], 1499)
        self.assertEqual(PLANS["advisory_business_name"]["amount_inr"], 5999)
        self.assertEqual(PLANS["advisory_brand_logo"]["amount_inr"], 9999)

        # 5. B2B SaaS Plans
        self.assertIn("b2b_consultant_pro", PLANS)
        self.assertIn("b2b_platform_growth", PLANS)
        self.assertEqual(PLANS["b2b_consultant_pro"]["amount_inr"], 2499)
        self.assertEqual(PLANS["b2b_platform_growth"]["amount_inr"], 9999)

        # 6. Life Relationship Harmonic Packages (Harmonic Roots 1, 3, 5, 6)
        self.assertIn("report_union_tripwire", PLANS)
        self.assertEqual(PLANS["report_union_tripwire"]["amount_inr"], 105)
        self.assertEqual(PLANS["report_union_master"]["amount_inr"], 510)
        self.assertEqual(PLANS["report_union_sovereign"]["amount_inr"], 5100)
        self.assertEqual(PLANS["report_commerce_tripwire"]["amount_inr"], 149)
        self.assertEqual(PLANS["report_commerce_master"]["amount_inr"], 599)
        self.assertEqual(PLANS["report_commerce_sovereign"]["amount_inr"], 5999)
        self.assertEqual(PLANS["personal_consult"]["amount_inr"], 11400)

    def test_get_plans_api_endpoint(self):
        resp = self.client.get("/api/v1/payments/plans")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get("success"))
        plans = data.get("plans", {})
        self.assertIn("report_master", plans)
        self.assertIn("ai_report_combo", plans)
        self.assertIn("report_union_master", plans)
        self.assertIn("report_commerce_sovereign", plans)
        self.assertIn("advisory_brand_logo", plans)
        self.assertIn("b2b_consultant_pro", plans)

    def test_html_contains_recommended_packages(self):
        import os
        static_dir = os.path.join(os.path.dirname(__file__), "..", "app", "static")
        with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
            index_html = f.read()
        with open(os.path.join(static_dir, "pricing.html"), "r", encoding="utf-8") as f:
            pricing_html = f.read()

        # Homepage maintains single-CTA post-calculator funnel into /your-reading/ and Charm AI pass link
        self.assertIn("See my report options", index_html)
        self.assertIn("navigateToReportOptions('home')", index_html)
        self.assertIn("/pricing/#charm-ai", index_html)

        # Pricing & ladder surface canonical Anveil packages (high-to-low with waitlist higher tiers & Basic ₹399 default)
        self.assertIn("Anveil every charm", pricing_html)
        self.assertIn("Anveil my glowing charms", pricing_html)
        self.assertIn("Anveil my alignments", pricing_html)
        self.assertIn("₹399", pricing_html)
        self.assertIn("Coming soon, notify me", pricing_html)

if __name__ == "__main__":
    unittest.main()
