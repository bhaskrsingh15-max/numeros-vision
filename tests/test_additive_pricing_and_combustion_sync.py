"""
Unit Tests for Additive Pricing Catalogue, Bundle Savings, and Deterministic Planetary Combustion
Numeros Vision — ANVEIL EVERY CHARM
"""

import unittest
from datetime import datetime, timezone
from fastapi.testclient import TestClient

from app.main import app
from app.engine.funnel_service import (
    digit_root,
    validate_price_pair,
    PRODUCT_FUNNEL_CATALOG,
    DEFAULT_ALLOWED_ROOTS,
)
from app.api.payments import PLANS
from app.charm.charts.fact_provider import (
    calculate_angular_separation,
    evaluate_planetary_combustion,
    get_chart_facts,
    COMBUSTION_LIMITS,
)


class TestAdditivePricingAndCombustionSync(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    # ── 1. DIGIT ROOT POLICY VERIFICATION (SINGLE SOURCE: packs.json) ────────

    def test_core_reports_digit_roots_and_waitlist_parity(self):
        """Verify active core reports in PLANS (from packs.json) obey digit roots {1, 3, 5, 6}."""
        import os
        from unittest.mock import patch
        from app.config.pricing_config import build_plans_from_packs_json

        with patch.dict(os.environ, {"ENVIRONMENT": "preview", "NV_FORCE_LAUNCH_MODE": "1"}, clear=False):
            plans = build_plans_from_packs_json()
            basic = plans["report_basic"]
            offer = basic["amount_inr"]
            list_price = basic["original_price_inr"]
            self.assertEqual(offer, 199)
            self.assertEqual(list_price, 399)
            self.assertIn(digit_root(offer), DEFAULT_ALLOWED_ROOTS)
            self.assertIn(digit_root(list_price), DEFAULT_ALLOWED_ROOTS)
            self.assertLess(offer, list_price)
            self.assertTrue(validate_price_pair(list_price, offer)["valid"])

            for wl_id in ("report_advanced", "report_premium", "planner_2027"):
                self.assertIn(wl_id, plans)
                self.assertIsNone(plans[wl_id]["amount_inr"])
                self.assertTrue(plans[wl_id]["waitlist_only"])

    def test_report_bundles_waitlist_parity(self):
        """Verify all bundles in PLANS match packs.json coming_soon / null price state."""
        for b_id in ("starter_bundle", "discovery_bundle", "comprehensive_bundle"):
            self.assertIn(b_id, PLANS)
            self.assertIsNone(PLANS[b_id]["amount_inr"])
            self.assertTrue(PLANS[b_id]["waitlist_only"])

    def test_charm_ai_packages_digit_roots(self):
        """Verify active paid Charm AI pack in PLANS conforms to digit root rules."""
        self.assertIn("charm_single", PLANS)
        pkg = PLANS["charm_single"]
        self.assertEqual(pkg["amount_inr"], 199)
        self.assertIn(digit_root(pkg["amount_inr"]), DEFAULT_ALLOWED_ROOTS)
        self.assertEqual(PLANS["charm_free"]["amount_inr"], 0)
        self.assertIsNone(PLANS["charm_multi"]["amount_inr"])
        self.assertIsNone(PLANS["charm_extended"]["amount_inr"])

    # ── 2. DETERMINISTIC PLANETARY COMBUSTION ─────────────────────────────────

    def test_calculate_angular_separation_circular_wrapping(self):
        """Test circular 360-degree shortest arc distance."""
        # 10 degrees and 20 degrees -> 10 degrees
        self.assertAlmostEqual(calculate_angular_separation(10.0, 20.0), 10.0)
        # 355 degrees and 5 degrees -> 10 degrees (across 0 deg Aries)
        self.assertAlmostEqual(calculate_angular_separation(355.0, 5.0), 10.0)
        # 180 degrees opposite -> 180 degrees
        self.assertAlmostEqual(calculate_angular_separation(0.0, 180.0), 180.0)
        # 10 degrees and 200 degrees -> 170 degrees
        self.assertAlmostEqual(calculate_angular_separation(10.0, 200.0), 170.0)

    def test_combustion_thresholds_all_planets(self):
        """Test classical angular thresholds for direct & retrograde planets."""
        sun_deg = 180.0  # 0 deg Libra

        # 1. Moon (12 deg limit)
        c_moon_combust = evaluate_planetary_combustion("Moon", 188.0, sun_deg)  # 8 deg sep
        self.assertTrue(c_moon_combust["is_combust"])
        self.assertEqual(c_moon_combust["status"], "COMBUST (Astangata)")

        c_moon_clear = evaluate_planetary_combustion("Moon", 195.0, sun_deg)  # 15 deg sep
        self.assertFalse(c_moon_clear["is_combust"])
        self.assertEqual(c_moon_clear["status"], "CLEAR (Udaya)")

        # 2. Mars (17 deg limit)
        c_mars_combust = evaluate_planetary_combustion("Mars", 196.0, sun_deg)  # 16 deg sep
        self.assertTrue(c_mars_combust["is_combust"])

        c_mars_clear = evaluate_planetary_combustion("Mars", 198.0, sun_deg)  # 18 deg sep
        self.assertFalse(c_mars_clear["is_combust"])

        # 3. Mercury: Direct (14 deg) vs Retrograde (12 deg)
        c_merc_dir_combust = evaluate_planetary_combustion("Mercury", 193.0, sun_deg, is_retrograde=False)  # 13 deg
        self.assertTrue(c_merc_dir_combust["is_combust"])

        c_merc_dir_clear = evaluate_planetary_combustion("Mercury", 195.0, sun_deg, is_retrograde=False)  # 15 deg
        self.assertFalse(c_merc_dir_clear["is_combust"])

        c_merc_ret_combust = evaluate_planetary_combustion("Mercury", 191.0, sun_deg, is_retrograde=True)  # 11 deg
        self.assertTrue(c_merc_ret_combust["is_combust"])

        c_merc_ret_clear = evaluate_planetary_combustion("Mercury", 193.0, sun_deg, is_retrograde=True)  # 13 deg (clear for ret!)
        self.assertFalse(c_merc_ret_clear["is_combust"])

        # 4. Jupiter (11 deg limit)
        c_jup_combust = evaluate_planetary_combustion("Jupiter", 190.0, sun_deg)  # 10 deg
        self.assertTrue(c_jup_combust["is_combust"])

        c_jup_clear = evaluate_planetary_combustion("Jupiter", 192.0, sun_deg)  # 12 deg
        self.assertFalse(c_jup_clear["is_combust"])

        # 5. Venus: Direct (10 deg) vs Retrograde (8 deg)
        c_ven_dir_combust = evaluate_planetary_combustion("Venus", 189.0, sun_deg, is_retrograde=False)  # 9 deg
        self.assertTrue(c_ven_dir_combust["is_combust"])

        c_ven_ret_combust = evaluate_planetary_combustion("Venus", 187.0, sun_deg, is_retrograde=True)  # 7 deg
        self.assertTrue(c_ven_ret_combust["is_combust"])

        c_ven_ret_clear = evaluate_planetary_combustion("Venus", 189.0, sun_deg, is_retrograde=True)  # 9 deg (clear for ret!)
        self.assertFalse(c_ven_ret_clear["is_combust"])

        # 6. Saturn (15 deg limit)
        c_sat_combust = evaluate_planetary_combustion("Saturn", 194.0, sun_deg)  # 14 deg
        self.assertTrue(c_sat_combust["is_combust"])

        c_sat_clear = evaluate_planetary_combustion("Saturn", 196.0, sun_deg)  # 16 deg
        self.assertFalse(c_sat_clear["is_combust"])

        # 7. Rahu / Ketu: Exempt
        c_rahu = evaluate_planetary_combustion("Rahu", 180.5, sun_deg)
        self.assertFalse(c_rahu["is_combust"])
        self.assertEqual(c_rahu["status"], "EXEMPT")

        # 8. Deep Combustion (Paramastangata within 1 deg)
        c_deep = evaluate_planetary_combustion("Mars", 180.6, sun_deg)  # 0.6 deg sep
        self.assertTrue(c_deep["is_combust"])
        self.assertTrue(c_deep["deep_combustion"])

    def test_get_chart_facts_combustion_enrichment(self):
        """Test that get_chart_facts automatically includes combustion audit."""
        facts = get_chart_facts(target_date="2026-10-15", city="New Delhi")
        self.assertIn("combustion_audit", facts)
        self.assertIn("planetary_positions", facts)
        
        # Verify every planet object has a combustion breakdown
        for p in facts["planetary_positions"].values():
            self.assertIn("combustion", p)
            self.assertIn("is_combust", p["combustion"])

    # ── 3. API ENDPOINTS INTEGRATION ──────────────────────────────────────────

    def test_api_plans_endpoint(self):
        """Test GET /api/v1/payments/plans exposes canonical packs.json plans with enriched metadata."""
        resp = self.client.get("/api/v1/payments/plans")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get("success"))
        plans = data.get("plans", {})

        for canonical_id in (
            "report_basic",
            "report_advanced",
            "report_premium",
            "planner_2027",
            "starter_bundle",
            "discovery_bundle",
            "comprehensive_bundle",
            "charm_free",
            "charm_single",
        ):
            self.assertIn(canonical_id, plans)

        charm_plan = plans["charm_single"]
        self.assertEqual(charm_plan["amount_inr"], 199)
        self.assertEqual(charm_plan["offer_price_root"], 1)
        self.assertEqual(charm_plan["questions_count"], 5)

    def test_api_funnel_products_endpoint(self):
        """Test GET /api/v1/payments/funnel/products includes full funnel hooks."""
        resp = self.client.get("/api/v1/payments/funnel/products")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data.get("status"), "success")
        self.assertEqual(data.get("tagline"), "ANVEIL EVERY CHARM")
        products = data.get("products", {})

        self.assertIn("report_marriage", products)
        self.assertIn("bundle_career_starter", products)
        self.assertIn("charm_consensus_reading", products)

        prod = products["report_marriage"]
        self.assertIn("awareness_hook", prod)
        self.assertIn("curiosity_hook", prod)
        self.assertIn("value_bridge", prod)
        self.assertIn("primary_cta", prod)
        self.assertIn("deliverables", prod)

    def test_reports_catalogue_html_routes(self):
        """Test GET /reports/ and /reports_catalogue/ render HTML catalogue cleanly."""
        for path in ("/reports/", "/reports_catalogue/"):
            with self.subTest(route=path):
                resp = self.client.get(path)
                self.assertEqual(resp.status_code, 200)
                self.assertIn("text/html", resp.headers.get("content-type", ""))
                self.assertIn("NUMEROS VISION", resp.text)
                self.assertIn("ANVEIL EVERY CHARM", resp.text)
                self.assertIn("Anveil my alignments", resp.text)

    def test_bundle_deliverables_completeness(self):
        """Verify each bundle in PLANS (from packs.json) specifies non-empty deliverables and coming_soon status."""
        for k, v in PLANS.items():
            if v.get("category") == "bundle":
                deliverables = v.get("deliverables", [])
                self.assertGreater(len(deliverables), 0, f"Bundle {k} has empty deliverables")
                self.assertTrue(v.get("waitlist_only"), f"Bundle {k} must be waitlisted per packs.json")
                self.assertIsNone(v.get("amount_inr"), f"Bundle {k} must have null price per packs.json")


if __name__ == "__main__":
    unittest.main()
