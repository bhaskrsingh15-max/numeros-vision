import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
STATIC_DIR = os.path.join(ROOT_DIR, "app", "static")

FAVICON_BLOCK = """  <!-- Standardized Favicon & Brand Touch Icons -->
  <link rel="icon" type="image/svg+xml" href="/logos/nv-logo-mark.svg" />
  <link rel="icon" type="image/png" sizes="32x32" href="/static/icons/favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="/static/icons/favicon-16x16.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="/static/icons/apple-touch-icon.png" />
  <link rel="shortcut icon" href="/favicon.ico" />"""

ICON_REGEX = re.compile(
    r'(?:[ \t]*<!--[^\n]*?(?:Favicon|Icons?|touch-icon)[^\n]*?-->\n)?'
    r'(?:[ \t]*<link[^>]*rel=["\'](?:shortcut\s+)?(?:icon|apple-touch-icon|apple-touch-icon-precomposed)["\'][^>]*>\s*)+',
    re.IGNORECASE
)

updated_count = 0
total_count = 0

for root, dirs, files in os.walk(STATIC_DIR):
    for f in files:
        if not f.endswith(".html"):
            continue
        total_count += 1
        path = os.path.join(root, f)
        with open(path, "r", encoding="utf-8") as fh:
            content = fh.read()

        head_match = re.search(r"<head[^>]*>", content, re.IGNORECASE)
        if not head_match:
            continue

        head_start = head_match.end()

        # Check if existing icon tags exist in <head>
        existing_icons = ICON_REGEX.search(content[:head_match.end() + 3500])
        if existing_icons:
            new_content = content[:existing_icons.start()] + FAVICON_BLOCK + "\n" + content[existing_icons.end():]
        else:
            # Insert right after <head> or viewport
            viewport_m = re.search(r'<meta[^>]*name=["\']viewport["\'][^>]*>', content, re.I)
            if viewport_m:
                insert_pos = viewport_m.end()
                new_content = content[:insert_pos] + "\n" + FAVICON_BLOCK + content[insert_pos:]
            else:
                new_content = content[:head_start] + "\n" + FAVICON_BLOCK + content[head_start:]

        if new_content != content:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new_content)
            updated_count += 1

print(f"Standardized favicons across {updated_count} / {total_count} HTML pages in {STATIC_DIR}!")
