# NUMEROS VISION — MASTER AUDIT GUIDE FOR CHATGPT & LLM REVIEW
**Website Tagline**: ANVEIL EVERY CHARM  
**Version**: 5.0.0 Production Release  
**Target Environment**: Cloudflare Live Deployment & Local Host (`http://127.0.0.1:8000`)

---

## 1. Executive Summary & Prompt for ChatGPT

Copy and paste the prompt below into ChatGPT, GPT-4o, or Claude to run an authoritative, automated audit on the live Cloudflare deployment:

```text
Act as a Principal Web Application Auditor, SEO Strategist, and Classical Numerology Domain Expert.
Please perform a comprehensive end-to-end audit on our live website: [INSERT_CLOUDFLARE_URL_HERE]

Audit against our 5 core release criteria:

1. MONETIZATION & FUNNEL CLUTTER AUDIT:
   - Verify that the homepage is clean, content-led, and clutter-free.
   - Confirm that redundant marketing cards ("100% Deterministic Engine", "10+ Specialised Topics", "3 Tiers Unified Pricing", "9 Traditions Cross-Synthesized") and the legacy "#about" transparency block have been completely removed.
   - Confirm that the 3 unified monetization tiers are consistent everywhere:
     • Basic Report: 3 Pages · ₹199
     • Advanced Report: 12 Pages · ₹489 (Most Popular)
     • Premium Sovereign Dossier: 32 Pages · ₹1,050

2. CLASSICAL CALCULATION RIGOR & NOMENCLATURE:
   - Check the 3x3 Lo Shu Sacred Grid and the 8 Planes of Expression.
   - CRITICAL TEST: Confirm that the diagonal (2-5-8) is strictly named "Silver Success Plane (2-5-8 / Property & Stability / Silver Rajyog)". It must NEVER be named "Disappointment Plane" or "Loss Plane".
   - Confirm that the diagonal (4-5-6) is named "Golden Success Plane (4-5-6 / Golden Rajyog)".
   - Verify that Driver (Mulank = single-digit day reduction) and Conductor (Bhagyank = single-digit full DOB reduction) calculate accurately without AI hallucination.

3. SAMPLE REPORTS & PACKAGE SHOWCASE (/sample_roadmap/ & /sample/):
   - Navigate to /sample_roadmap/ and test the interactive tier visualizer (Basic 3p, Advanced 12p, Premium 32p).
   - Test the Live Interactive Calculation Engine on the sample page: verify that changing the name and birth date instantly recomputes Driver, Conductor, Chaldean Name, and Lo Shu grid cells in real-time.
   - Test the PDF specimen download buttons to confirm valid PDF binary deliverables.

4. REPORTS CATALOGUE (/reports_catalogue/):
   - Verify that all 10 specialized report cards have functional "View Sample Report" buttons linked to /sample_roadmap/?topic=...
   - Verify the "Configure & Generate PDF" modal to ensure DOB and topic payloads submit smoothly and download a customized PDF dossier.

5. BRAND IDENTITY & ACCESSIBILITY:
   - Typography: Cormorant Garamond, Cinzel, and Plus Jakarta Sans.
   - Color Palette: Venus Pearl (#FFFDF7, #F7F3EA), Jupiter Gold (#C9A227, #8B6914), Mercury Emerald (#16835B), Sandalwood Ink (#523E28, #7A654D). Strictly zero raw black (#000000) typography.
   - Mobile UX: Sticky 4-tab bottom navigation, clean tap targets, zero horizontal overflow.

Please provide a structured scorecard (Pass/Fail/Notes) for each category.
```

---

## 2. Key URLs to Test on Cloudflare

| Page Name | Canonical Route | Core Function to Verify |
| :--- | :--- | :--- |
| **Homepage** | `/` | Hero Free Calculation (Driver, Conductor, Lo Shu Grid), Clutter-free monetization funnel, 3 unified pricing tiers. |
| **Sample Reports Showcase** | `/sample_roadmap/` | Interactive Tier Visualizer (Basic 3p, Advanced 12p, Premium 32p), Live interactive calculator, Sample PDF downloads. |
| **Reports Catalogue** | `/reports_catalogue/` | 10 specialized report topics, tier selector buttons, order modal with instant PDF delivery. |
| **Full Interactive Sample** | `/sample/` | 32-page comprehensive specimen dossier (Aarav Sharma) with full Dasha radar and remedies. |
| **Plans & Pricing** | `/pricing/` | Transparent ₹199, ₹489, ₹1,050 standalone report tiers and multi-report bundles. |
| **Lo Shu Grid Tool** | `/tools/lo-shu-grid/` | 3×3 Chinese sacred square, Silver Success Plane (2-5-8), Golden Rajyog (4-5-6), Poorak remedies. |
| **Name Balancing Tool** | `/tools/name-balancing/` | Acoustic Chaldean letter vibration calculator and compound number harmony score. |
| **Mobile Numerology** | `/tools/mobile-numerology/` | Phone number paired digit breakdown and planetary resonance. |
| **Compatibility Tool** | `/tools/compatibility-calculator/` | Dual-chart synastry comparing Driver, Conductor, and Lo Shu polarities. |

---

## 3. Pre-Flight Verification Checklist

- [x] Zero `#000000` black typography across all stylesheets.
- [x] Zero "Disappointment Plane" text — strictly "Silver Success Plane (2-5-8 / Property & Stability)".
- [x] Zero "Lorem Ipsum" or "TODO:" placeholders in production HTML.
- [x] All 101 static HTML files verified with canonical metadata and breadcrumbs.
- [x] Service Worker bumped to `v5.0.0-clean` with auto-eviction of stale caches.
- [x] `Cache-Control: no-cache, no-store, must-revalidate` enabled on `/`, `/sw.js`, and `/sample_roadmap/`.
- [x] Cloudflare Pages package `cloudflare_pages_upload.zip` created with `_redirects` and `_headers`.
