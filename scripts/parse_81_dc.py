import os
import sys
import json
import re
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

fp = r'data\uploaded_books_and_notes\Driver Conductor Destiny 81 Combinations PDF Planets In Astrology Planets.pdf'
reader = PdfReader(fp)
print(f'Total pages: {len(reader.pages)}')

combinations = {}

for p_num, page in enumerate(reader.pages):
    txt = page.extract_text() or ''
    lines = [l.strip() for l in txt.split('\n') if l.strip()]
    for line in lines:
        # Match pattern: D C Planet1 – Planet2 Influence Compatibility
        # e.g.: 1 1 Sun – Sun Leadership, authority, independence Very Strong
        m = re.match(r'^([1-9])\s+([1-9])\s+([A-Za-z]+)\s*[\–\-]\s*([A-Za-z]+)\s+(.+?)\s+([A-Za-z\s/]+)$', line)
        if m:
            d, c, p1, p2, influence, compat = m.groups()
            d, c = int(d), int(c)
            combinations[f'{d}_{c}'] = {
                'driver': d,
                'conductor': c,
                'driver_planet': p1,
                'conductor_planet': p2,
                'planet_combination': f'{p1}-{p2}',
                'destiny_influence': influence.strip(),
                'compatibility': compat.strip(),
                'source': 'SRC-81-DC-DESTINY-GUIDE',
                'source_page': p_num + 1,
                'rule_status': 'APPROVED'
            }

print(f'Successfully parsed {len(combinations)} / 81 combinations directly with regex!')

# If any are missing due to line wrap, let's parse robustly
if len(combinations) < 81:
    print('Checking for unparsed combinations...')
    for d in range(1, 10):
        for c in range(1, 10):
            k = f'{d}_{c}'
            if k not in combinations:
                print(f'Missing: D={d}, C={c}')

out_fp = r'data\knowledge_base\driver_conductor_81_rules.json'
with open(out_fp, 'w', encoding='utf-8') as f:
    json.dump(combinations, f, indent=2, ensure_ascii=False)

print(f'Saved to {out_fp}')
