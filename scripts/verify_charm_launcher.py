import urllib.request
import re

def verify_homepage_launcher():
    url = "http://127.0.0.1:8000/"
    html = urllib.request.urlopen(url).read().decode('utf-8')
    
    # 1. Verification of Component IDs (Pure Thumbnail Launcher)
    assert 'id="charm-ai-launcher"' in html, "Missing #charm-ai-launcher"
    assert 'id="charm-bot-avatar-link"' in html, "Missing #charm-bot-avatar-link"
    assert 'id="charm-bot-close-btn"' in html, "Missing #charm-bot-close-btn"
    assert 'initCharmAILauncher' in html, "Missing initCharmAILauncher"
    assert 'charm-bot-avatar.svg' in html, "Missing charm-bot-avatar.svg"
    
    # 2. Verify that the avatar SVG has NO NV monogram
    avatar_svg = urllib.request.urlopen("http://127.0.0.1:8000/logos/charm-bot-avatar.svg").read().decode('utf-8')
    assert "CHARM AI" in avatar_svg, "Avatar must contain 'CHARM AI'"
    assert ">NV<" not in avatar_svg and ">N<" not in avatar_svg and ">V<" not in avatar_svg, "Avatar must NOT contain NV monogram"
    
    # 3. Check for banned marketing buzzwords
    banned = ["unlock", "elevate", "game-changer", "revolutionary", "seamless"]
    for b in banned:
        assert not re.search(r'\b' + re.escape(b) + r'\b', html, re.I), f"Banned word {b} found in homepage"
        
    # 4. Check CSS rules in roadmap_components.css
    css = urllib.request.urlopen("http://127.0.0.1:8000/static/css/roadmap_components.css").read().decode('utf-8')
    assert '.nv-charm-bot-launcher' in css, "Missing .nv-charm-bot-launcher CSS"
    assert '.nv-charm-bot-close' in css, "Missing .nv-charm-bot-close CSS"
    assert '.nv-charm-bot-avatar-btn' in css, "Missing .nv-charm-bot-avatar-btn CSS"
    assert 'nvPulseAura' in css, "Missing nvPulseAura CSS"
    
    print("ALL TESTS PASSED: Pure Charm AI floating launcher (zero NV logo) verified!")

if __name__ == "__main__":
    verify_homepage_launcher()
