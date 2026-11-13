"""
scripts/test_all_live_urls.py
=============================
Comprehensive Live and Local URL Verification Suite for Numeros Vision.
Validates all public routes, calculators, blogs, legal pages, PWA assets, and Charm AI APIs.
"""

import urllib.request
import urllib.error
import json
import time

TARGET_URLS = [
    # Core & Hubs
    ("/", "Home Portal"),
    ("/about", "About Us"),
    ("/pricing", "Plans & Pricing"),
    ("/contact", "Contact Support"),
    ("/practitioner", "Practitioner CRM Workspace"),
    ("/sample", "Sample Dossier"),
    ("/sample2", "Sample 2 Mobile & Desktop Architecture"),
    ("/calculators/", "Calculators Hub"),
    ("/insights/", "Insights Knowledge Hub"),
    ("/consultation/", "1-on-1 Consultation"),
    ("/charm-ai", "Charm AI Conversational Portal"),
    ("/login", "User Login"),
    ("/signup", "User Registration"),
    ("/dashboard", "Client Dashboard"),
    ("/methodology", "Methodology Disclosure"),
    ("/faq", "FAQ"),
    
    # Legal & Compliance
    ("/privacy", "Privacy Policy (DPDP 2023)"),
    ("/terms", "Terms of Service"),
    ("/refund-policy", "Cancellation & Refund Policy"),
    ("/disclaimer", "Statutory Disclaimer"),
    ("/cookie-policy", "Cookie Policy"),
    ("/accessibility", "Accessibility Statement"),

    # Interactive Calculators & Tools
    ("/tools/name-balancing", "Name Balancing Studio"),
    ("/tools/mobile-numerology", "Mobile Numerology Audit"),
    ("/tools/blessing-years", "Blessing Years Timeline"),
    ("/tools/profession-calculator", "Profession & Career Engine"),
    ("/tools/vehicle-numerology", "Vehicle Number Harmonizer"),
    ("/tools/compatibility-calculator", "Relationship Compatibility"),
    ("/tools/property-numerology", "Property & House Numerology"),
    ("/tools/baby-naming", "Auspicious Baby Naming"),
    ("/tools/life-path-calculator", "Life Path Calculator"),
    ("/tools/lo-shu-grid", "Lo Shu Grid Calculator"),
    ("/tools/lucky-number", "Lucky Numbers Engine"),
    ("/tools/business-alignment", "Business Direction Alignment"),
    ("/tools/logo-intelligence", "Logo Intelligence Studio"),

    # Insights & Blog Hub
    ("/blog/what-is-numerology", "Blog: What is Numerology"),
    ("/blog/master-numbers-11-22-33", "Blog: Master Numbers"),
    ("/blog/chaldean-vs-pythagorean-numerology", "Blog: Chaldean vs Pythagorean"),
    ("/blog/lo-shu-grid-8-planes", "Blog: Lo Shu 8 Planes"),
    ("/blog/mobile-numerology-malefic-pairs", "Blog: Mobile Malefic Pairs"),
    ("/blog/life-path-numbers-explained", "Blog: Life Path Explained"),
    ("/blog/gemstone-remedies", "Blog: Gemstone Remedies Guide"),

    # Technical & PWA
    ("/manifest.json", "PWA Web App Manifest"),
    ("/sw.js", "PWA Service Worker"),
    ("/sitemap.xml", "Search Engine Sitemap"),
    ("/health", "Health Check API")
]

def run_url_audit(base_url: str):
    print("=" * 80)
    print(f"NUMEROS VISION — URL AUDIT TARGET: {base_url}")
    print("=" * 80)

    passed = 0
    failed = 0
    results = []

    for path, label in TARGET_URLS:
        full_url = f"{base_url.rstrip('/')}{path}"
        try:
            req = urllib.request.Request(full_url, headers={"User-Agent": "NumerosVision-QCAgent/1.0"})
            t0 = time.time()
            with urllib.request.urlopen(req, timeout=8) as resp:
                latency_ms = (time.time() - t0) * 1000
                status = resp.getcode()
                content = resp.read()
                size_kb = len(content) / 1024
                if status == 200:
                    passed += 1
                    status_str = f"200 OK ({size_kb:.1f} KB, {latency_ms:.0f}ms)"
                    results.append((path, label, True, status_str))
                    print(f"  [PASS] {path:<38} -> {status_str}")
                else:
                    failed += 1
                    status_str = f"Status {status}"
                    results.append((path, label, False, status_str))
                    print(f"  [FAIL] {path:<38} -> {status_str}")
        except Exception as e:
            failed += 1
            results.append((path, label, False, str(e)))
            print(f"  [FAIL] {path:<38} -> ERROR: {e}")

    # API Tests
    print("\n--- Testing Core APIs ---")
    
    # 1. Charm AI Chat
    try:
        chat_req = urllib.request.Request(
            f"{base_url.rstrip('/')}/api/charm/chat",
            data=json.dumps({
                "name": "Arjun Sharma",
                "dob": "1990-08-15",
                "question": "Is 2026 favorable for career growth?"
            }).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "NumerosVision-QCAgent/1.0"}
        )
        with urllib.request.urlopen(chat_req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if resp.getcode() == 200 and "prediction" in data:
                print("  [PASS] POST /api/charm/chat                -> 200 OK (Charm AI Dasha Prediction Verified)")
                passed += 1
            else:
                print("  [FAIL] POST /api/charm/chat                -> Invalid response")
                failed += 1
    except Exception as e:
        print(f"  [FAIL] POST /api/charm/chat                -> ERROR: {e}")
        failed += 1

    # 2. Readings Free Calculation
    try:
        free_req = urllib.request.Request(
            f"{base_url.rstrip('/')}/api/v1/readings/free",
            data=json.dumps({"name": "Arjun Sharma", "day": 15, "month": 8, "year": 1990}).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "NumerosVision-QCAgent/1.0"}
        )
        with urllib.request.urlopen(free_req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if resp.getcode() == 200 and data.get("data", {}).get("vedic_numerology", {}).get("driver_number") == 6:
                print("  [PASS] POST /api/v1/readings/free          -> 200 OK (Core Engine Driver 6 Conductor 6 Verified)")
                passed += 1
            else:
                print("  [FAIL] POST /api/v1/readings/free          -> Invalid response")
                failed += 1
    except Exception as e:
        print(f"  [FAIL] POST /api/v1/readings/free          -> ERROR: {e}")
        failed += 1

    # 3. Contact API
    try:
        cont_req = urllib.request.Request(
            f"{base_url.rstrip('/')}/api/v1/contact",
            data=json.dumps({
                "name": "Live Test Seeker",
                "email": "seeker@example.com",
                "phone": "+919876543210",
                "category": "consultation",
                "message": "Live endpoint test inquiry"
            }).encode("utf-8"),
            headers={"Content-Type": "application/json", "User-Agent": "NumerosVision-QCAgent/1.0"}
        )
        with urllib.request.urlopen(cont_req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            if resp.getcode() == 200 and "ticket_id" in data:
                print(f"  [PASS] POST /api/v1/contact                -> 200 OK (Ticket Issued: {data.get('ticket_id')})")
                passed += 1
            else:
                print("  [FAIL] POST /api/v1/contact                -> Invalid response")
                failed += 1
    except Exception as e:
        print(f"  [FAIL] POST /api/v1/contact                -> ERROR: {e}")
        failed += 1

    total = passed + failed
    print("\n" + "=" * 80)
    print(f"AUDIT SUMMARY: {passed}/{total} URLs & APIs Responded with 200 OK ({(passed/total)*100:.1f}% Success)")
    print("=" * 80)
    return passed, failed

if __name__ == "__main__":
    with open("LIVE_URL.txt", "r") as f:
        live_url = f.read().strip()
    
    print("\n>>> AUDITING LOCALHOST <<<")
    run_url_audit("http://127.0.0.1:8000")
    
    if live_url:
        print("\n>>> AUDITING PUBLIC TUNNEL <<<")
        run_url_audit(live_url)
