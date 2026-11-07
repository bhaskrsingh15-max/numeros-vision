-- 0006_events.sql
-- Server-side operational telemetry and journey events
-- Strict Zero-PII schema: no names, emails, phones, dates of birth, or astrological vectors.
-- Data Retention: 90-day rolling window for aggregated funnel optimization. Events older than 90 days are purged opportunistically on write.

CREATE TABLE IF NOT EXISTS events (
    id TEXT PRIMARY KEY,
    event_name TEXT NOT NULL,
    device_id TEXT,
    anonymous_session_id TEXT,
    page_path TEXT,
    product_id TEXT,
    value_inr REAL DEFAULT 0.0,
    currency TEXT DEFAULT 'INR',
    utm_source TEXT,
    utm_medium TEXT,
    utm_campaign TEXT,
    meta_json TEXT,
    ip_hash TEXT,
    user_agent TEXT,
    created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_events_name ON events(event_name);
CREATE INDEX IF NOT EXISTS idx_events_device ON events(device_id);
CREATE INDEX IF NOT EXISTS idx_events_created ON events(created_at);
