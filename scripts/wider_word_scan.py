import re
import sys
import json
import hashlib
import pypdf

WORDS = [
    'will', 'must', 'never', 'definitely', 'certain', 'destined', 'fate',
    'lucky', 'ensure', 'guarantee', 'unlock', 'cure', 'heal', 'remove', 'brings'
]

def scan_text(name, text):
    print(f"\n============================================================")
    print(f"SCAN REPORT: {name}")
    print(f"Total characters: {len(text)}")
    print("============================================================")
    total_hits = 0
    hits_by_word = {}
    contexts = {}

    for w in WORDS:
        # Match whole word, case-insensitive, including plurals/conjugations where relevant
        if w in ['ensure', 'guarantee', 'unlock', 'cure', 'heal', 'remove']:
            pattern = rf'\b{w}(?:s|d|ed|ing)?\b'
        elif w == 'destined':
            pattern = rf'\b(?:destined|destiny)\b'
        elif w == 'fate':
            pattern = rf'\b(?:fate|fates|fated)\b'
        elif w == 'certain':
            pattern = rf'\b(?:certain|certainly|certainty)\b'
        elif w == 'brings':
            pattern = rf'\b(?:brings|bring|bringing)\b'
        else:
            pattern = rf'\b{w}\b'

        matches = list(re.finditer(pattern, text, re.IGNORECASE))
        hits_by_word[w] = len(matches)
        total_hits += len(matches)
        
        # Collect sample contexts (up to 5 per word)
        contexts[w] = []
        for m in matches:
            start = max(0, m.start() - 50)
            end = min(len(text), m.end() + 50)
            snippet = text[start:end].replace('\n', ' ').strip()
            contexts[w].append((m.group(0), snippet))

    print(f"TOTAL FLAGGED HITS: {total_hits}")
    for w in WORDS:
        count = hits_by_word[w]
        print(f"  - {w:15}: {count:3} hits")
        if count > 0:
            for match_str, snippet in contexts[w][:3]:
                print(f"       -> [{match_str}]: ...{snippet}...")
            if count > 3:
                print(f"       -> (...and {count - 3} more)")
    return hits_by_word, total_hits

def scan_pdf(name, path):
    with open(path, 'rb') as f:
        data = f.read()
    sha = hashlib.sha256(data).hexdigest()
    reader = pypdf.PdfReader(path)
    full_text = ""
    for page_idx, page in enumerate(reader.pages):
        full_text += f"\n--- Page {page_idx+1} ---\n" + (page.extract_text() or "")
    print(f"\nPDF File: {path} | SHA-256: {sha} | Pages: {len(reader.pages)}")
    return scan_text(name, full_text)

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    
    # 1. Content Library
    with open('data/planner_2027_content_library.json', 'r', encoding='utf-8') as f:
        lib_data = f.read()
    scan_text("data/planner_2027_content_library.json", lib_data)

    # 2. Sample Arun Sharma PDF
    scan_pdf("Sample A: Arun Sharma 2027 PDF", "pdf_service/output/sample_arun_sharma_2027.pdf")

    # 3. Sample Anil Kumar PDF
    scan_pdf("Sample B: Anil Kumar 2027 PDF", "pdf_service/output/sample_anil_kumar_2027.pdf")

    # 4. Sales Page year_2027.html
    with open('app/static/year_2027.html', 'r', encoding='utf-8') as f:
        html_data = f.read()
    scan_text("app/static/year_2027.html", html_data)
