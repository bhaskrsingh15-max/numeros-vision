# STEP 1 AUDIT REPORT — 10-Logo Endpoint Verification & Regression Lock

**Date**: November 13, 2026  
**Branch**: `release/monetisation-fix` (`8f3cb7b`)  
**Verdict**: **Production endpoints fail (`405` on Cloudflare Worker, `404` on Render `pdf_service`).** Condition triggered: proceed with add-only `app/logo_intelligence/` + `pdf_service/app/logo_intelligence/` module build on top of locked engines.

---

## 1. Ten-Logo Endpoint Matrix (`5 SVG + 5 PNG`)

| # | Sample File | Format | Prod Worker `/preview` | Prod Worker `/analyze-existing` | Render `pdf_service` | Untracked Local Prototype Findings |
|---|---|---|---|---|---|---|
| 1 | `01_nv_full_lockup.svg` | SVG | `405` (len 0) | `405` (len 0) | `404` / `404` | Backend returns `dominant_colors` while UI reads `m.palette_sampled` (always shows 'Standard palette') |
| 2 | `02_nv_refined_brand.svg` | SVG | `405` (len 0) | `405` (len 0) | `404` / `404` | Backend returns `dominant_colors` while UI reads `m.palette_sampled` (always shows 'Standard palette'); Client-side JS Chaldean diverges from canonical server engine (server compound=35) |
| 3 | `03_aura_peak_gold_low_contrast.svg` | SVG | `405` (len 0) | `405` (len 0) | `404` / `404` | Backend returns `dominant_colors` while UI reads `m.palette_sampled` (always shows 'Standard palette'); Analyze measured low contrast (2.38:1) with no pass/fail gate; Preview silently swapped text fill to pass (9.93:1) while leaving symbol stroke `#C9A227` at 2.38:1 |
| 4 | `04_apex_stencil_cut_letters.svg` | SVG | `405` (len 0) | `405` (len 0) | `404` / `404` | Backend returns `dominant_colors` while UI reads `m.palette_sampled` (always shows 'Standard palette'); Stencil slice & unclosed path not detected (`nothing_cut` gate absent) |
| 5 | `05_fake_vector_raster_and_script.svg` | SVG | `405` (len 0) | `405` (len 0) | `404` / `404` | Backend returns `dominant_colors` while UI reads `m.palette_sampled` (always shows 'Standard palette'); CRITICAL: Fake `.svg` with embedded `<image>` PNG + `<script>` falsely marked `is_vector: True`; Client-side JS Chaldean diverges from canonical server engine (server compound=39) |
| 6 | `06_nv_horizontal_lockup.png` | PNG | `405` (len 0) | `405` (len 0) | `404` / `404` | Raster PNG upload returns zero OCR text (`extracted_text` key absent); Backend returns `dominant_colors` while UI reads `m.palette_sampled` (always shows 'Standard palette') |
| 7 | `07_nv_refined_mark.png` | PNG | `405` (len 0) | `405` (len 0) | `404` / `404` | Raster PNG upload returns zero OCR text (`extracted_text` key absent); Backend returns `dominant_colors` while UI reads `m.palette_sampled` (always shows 'Standard palette'); Client-side JS Chaldean diverges from canonical server engine (server compound=43) |
| 8 | `08_pwa_app_icon_512.png` | PNG | `405` (len 0) | `405` (len 0) | `404` / `404` | Raster PNG upload returns zero OCR text (`extracted_text` key absent); Backend returns `dominant_colors` while UI reads `m.palette_sampled` (always shows 'Standard palette') |
| 9 | `09_de_wow_wafel_demo.png` | PNG | `405` (len 0) | `405` (len 0) | `404` / `404` | Raster PNG upload returns zero OCR text (`extracted_text` key absent); Backend returns `dominant_colors` while UI reads `m.palette_sampled` (always shows 'Standard palette') |
| 10 | `10_tiny_32px_favicon.png` | PNG | `405` (len 0) | `405` (len 0) | `404` / `404` | Raster PNG upload returns zero OCR text (`extracted_text` key absent); Backend returns `dominant_colors` while UI reads `m.palette_sampled` (always shows 'Standard palette'); 32x32 tiny icon accepted with no app-icon/small-size legibility warning; Client-side JS Chaldean diverges from canonical server engine (server compound=19) |

---

## 2. Empirical Defects Confirmed by the 10-Logo Run

1. **Production Worker (`app/static/_worker.js`)**: All 10 `POST /api/v1/logo/preview` and all 10 `POST /api/v1/logo/analyze-existing` requests fall through to static asset handling and return **`405` with empty body (`0` bytes)**.
2. **Production Render Python Service (`pdf_service/app/services/internal_pdf_worker_service.py`)**: Returns **`404`** for all logo routes (only `/health` and `/internal/v1/render-pdf` are mounted).
3. **Fake Vector & Inline Script Blindness (`05_fake_vector_raster_and_script.svg`)**: Local `ExistingLogoInspector.inspect_svg()` hard-codes `is_vector: True`, certifying a base64 PNG wrapped in `<svg>` with an inline `<script>` tag as a pure vector.
4. **Zero Raster OCR (`06`–`10` PNGs)**: `ExistingLogoInspector.inspect_raster()` never extracts text (`extracted_text` missing on all 5 PNGs), so `DE WOW WAFEL` (`09_de_wow_wafel_demo.png`) cannot be read or name-checked from an uploaded PNG.
5. **Stencil / Cut-Form Blindness (`04_apex_stencil_cut_letters.svg`)**: Unclosed paths and negative-space bars slicing through `APEX FORGE` pass with zero warnings (`nothing_cut` gate absent).
6. **Gold Contrast Bypass (`03_aura_peak_gold_low_contrast.svg`)**: `/preview` silently substitutes `#523E28` on text to report `9.93:1` while leaving the `#C9A227` symbol stroke at `2.38:1` on `#FFFDF7` (below the `3.0:1` symbol hard gate).
7. **Schema Key Mismatch**: Backend emits `dominant_colors` while `logo-intelligence.html` reads `m.palette_sampled`, causing the UI to display `'Standard palette'` on every SVG.
8. **Client vs. Server Chaldean `'C'` Divergence**: Client JS maps `C=3` while `_worker.js` and `cheiro_engine.py` map `C=2` (affecting `ANVEIL CHARM`, `CHARM STUDIO`, `KAVACH AI`).

---

## 3. Build Safety Regression Lock Baseline

Locked in `tests/fixtures/pack_regression_lock_baseline.json` and verified via `scripts/verify_pack_regression_lock.py --verify`:
- Protected engine files hashed (`app/engine/*.py` + `pdf_service/app/engine/*.py`): **ZERO modifications permitted**.
- `report_basic` (3 pages), `report_advanced` (12 pages), `report_premium` (32 pages), and `planner_2027` (24 pages + engine JSON): **100% deterministic hash match across consecutive runs**.
