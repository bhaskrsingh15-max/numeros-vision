/**
 * NUMEROS VISION — AUTHORITATIVE PRICING MANIFEST
 * MVP Scope: Exactly 4 Active Products (3 Report Tiers + 1 Charm AI Pass)
 * Version: 2.2.0-MVP
 */

(function(window) {
  'use strict';

  const CATALOG = {
  "currency": "INR",
  "ladder_order": ["report_premium", "report_advanced", "report_basic"],
  "feature_flags": {
    "notify_me_higher_tiers": true,
    "notify_me_tiers": ["report_advanced", "report_premium", "planner_2027"],
    "waitlist_display_label": "Coming soon, notify me",
    "waitlist_launch_caption": "When this report opens, it starts at a launch price for its first 7 days. We\u2019ll email you the day it opens."
  },
  "launch_offer": {
    "enabled": true,
    "duration_days": 7,
    "started_at": null,
    "ends_at": null,
    "until_date_label": null,
    "regular_from_date_label": null,
    "copy_template": "Launch price until {until_date}. Regular price \u20b9{mrp_formatted} from {from_date}."
  },
  "report_tiers": {
    "premium": {
      "tier_id": "premium",
      "name": "Anveil every charm",
      "descriptor": "Complete Numerology Report, 32 pages",
      "display_name": "Anveil every charm \u00b7 Complete Numerology Report, 32 pages",
      "pages": 32,
      "page_target": "32-page PDF",
      "price_inr": 1050,
      "amount_paise": 105000,
      "mrp_inr": 2100,
      "mrp_paise": 210000,
      "digital_root": 6,
      "mrp_digital_root": 3,
      "best_value": true,
      "purpose": "The complete 32-page roadmap covering every glowing and veiled charm, dual-system synthesis, practical habits, and timing.",
      "deliverables": [
        "Everything in Basic & Advanced plus Missing Numbers (Open Grid Cells) Analysis",
        "Multi-Year Numerology Dasha & Pinnacle Cycle Timeline",
        "Chaldean Name Balancing & Signature Alignment Options",
        "Practical Lifestyle, Color, Directional (Vastu) & Habit Harmonizers",
        "Complete 32-Page Personalized Reference PDF Report"
      ],
      "depth_level": "Comprehensive",
      "comparisons": "Integrated across all supported modules",
      "methodology": "Deterministic formula steps & engine version trace",
      "guidance": "Consolidated lifetime reference & strategic roadmap",
      "active": true
    },
    "advanced": {
      "tier_id": "advanced",
      "name": "Anveil my glowing charms",
      "descriptor": "Advanced Numerology Report, 12 pages",
      "display_name": "Anveil my glowing charms \u00b7 Advanced Numerology Report, 12 pages",
      "pages": 12,
      "page_target": "12-page PDF",
      "price_inr": 510,
      "amount_paise": 51000,
      "mrp_inr": 1020,
      "mrp_paise": 102000,
      "digital_root": 6,
      "mrp_digital_root": 3,
      "popular": true,
      "purpose": "Expanded 12-page analysis of your glowing charms, supporting calculations, comparisons, and structured guidance.",
      "deliverables": [
        "Everything in Basic plus Deep Analysis of All Present Numbers",
        "Repeating Digit Amplifications & Behavioral Tendencies",
        "8 Lo Shu Planes & Raj Yoga Combinations Breakdown",
        "Career, Relationship & Financial Archetype Compatibility",
        "12-Page Structured PDF Report with Actionable Daily Habits"
      ],
      "depth_level": "Expanded",
      "comparisons": "Multiple, where supported",
      "methodology": "Expanded with calculation steps",
      "guidance": "Structured guidance & auspicious windows",
      "active": true
    },
    "basic": {
      "tier_id": "basic",
      "name": "Anveil my alignments",
      "descriptor": "Basic Numerology Report, 3 pages",
      "display_name": "Anveil my alignments \u00b7 Basic Numerology Report, 3 pages",
      "pages": 3,
      "page_target": "3-page PDF",
      "price_inr": 199,
      "amount_paise": 19900,
      "mrp_inr": 399,
      "mrp_paise": 39900,
      "digital_root": 1,
      "mrp_digital_root": 3,
      "purpose": "A focused 3-page reading of your core alignments with essential calculations and practical daily habits.",
      "deliverables": [
        "Core Numbers: Mulank (Birth Day number), Bhagyank (Life Path number), Kua number (Vastu direction number) & Personal Year",
        "9-Cell Lo Shu Grid (Lo Shu Square) Mapping & Active Plane Strengths",
        "Calling Name number (Chaldean Name number) Harmony Check",
        "Five-Element Distribution Balance & Practical Lifestyle Guidance",
        "Instant 3-Page Print-Ready Personalized PDF Report"
      ],
      "depth_level": "Focused",
      "comparisons": "Essential",
      "methodology": "Included",
      "guidance": "Key takeaways & practical daily habits",
      "active": true
    }
  },
  "supported_topics": {
    "love_romance": {
      "id": "love_romance",
      "category": "Love and Marriage",
      "title": "Love Style & Romance Profile",
      "icon": "\ud83d\udc96",
      "purpose": "Uncovers your relationship blueprint, emotional attraction triggers, and partnership style.",
      "tags": [
        "Love",
        "Relationships",
        "Partnership"
      ],
      "recommended_tier": "advanced"
    },
    "marriage_union": {
      "id": "marriage_union",
      "category": "Love and Marriage",
      "title": "Marriage Timing & Union Blueprint",
      "icon": "\ud83d\udc8d",
      "purpose": "Evaluates auspicious union windows, spousal harmony factors, and long-term marital alignment.",
      "tags": [
        "Marriage",
        "Timing",
        "Harmony"
      ],
      "recommended_tier": "advanced"
    },
    "partner_compatibility": {
      "id": "partner_compatibility",
      "category": "Love and Marriage",
      "title": "Ideal Partner Compatibility",
      "icon": "\u2696\ufe0f",
      "purpose": "Dual-chart synastry comparing Driver, Conductor, and Lo Shu grid polarities between two individuals.",
      "tags": [
        "Compatibility",
        "Synastry",
        "Dating"
      ],
      "recommended_tier": "advanced"
    },
    "love_or_arrange": {
      "id": "love_or_arrange",
      "category": "Love and Marriage",
      "title": "Love or Arrange Exploration",
      "icon": "\ud83d\udd4a\ufe0f",
      "purpose": "Identifies numerical indicators of self-chosen versus family-facilitated marriage harmony.",
      "tags": [
        "Marriage",
        "Decision",
        "Family"
      ],
      "recommended_tier": "basic"
    },
    "spouse_personality": {
      "id": "spouse_personality",
      "category": "Love and Marriage",
      "title": "Spouse Personality & Life Alignment",
      "icon": "\ud83d\udd2e",
      "purpose": "Archetypal profile of probable spouse traits, vocational leanings, and life temperament.",
      "tags": [
        "Spouse",
        "Traits",
        "Alignment"
      ],
      "recommended_tier": "advanced"
    },
    "family_harmony": {
      "id": "family_harmony",
      "category": "Love and Marriage",
      "title": "In-Laws & Family Harmony",
      "icon": "\ud83c\udfe1",
      "purpose": "Examines interpersonal family dynamics, domestic peace, and emotional grounding strategies.",
      "tags": [
        "Family",
        "In-laws",
        "Peace"
      ],
      "recommended_tier": "basic"
    },
    "wealth_abundance": {
      "id": "wealth_abundance",
      "category": "Money",
      "title": "Wealth & Abundance Report",
      "icon": "\ud83d\udcb0",
      "purpose": "Identifies your financial growth catalysts, wealth retention numbers, and prosperity cycles.",
      "tags": [
        "Money",
        "Wealth",
        "Finance"
      ],
      "recommended_tier": "advanced"
    },
    "billionaire_potential": {
      "id": "billionaire_potential",
      "category": "Money",
      "title": "High-Growth Commercial Potential",
      "icon": "\ud83c\udfdb\ufe0f",
      "purpose": "Explores enterprise scale capacity, high-stakes decision cycles, and institutional wealth vectors.",
      "tags": [
        "Enterprise",
        "Scale",
        "Ambition"
      ],
      "recommended_tier": "premium"
    },
    "career_growth": {
      "id": "career_growth",
      "category": "Work",
      "title": "Career Direction & Growth",
      "icon": "\ud83d\udcbc",
      "purpose": "Maps your optimal vocational pathways, promotion cycles, and leadership strengths.",
      "tags": [
        "Career",
        "Job",
        "Promotion"
      ],
      "recommended_tier": "advanced"
    },
    "business_venture": {
      "id": "business_venture",
      "category": "Work",
      "title": "Business & Venture Mastery",
      "icon": "\ud83d\ude80",
      "purpose": "Evaluates venture launch timings, commercial partnerships, and brand numerical resonance.",
      "tags": [
        "Business",
        "Startup",
        "Founder"
      ],
      "recommended_tier": "premium"
    },
    "job_interview_tactics": {
      "id": "job_interview_tactics",
      "category": "Work",
      "title": "Job Search & Interview Tactics",
      "icon": "\ud83c\udfaf",
      "purpose": "Pinpoints high-conversion application windows, interview days, and personal presentation styles.",
      "tags": [
        "Job Search",
        "Interview",
        "Career"
      ],
      "recommended_tier": "basic"
    },
    "core_blueprint": {
      "id": "core_blueprint",
      "category": "Self and Growth",
      "title": "Complete Personal Destiny Blueprint",
      "icon": "\u2600\ufe0f",
      "purpose": "Comprehensive baseline assessment of your life purpose, hidden strengths, and karmic lessons.",
      "tags": [
        "Destiny",
        "Life Purpose",
        "Core"
      ],
      "recommended_tier": "premium"
    },
    "name_spelling_calibration": {
      "id": "name_spelling_calibration",
      "category": "Self and Growth",
      "title": "Name Balancing & Spelling Calibration",
      "icon": "\u270d\ufe0f",
      "purpose": "Chaldean vibrational analysis of your calling name to calibrate harmonious compound resonances.",
      "tags": [
        "Name Correction",
        "Spelling",
        "Vibration"
      ],
      "recommended_tier": "advanced"
    },
    "personal_year_radar": {
      "id": "personal_year_radar",
      "category": "Self and Growth",
      "title": "Personal Year & Auspicious Timing Radar",
      "icon": "\ud83d\udcc5",
      "purpose": "Month-by-month cosmic timing roadmap detailing auspicious initiation and consolidation months.",
      "tags": [
        "Timing",
        "Personal Year",
        "Transit"
      ],
      "recommended_tier": "advanced"
    }
  },
  "bundles": {
    "starter_bundle": {
      "bundle_id": "starter_bundle",
      "name": "Starter Bundle",
      "display_name": "Starter Bundle \u00b7 2 Basic Reports",
      "included_reports_description": "Two Basic reports of your choice",
      "basic_report_count": 2,
      "advanced_report_count": 0,
      "premium_report_count": 0,
      "standalone_total_inr": 398,
      "bundle_price_inr": 339,
      "amount_paise": 33900,
      "savings_inr": 49,
      "savings_percent": 12,
      "purpose": "Ideal for exploring two connected life domains (e.g. Love Style + Career Direction).",
      "deliverables": [
        "2 Complete 3-Page Basic PDF Reports",
        "Choose any two topics across Love, Money, Work, or Growth",
        "Full calculation breakdown and method explanations",
        "Ready within minutes in your account dashboard"
      ],
      "active": false,
      "status": "paused_for_mvp"
    },
    "discovery_bundle": {
      "bundle_id": "discovery_bundle",
      "name": "Discovery Bundle",
      "display_name": "Discovery Bundle \u00b7 3 Advanced Reports",
      "included_reports_description": "Three Basic reports of your choice",
      "basic_report_count": 3,
      "advanced_report_count": 0,
      "premium_report_count": 0,
      "standalone_total_inr": 597,
      "bundle_price_inr": 1299,
      "amount_paise": 129900,
      "savings_inr": 98,
      "savings_percent": 16,
      "popular": true,
      "purpose": "Broad 3-domain diagnostic covering Relationships, Career, and Wealth foundations.",
      "deliverables": [
        "3 Complete 12-Page Advanced Master Reports",
        "Choose any three topics from the entire catalogue",
        "Independent deterministic calculation traces for each topic",
        "Unified dashboard access with download library"
      ],
      "active": false,
      "status": "paused_for_mvp"
    },
    "comprehensive_bundle": {
      "bundle_id": "comprehensive_bundle",
      "name": "Comprehensive Bundle",
      "display_name": "Comprehensive Bundle \u00b7 5 Advanced Reports",
      "included_reports_description": "Five 12-page Advanced reports across major life pillars",
      "basic_report_count": 1,
      "advanced_report_count": 2,
      "premium_report_count": 0,
      "standalone_total_inr": 1219,
      "bundle_price_inr": 1999,
      "amount_paise": 199900,
      "savings_inr": 220,
      "savings_percent": 18,
      "purpose": "Deep exploration for seekers making major life decisions across multiple domains.",
      "deliverables": [
        "5 Complete 12-Page Advanced Master Reports",
        "1 Complete 3-Page Basic Report",
        "5-Year Numerology Dasha & Numerology Dasha timing included",
        "7-Layer safe planetary remedy protocols for selected domains"
      ],
      "active": false,
      "status": "paused_for_mvp"
    }
  },
  "charm_ai": {
    "charm_free": {
      "pack_id": "charm_free",
      "name": "Free Preview",
      "display_name": "Charm AI \u00b7 Free Preview",
      "price_inr": 0,
      "amount_paise": 0,
      "questions_count": 1,
      "has_remedies": false,
      "purpose": "Experience conversational Charm AI intelligence with one free inquiry.",
      "deliverables": [
        "1 Targeted Question Prediction",
        "Instant Driver / Conductor token verification",
        "24/7 web access"
      ]
    },
    "charm_single": {
      "pack_id": "charm_single",
      "name": "Charm AI Starter Pass",
      "display_name": "Charm AI \u00b7 Starter Pass (5 Questions)",
      "price_inr": 199,
      "amount_paise": 19900,
      "questions_count": 5,
      "has_remedies": true,
      "purpose": "Focused query resolution for immediate decision crossroads.",
      "deliverables": [
        "3 In-Depth Question Predictions",
        "Acute execution timing windows (Hora & transit)",
        "Grounded non-fatalistic practical guidance",
        "Credits valid for 6 months"
      ],
      "active": true
    },
    "charm_multi": {
      "pack_id": "charm_multi",
      "name": "Multi-Reading Pack",
      "display_name": "Charm AI \u00b7 Multi-Reading Pack",
      "price_inr": 399,
      "amount_paise": 39900,
      "questions_count": 10,
      "has_remedies": true,
      "popular": true,
      "purpose": "Ongoing strategic guidance covering career, relationships, and finance.",
      "deliverables": [
        "10 Detailed Question Predictions",
        "Customised 7-Layer safe remedies for all queries",
        "Auspicious date selection & Muhurat guidance",
        "Priority engine response queue",
        "Credits valid for 12 months"
      ],
      "active": false,
      "status": "paused_for_mvp"
    },
    "charm_extended": {
      "pack_id": "charm_extended",
      "name": "Extended Reading Pack",
      "display_name": "Charm AI \u00b7 Extended Pack",
      "price_inr": 699,
      "amount_paise": 69900,
      "questions_count": 25,
      "has_remedies": true,
      "purpose": "Comprehensive conversational companion for active founders and decision-makers.",
      "deliverables": [
        "25 Deep In-Depth Predictions",
        "Interactive chart companion with transit radar",
        "Multi-profile synastry consultation capability",
        "Downloadable consultation transcript",
        "Credits valid for 12 months with rollover"
      ],
      "active": false,
      "status": "paused_for_mvp"
    }
  },
  "consultation": {
    "consultation_standard": {
      "consult_id": "consultation_standard",
      "name": "1-on-1 Expert Consultation",
      "display_name": "1-on-1 Expert Consultation",
      "price_inr": 1050,
      "amount_paise": 105000,
      "duration_minutes": 45,
      "mode": "Private Google Meet / Phone",
      "practitioner": "Certified Senior Astrologer & Numerologist",
      "purpose": "In-depth private live consultation for complex life transitions, business launches, and relationship alignment.",
      "deliverables": [
        "45-Minute Private 1-on-1 Consultation Session",
        "Birth Time Rectification (BTR) & Cross-Engine Chart Audit",
        "Comprehensive personal strategy & custom remedial protocols",
        "Complimentary 12-Page Advanced PDF Dossier (\u20b9510 value)",
        "Audio recording and written consultation summary",
        "Free 1-time rescheduling up to 24 hours prior"
      ]
    }
  },
  "all_skus": {
    "report_basic": {
      "sku_id": "report_basic",
      "family": "standalone_report",
      "name": "Anveil my alignments",
      "tier": "basic",
      "pages": 3,
      "amount_inr": 199,
      "amount_paise": 19900,
      "currency": "INR",
      "deliverables": [
        "Core Numbers: Mulank (Birth Day number), Bhagyank (Life Path number), Kua number (Vastu direction number) & Personal Year",
        "9-Cell Lo Shu Grid (Lo Shu Square) Mapping & Active Plane Strengths",
        "Calling Name number (Chaldean Name number) Harmony Check",
        "Five-Element Distribution Balance & Practical Lifestyle Guidance",
        "Instant 3-Page Print-Ready Personalized PDF Report"
      ]
    },
    "report_advanced": {
      "sku_id": "report_advanced",
      "family": "standalone_report",
      "name": "Anveil my glowing charms",
      "tier": "advanced",
      "pages": 12,
      "amount_inr": 510,
      "amount_paise": 51000,
      "currency": "INR",
      "deliverables": [
        "Everything in Basic plus Deep Analysis of All Present Numbers",
        "Repeating Digit Amplifications & Behavioral Tendencies",
        "8 Lo Shu Planes & Raj Yoga Combinations Breakdown",
        "Career, Relationship & Financial Archetype Compatibility",
        "12-Page Structured PDF Report with Actionable Daily Habits"
      ]
    },
    "report_premium": {
      "sku_id": "report_premium",
      "family": "standalone_report",
      "name": "Anveil every charm",
      "tier": "premium",
      "pages": 32,
      "amount_inr": 1050,
      "amount_paise": 105000,
      "currency": "INR",
      "deliverables": [
        "Everything in Basic & Advanced plus Missing Numbers (Open Grid Cells) Analysis",
        "Multi-Year Numerology Dasha & Pinnacle Cycle Timeline",
        "Chaldean Name Balancing & Signature Alignment Options",
        "Practical Lifestyle, Color, Directional (Vastu) & Habit Harmonizers",
        "Complete 32-Page Personalized Reference PDF Report"
      ]
    },
    "starter_bundle": {
      "sku_id": "starter_bundle",
      "family": "bundle",
      "name": "Starter Bundle",
      "amount_inr": 339,
      "amount_paise": 33900,
      "currency": "INR",
      "deliverables": [
        "2 Complete 3-Page Basic PDF Reports",
        "Choose any two topics across Love, Money, Work, or Growth",
        "Full calculation breakdown and method explanations",
        "Ready within minutes in your account dashboard"
      ]
    },
    "discovery_bundle": {
      "sku_id": "discovery_bundle",
      "family": "bundle",
      "name": "Discovery Bundle",
      "amount_inr": 1299,
      "amount_paise": 129900,
      "currency": "INR",
      "deliverables": [
        "3 Complete 12-Page Advanced Master Reports",
        "Choose any three topics from the entire catalogue",
        "Independent deterministic calculation traces for each topic",
        "Unified dashboard access with download library"
      ]
    },
    "comprehensive_bundle": {
      "sku_id": "comprehensive_bundle",
      "family": "bundle",
      "name": "Comprehensive Bundle",
      "amount_inr": 1999,
      "amount_paise": 199900,
      "currency": "INR",
      "deliverables": [
        "5 Complete 12-Page Advanced Master Reports",
        "1 Complete 3-Page Basic Report",
        "5-Year Numerology Dasha & Numerology Dasha timing included",
        "7-Layer safe planetary remedy protocols for selected domains"
      ]
    },
    "charm_free": {
      "sku_id": "charm_free",
      "family": "charm_ai",
      "name": "Free Preview",
      "questions_count": 3,
      "amount_inr": 0,
      "amount_paise": 0,
      "currency": "INR",
      "deliverables": [
        "3 Free Exploratory Inquiries per Visitor per Day",
        "Instant Mulank (Birth Day number) & Bhagyank (Life Path number) Context",
        "24/7 Web Access in Charm AI"
      ]
    },
    "charm_single": {
      "sku_id": "charm_single",
      "family": "charm_ai",
      "name": "Charm AI Starter Pack",
      "questions_count": 5,
      "amount_inr": 199,
      "amount_paise": 19900,
      "currency": "INR",
      "deliverables": [
        "5 Guided Numerology Q&A Inquiries across Career, Relationships, or Timing",
        "Deterministic Dasha & Personal Year Window Context",
        "Grounded, Non-Fatalistic Practical Reflection Points",
        "Credits Valid for 6 Months in Your Private Dashboard"
      ]
    },
    "charm_multi": {
      "sku_id": "charm_multi",
      "family": "charm_ai",
      "name": "Multi-Reading Pack",
      "questions_count": 10,
      "amount_inr": 399,
      "amount_paise": 39900,
      "currency": "INR",
      "deliverables": [
        "10 Detailed Question Predictions",
        "Customised 7-Layer safe remedies for all queries",
        "Auspicious date selection & Muhurat guidance",
        "Priority engine response queue",
        "Credits valid for 12 months"
      ]
    },
    "charm_extended": {
      "sku_id": "charm_extended",
      "family": "charm_ai",
      "name": "Extended Reading Pack",
      "questions_count": 25,
      "amount_inr": 699,
      "amount_paise": 69900,
      "currency": "INR",
      "deliverables": [
        "25 Deep In-Depth Predictions",
        "Interactive chart companion with transit radar",
        "Multi-profile synastry consultation capability",
        "Downloadable consultation transcript",
        "Credits valid for 12 months with rollover"
      ]
    },
    "consultation_standard": {
      "sku_id": "consultation_standard",
      "family": "consultation",
      "name": "1-on-1 Expert Consultation",
      "amount_inr": 1050,
      "amount_paise": 105000,
      "currency": "INR",
      "deliverables": [
        "45-Minute Private 1-on-1 Consultation Session",
        "Birth Time Rectification (BTR) & Cross-Engine Chart Audit",
        "Comprehensive personal strategy & custom remedial protocols",
        "Complimentary 12-Page Advanced PDF Dossier (\u20b9510 value)",
        "Audio recording and written consultation summary",
        "Free 1-time rescheduling up to 24 hours prior"
      ]
    }
  },
  "starter_bundle": {
    "sku_id": "starter_bundle",
    "family": "bundle",
    "name": "Starter Bundle",
    "amount_inr": 339,
    "amount_paise": 33900,
    "currency": "INR",
    "savings_inr": 59,
    "savings_percent": 15,
    "digital_root": 6,
    "deliverables": [
      "2 Complete 3-Page Basic PDF Reports",
      "Choose any two topics across Love, Money, Work, or Growth",
      "Full calculation breakdown and practical remedies",
      "Ready within minutes in your account dashboard with archival PDF download"
    ]
  },
  "discovery_bundle": {
    "sku_id": "discovery_bundle",
    "family": "bundle",
    "name": "Discovery Bundle",
    "amount_inr": 1299,
    "amount_paise": 129900,
    "currency": "INR",
    "savings_inr": 231,
    "savings_percent": 15,
    "digital_root": 3,
    "deliverables": [
      "3 Complete 12-Page Advanced Master Reports",
      "Choose any three topics from the entire catalogue",
      "Enabled Numbers in Depth & Auspicious Initiation Windows for each topic",
      "7-Layer safe planetary remedy protocols for selected domains"
    ]
  },
  "comprehensive_bundle": {
    "sku_id": "comprehensive_bundle",
    "family": "bundle",
    "name": "Comprehensive Bundle",
    "amount_inr": 1999,
    "amount_paise": 199900,
    "currency": "INR",
    "savings_inr": 551,
    "savings_percent": 22,
    "digital_root": 1,
    "deliverables": [
      "5 Complete 12-Page Advanced Master Reports",
      "Complete multi-domain lifetime clarity across Love, Career, Wealth & Family",
      "Enabled Numbers in Depth & Auspicious Initiation Windows for each domain",
      "7-Layer safe planetary remedy protocols & auspicious timing windows"
    ]
  },
  "charm_free": {
    "sku_id": "charm_free",
    "family": "charm_ai",
    "name": "Free Preview",
    "questions_count": 3,
    "amount_inr": 0,
    "amount_paise": 0,
    "currency": "INR",
    "deliverables": [
      "3 Free Exploratory Inquiries per Visitor per Day",
      "Instant Mulank (Birth Day number) & Bhagyank (Life Path number) Context",
      "24/7 Web Access in Charm AI"
    ]
  },
  "charm_single": {
    "sku_id": "charm_single",
    "family": "charm_ai",
    "name": "Charm AI Starter Pack",
    "questions_count": 5,
    "amount_inr": 199,
    "amount_paise": 19900,
    "currency": "INR",
    "digital_root": 1,
    "deliverables": [
      "5 Guided Numerology Q&A Inquiries across Career, Relationships, or Timing",
      "Deterministic Dasha & Personal Year Window Context",
      "Grounded, Non-Fatalistic Practical Reflection Points",
      "Credits Valid for 6 Months in Your Private Dashboard"
    ]
  },
  "charm_multi": {
    "sku_id": "charm_multi",
    "family": "charm_ai",
    "name": "Charm AI Growth Pack",
    "questions_count": 10,
    "amount_inr": 399,
    "amount_paise": 39900,
    "currency": "INR",
    "digital_root": 3,
    "deliverables": [
      "10 Detailed Consultation Inquiries",
      "Customised 7-Layer safe remedies for all queries",
      "Auspicious date selection & Muhurat guidance",
      "Priority engine response queue \u00b7 Credits valid for 12 months"
    ]
  },
  "charm_extended": {
    "sku_id": "charm_extended",
    "family": "charm_ai",
    "name": "Charm AI Extended Pack",
    "questions_count": 25,
    "amount_inr": 699,
    "amount_paise": 69900,
    "currency": "INR",
    "digital_root": 6,
    "deliverables": [
      "25 Deep Consultation Inquiries",
      "Interactive chart companion with transit radar",
      "Multi-profile synastry consultation capability",
      "Downloadable consultation transcript \u00b7 Credits valid for 12 months with rollover"
    ]
  },
  "mvp_scope": {
    "version": "1.0.0",
    "active_skus": [
      "report_basic",
      "report_advanced",
      "report_premium",
      "charm_single"
    ],
    "products": {
      "BASIC_REPORT": {
        "sku": "report_basic",
        "price_inr": 199,
        "pages": 3
      },
      "ADVANCED_REPORT": {
        "sku": "report_advanced",
        "price_inr": 510,
        "pages": 12
      },
      "PREMIUM_REPORT": {
        "sku": "report_premium",
        "price_inr": 1050,
        "pages": 32
      },
      "CHARM_AI_STARTER": {
        "sku": "charm_single",
        "price_inr": 199,
        "questions": 5
      }
    }
  }
};

  const NV_PRICING = {
    catalog: CATALOG,
    currency: CATALOG.currency || 'INR',

    // MVP Active Products
    mvpProducts: CATALOG.mvp_scope.products,

    getTier(tierId) {
      const id = (tierId || '').toLowerCase().replace('report_', '');
      if (id === 'essential') return CATALOG.report_tiers.basic;
      if (id === 'master') return CATALOG.report_tiers.advanced;
      if (id === 'divine') return CATALOG.report_tiers.premium;
      return CATALOG.report_tiers[id] || null;
    },

    getCharmAiPass() {
      return CATALOG.charm_ai.charm_single;
    },

    getWaitlistLabel() {
      return (CATALOG.feature_flags && CATALOG.feature_flags.waitlist_display_label) || 'Coming soon, notify me';
    },

    getWaitlistCaption() {
      return (CATALOG.feature_flags && CATALOG.feature_flags.waitlist_launch_caption) || 'When this report opens, it starts at a launch price for its first 7 days. We\u2019ll email you the day it opens.';
    },

    getLaunchPrice(skuId) {
      const clean = (skuId || '').toLowerCase();
      if (this.isNotifyMeTier(clean)) return null;
      if (clean === 'basic' || clean === 'report_basic' || clean === 'report_essential' || clean === 'alignments') return 199;
      if (clean === 'advanced' || clean === 'report_advanced' || clean === 'report_master' || clean === 'glowing') return 510;
      if (clean === 'premium' || clean === 'report_premium' || clean === 'report_divine' || clean === 'every_charm') return 1050;
      if (clean === 'charm_single' || clean === 'charm_starter' || clean === 'starter_5q') return 199;
      if (CATALOG.report_tiers[clean]) return CATALOG.report_tiers[clean].price_inr;
      return 199;
    },

    getPrice(skuId, nowMs, endsAtOverride, startsAtOverride) {
      const clean = (skuId || '').toLowerCase();
      if (this.isNotifyMeTier(clean)) return null;
      const mrp = this.getMrp(clean);
      if (mrp !== null) {
        const state = this.resolveLaunchOfferState(nowMs, endsAtOverride, startsAtOverride, clean);
        if (!state.active) {
          return mrp;
        }
      }
      return this.getLaunchPrice(clean);
    },

    getMrp(skuId) {
      const clean = (skuId || '').toLowerCase();
      if (this.isNotifyMeTier(clean)) return null;
      if (clean === 'basic' || clean === 'report_basic' || clean === 'report_essential' || clean === 'alignments') return 399;
      if (clean === 'advanced' || clean === 'report_advanced' || clean === 'report_master' || clean === 'glowing') return 1020;
      if (clean === 'premium' || clean === 'report_premium' || clean === 'report_divine' || clean === 'every_charm') return 2100;
      return null;
    },

    getStruckMrp(skuId, nowMs, endsAtOverride, startsAtOverride) {
      if (this.isNotifyMeTier(skuId)) return null;
      const mrp = this.getMrp(skuId);
      if (mrp === null) return null;
      const state = this.resolveLaunchOfferState(nowMs, endsAtOverride, startsAtOverride, skuId);
      return state.active ? mrp : null;
    },

    getDescriptor(skuId) {
      const clean = (skuId || '').toLowerCase();
      if (clean === 'basic' || clean === 'report_basic' || clean === 'report_essential' || clean === 'alignments') return 'Basic Numerology Report, 3 pages';
      if (clean === 'advanced' || clean === 'report_advanced' || clean === 'report_master' || clean === 'glowing') return 'Advanced Numerology Report, 12 pages';
      if (clean === 'premium' || clean === 'report_premium' || clean === 'report_divine' || clean === 'every_charm') return 'Complete Numerology Report, 32 pages';
      if (clean === 'charm_single' || clean === 'charm_starter' || clean === 'starter_5q') return 'Guided Numerology Q&A Pack, 5 questions';
      return '';
    },

    formatPrice(skuId, nowMs, endsAtOverride, startsAtOverride) {
      if (this.isNotifyMeTier(skuId)) return this.getWaitlistLabel();
      const price = this.getPrice(skuId, nowMs, endsAtOverride, startsAtOverride);
      if (price === null || price === undefined) return this.getWaitlistLabel();
      return '₹' + Number(price).toLocaleString('en-IN');
    },

    isMvpActive(skuId) {
      const clean = (skuId || '').toLowerCase();
      return ['report_basic', 'report_advanced', 'report_premium', 'charm_single', 'charm_starter'].includes(clean);
    },

    isNotifyMeHigherTiersEnabled() {
      if (typeof window !== 'undefined' && typeof window.__NV_NOTIFY_ME_HIGHER_TIERS === 'boolean') {
        return window.__NV_NOTIFY_ME_HIGHER_TIERS;
      }
      if (typeof window !== 'undefined' && window.location) {
        const host = window.location.hostname || '';
        if (host === 'localhost' || host === '127.0.0.1') {
          const sp = new URLSearchParams(window.location.search || '');
          if (sp.get('nv_notify_me_preview') === '1') return true;
          if (sp.get('nv_notify_me_preview') === '0') return false;
        }
      }
      return Boolean(CATALOG.feature_flags && CATALOG.feature_flags.notify_me_higher_tiers);
    },

    isNotifyMeTier(skuId) {
      const clean = (skuId || '').toLowerCase();
      if (clean === 'planner_2027' || clean === 'year_ahead_2027') {
        if (typeof window !== 'undefined' && window.__NV_PLANNER_2027_LIVE === true) return false;
        return true;
      }
      if (!this.isNotifyMeHigherTiersEnabled()) return false;
      return ['advanced', 'report_advanced', 'report_master', 'glowing', 'premium', 'report_premium', 'report_divine', 'every_charm'].includes(clean);
    },

    resolveLaunchOfferState(nowMs, endsAtOverride, startsAtOverride, skuId) {
      const lo = CATALOG.launch_offer || {};
      const durationDays = Number(lo.duration_days || 7);
      if (lo.enabled === false) {
        return { active: false, configured: false, durationDays, startedAt: null, endsAt: null, untilDate: '', fromDate: '', label: '' };
      }
      const clean = String(skuId || '').toLowerCase().replace('report_', '');
      let tierKey = '';
      if (clean === 'basic' || clean === 'essential' || clean === 'alignments') tierKey = 'BASIC';
      else if (clean === 'advanced' || clean === 'master' || clean === 'glowing') tierKey = 'ADVANCED';
      else if (clean === 'premium' || clean === 'divine' || clean === 'every_charm') tierKey = 'PREMIUM';

      let tierEnd = '';
      let tierStart = '';
      if (tierKey && typeof window !== 'undefined') {
        tierEnd = window['__NV_LAUNCH_' + tierKey + '_ENDS_AT'] || window['NV_LAUNCH_' + tierKey + '_ENDS_AT'] || '';
        tierStart = window['__NV_LAUNCH_' + tierKey + '_STARTS_AT'] || window['NV_LAUNCH_' + tierKey + '_STARTS_AT'] || '';
      }

      const rawEnd = endsAtOverride !== undefined
        ? endsAtOverride
        : (tierEnd || ((typeof window !== 'undefined' && (window.__NV_LAUNCH_ENDS_AT || window.NV_LAUNCH_ENDS_AT)) || ''));
      const rawStart = startsAtOverride !== undefined
        ? startsAtOverride
        : (tierStart || ((typeof window !== 'undefined' && (window.__NV_LAUNCH_STARTS_AT || window.NV_LAUNCH_STARTS_AT || window.__NV_LAUNCH_STARTED_AT)) || ''));
      if (!rawEnd || (!rawStart && endsAtOverride === undefined)) {
        if (endsAtOverride === undefined && startsAtOverride === undefined && typeof window !== 'undefined' && window.__NV_FORCE_LAUNCH_MODE === true) {
          return { active: true, configured: true, forced: true, durationDays, startedAt: null, endsAt: null, untilDate: '', fromDate: '', label: 'Launch price active during the launch window.' };
        }
        return { active: false, configured: false, forced: false, durationDays, startedAt: null, endsAt: null, untilDate: '', fromDate: '', label: '' };
      }
      const endMs = Date.parse(rawEnd);
      const startMs = rawStart ? Date.parse(rawStart) : (endMs - durationDays * 86400 * 1000);
      if (Number.isNaN(endMs) || Number.isNaN(startMs) || endMs <= startMs) {
        return { active: false, configured: false, durationDays, startedAt: null, endsAt: null, untilDate: '', fromDate: '', label: '' };
      }
      const currentMs = typeof nowMs === 'number'
        ? nowMs
        : ((typeof window !== 'undefined' && typeof window.__NV_NOW_MS === 'number') ? window.__NV_NOW_MS : Date.now());
      const active = currentMs >= startMs && currentMs <= endMs;
      const IST_OFFSET_MS = 5.5 * 3600 * 1000;
      const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
      const untilIst = new Date(endMs + IST_OFFSET_MS);
      const fromIst = new Date(endMs + 1000 + IST_OFFSET_MS);
      const isShortWindow = (endMs - startMs) < (24 * 3600 * 1000);
      const pad2 = (n) => String(n).padStart(2, '0');
      const untilDate = isShortWindow
        ? (untilIst.getUTCDate() + ' ' + months[untilIst.getUTCMonth()] + ' ' + untilIst.getUTCFullYear() + ', ' + pad2(untilIst.getUTCHours()) + ':' + pad2(untilIst.getUTCMinutes()) + ' IST')
        : (untilIst.getUTCDate() + ' ' + months[untilIst.getUTCMonth()] + ' ' + untilIst.getUTCFullYear());
      const fromDate = isShortWindow
        ? (fromIst.getUTCDate() + ' ' + months[fromIst.getUTCMonth()] + ' ' + fromIst.getUTCFullYear() + ', ' + pad2(fromIst.getUTCHours()) + ':' + pad2(fromIst.getUTCMinutes()) + ' IST')
        : (fromIst.getUTCDate() + ' ' + months[fromIst.getUTCMonth()] + ' ' + fromIst.getUTCFullYear());
      return {
        active,
        configured: true,
        durationDays,
        startedAt: new Date(startMs).toISOString(),
        endsAt: new Date(endMs).toISOString(),
        untilDate,
        fromDate,
        label: active
          ? ('Launch price until ' + untilDate + '.')
          : ('Regular pricing in effect from ' + fromDate + '.')
      };
    },

    formatLaunchOfferCopy(skuId, nowMs, endsAtOverride, startsAtOverride) {
      if (this.isNotifyMeTier(skuId)) return '';
      const mrp = this.getMrp(skuId);
      if (mrp === null) return '';
      const state = this.resolveLaunchOfferState(nowMs, endsAtOverride, startsAtOverride, skuId);
      if (!state.configured) return '';
      const mrpFormatted = mrp.toLocaleString('en-IN');
      if (state.active) {
        if (state.forced && !state.untilDate) {
          return 'Launch price active during the launch window. Regular price ₹' + mrpFormatted + ' thereafter.';
        }
        return 'Launch price until ' + state.untilDate + '. Regular price ₹' + mrpFormatted + ' from ' + state.fromDate + '.';
      }
      return 'Regular price ₹' + mrpFormatted + ' (effective ' + state.fromDate + ').';
    },

    recommendLadderTier(gapCount, notifyOverride, tappedContext) {
      const notifyActive = typeof notifyOverride === 'boolean'
        ? notifyOverride
        : this.isNotifyMeHigherTiersEnabled();
      if (notifyActive) return 'report_basic';
      if (tappedContext) {
        const ctx = String(tappedContext).trim().toLowerCase();
        if (ctx === 'veiled' || ctx === 'missing' || ctx === 'every') return 'report_premium';
        if (ctx === 'glowing' || ctx === 'present' || ctx === 'radiant') return 'report_advanced';
        if (ctx === 'alignment' || ctx === 'align' || ctx === 'plane') return 'report_basic';
      }
      if (gapCount === null || gapCount === undefined || Number.isNaN(Number(gapCount))) {
        return 'report_advanced';
      }
      const gaps = Math.max(0, Math.min(9, Math.trunc(Number(gapCount))));
      if (gaps <= 2) return 'report_basic';
      if (gaps <= 5) return 'report_advanced';
      return 'report_premium';
    }
  };

  window.NV_PRICING = NV_PRICING;
  window.NV_PRICING_CATALOG = CATALOG;
})(typeof window !== 'undefined' ? window : this);
