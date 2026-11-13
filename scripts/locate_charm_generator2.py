import os

terms = [
    'Tier 1: Career Momentum Takeaway',
    'Planetary Root Cause',
    'Numerology Dasha Career Timing & Consensus Matrix',
    'WATER ELEMENT ( NORTH ) CAREER'
]

for root, _, files in os.walk('app'):
    for f in files:
        if f.endswith(('.py', '.json', '.md')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                text = fp.read()
            for t in terms:
                if t.lower() in text.lower():
                    print(f'{p}: contains "{t}"')
