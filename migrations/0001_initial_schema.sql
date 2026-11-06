-- NUMEROS VISION: CLOUDFLARE D1 DATABASE SCHEMA
-- Migration: 0001_initial_schema.sql
-- All monetary amounts stored as integer paise (INR * 100).
-- Deterministic identity: subjects unique per (user_id, dob_hash).

PRAGMA foreign_keys = ON;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    email TEXT,
    phone_hash TEXT,
    phone_enc TEXT,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_users_phone_hash ON users(phone_hash);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- 2. Subjects Table (Unique on user_id + dob_hash)
CREATE TABLE IF NOT EXISTS subjects (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    dob_hash TEXT NOT NULL,
    dob_enc TEXT NOT NULL,
    gender TEXT,
    birth_time_enc TEXT,
    birth_place_enc TEXT,
    time_confidence TEXT,
    created_at INTEGER NOT NULL,
    UNIQUE(user_id, dob_hash)
);
CREATE INDEX IF NOT EXISTS idx_subjects_user ON subjects(user_id);

-- 3. Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    subject_id TEXT REFERENCES subjects(id),
    pack_id TEXT NOT NULL,
    amount_paise INTEGER NOT NULL,
    currency TEXT NOT NULL DEFAULT 'INR',
    rzp_order_id TEXT UNIQUE,
    status TEXT NOT NULL DEFAULT 'CREATED', -- CREATED, PAID, FAILED, REFUNDED
    created_at INTEGER NOT NULL,
    updated_at INTEGER
);
CREATE INDEX IF NOT EXISTS idx_orders_user ON orders(user_id);
CREATE INDEX IF NOT EXISTS idx_orders_rzp_order ON orders(rzp_order_id);

-- 4. Payments Table
CREATE TABLE IF NOT EXISTS payments (
    id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL REFERENCES orders(id),
    rzp_payment_id TEXT UNIQUE NOT NULL,
    amount_paise INTEGER NOT NULL,
    status TEXT NOT NULL, -- CAPTURED, FAILED, REFUNDED
    method TEXT,
    captured_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_payments_order ON payments(order_id);
CREATE INDEX IF NOT EXISTS idx_payments_rzp_payment ON payments(rzp_payment_id);

-- 5. Webhook Events Table (event_id primary key for idempotency)
CREATE TABLE IF NOT EXISTS webhook_events (
    event_id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    received_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_webhook_events_type ON webhook_events(type);

-- 6. Entitlements Table (unique on user_id, subject_id, pack_id)
CREATE TABLE IF NOT EXISTS entitlements (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    subject_id TEXT NOT NULL REFERENCES subjects(id),
    pack_id TEXT NOT NULL,
    order_id TEXT REFERENCES orders(id),
    granted_at INTEGER NOT NULL,
    UNIQUE(user_id, subject_id, pack_id)
);
CREATE INDEX IF NOT EXISTS idx_entitlements_lookup ON entitlements(user_id, subject_id);

-- 7. Voucher Ledger Table (Bundles redeemed as report vouchers against subject DOB)
CREATE TABLE IF NOT EXISTS voucher_ledger (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    order_id TEXT NOT NULL REFERENCES orders(id),
    voucher_type TEXT NOT NULL, -- basic_voucher, advanced_voucher
    status TEXT NOT NULL DEFAULT 'ACTIVE', -- ACTIVE, REDEEMED, EXPIRED
    redeemed_subject_id TEXT REFERENCES subjects(id),
    created_at INTEGER NOT NULL,
    redeemed_at INTEGER
);
CREATE INDEX IF NOT EXISTS idx_vouchers_user ON voucher_ledger(user_id, status);

-- 8. Credit Ledger Table (Charm AI queries, balances, and refunds)
CREATE TABLE IF NOT EXISTS credit_ledger (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    delta INTEGER NOT NULL,
    reason TEXT NOT NULL, -- signup_bonus, pack_purchase, question_asked, query_refund
    ref_id TEXT UNIQUE,
    balance_after INTEGER NOT NULL,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_credit_ledger_user ON credit_ledger(user_id);

-- 9. Report Jobs Table (PDF generation pipeline)
CREATE TABLE IF NOT EXISTS report_jobs (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    subject_id TEXT NOT NULL REFERENCES subjects(id),
    pack_id TEXT NOT NULL,
    order_id TEXT REFERENCES orders(id),
    status TEXT NOT NULL DEFAULT 'QUEUED', -- QUEUED, PROCESSING, COMPLETED, DOWNLOADED, FAILED, CANCELLED
    r2_key TEXT,
    created_at INTEGER NOT NULL,
    completed_at INTEGER
);
CREATE INDEX IF NOT EXISTS idx_report_jobs_user ON report_jobs(user_id, subject_id);

-- 10. Consents Table (DPDP 2023 statutory consent ledger)
CREATE TABLE IF NOT EXISTS consents (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    purpose TEXT NOT NULL, -- terms_dpdp, privacy_policy, report_processing
    text_version TEXT NOT NULL,
    granted_at INTEGER NOT NULL,
    withdrawn_at INTEGER
);
CREATE INDEX IF NOT EXISTS idx_consents_user ON consents(user_id);

-- 11. OTP Challenges Table (HMAC hashed OTP, expiry, attempt counter)
CREATE TABLE IF NOT EXISTS otp_challenges (
    id TEXT PRIMARY KEY,
    phone_hash TEXT NOT NULL,
    code_hash TEXT NOT NULL,
    attempts INTEGER NOT NULL DEFAULT 0,
    max_attempts INTEGER NOT NULL DEFAULT 5,
    expires_at INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    ip_hash TEXT
);
CREATE INDEX IF NOT EXISTS idx_otp_phone ON otp_challenges(phone_hash);

-- 12. Sessions Table (Server-side session management with HttpOnly cookies)
CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    token_hash TEXT UNIQUE NOT NULL,
    expires_at INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    ip_hash TEXT,
    user_agent TEXT
);
CREATE INDEX IF NOT EXISTS idx_sessions_token ON sessions(token_hash);
