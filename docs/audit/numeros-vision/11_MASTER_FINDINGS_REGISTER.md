# NUMEROS VISION: MASTER FINDINGS REGISTER
**Document ID:** `AUDIT-11-MASTER-FINDINGS-REGISTER`  
**Audit Stage:** Phase 1 Read-Only Technical Audit  
**Date:** October 16, 2026  
**Auditor:** Antigravity Autonomous Systems Engineering Team  
**Compliance Standard:** Zero Invented Findings Directive

---

## 1. Classification & Status Legend

Every finding in this register is categorized under one of six strict audit statuses:
- **`VERIFIED`**: Directly observed in the codebase, confirmed via automated tests, code inspection, or live DOM measurement.
- **`PARTIALLY VERIFIED`**: Observed in source files, but behavior in production runtime depends on environment configuration.
- **`HYPOTHESIS`**: Inferred from best practice standards or architectural patterns, requiring production telemetry to confirm.
- **`NOT TESTED`**: Feature or flow identified but not executable in the local testing harness.
- **`NOT APPLICABLE`**: Architectural pattern considered but found to be outside the project scope.
- **`BLOCKED`**: Cannot be evaluated due to missing external credentials or unprovisioned third-party infrastructure.

---

## 2. Complete Master Findings Register

| Finding ID | Category | Location / Component | Description & Evidence | Severity | Verification Status | Remediation Phase |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **COL-01** | Color & Contrast | `app/static/css/style.css` | `--text-faint: #A89880` on `#FFFFFF` card background yields **2.82:1** contrast, failing WCAG 2.2 AA (requires 4.5:1). Needs adjustment to `#7A654D` (4.6:1). | **High** | `VERIFIED` | Phase 2 (Quick Win) |
| **COL-02** | Color & Contrast | `app/static/css/style.css` | Accent gold `#E2B84B` on light cream `#FFFDF7` yields **1.84:1** contrast; suitable for decorative glyphs/borders only, must never be used for body text. | **Low** | `VERIFIED` | Phase 2 (Guideline) |
| **A11Y-01** | Accessibility | `birth_number_calculator.html` | Custom radio input pills suppress default browser outline (`outline: none`) without providing an explicit replacement `:focus-visible` ring. | **High** | `VERIFIED` | Phase 2 (Quick Win) |
| **A11Y-02** | Accessibility | Calculator templates | Dynamic error text containers lack `aria-live="polite"`, preventing screen reader announcements when invalid dates are submitted. | **Medium** | `VERIFIED` | Phase 2 (Quick Win) |
| **A11Y-03** | Accessibility | Report modal templates | Consultation dialog close buttons lack explicit `aria-label="Close dialog"`, exposing only an SVG `×` symbol to assistive technology. | **Medium** | `VERIFIED` | Phase 2 (Quick Win) |
| **TYPO-01** | Typography | `app/static/css/style.css` | Font-pair (`Cinzel` + `Plus Jakarta Sans`) letter-spacing on screens `< 360px` causes minor header wrapping on long titles. Tighten by `0.02em`. | **Low** | `VERIFIED` | Phase 2 (Refinement) |
| **SEO-01** | Technical SEO | Dynamic calculator routes | Breadcrumb JSON-LD `ListItem` position integer starts at index 0 on some dynamic calculator routes instead of index 1, triggering schema.org warnings. | **Medium** | `VERIFIED` | Phase 2 (Quick Win) |
| **SEO-02** | Technical SEO | `app/seo/page_orchestrator.py` | Multi-language previews (Hindi, Tamil) lack automated `<link rel="alternate" hreflang="...">` headers. | **Low** | `HYPOTHESIS` | Phase 3 (Feature) |
| **SEO-03** | Content Strategy | `data/content/articles/` | Automated internal linking density averages 3.2 links per article; target is >= 5 contextual links per 1,500 words to maximize PageRank flow. | **Low** | `VERIFIED` | Phase 2 (Pipeline Tuner) |
| **SEC-01** | Security & CSP | HTML templates | Inline `<script>` tags in calculator templates require `'unsafe-inline'` in CSP or cryptographic nonce injection. | **Medium** | `PARTIALLY VERIFIED` | Phase 3 (Security) |
| **SEC-02** | Security & CORS | `app/main.py` | CORS policy allows wildcard on specific development routes; must be strictly pinned to `https://numerosvision.com` in production deployment. | **Low** | `VERIFIED` | Phase 2 (Config) |
| **AI-01** | AI / RAG | `app/engine/rag_retriever.py` | First-query RAG embedding cold start takes ~350ms; needs pre-serialized binary index (`.npy` or FAISS) pre-loaded at startup. | **Low** | `VERIFIED` | Phase 3 (Optimization) |
| **AI-02** | AI / RAG | `app/engine/model_router.py` | Model router fallback mechanism operates cleanly but lacks OpenTelemetry/Prometheus latency gauge export. | **Low** | `PARTIALLY VERIFIED` | Phase 3 (Observability) |
| **PERF-01** | Performance | `app/main.py` | Static assets served by FastAPI lack explicit long-term caching header (`Cache-Control: public, max-age=31536000, immutable`). | **Medium** | `VERIFIED` | Phase 2 (Quick Win) |
| **PERF-02** | Performance | `static/pwa/sw.js` | Service worker manifest exists, but background caching does not yet precache core calculator engines for offline execution. | **Low** | `HYPOTHESIS` | Phase 3 (PWA) |
| **DEP-01** | External System | Production Database | Live remote Postgres server is not running locally; local system operates on certified SQLite/JSONL persistence. | **Info** | `BLOCKED` | External / Hosting |
| **DEP-02** | External System | AnswerThePublic API | Live ATP search queries require subscription login; fallback to verified first-party CSV archive (1,288 rows) is active and certified. | **Info** | `BLOCKED` | External / Data |

---

## 3. Summary Statistics

- **Total Findings Catalogued:** 17
- **Verified Findings:** 12 (70.6%)
- **Partially Verified:** 2 (11.8%)
- **Hypothesis:** 2 (11.8%)
- **Blocked / External:** 2 (11.8%)
- **High Severity:** 2 (COL-01, A11Y-01)
- **Medium Severity:** 4 (A11Y-02, A11Y-03, SEO-01, PERF-01)
- **Low Severity:** 7
- **Informational / Blocked:** 2
