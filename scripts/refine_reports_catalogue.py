"""
Refines app/static/reports_catalogue.html to implement the unified pricing architecture,
standardized report cards, package comparison table, and interactive PDF delivery modal.
"""

import os
import re

CATALOGUE_PATH = os.path.abspath("app/static/reports_catalogue.html")

def build_refined_catalogue_html():
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
  new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  })(window,document,'script','dataLayer','GTM-KW6GQRVZ');</script>
  <!-- End Google Tag Manager -->
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0" />

  <!-- Standardized Favicon & Brand Touch Icons -->
  <link rel="icon" type="image/svg+xml" href="/logos/nv-logo-mark.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="/static/icons/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/static/icons/favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/static/icons/apple-touch-icon.png" />
  <link rel="shortcut icon" href="/favicon.ico" />

  <title>Numerology Reports &amp; PDF Packages | Numeros Vision</title>
  <meta name="description" content="Explore personalised numerology reports for relationships, career, money and personal growth. Compare 3-page Basic, 12-page Advanced and 32-page Premium PDF packages." />
  <link rel="canonical" href="https://numerosvision.com/reports_catalogue/" />
  <!-- Search Engine Crawl & Indexing Directives -->
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />

  <!-- App Store, PWA & Mobile Web Directives -->
  <link rel="manifest" href="/manifest.json" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="default" />
  <meta name="apple-mobile-web-app-title" content="Numeros Vision" />

  <!-- Open Graph / Social Media Directives -->
  <meta property="og:site_name" content="Numeros Vision" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://numerosvision.com/reports_catalogue/" />
  <meta property="og:title" content="Numerology Reports &amp; PDF Packages | Numeros Vision" />
  <meta property="og:description" content="Explore personalised numerology reports for relationships, career, money and personal growth. Compare 3-page Basic, 12-page Advanced and 32-page Premium PDF packages." />
  <meta property="og:image" content="https://numerosvision.com/static/logos/anveil-charm-hero.png" />

  <!-- Twitter Card Directives -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Numerology Reports &amp; PDF Packages | Numeros Vision" />
  <meta name="twitter:description" content="Explore personalised numerology reports for relationships, career, money and personal growth. Compare 3-page Basic, 12-page Advanced and 32-page Premium PDF packages." />
  <meta name="twitter:image" content="https://numerosvision.com/static/logos/anveil-charm-hero.png" />

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/static/css/theme.css?v=4.7.3" />
  <link rel="stylesheet" href="/static/css/roadmap_components.css?v=4.8.0" />

  <!-- Schema.org JSON-LD Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebApplication",
        "name": "Numeros Vision Reports Catalogue",
        "url": "https://numerosvision.com/reports_catalogue/",
        "description": "Unified numerology reports catalogue offering deterministic Basic (₹199), Advanced (₹510), and Premium (₹1,050) PDF packages across relationships, career, wealth, and destiny.",
        "applicationCategory": "LifestyleApplication",
        "operatingSystem": "All",
        "provider": {
          "@type": "Organization",
          "name": "Numeros Vision",
          "url": "https://numerosvision.com"
        }
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://numerosvision.com/" },
          { "@type": "ListItem", "position": 2, "name": "Reports Catalogue", "item": "https://numerosvision.com/reports_catalogue/" }
        ]
      },
      {
        "@type": "OfferCatalog",
        "name": "Personalised Numerology PDF Packages",
        "itemListElement": [
          {
            "@type": "Offer",
            "name": "Basic Report (3 Pages)",
            "price": "199",
            "priceCurrency": "INR",
            "description": "Focused answer to one question with core calculations, method explanation, and initial findings."
          },
          {
            "@type": "Offer",
            "name": "Advanced Report (12 Pages)",
            "price": "510",
            "priceCurrency": "INR",
            "description": "Expanded analysis, Dasha timing, comparisons, and 7-layer safe planetary remedies."
          },
          {
            "@type": "Offer",
            "name": "Premium Dossier (32 Pages)",
            "price": "1050",
            "priceCurrency": "INR",
            "description": "Comprehensive sovereign master blueprint with dual-system synthesis, 10-year radar, and technical appendix."
          }
        ]
      }
    ]
  }
  </script>

  <style>
    :root {
      --gold-dark: #8B6914;
      --gold: #C9A227;
      --gold-light: #E2B84B;
      --pearl-bg: #FFFDF7;
      --ink: #523E28;
      --ink-muted: #7A654D;
      --emerald: #16835B;
      --border-gold: rgba(201, 162, 39, 0.35);
      --card-bg: #FFFFFF;
    }

    body {
      background-color: var(--pearl-bg);
      color: var(--ink);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      margin: 0;
      padding: 0;
      -webkit-font-smoothing: antialiased;
    }

    .reports-container {
      max-width: 1240px;
      margin: 0 auto;
      padding: 30px 20px 80px;
    }

    /* ── Header & Lead ── */
    .reports-hero {
      text-align: center;
      margin-bottom: 40px;
      padding-top: 10px;
    }
    .reports-eyebrow {
      font-family: 'Cinzel', serif;
      font-size: 0.82rem;
      letter-spacing: 0.2em;
      text-transform: uppercase;
      color: var(--gold-dark);
      margin-bottom: 8px;
      display: inline-block;
      font-weight: 700;
    }
    .reports-h1 {
      font-family: 'Cormorant Garamond', serif;
      font-size: clamp(2.2rem, 4.2vw, 3.4rem);
      color: var(--gold-dark);
      margin: 0 0 16px;
      font-weight: 700;
      line-height: 1.15;
    }
    .reports-lead {
      font-size: clamp(1rem, 1.8vw, 1.15rem);
      color: var(--ink-muted);
      max-width: 820px;
      margin: 0 auto 24px;
      line-height: 1.65;
    }

    /* ── Unified Package Comparison Table ── */
    .pricing-comparison-box {
      background: #FFFFFF;
      border: 1.5px solid var(--border-gold);
      border-radius: 16px;
      padding: 24px 20px;
      margin-bottom: 45px;
      box-shadow: 0 4px 20px rgba(139, 105, 20, 0.06);
      overflow-x: auto;
    }
    .comparison-title {
      font-family: 'Cinzel', serif;
      font-size: 1.25rem;
      color: var(--gold-dark);
      text-align: center;
      margin-bottom: 18px;
    }
    .comp-table {
      width: 100%;
      border-collapse: collapse;
      min-width: 650px;
      text-align: left;
      font-size: 0.88rem;
    }
    .comp-table th, .comp-table td {
      padding: 12px 14px;
      border-bottom: 1px solid rgba(201, 162, 39, 0.2);
    }
    .comp-table th {
      font-family: 'Cinzel', serif;
      color: var(--gold-dark);
      font-size: 0.95rem;
      background: rgba(201, 162, 39, 0.06);
    }
    .comp-table tr.highlight-row {
      background: rgba(201, 162, 39, 0.04);
      font-weight: 600;
    }
    .comp-badge {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 4px;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.05em;
    }
    .badge-basic { background: rgba(82, 62, 40, 0.1); color: var(--ink); }
    .badge-adv { background: rgba(201, 162, 39, 0.2); color: var(--gold-dark); }
    .badge-prem { background: rgba(22, 131, 91, 0.15); color: var(--emerald); }

    /* ── Filter Tabs ── */
    .nv-cat-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: center;
      margin-bottom: 35px;
    }
    .nv-cat-tab {
      background: #FFFFFF;
      border: 1.5px solid var(--border-gold);
      color: var(--ink);
      padding: 9px 18px;
      border-radius: 999px;
      font-size: 0.86rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .nv-cat-tab:hover, .nv-cat-tab.active {
      background: var(--gold);
      color: #FFFFFF;
      border-color: var(--gold-dark);
      box-shadow: 0 2px 10px rgba(201, 162, 39, 0.3);
    }

    /* ── Grid & Standalone Cards ── */
    .reports-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
      gap: 26px;
      margin-bottom: 50px;
    }
    .report-card {
      background: var(--card-bg);
      border: 1.5px solid var(--border-gold);
      border-radius: 16px;
      padding: 24px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.2s, box-shadow 0.2s;
      position: relative;
    }
    .report-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 8px 24px rgba(139, 105, 20, 0.12);
      border-color: var(--gold);
    }
    .report-card-top { margin-bottom: 16px; }
    .report-icon-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 10px;
    }
    .report-icon { font-size: 1.8rem; }
    .report-category-pill {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--gold-dark);
      background: rgba(201, 162, 39, 0.12);
      padding: 3px 8px;
      border-radius: 4px;
    }
    .report-card h3 {
      font-family: 'Cinzel', serif;
      font-size: 1.22rem;
      color: var(--gold-dark);
      margin: 0 0 8px;
      line-height: 1.35;
      min-height: 2.7em;
    }
    .report-desc {
      font-size: 0.88rem;
      color: var(--ink-muted);
      line-height: 1.55;
      margin-bottom: 16px;
      min-height: 2.8em;
    }

    /* ── Interactive Tier Selector on Card ── */
    .tier-selector-box {
      background: #FDFBF5;
      border: 1px solid var(--border-gold);
      border-radius: 10px;
      padding: 10px 12px;
      margin-bottom: 18px;
    }
    .tier-selector-title {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--ink-muted);
      margin-bottom: 8px;
      display: block;
    }
    .tier-options-group {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
    }
    .tier-btn {
      background: #FFFFFF;
      border: 1px solid var(--border-gold);
      border-radius: 6px;
      padding: 6px 4px;
      text-align: center;
      cursor: pointer;
      font-size: 0.76rem;
      transition: all 0.15s ease;
      color: var(--ink);
    }
    .tier-btn:hover, .tier-btn.selected {
      background: var(--gold-dark);
      color: #FFFFFF;
      border-color: var(--gold-dark);
      font-weight: 700;
    }
    .tier-btn small { display: block; font-size: 0.68rem; opacity: 0.9; }

    .deliverables-list {
      list-style: none;
      padding: 0;
      margin: 0 0 20px;
      font-size: 0.82rem;
      color: var(--ink);
      line-height: 1.6;
    }
    .deliverables-list li {
      padding-left: 18px;
      position: relative;
      margin-bottom: 5px;
    }
    .deliverables-list li::before {
      content: "✦";
      position: absolute;
      left: 0;
      color: var(--gold);
      font-size: 0.7rem;
    }

    .btn-choose-report {
      width: 100%;
      background: var(--gold-dark);
      color: #FFFFFF;
      border: none;
      padding: 11px 16px;
      border-radius: 8px;
      font-weight: 700;
      font-size: 0.9rem;
      cursor: pointer;
      text-align: center;
      transition: background 0.2s;
    }
    .btn-choose-report:hover {
      background: #73550F;
    }

    /* ── Bundles Section ── */
    .bundles-section {
      background: #FFFFFF;
      border: 1.5px solid var(--border-gold);
      border-radius: 20px;
      padding: 36px 28px;
      margin-bottom: 50px;
      box-shadow: 0 4px 20px rgba(139, 105, 20, 0.06);
    }
    .bundles-header { text-align: center; margin-bottom: 28px; }
    .bundles-title {
      font-family: 'Cormorant Garamond', serif;
      font-size: 2.2rem;
      color: var(--gold-dark);
      margin: 0 0 8px;
    }
    .bundles-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(290px, 1fr));
      gap: 22px;
    }
    .bundle-card {
      background: #FFFDF7;
      border: 1.5px solid var(--border-gold);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    .bundle-card.featured {
      border-color: var(--gold);
      box-shadow: 0 4px 16px rgba(201, 162, 39, 0.18);
    }
    .bundle-savings {
      font-size: 0.72rem;
      font-weight: 700;
      color: var(--emerald);
      background: rgba(22, 131, 91, 0.12);
      padding: 3px 8px;
      border-radius: 4px;
      display: inline-block;
      margin-bottom: 10px;
    }

    /* ── Interactive Order & PDF Delivery Modal ── */
    .nv-modal-backdrop {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(82, 62, 40, 0.6);
      backdrop-filter: blur(4px);
      z-index: 1000;
      align-items: center;
      justify-content: center;
      padding: 20px;
    }
    .nv-modal-backdrop.open { display: flex; }
    .nv-modal-window {
      background: #FFFDF7;
      border: 2px solid var(--gold);
      border-radius: 16px;
      max-width: 540px;
      width: 100%;
      padding: 28px 24px;
      box-shadow: 0 16px 40px rgba(82, 62, 40, 0.25);
      position: relative;
      max-height: 90vh;
      overflow-y: auto;
    }
    .modal-close {
      position: absolute;
      top: 14px;
      right: 16px;
      font-size: 1.4rem;
      background: none;
      border: none;
      cursor: pointer;
      color: var(--ink-muted);
    }
    .form-group {
      margin-bottom: 14px;
    }
    .form-label {
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--ink);
      display: block;
      margin-bottom: 5px;
    }
    .form-input {
      width: 100%;
      box-sizing: border-box;
      padding: 10px 12px;
      border: 1px solid var(--border-gold);
      border-radius: 8px;
      font-size: 0.92rem;
      background: #FFFFFF;
      color: var(--ink);
    }
  </style>
</head>

<body>
  <!-- Master Header Component -->
  <header class="nv-header" style="background:#FFFDF7; border-bottom:1px solid var(--border-gold); padding:16px 24px;">
    <div style="max-width:1240px; margin:0 auto; display:flex; align-items:center; justify-content:space-between;">
      <a href="/" style="text-decoration:none; display:flex; align-items:center; gap:10px;">
        <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision" width="34" height="34" />
        <span style="font-family:'Cinzel',serif; font-size:1.25rem; font-weight:700; color:var(--gold-dark); letter-spacing:0.08em;">NUMEROS VISION</span>
      </a>
      <nav style="display:flex; gap:20px; align-items:center;">
        <a href="/calculators/" style="text-decoration:none; color:var(--ink); font-size:0.9rem; font-weight:600;">Calculators</a>
        <a href="/reports_catalogue/" style="text-decoration:none; color:var(--gold-dark); font-size:0.9rem; font-weight:700;">Reports</a>
        <a href="/pricing/" style="text-decoration:none; color:var(--ink); font-size:0.9rem; font-weight:600;">Pricing</a>
        <a href="/consultation/" style="text-decoration:none; color:var(--ink); font-size:0.9rem; font-weight:600;">Consultation</a>
      </nav>
    </div>
  </header>

  <main class="reports-container">
    <!-- Hero Section -->
    <section class="reports-hero">
      <span class="reports-eyebrow">DETERMINISTIC NUMEROLOGY ARCHITECTURE</span>
      <h1 class="reports-h1">Personalised Numerology Reports &amp; Packages</h1>
      <p class="reports-lead">
        Explore personalised numerology reports for relationships, career, money and personal growth.
        Every report is powered by deterministic calculations and available in three standardized depths:
        <strong>3-Page Basic (₹199)</strong>, <strong>12-Page Advanced (₹510)</strong>, and <strong>32-Page Premium (₹1,050)</strong>.
      </p>
    </section>

    <!-- ── Unified Package Comparison Section ── -->
    <section class="pricing-comparison-box">
      <h2 class="comparison-title">Standardized Report Package Comparison</h2>
      <table class="comp-table">
        <thead>
          <tr>
            <th>Package Feature</th>
            <th>Basic · Entry</th>
            <th>Advanced · Recommended</th>
            <th>Premium · Sovereign</th>
          </tr>
        </thead>
        <tbody>
          <tr class="highlight-row">
            <td><strong>Retail Price</strong></td>
            <td><strong style="color:var(--gold-dark); font-size:1.1rem;">₹199</strong></td>
            <td><strong style="color:var(--gold-dark); font-size:1.1rem;">₹510</strong></td>
            <td><strong style="color:var(--gold-dark); font-size:1.1rem;">₹1,050</strong></td>
          </tr>
          <tr>
            <td><strong>Target PDF Length</strong></td>
            <td><span class="comp-badge badge-basic">3 Pages</span></td>
            <td><span class="comp-badge badge-adv">12 Pages</span></td>
            <td><span class="comp-badge badge-prem">32 Pages</span></td>
          </tr>
          <tr>
            <td><strong>Core Calculations</strong></td>
            <td>Mulank &amp; Bhagyank Foundations</td>
            <td>Driver, Conductor, Kua, Lo Shu &amp; Dasha</td>
            <td>Complete Multi-Engine Synthesis</td>
          </tr>
          <tr>
            <td><strong>Interpretation Depth</strong></td>
            <td>Focused single-question reading</td>
            <td>Expanded cross-factor analysis</td>
            <td>Comprehensive lifetime master synthesis</td>
          </tr>
          <tr>
            <td><strong>Comparisons &amp; Timing</strong></td>
            <td>Essential initial findings</td>
            <td>5-Year Vimshottari &amp; Dasha radar</td>
            <td>10-Year Macro radar &amp; Synastry matrix</td>
          </tr>
          <tr>
            <td><strong>Methodology &amp; Remedies</strong></td>
            <td>Method note &amp; reflection points</td>
            <td>7-Layer safe planetary remedies</td>
            <td>Exhaustive mathematical proofs appendix</td>
          </tr>
          <tr>
            <td><strong>Format &amp; Delivery</strong></td>
            <td>Instant Personalised PDF</td>
            <td>Instant Personalised PDF</td>
            <td>Instant Personalised PDF</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- ── Category Filter Tabs ── -->
    <div class="nv-cat-tabs">
      <button type="button" class="nv-cat-tab active" data-cat="all" onclick="filterCategory('all', this)">All Reports</button>
      <button type="button" class="nv-cat-tab" data-cat="Love and Marriage" onclick="filterCategory('Love and Marriage', this)">💖 Love &amp; Marriage</button>
      <button type="button" class="nv-cat-tab" data-cat="Money" onclick="filterCategory('Money', this)">💰 Money &amp; Wealth</button>
      <button type="button" class="nv-cat-tab" data-cat="Work" onclick="filterCategory('Work', this)">💼 Career &amp; Business</button>
      <button type="button" class="nv-cat-tab" data-cat="Self and Growth" onclick="filterCategory('Self and Growth', this)">🌱 Self &amp; Destiny</button>
      <button type="button" class="nv-cat-tab" data-cat="bundle" onclick="filterCategory('bundle', this)">📦 Bundles (Save Up To 18%)</button>
      <button type="button" class="nv-cat-tab" data-cat="charm_ai" onclick="filterCategory('charm_ai', this)">✨ Charm AI Access</button>
    </div>

    <!-- ── Standalone Reports Grid ── -->
    <div class="reports-grid" id="reportsGrid">

      <!-- 1. Love Style & Romance Profile -->
      <div class="report-card" data-category="Love and Marriage" data-topic-id="love_romance">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">💖</span>
            <span class="report-category-pill">Love &amp; Marriage</span>
          </div>
          <h3>Love Style &amp; Romance Profile</h3>
          <p class="report-desc">Uncovers your relationship blueprint, emotional attraction triggers, and partnership style.</p>
          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth:</span>
            <div class="tier-options-group">
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'basic', 199, '3 Pages')">Basic<small>₹199 · 3p</small></button>
              <button type="button" class="tier-btn selected" onclick="selectCardTier(this, 'advanced', 510, '12 Pages')">Adv.<small>₹510 · 12p</small></button>
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'premium', 1050, '32 Pages')">Prem.<small>₹1,050 · 32p</small></button>
            </div>
          </div>
          <ul class="deliverables-list">
            <li>Harmonic Venus &amp; Moon polarity analysis</li>
            <li>Attachment styles &amp; emotional grounding</li>
            <li>Auspicious courtship &amp; bonding dates</li>
          </ul>
        </div>
        <button type="button" class="btn-choose-report" onclick="openOrderModal('love_romance', 'Love Style & Romance Profile')">Choose Report ✦</button>
      </div>

      <!-- 2. Marriage Timing & Union Blueprint -->
      <div class="report-card" data-category="Love and Marriage" data-topic-id="marriage_union">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">💍</span>
            <span class="report-category-pill">Love &amp; Marriage</span>
          </div>
          <h3>Marriage Timing &amp; Union Blueprint</h3>
          <p class="report-desc">Evaluates auspicious union windows, spousal harmony factors, and long-term marital alignment.</p>
          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth:</span>
            <div class="tier-options-group">
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'basic', 199, '3 Pages')">Basic<small>₹199 · 3p</small></button>
              <button type="button" class="tier-btn selected" onclick="selectCardTier(this, 'advanced', 510, '12 Pages')">Adv.<small>₹510 · 12p</small></button>
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'premium', 1050, '32 Pages')">Prem.<small>₹1,050 · 32p</small></button>
            </div>
          </div>
          <ul class="deliverables-list">
            <li>5-Year Vimshottari marital timing radar</li>
            <li>Spousal harmony factors &amp; core traits</li>
            <li>Muhurat date selection guidelines</li>
          </ul>
        </div>
        <button type="button" class="btn-choose-report" onclick="openOrderModal('marriage_union', 'Marriage Timing & Union Blueprint')">Choose Report ✦</button>
      </div>

      <!-- 3. Ideal Partner Compatibility -->
      <div class="report-card" data-category="Love and Marriage" data-topic-id="partner_compatibility">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">⚖️</span>
            <span class="report-category-pill">Love &amp; Marriage</span>
          </div>
          <h3>Ideal Partner Compatibility</h3>
          <p class="report-desc">Dual-chart synastry comparing Driver, Conductor, and Lo Shu grid polarities between two individuals.</p>
          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth:</span>
            <div class="tier-options-group">
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'basic', 199, '3 Pages')">Basic<small>₹199 · 3p</small></button>
              <button type="button" class="tier-btn selected" onclick="selectCardTier(this, 'advanced', 510, '12 Pages')">Adv.<small>₹510 · 12p</small></button>
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'premium', 1050, '32 Pages')">Prem.<small>₹1,050 · 32p</small></button>
            </div>
          </div>
          <ul class="deliverables-list">
            <li>Dual-profile Driver/Conductor synastry</li>
            <li>Lo Shu grid elemental gap compensation</li>
            <li>Interpersonal friction mitigation protocols</li>
          </ul>
        </div>
        <button type="button" class="btn-choose-report" onclick="openOrderModal('partner_compatibility', 'Ideal Partner Compatibility')">Choose Report ✦</button>
      </div>

      <!-- 4. Wealth & Abundance Report -->
      <div class="report-card" data-category="Money" data-topic-id="wealth_abundance">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">💰</span>
            <span class="report-category-pill">Money &amp; Wealth</span>
          </div>
          <h3>Wealth &amp; Abundance Report</h3>
          <p class="report-desc">Identifies your financial growth catalysts, wealth retention numbers, and prosperity cycles.</p>
          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth:</span>
            <div class="tier-options-group">
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'basic', 199, '3 Pages')">Basic<small>₹199 · 3p</small></button>
              <button type="button" class="tier-btn selected" onclick="selectCardTier(this, 'advanced', 510, '12 Pages')">Adv.<small>₹510 · 12p</small></button>
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'premium', 1050, '32 Pages')">Prem.<small>₹1,050 · 32p</small></button>
            </div>
          </div>
          <ul class="deliverables-list">
            <li>Lo Shu Golden Prosperity Plane (4-5-6) audit</li>
            <li>Auspicious investment initiation windows</li>
            <li>Safe behavioral wealth compounding habits</li>
          </ul>
        </div>
        <button type="button" class="btn-choose-report" onclick="openOrderModal('wealth_abundance', 'Wealth & Abundance Report')">Choose Report ✦</button>
      </div>

      <!-- 5. High-Growth Commercial Potential -->
      <div class="report-card" data-category="Money" data-topic-id="billionaire_potential">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">🏛️</span>
            <span class="report-category-pill">Money &amp; Wealth</span>
          </div>
          <h3>High-Growth Commercial Potential</h3>
          <p class="report-desc">Explores enterprise scale capacity, high-stakes decision cycles, and institutional wealth vectors.</p>
          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth:</span>
            <div class="tier-options-group">
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'basic', 199, '3 Pages')">Basic<small>₹199 · 3p</small></button>
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'advanced', 510, '12 Pages')">Adv.<small>₹510 · 12p</small></button>
              <button type="button" class="tier-btn selected" onclick="selectCardTier(this, 'premium', 1050, '32 Pages')">Prem.<small>₹1,050 · 32p</small></button>
            </div>
          </div>
          <ul class="deliverables-list">
            <li>Enterprise scaling &amp; equity expansion cycles</li>
            <li>Saturn (8) &amp; Mercury (5) institutional resilience</li>
            <li>Commercial non-guarantee statutory evaluation</li>
          </ul>
        </div>
        <button type="button" class="btn-choose-report" onclick="openOrderModal('billionaire_potential', 'High-Growth Commercial Potential')">Choose Report ✦</button>
      </div>

      <!-- 6. Career Direction & Growth -->
      <div class="report-card" data-category="Work" data-topic-id="career_growth">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">💼</span>
            <span class="report-category-pill">Career &amp; Work</span>
          </div>
          <h3>Career Direction &amp; Growth</h3>
          <p class="report-desc">Maps your optimal vocational pathways, promotion cycles, and leadership strengths.</p>
          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth:</span>
            <div class="tier-options-group">
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'basic', 199, '3 Pages')">Basic<small>₹199 · 3p</small></button>
              <button type="button" class="tier-btn selected" onclick="selectCardTier(this, 'advanced', 510, '12 Pages')">Adv.<small>₹510 · 12p</small></button>
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'premium', 1050, '32 Pages')">Prem.<small>₹1,050 · 32p</small></button>
            </div>
          </div>
          <ul class="deliverables-list">
            <li>Vocational resonance with Driver &amp; Conductor</li>
            <li>Annual appraisal &amp; transition timing radar</li>
            <li>Leadership presence &amp; executive poise vectors</li>
          </ul>
        </div>
        <button type="button" class="btn-choose-report" onclick="openOrderModal('career_growth', 'Career Direction & Growth')">Choose Report ✦</button>
      </div>

      <!-- 7. Business & Venture Mastery -->
      <div class="report-card" data-category="Work" data-topic-id="business_venture">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">🚀</span>
            <span class="report-category-pill">Career &amp; Work</span>
          </div>
          <h3>Business &amp; Venture Mastery</h3>
          <p class="report-desc">Evaluates venture launch timings, commercial partnerships, and brand numerical resonance.</p>
          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth:</span>
            <div class="tier-options-group">
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'basic', 199, '3 Pages')">Basic<small>₹199 · 3p</small></button>
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'advanced', 510, '12 Pages')">Adv.<small>₹510 · 12p</small></button>
              <button type="button" class="tier-btn selected" onclick="selectCardTier(this, 'premium', 1050, '32 Pages')">Prem.<small>₹1,050 · 32p</small></button>
            </div>
          </div>
          <ul class="deliverables-list">
            <li>Incorporation &amp; brand launch auspicious dates</li>
            <li>Founder &amp; co-founder synergy matrix</li>
            <li>Entity name Chaldean vibrational calibration</li>
          </ul>
        </div>
        <button type="button" class="btn-choose-report" onclick="openOrderModal('business_venture', 'Business & Venture Mastery')">Choose Report ✦</button>
      </div>

      <!-- 8. Complete Personal Destiny Blueprint -->
      <div class="report-card" data-category="Self and Growth" data-topic-id="core_blueprint">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">☀️</span>
            <span class="report-category-pill">Self &amp; Destiny</span>
          </div>
          <h3>Complete Personal Destiny Blueprint</h3>
          <p class="report-desc">Comprehensive baseline assessment of your life purpose, hidden strengths, and karmic lessons.</p>
          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth:</span>
            <div class="tier-options-group">
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'basic', 199, '3 Pages')">Basic<small>₹199 · 3p</small></button>
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'advanced', 510, '12 Pages')">Adv.<small>₹510 · 12p</small></button>
              <button type="button" class="tier-btn selected" onclick="selectCardTier(this, 'premium', 1050, '32 Pages')">Prem.<small>₹1,050 · 32p</small></button>
            </div>
          </div>
          <ul class="deliverables-list">
            <li>Full 32-chapter sovereign executive dossier</li>
            <li>Dual-system synthesis (Chaldean + Pythagorean)</li>
            <li>Consolidated lifetime strategic reference</li>
          </ul>
        </div>
        <button type="button" class="btn-choose-report" onclick="openOrderModal('core_blueprint', 'Complete Personal Destiny Blueprint')">Choose Report ✦</button>
      </div>

      <!-- 9. Name Balancing & Spelling Calibration -->
      <div class="report-card" data-category="Self and Growth" data-topic-id="name_spelling_calibration">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">✍️</span>
            <span class="report-category-pill">Self &amp; Destiny</span>
          </div>
          <h3>Name Balancing &amp; Spelling Calibration</h3>
          <p class="report-desc">Chaldean vibrational analysis of your calling name to calibrate harmonious compound resonances.</p>
          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth:</span>
            <div class="tier-options-group">
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'basic', 199, '3 Pages')">Basic<small>₹199 · 3p</small></button>
              <button type="button" class="tier-btn selected" onclick="selectCardTier(this, 'advanced', 510, '12 Pages')">Adv.<small>₹510 · 12p</small></button>
              <button type="button" class="tier-btn" onclick="selectCardTier(this, 'premium', 1050, '32 Pages')">Prem.<small>₹1,050 · 32p</small></button>
            </div>
          </div>
          <ul class="deliverables-list">
            <li>Calling name vs legal name acoustic audit</li>
            <li>Elimination of frictional compound numbers</li>
            <li>3 optimal harmonized spelling suggestions</li>
          </ul>
        </div>
        <button type="button" class="btn-choose-report" onclick="openOrderModal('name_spelling_calibration', 'Name Balancing & Spelling Calibration')">Choose Report ✦</button>
      </div>

    </div>

    <!-- ── Product Family B: Multi-Report Bundles ── -->
    <section class="bundles-section" id="bundles">
      <div class="bundles-header">
        <span class="reports-eyebrow">CURATED SUITES</span>
        <h2 class="bundles-title">Multi-Report Bundles</h2>
        <p style="color:var(--ink-muted); max-width:650px; margin:0 auto; font-size:0.95rem;">
          Combine multiple focused reports to audit connected life domains. Standalone savings are computed directly from unified tier prices.
        </p>
      </div>
      <div class="bundles-grid">

        <!-- Starter Bundle -->
        <div class="bundle-card">
          <div>
            <span class="bundle-savings">SAVE ₹49 (12% OFF)</span>
            <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:0 0 8px;">Starter Bundle</h3>
            <p style="font-size:0.86rem; color:var(--ink-muted); margin-bottom:14px;">Two Basic 3-page reports of your choice across Love, Money, Work, or Growth.</p>
            <div style="margin-bottom:14px;">
              <span style="font-family:'Cinzel',serif; font-size:1.6rem; font-weight:700; color:var(--gold-dark);">₹349</span>
              <span style="font-size:0.88rem; color:#A89880; text-decoration:line-through; margin-left:6px;">₹398</span>
            </div>
            <ul class="deliverables-list">
              <li>2 Complete 3-Page Basic PDF Reports</li>
              <li>Choose any two catalogue topics</li>
              <li>Independent deterministic calculation traces</li>
              <li>Instant downloads upon generation</li>
            </ul>
          </div>
          <button type="button" class="btn-choose-report" onclick="openBundleModal('starter_bundle', 'Starter Bundle (2 Basic Reports)', 349)">Get Starter Bundle ✦</button>
        </div>

        <!-- Discovery Bundle -->
        <div class="bundle-card featured">
          <div>
            <span class="bundle-savings">SAVE ₹98 (16% OFF) · POPULAR</span>
            <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:0 0 8px;">Discovery Bundle</h3>
            <p style="font-size:0.86rem; color:var(--ink-muted); margin-bottom:14px;">Three Basic 3-page reports for a comprehensive 3-domain diagnostic (Love, Wealth &amp; Career).</p>
            <div style="margin-bottom:14px;">
              <span style="font-family:'Cinzel',serif; font-size:1.6rem; font-weight:700; color:var(--gold-dark);">₹499</span>
              <span style="font-size:0.88rem; color:#A89880; text-decoration:line-through; margin-left:6px;">₹597</span>
            </div>
            <ul class="deliverables-list">
              <li>3 Complete 3-Page Basic PDF Reports</li>
              <li>Choose any three catalogue topics</li>
              <li>Unified life domain audit</li>
              <li>Saved to your secure account dashboard</li>
            </ul>
          </div>
          <button type="button" class="btn-choose-report" onclick="openBundleModal('discovery_bundle', 'Discovery Bundle (3 Basic Reports)', 499)">Get Discovery Bundle ✦</button>
        </div>

        <!-- Comprehensive Bundle -->
        <div class="bundle-card">
          <div>
            <span class="bundle-savings">SAVE ₹220 (18% OFF)</span>
            <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:0 0 8px;">Comprehensive Bundle</h3>
            <p style="font-size:0.86rem; color:var(--ink-muted); margin-bottom:14px;">Two 12-page Advanced reports plus one 3-page Basic report (27 pages total) for high-stakes pivots.</p>
            <div style="margin-bottom:14px;">
              <span style="font-family:'Cinzel',serif; font-size:1.6rem; font-weight:700; color:var(--gold-dark);">₹999</span>
              <span style="font-size:0.88rem; color:#A89880; text-decoration:line-through; margin-left:6px;">₹1,219</span>
            </div>
            <ul class="deliverables-list">
              <li>2 Complete 12-Page Advanced Reports (24 pages)</li>
              <li>1 Complete 3-Page Basic Report (3 pages)</li>
              <li>5-Year Vimshottari timing radar included</li>
              <li>7-Layer safe planetary remedies</li>
            </ul>
          </div>
          <button type="button" class="btn-choose-report" onclick="openBundleModal('comprehensive_bundle', 'Comprehensive Bundle (2 Adv + 1 Basic)', 999)">Get Comprehensive Bundle ✦</button>
        </div>

      </div>
    </section>

    <!-- ── Product Family C & D: Charm AI & Consultation ── -->
    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:24px; margin-bottom:50px;">
      
      <!-- Charm AI Access -->
      <div style="background:#FFFFFF; border:1.5px solid var(--border-gold); border-radius:16px; padding:26px;">
        <span style="font-size:0.75rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase; letter-spacing:0.08em;">CONVERSATIONAL ORACLE</span>
        <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:6px 0 10px;">Charm AI Access Packs</h3>
        <p style="font-size:0.88rem; color:var(--ink-muted); line-height:1.55; margin-bottom:16px;">
          Interrogate your exact chart tokens, timing windows, and safe remedies in real-time conversational sessions.
        </p>
        <div style="display:grid; grid-template-columns:repeat(2, 1fr); gap:10px; margin-bottom:18px;">
          <div style="background:#FDFBF5; border:1px solid var(--border-gold); border-radius:8px; padding:10px; text-align:center;">
            <div style="font-size:0.75rem; color:var(--ink-muted);">Single Reading</div>
            <div style="font-weight:700; color:var(--gold-dark); font-size:1.15rem;">₹199</div>
            <div style="font-size:0.7rem; color:var(--ink);">3 Questions</div>
          </div>
          <div style="background:#FDFBF5; border:1px solid var(--border-gold); border-radius:8px; padding:10px; text-align:center;">
            <div style="font-size:0.75rem; color:var(--ink-muted);">Multi-Pack</div>
            <div style="font-weight:700; color:var(--gold-dark); font-size:1.15rem;">₹399</div>
            <div style="font-size:0.7rem; color:var(--ink);">10 Qs + Remedies</div>
          </div>
        </div>
        <a href="/pricing/" class="btn-choose-report" style="display:block; text-decoration:none;">View Charm AI Packs ✦</a>
      </div>

      <!-- Human Consultation -->
      <div style="background:#FFFFFF; border:1.5px solid var(--border-gold); border-radius:16px; padding:26px;">
        <span style="font-size:0.75rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase; letter-spacing:0.08em;">HUMAN PRACTITIONER ADVISORY</span>
        <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:6px 0 10px;">1-on-1 Expert Consultation</h3>
        <p style="font-size:0.88rem; color:var(--ink-muted); line-height:1.55; margin-bottom:16px;">
          Private 45-minute video or phone consultation with a certified senior numerologist and Vedic astrologer for complex life pivots.
        </p>
        <div style="background:#FDFBF5; border:1px solid var(--border-gold); border-radius:8px; padding:10px 14px; margin-bottom:18px; display:flex; justify-content:space-between; align-items:center;">
          <div>
            <div style="font-size:0.78rem; font-weight:700; color:var(--ink);">Standard Private Session</div>
            <div style="font-size:0.72rem; color:var(--ink-muted);">45 Mins · Includes 12p Dossier</div>
          </div>
          <div style="font-family:'Cinzel',serif; font-size:1.35rem; font-weight:700; color:var(--gold-dark);">₹1,050</div>
        </div>
        <a href="/consultation/" class="btn-choose-report" style="display:block; text-decoration:none;">Book Consultation ✦</a>
      </div>

    </div>

  </main>

  <!-- ── Interactive Order & PDF Generation Modal ── -->
  <div class="nv-modal-backdrop" id="orderModal">
    <div class="nv-modal-window">
      <button type="button" class="modal-close" onclick="closeOrderModal()" aria-label="Close Modal">&times;</button>
      
      <div style="text-align:center; margin-bottom:20px;">
        <span style="font-size:0.75rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase; letter-spacing:0.1em;">CUSTOMISED REPORT DELIVERY</span>
        <h2 id="modalReportTitle" style="font-family:'Cormorant Garamond',serif; font-size:1.8rem; color:var(--gold-dark); margin:4px 0 6px;">Report Title</h2>
        <p id="modalReportSub" style="font-size:0.85rem; color:var(--ink-muted); margin:0;">Select your package depth and enter birth details to generate your report.</p>
      </div>

      <form id="orderForm" onsubmit="handleGenerateSubmit(event)">
        <!-- Tier Selection in Modal -->
        <div class="form-group">
          <label class="form-label">Report Package Depth:</label>
          <div style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px;" id="modalTierGroup">
            <button type="button" class="tier-btn" data-tier="basic" onclick="setModalTier('basic', 199, '3 Pages')">
              <strong>Basic</strong><br/><small>₹199 · 3p</small>
            </button>
            <button type="button" class="tier-btn selected" data-tier="advanced" onclick="setModalTier('advanced', 510, '12 Pages')">
              <strong>Advanced</strong><br/><small>₹510 · 12p</small>
            </button>
            <button type="button" class="tier-btn" data-tier="premium" onclick="setModalTier('premium', 1050, '32 Pages')">
              <strong>Premium</strong><br/><small>₹1,050 · 32p</small>
            </button>
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" for="seekerName">Full Calling Name:</label>
          <input type="text" id="seekerName" class="form-input" placeholder="e.g. Rahul Sharma" required />
        </div>

        <div class="form-group">
          <label class="form-label">Date of Birth:</label>
          <div style="display:grid; grid-template-columns:1fr 1fr 1.5fr; gap:8px;">
            <input type="number" id="dobDay" class="form-input" placeholder="DD" min="1" max="31" required />
            <input type="number" id="dobMonth" class="form-input" placeholder="MM" min="1" max="12" required />
            <input type="number" id="dobYear" class="form-input" placeholder="YYYY" min="1900" max="2030" required />
          </div>
        </div>

        <!-- Live Calculation Box (Populated on input) -->
        <div id="liveCalcBox" style="display:none; background:#F9F4EA; border:1px solid var(--border-gold); border-radius:8px; padding:12px; margin-bottom:14px; font-size:0.82rem;">
          <strong style="color:var(--gold-dark); display:block; margin-bottom:4px;">✦ Deterministic Calculation Trace:</strong>
          <div id="liveCalcDetails" style="color:var(--ink);">Calculating...</div>
        </div>

        <div style="display:flex; gap:10px; margin-top:20px;">
          <button type="button" class="btn-choose-report" style="background:#FFFFFF; color:var(--ink); border:1px solid var(--border-gold);" onclick="calculatePreviewOnly()">Preview Calculations</button>
          <button type="submit" class="btn-choose-report" id="btnSubmitGenerate">Generate &amp; Download PDF (₹<span id="btnPriceDisplay">510</span>) ✦</button>
        </div>
      </form>
    </div>
  </div>

  <!-- Master Footer Component -->
  <footer class="nv-footer" style="background:#F7F3EA; border-top:1px solid var(--border-gold); padding:30px 20px; text-align:center; font-size:0.85rem; color:var(--ink-muted); margin-top:60px;">
    <div style="max-width:1240px; margin:0 auto;">
      <p style="font-family:'Cinzel',serif; font-weight:700; color:var(--gold-dark); margin-bottom:8px;">NUMEROS VISION · ANVEIL EVERY CHARM</p>
      <p style="margin-bottom:12px;">Unified deterministic numerology platform. All calculations are executed server-side with zero artificial arithmetic overrides.</p>
      <div style="display:flex; justify-content:center; gap:16px; margin-bottom:12px;">
        <a href="/about/" style="color:var(--ink-muted); text-decoration:none;">About Us</a>
        <a href="/methodology/" style="color:var(--ink-muted); text-decoration:none;">Methodology</a>
        <a href="/pricing/" style="color:var(--ink-muted); text-decoration:none;">Pricing Policy</a>
        <a href="/privacy/" style="color:var(--ink-muted); text-decoration:none;">Privacy Policy</a>
        <a href="/disclaimer/" style="color:var(--ink-muted); text-decoration:none;">Statutory Disclaimer</a>
      </div>
      <p style="font-size:0.75rem; color:#A89880;">© 2026 Numeros Vision. All rights reserved. Strictly zero raw black palette standard.</p>
    </div>
  </footer>

  <script>
    // State
    let currentTopicId = 'core_blueprint';
    let currentTier = 'advanced';
    let currentPrice = 510;

    function filterCategory(category, btn) {
      document.querySelectorAll('.nv-cat-tab').forEach(t => t.classList.remove('active'));
      if (btn) btn.classList.add('active');

      const cards = document.querySelectorAll('.report-card');
      const bundlesSec = document.getElementById('bundles');

      if (category === 'all') {
        cards.forEach(c => c.style.display = 'flex');
        if (bundlesSec) bundlesSec.style.display = 'block';
      } else if (category === 'bundle') {
        cards.forEach(c => c.style.display = 'none');
        if (bundlesSec) {
          bundlesSec.style.display = 'block';
          bundlesSec.scrollIntoView({ behavior: 'smooth' });
        }
      } else if (category === 'charm_ai') {
        window.location.href = '/pricing/#charm-ai';
      } else {
        cards.forEach(c => {
          if (c.getAttribute('data-category') === category) {
            c.style.display = 'flex';
          } else {
            c.style.display = 'none';
          }
        });
        if (bundlesSec) bundlesSec.style.display = 'none';
      }
    }

    function selectCardTier(btn, tier, price, pages) {
      const card = btn.closest('.report-card');
      card.querySelectorAll('.tier-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');
      card.setAttribute('data-selected-tier', tier);
      card.setAttribute('data-selected-price', price);
    }

    function openOrderModal(topicId, title) {
      currentTopicId = topicId;
      document.getElementById('modalReportTitle').textContent = title;
      
      // Default to advanced
      setModalTier('advanced', 510, '12 Pages');
      document.getElementById('orderModal').classList.add('open');
    }

    function closeOrderModal() {
      document.getElementById('orderModal').classList.remove('open');
    }

    function setModalTier(tier, price, pages) {
      currentTier = tier;
      currentPrice = price;
      document.querySelectorAll('#modalTierGroup .tier-btn').forEach(b => {
        if (b.getAttribute('data-tier') === tier) b.classList.add('selected');
        else b.classList.remove('selected');
      });
      document.getElementById('btnPriceDisplay').textContent = price;
    }

    function openBundleModal(bundleId, title, price) {
      currentTopicId = bundleId;
      document.getElementById('modalReportTitle').textContent = title;
      currentTier = 'bundle';
      currentPrice = price;
      document.getElementById('modalTierGroup').style.display = 'none';
      document.getElementById('btnPriceDisplay').textContent = price;
      document.getElementById('orderModal').classList.add('open');
    }

    async function calculatePreviewOnly() {
      const name = document.getElementById('seekerName').value.trim() || 'Seeker';
      const day = parseInt(document.getElementById('dobDay').value) || 15;
      const month = parseInt(document.getElementById('dobMonth').value) || 8;
      const year = parseInt(document.getElementById('dobYear').value) || 1990;

      try {
        const resp = await fetch('/api/v1/reports/calculate', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: name,
            day: day,
            month: month,
            year: year,
            topic_id: currentTopicId,
            tier: currentTier
          })
        });
        if (resp.ok) {
          const data = await resp.json();
          const f = data.deterministic_findings;
          const detailsBox = document.getElementById('liveCalcDetails');
          detailsBox.innerHTML = `
            <strong>Driver:</strong> ${f.driver_number} (${f.driver_planet}) | 
            <strong>Conductor:</strong> ${f.conductor_number} (${f.conductor_planet}) | 
            <strong>Chaldean Root:</strong> ${f.chaldean_name_compound} → ${f.chaldean_name_root} (${f.chaldean_name_planet})<br/>
            <strong>Present Numbers:</strong> [${f.present_frequencies.join(', ')}] | 
            <strong>Karmic Gaps:</strong> [${f.missing_karmic_gaps.join(', ')}]
          `;
          document.getElementById('liveCalcBox').style.display = 'block';
        }
      } catch (err) {
        console.error('Calculation error:', err);
      }
    }

    async function handleGenerateSubmit(e) {
      e.preventDefault();
      const name = document.getElementById('seekerName').value.trim();
      const day = parseInt(document.getElementById('dobDay').value);
      const month = parseInt(document.getElementById('dobMonth').value);
      const year = parseInt(document.getElementById('dobYear').value);

      const btn = document.getElementById('btnSubmitGenerate');
      btn.disabled = true;
      btn.textContent = 'Generating PDF...';

      try {
        const resp = await fetch('/api/v1/reports/generate-pdf', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: name,
            day: day,
            month: month,
            year: year,
            topic_id: currentTopicId,
            tier: currentTier
          })
        });

        if (resp.ok) {
          const blob = await resp.blob();
          const downloadUrl = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = downloadUrl;
          a.download = `NumerosVision_${name.replace(/\s+/g, '_')}_${currentTier}.pdf`;
          document.body.appendChild(a);
          a.click();
          a.remove();
          closeOrderModal();
        } else {
          alert('Could not generate PDF. Please verify details and retry.');
        }
      } catch (err) {
        console.error('Error generating PDF:', err);
        alert('Network error while generating report.');
      } finally {
        btn.disabled = false;
        btn.innerHTML = `Generate & Download PDF (₹<span id="btnPriceDisplay">${currentPrice}</span>) ✦`;
      }
    }
  </script>
</body>
</html>
'''

    with open(CATALOGUE_PATH, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Successfully refined {CATALOGUE_PATH} with unified pricing architecture!")

if __name__ == '__main__':
    build_refined_catalogue_html()
