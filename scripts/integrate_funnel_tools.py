"""
Script to integrate the Advanced Marketing Funnel (v1.5.0) across all calculators
and enforce brand spelling 'Anveil Every Charm'.
"""

import os
import re

TOOLS_DIR = os.path.join("app", "static", "tools")
STATIC_DIR = os.path.join("app", "static")

def fix_unveil_spelling(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace 'Unveil every charm' -> 'Anveil every charm'
    # and 'Unveil Master Dossier' -> 'Anveil Master Dossier'
    # and 'Unveil Every Charm' -> 'Anveil Every Charm'
    modified = re.sub(r'\bUnveil every charm\b', 'Anveil every charm', content)
    modified = re.sub(r'\bUnveil Every Charm\b', 'Anveil Every Charm', modified)
    modified = re.sub(r'\bUnveil Master Dossier\b', 'Anveil Master Dossier', modified)
    modified = re.sub(r'\bunveil every charm\b', 'anveil every charm', modified)

    if modified != content:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(modified)
        print(f"Fixed 'Unveil' spelling in {file_path}")


def add_funnel_script_if_missing(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if "funnel_journey.js" in content:
        return

    script_tag = '  <script src="/static/js/funnel_journey.js?v=1.5.0" defer></script>\n'
    if "</body>" in content:
        content = content.replace("</body>", f"{script_tag}</body>")
    elif "</head>" in content:
        content = content.replace("</head>", f"{script_tag}</head>")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Added funnel_journey.js to {file_path}")


def main():
    # 1. Fix spelling in all static HTML
    for root, _, files in os.walk(STATIC_DIR):
        for file in files:
            if file.endswith(".html"):
                path = os.path.join(root, file)
                fix_unveil_spelling(path)
                add_funnel_script_if_missing(path)

    print("Completed spelling and script tag integration across all static HTML files.")

if __name__ == "__main__":
    main()
