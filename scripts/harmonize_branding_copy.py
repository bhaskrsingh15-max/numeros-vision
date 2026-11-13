"""
SCRIPT: Harmonize Master Branding & Tagline Across All Frontend HTML Templates
Enforces the Master Roadmap specification:
1. Exact master brand: 'Numeros Vision'
2. Tagline: 'Unveil Every Charm'
3. Charm AI is retained strictly as the assistant name only, not the master brand.
4. Primary brand logo mark points to '/logos/nv-logo-mark.svg' with 'Numeros Vision - Unveil Every Charm'.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"

def harmonize_branding():
    html_files = sorted(list(STATIC_DIR.glob("**/*.html")))
    updated_files = 0

    print("================================================================================")
    print("NUMEROS VISION — MASTER BRANDING & TAGLINE HARMONIZATION")
    print(f"Scanning {len(html_files)} HTML templates in {STATIC_DIR}")
    print("================================================================================")

    for file_path in html_files:
        # Skip backups or cache if any
        if "backup" in str(file_path).lower():
            continue

        content = file_path.read_text(encoding="utf-8", errors="ignore")
        original_content = content

        # 1. Restore master brand title in site header lockup
        content = content.replace(
            '<div class="brand-title">CHARM AI</div>\n        <div class="brand-gold-bar"></div>\n        <div class="brand-tagline">ANVEIL EVERY CHARM</div>',
            '<div class="brand-title">NUMEROS VISION</div>\n        <div class="brand-gold-bar"></div>\n        <div class="brand-tagline">UNVEIL EVERY CHARM</div>'
        )
        content = content.replace(
            '<div class="brand-title">CHARM AI</div>\n        <div class="brand-gold-bar"></div>\n        <div class="brand-tagline">UNVEIL EVERY CHARM</div>',
            '<div class="brand-title">NUMEROS VISION</div>\n        <div class="brand-gold-bar"></div>\n        <div class="brand-tagline">UNVEIL EVERY CHARM</div>'
        )
        content = content.replace(
            '<div class="brand-title">CHARM AI</div>',
            '<div class="brand-title">NUMEROS VISION</div>'
        )

        # 2. Harmonize logo mark image in header
        content = content.replace(
            '<img src="/logos/charm-ai-logo.svg" alt="Charm AI - Anveil Every Charm"',
            '<img src="/logos/nv-logo-mark.svg" alt="Numeros Vision - Unveil Every Charm"'
        )
        content = content.replace(
            '<img src="/logos/charm-ai-logo.svg" alt="Numeros Vision"',
            '<img src="/logos/nv-logo-mark.svg" alt="Numeros Vision - Unveil Every Charm"'
        )
        content = content.replace(
            '<img src="/logos/charm-ai-logo.svg" alt="Charm AI"',
            '<img src="/logos/nv-logo-mark.svg" alt="Numeros Vision - Unveil Every Charm"'
        )
        content = content.replace(
            '<img src="/logos/charm-ai-logo.svg" alt="Numeros Vision - Anveil Every Charm"',
            '<img src="/logos/nv-logo-mark.svg" alt="Numeros Vision - Unveil Every Charm"'
        )
        content = content.replace(
            '<img src="/logos/nv-logo-mark.svg" alt="Numeros Vision - Anveil Every Charm"',
            '<img src="/logos/nv-logo-mark.svg" alt="Numeros Vision - Unveil Every Charm"'
        )
        content = content.replace(
            '<img src="/logos/nv-logo-stacked.svg" alt="Numeros Vision — Anveil Every Charm"',
            '<img src="/logos/nv-logo-stacked.svg" alt="Numeros Vision — Unveil Every Charm"'
        )

        # 3. Harmonize brand-logo-link titles and aria labels
        content = content.replace(
            'title="Charm AI — Anveil Every Charm"',
            'title="Numeros Vision — Unveil Every Charm"'
        )
        content = content.replace(
            'title="Numeros Vision — Anveil Every Charm"',
            'title="Numeros Vision — Unveil Every Charm"'
        )
        content = content.replace(
            'title="Numeros Vision - Anveil Every Charm"',
            'title="Numeros Vision — Unveil Every Charm"'
        )

        # 4. Harmonize tagline spellings in copy and badges
        content = content.replace('ANVEIL EVERY CHARM', 'UNVEIL EVERY CHARM')
        content = content.replace('Anveil Every Charm', 'Unveil Every Charm')
        content = content.replace('anveil every charm', 'unveil every charm')
        content = content.replace('Anveil Access', 'Unlock Access')
        content = content.replace('Anveil Master Dossier', 'Unveil Master Dossier')
        content = content.replace('Anveil Your Personal Destiny', 'Unveil Your Personal Destiny')

        # 5. Harmonize footer copyright text
        content = content.replace(
            '© 2026 Numeros Vision. Anveil Every Charm. Deterministic AI Numerology.',
            '© 2026 Numeros Vision. Unveil Every Charm™. Deterministic AI Numerology.'
        )
        content = content.replace(
            '© 2026 Numeros Vision. Anveil Every Charm.',
            '© 2026 Numeros Vision. Unveil Every Charm™.'
        )

        if content != original_content:
            file_path.write_text(content, encoding="utf-8")
            updated_files += 1
            rel_path = file_path.relative_to(BASE_DIR)
            print(f"  [HARMONIZED] {rel_path}")

    print("================================================================================")
    print(f"COMPLETE: {updated_files}/{len(html_files)} HTML templates successfully harmonized.")
    print("Master Brand: 'Numeros Vision' | Tagline: 'Unveil Every Charm'")
    print("================================================================================")

if __name__ == "__main__":
    harmonize_branding()
