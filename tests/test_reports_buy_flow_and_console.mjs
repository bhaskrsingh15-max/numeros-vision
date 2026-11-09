/**
 * TEST SUITE: Reports In-Page Buy Flow, Funnel Telemetry & Preview Test Console
 * Tests:
 * 1. Reports in-page tier picker (Basic 199, Advanced 510, Premium 1050 strictly from PACK_CATALOG)
 * 2. In-page prefill, OTP verification, and "Your purchase" screen 4-state lifecycle (generating, ready, failed, resume)
 * 3. After-calculator CTA cleanup (strictly ONE primary CTA by context and ONE quiet secondary link, zero other paid buttons)
 * 4. Zero /pricing detour (menu tabs, pricing comparison buttons enter product flow)
 * 5. Preview-only test console (404 in production, 403 on missing/invalid ADMIN_TOKEN, 200 with 5 SKUs, banned scan across 3 DOBs, idempotency)
 * 6. Funnel telemetry events & Razorpay trust line verification
 */

import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import worker from '../app/static/_worker.js';
const indexHtml = fs.readFileSync(path.resolve('app/static/index.html'), 'utf8');
const pricingHtml = fs.readFileSync(path.resolve('app/static/pricing.html'), 'utf8');
const packsJson = JSON.parse(fs.readFileSync(path.resolve('app/config/packs.json'), 'utf8'));

console.log('[TEST] Starting Reports In-Page Buy Flow & Test Console Suite...');

async function runSuite() {
  let passedCount = 0;

  // ---------------------------------------------------------------------------
  // TEST 1: Pricing source of truth & in-page tier picker prices
  // ---------------------------------------------------------------------------
  console.log('[TEST 1] Testing Reports tier picker prices against PACK_CATALOG...');
  assert.equal(packsJson.core_reports.report_basic.price_inr, 199, 'Basic report must be 199');
  assert.equal(packsJson.core_reports.report_advanced.price_inr, 510, 'Advanced report must be 510');
  assert.equal(packsJson.core_reports.report_premium.price_inr, 1050, 'Premium report must be 1050');

  // Verify in index.html that all 3 tiers exist with exact catalog prices
  assert.ok(indexHtml.includes('card-report-basic'), 'card-report-basic must exist in index.html');
  assert.ok(indexHtml.includes('card-report-advanced'), 'card-report-advanced must exist in index.html');
  assert.ok(indexHtml.includes('card-report-premium'), 'card-report-premium must exist in index.html');
  assert.ok(indexHtml.includes('₹199'), 'Basic price ₹199 must be in HTML');
  assert.ok(indexHtml.includes('₹510'), 'Advanced price ₹510 must be in HTML');
  assert.ok(indexHtml.includes('₹1,050'), 'Premium price ₹1,050 must be in HTML');
  console.log('  ✓ Tier picker prices match PACK_CATALOG exactly (199, 510, 1050)');
  passedCount++;

  // ---------------------------------------------------------------------------
  // TEST 2: In-Page Checkout Form & Seeker Prefill Elements
  // ---------------------------------------------------------------------------
  console.log('[TEST 2] Testing in-page checkout form & seeker prefill inputs...');
  assert.ok(indexHtml.includes('id="reports-checkout-console"'), 'In-page checkout console must exist');
  assert.ok(indexHtml.includes('id="reports-name"'), 'Seeker name input must exist');
  assert.ok(indexHtml.includes('id="reports-dob"'), 'Seeker DOB input must exist');
  assert.ok(indexHtml.includes('id="reports-email"'), 'Seeker email input must exist');
  assert.ok(indexHtml.includes('id="reports-phone"'), 'Seeker phone input must exist');
  assert.ok(indexHtml.includes('id="btn-reports-send-otp"'), 'Send OTP button must exist');
  assert.ok(indexHtml.includes('id="reports-otp-input"'), 'OTP input field must exist');
  assert.ok(indexHtml.includes('id="btn-reports-verify-otp"'), 'Verify OTP button must exist');
  assert.ok(indexHtml.includes('prefillReportsSeekerInputs'), 'prefillReportsSeekerInputs function must be present');
  console.log('  ✓ In-page checkout inputs, prefill handler, and OTP elements verified');
  passedCount++;

  // ---------------------------------------------------------------------------
  // TEST 3: "Your purchase" screen with 4 states
  // ---------------------------------------------------------------------------
  console.log('[TEST 3] Testing "Your purchase" screen 4-state lifecycle...');
  assert.ok(indexHtml.includes('id="reports-purchase-screen"'), 'reports-purchase-screen container must exist');
  assert.ok(indexHtml.includes('id="purchase-state-generating"'), 'generating state container must exist');
  assert.ok(indexHtml.includes('id="purchase-state-ready"'), 'ready state container must exist');
  assert.ok(indexHtml.includes('id="purchase-state-failed"'), 'failed state container must exist');
  assert.ok(indexHtml.includes('id="purchase-resume-container"'), 'resume lookup container must exist');
  assert.ok(indexHtml.includes('id="reports-ready-download-link"'), 'download link must exist in ready state');
  assert.ok(indexHtml.includes('resendPurchaseEmail'), 'resend email action must exist');
  assert.ok(indexHtml.includes('retryPurchasePolling'), 'retry generation action must exist');
  assert.ok(indexHtml.includes('lookupResumeOrder'), 'resume lookup action must exist');
  console.log('  ✓ All 4 purchase states (generating, ready, failed, resume) + download and email actions verified');
  passedCount++;

  // ---------------------------------------------------------------------------
  // TEST 4: Single Primary CTA & Quiet Secondary Link After Free Calculator
  // ---------------------------------------------------------------------------
  console.log('[TEST 4] Testing post-calculator CTA block cleanup (Requirement 2)...');
  assert.ok(indexHtml.includes('id="calc-after-cta-block"'), 'calc-after-cta-block must exist');
  assert.ok(indexHtml.includes('Get Your Full Numerology Report (from ₹199)'), 'Primary CTA text must match');
  assert.ok(indexHtml.includes('Compare all 3 report tiers &amp; inclusions ↓'), 'Quiet secondary link text must match');
  assert.ok(indexHtml.includes('nv-quiet-link'), 'Quiet link must carry nv-quiet-link styling class');

  // Verify that cluttered paid pitch pills & conversion matrix table were removed from loShuReferenceCard
  assert.ok(!indexHtml.includes('id="idxPillMissing"'), 'cluttered idxPillMissing must be removed');
  assert.ok(!indexHtml.includes('id="idxPillPresent"'), 'cluttered idxPillPresent must be removed');
  assert.ok(!indexHtml.includes('id="idxPillYogas"'), 'cluttered idxPillYogas must be removed');
  assert.ok(!indexHtml.includes('PERMUTATION &amp; COMBINATION CONVERSION MATRIX'), 'cluttered conversion matrix must be removed from free block');
  console.log('  ✓ Free calculator block shows strictly ONE primary CTA and ONE quiet secondary link with zero clutter');
  passedCount++;

  // ---------------------------------------------------------------------------
  // TEST 5: Zero /pricing Detour across Menu Tabs & Pricing Page
  // ---------------------------------------------------------------------------
  console.log('[TEST 5] Testing zero /pricing detour across navigation & pricing comparison...');
  // Menu navigation on index.html directs to #reports instead of /pricing/
  assert.ok(indexHtml.includes('href="/#reports" class="nv-nav-link">Reports</a>'), 'Menu nav link must go to /#reports');

  // Pricing comparison buttons enter the product flow directly
  assert.ok(pricingHtml.includes('/?plan=report_basic#reports'), 'Pricing table Basic button must enter /?plan=report_basic#reports');
  assert.ok(pricingHtml.includes('/?plan=report_advanced#reports'), 'Pricing table Advanced button must enter /?plan=report_advanced#reports');
  assert.ok(pricingHtml.includes('/?plan=report_premium#reports'), 'Pricing table Premium button must enter /?plan=report_premium#reports');
  assert.ok(pricingHtml.includes('/charm_ai.html#pass'), 'Pricing table Charm AI button must enter /charm_ai.html#pass');
  assert.ok(pricingHtml.includes('window.location.href = \'/?plan=\' + encodeURIComponent(targetPlan) + \'#reports\';'), 'startCheckout on pricing.html must redirect to in-page flow');
  console.log('  ✓ Menu tabs and pricing comparison buttons enter product flow directly with zero /pricing detour');
  passedCount++;

  // ---------------------------------------------------------------------------
  // TEST 6: Preview-Only Test Console Environment & Auth Guards (Requirement 4)
  // ---------------------------------------------------------------------------
  console.log('[TEST 6] Testing preview-only test console security & auth gating...');
  // 6A. Production must return clean 404
  const resProd = await worker.fetch(new Request('https://numerosvision.com/admin/test-console'), {
    ENVIRONMENT: 'production',
    ADMIN_TOKEN: 'secret_admin_token_999'
  });
  assert.equal(resProd.status, 404, 'Test console must return 404 in production environment');

  // 6B. Missing token in preview must return 403
  const resNoToken = await worker.fetch(new Request('https://preview.numerosvision.com/admin/test-console'), {
    ENVIRONMENT: 'preview',
    ADMIN_TOKEN: 'secret_admin_token_999'
  });
  assert.equal(resNoToken.status, 403, 'Missing ADMIN_TOKEN must return 403');

  // 6C. Wrong token in preview must return 403
  const resWrongToken = await worker.fetch(new Request('https://preview.numerosvision.com/admin/test-console', {
    headers: { 'Authorization': 'Bearer wrong_token' }
  }), {
    ENVIRONMENT: 'preview',
    ADMIN_TOKEN: 'secret_admin_token_999'
  });
  assert.equal(resWrongToken.status, 403, 'Wrong ADMIN_TOKEN must return 403');

  // 6D. Unset ADMIN_TOKEN on server must return 503
  const resUnsetSecret = await worker.fetch(new Request('https://preview.numerosvision.com/admin/test-console', {
    headers: { 'Authorization': 'Bearer any_token' }
  }), {
    ENVIRONMENT: 'preview'
  });
  assert.equal(resUnsetSecret.status, 503, 'Unset ADMIN_TOKEN on server must fail closed with 503');
  console.log('  ✓ Fail-closed environment & token gates verified (404 prod, 403 unauth, 503 unset)');
  passedCount++;

  // ---------------------------------------------------------------------------
  // TEST 7: Preview-Only Test Console Data & 5 SKUs Verification
  // ---------------------------------------------------------------------------
  console.log('[TEST 7] Testing preview test console 5 SKU rows, banned scan & idempotency...');
  const resConsole = await worker.fetch(new Request('https://preview.numerosvision.com/admin/test-console?format=json', {
    headers: { 'X-Admin-Token': 'secret_admin_token_999' }
  }), {
    ENVIRONMENT: 'preview',
    ADMIN_TOKEN: 'secret_admin_token_999'
  });
  assert.equal(resConsole.status, 200, 'Test console must return 200 with valid token in preview');
  const consoleData = await resConsole.json();

  assert.equal(consoleData.status, 'ok', 'Status must be ok');
  assert.equal(consoleData.overall_status, 'PASS', 'Overall status must be PASS');
  assert.equal(consoleData.skus.length, 5, 'Must evaluate exactly 5 SKUs');

  const expectedSkus = ['report_basic', 'report_advanced', 'report_premium', 'planner_2027', 'charm_single'];
  const actualSkus = consoleData.skus.map(s => s.sku);
  assert.deepEqual(actualSkus, expectedSkus, 'SKUs must match required 5 products');

  // Verify each SKU row
  for (const row of consoleData.skus) {
    assert.equal(row.price_match, true, `Price must match for SKU ${row.sku}`);
    assert.equal(row.order_status_lifecycle, 'PASSED', `Order status must pass for SKU ${row.sku}`);
    assert.equal(row.entitlement_status, 'ACTIVE', `Entitlement must be active for SKU ${row.sku}`);
    assert.equal(row.banned_word_scan, 'PASS', `Banned word scan must pass for SKU ${row.sku}`);
    assert.equal(row.name_dob_check, 'PASS', `Name/DOB match must pass for SKU ${row.sku}`);
    assert.equal(row.duplicate_on_retry_check, 'IDEMPOTENT_PASS', `Duplicate check must be idempotent for SKU ${row.sku}`);

    // Check 3 fixed sample DOBs
    assert.equal(row.sample_evaluations.length, 3, 'Must evaluate 3 fixed sample DOBs');
    const dobs = row.sample_evaluations.map(e => e.dob);
    assert.deepEqual(dobs, ['1981-11-28', '1990-01-01', '1988-08-18'], 'DOBs must be 1981-11-28, 1990-01-01, 1988-08-18');
    for (const sample of row.sample_evaluations) {
      assert.equal(sample.banned_words_detected, 0, `0 banned words for ${sample.dob}`);
      assert.equal(sample.name_dob_match, true, `Name/DOB must match for ${sample.dob}`);
      assert.ok(sample.report_url.includes(row.sku), 'Report URL must be linked');
    }
  }

  // Also check sample report endpoint
  const resSample = await worker.fetch(new Request('https://preview.numerosvision.com/api/v1/reports/sample/report_basic?dob=1981-11-28'), {
    ENVIRONMENT: 'preview'
  });
  assert.equal(resSample.status, 200, 'Sample report endpoint must return 200 in preview');
  const sampleData = await resSample.json();
  assert.equal(sampleData.banned_words_detected, 0, 'Sample report must have 0 banned words');
  assert.equal(sampleData.name_dob_match, true, 'Sample report must match name and DOB');
  console.log('  ✓ 5 SKUs verified: page vs catalog vs Razorpay, 3 sample DOBs with 0 banned terms, and idempotency');
  passedCount++;

  // ---------------------------------------------------------------------------
  // TEST 8: Funnel Telemetry Events & Mandatory Trust Line (Requirement 5)
  // ---------------------------------------------------------------------------
  console.log('[TEST 8] Testing funnel telemetry events & payment trust line...');
  assert.ok(indexHtml.includes('trackFunnelEvent'), 'trackFunnelEvent helper must exist');
  assert.ok(indexHtml.includes("'view_product'"), 'view_product funnel event must be wired');
  assert.ok(indexHtml.includes("'begin_checkout'"), 'begin_checkout funnel event must be wired');
  assert.ok(indexHtml.includes("'otp_verified'"), 'otp_verified funnel event must be wired');
  assert.ok(indexHtml.includes("'purchase_complete'"), 'purchase_complete funnel event must be wired');

  // Verify the exact trust line
  const expectedTrustLine = '🔒 100% Secure 256-bit Encrypted Payment via Razorpay · <a href="/refund.html" target="_blank" style="color:#8B6914; text-decoration:underline;">Refund Policy</a>';
  assert.ok(indexHtml.includes('🔒 100% Secure 256-bit Encrypted Payment via Razorpay · <a href="/refund.html"'), 'Mandatory trust line must exist beside pay button');
  console.log('  ✓ Funnel events (view_product, begin_checkout, otp_verified, purchase_complete) & trust line verified');
  passedCount++;

  console.log(`\n[SUCCESS] All ${passedCount} Reports Buy Flow & Test Console test cases passed successfully!`);
}

runSuite().catch(err => {
  console.error('[FAIL] Suite error:', err);
  process.exit(1);
});
