import os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('.'))

from app.services.pdf_report_generator import generate_customised_pdf_report
import pypdf

name = "Alexander Vance"
day = 18
month = 10
year = 1990

tiers = [
    ("basic", "Numeros_Vision_Basic_Report_Alexander_Vance.pdf", 3),
    ("basic", "Numeros_Vision_Executive_Brief_Alexander_Vance.pdf", 3),
    ("advanced", "Numeros_Vision_Advanced_Report_Alexander_Vance.pdf", 12),
    ("premium", "Numeros_Vision_Premium_Report_Alexander_Vance.pdf", 32)
]

for tier, fname, exp_pages in tiers:
    print(f"Generating {tier} for {name} ({day}-{month}-{year})...")
    pdf_bytes, meta = generate_customised_pdf_report(
        name=name,
        day=day,
        month=month,
        year=year,
        tier=tier
    )
    for folder in ['app/static/reports', 'dist_cloudflare_pages/reports']:
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, fname)
        with open(path, 'wb') as f:
            f.write(pdf_bytes)
        print(f"  Saved to {path} ({len(pdf_bytes)} bytes)")

    reader = pypdf.PdfReader(os.path.join('dist_cloudflare_pages/reports', fname))
    print(f"  Verified pages: {len(reader.pages)} (Expected: {exp_pages})")
    assert len(reader.pages) == exp_pages, f"Expected {exp_pages} pages, got {len(reader.pages)}"

print("All Alexander Vance reports generated and verified successfully!")
