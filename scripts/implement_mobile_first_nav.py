# implement_mobile_first_nav.py
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# ── 1. UPDATE APP/STATIC/JS/NAV.JS ───────────────────────────────────────────
with open('app/static/js/nav.js', 'r', encoding='utf-8') as f:
    nav_js = f.read()

# Update updateBottomNavActive()
old_active_fn = '''function updateBottomNavActive() {
  const path = window.location.pathname.toLowerCase();
  const hash = window.location.hash;
  const items = document.querySelectorAll('.nv-bottom-nav-item[data-nav]');
  items.forEach(item => {
    const nav = item.getAttribute('data-nav');
    let isActive = false;
    if (nav === 'home' && (path === '/' || path === '/index.html' || path === '') && !hash) {
      isActive = true;
    } else if ((nav === 'tools' || nav === 'calculators') && (path.includes('calculator') || path.includes('/tools/')) && !path.includes('catalogue')) {
      isActive = true;
    } else if (nav === 'charm-ai' && (path.includes('charm-ai') || hash === '#charm-ai')) {
      isActive = true;
    } else if (nav === 'reports' && (path.includes('reports') || path.includes('catalogue'))) {
      isActive = true;
    } else if (nav === 'profile' && (hash === '#birth-profile' || hash === '#calculator-card' || path.includes('/profile/'))) {
      isActive = true;
    }
    item.classList.toggle('active', isActive);
  });
}'''

new_active_fn = '''function updateBottomNavActive() {
  const path = window.location.pathname.toLowerCase();
  const hash = window.location.hash;
  const items = document.querySelectorAll('.nv-bottom-nav-item[data-nav], .nv-bottom-item[data-nav]');
  items.forEach(item => {
    const nav = item.getAttribute('data-nav');
    let isActive = false;
    if (nav === 'home' && (path === '/' || path === '/index.html' || path === '') && !hash) {
      isActive = true;
    } else if ((nav === 'calculate' || nav === 'tools' || nav === 'calculators') && (path.includes('calculator') || path.includes('/tools/')) && !path.includes('catalogue')) {
      isActive = true;
    } else if (nav === 'reports' && (path.includes('reports') || path.includes('catalogue'))) {
      isActive = true;
    } else if (nav === 'account' && (path.includes('dashboard') || path.includes('account') || path.includes('login') || path.includes('signup'))) {
      isActive = true;
    } else if (nav === 'home' && (hash === '#birth-profile' || hash === '#calculator-card')) {
      isActive = true;
    }
    item.classList.toggle('active', isActive);
  });
}'''

if old_active_fn in nav_js:
    nav_js = nav_js.replace(old_active_fn, new_active_fn)
    print("Updated updateBottomNavActive() in nav.js")
else:
    print("Warning: old_active_fn not found in nav.js")

# Update initStickyBottomNav() to 4 canonical items
old_init_fn = '''  const nav = document.createElement('nav');
  nav.className = 'nv-sticky-bottom-nav';
  nav.setAttribute('aria-label', 'Mobile and Tablet Navigation');
  nav.innerHTML = `
    <a href="/" class="nv-bottom-nav-item" data-nav="home">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      <span>Home</span>
    </a>
    <a href="/calculators/" class="nv-bottom-nav-item" data-nav="tools">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      <span>Tools</span>
    </a>
    <a href="/#charm-ai" class="nv-bottom-nav-item nv-bottom-nav-center" data-nav="charm-ai" title="Charm AI Conversational Intelligence">
      <div class="nv-bottom-center-btn">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg>
      </div>
      <span>Charm AI</span>
    </a>
    <a href="/reports_catalogue/" class="nv-bottom-nav-item" data-nav="reports" title="Comprehensive Numerology Reports">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>
      <span>Reports</span>
    </a>
    <a href="/#birth-profile" class="nv-bottom-nav-item" data-nav="profile" title="Your Cosmic Profile & Matrix">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      <span>Profile</span>
    </a>
  `;'''

new_init_fn = '''  const nav = document.createElement('nav');
  nav.className = 'nv-sticky-bottom-nav';
  nav.setAttribute('aria-label', 'Mobile and Tablet Navigation');
  nav.innerHTML = `
    <a href="/" class="nv-bottom-nav-item" data-nav="home" title="Home">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      <span>Home</span>
    </a>
    <a href="/calculators/" class="nv-bottom-nav-item" data-nav="calculate" title="Calculate">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      <span>Calculate</span>
    </a>
    <a href="/reports_catalogue/" class="nv-bottom-nav-item" data-nav="reports" title="Reports">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      <span>Reports</span>
    </a>
    <a href="/dashboard/" class="nv-bottom-nav-item" data-nav="account" title="Account">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      <span>Account</span>
    </a>
  `;'''

if old_init_fn in nav_js:
    nav_js = nav_js.replace(old_init_fn, new_init_fn)
    print("Updated initStickyBottomNav() in nav.js to 4 items")
else:
    print("Warning: old_init_fn not found in nav.js")

with open('app/static/js/nav.js', 'w', encoding='utf-8') as f:
    f.write(nav_js)

# ── 2. UPDATE STATIC BOTTOM NAV ON REPORTS_CATALOGUE.HTML & INDEX.HTML ─────────
canonical_4item_bottom = '''  <!-- ── MOBILE 4-ITEM STICKY BOTTOM NAVIGATION BAR ── -->
  <nav class="nv-sticky-bottom-nav" aria-label="Mobile and Tablet Sticky Navigation">
    <a href="/" class="nv-bottom-nav-item" data-nav="home" title="Home">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      <span>Home</span>
    </a>
    <a href="/calculators/" class="nv-bottom-nav-item" data-nav="calculate" title="Calculate">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      <span>Calculate</span>
    </a>
    <a href="/reports_catalogue/" class="nv-bottom-nav-item" data-nav="reports" title="Reports">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      <span>Reports</span>
    </a>
    <a href="/dashboard/" class="nv-bottom-nav-item" data-nav="account" title="Account">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
      <span>Account</span>
    </a>
  </nav>'''

# Apply to reports_catalogue.html
with open('app/static/reports_catalogue.html', 'r', encoding='utf-8') as f:
    rc_html = f.read()

import re
rc_html_updated = re.sub(r'<!-- ── 8\. MOBILE.*?<\/nav>', canonical_4item_bottom, rc_html, flags=re.DOTALL)
if rc_html_updated != rc_html:
    with open('app/static/reports_catalogue.html', 'w', encoding='utf-8') as f:
        f.write(rc_html_updated)
    print("Updated reports_catalogue.html to 4-item bottom navigation")

# Apply to index.html
with open('app/static/index.html', 'r', encoding='utf-8') as f:
    idx_html = f.read()

idx_html_updated = re.sub(r'<!-- ── 14\. MOBILE.*?<\/nav>', canonical_4item_bottom, idx_html, flags=re.DOTALL)
if idx_html_updated != idx_html:
    with open('app/static/index.html', 'w', encoding='utf-8') as f:
        f.write(idx_html_updated)
    print("Updated index.html to 4-item bottom navigation")

# ── 3. UPDATE CUSTOMER-INTENT HAMBURGER MENU IN INDEX.HTML ──────────────────
intent_menu = '''        <ul class="nv-nav-menu" id="nvNavMenu">
          <!-- 1. Home -->
          <li class="nv-nav-item">
            <a href="/" class="nv-nav-link active" title="Numeros Vision Home">Home</a>
          </li>

          <!-- 2. Explore (Calculators) -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Explore Calculators</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/calculators/" class="nv-submenu-link"><span class="nv-sub-icon">🔢</span> <span>All Calculators Directory</span> <span class="nv-sub-tag">Free</span></a></li>
              <li><a href="/tools/life-path-calculator" class="nv-submenu-link"><span class="nv-sub-icon">🧭</span> <span>Birth Number &amp; Life Path</span></a></li>
              <li><a href="/tools/name-balancing" class="nv-submenu-link"><span class="nv-sub-icon">✍️</span> <span>Name &amp; Mobile Number Balancing</span></a></li>
              <li><a href="/calculators/lo-shu-grid/" class="nv-submenu-link"><span class="nv-sub-icon">🔲</span> <span>Lo Shu Magic 3×3 Grid</span></a></li>
              <li><a href="/tools/kundali-milan" class="nv-submenu-link"><span class="nv-sub-icon">💍</span> <span>Compatibility &amp; Partner Synastry</span></a></li>
              <li><a href="/tools/baby-naming" class="nv-submenu-link"><span class="nv-sub-icon">👶</span> <span>Auspicious Baby Naming Studio</span></a></li>
              <li class="nv-submenu-footer"><a href="/calculators/" class="nv-submenu-all">View All 10+ Working Calculators →</a></li>
            </ul>
          </li>

          <!-- 3. Personalised Reports -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Personalised Reports</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/reports_catalogue/?topic=love_marriage" class="nv-submenu-link"><span class="nv-sub-icon">💖</span> <span>Love &amp; Marriage Synastry</span></a></li>
              <li><a href="/reports_catalogue/?topic=business_growth" class="nv-submenu-link"><span class="nv-sub-icon">💼</span> <span>Money &amp; Business Strategy</span></a></li>
              <li><a href="/reports_catalogue/?topic=career_transition" class="nv-submenu-link"><span class="nv-sub-icon">🚀</span> <span>Career &amp; Professional Transition</span></a></li>
              <li><a href="/reports_catalogue/?topic=vedic_destiny" class="nv-submenu-link"><span class="nv-sub-icon">📜</span> <span>Self &amp; Spiritual Growth Dossier</span></a></li>
              <li class="nv-submenu-footer"><a href="/reports_catalogue/" class="nv-submenu-all">Browse All 10 Specialised Reports →</a></li>
            </ul>
          </li>

          <!-- 4. Intelligence & Guidance -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Intelligence &amp; Guidance</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/#charm-ai" class="nv-submenu-link"><span class="nv-sub-icon">✨</span> <span>Charm AI Conversational Oracle</span></a></li>
              <li><a href="/#charm-profile" class="nv-submenu-link"><span class="nv-sub-icon">🏛️</span> <span>Four-Layer Charm Profile</span></a></li>
              <li><a href="/sample-report/" class="nv-submenu-link"><span class="nv-sub-icon">📑</span> <span>Sample Report Preview (Specimen)</span></a></li>
              <li><a href="/methodology/" class="nv-submenu-link"><span class="nv-sub-icon">📐</span> <span>Deterministic Methodology</span></a></li>
              <li><a href="/consultation/" class="nv-submenu-link"><span class="nv-sub-icon">👤</span> <span>1-on-1 Master Consultation (₹1,050)</span></a></li>
            </ul>
          </li>

          <!-- 5. Learn & Support -->
          <li class="nv-nav-item nv-has-dropdown">
            <button class="nv-nav-link nv-dropdown-toggle" onclick="toggleNavAccordion(this, event)" aria-expanded="false" type="button">
              <span>Learn &amp; Support</span>
              <svg class="nv-chevron" viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2.5"><path d="m6 9 6 6 6-6"/></svg>
            </button>
            <ul class="nv-submenu">
              <li><a href="/insights/" class="nv-submenu-link"><span class="nv-sub-icon">📚</span> <span>Learning Centre &amp; Research</span></a></li>
              <li><a href="/#faq" class="nv-submenu-link"><span class="nv-sub-icon">❓</span> <span>Frequently Asked Questions</span></a></li>
              <li><a href="/contact/" class="nv-submenu-link"><span class="nv-sub-icon">✉️</span> <span>Contact Support</span></a></li>
              <li><a href="/privacy-policy/" class="nv-submenu-link"><span class="nv-sub-icon">🛡️</span> <span>Privacy &amp; Terms Governance</span></a></li>
              <li><a href="/about/" class="nv-submenu-link"><span class="nv-sub-icon">🏛️</span> <span>About Numeros Vision</span></a></li>
            </ul>
          </li>

          <!-- 6. View Plans & Pricing -->
          <li class="nv-nav-item">
            <a href="/pricing/" class="nv-nav-link" title="Plans & Pricing">View Plans &amp; Pricing</a>
          </li>

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
        </ul>'''

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    cur_idx = f.read()

cur_idx_updated = re.sub(r'<ul class="nv-nav-menu" id="nvNavMenu">.*?<\/ul>', intent_menu, cur_idx, flags=re.DOTALL)
if cur_idx_updated != cur_idx:
    with open('app/static/index.html', 'w', encoding='utf-8') as f:
        f.write(cur_idx_updated)
    print("Updated index.html with customer-intent grouped hamburger menu")
else:
    print("Warning: could not replace #nvNavMenu in index.html")

print("Mobile navigation and menu alignment complete!")
