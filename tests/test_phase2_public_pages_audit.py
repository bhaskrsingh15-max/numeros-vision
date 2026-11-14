import os
import unittest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATIC_DIR = os.path.join(REPO_ROOT, "app", "static")


class TestPhase2PublicPagesAudit(unittest.TestCase):
    def test_static_folder_zero_audit_needles(self):
        """Phase 2 Acceptance: Searching the static folder finds no bypassLogoLockForTest,
        no unlocked=true, no 9.93, no Legal Certification, and no || 26."""
        forbidden = [
            ("bypassLogoLockForTest", False),
            ("unlocked=true", False),
            ("9.93", False),
            ("legal certification", True),
            ("|| 26", False),
        ]
        violations = []
        for root, _, files in os.walk(STATIC_DIR):
            for fname in sorted(files):
                if not fname.lower().endswith((".html", ".js", ".css", ".json")):
                    continue
                fpath = os.path.join(root, fname)
                rel = os.path.relpath(fpath, STATIC_DIR)
                with open(fpath, encoding="utf-8", errors="replace") as fh:
                    content = fh.read()
                content_lower = content.lower()
                for needle, ci in forbidden:
                    haystack = content_lower if ci else content
                    target = needle.lower() if ci else needle
                    if target in haystack:
                        violations.append(f"{rel}: found '{needle}'")
        self.assertEqual(violations, [], f"Static folder contains forbidden Phase 2 patterns: {violations}")

    def test_logo_studio_clean_and_backed_by_phase5_service(self):
        path = os.path.join(STATIC_DIR, "tools", "logo-intelligence.html")
        with open(path, encoding="utf-8") as fh:
            html = fh.read()
        for bad in [
            "Scripts have been safely removed",
            "Certified Multi-Gate Independent Audit",
            "100% Exact Wordmark OCR Match",
            "AAA Pass",
            "Pearl Luxe",
            "Standard palette",
            "Evaluated in viewer",
            "|| 8",
            "|| 4.5",
            "alert(",
            "/checkout/?plan=report_master",
            "calculateChaldeanWordmark",
            "nvLogoStudioComingSoon",
        ]:
            self.assertNotIn(bad, html, f"logo-intelligence.html still contains '{bad}'")
        self.assertIn("nv_tool_runtime.js", html)
        self.assertIn("nv_logo_studio_v1.js", html)
        self.assertIn("fourSeparateResultsGrid", html)

    def test_all_ten_tools_backed_and_have_no_alerts_or_broken_links(self):
        backed_tools = [
            "logo-intelligence.html",
            "business-alignment.html",
            "mobile-numerology.html",
            "property-numerology.html",
            "vehicle-numerology.html",
            "blessing-years.html",
            "name-balancing.html",
            "baby-naming.html",
            "profession-calculator.html",
            "compatibility-calculator.html",
        ]
        for fname in backed_tools:
            path = os.path.join(STATIC_DIR, "tools", fname)
            with open(path, encoding="utf-8") as fh:
                html = fh.read()
            self.assertIn("nv_tool_runtime.js", html, f"{fname} missing nv_tool_runtime.js")
            self.assertNotIn("alert(", html, f"{fname} still contains alert()")
            self.assertNotIn("/checkout/?plan=report_master", html, f"{fname} has broken report_master checkout URL")

    def test_calculator_pages_no_master_number_loops(self):
        calc_pages = [
            "index.html",
            "pythagorean_calculator.html",
            "reports_catalogue.html",
            "tools/life-path-calculator.html",
            "tools/lo-shu-grid.html",
            "tools/name-numerology.html",
            "tools/favourable-numbers.html",
            "tools/property-numerology.html",
            "tools/baby-naming.html",
            "tools/compatibility-calculator.html",
        ]
        for rel in calc_pages:
            path = os.path.join(STATIC_DIR, rel)
            with open(path, encoding="utf-8") as fh:
                html = fh.read()
            self.assertNotIn("!== 11", html, f"{rel} still preserves master 11")
            self.assertNotIn("=== 11 || n === 22", html, f"{rel} still preserves master 11/22")
            self.assertNotIn("reduceToSingle(totalSum, true)", html, f"{rel} still passes preserveMaster=true")


if __name__ == "__main__":
    unittest.main()
