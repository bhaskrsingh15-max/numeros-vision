"""
Targeted Clean Build Script for Numeros Vision Deployment Bundle
"""
import os
import zipfile

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_ZIP = os.path.join(ROOT_DIR, "numeros_vision_app_bundle.zip")

INCLUDE_DIRS = ["app", "configuration", "data", "deploy", "android", "ios"]
INCLUDE_FILES = [
    "requirements.txt",
    "Dockerfile",
    "Procfile",
    "app.yaml",
    ".dockerignore",
    ".env.example",
    "VERSION",
    "orchestrator.py",
    "phase2_d60_engine.py",
    "phase4_bnn_engine.py",
    "phase5_lal_kitab_engine.py",
    "phase6_correlation_engine.py",
    "phase7_kp_engine.py",
    "phase8_btr_engine.py"
]

EXCLUDE_DIRS = {"__pycache__", ".pytest_cache", "uploaded_books_and_notes"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".tar.gz"}

def build_bundle():
    print(f"Building clean deployment bundle {OUTPUT_ZIP}...")
    file_count = 0
    with zipfile.ZipFile(OUTPUT_ZIP, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add root files
        for f in INCLUDE_FILES:
            fp = os.path.join(ROOT_DIR, f)
            if os.path.exists(fp):
                zf.write(fp, f)
                file_count += 1
                print(f"Added root file: {f}")

        # Add include dirs
        for d in INCLUDE_DIRS:
            dp = os.path.join(ROOT_DIR, d)
            if not os.path.exists(dp):
                continue
            for root, dirs, files in os.walk(dp):
                dirs[:] = [sub for sub in dirs if sub not in EXCLUDE_DIRS]
                for file in files:
                    _, ext = os.path.splitext(file)
                    if ext.lower() in EXCLUDE_EXTS:
                        continue
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, ROOT_DIR)
                    zf.write(full_path, rel_path)
                    file_count += 1

    size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
    print(f"Clean bundle successfully created: {OUTPUT_ZIP} ({file_count} files, {size_mb:.2f} MB)")

if __name__ == "__main__":
    build_bundle()
