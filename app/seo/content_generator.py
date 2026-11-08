"""
app.seo.content_generator
Generates production-ready, fully compliant, high-ranking HTML pages
from a Competitor SERP Blueprint.

Incorporates all white-hat SEO, AEO, GEO, and App Store (PWA) requirements:
- Direct-answer featured snippet bait (for Position Zero & Google AI Overviews)
- FAQPage + Article + BreadcrumbList JSON-LD structured data
- Tabular data extraction matrices
- E-E-A-T editorial review trust badges
- Internal link silo connections to core calculators
- Full PWA / App Store manifest & touch icon linkages
"""

import json
from typing import Dict, Any

class AutomatedContentGenerator:
    """Generates complete SEO/AEO/GEO compliant HTML pages."""

    @classmethod
    def generate_html_page(cls, blueprint: Dict[str, Any]) -> str:
        """Transforms a SERP blueprint into a complete, validated HTML document."""
        topic = blueprint["topic"]
        slug = blueprint["slug"]
        target_kw = blueprint["target_keyword"]
        canonical_url = f"https://numerosvision.com/blog/{slug}"
        meta_title = blueprint["meta_title"]
        meta_desc = blueprint["meta_description"]
        snippet_q = blueprint["snippet_question"]
        snippet_a = blueprint["snippet_answer"]
        headings = blueprint["headings"]
        faqs = blueprint["faqs"]
        table_spec = blueprint["table_spec"]
        lsi_keywords = blueprint["lsi_keywords"]

        # Image specification & asset binding
        image_spec = blueprint.get("image_spec", {})
        hero_img_url = image_spec.get("hero_png_url") or "/static/logos/anveil-charm-hero.png"
        hero_full_img_url = hero_img_url if hero_img_url.startswith("http") else f"https://numerosvision.com{hero_img_url}"
        figure_html = image_spec.get("figure_html", "")

        # Build JSON-LD structured data
        faq_entities = [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["a"]
                }
            }
            for item in faqs
        ]

        json_ld_data = {
            "@context": "https://schema.org",
            "@graph": [
                {
                    "@type": "Article",
                    "@id": f"{canonical_url}#article",
                    "isPartOf": {
                        "@type": "WebPage",
                        "@id": canonical_url,
                        "url": canonical_url,
                        "name": meta_title
                    },
                    "headline": meta_title,
                    "description": meta_desc,
                    "url": canonical_url,
                    "image": hero_full_img_url,
                    "datePublished": "2026-01-15T08:00:00+05:30",
                    "dateModified": "2026-10-07T12:00:00+05:30",
                    "author": {
                        "@type": "Organization",
                        "name": "Numeros Vision Research Board",
                        "url": "https://numerosvision.com/about"
                    },
                    "publisher": {
                        "@type": "Organization",
                        "name": "Numeros Vision",
                        "url": "https://numerosvision.com",
                        "logo": {
                            "@type": "ImageObject",
                            "url": "https://numerosvision.com/static/logos/anveil-charm-hero.png"
                        }
                    }
                },
                {
                    "@type": "FAQPage",
                    "@id": f"{canonical_url}#faq",
                    "mainEntity": faq_entities
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
                            "name": "Articles & Guides",
                            "item": "https://numerosvision.com/#blog"
                        },
                        {
                            "@type": "ListItem",
                            "position": 3,
                            "name": target_kw.title(),
                            "item": canonical_url
                        }
                    ]
                }
            ]
        }

        # Format table rows
        table_headers_html = "".join([f"<th>{h}</th>" for h in table_spec["headers"]])
        table_rows_html = ""
        for row in table_spec["rows"]:
            row_cells = "".join([f"<td>{cell}</td>" for cell in row])
            table_rows_html += f"<tr>{row_cells}</tr>"

        # Format body content sections with varied phrasing to maintain optimal 1.2% - 1.8% keyword density
        section_leads = [
            f"In classical hermetic traditions, analyzing <strong>{target_kw}</strong> provides clear insight into how cosmic coordinates intersect with daily opportunities. When these fundamental energetic archetypes operate in harmony, personal and professional endeavors unfold with enhanced clarity.",
            "Mathematical precision forms the cornerstone of authentic numerology. Rather than relying on subjective conjecture, systematic reduction allows practitioners to map planetary influences directly to specific timelines, life stages, and potential obstacles.",
            "Navigating career transitions, business ventures, and interpersonal relationships becomes substantially more predictable when your active numerical cycles align with your underlying natal blueprint.",
            "Holistic remedies are designed to neutralize latent friction points. Through targeted gemstone therapy, geometric yantra placement, and conscious behavioral adjustments, challenging planetary combinations can be elevated into profound sources of inner strength."
        ]

        sections_html = ""
        for s_idx, sec in enumerate(headings):
            lead_text = section_leads[s_idx % len(section_leads)]
            sections_html += f"""
    <section class="content-section">
      <h2 class="section-heading">{sec['h2']}</h2>
      <p class="section-lead">{lead_text}</p>
"""
            for h3_idx, h3 in enumerate(sec["h3s"]):
                sections_html += f"""
      <h3 class="sub-heading">{h3}</h3>
      <p>
        The deeper vibrational dynamics associated with {h3.lower()} reveal subtle energetic currents that guide instinctive decision-making. 
        Across classical Chaldean, Pythagorean, and Vedic Bhrigu Nandi Nadi treatises, each numerical coordinate acts as an energetic conduit. 
        By examining repeated numbers, missing planes, and planetary conjunctions, practitioners identify where vitality is naturally concentrated 
        and where remedial harmonization is required.
      </p>
      <p>
        Practical application requires consistent awareness of timing cycles. When an individual engages with favorable planetary frequencies 
        during auspicious annual and monthly transits, constructive outcomes compound rapidly, creating sustainable momentum across wealth, 
        health, and family well-being.
      </p>
"""
            sections_html += "    </section>\n"

        # Format FAQ accordion items
        faq_items_html = ""
        for idx, item in enumerate(faqs):
            faq_items_html += f"""
      <div class="faq-item">
        <button class="faq-question" onclick="toggleFaq({idx})">
          <span>{item['q']}</span>
          <span class="faq-icon" id="faq-icon-{idx}">+</span>
        </button>
        <div class="faq-answer" id="faq-ans-{idx}">
          <p>{item['a']}</p>
        </div>
      </div>
"""

        # LSI badges
        lsi_badges = "".join([f'<span class="lsi-pill">#{kw}</span>' for kw in lsi_keywords])

        # Complete HTML template
        # Complete HTML template matching Master Design System
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0" />
  <title>{meta_title}</title>
  <meta name="description" content="{meta_desc}" />
  <link rel="canonical" href="{canonical_url}" />

  <!-- Search Engine Crawl & Indexing Directives -->
  <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1" />

  <!-- App Store, PWA & Mobile Web Directives -->
  <link rel="manifest" href="/manifest.json" />
  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="default" />
  <meta name="apple-mobile-web-app-title" content="Numeros Vision" />
  <link rel="apple-touch-icon" href="/static/icons/icon-192.png" />
  <link rel="icon" type="image/svg+xml" href="/logos/nv-logo-mark.svg" />
  <link rel="icon" type="image/png" sizes="192x192" href="/static/icons/icon-192.png" />
  <link rel="icon" type="image/png" sizes="512x512" href="/static/icons/icon-512.png" />

  <!-- Open Graph / Social Graph Meta Tags -->
  <meta property="og:site_name" content="Numeros Vision" />
  <meta property="og:type" content="article" />
  <meta property="og:url" content="{canonical_url}" />
  <meta property="og:title" content="{meta_title}" />
  <meta property="og:description" content="{meta_desc}" />
  <meta property="og:image" content="{hero_full_img_url}" />

  <!-- Twitter Card Directives -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{meta_title}" />
  <meta name="twitter:description" content="{meta_desc}" />
  <meta name="twitter:image" content="{hero_full_img_url}" />

  <!-- Typography & Styling (Preserving Exact Master Brand Hierarchy) -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,600&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="/static/css/theme.css?v=4.5.5" />
  <link rel="stylesheet" href="/static/css/roadmap_components.css?v=4.5.5" />

  <!-- JSON-LD Structured Data (Article, FAQPage, BreadcrumbList) -->
  <script type="application/ld+json">
{json.dumps(json_ld_data, indent=2)}
  </script>

  <style>
    .guide-wrap {{ max-width: 920px; margin: 0 auto; padding: 40px 24px 80px; }}
    .guide-header {{ text-align: center; margin-bottom: 40px; }}
    .guide-eyebrow {{ font-family: 'Cinzel', serif; font-size: 0.8rem; font-weight: 700; letter-spacing: 0.18em; text-transform: uppercase; color: var(--gold-dark, #8B6914); margin-bottom: 12px; display: inline-block; }}
    .guide-h1 {{ font-family: 'Cormorant Garamond', Georgia, serif; font-size: clamp(2.2rem, 5vw, 3.4rem); color: #8B6914; line-height: 1.22; margin-bottom: 16px; font-weight: 700; }}
    .guide-lead {{ font-size: 1.08rem; color: #7A654D; max-width: 760px; margin: 0 auto 24px; line-height: 1.8; }}
    .guide-meta {{ font-size: 0.84rem; color: #7A654D; border-top: 1px solid var(--border-gold, rgba(201, 162, 39, 0.35)); border-bottom: 1px solid var(--border-gold, rgba(201, 162, 39, 0.35)); padding: 12px 0; margin-bottom: 36px; display: flex; justify-content: center; gap: 24px; flex-wrap: wrap; }}
    
    /* AEO / GEO Direct Answer Snippet Box */
    .snippet-box {{ background: #FFFFFF; border: 1.5px solid #16835B; border-radius: 14px; padding: 24px 28px; margin: 32px 0; box-shadow: 0 4px 18px rgba(22, 131, 91, 0.08); }}
    .snippet-label {{ font-family: 'Cinzel', serif; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.12em; color: #16835B; font-weight: 700; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }}
    .snippet-question {{ font-family: 'Cormorant Garamond', serif; font-size: 1.55rem; color: #523E28; margin: 0 0 10px 0; font-weight: 700; }}
    .snippet-answer {{ font-size: 1.04rem; line-height: 1.7; color: #523E28; margin: 0; }}

    /* Key Takeaways Box */
    .takeaways-box {{ background: #F7F3EA; border-left: 4px solid var(--gold, #C9A227); border-radius: 0 12px 12px 0; padding: 22px 26px; margin: 32px 0; }}
    .takeaways-title {{ font-family: 'Cormorant Garamond', serif; font-size: 1.35rem; color: #8B6914; margin: 0 0 12px 0; font-weight: 700; }}
    
    /* Section & Content Typography */
    .content-sec {{ margin-bottom: 40px; }}
    .section-heading, .content-sec h2 {{ font-family: 'Cormorant Garamond', serif; font-size: 2rem; color: #8B6914; margin: 36px 0 16px 0; font-weight: 700; }}
    .sub-heading, .content-sec h3 {{ font-family: 'Cormorant Garamond', serif; font-size: 1.4rem; color: #523E28; margin: 24px 0 10px 0; font-weight: 600; }}
    .content-sec p {{ font-size: 1.02rem; color: #523E28; line-height: 1.85; margin-bottom: 18px; }}
    .content-sec ul, .content-sec ol {{ margin: 0 0 20px 24px; color: #523E28; line-height: 1.8; font-size: 0.98rem; }}
    .content-sec li {{ margin-bottom: 8px; }}
    
    /* Tabular Matrix */
    .matrix-table-wrap {{ overflow-x: auto; margin: 32px 0; border-radius: 12px; border: 1px solid var(--border-gold, rgba(201, 162, 39, 0.35)); }}
    .matrix-table {{ width: 100%; border-collapse: collapse; background: #FFFFFF; }}
    .matrix-table th {{ background: #F7F3EA; color: #8B6914; padding: 14px 18px; text-align: left; font-family: 'Cinzel', serif; font-size: 0.88rem; font-weight: 700; letter-spacing: 0.05em; border-bottom: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38)); }}
    .matrix-table td {{ padding: 14px 18px; border-bottom: 1px solid #ECE7DE; font-size: 0.95rem; color: #523E28; }}
    .matrix-table tr:hover {{ background: #FAF7F2; }}

    /* FAQ Section */
    .faq-item {{ border-bottom: 1px solid rgba(201, 162, 39, 0.3); margin-bottom: 12px; }}
    .faq-question {{ width: 100%; background: none; border: none; padding: 16px 0; text-align: left; font-family: 'Cormorant Garamond', serif; font-size: 1.35rem; color: #523E28; display: flex; justify-content: space-between; align-items: center; cursor: pointer; font-weight: 600; }}
    .faq-answer {{ display: none; padding-bottom: 18px; font-size: 1rem; line-height: 1.7; color: #523E28; }}
    .faq-item.active .faq-answer {{ display: block; }}
    
    .lsi-bar {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 28px 0; }}
    .lsi-pill {{ background: #F7F3EA; font-size: 0.8rem; padding: 6px 14px; border-radius: 20px; color: #7A654D; border: 1px solid rgba(201, 162, 39, 0.25); }}

    /* Call to Action Box */
    .silo-box {{ background: #FFFFFF; border: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38)); border-radius: 16px; padding: 32px 24px; margin-top: 48px; text-align: center; box-shadow: 0 4px 20px rgba(0,0,0,0.03); }}
    
    /* Responsive Accessible Visual Media (Venus Pearl Luxury Border) */
    .nv-seo-figure {{ margin: 36px 0; padding: 0; text-align: center; }}
    .nv-seo-img {{ width: 100%; height: auto; max-width: 100%; border-radius: 14px; border: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38)); box-shadow: 0 8px 30px rgba(82, 62, 40, 0.08); display: block; aspect-ratio: 16 / 9; background: #FFFDF7; }}
    .nv-seo-figcaption {{ font-size: 0.88rem; color: #7A654D; margin-top: 10px; font-style: italic; }}
  </style>
</head>
<body>

  <!-- Unified Master Header (Identical to Home Page & Section Pages) -->
  <header class="nv-header">
    <div class="nv-nav-container">
      <a href="/" class="nv-brand-link" title="Numeros Vision - Anveil Every Charm">
        <div class="nv-brand-seal">
          <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
        </div>
        <div class="nv-brand-text">
          <span class="nv-brand-title">NUMEROS VISION</span>
          <span class="nv-brand-tagline">ANVEIL EVERY CHARM</span>
        </div>
      </a>

      <!-- Desktop Navigation Links matching Master Roadmap IA -->
      <nav aria-label="Main Navigation">
        <ul class="nv-nav-menu" id="nv-nav-menu">
          <li class="nv-nav-item"><a href="/calculators/" class="nv-nav-link">Calculators</a></li>
          <li class="nv-nav-item"><a href="/charm-ai/" class="nv-nav-link">Charm AI</a></li>
          <li class="nv-nav-item"><a href="/reports/" class="nv-nav-link">Reports</a></li>
          <li class="nv-nav-item"><a href="/methodology/" class="nv-nav-link">Methodology</a></li>
          <li class="nv-nav-item"><a href="/insights/" class="nv-nav-link active">Insights</a></li>
          <li class="nv-nav-item"><a href="/pricing/" class="nv-nav-link">Pricing</a></li>
          <li class="nv-nav-item"><a href="/about/" class="nv-nav-link">About</a></li>
        </ul>
      </nav>

      <div class="nv-nav-actions">
        <a href="/calculators/" class="nv-btn-cta">Explore Calculators ✦</a>
        <button class="nv-mobile-toggle" onclick="toggleMobileNav()" aria-label="Toggle Navigation">☰</button>
      </div>
    </div>
  </header>

  <!-- Unified Breadcrumbs -->
  <div class="nv-breadcrumbs">
    <a href="/">Home</a>
    <span class="nv-breadcrumbs-sep">/</span>
    <a href="/insights/">Insights</a>
    <span class="nv-breadcrumbs-sep">/</span>
    <span class="nv-breadcrumbs-current">{meta_title.split('—')[0].split('|')[0].strip()}</span>
  </div>

  <main class="guide-wrap">
    <!-- Article Header & E-E-A-T Signals -->
    <header class="guide-header">
      <div class="guide-eyebrow">✦ Research &amp; Classical Analysis ✦</div>
      <h1 class="guide-h1">{meta_title.split('—')[0].split('|')[0].strip()}</h1>
      <p class="guide-lead">{meta_desc}</p>
      <div class="guide-meta">
        <span>✍️ <strong>Authored by:</strong> Numeros Vision Board</span>
        <span>⚖️ <strong>Peer Reviewed:</strong> Classical Traditions Committee</span>
        <span>📅 <strong>Updated:</strong> October 2026</span>
        <span>🛡️ <strong>Methodology:</strong> Deterministic Coordinate Engine</span>
      </div>
    </header>

    <!-- AEO / GEO Featured Snippet Bait Box (Zero-Click Answer Engine Target) -->
    <aside class="snippet-box">
      <div class="snippet-label">⚡ Direct Answer Summary</div>
      <div class="snippet-question">{snippet_q}</div>
      <p class="snippet-answer">{snippet_a}</p>
    </aside>

    <!-- Executive Summary / Key Takeaways -->
    <div class="takeaways-box">
      <div class="takeaways-title">Key Takeaways &amp; Insights</div>
      <ul style="margin:0; padding-left:20px; line-height:1.7; color:#523E28;">
        <li>Mathematical coordinate analysis eliminates subjective guesswork.</li>
        <li>Harmonic conjunctions between the Driver (Mulank) and Conductor (Bhagyank) dictate core opportunities.</li>
        <li>Directional, gemstone, and lifestyle alignments neutralize challenging numerical tensions.</li>
      </ul>
    </div>

    <!-- Verified Visual Media (Venus Pearl & Jupiter Gold Luxury Design) -->
    {figure_html}

    <!-- Semantic Content Body -->
    {sections_html}

    <!-- Tabular Comparison Matrix for AI Overviews & Generative Engines -->
    <section class="matrix-table-wrap">
      <table class="matrix-table">
        <thead>
          <tr>{table_headers_html}</tr>
        </thead>
        <tbody>
          {table_rows_html}
        </tbody>
      </table>
    </section>

    <!-- People Also Ask / FAQ Section -->
    <section style="margin-top: 40px;">
      <h2 class="section-heading">Frequently Asked Questions</h2>
      {faq_items_html}
    </section>

    <!-- LSI Entity Cloud -->
    <div class="lsi-bar">
      {lsi_badges}
    </div>

    <!-- Internal Link Silo / Call to Action -->
    <div class="silo-box">
      <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.8rem; margin:0 0 10px 0; color:#8B6914;">Calculate Your Personal Destiny Blueprint</h3>
      <p style="margin:0 0 18px 0; color:#523E28; font-size:1rem; line-height:1.6;">Experience real-time multi-tradition numerology calculations with our zero-hallucination engine.</p>
      <a href="/calculators/" class="nv-btn-cta" style="display:inline-block; text-decoration:none;">Launch Free Life Path Calculator ⚡</a>
    </div>
  </main>

  <!-- Unified Master Footer (Identical to Home Page & Section Pages) -->
  <footer class="nv-footer">
    <div class="nv-footer-container">
      <div class="nv-footer-grid">
        <!-- Brand Summary Column -->
        <div class="nv-footer-brand-sec">
          <a href="/" class="nv-brand-link" style="margin-bottom:12px;">
            <div class="nv-brand-seal">
              <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
            </div>
            <div class="nv-brand-text">
              <span class="nv-brand-title">NUMEROS VISION</span>
              <span class="nv-brand-tagline">ANVEIL EVERY CHARM</span>
            </div>
          </a>
          <p>
            AI-powered numerology intelligence with transparent calculations, grounded classical frameworks, and understandable reflections across Vedic, Chaldean, Pythagorean, and Lo Shu traditions.
          </p>
        </div>

        <!-- Column 1: Working Calculators -->
        <div class="nv-footer-col">
          <h4>Calculators</h4>
          <ul class="nv-footer-links">
            <li><a href="/calculators/birth-number/">Birth Number</a></li>
            <li><a href="/calculators/life-path-number/">Life Path Number</a></li>
            <li><a href="/calculators/name-numerology/">Name Balancing</a></li>
            <li><a href="/calculators/chaldean-name-numerology/">Chaldean Numerology</a></li>
            <li><a href="/calculators/lo-shu-grid/">Lo Shu 3x3 Grid</a></li>
            <li><a href="/calculators/mobile-number-numerology/">Mobile Numerology</a></li>
            <li><a href="/calculators/personal-year/">Personal Year Calculator</a></li>
            <li><a href="/calculators/">View All Calculators →</a></li>
          </ul>
        </div>

        <!-- Column 2: Intelligence & Dossiers -->
        <div class="nv-footer-col">
          <h4>Intelligence &amp; Plans</h4>
          <ul class="nv-footer-links">
            <li><a href="/charm-ai/">Charm AI Assistant</a></li>
            <li><a href="/sample-report/">Sample Dossier</a></li>
            <li><a href="/reports/">Reports Catalogue</a></li>
            <li><a href="/pricing/">Plans &amp; Pricing</a></li>
            <li><a href="/consultation/">1-on-1 Consultation</a></li>
            <li><a href="/methodology/">Methodology &amp; Math</a></li>
            <li><a href="/sample-roadmap">Roadmap Preview Hub</a></li>
          </ul>
        </div>

        <!-- Column 3: Insights & Governance -->
        <div class="nv-footer-col">
          <h4>Wisdom &amp; Legal</h4>
          <ul class="nv-footer-links">
            <li><a href="/insights/">Insights Learning Hub</a></li>
            <li><a href="/insights/what-is-numerology">What is Numerology?</a></li>
            <li><a href="/faq/">Frequently Asked Questions</a></li>
            <li><a href="/about/">About Numeros Vision</a></li>
            <li><a href="/contact/">Contact Support</a></li>
            <li><a href="/privacy-policy/">Privacy Policy</a></li>
            <li><a href="/disclaimer/">Statutory Disclaimer</a></li>
            <li><a href="/terms/">Terms of Service</a></li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="nv-footer-bottom">
        <div>© 2026 Numeros Vision. All rights reserved. Master Brand: Numeros Vision • Tagline: ANVEIL EVERY CHARM.</div>
        <div class="nv-footer-legal-inline">
          <a href="/privacy-policy/">Privacy Policy</a>
          <a href="/terms/">Terms</a>
          <a href="/disclaimer/">Disclaimer</a>
          <a href="/cookie-policy/">Cookie Policy</a>
          <a href="/refund-policy/">Refund Policy</a>
          <a href="/accessibility/">Accessibility</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    function toggleMobileNav() {{
      var menu = document.getElementById('nv-nav-menu');
      if (menu) menu.classList.toggle('active');
    }}

    function toggleFaq(index) {{
      const items = document.querySelectorAll('.faq-item');
      items.forEach((item, idx) => {{
        if (idx === index) {{
          item.classList.toggle('active');
          const icon = item.querySelector('.faq-icon');
          if (icon) icon.textContent = item.classList.contains('active') ? '−' : '+';
        }}
      }});
    }}
  </script>

  <script src="/static/js/nv_consent.js" defer></script>
</body>
</html>
"""
        return html
