import os
import shutil
import zipfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
BACKUPS_DIR = BASE_DIR / "backups"
COPY_DIR = BACKUPS_DIR / "version_copy_v4.0.5"
ZIP_PATH = BACKUPS_DIR / "numeros_vision_full_backup_v4.0.5.zip"

EXCLUDE_DIRS = {".venv", "venv", "__pycache__", ".git", ".pytest_cache", "backups", ".idea", ".vscode"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".tar.gz", ".zip", ".log"}

# 1. Clean previous copy folder if exists
if COPY_DIR.exists():
    shutil.rmtree(COPY_DIR)
COPY_DIR.mkdir(parents=True, exist_ok=True)

# 2. Gather files
copied_files = 0
with zipfile.ZipFile(ZIP_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(BASE_DIR):
        # Exclude directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        rel_root = Path(root).relative_to(BASE_DIR)
        
        # Don't copy anything inside backups/
        if "backups" in rel_root.parts:
            continue
            
        for f in files:
            full_path = Path(root) / f
            if full_path.suffix.lower() in EXCLUDE_EXTS:
                continue
                
            rel_file = full_path.relative_to(BASE_DIR)
            dest_file = COPY_DIR / rel_file
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Copy file to uncompressed folder
            shutil.copy2(full_path, dest_file)
            
            # Add to full zip archive
            zf.write(full_path, arcname=f"numeros_vision_v4.0.5/{rel_file}")
            copied_files += 1

print(f"Successfully copied {copied_files} files to {COPY_DIR}")
print(f"Successfully created full ZIP archive at {ZIP_PATH} ({ZIP_PATH.stat().st_size / (1024*1024):.2f} MB)")
