"""
NUMEROS VISION — ADVANCED MARKETING FUNNEL & CONVERSION FRAMEWORK (v1.5.0)
Brand Tagline: ANVEIL EVERY CHARM

PURPOSE:
1. Reusable Seven-Stage Customer Journey Engine:
   Awareness -> Interest -> Consideration -> Conversion -> Retention -> Loyalty -> Repeat Conversion
2. Brand-Led Curiosity Hook Architecture:
   - Curiosity Hook: Positive, open-ended question inviting discovery.
   - Value Bridge: What the user can explore in the free experience vs. full report.
   - Action CTA: Concise, specific action button (no generic/vague labels).
3. Deterministic Digit-Root Pricing Policy:
   - Enforces digital root of whole-rupee prices in allowed set {1, 3, 5, 6}.
   - Validates offer_price < reference_price for genuine savings.
4. Entitlement & Access Decision Engine:
   - Prevents duplicate purchases of already owned reports.
   - Manages one-time purchase vs. recurring subscription lifetimes.
5. Marketing Opt-Out Precedence:
   - If user opted out, marketing prompts are suppressed in favor of clean product action.
6. Privacy-Minimised Funnel Event Telemetry:
   - Logs non-PII funnel state transitions to data/funnel_events.jsonl.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, Any, List, Optional, FrozenSet, Set
import os
import json
import time

# ── 1. DIGIT-ROOT PRICING POLICY ─────────────────────────────────────────────

DEFAULT_ALLOWED_ROOTS: FrozenSet[int] = frozenset({1, 3, 5, 6})

@dataclass(frozen=True)
class PricePolicy:
    version: str = "nv-price-policy-v1.5"
    allowed_digit_roots: FrozenSet[int] = DEFAULT_ALLOWED_ROOTS
    require_offer_below_reference: bool = True


def digit_root(amount_major_units: int) -> int:
    """
    Computes the repeated single-digit sum (digital root) of a positive integer.
    Example: 199 -> 1+9+9=19 -> 1+9=10 -> 1+0 = 1
    """
    if not isinstance(amount_major_units, int) or isinstance(amount_major_units, bool):
        raise ValueError("Price must be an integer in configured major units (e.g. INR whole rupees)")
    if amount_major_units <= 0:
        raise ValueError("Price must be a positive integer")
    
    val = amount_major_units
    while val >= 10:
        val = sum(int(ch) for ch in str(val))
    return val


def validate_single_price(amount: int, policy: Optional[PricePolicy] = None) -> Dict[str, Any]:
    """Validates if a single major-unit price conforms to the approved digit root set."""
    p = policy or PricePolicy()
    root = digit_root(amount)
    is_valid = root in p.allowed_digit_roots
    return {
        "amount": amount,
        "digital_root": root,
        "valid": is_valid,
        "policy_version": p.version,
        "allowed_roots": sorted(list(p.allowed_digit_roots))
    }


def validate_price_pair(reference: int, offer: int, policy: Optional[PricePolicy] = None) -> Dict[str, Any]:
    """
    Validates reference and offer price pair:
    - Both roots must belong to the allowed root set.
    - Offer price must be strictly less than reference price if require_offer_below_reference is True.
    """
    p = policy or PricePolicy()
    errors = []
    
    ref_root = digit_root(reference)
    off_root = digit_root(offer)
    
    if ref_root not in p.allowed_digit_roots:
        errors.append("REFERENCE_PRICE_ROOT_NOT_ALLOWED")
    if off_root not in p.allowed_digit_roots:
        errors.append("OFFER_PRICE_ROOT_NOT_ALLOWED")
    if p.require_offer_below_reference and offer >= reference:
        errors.append("OFFER_NOT_BELOW_REFERENCE")
        
    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "reference": reference,
        "offer": offer,
        "reference_root": ref_root,
        "offer_root": off_root,
        "savings_inr": reference - offer if offer < reference else 0,
        "discount_percent": round(((reference - offer) / reference) * 100) if offer < reference else 0,
        "policy_version": p.version
    }


# ── 2. SEVEN-STAGE FUNNEL & JOURNEY STATE ENUMS ──────────────────────────────

class FunnelStage(str, Enum):
    AWARENESS = "AWARENESS"
    INTEREST = "INTEREST"
    CONSIDERATION = "CONSIDERATION"
    CONVERSION = "CONVERSION"
    RETENTION = "RETENTION"
    LOYALTY = "LOYALTY"
    REPEAT_CONVERSION = "REPEAT_CONVERSION"


class JourneyState(str, Enum):
    DISCOVERY = "DISCOVERY"
    CALCULATION_STARTED = "CALCULATION_STARTED"
    FREE_RESULT_READY = "FREE_RESULT_READY"
    OFFER_ELIGIBLE = "OFFER_ELIGIBLE"
    PRODUCT_DETAILS_VIEWED = "PRODUCT_DETAILS_VIEWED"
    CHECKOUT_STARTED = "CHECKOUT_STARTED"
    PAYMENT_CONFIRMED = "PAYMENT_CONFIRMED"
    FULFILMENT_PENDING = "FULFILMENT_PENDING"
    FULFILLED = "FULFILLED"
    POST_PURCHASE_ENGAGEMENT = "POST_PURCHASE_ENGAGEMENT"
    LOYALTY_ELIGIBLE = "LOYALTY_ELIGIBLE"
    REPEAT_OFFER_ELIGIBLE = "REPEAT_OFFER_ELIGIBLE"
    OPTED_OUT = "OPTED_OUT"


class EntitlementDecision(str, Enum):
    ALLOW_PURCHASED = "ALLOW_PURCHASED"
    ALLOW_SUBSCRIPTION = "ALLOW_SUBSCRIPTION"
    ALLOW_FREE_TIER = "ALLOW_FREE_TIER"
    DENY_NO_ENTITLEMENT = "DENY_NO_ENTITLEMENT"
    DENY_QUOTA_EXHAUSTED = "DENY_QUOTA_EXHAUSTED"
    DENY_EXPIRED = "DENY_EXPIRED"
    DENY_RESOURCE_NOT_OWNED = "DENY_RESOURCE_NOT_OWNED"


@dataclass(frozen=True)
class Entitlement:
    feature_id: str
    source_type: str            # "PURCHASE", "SUBSCRIPTION", "FREE_TIER"
    status: str                 # "ACTIVE", "EXPIRED", "REVOKED"
    starts_at: datetime
    expires_at: Optional[datetime] = None
    quota_remaining: Optional[int] = None


def entitlement_is_active(e: Entitlement, now: datetime) -> bool:
    if e.status != "ACTIVE" or e.starts_at > now:
        return False
    if e.expires_at is not None and now >= e.expires_at:
        return False
    if e.quota_remaining is not None and e.quota_remaining <= 0:
        return False
    return True


def decide_feature_access(
    feature_id: str,
    entitlements: List[Entitlement],
    now: datetime,
) -> EntitlementDecision:
    """Evaluates whether user has active entitlement for a feature/report."""
    matching = [e for e in entitlements if e.feature_id == feature_id]
    active = [e for e in matching if entitlement_is_active(e, now)]

    if any(e.source_type == "PURCHASE" for e in active):
        return EntitlementDecision.ALLOW_PURCHASED
    if any(e.source_type == "SUBSCRIPTION" for e in active):
        return EntitlementDecision.ALLOW_SUBSCRIPTION
    if any(e.source_type == "FREE_TIER" for e in active):
        return EntitlementDecision.ALLOW_FREE_TIER
    if any(e.quota_remaining is not None and e.quota_remaining <= 0 for e in matching):
        return EntitlementDecision.DENY_QUOTA_EXHAUSTED
    if matching:
        return EntitlementDecision.DENY_EXPIRED
    return EntitlementDecision.DENY_NO_ENTITLEMENT


# ── 3. PRODUCT CATALOG WITH FUNNEL HOOKS & DELIVERABLES ───────────────────────

PRODUCT_FUNNEL_CATALOG: Dict[str, Dict[str, Any]] = {
    "birth_number": {
        "id": "birth_number",
        "name": "Birth Number Analysis",
        "category": "calculator",
        "awareness_hook": "Discover the meaning of your birth number.",
        "curiosity_hook": "Want to Explore Your Number Further?",
        "value_bridge": "Your free calculation gives you your core Driver frequency. Explore the full blueprint to see planetary harmonics, career resonance, and personal year cycles.",
        "free_result_scope": "Basic Driver (Mulank) calculation, ruling planet, and primary attributes.",
        "primary_cta": "View Basic Report",
        "secondary_cta": "Compare Report Packages",
        "tertiary_link": "Preview a Sample Report",
        "recommended_plan": "report_essential",
        "plan_name": "Basic Numerology Report",
        "price_inr": 199,
        "original_price_inr": 399,
        "deliverables": [
            "12-15 Page Executive PDF Report",
            "Mulank (Driver) & Bhagyank (Conductor) Blueprint",
            "Lo Shu 3x3 Grid & Missing Numbers audit",
            "1-Year Personal Timing Snapshot",
            "Primary Gemstone & Color Harmony Guide"
        ]
    },
    "life_path": {
        "id": "life_path",
        "name": "Life Path Calculator",
        "category": "calculator",
        "awareness_hook": "Explore the number connected with your life path.",
        "curiosity_hook": "Explore the Wider Life Path Picture",
        "value_bridge": "Your free result reduces your birth epoch to your core Life Path. Explore the next layer to see your 5-Year Numerology Dasha Dasha timeline and cross-verified career transits.",
        "free_result_scope": "Life Path Number, planetary ruler, Driver-Conductor polarity status.",
        "primary_cta": "Explore Advanced Analysis",
        "secondary_cta": "Preview the Report",
        "tertiary_link": "View Deliverables & Terms",
        "recommended_plan": "report_master",
        "plan_name": "Advanced Numerology Report",
        "price_inr": 510,
        "original_price_inr": 999,
        "deliverables": [
            "35-40 Page Master Synthesis Dossier",
            "Full Name vs Calling Name Chaldean audit",
            "BNN 1-5-9 Trines & 2-12 Wealth Vector Analysis",
            "5-Year 5-Tier Numerology Dasha Dasha Timeline",
            "Historical Milestone Accuracy Calibration",
            "7-Layer Safe Remedies (Mantra, Daan, Crystal, Lifestyle)",
            "Mobile Number & Digital Touchpoint Audit"
        ]
    },
    "name_numerology": {
        "id": "name_numerology",
        "name": "Name Numerology",
        "category": "calculator",
        "awareness_hook": "What does your name’s number reveal?",
        "curiosity_hook": "Review the Additional Number Breakdown",
        "value_bridge": "Your free result shows your single-digit expression number. The complete analysis evaluates full vs calling name harmony, compound karmic debt, and spelling balancing.",
        "free_result_scope": "Single-digit name sum and primary planetary association.",
        "primary_cta": "View Basic Report",
        "secondary_cta": "Compare Report Packages",
        "tertiary_link": "How Name Balancing Works",
        "recommended_plan": "report_essential",
        "plan_name": "Basic Numerology Report",
        "price_inr": 199,
        "original_price_inr": 399,
        "deliverables": [
            "Full Name Vibration vs Driver-Conductor Compatibility",
            "Compound Number karmic debt assessment (13, 14, 16, 19, 28)",
            "3 Harmonized spelling calibration proposals",
            "Executive PDF deliverable with official brand seal"
        ]
    },
    "chaldean_name": {
        "id": "chaldean_name",
        "name": "Chaldean Name Numerology",
        "category": "calculator",
        "awareness_hook": "Explore your name through Chaldean numerology.",
        "curiosity_hook": "Discover the Ancient Sound Frequencies",
        "value_bridge": "Chaldean numerology focuses on occult compound vibrations. Explore how your compound number influences unseen career momentum and financial retention.",
        "free_result_scope": "Chaldean alphabet matrix calculation and primary compound sum.",
        "primary_cta": "Explore Advanced Analysis",
        "secondary_cta": "Compare Report Packages",
        "tertiary_link": "View Chaldean Methodology",
        "recommended_plan": "report_master",
        "plan_name": "Advanced Numerology Report",
        "price_inr": 510,
        "original_price_inr": 999,
        "deliverables": [
            "Chaldean Sound Frequency Analysis across all syllables",
            "Compound number occult symbolism & planetary ruler",
            "5-Year timing matrix calibrated with your calling vibration",
            "Consecrated sound frequency activation guide"
        ]
    },
    "lo_shu_grid": {
        "id": "lo_shu_grid",
        "name": "Lo Shu 3x3 Grid",
        "category": "calculator",
        "awareness_hook": "Explore the pattern in your personal grid.",
        "curiosity_hook": "Harmonize Incomplete Energy Planes",
        "value_bridge": "Your free grid shows existing and missing numbers. The master report maps incomplete planes (Golden Prosperity 4-5-6, Will 9-5-1) and prescribes bespoke planetary remedies.",
        "free_result_scope": "3x3 Lo Shu natal grid distribution and missing number indicators.",
        "primary_cta": "Explore Advanced Analysis",
        "secondary_cta": "Compare Report Packages",
        "tertiary_link": "Explore Plane Meanings",
        "recommended_plan": "report_master",
        "plan_name": "Advanced Numerology Report",
        "price_inr": 510,
        "original_price_inr": 999,
        "deliverables": [
            "8 Planes of Lo Shu comprehensive audit",
            "Golden Prosperity Plane (4-5-6) leakage remediation",
            "Central Brahmasthan Anchor Number 5 grounding protocol",
            "Consecrated crystal, metal, and directional placement blueprint"
        ]
    },
    "mobile_numerology": {
        "id": "mobile_numerology",
        "name": "Mobile Number Numerology",
        "category": "calculator",
        "awareness_hook": "Explore your number audit.",
        "curiosity_hook": "Uncover Paired Digit Harmonics",
        "value_bridge": "Every mobile contact number emits repetitive frequencies. The full report audits all 9 adjacent pairs and reveals whether your SIM aligns with business prosperity.",
        "free_result_scope": "Privacy-masked single-digit root and basic frequency summary.",
        "primary_cta": "Explore Advanced Analysis",
        "secondary_cta": "View My Report Options",
        "tertiary_link": "Privacy & Data Masking Policy",
        "recommended_plan": "report_master",
        "plan_name": "Advanced Numerology Report",
        "price_inr": 510,
        "original_price_inr": 999,
        "deliverables": [
            "Complete 9-pair frequency audit (anti-pairs like 2-8, 4-8, 1-8)",
            "Commercial & wealth calling vibration assessment",
            "Auspicious digit replacement recommendations",
            "Zero PII retention policy guaranteed"
        ]
    },
    "personal_year": {
        "id": "personal_year",
        "name": "Personal Year & Transit Engine",
        "category": "calculator",
        "awareness_hook": "Explore your personal-year number.",
        "curiosity_hook": "Map Your 12-Month Tactical Windows",
        "value_bridge": "Knowing your Personal Year number is step one. The full forecast breaks down month-by-month high-probability decision dates for career changes, investments, and contracts.",
        "free_result_scope": "Current calendar year personal number and overall theme.",
        "primary_cta": "View Basic Report",
        "secondary_cta": "Compare Report Packages",
        "tertiary_link": "Review Forecast Methodology",
        "recommended_plan": "report_essential",
        "plan_name": "Basic Numerology Report",
        "price_inr": 199,
        "original_price_inr": 399,
        "deliverables": [
            "12-Month personal timing calendar",
            "Gochar (planetary transit) favorable action windows",
            "Quarterly strategic review recommendations",
            "Auspicious Muhurat dates for major milestones"
        ]
    },
    "compatibility": {
        "id": "compatibility",
        "name": "Numerology Compatibility",
        "category": "calculator",
        "awareness_hook": "Explore your numerology compatibility.",
        "curiosity_hook": "Deepen Your Understanding of Relational Synergy",
        "value_bridge": "Our free tool assesses Driver-Conductor natural harmony. The full relationship dossier explores karmic bonds, 36-point Guna Milan cross-checks, and constructive communication remedies.",
        "free_result_scope": "Basic percentage alignment and friendly/neutral/friction status.",
        "primary_cta": "Explore Advanced Analysis",
        "secondary_cta": "Compare Report Packages",
        "tertiary_link": "View Synastry Principles",
        "recommended_plan": "report_master",
        "plan_name": "Advanced Numerology Report",
        "price_inr": 510,
        "original_price_inr": 999,
        "deliverables": [
            "Dual-Chart complete cross-synastry matrix",
            "Elemental compatibility (Fire, Water, Earth, Air)",
            "Conflict de-escalation timing windows",
            "Combined home energy and sacred geometry alignment"
        ]
    },
    "business_direction": {
        "id": "business_direction",
        "name": "Business Direction & Entity Matrix",
        "category": "calculator",
        "awareness_hook": "Explore your business alignment.",
        "curiosity_hook": "Align Your Corporate Brand with Market Timing",
        "value_bridge": "A business entity holds its own vibrational signature. Our corporate dossier validates trade name vibrations, founder synastry, and incorporation Muhurat windows.",
        "free_result_scope": "Core archetype category and basic planetary alignment.",
        "primary_cta": "Explore My Business Alignment Report",
        "secondary_cta": "Compare Business Report Options",
        "tertiary_link": "Corporate Confidentiality Terms",
        "recommended_plan": "advisory_business_name",
        "plan_name": "Commercial Entity & Brand Matrix",
        "price_inr": 5999,
        "original_price_inr": 14000,
        "deliverables": [
            "Corporate Legal Name & Trade Name vibration audit",
            "Founder & Co-Founder Synergy Compatibility Matrix",
            "Incorporation & Launch Muhurat (3 high-probability dates)",
            "Bank Account & Invoicing numerical vibration audit"
        ]
    },
    "logo_studio": {
        "id": "logo_studio",
        "name": "Logo Studio & Brand Geometry",
        "category": "calculator",
        "awareness_hook": "Explore the numerology and design of your brand.",
        "curiosity_hook": "Harmonize Sacred Geometry & Upward Trajectory",
        "value_bridge": "Great logos embody sacred proportions and elemental balance. Our full studio delivers OCR-validated wordmarks, 5-element color balance, and vector deliverables.",
        "free_result_scope": "Color contrast check and basic element distribution.",
        "primary_cta": "Explore My Full Logo Audit",
        "secondary_cta": "Review the Design Report",
        "tertiary_link": "Vector Output Specifications",
        "recommended_plan": "advisory_brand_logo",
        "plan_name": "Brand Logo Balancing & Sacred Geometry Harmony",
        "price_inr": 9996,
        "original_price_inr": 15000,
        "deliverables": [
            "5-Element Geometric Vector Energy Audit",
            "Planetary Color Vector Harmonization",
            "Upward-right growth trajectory vector verification",
            "3 Finalized Balanced Vector Logo Concepts (SVG / PNG)"
        ]
    },
    "charm_ai": {
        "id": "charm_ai",
        "name": "Charm AI",
        "category": "ai_oracle",
        "awareness_hook": "Ask a question. Explore a new perspective.",
        "curiosity_hook": "Engage in Conversational Cosmic Counsel",
        "value_bridge": "Charm AI answers with zero-hallucination classical numerology and astrology synthesis. Recharge question credits or upgrade to unlimited synthesis dossiers.",
        "free_result_scope": "Instant answers to foundational questions using classical ephemeris.",
        "primary_cta": "Explore a Deeper Reading",
        "secondary_cta": "Compare Charm AI Plans",
        "tertiary_link": "Review Classical Sources",
        "recommended_plan": "ai_growth_15q",
        "plan_name": "Charm AI — Growth Pack (15 Questions + Remedies)",
        "price_inr": 199,
        "original_price_inr": 399,
        "deliverables": [
            "15 In-depth Question Predictions",
            "Customized 7-Layer Safe Remedies for each query",
            "Auspicious timing windows & lucky dates",
            "Zero hallucination guarantee bound to classical texts"
        ]
    },
    "reports_catalogue": {
        "id": "reports_catalogue",
        "name": "Numeros Vision Reports Catalogue",
        "category": "reports",
        "awareness_hook": "Choose the insight you want to explore.",
        "curiosity_hook": "Explore Verified Cosmic Blueprint Dossiers",
        "value_bridge": "Select from executive blueprints, master dual-system synthesis, or sovereign roadmaps tailored to your career and life pivots.",
        "free_result_scope": "Sample preview pages and methodology breakdowns.",
        "primary_cta": "Choose My Report",
        "secondary_cta": "Compare Report Packages",
        "tertiary_link": "View Sample Dossier",
        "recommended_plan": "report_master",
        "plan_name": "Advanced Numerology Report",
        "price_inr": 510,
        "original_price_inr": 999,
        "deliverables": [
            "35+ Page Comprehensive Synthesis Dossier",
            "Instant PDF generation and secure download",
            "Cross-verified planetary dasha and transit alignment"
        ]
    },
    "consultation": {
        "id": "consultation",
        "name": "1-on-1 Astrological & Numerological Consultation",
        "category": "consultation",
        "awareness_hook": "Explore the consultation that fits your goal.",
        "curiosity_hook": "Personalized Counsel with Senior Numerologist",
        "value_bridge": "Gain private, in-depth consultation covering career transitions, partnership synastry, and custom consecrated remedial prescriptions.",
        "free_result_scope": "Practitioner credentials, session format, and preparation checklist.",
        "primary_cta": "Review Session Details",
        "secondary_cta": "Book a Consultation",
        "tertiary_link": "Cancellation & Rescheduling Policy",
        "recommended_plan": "complete_report",
        "plan_name": "Premium Numerology Report",
        "price_inr": 1050,
        "original_price_inr": 1299,
        "deliverables": [
            "Complete Personal Destiny Blueprint Report",
            "Comprehensive Multi-Layer Remedies & Gemstone Prescription",
            "Annual Timing Forecast & Life Roadmap",
            "Unlimited Question Predictions with Remedies"
        ]
    },

    # ── 18 SCREENSHOT-BASED INDIVIDUAL REPORTS ─────────────────────────────────
    # Group: Love and Marriage (Harmonic Personality 6 · Venusian Harmony)
    "report_love_style": {
        "id": "report_love_style",
        "name": "Love Style & Romance Profile",
        "category": "Love and Marriage",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "awareness_hook": "Discover how your planetary archetype expresses romantic intimacy.",
        "curiosity_hook": "Ready to Explore Your Emotional Rhythm?",
        "value_bridge": "Unveil Venusian harmonics, relational triggers, and deep affection patterns.",
        "free_result_scope": "Core Venusian attraction indicator and primary romance style.",
        "primary_cta": "Get Love Style Report",
        "secondary_cta": "Compare Love Reports",
        "tertiary_link": "View Romantic Archetypes",
        "recommended_plan": "report_love_style",
        "plan_name": "Love Style & Romance Profile",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "Venusian Expression & Romance Archetype",
            "Emotional Communication Style & Love Languages",
            "Vulnerability Blindspots & Conflict Triggers",
            "Practical Attunement & Heart-Chakra Guidance"
        ]
    },
    "report_marriage": {
        "id": "report_marriage",
        "name": "Marriage Timing & Union Blueprint",
        "category": "Love and Marriage",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "awareness_hook": "Explore auspicious windows for sacred partnership and marriage commitment.",
        "curiosity_hook": "When Does the Cosmic Alignment Favour Union?",
        "value_bridge": "Examine 7th house lord transits and Numerology Dasha timing windows for long-term commitment.",
        "free_result_scope": "Current Dasha climate and general marriage window indicators.",
        "primary_cta": "Explore Marriage Timing Report",
        "secondary_cta": "Preview Marriage Report",
        "tertiary_link": "Timing Methodology",
        "recommended_plan": "report_marriage",
        "plan_name": "Marriage Timing & Union Blueprint",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "Optimal Union Muhurat & Dasha Alignment Windows",
            "7th House & Venus/Jupiter Planetary Significations",
            "Key Milestones Leading to Sacred Union",
            "Remedial Harmonization for Delayed Unions"
        ]
    },
    "report_ideal_partner": {
        "id": "report_ideal_partner",
        "name": "Ideal Partner Profile & Compatibility Matrix",
        "category": "Love and Marriage",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "awareness_hook": "Identify the psychological archetype and vibration of your ideal companion.",
        "curiosity_hook": "Who Truly Matches Your Core Vibration?",
        "value_bridge": "Map soulmate vibrations, Driver-Conductor polarities, and shared spiritual values.",
        "free_result_scope": "Compatible driver roots and primary planetary affinities.",
        "primary_cta": "Get Ideal Partner Report",
        "secondary_cta": "Compare Compatibility Options",
        "tertiary_link": "Synastry Standards",
        "recommended_plan": "report_ideal_partner",
        "plan_name": "Ideal Partner Profile & Compatibility Matrix",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "Soulmate Vibration & Karaka Significations",
            "Complementary Number Profiles (Driver & Conductor)",
            "Key Interpersonal Dynamics & Shared Values",
            "Red Flag Frequencies & Alignment Guidance"
        ]
    },
    "report_love_or_arrange": {
        "id": "report_love_or_arrange",
        "name": "Love or Arrange Exploration Report",
        "category": "Love and Marriage",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "awareness_hook": "Evaluate classical indicators of self-chosen love vs traditional arranged marriage.",
        "curiosity_hook": "Which Path Resonates with Your Chart?",
        "value_bridge": "Compare 5th vs 7th/9th house influences, family blessings, and cultural alignment.",
        "free_result_scope": "5th vs 7th house preliminary planetary balance.",
        "primary_cta": "Explore Marriage Path Report",
        "secondary_cta": "Review Path Indicators",
        "tertiary_link": "Classical House Influences",
        "recommended_plan": "report_love_or_arrange",
        "plan_name": "Love or Arrange Exploration Report",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "5th vs 7th/9th House Influence Comparison",
            "Planetary Indicators for Self-Chosen vs Family Alliances",
            "Family Acceptance Potential & Parental Blessing Indicators",
            "Diplomatic Guidance for Navigating Marital Choices"
        ]
    },
    "report_spouse": {
        "id": "report_spouse",
        "name": "Spouse Personality & Life Alignment Report",
        "category": "Love and Marriage",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "awareness_hook": "Discover your future partner's temperament, career inclination, and shared destiny.",
        "curiosity_hook": "What Traits Will Your Partner Bring into Your Life?",
        "value_bridge": "Detailed portrait of spouse archetype, post-marriage fortune, and mutual growth.",
        "free_result_scope": "7th house planetary imprint and basic spousal personality indicators.",
        "primary_cta": "Get Spouse Profile Report",
        "secondary_cta": "Compare Family Reports",
        "tertiary_link": "Spouse Archetypes",
        "recommended_plan": "report_spouse",
        "plan_name": "Spouse Personality & Life Alignment Report",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "Spouse Temperament & Behavioral Archetype",
            "Likely Professional Domain & Social Standing",
            "Post-Marriage Fortune & Wealth Activation",
            "Harmonious Daily Habits & Relationship Care"
        ]
    },
    "report_in_laws": {
        "id": "report_in_laws",
        "name": "In-Laws & Family Harmony Report",
        "category": "Love and Marriage",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "awareness_hook": "Navigate relationships with extended family and domestic elders gracefully.",
        "curiosity_hook": "How Can You Cultivate Deep Extended Family Peace?",
        "value_bridge": "Understand in-law astrological influences, friction de-escalation, and Vastu alignment.",
        "free_result_scope": "Domestic stability indicator and general extended family alignment.",
        "primary_cta": "Get Family Harmony Report",
        "secondary_cta": "Preview In-Laws Report",
        "tertiary_link": "Vastu Harmonization",
        "recommended_plan": "report_in_laws",
        "plan_name": "In-Laws & Family Harmony Report",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "In-Law Astrological House Influences (9th/10th from 7th)",
            "Potential Communication Friction Points & Solutions",
            "Vedic Vastu Directions for Family Harmony",
            "Boundary Setting & Diplomatic Grace Protocols"
        ]
    },

    # Group: Money
    "report_billionaire_potential": {
        "id": "report_billionaire_potential",
        "name": "Billionaire Potential & Wealth Blueprint",
        "category": "Money",
        "category_group": "Money",
        "pricing_personality": 1,
        "awareness_hook": "Explore multi-generational wealth architecture and sovereign Dhana Yoga indicators.",
        "curiosity_hook": "Do You Carry the Signature of Outsized Financial Scale?",
        "value_bridge": "Audit Dhana/Lakshmi Yogas, Lo Shu Golden Prosperity Plane 4-5-6, and capital windows.",
        "free_result_scope": "Presence of core prosperity digits in birth epoch.",
        "primary_cta": "Explore Sovereign Wealth Blueprint",
        "secondary_cta": "Explore Wealth Options",
        "tertiary_link": "Wealth Archetypes",
        "recommended_plan": "report_billionaire_potential",
        "plan_name": "Billionaire Potential & Wealth Blueprint",
        "price_inr": 1499,
        "original_price_inr": 1999,
        "deliverables": [
            "Dhana Yoga & Lakshmi Yoga Conjunction Audit",
            "Lo Shu Prosperity Plane (4-5-6) Golden Flow Evaluation",
            "High-Stakes Capital Deployment Windows",
            "Wealth Retention & Institutional Compounding Strategy"
        ]
    },
    "report_wealth": {
        "id": "report_wealth",
        "name": "Wealth & Abundance Report",
        "category": "Money",
        "category_group": "Money",
        "pricing_personality": 6,
        "awareness_hook": "Understand your cash flow cycles, financial retention, and earning potential.",
        "curiosity_hook": "Where Is Your Financial Flow Naturally Channelled?",
        "value_bridge": "Identify wealth leakage points, auspicious financial quarters, and steady growth habits.",
        "free_result_scope": "Basic earning frequency and financial stability indicator.",
        "primary_cta": "Get Wealth & Abundance Report",
        "secondary_cta": "Compare Money Reports",
        "tertiary_link": "Prosperity Matrix",
        "recommended_plan": "report_wealth",
        "plan_name": "Wealth & Abundance Report",
        "price_inr": 699,
        "original_price_inr": 1299,
        "deliverables": [
            "Personal Cashflow & Wealth Retention Ratio",
            "Favorable Quarters for Asset Purchases & Investments",
            "Identification of Hidden Financial Leakage Patterns",
            "Practical Prosperity Affirmations & Workspace Alignment"
        ]
    },

    # Group: Work
    "report_career": {
        "id": "report_career",
        "name": "Career Direction & Growth Blueprint",
        "category": "Work",
        "category_group": "Work",
        "pricing_personality": 1,
        "awareness_hook": "Clarify your optimal industry domain, leadership trajectory, and promotion timing.",
        "curiosity_hook": "Is Your Current Role Aligned with Your True Calling?",
        "value_bridge": "Synthesize 10th house indicators, Saturnian career axis, and Dasha promotion windows.",
        "free_result_scope": "Primary career planet and basic leadership tendencies.",
        "primary_cta": "Get Career Blueprint",
        "secondary_cta": "Preview Career Report",
        "tertiary_link": "Leadership Models",
        "recommended_plan": "report_career",
        "plan_name": "Career Direction & Growth Blueprint",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "Ideal Industry Sectors & Functional Roles",
            "Leadership Archetype & Management Style",
            "Upcoming Promotion & Elevation Windows",
            "Workplace Politics Mitigation Strategy"
        ]
    },
    "report_business": {
        "id": "report_business",
        "name": "Business & Venture Mastery Dossier",
        "category": "Work",
        "category_group": "Work",
        "pricing_personality": 1,
        "awareness_hook": "Assess entrepreneurial suitability, commercial market timing, and venture scalability.",
        "curiosity_hook": "Ready to Build Independent Commercial Autonomy?",
        "value_bridge": "Evaluate founder risk appetite, Mercury-Sun trade alignment, and incorporation Muhurat.",
        "free_result_scope": "Entrepreneurial inclination score and commercial resonance.",
        "primary_cta": "Explore Business Mastery Dossier",
        "secondary_cta": "Compare Work Options",
        "tertiary_link": "Venture Criteria",
        "recommended_plan": "report_business",
        "plan_name": "Business & Venture Mastery Dossier",
        "price_inr": 1499,
        "original_price_inr": 1999,
        "deliverables": [
            "Founder Archetype & Strategic Risk Tolerance",
            "Optimal Business Sectors & Market Niches",
            "High-Probability Launch & Expansion Windows",
            "Commercial Entity Acoustic Alignment Guidelines"
        ]
    },
    "report_job_or_business": {
        "id": "report_job_or_business",
        "name": "Job or Business Decision Compass",
        "category": "Work",
        "category_group": "Work",
        "pricing_personality": 5,
        "awareness_hook": "Resolve the crossroads: structured institutional employment vs independent enterprise.",
        "curiosity_hook": "Should You Climb the Corporate Ladder or Forge Your Own Path?",
        "value_bridge": "Compare 6th house (service) vs 7th/10th house (enterprise) planetary strengths.",
        "free_result_scope": "Service vs Enterprise relative polarity score.",
        "primary_cta": "Get Decision Compass Report",
        "secondary_cta": "Explore Career Crossroads",
        "tertiary_link": "Crossroads Methodology",
        "recommended_plan": "report_job_or_business",
        "plan_name": "Job or Business Decision Compass",
        "price_inr": 699,
        "original_price_inr": 1299,
        "deliverables": [
            "6th House (Service) vs 7th/10th House (Trade) Comparison",
            "Timing Matrix for Transitioning from Employment to Business",
            "Risk Mitigation Checklist for Career Pivots",
            "Hybrid Career Model Viability Assessment"
        ]
    },
    "report_govt_job": {
        "id": "report_govt_job",
        "name": "Government & Public Service Examination Report",
        "category": "Work",
        "category_group": "Work",
        "pricing_personality": 1,
        "awareness_hook": "Assess astrological suitability and competitive exam timing for public service.",
        "curiosity_hook": "Do You Have the Classical Markers for Administrative Authority?",
        "value_bridge": "Analyze Surya-Guru authority combinations, 10th house stability, and examination windows.",
        "free_result_scope": "Solar administrative resonance and authority indicator.",
        "primary_cta": "Get Govt Job Report",
        "secondary_cta": "Review Exam Windows",
        "tertiary_link": "Public Sector Archetypes",
        "recommended_plan": "report_govt_job",
        "plan_name": "Government & Public Service Examination Report",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "Sun & Mars Authority Combinations in Natal Chart",
            "Optimal Examination & Interview Windows",
            "Aptitude for Administrative vs Specialized Cadres",
            "Mental Focus & Competitive Stamina Rituals"
        ]
    },
    "report_first_job": {
        "id": "report_first_job",
        "name": "First Job & Campus Placement Navigator",
        "category": "Work",
        "category_group": "Work",
        "pricing_personality": 1,
        "awareness_hook": "Strategic guidance for early graduates navigating entry-level roles and internships.",
        "curiosity_hook": "How Can You Land the Perfect Launchpad Role?",
        "value_bridge": "Identify breakthrough internship months, interview strengths, and first-step confidence.",
        "free_result_scope": "Early career potential indicator and natural work aptitudes.",
        "primary_cta": "Get First Job Navigator",
        "secondary_cta": "Preview Placement Report",
        "tertiary_link": "Early Career Guide",
        "recommended_plan": "report_first_job",
        "plan_name": "First Job & Campus Placement Navigator",
        "price_inr": 199,
        "original_price_inr": 399,
        "deliverables": [
            "Entry-Level Career Sectors with Highest Growth Potential",
            "Key Interview Strengths & Natural Pitch Resonance",
            "Auspicious Resume Submission & Interview Days",
            "First 90 Days Workplace Integration Protocol"
        ]
    },
    "report_job_search": {
        "id": "report_job_search",
        "name": "Job Search & Interview Tactics Report",
        "category": "Work",
        "category_group": "Work",
        "pricing_personality": 5,
        "awareness_hook": "Actionable tactics for unblocking stalled job searches and acing interviews.",
        "curiosity_hook": "Why Is the Search Stalled, and When Will It Break Through?",
        "value_bridge": "Map Mercury communication clarity, transit breakthrough periods, and interview pacing.",
        "free_result_scope": "Job search velocity indicator and current transit status.",
        "primary_cta": "Get Job Search Tactics Report",
        "secondary_cta": "Explore Interview Strategies",
        "tertiary_link": "Unblocking Framework",
        "recommended_plan": "report_job_search",
        "plan_name": "Job Search & Interview Tactics Report",
        "price_inr": 199,
        "original_price_inr": 399,
        "deliverables": [
            "Diagnosis of Current Application Blockages",
            "Breakthrough Interview & Offer Decision Windows",
            "Salary Negotiation Timing & Communication Style",
            "Practical Confidence & Mindset Calibration"
        ]
    },

    # Group: Self and Growth
    "report_intelligence": {
        "id": "report_intelligence",
        "name": "Cognitive Strengths & Intelligence Report",
        "category": "Self and Growth",
        "category_group": "Self and Growth",
        "pricing_personality": 3,
        "awareness_hook": "Uncover analytical, creative, and intuitive intelligence patterns from your chart.",
        "curiosity_hook": "How Does Your Mind Process, Synthesize, and Excel?",
        "value_bridge": "Audit Mercury cognition, Jupiterian wisdom, and Lo Shu thought-action planes.",
        "free_result_scope": "Intellectual orientation (Analytical vs Creative) balance.",
        "primary_cta": "Get Intelligence Blueprint",
        "secondary_cta": "Compare Growth Reports",
        "tertiary_link": "Cognitive Models",
        "recommended_plan": "report_intelligence",
        "plan_name": "Cognitive Strengths & Intelligence Report",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "Dominant Cognitive Wiring (Analytical, Creative, Intuitive)",
            "Mercury & Jupiter Resonance with Learning Channels",
            "Focus Enhancement & Mental Energy Conservation",
            "Strategic Problem-Solving Playbook"
        ]
    },
    "report_life_guidance": {
        "id": "report_life_guidance",
        "name": "Life Purpose & Sovereign Guidance Report",
        "category": "Self and Growth",
        "category_group": "Self and Growth",
        "pricing_personality": 1,
        "awareness_hook": "Profound philosophical orientation, dharma alignment, and major life phase lessons.",
        "curiosity_hook": "What Is the Deeper Purpose Guiding Your Journey?",
        "value_bridge": "Explore soul purpose markers, Driver-Conductor synergy, and long-term fulfillment.",
        "free_result_scope": "Primary life lesson and core soul alignment direction.",
        "primary_cta": "Get Sovereign Life Guidance",
        "secondary_cta": "Preview Guidance Report",
        "tertiary_link": "Dharmic Alignment",
        "recommended_plan": "report_life_guidance",
        "plan_name": "Life Purpose & Sovereign Guidance Report",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "Core Soul Purpose (Dharma) & Karmic Direction",
            "Major Life Phase Lessons & Evolution Markers",
            "Personal Values Hierarchy & Integrity Anchor",
            "Daily Sattvic Living & Purposeful Energy Rituals"
        ]
    },
    "report_personality": {
        "id": "report_personality",
        "name": "Personality Archetype & Behavioral Dynamics",
        "category": "Self and Growth",
        "category_group": "Self and Growth",
        "pricing_personality": 3,
        "awareness_hook": "Explore psychological temperament, subconscious instincts, and interpersonal presence.",
        "curiosity_hook": "How Do Others Truly Perceive and Experience You?",
        "value_bridge": "Examine behavioral strengths, shadow dynamics, and personal charismatic resonance.",
        "free_result_scope": "Core personality archetype name and dominant virtue.",
        "primary_cta": "Get Personality Report",
        "secondary_cta": "Compare Self Reports",
        "tertiary_link": "Archetype Index",
        "recommended_plan": "report_personality",
        "plan_name": "Personality Archetype & Behavioral Dynamics",
        "price_inr": 199,
        "original_price_inr": 399,
        "deliverables": [
            "Primary Psychological & Planetary Archetype",
            "Interpersonal Strengths & Hidden Shadow Patterns",
            "Emotional Grounding & Boundary Fortification",
            "Personal Presence & Authentic Expression Guide"
        ]
    },
    "report_education": {
        "id": "report_education",
        "name": "Higher Education & Academic Mastery Report",
        "category": "Self and Growth",
        "category_group": "Self and Growth",
        "pricing_personality": 3,
        "awareness_hook": "Academic stream selection, higher education prospects, and study abroad timing.",
        "curiosity_hook": "Which Academic Domain Truly Amplifies Your Future?",
        "value_bridge": "Analyze 4th/5th/9th house educational strengths, concentration cycles, and foreign study.",
        "free_result_scope": "Academic stream affinity indicator and focus strengths.",
        "primary_cta": "Get Academic Mastery Report",
        "secondary_cta": "Explore Study Timing",
        "tertiary_link": "Academic Strengths",
        "recommended_plan": "report_education",
        "plan_name": "Higher Education & Academic Mastery Report",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "Best-Fit Academic Streams (STEM, Commerce, Humanities, Arts)",
            "Higher Education & Advanced Degree Timing Windows",
            "Overseas Education / Study Abroad Indicators",
            "Concentration Optimization & Study Space Vastu"
        ]
    },

    # ── 8 REPORT BUNDLES ───────────────────────────────────────────────────────
    "bundle_love_compatibility": {
        "id": "bundle_love_compatibility",
        "name": "Love & Compatibility Set",
        "category": "bundle",
        "pricing_personality": 6,
        "awareness_hook": "Complete romantic journey package: Love Style, Ideal Partner profile, and Marriage timing blueprint.",
        "curiosity_hook": "Experience Complete Romantic & Relationship Clarity",
        "value_bridge": "3 Comprehensive PDF Reports covering Love Style, Ideal Partner, and Marriage timing with unified synastry.",
        "free_result_scope": "Overview of included romantic blueprints and savings.",
        "primary_cta": "Explore Love & Compatibility Set",
        "secondary_cta": "Preview Bundle Reports",
        "tertiary_link": "Bundle Terms & Inclusions",
        "recommended_plan": "bundle_love_compatibility",
        "plan_name": "Love & Compatibility Set",
        "price_inr": 1499,
        "original_price_inr": 1999,
        "deliverables": [
            "3 Comprehensive PDF Reports (Love Style, Ideal Partner, Marriage)",
            "Combined Venusian & Spousal Synastry Breakdown",
            "Save ₹500 off the bundle list price",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_marriage_family": {
        "id": "bundle_marriage_family",
        "name": "Marriage & Family Harmony Set",
        "category": "bundle",
        "pricing_personality": 6,
        "awareness_hook": "Total marital and domestic serenity package: Marriage readiness, Spouse personality, and In-laws harmony.",
        "curiosity_hook": "Harmonize Sacred Union and Extended Domestic Peace",
        "value_bridge": "3 In-depth PDF Reports addressing marriage timing, spouse profile, and peaceful family relationships.",
        "free_result_scope": "Overview of domestic harmony modules and savings.",
        "primary_cta": "Explore Marriage & Family Set",
        "secondary_cta": "Preview Inclusions",
        "tertiary_link": "Domestic Vastu Guide",
        "recommended_plan": "bundle_marriage_family",
        "plan_name": "Marriage & Family Harmony Set",
        "price_inr": 1499,
        "original_price_inr": 1999,
        "deliverables": [
            "3 Comprehensive PDF Reports (Marriage, Spouse, In-Laws)",
            "Extended Family Vastu & Communication Protocol",
            "Save ₹500 off the bundle list price",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_career_starter": {
        "id": "bundle_career_starter",
        "name": "Career Starter Set",
        "category": "bundle",
        "pricing_personality": 1,
        "awareness_hook": "Essential stepping stones for early career professionals: First Job, Job Search tactics, and Career blueprint.",
        "curiosity_hook": "Accelerate Your First Professional Milestone",
        "value_bridge": "3 Practical PDF Reports guiding early placement, active interview tactics, and long-term career foundation.",
        "free_result_scope": "Early career diagnostic and bundle savings overview.",
        "primary_cta": "Explore Career Starter Set",
        "secondary_cta": "Compare Career Options",
        "tertiary_link": "Campus to Corporate Guide",
        "recommended_plan": "bundle_career_starter",
        "plan_name": "Career Starter Set",
        "price_inr": 699,
        "original_price_inr": 1299,
        "deliverables": [
            "3 Practical PDF Reports (First Job, Job Search, Career)",
            "Interview Timing & Resume Calibration Guides",
            "Save ₹600 (46% off) compared to bundle list price",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_career_decision": {
        "id": "bundle_career_decision",
        "name": "Career Decision Set",
        "category": "bundle",
        "pricing_personality": 1,
        "awareness_hook": "Definitive career crossroads package: Career leadership, Business venture feasibility, and Job vs Business.",
        "curiosity_hook": "Make High-Stakes Career Choices with Total Certainty",
        "value_bridge": "3 Master-tier PDF Reports resolving corporate growth vs commercial enterprise with exact timing windows.",
        "free_result_scope": "Crossroads readiness diagnostic and savings breakdown.",
        "primary_cta": "Explore Career Decision Set",
        "secondary_cta": "Review Crossroads Reports",
        "tertiary_link": "Corporate Transition Framework",
        "recommended_plan": "bundle_career_decision",
        "plan_name": "Career Decision Set",
        "price_inr": 1999,
        "original_price_inr": 2499,
        "deliverables": [
            "3 Comprehensive PDF Reports (Career, Business, Job or Business)",
            "Executive Transition & Corporate Autonomy Roadmap",
            "Save ₹500 off bundle list (Save ₹598 over individual offers)",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_money_wealth": {
        "id": "bundle_money_wealth",
        "name": "Money & Wealth Set",
        "category": "bundle",
        "pricing_personality": 6,
        "awareness_hook": "Total financial mastery package: Wealth cashflow management and Sovereign Billionaire Potential blueprint.",
        "curiosity_hook": "Explore Sovereign Financial Scale and Retention",
        "value_bridge": "2 Elite Financial PDF Reports uniting tactical cashflow unblocking with high-stakes Dhana Yoga architecture.",
        "free_result_scope": "Prosperity plane preview and bundle savings overview.",
        "primary_cta": "Explore Money & Wealth Set",
        "secondary_cta": "Preview Wealth Modules",
        "tertiary_link": "Financial Architecture",
        "recommended_plan": "bundle_money_wealth",
        "plan_name": "Money & Wealth Set",
        "price_inr": 1999,
        "original_price_inr": 2499,
        "deliverables": [
            "2 Elite Financial PDF Reports (Wealth, Billionaire Potential)",
            "Dhana Yoga & Cashflow Leakage Remediation",
            "Save ₹500 off bundle list (Save ₹199 over individual offers)",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_self_discovery": {
        "id": "bundle_self_discovery",
        "name": "Self-Discovery Set",
        "category": "bundle",
        "pricing_personality": 3,
        "awareness_hook": "Profound inner alignment package: Personality archetype, Cognitive intelligence, and Sovereign life guidance.",
        "curiosity_hook": "Uncover Who You Truly Are Across Every Dimension",
        "value_bridge": "3 In-Depth Personal PDF Reports exploring psychological temperament, cognitive wiring, and dharmic soul purpose.",
        "free_result_scope": "Core archetype overview and bundle inclusions.",
        "primary_cta": "Explore Self-Discovery Set",
        "secondary_cta": "Preview Self Reports",
        "tertiary_link": "Holistic Discovery Framework",
        "recommended_plan": "bundle_self_discovery",
        "plan_name": "Self-Discovery Set",
        "price_inr": 1499,
        "original_price_inr": 1999,
        "deliverables": [
            "3 In-Depth Personal PDF Reports (Personality, Intelligence, Life Guidance)",
            "Cognitive Wiring & Soul Purpose Alignment",
            "Save ₹500 off the bundle list price",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_learning_growth": {
        "id": "bundle_learning_growth",
        "name": "Learning & Growth Set",
        "category": "bundle",
        "pricing_personality": 3,
        "awareness_hook": "Intellectual mastery package: Academic achievement, Intellectual aptitude, and Personality strengths.",
        "curiosity_hook": "Sharpen Your Intellect and Maximize Academic Flow",
        "value_bridge": "3 Focused Educational PDF Reports combining academic stream selection, cognitive processing, and personality traits.",
        "free_result_scope": "Learning style indicator and bundle savings breakdown.",
        "primary_cta": "Explore Learning & Growth Set",
        "secondary_cta": "Preview Academic Modules",
        "tertiary_link": "Academic Excellence Principles",
        "recommended_plan": "bundle_learning_growth",
        "plan_name": "Learning & Growth Set",
        "price_inr": 1499,
        "original_price_inr": 1999,
        "deliverables": [
            "3 Focused Educational PDF Reports (Education, Intelligence, Personality)",
            "Study Vastu & Academic Timing Calendars",
            "Save ₹500 off the bundle list price",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_complete_personal_insight": {
        "id": "bundle_complete_personal_insight",
        "name": "Complete Personal Insight Suite",
        "category": "bundle",
        "pricing_personality": 3,
        "awareness_hook": "Definitive multi-domain portfolio combining all core discovery and growth reports into one sovereign package.",
        "curiosity_hook": "Total Life Alignment Across Love, Wealth, Career, and Growth",
        "value_bridge": "Unlocks full personal dossier spanning personality, intelligence, career guidance, wealth, and relationship synastry.",
        "free_result_scope": "Comprehensive portfolio breakdown and massive multi-report savings.",
        "primary_cta": "Explore Complete Insight Suite",
        "secondary_cta": "Compare Bundle Suites",
        "tertiary_link": "Master Suite Deliverables",
        "recommended_plan": "bundle_complete_personal_insight",
        "plan_name": "Complete Personal Insight Suite",
        "price_inr": 2499,
        "original_price_inr": 3999,
        "deliverables": [
            "6 Foundational Personal PDF Reports Across All Domains",
            "Full Multi-System Consensus & Harmonic Alignment",
            "Save ₹1,500 off the suite list price",
            "Lifetime download access with free updates"
        ]
    },

    # ── 6 CHARM AI CONVERSATIONAL PACKAGES ─────────────────────────────────────
    "charm_quick_insight": {
        "id": "charm_quick_insight",
        "name": "Charm AI — Quick Insight",
        "category": "charm_package",
        "pricing_personality": 1,
        "awareness_hook": "Single pressing question answered with deterministic ephemeris and zero hallucination.",
        "curiosity_hook": "Need Immediate Clarity on One Urgent Life Question?",
        "value_bridge": "Direct, source-verified conversational answer with planetary timing window and practical action.",
        "free_result_scope": "Sample AI inquiry response and source methodology.",
        "primary_cta": "Get Quick Insight",
        "secondary_cta": "Compare Charm AI Packs",
        "tertiary_link": "Grounded Charm AI Standards",
        "recommended_plan": "charm_quick_insight",
        "plan_name": "Charm AI — Quick Insight",
        "price_inr": 199,
        "original_price_inr": 399,
        "deliverables": [
            "1 Dedicated Charm AI Consultation Turn",
            "Classical ephemeris calculation & dasha timing check",
            "Clear, concise answer with 3 practical action steps",
            "Zero hallucination guarantee bound to classical texts"
        ]
    },
    "charm_focused_reading": {
        "id": "charm_focused_reading",
        "name": "Charm AI — Focused Reading",
        "category": "charm_package",
        "pricing_personality": 3,
        "awareness_hook": "Deep-dive inquiry into a single life challenge with up to 3 follow-up clarifying questions.",
        "curiosity_hook": "Explore One Life Challenge in Complete Depth",
        "value_bridge": "One topic with a defined follow-up allowance and structured summary across 4 consultation turns.",
        "free_result_scope": "Structured topic consultation overview.",
        "primary_cta": "Get Focused Reading",
        "secondary_cta": "Compare AI Packages",
        "tertiary_link": "Topic Scope & Follow-Ups",
        "recommended_plan": "charm_focused_reading",
        "plan_name": "Charm AI — Focused Reading",
        "price_inr": 399,
        "original_price_inr": 699,
        "deliverables": [
            "4 Dedicated Charm AI Consultation Turns",
            "In-depth topic exploration with follow-up allowance",
            "Structured summary & timing window breakdown",
            "Custom 7-Layer safe lifestyle remedies"
        ]
    },
    "charm_consensus_reading": {
        "id": "charm_consensus_reading",
        "name": "Charm AI — Consensus Reading",
        "category": "charm_package",
        "pricing_personality": 5,
        "awareness_hook": "One topic evaluated across eligible, enabled and validated traditions with cross-system verification.",
        "curiosity_hook": "Compare What Multiple Ancient Systems Reveal About Your Query",
        "value_bridge": "Rigorous cross-verification comparing Numerology Dasha against KP, Vedic Parashari, and BNN.",
        "free_result_scope": "Multi-system consensus badge sample and tradition eligibility rules.",
        "primary_cta": "Get Consensus Reading",
        "secondary_cta": "Review Multi-System Rules",
        "tertiary_link": "Classical Corpus Citations",
        "recommended_plan": "charm_consensus_reading",
        "plan_name": "Charm AI — Consensus Reading",
        "price_inr": 699,
        "original_price_inr": 1299,
        "deliverables": [
            "8 In-depth Charm AI Consultation Turns",
            "Deterministic multi-system consensus evaluation",
            "Citations from verified Numeros Vision classical corpus",
            "Strict status badge (CORROBORATED / CONFLICTED / ONLY)"
        ]
    },
    "charm_personal_blueprint": {
        "id": "charm_personal_blueprint",
        "name": "Charm AI — Personal Blueprint",
        "category": "charm_package",
        "pricing_personality": 1,
        "awareness_hook": "Full life-aspect exploration spanning career pivots, marital timing, and financial security.",
        "curiosity_hook": "Consult Across Every Dimension of Your Life Blueprint",
        "value_bridge": "20 consultation turns covering career, wealth, relationships, and health with transcript download.",
        "free_result_scope": "Multi-topic blueprint preview and session allowance.",
        "primary_cta": "Explore Personal Blueprint",
        "secondary_cta": "Compare Blueprint Packages",
        "tertiary_link": "Blueprint Consultation Terms",
        "recommended_plan": "charm_personal_blueprint",
        "plan_name": "Charm AI — Personal Blueprint",
        "price_inr": 1499,
        "original_price_inr": 1999,
        "deliverables": [
            "20 Comprehensive Charm AI Consultation Turns",
            "Multi-topic coverage (Career, Wealth, Relationships, Health)",
            "Annual Personal Year transit and hora timing radar",
            "Downloadable summary transcript of full consultation"
        ]
    },
    "charm_family_compatibility": {
        "id": "charm_family_compatibility",
        "name": "Charm AI — Family Compatibility",
        "category": "charm_package",
        "pricing_personality": 6,
        "awareness_hook": "Interactive dual-profile synastry consultation exploring partner, family, or business synergy.",
        "curiosity_hook": "Discover Deep Relational Harmony Between Two Charts",
        "value_bridge": "Compatibility themes for user-supplied profiles with appropriate DPDP 2023 statutory consent.",
        "free_result_scope": "Synastry consultation format and privacy guarantees.",
        "primary_cta": "Explore Family Compatibility",
        "secondary_cta": "Preview Synastry Consultation",
        "tertiary_link": "DPDP 2023 Consent Notice",
        "recommended_plan": "charm_family_compatibility",
        "plan_name": "Charm AI — Family Compatibility",
        "price_inr": 699,
        "original_price_inr": 1299,
        "deliverables": [
            "8 Dual-Profile Charm AI Consultation Turns",
            "Driver/Conductor polarity and shared Lo Shu plane audit",
            "Interpersonal friction mitigation and communication advice",
            "Complies strictly with statutory DPDP 2023 consent"
        ]
    },
    "charm_career_business_direction": {
        "id": "charm_career_business_direction",
        "name": "Charm AI — Career & Business Direction",
        "category": "charm_package",
        "pricing_personality": 1,
        "awareness_hook": "Dedicated corporate and commercial guidance for job transitions, appraisal timing, or founder pivots.",
        "curiosity_hook": "Accelerate Your Professional Velocity with Precision Timing",
        "value_bridge": "Career/business exploration and practical next-step prompts across 8 strategic turns.",
        "free_result_scope": "Career consultation methodology and decision window sample.",
        "primary_cta": "Explore Career & Business Direction",
        "secondary_cta": "Compare Executive AI Plans",
        "tertiary_link": "Commercial Timing Rules",
        "recommended_plan": "charm_career_business_direction",
        "plan_name": "Charm AI — Career & Business Direction",
        "price_inr": 699,
        "original_price_inr": 1299,
        "deliverables": [
            "8 Strategic Career & Business Turns",
            "Acute execution window mapping (Pratyantardasha)",
            "3-point practical outreach & workspace grounding actions",
            "Zero ungrounded speculation or commercial guarantees"
        ]
    }
}


# ── 4. REUSABLE FUNNEL SERVICE CONTRACT ──────────────────────────────────────

@dataclass
class JourneyContext:
    user_id: Optional[str] = None
    session_token: Optional[str] = None
    user_opted_out_of_marketing: bool = False
    calculation_completed: bool = False
    free_result_available: bool = False
    payment_status: Optional[str] = None       # "CONFIRMED", "FAILED", None
    fulfilment_status: Optional[str] = None    # "FULFILLED", "PENDING", None
    current_entitlements: List[str] = field(default_factory=list)
    market: str = "IN"
    currency: str = "INR"


def get_next_step(
    user: Optional[Dict[str, Any]],
    product_id: str,
    journey_context: JourneyContext,
    now: Optional[datetime] = None
) -> Dict[str, Any]:
    """
    Evaluates the seeker's current journey context and determines the next action.
    Adheres strictly to the 7-stage marketing funnel and user privacy rights.
    """
    now = now or datetime.now(timezone.utc)
    product = PRODUCT_FUNNEL_CATALOG.get(product_id, PRODUCT_FUNNEL_CATALOG["birth_number"])

    # 1. OPT-OUT PRECEDENCE: If user opted out of promotional communications,
    # suppress commercial upgrade hooks and return pure product action.
    if journey_context.user_opted_out_of_marketing:
        return {
            "stage": FunnelStage.INTEREST.value,
            "journey_state": JourneyState.OPTED_OUT.value,
            "type": "PRODUCT_ACTION",
            "product_id": product["id"],
            "headline": "Numeros Vision Diagnostic",
            "tagline": "ANVEIL EVERY CHARM",
            "message": "Promotional offers are paused. Your calculation tools remain fully accessible.",
            "cta_label": "Calculate My Number",
            "cta_url": f"/tools/{product['id'].replace('_', '-')}/",
            "opted_out": True
        }

    # 2. PAYMENT CONFIRMED BUT FULFILMENT PENDING: Tell user report is processing.
    if journey_context.payment_status == "CONFIRMED":
        if journey_context.fulfilment_status != "FULFILLED":
            return {
                "stage": FunnelStage.RETENTION.value,
                "journey_state": JourneyState.FULFILMENT_PENDING.value,
                "type": "FULFILMENT_STATUS",
                "product_id": product["id"],
                "headline": "Payment Confirmed · Preparing Your Report",
                "tagline": "ANVEIL EVERY CHARM",
                "message": "Your payment has been verified. Our deterministic engine is compiling your personalized dossier.",
                "cta_label": "Refresh Status",
                "cta_url": f"/dashboard/",
                "is_pending": True
            }
        # Fulfilled -> Post-purchase engagement
        return {
            "stage": FunnelStage.RETENTION.value,
            "journey_state": JourneyState.FULFILLED.value,
            "type": "POST_PURCHASE",
            "product_id": product["id"],
            "headline": "Your Report Is Ready",
            "tagline": "ANVEIL EVERY CHARM",
            "message": "Your complete dossier has been compiled and is ready for download.",
            "cta_label": "View My Report",
            "cta_url": f"/dashboard/",
            "is_ready": True
        }

    # 3. ALREADY OWNED ENTITLEMENT CHECK: Avoid offering duplicate purchases.
    rec_plan = product["recommended_plan"]
    if rec_plan in journey_context.current_entitlements or "report_divine" in journey_context.current_entitlements:
        return {
            "stage": FunnelStage.LOYALTY.value,
            "journey_state": JourneyState.LOYALTY_ELIGIBLE.value,
            "type": "ALREADY_OWNED",
            "product_id": product["id"],
            "headline": "You Have Unlocked This Insight",
            "tagline": "ANVEIL EVERY CHARM",
            "message": f"Your account already holds active access to {product['plan_name']}.",
            "cta_label": "View My Report",
            "cta_url": "/dashboard/",
            "secondary_cta": "Explore My Next Report",
            "secondary_url": "/reports/"
        }

    # 4. FREE RESULT READY -> CONSIDERATION (Step 2 Curiosity Bridge + Step 3 Offer):
    if journey_context.free_result_available:
        # Validate price with digit-root policy
        price_val = validate_price_pair(product["original_price_inr"], product["price_inr"])
        
        return {
            "stage": FunnelStage.CONSIDERATION.value,
            "journey_state": JourneyState.OFFER_ELIGIBLE.value,
            "type": "CONSIDERATION_OFFER",
            "product_id": product["id"],
            "product_name": product["name"],
            "tagline": "ANVEIL EVERY CHARM",
            "brand_hook": "Your Numbers. Your Possibilities. Anveil Every Charm.",
            "curiosity_hook": product["curiosity_hook"],
            "value_bridge": product["value_bridge"],
            "offer": {
                "plan_id": product["recommended_plan"],
                "plan_name": product["plan_name"],
                "price_inr": product["price_inr"],
                "original_price_inr": product["original_price_inr"],
                "digital_root": price_val["offer_root"],
                "savings_inr": price_val["savings_inr"],
                "discount_percent": f"{price_val['discount_percent']}% OFF",
                "deliverables": product["deliverables"]
            },
            "cta": {
                "primary_label": product["primary_cta"],
                "primary_url": f"/pricing#plans",
                "checkout_url": f"/checkout/?plan={product['recommended_plan']}",
                "secondary_label": product["secondary_cta"],
                "secondary_url": "/pricing#plans",
                "tertiary_label": product["tertiary_link"],
                "tertiary_url": "/sample-report/"
            },
            "reassurance": "Secure checkout · Clear pricing · Your free calculation remains preserved."
        }

    # 5. INITIAL ENTRY -> INTEREST (Step 1 Free Participation):
    return {
        "stage": FunnelStage.INTEREST.value,
        "journey_state": JourneyState.CALCULATION_STARTED.value,
        "type": "CALCULATION_INVITE",
        "product_id": product["id"],
        "product_name": product["name"],
        "tagline": "ANVEIL EVERY CHARM",
        "brand_hook": "Your Numbers. Your Possibilities. Anveil Every Charm.",
        "awareness_hook": product["awareness_hook"],
        "cta_label": "Calculate My Number",
        "cta_url": f"#calculator-form"
    }


# ── 5. PRIVACY-MINIMISED FUNNEL TELEMETRY ─────────────────────────────────────

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
FUNNEL_EVENTS_FILE = os.path.join(DATA_DIR, "funnel_events.jsonl")

ALLOWED_FUNNEL_EVENTS = {
    "landing_viewed",
    "calculator_viewed",
    "calculation_started",
    "calculation_completed",
    "free_result_viewed",
    "upgrade_panel_viewed",
    "sample_report_viewed",
    "product_details_viewed",
    "checkout_started",
    "payment_succeeded",
    "payment_failed",
    "report_generation_started",
    "report_delivered",
    "subscription_started",
    "subscription_renewed",
    "subscription_cancelled",
    "loyalty_benefit_used",
    "repeat_offer_viewed",
    "repeat_purchase_succeeded",
    "marketing_opt_out"
}


def log_funnel_event(
    event_name: str,
    product_id: Optional[str] = None,
    stage: Optional[str] = None,
    session_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Logs privacy-safe funnel events.
    Strictly forbids raw DOB, full mobile number, full name, or payment details.
    """
    if event_name not in ALLOWED_FUNNEL_EVENTS:
        return False

    safe_meta = {}
    if metadata:
        for k, v in metadata.items():
            # Disallow sensitive PII fields
            if k.lower() in ("dob", "birth_date", "mobile", "phone", "email", "name", "full_name", "card", "token"):
                continue
            if isinstance(v, (str, int, float, bool)):
                safe_meta[k] = v

    record = {
        "event": event_name,
        "product_id": product_id or "unknown",
        "stage": stage or "AWARENESS",
        "session_id": (session_id[:16] + "...") if session_id else "anon",
        "timestamp": int(time.time()),
        "iso_time": datetime.now(timezone.utc).isoformat(),
        "metadata": safe_meta
    }

    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(FUNNEL_EVENTS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        return True
    except Exception:
        return False
