import os, sys, pypdf
sys.stdout.reconfigure(encoding='utf-8')

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath('.'))

from app.services.pdf_report_generator import generate_customised_pdf_report

test_cases = [
    # (tier, topic_id, expected_pages, filename)
    ("basic", "present_numbers", 3, "Test_Basic_Present.pdf"),
    ("basic", "love_relationship", 3, "Test_Basic_Love.pdf"),
    ("basic", "career_wealth", 3, "Test_Basic_Career.pdf"),
    ("advanced", "present_numbers", 12, "Test_Advanced_12_Present_Numbers.pdf"),
    ("advanced", "love_relationship", 12, "Test_Advanced_12_Love_Relationship.pdf"),
    ("advanced", "career_wealth", 12, "Test_Advanced_12_Career_Wealth.pdf"),
    ("advanced", "missing_numbers_vastu", 12, "Test_Advanced_12_Missing_Numbers.pdf"),
    ("premium", "missing_numbers_vastu", 32, "Test_Premium_32_Sovereign_Missing.pdf"),
    ("premium", "present_numbers", 32, "Test_Premium_32_Present_Numbers.pdf"),
]

os.makedirs('app/static/reports', exist_ok=True)
all_passed = True

print("=== VERIFYING DYNAMIC TOPIC & TIER REPORT GENERATION ===")
for tier, topic_id, expected_pages, fname in test_cases:
    print(f"\n--- Testing Tier: {tier.upper()} | Topic: {topic_id} (Expected {expected_pages} pages) ---")
    pdf_bytes, meta = generate_customised_pdf_report(
        name="Bhaskr Singh",
        day=28,
        month=11,
        year=1981,
        topic_id=topic_id,
        tier=tier
    )

    out_path = os.path.join('app/static/reports', fname)
    with open(out_path, 'wb') as f:
        f.write(pdf_bytes)

    reader = pypdf.PdfReader(out_path)
    actual_pages = len(reader.pages)
    status = "[OK]" if actual_pages == expected_pages else "[FAIL]"
    print(f"{status} Actual Pages: {actual_pages} | Expected: {expected_pages} | Size: {len(pdf_bytes)} bytes")
    
    if actual_pages != expected_pages:
        all_passed = False
        print(f"ERROR: Page count mismatch for {tier} - {topic_id}!")
    
    # Check page 1 stream
    p1_stream = reader.pages[0].get_contents().get_data().decode('latin1', 'backslashreplace')
    first_re_f = p1_stream.find("re f")
    first_text = p1_stream.find("NUMEROS VISION")
    if first_re_f != -1 and first_text != -1 and first_re_f < first_text:
        print("  Background rect is behind text [OK]")
    else:
        print("  WARNING: Background check failed!")

    # Check text presence on every page
    for i in range(actual_pages):
        page_txt = reader.pages[i].extract_text() or ''
        lines = [l.strip() for l in page_txt.split('\n') if l.strip()]
        first_line = lines[0] if lines else 'EMPTY'
        if len(page_txt.strip()) < 100:
            print(f"  [!] Page {i+1} has low text: {len(page_txt)} chars")
            all_passed = False
        else:
            print(f"  Page {i+1}: {len(page_txt)} chars | {first_line[:65]}")

if all_passed:
    print("\n>>> ALL TEST CASES PASSED PERFECTLY WITH EXACT PAGE COUNTS! <<<")
else:
    print("\n>>> FAILURES DETECTED IN TEST SUITE! <<<")
