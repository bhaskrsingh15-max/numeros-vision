import urllib.request
import ssl

ctx = ssl.create_default_context()
url = 'https://memphis-joined-drama-julie.trycloudflare.com/journey_prototype.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx, timeout=12) as resp:
        print("Journey Prototype Status:", resp.status)
        data = resp.read().decode('utf-8')
        print("Bytes:", len(data))
        print("Has ANVEIL EVERY CHARM:", 'ANVEIL EVERY CHARM' in data)
        print("Has 7 Stages:", 'Stage 1: Discovery Entry' in data and 'Stage 7: Central Product Catalogue' in data)
except Exception as e:
    print("Error:", e)

url_root = 'https://memphis-joined-drama-julie.trycloudflare.com/'
req_root = urllib.request.Request(url_root, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req_root, context=ctx, timeout=12) as resp:
        print("Root Status:", resp.status)
        data = resp.read().decode('utf-8')
        print("Root Bytes:", len(data))
        print("Modal Plan Price is 199:", 'id="modal-plan-price">₹199</span>' in data)
except Exception as e:
    print("Error:", e)
