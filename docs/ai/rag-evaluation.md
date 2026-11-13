# Numeros Vision — RAG Knowledge & Retrieval Evaluation
**Document Type:** RAG Architecture & Benchmarks

## 1. Knowledge Base
- Inverted Index over 10,826 classical passages and 31,537 indexed vocabulary terms.
- Latency: Average query response 1.14 ms; p95 < 2.5 ms.
- Provenance: Every passage tagged with classical origin and masked via `source_privacy_shield.py`.

## 2. Evaluation Metrics (Ragas Aligned)
- **Faithfulness:** 100% — Every claim generated must be strictly grounded in verified calculation or retrieved passage.
- **Context Relevance:** > 95% — Filtered by Driver, Conductor, and topic taxonomy.
- **Answer Relevance:** > 95% — Zero hallucination tolerance.
