#!/usr/bin/env python3
"""
UNIT TESTS: 2027 Year Ahead Planner Engine & Panchang
Tests deterministic calculations for Person A (Arun Sharma) & Person B (Anil Kumar).
Verifies Results-Only output integrity, Pinnacles, Month Ratings, and Panchang sync.
"""

import os
import json
import unittest
from app.engine.planner_2027_engine import (
    calculate_planner_2027,
    calculate_pinnacles,
    PERSONAL_MONTH_RATINGS,
    CRYSTAL_SUGGESTIONS
)

class TestPlanner2027Engine(unittest.TestCase):

    def test_person_a_arun_sharma(self):
        """
        Person A:
        Name: ARUN SHARMA
        DOB: 1981-11-28 (28-11-1981)
        Target: 2027
        """
        res = calculate_planner_2027("ARUN SHARMA", "1981-11-28")
        
        # Numbers verification
        self.assertEqual(res["numbers"]["mulank"], 1)
        self.assertEqual(res["numbers"]["bhagyank"], 4)
        self.assertEqual(res["numbers"]["personal_year_2027"], 5)
        self.assertEqual(res["numbers"]["driver_conductor_relation"], "Neutral")

        # Pinnacles specification test:
        # P1=3, P2=2, P3=5, P4=3; P1 ends at 32, P2 at 41, P3 at 50
        pinnacles = res["pinnacles"]["pinnacles"]
        self.assertEqual(pinnacles[0]["number"], 3)
        self.assertEqual(pinnacles[0]["age_span"], "Birth to age 32")
        self.assertEqual(pinnacles[1]["number"], 2)
        self.assertEqual(pinnacles[1]["age_span"], "Age 32 to 41")
        self.assertEqual(pinnacles[2]["number"], 5)
        self.assertEqual(pinnacles[2]["age_span"], "Age 41 to 50")
        self.assertEqual(pinnacles[3]["number"], 3)
        self.assertEqual(pinnacles[3]["age_span"], "Age 50 onwards")

        # Age in 2027 is 46 -> Current is P3, Next is P4
        self.assertEqual(res["pinnacles"]["current_pinnacle"], "P3")
        self.assertEqual(res["pinnacles"]["next_pinnacle"], "P4")

        # Crystal for Mulank 1
        self.assertEqual(res["crystal_suggestion"]["crystal"], "Sunstone or Carnelian")

        # 12 Months Ratings check (PY 5: Jan=6 -> Favourable, Feb=7 -> Neutral, ..., Apr=9 -> Asks for care)
        months = res["months"]
        self.assertEqual(len(months), 12)
        self.assertEqual(months[0]["personal_month_number"], 6)
        self.assertEqual(months[0]["rating"], "Favourable")
        self.assertEqual(months[1]["personal_month_number"], 7)
        self.assertEqual(months[1]["rating"], "Neutral")
        self.assertEqual(months[3]["personal_month_number"], 9)
        self.assertEqual(months[3]["rating"], "Asks for care")
        self.assertEqual(months[4]["personal_month_number"], 1)
        self.assertEqual(months[4]["rating"], "Favourable")

        # 365 days calendar
        self.assertEqual(len(res["calendar_365"]), 365)

    def test_person_b_anil_kumar(self):
        """
        Person B:
        Name: ANIL KUMAR
        DOB: 1975-05-01 (01-05-1975)
        Target: 2027
        """
        res = calculate_planner_2027("ANIL KUMAR", "1975-05-01")

        self.assertEqual(res["numbers"]["mulank"], 1)
        self.assertEqual(res["numbers"]["bhagyank"], 1)
        self.assertEqual(res["numbers"]["personal_year_2027"], 8)
        self.assertEqual(res["numbers"]["driver_conductor_relation"], "Friendly")

        # Pinnacles for 01-05-1975:
        # Life path = 1 -> P1 ends at 36-1 = 35.
        # P1 = 5 + 1 = 6
        # P2 = 1 + 4 = 5 (ends at 44)
        # P3 = 6 + 5 = 11 -> 2 (ends at 53)
        # P4 = 5 + 4 = 9 (53+)
        pinnacles = res["pinnacles"]["pinnacles"]
        self.assertEqual(pinnacles[0]["number"], 6)
        self.assertEqual(pinnacles[0]["age_span"], "Birth to age 35")
        self.assertEqual(pinnacles[1]["number"], 5)
        self.assertEqual(pinnacles[1]["age_span"], "Age 35 to 44")
        self.assertEqual(pinnacles[2]["number"], 2)
        self.assertEqual(pinnacles[2]["age_span"], "Age 44 to 53")
        self.assertEqual(pinnacles[3]["number"], 9)
        self.assertEqual(pinnacles[3]["age_span"], "Age 53 onwards")

        # Age in 2027 is 52 -> Current is P3, Next is P4
        self.assertEqual(res["pinnacles"]["current_pinnacle"], "P3")
        self.assertEqual(res["pinnacles"]["next_pinnacle"], "P4")

    def test_results_only_sanitation(self):
        """
        Enforce RESULTS-ONLY rules:
        - No '->' calculation steps
        - No weight numbers or raw mathematical reduction traces
        - No F+/F/N/E/E+ internal labels
        """
        res = calculate_planner_2027("ARUN SHARMA", "1981-11-28")
        dump = json.dumps(res)

        self.assertNotIn("->", dump)
        self.assertNotIn("F+", dump)
        self.assertNotIn("E+", dump)
        self.assertNotIn("weight", dump)
        self.assertNotIn("formula", dump)
        self.assertNotIn("reduction", dump)

    def test_panchang_static_data_exists(self):
        """Verify data/panchang_2027_delhi.json exists and has 365 days."""
        self.assertTrue(os.path.exists("data/panchang_2027_delhi.json"))
        with open("data/panchang_2027_delhi.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(len(data["days"]), 365)
        self.assertEqual(len(data["full_moons_2027"]), 12)
        self.assertEqual(len(data["new_moons_2027"]), 13)

if __name__ == "__main__":
    unittest.main()
