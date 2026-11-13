import os
import zipfile
import hashlib
import json
import datetime
import shutil
import sys

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUPS_DIR = os.path.join(BASE_DIR, "backups")
os.makedirs(BACKUPS_DIR, exist_ok=True)

VERSION = "v6.20.0"
TITLE = "seo_launch_and_humanized_charm_certified"
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

VERSION_DIR = os.path.join(BACKUPS_DIR, VERSION)
ZIP_FILENAME = f"numeros_vision_{VERSION}_{TITLE}_{TIMESTAMP}.zip"
ZIP_PATH = os.path.join(BACKUPS_DIR, ZIP_FILENAME)
RECEIPT_PATH = os.path.join(BACKUPS_DIR, f"backup_{VERSION}_{TIMESTAMP}_receipt.txt")
MANIFEST_PATH = os.path.join(BACKUPS_DIR, f"BACKUP_MANIFEST_{VERSION}_{TIMESTAMP}.json")

EXCLUDE_DIRS = {
    ".git", ".venv", "venv", "node_modules", "backups", "dist_cloudflare_pages",
    "__pycache__", ".gemini", ".idea", ".vscode"
}
EXCLUDE_EXTS = {".pyc", ".pyo", ".log", ".tmp"}

print(f"=== INITIATING CERTIFIED BACKUP: NUMEROS VISION {VERSION} ===")
print(f"Timestamp: {TIMESTAMP}")
print(f"Destination Zip: {ZIP_PATH}")

# 1. Archive to Zip
file_count = 0
total_uncompressed_bytes = 0
with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(BASE_DIR):
        # In-place directory prune
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith(".")]
        
        for f in files:
            if any(f.endswith(ext) for ext in EXCLUDE_EXTS):
                continue
            if f.endswith(".zip") or f.endswith(".tar.gz"):
                continue
            
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, BASE_DIR)
            
            zipf.write(full_path, arcname=rel_path)
            file_count += 1
            total_uncompressed_bytes += os.path.getsize(full_path)

# 2. Check Archive Integrity
print("Verifying archive integrity via testzip()...")
with zipfile.ZipFile(ZIP_PATH, "r") as zipf:
    bad_file = zipf.testzip()
    if bad_file:
        raise RuntimeError(f"Zip integrity check failed on file: {bad_file}")
print("Archive integrity verified: 0 errors detected (100% OK)!")

# 3. Calculate SHA-256
sha256 = hashlib.sha256()
with open(ZIP_PATH, "rb") as f:
    while chunk := f.read(1024 * 1024):
        sha256.update(chunk)
zip_hash = sha256.hexdigest()
zip_size_mb = os.path.getsize(ZIP_PATH) / (1024 * 1024)

# 4. Copy app/ into backups/v6.20.0/app/ for instant directory browsing
if os.path.exists(VERSION_DIR):
    shutil.rmtree(VERSION_DIR)
os.makedirs(VERSION_DIR, exist_ok=True)
app_src = os.path.join(BASE_DIR, "app")
app_dest = os.path.join(VERSION_DIR, "app")
shutil.copytree(app_src, app_dest, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.log"))

# 5. Write Manifest JSON
manifest_data = {
    "version": VERSION,
    "title": TITLE,
    "timestamp": TIMESTAMP,
    "archive_filename": ZIP_FILENAME,
    "archive_size_mb": round(zip_size_mb, 2),
    "total_files_archived": file_count,
    "uncompressed_size_mb": round(total_uncompressed_bytes / (1024 * 1024), 2),
    "sha256_checksum": zip_hash,
    "integrity_status": "PASSED_100_PERCENT",
    "key_milestones_included": [
        "Google Search Console & Bing Webmaster Verification (BingSiteAuth.xml, meta tags, IndexNow key)",
        "Dynamic 69-URL XML Sitemap (sitemap.xml) & Crawlable HTML Sitemap (/sitemap/)",
        "LLMs.txt & LLMs-Full.txt Specification Standards (zero code exposure, public citation only)",
        "Open Graph (1200x630) & Twitter Cards standard across all pages",
        "Contextual Internal Autolinking across all 24 blog articles",
        "Charm AI Humanization (removal of robotic astrological jargon, no headless Ketus, no 100% loss threats)",
        "Fixed 'ali' whole-word token matching for accurate Hindu/Sanatan vs Muslim faith detection",
        "Sanitized Day 16 Sub-date (The Strategic Visionary & Healer of Truth)",
        "Un-blurred Crisp Natal Lo Shu Grid on /charm-ai/ for full user trust",
        "Rebuilt Cloudflare Pages static distribution (326 files, cloudflare_pages_upload.zip)"
    ]
}

with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
    json.dump(manifest_data, f, indent=2, ensure_ascii=False)

# 6. Write Receipt TXT
receipt_content = f"""Numeros Vision {VERSION} Certified Milestone Backup
============================================================
Timestamp: {TIMESTAMP}
Archive: backups\\{ZIP_FILENAME}
Directory Mirror: backups\\{VERSION}\\app
Files Archived: {file_count}
Archive Size: {zip_size_mb:.2f} MB
Uncompressed Size: {total_uncompressed_bytes / (1024 * 1024):.2f} MB
SHA-256 Checksum: {zip_hash}
Integrity Check: PASSED (0 corrupted files)

Key Capabilities Locked In This Version:
----------------------------------------
1. Google Search Console & Bing Webmaster verification files & meta tags
2. IndexNow instant indexing key (49bf97a1d74343ce951918a3a0e676d4.txt)
3. 69 Canonical URLs XML Sitemap & Structured HTML Sitemap Directory (/sitemap/)
4. Modern LLMs.txt & LLMs-Full.txt with zero code/key exposure
5. Contextual Internal Autolinking across all 24 blog research articles
6. Humanized Charm AI Engine: eliminated fatalistic medieval jargon & headless Ketus
7. Whole-word token regex fixing faith detection for Anjali Sharma and all names
8. Sanitized Day 16 Sub-Birth Date (The Strategic Visionary & Healer of Truth)
9. Un-blurred, completely crisp and free Natal Lo Shu Grid on /charm-ai/
10. Updated build_bulletproof_dist.py & cloudflare_pages_upload.zip (326 files)

Status: CERTIFIED PRODUCTION MILESTONE LOCK
"""

with open(RECEIPT_PATH, "w", encoding="utf-8") as f:
    f.write(receipt_content)

print(f"\n[✓] Backup Complete!")
print(f"  Archive: {ZIP_PATH} ({zip_size_mb:.2f} MB)")
print(f"  Files: {file_count}")
print(f"  SHA-256: {zip_hash}")
print(f"  Receipt: {RECEIPT_PATH}")
print(f"  Manifest: {MANIFEST_PATH}")
print(f"  Directory: {VERSION_DIR}")
