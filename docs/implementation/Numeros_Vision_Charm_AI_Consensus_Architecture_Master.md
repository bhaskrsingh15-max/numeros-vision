# Numeros Vision + Charm AI
# Deterministic Multi-System Numerology & Astrology Consensus Architecture
## Master Implementation Specification for Google Antigravity

**Document status:** Implementation specification and acceptance contract  
**Product:** Numeros Vision  
**Customer-facing AI:** Charm AI by Numeros Vision  
**Tagline:** Unveil Every Charm  
**Scope:** Backend calculation logic, knowledge model, cross-system consensus, reports, Charm AI, user feedback, evaluation, and launch testing  
**Protected assets:** Existing UI/UX, theme, layout, logo, brand colours, routing and working frontend behaviour must remain intact unless a specific change is necessary and approved.

---

# 0. Mission and non-negotiable rules

Build a production-oriented, testable system in which each supported numerology or astrology tradition has its own documented calculation and interpretation logic. The system compares structured characteristics only after each engine finishes its work. It then creates a clear, humane explanation and practical, optional guidance.

This is not a request to produce a generic LLM chatbot that guesses planetary positions or blends traditions from its language-model memory.

## 0.1 Hard invariants

1. **Audit the existing repository before changing it.** Do not perform a blind rewrite or replace working modules because a new architecture looks cleaner.
2. **Preserve the existing brand, logo, theme, page structure, UI/UX and visual design.** Scope changes to calculation logic, APIs, data structures, orchestration, reporting logic, evaluation and necessary non-visual integration.
3. **Lo Shu is the core birth-date numerology calculation system.** It is the canonical numerology grid for the core profile, subject to the exact formula inventory and approved ruleset.
4. **Chaldean numerology is the core name-calculation and name-balancing system.** Do not substitute Pythagorean mapping for Chaldean name calculations.
5. Lo Shu, Chaldean/Cheiro, Pythagorean/Western and Vedic numerology each retain their own calculation and interpretation definitions. Do not collapse them into one formula.
6. KP, BNN, Vedic astrology and Lal Kitab each retain their own calculation and interpretation definitions. Do not make one astrology engine impersonate another.
7. Deterministic calculations are authoritative for numeric and chart outputs. The LLM is not allowed to calculate, amend, or guess them.
8. Every calculation, rule, source, prompt, report schema and evaluation set must be versioned.
9. If a formula or tradition is ambiguous, disputed, missing, or unsupported by an approved source, mark it `unverified` and prevent it from silently entering a production reading.
10. Do not invent formula details, source references, planet placements, dashas, birth-time assumptions, number meanings, remedies or accuracy statistics.
11. A cross-system agreement score is an **internal convergence indicator**, not a probability that an event will happen.
12. User confirmation that an interpretation “matches” is a subjective feedback label, not proof of objective prediction accuracy.
13. Never automatically modify production prompts, rules or model weights from raw feedback. Feedback enters a versioned, consented evaluation workflow.
14. Do not use fear-based predictions, guaranteed outcomes, medical diagnosis, or coercive remedy sales.
15. Preserve existing production data. Use additive, reversible migrations where possible. No destructive migrations, production deployment, deletion of data or secret rotation without explicit approval.
16. Do not claim “launch ready” until tests have actually run and critical acceptance gates have passed.
17. No invented reviews, performance numbers, customer results, market statistics or model-accuracy percentages.
18. Do not print API keys or secret values while inspecting the repository.
19. Review licences before reusing public source code or calculation/ephemeris dependencies.
20. If a required capability cannot be verified, implement a clear `unsupported`, `needs_input`, or `unverified` state rather than faking a result.

---

# 1. Product logic in one view

The intended system has six distinct layers:

1. **Calculation layer:** Produces exact, reproducible values from validated user inputs using each tradition's own formula.
2. **Characteristics layer:** Maps those values to documented characteristics, number patterns, planet attributes, houses, periods and traditional interpretations.
3. **Evidence layer:** Stores where every rule and interpretation came from, its version, source, applicability and confidence status.
4. **Consensus layer:** Compares equivalent characteristics across systems, groups correlated systems, preserves conflicts and identifies missing evidence.
5. **Guidance layer:** Turns validated consensus and individual-system findings into accessible explanations, lifestyle reflection and optional traditional remedies.
6. **Evaluation layer:** Collects consented feedback, tests historical and future-dated claims, measures technical quality and helps the team improve the product through controlled releases.

The same pipeline must serve:
- Free calculators
- Paid numerology reports
- Paid astrology and combined reports
- Charm AI chat
- Career/work readings
- Wealth and money-habit reflection
- Love and relationship reflection
- Partner compatibility
- Family themes
- Personal hurdles and repeated patterns
- Current period and timing questions
- Name analysis and name balancing
- Lifestyle suggestions and optional traditional remedies

The report generator and Charm AI must use the same calculation and consensus services. Do not implement separate hidden logic for chat and PDFs.

---

# 2. Traditions and source-of-truth registry

## 2.1 Numerology systems

| System ID | Role | Must calculate independently | Required interpretation coverage |
|---|---|---|---|
| `loshu` | Core birth-date numerology | Digit extraction, grid placement, counts, repeated/missing values, approved grid patterns and approved timing formulas | Individual number characteristics, frequency, missing/repeated numbers, grid lines/patterns, elements balance and limitations |
| `chaldean` | Core name calculation and balancing; secondary birth-number interpretation where specified | Approved Chaldean letter mapping, name totals, compound totals, reductions and approved number variants | Letter values, compound totals, root numbers, number characteristics, name comparison and balancing rationale |
| `cheiro` | Separate named interpretation profile | Only formulas explicitly defined for the selected Cheiro ruleset | Number and compound-number definitions with source attribution |
| `pythagorean_western` | Comparative numerology interpretation | Its own letter mapping and calculation rules, if the feature uses names | Core numbers and other supported outputs with source attribution |
| `vedic_numerology` | Comparative numerology interpretation | Its own documented birth/name mappings and number relationships | Number, planetary correspondence and interpretive definitions with source attribution |

**Important system boundary:** “Cheiro” and “Chaldean” may overlap in popular sources, but the software must not assume they are interchangeable. The formula registry must identify exactly which rulebook/source defines each calculation and meaning.

## 2.2 Astrology systems

| System ID | Role | Required engine outputs |
|---|---|---|
| `kp_astrology` | Independent KP chart and timing analysis | Required chart placements, cusps, nakshatra/sub-lord chain, significators, applicable dasha/bhukti/antara outputs and KP-specific interpretation references |
| `bnn_astrology` | Independent BNN analysis | Only the placements, combinations, rules and timing constructs supported by the approved BNN rulebook and implementation |
| `vedic_astrology` | Independent Vedic chart analysis | Chart placements, house/sign/planet relationships, selected divisional charts and dasha outputs supported by the implementation |
| `lal_kitab` | Independent Lal Kitab interpretation | Only documented Lal Kitab-specific planetary placements, house rules, interpretations and remedies supported by the approved source set |

Do not claim a complete engine for a tradition when only some of its rules are implemented. Each engine must advertise its implemented coverage and limitations.

## 2.3 Formula registry is the source of truth

Build a machine-readable registry. A human-readable spreadsheet or Markdown inventory should be generated from it.

Each formula record must contain:

- `formula_id`
- `system_id`
- `formula_name`
- `formula_version`
- `formula_status`: `draft`, `verified`, `production`, `deprecated`
- `input_schema`
- `output_schema`
- `algorithm_reference`
- `source_refs`
- `source_excerpt_or_rule_summary`
- `source_rights_or_license`
- `known_variants`
- `variant_selection_rule`
- `rounding_or_reduction_rule`
- `edge_case_policy`
- `golden_test_ids`
- `reviewer`
- `reviewed_at`
- `change_log`

A formula cannot be marked `production` until a reviewer confirms the rule and tests.

## 2.4 Source hierarchy and dispute handling

For each tradition:
1. Record primary/authoritative materials where available and legally usable.
2. Record the exact edition, author, page/section or stable URL where possible.
3. Record reputable secondary explanations separately from primary rules.
4. Record conflicting variants rather than silently merging them.
5. Select the default variant explicitly for the product.
6. Make the selected variant visible in internal diagnostics and available for disclosure in detailed reports where appropriate.
7. If sources disagree and the product has not selected a policy, return `variant_conflict` and do not guess.
8. Do not scrape or reuse material without reviewing permissions, licence, terms and copyright.

The LLM must not decide which formula is “correct” at runtime. The formula registry and reviewed ruleset decide that.

---

# 3. Canonical input and profile model

## 3.1 Input fields

Support only fields needed for the requested feature:

- Date of birth
- Birth time, if required by the selected astrology calculation
- Birthplace or coordinates, if required by the selected calculation
- Timezone resolved from the location and date, where applicable
- Name, only for features that require a name
- Partner details, only for compatibility features and with clear notice/permission
- Reading question/category
- Selected language
- User's selected historical or future time window, if applicable
- Consent choices for profile persistence, evaluation feedback and optional model-training use

Do not assume missing birth time is midnight. Do not infer a birthplace from IP address. Do not silently correct a date.

## 3.2 Canonical profile record

```json
{
  "profile_id": "server-generated-id",
  "date_of_birth": "YYYY-MM-DD",
  "birth_time": null,
  "birth_place_id": null,
  "timezone_id": null,
  "input_precision": {
    "date": "exact",
    "time": "unknown",
    "place": "unknown"
  },
  "created_at": "ISO-8601",
  "updated_at": "ISO-8601"
}
```

Store:
- Original user-entered value
- Normalised value
- Normalisation method/version
- Whether the user confirmed it
- Whether it is exact, approximate, unknown or derived
- Any assumptions used by the engine

## 3.3 Input validity

- Validate calendar dates, leap years and date boundaries.
- Validate time strings and timezone handling.
- Keep date/time timezone assumptions explicit.
- Validate location inputs and coordinate ranges.
- Validate name Unicode, whitespace and script rules before letter mapping.
- Handle diacritics and non-Latin scripts through an explicit, tested transliteration policy. Never silently transliterate a name.
- If a system requires an input that is missing, return `needs_input`.
- If birth time is approximate, propagate that uncertainty to chart-sensitive results.
- Keep profile data separate from analytics identifiers.
- Provide a way to correct input and regenerate a reading with a new calculation run.

---

# 4. Lo Shu core numerology engine

## 4.1 Required outputs

For every supported birth-date profile, the Lo Shu engine should return, where applicable:

1. Validated date input and normalised form.
2. Digit extraction result.
3. Treatment of zero, if any, as defined by the approved ruleset.
4. Count for each grid number.
5. Grid placement and ordered grid representation.
6. Missing-number list.
7. Repeated-number list and frequency per number.
8. Approved line/arrow/pattern detection.
9. Approved element-balance outputs.
10. Approved driver/conductor or other core numbers, only if included in the selected ruleset.
11. Approved timing/dasha outputs, if a documented Lo Shu/numerology timing rule is part of the product.
12. Warnings, assumptions and formula version.
13. A calculation trace suitable for internal debugging.
14. Stable result hash.

## 4.2 Grid representation

Conventional Lo Shu grid:

```text
+---+---+---+
|  4|  9|  2|
+---+---+---+
|  3|  5|  7|
+---+---+---+
|  8|  1|  6|
+---+---+---+
```

## 4.3 Repeat and missing number semantics

- A count is a calculation fact.
- The interpretation of that count is a separate, sourced rule.
- A number's absence is not automatically a defect or negative event.
- A repeated number must not automatically be described as a “problem.”
- Any intensity or balance label must be tied to a versioned rule with a documented range.
- Never invent a threshold such as “three repetitions means excess” unless the selected tradition's source explicitly supports it.

## 4.4 Element balance

Build an element mapping registry rather than embedding element assumptions in code.

## 4.5 Numerology timing/dasha

Treat each timing method as a distinct engine or sub-engine with explicit period intervals.

---

# 5. Chaldean name engine and name balancing

## 5.1 Core responsibilities

The Chaldean name service must:
1. Validate the name and script.
2. Apply the approved Chaldean letter mapping.
3. Return a character-by-character calculation trace.
4. Return the total before reduction.
5. Return compound-number interpretation where supported.
6. Return the reduced/root value under the selected ruleset.
7. Explain which mapping and reduction rule were used.
8. Compare alternative spellings using the same engine version.
9. Record any transliteration or unsupported-character warning.
10. Avoid claiming that changing a name guarantees success, money, health or relationship outcomes.

---

# 6. Numerology characteristic knowledge atlas

Build reviewed entries for every supported number and output that the system actually uses, normalising interpretations into a shared taxonomy (`career_growth`, `work_change`, `leadership`, `learning`, `communication`, `money_management`, `resource_stability`, `relationships`, `commitment`, `family_responsibility`, `emotional_reflection`, `discipline`, `creativity`, `spiritual_practice`, `routine_and_habits`, `travel_or_relocation`, `decision_making`, `social_support`, `rest_and_balance`, `challenge_or_delay`).

---

# 7. Astrology characteristics and timing atlas

Each astrology engine (KP, BNN, Vedic, Lal Kitab) returns its own structured output with explicit configuration (zodiac, ayanamsha, house system, nodes, ephemeris, dasha method).

---

# 8. Cross-system consensus engine

Consensus is created by comparing **normalised themes and claims**, not by mixing raw numbers or averaging planetary positions.

Top-level statuses:
- `convergent`
- `partially_convergent`
- `conflicted`
- `single_system`
- `insufficient_evidence`
- `not_comparable`

Family-aware convergence: collapse duplicate or near-duplicate support within correlation groups into one family-level signal.

`convergence_ratio = supporting_family_count / eligible_family_count`

---

# 9. Reading and prediction generation pipeline

Charm AI should sound like a thoughtful, realistic consultant: warm, clear, calm and conversational, explaining technical terms simply, without overstating outcomes or dramatising challenging periods.

---

# 10. Past-pattern validation and present-pattern check

Generate dated historical reflection questions to validate whether interpretations match the user's lived experience, collecting feedback across:
`yes_match`, `partial_match`, `no_match`, `not_enough_information`, `prefer_not_to_answer`, `skipped`.

---

# 11. Feedback data model and evaluation metrics

Store subjective resonance, factual fit, usefulness, and future outcomes separately. Never combine them into a single misleading “accuracy score.”

---

# 12. Continuous learning without uncontrolled production drift

Raw feedback enters a quarantined offline evaluation ledger. It must NEVER directly fine-tune the live model or alter production prompts dynamically.

---

# 13. Shared narrative and report contract

Charm AI chat (`/api/v1/readings/ask`) and every PDF report call the exact same calculation, interpretation, consensus, evidence, and safety pipeline.

---

# 14. Remedies, lifestyle guidance and crystals

Practical, optional, affordable, non-coercive lifestyle guidance:
- Dinacharya and spiritual circadian routines
- Sattvic habits and mindful pauses
- Sacred Yantras with directional Vastu and consecration timing
- Safe crystals/gemstones: prescribed strictly as subtle vibrational/color/elemental attunement, excluding natural planetary enemies (e.g., Sun/Venus/Mars vs Saturn/Rahu), fully compliant with Drugs and Magic Remedies Act 1954 (zero curative/financial claims).
