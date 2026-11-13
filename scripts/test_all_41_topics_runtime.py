import os
import sys
import json
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Import engines
from app.engine.professional_numerology_engine import (
    audit_mobile_number,
    calculate_personal_cycles,
    calculate_kua,
    analyze_kua_and_directions,
    score_partner_compatibility,
    analyze_share_market_profile,
    get_bonus_query_solution
)
from app.engine.asset_numerology_engine import (
    analyze_vehicle_number,
    analyze_house_number
)
from app.engine.driver_conductor_81_engine import lookup_driver_conductor_81
from app.engine.enhanced_lo_shu_engine import analyze_grid_repetitions_and_missing
from app.engine.complementary_poorak_engine import evaluate_grid_complementary_support
from app.engine.five_elements_hygiene_engine import evaluate_five_elements_balance
from app.engine.profession_engine import calculate_profession_suitability
from app.engine.life_aspects_engine import (
    analyze_foreign_settlement_potential,
    analyze_health_vulnerabilities
)
from app.engine.name_balancing_engine import analyze_name_balance_detailed

print("All engines imported successfully! Testing executions...")

# 1. Mobile
m = audit_mobile_number("9818284560", driver=1)
print(f"[Topic 2 Mobile] Status: {m.get('status')}, Malefics: {[p['pair'] for p in m.get('malefic_pairs_found', [])]}")

# 2. Vehicle
v = analyze_vehicle_number("DL01AB1234", driver=1, conductor=5)
print(f"[Topic 4 Vehicle] Compound: {v.get('compound_sum')}, Root: {v.get('root_number')}, Compatible: {v.get('is_compatible')}")

# 3. House
h = analyze_house_number("Flat 402, Tower B", driver=1, conductor=5)
print(f"[Topic 4 House] Compound: {h.get('compound_sum')}, Root: {h.get('root_number')}")

# 4. 81 Combos
c81 = lookup_driver_conductor_81(1, 8)
print(f"[Topic 5 81 Combos] Driver 1 - Conductor 8: Rating={c81.get('star_rating')}, Relationship={c81.get('relationship_type')}")

# 5. Repetitive & Missing
grid_eval = analyze_grid_repetitions_and_missing([1, 1, 1, 5, 9])
print(f"[Topic 7 & 8 Repetitive/Missing] Repetitive: {list(grid_eval.get('repetitive_numbers', {}).keys())}, Missing: {grid_eval.get('missing_numbers', [])[:4]}")

# 6. Complementary Poorak
comp = evaluate_grid_complementary_support([1, 5, 9], driver=1, conductor=6)
print(f"[Topic 9 Complementary] Active supports: {len(comp.get('supported_qualities', []))}")

# 7. Five Elements
elem = evaluate_five_elements_balance([1, 5, 9])
print(f"[Topic 10 Five Elements] Weak elements: {elem.get('weak_or_missing_elements', [])}")

# 8. Kua & Directions
kua = analyze_kua_and_directions("male", 1990)
print(f"[Topic 11 & 36 Kua] Kua: {kua.get('kua_number')}, Group: {kua.get('kua_group')}, Success Dir: {kua.get('success_direction_sheng_chi')}")

# 9. Personal Cycles
pc = calculate_personal_cycles(15, 8)
print(f"[Topic 15, 16, 18, 19 Personal Cycles] PY: {pc.get('personal_year')}, PM: {pc.get('personal_month')}, PD: {pc.get('personal_day')}, UY: {pc.get('universal_year')}")

# 10. Partner Compatibility
part = score_partner_compatibility(1, 8, [1, 8], 8, 1, [8, 1])
print(f"[Topic 28 & 29 Partner Compatibility] Score: {part.get('score_pct')}%, Category: {part.get('category')}")

# 11. Share Market
sm = analyze_share_market_profile(5, 6)
print(f"[Topic 35 Share Market] Style: {sm.get('trading_style')}, Suitability: {sm.get('intraday_suitability')}")

# 12. Bonus Queries (Topic 26)
for q in ["silver_square", "child_conceive", "autism", "door_remedies", "blood"]:
    bq = get_bonus_query_solution(q)
    print(f"[Topic 26 Bonus - {q}] Solution Topic: {bq.get('topic')}")

# 13. Foreign Settlement
fs = analyze_foreign_settlement_potential([5, 6, 7], driver=5, conductor=6)
print(f"[Topic 30 Foreign Settlement] Likelihood: {fs.get('foreign_travel_likelihood')}")

# 14. Health Vulnerabilities
hv = analyze_health_vulnerabilities(driver=1, conductor=8, age=45)
print(f"[Topic 34b Health] Active Ruler: {hv.get('active_ruler')}, Organs: {hv.get('vulnerable_organs')[:2]}")

# 15. Name Balancing
nb = analyze_name_balance_detailed("Bhaskr Singh", driver=1, conductor=5)
print(f"[Topic 31-34 Name Balancing] Name Total: {nb.get('full_name_compound')}, Root: {nb.get('full_name_root')}, Balanced: {nb.get('is_balanced')}")

print("\n--- ALL TESTS COMPLETED SUCCESSFULLY ---")
