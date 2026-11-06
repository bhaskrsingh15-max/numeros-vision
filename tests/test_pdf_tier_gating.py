import io
import os
import re
import sys
import unittest
import pypdf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.services.pdf_report_generator import generate_customised_pdf_report, run_deterministic_calculation

sys.stdout.reconfigure(encoding='utf-8')

BASIC_FORBIDDEN_KEYWORDS = [
    "FREE CELESTIAL DISCOVERY BLUEPRINT",
    "FREE DISCOVERY BLUEPRINT",
    "Free Discovery Tier",
    "KARMIC MISSING DIGITS & REMEDIES (LOCKED)",
    "KARMIC MISSING NUMBERS",
    "7-LAYER CURES",
    "SACRED REMEDIES & TIMELINES LOCKED",
    "PREMIUM CHAPTER LOCKED",
    "MAHADASHA RADAR",
    "PINNACLE CYCLES",
    "ACTIVATE LUCKY CHARM DOSSIER",
    "wrong gemstones without planetary conflict",
    "Section 4: The 8 Lo Shu Planes",
    "Section 5: Karmic Missing Numbers",
    "Section 7: 7-Layer Vastu",
    "Section 11: The 81-Pair Archetype Matrix",
    "Section 13: 10-Year Macro Planetary Timing Radar",
    "Section 14: Karmic Debt Diagnosis",
    "Section 21: Family & Multi-Generational Synastry Radar",
    "Section 29: 4-Stage Pinnacle Cycles",
]

ADVANCED_FORBIDDEN_KEYWORDS = [
    "Section 3: Missing Numbers Deep Void Diagnosis",
    "Section 4: Name Balancing, Acoustic Spelling",
    "Section 11: The 81-Pair Archetype Matrix",
    "Section 12: Signature Architecture & Graphology Audit",
    "Section 12: Dual-System Synthesis",
    "Section 13: 10-Year Macro Planetary Timing Radar",
    "Section 14: Karmic Debt Diagnosis",
    "Section 15: Full Name Balancing",
    "Section 15: Rudraksha, Mantra & Spiritual Sadhana",
    "Section 16: Health, Vitality & Ayurvedic Constitution",
    "Section 17: Real Estate, Property & Vastu Blueprint",
    "Section 18: Vehicle, Travel & Global Relocation",
    "Section 19: Compatibility, Marriage & Partnership Matrix",
    "Section 20: Business Name, Brand & Corporate Alignment",
    "Section 21: Family & Multi-Generational Synastry Radar",
    "Section 22: Wealth Compounding & Investment Corridors",
    "Section 29: 4-Stage Pinnacle Cycles",
]


class TestPdfTierGating(unittest.TestCase):
    def test_basic_tier_3_pages_and_zero_locked_leakage(self):
        pdf_bytes, meta = generate_customised_pdf_report(
            name="Aaditya Sharma",
            day=15,
            month=8,
            year=1990,
            tier="basic"
        )
        self.assertGreater(len(pdf_bytes), 10000, "PDF bytes should be non-empty")

        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        print(f"[PDF Tier Test] report_basic (Basic Report): {len(reader.pages)} pages")
        self.assertEqual(len(reader.pages), 3, f"Basic tier must be exactly 3 pages, got {len(reader.pages)}")

        full_text = "\n".join(page.extract_text() for page in reader.pages)
        norm_text = re.sub(r"\s+", " ", full_text)

        # 1. Must include renamed Basic heading & canonical pack name "Basic Report"
        self.assertIn("ELEMENT BALANCING & FOUNDATIONAL BLUEPRINT", norm_text)
        self.assertIn("Basic Report", norm_text)
        self.assertIn("33/6", norm_text)
        self.assertIn("Lo Shu Grid", norm_text)
        self.assertIn("8 ELEMENTAL PLANES", norm_text)
        self.assertIn("5-ELEMENT BALANCING ACTIONS", norm_text)

        # 2. Must NEVER include locked section headings or forbidden teaser copy
        for kw in BASIC_FORBIDDEN_KEYWORDS:
            self.assertNotIn(
                kw.lower(),
                norm_text.lower(),
                f"LOCKED CONTENT LEAK: Found locked keyword '{kw}' in Basic 3-Page PDF!"
            )

    def test_basic_page2_planes_and_raj_yogas_computed_from_grid(self):
        """
        DOB 10-08-1990 has digits {1, 8, 9} and lacks digits {2, 3, 4, 5, 6, 7}
        (specifically lacking 2, 3, 4, 6, and 7).
        Verify that on Page 2:
        - Missing numbers include [2, 3, 4, 6, 7]
        - Emotional Plane (3-5-7), Action Plane (2-7-6), and Golden Raj Yoga (4-5-6) are INACTIVE
        - Mental (4-9-2), Practical (8-1-6), Thought (4-3-8), Will (9-5-1), and Silver Earth Yoga (2-5-8) are PARTIAL
        - NONE of the 8 planes or Raj Yogas show as COMPLETE.
        """
        calc = run_deterministic_calculation("Aaditya Sharma", 10, 8, 1990, tier="basic")
        for missing_digit in [2, 3, 4, 6, 7]:
            self.assertIn(missing_digit, calc["missing_numbers"])

        pdf_bytes, meta = generate_customised_pdf_report(
            name="Aaditya Sharma",
            day=10,
            month=8,
            year=1990,
            tier="basic"
        )
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        page2_text = reader.pages[1].extract_text()
        norm_p2 = re.sub(r"\s+", " ", page2_text)

        self.assertNotIn("COMPLETE", norm_p2, "No plane or Raj Yoga can be COMPLETE for DOB 10-08-1990!")
        self.assertIn("Mental Plane 4 - 9 - 2 PARTIAL", norm_p2)
        self.assertIn("Emotional Plane 3 - 5 - 7 INACTIVE", norm_p2)
        self.assertIn("Practical Plane 8 - 1 - 6 PARTIAL", norm_p2)
        self.assertIn("Thought Plane 4 - 3 - 8 PARTIAL", norm_p2)
        self.assertIn("Will Plane 9 - 5 - 1 PARTIAL", norm_p2)
        self.assertIn("Action Plane 2 - 7 - 6 INACTIVE", norm_p2)
        self.assertIn("Golden Raj Yoga 4 - 5 - 6 INACTIVE", norm_p2)
        self.assertIn("Silver Earth Yoga 2 - 5 - 8 PARTIAL", norm_p2)

    def test_advanced_tier_12_pages_and_zero_premium_leakage(self):
        pdf_bytes, meta = generate_customised_pdf_report(
            name="Aaditya Sharma",
            day=15,
            month=8,
            year=1990,
            tier="advanced"
        )
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        print(f"[PDF Tier Test] report_advanced (Advanced Master Dossier): {len(reader.pages)} pages")
        self.assertEqual(len(reader.pages), 12, f"Advanced tier must be exactly 12 pages, got {len(reader.pages)}")

        full_text = "\n".join(page.extract_text() for page in reader.pages)
        norm_text = re.sub(r"\s+", " ", full_text)

        # 1. Must include Advanced deliverables
        self.assertIn("Lo Shu", norm_text)
        self.assertIn("Executive Summary", norm_text)

        # 2. Must NEVER include Premium-only chapters (Sections 11 to 30)
        for kw in ADVANCED_FORBIDDEN_KEYWORDS:
            self.assertNotIn(
                kw.lower(),
                norm_text.lower(),
                f"PREMIUM LEAK: Found Premium keyword '{kw}' in Advanced 12-Page PDF!"
            )

    def test_advanced_tier_present_numbers_benefic_vs_malefic_matrix(self):
        pdf_bytes, meta = generate_customised_pdf_report(
            name="Aaditya Sharma",
            day=15,
            month=8,
            year=1990,
            tier="advanced",
            topic_id="present_numbers"
        )
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        self.assertEqual(len(reader.pages), 12, "Advanced present numbers dossier must be exactly 12 pages.")
        full_text = "\n".join(page.extract_text() for page in reader.pages)
        self.assertIn("Benefic vs Malefic", full_text, "12-page Present Numbers report must contain Benefic vs Malefic Planetary Operating Matrix.")

    def test_premium_tier_32_pages_full_dossier(self):
        pdf_bytes, meta = generate_customised_pdf_report(
            name="Aaditya Sharma",
            day=15,
            month=8,
            year=1990,
            tier="premium"
        )
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        print(f"[PDF Tier Test] report_premium (Premium Sovereign Blueprint): {len(reader.pages)} pages")
        self.assertEqual(len(reader.pages), 32, f"Premium tier must be exactly 32 pages, got {len(reader.pages)}")

        full_text = "\n".join(page.extract_text() for page in reader.pages)
        norm_text = re.sub(r"\s+", " ", full_text)
        self.assertIn("Section 13: 10-Year Macro Planetary Timing Radar", norm_text)
        self.assertIn("Section 29: 4-Stage Pinnacle Cycles", norm_text)


if __name__ == '__main__':
    unittest.main()
