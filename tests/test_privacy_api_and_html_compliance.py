import sys
import os
import unittest
import re

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app

class TestPrivacyApiAndHtmlCompliance(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        html_path = os.path.join(os.path.dirname(__file__), "..", "app", "static", "index.html")
        with open(html_path, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

    def test_privacy_settings_endpoint(self):
        """Verify GET /api/v1/privacy/settings returns DPDP 2025 configuration."""
        response = self.client.get("/api/v1/privacy/settings")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("Digital Personal Data Protection Act 2025", data["jurisdiction"])
        self.assertIn("ESSENTIAL_SERVICE", data["purposes"])
        self.assertIn("LOCATION_FOR_VASTU", data["purposes"])
        self.assertIn("LOCATION_FOR_ADVERTISING", data["purposes"])
        self.assertTrue(len(data["approved_partners"]) > 0)

    def test_identity_registration_and_consent_lifecycle(self):
        """Verify registration, granting consent, listing consents, and cascading withdrawal."""
        # 1. Register Web identity
        reg_res = self.client.post("/api/v1/identity/register", json={
            "platform": "MOBILE_WEB",
            "client_id_type": "WEB_1P_ID",
            "raw_id": "test_web_client_12345"
        })
        self.assertEqual(reg_res.status_code, 200)
        reg_data = reg_res.json()
        self.assertEqual(reg_data["status"], "success")
        self.assertTrue(reg_data["token_id"].startswith("tok_"))
        identity_id = reg_data["identity_id"]

        # 2. Grant Analytics and Vastu Location consent
        c1 = self.client.post("/api/v1/privacy/consent", json={
            "identity_id": identity_id,
            "purpose": "ANALYTICS",
            "status": "GRANTED"
        })
        self.assertEqual(c1.status_code, 200)

        c2 = self.client.post("/api/v1/privacy/consent", json={
            "identity_id": identity_id,
            "purpose": "LOCATION_FOR_VASTU",
            "status": "GRANTED"
        })
        self.assertEqual(c2.status_code, 200)

        # 3. Retrieve active consents
        list_res = self.client.get(f"/api/v1/privacy/consents/{identity_id}")
        self.assertEqual(list_res.status_code, 200)
        list_data = list_res.json()
        purposes = [c["purpose"] for c in list_data["consents"] if c["status"] in ["granted", "GRANTED"]]
        self.assertIn("ANALYTICS", purposes)
        self.assertIn("LOCATION_FOR_VASTU", purposes)

        # 4. Withdraw Analytics consent only
        w1 = self.client.post("/api/v1/privacy/consent/withdraw", json={
            "identity_id": identity_id,
            "purpose": "ANALYTICS",
            "cascade": False
        })
        self.assertEqual(w1.status_code, 200)

        # Verify Analytics is withdrawn but Vastu remains
        list_res2 = self.client.get(f"/api/v1/privacy/consents/{identity_id}")
        analytics_status = [c["status"] for c in list_res2.json()["consents"] if c["purpose"] == "ANALYTICS"]
        vastu_status = [c["status"] for c in list_res2.json()["consents"] if c["purpose"] == "LOCATION_FOR_VASTU"]
        self.assertIn(analytics_status[-1], ["withdrawn", "revoked"])
        self.assertIn(vastu_status[-1], ["granted", "GRANTED"])

        # 5. Cascading withdrawal of all consents
        w_all = self.client.post("/api/v1/privacy/consent/withdraw", json={
            "identity_id": identity_id,
            "cascade": True
        })
        self.assertEqual(w_all.status_code, 200)
        self.assertTrue(w_all.json()["cascade_executed"])

    def test_html_zero_banned_buzzwords(self):
        """Frontend HTML must be 100% free of banned marketing buzzwords."""
        banned = ["unlock", "elevate", "game-changer", "revolutionary", "seamless"]
        for word in banned:
            matches = re.findall(rf"\b{word}\b", self.html_content, re.IGNORECASE)
            self.assertEqual(len(matches), 0, f"Found banned buzzword '{word}' in index.html {len(matches)} times: {matches}")

    def test_html_tagline_and_brand_locks(self):
        """Frontend HTML must enforce official tagline 'Anveil Every Charm' and zero black logo elements."""
        self.assertIn("ANVEIL EVERY CHARM", self.html_content.upper())
        self.assertIn("Privacy Center &amp; Consent", self.html_content)
        self.assertIn("id=\"privacy-modal\"", self.html_content)
        self.assertIn("id=\"terms-modal\"", self.html_content)

    def test_html_pricing_catalog(self):
        """Frontend HTML must accurately display all tiers and official pricing."""
        pricing_path = os.path.join(os.path.dirname(__file__), "..", "app", "static", "pricing.html")
        with open(pricing_path, "r", encoding="utf-8") as f:
            pricing_html = f.read()
        self.assertIn("₹95", pricing_html)
        self.assertIn("₹199", pricing_html)
        self.assertIn("5 Question Predictions", pricing_html)
        self.assertIn("₹399", pricing_html)
        self.assertIn("₹599", pricing_html)
        self.assertIn("10 Questions + Full Remedies", pricing_html)
        self.assertIn("₹1,050", pricing_html)
        self.assertIn("₹1,299", pricing_html)
        self.assertIn("₹11,400", pricing_html)
        self.assertIn("₹24,000", pricing_html)

if __name__ == "__main__":
    unittest.main()
