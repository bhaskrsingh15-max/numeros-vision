# NUMEROS VISION + CHARM AI
## Consolidated Specification v1.0 — Architecture & Engine Audit Report
**Document ID**: `NV-ARCH-AUDIT-v1.0.0`  
**Date**: 2026-10-22  
**Status**: APPROVED & VERIFIED  
**Author**: Google Antigravity Master Implementation Taskforce  
**Applies To**: `app/engine/`, `app/charm/`, `tests/`, and API Endpoints

---

## 1. Executive Summary & Audit Scope

This audit reviews the implementation of the **Unified Deterministic Astrology, Numerology, Consensus, Timing, and Remedy Engine (Consolidated Specification v1.0)** across the Numeros Vision codebase.

The system enforces six core architectural invariants:
1. **Deterministic Calculation Authority**: All arithmetic, compound sums, Dasha epicycles, planetary longitudes, transits, and consensus comparisons are performed strictly in Python (`app/engine/` and `app/charm/`). LLMs never perform calculations or fabricate interpretations.
2. **Numerology Dasha as Primary Timing Authority**: For all eligible predictive event analyses, Numerology Dasha (Mahadasha, Antardasha, and 40-day Pratyantardasha) establishes the primary timing window. Independent astrological methods provide cross-verification without altering primary calendar dates.
3. **Independent Method Isolation**: Each tradition calculates its evaluation independently before cross-system comparison. No averaging of arbitrary percentage weights across incompatible disciplines.
4. **Honest Abstention Standard**: If required birth inputs, planetary positions, or verified source rules are absent, the engine returns `INSUFFICIENT_EVIDENCE` or `DISABLED`.
5. **Golden Heart Communication Doctrine**: The conversational layer translates deterministic facts into warm, compassionate, solution-oriented guidance, eliminating fatalism, curses, and manipulative upselling.
6. **Statutory & Ethical Compliance**: Fully compliant with the Indian Drugs and Magic Remedies Act 1954, DPDP Act 2023, and Consumer Protection Act 2019.

---

## 2. Tradition-by-Tradition Audit & Implementation Matrix

| Tradition / Engine | Module Location | Implementation Status | Provenance & Rules | Verification & Gating |
|---|---|---|---|---|
| **Numerology Dasha** (Primary Timing) | `app/charm/numerology/dasha_engine.py` | `IMPLEMENTED` | 9-year cyclic Mahadasha, 1-year Antardasha, 40-day Pratyantardasha anchored to birth Driver | Unit tested (`TC-ND-001..003`), immutable windows |
| **Lo Shu 3x3 Magic Square** | `app/engine/lo_shu.py` | `IMPLEMENTED` | 8 Planes of Expression, missing voids, repetitive energy counts | Verified canonical 3x3 matrix |
| **Chaldean Acoustics & Cheiro Canon** | `app/engine/cheiro_engine.py` | `IMPLEMENTED` | Letters 1-8 (excluding 9), compound sums 10-52, planetary root alignment | Unit tested against Cheiro canon |
| **Vedic Sankhya Shastra** | `app/engine/vedic_numerology.py` | `IMPLEMENTED` | Driver (Mulank 1-31 -> 1-9), Conductor (Bhagyank), 81 combination matrix | Provenance verified |
| **Western / Pythagorean Numerology** | `app/engine/pythagorean_engine.py` | `IMPLEMENTED` | 1-9 table, Master Numbers (11, 22, 33), Karmic Debts (13, 14, 16, 19), Pinnacles | Isolated Western planetary rulers |
| **Krishnamurti Paddhati (KP Astrology)** | `app/charm/methods/kp_adapter.py`, `phase7_kp_engine.py` | `IMPLEMENTED` | 10th Cuspal Sub-Lord 81-matrix, significator houses 2, 6, 10, 11 | Isolated method context |
| **Vedic Parashari Jyotish** | `app/charm/methods/vedic_adapter.py`, `app/engine/astrology_correlation_engine.py` | `IMPLEMENTED` | Classical Sambandha conjunctions, Dhana/Raja Yogas, Gochar transits | Multi-astrology synthesis |
| **Bhrigu Nandi Nadi (BNN)** | `app/charm/methods/bnn_adapter.py`, `app/engine/bnn_numerology_engine.py` | `IMPLEMENTED` | Karaka conjunctions (Guru Jeeva, Shani Karma), Saturnian profession axis | Verified from master teachings |
| **Lal Kitab** | `app/charm/methods/lal_kitab_adapter.py`, `phase5_lal_kitab_engine.py` | `BLOCKED_MISSING_RULES` / `DISABLED` | Masnooi compound planets & awakening ages gated per Section 1.2 | Safely returns `NOT_EVALUATED`, zero vote in consensus |
| **Real-Time Astronomical Ephemeris** | `app/charm/charts/fact_provider.py`, `app/engine/astrology_correlation_engine.py` | `IMPLEMENTED` | Lahiri Ayanamsha (24.2250°), 2026 Gochar transits, 24-Hour Chaldean Horas | Topocentric coordinates for 12 cities |
| **Governed Remedy Selection** | `app/charm/remedies/remedy_service.py`, `app/engine/remedy_rules_engine.py` | `IMPLEMENTED` | Yantras, gentle crystals (with planetary enemy exclusions), Dinacharya, practical action | Drugs & Magic Remedies Act 1954 notice |
| **Golden Heart Master Consultant** | `app/charm/chat/humanized_consultant.py`, `app/charm/chat/response_composer.py` | `IMPLEMENTED` | 7-Tier prioritized response, empathetic re-framing, unblocking actions | Non-canned, customized to user inquiry |

---

## 3. Event Taxonomy & Ontology Mapping

The event intent service (`app/charm/intent/event_intent_service.py`) structures user inquiries into standardized event definitions:

1. **Career (`EVT-CAREER`)**:
   - `new_job_or_senior_role`: Transition into a new job or senior executive appointment.
   - `promotion`: Institutional promotion, band advancement, or executive authority expansion.
   - `career_change`: Strategic career pivot into a new operational domain.
   - `business_venture`: Commercial venture expansion and independent market agility.
   - `executive_appointment`: High-level board or institutional directorship.
2. **Wealth (`EVT-WEALTH`)**:
   - `capital_gain`: Capital accumulation and liquidity inflow.
   - `debt_clearance`: Strategic debt neutralization and credit restructuring.
   - `financial_stability`: Long-term asset foundation and risk hedging.
   - `investment_window`: Favorable capital deployment and equity holding.
3. **Relationship & Synastry (`EVT-MARRIAGE`)**:
   - `marriage_timing`: Auspicious marriage alliance and domestic union.
   - `relationship_harmony`: Partner synastry and interpersonal alignment.
   - `partner_meeting`: Serendipitous social and professional encounters.
4. **Health & Vitality (`EVT-HEALTH`)**:
   - `vitality_restoration`: Pranic equilibrium, Ayurvedic dosha harmony.
   - `stress_reduction`: Circadian alignment, digital sundown pacing.
   - `circadian_harmony`: Dinacharya 24-hour routine optimization.
5. **Property & Vastu (`EVT-PROPERTY`)**:
   - `property_purchase`: Real estate acquisition and fixed asset foundation.
   - `relocation`: Long-distance geographic movement and residential pivot.
   - `home_consecration`: Geometric yantra installation and directional harmonization.
6. **General Forecasting (`EVT-GENERAL`)**:
   - `annual_forecast`: Personal Year epicycle roadmap.
   - `destiny_milestone`: Major cycle turning points.
   - `dasha_alignment`: Overarching Mahadasha climate.

---

## 4. Consensus Decision Engine Analysis

The repository operates two complementary consensus engines:

### A. Modular Event Consensus Engine (`app/charm/consensus/engine.py`)
Used by Charm AI for career and milestone event predictions:
- **Primary Window Authority**: Numerology Dasha timing windows are immutable. Astrological adapters evaluate agreement or friction against that window, but never alter start or end dates.
- **Strict Verification Statuses**:
  1. `NUMEROLOGY_PRIMARY_CORROBORATED`: Supported by 2+ independent astrological traditions without conflict.
  2. `NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED`: Supported with mixed cross-currents.
  3. `NUMEROLOGY_PRIMARY_CONFLICTED`: Contested by astrological friction or delays.
  4. `NUMEROLOGY_PRIMARY_ONLY`: Evaluated purely through Numerology Dasha without astrological cross-checks.
  5. `INSUFFICIENT_EVIDENCE`: Required birth inputs are missing; prediction is abstained.
  6. `NOT_ELIGIBLE_FOR_PREDICTION`: Inquiries violating statutory, ethical, or health/death prediction prohibitions.
- **Separation of Assessment and Verification**: Event assessment (`FAVOURABLE`, `UNFAVOURABLE`, `MIXED`, `NEUTRAL`) is tracked as an orthogonal axis to verification status.

### B. Master Report Multi-System Consensus Engine (`app/engine/consensus.py`)
Used for comprehensive 55+ page downloadable reports and full-profile audits:
- Collapses traditions into 6 independent system families:
  1. `numerology_core` (Lo Shu 3x3 Magic Square)
  2. `acoustics` (Chaldean / Cheiro Name Resonance)
  3. `numerology_comparative` (Vedic Sankhya Shastra)
  4. `astrology_classical` (Vedic Parashari & KP Sub-Lord)
  5. `astrology_nadi` (Bhrigu Nandi Nadi)
  6. `astrology_remedial` (Lal Kitab Masnooi Alchemy)
- Calculates the convergence ratio (`supporting_families / eligible_families`).
- Evaluates domain verdicts across Career, Wealth, Health, and Relationships with RAG citations.

---

## 5. Golden Heart Communication Doctrine Verification

The Golden Heart Doctrine in `app/charm/chat/humanized_consultant.py` and `app/charm/chat/response_composer.py` ensures:
1. **Empathy Before Diagnosis**: Begins with warm acknowledgment of the seeker's context; never leads with an ominous astrological term like "bad chart" or "kaal sarp curse".
2. **Constructive Reframing**: Friction or delays (e.g. Saturn/Shani or Rahu transits) are explained as natural structural conditioning, filtering out compromise roles so the seeker steps into durable authority.
3. **Structured 7-Tier Communication**:
   - Tier 1: Core Career Takeaway
   - Tier 2: Timing Status & Verification Level
   - Tier 3: Supported by Verified Data
   - Tier 4: What Cannot Yet Be Concluded
   - Tier 5: Input & Calculation Trace (Honest Missing Breakdown)
   - Tier 6: Three Practical Unblocking Steps (Grounding First)
   - Tier 7: Single Empathetic Follow-Up Question
4. **Zero Fatalism**: Strict prohibition of fear-based marketing, karmic threats, or compulsory remedy purchases.

---

## 6. Recommendations & Implementation Actions

### 6.1 Deterministic Planetary Combustion (Astangata / Asta) Engine
Planetary combustion occurs when a planet draws within an acute angular threshold of Surya (the Sun). In traditional Indian astronomy and predictive astrology (*Brihat Parashara Hora Shastra* Ch. 3 and *Surya Siddhanta* Ch. 10), a combust planet (*Asta* / *Astangata*) has its physical light overwhelmed by the solar orb, altering its significations and temporal potency.

To eliminate any LLM guesswork or approximation, combustion is computed deterministically in `app/charm/charts/fact_provider.py` using absolute circular angular separation:

$$\Delta\theta = \min\left(|\lambda_{\text{planet}} - \lambda_{\text{Sun}}| \pmod{360^\circ},\; 360^\circ - (|\lambda_{\text{planet}} - \lambda_{\text{Sun}}| \pmod{360^\circ})\right)$$

#### Classical Angular Separation Thresholds
| Graha (Planet) | Direct Motion (*Margi*) | Retrograde Motion (*Vakri*) | Classical Authority | Physical / Astrological Rationale |
|---|---|---|---|---|
| **Chandra (Moon)** | $12^\circ 00'$ | $12^\circ 00'$ | *BPHS* / *Surya Siddhanta* | Amavasya phase boundary; proximity to Sun creates solar glare obscuration. |
| **Mangal (Mars)** | $17^\circ 00'$ | $17^\circ 00'$ | *BPHS* Ch. 3 | High solar luminosity threshold required to overwhelm exterior planet disc. |
| **Budha (Mercury)** | $14^\circ 00'$ | $12^\circ 00'$ | *BPHS* / *Phaladeepika* | Inferior planet orbit; retrograde proximity brings Mercury closer to Earth, reducing combustion boundary. |
| **Guru (Jupiter)** | $11^\circ 00'$ | $11^\circ 00'$ | *BPHS* Ch. 3 | Large planetary radius and intrinsic luminosity maintain visibility until $11^\circ$. |
| **Shukra (Venus)** | $10^\circ 00'$ | $8^\circ 00'$ | *BPHS* / *Surya Siddhanta* | High albedo; when retrograde (inferior conjunction), disc appears larger, resisting combustion down to $8^\circ$. |
| **Shani (Saturn)** | $15^\circ 00'$ | $15^\circ 00'$ | *BPHS* Ch. 3 | Distant slow-moving superior planet; faint disc obscured within $15^\circ$ of solar rays. |
| **Rahu & Ketu** | *Exempt* (`False`) | *Exempt* (`False`) | Astronomical Canon | Mathematical intersection points (nodes) having no physical disc; they eclipse the Sun rather than combust. |

#### Deterministic Combustion Audit & Classification
1. **Combustion Status**: `COMBUST (Astangata)` when $\Delta\theta \le \theta_{\text{limit}}$, else `CLEAR (Udaya)`.
2. **Deep Combustion (*Paramastangata*)**: Evaluated when $\Delta\theta \le 1^\circ 00'$. Indicates acute solar conjunction where the planet's external agenda is completely subsumed by solar soul purpose (*Atmakaraka*).
3. **Audit Log Generation**: `get_chart_facts()` produces a structured `combustion_audit` dictionary exposing `planet`, `separation_degrees`, `combustion_limit_degrees`, `is_combust`, `deep_combustion`, and `motion_state`.

---

### 6.2 Consolidated Astrological Calculation Characteristics as 100% Deterministic Engine Math
The table below consolidates all mathematical characteristics implemented across Numeros Vision to ensure that **zero astrological or numerological calculations are ever delegated to generative AI models**:

| Calculation Characteristic | Governing Python Module | Deterministic Mathematical Formula / Algorithm | Classical & Astronomical Provenance |
|---|---|---|---|
| **Lahiri Ayanamsha** | `app/charm/charts/fact_provider.py` | Topocentric true precession offset $\approx 24.2250^\circ$ at J2026.0 epoch | Chitra Paksha (Govt of India Calendar Reform Committee) |
| **Zodiac Sign (Rasi) Divisions** | `fact_provider.py`, `astrology_correlation_engine.py` | $\text{Rasi Index} = \lfloor \lambda_{\text{nirayana}} / 30^\circ \rfloor \pmod{12}$, exact degree $= \lambda \pmod{30^\circ}$ | 12 Equal signs ($0^\circ$ Mesha to $360^\circ$ Meena) |
| **Nakshatra & Pada Mapping** | `fact_provider.py`, `astrology_correlation_engine.py` | $\text{Nakshatra Index} = \lfloor \lambda / 13.3333^\circ \rfloor$, $\text{Pada} = \lfloor (\lambda \pmod{13.3333^\circ}) / 3.3333^\circ \rfloor + 1$ | 27 Vedic Nakshatras ($13^\circ 20'$ each), 108 Padas ($3^\circ 20'$) |
| **House / Cuspal Geometry** | `phase7_kp_engine.py`, `astrology_correlation_engine.py` | Placidus cusps for KP Astrology; Equal House / Sripati for Vedic Parashari | Padhdhati cuspal tables & Sripati Bhava Chalita |
| **Planetary Dignities** | `astrology_correlation_engine.py` | Exact deep exaltation/debilitation degrees (e.g. Sun $10^\circ$ Aries / $10^\circ$ Libra; Moon $3^\circ$ Taurus / $3^\circ$ Scorpio; Jupiter $5^\circ$ Cancer / $5^\circ$ Capricorn) | *Brihat Jataka* Ch. 1 & *Phaladeepika* Ch. 2 |
| **Planetary Aspects (Drishti)** | `fact_provider.py`, `astrology_correlation_engine.py` | All planets cast $100\%$ 7th house aspect. Special full aspects: Mars (4th, 8th), Jupiter (5th, 9th), Saturn (3rd, 10th), Rahu/Ketu (5th, 9th trines) | *Brihat Parashara Hora Shastra* Ch. 26 |
| **KP 4-Level Cuspal Significators** | `app/charm/methods/kp_adapter.py`, `phase7_kp_engine.py` | Level 1: Planet in Star of occupant; Level 2: Occupant; Level 3: Planet in Star of Lord; Level 4: Bhava Lord. Sub-Lord division via Vimshottari arc ratios | K.S. Krishnamurti, *KP Readers Vol. I-VI* |
| **BNN Karaka Trines & Vectors** | `app/charm/methods/bnn_adapter.py`, `bnn_numerology_engine.py` | 1-5-9 directional trines (Fire, Earth, Air, Water); 2-12 wealth vectors; Jupiter (Jeeva) to Saturn (Karma) relation | R.G. Rao, *Bhrigu Nandi Nadi* |
| **Vimshottari Dasha Epicycles** | `app/charm/numerology/dasha_engine.py`, `astrology_correlation_engine.py` | 120-year cycle: Ketu (7y), Shukra (20y), Surya (6y), Chandra (10y), Mangal (7y), Rahu (18y), Guru (16y), Shani (19y), Budha (17y). Sub-period: $T_{\text{sub}} = (Y_A \times Y_B) / 120$ | Classical Parashari Dasha algorithm |
| **Chaldean 24-Hour Planetary Horas** | `astrology_correlation_engine.py` | Planetary hour determined by sunrise/sunset division; sequence follows Chaldean descent: Saturn $\to$ Jupiter $\to$ Mars $\to$ Sun $\to$ Venus $\to$ Mercury $\to$ Moon | Ancient Chaldean Order of Spheres |
| **Planetary Combustion (Asta)** | `app/charm/charts/fact_provider.py` | Great circle angular distance $\Delta\theta \le \theta_{\text{limit}}$ relative to Surya | *Surya Siddhanta* Ch. 10 & *BPHS* Ch. 3 |
| **Digit-Root Pricing Policy** | `app/engine/funnel_service.py`, `app/api/payments.py` | $\text{digital\_root}(p) = 1 + ((p - 1) \pmod 9) \in \{1, 3, 5, 6\}$ for all whole-rupee prices | Sacred Numeros Vision Pricing Policy v1.5 |

---

### 6.3 Implementation Actions & Verification Roadmap
1. **Pythagorean & Vedic Numerology Adapters in Charm AI**:
   Add dedicated `PythagoreanMethodAdapter` and `VedicNumerologyMethodAdapter` to `app/charm/methods/` so that Western Pythagorean (Master numbers 11, 22, 33; Karmic debts 13, 14, 16, 19) and Vedic Sankhya Shastra participate directly as modular cross-verification adapters alongside KP, Vedic Astrology, BNN, and Lal Kitab.
2. **Ephemeris Ingress Timestamps**:
   Enrich `app/charm/charts/fact_provider.py` with exact zodiac ingress timestamps and retrograde turnaround station dates.
3. **Consolidated Test Verification**:
   Maintain unit test suite `tests/test_additive_pricing_and_combustion_sync.py` verifying all digit roots, bundle savings transparency, and planetary combustion thresholds.

### 6.4 Hybrid Mobile-First UI/UX Blueprint (Milestone v6.8.0)
The visual identity of Numeros Vision combines premium editorial design with an app-like personal discovery journey and transactional clarity. Implemented in pp/static/index.html and pp/static/js/nav.js:

1. **Hero & Immediate Discovery Action**:
   - Eyebrow: ✦ PERSONALISED NUMEROLOGY ✦
   - Headline: Discover the Meaning Behind Your Numbers
   - Subtitle: Explore your core numbers, personal patterns and numerology profile across Vedic, Chaldean, Pythagorean, and Lo Shu traditions.
   - Primary CTA: Discover My Numbers ✦ smoothly anchoring to #calculator-card.

2. **Compact Cosmic Matrix Input Card (#calculator-card)**:
   - Subtitle: Enter your details to begin.
   - Full birth name text input (#f-name).
   - 3-column birth date selectors (#f-day, #f-month, #f-year).
   - Method selector (#f-method) supporting Vedic, Chaldean, and Pythagorean calculation paths.
   - Gold action button: Calculate My Numbers ✦ (#birth-submit-btn).
   - Preserved all runtime calculation hooks and DPDP 2025 consent gatekeeper handlers.

3. **Explore Your Numerology 2x2 Grid (.nv-explore-grid)**:
   - Compact cards for Life Path, Name Analysis, Lo Shu Grid, and Compatibility with direct reading exploration links.

4. **Your Next Insight Card (.nv-next-insight-card)**:
   - Banner linking to /reports_catalogue/ with clear value proposition and call-to-action.

5. **5-Tab Persistent Mobile Bottom Navigation Bar**:
   - Five mobile-first tabs: Home (/), Tools (/calculators/), Charm AI (center elevated button /#charm-ai), Reports (/reports_catalogue/), and Profile (#birth-profile).
   - Zero raw black #000000, Jupiter Gold accents, Sandalwood Ink typography, and strict zero banned marketing buzzwords.
