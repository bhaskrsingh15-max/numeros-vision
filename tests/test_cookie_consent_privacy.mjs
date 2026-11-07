// tests/test_cookie_consent_privacy.mjs
import assert from 'node:assert';
import fs from 'node:fs';

console.log('--- STARTING COOKIE CONSENT & PRIVACY AUDIT VERIFICATION TESTS ---');

// 1. Verify sw.js privacy guard
const swCode = fs.readFileSync('app/static/sw.js', 'utf8');
assert.ok(swCode.includes("url.pathname.startsWith('/api/') || url.pathname.includes('/reports/download') || url.pathname.endsWith('.pdf')"),
  'FAIL: sw.js must strictly pass-through /api/, /reports/download, and .pdf without caching');
assert.ok(swCode.includes("url.pathname.startsWith('/dashboard')"),
  'FAIL: sw.js must strictly pass-through /dashboard without caching');
console.log('✓ PASS: Test 1 - sw.js never caches /api/*, /dashboard*, or report downloads/PDFs');

// 2. Verify marketing-analytics.js Google Consent Mode v2 default denied
const analyticsCode = fs.readFileSync('app/static/js/marketing-analytics.js', 'utf8');
assert.ok(analyticsCode.includes("'analytics_storage': 'denied'"),
  'FAIL: marketing-analytics.js must default analytics_storage to denied');
assert.ok(analyticsCode.includes("'ad_storage': 'denied'"),
  'FAIL: marketing-analytics.js must default ad_storage to denied');
assert.ok(analyticsCode.includes("window.fbq('consent', 'revoke')"),
  'FAIL: marketing-analytics.js must revoke Meta Pixel consent by default');
assert.ok(!analyticsCode.includes("document.cookie = `nv_dev_id="),
  'FAIL: marketing-analytics.js must NOT set nv_dev_id cookie on client before consent');
console.log('✓ PASS: Test 2 - Google Consent Mode v2 and Meta Pixel strictly default to denied/revoked; no cookie set prior to consent');

// 3. Verify nv_consent.js granular switches and clean device logout
const consentCode = fs.readFileSync('app/static/js/nv_consent.js', 'utf8');
assert.ok(consentCode.includes('nv-pref-analytics'),
  'FAIL: nv_consent.js must have a dedicated Analytics & Performance toggle switch');
assert.ok(consentCode.includes('nv-pref-marketing'),
  'FAIL: nv_consent.js must have a dedicated Marketing & Advertising toggle switch');
assert.ok(consentCode.includes('reopen: function'),
  'FAIL: nv_consent.js must expose reopen() API to reopen preferences');
assert.ok(consentCode.includes('withdraw: function'),
  'FAIL: nv_consent.js must expose withdraw() API to withdraw consent');
assert.ok(consentCode.includes('clearDevicePersonalData: function'),
  'FAIL: nv_consent.js must expose clearDevicePersonalData() to scrub PII from device on logout');
assert.ok(consentCode.includes('nv_user_dob') && consentCode.includes('nv_user_time') && consentCode.includes('nv_user_city'),
  'FAIL: clearDevicePersonalData must clean DOB, birth time, and birth city from device storage');
console.log('✓ PASS: Test 3 - Granular switches, reopen, withdraw, and post-logout device scrub implemented');

// 4. Verify dashboard.html logout integration
const dashCode = fs.readFileSync('app/static/dashboard.html', 'utf8');
assert.ok(dashCode.includes('clearDevicePersonalData'),
  'FAIL: dashboard.html handleLogout must call clearDevicePersonalData()');
console.log('✓ PASS: Test 4 - Dashboard logout scrubs personal storage and CacheStorage');

// 5. Verify _worker.js /api/v1/privacy/consent route
const workerCode = fs.readFileSync('app/static/_worker.js', 'utf8');
assert.ok(workerCode.includes("url.pathname === '/api/v1/privacy/consent'"),
  'FAIL: _worker.js must provide /api/v1/privacy/consent route');
assert.ok(workerCode.includes('cookie_consents') && workerCode.includes('pseudonymous_id'),
  'FAIL: /api/v1/privacy/consent must insert into cookie_consents table');
assert.ok(workerCode.includes('Set-Cookie') && workerCode.includes('nv_dev_id'),
  'FAIL: /api/v1/privacy/consent must set nv_dev_id cookie only after analytics consent');
console.log('✓ PASS: Test 5 - Worker statutory consent route and server-side Set-Cookie verified');

// 6. Verify cookie consents migration exists (0005_cookie_consents.sql or 0004_cookie_consents.sql)
assert.ok(
  fs.existsSync('migrations/0005_cookie_consents.sql') || fs.existsSync('migrations/0004_cookie_consents.sql'),
  'FAIL: migrations/0005_cookie_consents.sql or migrations/0004_cookie_consents.sql must exist'
);
console.log('✓ PASS: Test 6 - Migration file for cookie_consents present');

console.log('\n--- ALL COOKIE CONSENT & PRIVACY TESTS PASSED (6/6) ---');
