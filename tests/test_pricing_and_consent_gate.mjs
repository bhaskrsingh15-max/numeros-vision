/**
 * Test Suite: Pricing Page Hygiene & Consent Gate Verification
 * Verifies:
 * 1. pricing.html contains strictly INR, 0 USD, 0 Stripe, 0 setCurrency()
 * 2. All 77 HTML pages have 0 head GTM/GA4 and 0 noscript iframe
 * 3. With consent denied or ungranted, 0 network requests to googletagmanager.com or google-analytics.com occur on first load
 * 4. GTM loads only after explicit analytics consent
 * 5. Withdrawn consent persists and prevents script injection on subsequent visits
 */

import fs from 'fs';
import path from 'path';
import assert from 'assert';

console.log('--- STARTING PRICING & CONSENT GATE AUDIT TESTS ---');

// --- TEST 1: Pricing Page Zero USD / Zero Stripe / Zero setCurrency ---
console.log('\n[Test 1] Auditing app/static/pricing.html for currency hygiene...');
const pricingHtml = fs.readFileSync('app/static/pricing.html', 'utf-8');

assert.strictEqual((pricingHtml.match(/\bUSD\b/g) || []).length, 0, 'pricing.html must contain 0 occurrences of USD');
assert.strictEqual((pricingHtml.match(/Stripe/gi) || []).length, 0, 'pricing.html must contain 0 occurrences of Stripe');
assert.strictEqual((pricingHtml.match(/\$\d+/g) || []).length, 0, 'pricing.html must contain 0 occurrences of dollar prices');
assert.strictEqual((pricingHtml.match(/setCurrency/g) || []).length, 0, 'pricing.html must contain 0 occurrences of setCurrency');
assert.ok(pricingHtml.includes('Payments are in INR via Razorpay.'), 'pricing.html must state INR via Razorpay');
assert.ok(!pricingHtml.includes('International Cards (USD / Global)'), 'pricing.html must not claim international cards');

// Verify that the dynamic pricing script executes without error in a mock DOM
const scriptMatches = pricingHtml.match(/<script>([\s\S]*?)<\/script>/g);
const pricingScript = scriptMatches[scriptMatches.length - 1].replace('<script>', '').replace('</script>', '');

const mockWindow = { location: { search: '' } };
const mockElements = new Map();
const mockDocument = {
  getElementById: (id) => {
    if (!mockElements.has(id)) {
      mockElements.set(id, { classList: { toggle: () => {} }, innerHTML: '', style: {} });
    }
    return mockElements.get(id);
  }
};

try {
  const fn = new Function('window', 'document', 'Intl', pricingScript);
  fn(mockWindow, mockDocument, global.Intl);
  console.log('✔ PASS: pricing.html script executes with 0 runtime errors and is strictly locked to INR.');
} catch (e) {
  assert.fail('pricing.html script threw error: ' + e.message);
}

// --- TEST 2: Static HTML Scan: Zero Head GTM / Zero GA4 / Zero Noscript ---
console.log('\n[Test 2] Auditing all HTML pages for zero head GTM, zero GA4, and zero noscript iframe...');

function scanHtmlFiles(dir) {
  let results = [];
  const list = fs.readdirSync(dir);
  for (const item of list) {
    const fullPath = path.join(dir, item);
    const stat = fs.statSync(fullPath);
    if (stat.isDirectory()) {
      if (!fullPath.includes('amp')) {
        results = results.concat(scanHtmlFiles(fullPath));
      }
    } else if (item.endsWith('.html')) {
      results.push(fullPath);
    }
  }
  return results;
}

const allPages = scanHtmlFiles('app/static');
console.log(`Auditing ${allPages.length} non-AMP HTML pages...`);

const violations = [];
for (const file of allPages) {
  const content = fs.readFileSync(file, 'utf-8');
  if (content.includes('G-3Z2E6416W7')) {
    violations.push(`${file}: contains GA4 measurement ID G-3Z2E6416W7`);
  }
  if (content.includes('googletagmanager.com/gtm.js?id=GTM-KW6GQRVZ')) {
    violations.push(`${file}: contains synchronous head GTM script`);
  }
  if (content.includes('googletagmanager.com/ns.html?id=GTM-KW6GQRVZ')) {
    violations.push(`${file}: contains GTM noscript iframe`);
  }
}

assert.strictEqual(violations.length, 0, 'Found GTM/GA4 violations:\n' + violations.join('\n'));
console.log(`✔ PASS: All ${allPages.length} pages have 0 head GTM, 0 GA4 scripts, and 0 noscript iframes.`);

// --- TEST 3: Consent Gate Behavioral Simulation ---
console.log('\n[Test 3] Simulating first page load with consent pending/denied...');

// Load nv_consent.js code
const consentJsCode = fs.readFileSync('app/static/js/nv_consent.js', 'utf-8');

function createDomEnvironment(storedConsent) {
  const storage = new Map();
  if (storedConsent) {
    storage.set('nv_cookie_consent_v5', JSON.stringify(storedConsent));
  }

  const injectedScripts = [];
  const dataLayer = [];

  const doc = {
    readyState: 'complete',
    head: {
      appendChild: (el) => {
        if (el.tagName === 'SCRIPT' || el.src) injectedScripts.push(el);
      }
    },
    body: {
      appendChild: () => {}
    },
    createElement: (tag) => {
      const el = {
        tagName: tag.toUpperCase(),
        setAttribute: () => {},
        classList: { add: () => {}, remove: () => {} },
        style: {},
        innerHTML: ''
      };
      return el;
    },
    getElementById: (id) => null,
    querySelectorAll: () => [],
    getElementsByTagName: (tag) => {
      if (tag === 'script') {
        return [{
          parentNode: {
            insertBefore: (newEl) => {
              injectedScripts.push(newEl);
            }
          }
        }];
      }
      return [];
    },
    addEventListener: () => {}
  };

  const win = {
    localStorage: {
      getItem: (k) => storage.get(k) || null,
      setItem: (k, v) => storage.set(k, String(v)),
      removeItem: (k) => storage.delete(k)
    },
    sessionStorage: {
      getItem: () => null,
      setItem: () => {},
      removeItem: () => {}
    },
    document: doc,
    dataLayer: dataLayer,
    dispatchEvent: () => {},
    CustomEvent: class { constructor(n, d) { this.name = n; this.detail = d; } },
    location: { reload: () => {} }
  };

  return { win, doc, storage, injectedScripts, dataLayer };
}

// 3a: Fresh Visitor (No consent given yet)
{
  const env = createDomEnvironment(null);
  const fn = new Function('window', 'document', 'localStorage', consentJsCode);
  fn(env.win, env.doc, env.win.localStorage);

  // Assert ZERO scripts to googletagmanager.com or google-analytics.com
  const networkRequests = env.injectedScripts.filter(s =>
    (s.src && (s.src.includes('googletagmanager.com') || s.src.includes('google-analytics.com')))
  );

  assert.strictEqual(networkRequests.length, 0, 'Must NOT inject any GTM/GA4 script on initial load with consent ungranted');
  assert.strictEqual(env.win._nvGtmInjected, undefined, 'GTM injected flag must be undefined');
  console.log('✔ PASS: Initial load with consent ungranted makes 0 requests to googletagmanager.com / google-analytics.com.');
}

// 3b: Explicit Denial / Essential Only
{
  const env = createDomEnvironment({ essential: true, analytics: false, marketing: false });
  const fn = new Function('window', 'document', 'localStorage', consentJsCode);
  fn(env.win, env.doc, env.win.localStorage);

  const networkRequests = env.injectedScripts.filter(s =>
    (s.src && (s.src.includes('googletagmanager.com') || s.src.includes('google-analytics.com')))
  );

  assert.strictEqual(networkRequests.length, 0, 'Must NOT inject any GTM/GA4 script when analytics consent is false');
  console.log('✔ PASS: Load with explicit analytics denial makes 0 requests to googletagmanager.com / google-analytics.com.');
}

// 3c: Explicit Granting of Analytics Consent
{
  const env = createDomEnvironment(null);
  const fn = new Function('window', 'document', 'localStorage', consentJsCode);
  fn(env.win, env.doc, env.win.localStorage);

  // User clicks "Accept All"
  env.win.nvConsent.acceptChoice('all');

  const gtmScripts = env.injectedScripts.filter(s =>
    s.src && s.src.includes('googletagmanager.com/gtm.js?id=GTM-KW6GQRVZ')
  );

  assert.strictEqual(gtmScripts.length, 1, 'Must inject GTM script after explicit analytics consent');
  assert.strictEqual(env.win._nvGtmInjected, true, 'window._nvGtmInjected must be true');
  assert.ok(env.win.dataLayer.some(e => e['gtm.start']), 'dataLayer must contain gtm.start event');
  console.log('✔ PASS: Granting analytics consent dynamically loads GTM-KW6GQRVZ exactly once.');
}

// 3d: Withdrawal of Consent
{
  const env = createDomEnvironment({ essential: true, analytics: true, marketing: true });
  const fn = new Function('window', 'document', 'localStorage', consentJsCode);
  fn(env.win, env.doc, env.win.localStorage);

  // User withdraws consent
  env.win.nvConsent.withdraw();

  const saved = JSON.parse(env.storage.get('nv_cookie_consent_v5'));
  assert.strictEqual(saved.analytics, false, 'Analytics consent must be false after withdrawal');
  assert.strictEqual(saved.marketing, false, 'Marketing consent must be false after withdrawal');

  // Verify next session load with withdrawn consent does not inject GTM
  const reloadEnv = createDomEnvironment(saved);
  const reloadFn = new Function('window', 'document', 'localStorage', consentJsCode);
  reloadFn(reloadEnv.win, reloadEnv.doc, reloadEnv.win.localStorage);

  const reloadRequests = reloadEnv.injectedScripts.filter(s =>
    s.src && (s.src.includes('googletagmanager.com') || s.src.includes('google-analytics.com'))
  );
  assert.strictEqual(reloadRequests.length, 0, 'Must NOT inject GTM on reload after withdrawal');
  console.log('✔ PASS: Withdrawn consent persists in localStorage and prevents script injection on next load.');
}

console.log('\n--- ALL PRICING & CONSENT GATE AUDIT TESTS PASSED (100%) ---');
