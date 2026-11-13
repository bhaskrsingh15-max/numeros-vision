import os
import re
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
AMP_BLOG_DIR = os.path.join(ROOT_DIR, "app", "static", "amp", "blog")
AMP_INDEX = os.path.join(ROOT_DIR, "app", "static", "amp", "index.html")

files = sorted([f for f in os.listdir(AMP_BLOG_DIR) if f.endswith(".html")])

cards = []
for f in files:
    slug = f[:-5]
    with open(os.path.join(AMP_BLOG_DIR, f), "r", encoding="utf-8") as fh:
        html = fh.read()
    tm = re.search(r"<title>(.*?)</title>", html, re.I)
    raw_title = tm.group(1).replace(" | Numeros Vision AMP", "").strip() if tm else slug.replace("-", " ").title()
    
    dm = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
    desc = dm.group(1).strip() if dm else "Classical Numerological Insights and Deterministic Analysis by Numeros Vision."
    if len(desc) > 130:
        desc = desc[:127] + "..."
        
    tag = "Classical Guide"
    if "gemstone" in slug: tag = "Remedies & Gems"
    elif "chaldean" in slug: tag = "Chaldean Acoustic"
    elif "life-path" in slug: tag = "Life Path Matrix"
    elif "lo-shu" in slug: tag = "Lo Shu Energy"
    elif "mobile" in slug: tag = "Mobile Numerology"
    elif "master" in slug: tag = "Master Frequencies"
    elif "number-" in slug: tag = f"Core Root Number"

    cards.append(f"""    <div class="amp-card">
      <span class="amp-card-tag">{tag}</span>
      <h2><a href="/amp/blog/{slug}">{raw_title}</a></h2>
      <p>{desc}</p>
      <a href="/amp/blog/{slug}" class="amp-card-link">Read Accelerated Guide →</a>
    </div>""")

cards_html = "\n".join(cards)

hub_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>Accelerated Mobile Numerology &amp; Cosmic Insights Hub | Numeros Vision AMP</title>
  <link rel="canonical" href="https://numerosvision.com/insights/">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <meta name="description" content="Ultra-fast Google AMP library of authentic classical numerology: Chaldean acoustic resonance, Pythagorean harmony, Lo Shu 3×3 energy grids, and gemstone remedies.">
  
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">

  <!-- Open Graph -->
  <meta property="og:site_name" content="NUMEROS VISION">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://numerosvision.com/insights/">
  <meta property="og:title" content="Numerology Knowledge & Insights Hub — Numeros Vision">
  <meta property="og:description" content="Ultra-fast Google AMP library of authentic classical numerology: Chaldean vibrations, Lo Shu grids, and gemstone balancing.">
  <meta property="og:image" content="https://numerosvision.com/static/logos/anveil-charm-hero.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Numerology Knowledge & Insights Hub — Numeros Vision">
  <meta name="twitter:description" content="Ultra-fast Google AMP library of authentic classical numerology: Chaldean vibrations, Lo Shu grids, and gemstone balancing.">
  <meta name="twitter:image" content="https://numerosvision.com/static/logos/anveil-charm-hero.png">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Cormorant+Garamond:wght@400;600;700&family=Inter:wght@400;500;600&display=swap">
  
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "CollectionPage",
        "@id": "https://numerosvision.com/insights/#webpage",
        "url": "https://numerosvision.com/insights/",
        "name": "Accelerated Mobile Numerology & Insights Hub",
        "description": "Ultra-fast Google AMP library of authentic classical numerology.",
        "publisher": {{
          "@type": "Organization",
          "name": "NUMEROS VISION",
          "url": "https://numerosvision.com",
          "logo": {{
            "@type": "ImageObject",
            "url": "https://numerosvision.com/static/icons/icon-512.png"
          }}
        }}
      }},
      {{
        "@type": "BreadcrumbList",
        "@id": "https://numerosvision.com/insights/#breadcrumbs",
        "itemListElement": [
          {{
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://numerosvision.com/"
          }},
          {{
            "@type": "ListItem",
            "position": 2,
            "name": "Insights Hub",
            "item": "https://numerosvision.com/insights/"
          }}
        ]
      }}
    ]
  }}
  </script>

  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  
  <style amp-custom>
    :root {{
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
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      background: var(--pearl);
      color: var(--ink);
      font-family: 'Inter', -apple-system, sans-serif;
      line-height: 1.6;
      font-size: 1.0rem;
    }}
    a {{ color: var(--gold-dark); text-decoration: none; }}
    a:hover {{ text-decoration: underline; }}
    
    .amp-header {{
      background: var(--pearl-warm);
      border-bottom: 1.5px solid var(--border);
      padding: 14px 20px;
      position: sticky;
      top: 0;
      z-index: 1000;
    }}
    .amp-header-inner {{
      max-width: 840px;
      margin: 0 auto;
      display: flex;
      align-items: center;
      justify-content: space-between;
    }}
    .amp-brand-title {{
      font-family: 'Cinzel', serif;
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      color: var(--gold-dark);
    }}
    .amp-brand-tagline {{
      font-size: 0.62rem;
      font-weight: 600;
      letter-spacing: 0.2em;
      color: var(--ink-muted);
      text-transform: uppercase;
      display: block;
    }}
    .amp-cta-btn {{
      background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dark) 100%);
      color: var(--pearl) !important;
      padding: 8px 16px;
      border-radius: 999px;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-decoration: none !important;
    }}
    .amp-hero {{
      text-align: center;
      padding: 40px 20px 28px;
      max-width: 760px;
      margin: 0 auto;
    }}
    .amp-eyebrow {{
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.15em;
      color: var(--gold-dark);
      margin-bottom: 8px;
      display: inline-block;
    }}
    .amp-h1 {{
      font-family: 'Cormorant Garamond', serif;
      font-size: clamp(2.0rem, 5vw, 2.9rem);
      line-height: 1.2;
      color: var(--gold-dark);
      margin-bottom: 12px;
    }}
    .amp-lead {{
      color: var(--ink-muted);
      font-size: 0.98rem;
      line-height: 1.6;
    }}
    .amp-grid {{
      max-width: 840px;
      margin: 0 auto;
      padding: 10px 20px 50px;
      display: grid;
      grid-template-columns: 1fr;
      gap: 16px;
    }}
    @media (min-width: 600px) {{
      .amp-grid {{ grid-template-columns: repeat(2, 1fr); }}
    }}
    .amp-card {{
      background: var(--white);
      border: 1.5px solid var(--border);
      border-radius: 14px;
      padding: 22px 18px;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      box-shadow: 0 4px 14px rgba(180, 155, 110, 0.07);
    }}
    .amp-card-tag {{
      font-size: 0.68rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.12em;
      color: var(--gold-dark);
      margin-bottom: 8px;
      display: inline-block;
    }}
    .amp-card h2 {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.35rem;
      line-height: 1.25;
      margin-bottom: 8px;
    }}
    .amp-card h2 a {{
      color: var(--ink);
    }}
    .amp-card p {{
      color: var(--ink-muted);
      font-size: 0.88rem;
      line-height: 1.5;
      margin-bottom: 14px;
      flex-grow: 1;
    }}
    .amp-card-link {{
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--gold-dark);
      display: inline-flex;
      align-items: center;
    }}
    .amp-footer {{
      background: var(--pearl-warm);
      border-top: 1.5px solid var(--border);
      padding: 30px 20px;
      text-align: center;
      font-size: 0.85rem;
      color: var(--ink-muted);
    }}
  </style>

  <!-- Google Tag Manager AMP Analytics Component -->
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
    <span class="amp-eyebrow">✦ ACCELERATED MOBILE KNOWLEDGE ✦</span>
    <h1 class="amp-h1">Classical Numerology Library</h1>
    <p class="amp-lead">Fast, stripped-down mobile guides to Babylonian Chaldean acoustic resonance, Lo Shu 3×3 energy planes, Master Numbers, and gemstone balancing.</p>
  </div>

  <div class="amp-grid">
{cards_html}
  </div>

  <footer class="amp-footer">
    <p>© 2026 NUMEROS VISION. ANVEIL EVERY CHARM.</p>
    <p style="margin-top:8px;"><a href="/insights/">Switch to Full Interactive Knowledge Hub →</a></p>
  </footer>
</body>
</html>
"""

with open(AMP_INDEX, "w", encoding="utf-8") as f:
    f.write(hub_html)

print(f"Successfully generated AMP Index Hub at {AMP_INDEX} with {len(cards)} guides!")
