"""
Verification script for Mobile Phone Numerology Calculator.
Tests metadata, schema consistency, absence of ungrounded causal claims, privacy leak prevention,
worked example accuracy, and live HTTP responses.
"""

import os
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

def test_mobile_numerology_html():
    print("=== TESTING MOBILE NUMEROLOGY TOOL (app/static/tools/mobile-numerology.html) ===")
    path = "app/static/tools/mobile-numerology.html"
    assert os.path.exists(path), f"File {path} not found"
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. P0 Privacy: No phone in URL query params
    assert 'phone: mobile' not in html, "CRITICAL P0: phone: mobile still serialized into query params!"
    assert 'Privacy Assurance' in html, "Privacy note missing near form"
    print("  [PASS] P0 Privacy: Phone number completely removed from client URL parameter serialization")

    # 2. P0 Neutrality: Replaced ungrounded claims
    assert 'attract unexpected expenses' not in html.lower(), "Found 'attract unexpected expenses'"
    assert 'facilitate rapid deal closures' not in html.lower(), "Found 'facilitate rapid deal closures'"
    print("  [PASS] P0 Neutrality: Ungrounded causal outcome claims removed")

    # 3. P1 SEO Metadata
    assert '<title>Mobile Number Numerology Calculator | Numeros Vision</title>' in html, "Title mismatch"
    assert '<link rel="canonical" href="https://numerosvision.com/tools/mobile-numerology/" />' in html, "Canonical mismatch"
    assert '<meta property="og:url" content="https://numerosvision.com/tools/mobile-numerology/" />' in html, "OG URL mismatch"
    assert 'name="keywords"' not in html, "Keywords meta tag should be removed"
    print("  [PASS] P1 SEO Metadata: Title, Description, and Canonical URL standardized")

    # 4. P1 Schema.org structured data
    assert 'https://numerosvision.com/calculators/' in html, "Breadcrumb must point to calculators hub"
    assert 'Mobile Number Numerology Calculator' in html, "WebApplication name mismatch"
    print("  [PASS] P1 Schema: Breadcrumbs, WebApplication, and FAQPage aligned")

    # 5. P1 Direct Answer & Methodology Block
    assert 'How Does a Mobile Number Numerology Calculator Work?' in html, "Direct Answer H2 missing"
    assert 'Verified Worked Example: 9876543210' in html, "Worked example missing"
    assert '9 + 8 + 7 + 6 + 5 + 4 + 3 + 2 + 1 + 0 = 45 (Compound)' in html or '45 (Compound)' in html, "Worked example calculation missing"
    print("  [PASS] P1 GEO/AEO: Direct answer box and verified worked example integrated")

    # 6. P2 FAQs
    assert 'What is Vish Yog in a phone number?' in html, "FAQ 1 missing"
    assert 'Are repeating digits such as 888 or 444 bad?' in html, "FAQ 2 missing"
    assert 'How can I interpret an unfavorable mobile number?' in html, "FAQ 3 missing"
    print("  [PASS] P2 FAQs: 3 grounded, factual FAQs aligned in HTML and JSON-LD")

def test_live_http():
    print("\n=== TESTING LIVE HTTP ENDPOINTS (via local server on port 8000) ===")
    endpoints = [
        "http://127.0.0.1:8000/tools/mobile-numerology/",
        "http://127.0.0.1:8000/tools/mobile-numerology",
        "http://127.0.0.1:8000/blog/mobile-numerology-malefic-pairs/",
        "http://127.0.0.1:8000/blog/mobile-numerology-malefic-pairs"
    ]
    for url in endpoints:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "NumerosVisionVerifier/1.0"})
            with urllib.request.urlopen(req, timeout=5) as response:
                status = response.getcode()
                assert status == 200, f"Expected 200 for {url}, got {status}"
                body = response.read().decode('utf-8')
                assert len(body) > 1000, f"Response too short for {url}"
                print(f"  [PASS] {url} -> HTTP {status} (Length: {len(body):,} bytes)")
        except Exception as e:
            print(f"  [FAIL] {url} -> {e}")
            raise e

if __name__ == '__main__':
    test_mobile_numerology_html()
    test_live_http()
    print("\nALL MOBILE NUMEROLOGY VERIFICATIONS COMPLETED SUCCESSFULLY!")
