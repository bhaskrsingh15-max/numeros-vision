import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

app_dir = r"c:\Users\Bhaskr Singh\Downloads\AI Numrology\app"
matches = []

for root, dirs, files in os.walk(app_dir):
    for f in files:
        if f.endswith(('.html', '.py', '.js', '.css')):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                content = fp.read()
                # Check for emojis in bottom nav
                if 'nv-bottom-nav' in content or 'nv-sticky-bottom-nav' in content or 'bottom-nav' in content:
                    # check if emojis are present in navigation
                    emojis = re.findall(r'[\U0001F300-\U0001F9FF\u2600-\u26FF\u2700-\u27BF]', content)
                    # check if 'Home' is in header
                    has_home_nav = 'Home</a>' in content
                    matches.append((p, len(emojis), has_home_nav, 'nv-sticky-bottom-nav' in content, 'nv-bottom-nav' in content))

print(f"Total matching files: {len(matches)}")
for m in matches[:20]:
    print(m)
