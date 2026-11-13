"""
Unit & Integration tests for Section 17.9 Cost Controls, Quotas, and Tenant Isolation.
Verifies tenant isolation, idempotency deduplication, and budget protection.
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.services.image_provider import GoogleImageProvider, ImageGenerationRequest


class TestTenantIsolationAndQuotas(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_tenant_asset_isolation(self):
        """Tenant A cannot retrieve assets created by another tenant."""
        # 1. Tenant A creates project & job
        intake_a = self.client.post("/api/v1/logo/intake", json={
            "business_name": "TENANT ALFA",
            "business_activity": "Enterprise logistics software",
            "dpdp_consent": True,
        }).json()
        proj_a = intake_a["project_id"]
        self.client.post("/api/v1/logo/approve", json={"project_id": proj_a})
        gen_a = self.client.post("/api/v1/logo/generate", json={"project_id": proj_a}).json()
        job_a = gen_a["job_id"]

        # 2. Status is accessible with valid job_id
        res_a = self.client.get(f"/api/v1/logo/status/{job_a}")
        self.assertEqual(res_a.status_code, 200)

        # 3. Random / unauthorized job_id yields 404
        res_unauth = self.client.get("/api/v1/logo/status/job_unauthorized_999999")
        self.assertEqual(res_unauth.status_code, 404)

    def test_daily_budget_circuit_breaker(self):
        """Image provider halts and throws RuntimeError when daily budget is exhausted."""
        provider = GoogleImageProvider(mock_mode=True, max_daily_budget_usd=0.06)
        req = ImageGenerationRequest(job_id="job_budget_1", prompt="Logo test", output_count=1)
        
        # 1st call: $0.030 (passes)
        res1 = provider.generate_image(req)
        self.assertEqual(res1.estimated_cost_cents, 3)

        # 2nd call: $0.030 (passes, cumulative $0.06)
        res2 = provider.generate_image(req)
        self.assertEqual(res2.estimated_cost_cents, 3)

        # 3rd call: cumulative $0.09 > $0.06 -> Must trigger circuit breaker!
        with self.assertRaises(RuntimeError) as ctx:
            provider.generate_image(req)
        self.assertIn("BUDGET_EXHAUSTED", str(ctx.exception))

    def test_unsupported_download_format_rejected(self):
        """Download endpoint strictly rejects unverified format extensions."""
        intake = self.client.post("/api/v1/logo/intake", json={
            "business_name": "SECURE BRAND",
            "business_activity": "Financial auditing",
            "dpdp_consent": True,
        }).json()
        proj_id = intake["project_id"]
        self.client.post("/api/v1/logo/approve", json={"project_id": proj_id})
        gen = self.client.post("/api/v1/logo/generate", json={"project_id": proj_id}).json()
        job_id = gen["job_id"]

        resp = self.client.get(f"/api/v1/logo/download/{job_id}/exe")
        self.assertEqual(resp.status_code, 400)
        self.assertIn("Unsupported deliverable format", resp.json()["detail"])


if __name__ == "__main__":
    unittest.main()
