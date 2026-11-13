import sys
import json
import re
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

fp = r'data\uploaded_books_and_notes\Driver Conductor Destiny 81 Combinations PDF Planets In Astrology Planets.pdf'
reader = PdfReader(fp)

valid_compatibilities = [
    "Challenging / Karmic",
    "Strong / Balanced",
    "Very Strong",
    "Very Good",
    "Challenging",
    "Excellent",
    "Moderate",
    "Average",
    "Strong",
    "Good"
]

combinations = {}

for p_num, page in enumerate(reader.pages):
    txt = page.extract_text() or ''
    for line in txt.split('\n'):
        line_clean = line.strip()
        # Look for line starting with "D C Planet1 - Planet2"
        # e.g.: 9 2 Mars  –  Moon Emotional  intelligence,  diplomacy Moderate
        m = re.match(r'^([1-9])\s+([1-9])\s+([A-Za-z]+)\s*[\–\-]\s*([A-Za-z]+)\s+(.+)$', line_clean)
        if m:
            d, c, p1, p2, remainder = m.groups()
            d, c = int(d), int(c)
            remainder = re.sub(r'\s+', ' ', remainder).strip()
            
            # Find matching compatibility suffix
            matched_compat = None
            destiny_influence = remainder
            for vc in valid_compatibilities:
                if remainder.endswith(vc):
                    matched_compat = vc
                    destiny_influence = remainder[:-len(vc)].strip()
                    break
            
            combinations[f'{d}_{c}'] = {
                'driver': d,
                'conductor': c,
                'driver_planet': p1,
                'conductor_planet': p2,
                'planet_combination': f'{p1}-{p2}',
                'destiny_influence': destiny_influence,
                'compatibility': matched_compat or "Moderate",
                'source': 'SRC-81-DC-DESTINY-GUIDE',
                'source_page': p_num + 1,
                'rule_status': 'APPROVED'
            }

print(f'Cleanly parsed {len(combinations)} / 81 combinations!')
print('Sample 9_2:', combinations.get('9_2'))
print('Sample 9_8:', combinations.get('9_8'))
print('Sample 1_1:', combinations.get('1_1'))

out_fp = r'data\knowledge_base\driver_conductor_81_rules.json'
with open(out_fp, 'w', encoding='utf-8') as f:
    json.dump(combinations, f, indent=2, ensure_ascii=False)

print(f'Saved to {out_fp}')
