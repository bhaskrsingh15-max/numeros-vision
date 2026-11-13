import urllib.request
import ssl

ctx = ssl.create_default_context()
url = 'https://tracks-sunny-evaluation-properly.trycloudflare.com/charm-ai/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
        print("Status:", resp.status)
        data = resp.read().decode('utf-8')
        print("Page bytes:", len(data))
        print("Canonical white star present:", 'stroke="#FFFFFF"' in data)
        print("v=5.5.0 present:", 'v=5.5.0' in data)
except Exception as err:
    print("Fetch error:", err)
