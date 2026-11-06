-- NUMEROS VISION: CLOUDFLARE D1 DATABASE SCHEMA
-- Migration: 0003_report_jobs_lifecycle.sql
-- Enforces Commit 6b report_jobs lifecycle:
-- QUEUED -> PROCESSING -> COMPLETED -> DOWNLOADED (set on first signed download)
-- 3 retries (attempts >= 3) then FAILED with alert in audit_log.

PRAGMA foreign_keys = ON;

ALTER TABLE report_jobs ADD COLUMN attempts INTEGER NOT NULL DEFAULT 0;
ALTER TABLE report_jobs ADD COLUMN max_attempts INTEGER NOT NULL DEFAULT 3;
ALTER TABLE report_jobs ADD COLUMN last_error TEXT;
ALTER TABLE report_jobs ADD COLUMN updated_at INTEGER;
ALTER TABLE report_jobs ADD COLUMN downloaded_at INTEGER;

CREATE INDEX IF NOT EXISTS idx_report_jobs_status ON report_jobs(status, attempts);
