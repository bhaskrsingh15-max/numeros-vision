// tests/test_analytics_payload_privacy.mjs
import assert from 'node:assert';
import fs from 'node:fs';
import vm from 'node:vm';

console.log('--- STARTING TELEMETRY & MARKETING PAYLOAD PRIVACY AUDIT TEST ---');

// 1. Setup Mock Browser Environment
const capturedDataLayer = [];
const capturedFbq = [];
const capturedFetch = [];

const mockLocalStorage = {
  _data: {
    'nv_cookie_consent_v5': JSON.stringify({ essential: true, analytics: true, marketing: true }),
    'nv_device_id': 'nv_dev_test_device_123',
    'nv_uid': 'NV-USR-TEST-001'
  },
  getItem(k) { return this._data[k] || null; },
  setItem(k, v) { this._data[k] = String(v); },
  removeItem(k) { delete this._data[k]; }
};

const mockSessionStorage = {
  _data: {},
  getItem(k) { return this._data[k] || null; },
  setItem(k, v) { this._data[k] = String(v); },
  removeItem(k) { delete this._data[k]; }
};

const domWindow = {
  dataLayer: {
    push: function (...args) {
      capturedDataLayer.push(...args);
    }
  },
  fbq: function (...args) {
    capturedFbq.push(args);
  },
  localStorage: mockLocalStorage,
  sessionStorage: mockSessionStorage,
  location: {
    pathname: '/tools/lo-shu-grid/',
    search: '?utm_source=google&utm_medium=cpc&utm_campaign=numerology_brand',
    href: 'https://numerosvision.com/tools/lo-shu-grid/?utm_source=google'
  },
  URLSearchParams: globalThis.URLSearchParams,
  document: {
    title: 'Numeros Vision | Lo Shu Grid Calculator',
    createElement: () => ({ setAttribute: () => {}, appendChild: () => {} }),
    head: { appendChild: () => {} },
    body: { appendChild: () => {} },
    querySelectorAll: () => [],
    getElementById: () => null,
    readyState: 'complete'
  },
  navigator: { userAgent: 'Mozilla/5.0 Test Suite Chromium' },
  screen: { width: 1200 },
  innerWidth: 1200,
  matchMedia: () => ({ matches: false }),
  addEventListener: () => {},
  fetch: function (url, opts) {
    capturedFetch.push({ url, opts });
    return Promise.resolve({ ok: true, json: () => Promise.resolve({}) });
  },
  console: {
    log: () => {},
    debug: () => {},
    info: () => {},
    warn: () => {},
    error: () => {}
  }
};

domWindow.window = domWindow;
const context = vm.createContext(domWindow);

// 2. Execute marketing-analytics.js inside context
const analyticsCode = fs.readFileSync('app/static/js/marketing-analytics.js', 'utf8');
vm.runInContext(analyticsCode, context);

// 3. Prohibited Terms & Patterns Regex
const PROHIBITED_KEYS = [
  'dob', 'birth_date', 'birthdate', 'birth_time', 'birth_place', 'birth_city',
  'city', 'place', 'name', 'full_name', 'first_name', 'last_name', 'user_name',
  'email', 'phone', 'mobile', 'driver', 'conductor', 'driver_mulank', 'conductor_bhagyank',
  'mulank', 'bhagyank', 'destiny', 'lifepath', 'life_path', 'kua', 'loshu', 'grid', 'chart',
  'gaid', 'idfa', 'idfv', 'user_id', 'golden_profile_id'
];

const PROHIBITED_URL_PARAMS = [
  'dob=', 'birth_date=', 'birth_time=', 'birth_place=', 'city=', 'name=',
  'email=', 'phone=', 'mobile=', 'driver=', 'conductor=', 'mulank=', 'bhagyank=', 'loshu='
];

const EMAIL_REGEX = /[^\s@]+@[^\s@]+\.[^\s@]+/;
const PHONE_REGEX = /\b(?:\+?\d{1,3}[- ]?)?\d{10}\b/;
const DOB_REGEX = /\b(?:\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{4}|\d{8})\b/;

function assertNoPIIOrChartData(obj, path = 'root') {
  if (!obj || typeof obj !== 'object') return;

  if (Array.isArray(obj)) {
    obj.forEach((item, idx) => assertNoPIIOrChartData(item, `${path}[${idx}]`));
    return;
  }

  for (const [key, val] of Object.entries(obj)) {
    const currentPath = `${path}.${key}`;
    const lowerKey = key.toLowerCase();

    // Check prohibited key names
    for (const forbidden of PROHIBITED_KEYS) {
      assert.notStrictEqual(
        lowerKey,
        forbidden,
        `SECURITY VIOLATION: Telemetry payload contains forbidden key '${forbidden}' at ${currentPath}`
      );
    }

    // Check string values
    if (typeof val === 'string') {
      // Check for email
      assert.strictEqual(
        EMAIL_REGEX.test(val),
        false,
        `SECURITY VIOLATION: Telemetry value contains email '${val}' at ${currentPath}`
      );
      // Check for phone number
      assert.strictEqual(
        PHONE_REGEX.test(val),
        false,
        `SECURITY VIOLATION: Telemetry value contains phone number '${val}' at ${currentPath}`
      );
      // Check for date of birth
      assert.strictEqual(
        DOB_REGEX.test(val),
        false,
        `SECURITY VIOLATION: Telemetry value contains date of birth '${val}' at ${currentPath}`
      );
      // Check for URL query param leakage
      const lowerVal = val.toLowerCase();
      for (const forbiddenParam of PROHIBITED_URL_PARAMS) {
        assert.strictEqual(
          lowerVal.includes(forbiddenParam),
          false,
          `SECURITY VIOLATION: Telemetry URL/string contains forbidden query param '${forbiddenParam}' at ${currentPath}: ${val}`
        );
      }
    }

    if (typeof val === 'object' && val !== null) {
      assertNoPIIOrChartData(val, currentPath);
    }
  }
}

// 4. Test Scenario A: Page View with potential URL leakage
console.log('Testing Scenario A: pageView execution with PII query params in URL...');
domWindow.nvTrack.pageView('/tools/lo-shu-grid/?dob=1990-08-15&name=Alexander&phone=9876543210&utm_source=google', 'Lo Shu Tool');

// 5. Test Scenario B: Calculator Used with birth and chart data attempted
console.log('Testing Scenario B: calculatorUsed with attempted chart inputs...');
domWindow.nvTrack.calculatorUsed('lo_shu_grid', {
  dob: '1988-11-23',
  birth_time: '14:30',
  birth_place: 'Mumbai',
  name: 'Kavita Iyer',
  driver_mulank: 5,
  conductor_bhagyank: 6,
  grid: [1, 5, 8],
  chart: { sun: 'Leo' }
});

// 6. Test Scenario C: Free Signup / Lead Event with PII attempted
console.log('Testing Scenario C: freeSignup with full user contact info...');
domWindow.nvTrack.freeSignup({
  source: 'free_calculator_gate',
  name: 'Rohan Sharma',
  email: 'rohan.sharma@example.com',
  phone: '+919876543210',
  dob: '1992-05-18',
  birth_time: '08:15',
  birth_city: 'Delhi',
  driver_mulank: 9,
  conductor_bhagyank: 8
});

// 7. Test Scenario D: Initiate Checkout
console.log('Testing Scenario D: initiateCheckout with plan info and user details...');
domWindow.nvTrack.initiateCheckout('Basic Report', 199, {
  name: 'Rohan Sharma',
  email: 'rohan@example.com',
  dob: '1992-05-18',
  chart_type: 'vedic'
});

// 8. Test Scenario E: Paid Purchase
console.log('Testing Scenario E: paidPurchase with order and transaction data...');
domWindow.nvTrack.paidPurchase('order_NV_2026_9999', 'Advanced Master Dossier', 489, 'INR', {
  name: 'Rohan Sharma',
  email: 'rohan@example.com',
  phone: '9876543210',
  dob: '1992-05-18',
  birth_place: 'Bengaluru'
});

// 9. Test Scenario F: Direct dataLayer.push and gtag calls with raw PII
console.log('Testing Scenario F: Direct dataLayer.push and gtag invocations...');
domWindow.dataLayer.push({
  event: 'custom_diagnostic',
  name: 'Direct User',
  email: 'direct@test.com',
  phone: '9998887776',
  dob: '1985-12-31',
  birth_place: 'Chennai',
  driver: 4,
  conductor: 3,
  loshu: [3, 4]
});

domWindow.gtag('event', 'lead_test', {
  name: 'Gtag User',
  email: 'gtag@test.com',
  dob: '1990-01-01',
  mulank: 1
});

// 10. Audit all captured payloads
console.log('\n--- AUDITING ALL CAPTURED TELEMETRY PAYLOADS ---');
console.log(`Auditing ${capturedDataLayer.length} dataLayer entries...`);
for (let i = 0; i < capturedDataLayer.length; i++) {
  const item = capturedDataLayer[i];
  assertNoPIIOrChartData(item, `dataLayer[${i}]`);
}
console.log('✓ All dataLayer entries are strictly 100% free of PII and chart vectors.');

console.log(`Auditing ${capturedFbq.length} Meta Pixel (fbq) calls...`);
for (let i = 0; i < capturedFbq.length; i++) {
  const callArgs = capturedFbq[i];
  assertNoPIIOrChartData(callArgs, `fbq[${i}]`);
}
console.log('✓ All Meta Pixel payloads are strictly 100% free of PII and chart vectors.');

console.log('\n--- ALL TELEMETRY PRIVACY AUDIT TESTS PASSED (100% PII & CHART-FREE) ---');
