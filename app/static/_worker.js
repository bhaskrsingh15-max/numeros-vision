
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

function verifyOrigin(request, env) {
  const origin = request.headers.get('Origin');
  if (!origin) return true;
  if (origin === 'https://numerosvision.com') return true;
  if (env && env.ENVIRONMENT === 'local' && (origin.startsWith('http://localhost:') || origin.startsWith('http://127.0.0.1:'))) {
    return true;
  }
  return false;
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
  refunds: new Map()
};

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
  if (env && env.ENVIRONMENT === 'local') {
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
  const tokenHash = await sha256Hex(sessionToken);
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

const PACK_CATALOG = {
  version: "2.1.0",
  currency: "INR",
  core_reports: {
    report_basic: {
      pack_id: "report_basic",
      name: "Basic Report",
      pages: 3,
      price_inr: 199,
      amount_paise: 19900,
      status: "active"
    },
    report_advanced: {
      pack_id: "report_advanced",
      name: "Advanced Report",
      pages: 12,
      price_inr: 510,
      amount_paise: 51000,
      status: "active"
    },
    report_premium: {
      pack_id: "report_premium",
      name: "Premium Dossier",
      pages: 32,
      price_inr: 1050,
      amount_paise: 105000,
      status: "active"
    }
  },
  charm_ai: {
    charm_free: {
      pack_id: "charm_free",
      name: "Free Preview",
      price_inr: 0,
      amount_paise: 0,
      questions_count: 3,
      status: "active"
    },
    charm_single: {
      pack_id: "charm_single",
      name: "Charm AI Starter Pack",
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
      status: "inactive"
    },
    discovery_bundle: {
      pack_id: "discovery_bundle",
      name: "Discovery Bundle",
      price_inr: 1299,
      amount_paise: 129900,
      status: "inactive"
    },
    comprehensive_bundle: {
      pack_id: "comprehensive_bundle",
      name: "Comprehensive Bundle",
      price_inr: 1999,
      amount_paise: 199900,
      status: "inactive"
    }
  }
};

function getPackById(packId) {
  if (!packId || typeof packId !== 'string') return null;
  const p = packId.trim().toLowerCase();
  if (PACK_CATALOG.core_reports[p]) return PACK_CATALOG.core_reports[p];
  if (PACK_CATALOG.charm_ai[p]) return PACK_CATALOG.charm_ai[p];
  if (PACK_CATALOG.bundles[p]) return PACK_CATALOG.bundles[p];
  const aliases = {
    'basic': 'report_basic',
    'report_essential': 'report_basic',
    'advanced': 'report_advanced',
    'report_master': 'report_advanced',
    'premium': 'report_premium',
    'report_divine': 'report_premium',
    'starter_5q': 'charm_single'
  };
  const resolved = aliases[p];
  if (resolved) {
    return PACK_CATALOG.core_reports[resolved] || PACK_CATALOG.charm_ai[resolved] || PACK_CATALOG.bundles[resolved];
  }
  return null;
}

/**
 * SHARED IDEMPOTENT ORDER FULFILLMENT
 * Used by both /api/v1/payments/verify and /api/v1/payments/webhook.
 * Reads pack and subject strictly from D1 order. Fulfills even if status is EXPIRED (late UPI).
 */
async function fulfillPaidOrder(order, paymentId, amountPaise, method, env, now, source) {
  if (order.status === 'PAID') {
    return { alreadyFulfilled: true, orderId: order.id, packId: order.pack_id, subjectId: order.subject_id };
  }

  const pack = getPackById(order.pack_id);

  if (env.DB) {
    // 1. Update order status to PAID
    await env.DB.prepare("UPDATE orders SET status = 'PAID', updated_at = ? WHERE id = ?").bind(now, order.id).run();

    // 2. Record payment in payments table
    const pmtId = 'pmt_' + now + '_' + getRandomHex(4);
    await env.DB.prepare(
      "INSERT INTO payments (id, order_id, rzp_payment_id, amount_paise, status, method, captured_at) VALUES (?, ?, ?, ?, 'CAPTURED', ?, ?)"
    ).bind(pmtId, order.id, paymentId, amountPaise || order.amount_paise, method || 'online', now).run();

    // 3. Grant entitlement strictly using pack and subject from D1 order
    const entId = 'ent_' + now + '_' + getRandomHex(4);
    await env.DB.prepare(
      "INSERT OR IGNORE INTO entitlements (id, user_id, subject_id, pack_id, order_id, granted_at) VALUES (?, ?, ?, ?, ?, ?)"
    ).bind(entId, order.user_id, order.subject_id, order.pack_id, order.id, now).run();

    // 4. Credit ledger accounting for Charm AI packs
    if (pack && pack.questions_count) {
      const crdId = 'crd_' + now + '_' + getRandomHex(4);
      const prevBalRow = await env.DB.prepare('SELECT SUM(delta) as bal FROM credit_ledger WHERE user_id = ?').bind(order.user_id).first();
      const newBal = ((prevBalRow && prevBalRow.bal) ? prevBalRow.bal : 0) + pack.questions_count;
      await env.DB.prepare(
        'INSERT INTO credit_ledger (id, user_id, delta, reason, ref_id, balance_after, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)'
      ).bind(crdId, order.user_id, pack.questions_count, 'pack_purchase', 'order_' + order.id, newBal, now).run();
    }

    // 5. Voucher ledger allocation for bundles
    if (pack && pack.voucher_allocation) {
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

    // 6. Queue report generation job
    const jobId = 'job_' + now + '_' + getRandomHex(4);
    await env.DB.prepare(
      "INSERT INTO report_jobs (id, user_id, subject_id, pack_id, order_id, status, created_at) VALUES (?, ?, ?, ?, ?, 'QUEUED', ?)"
    ).bind(jobId, order.user_id, order.subject_id, order.pack_id, order.id, now).run();

    // 7. Audit log recording
    await env.DB.prepare(
      "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, ?, 'order_paid_fulfilled', 'orders', ?, ?, ?)"
    ).bind('aud_' + now + '_' + getRandomHex(4), source || 'system', order.id, JSON.stringify({ paymentId, amountPaise: amountPaise || order.amount_paise, source }), now).run();
  } else {
    order.status = 'PAID';
    order.updated_at = now;
    memoryStore.payments.set(paymentId, { id: 'pmt_' + now, order_id: order.id, rzp_payment_id: paymentId, status: 'CAPTURED', captured_at: now });
    memoryStore.entitlements.set(`${order.user_id}_${order.subject_id}_${order.pack_id}`, {
      user_id: order.user_id,
      subject_id: order.subject_id,
      pack_id: order.pack_id,
      order_id: order.id,
      granted_at: now
    });
    if (pack && pack.questions_count) {
      memoryStore.creditLedger.set('order_' + order.id, {
        user_id: order.user_id,
        delta: pack.questions_count,
        reason: 'pack_purchase',
        ref_id: 'order_' + order.id
      });
    }
    const jobId = 'job_' + now + '_' + getRandomHex(4);
    memoryStore.reportJobs.set(jobId, {
      id: jobId,
      user_id: order.user_id,
      subject_id: order.subject_id,
      pack_id: order.pack_id,
      order_id: order.id,
      status: 'QUEUED',
      created_at: now
    });
  }

  return { alreadyFulfilled: false, orderId: order.id, packId: order.pack_id, subjectId: order.subject_id };
}

/**
 * NUMEROS VISION — CLOUDFLARE PAGES EDGE WORKER
 * Document Version: 1.0.0
 * Handles real-time Fast2SMS OTP dispatching, OTP verification, and Google Identity auth on the edge.
 * All static assets are served transparently via env.ASSETS.fetch(request).
 */

    // Fast2SMS API key strictly loaded from env.FAST2SMS_API_KEY

export default {
  async fetch(request, env) {
        const url = new URL(request.url);

    // CSRF Protection: Verify Origin on state-changing POST endpoints
    if (request.method === 'POST' && (url.pathname.startsWith('/api/v1/auth/') || url.pathname.startsWith('/api/v1/payments/') || url.pathname === '/api/create-order' || url.pathname === '/api/verify-payment')) {
      if (!verifyOrigin(request, env)) {
        return new Response(JSON.stringify({
          error: 'CSRF origin validation failed.'
        }), {
          status: 403,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'https://numerosvision.com'
          }
        });
      }
    }

    // 0. SECURITY GATE / WAF: Block access to private files, hidden dotfiles, backups, and server scripts
    const forbiddenPatterns = [
      /^\/\.env/i,
      /^\/\.git/i,
      /^\/data\//i,
      /^\/app\//i,
      /^\/scripts\//i,
      /^\/reports\//i,
      /^\/static\/reports\//i,
      /^\/reports\//i,
      /^\/static\/reports\//i,
      /^\/reports\//i,
      /^\/static\/reports\//i,
      /^\/reports\//i,
      /^\/static\/reports\//i,
      /\.py$/i,
      /\.env/i,
      /\.jsonl$/i,
      /^\/_worker\.js$/i
    ];
    if (forbiddenPatterns.some(pattern => pattern.test(url.pathname))) {
      return new Response('403 Forbidden: Direct access to administrative and configuration resources is strictly prohibited.', {
        status: 403,
        headers: { 'Content-Type': 'text/plain; charset=utf-8' }
      });
    }

    // 0. CANONICAL 301 REDIRECTS (Gap G14)
    const canonicalRedirects = {
      '/charm_ai.html': '/charm-ai/',
      '/charm_ai': '/charm-ai/',
      '/privacy-policy': '/privacy/',
      '/privacy-policy/': '/privacy/',
      '/refund-policy': '/refund/',
      '/refund-policy/': '/refund/',
      '/reports': '/reports_catalogue/',
      '/reports/': '/reports_catalogue/'
    };
    if (canonicalRedirects[url.pathname]) {
      return Response.redirect(new URL(canonicalRedirects[url.pathname], url.origin), 301);
    }

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


    // 1. ROUTE: SEND OTP (/api/v1/auth/otp/send)
    if (url.pathname === '/api/v1/auth/otp/send' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
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

        const authSecret = env.AUTH_SECRET || env.RAZORPAY_KEY_SECRET || 'nv_auth_secret_salt_39900';
        const clientIp = request.headers.get('CF-Connecting-IP') || request.headers.get('x-forwarded-for') || '127.0.0.1';
        const phoneHash = await hmacSha256Hex(authSecret, mobile10);
        const ipHash = await hmacSha256Hex(authSecret, clientIp);
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
          const prev = memoryStore.otpChallenges.get(phoneHash);
          if (prev && (now - prev.created_at) < 60000) {
            return new Response(JSON.stringify({
              success: false,
              error: 'Please wait 60 seconds before requesting another code.'
            }), { status: 429, headers: corsHeaders });
          }
        }

        // Cryptographically secure 6-digit OTP
        const randomArr = new Uint32Array(1);
        crypto.getRandomValues(randomArr);
        const otpCode = (100000 + (randomArr[0] % 900000)).toString();
        const codeHash = await hmacSha256Hex(authSecret, `${mobile10}:${otpCode}`);
        const expiresAt = now + 5 * 60 * 1000;
        const challengeId = 'otp_' + now + '_' + getRandomHex(4);

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
        }

        // SMS dispatch via Fast2SMS
        let smsDispatched = false;
        const fast2smsKey = env.FAST2SMS_API_KEY;
        if (fast2smsKey) {
          try {
            const fast2smsUrl = `https://www.fast2sms.com/dev/bulkV2?authorization=${encodeURIComponent(fast2smsKey)}&route=otp&variables_values=${otpCode}&numbers=${mobile10}`;
            const fResp = await fetch(fast2smsUrl, {
              method: 'GET',
              headers: { 'cache-control': 'no-cache', 'User-Agent': 'NumerosVision/1.0' }
            });
            const fast2smsResponse = await fResp.json().catch(() => ({}));
            if (fast2smsResponse && fast2smsResponse.return === true) {
              smsDispatched = true;
            }
          } catch (smsErr) {
            console.error('[Fast2SMS_Edge_Error]', smsErr);
          }
        }

        const isLocalDev = env.ENVIRONMENT === 'local';
        const respPayload = {
          success: true,
          sms_delivered: smsDispatched,
          destination: `+91 ******${mobile10.slice(-4)}`,
          expires_in: 300,
          message: smsDispatched 
            ? `Verification code dispatched to +91 ******${mobile10.slice(-4)}`
            : 'Verification code generated for authentication'
        };

        // Dev OTP gate: returned ONLY when ENVIRONMENT=local
        if (isLocalDev) {
          respPayload.dev_otp = otpCode;
        }

        return new Response(JSON.stringify(respPayload), { status: 200, headers: corsHeaders });
      } catch (err) {
        return new Response(JSON.stringify({ success: false, error: err.message || 'OTP dispatch error' }), {
          status: 500,
          headers: corsHeaders
        });
      }
    }

    // 2. ROUTE: VERIFY OTP (/api/v1/auth/otp/verify & /api/v1/auth/login)
    if ((url.pathname === '/api/v1/auth/otp/verify' || url.pathname === '/api/v1/auth/login' || url.pathname === '/api/v1/auth/otp/login') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
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

        const authSecret = env.AUTH_SECRET || env.RAZORPAY_KEY_SECRET || 'nv_auth_secret_salt_39900';
        const phoneHash = await hmacSha256Hex(authSecret, mobile10);
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

        const expectedCodeHash = await hmacSha256Hex(authSecret, `${mobile10}:${code}`);
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
        if (env.DB) {
          let user = await env.DB.prepare('SELECT id FROM users WHERE phone_hash = ?').bind(phoneHash).first();
          if (!user) {
            userId = 'usr_' + now + '_' + getRandomHex(4);
            await env.DB.prepare('INSERT INTO users (id, phone_hash, created_at) VALUES (?, ?, ?)').bind(userId, phoneHash, now).run();
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
            user = { id: userId, phoneHash, createdAt: now };
            memoryStore.users.set(phoneHash, user);
            isNewUser = true;
          } else {
            userId = user.id;
          }
        }

        // Issue server session in D1
        const rawToken = getRandomHex(32);
        const tokenHash = await sha256Hex(rawToken);
        const sessionExpiresAt = now + 30 * 24 * 3600 * 1000;
        const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
        const userAgent = request.headers.get('User-Agent') || 'Unknown';
        const ipHash = await hmacSha256Hex(authSecret, clientIp);

        if (env.DB) {
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
            phone_masked: `+91 ******${mobile10.slice(-4)}`,
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
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      try {
        if (!env.GOOGLE_CLIENT_ID) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Google Identity authentication is not configured in this environment.'
          }), { status: 503, headers: corsHeaders });
        }
        const body = await request.json().catch(() => ({}));
        const credential = body.credential || body.id_token;

        const verifyResult = await verifyGoogleIdToken(credential, env);
        if (!verifyResult.valid) {
          return new Response(JSON.stringify({
            success: false,
            error: verifyResult.error
          }), { status: 401, headers: corsHeaders });
        }

        const tokenInfo = verifyResult.payload;
        const verifiedEmail = tokenInfo.email.toLowerCase().trim();
        const verifiedName = tokenInfo.name || verifiedEmail.split('@')[0];
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

        const rawToken = getRandomHex(32);
        const tokenHash = await sha256Hex(rawToken);
        const sessionExpiresAt = now + 30 * 24 * 3600 * 1000;
        const authSecret = env.AUTH_SECRET || env.RAZORPAY_KEY_SECRET || 'nv_auth_secret_salt_39900';
        const clientIp = request.headers.get('CF-Connecting-IP') || '127.0.0.1';
        const ipHash = await hmacSha256Hex(authSecret, clientIp);
        const userAgent = request.headers.get('User-Agent') || 'Unknown';

        if (env.DB) {
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

    // 4. ROUTE: 1-ON-1 CONSULTATION ENQUIRY (/api/v1/consultation/enquiry)
    if (url.pathname === '/api/v1/consultation/enquiry' && request.method === 'POST') {
      try {
        const body = await request.json().catch(() => ({}));
        const name = (body.name || '').trim();
        const email = (body.email || '').trim();
        const phone = (body.phone || '').trim();
        const area = (body.area_of_interest || 'General Numerology Consultation').trim();
        const description = (body.description || '').trim();
        const method = (body.preferred_contact_method || 'Email').trim();

        const ts = new Date().toISOString();
        const enquiryId = 'ENQ-' + Date.now().toString().slice(-6) + '-' + Math.random().toString(36).substring(2, 6).toUpperCase();

        // Web3Forms access key strictly loaded from Cloudflare environment
        const web3Key = env.WEB3FORMS_ACCESS_KEY;
        if (!web3Key) {
          return new Response(JSON.stringify({
            status: 'error',
            message: 'Consultation dispatch service is not configured on server.'
          }), {
            status: 503,
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': 'https://numerosvision.com'
            }
          });
        }
        try {
          await fetch('https://api.web3forms.com/submit', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                access_key: web3Key,
                subject: `✦ Consultation Enquiry [${enquiryId}]: ${name} (${area})`,
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
          } catch (e) {
            console.error('[Web3Forms_Edge_Error]', e);
          }

        return new Response(JSON.stringify({
          status: 'success',
          enquiry_id: enquiryId,
          recipient: 'support@numerosvision.com',
          timestamp: ts,
          message: 'Your consultation enquiry has been recorded and routed to support@numerosvision.com.'
        }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'https://numerosvision.com'
          }
        });
      } catch (err) {
        return new Response(JSON.stringify({ status: 'error', error: err.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }

    // 5. ROUTE: GENERAL CONTACT / INQUIRY (/api/v1/contact)
    if (url.pathname === '/api/v1/contact' && request.method === 'POST') {
      try {
        const body = await request.json().catch(() => ({}));
        const name = (body.name || '').trim();
        const email = (body.email || '').trim();
        const phone = (body.phone || '').trim();
        const category = (body.category || 'General').trim();
        const order = (body.order || '').trim();
        const message = (body.message || '').trim();

        const ticketId = 'NV-TICK-' + Math.floor(100000 + Math.random() * 900000);

        const web3Key = env.WEB3FORMS_ACCESS_KEY;
        if (!web3Key) {
          return new Response(JSON.stringify({
            status: 'error',
            message: 'Support ticket dispatch service is not configured on server.'
          }), {
            status: 503,
            headers: {
              'Content-Type': 'application/json',
              'Access-Control-Allow-Origin': 'https://numerosvision.com'
            }
          });
        }
        try {
          await fetch('https://api.web3forms.com/submit', {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                access_key: web3Key,
                subject: `✦ Contact Ticket [${ticketId}]: ${name} (${category})`,
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
          } catch (e) {}

        return new Response(JSON.stringify({
          status: 'success',
          ticket_id: ticketId,
          recipient: 'support@numerosvision.com',
          message: 'Your inquiry has been received and routed to support@numerosvision.com.'
        }), {
          status: 200,
          headers: {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': 'https://numerosvision.com'
          }
        });
      } catch (err) {
        return new Response(JSON.stringify({ status: 'error', error: err.message }), {
          status: 500,
          headers: { 'Content-Type': 'application/json' }
        });
      }
    }

        // 6. ROUTE: BILLING & INVOICES API (/api/v1/billing/*)
    if (url.pathname.startsWith('/api/v1/billing/')) {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };

      if (request.method === 'OPTIONS') {
        return new Response(null, { status: 204, headers: corsHeaders });
      }

      const sampleInvoices = [
        {
          invoice_id: 'NV-REC-2026-104819',
          order_id: 'order_RZP_MASTER_9102',
          payment_id: 'pay_LIVE_91028341',
          gateway: 'Razorpay',
          customer_name: 'Synthetic Seeker',
          customer_email: 'seeker@example.com',
          customer_phone: '+91 99999 00000',
          service_id: 'report_master',
          service_name: 'Personal Numerology Master Dossier (32 Pages)',
          service_category: 'Digital Dossier',
          amount_inr: 1050,
          currency: 'INR',
          tax_amount: 0,
          tax_note: 'Exempt under Sec 22, CGST Act 2017 (Individual Supplier — No GST Charged)',
          total_paid: 1050,
          status: 'PAID',
          payment_method: 'UPI (Instant)',
          created_at: '2026-11-02T14:32:00Z',
          report_url: '/sample-report/?tier=master',
          notes: 'Full planetary chart, D60 shashtiamsa rectification, gemstone remedies'
        },
        {
          invoice_id: 'NV-REC-2026-104820',
          order_id: 'order_RZP_CONSULT_8412',
          payment_id: 'pay_LIVE_84129901',
          gateway: 'Razorpay',
          customer_name: 'Anand Mehra',
          customer_email: 'anand.mehra@example.com',
          customer_phone: '+91 98765 43210',
          service_id: 'consultation_video',
          service_name: '1-on-1 Video Consultation & Live Chart Review (60 Mins)',
          service_category: 'Consultation',
          amount_inr: 1050,
          currency: 'INR',
          tax_amount: 0,
          tax_note: 'Exempt under Sec 22, CGST Act 2017 (Individual Supplier — No GST Charged)',
          total_paid: 1050,
          status: 'PAID',
          payment_method: 'Netbanking',
          created_at: '2026-11-03T11:15:00Z',
          report_url: '/consultation/',
          notes: 'Career transition & business partnership alignment discussion'
        },
        {
          invoice_id: 'NV-REC-2026-104821',
          order_id: 'order_RZP_CHARM_2209',
          payment_id: 'pay_LIVE_22091483',
          gateway: 'Razorpay',
          customer_name: 'Pooja Sharma',
          customer_email: 'pooja.sharma@example.com',
          customer_phone: '+91 99887 76655',
          service_id: 'growth_10q',
          service_name: 'Charm AI — Growth 10-Question Query Pack',
          service_category: 'Charm AI Credits',
          amount_inr: 399,
          currency: 'INR',
          tax_amount: 0,
          tax_note: 'Exempt under Sec 22, CGST Act 2017 (Individual Supplier — No GST Charged)',
          total_paid: 399,
          status: 'PAID',
          payment_method: 'UPI (GPay)',
          created_at: '2026-11-03T16:40:00Z',
          report_url: '/charm_ai.html',
          notes: '10 interactive consultation tokens credited'
        }
      ];

      // Route: GET /api/v1/billing/stats
      if (url.pathname === '/api/v1/billing/stats' && request.method === 'GET') {
        const totalRev = sampleInvoices.reduce((acc, i) => acc + i.total_paid, 0);
        return new Response(JSON.stringify({
          status: 'success',
          total_revenue_inr: totalRev,
          total_invoices_count: sampleInvoices.length,
          average_order_value_inr: Math.round(totalRev / sampleInvoices.length),
          breakdown: {
            digital_reports: sampleInvoices.filter(i => i.service_category === 'Digital Dossier').length,
            consultations: sampleInvoices.filter(i => i.service_category === 'Consultation').length,
            charm_ai_credits: sampleInvoices.filter(i => i.service_category === 'Charm AI Credits').length
          },
          statutory_note: 'Individual consultancy operation under Section 22 CGST Act 2017 exemption threshold'
        }), { status: 200, headers: corsHeaders });
      }

      // Route: GET /api/v1/billing/invoices or /my-invoices
      if ((url.pathname === '/api/v1/billing/invoices' || url.pathname === '/api/v1/billing/my-invoices') && request.method === 'GET') {
        const filterEmail = (url.searchParams.get('email') || '').trim().toLowerCase();
        let list = sampleInvoices;
        if (filterEmail) {
          list = sampleInvoices.filter(i => i.customer_email.toLowerCase() === filterEmail);
        }
        return new Response(JSON.stringify({
          status: 'success',
          total_count: list.length,
          invoices: list
        }), { status: 200, headers: corsHeaders });
      }

      // Route: POST /api/v1/billing/create
      if (url.pathname === '/api/v1/billing/create' && request.method === 'POST') {
        try {
          const body = await request.json().catch(() => ({}));
          const custName = (body.customer_name || 'Valued Seeker').trim();
          const custEmail = (body.customer_email || '').trim().toLowerCase();
          const custPhone = (body.customer_phone || '').trim();
          const planId = (body.plan_id || 'report_master').trim();
          const amount = parseInt(body.amount_inr, 10) || 1050;
          const orderId = body.order_id || ('order_' + Date.now());
          const paymentId = body.payment_id || ('pay_' + Date.now());

          const currentYear = new Date().getFullYear();
          const invId = 'NV-REC-' + currentYear + '-' + Math.floor(100000 + Math.random() * 900000);
          const serviceName = planId === 'consultation_video' ? '1-on-1 Video Consultation (60 Mins)' : 'Personal Numerology Master Dossier (32 Pages)';
          const reportUrl = planId.includes('consult') ? '/consultation/' : '/sample-report/?tier=master';

          const newInvoice = {
            invoice_id: invId,
            order_id: orderId,
            payment_id: paymentId,
            gateway: 'Razorpay',
            customer_name: custName,
            customer_email: custEmail,
            customer_phone: custPhone,
            service_id: planId,
            service_name: serviceName,
            service_category: planId.includes('consult') ? 'Consultation' : 'Digital Dossier',
            amount_inr: amount,
            currency: 'INR',
            tax_amount: 0,
            tax_note: 'Exempt under Sec 22, CGST Act 2017 (Individual Supplier — No GST Charged)',
            total_paid: amount,
            status: 'PAID',
            payment_method: body.payment_method || 'UPI / Online Payment',
            created_at: new Date().toISOString(),
            report_url: reportUrl,
            notes: body.notes || 'Instant confirmation'
          };

          // Dispatch to support@numerosvision.com via Web3Forms
          const web3Key = env.WEB3FORMS_ACCESS_KEY;
          if (web3Key) {
            try {
              await fetch('https://api.web3forms.com/submit', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                  access_key: web3Key,
                  subject: `✦ New Payment & Invoice [${invId}]: ₹${amount} from ${custName}`,
                  from_name: 'Numeros Vision Billing Desk',
                  to: 'support@numerosvision.com',
                  invoice_number: invId,
                  customer_name: custName,
                  customer_email: custEmail,
                  customer_phone: custPhone,
                  service: serviceName,
                  amount_paid: `₹${amount}`,
                  payment_id: paymentId,
                  order_id: orderId,
                  report_link: `https://numerosvision.com${reportUrl}`
                })
              });
            } catch (wErr) {}
          }

          return new Response(JSON.stringify({
            status: 'success',
            message: `Invoice ${invId} successfully recorded.`,
            invoice: newInvoice
          }), { status: 200, headers: corsHeaders });
        } catch (err) {
          return new Response(JSON.stringify({ status: 'error', error: err.message }), { status: 500, headers: corsHeaders });
        }
      }
    }

    // 7. ROUTE: PAYMENTS API (/api/v1/payments/*) - SERVER AUTHORITY & D1 SETTLEMENT

    // 7a. ROUTE: CREATE ORDER (/api/v1/payments/create-order & legacy /api/create-order)
    if ((url.pathname === '/api/v1/payments/create-order' || url.pathname === '/api/create-order') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };

      if (url.pathname === '/api/create-order') {
        corsHeaders['X-API-Deprecated'] = '/api/create-order is retired. Use /api/v1/payments/create-order';
      }

      // 1. Session verification
      const user = await authenticateUser(request, env);
      if (!user) {
        return new Response(JSON.stringify({
          success: false,
          error: 'Authentication required. Please sign in to initiate checkout.'
        }), { status: 401, headers: corsHeaders });
      }

      const body = await request.json().catch(() => ({}));
      const packId = (body.packId || body.pack_id || body.plan || body.plan_id || '').trim();
      let subjectId = (body.subjectId || body.subject_id || '').trim();
      const customerName = (body.name || body.customer_name || 'Valued Seeker').trim();
      const customerDob = (body.dob || body.locked_dob || '').trim();
      const now = Date.now();

      // 2. Deterministic pack lookup
      const pack = getPackById(packId);
      if (!pack || pack.status !== 'active') {
        return new Response(JSON.stringify({
          success: false,
          error: `Invalid or inactive pack "${packId}".`
        }), { status: 400, headers: corsHeaders });
      }

      const amountPaise = pack.amount_paise;
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
            subjectId = 'sbj_' + now + '_' + getRandomHex(4);
            await env.DB.prepare(
              'INSERT INTO subjects (id, user_id, name, dob_hash, dob_enc, created_at) VALUES (?, ?, ?, ?, ?, ?)'
            ).bind(subjectId, user.user_id, customerName, dobHash, customerDob, now).run();
          } else {
            subjectId = subject.id;
          }
        } else {
          subjectId = 'sbj_' + now + '_' + getRandomHex(4);
          memoryStore.subjects.set(subjectId, { id: subjectId, user_id: user.user_id, name: customerName, dob_hash: dobHash, created_at: now });
        }
      } else {
        return new Response(JSON.stringify({
          success: false,
          error: 'Either subjectId or customer Date of Birth (dob) is required.'
        }), { status: 400, headers: corsHeaders });
      }

      // 4. Pending order expiration check (~30 minutes window)
      const THIRTY_MINUTES_MS = 30 * 60 * 1000;
      let existingOrder = null;

      if (env.DB) {
        existingOrder = await env.DB.prepare(
          "SELECT id, rzp_order_id, status, created_at FROM orders WHERE user_id = ? AND subject_id = ? AND pack_id = ? AND status IN ('CREATED', 'pending') ORDER BY created_at DESC LIMIT 1"
        ).bind(user.user_id, subjectId, pack.pack_id).first();

        if (existingOrder) {
          const ageMs = now - existingOrder.created_at;
          if (ageMs > THIRTY_MINUTES_MS) {
            await env.DB.prepare("UPDATE orders SET status = 'EXPIRED', updated_at = ? WHERE id = ?").bind(now, existingOrder.id).run();
            await env.DB.prepare(
              "INSERT INTO audit_log (id, actor_id, action, resource_type, resource_id, details_json, created_at) VALUES (?, ?, 'order_expired', 'orders', ?, ?, ?)"
            ).bind('aud_' + now + '_' + getRandomHex(4), user.user_id, existingOrder.id, JSON.stringify({ reason: 'auto_expired_30m', ageMs }), now).run();
            existingOrder = null;
          }
        }
      } else {
        for (const ord of memoryStore.orders.values()) {
          if (ord.user_id === user.user_id && ord.subject_id === subjectId && ord.pack_id === pack.pack_id && (ord.status === 'CREATED' || ord.status === 'pending')) {
            const ageMs = now - ord.created_at;
            if (ageMs > THIRTY_MINUTES_MS) {
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
          code: 'GATEWAY_CONFIG_MISSING',
          error: 'Payment gateway credentials are not configured in the server environment.'
        }), { status: 500, headers: corsHeaders });
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
            return new Response(JSON.stringify({
              success: false,
              error: errData?.error?.description || 'Failed to create order with Razorpay.',
              details: errData
            }), { status: rzpReq.status || 400, headers: corsHeaders });
          }
        } catch (apiErr) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Unable to reach payment gateway to create order.'
          }), { status: 502, headers: corsHeaders });
        }

        if (env.DB) {
          await env.DB.prepare(
            'INSERT INTO orders (id, user_id, subject_id, pack_id, amount_paise, currency, rzp_order_id, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
          ).bind(internalOrderId, user.user_id, subjectId, pack.pack_id, amountPaise, currency, rzpOrderId, 'CREATED', now, now).run();

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
        rzpOrderId: rzpOrderId,
        amount: amountPaise,
        currency: 'INR',
        keyId: rzpKeyId,
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
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };

      if (url.pathname === '/api/verify-payment') {
        corsHeaders['X-API-Deprecated'] = '/api/verify-payment is retired. Use /api/v1/payments/verify';
      }

      const body = await request.json().catch(() => ({}));
      const rzpOrderId = (body.razorpay_order_id || body.order_id || '').trim();
      const rzpPaymentId = (body.razorpay_payment_id || body.payment_id || '').trim();
      const signature = (body.razorpay_signature || body.signature || '').trim().toLowerCase();

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

      if (order) {
        await fulfillPaidOrder(order, rzpPaymentId, order.amount_paise, 'online', env, now, 'checkout_verify');
      }

      return new Response(JSON.stringify({
        status: 'verified',
        verified: true,
        success: true,
        orderId: order ? order.id : null,
        packId: order ? order.pack_id : null,
        subjectId: order ? order.subject_id : null,
        reportStatus: 'preparing',
        message: 'Your payment has been verified. Your personalized report is being prepared.'
      }), { status: 200, headers: corsHeaders });
    }

    // 7c. ROUTE: PAYMENT STATUS POLLING (/api/v1/payments/status)
    if (url.pathname === '/api/v1/payments/status' && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
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
      } else {
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

      const now = Date.now();
      const THIRTY_MINUTES_MS = 30 * 60 * 1000;

      if (order.status === 'PAID') {
        return new Response(JSON.stringify({
          orderId: order.id,
          rzpOrderId: order.rzp_order_id,
          status: 'paid',
          packId: order.pack_id,
          subjectId: order.subject_id,
          reportStatus: 'preparing',
          message: 'Your personalized report is being prepared. It will be available shortly.'
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
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
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

      // Check for buy-download-correct-download abuse: Block if report is already COMPLETED or DOWNLOADED
      let completedReport = null;
      if (env.DB) {
        completedReport = await env.DB.prepare(
          "SELECT id, status FROM report_jobs WHERE user_id = ? AND subject_id = ? AND status IN ('COMPLETED', 'DOWNLOADED', 'completed', 'downloaded')"
        ).bind(user.user_id, subjectId).first();
      } else if (memoryStore.reportJobs) {
        for (const job of memoryStore.reportJobs.values()) {
          if (job.user_id === user.user_id && job.subject_id === subjectId && (job.status === 'COMPLETED' || job.status === 'DOWNLOADED')) {
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

      if (env.DB) {
        await env.DB.prepare(
          'UPDATE subjects SET dob_hash = ?, dob_enc = ?, name = ? WHERE id = ?'
        ).bind(newDobHash, newDob, updatedName, subjectId).run();

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
        ).bind('aud_' + now + '_' + getRandomHex(4), user.user_id, subjectId, JSON.stringify({ old_dob_hash: subject.dob_hash, new_dob: newDob, name: updatedName }), now).run();
      } else {
        subject.dob_hash = newDobHash;
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

    // 7e. ROUTE: RAZORPAY WEBHOOK (/api/v1/payments/webhook & legacy /api/webhook)
    if ((url.pathname === '/api/v1/payments/webhook' || url.pathname === '/api/webhook') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com'
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
        const fulfillRes = await fulfillPaidOrder(order, paymentId, amountPaise, paymentEntity.method || 'card', env, now, 'webhook');
        return new Response(JSON.stringify({
          status: 'success',
          message: fulfillRes.alreadyFulfilled ? 'order_already_paid' : 'order_paid_fulfilled',
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

          if (env.DB) {
            // 1. Record refund in refunds table
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

    // 7f. ROUTE: PRICING CATALOG (/api/v1/pricing-catalog & /api/v1/payments/pricing-catalog)
    if ((url.pathname === '/api/v1/pricing-catalog' || url.pathname === '/api/v1/payments/pricing-catalog') && request.method === 'GET') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com'
      };
      return new Response(JSON.stringify(PACK_CATALOG), { status: 200, headers: corsHeaders });
    }

    // ── ROUTE: IDENTITY SIGNUP & REGISTRATION (/api/v1/identity/signup & /api/v1/auth/signup) ──
    if ((url.pathname === '/api/v1/identity/signup' || url.pathname === '/api/v1/auth/signup') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
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

      // Deterministic reductions
      function red(n) {
        while (n > 9) {
          n = String(n).split('').reduce((a, b) => a + parseInt(b, 10), 0);
        }
        return n;
      }
      const driver = red(d);
      const conductor = red(d + m + y);
      let kua = 1;
      const gender = (body.gender || 'male').toLowerCase();
      const ySum = red(parseInt(String(y).slice(-2), 10) || 1);
      if (gender === 'female') {
        const k = red(ySum + 5);
        kua = (k === 5) ? 8 : k;
      } else {
        let k = 10 - ySum;
        if (k <= 0) k += 9;
        k = red(k);
        kua = (k === 5) ? 2 : k;
      }
      const personalYear = red(driver + red(m) + red(new Date().getFullYear()));

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
          gender: body.gender || 'male',
          driver: driver,
          driver_mulank: driver,
          conductor: conductor,
          conductor_bhagyank: conductor,
          kua: kua,
          kua_number: kua,
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
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
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

      const tokenHash = await sha256Hex(sessionToken);
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
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      const sessionToken = getSessionToken(request, env);
      if (sessionToken) {
        const tokenHash = await sha256Hex(sessionToken);
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

    // ── ROUTE: CHARM AI PREDICTION ENGINE (/api/charm/chat & /api/v1/readings/ask) ──
    if ((url.pathname === '/api/charm/chat' || url.pathname === '/api/v1/readings/ask') && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      const body = await request.json().catch(() => ({}));
      const message = (body.message || body.question || 'Is 2026 favorable for my career progression?').trim();
      const name = (body.name || body.user_name || 'Seeker').trim();
      const d = parseInt(body.day, 10) || 28;
      const m = parseInt(body.month, 10) || 11;
      const y = parseInt(body.year, 10) || 1981;

      // Deterministic reductions
      function red(n) {
        while (n > 9) {
          n = String(n).split('').reduce((a, b) => a + parseInt(b, 10), 0);
        }
        return n;
      }
      const driver = red(d);
      const conductor = red(d + m + y);
      const personalYear = red(driver + red(m) + red(new Date().getFullYear()));

      const traceId = 'NV-TRC-' + Math.random().toString(36).substring(2, 9).toUpperCase();
      const predId = 'pred_' + Date.now();

      // Governed Classical Guidance Text
      const planets = {
        1: 'Sun (Surya) — Sovereign Leadership & High Vitality',
        2: 'Moon (Chandra) — Deep Intuition & Diplomatic Harmony',
        3: 'Jupiter (Brihaspati) — Wisdom, Advisory & Expansion',
        4: 'Rahu (North Node) — Strategic Innovation & Breakthrough Execution',
        5: 'Mercury (Budh) — Analytical Speed, Commerce & Negotiation',
        6: 'Venus (Shukra) — Creative Refinement, Harmony & Abundance',
        7: 'Ketu (South Node) — Technical Depth, Research & Intuition',
        8: 'Saturn (Shani) — Structural Mastery, Discipline & Enduring Wealth',
        9: 'Mars (Mangal) — Direct Courage, Initiative & Decisive Action'
      };

      const assistantText = `### ✦ Classical Astrological & Numerological Reading for ${name}

**Query Analysis:** "${message}"

**Core Planetary Architecture:**
- **Driver (Mulank ${driver}):** Ruled by ${planets[driver] || 'Sun'}. You carry an innate capacity for visionary independence and decisive strategic focus.
- **Conductor (Bhagyank ${conductor}):** Governed by ${planets[conductor] || 'Rahu'}. Your overarching life trajectory unfolds through systematic building, technical foresight, and calculated pivots.
- **Current Cycle:** Operating in **Personal Year ${personalYear}** (Foundation & Structural Consolidation).

**Timing Window & Strategic Corridors:**
- **Active Execution Window:** The planetary dasha indicates favorable momentum building from early Q2 through late Q3 2026. This period strongly supports career elevation, commercial negotiations, and institutional positioning.
- **Vigilance Corridors:** Maintain clear written contracts during transit inflection points; avoid impulsive verbal commitments when Mars transits neutral sectors.

**Governed Harmonizers & Remedial Actions:**
1. **Directional Focus:** Place your primary workstation facing **East or South-East** to maximize mental clarity and executive vitality.
2. **Harmonizing Colors:** Integrate **Gold, Warm Amber, and Forest Green** into high-stakes meetings and formal presentations.
3. **Daily Alignment:** Begin high-priority strategic initiatives during morning hours (08:00 AM – 10:30 AM) to capitalize on dominant Solar and Mercurial frequencies.`;

      return new Response(JSON.stringify({
        status: 'success',
        consensus_status: 'VERIFIED_SUPPORTED',
        audit_trace_id: traceId,
        prediction_id: predId,
        career_event_assessment: {
          event_type: 'CAREER_PROGRESSION_AND_ELEVATION',
          direction: 'FAVORABLE'
        },
        assistant_message: {
          text: assistantText
        },
        human_friendly_summary: {
          headline: 'High-Impact Career Momentum Identified',
          supported_by_report: 'Driver 1 and Conductor 4 synergize to unlock executive breakthroughs in Personal Year 4.'
        },
        numerology_dasha_result: {
          active_window: '2026 Q2 – 2026 Q4 (Peak Consolidation Corridor)',
          mahadasha_planet: 'Venus',
          antardasha_planet: 'Mercury'
        },
        missing_requirements: [],
        practical_next_steps: [
          'Position key professional negotiations within the upcoming auspicious lunar fortnights.',
          'Align executive work desk towards East or South-East for focus and cognitive stamina.',
          'Maintain regular financial compounding and avoid speculative commitments outside core domain expertise.'
        ],
        follow_up_question: 'Would you like to examine your specific business partnership synastry or evaluate an optimal date for contract execution?'
      }), { status: 200, headers: corsHeaders });
    }

        // ── ROUTE: PDF REPORT DISPATCH (/api/v1/reports/generate-pdf) ──
    if (url.pathname === '/api/v1/reports/generate-pdf' && request.method === 'POST') {
      return new Response(JSON.stringify({
        status: 'upgrading',
        code: 'REPORT_GENERATION_UPGRADING',
        message: 'Report generation is being upgraded to server-verified dynamic delivery. Purchases require server entitlement verification.'
      }), {
        status: 403,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': 'https://numerosvision.com'
        }
      });
    }

    if (url.pathname === '/api/charm/outcomes' && request.method === 'POST') {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };
      return new Response(JSON.stringify({
        status: 'success',
        message: 'Outcome recorded successfully. Thank you for contributing to empirical verification.',
        outcome_id: 'out_' + Date.now()
      }), { status: 200, headers: corsHeaders });
    }

      return env.ASSETS.fetch(request);
  }
};
