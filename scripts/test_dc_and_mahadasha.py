import sys
import json
sys.stdout.reconfigure(encoding='utf-8')
from app.engine.rule_governance import rule_governance

dc = rule_governance.get_driver_conductor_combination(9, 2)
print('=== DRIVER 9 + CONDUCTOR 2 ===')
print(json.dumps(dc, indent=2))

md = rule_governance.calculate_numerological_mahadasha('18-10-1990', 2026)
print('\n=== NUMEROLOGICAL MAHADASHA (18-10-1990) ===')
print('King Driver Number:', md['king_driver_number'], f"({md['king_planet']})")
print('Active Mahadasha for 2026:', json.dumps(md['current_active_mahadasha'], indent=2))
print('Total periods generated:', len(md['periods']))
for p in md['periods']:
    mark = ' [ACTIVE]' if p['is_current_active'] else ''
    print(f" - Cycle {p['cycle_index']}: {p['planet']} (Number {p['number']}) | {p['duration_years']} yrs | {p['start_date']} to {p['end_date']}{mark}")
