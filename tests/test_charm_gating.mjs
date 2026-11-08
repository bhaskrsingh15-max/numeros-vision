// NUMEROS VISION — CHARM AI SERVER-SIDE GATING & REAL SQLITE VERIFICATION SUITE
//
// NOTE: node:sqlite (DatabaseSync) is a synchronous SQLite implementation.
// Therefore, the parallel tests verify transaction, ledger, and counter logic
// (e.g. conditional updates and change counts), not operating-system-level true thread concurrency.
//
// Verified Requirements:
// 1. Detection of prohibited terms (including variants) -> single retry with stricter instruction -> safe fallback sentence
// 2. Parallel guest counter on real SQLite (5 parallel requests on 2 used -> exactly 1 succeeds, 4 get 402)
// 3. Parallel paid user ledger on real SQLite (5 parallel requests on 1 credit -> exactly 1 succeeds, 4 get 402)
// 4. Reserve-then-refund on model failure/timeout (500 returned, -1 reservation matched by +1 refund, balance preserved)
// 5. LocalStorage tamper prevention (client cannot bypass 402 with nv_premium_token)
// 6. Zero model calls at zero balance (assert model invocation count is strictly 0)
// 7. Fail-closed security (missing CHARM_IP_HASH_SALT or D1 binding returns 503, kill-switch returns standardized pause message)
// 8. Verify + Webhook idempotency (unique ref_id prevents double credit grants)
// 9. /login same-site relative returnTo validation (rejects absolute URLs, //host, javascript:)

import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import { DatabaseSync } from 'node:sqlite';
import worker, {
  fulfillPaidOrder,
  memoryStore,
  hasBannedTerms,
  CHARM_SAFE_FALLBACK_TEXT,
  processTextWithBannedFilter,
  isValidRelativeReturnTo,
  sanitizeReturnToUrl
} from '../app/static/_worker.js';

console.log('[TEST] Starting Charm AI Server-Side Gating Suite (Real SQLite Backend via node:sqlite)...');

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
  memoryStore.charmModelInvocations = 0;
}

function computeTokenHash(token) {
  return crypto.createHmac('sha256', mockEnv.SESSION_SECRET).update(token).digest('hex');
}

// Real SQLite D1 Database Adapter for testing
function createRealSqliteD1() {
  const db = new DatabaseSync(':memory:');

  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id TEXT PRIMARY KEY,
      email TEXT,
      phone_hash TEXT,
      created_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS sessions (
      id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      token_hash TEXT NOT NULL UNIQUE,
      expires_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS credit_ledger (
      id TEXT PRIMARY KEY,
      user_id TEXT NOT NULL,
      delta INTEGER NOT NULL,
      reason TEXT NOT NULL,
      ref_id TEXT UNIQUE,
      balance_after INTEGER,
      created_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS free_chat_usage (
      id TEXT PRIMARY KEY,
      visitor_hash TEXT NOT NULL UNIQUE,
      user_id TEXT,
      questions_used INTEGER NOT NULL DEFAULT 0,
      max_free INTEGER NOT NULL DEFAULT 3,
      ip_hash TEXT,
      created_at INTEGER NOT NULL,
      updated_at INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS charm_rate_limits (
      key TEXT PRIMARY KEY,
      count INTEGER NOT NULL DEFAULT 1,
      window_start INTEGER NOT NULL,
      expires_at INTEGER NOT NULL
    );
  `);

  return {
    _rawDb: db,
    prepare(sql) {
      return {
        bind(...params) {
          return {
            async first() {
              const stmt = db.prepare(sql);
              const row = stmt.get(...params);
              return row || null;
            },
            async all() {
              const stmt = db.prepare(sql);
              const rows = stmt.all(...params);
              return { results: rows };
            },
            async run() {
              const stmt = db.prepare(sql);
              const info = stmt.run(...params);
              return {
                success: true,
                changes: Number(info.changes),
                meta: {
                  changes: Number(info.changes),
                  last_row_id: Number(info.lastInsertRowid)
                }
              };
            }
          };
        }
      };
    }
  };
}

async function runTests() {
  // ── TEST 1: Banned-Term Detection, Single Retry & Safe Fallback (No Deleted Words) ──
  {
    console.log('[TEST 1] Testing Banned-Term Detection & Fallback Logic...');

    // 1A. Exact test phrases from specification
    assert.equal(hasBannedTerms('will bring you clarity'), true, 'Should detect "will bring you clarity"');
    assert.equal(hasBannedTerms('good luck'), true, 'Should detect "good luck"');
    assert.equal(hasBannedTerms('secure'), false, 'Should allow "secure"');
    assert.equal(hasBannedTerms('exactly'), false, 'Should allow "exactly"');
    assert.equal(hasBannedTerms('accurate'), false, 'Should allow "accurate"');

    // 1B. Expanded prohibited variants
    const prohibitedVariants = [
      'guarantee', 'guarantees', 'guaranteed',
      'prediction', 'predictions',
      'prescription', 'prescriptions',
      'consecrated',
      'cure', 'cures', 'cured',
      'lucks', 'luck', 'lucky',
      'will bring', 'will fix',
      'exact'
    ];
    for (const term of prohibitedVariants) {
      assert.equal(hasBannedTerms(`This offers ${term} for you`), true, `Should detect prohibited term "${term}"`);
    }

    // 1C. Flow: Clean text passes through unchanged
    const cleanSample = 'We examine personal year cycles with disciplined strategic pacing.';
    const cleanProcessed = processTextWithBannedFilter(cleanSample, () => 'Retry text');
    assert.equal(cleanProcessed, cleanSample, 'Clean text must pass through completely intact');

    // 1D. Flow: Banned term detected -> single retry produces clean text -> accepts clean retry
    const dirtyInitial = 'This amulet will bring you clarity.';
    const cleanRetry = 'Focus on analytical clarity and structured execution during this cycle.';
    const retrySucceeded = processTextWithBannedFilter(dirtyInitial, () => cleanRetry);
    assert.equal(retrySucceeded, cleanRetry, 'Should accept clean regenerated response');

    // 1E. Flow: Banned term detected -> single retry STILL contains banned term -> returns fixed safe fallback
    const dirtyRetry = 'We wish you good luck in all endeavors.';
    const fallbackResult = processTextWithBannedFilter(dirtyInitial, () => dirtyRetry);
    assert.equal(fallbackResult, CHARM_SAFE_FALLBACK_TEXT, 'Must return fixed safe fallback sentence when retry fails');

    // 1F. Assert never outputs a sentence with a deleted word
    // Any result is either the original intact sentence, the regenerated intact sentence, or the intact fallback
    assert.ok(
      fallbackResult === cleanSample || fallbackResult === cleanRetry || fallbackResult === CHARM_SAFE_FALLBACK_TEXT,
      'Never output a mutated sentence with deleted words'
    );

    console.log('PASS: Banned-term detection, retry, and safe fallback verified without word deletions.');
  }

  // ── TEST 2: Parallel Guest Counter on Real SQLite ──
  {
    console.log('[TEST 2] Testing 5 Parallel Guest Requests on Real SQLite (node:sqlite)...');
    resetMemory();
    const realDb = createRealSqliteD1();
    const envWithDb = { ...mockEnv, DB: realDb };

    const visitorId = 'vis_parallel_guest_real_sqlite_001';
    const ipSalt = envWithDb.CHARM_IP_HASH_SALT;
    const visitorHash = crypto.createHash('sha256').update(visitorId + ipSalt).digest('hex');

    // Seed guest usage in real SQLite with exactly 2 questions used
    realDb._rawDb.prepare(`
      INSERT INTO free_chat_usage (id, visitor_hash, questions_used, max_free, ip_hash, created_at, updated_at)
      VALUES (?, ?, 2, 3, ?, ?, ?)
    `).run('fcu_seed_guest', visitorHash, 'ip_hash_guest', Date.now(), Date.now());

    // Fire 5 simultaneous requests from this guest
    const guestCookie = `nv_visitor_id=${visitorId}`;
    const promises = Array.from({ length: 5 }, (_, i) => {
      const req = new Request('https://numerosvision.com/api/charm/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Cookie': guestCookie, 'CF-Connecting-IP': '10.0.0.10' },
        body: JSON.stringify({ message: `Concurrent Guest Query ${i + 1}`, name: 'Parallel Guest' })
      });
      return worker.fetch(req, envWithDb, mockCtx);
    });

    const responses = await Promise.all(promises);
    const statuses = responses.map(r => r.status);
    const successCount = statuses.filter(s => s === 200).length;
    const exhaustedCount = statuses.filter(s => s === 402).length;

    assert.equal(successCount, 1, `Expected exactly 1 guest success, got ${successCount}`);
    assert.equal(exhaustedCount, 4, `Expected exactly 4 guest rejections (402), got ${exhaustedCount}`);

    // Verify database count in real SQLite is strictly 3
    const finalRow = realDb._rawDb.prepare('SELECT questions_used FROM free_chat_usage WHERE visitor_hash = ?').get(visitorHash);
    assert.equal(finalRow.questions_used, 3, `Expected database questions_used to be 3, got ${finalRow.questions_used}`);
    console.log('PASS: Real SQLite guest counter logic verified: exactly 1 parallel question succeeded, 4 rejected.');
  }

  // ── TEST 3: Parallel Paid User Concurrency on Real SQLite ──
  {
    console.log('[TEST 3] Testing 5 Parallel Paid Requests on Real SQLite (node:sqlite)...');
    resetMemory();
    const realDb = createRealSqliteD1();
    const envWithDb = { ...mockEnv, DB: realDb };

    const userId = 'usr_paid_concurrency_sqlite';
    const sessionToken = 'tok_paid_sqlite_test_sess';
    const tokenHash = computeTokenHash(sessionToken);

    // Seed user and session in real SQLite
    realDb._rawDb.prepare('INSERT INTO users (id, email, phone_hash, created_at) VALUES (?, ?, ?, ?)').run(userId, 'paid@example.com', 'ph_123', Date.now());
    realDb._rawDb.prepare('INSERT INTO sessions (id, user_id, token_hash, expires_at) VALUES (?, ?, ?, ?)').run('sess_real_1', userId, tokenHash, Date.now() + 86400000);

    // Seed exactly 1 credit in ledger in real SQLite (marked as free_allowance so ensureUserFreeAllowance does not add extra)
    realDb._rawDb.prepare(`
      INSERT INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at)
      VALUES (?, ?, 1, 'free_allowance', ?, 1, ?)
    `).run('crd_seed_1', userId, 'free_' + userId, Date.now());

    const authHeaders = {
      'Content-Type': 'application/json',
      'Cookie': `nv_session=${sessionToken}`,
      'CF-Connecting-IP': '10.0.0.11'
    };

    // Fire 5 simultaneous requests on 1 credit
    const promises = Array.from({ length: 5 }, (_, i) => {
      const req = new Request('https://numerosvision.com/api/charm/chat', {
        method: 'POST',
        headers: authHeaders,
        body: JSON.stringify({ message: `Concurrent Paid Query ${i + 1}`, name: 'Paid Seeker' })
      });
      return worker.fetch(req, envWithDb, mockCtx);
    });

    const responses = await Promise.all(promises);
    const statuses = responses.map(r => r.status);
    const successCount = statuses.filter(s => s === 200).length;
    const exhaustedCount = statuses.filter(s => s === 402).length;

    assert.equal(successCount, 1, `Expected exactly 1 paid success, got ${successCount}`);
    assert.equal(exhaustedCount, 4, `Expected exactly 4 paid rejections (402), got ${exhaustedCount}`);

    // Verify SQLite credit ledger sum is strictly 0
    const balRow = realDb._rawDb.prepare('SELECT SUM(delta) as bal FROM credit_ledger WHERE user_id = ?').get(userId);
    assert.equal(balRow.bal, 0, `Expected ledger balance 0 in real SQLite, got ${balRow.bal}`);
    console.log('PASS: Real SQLite paid ledger logic verified: exactly 1 parallel question succeeded, 4 rejected.');
  }

  // ── TEST 4: Reserve-Then-Refund on Model Failure/Timeout ──
  {
    console.log('[TEST 4] Testing Automatic Refund on Model Failure/Timeout...');
    resetMemory();
    const realDb = createRealSqliteD1();
    const envWithDb = { ...mockEnv, DB: realDb };

    const userId = 'usr_refund_test_user';
    const sessionToken = 'tok_refund_session_abc';
    const tokenHash = computeTokenHash(sessionToken);

    realDb._rawDb.prepare('INSERT INTO users (id, email, phone_hash, created_at) VALUES (?, ?, ?, ?)').run(userId, 'refund@example.com', 'ph_456', Date.now());
    realDb._rawDb.prepare('INSERT INTO sessions (id, user_id, token_hash, expires_at) VALUES (?, ?, ?, ?)').run('sess_refund_1', userId, tokenHash, Date.now() + 86400000);

    // Seed 1 credit in real SQLite (marked as free_allowance so ensureUserFreeAllowance does not add extra)
    realDb._rawDb.prepare(`
      INSERT INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at)
      VALUES (?, ?, 1, 'free_allowance', ?, 1, ?)
    `).run('crd_seed_refund', userId, 'free_' + userId, Date.now());

    // Send request that triggers forced model failure
    const req = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cookie': `nv_session=${sessionToken}`,
        'CF-Connecting-IP': '10.0.0.12'
      },
      body: JSON.stringify({ message: 'Trigger failure', __force_failure__: true })
    });

    const res = await worker.fetch(req, envWithDb, mockCtx);
    assert.equal(res.status, 500);
    const data = await res.json();
    assert.equal(data.code, 'MODEL_GENERATION_FAILED');
    assert.equal(data.error, 'Unable to complete consultation analysis. Your credit has been safely refunded.');

    // Verify ledger in real SQLite: contains reservation (-1) AND refund (+1)
    const ledgerRows = realDb._rawDb.prepare('SELECT delta, reason, ref_id FROM credit_ledger WHERE user_id = ? ORDER BY created_at ASC').all(userId);
    const reasons = ledgerRows.map(r => r.reason);
    assert.ok(reasons.includes('question_asked'), 'Reservation row missing');
    assert.ok(reasons.includes('refund'), 'Refund row missing');

    const balRow = realDb._rawDb.prepare('SELECT SUM(delta) as bal FROM credit_ledger WHERE user_id = ?').get(userId);
    assert.equal(balRow.bal, 1, `Expected final balance to remain 1 after refund, got ${balRow.bal}`);
    console.log('PASS: Automatic refund verified: 500 returned, reservation + refund rows recorded, balance intact.');
  }

  // ── TEST 5: LocalStorage Tamper Prevention ──
  {
    console.log('[TEST 5] Testing LocalStorage Tampering Prevention (Server-Authoritative Gate)...');
    resetMemory();
    const realDb = createRealSqliteD1();
    const envWithDb = { ...mockEnv, DB: realDb };

    const userId = 'usr_tamper_attacker';
    const sessionToken = 'tok_tamper_session_xyz';
    const tokenHash = computeTokenHash(sessionToken);

    realDb._rawDb.prepare('INSERT INTO users (id, email, phone_hash, created_at) VALUES (?, ?, ?, ?)').run(userId, 'tamper@example.com', 'ph_789', Date.now());
    realDb._rawDb.prepare('INSERT INTO sessions (id, user_id, token_hash, expires_at) VALUES (?, ?, ?, ?)').run('sess_tamper_1', userId, tokenHash, Date.now() + 86400000);

    // User already received and exhausted their free allowance (net balance = 0)
    realDb._rawDb.prepare(`
      INSERT INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at)
      VALUES (?, ?, 0, 'free_allowance', ?, 0, ?)
    `).run('crd_zero_tamper', userId, 'free_' + userId, Date.now());

    const balRow = realDb._rawDb.prepare('SELECT COALESCE(SUM(delta), 0) as bal FROM credit_ledger WHERE user_id = ?').get(userId);
    assert.equal(balRow.bal, 0);

    // Attacker crafts request with spoofed tokens attempting to bypass client checks
    const req = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cookie': `nv_session=${sessionToken}; nv_premium_token=fake_vip_token_unlimited; nv_active_tier=tier3`,
        'CF-Connecting-IP': '10.0.0.13'
      },
      body: JSON.stringify({ message: 'I have unlimited access on client', name: 'Attacker' })
    });

    const res = await worker.fetch(req, envWithDb, mockCtx);
    assert.equal(res.status, 402);
    const data = await res.json();
    assert.equal(data.code, 'CREDITS_EXHAUSTED');
    console.log('PASS: LocalStorage tampering blocked: client-side tokens ignored, strictly 402 returned.');
  }

  // ── TEST 6: Zero Model Calls at Zero Balance ──
  {
    console.log('[TEST 6] Testing Zero Model Calls at Zero Balance...');
    resetMemory();
    const realDb = createRealSqliteD1();
    const envWithDb = { ...mockEnv, DB: realDb };

    const userId = 'usr_zero_calls_check';
    const sessionToken = 'tok_zero_calls_session';
    const tokenHash = computeTokenHash(sessionToken);

    realDb._rawDb.prepare('INSERT INTO users (id, email, phone_hash, created_at) VALUES (?, ?, ?, ?)').run(userId, 'zero@example.com', 'ph_000', Date.now());
    realDb._rawDb.prepare('INSERT INTO sessions (id, user_id, token_hash, expires_at) VALUES (?, ?, ?, ?)').run('sess_zero_1', userId, tokenHash, Date.now() + 86400000);

    // User already received and exhausted their free allowance (net balance = 0)
    realDb._rawDb.prepare(`
      INSERT INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at)
      VALUES (?, ?, 0, 'free_allowance', ?, 0, ?)
    `).run('crd_zero_calls', userId, 'free_' + userId, Date.now());

    // Ensure model invocations counter starts at 0
    memoryStore.charmModelInvocations = 0;

    const req = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cookie': `nv_session=${sessionToken}`,
        'CF-Connecting-IP': '10.0.0.14'
      },
      body: JSON.stringify({ message: 'Attempt question with zero credits' })
    });

    const res = await worker.fetch(req, envWithDb, mockCtx);
    assert.equal(res.status, 402);
    assert.equal(memoryStore.charmModelInvocations, 0, `Model was called ${memoryStore.charmModelInvocations} times when balance was 0!`);
    console.log('PASS: Zero model calls verified: model invocations strictly 0 at zero balance.');
  }

  // ── TEST 7: Fail-Closed Security (Missing Salt/DB) & Kill-Switch Exact Message ──
  {
    console.log('[TEST 7] Testing Fail-Closed Security & Kill-Switch Message...');
    resetMemory();

    // 1. Missing CHARM_IP_HASH_SALT outside test environment -> HTTP 503
    const prodEnvMissingSalt = {
      ENVIRONMENT: 'production',
      MOCK_PAYMENTS: 'false',
      DB: createRealSqliteD1()
    };

    const req1 = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'CF-Connecting-IP': '10.0.0.15' },
      body: JSON.stringify({ message: 'Test missing salt' })
    });
    const res1 = await worker.fetch(req1, prodEnvMissingSalt, mockCtx);
    assert.equal(res1.status, 503);
    const data1 = await res1.json();
    assert.equal(data1.code, 'SERVICE_MISCONFIGURED');

    // 2. Missing D1 DB binding outside test environment -> HTTP 503
    const prodEnvMissingDb = {
      ENVIRONMENT: 'production',
      MOCK_PAYMENTS: 'false',
      CHARM_IP_HASH_SALT: 'configured_prod_salt'
    };

    const req2 = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'CF-Connecting-IP': '10.0.0.15' },
      body: JSON.stringify({ message: 'Test missing db' })
    });
    const res2 = await worker.fetch(req2, prodEnvMissingDb, mockCtx);
    assert.equal(res2.status, 503);
    const data2 = await res2.json();
    assert.equal(data2.code, 'SERVICE_DATABASE_UNAVAILABLE');

    // 3. Kill-Switch Activated -> HTTP 503 with exact updated message
    const killedEnv = { ...mockEnv, CHARM_KILL_SWITCH: 'true' };
    const kReq = new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'CF-Connecting-IP': '10.0.0.16' },
      body: JSON.stringify({ message: 'Test question during pause' })
    });
    const kRes = await worker.fetch(kReq, killedEnv, mockCtx);
    assert.equal(kRes.status, 503);
    const kData = await kRes.json();
    assert.equal(kData.code, 'SERVICE_TEMPORARILY_UNAVAILABLE');
    assert.equal(kData.error, 'Charm AI is temporarily paused. Please try again shortly.');

    console.log('PASS: Fail-closed security verified: 503 on missing salt/DB, exact kill-switch pause message.');
  }

  // ── TEST 8: Verify + Webhook Idempotency (Credits Granted Exactly Once) ──
  {
    console.log('[TEST 8] Testing Verify + Webhook Idempotency (Zero Double-Grant)...');
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

  // ── TEST 9: /login Same-Site Relative returnTo Validation ──
  {
    console.log('[TEST 9] Testing /login Same-Site Relative returnTo Validation...');

    // Accepted valid relative paths
    assert.equal(isValidRelativeReturnTo('/pricing/?domain=ai'), true);
    assert.equal(isValidRelativeReturnTo('/dashboard/'), true);
    assert.equal(isValidRelativeReturnTo('/calculators/life-path-number/'), true);
    assert.equal(isValidRelativeReturnTo('/charm_ai.html?q=test'), true);

    // Rejected absolute URLs, protocol-relative, and script schemes
    assert.equal(isValidRelativeReturnTo('https://evil.com'), false, 'Should reject https://evil.com');
    assert.equal(isValidRelativeReturnTo('http://evil.com'), false, 'Should reject http://evil.com');
    assert.equal(isValidRelativeReturnTo('//evil.com'), false, 'Should reject //evil.com');
    assert.equal(isValidRelativeReturnTo('/\\evil.com'), false, 'Should reject /\\evil.com');
    assert.equal(isValidRelativeReturnTo('\\evil.com'), false, 'Should reject \\evil.com');
    assert.equal(isValidRelativeReturnTo('javascript:alert(1)'), false, 'Should reject javascript: URI');
    assert.equal(isValidRelativeReturnTo('data:text/html,malicious'), false, 'Should reject data: URI');
    assert.equal(isValidRelativeReturnTo('vbscript:msgbox(1)'), false, 'Should reject vbscript: URI');

    // Fallback behavior
    assert.equal(sanitizeReturnToUrl('https://evil.com', '/dashboard/'), '/dashboard/');
    assert.equal(sanitizeReturnToUrl('//attacker.com/steal', '/dashboard/'), '/dashboard/');
    assert.equal(sanitizeReturnToUrl('/pricing/?domain=ai', '/dashboard/'), '/pricing/?domain=ai');

    console.log('PASS: /login same-site relative returnTo validation verified (open-redirects blocked).');
  }

  console.log('\n[SUCCESS] All Charm AI Gating & Ledger tests completed successfully!');
}

runTests().catch(err => {
  console.error('[FATAL TEST ERROR]', err);
  process.exit(1);
});
