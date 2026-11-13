import os, re, sys

sys.stdout.reconfigure(encoding='utf-8')

phrases = [
    'Private Limited',
    'Pvt Ltd',
    'Pvt.',
    'zero physical address',
    'Legal & Data Privacy Counsel',
    'malicious complaints',
    'stock market trading',
    'Foreign Visa & PR',
    'Child Conception & Progeny',
    'Wealth Obstacles & Debt Relief',
    'Clear Obstacles Everywhere',
    'Prescription',
    'cures',
    'Mathematical Proofs',
    'RECOMMENDED BY MASTERS',
    'NANO BANANA',
    'Classical Calculation Precisionematical calculations',
    'sealing your energetic alignment',
    'whichever is lower'
]

html_files = []
for root, dirs, files in os.walk('app/static'):
    for f in files:
        if f.endswith('.html') and not f.endswith('_backup'):
            html_files.append(os.path.join(root, f))

print(f'Scanning {len(html_files)} HTML files for audit risk phrases...\n')
for p in sorted(html_files):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    found = []
    for ph in phrases:
        matches = len(re.findall(re.escape(ph), content, re.IGNORECASE))
        if matches > 0:
            found.append(f'{ph}({matches})')
    if found:
        print(f'{p}: {", ".join(found)}')

print('\nScanning app .js, .py, .json files...')
for root, dirs, files in os.walk('app'):
    for f in files:
        if f.endswith(('.js', '.py', '.json')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fl:
                content = fl.read()
            found = [ph for ph in phrases if re.search(re.escape(ph), content, re.IGNORECASE)]
            if found:
                print(f'{p}: {", ".join(found)}')
