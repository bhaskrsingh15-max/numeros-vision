import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'def draw_page_decorations.*?(?=\n\s*def|\nclass|\Z)', text, re.DOTALL)
if m:
    print(m.group(0)[:1500])
