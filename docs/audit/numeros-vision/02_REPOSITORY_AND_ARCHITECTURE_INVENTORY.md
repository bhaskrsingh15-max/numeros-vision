# Numeros Vision — Repository & Architecture Inventory
**Phase 1: Read-Only Audit & Baseline Gap Analysis**  
**Execution Timestamp:** 2026-10-16  

---

## 1. Codebase & Runtime Specification

| Property | Verified Value | Evidence |
|---|---|---|
| **Operating System** | Windows 11 Pro 64-bit (10.0.26200) | `platform.platform()` |
| **Python Runtime** | Python 3.14.7 AMD64 | `sys.version` |
| **Application Framework** | FastAPI 0.141.1 (ASGI) | `pip list` |
| **Server Engine** | Uvicorn 0.53.0 (ASGI Daemon) | `app/main.py` |
| **Validation Library** | Pydantic 2.13.5 & Pydantic-Core 2.46.5 | `pip list` |
| **Image Processing** | Pillow 12.3.0 (WebP enabled) | `features.check('webp')` |
| **HTTP Client** | HTTPX 0.28.1 / Requests 2.34.2 | `pip list` |
| **Payment Gateway** | Razorpay SDK 2.0.1 | `app/api/payments.py` |
| **Document Processing** | PyPDF 6.19.0 / python-docx 1.2.0 | `pip list` |
| **Total Tracked Files** | 467 files (excl. .venv, backups) | `backups/v4.7.0` |

---

## 2. Directory Tree & Architecture Topology

```
c:\Users\Bhaskr Singh\Downloads\AI Numrology\
├── app/
│   ├── main.py                          # FastAPI ASGI entry point (157 routes)
│   ├── api/                             # REST API Routers
│   │   ├── auth.py                      # Session & authentication management
│   │   ├── b2b.py                       # Enterprise & partner integrations
│   │   ├── bookings.py                  # Consultant consultation scheduling
│   │   ├── cdp.py                       # Customer Data Platform tracking
│   │   ├── cost_governance.py           # Token accounting & budget limits
│   │   ├── numerology_v2.py             # Extended v2 numerology APIs
│   │   ├── payments.py                  # Razorpay checkout, verification, 38 offers
│   │   ├── premium.py                   # Subscription & VIP report generation
│   │   ├── privacy.py                   # DPDP Act 2023 consent & data export
│   │   ├── readings.py                  # Core numerological readings & consensus
│   │   ├── seo_engine_api.py            # Automated SEO & Image management API
│   │   └── v1_master_api.py             # Master unified numerology endpoint
│   ├── engine/                          # Deterministic Business Logic & RAG
│   │   ├── adtech_firewall.py           # Ad-network tracking blocker
│   │   ├── asset_numerology_engine.py   # Vehicle, home, bank account vibration
│   │   ├── astrology_correlation_engine.py # Planetary conjunctions & transits
│   │   ├── bnn_numerology_engine.py     # Bhrigu Nandi Nadi synthesis
│   │   ├── cdp_identity_engine.py       # Anonymous identity resolution
│   │   ├── cheiro_engine.py             # Cheiro Chaldean double numbers (10-52)
│   │   ├── claim_validator.py           # Copy linter & anti-hallucination checks
│   │   ├── consensus.py                 # Cross-school multi-tradition synthesis
│   │   ├── core_matrix_engine.py        # Driver (Mulank), Conductor (Bhagyank)
│   │   ├── enhanced_lo_shu_engine.py    # 8 Lo Shu planes & directional remedies
│   │   ├── enterprise_agent_gateway.py  # Charm AI orchestrated agent router
│   │   ├── forecast_engine.py           # Personal Year/Month/Day & cycles
│   │   ├── lo_shu.py                    # Classical 3x3 magic square builder
│   │   ├── master_knowledge_engine.py   # Unified methodology registry lookup
│   │   ├── pythagorean_engine.py        # Western Pythagorean 1-9 calculations
│   │   ├── rag_retriever.py             # 10,826 passage vector/corpus retriever
│   │   ├── remedy_engine.py             # Gemstone, yantra, directional remedies
│   │   ├── source_privacy_shield.py     # IP protection & citation redaction
│   │   └── zero_cost_llm.py             # Template & fallback offline responder
│   ├── security/                        # Application Protection
│   │   ├── anonymizer.py                # PII scrubber & pseudonymizer
│   │   ├── cyber_defense.py             # CyberDefenseMiddleware (WAF, anti-abuse)
│   │   └── logger.py                    # Structured audit logging
│   ├── seo/                             # Content Automation Subsystem
│   │   ├── connectors/                  # AnswerThePublic & IndexNow adapters
│   │   ├── images/                      # Deterministic diagram & WebP optimizer
│   │   ├── pipeline/                    # 7-stage content generator & quality gates
│   │   └── opportunity_scorer.py        # 0-100 normalized search opportunity score
│   └── static/                          # Static Frontend & Media Assets
│       ├── blog/                        # 24 live static SEO authority guides
│       ├── css/                         # theme.css & roadmap_components.css
│       ├── icons/                       # PWA icons (192, 512, maskable)
│       ├── images/seo/                  # Deterministic WebP diagrams & seals
│       ├── js/                          # Client-side validation & interactivity
│       ├── logos/                       # SVG brand marks, Charm AI logo, Yantras
│       └── *.html                       # 36 static pages (index, calculators, legal)
├── data/                                # Persistent Ledgers & Corpus
│   ├── knowledge_base/                  # 10,826-passage canonical corpus & sources
│   ├── conversion_events.jsonl          # Privacy-safe funnel telemetry
│   ├── indexing_events.jsonl            # IndexNow audit submissions
│   ├── keyword_expansion_inventory.json # 71 cluster search queries
│   ├── media_registry.json              # Visual asset ledger & SHA-256 hashes
│   ├── offer_registry.json              # 38 verified Razorpay offers
│   ├── payments.jsonl                   # Verified transaction records
│   └── verified_sessions.json           # Active authenticated sessions
└── tests/                               # 24 Test Suites (154 Passing Tests)
```

---

## 3. Storage & Persistence Layer

The application operates an air-gapped, zero-external-dependency JSON/JSONL persistence architecture designed for enterprise data isolation:
- **`data/payments.jsonl`**: Immutable transaction log recording Razorpay order IDs, payment IDs, offer IDs, amounts, and HMAC verification timestamps.
- **`data/conversion_events.jsonl`**: Anonymized telemetry events (`organic_landing`, `calculator_completed`, `package_viewed`, `purchase_confirmed`) stripped of customer PII.
- **`data/media_registry.json`**: Media asset provenance ledger tracking SHA-256 content hashes, responsive dimensions, and accessibility status.
- **`data/offer_registry.json`**: Authoritative repository of all 38 verified pricing packages and report entitlements.
- **`data/verified_sessions.json`**: Ephemeral secure sessions with 24-hour expiry and cryptographic token validation.
