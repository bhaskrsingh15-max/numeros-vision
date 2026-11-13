# Numeros Vision — Open Rule Questions & Governance Register
**Specification Version**: 2.0.0  
**Status**: Active Governance Document  
**Date**: 2026-10-21  

---

## 1. Governance Directives on Incomplete Domain Rules

Per Section 0 & 1.5 of Master Specification v2.0:
> "If a critical rule or formula is missing from the actual source corpus, build the interface/configuration needed to support it, mark that rule UNVERIFIED or DISABLED, and do not invent the rule. Continue implementing other verified infrastructure."

---

## 2. Quarantined & Gated Rules

| Rule Identifier | Domain / Method | Current Status | Cause of Quarantine / Open Question | Activation Release Gate |
|---|---|---|---|---|
| `RULE-LK-MASNOOI-001` | Lal Kitab | `DISABLED` / `UNVERIFIED` | Complete 1942 Urdu/Hindi original folio cross-reference for Masnooi planetary alchemy equations is pending physical library scan verification. | Keep adapter disabled; do not include in active consensus voting until reviewer signs off. |
| `RULE-ASTRO-VASTU-EVENT-001` | Astro-Vastu | `SEPARATED` | Astro-Vastu is an environmental spatial alignment system, not a primary event-timing engine. Cannot cast votes on career or marriage timing. | Retain as spatial recommendation only; block from consensus event-timing matrix. |
| `RULE-DASHA-SUBDAY-P4` | Numerology Dasha | `UNVERIFIED` | Calculating sub-day (hourly/minute) Dasha periods from numerology roots lacks unanimous classical source consensus. | Restrict Numerology Dasha granularity to Day level (Personal Day); defer hourly timing strictly to planetary Horas. |
| `RULE-CONSENSUS-REFINEMENT-001` | Consensus Timing | `DISABLED` | Rule allowing astrology transit dates to narrow the primary Numerology Dasha window without explicit human confirmation. | Immutable policy enforced: Numerology window remains primary. Astrology dates appear only as separate corroboration labels. |

---

## 3. Human Review Requirements & Sign-Off Checklist

- [ ] **Lal Kitab Source Text Acquisition**: Provide page locators for Masnooi compound awakening tables.
- [ ] **Astro-Vastu Domain Boundary Review**: Formalize policy separating spatial remediation from timing predictions.
- [ ] **Golden Dataset Calibration**: Expand golden test benchmark from 50 to 200 reviewed historical validation cases.
