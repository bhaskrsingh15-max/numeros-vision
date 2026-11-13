import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url = "https://memphis-joined-drama-julie.trycloudflare.com/api/v1/readings/ask"
payload = {
    "name": "Anjali Sharma",
    "day": 10,
    "month": 6,
    "year": 1990,
    "question": "Is 2026 better for my career prospects? and what how will it unfold?",
    "pob": "New Delhi",
    "tob": "10:30",
    "user_id": "test_user_anjali_cloud"
}

req = urllib.request.Request(
    url,
    data=json.dumps(payload).encode("utf-8"),
    headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"}
)

try:
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        ans = data.get("direct_answer", "")
        has_249 = "249" in ans
        has_raw_html = "<div" in ans or "<a" in ans
        has_cat_c = "Category C" in ans or "Intrinsic Potency" in ans
        print("API STATUS:", resp.status)
        print("HAS 249 in answer:", has_249)
        print("HAS RAW HTML in answer:", has_raw_html)
        print("HAS TECHNICAL CODES (Category C / Potency):", has_cat_c)
        print("ANSWER SNIPPET (last 300 chars):")
        print(ans[-300:].encode('ascii', errors='replace').decode('ascii'))
except Exception as e:
    print("API ERROR:", e)
