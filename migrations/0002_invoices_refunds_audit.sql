-- NUMEROS VISION: CLOUDFLARE D1 DATABASE SCHEMA
-- Migration: 0002_invoices_refunds_audit.sql
-- Enforces: Sequential invoices, GSTIN & tax fields, refunds, tamper-evident audit log,
-- Charm AI answer caching & report walkthrough insights,
-- and strict unique constraints on orders.rzp_order_id, users.email, and users.phone_hash.

PRAGMA foreign_keys = ON;

-- 1. Invoices Table (Sequential tax invoice record)
CREATE TABLE IF NOT EXISTS invoices (
    id TEXT PRIMARY KEY,
    order_id TEXT NOT NULL REFERENCES orders(id),
    user_id TEXT NOT NULL REFERENCES users(id),
    invoice_number TEXT UNIQUE NOT NULL, -- e.g. NV-INV-2026-00001
    amount_paise INTEGER NOT NULL,
    tax_paise INTEGER DEFAULT 0,
    gstin TEXT,
    billing_name TEXT NOT NULL,
    billing_email TEXT,
    billing_phone TEXT,
    billing_address TEXT,
    currency TEXT NOT NULL DEFAULT 'INR',
    status TEXT NOT NULL DEFAULT 'ISSUED', -- ISSUED, VOID, REFUNDED
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_invoices_order ON invoices(order_id);
CREATE INDEX IF NOT EXISTS idx_invoices_user ON invoices(user_id);
CREATE INDEX IF NOT EXISTS idx_invoices_number ON invoices(invoice_number);

-- 2. Refunds Table
CREATE TABLE IF NOT EXISTS refunds (
    id TEXT PRIMARY KEY,
    payment_id TEXT NOT NULL REFERENCES payments(id),
    order_id TEXT NOT NULL REFERENCES orders(id),
    user_id TEXT NOT NULL REFERENCES users(id),
    rzp_refund_id TEXT UNIQUE,
    amount_paise INTEGER NOT NULL,
    reason TEXT,
    status TEXT NOT NULL DEFAULT 'PENDING', -- PENDING, PROCESSED, FAILED
    created_at INTEGER NOT NULL,
    processed_at INTEGER
);
CREATE INDEX IF NOT EXISTS idx_refunds_payment ON refunds(payment_id);
CREATE INDEX IF NOT EXISTS idx_refunds_order ON refunds(order_id);
CREATE INDEX IF NOT EXISTS idx_refunds_user ON refunds(user_id);

-- 3. Audit Log Table (Tamper-evident system activity ledger)
CREATE TABLE IF NOT EXISTS audit_log (
    id TEXT PRIMARY KEY,
    actor_id TEXT NOT NULL, -- user_id or 'system' / 'webhook'
    action TEXT NOT NULL, -- order.created, payment.captured, entitlement.granted, etc.
    resource_type TEXT NOT NULL, -- orders, payments, entitlements, sessions
    resource_id TEXT NOT NULL,
    details_json TEXT,
    ip_hash TEXT,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_audit_actor ON audit_log(actor_id);
CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_log(action);
CREATE INDEX IF NOT EXISTS idx_audit_resource ON audit_log(resource_type, resource_id);

-- 4. Charm AI Answers Table (Cached answers, credit accounting & rule provenance)
CREATE TABLE IF NOT EXISTS charm_answers (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    subject_id TEXT NOT NULL REFERENCES subjects(id),
    question_key TEXT NOT NULL, -- predefined questionId or text_hash
    question_text TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    mode TEXT NOT NULL, -- 'predefined' or 'free_text'
    credits_spent INTEGER NOT NULL DEFAULT 1,
    rule_ids TEXT NOT NULL, -- JSON array of rule IDs used, e.g. '["RULE_001"]'
    label TEXT NOT NULL, -- 'Calculated', 'Traditional', or 'Interpretive'
    engine_version TEXT NOT NULL,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_charm_user ON charm_answers(user_id, subject_id);
CREATE INDEX IF NOT EXISTS idx_charm_cache ON charm_answers(subject_id, question_key, engine_version);

-- 5. Report Insights Table (Cached automatic walkthrough per paid report, zero credit cost)
CREATE TABLE IF NOT EXISTS report_insights (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    subject_id TEXT NOT NULL REFERENCES subjects(id),
    pack_id TEXT NOT NULL,
    walkthrough_json TEXT NOT NULL,
    created_at INTEGER NOT NULL,
    UNIQUE(user_id, subject_id, pack_id)
);
CREATE INDEX IF NOT EXISTS idx_report_insights_lookup ON report_insights(user_id, subject_id);

-- 6. Unique Constraints Confirmation & Enforcement
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email_unique ON users(email) WHERE email IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_phone_hash_unique ON users(phone_hash) WHERE phone_hash IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS idx_orders_rzp_order_unique ON orders(rzp_order_id) WHERE rzp_order_id IS NOT NULL;
