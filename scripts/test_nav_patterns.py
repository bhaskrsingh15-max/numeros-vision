import glob
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

pattern = re.compile(r'(<ul[^>]*class=["\']nv-nav-menu["\'][^>]*>\s*)(.*?)(<li[^>]*>\s*<a[^>]+href=["\']/about/["\'][^>]*>About Us</a>\s*</li>)', re.DOTALL | re.IGNORECASE)

files = glob.glob('app/static/*.html') + glob.glob('app/static/tools/*.html') + glob.glob('app/static/blog/*.html')

matched = []
unmatched = []

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()
    if 'nv-nav-menu' in content:
        if pattern.search(content):
            matched.append(fpath)
        else:
            unmatched.append(fpath)

print(f"Matched {len(matched)} files where 'About Us' can be identified after nv-nav-menu")
print(f"Unmatched {len(unmatched)} files with nv-nav-menu")
if unmatched:
    print("Unmatched samples:")
    for u in unmatched[:5]:
        print(" ", u)
