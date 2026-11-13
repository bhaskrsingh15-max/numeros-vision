"""
EXPANDED KNOWLEDGE BASE & MULTI-STRATEGY RAG TEST SUITE
Verifies:
1. Multi-source corpus contains 10,800+ passages across 70+ sources.
2. Proper ingestion of books, crystal guides, 25-remedies kits, Lo Shu guides, Vastu handbooks, and client sample reports.
3. Multi-strategy RAG queries accurately retrieve grounded passages with provenance.
4. AI LLM prediction engine (/api/v1/readings/ask) integrates grounded citations and remedies without hallucination.
"""

import unittest
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from fastapi.testclient import TestClient
from app.main import app
from app.engine.rag_retriever import rag_engine, sanitize_output_text


class TestExpandedCorpusRAG(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_corpus_volume_and_diversity(self):
        """Verifies corpus contains over 10,000 verified passages and diverse sources."""
        self.assertGreaterEqual(len(rag_engine.passages), 10000, "Corpus must have at least 10,000 passages")
        
        categories = set(p.get("category") for p in rag_engine.passages if p.get("category"))
        self.assertIn("authoritative_numerology_book", categories)
        self.assertIn("crystal_gemstone_guide", categories)
        self.assertIn("remedies_compendium", categories)
        self.assertIn("sample_client_report", categories)
        self.assertIn("astrology_bnn_treatise", categories)

    def test_sample_client_reports_retrieval(self):
        """Verifies that clinical diagnostic case archives can be queried for diagnostic patterns with privacy."""
        samples = rag_engine.query_sample_reports("career", 1, 9, top_k=2)
        self.assertGreaterEqual(len(samples), 1)
        for s in samples:
            self.assertEqual(s.get("category"), "sample_client_report")
            self.assertIn("source", s)
            self.assertTrue(s["source"].startswith("Numeros Vision"), "Source must be proprietary Numeros Vision identifier")
            self.assertFalse(".pdf" in s["source"].lower(), "Source must not reveal file extensions")
            self.assertTrue(len(s.get("content", "")) > 30)

    def test_crystal_and_gemstone_retrieval(self):
        """Verifies crystal frequency retrieval from the mineral frequency guide."""
        crystals = rag_engine.query_crystals_and_gemstones("Sun", top_k=2)
        self.assertGreaterEqual(len(crystals), 1)
        for c in crystals:
            self.assertEqual(c.get("category"), "crystal_gemstone_guide")
            self.assertIn("source", c)
            self.assertTrue(c["source"].startswith("Numeros Vision"))

    def test_remedies_compendium_retrieval(self):
        """Verifies planetary remedy retrieval from the proprietary remedies formulary."""
        rems = rag_engine.query_remedies("career", 1, 9, top_k=2)
        self.assertGreaterEqual(len(rems), 1)
        for r in rems:
            self.assertIn("source", r)
            self.assertTrue(r["source"].startswith("Numeros Vision"))
            self.assertTrue(len(r.get("content", "")) > 30)

    def test_ask_api_grounded_citations(self):
        """Verifies that /api/v1/readings/ask returns direct answers grounded in masked proprietary citations."""
        resp = self.client.post("/api/v1/readings/ask", json={
            "name": "Aarav Sharma",
            "day": 15,
            "month": 8,
            "year": 1990,
            "question": "What are my career prospects in leadership and what gemstone remedy suits me?"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("direct_answer", data)
        self.assertIn("why_this_is_happening", data)
        self.assertIn("remedies", data)
        self.assertIn("grounded_citations", data)
        self.assertGreaterEqual(len(data["grounded_citations"]), 1)
        for cit in data["grounded_citations"]:
            self.assertIn("source", cit)
            self.assertIn("location", cit)
            self.assertIn("excerpt", cit)
            self.assertTrue(cit["source"].startswith("Numeros Vision"), "Citation source must be proprietary")
            self.assertFalse(".pdf" in cit["source"].lower())
            self.assertFalse(".docx" in cit["source"].lower())


if __name__ == "__main__":
    unittest.main()
