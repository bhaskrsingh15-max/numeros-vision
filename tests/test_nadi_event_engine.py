"""
UNIT TEST SUITE FOR NADI EVENT INTELLIGENCE ENGINE
==================================================
Tests:
  1. Standard Career Evaluation & Hierarchy
  2. Business Evaluation & Significators
  3. Property & Asset Evaluation
  4. Missing Input Handling (Missing DOB)
  5. Past Milestone Calibration Flow
  6. Statutory PCPNDT Circuit Breaker (Blocked Sex Prediction)
  7. Public Output Neutrality & Clean Vocabulary
"""

import unittest
from app.engine.nadi_event_engine import evaluate_nadi_event

class TestNadiEventEngine(unittest.TestCase):
    def test_career_event_evaluation(self):
        birth_data = {
            "dob": "1988-06-15",
            "tob": "14:30",
            "latitude": 28.6139,
            "longitude": 77.2090
        }
        result = evaluate_nadi_event(birth_data, "When will I get a promotion or career advancement?")
        self.assertEqual(result["status"], "EVALUATED_SUCCESS")
        self.assertEqual(result["event_category"], "career")
        self.assertIn("provenance", str(result).lower())
        self.assertEqual(result["vibrational_evidence"]["source_provenance"]["author"], "Numeros Vision Classical Archive")
        self.assertEqual(result["vibrational_evidence"]["source_provenance"]["pdf_page"], 110)
        self.assertIn(result["temporal_rhythm"]["alignment_strength"], ("STRONG_STABLE", "MODERATE", "CONDITIONAL"))

    def test_business_event_evaluation(self):
        birth_data = {
            "dob": "1992-11-04",
            "tob": "09:15",
            "latitude": 19.0760,
            "longitude": 72.8777
        }
        result = evaluate_nadi_event(birth_data, "Can I start a new business venture or partnership?", event_category="career_business")
        self.assertEqual(result["status"], "EVALUATED_SUCCESS")
        self.assertEqual(result["event_category"], "career_business")
        self.assertIn(7, result["vibrational_evidence"]["resonant_houses"])
        self.assertIn("Mercury", result["vibrational_evidence"]["primary_significators"])

    def test_property_event_evaluation(self):
        birth_data = {
            "dob": "1985-03-22",
            "tob": "18:00",
            "latitude": 12.9716,
            "longitude": 77.5946
        }
        result = evaluate_nadi_event(birth_data, "Should I buy a flat or land this year?")
        self.assertEqual(result["status"], "EVALUATED_SUCCESS")
        self.assertEqual(result["event_category"], "property")
        self.assertIn(4, result["vibrational_evidence"]["resonant_houses"])
        self.assertIn("Mars", result["vibrational_evidence"]["primary_significators"])

    def test_missing_dob_input(self):
        birth_data = {"tob": "14:30"}
        result = evaluate_nadi_event(birth_data, "Tell me about my career")
        self.assertEqual(result["status"], "MISSING_REQUIRED_INPUT")
        self.assertIn("dob", result["missing_fields"])

    def test_milestone_calibration_flow(self):
        birth_data = {
            "dob": "1990-05-10",
            "tob": "11:20",
            "latitude": 28.7041,
            "longitude": 77.1025
        }
        milestones = [
            {"date": "2015-08-01", "event": "First corporate job"},
            {"date": "2020-02-14", "event": "Marriage"}
        ]
        result = evaluate_nadi_event(birth_data, "Career prospects", past_milestones=milestones)
        self.assertEqual(result["status"], "EVALUATED_SUCCESS")
        self.assertEqual(result["calibration"]["status"], "CALIBRATED_WITH_MILESTONES")

    def test_pcpndt_statutory_circuit_breaker(self):
        birth_data = {"dob": "1995-08-20"}
        result = evaluate_nadi_event(birth_data, "Will my next baby be a boy or girl?")
        self.assertEqual(result["status"], "PERMANENTLY_BLOCKED")
        self.assertEqual(result["error_code"], "STATUTORY_VIOLATION_PCPNDT")
        self.assertIn("PCPNDT", result["message"])
        self.assertIn("PCPNDT Act 1994", result["statutory_reference"])

    def test_public_output_neutrality(self):
        birth_data = {
            "dob": "1987-12-05",
            "tob": "07:30",
            "latitude": 26.9124,
            "longitude": 75.7873
        }
        result = evaluate_nadi_event(birth_data, "What are my career prospects?")
        res_str = str(result)
        self.assertNotIn("hard-coded algorithms", res_str)
        self.assertNotIn("trade secret", res_str.lower())
        remedy = result.get("optional_harmonic_remedy", {})
        self.assertTrue("practical_summary" in remedy or "safety_notes" in remedy)

if __name__ == '__main__':
    unittest.main()

