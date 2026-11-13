import sys
import re

with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'def _assemble_advanced_12_pages.*?(?=def _assemble_premium_32_pages)', text, re.DOTALL)
if m:
    adv_code = m.group(0)
    lines = adv_code.splitlines()
    for i in range(215, len(lines)):
        print(f'{i}: {lines[i]}')
