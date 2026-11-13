import os, hashlib
from pypdf import PdfReader

target_dir = 'c:/Users/Bhaskr Singh/Downloads'
files = [
    'Numeros Vision Classical Sound and Name Compendium 2005 PDF Classical Chaldean Tradition.pdf',
    'Chaldean Numerology PDF Numbers Pythagoras.pdf',
    'Classical Nine-Square Lo Shu System PDF.pdf',
    'Classical Nine-Square Lo Shu System PDF (1).pdf',
    'Planetary and Number Symbolism Archive PDF Planets In Astrology Angel.pdf',
    'Planetary and Number Symbolism Archive PDF Planets In Astrology Angel (1).pdf',
    'Numeros Vision Classical Numerology Manual 1945 PDF Pi Numbers.pdf',
    'Numeros Vision Classical Numerology Manual 1945 PDF Pi Numbers (1).pdf',
    'Understanding Numerology Basics PDF.pdf',
    'Understanding Numerology Basics PDF (1).pdf'
]

results = []

for fname in files:
    fpath = os.path.join(target_dir, fname)
    if not os.path.exists(fpath):
        print(f"NOT FOUND: {fname}")
        continue
    size = os.path.getsize(fpath)
    with open(fpath, 'rb') as fp:
        h = hashlib.sha256(fp.read()).hexdigest()
    
    try:
        reader = PdfReader(fpath)
        page_count = len(reader.pages)
        # Check text layer on sample pages (e.g. first 5 pages, middle pages)
        text_samples = []
        for i in range(min(5, page_count)):
            txt = reader.pages[i].extract_text() or ''
            if txt.strip():
                text_samples.append(txt.strip())
        has_text = "yes" if len(text_samples) >= 3 else ("partial" if len(text_samples) > 0 else "no")
    except Exception as e:
        page_count = -1
        has_text = f"error: {e}"
        
    results.append({
        "filename": fname,
        "size": size,
        "sha256": h,
        "pages": page_count,
        "has_text": has_text
    })

print(f"{'Filename':<70} | {'Size':<10} | {'Pages':<6} | {'Text':<8} | {'SHA256':<64}")
print("-" * 170)
for r in results:
    print(f"{r['filename']:<70} | {r['size']:<10} | {r['pages']:<6} | {r['has_text']:<8} | {r['sha256']}")
