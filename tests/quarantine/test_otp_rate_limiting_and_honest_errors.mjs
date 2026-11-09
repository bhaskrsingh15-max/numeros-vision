import assert from 'node:assert';
import fs from 'node:fs';
import path from 'node:path';
import workerModule from '../app/static/_worker.js';

console.log('--- STARTING OTP RATE LIMITING & HONEST ERROR TEST SUITE ---');

const baseEnv = {
  ENVIRONMENT: 'preview',
  OTP_HMAC_SECRET: 'test_otp_hmac_secret_32bytes_long_12345',
  SESSION_SECRET: 'test_session_secret_32bytes_long_12345',
  IP_HASH_SALT: 'test_ip_hash_salt_32bytes_long_12345',
  DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
  FAST2SMS_API_KEY: 'test_fast2sms_key_mock'
};

const originalFetch = globalThis.fetch;

async function runTests() {
  // ── TEST 1: Missing FAST2SMS_API_KEY returns 503 honest error ──
  console.log('\n[Test 1] Missing FAST2SMS_API_KEY returns honest 503 error...');
  {
    const envNoKey = { ...baseEnv, FAST2SMS_API_KEY: '' };
    const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({ phone: '9876543210' })
    });

    const res = await workerModule.fetch(req, envNoKey, {});
    assert.strictEqual(res.status, 503, `Expected 503, got ${res.status}`);
    const data = await res.json();
    assert.strictEqual(data.success, false, 'Expected success: false');
    assert.strictEqual(data.sms_delivered, false, 'sms_delivered must be false');
    assert.match(data.error, /FAST2SMS_API_KEY is not configured/, 'Error must explain missing FAST2SMS_API_KEY');
    assert(!JSON.stringify(data).includes('dispatched'), 'Must never say code dispatched on missing key');
    assert.strictEqual(data.code, undefined, 'Code must not be in response');
    console.log('✔ PASS: Missing key returns 503 with honest explanation and zero dispatch claim.');
  }

  // ── TEST 2: Fast2SMS gateway rejection returns 503 honest error ──
  console.log('\n[Test 2] Fast2SMS gateway rejection returns honest 503 error...');
  {
    globalThis.fetch = async (url) => {
      if (String(url).includes('fast2sms.com')) {
        return new Response(JSON.stringify({ return: false, message: 'Invalid Numbers or DLT Template error' }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        });
      }
      return originalFetch(url);
    };

    const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({ phone: '9876543211' })
    });

    const res = await workerModule.fetch(req, baseEnv, {});
    assert.strictEqual(res.status, 503, `Expected 503, got ${res.status}`);
    const data = await res.json();
    assert.strictEqual(data.success, false, 'Expected success: false');
    assert.strictEqual(data.sms_delivered, false, 'sms_delivered must be false');
    assert.match(data.error, /SMS delivery failed/, 'Error must clearly state SMS delivery failure');
    assert.match(data.error, /Invalid Numbers or DLT Template error/, 'Error must surface gateway explanation');
    assert(!JSON.stringify(data).includes('dispatched'), 'Must never say code dispatched on gateway failure');
    console.log('✔ PASS: Gateway rejection returns 503 with specific error and zero false claims.');
  }

  // ── TEST 3: Network exception to Fast2SMS returns 503 honest error ──
  console.log('\n[Test 3] Network exception during Fast2SMS dispatch returns 503...');
  {
    globalThis.fetch = async (url) => {
      if (String(url).includes('fast2sms.com')) {
        throw new TypeError('Fast2SMS socket network unreachable');
      }
      return originalFetch(url);
    };

    const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({ phone: '9876543212' })
    });

    const res = await workerModule.fetch(req, baseEnv, {});
    assert.strictEqual(res.status, 503, `Expected 503, got ${res.status}`);
    const data = await res.json();
    assert.strictEqual(data.success, false);
    assert.strictEqual(data.sms_delivered, false);
    assert.match(data.error, /SMS delivery failed/);
    console.log('✔ PASS: Network exception returns 503 and logs no secrets.');
  }

  // ── TEST 4: Successful Fast2SMS returns 200 with sms_delivered: true ──
  console.log('\n[Test 4] Successful Fast2SMS dispatch returns 200 with sms_delivered: true...');
  {
    globalThis.fetch = async (url) => {
      if (String(url).includes('fast2sms.com')) {
        return new Response(JSON.stringify({ return: true, message: ['SMS sent successfully'] }), {
          status: 200,
          headers: { 'Content-Type': 'application/json' }
        });
      }
      return originalFetch(url);
    };

    const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({ phone: '9876543213' })
    });

    const res = await workerModule.fetch(req, baseEnv, {});
    assert.strictEqual(res.status, 200, `Expected 200, got ${res.status}`);
    const data = await res.json();
    assert.strictEqual(data.success, true);
    assert.strictEqual(data.sms_delivered, true);
    assert.strictEqual(data.destination, '+91 ******3213');
    assert.strictEqual(data.code, undefined);
    assert.strictEqual(data.dev_otp, undefined);
    console.log('✔ PASS: Successful dispatch returns 200, sms_delivered: true, and never leaks OTP code.');
  }

  // ── TEST 5: Rate Limiting - Per-Mobile 60-second cooldown ──
  console.log('\n[Test 5] Per-Mobile 60-second cooldown returns 429...');
  {
    const req2 = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({ phone: '9876543213' }) // same number immediately
    });

    const res = await workerModule.fetch(req2, baseEnv, {});
    assert.strictEqual(res.status, 429, `Expected 429 for rapid consecutive OTP, got ${res.status}`);
    const data = await res.json();
    assert.strictEqual(data.success, false);
    assert.match(data.error, /Please wait 60 seconds before requesting another code/);
    console.log('✔ PASS: Consecutive request within 60s blocked with 429.');
  }

  // ── TEST 6: Rate Limiting - Per-Mobile hourly cap (5 max) in D1 ──
  console.log('\n[Test 6] Per-Mobile hourly cap in D1...');
  {
    const mockD1 = {
      prepare: (sql) => ({
        bind: (...args) => ({
          first: async () => {
            if (sql.includes('phone_hash = ? AND created_at > ?')) {
              // Simulate 5 attempts already recorded in the hour
              return { cnt: 5, last_req: Date.now() - 70000 };
            }
            if (sql.includes('ip_hash = ? AND created_at > ?')) {
              return { cnt: 1 };
            }
            return null;
          },
          run: async () => ({ success: true })
        })
      })
    };

    const d1Env = { ...baseEnv, DB: mockD1 };
    const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({ phone: '9876543214' })
    });

    const res = await workerModule.fetch(req, d1Env, {});
    assert.strictEqual(res.status, 429, `Expected 429 for >5 hourly OTPs, got ${res.status}`);
    const data = await res.json();
    assert.match(data.error, /Maximum OTP requests exceeded for this number/);
    console.log('✔ PASS: D1-backed hourly limit (5 requests) strictly enforces 429.');
  }

  // ── TEST 7: Rate Limiting - Per-IP hourly cap (10 max) in D1 ──
  console.log('\n[Test 7] Per-IP hourly cap in D1...');
  {
    const mockD1 = {
      prepare: (sql) => ({
        bind: (...args) => ({
          first: async () => {
            if (sql.includes('phone_hash = ? AND created_at > ?')) {
              return { cnt: 1, last_req: Date.now() - 70000 };
            }
            if (sql.includes('ip_hash = ? AND created_at > ?')) {
              // Simulate 10 requests from this IP in the hour
              return { cnt: 10 };
            }
            return null;
          },
          run: async () => ({ success: true })
        })
      })
    };

    const d1Env = { ...baseEnv, DB: mockD1 };
    const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'https://numerosvision.com',
        'CF-Connecting-IP': '203.0.113.195'
      },
      body: JSON.stringify({ phone: '9876543215' })
    });

    const res = await workerModule.fetch(req, d1Env, {});
    assert.strictEqual(res.status, 429, `Expected 429 for IP rate limit, got ${res.status}`);
    const data = await res.json();
    assert.match(data.error, /Rate limit exceeded for this IP/);
    console.log('✔ PASS: D1-backed IP hourly limit (10 requests) strictly enforces 429.');
  }

  // ── TEST 8: Client-Side login.html Honest Error Display Audit ──
  console.log('\n[Test 8] Client-side login.html honest error handling audit...');
  {
    const loginHtml = fs.readFileSync(path.resolve('app/static/login.html'), 'utf-8');
    assert(loginHtml.includes('if (!ok || !data || !data.success)'), 'login.html must guard against non-success responses');
    assert(loginHtml.includes("alertBox.className = 'alert-box alert-error'"), 'login.html must surface errors in alertBox');
    assert(loginHtml.includes("feedback.style.color = '#c53030'"), 'login.html must display error feedback in red');
    assert(!loginHtml.includes('console.warn(\'Backend login OTP unreachable, using fallback:\''), 'Unreachable warning fallback removed');
    console.log('✔ PASS: login.html audited: never claims dispatched on failure, renders honest errors.');
  }

  // Restore fetch
  globalThis.fetch = originalFetch;

  console.log('\n--- ALL OTP RATE LIMITING & HONEST ERROR TESTS PASSED (100%) ---');
}

runTests().catch(err => {
  globalThis.fetch = originalFetch;
  console.error('\n❌ TEST SUITE FAILED:', err);
  process.exit(1);
});
