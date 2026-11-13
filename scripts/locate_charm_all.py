import os

terms = [
    'Career Momentum Takeaway',
    'Planetary Root Cause',
    'Consensus Matrix',
    'WATER ELEMENT ( NORTH )',
    'Tier 1:'
]

for root, _, files in os.walk('.'):
    if any(x in root for x in ['.git', '__pycache__', 'node_modules']):
        continue
    for f in files:
        if f.endswith(('.py', '.json', '.md', '.js')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    text = fp.read()
                for t in terms:
                    if t.lower() in text.lower():
                        print(f'{p}: contains "{t}"')
            except:
                pass
