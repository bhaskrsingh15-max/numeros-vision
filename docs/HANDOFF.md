# NUMEROS VISION — STANDING DECISIONS & HANDOFF (`release/monetisation-fix`)

**Updated:** 2026-11-12  
**Deployment Status:** **LOCAL ONLY** (Do NOT deploy to preview or production until owner explicitly says `"go"`).

---

## 1. Non-Negotiable Standing Decisions

1. **Single-Digit `1–9` Rule Everywhere**:
   - Every reduced numerological output (`Driver / Mulank`, `Conductor / Bhagyank`, `Kua`, `Chaldean Calling Name root`, `Personal Year`, `Personal Month`, `Personal Day`, compatibility roots) reduces strictly to **`1–9`**.
   - Master numbers (`11, 22, 33`), karmic numbers (`13, 14, 16, 19`), and compounds (`29`, etc.) appear **only as path notes** (e.g., `"passes through 11 on the way to 2"`), never as final output values.
   - Kua `5` maps to `2` (male) and `8` (female); missing gender returns `"Kua needs gender"`.

2. **Canonical Lo Shu & Personal Cycles**:
   - Natal Lo Shu (`4 9 2 / 3 5 7 / 8 1 6`) uses **8-digit `DDMMYYYY` DOB digits only** (`0` excluded; Driver/Conductor/Kua never injected into natal counts).
   - UI cells show a **single digit** (`1`) plus a count chip (`x4` / `×4`), never repeated digits (`1111`).
   - Canonical Personal Cycles (`app/engine/digit_root.py` & `app/static/js/nv_kua.js`):
     - `Personal Year = digit_root(day + month + target_year)`
     - `Personal Month = digit_root(personal_year + calendar_month)`
     - `Personal Day = digit_root(personal_year + personal_month + digit_root(calendar_day))` (never double-adding month/year).

3. **Additive Layering & Golden Snapshots (`NV_ENABLE_LAYERS_2_3`)**:
   - Existing Layer 1 Five-Element counts, gaps, ranked element remedies, planet benefic/malefic & repetition logic (`docs/PLANET_LOGIC_SPEC.md`), report layouts (Basic strictly **3 pages**, Advanced **12**, Premium **32**), Charm AI credit/cookie/topic behaviour, and 2027 Planner waitlist stay 100% intact.
   - `tests/fixtures/layer1_golden_snapshots_16_dobs.json` locks 16 fixed DOBs across all 5 surfaces. With `NV_ENABLE_LAYERS_2_3=0` (default), snapshots match byte-for-byte. With `NV_ENABLE_LAYERS_2_3=1`, Layer 1 remains unchanged and Basic remains strictly 3 pages across all 16 DOBs.

4. **Shared Reading Pipeline & Live Progress (Section 17)**:
   - Shared path in `app/engine/reading_pipeline.py`: `Input -> Calculate -> Analyse -> Consolidate -> Write -> Check -> Deliver`.
   - `Write` receives only PII-free `ReadingPlan` (`temperature=0`, SHA-256 cached); `Check` validates via `app/engine/indication_validator.py` and falls back per-section to plain deterministic library text on any error/timeout/rejection.
   - Additive D1 migration: `migrations/0012_report_jobs_pipeline_stages.sql` (resumable stages, zero PII).
   - Charm AI SSE (`/api/charm/chat/stream`) emits fixed plain-language stage events (never model chain-of-thought, never `"verified"`/`"authentic"`), followed by adaptive client typing reveal (`Show all` button + `prefers-reduced-motion` instant display) of the validated text only.

5. **Remedy Sequence, Gemstones & Package Entitlements (Sections 16, 18C & 19)**:
   - Fixed 4-step remedy order: (1) Daily discipline & missing-plane habits -> (2) Existing 5-element remedies (+ optional `element_support`) -> (3) Separate optional planet practices (`app/data/remedy_library.json`, `DRAFT`, 56 items across `vedic`, `universal`, `western`) -> (4) General support only when needed.
   - Gemstones offered across styles as optional information with `gentle_alternatives`, practitioner caution on strong stones (`4` Hessonite, `7` Cat's eye, `8` Blue sapphire), never sold/linked, zero health/wealth promises, and excluded from Basic (along with mantras).
   - Server-side Section 19 entitlement matrix strictly governs General vs Personalised vs Monthly Affirmations and Year vs Current-Month vs Full Manifestation across Free, Basic, Advanced, Premium, 2027 Planner, and Charm AI tiers.

6. **Brand Palette, Plain Language & Zero Named Persons**:
   - Strictly zero green (`#16835B`) on UI badges/cards/numbers and zero raw black (`#000000`); all prices in theme gold (`#8B6914`).
   - `app/data/name_denylist.json` + `scan_repo_for_named_persons()` block real/famous names, company names (`NVIDIA`), and third-party course brands (`Talking Numbers`) across non-statutory repo files.
   - Charm AI free daily credits reset at **`00:00 IST`** (`Asia/Kolkata`); `100/day` IP cap applies **only when `nv_visitor_id` cookie is absent**.
