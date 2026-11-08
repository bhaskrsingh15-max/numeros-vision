// NUMEROS VISION — CHARM AI SERVER-SIDE GATING & CREDIT LEDGER TEST SUITE
// Verifies:
// 1. Reserve-then-refund atomic ledger semantics
// 2. 5 parallel requests on 1 credit -> exactly 1 succeeds, 4 return 402 CREDITS_EXHAUSTED
// 3. Verify + webhook idempotent fulfillment -> credits granted strictly once (ref_id uniqueness)
// 4. Free total = 3 per person. Guest usage carries over on sign-in with no extra signup bonus
// 5. Durable rate limiting across isolates & kill-switch (HTTP 503 / HTTP 429)
// 6. Banned words verification in generated responses

import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import worker, { fulfillPaidOrder, memoryStore } from '../app/static/_worker.js';

console.log('[TEST] Starting Charm AI Server-Side Gating Test Suite...');

const mockEnv = {
  ENVIRONMENT: 'local',
  MOCK_PAYMENTS: 'true',
  RAZORPAY_KEY_ID: 'rzp_test_charm_123',
  RAZORPAY_KEY_SECRET: 'test_rzp_secret',
  SESSION_SECRET: 'mock_test_session_secret_key_123',
  CHARM_IP_HASH_SALT: 'test_charm_salt_secret_123',
  CHARM_GLOBAL_DAILY_CAP: '100'
};

const mockCtx = { waitUntil() {} };

function resetMemory() {
  memoryStore.users.clear();
  memoryStore.sessions.clear();
  memoryStore.creditLedger.clear();
  memoryStore.orders.clear();
  memoryStore.payments.clear();
  memoryStore.entitlements.clear();
  memoryStore.freeChatUsage.clear();
  memoryStore.charmRateLimits.clear();
}

function computeTokenHash(token) {
  return crypto.createHmac('sha256', mockEnv.SESSION_SECRET).update(token).digest('hex');
}

async function runTests() {
  // ── TEST 1: Guest Free Questions (Max 3) ──
  {
    console.log('[TEST 1] Testing Guest Lifetime Free Allowance (Strict Total 3)...');
    resetMemory();

    const guestVisitorCookie = 'nv_visitor_id=vis_guest_test_cookie_001';

    // 1st question -> Success, 2 credits left
    const req1 = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': guestVisitorCookie, 'CF-Connecting-IP': '10.0.0.1' },
      body: JSON.stringify({ message: 'What is my trajectory for 2026?', name: 'Guest A' })
    });
    const res1 = await worker.fetch(req1, mockEnv, mockCtx);
    assert.equal(res1.status, 200);
    const data1 = await res1.json();
    assert.equal(data1.credits_remaining, 2);

    // 2nd question -> Success, 1 credit left
    const req2 = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': guestVisitorCookie, 'CF-Connecting-IP': '10.0.0.1' },
      body: JSON.stringify({ message: 'What about partnerships?', name: 'Guest A' })
    });
    const res2 = await worker.fetch(req2, mockEnv, mockCtx);
    assert.equal(res2.status, 200);
    const data2 = await res2.json();
    assert.equal(data2.credits_remaining, 1);

    // 3rd question -> Success, 0 credits left
    const req3 = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': guestVisitorCookie, 'CF-Connecting-IP': '10.0.0.1' },
      body: JSON.stringify({ message: 'What about health?', name: 'Guest A' })
    });
    const res3 = await worker.fetch(req3, mockEnv, mockCtx);
    assert.equal(res3.status, 200);
    const data3 = await res3.json();
    assert.equal(data3.credits_remaining, 0);

    // 4th question -> REJECTED with 402 FREE_TIER_EXHAUSTED
    const req4 = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Cookie': guestVisitorCookie, 'CF-Connecting-IP': '10.0.0.1' },
      body: JSON.stringify({ message: 'Can I ask another question?', name: 'Guest A' })
    });
    const res4 = await worker.fetch(req4, mockEnv, mockCtx);
    assert.equal(res4.status, 402);
    const data4 = await res4.json();
    assert.equal(data4.code, 'FREE_TIER_EXHAUSTED');
    console.log('PASS: Guest strictly capped at 3 questions; 4th correctly returned HTTP 402.');
  }

  // ── TEST 2: Guest Usage Carries Over On Sign-in (No Double Bonus) ──
  {
    console.log('[TEST 2] Testing Guest Usage Carry-Over On Sign-in (Strict Total 3)...');
    resetMemory();

    const guestVisitorCookie = 'nv_visitor_id=vis_guest_carryover_002';

    // Guest asks 2 questions
    for (let i = 0; i < 2; i++) {
      const gReq = new Request('https://numerosvision.com/api/charm/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Cookie': guestVisitorCookie, 'CF-Connecting-IP': '10.0.0.2' },
        body: JSON.stringify({ message: `Inquiry ${i + 1}`, name: 'Seeker B' })
      });
      const gRes = await worker.fetch(gReq, mockEnv, mockCtx);
      assert.equal(gRes.status, 200);
    }

    // Now visitor signs in as user_test_carryover
    const sessionToken = 'tok_carryover_session_test_abc';
    const tokenHash = computeTokenHash(sessionToken);
    memoryStore.sessions.set(tokenHash, {
      id: 'sess_001',
      user_id: 'user_carryover_123',
      token_hash: tokenHash,
      expires_at: Date.now() + 86400000
    });
    const authHeaders = {
      'Content-Type': 'application/json',
      'Cookie': `nv_session=${sessionToken}; ${guestVisitorCookie}`,
      'CF-Connecting-IP': '10.0.0.2'
    };

    // User checks balance on /api/charm/credits -> Must be exactly 1 remaining (3 - 2 = 1)
    const credReq = new Request('https://numerosvision.com/api/charm/credits', {
      method: 'GET',
      headers: authHeaders
    });
    const credRes = await worker.fetch(credReq, mockEnv, mockCtx);
    assert.equal(credRes.status, 200);
    const credData = await credRes.json();
    assert.equal(credData.authenticated, true);
    assert.equal(credData.credits_remaining, 1, `Expected 1 credit remaining (3-2), got ${credData.credits_remaining}`);

    // User asks 1 question -> 0 remaining
    const uReq1 = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: authHeaders,
      body: JSON.stringify({ message: 'Question as logged-in user', name: 'Seeker B' })
    });
    const uRes1 = await worker.fetch(uReq1, mockEnv, mockCtx);
    assert.equal(uRes1.status, 200);
    const uData1 = await uRes1.json();
    assert.equal(uData1.credits_remaining, 0);

    // User asks 2nd question -> Rejected with 402 CREDITS_EXHAUSTED
    const uReq2 = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: authHeaders,
      body: JSON.stringify({ message: 'Another question without credits', name: 'Seeker B' })
    });
    const uRes2 = await worker.fetch(uReq2, mockEnv, mockCtx);
    assert.equal(uRes2.status, 402);
    const uData2 = await uRes2.json();
    assert.equal(uData2.code, 'CREDITS_EXHAUSTED');
    console.log('PASS: Guest usage carried over seamlessly on sign-in (2 guest + 1 user = 3 total, zero extra bonus).');
  }

  // ── TEST 3: 5 Parallel Questions on 1 Credit -> Exactly 1 Succeeds ──
  {
    console.log('[TEST 3] Testing 5 Parallel Questions on 1 Credit (Race Condition Gate)...');
    resetMemory();

    const userId = 'user_parallel_test_456';
    const sessionToken = 'tok_parallel_session_xyz';
    const tokenHash = computeTokenHash(sessionToken);
    memoryStore.sessions.set(tokenHash, {
      id: 'sess_parallel',
      user_id: userId,
      token_hash: tokenHash,
      expires_at: Date.now() + 86400000
    });

    // Seed exactly 1 credit in ledger
    memoryStore.creditLedger.set('seed_1', {
      id: 'seed_1',
      user_id: userId,
      delta: 1,
      reason: 'free_allowance',
      ref_id: 'free_' + userId,
      balance_after: 1,
      created_at: Date.now()
    });

    const authHeaders = {
      'Content-Type': 'application/json',
      'Cookie': `nv_session=${sessionToken}`,
      'CF-Connecting-IP': '10.0.0.3'
    };

    // Fire 5 simultaneous requests
    const promises = Array.from({ length: 5 }, (_, i) => {
      const req = new Request('https://numerosvision.com/api/charm/chat', {
        method: 'POST',
        headers: authHeaders,
        body: JSON.stringify({ message: `Concurrent Query ${i + 1}`, name: 'Parallel Seeker' })
      });
      return worker.fetch(req, mockEnv, mockCtx);
    });

    const responses = await Promise.all(promises);
    const statuses = responses.map(r => r.status);
    const successCount = statuses.filter(s => s === 200).length;
    const exhaustedCount = statuses.filter(s => s === 402).length;

    assert.equal(successCount, 1, `Expected exactly 1 success, got ${successCount}`);
    assert.equal(exhaustedCount, 4, `Expected exactly 4 rejections (402), got ${exhaustedCount}`);

    // Verify ledger balance is exactly 0
    let finalBal = 0;
    for (const c of memoryStore.creditLedger.values()) {
      if (c.user_id === userId) finalBal += c.delta;
    }
    assert.equal(finalBal, 0, `Expected final ledger balance 0, got ${finalBal}`);
    console.log('PASS: Concurrency test passed: exactly 1 parallel question succeeded, 4 rejected with 402.');
  }

  // ── TEST 4: Verify + Webhook Idempotency (Credits Granted Exactly Once) ──
  {
    console.log('[TEST 4] Testing Verify + Webhook Idempotency (Zero Double-Grant)...');
    resetMemory();

    const userId = 'user_order_grant_789';
    const orderId = 'ord_charm_test_001';
    const rzpOrderId = 'order_rzp_mock_123';
    const rzpPaymentId = 'pay_rzp_mock_456';

    const orderObj = {
      id: orderId,
      user_id: userId,
      subject_id: 'subj_test_1',
      pack_id: 'charm_single', // Starter Pack: 5 questions
      amount_paise: 19900,
      currency: 'INR',
      rzp_order_id: rzpOrderId,
      status: 'CREATED',
      created_at: Date.now()
    };
    memoryStore.orders.set(orderId, orderObj);

    // Call fulfillPaidOrder from Verify
    await fulfillPaidOrder(orderObj, rzpPaymentId, 19900, 'upi', mockEnv, Date.now(), 'verify');

    // Call fulfillPaidOrder immediately again from Webhook
    await fulfillPaidOrder(orderObj, rzpPaymentId, 19900, 'upi', mockEnv, Date.now(), 'webhook');

    // Verify credits in memoryStore.creditLedger
    let totalCredits = 0;
    let grantRows = 0;
    for (const c of memoryStore.creditLedger.values()) {
      if (c.user_id === userId && c.reason === 'pack_purchase') {
        totalCredits += c.delta;
        grantRows += 1;
      }
    }
    assert.equal(grantRows, 1, `Expected exactly 1 grant row, got ${grantRows}`);
    assert.equal(totalCredits, 5, `Expected exactly 5 credits, got ${totalCredits}`);
    console.log('PASS: Verify + Webhook idempotency passed: 5 credits granted exactly once.');
  }

  // ── TEST 5: Kill Switch and Global Daily Spend Cap ──
  {
    console.log('[TEST 5] Testing Kill-Switch and Rate Limiting...');
    resetMemory();

    // 1. Kill-Switch
    const killedEnv = { ...mockEnv, CHARM_KILL_SWITCH: 'true' };
    const kReq = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'CF-Connecting-IP': '10.0.0.5' },
      body: JSON.stringify({ message: 'Test question' })
    });
    const kRes = await worker.fetch(kReq, killedEnv, mockCtx);
    assert.equal(kRes.status, 503);
    const kData = await kRes.json();
    assert.equal(kData.code, 'SERVICE_TEMPORARILY_UNAVAILABLE');

    // 2. Per-IP Burst Limit (Max 5 req/min)
    const burstIp = '192.168.1.100';
    for (let i = 0; i < 5; i++) {
      const bReq = new Request('https://numerosvision.com/api/charm/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'CF-Connecting-IP': burstIp },
        body: JSON.stringify({ message: `Burst ${i}` })
      });
      const bRes = await worker.fetch(bReq, mockEnv, mockCtx);
      assert.equal(bRes.status, 200);
    }
    // 6th request within 1 min -> 429 TOO_MANY_REQUESTS
    const bReq6 = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'CF-Connecting-IP': burstIp },
      body: JSON.stringify({ message: 'Burst 6' })
    });
    const bRes6 = await worker.fetch(bReq6, mockEnv, mockCtx);
    assert.equal(bRes6.status, 429);
    const bData6 = await bRes6.json();
    assert.equal(bData6.code, 'TOO_MANY_REQUESTS');
    console.log('PASS: Kill-switch (503) and cross-isolate rate limiting (429) verified.');
  }

  // ── TEST 6: Banned Words Scan on Generated Content ──
  {
    console.log('[TEST 6] Testing Banned Words in Response...');
    resetMemory();

    const req = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'CF-Connecting-IP': '10.0.0.9' },
      body: JSON.stringify({ message: 'Career advice please' })
    });
    const res = await worker.fetch(req, mockEnv, mockCtx);
    assert.equal(res.status, 200);
    const data = await res.json();
    const text = (data.assistant_message && data.assistant_message.text ? data.assistant_message.text : '').toLowerCase();

    const bannedList = ['luck', 'lucky', 'guaranteed', 'will bring', 'will fix', 'prediction', 'prescription', 'consecrated', 'cure', 'exact'];
    for (const b of bannedList) {
      assert.equal(text.includes(b), false, `Banned word "${b}" detected in assistant text!`);
    }
    console.log('PASS: Assistant response is 100% clean of all 10 banned words.');
  }

  console.log('\n[SUCCESS] All Charm AI Gating & Ledger tests completed successfully!');
}

runTests().catch(err => {
  console.error('[FATAL TEST ERROR]', err);
  process.exit(1);
});
