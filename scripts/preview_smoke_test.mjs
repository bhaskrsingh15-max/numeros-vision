/**
 * NUMEROS VISION — 2027 YEAR AHEAD PLANNER PREVIEW SMOKE TEST RUNNER
 * =================================================================
 * Exercises live preview endpoints:
 * 1. GET /api/planner-2027/price (server authority ₹1,499)
 * 2. Mandatory DPDP consent gate
 * 3. POST /api/planner-2027/order (order initiation)
 * 4. POST /api/planner-2027/resend-link (browserless delivery)
 * 5. GET /api/planner-2027/admin/stuck-orders (authenticated admin monitor)
 * 6. Public asset isolation (ensures private files return HTTP 404)
 */

import https from 'node:https';
import http from 'node:http';

const args = process.argv.slice(2);
let baseUrl = 'http://localhost:8788';
let adminToken = 'test_admin_token_2027';

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--url' && args[i + 1]) {
    baseUrl = args[i + 1].replace(/\/+$/, '');
    i++;
  } else if (args[i] === '--admin-token' && args[i + 1]) {
    adminToken = args[i + 1];
    i++;
  }
}

console.log(`[SMOKE] Running Preview Smoke Test against: ${baseUrl}`);

async function request(path, options = {}) {
  const url = new URL(path, baseUrl);
  const client = url.protocol === 'https:' ? https : http;

  return new Promise((resolve, reject) => {
    const req = client.request(url, options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        let json = null;
        try { json = JSON.parse(data); } catch (_) {}
        resolve({ status: res.statusCode, headers: res.headers, body: data, json });
      });
    });

    req.on('error', reject);
    if (options.body) {
      req.write(typeof options.body === 'string' ? options.body : JSON.stringify(options.body));
    }
    req.end();
  });
}

async function run() {
  let passed = 0;
  let failed = 0;

  function assert(condition, message) {
    if (condition) {
      console.log(`  ✓ ${message}`);
      passed++;
    } else {
      console.error(`  ✗ FAIL: ${message}`);
      failed++;
    }
  }

  // 1. Pricing Authority
  console.log('\n[1/6] Testing Pricing Authority (/api/planner-2027/price)...');
  const priceRes = await request('/api/planner-2027/price');
  assert(priceRes.status === 200, `Price endpoint returned ${priceRes.status}`);
  assert(priceRes.json?.amount_paise === 149900, `Amount is ₹1,499 (149900 paise)`);
  assert(priceRes.json?.currency === 'INR', `Currency is INR`);

  // 2. Mandatory Consent
  console.log('\n[2/6] Testing Mandatory DPDP Consent Gate...');
  const noConsentRes = await request('/api/planner-2027/order', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: { name: 'Arun Sharma', dob: '1980-01-01', email: 'arun@example.com', consent: false }
  });
  assert(noConsentRes.status === 400, `Rejected order without consent (HTTP ${noConsentRes.status})`);

  // 3. Order Creation
  console.log('\n[3/6] Testing Order Creation (/api/planner-2027/order)...');
  const orderRes = await request('/api/planner-2027/order', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: { name: 'Arun Sharma', dob: '1980-01-01', email: 'arun@example.com', consent: true }
  });
  assert(orderRes.status === 200, `Order created successfully (HTTP ${orderRes.status})`);
  assert(orderRes.json?.order_id?.startsWith('ord_p27_'), `Order ID generated: ${orderRes.json?.order_id}`);
  assert(orderRes.json?.amount_paise === 149900, `Enforced server price: 149900`);

  // 4. Browserless Recovery
  console.log('\n[4/6] Testing Browserless Link Recovery (/api/planner-2027/resend-link)...');
  const mismatchRes = await request('/api/planner-2027/resend-link', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: { order_id: orderRes.json?.order_id, email: 'wrong@example.com' }
  });
  assert(mismatchRes.status === 404, `Mismatched email returned 404 (zero PII disclosure)`);

  // 5. Admin Stuck Orders Monitor
  console.log('\n[5/6] Testing Admin Stuck Orders Monitor (/api/planner-2027/admin/stuck-orders)...');
  const unauthAdmin = await request('/api/planner-2027/admin/stuck-orders');
  assert(unauthAdmin.status === 401, `Unauthenticated admin query rejected (HTTP ${unauthAdmin.status})`);

  const authAdmin = await request('/api/planner-2027/admin/stuck-orders', {
    headers: { 'Authorization': `Bearer ${adminToken}` }
  });
  assert(authAdmin.status === 200, `Authenticated admin query succeeded (HTTP ${authAdmin.status})`);
  assert(typeof authAdmin.json?.stuck_orders_count === 'number', `Reported stuck orders count: ${authAdmin.json?.stuck_orders_count}`);

  // 6. Public Asset Isolation
  console.log('\n[6/6] Testing Public Asset Isolation...');
  const blockedPaths = [
    '/data/panchang_2027_delhi.json',
    '/planner_2027_engine.py',
    '/pdf_service/',
    '/_worker.js'
  ];
  for (const bp of blockedPaths) {
    const bRes = await request(bp);
    assert(bRes.status === 404, `Path ${bp} blocked (HTTP ${bRes.status})`);
  }

  console.log(`\n========================================`);
  console.log(`Preview Smoke Test Summary: ${passed} passed, ${failed} failed`);
  console.log(`========================================\n`);

  if (failed > 0) {
    process.exit(1);
  }
}

// In local test environments without a running server, this script can be invoked with a live preview URL
if (process.argv[1].endsWith('preview_smoke_test.mjs') && (args.includes('--url') || process.env.RUN_SMOKE === '1')) {
  run().catch((err) => {
    console.error('Smoke test failed with error:', err);
    process.exit(1);
  });
} else {
  console.log('Smoke test kit loaded. Run with --url https://<preview-domain> to execute against live preview.');
}
