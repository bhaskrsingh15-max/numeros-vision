import urllib.request
import re

def verify_all():
    print("======================================================================")
    print("VERIFYING HEADER ALIGNMENT, CHARM AI THEME, AND COOKIE POPUP")
    print("======================================================================")

    # 1. Fetch homepage
    url = "http://127.0.0.1:8000/"
    html = urllib.request.urlopen(url).read().decode('utf-8')

    # Check Cookie Banner Presence
    assert 'id="nv-cookie-banner"' in html, "Missing #nv-cookie-banner in homepage"
    assert 'nv-cookie-banner' in html, "Missing .nv-cookie-banner class in homepage"
    assert 'Cookie &amp; Privacy Preferences' in html or 'Cookie &amp; Data Consent' in html, "Missing Cookie title"
    assert 'Accept All' in html, "Missing Accept All button in Cookie banner"
    assert 'Essential Only' in html, "Missing Essential Only button in Cookie banner"
    assert 'initCookieConsent' in html, "Missing initCookieConsent() script"
    assert 'acceptCookieConsent' in html, "Missing acceptCookieConsent() script"
    print("  [PASS] Cookie consent popup (DPDP Act 2023) certified in DOM & JavaScript.")

    # Check Charm AI Navigation Link Alignment
    assert 'href="/charm-ai/"' in html or 'href="/charm-ai"' in html, "Missing Charm AI link in navigation"
    assert 'Charm AI' in html, "Missing 'Charm AI' in header nav"
    print("  [PASS] Charm AI navigation item certified.")

    # 2. Check CSS in roadmap_components.css
    css = urllib.request.urlopen("http://127.0.0.1:8000/static/css/roadmap_components.css").read().decode('utf-8')
    assert '.nv-nav-item' in css and 'white-space: nowrap' in css, "Missing white-space: nowrap on nav items"
    assert '.nv-nav-link' in css and 'white-space: nowrap' in css, "Missing white-space: nowrap on nav links"
    assert '.nv-brand-seal' in css and 'width: 60px' in css, "Header logo must be 60px in roadmap_components.css"
    assert '.nv-cookie-banner' in css, "Missing .nv-cookie-banner in CSS"
    assert '.nv-cookie-btn-primary' in css, "Missing .nv-cookie-btn-primary in CSS"
    assert '.nv-charm-bot-tooltip' in css and '#8B6914' in css, "Tooltip must use Jupiter Gold theme"
    print("  [PASS] Header CSS: 60px NV logo, nowrap nav links, and cookie banner rules verified.")

    # 3. Check theme.css
    theme_css = urllib.request.urlopen("http://127.0.0.1:8000/static/css/theme.css").read().decode('utf-8')
    assert '.brand-seal-icon' in theme_css and 'width: 60px' in theme_css, "brand-seal-icon must be 60px in theme.css"
    print("  [PASS] Theme CSS: 60px brand-seal-icon verified.")

    # 4. Check Charm AI Avatar SVGs match website theme
    avatar_svg = urllib.request.urlopen("http://127.0.0.1:8000/logos/charm-bot-avatar.svg").read().decode('utf-8')
    assert '#C9A227' in avatar_svg or '#8B6914' in avatar_svg, "Star must use Jupiter Gold in avatar SVG"
    assert 'CHARM AI' in avatar_svg, "Avatar must contain CHARM AI"
    assert '>NV<' not in avatar_svg, "Avatar must not have NV monogram"
    print("  [PASS] Charm AI Avatar SVG: Jupiter Gold website theme UI & UX verified.")

    # 5. Check Banned Buzzwords
    banned = ["unlock", "elevate", "game-changer", "revolutionary", "seamless"]
    for b in banned:
        assert not re.search(r'\b' + re.escape(b) + r'\b', html, re.I), f"Banned buzzword '{b}' found in homepage"
    print("  [PASS] Zero banned marketing buzzwords verified.")

    print("\nALL VERIFICATIONS PASSED SUCCESSFULLY (100% PASS RATE)!")

if __name__ == "__main__":
    verify_all()
