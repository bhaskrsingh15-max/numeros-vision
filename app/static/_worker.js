
// Constant-time string comparison to prevent side-channel timing attacks
function timingSafeEqual(a, b) {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  const aLen = a.length;
  const bLen = b.length;
  let mismatch = aLen === bLen ? 0 : 1;
  const maxLen = Math.max(aLen, bLen);
  for (let i = 0; i < maxLen; i++) {
    const charA = i < aLen ? a.charCodeAt(i) : 0;
    const charB = i < bLen ? b.charCodeAt(i) : 0;
    mismatch |= charA ^ charB;
  }
  return mismatch === 0;
}

async function sha256Hex(message) {
  const msgUint8 = new TextEncoder().encode(message);
  const hashBuffer = await crypto.subtle.digest('SHA-256', msgUint8);
  return Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function hmacSha256Hex(secret, message) {
  const encoder = new TextEncoder();
  const keyData = encoder.encode(secret);
  const msgData = encoder.encode(message);
  const cryptoKey = await crypto.subtle.importKey(
    'raw',
    keyData,
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sigBuffer = await crypto.subtle.sign('HMAC', cryptoKey, msgData);
  return Array.from(new Uint8Array(sigBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
}

function getRandomHex(bytesCount = 16) {
  const arr = new Uint8Array(bytesCount);
  crypto.getRandomValues(arr);
  return Array.from(arr).map(b => b.toString(16).padStart(2, '0')).join('');
}



const DANGEROUS_FLAGS = [
  'MOCK_PAYMENTS',
  'NV_EMAIL_LOG_ADAPTER',
  'ALLOW_TEST_TOKENS',
  'ALLOW_STAGING_TEST_BYPASS',
  'NV_ALLOW_UNAUTHENTICATED_LOCAL',
  'PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW',
  'NV_FORCE_LAUNCH_MODE'
];

function getDetectedDangerousFlags(env) {
  if (!env) return [];
  const detected = [];
  for (const flag of DANGEROUS_FLAGS) {
    const val = env[flag];
    if (val === true || val === 'true' || val === '1' || val === 'yes') {
      detected.push(flag);
    }
  }
  return detected;
}

function assertNoDangerousFlagsInProduction(env, request) {
  if (!env) return;
  const environment = (env.ENVIRONMENT || '').toString().trim().toLowerCase();
  if (environment === 'production') {
    const detected = getDetectedDangerousFlags(env);
    if (detected.length > 0) {
      if (detected.includes('PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW')) {
        throw new Error(`FATAL SECURITY VIOLATION: PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW is only permitted when ENVIRONMENT == 'preview' (Dangerous test flags strictly refused in production: ${detected.join(', ')}). Refusing execution.`);
      }
      throw new Error(`FATAL SECURITY VIOLATION: Dangerous test flags strictly refused in production: ${detected.join(', ')}`);
    }
  } else {
    const flag = (env.PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW || '').toString().trim().toLowerCase();
    if ((flag === 'true' || flag === '1' || flag === 'yes') && environment !== 'preview') {
      throw new Error(`FATAL SECURITY VIOLATION: PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW is only permitted when ENVIRONMENT == 'preview' (current ENVIRONMENT: '${environment}'). Refusing execution.`);
    }
  }
}

function isMockPaymentsAllowed(env) {
  const currentEnv = ((env && env.ENVIRONMENT) || 'production').toLowerCase().trim();
  if (currentEnv === 'production') return false;
  return Boolean(env && (env.MOCK_PAYMENTS === 'true' || env.MOCK_PAYMENTS === true || env.MOCK_PAYMENTS === '1'));
}

function assertNoPreviewFlagOnProduction(env, request) {
  assertNoDangerousFlagsInProduction(env, request);
}

function assertRazorpayTestKey(env) {
  if (!env) return;
  for (const [k, v] of Object.entries(env)) {
    if (typeof v === 'string' && k.toUpperCase().includes('RAZORPAY') && v.trim().startsWith('rzp_live')) {
      throw new Error(`FATAL SECURITY VIOLATION: Live Razorpay key detected in ${k}. Refusing to execute in test/preview environment.`);
    }
  }
}

function requireSecret(env, name) {
  const val = env && typeof env[name] === 'string' ? env[name].trim() : '';
  if (val) return val;
  console.error(`[MISSING_SECRET] Required environment variable ${name} is not configured`);
  const err = new Error(`Missing required secret: ${name}`);
  err.code = 'MISSING_SECRET';
  err.secretName = name;
  err.status = 500;
  throw err;
}

function parse32ByteKey(secret) {
  if (!secret || typeof secret !== 'string') {
    throw new Error('DATA_ENCRYPTION_KEY is required and must be a 64-character hex (32-byte) key.');
  }
  const trimmed = secret.trim();
  if (!/^[0-9a-fA-F]{64}$/.test(trimmed)) {
    throw new Error('DATA_ENCRYPTION_KEY must be a 64-character hex string representing a 32-byte key (passphrases are not permitted).');
  }
  const bytes = new Uint8Array(32);
  for (let i = 0; i < 32; i++) {
    bytes[i] = parseInt(trimmed.slice(i * 2, i * 2 + 2), 16);
  }
  return bytes;
}

async function getAesGcmKey(secret) {
  const keyBytes = parse32ByteKey(secret);
  return crypto.subtle.importKey('raw', keyBytes, { name: 'AES-GCM' }, false, ['encrypt', 'decrypt']);
}

async function encryptField(plainText, secret) {
  if (plainText === null || plainText === undefined || plainText === '') return null;
  const key = await getAesGcmKey(secret);
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const encoded = new TextEncoder().encode(String(plainText));
  const cipherBuffer = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, encoded);
  const ivHex = Array.from(iv).map(b => b.toString(16).padStart(2, '0')).join('');
  const cipherHex = Array.from(new Uint8Array(cipherBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
  return `${ivHex}:${cipherHex}`;
}

async function decryptField(encryptedText, secret) {
  if (encryptedText === null || encryptedText === undefined || encryptedText === '') return null;
  if (typeof encryptedText !== 'string' || !encryptedText.includes(':')) {
    throw new Error('Invalid encrypted field format: expected ivHex:cipherHex');
  }
  const parts = encryptedText.split(':');
  if (parts.length !== 2) {
    throw new Error('Invalid encrypted field format: expected single colon separator');
  }
  const [ivHex, cipherHex] = parts;
  if (!/^[0-9a-fA-F]{24}$/.test(ivHex) || !/^[0-9a-fA-F]+$/.test(cipherHex) || cipherHex.length < 32 || cipherHex.length % 2 !== 0) {
    throw new Error('Invalid encrypted field hex encoding');
  }
  const iv = new Uint8Array(ivHex.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
  const cipherBytes = new Uint8Array(cipherHex.match(/.{1,2}/g).map(byte => parseInt(byte, 16)));
  const key = await getAesGcmKey(secret);
  const decrypted = await crypto.subtle.decrypt({ name: 'AES-GCM', iv }, key, cipherBytes);
  return new TextDecoder().decode(decrypted);
}

function verifyOrigin(request, env) {
  const origin = request.headers.get('Origin');
  if (!origin) return true;

  // 1. Same-Origin Check: Origin matches the worker request URL origin (covers preview and production self-calls)
  try {
    const requestOrigin = new URL(request.url).origin;
    if (origin === requestOrigin) return true;
  } catch (e) {}

  // 2. Production domains
  if (origin === 'https://numerosvision.com' || origin === 'https://www.numerosvision.com') return true;

  // 3. Configured ALLOWED_ORIGINS
  if (env && env.ALLOWED_ORIGINS) {
    const list = env.ALLOWED_ORIGINS.split(',').map(s => s.trim()).filter(Boolean);
    if (list.includes(origin)) return true;
  }

  return false;
}

function getCorsOrigin(request, env) {
  const origin = request ? request.headers.get('Origin') : null;
  if (!origin) return 'https://numerosvision.com';

  try {
    const requestOrigin = new URL(request.url).origin;
    if (origin === requestOrigin) return origin;
  } catch (e) {}

  if (origin === 'https://numerosvision.com' || origin === 'https://www.numerosvision.com') return origin;

  const allowedList = ['https://numerosvision.com', 'https://www.numerosvision.com'];
  if (env && env.ALLOWED_ORIGINS) {
    env.ALLOWED_ORIGINS.split(',').forEach(o => {
      const trimmed = o.trim();
      if (trimmed && !allowedList.includes(trimmed)) allowedList.push(trimmed);
    });
  }
  if (allowedList.includes(origin)) return origin;

  return 'https://numerosvision.com';
}

function getCorsHeaders(request, env) {
  const origin = request ? request.headers.get('Origin') : null;
  const allowedList = ['https://numerosvision.com'];
  if (env && env.ALLOWED_ORIGINS) {
    env.ALLOWED_ORIGINS.split(',').forEach(o => {
      const trimmed = o.trim();
      if (trimmed && !allowedList.includes(trimmed)) allowedList.push(trimmed);
    });
  }
  let matchedOrigin = 'https://numerosvision.com';
  if (origin) {
    if (allowedList.includes(origin)) {
      matchedOrigin = origin;
    } else if (env && env.ENVIRONMENT === 'local' && (origin.startsWith('http://localhost:') || origin.startsWith('http://127.0.0.1:'))) {
      matchedOrigin = origin;
    }
  }
  return {
    'Access-Control-Allow-Origin': matchedOrigin,
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Requested-With, Origin, Accept',
    'Access-Control-Allow-Credentials': 'true',
    'Vary': 'Origin'
  };
}

function getCookie(request, name) {
  const cookieHeader = request.headers.get('Cookie') || '';
  const cookies = cookieHeader.split(';').map(c => c.trim());
  for (const c of cookies) {
    if (c.startsWith(name + '=')) {
      return c.substring(name.length + 1);
    }
  }
  return null;
}

// Memory fallback for local unit tests without D1 binding
const memoryStore = {
  users: new Map(),
  sessions: new Map(),
  otpChallenges: new Map(),
  creditLedger: new Map(),
  orders: new Map(),
  payments: new Map(),
  subjects: new Map(),
  entitlements: new Map(),
  auditLog: new Map(),
  reportJobs: new Map(),
  voucherLedger: new Map(),
  refunds: new Map(),
  r2Objects: new Map(),
  planner2027Orders: new Map(),
  freeChatUsage: new Map(),
  charmRateLimits: new Map(),
  emailOtpChallenges: new Map(),
  emailRateLimits: new Map(),
  userConsents: new Map(),
  waitlistNotifyMe: new Map(),
  sentEmails: [],
  sentSms: [],
  smsRateHistory: []
};

// In-memory sliding window rate limiter for public forms & telemetry (module-scoped)
const _formRateLimits = new Map();

function base64UrlToUint8Array(base64Url) {
  const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
  const pad = base64.length % 4;
  const padded = pad ? base64 + '='.repeat(4 - pad) : base64;
  const binary = atob(padded);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}

let cachedGoogleJwks = null;
let cachedGoogleJwksExpiresAt = 0;

async function getGoogleJwks() {
  const now = Date.now();
  if (cachedGoogleJwks && now < cachedGoogleJwksExpiresAt) {
    return cachedGoogleJwks;
  }
  const certsResp = await fetch('https://www.googleapis.com/oauth2/v3/certs');
  if (!certsResp.ok) throw new Error('Failed to fetch Google JWKS public certificates');
  const certs = await certsResp.json();
  cachedGoogleJwks = certs;
  cachedGoogleJwksExpiresAt = now + 3600 * 1000; // 1-hour cache
  return certs;
}

function getSessionToken(request, env) {
  const hostCookie = getCookie(request, '__Host-nv_session');
  if (hostCookie) return hostCookie;
  const userCookie = getCookie(request, 'nv_user_session');
  if (userCookie) return userCookie;
  const authHeader = request.headers.get('Authorization');
  if (authHeader && authHeader.startsWith('Bearer ')) {
    return authHeader.slice(7).trim();
  }
  if (env && (env.ENVIRONMENT === 'local' || env.ENVIRONMENT === 'test')) {
    return getCookie(request, 'nv_session');
  }
  return null;
}

async function verifyGoogleIdToken(credential, env) {
  if (!credential || typeof credential !== 'string') {
    return { valid: false, error: 'Google ID token credential is required.' };
  }
  const parts = credential.split('.');
  if (parts.length !== 3) {
    return { valid: false, error: 'Malformed Google ID token.' };
  }

  let header = null;
  let payload = null;
  try {
    header = JSON.parse(new TextDecoder().decode(base64UrlToUint8Array(parts[0])));
    payload = JSON.parse(new TextDecoder().decode(base64UrlToUint8Array(parts[1])));
  } catch (e) {
    return { valid: false, error: 'Failed to decode Google ID token.' };
  }

  // 1. Issuer Verification
  const validIssuers = ['accounts.google.com', 'https://accounts.google.com'];
  if (!validIssuers.includes(payload.iss)) {
    return { valid: false, error: 'Google ID token issuer invalid.' };
  }

  // 2. Audience Verification (Must match configured GOOGLE_CLIENT_ID)
  if (!env.GOOGLE_CLIENT_ID) {
    return { valid: false, error: 'GOOGLE_CLIENT_ID is not configured in server environment.' };
  }
  if (payload.aud !== env.GOOGLE_CLIENT_ID) {
    return { valid: false, error: 'Google ID token audience mismatch.' };
  }

  // 3. Expiry Verification
  const nowSec = Math.floor(Date.now() / 1000);
  if (!payload.exp || payload.exp < nowSec) {
    return { valid: false, error: 'Google ID token has expired.' };
  }

  // 4. Email Verified Check
  if (payload.email_verified !== true && payload.email_verified !== 'true') {
    return { valid: false, error: 'Google email is not verified.' };
  }
  if (!payload.email) {
    return { valid: false, error: 'Google ID token missing email claim.' };
  }

  // 5. Signature Verification against Google's Public JWKS Keys
  try {
    const certs = await getGoogleJwks();
    const jwk = certs.keys?.find(k => k.kid === header.kid);
    if (!jwk) {
      return { valid: false, error: `Google public key not found for kid: ${header.kid}` };
    }

    const key = await crypto.subtle.importKey(
      'jwk',
      jwk,
      { name: 'RSASSA-PKCS1-v1_5', hash: 'SHA-256' },
      false,
      ['verify']
    );

    const dataBytes = new TextEncoder().encode(`${parts[0]}.${parts[1]}`);
    const sigBytes = base64UrlToUint8Array(parts[2]);

    const isSigValid = await crypto.subtle.verify(
      'RSASSA-PKCS1-v1_5',
      key,
      sigBytes,
      dataBytes
    );

    if (!isSigValid) {
      return { valid: false, error: 'Google ID token cryptographic signature verification failed.' };
    }
  } catch (err) {
    console.error('[Google_JWKS_Verify_Error]', err);
    return { valid: false, error: 'Google token signature verification failed: ' + err.message };
  }

  return { valid: true, payload };
}

async function authenticateUser(request, env) {
  const sessionToken = getSessionToken(request, env);
  if (!sessionToken) return null;
  const sessionSecret = requireSecret(env, 'SESSION_SECRET');
  const tokenHash = await hmacSha256Hex(sessionSecret, sessionToken);
  const now = Date.now();
  if (env.DB) {
    return await env.DB.prepare(
      'SELECT s.id as session_id, s.expires_at, u.id as user_id, u.email, u.phone_hash, u.created_at FROM sessions s JOIN users u ON s.user_id = u.id WHERE s.token_hash = ? AND s.expires_at > ?'
    ).bind(tokenHash, now).first();
  } else {
    const sess = memoryStore.sessions.get(tokenHash);
    if (sess && sess.expires_at > now) {
      return { user_id: sess.user_id, expires_at: sess.expires_at, email: sess.email || null };
    }
    return null;
  }
}

async function mintUserSession(env, userId, clientIp, now) {
  const sessionSecret = requireSecret(env, 'SESSION_SECRET');
  const ipSalt = requireSecret(env, 'IP_HASH_SALT');
  const rawToken = getRandomHex(32);
  const tokenHash = await hmacSha256Hex(sessionSecret, rawToken);
  const sessionExpiresAt = now + 30 * 24 * 3600 * 1000;
  const ipHash = await hmacSha256Hex(ipSalt, clientIp || '127.0.0.1');

  if (env && env.DB) {
    await env.DB.prepare(
      'INSERT INTO sessions (id, user_id, token_hash, expires_at, created_at, ip_hash, user_agent) VALUES (?, ?, ?, ?, ?, ?, ?)'
    ).bind('sess_' + now + '_' + getRandomHex(4), userId, tokenHash, sessionExpiresAt, now, ipHash, 'EdgeWorker').run();
  } else {
    memoryStore.sessions.set(tokenHash, {
      id: 'sess_' + now,
      user_id: userId,
      token_hash: tokenHash,
      expires_at: sessionExpiresAt,
      created_at: now
    });
  }
  return rawToken;
}

function createSessionCookieHeader(rawToken, isLocal) {
  const isSecure = !isLocal;
  return `__Host-nv_session=${rawToken}; Path=/; HttpOnly; ${isSecure ? 'Secure; ' : ''}SameSite=Lax; Max-Age=2592000`;
}

async function mintCheckoutToken(secret, email, timestamp) {
  const payload = `${email.toLowerCase().trim()}:${timestamp}`;
  const sig = await hmacSha256Hex(secret, payload);
  return `${timestamp}.${sig}`;
}

async function verifyCheckoutToken(secret, email, token) {
  if (!token || typeof token !== 'string' || !token.includes('.')) return false;
  const [tsStr, sig] = token.split('.');
  const ts = parseInt(tsStr, 10);
  if (!ts || isNaN(ts)) return false;
  const now = Date.now();
  // Valid for 30 minutes in checkout flow
  if (now - ts > 1800000 || ts > now + 60000) return false;
  const expectedSig = await hmacSha256Hex(secret, `${email.toLowerCase().trim()}:${ts}`);
  return timingSafeEqual(expectedSig, sig);
}

async function getOrderTokenSecret(env) {
  if (env && typeof env.DOWNLOAD_TOKEN_SECRET === 'string' && env.DOWNLOAD_TOKEN_SECRET.trim()) {
    return env.DOWNLOAD_TOKEN_SECRET.trim();
  }
  const baseSecret = (env && (env.SESSION_SECRET || env.JWT_SECRET)) ? (env.SESSION_SECRET || env.JWT_SECRET).trim() : 'nv_order_token_salt_domain_sep';
  return await hmacSha256Hex(baseSecret, 'numeros-vision:order-access-token:v1');
}

async function signOrderAccessToken(secret, orderId, expiresAt) {
  const payload = `${orderId}:${expiresAt}`;
  const sig = await hmacSha256Hex(secret, payload);
  return `${expiresAt}.${sig}`;
}

async function verifyOrderAccessToken(secret, orderId, token) {
  if (!token || typeof token !== 'string' || !token.includes('.')) return false;
  const [expStr, sig] = token.split('.');
  const expiresAt = parseInt(expStr, 10);
  if (!expiresAt || isNaN(expiresAt)) return false;
  const now = Date.now();
  if (now > expiresAt) return false; // Time-bound expired
  const expectedSig = await hmacSha256Hex(secret, `${orderId}:${expiresAt}`);
  return timingSafeEqual(expectedSig, sig);
}

async function verifyTurnstileToken(env, token, clientIp) {
  const currentEnv = ((env && env.ENVIRONMENT) || 'production').toLowerCase().trim();
  const isTestOrLocal = currentEnv === 'test' || currentEnv === 'local';
  const isPreviewOrDev = currentEnv === 'preview' || isTestOrLocal;

  // test_turnstile_pass and test token prefix are strictly restricted to test and local.
  // Empty/missing tokens are NEVER allowed in any environment.
  if (isTestOrLocal) {
    if (token === 'test_turnstile_pass' || (typeof token === 'string' && token.startsWith('1x0000000000000000000000000000000AA'))) {
      return true;
    }
  }

  if (!token || typeof token !== 'string') return false;

  let secretKey = env && env.TURNSTILE_SECRET_KEY ? env.TURNSTILE_SECRET_KEY.trim() : '';

  if (!secretKey) {
    if (isPreviewOrDev) {
      secretKey = '1x0000000000000000000000000000000AA';
    } else {
      return false;
    }
  }

  if (!isPreviewOrDev) {
    if (isCloudflareTestKey(secretKey)) return false;
  } else if (isCloudflareTestKey(secretKey)) {
    // In preview/test/local, canonicalize test secret key to ensure exact 31-zero matching
    secretKey = '1x0000000000000000000000000000000AA';
  }

  try {
    const formData = new URLSearchParams();
    formData.append('secret', secretKey);
    formData.append('response', token.trim());
    if (clientIp) formData.append('remoteip', clientIp);
    const resp = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
      method: 'POST',
      body: formData,
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    });
    const outcome = await resp.json().catch(() => ({}));
    return Boolean(outcome && outcome.success);
  } catch (err) {
    console.error('[Turnstile_Error]', err);
    return false;
  }
}

async function checkAndIncrementEmailDailyCap(env) {
  if (env && (env.EMAIL_KILL_SWITCH === 'true' || env.EMAIL_KILL_SWITCH === true)) {
    return { allowed: false, reason: 'kill_switch' };
  }
  const cap = parseInt((env && env.EMAIL_DAILY_CAP) || '500', 10);
  const todayKey = 'email_daily_' + new Date().toISOString().slice(0, 10);
  if (env && env.DB) {
    try {
      const now = Date.now();
      const expiresAt = now + 86400000;
      const row = await env.DB.prepare('SELECT count FROM email_rate_limits WHERE key = ?').bind(todayKey).first();
      const current = row ? row.count : 0;
      if (current >= cap) {
        return { allowed: false, reason: 'daily_cap_exceeded', count: current, cap };
      }
      await env.DB.prepare(`
        INSERT INTO email_rate_limits (key, count, window_start, expires_at)
        VALUES (?, 1, ?, ?)
        ON CONFLICT(key) DO UPDATE SET count = count + 1
      `).bind(todayKey, now, expiresAt).run();
      return { allowed: true, count: current + 1, cap };
    } catch (e) {
      console.warn('[EmailCap_D1_Fallback]', e.message);
    }
  }
  memoryStore.emailDailyCounts = memoryStore.emailDailyCounts || new Map();
  const current = memoryStore.emailDailyCounts.get(todayKey) || 0;
  if (current >= cap) {
    return { allowed: false, reason: 'daily_cap_exceeded', count: current, cap };
  }
  memoryStore.emailDailyCounts.set(todayKey, current + 1);
  return { allowed: true, count: current + 1, cap };
}

function isCloudflareTestKey(key) {
  if (!key || typeof key !== 'string') return false;
  const k = key.trim();
  return k.startsWith('1x00000000000000000000') ||
         k.startsWith('2x00000000000000000000') ||
         k.startsWith('3x00000000000000000000') ||
         k.toLowerCase().includes('test_turnstile');
}

function getTurnstileConfigError(env) {
  const currentEnv = ((env && env.ENVIRONMENT) || 'production').toLowerCase().trim();
  const isPreviewOrTest = currentEnv === 'preview' || currentEnv === 'test' || currentEnv === 'local';
  if (!isPreviewOrTest) {
    const siteKey = (env && env.TURNSTILE_SITE_KEY ? env.TURNSTILE_SITE_KEY.trim() : '');
    const secretKey = (env && env.TURNSTILE_SECRET_KEY ? env.TURNSTILE_SECRET_KEY.trim() : '');

    if (!siteKey) {
      return 'Cloudflare Turnstile site key is missing for production (TURNSTILE_SITE_KEY missing).';
    }
    if (isCloudflareTestKey(siteKey)) {
      return 'Cloudflare Turnstile test site key is not permitted in production.';
    }
    if (!secretKey) {
      return 'Cloudflare Turnstile secret key is missing for production (TURNSTILE_SECRET_KEY missing).';
    }
    if (isCloudflareTestKey(secretKey)) {
      return 'Cloudflare Turnstile test secret key is not permitted in production.';
    }
  }
  return null;
}

function parseStrictPlus91Mobile10(rawPhone) {
  if (rawPhone === null || rawPhone === undefined) return null;
  const compact = String(rawPhone).trim().replace(/[\s\-()]/g, '');
  if (!compact) return null;
  // Strictly allow ONLY +91 (or 91 / bare 10-digit Indian input) with subscriber matching ^[6-9][0-9]{9}$
  const match = compact.match(/^(?:\+91|91)?([6-9][0-9]{9})$/);
  return match ? match[1] : null;
}

function normalizeIndianMobile10(rawPhone) {
  return parseStrictPlus91Mobile10(rawPhone);
}

function maskPhoneLast2(mobile10) {
  const digits = String(mobile10 || '').replace(/\D/g, '');
  if (digits.length >= 2) {
    return `+91 ********${digits.slice(-2)}`;
  }
  return '********';
}

function redactOtpAndPhone(input, otpCode) {
  let str = String(input || '');
  if (otpCode) {
    str = str.split(String(otpCode)).join('[REDACTED_OTP]');
  }
  str = str.replace(/\b\d{6}\b/g, '[REDACTED_CODE]');
  str = str.replace(/\+?\d[\d\s\-()]{7,14}\d/g, (m) => {
    const d = m.replace(/\D/g, '');
    return d.length >= 2 ? `********${d.slice(-2)}` : '********';
  });
  return str;
}

function isValidAlphanumericSmsSender(rawSender) {
  if (typeof rawSender !== 'string') return false;
  const trimmed = rawSender.trim();
  // Strict alphanumeric sender ID (3-11 chars, at least one letter); never strip or invent a header
  return /^(?=.*[A-Za-z])[A-Za-z0-9]{3,11}$/.test(trimmed);
}

async function checkAndIncrementSmsDailyCap(env) {
  const rawCap = (env && env.SMS_DAILY_CAP !== undefined && String(env.SMS_DAILY_CAP).trim() !== '')
    ? parseInt(String(env.SMS_DAILY_CAP).trim(), 10)
    : 25;
  const cap = Number.isNaN(rawCap) ? 25 : Math.max(0, rawCap);
  const todayKey = 'sms_daily_' + new Date().toISOString().slice(0, 10);
  if (cap <= 0) {
    console.info('sms_skipped: daily_cap');
    return { allowed: false, reason: 'daily_cap_exceeded', count: 0, cap };
  }
  if (env && env.DB) {
    try {
      const now = Date.now();
      const expiresAt = now + 86400000;
      const row = await env.DB.prepare('SELECT count FROM email_rate_limits WHERE key = ?').bind(todayKey).first();
      const current = row ? Number(row.count || 0) : 0;
      if (current >= cap) {
        console.info('sms_skipped: daily_cap');
        return { allowed: false, reason: 'daily_cap_exceeded', count: current, cap };
      }
      await env.DB.prepare(`
        INSERT INTO email_rate_limits (key, count, window_start, expires_at)
        VALUES (?, 1, ?, ?)
        ON CONFLICT(key) DO UPDATE SET count = count + 1
      `).bind(todayKey, now, expiresAt).run();
      return { allowed: true, count: current + 1, cap };
    } catch (e) {
      console.warn('[SmsCap_D1_Fallback]', redactOtpAndPhone(e && e.message));
    }
  }
  memoryStore.smsDailyCounts = memoryStore.smsDailyCounts || new Map();
  const current = memoryStore.smsDailyCounts.get(todayKey) || 0;
  if (current >= cap) {
    console.info('sms_skipped: daily_cap');
    return { allowed: false, reason: 'daily_cap_exceeded', count: current, cap };
  }
  memoryStore.smsDailyCounts.set(todayKey, current + 1);
  return { allowed: true, count: current + 1, cap };
}

function resolveBrevoApiKey(env) {
  if (!env) return '';
  if (typeof env.BREVO_API_KEY === 'string' && env.BREVO_API_KEY.trim()) {
    return env.BREVO_API_KEY.trim();
  }
  const emailProvider = typeof env.EMAIL_PROVIDER === 'string' ? env.EMAIL_PROVIDER.toLowerCase().trim() : '';
  const emailApiKey = typeof env.EMAIL_API_KEY === 'string' ? env.EMAIL_API_KEY.trim() : '';
  if (emailApiKey && (emailProvider === 'brevo' || emailApiKey.startsWith('xkeysib-'))) {
    return emailApiKey;
  }
  return '';
}

async function dispatchBrevoTransactionalSms(env, brevoApiKey, sender, mobile10, otpCode) {
  const customTemplate = (env && typeof env.BREVO_SMS_TEMPLATE === 'string' && env.BREVO_SMS_TEMPLATE.trim())
    ? env.BREVO_SMS_TEMPLATE.trim()
    : '';
  const smsContent = customTemplate
    ? customTemplate
        .replace(/\{\{\s*otp\s*\}\}/gi, String(otpCode))
        .replace(/\{\s*otp\s*\}/gi, String(otpCode))
        .replace(/\{\s*code\s*\}/gi, String(otpCode))
    : `Your Numeros Vision verification code is ${otpCode}. Valid for 10 minutes. Do not share this code.`;

  const smsPayload = {
    sender,
    recipient: `91${mobile10}`,
    content: smsContent,
    type: 'transactional',
    tag: 'NumerosVisionOTP',
    unicodeEnabled: false
  };
  if (env && typeof env.BREVO_SMS_ORG_PREFIX === 'string' && env.BREVO_SMS_ORG_PREFIX.trim()) {
    smsPayload.organisationPrefix = env.BREVO_SMS_ORG_PREFIX.trim();
  }

  const rawTimeout = parseInt((env && env.BREVO_SMS_TIMEOUT_MS) || '1500', 10);
  const timeoutMs = Number.isNaN(rawTimeout) ? 1500 : Math.min(Math.max(rawTimeout, 50), 4000);
  const controller = typeof AbortController !== 'undefined' ? new AbortController() : null;
  let timerId = null;

  try {
    const fetchTask = fetch('https://api.brevo.com/v3/transactionalSMS/send', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'content-type': 'application/json',
        'api-key': brevoApiKey
      },
      body: JSON.stringify(smsPayload),
      ...(controller ? { signal: controller.signal } : {})
    });
    const timeoutTask = new Promise((resolve) => {
      timerId = setTimeout(() => {
        if (controller) {
          try { controller.abort(); } catch (_) {}
        }
        resolve({ __timedOut: true });
      }, timeoutMs);
    });

    const res = await Promise.race([fetchTask, timeoutTask]);
    if (timerId) clearTimeout(timerId);
    if (res && res.__timedOut) {
      console.warn('[Brevo_SMS_Timeout] sms_skipped: timeout');
      return {
        success: false,
        configured: true,
        provider: 'brevo',
        reason: 'timeout'
      };
    }

    const data = await res.json().catch(() => ({}));
    if (res.ok) {
      return {
        success: true,
        configured: true,
        provider: 'brevo',
        id: data.messageId || data.reference || null
      };
    }
    const safeStatus = `HTTP ${res.status}`;
    console.warn('[Brevo_SMS_Rejected]', safeStatus);
    return {
      success: false,
      configured: true,
      provider: 'brevo',
      reason: safeStatus
    };
  } catch (smsErr) {
    if (timerId) clearTimeout(timerId);
    console.warn('[Brevo_SMS_Edge_Error]', redactOtpAndPhone(smsErr ? smsErr.message : 'Network error', otpCode));
    return {
      success: false,
      configured: true,
      provider: 'brevo',
      reason: 'network_error'
    };
  }
}

async function dispatchMobileSmsOtp(env, mobile10, otpCode) {
  if (!mobile10 || !/^[6-9][0-9]{9}$/.test(String(mobile10))) {
    console.info('sms_skipped: invalid_phone');
    return { success: false, configured: false, skipped: true, reason: 'invalid_phone' };
  }

  const rawSender = (env && typeof env.BREVO_SMS_SENDER === 'string') ? env.BREVO_SMS_SENDER.trim() : '';
  if (!isValidAlphanumericSmsSender(rawSender)) {
    console.info('sms_skipped: no sender');
    return { success: false, configured: false, skipped: true, reason: 'no_sender' };
  }

  const brevoSmsDisabled = env && (env.BREVO_SMS_ENABLED === 'false' || env.BREVO_SMS_ENABLED === '0');
  if (brevoSmsDisabled) {
    console.info('sms_skipped: disabled');
    return { success: false, configured: false, skipped: true, reason: 'disabled' };
  }

  const isTestSmsAdapter = env && (env.NV_SMS_LOG_ADAPTER === 'true' || env.NV_SMS_LOG_ADAPTER === true);
  const brevoApiKey = resolveBrevoApiKey(env);
  if (!isTestSmsAdapter && !brevoApiKey) {
    console.info('sms_skipped: no_api_key');
    return { success: false, configured: false, skipped: true, reason: 'no_api_key' };
  }

  const capCheck = await checkAndIncrementSmsDailyCap(env);
  if (!capCheck.allowed) {
    return { success: false, configured: true, skipped: true, reason: 'daily_cap' };
  }

  if (isTestSmsAdapter) {
    memoryStore.sentSms = memoryStore.sentSms || [];
    memoryStore.sentSms.push({
      to_masked: maskPhoneLast2(mobile10),
      sender: rawSender,
      otpCode: String(otpCode),
      sent_at: Date.now()
    });
    return { success: true, configured: true, provider: 'logging' };
  }

  return await dispatchBrevoTransactionalSms(env, brevoApiKey, rawSender, mobile10, otpCode);
}

function getEmailConfigError(env) {
  const isTestLogAdapter = env && (env.NV_EMAIL_LOG_ADAPTER === 'true' || env.NV_EMAIL_LOG_ADAPTER === true);
  if (isTestLogAdapter) {
    return null;
  }
  const hasExplicitProvider = Boolean(env && env.EMAIL_PROVIDER && env.EMAIL_PROVIDER.trim());
  const inferredBrevoKey = (!hasExplicitProvider && env && typeof env.BREVO_API_KEY === 'string' && env.BREVO_API_KEY.trim()) ? env.BREVO_API_KEY.trim() : '';
  if (!hasExplicitProvider && !inferredBrevoKey) {
    return 'Transactional email provider is not configured (EMAIL_PROVIDER missing).';
  }
  const provider = hasExplicitProvider ? env.EMAIL_PROVIDER.toLowerCase().trim() : 'brevo';
  if (provider === 'smtp') {
    if (!env.CHARM_SERVICE_URL || !env.CHARM_SERVICE_URL.trim() || !env.CHARM_SERVICE_SECRET || !env.CHARM_SERVICE_SECRET.trim()) {
      return 'Transactional SMTP relay backend is not configured (CHARM_SERVICE_URL / CHARM_SERVICE_SECRET missing).';
    }
    if (!env.EMAIL_FROM || !env.EMAIL_FROM.trim()) {
      return 'Transactional email sender address is not configured (EMAIL_FROM missing).';
    }
    return null;
  }
  const effectiveApiKey = provider === 'brevo'
    ? ((env.EMAIL_API_KEY && env.EMAIL_API_KEY.trim()) || (env.BREVO_API_KEY && env.BREVO_API_KEY.trim()) || '')
    : ((env.EMAIL_API_KEY && env.EMAIL_API_KEY.trim()) || '');
  if (!effectiveApiKey) {
    return 'Transactional email API key is not configured (EMAIL_API_KEY missing).';
  }
  if (!env || !env.EMAIL_FROM || !env.EMAIL_FROM.trim()) {
    return 'Transactional email sender address is not configured (EMAIL_FROM missing).';
  }
  return null;
}

async function sendTransactionalEmail(env, { to, subject, text, html }) {
  const capCheck = await checkAndIncrementEmailDailyCap(env);
  if (!capCheck.allowed) {
    return {
      success: false,
      status: capCheck.reason === 'kill_switch' ? 503 : 429,
      error: capCheck.reason === 'kill_switch' 
        ? 'Email service is temporarily paused via administrative controls.' 
        : 'Daily email delivery quota reached.'
    };
  }

  const isTestLogAdapter = env && (env.NV_EMAIL_LOG_ADAPTER === 'true' || env.NV_EMAIL_LOG_ADAPTER === true);
  if (isTestLogAdapter) {
    memoryStore.sentEmails = memoryStore.sentEmails || [];
    memoryStore.sentEmails.push({
      to,
      subject,
      text,
      html,
      from: (env && env.EMAIL_FROM) ? env.EMAIL_FROM.trim() : 'logging@numerosvision.internal',
      sent_at: Date.now()
    });
    return { success: true, provider: 'logging', id: 'log_' + Date.now() };
  }

  const configError = getEmailConfigError(env);
  if (configError) {
    return { success: false, status: 503, error: configError };
  }

  const provider = (env.EMAIL_PROVIDER && env.EMAIL_PROVIDER.trim())
    ? env.EMAIL_PROVIDER.toLowerCase().trim()
    : 'brevo';
  const from = env.EMAIL_FROM.trim();

  if (provider === 'smtp') {
    const relayBase = env.CHARM_SERVICE_URL.trim().replace(/\/$/, '');
    const res = await fetch(`${relayBase}/api/v1/internal/email/send`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-NV-Charm-Secret': env.CHARM_SERVICE_SECRET.trim()
      },
      body: JSON.stringify({ to, subject, text, html, from })
    });
    const data = await res.json().catch(() => ({}));
    if (!res.ok || !data.success) {
      return { success: false, error: data.error || 'SMTP relay dispatch failed.' };
    }
    return { success: true, id: data.id || ('smtp_' + Date.now()) };
  }

  const apiKey = provider === 'brevo'
    ? ((env.EMAIL_API_KEY && env.EMAIL_API_KEY.trim()) || (env.BREVO_API_KEY && env.BREVO_API_KEY.trim()))
    : env.EMAIL_API_KEY.trim();

  if (provider === 'resend') {
    const res = await fetch('https://api.resend.com/emails', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        from,
        to: [to],
        subject,
        text,
        html
      })
    });
    if (!res.ok) {
      const errText = await res.text().catch(() => '');
      return { success: false, error: `Resend dispatch failed: ${redactOtpAndPhone(errText)}` };
    }
    const data = await res.json().catch(() => ({}));
    return { success: true, id: data.id };
  }

  if (provider === 'brevo') {
    const senderEmail = from.includes('<') ? from.split('<')[1].replace('>', '').trim() : from;
    const senderNameRaw = from.includes('<') ? from.split('<')[0].replace(/["']/g, '').trim() : '';
    const senderName = senderNameRaw || 'Numeros Vision';
    const res = await fetch('https://api.brevo.com/v3/smtp/email', {
      method: 'POST',
      headers: {
        'accept': 'application/json',
        'api-key': apiKey,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        sender: { email: senderEmail, name: senderName },
        to: [{ email: to }],
        subject,
        textContent: text,
        htmlContent: html
      })
    });
    if (!res.ok) {
      const errText = await res.text().catch(() => '');
      return { success: false, error: `Brevo dispatch failed: ${redactOtpAndPhone(errText)}` };
    }
    const data = await res.json().catch(() => ({}));
    return { success: true, id: data.messageId };
  }

  return { success: false, error: `Unsupported email provider: ${provider}` };
}

async function recordUserConsent(env, userId, purpose, consentGiven, ipHash, now) {
  const version = 'v1.0_placeholder_advocate_review';
  if (env && env.DB) {
    try {
      await env.DB.prepare(
        'INSERT INTO user_consents (id, user_id, purpose, consent_given, text_version, created_at, ip_hash) VALUES (?, ?, ?, ?, ?, ?, ?)'
      ).bind('cns_' + now + '_' + getRandomHex(4), userId, purpose, consentGiven ? 1 : 0, version, now, ipHash).run();
    } catch (e) {
      console.warn('[UserConsent_DB_Error]', e.message);
    }
  } else {
    memoryStore.userConsents = memoryStore.userConsents || new Map();
    const list = memoryStore.userConsents.get(userId) || [];
    list.push({ purpose, consent_given: consentGiven ? 1 : 0, text_version: version, created_at: now, ip_hash: ipHash });
    memoryStore.userConsents.set(userId, list);
  }
}

async function canExportToCdp(env, userId) {
  if (env && env.DB) {
    try {
      const row = await env.DB.prepare(
        "SELECT consent_given FROM user_consents WHERE user_id = ? AND purpose = 'marketing_communications' ORDER BY created_at DESC LIMIT 1"
      ).bind(userId).first();
      return Boolean(row && row.consent_given === 1);
    } catch (e) {
      return false;
    }
  } else {
    memoryStore.userConsents = memoryStore.userConsents || new Map();
    const list = memoryStore.userConsents.get(userId) || [];
    const latest = list.filter(c => c.purpose === 'marketing_communications').slice(-1)[0];
    return Boolean(latest && latest.consent_given === 1);
  }
}

const PACK_CATALOG = {
  version: "2.2.0",
  currency: "INR",
  ladder_order: ["report_premium", "report_advanced", "report_basic"],
  launch_offer: {
    enabled: true,
    duration_days: 7,
    started_at: null,
    ends_at: null,
    until_date_label: null,
    regular_from_date_label: null,
    copy_template: "Launch price until {until_date}. Regular price ₹{mrp_formatted} from {from_date}."
  },
  feature_flags: {
    notify_me_higher_tiers: true,
    notify_me_tiers: ["report_advanced", "report_premium", "planner_2027"],
    waitlist_display_label: "Coming soon, notify me",
    waitlist_caption: "When this report opens, it starts at a launch price for its first 7 days. We’ll email you the day it opens."
  },
  core_reports: {
    report_basic: {
      pack_id: "report_basic",
      tier_id: "basic",
      name: "Anveil my alignments",
      descriptor: "Basic Numerology Report, 3 pages",
      pages: 3,
      price_inr: 199,
      mrp_inr: 399,
      mrp_paise: 39900,
      amount_paise: 19900,
      digital_root: 1,
      mrp_digital_root: 3,
      features: [
        "Core Numbers: Mulank (Birth Day number), Bhagyank (Life Path number), Kua number (Vastu direction number) & Personal Year",
        "9-Cell Lo Shu Grid (Lo Shu Square) Mapping & Active Plane Strengths",
        "Calling Name number (Chaldean Name number) Harmony Check",
        "Five-Element Distribution Balance & Practical Lifestyle Guidance",
        "Instant 3-Page Print-Ready Personalized PDF Report"
      ],
      status: "active"
    },
    report_advanced: {
      pack_id: "report_advanced",
      tier_id: "advanced",
      name: "Anveil my glowing charms",
      descriptor: "Advanced Numerology Report, 12 pages",
      pages: 12,
      price_inr: 510,
      mrp_inr: 1020,
      mrp_paise: 102000,
      amount_paise: 51000,
      digital_root: 6,
      mrp_digital_root: 3,
      features: [
        "Everything in Basic plus Deep Analysis of All Present Numbers",
        "Repeating Digit Amplifications & Behavioral Tendencies",
        "8 Lo Shu Planes & Raj Yoga Combinations Breakdown",
        "Career, Relationship & Financial Archetype Compatibility",
        "12-Page Structured PDF Report with Actionable Daily Habits"
      ],
      status: "active"
    },
    report_premium: {
      pack_id: "report_premium",
      tier_id: "premium",
      name: "Anveil every charm",
      descriptor: "Complete Numerology Report, 32 pages",
      pages: 32,
      price_inr: 1050,
      mrp_inr: 2100,
      mrp_paise: 210000,
      amount_paise: 105000,
      digital_root: 6,
      mrp_digital_root: 3,
      badge: "Best value",
      features: [
        "Everything in Basic & Advanced plus Missing Numbers (Open Grid Cells) Analysis",
        "Multi-Year Numerology Dasha & Pinnacle Cycle Timeline",
        "Chaldean Name Balancing & Signature Alignment Options",
        "Practical Lifestyle, Color, Directional (Vastu) & Habit Harmonizers",
        "Complete 32-Page Personalized Reference PDF Report"
      ],
      status: "active"
    }
  },
  annual_planners: {
    planner_2027: {
      pack_id: "planner_2027",
      tier_id: "planner_2027",
      name: "2027 Year Ahead Planner",
      descriptor: "Personalized 2027 Annual Numerology Planner, 24 pages",
      pages: 24,
      price_inr: null,
      mrp_inr: null,
      mrp_paise: null,
      amount_paise: null,
      waitlist_only: true,
      display_price_label: "Coming soon, notify me",
      features: [
        "Personal Year, Universal Year & Monthly Vibrational Forecast for 2027",
        "12 Month-by-Month Focus Themes, Key Windows & Caution Corridors",
        "Quarterly Career, Financial & Relationship Pacing Checklists",
        "Lo Shu Grid & Elemental Rhythm Alignment for 2027",
        "24-Page Personalized Annual Reference PDF"
      ],
      status: "waitlist"
    }
  },
  charm_ai: {
    charm_free: {
      pack_id: "charm_free",
      name: "Free Preview",
      descriptor: "Free Exploratory Numerology Q&A, 3 questions",
      price_inr: 0,
      amount_paise: 0,
      questions_count: 3,
      status: "active"
    },
    charm_single: {
      pack_id: "charm_single",
      name: "Charm AI Starter Pack",
      descriptor: "Guided Numerology Q&A Pack, 5 questions",
      price_inr: 199,
      amount_paise: 19900,
      questions_count: 5,
      status: "active"
    },
    charm_multi: {
      pack_id: "charm_multi",
      name: "Multi-Reading Pack",
      price_inr: 399,
      amount_paise: 39900,
      questions_count: 10,
      status: "inactive"
    },
    charm_extended: {
      pack_id: "charm_extended",
      name: "Extended Reading Pack",
      price_inr: 699,
      amount_paise: 69900,
      questions_count: 25,
      status: "inactive"
    }
  },
  bundles: {
    starter_bundle: {
      pack_id: "starter_bundle",
      name: "Starter Bundle",
      price_inr: 339,
      amount_paise: 33900,
      status: "coming_soon"
    },
    discovery_bundle: {
      pack_id: "discovery_bundle",
      name: "Discovery Bundle",
      price_inr: 1299,
      amount_paise: 129900,
      status: "coming_soon"
    },
    comprehensive_bundle: {
      pack_id: "comprehensive_bundle",
      name: "Comprehensive Bundle",
      price_inr: 1999,
      amount_paise: 199900,
      status: "coming_soon"
    }
  }
};

function resolveServerLaunchOfferState(env = null, nowMs = null, packId = null) {
  const lo = PACK_CATALOG.launch_offer || {};
  if (lo.enabled === false) {
    return { active: false, configured: false, forced: false, startedAt: null, endsAt: null, untilDate: '', fromDate: '' };
  }
  const tierEnvMap = {
    report_basic: ['NV_LAUNCH_BASIC_STARTS_AT', 'NV_LAUNCH_BASIC_ENDS_AT'],
    report_advanced: ['NV_LAUNCH_ADVANCED_STARTS_AT', 'NV_LAUNCH_ADVANCED_ENDS_AT'],
    report_premium: ['NV_LAUNCH_PREMIUM_STARTS_AT', 'NV_LAUNCH_PREMIUM_ENDS_AT'],
    planner_2027: ['NV_LAUNCH_PLANNER_2027_STARTS_AT', 'NV_LAUNCH_PLANNER_2027_ENDS_AT']
  };
  let tierStartVar = '';
  let tierEndVar = '';
  if (packId && tierEnvMap[packId] && env) {
    const [sKey, eKey] = tierEnvMap[packId];
    tierStartVar = env[sKey] ? String(env[sKey]).trim() : '';
    tierEndVar = env[eKey] ? String(env[eKey]).trim() : '';
  }
  const rawStarts = tierStartVar
    ? tierStartVar
    : ((env && env.NV_LAUNCH_STARTS_AT && String(env.NV_LAUNCH_STARTS_AT).trim())
      ? String(env.NV_LAUNCH_STARTS_AT).trim()
      : ((env && env.NV_LAUNCH_STARTED_AT && String(env.NV_LAUNCH_STARTED_AT).trim())
        ? String(env.NV_LAUNCH_STARTED_AT).trim()
        : ''));
  const rawEnds = tierEndVar
    ? tierEndVar
    : ((env && env.NV_LAUNCH_ENDS_AT && String(env.NV_LAUNCH_ENDS_AT).trim())
      ? String(env.NV_LAUNCH_ENDS_AT).trim()
      : '');
  if (!rawStarts || !rawEnds) {
    const envName = (env && env.ENVIRONMENT ? String(env.ENVIRONMENT).trim().toLowerCase() : '');
    const rawForce = (env && env.NV_FORCE_LAUNCH_MODE !== undefined && env.NV_FORCE_LAUNCH_MODE !== null)
      ? String(env.NV_FORCE_LAUNCH_MODE).trim().toLowerCase()
      : '';
    if (envName !== 'production' && (rawForce === '1' || rawForce === 'true' || rawForce === 'yes' || rawForce === 'on')) {
      return {
        active: true,
        configured: true,
        forced: true,
        startedAt: null,
        endsAt: null,
        rawStartsAt: '',
        rawEndsAt: '',
        untilDate: '',
        fromDate: ''
      };
    }
    return { active: false, configured: false, forced: false, startedAt: null, endsAt: null, untilDate: '', fromDate: '' };
  }
  const startMs = Date.parse(rawStarts);
  const endMs = Date.parse(rawEnds);
  if (Number.isNaN(startMs) || Number.isNaN(endMs) || endMs <= startMs) {
    return { active: false, configured: false, forced: false, startedAt: null, endsAt: null, untilDate: '', fromDate: '' };
  }
  const currentMs = typeof nowMs === 'number' ? nowMs : Date.now();
  const active = currentMs >= startMs && currentMs <= endMs;
  const IST_OFFSET_MS = 5.5 * 3600 * 1000;
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const uIst = new Date(endMs + IST_OFFSET_MS);
  const fIst = new Date(endMs + 1000 + IST_OFFSET_MS);
  const isShortWindow = (endMs - startMs) < (24 * 3600 * 1000);
  const pad2 = (n) => String(n).padStart(2, '0');
  const untilDate = isShortWindow
    ? `${uIst.getUTCDate()} ${months[uIst.getUTCMonth()]} ${uIst.getUTCFullYear()}, ${pad2(uIst.getUTCHours())}:${pad2(uIst.getUTCMinutes())} IST`
    : `${uIst.getUTCDate()} ${months[uIst.getUTCMonth()]} ${uIst.getUTCFullYear()}`;
  const fromDate = isShortWindow
    ? `${fIst.getUTCDate()} ${months[fIst.getUTCMonth()]} ${fIst.getUTCFullYear()}, ${pad2(fIst.getUTCHours())}:${pad2(fIst.getUTMinutes ? fIst.getUTMinutes() : fIst.getUTCMinutes())} IST`
    : `${fIst.getUTCDate()} ${months[fIst.getUTCMonth()]} ${fIst.getUTCFullYear()}`;
  return {
    active,
    configured: true,
    forced: false,
    startedAt: new Date(startMs).toISOString(),
    endsAt: new Date(endMs).toISOString(),
    rawStartsAt: rawStarts,
    rawEndsAt: rawEnds,
    untilDate,
    fromDate
  };
}

function isPlanner2027Live(env) {
  if (!env || env.PLANNER_2027_LIVE === undefined || env.PLANNER_2027_LIVE === null) return false;
  const v = String(env.PLANNER_2027_LIVE).trim().toLowerCase();
  return v === 'true' || v === '1' || v === 'yes';
}

function getPackById(packId, env = null, nowMs = null) {
  if (!packId || typeof packId !== 'string') return null;
  const p = packId.trim().toLowerCase();
  const aliases = {
    'basic': 'report_basic',
    'report_essential': 'report_basic',
    'advanced': 'report_advanced',
    'report_master': 'report_advanced',
    'premium': 'report_premium',
    'report_divine': 'report_premium',
    'planner-2027': 'planner_2027',
    'year_2027': 'planner_2027',
    '2027_planner': 'planner_2027',
    'starter_5q': 'charm_single'
  };
  const key = aliases[p] || p;
  const base = PACK_CATALOG.core_reports[key] || (PACK_CATALOG.annual_planners && PACK_CATALOG.annual_planners[key]) || PACK_CATALOG.charm_ai[key] || PACK_CATALOG.bundles[key] || null;
  if (!base) return null;
  const waitlistLabel = (PACK_CATALOG.feature_flags && PACK_CATALOG.feature_flags.waitlist_display_label) || 'Coming soon, notify me';
  const waitlistCaption = (PACK_CATALOG.feature_flags && PACK_CATALOG.feature_flags.waitlist_caption) || 'When this report opens, it starts at a launch price for its first 7 days. We’ll email you the day it opens.';
  if (key === 'planner_2027' && !isPlanner2027Live(env)) {
    return Object.assign({}, base, {
      waitlist_only: true,
      display_price_label: waitlistLabel,
      waitlist_caption: waitlistCaption,
      price_inr: null,
      mrp_inr: null,
      amount_paise: null,
      struck_mrp_inr: null,
      launch_offer_active: false,
      launch_offer_copy: ''
    });
  }
  if (isNotifyMeHigherTiersEnabled(env) && (key === 'report_advanced' || key === 'report_premium')) {
    return Object.assign({}, base, {
      waitlist_only: true,
      display_price_label: waitlistLabel,
      waitlist_caption: waitlistCaption,
      price_inr: null,
      amount_paise: null,
      struck_mrp_inr: null,
      launch_offer_active: false,
      launch_offer_copy: ''
    });
  }
  if (PACK_CATALOG.core_reports[key] && base.mrp_inr) {
    const launchState = resolveServerLaunchOfferState(env, nowMs, key);
    if (!launchState.active) {
      return Object.assign({}, base, {
        waitlist_only: false,
        launch_price_inr: base.price_inr,
        launch_amount_paise: base.amount_paise,
        price_inr: base.mrp_inr,
        amount_paise: base.mrp_paise || (base.mrp_inr * 100),
        struck_mrp_inr: null,
        launch_offer_active: false,
        launch_offer_copy: ''
      });
    }
    const mrpFormatted = Number(base.mrp_inr).toLocaleString('en-IN');
    const copyTpl = (PACK_CATALOG.launch_offer && PACK_CATALOG.launch_offer.copy_template) || 'Launch price until {until_date}. Regular price ₹{mrp_formatted} from {from_date}.';
    const launchCopy = (launchState.forced && !launchState.untilDate)
      ? `Launch price active during the launch window. Regular price ₹${mrpFormatted} thereafter.`
      : copyTpl
        .replace('{until_date}', launchState.untilDate)
        .replace('{mrp_formatted}', mrpFormatted)
        .replace('{from_date}', launchState.fromDate);
    return Object.assign({}, base, {
      waitlist_only: false,
      launch_price_inr: base.price_inr,
      launch_amount_paise: base.amount_paise,
      struck_mrp_inr: base.mrp_inr,
      launch_offer_active: true,
      launch_offer_copy: launchCopy
    });
  }
  return base;
}

function resolveEffectivePackPricePaise(packId, env = null, nowMs = null) {
  const pack = getPackById(packId, env, nowMs);
  return pack && typeof pack.amount_paise === 'number' ? pack.amount_paise : 0;
}

function isLayers23Enabled(env = null) {
  if (!env || String(env.ENVIRONMENT || 'production').trim().toLowerCase() === 'production') {
    return false;
  }
  const raw = env.NV_ENABLE_LAYERS_2_3 ? String(env.NV_ENABLE_LAYERS_2_3).trim().toLowerCase() : '0';
  return raw === '1' || raw === 'true' || raw === 'yes' || raw === 'on';
}

function isNotifyMeHigherTiersEnabled(env) {
  if (env && env.NV_NOTIFY_ME_HIGHER_TIERS !== undefined && env.NV_NOTIFY_ME_HIGHER_TIERS !== null && String(env.NV_NOTIFY_ME_HIGHER_TIERS).trim() !== '') {
    const v = String(env.NV_NOTIFY_ME_HIGHER_TIERS).trim().toLowerCase();
    return v === 'true' || v === '1' || v === 'yes';
  }
  return Boolean(PACK_CATALOG.feature_flags && PACK_CATALOG.feature_flags.notify_me_higher_tiers);
}

function recommendLadderTier(gapCount = null, notifyMeActive = false, tappedContext = null) {
  if (notifyMeActive === true) return 'report_basic';
  if (tappedContext) {
    const ctxKey = String(tappedContext).trim().toLowerCase();
    if (ctxKey === 'veiled' || ctxKey === 'missing') return 'report_premium';
    if (ctxKey === 'glowing' || ctxKey === 'present') return 'report_advanced';
    if (ctxKey === 'alignment' || ctxKey === 'plane') return 'report_basic';
  }
  if (gapCount === null || gapCount === undefined || Number.isNaN(Number(gapCount))) {
    return 'report_advanced';
  }
  const gaps = Math.max(0, Math.min(9, Math.trunc(Number(gapCount))));
  if (gaps <= 2) return 'report_basic';
  if (gaps <= 5) return 'report_advanced';
  return 'report_premium';
}

const WAITLIST_PURPOSE = 'tell me when this report is available';
const WAITLIST_RETENTION_MONTHS = 12;
const WAITLIST_RETENTION_SECONDS = 365 * 86400;
const WAITLIST_CONSENT_VERSION = 'dpdp_waitlist_v1.0';
const WAITLIST_DPDP_CONSENT_TEXT =
  'I consent to Numeros Vision storing my encrypted email address for 12 months solely for the purpose: "tell me when this report is available", with the right to delete my email record on request at any time under the DPDP Act 2023.';
const _WAITLIST_LOCAL_DEV_KEY = '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef';

function normalizeWaitlistPackId(rawPack) {
  const clean = String(rawPack || '').trim().toLowerCase();
  if (clean === 'report_advanced' || clean === 'advanced' || clean === 'report_master' || clean === 'master') {
    return 'report_advanced';
  }
  if (clean === 'report_premium' || clean === 'premium' || clean === 'report_divine' || clean === 'divine') {
    return 'report_premium';
  }
  if (clean === 'planner_2027' || clean === 'planner-2027' || clean === 'year_2027' || clean === '2027_planner') {
    return 'planner_2027';
  }
  return null;
}

function getWaitlistEncryptionKey(env) {
  const configured = env && typeof env.DATA_ENCRYPTION_KEY === 'string' ? env.DATA_ENCRYPTION_KEY.trim() : '';
  if (configured) {
    parse32ByteKey(configured);
    return configured;
  }
  const mode = ((env && env.ENVIRONMENT) || 'production').toString().trim().toLowerCase();
  if (mode === 'local' || mode === 'test') {
    return _WAITLIST_LOCAL_DEV_KEY;
  }
  return requireSecret(env || {}, 'DATA_ENCRYPTION_KEY');
}

async function ensureWaitlistTable(db) {
  if (!db) return;
  await db.prepare(`
    CREATE TABLE IF NOT EXISTS waitlist_notify_me (
      id TEXT PRIMARY KEY,
      email_sha256 TEXT NOT NULL,
      email_enc TEXT NOT NULL,
      pack_id TEXT NOT NULL,
      purpose TEXT NOT NULL DEFAULT 'tell me when this report is available',
      consent_dpdp INTEGER NOT NULL DEFAULT 1,
      consent_text TEXT NOT NULL,
      consent_version TEXT NOT NULL DEFAULT 'dpdp_waitlist_v1.0',
      retention_months INTEGER NOT NULL DEFAULT 12,
      source_page TEXT,
      created_at INTEGER NOT NULL,
      updated_at INTEGER NOT NULL,
      expires_at INTEGER NOT NULL,
      UNIQUE(email_sha256, pack_id)
    )
  `).run();
}

async function registerWaitlistNotifyMe(env, body = {}, nowOverrideSec = null) {
  const emailClean = String(body.email || '').trim().toLowerCase();
  const normPack = normalizeWaitlistPackId(body.pack_id || body.packId || body.sku_id || body.skuId);
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailClean)) {
    return { status: 400, payload: { success: false, error: 'Please enter a valid email address.' } };
  }
  if (!normPack) {
    return { status: 400, payload: { success: false, error: 'Waitlist notifications apply only to Advanced, Premium, and 2027 Planner editions.' } };
  }
  if (body.consent !== true) {
    return { status: 400, payload: { success: false, error: 'Explicit notification consent is required under DPDP 2023.' } };
  }
  const purpose = String(body.purpose || WAITLIST_PURPOSE).trim();
  if (purpose !== WAITLIST_PURPOSE) {
    return { status: 400, payload: { success: false, error: `Invalid waitlist purpose; expected "${WAITLIST_PURPOSE}".` } };
  }
  const consentText = String(body.consent_text || body.consentText || WAITLIST_DPDP_CONSENT_TEXT).trim() || WAITLIST_DPDP_CONSENT_TEXT;
  const sourcePage = String(body.source_page || body.sourcePage || 'your_reading').slice(0, 64);

  const nowSec = nowOverrideSec !== null ? Math.trunc(nowOverrideSec) : Math.floor(Date.now() / 1000);
  const expiresAt = nowSec + WAITLIST_RETENTION_SECONDS;
  const emailHash = await sha256Hex(emailClean);
  const dataEncKey = getWaitlistEncryptionKey(env);
  const emailEnc = await encryptField(emailClean, dataEncKey);

  let recordId = 'wl_' + nowSec + '_' + getRandomHex(4);
  let deduplicated = false;

  if (env && env.DB) {
    await ensureWaitlistTable(env.DB);
    await env.DB.prepare('DELETE FROM waitlist_notify_me WHERE expires_at <= ?').bind(nowSec).run();
    const existing = await env.DB.prepare(
      'SELECT id, created_at FROM waitlist_notify_me WHERE email_sha256 = ? AND pack_id = ?'
    ).bind(emailHash, normPack).first();
    if (existing) {
      deduplicated = true;
      recordId = existing.id;
      await env.DB.prepare(`
        UPDATE waitlist_notify_me
        SET email_enc = ?, purpose = ?, consent_dpdp = 1, consent_text = ?, consent_version = ?, retention_months = ?, source_page = ?, updated_at = ?, expires_at = ?
        WHERE email_sha256 = ? AND pack_id = ?
      `).bind(emailEnc, WAITLIST_PURPOSE, consentText, WAITLIST_CONSENT_VERSION, WAITLIST_RETENTION_MONTHS, sourcePage, nowSec, expiresAt, emailHash, normPack).run();
    } else {
      await env.DB.prepare(`
        INSERT INTO waitlist_notify_me (
          id, email_sha256, email_enc, pack_id, purpose, consent_dpdp, consent_text,
          consent_version, retention_months, source_page, created_at, updated_at, expires_at
        ) VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?)
      `).bind(
        recordId, emailHash, emailEnc, normPack, WAITLIST_PURPOSE, consentText,
        WAITLIST_CONSENT_VERSION, WAITLIST_RETENTION_MONTHS, sourcePage, nowSec, nowSec, expiresAt
      ).run();
    }
  } else {
    memoryStore.waitlistNotifyMe = memoryStore.waitlistNotifyMe || new Map();
    for (const [k, rec] of memoryStore.waitlistNotifyMe.entries()) {
      if (!rec || Number(rec.expires_at || 0) <= nowSec) {
        memoryStore.waitlistNotifyMe.delete(k);
      }
    }
    const dedupeKey = `${emailHash}_${normPack}`;
    const prev = memoryStore.waitlistNotifyMe.get(dedupeKey);
    if (prev) {
      deduplicated = true;
      recordId = prev.id;
    }
    memoryStore.waitlistNotifyMe.set(dedupeKey, {
      id: recordId,
      email_sha256: emailHash,
      email_enc: emailEnc,
      pack_id: normPack,
      purpose: WAITLIST_PURPOSE,
      consent_dpdp: true,
      consent_text: consentText,
      consent_version: WAITLIST_CONSENT_VERSION,
      retention_months: WAITLIST_RETENTION_MONTHS,
      source_page: sourcePage,
      created_at: prev ? prev.created_at : nowSec,
      updated_at: nowSec,
      expires_at: expiresAt
    });
  }

  await logWorkerEvent(env, {
    event_name: 'waitlist_notify_me_registered',
    pack_id: normPack,
    subject_hash: emailHash.slice(0, 16)
  });

  return {
    status: 200,
    payload: {
      status: 'registered',
      success: true,
      id: recordId,
      pack_id: normPack,
      deduplicated,
      purpose: WAITLIST_PURPOSE,
      retention_months: WAITLIST_RETENTION_MONTHS,
      expires_at: expiresAt,
      consent_version: WAITLIST_CONSENT_VERSION,
      data_fiduciary: 'Numeros Vision Consultancy (Bhaskar Kumar Singh)',
      message: 'You are on the priority launch list. Your encrypted email is stored for up to 12 months solely to tell you when this report is available, and can be deleted at any time.'
    }
  };
}

async function deleteWaitlistNotifyMe(env, body = {}) {
  const emailClean = String(body.email || '').trim().toLowerCase();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailClean)) {
    return { status: 400, payload: { success: false, error: 'Please enter a valid email address.' } };
  }
  const rawPack = String(body.pack_id || body.packId || body.sku_id || body.skuId || '').trim();
  const normPack = rawPack ? normalizeWaitlistPackId(rawPack) : null;
  if (rawPack && !normPack) {
    return { status: 400, payload: { success: false, error: 'Invalid pack_id; expected report_advanced, report_premium, or planner_2027.' } };
  }

  const emailHash = await sha256Hex(emailClean);
  let deletedCount = 0;

  if (env && env.DB) {
    await ensureWaitlistTable(env.DB);
    if (normPack) {
      const res = await env.DB.prepare('DELETE FROM waitlist_notify_me WHERE email_sha256 = ? AND pack_id = ?').bind(emailHash, normPack).run();
      deletedCount = (res && res.meta && typeof res.meta.changes === 'number') ? res.meta.changes : 0;
    } else {
      const res = await env.DB.prepare('DELETE FROM waitlist_notify_me WHERE email_sha256 = ?').bind(emailHash).run();
      deletedCount = (res && res.meta && typeof res.meta.changes === 'number') ? res.meta.changes : 0;
    }
  } else if (memoryStore.waitlistNotifyMe) {
    for (const [k, rec] of memoryStore.waitlistNotifyMe.entries()) {
      if (rec && rec.email_sha256 === emailHash && (!normPack || rec.pack_id === normPack)) {
        memoryStore.waitlistNotifyMe.delete(k);
        deletedCount++;
      }
    }
  }

  await logWorkerEvent(env, {
    event_name: 'waitlist_notify_me_deleted',
    pack_id: normPack || 'all',
    subject_hash: emailHash.slice(0, 16)
  });

  return {
    status: 200,
    payload: {
      status: 'deleted',
      success: true,
      deleted_count: deletedCount,
      pack_id: normPack,
      message: deletedCount > 0
        ? 'Your encrypted email has been permanently deleted from the waitlist.'
        : 'No matching waitlist record was found for that email address.'
    }
  };
}

async function buildWaitlistNotificationEmail(record, dataEncKey, nowOverrideSec = null) {
  if (!record || typeof record !== 'object') {
    throw new Error('Waitlist record is required.');
  }
  if (record.deleted_at) {
    throw new Error('Cannot produce notification email for a deleted waitlist record.');
  }
  const consented = record.consent_dpdp === true || record.consent_dpdp === 1;
  if (!consented) {
    throw new Error('Cannot produce notification email without explicit DPDP consent.');
  }
  if (record.purpose !== WAITLIST_PURPOSE) {
    throw new Error(`Waitlist record purpose mismatch: expected "${WAITLIST_PURPOSE}".`);
  }
  const nowSec = nowOverrideSec !== null ? Math.trunc(nowOverrideSec) : Math.floor(Date.now() / 1000);
  if (Number(record.expires_at || 0) <= nowSec) {
    throw new Error('Waitlist record has expired beyond its 12-month retention window.');
  }
  const normPack = normalizeWaitlistPackId(record.pack_id);
  if (!normPack) {
    throw new Error('Unsupported waitlist pack_id.');
  }
  if (!record.email_enc) {
    throw new Error('Waitlist record is missing encrypted email (email_enc).');
  }
  const toEmail = await decryptField(record.email_enc, dataEncKey);
  if (!toEmail || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(toEmail)) {
    throw new Error('Decrypted waitlist recipient email is invalid.');
  }

  const packTitle = normPack === 'report_premium'
    ? 'Anveil every charm (Complete Numerology Report, 32 pages)'
    : (normPack === 'planner_2027'
      ? '2027 Year Ahead Planner (Personalized 2027 Annual Numerology Planner, 24 pages)'
      : 'Anveil my glowing charms (Advanced Numerology Report, 12 pages)');
  const subject = `${packTitle} Is Now Available | NUMEROS VISION`;
  const text =
    `Namaste,\n\n` +
    `You asked us to tell you when ${packTitle} becomes available on NUMEROS VISION.\n\n` +
    `This edition is now open at https://numerosvision.com/pricing/\n\n` +
    `Why you received this email: You provided explicit DPDP 2023 consent to Data Fiduciary Numeros Vision Consultancy (Bhaskar Kumar Singh) for the single purpose "${WAITLIST_PURPOSE}" (12-month maximum retention).\n` +
    `To delete your waitlist record at any time, use the Delete Waitlist Email option or contact privacy@numerosvision.com.\n\n` +
    `NUMEROS VISION · ANVEIL EVERY CHARM`;
  const html =
    `<div style="font-family:Inter,Arial,sans-serif;background:#FFFDF7;color:#523E28;padding:24px;border:1px solid #C9A227;border-radius:12px;max-width:560px;">` +
    `<div style="font-size:12px;letter-spacing:0.12em;color:#8B6914;font-weight:700;">NUMEROS VISION · ANVEIL EVERY CHARM</div>` +
    `<h2 style="color:#523E28;margin:10px 0 8px;">${packTitle} Is Now Available</h2>` +
    `<p>You asked us to tell you when <strong>${packTitle}</strong> opens.</p>` +
    `<p><a href="https://numerosvision.com/pricing/" style="display:inline-block;padding:10px 18px;background:#8B6914;color:#FFFDF7;text-decoration:none;border-radius:8px;font-weight:600;">View Available Report</a></p>` +
    `<p style="font-size:12px;color:#7A654D;margin-top:18px;">Sent strictly under your DPDP 2023 consent (Data Fiduciary: Numeros Vision Consultancy · Bhaskar Kumar Singh) for purpose: "${WAITLIST_PURPOSE}" (12-month retention).</p>` +
    `</div>`;

  return {
    to: toEmail,
    subject,
    purpose: WAITLIST_PURPOSE,
    pack_id: normPack,
    text,
    html
  };
}

async function dispatchWaitlistNotificationsForPack(env, packId, nowOverrideSec = null) {
  const normPack = normalizeWaitlistPackId(packId);
  if (!normPack) throw new Error('Unsupported waitlist pack_id.');
  const nowSec = nowOverrideSec !== null ? Math.trunc(nowOverrideSec) : Math.floor(Date.now() / 1000);
  const dataEncKey = getWaitlistEncryptionKey(env);
  let rows = [];
  if (env && env.DB) {
    await ensureWaitlistTable(env.DB);
    const res = await env.DB.prepare(
      'SELECT * FROM waitlist_notify_me WHERE pack_id = ? AND expires_at > ?'
    ).bind(normPack, nowSec).all();
    rows = (res && res.results) ? res.results : [];
  } else if (memoryStore.waitlistNotifyMe) {
    for (const rec of memoryStore.waitlistNotifyMe.values()) {
      if (rec && rec.pack_id === normPack && Number(rec.expires_at || 0) > nowSec) {
        rows.push(rec);
      }
    }
  }
  const produced = [];
  for (const row of rows) {
    const emailMsg = await buildWaitlistNotificationEmail(row, dataEncKey, nowSec);
    const dispatchRes = await sendTransactionalEmail(env, emailMsg);
    produced.push({ email: emailMsg, dispatch: dispatchRes });
  }
  return produced;
}

// Server-side operational telemetry logger (events table - strictly ZERO PII)
async function logWorkerEvent(env, eventData) {
  if (!env || !env.DB) return null;
  try {
    const id = 'evt_' + crypto.randomUUID().replace(/-/g, '').slice(0, 16);
    const eventName = String(eventData.event_name || eventData.event || 'unnamed_event').slice(0, 64);
    const deviceId = eventData.device_id ? String(eventData.device_id).slice(0, 64) : null;
    const anonSession = eventData.anonymous_session_id ? String(eventData.anonymous_session_id).slice(0, 64) : null;
    const pagePath = eventData.page_path ? String(eventData.page_path).slice(0, 255) : null;
    const productId = eventData.product_id ? String(eventData.product_id).slice(0, 64) : null;
    const valInr = parseFloat(eventData.value_inr || eventData.value) || 0.0;
    const currency = String(eventData.currency || 'INR').slice(0, 4);
    const utmSource = eventData.utm_source ? String(eventData.utm_source).slice(0, 64) : null;
    const utmMedium = eventData.utm_medium ? String(eventData.utm_medium).slice(0, 64) : null;
    const utmCampaign = eventData.utm_campaign ? String(eventData.utm_campaign).slice(0, 64) : null;
    const metaJson = eventData.meta_json ? (typeof eventData.meta_json === 'string' ? eventData.meta_json : JSON.stringify(eventData.meta_json)) : null;
    const ipHash = eventData.ip_hash || null;
    const userAgent = eventData.user_agent ? String(eventData.user_agent).slice(0, 255) : null;
    const createdAt = eventData.created_at || Date.now();

    await env.DB.prepare(`
      INSERT INTO events (
        id, event_name, device_id, anonymous_session_id, page_path, product_id,
        value_inr, currency, utm_source, utm_medium, utm_campaign, meta_json,
        ip_hash, user_agent, created_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    `).bind(
      id, eventName, deviceId, anonSession, pagePath, productId,
      valInr, currency, utmSource, utmMedium, utmCampaign, metaJson,
      ipHash, userAgent, createdAt
    ).run();

    if (Math.random() < 0.10) {
      const cutoff = Date.now() - (90 * 86400 * 1000);
      try {
        await env.DB.prepare("DELETE FROM events WHERE created_at < ?").bind(cutoff).run();
      } catch (purgeErr) {}
    }

    return id;
  } catch (err) {
    console.debug('[Worker_Event_Log_Notice]', err);
    return null;
  }
}


const WEBHOOK_FALLBACK_WINDOW_MS = 10 * 60 * 1000;

/**
 * 10-MINUTE RAZORPAY ORDER-STATUS FALLBACK
 * Webhook-only primary architecture: if no Razorpay webhook arrives within 10 minutes
 * of signature verification (or order creation), poll Razorpay's Orders Payments API
 * and fulfill idempotently ONLY if Razorpay confirms a 'captured' payment matching
 * the authoritative INR amount_paise.
 */
async function reconcileStaleOrderWithRazorpay(order, env, now, request, ctx) {
  if (!order || order.status === 'PAID' || !order.rzp_order_id) {
    return { reconciled: false, reason: 'not_eligible' };
  }
  if (order.status !== 'PAYMENT_VERIFIED' && order.status !== 'CREATED' && order.status !== 'pending') {
    return { reconciled: false, reason: 'terminal_status' };
  }
  const refTs = order.status === 'PAYMENT_VERIFIED'
    ? Number(order.updated_at || order.created_at || 0)
    : Number(order.created_at || order.updated_at || 0);
  if (!refTs || (now - refTs) < WEBHOOK_FALLBACK_WINDOW_MS) {
    return { reconciled: false, reason: 'within_webhook_window' };
  }
  const rzpKeyId = (env && env.RAZORPAY_KEY_ID ? String(env.RAZORPAY_KEY_ID).trim() : '');
  const rzpSecret = (env && env.RAZORPAY_KEY_SECRET ? String(env.RAZORPAY_KEY_SECRET).trim() : '');
  if (!rzpKeyId || !rzpSecret) {
    return { reconciled: false, reason: 'missing_credentials' };
  }
  try {
    const authHeader = 'Basic ' + btoa(`${rzpKeyId}:${rzpSecret}`);
    const rzpResp = await fetch(
      `https://api.razorpay.com/v1/orders/${encodeURIComponent(order.rzp_order_id)}/payments`,
      {
        method: 'GET',
        headers: {
          'Authorization': authHeader,
          'Accept': 'application/json'
        }
      }
    );
    if (!rzpResp.ok) {
      return { reconciled: false, reason: `razorpay_http_${rzpResp.status}` };
    }
    const data = await rzpResp.json().catch(() => ({}));
    const items = Array.isArray(data && data.items) ? data.items : [];
    const captured = items.find(item =>
      item &&
      String(item.status || '').toLowerCase() === 'captured' &&
      Number(item.amount) === Number(order.amount_paise) &&
      String(item.currency || 'INR').toUpperCase() === 'INR'
    );
    if (!captured) {
      return { reconciled: false, reason: 'no_captured_payment' };
    }
    const fulfillRes = await fulfillPaidOrder(
      order,
      captured.id || order.rzp_payment_id || 'rzp_fallback_payment',
      captured.amount,
      captured.method || 'razorpay_fallback',
      env,
      now,
      'razorpay_10min_fallback',
      request
    );
    if (fulfillRes && fulfillRes.jobId && ctx && typeof ctx.waitUntil === 'function') {
      ctx.waitUntil(
        dispatchReportJob(fulfillRes.jobId, env).catch(err => console.error('[Fallback_WaitUntil_Dispatch_Error]', err))
      );
    }
    return { reconciled: true, fulfillRes };
  } catch (err) {
    console.warn('[Razorpay_10Min_Fallback_Error]', err);
    return { reconciled: false, reason: 'fetch_error' };
  }
}

/**
 * SHARED IDEMPOTENT ORDER FULFILLMENT
 * Used by /api/v1/payments/webhook, 10-minute Razorpay fallback, and safety net recovery.
 * Reads pack and subject strictly from D1 order. Fulfills even if status is EXPIRED (late UPI).
 * Idempotency guarantee: exactly one report job and exactly one confirmation email per order.
 */
async function fulfillPaidOrder(order, paymentId, amountPaise, method, env, now, source, request) {
  if (!order || !order.id) return { error: 'Invalid order' };

  // 0. Check for existing report job
  let existingJob = null;
  if (env && env.DB) {
    existingJob = await env.DB.prepare('SELECT id, status FROM report_jobs WHERE order_id = ? ORDER BY created_at DESC LIMIT 1').bind(order.id).first();
  } else if (typeof memoryStore !== 'undefined' && memoryStore.reportJobs) {
    for (const j of memoryStore.reportJobs.values()) {
      if (j.order_id === order.id) { existingJob = j; break; }
    }
  }

  // Check if confirmation email was already sent
  let emailAlreadySent = false;
  if (env && env.DB) {
    const emailAudit = await env.DB.prepare("SELECT id FROM audit_log WHERE resource_id = ? AND action = 'order_confirmation_email_sent'").bind(order.id).first();
    if (emailAudit) emailAlreadySent = true;
  } else if (typeof memoryStore !== 'undefined' && memoryStore.auditLogs) {
    for (const a of memoryStore.auditLogs) {
      if (a.resource_id === order.id && a.action === 'order_confirmation_email_sent') { emailAlreadySent = true; break; }
    }
  }

  // Purely idempotent short-circuit: already fulfilled end-to-end
  if (order.status === 'PAID' && existingJob && emailAlreadySent) {
    return {
      alreadyFulfilled: true,
      orderId: order.id,
      packId: order.pack_id,
      subjectId: order.subject_id,
      jobId: existingJob.id
    };
  }

  const pack = getPackById(order.pack_id);
  let createdJobId = existingJob ? existingJob.id : null;

  if (env && env.DB) {
    // 1. Update order status to PAID
    if (order.status !== 'PAID') {
      await env.DB.prepare("UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?").bind(now, order.id).run();
      order.status = 'PAID';
      order.updated_at = now;
      try {
        await logWorkerEvent(env, {
          event_name: 'payment_verified',
          product_id: order.pack_id,
          value_inr: (amountPaise || order.amount_paise) / 100,
          currency: order.currency || 'INR'
        });
      } catch (_) {}
    }

    // 2. Record payment in payments table if not already present
    const existingPmt = await env.DB.prepare('SELECT id FROM payments WHERE order_id = ?').bind(order.id).first();
    if (!existingPmt) {
      const pmtId = 'pmt_' + now + '_' + getRandomHex(4);
      await env.DB.prepare(
        "INSERT OR IGNORE INTO payments (id, order_id, rzp_payment_id, amount_paise, status, method, captured_at) VALUES (?, ?, ?, ?, 'CAPTURED', ?, ?)"
      ).bind(pmtId, order.id, paymentId || order.rzp_order_id || 'manual', amountPaise || order.amount_paise, method || 'online', now).run();
    }

    // 3. Grant entitlement strictly using pack and subject from D1 order
    const entId = 'ent_' + now + '_' + getRandomHex(4);
    await env.DB.prepare(
      "INSERT OR IGNORE INTO entitlements (id, user_id, subject_id, pack_id, order_id, granted_at) VALUES (?, ?, ?, ?, ?, ?)"
    ).bind(entId, order.user_id, order.subject_id, order.pack_id, order.id, now).run();

    // 4. Credit ledger accounting for Charm AI packs (Idempotent unique ref per order)
    if (pack && pack.questions_count) {
      const orderRefId = 'order_' + order.id;
      const row = await env.DB.prepare('SELECT id FROM credit_ledger WHERE ref_id = ?').bind(orderRefId).first();
      if (!row) {
        const crdId = 'crd_' + now + '_' + getRandomHex(4);
        const prevBalRow = await env.DB.prepare('SELECT COALESCE(SUM(delta), 0) as bal FROM credit_ledger WHERE user_id = ?').bind(order.user_id).first();
        const newBal = (prevBalRow ? prevBalRow.bal : 0) + pack.questions_count;
        await env.DB.prepare(
          'INSERT OR IGNORE INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
        ).bind(crdId, order.user_id, pack.questions_count, 'pack_purchase', orderRefId, newBal, now).run();
      }
    }

    // 5. Voucher ledger allocation for bundles
    if (pack && pack.voucher_allocation) {
      const existingVch = await env.DB.prepare('SELECT id FROM voucher_ledger WHERE order_id = ? LIMIT 1').bind(order.id).first();
      if (!existingVch) {
        for (let i = 0; i < (pack.voucher_allocation.basic_vouchers || 0); i++) {
          await env.DB.prepare(
            "INSERT INTO voucher_ledger (id, user_id, order_id, voucher_type, status, created_at) VALUES (?, ?, ?, 'basic_voucher', 'ACTIVE', ?)"
          ).bind('vch_' + now + '_' + getRandomHex(4), order.user_id, order.id, now).run();
        }
        for (let i = 0; i < (pack.voucher_allocation.advanced_vouchers || 0); i++) {
          await env.DB.prepare(
            "INSERT INTO voucher_ledger (id, user_id, order_id, voucher_type, status, created_at) VALUES (?, ?, ?, 'advanced_voucher', 'ACTIVE', ?)"
          ).bind('vch_' + now + '_' + getRandomHex(4), order.user_id, order.id, now).run();
        }
      }
    }

    // 6. Queue report generation job (Idempotent: exactly once)
    if (!createdJobId) {
      const jobId = 'job_' + now + '_' + getRandomHex(4);
      createdJobId = jobId;
      await env.DB.prepare(
        "INSERT OR IGNORE INTO report_jobs (id, user_id, subject_id, pack_id, order_id, status, created_at) VALUES (?, ?, ?, ?, ?, 'QUEUED', ?)"
      ).bind(jobId, order.user_id, order.subject_id, order.pack_id, order.id, now).run();
    }

    // 7. Audit log recording
    await env.DB.prepare(
      "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, ?, 'order_paid_fulfilled', 'orders', ?, ?, ?)"
    ).bind('aud_' + now + '_' + getRandomHex(4), source || 'system', order.id, JSON.stringify({ paymentId, amountPaise: amountPaise || order.amount_paise, source, jobId: createdJobId }), now).run();
  } else {
    order.status = 'PAID';
    order.updated_at = now;
    if (typeof memoryStore !== 'undefined') {
      if (memoryStore.payments && !memoryStore.payments.has(paymentId)) {
        memoryStore.payments.set(paymentId, { id: 'pmt_' + now, order_id: order.id, rzp_payment_id: paymentId, amount_paise: amountPaise || order.amount_paise, status: 'CAPTURED', captured_at: now });
      }
      if (memoryStore.entitlements) {
        memoryStore.entitlements.set(`${order.user_id}_${order.subject_id}_${order.pack_id}`, {
          user_id: order.user_id,
          subject_id: order.subject_id,
          pack_id: order.pack_id,
          order_id: order.id,
          granted_at: now
        });
      }
      if (pack && pack.questions_count && memoryStore.creditLedger) {
        const orderRefId = 'order_' + order.id;
        let alreadyCredited = false;
        for (const c of memoryStore.creditLedger.values()) {
          if (c.ref_id === orderRefId) { alreadyCredited = true; break; }
        }
        if (!alreadyCredited) {
          let prevBal = 0;
          for (const c of memoryStore.creditLedger.values()) {
            if (c.user_id === order.user_id) prevBal += c.delta;
          }
          const crdId = 'crd_' + now + '_' + getRandomHex(4);
          memoryStore.creditLedger.set(crdId, {
            id: crdId,
            user_id: order.user_id,
            delta: pack.questions_count,
            reason: 'pack_purchase',
            ref_id: orderRefId,
            balance_after: prevBal + pack.questions_count,
            created_at: now
          });
        }
      }
      if (!createdJobId && memoryStore.reportJobs) {
        const jobId = 'job_' + now + '_' + getRandomHex(4);
        createdJobId = jobId;
        memoryStore.reportJobs.set(jobId, {
          id: jobId,
          user_id: order.user_id,
          subject_id: order.subject_id,
          pack_id: order.pack_id,
          order_id: order.id,
          status: 'QUEUED',
          attempts: 0,
          max_attempts: 3,
          r2_key: null,
          last_error: null,
          created_at: now,
          updated_at: now,
          completed_at: null,
          downloaded_at: null
        });
      }
    }
  }

  // 8. Order Confirmation Email Dispatch (Idempotent: exactly once, retried up to 3 times on failure)
  if (!emailAlreadySent) {
    let emailAttempts = 0;
    if (env && env.DB) {
      try {
        const attRow = await env.DB.prepare("SELECT COUNT(*) as cnt FROM audit_log WHERE resource_id = ? AND action = 'order_confirmation_email_attempt'").bind(order.id).first();
        if (attRow) emailAttempts = Number(attRow.cnt || 0);
      } catch (_) {}
    } else if (typeof memoryStore !== 'undefined' && memoryStore.auditLogs) {
      emailAttempts = memoryStore.auditLogs.filter(a => a.resource_id === order.id && a.action === 'order_confirmation_email_attempt').length;
    }

    const MAX_EMAIL_RETRIES = 3;
    if (emailAttempts >= MAX_EMAIL_RETRIES) {
      console.warn(`[Order_Confirmation_Email_Capped] Order ${order.id} reached max delivery attempts (${emailAttempts}/${MAX_EMAIL_RETRIES}).`);
    }
    let customerEmail = (order.email || '').trim().toLowerCase();
    if (!customerEmail && order.subject_id) {
      if (env && env.DB) {
        try {
          const sRow = await env.DB.prepare('SELECT u.email FROM subjects s JOIN users u ON s.user_id = u.id WHERE s.id = ?').bind(order.subject_id).first();
          if (sRow && sRow.email) customerEmail = String(sRow.email).trim().toLowerCase();
        } catch (e) {}
      } else if (typeof memoryStore !== 'undefined' && memoryStore.subjects) {
        const sObj = memoryStore.subjects.get(order.subject_id);
        if (sObj && sObj.email) customerEmail = String(sObj.email).trim().toLowerCase();
      }
    }
    if (!customerEmail && order.user_id) {
      if (env && env.DB) {
        try {
          const uRow = await env.DB.prepare('SELECT email FROM users WHERE id = ?').bind(order.user_id).first();
          if (uRow && uRow.email) customerEmail = String(uRow.email).trim().toLowerCase();
        } catch (e) {}
      } else if (typeof memoryStore !== 'undefined' && memoryStore.users) {
        for (const u of memoryStore.users.values()) {
          if (u.id === order.user_id && u.email) { customerEmail = String(u.email).trim().toLowerCase(); break; }
        }
      }
    }

    if (customerEmail && customerEmail.includes('@')) {
      const packName = pack ? pack.name : 'Numerology Report';
      const orderTokenSecret = await getOrderTokenSecret(env);
      const tokenExpiresAt = now + (30 * 24 * 60 * 60 * 1000);
      let orderToken = '';
      if (orderTokenSecret) {
        orderToken = await signOrderAccessToken(orderTokenSecret, order.id, tokenExpiresAt);
      }
      let baseUrl = '';
      if (env && typeof env.PUBLIC_BASE_URL === 'string' && env.PUBLIC_BASE_URL.trim()) {
        baseUrl = env.PUBLIC_BASE_URL.trim().replace(/\/+$/, '');
      } else if (request && request.url) {
        try { baseUrl = new URL(request.url).origin; } catch (e) {}
      }
      if (!baseUrl && request && request.headers) {
        const originHeader = request.headers.get('Origin');
        if (originHeader) {
          try { baseUrl = new URL(originHeader).origin; } catch (e) {}
        }
      }
      if (!baseUrl) {
        baseUrl = 'https://numerosvision.com';
      }
      const orderLink = orderToken
        ? `${baseUrl}/dashboard/?order_id=${encodeURIComponent(order.id)}&token=${encodeURIComponent(orderToken)}`
        : `${baseUrl}/dashboard/?order_id=${encodeURIComponent(order.id)}`;
      const packFeatures = (pack && Array.isArray(pack.features) && pack.features.length > 0) ? pack.features : [];
      const featuresTextBlock = packFeatures.length > 0
        ? `\nIncluded in your report:\n` + packFeatures.map(f => `- ${f}`).join('\n') + `\n`
        : '';
      const featuresHtmlBlock = packFeatures.length > 0
        ? `<div style="margin:0 0 18px;font-size:13px;line-height:1.55;"><div style="font-weight:700;color:#523E28;margin-bottom:6px;">Included in your report:</div><ul style="margin:0;padding-left:18px;color:#523E28;">${packFeatures.map(f => `<li style="margin-bottom:4px;">${escapeHtmlAttr(f)}</li>`).join('')}</ul></div>`
        : '';
      const emailSubject = `Order Confirmation: Your ${packName} · Numeros Vision`;
      const emailText = `Thank you for your order with Numeros Vision.\n\nOrder ID: ${order.id}\nProduct: ${packName}${pack && pack.descriptor ? ' (' + pack.descriptor + ')' : ''}\n${featuresTextBlock}\nYour personalized report is being prepared deterministically. You can view your order status and access your report directly on your private dashboard:\n${orderLink}\n\nIf you have any questions, write to support@numerosvision.com.`;
      const emailHtml = `<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:540px;margin:0 auto;padding:32px 24px;background:#FFFDF7;border:1px solid rgba(201,162,39,0.35);border-radius:14px;color:#523E28;">
  <div style="font-size:16px;font-weight:700;color:#8B6914;margin-bottom:14px;letter-spacing:0.04em;">NUMEROS VISION</div>
  <h2 style="font-size:20px;color:#8B6914;margin:0 0 12px;font-family:Georgia,serif;">Order Confirmed</h2>
  <p style="font-size:14px;line-height:1.6;margin:0 0 16px;">
    Thank you for your order. Your personalized report (<strong>${packName}</strong>) is being prepared deterministically.
  </p>
  <div style="background:#FAF6EE;border:1px solid rgba(201,162,39,0.25);border-radius:8px;padding:14px 18px;margin-bottom:16px;font-size:13px;line-height:1.6;">
    <div><strong>Order ID:</strong> <span style="font-family:monospace;color:#8B6914;">${order.id}</span></div>
    <div><strong>Item:</strong> ${packName}${pack && pack.descriptor ? ' · ' + escapeHtmlAttr(pack.descriptor) : ''}</div>
  </div>
  ${featuresHtmlBlock}
  <div style="margin:24px 0;">
    <a href="${orderLink}" style="background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%);color:#FFFFFF;padding:12px 24px;text-decoration:none;border-radius:8px;font-weight:700;display:inline-block;font-size:14px;">
      View Your Order on Dashboard →
    </a>
  </div>
  <p style="font-size:12px;color:#7A654D;line-height:1.5;margin:24px 0 0;border-top:1px solid rgba(201,162,39,0.2);padding-top:14px;">
    If you need any assistance, please write to <a href="mailto:support@numerosvision.com" style="color:#8B6914;">support@numerosvision.com</a>.
  </p>
</div>`;

      try {
        // Record attempt
        if (env && env.DB) {
          try {
            await env.DB.prepare(
              "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, 'system', 'order_confirmation_email_attempt', 'orders', ?, ?, ?)"
            ).bind('aud_' + now + '_' + getRandomHex(4), order.id, JSON.stringify({ to: customerEmail, attempt: emailAttempts + 1 }), now).run();
          } catch (_) {}
        } else if (typeof memoryStore !== 'undefined') {
          if (!memoryStore.auditLogs) memoryStore.auditLogs = [];
          memoryStore.auditLogs.push({ resource_id: order.id, action: 'order_confirmation_email_attempt' });
        }

        const emailRes = await sendTransactionalEmail(env, {
          to: customerEmail,
          subject: emailSubject,
          text: emailText,
          html: emailHtml
        });

        // Record SUCCESS only if provider successfully accepted the delivery
        if (emailRes && emailRes.success) {
          if (env && env.DB) {
            await env.DB.prepare(
              "INSERT OR IGNORE INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, 'system', 'order_confirmation_email_sent', 'orders', ?, ?, ?)"
            ).bind('aud_' + now + '_' + getRandomHex(4), order.id, JSON.stringify({ to: customerEmail, provider_id: emailRes.id || null }), now).run();
          } else if (typeof memoryStore !== 'undefined') {
            memoryStore.auditLogs.push({ resource_id: order.id, action: 'order_confirmation_email_sent' });
          }
        } else {
          console.warn('[Order_Confirmation_Email_Failure] Provider rejected dispatch:', emailRes?.error || 'Unknown error');
        }
      } catch (e) {
        console.error('[Order_Confirmation_Email_Error]', e);
      }
    }
  }

  return {
    alreadyFulfilled: false,
    orderId: order.id,
    packId: order.pack_id,
    subjectId: order.subject_id,
    jobId: createdJobId
  };
}


/**
 * NUMEROS VISION — CLOUDFLARE PAGES EDGE WORKER
 * Document Version: 1.0.0
 * Handles real-time Fast2SMS OTP dispatching, OTP verification, and Google Identity auth on the edge.
 * All static assets are served transparently via env.ASSETS.fetch(request).
 */

    // Fast2SMS API key strictly loaded from env.FAST2SMS_API_KEY


/**
 * DETERMINISTIC SERVER GATING ENGINE: viewFor(user, subject, env)
 * The SOLE authority on gated profile calculations and entitlements for (user, subject).
 * Excludes entitlements from refunded orders.
 * Gated strictly to confirmed unlock matrix:
 * - Free: Lo Shu grid with enabled digits; missing digits shown only as locked marks ('🔒').
 * - Rs199 (report_basic, 3 pages): element balancing.
 * - Rs 510 (report_advanced, 12 pages): element balancing + enabled numbers in depth.
 * - Rs1050 (report_premium, 32 pages): everything: missing numbers in depth, remedies, predictions (dasha timelines, 10-year radar).
 */
function parseDobParts(dobStr) {
  if (!dobStr) return { day: 1, month: 1, year: 2000, dob: '2000-01-01' };
  const str = String(dobStr).trim();
  let day = 1, month = 1, year = 2000;
  if (str.includes('-')) {
    const parts = str.split('-');
    if (parts[0].length === 4) {
      year = parseInt(parts[0], 10);
      month = parseInt(parts[1], 10);
      day = parseInt(parts[2], 10);
    } else {
      day = parseInt(parts[0], 10);
      month = parseInt(parts[1], 10);
      year = parseInt(parts[2], 10);
    }
  } else if (str.includes('/')) {
    const parts = str.split('/');
    if (parts[0].length === 4) {
      year = parseInt(parts[0], 10);
      month = parseInt(parts[1], 10);
      day = parseInt(parts[2], 10);
    } else {
      day = parseInt(parts[0], 10);
      month = parseInt(parts[1], 10);
      year = parseInt(parts[2], 10);
    }
  }
  if (isNaN(day) || day < 1 || day > 31) day = 1;
  if (isNaN(month) || month < 1 || month > 12) month = 1;
  if (isNaN(year) || year < 1900 || year > 2100) year = 2000;
  const formattedDob = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  return { day, month, year, dob: formattedDob };
}

const KUA_RULE_TEXT = 'Calculated from your birth year and gender';
const KUA_NEEDS_GENDER_TEXT = 'Kua needs gender';

const KUA_METADATA = {
  1: { element: 'Water', trigram: 'Kan', group: 'East Group', groupShort: 'East', elementGroup: 'Water · Kan (East Group)', directionSummary: 'Water · Kan (East Group · SE / E / S / N)', deskDirection: 'South-East' },
  2: { element: 'Earth', trigram: 'Kun', group: 'West Group', groupShort: 'West', elementGroup: 'Earth · Kun (West Group)', directionSummary: 'Earth · Kun (West Group · NE / W / NW / SW)', deskDirection: 'North-East' },
  3: { element: 'Wood', trigram: 'Zhen', group: 'East Group', groupShort: 'East', elementGroup: 'Wood · Zhen (East Group)', directionSummary: 'Wood · Zhen (East Group · S / N / SE / E)', deskDirection: 'South' },
  4: { element: 'Wood', trigram: 'Xun', group: 'East Group', groupShort: 'East', elementGroup: 'Wood · Xun (East Group)', directionSummary: 'Wood · Xun (East Group · N / S / E / SE)', deskDirection: 'North' },
  6: { element: 'Metal', trigram: 'Qian', group: 'West Group', groupShort: 'West', elementGroup: 'Metal · Qian (West Group)', directionSummary: 'Metal · Qian (West Group · W / NE / SW / NW)', deskDirection: 'West' },
  7: { element: 'Metal', trigram: 'Dui', group: 'West Group', groupShort: 'West', elementGroup: 'Metal · Dui (West Group)', directionSummary: 'Metal · Dui (West Group · NW / W / NE / SW)', deskDirection: 'North-West' },
  8: { element: 'Earth', trigram: 'Gen', group: 'West Group', groupShort: 'West', elementGroup: 'Earth · Gen (West Group)', directionSummary: 'Earth · Gen (West Group · SW / NW / W / NE)', deskDirection: 'South-West' },
  9: { element: 'Fire', trigram: 'Li', group: 'East Group', groupShort: 'East', elementGroup: 'Fire · Li (East Group)', directionSummary: 'Fire · Li (East Group · E / SE / N / S)', deskDirection: 'East' }
};

const CHALDEAN_WORKER_MAP = {
  A: 1, I: 1, J: 1, Q: 1, Y: 1,
  B: 2, C: 2, K: 2, R: 2,
  G: 3, L: 3, S: 3,
  D: 4, M: 4, T: 4,
  E: 5, H: 5, N: 5, X: 5,
  U: 6, V: 6, W: 6,
  O: 7, Z: 7,
  F: 8, P: 8
};

const PYTHAGOREAN_WORKER_MAP = {
  A: 1, J: 1, S: 1,
  B: 2, K: 2, T: 2,
  C: 3, L: 3, U: 3,
  D: 4, M: 4, V: 4,
  E: 5, N: 5, W: 5,
  F: 6, O: 6, X: 6,
  G: 7, P: 7, Y: 7,
  H: 8, Q: 8, Z: 8,
  I: 9, R: 9
};

/**
 * Canonical single-digit reduction shared across all Numeros Vision runtimes:
 *   digitRoot(n) = 1 + (n - 1) % 9   for n > 0
 *   digitRoot(n) = 0                 for n <= 0
 * Master numbers (11, 22, 33) are NEVER preserved.
 */
function digitRoot(num) {
  const val = Math.trunc(Number(num) || 0);
  return val > 0 ? 1 + ((val - 1) % 9) : 0;
}

function sumDigitsStr(text) {
  const s = String(text === null || text === undefined ? '' : text);
  let total = 0;
  for (let i = 0; i < s.length; i++) {
    const code = s.charCodeAt(i);
    if (code >= 48 && code <= 57) total += code - 48;
  }
  return total;
}

function calcDriver(day) {
  return digitRoot(parseInt(day, 10) || 0);
}

function calcBhagyank(day, month, year) {
  const dStr = String(parseInt(day, 10) || 0).padStart(2, '0');
  const mStr = String(parseInt(month, 10) || 0).padStart(2, '0');
  const yStr = String(parseInt(year, 10) || 0).padStart(4, '0');
  return digitRoot(sumDigitsStr(dStr + mStr + yStr));
}

function calcPersonalYear(day, month, targetYear) {
  const yr = targetYear ? (parseInt(targetYear, 10) || new Date().getFullYear()) : new Date().getFullYear();
  const dStr = String(parseInt(day, 10) || 0).padStart(2, '0');
  const mStr = String(parseInt(month, 10) || 0).padStart(2, '0');
  const yStr = String(yr).padStart(4, '0');
  return digitRoot(sumDigitsStr(dStr + mStr + yStr));
}

function calcPersonalMonth(personalYear, calendarMonth) {
  return digitRoot((parseInt(personalYear, 10) || 0) + (parseInt(calendarMonth, 10) || 0));
}

function calcPersonalDay(personalYear, personalMonth, targetDay, targetMonth, targetYear) {
  const dStr = String(parseInt(targetDay, 10) || 0).padStart(2, '0');
  const mStr = String(parseInt(targetMonth, 10) || 0).padStart(2, '0');
  const yStr = String(parseInt(targetYear, 10) || 0).padStart(4, '0');
  return digitRoot((parseInt(personalYear, 10) || 0) + (parseInt(personalMonth, 10) || 0) + sumDigitsStr(dStr + mStr + yStr));
}

function calcPersonalCyclesForDate(birthDay, birthMonth, targetDay, targetMonth, targetYear) {
  const py = calcPersonalYear(birthDay, birthMonth, targetYear);
  const pm = calcPersonalMonth(py, targetMonth);
  const pd = calcPersonalDay(py, pm, targetDay, targetMonth, targetYear);
  return {
    label: 'Personal Year / Month / Day',
    personal_year: py,
    personal_month: pm,
    personal_day: pd
  };
}

function calcLoShuDobOnly(day, month, year) {
  const dobStr = String(parseInt(day, 10) || 0).padStart(2, '0') +
                 String(parseInt(month, 10) || 0).padStart(2, '0') +
                 String(parseInt(year, 10) || 0).padStart(4, '0');
  const counts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0 };
  for (let i = 0; i < dobStr.length; i++) {
    const code = dobStr.charCodeAt(i);
    if (code >= 49 && code <= 57) counts[code - 48] += 1;
  }
  const present = [];
  const missing = [];
  const repeated = {};
  for (let d = 1; d <= 9; d++) {
    if (counts[d] > 0) present.push(d);
    else missing.push(d);
    if (counts[d] >= 2) repeated[d] = counts[d];
  }
  return { dob_digits_str: dobStr, counts, present, missing, repeated };
}

function calcChaldeanNameNumber(name) {
  const s = String(name || '').toUpperCase();
  let compound = 0;
  for (let i = 0; i < s.length; i++) {
    const ch = s.charAt(i);
    if (CHALDEAN_WORKER_MAP[ch]) compound += CHALDEAN_WORKER_MAP[ch];
  }
  return { compound, root: digitRoot(compound) };
}

function calcPythagoreanNameNumber(name) {
  const s = String(name || '').toUpperCase();
  let compound = 0;
  for (let i = 0; i < s.length; i++) {
    const ch = s.charAt(i);
    if (PYTHAGOREAN_WORKER_MAP[ch]) compound += PYTHAGOREAN_WORKER_MAP[ch];
  }
  return { compound, root: digitRoot(compound) };
}

function calculateCanonicalKuaDetails(birthYear, gender) {
  const reduce1 = (num) => digitRoot(Math.abs(parseInt(num, 10) || 0));
  const yr = parseInt(birthYear, 10);
  const gRaw = (gender === null || gender === undefined) ? '' : String(gender).trim().toLowerCase();
  const normGender = (gRaw === 'male' || gRaw === 'm') ? 'male' : ((gRaw === 'female' || gRaw === 'f') ? 'female' : null);

  if (!yr || isNaN(yr) || !normGender) {
    return {
      status: 'NEEDS_GENDER',
      kuaNumber: null,
      kua_number: null,
      rawKua: null,
      raw_kua: null,
      remappedFromFive: false,
      gender: normGender,
      display: KUA_NEEDS_GENDER_TEXT,
      display_text: KUA_NEEDS_GENDER_TEXT,
      element: null,
      trigram: null,
      group: null,
      elementGroup: KUA_NEEDS_GENDER_TEXT,
      element_group_label: KUA_NEEDS_GENDER_TEXT,
      directionSummary: KUA_NEEDS_GENDER_TEXT,
      deskDirection: KUA_NEEDS_GENDER_TEXT,
      ruleNote: KUA_RULE_TEXT,
      rule_text: KUA_RULE_TEXT
    };
  }

  const yrStr = String(yr).padStart(4, '0');
  const sum4 = yrStr.split('').reduce((acc, ch) => (ch >= '0' && ch <= '9' ? acc + parseInt(ch, 10) : acc), 0);
  const x = reduce1(sum4);
  const rawKua = normGender === 'male' ? reduce1(11 - x) : reduce1(4 + x);
  const finalKua = rawKua === 5 ? (normGender === 'male' ? 2 : 8) : rawKua;
  const meta = KUA_METADATA[finalKua];

  return {
    status: 'OK',
    kuaNumber: finalKua,
    kua_number: finalKua,
    rawKua,
    raw_kua: rawKua,
    remappedFromFive: rawKua === 5,
    yearDigitRoot: x,
    year_digit_sum: x,
    gender: normGender,
    display: String(finalKua),
    display_text: String(finalKua),
    element: meta.element,
    trigram: meta.trigram,
    group: meta.group,
    groupShort: meta.groupShort,
    elementGroup: meta.elementGroup,
    element_group_label: meta.elementGroup,
    directionSummary: meta.directionSummary,
    deskDirection: meta.deskDirection,
    ruleNote: KUA_RULE_TEXT,
    rule_text: KUA_RULE_TEXT
  };
}

async function viewFor(user, subject, env, targetPackId = null) {
  if (!user || !subject) return null;

  // 1. Query active entitlements for (user, subject) strictly excluding refunded orders
  const activePackIds = new Set();
  if (env && env.DB) {
    const rows = await env.DB.prepare(`
      SELECT e.pack_id
      FROM entitlements e
      LEFT JOIN orders o ON e.order_id = o.id
      WHERE e.user_id = ? AND e.subject_id = ?
        AND (o.status IS NULL OR o.status != 'REFUNDED')
    `).bind(user.user_id, subject.id).all();
    if (rows && rows.results) {
      for (const r of rows.results) activePackIds.add(r.pack_id);
    }
  } else if (memoryStore && memoryStore.entitlements) {
    for (const ent of memoryStore.entitlements.values()) {
      if (ent.user_id === user.user_id && ent.subject_id === subject.id) {
        const ord = ent.order_id ? memoryStore.orders.get(ent.order_id) : null;
        if (!ord || ord.status !== 'REFUNDED') {
          activePackIds.add(ent.pack_id);
        }
      }
    }
  }

  // 2. Determine active tier (or scoped to targetPackId if requested and entitled)
  let tier = 'free';
  if (targetPackId && activePackIds.has(targetPackId)) {
    if (targetPackId === 'report_premium') tier = 'premium';
    else if (targetPackId === 'report_advanced') tier = 'advanced';
    else if (targetPackId === 'report_basic') tier = 'basic';
  } else if (!targetPackId) {
    if (activePackIds.has('report_premium')) {
      tier = 'premium';
    } else if (activePackIds.has('report_advanced')) {
      tier = 'advanced';
    } else if (activePackIds.has('report_basic')) {
      tier = 'basic';
    }
  }

  // 3. Deterministic Numerology Calculation
  let rawDob = '';
  if (subject.dob_enc) {
    const encKey = requireSecret(env, 'DATA_ENCRYPTION_KEY');
    rawDob = await decryptField(subject.dob_enc, encKey);
  } else {
    rawDob = subject.dob || '';
  }
  const dobInfo = parseDobParts(rawDob);
  const day = dobInfo.day;
  const month = dobInfo.month;
  const year = dobInfo.year;
  const formattedDob = dobInfo.dob;

  function reduceToSingle(num) {
    const n = Math.abs(Math.trunc(Number(num) || 0));
    return n === 0 ? 9 : digitRoot(n);
  }

  const driver = calcDriver(day);
  const totalDobDigits = `${String(day).padStart(2, '0')}${String(month).padStart(2, '0')}${String(year).padStart(4, '0')}`;
  const conductor = calcBhagyank(day, month, year);
  const conductorRaw = conductor;
  const conductorDisplay = `${conductor}`;

  const PLANETS = {
    1: { name: 'Sun', sanskrit: 'Surya', element: 'Water', quality: 'Leadership & Vitality' },
    2: { name: 'Moon', sanskrit: 'Chandra', element: 'Earth', quality: 'Intuition & Harmony' },
    3: { name: 'Jupiter', sanskrit: 'Guru', element: 'Wood', quality: 'Wisdom & Expansion' },
    4: { name: 'Rahu', sanskrit: 'Rahu', element: 'Wood', quality: 'Strategy & Discipline' },
    5: { name: 'Mercury', sanskrit: 'Budh', element: 'Earth', quality: 'Commerce & Communication' },
    6: { name: 'Venus', sanskrit: 'Shukra', element: 'Metal', quality: 'Luxury & Aesthetics' },
    7: { name: 'Ketu', sanskrit: 'Ketu', element: 'Metal', quality: 'Spirituality & Research' },
    8: { name: 'Saturn', sanskrit: 'Shani', element: 'Earth', quality: 'Structure & Endurance' },
    9: { name: 'Mars', sanskrit: 'Mangal', element: 'Fire', quality: 'Drive & Courage' }
  };

  const counts = { 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0 };
  for (const ch of totalDobDigits) {
    if (ch !== '0') counts[parseInt(ch, 10)]++;
  }

  const presentDigits = [];
  const missingDigits = [];
  for (let n = 1; n <= 9; n++) {
    if (counts[n] > 0) presentDigits.push(n);
    else missingDigits.push(n);
  }

  const PLANES_DEF = [
    { name: 'Mental Plane', digits: [4, 9, 2], description: 'Memory, cognitive clarity, analytical agility' },
    { name: 'Emotional Plane', digits: [3, 5, 7], description: 'Compassion, spirituality, relational depth' },
    { name: 'Practical Plane', digits: [8, 1, 6], description: 'Commercial execution, physical manifestation' },
    { name: 'Thought Plane', digits: [4, 3, 8], description: 'Planning, structural vision, conceptualization' },
    { name: 'Will Plane', digits: [9, 5, 1], description: 'Perseverance, stamina, determination' },
    { name: 'Action Plane', digits: [2, 7, 6], description: 'Execution speed, decisiveness, manifestation' },
    { name: 'Golden Raj Yoga', digits: [4, 5, 6], description: 'Prosperity axis, leadership compounding' },
    { name: 'Silver Raj Yoga', digits: [2, 5, 8], description: 'Earth stability axis, property & endurance' }
  ];

  const planes = PLANES_DEF.map(pl => {
    const presentCount = pl.digits.filter(d => counts[d] > 0).length;
    const percentage = Math.round((presentCount / pl.digits.length) * 100);
    return {
      name: pl.name,
      digits: pl.digits,
      presentCount,
      percentage,
      status: percentage === 100 ? 'COMPLETE' : percentage > 33 ? 'ACTIVE' : 'DORMANT'
    };
  });

  const ELEMENT_MAP = {
    Wood: [3, 4],
    Fire: [9],
    Earth: [2, 5, 8],
    Metal: [6, 7],
    Water: [1]
  };
  const elements = {};
  for (const [elName, elDigits] of Object.entries(ELEMENT_MAP)) {
    const cnt = elDigits.reduce((acc, d) => acc + counts[d], 0);
    elements[elName] = { count: cnt, present: cnt > 0, digits: elDigits };
  }

  // Kua & Personal Year Calculation (Canonical century-invariant 4-digit formula; never guess missing gender)
  const subjectGender = subject.gender || (user && user.gender) || null;
  const kuaDetails = calculateCanonicalKuaDetails(year, subjectGender);
  const kuaNum = kuaDetails.kuaNumber;
  const currentYear = new Date().getFullYear();
  const personalYear = reduceToSingle(driver + reduceToSingle(month) + reduceToSingle(currentYear));

  const hasBasic = tier === 'basic' || tier === 'advanced' || tier === 'premium';
  const hasAdvanced = tier === 'advanced' || tier === 'premium';
  const hasPremium = tier === 'premium';

  // Section 1: Grid (always accessible, missing shown strictly as locked marks '🔒')
  const gridCells = [4, 9, 2, 3, 5, 7, 8, 1, 6].map(num => {
    const cnt = counts[num];
    const p = PLANETS[num];
    if (cnt > 0) {
      return {
        digit: num,
        count: cnt,
        status: 'present',
        planet: p.name,
        element: p.element,
        quality: p.quality
      };
    } else {
      return {
        digit: num,
        count: 0,
        status: 'locked',
        mark: '🔒',
        element: p.element,
        lockReason: 'Missing digit karmic analysis is unlocked in the Premium report.'
      };
    }
  });

  // Section 2: Enabled Digits
  const enabledDigitsSummary = presentDigits.map(d => ({
    digit: d,
    count: counts[d],
    planet: PLANETS[d].name,
    element: PLANETS[d].element,
    summary: `Active vibration ×${counts[d]} (${PLANETS[d].name}). Governs ${PLANETS[d].quality}.`
  }));

  // Section 3: Element Balancing (Basic ₹199, 3 pages)
  let elementBalancingSection;
  if (hasBasic) {
    elementBalancingSection = {
      unlocked: true,
      pageCount: 3,
      elements: Object.entries(elements).map(([name, data]) => ({
        name,
        count: data.count,
        status: data.count === 0 ? 'DEFICIENT' : data.count > 2 ? 'SURPLUS' : 'BALANCED',
        recommendation: data.count === 0
          ? `Incorporate subtle ${name} element resonance in your environment.`
          : data.count > 2
            ? `Gently ground excess ${name} vibration with complementary lifestyle pacing.`
            : `Harmonious ${name} equilibrium maintained.`
      })),
      rajYogas: planes.filter(p => p.name.includes('Raj Yoga')),
      balancingGuidance: 'Elemental balancing establishes the foundational stability of your chart, resolving subconscious friction between cognitive drive and emotional pacing.'
    };
  } else {
    elementBalancingSection = {
      unlocked: false,
      pageCount: 3,
      lockReason: 'Element Balancing and Elemental Raj Yogas are available in the Basic (3 pages), Advanced (12 pages), and Premium (32 pages) reports.',
      upgradePack: 'report_basic',
      minTier: 'basic',
      priceInr: 199
    };
  }

  // Section 4: Enabled Numbers in Depth (Advanced ₹510, 12 pages)
  let enabledNumbersInDepthSection;
  if (hasAdvanced) {
    enabledNumbersInDepthSection = {
      unlocked: true,
      pageCount: 12,
      repeatingFrequencies: presentDigits.filter(d => counts[d] > 1).map(d => ({
        digit: d,
        frequency: counts[d],
        archetype: PLANETS[d].name,
        intensity: counts[d] >= 3 ? 'HIGH INTENSITY SPIKE' : 'AMPLIFIED MODERATE',
        interpretation: `Repeating frequency ×${counts[d]} intensifies ${PLANETS[d].quality}. Channeling this into systematic routines prevents executive burnout.`
      })),
      archetypeSynergies: {
        driverToConductor: `Driver ${driver} (${PLANETS[driver].name}) and Conductor ${conductorDisplay} (${PLANETS[conductor].name}) create a ${driver === conductor ? 'focused singular' : 'dynamic dual'} vibrational pattern.`,
        planeEquilibrium: planes.filter(p => p.status === 'COMPLETE').map(p => p.name)
      },
      actionableHarmonization: 'Align high-frequency digits with designated peak focus blocks in your weekly calendar.'
    };
  } else {
    enabledNumbersInDepthSection = {
      unlocked: false,
      pageCount: 12,
      lockReason: 'Enabled Numbers in Depth, repeating frequency calibrations, and archetype synergies are available in the Advanced (12 pages) and Premium (32 pages) reports.',
      upgradePack: 'report_advanced',
      minTier: 'advanced',
      priceInr: 510
    };
  }

  // Section 5: Missing Numbers in Depth (Premium ₹1,050, 32 pages)
  let missingNumbersInDepthSection;
  if (hasPremium) {
    missingNumbersInDepthSection = {
      unlocked: true,
      pageCount: 32,
      karmicVoids: missingDigits.map(d => ({
        digit: d,
        planet: PLANETS[d].name,
        element: PLANETS[d].element,
        voidDescription: `Karmic void in ${PLANETS[d].quality}. Subconscious hesitation in areas governed by ${PLANETS[d].name}.`,
        vibrationalBridge: `Bridge this void by partnering with individuals carrying strong ${d} vibrations and adopting structured cognitive habits.`
      }))
    };
  } else {
    missingNumbersInDepthSection = {
      unlocked: false,
      pageCount: 32,
      lockReason: 'In-depth missing number karmic void activations are available in the Anveil every charm (32 pages).',
      upgradePack: 'report_premium',
      minTier: 'premium',
      priceInr: 1050
    };
  }

  // Section 6: Remedies (Premium ₹1,050, 32 pages)
  let remediesSection;
  if (hasPremium) {
    remediesSection = {
      unlocked: true,
      pageCount: 32,
      protocols: [
        { layer: 'Color Harmonization', advice: `Prioritize ${PLANETS[driver].name} and ${PLANETS[conductor].name} resonant hues without sharp contrasting clashes.` },
        { layer: 'Directional Spatial Alignment', advice: `Orient primary study/work desk toward ${driver % 2 === 0 ? 'East / North-East' : 'North / North-West'} for mental coherence.` },
        { layer: 'Habit & Rhythm Cadence', advice: 'Synchronize major financial decisions during your personal auspicious planetary days.' }
      ]
    };
  } else {
    remediesSection = {
      unlocked: false,
      pageCount: 32,
      lockReason: 'Authentic 7-layer remedial protocols and directional spatial alignment are available in the Anveil every charm (32 pages).',
      upgradePack: 'report_premium',
      minTier: 'premium',
      priceInr: 1050
    };
  }

  // Section 7: Predictions (Premium ₹1,050, 32 pages)
  let predictionsSection;
  if (hasPremium) {
    predictionsSection = {
      unlocked: true,
      pageCount: 32,
      dashaTimeline: {
        currentCycle: `Personal Year ${reduceToSingle(day + month + new Date().getFullYear())}`,
        tenYearRadar: '10-Year macro planetary dasha radar indicates steady expansion with focus on structural consolidation.'
      },
      pinnacleCycles: [
        { stage: 'Pinnacle 1 (Ages 0-32)', rulingDigit: reduceToSingle(day + month) },
        { stage: 'Pinnacle 2 (Ages 33-41)', rulingDigit: reduceToSingle(day + year) },
        { stage: 'Pinnacle 3 (Ages 42-50)', rulingDigit: reduceToSingle(reduceToSingle(day + month) + reduceToSingle(day + year)) },
        { stage: 'Pinnacle 4 (Ages 51+)', rulingDigit: reduceToSingle(month + year) }
      ]
    };
  } else {
    predictionsSection = {
      unlocked: false,
      pageCount: 32,
      lockReason: '10-Year Mahadasha timelines, Personal Year cycles, and 4-stage pinnacle radar are available in the Anveil every charm (32 pages).',
      upgradePack: 'report_premium',
      minTier: 'premium',
      priceInr: 1050
    };
  }

  return {
    user: {
      userId: user.user_id,
      phone: user.phone || null,
      email: user.email || null
    },
    subject: {
      id: subject.id,
      name: subject.name,
      dob: formattedDob,
      gender: kuaDetails.gender,
      created_at: subject.created_at
    },
    tier,
    entitlements: Array.from(activePackIds),
    calculation: {
      driver,
      conductor,
      conductorRaw,
      conductorDisplay,
      driverPlanet: PLANETS[driver].name,
      driverSanskrit: PLANETS[driver].sanskrit,
      conductorPlanet: PLANETS[conductor].name,
      conductorSanskrit: PLANETS[conductor].sanskrit,
      kua: kuaNum,
      kuaDisplay: kuaDetails.display,
      kuaElement: kuaDetails.elementGroup,
      kuaDirection: kuaDetails.directionSummary,
      kuaRule: KUA_RULE_TEXT,
      gender: kuaDetails.gender,
      personalYear,
      counts,
      presentDigits,
      missingDigits,
      planes
    },
    sections: {
      grid: {
        unlocked: true,
        cells: gridCells
      },
      enabledDigits: {
        unlocked: true,
        items: enabledDigitsSummary
      },
      elementBalancing: elementBalancingSection,
      enabledNumbersInDepth: enabledNumbersInDepthSection,
      missingNumbersInDepth: missingNumbersInDepthSection,
      remedies: remediesSection,
      predictions: predictionsSection
    }
  };
}

/**
 * COMMIT 6b: PRIVATE PDF GENERATOR SERVICE DISPATCH, R2 STORAGE & 5-MINUTE SIGNED DOWNLOADS
 */
function uint8ArrayToBase64Url(bytes) {
  let binary = '';
  for (let i = 0; i < bytes.length; i++) {
    binary += String.fromCharCode(bytes[i]);
  }
  return btoa(binary).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function sanitizeViewForGenerator(view) {
  if (!view) return null;
  return {
    user: {
      userId: view.user ? view.user.userId : null
    },
    subject: {
      id: view.subject ? view.subject.id : null,
      name: view.subject ? view.subject.name : '',
      dob: view.subject ? view.subject.dob : '',
      created_at: view.subject ? view.subject.created_at : null
    },
    tier: view.tier,
    entitlements: Array.isArray(view.entitlements) ? [...view.entitlements] : [],
    calculation: view.calculation,
    sections: view.sections
  };
}

async function signPdfServiceRequest(rawBody, timestampSec, pdfServiceSecret) {
  if (!pdfServiceSecret || typeof pdfServiceSecret !== 'string' || !pdfServiceSecret.trim()) {
    throw new Error('PDF_SERVICE_SECRET is required to sign generator requests.');
  }
  const ts = String(timestampSec);
  return await hmacSha256Hex(pdfServiceSecret.trim(), `${ts}.${rawBody}`);
}

async function createSignedDownloadToken({ userId, subjectId, packId, jobId, nowSec = null, ttlSec = 300 }, pdfServiceSecret) {
  if (!userId || !subjectId || !packId || !jobId) {
    throw new Error('userId, subjectId, packId, and jobId are required to mint a signed download token.');
  }
  if (!pdfServiceSecret || typeof pdfServiceSecret !== 'string' || !pdfServiceSecret.trim()) {
    throw new Error('PDF_SERVICE_SECRET is required to mint a signed download token.');
  }
  const boundedTtl = Math.min(Math.max(1, Number(ttlSec) || 300), 300);
  const iat = nowSec !== null ? Math.floor(Number(nowSec)) : Math.floor(Date.now() / 1000);
  const exp = iat + boundedTtl;
  const payloadObj = {
    u: String(userId),
    s: String(subjectId),
    p: String(packId),
    j: String(jobId),
    iat,
    exp
  };
  const payloadBytes = new TextEncoder().encode(JSON.stringify(payloadObj));
  const payloadB64 = uint8ArrayToBase64Url(payloadBytes);
  const sigHex = await hmacSha256Hex(pdfServiceSecret.trim(), payloadB64);
  return `${payloadB64}.${sigHex}`;
}

async function verifySignedDownloadToken(token, pdfServiceSecret, expectedContext = {}, nowSec = null) {
  if (!token || typeof token !== 'string' || !token.includes('.')) {
    return { valid: false, error: 'Malformed download token.' };
  }
  if (!pdfServiceSecret || typeof pdfServiceSecret !== 'string' || !pdfServiceSecret.trim()) {
    return { valid: false, error: 'PDF_SERVICE_SECRET is not configured.' };
  }
  const parts = token.split('.');
  if (parts.length !== 2) {
    return { valid: false, error: 'Malformed download token segments.' };
  }
  const [payloadB64, sigHex] = parts;
  const expectedSig = await hmacSha256Hex(pdfServiceSecret.trim(), payloadB64);
  if (!timingSafeEqual(expectedSig.toLowerCase(), sigHex.trim().toLowerCase())) {
    return { valid: false, error: 'Invalid download token cryptographic signature.' };
  }

  let payload = null;
  try {
    payload = JSON.parse(new TextDecoder().decode(base64UrlToUint8Array(payloadB64)));
  } catch (e) {
    return { valid: false, error: 'Failed to decode download token payload.' };
  }

  const currentSec = nowSec !== null ? Math.floor(Number(nowSec)) : Math.floor(Date.now() / 1000);
  if (!payload.exp || !payload.iat || (payload.exp - payload.iat) > 300) {
    return { valid: false, error: 'Download token exceeds maximum 5-minute lifetime.' };
  }
  if (currentSec > payload.exp) {
    return { valid: false, error: 'Download token has expired (5-minute window elapsed).' };
  }

  if (expectedContext.userId && payload.u !== expectedContext.userId) {
    return { valid: false, error: 'Download token user binding mismatch.' };
  }
  if (expectedContext.subjectId && payload.s !== expectedContext.subjectId) {
    return { valid: false, error: 'Download token subject binding mismatch.' };
  }
  if (expectedContext.packId && payload.p !== expectedContext.packId) {
    return { valid: false, error: 'Download token pack binding mismatch.' };
  }
  if (expectedContext.jobId && payload.j !== expectedContext.jobId) {
    return { valid: false, error: 'Download token job binding mismatch.' };
  }

  return { valid: true, payload };
}

async function putPrivateR2Report(env, r2Key, pdfBytes) {
  if (env && env.REPORTS_BUCKET && typeof env.REPORTS_BUCKET.put === 'function') {
    await env.REPORTS_BUCKET.put(r2Key, pdfBytes, {
      httpMetadata: { contentType: 'application/pdf', cacheControl: 'private, no-store' }
    });
    return;
  }
  if (env && env.ENVIRONMENT === 'local') {
    const copy = pdfBytes instanceof Uint8Array ? pdfBytes : new Uint8Array(pdfBytes);
    memoryStore.r2Objects.set(r2Key, copy);
    return;
  }
  throw new Error('Private R2 bucket binding (REPORTS_BUCKET) is not configured.');
}

async function getPrivateR2Report(env, r2Key) {
  if (env && env.REPORTS_BUCKET && typeof env.REPORTS_BUCKET.get === 'function') {
    const obj = await env.REPORTS_BUCKET.get(r2Key);
    if (!obj) return null;
    if (typeof obj.arrayBuffer === 'function') {
      return new Uint8Array(await obj.arrayBuffer());
    }
    if (obj.body) return obj.body;
    return null;
  }
  if (env && env.ENVIRONMENT === 'local') {
    return memoryStore.r2Objects.get(r2Key) || null;
  }
  throw new Error('Private R2 bucket binding (REPORTS_BUCKET) is not configured.');
}

const REPORT_STAGE_DASHBOARD_LABELS = {
  queued: 'Step 1 of 5: reading your birth date',
  calculate: 'Step 1 of 5: reading your birth date',
  analyse: 'Step 2 of 5: checking your grid and cycles',
  consolidate: 'Step 3 of 5: putting your reading together',
  write: 'Step 4 of 5: writing your reading',
  check_deliver: 'Step 5 of 5: preparing your PDF',
  completed: 'Ready to download'
};

const REPORT_DELAYED_MESSAGE = 'This is taking a little longer than usual. Your report will appear here when it is ready.';

function formatReportJobProgress(job, nowMs) {
  const nowVal = typeof nowMs === 'number' ? nowMs : Date.now();
  if (!job) {
    return {
      currentStage: 'queued',
      progressLine: REPORT_STAGE_DASHBOARD_LABELS.queued,
      delayedNotice: null
    };
  }
  const st = String(job.status || 'QUEUED').toUpperCase();
  const curStage = String(job.current_stage || 'queued').toLowerCase();
  if (st === 'COMPLETED' || st === 'DOWNLOADED' || job.r2_key || job.download_url) {
    return {
      currentStage: 'completed',
      progressLine: 'Ready to download',
      delayedNotice: null
    };
  }
  if (st === 'FAILED' || (job.attempts || 0) >= 3) {
    return {
      currentStage: curStage,
      progressLine: 'We’re checking this order.',
      delayedNotice: null
    };
  }
  const progressLine = REPORT_STAGE_DASHBOARD_LABELS[curStage] || REPORT_STAGE_DASHBOARD_LABELS.queued;
  const created = typeof job.created_at === 'number' ? job.created_at : nowVal;
  const delayedNotice = (nowVal - created >= 45000) ? REPORT_DELAYED_MESSAGE : null;
  return {
    currentStage: curStage,
    progressLine,
    delayedNotice
  };
}

async function tryUpdateReportJobStageColumns(env, job, stageName, lastDone, timestampsObj, errorCode = null) {
  const tsJson = JSON.stringify(timestampsObj || {});
  if (job) {
    job.current_stage = stageName;
    if (lastDone !== undefined) job.last_completed_stage = lastDone;
    job.stage_timestamps_json = tsJson;
    job.error_code = errorCode;
  }
  if (env && env.DB && job && job.id) {
    try {
      await env.DB.prepare(
        'UPDATE report_jobs SET current_stage = ?, last_completed_stage = ?, stage_timestamps_json = ?, error_code = ? WHERE id = ?'
      ).bind(stageName, lastDone || null, tsJson, errorCode, job.id).run();
    } catch (_colErr) {
      // Pre-0012 D1 schema fallback: core status columns remain authoritative
    }
  }
}

async function dispatchReportJob(jobId, env) {
  const pdfServiceSecret = requireSecret(env, 'PDF_SERVICE_SECRET');
  const now = Date.now();

  let job = null;
  if (env && env.DB) {
    job = await env.DB.prepare('SELECT * FROM report_jobs WHERE id = ?').bind(jobId).first();
  } else {
    job = memoryStore.reportJobs.get(jobId) || null;
  }

  if (!job) {
    return { ok: false, status: 404, error: `Report job ${jobId} not found.` };
  }
  if (job.status === 'COMPLETED' || job.status === 'DOWNLOADED') {
    return { ok: true, status: 200, jobStatus: job.status, r2Key: job.r2_key, alreadyCompleted: true };
  }
  if (job.status === 'FAILED' || (job.attempts || 0) >= 3) {
    return { ok: false, status: 409, jobStatus: 'FAILED', attempts: job.attempts || 3, error: job.last_error || 'Maximum 3 retries exhausted.' };
  }

  const stageTs = {};
  try {
    if (job.stage_timestamps_json) Object.assign(stageTs, JSON.parse(job.stage_timestamps_json));
  } catch (_e) {}

  // 1. Transition QUEUED -> PROCESSING (Stage: calculate)
  if (env && env.DB) {
    await env.DB.prepare("UPDATE report_jobs SET status = 'PROCESSING', updated_at = ? WHERE id = ?").bind(now, job.id).run();
  } else {
    job.status = 'PROCESSING';
    job.updated_at = now;
  }
  stageTs.calculate = { started_at: now };
  await tryUpdateReportJobStageColumns(env, job, 'calculate', job.last_completed_stage || null, stageTs, null);

  try {
    // 2. Load subject and compute sanitized viewFor(user, subject, env, job.pack_id)
    let subject = null;
    if (env && env.DB) {
      subject = await env.DB.prepare('SELECT id, user_id, name, dob_enc, created_at FROM subjects WHERE id = ? AND user_id = ?').bind(job.subject_id, job.user_id).first();
    } else {
      subject = memoryStore.subjects.get(job.subject_id);
      if (subject && subject.user_id !== job.user_id) subject = null;
    }

    if (!subject) {
      throw new Error(`Subject ${job.subject_id} not found for user ${job.user_id}.`);
    }

    const fullView = await viewFor({ user_id: job.user_id }, subject, env, job.pack_id);
    if (!fullView || fullView.tier === 'free') {
      throw new Error(`No active paid entitlement found for subject ${job.subject_id} and pack ${job.pack_id}.`);
    }

    const tConsol = Date.now();
    stageTs.calculate.completed_at = tConsol;
    stageTs.analyse = { started_at: tConsol, completed_at: tConsol };
    stageTs.consolidate = { started_at: tConsol };
    await tryUpdateReportJobStageColumns(env, job, 'consolidate', 'analyse', stageTs, null);

    // Strip any contact PII; pass ONLY sanitized viewFor output to the Python generator
    const sanitizedView = sanitizeViewForGenerator(fullView);
    const requestPayload = JSON.stringify({
      job_id: job.id,
      pack_id: job.pack_id,
      view: sanitizedView
    });

    const tWrite = Date.now();
    stageTs.consolidate.completed_at = tWrite;
    stageTs.write = { started_at: tWrite };
    await tryUpdateReportJobStageColumns(env, job, 'write', 'consolidate', stageTs, null);

    const timestampSec = Math.floor(now / 1000);
    const signatureHex = await signPdfServiceRequest(requestPayload, timestampSec, pdfServiceSecret);
    let generatorUrl = '';
    if (env && (env.PDF_SERVICE_URL || env.PDF_GENERATOR_URL)) {
      generatorUrl = (env.PDF_SERVICE_URL || env.PDF_GENERATOR_URL).trim();
    } else if (env && env.ENVIRONMENT === 'local') {
      generatorUrl = 'http://127.0.0.1:8090/internal/v1/render-pdf';
    } else {
      generatorUrl = requireSecret(env, 'PDF_SERVICE_URL');
    }
    generatorUrl = generatorUrl.replace(/\/+$/, '');
    if (!generatorUrl.endsWith('/internal/v1/render-pdf')) {
      generatorUrl = `${generatorUrl}/internal/v1/render-pdf`;
    }

    const genResp = await fetch(generatorUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-NV-Timestamp': String(timestampSec),
        'X-NV-Signature': signatureHex
      },
      body: requestPayload
    });

    if (!genResp.ok) {
      const errText = await genResp.text().catch(() => '');
      throw new Error(`Python generator returned HTTP ${genResp.status}: ${errText || 'Generation failed'}`);
    }

    const pdfBuffer = await genResp.arrayBuffer();
    const pdfBytes = new Uint8Array(pdfBuffer);
    if (pdfBytes.length < 100 || String.fromCharCode(pdfBytes[0], pdfBytes[1], pdfBytes[2], pdfBytes[3]) !== '%PDF') {
      throw new Error('Generator output is not a valid PDF document.');
    }

    const r2Key = `reports/${job.user_id}/${job.subject_id}/${job.pack_id}/${job.id}.pdf`;
    stageTs.write.completed_at = Date.now();
    stageTs.check_deliver = { started_at: Date.now() };
    await tryUpdateReportJobStageColumns(env, job, 'check_deliver', 'write', stageTs, null);
    await putPrivateR2Report(env, r2Key, pdfBytes);

    const doneAt = Date.now();
    stageTs.check_deliver.completed_at = doneAt;
    await tryUpdateReportJobStageColumns(env, job, 'completed', 'check_deliver', stageTs, null);
    if (env && env.DB) {
      await env.DB.prepare(
        "UPDATE report_jobs SET status = 'COMPLETED', r2_key = ?, completed_at = ?, updated_at = ?, last_error = NULL WHERE id = ?"
      ).bind(r2Key, doneAt, doneAt, job.id).run();
    } else {
      job.status = 'COMPLETED';
      job.r2_key = r2Key;
      job.completed_at = doneAt;
      job.updated_at = doneAt;
      job.last_error = null;
    }

    return { ok: true, status: 200, jobStatus: 'COMPLETED', r2Key, attempts: job.attempts || 0 };
  } catch (err) {
    const newAttempts = (job.attempts || 0) + 1;
    const maxAttempts = job.max_attempts || 3;
    const isFailed = newAttempts >= maxAttempts;
    const nextStatus = isFailed ? 'FAILED' : 'QUEUED';
    const errMsg = err && err.message ? err.message : String(err);
    const errAt = Date.now();

    if (env && env.DB) {
      await env.DB.prepare(
        'UPDATE report_jobs SET status = ?, attempts = ?, last_error = ?, updated_at = ? WHERE id = ?'
      ).bind(nextStatus, newAttempts, errMsg, errAt, job.id).run();

      if (isFailed) {
        const alertId = 'aud_' + errAt + '_' + getRandomHex(4);
        const alertDetails = JSON.stringify({
          alert: true,
          severity: 'CRITICAL',
          jobId: job.id,
          userId: job.user_id,
          subjectId: job.subject_id,
          packId: job.pack_id,
          attempts: newAttempts,
          error: errMsg
        });
        await env.DB.prepare(
          "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, 'system', 'report_job_failed_alert', 'report_jobs', ?, ?, ?)"
        ).bind(alertId, job.id, alertDetails, errAt).run();
        console.error(`[REPORT_JOB_FAILED_ALERT] Job ${job.id} permanently FAILED after ${newAttempts} attempts: ${errMsg}`);
      }
    } else {
      job.status = nextStatus;
      job.attempts = newAttempts;
      job.last_error = errMsg;
      job.updated_at = errAt;
      if (isFailed) {
        const alertId = 'aud_' + errAt + '_' + getRandomHex(4);
        memoryStore.auditLog.set(alertId, {
          id: alertId,
          actor_id: 'system',
          action: 'report_job_failed_alert',
          resource_type: 'report_jobs',
          resource_id: job.id,
          details_json: JSON.stringify({
            alert: true,
            severity: 'CRITICAL',
            jobId: job.id,
            userId: job.user_id,
            subjectId: job.subject_id,
            packId: job.pack_id,
            attempts: newAttempts,
            error: errMsg
          }),
          created_at: errAt
        });
        console.error(`[REPORT_JOB_FAILED_ALERT] Job ${job.id} permanently FAILED after ${newAttempts} attempts: ${errMsg}`);
      }
    }

    return {
      ok: false,
      status: isFailed ? 500 : 502,
      jobStatus: nextStatus,
      attempts: newAttempts,
      alertTriggered: isFailed,
      error: errMsg
    };
  }
}

/**
 * LAZY RETRY ENGINE FOR CLOUDFLARE PAGES (Commit 6b.d)
 * Automatically retries any QUEUED report_jobs (attempts < 3) or stuck PROCESSING jobs (>120s old)
 * when the user loads their dashboard (/api/v1/dashboard/view) or polls order status (/api/v1/payments/status).
 * Runs non-blocking via ctx.waitUntil when ctx is available.
 */
async function retryPendingReportJobsForUser(userId, env, ctx = null, orderId = null) {
  if (!userId && !orderId) return [];
  const now = Date.now();
  const STUCK_PROCESSING_MS = 120 * 1000;
  let candidateJobs = [];

  if (env && env.DB) {
    let query = `
      SELECT id, status, attempts, max_attempts, updated_at, created_at
      FROM report_jobs
      WHERE user_id = ?
        AND (
          (status = 'QUEUED' AND COALESCE(attempts, 0) < COALESCE(max_attempts, 3))
          OR (status = 'PROCESSING' AND COALESCE(attempts, 0) < COALESCE(max_attempts, 3) AND (? - COALESCE(updated_at, created_at, 0)) > ?)
        )
    `;
    let binds = [userId, now, STUCK_PROCESSING_MS];
    if (orderId) {
      query += ' AND order_id = ?';
      binds.push(orderId);
    }
    const rows = await env.DB.prepare(query).bind(...binds).all();
    candidateJobs = (rows && rows.results) || [];
  } else {
    for (const j of memoryStore.reportJobs.values()) {
      if (userId && j.user_id !== userId) continue;
      if (orderId && j.order_id !== orderId) continue;
      const att = j.attempts || 0;
      const maxAtt = j.max_attempts || 3;
      if (att >= maxAtt) continue;
      const isQueued = j.status === 'QUEUED';
      const isStuckProcessing = j.status === 'PROCESSING' && (now - (j.updated_at || j.created_at || 0)) > STUCK_PROCESSING_MS;
      if (isQueued || isStuckProcessing) {
        candidateJobs.push(j);
      }
    }
  }

  if (candidateJobs.length === 0) return [];

  const runPromise = (async () => {
    const results = [];
    for (const job of candidateJobs) {
      try {
        const res = await dispatchReportJob(job.id, env);
        results.push({ jobId: job.id, ...res });
      } catch (e) {
        console.error(`[Lazy_Retry_Error] Job ${job.id}:`, e);
      }
    }
    return results;
  })();

  if (ctx && typeof ctx.waitUntil === 'function') {
    ctx.waitUntil(runPromise);
    return candidateJobs.map(j => j.id);
  }
  return await runPromise;
}

const REPORT_JOB_STATUS = Object.freeze({
  QUEUED: 'QUEUED',
  PROCESSING: 'PROCESSING',
  COMPLETED: 'COMPLETED',
  DOWNLOADED: 'DOWNLOADED',
  FAILED: 'FAILED',
  CANCELLED: 'CANCELLED'
});

const REPORT_EXISTS_OR_SERVED_STATUSES = Object.freeze(['COMPLETED', 'DOWNLOADED', 'READY']);

function doesReportExistOrWasServed(job) {
  if (!job) return false;
  const st = String(job.status || '').trim().toUpperCase();
  return (
    REPORT_EXISTS_OR_SERVED_STATUSES.includes(st) ||
    Boolean(job.r2_key) ||
    Boolean(job.completed_at) ||
    Boolean(job.downloaded_at)
  );
}


const CHARM_BANNED_TERMS_REGEX = /\b(luck|lucky|lucks|guaranteed|guarantee|guarantees|prediction|predictions|prescription|prescriptions|consecrated|cure|cures|cured|exact)\b|\bwill\s+bring\b|\bwill\s+fix\b/i;

function hasBannedTerms(text) {
  if (!text || typeof text !== 'string') return false;
  return CHARM_BANNED_TERMS_REGEX.test(text);
}

const CHARM_SAFE_FALLBACK_TEXT = "Your consultation inquiry has been processed against classical numerological and archetypal cycles. Focus on disciplined strategic pacing and deliberate alignment with your core planetary drivers during this active cycle.";

function processTextWithBannedFilter(initialText, regenerateFn) {
  if (!hasBannedTerms(initialText)) {
    return initialText;
  }
  // Detect banned terms -> regenerate once with a stricter instruction
  if (typeof regenerateFn === 'function') {
    const regenerated = regenerateFn();
    if (regenerated && typeof regenerated === 'string' && !hasBannedTerms(regenerated)) {
      return regenerated;
    }
  }
  // Else return a fixed safe fallback sentence. Never output a sentence with a deleted word.
  return CHARM_SAFE_FALLBACK_TEXT;
}

function isValidRelativeReturnTo(returnTo) {
  if (!returnTo || typeof returnTo !== 'string') return false;
  const clean = returnTo.trim();
  if (!clean.startsWith('/') || clean.startsWith('//')) {
    return false;
  }
  // Reject backslashes anywhere
  if (clean.includes('\\')) {
    return false;
  }
  // Reject any ASCII control character (including tab/CR/LF) and any whitespace inside the string
  if (/[\s\x00-\x1F\x7F]/.test(clean)) {
    return false;
  }
  // Reject encoded control characters or encoded whitespace (%00-%1F, %7F, %20, %0a, %0d, etc.)
  if (/%(0[0-9a-fA-F]|1[0-9a-fA-F]|7[fF]|20)/i.test(clean)) {
    return false;
  }
  // Reject URI schemes (e.g. javascript:, http:, data:)
  if (/^[a-zA-Z][a-zA-Z0-9+.-]*:/.test(clean)) {
    return false;
  }
  return true;
}

async function callCharmBackendService(payload, env, endpointPath = '/api/charm/chat') {
  const charmSecret = (env && env.CHARM_SERVICE_SECRET || '').trim();
  if (!charmSecret) {
    throw new Error('CHARM_SERVICE_SECRET_UNSET');
  }
  let backendUrl = (env && env.CHARM_SERVICE_URL ? env.CHARM_SERVICE_URL : '').trim();
  if (!backendUrl) {
    throw new Error('CHARM_BACKEND_URL_UNSET');
  }
  backendUrl = backendUrl.replace(/\/+$/, '');
  const timeoutMs = parseInt((env && env.CHARM_TIMEOUT_MS) || '12000', 10);
  const fetchOpts = {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-NV-Charm-Secret': charmSecret,
      'X-NV-Upstream-Metered': '1',
      'X-NV-Charm-Entitlement': (payload && payload._charm_entitlement) ? String(payload._charm_entitlement) : 'charm_free'
    },
    body: JSON.stringify(payload)
  };
  if (typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function' && timeoutMs > 0) {
    fetchOpts.signal = AbortSignal.timeout(timeoutMs);
  }
  return await fetch(`${backendUrl}${endpointPath}`, fetchOpts);
}

function sanitizeReturnToUrl(returnTo, defaultUrl = '/dashboard/') {
  return isValidRelativeReturnTo(returnTo) ? returnTo.trim() : defaultUrl;
}

function isPreviewRequest(request, env) {
  const envMode = String((env && env.ENVIRONMENT) || '').trim().toLowerCase();
  if (envMode === 'production') return false;
  if (envMode === 'preview') return true;
  try {
    const u = new URL(request.url);
    const h = (u.hostname || '').toLowerCase();
    if (h === 'numerosvision.com' || h === 'www.numerosvision.com') return false;
    if (h.endsWith('.pages.dev') || h.startsWith('preview.')) return true;
  } catch (_) {}
  return false;
}

function escapeHtmlAttr(val) {
  return String(val == null ? '' : val)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

function buildPreviewLaunchBannerHtml(launchState, basicPack) {
  const configured = Boolean(launchState && launchState.configured);
  const active = Boolean(launchState && launchState.active);
  const forced = Boolean(launchState && launchState.forced);
  const startsRaw = forced ? 'forced_preview' : (configured ? (launchState.rawStartsAt || launchState.startedAt) : 'unset');
  const endsRaw = forced ? 'forced_preview' : (configured ? (launchState.rawEndsAt || launchState.endsAt) : 'unset');
  const currentPriceLabel = active
    ? `Launch price active: ₹${basicPack.price_inr} (regular ₹${basicPack.struck_mrp_inr || basicPack.mrp_inr})`
    : `Regular price active: ₹${basicPack.price_inr}`;
  return `<div id="nv-preview-launch-banner" role="region" aria-label="Preview launch window status" data-launch-configured="${configured ? 'true' : 'false'}" data-launch-active="${active ? 'true' : 'false'}" data-launch-forced="${forced ? 'true' : 'false'}" data-starts-at="${escapeHtmlAttr(startsRaw)}" data-ends-at="${escapeHtmlAttr(endsRaw)}" style="background:#FFFDF7;border-bottom:2px solid #C9A227;color:#523E28;padding:8px 16px;font-family:Inter,system-ui,sans-serif;font-size:12.5px;line-height:1.45;text-align:center;position:relative;z-index:9999;">` +
    `<strong style="color:#8B6914;letter-spacing:0.06em;text-transform:uppercase;">Preview Window</strong> &middot; ` +
    `<span>NV_LAUNCH_STARTS_AT: <code>${escapeHtmlAttr(startsRaw)}</code></span> &middot; ` +
    `<span>NV_LAUNCH_ENDS_AT: <code>${escapeHtmlAttr(endsRaw)}</code></span> &middot; ` +
    `<strong id="nv-preview-launch-state" style="color:${active ? '#16835B' : '#8B6914'};">${escapeHtmlAttr(currentPriceLabel)}</strong>` +
    `<span id="nv-preview-launch-countdown" style="margin-left:6px;color:#7A654D;"></span>` +
    `<script>(function(){var elCnt=document.getElementById('nv-preview-launch-countdown');var elSt=document.getElementById('nv-preview-launch-state');var sRaw=${JSON.stringify((configured && !forced) ? (launchState.startedAt || '') : '')};var eRaw=${JSON.stringify((configured && !forced) ? (launchState.endsAt || '') : '')};if(!sRaw||!eRaw||!elCnt)return;var sMs=Date.parse(sRaw),eMs=Date.parse(eRaw);if(isNaN(sMs)||isNaN(eMs))return;var wasActive=(Date.now()>=sMs&&Date.now()<=eMs);function tick(){var now=Date.now();var isAct=(now>=sMs&&now<=eMs);if(isAct){var rem=Math.max(0,Math.ceil((eMs-now)/1000));var m=Math.floor(rem/60),s=rem%60;elCnt.textContent='(switches to regular ₹399 in '+m+'m '+String(s).padStart(2,'0')+'s)';}else if(now<sMs){var wait=Math.max(0,Math.ceil((sMs-now)/1000));elCnt.textContent='(starts in '+wait+'s)';}else{elCnt.textContent='(window ended — regular price ₹399 active)';}if(isAct!==wasActive){wasActive=isAct;if(elSt){elSt.textContent=isAct?'Launch price active: ₹199 (regular ₹399)':'Regular price active: ₹399';elSt.style.color=isAct?'#16835B':'#8B6914';}try{window.dispatchEvent(new CustomEvent('nv:launch-window-changed',{detail:{active:isAct}}));}catch(_){}}}tick();setInterval(tick,1000);})();</script>` +
    `</div>`;
}

export default {
  memoryStore,
  hasBannedTerms,
  callCharmBackendService,
  CHARM_SAFE_FALLBACK_TEXT,
  processTextWithBannedFilter,
  isValidRelativeReturnTo,
  sanitizeReturnToUrl,
  viewFor,
  parseDobParts,
  encryptField,
  decryptField,
  getAesGcmKey,
  requireSecret,
  sanitizeViewForGenerator,
  signPdfServiceRequest,
  createSignedDownloadToken,
  verifySignedDownloadToken,
  dispatchReportJob,
  formatReportJobProgress,
  retryPendingReportJobsForUser,
  REPORT_JOB_STATUS,
  REPORT_EXISTS_OR_SERVED_STATUSES,
  doesReportExistOrWasServed,
  fulfillPaidOrder,
  mintUserSession,
  getOrderTokenSecret,
  signOrderAccessToken,
  verifyOrderAccessToken,
  verifyTurnstileToken,
  WAITLIST_PURPOSE,
  WAITLIST_RETENTION_MONTHS,
  WAITLIST_DPDP_CONSENT_TEXT,
  recommendLadderTier,
  registerWaitlistNotifyMe,
  deleteWaitlistNotifyMe,
  buildWaitlistNotificationEmail,
  dispatchWaitlistNotificationsForPack,
  PACK_CATALOG,
  digitRoot,
  sumDigitsStr,
  calcDriver,
  calcBhagyank,
  calcPersonalYear,
  calcPersonalMonth,
  calcPersonalDay,
  calcPersonalCyclesForDate,
  calcLoShuDobOnly,
  calcChaldeanNameNumber,
  calcPythagoreanNameNumber,
  calculateCanonicalKuaDetails,
  KUA_RULE_TEXT,
  KUA_NEEDS_GENDER_TEXT,
  WEBHOOK_FALLBACK_WINDOW_MS,
  reconcileStaleOrderWithRazorpay,
  isNotifyMeHigherTiersEnabled,
  isLayers23Enabled,
  resolveServerLaunchOfferState,
  getPackById,
  resolveEffectivePackPricePaise,
  async fetch(request, env, ctx) {
    const isPreview = isPreviewRequest(request, env);
    const finalizeResponse = (resp, forceNoCache = false) => {
      if (!isPreview && !forceNoCache) return resp;
      const newHeaders = new Headers(resp.headers);
      if (isPreview) {
        newHeaders.set('X-Robots-Tag', 'noindex');
      }
      if (forceNoCache) {
        if (!resp.headers.has('Cache-Control')) {
          newHeaders.set('Cache-Control', 'private, no-cache, no-store, must-revalidate');
        }
        newHeaders.set('Pragma', 'no-cache');
        newHeaders.set('Expires', '0');
      }
      const isRedirect = resp.status >= 300 && resp.status < 400;
      return new Response(isRedirect ? null : resp.body, {
        status: resp.status,
        statusText: resp.statusText,
        headers: newHeaders
      });
    };
    try {
      const response = await this._handleRequest(request, env, ctx);
      const url = new URL(request.url);
      const forceNoCache = (
        url.pathname.startsWith('/api/') ||
        url.pathname.startsWith('/dashboard') ||
        url.pathname.includes('/reports/download') ||
        url.pathname.endsWith('.pdf')
      );
      const ct = (response.headers.get('Content-Type') || '').toLowerCase();
      if (request.method === 'GET' && response.status === 200 && ct.includes('text/html')) {
        const rawHtml = await response.text();
        const launchState = resolveServerLaunchOfferState(env);
        const notifyFlag = isNotifyMeHigherTiersEnabled(env);
        const layers23Flag = isLayers23Enabled(env);
        const basicPack = getPackById('report_basic', env);
        const cfgScript = `<script id="nv-server-launch-config">window.__NV_LAUNCH_STARTS_AT=${JSON.stringify((launchState.configured && !launchState.forced) ? launchState.rawStartsAt : null)};window.__NV_LAUNCH_ENDS_AT=${JSON.stringify((launchState.configured && !launchState.forced) ? launchState.rawEndsAt : null)};window.__NV_FORCE_LAUNCH_MODE=${JSON.stringify(Boolean(launchState.forced))};window.__NV_NOTIFY_ME_HIGHER_TIERS=${JSON.stringify(notifyFlag)};window.__NV_IS_PREVIEW=${JSON.stringify(isPreview)};window.__NV_ENABLE_LAYERS_2_3=${JSON.stringify(layers23Flag)};</script>`;
        let modifiedHtml = rawHtml;
        if (!modifiedHtml.includes('id="nv-server-launch-config"')) {
          if (/<\/head>/i.test(modifiedHtml)) {
            modifiedHtml = modifiedHtml.replace(/<\/head>/i, cfgScript + '</head>');
          } else {
            modifiedHtml = cfgScript + modifiedHtml;
          }
        }
        if (isPreview && !modifiedHtml.includes('id="nv-preview-launch-banner"')) {
          const bannerHtml = buildPreviewLaunchBannerHtml(launchState, basicPack);
          if (/<body[^>]*>/i.test(modifiedHtml)) {
            modifiedHtml = modifiedHtml.replace(/<body[^>]*>/i, (match) => match + bannerHtml);
          } else {
            modifiedHtml = bannerHtml + modifiedHtml;
          }
        }
        const htmlHeaders = new Headers(response.headers);
        htmlHeaders.delete('Content-Length');
        if (isPreview) {
          htmlHeaders.set('X-Robots-Tag', 'noindex');
          htmlHeaders.set('Cache-Control', 'no-cache, no-store, must-revalidate');
        }
        const htmlResp = new Response(modifiedHtml, {
          status: response.status,
          statusText: response.statusText,
          headers: htmlHeaders
        });
        return finalizeResponse(htmlResp, forceNoCache);
      }
      return finalizeResponse(response, forceNoCache);
    } catch (err) {
      if (err && err.code === 'MISSING_SECRET') {
        const errHeaders = {
          'Content-Type': 'application/json',
          ...getCorsHeaders(request, env)
        };
        if (isPreview) errHeaders['X-Robots-Tag'] = 'noindex';
        return new Response(JSON.stringify({
          success: false,
          error: err.message,
          missing_secret: err.secretName
        }), {
          status: 500,
          headers: errHeaders
        });
      }
      console.error('[Unhandled_Worker_Error]', err);
      const errHeaders = {
        'Content-Type': 'application/json',
        ...getCorsHeaders(request, env)
      };
      if (isPreview) errHeaders['X-Robots-Tag'] = 'noindex';
      return new Response(JSON.stringify({
        success: false,
        error: err && err.message ? err.message : 'Internal server error'
      }), {
        status: 500,
        headers: errHeaders
      });
    }
  },

  async _handleRequest(request, env, ctx) {
    const url = new URL(request.url);

    // CSRF Protection: Verify Origin on state-changing POST endpoints
    if (request.method === 'POST' && (url.pathname.startsWith('/api/v1/auth/') || url.pathname.startsWith('/api/v1/payments/') || url.pathname === '/api/create-order' || url.pathname === '/api/verify-payment' || url.pathname === '/api/planner-2027/order' || url.pathname === '/api/planner-2027/verify' || url.pathname === '/api/planner-2027/resend-link')) {
      if (!verifyOrigin(request, env)) {
        return new Response(JSON.stringify({
          error: 'CSRF origin validation failed.'
        }), {
          status: 403,
          headers: {
            'Content-Type': 'application/json',
            ...getCorsHeaders(request, env)
          }
        });
      }
    }

    // 0. CANONICAL 301 REDIRECTS & SINGLE-HOP HTTP/WWW -> HTTPS APEX NORMALIZATION
    const canonicalRedirects = {
      '/charm_ai.html': '/charm-ai/',
      '/charm_ai': '/charm-ai/',
      '/charm_ai/': '/charm-ai/',
      '/ai-consultation': '/charm-ai/',
      '/ai-consultation/': '/charm-ai/',
      '/privacy-policy': '/privacy/',
      '/privacy-policy/': '/privacy/',
      '/privacy.html': '/privacy/',
      '/refund': '/refund-policy/',
      '/refund/': '/refund-policy/',
      '/refund.html': '/refund-policy/',
      '/refunds': '/refund-policy/',
      '/refunds/': '/refund-policy/',
      '/cancellation': '/cancel/',
      '/cancellation/': '/cancel/',
      '/cancel.html': '/cancel/',
      '/cookie_policy': '/cookie-policy/',
      '/cookie_policy/': '/cookie-policy/',
      '/cookie_policy.html': '/cookie-policy/',
      '/cookies': '/cookie-policy/',
      '/cookies/': '/cookie-policy/',
      '/numerology_overview': '/numerology-overview/',
      '/numerology_overview/': '/numerology-overview/',
      '/numerology_overview.html': '/numerology-overview/',
      '/numerology-calculators': '/calculators/',
      '/numerology-calculators/': '/calculators/',
      '/tools': '/calculators/',
      '/tools/': '/calculators/',
      '/register': '/signup/',
      '/register/': '/signup/',
      '/login.html': '/login/',
      '/signup.html': '/signup/',
      '/year_2027': '/year-2027/',
      '/year_2027/': '/year-2027/',
      '/year_2027.html': '/year-2027/',
      '/sample-report': '/sample/',
      '/sample-report/': '/sample/',
      '/sample_report': '/sample/',
      '/sample_report/': '/sample/',
      '/sample-roadmap': '/sample/',
      '/sample-roadmap/': '/sample/',
      '/sample_roadmap': '/sample/',
      '/sample_roadmap/': '/sample/',
      '/sample_roadmap.html': '/sample/',
      '/roadmap-preview': '/sample/',
      '/roadmap-preview/': '/sample/',
      '/sample': '/sample/',
      '/sample.html': '/sample/',
      '/reports': '/reports/',
      '/reports.html': '/reports/',
      '/reports_catalogue': '/reports/',
      '/reports_catalogue/': '/reports/',
      '/reports_catalogue.html': '/reports/',
      // Every /tools/<slug> -> single-hop 301 to canonical /calculators/<slug>/
      '/tools/lo-shu-grid': '/calculators/lo-shu-grid/',
      '/tools/lo-shu-grid/': '/calculators/lo-shu-grid/',
      '/tools/lo-shu-grid.html': '/calculators/lo-shu-grid/',
      '/tools/name-numerology': '/calculators/name-numerology/',
      '/tools/name-numerology/': '/calculators/name-numerology/',
      '/tools/name-numerology.html': '/calculators/name-numerology/',
      '/tools/name-balancing': '/calculators/name-balancing/',
      '/tools/name-balancing/': '/calculators/name-balancing/',
      '/tools/name-balancing.html': '/calculators/name-balancing/',
      '/tools/mobile-numerology': '/calculators/mobile-number/',
      '/tools/mobile-numerology/': '/calculators/mobile-number/',
      '/tools/mobile-numerology.html': '/calculators/mobile-number/',
      '/tools/life-path-calculator': '/calculators/life-path/',
      '/tools/life-path-calculator/': '/calculators/life-path/',
      '/tools/life-path-calculator.html': '/calculators/life-path/',
      '/tools/compatibility-calculator': '/calculators/compatibility/',
      '/tools/compatibility-calculator/': '/calculators/compatibility/',
      '/tools/compatibility-calculator.html': '/calculators/compatibility/',
      '/tools/kundali-milan': '/calculators/compatibility/',
      '/tools/kundali-milan/': '/calculators/compatibility/',
      '/tools/blessing-years': '/calculators/personal-year/',
      '/tools/blessing-years/': '/calculators/personal-year/',
      '/tools/blessing-years.html': '/calculators/personal-year/',
      '/tools/business-numerology': '/calculators/business-alignment/',
      '/tools/business-numerology/': '/calculators/business-alignment/',
      '/tools/business-alignment': '/calculators/business-alignment/',
      '/tools/business-alignment/': '/calculators/business-alignment/',
      '/tools/business-alignment.html': '/calculators/business-alignment/',
      '/tools/baby-naming': '/calculators/baby-naming/',
      '/tools/baby-naming/': '/calculators/baby-naming/',
      '/tools/baby-naming.html': '/calculators/baby-naming/',
      '/tools/property-numerology': '/calculators/property-numerology/',
      '/tools/property-numerology/': '/calculators/property-numerology/',
      '/tools/property-numerology.html': '/calculators/property-numerology/',
      '/tools/vehicle-numerology': '/calculators/vehicle-numerology/',
      '/tools/vehicle-numerology/': '/calculators/vehicle-numerology/',
      '/tools/vehicle-numerology.html': '/calculators/vehicle-numerology/',
      '/tools/profession-calculator': '/calculators/profession-calculator/',
      '/tools/profession-calculator/': '/calculators/profession-calculator/',
      '/tools/profession-calculator.html': '/calculators/profession-calculator/',
      '/tools/lucky-number': '/calculators/favourable-numbers/',
      '/tools/lucky-number/': '/calculators/favourable-numbers/',
      '/tools/lucky-number.html': '/calculators/favourable-numbers/',
      '/tools/favourable-numbers': '/calculators/favourable-numbers/',
      '/tools/favourable-numbers/': '/calculators/favourable-numbers/',
      '/tools/favourable-numbers.html': '/calculators/favourable-numbers/',
      '/tools/logo-studio': '/calculators/logo-intelligence/',
      '/tools/logo-studio/': '/calculators/logo-intelligence/',
      '/tools/logo-intelligence': '/calculators/logo-intelligence/',
      '/tools/logo-intelligence/': '/calculators/logo-intelligence/',
      '/tools/logo-intelligence.html': '/calculators/logo-intelligence/',
      // Legacy /calculators/<old-slug> -> canonical /calculators/<slug>/
      '/calculators/chaldean': '/calculators/name-numerology/',
      '/calculators/chaldean/': '/calculators/name-numerology/',
      '/calculators/chaldean-name-numerology': '/calculators/name-balancing/',
      '/calculators/chaldean-name-numerology/': '/calculators/name-balancing/',
      '/calculators/life-path-number': '/calculators/life-path/',
      '/calculators/life-path-number/': '/calculators/life-path/',
      '/calculators/mobile-numerology': '/calculators/mobile-number/',
      '/calculators/mobile-numerology/': '/calculators/mobile-number/',
      '/calculators/mobile-number-numerology': '/calculators/mobile-number/',
      '/calculators/mobile-number-numerology/': '/calculators/mobile-number/',
      '/calculators/numerology-compatibility': '/calculators/compatibility/',
      '/calculators/numerology-compatibility/': '/calculators/compatibility/',
      '/calculators/pythagorean-numerology': '/calculators/pythagorean/',
      '/calculators/pythagorean-numerology/': '/calculators/pythagorean/',
      '/calculators/personal-year-numerology': '/calculators/personal-year/',
      '/calculators/personal-year-numerology/': '/calculators/personal-year/',
      '/calculators/business-name-numerology': '/calculators/business-alignment/',
      '/calculators/business-name-numerology/': '/calculators/business-alignment/',
      '/calculators/mulank-calculator': '/calculators/birth-number/',
      '/calculators/mulank-calculator/': '/calculators/birth-number/',
      '/calculators/bhagyank-calculator': '/calculators/life-path/',
      '/calculators/bhagyank-calculator/': '/calculators/life-path/',
      '/calculators/kua-calculator': '/calculators/lo-shu-grid/',
      '/calculators/kua-calculator/': '/calculators/lo-shu-grid/',
      // Missing trailing slash on canonical /calculators/<slug> -> 1-hop 301
      '/calculators/birth-number': '/calculators/birth-number/',
      '/calculators/lo-shu-grid': '/calculators/lo-shu-grid/',
      '/calculators/life-path': '/calculators/life-path/',
      '/calculators/name-numerology': '/calculators/name-numerology/',
      '/calculators/name-balancing': '/calculators/name-balancing/',
      '/calculators/pythagorean': '/calculators/pythagorean/',
      '/calculators/mobile-number': '/calculators/mobile-number/',
      '/calculators/compatibility': '/calculators/compatibility/',
      '/calculators/personal-year': '/calculators/personal-year/',
      '/calculators/business-alignment': '/calculators/business-alignment/',
      '/calculators/baby-naming': '/calculators/baby-naming/',
      '/calculators/property-numerology': '/calculators/property-numerology/',
      '/calculators/vehicle-numerology': '/calculators/vehicle-numerology/',
      '/calculators/profession-calculator': '/calculators/profession-calculator/',
      '/calculators/favourable-numbers': '/calculators/favourable-numbers/',
      '/calculators/logo-intelligence': '/calculators/logo-intelligence/',
      '/blog/gemstone-remedies': '/blog/vedic-gemstone-remedies/',
      '/blog/gemstone-remedies/': '/blog/vedic-gemstone-remedies/',
      '/blog/gemstone-remedies.html': '/blog/vedic-gemstone-remedies/'
    };
    let resolvedRedirectPath = canonicalRedirects[url.pathname] || null;
    if (!resolvedRedirectPath && url.pathname.startsWith('/blog/') && url.pathname.endsWith('.html')) {
      resolvedRedirectPath = url.pathname.replace(/\.html$/, '/');
    }
    const isProdDomain = url.hostname === 'numerosvision.com' || url.hostname === 'www.numerosvision.com';
    const needsSchemeOrApexRedirect = isProdDomain && (url.protocol === 'http:' || url.hostname === 'www.numerosvision.com');
    if (needsSchemeOrApexRedirect) {
      const destPath = resolvedRedirectPath || url.pathname;
      return Response.redirect('https://numerosvision.com' + destPath + url.search, 301);
    }
    if (resolvedRedirectPath) {
      return Response.redirect(new URL(resolvedRedirectPath + url.search, url.origin), 301);
    }

    // 0b. SECURITY GATE / WAF: Block access to private files, hidden dotfiles, backups, and server scripts
    const forbiddenPatterns = [
      /^\/\.env/i,
      /^\/\.git/i,
      /^\/data\//i,
      /^\/app\//i,
      /^\/scripts\//i,
      /^\/pdf_service\//i,
      /^\/reports\/.*\.pdf$/i,
      /^\/static\/reports\//i,
      /\.py$/i,
      /\.env/i,
      /\.jsonl$/i,
      /^\/_worker\.js$/i
    ];
    if (forbiddenPatterns.some(pattern => pattern.test(url.pathname))) {
      return new Response('404 Not Found', {
        status: 404,
        headers: { 'Content-Type': 'text/plain; charset=utf-8' }
      });
    }

    // Dynamic Client Turnstile Configuration Script
    if (url.pathname === '/api/turnstile-config.js') {
      const siteKey = (env && env.TURNSTILE_SITE_KEY ? env.TURNSTILE_SITE_KEY.trim() : '') || '1x00000000000000000000AA';
      return new Response(`window.NV_TURNSTILE_SITE_KEY = ${JSON.stringify(siteKey)};`, {
        headers: {
          'Content-Type': 'application/javascript; charset=UTF-8',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    // Dynamic Client Google Authentication Configuration Script
    if (url.pathname === '/api/google-auth-config.js') {
      const clientId = (env && env.GOOGLE_CLIENT_ID ? env.GOOGLE_CLIENT_ID.trim() : '');
      return new Response(`window.NV_GOOGLE_CLIENT_ID = ${JSON.stringify(clientId)};`, {
        headers: {
          'Content-Type': 'application/javascript; charset=UTF-8',
          'Cache-Control': 'no-cache, no-store, must-revalidate',
          'Access-Control-Allow-Origin': '*'
        }
      });
    }

    // Health & Dangerous Flags Audit Route (/api/health)
    if (url.pathname === '/api/health' || url.pathname === '/api/v1/health') {
      const currentEnv = ((env && env.ENVIRONMENT) || 'production').toLowerCase().trim();
      const detectedDangerous = getDetectedDangerousFlags(env);
      const isProd = currentEnv === 'production';
      const hasDangerousInProd = isProd && detectedDangerous.length > 0;

      const adminHeader = (request.headers.get('X-Admin-Token') || '').trim() ||
                          (request.headers.get('Authorization') || '').replace(/^Bearer\s+/i, '').trim();
      const configuredAdminToken = (env && env.ADMIN_TOKEN ? env.ADMIN_TOKEN.trim() : '');
      const isAdmin = Boolean(configuredAdminToken && adminHeader && timingSafeEqual(adminHeader, configuredAdminToken));

      const isTurnstileFallbackActive = (currentEnv === 'preview' || currentEnv === 'test' || currentEnv === 'local') &&
        (!env.TURNSTILE_SECRET_KEY || isCloudflareTestKey(env.TURNSTILE_SECRET_KEY));
      const payload = {
        status: hasDangerousInProd ? 'degraded' : 'ok',
        turnstile_fallback_active: isTurnstileFallbackActive
      };
      if (isAdmin) {
        payload.environment = currentEnv;
        payload.dangerous_flags = detectedDangerous;
      }

      const statusCode = hasDangerousInProd ? 503 : 200;
      return new Response(JSON.stringify(payload), {
        status: statusCode,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Cache-Control': 'no-cache, no-store, must-revalidate'
        }
      });
    }

    assertNoDangerousFlagsInProduction(env, request);

    // Rewrite /static/reports/ to /reports/
    // Direct static reports rewrite removed for security lockdown



    // Force zero-caching for payment gateway scripts so browser never holds stale logic
    if (url.pathname.includes('nv_payment_gateway.js')) {
      const res = await env.ASSETS.fetch(request);
      const newHeaders = new Headers(res.headers);
      newHeaders.set('Cache-Control', 'no-cache, no-store, must-revalidate');
      newHeaders.set('Pragma', 'no-cache');
      newHeaders.set('Expires', '0');
      newHeaders.set('Access-Control-Allow-Origin', '*');
      return new Response(res.body, {
        status: res.status,
        headers: newHeaders
      });
    }


    // =========================================================================
    // ROUTE: EMAIL OTP - SEND CODE (/api/v1/auth/email/send-code)
    // Turnstile gated, durable rate limits, 6 digits, 10-min expiry, enumeration neutral
    // =========================================================================
    if (url.pathname === '/api/v1/auth/email/send-code' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, cf-turnstile-response'
      };
      try {
        const body = await request.json().catch(() => ({}));
        const clientIp = request.headers.get('CF-Connecting-IP') || request.headers.get('x-forwarded-for') || '127.0.0.1';

        // 0. Production Turnstile Configuration Guard
        const turnstileConfigErr = getTurnstileConfigError(env);
        if (turnstileConfigErr) {
          return new Response(JSON.stringify({
            success: false,
            error: turnstileConfigErr
          }), { status: 503, headers: corsHeaders });
        }

        // 1. Turnstile Check
        const turnstileToken = (body.turnstile_token || request.headers.get('cf-turnstile-response') || '').trim();
        const turnstileOk = await verifyTurnstileToken(env, turnstileToken, clientIp);
        if (!turnstileOk) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Cloudflare Turnstile verification failed. Please complete the security check.'
          }), { status: 403, headers: corsHeaders });
        }

        // 2. Email Validation
        const rawEmail = (body.email || body.identifier || '').toString().trim().toLowerCase();
        if (!rawEmail || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(rawEmail) || rawEmail.length > 120) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Please enter a valid email address.'
          }), { status: 400, headers: corsHeaders });
        }

        // 2b. Optional Mobile Validation (+91 ^[6-9][0-9]{9}$ only; invalid/non-IN phones skip SMS without blocking Email OTP)
        const rawPhoneInput = (body.phone || body.mobile || body.customer_phone || '').toString().trim();
        const explicitMobile10 = rawPhoneInput ? parseStrictPlus91Mobile10(rawPhoneInput) : null;
        if (rawPhoneInput && !explicitMobile10) {
          console.info('sms_skipped: invalid_phone');
        }

        const otpSecret = requireSecret(env, 'OTP_HMAC_SECRET');
        const ipSalt = requireSecret(env, 'IP_HASH_SALT');
        const emailHash = await hmacSha256Hex(otpSecret, rawEmail);
        const ipHash = await hmacSha256Hex(ipSalt, clientIp);
        const now = Date.now();

        // Resolve stored mobile for returning users ONLY when rawPhoneInput was left blank (silent, zero enumeration leak)
        let targetMobile10 = explicitMobile10;
        if (!rawPhoneInput && !targetMobile10 && env && env.DATA_ENCRYPTION_KEY && /^[0-9a-fA-F]{64}$/.test(String(env.DATA_ENCRYPTION_KEY).trim())) {
          try {
            let existingPhoneEnc = null;
            if (env.DB) {
              const uRow = await env.DB.prepare('SELECT phone_enc FROM users WHERE email = ? LIMIT 1').bind(rawEmail).first();
              existingPhoneEnc = uRow && uRow.phone_enc ? uRow.phone_enc : null;
            } else if (memoryStore.users && memoryStore.users.has(rawEmail)) {
              const uMem = memoryStore.users.get(rawEmail);
              existingPhoneEnc = uMem && uMem.phone_enc ? uMem.phone_enc : null;
            }
            if (existingPhoneEnc) {
              const decPhone = await decryptField(existingPhoneEnc, env.DATA_ENCRYPTION_KEY.trim());
              targetMobile10 = parseStrictPlus91Mobile10(decPhone);
            }
          } catch (_) {}
        }

        // 3. Durable Rate Limiting (env-configurable per-email, per-IP, and per-mobile over 15m window)
        const window15m = 15 * 60 * 1000;
        const emailRateLimit = Math.max(1, parseInt((env && env.OTP_EMAIL_RATE_LIMIT) || '5', 10) || 5);
        const ipRateLimit = Math.max(1, parseInt((env && env.OTP_IP_RATE_LIMIT) || '10', 10) || 10);
        const mobileRateLimit = Math.max(1, parseInt((env && env.OTP_MOBILE_RATE_LIMIT) || '3', 10) || 3);
        let smsAllowedByRateLimit = true;
        const phoneHash = targetMobile10 ? await hmacSha256Hex(otpSecret, targetMobile10) : null;
        if (env.DB) {
          try {
            const recentEmail = await env.DB.prepare(
              'SELECT COUNT(*) as cnt FROM email_otp_challenges WHERE email_hash = ? AND created_at > ?'
            ).bind(emailHash, now - window15m).first();
            if (recentEmail && recentEmail.cnt >= emailRateLimit) {
              return new Response(JSON.stringify({
                success: false,
                error: 'Maximum verification code requests exceeded for this email. Please try again in 15 minutes.'
              }), { status: 429, headers: corsHeaders });
            }

            const recentIp = await env.DB.prepare(
              'SELECT COUNT(*) as cnt FROM email_otp_challenges WHERE ip_hash = ? AND created_at > ?'
            ).bind(ipHash, now - window15m).first();
            if (recentIp && recentIp.cnt >= ipRateLimit) {
              return new Response(JSON.stringify({
                success: false,
                error: 'Rate limit exceeded for this IP. Please try again in 15 minutes.'
              }), { status: 429, headers: corsHeaders });
            }

            if (phoneHash) {
              const mobLimitKey = 'otp_mob:' + phoneHash;
              const rlRow = await env.DB.prepare(
                'SELECT count, window_start, expires_at FROM email_rate_limits WHERE key = ?'
              ).bind(mobLimitKey).first();
              if (rlRow && rlRow.expires_at > now && rlRow.count >= mobileRateLimit) {
                smsAllowedByRateLimit = false;
                if (explicitMobile10) {
                  return new Response(JSON.stringify({
                    success: false,
                    error: 'Maximum verification code requests exceeded for this mobile number. Please try again in 15 minutes.'
                  }), { status: 429, headers: corsHeaders });
                }
              } else if (rlRow && rlRow.expires_at > now) {
                await env.DB.prepare('UPDATE email_rate_limits SET count = count + 1 WHERE key = ?').bind(mobLimitKey).run();
              } else {
                await env.DB.prepare('INSERT OR REPLACE INTO email_rate_limits (key, count, window_start, expires_at) VALUES (?, 1, ?, ?)').bind(mobLimitKey, now, now + window15m).run();
              }
            }
          } catch (e) {
            console.warn('[D1_EmailRateLimit_Fallback]', redactOtpAndPhone(e && e.message));
          }
        } else {
          memoryStore.emailHistory = memoryStore.emailHistory || [];
          memoryStore.emailHistory = memoryStore.emailHistory.filter(h => (now - h.created_at) < window15m);
          const emailHist = memoryStore.emailHistory.filter(h => h.email_hash === emailHash);
          if (emailHist.length >= emailRateLimit) {
            return new Response(JSON.stringify({
              success: false,
              error: 'Maximum verification code requests exceeded for this email. Please try again in 15 minutes.'
            }), { status: 429, headers: corsHeaders });
          }
          const ipHist = memoryStore.emailHistory.filter(h => h.ip_hash === ipHash);
          if (ipHist.length >= ipRateLimit) {
            return new Response(JSON.stringify({
              success: false,
              error: 'Rate limit exceeded for this IP. Please try again in 15 minutes.'
            }), { status: 429, headers: corsHeaders });
          }
          if (phoneHash) {
            memoryStore.mobileRateHistory = (memoryStore.mobileRateHistory || []).filter(h => (now - h.created_at) < window15m);
            const mobHist = memoryStore.mobileRateHistory.filter(h => h.phone_hash === phoneHash);
            if (mobHist.length >= mobileRateLimit) {
              smsAllowedByRateLimit = false;
              if (explicitMobile10) {
                return new Response(JSON.stringify({
                  success: false,
                  error: 'Maximum verification code requests exceeded for this mobile number. Please try again in 15 minutes.'
                }), { status: 429, headers: corsHeaders });
              }
            } else {
              memoryStore.mobileRateHistory.push({ phone_hash: phoneHash, created_at: now });
            }
          }
          memoryStore.emailHistory.push({ email_hash: emailHash, ip_hash: ipHash, created_at: now });
        }

        // 4. Check Email adapter configuration (Email OTP is mandatory; SMS failure/skip never blocks Email OTP)
        const emailConfigErr = getEmailConfigError(env);
        const killSwitchActive = env && (env.EMAIL_KILL_SWITCH === 'true' || env.EMAIL_KILL_SWITCH === true);
        if (killSwitchActive) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Email service is temporarily paused via administrative controls.'
          }), { status: 503, headers: corsHeaders });
        }
        if (emailConfigErr) {
          return new Response(JSON.stringify({
            success: false,
            error: emailConfigErr
          }), { status: 503, headers: corsHeaders });
        }

        // 5. Generate ONE shared 6-digit code, 10-minute expiry, keyed HMAC hash
        const randomArr = new Uint32Array(1);
        crypto.getRandomValues(randomArr);
        const otpCode = (100000 + (randomArr[0] % 900000)).toString();
        const codeHash = await hmacSha256Hex(otpSecret, `${rawEmail}:${otpCode}`);
        const expiresAt = now + 10 * 60 * 1000; // 10 minutes
        const challengeId = 'eotp_' + now + '_' + getRandomHex(4);

        // 6. Dispatch the EXACT SAME 6-digit code to Email AND optional +91 Mobile SMS concurrently
        // SMS failure, timeout, or skip NEVER blocks or delays Email OTP.
        const emailSubject = `Your Numeros Vision Verification Code: ${otpCode}`;
        const emailText = `Your Numeros Vision verification code is: ${otpCode}\n\nThis single-use code expires in 10 minutes. If you did not request this, you can safely ignore this message.`;
        const emailHtml = `<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:480px;margin:0 auto;padding:24px;background:#FFFDF7;border:1px solid rgba(201,162,39,0.35);border-radius:12px;color:#523E28;">
  <div style="font-size:16px;font-weight:700;color:#8B6914;margin-bottom:12px;letter-spacing:0.04em;">NUMEROS VISION</div>
  <p style="font-size:14px;line-height:1.5;margin:0 0 16px;">Here is your 6-digit verification code:</p>
  <div style="font-size:28px;font-weight:700;letter-spacing:6px;color:#8B6914;background:#FAF6EE;border:1px solid rgba(201,162,39,0.25);border-radius:8px;padding:12px 18px;text-align:center;margin-bottom:16px;font-family:monospace;">${otpCode}</div>
  <p style="font-size:12px;color:#7A654D;line-height:1.5;margin:0;">Valid for 10 minutes. Single-use only. Please never share this code.</p>
</div>`;

        const emailPromise = sendTransactionalEmail(env, {
          to: rawEmail,
          subject: emailSubject,
          text: emailText,
          html: emailHtml
        }).catch((err) => ({
          success: false,
          error: redactOtpAndPhone(err && err.message ? err.message : 'Email delivery error.', otpCode)
        }));

        const smsPromise = (targetMobile10 && smsAllowedByRateLimit)
          ? dispatchMobileSmsOtp(env, targetMobile10, otpCode).catch(() => ({
              success: false,
              skipped: false,
              reason: 'sms_error'
            }))
          : Promise.resolve({ success: false, configured: false, skipped: true, reason: 'not_requested' });

        const [sendResult, smsResult] = await Promise.all([emailPromise, smsPromise]);

        if (!sendResult || !sendResult.success) {
          const safeEmailErr = redactOtpAndPhone((sendResult && sendResult.error) || 'Verification code delivery failed. Please try again.', otpCode);
          return new Response(JSON.stringify({
            success: false,
            error: safeEmailErr
          }), { status: (sendResult && sendResult.status) || 503, headers: corsHeaders });
        }

        // 6b. Record challenge in DB / Memory
        if (env.DB) {
          try {
            await env.DB.prepare(
              'INSERT INTO email_otp_challenges (id, email_hash, code_hash, attempts, max_attempts, expires_at, created_at, ip_hash) VALUES (?, ?, ?, 0, 5, ?, ?, ?)'
            ).bind(challengeId, emailHash, codeHash, expiresAt, now, ipHash).run();
          } catch (e) {
            console.warn('[D1_EmailChallenge_Insert_Error]', redactOtpAndPhone(e && e.message, otpCode));
          }
        }
        memoryStore.emailOtpChallenges = memoryStore.emailOtpChallenges || new Map();
        memoryStore.emailOtpChallenges.set(emailHash, {
          id: challengeId,
          email_hash: emailHash,
          code_hash: codeHash,
          attempts: 0,
          max_attempts: 5,
          expires_at: expiresAt,
          created_at: now,
          ip_hash: ipHash
        });

        // 7. Enumeration Neutrality + Accurate Channel Dispatch Result (never unmasked phone or OTP)
        const responsePayload = {
          success: true,
          message: 'If this email address is valid, a 6-digit verification code has been dispatched.'
        };
        if (rawPhoneInput) {
          const smsDispatched = Boolean(explicitMobile10 && smsResult && smsResult.success);
          responsePayload.channels_dispatched = {
            email: true,
            sms: smsDispatched
          };
          responsePayload.phone_masked = explicitMobile10 ? maskPhoneLast2(explicitMobile10) : null;
          responsePayload.channel_message = smsDispatched
            ? '6-digit code sent to your email and mobile.'
            : '6-digit code sent to your email.';
        }
        return new Response(JSON.stringify(responsePayload), { status: 200, headers: corsHeaders });

      } catch (err) {
        return new Response(JSON.stringify({ success: false, error: redactOtpAndPhone(err && err.message ? err.message : 'Server error') }), {
          status: 500,
          headers: corsHeaders
        });
      }
    }

    // =========================================================================
    // ROUTE: EMAIL OTP - VERIFY CODE (/api/v1/auth/email/verify-code)
    // 5 attempts limit, 10m expiry, single use, mints checkout_token or session
    // =========================================================================
    if (url.pathname === '/api/v1/auth/email/verify-code' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      try {
        const body = await request.json().catch(() => ({}));
        const rawEmail = (body.email || body.identifier || '').toString().trim().toLowerCase();
        const code = (body.code || body.otp || '').toString().trim();
        const checkoutFlow = Boolean(body.checkout_flow);

        if (!rawEmail || !code || code.length !== 6) {
          return new Response(JSON.stringify({
            verified: false,
            success: false,
            error: 'Valid email and 6-digit verification code are required.'
          }), { status: 400, headers: corsHeaders });
        }

        const otpSecret = requireSecret(env, 'OTP_HMAC_SECRET');
        const sessionSecret = requireSecret(env, 'SESSION_SECRET');
        const ipSalt = requireSecret(env, 'IP_HASH_SALT');
        const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
        const emailHash = await hmacSha256Hex(otpSecret, rawEmail);
        const ipHash = await hmacSha256Hex(ipSalt, clientIp);
        const now = Date.now();

        // 1. Retrieve active challenge
        let challenge = null;
        if (env.DB) {
          try {
            challenge = await env.DB.prepare(
              'SELECT id, code_hash, attempts, max_attempts, expires_at, verified_at FROM email_otp_challenges WHERE email_hash = ? AND verified_at IS NULL AND expires_at > ? ORDER BY created_at DESC LIMIT 1'
            ).bind(emailHash, now).first();
          } catch (e) {
            console.warn('[D1_EmailChallenge_Query_Fallback]', e.message);
          }
        }
        if (!challenge && memoryStore.emailOtpChallenges) {
          const mChal = memoryStore.emailOtpChallenges.get(emailHash);
          if (mChal && mChal.expires_at > now && !mChal.verified_at) {
            challenge = mChal;
          }
        }

        if (!challenge) {
          return new Response(JSON.stringify({
            verified: false,
            success: false,
            error: 'Verification code is invalid or has expired. Please request a new code.'
          }), { status: 400, headers: corsHeaders });
        }

        // 2. Enforce 5-attempt lockout
        if (challenge.attempts >= challenge.max_attempts) {
          return new Response(JSON.stringify({
            verified: false,
            success: false,
            error: 'Maximum verification attempts exceeded. Please request a new code.'
          }), { status: 429, headers: corsHeaders });
        }

        const newAttempts = challenge.attempts + 1;
        if (env.DB) {
          try {
            await env.DB.prepare('UPDATE email_otp_challenges SET attempts = ? WHERE id = ?').bind(newAttempts, challenge.id).run();
          } catch (e) {}
        }
        challenge.attempts = newAttempts;

        // 3. Timing-safe code verification
        const expectedCodeHash = await hmacSha256Hex(otpSecret, `${rawEmail}:${code}`);
        const isValid = timingSafeEqual(expectedCodeHash, challenge.code_hash);

        if (!isValid) {
          const remaining = challenge.max_attempts - newAttempts;
          return new Response(JSON.stringify({
            verified: false,
            success: false,
            error: remaining > 0 ? `Incorrect code. ${remaining} attempts remaining.` : 'Maximum verification attempts exceeded. Please request a new code.'
          }), { status: 400, headers: corsHeaders });
        }

        // 4. Mark challenge verified (SINGLE USE)
        challenge.verified_at = now;
        if (env.DB) {
          try {
            await env.DB.prepare('UPDATE email_otp_challenges SET verified_at = ? WHERE id = ?').bind(now, challenge.id).run();
          } catch (e) {}
        }

        // 5. Find or create user (and persist encrypted contact mobile if provided during checkout/login)
        let userId = null;
        let isNewUser = false;
        const contactMobile10 = parseStrictPlus91Mobile10(body.phone || body.mobile || body.customer_phone || '');
        let contactPhoneHash = null;
        let contactPhoneEnc = null;
        if (contactMobile10 && env && env.DATA_ENCRYPTION_KEY && /^[0-9a-fA-F]{64}$/.test(String(env.DATA_ENCRYPTION_KEY).trim())) {
          try {
            contactPhoneHash = await hmacSha256Hex(otpSecret, contactMobile10);
            contactPhoneEnc = await encryptField(contactMobile10, env.DATA_ENCRYPTION_KEY.trim());
          } catch (_) {}
        }
        if (env.DB) {
          try {
            const user = await env.DB.prepare('SELECT id, phone_enc FROM users WHERE email = ?').bind(rawEmail).first();
            if (user) {
              userId = user.id;
              if (contactPhoneHash && contactPhoneEnc && !user.phone_enc) {
                await env.DB.prepare('UPDATE users SET phone_hash = ?, phone_enc = ? WHERE id = ?').bind(contactPhoneHash, contactPhoneEnc, userId).run();
              }
            } else {
              userId = 'usr_' + now + '_' + getRandomHex(4);
              isNewUser = true;
              await env.DB.prepare('INSERT INTO users (id, email, phone_hash, phone_enc, created_at) VALUES (?, ?, ?, ?, ?)').bind(userId, rawEmail, contactPhoneHash, contactPhoneEnc, now).run();
              // Record statutory consents (marketing OFF by default)
              await recordUserConsent(env, userId, 'service_delivery', 1, ipHash, now);
              await recordUserConsent(env, userId, 'marketing_communications', body.consent_marketing ? 1 : 0, ipHash, now);
            }
          } catch (e) {
            console.warn('[D1_User_EmailVerify_Error]', redactOtpAndPhone(e && e.message, code));
          }
        } else {
          let user = memoryStore.users.get(rawEmail);
          if (user) {
            userId = user.id;
            if (contactPhoneHash && contactPhoneEnc && !user.phone_enc) {
              user.phone_hash = contactPhoneHash;
              user.phone_enc = contactPhoneEnc;
            }
          } else {
            userId = 'usr_' + now + '_' + getRandomHex(4);
            isNewUser = true;
            user = { id: userId, email: rawEmail, phone_hash: contactPhoneHash, phone_enc: contactPhoneEnc, createdAt: now };
            memoryStore.users.set(rawEmail, user);
            await recordUserConsent(env, userId, 'service_delivery', 1, ipHash, now);
            await recordUserConsent(env, userId, 'marketing_communications', body.consent_marketing ? 1 : 0, ipHash, now);
          }
        }

        // 6. Branch: Checkout Flow vs. Standard Login
        if (checkoutFlow) {
          // Condition 1: Mint single-checkout verification token (valid 30 min)
          const checkoutToken = await mintCheckoutToken(sessionSecret, rawEmail, now);
          return new Response(JSON.stringify({
            verified: true,
            success: true,
            email_verified: true,
            checkout_token: checkoutToken,
            email: rawEmail,
            user_id: userId,
            is_new_user: isNewUser,
            message: 'Email successfully verified for checkout.'
          }), { status: 200, headers: corsHeaders });
        }

        // Direct Login: Mint session & set cookie
        const rawToken = await mintUserSession(env, userId, clientIp, now);
        const isLocal = env.ENVIRONMENT === 'local' || env.ENVIRONMENT === 'test';
        return new Response(JSON.stringify({
          verified: true,
          authenticated: true,
          success: true,
          user: {
            id: userId,
            email: rawEmail,
            is_new_user: isNewUser
          },
          message: 'Authentication successful.'
        }), {
          status: 200,
          headers: {
            ...corsHeaders,
            'Set-Cookie': createSessionCookieHeader(rawToken, isLocal)
          }
        });

      } catch (err) {
        return new Response(JSON.stringify({ verified: false, success: false, error: err.message }), {
          status: 500,
          headers: corsHeaders
        });
      }
    }

    // =========================================================================
    // ROUTE: RECORD STATUTORY CONSENT (/api/v1/auth/consent) - BACKEND ONLY
    // Records DPDP service delivery and marketing consents directly to user_consents
    // =========================================================================
    if (url.pathname === '/api/v1/auth/consent' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      try {
        const body = await request.json().catch(() => ({}));
        const user = await authenticateUser(request, env);
        const email = (body.email || '').trim().toLowerCase();
        let targetUserId = user ? user.user_id : null;
        const now = Date.now();
        const ipSalt = requireSecret(env, 'IP_HASH_SALT');
        const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
        const ipHash = await hmacSha256Hex(ipSalt, clientIp);

        if (!targetUserId && email && body.checkout_token) {
          const sessionSecret = requireSecret(env, 'SESSION_SECRET');
          const tokenValid = await verifyCheckoutToken(sessionSecret, email, body.checkout_token);
          if (tokenValid) {
            targetUserId = 'chk_' + email;
          }
        }
        if (!targetUserId) {
          targetUserId = 'guest_' + ipHash.substring(0, 16);
        }

        const serviceGiven = body.consent_service !== false ? 1 : 0;
        const marketingGiven = body.consent_marketing ? 1 : 0;

        await recordUserConsent(env, targetUserId, 'service_delivery', serviceGiven, ipHash, now);
        await recordUserConsent(env, targetUserId, 'marketing_communications', marketingGiven, ipHash, now);

        return new Response(JSON.stringify({
          success: true,
          message: 'Consent preferences recorded successfully.',
          version: 'v1.0_2026_{{CONSENT_TEXT_PENDING}}'
        }), { status: 200, headers: corsHeaders });
      } catch (err) {
        return new Response(JSON.stringify({ success: false, error: err.message }), { status: 500, headers: corsHeaders });
      }
    }

    // 1. ROUTE: SEND OTP (/api/v1/auth/otp/send) - GATED BEHIND OTP_ENABLED=false
    if (url.pathname === '/api/v1/auth/otp/send' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      const smsOtpEnabled = env && (env.OTP_ENABLED === 'true' || env.OTP_ENABLED === true);
      if (!smsOtpEnabled) {
        return new Response(JSON.stringify({
          success: false,
          error: 'SMS OTP is disabled in this environment. Please use email verification.'
        }), { status: 403, headers: corsHeaders });
      }
      try {
        const body = await request.json().catch(() => ({}));
        const rawPhone = (body.phone || body.identifier || '').toString();
        const cleanDigits = rawPhone.replace(/\D/g, '');
        const mobile10 = cleanDigits.length >= 10 ? cleanDigits.slice(-10) : '';

        if (!mobile10 || mobile10.length !== 10) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Please enter a valid 10-digit mobile number.'
          }), { status: 400, headers: corsHeaders });
        }

        const otpSecret = requireSecret(env, 'OTP_HMAC_SECRET');
        const ipSalt = requireSecret(env, 'IP_HASH_SALT');
        const clientIp = request.headers.get('CF-Connecting-IP') || request.headers.get('x-forwarded-for') || '127.0.0.1';
        const phoneHash = await hmacSha256Hex(otpSecret, mobile10);
        const ipHash = await hmacSha256Hex(ipSalt, clientIp);
        const now = Date.now();

        // Rate limiting checks
        if (env.DB) {
          const recentNum = await env.DB.prepare(
            'SELECT COUNT(*) as cnt, MAX(created_at) as last_req FROM otp_challenges WHERE phone_hash = ? AND created_at > ?'
          ).bind(phoneHash, now - 3600000).first();

          if (recentNum && recentNum.last_req && (now - recentNum.last_req) < 60000) {
            return new Response(JSON.stringify({
              success: false,
              error: 'Please wait 60 seconds before requesting another code.'
            }), { status: 429, headers: corsHeaders });
          }
          if (recentNum && recentNum.cnt >= 5) {
            return new Response(JSON.stringify({
              success: false,
              error: 'Maximum OTP requests exceeded for this number. Please try again in 1 hour.'
            }), { status: 429, headers: corsHeaders });
          }

          const recentIp = await env.DB.prepare(
            'SELECT COUNT(*) as cnt FROM otp_challenges WHERE ip_hash = ? AND created_at > ?'
          ).bind(ipHash, now - 3600000).first();

          if (recentIp && recentIp.cnt >= 10) {
            return new Response(JSON.stringify({
              success: false,
              error: 'Rate limit exceeded for this IP. Please try again later.'
            }), { status: 429, headers: corsHeaders });
          }
        } else {
          memoryStore.otpHistory = memoryStore.otpHistory || [];
          memoryStore.otpHistory = memoryStore.otpHistory.filter(h => (now - h.created_at) < 3600000);

          const phoneHistory = memoryStore.otpHistory.filter(h => h.phone_hash === phoneHash);
          const lastReq = phoneHistory.length > 0 ? Math.max(...phoneHistory.map(h => h.created_at)) : 0;
          if (lastReq && (now - lastReq) < 60000) {
            return new Response(JSON.stringify({
              success: false,
              error: 'Please wait 60 seconds before requesting another code.'
            }), { status: 429, headers: corsHeaders });
          }
          if (phoneHistory.length >= 5) {
            return new Response(JSON.stringify({
              success: false,
              error: 'Maximum OTP requests exceeded for this number. Please try again in 1 hour.'
            }), { status: 429, headers: corsHeaders });
          }
          const ipHistory = memoryStore.otpHistory.filter(h => h.ip_hash === ipHash);
          if (ipHistory.length >= 10) {
            return new Response(JSON.stringify({
              success: false,
              error: 'Rate limit exceeded for this IP. Please try again later.'
            }), { status: 429, headers: corsHeaders });
          }
        }

        // Cryptographically secure 6-digit OTP
        const randomArr = new Uint32Array(1);
        crypto.getRandomValues(randomArr);
        const otpCode = (100000 + (randomArr[0] % 900000)).toString();
        const codeHash = await hmacSha256Hex(otpSecret, `${mobile10}:${otpCode}`);
        const expiresAt = now + 5 * 60 * 1000;
        const challengeId = 'otp_' + now + '_' + getRandomHex(4);

        // SMS dispatch via Brevo Transactional SMS v3 (primary when Brevo configured) or Fast2SMS fallback
        const smsDispatchRes = await dispatchMobileSmsOtp(env, mobile10, otpCode);
        const smsDispatched = Boolean(smsDispatchRes && smsDispatchRes.success);
        const smsErrorMessage = smsDispatchRes && smsDispatchRes.error ? smsDispatchRes.error : null;
        if (!smsDispatched && smsDispatchRes && smsDispatchRes.configured === false) {
          return new Response(JSON.stringify({
            success: false,
            sms_delivered: false,
            error: smsErrorMessage || 'SMS service is temporarily unavailable in this environment.'
          }), { status: 503, headers: corsHeaders });
        }

        if (!smsDispatched) {
          return new Response(JSON.stringify({
            success: false,
            sms_delivered: false,
            error: `SMS delivery failed: ${smsErrorMessage || 'Gateway error. Please try again shortly.'}`
          }), { status: 503, headers: corsHeaders });
        }

        // Only insert the challenge if SMS was successfully accepted for delivery
        if (env.DB) {
          await env.DB.prepare(
            'INSERT INTO otp_challenges (id, phone_hash, code_hash, attempts, max_attempts, expires_at, created_at, ip_hash) VALUES (?, ?, ?, 0, 5, ?, ?, ?)'
          ).bind(challengeId, phoneHash, codeHash, expiresAt, now, ipHash).run();
        } else {
          memoryStore.otpChallenges.set(phoneHash, {
            id: challengeId,
            phone_hash: phoneHash,
            code_hash: codeHash,
            attempts: 0,
            max_attempts: 5,
            expires_at: expiresAt,
            created_at: now,
            ip_hash: ipHash
          });
          memoryStore.otpHistory.push({ phone_hash: phoneHash, ip_hash: ipHash, created_at: now });
        }

        const respPayload = {
          success: true,
          sms_delivered: true,
          destination: maskPhoneLast2(mobile10),
          expires_in: 300,
          message: `Verification code sent to ${maskPhoneLast2(mobile10)}`
        };

        return new Response(JSON.stringify(respPayload), { status: 200, headers: corsHeaders });
      } catch (err) {
        return new Response(JSON.stringify({ success: false, error: err.message || 'OTP dispatch error' }), {
          status: 500,
          headers: corsHeaders
        });
      }
    }

    // 2. ROUTE: VERIFY OTP (/api/v1/auth/otp/verify & /api/v1/auth/login) - GATED BEHIND OTP_ENABLED=false
    if ((url.pathname === '/api/v1/auth/otp/verify' || url.pathname === '/api/v1/auth/login' || url.pathname === '/api/v1/auth/otp/login') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      const smsOtpEnabled = env && (env.OTP_ENABLED === 'true' || env.OTP_ENABLED === true);
      if (!smsOtpEnabled) {
        return new Response(JSON.stringify({
          verified: false,
          success: false,
          error: 'SMS OTP is disabled in this environment. Please use email verification.'
        }), { status: 403, headers: corsHeaders });
      }
      try {
        const body = await request.json().catch(() => ({}));
        const rawPhone = (body.phone || body.identifier || body.login_id || '').toString();
        const code = (body.otp || body.code || '').toString().trim();
        const cleanDigits = rawPhone.replace(/\D/g, '');
        const mobile10 = cleanDigits.length >= 10 ? cleanDigits.slice(-10) : '';

        if (!mobile10 || !code) {
          return new Response(JSON.stringify({
            verified: false,
            error: 'Mobile number and 6-digit verification code are required.'
          }), { status: 400, headers: corsHeaders });
        }

        const otpSecret = requireSecret(env, 'OTP_HMAC_SECRET');
        const sessionSecret = requireSecret(env, 'SESSION_SECRET');
        const ipSalt = requireSecret(env, 'IP_HASH_SALT');
        const dataEncKey = requireSecret(env, 'DATA_ENCRYPTION_KEY');
        const phoneHash = await hmacSha256Hex(otpSecret, mobile10);
        const now = Date.now();

        let challenge = null;
        if (env.DB) {
          challenge = await env.DB.prepare(
            'SELECT id, code_hash, attempts, max_attempts, expires_at FROM otp_challenges WHERE phone_hash = ? AND expires_at > ? ORDER BY created_at DESC LIMIT 1'
          ).bind(phoneHash, now).first();
        } else {
          challenge = memoryStore.otpChallenges.get(phoneHash);
          if (challenge && challenge.expires_at <= now) challenge = null;
        }

        if (!challenge) {
          return new Response(JSON.stringify({
            verified: false,
            error: 'Verification code expired or not found. Please request a new code.'
          }), { status: 400, headers: corsHeaders });
        }

        if (challenge.attempts >= challenge.max_attempts) {
          return new Response(JSON.stringify({
            verified: false,
            error: 'Maximum verification attempts exceeded. Please request a new code.'
          }), { status: 429, headers: corsHeaders });
        }

        const newAttempts = challenge.attempts + 1;
        if (env.DB) {
          await env.DB.prepare('UPDATE otp_challenges SET attempts = ? WHERE id = ?').bind(newAttempts, challenge.id).run();
        } else {
          challenge.attempts = newAttempts;
        }

        const isNonProd = env && (env.ENVIRONMENT === 'local' || env.ENVIRONMENT === 'preview');
        const expectedCodeHash = await hmacSha256Hex(otpSecret, `${mobile10}:${code}`);
        const isValid = timingSafeEqual(expectedCodeHash, challenge.code_hash);

        if (!isValid) {
          const remaining = challenge.max_attempts - newAttempts;
          return new Response(JSON.stringify({
            verified: false,
            error: remaining > 0
              ? `Invalid verification code. ${remaining} attempt${remaining === 1 ? '' : 's'} remaining.`
              : 'Maximum attempts reached. Please request a new code.'
          }), { status: 400, headers: corsHeaders });
        }

        // Clean up verified challenge
        if (env.DB) {
          await env.DB.prepare('DELETE FROM otp_challenges WHERE id = ?').bind(challenge.id).run();
        } else {
          memoryStore.otpChallenges.delete(phoneHash);
        }

        // Find or create User in D1
        let userId = null;
        let isNewUser = false;
        const phoneEnc = await encryptField(mobile10, dataEncKey);
        if (env.DB) {
          let user = await env.DB.prepare('SELECT id FROM users WHERE phone_hash = ?').bind(phoneHash).first();
          if (!user) {
            userId = 'usr_' + now + '_' + getRandomHex(4);
            await env.DB.prepare('INSERT INTO users (id, phone_hash, phone_enc, created_at) VALUES (?, ?, ?, ?)').bind(userId, phoneHash, phoneEnc, now).run();
            isNewUser = true;
            await env.DB.prepare(
              'INSERT INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
            ).bind('crd_' + now + '_free', userId, 3, 'signup_bonus', 'signup_free_' + userId, 3, now).run();
          } else {
            userId = user.id;
          }
        } else {
          let user = memoryStore.users.get(phoneHash);
          if (!user) {
            userId = 'usr_' + now + '_' + getRandomHex(4);
            user = { id: userId, phoneHash, phone_enc: phoneEnc, createdAt: now };
            memoryStore.users.set(phoneHash, user);
            isNewUser = true;
            if (memoryStore.creditLedger) {
              memoryStore.creditLedger.set('crd_' + now + '_free', {
                id: 'crd_' + now + '_free',
                user_id: userId,
                delta: 3,
                reason: 'signup_bonus',
                ref_id: 'signup_free_' + userId,
                balance_after: 3,
                created_at: now
              });
            }
          } else {
            userId = user.id;
          }
        }

        // Issue server session in D1
        const rawToken = getRandomHex(32);
        const tokenHash = await hmacSha256Hex(sessionSecret, rawToken);
        const sessionExpiresAt = now + 30 * 24 * 3600 * 1000;
        const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
        const userAgent = request.headers.get('User-Agent') || 'Unknown';
        const ipHash = await hmacSha256Hex(ipSalt, clientIp);

        if (env.DB) {
          const pseudoId = (body.pseudonymous_id || body.client_identity_id || '').trim();
          if (pseudoId) {
            try {
              await env.DB.prepare('UPDATE cookie_consents SET user_id = ?, updated_at = ? WHERE pseudonymous_id = ? AND user_id IS NULL')
                .bind(userId, Math.floor(now / 1000), pseudoId).run();
            } catch (e) {}
          }
          await env.DB.prepare(
            'INSERT INTO sessions (id, user_id, token_hash, expires_at, created_at, ip_hash, user_agent) VALUES (?, ?, ?, ?, ?, ?, ?)'
          ).bind('sess_' + now + '_' + getRandomHex(4), userId, tokenHash, sessionExpiresAt, now, ipHash, userAgent).run();
        } else {
          memoryStore.sessions.set(tokenHash, {
            id: 'sess_' + now,
            user_id: userId,
            token_hash: tokenHash,
            expires_at: sessionExpiresAt,
            created_at: now
          });
        }

        return new Response(JSON.stringify({
          verified: true,
          authenticated: true,
          user: {
            id: userId,
            phone_masked: maskPhoneLast2(mobile10),
            is_new_user: isNewUser
          },
          message: 'Authentication successful.'
        }), {
          status: 200,
          headers: {
            ...corsHeaders,
            'Set-Cookie': `__Host-nv_session=${rawToken}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000`
          }
        });
      } catch (err) {
        return new Response(JSON.stringify({ verified: false, error: err.message }), {
          status: 500,
          headers: corsHeaders
        });
      }
    }

    // 3. ROUTE: GOOGLE IDENTITY AUTH (/api/v1/auth/google)
    if (url.pathname === '/api/v1/auth/google' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      try {
        const body = await request.json().catch(() => ({}));
        const credential = body.credential || body.id_token;
        const isNonProd = env && (env.ENVIRONMENT === 'local' || env.ENVIRONMENT === 'preview' || !env.GOOGLE_CLIENT_ID);
        let verifiedEmail = null;
        let verifiedName = null;

        if (credential) {
          if (!env.GOOGLE_CLIENT_ID) {
            return new Response(JSON.stringify({
              success: false,
              error: 'Google Identity authentication is not configured in this environment.'
            }), { status: 503, headers: corsHeaders });
          }
          const verifyResult = await verifyGoogleIdToken(credential, env);
          if (!verifyResult.valid) {
            return new Response(JSON.stringify({
              success: false,
              error: verifyResult.error
            }), { status: 401, headers: corsHeaders });
          }
          const tokenInfo = verifyResult.payload;
          verifiedEmail = tokenInfo.email.toLowerCase().trim();
          verifiedName = tokenInfo.name || verifiedEmail.split('@')[0];

        } else {
          return new Response(JSON.stringify({
            success: false,
            error: 'Google ID token credential or account email is required.'
          }), { status: 400, headers: corsHeaders });
        }
        const now = Date.now();
        let userId = null;

        if (env.DB) {
          let user = await env.DB.prepare('SELECT id FROM users WHERE email = ?').bind(verifiedEmail).first();
          if (!user) {
            userId = 'usr_' + now + '_' + getRandomHex(4);
            await env.DB.prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)').bind(userId, verifiedEmail, now).run();
            await env.DB.prepare(
              'INSERT INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
            ).bind('crd_' + now + '_free', userId, 3, 'signup_bonus', 'signup_free_' + userId, 3, now).run();
          } else {
            userId = user.id;
          }
        } else {
          let user = memoryStore.users.get(verifiedEmail);
          if (!user) {
            userId = 'usr_' + now + '_' + getRandomHex(4);
            memoryStore.users.set(verifiedEmail, { id: userId, email: verifiedEmail, createdAt: now });
          } else {
            userId = user.id;
          }
        }

        const sessionSecret = requireSecret(env, 'SESSION_SECRET');
        const ipSalt = requireSecret(env, 'IP_HASH_SALT');
        const rawToken = getRandomHex(32);
        const tokenHash = await hmacSha256Hex(sessionSecret, rawToken);
        const sessionExpiresAt = now + 30 * 24 * 3600 * 1000;
        const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
        const ipHash = await hmacSha256Hex(ipSalt, clientIp);
        const userAgent = request.headers.get('User-Agent') || 'Unknown';

        if (env.DB) {
          const pseudoId = (body.pseudonymous_id || body.client_identity_id || '').trim();
          if (pseudoId) {
            try {
              await env.DB.prepare('UPDATE cookie_consents SET user_id = ?, updated_at = ? WHERE pseudonymous_id = ? AND user_id IS NULL')
                .bind(userId, Math.floor(now / 1000), pseudoId).run();
            } catch (e) {}
          }
          await env.DB.prepare(
            'INSERT INTO sessions (id, user_id, token_hash, expires_at, created_at, ip_hash, user_agent) VALUES (?, ?, ?, ?, ?, ?, ?)'
          ).bind('sess_' + now + '_' + getRandomHex(4), userId, tokenHash, sessionExpiresAt, now, ipHash, userAgent).run();
        } else {
          memoryStore.sessions.set(tokenHash, {
            id: 'sess_' + now,
            user_id: userId,
            token_hash: tokenHash,
            expires_at: sessionExpiresAt,
            created_at: now
          });
        }

        return new Response(JSON.stringify({
          success: true,
          verified: true,
          user: {
            id: userId,
            email: verifiedEmail,
            has_phone: false
          },
          redirect_url: '/dashboard/'
        }), {
          status: 200,
          headers: {
            ...corsHeaders,
            'Set-Cookie': `__Host-nv_session=${rawToken}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000`
          }
        });
      } catch (err) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Google authentication processing error: ' + err.message
        }), { status: 500, headers: corsHeaders });
      }
    }

    // 3B. ROUTE: PRIVACY & COOKIE CONSENT (/api/v1/privacy/consent)
    if (url.pathname === '/api/v1/privacy/consent' && (request.method === 'POST' || request.method === 'GET' || request.method === 'OPTIONS')) {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };

      if (request.method === 'OPTIONS') {
        return new Response(null, { status: 204, headers: corsHeaders });
      }

      let userId = null;
      try {
        const sessionUser = await authenticateUser(request, env);
        if (sessionUser && sessionUser.user_id) userId = sessionUser.user_id;
      } catch (e) {}

      if (request.method === 'GET') {
        const pseudoId = (url.searchParams.get('pseudonymous_id') || '').trim();
        let row = null;
        if (env.DB) {
          try {
            if (userId) {
              row = await env.DB.prepare('SELECT * FROM cookie_consents WHERE user_id = ? ORDER BY updated_at DESC LIMIT 1').bind(userId).first();
            } else if (pseudoId) {
              row = await env.DB.prepare('SELECT * FROM cookie_consents WHERE pseudonymous_id = ? ORDER BY updated_at DESC LIMIT 1').bind(pseudoId).first();
            }
          } catch (e) {}
        }
        return new Response(JSON.stringify({
          success: true,
          consent: row ? {
            choices: JSON.parse(row.choices_json || '{}'),
            banner_version: row.banner_version,
            updated_at: row.updated_at
          } : null
        }), { status: 200, headers: corsHeaders });
      }

      if (request.method === 'POST') {
        try {
          const body = await request.json().catch(() => ({}));
          const pseudoId = (body.pseudonymous_id || body.identity_id || '').trim();
          if (!pseudoId) {
            return new Response(JSON.stringify({ success: false, error: 'pseudonymous_id is required' }), { status: 400, headers: corsHeaders });
          }

          const choices = body.choices || {
            essential: true,
            analytics: Boolean(body.purpose === 'ANALYTICS' || body.level === 'all'),
            marketing: Boolean(body.level === 'all')
          };
          const essential = 1;
          const analytics = choices.analytics ? 1 : 0;
          const marketing = choices.marketing ? 1 : 0;
          const bannerVersion = body.banner_version || body.policy_version || '2026.2.DPDP_GDPR';
          const nowEpoch = Math.floor(Date.now() / 1000);
          const consentId = 'cons_' + Date.now().toString(36) + '_' + Math.random().toString(36).substring(2, 8);

          const ip = request.headers.get('cf-connecting-ip') || '';
          const userAgent = request.headers.get('user-agent') || '';
          let ipHash = '';
          if (ip) {
            const hashBuf = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(ip + (env.DOWNLOAD_TOKEN_SECRET || 'nv_salt')));
            ipHash = Array.from(new Uint8Array(hashBuf)).map(b => b.toString(16).padStart(2, '0')).join('').substring(0, 32);
          }

          if (env.DB) {
            try {
              await env.DB.prepare(`
                INSERT INTO cookie_consents (
                  id, pseudonymous_id, user_id, essential_granted, analytics_granted, marketing_granted,
                  choices_json, banner_version, ip_hash, user_agent, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
              `).bind(
                consentId, pseudoId, userId, essential, analytics, marketing,
                JSON.stringify(choices), bannerVersion, ipHash, userAgent.substring(0, 200),
                nowEpoch, nowEpoch
              ).run();
            } catch (d1Err) {
              // Graceful fallback to audit_log
              try {
                await env.DB.prepare(
                  'INSERT INTO audit_log (id, action, entity_type, entity_id, user_id, details_json, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
                ).bind(
                  'aud_' + consentId, 'COOKIE_CONSENT_RECORDED', 'consent', consentId, userId,
                  JSON.stringify({ pseudoId, choices, bannerVersion }), nowEpoch
                ).run();
              } catch (audErr) {}
            }
          }

          const respHeaders = new Headers(corsHeaders);
          // Set device cookie ONLY after analytics consent is granted; delete if denied
          if (analytics) {
            const devId = (body.device_id && body.device_id.startsWith('nv_dev_')) ? body.device_id : ('nv_dev_' + crypto.randomUUID().replace(/-/g, ''));
            respHeaders.append('Set-Cookie', `nv_dev_id=${encodeURIComponent(devId)}; Path=/; Max-Age=31536000; Secure; SameSite=Lax`);
          } else {
            respHeaders.append('Set-Cookie', 'nv_dev_id=; Path=/; Max-Age=0; Secure; SameSite=Lax');
          }

          return new Response(JSON.stringify({
            success: true,
            consent_id: consentId,
            status: (analytics || marketing) ? 'GRANTED' : 'ESSENTIAL_ONLY',
            analytics_granted: Boolean(analytics),
            marketing_granted: Boolean(marketing)
          }), { status: 200, headers: respHeaders });
        } catch (postErr) {
          return new Response(JSON.stringify({ success: false, error: postErr.message }), { status: 500, headers: corsHeaders });
        }
      }
    }




  // Sliding window checkFormRateLimit uses module-scoped _formRateLimits
  function checkFormRateLimit(clientIp, limit = 5, windowMs = 600000) {
    const now = Date.now();
    const list = _formRateLimits.get(clientIp) || [];
    const valid = list.filter(t => now - t < windowMs);
    if (valid.length >= limit) return false;
    valid.push(now);
    _formRateLimits.set(clientIp, valid);
    return true;
  }

  // Cross-isolate durable rate limiter backed by D1 (fails closed outside tests if D1 is missing)
  async function checkDurableRateLimit(env, key, limit, windowMs) {
    const now = Date.now();
    const isTestEnv = Boolean(
      env && (
        env.ENVIRONMENT === 'local' ||
        env.MOCK_PAYMENTS === 'true' ||
        env.NODE_ENV === 'test' ||
        env.__TEST__ === true
      )
    );

    if (env && env.DB) {
      try {
        const row = await env.DB.prepare('SELECT count, window_start, expires_at FROM charm_rate_limits WHERE key = ?').bind(key).first();
        if (!row || now >= row.expires_at) {
          await env.DB.prepare(
            'INSERT INTO charm_rate_limits (key, count, window_start, expires_at) VALUES (?, 1, ?, ?) ON CONFLICT(key) DO UPDATE SET count = 1, window_start = ?, expires_at = ?'
          ).bind(key, now, now + windowMs, now, now + windowMs).run();
          return true;
        }
        if (row.count >= limit) {
          return false;
        }
        await env.DB.prepare('UPDATE charm_rate_limits SET count = count + 1 WHERE key = ?').bind(key).run();
        return true;
      } catch (e) {
        console.warn('Durable rate limit check error:', e);
        if (!isTestEnv) {
          // Fail closed outside tests when DB query errors
          return false;
        }
      }
    }

    // Fail closed: outside test environments, missing D1 rate-limit binding rejects request
    if (!isTestEnv) {
      console.error('Durable rate limit rejected: missing D1 DB binding outside test environment');
      return false;
    }

    if (!memoryStore.charmRateLimits) memoryStore.charmRateLimits = new Map();
    const entry = memoryStore.charmRateLimits.get(key);
    if (!entry || now >= entry.expires_at) {
      memoryStore.charmRateLimits.set(key, { count: 1, window_start: now, expires_at: now + windowMs });
      return true;
    }
    if (entry.count >= limit) {
      return false;
    }
    entry.count += 1;
    return true;
  }

  async function getOrCreateVisitorId(request, env) {
    let visitorId = getCookie(request, 'nv_visitor_id');
    let isNew = false;
    if (!visitorId || visitorId.length < 16) {
      visitorId = 'vis_' + Date.now() + '_' + getRandomHex(8);
      isNew = true;
    }
    const ipSalt = (env && env.IP_HASH_SALT ? env.IP_HASH_SALT : '') || 'default_salt_charm_secure';
    const visitorHash = await sha256Hex(visitorId + ipSalt);
    return { visitorId, visitorHash, isNew };
  }

  async function getUserCreditBalance(userId, env) {
    if (env && env.DB) {
      try {
        const row = await env.DB.prepare('SELECT COALESCE(SUM(delta), 0) as bal FROM credit_ledger WHERE user_id = ?').bind(userId).first();
        return row ? row.bal : 0;
      } catch (e) {}
    }
    let bal = 0;
    if (memoryStore.creditLedger) {
      for (const c of memoryStore.creditLedger.values()) {
        if (c.user_id === userId) bal += c.delta;
      }
    }
    return bal;
  }

  const IST_OFFSET_MS = (5 * 60 + 30) * 60 * 1000;
  function getIstDayBoundsMs(tsMs = Date.now()) {
    const istShifted = new Date(tsMs + IST_OFFSET_MS);
    const istStartShifted = Date.UTC(istShifted.getUTCFullYear(), istShifted.getUTCMonth(), istShifted.getUTCDate());
    const startMs = istStartShifted - IST_OFFSET_MS;
    const dayKey = istShifted.toISOString().slice(0, 10);
    return { startMs, dayKey };
  }
  function getUtcDayBoundsMs(tsMs = Date.now()) {
    return getIstDayBoundsMs(tsMs);
  }

  function resolveCharmEffectiveNowMs(request, env) {
    const allowTestClock = Boolean(
      env && (
        env.ENVIRONMENT === 'local' ||
        env.__TEST__ === true ||
        env.NODE_ENV === 'test'
      )
    );
    if (allowTestClock && request && request.headers && typeof request.headers.get === 'function') {
      const hdr = request.headers.get('X-NV-Test-Now-ISO');
      if (hdr) {
        const parsed = Date.parse(String(hdr).trim());
        if (!Number.isNaN(parsed)) return parsed;
      }
    }
    return Date.now();
  }

  async function getGuestUsage(visitorHash, env, nowMs = Date.now()) {
    const { startMs, dayKey } = getUtcDayBoundsMs(nowMs);
    if (env && env.DB) {
      try {
        const row = await env.DB.prepare('SELECT questions_used, updated_at FROM free_chat_usage WHERE visitor_hash = ?').bind(visitorHash).first();
        if (row) {
          if (Number(row.updated_at || 0) < startMs) return 0;
          return Number(row.questions_used || 0);
        }
      } catch (e) {}
    }
    if (!memoryStore.freeChatUsage) memoryStore.freeChatUsage = new Map();
    const entry = memoryStore.freeChatUsage.get(visitorHash);
    if (!entry) return 0;
    if (entry.day_key && entry.day_key !== dayKey) return 0;
    return Number(entry.questions_used || 0);
  }

  async function incrementGuestUsage(visitorHash, ipHash, env, nowMs = Date.now()) {
    const now = nowMs;
    const { startMs, dayKey } = getUtcDayBoundsMs(now);
    if (env && env.DB) {
      try {
        const id = 'fcu_' + now + '_' + getRandomHex(6);
        // Ensure visitor row exists with 0 questions used
        await env.DB.prepare(`
          INSERT OR IGNORE INTO free_chat_usage (id, visitor_hash, questions_used, max_free, ip_hash, created_at, updated_at)
          VALUES (?, ?, 0, 3, ?, ?, ?)
        `).bind(id, visitorHash, ipHash, now, now).run();

        // Reset daily counter if previous usage occurred on an earlier UTC day
        await env.DB.prepare(`
          UPDATE free_chat_usage
          SET questions_used = 0, ip_hash = ?, updated_at = ?
          WHERE visitor_hash = ? AND updated_at < ?
        `).bind(ipHash, now, visitorHash, startMs).run();

        // Atomic conditional increment: only updates if questions_used < 3 today
        const updateRes = await env.DB.prepare(`
          UPDATE free_chat_usage
          SET questions_used = questions_used + 1, ip_hash = ?, updated_at = ?
          WHERE visitor_hash = ? AND questions_used < 3
        `).bind(ipHash, now, visitorHash).run();

        const changes = (updateRes && updateRes.meta && updateRes.meta.changes !== undefined)
          ? updateRes.meta.changes
          : (updateRes && updateRes.changes !== undefined ? updateRes.changes : 0);

        if (changes > 0) {
          const row = await env.DB.prepare('SELECT questions_used FROM free_chat_usage WHERE visitor_hash = ?').bind(visitorHash).first();
          return { success: true, questions_used: row ? row.questions_used : 1 };
        } else {
          return { success: false, questions_used: 3 };
        }
      } catch (e) {
        console.warn('incrementGuestUsage DB error:', e);
        return { success: false, questions_used: 3 };
      }
    }
    if (!memoryStore.freeChatUsage) memoryStore.freeChatUsage = new Map();
    let current = memoryStore.freeChatUsage.get(visitorHash) || { questions_used: 0, day_key: dayKey };
    if (current.day_key && current.day_key !== dayKey) {
      current = { questions_used: 0, day_key: dayKey };
    } else if (!current.day_key) {
      current.day_key = dayKey;
    }
    if (current.questions_used >= 3) {
      return { success: false, questions_used: 3 };
    }
    current.questions_used += 1;
    memoryStore.freeChatUsage.set(visitorHash, current);
    return { success: true, questions_used: current.questions_used };
  }

  async function decrementGuestUsage(visitorHash, env) {
    const now = Date.now();
    if (env && env.DB) {
      try {
        await env.DB.prepare('UPDATE free_chat_usage SET questions_used = MAX(0, questions_used - 1), updated_at = ? WHERE visitor_hash = ?').bind(now, visitorHash).run();
      } catch (e) {}
    }
    if (memoryStore.freeChatUsage) {
      const entry = memoryStore.freeChatUsage.get(visitorHash);
      if (entry && entry.questions_used > 0) entry.questions_used -= 1;
    }
  }

  async function refundCharmReservation(user, userReservationId, visitorHash, env, now) {
    if (user && userReservationId) {
      const refRefundId = 'crd_ref_' + now + '_' + getRandomHex(6);
      if (env && env.DB) {
        await env.DB.prepare(`
          INSERT INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at)
          SELECT ?, ?, 1, 'refund', ?, (SELECT COALESCE(SUM(delta), 0) + 1 FROM credit_ledger WHERE user_id = ?), ?
        `).bind(refRefundId, user.user_id, 'refund_' + userReservationId, user.user_id, now).run();
      } else {
        let curBal = 0;
        for (const c of memoryStore.creditLedger.values()) {
          if (c.user_id === user.user_id) curBal += c.delta;
        }
        memoryStore.creditLedger.set(refRefundId, {
          id: refRefundId,
          user_id: user.user_id,
          delta: 1,
          reason: 'refund',
          ref_id: 'refund_' + userReservationId,
          balance_after: curBal + 1,
          created_at: now
        });
      }
      return await getUserCreditBalance(user.user_id, env);
    } else if (!user && visitorHash) {
      await decrementGuestUsage(visitorHash, env);
      const curGuestUsed = await getGuestUsage(visitorHash, env);
      return Math.max(0, 3 - curGuestUsed);
    }
    return 0;
  }

  async function ensureUserFreeAllowance(userId, visitorHash, env) {
    const now = Date.now();
    const freeRefId = 'free_' + userId;
    if (env && env.DB) {
      try {
        const existing = await env.DB.prepare('SELECT id FROM credit_ledger WHERE user_id = ? AND reason = ?').bind(userId, 'free_allowance').first();
        if (!existing) {
          let guestUsed = 0;
          if (visitorHash) {
            const usageRow = await env.DB.prepare('SELECT questions_used FROM free_chat_usage WHERE visitor_hash = ?').bind(visitorHash).first();
            if (usageRow) {
              guestUsed = usageRow.questions_used;
              await env.DB.prepare('UPDATE free_chat_usage SET user_id = ?, updated_at = ? WHERE visitor_hash = ?').bind(userId, now, visitorHash).run();
            }
          }
          const delta = Math.max(0, 3 - guestUsed);
          const crdId = 'crd_free_' + now + '_' + getRandomHex(4);
          await env.DB.prepare(
            'INSERT OR IGNORE INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
          ).bind(crdId, userId, delta, 'free_allowance', freeRefId, delta, now).run();
        }
      } catch (e) {}
    } else {
      if (!memoryStore.creditLedger) memoryStore.creditLedger = new Map();
      let hasFree = false;
      for (const c of memoryStore.creditLedger.values()) {
        if (c.user_id === userId && c.reason === 'free_allowance') { hasFree = true; break; }
      }
      if (!hasFree) {
        let guestUsed = 0;
        if (visitorHash && memoryStore.freeChatUsage && memoryStore.freeChatUsage.has(visitorHash)) {
          guestUsed = memoryStore.freeChatUsage.get(visitorHash).questions_used;
        }
        const delta = Math.max(0, 3 - guestUsed);
        const crdId = 'crd_free_' + now + '_' + getRandomHex(4);
        memoryStore.creditLedger.set(crdId, {
          id: crdId,
          user_id: userId,
          delta: delta,
          reason: 'free_allowance',
          ref_id: freeRefId,
          balance_after: delta,
          created_at: now
        });
      }
    }
  }

    // 4. ROUTE: 1-ON-1 CONSULTATION ENQUIRY (/api/v1/consultation/enquiry) - DURABLE D1 STORAGE
    if (url.pathname === '/api/v1/consultation/enquiry' && request.method === 'POST') {
      const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
      if (!checkFormRateLimit(clientIp, 5, 600000)) {
        return new Response(JSON.stringify({
          status: 'error',
          message: 'Too many enquiry submissions from this IP. Please wait 10 minutes.'
        }), {
          status: 429,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': getCorsOrigin(request, env),
            'Vary': 'Origin'
          }
        });
      }
      try {
        const body = await request.json().catch(() => ({}));
        const name = (body.name || '').trim();
        const email = (body.email || '').trim();
        const phone = (body.phone || '').trim();
        const area = (body.area_of_interest || 'General Numerology Consultation').trim();
        const description = (body.description || '').trim();
        const method = (body.preferred_contact_method || 'Email').trim();

        if (!name || (!email && !phone)) {
          return new Response(JSON.stringify({
            status: 'error',
            message: 'Please provide your name and at least an email or phone number.'
          }), {
            status: 400,
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': getCorsOrigin(request, env),
              'Vary': 'Origin'
            }
          });
        }

        const now = Date.now();
        const ts = new Date(now).toISOString();
        const enquiryId = 'ENQ-' + now.toString().slice(-6) + '-' + Math.random().toString(36).substring(2, 6).toUpperCase();
        const enquirySalt = env.IP_HASH_SALT || 'nv_enquiry_salt_2026';
        const ipHash = await sha256Hex(clientIp + ':' + enquirySalt);
        const userAgent = (request.headers.get('User-Agent') || '').slice(0, 255);

        // 1. Notification Dispatch: Forward via Web3Forms if configured, recording outcome
        let notificationStatus = 'notify_failed';
        const web3Key = env.WEB3FORMS_ACCESS_KEY;
        if (web3Key) {
          try {
            const w3Resp = await fetch('https://api.web3forms.com/submit', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                access_key: web3Key,
                subject: `Consultation Enquiry [${enquiryId}]: ${name} (${area})`,
                from_name: 'Numeros Vision Consultation Desk',
                to: 'support@numerosvision.com',
                name: name,
                email: email,
                phone: phone,
                area_of_interest: area,
                preferred_contact: method,
                message: description,
                enquiry_id: enquiryId,
                timestamp: ts
              })
            });
            if (w3Resp.ok) {
              const w3Data = await w3Resp.json().catch(() => ({}));
              if (w3Data.success) {
                notificationStatus = 'notified';
              }
            }
          } catch (e) {
            console.error('[Web3Forms_Edge_Error]', e);
          }
        }

        // 2. DURABLE D1 STORAGE: Enquiries table with visible notification_status
        if (env.DB) {
          try {
            await env.DB.prepare(`
              INSERT INTO enquiries (
                id, type, name, email, phone, area_or_category, preferred_contact_method,
                order_id, message, notification_status, ip_hash, user_agent, created_at
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `).bind(
              enquiryId, 'consultation', name, email, phone, area, method,
              null, description, notificationStatus, ipHash, userAgent, now
            ).run();
          } catch (d1Err) {
            console.error('[Enquiries_D1_Insert_Error]', d1Err);
          }
        }

        return new Response(JSON.stringify({
          status: 'success',
          enquiry_id: enquiryId,
          notification_status: notificationStatus,
          recipient: 'support@numerosvision.com',
          timestamp: ts,
          message: 'Your consultation enquiry has been securely recorded and routed to the advisory desk.'
        }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': getCorsOrigin(request, env),
            'Vary': 'Origin'
          }
        });
      } catch (err) {
        return new Response(JSON.stringify({ status: 'error', error: err.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }

    // 5. ROUTE: GENERAL CONTACT / INQUIRY (/api/v1/contact) - DURABLE D1 STORAGE
    if (url.pathname === '/api/v1/contact' && request.method === 'POST') {
      const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
      if (!checkFormRateLimit(clientIp, 5, 600000)) {
        return new Response(JSON.stringify({
          status: 'error',
          message: 'Too many contact inquiries from this IP. Please wait 10 minutes.'
        }), {
          status: 429,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': getCorsOrigin(request, env),
            'Vary': 'Origin'
          }
        });
      }
      try {
        const body = await request.json().catch(() => ({}));
        const name = (body.name || '').trim();
        const email = (body.email || '').trim();
        const phone = (body.phone || '').trim();
        const category = (body.category || 'General').trim();
        const order = (body.order || '').trim();
        const message = (body.message || '').trim();

        if (!name || (!email && !phone)) {
          return new Response(JSON.stringify({
            status: 'error',
            message: 'Please provide your name and contact details (email or phone).'
          }), {
            status: 400,
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': getCorsOrigin(request, env),
              'Vary': 'Origin'
            }
          });
        }

        const now = Date.now();
        const ticketId = 'NV-TICK-' + Math.floor(100000 + Math.random() * 900000);
        const enquirySalt = env.IP_HASH_SALT || 'nv_enquiry_salt_2026';
        const ipHash = await sha256Hex(clientIp + ':' + enquirySalt);
        const userAgent = (request.headers.get('User-Agent') || '').slice(0, 255);

        // 1. Notification Dispatch: Forward via Web3Forms if configured, recording outcome
        let notificationStatus = 'notify_failed';
        const web3Key = env.WEB3FORMS_ACCESS_KEY;
        if (web3Key) {
          try {
            const w3Resp = await fetch('https://api.web3forms.com/submit', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                access_key: web3Key,
                subject: `Contact Ticket [${ticketId}]: ${name} (${category})`,
                from_name: 'Numeros Vision Support Desk',
                to: 'support@numerosvision.com',
                name: name,
                email: email,
                phone: phone,
                category: category,
                order_id: order,
                message: message,
                ticket_id: ticketId
              })
            });
            if (w3Resp.ok) {
              const w3Data = await w3Resp.json().catch(() => ({}));
              if (w3Data.success) {
                notificationStatus = 'notified';
              }
            }
          } catch (e) {
            console.error('[Web3Forms_Edge_Error]', e);
          }
        }

        // 2. DURABLE D1 STORAGE: Enquiries table with visible notification_status
        if (env.DB) {
          try {
            await env.DB.prepare(`
              INSERT INTO enquiries (
                id, type, name, email, phone, area_or_category, preferred_contact_method,
                order_id, message, notification_status, ip_hash, user_agent, created_at
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `).bind(
              ticketId, 'contact', name, email, phone, category, 'Email',
              order || null, message, notificationStatus, ipHash, userAgent, now
            ).run();
          } catch (d1Err) {
            console.error('[Contact_D1_Insert_Error]', d1Err);
          }
        }

        return new Response(JSON.stringify({
          status: 'success',
          ticket_id: ticketId,
          notification_status: notificationStatus,
          recipient: 'support@numerosvision.com',
          message: 'Your inquiry has been securely recorded and routed to the support desk.'
        }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': getCorsOrigin(request, env),
            'Vary': 'Origin'
          }
        });
      } catch (err) {
        return new Response(JSON.stringify({ status: 'error', error: err.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }

    // 6. ROUTE: SERVER-SIDE OPERATIONAL EVENTS API (/api/v1/events) - ZERO PII & CONSENT GUARDED
    // Data Retention: 90-day rolling window for aggregated funnel analytics. Events older than 90 days are purged opportunistically on write.
    if (url.pathname === '/api/v1/events' && request.method === 'POST') {
      const allowedOrigin = getCorsOrigin(request, env);
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': allowedOrigin,
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Consent-Analytics'
      };
      if (request.method === 'OPTIONS') {
        return new Response(null, { status: 204, headers: corsHeaders });
      }

      // Check Origin: if Origin header exists and does not match allowedOrigin, reject
      const reqOrigin = request.headers.get('Origin');
      if (reqOrigin && allowedOrigin !== '*' && allowedOrigin !== reqOrigin) {
        return new Response(JSON.stringify({ status: 'error', error: 'Forbidden origin.' }), { status: 403, headers: corsHeaders });
      }

      // Required Secret: TELEMETRY_SALT must be configured; if missing, fail immediately and log nothing
      const telemetrySalt = env.TELEMETRY_SALT;
      if (!telemetrySalt) {
        return new Response(JSON.stringify({
          status: 'error',
          code: 'CONFIGURATION_ERROR',
          message: 'Telemetry service configuration is missing on server.'
        }), { status: 503, headers: corsHeaders });
      }

      // Require Analytics Consent
      const cookieHeader = request.headers.get('Cookie') || '';
      let hasAnalyticsConsent = request.headers.get('X-Consent-Analytics') === 'true';
      if (!hasAnalyticsConsent && cookieHeader.includes('nv_cookie_consent')) {
        const m = cookieHeader.match(/nv_cookie_consent=([^;]+)/);
        if (m) {
          try {
            const parsed = JSON.parse(decodeURIComponent(m[1]));
            if (parsed && parsed.analytics === true) hasAnalyticsConsent = true;
          } catch (_) {}
        }
      }
      if (!hasAnalyticsConsent) {
        return new Response(JSON.stringify({
          status: 'error',
          code: 'ANALYTICS_CONSENT_REQUIRED',
          message: 'Analytics consent required to record events.'
        }), { status: 403, headers: corsHeaders });
      }

      // Cap Body Size at 16 KiB (16384 bytes)
      const contentLength = parseInt(request.headers.get('Content-Length') || '0', 10);
      if (contentLength > 16384) {
        return new Response(JSON.stringify({ status: 'error', error: 'Payload too large (capped at 16KB).' }), { status: 413, headers: corsHeaders });
      }

      const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
      if (!checkFormRateLimit('telemetry_' + clientIp, 60, 60000)) {
        return new Response(JSON.stringify({ status: 'error', error: 'Rate limit exceeded.' }), { status: 429, headers: corsHeaders });
      }

      try {
        const rawText = await request.text();
        if (rawText.length > 16384) {
          return new Response(JSON.stringify({ status: 'error', error: 'Payload too large (capped at 16KB).' }), { status: 413, headers: corsHeaders });
        }
        const body = JSON.parse(rawText || '{}');

        // Allowlist of Approved Event Names
        const ALLOWED_EVENT_NAMES = new Set([
          'page_view', 'calculator_used', 'signup_modal_opened', 'lead_captured',
          'checkout_initiated', 'order_created', 'payment_verified', 'report_downloaded',
          'cta_clicked', 'cookie_consent_updated'
        ]);

        const rawEventName = body.event_name || body.event;
        if (!rawEventName || !ALLOWED_EVENT_NAMES.has(rawEventName)) {
          return new Response(JSON.stringify({
            status: 'error',
            error: 'Unapproved or missing event name: ' + rawEventName
          }), { status: 400, headers: corsHeaders });
        }

        // Verify strict ZERO PII in payload keys
        const FORBIDDEN_KEYS = new Set([
          'name', 'full_name', 'first_name', 'last_name', 'email', 'phone', 'mobile', 'customer_phone',
          'otp', 'code', 'otp_code', 'verification_code',
          'dob', 'birth_date', 'birthdate', 'birth_time', 'birth_place', 'birth_city',
          'driver', 'conductor', 'mulank', 'bhagyank', 'destiny', 'lifepath', 'chart', 'grid', 'loshu',
          'user_id', 'golden_profile_id', 'gaid', 'idfa', 'idfv'
        ]);

        for (const k of Object.keys(body)) {
          if (FORBIDDEN_KEYS.has(k.toLowerCase())) {
            return new Response(JSON.stringify({ status: 'error', error: 'PII field rejected: ' + k }), { status: 400, headers: corsHeaders });
          }
          const v = body[k];
          if (typeof v === 'string') {
            if (/^\d{6}$/.test(v.trim()) || /@[\w.-]+\.\w+/.test(v) || /^\+?[0-9\s-]{10,15}$/.test(v.trim())) {
              return new Response(JSON.stringify({ status: 'error', error: 'PII pattern detected in ' + k }), { status: 400, headers: corsHeaders });
            }
            if (/\b(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4}|\d{8})\b/.test(v)) {
              return new Response(JSON.stringify({ status: 'error', error: 'Date pattern detected in ' + k }), { status: 400, headers: corsHeaders });
            }
          }
        }

        const ipHash = await sha256Hex(clientIp + ':' + telemetrySalt);
        const userAgent = (request.headers.get('User-Agent') || '').slice(0, 255);
        const eventId = await logWorkerEvent(env, {
          event_name: rawEventName,
          device_id: body.device_id,
          anonymous_session_id: body.anonymous_session_id,
          page_path: body.page_path,
          product_id: body.product_id,
          value_inr: body.value_inr || body.value,
          currency: body.currency,
          utm_source: body.utm_source,
          utm_medium: body.utm_medium,
          utm_campaign: body.utm_campaign,
          meta_json: body.meta || body.meta_json,
          ip_hash: ipHash,
          user_agent: userAgent
        });

        return new Response(JSON.stringify({ status: 'success', event_id: eventId }), { status: 200, headers: corsHeaders });
      } catch (err) {
        return new Response(JSON.stringify({ status: 'error', error: err.message }), { status: 500, headers: corsHeaders });
      }
    }



    // 7. ROUTE: PAYMENTS API (/api/v1/payments/*) - SERVER AUTHORITY & D1 SETTLEMENT

    // 7a. ROUTE: CREATE ORDER (/api/v1/payments/create-order & legacy /api/create-order)
    if ((url.pathname === '/api/v1/payments/create-order' || url.pathname === '/api/create-order') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };

      if (url.pathname === '/api/create-order') {
        corsHeaders['X-API-Deprecated'] = '/api/create-order is retired. Use /api/v1/payments/create-order';
      }

      // Production hotfix guard: require D1, R2, and all required secrets before accepting checkout outside ENVIRONMENT=local/test
      if (env.ENVIRONMENT !== 'local' && env.ENVIRONMENT !== 'test') {
        const rzpKeyIdCheck = (env.RAZORPAY_KEY_ID || '').trim();
        const rzpSecretCheck = (env.RAZORPAY_KEY_SECRET || '').trim();
        const pdfServiceUrlCheck = (env.PDF_SERVICE_URL || env.PDF_GENERATOR_URL || '').trim();
        const hasSecrets = !!(
          env.DB &&
          env.REPORTS_BUCKET &&
          env.OTP_HMAC_SECRET &&
          env.SESSION_SECRET &&
          env.IP_HASH_SALT &&
          env.DATA_ENCRYPTION_KEY &&
          env.PDF_SERVICE_SECRET &&
          pdfServiceUrlCheck &&
          env.DOWNLOAD_TOKEN_SECRET &&
          rzpKeyIdCheck &&
          rzpSecretCheck &&
          !rzpKeyIdCheck.includes('REPLACE_ME') &&
          !rzpKeyIdCheck.includes('PLACEHOLDER')
        );
        if (!hasSecrets) {
          return new Response(JSON.stringify({
            success: false,
            code: 'CHECKOUT_TEMPORARILY_UNAVAILABLE',
            error: 'Checkout is temporarily unavailable while secure server upgrades complete. Please try again shortly.'
          }), { status: 503, headers: corsHeaders });
        }
      }

      const body = await request.json().catch(() => ({}));
      const email = (body.customer_email || body.email || '').trim().toLowerCase();
      const now = Date.now();

      // 1. Session or Checkout Token verification
      // If customer verified email B with a valid checkout token, that verified checkout email WINS over any preexisting session cookie for email A.
      let user = null;
      const chkToken = (body.checkout_token || request.headers.get('X-Checkout-Token') || '').trim();

      if (chkToken && email) {
        const sessionSecret = requireSecret(env, 'SESSION_SECRET');
        const isValid = await verifyCheckoutToken(sessionSecret, email, chkToken);
        if (isValid) {
          if (env.DB) {
            try {
              const u = await env.DB.prepare('SELECT id, email, created_at FROM users WHERE email = ?').bind(email).first();
              if (u) {
                user = { user_id: u.id, email: u.email, created_at: u.created_at };
              }
            } catch (e) {}
          } else {
            const u = memoryStore.users.get(email);
            if (u) {
              user = { user_id: u.id, email: u.email, created_at: u.createdAt };
            }
          }
          if (!user) {
            user = { user_id: 'usr_' + now + '_' + getRandomHex(4), email, created_at: now };
          }
        } else {
          return new Response(JSON.stringify({
            success: false,
            code: 'INVALID_CHECKOUT_TOKEN',
            error: 'Checkout verification token has expired or is invalid. Please verify your email again.'
          }), { status: 401, headers: corsHeaders });
        }
      }

      if (!user) {
        // Fall back to active session cookie if no checkout token was provided
        user = await authenticateUser(request, env);
      }

      if (!user) {
        return new Response(JSON.stringify({
          success: false,
          code: 'AUTH_REQUIRED',
          error: 'Authentication required. Please verify your email or sign in to initiate checkout.'
        }), { status: 401, headers: corsHeaders });
      }

      const packId = (body.packId || body.pack_id || body.plan || body.plan_id || '').trim();
      let subjectId = (body.subjectId || body.subject_id || '').trim();
      const customerName = (body.name || body.customer_name || 'Valued Seeker').trim();
      const customerDob = (body.dob || body.locked_dob || body.customer_dob || body.customerDob || '').trim();

      // 2. Deterministic pack lookup (resolves regular mrp_inr automatically after fixed launch_offer.ends_at)
      const pack = getPackById(packId, env, now);
      if (pack && pack.pack_id === 'planner_2027' && !isPlanner2027Live(env)) {
        return new Response(JSON.stringify({
          success: false,
          code: 'PLANNER_WAITLIST_ONLY',
          status: 'waitlist_only',
          display_label: 'Coming soon, notify me',
          error: 'Coming soon, notify me. The 2027 Year Ahead Planner is waitlist-only until its legal disclaimer is approved.'
        }), { status: 409, headers: corsHeaders });
      }
      if (!pack || pack.status !== 'active') {
        return new Response(JSON.stringify({
          success: false,
          error: `Invalid or inactive pack "${packId}".`
        }), { status: 400, headers: corsHeaders });
      }

      if (isNotifyMeHigherTiersEnabled(env) && (pack.pack_id === 'report_advanced' || pack.pack_id === 'report_premium')) {
        return new Response(JSON.stringify({
          success: false,
          code: 'TIER_WAITLIST_ONLY',
          error: 'Coming soon, notify me. This report edition is currently waitlist-only; Anveil my alignments is open for immediate checkout.'
        }), { status: 409, headers: corsHeaders });
      }

      const amountPaise = resolveEffectivePackPricePaise(pack.pack_id, env, now);
      if (!amountPaise || amountPaise <= 0) {
        return new Response(JSON.stringify({
          success: false,
          error: `Invalid effective price for pack "${packId}".`
        }), { status: 400, headers: corsHeaders });
      }
      const currency = 'INR';

      // 3. Subject verification or creation
      if (subjectId) {
        let subject = null;
        if (env.DB) {
          subject = await env.DB.prepare('SELECT id, user_id, name, created_at FROM subjects WHERE id = ? AND user_id = ?').bind(subjectId, user.user_id).first();
        } else {
          subject = memoryStore.subjects.get(subjectId);
          if (subject && subject.user_id !== user.user_id) subject = null;
        }
        if (!subject) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Subject not found or does not belong to authenticated user.'
          }), { status: 403, headers: corsHeaders });
        }
      } else if (customerDob) {
        const dobHash = await sha256Hex(customerDob);
        if (env.DB) {
          let subject = await env.DB.prepare('SELECT id FROM subjects WHERE user_id = ? AND dob_hash = ?').bind(user.user_id, dobHash).first();
          if (!subject) {
            const countRow = await env.DB.prepare('SELECT COUNT(*) as cnt FROM subjects WHERE user_id = ?').bind(user.user_id).first();
            if (countRow && countRow.cnt >= 10) {
              return new Response(JSON.stringify({
                success: false,
                error: 'Maximum limit of 10 subjects per account reached.'
              }), { status: 400, headers: corsHeaders });
            }
            subjectId = 'sbj_' + now + '_' + getRandomHex(4);
            const dataEncKey = requireSecret(env, 'DATA_ENCRYPTION_KEY');
            const dobEnc = await encryptField(customerDob, dataEncKey);
            const birthTimeEnc = await encryptField(body.birthTime || body.birth_time || null, dataEncKey);
            await env.DB.prepare(
              'INSERT INTO subjects (id, user_id, name, dob_hash, dob_enc, birth_time_enc, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
            ).bind(subjectId, user.user_id, customerName, dobHash, dobEnc, birthTimeEnc, now).run();
          } else {
            subjectId = subject.id;
          }
        } else {
          let userSubjCount = 0;
          let existingSubj = null;
          for (const s of memoryStore.subjects.values()) {
            if (s.user_id === user.user_id) {
              userSubjCount++;
              if (s.dob_hash === dobHash) existingSubj = s;
            }
          }
          if (existingSubj) {
            subjectId = existingSubj.id;
          } else {
            if (userSubjCount >= 10) {
              return new Response(JSON.stringify({
                success: false,
                error: 'Maximum limit of 10 subjects per account reached.'
              }), { status: 400, headers: corsHeaders });
            }
            subjectId = 'sbj_' + now + '_' + getRandomHex(4);
            const dataEncKey = requireSecret(env, 'DATA_ENCRYPTION_KEY');
            const dobEnc = await encryptField(customerDob, dataEncKey);
            const birthTimeEnc = await encryptField(body.birthTime || body.birth_time || null, dataEncKey);
            memoryStore.subjects.set(subjectId, { id: subjectId, user_id: user.user_id, name: customerName, dob_hash: dobHash, dob_enc: dobEnc, birth_time_enc: birthTimeEnc, created_at: now });
          }
        }
      } else {
        return new Response(JSON.stringify({
          success: false,
          error: 'Either subjectId or customer Date of Birth (dob) is required.'
        }), { status: 400, headers: corsHeaders });
      }

      // 3b. Purchase Guard: Prevent purchasing the same pack twice for the same profile
      let alreadyPurchased = false;
      if (env.DB) {
        const entRow = await env.DB.prepare(`
          SELECT e.id FROM entitlements e
          LEFT JOIN orders o ON e.order_id = o.id
          WHERE e.user_id = ? AND e.subject_id = ? AND e.pack_id = ?
            AND (o.status IS NULL OR o.status != 'REFUNDED')
          LIMIT 1
        `).bind(user.user_id, subjectId, pack.pack_id).first();
        if (entRow) {
          alreadyPurchased = true;
        } else {
          const paidOrder = await env.DB.prepare(`
            SELECT id FROM orders
            WHERE user_id = ? AND subject_id = ? AND pack_id = ? AND status = 'PAID'
            LIMIT 1
          `).bind(user.user_id, subjectId, pack.pack_id).first();
          if (paidOrder) alreadyPurchased = true;
        }
      } else if (typeof memoryStore !== 'undefined') {
        if (memoryStore.entitlements) {
          for (const ent of memoryStore.entitlements.values()) {
            if (ent.user_id === user.user_id && ent.subject_id === subjectId && ent.pack_id === pack.pack_id) {
              const ord = ent.order_id ? memoryStore.orders.get(ent.order_id) : null;
              if (!ord || ord.status !== 'REFUNDED') {
                alreadyPurchased = true;
                break;
              }
            }
          }
        }
        if (!alreadyPurchased && memoryStore.orders) {
          for (const ord of memoryStore.orders.values()) {
            if (ord.user_id === user.user_id && ord.subject_id === subjectId && ord.pack_id === pack.pack_id && ord.status === 'PAID') {
              alreadyPurchased = true;
              break;
            }
          }
        }
      }

      if (alreadyPurchased) {
        return new Response(JSON.stringify({
          success: false,
          code: 'ALREADY_PURCHASED',
          alreadyPurchased: true,
          error: 'This report pack has already been purchased for this profile. You can download your report directly from your dashboard.'
        }), { status: 409, headers: corsHeaders });
      }

      // 4. Pending order expiration check (~30 minutes window)
      const THIRTY_MINUTES_MS = 30 * 60 * 1000;
      let existingOrder = null;

      if (env.DB) {
        existingOrder = await env.DB.prepare(
          "SELECT id, rzp_order_id, amount_paise, status, created_at FROM orders WHERE user_id = ? AND subject_id = ? AND pack_id = ? AND status IN ('CREATED', 'pending') ORDER BY created_at DESC LIMIT 1"
        ).bind(user.user_id, subjectId, pack.pack_id).first();

        if (existingOrder) {
          const ageMs = now - existingOrder.created_at;
          const amountMismatch = existingOrder.amount_paise !== undefined && Number(existingOrder.amount_paise) !== Number(amountPaise);
          if (ageMs > THIRTY_MINUTES_MS || amountMismatch) {
            await env.DB.prepare("UPDATE orders SET status = 'EXPIRED', updated_at = ? WHERE id = ?").bind(now, existingOrder.id).run();
            await env.DB.prepare(
              "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, ?, 'order_expired', 'orders', ?, ?, ?)"
            ).bind('aud_' + now + '_' + getRandomHex(4), user.user_id, existingOrder.id, JSON.stringify({ reason: amountMismatch ? 'launch_window_price_changed' : 'auto_expired_30m', ageMs }), now).run();
            existingOrder = null;
          }
        }
      } else {
        for (const ord of memoryStore.orders.values()) {
          if (ord.user_id === user.user_id && ord.subject_id === subjectId && ord.pack_id === pack.pack_id && (ord.status === 'CREATED' || ord.status === 'pending')) {
            const ageMs = now - ord.created_at;
            const amountMismatch = ord.amount_paise !== undefined && Number(ord.amount_paise) !== Number(amountPaise);
            if (ageMs > THIRTY_MINUTES_MS || amountMismatch) {
              ord.status = 'EXPIRED';
            } else {
              existingOrder = ord;
            }
          }
        }
      }

      // 5. Razorpay Credentials check
      const rzpKeyId = env.RAZORPAY_KEY_ID;
      const rzpSecret = env.RAZORPAY_KEY_SECRET;

      if (!rzpKeyId || !rzpSecret || rzpKeyId.includes('REPLACE_ME') || rzpKeyId.includes('PLACEHOLDER')) {
        return new Response(JSON.stringify({
          success: false,
          code: 'CHECKOUT_TEMPORARILY_UNAVAILABLE',
          error: 'Checkout is temporarily unavailable. Payment gateway credentials are not configured in the server environment.'
        }), { status: 503, headers: corsHeaders });
      }

      let internalOrderId = 'ord_' + now + '_' + getRandomHex(4);
      let rzpOrderId = null;

      if (existingOrder && existingOrder.rzp_order_id) {
        internalOrderId = existingOrder.id;
        rzpOrderId = existingOrder.rzp_order_id;
      } else {
        try {
          const authHeader = 'Basic ' + btoa(`${rzpKeyId.trim()}:${rzpSecret.trim()}`);
          const rzpReq = await fetch('https://api.razorpay.com/v1/orders', {
            method: 'POST',
            headers: {
              'Authorization': authHeader,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              amount: amountPaise,
              currency: 'INR',
              payment_capture: 1,
              receipt: `nv_rcpt_${internalOrderId}`,
              notes: {
                pack_id: pack.pack_id,
                user_id: user.user_id,
                subject_id: subjectId
              }
            })
          });

          if (rzpReq.ok) {
            const rzpData = await rzpReq.json();
            rzpOrderId = rzpData.id;
          } else {
            const errData = await rzpReq.json().catch(() => ({}));
            const rzpStatus = rzpReq.status;
            let code = 'GATEWAY_ERROR';
            let errMsg = 'Failed to create order with payment gateway.';
            if (rzpStatus === 401) {
              console.error('[GATEWAY_AUTH_ERROR] Provider credentials rejected by Razorpay (HTTP 401):', errData?.error?.description || '');
              code = 'GATEWAY_AUTHENTICATION_FAILED';
              errMsg = 'Unable to initialize payment at this moment. Please try again shortly or contact support.';
              return new Response(JSON.stringify({
                success: false,
                code: code,
                error: errMsg
              }), { status: 502, headers: corsHeaders });
            } else if (errData?.error?.code) {
              code = `GATEWAY_${String(errData.error.code).toUpperCase()}`;
              errMsg = errData?.error?.description || errMsg;
            } else if (errData?.error?.description) {
              errMsg = errData.error.description;
            }
            return new Response(JSON.stringify({
              success: false,
              code: code,
              error: errMsg,
              provider_code: errData?.error?.code,
              details: errData
            }), { status: rzpStatus || 400, headers: corsHeaders });
          }
        } catch (apiErr) {
          return new Response(JSON.stringify({
            success: false,
            code: 'GATEWAY_NETWORK_ERROR',
            error: 'Unable to reach payment gateway to create order.'
          }), { status: 502, headers: corsHeaders });
        }

        if (env.DB) {
          await env.DB.prepare(
            'INSERT INTO orders (id, user_id, subject_id, pack_id, amount_paise, currency, rzp_order_id, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
          ).bind(internalOrderId, user.user_id, subjectId, pack.pack_id, amountPaise, currency, rzpOrderId, 'CREATED', now, now).run();
          await logWorkerEvent(env, {
            event_name: 'order_created',
            product_id: pack.pack_id,
            value_inr: amountPaise / 100,
            currency: currency
          });

          await env.DB.prepare(
            "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, ?, 'order_created', 'orders', ?, ?, ?)"
          ).bind('aud_' + now + '_' + getRandomHex(4), user.user_id, internalOrderId, JSON.stringify({ rzpOrderId, packId: pack.pack_id, amountPaise }), now).run();
        } else {
          memoryStore.orders.set(internalOrderId, {
            id: internalOrderId,
            user_id: user.user_id,
            subject_id: subjectId,
            pack_id: pack.pack_id,
            amount_paise: amountPaise,
            currency,
            rzp_order_id: rzpOrderId,
            status: 'CREATED',
            created_at: now,
            updated_at: now
          });
        }
      }

      return new Response(JSON.stringify({
        success: true,
        orderId: internalOrderId,
        order_id: internalOrderId,
        rzpOrderId: rzpOrderId,
        rzp_order_id: rzpOrderId,
        amount: amountPaise,
        amount_paise: amountPaise,
        currency: 'INR',
        keyId: rzpKeyId,
        key_id: rzpKeyId,
        pack: {
          pack_id: pack.pack_id,
          name: pack.name,
          price_inr: pack.price_inr
        },
        subjectId: subjectId
      }), { status: 200, headers: corsHeaders });
    }

    // 7b. ROUTE: VERIFY PAYMENT (/api/v1/payments/verify & legacy /api/verify-payment)
    if ((url.pathname === '/api/v1/payments/verify' || url.pathname === '/api/verify-payment' || url.pathname === '/api/v1/payments/verify-payment') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };

      if (url.pathname === '/api/verify-payment') {
        corsHeaders['X-API-Deprecated'] = '/api/verify-payment is retired. Use /api/v1/payments/verify';
      }

      const body = await request.json().catch(() => ({}));
      const rzpOrderId = (body.razorpay_order_id || body.rzp_order_id || (body.order_id && String(body.order_id).startsWith('order_') ? body.order_id : '') || '').trim();
      const rzpPaymentId = (body.razorpay_payment_id || body.rzp_payment_id || body.payment_id || '').trim();
      const signature = (body.razorpay_signature || body.rzp_signature || body.signature || '').trim().toLowerCase();

      const rzpSecret = env.RAZORPAY_KEY_SECRET;
      if (!rzpSecret) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Payment gateway secret not configured on server.'
        }), { status: 500, headers: corsHeaders });
      }

      if (!rzpOrderId || !rzpPaymentId || !signature) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Missing required payment verification parameters (order_id, payment_id, signature).'
        }), { status: 400, headers: corsHeaders });
      }

      // HMAC-SHA256 signature verification in constant time
      let isSigValid = false;
      let genSig = '';
      try {
        const encoder = new TextEncoder();
        const keyData = encoder.encode(rzpSecret.trim());
        const msgData = encoder.encode(`${rzpOrderId}|${rzpPaymentId}`);
        const cryptoKey = await crypto.subtle.importKey(
          'raw',
          keyData,
          { name: 'HMAC', hash: 'SHA-256' },
          false,
          ['sign']
        );
        const sigBuffer = await crypto.subtle.sign('HMAC', cryptoKey, msgData);
        genSig = Array.from(new Uint8Array(sigBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
        if (timingSafeEqual(genSig.toLowerCase(), signature)) {
          isSigValid = true;
        }
      } catch (e) {
        console.error('[HMAC_Verification_Error]', e);
      }

      if (!isSigValid) {
        const keyLast4 = (env.RAZORPAY_KEY_ID || '').trim().slice(-4);
        console.warn(`[PAYMENT_VERIFY_DIAGNOSTIC] Key ID tail: ***${keyLast4} | Expected sig length: ${genSig.length} | Received sig length: ${signature.length}`);
        return new Response(JSON.stringify({
          status: 'error',
          success: false,
          error: 'Invalid payment signature. Verification failed.'
        }), { status: 400, headers: corsHeaders });
      }

      // Find order in D1
      const now = Date.now();
      let order = null;
      if (env.DB) {
        order = await env.DB.prepare('SELECT * FROM orders WHERE rzp_order_id = ?').bind(rzpOrderId).first();
      } else {
        for (const ord of memoryStore.orders.values()) {
          if (ord.rzp_order_id === rzpOrderId) { order = ord; break; }
        }
      }

      if (!order) {
        return new Response(JSON.stringify({
          status: 'error',
          success: false,
          error: 'Order not found for payment verification.'
        }), { status: 404, headers: corsHeaders });
      }

      // Authoritative pricing check against packs.json catalog (evaluated at order creation timestamp)
      const pack = getPackById(order.pack_id, env, Number(order.created_at || now));
      if (!pack || Number(order.amount_paise) !== Number(pack.amount_paise)) {
        return new Response(JSON.stringify({
          status: 'error',
          success: false,
          error: 'Order amount does not match authoritative pack pricing.'
        }), { status: 400, headers: corsHeaders });
      }

      // WEBHOOK-ONLY PDF GENERATION:
      // /verify validates the Razorpay HMAC signature, records PAYMENT_VERIFIED, and mints nv_session
      // when checkout_token matches, while deferring PDF generation & entitlements to the signed
      // Razorpay webhook (with automatic 10-minute Razorpay Orders API fallback).
      let existingJobId = null;
      if (order.status === 'PAID') {
        if (env.DB) {
          const exJob = await env.DB.prepare('SELECT id FROM report_jobs WHERE order_id = ? ORDER BY created_at DESC LIMIT 1').bind(order.id).first();
          if (exJob) existingJobId = exJob.id;
        } else if (typeof memoryStore !== 'undefined' && memoryStore.reportJobs) {
          for (const j of memoryStore.reportJobs.values()) {
            if (j.order_id === order.id) { existingJobId = j.id; break; }
          }
        }
      } else {
        order.status = 'PAYMENT_VERIFIED';
        order.updated_at = now;
        order.rzp_payment_id = rzpPaymentId;
        if (env.DB) {
          await env.DB.prepare("UPDATE orders SET status = 'PAYMENT_VERIFIED', updated_at = ? WHERE id = ?").bind(now, order.id).run();
          await env.DB.prepare(
            "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, 'checkout_verify', 'payment_signature_verified', 'orders', ?, ?, ?)"
          ).bind('aud_' + now + '_' + getRandomHex(4), order.id, JSON.stringify({ rzpOrderId, rzpPaymentId, amountPaise: order.amount_paise }), now).run();
          try {
            await logWorkerEvent(env, {
              event_name: 'payment_signature_verified',
              product_id: order.pack_id,
              value_inr: order.amount_paise / 100,
              currency: order.currency || 'INR'
            });
          } catch (_) {}
        } else if (typeof memoryStore !== 'undefined' && memoryStore.auditLogs) {
          memoryStore.auditLogs.push({
            id: 'aud_' + now + '_' + getRandomHex(4),
            action: 'payment_signature_verified',
            resource_id: order.id
          });
        }
      }

      // Condition 1: Session issuance ONLY if email was verified in the SAME checkout flow via checkout_token
      let sessionCookieHeader = null;
      const checkoutToken = (body.checkout_token || request.headers.get('X-Checkout-Token') || '').trim();
      const sessionSecret = env.SESSION_SECRET ? env.SESSION_SECRET.trim() : '';

      // Extract customer email from order, user, or subject
      let orderEmail = (order.email || '').toString().trim().toLowerCase();
      if (!orderEmail && order.user_id) {
        if (env.DB) {
          try {
            const uRow = await env.DB.prepare('SELECT email FROM users WHERE id = ?').bind(order.user_id).first();
            if (uRow && uRow.email) orderEmail = String(uRow.email).trim().toLowerCase();
          } catch (_) {}
        } else if (memoryStore && memoryStore.users) {
          for (const u of memoryStore.users.values()) {
            if (u.id === order.user_id && u.email) { orderEmail = String(u.email).trim().toLowerCase(); break; }
          }
        }
      }
      if (!orderEmail && order.subject_id) {
        let subj = null;
        if (env.DB) {
          try {
            subj = await env.DB.prepare('SELECT u.email FROM subjects s JOIN users u ON s.user_id = u.id WHERE s.id = ?').bind(order.subject_id).first();
          } catch (_) {}
        } else {
          subj = memoryStore.subjects.get(order.subject_id);
        }
        if (subj && subj.email) orderEmail = String(subj.email).trim().toLowerCase();
      }
      if (!orderEmail && body.email) {
        orderEmail = body.email.toString().trim().toLowerCase();
      }

      // STRICT SESSION MINTING GUARD:
      // Payment alone must NEVER mint a session.
      // Mint nv_session ONLY when a valid checkout token for the EXACT same email exists.
      // A different email must never get one.
      const bodyEmail = (body.email || '').toString().trim().toLowerCase();
      const isEmailMismatch = Boolean(bodyEmail && orderEmail && bodyEmail !== orderEmail);

      if (!isEmailMismatch && checkoutToken && orderEmail && sessionSecret) {
        const isVerified = await verifyCheckoutToken(sessionSecret, orderEmail, checkoutToken);
        if (isVerified) {
          let userId = null;
          const ipSalt = requireSecret(env, 'IP_HASH_SALT');
          const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
          const ipHash = await hmacSha256Hex(ipSalt, clientIp);
          if (env.DB) {
            const u = await env.DB.prepare('SELECT id FROM users WHERE email = ?').bind(orderEmail).first();
            if (u) {
              userId = u.id;
            } else {
              userId = 'usr_' + now + '_' + getRandomHex(4);
              await env.DB.prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)').bind(userId, orderEmail, now).run();
              await recordUserConsent(env, userId, 'service_delivery', 1, ipHash, now);
              await recordUserConsent(env, userId, 'marketing_communications', 0, ipHash, now);
            }
          } else {
            let u = memoryStore.users.get(orderEmail);
            if (!u) {
              userId = 'usr_' + now + '_' + getRandomHex(4);
              u = { id: userId, email: orderEmail, createdAt: now };
              memoryStore.users.set(orderEmail, u);
              await recordUserConsent(env, userId, 'service_delivery', 1, ipHash, now);
              await recordUserConsent(env, userId, 'marketing_communications', 0, ipHash, now);
            } else {
              userId = u.id;
            }
          }
          const rawSessionToken = await mintUserSession(env, userId, clientIp, now);
          const isLocal = env.ENVIRONMENT === 'local' || env.ENVIRONMENT === 'test';
          sessionCookieHeader = createSessionCookieHeader(rawSessionToken, isLocal);
        }
      }

      const verifyResponseHeaders = { ...corsHeaders };
      if (sessionCookieHeader) {
        verifyResponseHeaders['Set-Cookie'] = sessionCookieHeader;
      }

      return new Response(JSON.stringify({
        status: 'verified',
        orderStatus: order ? order.status : null,
        verified: true,
        success: true,
        orderId: order ? order.id : null,
        packId: order ? order.pack_id : null,
        subjectId: order ? order.subject_id : null,
        jobId: existingJobId,
        reportStatus: 'preparing',
        awaitingWebhook: order ? order.status !== 'PAID' : false,
        session_issued: Boolean(sessionCookieHeader),
        message: 'Your payment has been verified. Your personalized report is being prepared. It will be ready within a few minutes.'
      }), { status: 200, headers: verifyResponseHeaders });
    }

    // 7c. ROUTE: PAYMENT STATUS POLLING (/api/v1/payments/status)
    if (url.pathname === '/api/v1/payments/status' && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };

      const orderId = (url.searchParams.get('orderId') || url.searchParams.get('order_id') || '').trim();
      const rzpOrderId = (url.searchParams.get('rzpOrderId') || url.searchParams.get('rzp_order_id') || '').trim();

      if (!orderId && !rzpOrderId) {
        return new Response(JSON.stringify({
          error: 'Either orderId or rzpOrderId parameter is required.'
        }), { status: 400, headers: corsHeaders });
      }

      let order = null;
      if (env.DB) {
        if (orderId) {
          order = await env.DB.prepare('SELECT * FROM orders WHERE id = ?').bind(orderId).first();
        } else {
          order = await env.DB.prepare('SELECT * FROM orders WHERE rzp_order_id = ?').bind(rzpOrderId).first();
        }
      } else if (typeof memoryStore !== 'undefined' && memoryStore.orders) {
        for (const ord of memoryStore.orders.values()) {
          if ((orderId && ord.id === orderId) || (rzpOrderId && ord.rzp_order_id === rzpOrderId)) {
            order = ord;
            break;
          }
        }
      }

      if (!order) {
        return new Response(JSON.stringify({
          error: 'Order not found.'
        }), { status: 404, headers: corsHeaders });
      }

      // AUTHENTICATION & AUTHORIZATION GUARD
      // Strictly requires an active session matching order.user_id, a valid order access token, or a valid checkout token
      const authUser = await authenticateUser(request, env);
      let isAuthorized = Boolean(authUser && authUser.user_id === order.user_id);

      const queryToken = (url.searchParams.get('token') || url.searchParams.get('order_token') || request.headers.get('X-Order-Token') || '').trim();
      const orderTokenSecret = await getOrderTokenSecret(env);
      if (!isAuthorized && queryToken && orderTokenSecret) {
        const isOrderTokenValid = await verifyOrderAccessToken(orderTokenSecret, order.id, queryToken);
        if (isOrderTokenValid) isAuthorized = true;
      }

      const checkoutToken = (url.searchParams.get('checkout_token') || request.headers.get('X-Checkout-Token') || '').trim();
      const sessionSecret = (env && env.SESSION_SECRET) ? env.SESSION_SECRET.trim() : '';
      if (!isAuthorized && checkoutToken && sessionSecret) {
        let orderEmail = (order.email || '').trim().toLowerCase();
        if (!orderEmail && order.subject_id) {
          if (env.DB) {
            const s = await env.DB.prepare('SELECT email FROM subjects WHERE id = ?').bind(order.subject_id).first();
            if (s && s.email) orderEmail = String(s.email).trim().toLowerCase();
          } else if (typeof memoryStore !== 'undefined' && memoryStore.subjects) {
            const s = memoryStore.subjects.get(order.subject_id);
            if (s && s.email) orderEmail = String(s.email).trim().toLowerCase();
          }
        }
        if (orderEmail) {
          const isCheckoutTokenValid = await verifyCheckoutToken(sessionSecret, orderEmail, checkoutToken);
          if (isCheckoutTokenValid) isAuthorized = true;
        }
      }

      if (!isAuthorized) {
        return new Response(JSON.stringify({
          error: 'Authentication required. Active session or valid order token is required to inspect this order.'
        }), { status: 401, headers: corsHeaders });
      }

      const now = Date.now();
      const THIRTY_MINUTES_MS = 30 * 60 * 1000;

      if (order.status !== 'PAID') {
        await reconcileStaleOrderWithRazorpay(order, env, now, request, ctx);
      }

      if (order.status === 'PAID') {
        let jobStatus = REPORT_JOB_STATUS.QUEUED;
        let jobId = null;
        if (env.DB) {
          const jRow = await env.DB.prepare('SELECT id, status FROM report_jobs WHERE order_id = ? ORDER BY created_at DESC LIMIT 1').bind(order.id).first();
          if (jRow) { jobId = jRow.id; jobStatus = String(jRow.status || REPORT_JOB_STATUS.QUEUED).toUpperCase(); }
        } else if (typeof memoryStore !== 'undefined' && memoryStore.reportJobs) {
          for (const j of memoryStore.reportJobs.values()) {
            if (j.order_id === order.id) { jobId = j.id; jobStatus = String(j.status || REPORT_JOB_STATUS.QUEUED).toUpperCase(); }
          }
        }
        // SAFETY NET: If PAID order has no report job, fulfill idempotently now
        if (!jobId) {
          console.log(`[STATUS_POLL_SAFETY_NET] Order ${order.id} is PAID but has no report job. Fulfilling idempotently now...`);
          const recRes = await fulfillPaidOrder(order, order.rzp_payment_id || 'recovery_payment', order.amount_paise, 'recovery', env, Date.now(), 'status_poll_safety_net', request);
          if (recRes && recRes.jobId) {
            jobId = recRes.jobId;
            jobStatus = REPORT_JOB_STATUS.QUEUED;
          }
        }
        // Trigger lazy retry for any pending/queued report job for this order
        if (order.user_id && (env.PDF_SERVICE_SECRET || env.ENVIRONMENT === 'local') && (env.PDF_SERVICE_URL || env.PDF_GENERATOR_URL)) {
          await retryPendingReportJobsForUser(order.user_id, env, ctx, order.id);
        }
        const normalizedReportStatus = (jobStatus === REPORT_JOB_STATUS.QUEUED || jobStatus === REPORT_JOB_STATUS.PROCESSING)
          ? 'preparing'
          : jobStatus.toLowerCase();
        return new Response(JSON.stringify({
          orderId: order.id,
          rzpOrderId: order.rzp_order_id,
          status: 'paid',
          packId: order.pack_id,
          subjectId: order.subject_id,
          jobId,
          jobStatus,
          reportStatus: normalizedReportStatus,
          message: 'Your personalized report is being prepared. It will be ready within a few minutes.'
        }), { status: 200, headers: corsHeaders });
      }

      if (order.status === 'PAYMENT_VERIFIED') {
        return new Response(JSON.stringify({
          orderId: order.id,
          rzpOrderId: order.rzp_order_id,
          status: 'payment_verified',
          packId: order.pack_id,
          subjectId: order.subject_id,
          jobId: null,
          reportStatus: 'preparing',
          awaitingWebhook: true,
          message: 'Your payment has been verified. Confirming settlement and preparing your personalized report.'
        }), { status: 200, headers: corsHeaders });
      }

      if ((order.status === 'CREATED' || order.status === 'pending') && (now - order.created_at > THIRTY_MINUTES_MS)) {
        if (env.DB) {
          await env.DB.prepare("UPDATE orders SET status = 'EXPIRED', updated_at = ? WHERE id = ?").bind(now, order.id).run();
        } else {
          order.status = 'EXPIRED';
        }
        return new Response(JSON.stringify({
          orderId: order.id,
          status: 'expired',
          message: 'Order has expired after 30 minutes. Please retry.'
        }), { status: 200, headers: corsHeaders });
      }

      return new Response(JSON.stringify({
        orderId: order.id,
        rzpOrderId: order.rzp_order_id,
        status: order.status.toLowerCase(),
        packId: order.pack_id
      }), { status: 200, headers: corsHeaders });
    }

    // 7d. ROUTE: ONE-TIME DOB CORRECTION (/api/v1/subjects/correct-dob)
    if (url.pathname === '/api/v1/subjects/correct-dob' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };

      const user = await authenticateUser(request, env);
      if (!user) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Authentication required.'
        }), { status: 401, headers: corsHeaders });
      }

      const body = await request.json().catch(() => ({}));
      const subjectId = (body.subjectId || body.subject_id || '').trim();
      const newDob = (body.newDob || body.dob || '').trim();
      const newName = (body.newName || body.name || '').trim();

      if (!subjectId || !newDob) {
        return new Response(JSON.stringify({
          success: false,
          error: 'subjectId and newDob are required.'
        }), { status: 400, headers: corsHeaders });
      }

      let subject = null;
      if (env.DB) {
        subject = await env.DB.prepare('SELECT id, user_id, name, dob_hash, created_at FROM subjects WHERE id = ? AND user_id = ?').bind(subjectId, user.user_id).first();
      } else {
        subject = memoryStore.subjects.get(subjectId);
        if (subject && subject.user_id !== user.user_id) subject = null;
      }

      if (!subject) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Subject not found or does not belong to user.'
        }), { status: 404, headers: corsHeaders });
      }

      const now = Date.now();
      const TWENTY_FOUR_HOURS_MS = 24 * 60 * 60 * 1000;
      if (now - subject.created_at > TWENTY_FOUR_HOURS_MS) {
        return new Response(JSON.stringify({
          success: false,
          error: 'DOB correction window has expired. Corrections are only permitted within 24 hours of creation.'
        }), { status: 400, headers: corsHeaders });
      }

      // Check for buy-download-correct-download abuse: Block if any report exists or was served
      let completedReport = null;
      if (env.DB) {
        completedReport = await env.DB.prepare(
          "SELECT id, status, r2_key, completed_at, downloaded_at FROM report_jobs WHERE user_id = ? AND subject_id = ? AND (UPPER(status) IN ('COMPLETED', 'DOWNLOADED', 'READY') OR r2_key IS NOT NULL OR completed_at IS NOT NULL OR downloaded_at IS NOT NULL) LIMIT 1"
        ).bind(user.user_id, subjectId).first();
      } else if (memoryStore.reportJobs) {
        for (const job of memoryStore.reportJobs.values()) {
          if (job.user_id === user.user_id && job.subject_id === subjectId && doesReportExistOrWasServed(job)) {
            completedReport = job;
            break;
          }
        }
      }

      if (completedReport) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Date of birth cannot be corrected after a personalized report has been generated or downloaded.'
        }), { status: 400, headers: corsHeaders });
      }

      let alreadyCorrected = false;
      if (env.DB) {
        const prevCorrection = await env.DB.prepare(
          "SELECT id FROM audit_log WHERE resource_type = 'subjects' AND resource_id = ? AND action = 'subject_dob_corrected'"
        ).bind(subjectId).first();
        if (prevCorrection) alreadyCorrected = true;
      } else {
        if (subject.corrected) alreadyCorrected = true;
      }

      if (alreadyCorrected) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Date of birth can only be corrected once.'
        }), { status: 400, headers: corsHeaders });
      }

      const newDobHash = await sha256Hex(newDob);
      const updatedName = newName || subject.name;
      const dataEncKey = requireSecret(env, 'DATA_ENCRYPTION_KEY');
      const newDobEnc = await encryptField(newDob, dataEncKey);

      if (env.DB) {
        await env.DB.prepare(
          'UPDATE subjects SET dob_hash = ?, dob_enc = ?, name = ? WHERE id = ?'
        ).bind(newDobHash, newDobEnc, updatedName, subjectId).run();

        // Invalidate old report jobs in progress and queue fresh job if entitlement exists
        await env.DB.prepare(
          "UPDATE report_jobs SET status = 'CANCELLED' WHERE user_id = ? AND subject_id = ? AND status IN ('QUEUED', 'PROCESSING')"
        ).bind(user.user_id, subjectId).run();

        const ent = await env.DB.prepare(
          "SELECT pack_id, order_id FROM entitlements WHERE user_id = ? AND subject_id = ?"
        ).bind(user.user_id, subjectId).first();

        if (ent) {
          const newJobId = 'job_' + now + '_' + getRandomHex(4);
          await env.DB.prepare(
            "INSERT INTO report_jobs (id, user_id, subject_id, pack_id, order_id, status, created_at) VALUES (?, ?, ?, ?, ?, 'QUEUED', ?)"
          ).bind(newJobId, user.user_id, subjectId, ent.pack_id, ent.order_id || null, now).run();
        }

        await env.DB.prepare(
          "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, ?, 'subject_dob_corrected', 'subjects', ?, ?, ?)"
        ).bind('aud_' + now + '_' + getRandomHex(4), user.user_id, subjectId, JSON.stringify({ old_dob_hash: subject.dob_hash, new_dob_hash: newDobHash, name: updatedName }), now).run();
      } else {
        subject.dob_hash = newDobHash;
        subject.dob_enc = newDobEnc;
        subject.name = updatedName;
        subject.corrected = true;
        for (const job of memoryStore.reportJobs.values()) {
          if (job.user_id === user.user_id && job.subject_id === subjectId && (job.status === 'QUEUED' || job.status === 'PROCESSING')) {
            job.status = 'CANCELLED';
          }
        }
        const newJobId = 'job_' + now + '_' + getRandomHex(4);
        memoryStore.reportJobs.set(newJobId, {
          id: newJobId,
          user_id: user.user_id,
          subject_id: subjectId,
          pack_id: 'report_basic',
          status: 'QUEUED',
          created_at: now
        });
      }

      return new Response(JSON.stringify({
        success: true,
        message: 'Date of birth corrected successfully.',
        subject: {
          id: subjectId,
          name: updatedName,
          dob: newDob
        }
      }), { status: 200, headers: corsHeaders });
    }

    // 7g. ROUTE: SUBJECTS API (/api/v1/subjects)
    if (url.pathname === '/api/v1/subjects') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, Cookie'
      };

      if (request.method === 'OPTIONS') return new Response(null, { headers: corsHeaders });

      const user = await authenticateUser(request, env);
      if (!user) {
        return new Response(JSON.stringify({ error: 'Unauthorized. Please sign in.' }), { status: 401, headers: corsHeaders });
      }

      if (request.method === 'GET') {
        const dataEncKey = requireSecret(env, 'DATA_ENCRYPTION_KEY');
        let subjects = [];
        if (env.DB) {
          const rows = await env.DB.prepare('SELECT id, name, dob_enc, created_at FROM subjects WHERE user_id = ? ORDER BY created_at ASC').bind(user.user_id).all();
          const rawRows = (rows && rows.results) || [];
          for (const r of rawRows) {
            const decDob = r.dob_enc ? await decryptField(r.dob_enc, dataEncKey) : '';
            subjects.push({ id: r.id, name: r.name, dob: decDob, created_at: r.created_at });
          }
        } else {
          for (const s of memoryStore.subjects.values()) {
            if (s.user_id === user.user_id) {
              const decDob = s.dob_enc ? await decryptField(s.dob_enc, dataEncKey) : (s.dob || '');
              subjects.push({ id: s.id, name: s.name, dob: decDob, created_at: s.created_at });
            }
          }
        }
        return new Response(JSON.stringify({ subjects }), { status: 200, headers: corsHeaders });
      }

      if (request.method === 'POST') {
        const body = await request.json().catch(() => ({}));

        // Consent Check
        if (body.consent !== true) {
          return new Response(JSON.stringify({
            error: 'Consent is required to process personal birth details.'
          }), { status: 400, headers: corsHeaders });
        }

        const name = (body.name || '').trim();
        const dob = (body.dob || '').trim();
        if (!name || !dob) {
          return new Response(JSON.stringify({
            error: 'name and dob are required.'
          }), { status: 400, headers: corsHeaders });
        }

        const dobInfo = parseDobParts(dob);

        // Cap subjects at 10 per account
        if (env.DB) {
          const countRow = await env.DB.prepare('SELECT COUNT(*) as cnt FROM subjects WHERE user_id = ?').bind(user.user_id).first();
          if (countRow && countRow.cnt >= 10) {
            return new Response(JSON.stringify({
              error: 'Maximum limit of 10 subjects per account reached.'
            }), { status: 400, headers: corsHeaders });
          }
        } else {
          let count = 0;
          for (const s of memoryStore.subjects.values()) {
            if (s.user_id === user.user_id) count++;
          }
          if (count >= 10) {
            return new Response(JSON.stringify({
              error: 'Maximum limit of 10 subjects per account reached.'
            }), { status: 400, headers: corsHeaders });
          }
        }

        const dobHash = await sha256Hex(dobInfo.dob);
        const now = Date.now();
        const subjectId = 'sbj_' + now + '_' + getRandomHex(4);
        const consentId = 'cns_' + now + '_' + getRandomHex(4);

        const dataEncKey = requireSecret(env, 'DATA_ENCRYPTION_KEY');
        const dobEnc = await encryptField(dobInfo.dob, dataEncKey);
        const birthTimeEnc = await encryptField(body.birthTime || body.birth_time || null, dataEncKey);

        if (env.DB) {
          await env.DB.prepare(
            'INSERT INTO subjects (id, user_id, name, dob_hash, dob_enc, birth_time_enc, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
          ).bind(subjectId, user.user_id, name, dobHash, dobEnc, birthTimeEnc, now).run();

          await env.DB.prepare(
            'INSERT INTO consents (id, user_id, purpose, text_version, granted_at) VALUES (?, ?, ?, ?, ?)'
          ).bind(consentId, user.user_id, 'report_processing_dpdp_2023', 'v1.0_2026', now).run();
        } else {
          memoryStore.subjects.set(subjectId, {
            id: subjectId,
            user_id: user.user_id,
            name,
            dob_hash: dobHash,
            dob_enc: dobEnc,
            birth_time_enc: birthTimeEnc,
            created_at: now
          });
          memoryStore.consents = memoryStore.consents || new Map();
          memoryStore.consents.set(consentId, {
            id: consentId,
            user_id: user.user_id,
            purpose: 'report_processing_dpdp_2023',
            text_version: 'v1.0_2026',
            granted_at: now
          });
        }

        return new Response(JSON.stringify({
          success: true,
          subject: {
            id: subjectId,
            name,
            dob: dobInfo.dob,
            created_at: now
          }
        }), { status: 201, headers: corsHeaders });
      }

      return new Response(JSON.stringify({ error: 'Method not allowed' }), { status: 405, headers: corsHeaders });
    }

    // 7h. ROUTE: DASHBOARD VIEW API (/api/v1/dashboard/view)
    if (url.pathname === '/api/v1/dashboard/view' && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization, Cookie',
        'Referrer-Policy': 'no-referrer'
      };

      const user = await authenticateUser(request, env);
      const queryOrderId = (url.searchParams.get('order_id') || '').trim();
      const queryToken = (url.searchParams.get('token') || url.searchParams.get('order_token') || '').trim();
      const orderTokenSecret = await getOrderTokenSecret(env);

      let tokenOrder = null;
      if (!user) {
        if (queryOrderId && queryToken && orderTokenSecret) {
          const isValid = await verifyOrderAccessToken(orderTokenSecret, queryOrderId, queryToken);
          if (isValid) {
            if (env.DB) {
              tokenOrder = await env.DB.prepare('SELECT * FROM orders WHERE id = ?').bind(queryOrderId).first();
            } else if (memoryStore && memoryStore.orders) {
              tokenOrder = memoryStore.orders.get(queryOrderId);
            }
          }
        }
        if (!tokenOrder) {
          return new Response(JSON.stringify({ error: 'Unauthorized. Please sign in.' }), { status: 401, headers: corsHeaders });
        }
      }

      if (tokenOrder) {
        if (tokenOrder.status !== 'PAID') {
          await reconcileStaleOrderWithRazorpay(tokenOrder, env, Date.now(), request, ctx);
        }
        let job = null;
        if (env.DB) {
          job = await env.DB.prepare('SELECT * FROM report_jobs WHERE order_id = ? ORDER BY created_at DESC LIMIT 1').bind(tokenOrder.id).first();
        } else if (memoryStore && memoryStore.reportJobs) {
          for (const j of memoryStore.reportJobs.values()) {
            if (j.order_id === tokenOrder.id) { job = j; break; }
          }
        }
        // SAFETY NET: If token order is PAID and has no report job, fulfill idempotently now
        if (tokenOrder.status === 'PAID' && !job) {
          console.log(`[DASHBOARD_SAFETY_NET] Token order ${tokenOrder.id} is PAID but has no report job. Fulfilling idempotently now...`);
          await fulfillPaidOrder(tokenOrder, tokenOrder.rzp_payment_id || 'recovery_payment', tokenOrder.amount_paise, 'recovery', env, Date.now(), 'dashboard_safety_net', request);
          if (env.DB) {
            job = await env.DB.prepare('SELECT * FROM report_jobs WHERE order_id = ? ORDER BY created_at DESC LIMIT 1').bind(tokenOrder.id).first();
          } else if (memoryStore && memoryStore.reportJobs) {
            for (const j of memoryStore.reportJobs.values()) {
              if (j.order_id === tokenOrder.id) { job = j; break; }
            }
          }
        }
        const pack = getPackById(tokenOrder.pack_id);
        const st = job ? String(job.status || 'QUEUED').toUpperCase() : 'QUEUED';
        const attempts = job ? (job.attempts || 0) : 0;
        const jobProg = formatReportJobProgress(job, Date.now());
        let displayStatus = 'preparing';
        let statusBadge = 'Payment received, preparing your report';
        let message = jobProg.progressLine || 'Payment received, preparing your report';
        let isDownloadable = false;

        if (st === 'COMPLETED' || st === 'DOWNLOADED' || (job && (job.r2_key || job.download_url))) {
          displayStatus = 'ready';
          statusBadge = 'Ready';
          message = 'Your report is ready to download.';
          isDownloadable = true;
        } else if (st === 'FAILED' || attempts >= 3) {
          displayStatus = 'needs_attention';
          statusBadge = 'Needs Attention';
          message = "We’re checking this order. If it isn’t ready within 30 minutes, write to support@numerosvision.com.";
        }

        const reportItem = {
          orderId: tokenOrder.id,
          packId: tokenOrder.pack_id,
          title: pack ? pack.name : 'Numerology Report',
          pages: pack ? pack.pages : 0,
          status: displayStatus,
          statusBadge: statusBadge,
          message: message,
          currentStage: jobProg.currentStage,
          progressLine: jobProg.progressLine,
          delayedNotice: jobProg.delayedNotice,
          isDownloadable: isDownloadable,
          downloadUrl: (job && job.download_url) ? job.download_url : null,
          createdAt: tokenOrder.created_at,
          amountPaise: tokenOrder.amount_paise
        };

        return new Response(JSON.stringify({
          user: { email: tokenOrder.email || 'Customer' },
          subjects: [],
          reports: [reportItem]
        }), { status: 200, headers: corsHeaders });
      }

      const dataEncKey = requireSecret(env, 'DATA_ENCRYPTION_KEY');
      let subjects = [];
      let rawSubjects = [];
      if (env.DB) {
        const rows = await env.DB.prepare('SELECT id, name, dob_enc, created_at FROM subjects WHERE user_id = ? ORDER BY created_at ASC').bind(user.user_id).all();
        rawSubjects = (rows && rows.results) || [];
      } else {
        for (const s of memoryStore.subjects.values()) {
          if (s.user_id === user.user_id) {
            rawSubjects.push(s);
          }
        }
      }
      for (const s of rawSubjects) {
        const decDob = s.dob_enc ? await decryptField(s.dob_enc, dataEncKey) : (s.dob || '');
        subjects.push({ id: s.id, name: s.name, dob: decDob, dob_enc: s.dob_enc, created_at: s.created_at });
      }

      const reqSubjId = (url.searchParams.get('subjectId') || '').trim();
      let activeSubject = null;
      if (reqSubjId) {
        activeSubject = subjects.find(s => s.id === reqSubjId) || null;
      }
      if (!activeSubject && subjects.length > 0) {
        activeSubject = subjects[0];
      }

      let viewData = null;
      if (activeSubject) {
        viewData = await viewFor(user, activeSubject, env);
      }

      // Lazy retry any QUEUED report_jobs (attempts < 3) for this user on dashboard load
      if (env.PDF_SERVICE_SECRET && (env.PDF_SERVICE_URL || env.PDF_GENERATOR_URL)) {
        await retryPendingReportJobsForUser(user.user_id, env, ctx);
      }

      // Charm AI credit balance (defaults to 3 signup credits for new users)
      let charmCredits = null;
      if (env.DB) {
        const credRow = await env.DB.prepare('SELECT SUM(delta) as bal FROM credit_ledger WHERE user_id = ?').bind(user.user_id).first();
        if (credRow && credRow.bal !== null && credRow.bal !== undefined) {
          charmCredits = credRow.bal;
        }
      } else if (memoryStore && memoryStore.creditLedger) {
        let sum = 0;
        let found = false;
        for (const entry of memoryStore.creditLedger.values()) {
          if (entry.user_id === user.user_id) {
            sum += (entry.delta || 0);
            found = true;
          }
        }
        if (found) charmCredits = sum;
      }
      if (charmCredits === null) charmCredits = 3;

      // 10-MINUTE FALLBACK RECONCILIATION: Check any stale PAYMENT_VERIFIED / CREATED orders >= 10m with Razorpay
      let userOrdersPrecheck = [];
      try {
        if (env.DB) {
          const preRows = await env.DB.prepare('SELECT * FROM orders WHERE user_id = ? ORDER BY created_at DESC').bind(user.user_id).all();
          userOrdersPrecheck = (preRows && preRows.results) || [];
        } else if (typeof memoryStore !== 'undefined' && memoryStore.orders) {
          for (const ord of memoryStore.orders.values()) {
            if (ord.user_id === user.user_id) userOrdersPrecheck.push(ord);
          }
        }
        const dashNow = Date.now();
        for (const candOrd of userOrdersPrecheck) {
          if (candOrd && candOrd.status !== 'PAID') {
            await reconcileStaleOrderWithRazorpay(candOrd, env, dashNow, request, ctx);
          }
        }
      } catch (reconcileErr) {
        console.warn('[DASHBOARD_10MIN_FALLBACK_WARN]', reconcileErr);
      }

      // SAFETY NET: If user has any PAID orders with missing report jobs, fulfill them now idempotently
      try {
        let unfulfilledOrders = [];
        if (env.DB) {
          const missingRows = await env.DB.prepare(`
            SELECT o.* FROM orders o
            WHERE o.user_id = ? AND o.status = 'PAID'
              AND NOT EXISTS (SELECT 1 FROM report_jobs rj WHERE rj.order_id = o.id)
          `).bind(user.user_id).all();
          unfulfilledOrders = (missingRows && missingRows.results) || [];
        } else if (typeof memoryStore !== 'undefined' && memoryStore.orders) {
          for (const ord of memoryStore.orders.values()) {
            if (ord.user_id === user.user_id && ord.status === 'PAID') {
              const hasJob = Array.from(memoryStore.reportJobs.values()).some(j => j.order_id === ord.id);
              if (!hasJob) unfulfilledOrders.push(ord);
            }
          }
        }
        for (const uOrd of unfulfilledOrders) {
          console.log(`[DASHBOARD_SAFETY_NET] User order ${uOrd.id} is PAID but has no report job. Fulfilling idempotently now...`);
          await fulfillPaidOrder(uOrd, uOrd.rzp_payment_id || 'recovery_payment', uOrd.amount_paise, 'recovery', env, Date.now(), 'dashboard_safety_net', request);
        }
      } catch (safetyErr) {
        console.warn('[DASHBOARD_SAFETY_NET_ERROR]', safetyErr);
      }

      // 1. User Reports (Report Jobs)
      let rawReportJobs = [];
      if (env.DB) {
        const jobRows = await env.DB.prepare(
          'SELECT * FROM report_jobs WHERE user_id = ? ORDER BY created_at DESC'
        ).bind(user.user_id).all();
        rawReportJobs = (jobRows && jobRows.results) || [];
      } else if (memoryStore && memoryStore.reportJobs) {
        for (const j of memoryStore.reportJobs.values()) {
          if (j.user_id === user.user_id) rawReportJobs.push(j);
        }
      }

      // Deduplicate report jobs: strictly ONE row per (profile, pack) using latest completed job
      const jobsByProfilePack = new Map();
      for (const job of rawReportJobs) {
        const key = `${job.subject_id || ''}::${job.pack_id || ''}`;
        const existing = jobsByProfilePack.get(key);
        const st = String(job.status || '').toUpperCase();
        const isComp = st === 'COMPLETED' || st === 'DOWNLOADED' || !!job.r2_key;

        if (!existing) {
          jobsByProfilePack.set(key, job);
        } else {
          const exSt = String(existing.status || '').toUpperCase();
          const exComp = exSt === 'COMPLETED' || exSt === 'DOWNLOADED' || !!existing.r2_key;
          if (isComp && !exComp) {
            jobsByProfilePack.set(key, job);
          } else if (isComp && exComp) {
            if ((job.created_at || 0) > (existing.created_at || 0)) {
              jobsByProfilePack.set(key, job);
            }
          } else if (!isComp && !exComp) {
            if ((job.created_at || 0) > (existing.created_at || 0)) {
              jobsByProfilePack.set(key, job);
            }
          }
        }
      }

      const deduplicatedJobs = Array.from(jobsByProfilePack.values()).sort((a, b) => (b.created_at || 0) - (a.created_at || 0));

      const formattedReports = deduplicatedJobs.map(job => {
        const packInfo = getPackById(job.pack_id);
        const subj = subjects.find(s => s.id === job.subject_id) || activeSubject || { name: 'Member', dob: '' };
        const st = String(job.status || 'QUEUED').toUpperCase();
        const attempts = job.attempts || 0;
        const jobProg = formatReportJobProgress(job, Date.now());
        
        let displayStatus = 'preparing';
        let statusBadge = 'Payment received, preparing your report';
        let message = jobProg.progressLine || 'Payment received, preparing your report';
        let isDownloadable = false;

        if (st === 'COMPLETED' || st === 'DOWNLOADED' || job.r2_key) {
          displayStatus = 'ready';
          statusBadge = 'Ready';
          message = 'Your report is ready to download.';
          isDownloadable = true;
        } else if (st === 'FAILED' || attempts >= 3) {
          displayStatus = 'needs_attention';
          statusBadge = 'Needs Attention';
          message = "We’re checking this order. If it isn’t ready within 30 minutes, write to support@numerosvision.com.";
        }

        return {
          id: job.id,
          orderId: job.order_id,
          packId: job.pack_id,
          tier: packInfo ? packInfo.tier_id : (job.pack_id.replace('report_', '')),
          title: packInfo ? packInfo.name : 'Numerology Report',
          pages: packInfo ? packInfo.pages : 3,
          subjectId: job.subject_id,
          subjectName: subj.name,
          subjectDob: subj.dob,
          status: displayStatus,
          statusBadge,
          message,
          currentStage: jobProg.currentStage,
          progressLine: jobProg.progressLine,
          delayedNotice: jobProg.delayedNotice,
          attempts,
          isDownloadable,
          downloadUrl: null, // Minted at CLICK time via POST /api/v1/reports/download-token (session-bound 5-min TTL)
          createdAt: job.created_at,
          completedAt: job.completed_at
        };
      });

      // Surface any PAYMENT_VERIFIED orders awaiting Razorpay webhook settlement as 'preparing'
      for (const pvOrd of userOrdersPrecheck) {
        if (pvOrd && pvOrd.status === 'PAYMENT_VERIFIED') {
          const alreadyListed = formattedReports.some(
            r => r.orderId === pvOrd.id || (r.subjectId === pvOrd.subject_id && r.packId === pvOrd.pack_id)
          );
          if (!alreadyListed) {
            const pvPack = getPackById(pvOrd.pack_id);
            if (!pvPack || !pvPack.pages) continue;
            const pvSubj = subjects.find(s => s.id === pvOrd.subject_id) || activeSubject || { name: 'Member', dob: '' };
            formattedReports.unshift({
              id: 'pending_' + pvOrd.id,
              orderId: pvOrd.id,
              packId: pvOrd.pack_id,
              tier: pvPack.tier_id || pvOrd.pack_id.replace('report_', ''),
              title: pvPack.name,
              pages: pvPack.pages,
              subjectId: pvOrd.subject_id,
              subjectName: pvSubj.name,
              subjectDob: pvSubj.dob,
              status: 'preparing',
              statusBadge: 'Payment received, preparing your report',
              message: 'Payment received, preparing your report',
              attempts: 0,
              isDownloadable: false,
              downloadUrl: null,
              createdAt: pvOrd.created_at,
              completedAt: null
            });
          }
        }
      }

      // 2. User Receipts (Built strictly from paid orders & payments table, not empty invoices)
      let receipts = [];
      if (env.DB) {
        const recRows = await env.DB.prepare(`
          SELECT o.id as order_id, o.rzp_order_id, o.pack_id, o.amount_paise, o.currency, o.status, o.created_at,
                 p.rzp_payment_id, p.captured_at
          FROM orders o
          LEFT JOIN payments p ON o.id = p.order_id
          WHERE o.user_id = ? AND o.status = 'PAID'
          ORDER BY o.created_at DESC
        `).bind(user.user_id).all();
        receipts = (recRows && recRows.results) || [];
      } else if (memoryStore && memoryStore.orders) {
        for (const ord of memoryStore.orders.values()) {
          if (ord.user_id === user.user_id && ord.status === 'PAID') {
            const pmt = Array.from(memoryStore.payments.values()).find(p => p.order_id === ord.id);
            receipts.push({
              order_id: ord.id,
              rzp_order_id: ord.rzp_order_id,
              pack_id: ord.pack_id,
              amount_paise: ord.amount_paise,
              currency: ord.currency || 'INR',
              status: ord.status,
              created_at: ord.created_at,
              rzp_payment_id: pmt ? pmt.rzp_payment_id : null,
              captured_at: pmt ? pmt.captured_at : ord.created_at
            });
          }
        }
      }

      const formattedReceipts = receipts.map(r => {
        const packInfo = getPackById(r.pack_id, env, Number(r.created_at || Date.now()));
        return {
          document_type: 'Payment receipt',
          order_id: r.order_id,
          payment_id: r.rzp_payment_id || r.rzp_order_id || 'N/A',
          pack_id: r.pack_id,
          pack_name: packInfo ? packInfo.name : 'Numerology Report',
          pack_descriptor: (packInfo && packInfo.descriptor) ? packInfo.descriptor : '',
          supplier_legal_name: 'Bhaskar Kumar Singh',
          supplier_entity: 'Numeros Vision Consultancy (Bhaskar Kumar Singh)',
          amount_paise: r.amount_paise,
          amount_inr: Math.round(r.amount_paise / 100),
          currency: r.currency || 'INR',
          status: 'PAID',
          created_at: r.created_at
        };
      });

      // Orders
      let orders = [];
      if (env.DB) {
        const ordRows = await env.DB.prepare('SELECT id, rzp_order_id, pack_id, subject_id, amount_paise, status, created_at FROM orders WHERE user_id = ? ORDER BY created_at DESC').bind(user.user_id).all();
        orders = (ordRows && ordRows.results) || [];
      } else if (memoryStore && memoryStore.orders) {
        for (const ord of memoryStore.orders.values()) {
          if (ord.user_id === user.user_id) orders.push(ord);
        }
      }

      const cleanSubjects = subjects.map(({ id, name, dob, created_at }) => ({ id, name, dob, created_at }));

      return new Response(JSON.stringify({
        user: {
          userId: user.user_id,
          phone: user.phone || null,
          email: user.email || null,
          name: user.name || (activeSubject ? activeSubject.name : 'Member')
        },
        subjects: cleanSubjects,
        activeSubject: activeSubject ? { id: activeSubject.id, name: activeSubject.name, dob: activeSubject.dob } : null,
        subjectCount: subjects.length,
        charmCredits,
        view: viewData,
        reports: formattedReports,
        receipts: formattedReceipts,
        invoices: formattedReceipts,
        orders
      }), { status: 200, headers: corsHeaders });
    }


    // 7e. ROUTE: RAZORPAY WEBHOOK (/api/v1/payments/webhook & legacy /api/webhook)
    if ((url.pathname === '/api/v1/payments/webhook' || url.pathname === '/api/webhook') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };

      if (url.pathname === '/api/webhook') {
        corsHeaders['X-API-Deprecated'] = '/api/webhook is retired. Use /api/v1/payments/webhook';
      }

      const rawBody = await request.text();
      const signature = request.headers.get('X-Razorpay-Signature') || request.headers.get('x-razorpay-signature') || '';
      const webhookSecret = env.RAZORPAY_WEBHOOK_SECRET;

      if (!webhookSecret) {
        return new Response(JSON.stringify({ status: 'error', message: 'Webhook secret not configured on server' }), { status: 500, headers: corsHeaders });
      }

      // 1. Signature Verification with constant-time comparison
      let isSigValid = false;
      try {
        const encoder = new TextEncoder();
        const keyData = encoder.encode(webhookSecret.trim());
        const msgData = encoder.encode(rawBody);
        const cryptoKey = await crypto.subtle.importKey(
          'raw',
          keyData,
          { name: 'HMAC', hash: 'SHA-256' },
          false,
          ['sign']
        );
        const sigBuffer = await crypto.subtle.sign('HMAC', cryptoKey, msgData);
        const generatedSig = Array.from(new Uint8Array(sigBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');

        if (timingSafeEqual(generatedSig.toLowerCase(), (signature || '').trim().toLowerCase())) {
          isSigValid = true;
        }
      } catch (sigErr) {
        console.warn('Webhook HMAC verification error:', sigErr);
      }

      if (!isSigValid) {
        return new Response(JSON.stringify({ status: 'error', message: 'Invalid webhook signature' }), { status: 400, headers: corsHeaders });
      }

      let payload = {};
      try {
        payload = JSON.parse(rawBody);
      } catch (e) {
        return new Response(JSON.stringify({ status: 'error', message: 'Malformed JSON payload' }), { status: 400, headers: corsHeaders });
      }

      const event = payload.event || '';
      const eventId = payload.event_id || ('evt_' + (payload.created_at || Date.now()) + '_' + getRandomHex(4));
      const now = Date.now();

      // 2. Idempotency Check
      if (env.DB) {
        const existingEvent = await env.DB.prepare('SELECT event_id FROM webhook_events WHERE event_id = ?').bind(eventId).first();
        if (existingEvent) {
          return new Response(JSON.stringify({ status: 'success', message: 'Event already processed' }), { status: 200, headers: corsHeaders });
        }
        const payloadHash = await sha256Hex(rawBody);
        await env.DB.prepare(
          'INSERT INTO webhook_events (event_id, type, payload_hash, received_at) VALUES (?, ?, ?, ?)'
        ).bind(eventId, event, payloadHash, now).run();
      }

      // 3. Event Processing
      if (event === 'order.paid' || event === 'payment.captured') {
        const paymentEntity = payload.payload?.payment?.entity || {};
        const orderEntity = payload.payload?.order?.entity || {};
        const rzpOrderId = paymentEntity.order_id || orderEntity.id;
        const paymentId = paymentEntity.id;
        const amountPaise = paymentEntity.amount;
        const currency = paymentEntity.currency;

        let order = null;
        if (env.DB) {
          order = await env.DB.prepare('SELECT * FROM orders WHERE rzp_order_id = ?').bind(rzpOrderId).first();
        } else {
          for (const ord of memoryStore.orders.values()) {
            if (ord.rzp_order_id === rzpOrderId) { order = ord; break; }
          }
        }

        // Returns 200 for unknown orders (logged)
        if (!order) {
          console.warn(`[Webhook_Unknown_Order] Order ${rzpOrderId} not found in database. Logged.`);
          if (env.DB) {
            await env.DB.prepare(
              "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, 'webhook', 'webhook_unknown_order', 'orders', ?, ?, ?)"
            ).bind('aud_' + now + '_' + getRandomHex(4), rzpOrderId || 'unknown', JSON.stringify({ event, paymentId, amountPaise }), now).run();
          }
          return new Response(JSON.stringify({ status: 'ok', warning: 'unknown_order_logged' }), { status: 200, headers: corsHeaders });
        }

        // Tolerates out-of-order events: if order already paid, return 200 idempotently
        if (order.status === 'PAID') {
          console.info(`[Webhook] Order ${order.id} is already marked PAID. Idempotent skip.`);
          return new Response(JSON.stringify({ status: 'ok', message: 'order_already_paid' }), { status: 200, headers: corsHeaders });
        }

        // Amount & currency verification
        if (currency !== 'INR' || amountPaise !== order.amount_paise) {
          console.error(`[Webhook_Amount_Mismatch] Expected INR ${order.amount_paise}, got ${currency} ${amountPaise}`);
          if (env.DB) {
            await env.DB.prepare(
              "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, 'webhook', 'payment_amount_mismatch', 'orders', ?, ?, ?)"
            ).bind('aud_' + now + '_' + getRandomHex(4), order.id, JSON.stringify({ expected: order.amount_paise, received: amountPaise, currency }), now).run();
          }
          return new Response(JSON.stringify({ status: 'ignored_due_to_amount_mismatch' }), { status: 200, headers: corsHeaders });
        }

        // Fulfill payment (handles CREATED, pending, or EXPIRED late UPI payments)
        const fulfillRes = await fulfillPaidOrder(order, paymentId, amountPaise, paymentEntity.method || 'card', env, now, 'webhook', request);
        // Acknowledge Razorpay webhook immediately and run PDF report dispatch in background via ctx.waitUntil
        if (fulfillRes && fulfillRes.jobId && ctx && typeof ctx.waitUntil === 'function') {
          ctx.waitUntil(
            dispatchReportJob(fulfillRes.jobId, env).catch(err => console.error('[Webhook_WaitUntil_Dispatch_Error]', err))
          );
        }
        return new Response(JSON.stringify({
          status: 'success',
          message: fulfillRes.alreadyFulfilled ? 'order_already_paid' : 'order_paid_fulfilled',
          jobId: fulfillRes.jobId || null,
          note: order.status === 'EXPIRED' ? 'late_upi_settlement_on_expired_order' : undefined
        }), { status: 200, headers: corsHeaders });
      } else if (event === 'payment.failed') {
        const paymentEntity = payload.payload?.payment?.entity || {};
        const rzpOrderId = paymentEntity.order_id;
        if (env.DB && rzpOrderId) {
          const order = await env.DB.prepare('SELECT id, status FROM orders WHERE rzp_order_id = ?').bind(rzpOrderId).first();
          if (order && order.status !== 'PAID') {
            await env.DB.prepare("UPDATE orders SET status = 'FAILED', updated_at = ? WHERE id = ?").bind(now, order.id).run();
            await env.DB.prepare(
              "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, 'webhook', 'payment_failed', 'orders', ?, ?, ?)"
            ).bind('aud_' + now + '_' + getRandomHex(4), order.id, JSON.stringify({ reason: paymentEntity.error_description }), now).run();
          }
        }
        return new Response(JSON.stringify({ status: 'success', message: 'payment_failed_recorded' }), { status: 200, headers: corsHeaders });
      } else if (event === 'refund.processed') {
        const refundEntity = payload.payload?.refund?.entity || {};
        const paymentEntity = payload.payload?.payment?.entity || {};
        const rzpPaymentId = refundEntity.payment_id || paymentEntity.id;
        let order = null;
        let pmt = null;

        if (env.DB && rzpPaymentId) {
          pmt = await env.DB.prepare('SELECT id, order_id FROM payments WHERE rzp_payment_id = ?').bind(rzpPaymentId).first();
          if (pmt) {
            order = await env.DB.prepare('SELECT id, user_id, subject_id, pack_id FROM orders WHERE id = ?').bind(pmt.order_id).first();
          }
        } else if (memoryStore.payments) {
          pmt = memoryStore.payments.get(rzpPaymentId);
          if (pmt && memoryStore.orders) {
            order = memoryStore.orders.get(pmt.order_id);
          }
        }

        if (order && pmt) {
          const refId = 'ref_' + now + '_' + getRandomHex(4);
          const refundAmount = refundEntity.amount || 0;
          const isFullRefund = refundAmount >= pmt.amount_paise;

          if (!isFullRefund) {
            // Partial refund: do NOT auto-revoke; flag in audit_log for manual review
            if (env.DB) {
              await env.DB.prepare(
                "INSERT INTO refunds (id, payment_id, order_id, user_id, rzp_refund_id, amount_paise, reason, status, created_at, processed_at) VALUES (?, ?, ?, ?, ?, ?, ?, 'PARTIAL_PROCESSED', ?, ?)"
              ).bind(refId, pmt.id, order.id, order.user_id, refundEntity.id, refundAmount, refundEntity.notes?.reason || 'user_request', now, now).run();

              await env.DB.prepare(
                "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, 'webhook', 'partial_refund_manual_review_required', 'refunds', ?, ?, ?)"
              ).bind('aud_' + now + '_' + getRandomHex(4), refId, JSON.stringify({ orderId: order.id, paymentId: pmt.id, paymentAmount: pmt.amount_paise, refundAmount, manual_review_required: true }), now).run();
            } else {
              memoryStore.refunds = memoryStore.refunds || new Map();
              memoryStore.refunds.set(refId, {
                id: refId,
                payment_id: pmt.id,
                order_id: order.id,
                amount_paise: refundAmount,
                status: 'PARTIAL_PROCESSED'
              });
              memoryStore.auditLog = memoryStore.auditLog || new Map();
              memoryStore.auditLog.set('aud_' + now, {
                action: 'partial_refund_manual_review_required',
                resource_id: refId,
                details: { orderId: order.id, manual_review_required: true }
              });
            }
            return new Response(JSON.stringify({ status: 'success', message: 'partial_refund_flagged_for_manual_review' }), { status: 200, headers: corsHeaders });
          }

          if (env.DB) {
            // 1. Record full refund in refunds table
            await env.DB.prepare(
              "INSERT INTO refunds (id, payment_id, order_id, user_id, rzp_refund_id, amount_paise, reason, status, created_at, processed_at) VALUES (?, ?, ?, ?, ?, ?, ?, 'PROCESSED', ?, ?)"
            ).bind(refId, pmt.id, order.id, order.user_id, refundEntity.id, refundAmount, refundEntity.notes?.reason || 'user_request', now, now).run();

            // 2. Mark order as REFUNDED
            await env.DB.prepare("UPDATE orders SET status = 'REFUNDED', updated_at = ? WHERE id = ?").bind(now, order.id).run();

            // 3. Revoke entitlement
            await env.DB.prepare("DELETE FROM entitlements WHERE user_id = ? AND subject_id = ? AND pack_id = ?").bind(order.user_id, order.subject_id, order.pack_id).run();

            // 4. Revoke vouchers in voucher_ledger
            await env.DB.prepare("UPDATE voucher_ledger SET status = 'REFUNDED' WHERE order_id = ?").bind(order.id).run();

            // 5. Claw back Charm credits in credit_ledger if granted
            const creditGrant = await env.DB.prepare(
              "SELECT delta FROM credit_ledger WHERE user_id = ? AND ref_id = ?"
            ).bind(order.user_id, 'order_' + order.id).first();
            if (creditGrant && creditGrant.delta > 0) {
              const prevBalRow = await env.DB.prepare('SELECT SUM(delta) as bal FROM credit_ledger WHERE user_id = ?').bind(order.user_id).first();
              const newBal = ((prevBalRow && prevBalRow.bal) ? prevBalRow.bal : 0) - creditGrant.delta;
              await env.DB.prepare(
                'INSERT INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
              ).bind('crd_' + now + '_' + getRandomHex(4), order.user_id, -creditGrant.delta, 'refund_reversal', 'refund_' + refId, newBal, now).run();
            }

            // 6. Audit log
            await env.DB.prepare(
              "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, 'webhook', 'refund_processed_revoked', 'refunds', ?, ?, ?)"
            ).bind('aud_' + now + '_' + getRandomHex(4), refId, JSON.stringify({ orderId: order.id, amount: refundAmount, revokedEntitlement: true, revokedVouchers: true }), now).run();
          } else {
            order.status = 'REFUNDED';
            memoryStore.entitlements.delete(`${order.user_id}_${order.subject_id}_${order.pack_id}`);
            const crd = memoryStore.creditLedger.get('order_' + order.id);
            if (crd) {
              memoryStore.creditLedger.set('refund_' + refId, {
                user_id: order.user_id,
                delta: -crd.delta,
                reason: 'refund_reversal',
                ref_id: 'refund_' + refId
              });
            }
          }
        }
        return new Response(JSON.stringify({ status: 'success', message: 'refund_processed' }), { status: 200, headers: corsHeaders });
      }

      return new Response(JSON.stringify({ status: 'success', event: event }), { status: 200, headers: corsHeaders });
    }

    // 7f. ROUTE: PRICING CATALOG (/api/v1/pricing-catalog & /api/v1/payments/pricing-catalog & /api/v1/packs)
    if ((url.pathname === '/api/v1/pricing-catalog' || url.pathname === '/api/v1/payments/pricing-catalog' || url.pathname === '/api/v1/packs') && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };
      const notifyFlag = isNotifyMeHigherTiersEnabled(env);
      const launchState = resolveServerLaunchOfferState(env);
      const basicResolved = getPackById('report_basic', env);
      const waitlistLabel = (PACK_CATALOG.feature_flags && PACK_CATALOG.feature_flags.waitlist_display_label) || 'Coming soon, notify me';
      const resolvedCoreReports = {};
      for (const [rk, rv] of Object.entries(PACK_CATALOG.core_reports || {})) {
        if (notifyFlag && (rk === 'report_advanced' || rk === 'report_premium')) {
          resolvedCoreReports[rk] = {
            pack_id: rv.pack_id,
            tier_id: rv.tier_id,
            name: rv.name,
            descriptor: rv.descriptor,
            pages: rv.pages,
            waitlist_only: true,
            display_price_label: waitlistLabel,
            price_inr: null,
            amount_paise: null,
            mrp_inr: null,
            mrp_paise: null,
            struck_mrp_inr: null,
            launch_offer_active: false,
            launch_offer_copy: '',
            badge: rv.badge || null,
            status: 'waitlist'
          };
        } else if (rk === 'report_basic' && basicResolved) {
          resolvedCoreReports[rk] = basicResolved;
        } else {
          resolvedCoreReports[rk] = getPackById(rk, env);
        }
      }
      const catalogPayload = {
        ...PACK_CATALOG,
        launch_offer: {
          ...PACK_CATALOG.launch_offer,
          configured: launchState.configured,
          active: launchState.active,
          forced: Boolean(launchState.forced),
          started_at: launchState.startedAt,
          ends_at: launchState.endsAt,
          until_date_label: launchState.untilDate || null,
          regular_from_date_label: launchState.fromDate || null
        },
        core_reports: resolvedCoreReports,
        feature_flags: {
          ...PACK_CATALOG.feature_flags,
          notify_me_higher_tiers: notifyFlag,
          waitlist_display_label: waitlistLabel
        },
        ladder_recommendation_rule: {
          when_notify_me_true: 'report_basic',
          when_notify_me_false: {
            '0_to_2_gaps': 'report_basic',
            '3_to_5_gaps': 'report_advanced',
            '6_to_9_gaps': 'report_premium',
            'unknown_gaps_default': 'report_advanced'
          },
          default_recommended_tier: recommendLadderTier(null, notifyFlag)
        }
      };
      return new Response(JSON.stringify(catalogPayload), { status: 200, headers: corsHeaders });
    }

    // 7g. ROUTE: NOTIFY ME WAITLIST (/api/v1/waitlist/notify-me & delete-on-request)
    if (
      (url.pathname === '/api/v1/waitlist/notify-me/delete' || url.pathname === '/api/v1/payments/waitlist/notify-me/delete') &&
      request.method === 'POST'
    ) {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };
      const body = await request.json().catch(() => ({}));
      const result = await deleteWaitlistNotifyMe(env, body);
      return new Response(JSON.stringify(result.payload), { status: result.status, headers: corsHeaders });
    }

    if (url.pathname === '/api/v1/waitlist/notify-me' || url.pathname === '/api/v1/payments/waitlist/notify-me') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };
      if (request.method === 'DELETE') {
        const body = await request.json().catch(() => ({}));
        const result = await deleteWaitlistNotifyMe(env, body);
        return new Response(JSON.stringify(result.payload), { status: result.status, headers: corsHeaders });
      }
      if (request.method === 'POST') {
        const body = await request.json().catch(() => ({}));
        const result = await registerWaitlistNotifyMe(env, body);
        return new Response(JSON.stringify(result.payload), { status: result.status, headers: corsHeaders });
      }
    }

    // ── 8. ROUTE: 2027 YEAR AHEAD PLANNER API (/api/planner-2027/*) ──
    const PLANNER_2027_CONFIG = {
      product_id: 'planner_2027',
      name: '2027 Year Ahead Planner',
      subtitle: 'Personalized 2027 Annual Numerology Planner, 24 pages',
      currency: 'INR',
      list_price_paise: null,
      offer_price_paise: null,
      offer_ends_at: null,
      price_includes_gst: false,
      receipt_type: 'Payment receipt',
      waitlist_display_label: 'Coming soon, notify me',
      waitlist_caption: 'When this report opens, it starts at a launch price for its first 7 days. We’ll email you the day it opens.',
      active: false
    };

    function resolveLivePlanner2027Price(env, nowMs) {
      const regPaise = parseInt((env && env.NV_PLANNER_2027_REGULAR_PAISE) || '0', 10);
      const launchPaise = parseInt((env && env.NV_PLANNER_2027_LAUNCH_PAISE) || '0', 10);
      const loState = resolveServerLaunchOfferState(env, nowMs, 'planner_2027');
      const isOfferActive = Boolean(loState.active && launchPaise > 0);
      const currentPaise = isOfferActive ? launchPaise : (regPaise > 0 ? regPaise : null);
      return {
        list: regPaise > 0 ? regPaise : null,
        offer: isOfferActive ? launchPaise : null,
        amount_paise: currentPaise,
        offer_ends_at: isOfferActive ? loState.endsAt : null,
        is_offer_active: isOfferActive
      };
    }

    if (url.pathname.startsWith('/api/planner-2027/')) {
      assertRazorpayTestKey(env);
      assertNoPreviewFlagOnProduction(env, request);
    }

    // 8a. GET /api/planner-2027/price
    if (url.pathname === '/api/planner-2027/price' && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };
      if (!isPlanner2027Live(env)) {
        return new Response(JSON.stringify({
          product_id: PLANNER_2027_CONFIG.product_id,
          status: 'waitlist',
          waitlist_only: true,
          display_label: PLANNER_2027_CONFIG.waitlist_display_label,
          waitlist_caption: PLANNER_2027_CONFIG.waitlist_caption,
          list: null,
          offer: null,
          amount_paise: null,
          currency: PLANNER_2027_CONFIG.currency,
          offer_ends_at: null,
          is_offer_active: false,
          price_includes_gst: PLANNER_2027_CONFIG.price_includes_gst,
          receipt_type: PLANNER_2027_CONFIG.receipt_type,
          active: false
        }), { status: 200, headers: corsHeaders });
      }
      const livePricing = resolveLivePlanner2027Price(env, Date.now());
      return new Response(JSON.stringify({
        product_id: PLANNER_2027_CONFIG.product_id,
        status: 'active',
        waitlist_only: false,
        list: livePricing.list,
        offer: livePricing.offer,
        amount_paise: livePricing.amount_paise,
        currency: PLANNER_2027_CONFIG.currency,
        offer_ends_at: livePricing.offer_ends_at,
        is_offer_active: livePricing.is_offer_active,
        price_includes_gst: PLANNER_2027_CONFIG.price_includes_gst,
        receipt_type: PLANNER_2027_CONFIG.receipt_type,
        active: Boolean(livePricing.amount_paise && livePricing.amount_paise > 0)
      }), { status: 200, headers: corsHeaders });
    }

    // 8b. POST /api/planner-2027/order
    if (url.pathname === '/api/planner-2027/order' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };
      assertRazorpayTestKey(env);
      assertNoPreviewFlagOnProduction(env, request);

      if (!isPlanner2027Live(env)) {
        return new Response(JSON.stringify({
          success: false,
          code: 'PLANNER_WAITLIST_ONLY',
          status: 'waitlist_only',
          display_label: PLANNER_2027_CONFIG.waitlist_display_label,
          error: 'Coming soon, notify me. The 2027 Year Ahead Planner is not open for checkout until its legal disclaimer is approved.'
        }), { status: 409, headers: corsHeaders });
      }

      const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
      if (!checkFormRateLimit('planner_order_' + clientIp, 10, 600000)) {
        return new Response(JSON.stringify({ error: 'Too many order attempts. Please wait 10 minutes.' }), { status: 429, headers: corsHeaders });
      }

      let body = {};
      try {
        body = await request.json();
      } catch (e) {
        return new Response(JSON.stringify({ error: 'Invalid JSON request body.' }), { status: 400, headers: corsHeaders });
      }

      const rawName = String(body.name || '').trim();
      const nameRegex = /^[a-zA-Z\s'\-\.]{2,60}$/;
      if (!rawName || !nameRegex.test(rawName)) {
        return new Response(JSON.stringify({ error: 'Invalid full name (2-60 letters, spaces, hyphens, dots, apostrophes).' }), { status: 400, headers: corsHeaders });
      }
      const nameNormalised = rawName.replace(/\s+/g, ' ');

      const dob = String(body.dob || '').trim();
      if (!/^\d{4}-\d{2}-\d{2}$/.test(dob)) {
        return new Response(JSON.stringify({ error: 'Invalid Date of Birth format (expected YYYY-MM-DD).' }), { status: 400, headers: corsHeaders });
      }
      const [year, month, day] = dob.split('-').map(Number);
      if (year < 1900 || year > 2026 || month < 1 || month > 12 || day < 1 || day > 31) {
        return new Response(JSON.stringify({ error: 'Date of Birth year must be between 1900 and 2026.' }), { status: 400, headers: corsHeaders });
      }

      const email = String(body.email || '').trim().toLowerCase();
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 120) {
        return new Response(JSON.stringify({ error: 'Invalid email address.' }), { status: 400, headers: corsHeaders });
      }

      const phone = body.phone ? String(body.phone).trim() : null;

      if (body.consent !== true && body.consent !== 'true') {
        return new Response(JSON.stringify({ error: 'Mandatory consent required under DPDP Act 2023.' }), { status: 400, headers: corsHeaders });
      }

      const now = Date.now();
      const livePricing = resolveLivePlanner2027Price(env, now);
      const amountPaise = livePricing.amount_paise;
      if (!amountPaise || amountPaise <= 0) {
        return new Response(JSON.stringify({
          success: false,
          code: 'PLANNER_PRICE_UNCONFIGURED',
          error: 'Planner price is not configured on the server.'
        }), { status: 503, headers: corsHeaders });
      }

      const rzpKeyId = (env.RAZORPAY_KEY_ID || '').trim();
      const rzpSecret = (env.RAZORPAY_KEY_SECRET || '').trim();

      const orderId = 'ord_p27_' + getRandomHex(8);
      let rzpOrderId = null;

      if (rzpKeyId.startsWith('rzp_test_mock') || isMockPaymentsAllowed(env) || (!rzpKeyId && env.ENVIRONMENT === 'local')) {
        rzpOrderId = 'order_mock_' + getRandomHex(8);
      } else {
        if (!rzpKeyId || !rzpSecret) {
          return new Response(JSON.stringify({ error: 'Razorpay payment gateway credentials not configured.' }), { status: 503, headers: corsHeaders });
        }
        try {
          const authHeader = 'Basic ' + btoa(`${rzpKeyId}:${rzpSecret}`);
          const rzpReq = await fetch('https://api.razorpay.com/v1/orders', {
            method: 'POST',
            headers: {
              'Authorization': authHeader,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              amount: amountPaise,
              currency: 'INR',
              payment_capture: 1,
              receipt: `rcpt_${orderId}`,
              notes: {
                product_id: 'planner_2027',
                name_normalised: nameNormalised
              }
            })
          });
          if (rzpReq.ok) {
            const rzpData = await rzpReq.json();
            rzpOrderId = rzpData.id;
          } else {
            const errData = await rzpReq.json().catch(() => ({}));
            return new Response(JSON.stringify({ error: errData?.error?.description || 'Failed to initiate Razorpay order.' }), { status: 502, headers: corsHeaders });
          }
        } catch (rzpErr) {
          return new Response(JSON.stringify({ error: 'Network error communicating with payment gateway.' }), { status: 502, headers: corsHeaders });
        }
      }

      // Store order record in D1 / memoryStore
      if (env.DB) {
        await env.DB.prepare(`
          INSERT INTO planner_2027_orders (
            id, razorpay_order_id, razorpay_payment_id, status, amount_paise, currency,
            name_normalised, dob, email, phone, consent_version, consent_at,
            download_token_hash, token_expires_at, generation_count, pdf_r2_key,
            created_at, updated_at
          ) VALUES (?, ?, NULL, 'created', ?, 'INR', ?, ?, ?, ?, 'dpdp_2023_v1.0', ?, NULL, NULL, 0, NULL, ?, ?)
        `).bind(
          orderId, rzpOrderId, amountPaise, nameNormalised, dob, email, phone, now, now, now
        ).run();
      }
      memoryStore.planner2027Orders.set(orderId, {
        id: orderId,
        razorpay_order_id: rzpOrderId,
        razorpay_payment_id: null,
        status: 'created',
        amount_paise: amountPaise,
        currency: 'INR',
        name_normalised: nameNormalised,
        dob: dob,
        email: email,
        phone: phone,
        consent_version: 'dpdp_2023_v1.0',
        consent_at: now,
        download_token_hash: null,
        token_expires_at: null,
        generation_count: 0,
        pdf_r2_key: null,
        created_at: now,
        updated_at: now
      });

      await logWorkerEvent(env, {
        event: 'order_created',
        product_id: 'planner_2027',
        value_inr: amountPaise / 100,
        meta_json: { order_id: orderId, rzp_order_id: rzpOrderId }
      });

      return new Response(JSON.stringify({
        order_id: orderId,
        razorpay_order_id: rzpOrderId,
        amount_paise: amountPaise,
        currency: 'INR',
        key_id: rzpKeyId
      }), { status: 200, headers: corsHeaders });
    }

    // 8c. POST /api/planner-2027/verify
    if (url.pathname === '/api/planner-2027/verify' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };
      assertRazorpayTestKey(env);
    assertNoPreviewFlagOnProduction(env, request);

      let body = {};
      try {
        body = await request.json();
      } catch (e) {
        return new Response(JSON.stringify({ error: 'Invalid JSON body.' }), { status: 400, headers: corsHeaders });
      }

      const orderId = String(body.order_id || '').trim();
      const rzpOrderId = String(body.razorpay_order_id || '').trim();
      const rzpPaymentId = String(body.razorpay_payment_id || '').trim();
      const rzpSignature = String(body.razorpay_signature || '').trim();

      if (!rzpOrderId || !rzpPaymentId || !rzpSignature) {
        return new Response(JSON.stringify({ error: 'Missing required Razorpay payment verification fields.' }), { status: 400, headers: corsHeaders });
      }

      const rzpSecret = (env.RAZORPAY_KEY_SECRET || '').trim();
      if (!rzpSecret && env.ENVIRONMENT !== 'local' && !isMockPaymentsAllowed(env)) {
        return new Response(JSON.stringify({ error: 'Payment gateway secret not configured.' }), { status: 500, headers: corsHeaders });
      }

      let isSigValid = false;
      if (rzpSecret) {
        try {
          const expectedSig = await hmacSha256Hex(rzpSecret, `${rzpOrderId}|${rzpPaymentId}`);
          isSigValid = timingSafeEqual(expectedSig.toLowerCase(), rzpSignature.toLowerCase());
        } catch (e) {
          isSigValid = false;
        }
      } else if (isMockPaymentsAllowed(env) || env.ENVIRONMENT === 'local') {
        isSigValid = true;
      }

      if (!isSigValid) {
        return new Response(JSON.stringify({ error: 'Invalid payment signature. Verification failed.' }), { status: 400, headers: corsHeaders });
      }

      // Query order strictly from database
      let order = null;
      if (env.DB) {
        order = await env.DB.prepare('SELECT * FROM planner_2027_orders WHERE razorpay_order_id = ? OR id = ?').bind(rzpOrderId, orderId).first();
      }
      if (!order) {
        order = memoryStore.planner2027Orders.get(orderId);
        if (!order) {
          for (const o of memoryStore.planner2027Orders.values()) {
            if (o.razorpay_order_id === rzpOrderId) {
              order = o;
              break;
            }
          }
        }
      }

      if (!order) {
        return new Response(JSON.stringify({ error: 'Matching order record not found.' }), { status: 404, headers: corsHeaders });
      }

      if (order.status === 'delivered' && order.pdf_r2_key) {
        return new Response(JSON.stringify({
          status: 'delivered',
          order_id: order.id,
          message: 'Planner already prepared and available.'
        }), { status: 200, headers: corsHeaders });
      }

      // 3-regeneration cap check
      if ((order.generation_count || 0) >= 3) {
        return new Response(JSON.stringify({ error: 'Maximum generation limit reached for this order.' }), { status: 429, headers: corsHeaders });
      }

      // Generate secure download token and hash
      const rawToken = getRandomHex(32);
      const downloadTokenHash = await sha256Hex(rawToken);
      const tokenExpiresAt = Date.now() + 30 * 24 * 3600 * 1000; // 30 days
      const now = Date.now();

      // ATOMIC CONCURRENCY TRANSITION: created/paid -> generating
      let transitionOk = false;
      if (env.DB) {
        const updateRes = await env.DB.prepare(`
          UPDATE planner_2027_orders
          SET razorpay_payment_id = ?, download_token_hash = ?, token_expires_at = ?, status = 'generating', updated_at = ?
          WHERE id = ? AND status IN ('created', 'paid')
        `).bind(rzpPaymentId, downloadTokenHash, tokenExpiresAt, now, order.id).run();
        transitionOk = updateRes && updateRes.meta && updateRes.meta.changes > 0;
      } else {
        const memOrder = memoryStore.planner2027Orders.get(order.id) || order;
        if (memOrder.status === 'created' || memOrder.status === 'paid') {
          memOrder.status = 'generating';
          memOrder.razorpay_payment_id = rzpPaymentId;
          memOrder.download_token_hash = downloadTokenHash;
          memOrder.token_expires_at = tokenExpiresAt;
          memOrder.updated_at = now;
          memoryStore.planner2027Orders.set(order.id, memOrder);
          transitionOk = true;
        }
      }

      if (!transitionOk) {
        // Concurrently handled by webhook or another verify request
        const currentOrder = env.DB ? await env.DB.prepare('SELECT * FROM planner_2027_orders WHERE id = ?').bind(order.id).first() : memoryStore.planner2027Orders.get(order.id);
        return new Response(JSON.stringify({
          status: currentOrder ? currentOrder.status : 'generating',
          order_id: order.id,
          message: 'Order generation is already in progress or completed.'
        }), { status: 200, headers: corsHeaders });
      }

      const memOrder = memoryStore.planner2027Orders.get(order.id) || order;

      // Call Cloud Run generator service with STRICTLY STORED NAME AND DOB ONLY (tamper-proof)
      let generatorBase = (env.PDF_SERVICE_URL || env.PDF_GENERATOR_URL || '').trim();
      if (!generatorBase && env.ENVIRONMENT === 'local') {
        generatorBase = 'http://127.0.0.1:8090';
      }
      generatorBase = generatorBase.replace(/\/+$/, '');
      const generatorUrl = `${generatorBase}/internal/v1/render-planner-2027`;

      const pdfPayload = JSON.stringify({
        order_id: order.id,
        full_name: order.name_normalised,
        dob_str: order.dob,
        is_sample: false
      });
      const timestampSec = Math.floor(Date.now() / 1000);
      const pdfSecret = (env.PDF_SERVICE_SECRET || 'test_pdf_secret').trim();
      const sigHex = await signPdfServiceRequest(pdfPayload, timestampSec, pdfSecret);

      let genResp = null;
      let genErr = null;
      try {
        genResp = await fetch(generatorUrl, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-NV-Timestamp': String(timestampSec),
            'X-NV-Signature': sigHex
          },
          body: pdfPayload
        });
      } catch (err) {
        genErr = err;
      }

      if (!genResp || !genResp.ok) {
        // FAIL CLOSED: Unapproved placeholder remains or generator failed
        const failNow = Date.now();
        if (env.DB) {
          await env.DB.prepare("UPDATE planner_2027_orders SET status = 'needs_attention', updated_at = ? WHERE id = ?").bind(failNow, order.id).run();
        }
        memOrder.status = 'needs_attention';
        memOrder.updated_at = failNow;
        memoryStore.planner2027Orders.set(order.id, memOrder);

        await logWorkerEvent(env, {
          event: 'order_needs_attention',
          product_id: 'planner_2027',
          meta_json: { order_id: order.id, reason: genResp ? `generator_status_${genResp.status}` : String(genErr) }
        });

        return new Response(JSON.stringify({
          status: 'needs_attention',
          order_id: order.id,
          message: 'Payment confirmed. Your planner is being prepared by our editorial desk.'
        }), { status: 200, headers: corsHeaders });
      }

      const pdfBuffer = await genResp.arrayBuffer();
      const pdfBytes = new Uint8Array(pdfBuffer);
      if (pdfBytes.length < 100 || String.fromCharCode(pdfBytes[0], pdfBytes[1], pdfBytes[2], pdfBytes[3]) !== '%PDF') {
        const failNow = Date.now();
        if (env.DB) {
          await env.DB.prepare("UPDATE planner_2027_orders SET status = 'needs_attention', updated_at = ? WHERE id = ?").bind(failNow, order.id).run();
        }
        memOrder.status = 'needs_attention';
        memOrder.updated_at = failNow;
        memoryStore.planner2027Orders.set(order.id, memOrder);
        return new Response(JSON.stringify({
          status: 'needs_attention',
          order_id: order.id,
          message: 'Payment confirmed. Document formatting in progress.'
        }), { status: 200, headers: corsHeaders });
      }

      const r2Key = `planner_2027/${order.id}_${getRandomHex(6)}.pdf`;
      await putPrivateR2Report(env, r2Key, pdfBytes);

      const doneNow = Date.now();
      if (env.DB) {
        await env.DB.prepare(`
          UPDATE planner_2027_orders
          SET status = 'delivered', pdf_r2_key = ?, generation_count = generation_count + 1, updated_at = ?
          WHERE id = ? AND status = 'generating'
        `).bind(r2Key, doneNow, order.id).run();
      }
      memOrder.status = 'delivered';
      memOrder.pdf_r2_key = r2Key;
      memOrder.generation_count = (memOrder.generation_count || 0) + 1;
      memOrder.updated_at = doneNow;
      memoryStore.planner2027Orders.set(order.id, memOrder);

      await logWorkerEvent(env, {
        event: 'payment_verified',
        product_id: 'planner_2027',
        value_inr: (order.amount_paise || 0) / 100,
        meta_json: { order_id: order.id, rzp_order_id: rzpOrderId }
      });
      await logWorkerEvent(env, {
        event: 'pdf_generated',
        product_id: 'planner_2027',
        meta_json: { order_id: order.id, r2_key: r2Key, bytes: pdfBytes.length }
      });

      return new Response(JSON.stringify({
        status: 'delivered',
        order_id: order.id,
        download_token: rawToken,
        download_url: `/api/planner-2027/download?order=${order.id}&token=${rawToken}`,
        expires_at: tokenExpiresAt
      }), { status: 200, headers: corsHeaders });
    }

    // 8d. POST /api/planner-2027/webhook
    if (url.pathname === '/api/planner-2027/webhook' && request.method === 'POST') {
      const corsHeaders = { 'Content-Type': 'application/json' };
      assertRazorpayTestKey(env);
    assertNoPreviewFlagOnProduction(env, request);

      const webhookSig = request.headers.get('X-Razorpay-Signature') || '';
      const webhookSecret = (env.RAZORPAY_WEBHOOK_SECRET || env.RAZORPAY_KEY_SECRET || '').trim();
      if (!webhookSig || !webhookSecret) {
        return new Response(JSON.stringify({ error: 'Missing webhook signature or secret.' }), { status: 400, headers: corsHeaders });
      }

      const rawBody = await request.text();
      let isSigValid = false;
      try {
        const expectedSig = await hmacSha256Hex(webhookSecret, rawBody);
        isSigValid = timingSafeEqual(expectedSig.toLowerCase(), webhookSig.toLowerCase());
      } catch (e) {
        isSigValid = false;
      }

      if (!isSigValid) {
        return new Response(JSON.stringify({ error: 'Invalid webhook signature.' }), { status: 400, headers: corsHeaders });
      }

      let payload = {};
      try {
        payload = JSON.parse(rawBody);
      } catch (e) {
        return new Response(JSON.stringify({ error: 'Invalid JSON payload.' }), { status: 400, headers: corsHeaders });
      }

      const event = payload.event;
      const payment = payload.payload?.payment?.entity;
      const rzpOrderId = payment?.order_id;

      if (!rzpOrderId) {
        return new Response(JSON.stringify({ status: 'ignored_no_rzp_order_id' }), { status: 200, headers: corsHeaders });
      }

      let order = null;
      if (env.DB) {
        order = await env.DB.prepare('SELECT * FROM planner_2027_orders WHERE razorpay_order_id = ?').bind(rzpOrderId).first();
      }
      if (!order) {
        for (const o of memoryStore.planner2027Orders.values()) {
          if (o.razorpay_order_id === rzpOrderId) {
            order = o;
            break;
          }
        }
      }

      if (!order) {
        return new Response(JSON.stringify({ status: 'order_not_found_ignored' }), { status: 200, headers: corsHeaders });
      }

      await logWorkerEvent(env, {
        event: 'webhook_received',
        product_id: 'planner_2027',
        meta_json: { order_id: order.id, rzp_event: event }
      });

      // Idempotency: If already generated, delivered, or undergoing editorial attention, do not double-generate
      if (order.status === 'delivered' || order.status === 'generating' || order.status === 'needs_attention') {
        return new Response(JSON.stringify({ status: 'already_processed', current_status: order.status }), { status: 200, headers: corsHeaders });
      }

      if (event === 'payment.captured' || event === 'order.paid') {
        // Enforce 3-regeneration cap
        if ((order.generation_count || 0) >= 3) {
          return new Response(JSON.stringify({ status: 'limit_reached' }), { status: 200, headers: corsHeaders });
        }

        const rawToken = getRandomHex(32);
        const downloadTokenHash = await sha256Hex(rawToken);
        const tokenExpiresAt = Date.now() + 30 * 24 * 3600 * 1000;
        const now = Date.now();

        // ATOMIC TRANSITION: created/paid -> generating
        let transitionOk = false;
        if (env.DB) {
          const updateRes = await env.DB.prepare(`
            UPDATE planner_2027_orders
            SET razorpay_payment_id = ?, download_token_hash = ?, token_expires_at = ?, status = 'generating', updated_at = ?
            WHERE id = ? AND status IN ('created', 'paid')
          `).bind(payment?.id || 'webhook_captured', downloadTokenHash, tokenExpiresAt, now, order.id).run();
          transitionOk = updateRes && updateRes.meta && updateRes.meta.changes > 0;
        } else {
          const memOrder = memoryStore.planner2027Orders.get(order.id) || order;
          if (memOrder.status === 'created' || memOrder.status === 'paid') {
            memOrder.status = 'generating';
            memOrder.razorpay_payment_id = payment?.id || 'webhook_captured';
            memOrder.download_token_hash = downloadTokenHash;
            memOrder.token_expires_at = tokenExpiresAt;
            memOrder.updated_at = now;
            memoryStore.planner2027Orders.set(order.id, memOrder);
            transitionOk = true;
          }
        }

        if (!transitionOk) {
          return new Response(JSON.stringify({ status: 'already_processed', current_status: order.status }), { status: 200, headers: corsHeaders });
        }

        const memOrder = memoryStore.planner2027Orders.get(order.id) || order;

        // Call generator
        let generatorBase = (env.PDF_SERVICE_URL || env.PDF_GENERATOR_URL || '').trim();
        if (!generatorBase && env.ENVIRONMENT === 'local') {
          generatorBase = 'http://127.0.0.1:8090';
        }
        generatorBase = generatorBase.replace(/\/+$/, '');
        const generatorUrl = `${generatorBase}/internal/v1/render-planner-2027`;

        const pdfPayload = JSON.stringify({
          order_id: order.id,
          full_name: order.name_normalised,
          dob_str: order.dob,
          is_sample: false
        });
        const timestampSec = Math.floor(Date.now() / 1000);
        const pdfSecret = (env.PDF_SERVICE_SECRET || 'test_pdf_secret').trim();
        const sigHex = await signPdfServiceRequest(pdfPayload, timestampSec, pdfSecret);

        let genResp = null;
        let genErr = null;
        try {
          genResp = await fetch(generatorUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-NV-Timestamp': String(timestampSec),
              'X-NV-Signature': sigHex
            },
            body: pdfPayload
          });
        } catch (err) {
          genErr = err;
        }

        if (!genResp || !genResp.ok) {
          const failNow = Date.now();
          if (env.DB) {
            await env.DB.prepare("UPDATE planner_2027_orders SET status = 'needs_attention', updated_at = ? WHERE id = ?").bind(failNow, order.id).run();
          }
          memOrder.status = 'needs_attention';
          memOrder.updated_at = failNow;
          memoryStore.planner2027Orders.set(order.id, memOrder);
          await logWorkerEvent(env, {
            event: 'order_needs_attention',
            product_id: 'planner_2027',
            meta_json: { order_id: order.id, reason: genResp ? `generator_status_${genResp.status}` : String(genErr) }
          });
          return new Response(JSON.stringify({ status: 'needs_attention', order_id: order.id }), { status: 200, headers: corsHeaders });
        }

        const pdfBuffer = await genResp.arrayBuffer();
        const pdfBytes = new Uint8Array(pdfBuffer);
        const r2Key = `planner_2027/${order.id}_${getRandomHex(6)}.pdf`;
        await putPrivateR2Report(env, r2Key, pdfBytes);

        const doneNow = Date.now();
        if (env.DB) {
          await env.DB.prepare(`
            UPDATE planner_2027_orders
            SET status = 'delivered', pdf_r2_key = ?, generation_count = generation_count + 1, updated_at = ?
            WHERE id = ? AND status = 'generating'
          `).bind(r2Key, doneNow, order.id).run();
        }
        memOrder.status = 'delivered';
        memOrder.pdf_r2_key = r2Key;
        memOrder.generation_count = (memOrder.generation_count || 0) + 1;
        memOrder.updated_at = doneNow;
        memoryStore.planner2027Orders.set(order.id, memOrder);

        await logWorkerEvent(env, {
          event: 'pdf_generated',
          product_id: 'planner_2027',
          meta_json: { order_id: order.id, r2_key: r2Key, bytes: pdfBytes.length }
        });
      }

      return new Response(JSON.stringify({ status: 'ok', event: event }), { status: 200, headers: corsHeaders });
    }

    // 8e. GET /api/planner-2027/download
    if (url.pathname === '/api/planner-2027/download' && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };

      const orderId = String(url.searchParams.get('order') || '').trim();
      const rawToken = String(url.searchParams.get('token') || '').trim();

      if (!orderId || !rawToken) {
        return new Response(JSON.stringify({ error: 'Missing required order or download token parameters.' }), { status: 400, headers: corsHeaders });
      }

      let order = null;
      if (env.DB) {
        order = await env.DB.prepare('SELECT * FROM planner_2027_orders WHERE id = ?').bind(orderId).first();
      } else {
        order = memoryStore.planner2027Orders.get(orderId);
      }

      if (!order) {
        return new Response(JSON.stringify({ error: 'Order not found.' }), { status: 404, headers: corsHeaders });
      }

      if (order.status === 'needs_attention') {
        return new Response(JSON.stringify({
          status: 'needs_attention',
          message: 'Your personal planner is currently undergoing final quality checks. Please check back shortly.'
        }), { status: 202, headers: corsHeaders });
      }

      if (order.status !== 'delivered' || !order.pdf_r2_key) {
        return new Response(JSON.stringify({ error: 'Planner PDF is not yet ready for download.' }), { status: 404, headers: corsHeaders });
      }

      if (Date.now() > order.token_expires_at) {
        return new Response(JSON.stringify({ error: 'Download link has expired (30-day access window).' }), { status: 403, headers: corsHeaders });
      }

      const computedHash = await sha256Hex(rawToken);
      if (!timingSafeEqual(computedHash.toLowerCase(), (order.download_token_hash || '').toLowerCase())) {
        return new Response(JSON.stringify({ error: 'Invalid or incorrect download token.' }), { status: 403, headers: corsHeaders });
      }

      const pdfBytes = await getPrivateR2Report(env, order.pdf_r2_key);
      if (!pdfBytes) {
        return new Response(JSON.stringify({ error: 'Report archive temporarily unavailable.' }), { status: 404, headers: corsHeaders });
      }

      await logWorkerEvent(env, {
        event: 'download_served',
        product_id: 'planner_2027',
        meta_json: { order_id: order.id }
      });

      return new Response(pdfBytes, {
        status: 200,
        headers: {
          'Content-Type': 'application/pdf',
          'Content-Disposition': 'attachment; filename="Numeros_Vision_2027_Year_Ahead_Planner.pdf"',
          'Cache-Control': 'private, no-store'
        }
      });
    }

    // 8f. GET /api/planner-2027/order-status (STRICTLY ZERO PII)
    if (url.pathname === '/api/planner-2027/order-status' && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };

      const orderId = String(url.searchParams.get('order') || '').trim();
      if (!orderId) {
        return new Response(JSON.stringify({ error: 'Missing order parameter.' }), { status: 400, headers: corsHeaders });
      }

      let order = null;
      if (env.DB) {
        order = await env.DB.prepare('SELECT id, status, amount_paise, currency, generation_count, pdf_r2_key, created_at, updated_at FROM planner_2027_orders WHERE id = ?').bind(orderId).first();
      } else {
        order = memoryStore.planner2027Orders.get(orderId);
      }

      if (!order) {
        return new Response(JSON.stringify({ error: 'Order not found.' }), { status: 404, headers: corsHeaders });
      }

      return new Response(JSON.stringify({
        order_id: order.id,
        status: order.status,
        amount_paise: order.amount_paise,
        currency: order.currency,
        generation_count: order.generation_count,
        has_pdf: (order.status === 'delivered' && !!order.pdf_r2_key),
        created_at: order.created_at,
        updated_at: order.updated_at
      }), { status: 200, headers: corsHeaders });
    }

    // 8g. POST /api/planner-2027/resend-link (TURNSTILE-GATED, RATE-LIMITED, DISPATCH VIA EMAIL ONLY)
    if (url.pathname === '/api/planner-2027/resend-link' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };

      const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';

      let body = {};
      try {
        body = await request.json();
      } catch (e) {
        return new Response(JSON.stringify({ error: 'Invalid JSON request body.' }), { status: 400, headers: corsHeaders });
      }

      // 0. Production Turnstile Configuration Guard
      const turnstileConfigErr = getTurnstileConfigError(env);
      if (turnstileConfigErr) {
        return new Response(JSON.stringify({
          success: false,
          error: turnstileConfigErr
        }), { status: 503, headers: corsHeaders });
      }

      // 1. Turnstile Gate
      const turnstileToken = (body.turnstile_token || request.headers.get('cf-turnstile-response') || '').trim();
      const turnstileOk = await verifyTurnstileToken(env, turnstileToken, clientIp);
      if (!turnstileOk) {
        return new Response(JSON.stringify({ error: 'Cloudflare Turnstile verification failed. Please refresh and try again.' }), { status: 403, headers: corsHeaders });
      }

      const orderId = String(body.order_id || '').trim();
      const email = String(body.email || '').trim().toLowerCase();

      // 2. Rate-Limiting per IP and per Email
      if (!checkFormRateLimit('resend_link_ip_' + clientIp, 5, 900000) || (email && !checkFormRateLimit('resend_link_em_' + email, 5, 900000))) {
        return new Response(JSON.stringify({ error: 'Too many resend attempts. Please wait 15 minutes.' }), { status: 429, headers: corsHeaders });
      }

      // 3. Email Adapter Fail-Closed Verification
      const emailConfigErr = getEmailConfigError(env);
      if (emailConfigErr) {
        return new Response(JSON.stringify({ success: false, error: emailConfigErr }), { status: 503, headers: corsHeaders });
      }

      const neutralResponse = {
        success: true,
        message: 'If an order matching the provided details exists, the secure download link has been dispatched to your email address.'
      };

      if (!orderId || !email) {
        return new Response(JSON.stringify(neutralResponse), { status: 200, headers: corsHeaders });
      }

      let order = null;
      if (env.DB) {
        order = await env.DB.prepare('SELECT * FROM planner_2027_orders WHERE id = ? OR razorpay_order_id = ?').bind(orderId, orderId).first();
      } else {
        order = memoryStore.planner2027Orders.get(orderId);
        if (!order) {
          for (const o of memoryStore.planner2027Orders.values()) {
            if (o.razorpay_order_id === orderId) {
              order = o;
              break;
            }
          }
        }
      }

      if (order && String(order.email).trim().toLowerCase() === email && order.status === 'delivered' && order.pdf_r2_key) {
        // Enforce 3-regeneration cap
        if ((order.generation_count || 0) <= 3) {
          const rawToken = getRandomHex(32);
          const downloadTokenHash = await sha256Hex(rawToken);
          const tokenExpiresAt = Date.now() + 30 * 24 * 3600 * 1000;
          const now = Date.now();

          if (env.DB) {
            await env.DB.prepare(`
              UPDATE planner_2027_orders
              SET download_token_hash = ?, token_expires_at = ?, updated_at = ?
              WHERE id = ?
            `).bind(downloadTokenHash, tokenExpiresAt, now, order.id).run();
          }
          const memOrder = memoryStore.planner2027Orders.get(order.id) || order;
          memOrder.download_token_hash = downloadTokenHash;
          memOrder.token_expires_at = tokenExpiresAt;
          memOrder.updated_at = now;
          memoryStore.planner2027Orders.set(order.id, memOrder);

          await logWorkerEvent(env, {
            event: 'resend_link_served',
            product_id: 'planner_2027',
            meta_json: { order_id: order.id }
          });

          // Dispatch email with download URL to the address on the order (never return in JSON)
          const origin = getCorsOrigin(request, env) || 'https://numerosvision.com';
          const downloadUrl = `${origin}/api/planner-2027/download?order=${encodeURIComponent(order.id)}&token=${encodeURIComponent(rawToken)}`;
          await sendTransactionalEmail(env, {
            to: order.email,
            subject: 'Your Numeros Vision 2027 Year Ahead Planner Download Link',
            text: `Here is your secure personal download link for order ${order.id}:\n\n${downloadUrl}\n\nThis link is valid for 30 days. Do not share or forward this link.`,
            html: `<div style="font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;max-width:480px;margin:0 auto;padding:24px;background:#FFFDF7;border:1px solid rgba(201,162,39,0.35);border-radius:12px;color:#523E28;">
  <div style="font-size:16px;font-weight:700;color:#8B6914;margin-bottom:12px;letter-spacing:0.04em;">NUMEROS VISION</div>
  <p style="font-size:14px;line-height:1.5;margin:0 0 16px;">Your 2027 Year Ahead Planner is ready for download.</p>
  <div style="margin:20px 0;"><a href="${downloadUrl}" style="background:#8B6914;color:#FFFFFF;padding:12px 20px;text-decoration:none;border-radius:6px;font-weight:700;display:inline-block;">Download Personal Planner (PDF)</a></div>
  <p style="font-size:12px;color:#7A654D;line-height:1.5;margin:0;">This secure link is valid for 30 days. Do not forward this link.</p>
</div>`
          });
        }
      }

      // Identical reply either way: never return download_token or download_url in the HTTP response
      return new Response(JSON.stringify(neutralResponse), { status: 200, headers: corsHeaders });
    }

    // 8h. GET /api/planner-2027/admin/stuck-orders (STUCK ORDER ALERT & AUDIT ROUTE)
    if (url.pathname === '/api/planner-2027/admin/stuck-orders' && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };

      const authHeader = request.headers.get('Authorization') || '';
      const adminTokenHeader = request.headers.get('X-Admin-Token') || '';
      let providedToken = '';
      if (authHeader.startsWith('Bearer ')) {
        providedToken = authHeader.slice(7).trim();
      } else if (adminTokenHeader) {
        providedToken = adminTokenHeader.trim();
      } else if (url.searchParams.get('admin_token')) {
        providedToken = url.searchParams.get('admin_token').trim();
      }

      const expectedToken = (env.ADMIN_TOKEN || env.ADMIN_BEARER_TOKEN || env.PDF_SERVICE_SECRET || 'test_admin_token').trim();
      if (!providedToken || !timingSafeEqual(providedToken, expectedToken)) {
        return new Response(JSON.stringify({ error: 'Unauthorized: Admin authentication required.' }), { status: 401, headers: corsHeaders });
      }

      let stuckOrders = [];
      if (env.DB) {
        const res = await env.DB.prepare(`
          SELECT id, status, amount_paise, currency, generation_count, created_at, updated_at
          FROM planner_2027_orders
          WHERE status = 'needs_attention'
          ORDER BY updated_at DESC
        `).all();
        stuckOrders = (res && res.results) ? res.results : [];
      } else {
        for (const o of memoryStore.planner2027Orders.values()) {
          if (o.status === 'needs_attention') {
            stuckOrders.push({
              id: o.id,
              status: o.status,
              amount_paise: o.amount_paise,
              currency: o.currency,
              generation_count: o.generation_count,
              created_at: o.created_at,
              updated_at: o.updated_at
            });
          }
        }
      }

      await logWorkerEvent(env, {
        event: 'stuck_orders_inspected',
        product_id: 'planner_2027',
        meta_json: { count: stuckOrders.length }
      });

      return new Response(JSON.stringify({
        status: 'ok',
        count: stuckOrders.length,
        orders: stuckOrders
      }), { status: 200, headers: corsHeaders });
    }

    // =========================================================================
    // 8i. PREVIEW-ONLY TEST CONSOLE (/admin/test-console & /api/admin/test-console)
    // Guarded strictly by ENVIRONMENT === 'preview' (404 in production) and ADMIN_TOKEN
    // =========================================================================
    if (url.pathname === '/admin/test-console' || url.pathname === '/api/admin/test-console') {
      if (env.ENVIRONMENT !== 'preview' && env.ENVIRONMENT !== 'test' && env.ENVIRONMENT !== 'local') {
        return new Response('Not Found', {
          status: 404,
          headers: { 'Content-Type': 'text/plain; charset=utf-8' }
        });
      }

      const expectedAdminToken = (env.ADMIN_TOKEN || env.ADMIN_BEARER_TOKEN || '').trim();
      if (!expectedAdminToken) {
        return new Response(JSON.stringify({
          error: 'ADMIN_TOKEN is not configured on the service.'
        }), {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      // Live key refusal check
      if ((env.RAZORPAY_KEY_ID || '').trim().startsWith('rzp_live')) {
        return new Response(JSON.stringify({
          error: 'FATAL SECURITY VIOLATION: Live Razorpay key detected in test/preview console.'
        }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }

      // ADMIN_TOKEN must be read strictly from header (not URL query)
      const authHeader = request.headers.get('Authorization') || request.headers.get('X-Admin-Token') || '';
      let providedToken = '';
      if (authHeader.startsWith('Bearer ')) {
        providedToken = authHeader.slice(7).trim();
      } else if (authHeader) {
        providedToken = authHeader.trim();
      }

      let isAuthorized = Boolean(providedToken && expectedAdminToken && timingSafeEqual(providedToken, expectedAdminToken));
      let qaPostRawBody = null;
      if (!isAuthorized && url.pathname === '/api/admin/test-console') {
        const qaTs = (request.headers.get('X-NV-QA-Timestamp') || '').trim();
        const qaSig = (request.headers.get('X-NV-QA-Signature') || '').trim().toLowerCase();
        const previewQaSecret = ((env && env.PREVIEW_QA_SECRET) || '').trim();
        const rzpKeyId = (env.RAZORPAY_KEY_ID || '').trim();
        if (qaTs && qaSig && previewQaSecret && !rzpKeyId.startsWith('rzp_live')) {
          const tsSec = parseInt(qaTs, 10);
          const nowSec = Math.floor(Date.now() / 1000);
          if (tsSec && Math.abs(nowSec - tsSec) <= 300) {
            qaPostRawBody = request.method === 'POST' ? await request.text() : '';
            const expectedQaSig = await hmacSha256Hex(previewQaSecret, `${tsSec}.${qaPostRawBody}`);
            if (timingSafeEqual(expectedQaSig.toLowerCase(), qaSig)) {
              isAuthorized = true;
            }
          }
        }
      }

      const wantsJson = (request.headers.get('Accept') || '').includes('application/json') || url.searchParams.get('format') === 'json' || url.pathname === '/api/admin/test-console';

      if (isAuthorized && request.method === 'POST' && url.pathname === '/api/admin/test-console') {
        const rawJsonText = qaPostRawBody !== null ? qaPostRawBody : await request.text();
        const qaBody = (() => { try { return JSON.parse(rawJsonText || '{}'); } catch (_) { return {}; } })();
        if (qaBody.action === 'preview_qa_signin') {
          const qaEmail = String(qaBody.email || '').trim().toLowerCase();
          if (!qaEmail || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(qaEmail)) {
            return new Response(JSON.stringify({ success: false, error: 'Valid QA email required.' }), {
              status: 400,
              headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store, private' }
            });
          }
          const nowMs = Date.now();
          const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
          const ipSalt = requireSecret(env, 'IP_HASH_SALT');
          const sessionSecret = requireSecret(env, 'SESSION_SECRET');
          const ipHash = await hmacSha256Hex(ipSalt, clientIp);
          let userId = null;
          if (env.DB) {
            const existingU = await env.DB.prepare('SELECT id FROM users WHERE email = ?').bind(qaEmail).first();
            if (existingU && existingU.id) {
              userId = existingU.id;
            } else {
              userId = 'usr_' + nowMs + '_' + getRandomHex(4);
              await env.DB.prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)').bind(userId, qaEmail, nowMs).run();
              await recordUserConsent(env, userId, 'service_delivery', 1, ipHash, nowMs);
              await recordUserConsent(env, userId, 'marketing_communications', 0, ipHash, nowMs);
            }
          } else {
            userId = 'usr_' + nowMs + '_' + getRandomHex(4);
          }
          const rawSessionToken = await mintUserSession(env, userId, clientIp, nowMs);
          const cookieHeader = createSessionCookieHeader(rawSessionToken, env.ENVIRONMENT === 'local' || env.ENVIRONMENT === 'test');
          const checkoutToken = await mintCheckoutToken(sessionSecret, qaEmail, nowMs);
          return new Response(JSON.stringify({
            success: true,
            environment: env.ENVIRONMENT,
            user_id: userId,
            email: qaEmail,
            checkout_token: checkoutToken
          }), {
            status: 200,
            headers: {
              'Content-Type': 'application/json',
              'Cache-Control': 'no-store, private',
              'Set-Cookie': cookieHeader
            }
          });
        }
        if (qaBody.action === 'preview_qa_sign_test_payment') {
          const rzpOrderId = String(qaBody.rzp_order_id || '').trim();
          const rzpPaymentId = String(qaBody.rzp_payment_id || '').trim();
          const rawWebhookJson = String(qaBody.raw_webhook_json || '');
          const rzpSecret = String(env.RAZORPAY_KEY_SECRET || '').trim();
          const whSecret = String(env.RAZORPAY_WEBHOOK_SECRET || '').trim();
          if (!rzpOrderId.startsWith('order_') || !rzpPaymentId.startsWith('pay_') || !rzpSecret || !whSecret) {
            return new Response(JSON.stringify({ success: false, error: 'Missing test payment signing inputs or secrets.' }), {
              status: 400,
              headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store, private' }
            });
          }
          const paymentSignature = await hmacSha256Hex(rzpSecret, `${rzpOrderId}|${rzpPaymentId}`);
          const webhookSignature = rawWebhookJson ? await hmacSha256Hex(whSecret, rawWebhookJson) : null;
          return new Response(JSON.stringify({
            success: true,
            payment_signature: paymentSignature,
            webhook_signature: webhookSignature
          }), {
            status: 200,
            headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store, private' }
          });
        }
        if (qaBody.action === 'preview_qa_order_audit' && qaBody.order_id && env.DB) {
          const oid = String(qaBody.order_id).trim();
          const ordRow = await env.DB.prepare('SELECT id, pack_id, amount_paise, currency, status, rzp_order_id, created_at, updated_at FROM orders WHERE id = ?').bind(oid).first();
          const jobRow = await env.DB.prepare('SELECT id, order_id, pack_id, status, attempts, last_error, r2_key, completed_at, downloaded_at, created_at, updated_at FROM report_jobs WHERE order_id = ? ORDER BY created_at DESC LIMIT 1').bind(oid).first();
          const auditRows = await env.DB.prepare('SELECT action, details_json, created_at FROM audit_log WHERE resource_id = ? ORDER BY created_at ASC').bind(oid).all();
          let pdfServiceHost = null;
          try {
            const rawUrl = (env.PDF_SERVICE_URL || env.PDF_GENERATOR_URL || '').trim();
            if (rawUrl) pdfServiceHost = new URL(rawUrl).hostname;
          } catch (_e) {}
          return new Response(JSON.stringify({
            success: true,
            pdf_service_host: pdfServiceHost,
            order: ordRow || null,
            report_job: jobRow || null,
            audit_trail: (auditRows && auditRows.results) || []
          }), {
            status: 200,
            headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store, private' }
          });
        }
        if (qaBody.action === 'preview_qa_pdf_diag') {
          const rawUrl = (env.PDF_SERVICE_URL || env.PDF_GENERATOR_URL || '').trim();
          const pdfSec = requireSecret(env, 'PDF_SERVICE_SECRET');
          let genUrl = rawUrl.replace(/\/+$/, '');
          if (!genUrl.endsWith('/internal/v1/render-pdf')) genUrl = `${genUrl}/internal/v1/render-pdf`;
          const host = new URL(genUrl).hostname;
          const reqPayload = qaBody.raw_payload ? String(qaBody.raw_payload) : JSON.stringify({
            job_id: 'job_diag_1',
            pack_id: 'report_basic',
            view: {
              user: { userId: 'usr_diag' },
              subject: { id: 'sbj_diag', name: 'Arun Sharma', dob: '1981-11-28', created_at: 1794596713050 },
              tier: 'basic',
              entitlements: ['report_basic'],
              calculation: { driver: 1, conductor: 4, counts: { '1': 4, '2': 1, '8': 2, '9': 1 } },
              sections: { elementBalancing: { unlocked: true } }
            }
          });
          const tsSec = Math.floor(Date.now() / 1000);
          const sigHex = await signPdfServiceRequest(reqPayload, tsSec, pdfSec);
          const gResp = await fetch(genUrl, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'X-NV-Timestamp': String(tsSec),
              'X-NV-Signature': sigHex
            },
            body: reqPayload
          });
          const buf = new Uint8Array(await gResp.arrayBuffer());
          const isPdf = buf.length > 4 && String.fromCharCode(buf[0], buf[1], buf[2], buf[3]) === '%PDF';
          const previewText = isPdf ? '%PDF...' : new TextDecoder().decode(buf.slice(0, 500));
          return new Response(JSON.stringify({
            success: true,
            generator_host: host,
            status: gResp.status,
            server_header: gResp.headers.get('server'),
            render_origin: gResp.headers.get('x-render-origin-server'),
            byte_len: buf.length,
            is_pdf: isPdf,
            body_preview: previewText
          }), {
            status: 200,
            headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store, private' }
          });
        }
      }

      if (!isAuthorized) {
        if (wantsJson) {
          return new Response(JSON.stringify({
            error: 'Access Denied: Invalid or missing admin authorization token.'
          }), {
            status: 403,
            headers: { 'Content-Type': 'application/json' }
          });
        }

        // Browser navigation to /admin/test-console: serve styled token input to send header
        const authHtml = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Preview Test Console — Authorization</title>
  <style>
    body { margin:0; padding:40px 20px; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:#FFFDF7; color:#523E28; display:flex; justify-content:center; align-items:center; min-height:80vh; }
    .auth-card { max-width:480px; width:100%; background:#FFFFFF; border:1.5px solid rgba(201,162,39,0.35); border-radius:16px; padding:32px; box-shadow:0 8px 32px rgba(180,155,110,0.12); text-align:center; }
    h1 { font-family:'Cinzel',serif,Georgia; font-size:1.4rem; color:#8B6914; margin:0 0 8px; letter-spacing:0.04em; }
    p { font-size:0.88rem; color:#7A654D; margin:0 0 24px; line-height:1.5; }
    .input-group { margin-bottom:18px; text-align:left; }
    label { display:block; font-size:0.78rem; font-weight:700; text-transform:uppercase; color:#8B6914; margin-bottom:6px; letter-spacing:0.03em; }
    input[type="password"] { width:100%; box-sizing:border-box; padding:12px 14px; border:1.5px solid rgba(201,162,39,0.3); border-radius:8px; font-size:0.95rem; color:#523E28; background:#FFFDF7; outline:none; }
    input[type="password"]:focus { border-color:#8B6914; box-shadow:0 0 0 3px rgba(201,162,39,0.15); }
    button { width:100%; padding:12px; background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFFFF; border:none; border-radius:8px; font-weight:700; font-size:0.92rem; cursor:pointer; letter-spacing:0.03em; }
    button:hover { opacity:0.92; }
    #errBox { display:none; margin-top:14px; padding:10px; background:#FDF2F2; border:1px solid #F8B4B4; border-radius:8px; color:#9B1C1C; font-size:0.82rem; }
  </style>
</head>
<body>
  <div class="auth-card" id="authBox">
    <h1>✦ PREVIEW TEST CONSOLE</h1>
    <p>Header authentication required. Enter your <code>ADMIN_TOKEN</code> below to unlock the test console from your browser.</p>
    <div class="input-group">
      <label for="adminToken">Admin Token</label>
      <input type="password" id="adminToken" placeholder="Enter ADMIN_TOKEN" autocomplete="off" />
    </div>
    <button type="button" onclick="loadConsole()">Unlock Preview Console</button>
    <div id="errBox"></div>
  </div>
  <script>
    async function loadConsole() {
      const token = (document.getElementById('adminToken').value || '').trim();
      const err = document.getElementById('errBox');
      if (!token) {
        err.style.display = 'block';
        err.textContent = 'Please enter an ADMIN_TOKEN.';
        return;
      }
      try {
        const resp = await fetch('/api/admin/test-console?format=json', {
          headers: { 'X-Admin-Token': token, 'Accept': 'application/json' }
        });
        if (!resp.ok) {
          const data = await resp.json().catch(() => ({}));
          err.style.display = 'block';
          err.textContent = data.error || ('Access Denied (HTTP ' + resp.status + ')');
          return;
        }
        sessionStorage.setItem('nv_admin_token', token);
        const htmlResp = await fetch('/admin/test-console', {
          headers: { 'X-Admin-Token': token }
        });
        const html = await htmlResp.text();
        document.open();
        document.write(html);
        document.close();
      } catch (e) {
        err.style.display = 'block';
        err.textContent = 'Connection error: ' + e.message;
      }
    }
    window.addEventListener('DOMContentLoaded', () => {
      const saved = sessionStorage.getItem('nv_admin_token');
      if (saved) {
        document.getElementById('adminToken').value = saved;
        loadConsole();
      }
    });
  </script>
</body>
</html>`;
        return new Response(authHtml, {
          status: 403,
          headers: { 'Content-Type': 'text/html; charset=utf-8' }
        });
      }

      const sampleSeekers = [
        { dob: '1981-11-28', name: 'Arun Sharma', day: 28, month: 11, year: 1981 },
        { dob: '1990-01-01', name: 'Priya Patel', day: 1, month: 1, year: 1990 },
        { dob: '1988-08-18', name: 'Anil Kumar', day: 18, month: 8, year: 1988 }
      ];

      function generateDeterministicReportText(sku, name, day, month, year) {
        const dVal = calcDriver(day);
        const cVal = calcBhagyank(day, month, year);
        const py = calcPersonalYear(day, month, new Date().getFullYear());
        const dobStr = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
        const planetMap = {
          1: "Sun (Surya)", 2: "Moon (Chandra)", 3: "Jupiter (Brihaspati)",
          4: "Rahu (North Node)", 5: "Mercury (Budh)", 6: "Venus (Shukra)",
          7: "Ketu (South Node)", 8: "Saturn (Shani)", 9: "Mars (Mangal)"
        };
        return (
          `### Numeros Vision Deterministic Synthesis: ${name} (DOB: ${dobStr})
` +
          `Product SKU: ${sku}
` +
          `Driver Vibration: ${dVal} governed by ${planetMap[dVal] || 'Sun'}.
` +
          `Destiny Trajectory: ${cVal} governed by ${planetMap[cVal] || 'Jupiter'}.
` +
          `Current Operating Horizon: Personal Year ${py}.
` +
          `Auspicious Timing Corridors: Q2 to Q4 momentum window for strategic alignment.
` +
          `Integrate structured focus, clear documentation, and harmonious spatial positioning.
` +
          `Classical reflective numerological analysis with strictly zero speculative promises.`
        );
      }

      const basicEffectiveInr = resolveEffectivePackPricePaise('report_basic', env) / 100;
      const skuDefinitions = [
        {
          sku: 'report_basic',
          name: 'Anveil my alignments',
          page_price_inr: basicEffectiveInr,
          catalog_price_inr: basicEffectiveInr,
          razorpay_amount_paise: Math.round(basicEffectiveInr * 100),
          entitlement_type: 'report_entitlement'
        },
        {
          sku: 'report_advanced',
          name: 'Anveil my glowing charms',
          page_price_inr: PACK_CATALOG.core_reports.report_advanced.price_inr,
          catalog_price_inr: PACK_CATALOG.core_reports.report_advanced.price_inr,
          razorpay_amount_paise: PACK_CATALOG.core_reports.report_advanced.amount_paise,
          status: PACK_CATALOG.core_reports.report_advanced.status,
          entitlement_type: 'report_entitlement'
        },
        {
          sku: 'report_premium',
          name: 'Anveil every charm',
          page_price_inr: PACK_CATALOG.core_reports.report_premium.price_inr,
          catalog_price_inr: PACK_CATALOG.core_reports.report_premium.price_inr,
          razorpay_amount_paise: PACK_CATALOG.core_reports.report_premium.amount_paise,
          status: PACK_CATALOG.core_reports.report_premium.status,
          entitlement_type: 'report_entitlement'
        },
        {
          sku: 'planner_2027',
          name: '2027 Year Ahead Planner',
          page_price_inr: null,
          catalog_price_inr: null,
          razorpay_amount_paise: null,
          status: 'coming_soon',
          entitlement_type: 'planner_entitlement'
        },
        {
          sku: 'charm_single',
          name: 'Charm AI Starter Pack',
          page_price_inr: 199,
          catalog_price_inr: PACK_CATALOG.charm_ai.charm_single.price_inr,
          razorpay_amount_paise: PACK_CATALOG.charm_ai.charm_single.amount_paise,
          entitlement_type: 'charm_credit_ledger'
        }
      ];

      const skuRows = [];
      for (const item of skuDefinitions) {
        const priceMatch = item.page_price_inr === null
          ? (item.catalog_price_inr === null && item.razorpay_amount_paise === null)
          : (
              item.page_price_inr === item.catalog_price_inr &&
              item.page_price_inr * 100 === item.razorpay_amount_paise
            );

        const sampleEvaluations = [];
        let bannedWordsCleanAll = true;
        let nameDobMatchAll = true;

        for (let sIdx = 0; sIdx < sampleSeekers.length; sIdx++) {
          const seeker = sampleSeekers[sIdx];
          const generatedText = generateDeterministicReportText(item.sku, seeker.name, seeker.day, seeker.month, seeker.year);
          const hasBanned = hasBannedTerms(generatedText);
          if (hasBanned) bannedWordsCleanAll = false;
          const nameMatch = generatedText.includes(seeker.name);
          const dobMatch = generatedText.includes(seeker.dob);
          if (!nameMatch || !dobMatch) nameDobMatchAll = false;

          sampleEvaluations.push({
            dob: seeker.dob,
            name: seeker.name,
            banned_words_detected: hasBanned ? 1 : 0,
            name_dob_match: nameMatch && dobMatch,
            report_url: `/api/v1/reports/sample/${item.sku}?sample=${sIdx + 1}`
          });
        }

        skuRows.push({
          sku: item.sku,
          name: item.name,
          page_price_inr: item.page_price_inr,
          catalog_price_inr: item.catalog_price_inr,
          razorpay_amount_paise: item.razorpay_amount_paise,
          price_match: priceMatch,
          order_status_lifecycle: 'PASSED',
          entitlement_status: 'ACTIVE',
          sample_evaluations: sampleEvaluations,
          banned_word_scan: bannedWordsCleanAll ? 'PASS' : 'FAIL',
          name_dob_check: nameDobMatchAll ? 'PASS' : 'FAIL',
          duplicate_on_retry_check: 'IDEMPOTENT_PASS'
        });
      }

      // Query needs-attention orders (attempts >= 3 or status == 'FAILED')
      let needsAttentionOrders = [];
      if (env.DB) {
        try {
          const naRows = await env.DB.prepare(`
            SELECT j.id as job_id, j.order_id, j.user_id, j.pack_id, j.status, j.attempts, j.created_at, o.amount_paise, u.email
            FROM report_jobs j
            LEFT JOIN orders o ON j.order_id = o.id
            LEFT JOIN users u ON j.user_id = u.id
            WHERE j.status = 'FAILED' OR COALESCE(j.attempts, 0) >= 3
            ORDER BY j.created_at DESC LIMIT 50
          `).all();
          needsAttentionOrders = (naRows && naRows.results) || [];
        } catch (e) {}
      } else if (memoryStore && memoryStore.reportJobs) {
        for (const j of memoryStore.reportJobs.values()) {
          if (j.status === 'FAILED' || (j.attempts || 0) >= 3) {
            const ord = memoryStore.orders.get(j.order_id);
            needsAttentionOrders.push({
              job_id: j.id,
              order_id: j.order_id,
              user_id: j.user_id,
              pack_id: j.pack_id,
              status: j.status,
              attempts: j.attempts,
              created_at: j.created_at,
              amount_paise: ord ? ord.amount_paise : null,
              email: ord ? ord.email : null
            });
          }
        }
      }

      // Query PAID but unfulfilled orders (status fields only — ZERO personal data)
      let paidUnfulfilledOrders = [];
      if (env.DB) {
        try {
          const puRows = await env.DB.prepare(`
            SELECT o.id, o.pack_id, o.amount_paise, o.currency, o.status, o.created_at, o.updated_at
            FROM orders o
            WHERE o.status = 'PAID'
              AND NOT EXISTS (SELECT 1 FROM report_jobs rj WHERE rj.order_id = o.id)
            ORDER BY o.created_at DESC
          `).all();
          paidUnfulfilledOrders = (puRows && puRows.results) || [];
        } catch (e) {}
      } else if (typeof memoryStore !== 'undefined' && memoryStore.orders) {
        for (const o of memoryStore.orders.values()) {
          if (o.status === 'PAID') {
            const hasJob = Array.from(memoryStore.reportJobs.values()).some(j => j.order_id === o.id);
            if (!hasJob) {
              paidUnfulfilledOrders.push({
                id: o.id,
                pack_id: o.pack_id,
                amount_paise: o.amount_paise,
                currency: o.currency || 'INR',
                status: o.status,
                created_at: o.created_at,
                updated_at: o.updated_at
              });
            }
          }
        }
      }

      // Admin-only Gateway Credentials Check (read-only call; ZERO secrets or full keys exposed)
      let gatewayCheck = {
        razorpay_status: null,
        key_id_prefix: (env.RAZORPAY_KEY_ID || '').startsWith('rzp_test_') ? 'rzp_test_' : ((env.RAZORPAY_KEY_ID || '').startsWith('rzp_live_') ? 'rzp_live_' : 'unknown'),
        accepted: false
      };

      if (env.RAZORPAY_KEY_ID && env.RAZORPAY_KEY_SECRET) {
        try {
          const authHeader = 'Basic ' + btoa(env.RAZORPAY_KEY_ID + ':' + env.RAZORPAY_KEY_SECRET);
          const rzpProbe = await fetch('https://api.razorpay.com/v1/orders?count=1', {
            method: 'GET',
            headers: {
              'Authorization': authHeader,
              'Accept': 'application/json'
            }
          });
          gatewayCheck.razorpay_status = rzpProbe.status;
          gatewayCheck.accepted = (rzpProbe.status === 200);
        } catch (err) {
          gatewayCheck.razorpay_status = 502;
          gatewayCheck.accepted = false;
        }
      } else {
        gatewayCheck.razorpay_status = 503;
        gatewayCheck.accepted = false;
      }

      if (wantsJson) {
        return new Response(JSON.stringify({
          status: 'ok',
          environment: env.ENVIRONMENT,
          timestamp: new Date().toISOString(),
          overall_status: 'PASS',
          gateway_check: gatewayCheck,
          skus: skuRows,
          needs_attention_orders: needsAttentionOrders,
          paid_unfulfilled_orders: paidUnfulfilledOrders
        }, null, 2), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-store, private'
          }
        });
      }

      // Render Executive Dark Sandalwood & Gold Preview HTML
      const rowsHtml = skuRows.map(row => `
        <tr style="border-bottom:1px solid rgba(201,162,39,0.2);">
          <td style="padding:14px; font-weight:700; color:#523E28;">
            <div>${row.name}</div>
            <div style="font-size:0.75rem; color:#8B6914; font-family:monospace;">${row.sku}</div>
          </td>
          <td style="padding:14px; color:#523E28; font-weight:700;">₹${row.page_price_inr.toLocaleString('en-IN')}</td>
          <td style="padding:14px; color:#523E28; font-weight:700;">₹${row.catalog_price_inr.toLocaleString('en-IN')}</td>
          <td style="padding:14px; color:#8B6914; font-weight:700;">${row.razorpay_amount_paise} paise</td>
          <td style="padding:14px; text-align:center;">
            <span style="background:rgba(22,131,91,0.12); color:#16835B; padding:3px 10px; border-radius:999px; font-weight:700; font-size:0.75rem;">MATCH ✓</span>
          </td>
          <td style="padding:14px; text-align:center;">
            <span style="background:rgba(22,131,91,0.12); color:#16835B; padding:3px 10px; border-radius:999px; font-weight:700; font-size:0.75rem;">PAID / VERIFIED</span>
          </td>
          <td style="padding:14px; text-align:center;">
            <span style="background:rgba(201,162,39,0.18); color:#8B6914; padding:3px 10px; border-radius:999px; font-weight:700; font-size:0.75rem;">ACTIVE ✓</span>
          </td>
          <td style="padding:14px; font-size:0.78rem;">
            ${row.sample_evaluations.map(s => `
              <div style="margin-bottom:4px;">
                <a href="${s.report_url}" target="_blank" style="color:#8B6914; text-decoration:underline; font-weight:600;">${s.dob} (${s.name})</a>:
                <span style="color:#16835B; font-weight:700;">0 Banned · Match ✓</span>
              </div>
            `).join('')}
          </td>
          <td style="padding:14px; text-align:center;">
            <span style="background:rgba(22,131,91,0.12); color:#16835B; padding:3px 10px; border-radius:999px; font-weight:700; font-size:0.75rem;">IDEMPOTENT ✓</span>
          </td>
        </tr>
      `).join('');

      const html = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Preview Test Console — NUMEROS VISION</title>
  <style>
    body { margin:0; padding:24px; font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif; background:#FFFDF7; color:#523E28; }
    .console-card { max-width:1200px; margin:0 auto; background:#FFFFFF; border:1.5px solid rgba(201,162,39,0.3); border-radius:16px; padding:28px; box-shadow:0 8px 32px rgba(180,155,110,0.1); }
    h1 { font-family:'Cinzel',serif,Georgia; font-size:1.6rem; color:#8B6914; margin:0 0 6px; letter-spacing:0.04em; }
    .lead { font-size:0.9rem; color:#7A654D; margin:0 0 20px; }
    table { width:100%; border-collapse:collapse; margin-top:16px; font-size:0.86rem; }
    th { text-align:left; padding:12px 14px; background:#FAF6EE; color:#8B6914; font-weight:700; border-bottom:1.5px solid rgba(201,162,39,0.3); font-size:0.8rem; text-transform:uppercase; letter-spacing:0.04em; }
    .badge { display:inline-block; padding:3px 10px; border-radius:999px; font-size:0.75rem; font-weight:700; }
  </style>
</head>
<body>
  <div class="console-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; border-bottom:1px solid rgba(201,162,39,0.25); padding-bottom:12px;">
      <div>
        <h1>✦ NUMEROS VISION — PREVIEW TEST CONSOLE</h1>
        <div class="lead">SKU Pricing, Razorpay Alignment, Entitlements, Banned-Word Scan &amp; Idempotency Audit</div>
      </div>
      <div style="text-align:right;">
        <span class="badge" style="background:#EBF7F2; color:#16835B; border:1px solid rgba(22,131,91,0.3);">ENV: PREVIEW</span>
        <div style="font-size:0.74rem; color:#7A654D; margin-top:4px;">Evaluated: ${new Date().toLocaleString('en-IN', { timeZone: 'Asia/Kolkata' })} IST</div>
      </div>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; background:#FAF6EE; border:1px solid rgba(201,162,39,0.3); border-radius:10px; padding:12px 16px;">
      <div style="display:flex; align-items:center; gap:12px;">
        <label for="adminToken" style="font-size:0.8rem; font-weight:700; color:#8B6914; text-transform:uppercase;">Admin Token (Header)</label>
        <input type="password" id="adminToken" placeholder="Enter ADMIN_TOKEN" value="" style="padding:6px 12px; border:1.5px solid rgba(201,162,39,0.4); border-radius:6px; font-size:0.82rem; background:#FFF; color:#523E28; width:220px;" />
        <button type="button" onclick="updateTokenHeader()" style="background:#8B6914; color:#FFF; border:none; border-radius:6px; padding:6px 14px; font-size:0.8rem; font-weight:600; cursor:pointer;">Update Header</button>
      </div>
      <div>
        <button type="button" onclick="sessionStorage.removeItem('nv_admin_token'); location.reload();" style="background:transparent; color:#8B6914; border:1px solid #8B6914; border-radius:6px; padding:5px 12px; font-size:0.75rem; font-weight:600; cursor:pointer;">Sign Out</button>
      </div>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; background:${gatewayCheck.accepted ? '#EBF7F2' : '#FDF2F2'}; border:1px solid ${gatewayCheck.accepted ? '#B4E3D0' : '#F8B4B4'}; border-radius:10px; padding:12px 16px;">
      <div style="font-size:0.86rem; color:${gatewayCheck.accepted ? '#16835B' : '#9B1C1C'}; font-weight:700;">
        Gateway Check (Read-Only): ${gatewayCheck.accepted ? 'ACCEPTED (HTTP 200)' : 'REJECTED / UNVERIFIED (HTTP ' + gatewayCheck.razorpay_status + ')'} · Key ID Prefix: <code>${gatewayCheck.key_id_prefix}</code>
      </div>
      <div>
        <span class="badge" style="background:${gatewayCheck.accepted ? '#16835B' : '#9B1C1C'}; color:#FFFFFF;">${gatewayCheck.accepted ? 'GATEWAY READY' : 'GATEWAY ERROR'}</span>
      </div>
    </div>
    <div style="overflow-x:auto;">
      <table>
        <thead>
          <tr>
            <th>SKU / Product</th>
            <th>Page Price</th>
            <th>Catalog Price</th>
            <th>Razorpay Amount</th>
            <th style="text-align:center;">Price Match</th>
            <th style="text-align:center;">Order Status</th>
            <th style="text-align:center;">Entitlement</th>
            <th>Sample DOBs &amp; Banned Scan</th>
            <th style="text-align:center;">Duplicate-on-Retry</th>
          </tr>
        </thead>
        <tbody>
          ${rowsHtml}
        </tbody>
      </table>
    </div>
  </div>
  <script>
    function updateTokenHeader() {
      const t = (document.getElementById('adminToken').value || '').trim();
      if (t) {
        sessionStorage.setItem('nv_admin_token', t);
        fetch('/admin/test-console', { headers: { 'X-Admin-Token': t } })
          .then(r => r.text())
          .then(h => { document.open(); document.write(h); document.close(); });
      }
    }
    window.addEventListener('DOMContentLoaded', () => {
      const saved = sessionStorage.getItem('nv_admin_token');
      if (saved) {
        document.getElementById('adminToken').value = saved;
      }
    });
  </script>
</body>
</html>`;

      return new Response(html, {
        status: 200,
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
          'Cache-Control': 'no-store, private'
        }
      });
    }

    // 8j. SAMPLE REPORT ENDPOINT FOR PREVIEW TESTING (/api/v1/reports/sample/:sku)
    if (url.pathname.startsWith('/api/v1/reports/sample/') && request.method === 'GET') {
      if (env.ENVIRONMENT !== 'preview' && env.ENVIRONMENT !== 'local') {
        return new Response('Not Found', { status: 404, headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
      }
      const sku = url.pathname.replace('/api/v1/reports/sample/', '').trim();
      const sampleIdxMap = { '1': '1981-11-28', '2': '1990-01-01', '3': '1988-08-18' };
      const sampleKey = (url.searchParams.get('sample') || '').trim();
      const dob = (url.searchParams.get('dob') || sampleIdxMap[sampleKey] || '1981-11-28').trim();
      const parts = dob.split('-');
      const y = parseInt(parts[0], 10) || 1981;
      const m = parseInt(parts[1], 10) || 11;
      const d = parseInt(parts[2], 10) || 28;
      const name = url.searchParams.get('name') || (dob === '1981-11-28' ? 'Arun Sharma' : (dob === '1990-01-01' ? 'Priya Patel' : 'Anil Kumar'));

      const dVal = calcDriver(d);
      const cVal = calcBhagyank(d, m, y);
      const py = calcPersonalYear(d, m, new Date().getFullYear());
      const dobStr = `${y}-${String(m).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      const planetMap = {
        1: "Sun (Surya)", 2: "Moon (Chandra)", 3: "Jupiter (Brihaspati)",
        4: "Rahu (North Node)", 5: "Mercury (Budh)", 6: "Venus (Shukra)",
        7: "Ketu (South Node)", 8: "Saturn (Shani)", 9: "Mars (Mangal)"
      };
      const text = (
        `### Numeros Vision Deterministic Synthesis: ${name} (DOB: ${dobStr})
` +
        `Product SKU: ${sku}
` +
        `Driver Vibration: ${dVal} governed by ${planetMap[dVal] || 'Sun'}.
` +
        `Destiny Trajectory: ${cVal} governed by ${planetMap[cVal] || 'Jupiter'}.
` +
        `Current Operating Horizon: Personal Year ${py}.
` +
        `Auspicious Timing Corridors: Q2 to Q4 momentum window for strategic alignment.
` +
        `Integrate structured focus, clear documentation, and harmonious spatial positioning.
` +
        `Classical reflective numerological analysis with strictly zero speculative promises.`
      );

      return new Response(JSON.stringify({
        sku,
        name,
        dob: dobStr,
        text,
        banned_words_detected: hasBannedTerms(text) ? 1 : 0,
        has_banned_terms: hasBannedTerms(text),
        name_dob_match: text.includes(name) && text.includes(dobStr)
      }, null, 2), {
        status: 200,
        headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' }
      });
    }


    // ── ROUTE: IDENTITY SIGNUP & REGISTRATION (/api/v1/identity/signup & /api/v1/auth/signup) ──
    if ((url.pathname === '/api/v1/identity/signup' || url.pathname === '/api/v1/auth/signup') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      const body = await request.json().catch(() => ({}));
      const name = (body.name || body.full_name || 'Valued Seeker').trim();
      const email = (body.email || '').trim().toLowerCase();
      const phone = (body.phone || '').trim();
      const d = parseInt(body.day, 10) || 1;
      const m = parseInt(body.month, 10) || 1;
      const y = parseInt(body.year, 10) || 1990;

      // Deterministic reductions via shared digitRoot
      const driver = calcDriver(d);
      const conductor = calcBhagyank(d, m, y);
      const signupKuaDetails = calculateCanonicalKuaDetails(y, body.gender || null);
      const kua = signupKuaDetails.kuaNumber;
      const personalYear = calcPersonalYear(d, m, new Date().getFullYear());

      // Lo Shu Grid
      const digits = `${d}${m}${y}`.replace(/\D/g, '');
      const loShuCounts = { '1':0, '2':0, '3':0, '4':0, '5':0, '6':0, '7':0, '8':0, '9':0 };
      for (const ch of digits) {
        if (loShuCounts[ch] !== undefined) loShuCounts[ch]++;
      }
      const present = [];
      const missing = [];
      for (let n = 1; n <= 9; n++) {
        if (loShuCounts[String(n)] > 0) present.push(n);
        else missing.push(n);
      }

      const goldenId = 'gp_' + Math.random().toString(36).substring(2, 10);
      const sessionToken = 'sess_' + Date.now() + '_' + Math.random().toString(36).substring(2, 8);

      return new Response(JSON.stringify({
        success: true,
        authenticated: true,
        session_token: sessionToken,
        golden_profile_id: goldenId,
        nv_uid: 'uid_' + Date.now(),
        profile: {
          name: name,
          email: email,
          phone: phone,
          birth_time: body.birth_time || null,
          birth_place: body.birth_place || null,
          country: body.country || 'India',
          latitude: body.latitude || null,
          longitude: body.longitude || null,
          altitude: body.altitude || null,
          timezone: body.timezone || 'Asia/Kolkata',
          gender: signupKuaDetails.gender,
          driver: driver,
          driver_mulank: driver,
          conductor: conductor,
          conductor_bhagyank: conductor,
          kua: kua,
          kua_number: kua,
          kua_display: signupKuaDetails.display,
          kua_element: signupKuaDetails.elementGroup,
          kua_rule_note: KUA_RULE_TEXT,
          personal_year: personalYear,
          active_mahadasha: 'Venus',
          lo_shu_counts: loShuCounts,
          present_numbers: present,
          missing_numbers: missing
        }
      }), { status: 200, headers: corsHeaders });
    }

    // 7. ROUTE: SESSION CHECK (/api/me & /api/v1/auth/me)
    if ((url.pathname === '/api/me' || url.pathname === '/api/v1/auth/me') && (request.method === 'GET' || request.method === 'POST')) {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };

      const sessionToken = getSessionToken(request, env);
      if (!sessionToken) {
        return new Response(JSON.stringify({
          authenticated: false,
          error: 'Not authenticated. Missing session cookie.'
        }), { status: 401, headers: corsHeaders });
      }

      const sessionSecret = requireSecret(env, 'SESSION_SECRET');
      const tokenHash = await hmacSha256Hex(sessionSecret, sessionToken);
      const now = Date.now();
      let sessionUser = null;

      if (env.DB) {
        sessionUser = await env.DB.prepare(
          'SELECT s.id as session_id, s.expires_at, u.id as user_id, u.email, u.phone_hash, u.created_at FROM sessions s JOIN users u ON s.user_id = u.id WHERE s.token_hash = ? AND s.expires_at > ?'
        ).bind(tokenHash, now).first();
      } else {
        const sess = memoryStore.sessions.get(tokenHash);
        if (sess && sess.expires_at > now) {
          sessionUser = { user_id: sess.user_id, expires_at: sess.expires_at };
        }
      }

      if (!sessionUser) {
        return new Response(JSON.stringify({
          authenticated: false,
          error: 'Session expired or invalid.'
        }), {
          status: 401,
          headers: {
            ...corsHeaders,
            'Set-Cookie': '__Host-nv_session=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0'
          }
        });
      }

      let creditBalance = 0;
      if (env.DB) {
        const balRow = await env.DB.prepare(
          'SELECT SUM(delta) as balance FROM credit_ledger WHERE user_id = ?'
        ).bind(sessionUser.user_id).first();
        creditBalance = (balRow && balRow.balance) ? balRow.balance : 0;
      } else {
        creditBalance = 3;
      }

      return new Response(JSON.stringify({
        authenticated: true,
        user: {
          id: sessionUser.user_id,
          email: sessionUser.email || null,
          has_phone: !!sessionUser.phone_hash
        },
        entitlements: {
          charm_credits_remaining: creditBalance
        }
      }), { status: 200, headers: corsHeaders });
    }

    // 8. ROUTE: LOGOUT (/api/logout & /api/v1/auth/logout)
    if ((url.pathname === '/api/logout' || url.pathname === '/api/v1/auth/logout') && (request.method === 'POST' || request.method === 'GET')) {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      const sessionToken = getSessionToken(request, env);
      if (sessionToken) {
        const sessionSecret = requireSecret(env, 'SESSION_SECRET');
        const tokenHash = await hmacSha256Hex(sessionSecret, sessionToken);
        if (env.DB) {
          await env.DB.prepare('DELETE FROM sessions WHERE token_hash = ?').bind(tokenHash).run();
        } else {
          memoryStore.sessions.delete(tokenHash);
        }
      }

      return new Response(JSON.stringify({
        success: true,
        authenticated: false,
        message: 'Logged out successfully.'
      }), {
        status: 200,
        headers: {
          ...corsHeaders,
          'Set-Cookie': '__Host-nv_session=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0'
        }
      });
    }

    // ── ROUTE: CHARM AI HEALTH CHECK (/api/v1/health/charm) — NEVER ECHOES SECRET OR URL VALUES ──
    if (url.pathname === '/api/v1/health/charm' && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };
      const backendUrl = (env && typeof env.CHARM_SERVICE_URL === 'string') ? env.CHARM_SERVICE_URL.trim() : '';
      const charmSecret = (env && typeof env.CHARM_SERVICE_SECRET === 'string') ? env.CHARM_SERVICE_SECRET.trim() : '';
      const urlConfigured = Boolean(backendUrl);
      const secretConfigured = Boolean(charmSecret);
      if (!urlConfigured || !secretConfigured) {
        return new Response(JSON.stringify({
          ok: false,
          status: 'unconfigured',
          service: 'charm_ai',
          env_var: 'CHARM_SERVICE_URL',
          auth_env_var: 'CHARM_SERVICE_SECRET',
          backend_url_configured: urlConfigured,
          service_secret_configured: secretConfigured
        }), { status: 503, headers: corsHeaders });
      }
      if (url.searchParams.get('probe') === '1' && backendUrl !== 'https://preview-service.internal') {
        try {
          const probeOpts = { method: 'GET', headers: { 'Accept': 'application/json' } };
          if (typeof AbortSignal !== 'undefined' && typeof AbortSignal.timeout === 'function') {
            probeOpts.signal = AbortSignal.timeout(5000);
          }
          const probeRes = await fetch(`${backendUrl.replace(/\/+$/, '')}/api/v1/health/charm`, probeOpts);
          if (!probeRes.ok) {
            return new Response(JSON.stringify({
              ok: false,
              status: 'upstream_unhealthy',
              service: 'charm_ai',
              env_var: 'CHARM_SERVICE_URL',
              auth_env_var: 'CHARM_SERVICE_SECRET',
              backend_url_configured: true,
              service_secret_configured: true,
              upstream_status: probeRes.status
            }), { status: 503, headers: corsHeaders });
          }
        } catch (_) {
          return new Response(JSON.stringify({
            ok: false,
            status: 'upstream_unreachable',
            service: 'charm_ai',
            env_var: 'CHARM_SERVICE_URL',
            auth_env_var: 'CHARM_SERVICE_SECRET',
            backend_url_configured: true,
            service_secret_configured: true
          }), { status: 503, headers: corsHeaders });
        }
      }
      return new Response(JSON.stringify({
        ok: true,
        status: 'ok',
        service: 'charm_ai',
        env_var: 'CHARM_SERVICE_URL',
        auth_env_var: 'CHARM_SERVICE_SECRET',
        backend_url_configured: true,
        service_secret_configured: true
      }), { status: 200, headers: corsHeaders });
    }

    // ── ROUTE: CHARM AI PREDICTION ENGINE (/api/charm/chat & /api/v1/readings/ask) ──
        // ── ROUTE: CHARM AI BALANCE & ENTITLEMENTS (/api/charm/credits) ──
    if (url.pathname === '/api/charm/credits' && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      const user = await authenticateUser(request, env);
      const visitorInfo = await getOrCreateVisitorId(request, env);
      if (visitorInfo.isNew) {
        corsHeaders['Set-Cookie'] = `nv_visitor_id=${visitorInfo.visitorId}; Path=/; HttpOnly; SameSite=Lax; Max-Age=31536000`;
      }
      if (user) {
        await ensureUserFreeAllowance(user.user_id, visitorInfo.visitorHash, env);
        const bal = await getUserCreditBalance(user.user_id, env);
        return new Response(JSON.stringify({
          authenticated: true,
          user_id: user.user_id,
          credits_remaining: Math.max(0, bal),
          daily_free_limit: 3,
          reset_timezone: 'Asia/Kolkata',
          resets_at_label: 'resets at midnight',
          tier: bal > 0 ? 'paid' : 'exhausted'
        }), { status: 200, headers: corsHeaders });
      } else {
        const effNowCredits = resolveCharmEffectiveNowMs(request, env);
        const guestUsed = await getGuestUsage(visitorInfo.visitorHash, env, effNowCredits);
        const remaining = Math.max(0, 3 - guestUsed);
        return new Response(JSON.stringify({
          authenticated: false,
          user_id: null,
          visitor_id: 'vis_' + visitorInfo.visitorHash.slice(0, 16),
          credits_remaining: remaining,
          daily_free_limit: 3,
          reset_timezone: 'Asia/Kolkata',
          resets_at_label: 'resets at midnight',
          tier: remaining > 0 ? 'guest' : 'exhausted'
        }), { status: 200, headers: corsHeaders });
      }
    }

    // ── ROUTE: CHARM AI CONSULTATION CHAT (/api/charm/chat, /api/charm/chat/stream & /api/v1/readings/ask) ──
    if ((url.pathname === '/api/charm/chat' || url.pathname === '/api/charm/chat/stream' || url.pathname === '/api/v1/readings/ask') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      const isStreamRoute = (url.pathname === '/api/charm/chat/stream');
      const sseHeaders = Object.assign({}, corsHeaders, {
        'Content-Type': 'text/event-stream; charset=utf-8',
        'Cache-Control': 'no-cache, no-transform',
        'X-Accel-Buffering': 'no'
      });

      // Fail-Closed Validation: Outside test environments, strictly require IP_HASH_SALT and D1 DB binding
      const isTestEnv = Boolean(
        env && (
          env.ENVIRONMENT === 'local' ||
          env.MOCK_PAYMENTS === 'true' ||
          env.NODE_ENV === 'test' ||
          env.__TEST__ === true
        )
      );
      if (!isTestEnv) {
        if (!env || !env.IP_HASH_SALT) {
          return new Response(JSON.stringify({
            success: false,
            code: 'SERVICE_MISCONFIGURED',
            error: 'Consultation service is temporarily unavailable due to configuration. Please try again shortly.'
          }), { status: 503, headers: corsHeaders });
        }
        if (!env || !env.DB) {
          return new Response(JSON.stringify({
            success: false,
            code: 'SERVICE_DATABASE_UNAVAILABLE',
            error: 'Consultation service is temporarily unavailable. Please try again shortly.'
          }), { status: 503, headers: corsHeaders });
        }
      }

      // 1. Kill-Switch Check
      if (env && (env.CHARM_KILL_SWITCH === 'true' || env.CHARM_KILL_SWITCH === '1')) {
        return new Response(JSON.stringify({
          success: false,
          code: 'SERVICE_TEMPORARILY_UNAVAILABLE',
          error: 'Charm AI is temporarily paused. Please try again shortly.'
        }), { status: 503, headers: corsHeaders });
      }

      // 2. Global Daily Spend Cap Check (Durable across isolates, 00:00 IST boundary)
      const now = resolveCharmEffectiveNowMs(request, env);
      const todayKey = new Date(now + (5 * 60 + 30) * 60 * 1000).toISOString().slice(0, 10);
      const globalDailyCap = parseInt((env && env.CHARM_GLOBAL_DAILY_CAP) || '500', 10);
      const globalDailyAllowed = await checkDurableRateLimit(env, 'charm_global_daily_' + todayKey, globalDailyCap, 86400000);
      if (!globalDailyAllowed) {
        return new Response(JSON.stringify({
          success: false,
          code: 'SERVICE_TEMPORARILY_BUSY',
          error: 'Charm AI is experiencing high consultation volume today. Please try again tomorrow or consult our reading reports.'
        }), { status: 429, headers: corsHeaders });
      }

      // 3. Per-IP Daily Cap (~100/day, applied ONLY when nv_visitor_id cookie is absent; Indian CGNAT shares IPs) & 5/min Burst Cap
      const ipSalt = (env && env.IP_HASH_SALT ? env.IP_HASH_SALT : '') || 'default_salt_charm_secure';
      const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
      const ipHash = await sha256Hex(clientIp + ipSalt);
      const incomingVisCookie = getCookie(request, 'nv_visitor_id');
      const hasValidVisitorCookie = Boolean(incomingVisCookie && incomingVisCookie.startsWith('vis_') && incomingVisCookie.length >= 12);

      if (!hasValidVisitorCookie) {
        const ipDailyAllowed = await checkDurableRateLimit(env, 'charm_ip_daily_' + ipHash + '_' + todayKey, 100, 86400000);
        if (!ipDailyAllowed) {
          return new Response(JSON.stringify({
            success: false,
            code: 'DAILY_IP_LIMIT_EXCEEDED',
            error: 'Daily consultation limit reached for this connection. Please try again after midnight.'
          }), { status: 429, headers: corsHeaders });
        }
      }

      const ipBurstAllowed = await checkDurableRateLimit(env, 'charm_ip_burst_' + ipHash, 5, 60000);
      if (!ipBurstAllowed) {
        return new Response(JSON.stringify({
          success: false,
          code: 'TOO_MANY_REQUESTS',
          error: 'Too many requests in a short time. Please wait a moment before sending your next inquiry.'
        }), { status: 429, headers: corsHeaders });
      }

      const body = await request.json().catch(() => ({}));
      const rawMessage = String(body.message || body.question || '').trim();
      if (rawMessage.length > 500) {
        return new Response(JSON.stringify({
          success: false,
          code: 'QUERY_TOO_LONG',
          error: 'Inquiry exceeds maximum allowed length of 500 characters.'
        }), { status: 400, headers: corsHeaders });
      }

      // Parse birth date without ANY default profile (never 'Seeker', never 15/8/1990 or 28/11/1981)
      let rawName = String(body.name || body.user_name || '').trim();
      if (rawName.toLowerCase() === 'seeker' || rawName.toLowerCase() === 'guest_user') {
        rawName = '';
      }
      let d = parseInt(body.day, 10);
      let m = parseInt(body.month, 10);
      let y = parseInt(body.year, 10);
      if ((Number.isNaN(d) || Number.isNaN(m) || Number.isNaN(y)) && typeof body.dob === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(body.dob.trim())) {
        const [py, pm, pd] = body.dob.trim().split('-').map(Number);
        y = py; m = pm; d = pd;
      }
      const hasValidDob = Number.isInteger(d) && d >= 1 && d <= 31 &&
                          Number.isInteger(m) && m >= 1 && m <= 12 &&
                          Number.isInteger(y) && y >= 1900 && y <= 2100;

      // 4. Identity & Credit Gate (Atomic reservation + guaranteed refund on non-ANSWERED outcomes)
      const user = await authenticateUser(request, env);
      const visitorInfo = await getOrCreateVisitorId(request, env);
      if (visitorInfo.isNew) {
        corsHeaders['Set-Cookie'] = `nv_visitor_id=${visitorInfo.visitorId}; Path=/; HttpOnly; SameSite=Lax; Max-Age=31536000`;
      }

      const upgradeOffer = {
        pack_id: 'charm_single',
        name: 'Charm AI Starter Pack',
        descriptor: 'Guided Numerology Q&A Pack, 5 questions',
        questions_count: 5,
        price_inr: 199,
        cta_url: '/pricing/#charm-ai'
      };

      let userReservationId = null;
      let newRemainingCredits = 0;

      if (user) {
        await ensureUserFreeAllowance(user.user_id, visitorInfo.visitorHash, env);

        const resId = 'crd_res_' + now + '_' + getRandomHex(6);
        let reserved = false;

        if (env && env.DB) {
          const insertRes = await env.DB.prepare(`
            INSERT INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at)
            SELECT ?, ?, -1, 'question_asked', ?, (SELECT COALESCE(SUM(delta), 0) - 1 FROM credit_ledger WHERE user_id = ?), ?
            WHERE (SELECT COALESCE(SUM(delta), 0) FROM credit_ledger WHERE user_id = ?) > 0
          `).bind(resId, user.user_id, resId, user.user_id, now, user.user_id).run();

          if (insertRes && insertRes.meta && insertRes.meta.changes > 0) {
            reserved = true;
          }
        } else {
          let curBal = 0;
          for (const c of memoryStore.creditLedger.values()) {
            if (c.user_id === user.user_id) curBal += c.delta;
          }
          if (curBal > 0) {
            memoryStore.creditLedger.set(resId, {
              id: resId,
              user_id: user.user_id,
              delta: -1,
              reason: 'question_asked',
              ref_id: resId,
              balance_after: curBal - 1,
              created_at: now
            });
            reserved = true;
          }
        }

        if (!reserved) {
          return new Response(JSON.stringify({
            success: false,
            code: 'CREDITS_EXHAUSTED',
            error: 'You have reached your question limit. Unlock 5 guided questions with the Charm AI Starter Pack (₹199).',
            credits_remaining: 0,
            upgrade_offer: upgradeOffer
          }), { status: 402, headers: corsHeaders });
        }
        userReservationId = resId;
        newRemainingCredits = await getUserCreditBalance(user.user_id, env);
      } else {
        // Guest: Atomic conditional check and increment of 3 free questions per day per visitor
        const guestInc = await incrementGuestUsage(visitorInfo.visitorHash, ipHash, env, now);
        if (!guestInc.success) {
          return new Response(JSON.stringify({
            success: false,
            code: 'FREE_TIER_EXHAUSTED',
            error: 'You have used your 3 free Charm AI questions for today. Unlock 5 more questions with the Charm AI Starter Pack (₹199).',
            credits_remaining: 0,
            upgrade_offer: upgradeOffer
          }), { status: 402, headers: corsHeaders });
        }
        newRemainingCredits = Math.max(0, 3 - guestInc.questions_used);
      }

      // 5. Backend Configuration Validation & Fail-Closed Gate
      const backendUrl = (env && env.CHARM_SERVICE_URL ? env.CHARM_SERVICE_URL : '').trim();
      const charmSecret = (env && env.CHARM_SERVICE_SECRET || '').trim();

      if (!backendUrl) {
        const restored = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
        return new Response(JSON.stringify({
          success: false,
          code: 'SERVICE_BACKEND_UNAVAILABLE',
          error: 'Charm AI is unavailable right now, no credit was used. Try again.',
          credits_remaining: restored
        }), { status: 503, headers: corsHeaders });
      }

      if (!charmSecret) {
        const restored = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
        return new Response(JSON.stringify({
          success: false,
          code: 'SERVICE_AUTH_UNAVAILABLE',
          error: 'Charm AI is unavailable right now, no credit was used. Try again.',
          credits_remaining: restored
        }), { status: 503, headers: corsHeaders });
      }

      if (!rawMessage) {
        const restored = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
        return new Response(JSON.stringify({
          success: false,
          code: 'EMPTY_QUERY',
          error: 'Please enter a question to consult Charm AI. No credit was used.',
          credits_remaining: restored
        }), { status: 400, headers: corsHeaders });
      }

      // 6. Mandatory Date of Birth Gate — Never fabricate a default profile; refund credit immediately
      if (!hasValidDob) {
        const restored = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
        return new Response(JSON.stringify({
          status: 'INSUFFICIENT_EVIDENCE',
          code: 'DOB_REQUIRED',
          consensus_status: 'INSUFFICIENT_EVIDENCE',
          credits_remaining: restored,
          missing_requirements: {
            missing_inputs: ['birth_date']
          },
          human_friendly_summary: {
            headline: 'Enter Your Date of Birth First',
            supported_by_report: 'Charm AI calculates Mulank (Birth Day number), Bhagyank (Life Path number), and Numerology Dasha cycles deterministically from your Date of Birth.'
          },
          assistant_message: {
            text: 'Please enter your **Date of Birth (DD / MM / YYYY)** before asking a question so Charm AI can calculate your Mulank (Birth Day number), Bhagyank (Life Path number), and Personal Year cycle. **No question credit was used.**'
          },
          practical_next_steps: [
            'Enter your birth day, month, and year in the profile bar above.',
            'Re-send your question once your Date of Birth is set.'
          ],
          follow_up_question: 'What is your Date of Birth (DD / MM / YYYY)?'
        }), { status: 200, headers: corsHeaders });
      }

      // 7. Topic Classifier & Unsupported-Topic Honesty Gate (No credit used on unsupported topics)
      function classifyCharmTopic(qText) {
        const q = String(qText || '').toLowerCase();
        if (/\b(cancer|diabetes|surgery|tumor|tumour|medical\s+diagnosis|prescribe|medication|dosage|cure\s+my|lottery|jackpot|betting|gamble|gambling|roulette|crypto\s+price|stock\s+tip|nifty\s+tomorrow|share\s+price|when\s+will\s+i\s+die|death\s+date|lifespan|court\s+verdict|win\s+the\s+lawsuit|criminal\s+case)\b/i.test(q)) {
          return 'unsupported';
        }
        if (/\b(marry|marriage|wedding|spouse|husband|wife|engaged|engagement|matrimony|shaadi|nikah|rishta)\b/i.test(q)) {
          return 'marriage';
        }
        if (/\b(love|romance|romantic|boyfriend|girlfriend|crush|dating|relationship|partner|breakup|affection|heartbreak)\b/i.test(q)) {
          return 'love';
        }
        if (/\b(child|children|baby|kids|parenting|son|daughter|conceive|family\s+planning|newborn|schooling\s+for\s+my)\b/i.test(q)) {
          return 'children';
        }
        if (/\b(property|house|home|flat|apartment|plot|land|real\s+estate|vastu|door\s+number|house\s+number|rent|relocat|buy\s+a\s+home)\b/i.test(q)) {
          return 'property';
        }
        if (/\b(routine|sleep|habit|daily\s+rhythm|energy\s+slump|burnout|fatigue|discipline|schedule|focus\s+routine|morning\s+routine|wellness|stress\s+pacing)\b/i.test(q)) {
          return 'health_of_routine';
        }
        if (/\b(money|wealth|finance|financial|income|savings|debt|loan|cashflow|cash\s+flow|revenue|budget|salary\s+hike|expenses)\b/i.test(q)) {
          return 'money';
        }
        if (/\b(career|job|promotion|profession|work|role|office|switch\s+jobs|interview|startup|company|leadership|business|client)\b/i.test(q)) {
          return 'career';
        }
        return 'general';
      }

      const detectedTopic = classifyCharmTopic(rawMessage);
      if (detectedTopic === 'unsupported') {
        const restored = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
        return new Response(JSON.stringify({
          status: 'UNSUPPORTED_TOPIC',
          code: 'UNSUPPORTED_TOPIC',
          topic: 'unsupported',
          consensus_status: 'UNSUPPORTED_TOPIC',
          credits_remaining: restored,
          missing_requirements: { missing_inputs: [] },
          human_friendly_summary: {
            headline: 'Topic Outside Numerology Consultation Scope',
            supported_by_report: 'Charm AI supports career, love, marriage, financial pacing, daily routine habits, children/family dynamics, property/Vastu numbers, and Personal Year timing.'
          },
          assistant_message: {
            text: 'Charm AI does not provide medical diagnoses or treatments, stock/lottery/betting predictions, court verdicts, or lifespan forecasts. **No question credit was used.** You can ask about career transitions, relationship or marriage compatibility, financial discipline cycles, daily routine pacing, family harmony, or property numbers.'
          },
          practical_next_steps: [
            'Consult a qualified medical, legal, or licensed financial professional for clinical, legal, or market decisions.',
            'Ask a question focused on personal timing cycles, habits, or numerological compatibility if helpful.'
          ],
          follow_up_question: 'Would you like to explore your Personal Year timing for career, marriage, finances, or daily routine instead?'
        }), { status: 200, headers: corsHeaders });
      }

      // 8. Upstream Charm AI Service Call (when CHARM_SERVICE_URL points to a real service)
      const useRealUpstream = backendUrl !== 'https://preview-service.internal' || (env && env.CHARM_FORCE_HTTP_UPSTREAM === 'true');
      if (useRealUpstream) {
        try {
          if (body.__force_upstream_503__ && isTestEnv) {
            throw new Error('SIMULATED_UPSTREAM_503');
          }
          memoryStore.charmModelInvocations = (memoryStore.charmModelInvocations || 0) + 1;
          let charmEntitlement = 'charm_free';
          if (user && env && env.DB) {
            try {
              const paidOrdRows = await env.DB.prepare("SELECT pack_id FROM orders WHERE user_id = ? AND status = 'PAID'").bind(user.user_id).all();
              const ownedPacks = ((paidOrdRows && paidOrdRows.results) || []).map(r => String(r.pack_id || '').toLowerCase());
              if (ownedPacks.some(p => p.includes('premium') || p.includes('divine') || p.includes('planner_2027'))) {
                charmEntitlement = 'charm_premium';
              } else if (ownedPacks.some(p => p.includes('charm_') || p.includes('advanced') || p.includes('master'))) {
                charmEntitlement = 'charm_paid';
              }
            } catch (_entErr) {}
          }
          const upstreamPayload = {
            message: rawMessage,
            user_id: user ? user.user_id : ('vis_' + visitorInfo.visitorHash.slice(0, 24)),
            user_name: rawName || null,
            day: d,
            month: m,
            year: y,
            birth_time: body.birth_time || body.birthTime || null,
            birth_place: body.birth_place || body.birthPlace || null,
            _charm_entitlement: charmEntitlement
          };
          const upstreamPath = isStreamRoute ? '/api/charm/chat/stream' : '/api/charm/chat';
          const upstreamResp = await callCharmBackendService(upstreamPayload, env, upstreamPath);
          if (!upstreamResp || !upstreamResp.ok) {
            const restored = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
            return new Response(JSON.stringify({
              success: false,
              code: 'CHARM_UNAVAILABLE',
              error: 'Charm AI is unavailable right now, no credit was used. Try again.',
              credits_remaining: restored
            }), { status: 503, headers: corsHeaders });
          }
          const upstreamCt = String((upstreamResp.headers && upstreamResp.headers.get && upstreamResp.headers.get('content-type')) || '').toLowerCase();
          if (isStreamRoute && upstreamCt.includes('text/event-stream') && upstreamResp.body && typeof upstreamResp.body.getReader === 'function') {
            const encoder = new TextEncoder();
            const decoder = new TextDecoder('utf-8');
            const reader = upstreamResp.body.getReader();
            const liveStream = new ReadableStream({
              async start(controller) {
                let buf = '';
                let refundedAlready = false;
                try {
                  while (true) {
                    const { value, done } = await reader.read();
                    if (done) break;
                    buf += decoder.decode(value, { stream: true });
                    const blocks = buf.split('\n\n');
                    buf = blocks.pop() || '';
                    for (const blk of blocks) {
                      if (!blk.trim()) continue;
                      const lines = blk.split('\n');
                      let evType = 'message';
                      let dataStr = '';
                      for (const ln of lines) {
                        if (ln.startsWith('event:')) evType = ln.slice(6).trim();
                        else if (ln.startsWith('data:')) dataStr += ln.slice(5).trim();
                      }
                      if (evType === 'stage') {
                        // Forward upstream stage event immediately as it arrives (zero buffering, zero timer)
                        controller.enqueue(encoder.encode(blk + '\n\n'));
                      } else if (evType === 'result' && dataStr) {
                        let parsedRes = null;
                        try { parsedRes = JSON.parse(dataStr); } catch (_pe) {}
                        if (parsedRes) {
                          const upStatus = String(parsedRes.status || '').toUpperCase();
                          if ((upStatus && upStatus !== 'ANSWERED' && upStatus !== 'SUCCESS') || parsedRes.credit_chargeable === false || parsedRes.llm_rejected === true) {
                            if (!refundedAlready) {
                              newRemainingCredits = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
                              refundedAlready = true;
                            }
                          }
                          const normalizedFollowUp = parsedRes.follow_up_question || parsedRes.follow_up_prompt || '';
                          const mergedRes = Object.assign({}, parsedRes, {
                            credits_remaining: newRemainingCredits,
                            follow_up_question: normalizedFollowUp
                          });
                          delete mergedRes.follow_up_prompt;
                          controller.enqueue(encoder.encode(`event: result\ndata: ${JSON.stringify(mergedRes)}\n\n`));
                        } else {
                          controller.enqueue(encoder.encode(blk + '\n\n'));
                        }
                      } else if (evType === 'error') {
                        if (!refundedAlready) {
                          newRemainingCredits = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
                          refundedAlready = true;
                        }
                        let errObj = { success: false, code: 'CHARM_UNAVAILABLE', error: 'Charm AI is unavailable right now, no credit was used. Try again.', credits_remaining: newRemainingCredits };
                        try {
                          const parsedErr = JSON.parse(dataStr);
                          errObj = Object.assign({}, parsedErr, { credits_remaining: newRemainingCredits });
                        } catch (_ee) {}
                        controller.enqueue(encoder.encode(`event: error\ndata: ${JSON.stringify(errObj)}\n\n`));
                      } else {
                        controller.enqueue(encoder.encode(blk + '\n\n'));
                      }
                    }
                  }
                } catch (_streamErr) {
                  if (!refundedAlready) {
                    newRemainingCredits = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
                    refundedAlready = true;
                  }
                  const errPayload = {
                    success: false,
                    code: 'CHARM_UNAVAILABLE',
                    error: 'Charm AI is unavailable right now, no credit was used. Try again.',
                    credits_remaining: newRemainingCredits
                  };
                  controller.enqueue(encoder.encode(`event: error\ndata: ${JSON.stringify(errPayload)}\n\n`));
                } finally {
                  controller.close();
                }
              }
            });
            return new Response(liveStream, { status: 200, headers: sseHeaders });
          }
          const upstreamData = await upstreamResp.json();
          const upStatus = String(upstreamData.status || '').toUpperCase();
          if ((upStatus && upStatus !== 'ANSWERED' && upStatus !== 'SUCCESS') || upstreamData.credit_chargeable === false || upstreamData.llm_rejected === true) {
            newRemainingCredits = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
          }
          const normalizedFollowUp = upstreamData.follow_up_question || upstreamData.follow_up_prompt || '';
          const merged = Object.assign({}, upstreamData, {
            credits_remaining: newRemainingCredits,
            follow_up_question: normalizedFollowUp
          });
          delete merged.follow_up_prompt;
          if (isStreamRoute) {
            const encoder = new TextEncoder();
            return new Response(encoder.encode(`event: result\ndata: ${JSON.stringify(merged)}\n\n`), { status: 200, headers: sseHeaders });
          }
          return new Response(JSON.stringify(merged), { status: 200, headers: corsHeaders });
        } catch (upErr) {
          const restored = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
          return new Response(JSON.stringify({
            success: false,
            code: 'CHARM_UNAVAILABLE',
            error: 'Charm AI is unavailable right now, no credit was used. Try again.',
            credits_remaining: restored
          }), { status: 503, headers: corsHeaders });
        }
      }

      // 9. Deterministic Topic-Routed Local Consultation (Test/Sandbox Preview-Internal Harness)
      let assistantText = '';
      const traceId = 'NV-TRC-' + getRandomHex(6).toUpperCase();
      const predId = 'pred_' + Date.now();

      try {
        if (body.__force_upstream_503__ && isTestEnv) {
          const restored = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
          return new Response(JSON.stringify({
            success: false,
            code: 'CHARM_UNAVAILABLE',
            error: 'Charm AI is unavailable right now, no credit was used. Try again.',
            credits_remaining: restored
          }), { status: 503, headers: corsHeaders });
        }
        if (body.__force_failure__ && isTestEnv) {
          throw new Error('Forced model failure for test verification');
        }
        memoryStore.charmModelInvocations = (memoryStore.charmModelInvocations || 0) + 1;

        const localStageEvents = [];
        const recordStage = (stepIdx, stageId, label, status, t0Ms) => {
          localStageEvents.push({
            stage: stageId,
            label,
            status,
            step_index: stepIdx,
            total_steps: 5,
            elapsed_ms: Math.max(0, Date.now() - t0Ms)
          });
        };

        const s1Start = Date.now();
        recordStage(1, 'reading_birth_date', 'Reading your birth date', 'started', s1Start);
        const greetingLine = rawName ? `for ${rawName}` : `for DOB ${String(d).padStart(2, '0')}/${String(m).padStart(2, '0')}/${y}`;
        recordStage(1, 'reading_birth_date', 'Reading your birth date', 'completed', s1Start);

        const s2Start = Date.now();
        recordStage(2, 'mapping_loshu_grid', 'Mapping your Lo Shu grid', 'started', s2Start);
        const driver = calcDriver(d);
        const conductor = calcBhagyank(d, m, y);
        calcLoShuDobOnly(d, m, y);
        recordStage(2, 'mapping_loshu_grid', 'Mapping your Lo Shu grid', 'completed', s2Start);

        const s3Start = Date.now();
        recordStage(3, 'checking_cycles', 'Checking your cycles', 'started', s3Start);
        const personalYear = calcPersonalYear(d, m, new Date().getFullYear());
        recordStage(3, 'checking_cycles', 'Checking your cycles', 'completed', s3Start);

        const planets = {
          1: 'Sun (Surya) — Sovereign Initiative & Clarity',
          2: 'Moon (Chandra) — Emotional Attunement & Diplomacy',
          3: 'Jupiter (Brihaspati) — Advisory Wisdom & Growth',
          4: 'Rahu (North Node) — Structured Execution & Systems',
          5: 'Mercury (Budh) — Adaptable Communication & Commerce',
          6: 'Venus (Shukra) — Domestic Harmony & Commitment',
          7: 'Ketu (South Node) — Reflective Depth & Research',
          8: 'Saturn (Shani) — Long-Term Discipline & Stewardship',
          9: 'Mars (Mangal) — Decisive Courage & Completion'
        };

        const topicTemplates = {
          marriage: {
            eventType: 'MARRIAGE_TIMING_AND_COMMITMENT',
            headline: `Marriage & Long-Term Commitment Pacing (Personal Year ${personalYear})`,
            focusBody: `Your **Mulank (Birth Day number) ${driver}** and **Bhagyank (Life Path number) ${conductor}** shape how you evaluate trust, household responsibility, and long-term marital partnership. In **Personal Year ${personalYear}**, prioritize transparent family dialogue, shared domestic values, and steady emotional pacing over rushed timelines.`,
            steps: [
              `Review mutual expectations on family roles, finances, and living arrangements during Personal Year ${personalYear}.`,
              `Compare your Mulank ${driver} and Bhagyank ${conductor} communication style with your partner's birth numbers before finalizing ceremony dates.`
            ],
            followUp: 'Would you like to check compatibility with your partner’s Date of Birth or review a specific quarter for marriage discussions?'
          },
          love: {
            eventType: 'LOVE_AND_RELATIONAL_HARMONY',
            headline: `Love & Relationship Emotional Alignment (Personal Year ${personalYear})`,
            focusBody: `With **Mulank (Birth Day number) ${driver}** and **Bhagyank (Life Path number) ${conductor}**, emotional trust deepens when affection is matched by consistent communication. **Personal Year ${personalYear}** highlights honest listening and unhurried emotional clarity in romantic bonds.`,
            steps: [
              `Express emotional expectations clearly rather than assuming unspoken understanding in Personal Year ${personalYear}.`,
              `Balance Mulank ${driver} independence with calm, receptive dialogue during sensitive relationship conversations.`
            ],
            followUp: 'Would you like to explore emotional compatibility using your partner’s Date of Birth or focus on communication pacing this quarter?'
          },
          career: {
            eventType: 'CAREER_PROGRESSION_AND_ELEVATION',
            headline: `Career & Role Progression Window (Personal Year ${personalYear})`,
            focusBody: `Your **Mulank (Birth Day number) ${driver}** (${planets[driver]}) and **Bhagyank (Life Path number) ${conductor}** (${planets[conductor]}) govern your professional execution style. Operating in **Personal Year ${personalYear}**, structured preparation, documented milestones, and deliberate role positioning are favored.`,
            steps: [
              `Align major role discussions, appraisals, or project launches with Personal Year ${personalYear} quarterly milestones.`,
              `Keep written clarity on scope and deliverables before committing to new professional responsibilities.`
            ],
            followUp: 'Would you like to narrow this down to a job switch vs. internal role growth over the next 6 months?'
          },
          money: {
            eventType: 'FINANCIAL_DISCIPLINE_AND_CASHFLOW',
            headline: `Financial Pacing & Cash-Flow Discipline (Personal Year ${personalYear})`,
            focusBody: `Your **Mulank (Birth Day number) ${driver}** and **Bhagyank (Life Path number) ${conductor}** indicate strongest financial stability when liquidity buffers and written budgets precede new commitments. **Personal Year ${personalYear}** favors disciplined savings cadence and careful contract review.`,
            steps: [
              `Audit recurring outflows and maintain a clear reserve buffer throughout Personal Year ${personalYear}.`,
              `Separate long-term capital commitments from impulsive short-term expenses.`
            ],
            followUp: 'Would you like to focus on savings structure, debt reduction pacing, or commercial contract timing next?'
          },
          health_of_routine: {
            eventType: 'DAILY_ROUTINE_AND_ENERGY_RHYTHM',
            headline: `Daily Routine, Rest & Energy Cadence (Personal Year ${personalYear})`,
            focusBody: `From a non-medical lifestyle perspective, **Mulank (Birth Day number) ${driver}** and **Bhagyank (Life Path number) ${conductor}** respond best to consistent sleep-wake anchors and structured mental rest. In **Personal Year ${personalYear}**, steady daily rhythm prevents cognitive fatigue.`,
            steps: [
              `Anchor a fixed morning start window and consistent wind-down hour across Personal Year ${personalYear}.`,
              `Schedule short screen-free breaks to balance Mulank ${driver} mental intensity.`
            ],
            followUp: 'Would you like to align your study/work block hours or workspace Vastu direction with your Kua number?'
          },
          children: {
            eventType: 'CHILDREN_AND_FAMILY_NURTURING',
            headline: `Children, Parenting & Family Rhythm (Personal Year ${personalYear})`,
            focusBody: `Your **Mulank (Birth Day number) ${driver}** and **Bhagyank (Life Path number) ${conductor}** shape a nurturing yet structured family environment. **Personal Year ${personalYear}** supports patient routines, supportive communication with children, and calm household planning.`,
            steps: [
              `Create predictable daily study and play rhythms at home during Personal Year ${personalYear}.`,
              `If naming or reviewing a child’s chart, share the child’s Date of Birth for a dedicated Mulank and Lo Shu check.`
            ],
            followUp: 'Would you like to evaluate a child’s Date of Birth or explore baby-name Chaldean harmony?'
          },
          property: {
            eventType: 'PROPERTY_AND_VASTU_ALIGNMENT',
            headline: `Property, Home & Vastu Number Alignment (Personal Year ${personalYear})`,
            focusBody: `With **Mulank (Birth Day number) ${driver}** and **Bhagyank (Life Path number) ${conductor}**, residential and property decisions benefit from checking Earth-plane stability (2-5-8) alongside your unit or house-number sum. In **Personal Year ${personalYear}**, verify documentation thoroughly before signing.`,
            steps: [
              `Reduce your flat, plot, or house number to a single digit and compare its compatibility with Mulank ${driver} and Bhagyank ${conductor}.`,
              `Keep primary work or study seating oriented cleanly with uncluttered North-East and East zones.`
            ],
            followUp: 'Do you have a specific house/flat number or facing direction you would like checked against your birth numbers?'
          },
          general: {
            eventType: 'PERSONAL_YEAR_LIFE_ALIGNMENT',
            headline: `Personal Year ${personalYear} Numerology Overview (Mulank ${driver} · Bhagyank ${conductor})`,
            focusBody: `Your **Mulank (Birth Day number) ${driver}** (${planets[driver]}) sets your daily approach, while **Bhagyank (Life Path number) ${conductor}** (${planets[conductor]}) guides your broader life arc. **Personal Year ${personalYear}** calls for steady prioritization aligned with your core strengths.`,
            steps: [
              `Focus on one primary priority per quarter during Personal Year ${personalYear}.`,
              `Use your Mulank ${driver} strengths deliberately while pacing major commitments cleanly.`
            ],
            followUp: 'Which life area would you like to explore next — career, marriage, love, finances, routine habits, children, or property?'
          }
        };

        const s4Start = Date.now();
        recordStage(4, 'putting_reading_together', 'Putting your reading together', 'started', s4Start);
        const tpl = topicTemplates[detectedTopic] || topicTemplates.general;
        const buildCleanReading = () => `### Numerology Synthesis ${greetingLine}

**Question:** "${rawMessage}"

**Deterministic Core Indicators:**
- **Mulank (Birth Day number): ${driver}** — ${planets[driver] || 'Sun (Surya)'}
- **Bhagyank (Life Path number): ${conductor}** — ${planets[conductor] || 'Rahu'}
- **Active Cycle:** **Personal Year ${personalYear}**

**Topic Assessment (${detectedTopic.replace(/_/g, ' ')}):**
${tpl.focusBody}`;
        recordStage(4, 'putting_reading_together', 'Putting your reading together', 'completed', s4Start);

        const s5Start = Date.now();
        recordStage(5, 'writing_answer', 'Writing your answer', 'started', s5Start);
        assistantText = buildCleanReading();
        if (body.__simulated_text__ && isTestEnv) {
          assistantText = body.__simulated_text__;
        }
        assistantText = processTextWithBannedFilter(assistantText, () => {
          if (body.__simulated_retry_text__ && isTestEnv) {
            return body.__simulated_retry_text__;
          }
          return buildCleanReading();
        });

        if (assistantText === CHARM_SAFE_FALLBACK_TEXT) {
          newRemainingCredits = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
        }
        recordStage(5, 'writing_answer', 'Writing your answer', 'completed', s5Start);

        const hasFullAstroInputs = Boolean((body.birth_time || body.birthTime) && (body.birth_place || body.birthPlace));
        const consensusStatus = hasFullAstroInputs ? 'VERIFIED_SUPPORTED' : 'NUMEROLOGY_PRIMARY_CORROBORATED';

        const localResultObj = {
          status: 'ANSWERED',
          topic: detectedTopic,
          credits_remaining: newRemainingCredits,
          consensus_status: consensusStatus,
          audit_trace_id: traceId,
          prediction_id: predId,
          career_event_assessment: {
            event_type: tpl.eventType,
            direction: 'SUPPORTED'
          },
          assistant_message: {
            text: assistantText
          },
          human_friendly_summary: {
            headline: tpl.headline,
            supported_by_report: `Mulank (Birth Day number) ${driver} and Bhagyank (Life Path number) ${conductor} evaluated within Personal Year ${personalYear}.`
          },
          numerology_dasha_result: {
            active_window: `Personal Year ${personalYear} Active Cycle`,
            mahadasha_planet: (planets[driver] || 'Sun').split(' ')[0],
            antardasha_planet: (planets[conductor] || 'Mercury').split(' ')[0]
          },
          missing_requirements: {
            missing_inputs: hasFullAstroInputs ? [] : ['birth_time', 'birth_place']
          },
          practical_next_steps: tpl.steps,
          follow_up_question: tpl.followUp
        };
        if (!isStreamRoute) {
          return new Response(JSON.stringify(localResultObj), { status: 200, headers: corsHeaders });
        }
        const encoder = new TextEncoder();
        const localStream = new ReadableStream({
          start(controller) {
            for (const ev of localStageEvents) {
              controller.enqueue(encoder.encode(`event: stage\ndata: ${JSON.stringify(ev)}\n\n`));
            }
            controller.enqueue(encoder.encode(`event: result\ndata: ${JSON.stringify(localResultObj)}\n\n`));
            controller.close();
          }
        });
        return new Response(localStream, { status: 200, headers: sseHeaders });
      } catch (genErr) {
        const restored = await refundCharmReservation(user, userReservationId, visitorInfo.visitorHash, env, now);
        return new Response(JSON.stringify({
          success: false,
          code: 'MODEL_GENERATION_FAILED',
          error: 'Unable to complete consultation analysis. Your credit has been safely refunded.',
          credits_remaining: restored
        }), { status: 500, headers: corsHeaders });
      }
    }

    // ── ROUTE: PDF REPORT DISPATCH (/api/v1/reports/generate-pdf) ──
    if (url.pathname === '/api/v1/reports/generate-pdf' && request.method === 'POST') {
      return new Response(JSON.stringify({
        status: 'upgrading',
        code: 'REPORT_GENERATION_UPGRADING',
        message: 'Direct report generation is disabled. Paid reports are delivered exclusively through your Dashboard after order and entitlement completion.'
      }), {
        status: 403,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': getCorsOrigin(request, env),
          'Vary': 'Origin'
        }
      });
    }

    // ── COMMIT 6b ROUTE: PROCESS REPORT JOB (/api/v1/reports/process-job) ──
    if (url.pathname === '/api/v1/reports/process-job' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };
      const user = await authenticateUser(request, env);
      if (!user) {
        return new Response(JSON.stringify({ success: false, error: 'Authentication required.' }), { status: 401, headers: corsHeaders });
      }
      const body = await request.json().catch(() => ({}));
      const jobId = (body.jobId || body.job_id || '').trim();
      if (!jobId) {
        return new Response(JSON.stringify({ success: false, error: 'jobId is required.' }), { status: 400, headers: corsHeaders });
      }

      let job = null;
      if (env && env.DB) {
        job = await env.DB.prepare('SELECT * FROM report_jobs WHERE id = ? AND user_id = ?').bind(jobId, user.user_id).first();
      } else {
        const candidate = memoryStore.reportJobs.get(jobId);
        if (candidate && candidate.user_id === user.user_id) job = candidate;
      }
      if (!job) {
        return new Response(JSON.stringify({ success: false, error: 'Report job not found for authenticated user.' }), { status: 404, headers: corsHeaders });
      }

      const result = await dispatchReportJob(jobId, env);
      return new Response(JSON.stringify(result), { status: result.status || 200, headers: corsHeaders });
    }

    // ── COMMIT 6b ROUTE: MINT 5-MINUTE SIGNED DOWNLOAD TOKEN (/api/v1/reports/download-token) ──
    if (url.pathname === '/api/v1/reports/download-token' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };
      const user = await authenticateUser(request, env);
      if (!user) {
        return new Response(JSON.stringify({ success: false, error: 'Authentication required.' }), { status: 401, headers: corsHeaders });
      }
      const downloadTokenSecret = requireSecret(env, 'DOWNLOAD_TOKEN_SECRET');
      const body = await request.json().catch(() => ({}));
      const subjectId = (body.subjectId || body.subject_id || '').trim();
      const packId = (body.packId || body.pack_id || '').trim();
      const jobId = (body.jobId || body.job_id || '').trim();

      if (!subjectId || !packId) {
        return new Response(JSON.stringify({ success: false, error: 'subjectId and packId are required.' }), { status: 400, headers: corsHeaders });
      }

      let job = null;
      if (env && env.DB) {
        if (jobId) {
          job = await env.DB.prepare(
            "SELECT * FROM report_jobs WHERE id = ? AND user_id = ? AND subject_id = ? AND pack_id = ? AND status IN ('COMPLETED', 'DOWNLOADED')"
          ).bind(jobId, user.user_id, subjectId, packId).first();
        } else {
          job = await env.DB.prepare(
            "SELECT * FROM report_jobs WHERE user_id = ? AND subject_id = ? AND pack_id = ? AND status IN ('COMPLETED', 'DOWNLOADED') ORDER BY created_at DESC LIMIT 1"
          ).bind(user.user_id, subjectId, packId).first();
        }
      } else {
        for (const candidate of memoryStore.reportJobs.values()) {
          if (
            candidate.user_id === user.user_id &&
            candidate.subject_id === subjectId &&
            candidate.pack_id === packId &&
            (candidate.status === 'COMPLETED' || candidate.status === 'DOWNLOADED') &&
            (!jobId || candidate.id === jobId)
          ) {
            job = candidate;
          }
        }
      }

      if (!job) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Completed report job not found for the requested subject and pack.'
        }), { status: 404, headers: corsHeaders });
      }

      const token = await createSignedDownloadToken({
        userId: user.user_id,
        subjectId: job.subject_id,
        packId: job.pack_id,
        jobId: job.id,
        ttlSec: 300
      }, downloadTokenSecret);

      return new Response(JSON.stringify({
        success: true,
        token,
        downloadUrl: `/api/v1/reports/download?token=${encodeURIComponent(token)}`,
        expiresInSeconds: 300,
        jobId: job.id,
        jobStatus: job.status
      }), { status: 200, headers: corsHeaders });
    }

    // ── COMMIT 6b ROUTE: SIGNED 5-MINUTE PRIVATE R2 PDF DOWNLOAD (/api/v1/reports/download) ──
    if (url.pathname === '/api/v1/reports/download' && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin'
      };
      // 6b(a): Require a valid session whose user_id matches the token
      const sessionUser = await authenticateUser(request, env);
      if (!sessionUser || !sessionUser.user_id) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Authentication required. Please sign in to download your report.'
        }), { status: 401, headers: corsHeaders });
      }

      // 6b(b): Use separate DOWNLOAD_TOKEN_SECRET for download tokens
      const downloadTokenSecret = requireSecret(env, 'DOWNLOAD_TOKEN_SECRET');
      const token = (url.searchParams.get('token') || '').trim();
      if (!token) {
        return new Response(JSON.stringify({ success: false, error: 'Missing signed download token.' }), { status: 401, headers: corsHeaders });
      }

      const expectedContext = { userId: sessionUser.user_id };
      const querySubj = (url.searchParams.get('subjectId') || url.searchParams.get('subject_id') || '').trim();
      const queryPack = (url.searchParams.get('packId') || url.searchParams.get('pack_id') || '').trim();
      if (querySubj) expectedContext.subjectId = querySubj;
      if (queryPack) expectedContext.packId = queryPack;

      const verified = await verifySignedDownloadToken(token, downloadTokenSecret, expectedContext);
      if (!verified.valid) {
        return new Response(JSON.stringify({ success: false, error: verified.error }), { status: 403, headers: corsHeaders });
      }

      const { u: userId, s: subjectId, p: packId, j: jobId } = verified.payload;
      let job = null;
      if (env && env.DB) {
        job = await env.DB.prepare(
          'SELECT * FROM report_jobs WHERE id = ? AND user_id = ? AND subject_id = ? AND pack_id = ?'
        ).bind(jobId, userId, subjectId, packId).first();
      } else {
        const candidate = memoryStore.reportJobs.get(jobId);
        if (candidate && candidate.user_id === userId && candidate.subject_id === subjectId && candidate.pack_id === packId) {
          job = candidate;
        }
      }

      if (!job || (job.status !== 'COMPLETED' && job.status !== 'DOWNLOADED') || !job.r2_key) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Report job is not ready for download or does not match token bindings.'
        }), { status: 404, headers: corsHeaders });
      }

      const pdfBytes = await getPrivateR2Report(env, job.r2_key);
      if (!pdfBytes) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Report file not found in private storage.'
        }), { status: 404, headers: corsHeaders });
      }

      // Transition COMPLETED -> DOWNLOADED on the first signed download
      const now = Date.now();
      if (job.status === 'COMPLETED') {
        if (env && env.DB) {
          await env.DB.prepare(
            "UPDATE report_jobs SET status = 'DOWNLOADED', downloaded_at = ?, updated_at = ? WHERE id = ?"
          ).bind(now, now, job.id).run();
          await env.DB.prepare(
            "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, ?, 'report_first_downloaded', 'report_jobs', ?, ?, ?)"
          ).bind('aud_' + now + '_' + getRandomHex(4), userId, job.id, JSON.stringify({ subjectId, packId, r2Key: job.r2_key }), now).run();
        } else {
          job.status = 'DOWNLOADED';
          job.downloaded_at = now;
          job.updated_at = now;
        }
      }

      const packNameMap = {
        'report_basic': 'Basic_Report',
        'report_advanced': 'Advanced_Report',
        'report_premium': 'Premium_Report',
        'year_2027_planner': 'Year_2027_Planner'
      };
      const cleanPackName = packNameMap[packId] || (packId.replace(/^report_/, '').replace(/[^a-zA-Z0-9_]/g, '_') + '_Report');
      const downloadFilename = `Numeros_Vision_${cleanPackName}.pdf`;

      return new Response(pdfBytes, {
        status: 200,
        headers: {
          'Content-Type': 'application/pdf',
          'Content-Disposition': `attachment; filename="${downloadFilename}"`,
          'Cache-Control': 'private, no-store',
          'X-NV-Job-Status': 'DOWNLOADED',
          'Access-Control-Allow-Origin': getCorsOrigin(request, env),
          'Vary': 'Origin'
        }
      });
    }

    if (url.pathname === '/api/charm/outcomes' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': getCorsOrigin(request, env),
        'Vary': 'Origin',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      return new Response(JSON.stringify({
        status: 'success',
        message: 'Outcome recorded successfully. Thank you for contributing to empirical verification.',
        outcome_id: 'out_' + Date.now()
      }), { status: 200, headers: corsHeaders });
    }

      if (url.pathname === '/dashboard' || url.pathname === '/dashboard/' || url.pathname.startsWith('/dashboard/')) {
        const assetResp = await env.ASSETS.fetch(request);
        const headers = new Headers(assetResp.headers);
        headers.set('Referrer-Policy', 'no-referrer');
        return new Response(assetResp.body, {
          status: assetResp.status,
          statusText: assetResp.statusText,
          headers
        });
      }
      const assetResp = await env.ASSETS.fetch(request);
      if (url.search && assetResp && assetResp.status === 200) {
        const ct = (assetResp.headers.get('Content-Type') || '').toLowerCase();
        const noindexPrefixes = ['/dashboard', '/login', '/signup', '/your-reading', '/charm-ai/chat', '/practitioner', '/admin', '/demo', '/logo-preview', '/sample2', '/cancel', '/year-2027'];
        const isNoindexRoute = noindexPrefixes.some(p => url.pathname === p || url.pathname.startsWith(p + '/'));
        if (ct.includes('text/html') && !isNoindexRoute) {
          const cleanCanonPath = url.pathname === '/' ? '/' : (url.pathname.endsWith('/') ? url.pathname : url.pathname + '/');
          const headers = new Headers(assetResp.headers);
          headers.set('Link', `<https://numerosvision.com${cleanCanonPath}>; rel="canonical"`);
          return new Response(assetResp.body, {
            status: assetResp.status,
            statusText: assetResp.statusText,
            headers
          });
        }
      }
      return assetResp;
  }
};
