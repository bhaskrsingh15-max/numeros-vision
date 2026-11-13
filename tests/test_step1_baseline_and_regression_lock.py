"""
Step 1 Automated Verification Suite:
1. Verifies that the 10-logo endpoint audit (`tests/fixtures/step1_10_logo_audit_results.json`)
   ran across 5 SVG + 5 PNG samples and documented the exact production `405` (Cloudflare Worker)
   and `404` (Render `pdf_service`) statuses plus prototype defects.
2. Verifies the Build Safety Regression Lock (`scripts/verify_pack_regression_lock.py --verify`):
   zero changes to all 91 protected engine files and 100% deterministic parity across
   `report_basic` (3 pages), `report_advanced` (12 pages), `report_premium` (32 pages),
   and `planner_2027` (24 pages).
"""

import json
import pathlib
import unittest

from scripts.verify_pack_regression_lock import (
    BASELINE_PATH,
    compare_snapshots,
    generate_all_pack_fingerprints,
)

ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestStep1BaselineAndRegressionLock(unittest.TestCase):
    def test_10_logo_audit_results_complete(self):
        audit_json = ROOT / "tests" / "fixtures" / "step1_10_logo_audit_results.json"
        audit_md = ROOT / "docs" / "STEP1_LOGO_ENDPOINT_AND_REGRESSION_AUDIT.md"
        self.assertTrue(audit_json.is_file(), f"Missing {audit_json}")
        self.assertTrue(audit_md.is_file(), f"Missing {audit_md}")

        data = json.loads(audit_json.read_text(encoding="utf-8"))
        self.assertEqual(data["sample_count"], 10)
        self.assertEqual(data["svg_count"], 5)
        self.assertEqual(data["png_count"], 5)
        self.assertTrue(data["production_worker_all_405"])
        self.assertTrue(data["render_pdf_service_all_404"])

        proto = data["local_prototype_results"]
        self.assertEqual(len(proto), 10)
        # Confirm fake vector SVG defect is recorded
        fake_svg = proto["05_fake_vector_raster_and_script.svg"]
        self.assertTrue(fake_svg["analyze_is_vector"])
        self.assertTrue(any("Fake `.svg`" in d for d in fake_svg["defects_observed"]))
        # Confirm raster PNG lacks OCR in prototype
        wafel_png = proto["09_de_wow_wafel_demo.png"]
        self.assertIsNone(wafel_png["analyze_extracted_text"])

    def test_pack_regression_lock_zero_drift(self):
        self.assertTrue(pathlib.Path(BASELINE_PATH).is_file(), "Regression baseline missing")
        baseline = json.loads(pathlib.Path(BASELINE_PATH).read_text(encoding="utf-8"))
        current = generate_all_pack_fingerprints()
        diffs = compare_snapshots(baseline, current)
        self.assertEqual(diffs, [], f"Build safety regression lock failed: {diffs}")


if __name__ == "__main__":
    unittest.main()
