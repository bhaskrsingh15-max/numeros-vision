"""
Refine app/static/tools/business-alignment.html according to SEO, GEO, AIO,
and P0/P1 audit guidelines:
- P0: Clarify separation between commercial analysis and traditional numerology
- P0: Replace prefilled sample data with informative placeholders and optional 'Load Sample Demo' trigger
- P0: Sector disclaimer for healthcare, licensing, and professional advice
- P1: SEO Title, meta description, and canonical URL alignment
- P1: Schema.org WebApplication, BreadcrumbList, and FAQPage
- P1: Clear H1 and tab labels (New Venture Assessment / Existing Business Review)
- P1: GEO/AEO 'How Does the Business Assessment Work?' section
- P1: 5 grounded FAQs aligned in visible HTML and JSON-LD
- P1: Business data privacy explanation
- P2: Refined scoring language and CTA buttons ('Assess My Business Idea' / 'Review My Business')
"""

import os
import re

FILE_PATH = os.path.abspath('app/static/tools/business-alignment.html')

def build_refined_html():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Title, Description, Canonical & Social Metadata
    html = re.sub(
        r'<title>.*?</title>',
        '<title>Business Numerology &amp; Business Diagnostic | Numeros Vision</title>',
        html,
        count=1
    )
    html = re.sub(
        r'<meta\s+name="description"\s+content=".*?"\s*/>',
        '<meta name="description" content="Explore a business numerology assessment for a new venture or existing business. Review founder and brand-name numerology alongside practical business factors, with clear separation between traditional interpretations and commercial analysis." />',
        html,
        count=1
    )
    # Remove meta keywords
    html = re.sub(r'<meta\s+name="keywords"\s+content=".*?"\s*/>\s*', '', html, count=1)

    # Canonical and OG URL
    html = re.sub(
        r'<link\s+rel="canonical"\s+href=".*?"\s*/>',
        '<link rel="canonical" href="https://numerosvision.com/tools/business-alignment/" />',
        html,
        count=1
    )
    html = re.sub(
        r'<meta\s+property="og:url"\s+content=".*?"\s*/>',
        '<meta property="og:url" content="https://numerosvision.com/tools/business-alignment/" />',
        html,
        count=1
    )
    html = re.sub(
        r'<meta\s+property="og:title"\s+content=".*?"\s*/>',
        '<meta property="og:title" content="Business Numerology &amp; Business Diagnostic | Numeros Vision" />',
        html,
        count=1
    )
    html = re.sub(
        r'<meta\s+property="og:description"\s+content=".*?"\s*/>',
        '<meta property="og:description" content="Explore a business numerology assessment for a new venture or existing business. Review founder and brand-name numerology alongside practical business factors, with clear separation between traditional interpretations and commercial analysis." />',
        html,
        count=1
    )

    # Twitter card tags
    twitter_block = '''  <!-- Twitter Card Directives -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Business Numerology &amp; Business Diagnostic | Numeros Vision" />
  <meta name="twitter:description" content="Explore a business numerology assessment for a new venture or existing business. Review founder and brand-name numerology alongside practical business factors." />
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
        "name": "Business Numerology & Business Diagnostic",
        "description": "Assess a proposed venture or review an existing business through practical commercial factors and traditional numerology interpretations.",
        "url": "https://numerosvision.com/tools/business-alignment/",
        "applicationCategory": "BusinessApplication",
        "operatingSystem": "All",
        "offers": { "@type": "Offer", "price": "0", "priceCurrency": "INR" },
        "provider": { "@type": "Organization", "name": "Numeros Vision", "url": "https://numerosvision.com" }
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://numerosvision.com/" },
          { "@type": "ListItem", "position": 2, "name": "Calculators", "item": "https://numerosvision.com/calculators/" },
          { "@type": "ListItem", "position": 3, "name": "Business Numerology & Diagnostic", "item": "https://numerosvision.com/tools/business-alignment/" }
        ]
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "What is business numerology?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Business numerology applies a selected numerology tradition to a company name, brand name or other business-related inputs. Interpretations depend on the calculation method used and should be distinguished from evidence-based commercial analysis."
            }
          },
          {
            "@type": "Question",
            "name": "Can numerology determine whether a startup will succeed?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "No numerology result can reliably establish whether a startup will succeed. Business viability depends on factors such as customer demand, competition, pricing, costs, execution and available capital. Numerology can be explored separately as a traditional interpretive framework."
            }
          },
          {
            "@type": "Question",
            "name": "What is the difference between a legal business name and a trading name?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "A legal business name identifies the registered legal entity, while a trading or brand name is the name used to present the business to customers. They may be identical or different, depending on the business and applicable rules."
            }
          },
          {
            "@type": "Question",
            "name": "What information do I need for a new venture assessment?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "The current form asks for the founder's name and date of birth, skills, available startup capital range, proposed business name, revenue model and business activity. The accuracy and scope of the assessment depend on the inputs and checks implemented by the tool."
            }
          },
          {
            "@type": "Question",
            "name": "Can I use this tool for an existing business?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. The existing-business form asks for the legal entity name, customer-facing brand name, products or services, fixed constraints and reported operating challenges. Its findings should be treated as an initial structured review, not a substitute for financial, legal or sector-specific professional advice."
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
        r'<div class="tool-header-sec">.*?<!-- Luxury Tab Switcher -->',
        re.DOTALL
    )
    new_hero_html = '''<div class="tool-header-sec">
      <div class="tool-eyebrow">Enterprise Strategic Intelligence</div>
      <h1 class="tool-title">Business Numerology &amp; Operating Business Diagnostic</h1>
      <p class="tool-subtitle" style="max-width:760px; margin:0 auto 14px;">
        Assess a proposed venture or review an existing business through two clearly separated lenses: practical business factors and traditional Chaldean-Vedic numerology interpretations.
      </p>
      <div style="max-width:760px; margin:0 auto; font-size:0.88rem; color:#523E28; line-height:1.6; text-align:left; background:rgba(201,162,39,0.06); border:1px solid rgba(201,162,39,0.22); border-radius:12px; padding:16px 20px;">
        <p style="margin:0 0 8px;"><strong>• New Venture Assessment:</strong> Review a proposed business name, founder profile, skills, available capital range, revenue model, and business activity.</p>
        <p style="margin:0 0 8px;"><strong>• Existing Business Review:</strong> Organize legal entity details, trading brand name, operating constraints, and reported challenges into a structured assessment.</p>
        <p style="margin:0; font-size:0.82rem; color:var(--text-muted, #7A654D); border-top:1px dashed rgba(201,162,39,0.25); padding-top:8px;">
          ✦ <em>Professional Disclaimer:</em> Numerology-based interpretations are presented separately from commercial analysis for reflection and exploration. They are not a substitute for market research, financial modelling, clinical, licensing, or sector-specific legal advice.
        </p>
      </div>
    </div>

    <!-- Luxury Tab Switcher -->'''
    html = old_hero_regex.sub(new_hero_html, html)

    # 4. Tab Labels update
    html = html.replace('Startup Direction (New Venture)', 'New Venture Assessment')
    html = html.replace('Operating Business Diagnostic\n        </button>', 'Existing Business Review\n        </button>')

    # 5. Form inputs: replace pre-filled values with clean placeholders + add Sample Demo buttons
    # Panel A: Startup Form
    html = re.sub(r'value="Alex Mercer"', 'placeholder="e.g. Alex Mercer"', html)
    html = re.sub(r'value="1990-05-15"', '', html)
    html = re.sub(r'value="software_engineering, product_management"', 'placeholder="e.g. software engineering, sales, marketing"', html)
    html = re.sub(r'value="PulseFlow Cloud"', 'placeholder="e.g. PulseFlow Cloud or Apex Systems"', html)
    html = html.replace(
        '<textarea id="activityDesc" rows="3" required>Cloud-based workflow automation and operational scheduling software for digital remote teams.</textarea>',
        '<textarea id="activityDesc" rows="3" required placeholder="Describe your product or service, target customer, and main business activity..."></textarea>'
    )

    # Add Load Sample Demo button for Startup Form
    startup_btn_replacement = '''        <div class="field-group full-width" style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
          <button type="submit" class="btn-calc" id="btnStartup" style="flex:2; min-width:240px;">
            <span>Assess My Business Idea ✦</span>
          </button>
          <button type="button" class="btn-preview-demo" onclick="loadStartupSampleData()" style="flex:1; min-width:180px; padding:15px 18px;">
            <span>Load Sample Data</span>
          </button>
        </div>
        <div class="field-group full-width" style="font-size:0.78rem; color:var(--text-muted); text-align:center;">
          🔒 <strong>Business Data Privacy:</strong> Information entered is processed for this assessment session only. See our <a href="/privacy-policy/" style="color:#8B6914;">Privacy Policy</a>.
        </div>'''
    html = re.sub(
        r'<div class="field-group full-width">\s*<button type="submit" class="btn-calc" id="btnStartup">.*?</div>',
        startup_btn_replacement,
        html,
        flags=re.DOTALL
    )

    # Panel B: Existing Business Form
    html = re.sub(r'value="Apex Healthcare Private Limited"', 'placeholder="e.g. Apex Enterprises Private Limited"', html)
    html = re.sub(r'value="Apex Vitality Clinic"', 'placeholder="e.g. Apex Clinic or Apex Brand"', html)
    html = html.replace(
        '<textarea id="productsServices" rows="2" required>Outpatient clinical diagnostics, preventive cardiology, and physical therapy services.</textarea>',
        '<textarea id="productsServices" rows="2" required placeholder="e.g. Outpatient clinical diagnostics, consulting, retail products..."></textarea>'
    )
    html = re.sub(r'value="5-year hospital commercial lease signed, State medical board facility license"', 'placeholder="e.g. Commercial lease commitment, sector licensing..."', html)
    html = re.sub(r'value="Customer retention dropping in Q3, Insurance claim reimbursement delays"', 'placeholder="e.g. Customer retention, payment cycle delays, expansion bottleneck..."', html)

    # Add Load Sample Demo button for Existing Form
    existing_btn_replacement = '''        <div class="field-group full-width" style="display:flex; gap:12px; flex-wrap:wrap; align-items:center;">
          <button type="submit" class="btn-calc" id="btnExisting" style="flex:2; min-width:240px;">
            <span>Review My Business ✦</span>
          </button>
          <button type="button" class="btn-preview-demo" onclick="loadExistingSampleData()" style="flex:1; min-width:180px; padding:15px 18px;">
            <span>Load Sample Data</span>
          </button>
        </div>
        <div class="field-group full-width" style="font-size:0.78rem; color:var(--text-muted); text-align:center;">
          🔒 <strong>Professional Notice:</strong> Numerology is not a substitute for financial, legal, licensing, or clinical advice. See our <a href="/disclaimer/" style="color:#8B6914;">Disclaimer</a>.
        </div>'''
    html = re.sub(
        r'<div class="field-group full-width">\s*<button type="submit" class="btn-calc" id="btnExisting">.*?</div>',
        existing_btn_replacement,
        html,
        flags=re.DOTALL
    )

    # 6. Add Methodology Section, Grounded FAQs, and Internal Links between </main> and <footer>
    educational_section = '''
    <!-- GEO & AEO Methodology Section -->
    <section class="methodology-section" style="margin-top:48px;">
      <div style="background:#FFFFFF; border:1.5px solid var(--border-gold); border-radius:18px; padding:32px 28px; box-shadow:0 6px 24px rgba(180, 155, 110, 0.08);">
        <div style="font-size:0.74rem; letter-spacing:0.14em; text-transform:uppercase; color:var(--gold-dark); font-weight:700; margin-bottom:8px;">
          ✦ METHODOLOGY &amp; EVIDENCE BOUNDARIES
        </div>
        <h2 style="font-family:'Cormorant Garamond',serif; font-size:1.85rem; color:#8B6914; margin:0 0 16px;">
          How Does the Business Assessment Work?
        </h2>
        <p style="font-size:0.94rem; color:var(--text-muted); line-height:1.75; margin-bottom:22px;">
          Numeros Vision separates practical commercial factors from traditional numerology interpretations to help founders and business owners clearly understand the basis of their results:
        </p>

        <div style="display:flex; flex-direction:column; gap:18px;">
          <div style="border-left:3.5px solid var(--gold); padding-left:16px;">
            <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.35rem; color:#8B6914; margin:0 0 6px;">
              1. Practical Business Assessment
            </h3>
            <p style="font-size:0.9rem; color:#523E28; line-height:1.7; margin:0 0 6px;">
              For a new venture, the assessment evaluates the information supplied about the proposed business, available capital runway, founder skills, revenue model, and business activity. For an existing business, it organizes legal entity details, trading brand names, operational constraints, and reported performance challenges.
            </p>
            <p style="font-size:0.84rem; color:var(--text-muted); line-height:1.6; margin:0;">
              <em>Scope:</em> Findings reflect the specific inputs provided. A complete commercial viability evaluation requires independent market evidence, including customer demand, competitor benchmarking, cost structures, and cash-flow projections.
            </p>
          </div>

          <div style="border-left:3.5px solid #16835B; padding-left:16px;">
            <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.35rem; color:#16835B; margin:0 0 6px;">
              2. Traditional Numerology Interpretation
            </h3>
            <p style="font-size:0.9rem; color:#523E28; line-height:1.7; margin:0 0 6px;">
              The numerology layer calculates the Chaldean compound and root numbers of the proposed or legal business name (values 1–8) and compares them with the founder's birth Driver (Mulank) and Conductor (Bhagyank) numbers where provided.
            </p>
            <p style="font-size:0.84rem; color:var(--text-muted); line-height:1.6; margin:0;">
              <em>Transparency:</em> Full acoustic letter breakdowns and calculation steps are presented in the report so users can follow the exact mathematical steps behind each symbolic association.
            </p>
          </div>

          <div style="border-left:3.5px solid #8B6914; padding-left:16px;">
            <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.35rem; color:#8B6914; margin:0 0 6px;">
              3. Understanding Your Results &amp; Scoring
            </h3>
            <p style="font-size:0.9rem; color:#523E28; line-height:1.7; margin:0;">
              Commercial findings and numerology interpretations are reported in separate sections. The harmony score reflects alignment within the chosen classical numerological framework, not a statistically validated probability of business revenue or success. Use empirical business evidence, professional counsel, and personal judgment for operational decisions.
            </p>
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
          <summary style="font-weight:700; color:#8B6914; cursor:pointer;">What is business numerology?</summary>
          <p style="margin-top:10px; font-size:0.92rem; color:#523E28; line-height:1.7;">
            Business numerology applies a selected numerology tradition to a company name, brand name or other business-related inputs. Interpretations depend on the calculation method used and should be distinguished from evidence-based commercial analysis.
          </p>
        </details>

        <details class="faq-item" style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
          <summary style="font-weight:700; color:#8B6914; cursor:pointer;">Can numerology determine whether a startup will succeed?</summary>
          <p style="margin-top:10px; font-size:0.92rem; color:#523E28; line-height:1.7;">
            No numerology result can reliably establish whether a startup will succeed. Business viability depends on factors such as customer demand, competition, pricing, costs, execution and available capital. Numerology can be explored separately as a traditional interpretive framework.
          </p>
        </details>

        <details class="faq-item" style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
          <summary style="font-weight:700; color:#8B6914; cursor:pointer;">What is the difference between a legal business name and a trading name?</summary>
          <p style="margin-top:10px; font-size:0.92rem; color:#523E28; line-height:1.7;">
            A legal business name identifies the registered legal entity, while a trading or brand name is the name used to present the business to customers. They may be identical or different, depending on the business and applicable rules.
          </p>
        </details>

        <details class="faq-item" style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
          <summary style="font-weight:700; color:#8B6914; cursor:pointer;">What information do I need for a new venture assessment?</summary>
          <p style="margin-top:10px; font-size:0.92rem; color:#523E28; line-height:1.7;">
            The current form asks for the founder's name and date of birth, skills, available startup capital range, proposed business name, revenue model and business activity. The accuracy and scope of the assessment depend on the inputs and checks implemented by the tool.
          </p>
        </details>

        <details class="faq-item" style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
          <summary style="font-weight:700; color:#8B6914; cursor:pointer;">Can I use this tool for an existing business?</summary>
          <p style="margin-top:10px; font-size:0.92rem; color:#523E28; line-height:1.7;">
            Yes. The existing-business form asks for the legal entity name, customer-facing brand name, products or services, fixed constraints and reported operating challenges. Its findings should be treated as an initial structured review, not a substitute for financial, legal or sector-specific professional advice.
          </p>
        </details>
      </div>
    </section>
'''
    html = html.replace('  </main>', educational_section + '\n  </main>')

    # 7. JavaScript: Add Sample Data Helpers & Refine Scoring Label
    sample_helper_js = '''
    function loadStartupSampleData() {
      document.getElementById('founderName').value = "Alex Mercer";
      document.getElementById('founderDob').value = "1990-05-15";
      document.getElementById('capitalBand').value = "seed_10k_50k";
      document.getElementById('founderSkills').value = "software engineering, product management";
      document.getElementById('ideaName').value = "PulseFlow Cloud";
      document.getElementById('revenueModel').value = "subscription";
      document.getElementById('activityDesc').value = "Cloud-based workflow automation and operational scheduling software for digital remote teams.";
      onFounderDobChange();
    }

    function loadExistingSampleData() {
      document.getElementById('legalName').value = "Apex Consulting Private Limited";
      document.getElementById('tradingName').value = "Apex Strategy Group";
      document.getElementById('productsServices').value = "Enterprise strategic advisory, supply chain diagnostics, and operational auditing.";
      document.getElementById('constraints').value = "Long-term client service retainers, professional indemnity insurance guidelines.";
      document.getElementById('challenges').value = "Quarterly client contract renewals, extended corporate billing cycles.";
    }
'''
    html = html.replace('function switchTab(tab) {', sample_helper_js + '\n    function switchTab(tab) {')

    # Update scoring label in result rendering
    html = html.replace('<span class="score-lbl">Cosmic Synergy</span>', '<span class="score-lbl">Harmony Score</span>')
    html = html.replace('Founder Cosmic Synergy score', 'Founder-Name Harmony score')

    # Update button text while loading
    html = html.replace('btn.innerText = "Analyzing Commercial & Archetype Alignment...";', 'btn.innerText = "Assessing Business Factors & Numerology...";')

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Successfully refined app/static/tools/business-alignment.html!")

if __name__ == '__main__':
    build_refined_html()
