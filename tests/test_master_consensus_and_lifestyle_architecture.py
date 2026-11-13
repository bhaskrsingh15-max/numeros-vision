"""
NUMEROS VISION — MASTER CONSENSUS & LIFESTYLE ARCHITECTURE TESTS
=================================================================
Automated verification of:
1. Multi-System Consensus Engine & Correlation-Aware System Families
2. Convergence Ratio & Strict Consensus Statuses
3. Vedic Lifestyle Transformation (Dinacharya & Sattvic Routines)
4. Safe Crystal Healing with Planetary Enemy Exclusions
5. Statutory Drugs & Magic Remedies Act 1954 Compliance Notice
6. Layman Narrative Synthesis & Past-Pattern Validation Question
7. Quarantined Offline Feedback Evaluation Ledger
"""

import unittest
from datetime import date
from app.engine.consensus import generate_consensus_reading, SAFE_CRYSTAL_CATALOGUE
from app.engine.charm_resonance_engine import charm_resonance


class TestMasterConsensusAndLifestyleArchitecture(unittest.TestCase):

    def setUp(self):
        # Driver 6 (Venus), Conductor 2 (Moon)
        self.report = generate_consensus_reading("Bhaskr Singh", 15, 8, 1995)

    def test_multi_system_consensus_structure(self):
        consensus = self.report.get("multi_system_consensus")
        self.assertIsNotNone(consensus, "multi_system_consensus must be present")
        
        # Status validation
        valid_statuses = [
            "convergent", "partially_convergent", "conflicted",
            "single_system", "insufficient_evidence", "not_comparable", "neutral"
        ]
        self.assertIn(consensus["consensus_status"], valid_statuses)
        self.assertIsInstance(consensus["convergence_ratio"], float)
        self.assertGreaterEqual(consensus["convergence_ratio"], 0.0)
        self.assertLessEqual(consensus["convergence_ratio"], 1.0)

        # 6 System Families
        families = consensus["system_families"]
        expected_families = [
            "numerology_core", "acoustics", "numerology_comparative",
            "astrology_classical", "astrology_nadi", "astrology_remedial"
        ]
        for ef in expected_families:
            self.assertIn(ef, families, f"Family {ef} must be present in consensus")
            self.assertIn("direction", families[ef])

    def test_vedic_lifestyle_dinacharya(self):
        lifestyle = self.report.get("vedic_lifestyle_transformation")
        self.assertIsNotNone(lifestyle, "vedic_lifestyle_transformation must be present")
        
        dina = lifestyle.get("dinacharya_circadian_routine", {})
        self.assertIn("brahma_muhurta", dina)
        self.assertIn("optimal_action_window", dina)
        self.assertIn("reflective_evening_sanctuary", dina)
        self.assertIn("sattvic_lifestyle_disciplines", dina)
        self.assertGreater(len(dina["sattvic_lifestyle_disciplines"]), 0)

    def test_safe_crystals_enemy_exclusion_and_statutory_notice(self):
        crystals = self.report.get("safe_crystals_and_gemstones")
        self.assertIsNotNone(crystals, "safe_crystals_and_gemstones must be present")
        self.assertIsInstance(crystals["recommended_crystals"], list)
        self.assertGreater(len(crystals["recommended_crystals"]), 0)
        
        # Statutory notice check (Drugs and Magic Remedies Act 1954)
        notice = crystals.get("statutory_compliance_notice", "")
        self.assertIn("Drugs & Magic Remedies Act 1954", notice)
        self.assertIn("traditional cultural", notice)

        # Test conflicting pair: Driver 1 (Sun) and Conductor 8 (Saturn)
        conflict_report = generate_consensus_reading("Arun Sharma", 10, 8, 1988)
        conf_crystals = conflict_report.get("safe_crystals_and_gemstones")
        # In conflict, neutral crystals must be chosen to prevent energetic aggravation
        self.assertIn("Clear Sphatik Quartz", conf_crystals["recommended_crystals"])
        self.assertGreater(len(conf_crystals["excluded_friction_crystals"]), 0)

    def test_sacred_yantras_and_vastu(self):
        yantra_data = self.report.get("sacred_yantras_and_vastu")
        self.assertIsNotNone(yantra_data, "sacred_yantras_and_vastu must be present")
        primary_yantra = yantra_data.get("primary_yantra")
        self.assertIsNotNone(primary_yantra)
        self.assertIn("geometry", primary_yantra)
        self.assertIn("optimal_direction", primary_yantra)
        self.assertIn("beej_mantra", primary_yantra)

    def test_layman_synthesis_and_past_validation(self):
        layman = self.report.get("layman_synthesis")
        self.assertIsNotNone(layman, "layman_synthesis must be present")
        self.assertIn("consultant_summary", layman)
        self.assertIn("where_traditions_agree", layman)
        self.assertIn("where_traditions_differ", layman)

        past_val = self.report.get("past_pattern_validation")
        self.assertIsNotNone(past_val, "past_pattern_validation must be present")
        self.assertIn("milestone_period", past_val)
        self.assertIn("validation_question", past_val)
        self.assertIn("yes_match", past_val["feedback_options"])
        self.assertIn("no_match", past_val["feedback_options"])

    def test_quarantined_offline_resonance_ledger(self):
        res = charm_resonance.record_resonance(
            trace_id="NV-TEST-CONSENSUS-001",
            user_id="test_seeker_99",
            rating="yes_match",
            topic="career",
            driver=6,
            conductor=2,
            feedback_text="Past timeline question matched lived transition in 2024 perfectly.",
            feedback_axis="factual_fit"
        )
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["rating_recorded"], "yes_match")
        self.assertEqual(res["feedback_axis"], "factual_fit")
        self.assertIn("Quarantined Offline Evaluation Ledger", res["message"])


if __name__ == "__main__":
    unittest.main()
