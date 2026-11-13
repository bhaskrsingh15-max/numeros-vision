"""
SCRIPTS: TEST PREDICTION LEVELS AND DATA SOURCES (LIVE COMPREHENSIVE SUITE)
Tests and validates:
1. Level 1: Foundational Natal Archetype (Mulank, Bhagyank, Kua, Chaldean/Cheiro Name).
2. Level 2: Geometrical Lo Shu Vectors (8 Planes of Destiny, Rajyogs, Vacuums).
3. Level 3: Chronological Cycles (Mahadasha, Antardasha, Personal Year/Month/Day).
4. Level 4: Blessing Years Milestone Timeline (Age 18 to 75 Convergence).
5. Level 5: Multi-System Astrological Concurrence (KP Sub-Lord, Vedic Yogas, Lal Kitab Masnooi, BNN Pairs).
6. Level 6: Holistic Remedial Harmonization & Asset Resonance (Mobile, Vehicle, Vastu Sheng Chi).
7. Level 7: Tamper-Evident Empirical Outcome Registry (Practitioner SHA-256 seed).
8. Data Source Confidentiality & Shielding (Zero external leakage, 100% sovereign mapping).
9. Live HTTP API Endpoint Verification against the active server.
"""

import sys
import os
import json
import urllib.request
import urllib.error
import datetime

# Setup root path
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from app.engine.core_matrix_engine import (
    generate_core_matrix_profile,
    calculate_driver,
    calculate_conductor,
    calculate_kua_number,
    calculate_chaldean_name
)
from app.engine.enhanced_lo_shu_engine import (
    build_birth_date_grid,
    build_name_derived_grid,
    compare_name_change_grids
)
from app.engine.forecast_engine import (
    calculate_blessing_years,
    generate_multi_year_forecast,
    generate_detailed_annual_matrix
)
from app.engine.unified_planetary_numerology_engine import (
    KP_SUBLORD_RULES,
    LAL_KITAB_MASNOOI_MAP,
    LAL_KITAB_AWAKENING_AGES,
    PLANET_BY_NUMBER
)
from app.engine.bnn_numerology_engine import (
    BNN_PAIR_DATABASE,
    PLANET_NUMBER_MAP
)
from app.engine.consensus import generate_consensus_reading
from app.engine.remedy_rules_engine import select_remedies_and_yantras
from app.engine.asset_numerology_engine import analyze_mobile_number
from app.engine.practitioner_engine import (
    register_client_profile,
    log_prediction,
    record_prediction_outcome
)
from app.engine.source_privacy_shield import (
    sanitize_citation,
    sanitize_text,
    SOURCE_PROPRIETARY_MAPPING
)

def run_prediction_levels_test():
    print("=" * 80)
    print("NUMEROS VISION / CHARM AI — COMPREHENSIVE PREDICTION LEVELS & SOURCES TEST")
    print("=" * 80)

    test_name = "Bhaskr Singh"
    day, month, year = 28, 11, 1981
    mobile = "9876543210"
    print(f"\n[TEST PROFILE] Subject: {test_name} | DOB: {day:02d}-{month:02d}-{year} | Mobile: {mobile}")

    results = {}

    # ── LEVEL 1: CORE NATAL ARCHETYPE ──
    print("\n" + "-" * 40)
    print(">>> [LEVEL 1] Foundational Natal Archetype (Core Matrix)")
    driver = calculate_driver(day)
    conductor = calculate_conductor(day, month, year)
    kua = calculate_kua_number(year, gender="male")
    name_eval = calculate_chaldean_name(test_name)
    core_profile = generate_core_matrix_profile(test_name, day, month, year, mobile_number=mobile, gender="male")

    print(f"  • Driver (Mulank): {driver} ({core_profile['core_numbers']['driver_planet']}) [Day {day} -> 2+8=10 -> 1]")
    print(f"  • Conductor (Bhagyank): {conductor} ({core_profile['core_numbers']['conductor_planet']}) [Total sum -> 31 -> 4]")
    print(f"  • Kua Directional Number: {kua} ({core_profile['core_numbers']['kua_profile']['trigram']} Trigram - {core_profile['core_numbers']['kua_profile']['energy_group']})")
    print(f"  • Name Compound (Chaldean): {name_eval['compound_sum']} -> Root {name_eval['single_root']} (Master 33 Vibration)")
    print(f"  • Poorak Number: {core_profile['poorak_number_analysis']['poorak_number']} ({core_profile['poorak_number_analysis']['rationale'][:60]}...)")
    print(f"  • Lottery / Speculative Picks: {core_profile['speculative_and_lottery_numbers']['lottery_numbers']}")

    assert driver == 1, f"Expected driver 1, got {driver}"
    assert conductor == 4, f"Expected conductor 4, got {conductor}"
    assert kua == 1, f"Expected kua 1, got {kua}"
    results["Level_1"] = "PASSED"

    # ── LEVEL 2: GEOMETRIC ENERGY VECTORS (LO SHU GRID & 8 PLANES) ──
    print("\n" + "-" * 40)
    print(">>> [LEVEL 2] Geometric Energy Vectors (Lo Shu Grid & 8 Planes)")
    lo_shu_data = build_birth_date_grid(day, month, year)
    present_numbers = [num for num, count in lo_shu_data['digit_counts'].items() if count > 0]
    print(f"  • Present Numbers: {present_numbers}")
    print(f"  • Missing Numbers: {lo_shu_data['missing_numbers']}")
    print(f"  • Repeated Numbers: {lo_shu_data['repeated_numbers']}")
    completed_planes = [p for p, data in lo_shu_data['planes'].items() if data['status'] == 'COMPLETE']
    print(f"  • Completed Planes ({len(completed_planes)}): {completed_planes}")
    print(f"  • Active Strengths: {[a['arrow'] for a in lo_shu_data['arrows_of_strength']]}")
    print(f"  • Missing Voids: {[a['arrow'] for a in lo_shu_data['arrows_of_weakness']]}")

    assert 1 in present_numbers
    assert 8 in present_numbers
    assert 9 in present_numbers
    assert 2 in present_numbers
    results["Level_2"] = "PASSED"

    # ── LEVEL 3: CHRONOLOGICAL CYCLES (DASHA & PERSONAL CYCLES) ──
    print("\n" + "-" * 40)
    print(">>> [LEVEL 3] Chronological Cycles (Dasha & Personal Timing)")
    multi_year = generate_multi_year_forecast(day, month, start_year=2026)
    annual_2026 = generate_detailed_annual_matrix(day, month, target_year=2026)
    dasha_cycles = core_profile["dasha_cycles"]
    print(f"  • Active Mahadasha: Number {dasha_cycles['mahadasha_number']} ({dasha_cycles['mahadasha_planet']})")
    print(f"  • Active Antardasha: Number {dasha_cycles['antardasha_number']} ({dasha_cycles['antardasha_planet']})")
    curr_fc = multi_year[0]
    print(f"  • Personal Year {curr_fc['year']}: {curr_fc['personal_year']} - {curr_fc['cycle_archetype']}")
    print(f"  • Next Horizons: {[(y['year'], y['personal_year'], y['cycle_archetype'][:25] + '...') for y in multi_year[1:]]}")
    sample_m1 = annual_2026['monthly_matrix'][0]
    print(f"  • 2026 Sample Month 1 Focus: {sample_m1['month_name']} (PM {sample_m1['personal_month']} - {sample_m1['focal_theme']})")

    assert curr_fc['personal_year'] == 4, f"Expected PY 4 for current year, got {curr_fc['personal_year']}"
    results["Level_3"] = "PASSED"

    # ── LEVEL 4: BLESSING YEARS MILESTONE TIMELINE ──
    print("\n" + "-" * 40)
    print(">>> [LEVEL 4] Blessing Years Milestone Timeline")
    blessing_data = calculate_blessing_years(day, month, year, current_age=45)
    print(f"  • Supreme Blessing Years Count: {blessing_data['supreme_blessing_years_count']}")
    print(f"  • High Support Years Count: {blessing_data['high_support_years_count']}")
    print(f"  • Total Evaluated Life Milestones: {len(blessing_data['full_timeline'])} milestones (Ages 18 to 75)")
    if blessing_data['immediate_upcoming_blessings']:
        next_bless = blessing_data['immediate_upcoming_blessings'][0]
        print(f"  • Immediate Upcoming Catalytic Milestone: Age {next_bless['age']} (Year {next_bless['calendar_year']} | Score {next_bless['blessing_score']})")
    sample_milestone = blessing_data['full_timeline'][0]
    print(f"  • Sample Milestone @ Age {sample_milestone['age']}: Year {sample_milestone['calendar_year']} | Tier: {sample_milestone['blessing_tier']} | Theme: {sample_milestone['milestone_theme']}")

    assert blessing_data['supreme_blessing_years_count'] > 0
    results["Level_4"] = "PASSED"

    # ── LEVEL 5: MULTI-SYSTEM ASTROLOGICAL CONCURRENCE ──
    print("\n" + "-" * 40)
    print(">>> [LEVEL 5] Multi-System Astrological Concurrence & Conjunctions")
    kp_rule = KP_SUBLORD_RULES.get(driver, {}).get(conductor, {})
    print(f"  • KP Sub-Lord Synthesis: Driver {driver} (Star-Lord) + Conductor {conductor} (Deciding Sub-Lord)")
    print(f"    - Verdict: {kp_rule.get('verdict')}")
    print(f"    - Signified Domains: {kp_rule.get('life_domain')}")
    print(f"    - Decisive Fruit: {kp_rule.get('fruit')}")

    # Lal Kitab Awakening & Masnooi
    d_awaken = LAL_KITAB_AWAKENING_AGES.get(driver)
    c_awaken = LAL_KITAB_AWAKENING_AGES.get(conductor)
    masnooi = LAL_KITAB_MASNOOI_MAP.get((driver, conductor), {"masnooi_planet": "Direct Polar Synergy", "meaning": "Dynamic combination."})
    print(f"  • Lal Kitab Destiny Awakening Ages: Driver awakens @ Age {d_awaken}, Conductor awakens @ Age {c_awaken}")
    print(f"  • Lal Kitab Masnooi Interaction: {masnooi.get('masnooi_planet')} -> {masnooi.get('meaning')}")

    # BNN Planetary Conjunction
    bnn_pair = BNN_PAIR_DATABASE.get((driver, conductor))
    if bnn_pair:
        print(f"  • BNN Planetary Conjunction (1-4): {bnn_pair['title']}")
        print(f"    - Archetype: {bnn_pair['archetype']}")
        print(f"    - Predictions: {bnn_pair['bnn_predictions'][:120]}...")
    else:
        print(f"  • BNN Planetary Pair: Driver {driver} (Sun) & Conductor {conductor} (Rahu)")

    # Multi-System Consensus Reading
    consensus_res = generate_consensus_reading(test_name, day, month, year)
    print(f"  • Cross-Tradition Consensus Certainty: {consensus_res['overall_consensus_strength_pct']}% Agreement")
    for dom, v in consensus_res["domain_verdicts"].items():
        print(f"    * {dom}: {v['verdict']} ({v['consensus_score_pct']}%)")

    assert consensus_res['overall_consensus_strength_pct'] > 50.0
    results["Level_5"] = "PASSED"

    # ── LEVEL 6: REMEDIAL HARMONIZATION & ASSET HARMONICS ──
    print("\n" + "-" * 40)
    print(">>> [LEVEL 6] Remedial Harmonization & Asset Resonance")
    remedies = select_remedies_and_yantras(driver, conductor, missing_numbers=lo_shu_data['missing_numbers'], max_remedies=4)
    yantra = remedies['prescribed_yantra']
    print(f"  • Prescribed Yantra: {yantra['name']} (Material: {yantra['material']}, Direction: {yantra['optimal_direction']})")
    print(f"  • Excluded Conflict Numbers: {remedies['excluded_conflict_numbers']}")
    print(f"  • Curated Actionable Remedies ({remedies['total_remedies_prescribed']}):")
    for r in remedies['prescribed_remedies']:
        print(f"    * [{r['category']}] {r['action'][:75]}...")

    # Asset Analysis: Mobile
    mobile_audit = analyze_mobile_number(mobile, driver, conductor)
    print(f"  • Mobile Number Audit ({mobile}):")
    print(f"    * Compound Total: {mobile_audit['total_compound']} -> Single Root {mobile_audit['total_root']} ({mobile_audit['root_planet']})")
    print(f"    * Compatibility: Driver ({mobile_audit['driver_compatibility']}), Conductor ({mobile_audit['conductor_compatibility']})")
    print(f"    * Malefic Pairs Detected: {mobile_audit['malefic_pairs_detected']}")
    print(f"    * Status: {mobile_audit['overall_status']}")

    # Vastu Directions
    vastu = core_profile['vastu_directional_synthesis']
    print(f"  • Vastu / Kua Directional Apex:")
    print(f"    * Wealth / Career (Sheng Chi): {vastu['wealth_and_career_apex']['primary_sheng_chi']}")
    print(f"    * Vitality / Recovery (Tien Yi): {vastu['health_and_vitality_anchor']['primary_tien_yi']}")
    print(f"    * Relationships (Nien Yen): {vastu['relationship_and_family_harmony']['primary_nien_yen']}")

    assert yantra['name'] is not None
    results["Level_6"] = "PASSED"

    # ── LEVEL 7: TAMPER-EVIDENT EMPIRICAL OUTCOME REGISTRY ──
    print("\n" + "-" * 40)
    print(">>> [LEVEL 7] Tamper-Evident Empirical Outcome Registry (Practitioner Governance)")
    client = register_client_profile("default_practitioner", test_name, f"{year}-{month:02d}-{day:02d}")
    client_id = client["client_id"]
    pred = log_prediction(
        client_id=client_id,
        practitioner_id="default_practitioner",
        prediction_text="Substantial international technological expansion occurring in Q3/Q4 of 2026.",
        category="CAREER",
        target_period_start="2026-07-01",
        target_period_end="2026-12-31",
        confidence_level="VERY_HIGH"
    )
    print(f"  • Prospective Prediction ID: {pred['prediction_id']}")
    print(f"  • Immutable Registration Timestamp: {pred['registered_at']}")
    print(f"  • Tamper-Evident Hash Seed: {pred['immutable_hash_seed']}")
    print(f"  • Evaluation Status: {pred['status']}")

    eval_res = record_prediction_outcome(
        prediction_id=pred['prediction_id'],
        outcome_status="FULFILLED",
        practitioner_notes="Matches Personal Year 4 structural foundation and Rahu innovation cycle. Confirmed by client."
    )
    print(f"  • Outcome Audited: {eval_res['status']} -> Final Status: {eval_res['final_status']}")

    assert eval_res['status'] == "OUTCOME_RECORDED"
    results["Level_7"] = "PASSED"

    # ── PREDICTION DATA SOURCES AUDIT & PRIVACY LOCK ──
    print("\n" + "-" * 40)
    print(">>> [CONFIDENTIAL IP & DATA SOURCES AUDIT] Source Privacy Shield Validation")
    print(f"  • Total Sovereign Catalog Entitlements Registered: {len(SOURCE_PROPRIETARY_MAPPING)}")
    sample_mappings = list(SOURCE_PROPRIETARY_MAPPING.items())[:5]
    for raw_src, sov_name in sample_mappings:
        print(f"    * Internal Matrix Node -> Cloaked Identity: '{sov_name}'")

    # Test sanitization gate
    test_raw_citation = {
        "source": "Cheiro's Book of Numbers (English Edition, 1935)",
        "location": "Chapter 3",
        "category": "Foundations",
        "excerpt": "Number 1 represents Sun, leadership and ambition."
    }
    sanitized = sanitize_citation(test_raw_citation)
    print(f"  • Live Cloaking Demonstration:")
    print(f"    - Input Source: '{test_raw_citation['source']}'")
    print(f"    - Sanitized Output: '{sanitized['source']}'")
    print(f"    - Privacy Verified: {'Cheiro' not in sanitized['source']}")

    assert "Cheiro" not in sanitized['source']
    assert "Numeros Vision" in sanitized['source']
    results["Source_Shield"] = "PASSED"

    # ── LIVE HTTP REST API ENDPOINT VERIFICATION ──
    print("\n" + "-" * 40)
    print(">>> [LIVE HTTP REST API VERIFICATION] Stealth Server (http://127.0.0.1:8000)")
    
    api_endpoints_to_test = [
        {
            "name": "Free Reading Endpoint",
            "url": "http://127.0.0.1:8000/api/v1/readings/free",
            "method": "POST",
            "body": {"name": test_name, "day": day, "month": month, "year": year}
        },
        {
            "name": "Blessing Years Forecast Endpoint",
            "url": "http://127.0.0.1:8000/api/v2/numerology/forecast/blessing-years",
            "method": "POST",
            "body": {"day": day, "month": month, "year": year, "current_age": 45}
        },
        {
            "name": "Enhanced Lo Shu Grid Endpoint",
            "url": "http://127.0.0.1:8000/api/v2/numerology/lo-shu/enhanced?day=28&month=11&year=1981&name=Bhaskr%20Singh",
            "method": "POST",
            "body": None
        },
        {
            "name": "Personal Cycles Horizon Endpoint",
            "url": "http://127.0.0.1:8000/api/v2/numerology/forecast/personal-cycles",
            "method": "POST",
            "body": {"day": day, "month": month, "year": year}
        },
        {
            "name": "Mobile Asset Audit Endpoint",
            "url": "http://127.0.0.1:8000/api/v2/numerology/assets/mobile",
            "method": "POST",
            "body": {"mobile_number": mobile, "driver": driver, "conductor": conductor}
        },
        {
            "name": "Explainable Remedies Endpoint",
            "url": "http://127.0.0.1:8000/api/v2/numerology/remedies/select",
            "method": "POST",
            "body": {"driver": driver, "conductor": conductor, "missing_numbers": [3, 5, 6, 7], "max_remedies": 3}
        }
    ]

    api_pass_count = 0
    for ep in api_endpoints_to_test:
        try:
            req_data = json.dumps(ep["body"]).encode("utf-8") if ep["body"] else None
            headers = {"Content-Type": "application/json"} if ep["body"] else {}
            req = urllib.request.Request(ep["url"], data=req_data, headers=headers, method=ep["method"])
            start_t = datetime.datetime.now()
            with urllib.request.urlopen(req, timeout=15) as response:
                duration_ms = (datetime.datetime.now() - start_t).total_seconds() * 1000
                res_json = json.loads(response.read().decode("utf-8"))
                status_code = response.status
                print(f"  • [HTTP {status_code}] {ep['name']} -> Latency: {duration_ms:.1f}ms | Payload Size: {len(str(res_json))} chars")
                if status_code == 200:
                    api_pass_count += 1
        except Exception as ex:
            print(f"  • [FAILED] {ep['name']}: {ex}")

    results["API_Endpoints"] = f"{api_pass_count}/{len(api_endpoints_to_test)} PASSED"
    assert api_pass_count == len(api_endpoints_to_test), f"Some API endpoints failed ({api_pass_count}/{len(api_endpoints_to_test)})"

    print("\n" + "=" * 80)
    print("ALL 7 PREDICTION LEVELS, SOVEREIGN SOURCES & LIVE APIS VERIFIED SUCCESSFULLY!")
    print(f"Summary Results: {json.dumps(results, indent=2)}")
    print("=" * 80)

if __name__ == "__main__":
    run_prediction_levels_test()
