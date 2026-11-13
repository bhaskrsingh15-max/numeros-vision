import os

with open('scripts/extracted_header.html', 'r', encoding='utf-8') as f:
    header = f.read()

with open('scripts/extracted_footer.html', 'r', encoding='utf-8') as f:
    footer = f.read()

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0" />

  <!-- Standardized Favicon & Brand Touch Icons -->
  <link rel="icon" type="image/svg+xml" href="/logos/nv-logo-mark.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="/static/icons/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/static/icons/favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/static/icons/apple-touch-icon.png" />
  <link rel="shortcut icon" href="/favicon.ico" />

  <title>How We Work — Foundations & Methodology | NUMEROS VISION</title>
  <meta name="description" content="Discover how Numeros Vision synthesizes classical Chaldean, Vedic, Lo Shu, and Pythagorean traditions with deterministic mathematical precision. Zero fatalism, zero superstition." />
  <link rel="canonical" href="https://numerosvision.com/how_we_work.html" />

  <meta name="robots" content="index, follow" />
  <meta property="og:site_name" content="NUMEROS VISION" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://numerosvision.com/how_we_work.html" />
  <meta property="og:title" content="How We Work — Foundations & Methodology | NUMEROS VISION" />
  <meta property="og:description" content="A transparent, multi-tradition approach to numerology: Chaldean, Vedic, Lo Shu, and Pythagorean traditions preserved as separate diagnostic layers." />
  <meta property="og:image" content="https://numerosvision.com/static/logos/anveil-charm-hero.png" />

  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500;600;700&family=Cinzel:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" />
  <link rel="stylesheet" href="/static/css/theme.css?v=5.4.0" />

  <style>
    body {{
      background: #FFFDF7;
      color: #523E28;
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
      margin: 0;
      padding: 0;
      line-height: 1.6;
    }}
    .hww-hero {{
      padding: 70px 24px 50px;
      text-align: center;
      background: linear-gradient(180deg, #F7F3EA 0%, #FFFDF7 100%);
      border-bottom: 1px solid rgba(201, 162, 39, 0.2);
    }}
    .hww-hero-eyebrow {{
      font-family: 'Cinzel', serif;
      font-size: 0.85rem;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--gold-dark, #8B6914);
      margin-bottom: 12px;
      display: block;
      font-weight: 600;
    }}
    .hww-hero h1 {{
      font-family: 'Cormorant Garamond', serif;
      font-size: clamp(2.2rem, 5vw, 3.4rem);
      color: var(--ink-dark, #523E28);
      margin: 0 0 16px;
      font-weight: 600;
      letter-spacing: -0.01em;
    }}
    .hww-hero p {{
      max-width: 680px;
      margin: 0 auto;
      font-size: 1.1rem;
      color: var(--ink-muted, #7A654D);
    }}
    .hww-container {{
      max-width: 960px;
      margin: 0 auto;
      padding: 60px 24px 80px;
    }}
    .tradition-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 28px;
      margin: 40px 0 60px;
    }}
    .tradition-card {{
      background: #FFFFFF;
      border: 1px solid rgba(201, 162, 39, 0.25);
      border-radius: 8px;
      padding: 28px;
      box-shadow: 0 4px 16px rgba(82, 62, 40, 0.04);
      transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    .tradition-card:hover {{
      transform: translateY(-2px);
      box-shadow: 0 8px 24px rgba(82, 62, 40, 0.08);
    }}
    .tradition-card-tag {{
      font-family: 'Cinzel', serif;
      font-size: 0.75rem;
      letter-spacing: 0.12em;
      text-transform: uppercase;
      color: var(--gold-dark, #8B6914);
      margin-bottom: 8px;
      display: block;
      font-weight: 600;
    }}
    .tradition-card h3 {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.6rem;
      color: var(--ink-dark, #523E28);
      margin: 0 0 12px;
      font-weight: 600;
    }}
    .tradition-card p {{
      font-size: 0.95rem;
      color: var(--ink-muted, #7A654D);
      margin: 0 0 14px;
    }}
    .principles-box {{
      background: #F7F3EA;
      border-left: 4px solid var(--gold-dark, #8B6914);
      padding: 30px;
      border-radius: 0 8px 8px 0;
      margin: 40px 0;
    }}
    .principles-box h2 {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.8rem;
      color: var(--ink-dark, #523E28);
      margin: 0 0 16px;
    }}
    .principles-list {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    .principles-list li {{
      padding: 10px 0 10px 24px;
      position: relative;
      font-size: 1rem;
      color: var(--ink-dark, #523E28);
    }}
    .principles-list li::before {{
      content: "•";
      position: absolute;
      left: 6px;
      color: var(--gold-dark, #8B6914);
      font-size: 1.4rem;
      line-height: 1;
    }}
    .placeholder-card {{
      background: #FFFFFF;
      border: 1px dashed rgba(201, 162, 39, 0.4);
      border-radius: 8px;
      padding: 32px;
      text-align: center;
      margin-top: 50px;
    }}
    .placeholder-card h3 {{
      font-family: 'Cormorant Garamond', serif;
      font-size: 1.5rem;
      color: var(--ink-dark, #523E28);
      margin: 0 0 10px;
    }}
    .placeholder-card p {{
      font-size: 0.95rem;
      color: var(--ink-muted, #7A654D);
      max-width: 600px;
      margin: 0 auto;
    }}
  </style>
</head>
<body>
  {header}

  <section class="hww-hero">
    <span class="hww-hero-eyebrow">Methodology &amp; Standards</span>
    <h1>How We Work</h1>
    <p>Mathematical rigor, historical provenance, and honest personal reflection. We present classical numerology as structured self-understanding without superstitious promises or fatalistic claims.</p>
  </section>

  <main class="hww-container">
    <div class="principles-box">
      <h2>Our Foundational Principles</h2>
      <ul class="principles-list">
        <li><strong>Deterministic calculation:</strong> Every number, vibration, and timeline is calculated via tested mathematical algorithms. We do not use speculative language or arbitrary scoring.</li>
        <li><strong>Independent diagnostic layers:</strong> Ancient traditions are evaluated as distinct perspectives. We never force-average contradictory systems into a misleading blend.</li>
        <li><strong>Zero fatalism:</strong> Numbers are interpretive indicators of habits, drives, and tendencies. They do not dictate fixed fates, guaranteed fortunes, or unalterable outcomes.</li>
        <li><strong>Privacy &amp; consent:</strong> We practice statutory data protection and privacy under statutory DPDP standards. Your birth details are used solely to generate your requested insights.</li>
      </ul>
    </div>

    <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.2rem; color:var(--ink-dark,#523E28); margin-top:50px; text-align:center;">The Four Core Traditions</h2>
    <p style="text-align:center; color:var(--ink-muted,#7A654D); max-width:640px; margin:0 auto 30px;">Each tradition offers a unique lens on character, timing, and personal balance.</p>

    <div class="tradition-grid">
      <div class="tradition-card">
        <span class="tradition-card-tag">Root Vibrational Model</span>
        <h3>Chaldean tradition</h3>
        <p>The Chaldean system maps letter sounds and single-digit numbers to planetary archetypes. It focuses on your day of birth and compound totals, providing deep insight into inner motives, communication style, and growth edges.</p>
      </div>

      <div class="tradition-card">
        <span class="tradition-card-tag">Harmonic Cycles</span>
        <h3>Vedic tradition</h3>
        <p>The Vedic perspective explores natal planetary rulers, temporal Dasha cycles, and directional balance. It emphasizes pacing, personal duty, and aligning deliberate action with natural cycles of life.</p>
      </div>

      <div class="tradition-card">
        <span class="tradition-card-tag">Spatial &amp; Elemental Matrix</span>
        <h3>Lo Shu grid</h3>
        <p>A classical 3×3 matrix that organizes your birth date across spatial coordinates and elemental energies. It maps balance across eight distinct life planes: Mental, Emotional, Practical, and Will.</p>
      </div>

      <div class="tradition-card">
        <span class="tradition-card-tag">Philosophical Archetypes</span>
        <h3>Pythagorean tradition</h3>
        <p>The foundational Western approach exploring the symbolic geometry of numbers 1 through 9. It provides an articulate comparative view of core personality polarities and collaborative dynamics.</p>
      </div>
    </div>

    <div class="placeholder-card">
      <span style="font-family:'Cinzel',serif; font-size:0.8rem; letter-spacing:0.12em; text-transform:uppercase; color:var(--gold-dark,#8B6914); display:block; margin-bottom:8px;">Reference Library</span>
      <h3>Verified Academic &amp; Historical Reading List</h3>
      <p>Our complete verified reference library, source cross-walk, and historical bibliography will be published here upon final review by our legal counsel.</p>
    </div>
  </main>

  {footer}
</body>
</html>
"""

with open('app/static/how_we_work.html', 'w', encoding='utf-8') as f:
    f.write(html)

print('Created app/static/how_we_work.html successfully!')
