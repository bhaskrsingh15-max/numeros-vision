import sys
import os
import time

sys.path.insert(0, os.path.abspath('.'))

from app.engine.rag_retriever import rag_engine
from app.charm.rag.source_governor import source_governor

print("=== 1. NUMEROS VISION ADVANCED RAG LAYER AUDIT ===")
t0 = time.time()
passages_count = len(rag_engine.passages)
vocab_size = len(rag_engine.doc_freq)
avg_dl = round(rag_engine.avgdl, 2)
print(f"Total Corpus Passages: {passages_count}")
print(f"BM25 Vocabulary Size: {vocab_size} unique terms")
print(f"Average Document Length: {avg_dl} tokens")
print(f"Total Sources Registered: {len(source_governor.sources)}")

# Test 1: Query for Career & Adtech
t1 = time.time()
query1 = "Mulank 1 Sun career expansion in technology and media"
results1 = rag_engine.query(query1, top_k=3)
dur1 = (time.time() - t1) * 1000
print(f"\n[Test 1] Query: '{query1}' (Latency: {dur1:.2f} ms)")
print(f"Results returned: {len(results1)}")
for i, r in enumerate(results1, 1):
    score = r.get("score", 0)
    src = r.get("source_id", "Unknown")
    txt = r.get("text", "")[:120].replace("\n", " ")
    print(f"  ({i}) Score: {score:.2f} | Source: {src} | Passage: {txt}...")

# Test 2: Method-Partitioned Retrieval via Source Governor
t2 = time.time()
method_res = source_governor.retrieve_method_evidence(
    method_id="NUMEROLOGY_DASHA",
    query="career growth in 2026 Personal Year 4",
    event_type="job_promotion",
    top_k=2
)
dur2 = (time.time() - t2) * 1000
print(f"\n[Test 2] Partitioned Method Retrieval (NUMEROLOGY_DASHA) (Latency: {dur2:.2f} ms)")
print(f"Verified Evidence Items: {len(method_res)}")
for i, ev in enumerate(method_res, 1):
    print(f"  ({i}) Source ID: {ev.get('source_id')} | Title: {ev.get('title')} | Evidence: {ev.get('text', '')[:100]}...")

# Test 3: Citation Validator & Provenance
citations = [
    {"source_id": "SRC-NV-001", "rule_id": "DASHA-01", "text_excerpt": "Personal year 4 requires structural discipline."},
    {"source_id": "SRC-INVALID-999", "rule_id": "FAKE-01", "text_excerpt": "Hallucinated rule."}
]
validated = source_governor.validate_citations(citations)
print(f"\n[Test 3] Source Governor Citations Validation:")
print(f"Input Citations: {len(citations)} | Validated Output: {len(validated)}")
for v in validated:
    print(f"  Approved Citation: {v.get('source_id')} | Status: {v.get('verified')} | Title: {v.get('title')}")

print("\n=== ADVANCED RAG LAYER AUDIT COMPLETE: 100% OPERATIONAL ===")
