# Numeros Vision - Master Rollback & Disaster Recovery Plan
**Specification Reference**: `NUMEROS_VISION_MASTER_IMPLEMENTATION.md` (Sections 1, 20, 23)  
**Brand Identity**: Numeros Vision | *Unveil Every Charm*  
**Date**: October 2026  
**Status**: APPROVED - OPERATIONAL RUNBOOK

---

## 1. Overview & Objectives

This document establishes the official rollback, disaster recovery, and fail-safe protocols for the **Numeros Vision** production and staging environments.

The primary objective is to guarantee **zero data loss**, **uninterrupted calculation integrity**, and an **RTO (Recovery Time Objective) of < 3 minutes** with an **RPO (Recovery Point Objective) of < 15 minutes** in the event of an operational anomaly, regression, or deployment incident.

---

## 2. Rollback Triggers & Severity Thresholds

An immediate automated or manual rollback must be initiated if any of the following critical conditions occur during or immediately following deployment:

| Trigger Code | Description | Threshold | Action Level |
|:---|:---|:---|:---:|
| **TRG-01** | Calculation Divergence | Any mismatch against Golden Numerology Records in production health check. | **IMMEDIATE ROLLBACK** |
| **TRG-02** | Payment Webhook Failure | $> 0$ unverified payments processed or HMAC verification failure on valid webhook. | **IMMEDIATE ROLLBACK** |
| **TRG-03** | Service Error Rate | HTTP 5xx error rate exceeds $0.5\%$ over a 3-minute sliding window. | **IMMEDIATE ROLLBACK** |
| **TRG-04** | AI Response Latency | P95 latency on `/api/v1/charm-ai/predict` exceeds $500\text{ms}$ or RAG service crashes. | **FAILOVER TO DETERMINISTIC CACHE** |
| **TRG-05** | Cyber Defense Degradation | WAF bypass detected or false-positive rate on legitimate users exceeds $1\%$. | **HOTFIX / REVERT WAF RULE** |
| **TRG-06** | Critical SEO Ingestion Defect | 404 errors on canonical URLs or missing Schema.org JSON-LD across $> 5$ pages. | **REVERT SITEMAP / CONTENT BINDINGS** |

---

## 3. Pre-Deployment Checkpoint Protocol

Before executing any deployment, migration, or major configuration change, the deployment pipeline or engineer must execute the automated pre-flight checkpoint script:

```powershell
# Pre-deployment snapshot command
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$CHECKPOINT_DIR = "backups/checkpoint_$TIMESTAMP"
New-Item -ItemType Directory -Path $CHECKPOINT_DIR -Force

# 1. Backup Database
Copy-Item "data/numeros_vision.db" "$CHECKPOINT_DIR/numeros_vision.db" -Force

# 2. Backup Inverted Index & Cache
Copy-Item "data/rag_index.json" "$CHECKPOINT_DIR/rag_index.json" -Force

# 3. Create Git Release Tag
$GIT_TAG = "release-pre-$TIMESTAMP"
git tag -a $GIT_TAG -m "Pre-deployment checkpoint before release $TIMESTAMP"

Write-Host "Checkpoint $CHECKPOINT_DIR created successfully with tag $GIT_TAG"
```

---

## 4. Subsystem Rollback Procedures

### 4.1 Application Code & Server Runtime
If a regression is identified in backend route handlers or middleware:
1. **Stop Application Daemon**:
   ```powershell
   Get-Process -Name "python" | Where-Object { $_.CommandLine -like "*uvicorn*" } | Stop-Process -Force
   ```
2. **Revert Git Working Tree to Pre-Release Tag**:
   ```powershell
   git checkout tags/$GIT_TAG --force
   ```
3. **Restart Application Daemon**:
   ```powershell
   Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m uvicorn app.main:app --host 127.0.0.1 --port 8000" -NoNewWindow
   ```
4. **Execute Post-Rollback Health Probe**:
   ```powershell
   Invoke-RestMethod -Uri "http://127.0.0.1:8000/health"
   ```

---

### 4.2 Database & Transactional State
If database corruption or schema migration failure occurs:
1. **Quiesce Database Writes**: Temporarily route `/api/v1/calculate` to in-memory read-only mode.
2. **Restore Database from Checkpoint**:
   ```powershell
   Copy-Item "$CHECKPOINT_DIR/numeros_vision.db" "data/numeros_vision.db" -Force
   ```
3. **Replay Unprocessed Razorpay Webhooks**:
   Query Razorpay API for all payments captured between `$TIMESTAMP` and current time, executing idempotent reconciliation against order state machine.

---

### 4.3 Charm AI & RAG Retriever Failover
If the LLM provider fails or the RAG inverted index is corrupted:
1. **Trigger Graceful Fallback Mode**:
   Set environment variable `RAG_FALLBACK_MODE=DETERMINISTIC_ONLY`.
   The `CharmAIService` will immediately serve pre-verified, deterministic knowledge cards derived from the core numerology matrix without making external generative calls.
2. **Restore Index**:
   ```powershell
   Copy-Item "$CHECKPOINT_DIR/rag_index.json" "data/rag_index.json" -Force
   ```
3. Latency returns immediately to $< 5\text{ms}$.

---

### 4.4 Technical SEO & Content Registry
If search engine crawling issues arise from newly published programmatic pages:
1. **Fallback to Static Registry**:
   Revert `configuration/seo-registry.json` and `configuration/search_intent_and_30day_content_plan.csv` to the last known good commit.
2. **Regenerate XML Sitemap**:
   Trigger `python scripts/generate_sitemap.py` to restore original indexable URL set.
3. **Purge Edge & CDN Caches**:
   Invalidate cloud edge caches for `/sitemap.xml`, `/robots.txt`, and affected landing pages.

---

### 4.5 Brand & UI Design System
If CSS changes cause visual regressions or broken layouts:
1. **Revert Stylesheets**:
   ```powershell
   git checkout tags/$GIT_TAG -- static/css/ templates/
   ```
2. **Verify Theme Tokens**:
   Execute visual regression test to confirm Venus Pearl (`#FFFDF7`), Jupiter Gold (`#C9A227`), and Warm Sandalwood Ink (`#523E28`) are active across all templates.

---

## 5. Post-Rollback Verification Checklist

Following any rollback operation, the following verification suite must pass before declaring normal operations:
- [ ] `/health` returns status `200 OK` with all database and cache connections healthy.
- [ ] Golden Calculation Suite (`tests/test_golden_calculations.py`) passes 100%.
- [ ] `tests/test_live_urls.py` verifies all 31 critical URLs return HTTP 200.
- [ ] `tests/test_api_cyber_security_suite.py` verifies 31/31 security layers active.
- [ ] Test calculation on `/` and `/sample2` submits cleanly to Charm AI consultation without errors.
- [ ] Incident Post-Mortem record initiated in `docs/operations/incident_logs/`.

---
*Authorized by Principal DevOps Engineer and QA Lead for Numeros Vision.*
