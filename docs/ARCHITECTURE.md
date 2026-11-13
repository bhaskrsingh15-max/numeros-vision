# Numeros Vision — System Architecture Specification
**Document Version**: 1.0.0  
**Status**: APPROVED  
**Architecture Lead**: Principal Software Architect & Application Security Lead

---

## 1. Architectural Principles

1. **Deterministic Core Primacy**:
   - Arithmetic calculations, compound reductions, planetary correlations, and matrix checks execute exclusively within pure Python deterministic modules (`app/engine/`).
   - Large Language Models (LLMs) and Generative AI are strictly confined to explanatory narrative generation and user interaction; they never calculate, rank, or alter mathematical findings.

2. **Multi-Layered Contextual Assessment**:
   - Traditional interpretations are evaluated as contextual hypotheses rather than direct causal drivers.
   - Business viability (market, operations, customer demand, unit economics) is evaluated independently from esoteric symbolism.

3. **Strict Zero-Trust Rule Governance**:
   - Every rule is an immutable or versioned data structure with explicit provenance, author, tradition, and claim type.
   - Unapproved rules remain `draft` and are barred from customer-facing scoring.

4. **Security & Privacy Defense-in-Depth**:
   - Zero secrets or internal matrices exposed to client bundles or browser consoles.
   - Per-tenant cryptographic isolation, HMAC-SHA256 authenticated sessions, and statutory DPDP 2023 consent ledgers.

---

## 2. System Architecture Diagram

```
+---------------------------------------------------------------------------------------+
|                                    CLIENT TIER                                        |
|  Responsive Web (HTML5/CSS3/Vanilla JS), PWA, Calculators, Customer Intake & Approval  |
|  Strict Palette: Venus Pearl, Jupiter Gold, Mercury Emerald | Zero Black Typography    |
+-------------------------------------------+-------------------------------------------+
                                            | HTTPS / WSS
                                            v
+---------------------------------------------------------------------------------------+
|                               API GATEWAY & SECURITY                                  |
|  FastAPI App (app/main.py), HMAC Sessions, Rate Limiting, CORS, AdTech Firewall        |
|  Statutory DPDP 2023 Consent Verification Gate (app/api/auth.py)                      |
+-------------------------------------------+-------------------------------------------+
                                            |
         +----------------------------------+----------------------------------+
         |                                                                     |
         v                                                                     v
+----------------------------------+                 +----------------------------------+
|   DETERMINISTIC ENGINE CORE      |                 |   INTELLIGENCE & ORCHESTRATION   |
|  - Core Matrix Engine (Pythagoras|                 |  - Enterprise Agent Gateway      |
|    Chaldean, Vedic, Lo Shu)      |                 |  - RAG Retriever (BM25 lexical)  |
|  - Business Taxonomy Registry    |                 |  - Source Privacy Shield         |
|  - Contextual Archetype Engine   |                 |  - Cost Accounting & Router      |
|  - Scoped Exception Evaluator    |                 |  - Diplomatic Narrative Engine   |
+-----------------+----------------+                 +-----------------+----------------+
                  |                                                    |
                  +-------------------------+--------------------------+
                                            | Validated DesignSpecification
                                            v
+---------------------------------------------------------------------------------------+
|                    GOOGLE NANO BANANA LOGO GENERATION PIPELINE                        |
|                                                                                       |
|  [DesignSpecification Compiler] ---> [Deterministic Prompt Compiler]                 |
|                                                     |                                 |
|                                                     v                                 |
|  [Google GenAI Provider Adapter] <------------------+ (Server-Side Only, Imagen 3)    |
|             |                                                                         |
|             v                                                                         |
|  [Multi-Gate Independent Validator]                                                   |
|   ├── 1. Exact Wordmark OCR & Levenshtein Check                                       |
|   ├── 2. Delta-E Palette Sampling Check                                               |
|   ├── 3. WCAG 2.1 Contrast Ratio Check                                                |
|   ├── 4. Dimension & MIME Verification                                                |
|   └── 5. Transparency / Alpha Channel Check                                           |
|             |                                                                         |
|             +---> [Pass] ---> Secure Asset Storage & Deliverable Package              |
|             |                                                                         |
|             +---> [Fail] ---> Bounded Correction Loop (Max 2 retries)                 |
|                                 └── Fallback: Deterministic SVG Vector Typesetting    |
+---------------------------------------------------------------------------------------+
```

---

## 3. Component Breakdown

### 3.1 Deterministic Engine Core (`app/engine/`)
- `core_matrix_engine.py`: Calculates Life Path/Conductor, Driver/Birth Number, First Name, Full Name, Compound Numbers, Kua Number, and Lo Shu Grids.
- `business_taxonomy.py`: Hierarchical taxonomy modeling business categories, product functions, customer outcomes, and operational intensity.
- `archetype_engine.py`: Contextual archetype engine evaluating the causal chain (`business activity → product function → customer outcome → candidate archetypes`), scoped exceptions (e.g. footwear endurance and black logo mapping), and relationship matrices.

### 3.2 AI & RAG Subsystem (`app/engine/`, `data/`)
- `rag_retriever.py`: High-speed BM25 inverted-index lexical retriever operating across 10,826 verified passages.
- `source_privacy_shield.py`: Sanitizes retrieved passages, scrubs prompt injection patterns, and redacts internal methodology keys before feeding structured data to narrative generators.

### 3.3 Google Nano Banana Logo Pipeline (`app/services/`)
- `design_specification.py`: Strict schema validation for the customer brief (exact wordmark, palette, direction, constraints, approval state).
- `prompt_compiler.py`: Deterministic compiler translating validated specifications into precise prompts, enforcing exact quoted literals, HEX roles, prohibited elements, and anti-injection guards.
- `image_provider.py`: Provider adapter communicating with Google GenAI (`imagen-3.0-generate-002`) with timeouts, retries, cost tracking ($0.030/image), and offline mock support.
- `logo_validator.py`: Independent validation engine testing OCR text match, palette fidelity, contrast ratio, dimensions, and alpha transparency.
- `vector_renderer.py`: Deterministic vector generator that typesets the exact approved wordmark with vector geometry, ensuring valid `.svg` output without ever misnaming raster images.

### 3.4 Security & Data Isolation Tier (`app/api/`, `app/security/`)
- `auth.py`: HMAC-SHA256 session management, OTP verification via SMS/Email, Google SSO tokens, and customer identity resolution.
- `cdp_identity_engine.py`: Statutory DPDP 2023 consent ledger logging consent events immutably to JSONL.
- Asset isolation: All customer assets stored in private tenant directories (`data/secure_assets/{tenant_id}/`) with signed, expiring download URLs.
