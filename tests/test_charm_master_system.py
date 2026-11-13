"""
tests/test_charm_master_system.py
==================================
Comprehensive Automated Test Suite for Numeros Vision Charm AI
Master Implementation Specification v2.0.

Tests:
1. Deterministic Numerology Dasha Hierarchy (Mahadasha, Antardasha, Pratyantardasha, Personal Year/Month/Day)
2. Chart Fact Provider & Ephemeris Verification
3. Independent Method Adapters (KP, Vedic, BNN, and Lal Kitab Disabled Gate)
4. Deterministic Consensus Engine (Dual-Axis Verification, Immutable Primary Window)
5. RAG Source Governor & Partitioned Knowledge Isolation
6. Governed Remedies & Practical Alignment Service
7. Outcome Tracking & Thread-Safe Snapshotting
8. REST API Endpoints (POST /api/charm/chat, GET /api/charm/predictions/{id}/evidence, POST /api/charm/outcomes)
"""

import unittest
from datetime import date
from fastapi.testclient import TestClient

from app.main import app
from app.charm.numerology.dasha_engine import numerology_dasha_engine
from app.charm.charts.fact_provider import planetary_fact_provider
from app.charm.methods.kp_adapter import kp_adapter
from app.charm.methods.vedic_adapter import vedic_adapter
from app.charm.methods.bnn_adapter import bnn_adapter
from app.charm.methods.lal_kitab_adapter import lal_kitab_adapter
from app.charm.consensus.engine import consensus_engine
from app.charm.rag.source_governor import source_governor
from app.charm.remedies.remedy_service import remedy_service, SAFE_CRYSTAL_CATALOGUE
from app.charm.outcomes.outcome_service import outcome_service, PredictionSnapshot

class TestCharmMasterSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # ─────────────────────────────────────────────────────────────────────────
    # 1. NUMEROLOGY DASHA HIERARCHY TESTS
    # ─────────────────────────────────────────────────────────────────────────
    def test_dasha_hierarchy_exact_dates_and_trace(self):
        """Verify Mahadasha, Antardasha, and Pratyantardasha exact date bounds and calculation trace."""
        timeline = numerology_dasha_engine.evaluate_dasha_hierarchy(
            day=15,
            month=8,
            year=1990,
            target_date=2026,
            event_definition_id="career_growth"
        )
        self.assertEqual(timeline.driver, 6)
        self.assertEqual(timeline.conductor, 6)
        self.assertEqual(timeline.personal_year, 6)

        # Check periods contain MAHADASHA, ANTARDASHA, and PRATYANTARDASHA
        levels = set(p.level for p in timeline.periods)
        self.assertIn("MAHADASHA", levels)
        self.assertIn("ANTARDASHA", levels)
        self.assertIn("PRATYANTARDASHA", levels)

        # Check rule trace
        self.assertGreater(len(timeline.rule_trace), 0)

        # Check primary windows
        self.assertGreaterEqual(len(timeline.primary_windows), 2)
        acute_win = timeline.primary_windows[0]
        self.assertEqual(acute_win.granularity, "MONTH")
        self.assertTrue(acute_win.start <= acute_win.end)
        self.assertIn("Pratyantardasha", acute_win.label)

    # ─────────────────────────────────────────────────────────────────────────
    # 2. CHART FACTS & TOPOCENTRIC EPHEMERIS
    # ─────────────────────────────────────────────────────────────────────────
    def test_chart_fact_provider_coordinates_and_transits(self):
        """Verify topocentric city coordinates and 2026 planetary transit facts."""
        facts = planetary_fact_provider.get_chart_facts(
            target_date=date(2026, 8, 15),
            city="delhi"
        )
        self.assertAlmostEqual(facts.latitude, 28.6139, places=2)
        self.assertAlmostEqual(facts.longitude, 77.2090, places=2)
        self.assertIn("Jupiter", facts.planetary_positions)
        self.assertIn("Saturn", facts.planetary_positions)
        self.assertIn("saturn_in_pisces", facts.transit_vectors)

    # ─────────────────────────────────────────────────────────────────────────
    # 3. INDEPENDENT METHOD ADAPTERS
    # ─────────────────────────────────────────────────────────────────────────
    def test_kp_adapter_significators(self):
        """Verify KP method evaluates 10th Cuspal Sub-Lord and returns structured evaluation."""
        profile = {"driver": 6, "conductor": 6, "day": 15, "month": 8, "year": 1990}
        chart = {"house_significators": {"10": ["Surya", "Guru"]}}
        res = kp_adapter.evaluate({"event_definition_id": "career_growth"}, profile, chart)
        self.assertEqual(res.method_id, "KP_ASTROLOGY")
        self.assertIn(res.assessment, ["SUPPORTS", "MIXED", "CHALLENGES"])
        self.assertGreater(len(res.rule_evidence), 0)

    def test_vedic_adapter_transits(self):
        """Verify Vedic Parashari evaluates Gochar and Sambandha."""
        profile = {"driver": 6, "conductor": 6, "day": 15, "month": 8, "year": 1990}
        chart = {"planetary_transits": {"Guru": "Vrishabha (Taurus)", "Shani": "Kumbha (Aquarius)"}}
        res = vedic_adapter.evaluate({"event_definition_id": "career_growth"}, profile, chart)
        self.assertEqual(res.method_id, "VEDIC_ASTROLOGY")
        self.assertIn(res.assessment, ["SUPPORTS", "MIXED", "CHALLENGES"])

    def test_bnn_adapter_karaka(self):
        """Verify BNN method evaluates Jeeva and Karma Karakas."""
        profile = {"driver": 6, "conductor": 6, "day": 15, "month": 8, "year": 1990, "name": "Seeker"}
        res = bnn_adapter.evaluate({"event_definition_id": "career_growth"}, profile, {})
        self.assertEqual(res.method_id, "BNN_NADI")
        self.assertIn(res.assessment, ["SUPPORTS", "MIXED", "CHALLENGES"])

    def test_lal_kitab_adapter_disabled_gate(self):
        """Verify Lal Kitab adapter remains strictly DISABLED and NOT_EVALUATED per release gate."""
        profile = {"driver": 6, "conductor": 6}
        res = lal_kitab_adapter.evaluate({"event_definition_id": "career_growth"}, profile, {})
        self.assertEqual(res.method_id, "LAL_KITAB")
        self.assertEqual(res.assessment, "NOT_EVALUATED")
        self.assertEqual(res.status, "DISABLED")
        self.assertGreater(len(res.limitations), 0)

    # ─────────────────────────────────────────────────────────────────────────
    # 4. DETERMINISTIC CONSENSUS ENGINE
    # ─────────────────────────────────────────────────────────────────────────
    def test_consensus_engine_dual_axis_and_immutable_primary_window(self):
        """Verify consensus dual axis and invariant: primary window is never altered by astrology."""
        timeline = numerology_dasha_engine.evaluate_dasha_hierarchy(15, 8, 1990, 2026, "career_growth")
        orig_windows = timeline.primary_windows
        
        eval_kp = kp_adapter.evaluate({"event_definition_id": "career_growth"}, {"driver": 6, "conductor": 6, "day": 15, "month": 8, "year": 1990}, {})
        eval_vedic = vedic_adapter.evaluate({"event_definition_id": "career_growth"}, {"driver": 6, "conductor": 6, "day": 15, "month": 8, "year": 1990}, {})
        eval_bnn = bnn_adapter.evaluate({"event_definition_id": "career_growth"}, {"driver": 6, "conductor": 6, "day": 15, "month": 8, "year": 1990}, {})
        eval_lk = lal_kitab_adapter.evaluate({"event_definition_id": "career_growth"}, {"driver": 6, "conductor": 6}, {})

        result = consensus_engine.derive_consensus(
            primary_numerology=timeline,
            evaluations=[eval_kp, eval_vedic, eval_bnn, eval_lk],
            event_definition={"event_definition_id": "career_growth"}
        )

        # Primary window immutability check (Section 6.1)
        self.assertEqual(result.primary_windows, orig_windows)
        self.assertEqual(result.primary_windows[0].start, orig_windows[0].start)
        self.assertEqual(result.primary_windows[0].end, orig_windows[0].end)

        # Consensus badge check
        self.assertIn(result.verification_status, [
            "NUMEROLOGY_PRIMARY_CORROBORATED",
            "NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED",
            "NUMEROLOGY_PRIMARY_CONFLICTED",
            "NUMEROLOGY_ONLY"
        ])
        self.assertIn(result.event_assessment, ["FAVOURABLE", "MIXED", "UNFAVOURABLE", "NEUTRAL"])

    # ─────────────────────────────────────────────────────────────────────────
    # 5. SOURCE GOVERNOR & RAG RETRIEVAL
    # ─────────────────────────────────────────────────────────────────────────
    def test_source_governor_partitioned_retrieval(self):
        """Verify method-partitioned retrieval isolates citations and prevents cross-method bleeding."""
        kp_citations = source_governor.retrieve_method_evidence("KP_ASTROLOGY", "10th cuspal sub lord", "career")
        self.assertGreater(len(kp_citations), 0)
        for cit in kp_citations:
            self.assertIn("SRC-NV", cit["source_id"])

        vedic_citations = source_governor.retrieve_method_evidence("VEDIC_ASTROLOGY", "Brihat Parashara", "career")
        self.assertGreater(len(vedic_citations), 0)
        for cit in vedic_citations:
            self.assertIn("SRC-NV", cit["source_id"])

    # ─────────────────────────────────────────────────────────────────────────
    # 6. GOVERNED REMEDIES & STATUTORY COMPLIANCE
    # ─────────────────────────────────────────────────────────────────────────
    def test_remedies_practical_first_and_safe_crystals(self):
        """Verify practical action is first, crystal excludes enemy stones, and yantra is configured."""
        # Driver 1 (Sun): Must NOT recommend Blue Sapphire (Saturn enemy)
        remedies = remedy_service.get_governed_remedies(
            event_family="career",
            driver=1,
            conductor=1,
            event_assessment="FAVOURABLE"
        )
        self.assertGreaterEqual(len(remedies), 3)

        # Item 1: Practical Action
        self.assertEqual(remedies[0].category, "PRACTICAL_ACTION")
        self.assertEqual(remedies[0].cost_level, "FREE")

        # Item 2: Vibrational Crystal
        crystal_remedy = remedies[1]
        self.assertEqual(crystal_remedy.category, "VIBRATIONAL_CRYSTAL")
        self.assertNotIn("Blue Sapphire", crystal_remedy.title)
        self.assertIn("Avoid clashing stones", crystal_remedy.description)

        # Compliance safety check
        compliance_notes = " ".join([note for r in remedies for note in r.safety_notes])
        self.assertIn("Drugs and Magic Remedies Act 1954", compliance_notes)

    # ─────────────────────────────────────────────────────────────────────────
    # 7. OUTCOME TRACKING & SNAPSHOTTING
    # ─────────────────────────────────────────────────────────────────────────
    def test_outcome_service_snapshot_and_recording(self):
        """Verify outcome recording attaches to immutable snapshot without modifying prediction."""
        timeline = numerology_dasha_engine.evaluate_dasha_hierarchy(15, 8, 1990, 2026, "career_growth")
        
        snap = PredictionSnapshot(
            prediction_id="TEST-PRED-SNAP-001",
            user_id="test_user_arjun",
            created_at="2026-10-21T12:00:00Z",
            event_definition_id="career_growth",
            event_family="career",
            driver=6,
            conductor=6,
            personal_year=6,
            verification_status="NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED",
            event_assessment="FAVOURABLE",
            primary_windows=[w.model_dump() for w in timeline.primary_windows],
            method_evaluations=[],
            citations=[],
            policy_version="2.0.0"
        )
        saved_snap = outcome_service.save_snapshot(snap)
        self.assertEqual(saved_snap.prediction_id, "TEST-PRED-SNAP-001")

        # Record outcome
        out_rec = outcome_service.record_outcome(
            prediction_id="TEST-PRED-SNAP-001",
            user_id="test_user_arjun",
            outcome_status="OCCURRED_WITHIN_WINDOW",
            user_comment="Promotion occurred in October as predicted"
        )
        self.assertEqual(out_rec.prediction_id, "TEST-PRED-SNAP-001")
        self.assertEqual(out_rec.outcome_status, "OCCURRED_WITHIN_WINDOW")

        # Invariant: Snapshot remains intact
        retrieved_snap = outcome_service.get_snapshot("TEST-PRED-SNAP-001")
        self.assertEqual(retrieved_snap.prediction_id, "TEST-PRED-SNAP-001")
        self.assertEqual(retrieved_snap.verification_status, "NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED")

    # ─────────────────────────────────────────────────────────────────────────
    # 8. REST API ENDPOINTS
    # ─────────────────────────────────────────────────────────────────────────
    def test_api_charm_chat(self):
        """Test POST /api/charm/chat conversational endpoint."""
        resp = self.client.post("/api/charm/chat", json={
            "name": "Arjun Sharma",
            "dob": "1990-08-15",
            "question": "Is 2026 favorable for expanding my business venture?"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("prediction", data)
        pred = data["prediction"]
        self.assertEqual(pred["primary_method"], "NUMEROLOGY_DASHA")
        self.assertIn("primary_windows", pred)
        self.assertGreater(len(pred["primary_windows"]), 0)

    def test_api_evidence_and_outcome_lifecycle(self):
        """Test full prediction evidence and outcome submission API lifecycle."""
        # Chat first to create prediction
        chat_resp = self.client.post("/api/charm/chat", json={
            "name": "Rohan Mehra",
            "day": 12,
            "month": 4,
            "year": 1988,
            "message": "When is an auspicious period for buying property?"
        })
        self.assertEqual(chat_resp.status_code, 200)
        pred_id = chat_resp.json()["prediction"]["prediction_id"]

        # Evidence lookup
        ev_resp = self.client.get(f"/api/charm/predictions/{pred_id}/evidence")
        self.assertEqual(ev_resp.status_code, 200)
        ev_data = ev_resp.json()
        self.assertEqual(ev_data["prediction_id"], pred_id)

        # Outcome submission
        out_resp = self.client.post("/api/charm/outcomes", json={
            "prediction_id": pred_id,
            "outcome_status": "OCCURRED_WITHIN_WINDOW",
            "user_comment": "Found property within the primary window"
        })
        self.assertEqual(out_resp.status_code, 200)
        out_data = out_resp.json()
        self.assertEqual(out_data["status"], "success")

    def test_api_readings_ask_embeds_charm_prediction(self):
        """Verify POST /api/v1/readings/ask includes charm_prediction card in output."""
        resp = self.client.post("/api/v1/readings/ask", json={
            "name": "Ananya Sen",
            "day": 23,
            "month": 11,
            "year": 1994,
            "question": "Will 2026 bring a job promotion?"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("charm_prediction", data)
        charm_pred = data["charm_prediction"]
        self.assertEqual(charm_pred["primary_method"], "NUMEROLOGY_DASHA")
        self.assertIn("verification_status", charm_pred)
        self.assertIn("primary_windows", charm_pred)

if __name__ == "__main__":
    unittest.main()
