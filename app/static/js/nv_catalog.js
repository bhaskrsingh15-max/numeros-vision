/**
 * NUMEROS VISION — CLIENT-SIDE CANONICAL PRICING CATALOG (v2.1.0)
 * Tagline: ANVIEL EVERY CHARM
 *
 * Auto-synchronized from app/config/packs.json at build time.
 * Single source of truth for all client-side pricing, page counts, deliverables,
 * bundle definitions, and Charm AI packs.
 */

(function(window) {
  'use strict';

  const PACKS_JSON = {
    version: '2.1.0',
    currency: 'INR',
    core_reports: {
      report_basic: {
        pack_id: 'report_basic',
        tier_id: 'basic',
        name: 'Basic Report',
        display_name: 'Basic Report · Entry',
        pages: 3,
        price_inr: 199,
        amount_paise: 19900,
        price_usd: 5,
        digital_root: 1,
        status: 'active'
      },
      report_advanced: {
        pack_id: 'report_advanced',
        tier_id: 'advanced',
        name: 'Advanced Master Dossier',
        display_name: 'Advanced Master Dossier · Recommended',
        pages: 12,
        price_inr: 510,
        amount_paise: 51000,
        price_usd: 14,
        digital_root: 6,
        status: 'active'
      },
      report_premium: {
        pack_id: 'report_premium',
        tier_id: 'premium',
        name: 'Premium Sovereign Blueprint',
        display_name: 'Premium Sovereign Blueprint · Comprehensive',
        pages: 32,
        price_inr: 1050,
        amount_paise: 105000,
        price_usd: 28,
        digital_root: 6,
        status: 'active'
      }
    },
    bundles: {
      starter_bundle: {
        pack_id: 'starter_bundle',
        name: 'Starter Bundle',
        display_name: 'Starter Bundle · 2 Basic Reports',
        price_inr: 339,
        amount_paise: 33900,
        digital_root: 6,
        status: 'coming_soon',
        reports_count: 2,
        tier: 'basic',
        pages: 3,
        deliverables: [
          '2 Complete 3-Page Basic PDF Reports',
          'Choose any two topics across Love, Money, Work, or Growth',
          'Full calculation breakdown and practical remedies',
          'Ready within minutes in your account dashboard with archival PDF download'
        ]
      },
      discovery_bundle: {
        pack_id: 'discovery_bundle',
        name: 'Discovery Bundle',
        display_name: 'Discovery Bundle · 3 Advanced Reports',
        price_inr: 1299,
        amount_paise: 129900,
        digital_root: 3,
        status: 'coming_soon',
        reports_count: 3,
        tier: 'advanced',
        pages: 12,
        deliverables: [
          '3 Complete 12-Page Advanced Master Reports',
          'Choose any three topics from the entire catalogue',
          'Enabled Numbers in Depth & Auspicious Initiation Windows for each topic',
          'Vedic Gharelu remedies & Kua directional protocols for selected domains'
        ]
      },
      comprehensive_bundle: {
        pack_id: 'comprehensive_bundle',
        name: 'Comprehensive Bundle',
        display_name: 'Comprehensive Bundle · 5 Advanced Reports',
        price_inr: 1999,
        amount_paise: 199900,
        digital_root: 1,
        status: 'coming_soon',
        reports_count: 5,
        tier: 'advanced',
        pages: 12,
        deliverables: [
          '5 Complete 12-Page Advanced Master Reports',
          'Complete multi-domain clarity across Love, Career, Wealth & Family',
          'Enabled Numbers in Depth & Auspicious Initiation Windows for each domain',
          'Vedic Gharelu remedies & Kua directional protocols'
        ]
      }
    },
    charm_ai: {
      charm_free: {
        pack_id: 'charm_free',
        name: 'Free Preview',
        display_name: 'Charm AI · Free Preview',
        price_inr: 0,
        amount_paise: 0,
        questions_count: 3,
        digital_root: 0,
        status: 'active',
        deliverables: [
          '3 Free Exploratory Inquiries Daily per Account',
          'Instant Driver / Conductor token verification',
          '24/7 web access'
        ]
      },
      charm_single: {
        pack_id: 'charm_single',
        name: 'Charm AI Starter Pack',
        display_name: 'Charm AI · Starter Pack',
        price_inr: 199,
        amount_paise: 19900,
        questions_count: 5,
        digital_root: 1,
        status: 'active',
        deliverables: [
          '5 In-Depth Consultation Inquiries across any life area',
          'Acute execution timing windows (Hora & transit)',
          'Grounded non-fatalistic practical guidance',
          'Credits valid for 6 months'
        ]
      },
      charm_multi: {
        pack_id: 'charm_multi',
        name: 'Multi-Reading Pack',
        display_name: 'Charm AI · Multi-Reading Pack',
        price_inr: 399,
        amount_paise: 39900,
        questions_count: 10,
        digital_root: 0,
        status: 'inactive',
        deliverables: [
          '10 Detailed Question Predictions',
          'Customised 7-Layer safe remedies for all queries',
          'Auspicious date selection & Muhurat guidance',
          'Priority engine response queue',
          'Credits valid for 12 months'
        ]
      },
      charm_extended: {
        pack_id: 'charm_extended',
        name: 'Extended Reading Pack',
        display_name: 'Charm AI · Extended Pack',
        price_inr: 699,
        amount_paise: 69900,
        questions_count: 25,
        digital_root: 0,
        status: 'inactive',
        deliverables: [
          '25 Deep In-Depth Predictions',
          'Interactive chart companion with transit radar',
          'Multi-profile synastry consultation capability',
          'Downloadable consultation transcript',
          'Credits valid for 12 months with rollover'
        ]
      }
    }
  };

  const NVCatalog = {
    currency: PACKS_JSON.currency,
    packsJson: PACKS_JSON,
    deliveryPromise: 'Your personalized PDF report is ready within minutes in your account dashboard.',
    investmentNotice: '100% One-Time Investment · Zero Auto-Debit · Zero Recurring Fees',
    sacredRootNotice: 'Publication fees reduce to sacred harmonic root numbers (1, 3, 5, or 6) aligned with planetary vibrations.',
    freeAllowanceNotice: '3 free exploratory inquiries after verified sign-up.',

    tiers: {
      basic: {
        id: 'report_basic',
        sku: 'report_basic',
        alias: 'report_essential',
        name: PACKS_JSON.core_reports.report_basic.name,
        display_name: 'Basic Report · 3 Pages',
        price_inr: PACKS_JSON.core_reports.report_basic.price_inr,
        price_usd: PACKS_JSON.core_reports.report_basic.price_usd,
        pages: PACKS_JSON.core_reports.report_basic.pages,
        digital_root: PACKS_JSON.core_reports.report_basic.digital_root,
        timeline: 'Foundational Lo Shu & Element Balancing',
        summary: '3-Page Personalised Executive PDF covering Driver, Conductor, Kua, Lo Shu 3x3 grid, and element balancing.'
      },
      advanced: {
        id: 'report_advanced',
        sku: 'report_advanced',
        alias: 'report_master',
        name: PACKS_JSON.core_reports.report_advanced.name,
        display_name: 'Advanced Master Dossier · 12 Pages',
        price_inr: PACKS_JSON.core_reports.report_advanced.price_inr,
        price_usd: PACKS_JSON.core_reports.report_advanced.price_usd,
        pages: PACKS_JSON.core_reports.report_advanced.pages,
        digital_root: PACKS_JSON.core_reports.report_advanced.digital_root,
        popular: true,
        timeline: 'Element Balancing + Enabled Numbers in Depth',
        summary: '12-Page Master Synthesis PDF Dossier with element balancing and enabled numbers in depth.'
      },
      premium: {
        id: 'report_premium',
        sku: 'report_premium',
        alias: 'report_divine',
        name: PACKS_JSON.core_reports.report_premium.name,
        display_name: 'Premium Sovereign Blueprint · 32 Pages',
        price_inr: PACKS_JSON.core_reports.report_premium.price_inr,
        price_usd: PACKS_JSON.core_reports.report_premium.price_usd,
        pages: PACKS_JSON.core_reports.report_premium.pages,
        digital_root: PACKS_JSON.core_reports.report_premium.digital_root,
        timeline: '10-Year Macro Planetary Timing Radar, Missing Numbers, Remedies & Predictions',
        summary: '32-Page Sovereign Executive Blueprint with dual Chaldean + Pythagorean synthesis, missing numbers in depth, remedies, and 10-year macro timing radar.'
      }
    },

    bundles: {
      starter_bundle: Object.assign({ id: 'starter_bundle', sku: 'starter_bundle' }, PACKS_JSON.bundles.starter_bundle),
      discovery_bundle: Object.assign({ id: 'discovery_bundle', sku: 'discovery_bundle', popular: true }, PACKS_JSON.bundles.discovery_bundle),
      comprehensive_bundle: Object.assign({ id: 'comprehensive_bundle', sku: 'comprehensive_bundle' }, PACKS_JSON.bundles.comprehensive_bundle)
    },

    charmAiPacks: {
      charm_free: Object.assign({ id: 'charm_free', queries: 3 }, PACKS_JSON.charm_ai.charm_free),
      charm_5q: Object.assign({ id: 'charm_single', sku: 'charm_single', queries: 5, price_usd: 5 }, PACKS_JSON.charm_ai.charm_single),
      charm_10q: Object.assign({ id: 'charm_multi', sku: 'charm_multi', queries: 10, price_usd: 10 }, PACKS_JSON.charm_ai.charm_multi),
      charm_25q: Object.assign({ id: 'charm_extended', sku: 'charm_extended', queries: 25, price_usd: 18 }, PACKS_JSON.charm_ai.charm_extended)
    },

    getSku: function(key) {
      if (!key) return this.tiers.advanced;
      const k = String(key).toLowerCase().trim();
      if (this.tiers[k]) return this.tiers[k];
      for (const t in this.tiers) {
        if (this.tiers[t].id === k || this.tiers[t].alias === k || this.tiers[t].sku === k) {
          return this.tiers[t];
        }
      }
      if (this.bundles[k]) return this.bundles[k];
      if (this.charmAiPacks[k]) return this.charmAiPacks[k];
      for (const c in this.charmAiPacks) {
        if (this.charmAiPacks[c].id === k || this.charmAiPacks[c].sku === k) {
          return this.charmAiPacks[c];
        }
      }
      return this.tiers.advanced;
    },

    formatPrice: function(key, currency) {
      const item = this.getSku(key);
      if (item && item.status === 'coming_soon') {
        return 'Coming soon';
      }
      const isUsd = currency === 'USD';
      if (isUsd) {
        return '$' + (item.price_usd || 14);
      }
      const inr = item.price_inr !== undefined ? item.price_inr : 510;
      return '₹' + Number(inr).toLocaleString('en-IN');
    }
  };

  window.NVCatalog = NVCatalog;
})(typeof window !== 'undefined' ? window : this);
