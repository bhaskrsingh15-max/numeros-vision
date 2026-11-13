"""
Integration tests for Business Alignment and Logo Studio Suite.
Verifies all route aliases, calculation mechanics, archetype mapping, and end-to-end pipeline.
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app


class TestBusinessAlignmentAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_routes_availability(self):
        """Verifies that all Specialized Business & Logo Studio route aliases return 200 OK."""
        routes = [
            "/tools/business-alignment",
            "/tools/business-alignment/",
            "/tools/business-direction",
            "/tools/business-direction/",
            "/tools/logo-intelligence",
            "/tools/logo-intelligence/",
            "/tools/logo-studio",
            "/tools/logo-studio/",
            "/logo-studio",
            "/logo-studio/",
            "/calculators/logo-studio",
            "/calculators/business-alignment",
        ]
        for r in routes:
            with self.subTest(route=r):
                resp = self.client.get(r)
                self.assertEqual(resp.status_code, 200, f"Route {r} failed with {resp.status_code}")

    def test_startup_evaluate_endpoint(self):
        """Tests startup evaluation with commercial viability, Chaldean calculations, and founder Driver/Conductor."""
        payload = {
            "founder_name": "Rohan Verma",
            "skills": ["software_engineering", "fintech"],
            "experience_years": 7,
            "capital_band": "growth_50k_250k",
            "location": "Delhi NCR",
            "risk_tolerance": "moderate",
            "operating_preference": "digital_remote",
            "founder_dob": "1988-11-23",
            "idea_name": "FinShield Pay",
            "activity_description": "Digital payment infrastructure and fraud prevention software",
            "revenue_model": "b2b_retainer",
            "customer_segment": "e-commerce merchants",
            "delivery_channel": "cloud_api",
            "estimated_startup_capital_required": "seed_10k_50k",
        }
        resp = self.client.post("/api/v1/business/startup-evaluate", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["business_name"], "FinShield Pay")
        self.assertTrue(data["commercial_viability"]["skill_match"])
        self.assertTrue(data["commercial_viability"]["capital_sufficient"])
        self.assertIn("mandatory_disclaimer", data)
        self.assertIn("Evidence Notice", data["mandatory_disclaimer"])

        # Check deterministic calculations
        trad = data["traditional_alignment"]
        self.assertGreater(trad["name_compound"], 0)
        self.assertGreater(trad["name_single"], 0)
        self.assertGreater(len(trad["candidate_archetypes"]), 0)
        self.assertTrue(any("Driver" in r for r in trad["reasons"]))

    def test_existing_diagnose_endpoint(self):
        """Tests existing business diagnostic with fixed vs changeable factors and brand harmony."""
        payload = {
            "legal_name": "Zenith Retail Ventures LLP",
            "trading_name": "Zenith Organic Superstore",
            "products_services": "Organic grocery and wellness merchandise",
            "current_constraints": ["10-year store lease in South Delhi", "Organic import license"],
            "performance_challenges": ["High inventory spoilage", "Customer footfall reduced 15%"],
        }
        resp = self.client.post("/api/v1/business/existing-diagnose", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["legal_name"], "Zenith Retail Ventures LLP")
        self.assertTrue(any("lease" in f.lower() for f in data["fixed_vs_changeable"]["fixed_constraints"]))
        self.assertTrue(len(data["practical_improvements_first"]) > 0)
        self.assertTrue(len(data["traditional_remedies"]) > 0)
        self.assertIn("Statutory Disclosure", data["statutory_notice"])

        # Check brand adjustments
        b_adj = data["brand_and_name_adjustments"]
        self.assertGreater(b_adj["legal_name_compound"], 0)
        self.assertGreater(b_adj["trading_name_compound"], 0)
        self.assertIn("Trading name compound", b_adj["trading_name_recommendation"])

    def test_logo_studio_full_pipeline(self):
        """Tests full Logo Studio end-to-end pipeline: Intake -> Approval -> Generation."""
        # 1. Intake
        intake_payload = {
            "business_name": "PulseFlow Cloud",
            "business_activity": "Cloud-based workflow automation and operational scheduling software for digital remote teams.",
            "customer_segment": "Enterprise B2B",
            "primary_color_preference": "#C9A227",
            "dpdp_consent": True,
        }
        res_intake = self.client.post("/api/v1/logo/intake", json=intake_payload)
        self.assertEqual(res_intake.status_code, 200)
        intake_data = res_intake.json()
        project_id = intake_data["project_id"]
        self.assertTrue(project_id.startswith("proj_"))
        num = intake_data["name_numerology"]
        self.assertGreater(num.get("compound_sum", num.get("compound_number", 0)), 0)

        # 2. Approval
        appr_payload = {
            "project_id": project_id,
            "approved_wordmark": True,
            "approved_palette": True,
            "approved_direction": True,
        }
        res_appr = self.client.post("/api/v1/logo/approve", json=appr_payload)
        self.assertEqual(res_appr.status_code, 200)
        appr_data = res_appr.json()
        self.assertTrue(appr_data["ready_for_generation"])

        # 3. Generation
        gen_payload = {
            "project_id": project_id,
            "symbol_concept": "ascending_peak",
        }
        res_gen = self.client.post("/api/v1/logo/generate", json=gen_payload)
        self.assertEqual(res_gen.status_code, 200)
        gen_data = res_gen.json()
        self.assertEqual(gen_data["status"], "COMPLETED")
        self.assertIn("<svg", gen_data["vector_svg"])
        self.assertTrue(gen_data["validation_report"]["ocr_wordmark_match"])
        self.assertGreaterEqual(gen_data["validation_report"]["contrast_ratio"], 4.5)


if __name__ == "__main__":
    unittest.main()
