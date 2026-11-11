import json
import os
import subprocess
import unittest
import pymupdf

from app.engine.kua import (
    KUA_METADATA,
    KUA_NEEDS_GENDER_TEXT,
    KUA_RULE_TEXT,
    calculate_kua_details,
    calculate_kua_number,
)
from app.engine.core_matrix_engine import (
    calculate_kua_number as core_calc_kua,
    get_kua_profile,
)
from app.engine.professional_numerology_engine import (
    analyze_kua_and_directions,
    calculate_kua as prof_calc_kua,
)
from app.services.pdf_report_generator import (
    generate_customised_pdf_report,
    run_deterministic_calculation,
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestCanonicalKuaFormula(unittest.TestCase):
    """Verifies the approved century-invariant 4-digit Kua formula across Python, Browser JS, Worker, and PDF."""

    EXACT_CASES = [
        # (year, gender, expected_raw_before_5_map, expected_final_kua)
        (1981, "male", 1, 1),
        (1985, "male", 6, 6),
        (1979, "male", 3, 3),
        (1990, "male", 1, 1),
        (2002, "male", 7, 7),
        (1986, "male", 5, 2),      # 5 -> 2 for male
        (1995, "female", 1, 1),
        (1993, "female", 8, 8),
        (1981, "female", 5, 8),    # 5 -> 8 for female
        (2002, "female", 8, 8),
    ]

    def test_01_exact_approved_table_and_print_output(self):
        rows = []
        print("\n=== APPROVED KUA TEST TABLE OUTPUT ===")
        print(
            f"{'Gender':<8} | {'Year':<6} | {'x':<3} | {'Raw->Final':<10} | {'Element':<7} | {'Trigram':<7} | {'Group':<10} | {'Rule'}"
        )
        print("-" * 108)
        for year, gender, exp_raw, exp_final in self.EXACT_CASES:
            res = calculate_kua_details(year, gender)
            self.assertEqual(res["status"], "OK")
            self.assertEqual(res["raw_kua"], exp_raw, f"Raw mismatch for {gender} {year}")
            self.assertEqual(res["kua_number"], exp_final, f"Final Kua mismatch for {gender} {year}")
            self.assertEqual(calculate_kua_number(year, gender), exp_final)
            self.assertEqual(core_calc_kua(year, gender), exp_final)
            self.assertEqual(prof_calc_kua(gender, year), exp_final)
            prof_dir = analyze_kua_and_directions(gender, year)
            self.assertEqual(prof_dir["kua_number"], exp_final)
            self.assertEqual(res["rule_note"], KUA_RULE_TEXT)
            arrow = f"{exp_raw}->{exp_final}" if exp_raw == 5 else f"{exp_final}"
            print(
                f"{gender:<8} | {year:<6} | {res['year_digit_root']:<3} | {arrow:<10} | "
                f"{res['element']:<7} | {res['trigram']:<7} | {res['group']:<10} | {res['rule_note']}"
            )
            rows.append(res)
        self.assertEqual(len(rows), 10)

    def test_02_years_1900_to_2099_sweep_both_genders(self):
        seen_elements = set()
        seen_groups = set()
        total_checked = 0
        for year in range(1900, 2100):
            for gender in ("male", "female"):
                res = calculate_kua_details(year, gender)
                kua = res["kua_number"]
                self.assertEqual(res["status"], "OK")
                self.assertIsInstance(kua, int)
                self.assertGreaterEqual(kua, 1, f"Kua < 1 for {gender} {year}")
                self.assertLessEqual(kua, 9, f"Kua > 9 for {gender} {year}")
                self.assertNotEqual(kua, 5, f"Kua must never be 5 ({gender} {year})")
                self.assertIn(kua, KUA_METADATA)
                self.assertEqual(res["element"], KUA_METADATA[kua]["element"])
                self.assertEqual(res["group"], KUA_METADATA[kua]["group"])
                seen_elements.add(res["element"])
                seen_groups.add(res["group"])
                total_checked += 1
        print(
            f"\n=== 1900-2099 SWEEP SUMMARY ===\n"
            f"Checked {total_checked} year/gender combinations (1900-2099 × male/female): "
            f"ALL in 1..9, ZERO 5s. Elements derived: {sorted(seen_elements)}, Groups: {sorted(seen_groups)}"
        )
        self.assertEqual(total_checked, 400)
        self.assertEqual(seen_groups, {"East Group", "West Group"})

    def test_03_missing_gender_never_guesses(self):
        for missing_val in (None, "", "   ", "unknown", "unspecified", "prefer_not_to_say", "other"):
            res = calculate_kua_details(1981, missing_val)
            self.assertEqual(res["status"], "NEEDS_GENDER")
            self.assertIsNone(res["kua_number"])
            self.assertEqual(res["display"], KUA_NEEDS_GENDER_TEXT)
            self.assertIsNone(calculate_kua_number(1981, missing_val))
            prof = get_kua_profile(1981, missing_val)
            self.assertIsNone(prof["kua_number"])
            self.assertEqual(prof["kua_display"], "Kua needs gender")

        det = run_deterministic_calculation(name="Bhaskr Singh", day=28, month=11, year=1981, gender=None)
        self.assertIsNone(det["kua_number"])
        self.assertEqual(det["kua_details"]["display"], "Kua needs gender")

    def test_04_browser_js_and_worker_js_parity(self):
        nv_kua_path = os.path.join(BASE_DIR, "app", "static", "js", "nv_kua.js").replace("\\", "/")
        worker_path = os.path.join(BASE_DIR, "app", "static", "_worker.js").replace("\\", "/")

        cases_json = json.dumps(
            [{"year": y, "gender": g, "expected": fin} for (y, g, _, fin) in self.EXACT_CASES]
        )

        # 1. Test Browser JS (nv_kua.js)
        browser_script = f"""
const NVKua = require('{nv_kua_path}');
const cases = {cases_json};
for (const c of cases) {{
  const d = NVKua.calculateKuaDetails(c.year, c.gender);
  if (d.kua_number !== c.expected || d.kuaNumber !== c.expected) {{
    throw new Error(`Browser mismatch ${{c.gender}} ${{c.year}}: got ${{d.kua_number}}, expected ${{c.expected}}`);
  }}
  if (d.rule_text !== 'Calculated from your birth year and gender') {{
    throw new Error('Missing rule_text in browser module');
  }}
}}
for (let y = 1900; y <= 2099; y++) {{
  for (const g of ['male', 'female']) {{
    const k = NVKua.calculateKua(y, g);
    if (!Number.isInteger(k) || k < 1 || k > 9 || k === 5) {{
      throw new Error(`Browser sweep failure ${{g}} ${{y}}: ${{k}}`);
    }}
  }}
}}
const missing = NVKua.calculateKuaDetails(1981, '');
if (missing.kua_number !== null || missing.display_text !== 'Kua needs gender') {{
  throw new Error('Browser missing-gender failure');
}}
console.log('BROWSER_JS_PARITY_OK');
"""
        proc_browser = subprocess.run(
            ["node", "-e", browser_script], capture_output=True, text=True, check=False
        )
        self.assertEqual(proc_browser.returncode, 0, proc_browser.stderr)
        self.assertIn("BROWSER_JS_PARITY_OK", proc_browser.stdout)

        # 2. Test Cloudflare Worker (_worker.js exported calculateCanonicalKuaDetails)
        worker_script = f"""
import {{ calculateCanonicalKuaDetails, KUA_RULE_TEXT, KUA_NEEDS_GENDER_TEXT }} from 'file:///{worker_path}';
const cases = {cases_json};
for (const c of cases) {{
  const d = calculateCanonicalKuaDetails(c.year, c.gender);
  if (d.kua_number !== c.expected || d.kuaNumber !== c.expected) {{
    throw new Error(`Worker mismatch ${{c.gender}} ${{c.year}}: got ${{d.kua_number}}, expected ${{c.expected}}`);
  }}
  if (d.rule_text !== KUA_RULE_TEXT) {{
    throw new Error('Worker rule_text mismatch');
  }}
}}
for (let y = 1900; y <= 2099; y++) {{
  for (const g of ['male', 'female']) {{
    const d = calculateCanonicalKuaDetails(y, g);
    if (!Number.isInteger(d.kua_number) || d.kua_number < 1 || d.kua_number > 9 || d.kua_number === 5) {{
      throw new Error(`Worker sweep failure ${{g}} ${{y}}: ${{d.kua_number}}`);
    }}
  }}
}}
const missing = calculateCanonicalKuaDetails(1995, null);
if (missing.kua_number !== null || missing.display_text !== KUA_NEEDS_GENDER_TEXT) {{
  throw new Error('Worker missing-gender failure');
}}
console.log('WORKER_JS_PARITY_OK');
"""
        proc_worker = subprocess.run(
            ["node", "--input-type=module", "-e", worker_script],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc_worker.returncode, 0, proc_worker.stderr)
        self.assertIn("WORKER_JS_PARITY_OK", proc_worker.stdout)

    def test_05_pdf_kua_rule_derived_group_missing_gender_and_angel_numbers(self):
        # Case A: Female 1993 -> Kua 8, Earth · Gen (West Group) (NOT hardcoded Water · Kan East Group!)
        pdf_f1993, meta_f = generate_customised_pdf_report(
            name="Meera Nair",
            day=14,
            month=8,
            year=1993,
            tier="basic",
            gender="female",
            edition="india",
        )
        self.assertEqual(meta_f["calculation_data"]["kua_number"], 8)
        doc_f = pymupdf.open(stream=pdf_f1993, filetype="pdf")
        text_f = " ".join("\n".join(page.get_text("text") for page in doc_f).split())
        self.assertEqual(len(doc_f), 3)
        self.assertIn("Calculated from your birth year and gender", text_f)
        self.assertIn("8 (Earth · Gen)", text_f)
        self.assertIn("West Group", text_f)
        self.assertNotIn("Water · Kan", text_f)

        # Case B: Missing gender -> "Kua needs gender"
        pdf_no_gender, meta_ng = generate_customised_pdf_report(
            name="Bhaskr Singh",
            day=28,
            month=11,
            year=1981,
            tier="basic",
            gender=None,
            edition="india",
        )
        self.assertIsNone(meta_ng["calculation_data"]["kua_number"])
        doc_ng = pymupdf.open(stream=pdf_no_gender, filetype="pdf")
        text_ng = " ".join("\n".join(page.get_text("text") for page in doc_ng).split())
        self.assertEqual(len(doc_ng), 3)
        self.assertIn("Kua needs gender", text_ng)
        self.assertIn("Calculated from your birth year and gender", text_ng)

        # Case C: Premium report Angel Numbers exact replacement check
        pdf_prem, meta_p = generate_customised_pdf_report(
            name="Bhaskr Singh",
            day=28,
            month=11,
            year=1981,
            tier="premium",
            gender="male",
            edition="india",
        )
        self.assertEqual(meta_p["calculation_data"]["kua_number"], 1)
        doc_prem = pymupdf.open(stream=pdf_prem, filetype="pdf")
        text_prem = " ".join("\n".join(page.get_text("text") for page in doc_prem).split())
        self.assertEqual(len(doc_prem), 32)
        self.assertIn(
            "777 signals reflective insight and inner alignment; 888 reflects structured commercial momentum and financial stewardship.",
            text_prem,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
