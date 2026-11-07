"""
Unit & Golden Test Suite for 2027 Year Ahead Planner Engine
Numeros Vision · Authoritative Master Verification
"""

import unittest
import csv
import json
import datetime
from app.engine.planner_2027_engine import (
    calculate_planner_2027,
    calculate_pinnacles,
    person,
    year,
    tiers,
    classify_tier,
    get_number_compatibility_lists,
    lookup_relation,
    red
)

class TestPlanner2027GoldenSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("tests/golden_sheets.json", "r", encoding="utf-8") as f:
            cls.golden_sheets = json.load(f)

        cls.golden_A = []
        with open("tests/golden_A_365.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cls.golden_A.append({
                    "date": row["date"],
                    "weekday": row["weekday"],
                    "score": int(row["score"]),
                    "tier": row["tier"]
                })

        cls.golden_B = []
        with open("tests/golden_B_365.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cls.golden_B.append({
                    "date": row["date"],
                    "weekday": row["weekday"],
                    "score": int(row["score"]),
                    "tier": row["tier"]
                })

    def test_person_a_golden_number_sheet(self):
        """Verify Arun Sharma's full profile against golden_sheets.json (strict equality)."""
        sheet = self.golden_sheets["A"]
        dob_str = f"{sheet['dob'][2]}-{sheet['dob'][1]:02d}-{sheet['dob'][0]:02d}"
        res = calculate_planner_2027(sheet["name"], dob_str)

        subj = res["subject"]
        self.assertEqual(subj["driver_mulank"], sheet["mulank"])
        self.assertEqual(subj["conductor_bhagyank"], sheet["bhagyank"])
        self.assertEqual(subj["driver_conductor_relation"], sheet["relation"])
        self.assertEqual(subj["personal_year_2027"], sheet["personal_year_2027"])
        self.assertEqual(subj["driver_lists"], sheet["driver_lists"])
        self.assertEqual(subj["conductor_lists"], sheet["conductor_lists"])
        self.assertEqual(subj["lo_shu_present"], sheet["lo_shu_present"])
        self.assertEqual(subj["name_data"]["name_numbers"], sheet["name_numbers"])

        pin = res["pinnacles_data"]
        self.assertEqual(pin["values"]["P1"], sheet["pinnacles"]["P1"])
        self.assertEqual(pin["values"]["P2"], sheet["pinnacles"]["P2"])
        self.assertEqual(pin["values"]["P3"], sheet["pinnacles"]["P3"])
        self.assertEqual(pin["values"]["P4"], sheet["pinnacles"]["P4"])
        self.assertEqual(pin["spans"], sheet["pinnacles"]["spans"])

        self.assertEqual(res["cutoffs"], sheet["cutoffs"])
        self.assertEqual(res["tier_counts"], sheet["tier_counts"])
        self.assertEqual(res["days_at_100"], sheet["days_at_100"])
        self.assertEqual(res["min"], sheet["min"])
        self.assertEqual(res["max"], sheet["max"])

        # Specific dates at 100 assertion by name (Arun Sharma)
        days_at_100_names = [d["date"] for d in res["full_calendar_365"] if d["alignment_score"] == 100]
        self.assertEqual(days_at_100_names, ["2027-04-04", "2027-05-21", "2027-05-30"])

        # Lo Shu digit counts assertions
        self.assertEqual(res["lo_shu_counts"][1], 5)
        self.assertEqual(res["lo_shu_counts"][2], 1)
        self.assertEqual(res["lo_shu_counts"][4], 1)
        self.assertEqual(res["lo_shu_counts"][8], 2)
        self.assertEqual(res["lo_shu_counts"][9], 1)
        self.assertEqual(res["dob_digit_counts"][1], 4)

    def test_person_b_golden_number_sheet(self):
        """Verify Anil Kumar's full profile against golden_sheets.json (strict equality)."""
        sheet = self.golden_sheets["B"]
        dob_str = f"{sheet['dob'][2]}-{sheet['dob'][1]:02d}-{sheet['dob'][0]:02d}"
        res = calculate_planner_2027(sheet["name"], dob_str)

        subj = res["subject"]
        self.assertEqual(subj["driver_mulank"], sheet["mulank"])
        self.assertEqual(subj["conductor_bhagyank"], sheet["bhagyank"])
        self.assertEqual(subj["driver_conductor_relation"], sheet["relation"])
        self.assertEqual(subj["personal_year_2027"], sheet["personal_year_2027"])
        self.assertEqual(subj["driver_lists"], sheet["driver_lists"])
        self.assertEqual(subj["conductor_lists"], sheet["conductor_lists"])
        self.assertEqual(subj["lo_shu_present"], sheet["lo_shu_present"])
        self.assertEqual(subj["name_data"]["name_numbers"], sheet["name_numbers"])

        pin = res["pinnacles_data"]
        self.assertEqual(pin["values"]["P1"], sheet["pinnacles"]["P1"])
        self.assertEqual(pin["values"]["P2"], sheet["pinnacles"]["P2"])
        self.assertEqual(pin["values"]["P3"], sheet["pinnacles"]["P3"])
        self.assertEqual(pin["values"]["P4"], sheet["pinnacles"]["P4"])
        self.assertEqual(pin["spans"], sheet["pinnacles"]["spans"])

        self.assertEqual(res["cutoffs"], sheet["cutoffs"])
        self.assertEqual(res["tier_counts"], sheet["tier_counts"])
        self.assertEqual(res["days_at_100"], sheet["days_at_100"])
        self.assertEqual(res["min"], sheet["min"])
        self.assertEqual(res["max"], sheet["max"])

        # Specific dates at 100 assertion by name (Anil Kumar)
        days_at_100_names = [d["date"] for d in res["full_calendar_365"] if d["alignment_score"] == 100]
        self.assertEqual(days_at_100_names, [
            "2027-01-10", "2027-02-28", "2027-03-14", "2027-07-28",
            "2027-10-10", "2027-11-28", "2027-12-05"
        ])

        # Lo Shu digit counts assertions
        self.assertEqual(res["lo_shu_counts"][1], 4)
        self.assertEqual(res["lo_shu_counts"][5], 2)
        self.assertEqual(res["lo_shu_counts"][7], 1)
        self.assertEqual(res["lo_shu_counts"][9], 1)
        self.assertEqual(res["dob_digit_counts"][1], 2)

    def test_person_a_365_days_exact_equality(self):
        """Every single day of 365 days for Person A must match golden_A_365.csv in score AND tier."""
        sheet = self.golden_sheets["A"]
        dob_str = f"{sheet['dob'][2]}-{sheet['dob'][1]:02d}-{sheet['dob'][0]:02d}"
        res = calculate_planner_2027(sheet["name"], dob_str)
        cal = res["full_calendar_365"]

        self.assertEqual(len(cal), 365)
        self.assertEqual(len(self.golden_A), 365)

        mismatches = []
        for i in range(365):
            actual = cal[i]
            expected = self.golden_A[i]
            if actual["date"] != expected["date"]:
                mismatches.append(f"Date mismatch at index {i}: actual={actual['date']}, expected={expected['date']}")
            if actual["weekday"] != expected["weekday"]:
                mismatches.append(f"Weekday mismatch at {actual['date']}: actual={actual['weekday']}, expected={expected['weekday']}")
            if actual["alignment_score"] != expected["score"]:
                mismatches.append(f"Score mismatch at {actual['date']}: actual={actual['alignment_score']}, expected={expected['score']}")
            if actual["tier"] != expected["tier"]:
                mismatches.append(f"Tier mismatch at {actual['date']}: actual={actual['tier']}, expected={expected['tier']}")

        self.assertEqual(len(mismatches), 0, f"Person A 365-day mismatches ({len(mismatches)}):\n" + "\n".join(mismatches[:10]))

    def test_person_b_365_days_exact_equality(self):
        """Every single day of 365 days for Person B must match golden_B_365.csv in score AND tier."""
        sheet = self.golden_sheets["B"]
        dob_str = f"{sheet['dob'][2]}-{sheet['dob'][1]:02d}-{sheet['dob'][0]:02d}"
        res = calculate_planner_2027(sheet["name"], dob_str)
        cal = res["full_calendar_365"]

        self.assertEqual(len(cal), 365)
        self.assertEqual(len(self.golden_B), 365)

        mismatches = []
        for i in range(365):
            actual = cal[i]
            expected = self.golden_B[i]
            if actual["date"] != expected["date"]:
                mismatches.append(f"Date mismatch at index {i}: actual={actual['date']}, expected={expected['date']}")
            if actual["weekday"] != expected["weekday"]:
                mismatches.append(f"Weekday mismatch at {actual['date']}: actual={actual['weekday']}, expected={expected['weekday']}")
            if actual["alignment_score"] != expected["score"]:
                mismatches.append(f"Score mismatch at {actual['date']}: actual={actual['alignment_score']}, expected={expected['score']}")
            if actual["tier"] != expected["tier"]:
                mismatches.append(f"Tier mismatch at {actual['date']}: actual={actual['tier']}, expected={expected['tier']}")

        self.assertEqual(len(mismatches), 0, f"Person B 365-day mismatches ({len(mismatches)}):\n" + "\n".join(mismatches[:10]))

    def test_sample_person_anita_sharma_corrected(self):
        """Extra unit test: Anita Sharma (1988-10-14)."""
        dob = datetime.date(1988, 10, 14)
        pin = calculate_pinnacles(dob, bhagyank=5, target_year=2027)
        self.assertEqual(pin["values"]["P1"], 6)
        self.assertEqual(pin["values"]["P2"], 4)
        self.assertEqual(pin["values"]["P3"], 1)
        self.assertEqual(pin["values"]["P4"], 9)
        self.assertEqual(pin["current_pinnacle"], "P2")  # Age 39 is 2nd pinnacle (31 to 40)

        res = calculate_planner_2027("ANITA SHARMA", "1988-10-14")
        self.assertEqual(res["subject"]["driver_mulank"], 5)
        self.assertEqual(res["subject"]["conductor_bhagyank"], 5)
        self.assertEqual(res["subject"]["personal_year_2027"], 8)

    def test_sample_person_vikram_patel_corrected(self):
        """Extra unit test: Vikram Patel (1975-06-29)."""
        dob = datetime.date(1975, 6, 29)
        pin = calculate_pinnacles(dob, bhagyank=3, target_year=2027)
        self.assertEqual(pin["values"]["P1"], 8)
        self.assertEqual(pin["values"]["P2"], 6)
        self.assertEqual(pin["values"]["P3"], 5)
        self.assertEqual(pin["values"]["P4"], 1)
        self.assertEqual(pin["current_pinnacle"], "P4")  # Age 52 is 4th pinnacle (51 onwards)

        res = calculate_planner_2027("VIKRAM PATEL", "1975-06-29")
        self.assertEqual(res["subject"]["driver_mulank"], 2)
        self.assertEqual(res["subject"]["conductor_bhagyank"], 3)
        self.assertEqual(res["subject"]["personal_year_2027"], 1)

    def test_master_vibration_11_flag(self):
        """Verify June for Personal Year 5 flags Master Vibration 11/2."""
        res = calculate_planner_2027("ARUN SHARMA", "1981-11-28")
        self.assertEqual(res["subject"]["personal_year_2027"], 5)
        june = [m for m in res["months"] if m["month_number"] == 6][0]
        self.assertTrue(june["is_master_11"])
        self.assertEqual(june["personal_month_display"], "2 (Master Vibration 11/2)")

    def test_input_validation(self):
        """Test boundary assertions on full name and DOB."""
        with self.assertRaises(ValueError):
            calculate_planner_2027("", "1981-11-28")
        with self.assertRaises(ValueError):
            calculate_planner_2027("A", "1981-11-28")
        with self.assertRaises(ValueError):
            calculate_planner_2027("Arun 123", "1981-11-28")
        with self.assertRaises(ValueError):
            calculate_planner_2027("Arun Sharma", "1899-12-31")
        with self.assertRaises(ValueError):
            calculate_planner_2027("Arun Sharma", "2030-01-01")

if __name__ == '__main__':
    unittest.main()
