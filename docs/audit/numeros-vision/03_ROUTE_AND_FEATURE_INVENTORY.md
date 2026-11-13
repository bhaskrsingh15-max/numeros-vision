# Numeros Vision — Complete Route & Feature Inventory
**Phase 1: Read-Only Audit & Baseline Gap Analysis**  
**Total Routes Catalogued:** 157 Registered Endpoints  
**Execution Timestamp:** 2026-10-16  

---

## 1. Public Website & Calculator Hub (HTML Pages)

| Route Path | Type | Method | Backing File / Handler | Functional Purpose |
|---|---|---|---|---|
| `/` | Landing | GET | `app/static/index.html` | Master homepage, brand value prop, interactive teaser, Charm AI entry |
| `/about` | Static Page | GET | `app/static/about.html` | Brand origin, methodology background, scientific boundaries |
| `/accessibility` | Compliance | GET | `app/static/accessibility.html` | WCAG 2.2 statement, keyboard navigation instructions |
| `/calculator_hub` | Hub | GET | `app/static/calculator_hub.html` | Central directory of all multi-tradition numerology calculators |
| `/calculators/` | Hub Alias | GET | `app/static/calculator_hub.html` | Canonical directory alias for calculators |
| `/calculators/birth-number` | Tool | GET | `app/static/birth_number_calculator.html` | Western & Vedic birth day reduction calculator |
| `/calculators/life-path-number`| Tool | GET | `app/static/pythagorean_calculator.html` | Master Pythagorean full date-of-birth life path tool |
| `/calculators/pythagorean` | Tool | GET | `app/static/pythagorean_calculator.html` | Pythagorean alphabet-to-number calculator |
| `/calculators/lo-shu-grid` | Tool | GET | Dynamic/`app/static/blog/...` | Interactive 3x3 Lo Shu energy planes calculator |
| `/calculators/chaldean-name-numerology` | Tool | GET | Dynamic/`app/static/blog/...` | Traditional Cheiro sound vibration calculator |
| `/calculators/business-name-numerology` | Tool | GET | Dynamic/`app/static/blog/...` | Commercial entity compound vibration assessment |
| `/calculators/mobile-number-numerology` | Tool | GET | Dynamic/`app/static/blog/...` | 10-digit mobile number total & malefic pair scanner |
| `/calculators/numerology-compatibility`| Tool | GET | Dynamic/`app/static/blog/...` | Dual-profile synastry & harmonic compatibility |
| `/calculators/personal-year-numerology`| Tool | GET | Dynamic/`app/static/blog/...` | Annual cyclical timing & personal year vibration |
| `/pricing` | Commercial | GET | `app/static/pricing.html` | Directory of 38 verified report packages & Razorpay checkout |
| `/reports_catalogue` | Commercial | GET | `app/static/reports_catalogue.html` | Sample report previews, feature comparisons |
| `/sample` | Preview | GET | `app/static/sample.html` | Full-fidelity sample individual report dossier |
| `/sample2` | Preview | GET | `app/static/sample2.html` | Sample compatibility and synastry report |
| `/sample_roadmap` | Preview | GET | `app/static/sample_roadmap.html` | Sample 12-month planetary roadmap breakdown |
| `/consultation` | Service | GET | `app/static/consultation.html` | Professional consultation booking and intake form |
| `/practitioner` | B2B Portal | GET | `app/static/practitioner.html` | Consultant portal, white-label PDF options |
| `/cdp` | Telemetry | GET | `app/static/cdp.html` | Anonymous privacy-safe profile management |
| `/dashboard` | User Portal | GET | `app/static/dashboard.html` | Authenticated client dashboard and saved reports |
| `/login` | Auth | GET | `app/static/login.html` | OTP and session login portal |
| `/signup` | Auth | GET | `app/static/signup.html` | Client account registration portal |
| `/charm_ai` | AI Chat | GET | `app/static/charm_ai.html` | Grounded Charm AI conversation assistant |
| `/privacy` | Legal | GET | `app/static/privacy.html` | DPDP Act 2023 & GDPR compliant privacy policy |
| `/terms` | Legal | GET | `app/static/terms.html` | Terms of service, cancellation, intellectual property |
| `/refund` | Legal | GET | `app/static/refund.html` | 100% digital goods refund and dispute policy |
| `/disclaimer` | Legal | GET | `app/static/disclaimer.html` | Dedicated statutory traditional interpretation notice |
| `/cookie_policy` | Legal | GET | `app/static/cookie_policy.html` | Essential cookies declaration and opt-out controls |
| `/methodology` | Technical | GET | `app/static/methodology.html` | 6-tradition calculation registry documentation |
| `/faq` | Support | GET | `app/static/faq.html` | Frequently asked questions & calculation explainers |
| `/blog/{slug}` | SEO Guides | GET | Dynamic file lookup | 24 verified authority guides in `app/static/blog/` |

---

## 2. Core REST API Endpoints

### 2.1 Numerology & Calculation Engines (`/v1` & `/api/v2`)
- `POST /v1/numbers/calculate`: Deterministic reduction for Driver, Conductor, Kua, Expression.
- `POST /v1/numbers/decode`: Traditional vibrational archetypes and planetary rulers.
- `POST /v1/correlations/analyze`: Driver-Conductor compatibility and life plane strengths.
- `POST /v1/forecast/generate`: Multi-year cyclical timing and Personal Year forecasts.
- `POST /v1/remedies/recommend`: Bounded traditional remedies (gemstones, yantras, lifestyle).
- `POST /api/v2/numerology/lo-shu/enhanced`: 8 planes analysis with missing/repeated digits.
- `POST /api/v2/numerology/naming/baby`: Auspicious letter and root vibration recommendations.
- `POST /api/v2/numerology/naming/business`: Enterprise brand name compatibility scoring.
- `POST /api/v2/numerology/assets/mobile`: 10-digit mobile number malefic sequence detection.
- `POST /api/v2/numerology/assets/vehicle`: License plate reduction and driver harmony.
- `POST /api/v2/numerology/relationships/synastry`: Dual-chart relationship synastry.

### 2.2 Monetization & Entitlements (`/api/v1/payments`)
- `GET /api/v1/payments/plans`: Authoritative list of 38 verified Razorpay offers.
- `POST /api/v1/payments/create-order`: Generates Razorpay order with currency & plan ID.
- `POST /api/v1/payments/verify`: Cryptographic HMAC SHA-256 signature verification.
- `POST /api/v1/payments/webhook`: Asynchronous transaction reconciliation.
- `GET /api/v1/payments/status/{order_id}`: Entitlement and payment state lookup.

### 2.3 Automated SEO & Image Intelligence (`/api/v1/seo-engine`)
- `GET /api/v1/seo-engine/keywords`: Prioritized search inventory with opportunity scores.
- `POST /api/v1/seo-engine/briefs/generate`: Structured brief generator with claim ledger.
- `POST /api/v1/seo-engine/pipeline/run`: 7-stage quality-governed drafting and validation.
- `POST /api/v1/seo-engine/images/render-diagram`: Deterministic Lo Shu, Chaldean, Compound seals.
- `POST /api/v1/seo-engine/images/process`: WebP optimization and responsive `<picture>` generation.
- `GET /api/v1/seo-engine/images/media-registry`: Asset provenance and SHA-256 hashes.
- `POST /api/v1/seo-engine/publishing/publish`: Idempotent static publishing with IndexNow ping.
- `POST /api/v1/seo-engine/analytics/track`: PII-stripped funnel telemetry tracker.
- `GET /api/v1/seo-engine/analytics/dashboard`: Discovery, engagement, and confirmed revenue summary.
