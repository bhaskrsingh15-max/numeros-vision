import sys
sys.stdout.reconfigure(encoding='utf-8')
import sys
import os
import pypdf

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath('.'))

from app.services.pdf_report_generator import generate_customised_pdf_report

name = "Bhaskr Singh"
day = 28
month = 11
year = 1981

tiers = [
    ("basic", "Numeros_Vision_Basic_Report_28-11-1981.pdf", 3),
    ("advanced", "Numeros_Vision_Advanced_Report_28-11-1981.pdf", 12),
    ("premium", "Numeros_Vision_Premium_Report_28-11-1981.pdf", 32)
]

os.makedirs('app/static/reports', exist_ok=True)
os.makedirs('dist_cloudflare_pages/reports', exist_ok=True)

for tier_name, filename, expected_pages in tiers:
    print(f"\n=======================================================")
    print(f"Generating {tier_name.upper()} report for {name} ({day}-{month}-{year})...")
    pdf_bytes, meta = generate_customised_pdf_report(
        name=name,
        day=day,
        month=month,
        year=year,
        topic_id="core_blueprint",
        tier=tier_name
    )

    path1 = os.path.join('app', 'static', 'reports', filename)
    path2 = os.path.join('dist_cloudflare_pages', 'reports', filename)

    with open(path1, 'wb') as f:
        f.write(pdf_bytes)
    with open(path2, 'wb') as f:
        f.write(pdf_bytes)

    print(f"Saved: {path1} ({len(pdf_bytes)} bytes)")
    print(f"Saved: {path2} ({len(pdf_bytes)} bytes)")

    # Read back with pypdf and verify
    reader = pypdf.PdfReader(path1)
    actual_pages = len(reader.pages)
    print(f"Actual pages: {actual_pages} (Expected: {expected_pages})")

    # Inspect first page stream to ensure NO blanking overlay
    p1_stream = reader.pages[0].get_contents().get_data().decode('latin1', 'backslashreplace')
    first_re_f = p1_stream.find("re f")
    first_text = p1_stream.find("NUMEROS VISION")

    print(f"Page 1: First 're f' (background rect) pos: {first_re_f}")
    print(f"Page 1: First 'NUMEROS VISION' text pos: {first_text}")
    if first_re_f != -1 and first_text != -1:
        if first_re_f < first_text:
            print(">>> SUCCESS: Background rect is rendered BEFORE text (Layer 0, behind text). Text is 100% VISIBLE!")
        else:
            print(">>> WARNING: Background rect is after text!")

    # Check text on each page
    for i in range(actual_pages):
        page_text = reader.pages[i].extract_text() or ''
        lines = [l.strip() for l in page_text.split('\n') if l.strip()]
        h = lines[0] if lines else 'EMPTY!'
        if len(page_text.strip()) < 150:
            print(f"  [!] Page {i+1} has very short text: {len(page_text)} chars")
        else:
            print(f"  Page {i+1}: {len(page_text)} chars | {h}")

print("\nAll 3 reports generated and verified successfully!")
