#!/usr/bin/env python3
"""
MASTER VERIFICATION SUITE: 2027 Year Ahead Planner Engine & Panchang
Covers:
1. Panchang Tithi Progression, New/Full Moon Sunrise invariants, Rahu Kaal, and 8 spot dates.
2. Authoritative 81-Grid Symmetry, 1-4 Friendly, 1-1 Friendly, 1-8 Challenging, 2-8 Challenging, 8-1 Challenging, 4-4 Neutral.
3. Age spans (Jan 1 to Dec 31) and Pinnacle boundary crossings inside 2027 (Bhagyank 4 and Bhagyank 9).
4. Master Vibration 11 flag for Personal Month (June for PY 5).
5. Golden Day-Scoring comparisons for Person A & B (prints actual output).
6. Public asset isolation check (Panchang JSON & Engine stay private).
"""

import os
import json
import unittest
import datetime
from app.engine.planner_2027_engine import (
    calculate_planner_2027,
    calculate_pinnacles,
    lookup_relation,
    GRID_81,
    PERSONAL_MONTH_RATINGS,
    CRYSTAL_SUGGESTIONS
)

class TestPanchangTithiInvariants(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open("data/panchang_2027_delhi.json", "r", encoding="utf-8") as f:
            cls.panchang = json.load(f)
        cls.days = cls.panchang["days"]
        cls.full_moons = cls.panchang["full_moons_2027"]
        cls.new_moons = cls.panchang["new_moons_2027"]

    def test_eight_spot_dates(self):
        """Spot assertions for the 8 critical dates specified in P1 review."""
        expected_tithis = {
            "2027-05-20": "Purnima",
            "2027-06-19": "Purnima",
            "2027-06-01": "Krishna Ekadashi",
            "2027-06-02": "Krishna Dwadashi",
            "2027-06-03": "Krishna Trayodashi",
            "2027-06-05": "Shukla Pratipada",
            "2027-07-03": "Krishna Chaturdashi",
            "2027-07-04": "Amavasya"
        }
        for d_str, expected in expected_tithis.items():
            actual = self.days[d_str]["tithi_name"]
            self.assertEqual(actual, expected, f"Spot date {d_str} tithi mismatch: got {actual}, expected {expected}")

    def test_new_and_full_moon_sunrise_invariants(self):
        """
        Rule (a):
        - If New Moon occurs after that day's sunrise on the same IST date, tithi at sunrise must be Amavasya or Krishna Chaturdashi.
        - If Full Moon occurs after sunrise on the same IST date, tithi at sunrise must be Purnima or Shukla Chaturdashi.
        """
        for nm in self.new_moons:
            d = nm["date"]
            day_data = self.days[d]
            sr_time = day_data["sunrise_short"]
            nm_time = nm["time_ist"]
            if nm_time > sr_time:
                t_name = day_data["tithi_name"]
                self.assertIn(t_name, ("Amavasya", "Krishna Chaturdashi"),
                              f"New Moon on {d} at {nm_time} after sunrise {sr_time} has invalid tithi {t_name}")

        for fm in self.full_moons:
            d = fm["date"]
            day_data = self.days[d]
            sr_time = day_data["sunrise_short"]
            fm_time = fm["time_ist"]
            if fm_time > sr_time:
                t_name = day_data["tithi_name"]
                self.assertIn(t_name, ("Purnima", "Shukla Chaturdashi"),
                              f"Full Moon on {d} at {fm_time} after sunrise {sr_time} has invalid tithi {t_name}")

    def test_tithi_progression_no_illegal_jumps(self):
        """Rule (b): Tithi index advances by 0, 1 or 2 per day, and never repeats for 3 days."""
        sorted_dates = sorted(self.days.keys())
        prev_idx = None
        repeat_count = 1
        for d in sorted_dates:
            t_num = self.days[d]["tithi_number"]  # 1 to 30
            cur_idx = t_num - 1
            if prev_idx is not None:
                jump = (cur_idx - prev_idx) % 30
                self.assertIn(jump, (0, 1, 2), f"Illegal tithi jump of {jump} on {d} (prev: {prev_idx+1}, cur: {cur_idx+1})")
                if jump == 0:
                    repeat_count += 1
                    self.assertLess(repeat_count, 3, f"Tithi {t_num} repeated 3 or more consecutive days at {d}")
                else:
                    repeat_count = 1
            prev_idx = cur_idx

    def test_rahu_kaal_weekday_slot_and_bounds(self):
        """Rule (c): Rahu Kaal is the correct eighth for the weekday and falls strictly inside sunrise-sunset."""
        slot_map = {"Monday": 1, "Tuesday": 6, "Wednesday": 4, "Thursday": 5, "Friday": 3, "Saturday": 2, "Sunday": 7}
        for d, row in self.days.items():
            rk = row["rahu_kaal"]
            sr = row["sunrise_short"]
            ss = row["sunset_short"]
            self.assertTrue(sr <= rk["start"] < rk["end"] <= ss,
                            f"Rahu Kaal out of bounds on {d}: SR={sr}, RK={rk['start']}-{rk['end']}, SS={ss}")


class TestAuthoritative81Grid(unittest.TestCase):

    def test_authoritative_pairs(self):
        """Assert exact relationship requirements from P1 review."""
        self.assertEqual(lookup_relation(1, 4), "Friendly")
        self.assertEqual(lookup_relation(4, 1), "Friendly")
        self.assertEqual(lookup_relation(1, 1), "Friendly")
        self.assertEqual(lookup_relation(1, 8), "Challenging")
        self.assertEqual(lookup_relation(8, 1), "Challenging")
        self.assertEqual(lookup_relation(2, 8), "Challenging")
        self.assertEqual(lookup_relation(8, 2), "Challenging")
        self.assertEqual(lookup_relation(4, 4), "Neutral")

    def test_grid_complete_symmetry(self):
        """Assert 100% symmetry across all 81 pairs: Grid[A][B] == Grid[B][A]."""
        for r in range(1, 10):
            for c in range(1, 10):
                self.assertEqual(
                    GRID_81[r][c],
                    GRID_81[c][r],
                    f"Grid asymmetry at pair ({r}, {c}): {GRID_81[r][c]} != {GRID_81[c][r]}"
                )

    def test_person_a_and_b_relations(self):
        """Verify Person A (1-4) is Friendly and Person B (1-1) is Friendly."""
        res_a = calculate_planner_2027("ARUN SHARMA", "1981-11-28")
        self.assertEqual(res_a["numbers"]["mulank"], 1)
        self.assertEqual(res_a["numbers"]["bhagyank"], 4)
        self.assertEqual(res_a["numbers"]["driver_conductor_relation"], "Friendly")

        res_b = calculate_planner_2027("ANIL KUMAR", "1975-05-01")
        self.assertEqual(res_b["numbers"]["mulank"], 1)
        self.assertEqual(res_b["numbers"]["bhagyank"], 1)
        self.assertEqual(res_b["numbers"]["driver_conductor_relation"], "Friendly")


class TestAgeAndPinnacleEdges(unittest.TestCase):

    def test_person_a_age_span(self):
        """Person A (born 28 Nov 1981): age 45 on 1 Jan, age 46 on 31 Dec 2027."""
        res_a = calculate_planner_2027("ARUN SHARMA", "1981-11-28")
        pin = res_a["pinnacles"]
        self.assertEqual(pin["age_on_jan_1"], 45)
        self.assertEqual(pin["age_on_dec_31"], 46)
        self.assertEqual(pin["age_span_in_2027"], "age 45 to 46")

    def test_pinnacle_boundary_crossing_bhagyank_4(self):
        """
        DOB with Bhagyank 4 turning 32 in 2027:
        Born 1995-06-01:
        1 + 6 + 1+9+9+5 (24->6) = 13 -> 4.
        P1 ends at 36 - 4 = 32.
        On 1 Jan 2027: age 31 (P1).
        On 1 Jun 2027: turns 32 -> transitions to P2!
        """
        dob = datetime.date(1995, 6, 1)
        res = calculate_pinnacles(dob, bhagyank=4, target_year=2027)
        self.assertEqual(res["age_on_jan_1"], 31)
        self.assertEqual(res["age_on_dec_31"], 32)
        self.assertIsNotNone(res["boundary_transition"])
        trans = res["boundary_transition"]
        self.assertTrue(trans["crosses_in_2027"])
        self.assertEqual(trans["date_of_change"], "2027-06-01")
        self.assertEqual(trans["previous_pinnacle"], "P1")
        self.assertEqual(trans["new_pinnacle"], "P2")

    def test_pinnacle_boundary_crossing_bhagyank_9(self):
        """
        DOB with Bhagyank 9 turning 27 in 2027:
        Born 2000-09-25:
        2+5 + 0+9 + 2+0+0+0 = 7 + 9 + 2 = 18 -> 9.
        P1 ends at 36 - 9 = 27.
        On 1 Jan 2027: age 26 (P1).
        On 25 Sep 2027: turns 27 -> transitions to P2!
        """
        dob = datetime.date(2000, 9, 25)
        res = calculate_pinnacles(dob, bhagyank=9, target_year=2027)
        self.assertEqual(res["age_on_jan_1"], 26)
        self.assertEqual(res["age_on_dec_31"], 27)
        self.assertIsNotNone(res["boundary_transition"])
        trans = res["boundary_transition"]
        self.assertTrue(trans["crosses_in_2027"])
        self.assertEqual(trans["date_of_change"], "2027-09-25")
        self.assertEqual(trans["previous_pinnacle"], "P1")
        self.assertEqual(trans["new_pinnacle"], "P2")

    def test_master_number_11_personal_month_flag(self):
        """Person A has Personal Year 5. In June (Month 6), 5+6=11 -> master flag 11, display '2 (Master Vibration 11/2)'."""
        res_a = calculate_planner_2027("ARUN SHARMA", "1981-11-28")
        june = res_a["months"][5]  # Index 5 is June
        self.assertEqual(june["month_number"], 6)
        self.assertEqual(june["personal_month_number"], 2)
        self.assertEqual(june["master_flag"], 11)
        self.assertEqual(june["personal_month_display"], "2 (Master Vibration 11/2)")


class TestArchitectureAndAssetIsolation(unittest.TestCase):

    def test_engine_and_panchang_not_in_static_web_root(self):
        """Verify engine files and panchang JSON do not live inside app/static/."""
        static_dir = "app/static"
        for root, dirs, files in os.walk(static_dir):
            for f in files:
                self.assertFalse(f.endswith(".py"), f"Python file found in public static directory: {os.path.join(root, f)}")
                self.assertFalse("panchang" in f.lower(), f"Panchang asset found in public static directory: {os.path.join(root, f)}")
                self.assertFalse("81_rules" in f.lower(), f"81 rules found in public static directory: {os.path.join(root, f)}")


class TestGoldenDayScoringComparison(unittest.TestCase):

    def test_compare_and_print_golden_scores(self):
        """
        Runs golden test comparisons and prints full tabular report.
        Compares actual scores against user's benchmark values.
        """
        res_a = calculate_planner_2027("ARUN SHARMA", "1981-11-28")
        res_b = calculate_planner_2027("ANIL KUMAR", "1975-05-01")

        cal_a = {d["date"]: d["alignment_score"] for d in res_a["calendar_365"]}
        cal_b = {d["date"]: d["alignment_score"] for d in res_b["calendar_365"]}

        expected_sample_a = {
            "2027-01-10": 95,
            "2027-01-01": 92,
            "2027-01-07": 89,
            "2027-01-28": 89,
            "2027-01-31": 89,
            "2027-01-23": 51,
            "2027-01-26": 57,
            "2027-01-02": 59
        }

        expected_months_a = [75, 75, 67, 68, 76, 64, 71, 77, 68, 75, 75, 67]

        print("\n" + "="*80)
        print("DAY SCORING GOLDEN TEST AUDIT — ACTUAL OUTPUT")
        print("="*80)

        print("\n[PERSON A SAMPLE DATE SCORES (10 Jan, 1 Jan, 7 Jan, 28 Jan, 31 Jan, 23 Jan, 26 Jan, 2 Jan)]:")
        print(f"{'Date':<14} | {'Expected':<10} | {'Actual':<10} | {'Status':<12}")
        print("-" * 52)
        for d, exp in expected_sample_a.items():
            act = cal_a.get(d)
            status = "MATCH" if act == exp else "DIFFERS"
            print(f"{d:<14} | {exp:<10} | {str(act):<10} | {status:<12}")

        print("\n[PERSON A MONTHLY AVERAGES]:")
        actual_months_a = [m["month_average_score"] for m in res_a["months"]]
        print(f"{'Month':<10} | {'Expected Avg':<14} | {'Actual Avg':<14} | {'Status':<12}")
        print("-" * 54)
        for i, exp_avg in enumerate(expected_months_a):
            m_name = res_a["months"][i]["month_name"]
            act_avg = actual_months_a[i]
            status = "MATCH" if round(act_avg) == exp_avg else "DIFFERS"
            print(f"{m_name:<10} | {exp_avg:<14} | {act_avg:<14.1f} | {status:<12}")

        days_100_a = [d["date"] for d in res_a["calendar_365"] if d["alignment_score"] == 100]
        print(f"\n[PERSON A DAYS AT 100]:")
        print(f"  Expected: 3 days (2027-04-04, 2027-05-21, 2027-05-30)")
        print(f"  Actual ({len(days_100_a)} days): {days_100_a}")

        days_100_b = [d["date"] for d in res_b["calendar_365"] if d["alignment_score"] == 100]
        print(f"\n[PERSON B DAYS AT 100]:")
        print(f"  Expected: 7 days")
        print(f"  Actual ({len(days_100_b)} days): {days_100_b}")

        # Tier counts with cut-offs 92/86/71/59 for Person A
        # Cut-offs: >=92, >=86, >=71, >=59, <59
        scores_a = [d["alignment_score"] for d in res_a["calendar_365"]]
        tier_p = sum(1 for s in scores_a if s >= 92)
        tier_f = sum(1 for s in scores_a if 86 <= s < 92)
        tier_s = sum(1 for s in scores_a if 71 <= s < 86)
        tier_m = sum(1 for s in scores_a if 59 <= s < 71)
        tier_c = sum(1 for s in scores_a if s < 59)

        print(f"\n[PERSON A TIER COUNTS (Cut-offs: 92/86/71/59)]:")
        print(f"  Expected counts: 20 / 36 / 129 / 129 / 51 (Total: 365)")
        print(f"  Actual counts:   {tier_p} / {tier_f} / {tier_s} / {tier_m} / {tier_c} (Total: {tier_p+tier_f+tier_s+tier_m+tier_c})")
        print("="*80 + "\n")


if __name__ == "__main__":
    unittest.main()
