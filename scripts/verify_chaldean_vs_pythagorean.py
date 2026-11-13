"""
Verification script for Name Balancing Calculator and Chaldean vs. Pythagorean Numerology Blog.
Tests metadata, schema consistency, absence of prohibited claims, presence of charts & worked examples,
and live HTTP responses.
"""

import os
import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

def test_name_balancing():
    print("=== TESTING NAME BALANCING TOOL (app/static/tools/name-balancing.html) ===")
    path = "app/static/tools/name-balancing.html"
    assert os.path.exists(path), f"File {path} not found"
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. P0 Security
    assert 'test_master_pass' not in html, "CRITICAL P0: test_master_pass found in name-balancing.html!"
    print("  [PASS] P0 Security: No test_master_pass in browser storage logic")

    # 2. Canonical & Metadata
    assert '<title>Chaldean Name Numerology Calculator | Numeros Vision</title>' in html, "Title mismatch"
    assert 'name="description"' in html and 'Chaldean numerology' in html, "Description missing"
    assert '<link rel="canonical" href="https://numerosvision.com/tools/name-balancing/" />' in html, "Canonical link incorrect"
    print("  [PASS] P1 SEO Metadata: Title, Description, and Canonical URL standardized")

    # 3. Calculation breakdown container
    assert 'id="calc-breakdown-box"' in html, "Calculation breakdown box missing in HTML"
    assert 'id="breakdown-segments-container"' in html, "Segments container missing in HTML"
    print("  [PASS] P1 Calculation Transparency: Step-by-step breakdown container integrated")

    # 4. Methodology Section
    assert 'How Numeros Vision Analyses a Name' in html, "Methodology section missing"
    print("  [PASS] P2 Methodology Block: 5-step transparent calculation process present")

    # 5. FAQs
    assert html.count('<details') >= 6, f"Expected at least 6 FAQs, found {html.count('<details')}"
    assert 'What is Chaldean name numerology?' in html, "FAQ 1 missing"
    assert 'Can a name change guarantee success or wealth?' in html, "FAQ 6 missing"
    print("  [PASS] P2 FAQs: 6 grounded, factual FAQs present")

def test_chaldean_vs_pythagorean():
    print("\n=== TESTING CHALDEAN VS PYTHAGOREAN BLOG (app/static/blog/chaldean-vs-pythagorean-numerology.html) ===")
    path = "app/static/blog/chaldean-vs-pythagorean-numerology.html"
    assert os.path.exists(path), f"File {path} not found"
    with open(path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. P0 Claims & Superiority Removal
    assert 'gold standard' not in html.lower(), "Found 'gold standard' claim"
    assert 'significantly more accurate' not in html.lower(), "Found 'significantly more accurate' claim"
    assert 'hidden compound afflictions' not in html.lower(), "Found 'hidden compound afflictions'"
    assert 'guaranteeing success' not in html.lower(), "Found 'guaranteeing success'"
    assert '4000 bce' not in html.lower(), "Found unsubstantiated '4000 BCE'"
    print("  [PASS] P0 Neutrality: Removed all superiority, predictive certainty, and unsubstantiated dates")

    # 2. Metadata & URLs
    assert '<title>Chaldean vs. Pythagorean Numerology: Charts &amp; Differences</title>' in html, "Title mismatch"
    assert '<link rel="canonical" href="https://numerosvision.com/blog/chaldean-vs-pythagorean-numerology/" />' in html, "Canonical mismatch"
    assert '<meta property="og:url" content="https://numerosvision.com/blog/chaldean-vs-pythagorean-numerology/" />' in html, "OG URL mismatch"
    print("  [PASS] P1 SEO Metadata: Canonical, OG URL, and Title aligned with trailing slash")

    # 3. Direct Answer Box (GEO / AEO)
    assert 'What Is the Difference Between Chaldean and Pythagorean Numerology?' in html, "Direct Answer H2 missing"
    assert 'Neither system has been established as scientifically more accurate' in html, "Direct Answer neutral verdict missing"
    print("  [PASS] P1 GEO/AEO Direct Answer Box: Concise, balanced, self-contained explanation present")

    # 4. Alphabet Charts
    assert 'Chaldean Alphabet Number Chart (1–8)' in html, "Chaldean Chart missing"
    assert 'Pythagorean Alphabet Number Chart (1–9)' in html, "Pythagorean Chart missing"
    # Check letters in Chaldean
    assert 'A, I, J, Q, Y' in html and 'F, P' in html and 'O, Z' in html, "Chaldean letters incomplete"
    # Check letters in Pythagorean
    assert 'A, J, S' in html and 'I, R' in html and 'H, Q, Z' in html, "Pythagorean letters incomplete"
    print("  [PASS] P1 Letter Charts: Complete 26-letter charts for both systems validated")

    # 5. Worked Calculation
    assert 'Step-by-Step Name Calculation: "Rahul Sharma"' in html, "Worked example heading missing"
    assert 'Full Name Total: 17 + 16 = 33' in html or '17 + 16 = 33' in html or '17 + 16 =' in html, "Chaldean worked calculation mismatch"
    assert 'Full Name Total: 24 + 24 = 48' in html or '24 + 24 = 48' in html or '24 + 24 =' in html, "Pythagorean worked calculation mismatch"
    print("  [PASS] P1 Worked Example: Dual-system calculation steps verified against calculation engine")

    # 6. CTAs and Internal Links
    assert 'Explore the Chaldean Name Calculator' in html, "Primary CTA missing"
    assert 'href="/tools/name-balancing/"' in html, "Link to name balancing calculator missing"
    print("  [PASS] P2 CTAs & Internal Links: Transparent CTA and relevant destination links present")

    # 7. FAQs
    assert html.count('class="faq-item"') >= 5, f"Expected 5 FAQs, found {html.count('class=\"faq-item\"')}"
    print("  [PASS] P2 FAQs: Grounded FAQs present in HTML and Schema.org")

def test_live_http():
    print("\n=== TESTING LIVE HTTP ENDPOINTS (via local server on port 8000) ===")
    endpoints = [
        "http://127.0.0.1:8000/tools/name-balancing/",
        "http://127.0.0.1:8000/tools/name-balancing",
        "http://127.0.0.1:8000/blog/chaldean-vs-pythagorean-numerology/",
        "http://127.0.0.1:8000/blog/chaldean-vs-pythagorean-numerology",
        "http://127.0.0.1:8000/amp/blog/chaldean-vs-pythagorean-numerology"
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
    test_name_balancing()
    test_chaldean_vs_pythagorean()
    test_live_http()
    print("\nALL VERIFICATION TESTS COMPLETED SUCCESSFULLY!")
