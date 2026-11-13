"""
Rebuild numeros_vision_app_bundle.zip with latest code
"""
import os
import zipfile

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_ZIP = os.path.join(ROOT_DIR, "numeros_vision_app_bundle.zip")

EXCLUDE_DIRS = {
    ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".idea", ".vscode", "tmp", "temp"
}
EXCLUDE_EXTS = {
    ".pyc", ".pyo", ".zip", ".tar.gz", ".log"
}

def should_exclude(rel_path):
    parts = rel_path.replace("\\", "/").split("/")
    for p in parts:
        if p in EXCLUDE_DIRS:
            return True
    _, ext = os.path.splitext(rel_path)
    if ext.lower() in EXCLUDE_EXTS:
        return True
    return False

def build_zip():
    print(f"Building {OUTPUT_ZIP}...")
    file_count = 0
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(ROOT_DIR):
            # Prune excluded directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, ROOT_DIR)
                if should_exclude(rel_path):
                    continue
                zf.write(full_path, rel_path)
                file_count += 1

    size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"Bundle successfully created: {OUTPUT_ZIP} ({file_count} files, {size_mb:.2f} MB)")

if __name__ == "__main__":
    build_zip()
