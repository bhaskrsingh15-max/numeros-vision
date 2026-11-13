import os
import sys
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

fp = r'data\uploaded_books_and_notes\81 Driver Conductor Combinations PDF Planets In Astrology Planets.pdf'
reader = PdfReader(fp)
for i, page in enumerate(reader.pages):
    print(f'=== Page {i+1} ===')
    txt = page.extract_text()
    for line in txt.split('\n'):
        if line.strip():
            print(line.strip())
