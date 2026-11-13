import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# 1. Test Charm AI Live Chat Endpoint
url = "https://www.numerosvision.com/api/charm/chat"
payload = {
    "message": "What does Personal Year 4 hold for career growth in 2026?",
    "name": "Bhaskr Singh",
    "day": 28,
    "month": 11,
    "year": 1981
}

print(f"Testing live Charm AI endpoint: {url}...")
try:
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0'}
    )
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        res_data = resp.read().decode('utf-8')
        status = resp.status
        print(f"Status Code: {status}")
        try:
            parsed = json.loads(res_data)
            print("Response Keys:", list(parsed.keys()))
            if "response" in parsed:
                print("\nCharm AI Response (first 500 chars):")
                print(parsed["response"][:500])
            if "trace_id" in parsed:
                print("Trace ID:", parsed.get("trace_id"))
            if "model" in parsed:
                print("Reported Model:", parsed.get("model"))
        except Exception:
            print("Raw Response:", res_data[:300])
except Exception as e:
    print(f"Error testing live Charm AI endpoint: {e}")

# 2. Test Report Endpoints
for r in [
    "Numeros_Vision_Basic_Report_28-11-1981.pdf",
    "Numeros_Vision_Advanced_Report_28-11-1981.pdf",
    "Numeros_Vision_Premium_Report_28-11-1981.pdf"
]:
    r_url = f"https://www.numerosvision.com/reports/{r}"
    try:
        req = urllib.request.Request(r_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            print(f"Report: {r} -> HTTP {resp.status}, Content-Length: {resp.headers.get('Content-Length')}")
    except Exception as e:
        print(f"Report: {r} -> Error: {e}")

# 3. Test Sample Page
s_url = "https://www.numerosvision.com/sample?format=brief"
try:
    req = urllib.request.Request(s_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
        print(f"Sample Page: {s_url} -> HTTP {resp.status}, Content-Length: {resp.headers.get('Content-Length')}")
except Exception as e:
    print(f"Sample Page Error: {e}")
