import urllib.request
import ssl

ctx = ssl.create_default_context()
url = 'https://greatly-certified-lauderdale-coating.trycloudflare.com/'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
        print("Root Status:", resp.status)
        data = resp.read().decode('utf-8')
        print("Root bytes:", len(data))
except Exception as err:
    print("Fetch error:", err)
