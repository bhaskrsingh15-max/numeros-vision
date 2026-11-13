import pypdf
import sys

sys.stdout.reconfigure(encoding="utf-8")
fpath = "data/nadi_books/Nadi Notes PDF Books Prediction.pdf"
reader = pypdf.PdfReader(fpath)

pages_to_extract = [1, 2, 3, 6, 7, 8, 16, 17, 18]

for pno in pages_to_extract:
    idx = pno - 1
    text = reader.pages[idx].extract_text() or ""
    print(f"==================== PAGE {pno} ====================")
    print(text[:1500])
    print("\n")
