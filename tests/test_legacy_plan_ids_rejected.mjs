/**
 * Verification Suite: Legacy Plan IDs Rejected at create-order (Worker)
 * =====================================================================
 * Proves that retired plan IDs:
 *   - report_essential, report_master, report_divine, master, divine
 *   - starter_5q, ai_starter_5q, ai_report_combo
 *   - growth_10q, ai_growth_15q, ai_power_35q, complete_report
 * are rejected at both POST /api/v1/payments/create-order and POST /api/create-order
 * with HTTP 400 (4xx), zero Razorpay API calls, and zero D1 orders rows.
 */

import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { DatabaseSync } from 'node:sqlite';
import { fileURLToPath } from 'node:url';
import worker from '../app/static/_worker.js';

const { getPackById, mintUserSession } = worker;
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

const LEGACY_IDS = [
  'report_essential',
  'report_master',
  'report_divine',
  'master',
  'divine',
  'starter_5q',
  'ai_starter_5q',
  'ai_report_combo',
  'growth_10q',
  'ai_growth_15q',
  'ai_power_35q',
  'complete_report'
];

const d1 = createRealSqliteD1();
const env = {
  ENVIRONMENT: 'preview',
  DB: d1,
  REPORTS_BUCKET: { put: async () => {}, get: async () => null },
  OTP_HMAC_SECRET: 'a'.repeat(64),
  SESSION_SECRET: 'b'.repeat(64),
  IP_HASH_SALT: 'c'.repeat(64),
  DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
  PDF_SERVICE_SECRET: 'd'.repeat(64),
  PDF_SERVICE_URL: 'https://pdf-mock.internal',
  DOWNLOAD_TOKEN_SECRET: 'e'.repeat(64),
  RAZORPAY_KEY_ID: 'rzp_test_legacycheck123',
  RAZORPAY_KEY_SECRET: 'secret_test_legacycheck123'
};

const nowTs = Date.now();
const userId = 'usr_legacy_check_1';
await d1.prepare('INSERT INTO users (id, email, created_at) VALUES (?, ?, ?)').bind(userId, 'legacy@example.com', nowTs).run();
const sessionToken = await mintUserSession(env, userId, '127.0.0.1', nowTs);

let razorpayCalls = 0;
const origFetch = globalThis.fetch;
globalThis.fetch = async (input, init) => {
  const urlStr = typeof input === 'string' ? input : input.url;
  if (urlStr.includes('razorpay.com')) {
    razorpayCalls += 1;
    throw new Error('Razorpay must NEVER be called for rejected legacy plan IDs');
  }
  return origFetch(input, init);
};

try {
  for (const legacyId of LEGACY_IDS) {
    assert.equal(getPackById(legacyId, env, nowTs), null, `getPackById("${legacyId}") must return null`);

    for (const endpoint of ['/api/v1/payments/create-order', '/api/create-order']) {
      const req = new Request(`https://preview.numeros-vision.pages.dev${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Origin': 'https://preview.numeros-vision.pages.dev',
          'Cookie': `__Host-nv_session=${sessionToken}`
        },
        body: JSON.stringify({
          pack_id: legacyId,
          name: 'Legacy Test User',
          dob: '1990-05-15',
          email: 'legacy@example.com'
        })
      });
      const resp = await worker.fetch(req, env, {});
      assert.equal(resp.status, 400, `Expected 400 for "${legacyId}" on ${endpoint}, got ${resp.status}`);
      const payload = await resp.json();
      assert.equal(payload.success, false);
      assert.equal(payload.code, 'LEGACY_PLAN_ID_REJECTED');
    }
  }

  assert.equal(razorpayCalls, 0, 'Zero Razorpay order calls must occur');
  const orderCountRow = await d1.prepare('SELECT COUNT(*) as cnt FROM orders').first();
  assert.equal(Number(orderCountRow.cnt), 0, 'Zero D1 order rows must be created for legacy plan IDs');

  console.log(`PASS: All ${LEGACY_IDS.length} legacy plan IDs rejected with HTTP 400 across both Worker create-order endpoints (0 Razorpay calls, 0 D1 rows).`);
} finally {
  globalThis.fetch = origFetch;
}
