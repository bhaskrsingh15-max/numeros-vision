import hashlib
import sys
import pypdf

def extract_evidence(pdf_path):
    with open(pdf_path, 'rb') as f:
        file_bytes = f.read()
    sha256_hash = hashlib.sha256(file_bytes).hexdigest()
    
    reader = pypdf.PdfReader(pdf_path)
    total_pages = len(reader.pages)
    
    # Page 3 is index 2
    page3_text = reader.pages[2].extract_text()
    return sha256_hash, total_pages, len(file_bytes), page3_text

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    files = [
        ('Arun Sharma (Sample A)', 'pdf_service/output/sample_arun_sharma_2027.pdf'),
        ('Anil Kumar (Sample B)', 'pdf_service/output/sample_anil_kumar_2027.pdf'),
    ]
    for label, path in files:
        sha, pages, size, text = extract_evidence(path)
        print(f"============================================================")
        print(f"EVIDENCE: {label}")
        print(f"File Path: {path}")
        print(f"SHA-256: {sha}")
        print(f"File Size: {size} bytes")
        print(f"Total Pages: {pages}")
        print(f"Verbatim Extracted Text of Page 3:")
        print(f"------------------------------------------------------------")
        print(text.strip())
        print(f"============================================================\n")
