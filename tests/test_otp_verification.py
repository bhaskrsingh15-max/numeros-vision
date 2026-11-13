import unittest
from fastapi.testclient import TestClient
from app.main import app

class TestOTPVerificationService(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_send_and_verify_otp_email(self):
        # 1. Send OTP to email
        resp = self.client.post("/api/v1/auth/otp/send", json={
            "identifier": "testseeker@example.com"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["channel"], "email")
        self.assertIn("otp_preview", data)
        otp_code = data["otp_preview"]

        # 2. Verify with wrong code
        bad_resp = self.client.post("/api/v1/auth/otp/verify", json={
            "identifier": "testseeker@example.com",
            "otp": "000000"
        })
        self.assertEqual(bad_resp.status_code, 400)

        # 3. Verify with correct code
        good_resp = self.client.post("/api/v1/auth/otp/verify", json={
            "identifier": "testseeker@example.com",
            "otp": otp_code
        })
        self.assertEqual(good_resp.status_code, 200)
        good_data = good_resp.json()
        self.assertTrue(good_data["verified"])
        self.assertIn("verification_token", good_data)

    def test_send_and_verify_otp_mobile_and_sandbox(self):
        # 1. Send OTP to mobile
        resp = self.client.post("/api/v1/auth/otp/send", json={
            "identifier": "+919876543210",
            "channel": "sms"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["channel"], "sms")

        # 2. Verify using universal sandbox OTP "123456"
        sandbox_resp = self.client.post("/api/v1/auth/otp/verify", json={
            "identifier": "+919876543210",
            "otp": "123456"
        })
        self.assertEqual(sandbox_resp.status_code, 200)
        self.assertTrue(sandbox_resp.json()["verified"])

    def test_identity_alias_and_passwordless_login(self):
        # 1. Identity route alias send
        resp = self.client.post("/api/v1/identity/otp/send", json={
            "identifier": "+919811122233"
        })
        self.assertEqual(resp.status_code, 200)

        # 2. Passwordless login with OTP
        login_resp = self.client.post("/api/v1/auth/otp/login", json={
            "identifier": "+919811122233",
            "otp": "123456",
            "name": "Aarav Patel"
        })
        self.assertEqual(login_resp.status_code, 200)
        login_data = login_resp.json()
        self.assertIn("session_token", login_data)
        self.assertEqual(login_data["profile"]["name"], "Aarav Patel")
        self.assertEqual(login_data["profile"]["verification_badge"], "verified_customer")

if __name__ == "__main__":
    unittest.main()
