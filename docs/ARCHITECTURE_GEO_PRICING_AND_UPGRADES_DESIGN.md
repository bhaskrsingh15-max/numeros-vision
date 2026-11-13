# NUMEROS VISION — SERVER-SIDE GEO PRICING, BUNDLES & UPGRADES ARCHITECTURE
**Document ID**: NV-ARCH-GEO-PRICING-V1  
**Status**: DESIGN ONLY (Awaiting User Confirmation Before Implementation)  
**Applies To**: Cloudflare Workers (_worker.js), D1 Schema, Razorpay International Integration, Tax Storage

---

## 1. Executive Summary & Design Principles

1. **Server-Side Price Authority**:
   - The client never dictates currency or amount.
   - Cloudflare Worker inspects `request.cf.country` to map the inbound request to a geographical region.
   - The region, currency, and exact integer amount (in lowest currency denomination, e.g. cents/paise) are locked into the database order record at creation time.
2. **Deterministic Numerological Root Compliance**:
   - Every price and MRP across all currencies (INR, USD, EUR, AED) has a digit sum that strictly reduces to **1, 3, 5, or 6** (Sun, Jupiter, Mercury, Venus).
3. **No Domestic Alterations**:
   - Indian pricing remains strictly untouched (₹199 / ₹489 / ₹1,050 / ₹1,499).

---

## 2. Multi-Region Pricing Matrix (Offer / MRP)

All displayed prices include local consumption taxes (GST/VAT) where required by law.

| Region | Currency | Basic (3p) | Advanced (12p) | Premium (32p) | Planner (16p) | Tax Policy |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **India** (`IN`) | **INR** (₹) | **₹199** / 289 | **₹489** / 699 | **₹1,050** / 1,479 | **₹1,499** / 1,999 | 18% GST Included |
| **United States & Rest of World** (`US`, `DEFAULT`) | **USD** ($) | **$5.99** / 8.49 | **$12.99** / 18.95 | **$24.99** / 35.49 | **$28.99** / 37.99 | Export of Services (0% GST / No Sales Tax at Source) |
| **Europe** (`EU_COUNTRIES`) | **EUR** (€) | **€5.99** / 8.49 | **€14.99** / 21.99 | **€28.99** / 41.99 | **€32.99** / 43.95 | Standard VAT Included |
| **Middle East** (`AE`, `SA`, `QA`, `OM`, `KW`, `BH`) | **AED** (AED) | **AED 21.99** / 30.99 | **AED 46.99** / 66.99 | **AED 91.99** / 131.99 | **AED 105.99** / 140.99 | 5% UAE VAT Included |

### Numerological Digit Sum Verification
- **USD**:
  - Basic: $5.99 \to 5+9+9 = 23 \to \mathbf{5}$; MRP $8.49 \to 8+4+9 = 21 \to \mathbf{3}$
  - Advanced: $12.99 \to 1+2+9+9 = 21 \to \mathbf{3}$; MRP $18.95 \to 1+8+9+5 = 23 \to \mathbf{5}$
  - Premium: $24.99 \to 2+4+9+9 = 24 \to \mathbf{6}$; MRP $35.49 \to 3+5+4+9 = 21 \to \mathbf{3}$
  - Planner: $28.99 \to 2+8+9+9 = 28 \to \mathbf{1}$; MRP $37.99 \to 3+7+9+9 = 28 \to \mathbf{1}$
- **EUR**:
  - Basic: €5.99 $\to \mathbf{5}$; MRP €8.49 $\to \mathbf{3}$
  - Advanced: €14.99 $\to 1+4+9+9 = 23 \to \mathbf{5}$; MRP €21.99 $\to 2+1+9+9 = 21 \to \mathbf{3}$
  - Premium: €28.99 $\to 2+8+9+9 = 28 \to \mathbf{1}$; MRP €41.99 $\to 4+1+9+9 = 23 \to \mathbf{5}$
  - Planner: €32.99 $\to 3+2+9+9 = 23 \to \mathbf{5}$; MRP €43.95 $\to 4+3+9+5 = 21 \to \mathbf{3}$
- **AED**:
  - Basic: AED 21.99 $\to 2+1+9+9 = 21 \to \mathbf{3}$; MRP AED 30.99 $\to 3+0+9+9 = 21 \to \mathbf{3}$
  - Advanced: AED 46.99 $\to 4+6+9+9 = 28 \to \mathbf{1}$; MRP AED 66.99 $\to 6+6+9+9 = 30 \to \mathbf{3}$
  - Premium: AED 91.99 $\to 9+1+9+9 = 28 \to \mathbf{1}$; MRP AED 131.99 $\to 1+3+1+9+9 = 23 \to \mathbf{5}$
  - Planner: AED 105.99 $\to 1+0+5+9+9 = 24 \to \mathbf{6}$; MRP AED 140.99 $\to 1+4+0+9+9 = 23 \to \mathbf{5}$

---

## 3. Order Creation & Region-Locking Flow

```
User visits /your-reading/
   │
   ▼
Cloudflare Worker reads `request.cf.country`
   │
   ├─► Country in ['IN']               ──► Region: 'IN', Currency: 'INR'
   ├─► Country in EU_LIST              ──► Region: 'EU', Currency: 'EUR'
   ├─► Country in ['AE','SA','QA',...] ──► Region: 'ME', Currency: 'AED'
   └─► All other countries            ──► Region: 'US', Currency: 'USD'
   │
   ▼
Worker returns localized Catalog to client via GET /api/v1/pricing/geo-catalog
   │
   ▼
POST /api/v1/payments/create-order
   │
   ├─► Server re-determines region independently from `request.cf.country`.
   ├─► Server resolves amount in minor units (e.g., $12.99 -> 1299 cents).
   ├─► Generates Razorpay order with currency ('USD', 'EUR', 'AED', 'INR').
   ├─► Writes DB record to `orders`:
   │     { order_id, user_id, pack_id, region, currency, amount_units, status: 'CREATED' }
   └─► Locks (region, currency, amount) — client CANNOT alter it.
```

---

## 4. VPN & Card-Country Mismatch Handling

1. **Card Country Inspection**:
   - In Razorpay Webhook `order.paid` / `payment.authorized`, the payment entity provides `payment.card.country` or `payment.acquirer_data`.
2. **Mismatch Policy**:
   - If user used a VPN to request Indian pricing (INR ₹489 / ~$5.80) but paid with a non-Indian card (e.g. US / UK card):
     - **Option A (Strict Reject)**: Automatically void/refund the transaction with code `REGIONAL_PRICING_MISMATCH` and prompt customer to checkout in their home currency.
     - **Option B (Grace Fulfillment + Flag)**: Fulfill the digital delivery to prevent customer drop-off, but log `regional_arbitrage_detected` in `audit_log` and require re-authentication for subsequent orders.
   - *Recommendation*: **Option B** for launch to eliminate checkout friction, with an auto-switch to **Option A** if arbitrage exceeds 2% of transaction volume.

---

## 5. Multi-Currency Refund Handling

1. **Original Currency Principle**:
   - All refunds are dispatched through Razorpay's `/v1/payments/{payment_id}/refund` API specifying the exact original `amount` in the original `currency`.
   - The customer is refunded in the exact currency charged, shielding them from exchange rate fluctuations.
2. **Database Ledger**:
   - `refunds` table records:
     `{ refund_id, order_id, currency, amount_units, fx_rate_at_refund, gateway_refund_id, created_at }`.

---

## 6. Regulatory & Statutory Requirements for Razorpay International

To enable international card processing (USD, EUR, AED) via Razorpay, the following compliances are required:

1. **Mandatory Documentation & Approvals**:
   - **LUT (Letter of Undertaking)**: Filed under Indian GST Rules on the GST Portal (Form GST RFD-11) for export of services without payment of integrated tax (IGST).
   - **IEC (Import Export Code)**: Issued by the Directorate General of Foreign Trade (DGFT) for Indian business entities exporting digital goods/services.
   - **FIRC / e-BRC (Foreign Inward Remittance Certificate)**: Generated by the authorized dealer bank for foreign currency settlements.
2. **Mandatory Website Policy Pages**:
   - Explicit company legal name and registered address in footer.
   - Comprehensive Delivery & Shipping Policy (stipulating immediate digital delivery via download link & email within minutes).
   - Cardholder Dispute & Chargeback Resolution Corridors (stipulating contact at `support@numerosvision.com`).
3. **Tax Data Storage Structure**:
   - Every order record records tax categorization in `orders`:
     - `tax_category`: `'DOMESTIC_GST'` (for IN) vs `'EXPORT_ZERO_RATED'` (for US/EU/ME).
     - `tax_rate`: `0.18` (for IN) vs `0.00` (for Export).
     - `customer_ip`: Masked / hashed for DPDP compliance.
     - `billing_country`: 2-letter ISO code.

---

## 7. Charm AI Packs Architecture (Design Only)

| Pack ID | Questions Count | Price (INR) | Digital Root | Validity | Deliverables |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`charm_p5`** | **5 Questions** | **₹199** | $1+9+9 = 19 \to \mathbf{1}$ | 6 Months | 5 In-Depth Consultation Questions, Transit Radar |
| **`charm_p12`** | **12 Questions** | **₹399** | $3+9+9 = 21 \to \mathbf{3}$ | 12 Months | 12 In-Depth Questions, Muhurat & Date Selection |
| **`charm_p25`** | **25 Questions** | **₹699** | $6+9+9 = 24 \to \mathbf{6}$ | 12 Months | 25 In-Depth Questions, Multi-Profile Synastry |

---

## 8. Bundle & Tier Upgrade Architecture (Design Only)

### Products & Pricing
1. **Comprehensive Bundle (`bundle_premium_planner`)**:
   - Premium Sovereign Blueprint (₹1,050) + 2027 Annual Planner (₹1,499) = ₹2,549 value.
   - **Bundle Offer Price**: **₹1,949** ($1+9+4+9 = 23 \to \mathbf{5}$, Mercury / Commercial Harmony).
2. **Tier Upgrades (Incremental Delta)**:
   - **Basic to Advanced Upgrade**: **₹289** ($2+8+9 = 19 \to \mathbf{1}$).
     - Unlocks 12-page Advanced Dossier for a profile that already owns the 3-page Basic Report.
   - **Advanced to Premium Upgrade**: **₹561** ($5+6+1 = 12 \to \mathbf{3}$).
     - Unlocks 32-page Sovereign Blueprint for a profile that already owns the 12-page Advanced Dossier ($1,050 - 489 = 561$).
   - **Basic to Premium Upgrade**: **₹851** ($8+5+1 = 14 \to \mathbf{5}$).
     - Unlocks 32-page Sovereign Blueprint directly from the 3-page Basic Report ($1,050 - 199 = 851$).

### Entitlement & Upgrade Logic
1. **Eligibility Check**:
   - `GET /api/v1/upgrades/eligible`:
     - Checks customer's active entitlements for the subject.
     - If customer owns `report_basic`, emit upgrade options for `upgrade_basic_to_advanced` (₹289) and `upgrade_basic_to_premium` (₹851).
     - If customer owns `report_advanced`, emit `upgrade_advanced_to_premium` (₹561).
     - If customer already owns `report_premium`, no upgrades emitted.
2. **Upgrade Order Execution**:
   - Order creation verifies existing entitlement.
   - On webhook fulfillment:
     - Creates new entitlement for target tier (e.g. `report_premium`).
     - Queues report generation job for target tier.
     - Does **NOT** delete lower-tier entitlement; marks it `SUPERSEDED_BY_UPGRADE` in `entitlements` ledger to preserve historical proof.
3. **Refund Handling on Upgraded Orders**:
   - If an upgraded order is refunded:
     - Target tier entitlement (`report_premium`) is revoked.
     - Prior tier entitlement (`report_advanced`) is restored to `ACTIVE`.
     - Ensures customer is never left with zero access after a partial upgrade dispute.
