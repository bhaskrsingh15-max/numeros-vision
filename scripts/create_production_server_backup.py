import zipfile
import os
import datetime
import hashlib
import json

def create_backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    version = "v4.5.6"
    backup_name = f"numeros_vision_{version}_production_server_certified_{timestamp}.zip"
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, backup_name)

    excluded_dirs = {'.venv', '__pycache__', '.git', 'backups', '.pytest_cache', 'node_modules', '.idea', '.vscode'}
    excluded_exts = {'.pyc', '.log'}

    file_count = 0
    total_uncompressed_bytes = 0

    print(f"Creating certified server backup: {backup_path} ...")
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in excluded_dirs]
            for file in files:
                if any(file.endswith(ext) for ext in excluded_exts):
                    continue
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, '.')
                zf.write(filepath, arcname)
                file_count += 1
                total_uncompressed_bytes += os.path.getsize(filepath)

    # Compute SHA-256 hash
    sha256 = hashlib.sha256()
    with open(backup_path, 'rb') as f:
        while chunk := f.read(65536):
            sha256.update(chunk)
    file_hash = sha256.hexdigest()

    size_bytes = os.path.getsize(backup_path)
    size_mb = size_bytes / (1024 * 1024)

    # Integrity verification
    with zipfile.ZipFile(backup_path, 'r') as zf:
        bad_file = zf.testzip()
        if bad_file:
            raise RuntimeError(f"Corrupt file found in backup: {bad_file}")
        test_count = len(zf.namelist())

    manifest = {
        "version": version,
        "backup_filename": backup_name,
        "backup_path": os.path.abspath(backup_path),
        "timestamp": timestamp,
        "sha256": file_hash,
        "size_bytes": size_bytes,
        "size_mb": round(size_mb, 2),
        "total_files": file_count,
        "uncompressed_bytes": total_uncompressed_bytes,
        "integrity_verified": True,
        "components_included": [
            "App core engines & routes (Vedic, Chaldean, Lo Shu, Dasha)",
            "Enterprise Agentic AI Gateway, ATL, and Circuit Breakers",
            "Enhanced 60px header brand logo & tagline styling",
            "Harmonized single-line Charm AI header nav alignment",
            "Jupiter Gold Charm AI floating launcher & tooltip",
            "DPDP Act 2023 hardened Cookie Consent Banner & controller",
            "Full 34 Canonical Master Roadmap routes & 31 SEO Hubs",
            "All test suites & real-time verification scripts"
        ]
    }

    manifest_path = os.path.join(backup_dir, f"BACKUP_MANIFEST_{version}_{timestamp}.json")
    with open(manifest_path, 'w', encoding='utf-8') as mf:
        json.dump(manifest, mf, indent=2)

    print("======================================================================")
    print("CERTIFIED PRODUCTION SERVER BACKUP CREATED & VERIFIED")
    print("======================================================================")
    print(f"  Archive:       {backup_path}")
    print(f"  Size:          {size_mb:.2f} MB ({size_bytes:,} bytes)")
    print(f"  Files Packed:  {file_count} files (all CRC32 verified)")
    print(f"  SHA-256 Hash:  {file_hash}")
    print(f"  Manifest:      {manifest_path}")
    print("======================================================================")

if __name__ == "__main__":
    create_backup()
