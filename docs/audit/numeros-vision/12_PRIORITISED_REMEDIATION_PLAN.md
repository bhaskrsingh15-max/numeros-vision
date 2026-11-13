# NUMEROS VISION: PRIORITISED REMEDIATION PLAN
**Document ID:** `AUDIT-12-REMEDIATION-PLAN`  
**Audit Stage:** Phase 1 Read-Only Technical Audit  
**Date:** October 16, 2026  
**Auditor:** Antigravity Autonomous Systems Engineering Team  
**Prerequisite:** Explicit User Approval Required Before Phase 2 Execution

---

## 1. Remediation Strategy Overview

Following the core directive of **inspect first, document gaps second, propose changes third, and implement only approved, testable changes**, this remediation plan organizes all verified gaps into two controlled, sequential execution phases.

No changes will be applied to the codebase until explicit user approval is granted at the Phase 1 Approval Gate.

---

## 2. Phase 2: Quick Wins & High-Impact Compliance Remediations

*Target Execution Time: 1–2 hours upon approval*  
*Risk Level: Low (Non-breaking, isolated UI/CSS/Header refinements)*

### Work Package 2.1: Color Contrast & Accessibility Remediation
- **Target Items:** `COL-01`, `A11Y-01`, `A11Y-02`, `A11Y-03`
- **Actions:**
  1. In `app/static/css/style.css`, update `--text-faint: #A89880` to `#7A654D`, elevating contrast ratio from 2.82:1 to 4.6:1 (WCAG 2.2 AA compliant).
  2. In `app/static/css/style.css`, add explicit `:focus-visible` styling for custom radio buttons and interactive cards:
     ```css
     .radio-pill:focus-visible, .calculator-card:focus-visible {
       outline: 2px solid var(--accent-gold);
       outline-offset: 2px;
     }
     ```
  3. In calculator templates, wrap dynamic error output elements in `<div aria-live="polite" role="status">` to ensure screen reader announcement.
  4. In report modal templates, add `aria-label="Close dialog"` to all dismiss buttons.

### Work Package 2.2: Technical SEO & Cache Header Enhancements
- **Target Items:** `SEO-01`, `PERF-01`, `SEO-03`
- **Actions:**
  1. Fix breadcrumb JSON-LD schema generation in `app/main.py` to ensure `position` integers start strictly at `1`.
  2. Configure FastAPI `StaticFiles` mounting with long-term caching headers (`Cache-Control: public, max-age=31536000, immutable`).
  3. Adjust `app/seo/pipeline/content_pipeline.py` internal linking heuristic to target a minimum of 5 contextual links per generated article.

### Work Package 2.3: Security Environment Hardening
- **Target Items:** `SEC-02`
- **Actions:**
  1. Enforce strict `allow_origins=["https://numerosvision.com"]` when `ENVIRONMENT=production`.

---

## 3. Phase 3: Architectural Optimizations & Advanced Features

*Target Execution Time: Staged roadmap*  
*Risk Level: Medium (Requires regression testing of RAG & build pipelines)*

### Work Package 3.1: RAG Cold-Start & Performance Acceleration
- **Target Items:** `AI-01`, `AI-02`
- **Actions:**
  1. Pre-compile vector embeddings for the 10,826 canonical passages into a memory-mapped binary array (`.npy`) loaded on ASGI startup, reducing first-query latency from ~350ms to <15ms.
  2. Implement OpenTelemetry/Prometheus metrics for fallback routing latencies.

### Work Package 3.2: CSP Nonce Injection & Deep Security
- **Target Items:** `SEC-01`
- **Actions:**
  1. Implement dynamic cryptographic nonce injection in `CyberDefenseMiddleware` to eliminate `'unsafe-inline'` from `Content-Security-Policy`.

### Work Package 3.3: Internationalization & Regional SEO
- **Target Items:** `SEO-02`
- **Actions:**
  1. Generate dynamic `<link rel="alternate" hreflang="...">` headers for localized multi-lingual content (Hindi, Tamil).

---

## 4. Protected Core Components (Strictly Frozen - Zero Modifications)

The following components are fully certified and must **NOT** be touched during remediation:
1. **Deterministic Calculation Logic:** `app/engine/core_matrix_engine.py`, `cheiro_engine.py`, `pythagorean_engine.py`, `enhanced_lo_shu_engine.py`.
2. **Canonical Knowledge Corpus:** `data/knowledge_base/numeros_vision_corpus.json` (10,826 passages).
3. **Razorpay Pricing & Offer Registry:** 38 active commercial plan configurations.
4. **Brand Design Identity:** Venus Pearl & Jupiter Gold palette, bronze text, approved tagline (*"Anveil Every Charm"*).
