import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/css/roadmap_components.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re

for selector in ['.nv-breadcrumbs', '.nv-sticky-bottom-nav', '.nv-footer', '.nv-btn-cta', '.nv-card']:
    m = re.search(r'(' + re.escape(selector) + r'\s*\{[^}]+\})', text)
    if m:
        print(m.group(1))
        print('-'*40)
