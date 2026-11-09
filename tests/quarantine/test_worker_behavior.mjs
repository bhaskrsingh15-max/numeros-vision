/**
 * NUMEROS VISION — WORKER RUNTIME BEHAVIOR TESTS
 * Tests the Cloudflare Pages Edge Worker fetch handler against the 4 critical behaviors:
 * 1. Fake pay_ ID with bad signature returns 400
 * 2. Correctly signed payload passes with 200
 * 3. Missing secret returns 500
 * 4. /reports/ and /static/reports/ return 403
 */

import worker from '../app/static/_worker.js';
import crypto from 'node:crypto';

async function runTests() {
  console.log('--- STARTING WORKER BEHAVIOR TESTS ---\n');
  let passed = 0;
  let total = 0;

  async function assertCase(name, fn) {
    total++;
    try {
      await fn();
      console.log(`✓ PASS: ${name}`);
      passed++;
    } catch (err) {
      console.error(`✗ FAIL: ${name}: ${err.message}`);
    }
  }

  const mockEnv = {
    RAZORPAY_KEY_ID: 'rzp_test_MOCK_ENV_KEY',
    RAZORPAY_KEY_SECRET: 'test_secret_for_local_behavior_suite',
    FAST2SMS_API_KEY: 'test_sms_key',
    ASSETS: {
      fetch: async (req) => new Response('Asset stub', { status: 200 })
    }
  };

  // Test 1: Fake pay_ ID with bad signature returns 400
  await assertCase('Fake pay_ ID with invalid signature returns 400', async () => {
    const req = new Request('https://numerosvision.com/api/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        razorpay_order_id: 'order_12345',
        razorpay_payment_id: 'pay_FAKECREDITCARD99',
        razorpay_signature: 'invalid_bad_signature_hex_1234567890abcdef'
      })
    });
    const res = await worker.fetch(req, mockEnv);
    if (res.status !== 400) {
      throw new Error(`Expected status 400, got ${res.status}`);
    }
    const data = await res.json();
    if (data.status !== 'error') {
      throw new Error(`Expected status error, got ${JSON.stringify(data)}`);
    }
  });

  // Test 2: Correctly signed payload passes with 200 and returns verified
  await assertCase('Correctly signed payload with valid HMAC passes with 200', async () => {
    const orderId = 'order_AUTHENTIC_99';
    const paymentId = 'pay_AUTHENTIC_99';
    const expectedSig = crypto
      .createHmac('sha256', mockEnv.RAZORPAY_KEY_SECRET)
      .update(`${orderId}|${paymentId}`)
      .digest('hex');

    const req = new Request('https://numerosvision.com/api/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        razorpay_order_id: orderId,
        razorpay_payment_id: paymentId,
        razorpay_signature: expectedSig,
        plan: 'report_master',
        customer_email: 'seeker@example.com',
        customer_name: 'Authentic Seeker'
      })
    });
    const res = await worker.fetch(req, mockEnv);
    if (res.status !== 200) {
      const errText = await res.text();
      throw new Error(`Expected status 200, got ${res.status}: ${errText}`);
    }
    const data = await res.json();
    if (data.status !== 'verified') {
      throw new Error(`Expected status verified, got ${JSON.stringify(data)}`);
    }
  });

  // Test 3: Missing secret returns 500
  await assertCase('Missing server secret returns 500', async () => {
    const envNoSecret = { ...mockEnv, RAZORPAY_KEY_SECRET: undefined };
    const req = new Request('https://numerosvision.com/api/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        razorpay_order_id: 'order_test',
        razorpay_payment_id: 'pay_test',
        razorpay_signature: 'sig'
      })
    });
    const res = await worker.fetch(req, envNoSecret);
    if (res.status !== 500) {
      throw new Error(`Expected status 500, got ${res.status}`);
    }
  });

  // Test 4: /reports/ path is blocked and returns 403
  await assertCase('/reports/ URL access is forbidden (403)', async () => {
    const req = new Request('https://numerosvision.com/reports/secret_report.pdf', {
      method: 'GET'
    });
    const res = await worker.fetch(req, mockEnv);
    if (res.status !== 403) {
      throw new Error(`Expected status 403, got ${res.status}`);
    }
  });

  // Test 5: /static/reports/ path is blocked and returns 403
  await assertCase('/static/reports/ URL access is forbidden (403)', async () => {
    const req = new Request('https://numerosvision.com/static/reports/secret_report.pdf', {
      method: 'GET'
    });
    const res = await worker.fetch(req, mockEnv);
    if (res.status !== 403) {
      throw new Error(`Expected status 403, got ${res.status}`);
    }
  });

  // Test 6: /api/v1/reports/generate-pdf returns 403 upgrading
  await assertCase('/api/v1/reports/generate-pdf returns 403 upgrading', async () => {
    const req = new Request('https://numerosvision.com/api/v1/reports/generate-pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ tier: 'premium', name: 'Alexander Vance' })
    });
    const res = await worker.fetch(req, mockEnv);
    if (res.status !== 403) {
      throw new Error(`Expected status 403, got ${res.status}`);
    }
    const data = await res.json();
    if (data.code !== 'REPORT_GENERATION_UPGRADING') {
      throw new Error(`Expected code REPORT_GENERATION_UPGRADING, got ${data.code}`);
    }
  });

  console.log(`\n--- RESULT: ${passed}/${total} WORKER BEHAVIOR TESTS PASSED ---`);
  if (passed !== total) {
    process.exit(1);
  }
}

runTests().catch(err => {
  console.error('Fatal test error:', err);
  process.exit(1);
});
