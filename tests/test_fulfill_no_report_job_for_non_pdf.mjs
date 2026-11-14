/**
 * Verification Suite: Item 4 — fulfillPaidOrder Creates Zero report_jobs Rows for Non-PDF Packs
 */

import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { fileURLToPath } from 'node:url';
import worker from '../app/static/_worker.js';

const { mintUserSession, fulfillPaidOrder } = worker;
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');

function createRealSqliteD1() {
  const sqlite = new DatabaseSync(':memory:');
  const migDir = path.join(repoRoot, 'migrations');
  for (const mf of fs.readdirSync(migDir).filter((f) => f.endsWith('.sql')).sort()) {
    sqlite.exec(fs.readFileSync(path.join(migDir, mf), 'utf8'));
  }
  return {
    _sqlite: sqlite,
    prepare(sql) {
      const makeBound = (params = []) => ({
        bind(...nextParams) {
          return makeBound(nextParams);
        },
        async first() {
          const stmt = sqlite.prepare(sql);
          return stmt.get(...params) ?? null;
        },
        async all() {
          const stmt = sqlite.prepare(sql);
          return { results: stmt.all(...params) };
        },
        async run() {
          const stmt = sqlite.prepare(sql);
          const info = stmt.run(...params);
          return { success: true, meta: { changes: info.changes } };
        }
      });
      return makeBound([]);
    }
  };
}

const d1 = createRealSqliteD1();
const env = {
  ENVIRONMENT: 'preview',
  NV_FORCE_LAUNCH_MODE: 'true',
  DB: d1,
  REPORTS_BUCKET: { put: async () => {}, get: async () => null },
  OTP_HMAC_SECRET: 'a'.repeat(64),
  SESSION_SECRET: 'b'.repeat(64),
  IP_HASH_SALT: 'c'.repeat(64),
  DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
  PDF_SERVICE_SECRET: 'd'.repeat(64),
  PDF_SERVICE_URL: 'https://pdf-mock.internal',
  DOWNLOAD_TOKEN_SECRET: 'e'.repeat(64),
  ADMIN_TOKEN: 'admin_test_token_item4_long_secret_value',
  RAZORPAY_KEY_ID: 'rzp_test_nojob123',
  RAZORPAY_KEY_SECRET: 'secret_test_nojob123',
  RAZORPAY_WEBHOOK_SECRET: 'whsec_test_nojob123'
};

const nowTs = Date.now();
const userId = 'usr_nojob_1';
await d1.prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)').bind(userId, 'nojob@example.com', nowTs).run();
const sessionToken = await mintUserSession(env, userId, '127.0.0.1', nowTs);

let rzpSeq = 0;
let pdfCalls = 0;
const origFetch = globalThis.fetch;
globalThis.fetch = async (input, init) => {
  const urlStr = typeof input === 'string' ? input : input.url;
  if (urlStr.includes('api.razorpay.com/v1/orders')) {
    rzpSeq += 1;
    const reqBody = JSON.parse(init.body);
    return new Response(JSON.stringify({
      id: `order_rzp_nojob_${rzpSeq}`,
      amount: reqBody.amount,
      currency: 'INR',
      status: 'created'
    }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  }
  if (urlStr.includes('pdf-mock.internal')) {
    pdfCalls += 1;
    return new Response(new Uint8Array([37, 80, 68, 70]), { status: 200 });
  }
  return origFetch(input, init);
};

try {
  // 1. Create and fulfill charm_single via webhook + status poll + dashboard view + direct fulfillPaidOrder retry
  const createCharmRes = await worker.fetch(new Request('https://preview.numeros-vision.pages.dev/api/v1/payments/create-order', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Origin': 'https://preview.numeros-vision.pages.dev',
      'Cookie': `__Host-nv_session=${sessionToken}`
    },
    body: JSON.stringify({
      pack_id: 'charm_single',
      name: 'Credit Only Buyer',
      dob: '1992-04-12',
      email: 'nojob@example.com'
    })
  }), env, { waitUntil: () => {} });
  assert.equal(createCharmRes.status, 200);
  const charmOrder = await createCharmRes.json();

  const whPayload = JSON.stringify({
    event: 'order.paid',
    payload: {
      order: { entity: { id: charmOrder.rzp_order_id, amount_paid: 19900, status: 'paid' } },
      payment: {
        entity: {
          id: 'pay_nojob_001',
          order_id: charmOrder.rzp_order_id,
          amount: 19900,
          currency: 'INR',
          status: 'captured',
          method: 'upi'
        }
      }
    }
  });
  const whSig = crypto.createHmac('sha256', env.RAZORPAY_WEBHOOK_SECRET).update(whPayload).digest('hex');
  const whRes = await worker.fetch(new Request('https://preview.numeros-vision.pages.dev/api/v1/payments/webhook', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': whSig },
    body: whPayload
  }), env, { waitUntil: () => {} });
  assert.equal(whRes.status, 200);
  const whBody = await whRes.json();
  assert.equal(whBody.jobId, null, 'Webhook response for charm_single must report jobId: null');

  // Re-run fulfillPaidOrder directly + hit /api/v1/payments/status + hit /api/v1/dashboard/view
  const ordRow = await d1.prepare('SELECT * FROM orders WHERE id = ?').bind(charmOrder.order_id).first();
  const directRes = await fulfillPaidOrder(ordRow, 'pay_nojob_001', 19900, 'upi', env, Date.now(), 'direct_check', null);
  assert.equal(directRes.jobId, null, 'fulfillPaidOrder must return jobId: null for charm_single');

  const statusRes = await worker.fetch(new Request(`https://preview.numeros-vision.pages.dev/api/v1/payments/status?order_id=${encodeURIComponent(charmOrder.order_id)}`, {
    method: 'GET',
    headers: { 'Cookie': `__Host-nv_session=${sessionToken}` }
  }), env, { waitUntil: () => {} });
  assert.equal(statusRes.status, 200);
  const statusBody = await statusRes.json();
  assert.equal(statusBody.status, 'paid');
  assert.equal(statusBody.jobId, null);
  assert.equal(statusBody.reportStatus, 'credits_granted');

  const dashRes = await worker.fetch(new Request('https://preview.numeros-vision.pages.dev/api/v1/dashboard/view', {
    method: 'GET',
    headers: { 'Cookie': `__Host-nv_session=${sessionToken}` }
  }), env, { waitUntil: () => {} });
  assert.equal(dashRes.status, 200);

  const jobsAfterCharm = await d1.prepare('SELECT COUNT(*) as cnt FROM report_jobs').first();
  assert.equal(Number(jobsAfterCharm.cnt), 0, 'ZERO report_jobs rows must exist after fulfilling charm_single');
  assert.equal(pdfCalls, 0, 'ZERO PDF service calls must occur for charm_single');

  const adminRes = await worker.fetch(new Request('https://preview.numeros-vision.pages.dev/api/admin/test-console?format=json', {
    method: 'GET',
    headers: { 'X-Admin-Token': env.ADMIN_TOKEN, 'Accept': 'application/json' }
  }), env, { waitUntil: () => {} });
  assert.equal(adminRes.status, 200);
  const adminBody = await adminRes.json();
  assert.equal(adminBody.paid_unfulfilled_orders.length, 0, 'Fulfilled charm_single order must NOT appear in paid_unfulfilled_orders');

  // 2. Contrast check: fulfilling report_basic DOES create exactly 1 report_jobs row
  const createBasicRes = await worker.fetch(new Request('https://preview.numeros-vision.pages.dev/api/v1/payments/create-order', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Origin': 'https://preview.numeros-vision.pages.dev',
      'Cookie': `__Host-nv_session=${sessionToken}`
    },
    body: JSON.stringify({
      pack_id: 'report_basic',
      name: 'Credit Only Buyer',
      dob: '1992-04-12',
      email: 'nojob@example.com'
    })
  }), env, { waitUntil: () => {} });
  assert.equal(createBasicRes.status, 200);
  const basicOrder = await createBasicRes.json();
  const basicOrdRow = await d1.prepare('SELECT * FROM orders WHERE id = ?').bind(basicOrder.order_id).first();
  const basicFulfillRes = await fulfillPaidOrder(basicOrdRow, 'pay_basic_001', 19900, 'upi', env, Date.now(), 'direct_check', null);
  assert.ok(basicFulfillRes.jobId && basicFulfillRes.jobId.startsWith('job_'), 'PDF pack report_basic must create a report_jobs row');

  const jobsAfterBasic = await d1.prepare('SELECT COUNT(*) as cnt FROM report_jobs').first();
  assert.equal(Number(jobsAfterBasic.cnt), 1, 'Exactly 1 report_jobs row must exist (for report_basic only)');

  console.log('PASS: fulfillPaidOrder creates ZERO report_jobs rows for non-PDF packs (charm_single) and 1 row for PDF packs.');
} finally {
  globalThis.fetch = origFetch;
}
