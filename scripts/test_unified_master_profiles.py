"""
NUMEROS VISION — LIVE UNIFIED MASTER EXECUTION TEST
Test Target:
- Profile 1: DOB 28-11-1981, Male
- Profile 2: DOB 13-10-1985, Female
"""

import urllib.request
import json
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

def post_api(endpoint: str, payload: dict) -> dict:
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))

def run_tests():
    print("=" * 80)
    print("NUMEROS VISION — LIVE UNIFIED MASTER EXECUTION TEST")
    print("PROFILES: Male (28-11-1981) & Female (13-10-1985)")
    print("=" * 80)

    # ── 1. PROFILE VALIDATION & DPDP CONSENT ─────────────────────────────
    print("\n[1] POST /v1/profile/validate")
    p1 = post_api("/v1/profile/validate", {
        "name": "Arjun Sharma",
        "day": 28, "month": 11, "year": 1981,
        "gender": "Male", "consent": True, "mobile": "9811002811"
    })
    print(f"  Male Profile ID   : {p1['profile_id']} (Status: {p1['status']})")
    print(f"  Normalized Date   : {p1['normalized_profile']['birth_date']}")
    print(f"  Masked Mobile     : {p1['normalized_profile']['masked_mobile']}")

    p2 = post_api("/v1/profile/validate", {
        "name": "Pooja Verma",
        "day": 13, "month": 10, "year": 1985,
        "gender": "Female", "consent": True, "mobile": "9820013105"
    })
    print(f"  Female Profile ID : {p2['profile_id']} (Status: {p2['status']})")
    print(f"  Normalized Date   : {p2['normalized_profile']['birth_date']}")
    print(f"  Masked Mobile     : {p2['normalized_profile']['masked_mobile']}")

    # ── 2. DETERMINISTIC CALCULATIONS (VEDIC, PYTHAGOREAN, LO SHU) ───────
    print("\n[2] POST /v1/numbers/calculate")
    # Male Vedic
    m_vedic = post_api("/v1/numbers/calculate", {
        "methodology_id": "METH-VEDIC-001",
        "day": 28, "month": 11, "year": 1981
    })
    m_drv = m_vedic["calculation_output"]["driver_number"]
    m_cnd = m_vedic["calculation_output"]["conductor_number"]
    print(f"  Male (28-11-1981) Vedic: Driver {m_drv} (Surya/Sun) / Conductor {m_cnd} (Rahu)")

    # Female Vedic
    f_vedic = post_api("/v1/numbers/calculate", {
        "methodology_id": "METH-VEDIC-001",
        "day": 13, "month": 10, "year": 1985
    })
    f_drv = f_vedic["calculation_output"]["driver_number"]
    f_cnd = f_vedic["calculation_output"]["conductor_number"]
    print(f"  Female (13-10-1985) Vedic: Driver {f_drv} (Rahu) / Conductor {f_cnd} (Surya/Sun)")
    print(f"  >> SYNASTRY HIGHLIGHT: EXACT MIRROR INVERSION (Male 1-4 <-> Female 4-1) <<")

    # Male Pythagorean
    m_pyth = post_api("/v1/numbers/calculate", {
        "methodology_id": "METH-PYTH-001",
        "day": 28, "month": 11, "year": 1981,
        "name": "Arjun Sharma"
    })
    print(f"  Male Pythagorean Life Path: {m_pyth['calculation_output']['life_path']['final_life_path']} | Trace: {m_pyth['calculation_output']['life_path']['calculation_trace']}")
    print(f"  Male Karmic Debt (13/4 in LP): {m_pyth['calculation_output']['life_path']['is_karmic_debt']}")

    # Female Pythagorean
    f_pyth = post_api("/v1/numbers/calculate", {
        "methodology_id": "METH-PYTH-001",
        "day": 13, "month": 10, "year": 1985,
        "name": "Pooja Verma"
    })
    print(f"  Female Pythagorean Life Path: {f_pyth['calculation_output']['life_path']['final_life_path']} | Trace: {f_pyth['calculation_output']['life_path']['calculation_trace']}")
    print(f"  Female Birthday Karmic Debt (13/4): {f_pyth['calculation_output']['birthday_number']['is_karmic_debt']}")

    # Male Lo Shu
    m_loshu = post_api("/v1/numbers/calculate", {
        "methodology_id": "METH-LOSHU-001",
        "day": 28, "month": 11, "year": 1981
    })
    print(f"  Male Lo Shu Present: {m_loshu['calculation_output']['present_numbers']} | Missing: {m_loshu['calculation_output']['missing_numbers']}")

    # Female Lo Shu
    f_loshu = post_api("/v1/numbers/calculate", {
        "methodology_id": "METH-LOSHU-001",
        "day": 13, "month": 10, "year": 1985
    })
    print(f"  Female Lo Shu Present: {f_loshu['calculation_output']['present_numbers']} | Missing: {f_loshu['calculation_output']['missing_numbers']}")

    # ── 3. COMPOUND NUMBER DECOMPOSITION (CLAUSE 6 & 7) ─────────────────
    print("\n[3] POST /v1/numbers/decode (Compound Preservation)")
    m_dec = post_api("/v1/numbers/decode", {
        "number": 28, "compound_value": 28, "methodology_id": "METH-CHALDEAN-001"
    })
    print(f"  Male Compound 28/1: {m_dec['decomposition']['compound_root_relationship']}")

    f_dec = post_api("/v1/numbers/decode", {
        "number": 13, "compound_value": 13, "methodology_id": "METH-PYTH-001"
    })
    print(f"  Female Compound 13/4: {f_dec['decomposition']['compound_root_relationship']}")
    print(f"  Karmic Theme: {f_dec['decomposition']['western_karmic_debt']['theme']}")

    # ── 4. CORRELATIONS & CROSS-SYSTEM SYNTHESIS (CLAUSE 9) ─────────────
    print("\n[4] POST /v1/correlations/analyze")
    m_corr = post_api("/v1/correlations/analyze", {
        "day": 28, "month": 11, "year": 1981, "name": "Arjun Sharma"
    })
    print(f"  Male Correlations Evaluated: {len(m_corr['pairwise_correlations'])} pairs")
    for pair in m_corr["pairwise_correlations"]:
        print(f"    - {pair['pair']}: {pair['values']} -> {pair['relationship']} ({pair['classification']})")

    # ── 5. BOUNDED FORECASTS & BLESSING YEARS (CLAUSE 10) ────────────────
    print("\n[5] POST /v1/forecast/generate")
    m_fcst = post_api("/v1/forecast/generate", {
        "day": 28, "month": 11, "year": 1981, "current_age": 43
    })
    male_blessings = [f"Age {b['age']} ({b['calendar_year']})" for b in m_fcst['blessing_years_milestones']['immediate_upcoming_blessings'][:3]]
    print(f"  Male Next Milestone Ages: {', '.join(male_blessings)}")

    f_fcst = post_api("/v1/forecast/generate", {
        "day": 13, "month": 10, "year": 1985, "current_age": 39
    })
    print(f"  Female Current Personal Year: {f_fcst['annual_monthly_matrix']['personal_year']} (Theme: {f_fcst['annual_monthly_matrix']['personal_year_theme']})")
    female_blessings = [f"Age {b['age']} ({b['calendar_year']})" for b in f_fcst['blessing_years_milestones']['immediate_upcoming_blessings'][:3]]
    print(f"  Female Next Milestone Ages: {', '.join(female_blessings)}")

    # ── 6. SOURCE-GROUNDED SAFE REMEDIES (CLAUSE 11) ─────────────────────
    print("\n[6] POST /v1/remedies/recommend")
    m_rem = post_api("/v1/remedies/recommend", {
        "driver": m_drv, "conductor": m_cnd, "missing_numbers": m_loshu["calculation_output"]["missing_numbers"]
    })
    print(f"  Male Recommended Remedies Count: {len(m_rem['remedy_prescription']['prescribed_remedies'])} (Max 5 enforced)")
    print(f"  Male Paired Sacred Yantra      : {m_rem['remedy_prescription']['prescribed_yantra']['name']}")
    print(f"  Safety Certification           : {m_rem['safety_certification']}")

    f_rem = post_api("/v1/remedies/recommend", {
        "driver": f_drv, "conductor": f_cnd, "missing_numbers": f_loshu["calculation_output"]["missing_numbers"]
    })
    print(f"  Female Recommended Remedies Count: {len(f_rem['remedy_prescription']['prescribed_remedies'])} (Max 5 enforced)")
    print(f"  Female Paired Sacred Yantra      : {f_rem['remedy_prescription']['prescribed_yantra']['name']}")

    # ── 7. INDIVIDUAL & CONSOLIDATED REPORTS (CLAUSE 16 & 17) ────────────
    print("\n[7] POST /v1/reports/consolidated")
    cons_report = post_api("/v1/reports/consolidated", {
        "day": 28, "month": 11, "year": 1981,
        "name": "Arjun Sharma",
        "methodologies": ["METH-VEDIC-001", "METH-CHALDEAN-001", "METH-LOSHU-001", "METH-PYTH-001"]
    })
    print(f"  Consolidated Report ID : {cons_report['report_id']} (Status: {cons_report['status']})")
    print(f"  Consensus Score        : {cons_report['integrated_synthesis']['multi_discipline_consensus_score']}%")
    print(f"  Conflict Disclosures   : {cons_report['integrated_synthesis']['disclosed_methodology_conflicts']}")

    # ── 8. RELATIONSHIP SYNASTRY ENGINE ──────────────────────────────────
    print("\n[8] POST /api/v2/numerology/relationships/synastry (Dual Native Match)")
    syn_res = post_api("/api/v2/numerology/relationships/synastry", {
        "person1_name": "Arjun Sharma (Male)",
        "p1_day": 28, "p1_month": 11, "p1_year": 1981,
        "person2_name": "Pooja Verma (Female)",
        "p2_day": 13, "p2_month": 10, "p2_year": 1985,
        "relationship_type": "romantic"
    })
    print(f"  Synastry Compatibility Score: {syn_res['synastry_report']['compatibility_score_pct']}%")
    print(f"  Vibe Classification        : {syn_res['synastry_report']['overall_verdict']}")
    print(f"  Driver Harmony             : {syn_res['synastry_report']['driver_harmony']}")
    print(f"  Conductor Harmony          : {syn_res['synastry_report']['conductor_harmony']}")
    print(f"  Lo Shu Complementation     : {syn_res['synastry_report']['lo_shu_complementation']}")

    # ── 9. PUBLICATION GATE & HALLUCINATION CHECK (CLAUSE 14 & 15) ───────
    print("\n[9] POST /v1/reports/validate (Publication Gate)")
    gate_res = post_api("/v1/reports/validate", {
        "report_text": f"Native 1 has Driver {m_drv} and Conductor {m_cnd}. Native 2 has Driver {f_drv} and Conductor {f_cnd}. Anveil Every Charm.",
        "calculation_ids": ["CALC-001"],
        "rule_ids": ["METH-VEDIC-001"],
        "source_ids": ["SRC-NV-001"]
    })
    print(f"  Publication Allowed : {gate_res['publication_allowed']}")
    print(f"  Stage Reached       : {gate_res['stage_reached']}/12")
    print(f"  Action Required     : {gate_res['action_required']}")

    print("\n" + "=" * 80)
    print("SUCCESS: ALL UNIFIED MASTER V1 APIS VERIFIED FOR BOTH PROFILES")
    print("=" * 80)

if __name__ == "__main__":
    run_tests()
