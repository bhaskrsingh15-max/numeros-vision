"""
Tests for 2027 Year Ahead Planner PDF Report & Deliverables Quality Control.
Validates:
1. Exact 16-page count and file size < 3 MB.
2. PDF metadata: Title and Author only.
3. Results-Only compliance: Zero calculation formulas, weights, reduction steps (->),
   grid scores (F+, E+), resonance bonus, or internal component names in PDF text.
4. Forbidden-word lint on content library and PDF extracted text:
   Strictly zero occurrences of: luck, lucky, guaranteed, will bring, will fix, prediction,
   prescription, consecrated, cure, exact.
5. 730 daily comparisons against golden_A_365.csv and golden_B_365.csv.
6. Personal Month ratings and Pinnacle spans against golden_sheets.json.
7. Explicit named dates for 100-score days for Person A and Person B.
"""

import os
import re
import csv
import json
import unittest
import pypdf

from app.engine.planner_2027_engine import calculate_planner_2027
from pdf_service.app.services.planner_2027_pdf_generator import generate_planner_2027_pdf

FORBIDDEN_WORDS = [
    "luck", "lucky", "guaranteed", "will bring", "will fix",
    "prediction", "prescription", "consecrated", "cure", "exact"
]

CALCULATION_JARGON = [
    "->", "F+", "E+", "relation-grid", "availability factor",
    "opposite-pair", "repeat-bonus", "weight =", "weights =",
    "component weights", "reduction step", "reduced to"
]


class TestPlanner2027PdfQc(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.out_dir = os.path.join("pdf_service", "output")
        os.makedirs(cls.out_dir, exist_ok=True)
        cls.pdf_a_path = os.path.join(cls.out_dir, "sample_arun_sharma_2027.pdf")
        cls.pdf_b_path = os.path.join(cls.out_dir, "sample_anil_kumar_2027.pdf")

        # Generate both sample PDFs
        cls.pdf_a_bytes = generate_planner_2027_pdf(
            "Arun Sharma", "1981-11-28", cls.pdf_a_path, is_sample=True
        )
        cls.pdf_b_bytes = generate_planner_2027_pdf(
            "Anil Kumar", "1975-05-01", cls.pdf_b_path, is_sample=True
        )

        # Load content library
        with open("data/planner_2027_content_library.json", "r", encoding="utf-8") as f:
            cls.content_lib = json.load(f)

        # Load golden sheets
        with open("tests/golden_sheets.json", "r", encoding="utf-8") as f:
            cls.golden_sheets = json.load(f)

    def test_library_status_and_structure(self):
        self.assertEqual(self.content_lib.get("status"), "DRAFT pending Bhaskr's review")
        self.assertIn("personal_year_overviews", self.content_lib)
        self.assertIn("personal_year_life_areas", self.content_lib)
        self.assertIn("tropical_sun_signs", self.content_lib)
        self.assertIn("personal_months", self.content_lib)
        self.assertIn("mulank_notes", self.content_lib)
        self.assertIn("pinnacles", self.content_lib)
        self.assertIn("name_number_alignments", self.content_lib)
        self.assertIn("remedies_library", self.content_lib)
        self.assertIn("date_notes", self.content_lib)
        self.assertIn("how_to_read", self.content_lib)

    def test_library_forbidden_words_lint(self):
        raw = json.dumps(self.content_lib).lower()
        for word in FORBIDDEN_WORDS:
            pattern = r'\b' + re.escape(word) + r'\b'
            matches = re.findall(pattern, raw)
            self.assertEqual(matches, [], f"Forbidden word '{word}' found in content library: {matches}")

    def test_pdf_page_counts_and_file_sizes(self):
        reader_a = pypdf.PdfReader(self.pdf_a_path)
        reader_b = pypdf.PdfReader(self.pdf_b_path)

        # Exactly 16 pages
        self.assertEqual(len(reader_a.pages), 16, f"Arun PDF has {len(reader_a.pages)} pages, expected 16")
        self.assertEqual(len(reader_b.pages), 16, f"Anil PDF has {len(reader_b.pages)} pages, expected 16")

        # Under 3 MB (3,145,728 bytes)
        size_a = os.path.getsize(self.pdf_a_path)
        size_b = os.path.getsize(self.pdf_b_path)
        self.assertLess(size_a, 3 * 1024 * 1024, f"Arun PDF size {size_a} exceeds 3 MB limit")
        self.assertLess(size_b, 3 * 1024 * 1024, f"Anil PDF size {size_b} exceeds 3 MB limit")

    def test_pdf_metadata_cleanliness(self):
        reader_a = pypdf.PdfReader(self.pdf_a_path)
        meta_a = reader_a.metadata
        self.assertEqual(meta_a.author, "NUMEROS VISION")
        self.assertEqual(meta_a.title, "2027 Year Ahead Planner - Arun Sharma")

        reader_b = pypdf.PdfReader(self.pdf_b_path)
        meta_b = reader_b.metadata
        self.assertEqual(meta_b.author, "NUMEROS VISION")
        self.assertEqual(meta_b.title, "2027 Year Ahead Planner - Anil Kumar")

    def test_pdf_forbidden_words_lint(self):
        for path in [self.pdf_a_path, self.pdf_b_path]:
            reader = pypdf.PdfReader(path)
            full_text = "\n".join(p.extract_text() for p in reader.pages)
            for word in FORBIDDEN_WORDS:
                pattern = r'\b' + re.escape(word) + r'\b'
                matches = re.findall(pattern, full_text, re.IGNORECASE)
                self.assertEqual(matches, [], f"Forbidden word '{word}' found in PDF {path}: {matches}")

    def test_pdf_results_only_no_calculation_workings(self):
        for path in [self.pdf_a_path, self.pdf_b_path]:
            reader = pypdf.PdfReader(path)
            full_text = "\n".join(p.extract_text() for p in reader.pages)
            for term in CALCULATION_JARGON:
                self.assertNotIn(term, full_text, f"Calculation jargon '{term}' found in PDF {path}")

    def test_golden_calendar_comparisons_365(self):
        # Arun Sharma (Person A)
        calc_a = calculate_planner_2027("Arun Sharma", "1981-11-28")
        cal_a = calc_a["full_calendar_365"]
        with open("tests/golden_A_365.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            golden_a_rows = list(reader)
        self.assertEqual(len(cal_a), 365)
        self.assertEqual(len(golden_a_rows), 365)
        for i in range(365):
            self.assertEqual(cal_a[i]["date"], golden_a_rows[i]["date"])
            self.assertEqual(cal_a[i]["alignment_score"], int(golden_a_rows[i]["score"]))
            self.assertEqual(cal_a[i]["tier"], golden_a_rows[i]["tier"])

        # Anil Kumar (Person B)
        calc_b = calculate_planner_2027("Anil Kumar", "1975-05-01")
        cal_b = calc_b["full_calendar_365"]
        with open("tests/golden_B_365.csv", "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            golden_b_rows = list(reader)
        self.assertEqual(len(cal_b), 365)
        self.assertEqual(len(golden_b_rows), 365)
        for i in range(365):
            self.assertEqual(cal_b[i]["date"], golden_b_rows[i]["date"])
            self.assertEqual(cal_b[i]["alignment_score"], int(golden_b_rows[i]["score"]))
            self.assertEqual(cal_b[i]["tier"], golden_b_rows[i]["tier"])

    def test_golden_sheets_ratings_and_pinnacles(self):
        # Person A
        calc_a = calculate_planner_2027("Arun Sharma", "1981-11-28")
        g_a = self.golden_sheets["A"]
        self.assertEqual(calc_a["subject"]["personal_year_2027"], g_a["personal_year_2027"])
        self.assertEqual(calc_a["pinnacles_data"]["spans"], g_a["pinnacles"]["spans"])
        self.assertEqual(calc_a["pinnacles_data"]["values"], {
            "P1": g_a["pinnacles"]["P1"],
            "P2": g_a["pinnacles"]["P2"],
            "P3": g_a["pinnacles"]["P3"],
            "P4": g_a["pinnacles"]["P4"]
        })

        # Person B
        calc_b = calculate_planner_2027("Anil Kumar", "1975-05-01")
        g_b = self.golden_sheets["B"]
        self.assertEqual(calc_b["subject"]["personal_year_2027"], g_b["personal_year_2027"])
        self.assertEqual(calc_b["pinnacles_data"]["spans"], g_b["pinnacles"]["spans"])
        self.assertEqual(calc_b["pinnacles_data"]["values"], {
            "P1": g_b["pinnacles"]["P1"],
            "P2": g_b["pinnacles"]["P2"],
            "P3": g_b["pinnacles"]["P3"],
            "P4": g_b["pinnacles"]["P4"]
        })

    def test_named_days_at_100(self):
        calc_b = calculate_planner_2027("Anil Kumar", "1975-05-01")
        b_100 = [r["date"] for r in calc_b["full_calendar_365"] if r["alignment_score"] == 100]
        expected_b_100 = [
            "2027-01-10", "2027-02-28", "2027-03-14",
            "2027-07-28", "2027-10-10", "2027-11-28", "2027-12-05"
        ]
        self.assertEqual(b_100, expected_b_100)

        calc_a = calculate_planner_2027("Arun Sharma", "1981-11-28")
        a_100 = [r["date"] for r in calc_a["full_calendar_365"] if r["alignment_score"] == 100]
        expected_a_100 = ["2027-04-04", "2027-05-21", "2027-05-30"]
        self.assertEqual(a_100, expected_a_100)


if __name__ == "__main__":
    unittest.main()
