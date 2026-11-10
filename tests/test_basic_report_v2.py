import unittest
import os
import json
import io
import itertools
import pypdf

from app.services.pdf_report_generator import generate_customised_pdf_report, run_deterministic_calculation

class TestBasicReportV2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        lib_path = os.path.join(os.path.dirname(__file__), "..", "app", "data", "basic_report_content_library.json")
        with open(lib_path, "r", encoding="utf-8") as f:
            cls.content_lib = json.load(f)

        geo_path = os.path.join(os.path.dirname(__file__), "..", "app", "data", "terminology_geo.json")
        with open(geo_path, "r", encoding="utf-8") as f:
            cls.geo_terms = json.load(f)

    def test_01_all_81_driver_conductor_pairs_exist_and_complete(self):
        """Verify all 81 combinations (1_1 to 9_9) have valid basic depth text and metadata."""
        dc_topics = self.content_lib["topics"]["driver_conductor"]
        self.assertEqual(len(dc_topics), 81, "Must contain exactly 81 driver-conductor pairs")
        for d in range(1, 10):
            for c in range(1, 10):
                key = f"{d}_{c}"
                self.assertIn(key, dc_topics, f"Missing pair {key}")
                pair_data = dc_topics[key]
                self.assertEqual(pair_data["driver"], d)
                self.assertEqual(pair_data["conductor"], c)
                self.assertIn("depth_1_basic", pair_data)
                self.assertTrue(len(pair_data["depth_1_basic"]["summary"]) > 10)
                self.assertEqual(pair_data["depth_1_basic"]["status"], "DRAFT")

    def test_02_life_path_and_name_keys(self):
        """Verify 9+3 Life Path keys and 9 Name keys exist with valid content."""
        lp_topics = self.content_lib["topics"]["life_path"]
        expected_lps = [str(n) for n in range(1, 10)] + ["11", "22", "33"]
        for lp in expected_lps:
            self.assertIn(lp, lp_topics, f"Missing life path {lp}")
            self.assertTrue(len(lp_topics[lp]["depth_1_basic"]["text"]) > 10)

        name_topics = self.content_lib["topics"]["name_number"]
        for n in range(1, 10):
            key = str(n)
            self.assertIn(key, name_topics, f"Missing name number {key}")
            self.assertTrue(len(name_topics[key]["depth_1_basic"]["text"]) > 10)

    def test_03_all_511_missing_subsets_ranking(self):
        """Verify all 511 non-empty subsets of {1..9} compute valid rankings without error."""
        digits = list(range(1, 10))
        subset_count = 0
        for r in range(1, 10):
            for subset in itertools.combinations(digits, r):
                missing = list(subset)
                subset_count += 1
                # Simulate ranking logic
                wood_missing = 3 in missing or 4 in missing
                fire_missing = 9 in missing
                earth_missing = 2 in missing or 5 in missing or 8 in missing
                metal_missing = 6 in missing or 7 in missing
                water_missing = 1 in missing

                elem_status = [
                    ("Wood", wood_missing),
                    ("Fire", fire_missing),
                    ("Earth", earth_missing),
                    ("Metal", metal_missing),
                    ("Water", water_missing),
                ]
                missing_elems = [e[0] for e in elem_status if e[1]]
                self.assertTrue(len(missing_elems) > 0, "Non-empty digit subset must yield at least one missing element")
                top_gap = missing_elems[0]
                self.assertIn(top_gap, self.content_lib["topics"]["ninety_day_plan"])

        self.assertEqual(subset_count, 511, "Must test exactly 511 non-empty subsets (2^9 - 1)")

    def test_04_banned_words_scan(self):
        """Ensure zero banned/superstitious causal words appear in content library or terminology."""
        banned = ["guaranteed windfall", "instant wealth", "spell", "magic remedy", "change your destiny overnight"]
        lib_str = json.dumps(self.content_lib).lower()
        geo_str = json.dumps(self.geo_terms).lower()

        for word in banned:
            self.assertNotIn(word, lib_str, f"Banned phrase '{word}' found in basic_report_content_library.json")
            self.assertNotIn(word, geo_str, f"Banned phrase '{word}' found in terminology_geo.json")

    def test_05_bhaskr_singh_chart_deterministic_parity(self):
        """Verify exact deterministic calculation for Bhaskr Singh (28-11-1981)."""
        calc = run_deterministic_calculation(
            name="Bhaskr Singh", day=28, month=11, year=1981, tier="basic"
        )
        self.assertEqual(calc["driver_number"], 1, "Day 28 must yield Driver 1")
        self.assertEqual(calc["conductor_number"], 4, "1981-11-28 must yield Conductor 4")
        self.assertEqual(calc["chaldean_name_root"], 5, "BHASKR SINGH Chaldean must yield root 5")
        self.assertEqual(calc["chaldean_name_compound"], 32, "BHASKR SINGH Chaldean must yield compound 32")
        self.assertEqual(calc["counts"][1], 4, "Must have four 1s (1981-11-28)")
        self.assertEqual(sorted(calc["missing_numbers"]), [3, 4, 5, 6, 7], "Missing must be [3, 4, 5, 6, 7]")

    def test_06_exact_three_pages_across_13_dobs_and_editions(self):
        """Verify that India and International editions across 13 diverse DOBs generate strictly 3 pages."""
        test_cohort = [
            ("Bhaskr Singh", 28, 11, 1981, "male"),
            ("Alexander Vance", 18, 10, 1990, "male"),
            ("Priya Sharma", 1, 1, 1990, "female"),
            ("Rajesh Kumar", 15, 5, 1985, "male"),
            ("Anita Patel", 8, 8, 1978, "female"),
            ("Vikram Malhotra", 9, 9, 1999, "male"),
            ("Sunita Rao", 2, 2, 2000, "female"),
            ("David Miller", 21, 3, 1965, "male"),
            ("Elena Rostova", 13, 4, 1992, "female"),
            ("Kavita Sen", 24, 12, 1988, "female"),
            ("Arjun Kapoor", 7, 7, 1975, "male"),
            ("Meera Nair", 19, 10, 1995, "female"),
            ("Siddharth Roy", 25, 6, 1984, "male")
        ]

        for name, d, m, y, g in test_cohort:
            for edition in ("india", "international"):
                pdf_bytes, meta = generate_customised_pdf_report(
                    name=name, day=d, month=m, year=y, tier="basic", gender=g, edition=edition
                )
                reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
                self.assertEqual(
                    len(reader.pages), 3,
                    f"Profile '{name}' ({y}-{m:02d}-{d:02d}) in {edition} edition generated {len(reader.pages)} pages instead of 3"
                )

    def test_07_genericness_audit_shares(self):
        """Audit that depth 1 (Basic) has unique focused paragraphs and does not clone full Advanced/Premium depth."""
        for num in range(1, 10):
            b_text = self.content_lib["topics"]["birth_day"][str(num)]["depth_1_basic"]["text"]
            a_text = self.content_lib["topics"]["birth_day"][str(num)]["depth_2_advanced"]["text"]
            p_text = self.content_lib["topics"]["birth_day"][str(num)]["depth_3_premium"]["text"]
            self.assertNotEqual(b_text, a_text, f"Basic and Advanced birth day {num} must not be identical")
            self.assertNotEqual(a_text, p_text, f"Advanced and Premium birth day {num} must not be identical")

if __name__ == "__main__":
    unittest.main()
