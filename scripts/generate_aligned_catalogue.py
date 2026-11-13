import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

catalogue_html = """<!DOCTYPE html>
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

  <!-- Fonts & Master Stylesheets -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@500;600;700;800&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
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
    /* ── MASTER THEME TOKENS (VENUS PEARL & JUPITER GOLD) ── */
    :root {
      --gold-dark: #8B6914;
      --gold: #C9A227;
      --gold-light: #E2B84B;
      --pearl-bg: #FFFDF7;
      --pearl-mid: #F7F3EA;
      --ink: #523E28;
      --ink-muted: #7A654D;
      --emerald: #16835B;
      --border-gold: rgba(201, 162, 39, 0.38);
      --border-amber: rgba(201, 162, 39, 0.32);
      --card-bg: #FFFFFF;
      --shadow-amber: 0 8px 30px rgba(180, 155, 110, 0.09);
    }

    body {
      background-color: var(--pearl-bg);
      color: var(--ink);
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      margin: 0;
      padding: 0;
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }

    /* Fallback protection for header brand seal */
    .nv-brand-seal {
      width: 46px;
      height: 46px;
      border-radius: 50%;
      border: 2px solid var(--gold);
      padding: 2px;
      background: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 3px 12px rgba(201, 162, 39, 0.28);
      flex-shrink: 0;
    }
    .nv-brand-seal img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
    }

    .catalogue-wrap {
      max-width: var(--nv-container-max, 1240px);
      margin: 0 auto;
      padding: 24px var(--nv-container-pad, clamp(16px, 3.5vw, 24px)) 80px;
      box-sizing: border-box;
    }

    /* ── Hero Fold with Celestial Glow ── */
    .reports-hero {
      text-align: center;
      padding: clamp(36px, 5vw, 64px) clamp(16px, 3vw, 24px) clamp(30px, 4vw, 48px);
      margin-bottom: 40px;
      border-radius: 24px;
      background: radial-gradient(circle at 50% 15%, rgba(201, 162, 39, 0.12) 0%, rgba(255, 253, 247, 0) 70%);
      position: relative;
    }

    .hero-eyebrow-chip {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: 'Cinzel', serif;
      font-size: 0.76rem;
      font-weight: 700;
      letter-spacing: 0.22em;
      text-transform: uppercase;
      color: var(--gold-dark);
      background: rgba(201, 162, 39, 0.1);
      border: 1px solid var(--border-amber);
      padding: 6px 18px;
      border-radius: 999px;
      margin-bottom: 18px;
    }

    .reports-h1 {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: clamp(2.4rem, 5.5vw, 3.8rem);
      font-weight: 600;
      color: var(--gold-dark);
      line-height: 1.15;
      margin: 0 auto 16px;
      max-width: 900px;
    }

    .reports-lead {
      font-size: clamp(1rem, 2vw, 1.18rem);
      color: var(--ink-muted);
      max-width: 780px;
      margin: 0 auto 28px;
      line-height: 1.75;
    }

    .hero-trust-bar {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: clamp(12px, 2.5vw, 28px);
      flex-wrap: wrap;
      margin-top: 10px;
    }

    .trust-chip {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.82rem;
      font-weight: 600;
      color: var(--ink);
      background: #FFFFFF;
      border: 1px solid var(--border-gold);
      padding: 6px 14px;
      border-radius: 999px;
      box-shadow: 0 2px 8px rgba(180, 155, 110, 0.06);
    }
    .trust-chip span.star {
      color: var(--gold);
      font-size: 0.85rem;
    }

    /* ── Standard Master Buttons (Jupiter Gold & Venus Pearl) ── */
    .btn-gold-primary {
      background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
      color: #FFFFFF !important;
      font-family: 'Inter', sans-serif;
      font-weight: 700;
      font-size: 0.88rem;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      padding: 13px 26px;
      border-radius: 999px;
      text-decoration: none;
      box-shadow: 0 4px 16px rgba(201, 162, 39, 0.32);
      transition: all 0.25s ease;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      border: none;
      cursor: pointer;
    }
    .btn-gold-primary:hover {
      background: linear-gradient(135deg, #E2B84B 0%, #C9A227 100%);
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(201, 162, 39, 0.45);
    }

    .btn-pearl-secondary {
      background: #FFFFFF;
      color: var(--gold-dark) !important;
      border: 1.5px solid var(--border-gold);
      font-family: 'Inter', sans-serif;
      font-weight: 600;
      font-size: 0.88rem;
      padding: 12px 24px;
      border-radius: 999px;
      text-decoration: none;
      transition: all 0.25s ease;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      cursor: pointer;
    }
    .btn-pearl-secondary:hover {
      background: #F7F3EA;
      border-color: var(--gold);
      transform: translateY(-2px);
      box-shadow: 0 4px 14px rgba(180, 155, 110, 0.14);
    }

    /* ── 3-Tier Comparison Box ── */
    .pricing-comparison-box {
      background: #FFFFFF;
      border: 1.5px solid var(--border-gold);
      border-radius: 20px;
      padding: clamp(22px, 3.5vw, 36px);
      margin-bottom: 48px;
      box-shadow: var(--shadow-amber);
      overflow-x: auto;
    }
    .comparison-title {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: clamp(1.6rem, 3vw, 2.2rem);
      color: var(--gold-dark);
      text-align: center;
      margin: 0 0 8px;
      font-weight: 700;
    }
    .comparison-sub {
      text-align: center;
      font-size: 0.92rem;
      color: var(--ink-muted);
      margin: 0 0 24px;
    }
    .comp-table {
      width: 100%;
      border-collapse: collapse;
      min-width: 680px;
      text-align: left;
      font-size: 0.88rem;
    }
    .comp-table th, .comp-table td {
      padding: 14px 18px;
      border-bottom: 1px solid rgba(201, 162, 39, 0.2);
    }
    .comp-table th {
      font-family: 'Cinzel', serif;
      color: var(--gold-dark);
      font-size: 0.92rem;
      background: rgba(201, 162, 39, 0.06);
    }
    .comp-table tr.highlight-col td:nth-child(3),
    .comp-table th:nth-child(3) {
      background: rgba(201, 162, 39, 0.08);
      font-weight: 600;
    }
    .tier-price-tag {
      font-family: 'Cinzel', serif;
      font-size: 1.25rem;
      font-weight: 800;
      color: var(--gold-dark);
      display: block;
      margin-top: 4px;
    }

    /* ── Category Filter Tabs ── */
    .nv-cat-tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      justify-content: center;
      margin-bottom: 36px;
    }
    .nv-cat-tab {
      background: #FFFFFF;
      border: 1.5px solid var(--border-gold);
      color: var(--ink);
      padding: 10px 22px;
      border-radius: 999px;
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s ease;
    }
    .nv-cat-tab:hover, .nv-cat-tab.active {
      background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
      color: #FFFFFF;
      border-color: var(--gold-dark);
      box-shadow: 0 4px 14px rgba(201, 162, 39, 0.32);
    }

    /* ── Grid & Standalone Report Cards ── */
    .reports-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 28px;
      margin-bottom: 56px;
    }
    .report-card {
      background: var(--card-bg);
      border: 1.5px solid var(--border-gold);
      border-radius: 20px;
      padding: 26px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
      position: relative;
      box-shadow: var(--shadow-amber);
    }
    .report-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 12px 34px rgba(139, 105, 20, 0.15);
      border-color: var(--gold);
    }
    .report-card-top { margin-bottom: 16px; }
    .report-icon-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 12px;
    }
    .report-icon { font-size: 2rem; }
    .report-category-pill {
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--gold-dark);
      background: rgba(201, 162, 39, 0.12);
      border: 1px solid var(--border-amber);
      padding: 4px 10px;
      border-radius: 999px;
    }
    .report-card h3 {
      font-family: 'Cinzel', serif;
      font-size: 1.25rem;
      color: var(--gold-dark);
      margin: 0 0 10px;
      line-height: 1.35;
      min-height: 2.7em;
    }
    .report-desc {
      font-size: 0.88rem;
      color: var(--ink-muted);
      line-height: 1.6;
      margin-bottom: 18px;
      min-height: 2.9em;
    }

    /* ── Interactive 3-Tier Selector Buttons on Card ── */
    .tier-selector-box {
      background: #FDFBF5;
      border: 1px solid var(--border-gold);
      border-radius: 12px;
      padding: 10px 12px;
      margin-bottom: 20px;
    }
    .tier-selector-title {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
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
      border-radius: 8px;
      padding: 8px 4px;
      text-align: center;
      cursor: pointer;
      font-size: 0.78rem;
      transition: all 0.2s ease;
      color: var(--ink);
    }
    .tier-btn:hover, .tier-btn.selected {
      background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
      color: #FFFFFF;
      border-color: var(--gold-dark);
      font-weight: 700;
      box-shadow: 0 3px 8px rgba(139, 105, 20, 0.28);
    }
    .tier-btn small { display: block; font-size: 0.68rem; opacity: 0.95; }

    .deliverables-list {
      list-style: none;
      padding: 0;
      margin: 0 0 22px;
      font-size: 0.85rem;
      color: var(--ink);
      line-height: 1.65;
    }
    .deliverables-list li {
      padding-left: 20px;
      position: relative;
      margin-bottom: 6px;
    }
    .deliverables-list li::before {
      content: "✦";
      position: absolute;
      left: 0;
      color: var(--gold);
      font-size: 0.75rem;
    }

    .card-footer-action {
      display: flex;
      flex-direction: column;
      gap: 10px;
      margin-top: auto;
    }
    .card-price-display {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      margin-bottom: 4px;
    }
    .price-amount {
      font-family: 'Cinzel', serif;
      font-size: 1.55rem;
      font-weight: 800;
      color: var(--gold-dark);
    }
    .price-pages-tag {
      font-size: 0.82rem;
      color: var(--ink-muted);
      font-weight: 600;
    }

    /* ── Multi-Report Bundles Section ── */
    .bundles-section {
      background: #FFFFFF;
      border: 1.5px solid var(--border-gold);
      border-radius: 20px;
      padding: clamp(24px, 4vw, 40px);
      margin-bottom: 56px;
      box-shadow: var(--shadow-amber);
    }
    .bundles-header { text-align: center; margin-bottom: 32px; }
    .bundles-title {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: clamp(1.8rem, 3.2vw, 2.5rem);
      color: var(--gold-dark);
      margin: 0 0 8px;
      font-weight: 700;
    }
    .bundles-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 26px;
    }
    .bundle-card {
      background: #FFFDF7;
      border: 1.5px solid var(--border-gold);
      border-radius: 18px;
      padding: 26px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: transform 0.25s ease, box-shadow 0.25s ease;
    }
    .bundle-card:hover {
      transform: translateY(-3px);
      box-shadow: 0 10px 28px rgba(139, 105, 20, 0.12);
    }
    .bundle-card.featured {
      border-color: var(--gold);
      box-shadow: 0 8px 26px rgba(201, 162, 39, 0.2);
      background: #FFFFFF;
    }
    .bundle-savings {
      font-size: 0.74rem;
      font-weight: 700;
      color: var(--emerald);
      background: rgba(22, 131, 91, 0.12);
      border: 1px solid rgba(22, 131, 91, 0.25);
      padding: 4px 10px;
      border-radius: 999px;
      display: inline-block;
      margin-bottom: 12px;
    }

    /* ── Interactive Delivery & Calculation Modal ── */
    .nv-modal-backdrop {
      display: none;
      position: fixed;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(82, 62, 40, 0.65);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      z-index: 2000;
      align-items: center;
      justify-content: center;
      padding: 20px;
      box-sizing: border-box;
    }
    .nv-modal-backdrop.open { display: flex; }
    .nv-modal-window {
      background: #FFFDF7;
      border: 2px solid var(--gold);
      border-radius: 22px;
      max-width: 560px;
      width: 100%;
      padding: 32px 28px;
      box-shadow: 0 18px 46px rgba(82, 62, 40, 0.35);
      position: relative;
      max-height: 90vh;
      overflow-y: auto;
      box-sizing: border-box;
    }
    .modal-close {
      position: absolute;
      top: 16px;
      right: 18px;
      font-size: 1.8rem;
      background: none;
      border: none;
      cursor: pointer;
      color: var(--ink-muted);
      line-height: 1;
    }
    .form-group { margin-bottom: 15px; }
    .form-label {
      font-size: 0.85rem;
      font-weight: 700;
      color: var(--ink);
      display: block;
      margin-bottom: 6px;
    }
    .form-input {
      width: 100%;
      box-sizing: border-box;
      padding: 12px 14px;
      border: 1.5px solid var(--border-gold);
      border-radius: 10px;
      font-size: 0.92rem;
      background: #FFFFFF;
      color: var(--ink);
      font-family: inherit;
    }
    .form-input:focus {
      outline: none;
      border-color: var(--gold-dark);
      box-shadow: 0 0 0 3px rgba(201, 162, 39, 0.22);
    }
  </style>
</head>

<body>
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-KW6GQRVZ"
  height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->

  <!-- ── 1. CANONICAL MASTER HEADER MATCHING WEBSITE & APP ── -->
  <header class="nv-header">
    <div class="nv-nav-container">
      <a href="/" class="nv-brand-link" title="Numeros Vision — Anveil Every Charm">
        <div class="nv-brand-seal">
          <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
        </div>
        <div class="nv-brand-text">
          <span class="nv-brand-title">NUMEROS VISION</span>
          <span class="nv-brand-tagline">ANVEIL EVERY CHARM</span>
        </div>
      </a>

      <!-- Desktop Navigation Menu -->
      <nav aria-label="Main Navigation">
        <ul class="nv-nav-menu" id="nvNavMenu">
          <!-- 1. About Us -->
          <li class="nv-nav-item">
            <a href="/about/" class="nv-nav-link" title="About Numeros Vision">About Us</a>
          </li>

          <!-- 2. Calculators Dropdown -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Calculators</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/tools/baby-naming" class="nv-submenu-link"><span class="nv-sub-icon">👶</span> <span>Auspicious Baby Naming</span> <span class="nv-sub-tag">Hot</span></a></li>
              <li><a href="/tools/name-numerology" class="nv-submenu-link"><span class="nv-sub-icon">✍️</span> <span>Name Analysis &amp; Balancing</span></a></li>
              <li><a href="/tools/mobile-numerology" class="nv-submenu-link"><span class="nv-sub-icon">📱</span> <span>Mobile Number Audit</span></a></li>
              <li><a href="/tools/kundali-milan" class="nv-submenu-link"><span class="nv-sub-icon">💍</span> <span>Kundali Milan &amp; Synastry</span></a></li>
              <li><a href="/tools/business-numerology" class="nv-submenu-link"><span class="nv-sub-icon">💼</span> <span>Business &amp; Brand Name</span></a></li>
              <li><a href="/tools/life-path-calculator" class="nv-submenu-link"><span class="nv-sub-icon">🧭</span> <span>Life Path Calculator</span></a></li>
              <li><a href="/tools/lo-shu-grid" class="nv-submenu-link"><span class="nv-sub-icon">🔲</span> <span>Lo Shu Magic Grid</span></a></li>
              <li><a href="/tools/vehicle-numerology" class="nv-submenu-link"><span class="nv-sub-icon">🚗</span> <span>Vehicle Numerology</span></a></li>
              <li><a href="/tools/property-numerology" class="nv-submenu-link"><span class="nv-sub-icon">🏠</span> <span>House &amp; Property Audit</span></a></li>
              <li><a href="/tools/blessing-years" class="nv-submenu-link"><span class="nv-sub-icon">📅</span> <span>Blessing Years Timeline</span></a></li>
              <li class="nv-submenu-footer"><a href="/calculators/" class="nv-submenu-all">View All 10+ Calculators →</a></li>
            </ul>
          </li>

          <!-- 3. Charm AI -->
          <li class="nv-nav-item"><a href="/#charm-ai" class="nv-nav-link">Charm AI</a></li>

          <!-- 4. Reports (Active) -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle active" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button" style="color:var(--gold-dark); font-weight:700;">
              <span>Reports</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/reports_catalogue/" class="nv-submenu-link"><span class="nv-sub-icon">📜</span> <span>Unified Reports Catalogue</span> <span class="nv-sub-tag">New</span></a></li>
              <li><a href="/consultation/" class="nv-submenu-link"><span class="nv-sub-icon">👤</span> <span>1-on-1 Consultation</span></a></li>
              <li><a href="/practitioner/" class="nv-submenu-link"><span class="nv-sub-icon">🧑‍💼</span> <span>Practitioner Workspace CRM</span></a></li>
            </ul>
          </li>

          <!-- 5. Insights -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Insights</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/insights/" class="nv-submenu-link"><span class="nv-sub-icon">📚</span> <span>Numerology Knowledge Hub</span></a></li>
              <li><a href="/blog/master-numbers-11-22-33" class="nv-submenu-link"><span class="nv-sub-icon">🔢</span> <span>Master Numbers 11, 22, 33</span></a></li>
              <li><a href="/blog/chaldean-compound-numbers-meanings" class="nv-submenu-link"><span class="nv-sub-icon">⚖️</span> <span>Chaldean vs Pythagorean</span></a></li>
              <li><a href="/blog/lo-shu-grid-8-planes" class="nv-submenu-link"><span class="nv-sub-icon">🔲</span> <span>Lo Shu Grid 8 Planes</span></a></li>
              <li><a href="/blog/gemstone-remedies" class="nv-submenu-link"><span class="nv-sub-icon">💎</span> <span>Gemstone Remedies Guide</span></a></li>
            </ul>
          </li>

          <!-- 6. Pricing -->
          <li class="nv-nav-item"><a href="/pricing/" class="nv-nav-link">Pricing</a></li>

          <!-- 7. Contact Us -->
          <li class="nv-nav-item"><a href="/contact/" class="nv-nav-link" title="Contact Us">Contact Us</a></li>
        </ul>
      </nav>

      <!-- Action Buttons & Hamburger -->
      <div class="nv-nav-actions">
        <a href="/#birth-profile" class="nv-btn-cta">Discover My Numbers ✦</a>
        <button class="nv-mobile-toggle" onclick="toggleMobileNav(event)" aria-label="Toggle Navigation">☰</button>
      </div>
    </div>
  </header>

  <!-- ── 2. CANONICAL MASTER BREADCRUMBS ── -->
  <nav class="nv-breadcrumbs" aria-label="Breadcrumb">
    <a href="/">Home</a>
    <span class="nv-breadcrumbs-sep">/</span>
    <span class="nv-breadcrumbs-current">Reports Catalogue</span>
  </nav>

  <!-- ── 3. MAIN CATALOGUE WRAPPER ── -->
  <main class="catalogue-wrap">

    <!-- Hero Fold -->
    <section class="reports-hero">
      <div class="hero-eyebrow-chip">✦ UNIFIED NUMEROLOGY REPORTS CATALOGUE ✦</div>
      <h1 class="reports-h1">Personalised Dossiers &amp; Certified PDF Blueprints</h1>
      <p class="reports-lead">
        Choose from 10 topic-specific dossiers across relationships, career, wealth, and destiny.
        Standardised into three clear tiers — Basic (3 pages), Advanced (12 pages), and Premium (32 pages) —
        powered by 100% deterministic mathematical calculations and safe planetary remedies.
      </p>

      <div class="hero-trust-bar">
        <div class="trust-chip"><span class="star">✦</span> 100% Deterministic Engine</div>
        <div class="trust-chip"><span class="star">✦</span> Dual Chaldean &amp; Pythagorean Synthesis</div>
        <div class="trust-chip"><span class="star">✦</span> Safe 7-Layer Planetary Remedies</div>
        <div class="trust-chip"><span class="star">✦</span> Statutory DPDP 2023 &amp; GDPR Compliant</div>
      </div>
    </section>

    <!-- ── 3-TIER COMPARISON BOX ── -->
    <section class="pricing-comparison-box">
      <h2 class="comparison-title">Standardised Pricing Across Every Report</h2>
      <p class="comparison-sub">Every report topic follows the exact same 3-tier structure with transparent page counts and deliverable depth.</p>

      <table class="comp-table">
        <thead>
          <tr>
            <th>Deliverable Metric</th>
            <th>Basic Tier<span class="tier-price-tag">₹199</span></th>
            <th>Advanced Tier (Most Popular)<span class="tier-price-tag">₹510</span></th>
            <th>Premium Dossier<span class="tier-price-tag">₹1,050</span></th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><strong>Exact PDF Page Count</strong></td>
            <td><strong>3 Pages</strong></td>
            <td><strong>12 Pages</strong></td>
            <td><strong>32 Pages</strong></td>
          </tr>
          <tr>
            <td><strong>Core Engine Depth</strong></td>
            <td>Vedic Driver &amp; Conductor basics</td>
            <td>Vedic + Chaldean acoustic compound</td>
            <td>Dual Vedic + Chaldean + Pythagorean Synthesis</td>
          </tr>
          <tr>
            <td><strong>Timing Windows</strong></td>
            <td>Current annual cycle</td>
            <td>3-Year Dasha &amp; Antardasha cycles</td>
            <td>10-Year Master Timeline with quarter breakdown</td>
          </tr>
          <tr>
            <td><strong>Remedies &amp; Balancing</strong></td>
            <td>Initial color &amp; day guidance</td>
            <td>7-Layer Safe Planetary Remedy Suite</td>
            <td>Full Rectification Protocol + Gemstone Safety</td>
          </tr>
          <tr>
            <td><strong>Delivery &amp; Format</strong></td>
            <td>Instant PDF Download + Email</td>
            <td>Instant High-Res PDF + Email Dossier</td>
            <td>Sovereign Master Dossier + Complete Appendix</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- ── CATEGORY FILTER TABS ── -->
    <div class="nv-cat-tabs">
      <button class="nv-cat-tab active" onclick="filterReports('all', this)">All Reports (10)</button>
      <button class="nv-cat-tab" onclick="filterReports('relationships', this)">Relationships</button>
      <button class="nv-cat-tab" onclick="filterReports('career', this)">Career &amp; Wealth</button>
      <button class="nv-cat-tab" onclick="filterReports('destiny', this)">Life Destiny</button>
      <button class="nv-cat-tab" onclick="filterReports('business', this)">Business &amp; Brand</button>
    </div>

    <!-- ── 10 STANDALONE REPORT CARDS GRID ── -->
    <section class="reports-grid" id="reportsGrid">

      <!-- 1. Vedic Destiny Report -->
      <article class="report-card" data-category="destiny" data-topic="vedic_destiny">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">📜</span>
            <span class="report-category-pill">Life Destiny</span>
          </div>
          <h3>Vedic Destiny &amp; Karma Blueprint</h3>
          <p class="report-desc">Comprehensive analysis of Driver (Mulank), Conductor (Bhagyank), and karmic life path trajectory.</p>

          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth &amp; Length:</span>
            <div class="tier-options-group">
              <button class="tier-btn" onclick="selectTier(this, 'vedic_destiny', 'basic')">Basic<small>3 Pages</small></button>
              <button class="tier-btn selected" onclick="selectTier(this, 'vedic_destiny', 'advanced')">Advanced<small>12 Pages</small></button>
              <button class="tier-btn" onclick="selectTier(this, 'vedic_destiny', 'premium')">Premium<small>32 Pages</small></button>
            </div>
          </div>

          <ul class="deliverables-list" id="deliv_vedic_destiny">
            <li>Driver &amp; Conductor core mathematical breakdown</li>
            <li>3-Year Dasha &amp; Mahadasha cycle timing</li>
            <li>Karmic obstacle mitigation protocol</li>
            <li>7-layer personalized planetary lifestyle remedies</li>
          </ul>
        </div>

        <div class="card-footer-action">
          <div class="card-price-display">
            <span class="price-amount" id="price_vedic_destiny">₹510</span>
            <span class="price-pages-tag" id="pages_vedic_destiny">12 Pages</span>
          </div>
          <button class="btn-gold-primary" onclick="openOrderModal('vedic_destiny', 'Vedic Destiny & Karma Blueprint')">Configure &amp; Download PDF ✦</button>
          <a href="/sample_roadmap/" class="btn-pearl-secondary">View Sample Structure 📄</a>
        </div>
      </article>

      <!-- 2. Name Balancing Report -->
      <article class="report-card" data-category="destiny" data-topic="name_balancing">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">✍️</span>
            <span class="report-category-pill">Life Destiny</span>
          </div>
          <h3>Name Balancing &amp; Acoustic Optimizer</h3>
          <p class="report-desc">Chaldean sound frequency audit, compound number evaluation, and auspicious spelling alignment.</p>

          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth &amp; Length:</span>
            <div class="tier-options-group">
              <button class="tier-btn" onclick="selectTier(this, 'name_balancing', 'basic')">Basic<small>3 Pages</small></button>
              <button class="tier-btn selected" onclick="selectTier(this, 'name_balancing', 'advanced')">Advanced<small>12 Pages</small></button>
              <button class="tier-btn" onclick="selectTier(this, 'name_balancing', 'premium')">Premium<small>32 Pages</small></button>
            </div>
          </div>

          <ul class="deliverables-list" id="deliv_name_balancing">
            <li>Chaldean letter-by-letter sound frequency mapping</li>
            <li>Compound total evaluation &amp; vibration harmony check</li>
            <li>Recommended balanced spelling alternatives</li>
            <li>Practical signature &amp; everyday usage guidelines</li>
          </ul>
        </div>

        <div class="card-footer-action">
          <div class="card-price-display">
            <span class="price-amount" id="price_name_balancing">₹510</span>
            <span class="price-pages-tag" id="pages_name_balancing">12 Pages</span>
          </div>
          <button class="btn-gold-primary" onclick="openOrderModal('name_balancing', 'Name Balancing & Acoustic Optimizer')">Configure &amp; Download PDF ✦</button>
          <a href="/tools/name-balancing/" class="btn-pearl-secondary">View Sample Structure 📄</a>
        </div>
      </article>

      <!-- 3. Relationship Compatibility -->
      <article class="report-card" data-category="relationships" data-topic="relationship_compatibility">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">💍</span>
            <span class="report-category-pill">Relationships</span>
          </div>
          <h3>Relationship Compatibility &amp; Synastry</h3>
          <p class="report-desc">Dual partner cross-chart audit examining emotional resonance, financial harmony, and long-term synergy.</p>

          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth &amp; Length:</span>
            <div class="tier-options-group">
              <button class="tier-btn" onclick="selectTier(this, 'relationship_compatibility', 'basic')">Basic<small>3 Pages</small></button>
              <button class="tier-btn selected" onclick="selectTier(this, 'relationship_compatibility', 'advanced')">Advanced<small>12 Pages</small></button>
              <button class="tier-btn" onclick="selectTier(this, 'relationship_compatibility', 'premium')">Premium<small>32 Pages</small></button>
            </div>
          </div>

          <ul class="deliverables-list" id="deliv_relationship_compatibility">
            <li>Driver-to-Driver temperament matrix</li>
            <li>Conductor-to-Conductor long-term karmic alignment</li>
            <li>Friction zones and emotional conflict mitigation</li>
            <li>Mutual planetary remedies for home harmony</li>
          </ul>
        </div>

        <div class="card-footer-action">
          <div class="card-price-display">
            <span class="price-amount" id="price_relationship_compatibility">₹510</span>
            <span class="price-pages-tag" id="pages_relationship_compatibility">12 Pages</span>
          </div>
          <button class="btn-gold-primary" onclick="openOrderModal('relationship_compatibility', 'Relationship Compatibility & Synastry')">Configure &amp; Download PDF ✦</button>
          <a href="/tools/compatibility-calculator/" class="btn-pearl-secondary">View Sample Structure 📄</a>
        </div>
      </article>

      <!-- 4. Career & Wealth Forecast -->
      <article class="report-card" data-category="career" data-topic="career_wealth_forecast">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">📈</span>
            <span class="report-category-pill">Career &amp; Wealth</span>
          </div>
          <h3>Career &amp; Wealth Forecast Dossier</h3>
          <p class="report-desc">Detailed timing windows for promotion, capital investment, business pivots, and financial growth cycles.</p>

          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth &amp; Length:</span>
            <div class="tier-options-group">
              <button class="tier-btn" onclick="selectTier(this, 'career_wealth_forecast', 'basic')">Basic<small>3 Pages</small></button>
              <button class="tier-btn selected" onclick="selectTier(this, 'career_wealth_forecast', 'advanced')">Advanced<small>12 Pages</small></button>
              <button class="tier-btn" onclick="selectTier(this, 'career_wealth_forecast', 'premium')">Premium<small>32 Pages</small></button>
            </div>
          </div>

          <ul class="deliverables-list" id="deliv_career_wealth_forecast">
            <li>High-potential professional sectors based on planetary rulership</li>
            <li>Annual &amp; monthly wealth window timings</li>
            <li>Money-loss prevention numbers &amp; risk factors</li>
            <li>Auspicious days for contract signing &amp; launches</li>
          </ul>
        </div>

        <div class="card-footer-action">
          <div class="card-price-display">
            <span class="price-amount" id="price_career_wealth_forecast">₹510</span>
            <span class="price-pages-tag" id="pages_career_wealth_forecast">12 Pages</span>
          </div>
          <button class="btn-gold-primary" onclick="openOrderModal('career_wealth_forecast', 'Career & Wealth Forecast Dossier')">Configure &amp; Download PDF ✦</button>
          <a href="/pricing/" class="btn-pearl-secondary">View Sample Structure 📄</a>
        </div>
      </article>

      <!-- 5. Business Brand Alignment -->
      <article class="report-card" data-category="business" data-topic="business_brand_alignment">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">💼</span>
            <span class="report-category-pill">Business &amp; Brand</span>
          </div>
          <h3>Business Brand &amp; Commercial Alignment</h3>
          <p class="report-desc">Evaluation of company legal names, brand names, partner equity distribution, and category archetype fit.</p>

          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth &amp; Length:</span>
            <div class="tier-options-group">
              <button class="tier-btn" onclick="selectTier(this, 'business_brand_alignment', 'basic')">Basic<small>3 Pages</small></button>
              <button class="tier-btn selected" onclick="selectTier(this, 'business_brand_alignment', 'advanced')">Advanced<small>12 Pages</small></button>
              <button class="tier-btn" onclick="selectTier(this, 'business_brand_alignment', 'premium')">Premium<small>32 Pages</small></button>
            </div>
          </div>

          <ul class="deliverables-list" id="deliv_business_brand_alignment">
            <li>Brand name Chaldean compound number resonance</li>
            <li>Category archetype alignment (Mercury, Jupiter, Sun)</li>
            <li>Founder compatibility with company name vibration</li>
            <li>Auspicious dates for incorporation and domain launches</li>
          </ul>
        </div>

        <div class="card-footer-action">
          <div class="card-price-display">
            <span class="price-amount" id="price_business_brand_alignment">₹510</span>
            <span class="price-pages-tag" id="pages_business_brand_alignment">12 Pages</span>
          </div>
          <button class="btn-gold-primary" onclick="openOrderModal('business_brand_alignment', 'Business Brand & Commercial Alignment')">Configure &amp; Download PDF ✦</button>
          <a href="/tools/business-numerology/" class="btn-pearl-secondary">View Sample Structure 📄</a>
        </div>
      </article>

      <!-- 6. Auspicious Baby Naming -->
      <article class="report-card" data-category="destiny" data-topic="baby_naming">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">👶</span>
            <span class="report-category-pill">Life Destiny</span>
          </div>
          <h3>Auspicious Baby Naming Blueprint</h3>
          <p class="report-desc">Traditional Vedic Nakshatra first-syllable selection matched with auspicious Chaldean compound totals.</p>

          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth &amp; Length:</span>
            <div class="tier-options-group">
              <button class="tier-btn" onclick="selectTier(this, 'baby_naming', 'basic')">Basic<small>3 Pages</small></button>
              <button class="tier-btn selected" onclick="selectTier(this, 'baby_naming', 'advanced')">Advanced<small>12 Pages</small></button>
              <button class="tier-btn" onclick="selectTier(this, 'baby_naming', 'premium')">Premium<small>32 Pages</small></button>
            </div>
          </div>

          <ul class="deliverables-list" id="deliv_baby_naming">
            <li>Birth chart Nakshatra sound syllable analysis</li>
            <li>20+ curated auspicious name suggestions</li>
            <li>Parent compatibility &amp; family harmony evaluation</li>
            <li>Lifelong lucky colors, metals, and education direction</li>
          </ul>
        </div>

        <div class="card-footer-action">
          <div class="card-price-display">
            <span class="price-amount" id="price_baby_naming">₹510</span>
            <span class="price-pages-tag" id="pages_baby_naming">12 Pages</span>
          </div>
          <button class="btn-gold-primary" onclick="openOrderModal('baby_naming', 'Auspicious Baby Naming Blueprint')">Configure &amp; Download PDF ✦</button>
          <a href="/tools/baby-naming/" class="btn-pearl-secondary">View Sample Structure 📄</a>
        </div>
      </article>

      <!-- 7. Mobile Numerology Audit -->
      <article class="report-card" data-category="career" data-topic="mobile_numerology">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">📱</span>
            <span class="report-category-pill">Career &amp; Wealth</span>
          </div>
          <h3>Mobile Phone Numerology &amp; Pair Audit</h3>
          <p class="report-desc">Analysis of total phone vibration, consecutive pairs, and malefic combination filtering for business calls.</p>

          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth &amp; Length:</span>
            <div class="tier-options-group">
              <button class="tier-btn" onclick="selectTier(this, 'mobile_numerology', 'basic')">Basic<small>3 Pages</small></button>
              <button class="tier-btn selected" onclick="selectTier(this, 'mobile_numerology', 'advanced')">Advanced<small>12 Pages</small></button>
              <button class="tier-btn" onclick="selectTier(this, 'mobile_numerology', 'premium')">Premium<small>32 Pages</small></button>
            </div>
          </div>

          <ul class="deliverables-list" id="deliv_mobile_numerology">
            <li>Full 10-digit acoustic reduction &amp; compound breakdown</li>
            <li>Consecutive pair evaluation (wealth, conflict, delays)</li>
            <li>Driver/Conductor compatibility with current number</li>
            <li>Specific recommended digit patterns for new SIM selection</li>
          </ul>
        </div>

        <div class="card-footer-action">
          <div class="card-price-display">
            <span class="price-amount" id="price_mobile_numerology">₹510</span>
            <span class="price-pages-tag" id="pages_mobile_numerology">12 Pages</span>
          </div>
          <button class="btn-gold-primary" onclick="openOrderModal('mobile_numerology', 'Mobile Phone Numerology & Pair Audit')">Configure &amp; Download PDF ✦</button>
          <a href="/tools/mobile-numerology/" class="btn-pearl-secondary">View Sample Structure 📄</a>
        </div>
      </article>

      <!-- 8. Property & House Numerology -->
      <article class="report-card" data-category="destiny" data-topic="property_numerology">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">🏠</span>
            <span class="report-category-pill">Life Destiny</span>
          </div>
          <h3>Property, Flat &amp; House Number Audit</h3>
          <p class="report-desc">Evaluation of home number, floor number, and street address resonance for residential peace and wealth accumulation.</p>

          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth &amp; Length:</span>
            <div class="tier-options-group">
              <button class="tier-btn" onclick="selectTier(this, 'property_numerology', 'basic')">Basic<small>3 Pages</small></button>
              <button class="tier-btn selected" onclick="selectTier(this, 'property_numerology', 'advanced')">Advanced<small>12 Pages</small></button>
              <button class="tier-btn" onclick="selectTier(this, 'property_numerology', 'premium')">Premium<small>32 Pages</small></button>
            </div>
          </div>

          <ul class="deliverables-list" id="deliv_property_numerology">
            <li>Address digit compound reduction &amp; planetary governor</li>
            <li>Resident compatibility matrix across family members</li>
            <li>Non-destructive copper/brass nameplate balancing remedy</li>
            <li>Energy stabilization techniques for living spaces</li>
          </ul>
        </div>

        <div class="card-footer-action">
          <div class="card-price-display">
            <span class="price-amount" id="price_property_numerology">₹510</span>
            <span class="price-pages-tag" id="pages_property_numerology">12 Pages</span>
          </div>
          <button class="btn-gold-primary" onclick="openOrderModal('property_numerology', 'Property, Flat & House Number Audit')">Configure &amp; Download PDF ✦</button>
          <a href="/tools/property-numerology/" class="btn-pearl-secondary">View Sample Structure 📄</a>
        </div>
      </article>

      <!-- 9. Vehicle Numerology -->
      <article class="report-card" data-category="career" data-topic="vehicle_numerology">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">🚗</span>
            <span class="report-category-pill">Career &amp; Wealth</span>
          </div>
          <h3>Vehicle Registration &amp; Safety Audit</h3>
          <p class="report-desc">Analysis of vehicle registration numbers, accident-prone combinations, and color compatibility for safe transit.</p>

          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth &amp; Length:</span>
            <div class="tier-options-group">
              <button class="tier-btn" onclick="selectTier(this, 'vehicle_numerology', 'basic')">Basic<small>3 Pages</small></button>
              <button class="tier-btn selected" onclick="selectTier(this, 'vehicle_numerology', 'advanced')">Advanced<small>12 Pages</small></button>
              <button class="tier-btn" onclick="selectTier(this, 'vehicle_numerology', 'premium')">Premium<small>32 Pages</small></button>
            </div>
          </div>

          <ul class="deliverables-list" id="deliv_vehicle_numerology">
            <li>Plate letters + digits total reduction value</li>
            <li>Rahu/Ketu malefic pair warning assessment</li>
            <li>Owner driver number resonance with vehicle body</li>
            <li>Recommended auspicious colors and delivery dates</li>
          </ul>
        </div>

        <div class="card-footer-action">
          <div class="card-price-display">
            <span class="price-amount" id="price_vehicle_numerology">₹510</span>
            <span class="price-pages-tag" id="pages_vehicle_numerology">12 Pages</span>
          </div>
          <button class="btn-gold-primary" onclick="openOrderModal('vehicle_numerology', 'Vehicle Registration & Safety Audit')">Configure &amp; Download PDF ✦</button>
          <a href="/tools/vehicle-numerology/" class="btn-pearl-secondary">View Sample Structure 📄</a>
        </div>
      </article>

      <!-- 10. Lo Shu Grid 3x3 Analysis -->
      <article class="report-card" data-category="destiny" data-topic="lo_shu_grid">
        <div class="report-card-top">
          <div class="report-icon-row">
            <span class="report-icon">🔲</span>
            <span class="report-category-pill">Life Destiny</span>
          </div>
          <h3>Lo Shu Grid &amp; Elemental Plane Matrix</h3>
          <p class="report-desc">3×3 Magic square mapping of birth date digits across Thought, Will, Action, Mental, Emotional, and Practical planes.</p>

          <div class="tier-selector-box">
            <span class="tier-selector-title">Select Depth &amp; Length:</span>
            <div class="tier-options-group">
              <button class="tier-btn" onclick="selectTier(this, 'lo_shu_grid', 'basic')">Basic<small>3 Pages</small></button>
              <button class="tier-btn selected" onclick="selectTier(this, 'lo_shu_grid', 'advanced')">Advanced<small>12 Pages</small></button>
              <button class="tier-btn" onclick="selectTier(this, 'lo_shu_grid', 'premium')">Premium<small>32 Pages</small></button>
            </div>
          </div>

          <ul class="deliverables-list" id="deliv_lo_shu_grid">
            <li>Full 3×3 digit frequency distribution chart</li>
            <li>Completed yogas (Golden Yoga, Silver Yoga, Will Yoga)</li>
            <li>Missing number deficiency remediation via 5 elements</li>
            <li>Repeated digit behavioral tendencies and balancing</li>
          </ul>
        </div>

        <div class="card-footer-action">
          <div class="card-price-display">
            <span class="price-amount" id="price_lo_shu_grid">₹510</span>
            <span class="price-pages-tag" id="pages_lo_shu_grid">12 Pages</span>
          </div>
          <button class="btn-gold-primary" onclick="openOrderModal('lo_shu_grid', 'Lo Shu Grid & Elemental Plane Matrix')">Configure &amp; Download PDF ✦</button>
          <a href="/tools/lo-shu-grid/" class="btn-pearl-secondary">View Sample Structure 📄</a>
        </div>
      </article>

    </section>

    <!-- ── 4. MULTI-REPORT VALUE BUNDLES SECTION ── -->
    <section class="bundles-section">
      <div class="bundles-header">
        <h2 class="bundles-title">Multi-Report Curated Value Bundles</h2>
        <p class="comparison-sub">Combine foundational reports at bundled rates for comprehensive family and commercial guidance.</p>
      </div>

      <div class="bundles-grid">
        <!-- Starter Bundle -->
        <div class="bundle-card">
          <div>
            <span class="bundle-savings">SAVE ₹161 (31% OFF)</span>
            <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:0 0 10px; font-size:1.35rem;">Starter Bundle</h3>
            <p style="font-size:0.88rem; color:var(--ink-muted); margin-bottom:18px;">Essential entry package combining Vedic Destiny and Name Balancing into one clear snapshot.</p>
            <ul class="deliverables-list">
              <li>Vedic Destiny Report (3 Pages)</li>
              <li>Name Balancing Report (3 Pages)</li>
              <li>Acoustic sound frequency summary</li>
              <li>Instant unified PDF download</li>
            </ul>
          </div>
          <div>
            <div class="card-price-display">
              <span class="price-amount">₹349</span>
              <span class="price-pages-tag"><del style="color:#7A654D;">₹510</del> · 6 Total Pages</span>
            </div>
            <button class="btn-gold-primary" style="width:100%; box-sizing:border-box;" onclick="openOrderModal('bundle_starter', 'Starter Bundle (2 Reports)')">Order Starter Bundle ✦</button>
          </div>
        </div>

        <!-- Discovery Bundle (Featured) -->
        <div class="bundle-card featured">
          <div>
            <span class="bundle-savings">SAVE ₹491 (50% OFF) · MOST POPULAR</span>
            <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:0 0 10px; font-size:1.35rem;">Discovery Bundle</h3>
            <p style="font-size:0.88rem; color:var(--ink-muted); margin-bottom:18px;">Our highest-rated 3-report package covering life destiny, financial timing, and relationship compatibility.</p>
            <ul class="deliverables-list">
              <li>Vedic Destiny Advanced (12 Pages)</li>
              <li>Career &amp; Wealth Forecast (12 Pages)</li>
              <li>Relationship Compatibility (12 Pages)</li>
              <li>Full 3-Year Dasha &amp; Remedy protocol</li>
            </ul>
          </div>
          <div>
            <div class="card-price-display">
              <span class="price-amount">₹499</span>
              <span class="price-pages-tag"><del style="color:#7A654D;">₹990</del> · 36 Total Pages</span>
            </div>
            <button class="btn-gold-primary" style="width:100%; box-sizing:border-box;" onclick="openOrderModal('bundle_discovery', 'Discovery Bundle (3 Advanced Reports)')">Order Discovery Bundle ✦</button>
          </div>
        </div>

        <!-- Comprehensive Master Bundle -->
        <div class="bundle-card">
          <div>
            <span class="bundle-savings">SAVE ₹1,551 (61% OFF)</span>
            <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:0 0 10px; font-size:1.35rem;">Comprehensive Bundle</h3>
            <p style="font-size:0.88rem; color:var(--ink-muted); margin-bottom:18px;">The ultimate suite covering every dimension: destiny, name, wealth, relationship, and mobile audit.</p>
            <ul class="deliverables-list">
              <li>All 5 Flagship Advanced Reports (60 Total Pages)</li>
              <li>Lo Shu Elemental Grid Analysis Included</li>
              <li>Full 7-Layer Planetary Safe Remedies</li>
              <li>Priority PDF backend queue generation</li>
            </ul>
          </div>
          <div>
            <div class="card-price-display">
              <span class="price-amount">₹999</span>
              <span class="price-pages-tag"><del style="color:#7A654D;">₹2,550</del> · 60+ Pages</span>
            </div>
            <button class="btn-gold-primary" style="width:100%; box-sizing:border-box;" onclick="openOrderModal('bundle_comprehensive', 'Comprehensive Master Bundle (5 Reports)')">Order Master Bundle ✦</button>
          </div>
        </div>
      </div>
    </section>

    <!-- ── 5. CHARM AI & 1-ON-1 CONSULTATION ── -->
    <section class="pricing-comparison-box" style="margin-bottom:20px;">
      <h2 class="comparison-title">Interactive Charm AI &amp; Certified Practitioner Consultation</h2>
      <p class="comparison-sub">Complement your static PDF blueprints with conversational AI synthesis or a 45-minute live certified consultation.</p>

      <div class="bundles-grid">
        <div class="bundle-card">
          <div>
            <span class="report-category-pill" style="margin-bottom:12px; display:inline-block;">AI Intelligence</span>
            <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:0 0 8px; font-size:1.25rem;">Charm AI Access Packs</h3>
            <p style="font-size:0.88rem; color:var(--ink-muted); margin-bottom:16px;">Ask specific conversational questions about your charts, remedy timing, and compatibility matches.</p>
            <ul class="deliverables-list">
              <li>Free Tier: 3 daily foundational queries (₹0)</li>
              <li>Single Deep Query: 1 in-depth breakdown (₹199)</li>
              <li>Multi-Query Pack: 10 queries across 30 days (₹399)</li>
              <li>Extended Blueprint: 25 queries + exportable notes (₹699)</li>
            </ul>
          </div>
          <div>
            <div class="card-price-display">
              <span class="price-amount">₹199 – ₹699</span>
              <span class="price-pages-tag">Instant Access</span>
            </div>
            <a href="/#charm-ai" class="btn-gold-primary" style="width:100%; box-sizing:border-box;">Launch Charm AI ✦</a>
          </div>
        </div>

        <div class="bundle-card featured">
          <div>
            <span class="report-category-pill" style="margin-bottom:12px; display:inline-block; background:rgba(22,131,91,0.12); color:var(--emerald);">Human Expert</span>
            <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:0 0 8px; font-size:1.25rem;">1-on-1 Certified Video Consultation</h3>
            <p style="font-size:0.88rem; color:var(--ink-muted); margin-bottom:16px;">45-minute private confidential consultation with a senior Numeros Vision certified practitioner.</p>
            <ul class="deliverables-list">
              <li>Live verification of birth time and planetary charts</li>
              <li>Personalized answers to career, marriage, and family questions</li>
              <li>Custom safe gemstone and acoustic name rectification advice</li>
              <li>Full recording + post-call PDF summary included</li>
            </ul>
          </div>
          <div>
            <div class="card-price-display">
              <span class="price-amount">₹1,050</span>
              <span class="price-pages-tag">45 Minutes · Google Meet</span>
            </div>
            <a href="/consultation/" class="btn-gold-primary" style="width:100%; box-sizing:border-box;">Book 1-on-1 Session ✦</a>
          </div>
        </div>
      </div>
    </section>

  </main>

  <!-- ── 6. INTERACTIVE REPORT CUSTOMIZER & INSTANT PDF DELIVERY MODAL ── -->
  <div class="nv-modal-backdrop" id="orderModal" onclick="closeModalOnBackdrop(event)">
    <div class="nv-modal-window" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
      <button class="modal-close" onclick="closeOrderModal()" aria-label="Close dialog">&times;</button>
      <div style="text-align:center; margin-bottom:20px;">
        <span class="hero-eyebrow-chip" id="modalTierChip">ADVANCED TIER (12 PAGES)</span>
        <h3 id="modalTitle" style="font-family:'Cormorant Garamond',Georgia,serif; font-size:1.8rem; color:var(--gold-dark); margin:8px 0 4px; font-weight:700;">Configure Report</h3>
        <p style="font-size:0.88rem; color:var(--ink-muted); margin:0;" id="modalPriceLabel">Price: ₹510 · Instant Download PDF</p>
      </div>

      <form id="reportOrderForm" onsubmit="handleGeneratePdf(event)">
        <input type="hidden" id="selectedTopic" value="vedic_destiny" />
        <input type="hidden" id="selectedTier" value="advanced" />

        <div class="form-group">
          <label class="form-label" for="clientName">Full Legal Name (as on birth certificate)</label>
          <input type="text" id="clientName" class="form-input" required placeholder="e.g. Bhaskr Singh" value="Bhaskr Singh" />
        </div>

        <div class="form-group" style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
          <div>
            <label class="form-label" for="clientDob">Date of Birth</label>
            <input type="date" id="clientDob" class="form-input" required value="1992-07-15" />
          </div>
          <div>
            <label class="form-label" for="clientGender">Gender</label>
            <select id="clientGender" class="form-input">
              <option value="male" selected>Male</option>
              <option value="female">Female</option>
              <option value="other">Other</option>
            </select>
          </div>
        </div>

        <div class="form-group" style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
          <div>
            <label class="form-label" for="clientTime">Time of Birth (Optional)</label>
            <input type="time" id="clientTime" class="form-input" value="10:30" />
          </div>
          <div>
            <label class="form-label" for="clientCity">Place of Birth (City)</label>
            <input type="text" id="clientCity" class="form-input" placeholder="e.g. New Delhi, India" value="New Delhi, India" />
          </div>
        </div>

        <div class="form-group">
          <label class="form-label" for="clientEmail">Delivery Email Address</label>
          <input type="email" id="clientEmail" class="form-input" required placeholder="your.name@example.com" value="test@numerosvision.com" />
        </div>

        <!-- Real-time Deterministic Calculation Preview Box -->
        <div id="calcPreviewBox" style="background:#FFFFFF; border:1px solid var(--border-gold); border-radius:12px; padding:12px 14px; margin-bottom:18px; font-size:0.84rem;">
          <div style="font-weight:700; color:var(--gold-dark); margin-bottom:6px; display:flex; justify-content:space-between;">
            <span>✦ Deterministic Calculation Engine Status:</span>
            <span style="color:var(--emerald);">Validated</span>
          </div>
          <div id="calcPreviewText" style="color:var(--ink-muted);">
            Driver: <strong>6 (Venus)</strong> · Conductor: <strong>7 (Ketu)</strong> · Lo Shu Archetype: <strong>Water / Intellect</strong>
          </div>
        </div>

        <div style="display:flex; flex-direction:column; gap:10px;">
          <button type="submit" id="downloadPdfBtn" class="btn-gold-primary" style="width:100%; box-sizing:border-box;">
            Generate &amp; Download Verified PDF ✦
          </button>
          <p style="font-size:0.75rem; color:var(--ink-muted); text-align:center; margin:0;">
            100% deterministic arithmetic. No generative AI arithmetic hallucinations. DPDP 2023 compliant.
          </p>
        </div>
      </form>
    </div>
  </div>

  <!-- ── 7. CANONICAL MASTER FOOTER MATCHING WEBSITE & APP ── -->
  <footer class="nv-footer">
    <div class="nv-footer-container">
      <div class="nv-footer-grid">
        <!-- Brand Summary Column -->
        <div class="nv-footer-brand-sec">
          <a href="/" class="nv-brand-link" style="margin-bottom:12px;">
            <div class="nv-brand-seal" style="width:42px; height:42px;">
              <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
            </div>
            <div class="nv-brand-text">
              <span class="nv-brand-title" style="font-size:1.15rem;">NUMEROS VISION</span>
              <span class="nv-brand-tagline">ANVEIL EVERY CHARM</span>
            </div>
          </a>
          <p class="nv-footer-brand-desc" style="color:#7A654D; font-size:0.86rem; line-height:1.6; margin-top:8px;">
            India's foremost deterministic numerological intelligence platform, synthesizing classical Vedic Driver &amp; Conductor frameworks, acoustic Chaldean vibrations, and Lo Shu grids into verified dossiers.
          </p>
        </div>

        <!-- Calculators Column -->
        <div class="nv-footer-col">
          <h4 class="nv-footer-heading" style="font-family:'Cinzel',serif; color:#8B6914; font-size:0.92rem; margin-bottom:12px;">Calculators</h4>
          <ul class="nv-footer-links" style="list-style:none; padding:0; margin:0; line-height:2;">
            <li><a href="/tools/name-numerology" style="color:#523E28; text-decoration:none;">Name Analysis &amp; Balancing</a></li>
            <li><a href="/tools/mobile-numerology" style="color:#523E28; text-decoration:none;">Mobile Number Audit</a></li>
            <li><a href="/tools/kundali-milan" style="color:#523E28; text-decoration:none;">Kundali Milan &amp; Synastry</a></li>
            <li><a href="/tools/business-numerology" style="color:#523E28; text-decoration:none;">Business &amp; Brand Name</a></li>
            <li><a href="/tools/life-path-calculator" style="color:#523E28; text-decoration:none;">Life Path Calculator</a></li>
            <li><a href="/tools/lo-shu-grid" style="color:#523E28; text-decoration:none;">Lo Shu Magic Grid</a></li>
          </ul>
        </div>

        <!-- Reports & Knowledge Column -->
        <div class="nv-footer-col">
          <h4 class="nv-footer-heading" style="font-family:'Cinzel',serif; color:#8B6914; font-size:0.92rem; margin-bottom:12px;">Reports &amp; Knowledge</h4>
          <ul class="nv-footer-links" style="list-style:none; padding:0; margin:0; line-height:2;">
            <li><a href="/reports_catalogue/" style="color:#8B6914; font-weight:700; text-decoration:none;">Reports Catalogue</a></li>
            <li><a href="/pricing/" style="color:#523E28; text-decoration:none;">Plans &amp; Pricing</a></li>
            <li><a href="/#charm-ai" style="color:#523E28; text-decoration:none;">Charm AI Assistant</a></li>
            <li><a href="/consultation/" style="color:#523E28; text-decoration:none;">1-on-1 Consultation</a></li>
            <li><a href="/insights/" style="color:#523E28; text-decoration:none;">Numerology Insights Hub</a></li>
            <li><a href="/about/" style="color:#523E28; text-decoration:none;">About Numeros Vision</a></li>
          </ul>
        </div>

        <!-- Legal & Compliance Column -->
        <div class="nv-footer-col">
          <h4 class="nv-footer-heading" style="font-family:'Cinzel',serif; color:#8B6914; font-size:0.92rem; margin-bottom:12px;">Legal &amp; Trust</h4>
          <ul class="nv-footer-links" style="list-style:none; padding:0; margin:0; line-height:2;">
            <li><a href="/privacy/" style="color:#523E28; text-decoration:none;">Privacy Policy (DPDP 2023)</a></li>
            <li><a href="/terms/" style="color:#523E28; text-decoration:none;">Terms of Service</a></li>
            <li><a href="/refund/" style="color:#523E28; text-decoration:none;">Cancellation &amp; Refund Policy</a></li>
            <li><a href="/disclaimer/" style="color:#523E28; text-decoration:none;">Statutory Disclaimer</a></li>
            <li><a href="/accessibility/" style="color:#523E28; text-decoration:none;">Accessibility Statement</a></li>
            <li><a href="/contact/" style="color:#523E28; text-decoration:none;">Contact Grievance Officer</a></li>
          </ul>
        </div>
      </div>

      <div class="footer-bottom-legal" style="border-top:1px solid rgba(201,162,39,0.25); margin-top:36px; padding-top:20px; font-size:0.78rem; color:#7A654D; text-align:center; line-height:1.6;">
        <p style="margin:0 0 6px;">&copy; 2026 Numeros Vision. All rights reserved. ANVEIL EVERY CHARM &trade; is a registered trademark.</p>
        <p style="margin:0;">
          Statutory Notice: Numerological calculations are classical cultural, mathematical and reflective interpretive frameworks. Numeros Vision does not guarantee commercial outcomes or medical/legal certainties.
        </p>
      </div>
    </div>
  </footer>

  <!-- ── 8. MOBILE & ANDROID STICKY BOTTOM NAVIGATION ── -->
  <nav class="nv-sticky-bottom-nav" aria-label="Mobile Navigation">
    <a href="/" class="nv-bottom-item" title="Home">
      <span class="nv-bottom-icon">🏠</span>
      <span class="nv-bottom-label">Home</span>
    </a>
    <a href="/calculators/" class="nv-bottom-item" title="Calculators">
      <span class="nv-bottom-icon">🔢</span>
      <span class="nv-bottom-label">Calculators</span>
    </a>
    <a href="/reports_catalogue/" class="nv-bottom-item active" title="Reports">
      <span class="nv-bottom-icon">📜</span>
      <span class="nv-bottom-label">Reports</span>
    </a>
    <a href="/#charm-ai" class="nv-bottom-item" title="Charm AI">
      <span class="nv-bottom-icon">✨</span>
      <span class="nv-bottom-label">Charm AI</span>
    </a>
    <a href="/pricing/" class="nv-bottom-item" title="Pricing">
      <span class="nv-bottom-icon">🏷️</span>
      <span class="nv-bottom-label">Pricing</span>
    </a>
  </nav>

  <!-- ── 9. PLATFORM JAVASCRIPT & INTERACTION ENGINE ── -->
  <script src="/static/js/nv_profile_sync.js"></script>
  <script src="/static/js/nav.js?v=4.7.3"></script>
  <script src="/static/js/nv_tracking_config.js?v=4.8.0"></script>
  <script src="/static/js/nv_consent.js?v=4.8.0"></script>
  <script src="/static/js/funnel_journey.js?v=1.5.0"></script>

  <script>
    // ── Tier Configuration Data ──
    const tierConfig = {
      basic: { price: '₹199', pages: '3 Pages', delivSuffix: ' (3 Pages - Core Analysis)' },
      advanced: { price: '₹510', pages: '12 Pages', delivSuffix: ' (12 Pages - Full Dasha & Remedies)' },
      premium: { price: '₹1,050', pages: '32 Pages', delivSuffix: ' (32 Pages - Master Sovereign Dossier)' }
    };

    // Current selections map
    const activeSelections = {};

    function selectTier(btn, topic, tier) {
      const card = btn.closest('.report-card');
      card.querySelectorAll('.tier-btn').forEach(b => b.classList.remove('selected'));
      btn.classList.add('selected');

      activeSelections[topic] = tier;

      const priceEl = document.getElementById('price_' + topic);
      const pagesEl = document.getElementById('pages_' + topic);
      if (priceEl) priceEl.innerText = tierConfig[tier].price;
      if (pagesEl) pagesEl.innerText = tierConfig[tier].pages;
    }

    function filterReports(category, tabBtn) {
      document.querySelectorAll('.nv-cat-tab').forEach(t => t.classList.remove('active'));
      tabBtn.classList.add('active');

      const cards = document.querySelectorAll('.report-card');
      cards.forEach(card => {
        if (category === 'all' || card.getAttribute('data-category') === category) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    }

    function openOrderModal(topic, title) {
      const tier = activeSelections[topic] || 'advanced';
      document.getElementById('selectedTopic').value = topic;
      document.getElementById('selectedTier').value = tier;
      document.getElementById('modalTitle').innerText = title;
      document.getElementById('modalTierChip').innerText = `${tier.toUpperCase()} TIER (${tierConfig[tier].pages.toUpperCase()})`;
      document.getElementById('modalPriceLabel').innerText = `Price: ${tierConfig[tier].price} · Instant Download PDF`;

      updateCalculationPreview();
      document.getElementById('orderModal').classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeOrderModal() {
      document.getElementById('orderModal').classList.remove('open');
      document.body.style.overflow = '';
    }

    function closeModalOnBackdrop(e) {
      if (e.target.id === 'orderModal') closeOrderModal();
    }

    // Real-time calculation preview
    function updateCalculationPreview() {
      const name = document.getElementById('clientName').value || 'User';
      const dob = document.getElementById('clientDob').value;
      if (!dob) return;

      const parts = dob.split('-');
      if (parts.length === 3) {
        const day = parseInt(parts[2], 10);
        let driver = day % 9;
        if (driver === 0) driver = 9;

        let sum = 0;
        dob.replace(/-/g, '').split('').forEach(d => sum += parseInt(d, 10));
        let conductor = sum % 9;
        if (conductor === 0) conductor = 9;

        const previewText = document.getElementById('calcPreviewText');
        if (previewText) {
          previewText.innerHTML = `Driver: <strong>${driver}</strong> · Conductor: <strong>${conductor}</strong> · Name acoustic check: <strong>Aligned</strong>`;
        }
      }
    }

    document.getElementById('clientDob').addEventListener('change', updateCalculationPreview);
    document.getElementById('clientName').addEventListener('input', updateCalculationPreview);

    // PDF generation and instant download trigger
    async function handleGeneratePdf(e) {
      e.preventDefault();
      const btn = document.getElementById('downloadPdfBtn');
      const originalText = btn.innerHTML;
      btn.innerHTML = '⏳ Computing Mathematical Engine &amp; Generating PDF...';
      btn.disabled = true;

      const topic = document.getElementById('selectedTopic').value;
      const tier = document.getElementById('selectedTier').value;
      const name = document.getElementById('clientName').value;
      const dob = document.getElementById('clientDob').value;
      const gender = document.getElementById('clientGender').value;
      const city = document.getElementById('clientCity').value;
      const email = document.getElementById('clientEmail').value;

      try {
        const payload = {
          name: name,
          dob: dob,
          gender: gender,
          time_of_birth: document.getElementById('clientTime').value || null,
          city_of_birth: city,
          topic: topic,
          tier: tier,
          email: email
        };

        const res = await fetch('/api/v1/reports/generate-pdf', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        if (!res.ok) {
          throw new Error('PDF Generation returned HTTP ' + res.status);
        }

        const blob = await res.blob();
        const downloadUrl = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = downloadUrl;
        a.download = `NumerosVision_${topic}_${tier}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(downloadUrl);

        btn.innerHTML = '✅ PDF Download Complete!';
        setTimeout(() => {
          btn.innerHTML = originalText;
          btn.disabled = false;
          closeOrderModal();
        }, 2200);

      } catch (err) {
        console.error('PDF generation error:', err);
        btn.innerHTML = '⚠️ Generation Note: Downloading sample dossier...';
        setTimeout(() => {
          window.location.href = '/sample_roadmap/';
        }, 1200);
      }
    }
  </script>
</body>
</html>
"""

with open('app/static/reports_catalogue.html', 'w', encoding='utf-8') as f:
    f.write(catalogue_html)

print("Generated canonical master app/static/reports_catalogue.html (length:", len(catalogue_html), ")")
