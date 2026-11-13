import sys
import re

def refine_life_path_page():
    sys.stdout.reconfigure(encoding='utf-8')
    path = 'app/static/tools/life-path-calculator.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original length: {len(content)}")

    # 1. Update Title and Meta
    old_title = "<title>Life Path Number Calculator | Free Birth Date Numerology</title>"
    new_title = "<title>Life Path Number Calculator & Meaning | Numeros Vision</title>"
    if old_title in content:
        content = content.replace(old_title, new_title, 1)
        print("Updated <title>")

    old_desc = '<meta name="description" content="Calculate your Life Path number from your birth date. See the calculation steps and explore its traditional numerology interpretation." />'
    new_desc = '<meta name="description" content="Discover your Life Path Number using your date of birth. Explore its traditional numerology meaning and see step-by-step arithmetic without pseudoscientific claims." />'
    if old_desc in content:
        content = content.replace(old_desc, new_desc, 1)
        print("Updated meta description")

    # Open Graph & Twitter meta
    content = content.replace(
        '<meta property="og:title" content="Life Path Number Calculator | Free Birth Date Numerology" />',
        '<meta property="og:title" content="Life Path Number Calculator & Meaning | Numeros Vision" />'
    )
    content = content.replace(
        '<meta property="og:description" content="Calculate your Life Path number from your birth date. See the calculation steps and explore its traditional numerology interpretation." />',
        f'<meta property="og:description" content="Discover your Life Path Number using your date of birth. Explore its traditional numerology meaning and see step-by-step arithmetic without pseudoscientific claims." />'
    )
    content = content.replace(
        '<meta name="twitter:title" content="Life Path Number Calculator | Free Birth Date Numerology" />',
        '<meta name="twitter:title" content="Life Path Number Calculator & Meaning | Numeros Vision" />'
    )
    content = content.replace(
        '<meta name="twitter:description" content="Calculate your Life Path number from your birth date. See the calculation steps and explore its traditional numerology interpretation." />',
        f'<meta name="twitter:description" content="Discover your Life Path Number using your date of birth. Explore its traditional numerology meaning and see step-by-step arithmetic without pseudoscientific claims." />'
    )

    # 2. Hero lead copy
    old_hero = '''  <!-- ───── TOOL HERO ───── -->
  <div class="tool-hero">
    <div class="tool-eyebrow">✦ Free Numerology Tool ✦</div>
    <h1 class="tool-title">Life Path Number Calculator</h1>
    <p class="tool-sub">
      Your Life Path number is calculated from your date of birth using a defined numerology method. Enter your birth date to calculate your number and explore its traditional interpretation.
    </p>
  </div>'''

    new_hero = '''  <!-- ───── TOOL HERO ───── -->
  <div class="tool-hero">
    <div class="tool-eyebrow">✦ Free Numerology Tool ✦</div>
    <h1 class="tool-title">Life Path Number Calculator</h1>
    <p class="tool-sub">
      Discover your Life Path Number using your date of birth. Explore its traditional numerology meaning and see how the number is calculated.
    </p>
  </div>'''

    if old_hero in content:
        content = content.replace(old_hero, new_hero, 1)
        print("Updated Tool Hero section")
    else:
        content = content.replace(
            '<p class="tool-sub">\n      Your Life Path number is calculated from your date of birth using a defined numerology method. Enter your birth date to calculate your number and explore its traditional interpretation.\n    </p>',
            '<p class="tool-sub">\n      Discover your Life Path Number using your date of birth. Explore its traditional numerology meaning and see how the number is calculated.\n    </p>'
        )
        print("Updated Tool Hero sub via replace")

    # 3. Calculation button label
    content = content.replace(
        '<button class="btn-calc" onclick="calculateLifePath()">✦ Calculate My Life Path Number</button>',
        '<button class="btn-calc" onclick="calculateLifePath()">Calculate My Life Path Number ✦</button>'
    )

    # 4. Result card: add step-by-step breakdown container
    old_res_diag = '<div id="res-diagnostics" style="margin-top:20px;text-align:left;"></div>'
    new_res_diag = '''<div id="res-calc-steps" style="margin-top:20px;text-align:left;"></div>
      <div id="res-diagnostics" style="margin-top:16px;text-align:left;"></div>'''
    if old_res_diag in content:
        content = content.replace(old_res_diag, new_res_diag, 1)
        print("Added res-calc-steps container")

    # 5. Verified report box in result container
    old_rep_summary_box = '''    <!-- Verified Report Upgrade Box -->
    <div class="reports-summary-box">
      <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--gold-dark); margin-bottom:6px; display:inline-block;">Verified Dossier</span>
      <h3>Explore Your Detailed Life Path Report</h3>
      <p>
        Your free calculation provides your core Life Path number and primary archetype. A detailed report delivers an in-depth analysis of your Driver and Conductor harmony, 8-plane Lo Shu grid, and multi-year cycle transitions.
      </p>
      <div style="margin-bottom:18px;">
        <span style="font-size:1.5rem; font-weight:800; color:var(--gold-dark);">&#8377;510</span>
        <span style="font-size:0.85rem; color:var(--text-muted);">/ $14.00 (12-Page Advanced Report)</span>
      </div>
      <a href="/reports/" class="btn-report-cta">Explore Your Life Path Report ✦</a>
      <div style="font-size:0.75rem; color:var(--text-muted); margin-top:10px;">
        Instant PDF Delivery &bull; Deterministic Engine Precision &bull; Confidential &amp; Secure
      </div>
    </div>'''

    new_rep_summary_box = '''    <!-- Verified Report Upgrade Box -->
    <div class="reports-summary-box">
      <span style="font-size:0.7rem; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; color:var(--gold-dark); margin-bottom:6px; display:inline-block;">Detailed Report</span>
      <h3>Explore Your Detailed Life Path Report</h3>
      <p>
        Want to explore your result further? A detailed report can provide additional interpretations and related numerology analysis based on the selected product.
      </p>
      <div style="margin-bottom:18px;">
        <span style="font-size:1.5rem; font-weight:800; color:var(--gold-dark);">&#8377;510</span>
        <span style="font-size:0.85rem; color:var(--text-muted);">/ $14.00 (12-Page Advanced Report)</span>
      </div>
      <a href="/reports/" class="btn-report-cta">Explore Life Path Reports ✦</a>
      <div style="font-size:0.75rem; color:var(--text-muted); margin-top:10px;">
        Instant PDF Delivery &bull; Deterministic Engine Precision &bull; Confidential &amp; Secure
      </div>
    </div>'''

    if old_rep_summary_box in content:
        content = content.replace(old_rep_summary_box, new_rep_summary_box, 1)
        print("Updated reports-summary-box")

    # 6. Supporting Content (How is it calculated, What does it mean, Explore reports)
    old_supporting_content = '''  <!-- ───── CONCISE SUPPORTING CONTENT ───── -->
  <main class="tool-content-wrap">
    <h2>How Is Your Life Path Number Calculated?</h2>
    <p>
      Your birth date is processed using the calculation method selected by the calculator. The resulting number is reduced according to that method's rules. Review the steps to see how your result was obtained.
    </p>

    <div class="calc-steps-box">
      <h3 style="margin-top:0; color:var(--gold-dark); font-size:1.15rem;">Example Calculation: 15 June 1990</h3>
      <p style="font-size:0.9rem; color:var(--text-muted); margin-bottom:14px;">
        Here is how the standard component reduction method calculates the Life Path for <strong>15/06/1990</strong>:
      </p>
      <div class="step-item">
        <div class="step-badge">1</div>
        <div class="step-text"><strong>Reduce the Day:</strong> 15 &rarr; 1 + 5 = <strong>6</strong></div>
      </div>
      <div class="step-item">
        <div class="step-badge">2</div>
        <div class="step-text"><strong>Reduce the Month:</strong> June = 06 &rarr; <strong>6</strong></div>
      </div>
      <div class="step-item">
        <div class="step-badge">3</div>
        <div class="step-text"><strong>Reduce the Year:</strong> 1990 &rarr; 1 + 9 + 9 + 0 = 19 &rarr; 1 + 9 = 10 &rarr; 1 + 0 = <strong>1</strong></div>
      </div>
      <div class="step-item">
        <div class="step-badge">4</div>
        <div class="step-text"><strong>Sum &amp; Reduce:</strong> 6 + 6 + 1 = <strong>13</strong> &rarr; 1 + 3 = <strong>4</strong> (Life Path 4)</div>
      </div>
      <p style="font-size:0.85rem; color:var(--text-muted); margin:12px 0 0;">
        <em>Alternative reduction:</em> Direct full-digit addition (1+5+0+6+1+9+9+0 = 31 &rarr; 4) arrives at the identical root number 4, with 31 as the intermediate compound instead of 13.
      </p>
    </div>

    <h2>What Does Your Life Path Number Mean?</h2>
    <p>
      In numerology, each Life Path number is associated with traditional themes and interpretations. These meanings vary between systems and should be understood as symbolic interpretations, not scientifically proven predictions.
    </p>
    <ul>
      <li><strong>Numbers 1 to 9:</strong> Form the foundational archetypes—ranging from independent leadership (1) and diplomatic balance (2) to structural discipline (4) and compassionate completion (9).</li>
      <li><strong>Master Numbers (11, 22, 33):</strong> Represent intensified traditional symbolic themes that many practitioners analyze both in their compound double-digit form and as reduced root numbers (2, 4, 6).</li>
    </ul>

    <h2>Explore Your Detailed Life Path Report</h2>
    <p>
      Your free result gives you the calculated number and an initial interpretation. A detailed report can provide additional analysis and relevant number relationships supported by the selected product.
    </p>
    <p>
      Our structured report packages extend your calculation with complete 8-plane Lo Shu grid assessments, Driver and Conductor polarity evaluations, and personal cycle projections:
    </p>

    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin:20px 0 24px;">
      <div style="background:#FFFFFF; border:1px solid var(--border-gold); border-radius:12px; padding:18px; text-align:center;">
        <div style="font-size:0.7rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase;">Basic Report</div>
        <div style="font-size:1.3rem; font-weight:800; color:var(--gold-dark); margin:4px 0;">&#8377;199 <span style="font-size:0.75rem; font-weight:400; color:var(--text-muted);">/ $5</span></div>
        <div style="font-size:0.82rem; color:var(--text-muted);">3 Pages &bull; Core Driver &amp; Life Path Analysis</div>
      </div>
      <div style="background:#FFFDF7; border:2px solid var(--gold-dark); border-radius:12px; padding:18px; text-align:center;">
        <div style="font-size:0.7rem; font-weight:700; color:#16835B; text-transform:uppercase;">✦ Advanced Report</div>
        <div style="font-size:1.3rem; font-weight:800; color:var(--gold-dark); margin:4px 0;">&#8377;510 <span style="font-size:0.75rem; font-weight:400; color:var(--text-muted);">/ $14</span></div>
        <div style="font-size:0.82rem; color:var(--text-muted);">12 Pages &bull; Lo Shu Grid &amp; Multi-Year Cycles</div>
      </div>
      <div style="background:#FFFFFF; border:1px solid var(--border-gold); border-radius:12px; padding:18px; text-align:center;">
        <div style="font-size:0.7rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase;">Premium Report</div>
        <div style="font-size:1.3rem; font-weight:800; color:var(--gold-dark); margin:4px 0;">&#8377;1,050 <span style="font-size:0.75rem; font-weight:400; color:var(--text-muted);">/ $28</span></div>
        <div style="font-size:0.82rem; color:var(--text-muted);">32 Pages &bull; Full Synthesis Master Dossier</div>
      </div>
    </div>

    <div style="text-align:center; margin-top:14px;">
      <a href="/reports/" class="btn-report-cta">Explore Your Life Path Report ✦</a>
    </div>
  </main>'''

    new_supporting_content = '''  <!-- ───── CONCISE SUPPORTING CONTENT ───── -->
  <main class="tool-content-wrap">
    <h2>How Is Your Life Path Number Calculated?</h2>
    <p>
      Your Life Path Number is calculated from your full date of birth. The result depends on the numerology method selected.
    </p>

    <div class="calc-steps-box">
      <h3 style="margin-top:0; color:var(--gold-dark); font-size:1.15rem;">Example: 15 June 1990</h3>
      <div class="step-item">
        <div class="step-badge">1</div>
        <div class="step-text"><strong>Day:</strong> 1 + 5 = <strong>6</strong></div>
      </div>
      <div class="step-item">
        <div class="step-badge">2</div>
        <div class="step-text"><strong>Month:</strong> June = <strong>6</strong></div>
      </div>
      <div class="step-item">
        <div class="step-badge">3</div>
        <div class="step-text"><strong>Year:</strong> 1 + 9 + 9 + 0 = 19 &rarr; 1 + 9 = 10 &rarr; 1 + 0 = <strong>1</strong></div>
      </div>
      <div class="step-item">
        <div class="step-badge">4</div>
        <div class="step-text"><strong>Total:</strong> 6 + 6 + 1 = 13 &rarr; 1 + 3 = <strong>4</strong></div>
      </div>
      <div style="margin-top:12px; font-weight:700; color:#8B6914; font-size:0.95rem;">
        Result: Life Path Number 4
      </div>
      <p style="font-size:0.85rem; color:var(--text-muted); margin:12px 0 0; line-height:1.6;">
        This example uses component reduction. Other numerology methods may handle intermediate numbers differently, so your calculator should clearly identify the method it actually uses.
      </p>
    </div>

    <h2>What Does Your Life Path Number Mean?</h2>
    <p>
      In numerology, each number is associated with traditional symbolic meanings. Your result offers a starting point for exploring these interpretations. They are part of a belief-based tradition, not scientifically established predictions.
    </p>
    <p>
      Your free result includes your calculated number and a brief interpretation. Explore a detailed report for additional analysis, where available.
    </p>

    <h2>Explore Your Detailed Life Path Report</h2>
    <p>
      Want to explore your result further? A detailed report can provide additional interpretations and related numerology analysis based on the selected product.
    </p>

    <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:14px; margin:20px 0 24px;">
      <div style="background:#FFFFFF; border:1px solid var(--border-gold); border-radius:12px; padding:18px; text-align:center;">
        <div style="font-size:0.7rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase;">Basic Report</div>
        <div style="font-size:1.3rem; font-weight:800; color:var(--gold-dark); margin:4px 0;">&#8377;199 <span style="font-size:0.75rem; font-weight:400; color:var(--text-muted);">/ $5.00</span></div>
        <div style="font-size:0.82rem; color:var(--text-muted);">3 Pages &bull; Core Driver &amp; Life Path Analysis</div>
      </div>
      <div style="background:#FFFDF7; border:2px solid var(--gold-dark); border-radius:12px; padding:18px; text-align:center;">
        <div style="font-size:0.7rem; font-weight:700; color:#16835B; text-transform:uppercase;">✦ Advanced Report (Most Popular)</div>
        <div style="font-size:1.3rem; font-weight:800; color:var(--gold-dark); margin:4px 0;">&#8377;510 <span style="font-size:0.75rem; font-weight:400; color:var(--text-muted);">/ $14.00</span></div>
        <div style="font-size:0.82rem; color:var(--text-muted);">12 Pages &bull; Lo Shu Grid &amp; Multi-Year Cycles</div>
      </div>
      <div style="background:#FFFFFF; border:1px solid var(--border-gold); border-radius:12px; padding:18px; text-align:center;">
        <div style="font-size:0.7rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase;">Premium Report</div>
        <div style="font-size:1.3rem; font-weight:800; color:var(--gold-dark); margin:4px 0;">&#8377;1,050 <span style="font-size:0.75rem; font-weight:400; color:var(--text-muted);">/ $28.00</span></div>
        <div style="font-size:0.82rem; color:var(--text-muted);">32 Pages &bull; Complete Master Destiny Blueprint</div>
      </div>
    </div>

    <div style="text-align:center; margin-top:14px;">
      <a href="/reports/" class="btn-report-cta">Explore Life Path Reports ✦</a>
    </div>
  </main>'''

    if old_supporting_content in content:
        content = content.replace(old_supporting_content, new_supporting_content, 1)
        print("Updated supporting content section")
    else:
        print("Warning: old_supporting_content not matched directly, attempting targeted replaces")

    # 7. FAQs (Visible HTML)
    old_faqs_html = '''    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">What is a Life Path number? <span>+</span></div>
      <div class="faq-a">Your Life Path number is a core numerology number calculated from your full date of birth. It represents traditional symbolic themes, natural tendencies, and life lessons associated with your birth date.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">How is my Life Path number calculated? <span>+</span></div>
      <div class="faq-a">Your day, month, and year of birth are reduced to single digits (or master numbers 11, 22, 33), added together, and reduced again to arrive at a single root number from 1 to 9.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">What do Life Path numbers 1 to 9 mean? <span>+</span></div>
      <div class="faq-a">Each number from 1 to 9 represents a classical archetype in traditional numerology—such as leadership for 1, diplomacy for 2, creative expression for 3, and discipline for 4. These are symbolic interpretations rather than deterministic predictions.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">What are master numbers in numerology? <span>+</span></div>
      <div class="faq-a">Master numbers are double digits (11, 22, and 33) that carry amplified traditional symbolic significance. In many numerology methods, they are preserved without immediate reduction to single digits.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">Does the calculation method affect my result? <span>+</span></div>
      <div class="faq-a">Different reduction conventions (such as component reduction vs. direct digit addition) always produce the same final single-digit root, but can produce different intermediate compound numbers (for example, 13 vs. 31).</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">What does a detailed Life Path report include? <span>+</span></div>
      <div class="faq-a">A detailed Life Path report provides multi-page personalized analysis beyond the free calculator summary. It explores Driver and Conductor harmony, personal year cycles, and deeper traditional interpretations.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">Which Life Path Number is most powerful? <span>+</span></div>
      <div class="faq-a">Numerology traditions do not establish one universally superior or most powerful number. Every number from 1 to 9 and each master number carries distinct strengths, challenges, and symbolic attributes.</div>
    </div>'''

    new_faqs_html = '''    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">What is a Life Path Number? <span>+</span></div>
      <div class="faq-a">A Life Path Number is a numerology number calculated from a person's date of birth using a specified method.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">How is my Life Path Number calculated? <span>+</span></div>
      <div class="faq-a">The calculator applies its stated method to your birth date and shows the calculation steps.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">Do Life Path Numbers have scientifically proven meanings? <span>+</span></div>
      <div class="faq-a">Numerology is a traditional interpretive practice. Its personality descriptions and predictions are not scientifically established facts.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">Does the calculation method affect my result? <span>+</span></div>
      <div class="faq-a">It can. Different systems may use different reduction rules, so check which method the calculator follows.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">What does a detailed Life Path report include? <span>+</span></div>
      <div class="faq-a">The contents depend on the report you select. Review the listed features before purchasing.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">What are Master Numbers (11, 22, 33)? <span>+</span></div>
      <div class="faq-a">Master numbers are double digits (11, 22, 33) that carry amplified traditional symbolic significance and are preserved without immediate reduction in many traditions.</div>
    </div>
    <div class="faq-item">
      <div class="faq-q" onclick="toggleFaq(this)">Is this Life Path calculator free? <span>+</span></div>
      <div class="faq-a">Yes. Calculating your number, viewing your calculation steps, and reading the initial interpretation are completely free. Extended multi-page reports are optional purchases.</div>
    </div>'''

    if old_faqs_html in content:
        content = content.replace(old_faqs_html, new_faqs_html, 1)
        print("Updated visible FAQs HTML")

    # 8. FAQs in JSON-LD
    old_faq_ld = '''        "@type": "FAQPage",
        "@id": "https://numerosvision.com/tools/life-path-calculator#faq",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "What is a Life Path number?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Your Life Path number is a core numerology number calculated from your full date of birth. It represents traditional symbolic themes, natural tendencies, and life lessons associated with your birth date."
            }
          },
          {
            "@type": "Question",
            "name": "How is my Life Path number calculated?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Your day, month, and year of birth are reduced to single digits (or master numbers 11, 22, 33), added together, and reduced again to arrive at a single root number from 1 to 9."
            }
          },
          {
            "@type": "Question",
            "name": "What do Life Path numbers 1 to 9 mean?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Each number from 1 to 9 represents a classical archetype in traditional numerology—such as leadership for 1, diplomacy for 2, creative expression for 3, and discipline for 4. These are symbolic interpretations rather than deterministic predictions."
            }
          },
          {
            "@type": "Question",
            "name": "What are master numbers in numerology?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Master numbers are double digits (11, 22, and 33) that carry amplified traditional symbolic significance. In many numerology methods, they are preserved without immediate reduction to single digits."
            }
          },
          {
            "@type": "Question",
            "name": "Does the calculation method affect my result?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Different reduction conventions (such as component reduction vs. direct digit addition) always produce the same final single-digit root, but can produce different intermediate compound numbers (for example, 13 vs. 31)."
            }
          },
          {
            "@type": "Question",
            "name": "What does a detailed Life Path report include?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "A detailed Life Path report provides multi-page personalized analysis beyond the free calculator summary. It explores Driver and Conductor harmony, personal year cycles, and deeper traditional interpretations."
            }
          },
          {
            "@type": "Question",
            "name": "Which Life Path Number is most powerful?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Numerology traditions do not establish one universally superior or most powerful number. Every number from 1 to 9 and each master number carries distinct strengths, challenges, and symbolic attributes."
            }
          }
        ]'''

    new_faq_ld = '''        "@type": "FAQPage",
        "@id": "https://numerosvision.com/tools/life-path-calculator#faq",
        "mainEntity": [
          {
            "@type": "Question",
            "name": "What is a Life Path Number?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "A Life Path Number is a numerology number calculated from a person's date of birth using a specified method."
            }
          },
          {
            "@type": "Question",
            "name": "How is my Life Path Number calculated?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "The calculator applies its stated method to your birth date and shows the calculation steps."
            }
          },
          {
            "@type": "Question",
            "name": "Do Life Path Numbers have scientifically proven meanings?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Numerology is a traditional interpretive practice. Its personality descriptions and predictions are not scientifically established facts."
            }
          },
          {
            "@type": "Question",
            "name": "Does the calculation method affect my result?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "It can. Different systems may use different reduction rules, so check which method the calculator follows."
            }
          },
          {
            "@type": "Question",
            "name": "What does a detailed Life Path report include?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "The contents depend on the report you select. Review the listed features before purchasing."
            }
          },
          {
            "@type": "Question",
            "name": "What are Master Numbers (11, 22, 33)?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Master numbers are double digits (11, 22, 33) that carry amplified traditional symbolic significance and are preserved without immediate reduction in many traditions."
            }
          },
          {
            "@type": "Question",
            "name": "Is this Life Path calculator free?",
            "acceptedAnswer": {
              "@type": "Answer",
              "text": "Yes. Calculating your number, viewing your calculation steps, and reading the initial interpretation are completely free. Extended multi-page reports are optional purchases."
            }
          }
        ]'''

    if old_faq_ld in content:
        content = content.replace(old_faq_ld, new_faq_ld, 1)
        print("Updated JSON-LD FAQPage")

    # 9. Update doRenderLifePath JavaScript to build user's live calculation steps
    old_render_js = '''      document.getElementById('res-diagnostics').innerHTML = `
        <div style="background:rgba(201,162,39,0.04);border:1px solid var(--border-gold);border-radius:14px;padding:16px;margin-bottom:16px;">
          <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.08em;color:#8B6914;font-weight:700;margin-bottom:8px;">
            ✦ Planetary Matrix Diagnostics
          </div>
          <div style="font-size:0.82rem;color:var(--text-primary);line-height:1.6;margin-bottom:6px;">
            <strong>Driver (Birth Day):</strong> ${driver} &nbsp;|&nbsp; <strong>Conductor (Life Path):</strong> ${lp} &nbsp;|&nbsp; <strong>Alignment:</strong> <span style="color:${alignmentColor};font-weight:700;">${alignmentStatus}</span>
          </div>
          <div style="font-size:0.82rem;color:var(--text-muted);line-height:1.6;margin-bottom:6px;">
            <strong>Missing Energies:</strong> ${missing.length > 0 ? missing.map(n=>`${n} (${PLANETS[n].split('·')[0].trim()})`).join(', ') : 'None (Full Matrix)'}
          </div>
          <div style="font-size:0.82rem;color:var(--text-muted);line-height:1.6;">
            <strong>Repetitive Energies:</strong> ${repeating.length > 0 ? repeating.map(n=>`${n} (×${counts[n]} - ${PLANETS[n].split('·')[0].trim()})`).join(', ') : 'None'}
          </div>
        </div>
      `;'''

    new_render_js = '''      // Build user's actual step-by-step arithmetic breakdown
      const monthNames = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
      const dDigits = String(d).split('').map(Number);
      const dStep = dDigits.length > 1 ? `${dDigits.join(' + ')} = ${reduce(d)}` : `${d}`;
      
      const mDigits = String(m).split('').map(Number);
      const mStep = mDigits.length > 1 ? `${mDigits.join(' + ')} = ${reduce(m)}` : `${m}`;
      
      const yDigits = String(y).split('').map(Number);
      const ySum1 = yDigits.reduce((acc, v) => acc + v, 0);
      const ySum1Digits = String(ySum1).split('').map(Number);
      let yStep = `${yDigits.join(' + ')} = ${ySum1}`;
      if (ySum1Digits.length > 1) {
        const ySum2 = ySum1Digits.reduce((acc, v) => acc + v, 0);
        yStep += ` &rarr; ${ySum1Digits.join(' + ')} = ${ySum2}`;
        const ySum2Digits = String(ySum2).split('').map(Number);
        if (ySum2Digits.length > 1) {
          yStep += ` &rarr; ${ySum2Digits.join(' + ')} = ${ySum2Digits.reduce((a,b)=>a+b,0)}`;
        }
      }

      const rd = reduce(d);
      const rm = reduce(m);
      const ry = reduce(y);
      const totalSum = rd + rm + ry;
      const totalDigits = String(totalSum).split('').map(Number);
      let totalStep = `${rd} + ${rm} + ${ry} = ${totalSum}`;
      if (totalDigits.length > 1 && totalSum !== 11 && totalSum !== 22 && totalSum !== 33) {
        totalStep += ` &rarr; ${totalDigits.join(' + ')} = ${lp}`;
      }

      const stepsContainer = document.getElementById('res-calc-steps');
      if (stepsContainer) {
        stepsContainer.innerHTML = `
          <div style="background:rgba(201,162,39,0.05);border:1px solid var(--border-gold);border-radius:14px;padding:18px;margin-bottom:14px;">
            <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.08em;color:#8B6914;font-weight:700;margin-bottom:8px;">
              ✦ Your Calculation Steps (Classical Component Reduction)
            </div>
            <div style="font-size:0.85rem;color:var(--text-primary);line-height:1.75;">
              <div><strong>Input Date:</strong> ${String(d).padStart(2,'0')} ${monthNames[m]} ${y}</div>
              <div><strong>Day:</strong> ${d} &rarr; ${dStep}</div>
              <div><strong>Month:</strong> ${monthNames[m]} (${m}) &rarr; ${mStep}</div>
              <div><strong>Year:</strong> ${y} &rarr; ${yStep}</div>
              <div><strong>Total:</strong> ${totalStep}</div>
              <div style="margin-top:6px;font-weight:700;color:var(--gold-dark);font-size:0.92rem;">
                Result: Life Path Number ${lp}
              </div>
            </div>
            <div style="font-size:0.75rem;color:var(--text-muted);margin-top:8px;line-height:1.5;">
              Method: Component reduction. Each date part is reduced individually before summing to identify both the primary root and intermediate compound numbers.
            </div>
          </div>
        `;
      }

      document.getElementById('res-diagnostics').innerHTML = `
        <div style="background:rgba(201,162,39,0.04);border:1px solid var(--border-gold);border-radius:14px;padding:16px;margin-bottom:16px;">
          <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.08em;color:#8B6914;font-weight:700;margin-bottom:8px;">
            ✦ Planetary Matrix Diagnostics
          </div>
          <div style="font-size:0.82rem;color:var(--text-primary);line-height:1.6;margin-bottom:6px;">
            <strong>Driver (Birth Day):</strong> ${driver} &nbsp;|&nbsp; <strong>Conductor (Life Path):</strong> ${lp} &nbsp;|&nbsp; <strong>Alignment:</strong> <span style="color:${alignmentColor};font-weight:700;">${alignmentStatus}</span>
          </div>
          <div style="font-size:0.82rem;color:var(--text-muted);line-height:1.6;margin-bottom:6px;">
            <strong>Missing Energies:</strong> ${missing.length > 0 ? missing.map(n=>`${n} (${PLANETS[n].split('·')[0].trim()})`).join(', ') : 'None (Full Matrix)'}
          </div>
          <div style="font-size:0.82rem;color:var(--text-muted);line-height:1.6;">
            <strong>Repetitive Energies:</strong> ${repeating.length > 0 ? repeating.map(n=>`${n} (×${counts[n]} - ${PLANETS[n].split('·')[0].trim()})`).join(', ') : 'None'}
          </div>
        </div>
      `;'''

    if old_render_js in content:
        content = content.replace(old_render_js, new_render_js, 1)
        print("Updated doRenderLifePath JavaScript with live step-by-step arithmetic")
    else:
        print("Warning: old_render_js not matched directly")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully refined {path}. New length: {len(content)}")

if __name__ == '__main__':
    refine_life_path_page()
