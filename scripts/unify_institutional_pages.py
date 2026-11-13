"""
Script: scripts/unify_institutional_pages.py
Purpose: Unify headers, breadcrumbs, footers, and CSS links across all institutional
         and legal pages to match the Venus Pearl & Jupiter Gold master roadmap standard.
"""

import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"

PAGES_CONFIG = {
    "pricing.html": {
        "title": "Plans & Pricing",
        "active": "pricing",
        "breadcrumb": "Plans & Pricing"
    },
    "contact.html": {
        "title": "Contact Us",
        "active": "",
        "breadcrumb": "Contact Us"
    },
    "privacy.html": {
        "title": "Privacy Policy",
        "active": "",
        "breadcrumb": "Privacy Policy"
    },
    "terms.html": {
        "title": "Terms of Service",
        "active": "",
        "breadcrumb": "Terms of Service"
    },
    "disclaimer.html": {
        "title": "Statutory Disclaimer",
        "active": "",
        "breadcrumb": "Statutory Disclaimer"
    },
    "refund.html": {
        "title": "Refund & Cancellation",
        "active": "",
        "breadcrumb": "Refund Policy"
    }
}

def get_nv_header(active_key, breadcrumb_label):
    def is_act(key):
        return "active" if key == active_key else ""

    return f'''  <!-- Unified Header -->
  <header class="nv-header">
    <div class="nv-nav-container">
      <a href="/" class="nv-brand-link" title="Numeros Vision — Anveil Every Charm">
        <div class="nv-brand-seal">
          <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
        </div>
        <div class="nv-brand-text">
          <span class="nv-brand-title">NUMEROS VISION</span>
          <span class="nv-brand-tagline">ANVEIL EVERY CHARM</span>
        </div>
      </a>

      <nav>
        <ul class="nv-nav-menu" id="nvNavMenu">
          <li class="nv-nav-item"><a href="/calculators/" class="nv-nav-link {is_act('calculators')}">Calculators</a></li>
          <li class="nv-nav-item"><a href="/charm-ai/" class="nv-nav-link {is_act('charm-ai')}">Charm AI</a></li>
          <li class="nv-nav-item"><a href="/reports/" class="nv-nav-link {is_act('reports')}">Reports</a></li>
          <li class="nv-nav-item"><a href="/methodology/" class="nv-nav-link {is_act('methodology')}">Methodology</a></li>
          <li class="nv-nav-item"><a href="/insights/" class="nv-nav-link {is_act('insights')}">Insights</a></li>
          <li class="nv-nav-item"><a href="/pricing/" class="nv-nav-link {is_act('pricing')}">Pricing</a></li>
          <li class="nv-nav-item"><a href="/about/" class="nv-nav-link {is_act('about')}">About</a></li>
        </ul>
      </nav>

      <div class="nv-nav-actions">
        <a href="/consultation/" class="nv-btn-cta">Book Consultation ✦</a>
        <button class="nv-mobile-toggle" onclick="toggleMobileNav()" aria-label="Toggle Navigation Menu">☰</button>
      </div>
    </div>
  </header>

  <!-- Breadcrumbs -->
  <div class="nv-breadcrumbs">
    <a href="/">Home</a>
    <span class="nv-breadcrumbs-sep">/</span>
    <span class="nv-breadcrumbs-current">{breadcrumb_label}</span>
  </div>'''

NV_FOOTER = '''  <!-- Unified Footer -->
  <footer class="nv-footer">
    <div class="nv-footer-container">
      <div class="nv-footer-grid">
        <div class="nv-footer-brand-sec">
          <div class="nv-brand-link" style="margin-bottom:12px;">
            <div class="nv-brand-seal" style="width:38px;height:38px;">
              <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
            </div>
            <div class="nv-brand-text">
              <span class="nv-brand-title" style="font-size:1.05rem;">NUMEROS VISION</span>
              <span class="nv-brand-tagline">ANVEIL EVERY CHARM</span>
            </div>
          </div>
          <p>
            AI-powered numerological intelligence combining deterministic Vedic, Chaldean, and Lo Shu mathematical frameworks.
          </p>
        </div>

        <div class="nv-footer-col">
          <h4>Core Solutions</h4>
          <ul class="nv-footer-links">
            <li><a href="/calculators/">Calculator Hub</a></li>
            <li><a href="/charm-ai/">Charm AI Assistant</a></li>
            <li><a href="/reports/">Reports Catalogue</a></li>
            <li><a href="/sample-report/">Sample Dossier</a></li>
            <li><a href="/consultation/">1-on-1 Consultation</a></li>
          </ul>
        </div>

        <div class="nv-footer-col">
          <h4>Calculators</h4>
          <ul class="nv-footer-links">
            <li><a href="/calculators/birth-number/">Birth Number (Mulank)</a></li>
            <li><a href="/calculators/life-path-number/">Life Path (Bhagyank)</a></li>
            <li><a href="/calculators/name-numerology/">Name Numerology</a></li>
            <li><a href="/calculators/lo-shu-grid/">Lo Shu 3x3 Grid</a></li>
            <li><a href="/calculators/mobile-number-numerology/">Mobile Number Audit</a></li>
            <li><a href="/calculators/personal-year/">Personal Year Cycle</a></li>
            <li><a href="/calculators/numerology-compatibility/">Compatibility Matrix</a></li>
          </ul>
        </div>

        <div class="nv-footer-col">
          <h4>Trust & Institutional</h4>
          <ul class="nv-footer-links">
            <li><a href="/about/">About Us</a></li>
            <li><a href="/methodology/">Methodology</a></li>
            <li><a href="/pricing/">Pricing & Plans</a></li>
            <li><a href="/faq/">Frequently Asked Questions</a></li>
            <li><a href="/privacy-policy/">Privacy Policy</a></li>
            <li><a href="/terms/">Terms of Service</a></li>
            <li><a href="/disclaimer/">Statutory Disclaimer</a></li>
          </ul>
        </div>
      </div>

      <div class="nv-footer-disclaimer-box">
        <strong>Statutory Disclaimer:</strong> Numeros Vision provides reflective numerological interpretations and traditional mathematical frameworks for self-reflection and personal insight. Our reports and AI analyses are not substitutes for professional medical, psychiatric, financial, or legal advice. All calculations are executed deterministically under strict Indian Digital Personal Data Protection (DPDP) Act 2023 compliance standards.
      </div>

      <div class="nv-footer-bottom">
        <div>© 2026 Numeros Vision. Anveil Every Charm. Deterministic AI Numerology.</div>
        <div class="nv-footer-legal-inline">
          <a href="/privacy-policy/">Privacy Policy</a>
          <a href="/terms/">Terms of Service</a>
          <a href="/disclaimer/">Disclaimer</a>
          <a href="/refund-policy/">Refund Policy</a>
          <a href="/accessibility/">Accessibility</a>
        </div>
      </div>
    </div>
  </footer>

  <script>
    function toggleMobileNav() {
      const menu = document.getElementById("nvNavMenu");
      if (menu) menu.classList.toggle("active");
    }
  </script>'''

def unify_page(filename, cfg):
    path = STATIC_DIR / filename
    if not path.exists():
        print(f"Skipping {filename}: not found")
        return

    content = path.read_text(encoding="utf-8")
    original = content

    # 1. Ensure roadmap_components.css is linked
    if "/static/css/roadmap_components.css" not in content:
        content = content.replace(
            '<link rel="stylesheet" href="/static/css/theme.css" />',
            '<link rel="stylesheet" href="/static/css/theme.css" />\n  <link rel="stylesheet" href="/static/css/roadmap_components.css" />'
        )

    # 2. Replace <header class="site-header">...</header>
    header_pattern = re.compile(r'<!-- Site Header -->\s*<header class="site-header">.*?</header>', re.DOTALL)
    if header_pattern.search(content):
        nv_hdr = get_nv_header(cfg["active"], cfg["breadcrumb"])
        content = header_pattern.sub(nv_hdr, content)
    elif '<header class="site-header">' in content:
        header_pattern_alt = re.compile(r'<header class="site-header">.*?</header>', re.DOTALL)
        nv_hdr = get_nv_header(cfg["active"], cfg["breadcrumb"])
        content = header_pattern_alt.sub(nv_hdr, content)

    # 3. Replace <footer class="site-footer">...</footer>
    footer_pattern = re.compile(r'<!-- Footer -->\s*<footer class="site-footer">.*?</footer>', re.DOTALL)
    if footer_pattern.search(content):
        content = footer_pattern.sub(NV_FOOTER, content)
    elif '<footer class="site-footer">' in content:
        footer_pattern_alt = re.compile(r'<footer class="site-footer">.*?</footer>', re.DOTALL)
        content = footer_pattern_alt.sub(NV_FOOTER, content)

    if content != original:
        path.write_text(content, encoding="utf-8")
        print(f"[UNIFIED] {filename}")
    else:
        print(f"[UNCHANGED] {filename}")

def main():
    for fn, cfg in PAGES_CONFIG.items():
        unify_page(fn, cfg)

if __name__ == "__main__":
    main()
