"""
tests/test_charm_service_auth.py
================================
Unit tests verifying fail-closed authentication for Charm AI / Gemini backend service.
Tests:
- Production environment: missing secret -> 503; wrong/missing header -> 403; correct header -> passes
- Preview environment: missing secret -> 503; wrong/missing header -> 403; correct header -> passes
- Unset ENVIRONMENT: missing secret -> 503; wrong/missing header -> 403; correct header -> passes
- NV_ALLOW_UNAUTHENTICATED_LOCAL=true: bypasses authentication for offline local testing
"""

import os
import unittest
from unittest.mock import Mock
from fastapi import HTTPException

from app.api.charm_ai import verify_charm_service_auth


class TestCharmServiceAuth(unittest.TestCase):
    def setUp(self):
        self.original_env = dict(os.environ)

    def tearDown(self):
        os.environ.clear()
        os.environ.update(self.original_env)

    def _mock_request(self, headers=None):
        req = Mock()
        req.headers = headers or {}
        return req

    def test_production_missing_secret_returns_503(self):
        os.environ["ENVIRONMENT"] = "production"
        os.environ.pop("CHARM_SERVICE_SECRET", None)
        os.environ.pop("NV_ALLOW_UNAUTHENTICATED_LOCAL", None)

        req = self._mock_request({"X-NV-Charm-Secret": "any_secret"})
        with self.assertRaises(HTTPException) as ctx:
            verify_charm_service_auth(req)
        self.assertEqual(ctx.exception.status_code, 503)

    def test_production_missing_header_returns_403(self):
        os.environ["ENVIRONMENT"] = "production"
        os.environ["CHARM_SERVICE_SECRET"] = "valid_configured_secret"
        os.environ.pop("NV_ALLOW_UNAUTHENTICATED_LOCAL", None)

        req = self._mock_request({})
        with self.assertRaises(HTTPException) as ctx:
            verify_charm_service_auth(req)
        self.assertEqual(ctx.exception.status_code, 403)

    def test_production_wrong_header_returns_403(self):
        os.environ["ENVIRONMENT"] = "production"
        os.environ["CHARM_SERVICE_SECRET"] = "valid_configured_secret"
        os.environ.pop("NV_ALLOW_UNAUTHENTICATED_LOCAL", None)

        req = self._mock_request({"X-NV-Charm-Secret": "invalid_probe_secret"})
        with self.assertRaises(HTTPException) as ctx:
            verify_charm_service_auth(req)
        self.assertEqual(ctx.exception.status_code, 403)

    def test_production_correct_header_succeeds(self):
        os.environ["ENVIRONMENT"] = "production"
        os.environ["CHARM_SERVICE_SECRET"] = "valid_configured_secret"
        os.environ.pop("NV_ALLOW_UNAUTHENTICATED_LOCAL", None)

        req = self._mock_request({"X-NV-Charm-Secret": "valid_configured_secret"})
        # Should not raise exception
        verify_charm_service_auth(req)

    def test_preview_missing_secret_returns_503(self):
        os.environ["ENVIRONMENT"] = "preview"
        os.environ.pop("CHARM_SERVICE_SECRET", None)
        os.environ.pop("NV_ALLOW_UNAUTHENTICATED_LOCAL", None)

        req = self._mock_request({"X-NV-Charm-Secret": "any_secret"})
        with self.assertRaises(HTTPException) as ctx:
            verify_charm_service_auth(req)
        self.assertEqual(ctx.exception.status_code, 503)

    def test_preview_wrong_header_returns_403(self):
        os.environ["ENVIRONMENT"] = "preview"
        os.environ["CHARM_SERVICE_SECRET"] = "preview_valid_secret"
        os.environ.pop("NV_ALLOW_UNAUTHENTICATED_LOCAL", None)

        req = self._mock_request({"X-NV-Charm-Secret": "wrong_secret"})
        with self.assertRaises(HTTPException) as ctx:
            verify_charm_service_auth(req)
        self.assertEqual(ctx.exception.status_code, 403)

    def test_preview_correct_header_succeeds(self):
        os.environ["ENVIRONMENT"] = "preview"
        os.environ["CHARM_SERVICE_SECRET"] = "preview_valid_secret"
        os.environ.pop("NV_ALLOW_UNAUTHENTICATED_LOCAL", None)

        req = self._mock_request({"X-NV-Charm-Secret": "preview_valid_secret"})
        verify_charm_service_auth(req)

    def test_unset_environment_missing_secret_returns_503(self):
        os.environ.pop("ENVIRONMENT", None)
        os.environ.pop("CHARM_SERVICE_SECRET", None)
        os.environ.pop("NV_ALLOW_UNAUTHENTICATED_LOCAL", None)

        req = self._mock_request({"X-NV-Charm-Secret": "any_secret"})
        with self.assertRaises(HTTPException) as ctx:
            verify_charm_service_auth(req)
        self.assertEqual(ctx.exception.status_code, 503)

    def test_unset_environment_wrong_header_returns_403(self):
        os.environ.pop("ENVIRONMENT", None)
        os.environ["CHARM_SERVICE_SECRET"] = "secret_for_unset"
        os.environ.pop("NV_ALLOW_UNAUTHENTICATED_LOCAL", None)

        req = self._mock_request({"X-NV-Charm-Secret": "wrong_secret"})
        with self.assertRaises(HTTPException) as ctx:
            verify_charm_service_auth(req)
        self.assertEqual(ctx.exception.status_code, 403)

    def test_unset_environment_correct_header_succeeds(self):
        os.environ.pop("ENVIRONMENT", None)
        os.environ["CHARM_SERVICE_SECRET"] = "secret_for_unset"
        os.environ.pop("NV_ALLOW_UNAUTHENTICATED_LOCAL", None)

        req = self._mock_request({"X-NV-Charm-Secret": "secret_for_unset"})
        verify_charm_service_auth(req)

    def test_local_bypass_with_explicit_flag_succeeds(self):
        os.environ["NV_ALLOW_UNAUTHENTICATED_LOCAL"] = "true"
        os.environ.pop("CHARM_SERVICE_SECRET", None)

        req = self._mock_request({})
        # Should bypass authentication cleanly
        verify_charm_service_auth(req)


if __name__ == "__main__":
    unittest.main()
