# Numeros Vision — Rule Governance & Provenance Policy
**Document Version**: 1.0.0  
**Effective Date**: 2026-10-21  
**Governance Authority**: Numeros Vision Domain Review Committee

---

## 1. Rule Governance Principles

1. **Explicit Provenance Mandatory**:
   Every traditional interpretation, planetary association, compound meaning, or compatibility rule must trace to an identifiable, published historical or expert source with an exact locator (book, edition, chapter, verse, or page).
2. **Strict Draft Lifecycle**:
   Any newly suggested rule or hypothesis begins in `draft` status with `requires_expert_approval: true`. It must **NEVER** participate in customer-facing scoring, ranking, or recommendations until approved by authorized reviewers.
3. **No Rule Invention**:
   If an entry in a relationship matrix or compatibility table is absent in approved sources, the engine must return `UNKNOWN` or `NOT_APPLICABLE`. It must never infer or fabricate an answer.
4. **Contextual Scoping**:
   Rules and exceptions do not apply globally. Every rule must define its applicable `business_categories`, `product_functions`, and `trigger_conditions`. An exception for athletic footwear does not transfer to banking or food brands.

---

## 2. Rule Schema (Section 16.4 Specification)

Every rule in the Numeros Vision system conforms to the following schema:

```json
{
  "rule_id": "BUSINESS_ARCHETYPE_SATURN_001",
  "rule_version": "1.0.0",
  "status": "draft",
  "tradition": "vedic_astrology",
  "claim_type": "traditional_interpretation",
  "source_id": "SRC_BPHS_1984_V1",
  "source_locator": "Vol 1, Ch 3, v 25-28",
  "business_categories": ["athletic_footwear", "sports_training", "endurance_sports"],
  "trigger_conditions": ["business_function includes endurance or sustained physical training"],
  "archetype": "Saturn",
  "relationship_type": "candidate_support",
  "exceptions": [
    {
      "exception_id": "EXC_FOOTWEAR_BLACK_001",
      "description": "Black logo color is permitted when business function maps to Saturn/Rahu endurance, overriding generic color warnings.",
      "conditions": ["business_category == athletic_footwear", "intended_attribute == endurance"]
    }
  ],
  "counter_rules": [],
  "confidence_policy": "expert_reviewed_rubric",
  "requires_expert_approval": true,
  "effective_from": null,
  "effective_to": null,
  "approved_by": null,
  "change_reason": "Initial draft for contextual footwear evaluation"
}
```

---

## 3. Registered Proposals & Status Table

| Rule ID | Archetype / Number | Status | Categories | Requires Approval | Notes |
| :--- | :---: | :---: | :--- | :---: | :--- |
| `SPORTS_ARCHETYPE_SATURN_8` | Saturn (8) | `draft` | `sports`, `endurance_sports` | `true` | Associated with discipline, stamina, and prolonged effort. Pending source verification. |
| `SPORTS_ARCHETYPE_KETU_7` | Ketu (7) | `draft` | `sports`, `precision_sports` | `true` | Associated with hyper-focus, precision, and detachment. Pending source verification. |
| `SPORTS_ARCHETYPE_MARS_9` | Mars (9) | `approved` | `sports`, `competitive_sports` | `false` | Traditional association with competitive energy, physical strength, and agility (BPHS Ch 3). |
| `FOOTWEAR_SATURN_RAHU_EXC` | Saturn/Rahu | `draft` | `athletic_footwear` | `true` | Contextual exception for dark palettes representing endurance and boundary-pushing. |

---

## 4. Conflict Resolution Hierarchy

When two approved rules produce divergent recommendations:
1. **Hard Design & Accessibility Constraints Always Prevail**: Legibility, contrast ratios, and exact wordmark accuracy cannot be overridden by any symbolic or traditional score.
2. **Specific Category Exception > Generic Rule**: A specific rule for `athletic_footwear` takes precedence over a generic rule for `all_businesses`.
3. **Multi-Tradition Divergence**: Disclose the conflict transparently (`Methodology A suggests X, Methodology B suggests Y`); never average disparate traditions into an artificial consensus.
