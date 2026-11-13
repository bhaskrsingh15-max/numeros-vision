import os
import sys

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

urls = [
    "/",
    "/reports/",
    "/reports_catalogue/",
    "/calculators/",
    "/pricing/",
    "/dashboard/",
    "/consultation/",
    "/about/",
    "/contact/",
    "/tools/baby-naming",
    "/tools/name-numerology",
    "/tools/mobile-numerology",
    "/tools/life-path-calculator",
    "/tools/lo-shu-grid",
    "/amp/blog/master-numbers-11-22-33",
]

print("=== TESTING FASTAPI ENDPOINTS ===")
for url in urls:
    try:
        resp = client.get(url, headers={'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)'}, follow_redirects=True)
        html = resp.text
        has_sticky_nav = 'nv-sticky-bottom-nav' in html
        has_old_nav = 'nv-bottom-nav' in html and not has_sticky_nav
        has_emoji_icon = 'nv-bottom-icon' in html
        has_script_nav = 'nav.js' in html
        print(f"{url} -> HTTP {resp.status_code} | StickyNav: {has_sticky_nav} | OldNav: {has_old_nav} | EmojiNav: {has_emoji_icon} | nav.js: {has_script_nav}")
    except Exception as e:
        print(f"{url} -> ERROR: {e}")
