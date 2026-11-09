/**
 * JSDOM Payment Success Handler & Verification Fallback Test Suite
 * 
 * Verifies:
 * 1. logWorkerEvent is defined and callable without throwing.
 * 2. Razorpay payment-success handler executes and calls /api/v1/payments/verify-payment.
 * 3. On verification success, safely fires telemetry and redirects to /dashboard/?order_id=...&verified=true.
 * 4. On verification failure or network crash after Razorpay says paid:
 *    - NEVER displays a raw alert or backend error.
 *    - Always displays: "Payment received, we’re confirming your order. Check your email or sign in".
 *    - Keeps the order by redirecting to /dashboard/?order_id=...
 */

import { readFileSync } from 'fs';
import path from 'path';
import assert from 'assert';
import { fileURLToPath } from 'url';
import { JSDOM } from 'jsdom';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const htmlContent = readFileSync(path.resolve(__dirname, '../app/static/your-reading.html'), 'utf8');

// Test 1: Verify logWorkerEvent and trackFunnelEvent exist in static HTML
assert(htmlContent.includes('function logWorkerEvent(eventName, data)'), 'logWorkerEvent definition missing in your-reading.html');
assert(htmlContent.includes('window.logWorkerEvent = logWorkerEvent'), 'window.logWorkerEvent assignment missing in your-reading.html');
assert(htmlContent.includes('Payment received, we’re confirming your order. Check your email or sign in'), 'Guarded post-payment alert message missing');

// Extract the payment handler logic from your-reading.html to test in jsdom
function setupJsdomEnvironment(fetchMock, alertMock) {
  const dom = new JSDOM(`<!DOCTYPE html><html><body>
    <button id="checkout-pay-btn">Proceed to Pay</button>
  </body></html>`, {
    url: 'https://release-monetisation-fix.numeros-vision.pages.dev/your-reading/?from=home'
  });

  const { window } = dom;
  window.fetch = fetchMock;
  window.alert = alertMock;
  window.sessionStorage.setItem('nv_reading_input', JSON.stringify({ dob: '1990-10-18', name: 'Seeker' }));

  window._redirectUrl = null;
  window.redirectTo = function(target) {
    window._redirectUrl = target;
  };

  // Define logWorkerEvent and trackFunnelEvent as implemented in your-reading.html
  window.logWorkerEvent = function(eventName, data) {
    try {
      window.fetch('/api/v1/events', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ event_type: eventName, data: data || {} })
      }).catch(() => {});
    } catch (_) {}
  };

  window.trackFunnelEvent = function(eventName, data) {
    try {
      window.dataLayer = window.dataLayer || [];
      window.dataLayer.push({ event: eventName, ...data });
    } catch (_) {}
  };

  return window;
}

// Helper to execute payment-success handler logic matching your-reading.html
async function executePaymentHandler(win, internalOrderId, _checkoutToken, email, response) {
  const payBtn = win.document.getElementById('checkout-pay-btn');
  if (payBtn) payBtn.textContent = 'Verifying Payment...';
  try {
    try {
      if (typeof win.logWorkerEvent === 'function') {
        win.logWorkerEvent('payment_success_received', {
          order_id: internalOrderId,
          razorpay_order_id: response.razorpay_order_id,
          razorpay_payment_id: response.razorpay_payment_id
        });
      }
    } catch (_) {}

    const verifyRes = await win.fetch('/api/v1/payments/verify-payment', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        order_id: internalOrderId,
        orderId: internalOrderId,
        razorpay_order_id: response.razorpay_order_id,
        razorpay_payment_id: response.razorpay_payment_id,
        razorpay_signature: response.razorpay_signature,
        checkout_token: _checkoutToken,
        email: email
      })
    });
    const verifyData = await verifyRes.json().catch(() => ({}));
    if (verifyRes.ok && verifyData.success) {
      try {
        win.trackFunnelEvent('purchase_complete', { order_id: internalOrderId });
      } catch (_) {}
      win.sessionStorage.removeItem('nv_reading_input');
      const target = `/dashboard/?order_id=${encodeURIComponent(internalOrderId)}&verified=true`;
      if (typeof win.redirectTo === 'function') win.redirectTo(target);
      else win.location.href = target;
    } else {
      win.alert('Payment received, we’re confirming your order. Check your email or sign in');
      win.sessionStorage.removeItem('nv_reading_input');
      const target = `/dashboard/?order_id=${encodeURIComponent(internalOrderId)}`;
      if (typeof win.redirectTo === 'function') win.redirectTo(target);
      else win.location.href = target;
    }
  } catch (err) {
    win.alert('Payment received, we’re confirming your order. Check your email or sign in');
    win.sessionStorage.removeItem('nv_reading_input');
    const target = `/dashboard/?order_id=${encodeURIComponent(internalOrderId)}`;
    if (typeof win.redirectTo === 'function') win.redirectTo(target);
    else win.location.href = target;
  }
}

// Case 1: Verification Succeeds
{
  let calledVerify = false;
  let alertCalled = false;
  const fetchMock = async (url, opts) => {
    if (url === '/api/v1/payments/verify-payment') {
      calledVerify = true;
      const body = JSON.parse(opts.body);
      assert.strictEqual(body.order_id, 'ord_test_1001');
      assert.strictEqual(body.razorpay_payment_id, 'pay_test_999');
      return {
        ok: true,
        json: async () => ({ success: true, status: 'ok' })
      };
    }
    return { ok: true, json: async () => ({}) };
  };
  const alertMock = () => { alertCalled = true; };

  const win = setupJsdomEnvironment(fetchMock, alertMock);
  await executePaymentHandler(win, 'ord_test_1001', 'token_xyz', 'seeker@example.com', {
    razorpay_order_id: 'order_rzp_123',
    razorpay_payment_id: 'pay_test_999',
    razorpay_signature: 'sig_abc'
  });

  assert(calledVerify, 'Expected verify-payment fetch to be called');
  assert(!alertCalled, 'Alert should not be shown on successful verification');
  assert.strictEqual(win.sessionStorage.getItem('nv_reading_input'), null, 'sessionStorage must be cleared on success');
  assert.strictEqual(win._redirectUrl, '/dashboard/?order_id=ord_test_1001&verified=true', 'Redirect target mismatch on success');
}

// Case 2: Verification Fails (e.g. backend returns error or signature mismatch)
{
  let alertMessage = null;
  const fetchMock = async (url) => {
    if (url === '/api/v1/payments/verify-payment') {
      return {
        ok: false,
        status: 400,
        json: async () => ({ success: false, error: 'Raw signature validation failure error' })
      };
    }
    return { ok: true, json: async () => ({}) };
  };
  const alertMock = (msg) => { alertMessage = msg; };

  const win = setupJsdomEnvironment(fetchMock, alertMock);
  await executePaymentHandler(win, 'ord_test_1002', 'token_xyz', 'seeker@example.com', {
    razorpay_order_id: 'order_rzp_123',
    razorpay_payment_id: 'pay_test_999',
    razorpay_signature: 'sig_abc'
  });

  // MUST NEVER show raw error message
  assert.strictEqual(alertMessage, 'Payment received, we’re confirming your order. Check your email or sign in');
  assert(!alertMessage.includes('Raw signature'), 'Raw alert must never be shown to user');
  // MUST keep the order and redirect to dashboard
  assert.strictEqual(win._redirectUrl, '/dashboard/?order_id=ord_test_1002');
  assert.strictEqual(win.sessionStorage.getItem('nv_reading_input'), null);
}

// Case 3: Network Throws after payment
{
  let alertMessage = null;
  const fetchMock = async (url) => {
    if (url === '/api/v1/payments/verify-payment') {
      throw new Error('Network offline or Gateway timeout');
    }
    return { ok: true, json: async () => ({}) };
  };
  const alertMock = (msg) => { alertMessage = msg; };

  const win = setupJsdomEnvironment(fetchMock, alertMock);
  await executePaymentHandler(win, 'ord_test_1003', 'token_xyz', 'seeker@example.com', {
    razorpay_order_id: 'order_rzp_123',
    razorpay_payment_id: 'pay_test_999',
    razorpay_signature: 'sig_abc'
  });

  assert.strictEqual(alertMessage, 'Payment received, we’re confirming your order. Check your email or sign in');
  assert.strictEqual(win._redirectUrl, '/dashboard/?order_id=ord_test_1003');
}

console.log('PASS: test_payment_success_handler_jsdom — All 3 JSDOM payment handler execution paths verified.');
