# Numeros Vision — Cost Governance & Quota Model
**Document Version**: 1.0.0  
**Effective Date**: 2026-10-21  
**Author**: Principal Software Architect & Financial Engineering Lead

---

## 1. Provider Cost Basis & Pricing Assumptions

As per the official Google GenAI / Gemini API pricing documentation for image generation:

| Service / Model | Role | Pricing Basis | Estimated Unit Cost |
| :--- | :--- | :--- | :--- |
| **`imagen-3.0-generate-002`** | High-Fidelity Final Logo Generation | Per Image Generated | **\$0.030 USD** (3.0 cents) |
| **Fast / Draft Image Model** | Concept Exploration & Thumbnails | Per Image Generated | **\$0.020 USD** (2.0 cents) |
| **Deterministic Vector Typesetting** | Wordmark & Vector Fallback (`SVG`) | Pure Python / Local CPU | **\$0.000 USD** (Zero API Cost) |
| **OCR & Image Validation Gates** | Spelling, Palette, Contrast | Local PIL / Local Heuristics | **\$0.000 USD** (Zero API Cost) |

*Note: All estimated costs are recorded in integer minor units (USD cents) in job audit metadata.*

---

## 2. Customer Package Entitlements & Revision Limits

To guarantee financial predictability and prevent runaway API expenditure:

1. **Logo Intelligence Package Entitlements**:
   - **Base Entitlement**: 1 primary generation run (producing 1-2 concept variants).
   - **Included Revisions**: Maximum 2 bounded automated correction attempts for validation failures (e.g. slight color drift or symbol alignment).
   - **Customer-Initiated Manual Revisions**: 1 free subjective revision. Extra revisions require purchasing additional revision credits ($5.00 / 3 revisions).

2. **System-Wide Circuit Breakers**:
   - **Daily Global Spend Limit**: \$50.00 USD (equivalent to ~1,666 image generation calls). If reached, the engine automatically disables new external API calls and falls back to deterministic vector generation or queues requests.
   - **Per-Tenant Daily Limit**: Maximum 3 generation jobs per 24-hour rolling window.
   - **Maximum Concurrent Provider Requests**: 5 concurrent active jobs across the entire instance.

---

## 3. Idempotency & Caching Strategy

- Every generation request requires a client-supplied or server-generated `idempotency_key` (derived from `SHA-256(tenant_id + exact_wordmark + approved_hex_palette + prompt_hash)`).
- If an identical generation request is submitted within 10 minutes, the existing in-flight job or cached result is returned immediately without invoking the external Google GenAI endpoint.
- Zero-cost local vector rendering is always executed as the final high-resolution deliverable format, minimizing unnecessary raster regeneration.
