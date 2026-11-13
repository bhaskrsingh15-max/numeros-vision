import urllib.request
import json
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

def test_live_endpoints():
    base_url = "http://127.0.0.1:8000"
    print(f"Testing live endpoints against {base_url}...")
    
    # 1. Test Home Page
    req = urllib.request.urlopen(f"{base_url}/")
    assert req.status == 200
    home_html = req.read().decode('utf-8')
    assert "Calculate Your Cosmic Matrix" in home_html
    assert 'id="f-day"' in home_html
    assert 'value="31"' in home_html
    assert 'value="2026"' in home_html
    assert 'value="1940"' in home_html
    assert 'document.write' not in home_html
    assert 'nv_profile_sync.js' in home_html
    print("[PASS] Home Page: Cosmic Matrix options pre-rendered, 0 document.write, profile sync active.")

    # 2. Test Header on Home Page and Subpages
    subpages = ['/about/', '/pricing/', '/calculators/', '/tools/life-path-calculator', '/tools/lo-shu-grid', '/signup/']
    for page in subpages:
        req = urllib.request.urlopen(f"{base_url}{page}")
        assert req.status == 200
        html = req.read().decode('utf-8')
        m = re.search(r'<nav\b[^>]*>[\s\S]*?</nav>', html)
        assert m, f"No nav in {page}"
        header_nav = m.group(0)
        c_pos = header_nav.find('Contact Us')
        a_pos = header_nav.find('About Us')
        assert c_pos != -1, f"No Contact Us in {page}"
        assert a_pos != -1, f"No About Us in {page}"
        assert a_pos < c_pos, f"About Us must be before Contact Us in {page}"
        # Ensure no stray About after Contact Us
        after_c = header_nav[c_pos:]
        assert '>About</a>' not in after_c, f"Stray About after Contact Us in {page}"
        print(f"[PASS] {page}: Header nav unified (About Us at start, Contact Us at right edge).")

    # 3. Test Signup Page DPDP Styling
    req = urllib.request.urlopen(f"{base_url}/signup/")
    signup_html = req.read().decode('utf-8')
    assert 'dpdp-box' in signup_html
    assert 'font-size: 0.74rem' in signup_html
    print("[PASS] Signup Page: Compact 0.74rem DPDP consent box styling active.")

    # 4. Test CDP Capture API
    post_data = json.dumps({
        "name": "Live Test Seeker",
        "email": "livetest@example.com",
        "day": 15,
        "month": 8,
        "year": 1990,
        "category": "cosmic_matrix_test"
    }).encode('utf-8')
    cdp_req = urllib.request.Request(
        f"{base_url}/api/v1/cdp/capture",
        data=post_data,
        headers={"Content-Type": "application/json"}
    )
    res = urllib.request.urlopen(cdp_req)
    assert res.status == 200
    cdp_res = json.loads(res.read().decode('utf-8'))
    assert cdp_res.get("status") == "success"
    print(f"[PASS] CDP Capture API: {cdp_res.get('golden_id')}")

    print("\nALL LIVE ENDPOINT TESTS PASSED WITH 100% SUCCESS!")

if __name__ == '__main__':
    test_live_endpoints()
