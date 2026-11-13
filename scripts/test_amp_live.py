"""
Test live AMP endpoints and verify GTM-5N2QCMZS
"""
import urllib.request

BASE_URL = "http://127.0.0.1:8000"

urls_to_test = [
    "/amp",
    "/amp/",
    "/amp/blog/what-is-numerology",
    "/blog/what-is-numerology/amp",
    "/amp/blog/master-numbers-11-22-33",
    "/amp/blog/chaldean-vs-pythagorean-numerology",
    "/amp/blog/lo-shu-grid-8-planes",
    "/amp/blog/gemstone-remedies"
]

all_passed = True
for path in urls_to_test:
    url = BASE_URL + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            status = resp.status
            content = resp.read().decode("utf-8")

        # Checks
        has_amp_boilerplate = "amp-boilerplate" in content
        has_amp_runtime = "cdn.ampproject.org/v0.js" in content
        has_amp_analytics = "custom-element=\"amp-analytics\"" in content
        has_gtm_amp = "GTM-5N2QCMZS" in content
        has_canonical = 'rel="canonical"' in content

        if (status == 200 and has_amp_boilerplate and has_amp_runtime and 
            has_amp_analytics and has_gtm_amp and has_canonical):
            print(f"[PASS] {path} (200 OK, length={len(content)}) - Valid AMP with GTM-5N2QCMZS")
        else:
            print(f"[FAIL] {path} - status={status}, gtm={has_gtm_amp}, runtime={has_amp_runtime}")
            all_passed = False
    except Exception as e:
        print(f"[ERROR] {path}: {e}")
        all_passed = False

if all_passed:
    print("\nALL AMP ENDPOINTS VERIFIED 100% OK!")
else:
    print("\nSOME AMP ENDPOINTS FAILED!")
