import urllib.request
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

urls = [
    "http://localhost:8000/",
    "http://localhost:8000/reports/",
    "http://localhost:8000/reports_catalogue/",
    "http://localhost:8000/calculators/",
    "http://localhost:8000/pricing/",
    "http://localhost:8000/dashboard/",
    "http://localhost:8000/consultation/",
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'})
        with urllib.request.urlopen(req) as resp:
            content = resp.read().decode('utf-8', errors='ignore')
            has_bottom_nav = 'nv-sticky-bottom-nav' in content or 'nv-bottom-nav' in content
            bottom_nav_type = 'nv-sticky-bottom-nav' if 'nv-sticky-bottom-nav' in content else ('nv-bottom-nav' if 'nv-bottom-nav' in content else 'NONE')
            has_emojis = bool('🏠' in content and 'nv-bottom' in content)
            print(f"URL: {url} -> Status: {resp.status}, Bottom Nav: {bottom_nav_type}, Emojis: {has_emojis}")
    except Exception as e:
        print(f"URL: {url} -> ERROR: {e}")
