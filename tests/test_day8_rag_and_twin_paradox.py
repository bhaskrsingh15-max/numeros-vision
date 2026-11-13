# -*- coding: utf-8 -*-
"""
Tests for Day 8 Canon:
1. Quality-Specific Complementary Numbers (Purak Numbers)
2. Master Key Number 5 & Willpower Plane (1-5-9)
3. Twin Paradox Input-Output 3-Layer Architecture
4. RAG Knowledge Base Governance & Unresolved Gaps
"""

import json
import os
import sys

# Configure UTF-8 stdout
if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.abspath("."))

from app.engine.complementary_poorak_engine import (
    DAY8_QUALITY_COMPLEMENTARY_REGISTRY,
    evaluate_grid_complementary_support,
    calculate_complementary_poorak
)
from app.engine.twin_paradox_engine import TwinParadoxEngine


def test_day8_knowledge_base_json():
    path = os.path.join("data", "knowledge_base", "day8_complementary_masterkey_twins_rules.json")
    assert os.path.exists(path), "Day 8 JSON must exist"
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    rules = data.get("rules", [])
    assert len(rules) >= 15, f"Expected at least 15 rules, found {len(rules)}"
    
    # Check schema fields on every rule
    for r in rules:
        assert "rule_id" in r
        assert "source_session" in r
        assert "concept" in r
        assert "evidence_type" in r
        assert "confidence_status" in r
        assert "method_version" in r
        
    gaps = data.get("unresolved_validation_gaps", [])
    assert len(gaps) >= 7, f"Expected 7 unresolved gaps, found {len(gaps)}"
    print("[PASS] Day 8 Knowledge Base JSON Schema & Rules Validated.")


def test_quality_specific_complementary_engine():
    # Verify exact pairings from Day 8
    assert DAY8_QUALITY_COMPLEMENTARY_REGISTRY[1]["complements"] == [9]
    assert DAY8_QUALITY_COMPLEMENTARY_REGISTRY[2]["complements"] == [3, 7]
    assert DAY8_QUALITY_COMPLEMENTARY_REGISTRY[3]["complements"] == [7]
    assert DAY8_QUALITY_COMPLEMENTARY_REGISTRY[4]["complements"] == [8]
    assert DAY8_QUALITY_COMPLEMENTARY_REGISTRY[5]["complements"] == [6]
    assert DAY8_QUALITY_COMPLEMENTARY_REGISTRY[6]["complements"] == [5]
    assert DAY8_QUALITY_COMPLEMENTARY_REGISTRY[7]["complements"] == [3]
    assert DAY8_QUALITY_COMPLEMENTARY_REGISTRY[8]["complements"] == [4, 5]
    assert DAY8_QUALITY_COMPLEMENTARY_REGISTRY[9]["complements"] == [1]

    # Verify 4-to-8 is strictly limited to discipline
    lim_4 = DAY8_QUALITY_COMPLEMENTARY_REGISTRY[4]["limitation"]
    assert "limits the 8-to-4 relationship to discipline" in lim_4

    print("[PASS] Quality-Specific Complementary Registry Validated.")


def test_evaluate_grid_complementary_support():
    # Scenario: Seeker missing 4 and 2, but has 8 and 3
    # Grid: {1: 1, 2: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 0, 8: 1, 9: 1}
    # Present: 1, 3, 5, 8, 9. Absent: 2, 4, 6, 7.
    grid = {1: 1, 2: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 0, 8: 1, 9: 1}
    res = evaluate_grid_complementary_support(grid)
    
    assert res["pipeline_version"] == "1.0.0"
    assert 4 in res["absent_numbers"]
    assert 2 in res["absent_numbers"]
    
    # 4 is missing, but 8 is present -> COMPENSATED
    rec_4 = [r for r in res["evaluations"] if r["missing_number"] == 4][0]
    assert rec_4["is_compensated"] is True
    assert 8 in rec_4["active_complements"]
    assert "Discipline" in rec_4["supported_qualities"][0]
    
    # 2 is missing, and 3 is present -> COMPENSATED by 3
    rec_2 = [r for r in res["evaluations"] if r["missing_number"] == 2][0]
    assert rec_2["is_compensated"] is True
    assert 3 in rec_2["active_complements"]
    
    # Master Key 5 evaluation: 5 is present, 1 and 9 present -> Willpower plane active!
    mk5 = res["master_key_5_evaluation"]
    assert mk5["is_number_5_present"] is True
    assert mk5["fighter_archetype_active"] is True
    assert mk5["willpower_plane_159"]["is_fully_present"] is True
    
    # Missing 6 supported by 5 applies!
    assert mk5["missing_6_support"]["applies"] is True
    
    # Remedy multiplier claim is flagged as UNVERIFIED_TEACHING_CLAIM
    assert mk5["remedy_acceleration_claim"]["implementation_treatment"] == "UNVERIFIED_TEACHING_CLAIM"
    
    print("[PASS] 6-Step Complementary & Master Key 5 Evaluation Validated.")


def test_twin_paradox_engine():
    engine = TwinParadoxEngine()
    
    twin_a = {
        "name": "Arjun Sharma",
        "education_stream": "Computer Science",
        "career_choice": "Software Architecture",
        "partner_dob": "1994-08-15",
        "relocation_city": "Bangalore"
    }
    
    twin_b = {
        "name": "Rohit Sharma",
        "education_stream": "Chartered Accountancy",
        "career_choice": "Tax & Investment Consulting",
        "partner_dob": "1996-03-22",
        "relocation_city": "Mumbai"
    }
    
    res = engine.analyze_twin_pair(
        birth_date="1992-05-14",
        twin_a_inputs=twin_a,
        twin_b_inputs=twin_b,
        gender_a="MALE",
        gender_b="MALE"
    )
    
    # Fixed foundations MUST be identical
    layer1 = res["layer_1_fixed_foundations"]
    assert layer1["driver"] == 5  # 14 -> 5
    assert layer1["conductor"] == 4  # 14 + 5 + 1992 -> 1+4+5+1+9+9+2 = 31 -> 4
    
    # Divergences must highlight acoustic name, career, and partner
    divs = res["layer_3_observed_divergences"]
    assert len(divs) >= 3
    
    dimensions = [d["dimension"] for d in divs]
    assert any("Acoustic Name" in dim for dim in dimensions)
    assert any("Vocation" in dim for dim in dimensions)
    assert any("Partner Synastry" in dim for dim in dimensions)
    
    # Scientific governance caveat must be present
    assert "scientific_disclaimer" in res["governance_and_claim_status"]
    
    print("[PASS] Twin Paradox 3-Layer Input-Output Engine Validated.")


if __name__ == "__main__":
    test_day8_knowledge_base_json()
    test_quality_specific_complementary_engine()
    test_evaluate_grid_complementary_support()
    test_twin_paradox_engine()
    print("\nALL DAY 8 RAG & TWIN PARADOX TESTS PASSED SUCCESSFULLY!")
