# scripts/build_cloudflare_pages_bundle.py
import os
import zipfile

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "static")
OUTPUT_ZIP = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cloudflare_pages_upload.zip")

print(f"Creating Cloudflare Pages upload bundle from {STATIC_DIR}...")

total_files = 0
with zipfile.ZipFile(OUTPUT_ZIP, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(STATIC_DIR):
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, STATIC_DIR)
            zipf.write(full_path, rel_path)
            total_files += 1

size_mb = os.path.getsize(OUTPUT_ZIP) / (1024 * 1024)
print(f"Successfully created {OUTPUT_ZIP}!")
print(f"Total files: {total_files}, Archive Size: {size_mb:.2f} MB")
