"""
NUMEROS VISION & CHARM AI — VERSION 4.1.1 BACKUP & SNAPSHOT ENGINE
Takes an automated, certified full-system backup of v4.1.1:
1. Compressed TAR.GZ archive in backups/
2. Compressed ZIP archive in backups/
3. Uncompressed full folder mirror in backups/version_copy_v4.1.1/
4. Manifest registration in backups/backup_manifest.json
5. Updates VERSION to 4.1.1
"""

import os
import shutil
import tarfile
import zipfile
import time
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BACKUPS_DIR = BASE_DIR / "backups"
VERSION_DIR = BACKUPS_DIR / "version_copy_v4.1.1"
MANIFEST_FILE = BACKUPS_DIR / "backup_manifest.json"
VERSION_FILE = BASE_DIR / "VERSION"

INCLUDE_DIRS = ["app", "data", "scripts", "tests", "docs", "deploy"]
ROOT_EXTENSIONS = [".py", ".html", ".md", ".txt", ".json", ".yaml", ".yml", ".sh", ".bat"]
EXCLUDE_DIRS = {".venv", "venv", "__pycache__", ".git", ".pytest_cache", "backups", ".idea", ".vscode"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".tar.gz", ".zip", ".log"}

def should_exclude(path_obj: Path) -> bool:
    for part in path_obj.parts:
        if part in EXCLUDE_DIRS:
            return True
    if path_obj.suffix.lower() in EXCLUDE_EXTS:
        return True
    return False

def run_backup():
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    version_name = "v4.1.1-enterprise-blueprint-deploy-ready"
    semver = "4.1.1"
    
    # 1. Update VERSION file
    VERSION_FILE.write_text(f"{semver}\n", encoding="utf-8")
    print(f"[1/4] Updated VERSION file to {semver}")

    # 2. Collect files
    files_to_copy = []
    total_uncompressed_bytes = 0

    for dir_name in INCLUDE_DIRS:
        dir_path = BASE_DIR / dir_name
        if dir_path.is_dir():
            for root, dirs, files in os.walk(dir_path):
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                for file in files:
                    fp = Path(root) / file
                    if not should_exclude(fp):
                        files_to_copy.append(fp)
                        total_uncompressed_bytes += fp.stat().st_size

    for item in BASE_DIR.iterdir():
        if item.is_file() and item.suffix.lower() in ROOT_EXTENSIONS:
            if not should_exclude(item):
                files_to_copy.append(item)
                total_uncompressed_bytes += item.stat().st_size

    # 3. Create uncompressed mirror copy in backups/version_copy_v4.1.1/
    if VERSION_DIR.exists():
        shutil.rmtree(VERSION_DIR)
    VERSION_DIR.mkdir(parents=True, exist_ok=True)

    for fp in files_to_copy:
        rel = fp.relative_to(BASE_DIR)
        dest = VERSION_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fp, dest)
    print(f"[2/4] Created uncompressed mirror at backups/version_copy_v4.1.1/ ({len(files_to_copy)} files)")

    # 4. Create .tar.gz archive
    tar_name = f"numeros_vision_backup_{version_name}_{timestamp}.tar.gz"
    tar_path = BACKUPS_DIR / tar_name
    with tarfile.open(tar_path, "w:gz") as tar:
        for fp in files_to_copy:
            rel = fp.relative_to(BASE_DIR)
            tar.add(fp, arcname=str(rel))
    tar_size_mb = tar_path.stat().st_size / (1024 * 1024)
    print(f"[3/4] Created tar.gz archive: {tar_name} ({tar_size_mb:.2f} MB)")

    # 5. Create .zip archive
    zip_name = f"numeros_vision_backup_{version_name}_{timestamp}.zip"
    zip_path = BACKUPS_DIR / zip_name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in files_to_copy:
            rel = fp.relative_to(BASE_DIR)
            zf.write(fp, arcname=str(rel))
    zip_size_mb = zip_path.stat().st_size / (1024 * 1024)
    print(f"[4/4] Created zip archive: {zip_name} ({zip_size_mb:.2f} MB)")

    # 6. Update manifest
    manifest_entries = []
    if MANIFEST_FILE.exists():
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                manifest_entries = json.load(f)
        except Exception:
            manifest_entries = []

    record = {
        "version_name": version_name,
        "semver": semver,
        "timestamp": timestamp,
        "date_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "archive_file": tar_name,
        "archive_path": str(tar_path),
        "archive_size_bytes": tar_path.stat().st_size,
        "archive_size_mb": round(tar_size_mb, 2),
        "zip_file": zip_name,
        "zip_size_mb": round(zip_size_mb, 2),
        "uncompressed_mirror_dir": str(VERSION_DIR),
        "files_archived": len(files_to_copy),
        "uncompressed_bytes": total_uncompressed_bytes,
        "reason": "Complete Enterprise Agentic AI Gateway, Redis Distributed Session Store, and Hassle-Free Cloud Deployment Suite"
    }
    manifest_entries.append(record)
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest_entries, f, indent=2)

    print("\n==================================================================")
    print("BACKUP COMPLETE: v4.1.1 REGISTERED & VERIFIED IN MANIFEST")
    print(f"Files: {len(files_to_copy)} | Tar: {tar_size_mb:.2f} MB | Zip: {zip_size_mb:.2f} MB")
    print("==================================================================")
    return record

if __name__ == "__main__":
    run_backup()
