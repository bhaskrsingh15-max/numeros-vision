"""
Patches app/static/_worker.js for Commit 3 (Real Authentication).
- Adds cryptographic helpers (sha256Hex, hmacSha256Hex, getRandomHex, verifyOrigin, getCookie)
- Implements HMAC-hashed OTP with 5-minute expiry and 5 attempts limit
- Implements rate limiting per number (60s / 5/hr) and per IP (10/hr)
- Enforces constant-time comparison (timingSafeEqual)
- Sets HttpOnly, Secure, SameSite=Lax session cookie (nv_session) backed by D1 sessions table
- Implements /api/me and /api/logout
- Implements Origin check for state-changing POST requests
- Verifies Google ID tokens server-side via Google tokeninfo endpoint
- Gating dev_otp strictly to ENVIRONMENT === 'local'
"""

import re
import os

worker_path = os.path.join('app', 'static', '_worker.js')
with open(worker_path, 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace('\r\n', '\n')

# 1. Update cryptographic helpers at top
crypto_helpers = '''// Constant-time string comparison to prevent side-channel timing attacks
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
  creditLedger: new Map()
};'''

old_top_re = re.compile(r'// Constant-time string comparison.*?return mismatch === 0;\s*}', re.DOTALL)
assert old_top_re.search(code), 'Old timingSafeEqual block not found'
code = old_top_re.sub(lambda m: crypto_helpers, code, count=1)

# 2. Add Origin Check right inside fetch(request, env)
origin_check_snippet = '''    const url = new URL(request.url);

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
    }'''

code = code.replace('const url = new URL(request.url);', origin_check_snippet, 1)

# 3. Replace Routes 1, 2, 3 (OTP Send, OTP Verify, Google Auth)
old_routes_123_re = re.compile(r'// 1\. ROUTE: SEND OTP \(.*?// 4\. ROUTE: 1-ON-1 CONSULTATION ENQUIRY', re.DOTALL)

new_routes_123 = '''// 1. ROUTE: SEND OTP (/api/v1/auth/otp/send)
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
        const cleanDigits = rawPhone.replace(/\\D/g, '');
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
          if (prev && (now - prev.createdAt) < 60000) {
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
            phoneHash,
            codeHash,
            attempts: 0,
            maxAttempts: 5,
            expiresAt,
            createdAt: now,
            ipHash
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
        const cleanDigits = rawPhone.replace(/\\D/g, '');
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
          if (challenge && challenge.expiresAt <= now) challenge = null;
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
            userId,
            tokenHash,
            expiresAt: sessionExpiresAt,
            createdAt: now
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
            'Set-Cookie': `nv_session=${rawToken}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000`
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
        const body = await request.json().catch(() => ({}));
        const credential = body.credential || body.id_token;

        if (!credential) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Google ID token credential is required.'
          }), { status: 400, headers: corsHeaders });
        }

        // Server-side verification via Google TokenInfo API
        let tokenInfo = null;
        try {
          const gResp = await fetch(`https://oauth2.googleapis.com/tokeninfo?id_token=${encodeURIComponent(credential)}`);
          if (gResp.ok) {
            tokenInfo = await gResp.json();
          }
        } catch (gErr) {
          console.error('[Google_TokenInfo_Error]', gErr);
        }

        if (!tokenInfo || !tokenInfo.email) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Invalid or expired Google ID token.'
          }), { status: 401, headers: corsHeaders });
        }

        const validIssuers = ['accounts.google.com', 'https://accounts.google.com'];
        if (!validIssuers.includes(tokenInfo.iss)) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Google ID token issuer invalid.'
          }), { status: 401, headers: corsHeaders });
        }

        if (env.GOOGLE_CLIENT_ID && tokenInfo.aud !== env.GOOGLE_CLIENT_ID) {
          return new Response(JSON.stringify({
            success: false,
            error: 'Google ID token audience mismatch.'
          }), { status: 401, headers: corsHeaders });
        }

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
          memoryStore.sessions.set(tokenHash, { userId, tokenHash, expiresAt: sessionExpiresAt, createdAt: now });
        }

        return new Response(JSON.stringify({
          success: true,
          authenticated: true,
          user: {
            id: userId,
            email: verifiedEmail,
            name: verifiedName
          },
          redirect_url: '/dashboard/'
        }), {
          status: 200,
          headers: {
            ...corsHeaders,
            'Set-Cookie': `nv_session=${rawToken}; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=2592000`
          }
        });
      } catch (err) {
        return new Response(JSON.stringify({ success: false, error: err.message }), {
          status: 500,
          headers: corsHeaders
        });
      }
    }

    // 4. ROUTE: 1-ON-1 CONSULTATION ENQUIRY'''

assert old_routes_123_re.search(code), 'Routes 1-3 regex match failed'
code = old_routes_123_re.sub(lambda m: new_routes_123, code, count=1)

# 4. Replace /api/v1/auth/me and /api/v1/auth/login with real session checks and logout
# Look for start of AUTH ME and end of AUTH LOGIN
auth_me_start = code.find('ROUTE: AUTH ME SESSION CHECK')
assert auth_me_start != -1, 'AUTH ME block start not found'
# Find the end of AUTH LOGIN block right before CHARM AI PREDICTION ENGINE
charm_start = code.find('ROUTE: CHARM AI PREDICTION ENGINE', auth_me_start)
assert charm_start != -1, 'CHARM AI block start not found'

# Back up to the comment line before AUTH ME
block_start = code.rfind('//', 0, auth_me_start)
block_end = code.rfind('//', auth_me_start, charm_start)

new_me_logout = '''// 7. ROUTE: SESSION CHECK (/api/me & /api/v1/auth/me)
    if ((url.pathname === '/api/me' || url.pathname === '/api/v1/auth/me') && (request.method === 'GET' || request.method === 'POST')) {
      const corsHeaders = {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': 'https://numerosvision.com',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization'
      };

      const sessionToken = getCookie(request, 'nv_session');
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
        if (sess && sess.expiresAt > now) {
          sessionUser = { user_id: sess.userId, expires_at: sess.expiresAt };
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
            'Set-Cookie': 'nv_session=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0'
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
      const sessionToken = getCookie(request, 'nv_session');
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
          'Set-Cookie': 'nv_session=; Path=/; HttpOnly; Secure; SameSite=Lax; Max-Age=0'
        }
      });
    }

    '''

code = code[:block_start] + new_me_logout + code[block_end:]

with open(worker_path, 'w', encoding='utf-8', newline='\r\n') as f:
    f.write(code)

print('Successfully applied Commit 3 Authentication patch to _worker.js')
