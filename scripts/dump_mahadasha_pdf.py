import os
import sys
import json
from pypdf import PdfReader

sys.stdout.reconfigure(encoding='utf-8')

fp = r'data\uploaded_books_and_notes\Calculating Mahadasha in Vedic Astrology PDF Planets In Astrology Self-Improvement.pdf'
reader = PdfReader(fp)
print(f'Total pages: {len(reader.pages)}')

mahadasha_data = {
    'system': 'Numerological Mahadasha (Numeros Vision / Vedic Numerology)',
    'source': 'SRC-NUMERO-MAHADASHA',
    'calculation_rules': [],
    'mahadasha_periods_by_number': {},
    'rating_rules': [],
    'remedy_framework': []
}

for i, page in enumerate(reader.pages):
    txt = page.extract_text() or ''
    print(f'=== Page {i+1} ===')
    print(txt[:600])
    print('-' * 40)
