-- NUMEROS VISION: CLOUDFLARE D1 DATABASE SCHEMA
-- Migration: 0010_email_otp_and_consents.sql
-- Email OTP passwordless authentication, verified checkout gating, and DPDP 2023 statutory consent ledger.
-- Non-destructive: no drops, no alters on existing tables.

-- 1. Email OTP Challenges Table (Hashed 6-digit codes, 10m expiry, 5-attempt limit, single-use)
CREATE TABLE IF NOT EXISTS email_otp_challenges (
    id TEXT PRIMARY KEY,
    email_hash TEXT NOT NULL,
    code_hash TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 5,
    expires_at INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    ip_hash TEXT NOT NULL,
    verified_at INTEGER
);

CREATE INDEX IF NOT EXISTS idx_email_otp_lookup ON email_otp_challenges(email_hash, expires_at);
CREATE INDEX IF NOT EXISTS idx_email_otp_ip ON email_otp_challenges(ip_hash, created_at);

-- 2. User Statutory Consents Ledger (DPDP 2023 Purpose-Specific Consent, Marketing OFF by default)
CREATE TABLE IF NOT EXISTS user_consents (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    purpose TEXT NOT NULL,
    consent_given INTEGER NOT NULL DEFAULT 0,
    text_version TEXT NOT NULL DEFAULT 'v1.0_placeholder_advocate_review',
    created_at INTEGER NOT NULL,
    ip_hash TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_user_consents_user ON user_consents(user_id, purpose);

-- 3. Durable Email Rate Limits & Spend Caps (Cross-Isolate Protection)
CREATE TABLE IF NOT EXISTS email_rate_limits (
    key TEXT PRIMARY KEY,
    count INTEGER NOT NULL DEFAULT 0,
    window_start INTEGER NOT NULL,
    expires_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_email_rate_limits_exp ON email_rate_limits(expires_at);
