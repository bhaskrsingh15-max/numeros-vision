# NUMEROS VISION — 2027 YEAR AHEAD PLANNER PREVIEW SMOKE-TEST KIT
**Document Version**: 1.0.0  
**Target Environment**: Cloudflare Pages (Preview Deployment) & Cloud Run Generator (`pdf_service`)  
**Gate**: Phase 3 Preview Only (Strictly zero production release, strictly test keys)

---

## 1. Safety & Compliance Directives

1. **Test Keys Only**: Never configure or enter live credentials. The application contains hard-coded barriers (`assert_no_live_razorpay_keys` and worker checks) that abort immediately if any key starts with `rzp_live`.
2. **Deterministic Server Authority**: Pricing is locked server-side at ₹1,499 (149,900 paise) until 31 January 2027 23:59 IST. Client price tampering is automatically rejected.
3. **Fail-Closed Protection**: If any unapproved placeholder (such as `{{DISCLAIMER_APPROVED_TEXT}}`) remains in a paid PDF, generation halts with HTTP 422, the order is marked `needs_attention`, and no PDF is released.
4. **Statutory Consent**: The DPDP 2023 consent checkbox is required to proceed.

---

## 2. Operator Setup: Required Preview Environment Secrets

Configure these environment variables in the **Cloudflare Pages Dashboard** under **Settings → Environment Variables → Preview**:

| Variable Name | Environment | Description |
| :--- | :--- | :--- |
| `RAZORPAY_KEY_ID` | Preview | Razorpay Test Key ID (e.g. `rzp_test_...`) |
| `RAZORPAY_KEY_SECRET` | Preview | Razorpay Test Key Secret |
| `RAZORPAY_WEBHOOK_SECRET` | Preview | Secret for signature verification on `/api/planner-2027/webhook` |
| `PDF_SERVICE_URL` | Preview | URL of the internal Cloud Run PDF service (or tunnel) |
| `PDF_SERVICE_SECRET` | Preview | 32+ character HMAC secret matching `PDF_SERVICE_SECRET` on Cloud Run |
| `ADMIN_BEARER_TOKEN` | Preview | High-entropy secret for querying `/api/planner-2027/admin/stuck-orders` |
| `DB` (D1 Binding) | Preview | D1 Database binding to `planner_2027_orders` table |

### Razorpay Test Dashboard Webhook Configuration
1. Open the [Razorpay Dashboard](https://dashboard.razorpay.com/) in **Test Mode**.
2. Navigate to **Settings → Webhooks → Add New Webhook**.
3. **Webhook URL**: `https://<your-preview-domain>/api/planner-2027/webhook`
4. **Secret**: Enter the exact string used in `RAZORPAY_WEBHOOK_SECRET`.
5. **Active Events**: Check `payment.captured`.
6. Save the webhook.

---

## 3. Manual Verification Checklist (7 Test Flows)

### Flow 1: Fresh Purchase & Instant PDF Delivery
1. Open `https://<your-preview-domain>/year_2027.html` in an incognito browser window.
2. Verify page aesthetics:
   - Header: Master header with `NUMEROS VISION` and `ANVEIL EVERY CHARM`.
   - Price box: Displays `₹1,499` with strikethrough `₹1,999` and note `"Offer ends 31 January 2027"`. Zero GST or tax claims.
   - Sample preview section: Disabled buttons showing `"Sample preview coming soon"`.
   - Sample labels:
     - `Sample A: Arun Sharma (Mulank 1, Bhagyank 4, Personal Year 5)`
     - `Sample B: Anil Kumar (Mulank 1, Bhagyank 1, Personal Year 8)`
3. Scroll to the order form. Fill in details:
   - **Full Name**: `Arun Sharma`
   - **Date of Birth**: `1980-01-01`
   - **Email**: `your-test-email@example.com`
   - **DPDP Consent**: Check the mandatory consent box.
4. Click **Proceed to Secure Checkout (₹1,499)**.
5. In the Razorpay modal:
   - Select **Card**.
   - Use Test Card Number: `4111 1111 1111 1111`
   - Expiry: Any future date (e.g. `12/28`), CVV: `123`.
   - Click Pay. Enter OTP `123456` if prompted.
6. Verify result:
   - The green alert `"Payment Verified! Your 2027 Year Ahead Planner is ready"` appears.
   - Click **Download 2027 Year Ahead Planner (PDF)**.
   - Confirm the 24-page PDF downloads and opens cleanly.

---

### Flow 2: Double-Trigger Concurrency Race (Webhook + /verify)
To confirm the database atomicity handles simultaneous webhook and client redirects without duplicating PDF generations:
1. Trigger `/api/planner-2027/order` to create an order.
2. Send simultaneous `/verify` and `/webhook` requests with the same payment credentials.
3. Query order status:
   - `status` must transition cleanly to `delivered`.
   - `generation_count` must be exactly `1`.
   - (Verified automatically in automated test suite `tests/test_planner_2027_worker.mjs` Test 7).

---

### Flow 3: Browserless Link Recovery (`/resend-link`)
Simulates a buyer who closed their browser tab immediately after payment:
1. On `https://<your-preview-domain>/year_2027.html`, scroll to **Already Ordered? Retrieve Your Download Link**.
2. Enter the **Order ID** from Flow 1 (`ord_p27_...`) and the matching email address.
3. Click **Retrieve Download Link**.
4. Confirm the success message displays an active download link.
5. Now test mismatch: change the email to an unregistered address.
6. Confirm error: `"Could not find a matching order"` (HTTP 404, zero PII disclosure).

---

### Flow 4: Security Token Expiry & Tamper Resistance
1. Copy the download link from Flow 1:
   `https://<your-preview-domain>/api/planner-2027/download?order=<ORDER_ID>&token=<TOKEN>`
2. Tamper with the token (change 2 characters in `<TOKEN>`).
3. Open in a new tab. Confirm HTTP 403 Forbidden (`"Invalid or expired download link"`).
4. Verify expired token: Any token past 30 days is rejected with HTTP 403.

---

### Flow 5: Fail-Closed Placeholder Protection
1. If the generator generates a PDF with an unapproved placeholder `{{...}}`, the generator returns HTTP 422.
2. The order is automatically tagged with `status = 'needs_attention'`.
3. The UI informs the buyer: `"Your personal planner is being prepared by our editorial desk."`
4. Zero unfinished or placeholder-bearing files are ever released to the buyer.

---

### Flow 6: Admin Stuck-Orders Alert Route
1. In terminal or Postman, run:
   ```bash
   curl -H "Authorization: Bearer <ADMIN_BEARER_TOKEN>" \
        https://<your-preview-domain>/api/planner-2027/admin/stuck-orders
   ```
2. Confirm the JSON response:
   ```json
   {
     "stuck_orders_count": 0,
     "stuck_orders": []
   }
   ```
3. Test unauthenticated request (without Bearer token): Confirm HTTP 401 Unauthorized.

---

### Flow 7: Public Asset Isolation
Confirm that proprietary calculation logic and Panchang files are inaccessible over HTTP:
1. `curl -I https://<your-preview-domain>/data/panchang_2027_delhi.json` → **HTTP 404**
2. `curl -I https://<your-preview-domain>/planner_2027_engine.py` → **HTTP 404**
3. `curl -I https://<your-preview-domain>/pdf_service/` → **HTTP 404**
4. `curl -I https://<your-preview-domain>/_worker.js` → **HTTP 404**

---

## 4. Automated Smoke-Test Script

You can run the automated smoke test against the live preview URL using:

```bash
node scripts/preview_smoke_test.mjs --url https://<preview-domain> --admin-token <token>
```
