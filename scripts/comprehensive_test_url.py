import urllib.request
import json
import ssl
import time

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = "https://memphis-joined-drama-julie.trycloudflare.com"

tests = [
    {"name": "Homepage", "url": f"{base}/", "method": "GET"},
    {"name": "Charm AI Page", "url": f"{base}/charm_ai.html", "method": "GET"},
    {"name": "End-to-End Prototype", "url": f"{base}/journey_prototype.html", "method": "GET"},
    {"name": "Pricing Page", "url": f"{base}/pricing/", "method": "GET"},
    {"name": "Payments Plans API", "url": f"{base}/api/v1/payments/plans", "method": "GET"},
    {
        "name": "Charm AI Ask API",
        "url": f"{base}/api/v1/readings/ask",
        "method": "POST",
        "data": {
            "name": "Anjali Sharma",
            "day": 10,
            "month": 6,
            "year": 1990,
            "question": "Is 2026 better for my career prospects? and what how will it unfold?",
            "pob": "New Delhi",
            "tob": "10:30",
            "user_id": "test_user_anjali_verify"
        }
    }
]

print(f"=== TESTING LIVE CLOUDFLARE URL: {base} ===\n")

all_passed = True

for t in tests:
    t_start = time.time()
    try:
        if t["method"] == "GET":
            req = urllib.request.Request(t["url"], headers={"User-Agent": "Mozilla/5.0"})
        else:
            payload = json.dumps(t["data"]).encode("utf-8")
            req = urllib.request.Request(
                t["url"],
                data=payload,
                headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
            )
        
        with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
            elapsed = time.time() - t_start
            content = resp.read().decode("utf-8")
            status = resp.status
            size = len(content)
            
            print(f"[PASS] {t['name']}")
            print(f"       URL: {t['url']}")
            print(f"       Status: {status} OK | Response Time: {elapsed:.2f}s | Size: {size:,} bytes")
            if t["name"] == "Charm AI Ask API":
                data = json.loads(content)
                ans = data.get("direct_answer", "")
                safe_preview = ans[:120].replace('\n', ' ').encode('ascii', errors='replace').decode('ascii')
                print(f"       Charm AI Verification: Status={data.get('status')}")
                print(f"       Topic={data.get('topic_display')}")
                print(f"       Answer preview: {safe_preview}")
            print()
    except Exception as e:
        all_passed = False
        print(f"[FAIL] {t['name']}")
        print(f"       URL: {t['url']}")
        print(f"       Error: {e}")
        print()

print(f"Overall Test Result: {'ALL TESTS PASSED (100% HEALTHY)' if all_passed else 'SOME TESTS FAILED'}")
