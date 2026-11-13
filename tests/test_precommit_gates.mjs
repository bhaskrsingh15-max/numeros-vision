/**
 * Pre-Commit Gates Verification Suite (Items 1, 2, 3, 5)
 * ======================================================
 * 1. Price parity: resolveEffectivePackPricePaise + POST /api/v1/payments/create-order
 *    equal app/config/packs.json for EVERY plan id in both launch and regular modes.
 * 2. Service Worker behaviour (not text match): executes app/static/sw.js and
 *    dist_cloudflare_pages/sw.js in a real VM ServiceWorker runtime and proves
 *    /dashboard* and /api/* (unauthenticated and authenticated) never touch CacheStorage.
 * 3. wrangler.toml vars: Preview forces launch mode without dates; Production has NO
 *    launch window set (empty launch fields) and rejects NV_FORCE_LAUNCH_MODE.
 * 5. Real-time SSE stage streaming: /api/charm/chat/stream flushes stage events as each
 *    step starts/completes (before Write finishes), never on a post-hoc timer.
 */

import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { DatabaseSync } from 'node:sqlite';
import { fileURLToPath } from 'node:url';

import worker from '../app/static/_worker.js';
const {
  resolveEffectivePackPricePaise,
  resolveServerLaunchOfferState,
  getPackById,
  mintUserSession,
  memoryStore
} = worker;

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');
const packsJson = JSON.parse(fs.readFileSync(path.join(repoRoot, 'app/config/packs.json'), 'utf8'));

function parseSimpleTomlSections(tomlText) {
  const sections = {};
  let current = '__root__';
  sections[current] = {};
  for (const rawLine of tomlText.split(/\r?\n/)) {
    const line = rawLine.trim();
    if (!line || line.startsWith('#')) continue;
    if (line.startsWith('[[') && line.endsWith(']]')) {
      current = line.slice(2, -2).trim() + '__array';
      sections[current] = sections[current] || {};
      continue;
    }
    if (line.startsWith('[') && line.endsWith(']')) {
      current = line.slice(1, -1).trim();
      sections[current] = sections[current] || {};
      continue;
    }
    const eqIdx = line.indexOf('=');
    if (eqIdx > 0) {
      const k = line.slice(0, eqIdx).trim();
      let v = line.slice(eqIdx + 1).trim();
      if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'"))) {
        v = v.slice(1, -1);
      }
      sections[current][k] = v;
    }
  }
  return sections;
}

function collectAllPlansFromPacksJson() {
  const buckets = ['core_reports', 'annual_planners', 'charm_ai', 'bundles'];
  const all = [];
  for (const bucket of buckets) {
    const group = packsJson[bucket] || {};
    for (const [id, entry] of Object.entries(group)) {
      all.push({ bucket, id, entry });
    }
  }
  return all;
}

async function testGate3WranglerVars() {
  const tomlRaw = fs.readFileSync(path.join(repoRoot, 'wrangler.toml'), 'utf8');
  const parsed = parseSimpleTomlSections(tomlRaw);
  const prodVars = parsed['vars'] || {};
  const previewVars = parsed['env.preview.vars'] || {};

  assert.equal(prodVars.ENVIRONMENT, 'production');
  assert.equal(prodVars.NV_LAUNCH_STARTS_AT || '', '', 'Production NV_LAUNCH_STARTS_AT must be empty');
  assert.equal(prodVars.NV_LAUNCH_ENDS_AT || '', '', 'Production NV_LAUNCH_ENDS_AT must be empty');
  assert.equal(prodVars.NV_FORCE_LAUNCH_MODE, undefined, 'Production must not set NV_FORCE_LAUNCH_MODE');
  assert.equal(prodVars.NV_ENABLE_LAYERS_2_3, '0');

  assert.equal(previewVars.ENVIRONMENT, 'preview');
  assert.equal(previewVars.NV_FORCE_LAUNCH_MODE, '1', 'Preview must force launch mode without dates');
  assert.equal(previewVars.NV_LAUNCH_STARTS_AT || '', '', 'Preview NV_LAUNCH_STARTS_AT must be empty');
  assert.equal(previewVars.NV_LAUNCH_ENDS_AT || '', '', 'Preview NV_LAUNCH_ENDS_AT must be empty');
  assert.equal(previewVars.NV_ENABLE_LAYERS_2_3, '1');

  const prodState = resolveServerLaunchOfferState(prodVars);
  assert.equal(prodState.active, false);
  assert.equal(prodState.configured, false);
  assert.equal(prodState.forced, false);

  const previewState = resolveServerLaunchOfferState(previewVars);
  assert.equal(previewState.active, true);
  assert.equal(previewState.configured, true);
  assert.equal(previewState.forced, true);
  assert.equal(previewState.startedAt, null);
  assert.equal(previewState.endsAt, null);

  // Verify production refuses NV_FORCE_LAUNCH_MODE if ever accidentally set
  const badProdEnv = { ...prodVars, NV_FORCE_LAUNCH_MODE: '1' };
  const badResp = await worker.fetch(new Request('https://numerosvision.com/api/v1/pricing-catalog'), badProdEnv, {});
  assert.equal(badResp.status, 500, 'Production must block NV_FORCE_LAUNCH_MODE via DANGEROUS_FLAGS');

  console.log('PASS [Gate 3]: wrangler.toml preview forced launch mode (date-free) & production empty launch fields verified.');
}

function createRealSqliteD1() {
  const sqlite = new DatabaseSync(':memory:');
  const migDir = path.join(repoRoot, 'migrations');
  const migFiles = fs.readdirSync(migDir).filter((f) => f.endsWith('.sql')).sort();
  for (const mf of migFiles) {
    sqlite.exec(fs.readFileSync(path.join(migDir, mf), 'utf8'));
  }
  return {
    prepare(sql) {
      return {
        _sql: sql,
        _params: [],
        bind(...params) {
          this._params = params.map((v) => (v === undefined ? null : v));
          return this;
        },
        async first() {
          const stmt = sqlite.prepare(this._sql);
          const row = stmt.get(...this._params);
          return row === undefined ? null : row;
        },
        async all() {
          const stmt = sqlite.prepare(this._sql);
          return { results: stmt.all(...this._params) };
        },
        async run() {
          const stmt = sqlite.prepare(this._sql);
          const info = stmt.run(...this._params);
          return { success: true, meta: { changes: info.changes } };
        }
      };
    }
  };
}

async function testGate1PackPriceParityBothModes() {
  const allPlans = collectAllPlansFromPacksJson();
  assert.ok(allPlans.length >= 10, `Expected >= 10 plans in packs.json, got ${allPlans.length}`);

  const d1 = createRealSqliteD1();
  const baseSecrets = {
    DB: d1,
    REPORTS_BUCKET: { put: async () => {}, get: async () => null },
    RAZORPAY_KEY_ID: 'rzp_test_paritykey123',
    RAZORPAY_KEY_SECRET: 'rzp_test_paritysecret456',
    RAZORPAY_WEBHOOK_SECRET: 'whsec_parity789',
    OTP_HMAC_SECRET: 'otp_hmac_secret_32_bytes_parity!!',
    SESSION_SECRET: 'sess_secret_32_bytes_minimum_length_ok!!',
    DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
    PDF_SERVICE_SECRET: 'pdf_secret_parity_check_12345678',
    PDF_SERVICE_URL: 'https://pdf-internal.example.com',
    DOWNLOAD_TOKEN_SECRET: 'dl_secret_parity_check_123456789',
    IP_HASH_SALT: 'salt_parity_check_123'
  };

  // Matrix of modes:
  // 1) Launch mode + default waitlist flags (matches preview wrangler.toml)
  // 2) Regular mode + default waitlist flags (matches production wrangler.toml)
  // 3) Launch mode + all report/planner tiers unlocked (verifies Advanced/Premium/Planner paise parity too)
  // 4) Regular mode + all report/planner tiers unlocked (verifies Advanced/Premium regular mrp_paise parity too)
  const scenarios = [
    {
      name: 'launch_default_waitlist',
      isLaunch: true,
      notifyHigher: true,
      plannerLive: false,
      env: { ...baseSecrets, ENVIRONMENT: 'preview', NV_FORCE_LAUNCH_MODE: '1', NV_LAUNCH_STARTS_AT: '', NV_LAUNCH_ENDS_AT: '' }
    },
    {
      name: 'regular_default_waitlist',
      isLaunch: false,
      notifyHigher: true,
      plannerLive: false,
      env: { ...baseSecrets, ENVIRONMENT: 'production', NV_LAUNCH_STARTS_AT: '', NV_LAUNCH_ENDS_AT: '' }
    },
    {
      name: 'launch_all_unlocked',
      isLaunch: true,
      notifyHigher: false,
      plannerLive: true,
      env: {
        ...baseSecrets,
        ENVIRONMENT: 'preview',
        NV_FORCE_LAUNCH_MODE: '1',
        NV_NOTIFY_ME_HIGHER_TIERS: 'false',
        PLANNER_2027_LIVE: 'true'
      }
    },
    {
      name: 'regular_all_unlocked',
      isLaunch: false,
      notifyHigher: false,
      plannerLive: true,
      env: {
        ...baseSecrets,
        ENVIRONMENT: 'production',
        NV_LAUNCH_STARTS_AT: '',
        NV_LAUNCH_ENDS_AT: '',
        NV_NOTIFY_ME_HIGHER_TIERS: 'false',
        PLANNER_2027_LIVE: 'true'
      }
    }
  ];

  const userId = 'usr_price_parity_1';
  const nowTs = Date.now();
  await d1.prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)').bind(userId, 'parity@example.com', nowTs).run();
  const rawToken = await mintUserSession(baseSecrets, userId, '127.0.0.1', nowTs);
  const sessCookie = `__Host-nv_session=${rawToken}`;

  const origFetch = globalThis.fetch;
  let capturedRazorpayOrders = [];
  let rzpOrderSeq = 0;
  globalThis.fetch = async (input, init = {}) => {
    const urlStr = typeof input === 'string' ? input : input.url;
    if (urlStr === 'https://api.razorpay.com/v1/orders') {
      const parsedBody = JSON.parse(init.body);
      capturedRazorpayOrders.push(parsedBody);
      rzpOrderSeq += 1;
      return new Response(
        JSON.stringify({
          id: 'order_rzp_' + rzpOrderSeq,
          amount: parsedBody.amount,
          currency: parsedBody.currency,
          status: 'created'
        }),
        { status: 200, headers: { 'Content-Type': 'application/json' } }
      );
    }
    return origFetch(input, init);
  };

  try {
    for (const sc of scenarios) {
      const scD1 = createRealSqliteD1();
      const scNow = Date.now();
      await scD1.prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)').bind(userId, 'parity@example.com', scNow).run();
      const scEnv = { ...sc.env, DB: scD1 };
      const scRawToken = await mintUserSession(scEnv, userId, '127.0.0.1', scNow);
      const scCookie = `__Host-nv_session=${scRawToken}`;

      for (const { bucket, id, entry } of allPlans) {
        const isWaitlistedInScenario =
          (id === 'planner_2027' && !sc.plannerLive) ||
          ((id === 'report_advanced' || id === 'report_premium') && sc.notifyHigher);

        let expectedHelperPaise = 0;
        if (isWaitlistedInScenario) {
          expectedHelperPaise = 0;
        } else if (bucket === 'core_reports' && entry.mrp_inr) {
          expectedHelperPaise = sc.isLaunch
            ? entry.amount_paise
            : (entry.mrp_paise || entry.mrp_inr * 100);
        } else if (typeof entry.amount_paise === 'number') {
          expectedHelperPaise = entry.amount_paise;
        } else {
          expectedHelperPaise = 0;
        }

        const actualHelperPaise = resolveEffectivePackPricePaise(id, scEnv);
        assert.equal(
          actualHelperPaise,
          expectedHelperPaise,
          `[${sc.name}] resolveEffectivePackPricePaise(${id}) = ${actualHelperPaise}, expected ${expectedHelperPaise}`
        );

        // Now verify actual create-order endpoint charges the exact same amount from packs.json!
        capturedRazorpayOrders = [];
        const origin = scEnv.ENVIRONMENT === 'production'
          ? 'https://numerosvision.com'
          : 'https://preview.numeros-vision.pages.dev';
        const req = new Request(`${origin}/api/v1/payments/create-order`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Origin': origin,
            'Cookie': scCookie
          },
          body: JSON.stringify({
            packId: id,
            customerDob: '1990-05-15',
            customerGender: 'male',
            dpdpConsent: true
          })
        });
        const resp = await worker.fetch(req, scEnv, {});
        const respJson = await resp.json();

        const isActivePurchasable =
          !isWaitlistedInScenario &&
          entry.status === 'active' &&
          expectedHelperPaise > 0;

        if (isWaitlistedInScenario) {
          assert.equal(resp.status, 409, `[${sc.name}] waitlisted ${id} must return 409`);
          assert.equal(capturedRazorpayOrders.length, 0);
        } else if (!isActivePurchasable) {
          assert.equal(resp.status, 400, `[${sc.name}] non-purchasable ${id} must return 400`);
          assert.equal(capturedRazorpayOrders.length, 0);
        } else {
          assert.equal(resp.status, 200, `[${sc.name}] active ${id} must return 200, got ${resp.status}: ${JSON.stringify(respJson)}`);
          assert.equal(capturedRazorpayOrders.length, 1);
          assert.equal(
            capturedRazorpayOrders[0].amount,
            expectedHelperPaise,
            `[${sc.name}] Razorpay charged amount for ${id} (${capturedRazorpayOrders[0].amount}) != packs.json (${expectedHelperPaise})`
          );
          assert.equal(respJson.amount, expectedHelperPaise);
        }
      }
    }
  } finally {
    globalThis.fetch = origFetch;
  }

  console.log(`PASS [Gate 1]: resolveEffectivePackPricePaise + create-order match packs.json across all ${allPlans.length} plan IDs in launch & regular modes.`);
}

async function runSwBehaviourCheckForFile(swPath) {
  const swCode = fs.readFileSync(swPath, 'utf8');
  const listeners = {};
  const cacheStores = new Map();
  const putCalls = [];
  const networkCalls = [];
  let seq = 0;

  class MockCache {
    constructor(name) {
      this.name = name;
      this.entries = new Map();
    }
    async addAll(urls) {
      for (const u of urls) {
        this.entries.set(new URL(u, 'https://numerosvision.com').href, new Response('precached:' + u, { status: 200 }));
      }
    }
    async put(req, resp) {
      const url = typeof req === 'string' ? new URL(req, 'https://numerosvision.com').href : req.url;
      putCalls.push({ cacheName: this.name, url });
      this.entries.set(url, resp);
    }
    async match(req) {
      const url = typeof req === 'string' ? new URL(req, 'https://numerosvision.com').href : req.url;
      return this.entries.get(url) || undefined;
    }
  }

  const cachesApi = {
    async open(name) {
      if (!cacheStores.has(name)) cacheStores.set(name, new MockCache(name));
      return cacheStores.get(name);
    },
    async keys() {
      return Array.from(cacheStores.keys());
    },
    async delete(name) {
      return cacheStores.delete(name);
    },
    async match(req) {
      for (const c of cacheStores.values()) {
        const hit = await c.match(req);
        if (hit) return hit;
      }
      return undefined;
    }
  };

  const mockFetch = async (input) => {
    seq += 1;
    const req = input instanceof Request ? input : new Request(String(input));
    const u = new URL(req.url);
    networkCalls.push({
      url: req.url,
      pathname: u.pathname,
      cookie: req.headers.get('cookie') || '',
      authorization: req.headers.get('authorization') || '',
      seq
    });
    const isHtml = u.pathname.startsWith('/dashboard');
    return new Response(
      isHtml ? `<html><body>dashboard-seq-${seq}</body></html>` : JSON.stringify({ seq, path: u.pathname }),
      {
        status: 200,
        headers: {
          'Content-Type': isHtml ? 'text/html; charset=utf-8' : 'application/json'
        }
      }
    );
  };

  const sandbox = {
    self: null,
    location: new URL('https://numerosvision.com/'),
    caches: cachesApi,
    fetch: mockFetch,
    URL,
    Request,
    Response,
    Headers,
    Promise,
    console,
    addEventListener(type, fn) {
      listeners[type] = listeners[type] || [];
      listeners[type].push(fn);
    },
    skipWaiting: async () => {},
    clients: { claim: async () => {} }
  };
  sandbox.self = sandbox;
  vm.createContext(sandbox);
  vm.runInContext(swCode, sandbox, { filename: swPath });

  assert.ok(listeners.fetch && listeners.fetch.length === 1, `${path.basename(swPath)} must register a fetch listener`);

  const dispatchFetch = async (req) => {
    let respondedPromise = null;
    const waitPromises = [];
    const event = {
      request: req,
      respondWith(p) {
        respondedPromise = Promise.resolve(p);
      },
      waitUntil(p) {
        waitPromises.push(Promise.resolve(p));
      }
    };
    listeners.fetch[0](event);
    const resp = respondedPromise ? await respondedPromise : await mockFetch(req);
    await Promise.all(waitPromises);
    // Flush microtasks for any async cache.put inside .then()
    await new Promise((r) => setTimeout(r, 5));
    return resp;
  };

  const sensitiveRoutes = [
    { url: 'https://numerosvision.com/dashboard', auth: false },
    { url: 'https://numerosvision.com/dashboard', auth: true },
    { url: 'https://numerosvision.com/dashboard/', auth: true },
    { url: 'https://numerosvision.com/dashboard/?order_id=ord_777', auth: true },
    { url: 'https://numerosvision.com/api/me', auth: false },
    { url: 'https://numerosvision.com/api/me', auth: true },
    { url: 'https://numerosvision.com/api/v1/dashboard/view', auth: true },
    { url: 'https://numerosvision.com/api/v1/pricing-catalog', auth: false },
    { url: 'https://numerosvision.com/api/charm/chat/stream', auth: true, method: 'POST' }
  ];

  for (const item of sensitiveRoutes) {
    const makeReq = () =>
      new Request(item.url, {
        method: item.method || 'GET',
        headers: item.auth
          ? {
              Cookie: '__Host-nv_session=sess_authenticated_xyz',
              Authorization: 'Bearer nv_token_authenticated_xyz',
              Accept: item.url.includes('/dashboard') ? 'text/html' : 'application/json'
            }
          : {
              Accept: item.url.includes('/dashboard') ? 'text/html' : 'application/json'
            }
      });

    const beforeNet = networkCalls.length;
    const r1 = await dispatchFetch(makeReq());
    const body1 = await r1.text();
    const r2 = await dispatchFetch(makeReq());
    const body2 = await r2.text();

    assert.equal(networkCalls.length, beforeNet + 2, `Both requests to ${item.url} (auth=${item.auth}) must go to live network`);
    assert.notEqual(body1, body2, `Repeated requests to ${item.url} (auth=${item.auth}) must return fresh network bodies, never cached response`);
  }

  // Verify ZERO /dashboard or /api/ entries were ever written to any cache
  const badPuts = putCalls.filter((p) => {
    const pathname = new URL(p.url).pathname;
    return pathname.startsWith('/dashboard') || pathname.startsWith('/api/');
  });
  assert.deepEqual(badPuts, [], `sw.js cached sensitive /dashboard or /api/ URLs: ${JSON.stringify(badPuts)}`);

  // Positive control: prove cacheable static CSS asset DOES trigger cache.put in this exact VM harness
  const putsBeforeStatic = putCalls.length;
  await dispatchFetch(new Request('https://numerosvision.com/static/css/theme.css?v=5.4.0', { method: 'GET' }));
  assert.ok(putCalls.length > putsBeforeStatic, 'Positive control failed: static CSS asset should be cached by sw.js');
}

async function testGate2ServiceWorkerBehaviour() {
  await runSwBehaviourCheckForFile(path.join(repoRoot, 'app/static/sw.js'));
  const distSw = path.join(repoRoot, 'dist_cloudflare_pages/sw.js');
  if (fs.existsSync(distSw)) {
    await runSwBehaviourCheckForFile(distSw);
  }
  console.log('PASS [Gate 2]: sw.js behaviour test proved 0 cache writes and live network pass-through for /dashboard & /api/ (unauthenticated + authenticated).');
}

async function testGate5RealTimeStageStream() {
  const origFetch = globalThis.fetch;
  const writeHoldMs = 220;

  globalThis.fetch = async (input, init = {}) => {
    const urlStr = typeof input === 'string' ? input : input.url;
    if (urlStr === 'http://127.0.0.1:19999/api/charm/chat/stream') {
      const encoder = new TextEncoder();
      const stream = new ReadableStream({
        async start(controller) {
          const stages = [
            [1, 'reading_birth_date', 'Reading your birth date'],
            [2, 'mapping_loshu_grid', 'Mapping your Lo Shu grid'],
            [3, 'checking_cycles', 'Checking your cycles'],
            [4, 'putting_reading_together', 'Putting your reading together']
          ];
          for (const [idx, sid, lbl] of stages) {
            controller.enqueue(encoder.encode(`event: stage\ndata: ${JSON.stringify({ stage: sid, label: lbl, status: 'started', step_index: idx, total_steps: 5, elapsed_ms: 0 })}\n\n`));
            controller.enqueue(encoder.encode(`event: stage\ndata: ${JSON.stringify({ stage: sid, label: lbl, status: 'completed', step_index: idx, total_steps: 5, elapsed_ms: 1 })}\n\n`));
          }
          // Stage 5 starts BEFORE slow LLM Write
          controller.enqueue(encoder.encode(`event: stage\ndata: ${JSON.stringify({ stage: 'writing_answer', label: 'Writing your answer', status: 'started', step_index: 5, total_steps: 5, elapsed_ms: 0 })}\n\n`));
          await new Promise((r) => setTimeout(r, writeHoldMs));
          controller.enqueue(encoder.encode(`event: stage\ndata: ${JSON.stringify({ stage: 'writing_answer', label: 'Writing your answer', status: 'completed', step_index: 5, total_steps: 5, elapsed_ms: writeHoldMs })}\n\n`));
          controller.enqueue(
            encoder.encode(
              `event: result\ndata: ${JSON.stringify({
                status: 'ANSWERED',
                topic: 'career',
                credit_chargeable: true,
                used_fallback: false,
                llm_rejected: false,
                human_friendly_summary: { headline: 'Steady Focus', supported_by_report: 'Numbers are a guide, not a compulsion.' },
                assistant_message: { text: 'Driver 8 and Conductor 2 may indicate steady focus. Numerology is a reflective guide, not a prediction.' },
                practical_next_steps: ['Keep one priority list.'],
                follow_up_question: 'Which months should I take extra care in 2027?'
              })}\n\n`
            )
          );
          controller.close();
        }
      });
      return new Response(stream, { status: 200, headers: { 'Content-Type': 'text/event-stream; charset=utf-8' } });
    }
    return origFetch(input, init);
  };

  try {
    const streamEnv = {
      ENVIRONMENT: 'preview',
      CHARM_SERVICE_URL: 'http://127.0.0.1:19999',
      CHARM_SERVICE_SECRET: 'test_charm_secret_123',
      IP_HASH_SALT: 'test_salt_stream_123',
      __TEST__: true
    };
    const t0 = Date.now();
    const resp = await worker.fetch(
      new Request('https://preview.numeros-vision.pages.dev/api/charm/chat/stream', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Origin': 'https://preview.numeros-vision.pages.dev',
          'CF-Connecting-IP': '203.0.113.77'
        },
        body: JSON.stringify({
          message: 'What do my numbers indicate for career focus?',
          day: 26,
          month: 3,
          year: 1980,
          gender: 'male'
        })
      }),
      streamEnv,
      {}
    );
    assert.equal(resp.status, 200);
    assert.ok((resp.headers.get('content-type') || '').includes('text/event-stream'));

    const reader = resp.body.getReader();
    const decoder = new TextDecoder('utf-8');
    let buf = '';
    const arrivals = [];
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      const nowElapsed = Date.now() - t0;
      buf += decoder.decode(value, { stream: true });
      const blocks = buf.split('\n\n');
      buf = blocks.pop() || '';
      for (const blk of blocks) {
        if (!blk.trim()) continue;
        let evType = 'message';
        let dataStr = '';
        for (const ln of blk.split('\n')) {
          if (ln.startsWith('event:')) evType = ln.slice(6).trim();
          else if (ln.startsWith('data:')) dataStr += ln.slice(5).trim();
        }
        arrivals.push({ evType, payload: JSON.parse(dataStr), arrivedAtMs: nowElapsed });
      }
    }

    const stage5Start = arrivals.find((a) => a.evType === 'stage' && a.payload.stage === 'writing_answer' && a.payload.status === 'started');
    const stage5Done = arrivals.find((a) => a.evType === 'stage' && a.payload.stage === 'writing_answer' && a.payload.status === 'completed');
    const finalResult = arrivals.find((a) => a.evType === 'result');

    assert.ok(stage5Start, 'Must emit writing_answer started event');
    assert.ok(stage5Done, 'Must emit writing_answer completed event');
    assert.ok(finalResult, 'Must emit final result event');
    const gapMs = stage5Done.arrivedAtMs - stage5Start.arrivedAtMs;
    assert.ok(
      gapMs >= 150,
      `Expected writing_answer started to arrive >=150ms before completed (real-time streaming, not buffered), got gap=${gapMs}ms`
    );
    assert.equal(finalResult.payload.credits_remaining, 2);
  } finally {
    globalThis.fetch = origFetch;
  }

  console.log('PASS [Gate 5]: /api/charm/chat/stream streams stage events live as steps start/complete (zero post-hoc timer).');
}

await testGate3WranglerVars();
await testGate1PackPriceParityBothModes();
await testGate2ServiceWorkerBehaviour();
await testGate5RealTimeStageStream();
console.log('ALL PRE-COMMIT GATES PASSED.');
