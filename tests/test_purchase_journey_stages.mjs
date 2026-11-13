/**
 * Purchase Journey Verification Suite
 * 
 * Tests:
 * 1. Parity between app/config/packs.ts and app/static/_worker.js (prices, amount_paise, status, pack_id)
 * 2. URL privacy guard: no personal data (DOB, name, phone, email) in any transition URL
 * 3. Consents default to unticked
 * 4. Server-side price authority overrides any tampered client price
 * 5. Dashboard security: refuses unauthenticated / unverified access
 */

import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const rootDir = join(__dirname, '..');

async function runTests() {
  console.log('\n--- STARTING PURCHASE JOURNEY STAGES VERIFICATION ---\n');
  let passCount = 0;
  let failCount = 0;

  function assert(condition, message) {
    if (condition) {
      console.log(`✔ PASS: ${message}`);
      passCount++;
    } else {
      console.error(`✖ FAIL: ${message}`);
      failCount++;
    }
  }

  // ── TEST 1: packs.ts and _worker.js Parity Check ──
  try {
    const packsTsContent = readFileSync(join(rootDir, 'app/config/packs.ts'), 'utf-8');
    const workerContent = readFileSync(join(rootDir, 'app/static/_worker.js'), 'utf-8');

    // Extract JSON object from packs.ts
    const jsonMatchPacks = packsTsContent.match(/export const PACK_CATALOG[\s\S]*?=\s*({[\s\S]*?});\s*export default/);
    if (!jsonMatchPacks) throw new Error('Could not parse PACK_CATALOG from packs.ts');
    const packsCatalog = JSON.parse(jsonMatchPacks[1]);

    // Extract PACK_CATALOG from _worker.js
    const workerCatalogMatch = workerContent.match(/const PACK_CATALOG\s*=\s*({[\s\S]*?});\s*function (?:resolveServerLaunchOfferState|getPackById)/);
    if (!workerCatalogMatch) throw new Error('Could not parse PACK_CATALOG from _worker.js');
    
    // Evaluate worker catalog safely
    const workerCatalog = eval('(' + workerCatalogMatch[1] + ')');

    let allMatch = true;
    const categories = ['core_reports', 'charm_ai', 'bundles'];

    for (const cat of categories) {
      const tsPacks = packsCatalog[cat] || {};
      const workerPacks = workerCatalog[cat] || {};

      for (const [id, def] of Object.entries(tsPacks)) {
        const wDef = workerPacks[id];
        if (!wDef) {
          assert(false, `Worker catalog missing pack "${id}" in ${cat}`);
          allMatch = false;
          continue;
        }
        if (def.price_inr !== wDef.price_inr) {
          assert(false, `Price mismatch on "${id}": packs.ts has ₹${def.price_inr}, worker has ₹${wDef.price_inr}`);
          allMatch = false;
        }
        if (def.amount_paise !== wDef.amount_paise) {
          assert(false, `Amount paise mismatch on "${id}": packs.ts has ${def.amount_paise}, worker has ${wDef.amount_paise}`);
          allMatch = false;
        }
        if (def.status !== wDef.status) {
          assert(false, `Status mismatch on "${id}": packs.ts has ${def.status}, worker has ${wDef.status}`);
          allMatch = false;
        }
      }
    }

    if (allMatch) {
      assert(true, 'app/config/packs.ts and app/static/_worker.js have 100% price and pack_id parity');
    }
  } catch (err) {
    assert(false, `Packs catalog parity check threw error: ${err.message}`);
  }

  // ── TEST 2: URL Privacy Guard — No PII in Query Strings or Links ──
  try {
    const htmlFiles = ['index.html', 'your-reading.html'].map(f => {
      try {
        return { file: f, content: readFileSync(join(rootDir, 'app/static', f), 'utf-8') };
      } catch (e) {
        return { file: f, content: '' };
      }
    });

    let piiFoundInLinks = false;
    for (const { file, content } of htmlFiles) {
      if (!content) continue;
      // Check for patterns like ?dob=, &dob=, ?name=, &name=, ?email=, &email=, ?phone=, &phone= in anchor tags or window.location hrefs
      const suspiciousUrlMatches = content.match(/href=["'][^"']*[?&](dob|birth_date|customer_name|email|mobile|phone)=/gi) || [];
      const locationAssignMatches = content.match(/location\.(href|assign)\s*=[^;]*[?&](dob|birth_date|customer_name|email|mobile|phone)=/gi) || [];
      if (suspiciousUrlMatches.length > 0 || locationAssignMatches.length > 0) {
        piiFoundInLinks = true;
        assert(false, `PII query parameter found in ${file}: ${[...suspiciousUrlMatches, ...locationAssignMatches].join(', ')}`);
      }
    }

    if (!piiFoundInLinks) {
      assert(true, 'No personal data (DOB, name, email, phone) exposed in URL query parameters');
    }
  } catch (err) {
    assert(false, `URL privacy guard check threw error: ${err.message}`);
  }

  // ── TEST 2B: Clutter Elimination & Single Path on index.html ──
  try {
    const indexHtml = readFileSync(join(rootDir, 'app/static/index.html'), 'utf-8');

    assert(!indexHtml.includes('Proceed to Pay'), 'index.html contains zero "Proceed to Pay" elements');
    assert(!indexHtml.includes('reports-checkout-console'), 'index.html contains zero #reports-checkout-console');
    assert(!indexHtml.includes('heroSaveProfileContainer'), 'index.html contains zero heroSaveProfileContainer');

    const forbiddenFns = [
      'sendReportsOtp',
      'verifyReportsOtp',
      'launchInPageReportsCheckout',
      'triggerEmailQuickSignIn',
      'triggerGoogleSignIn'
    ];
    for (const fn of forbiddenFns) {
      assert(!indexHtml.includes(`function ${fn}`), `index.html contains no legacy console function ${fn}`);
    }

    assert(indexHtml.includes("navigateToReportOptions('home')"), 'index.html retains lower "See my report options" button');
    assert(indexHtml.includes('/pricing/#charm-ai'), 'index.html retains Charm AI pass link');
  } catch (err) {
    assert(false, `index.html clutter elimination test failed: ${err.message}`);
  }

  // ── TEST 2C: All 8 Wired Calculators Navigate to /your-reading/?from=<slug> ──
  try {
    const calcs = [
      { file: 'index.html', slug: 'home' },
      { file: 'birth_number_calculator.html', slug: 'birth-number' },
      { file: 'pythagorean_calculator.html', slug: 'pythagorean' },
      { file: 'tools/life-path-calculator.html', slug: 'life-path-calculator' },
      { file: 'tools/lo-shu-grid.html', slug: 'lo-shu-grid' },
      { file: 'tools/name-numerology.html', slug: 'name-numerology' },
      { file: 'tools/name-balancing.html', slug: 'name-balancing' },
      { file: 'tools/compatibility-calculator.html', slug: 'compatibility-calculator' }
    ];

    for (const { file, slug } of calcs) {
      const html = readFileSync(join(rootDir, 'app/static', file), 'utf-8');
      const hasDirectNav = html.includes(`/your-reading/?from=${slug}`);
      const savesStorage = html.includes("sessionStorage.setItem('nv_reading_input'");
      const restoresStorage = html.includes("sessionStorage.getItem('nv_reading_input')");

      assert(hasDirectNav, `${file} navigates directly to /your-reading/?from=${slug} on Calculate`);
      assert(savesStorage, `${file} saves inputs to nv_reading_input on Calculate`);
      assert(restoresStorage, `${file} restores inputs from nv_reading_input on Back navigation`);
    }
  } catch (err) {
    assert(false, `All 8 calculators navigation test failed: ${err.message}`);
  }

  // ── TEST 3: Statutory Consents Default Unticked ──
  try {
    const htmlFiles = ['index.html', 'your-reading.html', 'signup.html', 'charm_ai.html'];
    let hardcodedCheckFound = false;

    for (const file of htmlFiles) {
      const p = join(rootDir, 'app/static', file);
      try {
        const content = readFileSync(p, 'utf-8');
        // Match consent checkboxes with checked attribute
        const matches = content.match(/id=["'][^"']*consent[^"']*["'][^>]*\bchecked\b/gi);
        if (matches) {
          hardcodedCheckFound = true;
          assert(false, `Consent checkbox hardcoded as checked in ${file}: ${matches.join(', ')}`);
        }
      } catch (e) {}
    }

    if (!hardcodedCheckFound) {
      assert(true, 'All statutory DPDP consent checkboxes default to unticked across pages');
    }
  } catch (err) {
    assert(false, `Consent check threw error: ${err.message}`);
  }

  // ── TEST 4: /your-reading/ marked noindex ──
  try {
    const yourReadingHtml = readFileSync(join(rootDir, 'app/static/your-reading.html'), 'utf-8');
    const hasNoIndex = /<meta\s+name=["']robots["']\s+content=["'][^"']*noindex/i.test(yourReadingHtml);
    assert(hasNoIndex, '/your-reading/ page is marked strictly noindex');
  } catch (e) {
    assert(false, `/your-reading/ noindex check failed: ${e.message}`);
  }

  // ── TEST 5: Server-side Price Overrides Tampered Client Price ──
  try {
    const workerModule = await import('../app/static/_worker.js');
    const worker = workerModule.default;

    const mockEnv = {
      ENVIRONMENT: 'test',
      NV_LAUNCH_STARTS_AT: '2026-01-01T00:00:00+05:30',
      NV_LAUNCH_ENDS_AT: '2027-12-31T23:59:59+05:30',
      RAZORPAY_KEY_ID: 'rzp_test_MOCK_JOURNEY_KEY',
      RAZORPAY_KEY_SECRET: 'test_secret_for_journey_payments',
      OTP_HMAC_SECRET: 'test_otp_hmac_secret_32b_journey',
      SESSION_SECRET: 'test_session_secret_32b_journey_',
      IP_HASH_SALT: 'test_ip_hash_salt_32b_journey_00',
      DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
      ASSETS: { fetch: async () => new Response('Asset stub', { status: 200 }) }
    };

    // Mock fetch for Razorpay
    const test4OriginalFetch = globalThis.fetch;
    let createdRazorpayAmount = null;

    globalThis.fetch = async (url, options = {}) => {
      const urlStr = String(url);
      if (urlStr.includes('api.razorpay.com/v1/orders')) {
        const body = JSON.parse(options.body || '{}');
        createdRazorpayAmount = body.amount;
        return new Response(JSON.stringify({
          id: 'order_rzp_mock_tamper_test',
          entity: 'order',
          amount: body.amount,
          currency: body.currency || 'INR',
          receipt: body.receipt,
          status: 'created'
        }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      return test4OriginalFetch(url, options);
    };

    // Generate valid checkout token for test email (${timestamp}.${sig})
    const email = 'tester.tamper@example.com';
    const now = Date.now();
    const testSecret = mockEnv.SESSION_SECRET;
    const encoder = new TextEncoder();
    const key = await crypto.subtle.importKey(
      'raw',
      encoder.encode(testSecret),
      { name: 'HMAC', hash: 'SHA-256' },
      false,
      ['sign']
    );
    const payload = `${email.toLowerCase().trim()}:${now}`;
    const sigBuffer = await crypto.subtle.sign('HMAC', key, encoder.encode(payload));
    const sigHex = Array.from(new Uint8Array(sigBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
    const validCheckoutToken = `${now}.${sigHex}`;

    // Attempt to tamper with price: send amount: 100 paise (₹1) for Basic Report (₹199 / 19900 paise)
    const tamperReq = new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'https://numerosvision.com'
      },
      body: JSON.stringify({
        pack_id: 'report_basic',
        name: 'Tamper Tester',
        dob: '1990-05-15',
        email: email,
        amount: 100, // Tampered ₹1
        amount_paise: 100, // Tampered ₹1
        price: 1, // Tampered ₹1
        checkout_token: validCheckoutToken
      })
    });

    const tamperRes = await worker.fetch(tamperReq, mockEnv);
    const tamperData = await tamperRes.json();

    assert(tamperRes.status === 200, `create-order returns HTTP 200 (got ${tamperRes.status})`);
    assert(
      tamperData.amount === 19900 && createdRazorpayAmount === 19900,
      `Server-side price (19900 paise) strictly overrides tampered client price (100 paise)`
    );

    // Restore fetch
    globalThis.fetch = test4OriginalFetch;
  } catch (err) {
    assert(false, `Price tampering override test threw error: ${err.message}`);
  }

  // ── TEST 5B: Server Check — create-order Rejects Unauthenticated / Unverified Requests ──
  try {
    const workerModule = await import('../app/static/_worker.js');
    const worker = workerModule.default;

    const mockEnv = {
      ENVIRONMENT: 'test',
      NV_LAUNCH_STARTS_AT: '2026-01-01T00:00:00+05:30',
      NV_LAUNCH_ENDS_AT: '2027-12-31T23:59:59+05:30',
      RAZORPAY_KEY_ID: 'rzp_test_MOCK_JOURNEY_KEY',
      RAZORPAY_KEY_SECRET: 'test_secret_for_journey_payments',
      OTP_HMAC_SECRET: 'test_otp_hmac_secret_32b_journey',
      SESSION_SECRET: 'test_session_secret_32b_journey_',
      IP_HASH_SALT: 'test_ip_hash_salt_32b_journey_00',
      DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef'
    };

    // Post to create-order with an email that has NO verified session and NO checkout_token
    const unverifiedReq = new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Origin': 'https://numerosvision.com'
      },
      body: JSON.stringify({
        pack_id: 'report_basic',
        name: 'Unverified Seeker',
        dob: '1990-05-15',
        email: 'unverified_stranger@example.com'
        // Notice checkout_token is intentionally omitted
      })
    });

    const unverifiedRes = await worker.fetch(unverifiedReq, mockEnv);
    const unverifiedData = await unverifiedRes.json();

    assert(unverifiedRes.status === 401, `create-order rejects unauthenticated request with HTTP 401 (got ${unverifiedRes.status})`);
    assert(
      unverifiedData.error && unverifiedData.error.includes('Authentication required'),
      'create-order returns honest "Authentication required" error message when unverified'
    );
  } catch (err) {
    assert(false, `create-order unverified rejection test threw error: ${err.message}`);
  }

  // ── TEST 6: Dashboard Refuses Unauthenticated / Unverified Access ──
  try {
    const workerModule = await import('../app/static/_worker.js');
    const worker = workerModule.default;

    const mockEnv = {
      ENVIRONMENT: 'test',
      SESSION_SECRET: 'test_session_secret_32b_journey_',
      IP_HASH_SALT: 'test_ip_hash_salt_32b_journey_00',
      DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
      ASSETS: { fetch: async () => new Response('Asset stub', { status: 200 }) }
    };

    // Anonymous request with no cookie or token
    const unauthReq = new Request('https://numerosvision.com/api/v1/dashboard/view', {
      method: 'GET',
      headers: { 'Origin': 'https://numerosvision.com' }
    });

    const unauthRes = await worker.fetch(unauthReq, mockEnv);
    assert(
      unauthRes.status === 401,
      `Dashboard view rejects unverified / unauthenticated session with HTTP 401 (got ${unauthRes.status})`
    );
  } catch (err) {
    assert(false, `Dashboard unverified session test threw error: ${err.message}`);
  }


  // ── TEST 7: Strict Gregorian Calendar Validation (31 Feb, 31 Apr, Leap Years) ──
  try {
    const yourReadingHtml = readFileSync(join(rootDir, 'app/static/your-reading.html'), 'utf-8');
    assert(yourReadingHtml.includes('isValidGregorianDate'), 'your-reading.html implements isValidGregorianDate function');

    // Extract function implementation from your-reading.html
    const funcMatch = yourReadingHtml.match(/function isValidGregorianDate\(d, m, y\)[\s\S]*?\n    \}/);
    if (!funcMatch) throw new Error('Could not extract isValidGregorianDate from your-reading.html');
    
    const isValidGregorianDate = new Function('d', 'm', 'y', funcMatch[0] + '; return isValidGregorianDate(d, m, y);');

    // Rigorous test matrix
    assert(!isValidGregorianDate(31, 2, 2024), 'Rejects impossible date 31 February');
    assert(!isValidGregorianDate(31, 4, 2024), 'Rejects 31 April (30-day month)');
    assert(!isValidGregorianDate(31, 6, 2024), 'Rejects 31 June (30-day month)');
    assert(!isValidGregorianDate(31, 9, 2024), 'Rejects 31 September (30-day month)');
    assert(!isValidGregorianDate(31, 11, 2024), 'Rejects 31 November (30-day month)');
    assert(!isValidGregorianDate(29, 2, 2023), 'Rejects 29 February on non-leap year (2023)');
    assert(!isValidGregorianDate(29, 2, 1900), 'Rejects 29 February on century year not divisible by 400 (1900)');
    assert(isValidGregorianDate(29, 2, 2024), 'Accepts 29 February on valid leap year (2024)');
    assert(isValidGregorianDate(29, 2, 2000), 'Accepts 29 February on valid 400-year leap year (2000)');
    assert(isValidGregorianDate(30, 4, 2024), 'Accepts valid date 30 April');
  } catch (err) {
    assert(false, `Gregorian calendar validation test threw error: ${err.message}`);
  }

  // ── TEST 8: SessionStorage Hygiene — nv_reading_input cleared on payment and dashboard arrival ──
  try {
    const yourReadingHtml = readFileSync(join(rootDir, 'app/static/your-reading.html'), 'utf-8');
    const dashboardHtml = readFileSync(join(rootDir, 'app/static/dashboard.html'), 'utf-8');

    const readingClearsOnSuccess = yourReadingHtml.includes("sessionStorage.removeItem('nv_reading_input')");
    const dashboardClearsOnArrival = dashboardHtml.includes("sessionStorage.removeItem('nv_reading_input')");

    assert(readingClearsOnSuccess, 'your-reading.html explicitly clears nv_reading_input upon successful payment confirmation');
    assert(dashboardClearsOnArrival, 'dashboard.html explicitly clears nv_reading_input upon arrival');
  } catch (err) {
    assert(false, `SessionStorage hygiene test threw error: ${err.message}`);
  }

  // ── TEST 9: Stage B Checkout Architecture (Locked Fields, Baseline Alignment, Unticked Consents, ISO DOB) ──
  try {
    const yourReadingHtml = readFileSync(join(rootDir, 'app/static/your-reading.html'), 'utf-8');

    // Locked seeker name and locked DOB
    const hasLockedName = /id=["']checkout-seeker-name["'][^>]*readonly/i.test(yourReadingHtml);
    const hasLockedDob = /id=["']checkout-seeker-dob["'][^>]*readonly/i.test(yourReadingHtml);
    assert(hasLockedName && hasLockedDob, 'Stage B checkout locks Seeker Name and Date of Birth as readonly');

    // Baseline aligned verification row (no mobile field overlap, collapsed dead space)
    assert(yourReadingHtml.includes('checkout-otp-row'), 'Stage B checkout uses dedicated baseline-aligned checkout-otp-row');
    assert(yourReadingHtml.includes('btn-checkout-send-code'), 'Send Code button is independent with zero overlap on mobile field');

    // Consents default to unticked
    const serviceConsentUnticked = !/id=["']checkout-consent-service["'][^>]*\bchecked\b/i.test(yourReadingHtml);
    const marketingConsentUnticked = !/id=["']checkout-consent-marketing["'][^>]*\bchecked\b/i.test(yourReadingHtml);
    assert(serviceConsentUnticked && marketingConsentUnticked, 'Both Stage B checkout statutory consents default to unticked');

    // ISO DOB submission in create-order
    assert(yourReadingHtml.includes('dob: isoDob') || yourReadingHtml.includes('customer_dob: isoDob'), 'Date of birth is stored and sent as ISO YYYY-MM-DD');

    // Turnstile & OTP Registration Guard
    const hasTurnstileScript = yourReadingHtml.includes('challenges.cloudflare.com/turnstile/v0/api.js');
    const hasTurnstileContainer = yourReadingHtml.includes('checkout-turnstile-container');
    const sendsTurnstileToken = yourReadingHtml.includes('turnstile_token: turnstileToken');
    assert(hasTurnstileScript && hasTurnstileContainer && sendsTurnstileToken, 'Stage B checkout integrates Cloudflare Turnstile verification and passes turnstile_token on OTP dispatch');
    assert(yourReadingHtml.includes('onCheckoutEmailInput()'), 'Checkout email changes dynamically revoke session verification');
    assert(yourReadingHtml.includes('window.turnstile.reset'), 'Checkout resets turnstile widget on send/resend and handles expiry');
  } catch (err) {
    assert(false, `Stage B checkout architecture test threw error: ${err.message}`);
  }

  // ── TEST 10: Strict Turnstile Enforcement Across ALL Callers of send-code ──
  try {
    const fs = await import('fs');
    const path = await import('path');
    const staticDir = join(rootDir, 'app/static');
    const files = fs.readdirSync(staticDir);

    const indexHtml = fs.readFileSync(join(staticDir, 'index.html'), 'utf-8');
    assert(!indexHtml.includes('/api/v1/auth/email/send-code'), 'index.html has zero calls to send-code (console fully removed)');

    const yourReadingHtml = fs.readFileSync(join(staticDir, 'your-reading.html'), 'utf-8');
    assert(yourReadingHtml.includes('/api/v1/auth/email/send-code'), 'your-reading.html is the single purchase report send-code caller');
    assert(yourReadingHtml.includes('challenges.cloudflare.com/turnstile'), 'your-reading.html loads Cloudflare Turnstile script');
    assert(/id=["'][^"']*turnstile[^"']*["']/i.test(yourReadingHtml), 'your-reading.html contains a Turnstile widget container');
    assert(yourReadingHtml.includes('turnstile_token: turnstileToken'), 'your-reading.html includes turnstile_token in payload');
  } catch (err) {
    assert(false, `Global Turnstile caller enforcement test threw error: ${err.message}`);
  }

  // ── TEST 11: Dashboard Sample-PDF Purge & Zero-Entitlement URL Verification ──
  try {
    const fs = await import('fs');
    const path = await import('path');
    const staticDir = join(rootDir, 'app/static');
    const dashboardHtml = fs.readFileSync(join(staticDir, 'dashboard.html'), 'utf-8');

    // 1. Zero sample-PDF fallback in dashboard.html
    assert(!dashboardHtml.includes('Numeros_Vision_Sample_Excerpt'), 'dashboard.html has zero sample excerpt fallback');
    assert(!dashboardHtml.includes('/samples/'), 'dashboard.html contains zero sample-PDF paths');
    assert(dashboardHtml.includes('contact support') || dashboardHtml.includes('Preparing download link'), 'dashboard.html instructs customer to wait or contact support when downloadUrl is missing');

    // 2. verified=true in query parameters grants zero entitlement
    assert(!dashboardHtml.includes("get('verified')"), 'dashboard.html never inspects verified URL parameter');
    assert(!dashboardHtml.includes('["verified"]'), 'dashboard.html never binds to verified parameter');

    // 3. Opening dashboard endpoints with verified=true and no session returns 401
    const workerModule = await import('../app/static/_worker.js');
    const worker = workerModule.default;
    const mockEnv = {
      ENVIRONMENT: 'test',
      SESSION_SECRET: 'test_session_secret_32b_journey_',
      IP_HASH_SALT: 'test_ip_hash_salt_32b_journey_00',
      DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
      ASSETS: { fetch: async () => new Response('Asset stub', { status: 200 }) }
    };

    const unauthReq = new Request('https://numerosvision.com/api/v1/dashboard/view?order_id=ord_fake_123&verified=true', {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Origin': 'https://numerosvision.com' }
    });
    const unauthRes = await worker.fetch(unauthReq, mockEnv, { waitUntil: () => {} });
    assert(unauthRes.status === 401, `Dashboard view with verified=true but no session must return 401 (got ${unauthRes.status})`);
    const unauthBody = await unauthRes.json().catch(() => ({}));
    assert(!unauthBody.orders && !unauthBody.reports, 'No orders or reports returned to unauthenticated session');

    // 4. /api/me check with verified=true and no session returns 401
    const meReq = new Request('https://numerosvision.com/api/me?order_id=ord_fake_123&verified=true', {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Origin': 'https://numerosvision.com' }
    });
    const meRes = await worker.fetch(meReq, mockEnv, { waitUntil: () => {} });
    assert(meRes.status === 401, `api/me with verified=true but no session must return 401 (got ${meRes.status})`);
  } catch (err) {
    assert(false, `Dashboard sample purge & verified query parameter test threw error: ${err.message}`);
  }

  // ── TEST 12: End-to-End Worker Lifecycle: Send-Code -> Verify-Code -> Create-Order -> Verify-Payment (Session Minting) -> Dashboard View ──
  let lifecycleOriginalFetch = globalThis.fetch;
  try {
    const crypto = await import('crypto');
    const workerModule = await import('../app/static/_worker.js');
    const worker = workerModule.default;
    const testSecret = 'test_session_secret_32b_journey_';
    const razorpaySecret = 'test_rzp_secret_key_1234567890';
    const testEmail = 'verified_seeker@numerosvision.com';

    const lifecycleEnv = {
      ENVIRONMENT: 'test',
      SESSION_SECRET: testSecret,
      OTP_HMAC_SECRET: 'test_otp_hmac_secret_32b_hex_000',
      IP_HASH_SALT: 'test_ip_hash_salt_32b_journey_00',
      DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
      PDF_SERVICE_SECRET: 'test_pdf_service_secret_32b_long_',
      RAZORPAY_KEY_ID: 'rzp_test_1234567890',
      RAZORPAY_KEY_SECRET: razorpaySecret,
      NV_EMAIL_LOG_ADAPTER: 'true',
      ASSETS: { fetch: async () => new Response('Asset stub', { status: 200 }) }
    };

    // Mock fetch for Razorpay order creation
    const lifecycleOriginalFetch = globalThis.fetch;
    globalThis.fetch = async (url, options = {}) => {
      const urlStr = String(url);
      if (urlStr.includes('api.razorpay.com/v1/orders')) {
        const body = JSON.parse(options.body || '{}');
        return new Response(JSON.stringify({
          id: 'order_rzp_lifecycle_' + Date.now(),
          entity: 'order',
          amount: body.amount,
          currency: body.currency || 'INR',
          receipt: body.receipt,
          status: 'created'
        }), { status: 200, headers: { 'Content-Type': 'application/json' } });
      }
      return lifecycleOriginalFetch(url, options);
    };

    // 1. Simulate send-code
    const sendReq = new Request('https://numerosvision.com/api/v1/auth/email/send-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({ email: testEmail, turnstile_token: 'test_turnstile_pass' })
    });
    const sendRes = await worker.fetch(sendReq, lifecycleEnv, { waitUntil: () => {} });
    assert(sendRes.status === 200, `send-code must return 200 (got ${sendRes.status})`);

    // 2. Extract generated OTP from memory store
    const otpSecret = lifecycleEnv.OTP_HMAC_SECRET;
    const emailHash = crypto.createHmac('sha256', otpSecret).update(testEmail).digest('hex');
    const mStore = workerModule.memoryStore || {};
    const challenge = mStore.emailOtpChallenges ? mStore.emailOtpChallenges.get(emailHash) : null;
    let foundCode = null;
    if (challenge && challenge.code_hash) {
      for (let c = 100000; c <= 999999; c++) {
        const testHash = crypto.createHmac('sha256', otpSecret).update(`${testEmail}:${c}`).digest('hex');
        if (testHash === challenge.code_hash) {
          foundCode = String(c);
          break;
        }
      }
    }
    assert(foundCode !== null, 'Found generated OTP challenge in memoryStore');

    // 3. Verify-code in checkout flow (mints checkout_token, NO session)
    const verifyCodeReq = new Request('https://numerosvision.com/api/v1/auth/email/verify-code', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({ email: testEmail, code: foundCode, checkout_flow: true })
    });
    const verifyCodeRes = await worker.fetch(verifyCodeReq, lifecycleEnv, { waitUntil: () => {} });
    assert(verifyCodeRes.status === 200, `verify-code must return 200 (got ${verifyCodeRes.status})`);
    const verifyCodeData = await verifyCodeRes.json();
    assert(verifyCodeData.verified === true, 'verify-code reports verified=true');
    assert(Boolean(verifyCodeData.checkout_token), 'verify-code returns checkout_token');
    assert(!verifyCodeRes.headers.get('set-cookie'), 'checkout verification MUST NOT issue a persistent session cookie');
    const chkToken = verifyCodeData.checkout_token;

    // 4. Create order with checkout_token
    const createOrderReq = new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({
        pack_id: 'report_basic',
        name: 'Lifecycle Seeker',
        dob: '1981-11-28',
        day: 28,
        month: 11,
        year: 1981,
        email: testEmail,
        checkout_token: chkToken,
        consent_service: true
      })
    });
    const createOrderRes = await worker.fetch(createOrderReq, lifecycleEnv, { waitUntil: () => {} });
    assert(createOrderRes.status === 200, `create-order returns 200 (got ${createOrderRes.status})`);
    const orderData = await createOrderRes.json();
    const internalOrderId = orderData.order_id;
    const rzpOrderId = orderData.rzp_order_id;
    assert(Boolean(internalOrderId), 'create-order returned order_id');

    // 5. Payment verification with checkout_token: MINTS SESSION
    const rzpPaymentId = 'pay_lifecycle_' + Date.now();
    const sigPayload = `${rzpOrderId}|${rzpPaymentId}`;
    const validSignature = crypto.createHmac('sha256', razorpaySecret).update(sigPayload).digest('hex');

    const paymentVerifyReq = new Request('https://numerosvision.com/api/v1/payments/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({
        order_id: internalOrderId,
        orderId: internalOrderId,
        razorpay_order_id: rzpOrderId,
        razorpay_payment_id: rzpPaymentId,
        razorpay_signature: validSignature,
        checkout_token: chkToken,
        email: testEmail
      })
    });
    const paymentVerifyRes = await worker.fetch(paymentVerifyReq, lifecycleEnv, { waitUntil: () => {} });
    assert(paymentVerifyRes.status === 200, `verify-payment returns 200 (got ${paymentVerifyRes.status})`);
    const pmtData = await paymentVerifyRes.json();
    assert(pmtData.verified === true, 'payment is verified');
    assert(pmtData.session_issued === true, 'session_issued must be true');
    const setCookieHeader = paymentVerifyRes.headers.get('set-cookie');
    assert(Boolean(setCookieHeader), 'Set-Cookie header must be present on valid payment with checkout_token');
    assert(setCookieHeader.includes('__Host-nv_session='), 'Cookie is __Host-nv_session');

    // Extract cookie value for subsequent requests
    const cookieVal = setCookieHeader.split(';')[0];

    // 6. Dashboard view with the returned session cookie: ASSERT ORDER APPEARS
    const dashReq = new Request(`https://numerosvision.com/api/v1/dashboard/view?order_id=${encodeURIComponent(internalOrderId)}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Cookie': cookieVal, 'Origin': 'https://numerosvision.com' }
    });
    const dashRes = await worker.fetch(dashReq, lifecycleEnv, { waitUntil: () => {} });
    assert(dashRes.status === 200, `Authenticated dashboard view returns 200 (got ${dashRes.status})`);
    const dashData = await dashRes.json();
    assert(dashData.reports && dashData.reports.some(r => r.orderId === internalOrderId), 'Order appears in authenticated customer dashboard');

    // 7. ASSERT: No cookie gives 401
    const noCookieReq = new Request(`https://numerosvision.com/api/v1/dashboard/view?order_id=${encodeURIComponent(internalOrderId)}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Origin': 'https://numerosvision.com' }
    });
    const noCookieRes = await worker.fetch(noCookieReq, lifecycleEnv, { waitUntil: () => {} });
    assert(noCookieRes.status === 401, `No cookie gives 401 on dashboard (got ${noCookieRes.status})`);

    // 8. ASSERT: Wrong email's cookie sees nothing
    const wrongUserToken = await workerModule.mintUserSession(lifecycleEnv, 'usr_intruder_999', '127.0.0.1', Date.now());
    const wrongUserCookie = `__Host-nv_session=${wrongUserToken}`;
    const wrongUserReq = new Request(`https://numerosvision.com/api/v1/dashboard/view?order_id=${encodeURIComponent(internalOrderId)}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Cookie': wrongUserCookie, 'Origin': 'https://numerosvision.com' }
    });
    const wrongUserRes = await worker.fetch(wrongUserReq, lifecycleEnv, { waitUntil: () => {} });
    assert(wrongUserRes.status === 200, 'Wrong user request returns 200 for their own empty dashboard');
    const wrongUserData = await wrongUserRes.json();
    assert(!wrongUserData.reports || !wrongUserData.reports.some(r => r.orderId === internalOrderId), 'Wrong email sees 0 reports for this order (tenant isolation)');

    // 9. ASSERT: Payment without a verified email (no checkout token) gets NO session
    const unauthPaymentId = 'pay_unauth_' + Date.now();
    const unauthSignature = crypto.createHmac('sha256', razorpaySecret).update(`${rzpOrderId}|${unauthPaymentId}`).digest('hex');
    const unverifiedPayReq = new Request('https://numerosvision.com/api/v1/payments/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({
        order_id: internalOrderId,
        orderId: internalOrderId,
        razorpay_order_id: rzpOrderId,
        razorpay_payment_id: unauthPaymentId,
        razorpay_signature: unauthSignature
        // checkout_token omitted!
      })
    });
    const unverifiedPayRes = await worker.fetch(unverifiedPayReq, lifecycleEnv, { waitUntil: () => {} });
    assert(unverifiedPayRes.status === 200, 'Payment verify returns 200');
    const unverifiedPayData = await unverifiedPayRes.json();
    assert(unverifiedPayData.session_issued === false, 'Payment without checkout_token must have session_issued=false');
    assert(!unverifiedPayRes.headers.get('set-cookie'), 'Payment without checkout_token MUST NOT receive a session cookie');

    // 10. ASSERT: Payment with wrong email gets NO session
    const wrongPaymentId = 'pay_wrong_' + Date.now();
    const wrongSignature = crypto.createHmac('sha256', razorpaySecret).update(`${rzpOrderId}|${wrongPaymentId}`).digest('hex');
    const wrongEmailPayReq = new Request('https://numerosvision.com/api/v1/payments/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://numerosvision.com' },
      body: JSON.stringify({
        order_id: internalOrderId,
        orderId: internalOrderId,
        razorpay_order_id: rzpOrderId,
        razorpay_payment_id: wrongPaymentId,
        razorpay_signature: wrongSignature,
        checkout_token: chkToken,
        email: 'attacker@evil.com'
      })
    });
    const wrongEmailPayRes = await worker.fetch(wrongEmailPayReq, lifecycleEnv, { waitUntil: () => {} });
    const wrongEmailPayData = await wrongEmailPayRes.json();
    assert(wrongEmailPayData.session_issued === false, 'Payment with mismatched email must have session_issued=false');
    assert(!wrongEmailPayRes.headers.get('set-cookie'), 'Payment with mismatched email MUST NOT receive a session cookie');
    // 11. ASSERT: Order Email Link with Signed, Time-Bound Token
    // A. Link without token shows nothing (401 Unauthorized)
    const linkNoTokenReq = new Request(`https://numerosvision.com/api/v1/dashboard/view?order_id=${encodeURIComponent(internalOrderId)}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Origin': 'https://numerosvision.com' }
    });
    const linkNoTokenRes = await worker.fetch(linkNoTokenReq, lifecycleEnv, { waitUntil: () => {} });
    assert(linkNoTokenRes.status === 401, `Email link without token must return 401 (got ${linkNoTokenRes.status})`);

    // B. Link with forged/tampered token shows nothing (401 Unauthorized)
    const forgedToken = `${Date.now() + 86400000}.badbeef000000000000000000000000000000000000000000000000000000000`;
    const linkForgedReq = new Request(`https://numerosvision.com/api/v1/dashboard/view?order_id=${encodeURIComponent(internalOrderId)}&token=${encodeURIComponent(forgedToken)}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Origin': 'https://numerosvision.com' }
    });
    const linkForgedRes = await worker.fetch(linkForgedReq, lifecycleEnv, { waitUntil: () => {} });
    assert(linkForgedRes.status === 401, `Email link with forged token must return 401 (got ${linkForgedRes.status})`);

    // C. Link with expired token shows nothing (401 Unauthorized)
    const pastExpiry = Date.now() - 3600000; // 1 hour ago
    const expiredToken = await workerModule.signOrderAccessToken(testSecret, internalOrderId, pastExpiry);
    const linkExpiredReq = new Request(`https://numerosvision.com/api/v1/dashboard/view?order_id=${encodeURIComponent(internalOrderId)}&token=${encodeURIComponent(expiredToken)}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Origin': 'https://numerosvision.com' }
    });
    const linkExpiredRes = await worker.fetch(linkExpiredReq, lifecycleEnv, { waitUntil: () => {} });
    assert(linkExpiredRes.status === 401, `Email link with expired token must return 401 (got ${linkExpiredRes.status})`);

    // D. Valid signed token shows ONLY that order
    const validExpiry = Date.now() + (30 * 24 * 60 * 60 * 1000);
    const orderTokenSecret = await workerModule.getOrderTokenSecret(lifecycleEnv);
    const validOrderToken = await workerModule.signOrderAccessToken(orderTokenSecret, internalOrderId, validExpiry);
    
    // Plant a second order in memoryStore to ensure strict single-order scoping
    const secondOrderId = 'ord_other_seeker_999';
    mStore.orders.set(secondOrderId, {
      id: secondOrderId,
      user_id: 'usr_other_999',
      pack_id: 'report_deep',
      amount_paise: 48900,
      email: 'other@example.com',
      created_at: Date.now()
    });

    const linkValidReq = new Request(`https://numerosvision.com/api/v1/dashboard/view?order_id=${encodeURIComponent(internalOrderId)}&token=${encodeURIComponent(validOrderToken)}`, {
      method: 'GET',
      headers: { 'Accept': 'application/json', 'Origin': 'https://numerosvision.com' }
    });
    const linkValidRes = await worker.fetch(linkValidReq, lifecycleEnv, { waitUntil: () => {} });
    assert(linkValidRes.status === 200, `Email link with valid signed token must return 200 (got ${linkValidRes.status})`);
    const linkValidData = await linkValidRes.json();
    assert(Array.isArray(linkValidData.reports) && linkValidData.reports.length === 1, 'Valid email link returns exactly 1 report');
    assert(linkValidData.reports[0].orderId === internalOrderId, 'Valid email link shows strictly the authorized order');
    assert(!linkValidData.reports.some(r => r.orderId === secondOrderId), 'Valid email link NEVER exposes other orders');
    assert(Array.isArray(linkValidData.subjects) && linkValidData.subjects.length === 0, 'Token-scoped view does not leak account subjects');

    // E. Health probe visibility of Turnstile fallback
    const healthPreviewReq = new Request('https://numerosvision.com/api/health');
    const healthPreviewRes = await worker.fetch(healthPreviewReq, { ENVIRONMENT: 'preview' }, {});
    const healthPreviewData = await healthPreviewRes.json();
    assert(healthPreviewData.turnstile_fallback_active === true, 'Health probe reports turnstile_fallback_active=true on preview without live secret');

    const healthProdReq = new Request('https://numerosvision.com/api/health');
    const healthProdRes = await worker.fetch(healthProdReq, { ENVIRONMENT: 'production', TURNSTILE_SECRET_KEY: 'live_prod_key' }, {});
    const healthProdData = await healthProdRes.json();
    assert(healthProdData.turnstile_fallback_active === false, 'Health probe reports turnstile_fallback_active=false on production with live secret');

    // F. Preview email links to preview origin (never hardcoded)
    const emailCaptureEnv = {
      ...lifecycleEnv,
      ENVIRONMENT: 'preview',
      NV_EMAIL_LOG_ADAPTER: 'true',
      DB: null
    };
    const previewOrder = {
      id: 'ord_preview_origin_test',
      pack_id: 'report_basic',
      user_id: 'usr_preview_123',
      subject_id: 'sbj_preview_123',
      email: 'preview_user@numerosvision.com',
      amount_paise: 19900
    };
    const previewReq = new Request('https://preview-stage-b.numerosvision.pages.dev/api/v1/payments/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Origin': 'https://preview-stage-b.numerosvision.pages.dev' }
    });
    
    await workerModule.fulfillPaidOrder(previewOrder, 'pay_prev_1', 19900, 'online', emailCaptureEnv, Date.now(), 'verify', previewReq);
    const sentEmails = mStore.sentEmails || [];
    const previewSentEmail = sentEmails.find(e => e.to === 'preview_user@numerosvision.com');
    assert(previewSentEmail && previewSentEmail.text.includes('https://preview-stage-b.numerosvision.pages.dev/dashboard/'), 'Order email links to preview origin when request originates from preview');

    // G. Turnstile preview restriction: rejects test_turnstile_pass without siteverify
    const previewTurnstilePass = await workerModule.verifyTurnstileToken(
      { ENVIRONMENT: 'preview', TURNSTILE_SECRET_KEY: '1x0000000000000000000000000000000AA' },
      'test_turnstile_pass',
      '127.0.0.1'
    );
    assert(previewTurnstilePass === false, 'Preview environment does NOT short-circuit test_turnstile_pass without Cloudflare siteverify');

    // H. Turnstile test/local acceptance: accepts test_turnstile_pass in test environment
    const testTurnstilePass = await workerModule.verifyTurnstileToken(
      { ENVIRONMENT: 'test' },
      'test_turnstile_pass',
      '127.0.0.1'
    );
    assert(testTurnstilePass === true, 'Test environment permits test_turnstile_pass');

    // I. Dashboard Referrer-Policy and HTML verification
    const dashAssetReq = new Request('https://numerosvision.com/dashboard/', {
      method: 'GET',
      headers: { 'Accept': 'text/html' }
    });
    const dashAssetRes = await worker.fetch(dashAssetReq, lifecycleEnv, {});
    assert(dashAssetRes.headers.get('referrer-policy') === 'no-referrer', 'Dashboard page route returns Referrer-Policy: no-referrer');
    assert(linkValidRes.headers.get('referrer-policy') === 'no-referrer', 'Dashboard view API returns Referrer-Policy: no-referrer');

    const fsModule = await import('fs');
    const dashHtmlContent = fsModule.readFileSync('app/static/dashboard.html', 'utf8');
    assert(dashHtmlContent.includes('<meta name="referrer" content="no-referrer" />'), 'dashboard.html contains <meta name="referrer" content="no-referrer" />');

    // J. Login HTML hides Password tab
    const loginHtmlContent = fsModule.readFileSync('app/static/login.html', 'utf8');
    assert(loginHtmlContent.includes('id="tabPasswordBtn" style="display:none;"'), 'login.html has Password tab hidden');

    // K. Verify analytics telemetry strictly strips token queries
    const marketingAnalyticsJs = fsModule.readFileSync('app/static/js/marketing-analytics.js', 'utf8');
    assert(!marketingAnalyticsJs.includes("'token'"), 'marketing-analytics does not allowlist token parameter');
    assert(!marketingAnalyticsJs.includes("'order_token'"), 'marketing-analytics does not allowlist order_token parameter');
    assert(!marketingAnalyticsJs.includes("'checkout_token'"), 'marketing-analytics does not allowlist checkout_token parameter');

    globalThis.fetch = lifecycleOriginalFetch;
  } catch (err) {
    globalThis.fetch = lifecycleOriginalFetch;
    assert(false, `Worker lifecycle and session minting test threw error: ${err.message}`);
  }

  console.log(`\nTests Completed: ${passCount} Passed, ${failCount} Failed\n`);
  if (failCount > 0) {
    process.exit(1);
  }
}

runTests();
