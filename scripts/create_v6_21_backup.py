import os
import zipfile
import datetime

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
backup_name = f"numeros_vision_v6.21.0_journey_monetization_charm_harmonized_{timestamp}.zip"
backup_path = os.path.join("backups", backup_name)

exclude_dirs = {'.git', 'node_modules', 'venv', '.venv', '__pycache__', '.gemini', 'backups'}

print(f"Creating backup: {backup_path}")
total_files = 0
with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('.'):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            if f.endswith(('.pyc', '.zip', '.tar.gz', '.log')):
                continue
            full_p = os.path.join(root, f)
            arc_p = os.path.relpath(full_p, '.')
            zf.write(full_p, arc_p)
            total_files += 1

print(f"Backup complete! Total files archived: {total_files}")
print(f"Saved to: {backup_path}")
