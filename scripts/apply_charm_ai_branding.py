"""
SCRIPT: Apply Charm AI Brand Name & Remove Oracle from all Frontend Templates
Updates all HTML templates in app/static to:
1. Remove all instances of 'oracle' from links, element IDs, functions, and text.
2. Standardize brand name as 'CHARM AI' with 'ANVEIL EVERY CHARM'.
3. Point logo marks to '/logos/charm-ai-logo.svg'.
"""

import os
import glob
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"


def process_html_files():
    html_files = list(STATIC_DIR.glob("**/*.html"))
    updated_files = 0

    for file_path in html_files:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        original_content = content

        # 1. Replace nav-group-oracle with nav-group-charm
        content = content.replace('id="nav-group-oracle"', 'id="nav-group-charm"')
        content = content.replace("'nav-group-oracle'", "'nav-group-charm'")
        content = content.replace('"nav-group-oracle"', '"nav-group-charm"')

        # 2. Replace acc-group-oracle with acc-group-charm
        content = content.replace('id="acc-group-oracle"', 'id="acc-group-charm"')
        content = content.replace("'acc-group-oracle'", "'acc-group-charm'")
        content = content.replace('"acc-group-oracle"', '"acc-group-charm"')

        # 3. Replace /#ai-oracle with /#charm-ai
        content = content.replace('href="/#ai-oracle"', 'href="/#charm-ai"')
        content = content.replace('src="http://localhost:8000/#ai-oracle"', 'src="http://localhost:8000/#charm-ai"')
        content = content.replace('http://localhost:8000/#ai-oracle', 'http://localhost:8000/#charm-ai')

        # 4. In brand header lockup, set Brand Title to CHARM AI
        content = content.replace('<div class="brand-title">NUMEROS VISION</div>', '<div class="brand-title">CHARM AI</div>')
        content = content.replace('title="Numeros Vision — Anveil Every Charm"', 'title="Charm AI — Anveil Every Charm"')
        content = content.replace('alt="Numeros Vision - Anveil Every Charm"', 'alt="Charm AI - Anveil Every Charm"')

        # 5. Point logo mark image tags to charm-ai-logo.svg
        content = content.replace('src="/logos/nv-logo-mark.svg"', 'src="/logos/charm-ai-logo.svg"')

        # 6. Replace any remaining visible 'Charm AI Oracle' or 'Oracle Consultation'
        content = content.replace('Charm AI Oracle', 'Charm AI')
        content = content.replace('Charm AI Consultation', 'Charm AI Counsel')

        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            updated_files += 1
            print(f"Updated: {file_path.name}")

    print(f"\nTotal HTML files updated: {updated_files}/{len(html_files)}")


if __name__ == "__main__":
    process_html_files()
