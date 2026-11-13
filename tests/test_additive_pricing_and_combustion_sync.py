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

    # ── 1. DIGIT ROOT POLICY VERIFICATION ─────────────────────────────────────

    def test_all_18_screenshot_reports_digit_roots(self):
        """Verify that all 18 screenshot-based reports have list & offer digit roots in {1, 3, 5, 6}."""
        reports_18 = [
            # Love and Marriage
            "report_love_style", "report_marriage", "report_ideal_partner",
            "report_love_or_arrange", "report_spouse", "report_in_laws",
            # Money
            "report_billionaire_potential", "report_wealth",
            # Work
            "report_career", "report_business", "report_job_or_business",
            "report_govt_job", "report_first_job", "report_job_search",
            # Self and Growth
            "report_intelligence", "report_life_guidance", "report_personality",
            "report_education",
        ]

        for rep_id in reports_18:
            with self.subTest(report_id=rep_id):
                self.assertIn(rep_id, PLANS, f"Report {rep_id} missing from PLANS")
                plan = PLANS[rep_id]
                offer = plan["amount_inr"]
                list_price = plan.get("original_price_inr", offer)

                # Digit roots
                offer_root = digit_root(offer)
                list_root = digit_root(list_price)
                self.assertIn(offer_root, DEFAULT_ALLOWED_ROOTS, f"{rep_id} offer {offer} root {offer_root} not allowed")
                self.assertIn(list_root, DEFAULT_ALLOWED_ROOTS, f"{rep_id} list {list_price} root {list_root} not allowed")

                # Genuine discount assertion
                self.assertLess(offer, list_price, f"{rep_id} offer must be strictly less than list price")

                # Validate price pair utility
                val_res = validate_price_pair(list_price, offer)
                self.assertTrue(val_res["valid"], f"Validation failed for {rep_id}: {val_res}")

    def test_all_8_report_bundles_digit_roots_and_savings(self):
        """Verify all 8 bundles conform to digit roots and offer real savings."""
        bundles_8 = [
            "bundle_love_compatibility", "bundle_marriage_family",
            "bundle_career_starter", "bundle_career_decision",
            "bundle_money_wealth", "bundle_self_discovery",
            "bundle_learning_growth", "bundle_complete_personal_insight"
        ]

        for b_id in bundles_8:
            with self.subTest(bundle_id=b_id):
                self.assertIn(b_id, PLANS, f"Bundle {b_id} missing from PLANS")
                bundle = PLANS[b_id]
                offer = bundle["amount_inr"]
                list_price = bundle.get("original_price_inr", offer)

                # Roots
                offer_root = digit_root(offer)
                list_root = digit_root(list_price)
                self.assertIn(offer_root, DEFAULT_ALLOWED_ROOTS, f"{b_id} offer {offer} root {offer_root} not allowed")
                self.assertIn(list_root, DEFAULT_ALLOWED_ROOTS, f"{b_id} list {list_price} root {list_root} not allowed")

                # Savings
                self.assertLess(offer, list_price, f"{b_id} offer must be less than list")
                self.assertGreater(bundle.get("original_price_inr", 0) - offer, 0)

    def test_all_6_charm_ai_packages_digit_roots(self):
        """Verify all 6 Charm AI packages conform to digit root rules."""
        charm_6 = [
            "charm_quick_insight", "charm_focused_reading",
            "charm_consensus_reading", "charm_personal_blueprint",
            "charm_family_compatibility", "charm_career_business_direction"
        ]

        for c_id in charm_6:
            with self.subTest(charm_id=c_id):
                self.assertIn(c_id, PLANS, f"Charm package {c_id} missing from PLANS")
                pkg = PLANS[c_id]
                offer = pkg["amount_inr"]
                list_price = pkg.get("original_price_inr", offer)

                # Roots
                offer_root = digit_root(offer)
                list_root = digit_root(list_price)
                self.assertIn(offer_root, DEFAULT_ALLOWED_ROOTS, f"{c_id} offer {offer} root {offer_root} not allowed")
                self.assertIn(list_root, DEFAULT_ALLOWED_ROOTS, f"{c_id} list {list_price} root {list_root} not allowed")
                self.assertLess(offer, list_price)

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
        """Test GET /api/v1/payments/plans exposes all plans with enriched metadata."""
        resp = self.client.get("/api/v1/payments/plans")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data.get("success"))
        plans = data.get("plans", {})

        # Test sample reports from all 4 categories exist
        self.assertIn("report_love_style", plans)
        self.assertIn("report_billionaire_potential", plans)
        self.assertIn("report_career", plans)
        self.assertIn("report_intelligence", plans)

        # Test bundle and charm packages exist
        self.assertIn("bundle_love_compatibility", plans)
        self.assertIn("charm_quick_insight", plans)

        # Check metadata fields
        love_plan = plans["report_love_style"]
        self.assertEqual(love_plan["category_group"], "Love and Marriage")
        self.assertEqual(love_plan["pricing_personality"], 6)
        self.assertEqual(love_plan["amount_inr"], 399)
        self.assertEqual(love_plan["offer_price_root"], 3)
        self.assertEqual(love_plan["list_price_root"], 6)

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
                self.assertIn("Love Style &amp; Romance Profile", resp.text)
                self.assertIn("nv-sticky-reports-bar", resp.text)
                self.assertIn("continue-exploration", resp.text)

    def test_bundle_inclusions_completeness(self):
        """Verify each bundle in PLANS specifies valid included_reports that exist in PLANS."""
        for k, v in PLANS.items():
            if v.get("category") == "bundle":
                inclusions = v.get("included_reports", [])
                self.assertGreater(len(inclusions), 0, f"Bundle {k} has empty included_reports")
                for rep in inclusions:
                    self.assertIn(rep, PLANS, f"Bundle {k} references non-existent report {rep}")


if __name__ == "__main__":
    unittest.main()
