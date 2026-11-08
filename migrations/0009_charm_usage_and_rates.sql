-- NUMEROS VISION: CLOUDFLARE D1 DATABASE SCHEMA
-- Migration: 0009_charm_usage_and_rates.sql
-- Server-side gating, lifetime free allowance tracking, and durable rate limits for Charm AI.
-- Non-destructive: no drops, no alters on existing tables.

-- 1. Free Chat Allowance Tracking (Strict total of 3 per person)
CREATE TABLE IF NOT EXISTS free_chat_usage (
    id TEXT PRIMARY KEY,
    visitor_hash TEXT UNIQUE NOT NULL,
    user_id TEXT,
    questions_used INTEGER NOT NULL DEFAULT 0,
    max_free INTEGER NOT NULL DEFAULT 3,
    ip_hash TEXT,
    created_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_free_chat_visitor ON free_chat_usage(visitor_hash);
CREATE INDEX IF NOT EXISTS idx_free_chat_user ON free_chat_usage(user_id);

-- 2. Durable Rate Limits & Spend Caps (Cross-Isolate Protection)
CREATE TABLE IF NOT EXISTS charm_rate_limits (
    key TEXT PRIMARY KEY,
    count INTEGER NOT NULL DEFAULT 0,
    window_start INTEGER NOT NULL,
    expires_at INTEGER NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_charm_rate_limits_exp ON charm_rate_limits(expires_at);
