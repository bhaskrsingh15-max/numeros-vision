import assert from 'node:assert';
import worker from '../app/static/_worker.js';

// Mock environment for edge worker testing
function createMockEnv() {
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
          if (q.includes('FROM orders o') && q.includes('WHERE o.user_id = ?')) {
            const orders = Array.from(memoryDB.orders.values()).filter(o => o.user_id === p[0] && o.status === 'PAID');
            return { results: orders };
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
          } else if (q.startsWith('INSERT INTO report_jobs')) {
            const [id, user_id, subject_id, pack_id, order_id, status, created_at] = p;
            memoryDB.report_jobs.set(id, { id, user_id, subject_id, pack_id, order_id, status, created_at });
          } else if (q.startsWith('INSERT INTO payments')) {
            const [id, order_id, rzp_payment_id, amount_paise, status, method, captured_at] = p;
            memoryDB.payments.set(id, { id, order_id, rzp_payment_id, amount_paise, status, method, captured_at });
          } else if (q.startsWith('INSERT OR IGNORE INTO entitlements')) {
            const [id, user_id, subject_id, pack_id, order_id, granted_at] = p;
            memoryDB.entitlements.set(id, { id, user_id, subject_id, pack_id, order_id, granted_at });
          } else if (q.startsWith('INSERT INTO audit_log')) {
            const isEmailSent = q.includes('order_confirmation_email_sent');
            const action = isEmailSent ? 'order_confirmation_email_sent' : (p[2] || 'order_paid_fulfilled');
            const resource_id = isEmailSent ? p[1] : (p[3] || p[2]);
            memoryDB.audit_log.push({ id: p[0], action, resource_id });
          } else if (q.startsWith('INSERT INTO events')) {
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
    EMAIL_API_KEY: 'mock_key',
    EMAIL_FROM: 'support@numerosvision.com',
    SESSION_SECRET: 'test_session_secret_32_chars_long_12345',
    RAZORPAY_KEY_ID: 'rzp_test_mockKey123',
    RAZORPAY_KEY_SECRET: 'mockRazorpaySecret12345',
    RAZORPAY_WEBHOOK_SECRET: 'mockWebhookSecret12345',
    DOWNLOAD_TOKEN_SECRET: 'mockDownloadTokenSecret12345',
    GOOGLE_CLIENT_ID: '123456789-mockclientid.apps.googleusercontent.com',
    BREVO_API_KEY: 'test_brevo_key_mock',
    PUBLIC_BASE_URL: 'https://test.numerosvision.com'
  };

  return env;
}

async function runTestSuite() {
  console.log('--- Starting Worker-Level Paid Order Idempotent Fulfillment Test ---');

  // =========================================================================
  // TEST 1: verify-payment path
  // =========================================================================
  {
    console.log('[Test 1] verify-payment path fulfillment & idempotency');
    const env = createMockEnv();
    const orderId = 'ord_test_verify_001';
    const rzpOrderId = 'order_rzp_mock_001';
    const rzpPaymentId = 'pay_rzp_mock_001';

    // Seed order in DB
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

    // Compute valid signature
    const crypto = await import('node:crypto');
    const hmac = crypto.createHmac('sha256', env.RAZORPAY_KEY_SECRET);
    hmac.update(`${rzpOrderId}|${rzpPaymentId}`);
    const validSignature = hmac.digest('hex');

    // Call verify-payment (Path 1)
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

    // Assert: Order status is PAID
    const orderAfter1 = env._memoryDB.orders.get(orderId);
    assert.strictEqual(orderAfter1.status, 'PAID', 'Order status must be updated to PAID');

    // Assert: Exactly ONE report job created
    const jobs1 = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobs1.length, 1, 'Exactly one report job must be created for order on first call');

    // Assert: Exactly ONE confirmation email recorded
    const emails1 = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emails1.length, 1, 'Exactly one order confirmation email must be recorded on first call');

    // Call verify-payment SECOND time (idempotency check)
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

    // Assert: STILL exactly ONE report job created (no duplicates)
    const jobs2 = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobs2.length, 1, 'Second verify call must NOT create a duplicate report job');

    // Assert: STILL exactly ONE confirmation email recorded
    const emails2 = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emails2.length, 1, 'Second verify call must NOT dispatch a duplicate confirmation email');

    console.log('✓ PASS: verify-payment creates exactly one job and one email; second call creates none.');
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

    // Seed order in DB
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

    // Call Webhook Call 1
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

    // Assert: Order is marked PAID
    assert.strictEqual(env._memoryDB.orders.get(orderId).status, 'PAID', 'Order status must be updated to PAID');

    // Assert: Exactly ONE report job created
    const jobs1 = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobs1.length, 1, 'Webhook must create exactly one report job');

    // Assert: Exactly ONE email sent
    const emails1 = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emails1.length, 1, 'Webhook must dispatch exactly one confirmation email');

    // Call Webhook Call 2 (Duplicate / retry event)
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

    // Assert: STILL exactly ONE job and ONE email
    const jobs2 = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobs2.length, 1, 'Duplicate webhook must not create a duplicate report job');

    const emails2 = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emails2.length, 1, 'Duplicate webhook must not dispatch a duplicate confirmation email');

    console.log('✓ PASS: Webhook marks order paid with exactly one job and one email; retry creates none.');
  }

  // =========================================================================
  // TEST 3: Safety net on status poll (Reproducing ord_1794260665323 real bug)
  // =========================================================================
  {
    console.log('[Test 3] Safety net on payments/status poll (reproducing ord_1794260665323)');
    const env = createMockEnv();
    const orderId = 'ord_1794260665323_cf45d0e3';

    // Seed order in DB as PAID but with NO report job and NO email (the exact defect state)
    env._memoryDB.orders.set(orderId, {
      id: orderId,
      user_id: 'usr_test_003',
      subject_id: 'sbj_test_003',
      pack_id: 'report_basic',
      amount_paise: 19900,
      currency: 'INR',
      rzp_order_id: 'order_TyEIRIFM6U9dAs',
      status: 'PAID',
      email: 'customer3@example.com',
      created_at: 1794260665323,
      updated_at: 1794260758973
    });
    env._memoryDB.subjects.set('sbj_test_003', {
      id: 'sbj_test_003',
      email: 'customer3@example.com',
      name: 'Bhaskr Singh'
    });

    // Ensure 0 jobs and 0 emails exist initially
    assert.strictEqual(Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId).length, 0);
    assert.strictEqual(env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent').length, 0);

    // Call /api/v1/payments/status
    const reqStatus1 = new Request(`https://test.numerosvision.com/api/v1/payments/status?orderId=${encodeURIComponent(orderId)}`, {
      method: 'GET'
    });

    const resStatus1 = await worker.fetch(reqStatus1, env, {});
    assert.strictEqual(resStatus1.status, 200, 'Status poll should succeed');

    // Assert: Safety net created the report job!
    const jobsAfterPoll1 = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobsAfterPoll1.length, 1, 'Safety net on status poll must create missing report job for PAID order');

    // Assert: Safety net sent the confirmation email!
    const emailsAfterPoll1 = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emailsAfterPoll1.length, 1, 'Safety net on status poll must dispatch missing confirmation email');

    // Call status poll a SECOND time
    const reqStatus2 = new Request(`https://test.numerosvision.com/api/v1/payments/status?orderId=${encodeURIComponent(orderId)}`, {
      method: 'GET'
    });
    const resStatus2 = await worker.fetch(reqStatus2, env, {});
    assert.strictEqual(resStatus2.status, 200);

    // Assert: No duplicate jobs or emails created
    const jobsAfterPoll2 = Array.from(env._memoryDB.report_jobs.values()).filter(j => j.order_id === orderId);
    assert.strictEqual(jobsAfterPoll2.length, 1, 'Subsequent status poll must NOT create duplicate report job');

    const emailsAfterPoll2 = env._memoryDB.audit_log.filter(a => a.resource_id === orderId && a.action === 'order_confirmation_email_sent');
    assert.strictEqual(emailsAfterPoll2.length, 1, 'Subsequent status poll must NOT dispatch duplicate confirmation email');

    console.log('✓ PASS: Safety net on status poll successfully heals PAID order without report job and without duplicate on retry.');
  }

  // =========================================================================
  // TEST 4: Google Auth Config route & Audience verification
  // =========================================================================
  {
    console.log('[Test 4] Google Auth Config route & Audience verification');
    const env = createMockEnv();

    const reqConfig = new Request('https://test.numerosvision.com/api/google-auth-config.js', { method: 'GET' });
    const resConfig = await worker.fetch(reqConfig, env, {});
    assert.strictEqual(resConfig.status, 200);
    const scriptBody = await resConfig.text();
    assert(scriptBody.includes('window.NV_GOOGLE_CLIENT_ID = "123456789-mockclientid.apps.googleusercontent.com";'), 'Script must define NV_GOOGLE_CLIENT_ID from env');

    // Test audience mismatch in /api/v1/auth/google
    const header = Buffer.from(JSON.stringify({ alg: 'RS256' })).toString('base64url');
    const wrongAudPayload = Buffer.from(JSON.stringify({
      iss: 'https://accounts.google.com',
      aud: 'wrong-audience-client-id.apps.googleusercontent.com',
      exp: Math.floor(Date.now() / 1000) + 3600,
      email: 'test@example.com',
      email_verified: true
    })).toString('base64url');
    const mockToken = `${header}.${wrongAudPayload}.mockSignature`;

    const reqGoogleAuth = new Request('https://test.numerosvision.com/api/v1/auth/google', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ credential: mockToken })
    });

    const resGoogleAuth = await worker.fetch(reqGoogleAuth, env, {});
    assert.strictEqual(resGoogleAuth.status, 401);
    const data = await resGoogleAuth.json();
    assert.strictEqual(data.error, 'Google ID token audience mismatch.');

    console.log('✓ PASS: /api/google-auth-config.js works and worker strictly verifies audience against GOOGLE_CLIENT_ID.');
  }

  console.log('--- ALL WORKER-LEVEL TESTS PASSED SUCCESSFULLY (4/4) ---');
}

runTestSuite().catch(err => {
  console.error('Test suite failed:', err);
  process.exit(1);
});
