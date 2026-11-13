import sys
import re

with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'def _assemble_advanced_12_pages.*?(?=def _assemble_premium_32_pages)', text, re.DOTALL)
if m:
    adv_code = m.group(0)
    page_breaks = adv_code.count('PageBreak()')
    print("PageBreak() count in _assemble_advanced_12_pages:", page_breaks)
    # Print lines with PageBreak
    lines = adv_code.splitlines()
    for i, l in enumerate(lines):
        if 'PageBreak()' in l:
            # print surrounding context
            prev = lines[max(0, i-2)]
            print(f"Line {i}: {prev.strip()} -> {l.strip()}")
