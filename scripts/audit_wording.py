import json
import re

with open('data/planner_2027_content_library.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

flagged = ['ensures', 'ensuring', 'earns', 'preserves', 'protect', 'protects', 'accelerates', 'guarantee', 'guarantees', 'guaranteed', 'always', 'definitely']
pattern = re.compile(rf'\b({"|".join(flagged)})\b', re.IGNORECASE)

def find_in_obj(obj, path=''):
    results = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            results.extend(find_in_obj(v, f'{path}.{k}' if path else k))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            results.extend(find_in_obj(item, f'{path}[{idx}]'))
    elif isinstance(obj, str):
        if pattern.search(obj):
            results.append((path, obj))
    return results

hits = find_in_obj(data)
print(f'Total field hits: {len(hits)}')
for path, text in hits:
    print(f'\nPATH: {path}')
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for s in sentences:
        if pattern.search(s):
            print(f'  SENTENCE: {s}')

print('\n=== ALL WELLBEING LINES ===')
for py, areas in sorted(data.get('personal_year_life_areas', {}).items(), key=lambda x: int(x[0])):
    print(f'PY {py}: {areas.get("wellbeing", "")}')
