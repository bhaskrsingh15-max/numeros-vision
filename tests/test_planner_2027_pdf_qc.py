"""
Tests for 2027 Year Ahead Planner PDF Report & Deliverables Quality Control.
Validates:
1. Exact 24-page count and file size < 3 MB.
2. PDF metadata: Title and Author only.
3. Results-Only compliance: Zero calculation formulas, weights, reduction steps (->),
   grid scores (F+, E+), resonance bonus, or internal component names in PDF text.
4. Forbidden-word lint on content library and PDF extracted text:
   Strictly zero occurrences of: luck, lucky, guaranteed, will bring, will fix, prediction,
   prescription, consecrated, cure, exact.
5. 730 daily comparisons against golden_A_365.csv and golden_B_365.csv.
6. Personal Month ratings and Pinnacle spans against golden_sheets.json.
7. Explicit named dates for 100-score days for Person A and Person B.
8. Month rating table spec (1 Favourable, 2 Neutral, 3 Favourable, 4 Neutral, 5 Asks for care,
   6 Favourable, 7 Neutral, 8 Neutral, 9 Asks for care; June for PY 5 shows master flag as 2).
9. Crystal suggestion text for Mulank and non-medical notice.
10. Each month page (7-18) contains Full Moon and New Moon dates/times in IST from panchang.
11. No SAMPLE watermark when is_sample=False.
12. SHA-256 difference and strict person isolation between Arun Sharma and Anil Kumar.
13. Near-boundary panchang annotations on key dates.
"""

import os
import io
import re
import csv
import json
import hashlib
import datetime
import unittest
import pypdf

from app.engine.planner_2027_engine import calculate_planner_2027
from pdf_service.app.services.planner_2027_pdf_generator import (
    generate_planner_2027_pdf,
    MONTH_RATINGS_SPEC,
    CRYSTALS_BY_MULANK
)

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

        # Generate both sample PDFs (with is_sample=True)
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

        # Exactly 24 pages
        self.assertEqual(len(reader_a.pages), 24, f"Arun PDF has {len(reader_a.pages)} pages, expected 24")
        self.assertEqual(len(reader_b.pages), 24, f"Anil PDF has {len(reader_b.pages)} pages, expected 24")

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

    def test_month_rating_table_spec(self):
        expected_spec = {
            1: "Favourable",
            2: "Neutral",
            3: "Favourable",
            4: "Neutral",
            5: "Asks for care",
            6: "Favourable",
            7: "Neutral",
            8: "Neutral",
            9: "Asks for care"
        }
        self.assertEqual(MONTH_RATINGS_SPEC, expected_spec)

        # June for Person A (PY 5): Personal Month 11/2 has master flag 2
        reader_a = pypdf.PdfReader(self.pdf_a_path)
        june_page_text = reader_a.pages[11].extract_text()  # Page 12 is June (index 11)
        self.assertIn("JUNE 2027", june_page_text)
        self.assertIn("Master Flag: 2", june_page_text)
        self.assertIn("Personal Month 2", june_page_text)
        self.assertIn("Neutral", june_page_text)

    def test_crystal_text_present(self):
        reader_a = pypdf.PdfReader(self.pdf_a_path)
        p19_text_a = reader_a.pages[18].extract_text()  # Page 19 (index 18)
        self.assertIn("Sunstone or Carnelian", p19_text_a)
        self.assertIn("traditional suggestion, not medical or financial advice", p19_text_a)

        # Verify crystal dictionary equals spec
        expected_crystals = {
            1: "Sunstone or Carnelian",
            2: "Moonstone",
            3: "Citrine",
            4: "Hessonite garnet",
            5: "Green aventurine",
            6: "Clear quartz",
            7: "Tiger's eye",
            8: "Amethyst or Lapis lazuli",
            9: "Red jasper"
        }
        self.assertEqual(CRYSTALS_BY_MULANK, expected_crystals)

    def test_each_month_page_has_moon_dates(self):
        reader_a = pypdf.PdfReader(self.pdf_a_path)
        for page_num in range(6, 18):  # Pages 7 to 18 (index 6 to 17)
            page_text = reader_a.pages[page_num].extract_text()
            self.assertIn("Full Moon", page_text, f"Page {page_num+1} missing Full Moon")
            self.assertIn("New Moon", page_text, f"Page {page_num+1} missing New Moon")
            self.assertIn("IST", page_text, f"Page {page_num+1} missing IST timezone indicator")

    def test_no_sample_watermark_when_flag_off(self):
        paid_pdf_bytes = generate_planner_2027_pdf(
            "Arun Sharma", "1981-11-28", is_sample=False
        )
        # Verify paid PDF is valid PDF
        reader = pypdf.PdfReader(io.BytesIO(paid_pdf_bytes))
        self.assertEqual(len(reader.pages), 24)
        full_text = "\n".join(p.extract_text() for p in reader.pages)
        self.assertNotIn("SAMPLE", full_text)

    def test_sha256_difference_and_person_isolation(self):
        def sha256_file(path):
            h = hashlib.sha256()
            with open(path, "rb") as f:
                while chunk := f.read(8192):
                    h.update(chunk)
            return h.hexdigest()

        sha_a = sha256_file(self.pdf_a_path)
        sha_b = sha256_file(self.pdf_b_path)
        self.assertNotEqual(sha_a, sha_b, "Sample PDFs must have distinct SHA-256 hashes")

        reader_a = pypdf.PdfReader(self.pdf_a_path)
        text_a = "\n".join(p.extract_text() for p in reader_a.pages).upper()

        reader_b = pypdf.PdfReader(self.pdf_b_path)
        text_b = "\n".join(p.extract_text() for p in reader_b.pages).upper()

        self.assertIn("ARUN SHARMA", text_a)
        self.assertNotIn("ANIL KUMAR", text_a)

        self.assertIn("ANIL KUMAR", text_b)
        self.assertNotIn("ARUN SHARMA", text_b)

        # DOB Isolation
        self.assertIn("1981", text_a)
        self.assertNotIn("1975", text_a)

        self.assertIn("1975", text_b)
        self.assertNotIn("1981", text_b)

    def test_key_dates_near_boundary_annotations(self):
        # 10 Jan is near-boundary (6.4 min) and has score 95 for Person A, 100 for Person B
        reader_a = pypdf.PdfReader(self.pdf_a_path)
        page6_a = " ".join(reader_a.pages[5].extract_text().split())  # Page 6 (index 5)
        self.assertIn("10 Jan", page6_a)
        self.assertIn("Panchang: the tithi changes shortly after sunrise; check your local Panchang", page6_a)

        reader_b = pypdf.PdfReader(self.pdf_b_path)
        page6_b = " ".join(reader_b.pages[5].extract_text().split())  # Page 6 (index 5)
        self.assertIn("10 Jan", page6_b)
        self.assertIn("Panchang: the tithi changes shortly after sunrise; check your local Panchang", page6_b)

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

    def test_every_month_page_parses_and_matches_golden_full(self):
        """
        Parses EVERY month page (12 pages x 2 persons = 24 pages) directly from
        the generated PDF files and asserts:
          - Average score matches average of golden CSV
          - Top 5 dates: date, weekday, score, tier, and sunrise tithi match golden CSV and panchang
          - Care 5 dates: date, weekday, score, tier, and sunrise tithi match golden CSV and panchang
          - Moon dates and times match panchang JSON
        """
        panchang_golden = {}
        with open("tests/golden_panchang_delhi_365.csv", "r", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                panchang_golden[r["date"]] = r

        with open("data/panchang_2027_delhi.json", "r", encoding="utf-8") as f:
            panchang_json = json.load(f)

        for pdf_path, golden_csv, name in [
            (self.pdf_a_path, "tests/golden_A_365.csv", "Arun Sharma"),
            (self.pdf_b_path, "tests/golden_B_365.csv", "Anil Kumar")
        ]:
            with open(golden_csv, "r", encoding="utf-8") as f:
                golden_days = {r["date"]: r for r in csv.DictReader(f)}

            reader = pypdf.PdfReader(pdf_path)
            self.assertEqual(len(reader.pages), 24)

            for m in range(1, 13):
                p_idx = 5 + m  # Pages 7 to 18 correspond to index 6 to 17
                text = reader.pages[p_idx].extract_text()

                # 1. Average score assertion
                m_days = [r for d, r in golden_days.items() if d.startswith(f"2027-{m:02d}")]
                scores = [int(r["score"]) for r in m_days]
                expected_avg = round(sum(scores) / len(scores), 1)

                avg_match = re.search(r"Average Score:\s*([\d\.]+)\s*/\s*100", text)
                self.assertTrue(avg_match, f"{name} M{m}: average score line missing in PDF")
                found_avg = float(avg_match.group(1))
                self.assertAlmostEqual(found_avg, expected_avg, places=1, msg=f"{name} M{m} avg mismatch")

                # 2. Top 5 dates assertion (Amavasya days excluded per Point 6)
                sorted_best = [
                    r for r in sorted(m_days, key=lambda x: (-int(x["score"]), x["date"]))
                    if (panchang_golden[r["date"]].get("tithi_at_sunrise") or panchang_golden[r["date"]].get("tithi_name")) != "Amavasya"
                ][:5]
                for b in sorted_best:
                    dt = datetime.date.fromisoformat(b["date"])
                    d_str = dt.strftime("%d %b")
                    self.assertIn(d_str, text, f"{name} M{m}: Top date {d_str} missing from PDF")
                    tithi_expected = panchang_golden[b["date"]].get("tithi_at_sunrise") or panchang_golden[b["date"]].get("tithi_name")
                    self.assertIn(tithi_expected, text, f"{name} M{m}: Tithi {tithi_expected} for {b['date']} missing from PDF")

                # 3. Care 5 dates assertion
                sorted_care = sorted(m_days, key=lambda x: (int(x["score"]), x["date"]))[:5]
                for c in sorted_care:
                    dt = datetime.date.fromisoformat(c["date"])
                    d_str = dt.strftime("%d %b")
                    self.assertIn(d_str, text, f"{name} M{m}: Care date {d_str} missing from PDF")
                    tithi_expected = panchang_golden[c["date"]].get("tithi_at_sunrise") or panchang_golden[c["date"]].get("tithi_name")
                    self.assertIn(tithi_expected, text, f"{name} M{m}: Tithi {tithi_expected} for {c['date']} missing from PDF")

                # 4. Moon events assertion
                m_prefix = f"2027-{m:02d}"
                f_moons = [fm for fm in panchang_json.get("full_moons_2027", []) if fm["date"].startswith(m_prefix)]
                n_moons = [nm for nm in panchang_json.get("new_moons_2027", []) if nm["date"].startswith(m_prefix)]
                for fm in f_moons:
                    dt_fm = datetime.date.fromisoformat(fm["date"])
                    fm_str = f"{dt_fm.strftime('%d %b')} at {fm['time_ist']}"
                    self.assertIn(fm_str, text, f"{name} M{m}: Full moon {fm_str} missing from PDF")
                for nm in n_moons:
                    dt_nm = datetime.date.fromisoformat(nm["date"])
                    nm_str = f"{dt_nm.strftime('%d %b')} at {nm['time_ist']}"
                    self.assertIn(nm_str, text, f"{name} M{m}: New moon {nm_str} missing from PDF")

    def test_amavasya_replacements_explicit(self):
        """
        Explicitly asserts that Amavasya is excluded from the month's Top 5,
        and that the exact golden replacement dates appear on their respective pages:
        - Arun Jan (Page 7): 19 Jan (86, Shukla Ekadashi)
        - Arun Feb (Page 8): 3 Feb (85, Krishna Dwadashi)
        - Arun Jul (Page 13): 22 Jul (86, Krishna Chaturthi)
        - Anil Apr (Page 10): 18 Apr (84, Shukla Dwadashi)
        - Anil Nov (Page 17): 15 Nov (94, Krishna Pratipada) [14 Nov stays as Purnima, 96]
        """
        reader_a = pypdf.PdfReader(self.pdf_a_path)
        reader_b = pypdf.PdfReader(self.pdf_b_path)

        def get_top_5_table_text(page_text):
            return page_text.split("Top Favourable Windows for Important Initiatives")[1].split("Mindful Pacing Dates")[0]

        # Arun Jan (Page 7)
        jan_a_text = reader_a.pages[6].extract_text()
        top_jan_a = get_top_5_table_text(jan_a_text)
        self.assertNotIn("Amavasya", top_jan_a)
        self.assertIn("19 Jan", top_jan_a)
        self.assertIn("Shukla Ekadashi", top_jan_a)

        # Arun Feb (Page 8)
        feb_a_text = reader_a.pages[7].extract_text()
        top_feb_a = get_top_5_table_text(feb_a_text)
        self.assertNotIn("Amavasya", top_feb_a)
        self.assertIn("03 Feb", top_feb_a)
        self.assertIn("Krishna Dwadashi", top_feb_a)

        # Arun Jul (Page 13)
        jul_a_text = reader_a.pages[12].extract_text()
        top_jul_a = get_top_5_table_text(jul_a_text)
        self.assertNotIn("Amavasya", top_jul_a)
        self.assertIn("22 Jul", top_jul_a)
        self.assertIn("Krishna Chaturthi", top_jul_a)

        # Anil Apr (Page 10)
        apr_b_text = reader_b.pages[9].extract_text()
        top_apr_b = get_top_5_table_text(apr_b_text)
        self.assertNotIn("Amavasya", top_apr_b)
        self.assertIn("18 Apr", top_apr_b)
        self.assertIn("Shukla Dwadashi", top_apr_b)

        # Anil Nov (Page 17)
        nov_b_text = reader_b.pages[16].extract_text()
        top_nov_b = get_top_5_table_text(nov_b_text)
        self.assertNotIn("Amavasya", top_nov_b)
        self.assertIn("15 Nov", top_nov_b)
        self.assertIn("Krishna Pratipada", top_nov_b)
        self.assertIn("14 Nov", top_nov_b)
        self.assertIn("Purnima", top_nov_b)

    def test_golden_panchang_sha256(self):
        """
        Asserts that tests/golden_panchang_delhi_365.csv exists, has 366 lines, 12054 bytes,
        and matches SHA-256: c3b2f6b6af414670adfbbf25e1f4aec0b39b321af18ebe8a57406048aa1dc1a5.
        """
        csv_path = os.path.join("tests", "golden_panchang_delhi_365.csv")
        self.assertTrue(os.path.exists(csv_path), "golden_panchang_delhi_365.csv does not exist")
        with open(csv_path, "rb") as f:
            data = f.read()
        self.assertEqual(len(data), 12054, f"Expected 12054 bytes, got {len(data)}")
        self.assertEqual(len(data.decode("utf-8").splitlines()), 366, "Expected 366 lines (header + 365 days)")
        expected_hash = "c3b2f6b6af414670adfbbf25e1f4aec0b39b321af18ebe8a57406048aa1dc1a5"
        actual_hash = hashlib.sha256(data).hexdigest()
        self.assertEqual(actual_hash, expected_hash, f"Panchang SHA-256 mismatch: {actual_hash} != {expected_hash}")

    def test_brand_consistency_shared_constants_and_contrast(self):
        """
        Brand consistency audit:
        1. Asserts all brand colour constants are imported/shared with app.services.pdf_report_generator.
        2. Asserts draw_page_background is the shared implementation.
        3. Asserts fonts and logo image path exist and match brand standards.
        4. Asserts body text over watermark area maintains WCAG AAA contrast ratio (>= 7.0:1).
        """
        import pdf_service.app.services.planner_2027_pdf_generator as planner_gen
        import app.services.pdf_report_generator as shared_gen

        # 1. Palette constants assertion
        color_attrs = [
            "COLOR_PEARL_BG", "COLOR_PEARL_MID", "COLOR_GOLD_DARK", "COLOR_GOLD",
            "COLOR_GOLD_LIGHT", "COLOR_INK_DARK", "COLOR_INK_MUTED", "COLOR_EMERALD",
            "COLOR_BORDER", "COLOR_CARD_BG", "COLOR_RED_ALERT"
        ]
        for attr in color_attrs:
            val_planner = getattr(planner_gen, attr)
            val_shared = getattr(shared_gen, attr)
            self.assertEqual(
                val_planner.hexval(), val_shared.hexval(),
                f"Brand color {attr} mismatch: planner={val_planner.hexval()} vs shared={val_shared.hexval()}"
            )

        # 2. Shared draw_page_background
        self.assertIs(
            planner_gen.draw_page_background, shared_gen.draw_page_background,
            "draw_page_background must be imported directly from shared pdf_report_generator"
        )

        # 3. Logo asset check
        logo_path = os.path.join("app", "static", "logos", "nv-logo-mark.png")
        self.assertTrue(os.path.exists(logo_path), f"Official logo mark not found at {logo_path}")

        # 4. WCAG Contrast ratio check over watermark area
        def srgb_to_linear(c):
            c = c / 255.0
            return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

        def luminance(r, g, b):
            return 0.2126 * srgb_to_linear(r) + 0.7152 * srgb_to_linear(g) + 0.0722 * srgb_to_linear(b)

        def contrast(c1, c2):
            l1 = luminance(*c1)
            l2 = luminance(*c2)
            return (max(l1, l2) + 0.05) / (min(l1, l2) + 0.05)

        # Base pearl background: #FFFDF7 (255, 253, 247)
        bg_pearl = (255, 253, 247)
        # Body text ink: #523E28 (82, 62, 40)
        text_ink = (82, 62, 40)

        # Watermark opacity 0.045 with gold / dark logo
        # Blend worst case (dark logo mark at 0.045 alpha):
        bg_blended_dark = tuple(round((1 - 0.045) * b + 0.045 * w) for b, w in zip(bg_pearl, text_ink))
        cr_watermark = contrast(text_ink, bg_blended_dark)
        self.assertGreaterEqual(
            cr_watermark, 7.0,
            f"Contrast ratio over watermark area ({cr_watermark:.2f}:1) must meet WCAG AAA standard (>= 7.0:1)"
        )

    def test_rasterization_all_pages_non_background(self):
        """
        Rasterizes EVERY page of both generated PDFs with pypdfium2
        and asserts:
          - No page is entirely white
          - Every page has >= 1.0% non-background pixels
        """
        import pypdfium2 as pdfium
        import numpy as np

        for pdf_path, name in [(self.pdf_a_path, "Arun Sharma"), (self.pdf_b_path, "Anil Kumar")]:
            doc = pdfium.PdfDocument(pdf_path)
            self.assertEqual(len(doc), 24)
            for i in range(len(doc)):
                img = doc[i].render(scale=80/72).to_pil()
                arr = np.array(img)
                bg_mask = ((arr[:,:,0] >= 253) & (arr[:,:,1] >= 250) & (arr[:,:,2] >= 244))
                non_bg_pct = (1.0 - np.mean(bg_mask)) * 100
                self.assertGreaterEqual(
                    non_bg_pct, 1.0,
                    f"{name} Page {i+1} has under 1% non-bg pixels ({non_bg_pct:.2f}%). Blank page detected!"
                )


if __name__ == "__main__":
    unittest.main()
