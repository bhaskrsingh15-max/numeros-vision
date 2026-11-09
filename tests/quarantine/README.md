# Quarantined Test Suites

The following test suites have been placed in quarantine because they test deprecated/superseded architectures, legacy endpoints, or historical mocks. They are preserved here for historical reference and auditability.

| Quarantined Suite | Written Reason |
| :--- | :--- |
| test_auth_commit3.mjs | Superseded by commit 6b auth architecture and Turnstile v0 verification. Tests deprecated v1 endpoints and headers. |
| test_payments_commit4.mjs | Superseded by commit 6b Razorpay verification & unified pricing flow. Tests deprecated direct mock pricing paths. |
| test_gating_commit5.mjs | Superseded by unified entitlement gateway in _worker.js. Tests obsolete tier gating schemas. |
| test_events_and_form_routing.mjs | Asserts deprecated /billing route and pre-Stage-A legal disclaimer text removed in unified journey. |
| test_encryption_aes_gcm.mjs | Uses outdated subtle crypto mock structure incompatible with current WebCrypto runtime. |
| test_otp_rate_limiting_and_honest_errors.mjs | Tests outdated origin validation mock schema that conflicts with multi-environment worker headers. |
| test_otp_security_and_dashboard_packs.mjs | Asserts deprecated dev_otp bypass pattern that was removed for zero-trust security. |
| test_worker_behavior.mjs | Asserts legacy 403 Forbidden on deprecated /reports/ route instead of modern 404/redirect behavior. |
| test_ui_ux_consistency.py | Asserts obsolete pre-Stage-A CSS classes and legacy homepage calculator DOM structure. |
| test_enterprise_agent_gateway.py | Tests legacy token format and gateway signatures from initial prototype before unified master API. |
| test_rag_speedup.py | Asserts cold BM25 init time < 100ms benchmark; fails spuriously across varying disk/CPU performance. |
