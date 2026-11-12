/**
 * NUMEROS VISION — CANONICAL PACK CATALOG (TypeScript)
 * Auto-generated from app/config/packs.json (v2.2.0)
 * Enforces server-side authority, integer paise, and voucher architectures.
 */

export interface PackDefinition {
  pack_id: string;
  tier_id?: string;
  name: string;
  descriptor?: string;
  display_name: string;
  price_inr: number;
  mrp_inr?: number;
  mrp_paise?: number;
  amount_paise: number;
  digital_root?: number;
  mrp_digital_root?: number;
  launch_offer_duration_days?: number;
  launch_offer_started_at?: string | null;
  launch_offer_ends_at?: string | null;
  badge?: string | null;
  status: 'active' | 'inactive' | 'coming_soon';
  pages?: number;
  deliverables: string[];
  voucher_allocation?: {
    basic_vouchers: number;
    advanced_vouchers: number;
    premium_vouchers: number;
  };
  questions_count?: number;
  progressive_unlock?: string;
}

export const PACK_CATALOG: {
  version: string;
  currency: string;
  updated_at?: string;
  ladder_order?: string[];
  launch_offer?: {
    enabled?: boolean;
    duration_days: number;
    started_at: string | null;
    ends_at?: string | null;
    until_date_label?: string;
    regular_from_date_label?: string;
    copy_template?: string;
  };
  feature_flags?: {
    notify_me_higher_tiers: boolean;
    notify_me_tiers: string[];
  };
  core_reports: Record<string, PackDefinition>;
  bundles: Record<string, PackDefinition>;
  charm_ai: Record<string, PackDefinition>;
  annual_planners?: Record<string, unknown>;
} = {
  "version": "2.2.0",
  "currency": "INR",
  "updated_at": "2026-11-12T00:55:00Z",
  "feature_flags": {
    "notify_me_higher_tiers": true,
    "notify_me_tiers": [
      "report_advanced",
      "report_premium"
    ]
  },
  "launch_offer": {
    "enabled": true,
    "duration_days": 7,
    "started_at": "2026-11-12T00:00:00+05:30",
    "ends_at": "2026-11-19T23:59:59+05:30",
    "until_date_label": "19 Nov 2026",
    "regular_from_date_label": "20 Nov 2026",
    "copy_template": "Launch price until {until_date}. Regular price \u20b9{mrp_formatted} from {from_date}."
  },
  "ladder_order": [
    "report_premium",
    "report_advanced",
    "report_basic"
  ],
  "core_reports": {
    "report_premium": {
      "pack_id": "report_premium",
      "tier_id": "premium",
      "name": "Anveil every charm",
      "descriptor": "Complete Numerology Report, 32 pages",
      "display_name": "Anveil every charm \u00b7 Complete Numerology Report, 32 pages",
      "pages": 32,
      "price_inr": 1050,
      "amount_paise": 105000,
      "mrp_inr": 2100,
      "mrp_paise": 210000,
      "launch_offer_duration_days": 7,
      "launch_offer_started_at": "2026-11-12T00:00:00+05:30",
      "launch_offer_ends_at": "2026-11-19T23:59:59+05:30",
      "digital_root": 6,
      "mrp_digital_root": 3,
      "status": "active",
      "deliverables": [
        "32-Page Complete Roadmap PDF (all 9 glowing & veiled charms)",
        "Dual-System Comprehensive Synthesis (Chaldean + Pythagorean)",
        "Full Name Balancing, Acoustic Spelling & Poorak Numbers Protocol",
        "10-Year Macro Planetary Timing Radar & Month-by-Month Auspicious Windows",
        "Veiled Charms Deep Diagnosis, 81-Pair Matrix & 4-Stage Pinnacle Cycles",
        "Multi-Generational Synastry, Commercial Vectors & Methodology Appendix"
      ],
      "progressive_unlock": "includes_basic"
    },
    "report_advanced": {
      "pack_id": "report_advanced",
      "tier_id": "advanced",
      "name": "Anveil my glowing charms",
      "descriptor": "Advanced Numerology Report, 12 pages",
      "display_name": "Anveil my glowing charms \u00b7 Advanced Numerology Report, 12 pages",
      "pages": 12,
      "price_inr": 510,
      "amount_paise": 51000,
      "mrp_inr": 1020,
      "mrp_paise": 102000,
      "launch_offer_duration_days": 7,
      "launch_offer_started_at": "2026-11-12T00:00:00+05:30",
      "launch_offer_ends_at": "2026-11-19T23:59:59+05:30",
      "digital_root": 6,
      "mrp_digital_root": 3,
      "status": "active",
      "deliverables": [
        "12-Page Glowing Charms Reading PDF",
        "All Alignment calculations + Auspicious Initiation Windows & Personal Year Cycles",
        "Complete 8 Elemental Planes & Lo Shu Grid Analysis",
        "Glowing Numbers in Depth & Benefic vs Malefic Operating Matrix",
        "Vedic Gharelu Remedies Bank & 40-Day Aura Cleansing",
        "Interpersonal Synergy, Co-Founder Matching & Kua Directional Blueprint"
      ],
      "progressive_unlock": "includes_basic"
    },
    "report_basic": {
      "pack_id": "report_basic",
      "tier_id": "basic",
      "name": "Anveil my alignments",
      "descriptor": "Basic Numerology Report, 3 pages",
      "display_name": "Anveil my alignments \u00b7 Basic Numerology Report, 3 pages",
      "pages": 3,
      "price_inr": 199,
      "amount_paise": 19900,
      "mrp_inr": 399,
      "mrp_paise": 39900,
      "launch_offer_duration_days": 7,
      "launch_offer_started_at": "2026-11-12T00:00:00+05:30",
      "launch_offer_ends_at": "2026-11-19T23:59:59+05:30",
      "digital_root": 1,
      "mrp_digital_root": 3,
      "status": "active",
      "deliverables": [
        "3-Page Personalised Alignments PDF",
        "Deterministic Mulank (Driver) & Bhagyank (Conductor) Calculations",
        "Lo Shu 3x3 Grid Matrix & 8 Elemental Planes Audit",
        "Chaldean Calling Name Compound & Root Summary",
        "5-Element Balancing Actions & 90-Day Roadmap"
      ],
      "progressive_unlock": "entry"
    }
  },
  "bundles": {
    "starter_bundle": {
      "pack_id": "starter_bundle",
      "name": "Starter Bundle",
      "display_name": "Starter Bundle \u00b7 2 Alignment Reports",
      "price_inr": 339,
      "amount_paise": 33900,
      "digital_root": 6,
      "status": "coming_soon",
      "voucher_allocation": {
        "basic_vouchers": 2,
        "advanced_vouchers": 0,
        "premium_vouchers": 0
      },
      "deliverables": [
        "2 Complete 3-Page Alignment PDF Reports",
        "Choose any two topics across Love, Money, Work, or Growth",
        "Full calculation breakdown and practical remedies",
        "Ready within minutes in your account dashboard with archival PDF download"
      ]
    },
    "discovery_bundle": {
      "pack_id": "discovery_bundle",
      "name": "Discovery Bundle",
      "display_name": "Discovery Bundle \u00b7 3 Glowing Charm Reports",
      "price_inr": 1299,
      "amount_paise": 129900,
      "digital_root": 3,
      "status": "coming_soon",
      "voucher_allocation": {
        "basic_vouchers": 0,
        "advanced_vouchers": 3,
        "premium_vouchers": 0
      },
      "deliverables": [
        "3 Complete 12-Page Glowing Charm Reports",
        "Choose any three topics from the entire catalogue",
        "Glowing Numbers in Depth & Auspicious Initiation Windows for each topic",
        "Vedic Gharelu remedies & Kua directional protocols for selected domains"
      ]
    },
    "comprehensive_bundle": {
      "pack_id": "comprehensive_bundle",
      "name": "Comprehensive Bundle",
      "display_name": "Comprehensive Bundle \u00b7 5 Glowing Charm Reports",
      "price_inr": 1999,
      "amount_paise": 199900,
      "digital_root": 1,
      "status": "coming_soon",
      "voucher_allocation": {
        "basic_vouchers": 0,
        "advanced_vouchers": 5,
        "premium_vouchers": 0
      },
      "deliverables": [
        "5 Complete 12-Page Glowing Charm Reports",
        "Complete multi-domain clarity across Love, Career, Wealth & Family",
        "Glowing Numbers in Depth & Auspicious Initiation Windows for each domain",
        "Vedic Gharelu remedies & Kua directional protocols"
      ]
    }
  },
  "charm_ai": {
    "charm_free": {
      "pack_id": "charm_free",
      "name": "Free Preview",
      "display_name": "Charm AI \u00b7 Free Preview",
      "price_inr": 0,
      "amount_paise": 0,
      "questions_count": 3,
      "digital_root": 0,
      "status": "active",
      "deliverables": [
        "3 Free Exploratory Inquiries Daily per Account",
        "Instant Driver / Conductor token verification",
        "24/7 web access"
      ]
    },
    "charm_single": {
      "pack_id": "charm_single",
      "name": "Charm AI Starter Pack",
      "display_name": "Charm AI \u00b7 Starter Pack",
      "price_inr": 199,
      "amount_paise": 19900,
      "questions_count": 5,
      "digital_root": 1,
      "status": "active",
      "deliverables": [
        "5 In-Depth Consultation Inquiries across any life area",
        "Acute execution timing windows (Hora & transit)",
        "Grounded non-fatalistic practical guidance",
        "Credits valid for 6 months"
      ]
    },
    "charm_multi": {
      "pack_id": "charm_multi",
      "name": "Multi-Reading Pack",
      "display_name": "Charm AI \u00b7 Multi-Reading Pack",
      "price_inr": 399,
      "amount_paise": 39900,
      "questions_count": 10,
      "digital_root": 3,
      "status": "inactive",
      "deliverables": [
        "10 Detailed Question Predictions",
        "Customised 7-Layer safe remedies for all queries",
        "Auspicious date selection & Muhurat guidance",
        "Priority engine response queue",
        "Credits valid for 12 months"
      ]
    },
    "charm_extended": {
      "pack_id": "charm_extended",
      "name": "Extended Reading Pack",
      "display_name": "Charm AI \u00b7 Extended Pack",
      "price_inr": 699,
      "amount_paise": 69900,
      "questions_count": 25,
      "digital_root": 6,
      "status": "inactive",
      "deliverables": [
        "25 Deep In-Depth Predictions",
        "Interactive chart companion with transit radar",
        "Multi-profile synastry consultation capability",
        "Downloadable consultation transcript",
        "Credits valid for 12 months with rollover"
      ]
    }
  },
  "annual_planners": {
    "planner_2027": {
      "pack_id": "planner_2027",
      "tier_id": "year_ahead_2027",
      "name": "2027 Year Ahead Planner",
      "display_name": "2027 Year Ahead Planner \u00b7 Annual Blueprint",
      "pages": 16,
      "list_price_inr": 1999,
      "list_price_paise": 199900,
      "offer_price_inr": 1499,
      "offer_price_paise": 149900,
      "offer_ends_at": "2027-01-31T23:59:59+05:30",
      "currency": "INR",
      "status": "active",
      "deliverables": [
        "16-Page High-Precision 2027 Annual Master Planner PDF",
        "Personal Year 2027 Governing Archetype & Macro Trajectory",
        "12-Month Tactical Matrix with Auspicious Decision Windows",
        "Quarterly Pivot Radar (Q1\u2013Q4 Strategic Milestones)",
        "Commercial, Vocational & Relationship Timing Corridors",
        "Vedic Gharelu Remedies & 40-Day Aural Attunement for 2027"
      ]
    }
  }
};

export default PACK_CATALOG;
