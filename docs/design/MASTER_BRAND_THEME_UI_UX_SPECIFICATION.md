# NUMEROS VISION — MASTER BRAND, THEME, UI/UX & NAVIGATION SPECIFICATION
**Brand:** Numeros Vision  
**Tagline:** Anveil Every Charm  
**Status:** Canonical & Immutable  
**Application Scope:** Website, Customer App, Practitioner Dashboard Application (PDA), Calculators, Reports, Blogs, and all future generated pages.

---

## 1. Core Visual Identity & Design System

Every page developed in the Numeros Vision platform must strictly conform to this visual identity contract. No individual page, sub-module, tool, or PDA screen may deviate from this specification.

### 1.1 Master Color Palette
- **Canvas Primary:** `#FFFDF7` (Venus Pearl — luminous celestial background)
- **Canvas Warm / Subtle:** `#F7F3EA` (Used for secondary sections and footer)
- **Canvas Pure:** `#FFFFFF` (Card surfaces, inputs, modal containers)
- **Primary Brand Metallic:** `#C9A227` (Jupiter Gold — buttons, active borders, icons, rings)
- **Dark Gold / Typography Accent:** `#8B6914` (High-contrast headings, active navigation text)
- **Light Gold Accent:** `#E2B84B` (Gradients and hover states)
- **Deep Amber Gold:** `#9E7B15` (Logotype fill)
- **Secondary Metaphysical Emerald:** `#16835B` (Mercury Emerald — checkmarks, status pills, tagline)
- **Body & Text Primary:** `#523E28` (Warm Deep Jupiter Bronze / Sandalwood Ink)
- **Body & Text Muted:** `#7A654D` (WCAG 2.2 AA compliant secondary text, min 4.6:1 contrast)
- **Card Borders:** `rgba(201, 162, 39, 0.38)` (`--border-gold`) and `rgba(180, 155, 110, 0.22)` (`--border`)
- **Strict Prohibition:** Zero raw black (`#000000`). Never render pure black on avatars, backgrounds, icons, or headers.

### 1.2 Master Typography
- **Headings (H1, H2, H3) & Hero:** `'Cormorant Garamond', Georgia, serif`
- **Brand Title & Eyebrows:** `'Cinzel', serif`
- **Body, Inputs, Navigation, Buttons:** `'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`

---

## 2. Canonical Brand Lockup & Logo
The master logo lockup is the single source of truth across all platforms:
- **Logo Mark:** `/logos/nv-logo-mark.svg`
- **Brand Title:** `NUMEROS VISION`
- **Brand Tagline:** `ANVEIL EVERY CHARM`

### Exact HTML Lockup:
```html
<a href="/" class="nv-brand-link" title="Numeros Vision — Anveil Every Charm">
  <div class="nv-brand-seal">
    <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
  </div>
  <div class="nv-brand-text">
    <span class="nv-brand-title">NUMEROS VISION</span>
    <span class="nv-brand-tagline">ANVEIL EVERY CHARM</span>
  </div>
</a>
```

---

## 3. Universal Navigation Architecture

### 3.1 Master Header (`<header class="nv-header">`)
Every page MUST render `<header class="nv-header">` containing:
1. Canonical brand lockup link (`/`).
2. Main navigation links:
   - Calculators (`/calculators/`)
   - Charm AI (`/charm-ai/`)
   - Reports (`/reports/`)
   - Methodology (`/methodology/`)
   - Insights (`/insights/`)
   - Pricing (`/pricing/`)
   - About (`/about/`)
3. CTA button (`.nv-btn-cta`): `Discover My Numbers ✦` (or context-specific action e.g. `Portal Home ✦` on PDA).
4. Mobile menu button (`.nv-mobile-toggle`) invoking `toggleMobileNav()`.

### 3.2 Master Footer (`<footer class="nv-footer">`)
Every page MUST render `<footer class="nv-footer">` containing:
1. 4-column structured grid:
   - **Column 1 (Brand Summary):** Official seal, logotype, and mission description.
   - **Column 2 (Calculators):** Birth Number, Life Path, Name Balancing, Lo Shu 3×3, Mobile Numerology, Personal Year.
   - **Column 3 (Intelligence & Plans):** Charm AI Assistant, Reports Catalogue, Sample Dossier, Pricing, Consultations.
2. Bottom Bar: Copyright notice, Privacy Center, Privacy Policy, Terms, Disclaimer, Cookie Policy, Refund Policy, Accessibility.

---

## 4. Required Assets for Every Page
Every HTML page must include:
```html
<!-- Typography -->
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />

<!-- Core Themes -->
<link rel="stylesheet" href="/static/css/theme.css" />
<link rel="stylesheet" href="/static/css/roadmap_components.css" />

<!-- Canonical Brand Seal Favicon -->
<link rel="icon" type="image/svg+xml" href="/logos/nv-logo-mark.svg" />
```

---

## 5. Antigravity Memory & Governance Directive
Whenever Google Antigravity or any autonomous subagent develops, updates, or audits a page:
1. Verify that `nv-header` and `nv-footer` are present.
2. Verify that `/logos/nv-logo-mark.svg` is used as the logo seal.
3. Verify that the title text reads `NUMEROS VISION` and tagline reads `ANVEIL EVERY CHARM`.
4. Ensure zero hardcoded black `#000000` is introduced.
5. Retain 100% test pass on `tests/test_live_urls.py` and `tests/test_api_cyber_security_suite.py`.
