import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/css/roadmap_components.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines[:120]):
    print(f'{i+1}: {line}', end='')
