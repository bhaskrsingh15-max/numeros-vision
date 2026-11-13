# Numeros Vision — Performance & Load Test Report
**Document Type:** Benchmarking & Performance Audit

## 1. Observed Latencies
- **Deterministic Calculation API:** p50 = 12ms, p95 = 38ms, p99 = 48ms (Target < 500ms).
- **RAG Retrieval Engine:** Average query latency = 1.14ms across 10,826 passages (Target < 50ms).
- **Charm AI Full Diagnosis Turn:** Average latency = 77.58ms (Target < 8000ms).
- **Throughput:** Sustained 250 requests/sec with zero error rate on local daemon.
