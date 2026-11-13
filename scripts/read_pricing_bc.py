import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/pricing.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'(<nav[^>]*class=["\']nv-breadcrumbs["\'].*?</nav>)', text, re.DOTALL)
if m:
    print('Pricing breadcrumbs:\n', m.group(1))
else:
    # check any breadcrumbs in pricing
    m2 = re.search(r'(<[^>]*breadcrumbs[^>]*>.*?</[^>]*>)', text, re.DOTALL)
    print('Found:', m2.group(0)[:200] if m2 else 'None')
