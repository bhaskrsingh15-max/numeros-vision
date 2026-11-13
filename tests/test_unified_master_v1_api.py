"""
NUMEROS VISION — UNIFIED MASTER SPECIFICATION V1 API TEST SUITE
Tests the 9 Canonical V1 Endpoints, Methodology Isolation, Compound Preservation,
and Publication Gate under Version 1.0 Implementation Specification.
"""

import unittest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from app.main import app
from app.engine.methodology_registry import list_methodologies, get_methodology


class TestUnifiedMasterV1API(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_methodology_registry_includes_pythagorean(self):
        """Verifies METH-PYTH-001 is active in the methodology registry."""
        meth = get_methodology("METH-PYTH-001")
        self.assertIsNotNone(meth, "METH-PYTH-001 must be registered")
        self.assertEqual(meth["school"], "Pythagorean Western Numerology")
        self.assertEqual(meth["version"], "1.0.0")

    def test_1_profile_validate(self):
        """Tests POST /v1/profile/validate for valid and invalid inputs."""
        # 1. Valid request
        resp = self.client.post("/v1/profile/validate", json={
            "name": "Aarav Sharma",
            "day": 15,
            "month": 8,
            "year": 1990,
            "mobile": "9876543210",
            "consent": True
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "VALIDATED")
        self.assertTrue(data["profile_id"].startswith("NV-PROF-"))
        self.assertEqual(data["normalized_profile"]["masked_mobile"], "XXXXXX3210")
        self.assertTrue(data["consent_audit"]["dpdp_act_compliant"])

        # 2. Invalid date (Feb 30)
        resp_invalid = self.client.post("/v1/profile/validate", json={
            "name": "Invalid Date Native",
            "day": 30,
            "month": 2,
            "year": 1995,
            "consent": True
        })
        self.assertEqual(resp_invalid.status_code, 422)

        # 3. Missing consent
        resp_no_consent = self.client.post("/v1/profile/validate", json={
            "name": "No Consent Native",
            "day": 1,
            "month": 1,
            "year": 1990,
            "consent": False
        })
        self.assertEqual(resp_no_consent.status_code, 400)

    def test_2_numbers_calculate_across_methodologies(self):
        """Tests POST /v1/numbers/calculate across Vedic, Chaldean, Lo Shu, and Pythagorean."""
        # A. Vedic (METH-VEDIC-001)
        resp_v = self.client.post("/v1/numbers/calculate", json={
            "methodology_id": "METH-VEDIC-001",
            "day": 15,
            "month": 8,
            "year": 1990
        })
        self.assertEqual(resp_v.status_code, 200)
        dv = resp_v.json()
        self.assertEqual(dv["calculation_output"]["driver_number"], 6)  # 15 -> 6
        self.assertEqual(dv["calculation_output"]["conductor_number"], 6)  # 1+5+8+1+9+9+0 = 33 -> 6

        # B. Chaldean (METH-CHALDEAN-001)
        resp_c = self.client.post("/v1/numbers/calculate", json={
            "methodology_id": "METH-CHALDEAN-001",
            "day": 1,
            "month": 1,
            "year": 1990,
            "name": "Aarav Sharma"
        })
        self.assertEqual(resp_c.status_code, 200)
        dc = resp_c.json()
        self.assertIn("compound_sum", dc["calculation_output"])
        self.assertIn("single_root", dc["calculation_output"])

        # C. Lo Shu (METH-LOSHU-001)
        resp_l = self.client.post("/v1/numbers/calculate", json={
            "methodology_id": "METH-LOSHU-001",
            "day": 15,
            "month": 8,
            "year": 1990
        })
        self.assertEqual(resp_l.status_code, 200)
        dl = resp_l.json()
        self.assertIn("digit_counts", dl["calculation_output"])

        # D. Pythagorean (METH-PYTH-001)
        resp_p = self.client.post("/v1/numbers/calculate", json={
            "methodology_id": "METH-PYTH-001",
            "day": 15,
            "month": 8,
            "year": 1990,
            "name": "Aarav Sharma"
        })
        self.assertEqual(resp_p.status_code, 200)
        dp = resp_p.json()
        self.assertIn("life_path", dp["calculation_output"])
        self.assertIn("pinnacles_and_cycles", dp["calculation_output"])

    def test_3_numbers_decode_compound_preservation(self):
        """Tests POST /v1/numbers/decode preserves compound numbers (Section 6)."""
        # Test 23/5 compound decoding
        resp = self.client.post("/v1/numbers/decode", json={
            "number": 23,
            "methodology_id": "METH-CHALDEAN-001",
            "compound_value": 23
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["compound_value"], 23)
        self.assertEqual(data["reduced_root"], 5)
        self.assertIn("23", data["decomposition"]["compound_root_relationship"])
        self.assertIn("5", data["decomposition"]["compound_root_relationship"])

        # Test Western Karmic Debt 14/5
        resp_karmic = self.client.post("/v1/numbers/decode", json={
            "number": 14,
            "methodology_id": "METH-PYTH-001",
            "compound_value": 14
        })
        self.assertEqual(resp_karmic.status_code, 200)
        dk = resp_karmic.json()
        self.assertIsNotNone(dk["decomposition"]["western_karmic_debt"])
        self.assertEqual(dk["decomposition"]["western_karmic_debt"]["karmic_debt"], 14)

    def test_4_correlations_analyze(self):
        """Tests POST /v1/correlations/analyze pairwise evaluations (Section 9)."""
        resp = self.client.post("/v1/correlations/analyze", json={
            "day": 15,
            "month": 8,
            "year": 1990,
            "name": "Aarav Sharma"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "CORRELATED")
        self.assertGreaterEqual(len(data["pairwise_correlations"]), 3)
        for pair in data["pairwise_correlations"]:
            self.assertIn("pair", pair)
            self.assertIn("classification", pair)
            self.assertIn("evidence_basis", pair)

    def test_5_forecast_generate(self):
        """Tests POST /v1/forecast/generate bounded cycles and limitations (Section 10)."""
        resp = self.client.post("/v1/forecast/generate", json={
            "day": 15,
            "month": 8,
            "year": 1990,
            "current_age": 34
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "FORECAST_GENERATED")
        self.assertIn("statutory_limitation", data)
        self.assertIn("blessing_years_milestones", data)
        self.assertIn("multi_year_horizon", data)

    def test_6_remedies_recommend(self):
        """Tests POST /v1/remedies/recommend safe source-grounded remedies (Section 11)."""
        resp = self.client.post("/v1/remedies/recommend", json={
            "driver": 6,
            "conductor": 6,
            "missing_numbers": [3, 7, 8],
            "max_remedies": 5
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "RECOMMENDED")
        self.assertIn("safety_certification", data)
        self.assertIn("remedy_prescription", data)
        self.assertIn("grounded_rag_citations", data)

    def test_7_reports_individual(self):
        """Tests POST /v1/reports/individual structured generation (Section 16 & 17)."""
        resp = self.client.post("/v1/reports/individual", json={
            "methodology_id": "METH-VEDIC-001",
            "day": 15,
            "month": 8,
            "year": 1990,
            "name": "Aarav Sharma",
            "package": "basic",
            "language": "en"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "PUBLISHED")
        self.assertEqual(data["report_type"], "individual")
        self.assertIn("deterministic_calculations", data)
        self.assertIn("governed_rag_evidence", data)

    def test_8_reports_consolidated(self):
        """Tests POST /v1/reports/consolidated cross-system synthesis (Section 16)."""
        resp = self.client.post("/v1/reports/consolidated", json={
            "day": 15,
            "month": 8,
            "year": 1990,
            "name": "Aarav Sharma",
            "methodologies": ["METH-VEDIC-001", "METH-CHALDEAN-001", "METH-LOSHU-001", "METH-PYTH-001"],
            "package": "advanced"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "PUBLISHED")
        self.assertEqual(data["report_type"], "consolidated")
        self.assertIn("integrated_synthesis", data)
        self.assertIn("disclosed_methodology_conflicts", data["integrated_synthesis"])

    def test_9_reports_validate_gate(self):
        """Tests POST /v1/reports/validate 12-Stage Hallucination Gate (Section 14 & 15)."""
        # A. Clean valid report mapped to calculation ID
        resp_valid = self.client.post("/v1/reports/validate", json={
            "report_text": "The native is guided by Driver 6 and Conductor 6, with Venus as the governing celestial vibration.",
            "calculation_ids": ["CALC-001"],
            "rule_ids": ["METH-VEDIC-001"],
            "source_ids": ["SRC-VEDIC-001"]
        })
        self.assertEqual(resp_valid.status_code, 200)
        dv = resp_valid.json()
        self.assertTrue(dv["publication_allowed"])
        self.assertEqual(dv["action_required"], "PUBLISH")

        # B. Report with prohibited medical guarantee claim
        resp_unsafe = self.client.post("/v1/reports/validate", json={
            "report_text": "Wearing this gemstone will cure heart attack and replace your doctor completely.",
            "calculation_ids": ["CALC-001"],
            "rule_ids": ["METH-VEDIC-001"],
            "source_ids": ["SRC-VEDIC-001"]
        })
        self.assertEqual(resp_unsafe.status_code, 200)
        du = resp_unsafe.json()
        self.assertFalse(du["publication_allowed"])
        self.assertEqual(du["action_required"], "REGENERATE_OR_BLOCK")


if __name__ == "__main__":
    unittest.main()
