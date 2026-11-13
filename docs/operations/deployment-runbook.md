# Numeros Vision - Production Deployment Runbook
**Specification Reference**: `NUMEROS_VISION_MASTER_IMPLEMENTATION.md` (Sections 18–21)  
**Brand Identity**: Numeros Vision | *Unveil Every Charm*  
**Date**: October 2026  
**Status**: APPROVED - PRODUCTION OPERATIONS

---

## 1. Overview & Architecture Staging

This runbook specifies the step-by-step procedures for deploying changes to the **Numeros Vision** platform across Staging and Production environments.

### System Stack:
- **Framework**: FastAPI (Asynchronous Python 3.11+)
- **Server Gateway**: Uvicorn ASGI Daemon
- **Frontend**: SSR Jinja2 Templates + Vanilla Modular ES6 JavaScript + Shared Design System CSS
- **Data Stores**: SQLite (WAL Mode) + JSON Knowledge Graph Indexes
- **RAG Retrieval Engine**: Inverted Index BM25 Retriever with In-Memory LRU Cache
- **Payment Gateway**: Razorpay (HMAC-SHA256 signature verification)
- **Static Assets & CDN**: Local / static file serving with gzip compression & cache headers

---

## 2. Pre-Deployment Verification Checklist

Before deploying any release tag:
- [ ] Working tree clean (`git status` shows no uncommitted files).
- [ ] All unit, integration, and cyber defense tests pass:
  ```powershell
  .\.venv\Scripts\pytest tests/ -v
  ```
- [ ] Golden calculation outputs match known records (`tests/test_golden_calculations.py`).
- [ ] Pre-flight backup checkpoint created in `backups/checkpoint_<timestamp>`.
- [ ] Static assets minified and CSS design tokens verified (zero `#000000`, Venus Pearl `#FFFDF7` base).

---

## 3. Standard Deployment Procedure

### Step 1: Create Pre-Deployment Checkpoint
```powershell
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$CHECKPOINT_DIR = "backups/checkpoint_$TIMESTAMP"
New-Item -ItemType Directory -Path $CHECKPOINT_DIR -Force
Copy-Item "data/numeros_vision.db" "$CHECKPOINT_DIR/numeros_vision.db" -Force -ErrorAction SilentlyContinue
Copy-Item "data/rag_index.json" "$CHECKPOINT_DIR/rag_index.json" -Force -ErrorAction SilentlyContinue
git tag -a "release-$TIMESTAMP" -m "Automated release tag $TIMESTAMP"
```

### Step 2: Ingest Updated Configuration & Re-index RAG
```powershell
.\.venv\Scripts\python.exe scripts/parse_seo_registry.py
.\.venv\Scripts\python.exe -c "from app.services.rag_retriever import rag_retriever; print(f'Index loaded: {len(rag_retriever.index)} terms')"
```

### Step 3: Gracefully Reload Application Daemon
```powershell
# Identify running Uvicorn process
$proc = Get-Process -Name "python" -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like "*uvicorn*" }
if ($proc) {
    Stop-Process -Id $proc.Id -Force
    Start-Sleep -Seconds 1
}

# Launch refreshed daemon
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000" -NoNewWindow
Start-Sleep -Seconds 3
```

### Step 4: Execute Post-Deployment Smoke Probes
```powershell
.\.venv\Scripts\pytest tests/test_live_urls.py tests/test_charm_ai_perf_and_ui.py -v
```

---

## 4. Emergency Failover & Abort Protocol

If any smoke test fails:
1. Immediately kill the new process.
2. Revert to `$CHECKPOINT_DIR`:
   ```powershell
   git checkout tags/release-pre-$TIMESTAMP --force
   ```
3. Restart daemon using prior release assets.
4. Notify Engineering Lead and log post-incident report.

---
*Verified and Certified for Numeros Vision Infrastructure.*
