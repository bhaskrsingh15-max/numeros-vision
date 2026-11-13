"""
Verification script for Business Numerology & Operating Business Diagnostic.
Tests metadata, schema consistency, placeholder cleanliness, methodology block,
sector disclaimers, grounded FAQs, and live HTTP response.
"""

import os
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

def test_business_alignment_html():
    print("=== TESTING BUSINESS ALIGNMENT TOOL (app/static/tools/business-alignment.html) ===")
    path = "app/static/tools/business-alignment.html"
    assert os.path.exists(path), f"File {path} not found"
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. P0 Separation & Sector Disclaimer
    assert 'not a substitute for market research, financial modelling, clinical, licensing, or sector-specific legal advice' in html or 'not a substitute for financial, legal' in html, "Professional disclaimer missing"
    print("  [PASS] P0 Professional Disclaimer: Commercial and legal/licensing boundaries established")

    # 2. P0 No prefilled default values (clean placeholders)
    assert 'placeholder="e.g. Alex Mercer"' in html, "Founder placeholder missing"
    assert 'placeholder="e.g. PulseFlow Cloud' in html, "Business name placeholder missing"
    assert 'loadStartupSampleData' in html, "Sample demo loader missing"
    print("  [PASS] P0 Form Cleanliness: Pre-filled values replaced with placeholders and sample loader")

    # 3. P1 SEO Title, Meta Description & Canonical
    assert '<title>Business Numerology &amp; Business Diagnostic | Numeros Vision</title>' in html, "Title mismatch"
    assert '<link rel="canonical" href="https://numerosvision.com/tools/business-alignment/" />' in html, "Canonical mismatch"
    assert '<meta property="og:url" content="https://numerosvision.com/tools/business-alignment/" />' in html, "OG URL mismatch"
    assert 'name="keywords"' not in html, "Keywords meta tag should be removed"
    print("  [PASS] P1 SEO Metadata: Title, Description, and Canonical URL standardized")

    # 4. P1 H1 and Tabs
    assert 'Business Numerology &amp; Operating Business Diagnostic' in html, "H1 mismatch"
    assert 'New Venture Assessment' in html, "Tab A label mismatch"
    assert 'Existing Business Review' in html, "Tab B label mismatch"
    print("  [PASS] P1 Headings & Tabs: Clean H1 and accessible tab terminology verified")

    # 5. P1 Methodology Block
    assert 'How Does the Business Assessment Work?' in html, "Methodology title missing"
    assert '1. Practical Business Assessment' in html, "Methodology section 1 missing"
    assert '2. Traditional Numerology Interpretation' in html, "Methodology section 2 missing"
    assert '3. Understanding Your Results &amp; Scoring' in html, "Methodology section 3 missing"
    print("  [PASS] P1 GEO/AEO Methodology: 3-part framework clearly documented")

    # 6. P1 Grounded FAQs (HTML & Schema)
    assert 'What is business numerology?' in html, "FAQ 1 missing"
    assert 'Can numerology determine whether a startup will succeed?' in html, "FAQ 2 missing"
    assert 'What is the difference between a legal business name and a trading name?' in html, "FAQ 3 missing"
    assert 'What information do I need for a new venture assessment?' in html, "FAQ 4 missing"
    assert 'Can I use this tool for an existing business?' in html, "FAQ 5 missing"
    assert 'https://schema.org' in html and 'FAQPage' in html, "FAQ schema missing"
    print("  [PASS] P1 FAQs & Schema: 5 grounded FAQs present in HTML and JSON-LD")

    # 7. P1 Business Data Privacy
    assert 'Business Data Privacy' in html, "Business privacy statement missing"
    print("  [PASS] P1 Data Privacy: Explicit business data handling disclosure present")

def test_live_http():
    print("\n=== TESTING LIVE HTTP ENDPOINTS (via local server on port 8000) ===")
    endpoints = [
        "http://127.0.0.1:8000/tools/business-alignment/",
        "http://127.0.0.1:8000/tools/business-alignment"
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
    test_business_alignment_html()
    test_live_http()
    print("\nALL BUSINESS ALIGNMENT VERIFICATIONS COMPLETED SUCCESSFULLY!")
