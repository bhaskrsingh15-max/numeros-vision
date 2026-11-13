"""
Integration tests for Logo Intelligence & Google Nano Banana API (/api/v1/logo).
Verifies complete customer workflow: intake -> approval -> generation -> validation -> status.
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app


class TestLogoAPI(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_logo_intake_success(self):
        """Intake classifies business, calculates numerology, and compiles initial DesignSpecification."""
        payload = {
            "business_name": "AURA PEAK",
            "business_activity": "High performance athletic footwear and marathon running shoes",
            "customer_segment": "marathon runners",
            "market": "global",
            "positioning": "endurance athletic luxury",
            "primary_color_preference": "#C9A227",
            "dpdp_consent": True,
        }
        resp = self.client.post("/api/v1/logo/intake", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("project_id", data)
        self.assertEqual(data["business_name"], "AURA PEAK")
        self.assertEqual(data["taxonomy"]["primary_category"], "athletic_footwear")
        self.assertIn("design_specification", data)

    def test_logo_intake_dpdp_consent_required(self):
        """Intake rejects request if statutory DPDP consent is missing."""
        payload = {
            "business_name": "AURA PEAK",
            "business_activity": "Footwear",
            "dpdp_consent": False,
        }
        resp = self.client.post("/api/v1/logo/intake", json=payload)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("DPDP consent required", resp.json()["detail"])

    def test_generation_approval_gate_enforcement(self):
        """Generating logo fails if customer has not explicitly approved the DesignSpecification."""
        # 1. Intake
        intake_resp = self.client.post("/api/v1/logo/intake", json={
            "business_name": "ZENITH MOTION",
            "business_activity": "Athletic sportswear and running apparel",
            "dpdp_consent": True,
        })
        project_id = intake_resp.json()["project_id"]

        # 2. Attempt generate without approval -> Expect 403 Forbidden!
        gen_resp = self.client.post("/api/v1/logo/generate", json={
            "project_id": project_id,
        })
        self.assertEqual(gen_resp.status_code, 403)
        self.assertIn("Customer must approve", gen_resp.json()["detail"])

    def test_full_customer_logo_workflow(self):
        """End-to-end workflow: intake -> approve -> generate -> status verification."""
        # Step 1: Intake
        intake_resp = self.client.post("/api/v1/logo/intake", json={
            "business_name": "SOLARIS DYNAMICS",
            "business_activity": "Clean energy systems and solar power hardware",
            "customer_segment": "commercial enterprises",
            "primary_color_preference": "#C9A227",
            "dpdp_consent": True,
        })
        self.assertEqual(intake_resp.status_code, 200)
        project_id = intake_resp.json()["project_id"]

        # Step 2: Customer approves wordmark and palette
        appr_resp = self.client.post("/api/v1/logo/approve", json={
            "project_id": project_id,
            "approved_wordmark": True,
            "approved_palette": True,
            "approved_direction": True,
        })
        self.assertEqual(appr_resp.status_code, 200)
        self.assertTrue(appr_resp.json()["ready_for_generation"])

        # Step 3: Customer triggers generation
        gen_resp = self.client.post("/api/v1/logo/generate", json={
            "project_id": project_id,
            "symbol_concept": "ascending_peak",
        })
        self.assertEqual(gen_resp.status_code, 200)
        gen_data = gen_resp.json()
        self.assertEqual(gen_data["status"], "COMPLETED")
        self.assertIn("vector_svg", gen_data)
        self.assertTrue(gen_data["validation_passed"])
        self.assertIn("SOLARIS DYNAMICS", gen_data["vector_svg"])
        job_id = gen_data["job_id"]

        # Step 4: Verify Job Status
        status_resp = self.client.get(f"/api/v1/logo/status/{job_id}")
        self.assertEqual(status_resp.status_code, 200)
        status_data = status_resp.json()
        self.assertEqual(status_data["status"], "COMPLETED")
        self.assertIn("vector_svg", status_data)
        self.assertIn("validation_gates", status_data)


if __name__ == "__main__":
    unittest.main()
