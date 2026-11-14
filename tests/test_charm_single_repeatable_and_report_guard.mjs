/**
 * Verification Suite: Item 3 — charm_single Repeatable +5 Credits (Idempotent per Order ID)
 * & ALREADY_PURCHASED Scoped Strictly to PDF Reports per (user, subject, pack)
 */

import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { fileURLToPath } from 'node:url';
import worker from '../app/static/_worker.js';

const { isPdfReportPackId, mintUserSession, fulfillPaidOrder } = worker;
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

assert.equal(isPdfReportPackId('report_basic'), true);
assert.equal(isPdfReportPackId('report_advanced'), true);
assert.equal(isPdfReportPackId('report_premium'), true);
assert.equal(isPdfReportPackId('planner_2027'), true);
assert.equal(isPdfReportPackId('charm_single'), false);

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
  RAZORPAY_KEY_ID: 'rzp_test_repeatable123',
  RAZORPAY_KEY_SECRET: 'secret_test_repeatable123',
  RAZORPAY_WEBHOOK_SECRET: 'whsec_test_repeatable123'
};

const nowTs = Date.now();
const userId = 'usr_charm_repeat_1';
await d1.prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)').bind(userId, 'repeat@example.com', nowTs).run();
const sessionToken = await mintUserSession(env, userId, '127.0.0.1', nowTs);

let rzpCounter = 0;
const origFetch = globalThis.fetch;
globalThis.fetch = async (input, init) => {
  const urlStr = typeof input === 'string' ? input : input.url;
  if (urlStr.includes('api.razorpay.com/v1/orders')) {
    rzpCounter += 1;
    const reqBody = JSON.parse(init.body);
    return new Response(JSON.stringify({
      id: `order_rzp_seq_${rzpCounter}`,
      amount: reqBody.amount,
      currency: reqBody.currency || 'INR',
      status: 'created'
    }), { status: 200, headers: { 'Content-Type': 'application/json' } });
  }
  if (urlStr.includes('pdf-mock.internal')) {
    return new Response(new Uint8Array([37, 80, 68, 70]), { status: 200 });
  }
  return origFetch(input, init);
};

async function createOrderRequest(packId, dob, name = 'Repeat Buyer') {
  const req = new Request('https://preview.numeros-vision.pages.dev/api/v1/payments/create-order', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Origin': 'https://preview.numeros-vision.pages.dev',
      'Cookie': `__Host-nv_session=${sessionToken}`
    },
    body: JSON.stringify({
      pack_id: packId,
      name,
      dob,
      email: 'repeat@example.com'
    })
  });
  const res = await worker.fetch(req, env, { waitUntil: () => {} });
  const body = await res.json();
  return { status: res.status, body };
}

async function deliverWebhook(rzpOrderId, rzpPaymentId, amountPaise) {
  const webhookBody = JSON.stringify({
    event: 'order.paid',
    payload: {
      order: { entity: { id: rzpOrderId, amount_paid: amountPaise, status: 'paid' } },
      payment: {
        entity: {
          id: rzpPaymentId,
          order_id: rzpOrderId,
          amount: amountPaise,
          currency: 'INR',
          status: 'captured',
          method: 'upi'
        }
      }
    }
  });
  const sig = crypto.createHmac('sha256', env.RAZORPAY_WEBHOOK_SECRET).update(webhookBody).digest('hex');
  const req = new Request('https://preview.numeros-vision.pages.dev/api/v1/payments/webhook', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Razorpay-Signature': sig
    },
    body: webhookBody
  });
  const res = await worker.fetch(req, env, { waitUntil: () => {} });
  assert.equal(res.status, 200, 'Webhook must succeed with 200');
}

async function getCreditBalance() {
  const row = await d1.prepare('SELECT COALESCE(SUM(delta), 0) as bal FROM credit_ledger WHERE user_id = ?').bind(userId).first();
  return Number(row ? row.bal : 0);
}

try {
  // 1. First charm_single purchase (+5 credits) + idempotency on duplicate fulfillment
  const c1 = await createOrderRequest('charm_single', '1991-08-21');
  assert.equal(c1.status, 200, 'First charm_single create-order must return 200');
  assert.equal(c1.body.amount_paise, 19900);

  await deliverWebhook(c1.body.rzp_order_id, 'pay_charm_001', 19900);
  assert.equal(await getCreditBalance(), 5, 'First paid charm_single order must grant +5 credits');

  // Re-deliver webhook AND re-invoke fulfillPaidOrder for the SAME order_id -> still 5 credits
  await deliverWebhook(c1.body.rzp_order_id, 'pay_charm_001', 19900);
  const ord1Row = await d1.prepare('SELECT * FROM orders WHERE id = ?').bind(c1.body.order_id).first();
  await fulfillPaidOrder(ord1Row, 'pay_charm_001', 19900, 'upi', env, Date.now(), 'retry_test', null);
  assert.equal(await getCreditBalance(), 5, 'Duplicate fulfillment for same order_id must NOT double-credit');

  // 2. Second charm_single purchase for the EXACT SAME (user, subject/DOB) -> repeatable (+5 more = 10)
  const c2 = await createOrderRequest('charm_single', '1991-08-21');
  assert.equal(c2.status, 200, 'Second charm_single create-order for same user & DOB must succeed (repeatable)');
  assert.notEqual(c2.body.order_id, c1.body.order_id, 'Second charm_single must create a fresh order_id');

  await deliverWebhook(c2.body.rzp_order_id, 'pay_charm_002', 19900);
  assert.equal(await getCreditBalance(), 10, 'Second paid charm_single order must add +5 credits (total 10)');

  // Duplicate fulfillment on order #2 -> still 10
  const ord2Row = await d1.prepare('SELECT * FROM orders WHERE id = ?').bind(c2.body.order_id).first();
  await fulfillPaidOrder(ord2Row, 'pay_charm_002', 19900, 'upi', env, Date.now(), 'retry_test', null);
  assert.equal(await getCreditBalance(), 10, 'Duplicate fulfillment on second order_id must stay at 10 credits');

  const ledgerCount = await d1.prepare("SELECT COUNT(*) as cnt FROM credit_ledger WHERE user_id = ? AND reason = 'pack_purchase'").bind(userId).first();
  assert.equal(Number(ledgerCount.cnt), 2, 'Exactly 2 pack_purchase ledger rows must exist for 2 paid charm_single orders');

  // 3. PDF report (report_basic): ALREADY_PURCHASED blocks duplicate (user, subjectA, report_basic),
  //    while allowing (user, subjectB, report_basic) for a different DOB!
  const r1 = await createOrderRequest('report_basic', '1991-08-21');
  assert.equal(r1.status, 200, 'First report_basic for DOB A must return 200');
  await deliverWebhook(r1.body.rzp_order_id, 'pay_rep_001', 19900);

  const rDup = await createOrderRequest('report_basic', '1991-08-21');
  assert.equal(rDup.status, 409, 'Duplicate report_basic for same (user, DOB A, pack) must return 409');
  assert.equal(rDup.body.code, 'ALREADY_PURCHASED');

  const rOtherDob = await createOrderRequest('report_basic', '1994-11-03', 'Family Member');
  assert.equal(rOtherDob.status, 200, 'report_basic for same user + different DOB B must return 200');

  // 4. Even after buying report_basic, charm_single remains repeatable (+5 more = 15)!
  const c3 = await createOrderRequest('charm_single', '1991-08-21');
  assert.equal(c3.status, 200, 'Third charm_single create-order must still return 200');
  await deliverWebhook(c3.body.rzp_order_id, 'pay_charm_003', 19900);
  assert.equal(await getCreditBalance(), 15, 'Third paid charm_single order must bring total credits to 15');

  console.log('PASS: charm_single repeatable (+5 credits per paid order, idempotent per order_id) & ALREADY_PURCHASED scoped strictly to PDF reports per (user, subject, pack).');
} finally {
  globalThis.fetch = origFetch;
}
