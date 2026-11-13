import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def _assemble_premium_32_pages' in l:
        for j in range(i, min(i + 60, len(lines))):
            print(f'{j+1}: {lines[j]}', end='')
        break
