# NUMEROS VISION — MASTER AGENT & WORKSPACE RULES
**Document Version**: 1.0.0  
**Effective Date**: 2026-10-21  
**Applies To**: All AI agents, subagents, and human contributors working on Numeros Vision.

---

## 1. Non-Negotiable Core Directives

1. **Deterministic Engine Authority**:
   - The deterministic Python calculation engine (`app/engine/`) owns 100% of calculations.
   - LLMs, vision models, and prompt chains must **NEVER** calculate numerological sums, compound numbers, astrological charts, compatibility matrices, ranking, eligibility, or remedy selections.
   - LLMs may only explain validated, structured results, formulate questions, and draft natural language summaries.

2. **Zero Rule Fabrication**:
   - If a numerology mapping, compound-number interpretation, planetary compatibility, anti/enemy number matrix, remedy rule, or astrological timing condition is not explicitly approved in the repository, it MUST remain a disabled `UNCONFIGURED` or `DRAFT` rule with documented missing provenance.
   - Never fill gaps with guesses or LLM-hallucinated traditions.

3. **Unknown Is Not Negative**:
   - Missing birth time, ambiguous business classification, missing methodology, or contradictory rules must strictly yield `UNKNOWN`, `INSUFFICIENT_EVIDENCE`, or `CONFLICT`.
   - Never fabricate an answer to avoid showing an incomplete status.

4. **Mandatory Evidence Labeling**:
   - Every claim must explicitly separate:
     - (a) **Deterministic/measurable findings** (exact name calculations, contrast ratios, dimensions, OCR output).
     - (b) **Traditional interpretations** (Chaldean, Pythagorean, Vedic, Lo Shu symbolic associations).
     - (c) **Commercial/business evidence** (market positioning, customer utility, operational facts).
     - (d) **Speculative/unvalidated hypotheses** (unapproved proposals like sports Saturn 8 / Ketu 7).
   - Never present traditional interpretations as scientifically proven causal claims or promise commercial success.

5. **Security Release Gate & IP Protection**:
   - All rule matrices, scoring weights, calculation algorithms, system prompts, Google API keys, and internal methodology files remain strictly **server-side**.
   - No secrets, proprietary calculation code, or customer PII may appear in client bundles, public source maps, public APIs, browser storage, or downloadable client configuration.
   - Every endpoint must enforce authentication, tenant isolation, and statutory DPDP 2023 consent.

6. **Honest Completion Claims**:
   - Never state a feature works based on a stub, mock, or UI placeholder. A feature is only complete when tests and runtime evidence verify its behavior end-to-end.
   - Clearly distinguish `IMPLEMENTED`, `PARTIAL`, `MOCKED`, `PENDING`, and `BLOCKED`.

7. **Exact Wordmark & Vector Standards**:
   - Customer-approved business names must be validated against generated logos with independent OCR and normalized string matching.
   - If an image model misrenders text, extract/use the approved symbol and typeset the exact wordmark using a deterministic vector typesetting service (`app/services/vector_renderer.py`).
   - Never rename a raster file (PNG/JPG) to `.svg`. All vector deliverables must contain valid geometric vector paths.

---

## 2. Brand Identity & Design System Guidelines

- **Brand Name**: `NUMEROS VISION` (Always all-caps in titles and wordmarks).
- **Tagline**: `ANVEIL EVERY CHARM` (Always all-caps).
- **Master Header & Footer**: All pages must integrate `<header class="nv-header">` and `<footer class="nv-footer">`.
- **Approved Theme Palette**:
  - Venus Pearl: `#FFFDF7`, `#F7F3EA`, `#FFFFFF`
  - Jupiter Gold: `#C9A227`, `#8B6914`, `#E2B84B`, `#9E7B15`
  - Mercury Emerald: `#16835B`
  - Sandalwood Ink: `#523E28`, `#7A654D`
  - **STRICTLY ZERO** raw black `#000000` in typography or UI containers.
  - All prices must strictly use theme gold (`var(--gold-dark, #8B6914)`).

---

## 3. Contextual Archetype Engine (Section 16)

- Evaluate businesses using the contextual causal chain:
  `business activity → product function → customer outcome → candidate planetary archetypes`.
- Never judge a name, planet, or color in isolation.
- Contextual exceptions (e.g., footwear endurance associating with Saturn/Rahu, allowing black branding) are scoped strictly to matching categories and do not transfer to unrelated categories (e.g. food or banking).
- Model reasoning rather than historical claims (e.g. Nike Swoosh historical facts vs. traditional astrological hypothesis).

---

## 4. Google Nano Banana Logo Framework (Section 17)

- Server-side adapter for Google GenAI image generation with configurable model ID (`imagen-3.0-generate-002`).
- Prompts compiled deterministically from validated `DesignSpecification` JSON objects.
- Multi-gate independent validation: OCR text match, palette sampling, contrast ratio, dimensions, small-size legibility, transparency.
- Bounded correction attempts (maximum 2 retries); route to human review or deterministic vector typesetting upon exhaustion.

---

## 5. Charm AI Career Rectification Directives (Section 18)

- Detailed persistent rules are stored in `.agents/rules/charm_ai_rectification.md`.
- **Dasha-First Primary Authority**: Numerology Dasha owns primary timing windows; KP, Vedic, and BNN provide independent cross-verification without altering primary windows.
- **Forecast Horizon Separation**: User requested horizon (e.g. 6 months) must remain separate from calculated windows.
- **Abstention Standard**: Missing birth inputs or unapproved rules strictly return `INSUFFICIENT_EVIDENCE`. Never name predicted dates when calculations are blocked.
- **Prioritized 7-Tier User Experience**: User responses strictly follow: 1. Takeaway, 2. Timing Status, 3. Supported Findings, 4. Unconcluded Elements, 5. Missing Inputs, 6. Practical Actions, 7. Single Concise Follow-up.

---

## 6. NV THINK™ Logic-to-Psychology Framework (Section 19)

- Detailed persistent rules are stored in `.agents/rules/nv_think_framework.md`.
- **Core Principle**: Never assume a number is a person. A number is an interpretive indicator. A chart is a collection of indicators. Behaviour requires context. Psychology requires understanding. Prediction requires validation.
- **7 Stages of Intelligence**: All interpretive agents and Charm AI must reason across: `Logic → Observation → Behaviour → Psychology → Context → Contradiction → Validation/Prediction`.
- **Multi-Model Consensus via Duality**: Numerology Dasha owns primary timing boundaries; astrological models (KP, Vedic, BNN) cross-verify. Any tension between models is investigated as psychological and environmental duality (e.g., internal drive vs external structural pacing), never suppressed or dismissed as an error.
- **Diagnostic Structured Output**: Pipeline emits 15 psychological dimensions with explicit validation status and prediction eligibility.


