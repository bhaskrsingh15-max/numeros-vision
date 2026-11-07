-- 0004_cookie_consents.sql
-- Server-side statutory consent ledger for pseudonymous visitors and authenticated users (DPDP Act 2023 & GDPR)

CREATE TABLE IF NOT EXISTS cookie_consents (
    id TEXT PRIMARY KEY,
    pseudonymous_id TEXT NOT NULL,
    user_id TEXT REFERENCES users(id),
    essential_granted INTEGER NOT NULL DEFAULT 1,
    analytics_granted INTEGER NOT NULL DEFAULT 0,
    marketing_granted INTEGER NOT NULL DEFAULT 0,
    choices_json TEXT NOT NULL,
    banner_version TEXT NOT NULL,
    ip_hash TEXT,
    user_agent TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_cookie_consents_pseudo ON cookie_consents(pseudonymous_id);
CREATE INDEX IF NOT EXISTS idx_cookie_consents_user ON cookie_consents(user_id);
