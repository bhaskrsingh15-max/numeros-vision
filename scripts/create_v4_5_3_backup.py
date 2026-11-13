import os
import zipfile
import datetime

def create_backup():
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"numeros_vision_v4.5.3_charm_star_squircle_thumbnail_certified_{timestamp}.zip"
    backup_path = os.path.join("backups", backup_filename)
    os.makedirs("backups", exist_ok=True)
    
    exclude_dirs = {'.venv', '__pycache__', '.git', 'node_modules', 'backups', '.pytest_cache'}
    exclude_extensions = {'.pyc', '.pyo'}

    print(f"Creating backup archive: {backup_path}")
    count = 0
    with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk('.'):
            dirs[:] = [d for d in dirs if d not in exclude_dirs and not d.startswith('.')]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                if ext in exclude_extensions:
                    continue
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, '.')
                zipf.write(file_path, arcname)
                count += 1

    size_mb = os.path.getsize(backup_path) / (1024 * 1024)
    print(f"Backup created successfully: {backup_filename} ({size_mb:.2f} MB, {count} files)")
    return backup_filename, size_mb, count

if __name__ == '__main__':
    create_backup()
