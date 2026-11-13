"""
Build app/static/amp/index.html as AMP Mobile Hub
"""
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AMP_INDEX_PATH = os.path.join(ROOT_DIR, "app", "static", "amp", "index.html")

AMP_INDEX_HTML = """<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>Accelerated Mobile Numerology &amp; Insights Hub | Numeros Vision AMP</title>
  <link rel="canonical" href="https://numerosvision.com/insights/">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <meta name="description" content="Fast-loading AMP mobile guide to authentic Vedic, Chaldean, and Lo Shu numerology traditions. ANVEIL EVERY CHARM on mobile.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Cormorant+Garamond:wght@400;600;700&family=Inter:wght@400;500;600&display=swap">
  
  <style amp-boilerplate>body{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}@-webkit-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-moz-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-ms-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@-o-keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}@keyframes -amp-start{from{visibility:hidden}to{visibility:visible}}</style><noscript><style amp-boilerplate>body{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}</style></noscript>
  
  <style amp-custom>
    :root {
      --pearl: #FFFDF7;
      --pearl-warm: #F7F3EA;
      --white: #FFFFFF;
      --gold: #C9A227;
      --gold-dark: #8B6914;
      --gold-light: #E2B84B;
      --emerald: #16835B;
      --ink: #523E28;
      --ink-muted: #7A654D;
      --border: rgba(201, 162, 39, 0.28);
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--pearl);
      color: var(--ink);
      font-family: 'Inter', -apple-system, sans-serif;
      line-height: 1.6;
      font-size: 1.0rem;
    }
    a { color: var(--gold-dark); text-decoration: none; }
    a:hover { text-decoration: underline; }
    .amp-header {
      background: var(--pearl-warm);
      border-bottom: 1.5px solid var(--border);
      padding: 14px 20px;
      position: sticky;
      top: 0;
      z-index: 1000;
    }
    .amp-header-inner {
      max-width: 840px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .amp-brand-title {
      font-family: 'Cinzel', serif;
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: var(--gold-dark);
    }
    .amp-brand-tagline {
      font-size: 0.62rem;
      font-weight: 600;
      letter-spacing: 0.2em;
      color: var(--ink-muted);
      text-transform: uppercase;
      display: block;
    }
    .amp-cta-btn {
      background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dark) 100%);
      color: var(--pearl) !important;
      padding: 8px 16px;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-decoration: none !important;
    }
    .amp-hero {
      text-align: center;
      padding: 36px 20px 24px;
      max-width: 760px;
      margin: 0 auto;
    }
    .amp-eyebrow {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: var(--gold-dark);
      margin-bottom: 8px;
      display: inline-block;
    }
    .amp-h1 {
      font-family: 'Cormorant Garamond', serif;
      font-size: clamp(2.0rem, 5vw, 2.8rem);
      line-height: 1.2;
      color: var(--gold-dark);
      margin-bottom: 12px;
    }
    .amp-lead {
      color: var(--ink-muted);
      font-size: 0.98rem;
      line-height: 1.6;
    }
    .amp-grid {
      max-width: 800px;
      margin: 0 auto;
      padding: 10px 20px 50px;
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
    }
    @media (min-width: 600px) {
      .amp-grid { grid-template-columns: repeat(2, 1fr); }
    }
    .amp-card {
      background: var(--white);
      border: 1.5px solid var(--border);
      border-radius: 14px;
      padding: 20px;
      transition: transform 0.2s;
    }
    .amp-card-tag {
      font-size: 0.7rem;
      font-weight: 700;
      text-transform: uppercase;
      color: var(--emerald);
      margin-bottom: 6px;
      display: block;
    }
    .amp-card h2 {
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.35rem;
      color: var(--gold-dark);
      margin-bottom: 8px;
      line-height: 1.3;
    }
    .amp-card p {
      font-size: 0.88rem;
      color: var(--ink-muted);
      margin-bottom: 12px;
      line-height: 1.5;
    }
    .amp-footer {
      background: var(--pearl-warm);
      border-top: 1.5px solid var(--border);
      padding: 32px 20px;
      text-align: center;
      font-size: 0.85rem;
      color: var(--ink-muted);
    }
  </style>

  <!-- AMP Analytics --><script async custom-element="amp-analytics" src="https://cdn.ampproject.org/v0/amp-analytics-0.1.js"></script>
</head>
<body>
  <!-- Google Tag Manager -->
  <amp-analytics config="https://www.googletagmanager.com/amp.json?id=GTM-5N2QCMZS&gtm.url=SOURCE_URL" data-credentials="include"></amp-analytics>

  <header class="amp-header">
    <div class="amp-header-inner">
      <a href="/" title="Numeros Vision - Anveil Every Charm">
        <span class="amp-brand-title">NUMEROS VISION</span>
        <span class="amp-brand-tagline">ANVEIL EVERY CHARM</span>
      </a>
      <a href="/calculators/" class="amp-cta-btn">Calculators ✦</a>
    </div>
  </header>

  <div class="amp-hero">
    <span class="amp-eyebrow">⚡ FAST ACCELERATED MOBILE PAGES</span>
    <h1 class="amp-h1">Numerology Knowledge &amp; Articles Hub</h1>
    <p class="amp-lead">Read high-speed, mobile-optimized editorial insights on Life Path numbers, Lo Shu magic squares, Chaldean name vibrations, and planetary timing.</p>
  </div>

  <div class="amp-grid">
    <div class="amp-card">
      <span class="amp-card-tag">Foundations</span>
      <h2><a href="/amp/blog/what-is-numerology">What is Numerology? The Complete Beginner's Guide</a></h2>
      <p>How numerology works, the 9 core numbers, and how AI-powered calculations unlock personal trajectory.</p>
      <a href="/amp/blog/what-is-numerology">Read AMP Article →</a>
    </div>
    <div class="amp-card">
      <span class="amp-card-tag">Life Path</span>
      <h2><a href="/amp/blog/life-path-numbers-explained">Life Path Numbers 1 to 9 &amp; Master Numbers</a></h2>
      <p>Complete meanings, career archetypes, and relationship resonance for each life path frequency.</p>
      <a href="/amp/blog/life-path-numbers-explained">Read AMP Article →</a>
    </div>
    <div class="amp-card">
      <span class="amp-card-tag">Ancient Systems</span>
      <h2><a href="/amp/blog/chaldean-vs-pythagorean-numerology">Chaldean vs Pythagorean Numerology</a></h2>
      <p>Discover the critical mathematical differences between Western alphabet sums and Babylonian sound resonance.</p>
      <a href="/amp/blog/chaldean-vs-pythagorean-numerology">Read AMP Article →</a>
    </div>
    <div class="amp-card">
      <span class="amp-card-tag">Spatial &amp; Energy</span>
      <h2><a href="/amp/blog/lo-shu-grid-8-planes">Lo Shu Grid &amp; The 8 Cosmic Planes</a></h2>
      <p>How the 3×3 magic square reveals mental, emotional, practical, and financial energy lines.</p>
      <a href="/amp/blog/lo-shu-grid-8-planes">Read AMP Article →</a>
    </div>
    <div class="amp-card">
      <span class="amp-card-tag">Karmic Resonance</span>
      <h2><a href="/amp/blog/master-numbers-11-22-33">Master Numbers 11, 22, and 33 Explained</a></h2>
      <p>The spiritual potency, life challenges, and high missions of the three ancient Master Frequencies.</p>
      <a href="/amp/blog/master-numbers-11-22-33">Read AMP Article →</a>
    </div>
    <div class="amp-card">
      <span class="amp-card-tag">Modern Touchpoints</span>
      <h2><a href="/amp/blog/mobile-numerology-malefic-pairs">Mobile Number Numerology: Auspicious &amp; Enemy Pairs</a></h2>
      <p>How daily calling digits and adjacent frequency pairings impact business discussions and wealth flow.</p>
      <a href="/amp/blog/mobile-numerology-malefic-pairs">Read AMP Article →</a>
    </div>
  </div>

  <footer class="amp-footer">
    <p>© 2026 NUMEROS VISION. ANVEIL EVERY CHARM.</p>
    <p style="margin-top:8px;"><a href="/insights/">Switch to Full Interactive Knowledge Hub →</a></p>
  </footer>
</body>
</html>"""

with open(AMP_INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(AMP_INDEX_HTML)

print(f"Created AMP mobile hub at {AMP_INDEX_PATH}")
