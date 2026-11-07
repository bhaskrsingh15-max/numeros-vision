import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert';
import vm from 'node:vm';

console.log('--- STARTING CDP CLEANUP & TELEMETRY ALLOWLIST AUDIT SUITE ---');

const ROOT_DIR = process.cwd();

// Test 1: cdp.html & cdp_tracker.js do not exist in app/static
assert.strictEqual(fs.existsSync(path.join(ROOT_DIR, 'app', 'static', 'cdp.html')), false, 'FAIL: cdp.html still exists in app/static');
assert.strictEqual(fs.existsSync(path.join(ROOT_DIR, 'app', 'static', 'js', 'cdp_tracker.js')), false, 'FAIL: cdp_tracker.js still exists in app/static/js');
console.log('✔ PASS: Test 1: cdp.html and cdp_tracker.js are deleted from app/static');

// Test 2: cdp.html is not referenced in build_bulletproof_dist.py, sitemap.xml, robots.txt
const bbd = fs.readFileSync(path.join(ROOT_DIR, 'build_bulletproof_dist.py'), 'utf-8');
assert.strictEqual(bbd.includes('"cdp": "cdp.html"'), false, 'FAIL: build_bulletproof_dist.py still maps cdp');
const robots = fs.readFileSync(path.join(ROOT_DIR, 'app', 'static', 'robots.txt'), 'utf-8');
assert.strictEqual(robots.includes('cdp'), false, 'FAIL: robots.txt still mentions cdp');
const sitemapXml = fs.readFileSync(path.join(ROOT_DIR, 'app', 'static', 'sitemap.xml'), 'utf-8');
assert.strictEqual(sitemapXml.includes('/cdp/'), false, 'FAIL: sitemap.xml still contains /cdp/');
console.log('✔ PASS: Test 2: cdp.html excluded from build, robots, and sitemap');

// Test 3: Zero pre-filled admin credentials in app/api/cdp.py
const cdpPy = fs.readFileSync(path.join(ROOT_DIR, 'app', 'api', 'cdp.py'), 'utf-8');
assert.strictEqual(cdpPy.includes('NumerosVisionAdmin2026!'), false, 'FAIL: cdp.py still contains NumerosVisionAdmin2026!');
assert.strictEqual(cdpPy.includes('admin@numerosvision.com'), false, 'FAIL: cdp.py still contains admin@numerosvision.com');
console.log('✔ PASS: Test 3: Hardcoded admin credentials deleted from cdp.py');

// Test 4: Fake invoices & unused /billing routes removed from _worker.js
const workerJs = fs.readFileSync(path.join(ROOT_DIR, 'app', 'static', '_worker.js'), 'utf-8');
assert.strictEqual(workerJs.includes('NV-REC-2026-104819'), false, 'FAIL: _worker.js still contains fake invoice NV-REC-2026-104819');
assert.strictEqual(workerJs.includes('NV-REC-2026-104820'), false, 'FAIL: _worker.js still contains fake invoice NV-REC-2026-104820');
assert.strictEqual(workerJs.includes('Synthetic Seeker'), false, 'FAIL: _worker.js still contains Synthetic Seeker');
assert.strictEqual(workerJs.includes("url.pathname.startsWith('/api/v1/billing/')"), false, 'FAIL: _worker.js still contains /api/v1/billing/ router');
console.log('✔ PASS: Test 4: Fake sample invoices and unused /billing routes removed from _worker.js');

// Test 5: Web3Forms payment dispatch removed from _worker.js
assert.strictEqual(workerJs.includes('✦ New Payment & Invoice'), false, 'FAIL: Web3Forms payment dispatch still exists in _worker.js');
console.log('✔ PASS: Test 5: Web3Forms payment dispatch removed from _worker.js');

// Test 6: Zero client-side calls to /api/v1/cdp/* or /payments/funnel/event in app/static/js/
const jsFiles = fs.readdirSync(path.join(ROOT_DIR, 'app', 'static', 'js')).filter(f => f.endsWith('.js'));
for (const file of jsFiles) {
  const code = fs.readFileSync(path.join(ROOT_DIR, 'app', 'static', 'js', file), 'utf-8');
  assert.strictEqual(code.includes('/api/v1/cdp'), false, `FAIL: ${file} still contains /api/v1/cdp call`);
  assert.strictEqual(code.includes('/payments/funnel/event'), false, `FAIL: ${file} still contains /payments/funnel/event call`);
}
console.log('✔ PASS: Test 6: Zero calls to /api/v1/cdp/* or /payments/funnel/event in all client scripts');

// Test 7: Clarity and Firebase injectors removed from marketing-analytics.js
const maJs = fs.readFileSync(path.join(ROOT_DIR, 'app', 'static', 'js', 'marketing-analytics.js'), 'utf-8');
assert.strictEqual(maJs.includes('clarity.ms'), false, 'FAIL: Clarity injector still present in marketing-analytics.js');
assert.strictEqual(maJs.includes('firebase-analytics-compat.js'), false, 'FAIL: Firebase Analytics injector still present in marketing-analytics.js');
assert.strictEqual(maJs.includes('window.nvFirebaseAnalytics'), false, 'FAIL: nvFirebaseAnalytics still referenced in marketing-analytics.js');
console.log('✔ PASS: Test 7: Clarity and Firebase injectors removed from marketing-analytics.js');

// Test 8: sanitizeTelemetryPayload is an ALLOWLIST, not a blocklist
// Extract ALLOWED_TELEMETRY_KEYS and sanitizeTelemetryPayload function directly from marketing-analytics.js
assert.ok(maJs.includes('const ALLOWED_TELEMETRY_KEYS = new Set(['), 'FAIL: ALLOWED_TELEMETRY_KEYS Set not found in marketing-analytics.js');

const fnMatch = maJs.match(/(const ALLOWED_TELEMETRY_KEYS = new Set\([\s\S]*?function sanitizeTelemetryPayload\(obj\) \{[\s\S]*?\n  \})/);
assert.ok(fnMatch, 'FAIL: Could not extract sanitizeTelemetryPayload from marketing-analytics.js');

const sandbox = {
  console: console,
  Set: Set,
  Object: Object,
  Array: Array
};
vm.createContext(sandbox);
const codeToRun = fnMatch[1]
  .replace('const ALLOWED_TELEMETRY_KEYS', 'this.ALLOWED_TELEMETRY_KEYS')
  .replace('function sanitizeTelemetryPayload', 'this.sanitizeTelemetryPayload = function');
vm.runInContext(codeToRun, sandbox);

// Test 8a: Verify gaid, idfa, idfv, user_id, golden_profile_id are NOT in ALLOWED_TELEMETRY_KEYS
assert.strictEqual(sandbox.ALLOWED_TELEMETRY_KEYS.has('gaid'), false, 'FAIL: gaid must NOT be in ALLOWED_TELEMETRY_KEYS');
assert.strictEqual(sandbox.ALLOWED_TELEMETRY_KEYS.has('idfa'), false, 'FAIL: idfa must NOT be in ALLOWED_TELEMETRY_KEYS');
assert.strictEqual(sandbox.ALLOWED_TELEMETRY_KEYS.has('idfv'), false, 'FAIL: idfv must NOT be in ALLOWED_TELEMETRY_KEYS');
assert.strictEqual(sandbox.ALLOWED_TELEMETRY_KEYS.has('user_id'), false, 'FAIL: user_id must NOT be in ALLOWED_TELEMETRY_KEYS');
assert.strictEqual(sandbox.ALLOWED_TELEMETRY_KEYS.has('golden_profile_id'), false, 'FAIL: golden_profile_id must NOT be in ALLOWED_TELEMETRY_KEYS');
console.log('✔ PASS: Test 8a: gaid, idfa, idfv, user_id, golden_profile_id are NOT in ALLOWED_TELEMETRY_KEYS');

// Test 8b: Verify Date format rejection in sanitizeTelemetryPayload
const dateFormatsToTest = [
  '1990-05-15',      // YYYY-MM-DD
  '1990/05/15',      // YYYY/MM/DD
  '15-05-1990',      // DD-MM-YYYY
  '15/05/1990',      // DD/MM/YYYY
  '15051990',        // DDMMYYYY
  '19900515'         // YYYYMMDD
];

for (const dateStr of dateFormatsToTest) {
  const result = sandbox.sanitizeTelemetryPayload({ topic: dateStr });
  assert.strictEqual(result.topic, undefined, `FAIL: Date format ${dateStr} was not rejected by sanitizeTelemetryPayload`);
}
console.log('✔ PASS: Test 8b: Extended date rejection (DD-MM-YYYY, DD/MM/YYYY, DDMMYYYY, YYYYMMDD, YYYY-MM-DD, YYYY/MM/DD) verified');

const testPayload = {
  // Allowed keys
  event: 'purchase',
  page_path: '/pricing/',
  value: 199,
  currency: 'INR',
  transaction_id: 'ord_123',
  utm_source: 'google',
  // Disallowed arbitrary / personal keys (must be dropped by allowlist)
  driver: 7,
  conductor: 8,
  dob: '1990-05-15',
  custom_tag: 'vip',
  user_phone: '+91 9999999999',
  arbitrary_meta: { foo: 'bar' },
  // Allowed key with PII value (must be dropped by value sanitizer)
  plan_id: 'test@example.com',
  topic: '+91 9876543210'
};

const cleaned = sandbox.sanitizeTelemetryPayload(testPayload);

// Assert allowed keys are present
assert.strictEqual(cleaned.event, 'purchase');
assert.strictEqual(cleaned.page_path, '/pricing/');
assert.strictEqual(cleaned.value, 199);
assert.strictEqual(cleaned.currency, 'INR');
assert.strictEqual(cleaned.transaction_id, 'ord_123');
assert.strictEqual(cleaned.utm_source, 'google');

// Assert unallowed keys are dropped
assert.strictEqual(cleaned.driver, undefined);
assert.strictEqual(cleaned.conductor, undefined);
assert.strictEqual(cleaned.dob, undefined);
assert.strictEqual(cleaned.custom_tag, undefined);
assert.strictEqual(cleaned.user_phone, undefined);
assert.strictEqual(cleaned.arbitrary_meta, undefined);

// Assert values containing PII are dropped even if key was allowed
assert.strictEqual(cleaned.plan_id, undefined);
assert.strictEqual(cleaned.topic, undefined);

console.log('✔ PASS: Test 8: sanitizeTelemetryPayload strictly enforces ALLOWLIST and drops all unapproved keys & PII values');

console.log('--- ALL CDP CLEANUP & TELEMETRY ALLOWLIST AUDIT TESTS PASSED (100%) ---');
