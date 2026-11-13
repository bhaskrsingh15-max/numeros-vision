"""
TEST SUITE FOR CHEIRO COMPOUND NUMBERS 1-100 & RAG ARCHITECTURE
Verifies:
1. Canonical Cheiro 10-52 archetypes match Cheiro's Book of Numbers
2. Dual-Layer decoding: GR-001 (input compound) & GR-002 (output root)
3. Distinction between same-root numbers (e.g., 19 Prince of Heaven vs 28 Promise and Loss)
4. Fallback for 53-100 (root only, no hallucinated compound names)
5. Anti-hallucination guardrail RAG-002 (no fake stats, [INSERT REAL FIGURE])
6. Chaldean name balancing with compound preservation
"""

import unittest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.engine.cheiro_engine import (
    analyze_number,
    analyze_birth_day_cheiro,
    analyze_name_cheiro,
    analyze_dob_conductor_cheiro,
    verify_evidence_guardrails,
    CHEIRO_DATASET
)

class TestCheiroEngine(unittest.TestCase):

    def test_database_completeness_1_to_100(self):
        """Verify all 100 numbers are deterministically present."""
        self.assertEqual(len(CHEIRO_DATASET), 100)
        for i in range(1, 101):
            self.assertIn(i, CHEIRO_DATASET)
            entry = CHEIRO_DATASET[i]
            self.assertEqual(entry["input_number"], i)
            self.assertIn(entry["output_number"], list(range(1, 10)))

    def test_single_numbers_1_to_9(self):
        """Verify single root digits 1 to 9 match pure planetary rulers."""
        expected_planets = {
            1: "Sun", 2: "Moon", 3: "Jupiter", 4: "Rahu/Uranian tradition",
            5: "Mercury", 6: "Venus", 7: "Ketu/Neptune tradition", 8: "Saturn", 9: "Mars"
        }
        for n, planet in expected_planets.items():
            entry = analyze_number(n)
            self.assertEqual(entry["input_type"], "Single")
            self.assertEqual(entry["output_planet_tradition"], planet)
            self.assertEqual(entry["output_number"], n)

    def test_canonical_cheiro_archetypes(self):
        """Verify key canonical Cheiro compound archetypes 10 to 52."""
        cases = {
            10: ("Wheel of Fortune", 1),
            11: ("Clenched Hand / Lion Muzzled", 2),
            12: ("Sacrifice / Victim", 3),
            13: ("Upheaval and Change", 4),
            14: ("Movement and Risk", 5),
            15: ("Magician", 6),
            16: ("Shattered Citadel", 7),
            17: ("Star of the Magi", 8),
            18: ("Rayed Moon", 9),
            19: ("Prince of Heaven / Sun", 1),
            22: ("Good Man Blinded", 4),
            23: ("Royal Star of the Lion", 5),
            24: ("Gain Through Love", 6),
            25: ("Strength Through Trial", 7),
            26: ("Grave Warning", 8),
            27: ("The Sceptre", 9),
            28: ("Promise and Loss", 1),
            29: ("Uncertainty / Deception", 2),
            32: ("Command / Combination", 5),
            37: ("Fortunate Friendships", 1),
            43: ("Revolution / Upheaval", 7),
            51: ("Warrior", 6),
        }
        for num, (expected_arch, expected_root) in cases.items():
            entry = analyze_number(num)
            self.assertEqual(entry["input_compound_archetype"], expected_arch, f"Failed archetype for {num}")
            self.assertEqual(entry["output_number"], expected_root, f"Failed root for {num}")

    def test_gr001_and_rag001_dual_layer_differentiation(self):
        """
        Verify GR-001 & RAG-001: 19 and 28 both reduce to root 1 (Sun),
        but their compound input journeys are completely different!
        """
        c19 = analyze_number(19)
        c28 = analyze_number(28)
        
        # Output root is identical
        self.assertEqual(c19["output_number"], 1)
        self.assertEqual(c28["output_number"], 1)
        self.assertEqual(c19["output_planet_tradition"], "Sun")
        self.assertEqual(c28["output_planet_tradition"], "Sun")
        
        # Compound input archetypes MUST be completely distinct
        self.assertEqual(c19["input_compound_archetype"], "Prince of Heaven / Sun")
        self.assertEqual(c28["input_compound_archetype"], "Promise and Loss")
        self.assertIn("success", c19["input_characteristics"].lower())
        self.assertIn("reversals", c28["input_characteristics"].lower())

    def test_extended_numbers_53_to_100_no_hallucination(self):
        """
        Verify numbers 53 to 100 flag that there is no canonical Cheiro compound meaning,
        reducing strictly to their root digit without inventing fake archetypes.
        """
        for n in [53, 54, 75, 88, 99, 100]:
            entry = analyze_number(n)
            self.assertEqual(entry["input_compound_archetype"], "No canonical Classical Chaldean compound meaning in 10–52")
            self.assertEqual(entry["rag_source_layer"], "Root only / extended-school flag")
            self.assertTrue(entry["reduction_path"].startswith(f"{n} →"))

    def test_chaldean_name_balancing_with_compound_preservation(self):
        """Verify Chaldean name computation preserves compound total before reduction."""
        # e.g., 'Vikram'
        # V=6, I=1, K=2, R=2, A=1, M=4 -> 6+1+2+2+1+4 = 16 (Shattered Citadel -> 7)
        res = analyze_name_cheiro("Vikram", driver=1)
        self.assertEqual(res["compound_sum"], 16)
        self.assertEqual(res["compound_archetype"], "Shattered Citadel")
        self.assertEqual(res["name_root"], 7)
        self.assertIn("Warning: Name compound 16", res["balancing_evaluation"])

    def test_anti_hallucination_guardrail_rag002(self):
        """Verify RAG-002 guardrail strips fabricated statistics."""
        fake_stat_text = "This method has a clinical success rate of 99% and is scientifically proven to be 95% effective."
        cleaned = verify_evidence_guardrails(fake_stat_text)
        self.assertNotIn("99%", cleaned)
        self.assertNotIn("95%", cleaned)
        self.assertIn("[INSERT REAL FIGURE]", cleaned)

if __name__ == "__main__":
    unittest.main()
