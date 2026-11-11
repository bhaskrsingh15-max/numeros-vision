"""
NUMEROS VISION — CENTRAL AUTHORITATIVE PRICING ARCHITECTURE (v2.0.0)
Tagline: ANVEIL EVERY CHARM

Single server-side source of truth for all pricing across the website, app,
calculators, checkout, payment webhooks, and PDF report delivery.

Enforces:
1. Four Distinct Product Families:
   - Standalone Reports (Basic ₹199 / Advanced ₹489 / Premium ₹1,050)
   - Multi-Report Bundles (Starter / Discovery / Comprehensive · Coming soon)
   - Charm AI Access (Free ₹0 / Starter ₹199)
   - Human Consultation (Standard 1-on-1 Session ₹1,050)
2. Topic-Independent Pricing:
   - The topic determines content; the tier determines depth, deliverables, and price.
3. Server-Side Validation:
   - Client prices are strictly rejected; the server resolves payable amounts from this catalog.
4. Deterministic Digit Root Verification:
   - 199 (root 1), 489 (root 3), 1050 (root 6), 399 (root 3), 699 (root 6), 1050 (root 6).
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict
import json
import os

CURRENCY = "INR"

# ── 1. PRODUCT FAMILY A: STANDALONE REPORTS (3 UNIFIED TIERS) ────────────────
REPORT_TIERS: Dict[str, Dict[str, Any]] = {
    "basic": {
        "tier_id": "basic",
        "name": "Basic Report",
        "display_name": "Basic Report · Entry",
        "pages": 3,
        "page_target": "3-page PDF",
        "price_inr": 199,
        "amount_paise": 19900,
        "digital_root": 1,  # 1+9+9=19 -> 1+0=1 (Sun / Leadership)
        "purpose": "A focused answer to one core question with essential calculations and initial findings.",
        "deliverables": [
            "3-Page Personalised Executive PDF",
            "Deterministic Mulank (Driver) & Bhagyank (Conductor) Calculations",
            "Lo Shu 3x3 Grid Matrix & Elemental Distribution",
            "Chaldean Single Root & Compound Letter Breakdown",
            "Methodology Note & Interpretive Limitations Summary"
        ],
        "depth_level": "Focused",
        "comparisons": "Essential",
        "methodology": "Included",
        "guidance": "Key takeaways & reflection points"
    },
    "advanced": {
        "tier_id": "advanced",
        "name": "Advanced Master Dossier",
        "display_name": "Advanced Master Dossier · Recommended",
        "pages": 12,
        "page_target": "12-page PDF",
        "price_inr": 489,
        "amount_paise": 48900,
        "digital_root": 3,  # 4+8+9=21 -> 3 (Jupiter / Wisdom)
        "popular": True,
        "purpose": "Expanded analysis, supporting calculations, comparisons, and structured guidance.",
        "deliverables": [
            "12-Page Master Synthesis PDF Dossier",
            "All Basic calculations + 5-Year Numerology Dasha Timing Timeline",
            "Complete Lo Shu Plane Analysis (Thought, Will, Action, Mental, Emotional)",
            "Chaldean Sound Frequency & Name Harmony Matrix",
            "7-Layer Safe Planetary Remedy Protocols",
            "Structured Cross-Factor Comparisons & Practical Guidance"
        ],
        "depth_level": "Expanded",
        "comparisons": "Multiple, where supported",
        "methodology": "Expanded with calculation steps",
        "guidance": "Structured guidance & auspicious windows"
    },
    "premium": {
        "tier_id": "premium",
        "name": "Premium Sovereign Blueprint",
        "display_name": "Premium Sovereign Blueprint · Comprehensive",
        "pages": 32,
        "page_target": "32-page PDF",
        "price_inr": 1050,
        "amount_paise": 105000,
        "digital_root": 6,  # 1+0+5+0=6 (Venus / Harmony)
        "purpose": "The broadest supported analysis with integrated multi-engine findings and consolidated reference.",
        "deliverables": [
            "32-Page Sovereign Executive Master Blueprint PDF",
            "Dual-System Comprehensive Synthesis (Chaldean + Pythagorean)",
            "10-Year Macro Planetary Timing Radar & Acute Execution Windows",
            "Multi-Generational Synastry & Compatibility Analysis",
            "Commercial & Professional Resonance Vectors",
            "Complete Technical Appendix: Formulas, Engine Versions & Assumptions"
        ],
        "depth_level": "Comprehensive",
        "comparisons": "Integrated across all supported modules",
        "methodology": "Detailed mathematical proofs & engine version trace",
        "guidance": "Consolidated lifetime reference & strategic roadmap"
    }
}

# ── 2. SUPPORTED REPORT TOPICS (CATALOGUE TOPICS) ────────────────────────────
SUPPORTED_REPORT_TOPICS: Dict[str, Dict[str, Any]] = {
    "love_romance": {
        "id": "love_romance",
        "category": "Love and Marriage",
        "title": "Love Style & Romance Profile",
        "icon": "💖",
        "purpose": "Uncovers your relationship blueprint, emotional attraction triggers, and partnership style.",
        "tags": ["Love", "Relationships", "Partnership"],
        "recommended_tier": "advanced"
    },
    "marriage_union": {
        "id": "marriage_union",
        "category": "Love and Marriage",
        "title": "Marriage Timing & Union Blueprint",
        "icon": "💍",
        "purpose": "Evaluates auspicious union windows, spousal harmony factors, and long-term marital alignment.",
        "tags": ["Marriage", "Timing", "Harmony"],
        "recommended_tier": "advanced"
    },
    "partner_compatibility": {
        "id": "partner_compatibility",
        "category": "Love and Marriage",
        "title": "Ideal Partner Compatibility",
        "icon": "⚖️",
        "purpose": "Dual-chart synastry comparing Driver, Conductor, and Lo Shu grid polarities between two individuals.",
        "tags": ["Compatibility", "Synastry", "Dating"],
        "recommended_tier": "advanced"
    },
    "love_or_arrange": {
        "id": "love_or_arrange",
        "category": "Love and Marriage",
        "title": "Love or Arrange Exploration",
        "icon": "🕊️",
        "purpose": "Identifies numerical indicators of self-chosen versus family-facilitated marriage harmony.",
        "tags": ["Marriage", "Decision", "Family"],
        "recommended_tier": "basic"
    },
    "spouse_personality": {
        "id": "spouse_personality",
        "category": "Love and Marriage",
        "title": "Spouse Personality & Life Alignment",
        "icon": "🔮",
        "purpose": "Archetypal profile of probable spouse traits, vocational leanings, and life temperament.",
        "tags": ["Spouse", "Traits", "Alignment"],
        "recommended_tier": "advanced"
    },
    "family_harmony": {
        "id": "family_harmony",
        "category": "Love and Marriage",
        "title": "In-Laws & Family Harmony",
        "icon": "🏡",
        "purpose": "Examines interpersonal family dynamics, domestic peace, and emotional grounding strategies.",
        "tags": ["Family", "In-laws", "Peace"],
        "recommended_tier": "basic"
    },
    "wealth_abundance": {
        "id": "wealth_abundance",
        "category": "Money",
        "title": "Wealth & Abundance Report",
        "icon": "💰",
        "purpose": "Identifies your financial growth catalysts, wealth retention numbers, and prosperity cycles.",
        "tags": ["Money", "Wealth", "Finance"],
        "recommended_tier": "advanced"
    },
    "billionaire_potential": {
        "id": "billionaire_potential",
        "category": "Money",
        "title": "High-Growth Commercial Potential",
        "icon": "🏛️",
        "purpose": "Explores enterprise scale capacity, high-stakes decision cycles, and institutional wealth vectors.",
        "tags": ["Enterprise", "Scale", "Ambition"],
        "recommended_tier": "premium"
    },
    "career_growth": {
        "id": "career_growth",
        "category": "Work",
        "title": "Career Direction & Growth",
        "icon": "💼",
        "purpose": "Maps your optimal vocational pathways, promotion cycles, and leadership strengths.",
        "tags": ["Career", "Job", "Promotion"],
        "recommended_tier": "advanced"
    },
    "business_venture": {
        "id": "business_venture",
        "category": "Work",
        "title": "Business & Venture Mastery",
        "icon": "🚀",
        "purpose": "Evaluates venture launch timings, commercial partnerships, and brand numerical resonance.",
        "tags": ["Business", "Startup", "Founder"],
        "recommended_tier": "premium"
    },
    "job_interview_tactics": {
        "id": "job_interview_tactics",
        "category": "Work",
        "title": "Job Search & Interview Tactics",
        "icon": "🎯",
        "purpose": "Pinpoints high-conversion application windows, interview days, and personal presentation styles.",
        "tags": ["Job Search", "Interview", "Career"],
        "recommended_tier": "basic"
    },
    "core_blueprint": {
        "id": "core_blueprint",
        "category": "Self and Growth",
        "title": "Complete Personal Destiny Blueprint",
        "icon": "☀️",
        "purpose": "Comprehensive baseline assessment of your life purpose, hidden strengths, and karmic lessons.",
        "tags": ["Destiny", "Life Purpose", "Core"],
        "recommended_tier": "premium"
    },
    "name_spelling_calibration": {
        "id": "name_spelling_calibration",
        "category": "Self and Growth",
        "title": "Name Balancing & Spelling Calibration",
        "icon": "✍️",
        "purpose": "Chaldean vibrational analysis of your calling name to calibrate harmonious compound resonances.",
        "tags": ["Name Correction", "Spelling", "Vibration"],
        "recommended_tier": "advanced"
    },
    "personal_year_radar": {
        "id": "personal_year_radar",
        "category": "Self and Growth",
        "title": "Personal Year & Auspicious Timing Radar",
        "icon": "📅",
        "purpose": "Month-by-month cosmic timing roadmap detailing auspicious initiation and consolidation months.",
        "tags": ["Timing", "Personal Year", "Transit"],
        "recommended_tier": "advanced"
    },
    "vedic_destiny": {
        "id": "vedic_destiny",
        "category": "Self and Growth",
        "title": "Vedic Destiny & Karmic Life Path",
        "icon": "🕉️",
        "purpose": "Deterministic Driver & Conductor synthesis, Dasha timing, and karmic life roadmap.",
        "tags": ["Vedic", "Destiny", "Driver-Conductor"],
        "recommended_tier": "advanced"
    },
    "career_wealth_forecast": {
        "id": "career_wealth_forecast",
        "category": "Work & Wealth",
        "title": "Career & Wealth Timing Forecast",
        "icon": "💼",
        "purpose": "Comprehensive vocational mapping, business expansion windows, and wealth accumulation vectors.",
        "tags": ["Career", "Wealth", "Timing"],
        "recommended_tier": "advanced"
    },
    "name_balancing": {
        "id": "name_balancing",
        "category": "Self and Growth",
        "title": "Name Balancing & Acoustic Resonance",
        "icon": "✍️",
        "purpose": "Chaldean vibrational harmony analysis to optimize personal or legal calling name.",
        "tags": ["Name Balancing", "Chaldean", "Acoustics"],
        "recommended_tier": "advanced"
    },
    "lo_shu_grid": {
        "id": "lo_shu_grid",
        "category": "Self and Growth",
        "title": "Lo Shu Magic Grid & Elemental Matrix",
        "icon": "🔢",
        "purpose": "3x3 Chinese Sacred Square analysis, 8 Planes of Expression, and missing number remedies.",
        "tags": ["Lo Shu", "Planes", "Elements"],
        "recommended_tier": "advanced"
    },
    "business_brand_alignment": {
        "id": "business_brand_alignment",
        "category": "Business",
        "title": "Business & Brand Name Alignment",
        "icon": "🏢",
        "purpose": "Commercial archetype resonance, legal entity name scoring, and brand color harmony.",
        "tags": ["Business", "Brand", "Commercial"],
        "recommended_tier": "premium"
    },
    "mobile_numerology": {
        "id": "mobile_numerology",
        "category": "Practical",
        "title": "Mobile Number Vibrational Audit",
        "icon": "📱",
        "purpose": "Analysis of paired combinations, root sums, and planetary resonance of your phone number.",
        "tags": ["Mobile", "Pairs", "Communication"],
        "recommended_tier": "basic"
    },
    "relationship_compatibility": {
        "id": "relationship_compatibility",
        "category": "Love and Marriage",
        "title": "Relationship Compatibility & Synastry",
        "icon": "❤️",
        "purpose": "In-depth dual chart comparison across Vedic numbers, Lo Shu planes, and acoustic harmony.",
        "tags": ["Compatibility", "Synastry", "Marriage"],
        "recommended_tier": "advanced"
    },
    "baby_naming": {
        "id": "baby_naming",
        "category": "Family",
        "title": "Auspicious Baby Naming Blueprint",
        "icon": "👶",
        "purpose": "Auspicious starting sounds (Nakshatra / acoustic) and compound number optimization for newborns.",
        "tags": ["Baby Naming", "Auspicious", "Family"],
        "recommended_tier": "advanced"
    },
    "property_numerology": {
        "id": "property_numerology",
        "category": "Real Estate",
        "title": "Property & Address Numerology",
        "icon": "🏠",
        "purpose": "House and flat number vibrational resonance with personal Driver and Conductor energies.",
        "tags": ["Property", "Real Estate", "Silver Rajyog"],
        "recommended_tier": "basic"
    },
    "vehicle_numerology": {
        "id": "vehicle_numerology",
        "category": "Practical",
        "title": "Vehicle & License Plate Alignment",
        "icon": "🚗",
        "purpose": "License plate digit reduction and planetary harmony check for safety and auspicious travel.",
        "tags": ["Vehicle", "Travel", "Safety"],
        "recommended_tier": "basic"
    },
    "bundle_starter": {
        "id": "bundle_starter",
        "category": "Bundles",
        "title": "Starter Duo Report Pack",
        "icon": "📦",
        "purpose": "Two focused Basic reports covering foundational core life areas.",
        "tags": ["Bundle", "Starter", "Savings"],
        "recommended_tier": "basic"
    },
    "bundle_discovery": {
        "id": "bundle_discovery",
        "category": "Bundles",
        "title": "Discovery Trio Report Pack",
        "icon": "📦",
        "purpose": "Three multi-system reports synthesizing career, love, and personal timing.",
        "tags": ["Bundle", "Discovery", "Trio"],
        "recommended_tier": "advanced"
    },
    "bundle_comprehensive": {
        "id": "bundle_comprehensive",
        "category": "Bundles",
        "title": "Comprehensive Sovereign Master Bundle",
        "icon": "👑",
        "purpose": "All-inclusive complete lifetime numerological dossier covering every supported domain.",
        "tags": ["Bundle", "Master", "Sovereign"],
        "recommended_tier": "premium"
    }
}

# ── 3. PRODUCT FAMILY B: MULTI-REPORT BUNDLES ────────────────────────────────
BUNDLES: Dict[str, Dict[str, Any]] = {
    "starter_bundle": {
        "bundle_id": "starter_bundle",
        "name": "Starter Bundle",
        "display_name": "Starter Bundle · 2 Basic Reports",
        "included_reports_description": "Two Basic reports of your choice",
        "basic_report_count": 2,
        "advanced_report_count": 0,
        "premium_report_count": 0,
        "standalone_total_inr": 398,
        "bundle_price_inr": 339,
        "amount_paise": 33900,
        "savings_inr": 59,
        "savings_percent": 15,
        "digital_root": 6,
        "purpose": "Ideal for exploring two connected life domains (e.g. Love Style + Career Direction).",
        "deliverables": [
            "2 Complete 3-Page Basic PDF Reports",
            "Choose any two topics across Love, Money, Work, or Growth",
            "Full calculation breakdown and practical remedies",
            "Ready within minutes in your account dashboard with archival PDF download"
        ]
    },
    "discovery_bundle": {
        "bundle_id": "discovery_bundle",
        "name": "Discovery Bundle",
        "display_name": "Discovery Bundle · 3 Advanced Reports",
        "included_reports_description": "Three Advanced reports of your choice",
        "basic_report_count": 0,
        "advanced_report_count": 3,
        "premium_report_count": 0,
        "standalone_total_inr": 1530,
        "bundle_price_inr": 1299,
        "amount_paise": 129900,
        "savings_inr": 231,
        "savings_percent": 15,
        "digital_root": 3,
        "popular": True,
        "purpose": "Broad 3-domain diagnostic covering Relationships, Career, and Wealth foundations.",
        "deliverables": [
            "3 Complete 12-Page Advanced Master Reports",
            "Choose any three topics from the entire catalogue",
            "Enabled Numbers in Depth & Auspicious Initiation Windows for each topic",
            "7-Layer safe planetary remedy protocols for selected domains"
        ]
    },
    "comprehensive_bundle": {
        "bundle_id": "comprehensive_bundle",
        "name": "Comprehensive Bundle",
        "display_name": "Comprehensive Bundle · 5 Advanced Reports",
        "included_reports_description": "Five 12-page Advanced reports across major life pillars",
        "basic_report_count": 0,
        "advanced_report_count": 5,
        "premium_report_count": 0,
        "standalone_total_inr": 2550,
        "bundle_price_inr": 1999,
        "amount_paise": 199900,
        "savings_inr": 551,
        "savings_percent": 22,
        "digital_root": 1,
        "purpose": "Deep exploration for seekers making major life decisions across multiple domains.",
        "deliverables": [
            "5 Complete 12-Page Advanced Master Reports",
            "Complete multi-domain lifetime clarity across Love, Career, Wealth & Family",
            "Enabled Numbers in Depth & Auspicious Initiation Windows for each domain",
            "7-Layer safe planetary remedy protocols & auspicious timing windows"
        ]
    }
}

# ── 4. PRODUCT FAMILY C: CHARM AI ACCESS ────────────────────────────────────
CHARM_AI_PACKS: Dict[str, Dict[str, Any]] = {
    "charm_free": {
        "pack_id": "charm_free",
        "name": "Free Preview",
        "display_name": "Charm AI · Free Preview",
        "price_inr": 0,
        "amount_paise": 0,
        "questions_count": 3,
        "has_remedies": False,
        "purpose": "Experience conversational Charm AI intelligence with 3 free exploratory inquiries daily.",
        "deliverables": [
            "3 Free Exploratory Inquiries Daily per Account",
            "Instant Driver / Conductor token verification",
            "24/7 web access"
        ]
    },
    "charm_single": {
        "pack_id": "charm_single",
        "name": "Charm AI Starter Pack",
        "display_name": "Charm AI · Starter Pack",
        "price_inr": 199,
        "amount_paise": 19900,
        "questions_count": 5,
        "has_remedies": True,
        "digital_root": 1,
        "purpose": "Focused query resolution for immediate decision crossroads.",
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
        "display_name": "Charm AI · Multi-Reading Pack",
        "price_inr": 399,
        "amount_paise": 39900,
        "questions_count": 10,
        "has_remedies": True,
        "popular": True,
        "purpose": "Ongoing strategic guidance covering career, relationships, and finance.",
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
        "display_name": "Charm AI · Extended Pack",
        "price_inr": 699,
        "amount_paise": 69900,
        "questions_count": 25,
        "has_remedies": True,
        "purpose": "Comprehensive conversational companion for active founders and decision-makers.",
        "deliverables": [
            "25 Deep In-Depth Predictions",
            "Interactive chart companion with transit radar",
            "Multi-profile synastry consultation capability",
            "Downloadable consultation transcript",
            "Credits valid for 12 months with rollover"
        ]
    }
}

# ── 5. PRODUCT FAMILY D: HUMAN CONSULTATION ──────────────────────────────────
CONSULTATION_PACKS: Dict[str, Dict[str, Any]] = {
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
            "Complimentary 12-Page Advanced PDF Dossier (₹489 value)",
            "Audio recording and written consultation summary",
            "Free 1-time rescheduling up to 24 hours prior"
        ]
    }
}


def get_all_product_skus() -> Dict[str, Dict[str, Any]]:
    """
    Returns a unified flat lookup dictionary of all purchasable SKUs with
    authoritative price and metadata.
    """
    skus: Dict[str, Dict[str, Any]] = {}

    # Standalone report tiers
    for tier_id, tier in REPORT_TIERS.items():
        skus[f"report_{tier_id}"] = {
            "sku_id": f"report_{tier_id}",
            "family": "standalone_report",
            "name": tier["name"],
            "tier": tier_id,
            "pages": tier["pages"],
            "amount_inr": tier["price_inr"],
            "amount_paise": tier["amount_paise"],
            "original_price_inr": tier.get("original_price_inr", tier.get("mrp_inr", tier["price_inr"])),
            "currency": CURRENCY,
            "deliverables": tier["deliverables"]
        }

    # Bundles
    for b_id, bundle in BUNDLES.items():
        skus[b_id] = {
            "sku_id": b_id,
            "family": "bundle",
            "name": bundle["name"],
            "amount_inr": bundle["bundle_price_inr"],
            "amount_paise": bundle["amount_paise"],
            "original_price_inr": bundle.get("standalone_total_inr", bundle["bundle_price_inr"]),
            "currency": CURRENCY,
            "deliverables": bundle["deliverables"]
        }

    # Charm AI
    for p_id, pack in CHARM_AI_PACKS.items():
        skus[p_id] = {
            "sku_id": p_id,
            "family": "charm_ai",
            "name": pack["name"],
            "questions_count": pack["questions_count"],
            "amount_inr": pack["price_inr"],
            "amount_paise": pack["amount_paise"],
            "original_price_inr": pack.get("original_price_inr", pack["price_inr"]),
            "currency": CURRENCY,
            "deliverables": pack["deliverables"]
        }

    # Consultations
    for c_id, consult in CONSULTATION_PACKS.items():
        skus[c_id] = {
            "sku_id": c_id,
            "family": "consultation",
            "name": consult["name"],
            "amount_inr": consult["price_inr"],
            "amount_paise": consult["amount_paise"],
            "original_price_inr": consult.get("original_price_inr", consult["price_inr"]),
            "currency": CURRENCY,
            "deliverables": consult["deliverables"]
        }

    return skus


def resolve_sku_price(sku_or_plan_id: str) -> Optional[Dict[str, Any]]:
    """
    Given a SKU ID or legacy plan ID, safely resolves the authoritative server price.
    Never trusts client input.
    """
    clean_id = sku_or_plan_id.lower().strip()
    skus = get_all_product_skus()

    if clean_id in skus:
        return skus[clean_id]

    # Map legacy aliases safely to unified SKUs
    alias_map = {
        # Standalone report aliases
        "basic": "report_basic",
        "starter": "report_basic",
        "report_essential": "report_basic",
        "advanced": "report_advanced",
        "growth": "report_advanced",
        "report_master": "report_advanced",
        "premium": "report_premium",
        "complete": "report_premium",
        "report_divine": "report_premium",
        "complete_report": "report_premium",

        # Charm AI aliases
        "starter_5q": "charm_single",
        "ai_starter_5q": "charm_single",
        "growth_10q": "charm_multi",
        "ai_growth_15q": "charm_multi",
        "ai_power_35q": "charm_extended",
        "ai_report_combo": "charm_extended",

        # Bundles aliases
        "bundle_starter": "starter_bundle",
        "bundle_discovery": "discovery_bundle",
        "bundle_comprehensive": "comprehensive_bundle",

        # Consultation aliases
        "consultation": "consultation_standard",
        "personal_consult": "consultation_standard",
        "phone_consult": "consultation_standard",
        "master_consultation": "consultation_standard",
        "advisory_personal_name": "consultation_standard",
    }

    if clean_id in alias_map:
        target_sku = alias_map[clean_id]
        if target_sku in skus:
            return skus[target_sku]

    return None


def is_notify_me_higher_tiers_enabled() -> bool:
    """
    Returns True only when the Advanced/Premium 'Notify me' waitlist flag is enabled.
    Defaults strictly to False ([PENDING LAUNCH DECISION]).
    """
    env_val = os.getenv("NV_NOTIFY_ME_HIGHER_TIERS")
    if env_val is not None and env_val.strip() != "":
        return env_val.strip().lower() in ("true", "1", "yes")
    try:
        packs_path = os.path.join(os.path.dirname(__file__), "packs.json")
        with open(packs_path, "r", encoding="utf-8") as fh:
            packs_data = json.load(fh)
        return bool(packs_data.get("feature_flags", {}).get("notify_me_higher_tiers", False))
    except Exception:
        return False


def recommend_ladder_tier(
    gap_count: Optional[int] = None,
    notify_me_higher_tiers: Optional[bool] = None,
) -> str:
    """
    Deterministic 3-card report ladder recommendation rule:
    - When `notify_me_higher_tiers` is True: strictly recommends `report_basic`
      (never recommends a waitlist tier).
    - When `notify_me_higher_tiers` is False: recommends by Lo Shu birth-date gap count
      (`gap_count` = missing digits out of 1..9):
        * 0–2 open cells -> `report_basic`
        * 3–5 open cells -> `report_advanced`
        * 6–9 open cells -> `report_premium`
      (Defaults to `report_advanced` when `gap_count` is not yet known.)
    """
    notify_active = (
        is_notify_me_higher_tiers_enabled()
        if notify_me_higher_tiers is None
        else bool(notify_me_higher_tiers)
    )
    if notify_active:
        return "report_basic"
    if gap_count is None:
        return "report_advanced"
    gaps = max(0, min(9, int(gap_count)))
    if gaps <= 2:
        return "report_basic"
    if gaps <= 5:
        return "report_advanced"
    return "report_premium"


def export_pricing_catalog_json() -> str:
    """Exports full public catalog for frontend consumers and API responses."""
    notify_active = is_notify_me_higher_tiers_enabled()
    catalog = {
        "currency": CURRENCY,
        "feature_flags": {
            "notify_me_higher_tiers": notify_active,
            "notify_me_tiers": ["report_advanced", "report_premium"]
        },
        "ladder_recommendation_rule": {
            "when_notify_me_true": "report_basic",
            "when_notify_me_false": {
                "0_to_2_gaps": "report_basic",
                "3_to_5_gaps": "report_advanced",
                "6_to_9_gaps": "report_premium",
                "unknown_gaps_default": "report_advanced",
            },
            "default_recommended_tier": recommend_ladder_tier(None, notify_active),
        },
        "report_tiers": REPORT_TIERS,
        "supported_topics": SUPPORTED_REPORT_TOPICS,
        "bundles": BUNDLES,
        "charm_ai": CHARM_AI_PACKS,
        "consultation": CONSULTATION_PACKS,
        "all_skus": get_all_product_skus()
    }
    return json.dumps(catalog, indent=2)
