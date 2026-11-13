import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

target_files = [
    r"app\static\calculator_hub.html",
    r"app\static\compare_hub.html",
    r"app\static\insights_hub.html",
    r"app\static\learn.html",
    r"app\static\logo-preview.html",
    r"app\static\sample_roadmap.html"
]

for p in target_files:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace minmax(330px/340px/350px/360px, 1fr) with minmax(min(100%, 320px), 1fr)
        new_content = re.sub(r'minmax\((?:330|340|350|360)px,\s*1fr\)', 'minmax(min(100%, 300px), 1fr)', content)
        
        # Ensure max-width: 100% and overflow-x: hidden on body
        if 'overflow-x: hidden' not in new_content:
            new_content = new_content.replace('body {', 'body {\n      overflow-x: hidden;\n      max-width: 100vw;', 1)
        
        if new_content != content:
            with open(p, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Adapted responsive grid in: {p}")
