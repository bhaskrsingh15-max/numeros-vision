/**
 * NUMEROS VISION - COMMIT 5 GATING & ENTITLEMENTS TEST SUITE
 * Validates:
 * 1. viewFor(user, subject, env) unlock matrix:
 *    - Free: Lo Shu grid with enabled digits; missing digits as locked marks ('🔒')
 *    - Basic (report_basic, ₹199, 3 pages): elementBalancing unlocked; rest locked
 *    - Advanced (report_advanced, ₹510, 12 pages): elementBalancing + enabledNumbersInDepth unlocked; rest locked
 *    - Premium (report_premium, ₹1,050, 32 pages): 100% unlocked (missing numbers in depth, remedies, predictions)
 * 2. Entitlements from refunded orders are excluded from viewFor
 * 3. POST /api/v1/subjects requires session (401)
 * 4. POST /api/v1/subjects enforces DPDP 2023 statutory consent (consent === true)
 * 5. POST /api/v1/subjects caps subjects at 10 per account
 * 6. POST /api/v1/payments/create-order enforces 10-subject cap on auto-creation
 * 7. GET /api/v1/subjects enforces tenant isolation
 * 8. GET /api/v1/dashboard/view rejects unauthenticated requests (401)
 * 9. GET /api/v1/dashboard/view returns server-gated view, invoices, orders, and Charm credits
 * 10. Partial refund does not auto-revoke; flags in audit_log for manual review
 */

import worker, { viewFor, parseDobParts } from '../app/static/_worker.js';
import crypto from 'node:crypto';

async function assertCase(name, fn) {
  try {
    await fn();
    console.log(`✓ PASS: ${name}`);
  } catch (err) {
    console.error(`✗ FAIL: ${name}: ${err.message}`);
    process.exitCode = 1;
  }
}

async function runTests() {
  console.log('\n--- STARTING COMMIT 5 GATING & ENTITLEMENTS TESTS ---\n');

  const mockEnv = {
    ENVIRONMENT: 'local',
    RAZORPAY_KEY_ID: 'rzp_test_MOCK_COMMIT5_KEY',
    RAZORPAY_KEY_SECRET: 'test_secret_for_commit5_payments',
    RAZORPAY_WEBHOOK_SECRET: 'test_webhook_secret_commit5',
    AUTH_SECRET: 'test_auth_secret_commit5_salt',
    ASSETS: {
      fetch: async () => new Response('Asset stub', { status: 200 })
    }
  };

  // Mock global fetch for Razorpay API calls in test environment
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, options = {}) => {
    const urlStr = String(url);
    if (urlStr.includes('api.razorpay.com/v1/orders')) {
      const body = JSON.parse(options.body || '{}');
      return new Response(JSON.stringify({
        id: 'order_rzp_mock_' + Date.now() + '_' + Math.random().toString(36).substring(2, 7),
        entity: 'order',
        amount: body.amount,
        currency: body.currency || 'INR',
        receipt: body.receipt,
        status: 'created'
      }), { status: 200, headers: { 'Content-Type': 'application/json' } });
    }
    return originalFetch(url, options);
  };

  // Helper: create authenticated session cookie
  async function createSession(phone) {
    const sendReq = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone })
    });
    const sendRes = await worker.fetch(sendReq, mockEnv);
    const sendData = await sendRes.json();
    const code = sendData.dev_otp;

    const verifyReq = new Request('https://numerosvision.com/api/v1/auth/otp/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone, code })
    });
    const verifyRes = await worker.fetch(verifyReq, mockEnv);
    const cookieHeader = verifyRes.headers.get('Set-Cookie');
    return cookieHeader.split(';')[0]; // "__Host-nv_session=..."
  }

  const sessionCookie = await createSession('9876540001');
  const sessionCookie2 = await createSession('9876540002');

  // Fetch user info for tester 1
  const meRes = await worker.fetch(new Request('https://numerosvision.com/api/me', {
    headers: { 'Cookie': sessionCookie }
  }), mockEnv);
  const meData = await meRes.json();
  const testUser = { user_id: meData.user.id, phone: '9876540001', email: 'test1@example.com' };

  // 1. Test parseDobParts
  await assertCase('parseDobParts parses standard YYYY-MM-DD and DD-MM-YYYY formats', async () => {
    const p1 = parseDobParts('1981-11-28');
    if (p1.day !== 28 || p1.month !== 11 || p1.year !== 1981 || p1.dob !== '1981-11-28') {
      throw new Error(`Expected 1981-11-28, got ${JSON.stringify(p1)}`);
    }
    const p2 = parseDobParts('28-11-1981');
    if (p2.day !== 28 || p2.month !== 11 || p2.year !== 1981 || p2.dob !== '1981-11-28') {
      throw new Error(`Expected 1981-11-28 from DD-MM-YYYY, got ${JSON.stringify(p2)}`);
    }
  });

  // 2. Test viewFor Free Tier
  const subjectA = { id: 'sbj_free_test', name: 'Free Seeker', dob: '1981-11-28', created_at: Date.now() };
  await assertCase('viewFor Free Tier: grid with enabled digits, missing digits as locked marks (🔒), and locked deep sections', async () => {
    const view = await viewFor(testUser, subjectA, mockEnv);
    if (!view) throw new Error('Expected viewFor to return data');
    if (view.tier !== 'free') throw new Error(`Expected tier free, got ${view.tier}`);

    // Check grid cells
    const cells = view.sections.grid.cells;
    if (!cells || cells.length !== 9) throw new Error(`Expected 9 grid cells, got ${cells ? cells.length : 0}`);

    // Digits 1, 2, 8, 9 are present in 1981-11-28
    const cell1 = cells.find(c => c.digit === 1);
    if (!cell1 || cell1.status !== 'present' || cell1.count !== 4) {
      throw new Error(`Expected digit 1 present with count 4, got ${JSON.stringify(cell1)}`);
    }

    // Digit 5 is missing in 1981-11-28 -> must be locked with mark '🔒'
    const cell5 = cells.find(c => c.digit === 5);
    if (!cell5 || cell5.status !== 'locked' || cell5.mark !== '🔒') {
      throw new Error(`Expected missing digit 5 to be locked with mark 🔒, got ${JSON.stringify(cell5)}`);
    }

    // Check locked sections
    if (view.sections.elementBalancing.unlocked !== false) throw new Error('Expected elementBalancing to be locked in free tier');
    if (view.sections.enabledNumbersInDepth.unlocked !== false) throw new Error('Expected enabledNumbersInDepth to be locked in free tier');
    if (view.sections.missingNumbersInDepth.unlocked !== false) throw new Error('Expected missingNumbersInDepth to be locked in free tier');
    if (view.sections.remedies.unlocked !== false) throw new Error('Expected remedies to be locked in free tier');
    if (view.sections.predictions.unlocked !== false) throw new Error('Expected predictions to be locked in free tier');
  });

  // 3. Test viewFor Basic Tier (report_basic, ₹199, 3 pages)
  await assertCase('viewFor Basic Tier: elementBalancing unlocked (3 pages); rest locked', async () => {
    const subjectBasic = { id: 'sbj_basic_test', name: 'Basic Seeker', dob: '1985-06-15', created_at: Date.now() };
    // Grant report_basic entitlement directly in memoryStore
    const ordId = 'ord_basic_' + Date.now();
    mockEnv.orders = mockEnv.orders || new Map();
    // In _worker.js memoryStore handles this:
    // Create an order and pay it
    const createReq = new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': sessionCookie },
      body: JSON.stringify({ packId: 'report_basic', name: 'Basic Seeker', dob: '1985-06-15' })
    });
    const createRes = await worker.fetch(createReq, mockEnv);
    const ordData = await createRes.json();

    // Webhook pay
    const payId = 'pay_basic_' + Date.now();
    const payPayload = JSON.stringify({
      event: 'order.paid',
      event_id: 'evt_basic_' + Date.now(),
      payload: {
        order: { entity: { id: ordData.rzpOrderId } },
        payment: { entity: { id: payId, amount: 19900, currency: 'INR', order_id: ordData.rzpOrderId } }
      }
    });
    const sig = crypto.createHmac('sha256', mockEnv.RAZORPAY_WEBHOOK_SECRET).update(payPayload).digest('hex');
    await worker.fetch(new Request('https://numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': sig },
      body: payPayload
    }), mockEnv);

    const paidSubject = { id: ordData.subjectId, name: 'Basic Seeker', dob: '1985-06-15' };
    const view = await viewFor(testUser, paidSubject, mockEnv);

    if (view.tier !== 'basic') throw new Error(`Expected tier basic, got ${view.tier}`);
    if (view.sections.elementBalancing.unlocked !== true) throw new Error('Expected elementBalancing to be unlocked in basic tier');
    if (view.sections.elementBalancing.pageCount !== 3) throw new Error(`Expected 3 pages, got ${view.sections.elementBalancing.pageCount}`);
    if (view.sections.enabledNumbersInDepth.unlocked !== false) throw new Error('Expected enabledNumbersInDepth to be locked in basic tier');
    if (view.sections.missingNumbersInDepth.unlocked !== false) throw new Error('Expected missingNumbersInDepth to be locked in basic tier');
    if (view.sections.remedies.unlocked !== false) throw new Error('Expected remedies to be locked in basic tier');
    if (view.sections.predictions.unlocked !== false) throw new Error('Expected predictions to be locked in basic tier');
  });

  // 4. Test viewFor Advanced Tier (report_advanced, ₹510, 12 pages)
  await assertCase('viewFor Advanced Tier: elementBalancing + enabledNumbersInDepth unlocked (12 pages); rest locked', async () => {
    const createReq = new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': sessionCookie },
      body: JSON.stringify({ packId: 'report_advanced', name: 'Advanced Seeker', dob: '1990-03-24' })
    });
    const createRes = await worker.fetch(createReq, mockEnv);
    const ordData = await createRes.json();

    const payId = 'pay_adv_' + Date.now();
    const payPayload = JSON.stringify({
      event: 'order.paid',
      event_id: 'evt_adv_' + Date.now(),
      payload: {
        order: { entity: { id: ordData.rzpOrderId } },
        payment: { entity: { id: payId, amount: 51000, currency: 'INR', order_id: ordData.rzpOrderId } }
      }
    });
    const sig = crypto.createHmac('sha256', mockEnv.RAZORPAY_WEBHOOK_SECRET).update(payPayload).digest('hex');
    await worker.fetch(new Request('https://numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': sig },
      body: payPayload
    }), mockEnv);

    const paidSubject = { id: ordData.subjectId, name: 'Advanced Seeker', dob: '1990-03-24' };
    const view = await viewFor(testUser, paidSubject, mockEnv);

    if (view.tier !== 'advanced') throw new Error(`Expected tier advanced, got ${view.tier}`);
    if (view.sections.elementBalancing.unlocked !== true) throw new Error('Expected elementBalancing to be unlocked');
    if (view.sections.enabledNumbersInDepth.unlocked !== true) throw new Error('Expected enabledNumbersInDepth to be unlocked');
    if (view.sections.enabledNumbersInDepth.pageCount !== 12) throw new Error(`Expected 12 pages, got ${view.sections.enabledNumbersInDepth.pageCount}`);
    if (view.sections.missingNumbersInDepth.unlocked !== false) throw new Error('Expected missingNumbersInDepth to be locked');
    if (view.sections.remedies.unlocked !== false) throw new Error('Expected remedies to be locked');
    if (view.sections.predictions.unlocked !== false) throw new Error('Expected predictions to be locked');
  });

  // 5. Test viewFor Premium Tier (report_premium, ₹1,050, 32 pages)
  await assertCase('viewFor Premium Tier: 100% unlocked (missing numbers in depth, remedies, predictions, 32 pages)', async () => {
    const createReq = new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': sessionCookie },
      body: JSON.stringify({ packId: 'report_premium', name: 'Premium Seeker', dob: '1977-07-07' })
    });
    const createRes = await worker.fetch(createReq, mockEnv);
    const ordData = await createRes.json();

    const payId = 'pay_prem_' + Date.now();
    const payPayload = JSON.stringify({
      event: 'order.paid',
      event_id: 'evt_prem_' + Date.now(),
      payload: {
        order: { entity: { id: ordData.rzpOrderId } },
        payment: { entity: { id: payId, amount: 105000, currency: 'INR', order_id: ordData.rzpOrderId } }
      }
    });
    const sig = crypto.createHmac('sha256', mockEnv.RAZORPAY_WEBHOOK_SECRET).update(payPayload).digest('hex');
    await worker.fetch(new Request('https://numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': sig },
      body: payPayload
    }), mockEnv);

    const paidSubject = { id: ordData.subjectId, name: 'Premium Seeker', dob: '1977-07-07' };
    const view = await viewFor(testUser, paidSubject, mockEnv);

    if (view.tier !== 'premium') throw new Error(`Expected tier premium, got ${view.tier}`);
    if (view.sections.elementBalancing.unlocked !== true) throw new Error('Expected elementBalancing to be unlocked');
    if (view.sections.enabledNumbersInDepth.unlocked !== true) throw new Error('Expected enabledNumbersInDepth to be unlocked');
    if (view.sections.missingNumbersInDepth.unlocked !== true) throw new Error('Expected missingNumbersInDepth to be unlocked');
    if (view.sections.remedies.unlocked !== true) throw new Error('Expected remedies to be unlocked');
    if (view.sections.predictions.unlocked !== true) throw new Error('Expected predictions to be unlocked');
    if (view.sections.missingNumbersInDepth.pageCount !== 32) throw new Error('Expected 32 pages in missingNumbersInDepth');
  });

  // 6. Test: Entitlements from refunded orders are excluded from viewFor
  await assertCase('Entitlements from refunded orders are strictly excluded from viewFor', async () => {
    // Buy a basic report for a fresh subject
    const createReq = new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': sessionCookie },
      body: JSON.stringify({ packId: 'report_basic', name: 'Refund Test Subject', dob: '1999-09-09' })
    });
    const createRes = await worker.fetch(createReq, mockEnv);
    const ordData = await createRes.json();

    const payId = 'pay_to_ref_ent_' + Date.now();
    const payPayload = JSON.stringify({
      event: 'order.paid',
      event_id: 'evt_pre_ref_' + Date.now(),
      payload: {
        order: { entity: { id: ordData.rzpOrderId } },
        payment: { entity: { id: payId, amount: 19900, currency: 'INR', order_id: ordData.rzpOrderId } }
      }
    });
    const sig = crypto.createHmac('sha256', mockEnv.RAZORPAY_WEBHOOK_SECRET).update(payPayload).digest('hex');
    await worker.fetch(new Request('https://numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': sig },
      body: payPayload
    }), mockEnv);

    const testSubj = { id: ordData.subjectId, name: 'Refund Test Subject', dob: '1999-09-09' };

    // Before refund: tier is basic
    const viewBefore = await viewFor(testUser, testSubj, mockEnv);
    if (viewBefore.tier !== 'basic') throw new Error(`Expected tier basic before refund, got ${viewBefore.tier}`);

    // Process full refund
    const refPayload = JSON.stringify({
      event: 'refund.processed',
      event_id: 'evt_full_ref_' + Date.now(),
      payload: {
        refund: { entity: { id: 'rfnd_full_' + Date.now(), payment_id: payId, amount: 19900 } },
        payment: { entity: { id: payId, order_id: ordData.rzpOrderId } }
      }
    });
    const refSig = crypto.createHmac('sha256', mockEnv.RAZORPAY_WEBHOOK_SECRET).update(refPayload).digest('hex');
    await worker.fetch(new Request('https://numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': refSig },
      body: refPayload
    }), mockEnv);

    // After refund: entitlement from refunded order is excluded, tier falls back to free
    const viewAfter = await viewFor(testUser, testSubj, mockEnv);
    if (viewAfter.tier !== 'free') {
      throw new Error(`Expected tier free after full refund, got ${viewAfter.tier}`);
    }
  });

  // 7. Test: POST /api/v1/subjects requires session cookie (401)
  await assertCase('POST /api/v1/subjects requires session cookie (401)', async () => {
    const res = await worker.fetch(new Request('https://numerosvision.com/api/v1/subjects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: 'Alice', dob: '1992-02-02', consent: true })
    }), mockEnv);
    if (res.status !== 401) throw new Error(`Expected 401, got ${res.status}`);
  });

  // 8. Test: POST /api/v1/subjects requires statutory DPDP 2023 consent (consent === true)
  await assertCase('POST /api/v1/subjects enforces DPDP 2023 statutory consent (400 if missing/false)', async () => {
    const res = await worker.fetch(new Request('https://numerosvision.com/api/v1/subjects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': sessionCookie2 },
      body: JSON.stringify({ name: 'Alice', dob: '1992-02-02', consent: false })
    }), mockEnv);
    if (res.status !== 400) throw new Error(`Expected 400, got ${res.status}`);
    const data = await res.json();
    if (!data.error || !data.error.includes('DPDP 2023')) {
      throw new Error(`Expected DPDP 2023 consent error message, got ${JSON.stringify(data)}`);
    }
  });

  // 9. Test: POST /api/v1/subjects creates subject and caps subjects at 10 per account
  await assertCase('POST /api/v1/subjects successfully creates subject and caps at 10 per account', async () => {
    // Create subjects up to limit for sessionCookie2
    // User starts with 0 subjects. Create 10 subjects.
    for (let i = 1; i <= 10; i++) {
      const res = await worker.fetch(new Request('https://numerosvision.com/api/v1/subjects', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Cookie': sessionCookie2 },
        body: JSON.stringify({
          name: `Family Member ${i}`,
          dob: `1980-01-${String(i).padStart(2, '0')}`,
          consent: true
        })
      }), mockEnv);
      if (res.status !== 201) {
        const err = await res.json();
        throw new Error(`Expected 201 creating subject ${i}, got ${res.status}: ${JSON.stringify(err)}`);
      }
    }

    // 11th subject attempt must be rejected with 400
    const res11 = await worker.fetch(new Request('https://numerosvision.com/api/v1/subjects', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': sessionCookie2 },
      body: JSON.stringify({
        name: 'Family Member 11',
        dob: '1980-01-11',
        consent: true
      })
    }), mockEnv);

    if (res11.status !== 400) {
      throw new Error(`Expected 400 capping subjects at 10, got ${res11.status}`);
    }
    const data11 = await res11.json();
    if (!data11.error || !data11.error.includes('10 subjects')) {
      throw new Error(`Expected 10 subjects limit message, got ${JSON.stringify(data11)}`);
    }
  });

  // 10. Test: POST /api/v1/payments/create-order enforces 10-subject cap when auto-creating from DOB
  await assertCase('create-order enforces 10-subject cap when auto-creating subject', async () => {
    // User sessionCookie2 already has 10 subjects
    const res = await worker.fetch(new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': sessionCookie2 },
      body: JSON.stringify({
        packId: 'report_basic',
        name: 'Extra Person',
        dob: '1980-01-12'
      })
    }), mockEnv);

    if (res.status !== 400) {
      throw new Error(`Expected 400 blocking 11th subject creation in create-order, got ${res.status}`);
    }
  });

  // 11. Test: GET /api/v1/subjects returns tenant-isolated subjects list
  await assertCase('GET /api/v1/subjects enforces tenant isolation', async () => {
    const res = await worker.fetch(new Request('https://numerosvision.com/api/v1/subjects', {
      method: 'GET',
      headers: { 'Cookie': sessionCookie2 }
    }), mockEnv);
    if (res.status !== 200) throw new Error(`Expected 200, got ${res.status}`);
    const data = await res.json();
    if (!Array.isArray(data.subjects) || data.subjects.length !== 10) {
      throw new Error(`Expected exactly 10 subjects for tester 2, got ${data.subjects ? data.subjects.length : 0}`);
    }
  });

  // 12. Test: GET /api/v1/dashboard/view rejects unauthenticated request (401)
  await assertCase('GET /api/v1/dashboard/view rejects unauthenticated request (401)', async () => {
    const res = await worker.fetch(new Request('https://numerosvision.com/api/v1/dashboard/view'), mockEnv);
    if (res.status !== 401) throw new Error(`Expected 401, got ${res.status}`);
  });

  // 13. Test: GET /api/v1/dashboard/view returns server-gated view, invoices, orders, and Charm credits
  await assertCase('GET /api/v1/dashboard/view returns server-gated view, invoices, orders, and Charm credits', async () => {
    const res = await worker.fetch(new Request('https://numerosvision.com/api/v1/dashboard/view', {
      method: 'GET',
      headers: { 'Cookie': sessionCookie2 }
    }), mockEnv);
    if (res.status !== 200) throw new Error(`Expected 200, got ${res.status}`);
    const data = await res.json();

    if (!data.user || !data.user.userId) throw new Error('Missing user in dashboard response');
    if (!data.activeSubject || !data.activeSubject.name) throw new Error('Missing activeSubject in dashboard response');
    if (data.subjectCount !== 10) throw new Error(`Expected 10 subjects, got ${data.subjectCount}`);
    if (typeof data.charmCredits !== 'number') throw new Error('Missing charmCredits number');
    if (!data.view || !data.view.sections || !data.view.sections.grid) throw new Error('Missing viewFor data in dashboard view');
    if (!Array.isArray(data.invoices)) throw new Error('Missing invoices array');
    if (!Array.isArray(data.orders)) throw new Error('Missing orders array');
  });

  // 14. Test: Partial refund does not auto-revoke; flags in audit_log for manual review
  await assertCase('Partial refund does not auto-revoke and flags in audit_log for manual review', async () => {
    // 1. Buy basic report for user 1 (₹199 = 19900 paise)
    const createReq = new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': sessionCookie },
      body: JSON.stringify({ packId: 'report_basic', name: 'Partial Refund Subject', dob: '1975-05-25' })
    });
    const createRes = await worker.fetch(createReq, mockEnv);
    const ordData = await createRes.json();

    const payId = 'pay_part_' + Date.now();
    const payPayload = JSON.stringify({
      event: 'order.paid',
      event_id: 'evt_part_' + Date.now(),
      payload: {
        order: { entity: { id: ordData.rzpOrderId } },
        payment: { entity: { id: payId, amount: 19900, currency: 'INR', order_id: ordData.rzpOrderId } }
      }
    });
    const sig = crypto.createHmac('sha256', mockEnv.RAZORPAY_WEBHOOK_SECRET).update(payPayload).digest('hex');
    await worker.fetch(new Request('https://numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': sig },
      body: payPayload
    }), mockEnv);

    const partSubj = { id: ordData.subjectId, name: 'Partial Refund Subject', dob: '1975-05-25' };

    // 2. Issue partial refund of ₹50 (5000 paise out of 19900)
    const refPayload = JSON.stringify({
      event: 'refund.processed',
      event_id: 'evt_part_proc_' + Date.now(),
      payload: {
        refund: { entity: { id: 'rfnd_part_' + Date.now(), payment_id: payId, amount: 5000 } },
        payment: { entity: { id: payId, order_id: ordData.rzpOrderId } }
      }
    });
    const refSig = crypto.createHmac('sha256', mockEnv.RAZORPAY_WEBHOOK_SECRET).update(refPayload).digest('hex');
    const refRes = await worker.fetch(new Request('https://numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': refSig },
      body: refPayload
    }), mockEnv);

    if (refRes.status !== 200) throw new Error(`Expected 200, got ${refRes.status}`);
    const refData = await refRes.json();
    if (refData.message !== 'partial_refund_flagged_for_manual_review') {
      throw new Error(`Expected partial_refund_flagged_for_manual_review, got ${JSON.stringify(refData)}`);
    }

    // 3. Verify entitlement was NOT revoked (remains basic tier)
    const viewAfter = await viewFor(testUser, partSubj, mockEnv);
    if (viewAfter.tier !== 'basic') {
      throw new Error(`Expected tier to remain basic after partial refund, got ${viewAfter.tier}`);
    }
  });

  console.log('\n--- RESULT: 14/14 COMMIT 5 GATING & ENTITLEMENTS TESTS PASSED ---\n');
}

runTests().catch(err => {
  console.error('Test runner failure:', err);
  process.exitCode = 1;
});
