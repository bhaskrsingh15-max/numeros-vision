"""
tests/test_consolidated_specification_v1.py
============================================
Comprehensive Automated Test Suite for:
NUMEROS VISION + CHARM AI — Consolidated Specification v1.0
Unified Deterministic Astrology, Numerology, Consensus, Timing and Remedy Engine.

Validates:
1. Independent Method Isolation across all 6 traditions:
   - Numerology Dasha (Primary Timing Anchor)
   - KP Astrology (10th Cuspal Sub-Lord Matrix)
   - Vedic Parashari Jyotish (Sambandha Yogas & Gochar Transits)
   - Bhrigu Nandi Nadi (BNN Karaka Conjunctions)
   - Western Pythagorean Numerology (Master Numbers & Karmic Debts)
   - Vedic Sankhya Shastra (Driver/Conductor Dynamics)
   - Lal Kitab (Safely Gated / Disabled per Section 1.2)
2. Primary Window Immutability:
   - Astrological cross-checks cannot alter Numerology Dasha dates.
3. Real-Time Astronomical Ephemeris:
   - Transit coordinates, retrograde (vakri) status, sign lords, and ingress epochs.
4. Deterministic Consensus Status Coverage:
   - NUMEROLOGY_PRIMARY_CORROBORATED, NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED,
     NUMEROLOGY_PRIMARY_CONFLICTED, NUMEROLOGY_PRIMARY_ONLY, INSUFFICIENT_EVIDENCE,
     NOT_ELIGIBLE_FOR_PREDICTION.
5. Golden Heart Communication Doctrine:
   - Empathetic re-framing, unblocking steps, zero alarming fatalism.
6. Statutory Compliance & Non-Magic Remedy Notices (Drugs & Magic Remedies Act 1954).
7. Brand Tagline ('ANVEIL EVERY CHARM') & Zero Raw Black Compliance.
"""

import unittest
from datetime import date
from fastapi.testclient import TestClient

from app.main import app
from app.charm.intent.event_intent_service import event_intent_service
from app.charm.numerology.dasha_engine import numerology_dasha_engine
from app.charm.consensus.engine import consensus_engine
from app.charm.charts.fact_provider import planetary_fact_provider, TRANSIT_POSITIONS_2026
from app.charm.methods.kp_adapter import kp_adapter
from app.charm.methods.vedic_adapter import vedic_adapter
from app.charm.methods.bnn_adapter import bnn_adapter
from app.charm.methods.pythagorean_adapter import pythagorean_adapter
from app.charm.methods.vedic_numerology_adapter import vedic_numerology_adapter
from app.charm.methods.lal_kitab_adapter import lal_kitab_adapter
from app.charm.chat.response_composer import charm_chat_orchestrator
from app.engine.consensus import generate_consensus_reading


class TestConsolidatedSpecificationV1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # ─────────────────────────────────────────────────────────────────────────
    # 1. INDEPENDENT METHOD ISOLATION & TRADITIONS
    # ─────────────────────────────────────────────────────────────────────────
    def test_independent_method_adapters_execution(self):
        """Verify each tradition calculates independently without cross-contamination."""
        event_def = {"event_family": "career", "event_definition_id": "career_growth", "event_type": "promotion"}
        profile = {"day": 15, "month": 8, "year": 1990, "name": "Arjun Sharma", "driver": 6, "conductor": 6}
        chart_facts = planetary_fact_provider.get_chart_facts(city="delhi")

        # KP Astrology
        kp_eval = kp_adapter.evaluate(event_def, profile, chart_facts.model_dump())
        self.assertEqual(kp_eval.method_id, "KP_ASTROLOGY")
        self.assertIn(kp_eval.assessment, ["SUPPORTS", "CHALLENGES", "MIXED"])
        self.assertEqual(kp_eval.status, "VALID")

        # Vedic Astrology
        vedic_eval = vedic_adapter.evaluate(event_def, profile, chart_facts.model_dump())
        self.assertEqual(vedic_eval.method_id, "VEDIC_ASTROLOGY")
        self.assertIn(vedic_eval.assessment, ["SUPPORTS", "CHALLENGES", "MIXED"])
        self.assertEqual(vedic_eval.status, "VALID")

        # Bhrigu Nandi Nadi (BNN)
        bnn_eval = bnn_adapter.evaluate(event_def, profile, chart_facts.model_dump())
        self.assertEqual(bnn_eval.method_id, "BNN_NADI")
        self.assertIn(bnn_eval.assessment, ["SUPPORTS", "CHALLENGES", "MIXED"])
        self.assertEqual(bnn_eval.status, "VALID")

        # Western Pythagorean
        pyth_eval = pythagorean_adapter.evaluate(event_def, profile, chart_facts.model_dump())
        self.assertEqual(pyth_eval.method_id, "PYTHAGOREAN_NUMEROLOGY")
        self.assertIn(pyth_eval.assessment, ["SUPPORTS", "CHALLENGES", "MIXED"])
        self.assertEqual(pyth_eval.status, "VALID")

        # Vedic Sankhya Shastra
        vnum_eval = vedic_numerology_adapter.evaluate(event_def, profile, chart_facts.model_dump())
        self.assertEqual(vnum_eval.method_id, "VEDIC_NUMEROLOGY")
        self.assertIn(vnum_eval.assessment, ["SUPPORTS", "CHALLENGES", "MIXED"])
        self.assertEqual(vnum_eval.status, "VALID")

        # Lal Kitab (Gated per Section 1.2)
        lk_eval = lal_kitab_adapter.evaluate(event_def, profile, chart_facts.model_dump())
        self.assertEqual(lk_eval.method_id, "LAL_KITAB")
        self.assertEqual(lk_eval.assessment, "NOT_EVALUATED")
        self.assertEqual(lk_eval.status, "DISABLED")

    # ─────────────────────────────────────────────────────────────────────────
    # 2. PRIMARY WINDOW IMMUTABILITY
    # ─────────────────────────────────────────────────────────────────────────
    def test_numerology_dasha_primary_timing_immutability(self):
        """Verify Dasha timing window is strictly immutable and cannot be rewritten by astrology."""
        dasha_res = numerology_dasha_engine.evaluate_dasha_hierarchy(15, 8, 1990)
        self.assertTrue(len(dasha_res.primary_windows) > 0)
        original_start = dasha_res.primary_windows[0].start
        original_end = dasha_res.primary_windows[0].end

        resp = charm_chat_orchestrator.process_chat_turn(
            message="Will I get promoted to Director this year?",
            user_name="Arjun Sharma",
            day=15,
            month=8,
            year=1990
        )
        self.assertEqual(resp.status, "ANSWERED")
        primary_wins = resp.prediction["primary_windows"]
        self.assertEqual(primary_wins[0]["start"], original_start)
        self.assertEqual(primary_wins[0]["end"], original_end)

    # ─────────────────────────────────────────────────────────────────────────
    # 3. REAL-TIME ASTRONOMICAL EPHEMERIS & RETROGRADE (VAKRI) DATA
    # ─────────────────────────────────────────────────────────────────────────
    def test_realtime_astronomical_ephemeris(self):
        """Verify 2026 transits, retrograde states, sign lords, and ingress epochs."""
        facts = planetary_fact_provider.get_chart_facts(city="delhi")
        positions = facts.planetary_positions

        # Saturn check
        saturn = positions["Saturn"]
        self.assertIn("Pisces", saturn["sign"])
        self.assertIn("motion_state", saturn)
        self.assertIn("sign_lord", saturn)
        self.assertIn("nakshatra", saturn)
        self.assertIn("ingress_epoch", saturn)

        # Rahu/Ketu retrograde (Vakri) check
        rahu = positions["Rahu"]
        ketu = positions["Ketu"]
        self.assertTrue(rahu["is_retrograde"])
        self.assertTrue(ketu["is_retrograde"])
        self.assertIn("Vakri", rahu["motion_state"])
        self.assertIn("Vakri", ketu["motion_state"])

    # ─────────────────────────────────────────────────────────────────────────
    # 4. DETERMINISTIC CONSENSUS STATUS DETERMINATION
    # ─────────────────────────────────────────────────────────────────────────
    def test_consensus_engine_statuses(self):
        """Verify consensus engine resolves strictly into approved statuses."""
        dasha = numerology_dasha_engine.evaluate_dasha_hierarchy(15, 8, 1990)
        event_def = {"event_family": "career", "event_definition_id": "career_growth"}

        # Empty evaluations -> NUMEROLOGY_PRIMARY_ONLY
        res_only = consensus_engine.derive_consensus(dasha, [], event_def)
        self.assertEqual(res_only.verification_status, "NUMEROLOGY_PRIMARY_ONLY")

        # Missing DOB -> INSUFFICIENT_EVIDENCE
        dasha_empty = numerology_dasha_engine.evaluate_dasha_hierarchy(0, 0, 0)
        res_insufficient = consensus_engine.derive_consensus(dasha_empty, [], event_def)
        self.assertEqual(res_insufficient.verification_status, "INSUFFICIENT_EVIDENCE")

        # Death/Lottery query -> NOT_ELIGIBLE_FOR_PREDICTION
        res_ineligible = consensus_engine.derive_consensus(dasha, [], {"event_definition_id": "lottery_gambling"})
        self.assertEqual(res_ineligible.verification_status, "NOT_ELIGIBLE_FOR_PREDICTION")

    # ─────────────────────────────────────────────────────────────────────────
    # 5. GOLDEN HEART MASTER CONSULTATION & DIALOGUE
    # ─────────────────────────────────────────────────────────────────────────
    def test_golden_heart_humanized_consultation_tone(self):
        """Verify consultation is compassionate, non-alarming, and solution-focused."""
        resp = charm_chat_orchestrator.process_chat_turn(
            message="I feel completely stuck and missed all opportunities in my job",
            user_name="Priya Patel",
            day=22,
            month=4,
            year=1992
        )
        self.assertEqual(resp.status, "ANSWERED")
        dialogue = resp.human_friendly_summary["full_dialogue_text"]

        # Empathetic opening, zero alarming labels
        self.assertIn("take a deep breath", dialogue.lower())
        self.assertNotIn("cursed", dialogue.lower())
        self.assertNotIn("bad chart", dialogue.lower())
        self.assertNotIn("doomed", dialogue.lower())

        # Grounded practical actions present
        actions = resp.human_friendly_summary["practical_actions"]
        self.assertTrue(len(actions) >= 2)
        self.assertIn("Three Practical Actions", dialogue)

    # ─────────────────────────────────────────────────────────────────────────
    # 6. STATUTORY DISCLAIMER & LIFESTYLE REMEDIES
    # ─────────────────────────────────────────────────────────────────────────
    def test_statutory_remedy_compliance(self):
        """Verify Drugs and Magic Remedies Act 1954 compliance notices."""
        report = generate_consensus_reading("Bhaskr Singh", 15, 8, 1995)
        crystals = report.get("safe_crystals_and_gemstones", {})
        self.assertIn("statutory_compliance_notice", crystals)
        self.assertIn("Drugs & Magic Remedies Act 1954", crystals["statutory_compliance_notice"])

    # ─────────────────────────────────────────────────────────────────────────
    # 7. BRAND INTEGRITY & ZERO RAW BLACK
    # ─────────────────────────────────────────────────────────────────────────
    def test_brand_tagline_integrity(self):
        """Verify brand tagline ANVEIL EVERY CHARM is strictly preserved."""
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("ANVEIL EVERY CHARM", resp.text)
        self.assertNotIn("UNVEIL EVERY CHARM", resp.text)


if __name__ == "__main__":
    unittest.main()
