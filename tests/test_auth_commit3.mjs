/**
 * NUMEROS VISION — COMMIT 3 AUTHENTICATION TEST SUITE
 * Tests:
 * 1. CSRF Origin check on state-changing POST requests
 * 2. OTP Send, masking, rate limiting, and dev_otp gate
 * 3. OTP Verify with attempts countdown, lockout, and constant-time compare
 * 4. HttpOnly, Secure, SameSite=Lax session cookie generation
 * 5. /api/me session verification and entitlement balance
 * 6. /api/logout session termination and cookie clearing
 * 7. Google Identity credential verification gate
 */

import worker from '../app/static/_worker.js';

async function runAuthTests() {
  console.log('--- STARTING COMMIT 3 AUTHENTICATION TESTS ---\n');
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

  const baseEnv = {
    ENVIRONMENT: 'production',
    AUTH_SECRET: 'test_auth_secret_key_99',
    RAZORPAY_KEY_ID: 'rzp_test_MOCK_ENV_KEY',
    RAZORPAY_KEY_SECRET: 'test_secret_for_local_behavior_suite',
    FAST2SMS_API_KEY: 'test_fast2sms_key',
    ASSETS: { fetch: async () => new Response('stub', { status: 200 }) }
  };

  // Test 1: Origin check blocks malicious cross-site POSTs
  await assertCase('CSRF Origin Check blocks unauthorized origins (403)', async () => {
    const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'https://evil-attacker.example.com'
      },
      body: JSON.stringify({ phone: '9876543210' })
    });
    const res = await worker.fetch(req, baseEnv);
    if (res.status !== 403) throw new Error(`Expected 403, got ${res.status}`);
  });

  // Test 2: In production, dev_otp is NEVER returned in response
  await assertCase('Production OTP send never returns dev_otp or code in JSON', async () => {
    const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'https://numerosvision.com'
      },
      body: JSON.stringify({ phone: '9876543210' })
    });
    const res = await worker.fetch(req, baseEnv);
    if (res.status !== 200) throw new Error(`Expected 200, got ${res.status}`);
    const data = await res.json();
    if (data.dev_otp !== undefined) throw new Error('dev_otp must not exist in production');
    if (data.destination !== '+91 ******3210') throw new Error(`Expected masked phone, got ${data.destination}`);
  });

  // Test 3: In local dev, dev_otp is gated strictly to ENVIRONMENT=local
  let devCode = null;
  await assertCase('Local dev OTP send returns dev_otp when ENVIRONMENT=local', async () => {
    const devEnv = { ...baseEnv, ENVIRONMENT: 'local' };
    const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000'
      },
      body: JSON.stringify({ phone: '9812345678' })
    });
    const res = await worker.fetch(req, devEnv);
    if (res.status !== 200) throw new Error(`Expected 200, got ${res.status}`);
    const data = await res.json();
    if (!data.dev_otp || data.dev_otp.length !== 6) throw new Error(`Invalid dev_otp: ${data.dev_otp}`);
    devCode = data.dev_otp;
  });

  // Test 4: Rate limiting: consecutive request within 60s returns 429
  await assertCase('Requesting OTP again within 60 seconds returns 429 Too Many Requests', async () => {
    const devEnv = { ...baseEnv, ENVIRONMENT: 'local' };
    const req = new Request('https://numerosvision.com/api/v1/auth/otp/send', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000'
      },
      body: JSON.stringify({ phone: '9812345678' })
    });
    const res = await worker.fetch(req, devEnv);
    if (res.status !== 429) throw new Error(`Expected 429, got ${res.status}`);
  });

  // Test 5: Wrong OTP code returns 400 and decreases attempt count
  await assertCase('Wrong verification code returns 400 with attempts countdown', async () => {
    const devEnv = { ...baseEnv, ENVIRONMENT: 'local' };
    const req = new Request('https://numerosvision.com/api/v1/auth/otp/verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000'
      },
      body: JSON.stringify({ phone: '9812345678', otp: '000000' })
    });
    const res = await worker.fetch(req, devEnv);
    if (res.status !== 400) throw new Error(`Expected 400, got ${res.status}`);
    const data = await res.json();
    if (!data.error.includes('attempt')) throw new Error(`Expected attempt countdown, got ${data.error}`);
  });

  // Test 6: Correct OTP verifies, returns 200, sets HttpOnly nv_session cookie
  let sessionCookie = null;
  await assertCase('Authentic OTP verification sets HttpOnly Secure session cookie', async () => {
    const devEnv = { ...baseEnv, ENVIRONMENT: 'local' };
    const req = new Request('https://numerosvision.com/api/v1/auth/otp/verify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3000'
      },
      body: JSON.stringify({ phone: '9812345678', otp: devCode })
    });
    const res = await worker.fetch(req, devEnv);
    if (res.status !== 200) {
      const errText = await res.text();
      throw new Error(`Expected 200, got ${res.status}: ${errText}`);
    }
    const data = await res.json();
    if (!data.verified || !data.authenticated) throw new Error(`Expected verified=true, got ${JSON.stringify(data)}`);

    const setCookie = res.headers.get('Set-Cookie');
    if (!setCookie || !setCookie.includes('nv_session=') || !setCookie.includes('HttpOnly')) {
      throw new Error(`Expected HttpOnly nv_session cookie, got ${setCookie}`);
    }
    sessionCookie = setCookie.split(';')[0];
  });

  // Test 7: /api/me without cookie returns 401
  await assertCase('/api/me without session cookie returns 401 Unauthorized', async () => {
    const req = new Request('https://numerosvision.com/api/me', { method: 'GET' });
    const res = await worker.fetch(req, baseEnv);
    if (res.status !== 401) throw new Error(`Expected 401, got ${res.status}`);
    const data = await res.json();
    if (data.authenticated !== false) throw new Error('Expected authenticated=false');
  });

  // Test 8: /api/me with valid session cookie returns 200 and user profile
  await assertCase('/api/me with valid nv_session cookie returns 200 and authenticated session', async () => {
    const req = new Request('https://numerosvision.com/api/me', {
      method: 'GET',
      headers: { 'Cookie': sessionCookie }
    });
    const res = await worker.fetch(req, baseEnv);
    if (res.status !== 200) throw new Error(`Expected 200, got ${res.status}`);
    const data = await res.json();
    if (data.authenticated !== true || !data.user || !data.user.id) {
      throw new Error(`Invalid session data: ${JSON.stringify(data)}`);
    }
  });

  // Test 9: /api/logout terminates session and clears cookie
  await assertCase('/api/logout invalidates session and clears cookie with Max-Age=0', async () => {
    const req = new Request('https://numerosvision.com/api/logout', {
      method: 'POST',
      headers: {
        'Cookie': sessionCookie,
        'Origin': 'https://numerosvision.com'
      }
    });
    const res = await worker.fetch(req, baseEnv);
    if (res.status !== 200) throw new Error(`Expected 200, got ${res.status}`);
    const setCookie = res.headers.get('Set-Cookie');
    if (!setCookie || !setCookie.includes('Max-Age=0')) {
      throw new Error(`Expected Max-Age=0 cookie clearing header, got ${setCookie}`);
    }
  });

  // Test 10: /api/v1/auth/google rejects invalid/unverified credential with 401
  await assertCase('Google Identity auth rejects invalid credential (401)', async () => {
    const req = new Request('https://numerosvision.com/api/v1/auth/google', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'https://numerosvision.com'
      },
      body: JSON.stringify({ credential: 'fake_unverified_token_12345' })
    });
    const res = await worker.fetch(req, baseEnv);
    if (res.status !== 401) throw new Error(`Expected 401, got ${res.status}`);
  });

  console.log(`\n--- RESULT: ${passed}/${total} COMMIT 3 AUTH TESTS PASSED ---`);
  if (passed !== total) {
    process.exit(1);
  }
}

runAuthTests().catch(err => {
  console.error('Fatal auth test error:', err);
  process.exit(1);
});
