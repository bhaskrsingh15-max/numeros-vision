# NUMEROS VISION — PLANET LOGIC, REPETITION & COMMANDING-PLANET SPECIFICATION (`PLANET_LOGIC_SPEC.md`)

**Status**: Extracted verbatim from existing repository logic (Additive-Only Audit — Section 2.b & Section 16.A)  
**Rule**: None of the existing functions, thresholds, or data tables documented below were rewritten, removed, or modified. New additive layers read these outputs directly and attach structured `fact_id` / `logic_link` labels behind `NV_ENABLE_LAYERS_2_3`.

---

## 1. Existing Modules Governing Planet Character, Repetition & Benefic/Malefic Outcomes

| Module | Functions / Tables | Primary Consumers |
|---|---|---|
| `app/engine/charm_oracle_synthesizer.py` | `PLANETARY_INFO`, `NUMBER_DUAL_ATTRIBUTES`, `classify_digit_degree(digit, count)` | Charm AI Oracle Synthesizer, grid frequency evaluation |
| `app/engine/rule_governance.py` + `data/knowledge_base/day7_loshu_rules.json` + `data/knowledge_base/missing_number_rules.json` | `get_repetition_evaluation(digit, count)`, `get_missing_number_evaluation(digit)`, `evaluate_grid_frequencies(digit_counts)` | Governed Lo Shu frequency reports, Master Key `5` check, `>5` abstention |
| `app/engine/core_matrix_engine.py` | `analyze_repeat_numbers(d, m, y)`, `assess_karmic_and_master(d, m, y, name)`, `analyze_elements_balancing(d, m, y)` | Core Matrix API, PDF generators, web summaries |
| `app/engine/number_characteristics_registry.py` | `NUMBER_REGISTRY` (`1..9` planet, Sanskrit name, element, `core_essence`, `career_fit`, `shadow_side`, `growth_advice`) | Archetype & number characteristics lookups |
| `app/engine/unified_planetary_numerology_engine.py` | `UNIFIED_81_MATRIX` (`Driver x Conductor` `1..9 x 1..9`), `PLANETARY_RELATIONS` (`friends`, `neutral`, `enemies`) | 81 Driver-Conductor dynamic & planetary compatibility |

---

## 2. Exact Repetition Thresholds & Benefic / Malefic Classification Per Count

### 2.1 `charm_oracle_synthesizer.classify_digit_degree(digit, count)`
Applies uniformly to digits `1..9` using `NUMBER_DUAL_ATTRIBUTES[digit]`:

| DOB Count | `degree` | `status` | Narrative Source |
|---:|---|---|---|
| `0` | `MISSING` | `DEFICIENT` | `NUMBER_DUAL_ATTRIBUTES[digit]["under"]` (open grid cell requiring conscious habit building) |
| `1` | `UNDER` | `DEVELOPING` | `good` trait active at baseline + `under` note |
| `2` | `PAIR` | `OPTIMAL` | Strong and balanced expression (`good` attributes) |
| `3` | `EXAGGERATE` | `AMPLIFIED` | Turning-point intensity (`exaggerated` modifier) |
| `4` | `REACTIVE` | `HIGH_FRICTION` | Over-concentration (`bad` / shadow attributes + `exaggerated` modifier) |
| `>= 5` | `VOLATILE` | `EXTREME_IMBALANCE` | Extreme concentration (`bad` attributes requiring conscious grounding) |

### 2.2 `rule_governance.evaluate_grid_frequencies(digit_counts)` (`day7_loshu_rules.json`)
- **`count == 0`**: Evaluates missing-digit impact, `poorak` (supporting number), element remedy, and yantra note from `missing_number_rules.json` (`SRC-ADV-PROF-NOTES`).
- **`count == 1`**: `degree = "Under"` (`status = "EVALUATED"`).
- **`count == 2`**: `degree = "Pair"` (`status = "EVALUATED"`).
- **`count == 3`**: `degree = "Exaggerate"` (`status = "EVALUATED"`).
- **`count == 4`**: `degree = "Reactive"` (`status = "EVALUATED"`).
- **`count == 5`**: `degree = "Over-reactive"` (`status = "EVALUATED"`).
- **`count > 5` (`6+`)**: Returns `status = "PENDING_EVIDENCE"`, `degree = "EXTREME_REPETITION_UNVERIFIED"` (strict abstention against unverified claims).
- **Master Key `5` (`Mercury`)**: Sets `master_key_5_active = (digit_counts.get(5, 0) > 0)`.

### 2.3 `core_matrix_engine.analyze_repeat_numbers(day, month, year)`
Evaluates every present digit (`count >= 1`) in `DDMMYYYY` (non-zero digits only) and returns `{"counts": ..., "evaluations": [...]}`:
- **`frequency == 1`**: `type = "Harmonious"` (benefic baseline).
- **`frequency == 2`**: `type = "Benefic Amplification"` (strong and balanced).
- **`frequency == 3`**: `type = "Intense / Dual Potential"` (turning point — strong drive that can tip into shadow under stress).
- **`frequency >= 4`**: `type = "Malefic Over-Concentration"` (malefic-leaning concentration requiring grounding practices).

### 2.4 Reference Stage Mapping in `indications_engine.py` (Section 3.4 & 16.B.4)
Without altering any of the three existing functions above, `indications_engine.py` reads all three outputs and attaches the canonical reference stage id `planet_repeated_stage:{digit}:{count}`:
- `0` -> `missing`
- `1` -> `baseline`
- `2` -> `strong_and_balanced` (benefic-leaning)
- `3` -> `turning_point` (dual / watch point; Saturn `8`, Rahu `4`, Ketu `7`, and Mars `9` lean demanding at `3x`, while Sun `1`, Jupiter `3`, Mercury `5`, Venus `6` retain protective/constructive strength alongside ego/restlessness watch points)
- `4..5` -> `high` (malefic-leaning concentration; Sun `1` retains traditional steadying/protective note alongside control/solo-carrying watch point)
- `6+` -> `extreme` (malefic-leaning over-concentration + `rule_governance` `PENDING_EVIDENCE` abstention preserved)

---

## 3. Planet Character Modifiers (`1..9`) in Current Software

Extracted from `NUMBER_DUAL_ATTRIBUTES` (`charm_oracle_synthesizer.py`) and `NUMBER_REGISTRY` (`number_characteristics_registry.py`):

1. **1 — Sun (Surya)** | Element: Water (Lo Shu North) | Character: Leadership, initiative, self-reliance, clarity; traditionally seen as kingly and steadying/protective when circumstances are demanding. Shadow when over-repeated (`3x+`): stubbornness, carrying too much alone, resisting advice, ego friction (`exaggerated`: dominating speech).
2. **2 — Moon (Chandra)** | Element: Earth (Lo Shu South-West) | Character: Intuition, empathy, diplomacy, emotional sensitivity. Shadow when over-repeated (`3x+`): mood swings, over-sensitivity, hesitation, taking things personally.
3. **3 — Jupiter (Brihaspati / Guru)** | Element: Wood (Lo Shu East) | Character: Wisdom, learning, teaching, principled counsel, structured growth. Shadow when over-repeated (`3x+`): scattered commitments, dogmatic or preachy tone, mental over-expansion.
4. **4 — Rahu (North Node)** | Element: Wood (Lo Shu South-East) | Character: Practical systems, unconventional problem-solving, discipline, technical execution. Intense when repeated (`3x+`): rigidity, argumentative friction, sudden shifts, mental restlessness. *(Open terminology point for International edition: currently `"Rahu (North Node)"`; awaiting owner confirmation before switching to `"Rahu (Uranus in Western numerology)"`.)*
5. **5 — Mercury (Budh)** | Element: Earth (Lo Shu Center — Master Key) | Character: Adaptability, communication, commercial agility, emotional stability bridge. Shadow when over-repeated (`3x+`): nervous restlessness, juggling too many changes at once, impatience with routine.
6. **6 — Venus (Shukra)** | Element: Metal (Lo Shu North-West) | Character: Harmony, family care, responsibility, aesthetics, service. Shadow when over-repeated (`3x+`): over-protectiveness, attachment to comfort/approval, perfectionism in relationships.
7. **7 — Ketu (South Node)** | Element: Metal (Lo Shu West) | Character: Research, introspection, analytical depth, spiritual discernment. Intense when repeated (`3x+`): isolation, over-analysis, scepticism, stepping back emotionally.
8. **8 — Saturn (Shani)** | Element: Earth (Lo Shu North-East) | Character: Endurance, accountability, fair governance, long-term structural discipline. Heavy and slow when repeated (`3x+`): delayed pacing, self-criticism, workaholic heaviness, strictness with self and others.
9. **9 — Mars (Mangal)** | Element: Fire (Lo Shu South) | Character: Courage, humanitarian drive, decisive action, completion. Intense when repeated (`3x+`): a short fuse under pressure, haste, impulsive speech, burnout if unpaced.

---

## 4. Commanding-Planet Rule Audit & Default Additive Rule (Section 3.3 & 16.B.3)

### 4.1 What Existed Previously
A full repository search across `app/` confirmed that **no standalone numerical DOB-grid commanding-planet detector existed prior to this spec**:
- The word `"commanding"` previously appeared only as descriptive English prose in `NUMBER_REGISTRY` (`1` and `9`), `astrolearn_knowledge.py` (`1`, `6`, `9`), and `pdf_report_generator.py` (`Mulank 1`).
- No existing function selected a commanding planet from Lo Shu DOB digit counts.

### 4.2 Additive Rule Implemented (`detect_commanding_planet` in `app/engine/indications_engine.py`)
Per Section 3.3 & Section 16.B.3 (owner-confirmable thresholds, zero change to existing modules):
- **Input**: Non-zero DOB digit counts (`DDMMYYYY` only; Mulank, Bhagyank, and Kua excluded).
- **Default Threshold**: Let `top_count = max(counts.values())`, `leaders = [d for d, c in counts.items() if c == top_count]`, and `others_max = max([c for d, c in counts.items() if d not in leaders], default=0)`.
- A planet commands the grid iff **`top_count >= 4` AND `others_max <= 2`**.
- **Ties**: If two digits tie at `top_count >= 4` (e.g., `4x` and `4x` in an 8-digit DOB where all remaining digits have `0`), both are returned as **co-commanders**.
- **Lean Logic Links**:
  - `commanding_planet:{digit}:{count}`
  - `commanding_planet_benefic_lean` when traditional protective/steadying note applies (e.g., Sun `1` traditionally steadying alongside its high-repetition watch point)
  - `commanding_planet_malefic_lean` when high concentration (`>= 4`) creates over-dominance / friction requiring plane-balance habits first + planet pacing practices.

---

## 5. Master, Karmic & Compound Notes Usage Today

1. **Universal Single-Digit Rule (`app/engine/digit_root.py`)**:
   - Every derived core number (`Mulank`, `Bhagyank`, `Kua`, `Name number`, `Personal Year`, `Personal Month`, `Personal Day`) reduces strictly to **`1..9`** (`1 + (n - 1) % 9`; multiples of `9` return `9`).
   - **Master numbers (`11`, `22`, `33`) are NEVER returned as final results**. When an unreduced sum passes through `11`, `22`, or `33` (e.g. `17-02-1963`: `1+7+0+2+1+9+6+3 = 29 -> 11 -> 2`), `calc_compound_steps` records `master_path_note = "passes through 11 on the way to 2"` (`fact_id: master_path_note:conductor:11->2`).
2. **Karmic Debt Notes (`13, 14, 16, 19`)**:
   - `core_matrix_engine.assess_karmic_and_master(day, month, year, name)` inspects raw day (`13, 14, 16, 19`) and unreduced Bhagyank compound sum (`13, 14, 16, 19`) as **explanatory path notes only** (`karmic_note:13`, `14`, `16`, `19`), never overriding the `1..9` single-digit result.
3. **Compound Number Notes (`10..52+`)**:
   - Unreduced compound totals on birth day (`10..31`), Bhagyank sum, and Chaldean name sum are exposed as `compound_note:{source}:{compound}` explanatory metadata while final numbers remain `1..9`.
