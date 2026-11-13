"""
Refine app/static/tools/name-balancing.html according to Numeros Vision SEO, GEO, AIO,
and P0 Security/Privacy Guidelines.
"""

import os
import re

FILE_PATH = os.path.abspath('app/static/tools/name-balancing.html')

def refine_name_balancing():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. P0 Security: Remove test_master_pass assignment
    test_token_pattern = re.compile(
        r"if\s*\(!localStorage\.getItem\(['\"]nv_premium_token['\"]\)\)\s*\{\s*localStorage\.setItem\(['\"]nv_premium_token['\"],\s*['\"]test_master_pass['\"]\);\s*\}",
        re.MULTILINE
    )
    html = test_token_pattern.sub("// Security verified: client-side premium pass injection removed", html)

    # 2. SEO Title & Meta Description & remove keywords
    old_title_pattern = re.compile(r"<title>.*?</title>", re.DOTALL)
    html = old_title_pattern.sub("<title>Chaldean Name Numerology Calculator | Numeros Vision</title>", html, count=1)

    old_desc_pattern = re.compile(r'<meta\s+name="description"\s+content=".*?"\s*/>', re.DOTALL)
    html = old_desc_pattern.sub(
        '<meta name="description" content="Explore your name number using Chaldean numerology. Compare name calculations with your birth Driver and Conductor numbers and explore traditional interpretations." />',
        html,
        count=1
    )

    old_kw_pattern = re.compile(r'<meta\s+name="keywords"\s+content=".*?"\s*/>\s*', re.DOTALL)
    html = old_kw_pattern.sub('', html, count=1)

    # Open Graph & Twitter tags
    html = re.sub(
        r'<meta\s+property="og:url"\s+content=".*?"\s*/>',
        '<meta property="og:url" content="https://numerosvision.com/tools/name-balancing/" />',
        html
    )
    html = re.sub(
        r'<meta\s+property="og:title"\s+content=".*?"\s*/>',
        '<meta property="og:title" content="Chaldean Name Numerology Calculator | Numeros Vision" />',
        html
    )
    html = re.sub(
        r'<meta\s+property="og:description"\s+content=".*?"\s*/>',
        '<meta property="og:description" content="Explore your name number using Chaldean numerology. Compare name calculations with your birth Driver and Conductor numbers and explore traditional interpretations." />',
        html
    )
    html = re.sub(
        r'<meta\s+name="twitter:title"\s+content=".*?"\s*/>',
        '<meta name="twitter:title" content="Chaldean Name Numerology Calculator | Numeros Vision" />',
        html
    )
    html = re.sub(
        r'<meta\s+name="twitter:description"\s+content=".*?"\s*/>',
        '<meta name="twitter:description" content="Explore your name number using Chaldean numerology. Compare name calculations with your birth Driver and Conductor numbers and explore traditional interpretations." />',
        html
    )

    # 3. JSON-LD Structured Data
    new_json_ld = '''  <!-- JSON-LD Structured Data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "WebApplication",
        "name": "Chaldean Name Numerology Calculator",
        "description": "Calculate your name number using Chaldean numerology and compare it with your birth Driver and Conductor numbers.",
        "url": "https://numerosvision.com/tools/name-balancing/",
        "applicationCategory": "LifestyleApplication",
        "operatingSystem": "All",
        "offers": { "@type": "Offer", "price": "0", "priceCurrency": "INR" },
        "provider": { "@type": "Organization", "name": "Numeros Vision", "url": "https://numerosvision.com" }
      },
      {
        "@type": "BreadcrumbList",
        "itemListElement": [
          { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://numerosvision.com/" },
          { "@type": "ListItem", "position": 2, "name": "Calculators", "item": "https://numerosvision.com/calculators/" },
          { "@type": "ListItem", "position": 3, "name": "Chaldean Name Numerology", "item": "https://numerosvision.com/tools/name-balancing/" }
        ]
      },
      {
        "@type": "FAQPage",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "What is Chaldean name numerology?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Chaldean numerology is a traditional system originating in ancient Mesopotamia that assigns numbers from 1 to 8 to letters of the alphabet based on sound vibrations. The number 9 is considered sacred and not assigned to individual letters, though it can appear as a compound sum."
            }
          },
          {
            "@type": "Question",
            "name": "How is a Chaldean name number calculated?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Each letter in your full name is converted into its traditional Chaldean numerical value. The values are added together to produce a compound number (e.g., 23), which is then reduced by adding its digits together until a single root digit between 1 and 9 is reached (e.g., 2 + 3 = 5)."
            }
          },
          {
            "@type": "Question",
            "name": "Why does the Chaldean system exclude the number 9 from the alphabet?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "In classical Chaldean tradition, 9 is considered a complete and sacred number that disappears or returns to the original value when added to other single digits in modular arithmetic. It represents finality and is reserved for compound sums rather than individual letter values."
            }
          },
          {
            "@type": "Question",
            "name": "How do my birth numbers relate to my name number?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Your birth date produces two key numbers: your Driver (Mulank, derived from your day of birth) and your Conductor (Bhagyank, derived from the full birth date). In traditional numerology, a harmonious name number shares friendly planetary associations with both your Driver and Conductor numbers."
            }
          },
          {
            "@type": "Question",
            "name": "Do I need to change my legal name if my number is not aligned?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "No. Traditional numerologists emphasize that everyday usage—such as the name on your business cards, social profiles, email signatures, and daily correspondence—carries the primary social and practical frequency. Official legal changes are unnecessary for exploring traditional numerology adjustments."
            }
          },
          {
            "@type": "Question",
            "name": "Can a name change guarantee success or wealth?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "No. Numerology is a traditional symbolic discipline that explores archetypal associations and self-reflection. It does not provide scientific, medical, legal, or guaranteed financial outcomes. Any recommendations provide traditional perspectives to assist personal decision-making."
            }
          }
        ]
      }
    ]
  }
  </script>'''

    # Replace existing JSON-LD script
    json_ld_regex = re.compile(r'<!-- JSON-LD Structured Data -->\s*<script type="application/ld\+json">.*?</script>', re.DOTALL)
    html = json_ld_regex.sub(new_json_ld, html)

    # 4. Hero Section & AEO Box
    old_hero_aeo = re.compile(
        r'<!-- Hero Section -->.*?<!-- Centered, Aligned Calculator Form',
        re.DOTALL
    )

    new_hero_aeo = '''<!-- Hero Section -->
  <div class="tool-hero">
    <div class="tool-eyebrow">CHALDEAN NAME NUMEROLOGY</div>
    <h1 class="tool-title">Name Numerology Calculator &amp; Name Balancing</h1>
    <p class="tool-sub">
      Explore your name through Chaldean numerology. Enter your name and date of birth to calculate your name number and compare it with your birth numbers, where supported by the selected method. Understand the traditional interpretation of your results before considering spelling variations.
    </p>
  </div>

  <!-- AEO Quick Answer Box -->
  <div class="aeo-box">
    <h3>How Does Chaldean Name Numerology Work?</h3>
    <p>
      Chaldean numerology assigns numerical values from 1 to 8 to letters based on sound vibrations. The number 9 is considered sacred and unassigned to single letters. By summing the numerical values of the letters in your name, you calculate a compound number and a single-digit root number, which are traditionally compared with your birth Driver (Mulank) and Conductor (Bhagyank) numbers to evaluate classical harmony.
    </p>
  </div>

  <!-- Centered, Aligned Calculator Form'''

    html = old_hero_aeo.sub(new_hero_aeo, html)

    # 5. Form button label
    html = re.sub(
        r'<button type="submit" class="btn-calc" id="btn-submit">\s*<span>✦</span> Audit &amp; Balance Name\s*</button>',
        '<button type="submit" class="btn-calc" id="btn-submit">\n        <span>✦</span> Calculate My Name Number\n      </button>',
        html
    )

    # 6. Add Calculation Breakdown container in results right before planetary-diag-box
    calc_breakdown_html = '''      <!-- Transparent Calculation Breakdown Box -->
      <div id="calc-breakdown-box" style="display:none; background:var(--bg-mid); border:1.5px solid var(--border-gold); border-radius:14px; padding:20px 22px; margin-bottom:24px;">
        <div style="font-size:0.75rem; text-transform:uppercase; color:var(--gold-dark); font-weight:700; margin-bottom:12px; letter-spacing:0.06em;">
          ✦ Step-by-Step Chaldean Letter-to-Number Breakdown
        </div>
        <div id="breakdown-segments-container" style="display:flex; flex-direction:column; gap:10px; margin-bottom:14px;">
          <!-- Populated dynamically with each word's letter values -->
        </div>
        <div style="border-top:1px dashed var(--border); padding-top:12px; font-size:0.88rem; color:#523E28; display:flex; flex-wrap:wrap; justify-content:space-between; gap:10px;">
          <div>Full Compound: <strong id="breakdown-compound" style="color:#8B6914;">-</strong></div>
          <div>Root Reduction: <strong id="breakdown-reduction" style="color:#8B6914;">-</strong></div>
          <div>Planetary Association: <strong id="breakdown-planet" style="color:#8B6914;">-</strong></div>
        </div>
      </div>

'''
    if 'id="calc-breakdown-box"' not in html:
      html = html.replace(
          '<!-- Planetary Energy Balance Diagnostic',
          calc_breakdown_html + '      <!-- Planetary Energy Balance Diagnostic'
      )

    # 7. Aligned card wording (softer, authentic, no wild claims)
    old_aligned_header = '''      <div style="display:inline-flex;align-items:center;gap:6px;padding:4px 14px;border-radius:100px;background:rgba(22, 131, 91, 0.12);color:#16835B;font-size:0.78rem;font-weight:700;margin-bottom:12px;">
        ✓ NAME ENERGETICALLY ALIGNED WITH BIRTH BLUEPRINT
      </div>
      <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.85rem; color:#16835B; margin-bottom:10px;">
        Auspicious Planetary Resonance Confirmed
      </h3>
      <p style="font-size:0.94rem; color:var(--text-muted); line-height:1.7; max-width:640px; margin:0 auto 16px;">
        Your current name frequency harmonizes with your birth Driver and Conductor matrix. Auspicious planetary resonance confirmed with zero vibrational resistance. 
        Your name requires <strong>no structural alteration or phonetic rebalancing</strong>.
      </p>'''

    new_aligned_header = '''      <div style="display:inline-flex;align-items:center;gap:6px;padding:4px 14px;border-radius:100px;background:rgba(22, 131, 91, 0.12);color:#16835B;font-size:0.78rem;font-weight:700;margin-bottom:12px;">
        ✓ NAME HARMONIOUS UNDER TRADITIONAL CHALDEAN RULES
      </div>
      <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.85rem; color:#16835B; margin-bottom:10px;">
        Traditional Alignment Confirmed
      </h3>
      <p style="font-size:0.94rem; color:var(--text-muted); line-height:1.7; max-width:640px; margin:0 auto 16px;">
        Your current name number harmonizes with your birth Driver and Conductor numbers under classical Chaldean compatibility rules. 
        Traditional numerology indicates <strong>no spelling adjustments or modifications</strong> are necessary for this name.
      </p>'''

    html = html.replace(old_aligned_header, new_aligned_header)

    # 8. Unaligned card wording (responsible, clear, no scaremongering)
    old_unaligned_text = '''      <div style="display:inline-flex;align-items:center;gap:6px;padding:4px 14px;border-radius:100px;background:rgba(192, 57, 43, 0.12);color:#C0392B;font-size:0.78rem;font-weight:700;margin-bottom:12px;">
        ⚠️ NAME NOT ALIGNED · ENERGETIC FRICTION DETECTED
      </div>
      <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.75rem; color:#8B6914; margin-bottom:10px;">
        Consecrated 1-on-1 Name Balancing Consultation
      </h3>
      <p style="font-size:0.92rem; color:var(--text-muted); line-height:1.7; max-width:640px; margin:0 auto 16px;">
        Your name frequency creates energetic friction with your birth Driver or Conductor matrix. 
        In traditional spiritual science, <strong>name balancing is NEVER performed automatically by an app or algorithm</strong>. 
        Altering letters shifts subtle planetary vibrations governing your signature, career, and commercial destiny. 
        Authentic name balancing is calibrated exclusively by our Master Numerologists in a private 1-on-1 consultation.
      </p>

      <!-- Sanctuary Policy Notice -->
      <div style="display:inline-block; margin-bottom:22px; padding:12px 24px; border-radius:12px; background:rgba(201,162,39,0.08); border:1.5px dashed var(--border-gold); font-size:0.86rem; color:#8B6914; font-weight:600;">
        ✦ Sacred Sanctuary Policy: Name Balancing is Calibrated Exclusively in 1-on-1 Consultation. No Automated Modifications.
      </div>'''

    new_unaligned_text = '''      <div style="display:inline-flex;align-items:center;gap:6px;padding:4px 14px;border-radius:100px;background:rgba(192, 57, 43, 0.12);color:#C0392B;font-size:0.78rem;font-weight:700;margin-bottom:12px;">
        ⚠️ TRADITIONAL FRICTION IDENTIFIED UNDER CHALDEAN RULES
      </div>
      <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.75rem; color:#8B6914; margin-bottom:10px;">
        Personalized 1-on-1 Name Balancing Consultation
      </h3>
      <p style="font-size:0.92rem; color:var(--text-muted); line-height:1.7; max-width:640px; margin:0 auto 16px;">
        Under classical Chaldean numerology, your current name number creates planetary friction with your birth Driver or Conductor numbers. 
        Traditional numerologists recommend reviewing potential phonetic variations and assessing your daily signature with a qualified practitioner before making changes to public or professional correspondence.
      </p>

      <!-- Consultation Notice -->
      <div style="display:inline-block; margin-bottom:22px; padding:12px 24px; border-radius:12px; background:rgba(201,162,39,0.08); border:1.5px dashed var(--border-gold); font-size:0.86rem; color:#8B6914; font-weight:600;">
        ✦ In-Depth Analysis: Explore Auspicious Spelling Variations in a Personalized 1-on-1 Session.
      </div>'''

    html = html.replace(old_unaligned_text, new_unaligned_text)

    # 9. Insert Methodology block before FAQs
    methodology_block = '''  <!-- Transparent Methodology Section (GEO & AEO) -->
  <section class="methodology-section" style="max-width:820px; margin:40px auto 40px; padding:0 20px;">
    <div style="background:#FFFFFF; border:1.5px solid var(--border-gold); border-radius:18px; padding:30px 28px; box-shadow:0 6px 24px rgba(180, 155, 110, 0.08);">
      <div style="font-size:0.75rem; letter-spacing:0.14em; text-transform:uppercase; color:var(--gold-dark); font-weight:700; margin-bottom:8px;">
        ✦ TRANSPARENT CALCULATION PROCESS
      </div>
      <h2 style="font-family:'Cormorant Garamond',serif; font-size:1.85rem; color:#8B6914; margin:0 0 16px;">
        How Numeros Vision Analyses a Name
      </h2>
      <p style="font-size:0.92rem; color:var(--text-muted); line-height:1.7; margin-bottom:22px;">
        Numeros Vision uses a deterministic calculation engine rooted in classical Chaldean numerology to evaluate your name and birth numbers:
      </p>
      <div style="display:grid; grid-template-columns:1fr; gap:16px;">
        <div style="display:flex; gap:14px; align-items:flex-start;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:rgba(201,162,39,0.15); color:#8B6914; font-weight:700; font-size:0.85rem; flex-shrink:0;">1</span>
          <div>
            <strong style="color:var(--text-primary); font-size:0.92rem;">Enter your active name:</strong>
            <p style="margin:4px 0 0; font-size:0.86rem; color:var(--text-muted); line-height:1.6;">Use the exact spelling you commonly use in personal, professional, or social communications.</p>
          </div>
        </div>
        <div style="display:flex; gap:14px; align-items:flex-start;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:rgba(201,162,39,0.15); color:#8B6914; font-weight:700; font-size:0.85rem; flex-shrink:0;">2</span>
          <div>
            <strong style="color:var(--text-primary); font-size:0.92rem;">Derive your birth numbers:</strong>
            <p style="margin:4px 0 0; font-size:0.86rem; color:var(--text-muted); line-height:1.6;">Your date of birth determines your Driver (day reduced to 1–9) and Conductor (total date digits reduced to 1–9).</p>
          </div>
        </div>
        <div style="display:flex; gap:14px; align-items:flex-start;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:rgba(201,162,39,0.15); color:#8B6914; font-weight:700; font-size:0.85rem; flex-shrink:0;">3</span>
          <div>
            <strong style="color:var(--text-primary); font-size:0.92rem;">Map letters to Chaldean values:</strong>
            <p style="margin:4px 0 0; font-size:0.86rem; color:var(--text-muted); line-height:1.6;">Each character is mapped to values 1–8. Words are summed into segment compounds, and the total name compound is calculated and reduced to a root number.</p>
          </div>
        </div>
        <div style="display:flex; gap:14px; align-items:flex-start;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:rgba(201,162,39,0.15); color:#8B6914; font-weight:700; font-size:0.85rem; flex-shrink:0;">4</span>
          <div>
            <strong style="color:var(--text-primary); font-size:0.92rem;">Evaluate traditional planetary compatibility:</strong>
            <p style="margin:4px 0 0; font-size:0.86rem; color:var(--text-muted); line-height:1.6;">The name's ruling planet is compared against the ruling planets of your birth Driver and Conductor numbers to assess classical harmony.</p>
          </div>
        </div>
        <div style="display:flex; gap:14px; align-items:flex-start;">
          <span style="display:inline-flex; align-items:center; justify-content:center; width:28px; height:28px; border-radius:50%; background:rgba(201,162,39,0.15); color:#8B6914; font-weight:700; font-size:0.85rem; flex-shrink:0;">5</span>
          <div>
            <strong style="color:var(--text-primary); font-size:0.92rem;">Explore optional balancing options:</strong>
            <p style="margin:4px 0 0; font-size:0.86rem; color:var(--text-muted); line-height:1.6;">If traditional friction is identified, you can examine alternative phonetic spellings or consult a professional numerologist for personalised guidance.</p>
          </div>
        </div>
      </div>
    </div>
  </section>

'''

    # Replace FAQ section completely with 6 grounded FAQs
    old_faq_pattern = re.compile(
        r'<!-- Educational & FAQ Section for Search Engines -->.*?<!-- Master Footer -->',
        re.DOTALL
    )

    new_faq_html = '''<!-- Educational & FAQ Section for Search Engines -->
''' + methodology_block + '''  <section style="max-width:820px; margin:40px auto 80px; padding:0 20px;">
    <h2 style="font-family:'Cormorant Garamond',serif; font-size:2rem; color:#8B6914; text-align:center; margin-bottom:30px;">
      Frequently Asked Questions About Name Numerology
    </h2>
    <div style="display:flex; flex-direction:column; gap:16px;">
      <details style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
        <summary style="font-weight:700; color:#8B6914; cursor:pointer;">What is Chaldean name numerology?</summary>
        <p style="margin-top:10px; font-size:0.92rem; color:var(--text-muted); line-height:1.7;">
          Chaldean numerology is a traditional system originating in ancient Mesopotamia that assigns numbers from 1 to 8 to letters of the alphabet based on sound vibrations. The number 9 is considered sacred and not assigned to individual letters, though it can appear as a compound sum.
        </p>
      </details>
      <details style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
        <summary style="font-weight:700; color:#8B6914; cursor:pointer;">How is a Chaldean name number calculated?</summary>
        <p style="margin-top:10px; font-size:0.92rem; color:var(--text-muted); line-height:1.7;">
          Each letter in your full name is converted into its traditional Chaldean numerical value. The values are added together to produce a compound number (e.g., 23), which is then reduced by adding its digits together until a single root digit between 1 and 9 is reached (e.g., 2 + 3 = 5).
        </p>
      </details>
      <details style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
        <summary style="font-weight:700; color:#8B6914; cursor:pointer;">Why does the Chaldean system exclude the number 9 from the alphabet?</summary>
        <p style="margin-top:10px; font-size:0.92rem; color:var(--text-muted); line-height:1.7;">
          In classical Chaldean tradition, 9 is considered a complete and sacred number that disappears or returns to the original value when added to other single digits in modular arithmetic. It represents finality and is reserved for compound sums rather than individual letter values.
        </p>
      </details>
      <details style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
        <summary style="font-weight:700; color:#8B6914; cursor:pointer;">How do my birth numbers relate to my name number?</summary>
        <p style="margin-top:10px; font-size:0.92rem; color:var(--text-muted); line-height:1.7;">
          Your birth date produces two key numbers: your Driver (Mulank, derived from your day of birth) and your Conductor (Bhagyank, derived from the full birth date). In traditional numerology, a harmonious name number shares friendly planetary associations with both your Driver and Conductor numbers.
        </p>
      </details>
      <details style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
        <summary style="font-weight:700; color:#8B6914; cursor:pointer;">Do I need to change my legal name if my number is not aligned?</summary>
        <p style="margin-top:10px; font-size:0.92rem; color:var(--text-muted); line-height:1.7;">
          No. Traditional numerologists emphasize that everyday usage—such as the name on your business cards, social profiles, email signatures, and daily correspondence—carries the primary social and practical frequency. Official legal changes are unnecessary for exploring traditional numerology adjustments.
        </p>
      </details>
      <details style="background:#FFFFFF; border:1px solid var(--border); border-radius:12px; padding:16px 20px;">
        <summary style="font-weight:700; color:#8B6914; cursor:pointer;">Can a name change guarantee success or wealth?</summary>
        <p style="margin-top:10px; font-size:0.92rem; color:var(--text-muted); line-height:1.7;">
          No. Numerology is a traditional symbolic discipline that explores archetypal associations and self-reflection. It does not provide scientific, medical, legal, or guaranteed financial outcomes. Any recommendations provide traditional perspectives to assist personal decision-making.
        </p>
      </details>
    </div>
  </section>

  <!-- Master Footer -->'''

    html = old_faq_pattern.sub(new_faq_html, html)

    # 10. Update JavaScript logic:
    # - Ensure doProcessNameBalance has defensive API handling
    # - Render the calculation breakdown in renderResults
    # - Handle graceful fallback if nvProfileSync is not defined
    js_old_process = '''        try {
          const resp = await fetch('/api/v2/numerology/name/balance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              full_name: name,
              dob_str: dobVal,
              driver: driver,
              conductor: conductor
            })
          });
          const data = await resp.json();
          renderResults(data, driver, conductor, driverPlanet, conductorPlanet);
        } catch (err) {
          alert('Unable to complete calculation. Please verify your inputs and try again.');
          console.error(err);
        } finally {
          btn.innerHTML = '<span>✦</span> Audit &amp; Balance Name';
          btn.disabled = false;
        }
      };

      if (window.nvProfileSync && typeof window.nvProfileSync.requireConsentToReveal === 'function') {
        window.nvProfileSync.requireConsentToReveal(calcData, doProcessNameBalance, 'result-view');
      } else {
        const qp = new URLSearchParams(calcData).toString();
        window.location.href = '/signup/?source=calculator_gate&' + qp;
      
      }'''

    js_new_process = '''        try {
          const resp = await fetch('/api/v2/numerology/name/balance', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
              full_name: name,
              dob_str: dobVal,
              driver: driver,
              conductor: conductor
            })
          });
          if (!resp.ok) {
            throw new Error('API server returned status: ' + resp.status);
          }
          const data = await resp.json();
          if (!data || !data.current_name_evaluation) {
            throw new Error('Calculation response format unrecognized');
          }
          renderResults(data, driver, conductor, driverPlanet, conductorPlanet);
        } catch (err) {
          console.error('[Numeros Vision] Name balance error:', err);
          alert('Unable to complete calculation. Please verify your inputs and try again.');
        } finally {
          btn.innerHTML = '<span>✦</span> Calculate My Name Number';
          btn.disabled = false;
        }
      };

      if (window.nvProfileSync && typeof window.nvProfileSync.requireConsentToReveal === 'function') {
        window.nvProfileSync.requireConsentToReveal(calcData, doProcessNameBalance, 'result-view');
      } else {
        // Fallback: Proceed directly with calculation if sync script is not present
        doProcessNameBalance();
      }'''

    html = html.replace(js_old_process, js_new_process)

    # 11. Enhance renderResults in JavaScript to populate calculation breakdown
    old_render_start = '''    function renderResults(data, driver, conductor, driverPlanet, conductorPlanet) {
      document.getElementById('result-view').style.display = 'block';
      const evalData = data.current_name_evaluation;
      const seg = evalData.segment_analysis;'''

    new_render_start = '''    function renderResults(data, driver, conductor, driverPlanet, conductorPlanet) {
      document.getElementById('result-view').style.display = 'block';
      const evalData = data.current_name_evaluation || {};
      const seg = evalData.segment_analysis || {};

      // Populate Step-by-Step Breakdown
      const breakdownBox = document.getElementById('calc-breakdown-box');
      const segmentsCont = document.getElementById('breakdown-segments-container');
      if (breakdownBox && segmentsCont) {
        breakdownBox.style.display = 'block';
        segmentsCont.innerHTML = '';

        if (seg.segments && seg.segments.length > 0) {
          seg.segments.forEach(function(segment) {
            const letterItems = (segment.letter_breakdown || []).map(function(item) {
              return `<span style="display:inline-block; background:#FFFFFF; border:1px solid var(--border-gold); padding:2px 8px; border-radius:6px; font-size:0.82rem; margin:2px;"><strong>${item.letter}</strong>=${item.value}</span>`;
            }).join(' + ');

            const segRow = document.createElement('div');
            segRow.style.padding = '8px 12px';
            segRow.style.background = '#FFFFFF';
            segRow.style.borderRadius = '8px';
            segRow.style.border = '1px solid var(--border)';
            segRow.innerHTML = `
              <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:4px;">
                <span style="font-weight:700; color:#8B6914; font-size:0.88rem;">${segment.role || 'Word'}: "${segment.word}"</span>
                <span style="font-size:0.82rem; color:var(--text-faint);">${segment.reduction_path || segment.compound_sum} (${segment.planet || ''})</span>
              </div>
              <div style="font-size:0.84rem; color:#523E28; line-height:1.6;">${letterItems} = <strong>${segment.compound_sum}</strong> &rarr; <strong>${segment.root_number}</strong></div>
            `;
            segmentsCont.appendChild(segRow);
          });
        }

        document.getElementById('breakdown-compound').innerText = seg.full_compound || '-';
        document.getElementById('breakdown-reduction').innerText = seg.full_reduction_path || (seg.full_compound + ' \u2192 ' + seg.full_root);
        document.getElementById('breakdown-planet').innerText = seg.full_planet || '-';
      }'''

    html = html.replace(old_render_start, new_render_start)

    # 12. Update badge and verdict text inside renderResults
    old_badge_verdict = '''      const badge = document.getElementById('res-badge-score');
      if (isAligned) {
        badge.innerText = 'Vibrational Status: Aligned & Harmonious';
        badge.className = 'badge-score';
      } else {
        badge.innerText = 'Vibrational Status: Energetic Friction Detected';
        badge.className = 'badge-score danger';
      }

      document.getElementById('res-verdict-desc').innerText = isAligned
        ? 'Your current name frequency harmonizes with your birth Driver and Conductor matrix. Auspicious resonance confirmed.'
        : 'Your current name frequency creates active energetic friction with your birth matrix. Name balancing is calibrated exclusively via a private 1-on-1 consultation.';'''

    new_badge_verdict = '''      const badge = document.getElementById('res-badge-score');
      if (isAligned) {
        badge.innerText = 'Traditional Status: Aligned & Harmonious';
        badge.className = 'badge-score';
      } else {
        badge.innerText = 'Traditional Status: Friction Identified';
        badge.className = 'badge-score danger';
      }

      document.getElementById('res-verdict-desc').innerText = isAligned
        ? 'Under classical Chaldean guidelines, your name compound and root number share friendly planetary associations with your birth Driver and Conductor numbers.'
        : 'Under classical Chaldean guidelines, your name numbers create traditional friction with your birth numbers. Review the calculation breakdown below before considering spelling variations.';'''

    html = html.replace(old_badge_verdict, new_badge_verdict)

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(html)

    print('Successfully refined app/static/tools/name-balancing.html!')

if __name__ == '__main__':
    refine_name_balancing()
