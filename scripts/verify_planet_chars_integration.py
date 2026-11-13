import urllib.request
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

urls = [
    'http://127.0.0.1:8000/',
    'https://sudden-married-mutual-calculated.trycloudflare.com/'
]

for url in urls:
    print(f"\n--- Testing {url} ---")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, context=ctx, timeout=10) as r:
            html = r.read().decode('utf-8')
            print(f"Status: {r.status}, HTML length: {len(html)}")
            print(f"Contains number_characteristics.js: {'/static/js/number_characteristics.js' in html}")
            print(f"Contains id='planet-characteristics-results': {'id=\"planet-characteristics-results\"' in html}")
            print(f"Contains renderPlanetaryCharacteristicsHtml call: {'renderPlanetaryCharacteristicsHtml(driver, conductor)' in html}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")

# Verify JS asset
js_url = 'http://127.0.0.1:8000/static/js/number_characteristics.js'
print(f"\n--- Testing {js_url} ---")
try:
    with urllib.request.urlopen(js_url, timeout=10) as r:
        js = r.read().decode('utf-8')
        print(f"Status: {r.status}, JS length: {len(js)}")
        print(f"Contains Sun (Surya): {'Sun (Surya)' in js}")
        print(f"Contains Saturn (Shani): {'Saturn (Shani)' in js}")
        print(f"Contains Creative Growth Tension: {'Creative Growth Tension' in js}")
except Exception as e:
    print(f"Error fetching {js_url}: {e}")
