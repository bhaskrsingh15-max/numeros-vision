"""
scripts/apply_frontend_integration.py
Integrate newly created Business Direction Intelligence and Logo Intelligence Studio
into frontend navigation, homepage showcase, and calculator hub, maintaining 100% theme,
font, logo, and header/footer parity.
"""
import os
import re

MASTER_HEADER = """  <!-- Master Unified Site Header — Numeros Vision | Anveil Every Charm -->
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

      <!-- Desktop Navigation Links matching Master Roadmap IA -->
      <nav aria-label="Main Navigation">
                <ul class="nv-nav-menu" id="nvNavMenu">
          <!-- 1. About Us -->
          <li class="nv-nav-item">
            <a href="/about/" class="nv-nav-link" title="About Numeros Vision | Our Approach to Numerology" data-canonical="https://numerosvision.com/about/">About Us</a>
          </li>

          <!-- 2. Calculators (Accordion / Dropdown) -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Calculators</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/tools/baby-naming" class="nv-submenu-link"><span class="nv-sub-icon">👶</span> <span>Auspicious Baby Naming</span> <span class="nv-sub-tag">Hot</span></a></li>
              <li><a href="/tools/name-numerology" class="nv-submenu-link"><span class="nv-sub-icon">✍️</span> <span>Name Analysis &amp; Balancing</span></a></li>
              <li><a href="/tools/mobile-numerology" class="nv-submenu-link"><span class="nv-sub-icon">📱</span> <span>Mobile Number Audit</span></a></li>
              <li><a href="/tools/kundali-milan" class="nv-submenu-link"><span class="nv-sub-icon">💍</span> <span>Kundali Milan &amp; Synastry</span></a></li>
              <li><a href="/tools/business-numerology" class="nv-submenu-link"><span class="nv-sub-icon">💼</span> <span>Business &amp; Brand Name</span></a></li>
              <li><a href="/tools/life-path-calculator" class="nv-submenu-link"><span class="nv-sub-icon">🧭</span> <span>Life Path Calculator</span></a></li>
              <li><a href="/tools/lo-shu-grid" class="nv-submenu-link"><span class="nv-sub-icon">🔲</span> <span>Lo Shu Magic Grid</span></a></li>
              <li><a href="/tools/vehicle-numerology" class="nv-submenu-link"><span class="nv-sub-icon">🚗</span> <span>Vehicle Numerology</span></a></li>
              <li><a href="/tools/property-numerology" class="nv-submenu-link"><span class="nv-sub-icon">🏠</span> <span>House &amp; Property Audit</span></a></li>
              <li><a href="/tools/blessing-years" class="nv-submenu-link"><span class="nv-sub-icon">📅</span> <span>Blessing Years Timeline</span></a></li>
              <li class="nv-submenu-footer"><a href="/calculators/" class="nv-submenu-all">View All 10+ Calculators →</a></li>
            </ul>
          </li>

          <!-- 2. Charm AI -->
          <li class="nv-nav-item"><a href="/#charm-ai" class="nv-nav-link">Charm AI</a></li>

          <!-- 3. Reports & Consultations -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Reports</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/reports/" class="nv-submenu-link"><span class="nv-sub-icon">📜</span> <span>Vedic Destiny Report</span></a></li>
              <li><a href="/consultation/" class="nv-submenu-link"><span class="nv-sub-icon">👤</span> <span>1-on-1 Consultation</span></a></li>
              <li><a href="/practitioner/" class="nv-submenu-link"><span class="nv-sub-icon">🧑‍💼</span> <span>Practitioner Workspace CRM</span></a></li>
            </ul>
          </li>

          <!-- 5. Insights -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Insights</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/insights/" class="nv-submenu-link"><span class="nv-sub-icon">📚</span> <span>Numerology Knowledge Hub</span></a></li>
              <li><a href="/blog/master-numbers-11-22-33" class="nv-submenu-link"><span class="nv-sub-icon">🔢</span> <span>Master Numbers 11, 22, 33</span></a></li>
              <li><a href="/blog/chaldean-vs-pythagorean-numerology" class="nv-submenu-link"><span class="nv-sub-icon">⚖️</span> <span>Chaldean vs Pythagorean</span></a></li>
              <li><a href="/blog/lo-shu-grid-8-planes" class="nv-submenu-link"><span class="nv-sub-icon">🔲</span> <span>Lo Shu Grid 8 Planes</span></a></li>
              <li><a href="/blog/gemstone-remedies" class="nv-submenu-link"><span class="nv-sub-icon">💎</span> <span>Gemstone Remedies Guide</span></a></li>
            </ul>
          </li>

          <!-- 5. Pricing -->
          <li class="nv-nav-item"><a href="/pricing/" class="nv-nav-link">Pricing</a></li>

          <!-- 6. Contact Us -->
          <li class="nv-nav-item"><a href="/contact/" class="nv-nav-link" title="Contact Us">Contact Us</a></li>

          <!-- 7. PWA Download / Install App on Mobile & Tablet ONLY -->
          <li class="nv-nav-item nv-pwa-menu-item" id="nvPwaDrawerItem" style="display:none; margin: 8px 0; width: 100%; box-sizing: border-box;">
            <button type="button" class="nv-nav-link nv-pwa-install-trigger-btn" onclick="triggerPwaInstall(event)" style="background: rgba(201,162,39,0.12); border: 1.5px solid rgba(201,162,39,0.38); border-radius: 999px; padding: 10px 18px; font-weight: 600; color: #8B6914; display: flex; align-items: center; justify-content: space-between; width: 100%; cursor: pointer; text-align: left; box-sizing: border-box;">
              <span style="display: flex; align-items: center; gap: 8px;">
                <span class="nv-sub-icon" style="font-size: 1.15rem;">📲</span>
                <span>Install / Download App</span>
              </span>
              <span class="nv-sub-tag" style="background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color: #fff; font-size: 0.65rem; padding: 2px 7px; border-radius: 6px; font-weight: 700; text-transform: uppercase;">PWA</span>
            </button>
          </li>
        </ul>
      </nav>

      <div class="nv-nav-actions">
        <a href="/signup/" class="nv-nav-link-auth">Sign Up</a>
        <a href="/#birth-profile" class="nv-btn-cta">Discover My Numbers ✦</a>
        <button class="nv-mobile-toggle" onclick="toggleMobileNav(event)" aria-label="Toggle Navigation">☰</button>
      </div>
    </div>
  </header>
  <script>
    function toggleMobileNav(e) {
      if (window.nvToggleMaster && typeof window.nvToggleMaster === 'function') {
        return window.nvToggleMaster(e || window.event);
      }
      var evt = e || window.event;
      if (evt && evt.stopPropagation) evt.stopPropagation();
      var menu = document.getElementById('nvNavMenu');
      var btn = document.querySelector('.nv-mobile-toggle');
      if (menu) {
        var isOpen = menu.classList.toggle('active');
        if (btn) {
          btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
          btn.innerHTML = isOpen ? '✕' : '☰';
        }
      }
    }
    function toggleNavAccordion(btn, e) {
      var evt = e || window.event;
      if (evt && evt.stopPropagation) evt.stopPropagation();
      var parent = btn.closest('.nv-has-dropdown');
      if (!parent) return;
      var isOpen = parent.classList.toggle('open');
      btn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    }
  </script>"""

MASTER_FOOTER_AND_SCRIPTS = """  <!-- Master Unified Site Footer -->
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
              <span class="nv-brand-tagline">ANVEIL EVERY CHARM</span>
            </div>
          </a>
          <p>
            AI-powered numerological intelligence combining deterministic Vedic, Chaldean, and Lo Shu mathematical frameworks. Anveil every charm with clarity, mathematical rigor, and ethical privacy.
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
            <li><a href="/tools/business-alignment">Business Direction Intelligence</a></li>
            <li><a href="/tools/logo-intelligence">Logo Intelligence Studio</a></li>
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
            <li><a href="/practitioner">Practitioner Portal</a></li>
            <li><a href="/privacy-policy/">Privacy Policy</a></li>
            <li><a href="/disclaimer/">Statutory Disclaimer</a></li>
            <li><a href="/terms/">Terms of Service</a></li>
          </ul>
        </div>
      </div>

      <!-- Bottom Bar -->
      <div class="nv-footer-bottom">
        <div>© 2026 Numeros Vision. All rights reserved. Master Brand: Numeros Vision · Tagline: Anveil Every Charm.</div>
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

  <script src="/static/js/nav.js?v=4.7.3" defer></script>
  <script src="/static/js/nv_tracking_config.js?v=4.8.0" defer></script>
  <script src="/static/js/marketing-analytics.js?v=4.8.0" defer></script>
  <script src="/static/js/nv_consent.js?v=4.8.0" defer></script>
"""

def update_tool_page(file_path):
    print(f"Updating tool page: {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Replace header
    header_pattern = re.compile(r'<!--\s*Master Unified Site Header[\s\S]*?</header>', re.MULTILINE)
    if header_pattern.search(content):
        content = header_pattern.sub(MASTER_HEADER, content, count=1)
    else:
        # Fallback to <header class="nv-header">...</header>
        h2 = re.compile(r'<header class="nv-header">[\s\S]*?</header>', re.MULTILINE)
        content = h2.sub(MASTER_HEADER, content, count=1)

    # 2. Add footer before </body> if not present
    if '<footer class="nv-footer">' not in content:
        content = content.replace("</body>", MASTER_FOOTER_AND_SCRIPTS + "\n</body>")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated {file_path} successfully.")

def update_index():
    index_path = "app/static/index.html"
    print(f"Updating homepage: {index_path}")
    with open(index_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Add cards 7 & 8 to calc-hub-grid if not present
    if "/tools/business-alignment" not in content:
        target_after_p_year = """        <!-- 6. Personal Year -->
        <a href="/calculators/personal-year/" class="calc-tool-card">
          <div>
            <span class="calc-tool-badge">Annual Cycle 2026</span>
            <h4 class="calc-tool-title">Personal Year Calculator</h4>
            <p class="calc-tool-desc">
              Understand the 9-year vibrational cycle active in your current year to align timing for major transitions.
            </p>
          </div>
          <span class="calc-tool-link-text">Calculate 2026 Cycle →</span>
        </a>"""

        replacement_cards = """        <!-- 6. Personal Year -->
        <a href="/calculators/personal-year/" class="calc-tool-card">
          <div>
            <span class="calc-tool-badge">Annual Cycle 2026</span>
            <h4 class="calc-tool-title">Personal Year Calculator</h4>
            <p class="calc-tool-desc">
              Understand the 9-year vibrational cycle active in your current year to align timing for major transitions.
            </p>
          </div>
          <span class="calc-tool-link-text">Calculate 2026 Cycle →</span>
        </a>

        <!-- 7. Business Direction Intelligence -->
        <a href="/tools/business-alignment" class="calc-tool-card" title="Business Direction &amp; Alignment Intelligence">
          <div>
            <span class="calc-tool-badge">Enterprise Direction</span>
            <h4 class="calc-tool-title">Business Direction Intelligence</h4>
            <p class="calc-tool-desc">
              Compare candidate business models or operating activities against deterministic numerology, archetypes, and market viability.
            </p>
          </div>
          <span class="calc-tool-link-text">Analyze Business Fit →</span>
        </a>

        <!-- 8. Logo Intelligence & Google Nano Banana Studio -->
        <a href="/tools/logo-intelligence" class="calc-tool-card" title="Logo Intelligence &amp; Design Studio">
          <div>
            <span class="calc-tool-badge">Nano Banana Studio</span>
            <h4 class="calc-tool-title">Logo Intelligence Studio</h4>
            <p class="calc-tool-desc">
              Inspect brand marks for contrast and OCR alignment, or generate validated vector brand marks via Google Nano Banana.
            </p>
          </div>
          <span class="calc-tool-link-text">Launch Logo Studio →</span>
        </a>"""
        content = content.replace(target_after_p_year, replacement_cards)

    # 2. Update the button text
    content = content.replace(
        "View All 11 Verified Calculators →",
        "Explore All Calculators &amp; Intelligence Tools →"
    )

    # 3. Add to footer column 2 if not present
    if '<li><a href="/tools/business-alignment">Business Direction Intelligence</a></li>' not in content:
        target_footer_plans = """          <h4>Intelligence &amp; Plans</h4>

          <ul class="nv-footer-links">

            <li><a href="/charm-ai/">Charm AI Assistant</a></li>"""
        replacement_footer_plans = """          <h4>Intelligence &amp; Plans</h4>

          <ul class="nv-footer-links">

            <li><a href="/tools/business-alignment">Business Direction Intelligence</a></li>
            <li><a href="/tools/logo-intelligence">Logo Intelligence Studio</a></li>
            <li><a href="/charm-ai/">Charm AI Assistant</a></li>"""
        content = content.replace(target_footer_plans, replacement_footer_plans)

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Homepage updated successfully.")

if __name__ == "__main__":
    update_tool_page("app/static/tools/business-alignment.html")
    update_tool_page("app/static/tools/logo-intelligence.html")
    update_index()
