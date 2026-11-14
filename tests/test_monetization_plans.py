import json
import os
import sys
import unittest
from unittest.mock import patch

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app
from app.api.payments import PLANS
from app.config.pricing_config import (
    PACKS_JSON_PATH,
    build_plans_from_packs_json,
    load_packs_json,
    resolve_sku_price,
)


class TestMonetizationPlans(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.packs = load_packs_json()

    def _expected_pack_ids(self):
        expected = set()
        for bucket in ("core_reports", "annual_planners", "bundles", "charm_ai"):
            expected.update((self.packs.get(bucket) or {}).keys())
        return expected

    def test_single_price_source_matches_packs_json(self):
        """Python pricing_config & payments.PLANS read app/config/packs.json with zero second table."""
        expected_ids = self._expected_pack_ids()
        self.assertEqual(set(PLANS.keys()), expected_ids)

        # Retired / second-table SKUs must NOT appear in PLANS
        for retired_id in (
            "report_essential",
            "report_master",
            "report_divine",
            "starter_5q",
            "ai_starter_5q",
            "ai_report_combo",
            "advisory_brand_logo",
            "b2b_consultant_pro",
            "report_union_master",
            "personal_consult",
        ):
            self.assertNotIn(retired_id, PLANS)

        # Regular mode (no launch window set): report_basic = mrp_inr (399), charm_single = 199
        with patch.dict(os.environ, {"ENVIRONMENT": "production", "NV_LAUNCH_STARTS_AT": "", "NV_LAUNCH_ENDS_AT": ""}, clear=False):
            os.environ.pop("NV_FORCE_LAUNCH_MODE", None)
            reg_plans = build_plans_from_packs_json()
            self.assertEqual(reg_plans["report_basic"]["amount_inr"], self.packs["core_reports"]["report_basic"]["mrp_inr"])
            self.assertEqual(reg_plans["report_basic"]["amount_paise"], self.packs["core_reports"]["report_basic"]["mrp_paise"])
            self.assertEqual(reg_plans["charm_single"]["amount_inr"], self.packs["charm_ai"]["charm_single"]["price_inr"])
            self.assertEqual(reg_plans["charm_single"]["amount_paise"], self.packs["charm_ai"]["charm_single"]["amount_paise"])
            for wl_id in ("report_advanced", "report_premium", "planner_2027"):
                self.assertIsNone(reg_plans[wl_id]["amount_inr"])
                self.assertIsNone(reg_plans[wl_id]["amount_paise"])
                self.assertTrue(reg_plans[wl_id]["waitlist_only"])

        # Preview launch mode: report_basic = price_inr (199) with struck_mrp_inr (399)
        with patch.dict(os.environ, {"ENVIRONMENT": "preview", "NV_FORCE_LAUNCH_MODE": "1"}, clear=False):
            launch_plans = build_plans_from_packs_json()
            self.assertEqual(launch_plans["report_basic"]["amount_inr"], self.packs["core_reports"]["report_basic"]["price_inr"])
            self.assertEqual(launch_plans["report_basic"]["amount_paise"], self.packs["core_reports"]["report_basic"]["amount_paise"])
            self.assertEqual(launch_plans["report_basic"]["struck_mrp_inr"], self.packs["core_reports"]["report_basic"]["mrp_inr"])
            self.assertEqual(resolve_sku_price("charm_single")["amount_paise"], 19900)

    def test_get_plans_api_endpoint(self):
        resp = self.client.get("/api/v1/payments/plans")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get("success"))
        plans = data.get("plans", {})
        self.assertEqual(set(plans.keys()), self._expected_pack_ids())
        self.assertEqual(plans["charm_single"]["amount_inr"], 199)
        self.assertIsNone(plans["report_advanced"]["amount_inr"])
        self.assertIsNone(plans["report_premium"]["amount_inr"])
        self.assertIsNone(plans["planner_2027"]["amount_inr"])

    def test_html_contains_recommended_packages(self):
        static_dir = os.path.join(os.path.dirname(__file__), "..", "app", "static")
        with open(os.path.join(static_dir, "index.html"), "r", encoding="utf-8") as f:
            index_html = f.read()
        with open(os.path.join(static_dir, "pricing.html"), "r", encoding="utf-8") as f:
            pricing_html = f.read()

        self.assertIn("See my report options", index_html)
        self.assertIn("navigateToReportOptions('home')", index_html)
        self.assertIn("/pricing/#charm-ai", index_html)

        self.assertIn("Anveil every charm", pricing_html)
        self.assertIn("Anveil my glowing charms", pricing_html)
        self.assertIn("Anveil my alignments", pricing_html)
        self.assertIn("₹399", pricing_html)
        self.assertIn("Coming soon, notify me", pricing_html)


if __name__ == "__main__":
    unittest.main()
