"""
AUTOMATED FULL SYSTEM BACKUP ENGINE WITH SEMANTIC VERSIONING
Creates timestamped, compressed backups of the entire application, frontend,
prediction engines, database/corpora, and test suites.

Features:
- Explicit or auto-incrementing Backup Version Names (e.g. v3.2.1-charm-ai)
- Formats archives with version name: numeros_vision_backup_{version}_{timestamp}.tar.gz
- JSON Manifest tracking all backup versions, sizes, file counts, and metadata
- CLI support for:
    --version <name>   : Specify explicit backup version name
    --desc <text>      : Description / reason for this backup version
    --bump [patch|minor|major] : Auto-increment semver
    --list             : Show all backup versions
"""

import os
import re
import sys
import tarfile
import time
import json
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BACKUPS_DIR = BASE_DIR / "backups"
MANIFEST_FILE = BACKUPS_DIR / "backup_manifest.json"
VERSION_FILE = BASE_DIR / "VERSION"

# Directories and file types to include in backup
INCLUDE_DIRS = ["app", "data", "scripts", "tests", "docs", "deploy"]
ROOT_EXTENSIONS = [".py", ".html", ".md", ".txt", ".json", ".yaml", ".yml", ".sh", ".bat"]

# Items to strictly exclude to prevent bloat
EXCLUDE_DIRS = {".venv", "venv", "__pycache__", ".git", ".pytest_cache", "backups", ".idea", ".vscode"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".tar.gz", ".zip", ".log"}


def get_current_semver() -> str:
    """Read the current base semver from VERSION file."""
    if VERSION_FILE.exists():
        try:
            return VERSION_FILE.read_text(encoding="utf-8").strip()
        except Exception:
            pass
    return "3.2.1"


def set_current_semver(new_ver: str) -> None:
    """Persist new semver into VERSION file."""
    try:
        VERSION_FILE.write_text(new_ver.strip() + "\n", encoding="utf-8")
    except Exception as e:
        print(f"Warning: could not write VERSION file: {e}")


def bump_semver(current: str, part: str = "patch") -> str:
    """Bump major, minor, or patch in semver string."""
    m = re.match(r"^v?(\d+)\.(\d+)\.(\d+)", current)
    if not m:
        return "3.2.2"
    major, minor, patch = int(m.group(1)), int(m.group(2)), int(m.group(3))
    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    else:  # patch
        patch += 1
    return f"{major}.{minor}.{patch}"


def sanitize_filename_token(token: str) -> str:
    """Convert version name string to filesystem-safe token."""
    cleaned = re.sub(r"[^\w\.-]", "_", token.strip())
    return re.sub(r"_+", "_", cleaned).strip("_")


def should_exclude(path_obj: Path) -> bool:
    for part in path_obj.parts:
        if part in EXCLUDE_DIRS:
            return True
    if path_obj.suffix.lower() in EXCLUDE_EXTS:
        return True
    return False


def load_manifest() -> list:
    if MANIFEST_FILE.exists():
        try:
            with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []


def save_manifest(manifest: list) -> None:
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)


def list_backups() -> None:
    manifest = load_manifest()
    print("=" * 88)
    print("NUMEROS VISION — BACKUP VERSION CATALOG")
    print(f"Directory: {BACKUPS_DIR}")
    print("=" * 88)
    if not manifest:
        print("No backups recorded yet in manifest.")
        print("=" * 88)
        return

    print(f"{'VER NAME':<24} | {'TIMESTAMP':<16} | {'SIZE':<9} | {'FILES':<6} | {'DESCRIPTION'}")
    print("-" * 88)
    for entry in manifest:
        v_name = entry.get("version_name", entry.get("archive_file", "unknown"))[:24]
        t_stamp = entry.get("timestamp", "")
        size = f"{entry.get('archive_size_mb', 0):.2f} MB"
        files = str(entry.get("files_archived", 0))
        desc = entry.get("reason", entry.get("description", ""))[:32]
        print(f"{v_name:<24} | {t_stamp:<16} | {size:<9} | {files:<6} | {desc}")
    print("=" * 88)
    print(f"Total Backups: {len(manifest)}\n")


def take_backup(
    version_name: str = None,
    description: str = "Automated pre-change snapshot",
    bump_type: str = None
) -> dict:
    BACKUPS_DIR.mkdir(parents=True, exist_ok=True)
    timestamp_str = time.strftime("%Y%m%d_%H%M%S")
    current_ver = get_current_semver()

    # Determine version string
    if bump_type:
        semver = bump_semver(current_ver, bump_type)
        set_current_semver(semver)
        if not version_name:
            version_name = f"v{semver}"
    elif version_name:
        # Check if version_name has semver inside it
        m = re.search(r"(\d+\.\d+\.\d+)", version_name)
        if m:
            semver = m.group(1)
            set_current_semver(semver)
        else:
            semver = current_ver
    else:
        # Default: use current semver
        semver = current_ver
        version_name = f"v{semver}"

    # Ensure version_name starts with 'v' if it's purely digits/dots
    if re.match(r"^\d+\.\d+", version_name):
        version_name = f"v{version_name}"

    clean_ver = sanitize_filename_token(version_name)
    archive_name = f"numeros_vision_backup_{clean_ver}_{timestamp_str}.tar.gz"
    archive_path = BACKUPS_DIR / archive_name

    file_count = 0
    total_uncompressed_bytes = 0

    print(f"\n=== INITIATING BACKUP VERSION: {version_name} ===")
    print(f"Semver:     {semver}")
    print(f"Timestamp:  {timestamp_str}")
    print(f"Target:     {archive_name}")
    print(f"Reason:     {description}")

    with tarfile.open(archive_path, "w:gz") as tar:
        # 1. Add directories
        for dir_name in INCLUDE_DIRS:
            dir_path = BASE_DIR / dir_name
            if dir_path.is_dir():
                for root, dirs, files in os.walk(dir_path):
                    dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                    for file in files:
                        file_path = Path(root) / file
                        if not should_exclude(file_path):
                            rel_path = file_path.relative_to(BASE_DIR)
                            tar.add(file_path, arcname=str(rel_path))
                            file_count += 1
                            total_uncompressed_bytes += file_path.stat().st_size

        # 2. Add root project files
        for item in BASE_DIR.iterdir():
            if item.is_file() and item.suffix.lower() in ROOT_EXTENSIONS:
                if not should_exclude(item):
                    tar.add(item, arcname=item.name)
                    file_count += 1
                    total_uncompressed_bytes += item.stat().st_size

    archive_size_bytes = archive_path.stat().st_size
    archive_size_mb = archive_size_bytes / (1024 * 1024)

    record = {
        "version_name": version_name,
        "semver": semver,
        "timestamp": timestamp_str,
        "date_iso": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "archive_file": archive_name,
        "archive_path": str(archive_path),
        "archive_size_bytes": archive_size_bytes,
        "archive_size_mb": round(archive_size_mb, 2),
        "files_archived": file_count,
        "uncompressed_bytes": total_uncompressed_bytes,
        "reason": description
    }

    manifest = load_manifest()
    manifest.append(record)
    save_manifest(manifest)

    print(f"-> SUCCESS: Backup Version '{version_name}' Created!")
    print(f"-> Archived: {file_count} files ({archive_size_mb:.2f} MB compressed)")
    print(f"-> Manifest logged to {MANIFEST_FILE.name}")
    print("============================================================\n")
    return record


def main():
    parser = argparse.ArgumentParser(description="Numeros Vision Automated Versioned Backup Tool")
    parser.add_argument("--version", "-v", type=str, default=None, help="Explicit backup version name (e.g. v3.2.1-b2b-offloaded)")
    parser.add_argument("--desc", "-d", type=str, default=None, help="Description or reason for backup")
    parser.add_argument("--bump", "-b", choices=["patch", "minor", "major"], default=None, help="Auto-bump semver")
    parser.add_argument("--list", "-l", action="store_true", help="List all backup versions")
    parser.add_argument("positional_args", nargs="*", help="Optional version name and description")

    args = parser.parse_args()

    if args.list:
        list_backups()
        return

    version_name = args.version
    desc = args.desc

    # Handle positional args if flags not explicitly used
    if not version_name and args.positional_args:
        first = args.positional_args[0]
        # Check if first arg looks like a version name (e.g. v3.2.1 or v3.2.1-slug)
        if re.match(r"^v?\d+\.\d+", first) or first.startswith("v"):
            version_name = first
            if len(args.positional_args) > 1 and not desc:
                desc = " ".join(args.positional_args[1:])
        elif not desc:
            desc = " ".join(args.positional_args)

    if not desc:
        desc = "Snapshot triggered before changes"

    take_backup(version_name=version_name, description=desc, bump_type=args.bump)


if __name__ == "__main__":
    main()
