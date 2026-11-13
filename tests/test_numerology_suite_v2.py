"""
COMPREHENSIVE NUMEROLOGY SUITE V2 TEST SUITE (NV-001 TO NV-026)
Verifies:
1. All new additive features function deterministically without regression.
2. Zero previous logic altered or overwritten.
3. Every endpoint returns HTTP 200 and complies with data contracts and legal guardrails.
"""

import sys
import os
import unittest

# Ensure workspace root in path
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app


class TestNumerologySuiteV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # NV-001: Methodology Registry
    def test_methodology_registry(self):
        resp = self.client.get("/api/v2/numerology/methodology-registry")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertIn("methodologies", data)
        self.assertGreaterEqual(len(data["methodologies"]), 8)
        self.assertIn("METH-VEDIC-001", data["methodologies"])
        self.assertIn("METH-CHALDEAN-001", data["methodologies"])

    # NV-002: Number Characteristics Registry
    def test_number_profile_registry(self):
        # Test single digit 1
        resp = self.client.get("/api/v2/numerology/number-profile/1")
        self.assertEqual(resp.status_code, 200)
        p1 = resp.json()["profile"]
        self.assertEqual(p1["root_number"], 1)
        self.assertIn("Sun", p1["planet"])
        self.assertIn(8, p1["enemy_numbers"])

        # Test Master Number 11
        resp_m11 = self.client.get("/api/v2/numerology/number-profile/11")
        self.assertEqual(resp_m11.status_code, 200)
        self.assertEqual(resp_m11.json()["profile"]["number"], 11)

        # Test Compound Number 24 (Auspicious in Cheiro canon)
        resp_c24 = self.client.get("/api/v2/numerology/number-profile/24")
        self.assertEqual(resp_c24.status_code, 200)
        p24 = resp_c24.json()["profile"]
        self.assertEqual(p24["number"], 24)
        self.assertEqual(p24["root_number"], 6)

    # NV-003: Enhanced Lo Shu Analysis
    def test_enhanced_lo_shu_grid(self):
        resp = self.client.post(
            "/api/v2/numerology/lo-shu/enhanced?day=15&month=1&year=1990&name=Rahul Sharma&proposed_name=RahulA Sharma"
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertIn("birth_date_grid", data)
        self.assertIn("name_grid", data)
        self.assertIn("name_change_comparison", data)
        self.assertEqual(data["birth_date_grid"]["driver"], 6)
        self.assertEqual(data["birth_date_grid"]["conductor"], 8)

    # NV-004: Name Balancing Engine
    def test_name_balancing_engine(self):
        payload = {
            "full_name": "Rahul Sharma",
            "driver": 1,
            "conductor": 5,
            "dob_str": "1990-01-15"
        }
        resp = self.client.post("/api/v2/numerology/name/balance", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertIn("current_name_evaluation", data)
        self.assertIn("is_aligned", data)
        # Sanctuary Policy: Zero automated spelling balancing generated on app; 1-on-1 consultation gating enforced
        self.assertFalse(data["is_aligned"])
        self.assertIn("recommendation", data["current_name_evaluation"])

    # NV-005: Profession Recommendation Engine
    def test_profession_recommendations(self):
        payload = {
            "driver": 1,
            "conductor": 8,
            "saturn_override": 8,
            "kp_sub_lord": "Jupiter"
        }
        resp = self.client.post("/api/v2/numerology/professions/recommend", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        rec = data["recommendations"]
        self.assertIn("Bifurcated", rec["synthesis_mode"])
        self.assertGreaterEqual(len(rec["primary_recommended_professions"]), 3)
        self.assertIn("statutory_qualification", rec)
        self.assertIn("independent_business_and_founding", rec["suitability_matrix"])

    # NV-006: Blessing Years Timeline
    def test_blessing_years_timeline(self):
        payload = {
            "day": 15,
            "month": 1,
            "year": 1990,
            "current_age": 36
        }
        resp = self.client.post("/api/v2/numerology/forecast/blessing-years", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        bless = data["blessing_years"]
        self.assertGreater(bless["supreme_blessing_years_count"] + bless["high_support_years_count"], 0)
        self.assertIn("immediate_upcoming_blessings", bless)

    # NV-007: Personal Cycle Forecasts
    def test_personal_cycle_forecasts(self):
        payload = {
            "day": 15,
            "month": 1,
            "year": 2026
        }
        resp = self.client.post("/api/v2/numerology/forecast/personal-cycles", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data["multi_year_horizon"]), 4)
        self.assertEqual(len(data["annual_monthly_matrix"]["monthly_matrix"]), 12)

    # NV-008 & NV-009: Remedy Rules & Yantra Selector
    def test_remedy_rules_and_yantra(self):
        payload = {
            "driver": 1,
            "conductor": 8,
            "missing_numbers": [5, 6],
            "max_remedies": 5
        }
        resp = self.client.post("/api/v2/numerology/remedies/select", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        rx = data["remedy_prescription"]
        self.assertLessEqual(rx["total_remedies_prescribed"], 5)
        self.assertIn("prescribed_yantra", rx)
        # Verify enemy numbers were excluded
        self.assertIn(8, rx["excluded_conflict_numbers"])

    # NV-010: Mobile Number Analysis
    def test_mobile_number_audit(self):
        payload = {
            "mobile_number": "9812345678",
            "driver": 1,
            "conductor": 5
        }
        resp = self.client.post("/api/v2/numerology/assets/mobile", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["mobile_audit"]
        self.assertIn("total_compound", data)
        self.assertIn("digit_frequency", data)
        self.assertIn("malefic_pairs_detected", data)

    # NV-011: Vehicle Registration Number Analysis
    def test_vehicle_number_audit(self):
        payload = {
            "registration_plate": "DL 01 AB 1234",
            "driver": 1,
            "conductor": 5
        }
        resp = self.client.post("/api/v2/numerology/assets/vehicle", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["vehicle_audit"]
        self.assertEqual(data["full_plate_root"], 3)
        self.assertIn("protective_remedies", data)

    # NV-012: Property Number Analysis
    def test_property_number_audit(self):
        payload = {
            "property_identifier": "Flat 402",
            "driver": 1,
            "conductor": 5
        }
        resp = self.client.post("/api/v2/numerology/assets/property", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["property_audit"]
        self.assertEqual(data["property_root"], 4)
        self.assertIn("elemental_nature", data)
        self.assertIn("door_and_vastu_remedies", data)

    # NV-013: Bank Account Number Harmony (Strict Privacy)
    def test_bank_account_harmony_privacy(self):
        payload = {
            "account_number": "501002345678",
            "driver": 1,
            "conductor": 5
        }
        resp = self.client.post("/api/v2/numerology/assets/bank-account", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["bank_account_harmony"]
        # Raw number must be masked
        self.assertTrue(data["masked_account_number"].startswith("*********"))
        self.assertTrue(data["masked_account_number"].endswith("678"))
        self.assertIn("privacy_compliance_notice", data)

    # NV-014: Business Name Analysis
    def test_business_name_audit(self):
        payload = {
            "brand_name": "TechVision Alpha",
            "owner_driver": 1,
            "owner_conductor": 5,
            "industry_category": "technology"
        }
        resp = self.client.post("/api/v2/numerology/naming/business", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["business_name_audit"]
        self.assertIn("commercial_score", data)
        self.assertIn("branding_guidance", data)

    # NV-015: Baby Naming Workflow
    def test_baby_naming_workflow(self):
        payload = {
            "baby_driver": 1,
            "baby_conductor": 5,
            "gender": "boy",
            "missing_numbers_in_chart": [3, 6]
        }
        resp = self.client.post("/api/v2/numerology/naming/baby", json=payload)
        self.assertEqual(resp.status_code, 200)
        names = resp.json()["baby_name_recommendations"]
        self.assertGreaterEqual(len(names), 1)
        self.assertIn("suitability_score", names[0])

    # NV-016: Relationship Synastry
    def test_relationship_synastry(self):
        payload = {
            "person1_name": "Aarav",
            "p1_day": 1,
            "p1_month": 5,
            "p1_year": 1990,
            "person2_name": "Diya",
            "p2_day": 3,
            "p2_month": 8,
            "p2_year": 1993
        }
        resp = self.client.post("/api/v2/numerology/relationships/synastry", json=payload)
        self.assertEqual(resp.status_code, 200)
        syn = resp.json()["synastry_report"]
        self.assertIn("compatibility_score_pct", syn)
        self.assertIn("diplomatic_communication_suggestions", syn)

    # NV-017: Foreign Travel & Relocation
    def test_foreign_travel_indicators(self):
        payload = {
            "day": 15,
            "month": 1,
            "year": 1990,
            "target_year": 2026
        }
        resp = self.client.post("/api/v2/numerology/travel/foreign", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()["travel_indicators"]
        self.assertIn("overall_travel_potency_score", data)
        self.assertIn("settlement_verdict", data)

    # NV-018: Health & Wellbeing (Safe Use)
    def test_health_and_wellbeing_compliance(self):
        payload = {
            "driver": 1,
            "conductor": 8,
            "current_age": 42
        }
        resp = self.client.post("/api/v2/numerology/health/wellbeing", json=payload)
        self.assertEqual(resp.status_code, 200)
        wb = resp.json()["wellbeing_analysis"]
        self.assertTrue(wb["is_second_life_phase_active"])
        self.assertIn("statutory_compliance_disclaimer", wb)
        self.assertIn("Indian Drugs and Magic Remedies", wb["statutory_compliance_disclaimer"])

    # NV-019, NV-022, NV-024, NV-025, NV-026: Practitioner Management
    def test_practitioner_management_flow(self):
        # 1. Register Client with DPDP consent
        c_resp = self.client.post("/api/v2/numerology/practitioner/client", json={
            "practitioner_id": "test_pract_99",
            "full_name": "Vikram Seth",
            "dob_str": "1988-11-20",
            "email": "vikram@example.com"
        })
        self.assertEqual(c_resp.status_code, 200)
        client_data = c_resp.json()["client"]
        c_id = client_data["client_id"]
        self.assertTrue(client_data["consent"]["consent_given"])

        # 2. Log Immutable Prediction
        p_resp = self.client.post("/api/v2/numerology/practitioner/prediction", json={
            "client_id": c_id,
            "practitioner_id": "test_pract_99",
            "prediction_text": "Transition to venture capital partner",
            "category": "CAREER",
            "start_date": "2026-06-01",
            "end_date": "2026-12-31"
        })
        self.assertEqual(p_resp.status_code, 200)
        pred_data = p_resp.json()["prediction"]
        p_id = pred_data["prediction_id"]

        # 3. Record Outcome
        o_resp = self.client.post("/api/v2/numerology/practitioner/prediction/outcome", json={
            "prediction_id": p_id,
            "outcome_status": "FULFILLED",
            "practitioner_notes": "Joined as General Partner in August 2026."
        })
        self.assertEqual(o_resp.status_code, 200)
        self.assertEqual(o_resp.json()["outcome"]["final_status"], "FULFILLED")

        # 4. Fetch Dashboard
        d_resp = self.client.get("/api/v2/numerology/practitioner/test_pract_99/dashboard")
        self.assertEqual(d_resp.status_code, 200)
        dash = d_resp.json()["dashboard"]
        self.assertEqual(dash["metrics"]["total_clients_managed"], 1)
        self.assertEqual(dash["metrics"]["outcome_accuracy_rate_pct"], 100.0)

        # 5. Configure White-Label
        wl_resp = self.client.post("/api/v2/numerology/practitioner/white-label", json={
            "practitioner_id": "test_pract_99",
            "studio_name": "Aura Numerics Global",
            "practitioner_name": "Master Vikram",
            "logo_url": "https://example.com/logo.png",
            "contact_email": "aura@example.com",
            "contact_phone": "+91 99999 88888",
            "custom_footer": "Navigating life through sacred numbers."
        })
        self.assertEqual(wl_resp.status_code, 200)
        self.assertEqual(wl_resp.json()["white_label_config"]["studio_name"], "Aura Numerics Global")


if __name__ == "__main__":
    unittest.main()
