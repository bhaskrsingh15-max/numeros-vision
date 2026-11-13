# Numeros Vision - Master Acceptance Criteria & Definition of Done
**Specification Reference**: `NUMEROS_VISION_MASTER_IMPLEMENTATION.md` (Sections 3–22)  
**Brand Identity**: Numeros Vision | *Unveil Every Charm*  
**Date**: October 2026  
**Status**: APPROVED - ENGINEERING STANDARD

---

## 1. Overview & Evaluation Protocol

This document establishes the precise, unambiguous, and verifiable acceptance criteria for every subsystem across the **Numeros Vision** platform. Each criterion specifies:
- **Test ID**: Unique traceable requirement identifier.
- **Verification Method**: Automated unit test, integration test, security probe, or visual audit.
- **Pass Threshold**: Exact quantitative or qualitative standard required for sign-off.
- **Failure Classification**: Blocker (prevents release) vs. Minor (advisory).

---

## 2. Subsystem Acceptance Criteria

### 2.1 Technical SEO & Discoverability
| Criteria ID | Requirement | Verification Method | Pass Threshold | Severity |
|:---|:---|:---|:---|:---:|
| **AC-SEO-01** | Canonical Tag Consistency | Automated HTML parser on all 43 roadmap URLs | Exactly 1 self-referential canonical URL per page matching domain structure. No query parameters in canonical. | Blocker |
| **AC-SEO-02** | Structured Data (Schema.org) | Google Rich Results validator / Schema.org linter | 0 errors, 0 warnings. `WebSite`, `Organization`, `FAQPage`, and `BreadcrumbList` valid on all content pages. | Blocker |
| **AC-SEO-03** | Meta Title & Description Integrity | Automated crawler regex | Titles: 50–60 chars, includes target keyword & "Numeros Vision". Descriptions: 145–160 chars with compelling CTA. | Blocker |
| **AC-SEO-04** | Heading Hierarchy (H1-H4) | DOM tree traversal | Exactly 1 `<h1>` per page. Strict hierarchical nesting without skipped levels. | High |
| **AC-SEO-05** | Internal Linking Network | Graph validator over internal links | Each of the 43 target pages receives $\ge 3$ inbound internal links from thematic cluster pages and links to relevant calculators. | Blocker |
| **AC-SEO-06** | XML Sitemap & Robots.txt | HTTP GET `/sitemap.xml` and `/robots.txt` | Returns HTTP 200 with valid XML syntax. Disallows `/admin`, `/api/`, and private endpoints while allowing all public URLs. | Blocker |
| **AC-SEO-07** | Core Web Vitals (LCP, CLS, INP) | Lighthouse CLI automated audit | LCP $\le 2.5\text{s}$, CLS $\le 0.1$, INP $\le 200\text{ms}$ on desktop and mobile. Performance score $\ge 90$. | High |

---

### 2.2 Deterministic Numerology Calculation Engine
| Criteria ID | Requirement | Verification Method | Pass Threshold | Severity |
|:---|:---|:---|:---|:---:|
| **AC-NUM-01** | Cheiro Calculation Precision | Known-Answer Unit Tests (`test_golden_calculations.py`) | 100% agreement with manual Cheiro Chaldean tables (`A=1, B=2... I=1, J=1... O=7, P=8...`). Alphabet excludes 9. Compound numbers 10 to 52 resolved verbatim. | Blocker |
| **AC-NUM-02** | Pythagorean Calculation Precision | Known-Answer Unit Tests | 100% agreement with standard Pythagorean 1–9 cycle. Full name, soul urge (vowels), and personality (consonants) calculate accurately. | Blocker |
| **AC-NUM-03** | Master Number Preservation | Edge-case boundary tests | Master numbers `11`, `22`, and `33` are preserved during sub-reductions and flagged with compound master designations. | Blocker |
| **AC-NUM-04** | Lo Shu 3x3 Magic Square | Matrix plane validator | Correct digit distribution into 3x3 grid: `4-9-2`, `3-5-7`, `8-1-6`. Accurately identifies complete planes (Mental, Emotional, Practical) and missing numbers. | Blocker |
| **AC-NUM-05** | Calculation Engine Isolation | Source code audit | Zero generative AI or dynamic LLM calls present inside `app/engine/`. Calculations are 100% deterministic and stateless. | Blocker |

---

### 2.3 Governed Charm AI & RAG Retrieval
| Criteria ID | Requirement | Verification Method | Pass Threshold | Severity |
|:---|:---|:---|:---|:---:|
| **AC-RAG-01** | Retrieval Latency | Benchmark timer over 1,000 queries | Average inverted index retrieval time $\le 10\text{ms}$. LRU cache hit time $\le 2\text{ms}$. Total end-to-end response time $\le 100\text{ms}$. | Blocker |
| **AC-RAG-02** | Evidence Grounding & Zero Hallucination | Adversarial prompt suite | 100% of predictions must cite canonical numerological texts (`[CHALDEAN_TEXT_01]`, `[PYTHAGOREAN_TREATISE]`). Non-canonical claims (fatalism, medical cure) rejected with disclaimer. | Blocker |
| **AC-RAG-03** | Calculator Data Hand-off | Integration test (`test_charm_ai_perf_and_ui.py`) | Form input from calculator or test page passes calculated core matrix payload seamlessly to Charm AI consultation without data loss. | Blocker |
| **AC-RAG-04** | Brand Voice & Identity in AI Responses | NLP tone evaluation | Tone is warm, empowering, analytical, and respectful. Includes official tagline *"Unveil Every Charm"* and signs off as "Numeros Vision Charm AI". | High |

---

### 2.4 Brand, UI/UX & Design System
| Criteria ID | Requirement | Verification Method | Pass Threshold | Severity |
|:---|:---|:---|:---|:---:|
| **AC-UI-01** | Palette Consistency | Automated CSS token scan | Only design system tokens utilized: Venus Pearl (`#FFFDF7`), Warm Ivory (`#FAF6EE`), Jupiter Gold (`#C9A227`, `#8B6914`), Sandalwood Ink (`#523E28`), Emerald Accent (`#16835B`). Zero raw black (`#000000`). | Blocker |
| **AC-UI-02** | Official Logo & Tagline | Visual regression & DOM check | Official SVG/PNG logo rendered with exact aspect ratio. Exact brand tagline displayed: **Numeros Vision | Unveil Every Charm**. | Blocker |
| **AC-UI-03** | Typography Discipline | Computed style linter | Headings: `Cinzel, serif`. Body text: `Plus Jakarta Sans, sans-serif`. Proper line heights and readable contrast ratios ($\ge 4.5:1$). | Blocker |
| **AC-UI-04** | WCAG 2.2 AA Compliance | Axe-core automated audit | 0 critical or serious accessibility violations. All interactive elements have focus rings, keyboard navigability, and ARIA labels. | High |
| **AC-UI-05** | Mobile Responsiveness | Viewport testing (320px, 375px, 768px, 1024px, 1440px) | Zero horizontal scrolling or broken flex/grid containers across all breakpoints. Hamburger navigation functions smoothly on mobile. | Blocker |

---

### 2.5 Customer App & Personal Destiny Application (PDA)
| Criteria ID | Requirement | Verification Method | Pass Threshold | Severity |
|:---|:---|:---|:---|:---:|
| **AC-APP-01** | User Destiny Dossier Dashboard | End-to-end user session flow | User can input birth details and instantly view full Core Matrix, Lo Shu Grid, Pinnacles, Challenges, and Yearly Forecast. | Blocker |
| **AC-APP-02** | Seamless Charm AI Consultation Tab | Interactive UI automated test | Clicking "Ask Charm AI" opens the consultation drawer pre-populated with user's specific Life Path and Destiny numbers. | Blocker |
| **AC-APP-03** | Destiny Blueprint Download | PDF generation check | User can download high-resolution PDF Destiny Blueprint matching their personalized calculations within 3 seconds. | High |

---

### 2.6 Practitioner Dashboard Application (PDA Workspace)
| Criteria ID | Requirement | Verification Method | Pass Threshold | Severity |
|:---|:---|:---|:---|:---:|
| **AC-PDA-01** | Client Dossier Management | Practitioner CRUD test | Certified consultant can search, view, and organize client profiles, calculation matrices, and historic consultations. | Blocker |
| **AC-PDA-02** | Birth Time Rectification Notes | Practitioner form test | Practitioner can record notes on events and adjust rectification timestamps with instant delta matrix recalculation. | High |
| **AC-PDA-03** | Custom Yantra & Remedy Studio | Visual rendering test | Practitioner can generate customized planetary yantras based on missing numbers in client's Lo Shu grid. | High |

---

### 2.7 Payment & Order Security
| Criteria ID | Requirement | Verification Method | Pass Threshold | Severity |
|:---|:---|:---|:---|:---:|
| **AC-PAY-01** | HMAC Signature Verification | Razorpay webhook test suite | 100% of webhook requests lacking valid `X-Razorpay-Signature` are rejected with HTTP 400. Valid signatures processed immediately. | Blocker |
| **AC-PAY-02** | Order Idempotency | Duplicate webhook replay test | Replaying the same payment webhook multiple times produces exactly 1 order fulfillment and 1 PDF generation. Zero duplicate credits. | Blocker |
| **AC-PAY-03** | Currency & Product Pricing | Gateway integration test | Displayed pricing matches Razorpay order amount exactly (INR / USD / EUR / GBP). Zero price tampering possible via client payloads. | Blocker |

---

### 2.8 Cyber Defense & Statutory Privacy
| Criteria ID | Requirement | Verification Method | Pass Threshold | Severity |
|:---|:---|:---|:---|:---:|
| **AC-SEC-01** | AI Scraper Bot Defense | User-Agent & bot probe test | Known scrapers (GPTBot, CCBot, ClaudeBot, Bytespider, PetalBot) blocked with HTTP 403 Forbidden. | Blocker |
| **AC-SEC-02** | Payload Inspection & WAF Rules | Security injection suite (31 tests) | SQLi, XSS, Path Traversal, and Prompt Injection payloads blocked with HTTP 403. Maximum payload size enforced at 256KB. | Blocker |
| **AC-SEC-03** | DPDP Act 2023 & GDPR Consent | Consent API test (`/api/v1/consent`) | Explicit consent recorded with timestamp, IP hash, and purpose. User can request data deletion with immediate record purge. | Blocker |
| **AC-SEC-04** | Zero Secret Exposure | Static code & git commit analysis | No API keys, passwords, database credentials, or secret tokens exposed in client code, test fixtures, or public files. | Blocker |

---

## 3. Definition of Done (Release Gate Checklist)

Before promoting any feature or release branch to Production Staging:
- [x] All Unit, Integration, and Regression Tests pass (100% pass rate).
- [x] Deterministic calculation results verified against Golden Records.
- [x] RAG response latency verified $< 100\text{ms}$ with zero hallucinations.
- [x] Cyber Defense WAF suite passes all 31 penetration checks.
- [x] Design tokens match Venus Pearl & Jupiter Gold guidelines with zero hard black (`#000000`).
- [x] Structured data schemas validate cleanly with zero errors on Schema.org.
- [x] Canonical tags, XML sitemap, and robots.txt verified.
- [x] Payment webhook signature verification and idempotency verified.
- [x] Rollback plan documented and verified with one-command recovery.

---
*Certified by QA Lead and Principal Software Architect for Numeros Vision.*
