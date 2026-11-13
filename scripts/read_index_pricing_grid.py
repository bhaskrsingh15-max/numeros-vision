import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'<div class="pricing-grid">(.*?)</div>\s*</div>\s*</section>', text, re.DOTALL)
if m:
    print(m.group(0))
