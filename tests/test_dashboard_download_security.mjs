/**
 * NUMEROS VISION — DASHBOARD SECURE DOWNLOAD & R2 VERIFICATION SUITE
 *
 * Verifies:
 * 1. dashboard/view never returns a /samples/ URL for a paid job.
 * 2. POST /api/v1/reports/download-token generates a 5-minute signed token bound to user session.
 * 3. GET /api/v1/reports/download?token=... returns exact R2 bytes matching the SHA-256 hash.
 * 4. Response headers:
 *    - Content-Type: application/pdf
 *    - Content-Disposition: attachment; filename="Numeros_Vision_Basic_Report.pdf"
 *    - Cache-Control: private, no-store
 * 5. Security guards:
 *    - Cross-user rejection: User B attempting to download User A's report gets 403/404, never bytes.
 *    - Expiration rejection: Expired token (> 300s) gets 403.
 *    - Incomplete job rejection: Job not in COMPLETED/DOWNLOADED state refuses download token / returns 404.
 */

import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import worker, {
  encryptField,
  createSignedDownloadToken,
  memoryStore
} from '../app/static/_worker.js';

const TEST_ENV = {
  ENVIRONMENT: 'local',
  RAZORPAY_KEY_ID: 'rzp_test_MOCK_DOWNLOAD_SEC',
  RAZORPAY_KEY_SECRET: 'rzp_secret_mock_sec',
  RAZORPAY_WEBHOOK_SECRET: 'rzp_webhook_secret_sec',
  OTP_HMAC_SECRET: '1111111111111111111111111111111111111111111111111111111111111111',
  SESSION_SECRET: '2222222222222222222222222222222222222222222222222222222222222222',
  IP_HASH_SALT: '3333333333333333333333333333333333333333333333333333333333333333',
  DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
  PDF_SERVICE_SECRET: 'fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210',
  DOWNLOAD_TOKEN_SECRET: 'abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789'
};

function createMockR2Bucket() {
  const store = new Map();
  return {
    store,
    async put(key, value, options) {
      const bytes = value instanceof Uint8Array ? value : new Uint8Array(value);
      store.set(key, { bytes, options });
    },
    async get(key) {
      const entry = store.get(key);
      if (!entry) return null;
      return {
        async arrayBuffer() {
          return entry.bytes.buffer.slice(entry.bytes.byteOffset, entry.bytes.byteOffset + entry.bytes.byteLength);
        }
      };
    }
  };
}

async function runTests() {
  console.log('=== TEST SUITE: DASHBOARD SECURE DOWNLOAD & R2 VERIFICATION ===\n');

  const r2Bucket = createMockR2Bucket();
  const env = { ...TEST_ENV, REPORTS_BUCKET: r2Bucket };

  const userA = 'usr_test_buyer_A';
  const userB = 'usr_test_attacker_B';
  const subjectA = 'sbj_test_subject_A';
  const packId = 'report_basic';
  const completedJobId = 'job_test_completed_123';
  const queuedJobId = 'job_test_queued_456';
  const now = Date.now();

  // 1. Seed simulated personalized PDF in R2
  const fakePdfContent = Buffer.from('%PDF-1.4\n%Numeros Vision Personalized Report for Bhaskr Singh (DOB: 1981-11-28)\n%%EOF');
  const expectedHash = crypto.createHash('sha256').update(fakePdfContent).digest('hex');
  const r2Key = `reports/${userA}/${subjectA}/${packId}/${completedJobId}.pdf`;
  await r2Bucket.put(r2Key, fakePdfContent, { httpMetadata: { contentType: 'application/pdf' } });

  // 2. Seed memory store with users, sessions, subject, entitlements, and jobs
  const dobEnc = await encryptField('1981-11-28', env.DATA_ENCRYPTION_KEY);
  const phoneEnc = await encryptField('+919876543210', env.DATA_ENCRYPTION_KEY);

  memoryStore.users.set(userA, {
    id: userA,
    email: 'bhaskr@example.com',
    phone_hash: 'hash_user_A',
    phone_enc: phoneEnc,
    created_at: now
  });
  memoryStore.users.set(userB, {
    id: userB,
    email: 'attacker@example.com',
    phone_hash: 'hash_user_B',
    phone_enc: phoneEnc,
    created_at: now
  });

  // User A session
  const rawTokenA = 'sess_token_buyer_A';
  const tokenHashA = crypto.createHmac('sha256', env.SESSION_SECRET).update(rawTokenA).digest('hex');
  memoryStore.sessions.set(tokenHashA, {
    id: 'ses_A',
    user_id: userA,
    token_hash: tokenHashA,
    expires_at: now + 86400000
  });
  const cookieA = `nv_session=${rawTokenA}`;

  // User B session
  const rawTokenB = 'sess_token_attacker_B';
  const tokenHashB = crypto.createHmac('sha256', env.SESSION_SECRET).update(rawTokenB).digest('hex');
  memoryStore.sessions.set(tokenHashB, {
    id: 'ses_B',
    user_id: userB,
    token_hash: tokenHashB,
    expires_at: now + 86400000
  });
  const cookieB = `nv_session=${rawTokenB}`;

  memoryStore.subjects.set(subjectA, {
    id: subjectA,
    user_id: userA,
    name: 'Bhaskr Singh',
    dob_hash: 'dob_hash_A',
    dob_enc: dobEnc,
    created_at: now
  });

  memoryStore.entitlements.set(`${userA}_${subjectA}_${packId}`, {
    user_id: userA,
    subject_id: subjectA,
    pack_id: packId,
    order_id: 'ord_test_1',
    granted_at: now
  });

  // Completed job
  memoryStore.reportJobs.set(completedJobId, {
    id: completedJobId,
    user_id: userA,
    subject_id: subjectA,
    pack_id: packId,
    order_id: 'ord_test_1',
    status: 'COMPLETED',
    attempts: 0,
    max_attempts: 3,
    r2_key: r2Key,
    last_error: null,
    created_at: now - 60000,
    updated_at: now,
    completed_at: now
  });

  // Queued (uncompleted) job
  memoryStore.reportJobs.set(queuedJobId, {
    id: queuedJobId,
    user_id: userA,
    subject_id: subjectA,
    pack_id: packId,
    order_id: 'ord_test_2',
    status: 'QUEUED',
    attempts: 0,
    max_attempts: 3,
    r2_key: null,
    last_error: null,
    created_at: now,
    updated_at: now
  });

  // ─────────────────────────────────────────────────────────────
  // TEST 1: dashboard/view NEVER returns /samples/ for paid job
  // ─────────────────────────────────────────────────────────────
  console.log('[TEST 1] Verifying GET /api/v1/dashboard/view never returns /samples/ URL...');
  const dashReq = new Request('https://numerosvision.com/api/v1/dashboard/view', {
    headers: { 'Cookie': cookieA }
  });
  const dashRes = await worker.fetch(dashReq, env);
  assert.equal(dashRes.status, 200, 'Dashboard view must return 200 for authenticated user');
  const dashData = await dashRes.json();

  const completedJobView = dashData.reports.find(r => r.id === completedJobId);
  assert(completedJobView, 'Completed job must be present in dashboard reports');
  assert.equal(completedJobView.isDownloadable, true, 'Completed job must have isDownloadable: true');
  assert.equal(completedJobView.downloadUrl, null, 'downloadUrl must be null (no static/view-time token in dashboard/view)');
  assert(!JSON.stringify(dashData).includes('/samples/'), 'Entire dashboard/view response MUST NOT contain /samples/');
  console.log('  -> PASS: dashboard/view contains zero /samples/ and downloadUrl is null\n');

  // ─────────────────────────────────────────────────────────────
  // TEST 2: POST /api/v1/reports/download-token mints click-time token
  // ─────────────────────────────────────────────────────────────
  console.log('[TEST 2] Verifying click-time token minting via POST /api/v1/reports/download-token...');
  const tokenReq = new Request('https://numerosvision.com/api/v1/reports/download-token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Cookie': cookieA
    },
    body: JSON.stringify({
      subjectId: subjectA,
      packId: packId,
      jobId: completedJobId
    })
  });
  const tokenRes = await worker.fetch(tokenReq, env);
  assert.equal(tokenRes.status, 200, 'download-token must return 200 for valid completed job');
  const tokenData = await tokenRes.json();
  assert.equal(tokenData.success, true);
  assert(tokenData.token, 'Token string must be present');
  assert(tokenData.downloadUrl.startsWith('/api/v1/reports/download?token='), 'downloadUrl must route to /api/v1/reports/download');
  assert.equal(tokenData.expiresInSeconds, 300, 'Token TTL must be 300s (5 minutes)');
  console.log('  -> PASS: Click-time token minted successfully with 300s TTL\n');

  // ─────────────────────────────────────────────────────────────
  // TEST 3: GET /api/v1/reports/download serves real R2 bytes & headers
  // ─────────────────────────────────────────────────────────────
  console.log('[TEST 3] Verifying GET /api/v1/reports/download returns real R2 bytes and proper headers...');
  const dlReq = new Request(`https://numerosvision.com${tokenData.downloadUrl}`, {
    headers: { 'Cookie': cookieA }
  });
  const dlRes = await worker.fetch(dlReq, env);
  assert.equal(dlRes.status, 200, 'Download endpoint must return 200');

  // Headers check
  assert.equal(dlRes.headers.get('Content-Type'), 'application/pdf', 'Content-Type must be application/pdf');
  assert.equal(dlRes.headers.get('Content-Disposition'), 'attachment; filename="Numeros_Vision_Basic_Report.pdf"', 'Content-Disposition must have clean filename');
  assert.equal(dlRes.headers.get('Cache-Control'), 'private, no-store', 'Cache-Control must be private, no-store');

  // Byte & hash check
  const downloadedBytes = Buffer.from(await dlRes.arrayBuffer());
  const actualHash = crypto.createHash('sha256').update(downloadedBytes).digest('hex');
  assert.equal(actualHash, expectedHash, 'Downloaded byte hash must match exact R2 object hash');
  assert.equal(downloadedBytes.length, fakePdfContent.length, 'Downloaded byte length must match R2 object length');
  console.log(`  -> PASS: Downloaded bytes verified (Hash: ${actualHash.slice(0, 16)}... Len: ${downloadedBytes.length}) with correct headers\n`);

  // ─────────────────────────────────────────────────────────────
  // TEST 4: Security rejection — Cross-user token or session
  // ─────────────────────────────────────────────────────────────
  console.log('[TEST 4] Verifying security: Cross-user access rejected...');
  // User B tries to use User A's token with User B's session
  const crossUserReq = new Request(`https://numerosvision.com${tokenData.downloadUrl}`, {
    headers: { 'Cookie': cookieB }
  });
  const crossUserRes = await worker.fetch(crossUserReq, env);
  assert.equal(crossUserRes.status, 403, 'Cross-user session mismatch must return 403 Forbidden');
  const crossUserBody = await crossUserRes.json();
  assert.equal(crossUserBody.success, false);
  assert(crossUserBody.error.includes('binding mismatch') || crossUserRes.status === 403);

  // User B tries to mint a token for User A's job
  const attackerMintReq = new Request('https://numerosvision.com/api/v1/reports/download-token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Cookie': cookieB
    },
    body: JSON.stringify({
      subjectId: subjectA,
      packId: packId,
      jobId: completedJobId
    })
  });
  const attackerMintRes = await worker.fetch(attackerMintReq, env);
  assert.equal(attackerMintRes.status, 404, 'User B must not be able to mint a token for User A job (404)');

  // Request with no session cookie
  const noSessionReq = new Request(`https://numerosvision.com${tokenData.downloadUrl}`);
  const noSessionRes = await worker.fetch(noSessionReq, env);
  assert.equal(noSessionRes.status, 401, 'Unauthenticated download must return 401 Unauthorized');
  console.log('  -> PASS: Cross-user and unauthenticated download strictly rejected with 401/403/404\n');

  // ─────────────────────────────────────────────────────────────
  // TEST 5: Security rejection — Expired token (> 300s)
  // ─────────────────────────────────────────────────────────────
  console.log('[TEST 5] Verifying security: Expired token (> 300s) rejected...');
  // Mint an already expired token (iat: now - 3600, ttl: 300)
  const expiredToken = await createSignedDownloadToken({
    userId: userA,
    subjectId: subjectA,
    packId: packId,
    jobId: completedJobId,
    nowSec: Math.floor(Date.now() / 1000) - 350,
    ttlSec: 300
  }, env.DOWNLOAD_TOKEN_SECRET);

  const expiredReq = new Request(`https://numerosvision.com/api/v1/reports/download?token=${encodeURIComponent(expiredToken)}`, {
    headers: { 'Cookie': cookieA }
  });
  const expiredRes = await worker.fetch(expiredReq, env);
  assert.equal(expiredRes.status, 403, 'Expired download token must return 403 Forbidden');
  const expiredBody = await expiredRes.json();
  assert(expiredBody.error.includes('expired'), 'Error message must specify token expiration');
  console.log('  -> PASS: Expired token rejected with 403\n');

  // ─────────────────────────────────────────────────────────────
  // TEST 6: Incomplete job returns no download link / rejects download
  // ─────────────────────────────────────────────────────────────
  console.log('[TEST 6] Verifying uncompleted job (QUEUED) rejects download token minting...');
  const queuedTokenReq = new Request('https://numerosvision.com/api/v1/reports/download-token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Cookie': cookieA
    },
    body: JSON.stringify({
      subjectId: subjectA,
      packId: packId,
      jobId: queuedJobId
    })
  });
  const queuedTokenRes = await worker.fetch(queuedTokenReq, env);
  assert.equal(queuedTokenRes.status, 404, 'Queued job must return 404 (Completed report job not found)');

  console.log('  -> PASS: Queued job refuses download token\n');

  console.log('=== ALL DASHBOARD DOWNLOAD SECURITY TESTS PASSED! ===');
}

runTests().catch(err => {
  console.error('TEST RUNNER FAILED:', err);
  process.exit(1);
});
