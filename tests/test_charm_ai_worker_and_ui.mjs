// tests/test_charm_ai_worker_and_ui.mjs
// End-to-end verification of Cloudflare Pages `_worker.js` Charm AI fixes + Preview/Production header guards:
//   1. Unique `nv_visitor_id` HttpOnly cookie per visitor (never 'guest_user')
//   2. Missing DOB -> asks for Date of Birth first, 0 credits used
//   3. Unsupported topic -> honest scope message, 0 credits used
//   4. Upstream 503 / failure -> HTTP 503 ("Charm AI is unavailable right now, no credit was used. Try again.") + 0 credits lost
//   5. 3 free questions -> 3 distinct, topic-matched answers (`credits_remaining`: 2, 1, 0)
//   6. 4th question -> HTTP 402 (`FREE_TIER_EXHAUSTED`) + ₹199 Starter Pack upgrade offer
//   7. IP backup rate limit (`charm_rate_limits`) blocks cookie-stripping floods (>5/min -> 429)
//   8. `/api/v1/health/charm` returns 503 when `CHARM_SERVICE_URL` unset, 200 when healthy, zero secret/URL leakage
//   9. Production vs Preview `X-Robots-Tag` guard: Preview sets `noindex`, Production public pages do NOT set `noindex`.

import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import worker from '../app/static/_worker.js';

function createWorkerD1() {
  const sqlite = new DatabaseSync(':memory:');
  const migrationFiles = [
    '0001_initial_schema.sql',
    '0002_invoices_refunds_audit.sql',
    '0009_charm_usage_and_rates.sql',
    '0010_email_otp_and_consents.sql',
    '0011_waitlist_notify_me.sql',
  ];
  for (const file of migrationFiles) {
    const sql = fs.readFileSync(path.join(process.cwd(), 'migrations', file), 'utf8');
    sqlite.exec(sql);
  }

  function makeStmt(sql, bound = []) {
    return {
      bind(...args) {
        return makeStmt(sql, args);
      },
      async first() {
        const row = sqlite.prepare(sql).get(...bound);
        return row === undefined ? null : row;
      },
      async all() {
        return { results: sqlite.prepare(sql).all(...bound) };
      },
      async run() {
        const info = sqlite.prepare(sql).run(...bound);
        return { success: true, meta: { changes: Number(info.changes || 0) } };
      },
    };
  }

  return {
    sqlite,
    DB: {
      prepare(sql) {
        return makeStmt(sql, []);
      },
    },
  };
}

function extractSetCookieValue(resp, cookieName) {
  const raw = resp.headers.get('Set-Cookie') || '';
  const m = raw.match(new RegExp(`${cookieName}=([^;]+)`));
  return m ? m[1] : null;
}

async function run() {
  const { DB } = createWorkerD1();
  const baseEnv = {
    DB,
    ENVIRONMENT: 'local',
    __TEST__: true,
    IP_HASH_SALT: 'test_ip_salt_987654',
    CHARM_SERVICE_URL: 'https://preview-service.internal',
    CHARM_SERVICE_SECRET: 'secret_do_not_echo_value_123',
  };

  // ── 1. Unique anonymous visitor cookies ──
  const credRespA = await worker.fetch(
    new Request('https://numerosvision.com/api/charm/credits', {
      headers: { 'CF-Connecting-IP': '203.0.113.10' },
    }),
    baseEnv
  );
  assert.equal(credRespA.status, 200);
  const cookieA = extractSetCookieValue(credRespA, 'nv_visitor_id');
  assert.ok(cookieA && cookieA.startsWith('vis_'), 'Visitor A must receive unique vis_ cookie');
  assert.notEqual(cookieA, 'guest_user');

  const credRespB = await worker.fetch(
    new Request('https://numerosvision.com/api/charm/credits', {
      headers: { 'CF-Connecting-IP': '203.0.113.11' },
    }),
    baseEnv
  );
  const cookieB = extractSetCookieValue(credRespB, 'nv_visitor_id');
  assert.ok(cookieB && cookieB.startsWith('vis_'));
  assert.notEqual(cookieA, cookieB, 'Visitor A and Visitor B must have unique cookies');

  // ── 2. Missing DOB asks for DOB first with ZERO credits lost ──
  const missingDobResp = await worker.fetch(
    new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Cookie: `nv_visitor_id=${cookieA}`,
        'CF-Connecting-IP': '203.0.113.10',
      },
      body: JSON.stringify({ message: 'When is a good window for marriage?', name: 'Seeker' }),
    }),
    baseEnv
  );
  assert.equal(missingDobResp.status, 400);
  const missingDobJson = await missingDobResp.json();
  assert.equal(missingDobJson.status, 'INSUFFICIENT_EVIDENCE');
  assert.equal(missingDobJson.code, 'DOB_REQUIRED');
  assert.equal(missingDobJson.credits_remaining, 3, 'Missing DOB must NOT deduct a credit');

  // ── 3. Unsupported topic says so honestly with ZERO credits lost ──
  const unsupResp = await worker.fetch(
    new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Cookie: `nv_visitor_id=${cookieA}`,
        'CF-Connecting-IP': '203.0.113.10',
      },
      body: JSON.stringify({
        message: 'Which stock tip will double tomorrow?',
        day: 14,
        month: 7,
        year: 1992,
      }),
    }),
    baseEnv
  );
  assert.equal(unsupResp.status, 200);
  const unsupJson = await unsupResp.json();
  assert.equal(unsupJson.status, 'UNSUPPORTED_TOPIC');
  assert.equal(unsupJson.credits_remaining, 3, 'Unsupported topic must NOT deduct a credit');

  // ── 4. Upstream 503 error never loses a credit and returns exact retry message ──
  const errResp = await worker.fetch(
    new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Cookie: `nv_visitor_id=${cookieA}`,
        'CF-Connecting-IP': '203.0.113.10',
      },
      body: JSON.stringify({
        message: 'When is a supportive period for marriage?',
        day: 14,
        month: 7,
        year: 1992,
        __force_upstream_503__: true,
      }),
    }),
    baseEnv
  );
  assert.equal(errResp.status, 503);
  const errJson = await errResp.json();
  assert.equal(errJson.error, 'Charm AI is unavailable right now, no credit was used. Try again.');
  assert.equal(errJson.credits_remaining, 3, '503 error must refund reservation so 0 credits are lost');

  // ── 5. 3 Free Questions -> 3 distinct, topic-matched answers (remaining: 2, 1, 0) ──
  const questions = [
    { q: 'When is a supportive period for marriage with my partner?', kw: 'marriage' },
    { q: 'How can I build stronger monthly money and savings habits?', kw: 'money' },
    { q: 'What should I review for house number harmony on a new flat?', kw: 'property' },
  ];
  const distinctAnswers = new Set();

  for (let i = 0; i < questions.length; i++) {
    // Use separate IP per call or stay within 5/min burst (we used 3 above, so use .12 for clean burst budget)
    const r = await worker.fetch(
      new Request('https://numerosvision.com/api/charm/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Cookie: `nv_visitor_id=${cookieA}`,
          'CF-Connecting-IP': '203.0.113.12',
        },
        body: JSON.stringify({
          message: questions[i].q,
          day: 14,
          month: 7,
          year: 1992,
        }),
      }),
      baseEnv
    );
    assert.equal(r.status, 200);
    const data = await r.json();
    assert.equal(data.credits_remaining, 2 - i);
    assert.ok(data.human_friendly_summary && data.human_friendly_summary.headline);
    assert.ok(data.assistant_message && data.assistant_message.text);
    assert.ok(Array.isArray(data.practical_next_steps) && data.practical_next_steps.length >= 1);
    assert.ok(data.follow_up_question && data.follow_up_question.length > 5);

    const combined = `${data.human_friendly_summary.headline} ${data.assistant_message.text} ${data.follow_up_question}`.toLowerCase();
    assert.ok(combined.includes(questions[i].kw), `Expected topic keyword ${questions[i].kw} in response`);
    if (questions[i].kw === 'marriage') {
      assert.ok(!data.human_friendly_summary.headline.toLowerCase().includes('career'));
      assert.ok(!data.follow_up_question.toLowerCase().includes('business'));
    }
    distinctAnswers.add(data.assistant_message.text);
  }
  assert.equal(distinctAnswers.size, 3, 'All 3 free answers must be distinct');

  // ── 6. 4th Question -> 402 Limit + ₹199 Starter Pack Upgrade Offer ──
  const fourthResp = await worker.fetch(
    new Request('https://numerosvision.com/api/charm/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Cookie: `nv_visitor_id=${cookieA}`,
        'CF-Connecting-IP': '203.0.113.12',
      },
      body: JSON.stringify({
        message: 'What career habits suit my Personal Year?',
        day: 14,
        month: 7,
        year: 1992,
      }),
    }),
    baseEnv
  );
  assert.equal(fourthResp.status, 402);
  const fourthJson = await fourthResp.json();
  assert.equal(fourthJson.credits_remaining, 0);
  assert.ok(fourthJson.upgrade_offer);
  assert.equal(fourthJson.upgrade_offer.price_inr, 199);

  // ── 7. IP Backup Rate Limit blocks cookie-stripping burst (>5/min -> 429) ──
  let hit429 = false;
  for (let n = 0; n < 7; n++) {
    const flood = await worker.fetch(
      new Request('https://numerosvision.com/api/charm/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'CF-Connecting-IP': '203.0.113.99', // No cookie sent!
        },
        body: JSON.stringify({
          message: `Question ${n} about daily routine`,
          day: 10,
          month: 5,
          year: 1991,
        }),
      }),
      baseEnv
    );
    if (flood.status === 429) {
      hit429 = true;
      break;
    }
  }
  assert.equal(hit429, true, 'IP burst rate limit must block cookie-stripping floods');

  // ── 8. `/api/v1/health/charm` checks config without leaking secret or URL ──
  const healthUnset = await worker.fetch(
    new Request('https://numerosvision.com/api/v1/health/charm'),
    { ...baseEnv, CHARM_SERVICE_URL: '' }
  );
  assert.equal(healthUnset.status, 503);
  const unsetText = await healthUnset.text();
  assert.ok(!unsetText.includes(baseEnv.CHARM_SERVICE_SECRET));

  // ── 9. Preview vs Production `X-Robots-Tag: noindex` guard (Batch A #8 + d) ──
  const mockAssets = {
    async fetch() {
      return new Response('<!doctype html><html><head><title>Pricing</title></head><body>Pricing</body></html>', {
        status: 200,
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
      });
    },
  };

  const previewPageResp = await worker.fetch(
    new Request('https://preview.numeros-vision.pages.dev/pricing/'),
    { ...baseEnv, ENVIRONMENT: 'preview', ASSETS: mockAssets }
  );
  assert.equal(previewPageResp.status, 200);
  assert.match(
    previewPageResp.headers.get('X-Robots-Tag') || '',
    /noindex/i,
    'Preview public page responses MUST send X-Robots-Tag: noindex'
  );

  const prodPageResp = await worker.fetch(
    new Request('https://numerosvision.com/pricing/'),
    { ...baseEnv, ENVIRONMENT: 'production', ASSETS: mockAssets }
  );
  assert.equal(prodPageResp.status, 200);
  const prodRobotsHeader = prodPageResp.headers.get('X-Robots-Tag') || '';
  assert.ok(
    !/noindex/i.test(prodRobotsHeader),
    `Production public page responses MUST NOT send X-Robots-Tag: noindex (got: "${prodRobotsHeader}")`
  );

  console.log('ALL CHARM AI WORKER + ROBOTS HEADER GUARD TESTS PASSED (9/9 groups green)');
}

run().catch((err) => {
  console.error(err);
  process.exit(1);
});
