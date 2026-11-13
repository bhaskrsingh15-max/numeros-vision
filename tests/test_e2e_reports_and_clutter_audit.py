"""
Integration test for end-to-end report delivery, flexible request validation,
and deterministic Lo Shu grid plane verification.
"""
import unittest
from app.api.reports_delivery import ReportPdfRequest, ReportCalculateRequest, generate_pdf_endpoint, calculate_report_preview
from app.engine.lo_shu import analyze_lo_shu_grid, PLANES
from app.config.pricing_config import REPORT_TIERS, SUPPORTED_REPORT_TOPICS

class TestE2EReportsAndAudit(unittest.TestCase):

    def test_flexible_dob_parsing(self):
        # 1. ISO format YYYY-MM-DD
        req1 = ReportPdfRequest.model_validate({
            "name": "Bhaskr Singh",
            "dob": "1992-07-15",
            "topic": "vedic_destiny",
            "tier": "advanced"
        })
        self.assertEqual(req1.name, "Bhaskr Singh")
        self.assertEqual(req1.day, 15)
        self.assertEqual(req1.month, 7)
        self.assertEqual(req1.year, 1992)
        self.assertEqual(req1.topic_id, "vedic_destiny")
        self.assertEqual(req1.tier, "advanced")

        # 2. Slash format DD/MM/YYYY
        req2 = ReportCalculateRequest.model_validate({
            "name": "Aarav Sharma",
            "dob": "28/11/1985",
            "topic": "career_wealth_forecast",
            "package_tier": "premium"
        })
        self.assertEqual(req2.day, 28)
        self.assertEqual(req2.month, 11)
        self.assertEqual(req2.year, 1985)
        self.assertEqual(req2.topic_id, "career_wealth_forecast")
        self.assertEqual(req2.tier, "premium")

    def test_calculate_report_preview_endpoint(self):
        req = ReportCalculateRequest(
            name="Bhaskr Singh",
            day=15,
            month=7,
            year=1992,
            topic_id="vedic_destiny",
            tier="advanced"
        )
        res = calculate_report_preview(req)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["deterministic_findings"]["driver_number"], 6)
        self.assertEqual(res["deterministic_findings"]["conductor_number"], 7)
        self.assertIn("Silver Success Plane (2-5-8)", PLANES)
        self.assertIn("Golden Success Plane (4-5-6)", PLANES)

    def test_generate_pdf_endpoint_deliverable(self):
        req = ReportPdfRequest(
            name="Bhaskr Singh",
            day=15,
            month=7,
            year=1992,
            topic_id="vedic_destiny",
            tier="basic"
        )
        response = generate_pdf_endpoint(req)
        self.assertEqual(response.media_type, "application/pdf")
        self.assertTrue(len(response.body) > 5000)
        self.assertTrue(response.body.startswith(b"%PDF"))

    def test_silver_success_plane_verification(self):
        # Date with 2, 5, 8: 25-08-1990
        res = analyze_lo_shu_grid(25, 8, 1990)
        self.assertIn("Silver Success Plane (2-5-8)", res["completed_planes"])
        self.assertNotIn("Disappointment Plane", str(res))

if __name__ == "__main__":
    unittest.main()
