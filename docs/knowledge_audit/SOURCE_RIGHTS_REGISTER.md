# NUMEROS VISION & CHARM AI — SOURCE RIGHTS & PERMISSIONS REGISTER
**Document Version**: 2.0.0  
**Effective Date**: 2026-10-29  
**Audit Standard**: Master Implementation Specification Section 0 & 3 (Execution Contract)

---

## 1. Statutory Compliance & IP Rights Policy

Pursuant to Section 0 (Rule 7) of the Master Implementation Specification:
1. **Internal Access ≠ Redistribution**: Possession of an internal PDF file or reference scan in developer storage does not grant permission for customer-facing verbatim redistribution, public source quotation, model pre-training, or third-party syndication.
2. **Proprietary Rule Isolation**: All rule extraction, algorithmic scoring weights, planetary transit models, and internal prompt templates remain strictly **server-side**.
3. **Permission Gate**: Production ingestion into customer-facing RAG retrieval requires explicit permission verification. Sources classified as `pending_review` or `restricted` are restricted exclusively to `internal_research` and deterministic logic modeling.

---

## 2. Comprehensive Source Rights Inventory

### Category 1: Nadi Astrology & BNN Multi-Branch Corpus (`data/nadi_books/`)

| Source ID | Canonical Title & File | Author / Attribution | Doc Type | Rights Status | Allowed Uses | Ingestion Gate | Review Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SRC-NADI-NOTES-2026** | *Nadi Notes: Compiled Multi-Branch Nadi & BNN Analysis* (`Nadi Notes PDF Books Prediction.pdf`) | Compiled Expert Analysis (82 pp) | Secondary Analysis | `pending_review` | `internal_research` | **APPROVED FOR ARCHITECTURAL MODELING ONLY** | High-value comparative analysis distinguishing BNN (karaka-first) from Bhrigu Prashna (107 lookup). Serves as software architecture guide; secondary claims require primary source verification. |
| **SRC-NADI-Classical Nadi-2013** | *Numeros Vision Classical Nadi Event System* (`nadi-astrology-accurate-predictive-methodology-2013nbsped_compress.pdf`) | Numeros Vision Classical Archive (2013 Edition, 277 pp) | Primary Book | `pending_review` | `internal_research` | **RESTRICTED TO INTERNAL RESEARCH** | Full 277-page text on KP-Nadi sub-lord combinations. Commercial customer quotation requires publisher clearance. |
| **SRC-NADI-VERMA-SHEET** | *Nadi Astrology Combinations Reference Sheet* (`Nadi Astrolology Combiations.pdf`) | Numeros Vision Classical Archive / Classical Nadi Archive (3 pp) | Reference Sheet | `pending_review` | `internal_research` | **APPROVED FOR HEURISTIC CROSS-CHECK** | Compact 3-page event reference. Compact combinations cannot be treated as universal laws. |
| **SRC-NADI-Classical Nadi-EXTRACT** | *Nadi Astrology by Numeros Vision Classical Archive Extract* (`Nadi Astrology by Numeros Vision Classical Archive - PDF - Astrological Sign - Divination.pdf`) | Numeros Vision Classical Archive (36 pp) | Book Extract | `restricted` | `internal_research` | **BLOCKED (PARTIAL PREVIEW)** | Incomplete 36-page demo extract. Section 0 Rule 2 blocks partial previews from primary rule generation. |
| **SRC-BNN-BASICS** | *Bhrigu Nandi Nadi Astrology Basics* (`Bhrigu Nandi Nadi Astrology Basics _ PDF...pdf`) | Unknown / Course Notes (19 pp) | Course Notes | `pending_review` | `internal_research` | **APPROVED FOR LOGIC EXTRACTION** | Digital text available. Focuses on planetary signification and basic combinations. |
| **SRC-BNN-OVERVIEW** | *Bhrigu Nandi Nadi Astrology Overview* (`Bhrigu Nandi Nadi Astrology Overview _ PDF...pdf`) | Unknown / Course Notes (45 pp) | Course Notes | `pending_review` | `internal_research` | **APPROVED FOR LOGIC EXTRACTION** | Digital text available. Detailed 45-page planetary pairing catalog. |
| **SRC-BNN-PRED-TECH** | *Bhrigu Nandi Nadi Prediction Techniques* (`Bhrigu Nandi Nadi Prediction Techniques _ PDF...pdf`) | Unknown / Course Notes (19 pp) | Course Notes | `pending_review` | `internal_research` | **APPROVED FOR LOGIC EXTRACTION** | Explores Jupiter and Saturn transit rounds and age bands. |
| **SRC-BNN-INSIGHTS-SCAN** | *Bhrigu Nadi Astrology Insights* (`Bhrigu Nadi Astrology Insights _ PDF _ Astronomy.pdf`) | Unknown (95 pp) | Scanned Book | `restricted` | `internal_research` | **BLOCKED FROM RAG (SCANNED)** | 95-page scanned volume. Full text transcribed in adjacent markdown file. |
| **SRC-BNN-INSIGHTS-TRANSCRIPT**| *Bhrigu Nadi Astrology Insights Complete Pagewise Markdown* (`Bhrigu_Nadi_Astrology_Insights_Complete_Pagewise.md`) | Verified OCR Transcription (268 KB) | Transcript | `approved_internal` | `internal_research`, `retrieval` | **APPROVED FOR INTERNAL RETRIEVAL** | Clean machine-readable pagewise transcription of the 95-page BNN insights book. |

---

### Category 2: Core Numerology Reference Books (`data/reference_books/`)

| Source ID | Canonical Title & File | Author / Attribution | Doc Type | Rights Status | Allowed Uses | Ingestion Gate | Review Notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **B1** | *Numeros Vision Classical Sound and Name Compendium* (2005) | Classical Chaldean Tradition / Classical Chaldean (188 pp) | Scanned Book | `pending_review` | `internal_research` | **BLOCKED FROM RAG (PENDING OCR)** | Scanned volume. Sound vibration rationale modeled in `formula_registry.json`. |
| **B2** | *Chaldean Numerology: Structured Learning Reference* | Pythagoras / Classical Chaldean (133 pp) | Digital Text Book | `approved_internal` | `internal_research`, `retrieval`, `customer_answers` | **APPROVED FOR CANONICAL RETRIEVAL** | 133 pages with full machine-readable text and 31-section Table of Contents. Primary Chaldean learning reference. |
| **B3** | *Numeros Vision Classical Nine-Square Lo Shu System* (1998) | Classical Chinese / Lo Shu (276 pp) | Scanned Book | `pending_review` | `internal_research` | **BLOCKED FROM RAG (PENDING OCR)** | Scanned volume. 3x3 Magic Square coordinates deterministically codified in `formula_registry.json`. |
| **B4** | *Numeros Vision Planetary and Number Symbolism Archive* | Esoteric Numerology (116 pp) | Scanned Book | `pending_review` | `internal_research` | **BLOCKED FROM RAG (PENDING OCR)** | Scanned volume. Historical planetary symbolism. |
| **B5** | *Numeros Vision Classical Numerology Manual* (1945 Edition) | Historic 1945 Volume (200 pp) | Scanned Book | `public_domain_candidate` | `internal_research` | **BLOCKED FROM RAG (PENDING OCR)** | Historic 1945 publication. Mathematical constants and number magic. |
| **B6** | *Understanding Numerology: The Power to Know Anybody* | Introductory Numerology (148 pp) | Scanned Book | `pending_review` | `internal_research` | **BLOCKED FROM RAG (PENDING OCR)** | Scanned volume. Introductory treatments. |

---

## 3. Strict Permission Gates & Approval Protocol

```
                                [Source File Discovery]
                                           │
                                           ▼
                            [Permission & License Review]
                                ├─────────────────────────┐
                                ▼                         ▼
                     [Rights Approved / Fair Use]    [Rights Unknown / Partial]
                                │                         │
                                ▼                         ▼
                    [Text Extractability Check]     [Flagged: RESTRICTED]
                      ├────────────────────┐              │
                      ▼                    ▼              ▼
             [Searchable Text]     [Image-Only Scan]  [INTERNAL RESEARCH ONLY]
                      │                    │          [BLOCKED FROM PRODUCTION RAG]
                      ▼                    ▼
             [Internal RAG Pool]   [OCR Verification]
                      │                    │
                      ▼                    ▼
             [Production Release] ──► [Needs Review]
```

### Mandatory Rules for Production Release
1. **Zero Unapproved Text in Customer Prompt Context**: Unapproved or rights-restricted material must never be injected into public customer-facing prompts or public APIs.
2. **Deterministic Engine Independence**: Calculation formulas (Chaldean letter values, Pythagorean reductions, BNN 7-factor field analysis, Lo Shu planes) are abstract mathematical concepts and can safely be codified into Python algorithms without copyright infringement, provided no verbatim literary text is reproduced.
3. **Opt-in Commercial Clearing**: Any commercial publication of direct quotations exceeding standard fair-use scholarship excerpts requires written rights clearance from the respective copyright holders.
