# Numeros Vision — Security, Privacy & Consent Governance
**Document Type:** Statutory Privacy Compliance

## 1. Compliance Standards
- India Digital Personal Data Protection (DPDP) Act 2023.
- EU General Data Protection Regulation (GDPR).

## 2. Data Safeguards
- Distinct, unbundled consent flags for profile storage, evaluation feedback, and communication.
- Consent withdrawal endpoint (`POST /api/v1/privacy/consent/withdraw`) immediately quarantines or deletes profile data.
- Redaction of PII, birth dates, and names from general server telemetry.
- Zero client-side storage of payment secrets; Razorpay webhooks verified server-side via HMAC SHA256.
