"""
STRICT AUDIT & QC TEST SUITE: PLANETARY PACKAGE REPORT FLOW-DOWN & DELIVERABLES
Verifies that when a seeker purchases ANY planetary package, the system generates the EXACT,
tailored, problem-based solution report with zero dilution, zero generic filler, and exact page depth.
"""

import sys
import os
import re
import unittest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app
from app.engine.package_report_generator import generate_package_report
from app.engine.claim_validator import BANNED_WORDS

class TestPlanetPackageReportFlowdownQC(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        self.profile = {
            "name": "Bhaskr Singh",
            "day": 28,
            "month": 11,
            "year": 1981,
            "birth_time": "11:10 AM",
            "birth_city": "Chennai"
        }

    # ──────────────────────────────────────────────────────────────────────────
    # 1. VENUS (SHUKRA) · LOVE & MARRIAGE PACKAGES (ROOT 6)
    # ──────────────────────────────────────────────────────────────────────────
    def test_union_packages_flowdown(self):
        # 1. Tripwire (₹105, 3 Pages)
        rep1 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_union_tripwire")
        self.assertEqual(rep1["price_inr"], 105)
        self.assertEqual(rep1["page_target"], "3 Pages")
        self.assertEqual(rep1["harmonic_root"], 6)
        self.assertIn("Spousal Harmony", rep1["report_markdown"])
        self.assertIn("Friday", rep1["report_markdown"])

        # 2. Master Dossier (₹489, 12 Pages)
        rep2 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_union_master")
        self.assertEqual(rep2["price_inr"], 489)
        self.assertEqual(rep2["page_target"], "12 Pages")
        self.assertIn("Ishta Devata", rep2["report_markdown"])
        self.assertIn("Lo Shu", rep2["report_markdown"])

        # 3. Sovereign (₹5,100, 32 Pages)
        rep3 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_union_sovereign")
        self.assertEqual(rep3["price_inr"], 5100)
        self.assertEqual(rep3["page_target"], "32 Pages")
        self.assertIn("Chaldean Legal & Calling Name Harmonization", rep3["report_markdown"])
        self.assertIn("Synastry", rep3["report_markdown"])

    # ──────────────────────────────────────────────────────────────────────────
    # 2. MERCURY (BUDH) · WEALTH & COMMERCE PACKAGES (ROOT 5)
    # ──────────────────────────────────────────────────────────────────────────
    def test_commerce_packages_flowdown(self):
        # 1. Tripwire (₹149, 3 Pages)
        rep1 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_commerce_tripwire")
        self.assertEqual(rep1["price_inr"], 149)
        self.assertEqual(rep1["page_target"], "3 Pages")
        self.assertEqual(rep1["harmonic_root"], 5)
        self.assertIn("Missing Number 5 & Cash Drainage Audit", rep1["report_markdown"])
        self.assertIn("Wednesday", rep1["report_markdown"])

        # 2. Master Dossier (₹599, 12 Pages)
        rep2 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_commerce_master")
        self.assertEqual(rep2["price_inr"], 599)
        self.assertEqual(rep2["page_target"], "12 Pages")
        self.assertIn("4-5-6", rep2["report_markdown"])
        self.assertIn("2-5-8", rep2["report_markdown"])

        # 3. Sovereign (₹5,999, 32 Pages)
        rep3 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_commerce_sovereign")
        self.assertEqual(rep3["price_inr"], 5999)
        self.assertEqual(rep3["page_target"], "32 Pages")
        self.assertIn("GST Entity Name", rep3["report_markdown"])

    # ──────────────────────────────────────────────────────────────────────────
    # 3. SUN (SURYA) · CAREER & PROMOTION PACKAGES (ROOT 1)
    # ──────────────────────────────────────────────────────────────────────────
    def test_authority_packages_flowdown(self):
        # 1. Tripwire (₹199, 3 Pages)
        rep1 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_authority_tripwire")
        self.assertEqual(rep1["price_inr"], 199)
        self.assertEqual(rep1["page_target"], "3 Pages")
        self.assertEqual(rep1["harmonic_root"], 1)
        self.assertIn("Office Politics", rep1["report_markdown"])

        # 2. Master Dossier (₹550, 12 Pages)
        rep2 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_authority_master")
        self.assertEqual(rep2["price_inr"], 550)
        self.assertEqual(rep2["page_target"], "12 Pages")
        self.assertIn("1-5-9", rep2["report_markdown"])

        # 3. Sovereign (₹5,500, 32 Pages)
        rep3 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_authority_sovereign")
        self.assertEqual(rep3["price_inr"], 5500)
        self.assertEqual(rep3["page_target"], "32 Pages")
        self.assertIn("Name Spelling Rectification", rep3["report_markdown"])

    # ──────────────────────────────────────────────────────────────────────────
    # 4. GLOBAL RELOCATION & VISA PACKAGES (ROOT 5 & 6)
    # ──────────────────────────────────────────────────────────────────────────
    def test_relocation_packages_flowdown(self):
        # 1. Tripwire (₹149, 3 Pages)
        rep1 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_relocation_tripwire")
        self.assertEqual(rep1["price_inr"], 149)
        self.assertEqual(rep1["page_target"], "3 Pages")
        self.assertIn("Visa Lodgment", rep1["report_markdown"])

        # 2. Master Dossier (₹489, 12 Pages)
        rep2 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_relocation_master")
        self.assertEqual(rep2["price_inr"], 489)
        self.assertEqual(rep2["page_target"], "12 Pages")
        self.assertIn("Permanent Residency", rep2["report_markdown"])

        # 3. Sovereign (₹5,100, 32 Pages)
        rep3 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_relocation_sovereign")
        self.assertEqual(rep3["price_inr"], 5100)
        self.assertEqual(rep3["page_target"], "32 Pages")
        self.assertIn("Passport Name Spelling", rep3["report_markdown"])

    # ──────────────────────────────────────────────────────────────────────────
    # 5. JUPITER (GURU) · DHARMA & PURPOSE PACKAGES (ROOT 3)
    # ──────────────────────────────────────────────────────────────────────────
    def test_dharma_packages_flowdown(self):
        # 1. Tripwire (₹120, 3 Pages)
        rep1 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_dharma_tripwire")
        self.assertEqual(rep1["price_inr"], 120)
        self.assertEqual(rep1["page_target"], "3 Pages")
        self.assertIn("Dharma Compass", rep1["report_markdown"])

        # 2. Master Dossier (₹570, 12 Pages)
        rep2 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_dharma_master")
        self.assertEqual(rep2["price_inr"], 570)
        self.assertEqual(rep2["page_target"], "12 Pages")
        self.assertIn("Ancestral Karma", rep2["report_markdown"])

        # 3. Sovereign (₹4,800, 32 Pages)
        rep3 = generate_package_report(self.profile["name"], self.profile["day"], self.profile["month"], self.profile["year"], "report_dharma_sovereign")
        self.assertEqual(rep3["price_inr"], 4800)
        self.assertEqual(rep3["page_target"], "32 Pages")
        self.assertIn("Karmic Destiny Architecture", rep3["report_markdown"])

    # ──────────────────────────────────────────────────────────────────────────
    # 6. API ENDPOINT & STRICT COMPLIANCE LINTER
    # ──────────────────────────────────────────────────────────────────────────
    def test_api_package_report_endpoint_flowdown(self):
        resp = self.client.post("/api/v1/readings/package-report", json={
            "name": "Bhaskr Singh",
            "day": 28, "month": 11, "year": 1981,
            "tier": "report_commerce_master"
        }, headers={"x-staging-test-bypass": "true"})
        self.assertEqual(resp.status_code, 200)
        res_json = resp.json()
        data = res_json.get("data", res_json)
        self.assertEqual(data["price_inr"], 599)
        self.assertEqual(data["domain"], "Money Flow, Business & Career Wealth")
        self.assertIn("Commercial Mastery", data["report_markdown"])

        # Strict Buzzword Linter: Zero banned marketing words
        text = data["report_markdown"]
        for pattern in BANNED_WORDS:
            self.assertFalse(bool(re.search(pattern, text, re.IGNORECASE)), f"Banned buzzword found in report: {pattern}")

if __name__ == "__main__":
    unittest.main()
