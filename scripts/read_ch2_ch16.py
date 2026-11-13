import pypdf

reader = pypdf.PdfReader('data/uploaded_books_and_notes/nadi-astrology-accurate-predictive-methodology-2013nbsped_compress.pdf')

print("=== CHAPTER 2 (PDF pages 13-20) ===")
for p in range(12, 22):
    t = reader.pages[p].extract_text()
    lines = [line.strip() for line in t.split('\n') if line.strip()]
    print(f"\n--- PDF Page {p+1} ---")
    for l in lines[:10]:
        print("  ", l.encode('ascii', errors='replace').decode('ascii'))

print("\n=== CHAPTER 16 REMEDIAL MEASURES (PDF pages 228-234) ===")
for p in range(227, 235):
    t = reader.pages[p].extract_text()
    lines = [line.strip() for line in t.split('\n') if line.strip()]
    print(f"\n--- PDF Page {p+1} ---")
    for l in lines[:10]:
        print("  ", l.encode('ascii', errors='replace').decode('ascii'))
