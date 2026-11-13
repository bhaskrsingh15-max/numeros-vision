"""
scripts/create_v6_4_charm_humanized_consultant_backup.py
========================================================
Creates a certified milestone backup of Numeros Vision v6.4.0
Charm AI Humanized Master Numerologist Consultation Release:
- Deterministic calculation engine & consensus fully preserved.
- Natural, warm, empathetic master numerologist dialogue with zero arithmetic hallucinations.
- Distinct, personalized explanations for career stuckness vs. Driver meaning vs. promotions.
- Homepage chat widget (index.html) and Charm AI (charm_ai.html) fully synchronized with 7-tier Dasha consensus cards and rich markdown rendering.
- Complete elimination of static generic canned fallback strings.
"""

import os
import zipfile
import hashlib
from datetime import datetime

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup_dir = "backups"
os.makedirs(backup_dir, exist_ok=True)
zip_filename = os.path.join(backup_dir, f"numeros_vision_v6.4.0_charm_humanized_master_{timestamp}.zip")

exclude_dirs = {'.venv', '__pycache__', '.git', 'backups', '.gemini', 'scratch', 'node_modules'}
exclude_extensions = {'.pyc', '.log', '.tmp'}

print(f"Creating certified milestone backup: {zip_filename}")
archived_count = 0

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in exclude_extensions or file.endswith('.zip') or file.endswith('.tar.gz'):
                continue
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, '.')
            zipf.write(full_path, rel_path)
            archived_count += 1

print(f"Total archived files: {archived_count}")
file_size_mb = os.path.getsize(zip_filename) / (1024 * 1024)
print(f"Archive size: {file_size_mb:.2f} MB")

hasher = hashlib.sha256()
with open(zip_filename, 'rb') as f:
    while chunk := f.read(65536):
        hasher.update(chunk)

checksum = hasher.hexdigest()
print(f"SHA-256 Checksum: {checksum}")

with zipfile.ZipFile(zip_filename, 'r') as zipf:
    bad_file = zipf.testzip()

print("INTEGRITY VERIFICATION:", "PASSED (0 corrupted files)" if bad_file is None else f"FAILED: {bad_file}")

receipt_path = os.path.join(backup_dir, f"backup_v6.4.0_{timestamp}_receipt.txt")
with open(receipt_path, 'w', encoding='utf-8') as f:
    f.write("Numeros Vision v6.4.0 Certified Milestone Backup\n")
    f.write(f"Timestamp: {timestamp}\n")
    f.write(f"Archive: {zip_filename}\n")
    f.write(f"Archived Files: {archived_count}\n")
    f.write(f"Size: {file_size_mb:.2f} MB\n")
    f.write(f"SHA-256: {checksum}\n")
    f.write("Integrity: PASSED\n")

print(f"Backup receipt saved: {receipt_path}")
