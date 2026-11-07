-- 0007_schema_alignment.sql
-- Align cookie_consents, enquiries, and events schemas and indexes
-- Recreates cookie_consents with full application schema (consent toggles and versions)

DROP TABLE IF EXISTS cookie_consents;

CREATE TABLE IF NOT EXISTS cookie_consents (
    id TEXT PRIMARY KEY,
    pseudonymous_id TEXT NOT NULL,
    user_id TEXT REFERENCES users(id),
    essential_granted INTEGER NOT NULL DEFAULT 1,
    analytics_granted INTEGER NOT NULL DEFAULT 0,
    marketing_granted INTEGER NOT NULL DEFAULT 0,
    choices_json TEXT NOT NULL DEFAULT '{}',
    banner_version TEXT NOT NULL DEFAULT '1.0',
    ip_hash TEXT,
    user_agent TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_cookie_consents_pseudo ON cookie_consents(pseudonymous_id);
CREATE INDEX IF NOT EXISTS idx_cookie_consents_user ON cookie_consents(user_id);

-- Enquiries index alignment for notification filtering
CREATE INDEX IF NOT EXISTS idx_enquiries_status ON enquiries(notification_status);

-- Events index alignment for 90-day retention query optimization
CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at);
