import time
import re
from pathlib import Path
import json

CORPUS_FILE = Path("data/knowledge_base/numeros_vision_corpus.json")

with open(CORPUS_FILE, 'r', encoding='utf-8') as f:
    passages = json.load(f).get("passages", [])

print(f"Loaded {len(passages)} passages.")

# Build inverted index
t0 = time.time()
inverted_index = {}
for idx, p in enumerate(passages):
    words = set(re.findall(r'\w+', (p["content"] + " " + p["source"] + " " + p.get("location", "")).lower()))
    for w in words:
        if len(w) > 2 or w.isdigit():
            if w not in inverted_index:
                inverted_index[w] = []
            inverted_index[w].append(idx)
t1 = time.time()
print(f"Index built in {(t1-t0)*1000:.2f} ms with {len(inverted_index)} distinct terms.")

# Fast query using inverted index
def fast_query(query_str, top_k=3):
    keywords = [k.lower() for k in re.findall(r'\w+', query_str) if len(k) > 2 or k.isdigit()]
    if not keywords:
        return passages[:top_k]
    
    candidate_scores = {}
    for kw in keywords:
        matches = inverted_index.get(kw, [])
        for idx in matches:
            candidate_scores[idx] = candidate_scores.get(idx, 0) + 1
            
    if not candidate_scores:
        return passages[:top_k]
        
    top_indices = sorted(candidate_scores.keys(), key=lambda i: candidate_scores[i], reverse=True)[:top_k]
    return [passages[i] for i in top_indices]

# Test 10 queries
queries = [
    "Driver 6 Conductor 8 career business leadership",
    "Driver 1 Conductor 9 wealth and money timing 2026",
    "Missing numbers 4 5 6 Lo Shu grid balancing crystals",
    "Marriage compatibility driver 2 and driver 7",
    "Personal year 2026 Mahadasha Saturn transition"
]

total_ms = 0
for q in queries:
    t_start = time.time()
    res = fast_query(q, top_k=3)
    t_end = time.time()
    duration = (t_end - t_start) * 1000
    total_ms += duration
    print(f"Query: '{q[:30]}...' -> {duration:.2f} ms (Found {len(res)} matches)")

print(f"\nAverage fast query time: {total_ms/len(queries):.2f} ms!")
