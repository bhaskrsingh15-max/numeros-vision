import unittest
from pathlib import Path
from fastapi.testclient import TestClient
from app.main import app

class TestTwoStepSignupWorkflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        signup_path = Path("app/static/signup.html")
        cls.signup_html = signup_path.read_text(encoding="utf-8")

    def test_signup_html_twostep_elements(self):
        """Verifies all required Step 1 and Step 2 elements exist in signup.html."""
        # Progress tracker
        self.assertIn('class="step-progress-wrapper"', self.signup_html)
        self.assertIn('id="progressStep1"', self.signup_html)
        self.assertIn('id="progressStep2"', self.signup_html)

        # Step 1 containers and fields
        self.assertIn('id="step1Container"', self.signup_html)
        self.assertIn('id="regPhonePrefix"', self.signup_html)
        self.assertIn('id="regPhone"', self.signup_html)
        self.assertIn('id="regEmail"', self.signup_html)
        self.assertIn('id="regPass"', self.signup_html)
        self.assertIn('id="btnSendStep1Otp"', self.signup_html)
        self.assertIn('id="step1OtpDrawer"', self.signup_html)
        self.assertIn('id="otpCodeInput"', self.signup_html)
        self.assertIn('id="btnVerifyStep1Otp"', self.signup_html)

        # Step 2 containers and fields
        self.assertIn('id="step2Container"', self.signup_html)
        self.assertIn('class="verified-contact-summary"', self.signup_html)
        self.assertIn('id="step2DisplayPhone"', self.signup_html)
        self.assertIn('id="step2DisplayEmail"', self.signup_html)
        self.assertIn('id="regName"', self.signup_html)
        self.assertIn('id="regDay"', self.signup_html)
        self.assertIn('id="regMonth"', self.signup_html)
        self.assertIn('id="regYear"', self.signup_html)
        self.assertIn('id="regTimeHour"', self.signup_html)
        self.assertIn('id="regTimeMinute"', self.signup_html)
        self.assertIn('id="regTimePeriod"', self.signup_html)
        self.assertIn('id="regPlace"', self.signup_html)
        self.assertIn('id="regCountry"', self.signup_html)
        self.assertIn('id="regLatitude"', self.signup_html)
        self.assertIn('id="regLongitude"', self.signup_html)
        self.assertIn('id="regAltitude"', self.signup_html)
        self.assertIn('id="regTimezone"', self.signup_html)
        self.assertIn('id="regGender"', self.signup_html)
        self.assertIn('id="consentStorage"', self.signup_html)
        self.assertIn('id="btnSubmit"', self.signup_html)

        # Canonical brand identity
        self.assertIn('class="nv-header"', self.signup_html)
        self.assertIn('class="nv-footer"', self.signup_html)
        self.assertIn('NUMEROS VISION', self.signup_html)
        self.assertIn('ANVEIL EVERY CHARM', self.signup_html)

    def test_step1_otp_lifecycle(self):
        """Verifies Step 1 OTP generation, verification, and token emission."""
        phone = "+91 91234 56789"
        
        # 1. Send OTP
        res_send = self.client.post("/api/v1/auth/otp/send", json={"identifier": phone, "channel": "sms"})
        self.assertEqual(res_send.status_code, 200)
        self.assertEqual(res_send.json()["status"], "success")

        # 2. Verify with invalid OTP
        res_bad = self.client.post("/api/v1/auth/otp/verify", json={"identifier": phone, "otp": "000000"})
        self.assertEqual(res_bad.status_code, 400)

        # 3. Verify with valid sandbox OTP
        res_good = self.client.post("/api/v1/auth/otp/verify", json={"identifier": phone, "otp": "123456"})
        self.assertEqual(res_good.status_code, 200)
        data = res_good.json()
        self.assertTrue(data["verified"])
        self.assertIn("verification_token", data)

    def test_step2_profile_submission_with_altitude_and_consent(self):
        """Verifies Step 2 submission stores birth matrix, coordinates with altitude, and DPDP consent."""
        payload = {
            "name": "Kavita Rao",
            "email": "kavita.rao@example.com",
            "phone": "+91 98888 77777",
            "password": "Password123#",
            "phone_verified": True,
            "email_verified": True,
            "verification_token": "token_verified_step1",
            "day": 24,
            "month": 11,
            "year": 1992,
            "birth_time": "10:15 AM",
            "birth_time_hour": 10,
            "birth_time_minute": 15,
            "birth_time_period": "AM",
            "birth_place": "Bengaluru",
            "country": "India",
            "latitude": 12.9716,
            "longitude": 77.5946,
            "altitude": 920.0,
            "timezone": "Asia/Kolkata",
            "gender": "female",
            "consent_profile_storage": True,
            "consent_evaluation_feedback": True,
            "consent_marketing": False
        }

        res = self.client.post("/api/v1/auth/signup", json=payload)
        self.assertEqual(res.status_code, 200, res.text)
        data = res.json()
        self.assertEqual(data["status"], "success")
        
        prof = data["profile"]
        self.assertEqual(prof["name"], "Kavita Rao")
        self.assertEqual(prof["altitude"], 920.0)
        self.assertEqual(prof["latitude"], 12.9716)
        self.assertEqual(prof["longitude"], 77.5946)
        self.assertEqual(prof["driver_mulank"], 6)  # 24 -> 2 + 4 = 6 (Venus)
        self.assertTrue(prof["phone_verified"])

if __name__ == "__main__":
    unittest.main()
