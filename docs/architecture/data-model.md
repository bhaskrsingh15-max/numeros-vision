# Numeros Vision — Canonical Data Model
**Document Type:** Data Model Specification

## 1. Core Entities
- `profiles`: User birth date, normalized birth time, location coordinates, timezone, input precision (`exact`, `approximate`, `unknown`, `derived`), consent flags.
- `calculation_runs`: Run ID, engine ID, engine version, input snapshot hash, raw calculation JSON, timestamp.
- `claims`: Claim ID, system ID, family ID, characteristic IDs, theme IDs, time window (`start`, `end`, or `timeless`), direction (`positive`, `challenging`, `mixed`, `neutral`), support type, source refs, conflict status.
- `consensus_runs`: Consensus ID, participating family IDs, supporting families, opposing families, convergence ratio, consensus status, layman narrative, past reflection question.
- `feedback_events`: Feedback ID, claim ID, feedback type (`historical_fit`, `present_resonance`, `future_outcome`), label (`yes_match`, `partial_match`, `no_match`, `not_enough_information`, `prefer_not_to_answer`, `skipped`), consent scope.
- `credit_ledger`: Transaction ID, user ID, order ID, credits added, credits consumed, balance, idempotency key.
