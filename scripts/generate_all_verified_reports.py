import os, sys
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.abspath('.'))

from app.services.pdf_report_generator import generate_customised_pdf_report
import pypdf

tasks = [
    # Bhaskr Singh
    ("Bhaskr Singh", 28, 11, 1981, "basic", "Numeros_Vision_Basic_Report_28-11-1981.pdf", 3),
    ("Bhaskr Singh", 28, 11, 1981, "advanced", "Numeros_Vision_Advanced_Report_28-11-1981.pdf", 12),
    ("Bhaskr Singh", 28, 11, 1981, "premium", "Numeros_Vision_Premium_Report_28-11-1981.pdf", 32),
    # Alexander Vance
    ("Alexander Vance", 18, 10, 1990, "basic", "Numeros_Vision_Basic_Report_Alexander_Vance.pdf", 3),
    ("Alexander Vance", 18, 10, 1990, "basic", "Numeros_Vision_Executive_Brief_Alexander_Vance.pdf", 3),
    ("Alexander Vance", 18, 10, 1990, "advanced", "Numeros_Vision_Advanced_Report_Alexander_Vance.pdf", 12),
    ("Alexander Vance", 18, 10, 1990, "premium", "Numeros_Vision_Premium_Report_Alexander_Vance.pdf", 32),
]

for name, d, m, y, tier, fname, exp_pages in tasks:
    print(f"Generating {tier} ({exp_pages} pgs) for {name} ({d}-{m}-{y})...")
    pdf_bytes, meta = generate_customised_pdf_report(
        name=name,
        day=d,
        month=m,
        year=y,
        tier=tier
    )
    for folder in ['app/static/reports', 'dist_cloudflare_pages/reports']:
        os.makedirs(folder, exist_ok=True)
        path = os.path.join(folder, fname)
        with open(path, 'wb') as f:
            f.write(pdf_bytes)

    dist_path = os.path.join('dist_cloudflare_pages/reports', fname)
    reader = pypdf.PdfReader(dist_path)
    actual_pages = len(reader.pages)
    print(f"  Saved {fname}: {len(pdf_bytes)} bytes, pages={actual_pages}")
    assert actual_pages == exp_pages, f"Page mismatch: expected {exp_pages}, got {actual_pages}"

print("\nALL 7 AUTHORITATIVE REPORTS GENERATED AND VERIFIED WITH 100% SUCCESS!")
