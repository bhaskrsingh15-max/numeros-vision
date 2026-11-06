# NUMEROS VISION — DEPLOYMENT SECURITY POLICY & GATING DIRECTIVES

## Mandatory Release Gate: Live Mode Prohibition

> [!CRITICAL]
> **DO NOT ENABLE ANY LIVE RAZORPAY KEYS ANYWHERE UNTIL RELEASE GATE PASSES.**
> 
> Switching the gateway from Test Mode to Live Mode is **STRICTLY PROHIBITED** until:
> 1. **Commit 4** (Server-side order creation accepting only `packId` and `subjectId`, amount validation against canonical catalog, and subject ownership verification) is deployed and verified.
> 2. **Commit 5** (Complete elimination of client-side `localStorage` unlocks, query parameter injection `?paid=true`, and enforcement of server-side `viewFor(userId, subjectId)` gating) is deployed and verified.
> 3. **The Audit Leak Test (Section 6)** passes with zero unauthorized data access.

---

## Secret Storage Standards

1. **Zero Hardcoded Secrets**:
   * No API keys, webhook secrets, or credentials may appear in client bundles, HTML templates, JavaScript files, or version control.
2. **Cloudflare Secrets Injection**:
   * Inject all secrets exclusively via the Cloudflare Pages / Workers dashboard or via the Wrangler CLI:
     ```bash
     npx wrangler secret put RAZORPAY_KEY_ID
     npx wrangler secret put RAZORPAY_KEY_SECRET
     npx wrangler secret put RAZORPAY_WEBHOOK_SECRET
     npx wrangler secret put FAST2SMS_API_KEY
     npx wrangler secret put WEB3FORMS_ACCESS_KEY
     ```
3. **Fail-Closed Architecture**:
   * All payment, SMS, and webhook endpoints fail closed (HTTP 500/503) if server secrets are absent. No mock order fallback is permitted.
