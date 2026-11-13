import urllib.request
import ssl

ctx = ssl.create_default_context()
url = 'https://tracks-sunny-evaluation-properly.trycloudflare.com/journey_prototype.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
        print("Status:", resp.status)
        data = resp.read().decode('utf-8')
        print("Bytes:", len(data))
        print("Has ANVEIL EVERY CHARM:", 'ANVEIL EVERY CHARM' in data)
        print("Has Rapid Action Plan ₹199:", 'Rapid Action Plan' in data and '₹199' in data)
except Exception as e:
    print("Error:", e)
