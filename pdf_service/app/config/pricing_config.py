"""
NUMEROS VISION — CENTRAL AUTHORITATIVE PRICING ARCHITECTURE (v2.3.0)
Tagline: ANVEIL EVERY CHARM

Single server-side source of truth: reads `app/config/packs.json` directly
(the exact same canonical pack catalog used by the Cloudflare Worker).
Zero second price tables or hardcoded fallback amounts exist in Python.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta, timezone
import json
import os

PACKS_JSON_PATH = os.path.join(os.path.dirname(__file__), "packs.json")
IST_TZ = timezone(timedelta(hours=5, minutes=30))


def load_packs_json() -> Dict[str, Any]:
    """Loads the canonical `app/config/packs.json` catalog."""
    with open(PACKS_JSON_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


def _build_report_tiers(packs_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    tiers: Dict[str, Dict[str, Any]] = {}
    waitlist_label = (
        packs_data.get("feature_flags", {}).get("waitlist_display_label")
        or "Coming soon, notify me"
    )
    for pack_id, pack in (packs_data.get("core_reports") or {}).items():
        tier_id = str(pack.get("tier_id") or pack_id.replace("report_", "")).strip()
        pages = int(pack.get("pages") or 0)
        tiers[tier_id] = {
            "pack_id": pack_id,
            "tier_id": tier_id,
            "name": pack["name"],
            "descriptor": pack.get("descriptor", ""),
            "display_name": pack.get("display_name", pack["name"]),
            "pages": pages,
            "page_target": f"{pages}-page PDF" if pages else "PDF",
            "price_inr": pack.get("price_inr"),
            "amount_paise": pack.get("amount_paise"),
            "mrp_inr": pack.get("mrp_inr"),
            "mrp_paise": pack.get("mrp_paise"),
            "digital_root": pack.get("digital_root"),
            "mrp_digital_root": pack.get("mrp_digital_root"),
            "status": pack.get("status", "coming_soon"),
            "waitlist_only": bool(pack.get("waitlist_only", pack.get("price_inr") is None)),
            "display_price_label": pack.get("display_price_label")
            or (waitlist_label if pack.get("price_inr") is None else f"₹{int(pack['price_inr']):,}"),
            "deliverables": list(pack.get("deliverables") or []),
            "progressive_unlock": pack.get("progressive_unlock", ""),
        }
    return tiers


def _build_bundles(packs_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    bundles: Dict[str, Dict[str, Any]] = {}
    waitlist_label = (
        packs_data.get("feature_flags", {}).get("waitlist_display_label")
        or "Coming soon, notify me"
    )
    for b_id, bundle in (packs_data.get("bundles") or {}).items():
        vouchers = bundle.get("voucher_allocation") or {}
        bundles[b_id] = {
            "bundle_id": b_id,
            "pack_id": bundle.get("pack_id", b_id),
            "name": bundle["name"],
            "display_name": bundle.get("display_name", bundle["name"]),
            "basic_report_count": int(vouchers.get("basic_vouchers", 0)),
            "advanced_report_count": int(vouchers.get("advanced_vouchers", 0)),
            "premium_report_count": int(vouchers.get("premium_vouchers", 0)),
            "price_inr": bundle.get("price_inr"),
            "bundle_price_inr": bundle.get("price_inr"),
            "amount_paise": bundle.get("amount_paise"),
            "status": bundle.get("status", "coming_soon"),
            "waitlist_only": bool(bundle.get("waitlist_only", bundle.get("price_inr") is None)),
            "display_price_label": bundle.get("display_price_label", waitlist_label),
            "deliverables": list(bundle.get("deliverables") or []),
        }
    return bundles


def _build_charm_ai_packs(packs_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    charm: Dict[str, Dict[str, Any]] = {}
    for p_id, pack in (packs_data.get("charm_ai") or {}).items():
        q_count = int(pack.get("questions_count") or 0)
        charm[p_id] = {
            "pack_id": pack.get("pack_id", p_id),
            "name": pack["name"],
            "descriptor": pack.get("descriptor", ""),
            "display_name": pack.get("display_name", pack["name"]),
            "price_inr": pack.get("price_inr"),
            "amount_paise": pack.get("amount_paise"),
            "questions_count": q_count,
            "digital_root": pack.get("digital_root"),
            "has_remedies": bool(p_id != "charm_free" and q_count > 3),
            "status": pack.get("status", "inactive"),
            "deliverables": list(pack.get("deliverables") or []),
        }
    return charm


def _build_annual_planners(packs_data: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    planners: Dict[str, Dict[str, Any]] = {}
    waitlist_label = (
        packs_data.get("feature_flags", {}).get("waitlist_display_label")
        or "Coming soon, notify me"
    )
    for pl_id, pl in (packs_data.get("annual_planners") or {}).items():
        planners[pl_id] = {
            "pack_id": pl.get("pack_id", pl_id),
            "tier_id": pl.get("tier_id", pl_id),
            "name": pl["name"],
            "display_name": pl.get("display_name", pl["name"]),
            "pages": int(pl.get("pages") or 24),
            "price_inr": pl.get("price_inr"),
            "amount_paise": pl.get("amount_paise"),
            "list_price_inr": pl.get("list_price_inr"),
            "list_price_paise": pl.get("list_price_paise"),
            "offer_price_inr": pl.get("offer_price_inr"),
            "offer_price_paise": pl.get("offer_price_paise"),
            "offer_ends_at": pl.get("offer_ends_at"),
            "status": pl.get("status", "coming_soon"),
            "waitlist_only": bool(pl.get("waitlist_only", pl.get("price_inr") is None)),
            "display_price_label": pl.get("display_price_label", waitlist_label),
            "deliverables": list(pl.get("deliverables") or []),
        }
    return planners


_INITIAL_PACKS = load_packs_json()
CURRENCY: str = str(_INITIAL_PACKS.get("currency", "INR"))
LADDER_ORDER: List[str] = list(
    _INITIAL_PACKS.get("ladder_order", ["report_premium", "report_advanced", "report_basic"])
)
LAUNCH_OFFER_DURATION_DAYS: int = int(
    (_INITIAL_PACKS.get("launch_offer") or {}).get("duration_days", 7)
)
LAUNCH_OFFER_DURATION_SECONDS: int = LAUNCH_OFFER_DURATION_DAYS * 24 * 3600
LAUNCH_OFFER_STARTED_AT_DEFAULT: Optional[str] = (
    _INITIAL_PACKS.get("launch_offer") or {}
).get("started_at")
LAUNCH_OFFER_ENDS_AT_DEFAULT: Optional[str] = (
    _INITIAL_PACKS.get("launch_offer") or {}
).get("ends_at")
WAITLIST_DISPLAY_LABEL: str = str(
    (_INITIAL_PACKS.get("feature_flags") or {}).get(
        "waitlist_display_label", "Coming soon, notify me"
    )
)
WAITLIST_LAUNCH_CAPTION: str = str(
    (_INITIAL_PACKS.get("feature_flags") or {}).get(
        "waitlist_launch_caption",
        "When this report opens, it starts at a launch price for its first 7 days. We\u2019ll email you the day it opens.",
    )
)

# Derived strictly from app/config/packs.json (zero second price table)
REPORT_TIERS: Dict[str, Dict[str, Any]] = _build_report_tiers(_INITIAL_PACKS)
BUNDLES: Dict[str, Dict[str, Any]] = _build_bundles(_INITIAL_PACKS)
CHARM_AI_PACKS: Dict[str, Dict[str, Any]] = _build_charm_ai_packs(_INITIAL_PACKS)
ANNUAL_PLANNERS: Dict[str, Dict[str, Any]] = _build_annual_planners(_INITIAL_PACKS)
CONSULTATION_PACKS: Dict[str, Dict[str, Any]] = {}

# ── SUPPORTED REPORT TOPICS (TOPIC METADATA ONLY — ZERO PRICES) ──────────────
SUPPORTED_REPORT_TOPICS: Dict[str, Dict[str, Any]] = {
    "love_romance": {
        "id": "love_romance",
        "category": "Love and Marriage",
        "title": "Love Style & Romance Profile",
        "icon": "💖",
        "purpose": "Uncovers your relationship blueprint, emotional attraction triggers, and partnership style.",
        "tags": ["Love", "Relationships", "Partnership"],
        "recommended_tier": "advanced",
    },
    "marriage_union": {
        "id": "marriage_union",
        "category": "Love and Marriage",
        "title": "Marriage Timing & Union Blueprint",
        "icon": "💍",
        "purpose": "Evaluates auspicious union windows, spousal harmony factors, and long-term marital alignment.",
        "tags": ["Marriage", "Timing", "Harmony"],
        "recommended_tier": "advanced",
    },
    "partner_compatibility": {
        "id": "partner_compatibility",
        "category": "Love and Marriage",
        "title": "Ideal Partner Compatibility",
        "icon": "⚖️",
        "purpose": "Dual-chart synastry comparing Driver, Conductor, and Lo Shu grid polarities between two individuals.",
        "tags": ["Compatibility", "Synastry", "Dating"],
        "recommended_tier": "advanced",
    },
    "love_or_arrange": {
        "id": "love_or_arrange",
        "category": "Love and Marriage",
        "title": "Love or Arrange Exploration",
        "icon": "🕊️",
        "purpose": "Identifies numerical indicators of self-chosen versus family-facilitated marriage harmony.",
        "tags": ["Marriage", "Decision", "Family"],
        "recommended_tier": "basic",
    },
    "spouse_personality": {
        "id": "spouse_personality",
        "category": "Love and Marriage",
        "title": "Spouse Personality & Life Alignment",
        "icon": "🔮",
        "purpose": "Archetypal profile of probable spouse traits, vocational leanings, and life temperament.",
        "tags": ["Spouse", "Traits", "Alignment"],
        "recommended_tier": "advanced",
    },
    "family_harmony": {
        "id": "family_harmony",
        "category": "Love and Marriage",
        "title": "In-Laws & Family Harmony",
        "icon": "🏡",
        "purpose": "Examines interpersonal family dynamics, domestic peace, and emotional grounding strategies.",
        "tags": ["Family", "In-laws", "Peace"],
        "recommended_tier": "basic",
    },
    "wealth_abundance": {
        "id": "wealth_abundance",
        "category": "Money",
        "title": "Wealth & Abundance Report",
        "icon": "💰",
        "purpose": "Identifies your financial growth catalysts, wealth retention numbers, and prosperity cycles.",
        "tags": ["Money", "Wealth", "Finance"],
        "recommended_tier": "advanced",
    },
    "billionaire_potential": {
        "id": "billionaire_potential",
        "category": "Money",
        "title": "High-Growth Commercial Potential",
        "icon": "🏛️",
        "purpose": "Explores enterprise scale capacity, high-stakes decision cycles, and institutional wealth vectors.",
        "tags": ["Enterprise", "Scale", "Ambition"],
        "recommended_tier": "premium",
    },
    "career_growth": {
        "id": "career_growth",
        "category": "Work",
        "title": "Career Direction & Growth",
        "icon": "💼",
        "purpose": "Maps your optimal vocational pathways, promotion cycles, and leadership strengths.",
        "tags": ["Career", "Job", "Promotion"],
        "recommended_tier": "advanced",
    },
    "business_venture": {
        "id": "business_venture",
        "category": "Work",
        "title": "Business & Venture Mastery",
        "icon": "🚀",
        "purpose": "Evaluates venture launch timings, commercial partnerships, and brand numerical resonance.",
        "tags": ["Business", "Startup", "Founder"],
        "recommended_tier": "premium",
    },
    "job_interview_tactics": {
        "id": "job_interview_tactics",
        "category": "Work",
        "title": "Job Search & Interview Tactics",
        "icon": "🎯",
        "purpose": "Pinpoints high-conversion application windows, interview days, and personal presentation styles.",
        "tags": ["Job Search", "Interview", "Career"],
        "recommended_tier": "basic",
    },
    "core_blueprint": {
        "id": "core_blueprint",
        "category": "Self and Growth",
        "title": "Complete Personal Destiny Blueprint",
        "icon": "☀️",
        "purpose": "Comprehensive baseline assessment of your life purpose, hidden strengths, and karmic lessons.",
        "tags": ["Destiny", "Life Purpose", "Core"],
        "recommended_tier": "premium",
    },
    "name_spelling_calibration": {
        "id": "name_spelling_calibration",
        "category": "Self and Growth",
        "title": "Name Balancing & Spelling Calibration",
        "icon": "✍️",
        "purpose": "Chaldean vibrational analysis of your calling name to calibrate harmonious compound resonances.",
        "tags": ["Name Correction", "Spelling", "Vibration"],
        "recommended_tier": "advanced",
    },
    "personal_year_radar": {
        "id": "personal_year_radar",
        "category": "Self and Growth",
        "title": "Personal Year & Auspicious Timing Radar",
        "icon": "📅",
        "purpose": "Month-by-month cosmic timing roadmap detailing auspicious initiation and consolidation months.",
        "tags": ["Timing", "Personal Year", "Transit"],
        "recommended_tier": "advanced",
    },
    "vedic_destiny": {
        "id": "vedic_destiny",
        "category": "Self and Growth",
        "title": "Vedic Destiny & Karmic Life Path",
        "icon": "🕉️",
        "purpose": "Deterministic Driver & Conductor synthesis, Dasha timing, and karmic life roadmap.",
        "tags": ["Vedic", "Destiny", "Driver-Conductor"],
        "recommended_tier": "advanced",
    },
    "career_wealth_forecast": {
        "id": "career_wealth_forecast",
        "category": "Work & Wealth",
        "title": "Career & Wealth Timing Forecast",
        "icon": "💼",
        "purpose": "Comprehensive vocational mapping, business expansion windows, and wealth accumulation vectors.",
        "tags": ["Career", "Wealth", "Timing"],
        "recommended_tier": "advanced",
    },
    "name_balancing": {
        "id": "name_balancing",
        "category": "Self and Growth",
        "title": "Name Balancing & Acoustic Resonance",
        "icon": "✍️",
        "purpose": "Chaldean vibrational harmony analysis to optimize personal or legal calling name.",
        "tags": ["Name Balancing", "Chaldean", "Acoustics"],
        "recommended_tier": "advanced",
    },
    "lo_shu_grid": {
        "id": "lo_shu_grid",
        "category": "Self and Growth",
        "title": "Lo Shu Magic Grid & Elemental Matrix",
        "icon": "🔢",
        "purpose": "3x3 Chinese Sacred Square analysis, 8 Planes of Expression, and missing number remedies.",
        "tags": ["Lo Shu", "Planes", "Elements"],
        "recommended_tier": "advanced",
    },
    "business_brand_alignment": {
        "id": "business_brand_alignment",
        "category": "Business",
        "title": "Business & Brand Name Alignment",
        "icon": "🏢",
        "purpose": "Commercial archetype resonance, legal entity name scoring, and brand color harmony.",
        "tags": ["Business", "Brand", "Commercial"],
        "recommended_tier": "premium",
    },
    "mobile_numerology": {
        "id": "mobile_numerology",
        "category": "Practical",
        "title": "Mobile Number Vibrational Audit",
        "icon": "📱",
        "purpose": "Analysis of paired combinations, root sums, and planetary resonance of your phone number.",
        "tags": ["Mobile", "Pairs", "Communication"],
        "recommended_tier": "basic",
    },
    "relationship_compatibility": {
        "id": "relationship_compatibility",
        "category": "Love and Marriage",
        "title": "Relationship Compatibility & Synastry",
        "icon": "❤️",
        "purpose": "In-depth dual chart comparison across Vedic numbers, Lo Shu planes, and acoustic harmony.",
        "tags": ["Compatibility", "Synastry", "Marriage"],
        "recommended_tier": "advanced",
    },
    "baby_naming": {
        "id": "baby_naming",
        "category": "Family",
        "title": "Auspicious Baby Naming Blueprint",
        "icon": "👶",
        "purpose": "Auspicious starting sounds (Nakshatra / acoustic) and compound number optimization for newborns.",
        "tags": ["Baby Naming", "Auspicious", "Family"],
        "recommended_tier": "advanced",
    },
    "property_numerology": {
        "id": "property_numerology",
        "category": "Real Estate",
        "title": "Property & Address Numerology",
        "icon": "🏠",
        "purpose": "House and flat number vibrational resonance with personal Driver and Conductor energies.",
        "tags": ["Property", "Real Estate", "Silver Rajyog"],
        "recommended_tier": "basic",
    },
    "vehicle_numerology": {
        "id": "vehicle_numerology",
        "category": "Practical",
        "title": "Vehicle & License Plate Alignment",
        "icon": "🚗",
        "purpose": "License plate digit reduction and planetary harmony check for safety and auspicious travel.",
        "tags": ["Vehicle", "Travel", "Safety"],
        "recommended_tier": "basic",
    },
    "bundle_starter": {
        "id": "bundle_starter",
        "category": "Bundles",
        "title": "Starter Duo Report Pack",
        "icon": "📦",
        "purpose": "Two focused Basic reports covering foundational core life areas.",
        "tags": ["Bundle", "Starter", "Savings"],
        "recommended_tier": "basic",
    },
    "bundle_discovery": {
        "id": "bundle_discovery",
        "category": "Bundles",
        "title": "Discovery Trio Report Pack",
        "icon": "📦",
        "purpose": "Three multi-system reports synthesizing career, love, and personal timing.",
        "tags": ["Bundle", "Discovery", "Trio"],
        "recommended_tier": "advanced",
    },
    "bundle_comprehensive": {
        "id": "bundle_comprehensive",
        "category": "Bundles",
        "title": "Comprehensive Sovereign Master Bundle",
        "icon": "👑",
        "purpose": "All-inclusive complete lifetime numerological dossier covering every supported domain.",
        "tags": ["Bundle", "Master", "Sovereign"],
        "recommended_tier": "premium",
    },
}


def _parse_iso_dt(ts: str) -> datetime:
    cleaned = str(ts).strip().replace("Z", "+00:00")
    dt = datetime.fromisoformat(cleaned)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _format_ist_date(dt: datetime, include_time: bool = False) -> str:
    ist_dt = dt.astimezone(IST_TZ)
    base = f"{ist_dt.day} {ist_dt.strftime('%b %Y')}"
    if include_time:
        return f"{base}, {ist_dt.strftime('%H:%M')} IST"
    return base


def resolve_launch_offer_state(
    now_iso: Optional[str] = None,
    ends_at_override: Optional[str] = None,
    starts_at_override: Optional[str] = None,
    tier_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Resolves the server-configured launch offer window strictly from per-tier
    `NV_LAUNCH_<TIER>_STARTS_AT`/`NV_LAUNCH_<TIER>_ENDS_AT` falling back to
    `NV_LAUNCH_STARTS_AT` (alias `NV_LAUNCH_STARTED_AT`) and `NV_LAUNCH_ENDS_AT`.
    """
    clean_tier = str(tier_id or "").strip().lower().replace("report_", "")
    tier_starts = ""
    tier_ends = ""
    if clean_tier in ("basic", "advanced", "premium"):
        upper = clean_tier.upper()
        tier_starts = (
            os.getenv(f"NV_LAUNCH_{upper}_STARTS_AT")
            or os.getenv(f"NV_LAUNCH_{upper}_STARTED_AT")
            or ""
        ).strip()
        tier_ends = (os.getenv(f"NV_LAUNCH_{upper}_ENDS_AT") or "").strip()

    env_starts = (
        tier_starts
        or (os.getenv("NV_LAUNCH_STARTS_AT") or os.getenv("NV_LAUNCH_STARTED_AT") or "").strip()
    )
    env_ends = tier_ends or (os.getenv("NV_LAUNCH_ENDS_AT") or "").strip()

    started_raw: Optional[str] = (
        starts_at_override.strip()
        if isinstance(starts_at_override, str) and starts_at_override.strip()
        else (env_starts or None)
    )
    ends_raw: Optional[str] = (
        ends_at_override.strip()
        if isinstance(ends_at_override, str) and ends_at_override.strip()
        else (env_ends or None)
    )

    if not ends_raw:
        env_mode = (os.getenv("ENVIRONMENT") or "production").strip().lower()
        force_raw = (os.getenv("NV_FORCE_LAUNCH_MODE") or "").strip().lower()
        if env_mode != "production" and force_raw in ("1", "true", "yes", "on"):
            return {
                "active": True,
                "configured": True,
                "forced": True,
                "duration_days": LAUNCH_OFFER_DURATION_DAYS,
                "duration_hours": LAUNCH_OFFER_DURATION_DAYS * 24,
                "started_at": None,
                "ends_at": None,
                "until_date": "",
                "from_date": "",
                "label": "Launch price active during the launch window.",
            }
        return {
            "active": False,
            "configured": False,
            "forced": False,
            "duration_days": LAUNCH_OFFER_DURATION_DAYS,
            "duration_hours": LAUNCH_OFFER_DURATION_DAYS * 24,
            "started_at": None,
            "ends_at": None,
            "until_date": "",
            "from_date": "",
            "label": "",
        }

    ends_dt = _parse_iso_dt(ends_raw)
    started_dt = (
        _parse_iso_dt(started_raw)
        if started_raw
        else (ends_dt - timedelta(days=LAUNCH_OFFER_DURATION_DAYS))
    )
    from_dt = ends_dt + timedelta(seconds=1)
    now_dt = _parse_iso_dt(now_iso) if now_iso else datetime.now(timezone.utc)
    is_active = started_dt <= now_dt <= ends_dt
    short_window = (ends_dt - started_dt) < timedelta(days=1)
    until_str = _format_ist_date(ends_dt, include_time=short_window)
    from_str = _format_ist_date(from_dt, include_time=short_window)
    return {
        "active": is_active,
        "configured": True,
        "duration_days": LAUNCH_OFFER_DURATION_DAYS,
        "duration_hours": LAUNCH_OFFER_DURATION_DAYS * 24,
        "started_at": started_dt.isoformat(),
        "ends_at": ends_dt.isoformat(),
        "until_date": until_str,
        "from_date": from_str,
        "label": (
            f"Launch price until {until_str}."
            if is_active
            else f"Regular pricing in effect from {from_str}."
        ),
    }


def is_notify_me_higher_tiers_enabled() -> bool:
    """Returns True when the Advanced/Premium 'Notify me' waitlist flag is enabled."""
    env_val = os.getenv("NV_NOTIFY_ME_HIGHER_TIERS")
    if env_val is not None and env_val.strip() != "":
        return env_val.strip().lower() in ("true", "1", "yes")
    try:
        packs_data = load_packs_json()
        return bool(packs_data.get("feature_flags", {}).get("notify_me_higher_tiers", True))
    except Exception:
        return True


def format_launch_offer_copy(
    sku_or_tier_id: str,
    now_iso: Optional[str] = None,
    ends_at_override: Optional[str] = None,
    starts_at_override: Optional[str] = None,
    notify_me_higher_tiers: Optional[bool] = None,
) -> str:
    """Returns launch/regular price notice ONLY for purchasable report SKUs."""
    tier_key = str(sku_or_tier_id or "").strip().lower().replace("report_", "")
    packs_data = load_packs_json()
    report_tiers = _build_report_tiers(packs_data)
    tier = report_tiers.get(tier_key)
    if not tier:
        return ""
    notify_active = (
        is_notify_me_higher_tiers_enabled()
        if notify_me_higher_tiers is None
        else bool(notify_me_higher_tiers)
    )
    if (
        tier.get("waitlist_only")
        or tier.get("price_inr") is None
        or tier.get("mrp_inr") is None
        or (notify_active and tier_key in ("advanced", "premium"))
    ):
        return ""
    mrp_inr = int(tier["mrp_inr"])
    state = resolve_launch_offer_state(
        now_iso=now_iso,
        ends_at_override=ends_at_override,
        starts_at_override=starts_at_override,
        tier_id=tier_key,
    )
    if not state.get("configured"):
        return ""
    if state["active"]:
        if state.get("forced") and not state.get("until_date"):
            return f"Launch price active during the launch window. Regular price ₹{mrp_inr:,} thereafter."
        return f"Launch price until {state['until_date']}. Regular price ₹{mrp_inr:,} from {state['from_date']}."
    if state.get("from_date"):
        return f"Regular price ₹{mrp_inr:,} (effective {state['from_date']})."
    return f"Regular price ₹{mrp_inr:,}."


def get_all_product_skus(
    now_iso: Optional[str] = None,
    ends_at_override: Optional[str] = None,
    starts_at_override: Optional[str] = None,
    notify_me_higher_tiers: Optional[bool] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Returns a unified flat lookup dictionary of all SKUs strictly derived from `packs.json`.
    """
    packs_data = load_packs_json()
    currency = str(packs_data.get("currency", "INR"))
    ff = packs_data.get("feature_flags") or {}
    wl_label = str(ff.get("waitlist_display_label", WAITLIST_DISPLAY_LABEL))
    wl_caption = str(ff.get("waitlist_launch_caption", WAITLIST_LAUNCH_CAPTION))

    skus: Dict[str, Dict[str, Any]] = {}
    notify_active = (
        is_notify_me_higher_tiers_enabled()
        if notify_me_higher_tiers is None
        else bool(notify_me_higher_tiers)
    )

    # 1. Core reports from packs.json
    for pack_id, pack in (packs_data.get("core_reports") or {}).items():
        tier_id = str(pack.get("tier_id") or pack_id.replace("report_", "")).strip()
        is_waitlist = (
            bool(pack.get("waitlist_only"))
            or pack.get("price_inr") is None
            or (notify_active and tier_id in ("advanced", "premium"))
        )
        if is_waitlist:
            skus[pack_id] = {
                "sku_id": pack_id,
                "family": "standalone_report",
                "name": pack["name"],
                "descriptor": pack.get("descriptor", ""),
                "display_name": pack.get("display_name", pack["name"]),
                "tier": tier_id,
                "pages": int(pack.get("pages") or 0),
                "waitlist_only": True,
                "status": "waitlist",
                "display_price_label": pack.get("display_price_label") or wl_label,
                "waitlist_caption": wl_caption,
                "launch_price_inr": None,
                "launch_amount_paise": None,
                "amount_inr": None,
                "amount_paise": None,
                "mrp_inr": None,
                "mrp_paise": None,
                "struck_mrp_inr": None,
                "show_strike_through": False,
                "launch_offer_active": False,
                "launch_offer_copy": "",
                "original_price_inr": None,
                "currency": currency,
                "deliverables": list(pack.get("deliverables") or []),
            }
            continue

        launch_inr = int(pack["price_inr"])
        launch_paise = int(pack.get("amount_paise") or (launch_inr * 100))
        mrp_inr = int(pack.get("mrp_inr") if pack.get("mrp_inr") is not None else launch_inr)
        mrp_paise = int(pack.get("mrp_paise") if pack.get("mrp_paise") is not None else (mrp_inr * 100))

        tier_launch_state = resolve_launch_offer_state(
            now_iso=now_iso,
            ends_at_override=ends_at_override,
            starts_at_override=starts_at_override,
            tier_id=tier_id,
        )
        tier_launch_active = bool(tier_launch_state.get("active"))
        active_inr = launch_inr if tier_launch_active else mrp_inr
        active_paise = launch_paise if tier_launch_active else mrp_paise

        skus[pack_id] = {
            "sku_id": pack_id,
            "family": "standalone_report",
            "name": pack["name"],
            "descriptor": pack.get("descriptor", ""),
            "display_name": pack.get("display_name", pack["name"]),
            "tier": tier_id,
            "pages": int(pack.get("pages") or 0),
            "waitlist_only": False,
            "status": str(pack.get("status", "active")),
            "display_price_label": f"₹{active_inr:,}",
            "launch_price_inr": launch_inr,
            "launch_amount_paise": launch_paise,
            "amount_inr": active_inr,
            "amount_paise": active_paise,
            "mrp_inr": mrp_inr,
            "mrp_paise": mrp_paise,
            "struck_mrp_inr": mrp_inr if tier_launch_active else None,
            "show_strike_through": tier_launch_active,
            "launch_offer_active": tier_launch_active,
            "launch_offer_copy": format_launch_offer_copy(
                tier_id,
                now_iso=now_iso,
                ends_at_override=ends_at_override,
                starts_at_override=starts_at_override,
                notify_me_higher_tiers=notify_active,
            ),
            "original_price_inr": mrp_inr,
            "currency": currency,
            "deliverables": list(pack.get("deliverables") or []),
        }

    # 2. Annual Planners from packs.json
    try:
        from app.config.planner_2027_pricing import is_planner_2027_live
        planner_live = is_planner_2027_live()
    except Exception:
        planner_live = False

    for pl_id, pl in (packs_data.get("annual_planners") or {}).items():
        pl_waitlist = bool(pl.get("waitlist_only")) or pl.get("price_inr") is None or (not planner_live)
        pl_inr = None if pl_waitlist else int(pl["price_inr"])
        pl_paise = None if pl_waitlist else int(pl.get("amount_paise") or (pl_inr * 100))
        skus[pl_id] = {
            "sku_id": pl_id,
            "family": "annual_planner",
            "name": pl["name"],
            "descriptor": pl.get("descriptor") or pl.get("display_name") or pl["name"],
            "display_name": pl.get("display_name", pl["name"]),
            "pages": int(pl.get("pages") or 24),
            "waitlist_only": pl_waitlist,
            "status": "waitlist" if pl_waitlist else "active",
            "display_price_label": (pl.get("display_price_label") or wl_label) if pl_waitlist else f"₹{pl_inr:,}",
            "waitlist_caption": wl_caption if pl_waitlist else "",
            "amount_inr": pl_inr,
            "amount_paise": pl_paise,
            "original_price_inr": pl.get("list_price_inr") if not pl_waitlist else None,
            "currency": str(pl.get("currency") or currency),
            "deliverables": list(pl.get("deliverables") or []),
        }

    # 3. Bundles from packs.json
    for b_id, bundle in (packs_data.get("bundles") or {}).items():
        b_inr = bundle.get("price_inr")
        b_paise = bundle.get("amount_paise")
        b_waitlist = bool(bundle.get("waitlist_only", b_inr is None or bundle.get("status") != "active"))
        skus[b_id] = {
            "sku_id": b_id,
            "family": "bundle",
            "name": bundle["name"],
            "descriptor": bundle.get("display_name", bundle["name"]),
            "display_name": bundle.get("display_name", bundle["name"]),
            "waitlist_only": b_waitlist,
            "status": str(bundle.get("status", "coming_soon")),
            "display_price_label": bundle.get("display_price_label") or (wl_label if b_inr is None else f"₹{int(b_inr):,}"),
            "amount_inr": int(b_inr) if b_inr is not None else None,
            "amount_paise": int(b_paise) if b_paise is not None else None,
            "original_price_inr": int(b_inr) if b_inr is not None else None,
            "currency": currency,
            "deliverables": list(bundle.get("deliverables") or []),
        }

    # 4. Charm AI packs from packs.json
    for p_id, pack in (packs_data.get("charm_ai") or {}).items():
        p_inr = pack.get("price_inr")
        p_paise = pack.get("amount_paise")
        q_count = int(pack.get("questions_count") or 0)
        skus[p_id] = {
            "sku_id": p_id,
            "family": "charm_ai",
            "name": pack["name"],
            "descriptor": pack.get("descriptor", ""),
            "display_name": pack.get("display_name", pack["name"]),
            "questions_count": q_count,
            "has_remedies": bool(p_id != "charm_free" and q_count > 3),
            "waitlist_only": False,
            "status": str(pack.get("status", "inactive")),
            "amount_inr": int(p_inr) if p_inr is not None else None,
            "amount_paise": int(p_paise) if p_paise is not None else None,
            "original_price_inr": int(p_inr) if p_inr is not None else None,
            "currency": currency,
            "deliverables": list(pack.get("deliverables") or []),
        }

    return skus


def build_plans_from_packs_json(
    now_iso: Optional[str] = None,
    ends_at_override: Optional[str] = None,
    starts_at_override: Optional[str] = None,
    notify_me_higher_tiers: Optional[bool] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Constructs `app.api.payments.PLANS` strictly from `app/config/packs.json`
    (via `get_all_product_skus`) with zero second price table.
    """
    skus = get_all_product_skus(
        now_iso=now_iso,
        ends_at_override=ends_at_override,
        starts_at_override=starts_at_override,
        notify_me_higher_tiers=notify_me_higher_tiers,
    )
    plans: Dict[str, Dict[str, Any]] = {}
    category_map = {
        "standalone_report": "report",
        "annual_planner": "annual_planner",
        "bundle": "bundle",
        "charm_ai": "charm_ai",
    }
    for sku_id, sku in skus.items():
        family = sku.get("family", "")
        pages = sku.get("pages")
        q_count = int(sku.get("questions_count") or 0)
        if pages:
            period = f"{pages}-Page Personalized PDF"
        elif family == "charm_ai":
            period = f"{q_count} Questions"
        else:
            period = sku.get("display_name", sku["name"])

        plans[sku_id] = {
            "pack_id": sku_id,
            "name": sku["name"],
            "display_name": sku.get("display_name", sku["name"]),
            "amount_inr": sku.get("amount_inr"),
            "original_price_inr": sku.get("original_price_inr"),
            "amount_paise": sku.get("amount_paise"),
            "struck_mrp_inr": sku.get("struck_mrp_inr"),
            "status": sku.get("status", "inactive"),
            "waitlist_only": bool(sku.get("waitlist_only", False)),
            "display_price_label": sku.get("display_price_label"),
            "period": period,
            "questions_count": q_count,
            "has_remedies": bool(
                sku.get("has_remedies", family in ("standalone_report", "annual_planner", "bundle"))
            ),
            "category": category_map.get(family, family),
            "description": sku.get("descriptor", ""),
            "features": list(sku.get("deliverables") or []),
            "deliverables": list(sku.get("deliverables") or []),
        }
    return plans


def resolve_sku_price(
    sku_or_plan_id: str,
    now_iso: Optional[str] = None,
    ends_at_override: Optional[str] = None,
    starts_at_override: Optional[str] = None,
    notify_me_higher_tiers: Optional[bool] = None,
) -> Optional[Dict[str, Any]]:
    """
    Resolves the authoritative server SKU record strictly from `packs.json`.
    """
    if not sku_or_plan_id or not isinstance(sku_or_plan_id, str):
        return None
    clean_id = sku_or_plan_id.lower().strip()
    skus = get_all_product_skus(
        now_iso=now_iso,
        ends_at_override=ends_at_override,
        starts_at_override=starts_at_override,
        notify_me_higher_tiers=notify_me_higher_tiers,
    )
    if clean_id in skus:
        return skus[clean_id]

    alias_map = {
        "basic": "report_basic",
        "advanced": "report_advanced",
        "premium": "report_premium",
        "planner-2027": "planner_2027",
        "year_2027": "planner_2027",
        "2027_planner": "planner_2027",
    }
    target_sku = alias_map.get(clean_id)
    if target_sku and target_sku in skus:
        return skus[target_sku]

    return None


def recommend_ladder_tier(
    gap_count: Optional[int] = None,
    notify_me_higher_tiers: Optional[bool] = None,
    tapped_context: Optional[str] = None,
) -> str:
    """Combined deterministic 3-card report ladder recommendation rule."""
    notify_active = (
        is_notify_me_higher_tiers_enabled()
        if notify_me_higher_tiers is None
        else bool(notify_me_higher_tiers)
    )
    if notify_active:
        return "report_basic"

    if tapped_context:
        ctx = str(tapped_context).strip().lower()
        if ctx in ("veiled", "missing", "every"):
            return "report_premium"
        if ctx in ("glowing", "present", "radiant"):
            return "report_advanced"
        if ctx in ("alignment", "align", "plane"):
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
    """Exports full public catalog derived from `packs.json` for API consumers."""
    packs_data = load_packs_json()
    notify_active = is_notify_me_higher_tiers_enabled()
    launch_offer = resolve_launch_offer_state()
    report_tiers = _build_report_tiers(packs_data)
    bundles = _build_bundles(packs_data)
    charm_ai = _build_charm_ai_packs(packs_data)
    annual_planners = _build_annual_planners(packs_data)

    public_tiers: Dict[str, Dict[str, Any]] = {}
    for tid, tval in report_tiers.items():
        if tval.get("waitlist_only") or tval.get("price_inr") is None or (notify_active and tid in ("advanced", "premium")):
            t_copy = dict(tval)
            t_copy["waitlist_only"] = True
            t_copy["status_label"] = WAITLIST_DISPLAY_LABEL
            t_copy["price_inr"] = None
            t_copy["amount_paise"] = None
            t_copy["mrp_inr"] = None
            t_copy["mrp_paise"] = None
            public_tiers[tid] = t_copy
        else:
            public_tiers[tid] = dict(tval)

    catalog = {
        "version": packs_data.get("version", "2.2.0"),
        "currency": str(packs_data.get("currency", CURRENCY)),
        "ladder_order": list(packs_data.get("ladder_order", LADDER_ORDER)),
        "feature_flags": {
            "notify_me_higher_tiers": notify_active,
            "notify_me_tiers": list(
                (packs_data.get("feature_flags") or {}).get(
                    "notify_me_tiers", ["report_advanced", "report_premium", "planner_2027"]
                )
            ),
            "waitlist_display_label": WAITLIST_DISPLAY_LABEL,
            "waitlist_launch_caption": WAITLIST_LAUNCH_CAPTION,
        },
        "launch_offer": launch_offer,
        "ladder_recommendation_rule": {
            "when_notify_me_true": "report_basic",
            "when_notify_me_false": {
                "tapped_veiled": "report_premium",
                "tapped_glowing": "report_advanced",
                "tapped_alignment": "report_basic",
                "0_to_2_gaps": "report_basic",
                "3_to_5_gaps": "report_advanced",
                "6_to_9_gaps": "report_premium",
                "unknown_gaps_default": "report_advanced",
            },
            "default_recommended_tier": recommend_ladder_tier(None, notify_active),
        },
        "report_tiers": public_tiers,
        "supported_topics": SUPPORTED_REPORT_TOPICS,
        "bundles": bundles,
        "charm_ai": charm_ai,
        "annual_planners": annual_planners,
        "consultation": CONSULTATION_PACKS,
        "all_skus": get_all_product_skus(notify_me_higher_tiers=notify_active),
    }
    return json.dumps(catalog, indent=2)
