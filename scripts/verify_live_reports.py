import urllib.request

for tier, filename in [
    ('Basic (3 Pages - Rs 199)', 'Numeros_Vision_Basic_Report_28-11-1981.pdf'),
    ('Advanced (12 Pages - Rs 510)', 'Numeros_Vision_Advanced_Report_28-11-1981.pdf'),
    ('Premium (32 Pages - Rs 1050)', 'Numeros_Vision_Premium_Report_28-11-1981.pdf')
]:
    url = f'http://127.0.0.1:8000/static/reports/{filename}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read()
            print(f'{tier}: HTTP {resp.status}, size={len(content)} bytes, Valid PDF={content.startswith(b"%PDF")}')
    except Exception as e:
        print(f'{tier}: ERROR -> {e}')
