# NUMEROS VISION — ENVIRONMENT VARIABLE MANIFEST

**Document Version**: 1.0.0  
**Effective Date**: 2026-11-09  
**Standardized Canonical Names**:
- Charm AI Backend URL: `CHARM_SERVICE_URL` (accepts only this name; `BACKEND_API_URL` removed).
- IP Hash Salt: `IP_HASH_SALT` (accepts only this name; `CHARM_IP_HASH_SALT` removed).

---

## 1. Cloudflare Pages & Edge Worker (`app/static/_worker.js`)

| Variable Name | Environment | Requirement | Behaviour When Missing | Service |
| :--- | :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | Preview, Production | Required | Defaults to `production` (fail-closed secure state). | Edge Worker |
| `SESSION_SECRET` | Preview, Production | Required | Throws `SESSION_SECRET_MISSING`; auth sessions & cookies fail closed. | Edge Worker |
| `OTP_HMAC_SECRET` | Preview, Production | Required | Throws `OTP_HMAC_SECRET_MISSING`; OTP code hashing & verification blocked. | Edge Worker |
| `IP_HASH_SALT` | Preview, Production | Required | Throws `IP_HASH_SALT_MISSING` on auth; returns 503 `SERVICE_MISCONFIGURED` on Charm. | Edge Worker |
| `DATA_ENCRYPTION_KEY` | Preview, Production | Required | Throws `DATA_ENCRYPTION_KEY_MISSING`; PII encryption/decryption fails closed. | Edge Worker |
| `DOWNLOAD_TOKEN_SECRET` | Preview, Production | Required | Throws `DOWNLOAD_TOKEN_SECRET_MISSING`; secure download links fail closed. | Edge Worker |
| `ADMIN_TOKEN` | Preview, Production | Required (Preview/Admin) | Returns 503 `ADMIN_TOKEN is not configured` on `/api/admin/*`. | Edge Worker |
| `TURNSTILE_SECRET_KEY` | Preview, Production | Required | Local/test bypass allowed; in production returns 503 or 403 on invalid verification. | Edge Worker |
| `TURNSTILE_SITE_KEY` | Preview, Production | Required (Production) | In production, missing or test keys trigger 503 on `send-code` and `resend-link`. | Edge Worker / Client |
| `EMAIL_PROVIDER` | Preview, Production | Required (Out-of-test) | Returns 503 `Transactional email provider is not configured` on send/resend. | Edge Worker |
| `EMAIL_API_KEY` | Preview, Production | Required (Out-of-test) | Returns 503 `Transactional email API key is not configured` on send/resend. | Edge Worker |
| `EMAIL_FROM` | Preview, Production | Required (Out-of-test) | Returns 503 `Transactional email sender address is not configured`. | Edge Worker |
| `EMAIL_DAILY_CAP` | Preview, Production | Optional | Defaults to 500 emails/day; dispatches paused when reached. | Edge Worker |
| `EMAIL_KILL_SWITCH` | Preview, Production | Optional | Defaults to false; when `true`, all outbound emails return 503. | Edge Worker |
| `NV_EMAIL_LOG_ADAPTER` | Test only | Optional | Must be `true` to allow logging adapter; never set in preview or production. | Edge Worker |
| `CHARM_SERVICE_URL` | Preview, Production | Required (for Charm) | Returns 503 `SERVICE_BACKEND_UNAVAILABLE` on `/api/charm/chat`. | Edge Worker |
| `CHARM_SERVICE_SECRET` | Preview, Production | Required (for Charm) | Returns 503 `SERVICE_AUTH_UNAVAILABLE` on `/api/charm/chat`. | Edge Worker |
| `CHARM_GLOBAL_DAILY_CAP` | Preview, Production | Optional | Defaults to 500 questions/day; returns 429 when cap reached. | Edge Worker |
| `CHARM_KILL_SWITCH` | Preview, Production | Optional | Defaults to false; when `true`, returns 503 pause message. | Edge Worker |
| `PDF_SERVICE_URL` | Preview, Production | Required (for PDF) | Falls back to localhost in `local`; fails generation in preview/prod. | Edge Worker |
| `PDF_SERVICE_SECRET` | Preview, Production | Required (for PDF) | Fails generation with 500/503 when missing. | Edge Worker |
| `RAZORPAY_KEY_ID` | Preview, Production | Required (Payments) | Refuses execution if live key on test/preview; payments fail if missing. | Edge Worker |
| `RAZORPAY_KEY_SECRET` | Preview, Production | Required (Payments) | Signature verification and payment capture blocked. | Edge Worker |
| `RAZORPAY_WEBHOOK_SECRET` | Preview, Production | Required (Webhooks) | Webhook signature verification fails with 400/401. | Edge Worker |
| `OTP_ENABLED` | Preview, Production | Optional | Defaults to `false` (SMS OTP disabled in favor of Email OTP). | Edge Worker |
| `FAST2SMS_API_KEY` | Preview, Production | Optional (SMS) | SMS OTP dispatch disabled when unset or when `OTP_ENABLED=false`. | Edge Worker |
| `TELEMETRY_SALT` | Preview, Production | Optional | Anonymized analytics salt; falls back to internal SHA-256 hash. | Edge Worker |
| `GOOGLE_CLIENT_ID` | Preview, Production | Optional | Google Sign-In button disabled or token verification rejected. | Edge Worker |
| `PLANNER_2027_ALLOW_PLACEHOLDER_ON_PREVIEW` | Preview only | Optional | Allows mock preview PDF only when `ENVIRONMENT=preview`. Throws in prod. | Edge Worker |
| `MOCK_PAYMENTS` | Local, Preview | Optional | Defaults to `false`; enables simulated payments in test environments only. | Edge Worker |

---

## 2. Python Backend & PDF Microservices (`app/` and `pdf_service/`)

| Variable Name | Environment | Requirement | Behaviour When Missing | Service |
| :--- | :--- | :--- | :--- | :--- |
| `ENVIRONMENT` | Preview, Production | Required | Defaults to `development`. Dictates bypass allowances and error detail. | FastAPI / PDF Service |
| `CHARM_SERVICE_SECRET` | Preview, Production | Required | Fails closed with 503 in all deployed environments (`X-NV-Charm-Secret`). | FastAPI / Charm AI |
| `PDF_SERVICE_SECRET` | Preview, Production | Required | Fails closed with 503 on PDF render requests (`X-PDF-Worker-Secret`). | PDF Service |
| `NV_ALLOW_UNAUTHENTICATED_LOCAL` | Local only | Optional | Defaults to false. Allows unauthenticated calls only in local dev. | FastAPI / PDF Service |
| `CDP_ADMIN_USER` | Preview, Production | Optional | Admin access to CDP export endpoints disabled when missing. | FastAPI (CDP) |
| `CDP_ADMIN_PASSWORD` | Preview, Production | Optional | Admin access to CDP export endpoints disabled when missing. | FastAPI (CDP) |
| `GA4_MEASUREMENT_ID` | Preview, Production | Optional | Server-side GA4 telemetry omitted when unset. | FastAPI (CDP) |
| `GOOGLE_ADS_ID` | Preview, Production | Optional | Google Ads conversion tracking omitted when unset. | FastAPI (CDP) |
| `GOOGLE_ADS_CONVERSION_LABEL_SIGNUP` | Preview, Production | Optional | Signup conversion event omitted when unset. | FastAPI (CDP) |
| `GOOGLE_ADS_CONVERSION_LABEL_PURCHASE` | Preview, Production | Optional | Purchase conversion event omitted when unset. | FastAPI (CDP) |
| `META_PIXEL_ID` | Preview, Production | Optional | Meta Conversions API events omitted when unset. | FastAPI (CDP) |
| `CLARITY_PROJECT_ID` | Preview, Production | Optional | MS Clarity tracking script omitted when unset. | FastAPI (CDP) |
| `GTM_CONTAINER_ID` | Preview, Production | Optional | Google Tag Manager script omitted when unset. | FastAPI (CDP) |
| `FIREBASE_API_KEY` | Preview, Production | Optional | Client Firebase configuration block omitted when unset. | FastAPI (CDP) |
| `FIREBASE_AUTH_DOMAIN` | Preview, Production | Optional | Client Firebase configuration block omitted when unset. | FastAPI (CDP) |
| `FIREBASE_PROJECT_ID` | Preview, Production | Optional | Client Firebase configuration block omitted when unset. | FastAPI (CDP) |
| `FIREBASE_STORAGE_BUCKET` | Preview, Production | Optional | Client Firebase configuration block omitted when unset. | FastAPI (CDP) |
| `FIREBASE_MESSAGING_SENDER_ID` | Preview, Production | Optional | Client Firebase configuration block omitted when unset. | FastAPI (CDP) |
| `FIREBASE_APP_ID` | Preview, Production | Optional | Client Firebase configuration block omitted when unset. | FastAPI (CDP) |
| `FIREBASE_MEASUREMENT_ID` | Preview, Production | Optional | Client Firebase configuration block omitted when unset. | FastAPI (CDP) |
| `ALLOW_TEST_TOKENS` | Preview only | Optional | Defaults to false; allows test tokens in non-production environments. | FastAPI Engine |
| `ALLOW_STAGING_TEST_BYPASS` | Preview only | Optional | Defaults to false; allows test bypass headers in non-production environments. | FastAPI Engine |
| `NADI_EVENT_ENGINE_ENABLED` | Preview, Production | Optional | Defaults to `True`; feature flag for Nadi event calculation subsystem. | FastAPI Engine |
