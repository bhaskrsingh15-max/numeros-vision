-- ============================================================
-- Numeros Vision — PostgreSQL Schema v1.0
-- Phase 3: Replace flat JSONL stores with proper relational DB
-- Compatible with: Supabase, Neon, Railway, AWS RDS PostgreSQL
-- ============================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ── USERS ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS users (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email           TEXT UNIQUE,
    name            TEXT,
    whatsapp        TEXT,                           -- optional, user-provided
    plan            TEXT NOT NULL DEFAULT 'free',  -- free | premium | elite
    plan_expires_at TIMESTAMPTZ,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_plan  ON users(plan);

-- ── BIRTH PROFILES ──────────────────────────────────────────
-- One profile per user (upserted when they save birth details)
CREATE TABLE IF NOT EXISTS birth_profiles (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID REFERENCES users(id) ON DELETE CASCADE,
    premium_token   TEXT UNIQUE,                    -- SHA256 token for token-only auth
    full_name       TEXT,
    birth_day       SMALLINT CHECK (birth_day BETWEEN 1 AND 31),
    birth_month     SMALLINT CHECK (birth_month BETWEEN 1 AND 12),
    birth_year      SMALLINT CHECK (birth_year BETWEEN 1900 AND 2100),
    birth_time      TEXT,                           -- HH:MM, nullable
    birth_city      TEXT,
    current_city    TEXT,
    -- Calculated fields (cached on save, recalc on profile update)
    life_path       SMALLINT,
    psychic_number  SMALLINT,
    destiny_number  SMALLINT,
    name_chaldean   SMALLINT,
    personal_year   SMALLINT,
    -- Questionnaire answers (JSONB for flexibility)
    questionnaire   JSONB DEFAULT '{}'::JSONB,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_bp_user_id       ON birth_profiles(user_id);
CREATE INDEX idx_bp_premium_token ON birth_profiles(premium_token);

-- ── PAYMENTS ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS payments (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id             UUID REFERENCES users(id) ON DELETE SET NULL,
    premium_token       TEXT UNIQUE NOT NULL,
    razorpay_order_id   TEXT UNIQUE,
    razorpay_payment_id TEXT UNIQUE,
    razorpay_signature  TEXT,
    plan                TEXT NOT NULL,              -- premium | elite | phone_consult | video_consult
    amount_inr          INTEGER NOT NULL,
    currency            TEXT NOT NULL DEFAULT 'INR',
    status              TEXT NOT NULL DEFAULT 'created', -- created | verified | failed | refunded
    email               TEXT,
    name                TEXT,
    verified_at         TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_payments_token      ON payments(premium_token);
CREATE INDEX idx_payments_order_id   ON payments(razorpay_order_id);
CREATE INDEX idx_payments_payment_id ON payments(razorpay_payment_id);
CREATE INDEX idx_payments_status     ON payments(status);
CREATE INDEX idx_payments_plan       ON payments(plan);

-- ── CONSULTATIONS / BOOKINGS ────────────────────────────────
CREATE TABLE IF NOT EXISTS bookings (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id         UUID REFERENCES users(id) ON DELETE SET NULL,
    booking_type    TEXT NOT NULL,                  -- phone | video
    amount_inr      INTEGER NOT NULL,
    name            TEXT NOT NULL,
    whatsapp        TEXT NOT NULL,
    preferred_date  TEXT,
    preferred_time  TEXT,
    notes           TEXT,
    status          TEXT NOT NULL DEFAULT 'pending', -- pending | confirmed | completed | cancelled
    payment_id      UUID REFERENCES payments(id) ON DELETE SET NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_type   ON bookings(booking_type);

-- ── CHAT CONVERSATIONS ──────────────────────────────────────
CREATE TABLE IF NOT EXISTS conversations (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    profile_id      UUID REFERENCES birth_profiles(id) ON DELETE CASCADE,
    premium_token   TEXT,                           -- for anonymous premium sessions
    session_id      TEXT,                           -- client-side session
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_conv_profile   ON conversations(profile_id);
CREATE INDEX idx_conv_token     ON conversations(premium_token);
CREATE INDEX idx_conv_session   ON conversations(session_id);

-- ── CHAT MESSAGES ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS messages (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    role            TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content         TEXT NOT NULL,
    -- Metadata (optional, for analytics)
    engine_used     JSONB,                          -- which internal engines contributed (NEVER exposed to frontend)
    rag_passages    INTEGER,                        -- number of RAG passages retrieved
    latency_ms      INTEGER,
    is_premium      BOOLEAN DEFAULT FALSE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_msg_conversation ON messages(conversation_id);
CREATE INDEX idx_msg_role         ON messages(role);
CREATE INDEX idx_msg_created      ON messages(created_at DESC);

-- ── B2B API KEYS ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS api_keys (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    key_hash        TEXT UNIQUE NOT NULL,           -- SHA256(api_key) — never store plaintext
    client_name     TEXT NOT NULL,
    tier            TEXT NOT NULL DEFAULT 'basic', -- basic | standard | enterprise
    monthly_quota   INTEGER NOT NULL DEFAULT 1000,
    used_this_month INTEGER NOT NULL DEFAULT 0,
    quota_reset_at  TIMESTAMPTZ NOT NULL DEFAULT (DATE_TRUNC('month', NOW()) + INTERVAL '1 month'),
    active          BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_used_at    TIMESTAMPTZ
);
CREATE INDEX idx_apikeys_hash   ON api_keys(key_hash);
CREATE INDEX idx_apikeys_active ON api_keys(active);

-- ── B2B API USAGE LOG ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS api_usage (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    api_key_id  UUID REFERENCES api_keys(id) ON DELETE CASCADE,
    endpoint    TEXT NOT NULL,
    status_code SMALLINT,
    latency_ms  INTEGER,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_usage_key     ON api_usage(api_key_id);
CREATE INDEX idx_usage_created ON api_usage(created_at DESC);

-- ── TRIGGERS: auto-update updated_at ─────────────────────────
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN NEW.updated_at = NOW(); RETURN NEW; END;
$$ LANGUAGE plpgsql;

DO $$ DECLARE t TEXT;
BEGIN
  FOR t IN SELECT unnest(ARRAY['users','birth_profiles','bookings'])
  LOOP
    EXECUTE format('DROP TRIGGER IF EXISTS trg_%s_updated_at ON %s', t, t);
    EXECUTE format('CREATE TRIGGER trg_%s_updated_at BEFORE UPDATE ON %s FOR EACH ROW EXECUTE FUNCTION set_updated_at()', t, t);
  END LOOP;
END $$;

-- ── VIEWS: handy aggregates ───────────────────────────────────

-- Revenue by plan
CREATE OR REPLACE VIEW v_revenue_by_plan AS
SELECT
    plan,
    COUNT(*)                    AS total_payments,
    SUM(amount_inr)             AS total_inr,
    AVG(amount_inr)::INTEGER    AS avg_inr,
    DATE_TRUNC('month', created_at) AS month
FROM payments
WHERE status = 'verified'
GROUP BY plan, DATE_TRUNC('month', created_at)
ORDER BY month DESC, total_inr DESC;

-- Active premium users
CREATE OR REPLACE VIEW v_active_premium AS
SELECT
    u.id, u.email, u.name, u.plan, u.plan_expires_at,
    bp.life_path, bp.psychic_number, bp.current_city,
    p.amount_inr, p.verified_at
FROM users u
LEFT JOIN birth_profiles bp ON bp.user_id = u.id
LEFT JOIN payments p ON p.premium_token = bp.premium_token AND p.status = 'verified'
WHERE u.plan IN ('premium', 'elite')
ORDER BY u.plan_expires_at DESC;

-- Daily chat volume
CREATE OR REPLACE VIEW v_daily_chat_volume AS
SELECT
    DATE(created_at)        AS day,
    role,
    COUNT(*)                AS message_count,
    AVG(latency_ms)::INTEGER AS avg_latency_ms
FROM messages
GROUP BY DATE(created_at), role
ORDER BY day DESC;

-- ── SEED: default free user for testing ──────────────────────
-- (Remove before production)
INSERT INTO users (email, name, plan)
VALUES ('test@numerosvision.com', 'Test User', 'free')
ON CONFLICT (email) DO NOTHING;

-- ============================================================
-- MIGRATION NOTES
-- 1. Apply with: psql $DATABASE_URL -f schema.sql
-- 2. For Supabase: paste into SQL Editor and Run
-- 3. JSONL flat files in data/ can be migrated with the
--    migration script: python tools/migrate_jsonl_to_pg.py
-- 4. Set DATABASE_URL in .env — app/main.py reads it via
--    os.environ.get("DATABASE_URL")
-- ============================================================
