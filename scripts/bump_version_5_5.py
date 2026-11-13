import os
import re

# 1. Update sw.js
with open('app/static/sw.js', 'r', encoding='utf-8') as f:
    sw = f.read()

sw = re.sub(r'const CACHE_NAME = [\'"][^\'"]+[\'"];', "const CACHE_NAME = 'numeros-static-v5.5.0-charm-logo-canonical';", sw)
sw = re.sub(r'const STATIC_CACHE = [\'"][^\'"]+[\'"];', "const STATIC_CACHE = 'numeros-static-v5.5.0-charm-logo-canonical';", sw)
sw = re.sub(r'const API_CACHE = [\'"][^\'"]+[\'"];', "const API_CACHE = 'numeros-api-v5.5.0-charm-logo-canonical';", sw)

with open('app/static/sw.js', 'w', encoding='utf-8') as f:
    f.write(sw)
print("Updated sw.js cache name to v5.5.0-charm-logo-canonical")

# 2. Update query strings in all HTML files
css_pattern = re.compile(r'roadmap_components\.css(\?v=[a-zA-Z0-9\.\-_]+)?')
nav_pattern = re.compile(r'nav\.js(\?v=[a-zA-Z0-9\.\-_]+)?')

count = 0
for root, dirs, files in os.walk('app'):
    for f in files:
        if f.endswith('.html'):
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as file:
                content = file.read()

            new_c = css_pattern.sub('roadmap_components.css?v=5.5.0', content)
            new_c = nav_pattern.sub('nav.js?v=5.5.0', new_c)

            if new_c != content:
                with open(fp, 'w', encoding='utf-8') as file:
                    file.write(new_c)
                count += 1

print(f"Updated cache-busting query params in {count} HTML files to v=5.5.0")
