import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

base = "https://memphis-joined-drama-julie.trycloudflare.com"

for path in ["/", "/charm_ai.html", "/journey_prototype.html"]:
    url = base + path
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            body = r.read().decode("utf-8")
            has_249 = "249" in body
            has_510 = "510" in body
            has_199 = "199" in body
            print(f"URL: {url} -> Status {r.status}, Length {len(body)}, has_249: {has_249}, has_510: {has_510}, has_199: {has_199}")
    except Exception as e:
        print(f"URL: {url} -> ERROR: {e}")
