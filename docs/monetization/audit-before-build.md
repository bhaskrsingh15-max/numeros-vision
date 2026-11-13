# NUMEROS VISION — MONETIZATION & FUNNEL AUDIT BEFORE BUILD
**Document Version:** 1.5.0  
**Audit Date:** 2026-10-21  
**Scope:** Existing Commercial Architecture, Payment Gateways, Pricing Catalog, Calculators, Charm AI, and 7-Stage Funnel Integration.

---

## 1. Executive Summary

This audit assesses the existing Numeros Vision repository against the requirements of the **Advanced Marketing Funnel & Conversion Framework (v1.5.0)**.
The objective is to establish a unified, configuration-driven commercial journey:
$$\text{Curiosity} \longrightarrow \text{Discovery} \longrightarrow \text{Relevance} \longrightarrow \text{Purchase} \longrightarrow \text{Value} \longrightarrow \text{Loyalty}$$
while preserving all existing visual design, brand lock-ups (`NUMEROS VISION`), approved tagline (`ANVEIL EVERY CHARM`), and deterministic calculation engines.

---

## 2. Existing Commercial Infrastructure

### 2.1 Backend Services & Endpoints
1. **`app/api/payments.py`**:
   - `GET /api/v1/payments/plans`: Returns public catalog of plans and Razorpay public key.
   - `POST /api/v1/payments/alignment-gap-analysis`: Evaluates Driver-Conductor polarity and Lo Shu missing planes via `monetization_alignment_engine.py`.
   - `POST /api/v1/payments/create-order`: Generates Razorpay orders (with mock fallback for sandbox testing).
   - `POST /api/v1/payments/verify`: Performs server-side HMAC-SHA256 signature verification and issues session tokens.
   - `GET /api/v1/payments/status/{session_token}`: Queries active entitlement status.
   - `POST /api/v1/payments/webhook`: Server-to-server webhook handler for `payment.captured` and `order.paid`.
2. **`app/engine/monetization_alignment_engine.py`**:
   - Analyzes Driver vs. Conductor compatibility and Lo Shu 3x3 Grid gaps (Golden Plane 4-5-6, Will Plane 9-5-1, etc.).
   - Computes alignment status (`ALIGNED`, `PARTIALLY_ALIGNED`, `FRICTION_DETECTED`).
   - Generates brand-led CTAs and personalized hooks.
   - Monitors question credits and upselling pathways.
3. **`app/api/auth.py`**:
   - Manages user account session state and persists entitlements in `update_user_entitlements()`.

---

## 3. Pricing Catalog & Digit-Root Audit

The brand policy requires all whole-rupee prices to reduce to single digital roots in $\{1, 3, 5, 6\}$.

| Plan ID | Plan Name | Price (INR) | Digital Root Calculation | Root | Status |
| :--- | :--- | :--- | :--- | :---: | :---: |
| `starter_5q` | Starter — 5 Questions | ₹95 | $9+5=14 \to 1+4$ | **5** | Approved |
| `growth_10q` | Growth — 10 Questions + Remedies | ₹399 | $3+9+9=21 \to 2+1$ | **3** | Approved |
| `complete_report` | Complete Reports & Remedies | ₹1,050 | $1+0+5+0$ | **6** | Approved |
| `report_essential` | Essential Cosmic Blueprint | ₹199 | $1+9+9=19 \to 1+9=10 \to 1+0$ | **1** | Approved |
| `report_master` | Master Dual-System Synthesis | ₹510 | $5+1+0$ | **6** | Approved |
| `report_divine` | Divine Sovereign Life Roadmap | ₹1,050 | $1+0+5+0$ | **6** | Approved |
| `ai_starter_5q` | Charm AI — Starter Pack | ₹95 | $9+5=14 \to 1+4$ | **5** | Approved |
| `ai_growth_15q` | Charm AI — Growth Pack | ₹249 | $2+4+9=15 \to 1+5$ | **6** | Approved |
| `ai_power_35q` | Charm AI — Power Pack | ₹492 | $4+9+2=15 \to 1+5$ | **6** | Approved |
| `sub_monthly` | Monthly Pass | ₹150 | $1+5+0$ | **6** | Approved |
| `sub_annual` | Annual VIP Pass | ₹999 | $9+9+9=27 \to 2+7$ | **9** | Legacy/Exemption |
| `ai_report_combo` | Interactive Charm AI + Master Report | ₹699 | $6+9+9=24 \to 2+4$ | **6** | Approved |
| `advisory_personal_name` | Personal Name Balancing | ₹1,499 | $1+4+9+9=23 \to 2+3$ | **5** | Approved |
| `advisory_business_name` | Commercial Entity & Brand Matrix | ₹5,999 | $5+9+9+9=32 \to 3+2$ | **5** | Approved |
| `b2b_consultant_pro` | B2B SaaS — Consultant Pro | ₹2,499 | $2+4+9+9=24 \to 2+4$ | **6** | Approved |

---

## 4. Calculator Frontends & Result Transitions Audit

### 4.1 Identified Gaps in Frontend Calculators
1. **Inconsistent Result-to-Offer Transitions**:
   - Several calculators (`life-path-calculator.html`, `lo-shu-grid.html`, etc.) render ad-hoc locked remedy blocks directly inside JavaScript string templates rather than using a centralized, responsive component.
2. **Brand Spelling Defects ("Unveil" vs. "Anveil")**:
   - Found occurrences of "Unveil Master Dossier" or "Unveil" in buttons and templates. The master brand directive explicitly enforces: **ANVEIL EVERY CHARM** (spelled A-N-V-E-I-L, never "Unveil").
3. **Missing Curiosity Bridge (Step 2)**:
   - Free calculators jump abruptly from mathematical diagnostics to a locked remedy box without the educational "Want to explore the next layer?" bridge explaining the additional deliverables of the full report.
4. **Lack of Shared Funnel State**:
   - No unified tracking for funnel progression: `Awareness → Interest → Consideration → Conversion → Retention → Loyalty → Repeat Conversion`.
5. **Marketing Opt-Out Precedence**:
   - Users who dismiss or opt out of promotional messages must be able to view their free calculations peacefully without repeated hard paywalls.

---

## 5. Architectural Gap Register

| Gap ID | Component | Current State | Required State (v1.5.0) |
| :--- | :--- | :--- | :--- |
| **GAP-FUNNEL-01** | Backend Service | Only polarity gap analysis in `monetization_alignment_engine.py` | Dedicated `app/engine/funnel_service.py` implementing 7-stage state machine & `get_next_step()` |
| **GAP-FUNNEL-02** | Pricing Policy Engine | Hard-coded prices in `PLANS` dict | Server-side digit root validator enforcing roots in $\{1, 3, 5, 6\}$ and `offer < reference` |
| **GAP-FUNNEL-03** | Entitlement Decision | Simple key check in `_verified_payments` | Immutable access evaluator (`decide_feature_access`) handling Purchases, Subscriptions, Expiries & Quotas |
| **GAP-FUNNEL-04** | Promotion Engine | No stacking policy enforced | Server-side stacking rule rejecting stacked discounts by default |
| **GAP-FUNNEL-05** | Frontend Offer Bridge | Divergent inline HTML across 14 calculator files | Unified, responsive component `renderFunnelOfferBridge()` in `app/static/js/funnel_journey.js` |
| **GAP-FUNNEL-06** | Tagline Integrity | Stray instances of "Unveil" | Strictly zero instances of "Unveil"; all replaced with "Anveil" |
| **GAP-FUNNEL-07** | Privacy & Opt-Out | No explicit funnel opt-out preference | Support for `OPTED_OUT` state honoring seeker preferences |

---

## 6. Implementation Plan & Non-Regression Commitments

1. **Build `app/engine/funnel_service.py`**:
   - Provide `PricePolicy`, `digit_root()`, `validate_price_pair()`, `FunnelStage`, `JourneyState`, `ProductCatalog`, and `get_next_step()`.
2. **Expose Funnel API Endpoints in `app/api/payments.py`**:
   - `/api/v1/payments/funnel/next-step`, `/api/v1/payments/funnel/products`, `/api/v1/payments/funnel/validate-price`, `/api/v1/payments/funnel/event`.
3. **Build `app/static/js/funnel_journey.js`**:
   - Expose `window.nvFunnelJourney` with `renderOfferBridge(containerId, options)`, `trackEvent()`, and `optOut()`.
4. **Refactor Calculators**:
   - Seamlessly connect calculators to the unified offer bridge without modifying calculation math or page themes.
5. **Verify with Tests**:
   - Ensure 100% of existing 263 tests pass, add comprehensive new unit tests for the funnel engine, and run header/QC audits.
