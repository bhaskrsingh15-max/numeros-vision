import sys
import os
import pypdf

sys.path.insert(0, os.path.abspath('.'))
from app.services.pdf_report_generator import generate_customised_pdf_report

print("Testing dynamic asset input...")
pdf_bytes, meta = generate_customised_pdf_report(
    name="Bhaskr Singh",
    day=28,
    month=11,
    year=1981,
    topic_id="core_blueprint",
    tier="premium",
    mobile_number="9818418039",
    vehicle_number="DL01AB1234",
    property_number="Flat 402"
)

test_pdf_path = "test_premium_dynamic.pdf"
with open(test_pdf_path, "wb") as f:
    f.write(pdf_bytes)

reader = pypdf.PdfReader(test_pdf_path)
print(f"Total pages: {len(reader.pages)}")

# Extract text of page 22 (Mobile) and page 27 (Vehicle/Property)
p22_text = reader.pages[21].extract_text()
p27_text = reader.pages[26].extract_text()

print("\n--- PAGE 22 (Mobile) ---")
print(p22_text[:400])

print("\n--- PAGE 27 (Vehicle & Property) ---")
print(p27_text[:500])

assert "9818418039" in p22_text, "Mobile number not found in Page 22!"
assert "DL01AB1234" in p27_text, "Vehicle plate not found in Page 27!"
assert "Flat 402" in p27_text, "Property number not found in Page 27!"

os.remove(test_pdf_path)
print("\n>>> ALL DYNAMIC ASSET CHECKS PASSED PERFECTLY!")
