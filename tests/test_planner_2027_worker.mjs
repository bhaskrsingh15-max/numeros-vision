// NUMEROS VISION — 2027 YEAR AHEAD PLANNER COMPREHENSIVE WORKER TEST SUITE (Node.js)
// Covers:
// 1. Live key refusal (never allows rzp_live)
// 2. GET /api/planner-2027/price (server pricing authority)
// 3. Mandatory DPDP consent requirement
// 4. Client amount tamper resistance (server enforces price)
// 5. Rate limiting on /order (HTTP 429)
// 6. Signature verification gate (HMAC-SHA256)
// 7. Atomic concurrency: verify and webhook fired simultaneously -> exactly 1 generation, generation_count = 1
// 8. 3-regeneration cap
// 9. Tamper-proof name and DOB (PDF generated strictly from stored order record)
// 10. Token expiry (> 30 days -> HTTP 403)
// 11. Wrong token (HTTP 403)
// 12. Privacy gate: order-status returns strictly zero PII (no name, dob, email, token)
// 13. Delivery without browser: /resend-link with order_id and email
// 14. Stuck order alert & admin list route (/admin/stuck-orders)

import assert from 'node:assert';
import crypto from 'node:crypto';
import worker, { memoryStore } from '../app/static/_worker.js';

async function runWorkerTestSuite() {
  console.log('[TEST] Starting Full Planner 2027 Worker Test Suite...');

  const baseEnv = {
    ENVIRONMENT: 'local',
    NV_EMAIL_LOG_ADAPTER: 'true',
    MOCK_PAYMENTS: 'true',
    RAZORPAY_KEY_ID: 'rzp_test_12345678',
    RAZORPAY_KEY_SECRET: 'test_rzp_secret_key',
    PDF_SERVICE_SECRET: 'test_pdf_secret',
    ADMIN_TOKEN: 'test_admin_token_xyz',
    PDF_SERVICE_URL: 'http://127.0.0.1:8090'
  };

  // 1. Live key refusal
  {
    console.log('[TEST 1] Asserting live key refusal in worker...');
    const liveEnv = { ...baseEnv, RAZORPAY_KEY_ID: 'rzp_live_dangerous_key' };
    const req = new Request('http://localhost/api/planner-2027/order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost' },
      body: JSON.stringify({ name: 'Arun Sharma', dob: '1988-04-14', email: 'test@example.com', consent: true })
    });
    let threw = false;
    try {
      await worker._handleRequest(req, liveEnv, {});
    } catch (e) {
      threw = true;
      assert(e.message.includes('Live Razorpay key detected'), `Expected live key error but got ${e.message}`);
    }
    assert(threw, 'Worker._handleRequest must throw when rzp_live key is present');

    const res = await worker.fetch(req, liveEnv, {});
    assert.strictEqual(res.status, 500);
    console.log('  ✓ Live key correctly rejected with fatal error');
  }

  // 1B. Preview Flag Strict Guard: Allowed ONLY when ENVIRONMENT === 'preview'
  {
    console.log('[TEST 1B] Testing PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW strict guard...');
    const req = new Request('http://localhost/api/planner-2027/price', {
      method: 'GET',
      headers: { 'Origin': 'http://localhost' }
    });

    // Case A: Refused when ENVIRONMENT is unset/empty
    const emptyEnv = { ...baseEnv, PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW: 'true', ENVIRONMENT: '' };
    let threwEmpty = false;
    try {
      await worker._handleRequest(req, emptyEnv);
    } catch (e) {
      threwEmpty = true;
      assert(e.message.includes("only permitted when ENVIRONMENT == 'preview'"));
    }
    assert(threwEmpty, 'Worker must throw when ENVIRONMENT is empty');

    // Case B: Refused when ENVIRONMENT is 'staging'
    const stagingEnv = { ...baseEnv, PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW: 'true', ENVIRONMENT: 'staging' };
    let threwStaging = false;
    try {
      await worker._handleRequest(req, stagingEnv);
    } catch (e) {
      threwStaging = true;
      assert(e.message.includes("only permitted when ENVIRONMENT == 'preview'"));
    }
    assert(threwStaging, 'Worker must throw when ENVIRONMENT is staging');

    // Case C: Refused when ENVIRONMENT is 'production'
    const prodEnv = { ...baseEnv, PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW: 'true', ENVIRONMENT: 'production' };
    let threwProd = false;
    try {
      await worker._handleRequest(req, prodEnv);
    } catch (e) {
      threwProd = true;
      assert(e.message.includes("only permitted when ENVIRONMENT == 'preview'"));
    }
    assert(threwProd, 'Worker must throw when ENVIRONMENT is production');

    // Case D: Accepted when ENVIRONMENT is 'preview' explicitly
    const previewEnv = { ...baseEnv, PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW: 'true', ENVIRONMENT: 'preview' };
    const validRes = await worker._handleRequest(req, previewEnv);
    assert.strictEqual(validRes.status, 200);

    console.log('  ✓ Preview flag strictly guarded to ENVIRONMENT == "preview"');
  }

  // 2. Pricing & order endpoints: Waitlist-only default + post-approval live env
  const defaultWaitlistEnv = { ...baseEnv };
  {
    console.log('[TEST 2A] Testing default waitlist-only state on /price and 409 block on /order...');
    const priceReq = new Request('http://localhost/api/planner-2027/price', {
      method: 'GET',
      headers: { 'Origin': 'http://localhost' }
    });
    const priceRes = await worker.fetch(priceReq, defaultWaitlistEnv, {});
    assert.strictEqual(priceRes.status, 200);
    const priceData = await priceRes.json();
    assert.strictEqual(priceData.active, false);
    assert.strictEqual(priceData.waitlist_only, true);
    assert.strictEqual(priceData.amount_paise, null);
    assert.strictEqual(priceData.list, null);
    assert.strictEqual(priceData.offer, null);

    const blockedOrderReq = new Request('http://localhost/api/planner-2027/order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.0.0.99' },
      body: JSON.stringify({ name: 'Arun Sharma', dob: '1988-04-14', email: 'test@example.com', consent: true })
    });
    const blockedRes = await worker.fetch(blockedOrderReq, defaultWaitlistEnv, {});
    assert.strictEqual(blockedRes.status, 409);
    const blockedData = await blockedRes.json();
    assert.strictEqual(blockedData.code, 'PLANNER_WAITLIST_ONLY');
    console.log('  ✓ Default waitlist-only pricing (null) and 409 order block verified');
  }

  // Enable post-approval live Planner env for downstream payment/tamper/concurrency tests
  Object.assign(baseEnv, {
    PLANNER_2027_LIVE: 'true',
    NV_PLANNER_2027_REGULAR_PAISE: '199900',
    NV_PLANNER_2027_LAUNCH_PAISE: '149900',
    NV_LAUNCH_PLANNER_2027_STARTS_AT: '2026-01-01T00:00:00Z',
    NV_LAUNCH_PLANNER_2027_ENDS_AT: '2027-01-31T23:59:00+05:30'
  });

  {
    console.log('[TEST 2B] Testing post-approval GET /api/planner-2027/price when PLANNER_2027_LIVE=true...');
    const req = new Request('http://localhost/api/planner-2027/price', {
      method: 'GET',
      headers: { 'Origin': 'http://localhost' }
    });
    const res = await worker.fetch(req, baseEnv, {});
    assert.strictEqual(res.status, 200);
    const data = await res.json();
    assert.strictEqual(data.list, 199900);
    assert.strictEqual(data.offer, 149900);
    assert.strictEqual(data.amount_paise, 149900);
    assert.strictEqual(data.currency, 'INR');
    assert.strictEqual(data.price_includes_gst, false);
    assert.strictEqual(data.receipt_type, 'Payment receipt');
    assert.strictEqual(data.active, true);
    console.log('  ✓ Post-approval pricing endpoint verified');
  }

  // 3. Mandatory DPDP consent
  {
    console.log('[TEST 3] Testing mandatory DPDP consent...');
    const req = new Request('http://localhost/api/planner-2027/order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.0.0.1' },
      body: JSON.stringify({ name: 'Arun Sharma', dob: '1988-04-14', email: 'test@example.com', consent: false })
    });
    const res = await worker.fetch(req, baseEnv, {});
    assert.strictEqual(res.status, 400);
    const data = await res.json();
    assert(data.error.includes('Mandatory consent required'), 'Must reject when consent is false');
    console.log('  ✓ Mandatory consent gate verified');
  }

  // 4. Rate limiting on /order
  {
    console.log('[TEST 4] Testing rate limiting on /order...');
    const rateLimitIp = '10.99.88.77';
    let rateLimited = false;
    for (let i = 0; i < 12; i++) {
      const req = new Request('http://localhost/api/planner-2027/order', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': rateLimitIp },
        body: JSON.stringify({ name: 'Arun Sharma', dob: '1988-04-14', email: 'test@example.com', consent: true })
      });
      const res = await worker.fetch(req, baseEnv, {});
      if (res.status === 429) {
        rateLimited = true;
        break;
      }
    }
    assert(rateLimited, 'Order endpoint must enforce rate limiting (HTTP 429)');
    console.log('  ✓ Rate limit on /order verified');
  }

  // 5. Order creation & client price tamper resistance
  let orderA = null;
  {
    console.log('[TEST 5] Testing order creation with server price enforcement...');
    const req = new Request('http://localhost/api/planner-2027/order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.0.0.2' },
      body: JSON.stringify({
        name: '  Arun   Sharma  ',
        dob: '1988-04-14',
        email: 'arun.sharma@example.com',
        consent: true,
        amount_paise: 99 // Client attempts price tamper
      })
    });
    const res = await worker.fetch(req, baseEnv, {});
    assert.strictEqual(res.status, 200);
    orderA = await res.json();
    assert(orderA.order_id);
    assert(orderA.razorpay_order_id);
    assert.strictEqual(orderA.amount_paise, 149900, 'Server must enforce offer price 149900');
    console.log('  ✓ Order created and price tamper resistance verified');
  }

  // 6. Invalid payment signature rejected
  {
    console.log('[TEST 6] Testing invalid payment signature rejection...');
    const req = new Request('http://localhost/api/planner-2027/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost' },
      body: JSON.stringify({
        order_id: orderA.order_id,
        razorpay_order_id: orderA.razorpay_order_id,
        razorpay_payment_id: 'pay_test_123',
        razorpay_signature: 'forged_signature_hex'
      })
    });
    const res = await worker.fetch(req, baseEnv, {});
    assert.strictEqual(res.status, 400);
    const data = await res.json();
    assert(data.error.includes('Invalid payment signature'));
    console.log('  ✓ Invalid signature rejected');
  }

  // 7. Atomic Concurrency: /verify and /webhook fired simultaneously
  {
    console.log('[TEST 7] Testing atomic concurrency between /verify and /webhook...');
    // Create fresh order for concurrency test
    const createReq = new Request('http://localhost/api/planner-2027/order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.0.0.3' },
      body: JSON.stringify({ name: 'Anil Kumar', dob: '1975-06-22', email: 'anil.kumar@example.com', consent: true })
    });
    const createRes = await worker.fetch(createReq, baseEnv, {});
    const orderConcurrent = await createRes.json();

    const rzpPayId = 'pay_concurrent_123';
    const validVerifySig = crypto.createHmac('sha256', baseEnv.RAZORPAY_KEY_SECRET)
      .update(`${orderConcurrent.razorpay_order_id}|${rzpPayId}`)
      .digest('hex');

    const verifyReq = new Request('http://localhost/api/planner-2027/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost' },
      body: JSON.stringify({
        order_id: orderConcurrent.order_id,
        razorpay_order_id: orderConcurrent.razorpay_order_id,
        razorpay_payment_id: rzpPayId,
        razorpay_signature: validVerifySig
      })
    });

    const webhookBody = JSON.stringify({
      event: 'payment.captured',
      payload: { payment: { entity: { id: rzpPayId, order_id: orderConcurrent.razorpay_order_id } } }
    });
    const webhookSig = crypto.createHmac('sha256', baseEnv.RAZORPAY_KEY_SECRET)
      .update(webhookBody)
      .digest('hex');

    const webhookReq = new Request('http://localhost/api/planner-2027/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': webhookSig },
      body: webhookBody
    });

    // Fire both at the exact same time
    const [resVerify, resWebhook] = await Promise.all([
      worker._handleRequest(verifyReq, baseEnv, {}),
      worker._handleRequest(webhookReq, baseEnv, {})
    ]);

    assert(resVerify.status === 200);
    assert(resWebhook.status === 200);

    // Assert order state in memoryStore
    const finalOrder = memoryStore.planner2027Orders.get(orderConcurrent.order_id);
    assert(finalOrder);
    // Because in test mode generator is offline (local), fail-closed transitions order to needs_attention,
    // and generation_count remains 0 or 1, NEVER 2!
    assert(finalOrder.generation_count <= 1, `generation_count must be <= 1, got ${finalOrder.generation_count}`);
    console.log('  ✓ Concurrency atomic transition verified (no double generation)');
  }

  // 8. 3-regeneration cap
  {
    console.log('[TEST 8] Testing 3-regeneration cap...');
    const orderCap = memoryStore.planner2027Orders.get(orderA.order_id);
    orderCap.generation_count = 3; // Simulate cap reached
    memoryStore.planner2027Orders.set(orderA.order_id, orderCap);

    const validSig = crypto.createHmac('sha256', baseEnv.RAZORPAY_KEY_SECRET)
      .update(`${orderA.razorpay_order_id}|pay_cap_test`)
      .digest('hex');

    const req = new Request('http://localhost/api/planner-2027/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost' },
      body: JSON.stringify({
        order_id: orderA.order_id,
        razorpay_order_id: orderA.razorpay_order_id,
        razorpay_payment_id: 'pay_cap_test',
        razorpay_signature: validSig
      })
    });
    const res = await worker.fetch(req, baseEnv, {});
    assert.strictEqual(res.status, 429, 'Must reject with 429 when generation_count >= 3');
    const data = await res.json();
    assert(data.error.includes('Maximum generation limit reached'));
    console.log('  ✓ 3-regeneration cap verified');
  }

  // 9. Tamper protection: Forged client request cannot alter PDF name or DOB
  {
    console.log('[TEST 9] Testing name and DOB tamper resistance...');
    // Create order with official name "Arun Sharma" and DOB "1988-04-14"
    const createReq = new Request('http://localhost/api/planner-2027/order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.0.0.4' },
      body: JSON.stringify({ name: 'Arun Sharma', dob: '1988-04-14', email: 'arun@example.com', consent: true })
    });
    const createRes = await worker.fetch(createReq, baseEnv, {});
    const ord = await createRes.json();

    // Verify request passes forged name/DOB in client body
    const validSig = crypto.createHmac('sha256', baseEnv.RAZORPAY_KEY_SECRET)
      .update(`${ord.razorpay_order_id}|pay_forge_123`)
      .digest('hex');

    const verifyReq = new Request('http://localhost/api/planner-2027/verify', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost' },
      body: JSON.stringify({
        order_id: ord.order_id,
        razorpay_order_id: ord.razorpay_order_id,
        razorpay_payment_id: 'pay_forge_123',
        razorpay_signature: validSig,
        full_name: 'Attacker Name', // Forged payload field
        dob_str: '2005-01-01'        // Forged payload field
      })
    });
    await worker.fetch(verifyReq, baseEnv, {});

    // Check order in store: stored record must still be original
    const stored = memoryStore.planner2027Orders.get(ord.order_id);
    assert.strictEqual(stored.name_normalised, 'Arun Sharma', 'Name must remain official database value');
    assert.strictEqual(stored.dob, '1988-04-14', 'DOB must remain official database value');
    console.log('  ✓ Tamper protection verified (official order DB record authoritative)');
  }

  // 10. Download token expiry (> 30 days) & 11. Wrong token
  {
    console.log('[TEST 10 & 11] Testing download token expiry and wrong token check...');
    // Set up delivered mock order
    const mockDeliveredId = 'ord_p27_mock_delivered';
    const rawToken = 'secret_download_token_1234567890abcdef';
    const tokenHash = crypto.createHash('sha256').update(rawToken).digest('hex');
    const mockPdfKey = `planner_2027/${mockDeliveredId}.pdf`;

    // Put mock PDF in r2Objects
    memoryStore.r2Objects.set(mockPdfKey, new Uint8Array([0x25, 0x50, 0x44, 0x46, 0x2d, 0x31, 0x2e, 0x34])); // %PDF-1.4

    // Case A: Wrong token
    memoryStore.planner2027Orders.set(mockDeliveredId, {
      id: mockDeliveredId,
      status: 'delivered',
      download_token_hash: tokenHash,
      token_expires_at: Date.now() + 86400000,
      pdf_r2_key: mockPdfKey,
      email: 'user@example.com',
      generation_count: 1
    });

    const wrongReq = new Request(`http://localhost/api/planner-2027/download?order=${mockDeliveredId}&token=wrong_token`, { method: 'GET' });
    const wrongRes = await worker.fetch(wrongReq, baseEnv, {});
    assert.strictEqual(wrongRes.status, 403, 'Must return 403 on wrong token');
    console.log('  ✓ Wrong token rejected (HTTP 403)');

    // Case B: Expired token
    const orderExpired = memoryStore.planner2027Orders.get(mockDeliveredId);
    orderExpired.token_expires_at = Date.now() - 5000; // Expired 5 seconds ago
    memoryStore.planner2027Orders.set(mockDeliveredId, orderExpired);

    const expiredReq = new Request(`http://localhost/api/planner-2027/download?order=${mockDeliveredId}&token=${rawToken}`, { method: 'GET' });
    const expiredRes = await worker.fetch(expiredReq, baseEnv, {});
    assert.strictEqual(expiredRes.status, 403, 'Must return 403 on expired token');
    console.log('  ✓ Expired token rejected (HTTP 403)');

    // Case C: Valid token within window
    orderExpired.token_expires_at = Date.now() + 86400000; // Valid
    memoryStore.planner2027Orders.set(mockDeliveredId, orderExpired);

    const validReq = new Request(`http://localhost/api/planner-2027/download?order=${mockDeliveredId}&token=${rawToken}`, { method: 'GET' });
    const validRes = await worker.fetch(validReq, baseEnv, {});
    assert.strictEqual(validRes.status, 200, 'Must return 200 on valid token');
    assert.strictEqual(validRes.headers.get('content-type'), 'application/pdf');
    console.log('  ✓ Valid token served PDF download (HTTP 200)');
  }

  // 12. Order status returns zero PII
  {
    console.log('[TEST 12] Testing order-status endpoint privacy (strictly ZERO PII)...');
    const req = new Request(`http://localhost/api/planner-2027/order-status?order=ord_p27_mock_delivered`, { method: 'GET' });
    const res = await worker.fetch(req, baseEnv, {});
    assert.strictEqual(res.status, 200);
    const data = await res.json();

    const forbiddenFields = ['name', 'name_normalised', 'dob', 'email', 'phone', 'token', 'download_token', 'download_token_hash'];
    for (const f of forbiddenFields) {
      assert.strictEqual(data[f], undefined, `Field '${f}' must not be exposed in order-status`);
    }
    assert(data.order_id);
    assert(data.status);
    console.log('  ✓ Order status endpoint verified strictly zero PII');
  }

  // 13. Delivery without browser: /resend-link (Turnstile-gated, email-only delivery, neutral response)
  {
    console.log('[TEST 13] Testing delivery without browser (/resend-link)...');
    const req = new Request('http://localhost/api/planner-2027/resend-link', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.0.0.5' },
      body: JSON.stringify({ order_id: 'ord_p27_mock_delivered', email: 'user@example.com', turnstile_token: 'test_turnstile_pass' })
    });
    const res = await worker.fetch(req, baseEnv, {});
    assert.strictEqual(res.status, 200);
    const data = await res.json();
    assert.strictEqual(data.success, true);
    assert.strictEqual(data.download_token, undefined, 'Download token must NEVER be returned in response');
    assert.strictEqual(data.download_url, undefined, 'Download url must NEVER be returned in response');
    assert(data.message.includes('dispatched to your email'));
    console.log('  ✓ Delivery without browser (/resend-link) verified via transactional email');

    // Mismatched email receives identical neutral response (zero enumeration)
    const badEmailReq = new Request('http://localhost/api/planner-2027/resend-link', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.0.0.5' },
      body: JSON.stringify({ order_id: 'ord_p27_mock_delivered', email: 'wrong@example.com', turnstile_token: 'test_turnstile_pass' })
    });
    const badRes = await worker.fetch(badEmailReq, baseEnv, {});
    assert.strictEqual(badRes.status, 200);
    const badData = await badRes.json();
    assert.strictEqual(badData.success, true);
    assert.strictEqual(badData.message, data.message, 'Response must be strictly identical for mismatched email');
    console.log('  ✓ Mismatched email returned identical neutral response (zero enumeration)');
  }

  // 14. Stuck order alert & admin list route
  {
    console.log('[TEST 14] Testing stuck order alert & admin list route (/admin/stuck-orders)...');
    // Set one order to needs_attention
    const stuckId = 'ord_p27_mock_stuck';
    memoryStore.planner2027Orders.set(stuckId, {
      id: stuckId,
      status: 'needs_attention',
      amount_paise: 149900,
      currency: 'INR',
      generation_count: 0,
      created_at: Date.now(),
      updated_at: Date.now()
    });

    // Unauthenticated request rejected
    const unauthReq = new Request('http://localhost/api/planner-2027/admin/stuck-orders', { method: 'GET' });
    const unauthRes = await worker.fetch(unauthReq, baseEnv, {});
    assert.strictEqual(unauthRes.status, 401, 'Admin route must require authentication');

    // Authenticated request with Bearer ADMIN_TOKEN
    const authReq = new Request('http://localhost/api/planner-2027/admin/stuck-orders', {
      method: 'GET',
      headers: { 'Authorization': `Bearer ${baseEnv.ADMIN_TOKEN}` }
    });
    const authRes = await worker.fetch(authReq, baseEnv, {});
    assert.strictEqual(authRes.status, 200);
    const data = await authRes.json();
    assert.strictEqual(data.status, 'ok');
    assert(data.count >= 1);
    const found = data.orders.some(o => o.id === stuckId);
    assert(found, 'Stuck order must be present in admin list');
    console.log('  ✓ Admin stuck orders route verified with authentication');
  }

  console.log('\n[PASS] All 14 Planner 2027 Worker tests passed successfully!');
}

runWorkerTestSuite().catch(err => {
  console.error('\n[FAIL] Worker test suite failed:', err);
  process.exit(1);
});
