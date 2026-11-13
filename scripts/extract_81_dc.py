import os
import sys
import json
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

fp = r'data\uploaded_books_and_notes\81 Driver Conductor Combinations PDF Planets In Astrology Planets.pdf'
reader = PdfReader(fp)
print(f'Total pages in 81 Driver Conductor Combinations: {len(reader.pages)}')

all_combinations = []
for p_idx, page in enumerate(reader.pages):
    text = page.extract_text()
    lines = text.split('\n')
    for line in lines:
        line_clean = line.strip()
        parts = line_clean.split()
        if len(parts) >= 5 and parts[0].isdigit() and parts[1].isdigit():
            d = int(parts[0])
            c = int(parts[1])
            if 1 <= d <= 9 and 1 <= c <= 9:
                all_combinations.append((d, c, line_clean))

print(f'Extracted {len(all_combinations)} driver-conductor lines directly.')
for combo in all_combinations[:15]:
    print(combo)
if len(all_combinations) < 81:
    print('Some rows might have different formatting, let\'s dump all text lines for checking.')
