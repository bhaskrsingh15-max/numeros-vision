import os
import re

def clean_file(path):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig = content
    # Remove strike-through spans with currency
    content = re.sub(r'<span[^>]*style="[^"]*text-decoration:\s*line-through[^"]*"[^>]*>[\s\S]*?</span>\s*', '', content)
    # Remove strike-through divs (e.g. 50% OFF)
    content = re.sub(r'<div[^>]*style="[^"]*text-decoration:\s*line-through[^"]*"[^>]*>[\s\S]*?</div>\s*', '', content)
    
    # Specific cleanup for template literals if any remain
    content = content.replace('Missing @ 1050', 'Missing @ ₹1,050')
    content = content.replace('Present @ 510', 'Present @ ₹510')
    content = content.replace('Missing @ ₹1050', 'Missing @ ₹1,050')
    content = content.replace('Present @ ₹510', 'Present @ ₹510')

    if content != orig:
        with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(content)
        print(f"Cleaned strike-through prices in {path}")
    else:
        print(f"No strike-through prices found in {path}")

for f in [
    'app/static/index.html',
    'app/static/tools/lo-shu-grid.html',
    'app/static/dashboard.html',
    'app/static/pricing.html',
    'app/static/charm_ai.html',
    'app/static/birth_number_calculator.html'
]:
    clean_file(f)
