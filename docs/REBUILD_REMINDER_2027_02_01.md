# NUMEROS VISION — 1 FEBRUARY 2027 REBUILD & PRICE TRANSITION SPECIFICATION
**Document ID**: NV-REBUILD-20270201  
**Trigger Date**: 2027-02-01T00:00:00+05:30 (Midnight IST)  
**Applies To**: Production & Preview Web Deployments, JSON-LD Schemas, Server-Side Pack Catalogs, PDF Engine

---

## 1. Executive Summary & Purpose

The initial launch offer pricing for Numeros Vision core report products expires at **23:59:59 IST on 31 January 2027**.
Starting **1 February 2027**, the displayed price becomes the canonical Maximum Retail Price (MRP).

---

## 2. Canonical Price Transition Table

All regular prices strictly adhere to the numerological single-digit root requirement (reducing to **1, 3, 5, or 6**):

| Product SKU | Launch Offer Price (Through 2027-01-31) | Canonical Price (From 2027-02-01) | Digit Calculation | Planetary Archetype |
| :--- | :--- | :--- | :--- | :--- |
| **`report_basic`** (3 Pages) | ₹199 (19,900 paise) | **₹289** (28,900 paise) | $2+8+9 = 19 \to 1$ | Sun (Surya) · Leadership & Vitality |
| **`report_advanced`** (12 Pages) | ₹489 (48,900 paise) | **₹699** (69,900 paise) | $6+9+9 = 24 \to 6$ | Venus (Shukra) · Harmony & Synthesis |
| **`report_premium`** (32 Pages) | ₹1,050 (105,000 paise) | **₹1,479** (147,900 paise) | $1+4+7+9 = 21 \to 3$ | Jupiter (Guru) · Expansion & Mastery |
| **`planner_2027`** (16 Pages) | ₹1,499 (149,900 paise) | **₹1,999** (199,900 paise) | $1+9+9+9 = 28 \to 1$ | Sun (Surya) · Sovereign Focus |

---

## 3. Required Rebuild Actions on 2027-02-01

1. **Server Price Authority**:
   - In `app/config/packs.json`, update `price_inr` and `amount_paise` to the MRP figures (289 / 28900, 699 / 69900, 1479 / 147900, 1999 / 199900).
   - In `app/config/packs.ts` and `app/config/pricing_config.py`, update `PACK_CATALOG` to reflect the new amounts.
   - In `app/static/_worker.js`, update `PACK_CATALOG.core_reports` integer paise and pricing gates.

2. **UI & Markup Transitions**:
   - In `your-reading.html`, `pricing.html`, `dashboard.html`, and `reports_catalogue.html`:
     - Remove the strikethrough `<span class="tier-mrp">` elements.
     - Remove the `"Launch offer valid until 31 Jan 2027"` subtext.
     - Display the standard regular pricing with `"One-time payment · GST included"`.

3. **JSON-LD Structured Data**:
   - In `year_2027.html`, `pricing.html`, and `index.html`:
     - In the Schema.org `Offer` objects:
       - Update `"price"` to `"289"`, `"699"`, `"1479"`, and `"1999"`.
       - Remove `"priceValidUntil": "2027-01-31T23:59:59+05:30"`.

4. **Automated Verification**:
   - Run `python -m unittest tests/test_price_digit_sums.py` to confirm all active prices reduce to 1, 3, 5, or 6.
   - Run `node tests/test_purchase_journey_stages.mjs` to confirm server-side override integrity.
   - Run `python build_bulletproof_dist.py` to regenerate `dist_cloudflare_pages/`.
