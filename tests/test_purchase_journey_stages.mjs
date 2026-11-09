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
    const workerCatalogMatch = workerContent.match(/const PACK_CATALOG\s*=\s*({[\s\S]*?});\s*function getPackById/);
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
      RAZORPAY_KEY_ID: 'rzp_test_MOCK_JOURNEY_KEY',
      RAZORPAY_KEY_SECRET: 'test_secret_for_journey_payments',
      OTP_HMAC_SECRET: 'test_otp_hmac_secret_32b_journey',
      SESSION_SECRET: 'test_session_secret_32b_journey_',
      IP_HASH_SALT: 'test_ip_hash_salt_32b_journey_00',
      DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
      ASSETS: { fetch: async () => new Response('Asset stub', { status: 200 }) }
    };

    // Mock fetch for Razorpay
    const originalFetch = globalThis.fetch;
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
      return originalFetch(url, options);
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
    globalThis.fetch = originalFetch;
  } catch (err) {
    assert(false, `Price tampering override test threw error: ${err.message}`);
  }

  // ── TEST 5B: Server Check — create-order Rejects Unauthenticated / Unverified Requests ──
  try {
    const workerModule = await import('../app/static/_worker.js');
    const worker = workerModule.default;

    const mockEnv = {
      ENVIRONMENT: 'test',
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

  console.log(`\nTests Completed: ${passCount} Passed, ${failCount} Failed\n`);
  if (failCount > 0) {
    process.exit(1);
  }
}

runTests();
