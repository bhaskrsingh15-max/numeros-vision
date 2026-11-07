-- 0004_cookie_consents.sql
-- Server-side consent ledger for pseudonymous visitors and authenticated users

CREATE TABLE IF NOT EXISTS cookie_consents (
    id TEXT PRIMARY KEY,
    user_id TEXT,
    pseudonymous_id TEXT,
    consent_state TEXT NOT NULL,
    policy_version TEXT NOT NULL,
    user_agent TEXT,
    ip_hash TEXT,
    created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_cookie_consents_uid ON cookie_consents(user_id);
CREATE INDEX IF NOT EXISTS idx_cookie_consents_pseudo ON cookie_consents(pseudonymous_id);
