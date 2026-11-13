import glob
import re

files = [
    'app/static/index.html',
    'app/static/blog/gemstone-remedies.html',
    'app/static/blog/life-path-numbers-explained.html',
    'app/static/blog/vedic-gemstone-remedies.html',
    'app/static/blog/what-is-numerology.html',
    'app/static/tools/life-path-calculator.html',
    'app/static/tools/lo-shu-grid.html',
    'app/static/tools/lucky-number.html',
    'app/static/tools/name-numerology.html',
]

pattern = re.compile(r'\s*<a\s+href=[\"\']/docs[\"\'][^>]*>API Docs</a>\s*', re.IGNORECASE)

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content, count = pattern.subn('\n', content)
    if count > 0:
        # Clean up any potential double empty lines in footer-links
        new_content = re.sub(r'(\n\s*){3,}', '\n\n', new_content)
        with open(fpath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Removed {count} API Docs link(s) from {fpath}")
    else:
        print(f"No API Docs link found in {fpath}")
