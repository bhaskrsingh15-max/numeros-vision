"""
Test Suite: AnswerThePublic 30-Day SEO Content Roadmap and Route Verification
"""
import sys
import os
import unittest
import re

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app

class TestAnswerThePublicSEORoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        cls.banned_words = ["unlock", "elevate", "game-changer", "revolutionary", "seamless"]
        cls.routes_to_verify = [
            ("/", "Anveil Every Charm", "Day 1: Baseline & Home Portal"),
            ("/guides/numerology-guide/", "What Is Numerology", "Day 2: What is Numerology Guide"),
            ("/calculators/", "Explore Numerology Calculators", "Day 3: Calculator Hub"),
            ("/calculators/name-numerology/", "Name Numerology", "Day 4: Name Numerology Calculator"),
            ("/guides/how-to-calculate-name-numerology/", "How to Calculate Name Numerology", "Day 5: Name Calculation Guide"),
            ("/guides/numerology-alphabet-chart/", "Numerology Alphabet Chart", "Day 6: Alphabet Chart Reference"),
            ("/guides/chaldean-numerology/", "Chaldean Numerology Explained", "Day 7: Chaldean Numerology Guide"),
            ("/guides/chaldean-vs-pythagorean-numerology/", "Chaldean vs. Pythagorean", "Day 8: Chaldean vs Pythagorean"),
            ("/guides/numerology-number-meanings/", "Numerology Number Meanings", "Day 9: Number Meanings Pillar"),
            ("/guides/numerology-number-1/", "Number 1 Meaning in Numerology", "Day 10: Number 1 Meaning"),
            ("/guides/numerology-number-2/", "Number 2 Meaning in Numerology", "Day 11: Number 2 Meaning"),
            ("/guides/numerology-number-3/", "Number 3 Meaning in Numerology", "Day 12: Number 3 Meaning"),
            ("/guides/numerology-number-4/", "Number 4 Meaning in Numerology", "Day 13: Number 4 Meaning"),
            ("/guides/numerology-number-5/", "Number 5 Meaning in Numerology", "Day 14: Number 5 Meaning"),
            ("/guides/numerology-number-6/", "Number 6 Meaning in Numerology", "Day 15: Number 6 Meaning"),
            ("/guides/numerology-number-7/", "Number 7 Meaning in Numerology", "Day 16: Number 7 Meaning"),
            ("/guides/numerology-number-8/", "Number 8 Meaning in Numerology", "Day 17: Number 8 Meaning"),
            ("/guides/numerology-number-9/", "Number 9 Meaning in Numerology", "Day 18: Number 9 Meaning"),
            ("/guides/master-numbers-in-numerology/", "Master Numbers", "Day 18b: Master Numbers 11, 22, 33"),
            ("/calculators/life-path-number/", "Life Path Calculator", "Day 19: Life Path Calculator"),
            ("/guides/life-path-and-birth-numbers/", "Life Path", "Day 20: Life Path & Birth Numbers Guide"),
            ("/calculators/lo-shu-grid/", "Lo Shu Grid", "Day 21: Lo Shu Grid Tool"),
            ("/calculators/numerology-compatibility/", "Compatibility Calculator", "Day 22: Compatibility Calculator"),
            ("/calculators/business-name-numerology/", "Name Balancing", "Day 23: Business Name Numerology Tool"),
            ("/calculators/mobile-number-numerology/", "Mobile Number Numerology", "Day 24: Mobile Numerology Tool"),
            ("/guides/house-number-numerology/", "Property Numerology", "Day 25: House Number Numerology"),
            ("/calculators/personal-year-numerology/", "Blessing Years", "Day 26: Personal Year Tool"),
            ("/guides/name-vs-date-of-birth-numerology/", "Name vs. Date-of-Birth Numerology", "Day 27: Name vs DOB Guide"),
            ("/sample-report/", "Celestial Master Blueprint", "Day 28: Sample Report"),
            ("/methodology/", "How Numeros Vision Calculates and Explains Numbers", "Day 29: Methodology"),
            ("/faq/", "Frequently Asked Questions", "Day 30: FAQ Hub")
        ]

    def test_all_answerthepublic_seo_routes(self):
        """Verify all 31 AnswerThePublic 30-day roadmap routes return 200 and contain no banned words."""
        for path, expected_text, desc in self.routes_to_verify:
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200, f"Route {path} returned status {resp.status_code}")
            cont = resp.text
            self.assertIn(expected_text, cont, f"Expected '{expected_text}' in {path} ({desc})")
            for b in self.banned_words:
                self.assertIsNone(
                    re.search(r'\b' + re.escape(b) + r'\b', cont, re.IGNORECASE),
                    f"Banned word '{b}' found in {path}"
                )

if __name__ == "__main__":
    unittest.main()
