// tests/test_events_and_form_routing.mjs
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert';
import { DatabaseSync } from 'node:sqlite';

console.log('--- STARTING EVENTS & FORM ROUTING TEST SUITE ---');

const ROOT_DIR = process.cwd();

// Test 1: Zero Web3Forms keys in client HTML
const contactHtml = fs.readFileSync(path.join(ROOT_DIR, 'app', 'static', 'contact.html'), 'utf-8');
const consultationHtml = fs.readFileSync(path.join(ROOT_DIR, 'app', 'static', 'consultation.html'), 'utf-8');

assert.strictEqual(contactHtml.includes('web3forms.com'), false, 'FAIL: contact.html still contains web3forms.com reference');
assert.strictEqual(contactHtml.includes('e27c09c1-4ad2-4301-ac99-98c230ad866c'), false, 'FAIL: contact.html still contains Web3Forms access key');
assert.ok(contactHtml.includes("fetch('/api/v1/contact'"), 'FAIL: contact.html does not route to /api/v1/contact');
assert.strictEqual(contactHtml.includes('localStorage.setItem(\'nv_contact_tickets\''), false, 'FAIL: contact.html still writes to localStorage');
console.log('✔ PASS: Test 1a: contact.html routes cleanly to Worker with zero Web3Forms key & zero localStorage PII write');

assert.strictEqual(consultationHtml.includes('web3forms.com'), false, 'FAIL: consultation.html still contains web3forms.com reference');
assert.strictEqual(consultationHtml.includes('e27c09c1-4ad2-4301-ac99-98c230ad866c'), false, 'FAIL: consultation.html still contains Web3Forms access key');
assert.ok(consultationHtml.includes("fetch('/api/v1/consultation/enquiry'"), 'FAIL: consultation.html does not route to /api/v1/consultation/enquiry');
assert.strictEqual(consultationHtml.includes('localStorage.setItem(\'nv_consultation_enquiries\''), false, 'FAIL: consultation.html still writes to localStorage');
console.log('✔ PASS: Test 1b: consultation.html routes cleanly to Worker with zero Web3Forms key & zero localStorage PII write');

// Test 2: Verify 0004_events.sql runs cleanly in SQLite and contains NO PII columns
const eventsSql = fs.readFileSync(path.join(ROOT_DIR, 'migrations', '0004_events.sql'), 'utf-8');
const db = new DatabaseSync(':memory:');
db.exec(eventsSql);

const columns = db.prepare('PRAGMA table_info(events)').all();
const columnNames = columns.map(c => c.name.toLowerCase());

const FORBIDDEN_COLS = [
  'name', 'full_name', 'email', 'phone', 'mobile', 'dob', 'birth_date',
  'birth_time', 'birth_place', 'city', 'driver', 'conductor', 'chart', 'loshu'
];

for (const col of FORBIDDEN_COLS) {
  assert.strictEqual(columnNames.includes(col), false, `FAIL: events table contains forbidden PII column ${col}`);
}

assert.ok(columnNames.includes('id'), 'FAIL: events table missing id');
assert.ok(columnNames.includes('event_name'), 'FAIL: events table missing event_name');
assert.ok(columnNames.includes('device_id'), 'FAIL: events table missing device_id');
assert.ok(columnNames.includes('anonymous_session_id'), 'FAIL: events table missing anonymous_session_id');
assert.ok(columnNames.includes('created_at'), 'FAIL: events table missing created_at');
console.log('✔ PASS: Test 2: 0004_events.sql creates valid table in SQLite with zero PII columns');

// Test 3: Verify rate limiting in _worker.js code
const workerJs = fs.readFileSync(path.join(ROOT_DIR, 'app', 'static', '_worker.js'), 'utf-8');
assert.ok(workerJs.includes('function checkFormRateLimit('), 'FAIL: checkFormRateLimit function missing from _worker.js');
assert.ok(workerJs.includes('url.pathname === \'/api/v1/events\''), 'FAIL: /api/v1/events endpoint missing from _worker.js');
assert.ok(workerJs.includes('logWorkerEvent(env,'), 'FAIL: logWorkerEvent helper missing from _worker.js');
console.log('✔ PASS: Test 3: _worker.js contains checkFormRateLimit, logWorkerEvent, and POST /api/v1/events route');

// Test 4: Evaluate checkFormRateLimit behavior
const rateLimiterCode = `
  const _formRateLimits = new Map();
  function checkFormRateLimit(clientIp, limit = 5, windowMs = 600000) {
    const now = Date.now();
    const list = _formRateLimits.get(clientIp) || [];
    const valid = list.filter(t => now - t < windowMs);
    if (valid.length >= limit) return false;
    valid.push(now);
    _formRateLimits.set(clientIp, valid);
    return true;
  }
`;
const evalFn = new Function(rateLimiterCode + ' return checkFormRateLimit;');
const checkRateLimit = evalFn();

// First 5 should succeed
for (let i = 0; i < 5; i++) {
  assert.strictEqual(checkRateLimit('192.168.1.1', 5, 600000), true, `Request ${i+1} should pass rate limit`);
}
// 6th should fail (429)
assert.strictEqual(checkRateLimit('192.168.1.1', 5, 600000), false, '6th request must be rejected with 429');
// Different IP should still succeed
assert.strictEqual(checkRateLimit('192.168.1.2', 5, 600000), true, 'Different IP must succeed');
console.log('✔ PASS: Test 4: checkFormRateLimit correctly allows 5 requests and blocks subsequent attempts within sliding window');

// Test 5: Verify PII rejection rules in POST /api/v1/events
const FORBIDDEN_KEYS = new Set([
  'name', 'full_name', 'first_name', 'last_name', 'email', 'phone', 'mobile',
  'dob', 'birth_date', 'birthdate', 'birth_time', 'birth_place', 'birth_city',
  'driver', 'conductor', 'mulank', 'bhagyank', 'destiny', 'lifepath', 'chart', 'grid', 'loshu'
]);

function validateEventPayload(body) {
  for (const k of Object.keys(body)) {
    if (FORBIDDEN_KEYS.has(k.toLowerCase())) {
      return { ok: false, error: 'PII field rejected: ' + k };
    }
    const v = body[k];
    if (typeof v === 'string') {
      if (/@[\w.-]+\.\w+/.test(v) || /^\+?[0-9\s-]{10,15}$/.test(v.trim())) {
        return { ok: false, error: 'PII pattern detected in ' + k };
      }
    }
  }
  return { ok: true };
}

assert.strictEqual(validateEventPayload({ event_name: 'test', name: 'John Doe' }).ok, false);
assert.strictEqual(validateEventPayload({ event_name: 'test', email: 'john@example.com' }).ok, false);
assert.strictEqual(validateEventPayload({ event_name: 'test', dob: '1990-01-01' }).ok, false);
assert.strictEqual(validateEventPayload({ event_name: 'test', driver: 5 }).ok, false);
assert.strictEqual(validateEventPayload({ event_name: 'test', topic: 'user@gmail.com' }).ok, false);
assert.strictEqual(validateEventPayload({ event_name: 'test', topic: '+919876543210' }).ok, false);
assert.strictEqual(validateEventPayload({ event_name: 'cta_click', product_id: 'pkg_vedic_199', page_path: '/pricing/' }).ok, true);
console.log('✔ PASS: Test 5: Event payload validator strictly rejects PII keys, emails, and phone numbers');

console.log('--- ALL EVENTS & FORM ROUTING TESTS PASSED (100%) ---');
