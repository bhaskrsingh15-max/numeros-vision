import urllib.request
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

endpoints = [
    ("GET", "https://www.numerosvision.com/api/charm/chat"),
    ("POST", "https://www.numerosvision.com/api/charm/chat"),
    ("GET", "https://www.numerosvision.com/api/v1/readings/ask"),
    ("POST", "https://www.numerosvision.com/api/v1/readings/ask"),
    ("GET", "https://www.numerosvision.com/charm_ai.html"),
    ("GET", "https://www.numerosvision.com/charm-ai/"),
    ("GET", "https://www.numerosvision.com/static/reports/Numeros_Vision_Basic_Report_28-11-1981.pdf"),
    ("GET", "https://www.numerosvision.com/api/health"),
]

for method, url in endpoints:
    try:
        data = json.dumps({"message": "test", "day": 28, "month": 11, "year": 1981}).encode('utf-8') if method == "POST" else None
        headers = {'User-Agent': 'Mozilla/5.0'}
        if data:
            headers['Content-Type'] = 'application/json'
        req = urllib.request.Request(url, data=data, headers=headers, method=method)
        with urllib.request.urlopen(req, context=ctx, timeout=10) as resp:
            print(f"{method} {url} -> {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"{method} {url} -> HTTP {e.code}: {e.reason}")
    except Exception as e:
        print(f"{method} {url} -> Error: {e}")
