import os
import sys
import json
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

fp = r'data\uploaded_books_and_notes\ADVANCE & PROFESSIONAL COURSE - NOTES.pdf'
reader = PdfReader(fp)

# Extract pages 6, 7, 8, 9, 24
extracted_text = {}
for p_num in [6, 7, 8, 9, 24]:
    text = reader.pages[p_num - 1].extract_text()
    extracted_text[p_num] = text

for p_num, text in extracted_text.items():
    print(f'=== Page {p_num} ===')
    print(text)
    print('-' * 40)
