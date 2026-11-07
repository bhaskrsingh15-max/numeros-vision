/**

 * NUMEROS VISION — PRODUCTION PAYMENT GATEWAY CONTROLLER

 * Supports Razorpay (UPI, Google Pay, PhonePe, Cards, Netbanking) & Direct Invoicing

 * Version: 2.1.0 (Commit 4 - Server-Authoritative Orders & Pre-Payment Confirmation)

 */

(function(window) {

  'use strict';

  function loadRazorpaySdk() {

    return new Promise((resolve) => {

      if (window.Razorpay) {

        return resolve(true);

      }

      const script = document.createElement('script');

      script.src = 'https://checkout.razorpay.com/v1/checkout.js';

      script.async = true;

      script.onload = () => resolve(true);

      script.onerror = () => {

        console.warn('Razorpay SDK failed to load from CDN. Fallback active.');

        resolve(false);

      };

      document.head.appendChild(script);

    });

  }

  if (typeof window !== 'undefined') {

    if (window.requestIdleCallback) {

      window.requestIdleCallback(() => loadRazorpaySdk());

    } else {

      setTimeout(loadRazorpaySdk, 2000);

    }

  }

  const NumerosPay = {

    /**

     * Show pre-payment DOB confirmation modal before opening checkout.

     */

    showDobConfirmationModal(opts, onConfirmed) {

      const modalId = 'nvDobConfirmModal';

      let existingModal = document.getElementById(modalId);

      if (existingModal) existingModal.remove();

      const customerName = (opts.customer_name || opts.name || 'Valued Seeker').trim();

      const customerDob = (opts.customer_dob || opts.dob || opts.locked_dob || '').trim();

      const modal = document.createElement('div');

      modal.id = modalId;

      modal.style.cssText = 'position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(42,32,20,0.65); backdrop-filter:blur(4px); display:flex; align-items:center; justify-content:center; z-index:9999999; padding:16px;';

      modal.innerHTML = `

        <div style="background:#FFFDF7; border:2px solid #C9A227; border-radius:14px; max-width:440px; width:100%; padding:24px; box-shadow:0 12px 36px rgba(0,0,0,0.25); font-family:system-ui,-apple-system,sans-serif; color:#523E28;">

          <h3 style="margin:0 0 10px 0; color:#8B6914; font-size:1.15rem; font-weight:700; display:flex; align-items:center; gap:8px;">

            <span>🔒</span> Confirm Seeker Details

          </h3>

          <p style="font-size:0.82rem; line-height:1.45; margin:0 0 14px 0; color:#7A654D;">

            Your calculations, personal dasha timing, and executive blueprints are deterministically bound to your exact Date of Birth.

          </p>

          <div style="background:#FAF6EE; border:1px solid rgba(201,162,39,0.3); border-radius:8px; padding:12px; margin-bottom:14px; font-size:0.86rem;">

            <div style="margin-bottom:6px;"><strong style="color:#8B6914;">Full Name:</strong> <span style="font-weight:600;">${customerName}</span></div>

            <div><strong style="color:#8B6914;">Date of Birth:</strong> <span style="font-weight:700; color:#16835B;">${customerDob || 'Not specified'}</span></div>

          </div>

          <div style="font-size:0.73rem; color:#8B6914; margin-bottom:18px; line-height:1.35; background:#FFF9E6; padding:8px 10px; border-radius:6px; border-left:3px solid #C9A227;">

            ⚠️ <em>Please review carefully. A one-time DOB correction is permitted within 24 hours of registration.</em>

          </div>

          <div style="display:flex; justify-content:flex-end; gap:10px;">

            <button id="nvCancelConfirmBtn" type="button" style="background:#F7F3EA; border:1px solid #7A654D; color:#523E28; padding:8px 14px; border-radius:8px; font-size:0.82rem; cursor:pointer; font-weight:600;">

              Edit Details

            </button>

            <button id="nvProceedConfirmBtn" type="button" style="background:#8B6914; border:none; color:#FFFFFF; padding:8px 18px; border-radius:8px; font-size:0.82rem; cursor:pointer; font-weight:700; box-shadow:0 2px 6px rgba(139,105,20,0.3);">

              Confirm &amp; Proceed to Pay →

            </button>

          </div>

        </div>

      `;

      document.body.appendChild(modal);

      document.getElementById('nvCancelConfirmBtn').onclick = () => {

        modal.remove();

        if (opts.onFailure) opts.onFailure({ status: 'cancelled_by_user' });

      };

      document.getElementById('nvProceedConfirmBtn').onclick = () => {

        modal.remove();

        try {

          sessionStorage.removeItem('nv_pending_subject');

        } catch (e) {}

        onConfirmed();

      };

    },

    /**

     * Launch payment checkout for any report or consultation.

     */

    async openCheckout(opts) {

      const planId = opts.plan_id || opts.pack_id || opts.plan || 'report_basic';

      const customerName = (opts.customer_name || opts.name || '').trim();

      const customerEmail = (opts.customer_email || opts.email || '').trim();

      const customerPhone = (opts.customer_phone || opts.phone || '').trim();

      let customerDob = (opts.customer_dob || opts.dob || opts.locked_dob || '').trim();

      // If DOB not provided directly, check sessionStorage

      if (!customerDob) {

        try {

          const pending = JSON.parse(sessionStorage.getItem('nv_pending_subject') || '{}');

          if (pending.dob) customerDob = pending.dob;

        } catch (e) {}

      }

      // Pre-payment DOB confirmation screen

      if (customerDob && !opts.skip_dob_modal) {

        opts.customer_dob = customerDob;

        NumerosPay.showDobConfirmationModal(opts, () => {

          NumerosPay._executeOrderCreationAndCheckout(opts);

        });

      } else {

        NumerosPay._executeOrderCreationAndCheckout(opts);

      }

    },

    async _executeOrderCreationAndCheckout(opts) {

      const planId = opts.plan_id || opts.pack_id || opts.plan || 'report_basic';

      const customerName = (opts.customer_name || opts.name || 'Valued Seeker').trim();

      const customerEmail = (opts.customer_email || opts.email || '').trim();

      const customerPhone = (opts.customer_phone || opts.phone || '').trim();

      const customerDob = (opts.customer_dob || opts.dob || opts.locked_dob || '').trim();

      const subjectId = opts.subjectId || opts.subject_id || '';

      // Step 1: Create Order via Canonical Edge API (/api/v1/payments/create-order)

      let orderData = null;

      try {

        const orderRes = await fetch('/api/v1/payments/create-order', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json' },

          body: JSON.stringify({

            packId: planId,

            subjectId: subjectId,

            name: customerName,

            dob: customerDob,

            email: customerEmail,

            phone: customerPhone

          })

        });

        if (orderRes.ok) {

          orderData = await orderRes.json();

        } else {

          const errData = await orderRes.json().catch(() => ({}));

          console.warn('Order creation failed on backend:', errData);

          if (orderRes.status === 503 || (errData && errData.code === 'CHECKOUT_TEMPORARILY_UNAVAILABLE')) {

            alert('Checkout Temporarily Unavailable:\n\n' + ((errData && errData.error) || 'Checkout is temporarily unavailable while server maintenance completes. Please try again shortly.'));

            if (opts.onFailure) opts.onFailure(errData);

            return;

          }

          if (orderRes.status === 401) {

            // Unauthenticated: store pending state in sessionStorage and redirect to login

            sessionStorage.setItem('nv_pending_subject', JSON.stringify({

              name: customerName,

              dob: customerDob,

              email: customerEmail,

              phone: customerPhone,

              planId: planId

            }));

            window.location.href = '/login?returnTo=/dashboard/';

            return;

          }

          const msg = (errData && errData.error) || 'Checkout is temporarily unavailable. Please try again shortly.';

          alert('Payment Notice:\n\n' + msg);

          if (opts.onFailure) opts.onFailure(errData);

          return;

        }

      } catch (err) {

        console.warn('Backend order creation network exception:', err);

        alert('Network Notice:\n\nUnable to reach payment gateway. Please verify your connection.');

        if (opts.onFailure) opts.onFailure(err);

        return;

      }

      if (!orderData || !orderData.rzpOrderId) {

        alert('Payment Notice:\n\nFailed to obtain a valid order ID from the payment gateway.');

        if (opts.onFailure) opts.onFailure({ error: 'Order creation failed' });

        return;

      }

      // Step 2: Ensure Razorpay SDK is ready

      await loadRazorpaySdk();

      if (!window.Razorpay) {

        alert('Payment gateway SDK could not be loaded. Please disable ad-blockers and refresh.');

        if (opts.onFailure) opts.onFailure({ error: 'SDK load failed' });

        return;

      }

      // Step 3: Launch Razorpay Standard Checkout Modal

      const options = {

        key: orderData.keyId,

        amount: orderData.amount,

        currency: orderData.currency || 'INR',

        name: 'NUMEROS VISION',

        description: orderData.pack ? orderData.pack.name : 'Personal Numerology Dossier',

        image: '/apple-touch-icon.png',

        order_id: orderData.rzpOrderId,

        prefill: {

          name: customerName,

          email: customerEmail,

          contact: customerPhone

        },

        theme: {

          color: '#8B6914'

        },

        handler: async function(response) {

          await NumerosPay._completePaymentVerification({

            order_id: response.razorpay_order_id || orderData.rzpOrderId,

            payment_id: response.razorpay_payment_id,

            signature: response.razorpay_signature,

            plan_id: planId,

            plan_name: orderData.pack ? orderData.pack.name : 'Numerology Report',

            amount_inr: (orderData.amount / 100),

            customer_name: customerName,

            customer_email: customerEmail,

            customer_phone: customerPhone,

            customer_dob: customerDob,

            subject_id: orderData.subjectId,

            onSuccess: opts.onSuccess

          });

        },

        modal: {

          ondismiss: function() {

            if (opts.onFailure) opts.onFailure({ status: 'dismissed' });

          }

        }

      };

      try {

        const rzp = new window.Razorpay(options);

        rzp.on('payment.failed', function(resp) {

          alert('Payment Failed: ' + (resp.error ? resp.error.description : 'Transaction not completed.'));

          if (opts.onFailure) opts.onFailure(resp.error);

        });

        rzp.open();

      } catch (sdkErr) {

        console.error('Error invoking Razorpay instance:', sdkErr);

        if (opts.onFailure) opts.onFailure(sdkErr);

      }

    },

    /**

     * Server-side signature verification & report preparation notice.

     */

    async _completePaymentVerification(params) {

      try {

        const verifyRes = await fetch('/api/v1/payments/verify', {

          method: 'POST',

          headers: { 'Content-Type': 'application/json' },

          body: JSON.stringify({

            razorpay_order_id: params.order_id,

            razorpay_payment_id: params.payment_id,

            razorpay_signature: params.signature

          })

        });

        if (!verifyRes.ok) {

          const errData = await verifyRes.json().catch(() => ({}));

          console.error('[Payment_Verify_Failed]', errData);

          alert('Security Verification Notice:\n\nPayment verification failed on the server. Please contact support.');

          return;

        }

        const verifyData = await verifyRes.json();

        // Show official report preparation modal

        NumerosPay.showReportPreparingModal({

          payment_id: params.payment_id,

          order_id: params.order_id,

          plan_name: params.plan_name,

          amount_inr: params.amount_inr,

          customer_email: params.customer_email

        });

        if (params.onSuccess) params.onSuccess(verifyData);

      } catch (err) {

        console.error('[Payment_Verification_Exception]', err);

        alert('Verification Notice:\n\nUnable to verify payment signature with server. Please refresh your dashboard.');

      }

    },

    /**

     * Displays modal showing report being prepared.

     */

    showReportPreparingModal(inv) {

      let modal = document.getElementById('nvPaymentSuccessModal');

      if (!modal) {

        modal = document.createElement('div');

        modal.id = 'nvPaymentSuccessModal';

        modal.style.cssText = 'position:fixed; top:0; left:0; width:100vw; height:100vh; background:rgba(42,32,20,0.7); backdrop-filter:blur(5px); display:flex; align-items:center; justify-content:center; z-index:9999999; padding:16px;';

        document.body.appendChild(modal);

      }

      modal.innerHTML = `

        <div style="background:#FFFDF7; border:2px solid #C9A227; border-radius:14px; max-width:440px; width:100%; padding:26px; text-align:center; box-shadow:0 12px 36px rgba(0,0,0,0.25); font-family:system-ui,-apple-system,sans-serif; color:#523E28;">

          <div style="width:56px; height:56px; background:#FAF3E0; border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 14px auto; font-size:1.6rem; color:#8B6914;">

            ⏳

          </div>

          <h3 style="margin:0 0 8px 0; color:#8B6914; font-size:1.2rem; font-weight:700;">

            Payment Confirmed

          </h3>

          <p style="font-size:0.86rem; color:#7A654D; margin:0 0 16px 0; line-height:1.45;">

            Your payment of <strong>₹${inv.amount_inr}</strong> has been verified. Your personalized executive report is now being prepared by the calculation engine.

          </p>

          <div style="background:#FAF6EE; border:1px solid rgba(201,162,39,0.3); border-radius:8px; padding:12px; margin-bottom:18px; text-align:left; font-size:0.80rem; line-height:1.5;">

            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">

              <span style="color:#7A654D;">Order Reference:</span>

              <strong style="color:#523E28;">${inv.order_id}</strong>

            </div>

            <div style="display:flex; justify-content:space-between; margin-bottom:4px;">

              <span style="color:#7A654D;">Payment ID:</span>

              <code style="font-size:0.75rem;">${inv.payment_id}</code>

            </div>

            <div style="display:flex; justify-content:space-between;">

              <span style="color:#7A654D;">Status:</span>

              <strong style="color:#16835B;">Report Being Prepared</strong>

            </div>

          </div>

          <div style="display:flex; gap:10px;">

            <a href="/dashboard/" style="flex:1; background:#8B6914; color:#FFFFFF; text-decoration:none; padding:11px 16px; border-radius:8px; font-weight:700; font-size:0.86rem; display:inline-block;">

              Go to Dashboard →

            </a>

            <button type="button" onclick="document.getElementById('nvPaymentSuccessModal').style.display='none'" style="flex:1; background:#F4EFE6; border:none; color:#523E28; padding:11px 16px; border-radius:8px; font-weight:600; font-size:0.86rem; cursor:pointer;">

              Close

            </button>

          </div>

        </div>

      `;

      modal.style.display = 'flex';

    }

  };

  window.NumerosPay = NumerosPay;

  window.NVPaymentGateway = {

    initiateCheckout: function(opts) { return NumerosPay.openCheckout(opts); },

    openCheckout: function(opts) { return NumerosPay.openCheckout(opts); }

  };

})(typeof window !== 'undefined' ? window : this);

