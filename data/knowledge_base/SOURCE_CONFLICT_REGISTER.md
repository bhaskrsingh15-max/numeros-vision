# SOURCE CONFLICT & HARMONIZATION REGISTER
**Version:** 1.0.0  
**Effective Date:** 2026-10-29  
**Scope:** Numeros Vision / Charm AI Knowledge Architecture  
**Directives:** Adheres strictly to Non-Negotiable Directives: No silent averaging, no semantic override of deterministic formulas, provenance preservation, explicit status reporting (`CONFLICT_UNRESOLVED`).

---

## 1. Methodology Separation Principles

Numeros Vision operates multiple distinct wisdom systems. Under Master Rules, **different traditions must never be blended, averaged, or converted into an ad-hoc hybrid formula**. Each tradition retains its independent calculation engine and verified source authority.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                       METHODOLOGY NAMESPACE MATRIX                          │
├───────────────────────────────┬─────────────────────────────┬───────────────┤
│ Namespace                     │ Authoritative Primary Text  │ Engine Key    │
├───────────────────────────────┼─────────────────────────────┼───────────────┤
│ numerology.chaldean_cheiro     │ Cheiro's Book of Numbers    │ CHALDEAN      │
│ numerology.pythagorean        │ Complete Guide to Numerology│ PYTHAGOREAN   │
│ numerology.lo_shu             │ Lo Shu Grid Traditional     │ LO_SHU        │
│ numerology.vedic              │ Classical Vedic Tradition / Classical Vedic Heritage 1990 │ VEDIC_NUM     │
│ numerology.craze_decoder      │ Richard Craze (1998)        │ CRAZE_DECODER │
│ astrology.nadi                │ Numeros Vision Classical Archive (2013 ed.)     │ NADI_EVENT    │
└───────────────────────────────┴─────────────────────────────┴───────────────┘
```

---

## 2. Reconciled Conflict Records

### Conflict CR-001: Alphabet-to-Number Letter Mapping
- **Tradition A (Chaldean / Cheiro):**
  - Mappings: A=1, B=2, C=3, D=4, E=5, F=8, G=3, H=5, I=1, J=1, K=2, L=3, M=4, N=5, O=7, P=8, Q=1, R=2, S=3, T=4, U=6, V=6, W=6, X=5, Y=1, Z=7.
  - Number 9 is sacred and excluded from individual single-letter assignments; 9 only appears as a compound sum.
- **Tradition B (Pythagorean / Western):**
  - Linear sequential 1–9 mapping across the 26 letters (A=1, B=2, ... I=9, J=1, ... R=9, S=1, ... Z=8).
- **Resolution & System Behavior:**
  - **Zero Cross-Contamination:** Chaldean is the strict default for all commercial name vibrations, mobile vibrations, and brand naming. Pythagorean is maintained as a separate, explicitly tagged secondary module.
  - If a user requests a Chaldean name calculation, Pythagorean values are NEVER substituted or averaged.
  - Status: `RECONCILED_ISOLATED`.

---

### Conflict CR-002: Master Numbers (11, 22, 33) Reduction
- **Tradition A (Modern Western / Richard Craze):**
  - Preserves 11, 22, and 33 without single-digit reduction during core profile calculation.
- **Tradition B (Classical Chaldean / Indian Mulank-Bhagyank):**
  - Always reduces to root numbers (11 $\to$ 2, 22 $\to$ 4, 33 $\to$ 6) for planet assignment, while recording the compound number (11, 22, 33) for symbolic narrative interpretation.
- **Resolution & System Behavior:**
  - Deterministic engine stores **both** the compound number ($11$) and root planetary vibration ($2$).
  - UI displays the compound number alongside root planet assignment, preventing reduction ambiguity.
  - Status: `RECONCILED_DUAL_STORE`.

---

### Conflict CR-003: Lo Shu Grid vs. Vedic Kundli House Systems
- **Tradition A (Lo Shu 3x3 Magic Square):**
  - Grid based on natural digits of birth date (South=9 at top, North=1 at bottom, East=3, West=7).
  - Used for missing/repeated number plane analysis (Mental 4-9-2, Emotional 3-5-7, Practical 8-1-6).
- **Tradition B (Vedic Astrology / Nirayana Bhava Chalit):**
  - 12 Houses based on exact time of birth, geographic latitude/longitude, and Ayanamsa (Krishnamurti / Lahiri).
- **Resolution & System Behavior:**
  - **Strict Architectural Wall:** The Lo Shu Grid calculations in `app/engine/lo_shu.py` have zero overlap with astrological ascendant/house calculations.
  - Lo Shu requires only DOB (Day, Month, Year). Astrological Nirayana Bhava Chalit strictly requires verified birth time and geographic coordinates.
  - If birth time is missing, Nadi/astrology modules return `INSUFFICIENT_INPUTS` while Lo Shu completes normally.
  - Status: `STRICT_SEPARATION`.

---

### Conflict CR-004: Career Combinations (Numeros Vision Classical Archive Ch. 8 vs. Numeros Vision Classical Archive Sheet)
- **Source A (Numeros Vision Classical Archive 2013 ed., Ch. 8, pp. 109–110):**
  - Details full conditional hierarchy: Group A ($2,6,10,11 = 6,10,11 = 6,11 = 10,11 > 2,11 = 11$), Group B ($2,6,10 = 6,10$), Group C ($6 = 10 > 2$).
  - Explains the mechanism: 6th house is 12th from 7th (loss to competitor), 10th is status, 11th is gain, 2nd is liquid wealth.
- **Source B (Numeros Vision Classical Archive Summary Sheet, Page 2–3):**
  - Summarizes job as $2,6,10,11$ and business as $2,7,10,11$.
- **Resolution & System Behavior:**
  - Classical Nadi Ch. 8 is designated as **Primary Theoretical Authority**; Verma sheet is designated as **Fast-Lookup Synopsis**.
  - Engine implements Classical Nadi's full 3-tier hierarchy ($Group A > Group B > Group C$) rather than treating $2,6,10,11$ as an all-or-nothing requirement.
  - Status: `RECONCILED_HIERARCHICAL`.

---

### Conflict CR-005: Gemstone Duration & Life-Long Usage
- **Tradition A (Commercial Gemology):**
  - Frequently recommends wearing a life-stone indefinitely.
- **Tradition B (Numeros Vision Classical Archive Ch. 16, p. 232):**
  - Strictly warns that gemstones enhancing career houses (6, 10) MUST be discontinued once the job is secured, because 6 and 10 negate the 7th house of marriage ($1,6,10$ combination blocks marriage).
- **Resolution & System Behavior:**
  - **Safety-First Rule Implementation:** All gemstone outputs in Numeros Vision include mandatory discontinuation warnings and temporary timing parameters.
  - Low-cost, non-invasive lifestyle reflections are presented as standard; gemstone references are strictly marked as traditional optional notes with safety disclaimers.
  - Status: `SAFETY_RULE_ENFORCED`.

---

### Conflict CR-006: Child Gender / Sex Prediction Request
- **Traditions (Vedic / Folklore):**
  - Historical folklore attempts to associate odd/even signs or planets with male/female child births.
- **Statutory Law (PCPNDT Act 1994, India):**
  - Explicitly criminalizes any determination, prediction, or indication of the sex of an unborn child.
- **Resolution & System Behavior:**
  - **Statutory Override:** Any query regarding fetal sex prediction is instantly intercepted and `PERMANENTLY_BLOCKED`.
  - The system returns an educational statutory notification explaining the prohibition under the PCPNDT Act 1994.
  - Status: `STATUTORILY_BLOCKED`.
