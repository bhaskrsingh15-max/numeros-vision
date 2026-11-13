# Numeros Vision - Monitoring, Observability & Health Probing
**Specification Reference**: `NUMEROS_VISION_MASTER_IMPLEMENTATION.md` (Section 21)  
**Brand Identity**: Numeros Vision | *Unveil Every Charm*  
**Date**: October 2026  
**Status**: APPROVED - OPERATIONAL RUNBOOK

---

## 1. Observability Overview

This document specifies the metrics, health probes, log aggregation, and alerting rules for the **Numeros Vision** platform across the public website, deterministic calculator engines, Charm AI RAG retrieval, and payment workflows.

---

## 2. Core Health Probes

| Endpoint | Probe Type | Frequency | Success Criteria | Failure Action |
|:---|:---|:---:|:---|:---|
| `/health` | Liveness & Readiness | 30s | HTTP 200 `{"status": "healthy", "service": "numeros-vision"}` | Alert DevOps; restart daemon if 3 consecutive failures. |
| `/api/v1/calculate/health` | Engine Integrity | 60s | HTTP 200 with active Cheiro & Pythagorean deterministic status | Flush calculation cache; inspect engine worker. |
| `/api/v1/charm-ai/health` | RAG Index Status | 60s | HTTP 200 `{"status": "ready", "terms_indexed": > 30000, "cache_size": ...}` | Reload inverted index from `data/rag_index.json`. |
| `/api/v1/payment/health` | Gateway Connectivity | 120s | HTTP 200 with Razorpay API reachable | Alert on-call engineer for payment gateway issues. |

---

## 3. Key Performance Indicators (KPIs) & SLA Thresholds

- **Core Calculation Latency**: $\le 15\text{ms}$ (P95)
- **RAG Retrieval Latency**: $\le 10\text{ms}$ (Inverted index query time), $\le 2\text{ms}$ on cache hit
- **Charm AI End-to-End Latency**: $\le 100\text{ms}$ (Pre-warmed consultation response)
- **HTTP Error Rate (5xx)**: $< 0.1\%$ of total daily traffic
- **Payment Webhook Verification**: $100\%$ signature verification rate with 0 dropped webhooks

---

## 4. Log Inspection & Audit Streams

1. **Access & Latency Logs**:
   - Location: `logs/access.log`
   - Formatted with timestamp, method, path, response status, duration (ms), client IP hash.
2. **Cyber Defense & Security Violations**:
   - Location: `logs/cyber_defense_violations.log`
   - Formatted with blocked IP, rule triggered (AI Bot, SQLi, Prompt Injection), payload sample.
3. **Consent & Privacy Audit**:
   - Location: SQLite table `user_consents` and `logs/consent_audit.log`
   - Records DPDP Act 2023 & GDPR explicit consent timestamp and purpose hash.

---
*Certified by Platform SRE for Numeros Vision.*
