/**
 * NUMEROS VISION — COMMIT 6b END-TO-END VERIFICATION SUITE
 * Verifies:
 * 1. Private R2 storage (env.REPORTS_BUCKET) & zero public PDF exposure.
 * 2. Worker calls Python generator service with HMAC-signed, timestamped request (X-NV-Timestamp, X-NV-Signature)
 *    using PDF_SERVICE_SECRET.
 * 3. Generator receives ONLY sanitized viewFor output for (subject, pack), never raw data (dob_enc, phone_enc, phone, email).
 * 4. report_jobs lifecycle: QUEUED -> PROCESSING -> COMPLETED -> DOWNLOADED (set on first signed download).
 * 5. 3 retries then FAILED with an alert in audit_log ('report_job_failed_alert').
 * 6. Signed download token valid for 5 minutes (300s) bound to (user, subject, pack).
 */

import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import worker, {
  encryptField,
  signPdfServiceRequest,
  createSignedDownloadToken,
  verifySignedDownloadToken,
  dispatchReportJob,
  retryPendingReportJobsForUser,
  memoryStore
} from '../app/static/_worker.js';

const TEST_ENV = {
  ENVIRONMENT: 'local',
  RAZORPAY_KEY_ID: 'rzp_test_MOCK_6B',
  RAZORPAY_KEY_SECRET: 'rzp_secret_mock_6b',
  RAZORPAY_WEBHOOK_SECRET: 'rzp_webhook_secret_6b',
  OTP_HMAC_SECRET: '1111111111111111111111111111111111111111111111111111111111111111',
  SESSION_SECRET: '2222222222222222222222222222222222222222222222222222222222222222',
  IP_HASH_SALT: '3333333333333333333333333333333333333333333333333333333333333333',
  DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
  PDF_SERVICE_SECRET: 'fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210',
  DOWNLOAD_TOKEN_SECRET: 'abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789',
  PDF_SERVICE_URL: 'http://internal-pdf-generator.local/internal/v1/render-pdf'
};

// Mock private R2 bucket binding
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
  console.log('=== COMMIT 6b PDF PIPELINE, R2, HMAC & SIGNED DOWNLOAD TESTS ===');

  const r2Bucket = createMockR2Bucket();
  const env = { ...TEST_ENV, REPORTS_BUCKET: r2Bucket };

  // Seed user, session, encrypted subject, and entitlement
  const userId = 'usr_commit6b_1';
  const otherUserId = 'usr_commit6b_2_other';
  const subjectId = 'sbj_commit6b_1';
  const packId = 'report_basic';
  const jobId = 'job_commit6b_1';
  const now = Date.now();

  const dobEnc = await encryptField('1990-08-15', env.DATA_ENCRYPTION_KEY);
  const phoneEnc = await encryptField('+919876543210', env.DATA_ENCRYPTION_KEY);
  const birthTimeEnc = await encryptField('14:30', env.DATA_ENCRYPTION_KEY);

  memoryStore.users.set(userId, {
    id: userId,
    email: 'seeker@example.com',
    phone_hash: 'hash_123',
    phone_enc: phoneEnc,
    created_at: now
  });
  memoryStore.users.set(otherUserId, {
    id: otherUserId,
    email: 'other@example.com',
    phone_hash: 'hash_456',
    phone_enc: phoneEnc,
    created_at: now
  });

  // Create valid session tokens in memoryStore.sessions
  const rawTokenUser1 = 'sess_token_commit6b_user1';
  const tokenHashUser1 = crypto.createHmac('sha256', env.SESSION_SECRET).update(rawTokenUser1).digest('hex');
  memoryStore.sessions.set(tokenHashUser1, {
    id: 'ses_6b_1',
    user_id: userId,
    token_hash: tokenHashUser1,
    expires_at: now + 86400000
  });
  const sessionCookieUser1 = `nv_session=${rawTokenUser1}`;

  const rawTokenUser2 = 'sess_token_commit6b_user2';
  const tokenHashUser2 = crypto.createHmac('sha256', env.SESSION_SECRET).update(rawTokenUser2).digest('hex');
  memoryStore.sessions.set(tokenHashUser2, {
    id: 'ses_6b_2',
    user_id: otherUserId,
    token_hash: tokenHashUser2,
    expires_at: now + 86400000
  });
  const sessionCookieUser2 = `nv_session=${rawTokenUser2}`;

  memoryStore.subjects.set(subjectId, {
    id: subjectId,
    user_id: userId,
    name: 'Aaditya Sharma',
    dob_hash: 'dob_hash_123',
    dob_enc: dobEnc,
    birth_time_enc: birthTimeEnc,
    created_at: now
  });

  memoryStore.entitlements.set(`${userId}_${subjectId}_${packId}`, {
    user_id: userId,
    subject_id: subjectId,
    pack_id: packId,
    order_id: 'ord_commit6b_1',
    granted_at: now
  });

  memoryStore.reportJobs.set(jobId, {
    id: jobId,
    user_id: userId,
    subject_id: subjectId,
    pack_id: packId,
    order_id: 'ord_commit6b_1',
    status: 'QUEUED',
    attempts: 0,
    max_attempts: 3,
    r2_key: null,
    last_error: null,
    created_at: now,
    updated_at: now,
    completed_at: null,
    downloaded_at: null
  });

  // Intercept fetch to verify HMAC signature, timestamp, and viewFor-only payload
  let capturedGeneratorRequest = null;
  const originalFetch = globalThis.fetch;
  globalThis.fetch = async (url, init) => {
    if (String(url) === env.PDF_SERVICE_URL) {
      const rawBody = init.body;
      const tsHeader = init.headers['X-NV-Timestamp'];
      const sigHeader = init.headers['X-NV-Signature'];
      const expectedSig = await signPdfServiceRequest(rawBody, tsHeader, env.PDF_SERVICE_SECRET);
      assert.equal(sigHeader, expectedSig, 'Worker must sign generator request with HMAC-SHA256 using PDF_SERVICE_SECRET');
      assert.ok(Math.abs(Math.floor(Date.now() / 1000) - Number(tsHeader)) <= 5, 'Timestamp must be current');

      const parsed = JSON.parse(rawBody);
      capturedGeneratorRequest = parsed;

      // Return fake valid PDF bytes
      const pdfContent = new TextEncoder().encode('%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n' + 'A'.repeat(250) + '\n%%EOF');
      return new Response(pdfContent, {
        status: 200,
        headers: { 'Content-Type': 'application/pdf' }
      });
    }
    return originalFetch(url, init);
  };

  try {
    // 1. Test QUEUED -> PROCESSING -> COMPLETED & viewFor-only payload
    const jobBefore = memoryStore.reportJobs.get(jobId);
    assert.equal(jobBefore.status, 'QUEUED');

    const dispatchRes = await dispatchReportJob(jobId, env);
    assert.equal(dispatchRes.ok, true);
    assert.equal(dispatchRes.jobStatus, 'COMPLETED');

    // Verify generator received ONLY viewFor output, zero raw data
    assert.ok(capturedGeneratorRequest, 'Generator must have been called');
    assert.equal(capturedGeneratorRequest.job_id, jobId);
    assert.equal(capturedGeneratorRequest.pack_id, packId);
    const rawJsonStr = JSON.stringify(capturedGeneratorRequest);
    assert.ok(!rawJsonStr.includes('dob_enc'), 'dob_enc must NEVER be sent to generator');
    assert.ok(!rawJsonStr.includes('phone_enc'), 'phone_enc must NEVER be sent to generator');
    assert.ok(!rawJsonStr.includes('birth_time_enc'), 'birth_time_enc must NEVER be sent to generator');
    assert.ok(!rawJsonStr.includes('seeker@example.com'), 'user email must NEVER be sent to generator');
    assert.ok(!rawJsonStr.includes('+919876543210'), 'user phone must NEVER be sent to generator');
    assert.equal(capturedGeneratorRequest.view.calculation.conductorDisplay, '33/6');

    const jobAfterComplete = memoryStore.reportJobs.get(jobId);
    assert.equal(jobAfterComplete.status, 'COMPLETED');
    assert.ok(jobAfterComplete.r2_key.startsWith(`reports/${userId}/${subjectId}/${packId}/`));
    assert.ok(r2Bucket.store.has(jobAfterComplete.r2_key), 'PDF must be stored in private R2 bucket');

    console.log('  [PASS] 1. Worker HMAC request, viewFor-only payload, and R2 storage verified');

    // 2. Test 6b(a) & 6b(b): Download endpoint requires valid session matching token user_id + separate DOWNLOAD_TOKEN_SECRET
    const token = await createSignedDownloadToken({
      userId,
      subjectId,
      packId,
      jobId,
      ttlSec: 300
    }, env.DOWNLOAD_TOKEN_SECRET);

    // 2a. Unauthenticated request -> 401
    const unauthDlReq = new Request(`https://numerosvision.com/api/v1/reports/download?token=${encodeURIComponent(token)}`, {
      method: 'GET'
    });
    const unauthDlResp = await worker.fetch(unauthDlReq, env);
    assert.equal(unauthDlResp.status, 401, 'Download without session cookie must return 401');

    // 2b. Session of a different user -> 403
    const wrongUserDlReq = new Request(`https://numerosvision.com/api/v1/reports/download?token=${encodeURIComponent(token)}`, {
      method: 'GET',
      headers: { Cookie: sessionCookieUser2 }
    });
    const wrongUserDlResp = await worker.fetch(wrongUserDlReq, env);
    assert.equal(wrongUserDlResp.status, 403, 'Download with mismatched session user_id must return 403');

    // 2c. Token signed with PDF_SERVICE_SECRET instead of DOWNLOAD_TOKEN_SECRET -> 403
    const wrongSecretToken = await createSignedDownloadToken({
      userId,
      subjectId,
      packId,
      jobId,
      ttlSec: 300
    }, env.PDF_SERVICE_SECRET);
    const wrongSecretDlReq = new Request(`https://numerosvision.com/api/v1/reports/download?token=${encodeURIComponent(wrongSecretToken)}`, {
      method: 'GET',
      headers: { Cookie: sessionCookieUser1 }
    });
    const wrongSecretDlResp = await worker.fetch(wrongSecretDlReq, env);
    assert.equal(wrongSecretDlResp.status, 403, 'Token signed with PDF_SERVICE_SECRET must be rejected by download endpoint');

    // 2d. Valid session matching token user_id + DOWNLOAD_TOKEN_SECRET -> 200 & DOWNLOADED transition
    const dlReq = new Request(`https://numerosvision.com/api/v1/reports/download?token=${encodeURIComponent(token)}`, {
      method: 'GET',
      headers: { Cookie: sessionCookieUser1 }
    });
    const dlResp = await worker.fetch(dlReq, env);
    assert.equal(dlResp.status, 200);
    assert.equal(dlResp.headers.get('Content-Type'), 'application/pdf');
    assert.equal(dlResp.headers.get('X-NV-Job-Status'), 'DOWNLOADED');
    const dlBytes = new Uint8Array(await dlResp.arrayBuffer());
    assert.ok(dlBytes.length > 100);

    const jobAfterDownload = memoryStore.reportJobs.get(jobId);
    assert.equal(jobAfterDownload.status, 'DOWNLOADED', 'Job status must transition to DOWNLOADED on first signed download');
    assert.ok(jobAfterDownload.downloaded_at > 0, 'downloaded_at timestamp must be set');

    console.log('  [PASS] 2. Session-authenticated download (401/403/200), separate DOWNLOAD_TOKEN_SECRET, & DOWNLOADED transition verified');

    // 3. Verify token binding to (user, subject, pack) and 5-minute expiration
    const nowSec = Math.floor(Date.now() / 1000);
    const expiredToken = await createSignedDownloadToken({
      userId,
      subjectId,
      packId,
      jobId,
      nowSec: nowSec - 305,
      ttlSec: 300
    }, env.DOWNLOAD_TOKEN_SECRET);

    const expVerify = await verifySignedDownloadToken(expiredToken, env.DOWNLOAD_TOKEN_SECRET, {}, nowSec);
    assert.equal(expVerify.valid, false, 'Token older than 5 minutes (300s) must be rejected');

    const wrongUserVerify = await verifySignedDownloadToken(token, env.DOWNLOAD_TOKEN_SECRET, { userId: 'usr_other' });
    assert.equal(wrongUserVerify.valid, false, 'Token bound to a different user must be rejected');

    const wrongSubjectVerify = await verifySignedDownloadToken(token, env.DOWNLOAD_TOKEN_SECRET, { subjectId: 'sbj_other' });
    assert.equal(wrongSubjectVerify.valid, false, 'Token bound to a different subject must be rejected');

    const wrongPackVerify = await verifySignedDownloadToken(token, env.DOWNLOAD_TOKEN_SECRET, { packId: 'report_premium' });
    assert.equal(wrongPackVerify.valid, false, 'Token bound to a different pack must be rejected');

    const badQueryReq = new Request(
      `https://numerosvision.com/api/v1/reports/download?token=${encodeURIComponent(token)}&packId=report_premium`,
      { method: 'GET', headers: { Cookie: sessionCookieUser1 } }
    );
    const badQueryResp = await worker.fetch(badQueryReq, env);
    assert.equal(badQueryResp.status, 403, 'Download route must reject mismatched packId with 403');

    console.log('  [PASS] 3. 5-minute token expiration and (user, subject, pack) binding verified');

    // 4. Test 3 retries then FAILED with an alert in audit_log
    const failingJobId = 'job_commit6b_fail3';
    memoryStore.reportJobs.set(failingJobId, {
      id: failingJobId,
      user_id: userId,
      subject_id: subjectId,
      pack_id: packId,
      order_id: 'ord_commit6b_2',
      status: 'QUEUED',
      attempts: 0,
      max_attempts: 3,
      r2_key: null,
      last_error: null,
      created_at: now,
      updated_at: now
    });

    globalThis.fetch = async (url, init) => {
      if (String(url) === env.PDF_SERVICE_URL) {
        return new Response('Internal Generator Error', { status: 500 });
      }
      return originalFetch(url, init);
    };

    // Attempt 1 -> stays QUEUED, attempts = 1
    const att1 = await dispatchReportJob(failingJobId, env);
    assert.equal(att1.ok, false);
    assert.equal(att1.jobStatus, 'QUEUED');
    assert.equal(att1.attempts, 1);
    assert.equal(att1.alertTriggered, false);

    // Attempt 2 -> stays QUEUED, attempts = 2
    const att2 = await dispatchReportJob(failingJobId, env);
    assert.equal(att2.ok, false);
    assert.equal(att2.jobStatus, 'QUEUED');
    assert.equal(att2.attempts, 2);
    assert.equal(att2.alertTriggered, false);

    // Attempt 3 -> transitions to FAILED, attempts = 3, alertTriggered = true
    const att3 = await dispatchReportJob(failingJobId, env);
    assert.equal(att3.ok, false);
    assert.equal(att3.jobStatus, 'FAILED');
    assert.equal(att3.attempts, 3);
    assert.equal(att3.alertTriggered, true);

    const failedJob = memoryStore.reportJobs.get(failingJobId);
    assert.equal(failedJob.status, 'FAILED');
    assert.equal(failedJob.attempts, 3);

    // Verify alert entry in auditLog
    let foundAlert = null;
    for (const logEntry of memoryStore.auditLog.values()) {
      if (logEntry.action === 'report_job_failed_alert' && logEntry.resource_id === failingJobId) {
        foundAlert = logEntry;
        break;
      }
    }
    assert.ok(foundAlert, 'Failed job after 3 retries must write report_job_failed_alert to audit_log');

    console.log('  [PASS] 4. 3 retries -> FAILED + report_job_failed_alert in audit_log verified');

    // 5. Test 6b(c) & 6b(d): Webhook acknowledges first with ctx.waitUntil, and lazy retry on status poll completes a QUEUED job
    globalThis.fetch = async (url, init) => {
      if (String(url) === env.PDF_SERVICE_URL) {
        const pdfContent = new TextEncoder().encode('%PDF-1.4\n1 0 obj\n<< /Type /Catalog >>\nendobj\n' + 'B'.repeat(250) + '\n%%EOF');
        return new Response(pdfContent, { status: 200, headers: { 'Content-Type': 'application/pdf' } });
      }
      return originalFetch(url, init);
    };

    const rzpOrderId = 'order_rzp_6b_waituntil';
    const internalOrderId = 'ord_6b_waituntil';
    memoryStore.orders.set(internalOrderId, {
      id: internalOrderId,
      user_id: userId,
      subject_id: subjectId,
      pack_id: 'report_advanced',
      amount_paise: 51000,
      currency: 'INR',
      rzp_order_id: rzpOrderId,
      status: 'CREATED',
      created_at: now
    });

    const waitUntilPromises = [];
    const mockCtx = {
      waitUntil(promise) {
        waitUntilPromises.push(promise);
      }
    };

    const whBody = JSON.stringify({
      event: 'order.paid',
      event_id: 'evt_6b_waituntil_1',
      payload: {
        order: { entity: { id: rzpOrderId } },
        payment: { entity: { id: 'pay_6b_waituntil_1', amount: 51000, currency: 'INR', order_id: rzpOrderId } }
      }
    });
    const whSig = crypto.createHmac('sha256', env.RAZORPAY_WEBHOOK_SECRET).update(whBody).digest('hex');
    const whReq = new Request('https://numerosvision.com/api/v1/payments/webhook', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-Razorpay-Signature': whSig },
      body: whBody
    });
    const whResp = await worker.fetch(whReq, env, mockCtx);
    assert.equal(whResp.status, 200, 'Webhook must immediately return 200');
    assert.equal(waitUntilPromises.length, 1, 'Webhook must schedule report dispatch via ctx.waitUntil');
    await Promise.all(waitUntilPromises);

    // Seed a transient failed job (status QUEUED, attempts = 1) and verify lazy retry via retryPendingReportJobsForUser
    memoryStore.entitlements.set(`${userId}_${subjectId}_report_premium`, {
      user_id: userId,
      subject_id: subjectId,
      pack_id: 'report_premium',
      order_id: 'ord_6b_lazy',
      granted_at: now
    });
    const retryJobId = 'job_6b_lazy_retry';
    memoryStore.reportJobs.set(retryJobId, {
      id: retryJobId,
      user_id: userId,
      subject_id: subjectId,
      pack_id: 'report_premium',
      order_id: 'ord_6b_lazy',
      status: 'QUEUED',
      attempts: 1,
      max_attempts: 3,
      r2_key: null,
      last_error: 'transient timeout',
      created_at: now - 30000,
      updated_at: now - 30000
    });
    const retryRes = await retryPendingReportJobsForUser(userId, env, null);
    assert.equal(retryRes.length, 1, 'Lazy retry must pick up and retry the QUEUED job with attempts < 3');
    assert.equal(memoryStore.reportJobs.get(retryJobId).status, 'COMPLETED', 'Lazy retry must complete the job');

    console.log('  [PASS] 5. Webhook ctx.waitUntil dispatch & lazy retry for failed/queued jobs verified');

    // 6. Test 6b(e): Required-secrets guard in production for PDF_SERVICE_URL and DOWNLOAD_TOKEN_SECRET
    const prodMissingUrlEnv = { ...env, ENVIRONMENT: 'production', DB: {}, PDF_SERVICE_URL: undefined, PDF_GENERATOR_URL: undefined };
    const createOrderReq = new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Cookie: sessionCookieUser1 },
      body: JSON.stringify({ packId: 'report_basic', subjectId })
    });
    const createOrderResp = await worker.fetch(createOrderReq, prodMissingUrlEnv);
    assert.equal(createOrderResp.status, 503, 'Missing PDF_SERVICE_URL in production must return 503');

    const prodMissingDlSecretEnv = { ...env, ENVIRONMENT: 'production', DB: {}, DOWNLOAD_TOKEN_SECRET: undefined };
    const createOrderResp2 = await worker.fetch(new Request('https://numerosvision.com/api/v1/payments/create-order', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Cookie: sessionCookieUser1 },
      body: JSON.stringify({ packId: 'report_basic', subjectId })
    }), prodMissingDlSecretEnv);
    assert.equal(createOrderResp2.status, 503, 'Missing DOWNLOAD_TOKEN_SECRET in production must return 503');

    console.log('  [PASS] 6. Required-secrets guard for PDF_SERVICE_URL and DOWNLOAD_TOKEN_SECRET verified');
    console.log('ALL COMMIT 6b TESTS PASSED!');
  } finally {
    globalThis.fetch = originalFetch;
  }
}

runTests().catch(err => {
  console.error(err);
  process.exit(1);
});
