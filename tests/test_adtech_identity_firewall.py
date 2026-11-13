import sys
import os
import unittest
import time

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.engine.identity_service import (
    PlatformType, ATTStatus, ConsentPurpose, ConsentStatus, ZERO_IDFA,
    register_platform_identity, record_consent, check_consent, withdraw_consent,
    link_identities, IDENTITY_REGISTRY, TOKENIZED_VAULT
)
from app.engine.adtech_firewall import (
    OutboundAdTechRequest, filter_and_activate_adtech_payload,
    APPROVED_PARTNERS, APPROVED_NON_SENSITIVE_SEGMENTS
)

class TestAdTechIdentityAndFirewall(unittest.TestCase):
    
    def test_mobile_web_identity_isolation(self):
        """Clauses 88 & 89: Mobile Web must use first-party web ID, not hardware/OS ad IDs."""
        res = register_platform_identity(PlatformType.MOBILE_WEB, user_id="user_web_001")
        self.assertEqual(res["platform"], "MOBILE_WEB")
        self.assertEqual(res["identifier_type"], "WEB_1P_ID")
        self.assertFalse(res["ad_tracking_eligible"])
        self.assertTrue(res["scoped_token"].startswith("tok_"))

    def test_pwa_identity_isolation(self):
        """Clauses 88 & 89: PWA must use first-party installation ID, not hardware/OS ad IDs."""
        res = register_platform_identity(PlatformType.PWA, user_id="user_pwa_001")
        self.assertEqual(res["platform"], "PWA")
        self.assertEqual(res["identifier_type"], "PWA_INSTALL_ID")
        self.assertFalse(res["ad_tracking_eligible"])

    def test_native_android_aaid(self):
        """Clause 90: Native Android uses Android Advertising ID with user-resettable vault token."""
        raw_aaid = "38400000-8cf0-11bd-b23e-10b96e4ef00d"
        res = register_platform_identity(
            PlatformType.NATIVE_ANDROID,
            user_id="user_droid_001",
            raw_identifier=raw_aaid
        )
        self.assertEqual(res["platform"], "NATIVE_ANDROID")
        self.assertEqual(res["identifier_type"], "ANDROID_ADVERTISING_ID")
        self.assertTrue(res["ad_tracking_eligible"])
        token = res["scoped_token"]
        self.assertIn(token, TOKENIZED_VAULT)
        self.assertNotEqual(TOKENIZED_VAULT[token], raw_aaid)  # Salt-hashed in vault

    def test_native_ios_att_denied(self):
        """Clause 91: Without ATT authorization, IDFA must return all zeros and anti-fingerprinting applies."""
        raw_idfa = "EA7583CD-A667-48BC-B806-42ECB2B48D12"
        res = register_platform_identity(
            PlatformType.NATIVE_IOS,
            user_id="user_ios_denied",
            raw_identifier=raw_idfa,
            att_status=ATTStatus.DENIED
        )
        self.assertEqual(res["platform"], "NATIVE_IOS")
        self.assertFalse(res["ad_tracking_eligible"])

    def test_native_ios_att_authorized(self):
        """Clause 91: With ATT authorization, IDFA is permitted in tokenized form."""
        raw_idfa = "EA7583CD-A667-48BC-B806-42ECB2B48D12"
        res = register_platform_identity(
            PlatformType.NATIVE_IOS,
            user_id="user_ios_auth",
            raw_identifier=raw_idfa,
            att_status=ATTStatus.AUTHORIZED
        )
        self.assertEqual(res["platform"], "NATIVE_IOS")
        self.assertTrue(res["ad_tracking_eligible"])
        token = res["scoped_token"]
        self.assertIn(token, TOKENIZED_VAULT)

    def test_granular_consent_and_cascading_withdrawal(self):
        """Clauses 92, 93, 104: Granular DPDP 2025 consent with cascading withdrawal."""
        ident = register_platform_identity(PlatformType.PWA, user_id="user_dpdp_001")
        id_id = ident["identity_id"]

        # Default deny
        self.assertFalse(check_consent(id_id, ConsentPurpose.ADVERTISING))
        self.assertFalse(check_consent(id_id, ConsentPurpose.LOCATION_FOR_VASTU))

        # Record affirmative consent for Vastu and Advertising
        record_consent(id_id, "user_dpdp_001", ConsentPurpose.LOCATION_FOR_VASTU, ConsentStatus.GRANTED)
        record_consent(id_id, "user_dpdp_001", ConsentPurpose.ADVERTISING, ConsentStatus.GRANTED)

        self.assertTrue(check_consent(id_id, ConsentPurpose.LOCATION_FOR_VASTU))
        self.assertTrue(check_consent(id_id, ConsentPurpose.ADVERTISING))

        # Withdraw Advertising consent
        withdrawn = withdraw_consent(id_id, ConsentPurpose.ADVERTISING)
        self.assertEqual(withdrawn["status"], "success")

        # Advertising now denied, but Vastu consent remains active (purpose isolation)
        self.assertFalse(check_consent(id_id, ConsentPurpose.ADVERTISING))
        self.assertTrue(check_consent(id_id, ConsentPurpose.LOCATION_FOR_VASTU))

    def test_data_firewall_blocks_sensitive_profile_data(self):
        """Clauses 87 & 148: Strict Data Firewall must intercept sensitive profile data."""
        ident = register_platform_identity(PlatformType.NATIVE_ANDROID, user_id="user_fw_001", raw_identifier="ad-12345")
        id_id = ident["identity_id"]
        record_consent(id_id, "user_fw_001", ConsentPurpose.ADVERTISING, ConsentStatus.GRANTED)

        # Candidate outbound payload containing sensitive service intelligence
        sensitive_payload = {
            "dob": "1981-11-28",
            "driver_number": 1,
            "conductor_number": 4,
            "divorce_risk": "high",
            "health_problem": "chronic gastric inflammation",
            "financial_distress": "severe debt in Saturn dasha",
            "remedies": ["Wear yellow sapphire", "Perform Rahu shanti"]
        }

        req = OutboundAdTechRequest(
            identity_id=id_id,
            target_partner_id="partner_google_ad_manager",
            purpose=ConsentPurpose.ADVERTISING,
            requested_segments=["seg_lang_english", "seg_geo_india_metro"],
            client_region="IN",
            service_payload_candidate=sensitive_payload
        )

        res = filter_and_activate_adtech_payload(req)
        self.assertEqual(res["status"], "APPROVED")
        # Ensure all sensitive fields were detected and blocked from outbound transmission
        blocked = res["blocked_sensitive_fields"]
        self.assertIn("dob", blocked)
        self.assertIn("divorce_risk", blocked)
        self.assertIn("health_problem", blocked)
        self.assertIn("financial_distress", blocked)
        self.assertIn("remedies", blocked)

        # Check that ONLY approved non-sensitive segments and scoped token are present
        self.assertEqual(res["approved_segments"], ["seg_lang_english", "seg_geo_india_metro"])
        self.assertTrue(res["identity_token"].startswith("tok_"))

    def test_data_firewall_fail_closed_without_consent(self):
        """Clause 212: Outbound AdTech payload without consent must FAIL CLOSED."""
        ident = register_platform_identity(PlatformType.PWA, user_id="user_no_consent")
        id_id = ident["identity_id"]

        req = OutboundAdTechRequest(
            identity_id=id_id,
            target_partner_id="partner_trade_desk",
            purpose=ConsentPurpose.ADVERTISING,
            requested_segments=["seg_lang_hindi"]
        )

        res = filter_and_activate_adtech_payload(req)
        self.assertEqual(res["status"], "BLOCKED")
        self.assertIn("Missing active affirmative consent", res["reason"])

if __name__ == "__main__":
    unittest.main()
