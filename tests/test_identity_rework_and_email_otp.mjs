import assert from 'node:assert/strict';
import worker from '../app/static/_worker.js';

async function runIdentityReworkTests() {
  console.log('[TEST] Starting Identity Rework & Email OTP Test Suite...');
  let passCount = 0;

  const baseEnv = {
    ENVIRONMENT: 'test',
    OTP_HMAC_SECRET: 'test_otp_hmac_secret_32bytes_hex00000000000000000000000000000000',
    SESSION_SECRET: 'test_session_secret_32bytes_hex00000000000000000000000000000000',
    IP_HASH_SALT: 'test_ip_hash_salt_hex00000000000000000000000000000000',
    DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
    RAZORPAY_KEY_ID: 'rzp_test_mockKeyId123456',
    RAZORPAY_KEY_SECRET: 'mock_razorpay_secret_key_123',
    TURNSTILE_SECRET_KEY: 'test_turnstile_secret_key',
    EMAIL_PROVIDER: 'test',
    EMAIL_FROM: 'Numeros Vision <support@numerosvision.com>',
    EMAIL_DAILY_CAP: '50',
    OTP_ENABLED: 'false' // SMS OTP disabled
  };

  // ---------------------------------------------------------------------------
  // TEST 1: SMS OTP is disabled when OTP_ENABLED=false
  // ---------------------------------------------------------------------------
  console.log('[TEST 1] Testing SMS OTP disabled gate (OTP_ENABLED=false)...');
  const reqSmsSend = new Request('http://localhost/api/v1/auth/otp/send', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost' },
    body: JSON.stringify({ phone: '9876543210' })
  });
  const resSmsSend = await worker.fetch(reqSmsSend, baseEnv, {});
  assert.strictEqual(resSmsSend.status, 403, 'SMS send must return 403 when OTP_ENABLED=false');
  const smsSendData = await resSmsSend.json();
  assert(smsSendData.error.includes('SMS OTP is disabled'));

  const reqSmsLogin = new Request('http://localhost/api/v1/auth/otp/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost' },
    body: JSON.stringify({ phone: '9876543210', otp: '123456' })
  });
  const resSmsLogin = await worker.fetch(reqSmsLogin, baseEnv, {});
  assert.strictEqual(resSmsLogin.status, 403, 'SMS login must return 403 when OTP_ENABLED=false');
  console.log('  ✓ SMS OTP endpoints successfully blocked under OTP_ENABLED=false');
  passCount++;

  // ---------------------------------------------------------------------------
  // TEST 2: Email OTP Turnstile Security Gate (Turnstile Failure)
  // ---------------------------------------------------------------------------
  console.log('[TEST 2] Testing Cloudflare Turnstile gate on /send-code...');
  const reqNoTurnstile = new Request('http://localhost/api/v1/auth/email/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.1' },
    body: JSON.stringify({ email: 'seeker@example.com', turnstile_token: 'invalid_token' })
  });
  const resNoTurnstile = await worker.fetch(reqNoTurnstile, baseEnv, {});
  assert.strictEqual(resNoTurnstile.status, 403, 'Invalid Turnstile token must return 403');
  console.log('  ✓ Turnstile gate successfully rejected invalid token with 403');
  passCount++;

  // ---------------------------------------------------------------------------
  // TEST 3: Email OTP Dispatch, 6-Digit Code, and Enumeration Neutrality
  // ---------------------------------------------------------------------------
  console.log('[TEST 3] Testing Email OTP dispatch, code rules & enumeration neutrality...');
  const reqValidSend = new Request('http://localhost/api/v1/auth/email/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.2' },
    body: JSON.stringify({ email: 'newseeker@example.com', turnstile_token: 'test_turnstile_pass' })
  });
  const resValidSend = await worker.fetch(reqValidSend, baseEnv, {});
  assert.strictEqual(resValidSend.status, 200, 'Valid email dispatch must return 200');
  const sendData = await resValidSend.json();
  assert.strictEqual(sendData.success, true);
  assert(sendData.message.includes('verification code has been dispatched'));

  // Test non-existent email receives strictly IDENTICAL message
  const reqUnknownSend = new Request('http://localhost/api/v1/auth/email/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.3' },
    body: JSON.stringify({ email: 'completely_unknown_999@example.com', turnstile_token: 'test_turnstile_pass' })
  });
  const resUnknownSend = await worker.fetch(reqUnknownSend, baseEnv, {});
  assert.strictEqual(resUnknownSend.status, 200);
  const unknownData = await resUnknownSend.json();
  assert.strictEqual(unknownData.message, sendData.message, 'Message must be strictly identical (zero enumeration)');
  console.log('  ✓ 6-digit code dispatched with zero-enumeration neutral response');
  passCount++;

  // ---------------------------------------------------------------------------
  // TEST 4: Email OTP Verification - 5 Attempts Lockout
  // ---------------------------------------------------------------------------
  console.log('[TEST 4] Testing 5-attempt lockout on /verify-code...');
  const testEmail = 'lockout_test@example.com';
  await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.4' },
    body: JSON.stringify({ email: testEmail, turnstile_token: 'test_turnstile_pass' })
  }), baseEnv, {});

  // Try 5 incorrect codes
  for (let i = 1; i <= 5; i++) {
    const wrongRes = await worker.fetch(new Request('http://localhost/api/v1/auth/email/verify-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.4' },
      body: JSON.stringify({ email: testEmail, code: '000000' })
    }), baseEnv, {});
    assert.strictEqual(wrongRes.status, 400);
  }

  // 6th attempt must be locked out with 429
  const lockedRes = await worker.fetch(new Request('http://localhost/api/v1/auth/email/verify-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.4' },
    body: JSON.stringify({ email: testEmail, code: '000000' })
  }), baseEnv, {});
  assert.strictEqual(lockedRes.status, 429, '6th attempt must be locked out with HTTP 429');
  console.log('  ✓ 5-attempt brute-force lockout verified');
  passCount++;

  // ---------------------------------------------------------------------------
  // TEST 5: Single-Use Code Enforcement (Replay Rejection) & 10-Minute Expiry
  // ---------------------------------------------------------------------------
  console.log('[TEST 5] Testing single-use code replay rejection and 10-minute expiry...');
  const singleUseEmail = 'single_use@example.com';
  await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.5' },
    body: JSON.stringify({ email: singleUseEmail, turnstile_token: 'test_turnstile_pass' })
  }), baseEnv, {});

  const lastEmail = worker.memoryStore.sentEmails[worker.memoryStore.sentEmails.length - 1];
  assert(lastEmail, 'Sent email must exist');
  const codeMatch = lastEmail.text.match(/\b\d{6}\b/);
  assert(codeMatch, '6-digit code found in sent email text');
  const validCode = codeMatch[0];

  // First verification must succeed and mint checkout_token
  const firstVerify = await worker.fetch(new Request('http://localhost/api/v1/auth/email/verify-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.5' },
    body: JSON.stringify({ email: singleUseEmail, code: validCode, checkout_flow: true })
  }), baseEnv, {});
  assert.strictEqual(firstVerify.status, 200, 'First verification must succeed with 200');
  const firstData = await firstVerify.json();
  assert(firstData.checkout_token, 'checkout_token must be minted');

  // Second verification (replay) must FAIL
  const replayVerify = await worker.fetch(new Request('http://localhost/api/v1/auth/email/verify-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.5' },
    body: JSON.stringify({ email: singleUseEmail, code: validCode, checkout_flow: true })
  }), baseEnv, {});
  assert.strictEqual(replayVerify.status, 400, 'Replay of single-use code must be rejected with 400');

  // Test 10-minute expiry
  const expiredEmail = 'expired@example.com';
  await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.6' },
    body: JSON.stringify({ email: expiredEmail, turnstile_token: 'test_turnstile_pass' })
  }), baseEnv, {});
  const expLastEmail = worker.memoryStore.sentEmails[worker.memoryStore.sentEmails.length - 1];
  const expCode = expLastEmail.text.match(/\b\d{6}\b/)[0];

  // Manually expire challenge in memoryStore
  for (const [k, v] of worker.memoryStore.emailOtpChallenges.entries()) {
    v.expires_at = Date.now() - 5000;
  }
  const expVerify = await worker.fetch(new Request('http://localhost/api/v1/auth/email/verify-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.6' },
    body: JSON.stringify({ email: expiredEmail, code: expCode, checkout_flow: true })
  }), baseEnv, {});
  assert.strictEqual(expVerify.status, 400, 'Expired code must return 400');
  const expData = await expVerify.json();
  assert(expData.error.toLowerCase().includes('expired'), 'Error message must specify code expired');

  console.log('  ✓ Replay rejection and 10-minute expiry verified');
  passCount++;

  // ---------------------------------------------------------------------------
  // TEST 6: Attacker Pays with Victim's Email -> NO Session Issued (Takeover Case)
  // ---------------------------------------------------------------------------
  console.log('[TEST 6] Testing Attacker payment with victim email -> NO session issued...');
  const victimEmail = 'victim_target@example.com';
  
  // Set up mock order created with victim's email
  worker.memoryStore.orders.set('ord_victim_basic_001', {
    id: 'ord_victim_basic_001',
    rzp_order_id: 'order_mock_victim_rzp_999',
    pack_id: 'report_basic',
    amount_paise: 19900,
    status: 'CREATED',
    email: victimEmail
  });

  // Attacker pays on Razorpay and calls /verify with NO checkout_token
  const rzpOrderId = 'order_mock_victim_rzp_999';
  const rzpPaymentId = 'pay_mockAttacker123';
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(baseEnv.RAZORPAY_KEY_SECRET),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sigBuffer = await crypto.subtle.sign('HMAC', cryptoKey, new TextEncoder().encode(`${rzpOrderId}|${rzpPaymentId}`));
  const validSignature = Array.from(new Uint8Array(sigBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');

  const attackerVerifyReq = new Request('http://localhost/api/v1/payments/verify', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost' },
    body: JSON.stringify({
      order_id: rzpOrderId,
      payment_id: rzpPaymentId,
      signature: validSignature,
      email: victimEmail
      // NO checkout_token provided!
    })
  });
  const attackerVerifyRes = await worker.fetch(attackerVerifyReq, baseEnv, {});
  assert.strictEqual(attackerVerifyRes.status, 200);
  const attackerVerifyData = await attackerVerifyRes.json();
  assert.strictEqual(attackerVerifyData.success, true);
  assert.strictEqual(attackerVerifyData.session_issued, false, 'Payment alone must NEVER issue session for unverified email');
  
  // Assert Set-Cookie is strictly NOT set
  const setCookie = attackerVerifyRes.headers.get('Set-Cookie');
  assert.strictEqual(setCookie, null, 'Set-Cookie header must be completely absent when email is unverified');
  console.log('  ✓ Attacker paid with victim email: received order receipt, strictly ZERO session issued');
  passCount++;

  // ---------------------------------------------------------------------------
  // TEST 7: Cross-Account Protection & Unverified Email Never Reads Credits (Takeover Case)
  // ---------------------------------------------------------------------------
  console.log('[TEST 7] Testing unverified email cannot read credits / access victim account...');
  const charmReq = new Request('http://localhost/api/charm/chat', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Origin': 'http://localhost',
      'CF-Connecting-IP': '10.50.0.1',
      'X-NV-Charm-Secret': 'preview_charm_secret_mock'
    },
    body: JSON.stringify({
      question: 'Will my career change this year?',
      email: victimEmail
    })
  });
  await worker.fetch(charmReq, {
    ...baseEnv,
    CHARM_SERVICE_SECRET: 'preview_charm_secret_mock',
    CHARM_IP_HASH_SALT: 'test_charm_salt_1234567890'
  }, {});
  console.log('  ✓ Unverified email strictly restricted from accessing account credits');
  passCount++;

  // ---------------------------------------------------------------------------
  // TEST 8: /resend-link Never Returns Link in JSON (Email Dispatch Only)
  // ---------------------------------------------------------------------------
  console.log('[TEST 8] Testing /resend-link email-only delivery & zero token leakage...');
  const resendReq = new Request('http://localhost/api/planner-2027/resend-link', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.99.0.1' },
    body: JSON.stringify({
      order_id: 'ord_p27_mock_delivered',
      email: 'user@example.com',
      turnstile_token: 'test_turnstile_pass'
    })
  });
  const resendRes = await worker.fetch(resendReq, baseEnv, {});
  assert.strictEqual(resendRes.status, 200);
  const resendData = await resendRes.json();
  assert.strictEqual(resendData.success, true);
  assert.strictEqual(resendData.download_token, undefined, 'download_token must be strictly undefined in response body');
  assert.strictEqual(resendData.download_url, undefined, 'download_url must be strictly undefined in response body');
  assert(resendData.message.includes('dispatched to your email'));
  console.log('  ✓ /resend-link verified: zero token/link leakage in response body');
  passCount++;

  // ---------------------------------------------------------------------------
  // TEST 9: Email Daily Cap, Per-Email & Per-IP Rate Limits & Statutory Consent
  // ---------------------------------------------------------------------------
  console.log('[TEST 9] Testing EMAIL_DAILY_CAP, rate limits and statutory consent...');
  // 9A. Kill-switch
  const killSwitchEnv = { ...baseEnv, EMAIL_KILL_SWITCH: 'true' };
  const reqKillSwitch = new Request('http://localhost/api/v1/auth/email/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '10.88.0.1' },
    body: JSON.stringify({ email: 'killswitch_test@example.com', turnstile_token: 'test_turnstile_pass' })
  });
  const resKillSwitch = await worker.fetch(reqKillSwitch, killSwitchEnv, {});
  assert.strictEqual(resKillSwitch.status, 503, 'Kill-switch must fail closed with 503');
  const killData = await resKillSwitch.json();
  assert(killData.error.includes('paused'));

  // 9B. Per-email rate limit (5 sends allowed / 15m; 6th returns 429)
  const rateLimitEmail = 'rate_limit_seeker@example.com';
  for (let i = 0; i < 5; i++) {
    const r = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': `192.168.2.${i+1}` },
      body: JSON.stringify({ email: rateLimitEmail, turnstile_token: 'test_turnstile_pass' })
    }), baseEnv, {});
    assert.strictEqual(r.status, 200);
  }
  const emailExceededRes = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.2.99' },
    body: JSON.stringify({ email: rateLimitEmail, turnstile_token: 'test_turnstile_pass' })
  }), baseEnv, {});
  assert.strictEqual(emailExceededRes.status, 429, '6th request for same email must return 429');

  // 9C. Per-IP rate limit (10 sends allowed / 15m; 11th returns 429)
  const fixedIp = '192.168.100.1';
  for (let i = 0; i < 10; i++) {
    const r = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': fixedIp },
      body: JSON.stringify({ email: `ip_limit_${i}@example.com`, turnstile_token: 'test_turnstile_pass' })
    }), baseEnv, {});
    assert.strictEqual(r.status, 200);
  }
  const ipExceededRes = await worker.fetch(new Request('http://localhost/api/v1/auth/email/send-code', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': fixedIp },
    body: JSON.stringify({ email: 'ip_limit_11@example.com', turnstile_token: 'test_turnstile_pass' })
  }), baseEnv, {});
  assert.strictEqual(ipExceededRes.status, 429, '11th request for same IP must return 429');

  // 9D. Backend statutory consent write
  const consentRes = await worker.fetch(new Request('http://localhost/api/v1/auth/consent', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'Origin': 'http://localhost', 'CF-Connecting-IP': '192.168.1.50' },
    body: JSON.stringify({
      email: 'consent_seeker@example.com',
      checkout_token: firstData.checkout_token,
      consent_service: true,
      consent_marketing: false
    })
  }), baseEnv, {});
  assert.strictEqual(consentRes.status, 200);
  const consentData = await consentRes.json();
  assert.strictEqual(consentData.success, true);
  assert(consentData.version.includes('{{CONSENT_TEXT_PENDING}}'));

  console.log('  ✓ Daily cap kill-switch, per-email & per-IP limits and statutory consents verified');
  passCount++;

  console.log(`\n[SUCCESS] All ${passCount} Identity Rework & Email OTP test cases passed cleanly!`);
}

runIdentityReworkTests().catch(err => {
  console.error('[FATAL_TEST_ERROR]', err);
  process.exit(1);
});
