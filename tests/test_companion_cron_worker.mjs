// Tests for Companion Scheduled Worker (`workers/reconcile_and_purge_cron.js`)
// Verifies:
//   1. Every-10-min (`*/10 * * * *`) Stale-Order Reconcile
//   2. Daily (`15 2 * * *`) 30-Day Retention Job (disabled flag, report_only default, scoped delete)

import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import cronWorker, {
  runStaleOrderReconcile,
  runRetentionPurge30d,
} from '../workers/reconcile_and_purge_cron.js';

function createSqliteD1Adapter() {
  const sqlite = new DatabaseSync(':memory:');
  const migrations = [
    '0001_initial_schema.sql',
    '0002_invoices_refunds_audit.sql',
    '0010_email_otp_and_consents.sql',
  ];
  for (const file of migrations) {
    const sql = fs.readFileSync(path.join(process.cwd(), 'migrations', file), 'utf8');
    sqlite.exec(sql);
  }

  function makeStmt(sql, bound = []) {
    return {
      bind(...args) {
        return makeStmt(sql, args);
      },
      async first() {
        const stmt = sqlite.prepare(sql);
        const row = stmt.get(...bound);
        return row === undefined ? null : row;
      },
      async all() {
        const stmt = sqlite.prepare(sql);
        const rows = stmt.all(...bound);
        return { results: rows };
      },
      async run() {
        const stmt = sqlite.prepare(sql);
        const info = stmt.run(...bound);
        return { success: true, meta: { changes: Number(info.changes || 0) } };
      },
    };
  }

  return {
    sqlite,
    d1: {
      prepare(sql) {
        return makeStmt(sql, []);
      },
    },
  };
}

async function runTests() {
  const nowMs = Date.UTC(2026, 10, 12, 12, 0, 0); // 2026-11-12T12:00:00Z
  const { sqlite, d1 } = createSqliteD1Adapter();

  // Seed 2 users and 2 subjects (MUST NEVER BE DELETED)
  sqlite
    .prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)')
    .run('usr_paid', 'paid@example.com', nowMs - 45 * 86_400_000);
  sqlite
    .prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)')
    .run('usr_abandoned', 'abandoned@example.com', nowMs - 45 * 86_400_000);

  sqlite
    .prepare(
      'INSERT INTO subjects (id, user_id, name, dob_hash, dob_enc, gender, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
    )
    .run('sub_1', 'usr_paid', 'Customer One', 'hash1', 'enc1', 'M', nowMs - 45 * 86_400_000);
  sqlite
    .prepare(
      'INSERT INTO subjects (id, user_id, name, dob_hash, dob_enc, gender, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
    )
    .run('sub_2', 'usr_abandoned', 'Customer Two', 'hash2', 'enc2', 'F', nowMs - 45 * 86_400_000);

  // Order A: Stale paid-at-gateway order (25 min old, CREATED, rzp_order_captured)
  sqlite
    .prepare(
      `INSERT INTO orders (id, user_id, subject_id, pack_id, amount_paise, currency, rzp_order_id, status, created_at)
       VALUES (?, ?, ?, ?, ?, 'INR', ?, 'CREATED', ?)`
    )
    .run('ord_stale_captured', 'usr_paid', 'sub_1', 'report_basic', 39900, 'order_rzp_captured_1', nowMs - 25 * 60_000);

  // Order B: Stale authorized-but-uncaptured order (30 min old)
  sqlite
    .prepare(
      `INSERT INTO orders (id, user_id, subject_id, pack_id, amount_paise, currency, rzp_order_id, status, created_at)
       VALUES (?, ?, ?, ?, ?, 'INR', ?, 'CREATED', ?)`
    )
    .run('ord_stale_auth_only', 'usr_paid', 'sub_1', 'report_basic', 39900, 'order_rzp_auth_only', nowMs - 30 * 60_000);

  // Order C: Fresh order (<10 min old — must be ignored by cron)
  sqlite
    .prepare(
      `INSERT INTO orders (id, user_id, subject_id, pack_id, amount_paise, currency, rzp_order_id, status, created_at)
       VALUES (?, ?, ?, ?, ?, 'INR', ?, 'CREATED', ?)`
    )
    .run('ord_fresh', 'usr_paid', 'sub_1', 'report_basic', 39900, 'order_rzp_fresh', nowMs - 3 * 60_000);

  // Order D: 35-day-old abandoned unpaid order (eligible for 30d purge)
  sqlite
    .prepare(
      `INSERT INTO orders (id, user_id, subject_id, pack_id, amount_paise, currency, rzp_order_id, status, created_at)
       VALUES (?, ?, ?, ?, ?, 'INR', ?, 'CREATED', ?)`
    )
    .run('ord_abandoned_35d', 'usr_abandoned', 'sub_2', 'report_basic', 39900, 'order_rzp_old_unpaid', nowMs - 35 * 86_400_000);

  // Order E: 40-day-old PAID order (MUST NEVER be purged!)
  sqlite
    .prepare(
      `INSERT INTO orders (id, user_id, subject_id, pack_id, amount_paise, currency, rzp_order_id, status, created_at)
       VALUES (?, ?, ?, ?, ?, 'INR', ?, 'PAID', ?)`
    )
    .run('ord_paid_40d', 'usr_paid', 'sub_1', 'report_basic', 39900, 'order_rzp_old_paid', nowMs - 40 * 86_400_000);

  // Seed OTPs & sessions (expired + active)
  sqlite
    .prepare(
      'INSERT INTO email_otp_challenges (id, email_hash, code_hash, expires_at, created_at, ip_hash) VALUES (?, ?, ?, ?, ?, ?)'
    )
    .run('eotp_exp_1', 'eh1', 'ch1', nowMs - 60_000, nowMs - 660_000, 'ip1');
  sqlite
    .prepare(
      'INSERT INTO email_otp_challenges (id, email_hash, code_hash, expires_at, created_at, ip_hash) VALUES (?, ?, ?, ?, ?, ?)'
    )
    .run('eotp_active_1', 'eh2', 'ch2', nowMs + 300_000, nowMs - 60_000, 'ip2');

  sqlite
    .prepare(
      'INSERT INTO otp_challenges (id, phone_hash, code_hash, expires_at, created_at, ip_hash) VALUES (?, ?, ?, ?, ?, ?)'
    )
    .run('potp_exp_1', 'ph1', 'ch1', nowMs - 120_000, nowMs - 720_000, 'ip1');

  sqlite
    .prepare(
      'INSERT INTO sessions (id, user_id, token_hash, expires_at, created_at) VALUES (?, ?, ?, ?, ?)'
    )
    .run('sess_exp_1', 'usr_abandoned', 'tok_exp', nowMs - 10_000, nowMs - 86_400_000);
  sqlite
    .prepare(
      'INSERT INTO sessions (id, user_id, token_hash, expires_at, created_at) VALUES (?, ?, ?, ?, ?)'
    )
    .run('sess_active_1', 'usr_paid', 'tok_active', nowMs + 86_400_000, nowMs - 1_000);

  // ── 1. Preview safety guard: reject rzp_live_ key in preview ──
  const liveKeyBlocked = await runStaleOrderReconcile(
    {
      DB: d1,
      ENVIRONMENT: 'preview',
      RAZORPAY_KEY_ID: 'rzp_live_should_not_run',
      RAZORPAY_KEY_SECRET: 'sec_dummy',
    },
    nowMs,
    async () => {
      throw new Error('Should never fetch Razorpay with live key in preview');
    }
  );
  assert.equal(liveKeyBlocked.skipped, true);
  assert.equal(liveKeyBlocked.reason, 'preview_requires_test_razorpay_key');

  // ── 2. Stale-order reconcile with mocked Razorpay API ──
  const mockRazorpayFetch = async (url) => {
    if (String(url).includes('order_rzp_captured_1')) {
      return new Response(
        JSON.stringify({
          items: [
            {
              id: 'pay_captured_001',
              status: 'captured',
              captured: true,
              amount: 39900,
              currency: 'INR',
              method: 'upi',
            },
          ],
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      );
    }
    if (String(url).includes('order_rzp_auth_only')) {
      return new Response(
        JSON.stringify({
          items: [
            {
              id: 'pay_auth_only_002',
              status: 'authorized',
              captured: false,
              amount: 39900,
              currency: 'INR',
              method: 'card',
            },
          ],
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      );
    }
    throw new Error(`Unexpected Razorpay URL: ${url}`);
  };

  const envPreview = {
    DB: d1,
    ENVIRONMENT: 'preview',
    RAZORPAY_KEY_ID: 'rzp_test_preview_key',
    RAZORPAY_KEY_SECRET: 'test_secret_placeholder',
    ENABLE_RETENTION_PURGE_30D: 'false',
    RETENTION_PURGE_MODE: 'report_only',
  };

  const rec1 = await runStaleOrderReconcile(envPreview, nowMs, mockRazorpayFetch);
  assert.equal(rec1.scanned, 2, 'Should scan only the 2 stale orders between 10m and 7d old');
  assert.equal(rec1.reconciled, 1);
  assert.deepEqual(rec1.reconciledOrderIds, ['ord_stale_captured']);
  assert.equal(rec1.uncapturedAuthorized, 1);

  // Verify Order A is PAID, entitled, and has exactly 1 report_job; Order B is still CREATED
  const ordA = sqlite.prepare('SELECT status FROM orders WHERE id = ?').get('ord_stale_captured');
  const ordB = sqlite.prepare('SELECT status FROM orders WHERE id = ?').get('ord_stale_auth_only');
  assert.equal(ordA.status, 'PAID');
  assert.equal(ordB.status, 'CREATED');

  const jobCount1 = sqlite
    .prepare('SELECT COUNT(*) AS cnt FROM report_jobs WHERE order_id = ?')
    .get('ord_stale_captured').cnt;
  assert.equal(jobCount1, 1);

  // Re-running reconcile is idempotent (order is now PAID so scanned drops to 1)
  const rec2 = await runStaleOrderReconcile(envPreview, nowMs, mockRazorpayFetch);
  assert.equal(rec2.scanned, 1);
  assert.equal(rec2.reconciled, 0);

  // ── 3. Retention Purge: Disabled by default (`ENABLE_RETENTION_PURGE_30D = "false"`) ──
  const purgeDisabled = await runRetentionPurge30d(envPreview, nowMs);
  assert.equal(purgeDisabled.enabled, false);
  assert.equal(purgeDisabled.skipped, true);
  assert.equal(purgeDisabled.reason, 'ENABLE_RETENTION_PURGE_30D_DISABLED');

  // ── 4. Retention Purge: Enabled in default `report_only` mode (counts only, ZERO deletes!) ──
  const purgeReportOnly = await runRetentionPurge30d(
    {
      ...envPreview,
      ENABLE_RETENTION_PURGE_30D: 'true',
      // RETENTION_PURGE_MODE intentionally omitted to prove default is report_only
    },
    nowMs
  );
  assert.equal(purgeReportOnly.enabled, true);
  assert.equal(purgeReportOnly.mode, 'report_only');
  assert.deepEqual(purgeReportOnly.candidates, {
    email_otp_challenges: 1,
    otp_challenges: 1,
    sessions: 1,
    abandoned_orders: 1,
  });
  assert.deepEqual(purgeReportOnly.deleted, {
    email_otp_challenges: 0,
    otp_challenges: 0,
    sessions: 0,
    abandoned_orders: 0,
  });

  // Verify ZERO rows were deleted in report_only mode
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS c FROM email_otp_challenges').get().c, 2);
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS c FROM otp_challenges').get().c, 1);
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS c FROM sessions').get().c, 2);
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS c FROM orders').get().c, 5);

  // ── 5. Retention Purge: Explicit `delete` mode removes ONLY scoped expired/abandoned rows ──
  const purgeDelete = await runRetentionPurge30d(
    {
      ...envPreview,
      ENABLE_RETENTION_PURGE_30D: 'true',
      RETENTION_PURGE_MODE: 'delete',
    },
    nowMs
  );
  assert.equal(purgeDelete.mode, 'delete');
  assert.deepEqual(purgeDelete.deleted, {
    email_otp_challenges: 1,
    otp_challenges: 1,
    sessions: 1,
    abandoned_orders: 1,
  });

  // Active OTP, active session, fresh/paid orders, AND 100% of users + subjects remain intact!
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS c FROM users').get().c, 2, 'Users must NEVER be deleted');
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS c FROM subjects').get().c, 2, 'Subjects must NEVER be deleted');
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS c FROM email_otp_challenges').get().c, 1);
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS c FROM otp_challenges').get().c, 0);
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS c FROM sessions').get().c, 1);
  assert.equal(sqlite.prepare('SELECT COUNT(*) AS c FROM orders').get().c, 4);
  assert.equal(
    sqlite.prepare('SELECT COUNT(*) AS c FROM orders WHERE id = ?').get('ord_paid_40d').c,
    1,
    'Paid historical orders must NEVER be deleted'
  );

  // ── 6. Worker `/health` endpoint returns non-secret config status + noindex ──
  const healthResp = await cronWorker.fetch(new Request('https://cron.internal/health'), envPreview);
  assert.equal(healthResp.status, 200);
  assert.match(healthResp.headers.get('X-Robots-Tag') || '', /noindex/);
  const healthBody = await healthResp.json();
  assert.equal(healthBody.ok, true);
  assert.equal(healthBody.retention_purge_30d_enabled, false);
  assert.equal(healthBody.retention_purge_mode, 'report_only');

  console.log('ALL COMPANION CRON WORKER TESTS PASSED (6/6 assertions green)');
}

runTests().catch((err) => {
  console.error(err);
  process.exit(1);
});
