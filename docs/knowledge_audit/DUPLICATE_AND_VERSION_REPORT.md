# NUMEROS VISION & CHARM AI — DUPLICATE & VERSION REPORT
**Document Version**: 2.0.0  
**Effective Date**: 2026-10-29  
**Audit Standard**: Master Implementation Specification Section 0, 1 & 4 (Execution Contract)

---

## 1. Executive Summary & Verification Methodology

A full SHA-256 cryptographic hash scan and page-level fingerprint audit was conducted across all repository storage directories:
- `data/nadi_books/` (Nadi & BNN Corpus)
- `data/reference_books/` (Core Numerology Reference Books)
- `data/uploaded_books_and_notes/` (Legacy Uploaded Books & Notes)
- `data/transcripts/` (BNN Video & Lesson Transcripts)

### Key Duplicate Findings
- **42 total files** were scanned across all directories.
- **7 duplicate SHA-256 hash clusters** were identified.
- **4 clusters** represent bit-identical duplicate uploads of reference numerology books in downloads.
- **2 clusters** represent files existing in both `data/nadi_books/` and `data/uploaded_books_and_notes/`.
- **1 cluster** represents duplicate pagewise markdown transcriptions (`Bhrigu_Nadi_Astrology_Insights_Complete_Pagewise (1).md` and `.md`).
- **Zero near-duplicate false merges**: Distinct editions, previews, and transcriptions are strictly preserved as independent linked versions.

---

## 2. Cryptographically Proven Exact Duplicates (SHA-256 Match)

| Cluster ID | SHA-256 Hash Prefix | File Size (Bytes) | Matching Files & Locations | Operational Deduplication Action |
| :--- | :--- | :--- | :--- | :--- |
| **DUP-01** | `76b547979323...` | 83,130,171 | 1. `data/reference_books/Classical Nine-Square Lo Shu System PDF.pdf`<br>2. `data/reference_books/Classical Nine-Square Lo Shu System PDF (1).pdf` | **DEDUPLICATED**: Canonical ID `B3`. The duplicate upload `(1).pdf` is aliased to `B3-DUP` and archived. |
| **DUP-02** | `6ce32f269718...` | 42,076,006 | 1. `data/reference_books/Planetary and Number Symbolism Archive PDF Planets In Astrology Angel.pdf`<br>2. `data/reference_books/Planetary and Number Symbolism Archive PDF Planets In Astrology Angel (1).pdf` | **DEDUPLICATED**: Canonical ID `B4`. The duplicate upload `(1).pdf` is aliased to `B4-DUP` and archived. |
| **DUP-03** | `9a0f59dbdd51...` | 77,688,795 | 1. `data/reference_books/Numeros Vision Classical Numerology Manual 1945 PDF Pi Numbers.pdf`<br>2. `data/reference_books/Numeros Vision Classical Numerology Manual 1945 PDF Pi Numbers (1).pdf` | **DEDUPLICATED**: Canonical ID `B5`. The duplicate upload `(1).pdf` is aliased to `B5-DUP` and archived. |
| **DUP-04** | `ff4292e1e7bd...` | 71,535,017 | 1. `data/reference_books/Understanding Numerology Basics PDF.pdf`<br>2. `data/reference_books/Understanding Numerology Basics PDF (1).pdf` | **DEDUPLICATED**: Canonical ID `B6`. The duplicate upload `(1).pdf` is aliased to `B6-DUP` and archived. |
| **DUP-05** | `c5b46d005c81...` | 667,787 | 1. `data/nadi_books/Nadi Astrolology Combiations.pdf`<br>2. `data/uploaded_books_and_notes/Nadi Astrolology Combiations.pdf` | **LINKED & CONSOLIDATED**: Canonical ID `SRC-NADI-VERMA-SHEET`. Preserved in `data/nadi_books/` as active reference. |
| **DUP-06** | `dcf17fb7b08e...` | 5,213,892 | 1. `data/nadi_books/nadi-astrology-accurate-predictive-methodology-2013nbsped_compress.pdf`<br>2. `data/uploaded_books_and_notes/nadi-astrology-accurate-predictive-methodology-2013nbsped_compress.pdf` | **LINKED & CONSOLIDATED**: Canonical ID `SRC-NADI-Classical Nadi-2013`. Preserved in `data/nadi_books/` as active reference. |
| **DUP-07** | `cb8f69121aef...` | 268,125 | 1. `data/nadi_books/Bhrigu_Nadi_Astrology_Insights_Complete_Pagewise.md`<br>2. `data/nadi_books/Bhrigu_Nadi_Astrology_Insights_Complete_Pagewise (1).md` | **DEDUPLICATED**: Canonical ID `SRC-BNN-INSIGHTS-TRANSCRIPT`. File `(1).md` is a browser download duplicate. |

---

## 3. Near-Duplicates & Edition Lineage Analysis

The following files share conceptual topics or authors but represent **distinct editions, excerpts, or media types**. Pursuant to Section 0 Rule 2 and Section 4.1 Rule 5, they are strictly kept separate:

### 1. Numeros Vision Classical Archive Nadi Astrology: Full Book vs. Demo Extract
- **Full Book (277 pages)**: `nadi-astrology-accurate-predictive-methodology-2013nbsped_compress.pdf` (5,213,892 bytes, SHA-256: `dcf17fb7...`). Complete 2013 edition covering rules, houses, and timing.
- **Extract (36 pages)**: `Nadi Astrology by Numeros Vision Classical Archive - PDF - Astrological Sign - Divination.pdf` (2,751,222 bytes, SHA-256: `bb121efb...`). A 36-page sample extract.
- *Handling Policy*: **Do not merge**. The full 277-page text is the primary reference. The 36-page extract is tagged as an incomplete preview and excluded from rule registration.

### 2. Bhrigu Nadi Astrology Insights: Scanned PDF vs. Pagewise Markdown
- **Scanned Book (95 pages)**: `Bhrigu Nadi Astrology Insights _ PDF _ Astronomy.pdf` (55,681,530 bytes, SHA-256: `42bc9a88...`). Image scan without machine-readable text.
- **Pagewise Markdown Transcription**: `Bhrigu_Nadi_Astrology_Insights_Complete_Pagewise.md` (268,125 bytes, SHA-256: `cb8f6912...`). Full pagewise OCR transcript mapping pages 1 through 95.
- *Handling Policy*: **Linked Transcription Pair**. The scanned PDF serves as the immutable ground-truth image baseline; the Markdown transcript provides machine-readable text for internal indexing, with every claim verifiable against the corresponding PDF page.

### 3. Bhrigu Nandi Nadi Course Primer Series
- `Bhrigu Nandi Nadi Astrology Basics _ PDF...` (19 pages, 217,576 bytes)
- `Bhrigu Nandi Nadi Astrology Overview _ PDF...` (45 pages, 52,858,134 bytes)
- `Bhrigu Nandi Nadi Prediction Techniques _ PDF...` (19 pages, 3,752,337 bytes)
- *Handling Policy*: **Preserved as Distinct Modules**. These three documents represent progressive levels of an instructional course (Basics -> Overview -> Prediction Techniques). They are registered with independent IDs (`SRC-BNN-BASICS`, `SRC-BNN-OVERVIEW`, `SRC-BNN-PRED-TECH`).
