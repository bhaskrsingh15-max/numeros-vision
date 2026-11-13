import glob
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

html_files = (
    glob.glob('app/static/*.html') +
    glob.glob('app/static/tools/*.html') +
    glob.glob('app/static/blog/*.html')
)

updated_count = 0

for path in html_files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    if 'nv-nav-menu' not in content:
        continue

    # Check if Home is already in nv-nav-menu
    menu_match = re.search(r'(<ul[^>]*class=["\']nv-nav-menu["\'][^>]*>)(.*?)</ul>', content, re.DOTALL)
    if not menu_match:
        continue

    menu_header = menu_match.group(1)
    menu_body = menu_match.group(2)

    if re.search(r'<a[^>]+href=["\'](?:/|index\.html)["\'][^>]*>\s*Home\s*</a>', menu_body, re.IGNORECASE):
        print(f"Skipping {path}: Home already present")
        continue

    # Determine if this file is the homepage (index.html)
    is_index = os.path.basename(path).lower() in ['index.html']
    active_attr = ' active' if is_index else ''

    home_li = f'''
          <!-- 1. Home -->
          <li class="nv-nav-item">
            <a href="/" class="nv-nav-link{active_attr}" title="Numeros Vision Home">Home</a>
          </li>
'''

    # Find the position of About Us or the first <li
    about_match = re.search(r'([ \t]*(?:<!--\s*\d*\.?\s*About\s*Us\s*-->\s*)?<li[^>]*>\s*<a[^>]+href=["\']/about/["\'][^>]*>About Us</a>\s*</li>)', menu_body, re.IGNORECASE)

    if about_match:
        # Insert Home right before About Us
        target = about_match.group(1)
        new_target = home_li.strip('\n') + '\n\n' + target
        new_menu_body = menu_body.replace(target, new_target, 1)
        new_content = content.replace(menu_body, new_menu_body, 1)
    else:
        # Fallback: insert right after <ul class="nv-nav-menu"...>
        new_menu_body = '\n' + home_li.strip('\n') + '\n' + menu_body
        new_content = content.replace(menu_body, new_menu_body, 1)

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)

    updated_count += 1
    print(f"Updated {path} with Home navigation link")

print(f"\nSuccessfully added Home to header navigation across {updated_count} files!")
