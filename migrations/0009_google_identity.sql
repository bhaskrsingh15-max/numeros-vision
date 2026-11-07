-- NUMEROS VISION: CLOUDFLARE D1 DATABASE SCHEMA
-- Migration: 0008_google_identity.sql
-- Additive migration: Google Identity subject support and signup grant abuse tracking
-- Non-destructive: no drops, no alters on existing data

ALTER TABLE users ADD COLUMN google_sub TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_google_sub ON users(google_sub);

-- Signup grants ledger to enforce once-per-identity free credit policies
CREATE TABLE IF NOT EXISTS signup_grants (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    google_sub TEXT,
    email TEXT,
    ip_hash TEXT,
    device_hash TEXT,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_signup_grants_sub ON signup_grants(google_sub);
CREATE INDEX IF NOT EXISTS idx_signup_grants_email ON signup_grants(email);
CREATE INDEX IF NOT EXISTS idx_signup_grants_ip ON signup_grants(ip_hash);
CREATE INDEX IF NOT EXISTS idx_signup_grants_device ON signup_grants(device_hash);
