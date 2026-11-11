-- NUMEROS VISION: CLOUDFLARE D1 DATABASE SCHEMA
-- Migration: 0011_waitlist_notify_me.sql
-- DPDP 2023 Encrypted "Notify Me" Waitlist Storage (12-month retention, hash strictly for deduplication, delete-on-request).

CREATE TABLE IF NOT EXISTS waitlist_notify_me (
    id TEXT PRIMARY KEY,
    email_sha256 TEXT NOT NULL,
    email_enc TEXT NOT NULL,
    pack_id TEXT NOT NULL,
    purpose TEXT NOT NULL DEFAULT 'tell me when this report is available',
    consent_dpdp INTEGER NOT NULL DEFAULT 1,
    consent_text TEXT NOT NULL,
    consent_version TEXT NOT NULL DEFAULT 'dpdp_waitlist_v1.0',
    retention_months INTEGER NOT NULL DEFAULT 12,
    source_page TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    expires_at INTEGER NOT NULL,
    UNIQUE(email_sha256, pack_id)
);

CREATE INDEX IF NOT EXISTS idx_waitlist_notify_pack_exp ON waitlist_notify_me(pack_id, expires_at);
CREATE INDEX IF NOT EXISTS idx_waitlist_notify_hash ON waitlist_notify_me(email_sha256);
