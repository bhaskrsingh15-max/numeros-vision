import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.stdout.reconfigure(encoding='utf-8')

from app.services.pdf_report_generator import generate_customised_pdf_report

os.makedirs("scratch", exist_ok=True)

for tier, expected_pages in [("basic", 3), ("advanced", 12), ("premium", 32)]:
    pdf_bytes, meta = generate_customised_pdf_report(
        name="Bhaskr Singh",
        day=15,
        month=7,
        year=1992,
        topic_id="vedic_destiny",
        tier=tier
    )
    pages = meta.get("pages_count")
    size = len(pdf_bytes)
    out_path = f"scratch/test_{tier}_report.pdf"
    with open(out_path, "wb") as f:
        f.write(pdf_bytes)
    print(f"Tier: {tier} -> Generated: {pages} pages (Expected: {expected_pages}), Size: {size} bytes")
    assert pages == expected_pages, f"Expected {expected_pages} pages, got {pages}"

print("\nAll 3 tiers generated with exact page counts!")
