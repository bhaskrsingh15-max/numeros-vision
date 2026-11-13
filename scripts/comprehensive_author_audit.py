import sys
import os
import re

sys.stdout.reconfigure(encoding='utf-8')

all_authors = [
    'umang taneja', 'umang', 'taneja',
    'gautam verma',
    'chaitanyaa misra', 'chaitanyaa', 'chaitanya misra',
    'harish johari', 'johari',
    'vijaya kumar',
    'linda goodman',
    'matthew oliver goodwin', 'matthew oliver', 'goodwin',
    'hans decoz', 'decoz',
    'faith javane', 'javane',
    'dusty bunker', 'bunker',
    'sepharial',
    'florence campbell', 'campbell',
    'richard webster', 'webster',
    'eric temple bell', 'e.t. bell',
    'vincent lopez', 'mark crawford',
    'kpastrologer',
    'yoga mantra',
    'accurate predictive methodology',
    'fortune through your name',
    'meaning and magic of numbers',
    'numbers their meaning and magic',
    'the magic of numbers',
    'chinese numerology 1998',
    'cheiro'
]

targets = ['app', 'data', 'docs', 'dist_cloudflare_pages', 'scripts']
found = {}

for target in targets:
    if not os.path.exists(target):
        continue
    for root, dirs, files in os.walk(target):
        if any(x in root for x in ['.git', '__pycache__', 'node_modules', '.pytest_cache']):
            continue
        for file in files:
            if file.endswith(('.py', '.js', '.html', '.json', '.md', '.csv', '.txt', '.yaml', '.yml')):
                p = os.path.join(root, file)
                try:
                    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
                        text = f.read()
                    for author in all_authors:
                        matches = len(re.findall(r'\b' + re.escape(author) + r'\b', text, re.I))
                        if matches > 0:
                            if author not in found:
                                found[author] = []
                            found[author].append((p, matches))
                except Exception as e:
                    pass

for a in sorted(found.keys()):
    files = found[a]
    total_matches = sum(c for _, c in files)
    print(f'AUTHOR/SOURCE: "{a}" -> {total_matches} matches in {len(files)} files')
    for p, c in files[:6]:
        print(f'   {p} ({c})')
    if len(files) > 6:
        print(f'   ... and {len(files)-6} more')
