-- NUMEROS VISION: CLOUDFLARE D1 DATABASE SCHEMA
-- Migration: 0012_report_jobs_pipeline_stages.sql
-- Section 17.B Additive Report Pipeline Stages & Resumable Checkpoints (Strictly ZERO PII)
--
-- Pipeline order (shared deterministic + Write/Check stages):
--   1. calculate     ("Step 1 of 5: reading your birth date")
--   2. analyse       ("Step 2 of 5: checking your grid and cycles")
--   3. consolidate   ("Step 3 of 5: putting your reading together")
--   4. write         ("Step 4 of 5: writing your reading")
--   5. check_deliver ("Step 5 of 5: preparing your PDF")
--
-- Note: `report_jobs` already exists from 0001_initial_schema.sql & 0003_report_jobs_lifecycle.sql
-- with columns: id, user_id, subject_id, pack_id, order_id, status, r2_key, created_at,
-- completed_at, attempts, max_attempts, last_error, updated_at, downloaded_at.
-- All columns added below are strictly non-PII operational metadata.

PRAGMA foreign_keys = ON;

ALTER TABLE report_jobs ADD COLUMN tier TEXT NOT NULL DEFAULT 'basic';
ALTER TABLE report_jobs ADD COLUMN current_stage TEXT NOT NULL DEFAULT 'queued';
ALTER TABLE report_jobs ADD COLUMN last_completed_stage TEXT;
ALTER TABLE report_jobs ADD COLUMN stage_timestamps_json TEXT NOT NULL DEFAULT '{}';
ALTER TABLE report_jobs ADD COLUMN error_code TEXT;
ALTER TABLE report_jobs ADD COLUMN reading_plan_hash TEXT;
ALTER TABLE report_jobs ADD COLUMN fallback_sections_count INTEGER NOT NULL DEFAULT 0;

CREATE INDEX IF NOT EXISTS idx_report_jobs_stage ON report_jobs(status, current_stage);
CREATE INDEX IF NOT EXISTS idx_report_jobs_order ON report_jobs(order_id);
