# Numeros Vision — Current State Architecture Audit
**Specification Reference:** Numeros Vision + Charm AI Master Implementation Specification
**Document Type:** Architecture Baseline Audit
**Audit Date:** October 2026
**Status:** Operational / Verified

## 1. Executive Summary
Numeros Vision is an operational, high-performance, deterministic AI-assisted numerology and astrology platform. It synthesizes classical Vedic (Ank Jyotish), Chaldean (Cheiro canon), Pythagorean/Western, Chinese Lo Shu 3x3 Magic Square, and astrological traditions (Krishnamurti Paddhati, Bhrigu Nandi Nadi, Lal Kitab, and Vedic Parashari Jyotish) using pure Python deterministic calculation engines, grounded RAG retrieval, and an empathetic, layman-friendly AI layer (Charm AI).

## 2. Technology Stack & Runtime Inventory
- **Backend Runtime:** Python 3.12+ in dedicated virtual environment (`.\.venv\Scripts\python.exe`)
- **Web Framework:** FastAPI (async REST API, Starlette middleware, Pydantic v2 schemas)
- **ASGI Server:** Uvicorn on port 8000 (Daemon mode, host 127.0.0.1)
- **Tunnels / Public Delivery:** Cloudflare Tunnel (`trycloudflare.com`) & SSH Tunnel (`lhr.life`)
- **Frontend Architecture:** Semantic HTML5 + Vanilla ES6+ JavaScript + CSS3 custom properties; zero frontend bloat; sub-100ms LCP.
- **Brand Palette:** Venus Pearl (`#FFFDF7`), Jupiter Gold (`#C9A227`), Sandalwood Ink (`#523E28`), Deep Obsidian (`#1A1714`).
- **Brand Signature & Tagline:** Numeros Vision · *"Anveil Every Charm"* / *"Unveil Every Charm"*
- **Deterministic Engines (`app/engine/`):**
  - `core_matrix_engine.py`: Driver (1-9), Conductor (preserving 11, 22, 33), Kua, Dasha, repeat/missing numbers.
  - `enhanced_lo_shu_engine.py` & `lo_shu.py`: 3x3 Magic square and 8 planes of expression.
  - `cheiro_engine.py` & `name_balancing_engine.py`: Chaldean name analysis & compound numbers 10-52.
  - `pythagorean_engine.py`: Western Life Path, Expression, Soul Urge, Karmic Debt (13, 14, 16, 19).
  - `bnn_numerology_engine.py`: Bhrigu Nandi Nadi planetary combinations.
  - `astrology_correlation_engine.py`: KP Sub-Lord, Lal Kitab Masnooi, Vedic Jyotish Yogas, Horas, Transits.
  - `remedy_rules_engine.py`: 5-tier explainable remedies, Yantra catalogue, enemy exclusions.
  - `rag_retriever.py`: Inverted index over 10,826 classical passages, sub-2ms retrieval.
  - `source_privacy_shield.py`: Masking internal file paths and author references.
  - `claim_validator.py`: Anti-hallucination and claim-level verification gate.
- **Test Suite Status:** 169 / 169 tests passing (100% OK), end-to-end QC passing 109 / 109 checks.
