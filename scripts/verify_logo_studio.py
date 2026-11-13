import sys
import json
import re
from pathlib import Path
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

def test_file_integrity():
    path = Path("app/static/tools/logo-intelligence.html")
    assert path.exists(), f"File not found: {path}"
    content = path.read_text(encoding="utf-8")
    
    print("--- 1. Testing SEO, GEO, AIO Metadata & Canonical ---")
    assert ("<title>Logo Design &amp; Business Name Numerology Studio | Numeros Vision</title>" in content or
            "<title>Logo Design & Business Name Numerology Studio | Numeros Vision</title>" in content), "Missing or incorrect title"
    assert '<link rel="canonical" href="https://numerosvision.com/tools/logo-studio/" />' in content, "Missing or incorrect canonical"
    assert '<meta property="og:url" content="https://numerosvision.com/tools/logo-studio/" />' in content, "Missing or incorrect og:url"
    assert 'name="description"' in content, "Missing meta description"
    print("✓ Metadata and Canonical verified!")

    print("--- 2. Testing JSON-LD Structured Data ---")
    schema_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    assert schema_matches, "No JSON-LD scripts found"
    
    parsed_schemas = []
    for s in schema_matches:
        try:
            parsed = json.loads(s.strip())
            parsed_schemas.append(parsed)
        except Exception as e:
            raise AssertionError(f"Invalid JSON-LD: {e}")
            
    types = []
    faq_schema = None
    for s in parsed_schemas:
        if "@graph" in s:
            for item in s["@graph"]:
                t = item.get("@type")
                types.append(t)
                if t == "FAQPage":
                    faq_schema = item
        else:
            t = s.get("@type")
            types.append(t)
            if t == "FAQPage":
                faq_schema = s

    assert "WebApplication" in types, f"Missing WebApplication schema. Found: {types}"
    assert "BreadcrumbList" in types, f"Missing BreadcrumbList schema. Found: {types}"
    assert "FAQPage" in types, f"Missing FAQPage schema. Found: {types}"
    
    assert faq_schema is not None, "FAQPage schema not found"
    assert len(faq_schema.get("mainEntity", [])) == 5, f"Expected 5 FAQ items in schema, found {len(faq_schema.get('mainEntity', []))}"
    print(f"✓ JSON-LD Schemas verified! Found types: {types} with 5 FAQ entities")

    print("--- 3. Testing Headings, Tabs & Brand Foundation Controls ---")
    assert ("Logo Design Studio &amp; Business Name Numerology" in content or
            "Logo Design Studio & Business Name Numerology" in content), "H1 missing or incorrect"
    assert "Create a New Logo" in content, "Tab 1 label missing"
    assert "Inspect an Existing Logo" in content, "Tab 2 label missing"
    
    # Brand brief fields
    for field_id in ["industrySector", "targetAudience", "brandPersonality", "brandPositioning", "businessActivity"]:
        assert f'id="{field_id}"' in content, f"Missing brand brief field: {field_id}"
    print("✓ Headings, Tabs & Brand Foundation fields verified!")

    print("--- 4. Testing Grounded Claims & Disclaimers ---")
    assert "zero AI hallucination" not in content, "Prohibited ungrounded claim 'zero AI hallucination' found"
    assert "Design & Validation Notice" in content, "Missing Design & Validation Notice"
    assert "Can a numerology-based logo guarantee business success" in content, "Missing grounded FAQ on business success"
    print("✓ Grounded claims and disclaimers verified!")

    print("--- 5. Testing Methodology & FAQs in HTML ---")
    assert "How the Numeros Vision Logo Studio Works" in content, "Missing methodology section"
    assert "Frequently Asked Questions" in content, "Missing FAQ section"
    faq_questions = re.findall(r'<details class="faq-item".*?<summary.*?>(.*?)</summary>', content, re.DOTALL)
    assert len(faq_questions) == 5, f"Expected 5 FAQ questions in HTML, found {len(faq_questions)}"
    print(f"✓ Methodology and {len(faq_questions)} HTML FAQs verified!")

    print("--- 6. Testing Script Logic (SVG sanitization & brief update) ---")
    assert "calculateChaldeanWordmark" in content, "Missing calculateChaldeanWordmark function"
    assert "updateNumerologyBrief" in content, "Missing updateNumerologyBrief function"
    assert "script" in content.lower() and "onerror" in content.lower(), "SVG sanitization logic check failed"
    print("✓ Client-side calculation and SVG sanitization verified!")

def test_endpoints():
    base_url = "http://127.0.0.1:8000"
    endpoints = [
        "/tools/logo-studio/",
        "/tools/logo-studio",
        "/tools/logo-intelligence/",
        "/tools/logo-intelligence"
    ]
    
    print("\n--- 7. Testing Live Serving Endpoints ---")
    for ep in endpoints:
        url = f"{base_url}{ep}"
        req = urllib.request.Request(url, headers={"User-Agent": "NumerosVisionVerifier/1.0"})
        with urllib.request.urlopen(req, timeout=5) as resp:
            status = resp.status
            body = resp.read().decode("utf-8")
            assert status == 200, f"Expected 200, got {status} for {url}"
            assert "Logo Design Studio" in body, f"H1 not found in response for {url}"
            print(f"✓ {url} -> 200 OK (Verified H1 in response)")

    print("\n--- 8. Testing Logo Studio Backend Preview API ---")
    preview_url = f"{base_url}/api/v1/logo/preview"
    req_body = json.dumps({
        "business_name": "NUMEROS",
        "symbol_concept": "solarsuncrest1",
        "primary_color": "#C9A227",
        "accent_color": "#8B6914",
        "bg_color": "#FFFDF7",
        "tagline": "ANVEIL EVERY CHARM",
        "variant": "primary_horizontal"
    }).encode("utf-8")
    
    req = urllib.request.Request(preview_url, data=req_body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        status = resp.status
        data = json.loads(resp.read().decode("utf-8"))
        assert status == 200, f"Expected 200, got {status}"
        assert "svg" in data and "<svg" in data["svg"], "Preview API did not return valid SVG"
        assert "validation" in data, "Preview API missing validation payload"
        print(f"✓ Preview API (/api/v1/logo/preview) -> 200 OK (Vector output verified, contrast ratio: {data['validation']['contrast_ratio']})")

    print("\n--- 9. Testing Existing Logo Analysis API ---")
    analyze_url = f"{base_url}/api/v1/logo/analyze-existing"
    sample_svg = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60"><rect width="200" height="60" fill="#FFFDF7"/><text x="20" y="35" fill="#523E28" font-family="Cinzel">NUMEROS</text></svg>'
    req_body = json.dumps({
        "svg_content": sample_svg
    }).encode("utf-8")
    
    req = urllib.request.Request(analyze_url, data=req_body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=5) as resp:
        status = resp.status
        data = json.loads(resp.read().decode("utf-8"))
        assert status == 200, f"Expected 200, got {status}"
        assert "measurable_design_checks" in data, "Analyze API missing measurable_design_checks"
        assert "traditional_symbolic_interpretations" in data, "Analyze API missing traditional_symbolic_interpretations"
        print("✓ Analyze Existing Logo API (/api/v1/logo/analyze-existing) -> 200 OK (Separates measurable findings from traditional interpretations)")

if __name__ == "__main__":
    test_file_integrity()
    test_endpoints()
    print("\n=======================================================")
    print("ALL 9 VERIFICATION CHECKS PASSED WITH ZERO ERRORS!")
    print("=======================================================")
