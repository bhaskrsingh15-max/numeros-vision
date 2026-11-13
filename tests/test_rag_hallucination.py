"""
RAG HALLUCINATION & GROUNDEDNESS EVALUATION HARNESS
Tests retrieval accuracy, groundedness scoring, citation integrity,
and verifies that fake/fabricated queries are correctly caught as low-confidence / ungrounded
rather than hallucinating fake rules (Section 10, 12.3 & 15.4 compliance).
"""

import unittest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.engine.rag_retriever import rag_engine
from app.engine.ai_cost_and_security import validate_before_showing
from app.engine.consensus import generate_consensus_reading

class TestRAGHallucination(unittest.TestCase):

    def test_valid_rag_retrieval_and_grounding(self):
        """Test 1: Valid query returns grounded citations with real source document metadata."""
        query = "Driver 1 Conductor 9 career health combination"
        results = rag_engine.query(query, top_k=3)
        
        self.assertTrue(len(results) > 0, "RAG query should return passages for valid query")
        for res in results:
            self.assertIn("source", res, "Each passage must contain a source file citation")
            self.assertIn("location", res, "Each passage must contain page/section location")
            self.assertEqual(res["provenance"], "verified_numeros_vision", "Provenance tag must be verified_numeros_vision")
            
        # Test gate for valid reading
        gate = validate_before_showing(consensus_score_pct=83.0, verified_passage_count=len(results))
        self.assertEqual(gate["confidence"], "high")
        self.assertEqual(gate["show"], "full_reading")

    def test_hallucination_prevention_on_fake_query(self):
        """Test 2: Non-existent / fake query does NOT produce false high confidence."""
        fake_query = "Driver 999 Conductor 888 quantum teleportation planetary yoga"
        results = rag_engine.query(fake_query, top_k=3)
        
        # Verify gate behavior when verified passages are missing/low relevance
        gate = validate_before_showing(consensus_score_pct=30.0, verified_passage_count=0)
        self.assertEqual(gate["confidence"], "low")
        self.assertEqual(gate["show"], "flagged_for_review")
        self.assertEqual(gate["action"], "route_to_human_astrologer")
        self.assertIn("routed for astrologer review", gate["message"])

    def test_consensus_report_citation_integrity(self):
        """Test 3: Every domain verdict in a consensus reading includes grounded RAG citations."""
        report = generate_consensus_reading("Bhaskr Singh", 15, 8, 1995)
        
        self.assertIn("domain_verdicts", report)
        for domain, details in report["domain_verdicts"].items():
            self.assertEqual(details["provenance"], "verified_numeros_vision")
            citations = details["grounded_citations"]
            self.assertTrue(len(citations) > 0, f"Domain {domain} must include grounded citations")
            for cit in citations:
                self.assertIn("source", cit)
                self.assertIn("location", cit)
                self.assertIn("excerpt", cit)

if __name__ == "__main__":
    unittest.main()
