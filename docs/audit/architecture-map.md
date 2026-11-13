# Numeros Vision — Architecture Map & System Topology
**Repository:** `Numeros Vision (AI Numerology)`  
**Document ID:** `docs/audit/architecture-map.md`  
**Specification Reference:** `NUMEROS_VISION_MASTER_IMPLEMENTATION.md` Section 2  
**Brand Signature:** Numeros Vision | Unveil Every Charm

---

## 1. High-Level Logical Architecture

```mermaid
flowchart TD
    subgraph CLIENT_TIERS["Client Access Interfaces"]
        WEB["Public Website\n(Homepage, Calculators, SEO Hubs, Trust Pages)"]
        APP["Customer Application\n(Dashboard, Charm AI, Personal Dossiers)"]
        PDA["Practitioner Workspace & CRM (PDA)\n(/practitioner, Client Dossiers, Rectification)"]
    end

    subgraph SECURITY_PERIMETER["Perimeter Security & WAF"]
        WAF["CyberDefenseMiddleware\n(Scraper Bot Blocker, SQLi/XSS Filter, Prompt Injection Shield, 256KB Limiter)"]
        CONSENT["Privacy & Consent Engine\n(DPDP Act 2023, EU GDPR, Essential Cookies Only)"]
    end

    subgraph ROUTER_LAYER["FastAPI Application Routers"]
        R_MASTER["v1_master_router\n(/api/v1/* calculations & contact)"]
        R_READINGS["readings_router\n(/api/v1/readings/ask, /remedies)"]
        R_PAYMENTS["payments_router\n(/api/v1/payments/* Razorpay order & webhook)"]
        R_V2["numerology_v2_router\n(Comprehensive 9-Engine Synthesis)"]
        R_SEO["seo_engine_router\n(Ranking scanner & content automation)"]
        R_AUTH["auth_router & cdp_router\n(Customer & Practitioner Session Tokens)"]
    end

    subgraph DETERMINISTIC_ENGINES["Deterministic Calculation Engines (No LLM)"]
        E_CORE["Core Matrix (Driver & Conductor)"]
        E_LOSHU["Lo Shu Grid & 8 Planes"]
        E_CHALDEAN["Chaldean / Cheiro Sound Matrix"]
        E_PYTHAG["Pythagorean Matrix"]
        E_MOBILE["Mobile Number Vibration & Malefic Pairs"]
        E_NAME["Name Balancing & Spelling Calibration"]
        E_REPORT["Package Report Generator (Tier Reports)"]
    end

    subgraph GOVERNED_AI["Governed AI & RAG Retreival Engine"]
        RAG_RETRIEVER["Inverted Index RAG Retriever\n(10,826 Passages, 31,537 Terms, <5ms Query)"]
        CLAIM_LEDGER["Claim Verification & Grounding Validator\n(Zero-Hallucination Guardrail)"]
        ORCHESTRATOR["Question Orchestrator\n(Vedic + Chaldean Consensus Reading)"]
    end

    subgraph DATA_STORAGE["Data & Persistence Layer"]
        FILE_SESSIONS["Verified Sessions Store\n(verified_sessions.json)"]
        CDP_STORE["CDP Identities & Consent Store\n(cdp_identities.json)"]
        PASSAGES_CORPUS["Classical Corpus Knowledge Base\n(10,826 verified texts)"]
        SECRETS_ENV[".env Secrets Store\n(Razorpay, WAF, Redis, Admin)"]
    end

    CLIENT_TIERS --> SECURITY_PERIMETER
    SECURITY_PERIMETER --> ROUTER_LAYER
    ROUTER_LAYER --> DETERMINISTIC_ENGINES
    ROUTER_LAYER --> GOVERNED_AI
    GOVERNED_AI --> DETERMINISTIC_ENGINES
    GOVERNED_AI --> PASSAGES_CORPUS
    ROUTER_LAYER --> DATA_STORAGE
```

---

## 2. Component Boundaries & Responsibilities

### 2.1 Public Website Layer
- **Responsibility:** Discoverability, educational content, top-of-funnel lead generation, free instant diagnostics, and brand building.
- **Components:**
  - `app/static/index.html`: Unified homepage with instant hero Mulank/Bhagyank calculator, 9-layer preview, and Charm AI chat box.
  - `app/static/calculators.html` & specific tool pages: `/tools/name-balancing`, `/tools/mobile-numerology`, etc.
  - `app/static/blog/*.html` & `/blog/what-is-numerology`: High-authority SEO pillar guides and spoke articles.
  - Trust & Legal Pages: `/about`, `/methodology`, `/privacy`, `/terms`, `/refund-policy`, `/disclaimer`.

### 2.2 Customer Application Layer
- **Responsibility:** Post-calculation exploration, conversational querying, report purchasing, and profile preservation.
- **Components:**
  - `app/static/charm_ai.html`: Dedicated conversational AI portal backed by sub-55ms grounded RAG.
  - `app/static/dashboard.html`: Authenticated customer profile, saved calculation charts, and active question credits.
  - `app/static/sample2.html`: Mobile app preview demonstrating responsive luxury UI/UX and PWA compatibility.

### 2.3 Practitioner Workspace & CRM (PDA)
- **Responsibility:** B2B expert workstation for professional numerologists and consultants.
- **Components:**
  - `app/static/practitioner.html`: Multi-client management, Birth Time Rectification notes, personalized yantra drafting, and consultation scheduler.
  - `app/api/auth.py`: Practitioner credential validation, role checking (`practitioner`, `admin`).
  - `app/api/numerology_v2.py`: Deep 40-syllabus diagnostic outputs for professional clients.

### 2.4 Shared Application Services & Deterministic Engines
- **Responsibility:** Mathematical calculations that must NEVER hallucinate or fluctuate.
- **Rule:** 100% pure Python arithmetic without language model invocation.
- **Modules in `app/engine/`:**
  - `core_matrix.py`: Mulank (Driver, 1-9) and Bhagyank (Conductor, 1-9) calculation.
  - `cheiro_engine.py` & `chaldean_table.py`: Ancient Chaldean compound vibrations (10-52).
  - `pythagorean_engine.py`: Western reduction and master numbers (11, 22, 33).
  - `loshu_grid.py`: 3x3 Magic Square and 8 Planes analysis.
  - `name_balancer.py`: Calling name vs legal name vibrational harmonizer.
  - `package_report_generator.py`: Commercial multi-chapter dossier synthesis.

### 2.5 Governed RAG & AI Orchestrator
- **Responsibility:** Conversational synthesis, classical citations, planetary root-cause explanations, and consecrated remedies.
- **Modules:**
  - `rag_retriever.py`: Inverted index over 10,826 classical passages across 31,537 distinct terms with query caching (4.5ms lookup).
  - `consensus.py`: Multi-engine astrological consensus reading generator.
  - `ai_cost_and_security.py`: Section 15.4 deterministic gating, plan-based usage metering, and prompt injection defense.

### 2.6 Payment & Order Lifecycle
- **Responsibility:** Secure, idempotent commercial monetization.
- **Modules:**
  - `app/api/payments.py`: Razorpay order creation (`/create-order`), HMAC-SHA256 webhook signature verification (`/webhook`), session credit issuance (`consume_question`, `get_session_info`), and refund tracking.

---

## 3. End-to-End Request Lifecycle

```mermaid
sequenceDiagram
    autonumber
    actor User as Client / Searcher
    participant WAF as CyberDefenseMiddleware
    participant API as FastAPI Router
    participant Engine as Deterministic Engines
    participant RAG as Inverted Index RAG
    participant Pay as Razorpay Gateway
    participant Store as Session & CDP Store

    User->>WAF: POST /api/v1/readings/ask (Question + Birth Profile)
    WAF->>WAF: Verify User-Agent, Scraper Check, SQLi/XSS Filter, Payload <256KB
    alt Malicious Request Detected
        WAF-->>User: HTTP 400/403 Blocked
    else Legitimate Request
        WAF->>API: Forward sanitized request
    end

    API->>Store: Validate token & question credits (test_master_pass / paid pass)
    API->>Engine: Calculate Driver (Mulank) & Conductor (Bhagyank)
    Engine-->>API: Deterministic numbers & ruling planets

    API->>RAG: Query 10,826 passages via Inverted Term Index
    RAG-->>API: Top-3 grounded classical excerpts (<5ms)

    API->>Engine: Synthesize planetary root-cause & multi-layer remedies
    Engine-->>API: Structured alignment summary & consecrated upay

    API->>Store: Decrement question credit (if metered) & log trace ID
    API-->>User: HTTP 200 OK (<55ms Latency) with full branded response
```

---

## 4. Environment Configuration & Security Perimeter

- **Development/Staging:** `ENVIRONMENT=development`, test tokens enabled (`test_master_pass`), WAF actively enforcing all defenses.
- **Production Mode:** Strict origin restriction (`https://numerosvision.com`), test token bypass disabled, SSL/TLS termination, secure cookies, and no-server-header cloaking.
