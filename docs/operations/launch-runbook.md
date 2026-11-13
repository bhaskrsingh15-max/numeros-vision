# Numeros Vision — Production Launch Runbook
**Document Type:** Operational Procedures

## 1. Service Verification Checklist
1. Virtual environment active: `.\.venv\Scripts\python.exe`.
2. Uvicorn service running on `http://127.0.0.1:8000`.
3. Tunnels operational (Cloudflare & SSH supervisor daemons).
4. Automated unit tests passing: 169/169 (`100% OK`).
5. Complete audit QC script passing: 109/109 (`100% OK`).
6. Zero hallucination check confirmed on RAG retriever.
