"""
NUMEROS VISION — DEDICATED UI, UX & THEME BACKUP ENGINE
Packages all frontend design system assets, theme stylesheets, templates,
PWA mobile manifests, logos, and UI scripts into standalone ZIP & TAR.GZ archives.
"""

import os
import sys
import time
import json
import zipfile
import tarfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
BACKUPS_DIR = BASE_DIR / "backups"
THEME_MANIFEST_FILE = BACKUPS_DIR / "theme_ui_ux_manifest.json"
BACKUP_MANIFEST_FILE = BACKUPS_DIR / "backup_manifest.json"

VERSION = "v4.0.5-ui-ux-theme-harmony"

THEME_README = """# Numeros Vision — Master UI, UX & Theme Specification (v4.0.5)

## 1. Design System Foundations
- **Canvas (Venus Pearl)**:
  - Base Background: `#FFFDF7`
  - Mid Surface / Section: `#F7F3EA`
  - Card Background: `#FFFFFF`
  - Deep Surface: `#F0EBE0`
- **Luxury Accent (Jupiter Gold)**:
  - Primary Gold: `#C9A227`
  - Amber / Highlight: `#E2B84B`
  - Deep Bronze Gold: `#8B6914`
  - Border Gold: `rgba(201, 162, 39, 0.38)`
- **Intelligence Accent (Mercury Emerald)**:
  - Primary Emerald: `#16835B`
  - Secondary Jade: `#2AAE7A`
  - Emerald Tint: `rgba(22, 131, 91, 0.1)`
- **Typography & High-Contrast Readability**:
  - Primary Text: `#523E28` (Warm Deep Antique Jupiter Bronze — strictly ZERO harsh pitch black)
  - Muted Text: `#7A654D`
  - Faint Text: `#A89880`
  - Headings Font: `'Cormorant Garamond', Georgia, serif`
  - Body & UI Font: `'Inter', -apple-system, system-ui, sans-serif`
  - Numeric Accents Font: `'Cinzel', 'Cinzel Decorative', serif`

## 2. Directory Structure of This UI/UX Bundle
- `theme/`: Core CSS (`theme.css`) with all variables, animations, and typography rules.
- `templates/`:
  - `index.html`: Main home portal with Harmony Destiny Blueprint, calculators, Charm AI, and Dakshina plans.
  - `sample.html`: Luxury Celestial Master Blueprint report viewer UI.
  - `sample2.html`: Alternative mobile app bento-style UI layout.
  - `tools/`: 12 specialized numerology calculator interfaces.
  - `blog/`: 7 responsive editorial and guide templates.
  - Sub-pages: `pricing.html`, `about.html`, `contact.html`, `cdp.html`, `practitioner.html`, `privacy.html`, `terms.html`, `refund.html`, `404.html`.
- `pwa_app/`: `manifest.json` (PWA definition) & `sw.js` (Service Worker cache).
- `assets/`:
  - `logos/`: High-resolution SVG monogram seals, Charm AI logos, and hero badges.
  - `icons/`: PWA icons (192px, 512px) and favicons.
  - `social/`: OpenGraph cards and Twitter summary image assets.
  - `js/`: Client interactive telemetry, calculators, and DPDP cookie consent logic.

## 3. Brand Identity
- **Name**: Numeros Vision
- **Tagline**: Anveil Every Charm
- **Hero Title**: AI Numerology Calculator & Harmony Destiny Blueprint
"""

def create_theme_backup():
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    zip_filename = f"numeros_vision_ui_ux_theme_{VERSION}_{timestamp}.zip"
    tar_filename = f"numeros_vision_ui_ux_theme_{VERSION}_{timestamp}.tar.gz"
    
    zip_path = BACKUPS_DIR / zip_filename
    tar_path = BACKUPS_DIR / tar_filename
    
    file_list = []
    total_uncompressed = 0

    # Collect files from app/static
    for root, dirs, files in os.walk(STATIC_DIR):
        for f in files:
            full_path = Path(root) / f
            rel_to_static = full_path.relative_to(STATIC_DIR)
            file_list.append((full_path, rel_to_static))
            total_uncompressed += full_path.stat().st_size

    # 1. Create ZIP Archive
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("README_THEME_UI_UX.md", THEME_README)
        for full_path, rel_path in file_list:
            zf.write(full_path, arcname=f"ui_ux_theme/{rel_path}")

    # 2. Create TAR.GZ Archive
    with tarfile.open(tar_path, 'w:gz') as tf:
        import io
        readme_bytes = THEME_README.encode('utf-8')
        ti = tarfile.TarInfo(name="ui_ux_theme/README_THEME_UI_UX.md")
        ti.size = len(readme_bytes)
        ti.mtime = int(time.time())
        tf.addfile(ti, io.BytesIO(readme_bytes))
        
        for full_path, rel_path in file_list:
            tf.add(full_path, arcname=f"ui_ux_theme/{rel_path}")

    zip_size_bytes = zip_path.stat().st_size
    zip_size_mb = zip_size_bytes / (1024 * 1024)
    tar_size_bytes = tar_path.stat().st_size
    tar_size_mb = tar_size_bytes / (1024 * 1024)

    record = {
        "version_name": VERSION,
        "backup_type": "UI_UX_AND_THEME_STANDALONE",
        "timestamp": timestamp,
        "date_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "zip_archive": zip_filename,
        "zip_size_mb": round(zip_size_mb, 2),
        "tar_archive": tar_filename,
        "tar_size_mb": round(tar_size_mb, 2),
        "files_archived": len(file_list) + 1,
        "uncompressed_bytes": total_uncompressed + len(THEME_README.encode('utf-8')),
        "description": "Standalone backup of website & app UI/UX, Master Theme (Venus Pearl #FFFDF7 & Jupiter Gold #C9A227), PWA manifest, SVG seals, 12 tools, and Harmony Destiny Blueprint."
    }

    # Save to dedicated theme manifest
    theme_manifest = []
    if THEME_MANIFEST_FILE.exists():
        try:
            with open(THEME_MANIFEST_FILE, "r", encoding="utf-8") as f:
                theme_manifest = json.load(f)
        except Exception:
            theme_manifest = []
    theme_manifest.append(record)
    with open(THEME_MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(theme_manifest, f, indent=2)

    # Also register in main backup manifest
    if BACKUP_MANIFEST_FILE.exists():
        try:
            with open(BACKUP_MANIFEST_FILE, "r", encoding="utf-8") as f:
                main_manifest = json.load(f)
            main_manifest.append(record)
            with open(BACKUP_MANIFEST_FILE, "w", encoding="utf-8") as f:
                json.dump(main_manifest, f, indent=2)
        except Exception as e:
            print("Warning: Could not update main manifest:", e)

    print("============================================================")
    print("-> SUCCESS: Standalone UI, UX & Theme Backup Created!")
    print(f"-> ZIP Archive: {zip_filename} ({zip_size_mb:.2f} MB)")
    print(f"-> TAR.GZ Archive: {tar_filename} ({tar_size_mb:.2f} MB)")
    print(f"-> Total Frontend Files Archived: {len(file_list) + 1}")
    print(f"-> Dedicated Manifest: {THEME_MANIFEST_FILE.name}")
    print("============================================================")
    return record

if __name__ == "__main__":
    create_theme_backup()
