-- NUMEROS VISION: CLOUDFLARE D1 DATABASE SCHEMA
-- Migration: 0008_planner_2027_orders.sql
-- Dedicated ledger for 2027 Year Ahead Planner orders, verification, and private delivery.
-- Non-destructive: no drops, no alters on existing data.
-- STORES STRICTLY ZERO CARD OR FINANCIAL INSTRUMENT DATA.

CREATE TABLE IF NOT EXISTS planner_2027_orders (
    id TEXT PRIMARY KEY,
    razorpay_order_id TEXT UNIQUE NOT NULL,
    razorpay_payment_id TEXT,
    status TEXT NOT NULL DEFAULT 'created' CHECK (status IN ('created', 'paid', 'generating', 'delivered', 'needs_attention', 'refunded')),
    amount_paise INTEGER NOT NULL,
    currency TEXT NOT NULL DEFAULT 'INR',
    name_normalised TEXT NOT NULL,
    dob TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT,
    consent_version TEXT NOT NULL,
    consent_at INTEGER NOT NULL,
    download_token_hash TEXT,
    token_expires_at INTEGER,
    generation_count INTEGER NOT NULL DEFAULT 0,
    pdf_r2_key TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_planner_orders_rzp_order ON planner_2027_orders(razorpay_order_id);
CREATE INDEX IF NOT EXISTS idx_planner_orders_token_hash ON planner_2027_orders(download_token_hash);
CREATE INDEX IF NOT EXISTS idx_planner_orders_status ON planner_2027_orders(status);
