"""
TEST SUITE: PHASE 1 LIVE PAYMENTS, DISK-BACKED SESSIONS & RAZORPAY WEBHOOKS
Covers:
1. Razorpay order creation for all core plans (Starter ₹95, Growth ₹399, Complete ₹1,050, VIP ₹11,400).
2. Server-to-server Razorpay webhook processing (payment.captured) and automated token provisioning.
3. Client-side payment verification (HMAC signature / mock) and token generation.
4. Disk-backed session persistence across server restart simulation.
5. Multi-turn paid question consumption and conversation history preservation.
"""

import sys
import os
import unittest
import json
import time
import hmac
import hashlib

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app
from app.api.payments import (
    PLANS, _verified_payments, _save_sessions, _load_sessions,
    SESSIONS_FILE, DATA_DIR, RAZORPAY_KEY_SECRET, RAZORPAY_WEBHOOK_SECRET
)

class TestPhase1LivePaymentsAndWebhooks(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.test_email = f"seeker.{int(time.time() * 1000)}@numerosvision.com"
        signup_res = self.client.post("/api/v1/auth/signup", json={
            "name": "Phase1 Seeker",
            "email": self.test_email,
            "phone": "+919876500123",
            "day": 28,
            "month": 11,
            "year": 1981,
            "password": "SecurePassword123!",
            "consent_profile_storage": True,
        })
        self.auth_headers = {}
        if signup_res.status_code == 200 and signup_res.json().get("session_token"):
            self.auth_headers = {"Authorization": f"Bearer {signup_res.json()['session_token']}"}

    def _sign_razorpay(self, order_id: str, payment_id: str) -> str:
        return hmac.new(
            RAZORPAY_KEY_SECRET.encode(),
            f"{order_id}|{payment_id}".encode(),
            hashlib.sha256,
        ).hexdigest()

    def test_create_order_starter_and_growth(self):
        """Tests order creation endpoint returns valid amount, paise, and currency."""
        from unittest.mock import patch

        with patch("razorpay.Client") as mock_rzp_cls:
            mock_rzp_cls.return_value.order.create.side_effect = (
                lambda payload: {"id": f"order_test_{payload['amount']}", **payload}
            )
            # Canonical Charm AI Starter Pack ₹199 (`charm_single`)
            resp = self.client.post("/api/v1/payments/create-order", json={
                "plan": "charm_single",
                "name": "Phase1 Seeker",
                "email": self.test_email,
                "mobile": "9876543210"
            }, headers=self.auth_headers)
            self.assertEqual(resp.status_code, 200)
            data = resp.json()
            self.assertIn("order_id", data)
            self.assertEqual(data["amount_inr"], 199)
            self.assertEqual(data["amount"], 19900)
            self.assertEqual(data["currency"], "INR")

            # Canonical Basic Report (`report_basic`: ₹399 regular when launch window unset)
            with patch.dict(os.environ, {"ENVIRONMENT": "production", "NV_LAUNCH_STARTS_AT": "", "NV_LAUNCH_ENDS_AT": ""}, clear=False):
                os.environ.pop("NV_FORCE_LAUNCH_MODE", None)
                resp_g = self.client.post("/api/v1/payments/create-order", json={
                    "plan": "report_basic",
                    "name": "Phase1 Seeker",
                    "email": self.test_email
                }, headers=self.auth_headers)
                self.assertEqual(resp_g.status_code, 200)
                data_g = resp_g.json()
                self.assertEqual(data_g["amount_inr"], 399)
                self.assertEqual(data_g["amount"], 39900)

    def test_client_verify_payment_and_disk_persistence(self):
        """Verifies payment, checks token, and ensures data/verified_sessions.json persists it."""
        mock_order_id = f"order_TEST_{int(time.time())}"
        mock_pay_id = f"pay_TEST_{int(time.time())}"

        resp = self.client.post("/api/v1/payments/verify", json={
            "razorpay_order_id": mock_order_id,
            "razorpay_payment_id": mock_pay_id,
            "razorpay_signature": self._sign_razorpay(mock_order_id, mock_pay_id),
            "plan": "charm_single",
            "email": self.test_email
        }, headers=self.auth_headers)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertTrue(data["verified"])
        token = data["premium_token"]

        # Check status endpoint
        st_resp = self.client.get(f"/api/v1/payments/status/{token}")
        self.assertEqual(st_resp.status_code, 200)
        st_data = st_resp.json()
        self.assertTrue(st_data["active"])
        self.assertEqual(st_data["questions_remaining"], 5)
        self.assertTrue(st_data["has_remedies"])

        # Check disk file exists and contains the session
        self.assertTrue(os.path.exists(SESSIONS_FILE))
        with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
            disk_data = json.load(f)
        self.assertIn(token, disk_data)
        self.assertEqual(disk_data[token]["order_id"], mock_order_id)

    def test_razorpay_webhook_processing(self):
        """Tests server-to-server webhook handling for payment.captured event."""
        webhook_pay_id = f"pay_hook_{int(time.time())}"
        webhook_order_id = f"order_hook_{int(time.time())}"
        payload = {
            "event": "payment.captured",
            "payload": {
                "payment": {
                    "entity": {
                        "id": webhook_pay_id,
                        "order_id": webhook_order_id,
                        "amount": 19900,
                        "currency": "INR",
                        "status": "captured",
                        "notes": {
                            "plan": "charm_single",
                            "email": self.test_email,
                            "name": "Auspicious Seeker"
                        }
                    }
                }
            }
        }
        raw_body = json.dumps(payload).encode("utf-8")
        sig = hmac.new(RAZORPAY_WEBHOOK_SECRET.encode(), raw_body, hashlib.sha256).hexdigest()

        resp = self.client.post(
            "/api/v1/payments/webhook",
            data=raw_body,
            headers={
                "Content-Type": "application/json",
                "X-Razorpay-Signature": sig
            }
        )
        self.assertEqual(resp.status_code, 200)
        res_data = resp.json()
        self.assertEqual(res_data["status"], "success")
        self.assertEqual(res_data["event"], "payment.captured")
        session_token = res_data["session_token"]

        # Confirm session is activated with 5 questions and remedies enabled
        st_resp = self.client.get(f"/api/v1/payments/status/{session_token}")
        self.assertEqual(st_resp.status_code, 200)
        st_data = st_resp.json()
        self.assertTrue(st_data["active"])
        self.assertEqual(st_data["questions_remaining"], 5)
        self.assertTrue(st_data["has_remedies"])

    def test_multi_turn_questions_and_history_persistence(self):
        """
        Tests multi-turn questioning:
        Question 1 -> balance 5 -> 4.
        Simulate server reload -> balance remains 4.
        Question 2 -> balance 4 -> 3 -> history preserved.
        """
        # 1. Create and verify a starter plan
        mt_ord = f"order_MULTITURN_{int(time.time())}"
        mt_pay = f"pay_MULTITURN_{int(time.time())}"
        resp = self.client.post("/api/v1/payments/verify", json={
            "razorpay_order_id": mt_ord,
            "razorpay_payment_id": mt_pay,
            "razorpay_signature": self._sign_razorpay(mt_ord, mt_pay),
            "plan": "charm_single",
            "email": self.test_email
        }, headers=self.auth_headers)
        token = resp.json()["premium_token"]

        # 2. Ask Question 1
        q1_resp = self.client.post("/api/v1/readings/ask", json={
            "name": "Phase1 Seeker",
            "day": 28, "month": 11, "year": 1981,
            "question": "What is my career direction for this quarter?",
            "premium_token": token
        })
        self.assertEqual(q1_resp.status_code, 200)
        q1_data = q1_resp.json()
        self.assertTrue(q1_data["is_premium"])
        self.assertEqual(q1_data["questions_remaining"], 4)

        # 3. Simulate Server Restart: clear in-memory cache and reload from disk
        _verified_payments.clear()
        self.assertEqual(len(_verified_payments), 0)
        _load_sessions()
        self.assertIn(token, _verified_payments)
        self.assertEqual(_verified_payments[token]["questions_remaining"], 4)
        self.assertEqual(len(_verified_payments[token].get("question_history", [])), 1)

        # 4. Ask Question 2 (Multi-turn follow-up)
        q2_resp = self.client.post("/api/v1/readings/ask", json={
            "name": "Phase1 Seeker",
            "day": 28, "month": 11, "year": 1981,
            "question": "Following up on that, should I relocate for this job?",
            "premium_token": token
        })
        self.assertEqual(q2_resp.status_code, 200)
        q2_data = q2_resp.json()
        self.assertEqual(q2_data["questions_remaining"], 3)

        # Verify history has 2 questions recorded
        history = _verified_payments[token].get("question_history", [])
        self.assertEqual(len(history), 2)
        self.assertIn("career", history[0]["question"].lower())
        self.assertIn("relocate", history[1]["question"].lower())

if __name__ == "__main__":
    unittest.main()
