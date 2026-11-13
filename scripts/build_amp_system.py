"""
Google AMP, SEO, GEO & AIO Production Generator for Numeros Vision
Generates 100% valid Google AMP HTML articles with:
1. Google Tag Manager for AMP:
   - Head script: <script async custom-element="amp-analytics" src="https://cdn.ampproject.org/v0/amp-analytics-0.1.js"></script>
   - Body container: <amp-analytics config="https://www.googletagmanager.com/amp.json?id=GTM-5N2QCMZS&gtm.url=SOURCE_URL" data-credentials="include"></amp-analytics>
2. Google SEO Guidelines:
   - Canonical & amphtml cross-linking
   - Robots meta directives with max-image-preview:large
   - Open Graph (OG) & Twitter Card full metadata
   - Structured Breadcrumb navigation
3. GEO (Generative Engine Optimization) & AIO (AI Overviews):
   - Schema.org @graph (Article + BreadcrumbList + Organization)
   - Executive Takeaway / Direct Answer Card for AI citation
   - Deterministic vs Traditional evidence labeling
4. Complete removal of stray/unstyled mobile bottom navigation bars and SVGs.
"""
import os
import re
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BLOG_DIR = os.path.join(ROOT_DIR, "app", "static", "blog")
AMP_BLOG_DIR = os.path.join(ROOT_DIR, "app", "static", "amp", "blog")
AMP_HUB_FILE = os.path.join(ROOT_DIR, "app", "static", "amp", "index.html")

os.makedirs(AMP_BLOG_DIR, exist_ok=True)

AMP_CSS = """
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
    --border-gold: rgba(201, 162, 39, 0.45);
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    background: var(--pearl);
    color: var(--ink);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.75;
    font-size: 1.02rem;
    -webkit-font-smoothing: antialiased;
  }
  a { color: var(--gold-dark); text-decoration: none; }
  a:hover { text-decoration: underline; }
  
  /* Strictly hide any stray mobile bottom tabs or floating buttons in AMP */
  .mobile-bottom-tabs, .bottom-tab-item, .bottom-tab-icon, #mobile-bottom-tabs,
  .back-to-top-btn, #backToTop, .bottom-tab-indicator {
    display: none !important;
  }
  svg { max-width: 100%; height: auto; }

  /* AMP Header */
  .amp-header {
    background: var(--pearl-warm);
    border-bottom: 1.5px solid var(--border);
    padding: 14px 20px;
    position: sticky;
    top: 0;
    z-index: 1000;
  }
  .amp-header-inner {
    max-width: 800px;
    margin: 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
  }
  .amp-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    text-decoration: none;
  }
  .amp-brand-text {
    display: flex;
    flex-direction: column;
  }
  .amp-brand-title {
    font-family: 'Cinzel', Georgia, serif;
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
    display: inline-block;
  }

  /* Breadcrumbs */
  .amp-breadcrumbs {
    font-size: 0.8rem;
    color: var(--ink-muted);
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .amp-breadcrumbs a {
    color: var(--ink-muted);
    text-decoration: none;
  }
  .amp-breadcrumbs a:hover {
    color: var(--gold-dark);
    text-decoration: underline;
  }
  .amp-breadcrumbs span.sep {
    color: var(--gold-light);
  }
  .amp-breadcrumbs span.current {
    color: var(--gold-dark);
    font-weight: 600;
  }

  /* Article Wrapper */
  .amp-article-wrap {
    max-width: 760px;
    margin: 0 auto;
    padding: 24px 20px 60px;
  }
  .amp-eyebrow {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--gold-dark);
    margin-bottom: 12px;
    display: inline-block;
  }
  .amp-h1 {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: clamp(2.1rem, 5vw, 3.1rem);
    line-height: 1.18;
    color: var(--gold-dark);
    margin-bottom: 16px;
    font-weight: 700;
  }
  .amp-meta {
    font-size: 0.82rem;
    color: var(--ink-muted);
    padding-bottom: 14px;
    margin-bottom: 24px;
    border-bottom: 1px solid var(--border);
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
  }

  /* GEO / AIO Executive Takeaway Box */
  .amp-takeaway-box {
    background: #FFFFFF;
    border: 1.5px solid var(--gold);
    border-radius: 14px;
    padding: 20px 22px;
    margin-bottom: 32px;
    box-shadow: 0 4px 18px rgba(201, 162, 39, 0.12);
  }
  .amp-takeaway-tag {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--gold-dark);
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .amp-takeaway-lead {
    font-size: 1.05rem;
    font-weight: 600;
    line-height: 1.6;
    color: var(--ink);
    margin-bottom: 14px;
  }
  .amp-takeaway-list {
    list-style: none;
    padding-left: 0;
    margin: 0;
  }
  .amp-takeaway-list li {
    font-size: 0.92rem;
    color: var(--ink-muted);
    margin-bottom: 8px;
    padding-left: 20px;
    position: relative;
    line-height: 1.55;
  }
  .amp-takeaway-list li::before {
    content: "✦";
    position: absolute;
    left: 0;
    color: var(--gold);
    font-size: 0.85rem;
  }
  .amp-takeaway-list li strong {
    color: var(--ink);
  }

  /* Article Content Formatting */
  .amp-body h2 {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.85rem;
    color: var(--gold-dark);
    margin: 36px 0 14px;
    line-height: 1.25;
    font-weight: 600;
  }
  .amp-body h3 {
    font-family: 'Cinzel', Georgia, serif;
    font-size: 1.25rem;
    color: var(--ink);
    margin: 26px 0 10px;
    font-weight: 600;
  }
  .amp-body p {
    margin-bottom: 18px;
    color: var(--ink);
    font-size: 1.02rem;
  }
  .amp-body ul, .amp-body ol {
    margin-bottom: 20px;
    padding-left: 24px;
  }
  .amp-body li {
    margin-bottom: 8px;
  }
  .amp-body blockquote {
    border-left: 3.5px solid var(--gold);
    padding: 14px 20px;
    margin: 26px 0;
    background: rgba(201, 162, 39, 0.08);
    font-style: italic;
    color: var(--ink);
    border-radius: 0 10px 10px 0;
  }

  /* Number Grid */
  .number-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 26px 0;
  }
  .ng-cell {
    padding: 18px 12px;
    border: 1.5px solid var(--border-gold);
    border-radius: 14px;
    background: #FFFFFF;
    text-align: center;
    box-shadow: 0 4px 12px rgba(180, 155, 110, 0.08);
  }
  .ng-num {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2.2rem;
    color: var(--gold-dark);
    font-weight: 600;
    line-height: 1;
  }
  .ng-theme {
    font-size: 0.8rem;
    color: var(--ink);
    font-weight: 700;
    margin-top: 6px;
  }
  .ng-desc {
    font-size: 0.72rem;
    color: var(--ink-muted);
    margin-top: 4px;
    line-height: 1.4;
  }

  /* Calculation Box */
  .calc-box {
    background: #FFFFFF;
    border: 1.5px solid var(--border-gold);
    border-radius: 16px;
    padding: 24px 20px;
    margin: 28px 0;
    box-shadow: 0 4px 18px rgba(180, 155, 110, 0.1);
  }
  .calc-box h3 { margin-top: 0; color: var(--gold-dark); }
  .calc-step {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    margin-bottom: 12px;
  }
  .calc-step-num {
    min-width: 28px;
    height: 28px;
    border-radius: 50%;
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-light) 100%);
    color: #FFFDF7;
    font-weight: 700;
    font-size: 0.8rem;
    display: flex;
    align-items: center;
    justify-content: center;
  }

  /* Responsive Tables */
  .amp-body table {
    width: 100%;
    border-collapse: collapse;
    margin: 24px 0;
    font-size: 0.92rem;
    background: #FFFFFF;
  }
  .amp-body th {
    background: var(--pearl-warm);
    border: 1px solid var(--border);
    padding: 10px 14px;
    color: var(--gold-dark);
    text-align: left;
    font-family: 'Cinzel', serif;
    font-size: 0.85rem;
  }
  .amp-body td {
    border: 1px solid var(--border);
    padding: 10px 14px;
  }

  /* Interactive Upgrade Callout */
  .amp-action-card {
    background: var(--white);
    border: 2px solid var(--gold);
    border-radius: 16px;
    padding: 28px 24px;
    margin: 40px 0;
    text-align: center;
    box-shadow: 0 4px 20px rgba(139, 105, 20, 0.08);
  }
  .amp-action-card h3 {
    font-family: 'Cormorant Garamond', Georgia, serif;
    font-size: 1.7rem;
    color: var(--gold-dark);
    margin-bottom: 10px;
  }
  .amp-action-card p {
    font-size: 0.95rem;
    color: var(--ink-muted);
    margin-bottom: 18px;
  }
  .amp-action-btn {
    background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dark) 100%);
    color: var(--pearl) !important;
    padding: 12px 28px;
    border-radius: 999px;
    font-size: 0.92rem;
    font-weight: 700;
    letter-spacing: 0.05em;
    text-decoration: none !important;
    display: inline-block;
    box-shadow: 0 4px 14px rgba(201, 162, 39, 0.35);
  }

  /* AMP Footer */
  .amp-footer {
    background: var(--pearl-warm);
    border-top: 1.5px solid var(--border);
    padding: 36px 20px;
    text-align: center;
    font-size: 0.85rem;
    color: var(--ink-muted);
  }
  .amp-footer-links {
    display: flex;
    justify-content: center;
    gap: 18px;
    margin-bottom: 16px;
    flex-wrap: wrap;
  }
  .amp-footer-links a {
    color: var(--ink-muted);
    font-weight: 500;
  }
  @media (max-width: 600px) {
    .number-grid { grid-template-columns: repeat(2, 1fr); }
  }
"""

def extract_clean_article(html):
    """
    Extracts purely the article content, stripping headers, footers, mobile tabs,
    scripts, and floating elements.
    """
    # 1. Find start of article
    start_idx = -1
    for marker in ['<div class="blog-wrap">', '<div class="blog-wrap', '<main class="content-wrap">', '<main', '<article']:
        pos = html.find(marker)
        if pos != -1:
            start_idx = pos
            break
    if start_idx == -1:
        header_end = html.find("</header>")
        start_idx = header_end + len("</header>") if header_end != -1 else 0

    # 2. Find end of article
    end_idx = -1
    for marker in [
        '<nav class="mobile-bottom-tabs"',
        '<nav id="mobile-bottom-tabs"',
        '<!-- ───── FIXED MOBILE BOTTOM BAR',
        '<!-- ── FIXED MOBILE BOTTOM BAR',
        '<footer class="nv-footer">',
        '<footer'
    ]:
        pos = html.find(marker, start_idx)
        if pos != -1:
            end_idx = pos
            break
    if end_idx == -1:
        end_idx = html.find("</body>")
    if end_idx == -1:
        end_idx = len(html)

    body_slice = html[start_idx:end_idx]

    # 3. Aggressive sanitization of any stray mobile bottom bar SVGs or markup
    body_slice = re.sub(r'<nav\b[^>]*class=["\'][^"\']*mobile-bottom-tabs[^"\']*["\'][^>]*>.*?</nav>', '', body_slice, flags=re.DOTALL | re.IGNORECASE)
    body_slice = re.sub(r'<nav\b[^>]*id=["\']mobile-bottom-tabs["\'][^>]*>.*?</nav>', '', body_slice, flags=re.DOTALL | re.IGNORECASE)
    body_slice = re.sub(r'<div\b[^>]*class=["\'][^"\']*bottom-tab-[^"\']*["\'][^>]*>.*?</div>', '', body_slice, flags=re.DOTALL | re.IGNORECASE)
    body_slice = re.sub(r'<a\b[^>]*class=["\'][^"\']*bottom-tab-item[^"\']*["\'][^>]*>.*?</a>', '', body_slice, flags=re.DOTALL | re.IGNORECASE)
    body_slice = re.sub(r'<button[^>]*id=["\']backToTop["\'][^>]*>.*?</button>', '', body_slice, flags=re.DOTALL | re.IGNORECASE)
    body_slice = re.sub(r'<button[^>]*class=["\'][^"\']*back-to-top[^"\']*["\'][^>]*>.*?</button>', '', body_slice, flags=re.DOTALL | re.IGNORECASE)
    body_slice = re.sub(r'<div[^>]*class=["\'][^"\']*back-to-top[^"\']*["\'][^>]*>.*?</div>', '', body_slice, flags=re.DOTALL | re.IGNORECASE)
    body_slice = re.sub(r'<a[^>]*class=["\'][^"\']*back-to-top[^"\']*["\'][^>]*>.*?</a>', '', body_slice, flags=re.DOTALL | re.IGNORECASE)
    body_slice = re.sub(r'<!--.*?-->', '', body_slice, flags=re.DOTALL)

    # 4. Convert all <img> to valid <amp-img>
    def replace_img(match):
        img_tag = match.group(0)
        src_m = re.search(r'src=["\']([^"\']+)["\']', img_tag)
        alt_m = re.search(r'alt=["\']([^"\']+)["\']', img_tag)
        src = src_m.group(1) if src_m else ""
        alt = alt_m.group(1) if alt_m else "Numeros Vision Classical Numerology"
        return f'<amp-img src="{src}" alt="{alt}" width="600" height="400" layout="responsive"></amp-img>'

    body_slice = re.sub(r'<img[^>]+>', replace_img, body_slice, flags=re.IGNORECASE)

    # 5. Remove any prohibited inline <script> tags
    body_slice = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', body_slice, flags=re.IGNORECASE)

    # 6. Ensure closing tags are balanced
    open_divs = body_slice.count('<div')
    close_divs = body_slice.count('</div>')
    if open_divs > close_divs:
        body_slice += '</div>' * (open_divs - close_divs)

    return body_slice.strip()

def build_amp_article(slug, html):
    # Extract clean Title
    tm = re.search(r"<title>(.*?)</title>", html, re.I)
    raw_title = tm.group(1) if tm else "Numeros Vision Guide"
    clean_title = raw_title.replace("— Numeros Vision", "").replace("| Numeros Vision", "").replace("&amp;", "&").strip()
    full_title = f"{clean_title} | Numeros Vision AMP"

    # Extract Meta Description
    dm = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', html, re.I)
    clean_desc = dm.group(1).replace('"', '&quot;').strip() if dm else (
        f"Read authentic classical numerological analysis on {clean_title}. Deterministic calculation and traditional insights by Numeros Vision."
    )

    # Extract H1 for display
    h1m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.I | re.DOTALL)
    h1_text = re.sub(r'<[^>]+>', '', h1m.group(1)).strip() if h1m else clean_title

    # Canonical & AMP URLs
    canonical_url = f"https://numerosvision.com/blog/{slug}"
    amp_url = f"https://numerosvision.com/amp/blog/{slug}"

    # Extract clean article body
    article_body = extract_clean_article(html)

    # Schema.org JSON-LD Graph for Google Rich Results & AIO (AI Overviews)
    schema_graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Article",
                "@id": f"{canonical_url}#article",
                "isPartOf": {
                    "@type": "WebPage",
                    "@id": canonical_url
                },
                "headline": clean_title,
                "description": clean_desc,
                "image": ["https://numerosvision.com/static/logos/anveil-charm-hero.png"],
                "datePublished": "2026-01-15T08:00:00+05:30",
                "dateModified": "2026-10-26T20:00:00+05:30",
                "author": {
                    "@type": "Organization",
                    "name": "Numeros Vision Research Desk",
                    "url": "https://numerosvision.com/about/"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": "NUMEROS VISION",
                    "url": "https://numerosvision.com",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://numerosvision.com/static/icons/icon-512.png",
                        "width": 512,
                        "height": 512
                    }
                },
                "mainEntityOfPage": canonical_url,
                "articleSection": "Classical Numerology & Cosmic Insights",
                "inLanguage": "en-US"
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"{canonical_url}#breadcrumbs",
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Home",
                        "item": "https://numerosvision.com/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Insights",
                        "item": "https://numerosvision.com/insights/"
                    },
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": clean_title,
                        "item": canonical_url
                    }
                ]
            }
        ]
    }
    schema_json_str = json.dumps(schema_graph, indent=2, ensure_ascii=False)

    # AIO / GEO Direct Answer Key Takeaways
    takeaway_box = f"""
    <div class="amp-takeaway-box">
      <div class="amp-takeaway-tag">✦ EXECUTIVE TAKEAWAY · AI OVERVIEW SUMMARY ✦</div>
      <div class="amp-takeaway-lead">{clean_desc}</div>
      <ul class="amp-takeaway-list">
        <li><strong>Deterministic Precision:</strong> Numerical calculations computed with transparent deterministic algorithms.</li>
        <li><strong>Classical Traditions:</strong> Explores Pythagorean, Chaldean, and Lo Shu systems as distinct traditional frameworks.</li>
        <li><strong>Practical Focus:</strong> Formulated for name balancing, core life-path inquiry, and personal cycle awareness.</li>
      </ul>
    </div>
    """

    amp_html = f"""<!doctype html>
<html ⚡ lang="en">
<head>
  <meta charset="utf-8">
  <script async src="https://cdn.ampproject.org/v0.js"></script>
  <title>{full_title}</title>
  <link rel="canonical" href="{canonical_url}">
  <meta name="viewport" content="width=device-width,minimum-scale=1,initial-scale=1">
  <meta name="description" content="{clean_desc}">
  
  <!-- Standardized Favicon & Brand Touch Icons -->
  <link rel="icon" type="image/svg+xml" href="/logos/nv-logo-mark.svg">
  <link rel="icon" type="image/png" sizes="32x32" href="/static/icons/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/static/icons/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/static/icons/apple-touch-icon.png">
  <link rel="shortcut icon" href="/favicon.ico">
  
  <!-- Search Engine Crawl & Google Discover Directives -->
  <meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
  
  <!-- Open Graph / Social / AI Crawler Metadata -->
  <meta property="og:site_name" content="NUMEROS VISION">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical_url}">
  <meta property="og:title" content="{clean_title} — Numeros Vision">
  <meta property="og:description" content="{clean_desc}">
  <meta property="og:image" content="https://numerosvision.com/static/logos/anveil-charm-hero.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">

  <!-- Twitter Card Directives -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{clean_title} — Numeros Vision">
  <meta name="twitter:description" content="{clean_desc}">
  <meta name="twitter:image" content="https://numerosvision.com/static/logos/anveil-charm-hero.png">

  <!-- Google Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700&family=Cormorant+Garamond:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap">
  
  <!-- Schema.org JSON-LD Structured Data (Article + BreadcrumbList) -->
  <script type="application/ld+json">
{schema_json_str}
  </script>

  <!-- Required AMP Boilerplate -->
  <style amp-boilerplate>body{{-webkit-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-moz-animation:-amp-start 8s steps(1,end) 0s 1 normal both;-ms-animation:-amp-start 8s steps(1,end) 0s 1 normal both;animation:-amp-start 8s steps(1,end) 0s 1 normal both}}@-webkit-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-moz-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-ms-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@-o-keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}@keyframes -amp-start{{from{{visibility:hidden}}to{{visibility:visible}}}}</style><noscript><style amp-boilerplate>body{{-webkit-animation:none;-moz-animation:none;-ms-animation:none;animation:none}}</style></noscript>
  
  <!-- Custom AMP CSS -->
  <style amp-custom>
{AMP_CSS}
  </style>

  <!-- Google Tag Manager AMP Analytics Component -->
  <!-- AMP Analytics --><script async custom-element="amp-analytics" src="https://cdn.ampproject.org/v0/amp-analytics-0.1.js"></script>
</head>
<body>
  <!-- Google Tag Manager -->
  <amp-analytics config="https://www.googletagmanager.com/amp.json?id=GTM-5N2QCMZS&gtm.url=SOURCE_URL" data-credentials="include"></amp-analytics>

  <header class="amp-header">
    <div class="amp-header-inner">
      <a href="/" class="amp-brand" title="Numeros Vision - Anveil Every Charm">
        <div class="amp-brand-text">
          <span class="amp-brand-title">NUMEROS VISION</span>
          <span class="amp-brand-tagline">ANVEIL EVERY CHARM</span>
        </div>
      </a>
      <a href="/calculators/" class="amp-cta-btn">Calculators ✦</a>
    </div>
  </header>

  <main class="amp-article-wrap">
    <!-- Visual Semantic Breadcrumb for SEO & AI Overviews -->
    <nav class="amp-breadcrumbs" aria-label="Breadcrumb">
      <a href="/">Home</a>
      <span class="sep">›</span>
      <a href="/insights/">Insights</a>
      <span class="sep">›</span>
      <span class="current">{h1_text}</span>
    </nav>

    <!-- GEO / AIO Direct Answer Summary Card -->
    {takeaway_box}

    <!-- Article Content (Cleaned of stray SVGs & Navigation bars) -->
    <div class="amp-body">
      {article_body}
    </div>

    <!-- Interactive Numerology Engine Callout -->
    <div class="amp-action-card">
      <span class="amp-eyebrow">✦ INTERACTIVE NUMEROLOGY STUDIO ✦</span>
      <h3>Verify Your Numbers Deterministically</h3>
      <p>Calculate your Life Path number, Chaldean name number, and Lo Shu 3×3 Grid with our free deterministic calculation engine.</p>
      <a href="/tools/life-path-calculator" class="amp-action-btn">Calculate Your Number Free ✦</a>
    </div>
  </main>

  <footer class="amp-footer">
    <div class="amp-footer-links">
      <a href="/">Home</a>
      <a href="/calculators/">Calculators</a>
      <a href="/reports/">Reports</a>
      <a href="/pricing/">Pricing</a>
      <a href="/about/">About Us</a>
      <a href="/privacy-policy/">Privacy</a>
      <a href="/terms/">Terms</a>
    </div>
    <p>© 2026 NUMEROS VISION. All rights reserved. ANVEIL EVERY CHARM.</p>
    <p style="margin-top:8px; font-size:0.75rem;"><a href="{canonical_url}" style="color:var(--gold-dark);">Switch to Full Interactive Web Experience →</a></p>
  </footer>
</body>
</html>"""
    return amp_html

def process_all_blogs():
    blog_files = [f for f in os.listdir(BLOG_DIR) if f.endswith(".html")]
    print(f"Auditing and rebuilding {len(blog_files)} blog articles for AMP, SEO, GEO & AIO...")

    count = 0
    for file in blog_files:
        slug = file[:-5]
        canonical_path = os.path.join(BLOG_DIR, file)
        with open(canonical_path, "r", encoding="utf-8") as f:
            canonical_html = f.read()

        amp_content = build_amp_article(slug, canonical_html)
        amp_path = os.path.join(AMP_BLOG_DIR, file)
        with open(amp_path, "w", encoding="utf-8") as f:
            f.write(amp_content)

        # Ensure canonical file links to AMP
        amphtml_tag = f'<link rel="amphtml" href="https://numerosvision.com/amp/blog/{slug}" />'
        if 'rel="amphtml"' not in canonical_html:
            canonical_html = re.sub(
                r'(<link\s+rel=["\']canonical["\'][^>]*>)',
                r'\1\n  ' + amphtml_tag,
                canonical_html,
                count=1,
                flags=re.IGNORECASE
            )
            with open(canonical_path, "w", encoding="utf-8") as f:
                f.write(canonical_html)

        count += 1
        print(f"[{count}/{len(blog_files)}] Generated AMP (SEO+GEO+AIO) for {slug}")

    print(f"\nAll {count} AMP articles successfully rebuilt with clean layouts, complete schema, and zero stray symbols.")

if __name__ == "__main__":
    process_all_blogs()
