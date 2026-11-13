# -*- coding: utf-8 -*-
"""
Tests for Evidence-Grounded Prediction & Remedy Intelligence Engine:
1. Four-Tier Evidence Model (E1-E4) & Feature Validation
2. Multi-Dimensional Case Retrieval & Counterexample Handling
3. Prediction Ledger & Prospective Outcome Freezing (DPDP 2023)
4. Seven-Engine Prediction Orchestrator & Canonical Result Object
"""

import os
import sys

# Configure UTF-8 stdout
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.abspath("."))

from app.engine.case_intelligence_schema import (
    EvidenceLevel,
    VerificationStatus,
    NumerologyFeatures,
    CaseRecord
)
from app.engine.case_library_engine import CaseLibraryEngine
from app.engine.prediction_ledger_engine import PredictionLedgerEngine
from app.engine.prediction_orchestrator import PredictionOrchestrator


def test_numerology_features_validation():
    # Valid features
    valid = NumerologyFeatures(
        birth_number=1,
        destiny_number=5,
        name_number=6,
        compound_number=33,
        personal_year=9,
        domain="career"
    )
    valid.validate_features()
    assert valid.feature_key() == (1, 5, 6, 33, 9, "career")

    # Invalid birth number (must be 1-9)
    try:
        invalid = NumerologyFeatures(10, 5, 6, 33, 9, "career")
        invalid.validate_features()
        assert False, "Should have raised ValueError for birth_number 10"
    except ValueError:
        pass

    # Invalid compound number (must be > 0)
    try:
        invalid = NumerologyFeatures(1, 5, 6, -5, 9, "career")
        invalid.validate_features()
        assert False, "Should have raised ValueError for negative compound"
    except ValueError:
        pass

    print("[PASS] NumerologyFeatures Validation & Bounds Checking Passed.")


def test_case_library_retrieval():
    engine = CaseLibraryEngine()
    assert len(engine.cases) >= 3, "Case library must contain initial seed cases"

    features = NumerologyFeatures(
        birth_number=1,
        destiny_number=1,
        name_number=1,
        compound_number=37,
        personal_year=1,
        domain="career"
    )

    matches = engine.retrieve_similar_cases(features, limit=3)
    assert len(matches) > 0
    top_match = matches[0]
    
    assert top_match["case_id"] == "NV-CASE-000001"
    assert top_match["evidence_level"] == EvidenceLevel.E3_PRACTITIONER_CASE.value
    assert "similarity_score" in top_match
    assert top_match["similarity_score"] > 0.5
    
    # Counterexample case (NV-CASE-000003) must be present in library
    counterexamples = [c for c in engine.cases if c.get("source", {}).get("verification_status") == VerificationStatus.CONTRADICTED.value]
    assert len(counterexamples) >= 1
    assert counterexamples[0]["case_id"] == "NV-CASE-000003"

    print("[PASS] Multi-Dimensional Case Retrieval & Counterexample Verification Passed.")


def test_prediction_ledger_and_outcome_tracking():
    ledger = PredictionLedgerEngine()
    initial_count = len(ledger.ledger)

    # 1. Freeze a prospective prediction
    frozen = ledger.freeze_prediction(
        user_identifier="user_test_99@example.com",
        domain="career",
        forecast_text="Personal Year 1 initiation favoring executive transition.",
        start_date="2026-11-01",
        end_date="2027-04-01",
        success_criterion="Receiving formal written promotion offer",
        prediction_mode="MODE_A_TRADITIONAL"
    )

    assert frozen["status"] == "ACTIVE_PENDING"
    assert "user_test_99" not in frozen["user_hash"]  # SHA-256 hashed
    assert len(ledger.ledger) == initial_count + 1
    ledger_id = frozen["ledger_id"]

    # 2. Record verified outcome after event window
    resolved = ledger.record_outcome(
        ledger_id=ledger_id,
        outcome_status="VERIFIED_SUCCESS",
        observed_result="User promoted to Director of Engineering in March 2027.",
        evidence_source="Consented user verification submission with offer letter proof",
        confounders=["Organizational restructuring"],
        independent_review=True
    )

    assert resolved["status"] == "VERIFIED_SUCCESS"
    assert resolved["post_event_outcome"]["independent_review"] is True
    assert resolved["forecast_text"] == "Personal Year 1 initiation favoring executive transition."  # Unmodified!

    print("[PASS] Prediction Ledger Freezing & Real-World Outcome Tracking Passed.")


def test_prediction_orchestrator_canonical_analysis():
    orchestrator = PredictionOrchestrator()

    canonical = orchestrator.generate_canonical_analysis(
        birth_date="1988-10-19",
        full_name="Rohan Verma",
        gender="male",
        domain="career",
        question="Executive career progression and board elevation"
    )

    # 1. Structure & Provenance
    assert "canonical_id" in canonical
    assert canonical["ruleset_version"] == "2.0.0"

    # 2. Deterministic Core Calculations (E1)
    core = canonical["core_matrix"]
    assert core["driver"] == 1  # 19 -> 1
    assert core["subdate_category"] == "A"  # 19(a) Prince of Heaven
    assert core["personal_year"] in range(1, 10)
    assert core["name_root"] in range(1, 10)

    # 3. Day 8 Complementary Evaluation
    assert "complementary_support_day8" in canonical
    assert canonical["complementary_support_day8"]["pipeline_version"] == "1.0.0"

    # 4. Retrieved Historical Cases (E3)
    assert len(canonical["historical_cases"]) > 0
    assert canonical["historical_cases"][0]["evidence_level"] == "E3"

    # 5. Governed Prediction Engine
    preds = canonical["predictions"]
    assert preds["mode_a_traditional_forecast"]["evidence_level"] == "E2"
    assert preds["mode_b_empirical_prediction"]["status"] == "UNVALIDATED_FOR_EMPIRICAL_PROBABILITY"

    # 6. Remedy Proportionality (Practical First)
    remedies = canonical["remedies"]
    assert len(remedies["practical_actions_first"]) >= 2
    assert "panch_tattva_tactile_hygiene" in remedies

    # 7. Audit Trail
    audit = canonical["evidence_audit_trail"]
    assert audit["E1_arithmetic_verified"] is True
    assert audit["E4_empirical_guarantees_prohibited"] is True

    print("[PASS] Seven-Engine Prediction Orchestrator & Canonical Result Validated.")


if __name__ == "__main__":
    test_numerology_features_validation()
    test_case_library_retrieval()
    test_prediction_ledger_and_outcome_tracking()
    test_prediction_orchestrator_canonical_analysis()
    print("\nALL EVIDENCE-GROUNDED PREDICTION & REMEDY ENGINE TESTS PASSED!")
