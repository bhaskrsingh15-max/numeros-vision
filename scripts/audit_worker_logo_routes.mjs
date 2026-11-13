/**
 * NUMEROS VISION — Step 1 Production Cloudflare Worker Route Audit
 * Tests `/api/v1/logo/preview` and `/api/v1/logo/analyze-existing` directly against
 * the production Cloudflare Pages Worker (`app/static/_worker.js`) across all 10 sample logos.
 */

import fs from 'node:fs';
import path from 'node:path';
import worker from '../app/static/_worker.js';

const TEST_ENV = {
  ENVIRONMENT: 'production',
  RAZORPAY_KEY_ID: 'rzp_test_step1',
  RAZORPAY_KEY_SECRET: 'rzp_secret_step1',
  RAZORPAY_WEBHOOK_SECRET: 'rzp_wh_step1',
  OTP_HMAC_SECRET: '1111111111111111111111111111111111111111111111111111111111111111',
  SESSION_SECRET: '2222222222222222222222222222222222222222222222222222222222222222',
  IP_HASH_SALT: '3333333333333333333333333333333333333333333333333333333333333333',
  DATA_ENCRYPTION_KEY: '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
  PDF_SERVICE_SECRET: 'fedcba9876543210fedcba9876543210fedcba9876543210fedcba9876543210',
  DOWNLOAD_TOKEN_SECRET: 'abcdef0123456789abcdef0123456789abcdef0123456789abcdef0123456789',
  PDF_SERVICE_URL: 'http://127.0.0.1:8090/internal/v1/render-pdf',
  ASSETS: {
    async fetch() {
      // Simulate Cloudflare Pages static asset fallback behavior: POST to non-worker route -> 405 Method Not Allowed
      return new Response(null, { status: 405, headers: { Allow: 'GET, HEAD' } });
    }
  }
};

async function probeEndpoint(urlPath, payloadObj) {
  const req = new Request(`https://numerosvision.com${urlPath}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
    body: JSON.stringify(payloadObj)
  });
  const res = await worker.fetch(req, TEST_ENV, { waitUntil() {} });
  const bodyText = await res.text();
  return {
    status: res.status,
    contentType: res.headers.get('content-type') || '',
    bodyLength: bodyText.length,
    bodyPreview: bodyText.slice(0, 160)
  };
}

async function main() {
  const manifestPath = process.argv[2];
  if (!manifestPath || !fs.existsSync(manifestPath)) {
    console.error('Usage: node scripts/audit_worker_logo_routes.mjs <manifest.json>');
    process.exit(1);
  }
  const samples = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
  const results = [];

  for (const sample of samples) {
    const previewRes = await probeEndpoint('/api/v1/logo/preview', sample.preview_payload);
    const analyzeRes = await probeEndpoint('/api/v1/logo/analyze-existing', sample.analyze_payload);
    results.push({
      id: sample.id,
      format: sample.format,
      preview: previewRes,
      analyze_existing: analyzeRes
    });
  }

  process.stdout.write(JSON.stringify(results, null, 2));
  process.exit(0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
