# NUMEROS VISION — CHARM AI RECTIFICATION RULES
**Applies To**: Charm AI Chatbot, Career Analysis Engine, Numerology Dasha Pipeline, API Endpoints, and Frontend Integration.

---

## 1. Non-Negotiable Calculation & Verification Directives

1. **Numerology Dasha is Primary**:
   - The deterministic Python calculation engine (`app/charm/numerology/dasha_engine.py`) owns 100% of timing window calculations.
   - KP Astrology, Vedic Astrology, and BNN are independent cross-verification systems, never replacements for Numerology Dasha.
   - Astrological transits or significators can corroborate or contextualize, but can **never** overwrite or alter the Numerology Dasha primary date boundaries.

2. **Forecast Horizon vs Calculated Windows**:
   - The user's requested forecast horizon (e.g. "next 6 months") must be captured separately from calculated results.
   - Never mistake or substitute the user's requested horizon for a calculated prediction window.

3. **Missing Data & Abstention Standard**:
   - If required birth inputs or verified calculation rules are missing, the system must return `INSUFFICIENT_EVIDENCE`.
   - Never name a favorable month, job-offer date, or predicted appointment when calculations are blocked.
   - Provide a structured 6-point breakdown: (a) what is available, (b) what is missing, (c) why it is required, (d) required approved source/rule, (e) blocked calculations, (f) safe interim conclusions.
   - Ask exactly one concise follow-up question at a time. Never ask for birth time/place unless the requested astrological method strictly requires it.

4. **Supported Consensus Verification Statuses**:
   The backend consensus engine must strictly emit one of the 6 canonical statuses:
   - `NUMEROLOGY_PRIMARY_CORROBORATED`
   - `NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED`
   - `NUMEROLOGY_PRIMARY_CONFLICTED`
   - `NUMEROLOGY_PRIMARY_ONLY`
   - `INSUFFICIENT_EVIDENCE`
   - `NOT_ELIGIBLE_FOR_PREDICTION`
   Verification status must remain strictly separate from the career assessment (`FAVOURABLE`, `MIXED`, `UNFAVOURABLE`, `NEUTRAL`).

5. **Lo Shu vs Dasha Boundary**:
   - Retain user-supplied date of birth and reported Lo Shu numbers as user-supplied information until validated.
   - Never assume that a Lo Shu grid establishes a Numerology Dasha, subperiods, or a career timing window.

6. **Prioritized 7-Tier Response Order**:
   All user-facing career responses must follow this exact hierarchy:
   1. Concise career takeaway.
   2. Timing status and verification level.
   3. What the supplied report supports.
   4. What cannot yet be concluded.
   5. The exact missing calculation or input.
   6. Practical job-search actions (portfolio audit, networking).
   7. Optional neutral follow-up question.

7. **Brand Identity & Zero Raw Black**:
   - Strictly ZERO raw black `#000000`. Use Sandalwood Ink (`#523E28`, `#7A654D`), Jupiter Gold (`#8B6914`, `#C9A227`), Venus Pearl (`#FFFDF7`, `#FFFFFF`).
   - Preserve `NUMEROS VISION` wordmark and `ANVEIL EVERY CHARM` tagline in all-caps.
