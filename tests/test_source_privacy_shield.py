"""
NUMEROS VISION — SOURCE PRIVACY & IP LOCKDOWN VERIFICATION SUITE
Verifies:
1. Zero source names, book titles, author names, or file extensions exposed in API outputs.
2. Zero personal client names or case report identities exposed in RAG citations or text.
3. All citations and grounded sources are 100% transformed into proprietary Numeros Vision Vault identities.
4. Copy linter flags and redacts any training leaks or client identifiers.
5. The full 10,826-passage corpus contains zero raw .pdf, author, or client references.
"""

import unittest
import sys
import os
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from app.main import app
from app.engine.source_privacy_shield import (
    mask_source_name,
    sanitize_location,
    sanitize_text,
    sanitize_citation,
    SOURCE_PROPRIETARY_MAPPING,
)
from app.engine.rag_retriever import rag_engine
from app.engine.consensus import generate_consensus_reading
from app.engine.claim_validator import lint_copy


class TestSourcePrivacyShield(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_source_mapping_covers_treatises_and_reports(self):
        """Verifies that all raw documents and client reports map to prestigious Numeros Vision titles."""
        test_cases = [
            ("numerology Numeros Vision Classical Methodology .pdf", "Numeros Vision Hermetic Core Archive (NV-HCA-01)"),
            ("Bhaskr_Singh_numerology.pdf", "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-01)"),
            ("Ummika_Singh_numerology.pdf", "Numeros Vision Clinical Diagnostic Archive (Case Reference NV-CDA-03)"),
            ("25 astrological remedies all in one  (1)_compressed.pdf", "Numeros Vision Planetary Harmonization & Remedy Protocols (NV-PHRP-29A)"),
            ("Cheiros_Book_of_Numbers_Study_Notes.docx", "Numeros Vision Chaldean Mathematical Notes (NV-CMN-07B)"),
            ("THE BOOK OF NAKSHATRAS.pdf", "Numeros Vision Stellar Constellation Resonance Canon (NV-SCRC-08)"),
            ("Unknown_Random_Textbook.pdf", "Numeros Vision Sovereign Archive (NV-VAULT-"),
        ]
        for raw, expected_prefix in test_cases:
            masked = mask_source_name(raw)
            self.assertTrue(masked.startswith(expected_prefix) or expected_prefix in masked, f"Failed for {raw}: got {masked}")
            self.assertFalse(".pdf" in masked.lower(), f"Raw extension leaked in {masked}")
            self.assertFalse(".docx" in masked.lower(), f"Raw extension leaked in {masked}")
            self.assertFalse("chaitanya" in masked.lower(), f"Author leaked in {masked}")
            self.assertFalse("bhaskr" in masked.lower(), f"Client leaked in {masked}")

    def test_text_sanitizer_scrubs_pii_and_authors(self):
        """Verifies that sanitize_text redacts personal client names and authors."""
        leaky_text = (
            "Client Bhaskr Singh consulted on 28-11-1981 with Numeros Vision Classical Methodology and Classical Vedic Tradition. "
            "Ummika Singh and Kaashvi Singh were present along with Ankur Sachdeva. "
            "Contact: user@gmail.com, phone 9811223344. Reference: numerology Numeros Vision Classical Methodology .pdf"
        )
        cleaned = sanitize_text(leaky_text)
        self.assertNotIn("Bhaskr", cleaned)
        self.assertNotIn("Chaitanya", cleaned)
        self.assertNotIn("Missra", cleaned)
        self.assertNotIn("Johari", cleaned)
        self.assertNotIn("Ummika", cleaned)
        self.assertNotIn("Kaashvi", cleaned)
        self.assertNotIn("Sachdeva", cleaned)
        self.assertNotIn(".pdf", cleaned)
        self.assertNotIn("user@gmail.com", cleaned)
        self.assertNotIn("9811223344", cleaned)

    def test_corpus_contains_zero_raw_leaks(self):
        """Scans all passages in the active corpus to ensure zero leaks in source or content."""
        leak_pattern = re.compile(r'(\.pdf|\.docx|\.xlsx|bhaskr|ummika|kaashvi|sachdeva|shally|chaitanya|Classical Vedic Tradition|Classical Astrological Framework)', re.I)
        
        for idx, p in enumerate(rag_engine.passages):
            src = p.get("source", "")
            cnt = p.get("content", "")
            
            # Check source field
            m_src = leak_pattern.search(src)
            self.assertIsNone(m_src, f"Passage {idx} source leaked: {src}")
            self.assertTrue(src.startswith("Numeros Vision"), f"Passage {idx} source not proprietary: {src}")

            # Check content field
            m_cnt = leak_pattern.search(cnt)
            self.assertIsNone(m_cnt, f"Passage {idx} content leaked sensitive entity: {cnt[:80]}")

    def test_ask_api_zero_leakage_and_proprietary_branding(self):
        """Verifies that /api/v1/readings/ask returns completely masked proprietary citations."""
        resp = self.client.post("/api/v1/readings/ask", json={
            "name": "Dev Sharma",
            "day": 1,
            "month": 1,
            "year": 1990,
            "question": "What is my career forecast in technology leadership?"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()

        # Check why_this_is_happening
        why = data.get("why_this_is_happening", {})
        grounded_src = why.get("grounded_source", "")
        self.assertTrue("Numeros Vision" in grounded_src, f"Grounded source not branded: {grounded_src}")
        self.assertNotIn(".pdf", grounded_src)
        self.assertNotIn("Chaitanya", grounded_src)

        # Check remedies
        for r in data.get("remedies", []):
            title = r.get("title", "")
            self.assertNotIn(".pdf", title)
            self.assertNotIn("25 astrological remedies", title.lower())

        # Check grounded_citations
        citations = data.get("grounded_citations", [])
        self.assertGreaterEqual(len(citations), 1)
        for cit in citations:
            src = cit.get("source", "")
            loc = cit.get("location", "")
            exc = cit.get("excerpt", "")

            self.assertTrue(src.startswith("Numeros Vision"), f"Citation source not proprietary: {src}")
            self.assertNotIn(".pdf", src)
            self.assertNotIn(".docx", src)
            self.assertNotIn(".pdf", loc)
            self.assertNotIn("Bhaskr", exc)
            self.assertNotIn("Chaitanya", exc)

    def test_consensus_reading_zero_leakage(self):
        """Verifies consensus reading citations are fully proprietary."""
        reading = generate_consensus_reading("Test Subject", 10, 5, 1992)
        self.assertIn("domain_verdicts", reading)
        for domain, verdict in reading["domain_verdicts"].items():
            for cit in verdict.get("grounded_citations", []):
                self.assertTrue(cit["source"].startswith("Numeros Vision"))
                self.assertNotIn(".pdf", cit["source"])
                self.assertNotIn(".docx", cit["source"])
                self.assertNotIn("Bhaskr", cit["excerpt"])

    def test_copy_linter_blocks_source_and_client_leaks(self):
        """Verifies that the automated copy linter catches and redacts training source leaks."""
        bad_text = "As stated in Cheiro's Book of Numbers and Numeros Vision Classical Methodology study notes for Bhaskr Singh."
        res = lint_copy(bad_text)
        self.assertFalse(res.is_valid, "Copy linter should reject text with source leaks")
        self.assertGreaterEqual(len(res.privacy_leaks_found), 1)
        self.assertNotIn("Bhaskr", res.remediated_text)
        self.assertNotIn("Chaitanya", res.remediated_text)


if __name__ == "__main__":
    unittest.main()
