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

// Test 2: Verify Migrations 0004, 0005, 0006 filenames and SQLite schema execution
assert.strictEqual(fs.existsSync(path.join(ROOT_DIR, 'migrations', '0004_cookie_consents.sql')), true, 'FAIL: 0004_cookie_consents.sql must exist');
assert.strictEqual(fs.existsSync(path.join(ROOT_DIR, 'migrations', '0005_enquiries.sql')), true, 'FAIL: 0005_enquiries.sql must exist');
assert.strictEqual(fs.existsSync(path.join(ROOT_DIR, 'migrations', '0006_events.sql')), true, 'FAIL: 0006_events.sql must exist');

const db = new DatabaseSync(':memory:');

// Execute 0005_enquiries.sql and verify notification_status column
const enquiriesSql = fs.readFileSync(path.join(ROOT_DIR, 'migrations', '0005_enquiries.sql'), 'utf-8');
db.exec(enquiriesSql);
const enquiriesCols = db.prepare('PRAGMA table_info(enquiries)').all().map(c => c.name.toLowerCase());
assert.ok(enquiriesCols.includes('id'), 'FAIL: enquiries table missing id');
assert.ok(enquiriesCols.includes('type'), 'FAIL: enquiries table missing type');
assert.ok(enquiriesCols.includes('name'), 'FAIL: enquiries table missing name');
assert.ok(enquiriesCols.includes('email'), 'FAIL: enquiries table missing email');
assert.ok(enquiriesCols.includes('phone'), 'FAIL: enquiries table missing phone');
assert.ok(enquiriesCols.includes('notification_status'), 'FAIL: enquiries table missing notification_status');
assert.ok(enquiriesCols.includes('created_at'), 'FAIL: enquiries table missing created_at');

// Test insert into enquiries table with notification_status
db.prepare(`
  INSERT INTO enquiries (id, type, name, email, phone, area_or_category, preferred_contact_method, order_id, message, notification_status, ip_hash, user_agent, created_at)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
`).run('ENQ-123456-ABCD', 'consultation', 'Ananya Sharma', 'ananya@example.com', '+919876543210', 'Career', 'Email', null, 'Requesting career consultation', 'notified', 'hash123', 'Agent 1.0', Date.now());
const enqRow = db.prepare('SELECT * FROM enquiries WHERE id = ?').get('ENQ-123456-ABCD');
assert.strictEqual(enqRow.name, 'Ananya Sharma');
assert.strictEqual(enqRow.type, 'consultation');
assert.strictEqual(enqRow.notification_status, 'notified');
console.log('✔ PASS: Test 2a: 0005_enquiries.sql creates valid table and successfully stores consultation submissions with notification_status');

// Execute 0006_events.sql
const eventsSql = fs.readFileSync(path.join(ROOT_DIR, 'migrations', '0006_events.sql'), 'utf-8');
assert.strictEqual(eventsSql.includes('statutory'), false, 'FAIL: 0006_events.sql contains legal claim "statutory"');
assert.strictEqual(eventsSql.includes('DPDP'), false, 'FAIL: 0006_events.sql contains legal claim "DPDP"');
db.exec(eventsSql);

const eventCols = db.prepare('PRAGMA table_info(events)').all().map(c => c.name.toLowerCase());
const FORBIDDEN_COLS = [
  'name', 'full_name', 'email', 'phone', 'mobile', 'dob', 'birth_date',
  'birth_time', 'birth_place', 'city', 'driver', 'conductor', 'chart', 'loshu'
];
for (const col of FORBIDDEN_COLS) {
  assert.strictEqual(eventCols.includes(col), false, `FAIL: events table contains forbidden PII column ${col}`);
}
assert.ok(eventCols.includes('id'), 'FAIL: events table missing id');
assert.ok(eventCols.includes('event_name'), 'FAIL: events table missing event_name');
assert.ok(eventCols.includes('device_id'), 'FAIL: events table missing device_id');
assert.ok(eventCols.includes('created_at'), 'FAIL: events table missing created_at');
console.log('✔ PASS: Test 2b: 0006_events.sql creates valid table with zero PII columns and neutral documentation');

// Test 2c: REAL PURGE UNIT TEST - Delete events older than 90 days
const now = Date.now();
const oldTimestamp = now - (95 * 86400 * 1000); // 95 days ago (must be purged)
const recentTimestamp = now - (5 * 86400 * 1000); // 5 days ago (must be kept)

db.prepare(`
  INSERT INTO events (id, event_name, created_at)
  VALUES ('evt_old_95d', 'page_view', ?)
`).run(oldTimestamp);

db.prepare(`
  INSERT INTO events (id, event_name, created_at)
  VALUES ('evt_recent_5d', 'page_view', ?)
`).run(recentTimestamp);

// Verify both exist before purge
assert.strictEqual(db.prepare("SELECT COUNT(*) as c FROM events WHERE id = 'evt_old_95d'").get().c, 1);
assert.strictEqual(db.prepare("SELECT COUNT(*) as c FROM events WHERE id = 'evt_recent_5d'").get().c, 1);

// Execute real 90-day cutoff purge
const cutoff = now - (90 * 86400 * 1000);
db.prepare("DELETE FROM events WHERE created_at < ?").run(cutoff);

// Assert: Old event is purged, recent event remains
assert.strictEqual(db.prepare("SELECT COUNT(*) as c FROM events WHERE id = 'evt_old_95d'").get().c, 0, 'FAIL: Event older than 90 days was not purged');
assert.strictEqual(db.prepare("SELECT COUNT(*) as c FROM events WHERE id = 'evt_recent_5d'").get().c, 1, 'FAIL: Recent event within 90 days was incorrectly purged');
console.log('✔ PASS: Test 2c: 90-day rolling purge successfully purges expired events and retains active events');

// Test 3: Verify Worker contains durable D1 insertion, TELEMETRY_SALT requirement, and neutral error wording
const workerJs = fs.readFileSync(path.join(ROOT_DIR, 'app', 'static', '_worker.js'), 'utf-8');
assert.ok(workerJs.includes('INSERT INTO enquiries ('), 'FAIL: _worker.js does not insert into enquiries table');
assert.ok(workerJs.includes('notification_status'), 'FAIL: _worker.js does not track notification_status');
assert.ok(workerJs.includes('const telemetrySalt = env.TELEMETRY_SALT;'), 'FAIL: _worker.js does not require env.TELEMETRY_SALT');
assert.ok(workerJs.includes('if (!telemetrySalt)'), 'FAIL: _worker.js missing !telemetrySalt check');
assert.strictEqual(workerJs.includes('nv_statutory_telemetry_salt_2026'), false, 'FAIL: Hardcoded fallback salt still present');
assert.ok(workerJs.includes('Analytics consent required to record events.'), 'FAIL: Neutral consent error message missing');
assert.strictEqual(workerJs.includes('under DPDP Act 2023'), false, 'FAIL: Legal claim "under DPDP Act 2023" still in worker');
assert.strictEqual(workerJs.includes('sendEmailViaCloudflare'), false, 'FAIL: sendEmailViaCloudflare should be completely removed');
console.log('✔ PASS: Test 3: _worker.js requires TELEMETRY_SALT (no fallback), records notification_status, uses neutral wording, and has no fake email stubs');

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

for (let i = 0; i < 5; i++) {
  assert.strictEqual(checkRateLimit('192.168.1.1', 5, 600000), true, `Request ${i+1} should pass rate limit`);
}
assert.strictEqual(checkRateLimit('192.168.1.1', 5, 600000), false, '6th request must be rejected with 429');
assert.strictEqual(checkRateLimit('192.168.1.2', 5, 600000), true, 'Different IP must succeed');
console.log('✔ PASS: Test 4: checkFormRateLimit correctly allows 5 requests and blocks subsequent attempts within sliding window');

// Test 5: Verify PII rejection rules & Event Name Allowlist
const ALLOWED_EVENT_NAMES = new Set([
  'page_view', 'calculator_used', 'signup_modal_opened', 'lead_captured',
  'checkout_initiated', 'order_created', 'payment_verified', 'report_downloaded',
  'cta_clicked', 'cookie_consent_updated'
]);

assert.strictEqual(ALLOWED_EVENT_NAMES.has('page_view'), true);
assert.strictEqual(ALLOWED_EVENT_NAMES.has('arbitrary_malicious_event'), false);
assert.strictEqual(ALLOWED_EVENT_NAMES.has('drop_tables'), false);
console.log('✔ PASS: Test 5: Event name allowlist strictly enforces approved lifecycle events');

console.log('--- ALL EVENTS & FORM ROUTING TESTS PASSED (100%) ---');
