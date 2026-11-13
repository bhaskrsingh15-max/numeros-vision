import re

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

canonical_4item_bottom = '''<!-- ── MOBILE 4-ITEM STICKY BOTTOM NAVIGATION BAR ── -->
  <nav class="nv-sticky-bottom-nav" aria-label="Mobile and Tablet Sticky Navigation">
    <a href="/" class="nv-bottom-nav-item active" data-nav="home" title="Home">
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

# Replace <nav class="nv-sticky-bottom-nav".*?</nav>
text_new = re.sub(r'<nav class="nv-sticky-bottom-nav".*?<\/nav>', canonical_4item_bottom, text, flags=re.DOTALL)
if text_new != text:
    with open('app/static/index.html', 'w', encoding='utf-8') as f:
        f.write(text_new)
    print("Successfully updated index.html with 4-item bottom nav")
else:
    print("Warning: regex didn't match in index.html")
