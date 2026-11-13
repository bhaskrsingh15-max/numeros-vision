import pypdf
import json

reader = pypdf.PdfReader('data/uploaded_books_and_notes/nadi-astrology-accurate-predictive-methodology-2013nbsped_compress.pdf')

def extract_section(start_pdf_page, end_pdf_page, out_file):
    pages_data = []
    for p in range(start_pdf_page - 1, end_pdf_page):
        t = reader.pages[p].extract_text()
        pages_data.append({
            "pdf_page": p + 1,
            "text": t
        })
    with open(out_file, 'w', encoding='utf-8') as f:
        json.dump(pages_data, f, indent=2, ensure_ascii=False)
    print(f"Extracted pages {start_pdf_page} to {end_pdf_page} into {out_file}")

# Chapter 2 starts around printed page 8 (PDF pages ~13 to 30)
# Let's search for "CHAPTER- 2" or "RULES OF NADI ASTROLOGY"
for p_idx, page in enumerate(reader.pages[:40]):
    t = page.extract_text()
    if "chapter- 2" in t.lower() or "rules of nadi" in t.lower():
        print(f"Chapter 2 found at PDF page {p_idx + 1}")

# Search for Chapter 16 Remedial Measures
for p_idx, page in enumerate(reader.pages[210:250]):
    t = page.extract_text()
    if "remedial measures" in t.lower() or "chapter- 16" in t.lower() or "chapter" in t.lower() and "16" in t:
        print(f"Chapter 16 found at PDF page {p_idx + 211}")

