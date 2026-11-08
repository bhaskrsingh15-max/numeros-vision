import os, re, glob

# Master unified snippets
FONTS_SNIPPET = """  <!-- Google Fonts for Unified Master Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800&family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet" />"""

STYLES_SNIPPET = """  <link rel="stylesheet" href="/static/css/theme.css" />
  <link rel="stylesheet" href="/static/css/roadmap_components.css" />"""

FAVICON_SNIPPET = """  <link rel="icon" type="image/svg+xml" href="/logos/nv-logo-mark.svg" />"""

NAV_SCRIPT = """  <script>
    function toggleMobileNav() {
      const m = document.getElementById('nvNavMenu') || document.getElementById('nv-nav-menu');
      if (m) m.classList.toggle('active');
    }
  </script>"""

MASTER_HEADER = """  <!-- Master Unified Site Header -->
  <header class="nv-header">
    <div class="nv-nav-container">
      <a href="/" class="nv-brand-link" title="Numeros Vision — Anviel Every Charm">
        <div class="nv-brand-seal">
          <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
        </div>
        <div class="nv-brand-text">
          <span class="nv-brand-title">NUMEROS VISION</span>
          <span class="nv-brand-tagline">ANVIEL EVERY CHARM</span>
        </div>
      </a>

      <!-- Desktop Navigation Links matching Master Roadmap IA -->
      <nav aria-label="Main Navigation">
        <ul class="nv-nav-menu" id="nvNavMenu">
          <li class="nv-nav-item"><a href="/calculators/" class="nv-nav-link">Calculators</a></li>
          <li class="nv-nav-item"><a href="/charm-ai/" class="nv-nav-link">Charm AI</a></li>
          <li class="nv-nav-item"><a href="/reports/" class="nv-nav-link">Reports</a></li>
          <li class="nv-nav-item"><a href="/methodology/" class="nv-nav-link">Methodology</a></li>
          <li class="nv-nav-item"><a href="/insights/" class="nv-nav-link">Insights</a></li>
          <li class="nv-nav-item"><a href="/pricing/" class="nv-nav-link">Pricing</a></li>
          <li class="nv-nav-item"><a href="/about/" class="nv-nav-link">About</a></li>
        </ul>
      </nav>

      <div class="nv-nav-actions">
        <a href="/#birth-profile" class="nv-btn-cta">Discover My Numbers ✦</a>
        <button class="nv-mobile-toggle" onclick="toggleMobileNav()" aria-label="Toggle Navigation">☰</button>
      </div>
    </div>
  </header>"""

PRACTITIONER_HEADER = """  <!-- Master Unified Site Header -->
  <header class="nv-header">
    <div class="nv-nav-container">
      <a href="/" class="nv-brand-link" title="Numeros Vision — Anviel Every Charm">
        <div class="nv-brand-seal">
          <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
        </div>
        <div class="nv-brand-text">
          <span class="nv-brand-title">NUMEROS VISION</span>
          <span class="nv-brand-tagline">ANVIEL EVERY CHARM</span>
        </div>
      </a>

      <!-- Desktop Navigation Links matching Master Roadmap IA -->
      <nav aria-label="Main Navigation">
        <ul class="nv-nav-menu" id="nvNavMenu">
          <li class="nv-nav-item"><a href="/calculators/" class="nv-nav-link">Calculators</a></li>
          <li class="nv-nav-item"><a href="/charm-ai/" class="nv-nav-link">Charm AI</a></li>
          <li class="nv-nav-item"><a href="/reports/" class="nv-nav-link">Reports</a></li>
          <li class="nv-nav-item"><a href="/methodology/" class="nv-nav-link">Methodology</a></li>
          <li class="nv-nav-item"><a href="/insights/" class="nv-nav-link">Insights</a></li>
          <li class="nv-nav-item"><a href="/pricing/" class="nv-nav-link">Pricing</a></li>
          <li class="nv-nav-item"><a href="/practitioner" class="nv-nav-link active">Practitioner</a></li>
        </ul>
      </nav>

      <div class="nv-nav-actions">
        <button id="btn-signout" onclick="handlePractitionerLogout()" class="btn-ghost" style="display:none; padding:8px 14px; font-size:0.75rem; color:#C92A2A; cursor:pointer;">Sign Out ⎋</button>
        <a href="/" class="nv-btn-cta">Portal Home ✦</a>
        <button class="nv-mobile-toggle" onclick="toggleMobileNav()" aria-label="Toggle Navigation">☰</button>
      </div>
    </div>
  </header>"""

SAMPLE_HEADER = """  <!-- Master Unified Site Header -->
  <header class="nv-header">
    <div class="nv-nav-container">
      <a href="/" class="nv-brand-link" title="Numeros Vision — Anviel Every Charm">
        <div class="nv-brand-seal">
          <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
        </div>
        <div class="nv-brand-text">
          <span class="nv-brand-title">NUMEROS VISION</span>
          <span class="nv-brand-tagline">ANVIEL EVERY CHARM</span>
        </div>
      </a>

      <!-- Desktop Navigation Links matching Master Roadmap IA -->
      <nav aria-label="Main Navigation">
        <ul class="nv-nav-menu" id="nvNavMenu">
          <li class="nv-nav-item"><a href="/calculators/" class="nv-nav-link">Calculators</a></li>
          <li class="nv-nav-item"><a href="/charm-ai/" class="nv-nav-link">Charm AI</a></li>
          <li class="nv-nav-item"><a href="/reports/" class="nv-nav-link">Reports</a></li>
          <li class="nv-nav-item"><a href="/methodology/" class="nv-nav-link">Methodology</a></li>
          <li class="nv-nav-item"><a href="/insights/" class="nv-nav-link">Insights</a></li>
          <li class="nv-nav-item"><a href="/pricing/" class="nv-nav-link">Pricing</a></li>
          <li class="nv-nav-item"><a href="/about/" class="nv-nav-link">About</a></li>
        </ul>
      </nav>

      <div class="nv-nav-actions">
        <button class="btn-gold" onclick="window.print()" style="padding:8px 16px; font-size:0.8rem; cursor:pointer;">📥 Print / PDF</button>
        <a href="/#birth-profile" class="nv-btn-cta">Discover My Numbers ✦</a>
        <button class="nv-mobile-toggle" onclick="toggleMobileNav()" aria-label="Toggle Navigation">☰</button>
      </div>
    </div>
  </header>"""

MASTER_FOOTER = """  <!-- Master Unified Site Footer -->
  <footer class="nv-footer">
    <div class="nv-footer-container">
      <div class="nv-footer-grid">
        <!-- Brand Summary Column -->
        <div class="nv-footer-brand-sec">
          <a href="/" class="nv-brand-link" style="margin-bottom:12px;">
            <div class="nv-brand-seal" style="width:38px;height:38px;">
              <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
            </div>
            <div class="nv-brand-text">
              <span class="nv-brand-title" style="font-size:1.05rem;">NUMEROS VISION</span>
              <span class="nv-brand-tagline">ANVIEL EVERY CHARM</span>
            </div>
          </a>
          <p>
            AI-powered numerological intelligence combining deterministic Vedic, Chaldean, and Lo Shu mathematical frameworks. Unveil every charm with clarity, mathematical rigor, and ethical privacy.
          </p>
        </div>

        <!-- Column 1: Working Calculators -->
        <div class="nv-footer-col">
          <h4>Calculators</h4>
          <ul class="nv-footer-links">
            <li><a href="/calculators/birth-number/">Birth Number (Mulank)</a></li>
            <li><a href="/calculators/life-path-number/">Life Path (Bhagyank)</a></li>
            <li><a href="/calculators/name-numerology/">Name Balancing</a></li>
            <li><a href="/calculators/lo-shu-grid/">Lo Shu 3×3 Grid</a></li>
            <li><a href="/calculators/mobile-number-numerology/">Mobile Numerology</a></li>
            <li><a href="/calculators/personal-year/">Personal Year Calculator</a></li>
            <li><a href="/calculators/">View All Calculators →</a></li>
          </ul>
        </div>

        <!-- Column 2: Intelligence & Plans -->
        <div class="nv-footer-col">
          <h4>Intelligence &amp; Plans</h4>
          <ul class="nv-footer-links">
            <li><a href="/charm-ai/">Charm AI Assistant</a></li>
            <li><a href="/reports/">Reports Catalogue</a></li>
            <li><a href="/sample">Sample Dossier</a></li>
            <li><a href="/pricing/">Plans &amp; Pricing</a></li>
            <li><a href="/consultation/">1-on-1 Consultation</a></li>
            <li><a href="/methodology/">Methodology &amp; Math</a></li>
          </ul>
        </div>

        <!-- Column 3: Wisdom & Governance -->
        <div class="nv-footer-col">
          <h4>Wisdom &amp; Legal</h4>
          <ul class="nv-footer-links">
            <li><a href="/insights/">Insights Learning Hub</a></li>
            <li><a href="/about/">About Numeros Vision</a></li>
            <li><a href="/contact/">Contact Support</a></li>
            <li><a href="mailto:support@numerosvision.com">support@numerosvision.com</a></li>
            <li><a href="/practitioner">Practitioner Portal</a></li>
            <li><a href="/privacy-policy/">Privacy Policy</a></li>
            <li><a href="/disclaimer/">Statutory Disclaimer</a></li>
            <li><a href="/terms/">Terms of Service</a></li>
          </ul>
        </div>
      </div>

      <!-- Statutory Disclaimer Box -->
      <div class="nv-footer-disclaimer-box">
        <strong>Statutory Ethical Disclaimer:</strong> Numeros Vision interpretations, mathematical calculations, and AI reflections are generated strictly for philosophical inquiry, self-reflection, and cultural entertainment. Numeros Vision does not provide licensed medical, legal, or financial advice.
      </div>

      <!-- Bottom Bar -->
      <div class="nv-footer-bottom">
        <div>© 2026 Numeros Vision. All rights reserved. Master Brand: Numeros Vision · Tagline: Anviel Every Charm.</div>
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
  </footer>"""

def update_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    
    # 1. Ensure roadmap_components.css is included in head
    if 'roadmap_components.css' not in content:
        if '</head>' in content:
            content = content.replace('</head>', f'  <link rel="stylesheet" href="/static/css/roadmap_components.css" />\n</head>', 1)
            modified = True
    
    # 2. Ensure Cinzel and Cormorant Garamond fonts are included
    if 'Cinzel' not in content:
        if '</head>' in content:
            content = content.replace('</head>', f'{FONTS_SNIPPET}\n</head>', 1)
            modified = True
            
    # 3. Ensure favicon is set to official logo
    if 'nv-logo-mark.svg' not in content:
        if '</head>' in content:
            content = content.replace('</head>', f'{FAVICON_SNIPPET}\n</head>', 1)
            modified = True
            
    # 4. Replace Header
    header_to_use = MASTER_HEADER
    if 'practitioner.html' in fpath:
        header_to_use = PRACTITIONER_HEADER
    elif 'sample.html' in fpath or 'sample2.html' in fpath:
        header_to_use = SAMPLE_HEADER
        
    if '<header class="nv-header">' not in content:
        # Search for existing header
        existing_header = re.search(r'<header.*?</header>', content, re.DOTALL | re.IGNORECASE)
        if existing_header:
            content = content[:existing_header.start()] + header_to_use + content[existing_header.end():]
            modified = True
        else:
            # Insert right after <body>
            body_match = re.search(r'<body[^>]*>', content, re.IGNORECASE)
            if body_match:
                insert_pos = body_match.end()
                content = content[:insert_pos] + '\n\n' + header_to_use + '\n' + content[insert_pos:]
                modified = True

    # 5. Replace Footer
    if '<footer class="nv-footer">' not in content:
        existing_footer = re.search(r'<footer.*?</footer>', content, re.DOTALL | re.IGNORECASE)
        if existing_footer:
            content = content[:existing_footer.start()] + MASTER_FOOTER + content[existing_footer.end():]
            modified = True
        else:
            # Insert right before </body>
            if '</body>' in content:
                content = content.replace('</body>', f'\n{MASTER_FOOTER}\n</body>', 1)
                modified = True
                
    # 6. Ensure toggleMobileNav script exists
    if 'toggleMobileNav' not in content:
        if '</body>' in content:
            content = content.replace('</body>', f'\n{NAV_SCRIPT}\n</body>', 1)
            modified = True
            
    if modified:
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[UPDATED] {fpath}")
    else:
        print(f"[UNCHANGED] {fpath}")

# Run across all 27 files
target_files = [
    'app/static/practitioner.html',
    'app/static/sample.html',
    'app/static/sample2.html',
    'app/static/cdp.html',
    'app/static/demo.html',
    'app/static/logo-preview.html',
] + glob.glob('app/static/tools/*.html') + [
    'app/static/blog/chaldean-vs-pythagorean-numerology.html',
    'app/static/blog/gemstone-remedies.html',
    'app/static/blog/kua-number-auspicious-directions-and-career-feng-shui.html',
    'app/static/blog/life-path-numbers-explained.html',
    'app/static/blog/lo-shu-grid-8-planes.html',
    'app/static/blog/master-numbers-11-22-33.html',
    'app/static/blog/mobile-numerology-malefic-pairs.html',
    'app/static/blog/vedic-gemstone-remedies.html',
    'app/static/blog/what-is-numerology.html',
]

print(f"Processing {len(target_files)} target files...")
for f in target_files:
    if os.path.exists(f):
        update_file(f)
    else:
        print(f"[MISSING] {f}")
