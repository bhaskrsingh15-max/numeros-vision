import assert from 'node:assert';
import worker from '../app/static/_worker.js';

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
                if (!hasJob) unfulfilled.push(o);
              }
            }
            return { results: unfulfilled };
          }
          if (q.includes('FROM report_jobs WHERE user_id = ?')) {
            const jobs = Array.from(memoryDB.report_jobs.values()).filter(j => j.user_id === p[0]);
            return { results: jobs };
          }
          if (q.includes("FROM orders WHERE user_id = ? AND status IN ('CREATED', 'PAYMENT_VERIFIED')")) {
            const pending = Array.from(memoryDB.orders.values()).filter(o => o.user_id === p[0] && (o.status === 'CREATED' || o.status === 'PAYMENT_VERIFIED'));
            return { results: pending };
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
                if (!hasJob) {
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
    RAZORPAY_KEY_ID: 'rzp_test_mockKey123',
    RAZORPAY_KEY_SECRET: 'mockRazorpaySecret12345',
    RAZORPAY_WEBHOOK_SECRET: 'mockWebhookSecret12345',
    DOWNLOAD_TOKEN_SECRET: 'mockDownloadTokenSecret12345',
    GOOGLE_CLIENT_ID: '123456789-mockclientid.apps.googleusercontent.com',
    BREVO_API_KEY: 'test_brevo_key_mock',
    PUBLIC_BASE_URL: 'https://test.numerosvision.com',
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
      pack_id: 'report_master',
      amount_paise: 51000,
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
            amount_paid: 51000,
            status: 'paid'
          }
        },
        payment: {
          entity: {
            id: rzpPaymentId,
            order_id: rzpOrderId,
            amount: 51000,
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

    // 8b. /reports/secret.pdf -> 404 blocked, while /reports/ -> 301 /reports_catalogue/
    const resPdfBlock = await worker.fetch(new Request('https://numerosvision.com/reports/customer_123.pdf'), env, {});
    assert.strictEqual(resPdfBlock.status, 404);
    const resReportsDir = await worker.fetch(new Request('https://numerosvision.com/reports/'), env, {});
    assert.strictEqual(resReportsDir.status, 301);
    assert.ok(resReportsDir.headers.get('Location').endsWith('/reports_catalogue/'));

    // 8c. Parameterized public HTML response includes HTTP Link rel="canonical"
    const resParamHtml = await worker.fetch(new Request('https://numerosvision.com/pricing/?utm_campaign=launch'), env, {});
    assert.strictEqual(resParamHtml.status, 200);
    assert.strictEqual(resParamHtml.headers.get('Link'), '<https://numerosvision.com/pricing/>; rel="canonical"');

    console.log('✓ PASS: Single-hop www/tool 301s, /reports/*.pdf WAF, and Link rel="canonical" verified.');
  }

  console.log('--- ALL SUITE TESTS PASSED SUCCESSFULLY (8/8) ---');
}

runTestSuite().catch(err => {
  console.error('Test suite failed:', err);
  process.exit(1);
});
