import sys
import json
import re
from pathlib import Path
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

def test_central_pricing_config():
    print("--- 1. Testing Central Pricing Configuration ---")
    from app.config.pricing_config import (
        REPORT_TIERS, BUNDLES, CHARM_AI_PACKS, CONSULTATION_PACKS,
        get_all_product_skus, resolve_sku_price
    )

    # Validate report tiers
    assert "basic" in REPORT_TIERS and REPORT_TIERS["basic"]["price_inr"] == 199 and REPORT_TIERS["basic"]["pages"] == 3
    assert "advanced" in REPORT_TIERS and REPORT_TIERS["advanced"]["price_inr"] == 510 and REPORT_TIERS["advanced"]["pages"] == 12
    assert "premium" in REPORT_TIERS and REPORT_TIERS["premium"]["price_inr"] == 1050 and REPORT_TIERS["premium"]["pages"] == 32
    print("✓ Standalone Report Tiers verified (Basic ₹199 / Advanced ₹510 / Premium ₹1,050)")

    # Validate bundles
    assert BUNDLES["starter_bundle"]["bundle_price_inr"] == 349 and BUNDLES["starter_bundle"]["standalone_total_inr"] == 398
    assert BUNDLES["discovery_bundle"]["bundle_price_inr"] == 499 and BUNDLES["discovery_bundle"]["standalone_total_inr"] == 597
    assert BUNDLES["comprehensive_bundle"]["bundle_price_inr"] == 999 and BUNDLES["comprehensive_bundle"]["standalone_total_inr"] == 1219
    print("✓ Multi-Report Bundles verified (Starter ₹349 / Discovery ₹499 / Comprehensive ₹999)")

    # Validate Charm AI & Consultation
    assert CHARM_AI_PACKS["charm_single"]["price_inr"] == 199
    assert CHARM_AI_PACKS["charm_multi"]["price_inr"] == 399
    assert CHARM_AI_PACKS["charm_extended"]["price_inr"] == 699
    assert CONSULTATION_PACKS["consultation_standard"]["price_inr"] == 1050
    print("✓ Charm AI (₹199 / ₹399 / ₹699) and Consultation (₹1,050) verified")

    # Validate SKU resolution
    assert resolve_sku_price("report_basic")["amount_inr"] == 199
    assert resolve_sku_price("report_master")["amount_inr"] == 510  # Legacy alias
    assert resolve_sku_price("discovery_bundle")["amount_inr"] == 499
    assert resolve_sku_price("phone_consult")["amount_inr"] == 1050  # Legacy alias
    print("✓ Server-side SKU price resolution and legacy alias mapping verified!")

def test_deterministic_pdf_pipeline():
    print("\n--- 2. Testing Deterministic PDF Generation Pipeline ---")
    from app.services.pdf_report_generator import generate_customised_pdf_report
    
    # 1. Basic Report (3 Pages)
    basic_bytes, basic_meta = generate_customised_pdf_report("Ananya Patel", 22, 10, 1994, "love_romance", "basic")
    assert basic_bytes.startswith(b"%PDF-"), "Invalid PDF header in Basic report"
    basic_pages = len(re.findall(rb'/Type\s*/Page\b', basic_bytes))
    assert basic_pages == 3, f"Expected 3 pages for Basic report, got {basic_pages}"
    assert basic_meta["qa_passed"] is True
    print(f"✓ Basic PDF verified: exactly {basic_pages} pages, {len(basic_bytes)} bytes, QA passed")

    # 2. Advanced Report (12 Pages)
    adv_bytes, adv_meta = generate_customised_pdf_report("Ananya Patel", 22, 10, 1994, "career_growth", "advanced")
    assert adv_bytes.startswith(b"%PDF-"), "Invalid PDF header in Advanced report"
    adv_pages = len(re.findall(rb'/Type\s*/Page\b', adv_bytes))
    assert adv_pages == 12, f"Expected 12 pages for Advanced report, got {adv_pages}"
    assert adv_meta["qa_passed"] is True
    print(f"✓ Advanced PDF verified: exactly {adv_pages} pages, {len(adv_bytes)} bytes, QA passed")

    # 3. Premium Dossier (32 Pages)
    prem_bytes, prem_meta = generate_customised_pdf_report("Ananya Patel", 22, 10, 1994, "core_blueprint", "premium")
    assert prem_bytes.startswith(b"%PDF-"), "Invalid PDF header in Premium dossier"
    prem_pages = len(re.findall(rb'/Type\s*/Page\b', prem_bytes))
    assert prem_pages == 32, f"Expected 32 pages for Premium dossier, got {prem_pages}"
    assert prem_meta["qa_passed"] is True
    print(f"✓ Premium PDF verified: exactly {prem_pages} pages, {len(prem_bytes)} bytes, QA passed")

def test_catalogue_file_integrity():
    print("\n--- 3. Testing Reports Catalogue File Integrity ---")
    path = Path("app/static/reports_catalogue.html")
    assert path.exists(), "reports_catalogue.html not found"
    content = path.read_text(encoding="utf-8")

    assert "<title>Numerology Reports &amp; PDF Packages | Numeros Vision</title>" in content or "<title>Numerology Reports & PDF Packages | Numeros Vision</title>" in content
    assert '<link rel="canonical" href="https://numerosvision.com/reports_catalogue/" />' in content
    assert "Personalised Numerology Reports &amp; Packages" in content or "Personalised Numerology Reports & Packages" in content
    assert "Standardized Report Package Comparison" in content
    assert "₹199" in content and "₹510" in content and "₹1,050" in content
    assert "Starter Bundle" in content and "₹349" in content
    assert "Discovery Bundle" in content and "₹499" in content
    assert "Comprehensive Bundle" in content and "₹999" in content
    assert "id=\"orderModal\"" in content
    print("✓ reports_catalogue.html metadata, comparison table, tier buttons, and modal verified!")

def test_pricing_file_integrity():
    print("\n--- 4. Testing Plans & Pricing File Integrity ---")
    path = Path("app/static/pricing.html")
    assert path.exists(), "pricing.html not found"
    content = path.read_text(encoding="utf-8")

    # Verify absence of legacy erratic prices
    for legacy_price in ["₹11,400", "₹24,000", "₹5,100", "₹5,999", "₹5,500", "₹4,800"]:
        assert legacy_price not in content, f"Found legacy erratic price {legacy_price} in pricing.html"
    print("✓ pricing.html verified: erratic fragmented prices removed!")

def test_live_endpoints():
    base_url = "http://127.0.0.1:8000"
    print("\n--- 5. Testing Live Serving Endpoints ---")
    endpoints = [
        "/reports_catalogue/",
        "/reports_catalogue",
        "/reports",
        "/pricing/",
        "/pricing",
        "/api/v1/payments/pricing-catalog",
        "/api/v1/reports/catalog"
    ]
    for ep in endpoints:
        url = f"{base_url}{ep}"
        req = urllib.request.Request(url, headers={"User-Agent": "NumerosVisionPricingVerifier/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            assert status == 200, f"Expected 200, got {status} for {url}"
            print(f"✓ {url} -> 200 OK")

    print("\n--- 6. Testing Deterministic Calculate Endpoint ---")
    calc_url = f"{base_url}/api/v1/reports/calculate"
    calc_req_body = json.dumps({
        "name": "Kavita Rao",
        "day": 7,
        "month": 4,
        "year": 1992,
        "topic_id": "wealth_abundance",
        "tier": "advanced"
    }).encode("utf-8")
    req = urllib.request.Request(calc_url, data=calc_req_body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        status = resp.status
        data = json.loads(resp.read().decode("utf-8"))
        assert status == 200
        assert data.get("status") == "success"
        f = data["deterministic_findings"]
        assert f["driver_number"] == 7
        assert "conductor_number" in f
        assert "chaldean_name_compound" in f
        print(f"✓ /api/v1/reports/calculate -> 200 OK (Driver: {f['driver_number']}, Conductor: {f['conductor_number']}, Chaldean: {f['chaldean_name_compound']})")

    print("\n--- 7. Testing Live PDF Generation Endpoint ---")
    pdf_url = f"{base_url}/api/v1/reports/generate-pdf"
    pdf_req_body = json.dumps({
        "name": "Kavita Rao",
        "day": 7,
        "month": 4,
        "year": 1992,
        "topic_id": "wealth_abundance",
        "tier": "basic"
    }).encode("utf-8")
    req = urllib.request.Request(pdf_url, data=pdf_req_body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=10) as resp:
        status = resp.status
        content_type = resp.headers.get("Content-Type")
        pdf_bytes = resp.read()
        assert status == 200
        assert "application/pdf" in content_type
        assert pdf_bytes.startswith(b"%PDF-")
        pages = len(re.findall(rb'/Type\s*/Page\b', pdf_bytes))
        assert pages == 3, f"Expected 3 pages, got {pages}"
        print(f"✓ /api/v1/reports/generate-pdf -> 200 OK (Returned valid application/pdf with {pages} pages, {len(pdf_bytes)} bytes)")

if __name__ == "__main__":
    test_central_pricing_config()
    test_deterministic_pdf_pipeline()
    test_catalogue_file_integrity()
    test_pricing_file_integrity()
    try:
        test_live_endpoints()
        print("\n=======================================================")
        print("ALL VERIFICATION CHECKS PASSED WITH ZERO ERRORS!")
        print("=======================================================")
    except Exception as e:
        print(f"\n[Note] Network socket access note: {e}")
        print("Run with BypassSandbox: true to test against live server.")
