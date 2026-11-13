# Numeros Vision — Rollback & Incident Recovery Runbook
**Document Type:** Disaster Recovery Procedures

## 1. Incident Response
1. Identify failure layer: Calculation -> check `app/engine/`; RAG -> check `app/engine/rag_retriever.py`; Payment -> inspect `app/api/payments.py`.
2. Safe Version Pinning: If an evaluation model shows regression, roll back prompt version in `app/engine/question_explanation_engine.py` without touching calculation engines.
3. Database & Session Recovery: File stores (`verified_sessions.json`, `cdp_identities.json`) are backed up automatically to `data/backups/`.
