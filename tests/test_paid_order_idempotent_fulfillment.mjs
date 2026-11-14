import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import worker from '../app/static/_worker.js';
const { mintUserSession, getPackById, resolveServerLaunchOfferState } = worker;

// Mock environment for edge worker testing
function createMockEnv(overrides = {}) {
  const memoryDB = {
    orders: new Map(),
    report_jobs: new Map(),
    payments: new Map(),
    entitlements: new Map(),
    credit_ledger: new Map(),
    voucher_ledger: new Map(),
    audit_log: [],
    events: [],
    users: new Map(),
    subjects: new Map(),
    sessions: new Map(),
    emails_sent: []
  };

  const db = {
    prepare(query) {
      return {
        _query: query,
        _params: [],
        bind(...params) {
          this._params = params;
          return this;
        },
        async first() {
          const q = this._query;
          const p = this._params;
          if (q.includes('FROM report_jobs WHERE order_id = ?')) {
            const jobs = Array.from(memoryDB.report_jobs.values()).filter(j => j.order_id === p[0]);
            return jobs.length > 0 ? jobs[jobs.length - 1] : null;
          }
          if (q.includes("FROM audit_log WHERE resource_id = ? AND action = 'order_confirmation_email_sent'")) {
            const entry = memoryDB.audit_log.find(a => a.resource_id === p[0] && a.action === 'order_confirmation_email_sent');
            return entry || null;
          }
          if (q.includes("SELECT COUNT(*) as cnt FROM audit_log WHERE resource_id = ? AND action = 'order_confirmation_email_attempt'")) {
            const cnt = memoryDB.audit_log.filter(a => a.resource_id === p[0] && a.action === 'order_confirmation_email_attempt').length;
            return { cnt };
          }
          if (q.includes('FROM payments WHERE order_id = ?')) {
            const pmt = Array.from(memoryDB.payments.values()).find(pm => pm.order_id === p[0]);
            return pmt || null;
          }
          if (q.includes('FROM orders WHERE id = ?')) {
            return memoryDB.orders.get(p[0]) || null;
          }
          if (q.includes('FROM orders WHERE rzp_order_id = ?')) {
            return Array.from(memoryDB.orders.values()).find(o => o.rzp_order_id === p[0]) || null;
          }
          if (q.includes('FROM subjects WHERE id = ?')) {
            return memoryDB.subjects.get(p[0]) || null;
          }
          if (q.includes('FROM users WHERE id = ?')) {
            return memoryDB.users.get(p[0]) || null;
          }
          if (q.includes('FROM credit_ledger WHERE ref_id = ?')) {
            return Array.from(memoryDB.credit_ledger.values()).find(c => c.ref_id === p[0]) || null;
          }
          if (q.includes('SELECT COALESCE(SUM(delta), 0) as bal FROM credit_ledger')) {
            let sum = 0;
            for (const c of memoryDB.credit_ledger.values()) {
              if (c.user_id === p[0]) sum += c.delta;
            }
            return { bal: sum };
          }
          if (q.includes('FROM voucher_ledger WHERE order_id = ?')) {
            return Array.from(memoryDB.voucher_ledger.values()).find(v => v.order_id === p[0]) || null;
          }
          if (q.includes('SELECT count FROM email_rate_limits')) {
            return { count: 0 };
          }
          if (q.includes('FROM sessions s JOIN users u')) {
            const [tokenHash, nowTs] = p;
            const sess = memoryDB.sessions.get(tokenHash);
            if (sess && sess.expires_at > nowTs) {
              const usr = memoryDB.users.get(sess.user_id) || {};
              return {
                session_id: sess.id,
                expires_at: sess.expires_at,
                user_id: sess.user_id,
                email: usr.email || null,
                phone_hash: usr.phone_hash || null,
                created_at: usr.created_at || sess.created_at
              };
            }
            return null;
          }
          return null;
        },
        async all() {
          const q = this._query;
          const p = this._params;
          if (q.includes('SELECT o.* FROM orders o') && q.includes("o.status = 'PAID'")) {
            const unfulfilled = [];
            for (const o of memoryDB.orders.values()) {
              if (o.user_id === p[0] && o.status === 'PAID') {
                const hasJob = Array.from(memoryDB.report_jobs.values()).some(j => j.order_id === o.id);
                const hasCredit = Array.from(memoryDB.credit_ledger.values()).some(c => c.ref_id === 'order_' + o.id);
                if (!hasJob && !hasCredit) unfulfilled.push(o);
              }
            }
            return { results: unfulfilled };
          }
          if (q.includes('FROM report_jobs WHERE user_id = ?')) {
            const jobs = Array.from(memoryDB.report_jobs.values()).filter(j => j.user_id === p[0]);
            return { results: jobs };
          }
          if (q.includes('FROM subjects WHERE user_id = ?')) {
            const subjs = Array.from(memoryDB.subjects.values()).filter(s => s.user_id === p[0]);
            return { results: subjs };
          }
          if (q.includes("FROM orders WHERE user_id = ? AND status IN ('CREATED', 'PAYMENT_VERIFIED')")) {
            const pending = Array.from(memoryDB.orders.values()).filter(o => o.user_id === p[0] && (o.status === 'CREATED' || o.status === 'PAYMENT_VERIFIED'));
            return { results: pending };
          }
          if (q.includes('SELECT * FROM orders WHERE user_id = ?')) {
            const orders = Array.from(memoryDB.orders.values()).filter(o => o.user_id === p[0]);
            return { results: orders };
          }
          if (q.includes('LEFT JOIN payments p ON o.id = p.order_id') && q.includes("o.status = 'PAID'")) {
            const paid = Array.from(memoryDB.orders.values()).filter(o => o.user_id === p[0] && o.status === 'PAID').map(ord => {
              const pmt = Array.from(memoryDB.payments.values()).find(pm => pm.order_id === ord.id);
              return {
                order_id: ord.id,
                rzp_order_id: ord.rzp_order_id,
                pack_id: ord.pack_id,
                amount_paise: ord.amount_paise,
                currency: ord.currency || 'INR',
                status: ord.status,
                created_at: ord.created_at,
                rzp_payment_id: pmt ? pmt.rzp_payment_id : null,
                captured_at: pmt ? pmt.captured_at : ord.created_at
              };
            });
            return { results: paid };
          }
          if (q.includes('FROM orders o') && q.includes('WHERE o.user_id = ?')) {
            const orders = Array.from(memoryDB.orders.values()).filter(o => o.user_id === p[0] && (o.status === 'PAID' || o.status === 'PAYMENT_VERIFIED'));
            return { results: orders };
          }
          if (q.includes('paidUnfulfilledOrders') || (q.includes("WHERE o.status = 'PAID'") && q.includes('NOT EXISTS (SELECT 1 FROM report_jobs'))) {
            const unfulfilled = [];
            for (const o of memoryDB.orders.values()) {
              if (o.status === 'PAID') {
                const hasJob = Array.from(memoryDB.report_jobs.values()).some(j => j.order_id === o.id);
                const hasCredit = Array.from(memoryDB.credit_ledger.values()).some(c => c.ref_id === 'order_' + o.id);
                if (!hasJob && !hasCredit) {
                  unfulfilled.push({
                    id: o.id,
                    pack_id: o.pack_id,
                    amount_paise: o.amount_paise,
                    currency: o.currency || 'INR',
                    status: o.status,
                    created_at: o.created_at,
                    updated_at: o.updated_at
                  });
                }
              }
            }
            return { results: unfulfilled };
          }
          return { results: [] };
        },
        async run() {
          const q = this._query;
          const p = this._params;
          if (q.startsWith("UPDATE orders SET status = 'PAID'")) {
            const o = memoryDB.orders.get(p[1]);
            if (o) {
              o.status = 'PAID';
              o.updated_at = p[0];
            }
          } else if (q.startsWith("UPDATE orders SET status = 'PAYMENT_VERIFIED'")) {
            const o = memoryDB.orders.get(p[1]);
            if (o && o.status !== 'PAID') {
              o.status = 'PAYMENT_VERIFIED';
              o.updated_at = p[0];
            }
          } else if (q.includes('INSERT INTO report_jobs') || q.includes('INSERT OR IGNORE INTO report_jobs')) {
            const [id, user_id, subject_id, pack_id, order_id, status, created_at] = p;
            if (!Array.from(memoryDB.report_jobs.values()).some(j => j.order_id === order_id)) {
              memoryDB.report_jobs.set(id, { id, user_id, subject_id, pack_id, order_id, status, created_at });
            }
          } else if (q.includes('INSERT INTO payments') || q.includes('INSERT OR IGNORE INTO payments')) {
            const [id, order_id, rzp_payment_id, amount_paise, status, method, captured_at] = p;
            if (!Array.from(memoryDB.payments.values()).some(pm => pm.order_id === order_id)) {
              memoryDB.payments.set(id, { id, order_id, rzp_payment_id, amount_paise, status, method, captured_at });
            }
          } else if (q.includes('INSERT OR IGNORE INTO entitlements')) {
            const [id, user_id, subject_id, pack_id, order_id, granted_at] = p;
            memoryDB.entitlements.set(id, { id, user_id, subject_id, pack_id, order_id, granted_at });
          } else if (q.includes('INSERT INTO audit_log') || q.includes('INSERT OR IGNORE INTO audit_log')) {
            const isEmailSent = q.includes('order_confirmation_email_sent');
            const isEmailAttempt = q.includes('order_confirmation_email_attempt');
            const action = isEmailSent ? 'order_confirmation_email_sent' : (isEmailAttempt ? 'order_confirmation_email_attempt' : (p[2] || 'order_paid_fulfilled'));
            const resource_id = (isEmailSent || isEmailAttempt) ? p[1] : (p[3] || p[2]);
            memoryDB.audit_log.push({ id: p[0], action, resource_id });
          } else if (q.startsWith('INSERT INTO sessions')) {
            const [id, user_id, token_hash, expires_at, created_at, ip_hash, user_agent] = p;
            memoryDB.sessions.set(token_hash, { id, user_id, token_hash, expires_at, created_at, ip_hash, user_agent });
          } else if (q.startsWith('INSERT INTO events')) {
            if (overrides.telemetryThrows) {
              throw new Error('Simulated telemetry failure (e.g. events table lock or network failure)');
            }
            memoryDB.events.push(p);
          }
          return { success: true };
        }
      };
    }
  };

  const env = {
    DB: db,
    _memoryDB: memoryDB,
    ENVIRONMENT: 'test',
    NV_EMAIL_LOG_ADAPTER: 'true',
    EMAIL_PROVIDER: 'brevo',
    EMAIL_API_KEY: 'test_key',
    EMAIL_FROM: 'support@numerosvision.com',
    ADMIN_TOKEN: 'test_admin_token_secret_123',
    IP_HASH_SALT: 'test_ip_hash_salt_mock_12345',
    SESSION_SECRET: 'test_session_secret_32_chars_long_12345',
    DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
    RAZORPAY_KEY_ID: 'rzp_test_mockKey123',
    RAZORPAY_KEY_SECRET: 'mockRazorpaySecret12345',
    RAZORPAY_WEBHOOK_SECRET: 'mockWebhookSecret12345',
    DOWNLOAD_TOKEN_SECRET: 'mockDownloadTokenSecret12345',
    GOOGLE_CLIENT_ID: '123456789-mockclientid.apps.googleusercontent.com',
    BREVO_API_KEY: 'test_brevo_key_mock',
    PUBLIC_BASE_URL: 'https://test.numerosvision.com',
    NV_LAUNCH_STARTS_AT: new Date(Date.now() - 86400000).toISOString(),
    NV_LAUNCH_ENDS_AT: new Date(Date.now() + 6 * 86400000).toISOString(),
    ...overrides
  };

  return env;
}

async function runTestSuite() {
  console.log('--- Starting Comprehensive Paid Order Idempotent Fulfillment Test ---');

  // =========================================================================
  // TEST 1: verify-payment path
  // =========================================================================
  {
    console.log('[Test 1] verify-payment path fulfillment & idempotency');
    const env = createMockEnv();
    const orderId = 'ord_test_verify_001';
    const rzpOrderId = 'order_rzp_mock_001';
    const rzpPaymentId = 'pay_rzp_mock_001';

    env._memoryDB.orders.set(orderId, {
      id: orderId,
      user_id: 'usr_test_001',
      subject_id: 'sbj_test_001',
      pack_id: 'report_basic',
      amount_paise: 19900,
      currency: 'INR',
      rzp_order_id: rzpOrderId,
      status: 'CREATED',
      email: 'customer1@example.com',
      created_at: Date.now() - 5000,
      updated_at: Date.now() - 5000
    });
    env._memoryDB.subjects.set('sbj_test_001', {
      id: 'sbj_test_001',
      email: 'customer1@example.com',
      name: 'Test Customer'
    });

    const crypto = await import('node:crypto');
    const hmac = crypto.createHmac('sha256', env.RAZORPAY_KEY_SECRET);
    hmac.update(`${rzpOrderId}|${rzpPaymentId}`);
    const validSignature = hmac.digest('hex');

    const req1 = new Request('https://test.numerosvision.com/api/v1/payments/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_id: orderId,
        razorpay_order_id: rzpOrderId,
        razorpay_payment_id: rzpPaymentId,
        razorpay_signature: validSignature,
        email: 'customer1@example.com'
      })
    });

    const res1 = await worker.fetch(req1, env, {});
    assert.strictEqual(res1.status, 200, 'verify-payment call 1 should succeed');
    const body1 = await res1.json();
    assert.strictEqual(body1.status, 'verified', 'verify-payment must return status: verified');
    assert.strictEqual(body1.orderStatus, 'PAYMENT_VERIFIED', 'verify-payment must return orderStatus: PAYMENT_VERIFIED');
    assert.strictEqual(body1.awaitingWebhook, true, 'verify-payment must indicate awaitingWebhook: true');

    const orderAfter1 = env._memoryDB.orders.get(orderId);
    assert.strictEqual(orderAfter1.status, 'PAYMENT_VERIFIED', 'Order status must be PAYMENT_VERIFIED (webhook-only PDF generation)');

    const jobs1 = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobs1.length, 0, 'verify-payment must NOT create report job before webhook');

    const emails1 = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emails1.length, 0, 'verify-payment must NOT send fulfillment email before webhook');

    // Second call idempotency check
    const req2 = new Request('https://test.numerosvision.com/api/v1/payments/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_id: orderId,
        razorpay_order_id: rzpOrderId,
        razorpay_payment_id: rzpPaymentId,
        razorpay_signature: validSignature,
        email: 'customer1@example.com'
      })
    });

    const res2 = await worker.fetch(req2, env, {});
    assert.strictEqual(res2.status, 200, 'verify-payment call 2 should succeed idempotently');

    const jobs2 = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobs2.length, 0, 'Second verify call must still wait for webhook');

    console.log('✓ PASS: verify-payment sets PAYMENT_VERIFIED without premature PDF generation.');
  }

  // =========================================================================
  // TEST 2: Webhook path
  // =========================================================================
  {
    console.log('[Test 2] Webhook path fulfillment & idempotency');
    const env = createMockEnv();
    const orderId = 'ord_test_webhook_002';
    const rzpOrderId = 'order_rzp_mock_002';
    const rzpPaymentId = 'pay_rzp_mock_002';

    env._memoryDB.orders.set(orderId, {
      id: orderId,
      user_id: 'usr_test_002',
      subject_id: 'sbj_test_002',
      pack_id: 'report_basic',
      amount_paise: 19900,
      currency: 'INR',
      rzp_order_id: rzpOrderId,
      status: 'CREATED',
      email: 'customer2@example.com',
      created_at: Date.now() - 5000,
      updated_at: Date.now() - 5000
    });
    env._memoryDB.subjects.set('sbj_test_002', {
      id: 'sbj_test_002',
      email: 'customer2@example.com',
      name: 'Webhook Customer'
    });

    const webhookBody = JSON.stringify({
      event: 'order.paid',
      payload: {
        order: {
          entity: {
            id: rzpOrderId,
            amount_paid: 19900,
            status: 'paid'
          }
        },
        payment: {
          entity: {
            id: rzpPaymentId,
            order_id: rzpOrderId,
            amount: 19900,
            currency: 'INR',
            status: 'captured',
            method: 'card'
          }
        }
      }
    });

    const crypto = await import('node:crypto');
    const webhookSig = crypto.createHmac('sha256', env.RAZORPAY_WEBHOOK_SECRET).update(webhookBody).digest('hex');

    const req1 = new Request('https://test.numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Razorpay-Signature': webhookSig
      },
      body: webhookBody
    });

    const res1 = await worker.fetch(req1, env, {});
    assert.strictEqual(res1.status, 200, 'Webhook call 1 should return 200');

    assert.strictEqual(env._memoryDB.orders.get(orderId).status, 'PAID', 'Order status must be updated to PAID');

    const jobs1 = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobs1.length, 1, 'Webhook must create exactly one report job');

    const emails1 = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emails1.length, 1, 'Webhook must dispatch exactly one confirmation email');

    // Duplicate webhook call
    const req2 = new Request('https://test.numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Razorpay-Signature': webhookSig
      },
      body: webhookBody
    });

    const res2 = await worker.fetch(req2, env, {});
    assert.strictEqual(res2.status, 200, 'Duplicate webhook should return 200');

    const jobs2 = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobs2.length, 1, 'Duplicate webhook must not create a duplicate report job');

    const emails2 = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emails2.length, 1, 'Duplicate webhook must not dispatch a duplicate confirmation email');

    console.log('✓ PASS: Webhook marks order paid with exactly one job and one email; retry creates none.');
  }

  // =========================================================================
  // TEST 3: REGRESSION TEST FOR ORIGINAL BUG (Telemetry throws after PAID update)
  // =========================================================================
  {
    console.log('[Test 3] REGRESSION TEST: Telemetry throws after order marked PAID');
    const env = createMockEnv({ telemetryThrows: true });
    const orderId = 'ord_test_telemetry_crash_003';
    const rzpOrderId = 'order_rzp_telemetry_003';
    const rzpPaymentId = 'pay_rzp_telemetry_003';

    env._memoryDB.orders.set(orderId, {
      id: orderId,
      user_id: 'usr_telemetry_003',
      subject_id: 'sbj_telemetry_003',
      pack_id: 'report_basic',
      amount_paise: 19900,
      currency: 'INR',
      rzp_order_id: rzpOrderId,
      status: 'CREATED',
      email: 'seeker@example.com',
      created_at: Date.now() - 2000,
      updated_at: Date.now() - 2000
    });
    env._memoryDB.subjects.set('sbj_telemetry_003', {
      id: 'sbj_telemetry_003',
      email: 'seeker@example.com',
      name: 'Telemetry Seeker'
    });

    const crypto = await import('node:crypto');
    const validSignature = crypto.createHmac('sha256', env.RAZORPAY_KEY_SECRET)
      .update(`${rzpOrderId}|${rzpPaymentId}`).digest('hex');

    // Create a valid checkout token for email
    const ts = Date.now();
    const sig = crypto.createHmac('sha256', env.SESSION_SECRET)
      .update(`seeker@example.com:${ts}`).digest('hex');
    const checkoutToken = `${ts}.${sig}`;

    const req = new Request('https://test.numerosvision.com/api/v1/payments/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_id: orderId,
        razorpay_order_id: rzpOrderId,
        razorpay_payment_id: rzpPaymentId,
        razorpay_signature: validSignature,
        email: 'seeker@example.com',
        checkout_token: checkoutToken
      })
    });

    const res = await worker.fetch(req, env, {});
    assert.strictEqual(res.status, 200, 'verify-payment must succeed even when telemetry throws');
    assert.strictEqual(env._memoryDB.orders.get(orderId).status, 'PAYMENT_VERIFIED', 'Order status must be PAYMENT_VERIFIED after verify');

    // Deliver webhook under telemetryThrows: true as well
    const whBody = JSON.stringify({
      event: 'order.paid',
      payload: {
        order: { entity: { id: rzpOrderId, amount_paid: 19900, status: 'paid' } },
        payment: { entity: { id: rzpPaymentId, order_id: rzpOrderId, amount: 19900, currency: 'INR', status: 'captured', method: 'upi' } }
      }
    });
    const whSig = crypto.createHmac('sha256', env.RAZORPAY_WEBHOOK_SECRET).update(whBody).digest('hex');
    const whRes = await worker.fetch(new Request('https://test.numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': whSig },
      body: whBody
    }), env, {});
    assert.strictEqual(whRes.status, 200, 'webhook must succeed even when telemetry throws');

    // 1. Order marked PAID
    assert.strictEqual(env._memoryDB.orders.get(orderId).status, 'PAID', 'Order status must be PAID');

    // 2. Report job completed
    const jobs = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobs.length, 1, 'Report job must still be created even if telemetry throws');

    // 3. Payment row recorded
    const payments = Array.from(env._memoryDB.payments.values()).filter(p => p.order_id === orderId);
    assert.strictEqual(payments.length, 1, 'Payment row must still be inserted even if telemetry throws');

    // 4. Entitlement recorded
    const entitlements = Array.from(env._memoryDB.entitlements.values()).filter(e => e.order_id === orderId);
    assert.strictEqual(entitlements.length, 1, 'Entitlement must still be granted even if telemetry throws');

    // 5. Email sent
    const emails = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emails.length, 1, 'Confirmation email must still be sent even if telemetry throws');

    // 6. Session minted and Set-Cookie returned
    const setCookie = res.headers.get('Set-Cookie') || '';
    assert(setCookie.includes('__Host-nv_session=') || setCookie.includes('nv_session='), 'Session cookie must be issued even if telemetry throws');

    console.log('✓ PASS: Telemetry failure does not abort fulfillment: job, payment, entitlement, email, and session all complete.');
  }

  // =========================================================================
  // TEST 4: CONCURRENT verify, webhook, and poll
  // =========================================================================
  {
    console.log('[Test 4] CONCURRENCY: Simultaneous verify, webhook, and status poll');
    const env = createMockEnv();
    const orderId = 'ord_concurrent_race_004';
    const rzpOrderId = 'order_rzp_concurrent_004';
    const rzpPaymentId = 'pay_rzp_concurrent_004';

    env._memoryDB.orders.set(orderId, {
      id: orderId,
      user_id: 'usr_concurrent_004',
      subject_id: 'sbj_concurrent_004',
      pack_id: 'report_basic',
      amount_paise: 19900,
      currency: 'INR',
      rzp_order_id: rzpOrderId,
      status: 'CREATED',
      email: 'race@example.com',
      created_at: Date.now() - 3000,
      updated_at: Date.now() - 3000
    });
    env._memoryDB.subjects.set('sbj_concurrent_004', {
      id: 'sbj_concurrent_004',
      email: 'race@example.com',
      name: 'Race Candidate'
    });

    const crypto = await import('node:crypto');
    const verifySig = crypto.createHmac('sha256', env.RAZORPAY_KEY_SECRET)
      .update(`${rzpOrderId}|${rzpPaymentId}`).digest('hex');

    const webhookBody = JSON.stringify({
      event: 'payment.captured',
      payload: {
        payment: {
          entity: {
            id: rzpPaymentId,
            order_id: rzpOrderId,
            amount: 19900,
            currency: 'INR',
            status: 'captured',
            method: 'upi'
          }
        }
      }
    });
    const webhookSig = crypto.createHmac('sha256', env.RAZORPAY_WEBHOOK_SECRET)
      .update(webhookBody).digest('hex');

    // Create HMAC order token for status poll auth
    const expiresAt = Date.now() + 86400000;
    const orderTokenSig = crypto.createHmac('sha256', env.DOWNLOAD_TOKEN_SECRET)
      .update(`${orderId}:${expiresAt}`).digest('hex');
    const orderToken = `${expiresAt}.${orderTokenSig}`;

    // Fire verify, webhook, and status poll concurrently
    const pVerify = worker.fetch(new Request('https://test.numerosvision.com/api/v1/payments/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        order_id: orderId,
        razorpay_order_id: rzpOrderId,
        razorpay_payment_id: rzpPaymentId,
        razorpay_signature: verifySig,
        email: 'race@example.com'
      })
    }), env, {});

    const pWebhook = worker.fetch(new Request('https://test.numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': webhookSig },
      body: webhookBody
    }), env, {});

    const pPoll = worker.fetch(new Request(`https://test.numerosvision.com/api/v1/payments/status?orderId=${encodeURIComponent(orderId)}&token=${encodeURIComponent(orderToken)}`, {
      method: 'GET'
    }), env, {});

    const results = await Promise.all([pVerify, pWebhook, pPoll]);
    for (const r of results) {
      assert(r.status === 200, `Concurrent requests must all succeed (got HTTP ${r.status})`);
    }

    // Assert: EXACTLY ONE report job
    const jobs = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobs.length, 1, `Concurrent race must yield EXACTLY ONE report job (got ${jobs.length})`);

    // Assert: EXACTLY ONE payment row
    const payments = Array.from(env._memoryDB.payments.values()).filter(p => p.order_id === orderId);
    assert.strictEqual(payments.length, 1, `Concurrent race must yield EXACTLY ONE payment row (got ${payments.length})`);

    // Assert: EXACTLY ONE confirmation email
    const emails = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emails.length, 1, `Concurrent race must dispatch EXACTLY ONE confirmation email (got ${emails.length})`);

    console.log('✓ PASS: Concurrent verify, webhook, and status poll fire simultaneously and yield exactly 1 job, 1 payment, and 1 email.');
  }

  // =========================================================================
  // TEST 5: STRICT AUTH ON /api/v1/payments/status
  // =========================================================================
  {
    console.log('[Test 5] STRICT AUTH ON /api/v1/payments/status');
    const env = createMockEnv();
    const orderId = 'ord_status_auth_005';

    env._memoryDB.orders.set(orderId, {
      id: orderId,
      user_id: 'usr_owner_005',
      subject_id: 'sbj_005',
      pack_id: 'report_basic',
      amount_paise: 19900,
      status: 'PAID',
      created_at: Date.now() - 1000
    });

    // 1. Unauthenticated request without token or session -> MUST BE REJECTED (HTTP 401)
    const resNoAuth = await worker.fetch(new Request(`https://test.numerosvision.com/api/v1/payments/status?orderId=${encodeURIComponent(orderId)}`), env, {});
    assert.strictEqual(resNoAuth.status, 401, 'Unauthenticated status poll must return HTTP 401');

    // 2. Request with valid order access token -> MUST BE ACCEPTED (HTTP 200)
    const crypto = await import('node:crypto');
    const expiresAt = Date.now() + 86400000;
    const validSig = crypto.createHmac('sha256', env.DOWNLOAD_TOKEN_SECRET)
      .update(`${orderId}:${expiresAt}`).digest('hex');
    const validToken = `${expiresAt}.${validSig}`;

    const resValidToken = await worker.fetch(new Request(`https://test.numerosvision.com/api/v1/payments/status?orderId=${encodeURIComponent(orderId)}&token=${encodeURIComponent(validToken)}`), env, {});
    assert.strictEqual(resValidToken.status, 200, 'Status poll with valid order token must return HTTP 200');

    // 3. Request with invalid / tampered token -> MUST BE REJECTED (HTTP 401)
    const resInvalidToken = await worker.fetch(new Request(`https://test.numerosvision.com/api/v1/payments/status?orderId=${encodeURIComponent(orderId)}&token=invalid.tampered`), env, {});
    assert.strictEqual(resInvalidToken.status, 401, 'Status poll with invalid token must return HTTP 401');

    console.log('✓ PASS: /api/v1/payments/status strictly requires authentication (token or matching session).');
  }

  // =========================================================================
  // TEST 6: ADMIN TEST CONSOLE "paid_unfulfilled_orders" LIST
  // =========================================================================
  {
    console.log('[Test 6] ADMIN CONSOLE: paid_unfulfilled_orders list');
    const env = createMockEnv();

    // Add 1 paid but unfulfilled order (no report job)
    const unfulfilledId = 'ord_unfulfilled_006';
    env._memoryDB.orders.set(unfulfilledId, {
      id: unfulfilledId,
      user_id: 'usr_006',
      subject_id: 'sbj_006',
      pack_id: 'report_basic',
      amount_paise: 19900,
      currency: 'INR',
      status: 'PAID',
      created_at: 1794260000000,
      updated_at: 1794260100000
    });

    const reqAdmin = new Request('https://test.numerosvision.com/api/admin/test-console?format=json', {
      headers: {
        'X-Admin-Token': env.ADMIN_TOKEN,
        'Accept': 'application/json'
      }
    });

    const resAdmin = await worker.fetch(reqAdmin, env, {});
    assert.strictEqual(resAdmin.status, 200, 'Admin test console must return HTTP 200 for authorized caller');

    const adminData = await resAdmin.json();
    assert(Array.isArray(adminData.paid_unfulfilled_orders), 'Response must contain paid_unfulfilled_orders array');
    assert.strictEqual(adminData.paid_unfulfilled_orders.length, 1, 'Must list exactly 1 unfulfilled paid order');

    const item = adminData.paid_unfulfilled_orders[0];
    assert.strictEqual(item.id, unfulfilledId);
    assert.strictEqual(item.status, 'PAID');
    assert.strictEqual(item.pack_id, 'report_basic');
    // Ensure ZERO personal data
    assert.strictEqual(item.name, undefined, 'Must contain NO personal name');
    assert.strictEqual(item.dob, undefined, 'Must contain NO date of birth');
    assert.strictEqual(item.email, undefined, 'Must contain NO personal email');
    assert.strictEqual(item.phone, undefined, 'Must contain NO phone number');

    // Gateway check validation
    assert(adminData.gateway_check, 'Response must contain gateway_check object');
    assert.strictEqual(adminData.gateway_check.key_id_prefix, 'rzp_test_');
    assert(adminData.gateway_check.razorpay_status !== undefined, 'Gateway check must report razorpay_status');

    console.log('✓ PASS: /api/admin/test-console exposes paid_unfulfilled_orders and read-only gateway_check.');
  }

  // =========================================================================
  // TEST 7: 10-MINUTE RAZORPAY FALLBACK WHEN WEBHOOK IS DELAYED
  // =========================================================================
  {
    console.log('[Test 7] 10-Minute Razorpay REST API Fallback on Stale Unwebhooked Order');
    const env = createMockEnv();
    const orderId = 'ord_fallback_10min_007';
    const rzpOrderId = 'order_rzp_fallback_007';
    const crypto = await import('node:crypto');

    // Seed order created 5 minutes ago (< 10-min threshold)
    env._memoryDB.orders.set(orderId, {
      id: orderId,
      user_id: 'usr_fallback_007',
      subject_id: 'sbj_fallback_007',
      pack_id: 'report_basic',
      amount_paise: 19900,
      currency: 'INR',
      rzp_order_id: rzpOrderId,
      status: 'PAYMENT_VERIFIED',
      email: 'fallback@example.com',
      created_at: Date.now() - (5 * 60 * 1000),
      updated_at: Date.now() - (5 * 60 * 1000)
    });
    env._memoryDB.subjects.set('sbj_fallback_007', {
      id: 'sbj_fallback_007',
      email: 'fallback@example.com',
      name: 'Fallback Seeker'
    });

    const expiresAt = Date.now() + 86400000;
    const validSig = crypto.createHmac('sha256', env.DOWNLOAD_TOKEN_SECRET)
      .update(`${orderId}:${expiresAt}`).digest('hex');
    const validToken = `${expiresAt}.${validSig}`;

    let rzpCalls = 0;
    const origFetch = globalThis.fetch;
    globalThis.fetch = async (input, init) => {
      const u = typeof input === 'string' ? input : input.url;
      if (u === `https://api.razorpay.com/v1/orders/${encodeURIComponent(rzpOrderId)}/payments`) {
        rzpCalls++;
        return new Response(JSON.stringify({
          items: [
            {
              id: 'pay_fallback_captured_007',
              order_id: rzpOrderId,
              amount: 19900,
              currency: 'INR',
              status: 'captured',
              method: 'upi'
            }
          ]
        }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      return origFetch(input, init);
    };

    try {
      // 7a. Poll at 5 minutes (< 10 minutes): must NOT call Razorpay API yet
      const resEarly = await worker.fetch(
        new Request(`https://test.numerosvision.com/api/v1/payments/status?orderId=${encodeURIComponent(orderId)}&token=${encodeURIComponent(validToken)}`),
        env,
        {}
      );
      assert.strictEqual(resEarly.status, 200);
      const dataEarly = await resEarly.json();
      assert.strictEqual(rzpCalls, 0, 'Must not query Razorpay API before 10-minute window');
      assert.strictEqual(dataEarly.status, 'payment_verified');

      // 7b. Age order to 11 minutes (>= 10 minutes) and poll again -> fallback triggers!
      env._memoryDB.orders.get(orderId).created_at = Date.now() - (11 * 60 * 1000);
      env._memoryDB.orders.get(orderId).updated_at = Date.now() - (11 * 60 * 1000);
      const resLate = await worker.fetch(
        new Request(`https://test.numerosvision.com/api/v1/payments/status?orderId=${encodeURIComponent(orderId)}&token=${encodeURIComponent(validToken)}`),
        env,
        {}
      );
      assert.strictEqual(resLate.status, 200);
      const dataLate = await resLate.json();
      assert.strictEqual(rzpCalls, 1, 'Must query Razorpay /orders/{id}/payments once after 10 minutes');
      assert.strictEqual(env._memoryDB.orders.get(orderId).status, 'PAID', 'Fallback must transition order to PAID');
      assert.strictEqual(dataLate.status, 'paid');
      const jobsAfterFallback = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
      assert.strictEqual(jobsAfterFallback.length, 1, 'Fallback must create exactly 1 report job');

      // 7c. Subsequent poll must NOT query Razorpay again or duplicate job
      await worker.fetch(
        new Request(`https://test.numerosvision.com/api/v1/payments/status?orderId=${encodeURIComponent(orderId)}&token=${encodeURIComponent(validToken)}`),
        env,
        {}
      );
      assert.strictEqual(rzpCalls, 1, 'Already-PAID order must not re-query Razorpay');
    } finally {
      globalThis.fetch = origFetch;
    }
    console.log('✓ PASS: 10-minute Razorpay fallback reconciles stale orders idempotently.');
  }

  // =========================================================================
  // TEST 8: PHASE 1 EDGE REDIRECTS, WAF & CANONICAL LINK HEADER
  // =========================================================================
  {
    console.log('[Test 8] Phase 1 single-hop www + /tools/ 301s, /reports/*.pdf WAF, and Link canonical header');
    const env = createMockEnv({
      ASSETS: {
        fetch: async () => new Response('<!DOCTYPE html><html><body>Pricing</body></html>', {
          status: 200,
          headers: { 'Content-Type': 'text/html; charset=utf-8' }
        })
      }
    });

    // 8a. www + legacy /tools/lo-shu-grid -> single-hop 301 to https://numerosvision.com/calculators/lo-shu-grid/
    const resWwwTool = await worker.fetch(new Request('https://www.numerosvision.com/tools/lo-shu-grid?utm_source=ig'), env, {});
    assert.strictEqual(resWwwTool.status, 301);
    assert.strictEqual(resWwwTool.headers.get('Location'), 'https://numerosvision.com/calculators/lo-shu-grid/?utm_source=ig');

    // 8b. /reports/secret.pdf -> 404 blocked, /reports/ -> 200 canonical hub, /reports_catalogue/ -> 301 /reports/
    const resPdfBlock = await worker.fetch(new Request('https://numerosvision.com/reports/customer_123.pdf'), env, {});
    assert.strictEqual(resPdfBlock.status, 404);
    const resReportsDir = await worker.fetch(new Request('https://numerosvision.com/reports/'), env, {});
    assert.strictEqual(resReportsDir.status, 200);
    assert.strictEqual(resReportsDir.headers.get('X-Robots-Tag'), null);
    const resCatalogueLegacy = await worker.fetch(new Request('https://numerosvision.com/reports_catalogue/'), env, {});
    assert.strictEqual(resCatalogueLegacy.status, 301);
    assert.ok(resCatalogueLegacy.headers.get('Location').endsWith('/reports/'));

    // 8b-preview. Preview responses send X-Robots-Tag: noindex on HTML, 301s, and APIs
    const previewEnv = createMockEnv({
      ENVIRONMENT: 'preview',
      NV_LAUNCH_STARTS_AT: '2026-11-12T16:25:00+05:30',
      NV_LAUNCH_ENDS_AT: '2026-11-12T16:50:00+05:30',
      ASSETS: env.ASSETS
    });
    const resPreviewHtml = await worker.fetch(new Request('https://preview.numeros-vision.pages.dev/reports/'), previewEnv, {});
    assert.strictEqual(resPreviewHtml.status, 200);
    assert.strictEqual(resPreviewHtml.headers.get('X-Robots-Tag'), 'noindex');
    const previewBody = await resPreviewHtml.text();
    assert.ok(previewBody.includes('id="nv-preview-launch-banner"'));
    const resPreview301 = await worker.fetch(new Request('https://preview.numeros-vision.pages.dev/reports_catalogue/'), previewEnv, {});
    assert.strictEqual(resPreview301.status, 301);
    assert.strictEqual(resPreview301.headers.get('X-Robots-Tag'), 'noindex');

    // 8c. Parameterized public HTML response includes HTTP Link rel="canonical"
    const resParamHtml = await worker.fetch(new Request('https://numerosvision.com/pricing/?utm_campaign=launch'), env, {});
    assert.strictEqual(resParamHtml.status, 200);
    assert.strictEqual(resParamHtml.headers.get('Link'), '<https://numerosvision.com/pricing/>; rel="canonical"');

    console.log('✓ PASS: Single-hop www/tool 301s, /reports/*.pdf WAF, and Link rel="canonical" verified.');
  }

  // =========================================================================
  // TEST 9: DASHBOARD VIEW — (A) WEBHOOK ARRIVING LATE & (B) WEBHOOK NEVER ARRIVING
  // =========================================================================
  {
    console.log('[Test 9] Dashboard /api/v1/dashboard/view: (a) webhook arriving late & (b) webhook never arriving');
    const env = createMockEnv();
    const crypto = await import('node:crypto');
    const userId = 'usr_dash_reconcile_009';
    env._memoryDB.users.set(userId, {
      id: userId,
      email: 'seeker9@example.com',
      name: 'Bhaskr Singh',
      verified: 1
    });
    env._memoryDB.subjects.set('sbj_dash_009', {
      id: 'sbj_dash_009',
      user_id: userId,
      email: 'seeker9@example.com',
      name: 'Bhaskr Singh'
    });
    const sessionToken = await mintUserSession(env, userId, '127.0.0.1', Date.now());
    const cookieHeader = `nv_session=${sessionToken}`;

    // --- (A) WEBHOOK ARRIVING LATE ---
    const lateOrderId = 'ord_webhook_late_009a';
    const lateRzpOrderId = 'order_rzp_late_009a';
    env._memoryDB.orders.set(lateOrderId, {
      id: lateOrderId,
      user_id: userId,
      subject_id: 'sbj_dash_009',
      pack_id: 'report_basic',
      amount_paise: 19900,
      currency: 'INR',
      rzp_order_id: lateRzpOrderId,
      status: 'PAYMENT_VERIFIED',
      email: 'seeker9@example.com',
      created_at: Date.now() - (4 * 60 * 1000),
      updated_at: Date.now() - (4 * 60 * 1000)
    });

    let rzpFallbackHits = 0;
    const origFetch = globalThis.fetch;
    globalThis.fetch = async (input, init) => {
      const u = typeof input === 'string' ? input : input.url;
      if (u.startsWith('https://api.razorpay.com/v1/orders/')) {
        rzpFallbackHits++;
        const oidMatch = u.split('/orders/')[1].split('/')[0];
        return new Response(JSON.stringify({
          items: [{
            id: `pay_never_webhook_${oidMatch}`,
            order_id: decodeURIComponent(oidMatch),
            amount: 19900,
            currency: 'INR',
            status: 'captured',
            method: 'upi'
          }]
        }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      return origFetch(input, init);
    };

    try {
      // Poll 1 at +4 min: shows "Payment received, preparing your report" without hitting Razorpay API
      const dashRes1 = await worker.fetch(new Request('https://test.numerosvision.com/api/v1/dashboard/view', {
        headers: { Cookie: cookieHeader }
      }), env, {});
      assert.strictEqual(dashRes1.status, 200);
      const dashBody1 = await dashRes1.json();
      assert.strictEqual(rzpFallbackHits, 0, 'Webhook-late order at +4 min must NOT hit Razorpay fallback API');
      const lateReportCard1 = dashBody1.reports.find(r => r.orderId === lateOrderId);
      assert.ok(lateReportCard1, 'PAYMENT_VERIFIED order must appear in dashboard reports');
      assert.strictEqual(lateReportCard1.status, 'preparing');
      assert.strictEqual(lateReportCard1.message, 'Payment received, preparing your report');

      // Signed webhook arrives late (+5 min) -> fulfills order
      const lateWebhookPayload = JSON.stringify({
        event: 'order.paid',
        payload: {
          order: { entity: { id: lateRzpOrderId, amount_paid: 19900, status: 'paid' } },
          payment: { entity: { id: 'pay_late_009a', order_id: lateRzpOrderId, amount: 19900, currency: 'INR', status: 'captured', method: 'upi' } }
        }
      });
      const lateSig = crypto.createHmac('sha256', env.RAZORPAY_WEBHOOK_SECRET).update(lateWebhookPayload).digest('hex');
      const whRes = await worker.fetch(new Request('https://test.numerosvision.com/api/v1/payments/webhook', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': lateSig },
        body: lateWebhookPayload
      }), env, {});
      assert.strictEqual(whRes.status, 200);
      assert.strictEqual(env._memoryDB.orders.get(lateOrderId).status, 'PAID');
      const lateJobs = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === lateOrderId);
      assert.strictEqual(lateJobs.length, 1, 'Late webhook must create 1 report job');

      // --- (B) WEBHOOK NEVER ARRIVING ---
      const neverOrderId = 'ord_webhook_never_009b';
      const neverRzpOrderId = 'order_rzp_never_009b';
      env._memoryDB.orders.set(neverOrderId, {
        id: neverOrderId,
        user_id: userId,
        subject_id: 'sbj_dash_009',
        pack_id: 'report_basic',
        amount_paise: 19900,
        currency: 'INR',
        rzp_order_id: neverRzpOrderId,
        status: 'PAYMENT_VERIFIED',
        email: 'seeker9@example.com',
        created_at: Date.now() - (11 * 60 * 1000),
        updated_at: Date.now() - (11 * 60 * 1000)
      });

      // Dashboard auto-refresh poll at +11 min triggers reconcileStaleOrderWithRazorpay automatically!
      const dashRes2 = await worker.fetch(new Request('https://test.numerosvision.com/api/v1/dashboard/view', {
        headers: { Cookie: cookieHeader }
      }), env, {});
      assert.strictEqual(dashRes2.status, 200);
      const dashBody2 = await dashRes2.json();
      assert.strictEqual(rzpFallbackHits, 1, 'Dashboard poll at +11 min must call Razorpay fallback API once');
      assert.strictEqual(env._memoryDB.orders.get(neverOrderId).status, 'PAID', 'Never-webhook order must transition to PAID via fallback');
      const neverJobs = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === neverOrderId);
      assert.strictEqual(neverJobs.length, 1, 'Never-webhook order must fulfill exactly 1 report job');
      const neverReceipt = dashBody2.receipts.find(rc => rc.order_id === neverOrderId);
      assert.ok(neverReceipt, 'Paid receipt must be emitted in dashboard');
      assert.strictEqual(neverReceipt.supplier_legal_name, 'Bhaskar Kumar Singh');
      assert.strictEqual(neverReceipt.document_type, 'Payment receipt');

      // Repeat dashboard poll must NOT re-call Razorpay or duplicate jobs
      await worker.fetch(new Request('https://test.numerosvision.com/api/v1/dashboard/view', {
        headers: { Cookie: cookieHeader }
      }), env, {});
      assert.strictEqual(rzpFallbackHits, 1, 'Subsequent dashboard polls must not re-query Razorpay');
    } finally {
      globalThis.fetch = origFetch;
    }
    console.log('✓ PASS: Dashboard preparing state + webhook-late and webhook-never-arriving flows verified.');
  }

  // =========================================================================
  // TEST 10: ENV-ONLY LAUNCH WINDOW SWITCH + WAITLIST MASKING + AUTO-CAPTURE
  // =========================================================================
  {
    console.log('[Test 10] Env-only launch-offer switch (unset vs active 7x24h vs expired) + waitlist masking + Razorpay payment_capture: 1');
    // 1. Unset env -> Basic is regular 39900, waitlist tiers masked with "Coming soon, notify me"
    const unsetEnv = createMockEnv({ NV_LAUNCH_STARTS_AT: '', NV_LAUNCH_ENDS_AT: '' });
    const stUnset = resolveServerLaunchOfferState(unsetEnv, Date.now());
    assert.strictEqual(stUnset.configured, false);
    assert.strictEqual(stUnset.active, false);
    assert.strictEqual(getPackById('report_basic', unsetEnv).amount_paise, 39900);
    assert.strictEqual(getPackById('report_basic', unsetEnv).struck_mrp_inr, null);
    for (const wl of ['report_advanced', 'report_premium']) {
      const pWl = getPackById(wl, unsetEnv);
      assert.strictEqual(pWl.waitlist_only, true);
      assert.strictEqual(pWl.display_price_label, 'Coming soon, notify me');
      assert.strictEqual(pWl.struck_mrp_inr, null);
      assert.strictEqual(pWl.launch_offer_copy, '');
    }

    // 2. Active 7x24h window via NV_LAUNCH_STARTS_AT & NV_LAUNCH_ENDS_AT
    const envWin = createMockEnv({
      NV_LAUNCH_STARTS_AT: '2027-01-10T00:00:00+05:30',
      NV_LAUNCH_ENDS_AT: '2027-01-17T00:00:00+05:30'
    });
    const beforeMs = Date.parse('2027-01-12T12:00:00+05:30');
    const afterMs = Date.parse('2027-01-17T00:00:01+05:30');
    assert.strictEqual(resolveServerLaunchOfferState(envWin, beforeMs).active, true);
    assert.strictEqual(resolveServerLaunchOfferState(envWin, afterMs).active, false);
    assert.strictEqual(getPackById('report_basic', envWin, beforeMs).amount_paise, 19900);
    assert.strictEqual(getPackById('report_basic', envWin, beforeMs).struck_mrp_inr, 399);
    assert.strictEqual(getPackById('report_basic', envWin, afterMs).amount_paise, 39900);
    assert.strictEqual(getPackById('report_basic', envWin, afterMs).struck_mrp_inr, null);
    // Waitlist tiers still show "Coming soon, notify me" while NV_NOTIFY_ME_HIGHER_TIERS=true
    assert.strictEqual(getPackById('report_advanced', envWin, beforeMs).display_price_label, 'Coming soon, notify me');
    assert.strictEqual(getPackById('report_premium', envWin, beforeMs).display_price_label, 'Coming soon, notify me');

    // 3. report_advanced and report_premium remain waitlist-only ("Coming soon, notify me", null amount) per packs.json
    const envUnlocked = createMockEnv({
      NV_NOTIFY_ME_HIGHER_TIERS: 'false',
      NV_LAUNCH_STARTS_AT: '2027-01-10T00:00:00+05:30',
      NV_LAUNCH_ENDS_AT: '2027-01-17T00:00:00+05:30'
    });
    assert.strictEqual(getPackById('report_advanced', envUnlocked, beforeMs).amount_paise, null);
    assert.strictEqual(getPackById('report_advanced', envUnlocked, afterMs).amount_paise, null);
    assert.strictEqual(getPackById('report_premium', envUnlocked, beforeMs).amount_paise, null);
    assert.strictEqual(getPackById('report_premium', envUnlocked, afterMs).amount_paise, null);

    // 4. Verify Razorpay order creation sends payment_capture: 1 (auto-capture enabled)
    const workerSrc = fs.readFileSync(path.resolve(process.cwd(), 'app/static/_worker.js'), 'utf8');
    const autoCaptureMatches = workerSrc.match(/payment_capture:\s*1/g) || [];
    assert(autoCaptureMatches.length >= 2, `Expected payment_capture: 1 on both Razorpay order endpoints in _worker.js, found ${autoCaptureMatches.length}`);
    console.log('✓ PASS: Env-only launch window, waitlist masking ("Coming soon, notify me"), and Razorpay payment_capture: 1 verified.');
  }

  // =========================================================================
  // TEST 11: ONE-HOP (301) REDIRECT VERIFICATION MATRIX AGAINST DIST
  // =========================================================================
  {
    console.log('[Test 11] One-hop (301) redirect verification matrix against dist_cloudflare_pages');
    const distDir = path.resolve(process.cwd(), 'dist_cloudflare_pages');
    const env = createMockEnv({
      ASSETS: {
        fetch: async (req) => {
          const u = new URL(req.url);
          const rel = u.pathname === '/' ? 'index.html' : path.join(...u.pathname.replace(/^\/+|\/+$/g, '').split('/'), 'index.html');
          const full = path.join(distDir, rel);
          if (fs.existsSync(full)) {
            return new Response(fs.readFileSync(full), {
              status: 200,
              headers: { 'Content-Type': 'text/html; charset=utf-8' }
            });
          }
          return new Response('Not Found', { status: 404 });
        }
      }
    });

    const redirectCases = [
      ['https://numerosvision.com/tools/lucky-number/', 'https://numerosvision.com/calculators/favourable-numbers/'],
      ['https://numerosvision.com/tools/favourable-numbers/', 'https://numerosvision.com/calculators/favourable-numbers/'],
      ['https://numerosvision.com/tools/lo-shu-grid/', 'https://numerosvision.com/calculators/lo-shu-grid/'],
      ['https://numerosvision.com/tools/name-numerology/', 'https://numerosvision.com/calculators/name-numerology/'],
      ['https://numerosvision.com/tools/name-balancing/', 'https://numerosvision.com/calculators/name-balancing/'],
      ['https://numerosvision.com/tools/mobile-numerology/', 'https://numerosvision.com/calculators/mobile-number/'],
      ['https://numerosvision.com/tools/life-path-calculator/', 'https://numerosvision.com/calculators/life-path/'],
      ['https://numerosvision.com/tools/compatibility-calculator/', 'https://numerosvision.com/calculators/compatibility/'],
      ['https://numerosvision.com/tools/kundali-milan/', 'https://numerosvision.com/calculators/compatibility/'],
      ['https://numerosvision.com/tools/blessing-years/', 'https://numerosvision.com/calculators/personal-year/'],
      ['https://numerosvision.com/tools/business-alignment/', 'https://numerosvision.com/calculators/business-alignment/'],
      ['https://numerosvision.com/tools/business-numerology/', 'https://numerosvision.com/calculators/business-alignment/'],
      ['https://numerosvision.com/tools/baby-naming/', 'https://numerosvision.com/calculators/baby-naming/'],
      ['https://numerosvision.com/tools/property-numerology/', 'https://numerosvision.com/calculators/property-numerology/'],
      ['https://numerosvision.com/tools/vehicle-numerology/', 'https://numerosvision.com/calculators/vehicle-numerology/'],
      ['https://numerosvision.com/tools/profession-calculator/', 'https://numerosvision.com/calculators/profession-calculator/'],
      ['https://numerosvision.com/tools/logo-intelligence/', 'https://numerosvision.com/calculators/logo-intelligence/'],
      ['https://numerosvision.com/tools/logo-studio/', 'https://numerosvision.com/calculators/logo-intelligence/'],
      ['https://numerosvision.com/reports_catalogue/', 'https://numerosvision.com/reports/'],
      ['https://numerosvision.com/reports_catalogue', 'https://numerosvision.com/reports/'],
      ['https://numerosvision.com/reports_catalogue.html', 'https://numerosvision.com/reports/'],
      ['https://numerosvision.com/reports', 'https://numerosvision.com/reports/'],
      ['https://numerosvision.com/reports.html', 'https://numerosvision.com/reports/'],
      ['https://numerosvision.com/charm_ai.html', 'https://numerosvision.com/charm-ai/'],
      ['https://numerosvision.com/privacy-policy/', 'https://numerosvision.com/privacy/'],
      ['https://numerosvision.com/sample-report/', 'https://numerosvision.com/sample/'],
      ['http://numerosvision.com/', 'https://numerosvision.com/'],
      ['https://www.numerosvision.com/', 'https://numerosvision.com/'],
      ['http://www.numerosvision.com/tools/lucky-number/', 'https://numerosvision.com/calculators/favourable-numbers/'],
      ['https://numerosvision.com/numerology_overview/', 'https://numerosvision.com/numerology-overview/'],
      ['https://numerosvision.com/blog/gemstone-remedies.html', 'https://numerosvision.com/blog/vedic-gemstone-remedies/'],
      ['https://numerosvision.com/blog/what-is-numerology.html', 'https://numerosvision.com/blog/what-is-numerology/']
    ];

    for (const [srcUrl, expectedTarget] of redirectCases) {
      const r1 = await worker.fetch(new Request(srcUrl), env, {});
      assert.strictEqual(r1.status, 301, `Expected 301 on ${srcUrl}, got ${r1.status}`);
      const loc = r1.headers.get('Location');
      assert.strictEqual(loc, expectedTarget, `Expected 1-hop Location ${expectedTarget} for ${srcUrl}, got ${loc}`);
      const r2 = await worker.fetch(new Request(loc), env, {});
      assert.strictEqual(r2.status, 200, `Expected final 200 OK at ${loc} (1 hop from ${srcUrl}), got ${r2.status}`);
    }
    const pdfBlockRes = await worker.fetch(new Request('https://numerosvision.com/reports/private_customer.pdf'), env, {});
    assert.strictEqual(pdfBlockRes.status, 404, 'Direct /reports/*.pdf requests must still be blocked with HTTP 404');
    console.log(`✓ PASS: All ${redirectCases.length} redirect routes verified as 301 in exactly 1 hop -> 200 OK (and /reports/*.pdf blocked 404).`);
  }

  // =========================================================================
  // TEST 12: PREVIEW X-ROBOTS-TAG: NOINDEX & ACTIVE LAUNCH WINDOW BANNER
  // =========================================================================
  {
    console.log('[Test 12] Preview responses send X-Robots-Tag: noindex and render active launch-window banner');
    const previewEnv = createMockEnv({
      ENVIRONMENT: 'preview',
      NV_LAUNCH_STARTS_AT: new Date(Date.now() - 60000).toISOString(),
      NV_LAUNCH_ENDS_AT: new Date(Date.now() + 1800000).toISOString(),
      ASSETS: {
        fetch: async () => new Response('<!DOCTYPE html><html><head><title>Preview</title></head><body><h1>Main</h1></body></html>', {
          status: 200,
          headers: { 'Content-Type': 'text/html; charset=utf-8' }
        })
      }
    });

    const prevHtmlRes = await worker.fetch(new Request('https://preview.numeros-vision.pages.dev/pricing/'), previewEnv, {});
    assert.strictEqual(prevHtmlRes.status, 200);
    assert(prevHtmlRes.headers.get('X-Robots-Tag')?.includes('noindex'), 'Preview HTML response must send X-Robots-Tag: noindex');
    const prevHtmlBody = await prevHtmlRes.text();
    assert(prevHtmlBody.includes('id="nv-preview-launch-banner"'), 'Preview HTML response must inject active launch-window banner');
    assert(prevHtmlBody.includes('window.__NV_LAUNCH_ENDS_AT'), 'Preview HTML response must inject server launch window config');

    const prevRedirRes = await worker.fetch(new Request('https://preview.numeros-vision.pages.dev/reports_catalogue/'), previewEnv, {});
    assert.strictEqual(prevRedirRes.status, 301);
    assert(prevRedirRes.headers.get('X-Robots-Tag')?.includes('noindex'), 'Preview 301 redirect response must also send X-Robots-Tag: noindex');

    const prevApiRes = await worker.fetch(new Request('https://preview.numeros-vision.pages.dev/api/v1/pricing-catalog'), previewEnv, {});
    assert.strictEqual(prevApiRes.status, 200);
    assert(prevApiRes.headers.get('X-Robots-Tag')?.includes('noindex'), 'Preview API response must also send X-Robots-Tag: noindex');
    console.log('✓ PASS: Preview HTML, 301 redirects, and API responses all send X-Robots-Tag: noindex and render preview window banner.');
  }

  console.log('--- ALL SUITE TESTS PASSED SUCCESSFULLY (12/12) ---');
}

runTestSuite().catch(err => {
  console.error('Test suite failed:', err);
  process.exit(1);
});
