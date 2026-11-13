import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'def _assemble_advanced_12_pages.*?(?=\ndef _assemble_premium_32_pages)', text, re.DOTALL)
if m:
    print(m.group(0)[:2000])
