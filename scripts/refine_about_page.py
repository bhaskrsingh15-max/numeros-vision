import sys
import re

def refine_about():
    sys.stdout.reconfigure(encoding='utf-8')
    path = 'app/static/about.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    print(f"Original length: {len(content)}")

    # 1. Page Title & Meta Description
    old_title = "<title>About Numeros Vision | Our Approach to Numerology</title>"
    new_title = "<title>About Numeros Vision | Our Methods &amp; Principles</title>"
    if old_title in content:
        content = content.replace(old_title, new_title, 1)
        print("Updated <title>")

    old_meta_desc = '<meta name="description" content="Learn about Numeros Vision\'s mission: uniting 6 classical occult traditions with classical mathematical algorithms and non-fear-based conversational AI guidance." />'
    new_meta_desc = '<meta name="description" content="Discover Numeros Vision, our approach to numerology calculators, name analysis, Lo Shu Grid insights and personalised reports, with transparent methods and responsible interpretation." />'
    if old_meta_desc in content:
        content = content.replace(old_meta_desc, new_meta_desc, 1)
        print("Updated meta description")

    # Remove deprecated meta keywords
    content = re.sub(r'\s*<meta name="keywords"[^>]*>', '', content)
    print("Removed deprecated meta keywords tag")

    # Open Graph & Twitter meta tags
    content = content.replace(
        '<meta property="og:title" content="About Numeros Vision | Our Approach to Numerology" />',
        '<meta property="og:title" content="About Numeros Vision | Our Methods &amp; Principles" />'
    )
    content = content.replace(
        '<meta property="og:description" content="Learn about Numeros Vision\'s mission: uniting 6 classical occult traditions with classical mathematical algorithms and non-fear-based conversational AI guidance." />',
        '<meta property="og:description" content="Discover Numeros Vision, our approach to numerology calculators, name analysis, Lo Shu Grid insights and personalised reports, with transparent methods and responsible interpretation." />'
    )
    content = content.replace(
        '<meta name="twitter:title" content="About Numeros Vision | Our Approach to Numerology" />',
        '<meta name="twitter:title" content="About Numeros Vision | Our Methods &amp; Principles" />'
    )
    content = content.replace(
        '<meta name="twitter:description" content="Learn about Numeros Vision\'s mission: uniting 6 classical occult traditions with classical mathematical algorithms and non-fear-based conversational AI guidance." />',
        '<meta name="twitter:description" content="Discover Numeros Vision, our approach to numerology calculators, name analysis, Lo Shu Grid insights and personalised reports, with transparent methods and responsible interpretation." />'
    )

    # 2. JSON-LD structured data: ensure URLs are /about/ consistently
    old_json_ld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "AboutPage",
        "@id": "https://numerosvision.com/about#webpage",
        "url": "https://numerosvision.com/about",
        "name": "About Numeros Vision | Our Approach to Numerology",
        "description": "Learn about Numeros Vision's mission: uniting 6 classical occult traditions with classical mathematical algorithms and non-fear-based conversational AI guidance.",
        "isPartOf": {
          "@id": "https://numerosvision.com/#website"
        },
        "about": {
          "@id": "https://numerosvision.com/#organization"
        },
        "breadcrumb": {
          "@id": "https://numerosvision.com/about#breadcrumb"
        }
      },
      {
        "@type": "BreadcrumbList",
        "@id": "https://numerosvision.com/about#breadcrumb",
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
            "name": "About Us",
            "item": "https://numerosvision.com/about"
          }
        ]
      }
    ]
  }
  </script>'''

    new_json_ld = '''  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@graph": [
      {
        "@type": "AboutPage",
        "@id": "https://numerosvision.com/about/#webpage",
        "url": "https://numerosvision.com/about/",
        "name": "About Numeros Vision | Our Methods & Principles",
        "description": "Discover Numeros Vision, our approach to numerology calculators, name analysis, Lo Shu Grid insights and personalised reports, with transparent methods and responsible interpretation.",
        "isPartOf": {
          "@id": "https://numerosvision.com/#website"
        },
        "about": {
          "@id": "https://numerosvision.com/#organization"
        },
        "breadcrumb": {
          "@id": "https://numerosvision.com/about/#breadcrumb"
        }
      },
      {
        "@type": "BreadcrumbList",
        "@id": "https://numerosvision.com/about/#breadcrumb",
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
            "name": "About Us",
            "item": "https://numerosvision.com/about/"
          }
        ]
      }
    ]
  }
  </script>'''

    if old_json_ld in content:
        content = content.replace(old_json_ld, new_json_ld, 1)
        print("Updated JSON-LD structured data with consistent canonical /about/ URLs")

    # 3. Add .hero-subtitle style in CSS
    old_css_needle = ".hero-desc { font-size: 1.05rem; color: var(--text-muted); max-width: 660px; margin: 0 auto; line-height: 1.7; }"
    new_css_needle = ".hero-subtitle { font-family: 'Cormorant Garamond', serif; font-size: clamp(1.35rem, 3vw, 1.8rem); font-weight: 400; color: #8B6914; line-height: 1.4; margin: 8px 0 14px; }\n    .hero-desc { font-size: 1.02rem; color: var(--text-muted); max-width: 720px; margin: 0 auto; line-height: 1.75; }"
    if old_css_needle in content:
        content = content.replace(old_css_needle, new_css_needle, 1)
        print("Added .hero-subtitle styling")

    # 4. Hero section markup
    old_hero_markup = '''    <div class="hero-sec">
      <span class="hero-eyebrow">ANCIENT MATHEMATICS · SOVEREIGN AI</span>
      <h1 class="hero-title">About Numeros Vision<br/><span style="font-size:0.62em;display:block;margin-top:8px;font-weight:400;color:var(--text-muted);">Bridging Wisdom with Absolute Precision</span></h1>
      <p class="hero-desc">
        Numeros Vision was born out of a profound conviction: that the sacred numerical sciences of antiquity deserve mathematical rigor, complete freedom from superstition, and the highest ethical data standards.
      </p>
    </div>'''

    new_hero_markup = '''    <div class="hero-sec">
      <span class="hero-eyebrow">✦ NUMEROLOGY METHODS · RESPONSIBLE INTERPRETATION ✦</span>
      <h1 class="hero-title">About Numeros Vision</h1>
      <p class="hero-subtitle">Traditional Numerology, Transparent Calculations</p>
      <p class="hero-desc">
        Numeros Vision brings traditional numerology methods into a clear, structured digital experience. Explore <a href="/calculators/" style="color:var(--gold-dark); text-decoration:underline; font-weight:600;">numerology calculators</a>, <a href="/tools/name-numerology" style="color:var(--gold-dark); text-decoration:underline; font-weight:600;">name analysis</a>, <a href="/tools/lo-shu-grid" style="color:var(--gold-dark); text-decoration:underline; font-weight:600;">Lo Shu Grid insights</a> and <a href="/reports/" style="color:var(--gold-dark); text-decoration:underline; font-weight:600;">personalised reports</a>, with explanations of the methods used to calculate your results.
      </p>
    </div>'''

    if old_hero_markup in content:
        content = content.replace(old_hero_markup, new_hero_markup, 1)
        print("Updated Hero section markup")

    # 5. Mission box
    old_mission_box = '''    <!-- The Mission Statement -->
    <div class="mission-box">
      <div class="mission-quote">"ANVEIL EVERY CHARM — To illuminate human potential through sacred numbers, without fatalism or fear."</div>
      <p class="mission-sub">
        For centuries, astrology and numerology were clouded by contradictory claims, generic horoscopes, and fear-based predictions.
        Numeros Vision replaces guesswork with authentic classical wisdom and mathematical rigor, providing you with honest, grounded perspectives and practical clarity for self-mastery.
      </p>
    </div>'''

    new_mission_box = '''    <!-- The Mission Statement -->
    <div class="mission-box">
      <div class="mission-quote">"ANVEIL EVERY CHARM — To illuminate human potential through traditional numbers, without fatalism or fear."</div>
      <p class="mission-sub">
        Our approach values transparency, responsible interpretation and respect for individual choice. Numerology is a traditional belief system, not a scientifically established way to predict a person's future.
        Numeros Vision replaces guesswork with verified calculation rules and clear explanations, providing honest perspectives and practical clarity for personal reflection.
      </p>
    </div>'''

    if old_mission_box in content:
        content = content.replace(old_mission_box, new_mission_box, 1)
        print("Updated Mission box")

    # 6. Three Core Foundational Pillars
    old_pillars = '''    <!-- 3 Core Foundational Pillars -->
    <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.2rem; color:#8B6914; text-align:center; margin-bottom:30px;">Our Three Pillars of Integrity</h2>
    <div class="pillars-grid">
      <div class="pillar-card">
        <div class="pillar-icon">📐</div>
        <h3 class="pillar-title">Authentic Rigor</h3>
        <p class="pillar-desc">
          Every reading is rooted in verified classical mathematics rather than subjective guesswork or artificial estimates. You receive dependable, transparent clarity every time.
        </p>
      </div>

      <div class="pillar-card">
        <div class="pillar-icon">🕊️</div>
        <h3 class="pillar-title">Empowering &amp; Non-Fatalistic</h3>
        <p class="pillar-desc">
          We reject the notion of cursed horoscopes. Challenging numbers represent growth opportunities to be understood and mastered through daily discipline, practical remedies, and mindful focus.
        </p>
      </div>

      <div class="pillar-card">
        <div class="pillar-icon">🛡️</div>
        <h3 class="pillar-title">Zero-Broker Data Privacy</h3>
        <p class="pillar-desc">
          Your birth date, personal questions, and life reflections are sacred. We protect them behind an encrypted, private vault physically isolated from AdTech networks and commercial data brokers.
        </p>
      </div>
    </div>'''

    new_pillars = '''    <!-- 3 Core Foundational Pillars -->
    <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.2rem; color:#8B6914; text-align:center; margin-bottom:30px;">Our Principles</h2>
    <div class="pillars-grid">
      <div class="pillar-card">
        <div class="pillar-icon">📐</div>
        <h3 class="pillar-title">Transparent Calculations</h3>
        <p class="pillar-desc">
          We explain the calculation method and show how your numerical result is derived. Where traditions differ, we identify the method used.
        </p>
      </div>

      <div class="pillar-card">
        <div class="pillar-icon">🕊️</div>
        <h3 class="pillar-title">Responsible Interpretation</h3>
        <p class="pillar-desc">
          Numerology interpretations are offered for reflection and self-understanding, not as fixed predictions. Your decisions remain your own.
        </p>
      </div>

      <div class="pillar-card">
        <div class="pillar-icon">🛡️</div>
        <h3 class="pillar-title">Privacy and Data Control</h3>
        <p class="pillar-desc">
          Your personal information deserves careful handling. Our <a href="/privacy/" style="color:#8B6914; text-decoration:underline;">Privacy Policy</a> explains what information we collect, how it is used, how it is retained and shared, and what choices are available to you.
        </p>
      </div>
    </div>'''

    if old_pillars in content:
        content = content.replace(old_pillars, new_pillars, 1)
        print("Updated Three Pillars of Integrity")

    # 7. Purpose & Promise -> Our Purpose
    old_purpose = '''    <!-- Our Purpose & Promise -->
    <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.2rem; color:#8B6914; margin-top:40px; margin-bottom:12px; text-align:center;">Our Purpose &amp; Promise</h2>
    <p style="font-size:0.95rem; color:#523E28; line-height:1.7; text-align:center; max-width:680px; margin:0 auto 32px;">
      Numeros Vision exists to provide clarity, inner balance, and mindful direction. We translate timeless numerical wisdom into practical guidance for your everyday personal and professional life.
    </p>

    <div class="pillars-grid" style="margin-bottom:40px;">
      <div class="pillar-card">
        <div class="pillar-icon">✨</div>
        <h3 class="pillar-title">Clarity in Decision-Making</h3>
        <p class="pillar-desc">
          Gain conscious perspective on your innate strengths, relationships, and natural life themes—free from ambiguity, fatalism, or fear.
        </p>
      </div>

      <div class="pillar-card">
        <div class="pillar-icon">⏳</div>
        <h3 class="pillar-title">Harmonious Life Timing</h3>
        <p class="pillar-desc">
          Understand natural cyclical rhythms to make career moves, creative pursuits, and life milestones with confidence and inner peace.
        </p>
      </div>

      <div class="pillar-card">
        <div class="pillar-icon">🌱</div>
        <h3 class="pillar-title">Actionable Self-Mastery</h3>
        <p class="pillar-desc">
          Receive grounded, everyday lifestyle adjustments and mindful habits designed to cultivate balance, focus, and authentic personal fulfillment.
        </p>
      </div>
    </div>'''

    new_purpose = '''    <!-- Our Purpose -->
    <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.2rem; color:#8B6914; margin-top:40px; margin-bottom:12px; text-align:center;">Our Purpose</h2>
    <p style="font-size:0.95rem; color:#523E28; line-height:1.75; text-align:center; max-width:680px; margin:0 auto 32px;">
      Numeros Vision helps people explore traditional numerology through accessible calculations, understandable interpretations and personalised reports.
    </p>

    <div class="pillars-grid" style="margin-bottom:40px;">
      <div class="pillar-card">
        <div class="pillar-icon">✨</div>
        <h3 class="pillar-title">Clarity in Personal Reflection</h3>
        <p class="pillar-desc">
          Explore numerical patterns and traditional interpretations without treating them as definitive judgments about your life.
        </p>
      </div>

      <div class="pillar-card">
        <div class="pillar-icon">⏳</div>
        <h3 class="pillar-title">Understanding Personal Cycles</h3>
        <p class="pillar-desc">
          Explore how numerology traditions interpret numbers associated with dates and personal cycles. Results depend on the selected method.
        </p>
      </div>

      <div class="pillar-card">
        <div class="pillar-icon">🌱</div>
        <h3 class="pillar-title">Practical, Non-Fatalistic Guidance</h3>
        <p class="pillar-desc">
          Use interpretations as prompts for reflection, while making important personal, health and financial decisions using appropriate evidence and professional advice.
        </p>
      </div>
    </div>'''

    if old_purpose in content:
        content = content.replace(old_purpose, new_purpose, 1)
        print("Updated Our Purpose section")

    # 8. Add Factual GEO / AIO Section: How Numeros Vision Works
    geo_aio_section = '''    <!-- How Numeros Vision Works (GEO / AIO) -->
    <div style="background:#FFFFFF; border:1.5px solid var(--border-gold); border-radius:18px; padding:30px 24px; margin:36px 0; box-shadow:0 6px 20px rgba(180,155,110,0.06);">
      <h2 style="font-family:'Cormorant Garamond',serif; font-size:2rem; color:#8B6914; margin:0 0 12px; text-align:center;">
        How Numeros Vision Works
      </h2>
      <p style="font-size:0.92rem; color:var(--text-muted); line-height:1.7; text-align:center; max-width:680px; margin:0 auto 20px;">
        Numeros Vision provides digital tools for exploring traditional numerology methods across Vedic, Chaldean, Pythagorean, and Lo Shu traditions.
      </p>
      <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:18px; margin-top:20px;">
        <div style="background:#FAF6EE; border-radius:12px; padding:18px;">
          <h4 style="color:#8B6914; font-size:1.1rem; margin:0 0 8px; font-family:'Cormorant Garamond',serif;">1. Deterministic Calculations</h4>
          <p style="font-size:0.85rem; color:var(--text-muted); line-height:1.65; margin:0;">
            Core numbers—including Driver (Mulank), Conductor (Bhagyank), Chaldean compound numbers, and Lo Shu 3×3 grids—are generated using defined mathematical rules. Where calculation conventions differ between traditions, the selected method is clearly identified.
          </p>
        </div>
        <div style="background:#FAF6EE; border-radius:12px; padding:18px;">
          <h4 style="color:#8B6914; font-size:1.1rem; margin:0 0 8px; font-family:'Cormorant Garamond',serif;">2. Traditional Interpretations</h4>
          <p style="font-size:0.85rem; color:var(--text-muted); line-height:1.65; margin:0;">
            Explanations describe traditional numerology perspectives and are intended for personal reflection and cycle awareness, not as scientifically validated predictions.
          </p>
        </div>
        <div style="background:#FAF6EE; border-radius:12px; padding:18px;">
          <h4 style="color:#8B6914; font-size:1.1rem; margin:0 0 8px; font-family:'Cormorant Garamond',serif;">3. Personalised Reports</h4>
          <p style="font-size:0.85rem; color:var(--text-muted); line-height:1.65; margin:0;">
            Users can explore additional interpretations, multi-year timing, and related numerical patterns through the <a href="/reports/" style="color:#8B6914; text-decoration:underline;">report options</a> available on the platform.
          </p>
        </div>
        <div style="background:#FAF6EE; border-radius:12px; padding:18px;">
          <h4 style="color:#8B6914; font-size:1.1rem; margin:0 0 8px; font-family:'Cormorant Garamond',serif;">4. Privacy and Data Security</h4>
          <p style="font-size:0.85rem; color:var(--text-muted); line-height:1.65; margin:0;">
            We operate under strict data minimization guidelines. Please review our <a href="/privacy/" style="color:#8B6914; text-decoration:underline;">Privacy Policy</a> for details about information collection, processing, retention, and sharing.
          </p>
        </div>
      </div>
    </div>

'''
    # Insert right before the Ethical Pledge
    target_ethics = '    <!-- Ethical Pledge -->'
    if target_ethics in content and 'How Numeros Vision Works' not in content:
        content = content.replace(target_ethics, geo_aio_section + target_ethics, 1)
        print("Inserted How Numeros Vision Works (GEO / AIO) section")

    # 9. Ethical pledge text
    old_ethics_text = '''      <p style="font-size:0.88rem; color:#523E28; line-height:1.7; margin:0;">
        We strictly abide by the Indian Drugs and Magic Remedies Act 1954 and Consumer Protection Regulations. We will never sell you "miracle curses", promise instant lottery winnings, or claim that numbers can replace licensed doctors, surgeons, certified accountants, or professional mental health therapists. Our purpose is clarity, empowerment, and self-mastery.
      </p>'''

    new_ethics_text = '''      <p style="font-size:0.88rem; color:#523E28; line-height:1.7; margin:0;">
        We strictly abide by consumer protection guidelines and the Indian Drugs and Magic Remedies (Objectionable Advertisements) Act 1954. We will never sell "miracle cures", promise financial windfalls, or claim that numbers can substitute for professional medical, legal, or financial advice. Our purpose is personal reflection, clarity, and self-empowerment.
      </p>'''

    if old_ethics_text in content:
        content = content.replace(old_ethics_text, new_ethics_text, 1)
        print("Updated Ethical Pledge text")

    # 10. Conversion CTA box
    old_cta_box = '''    <!-- Ready to Anveil Your Chart Conversion Showcase -->
    <div class="conversion-dossier-card" style="background:linear-gradient(135deg, rgba(201,162,39,0.08) 0%, rgba(22,131,91,0.06) 100%); border:1.5px solid var(--border-gold); border-radius:20px; padding:32px 26px; margin:40px 0 20px; text-align:center;">
      <span style="display:inline-block; font-size:0.72rem; letter-spacing:0.14em; text-transform:uppercase; color:#8B6914; font-weight:700; margin-bottom:8px;">Begin Your Journey With Clarity</span>
      <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.95rem; color:var(--text-primary); margin-bottom:12px;">
        ANVEIL Your Personal Destiny With Classical Vedic Precision
      </h3>
      <p style="font-size:0.92rem; color:var(--text-muted); line-height:1.7; max-width:640px; margin:0 auto 22px;">
        Classical numerology becomes truly transformative when calculated without human bias or algorithmic hallucination. Discover your inborn strengths, upcoming blessing cycles, and tailored remedies through our comprehensive dossiers or private sessions.
      </p>
      <div style="display:flex; justify-content:center; gap:14px; flex-wrap:wrap;">
        <a href="/reports/" class="btn-gold" style="text-decoration:none; padding:13px 26px; font-size:0.84rem; font-weight:700;">
          ✦ Explore Personalised Reports
        </a>
        <a href="/consultation/" class="btn-ghost" style="text-decoration:none; padding:13px 24px; font-size:0.84rem;">
          📞 Book 1-on-1 Consultation
        </a>
        <a href="/charm-ai/" style="display:inline-flex; align-items:center; padding:12px 18px; font-size:0.84rem; color:#8B6914; font-weight:600; text-decoration:none;">
          Ask Charm AI Free →
        </a>
      </div>
    </div>'''

    new_cta_box = '''    <!-- Conversion Showcase -->
    <div class="conversion-dossier-card" style="background:linear-gradient(135deg, rgba(201,162,39,0.08) 0%, rgba(22,131,91,0.06) 100%); border:1.5px solid var(--border-gold); border-radius:20px; padding:32px 26px; margin:40px 0 20px; text-align:center;">
      <span style="display:inline-block; font-size:0.72rem; letter-spacing:0.14em; text-transform:uppercase; color:#8B6914; font-weight:700; margin-bottom:8px;">Begin Your Journey With Clarity</span>
      <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.95rem; color:var(--text-primary); margin-bottom:12px;">
        ANVEIL Your Numbers With Transparent Calculations
      </h3>
      <p style="font-size:0.92rem; color:var(--text-muted); line-height:1.7; max-width:640px; margin:0 auto 22px;">
        Explore your numerical results, understand the calculation method, and discover traditional interpretations through our free calculators, detailed reports, or personalised consultations.
      </p>
      <div style="display:flex; justify-content:center; gap:14px; flex-wrap:wrap;">
        <a href="/reports/" class="btn-gold" style="text-decoration:none; padding:13px 26px; font-size:0.84rem; font-weight:700;">
          ✦ Explore Personalised Reports
        </a>
        <a href="/calculators/" class="btn-ghost" style="text-decoration:none; padding:13px 24px; font-size:0.84rem;">
          🔢 Free Calculators
        </a>
        <a href="/consultation/" class="btn-ghost" style="text-decoration:none; padding:13px 24px; font-size:0.84rem;">
          📞 1-on-1 Consultation
        </a>
      </div>
    </div>'''

    if old_cta_box in content:
        content = content.replace(old_cta_box, new_cta_box, 1)
        print("Updated Conversion CTA box")

    # 11. Footer description update
    content = content.replace(
        'AI-powered numerological intelligence combining authentic classical Vedic, Chaldean, and Lo Shu frameworks. ANVEIL EVERY CHARM with clarity, mathematical rigor, and ethical privacy.',
        'Transparent numerological calculations combining authentic classical Vedic, Chaldean, and Lo Shu frameworks. ANVEIL EVERY CHARM with clarity, mathematical rigor, and ethical privacy.'
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"Successfully refined {path}. New length: {len(content)}")

if __name__ == '__main__':
    refine_about()
