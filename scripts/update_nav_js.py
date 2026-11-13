# -*- coding: utf-8 -*-
with open('app/static/js/nav.js', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update updateBottomNavActive to support charm
old_check = "    } else if (nav === 'reports' && (path.includes('reports') || path.includes('catalogue'))) {"
new_check = """    } else if (nav === 'charm' && (path.includes('charm') || hash === '#charm-ai')) {
      isActive = true;
    } else if (nav === 'reports' && (path.includes('reports') || path.includes('catalogue'))) {"""

if old_check in text:
    text = text.replace(old_check, new_check, 1)
    print("SUCCESS: Updated active check in nav.js")
else:
    print("Warning: old_check not found in nav.js")

# 2. Update initStickyBottomNav to include center Charm AI item
old_injection = """    <a href="/calculators/" class="nv-bottom-nav-item" data-nav="calculate" title="Calculate">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      <span>Calculate</span>
    </a>
    <a href="/reports_catalogue/" class="nv-bottom-nav-item" data-nav="reports" title="Reports">"""

new_injection = """    <a href="/calculators/" class="nv-bottom-nav-item" data-nav="calculate" title="Calculate">
      <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/></svg>
      <span>Calculate</span>
    </a>
    <a href="/charm_ai.html" class="nv-bottom-nav-item nv-bottom-nav-center" data-nav="charm" title="Charm AI Oracle">
      <div class="nv-bottom-center-btn">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/></svg>
      </div>
      <span>Charm AI</span>
    </a>
    <a href="/reports_catalogue/" class="nv-bottom-nav-item" data-nav="reports" title="Reports">"""

old_injection_crlf = old_injection.replace('\n', '\r\n')
new_injection_crlf = new_injection.replace('\n', '\r\n')

if old_injection_crlf in text:
    text = text.replace(old_injection_crlf, new_injection_crlf, 1)
    print("SUCCESS: Updated bottom nav injection in nav.js (CRLF)")
elif old_injection in text:
    text = text.replace(old_injection, new_injection, 1)
    print("SUCCESS: Updated bottom nav injection in nav.js (LF)")
else:
    print("Warning: old_injection not found in nav.js")

with open('app/static/js/nav.js', 'w', encoding='utf-8') as f:
    f.write(text)
