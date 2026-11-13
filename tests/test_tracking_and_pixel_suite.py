"""
TEST SUITE: TRACKING, PIXELS & ANALYTICS SUITE
Verifies:
1. GET /api/v1/cdp/config/analytics returns public client configuration schema.
2. Environment variables (GA4, Meta, Google Ads, Firebase, Clarity) correctly propagate.
3. Static files /static/js/nv_tracking_config.js and /static/js/marketing-analytics.js are served.
4. CDP event capture endpoints ingest conversion telemetry with DPDP consent.
"""

import os
import unittest
from fastapi.testclient import TestClient
from app.main import app


class TestTrackingAndPixelSuite(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_analytics_config_endpoint_schema(self):
        """Verifies that /api/v1/cdp/config/analytics returns expected public keys."""
        res = self.client.get("/api/v1/cdp/config/analytics")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data.get("status"), "success")
        cfg = data.get("config", {})

        # Assert presence of all required tracker keys
        self.assertIn("ga4_measurement_id", cfg)
        self.assertIn("google_ads_id", cfg)
        self.assertIn("google_ads_conversion_label_signup", cfg)
        self.assertIn("google_ads_conversion_label_purchase", cfg)
        self.assertIn("meta_pixel_id", cfg)
        self.assertIn("clarity_project_id", cfg)
        self.assertIn("gtm_container_id", cfg)
        self.assertIn("firebase", cfg)

        # Assert firebase sub-keys
        fb = cfg.get("firebase", {})
        self.assertIn("apiKey", fb)
        self.assertIn("projectId", fb)
        self.assertIn("appId", fb)

    def test_environment_variable_override(self):
        """Verifies that environment variables dynamically override tracking IDs."""
        test_ga4 = "G-DETERMINISTIC_TEST_01"
        test_meta = "987654321012345"
        test_gads = "AW-1122334455"
        test_clarity = "clarity_proj_99"

        os.environ["GA4_MEASUREMENT_ID"] = test_ga4
        os.environ["META_PIXEL_ID"] = test_meta
        os.environ["GOOGLE_ADS_ID"] = test_gads
        os.environ["CLARITY_PROJECT_ID"] = test_clarity

        try:
            res = self.client.get("/api/v1/cdp/config/analytics")
            self.assertEqual(res.status_code, 200)
            cfg = res.json().get("config", {})
            self.assertEqual(cfg.get("ga4_measurement_id"), test_ga4)
            self.assertEqual(cfg.get("meta_pixel_id"), test_meta)
            self.assertEqual(cfg.get("google_ads_id"), test_gads)
            self.assertEqual(cfg.get("clarity_project_id"), test_clarity)
        finally:
            # Clean up
            os.environ.pop("GA4_MEASUREMENT_ID", None)
            os.environ.pop("META_PIXEL_ID", None)
            os.environ.pop("GOOGLE_ADS_ID", None)
            os.environ.pop("CLARITY_PROJECT_ID", None)

    def test_static_analytics_js_assets_accessible(self):
        """Verifies that tracking scripts are served statically via FastAPI."""
        res_cfg = self.client.get("/static/js/nv_tracking_config.js")
        self.assertEqual(res_cfg.status_code, 200)
        self.assertIn("window.NV_TRACKING_CONFIG", res_cfg.text)

        res_eng = self.client.get("/static/js/marketing-analytics.js")
        self.assertEqual(res_eng.status_code, 200)
        self.assertIn("window.nvTrack", res_eng.text)
        self.assertIn("freeSignup", res_eng.text)
        self.assertIn("paidPurchase", res_eng.text)

    def test_cdp_capture_conversion_events(self):
        """Verifies that conversion telemetry events are captured in CDP."""
        # 1. Free Signup event
        payload_signup = {
            "name": "Conversion Test Seeker",
            "email": "conversion_seeker@example.com",
            "device_id": "test_device_conv_001",
            "device_type": "mobile",
            "category": "free_signup",
            "utm_source": "meta_ads",
            "utm_medium": "cpc",
            "utm_campaign": "lo_shu_grid_prospecting"
        }
        res_signup = self.client.post("/api/v1/cdp/capture", json=payload_signup)
        self.assertEqual(res_signup.status_code, 200)
        self.assertEqual(res_signup.json().get("status"), "success")

        # 2. Paid Purchase event with spend
        payload_purchase = {
            "device_id": "test_device_conv_001",
            "device_type": "mobile",
            "total_spend_inr": 510.0,
            "category": "paid_report_purchase",
            "utm_source": "google_ads",
            "utm_campaign": "master_report_retargeting"
        }
        res_purchase = self.client.post("/api/v1/cdp/capture", json=payload_purchase)
        self.assertEqual(res_purchase.status_code, 200)
        self.assertEqual(res_purchase.json().get("status"), "success")


if __name__ == "__main__":
    unittest.main()
