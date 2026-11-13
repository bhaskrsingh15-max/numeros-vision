"""
COMPREHENSIVE ZERO-COST AUTOMATED TEST SUITE
Runs unit and integration tests across all 8 prediction engines, security middleware,
RAG retriever, cache service, PII anonymizer, and B2B enterprise routes.
"""

import unittest
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

from app.engine.lo_shu import analyze_lo_shu_grid
from app.engine.vedic_numerology import analyze_vedic_numerology
from phase4_bnn_engine import run_full_bnn_analysis
from phase5_lal_kitab_engine import run_full_lal_kitab_analysis
from phase7_kp_engine import analyze_kp_sub_lord
from phase8_btr_engine import run_full_btr_analysis, mahadasha_periods
from orchestrator import handle_question, classify_topic
from app.engine.rag_retriever import rag_engine
from app.engine.cache_service import calculation_cache
from app.security.anonymizer import anonymize_user_profile
from app.security.cyber_defense import is_malicious_payload
from app.engine.zero_cost_llm import synthesize_zero_cost_narrative

class TestPredictionEngineSuite(unittest.TestCase):

    def test_vedic_numerology(self):
        res = analyze_vedic_numerology(15, 8, 1995)
        self.assertEqual(res["driver_number"], 6)
        self.assertEqual(res["conductor_number"], 2)

    def test_lo_shu_grid(self):
        res = analyze_lo_shu_grid(15, 8, 1995)
        self.assertIn(1, res["present_numbers"])
        self.assertIn(3, res["missing_numbers"])

    def test_bnn_engine(self):
        chart = {
            "Sun": {"sign": "Scorpio", "degree": 12.0},
            "Jupiter": {"sign": "Cancer", "degree": 15.0}  # Trine to Scorpio (Moksha trine)
        }
        bnn_res = run_full_bnn_analysis(chart, current_age=30)
        self.assertEqual(bnn_res["engine"], "Bhrigu Nandi Nadi (BNN)")
        self.assertTrue(len(bnn_res["active_combinations"]) > 0)

    def test_lal_kitab_engine(self):
        chart = {"Sun": {"house": 1}, "Moon": {"house": 5}}
        lk_res = run_full_lal_kitab_analysis(chart)
        self.assertEqual(lk_res["engine"], "Lal Kitab Engine")

    def test_kp_engine(self):
        kp_res = analyze_kp_sub_lord(242.39)  # Sagittarius 2.39 deg
        self.assertEqual(kp_res["nakshatra"], "Mula")
        self.assertEqual(kp_res["star_lord"], "Ketu")

    def test_btr_engine(self):
        mahadashas = mahadasha_periods("Ketu", 1990.0)
        candidates = [{"label": "12:00 PM", "mahadasha_list": mahadashas}]
        events = [{"type": "job", "year": 2015.0}]
        btr_res = run_full_btr_analysis(candidates, events)
        self.assertEqual(btr_res["rectified_time"], "12:00 PM")

    def test_orchestrator(self):
        topic = classify_topic("mera career aur job kaisa rahega")
        self.assertEqual(topic, "career")

    def test_rag_retriever(self):
        passages = rag_engine.query("career job success", top_k=2)
        self.assertTrue(len(passages) > 0)

    def test_cache_service(self):
        calculation_cache.set(15, 8, 1995, {"result": "success"})
        cached = calculation_cache.get(15, 8, 1995)
        self.assertEqual(cached["result"], "success")

    def test_pii_anonymizer(self):
        anon = anonymize_user_profile("Bhaskr Singh", 15, 8, 1995)
        self.assertIn("anon_name_hash", anon)
        self.assertEqual(len(anon["anon_name_hash"]), 64)

    def test_cyber_defense_waf(self):
        self.assertTrue(is_malicious_payload("http://example.com/?id=1' UNION SELECT NULL--"))
        self.assertFalse(is_malicious_payload("http://example.com/?query=career"))

    def test_zero_cost_narrative(self):
        dummy_consensus = {
            "user_name": "Test User",
            "overall_consensus_strength_pct": 80.0,
            "vedic_numerology": {"driver_number": 1, "driver_planet": "Sun", "conductor_number": 9, "conductor_planet": "Mars"},
            "lo_shu_grid": {"completed_planes": ["Will Plane (9-5-1)"], "missing_numbers": [2, 3]}
        }
    def test_sample_report_endpoint(self):
        from fastapi.testclient import TestClient
        from app.main import app
        client = TestClient(app)
        res = client.get("/sample")
        self.assertEqual(res.status_code, 200)
        self.assertIn("Celestial Master Blueprint", res.text)
        self.assertIn("ANVEIL EVERY CHARM", res.text)
        self.assertIn("page-watermark", res.text)

        res2 = client.get("/report")
        self.assertEqual(res2.status_code, 200)

    def test_rag_corpus_market_correlation(self):
        self.assertGreaterEqual(len(rag_engine.passages), 2140)
        hits = rag_engine.query("Lo Shu Missing Number 1 Protocol", top_k=3)
        self.assertTrue(len(hits) > 0)
        self.assertTrue(any("Numeros Vision Empirical Benchmark" in h.get("source", "") or "Market Correlation Engine" in h.get("source", "") for h in hits))

if __name__ == "__main__":
    unittest.main()
