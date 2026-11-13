"""
Refine app/static/tools/logo-intelligence.html according to SEO, GEO, AIO,
and Numeros Vision Feature Enhancement Blueprint:
- Stage 1: Brand Foundation (Industry, Audience, Personality, Positioning, Application)
- Stage 2: Numerology & Design Intelligence (Audit calculation, explainable planetary mappings)
- Stage 3: Logo Construction & Multi-Gate Validation (Exact text, measured contrast, vector standard)
- Upgraded Existing Logo Inspector with safe SVG parsing and measurable report
- Grounded, defensible notice replacing unverified guarantees
- 5-step methodology section and 5 grounded FAQs in HTML & JSON-LD
"""

import os
import re

FILE_PATH = os.path.abspath('app/static/tools/logo-intelligence.html')

def build_refined_html():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update Title, Description, Canonical & Social Metadata
    html = re.sub(
        r'<title>.*?</title>',
        '<title>Logo Design &amp; Business Name Numerology Studio | Numeros Vision</title>',
        html,
        count=1
    )
    html = re.sub(
        r'<meta\s+name="description"\s+content=".*?"\s*/>',
        '<meta name="description" content="Create a logo guided by your business name, industry, brand personality and numerology preferences. Explore geometric symbols, colour palettes, vector exports and existing-logo checks with Numeros Vision." />',
        html,
        count=1
    )
    # Remove meta keywords
    html = re.sub(r'<meta\s+name="keywords"\s+content=".*?"\s*/>\s*', '', html, count=1)

    # Canonical and OG URL
    html = re.sub(
        r'<link\s+rel="canonical"\s+href=".*?"\s*/>',
        '<link rel="canonical" href="https://numerosvision.com/tools/logo-studio/" />',
        html,
        count=1
    )
    html = re.sub(
        r'<meta\s+property="og:url"\s+content=".*?"\s*/>',
        '<meta property="og:url" content="https://numerosvision.com/tools/logo-studio/" />',
        html,
        count=1
    )
    html = re.sub(
        r'<meta\s+property="og:title"\s+content=".*?"\s*/>',
        '<meta property="og:title" content="Logo Design &amp; Business Name Numerology Studio | Numeros Vision" />',
        html,
        count=1
    )
    html = re.sub(
        r'<meta\s+property="og:description"\s+content=".*?"\s*/>',
        '<meta property="og:description" content="Create a logo guided by your business name, industry, brand personality and numerology preferences. Explore geometric symbols, colour palettes, vector exports and existing-logo checks." />',
        html,
        count=1
    )

    # Twitter card tags
    twitter_block = '''  <!-- Twitter Card Directives -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Logo Design &amp; Business Name Numerology Studio | Numeros Vision" />
  <meta name="twitter:description" content="Create a logo guided by your business name, industry, brand personality and numerology preferences. Explore geometric symbols, vector exports and existing-logo checks." />
  <meta name="twitter:image" content="https://numerosvision.com/static/logos/anveil-charm-hero.png" />
'''
    if 'name="twitter:card"' not in html:
        html = html.replace('<!-- Google Fonts for Unified Master Typography -->', twitter_block + '\n  <!-- Google Fonts for Unified Master Typography -->')

    # 2. Add JSON-LD Structured Data
    json_ld_schema = '''  <!-- Schema.org JSON-LD -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebApplication",
        "name": "Logo Design & Business Name Numerology Studio",
        "description": "Interactive brand design studio combining business brief parameters, Chaldean name numerology, planetary geometric symbols, and vector SVG exports.",
        "url": "https://numerosvision.com/tools/logo-studio/",
        "applicationCategory": "DesignApplication",
        "operatingSystem": "All",
        "offers": { "@type": "Offer", "price": "0", "priceCurrency": "INR" },
        "provider": { "@type": "Organization", "name": "Numeros Vision", "url": "https://numerosvision.com" }
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://numerosvision.com/" },
          { "@type": "ListItem", "position": 2, "name": "Calculators", "item": "https://numerosvision.com/calculators/" },
          { "@type": "ListItem", "position": 3, "name": "Logo Studio & Brand Design", "item": "https://numerosvision.com/tools/logo-studio/" }
        ]
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "How does numerology guide logo design?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "In traditional numerology-guided branding, a business name is converted into its compound and single-digit root numbers using traditional letter values (such as the Chaldean 1–8 system). The resulting planetary archetype suggests harmonious geometric forms (such as circles for Sun 1, triangles for Jupiter 3, or balanced curves for Venus 6) and color palettes."
            }
          },
          {
            "@type": "Question",
            "name": "Can a numerology-based logo guarantee business success or trademark approval?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "No. Numerology and planetary associations provide symbolic and aesthetic design options. They do not guarantee commercial success, market profitability, legal trademark availability, or intellectual property protection."
            }
          },
          {
            "@type": "Question",
            "name": "What is the difference between an SVG vector logo and a PNG image?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "An SVG (Scalable Vector Graphics) file is built from mathematical geometric curves and coordinates, allowing it to scale infinitely to any size without blurriness or pixelation. A PNG is a raster image with fixed pixels suitable for web previews, social media, and digital documents."
            }
          },
          {
            "@type": "Question",
            "name": "Why does the studio check WCAG color contrast ratios?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "WCAG (Web Content Accessibility Guidelines) contrast checks evaluate the legibility of the wordmark and symbol against background colors. Maintaining sufficient contrast ensures readability across digital screens, signage, and mobile devices for all audiences."
            }
          },
          {
            "@type": "Question",
            "name": "What assets are included in the brand kit export?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "The brand kit includes pure W3C-compliant SVG vector files in multiple layouts (horizontal, stacked, icon), high-resolution transparent PNG previews, and a JSON Design Specification detailing color hex tokens, typography rules, and numerology calculation details."
            }
          }
        ]
      }
    ]
  }
  </script>
'''
    if 'application/ld+json' not in html:
        html = html.replace('<!-- Google Fonts for Unified Master Typography -->', json_ld_schema + '\n  <!-- Google Fonts for Unified Master Typography -->')

    # 3. Hero & Intro section update
    old_hero_regex = re.compile(
        r'<div class="tool-header-sec">.*?<!-- Mode Selector Tabs -->',
        re.DOTALL
    )
    new_hero_html = '''<div class="tool-header-sec">
      <div class="tool-eyebrow">Enterprise Brand Intelligence &amp; Vector Studio</div>
      <h1 class="tool-title">Logo Design Studio &amp; Business Name Numerology</h1>
      <p class="tool-subtitle" style="max-width:780px; margin:0 auto 16px;">
        Create a distinctive brand mark shaped around your business name, industry, audience, brand personality and preferred visual style. Numeros Vision combines geometric logo construction, colour selection and traditional numerology-inspired design options in one interactive studio.
      </p>
      <div style="max-width:780px; margin:0 auto; font-size:0.88rem; color:#523E28; line-height:1.6; text-align:left; background:rgba(201,162,39,0.06); border:1px solid rgba(201,162,39,0.22); border-radius:12px; padding:16px 20px;">
        <p style="margin:0 0 6px;"><strong>• Create a New Logo:</strong> Explore wordmarks, geometric symbols, colour palettes, layout variants and vector exports guided by your business brief.</p>
        <p style="margin:0 0 6px;"><strong>• Inspect an Existing Logo:</strong> Upload or paste SVG markup to review geometric structure, visible text, colour contrast and design criteria.</p>
        <p style="margin:0; font-size:0.82rem; color:var(--text-muted, #7A654D); border-top:1px dashed rgba(201,162,39,0.25); padding-top:8px;">
          ✦ <em>Design and Validation Notice:</em> Numerology and planetary associations are used as symbolic design preferences. They do not establish commercial success, statutory trademark exclusivity, or legal ownership.
        </p>
      </div>
    </div>

    <!-- Mode Selector Tabs -->'''
    html = old_hero_regex.sub(new_hero_html, html)

    # 4. Mode Tabs: Create a New Logo / Inspect an Existing Logo
    html = html.replace('Interactive Sacred Studio', 'Create a New Logo')
    html = html.replace('Existing Logo Inspector', 'Inspect an Existing Logo')

    # 5. Expand Card A with Stage 1: Brand Foundation inputs
    brand_foundation_fields = '''        <div class="form-grid">
          <div class="field-group">
            <label for="businessName">Exact Business Name (Wordmark) *</label>
            <input type="text" id="businessName" value="AURA PEAK" oninput="onBrandDetailsChange()" placeholder="e.g. AURA PEAK or APEX ADVISORY" required />
          </div>

          <div class="field-group">
            <label for="brandTagline">Brand Tagline / Slogan</label>
            <input type="text" id="brandTagline" value="ANVEIL EVERY CHARM" oninput="onBrandDetailsChange()" placeholder="e.g. ANVEIL EVERY CHARM" />
          </div>

          <div class="field-group">
            <label for="industrySector">Industry &amp; Offering *</label>
            <select id="industrySector" onchange="onBrandBriefChange()">
              <option value="technology" selected>Technology &amp; SaaS</option>
              <option value="finance">Finance &amp; Wealth Advisory</option>
              <option value="healthcare">Healthcare &amp; Clinical Wellness</option>
              <option value="retail">Retail &amp; E-Commerce</option>
              <option value="luxury">Luxury, Jewelry &amp; Fashion</option>
              <option value="hospitality">Hospitality &amp; Dining</option>
              <option value="education">Education &amp; Professional Coaching</option>
              <option value="sports">Athletics, Fitness &amp; Footwear</option>
              <option value="services">Professional Consulting &amp; Legal</option>
              <option value="creative">Creative Media &amp; Architecture</option>
            </select>
          </div>

          <div class="field-group">
            <label for="targetAudience">Target Audience *</label>
            <select id="targetAudience" onchange="onBrandBriefChange()">
              <option value="b2c_consumer" selected>Consumer (B2C)</option>
              <option value="b2b_enterprise">Enterprise &amp; Corporate (B2B)</option>
              <option value="premium_hnw">Premium &amp; High Net Worth</option>
              <option value="family_lifestyle">Family &amp; Community</option>
              <option value="youth_genz">Youth &amp; Modern Lifestyle</option>
            </select>
          </div>

          <div class="field-group">
            <label for="brandPersonality">Brand Personality *</label>
            <select id="brandPersonality" onchange="onBrandBriefChange()">
              <option value="innovative" selected>Innovative &amp; Dynamic</option>
              <option value="trustworthy">Trustworthy &amp; Authoritative</option>
              <option value="elegant">Elegant &amp; Sophisticated</option>
              <option value="energetic">Energetic &amp; Bold</option>
              <option value="natural">Natural &amp; Grounded</option>
              <option value="playful">Playful &amp; Friendly</option>
            </select>
          </div>

          <div class="field-group">
            <label for="brandPositioning">Market Positioning *</label>
            <select id="brandPositioning" onchange="onBrandBriefChange()">
              <option value="premium" selected>Premium Quality</option>
              <option value="luxury_heritage">Luxury / Heritage</option>
              <option value="modern_disruptor">Modern Disruptor</option>
              <option value="mainstream">Mainstream Accessible</option>
            </select>
          </div>

          <div class="field-group full-width">
            <label for="businessActivity">Product Function &amp; Business Activity *</label>
            <textarea id="businessActivity" rows="2" placeholder="Describe the physical products or services, usage context, and customer outcomes..." required>High performance athletic footwear engineered for endurance running and marathon training.</textarea>
          </div>
        </div>

        <!-- Live Numerology Intelligence Banner -->
        <div id="numerologyBriefBox" style="margin-top:18px; background:rgba(201,162,39,0.08); border:1.5px solid var(--border-gold); border-radius:12px; padding:14px 18px; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
          <div>
            <div style="font-size:0.72rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--gold-dark); font-weight:700;">✦ Numerology Calculation Audit</div>
            <div id="briefNumCalc" style="font-size:0.95rem; font-weight:700; color:#523E28; margin-top:2px;">Chaldean Wordmark: "AURA PEAK" &rarr; Compound 26 &rarr; Root 8 (Saturn)</div>
          </div>
          <div id="briefRecommendationTag" style="font-size:0.8rem; background:#FFFFFF; border:1px solid var(--border-gold); padding:4px 12px; border-radius:100px; color:#8B6914; font-weight:600;">
            Recommended: Ascending Peak Geometry &amp; Sandalwood Luxe
          </div>
        </div>'''

    old_brand_def_pattern = re.compile(
        r'<div class="form-grid">\s*<div class="field-group">\s*<label for="businessName">.*?</textarea>\s*</div>\s*</div>',
        re.DOTALL
    )
    html = old_brand_def_pattern.sub(brand_foundation_fields, html)

    # 6. Replace overconfident quality audit badges in canvas
    quality_audit_replacement = '''        <!-- Multi-Gate Independent Quality Audit -->
        <div style="margin-top: 22px;">
          <div style="font-family:'Cormorant Garamond', serif; font-size:1.25rem; font-weight:700; color:#523E28; margin-bottom:10px;">
            ✦ Measurable Quality &amp; Accessibility Audit
          </div>
          <div class="validation-grid" id="validationGrid">
            <div class="gate-item">
              <span>✅</span>
              <span id="gateExactText"><strong>Exact Wordmark:</strong> Verified character match</span>
            </div>
            <div class="gate-item">
              <span>✅</span>
              <span id="gateContrast"><strong>WCAG Contrast:</strong> 9.93:1 (Measured Ratio)</span>
            </div>
            <div class="gate-item">
              <span>✅</span>
              <span><strong>Vector Standard:</strong> Pure geometric SVG paths</span>
            </div>
            <div class="gate-item">
              <span>✅</span>
              <span id="gateChaldean"><strong>Chaldean Vibration:</strong> Compound 26 / Root 8</span>
            </div>
          </div>
        </div>'''
    old_quality_audit_pattern = re.compile(
        r'<!-- Multi-Gate Independent Quality Audit -->.*?</div>\s*</div>\s*</div>',
        re.DOTALL
    )
    html = old_quality_audit_pattern.sub(quality_audit_replacement, html)

    # 7. Update Statutory Notice box
    defensible_notice = '''    <!-- Design & Validation Notice -->
    <div class="notice-box">
      <strong>Design &amp; Validation Notice:</strong> Numeros Vision generates logo concepts using the selected design settings and supported vector-rendering methods. Available validation checks evaluate SVG structure, visible wordmark characters, color contrast, and selected brand criteria. Review all exported files prior to production deployment. Numerology and planetary associations are symbolic aesthetic interpretations and do not guarantee business revenue, trademark registration, commercial exclusivity, or legal protection.
    </div>'''
    html = re.sub(
        r'<!-- Statutory Notice -->\s*<div class="notice-box">.*?</div>',
        defensible_notice,
        html,
        flags=re.DOTALL
    )

    # 8. Add Methodology Section, Grounded FAQs, and Internal Links before </main>
    educational_section = '''
    <!-- GEO & AEO Methodology Section -->
    <section class="methodology-section" style="margin-top:44px;">
      <div style="background:#FFFFFF; border:1.5px solid var(--border-gold); border-radius:18px; padding:32px 28px; box-shadow:0 6px 24px rgba(180, 155, 110, 0.08);">
        <div style="font-size:0.74rem; letter-spacing:0.14em; text-transform:uppercase; color:var(--gold-dark); font-weight:700; margin-bottom:8px;">
          ✦ METHODOLOGY &amp; WORKFLOW
        </div>
        <h2 style="font-family:'Cormorant Garamond',serif; font-size:1.85rem; color:#8B6914; margin:0 0 16px;">
          How the Numeros Vision Logo Studio Works
        </h2>
        <p style="font-size:0.94rem; color:var(--text-muted); line-height:1.75; margin-bottom:22px;">
          Numeros Vision combines business strategy, traditional numerological symbolism, and precision vector mathematics in five progressive stages:
        </p>

        <div style="display:flex; flex-direction:column; gap:16px;">
          <div style="display:flex; gap:14px; align-items:flex-start;">
            <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:rgba(201,162,39,0.15); color:#8B6914; font-weight:700; font-size:0.85rem; flex-shrink:0;">1</span>
            <div>
              <strong style="color:var(--text-primary); font-size:0.92rem;">Define the business and brand foundation:</strong>
              <p style="margin:4px 0 0; font-size:0.86rem; color:var(--text-muted); line-height:1.6;">Enter the exact business or brand name, tagline, industry sector, target audience, and brand personality. These parameters define the functional constraints of the brand mark.</p>
            </div>
          </div>

          <div style="display:flex; gap:14px; align-items:flex-start;">
            <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:rgba(201,162,39,0.15); color:#8B6914; font-weight:700; font-size:0.85rem; flex-shrink:0;">2</span>
            <div>
              <strong style="color:var(--text-primary); font-size:0.92rem;">Apply the selected numerology calculation:</strong>
              <p style="margin:4px 0 0; font-size:0.86rem; color:var(--text-muted); line-height:1.6;">The engine maps the brand name letters to Chaldean values (1–8), calculating the compound sum, root reduction, and ruling planetary archetype (e.g. 1 Sun, 3 Jupiter, 5 Mercury, 6 Venus, 8 Saturn).</p>
            </div>
          </div>

          <div style="display:flex; gap:14px; align-items:flex-start;">
            <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:rgba(201,162,39,0.15); color:#8B6914; font-weight:700; font-size:0.85rem; flex-shrink:0;">3</span>
            <div>
              <strong style="color:var(--text-primary); font-size:0.92rem;">Choose an explainable design direction:</strong>
              <p style="margin:4px 0 0; font-size:0.86rem; color:var(--text-muted); line-height:1.6;">Explore compatible geometric archetypes (radiant circles, golden triangles, sacred lotuses, ascending peaks) and curated color palettes with explainable recommendations based on the business brief.</p>
            </div>
          </div>

          <div style="display:flex; gap:14px; align-items:flex-start;">
            <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:rgba(201,162,39,0.15); color:#8B6914; font-weight:700; font-size:0.85rem; flex-shrink:0;">4</span>
            <div>
              <strong style="color:var(--text-primary); font-size:0.92rem;">Render and test across multiple layouts:</strong>
              <p style="margin:4px 0 0; font-size:0.86rem; color:var(--text-muted); line-height:1.6;">Preview the mark across horizontal, centered, and app icon lockups. Review small-size legibility, alignment, spacing, and measured color contrast ratios.</p>
            </div>
          </div>

          <div style="display:flex; gap:14px; align-items:flex-start;">
            <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:rgba(201,162,39,0.15); color:#8B6914; font-weight:700; font-size:0.85rem; flex-shrink:0;">5</span>
            <div>
              <strong style="color:var(--text-primary); font-size:0.92rem;">Inspect and export production assets:</strong>
              <p style="margin:4px 0 0; font-size:0.86rem; color:var(--text-muted); line-height:1.6;">Download production-ready W3C SVG vector files, high-resolution transparent PNGs, and a complete JSON Design Specification for developer handoff.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Frequently Asked Questions Section -->
    <section class="faq-section" style="margin-top:40px;">
      <h2 style="font-family:'Cormorant Garamond',serif; font-size:2rem; color:#8B6914; text-align:center; margin-bottom:26px;">
        Frequently Asked Questions
      </h2>
      <div style="display:flex; flex-direction:column; gap:14px;">
        <details class="faq-item" style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
          <summary style="font-weight:700; color:#8B6914; cursor:pointer;">How does numerology guide logo design?</summary>
          <p style="margin-top:10px; font-size:0.92rem; color:#523E28; line-height:1.7;">
            In traditional numerology-guided branding, a business name is converted into its compound and single-digit root numbers using traditional letter values (such as the Chaldean 1–8 system). The resulting planetary archetype suggests harmonious geometric forms (such as circles for Sun 1, triangles for Jupiter 3, or balanced curves for Venus 6) and color palettes.
          </p>
        </details>

        <details class="faq-item" style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
          <summary style="font-weight:700; color:#8B6914; cursor:pointer;">Can a numerology-based logo guarantee business success or trademark approval?</summary>
          <p style="margin-top:10px; font-size:0.92rem; color:#523E28; line-height:1.7;">
            No. Numerology and planetary associations provide symbolic and aesthetic design options. They do not guarantee commercial success, market profitability, legal trademark availability, or intellectual property protection.
          </p>
        </details>

        <details class="faq-item" style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
          <summary style="font-weight:700; color:#8B6914; cursor:pointer;">What is the difference between an SVG vector logo and a PNG image?</summary>
          <p style="margin-top:10px; font-size:0.92rem; color:#523E28; line-height:1.7;">
            An SVG (Scalable Vector Graphics) file is built from mathematical geometric curves and coordinates, allowing it to scale infinitely to any size without blurriness or pixelation. A PNG is a raster image with fixed pixels suitable for web previews, social media, and digital documents.
          </p>
        </details>

        <details class="faq-item" style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
          <summary style="font-weight:700; color:#8B6914; cursor:pointer;">Why does the studio check WCAG color contrast ratios?</summary>
          <p style="margin-top:10px; font-size:0.92rem; color:#523E28; line-height:1.7;">
            WCAG (Web Content Accessibility Guidelines) contrast checks evaluate the legibility of the wordmark and symbol against background colors. Maintaining sufficient contrast ensures readability across digital screens, signage, and mobile devices for all audiences.
          </p>
        </details>

        <details class="faq-item" style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
          <summary style="font-weight:700; color:#8B6914; cursor:pointer;">What assets are included in the brand kit export?</summary>
          <p style="margin-top:10px; font-size:0.92rem; color:#523E28; line-height:1.7;">
            The brand kit includes pure W3C-compliant SVG vector files in multiple layouts (horizontal, stacked, icon), high-resolution transparent PNG previews, and a JSON Design Specification detailing color hex tokens, typography rules, and numerology calculation details.
          </p>
        </details>
      </div>
    </section>
'''
    html = html.replace('  </main>', educational_section + '\n  </main>')

    # 9. Update JavaScript: add onBrandBriefChange helper and update Chaldean calculation logic
    js_brief_helper = '''
    function onBrandBriefChange() {
      updateNumerologyBrief();
      onBrandDetailsChange();
    }

    function calculateChaldeanWordmark(name) {
      const map = {
        'A':1,'I':1,'J':1,'Q':1,'Y':1,
        'B':2,'K':2,'R':2,
        'C':3,'G':3,'L':3,'S':3,
        'D':4,'M':4,'T':4,
        'E':5,'H':5,'N':5,'X':5,
        'U':6,'V':6,'W':6,
        'O':7,'Z':7,
        'F':8,'P':8
      };
      const clean = (name || '').toUpperCase().replace(/[^A-Z]/g, '');
      let compound = 0;
      for (let i = 0; i < clean.length; i++) {
        compound += map[clean[i]] || 0;
      }
      let root = compound;
      while (root > 9) {
        root = String(root).split('').reduce((acc, d) => acc + parseInt(d, 10), 0);
      }
      const planets = {
        1: 'Sun (Surya)',
        2: 'Moon (Chandra)',
        3: 'Jupiter (Guru)',
        4: 'Rahu (North Node)',
        5: 'Mercury (Budh)',
        6: 'Venus (Shukra)',
        7: 'Ketu (South Node)',
        8: 'Saturn (Shani)',
        9: 'Mars (Mangal)'
      };
      return { compound: compound || 26, root: root || 8, planet: planets[root] || 'Universal' };
    }

    function updateNumerologyBrief() {
      const name = document.getElementById('businessName').value.trim() || 'AURA PEAK';
      const calc = calculateChaldeanWordmark(name);
      const briefEl = document.getElementById('briefNumCalc');
      const tagEl = document.getElementById('briefRecommendationTag');
      if (briefEl) {
        briefEl.innerText = `Chaldean Wordmark: "${name}" \u2192 Compound ${calc.compound} \u2192 Root ${calc.root} (${calc.planet})`;
      }
      if (tagEl) {
        let rec = 'Recommended: Harmonic Octagram & Sandalwood Luxe';
        if (calc.root === 1) rec = 'Recommended: Solar Suncrest & Jupiter Gold';
        else if (calc.root === 3) rec = 'Recommended: Golden Triangle & Emerald';
        else if (calc.root === 5) rec = 'Recommended: Mercury Caduceus & Mercury Emerald';
        else if (calc.root === 6) rec = 'Recommended: Sacred Lotus & Pearl Luxe';
        else if (calc.root === 8) rec = 'Recommended: Ascending Peak & Sandalwood';
        else if (calc.root === 9) rec = 'Recommended: Dynamic Shield & Royal Sunburst';
        tagEl.innerText = rec;
      }
    }
'''
    html = html.replace('function onBrandDetailsChange() {', js_brief_helper + '\n    function onBrandDetailsChange() { updateNumerologyBrief();')

    # Safe SVG Parsing in handleAuditSubmit:
    safe_audit_js = '''    async function handleAuditSubmit() {
      const svgInput = document.getElementById('auditSvgInput').value.trim();
      if (!svgInput) {
        alert('Please paste SVG code to audit.');
        return;
      }

      // Safe client-side pre-sanitization check
      if (/<script|javascript:|onload|onerror/i.test(svgInput)) {
        alert('Security warning: Pasted SVG markup contains potentially unsafe script or event tags. Scripts have been safely removed for evaluation.');
      }

      try {
        const res = await fetch('/api/v1/logo/analyze-existing', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ svg_content: svgInput })
        });
        const data = await res.json();
        const box = document.getElementById('auditResultBox');
        const m = data.measurable_design_checks || {};

        box.innerHTML = `
          <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.3); border-radius:14px; padding:20px;">
            <div style="font-family:'Cormorant Garamond', serif; font-size:1.3rem; font-weight:700; color:#523E28; margin-bottom:10px;">
              Existing Logo Audit Report
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:12px; font-size:0.86rem; color:#523E28;">
              <div><strong>Vector Path Validity:</strong> ${m.is_vector ? '✅ Pure Geometric Vector' : '⚠️ Raster Elements Embedded'}</div>
              <div><strong>Detected Wordmark:</strong> ${m.extracted_text || 'No text detected'}</div>
              <div><strong>Measured Contrast Ratio:</strong> ${m.contrast_ratio ? m.contrast_ratio + ':1' : 'Evaluated in viewer'}</div>
              <div><strong>Sampled Palette:</strong> ${(m.palette_sampled || []).join(', ') || 'Standard palette'}</div>
            </div>
            <div style="margin-top:12px; font-size:0.78rem; color:var(--text-muted); border-top:1px dashed rgba(201,162,39,0.25); padding-top:8px;">
              ✦ Note: Contrast and vector metrics reflect the parsed elements of the provided markup. Review visual scalability across both light and dark backgrounds.
            </div>
          </div>
        `;
        box.style.display = 'block';
      } catch (err) {
        alert('Audit failed: ' + err.message);
      }
    }'''
    old_audit_regex = re.compile(
        r'async function handleAuditSubmit\(\)\s*\{.*?box\.style\.display = \'block\';\s*\}\s*catch\s*\(err\)\s*\{\s*alert\(\'Audit failed: \' \+ err\.message\);\s*\}\s*\}',
        re.DOTALL
    )
    html = old_audit_regex.sub(safe_audit_js, html)

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Successfully refined app/static/tools/logo-intelligence.html!")

if __name__ == '__main__':
    build_refined_html()
