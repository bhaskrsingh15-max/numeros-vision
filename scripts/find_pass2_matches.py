import json
import re

with open('data/planner_2027_content_library.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

flagged = [
    'prevents', 'brings', 'keeps', 'makes', 'creates', 'proves', 'builds',
    'guarantees', 'ensures', 'secures', 'peace of mind', 'mental peace',
    'highly productive', 'greatly', 'always'
]
pattern = re.compile(rf'\b({"|".join(re.escape(w) for w in flagged)})\b', re.IGNORECASE)

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
print(f"Total fields with matches: {len(hits)}")
for path, text in hits:
    print(f"\nPATH: {path}")
    sentences = re.split(r'(?<=[.!?])\s+', text)
    for s in sentences:
        if pattern.search(s):
            found_words = [w for w in flagged if re.search(rf'\b{re.escape(w)}\b', s, re.IGNORECASE)]
            print(f"  [{', '.join(found_words)}] {s}")
