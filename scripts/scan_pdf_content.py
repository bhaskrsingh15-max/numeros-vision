import hashlib
import re
import sys
import pypdf

FLAGGED = [
    'prevents', 'brings', 'keeps', 'makes', 'creates', 'proves', 'builds',
    'guarantees', 'ensures', 'secures', 'peace of mind', 'mental peace',
    'highly productive', 'greatly', 'always'
]

def scan_pdf(pdf_path):
    with open(pdf_path, 'rb') as f:
        data = f.read()
    sha = hashlib.sha256(data).hexdigest()
    reader = pypdf.PdfReader(pdf_path)
    
    hits = {w: [] for w in FLAGGED}
    full_text_by_page = []
    
    for page_idx, page in enumerate(reader.pages):
        page_num = page_idx + 1
        txt = page.extract_text() or ""
        full_text_by_page.append((page_num, txt))
        
        for w in FLAGGED:
            matches = re.findall(rf'\b{re.escape(w)}\b', txt, re.IGNORECASE)
            if matches:
                hits[w].append((page_num, len(matches)))
                
    return sha, len(reader.pages), len(data), hits

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    pdfs = [
        ('Arun Sharma (Sample A)', 'pdf_service/output/sample_arun_sharma_2027.pdf'),
        ('Anil Kumar (Sample B)', 'pdf_service/output/sample_anil_kumar_2027.pdf')
    ]
    
    print("============================================================")
    print("SCANNING GENERATED PDF DELIVERABLES FOR FLAGGED WORDS")
    print(f"Flagged terms ({len(FLAGGED)}): {', '.join(FLAGGED)}")
    print("============================================================\n")
    
    for label, path in pdfs:
        sha, pages, size, hits = scan_pdf(path)
        print(f"PDF: {label}")
        print(f"File Path: {path}")
        print(f"SHA-256: {sha}")
        print(f"File Size: {size} bytes | Page Count: {pages}")
        
        total_hits = sum(sum(count for _, count in page_hits) for page_hits in hits.values())
        print(f"Total Flagged Hits in PDF Text: {total_hits}")
        
        for w, page_hits in hits.items():
            count = sum(c for _, c in page_hits)
            pages_str = ", ".join(f"p.{p} (x{c})" for p, c in page_hits) if page_hits else "None"
            print(f"  - {w:18}: {count:2} hits  [{pages_str}]")
        print("------------------------------------------------------------\n")
