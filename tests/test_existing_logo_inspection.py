"""
Unit tests for Existing Logo Inspection & Asset Lifecycle (/api/v1/logo/analyze-existing, /download, /project delete).
Verifies measurable checks vs traditional interpretation separation, SVG download, and DPDP deletion.
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.services.vector_renderer import VectorRenderer


class TestExistingLogoInspection(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_analyze_existing_svg(self):
        """Inspects existing SVG logo and separates measurable checks from traditional interpretations."""
        svg = VectorRenderer.render_svg(
            exact_wordmark="OLYMPIA RUN",
            symbol_type="ascending_peak",
            primary_hex="#523E28",
            bg_hex="#FFFDF7",
        )
        resp = self.client.post("/api/v1/logo/analyze-existing", json={"svg_content": svg})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        # Measurable checks
        measurable = data["measurable_design_checks"]
        self.assertEqual(measurable["format"], "image/svg+xml")
        self.assertTrue(measurable["is_vector"])
        self.assertIn("OLYMPIA RUN", measurable["extracted_text"])
        self.assertGreater(measurable["contrast_ratio"], 2.0)

        # Traditional interpretations
        symbolic = data["traditional_symbolic_interpretations"]
        self.assertTrue(len(symbolic) > 0)
        self.assertEqual(symbolic[0]["evidence_status"], "TRADITIONAL_HYPOTHESIS")

        # Objective distinction notice
        self.assertIn("Objective Distinction", data["mandatory_disclaimer"])

    def test_download_svg_and_delete_project(self):
        """Workflow: Intake -> Approve -> Generate -> Download SVG -> Purge Project Data."""
        # 1. Intake
        intake_resp = self.client.post("/api/v1/logo/intake", json={
            "business_name": "VALIANT TECH",
            "business_activity": "Enterprise cybersecurity software and cloud protection",
            "dpdp_consent": True,
        })
        project_id = intake_resp.json()["project_id"]

        # 2. Approve
        self.client.post("/api/v1/logo/approve", json={
            "project_id": project_id,
            "approved_wordmark": True,
            "approved_palette": True,
            "approved_direction": True,
        })

        # 3. Generate
        gen_resp = self.client.post("/api/v1/logo/generate", json={"project_id": project_id})
        job_id = gen_resp.json()["job_id"]

        # 4. Download SVG
        dl_resp = self.client.get(f"/api/v1/logo/download/{job_id}/svg")
        self.assertEqual(dl_resp.status_code, 200)
        self.assertEqual(dl_resp.headers["content-type"], "image/svg+xml")
        self.assertIn("VALIANT TECH", dl_resp.text)

        # 5. Download JSON Spec
        json_resp = self.client.get(f"/api/v1/logo/download/{job_id}/json")
        self.assertEqual(json_resp.status_code, 200)
        self.assertIn("application/json", json_resp.headers["content-type"])

        # 6. Delete project
        del_resp = self.client.delete(f"/api/v1/logo/project/{project_id}")
        self.assertEqual(del_resp.status_code, 200)
        self.assertEqual(del_resp.json()["status"], "DELETED")

        # Verify job no longer accessible
        status_resp = self.client.get(f"/api/v1/logo/status/{job_id}")
        self.assertEqual(status_resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
