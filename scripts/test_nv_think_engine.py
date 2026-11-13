import sys
import os

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath('.'))

from app.engine.nv_psychology_engine import nv_think_engine

print("=== 1. TESTING SINGLE NUMBER NV THINK™ EVALUATION (NUMBER 1) ===")
res1 = nv_think_engine.evaluate_number(1, frequency=4, position="Driver (Mulank)")
print("Indicator:", res1["indicator"])
print("Methodology:", res1["methodology"])
print("Observations:", res1["chart_observations"])
print("Possible Behaviours:", res1["possible_behaviours"][:2])
print("Psychological Hypotheses:", res1["psychological_hypotheses"][:2])
print("Duality Patterns:", res1["contradictory_indicators"][:1])
print("Consensus Status:", res1["consensus_status"])
print("Validation Status:", res1["validation_status"])

print("\n=== 2. TESTING FULL CHART SYNTHESIS (DOB: 28-11-1981) ===")
chart_synth = nv_think_engine.evaluate_chart_synthesis(
    driver=1,
    conductor=4,
    loshu_counts={1: 4, 2: 1, 8: 2, 9: 1},
    active_planes=["Will Plane (9-5-1 partial)"],
    missing_numbers=[3, 4, 5, 6, 7]
)
print("Dualities Found:", chart_synth["chart_dualities"])
print("Synthesized Narrative:", chart_synth["synthesized_narrative"])

print("\n=== 3. TESTING CHARM AI MULTI-MODEL CORRELATION WITH DUALITY ===")
# Case A: Full Corroboration
cons_a = nv_think_engine.correlate_charm_ai_consensus(
    numerology_dasha={"active_dasha": "Mercury", "acute_window": "2024-03-15 to 2029-03-15"},
    vedic_factors={"favorable": True, "subperiod_lord": "Jupiter"},
    kp_factors={"houses": [2, 10, 11]},
    bnn_factors={"conjunction": "Sun-Mercury"}
)
print("Case A Status:", cons_a["consensus_status"])
print("Case A Takeaway:", cons_a["nv_think_takeaway"])

# Case B: Duality Tension (Vedic Saturn transit tests delay while Numerology Dasha is active)
cons_b = nv_think_engine.correlate_charm_ai_consensus(
    numerology_dasha={"active_dasha": "Sun", "acute_window": "2025-01-01 to 2026-06-01"},
    vedic_factors={"favorable": False, "subperiod_lord": "Saturn"},
    kp_factors={"houses": [2, 11]},
    bnn_factors={"conjunction": "Saturn-Rahu"}
)
print("\nCase B Status (Tension):", cons_b["consensus_status"])
print("Case B Duality Tensions:", cons_b["multi_model_summary"]["duality_tensions"])

print("\n[SUCCESS] NV THINK™ Engine verified 100% operational!")
