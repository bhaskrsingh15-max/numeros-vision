import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

css_path = r"app\static\css\roadmap_components.css"
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

print("=== VERIFYING CSS BREAKPOINTS IN ROADMAP_COMPONENTS.CSS ===")

# Check 1: Desktop display: none on nv-sticky-bottom-nav
m1 = re.search(r'\.nv-sticky-bottom-nav\s*\{\s*display:\s*none', css)
print("1. Desktop bottom nav hidden by default:", bool(m1))

# Check 2: Max-width 1199px displays bottom nav flex with safe-area padding
m2 = re.search(r'@media\s*\(max-width:\s*1199px\)[^\{]*\{.*?\.nv-sticky-bottom-nav\s*\{[^}]*display:\s*flex[^}]*safe-area-inset-bottom', css, re.DOTALL)
print("2. Mobile/Tablet (<=1199px) bottom nav flex with safe-area padding:", bool(m2))

# Check 3: Max-width 1199px body safe padding
m3 = re.search(r'@media\s*\(max-width:\s*1199px\)[^\{]*\{.*?body\s*\{[^}]*padding-bottom:\s*calc\(76px\s*\+\s*env\(safe-area-inset-bottom', css, re.DOTALL)
print("3. Mobile/Tablet (<=1199px) body padding-bottom safe-area:", bool(m3))

# Check 4: Tablet dock 600px - 1199px
m4 = re.search(r'@media\s*\(min-width:\s*600px\)\s*and\s*\(max-width:\s*1199px\)[^\{]*\{.*?\.nv-sticky-bottom-nav\s*\{[^}]*max-width:\s*520px', css, re.DOTALL)
print("4. Tablet dock (600px - 1199px) max-width 520px centered:", bool(m4))

# Check 5: Reports catalogue responsive rules
rc_path = r"app\static\reports_catalogue.html"
with open(rc_path, 'r', encoding='utf-8') as f:
    rc = f.read()
m5 = 'MOBILE & TABLET RESPONSIVE REFINEMENTS' in rc
m6 = 'nv-cat-tabs' in rc and 'overflow-x: auto' in rc
m7 = 'class="nv-bottom-nav-item active" data-nav="reports"' in rc
print("5. reports_catalogue.html has responsive rules:", m5)
print("6. reports_catalogue.html has swipeable category tabs:", m6)
print("7. reports_catalogue.html has active reports tab:", m7)

print("\n=== AUDITING ALL STATIC HTML PAGES ===")
static_dir = r"app\static"
total_html = 0
valid_bottom_nav = 0
for root, dirs, files in os.walk(static_dir):
    if 'amp' in root:
        continue
    for f in files:
        if f.endswith('.html'):
            total_html += 1
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8') as fp:
                c = fp.read()
            if 'nv-sticky-bottom-nav' in c and '<svg' in c and 'data-nav="home"' in c and 'data-nav="calculate"' in c and 'data-nav="reports"' in c and 'data-nav="account"' in c:
                valid_bottom_nav += 1
            else:
                print(f"File missing standardized 4-item SVG bottom nav: {p}")

print(f"Total HTML pages audited: {total_html}")
print(f"Standardized 4-item SVG bottom nav pages: {valid_bottom_nav}/{total_html}")
