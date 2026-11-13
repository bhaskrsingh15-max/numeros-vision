import os

terms = [
    'Constitutional Architecture & Synergy Matrix',
    'Non-Negotiable Panch Tattva Bodyguard Hygiene',
    'Birth Sub-Date',
    'Tier 1: Career Momentum Takeaway',
    'Planetary Root Cause'
]

for root, _, files in os.walk('app'):
    for f in files:
        if f.endswith('.py'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                text = fp.read()
            for t in terms:
                if t.lower() in text.lower():
                    print(f'{p}: contains "{t}"')
