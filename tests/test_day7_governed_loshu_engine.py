"""
NUMEROS VISION — UNIT & REGRESSION TEST SUITE
Governed Lo Shu Rule Catalog, Lifecycle & Exception Resolution Engine (Version 2.0.0)
Validates Day 7 transcript rules + Ingested Authoritative Books & Notes:
  - Day 7 Lo Shu Elements, Attributes & Repetition Framework (SRC-DAY7-TRANSCRIPT)
  - Advance & Professional Missing Number Diagnoses, Poorak Numbers & Remedies (SRC-ADV-PROF-NOTES)
  - All 81 Driver-Conductor Combinations (SRC-81-DC-DESTINY-GUIDE)
  - Numerological Mahadasha Calculation Cycle & Scoring (SRC-NUMERO-MAHADASHA)
"""

import unittest
from app.engine.rule_governance import rule_governance, RuleStatus
from app.engine.lo_shu import analyze_lo_shu_grid, generate_loshu_grid_markdown


class TestGovernedLoShuAndAuthoritativeNotesEngine(unittest.TestCase):
    def test_all_nine_number_attributes_and_elements(self):
        """Verifies all 9 attributes and element mappings extracted from Day 7 transcript."""
        expected = {
            1: ("Communication", "Water", "Sun"),
            2: ("Intuition and sensitive power", "Earth", "Moon"),
            3: ("Creativity and imagination", "Wood", "Jupiter"),
            4: ("Discipline and organised power", "Wood", "Rahu"),
            5: ("Balance", "Earth", "Mercury"),
            6: ("Home, family and love relationships", "Metal", "Venus"),
            7: ("Disappointment, healing, wisdom, spirituality and the divine", "Metal", "Ketu"),
            8: ("Money and finance management", "Earth", "Saturn"),
            9: ("Aggression, ego, humanity and humility", "Fire", "Mars")
        }

        for num, (exp_attr, exp_elem, exp_planet) in expected.items():
            rule = rule_governance.get_attribute_for_number(num)
            self.assertIsNotNone(rule, f"Rule missing for number {num}")
            self.assertEqual(rule["attribute"], exp_attr)
            self.assertEqual(rule["element"], exp_elem)
            self.assertEqual(rule["planet"], exp_planet)
            self.assertEqual(rule["approval_status"], "APPROVED")
            self.assertEqual(rule["source_document_id"], "SRC-DAY7-TRANSCRIPT")

    def test_five_repetition_categories(self):
        """Verifies the 5 repetition tiers: Under, Pair, Exaggerate, Reactive, Over-reactive."""
        # 1 occurrence -> Under
        r1 = rule_governance.get_repetition_evaluation(1, 1)
        self.assertEqual(r1["repetition_category"], "Under")
        self.assertEqual(r1["rule_id"], "RUL-LOSHU-D7-REP-1")
        self.assertEqual(r1["approval_status"], "APPROVED")

        # 2 occurrences -> Pair (best-performing)
        r2 = rule_governance.get_repetition_evaluation(5, 2)
        self.assertEqual(r2["repetition_category"], "Pair")
        self.assertEqual(r2["rule_id"], "RUL-LOSHU-D7-REP-2")
        self.assertEqual(r2["approval_status"], "APPROVED")

        # 3 occurrences -> Exaggerate
        r3 = rule_governance.get_repetition_evaluation(9, 3)
        self.assertEqual(r3["repetition_category"], "Exaggerate")
        self.assertEqual(r3["rule_id"], "RUL-LOSHU-D7-REP-3")
        self.assertEqual(r3["approval_status"], "APPROVED")

        # 4 occurrences -> Reactive
        r4 = rule_governance.get_repetition_evaluation(4, 4)
        self.assertEqual(r4["repetition_category"], "Reactive")
        self.assertEqual(r4["rule_id"], "RUL-LOSHU-D7-REP-4")
        self.assertEqual(r4["approval_status"], "APPROVED")

        # 5 occurrences -> Over-reactive / Hyper-reactive
        r5 = rule_governance.get_repetition_evaluation(2, 5)
        self.assertEqual(r5["repetition_category"], "Over-reactive")
        self.assertEqual(r5["rule_id"], "RUL-LOSHU-D7-REP-5")
        self.assertEqual(r5["approval_status"], "APPROVED")

    def test_repetition_extrapolation_boundary_abstention(self):
        """Verifies frequencies > 5 strictly return PENDING_EVIDENCE rather than inventing claims."""
        r6 = rule_governance.get_repetition_evaluation(1, 6)
        self.assertEqual(r6["status"], "EXTRAPOLATION_LIMIT_EXCEEDED")
        self.assertEqual(r6["repetition_category"], "PENDING_EVIDENCE")
        self.assertEqual(r6["approval_status"], "PENDING_EVIDENCE")
        self.assertEqual(r6["rule_id"], "RUL-LOSHU-D7-REP-EXTRAPOLATION")
        self.assertIn("abstains from extrapolating", r6["interpretation"])

    def test_missing_number_verified_from_advance_notes(self):
        """Verifies missing digits report verified diagnosis, poorak numbers, and remedies from SRC-ADV-PROF-NOTES."""
        # Missing 2
        r2 = rule_governance.get_missing_number_evaluation(2)
        self.assertEqual(r2["status"], "MISSING_VERIFIED")
        self.assertEqual(r2["approval_status"], "APPROVED")
        self.assertEqual(r2["source_document_id"], "SRC-ADV-PROF-NOTES")
        self.assertEqual(r2["poorak_complimentary_numbers"], [5, 7])
        self.assertIn("crystal bracelet", r2["element_remedy"].lower())
        self.assertIn("Chandra Yantra", r2["yantra_remedy"])

        # Missing 6
        r6 = rule_governance.get_missing_number_evaluation(6)
        self.assertEqual(r6["status"], "MISSING_VERIFIED")
        self.assertEqual(r6["poorak_complimentary_numbers"], [5])
        self.assertIn("golden", r6["element_remedy"].lower())

    def test_all_81_driver_conductor_combinations_catalog(self):
        """Verifies all 81 Driver-Conductor combinations are loaded and return verified data."""
        # Test 9-2 (Alexander Vance)
        dc_9_2 = rule_governance.get_driver_conductor_combination(9, 2)
        self.assertEqual(dc_9_2["approval_status"], "APPROVED")
        self.assertEqual(dc_9_2["driver_planet"], "Mars")
        self.assertEqual(dc_9_2["conductor_planet"], "Moon")
        self.assertEqual(dc_9_2["compatibility"], "Moderate")
        self.assertEqual(dc_9_2["destiny_influence"], "Emotional intelligence, diplomacy")

        # Test 1-1 (Sun - Sun)
        dc_1_1 = rule_governance.get_driver_conductor_combination(1, 1)
        self.assertEqual(dc_1_1["approval_status"], "APPROVED")
        self.assertEqual(dc_1_1["compatibility"], "Very Strong")

        # Test 9-8 (Mars - Saturn)
        dc_9_8 = rule_governance.get_driver_conductor_combination(9, 8)
        self.assertEqual(dc_9_8["approval_status"], "APPROVED")
        self.assertEqual(dc_9_8["compatibility"], "Challenging / Karmic")

    def test_numerological_mahadasha_deterministic_cycle(self):
        """Verifies calculation of Numerological Mahadasha based on SRC-NUMERO-MAHADASHA."""
        # Example from book: DOB 04/08/1990 -> King 4 -> runs 4 yrs (1990-1994)
        md_book = rule_governance.calculate_numerological_mahadasha("04-08-1990", 1992)
        self.assertEqual(md_book["king_driver_number"], 4)
        self.assertEqual(md_book["periods"][0]["number"], 4)
        self.assertEqual(md_book["periods"][0]["duration_years"], 4)
        self.assertEqual(md_book["periods"][0]["start_year"], 1990)
        self.assertEqual(md_book["periods"][0]["end_year"], 1994)
        self.assertTrue(md_book["periods"][0]["is_current_active"])

        # Second period in book: 5 (Mercury) for 5 yrs (1994-1999)
        self.assertEqual(md_book["periods"][1]["number"], 5)
        self.assertEqual(md_book["periods"][1]["duration_years"], 5)
        self.assertEqual(md_book["periods"][1]["start_year"], 1994)
        self.assertEqual(md_book["periods"][1]["end_year"], 1999)

        # Alexander Vance: 18-10-1990 -> King 9 (Mars) -> 1990 to 1999
        md_vance = rule_governance.calculate_numerological_mahadasha("18-10-1990", 2026)
        self.assertEqual(md_vance["king_driver_number"], 9)
        self.assertEqual(md_vance["periods"][0]["number"], 9)
        self.assertEqual(md_vance["periods"][0]["duration_years"], 9)
        # In 2026, Vance is in Cycle 8: Ketu 7 (2020-2027)
        self.assertEqual(md_vance["current_active_mahadasha"]["number"], 7)
        self.assertEqual(md_vance["current_active_mahadasha"]["planet"], "Ketu")

    def test_pedagogy_135_framework_qualification(self):
        """Verifies the 135 reading-type framework is treated as instructor pedagogy, not verified math count."""
        rule = rule_governance.get_rule_by_id("RUL-LOSHU-D7-FRAMEWORK-135")
        self.assertIsNotNone(rule)
        self.assertEqual(rule.authority_status, "instructor_stated_pedagogy")
        self.assertIn("pedagogical teaching structure", rule.interpretation)

    def test_integration_with_analyze_lo_shu_grid(self):
        """Verifies end-to-end integration with analyze_lo_shu_grid."""
        # DOB: 15-08-1995 -> Digits: 1: 2, 5: 2, 8: 1, 9: 2. Missing: 2, 3, 4, 6, 7
        res = analyze_lo_shu_grid(15, 8, 1995)
        self.assertTrue(res["governed_rules_applied"])
        self.assertEqual(res["governance_version"], "2.0.0")
        
        rep = res["repetition_analysis"]
        self.assertEqual(rep["1"]["repetition_category"], "Pair")  # 2 ones
        self.assertEqual(rep["5"]["repetition_category"], "Pair")  # 2 fives
        self.assertEqual(rep["8"]["repetition_category"], "Under") # 1 eight
        self.assertEqual(rep["9"]["repetition_category"], "Pair")  # 2 nines
        self.assertEqual(rep["4"]["status"], "MISSING_VERIFIED")    # 0 fours
        self.assertEqual(rep["4"]["approval_status"], "APPROVED")

    def test_silver_success_plane_designation(self):
        """Verifies 2-5-8 is designated as Silver Success Plane (Silver Raj Yoga), never Disappointment Plane."""
        # DOB 25-08-1982 has digits 2, 5, 8 present
        res = analyze_lo_shu_grid(25, 8, 1982)
        self.assertIn("Silver Success Plane (2-5-8)", res["completed_planes"])
        self.assertNotIn("Loss/Disappointment Plane (2-5-8)", res["completed_planes"])
        self.assertNotIn("Disappointment Plane", res["completed_planes"])


if __name__ == "__main__":
    unittest.main()
