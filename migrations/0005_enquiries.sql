-- 0005_enquiries.sql
-- Durable storage for contact inquiries and 1-on-1 consultation requests

CREATE TABLE IF NOT EXISTS enquiries (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL, -- 'contact' or 'consultation'
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    area_or_category TEXT,
    preferred_contact_method TEXT,
    order_id TEXT,
    message TEXT,
    notification_status TEXT NOT NULL DEFAULT 'notify_failed', -- 'notified' or 'notify_failed'
    ip_hash TEXT,
    user_agent TEXT,
    created_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_enquiries_type ON enquiries(type);
CREATE INDEX IF NOT EXISTS idx_enquiries_email ON enquiries(email);
CREATE INDEX IF NOT EXISTS idx_enquiries_status ON enquiries(notification_status);
CREATE INDEX IF NOT EXISTS idx_enquiries_created ON enquiries(created_at);
