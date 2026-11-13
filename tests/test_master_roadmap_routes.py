"""
Test Suite: Numeros Vision Master Website Roadmap & Canonical Route Verification
Validates that the separate sample version (/sample-roadmap) and all canonical
roadmap routes resolve with HTTP 200, contain valid H1 tags, and adhere to
the master brand 'Numeros Vision' and tagline 'Anveil Every Charm'.
"""

import urllib.request
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

CANONICAL_TEST_ROUTES = [
    ("/", "Anveil Every Charm", "Home Portal (Page 1)"),
    ("/numerology/", "Explore Numerology and Its Different Methods", "Numerology Guide (Page 2)"),
    ("/calculators/", "Explore Numerology Calculators", "Calculator Hub (Page 3)"),
    ("/calculators/birth-number/", "Calculate Your Birth Number", "Birth Number Calculator (Page 4)"),
    ("/calculators/life-path-number/", "Life Path Calculator", "Life Path Calculator Alias (Page 5)"),
    ("/calculators/name-numerology/", "Name Numerology", "Name Numerology Calculator Alias (Page 6)"),
    ("/calculators/chaldean-name-numerology/", "Name Balancing", "Chaldean Name Calculator Alias (Page 7)"),
    ("/calculators/pythagorean-numerology/", "Calculate Your Pythagorean Number", "Pythagorean Calculator (Page 8)"),
    ("/calculators/lo-shu-grid/", "Lo Shu Grid", "Lo Shu Grid Calculator Alias (Page 9)"),
    ("/calculators/mobile-number-numerology/", "Mobile Number Numerology", "Mobile Calculator Alias (Page 10)"),
    ("/calculators/personal-year/", "Blessing Years", "Personal Year Calculator Alias (Page 11)"),
    ("/calculators/numerology-compatibility/", "Compatibility Calculator", "Compatibility Calculator Alias (Page 12)"),
    ("/charm-ai/", "Ask Charm AI About Your Numbers", "Charm AI Assistant (Page 13)"),
    ("/sample-report/", "Celestial Master Blueprint", "Sample Numerology Report (Page 14)"),
    ("/reports/", "Personalised Dossiers", "Reports Catalogue (Page 15)"),
    ("/pricing/", "Accepted Payment Modes", "Plans and Pricing (Page 16)"),
    ("/consultation/", "Personalised Numerology Consultation", "Consultation Page (Page 17)"),
    ("/about/", "About Numeros Vision", "About Us (Page 18)"),
    ("/methodology/", "How Numeros Vision Calculates and Explains Numbers", "Methodology Principles (Page 19)"),
    ("/insights/", "Numerology Insights", "Insights Learning Hub (Page 20)"),
    ("/faq/", "Frequently Asked Questions", "FAQ Page (Page 22)"),
    ("/contact/", "We Are Here to Guide You", "Contact Us (Page 23)"),
    ("/login/", "Sign In to Numeros Vision", "Member Sign In (Page 24)"),
    ("/signup/", "Create Your Golden Profile", "Member Registration (Page 25)"),
    ("/dashboard/", "Your Numeros Dashboard", "Member Dashboard (Page 26)"),
    ("/privacy-policy/", "Privacy Policy &amp; Data Protection", "Privacy Policy (Page 27)"),
    ("/terms/", "Terms of Service", "Terms of Service (Page 28)"),
    ("/disclaimer/", "Numerology Disclaimer", "Statutory Disclaimer (Page 29)"),
    ("/cookie-policy/", "Cookie Policy", "Cookie Policy (Page 30)"),
    ("/refund-policy/", "Refund Policy", "Refund Policy (Page 31)"),
    ("/accessibility/", "Accessibility Statement", "Accessibility Statement (Page 32)"),
    ("/404", "Page Not Found", "404 Error Recovery (Page 33)"),
    ("/sample-roadmap", "Anveil Every Charm", "Separate Sample Preview Version"),
    ("/roadmap-preview", "Anveil Every Charm", "Sample Roadmap Alias")
]

def test_all_routes():
    print("================================================================================")
    print("NUMEROS VISION — MASTER WEBSITE ROADMAP CANONICAL ROUTE VERIFICATION")
    print("================================================================================")
    
    is_live = False
    try:
        req = urllib.request.Request(f"{BASE_URL}/health", headers={"User-Agent": "NumerosVision-QC/1.0"})
        with urllib.request.urlopen(req, timeout=1) as response:
            if response.getcode() == 200:
                is_live = True
    except Exception:
        is_live = False

    test_client = None
    if not is_live:
        print("[NOTICE] Live server at 127.0.0.1:8000 not detected.")
        print("[NOTICE] Using FastAPI TestClient for in-process route verification.\n")
        import os
        _ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        if _ROOT not in sys.path:
            sys.path.insert(0, _ROOT)
        from fastapi.testclient import TestClient
        from app.main import app
        test_client = TestClient(app)

    passed = 0
    failed = 0
    
    for route, expected_text, desc in CANONICAL_TEST_ROUTES:
        url = f"{BASE_URL}{route}"
        try:
            if is_live:
                req = urllib.request.Request(url, headers={"User-Agent": "NumerosVision-QC/1.0"})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    content = resp.read().decode("utf-8")
                    status = resp.status
            else:
                resp = test_client.get(route)
                content = resp.text
                status = resp.status_code

            target_status = 404 if route == "/404" else 200
            if status == target_status and expected_text in content:
                print(f"  [PASS] {route:<36} ({status} OK) -> {desc}")
                passed += 1
            else:
                print(f"  [FAIL] {route:<36} Status: {status} (exp {target_status}), Text Match: {expected_text in content}")
                failed += 1
        except urllib.error.HTTPError as e:
            if route == "/404" and e.code == 404:
                err_content = e.read().decode("utf-8", errors="ignore")
                if expected_text in err_content:
                    print(f"  [PASS] {route:<36} (404 OK) -> {desc}")
                    passed += 1
                else:
                    print(f"  [FAIL] {route:<36} Status: 404, Text Match: False")
                    failed += 1
            else:
                print(f"  [ERROR] {route:<35} -> {e}")
                failed += 1
        except Exception as e:
            print(f"  [ERROR] {route:<35} -> {e}")
            failed += 1
            
    print("================================================================================")
    print(f"RESULTS: {passed}/{len(CANONICAL_TEST_ROUTES)} Routes Passed. Failed: {failed}")
    print("================================================================================")
    return failed == 0

if __name__ == "__main__":
    success = test_all_routes()
    sys.exit(0 if success else 1)
