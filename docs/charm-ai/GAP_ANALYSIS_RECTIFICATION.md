# NUMEROS VISION / CHARM AI
## Gap Analysis & Rectification Matrix

**Document Version**: 1.0.0  
**Effective Date**: 2026-10-21  
**Target Subsystem**: Charm AI Career Analysis & Numerology Dasha Engine  
**Standards Authority**: Master Implementation Specification & Rectification Instructions v2.0  

---

## 1. Executive Summary

A comprehensive gap audit was conducted on the current Charm AI career-analysis implementation. 

While the system successfully calculates basic 9-year Mahadashas and displays multi-method status pills in the frontend, the backend currently contains gaps in:
1. **Forecast Horizon vs Calculated Windows**: User-requested forecast horizons (e.g. "next 6 months") were conflated or unparsed from actual calculated Dasha periods.
2. **Missing Input & Evidence Behavior**: The engine did not provide a granular breakdown of what inputs are available vs missing, why they are required, what calculations remain blocked, and what can responsibly be concluded now.
3. **Consensus Verification Status Exhaustiveness**: The consensus engine supported 4 statuses but omitted formal handling of `INSUFFICIENT_EVIDENCE` and `NOT_ELIGIBLE_FOR_PREDICTION`.
4. **Lo Shu vs Dasha Conflation**: User reports frequently assume a Lo Shu natal grid establishes career dasha periods or a 6-month timing window, which must be clearly separated and labeled as unverified user-supplied data until proven.
5. **Prioritized 7-Tier Human-Friendly Response**: The chatbot output needed a structured 7-part hierarchy (Takeaway, Timing Status, Supported Findings, Unconcluded Elements, Exact Missing Inputs, Practical Actions, Single Concise Follow-up).

---

## 2. Comprehensive Gap Matrix

| # | Subsystem / Feature | Current Behavior | Repository Evidence | Expected Behavior | Severity | Affected Files | Proposed Correction | Test Required |
|---|---|---|---|---|---|---|---|---|
| **GAP-01** | **User Intent & Horizon Parsing** | `requested_horizon` hardcoded to `"12_months"`; career goals are not categorized into specific intent codes. | `app/charm/intent/event_intent_service.py:45` | Parse goals (`new_job_or_senior_role`, `senior_appointment`, `promotion`, `career_change`, `business_venture`). Parse forecast horizon (e.g. `6_months`, `3_months`) and keep it strictly separated from calculated windows. | High | `app/charm/intent/event_intent_service.py` | Add regex parser for forecast horizons (`6_months`, `1_year`, etc.) and career goal taxonomy. | Verify requested horizon is captured but does not alter calculated windows. |
| **GAP-02** | **Consensus Status Completeness** | Gate 1 returns `NOT_EVALUATED` or defaults to `NUMEROLOGY_PRIMARY_ONLY`; missing `INSUFFICIENT_EVIDENCE` and `NOT_ELIGIBLE_FOR_PREDICTION`. | `app/charm/consensus/engine.py:58-69` | Enforce all 6 standard verification statuses: `NUMEROLOGY_PRIMARY_CORROBORATED`, `NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED`, `NUMEROLOGY_PRIMARY_CONFLICTED`, `NUMEROLOGY_PRIMARY_ONLY`, `INSUFFICIENT_EVIDENCE`, `NOT_ELIGIBLE_FOR_PREDICTION`. | Critical | `app/charm/consensus/engine.py` | Update Gate 1 & Gate 3 to return `INSUFFICIENT_EVIDENCE` when inputs/rules missing, and `NOT_ELIGIBLE_FOR_PREDICTION` for out-of-scope inquiries. | Test consensus returns `INSUFFICIENT_EVIDENCE` when birth date or dasha rules are missing. |
| **GAP-03** | **Missing Data & Abstention Handling** | Returns generic "Please provide complete birth details" without structured breakdown. | `app/charm/chat/response_composer.py:72-84` | Return structured 6-point explanation: Available inputs, Missing inputs, Why required, Required rules, Blocked calculations, Safe interim conclusions. Never name a favorable month or job date when blocked. | Critical | `app/charm/chat/response_composer.py` | Implement `StructuredMissingDataExplanation` and abstain from date prediction when inputs/rules are blocked. | Test that unverified birth details abstain from date prediction and output structured breakdown. |
| **GAP-04** | **Lo Shu vs Dasha Boundary** | Lo Shu numbers can be mistaken as establishing a career dasha or 6-month prediction. | `app/charm/numerology/dasha_engine.py` | Retain Lo Shu digits strictly as user-supplied natal inventory; do not derive Dasha timelines from Lo Shu grid counts. | High | `app/charm/numerology/dasha_engine.py` | Add provenance metadata explicitly noting Lo Shu does not establish timing windows. | Test that missing birth date with present Lo Shu yields `INSUFFICIENT_EVIDENCE`. |
| **GAP-05** | **Career-Event Source Mapping** | General symbolic planetary interpretations mixed with timing window support rules. | `app/charm/methods/kp_adapter.py`, `app/charm/methods/vedic_adapter.py` | Distinguish symbolic planetary meaning (e.g. Venus harmony) from verified timing rules (e.g. 10th cuspal sub-lord significator). | Medium | `app/charm/methods/`, `app/charm/rag/` | Explicitly tag rule evidence as `SYMBOLIC_CORRESPONDENCE` vs `TIMING_SIGNIFICATOR`. | Verify only timing significator rules contribute to window corroboration. |
| **GAP-06** | **Prioritized 7-Tier Response Structure** | Chatbot output has greeting, direct answer, Lo Shu, age card, but lacks the standardized 7-tier decision flow. | `app/static/charm_ai.html:821-840` | Deliver output in strict prioritized order: 1. Career Takeaway, 2. Timing Status, 3. Supported Findings, 4. What cannot yet be concluded, 5. Exact missing inputs, 6. Practical job actions, 7. Single concise follow-up. | High | `app/charm/chat/response_composer.py`, `app/static/charm_ai.html` | Format the view model and UI template to render the 7-tier hierarchy with expandable technical sections. | Test UI renders all 7 tiers with zero raw black `#000000`. |
| **GAP-07** | **Persistent Antigravity Project Rules** | Project rules were solely in `AGENTS.md`; `.agents/rules/` directory was absent. | Workspace root | Add `.agents/rules/charm_ai_rectification.md` adhering to the official 24 KB per-file limit to persist calculation and UI-preservation constraints. | Medium | `.agents/rules/charm_ai_rectification.md`, `AGENTS.md` | Create `.agents/rules/charm_ai_rectification.md` and link in `AGENTS.md`. | Validate file exists and is under 24 KB. |

---

## 3. Implementation Phasing Plan

- **Phase A**: Audit and Gap Matrix (Complete in this document).
- **Phase B**: Intent, Horizon & Input Validation Corrections (`app/charm/intent/event_intent_service.py`, `app/charm/numerology/dasha_engine.py`).
- **Phase C**: Consensus & Verification Statuses (`app/charm/consensus/engine.py`).
- **Phase D**: Backend Orchestrator & API Integration (`app/charm/chat/response_composer.py`, `app/api/charm_ai.py`).
- **Phase E**: Frontend 7-Tier Rendering Integration (`app/static/charm_ai.html`).
- **Phase F**: Automated Test Suite & Regression Verification (`tests/test_charm_career_rectification.py`).
