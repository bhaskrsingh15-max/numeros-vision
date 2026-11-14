/**
 * Production 404 Security Gate Suite for Preview QA Sign-In & /api/admin/test-console
 * ===================================================================================
 * Proves that `/admin/test-console`, `/api/admin/test-console`, and all QA actions
 * (`preview_qa_signin`, `preview_qa_sign_test_payment`, `preview_qa_order_audit`,
 * `preview_qa_pdf_diag`) unconditionally return HTTP 404 when `ENVIRONMENT=production`
 * (case-insensitively, or when `ENVIRONMENT` is unset/empty), REGARDLESS of whether
 * valid `ADMIN_TOKEN`, `ADMIN_BEARER_TOKEN`, `PREVIEW_QA_SECRET` HMAC signature, or
 * `rzp_test_*` keys are supplied.
 */

import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import worker from '../app/static/_worker.js';

function hmacHex(secret, message) {
  return crypto.createHmac('sha256', secret).update(message, 'utf8').digest('hex');
}

async function runTests() {
  const adminToken = 'super_valid_admin_token_for_test_404_check';
  const previewQaSecret = 'super_valid_preview_qa_hmac_secret_404_check';
  const nowSec = Math.floor(Date.now() / 1000);

  const envVariants = [
    { label: 'ENVIRONMENT=production', ENVIRONMENT: 'production' },
    { label: 'ENVIRONMENT=PRODUCTION (uppercase)', ENVIRONMENT: 'PRODUCTION' },
    { label: 'ENVIRONMENT=" production " (padded)', ENVIRONMENT: ' production ' },
    { label: 'ENVIRONMENT="" (empty)', ENVIRONMENT: '' },
    { label: 'ENVIRONMENT=undefined (unset)', ENVIRONMENT: undefined },
    { label: 'ENVIRONMENT=staging (unknown)', ENVIRONMENT: 'staging' }
  ];

  const qaPayloads = [
    JSON.stringify({ action: 'preview_qa_signin', email: 'qa@numerosvision.com' }),
    JSON.stringify({
      action: 'preview_qa_sign_test_payment',
      rzp_order_id: 'order_test123',
      rzp_payment_id: 'pay_test123',
      raw_webhook_json: '{}'
    }),
    JSON.stringify({ action: 'preview_qa_order_audit', order_id: 'ord_123' }),
    JSON.stringify({ action: 'preview_qa_pdf_diag' })
  ];

  let assertionsCount = 0;

  for (const variant of envVariants) {
    const env = {
      ...(variant.ENVIRONMENT !== undefined ? { ENVIRONMENT: variant.ENVIRONMENT } : {}),
      ADMIN_TOKEN: adminToken,
      ADMIN_BEARER_TOKEN: adminToken,
      PREVIEW_QA_SECRET: previewQaSecret,
      RAZORPAY_KEY_ID: 'rzp_test_validtestkey123',
      RAZORPAY_KEY_SECRET: 'rzp_test_validsecret456',
      RAZORPAY_WEBHOOK_SECRET: 'whsec_validsecret789',
      SESSION_SECRET: 'sess_secret_32_bytes_minimum_length_ok!!',
      IP_HASH_SALT: 'ip_salt_32_bytes_minimum_length_ok!!'
    };

    // 1. GET /admin/test-console and /api/admin/test-console (with & without trailing slash)
    //    carrying valid Bearer token, X-Admin-Token, AND valid QA HMAC signature
    const getSig = hmacHex(previewQaSecret, `${nowSec}.`);
    for (const route of [
      '/admin/test-console',
      '/admin/test-console/',
      '/api/admin/test-console',
      '/api/admin/test-console/',
      '/api/admin/test-console?format=json'
    ]) {
      const resGet = await worker.fetch(
        new Request(`https://numerosvision.com${route}`, {
          method: 'GET',
          headers: {
            Accept: 'application/json',
            Authorization: `Bearer ${adminToken}`,
            'X-Admin-Token': adminToken,
            'X-NV-QA-Timestamp': String(nowSec),
            'X-NV-QA-Signature': getSig
          }
        }),
        env,
        {}
      );
      assert.equal(
        resGet.status,
        404,
        `[${variant.label}] GET ${route} with all valid secrets must return 404, got ${resGet.status}`
      );
      const textGet = await resGet.text();
      assert.equal(textGet, 'Not Found');
      assertionsCount++;
    }

    // 2. POST /api/admin/test-console (including preview_qa_signin) with:
    //    (a) valid ADMIN_TOKEN only
    //    (b) valid PREVIEW_QA_SECRET HMAC signature only
    //    (c) BOTH valid ADMIN_TOKEN and valid PREVIEW_QA_SECRET HMAC signature
    for (const rawBody of qaPayloads) {
      const postSig = hmacHex(previewQaSecret, `${nowSec}.${rawBody}`);
      const headerSets = [
        {
          name: 'Bearer ADMIN_TOKEN',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${adminToken}`
          }
        },
        {
          name: 'Valid PREVIEW_QA_SECRET HMAC',
          headers: {
            'Content-Type': 'application/json',
            'X-NV-QA-Timestamp': String(nowSec),
            'X-NV-QA-Signature': postSig
          }
        },
        {
          name: 'Both X-Admin-Token + Valid PREVIEW_QA_SECRET HMAC',
          headers: {
            'Content-Type': 'application/json',
            'X-Admin-Token': adminToken,
            Authorization: `Bearer ${adminToken}`,
            'X-NV-QA-Timestamp': String(nowSec),
            'X-NV-QA-Signature': postSig
          }
        }
      ];

      for (const hs of headerSets) {
        for (const postRoute of ['/api/admin/test-console', '/api/admin/test-console/', '/admin/test-console']) {
          const resPost = await worker.fetch(
            new Request(`https://numerosvision.com${postRoute}`, {
              method: 'POST',
              headers: hs.headers,
              body: rawBody
            }),
            env,
            {}
          );
          assert.equal(
            resPost.status,
            404,
            `[${variant.label}] POST ${postRoute} (${hs.name}, ${rawBody}) must return 404, got ${resPost.status}`
          );
          assert.equal(
            resPost.headers.get('Set-Cookie'),
            null,
            `[${variant.label}] POST ${postRoute} must NEVER mint a session cookie in production`
          );
          const bodyText = await resPost.text();
          assert.equal(bodyText, 'Not Found');
          assertionsCount++;
        }
      }
    }
  }

  // Positive control: prove the exact same signed preview_qa_signin request succeeds (200) ONLY when ENVIRONMENT=preview
  const previewBody = JSON.stringify({ action: 'preview_qa_signin', email: 'qa@numerosvision.com' });
  const previewSig = hmacHex(previewQaSecret, `${nowSec}.${previewBody}`);
  const previewRes = await worker.fetch(
    new Request('https://preview.numeros-vision.pages.dev/api/admin/test-console', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-NV-QA-Timestamp': String(nowSec),
        'X-NV-QA-Signature': previewSig
      },
      body: previewBody
    }),
    {
      ENVIRONMENT: 'preview',
      ADMIN_TOKEN: adminToken,
      PREVIEW_QA_SECRET: previewQaSecret,
      RAZORPAY_KEY_ID: 'rzp_test_validtestkey123',
      SESSION_SECRET: 'sess_secret_32_bytes_minimum_length_ok!!',
      IP_HASH_SALT: 'ip_salt_32_bytes_minimum_length_ok!!'
    },
    {}
  );
  assert.equal(previewRes.status, 200, 'Control check: valid HMAC on ENVIRONMENT=preview must return 200');

  console.log(
    `PASS: ${assertionsCount} production/non-preview combinations verified -> 404 Not Found with zero cookies regardless of any key or secret.`
  );
}

runTests().catch((err) => {
  console.error('FAIL:', err);
  process.exit(1);
});
