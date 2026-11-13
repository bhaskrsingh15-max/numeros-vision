# Numeros Vision — Logo Generation & Independent Validation Specification
**Document Version**: 1.0.0  
**Effective Date**: 2026-10-21  
**Reference**: Sections 17.3 - 17.7 of Master Build Specification

---

## 1. End-to-End Customer Logo Workflow

The complete customer logo journey executes through 20 governed steps:

1. **Authentication & Tenant Isolation**: Authenticate customer and resolve tenant context.
2. **Entitlement Verification**: Check remaining generation and revision credits.
3. **Business Intake**: Capture exact wordmark spelling, business activity, customer segment, and market positioning.
4. **Optional Founder Birth Data**: Capture with explicit DPDP 2023 consent if customer requests astrological alignment.
5. **Deterministic Numerology Execution**: Calculate Chaldean, Pythagorean, and Lo Shu metrics.
6. **Rule Engine Evaluation**: Evaluate business archetype alignment with status `draft`/`approved` tracking.
7. **Business Taxonomy Classification**: Classify primary and secondary functions.
8. **Existing Logo Feature Extraction**: If uploaded, measure detected colors, contrast, and layout objectively.
9. **RAG Provenance Retrieval**: Extract verified source references via `SourcePrivacyShield`.
10. **Assessment Compilation**: Build structured `AssessmentResult`.
11. **DesignSpecification Assembly**: Create customer brief conforming to Section 17.4 schema.
12. **Customer Explicit Approval**: Customer explicitly signs off on exact wordmark, palette roles, and visual direction.
13. **Deterministic Prompt Compilation**: Compile prompt with quoted literals and prohibited elements.
14. **Provider Invocation**: Send request to `GoogleImageProvider` (Imagen 3).
15. **Independent Multi-Gate Validation**: Run automated OCR, palette, contrast, and dimension checks.
16. **Bounded Correction Loop**: If minor validation failure occurs, retry with specific defect prompt (max 2 retries).
17. **Deterministic Vector Typesetting Fallback**: If wordmark OCR fails, typeset approved wordmark with pure SVG vector typography.
18. **Secure Asset Storage**: Store generated deliverables in private tenant directories with expiring download links.
19. **Deliverable Delivery**: Provide icon, stacked, and horizontal variants in SVG, PNG, and PDF.
20. **Audit Trail Recording**: Log job status, prompt hash, model ID, costs, and validation results.

---

## 2. Multi-Gate Independent Validation Engine

Every generated image passes through 5 automated gates before being shown to the customer:

| Gate | Verification Method | Pass Criteria | Failure Action |
| :--- | :--- | :--- | :--- |
| **1. Exact Wordmark** | OCR / Levenshtein Distance | Exact string match with customer-approved wordmark | Trigger bounded retry or switch to deterministic SVG typesetting |
| **2. Palette Fidelity** | Region Sampling & RGB Euclidean Distance | Dominant colors match approved HEX palette within $\Delta E \le 25$ | Record color drift warning; adjust in SVG |
| **3. Contrast Ratio** | WCAG 2.1 Relative Luminance | Text/Symbol vs. Background contrast $\ge 4.5:1$ (normal) or $\ge 3.0:1$ (large) | Adjust background or flag contrast warning |
| **4. Dimensions & MIME** | PIL Image Inspection | Valid PNG/SVG/WebP format, width/height $\ge 1024\text{px}$ | Fail job safely; reject corrupt payload |
| **5. Alpha Transparency** | Alpha Channel Inspection | 4-channel RGBA with valid transparent bounding area if transparency requested | Flag flat-background post-processing |

---

## 3. Two-Part Vector Delivery Standard

- **No Pseudo-SVGs**: Renaming a `.png` to `.svg` is strictly prohibited.
- When vector deliverables are requested, the platform generates true SVG paths (`<path d="...">`, `<circle>`, `<text>`) via `app/services/vector_renderer.py`, embedding the customer-approved wordmark in clean, scalable typography.
