import unittest
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.engine.source_privacy_shield import (
    mask_source_name,
    sanitize_location,
    sanitize_text,
    sanitize_citation,
)
from app.engine.rag_retriever import rag_engine
from app.engine.claim_validator import lint_copy

class TestPurePrivacyShield(unittest.TestCase):
    def test_source_mapping_covers_treatises_and_reports(self):
        test_cases = [
            ("numerology Numeros Vision Classical Methodology .pdf", "Numeros Vision Hermetic Core Archive (NV-HCA-01)"),
            ("25 astrological remedies all in one  (1)_compressed.pdf", "Numeros Vision Planetary Harmonization & Remedy Protocols (NV-PHRP-29A)"),
            ("Cheiros_Book_of_Numbers_Study_Notes.docx", "Numeros Vision Chaldean Mathematical Notes (NV-CMN-07B)"),
            ("THE BOOK OF NAKSHATRAS.pdf", "Numeros Vision Stellar Constellation Resonance Canon (NV-SCRC-08)"),
            ("You and Your Name (Know Your Fortune Through Your Name) 2005 PDF Yoga Mantra.pdf", "Numeros Vision Classical Sound and Name Compendium (NV-CSNC-43)"),
            ("nadi-astrology-accurate-predictive-methodology-2013nbsped_compress.pdf", "Numeros Vision Classical Nadi Event System (NV-CNES-50)"),
        ]
        for raw, expected_prefix in test_cases:
            masked = mask_source_name(raw)
            self.assertTrue(masked.startswith(expected_prefix) or expected_prefix in masked, f"Failed for {raw}: got {masked}")
            self.assertFalse(".pdf" in masked.lower(), f"Raw extension leaked in {masked}")

    def test_text_sanitizer_scrubs_pii_and_authors(self):
        leaky_text = (
            "Client Bhaskr Singh consulted on 28-11-1981 with Umang Taneja and Gautam Verma. "
            "Ummika Singh and Kaashvi Singh were present. "
            "Author Harish Johari and Dr. Chaitanyaa Misra and Linda Goodman and Matthew Oliver Goodwin. "
            "Also Cheiro's Book of Numbers and Accurate Predictive Methodology. "
            "Contact: user@gmail.com, phone 9811223344. Reference: test.pdf"
        )
        cleaned = sanitize_text(leaky_text)
        self.assertNotIn("Bhaskr", cleaned)
        self.assertNotIn("Chaitanya", cleaned)
        self.assertNotIn("Misra", cleaned)
        self.assertNotIn("Johari", cleaned)
        self.assertNotIn("Taneja", cleaned)
        self.assertNotIn("Gautam Verma", cleaned)
        self.assertNotIn("Goodman", cleaned)
        self.assertNotIn("Goodwin", cleaned)
        self.assertNotIn("Cheiro", cleaned)
        self.assertNotIn("Accurate Predictive Methodology", cleaned)
        self.assertNotIn(".pdf", cleaned)
        self.assertNotIn("user@gmail.com", cleaned)
        self.assertNotIn("9811223344", cleaned)
        print("Sanitized text output:", cleaned[:120], "...")

    def test_corpus_contains_zero_raw_leaks(self):
        import re
        leak_pattern = re.compile(r'(\.pdf|\.docx|\.xlsx|bhaskr|ummika|kaashvi|sachdeva|shally|chaitanya|taneja|gautam verma)', re.I)
        for idx, p in enumerate(rag_engine.passages):
            src = p.get("source", "")
            cnt = p.get("content", "")
            m_src = leak_pattern.search(src)
            self.assertIsNone(m_src, f"Passage {idx} source leaked: {src}")
            self.assertTrue(src.startswith("Numeros Vision"), f"Passage {idx} source not proprietary: {src}")

if __name__ == "__main__":
    unittest.main()
