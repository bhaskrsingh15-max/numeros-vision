"""
ZERO-COST AUTOMATED DATABASE & KNOWLEDGE BASE BACKUP SCRIPT
Creates compressed gzip backups of the RAG Knowledge Base, Consent Ledger, and User Schemas.
Requires zero paid backup services — runs locally or on cron at $0 cost.
"""

import os
import tarfile
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
BACKUP_DIR = BASE_DIR / "backups"

def create_backup():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"prediction_engine_backup_{timestamp}.tar.gz"
    
    print(f"Starting zero-cost backup to {backup_path}...")
    with tarfile.open(backup_path, "w:gz") as tar:
        if DATA_DIR.exists():
            tar.add(DATA_DIR, arcname="data")
            print("  -> Compressed data/ directory.")
            
    backup_size_kb = os.path.getsize(backup_path) / 1024.0
    print(f"Backup Complete! File Size: {backup_size_kb:.2f} KB")
    return str(backup_path)

if __name__ == "__main__":
    create_backup()
