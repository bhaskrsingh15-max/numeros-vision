import sys
import os
import unittest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.engine.cdp_identity_engine import (
    normalize_email, normalize_phone, hash_sha256,
    resolve_golden_profile, enrich_audience_taxonomy,
    build_meta_capi_payload, IdentityPayload
)

class TestCDPIdentityEngine(unittest.TestCase):
    def test_normalization_and_hashing(self):
        # Email: should trim, lowercase, remove dots for gmail, remove sub-address plus
        raw_email = "  John.Doe+numerology@Gmail.com "
        norm = normalize_email(raw_email)
        self.assertEqual(norm, "johndoe@gmail.com")
        self.assertEqual(len(hash_sha256(norm)), 64)

        # Phone: E.164 normalization
        raw_phone = "+91 (987) 654-3210"
        norm_ph = normalize_phone(raw_phone)
        self.assertEqual(norm_ph, "919876543210")
        self.assertEqual(len(hash_sha256(norm_ph)), 64)

    def test_identity_graph_merger(self):
        # Step 1: Anonymous web visit with 1P cookie and fbp
        p1 = IdentityPayload(
            nv_uid="nv_cookie_12345",
            fbp="fb.1.1689000000.123456",
            client_ip="103.21.12.4"
        )
        prof1 = resolve_golden_profile(p1)
        golden_id = prof1["golden_profile_id"]
        self.assertTrue(golden_id.startswith("gp_"))

        # Step 2: Later, user submits free scorecard with email
        p2 = IdentityPayload(
            nv_uid="nv_cookie_12345",
            email="aarav.sharma@example.com"
        )
        prof2 = resolve_golden_profile(p2)
        # Must resolve to the SAME golden_id because nv_uid matched!
        self.assertEqual(prof2["golden_profile_id"], golden_id)
        self.assertIn("email_sha256", prof2["hashes"])

        # Step 3: Later, user pays with phone number on Razorpay
        p3 = IdentityPayload(
            email="aarav.sharma@example.com",
            phone="+91 98765 43210"
        )
        prof3 = resolve_golden_profile(p3)
        # Must resolve to the SAME golden_id because email matched!
        self.assertEqual(prof3["golden_profile_id"], golden_id)
        self.assertIn("phone_sha256", prof3["hashes"])

    def test_dual_audience_taxonomy_enrichment(self):
        p = IdentityPayload(email="test@numerosvision.com", phone="919999999999")
        prof = resolve_golden_profile(p)
        gid = prof["golden_profile_id"]

        chart_data = {
            "sun_sign": "Leo",
            "moon_sign": "Aries",
            "lagna": "Scorpio",
            "mulank": 1,
            "bhagyank": 8,
            "mahadasha": "Saturn",
            "antardasha": "Mercury",
            "missing_numbers": [4, 5, 6],
            "is_saturn_challenging": True
        }
        tx_data = {
            "purchase_count": 2,
            "total_spend_inr": 1098
        }
        beh_data = {
            "page_views_career": 4,
            "page_views_love": 1,
            "viewed_business_consultation": True
        }

        enriched = enrich_audience_taxonomy(gid, chart_data, tx_data, beh_data)
        
        # Verify Deterministic Taxonomy
        det = enriched["deterministic_taxonomy"]
        self.assertEqual(det["numerology_mulank"], 1)
        self.assertEqual(det["customer_tier"], "MASTER_REPORT_BUYER")
        self.assertEqual(det["active_mahadasha"], "Saturn")

        # Verify Probabilistic Taxonomy
        prob = enriched["probabilistic_taxonomy"]
        self.assertGreaterEqual(prob["career_pivot_propensity"], 0.7)
        self.assertGreaterEqual(prob["transit_friction_index"], 0.6)
        self.assertGreaterEqual(prob["hni_affluence_propensity"], 0.5)

    def test_meta_capi_high_match_payload(self):
        p = IdentityPayload(
            email="client@domain.com",
            phone="+91 91234 56789",
            fbp="fb.1.1234.5678",
            client_ip="122.161.45.10",
            client_user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 17_0)"
        )
        prof = resolve_golden_profile(p)
        gid = prof["golden_profile_id"]

        capi = build_meta_capi_payload(
            golden_profile_id=gid,
            event_name="Purchase",
            event_id="evt_tx_12345",
            event_source_url="https://numerosvision.com/checkout/success",
            value=499.0,
            currency="INR"
        )

        user_data = capi["data"][0]["user_data"]
        # Must have at least 5 match keys for Event Match Quality > 8.5
        self.assertIn("em", user_data)
        self.assertIn("ph", user_data)
        self.assertIn("fbp", user_data)
        self.assertIn("client_ip_address", user_data)
        self.assertIn("client_user_agent", user_data)
        self.assertIn("external_id", user_data)

    def test_iab_sda_openrtb_and_uid2(self):
        from app.engine.cdp_identity_engine import build_iab_sda_user_data, generate_uid2_token

        p = IdentityPayload(
            email="iab.client@numerosvision.com",
            phone="+91 99887 76655",
            consent_opt_in=True
        )
        prof = resolve_golden_profile(p)
        gid = prof["golden_profile_id"]

        chart_data = {
            "sun_sign": "Scorpio",
            "mulank": 8,
            "bhagyank": 4,
            "mahadasha": "Rahu",
            "is_saturn_challenging": True
        }
        tx_data = {"purchase_count": 3, "total_spend_inr": 2499}
        beh_data = {"page_views_career": 6, "viewed_business_consultation": True}

        enrich_audience_taxonomy(gid, chart_data, tx_data, beh_data)

        # 1. Test IAB OpenRTB Seller-Defined Audiences (Curated Audiences)
        sda_data = build_iab_sda_user_data(gid)
        self.assertIn("segment", sda_data)
        self.assertEqual(sda_data["name"], "numerosvision.com")
        self.assertEqual(sda_data["ext"]["segtax"], 4)
        
        segment_ids = [s["id"] for s in sda_data["segment"]]
        # 137 is Career Transition, 782 is Wealth Investment, 52 is HNI Affluent
        self.assertIn("137", segment_ids)
        self.assertIn("782", segment_ids)

        # 2. Test UID2 Token Generation
        uid2 = generate_uid2_token(gid)
        self.assertIsNotNone(uid2)
        self.assertTrue(uid2.startswith("UID2_v2_"))

    def test_device_and_advertising_id_capture_with_consent(self):
        # 1. Android Mobile with GAID and explicit consent
        payload_android = IdentityPayload(
            email="arjun.patel@example.com",
            device_id="nv_dev_android_sm_s24",
            device_type="mobile",
            gaid_aaid="38400000-8cf0-11bd-b23e-10b96e40000d",
            consent_marketing=True,
            consent_device_tracking=True
        )
        prof_android = resolve_golden_profile(payload_android)
        gid = prof_android["golden_profile_id"]
        
        self.assertEqual(prof_android["devices"]["primary_device_id"], "nv_dev_android_sm_s24")
        self.assertEqual(prof_android["devices"]["device_type"], "mobile")
        self.assertEqual(prof_android["ad_ids"]["gaid"], "38400000-8cf0-11bd-b23e-10b96e40000d")

        # 2. Re-visit from same device without email -> must stitch to same Golden Profile ID!
        payload_return = IdentityPayload(
            device_id="nv_dev_android_sm_s24",
            consent_device_tracking=True
        )
        prof_return = resolve_golden_profile(payload_return)
        self.assertEqual(prof_return["golden_profile_id"], gid)

        # 3. iPad Tablet with Apple IDFA and ATT Consent
        payload_ipad = IdentityPayload(
            email="meera.nair@example.com",
            device_id="nv_dev_ipad_pro_13",
            device_type="tablet",
            idfa="EA7583CD-A667-48BC-B806-42ECB2B48D12",
            consent_marketing=True,
            consent_device_tracking=True
        )
        prof_ipad = resolve_golden_profile(payload_ipad)
        self.assertEqual(prof_ipad["devices"]["device_type"], "tablet")
        self.assertEqual(prof_ipad["ad_ids"]["idfa"], "ea7583cd-a667-48bc-b806-42ecb2b48d12")

    def test_consent_denial_scrubbing(self):
        # If user explicitly denies consent (e.g. DPDP / ATT / GDPR opt-out)
        payload_optout = IdentityPayload(
            email="optout.user@example.com",
            device_id="nv_dev_secret_device",
            gaid_aaid="99999999-8cf0-11bd-b23e-10b96e40000d",
            idfa="88888888-A667-48BC-B806-42ECB2B48D12",
            consent_marketing=False,
            consent_device_tracking=False
        )
        prof_optout = resolve_golden_profile(payload_optout)
        
        # Ad IDs must NOT be recorded
        self.assertNotIn("gaid", prof_optout.get("ad_ids", {}))
        self.assertNotIn("idfa", prof_optout.get("ad_ids", {}))
        self.assertEqual(prof_optout.get("consent_device_tracking"), False)

    def test_omnichannel_taxonomy_sync_and_multi_key_lookup(self):
        from app.engine.cdp_identity_engine import sync_omnichannel_taxonomy, lookup_taxonomy_by_any_identifier
        
        # 1. Sync full omnichannel identity record with separate taxonomies
        synced = sync_omnichannel_taxonomy(
            phone="+91 98200 88776",
            email="rajesh.oberoi@oberoigroup.com",
            device_id="nv_dev_iphone_16_pro",
            device_type="mobile",
            idfa="55555555-8cf0-11bd-b23e-10b96e40000a",
            deterministic_attributes={
                "numerology_mulank": 1,
                "numerology_bhagyank": 9,
                "astro_sun_sign": "Leo",
                "active_mahadasha": "Sun",
                "total_spend_inr": 11400.0,
                "customer_tier": "HNI_CONSULTATION_CLIENT"
            },
            probabilistic_attributes={
                "career_pivot_propensity": 0.85,
                "hni_affluence_propensity": 0.95,
                "marriage_urgency_propensity": 0.20,
                "transit_friction_index": 0.35
            }
        )
        self.assertEqual(synced["status"], "success")
        gid = synced["golden_profile_id"]
        
        # Verify separate deterministic taxonomy
        det = synced["deterministic_taxonomy"]
        self.assertEqual(det["numerology_mulank"], 1)
        self.assertEqual(det["customer_tier"], "HNI_CONSULTATION_CLIENT")
        
        # Verify separate probabilistic taxonomy
        prob = synced["probabilistic_taxonomy"]
        self.assertEqual(prob["career_pivot_propensity"], 0.85)
        self.assertEqual(prob["hni_affluence_propensity"], 0.95)

        # 2. Lookup by Mobile Number (E.164 formatted or digits)
        res_phone = lookup_taxonomy_by_any_identifier("+919820088776")
        self.assertIsNotNone(res_phone)
        self.assertEqual(res_phone["golden_profile_id"], gid)
        self.assertEqual(res_phone["deterministic_taxonomy"]["numerology_mulank"], 1)
        self.assertEqual(res_phone["probabilistic_taxonomy"]["career_pivot_propensity"], 0.85)

        # 3. Lookup by Email ID
        res_email = lookup_taxonomy_by_any_identifier("rajesh.oberoi@oberoigroup.com")
        self.assertIsNotNone(res_email)
        self.assertEqual(res_email["golden_profile_id"], gid)

        # 4. Lookup by Device ID
        res_device = lookup_taxonomy_by_any_identifier("nv_dev_iphone_16_pro")
        self.assertIsNotNone(res_device)
        self.assertEqual(res_device["golden_profile_id"], gid)

        # 5. Lookup by Advertising ID (IDFA)
        res_idfa = lookup_taxonomy_by_any_identifier("55555555-8cf0-11bd-b23e-10b96e40000a")
        self.assertIsNotNone(res_idfa)
        self.assertEqual(res_idfa["golden_profile_id"], gid)
        self.assertEqual(res_idfa["mapped_identifiers"]["primary_device_id"], "nv_dev_iphone_16_pro")

if __name__ == "__main__":
    unittest.main()
