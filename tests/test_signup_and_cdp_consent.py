"""
TEST SUITE: SIGNUP PAGE, DPDP CONSENT & CDP IDENTITY STITCHING
Verifies:
1. Mandatory DPDP Act 2023 Consent Enforcement.
2. Deterministic Numerology (Mulank, Bhagyank, Lo Shu, Kua, Dasha).
3. CDP Golden Profile Identity Graph Stitching & UID2 Generation.
4. Statutory DPDP Consent Ledger Audit Trail.
5. User Authentication, Session Minting & Multi-Tool Profile Recall.
"""

import unittest
from fastapi.testclient import TestClient
from app.main import app
from app.api.auth import _USER_ACCOUNTS, _EMAIL_TO_USER_ID, _ACTIVE_SESSIONS
from app.engine.cdp_identity_engine import _GOLDEN_PROFILES, _IDENTIFIER_TO_GOLDEN_ID, hash_sha256, normalize_email
from app.api.consent import CONSENT_LEDGER


class TestSignupAndCdpConsent(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.valid_payload = {
            "name": "Devavrat Mukherjee",
            "email": "devavrat.m@example.org",
            "phone": "+91 98765 12345",
            "day": 18,
            "month": 7,
            "year": 1985,
            "birth_time": "02:35 PM",
            "birth_time_hour": 2,
            "birth_time_minute": 35,
            "birth_time_period": "PM",
            "birth_place": "Kolkata, West Bengal, India",
            "country": "India",
            "latitude": 22.5726,
            "longitude": 88.3639,
            "timezone": "Asia/Kolkata",
            "gender": "male",
            "password": "SecurePass2026!#",
            "consent_profile_storage": True,
            "consent_evaluation_feedback": True,
            "consent_marketing": True,
            "device_id": "test_device_uuid_9912",
            "device_type": "desktop",
            "utm_source": "google_search",
            "utm_campaign": "lo_shu_grid",
            "source": "signup_page",
            "redirect_url": "/dashboard/"
        }

    def test_signup_requires_mandatory_dpdp_consent(self):
        """Verifies that signup fails with 400 when mandatory DPDP storage consent is missing."""
        payload = self.valid_payload.copy()
        payload["email"] = "no_consent_user@example.com"
        payload["consent_profile_storage"] = False

        res = self.client.post("/api/v1/auth/signup", json=payload)
        self.assertEqual(res.status_code, 400)
        data = res.json()
        self.assertIn("Statutory Consent Required", data.get("detail", ""))

        # Verify also on alias endpoint
        res_alias = self.client.post("/api/v1/identity/signup", json=payload)
        self.assertEqual(res_alias.status_code, 400)

    def test_signup_validates_email_and_date(self):
        """Verifies rejection of invalid email or non-existent calendar dates."""
        # Invalid email
        payload_bad_email = self.valid_payload.copy()
        payload_bad_email["email"] = "invalid-email-string"
        res = self.client.post("/api/v1/auth/signup", json=payload_bad_email)
        self.assertEqual(res.status_code, 400)

        # Invalid date (Feb 30)
        payload_bad_date = self.valid_payload.copy()
        payload_bad_date["email"] = "valid_date_check@example.com"
        payload_bad_date["day"] = 30
        payload_bad_date["month"] = 2
        payload_bad_date["year"] = 1990
        res_date = self.client.post("/api/v1/auth/signup", json=payload_bad_date)
        self.assertEqual(res_date.status_code, 400)
        self.assertIn("Invalid date of birth", res_date.json().get("detail", ""))

    def test_successful_signup_and_deterministic_matrix(self):
        """Verifies successful registration and deterministic calculation of Mulank, Bhagyank, Lo Shu, Kua."""
        res = self.client.post("/api/v1/auth/signup", json=self.valid_payload)
        self.assertEqual(res.status_code, 200, res.text)
        data = res.json()

        self.assertEqual(data.get("status"), "success")
        self.assertIn("session_token", data)
        self.assertIn("user_id", data)
        self.assertIn("golden_profile_id", data)
        self.assertIn("uid2_token", data)

        prof = data.get("profile", {})
        # Day 18 -> 1 + 8 = 9 (Mars)
        self.assertEqual(prof.get("driver_mulank"), 9)
        # 18-07-1985 -> 1+8 + 7 + 1+9+8+5 = 9 + 7 + 23 = 39 -> 3+9=12 -> 3 (Jupiter)
        self.assertEqual(prof.get("conductor_bhagyank"), 3)
        # Year 1985 male -> last two 85 -> 8+5=13 -> 4. 10 - 4 = 6 (Kua 6, Metal)
        self.assertEqual(prof.get("kua_number"), 6)
        # Lo Shu grid counts for 18-07-1985: digits '18071985' -> 1:2, 8:2, 7:1, 9:1, 5:1
        loshu = prof.get("loshu_counts", {})
        self.assertEqual(loshu.get("1") or loshu.get(1), 2)
        self.assertEqual(loshu.get("8") or loshu.get(8), 2)
        self.assertEqual(loshu.get("7") or loshu.get(7), 1)
        self.assertEqual(loshu.get("9") or loshu.get(9), 1)
        self.assertEqual(loshu.get("5") or loshu.get(5), 1)

    def test_cdp_golden_profile_stitching(self):
        """Verifies that signup data is ingested and stitched into CDP Golden Profile."""
        signup_email = "cdp_stitch_test@example.com"
        signup_phone = "+91 99000 88776"
        payload = self.valid_payload.copy()
        payload["email"] = signup_email
        payload["phone"] = signup_phone

        res = self.client.post("/api/v1/identity/signup", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        gid = data["golden_profile_id"]

        # Profile must exist in CDP storage
        self.assertIn(gid, _GOLDEN_PROFILES)
        golden = _GOLDEN_PROFILES[gid]

        # Verify identity hashes
        norm_email = normalize_email(signup_email)
        norm_phone = "919900088776"
        self.assertEqual(golden["hashes"].get("email_sha256"), hash_sha256(norm_email))
        self.assertEqual(golden["hashes"].get("phone_sha256"), hash_sha256(norm_phone))

        # Verify deterministic taxonomy in CDP
        det = golden.get("deterministic_taxonomy", {})
        self.assertEqual(det.get("seeker_name"), payload["name"])
        self.assertEqual(det.get("numerology_mulank"), 9)
        self.assertEqual(det.get("numerology_bhagyank"), 3)
        self.assertEqual(det.get("kua_number"), 6)
        self.assertTrue(det.get("consent_profile_storage"))

    def test_dpdp_consent_ledger_audit_trail(self):
        """Verifies that statutory consent events are logged in the Consent Ledger."""
        test_email = "audit_ledger_seeker@example.org"
        payload = self.valid_payload.copy()
        payload["email"] = test_email
        payload["consent_profile_storage"] = True
        payload["consent_evaluation_feedback"] = True
        payload["consent_marketing"] = False

        res = self.client.post("/api/v1/auth/signup", json=payload)
        self.assertEqual(res.status_code, 200)
        uid = res.json()["user_id"]

        user_consents = [c for c in CONSENT_LEDGER if c.get("user_id") == uid]
        self.assertTrue(len(user_consents) >= 2)
        purposes = [c["purpose"] for c in user_consents]
        self.assertIn("profile_storage_and_calculations", purposes)
        self.assertIn("evaluation_feedback_flywheel", purposes)
        self.assertNotIn("marketing_and_transit_alerts", purposes)

    def test_login_and_me_profile_recall(self):
        """Verifies user login and profile retrieval via /api/v1/auth/me."""
        test_email = "login_recall_user@example.com"
        test_pass = "ComplexPass2026@"
        payload = self.valid_payload.copy()
        payload["email"] = test_email
        payload["password"] = test_pass

        # 1. Sign up
        res_signup = self.client.post("/api/v1/auth/signup", json=payload)
        self.assertEqual(res_signup.status_code, 200)

        # 2. Login with email and password
        res_login = self.client.post("/api/v1/auth/login", json={
            "login_id": test_email,
            "password": test_pass
        })
        self.assertEqual(res_login.status_code, 200)
        login_data = res_login.json()
        self.assertEqual(login_data["role"], "registered_user")
        token = login_data["session_token"]

        # 3. Call /me with Bearer token
        res_me = self.client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(res_me.status_code, 200)
        me_data = res_me.json()
        self.assertTrue(me_data["authenticated"])
        self.assertEqual(me_data["profile"]["email"], test_email)
        self.assertEqual(me_data["profile"]["name"], payload["name"])
        self.assertEqual(me_data["profile"]["driver_mulank"], 9)
        self.assertEqual(me_data["profile"]["conductor_bhagyank"], 3)

    def test_signup_place_coordinates_and_ampm_precision(self):
        """Verifies place of birth, country, latitude, longitude, timezone, and AM/PM time persistence."""
        test_email = "astrological_precision@example.com"
        payload = self.valid_payload.copy()
        payload["email"] = test_email
        payload["birth_place"] = "New Delhi, Delhi, India"
        payload["country"] = "India"
        payload["latitude"] = 28.6139
        payload["longitude"] = 77.2090
        payload["timezone"] = "Asia/Kolkata"
        payload["birth_time_hour"] = 6
        payload["birth_time_minute"] = 45
        payload["birth_time_period"] = "AM"
        payload["birth_time"] = "06:45 AM"

        res = self.client.post("/api/v1/auth/signup", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.json()
        prof = data.get("profile", {})

        # Assert profile responses
        self.assertEqual(prof.get("birth_place"), "New Delhi, Delhi, India")
        self.assertEqual(prof.get("country"), "India")
        self.assertEqual(prof.get("latitude"), 28.6139)
        self.assertEqual(prof.get("longitude"), 77.2090)
        self.assertEqual(prof.get("timezone"), "Asia/Kolkata")
        self.assertEqual(prof.get("birth_time_hour"), 6)
        self.assertEqual(prof.get("birth_time_minute"), 45)
        self.assertEqual(prof.get("birth_time_period"), "AM")
        self.assertEqual(prof.get("birth_time"), "06:45 AM")

        # Verify in CDP Golden Profile
        gid = data["golden_profile_id"]
        self.assertIn(gid, _GOLDEN_PROFILES)
        taxonomy = _GOLDEN_PROFILES[gid].get("deterministic_taxonomy", {})
        self.assertEqual(taxonomy.get("birth_place"), "New Delhi, Delhi, India")
        self.assertEqual(taxonomy.get("country"), "India")
        self.assertEqual(taxonomy.get("latitude"), 28.6139)
        self.assertEqual(taxonomy.get("longitude"), 77.2090)
        self.assertEqual(taxonomy.get("timezone"), "Asia/Kolkata")
        self.assertEqual(taxonomy.get("birth_time_period"), "AM")

        # Verify /me endpoint recall with Bearer token
        token = data["session_token"]
        res_me = self.client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
        self.assertEqual(res_me.status_code, 200)
        me_prof = res_me.json().get("profile", {})
        self.assertEqual(me_prof.get("birth_place"), "New Delhi, Delhi, India")
        self.assertEqual(me_prof.get("country"), "India")
        self.assertEqual(me_prof.get("latitude"), 28.6139)
        self.assertEqual(me_prof.get("longitude"), 77.2090)
        self.assertEqual(me_prof.get("timezone"), "Asia/Kolkata")
        self.assertEqual(me_prof.get("birth_time_hour"), 6)
        self.assertEqual(me_prof.get("birth_time_minute"), 45)
        self.assertEqual(me_prof.get("birth_time_period"), "AM")

    def test_twostep_onboarding_with_otp_and_altitude(self):
        """Verifies full two-step onboarding: Step 1 OTP verification + Step 2 birth matrix with altitude."""
        test_email = "twostep_seeker@example.com"
        test_phone = "+91 99887 76655"
        
        # Step 1: Send & verify OTP
        otp_send = self.client.post("/api/v1/auth/otp/send", json={"identifier": test_phone, "channel": "sms"})
        self.assertEqual(otp_send.status_code, 200)
        
        otp_ver = self.client.post("/api/v1/auth/otp/verify", json={"identifier": test_phone, "otp": "123456"})
        self.assertEqual(otp_ver.status_code, 200)
        v_token = otp_ver.json()["verification_token"]

        # Step 2: Submit complete birth matrix with altitude and statutory DPDP consent
        payload = self.valid_payload.copy()
        payload["email"] = test_email
        payload["phone"] = test_phone
        payload["verification_token"] = v_token
        payload["phone_verified"] = True
        payload["email_verified"] = True
        payload["altitude"] = 216.0
        payload["birth_place"] = "New Delhi"
        payload["country"] = "India"

        signup_resp = self.client.post("/api/v1/auth/signup", json=payload)
        self.assertEqual(signup_resp.status_code, 200)
        res_data = signup_resp.json()
        
        self.assertEqual(res_data["status"], "success")
        self.assertEqual(res_data["profile"]["altitude"], 216.0)
        self.assertTrue(res_data["profile"]["phone_verified"])

        # Check /me recalls altitude
        me_res = self.client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {res_data['session_token']}"})
        self.assertEqual(me_res.status_code, 200)
        self.assertEqual(me_res.json()["profile"]["altitude"], 216.0)


if __name__ == "__main__":
    unittest.main()
