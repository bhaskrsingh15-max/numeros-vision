import io
import json
import os
import sys
import time
import unittest
import pypdf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.internal_pdf_worker_service import (
    MAX_REQUEST_BODY_BYTES,
    app as pdf_service_app,
    compute_worker_hmac_signature,
    verify_worker_hmac_signature,
    validate_view_only_payload,
    render_pdf_from_view,
)
from tests.test_pdf_tier_gating import BASIC_FORBIDDEN_KEYWORDS, ADVANCED_FORBIDDEN_KEYWORDS

sys.stdout.reconfigure(encoding="utf-8")


def _sample_view_for_payload(tier: str = "basic", pack_id: str = "report_basic") -> dict:
    has_basic = tier in ("basic", "advanced", "premium")
    has_advanced = tier in ("advanced", "premium")
    has_premium = tier == "premium"
    return {
        "job_id": f"job_test_{tier}",
        "pack_id": pack_id,
        "view": {
            "user": {"userId": "usr_101"},
            "subject": {
                "id": "sbj_202",
                "name": "Aaditya Sharma",
                "dob": "1990-08-15",
                "created_at": 1700000000000,
            },
            "tier": tier,
            "entitlements": [pack_id],
            "calculation": {
                "driver": 6,
                "conductor": 6,
                "conductorRaw": 33,
                "conductorDisplay": "33/6",
                "driverPlanet": "Venus",
                "conductorPlanet": "Venus",
                "counts": {"1": 2, "2": 0, "3": 0, "4": 0, "5": 1, "6": 0, "7": 0, "8": 1, "9": 2},
                "presentDigits": [1, 5, 8, 9],
                "missingDigits": [2, 3, 4, 6, 7],
                "planes": [
                    {"name": "Will Plane", "digits": [9, 5, 1], "presentCount": 3, "percentage": 100, "status": "COMPLETE"}
                ],
            },
            "sections": {
                "grid": {"unlocked": True, "cells": []},
                "enabledDigits": {"unlocked": True, "items": []},
                "elementBalancing": {"unlocked": has_basic, "pageCount": 3},
                "enabledNumbersInDepth": {"unlocked": has_advanced, "pageCount": 12},
                "missingNumbersInDepth": {"unlocked": has_premium, "pageCount": 32},
                "remedies": {"unlocked": has_premium, "pageCount": 32},
                "predictions": {"unlocked": has_premium, "pageCount": 32},
            },
        },
    }


class TestCommit6bPythonGenerator(unittest.TestCase):
    def test_hmac_signature_and_timestamp_verification(self):
        secret = "a1b2c3d4e5f60718293a4b5c6d7e8f90a1b2c3d4e5f60718293a4b5c6d7e8f90"
        raw_body = json.dumps(_sample_view_for_payload("basic", "report_basic")).encode("utf-8")
        now_sec = int(time.time())
        sig = compute_worker_hmac_signature(raw_body, str(now_sec), secret)

        ok, msg = verify_worker_hmac_signature(raw_body, str(now_sec), sig, secret, now_sec=now_sec)
        self.assertTrue(ok, msg)

        # Expired timestamp (> 300s skew) must fail
        ok_exp, msg_exp = verify_worker_hmac_signature(
            raw_body, str(now_sec - 301), sig, secret, now_sec=now_sec
        )
        self.assertFalse(ok_exp)
        self.assertIn("expired", msg_exp.lower())

        # Tampered body or wrong signature must fail
        ok_bad, msg_bad = verify_worker_hmac_signature(
            raw_body + b" ", str(now_sec), sig, secret, now_sec=now_sec
        )
        self.assertFalse(ok_bad)
        self.assertIn("invalid", msg_bad.lower())

    def test_rejects_raw_data_and_pii_fields(self):
        for forbidden_key in ("dob_enc", "phone_enc", "birth_time_enc", "phone_hash", "token_hash"):
            payload = _sample_view_for_payload("basic", "report_basic")
            payload["view"]["subject"][forbidden_key] = "encrypted_or_raw_secret"
            with self.assertRaises(ValueError) as ctx:
                validate_view_only_payload(payload)
            self.assertIn(forbidden_key, str(ctx.exception))

        # Contact PII in view.user must also be rejected
        payload_pii = _sample_view_for_payload("basic", "report_basic")
        payload_pii["view"]["user"]["phone"] = "+919876543210"
        with self.assertRaises(ValueError) as ctx2:
            validate_view_only_payload(payload_pii)
        self.assertIn("phone", str(ctx2.exception))

    def test_renders_all_three_tiers_strictly_from_view_for(self):
        for tier, pack_id, expected_pages in (
            ("basic", "report_basic", 3),
            ("advanced", "report_advanced", 12),
            ("premium", "report_premium", 32),
        ):
            payload = _sample_view_for_payload(tier=tier, pack_id=pack_id)
            pdf_bytes, meta = render_pdf_from_view(payload)
            self.assertEqual(meta["tier"], tier)
            reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
            self.assertEqual(len(reader.pages), expected_pages)
            full_text = " ".join(p.extract_text() for p in reader.pages)

            if tier == "basic":
                for kw in BASIC_FORBIDDEN_KEYWORDS:
                    self.assertNotIn(kw.lower(), full_text.lower())
            elif tier == "advanced":
                for kw in ADVANCED_FORBIDDEN_KEYWORDS:
                    self.assertNotIn(kw.lower(), full_text.lower())

    def test_request_size_limit_and_isolated_pdf_service_folder(self):
        from starlette.requests import Request
        from fastapi import HTTPException
        from app.services.internal_pdf_worker_service import handle_render_pdf

        os.environ["PDF_SERVICE_SECRET"] = "fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210"
        oversized_body = b"x" * (MAX_REQUEST_BODY_BYTES + 10)

        async def receive():
            return {"type": "http.request", "body": oversized_body, "more_body": False}

        scope = {
            "type": "http",
            "method": "POST",
            "path": "/internal/v1/render-pdf",
            "headers": [(b"content-length", str(len(oversized_body)).encode("ascii"))],
        }
        req = Request(scope, receive)
        coro = handle_render_pdf(req)
        with self.assertRaises(HTTPException) as ctx:
            try:
                coro.send(None)
            finally:
                coro.close()
        self.assertEqual(ctx.exception.status_code, 413)

        # Verify dedicated pdf_service directory contains Dockerfile, requirements.txt, and needed modules only
        pdf_svc_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "pdf_service")
        self.assertTrue(os.path.isfile(os.path.join(pdf_svc_dir, "Dockerfile")))
        self.assertTrue(os.path.isfile(os.path.join(pdf_svc_dir, "requirements.txt")))
        self.assertTrue(os.path.isfile(os.path.join(pdf_svc_dir, "app", "services", "internal_pdf_worker_service.py")))
        self.assertFalse(os.path.exists(os.path.join(pdf_svc_dir, "app", "static")))


if __name__ == "__main__":
    unittest.main()
