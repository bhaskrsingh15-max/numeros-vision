import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/services/pdf_report_generator.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'def _assemble_advanced_12_pages' in l:
        for j in range(i, min(i + 90, len(lines))):
            print(f'{j+1}: {lines[j]}', end='')
        break
