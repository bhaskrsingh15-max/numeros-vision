import urllib.request
import json
import sys
import os
import io

# Ensure project root is in sys.path
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Ensure UTF-8 output on Windows console
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

URLS_TO_TEST = [
    {
        "path": "/",
        "name": "Home Portal",
        "expected_elements": [
            "✦",
            "Charm AI",
            "#charm-ai",
            "#ai-oracle",
            "/tools/name-balancing",
            "/tools/mobile-numerology",
            "/tools/life-path-calculator",
            "/blog/master-numbers-11-22-33"
        ],
        "forbidden_elements": ["b2b-header-pill", "acc-group-b2b"]
    },
    {
        "path": "/about",
        "name": "Corporate: About Us",
        "expected_elements": [
            "About Us",
            "Anveil Every Charm",
            "Three Pillars of Integrity",
            "Our Purpose &amp; Promise",
            "Our Ethical Pledge to You",
            "Cormorant Garamond"
        ],
        "forbidden_elements": ["Six Integrated Traditions", "traditions-table"]
    },
    {
        "path": "/pricing",
        "name": "Commercial: Plans & Pricing",
        "expected_elements": [
            "Accepted Payment Modes",
            "UPI (Google Pay, PhonePe, Paytm, BHIM)",
            "Debit &amp; Credit Cards"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/contact",
        "name": "Support: Contact Us",
        "expected_elements": [
            "We Are Here to Guide You",
            "support@numerosvision.com",
            "grievance@numerosvision.com",
            "Statutory Redressal",
            "contact-form"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/privacy",
        "name": "Legal: Privacy Policy & Data Governance",
        "expected_elements": [
            "Privacy Policy &amp; Data Protection",
            "Digital Personal Data Protection Act, 2023",
            "AdTech Isolation Guarantee",
            "Right to Erasure",
            "Chief Grievance &amp; Data Protection Officer"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/terms",
        "name": "Legal: Terms of Service",
        "expected_elements": [
            "Terms of Service",
            "Drugs and Magic Remedies",
            "Consumer Protection Act",
            "Non-Diagnostic Disclaimer",
            "Dispute Resolution"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/refund-policy",
        "name": "Legal: Cancellation & Refund Policy",
        "expected_elements": [
            "Cancellation &amp; Refund Policy",
            "Digital AI Reports",
            "1-on-1 Consultations",
            "5 – 7 Business Days",
            "support@numerosvision.com"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/disclaimer",
        "name": "Legal: Statutory Disclaimer & Astrological Scope",
        "expected_elements": [
            "Statutory Disclaimer &amp; Astrological Scope",
            "What numerological and vibrational guidance on Numeros Vision is, and what it is not",
            "Non-Medical &amp; Non-Psychiatric Advisory Carveout",
            "Non-Financial, Non-Investment &amp; Non-Tax Advisory",
            "Non-Legal &amp; Statutory Civil Records Notice",
            "Conscious Volition, Free Will &amp; Personal Agency",
            "Crystal Remedies, Metals &amp; Metaphysical Attunement",
            "support@numerosvision.com"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/tools/name-balancing",
        "name": "Tool: Name Balancing Engine",
        "expected_elements": [
            "Name Balancing &amp; Spelling Optimizer",
            "Planetary Vibrational Diagnostics",
            "calculateNameBalance",
            "application/ld+json",
            "Cormorant Garamond"
        ],
        "forbidden_elements": [
            "5-Rule Mathematical Audit",
            "1, 3, 5, 6 Only"
        ]
    },
    {
        "path": "/tools/mobile-numerology",
        "name": "Tool: Mobile Numerology Audit",
        "expected_elements": [
            "Mobile Phone Numerology",
            "18 malefic number pairs",
            "auditMobileNumber",
            "application/ld+json",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/tools/blessing-years",
        "name": "Tool: Blessing Years Timeline",
        "expected_elements": [
            "Blessing Years",
            "calculateBlessings",
            "application/ld+json",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/tools/profession-calculator",
        "name": "Tool: Career & Profession Engine",
        "expected_elements": [
            "Career &amp; Profession",
            "calculateProfessions",
            "Work Environment Suitability",
            "application/ld+json"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/tools/vehicle-numerology",
        "name": "Tool: Vehicle Numerology",
        "expected_elements": [
            "Vehicle Registration",
            "calculateVehicle",
            "application/ld+json",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/tools/compatibility-calculator",
        "name": "Tool: Relationship & Marriage Compatibility",
        "expected_elements": [
            "Compatibility Calculator",
            "calculateSynastry",
            "application/ld+json",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/tools/property-numerology",
        "name": "Tool: House & Property Numerology",
        "expected_elements": [
            "Property Numerology Calculator",
            "calculateProperty",
            "application/ld+json",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/tools/baby-naming",
        "name": "Tool: Auspicious Baby Naming Studio",
        "expected_elements": [
            "Baby Naming",
            "calculateBabyNames",
            "application/ld+json",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/practitioner",
        "name": "Portal: Practitioner Workspace & CRM",
        "expected_elements": [
            "Practitioner Portal",
            "Prediction Outcome Tracking",
            "White-Label Studio",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/tools/life-path-calculator",
        "name": "Tool: Life Path Calculator",
        "expected_elements": [
            "Life Path Calculator",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/tools/lo-shu-grid",
        "name": "Tool: Lo Shu Grid Calculator",
        "expected_elements": [
            "Lo Shu Grid",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/tools/lucky-number",
        "name": "Tool: Lucky Number Analysis",
        "expected_elements": [
            "Lucky Number",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/blog/master-numbers-11-22-33",
        "name": "Blog: Master Numbers 11, 22, 33",
        "expected_elements": [
            "Master Numbers 11, 22, and 33 Explained",
            "Triangle of Enlightenment",
            "aeo-box",
            "application/ld+json",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/blog/chaldean-vs-pythagorean-numerology",
        "name": "Blog: Chaldean vs Pythagorean",
        "expected_elements": [
            "Chaldean vs. Pythagorean Numerology",
            "Alphabet Chart Guide",
            "aeo-box",
            "application/ld+json",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/blog/lo-shu-grid-8-planes",
        "name": "Blog: Lo Shu Grid 8 Planes",
        "expected_elements": [
            "8 Planes of the Lo Shu Grid",
            "Golden Rajyog",
            "Silver Rajyog",
            "aeo-box",
            "application/ld+json"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/blog/mobile-numerology-malefic-pairs",
        "name": "Blog: Mobile Numerology Malefic Pairs",
        "expected_elements": [
            "Mobile Numerology Malefic Pairs",
            "Sun (1) + Saturn (8)",
            "aeo-box",
            "application/ld+json"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/blog/what-is-numerology",
        "name": "Blog: What is Numerology?",
        "expected_elements": [
            "What is Numerology",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/blog/life-path-numbers-explained",
        "name": "Blog: Life Path Numbers Explained",
        "expected_elements": [
            "Life Path Numbers",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/blog/gemstone-remedies",
        "name": "Blog: Gemstone Remedies",
        "expected_elements": [
            "Gemstone",
            "Cormorant Garamond"
        ],
        "forbidden_elements": []
    },
    {
        "path": "/sitemap.xml",
        "name": "Sitemap XML",
        "expected_elements": [
            "<?xml version=\"1.0\" encoding=\"UTF-8\"?>",
            "<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\"",
            "<loc>https://numerosvision.com/about</loc>",
            "<loc>https://numerosvision.com/pricing</loc>",
            "<loc>https://numerosvision.com/contact</loc>",
            "<loc>https://numerosvision.com/privacy</loc>",
            "<loc>https://numerosvision.com/terms</loc>",
            "<loc>https://numerosvision.com/refund-policy</loc>",
            "<loc>https://numerosvision.com/tools/compatibility-calculator</loc>",
            "<loc>https://numerosvision.com/tools/property-numerology</loc>",
            "<loc>https://numerosvision.com/tools/baby-naming</loc>",
            "<loc>https://numerosvision.com/practitioner</loc>"
        ],
        "forbidden_elements": ["\"<?xml"]
    },
    {
        "path": "/health",
        "name": "API Health Endpoint",
        "expected_elements": [
            "healthy",
            "3.7.0",
            "NameBalancing",
            "MobileNumerology",
            "/about",
            "/pricing",
            "/refund-policy",
            "/tools/compatibility-calculator",
            "/tools/property-numerology",
            "/tools/baby-naming",
            "/practitioner"
        ],
        "forbidden_elements": []
    }
]

BASE_URL = "http://127.0.0.1:8000"

def run_tests():
    print("=" * 80)
    print("NUMEROS VISION — COMPLETE URL, LEGAL & SEO/AEO VERIFICATION SUITE")
    print(f"Target: {BASE_URL}")
    print("=" * 80)
    
    # Check if live server is reachable
    is_live = False
    try:
        req = urllib.request.Request(f"{BASE_URL}/health", headers={"User-Agent": "NumerosVision-QCAgent/1.0"})
        with urllib.request.urlopen(req, timeout=1) as response:
            if response.getcode() == 200:
                is_live = True
    except Exception:
        is_live = False

    test_client = None
    if not is_live:
        print("[NOTICE] Live server at 127.0.0.1:8000 not detected.")
        print("[NOTICE] Using FastAPI TestClient for in-process full endpoint verification.\n")
        from fastapi.testclient import TestClient
        from app.main import app
        test_client = TestClient(app)

    total_urls = len(URLS_TO_TEST)
    passed_urls = 0
    failures = []

    for item in URLS_TO_TEST:
        full_url = BASE_URL + item["path"]
        print(f"\n[TESTING] {item['name']}")
        print(f"  Path: {item['path']}")
        
        try:
            if is_live:
                req = urllib.request.Request(full_url, headers={"User-Agent": "NumerosVision-QCAgent/1.0"})
                with urllib.request.urlopen(req, timeout=5) as response:
                    status_code = response.getcode()
                    html_bytes = response.read()
                    html_text = html_bytes.decode("utf-8", errors="replace")
            else:
                resp = test_client.get(item["path"])
                status_code = resp.status_code
                html_text = resp.text
                html_bytes = html_text.encode("utf-8")
                
            if status_code != 200:
                print(f"  [FAIL] Unexpected status code {status_code}")
                failures.append((item['name'], f"Status code {status_code}"))
                continue
            else:
                print(f"  [PASS] HTTP Status: {status_code} OK (Length: {len(html_bytes):,} bytes)")

            # Check expected elements
            missing = []
            for exp in item.get("expected_elements", []):
                if exp not in html_text:
                    missing.append(exp)

            if missing:
                print(f"  [FAIL] Missing expected tokens: {missing}")
                failures.append((item['name'], f"Missing tokens: {missing}"))
                continue
            else:
                print(f"  [PASS] All expected tokens verified ({len(item['expected_elements'])} matched)")

            # Check forbidden elements
            found_forbidden = []
            for forb in item.get("forbidden_elements", []):
                if forb in html_text:
                    found_forbidden.append(forb)

            if found_forbidden:
                print(f"  [FAIL] Found forbidden tokens: {found_forbidden}")
                failures.append((item['name'], f"Forbidden tokens present: {found_forbidden}"))
                continue
            else:
                passed_urls += 1

        except Exception as e:
            print(f"  [ERROR] {e}")
            failures.append((item['name'], str(e)))

    # Test Contact POST API
    print(f"\n[TESTING] API Endpoint: POST /api/v1/contact")
    try:
        contact_dict = {
            "name": "Aarav Singhania",
            "email": "aarav@example.com",
            "phone": "+919876543210",
            "category": "consultation",
            "message": "Inquiry regarding birth time rectification consultation."
        }

        if is_live:
            contact_payload = json.dumps(contact_dict).encode("utf-8")
            req = urllib.request.Request(
                f"{BASE_URL}/api/v1/contact",
                data=contact_payload,
                headers={"Content-Type": "application/json", "User-Agent": "NumerosVision-QCAgent/1.0"}
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode("utf-8"))
        else:
            resp = test_client.post("/api/v1/contact", json=contact_dict)
            data = resp.json()

        if data.get("status") == "success" and "NV-TICK-" in data.get("ticket_id", ""):
            print(f"  [PASS] Contact API working. Ticket ID issued: {data['ticket_id']}")
            passed_urls += 1
            total_urls += 1
        else:
            failures.append(("POST /api/v1/contact", f"Invalid response: {data}"))
            total_urls += 1
    except Exception as e:
        print(f"  [ERROR] Contact API failure: {e}")
        failures.append(("POST /api/v1/contact", str(e)))
        total_urls += 1

    print("\n" + "=" * 80)
    print(f"TEST SUMMARY: {passed_urls}/{total_urls} URLs & APIs Passed Verification")
    if failures:
        print("FAILURES:")
        for name, err in failures:
            print(f"  - {name}: {err}")
        print("=" * 80)
        sys.exit(1)
    else:
        print(f"SUCCESS: ALL {total_urls} ENDPOINTS, LEGAL PAGES & APIS VERIFIED WITH 100% PASS RATE")
        print("=" * 80)
        sys.exit(0)

if __name__ == "__main__":
    run_tests()
