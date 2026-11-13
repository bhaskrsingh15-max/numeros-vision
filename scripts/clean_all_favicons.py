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

total_clean = 0

for root, dirs, files in os.walk(STATIC_DIR):
    for f in files:
        if not f.endswith(".html"):
            continue
        path = os.path.join(root, f)
        with open(path, "r", encoding="utf-8") as fh:
            c = fh.read()

        head_m = re.search(r"(<head[^>]*>)(.*?)(</head>)", c, re.DOTALL | re.IGNORECASE)
        if not head_m:
            continue

        head_open = head_m.group(1)
        head_body = head_m.group(2)
        head_close = head_m.group(3)

        # Remove all existing icon links and comments
        head_body_clean = re.sub(
            r'[ \t]*<!--[^\n]*?(?:Favicon|Icons?|touch-icon)[^\n]*?-->\n?',
            '',
            head_body,
            flags=re.IGNORECASE
        )
        head_body_clean = re.sub(
            r'[ \t]*<link[^>]*rel=["\'](?:shortcut\s+)?(?:icon|apple-touch-icon|apple-touch-icon-precomposed)["\'][^>]*>\n?',
            '',
            head_body_clean,
            flags=re.IGNORECASE
        )

        # Place the canonical block directly after <head> or viewport
        viewport_m = re.search(r'(<meta[^>]*name=["\']viewport["\'][^>]*>\n?)', head_body_clean, re.IGNORECASE)
        if viewport_m:
            idx = viewport_m.end()
            new_head_body = head_body_clean[:idx] + "\n" + FAVICON_BLOCK + "\n" + head_body_clean[idx:]
        else:
            new_head_body = "\n" + FAVICON_BLOCK + "\n" + head_body_clean

        new_c = c[:head_m.start()] + head_open + new_head_body + head_close + c[head_m.end():]
        if new_c != c:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new_c)
            total_clean += 1

print(f"Perfect cleanup applied: {total_clean} HTML files updated with exactly one clean favicon block.")
