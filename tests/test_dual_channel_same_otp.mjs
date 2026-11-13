import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import worker from '../app/static/_worker.js';

function createCleanMemoryReset() {
  if (!worker.memoryStore) return;
  if (worker.memoryStore.emailHistory) worker.memoryStore.emailHistory.length = 0;
  if (worker.memoryStore.mobileRateHistory) worker.memoryStore.mobileRateHistory.length = 0;
  if (worker.memoryStore.smsDailyCounts) worker.memoryStore.smsDailyCounts.clear();
  if (worker.memoryStore.emailDailyCounts) worker.memoryStore.emailDailyCounts.clear();
  if (worker.memoryStore.sentEmails) worker.memoryStore.sentEmails.length = 0;
  if (worker.memoryStore.sentSms) worker.memoryStore.sentSms.length = 0;
}

async function runBrevoDualChannelOtpSuite() {
  console.log('[TEST] Running Brevo Dual-Channel OTP, Sender Gate, Abuse Controls & Redaction Suite...');

  const baseEnv = {
    ENVIRONMENT: 'test',
    NV_FORCE_LAUNCH_MODE: '1',
    OTP_HMAC_SECRET: 'test_otp_hmac_secret_32bytes_hex00000000000000000000000000000000',
    SESSION_SECRET: 'test_session_secret_32bytes_hex00000000000000000000000000000000',
    IP_HASH_SALT: 'test_ip_hash_salt_hex00000000000000000000000000000000',
    DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
    TELEMETRY_SALT: 'test_telemetry_salt_0123456789abcdef',
    RAZORPAY_KEY_ID: 'rzp_test_mockKeyId123456',
    RAZORPAY_KEY_SECRET: 'mock_razorpay_secret_key_123',
    RAZORPAY_WEBHOOK_SECRET: 'mock_webhook_secret_123',
    DOWNLOAD_TOKEN_SECRET: 'test_download_token_secret_32bytes_hex00000000000000000000000000',
    TURNSTILE_SECRET_KEY: '1x0000000000000000000000000000000AA',
    EMAIL_PROVIDER: 'brevo',
    EMAIL_API_KEY: 'xkeysib-mock_brevo_unit_test_key_001',
    EMAIL_FROM: 'Numeros Vision <support@numerosvision.com>',
    BREVO_SMS_SENDER: 'NVMOCKHDR',
    EMAIL_DAILY_CAP: '500',
    SMS_DAILY_CAP: '25',
    OTP_MOBILE_RATE_LIMIT: '3',
    OTP_EMAIL_RATE_LIMIT: '5',
    OTP_IP_RATE_LIMIT: '10'
  };

  // Capture all console logs to verify exact "sms_skipped: no sender" and zero OTP/phone leakage
  const capturedLogs = [];
  const origInfo = console.info;
  const origWarn = console.warn;
  const origError = console.error;
  const recordLog = (level, args) => {
    capturedLogs.push({
      level,
      text: args.map((a) => (typeof a === 'string' ? a : JSON.stringify(a))).join(' ')
    });
  };
  console.info = (...args) => { recordLog('info', args); };
  console.warn = (...args) => { recordLog('warn', args); };
  console.error = (...args) => { recordLog('error', args); };

  // Strict mocked Brevo transport (zero live network calls)
  const brevoEmailCalls = [];
  const brevoSmsCalls = [];
  let smsMockBehavior = 'ok'; // 'ok' | 'http_500_echo_secret' | 'network_throw' | 'slow_hang'

  const origFetch = globalThis.fetch;
  globalThis.fetch = async (url, init = {}) => {
    const urlStr = String(url);
    if (urlStr === 'https://api.brevo.com/v3/smtp/email') {
      const parsedBody = JSON.parse(init.body);
      brevoEmailCalls.push({ url: urlStr, headers: init.headers, body: parsedBody });
      return new Response(JSON.stringify({ messageId: `<brevo_email_${brevoEmailCalls.length}@numerosvision.test>` }), {
        status: 201,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    if (urlStr === 'https://api.brevo.com/v3/transactionalSMS/send') {
      const parsedBody = JSON.parse(init.body);
      brevoSmsCalls.push({ url: urlStr, headers: init.headers, body: parsedBody });
      if (smsMockBehavior === 'http_500_echo_secret') {
        return new Response(JSON.stringify({
          code: 'internal_error',
          message: `Gateway failed for ${parsedBody.recipient} payload: ${parsedBody.content}`
        }), { status: 500, headers: { 'Content-Type': 'application/json' } });
      }
      if (smsMockBehavior === 'network_throw') {
        throw new Error(`Socket reset sending to ${parsedBody.recipient}: ${parsedBody.content}`);
      }
      if (smsMockBehavior === 'slow_hang') {
        return await new Promise((resolve, reject) => {
          const t = setTimeout(() => {
            resolve(new Response(JSON.stringify({ messageId: 999 }), { status: 201 }));
          }, 2500);
          if (init.signal) {
            init.signal.addEventListener('abort', () => {
              clearTimeout(t);
              reject(new Error('Aborted'));
            });
          }
        });
      }
      return new Response(JSON.stringify({ reference: 'brevo_sms_ref_mock', messageId: 900100 + brevoSmsCalls.length }), {
        status: 201,
        headers: { 'Content-Type': 'application/json' }
      });
    }
    if (urlStr === 'https://api.razorpay.com/v1/orders') {
      const parsed = JSON.parse(init.body);
      return new Response(JSON.stringify({
        id: 'order_rzp_' + Math.random().toString(36).slice(2, 10),
        amount: parsed.amount,
        currency: 'INR',
        status: 'created'
      }), { status: 200, headers: { 'Content-Type': 'application/json' } });
    }
    throw new Error(`Unexpected external network call in unit test: ${urlStr}`);
  };

  try {
    createCleanMemoryReset();

    // =========================================================================
    // 1. SENDER GATE: Unset or invalid BREVO_SMS_SENDER skips SMS & logs "sms_skipped: no sender"
    // =========================================================================
    const invalidSenders = ['', undefined, '123456', 'AB', 'ABCDEFGHIJKLM', 'NV-SMS!'];
    for (let i = 0; i < invalidSenders.length; i++) {
      const envNoSender = { ...baseEnv };
      if (invalidSenders[i] === undefined) delete envNoSender.BREVO_SMS_SENDER;
      else envNoSender.BREVO_SMS_SENDER = invalidSenders[i];

      const logCountBefore = capturedLogs.length;
      const smsCountBefore = brevoSmsCalls.length;
      const emailCountBefore = brevoEmailCalls.length;

      const res = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': `10.20.1.${i + 1}` },
        body: JSON.stringify({
          email: `nosender_${i}@example.com`,
          phone: `+91 98765 4321${i}`,
          turnstile_token: 'test_turnstile_pass'
        })
      }), envNoSender, {});

      assert.strictEqual(res.status, 200, `Missing/invalid sender case #${i} must not fail Email OTP`);
      const data = await res.json();
      assert.deepStrictEqual(data.channels_dispatched, { email: true, sms: false });
      assert.strictEqual(data.channel_message, '6-digit code sent to your email.');
      assert.strictEqual(brevoEmailCalls.length, emailCountBefore + 1, 'Email OTP must be sent');
      assert.strictEqual(brevoSmsCalls.length, smsCountBefore, 'Brevo SMS must be skipped completely (never invent header)');
      const recentLogs = capturedLogs.slice(logCountBefore).map((l) => l.text);
      assert(recentLogs.includes('sms_skipped: no sender'), `Must log exact "sms_skipped: no sender" for sender=${String(invalidSenders[i])}`);
    }
    origInfo('  ✓ 1. Verified unset/invalid BREVO_SMS_SENDER skips SMS & logs "sms_skipped: no sender" without inventing a header');

    // =========================================================================
    // 2. DUAL-CHANNEL BREVO DISPATCH: Exact same 6-digit OTP + accurate UI channel message + last-2 mask
    // =========================================================================
    createCleanMemoryReset();
    const dualRes = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.20.2.1' },
      body: JSON.stringify({
        email: 'dual_brevo@example.com',
        phone: '+91 98765 43239',
        turnstile_token: 'test_turnstile_pass'
      })
    }), baseEnv, {});
    assert.strictEqual(dualRes.status, 200);
    const dualJson = await dualRes.json();
    assert.deepStrictEqual(dualJson.channels_dispatched, { email: true, sms: true });
    assert.strictEqual(dualJson.phone_masked, '+91 ********39', 'Phone mask must show ONLY last 2 digits');
    assert.strictEqual(dualJson.channel_message, '6-digit code sent to your email and mobile.');

    const lastEmailCall = brevoEmailCalls[brevoEmailCalls.length - 1];
    const lastSmsCall = brevoSmsCalls[brevoSmsCalls.length - 1];
    const emailOtp = lastEmailCall.body.textContent.match(/\b(\d{6})\b/)[1];
    const smsOtp = lastSmsCall.body.content.match(/\b(\d{6})\b/)[1];
    assert.strictEqual(smsOtp, emailOtp, 'Brevo Email and Brevo SMS must carry the EXACT SAME 6-digit OTP');
    assert.strictEqual(lastSmsCall.body.sender, 'NVMOCKHDR');
    assert.strictEqual(lastSmsCall.body.recipient, '919876543239');

    const verifyDual = await worker.fetch(new Request('http://localhost/api/v1/auth/email/verify-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.20.2.1' },
      body: JSON.stringify({
        email: 'dual_brevo@example.com',
        phone: '+919876543239',
        code: smsOtp,
        checkout_flow: true
      })
    }), baseEnv, {});
    assert.strictEqual(verifyDual.status, 200);
    const verifyDualJson = await verifyDual.json();
    assert.strictEqual(verifyDualJson.verified, true);
    assert(verifyDualJson.checkout_token);
    origInfo('  ✓ 2. Verified Brevo Email + Brevo SMS send identical OTP, last-2 phone mask, and accurate channel status');

    // =========================================================================
    // 3. NON-BLOCKING SMS: HTTP 500, network throw, and timeout never block or delay Email OTP
    // =========================================================================
    for (const mode of ['http_500_echo_secret', 'network_throw', 'slow_hang']) {
      smsMockBehavior = mode;
      const envForFailure = { ...baseEnv, BREVO_SMS_TIMEOUT_MS: '80' };
      const t0 = Date.now();
      const failRes = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': `10.20.3.${mode.length}` },
        body: JSON.stringify({
          email: `resilient_${mode}@example.com`,
          phone: '+91 97654 32188',
          turnstile_token: 'test_turnstile_pass'
        })
      }), envForFailure, {});
      const elapsedMs = Date.now() - t0;
      assert.strictEqual(failRes.status, 200, `SMS failure mode=${mode} must NEVER fail Email OTP`);
      assert(elapsedMs < 600, `SMS failure mode=${mode} must not delay Email OTP (took ${elapsedMs}ms)`);
      const failJson = await failRes.json();
      assert.deepStrictEqual(failJson.channels_dispatched, { email: true, sms: false });
      assert.strictEqual(failJson.channel_message, '6-digit code sent to your email.');
    }
    smsMockBehavior = 'ok';
    origInfo('  ✓ 3. Verified SMS HTTP 500, network throw, and timeout never block or delay Email OTP');

    // =========================================================================
    // 4. ABUSE CONTROLS ON POST /api/v1/auth/email/send-code
    // =========================================================================
    // 4a. Turnstile required (empty and invalid tokens rejected with 403)
    for (const badTok of ['', 'invalid_turnstile_tok']) {
      const tsRes = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.20.4.1' },
        body: JSON.stringify({ email: 'turnstile@example.com', phone: '+919876543211', turnstile_token: badTok })
      }), baseEnv, {});
      assert.strictEqual(tsRes.status, 403, `Turnstile token="${badTok}" must be rejected with 403`);
    }

    // 4b. Per-mobile rate limit
    createCleanMemoryReset();
    const mobLimitEnv = { ...baseEnv, OTP_MOBILE_RATE_LIMIT: '2', OTP_EMAIL_RATE_LIMIT: '20', OTP_IP_RATE_LIMIT: '20' };
    for (let attempt = 1; attempt <= 3; attempt++) {
      const r = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': `10.20.5.${attempt}` },
        body: JSON.stringify({
          email: `mob_rl_${attempt}@example.com`,
          phone: '+91 98111 22244',
          turnstile_token: 'test_turnstile_pass'
        })
      }), mobLimitEnv, {});
      if (attempt <= 2) assert.strictEqual(r.status, 200, `Mobile attempt #${attempt} must succeed`);
      else assert.strictEqual(r.status, 429, 'Per-mobile rate limit must reject 3rd request with 429');
    }

    // 4c. Per-email rate limit
    createCleanMemoryReset();
    const emailLimitEnv = { ...baseEnv, OTP_EMAIL_RATE_LIMIT: '3', OTP_IP_RATE_LIMIT: '20', OTP_MOBILE_RATE_LIMIT: '20' };
    for (let attempt = 1; attempt <= 4; attempt++) {
      const r = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': `10.20.6.${attempt}` },
        body: JSON.stringify({
          email: 'same_target@example.com',
          turnstile_token: 'test_turnstile_pass'
        })
      }), emailLimitEnv, {});
      if (attempt <= 3) assert.strictEqual(r.status, 200, `Email attempt #${attempt} must succeed`);
      else assert.strictEqual(r.status, 429, 'Per-email rate limit must reject 4th request with 429');
    }

    // 4d. Per-IP rate limit
    createCleanMemoryReset();
    const ipLimitEnv = { ...baseEnv, OTP_IP_RATE_LIMIT: '3', OTP_EMAIL_RATE_LIMIT: '20', OTP_MOBILE_RATE_LIMIT: '20' };
    for (let attempt = 1; attempt <= 4; attempt++) {
      const r = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.20.7.99' },
        body: JSON.stringify({
          email: `ip_target_${attempt}@example.com`,
          turnstile_token: 'test_turnstile_pass'
        })
      }), ipLimitEnv, {});
      if (attempt <= 3) assert.strictEqual(r.status, 200, `IP attempt #${attempt} must succeed`);
      else assert.strictEqual(r.status, 429, 'Per-IP rate limit must reject 4th request with 429');
    }

    // 4e. Daily SMS cap (env-configurable, skips SMS when capped without blocking Email OTP)
    createCleanMemoryReset();
    const smsCapEnv = { ...baseEnv, SMS_DAILY_CAP: '2', OTP_IP_RATE_LIMIT: '20', OTP_EMAIL_RATE_LIMIT: '20', OTP_MOBILE_RATE_LIMIT: '20' };
    const smsCallsBeforeCap = brevoSmsCalls.length;
    for (let attempt = 1; attempt <= 3; attempt++) {
      const r = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': `10.20.8.${attempt}` },
        body: JSON.stringify({
          email: `cap_user_${attempt}@example.com`,
          phone: `+91982223330${attempt}`,
          turnstile_token: 'test_turnstile_pass'
        })
      }), smsCapEnv, {});
      assert.strictEqual(r.status, 200, 'Daily SMS cap must never block Email OTP');
      const d = await r.json();
      if (attempt <= 2) {
        assert.deepStrictEqual(d.channels_dispatched, { email: true, sms: true });
      } else {
        assert.deepStrictEqual(d.channels_dispatched, { email: true, sms: false });
      }
    }
    assert.strictEqual(brevoSmsCalls.length, smsCallsBeforeCap + 2, '3rd SMS must be skipped after SMS_DAILY_CAP=2');

    // 4f. +91 ^[6-9][0-9]{9}$ filter: non-India / invalid phones never trigger SMS, Email OTP still succeeds
    createCleanMemoryReset();
    const nonInPhones = ['+14155552671', '+447911123456', '+6591234567', '00919876543210', '09876543210', '5123456789', '98765'];
    const smsBeforeNonIn = brevoSmsCalls.length;
    for (let idx = 0; idx < nonInPhones.length; idx++) {
      const r = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': `10.20.9.${idx + 1}` },
        body: JSON.stringify({
          email: `intl_${idx}@example.com`,
          phone: nonInPhones[idx],
          turnstile_token: 'test_turnstile_pass'
        })
      }), baseEnv, {});
      assert.strictEqual(r.status, 200, `Phone=${nonInPhones[idx]} must still receive Email OTP`);
      const d = await r.json();
      assert.deepStrictEqual(d.channels_dispatched, { email: true, sms: false }, `Phone=${nonInPhones[idx]} must NOT receive SMS`);
    }
    assert.strictEqual(brevoSmsCalls.length, smsBeforeNonIn, 'Zero SMS calls permitted for non-+91 or invalid numbers');
    origInfo('  ✓ 4. Verified Turnstile gate, per-mobile/per-email/per-IP limits, SMS_DAILY_CAP, and strict +91 ^[6-9][0-9]{9}$ filter');

    // =========================================================================
    // 5. ZERO OTP / PHONE LEAKAGE IN LOGS, ANALYTICS & ERROR REPORTS
    // =========================================================================
    const allDispatchedOtps = brevoEmailCalls.map((c) => c.body.textContent.match(/\b(\d{6})\b/)[1]);
    const rawTestPhones = ['9876543210', '9876543239', '9765432188', '9811122244', '9822233301', '9822233302', '9822233303'];
    for (const entry of capturedLogs) {
      for (const otp of allDispatchedOtps) {
        assert(!entry.text.includes(otp), `Plaintext OTP leaked into console.${entry.level}: ${entry.text}`);
      }
      for (const ph of rawTestPhones) {
        assert(!entry.text.includes(ph), `Unmasked phone leaked into console.${entry.level}: ${entry.text}`);
        assert(!entry.text.includes(ph.slice(-4)), `Last-4 phone digits leaked into console.${entry.level} (must be last-2 only): ${entry.text}`);
      }
    }

    // Verify /api/v1/events rejects OTP codes and phone numbers
    const evtOtpReject = await worker.fetch(new Request('http://localhost/api/v1/events', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost',
        'X-Consent-Analytics': 'true'
      },
      body: JSON.stringify({ event_name: 'page_view', otp: '123456' })
    }), baseEnv, {});
    assert.strictEqual(evtOtpReject.status, 400, '/api/v1/events must reject otp key');

    const evtSixDigitReject = await worker.fetch(new Request('http://localhost/api/v1/events', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost',
        'X-Consent-Analytics': 'true'
      },
      body: JSON.stringify({ event_name: 'page_view', ref: '654321' })
    }), baseEnv, {});
    assert.strictEqual(evtSixDigitReject.status, 400, '/api/v1/events must reject 6-digit OTP value pattern');
    origInfo('  ✓ 5. Verified zero OTP codes or >2-digit phones in logs, error responses, or /api/v1/events analytics');

    // =========================================================================
    // 6. WORDING & DEFAULT SENDER STATIC VERIFICATION ACROSS CODEBASE
    // =========================================================================
    const filesToAudit = [
      'app/static/_worker.js',
      'app/services/otp_dispatcher.py',
      'app/static/your-reading.html',
      'app/static/charm_ai_chat.html',
      'app/static/login.html',
      'app/static/dashboard.html',
      '.env.example'
    ];
    for (const rel of filesToAudit) {
      const content = fs.readFileSync(path.resolve(rel), 'utf8');
      assert(!content.includes('NUMEROSVSN'), `Default sender NUMEROSVSN must be removed from ${rel}`);
      assert(!/mobile\s+is\s+verified|mobile\s+verified|phone\s+verified|verified\s+via\s+otp/i.test(content), `Forbidden mobile-verified wording found in ${rel}`);
    }
    const yrHtml = fs.readFileSync(path.resolve('app/static/your-reading.html'), 'utf8');
    const loginHtml = fs.readFileSync(path.resolve('app/static/login.html'), 'utf8');
    const charmHtml = fs.readFileSync(path.resolve('app/static/charm_ai_chat.html'), 'utf8');
    assert(yrHtml.includes('code sent to your email and mobile'), 'your-reading.html must use exact "code sent to your email and mobile" wording');
    assert(loginHtml.includes('code sent to your email and mobile'), 'login.html must use exact "code sent to your email and mobile" wording');
    assert(charmHtml.includes('Enter 6-digit code sent to') && charmHtml.includes('your email and mobile'), 'charm_ai_chat.html must render "code sent to your email and mobile"');
    origInfo('  ✓ 6. Verified zero NUMEROSVSN default, zero "mobile verified" wording, and exact "code sent to your email and mobile" copy');

    origInfo('\n[PASS] ALL BREVO SMS FOLLOW-UP & DUAL-CHANNEL OTP TESTS PASSED!');
  } finally {
    globalThis.fetch = origFetch;
    console.info = origInfo;
    console.warn = origWarn;
    console.error = origError;
  }
}

runBrevoDualChannelOtpSuite().catch((err) => {
  console.error('[FAIL]', err);
  process.exit(1);
});
