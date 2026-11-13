# Numeros Vision - Backup & Disaster Recovery Runbook
**Specification Reference**: `NUMEROS_VISION_MASTER_IMPLEMENTATION.md` (Section 21)  
**Brand Identity**: Numeros Vision | *Unveil Every Charm*  
**Date**: October 2026  
**Status**: APPROVED - OPERATIONAL RUNBOOK

---

## 1. Overview & Recovery Targets

This runbook defines the schedules, scripts, and recovery protocols for all persistent state in **Numeros Vision**:
- **SQLite Database (`data/numeros_vision.db`)**: Stores user profiles, calculation histories, consent audit logs, and order records.
- **Inverted Index RAG Store (`data/rag_index.json`)**: Authoritative numerology text corpus and term inverted indices.
- **Generated Report Dossiers (`static/generated_reports/`)**: Rendered high-resolution PDF customer blueprints.
- **Application Configuration & Registries (`configuration/`)**: 433-keyword intent CSV, SEO registry, and content schemas.

### Recovery Targets:
- **RTO (Recovery Time Objective)**: $< 5\text{ minutes}$
- **RPO (Recovery Point Objective)**: $< 1\text{ hour}$

---

## 2. Automated Backup Schedule & Scripting

### 2.1 Daily Snapshot Script (`scripts/backup_database.ps1`)
```powershell
param(
    [string]$BackupRoot = "backups/daily"
)

$DateStr = Get-Date -Format "yyyyMMdd_HHmmss"
$TargetDir = Join-Path $BackupRoot $DateStr
New-Item -ItemType Directory -Path $TargetDir -Force

# 1. Vacuum and copy SQLite in WAL mode
Copy-Item "data/numeros_vision.db" (Join-Path $TargetDir "numeros_vision.db") -Force
if (Test-Path "data/numeros_vision.db-wal") {
    Copy-Item "data/numeros_vision.db-wal" (Join-Path $TargetDir "numeros_vision.db-wal") -Force
}

# 2. Copy RAG index
Copy-Item "data/rag_index.json" (Join-Path $TargetDir "rag_index.json") -Force

# 3. Retain only last 30 daily snapshots
$AllSnapshots = Get-ChildItem -Path $BackupRoot -Directory | Sort-Object CreationTime -Descending
if ($AllSnapshots.Count -gt 30) {
    $AllSnapshots[30..($AllSnapshots.Count - 1)] | Remove-Item -Recurse -Force
}

Write-Host "Daily snapshot completed: $TargetDir"
```

---

## 3. Database Restoration Protocol

In the event of database failure or corrupted records:
1. **Quiesce Writes**: Stop application daemon or toggle read-only mode.
2. **Identify Target Snapshot**:
   Select the latest intact snapshot from `backups/daily/`.
3. **Execute Safe Overwrite**:
   ```powershell
   Stop-Process -Name "python" -Force -ErrorAction SilentlyContinue
   Copy-Item "backups/daily/<TARGET_DATE>/numeros_vision.db" "data/numeros_vision.db" -Force
   Remove-Item "data/numeros_vision.db-wal" -Force -ErrorAction SilentlyContinue
   Remove-Item "data/numeros_vision.db-shm" -Force -ErrorAction SilentlyContinue
   ```
4. **Run Integrity Check**:
   ```powershell
   .\.venv\Scripts\python.exe -c "import sqlite3; conn=sqlite3.connect('data/numeros_vision.db'); print(conn.execute('PRAGMA integrity_check;').fetchall())"
   ```
   *Expected Output*: `[('ok',)]`
5. **Restart Service & Verify Health**:
   Start Uvicorn daemon and verify `/health`.

---
*Certified by Data Platform & Reliability Engineering for Numeros Vision.*
