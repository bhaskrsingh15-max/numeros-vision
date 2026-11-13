from dotenv import load_dotenv
load_dotenv(override=True)
"""
Razorpay Payment Integration — Numeros Vision
POST /api/v1/payments/create-order   → create Razorpay order
POST /api/v1/payments/verify         → verify payment signature (called client-side after success)
GET  /api/v1/payments/plans          → public pricing catalogue
"""

import os
import hmac
import hashlib
import json
import time
from typing import Optional, Dict, Any, List, Tuple
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.engine.monetization_alignment_engine import (
    analyze_user_alignment_and_gaps,
    is_staging_bypass_authorized
)
from app.config.pricing_config import (
    resolve_sku_price,
    is_notify_me_higher_tiers_enabled,
    REPORT_TIERS,
    BUNDLES,
    CHARM_AI_PACKS,
    CONSULTATION_PACKS,
)
from app.engine.funnel_service import (
    PricePolicy,
    digit_root,
    validate_single_price,
    validate_price_pair,
    FunnelStage,
    JourneyState,
    JourneyContext,
    get_next_step,
    log_funnel_event,
    PRODUCT_FUNNEL_CATALOG,
)
from app.api.auth import (
    update_user_entitlements,
    get_user_account_by_identifier,
    _ACTIVE_SESSIONS,
    _USER_ACCOUNTS
)

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])
api_router = APIRouter(prefix="/api", tags=["payments-standard"])

# ── Razorpay credentials (set in environment) ─────────────────────────────
# Test keys:  rzp_test_XXXXXXXXXXXXXXXXXXXX  /  your_test_secret
# Live keys:  rzp_live_XXXXXXXXXXXXXXXXXXXX  /  your_live_secret
RAZORPAY_KEY_ID         = os.getenv("RAZORPAY_KEY_ID", "rzp_test_REPLACE_ME")
RAZORPAY_KEY_SECRET     = os.getenv("RAZORPAY_KEY_SECRET", "REPLACE_ME_SECRET")
RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", RAZORPAY_KEY_SECRET)

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
SESSIONS_FILE = os.path.join(DATA_DIR, "verified_sessions.json")

# ── Plan catalogue ─────────────────────────────────────────────────────────
PLANS = {
    # ── UNIFIED STANDALONE REPORT TIERS ──────────────────────────────────────
    "report_basic": {
        "name": "Anveil my alignments",
        "amount_inr": 399,
        "original_price_inr": 399,
        "amount_paise": 39900,
        "period": "3-Page Personalized PDF",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "3-page personalized report covering core birth numbers, 9-cell Lo Shu Grid (Lo Shu Square), Calling Name number (Chaldean Name number) harmony, and Five-Element lifestyle guidance.",
        "features": [
            "Core Numbers: Mulank (Birth Day number), Bhagyank (Life Path number), Kua number (Vastu direction number) & Personal Year",
            "9-Cell Lo Shu Grid (Lo Shu Square) Mapping & Active Plane Strengths",
            "Calling Name number (Chaldean Name number) Harmony Check",
            "Five-Element Distribution Balance & Practical Lifestyle Guidance",
            "Instant 3-Page Print-Ready Personalized PDF Report"
        ]
    },
    "report_advanced": {
        "name": "Anveil my glowing charms",
        "amount_inr": 1020,
        "original_price_inr": 1020,
        "amount_paise": 102000,
        "period": "12-Page Structured PDF",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "popular": True,
        "description": "12-page structured report covering present numbers, repeating digit amplifications, all 8 Lo Shu planes, and career/relationship/financial archetype compatibility.",
        "features": [
            "Everything in Basic plus Deep Analysis of All Present Numbers",
            "Repeating Digit Amplifications & Behavioral Tendencies",
            "8 Lo Shu Planes & Raj Yoga Combinations Breakdown",
            "Career, Relationship & Financial Archetype Compatibility",
            "12-Page Structured PDF Report with Actionable Daily Habits"
        ]
    },
    "report_premium": {
        "name": "Anveil every charm",
        "amount_inr": 2100,
        "original_price_inr": 2100,
        "amount_paise": 210000,
        "period": "32-Page Complete Reference PDF",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "32-page complete reference report covering missing numbers (open grid cells), multi-year Numerology Dasha & Pinnacle cycles, Chaldean name & signature alignment options, and practical lifestyle harmonizers.",
        "features": [
            "Everything in Basic & Advanced plus Missing Numbers (Open Grid Cells) Analysis",
            "Multi-Year Numerology Dasha & Pinnacle Cycle Timeline",
            "Chaldean Name Balancing & Signature Alignment Options",
            "Practical Lifestyle, Color, Directional (Vastu) & Habit Harmonizers",
            "Complete 32-Page Personalized Reference PDF Report"
        ]
    },
    # ── UNIFIED MULTI-REPORT BUNDLES ─────────────────────────────────────────
    "starter_bundle": {
        "name": "Starter Bundle — 2 Anveil my alignmentss",
        "amount_inr": 349,
        "original_price_inr": 398,
        "amount_paise": 34900,
        "period": "2 Anveil my alignmentss",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "description": "Two 3-page Basic reports of your choice across Love, Money, Work, or Growth.",
        "features": ["2 Complete Basic 3-Page Reports", "Save ₹49 (12% off standalone)", "Independent deterministic calculation traces", "Instant PDF downloads"]
    },
    "discovery_bundle": {
        "name": "Discovery Bundle — 3 Anveil my alignmentss",
        "amount_inr": 499,
        "original_price_inr": 597,
        "amount_paise": 49900,
        "period": "3 Anveil my alignmentss",
        "questions_count": 0,
        "has_remedies": True,
        "popular": True,
        "category": "bundle",
        "description": "Three 3-page Basic reports covering Love, Career, and Wealth foundations.",
        "features": ["3 Complete Basic 3-Page Reports", "Save ₹98 (16% off standalone)", "Multi-domain life audit", "Unified dashboard access"]
    },
    "comprehensive_bundle": {
        "name": "Comprehensive Bundle — 2 Advanced + 1 Basic",
        "amount_inr": 999,
        "original_price_inr": 1219,
        "amount_paise": 99900,
        "period": "2 Advanced + 1 Basic (27 pages total)",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "description": "Two 12-page Advanced reports plus one 3-page Basic report for major life pivots.",
        "features": ["2 Complete 12-Page Advanced Reports (24 pages)", "1 Complete 3-Page Anveil my alignments (3 pages)", "Save ₹220 (18% off standalone)", "Full Dasha timelines & 7-layer remedies"]
    },
    # ── UNIFIED CHARM AI PACKAGES ────────────────────────────────────────────
    "charm_single": {
        "name": "Charm AI — Starter Pass",
        "amount_inr": 199,
        "original_price_inr": 399,
        "amount_paise": 19900,
        "period": "5 Questions",
        "questions_count": 5,
        "has_remedies": True,
        "category": "ai_credits",
        "description": "3 targeted Charm AI predictions with acute execution timing windows.",
        "features": ["3 In-Depth Question Predictions", "Auspicious timing windows & lucky dates", "Grounded non-fatalistic guidance", "Valid for 6 months"]
    },
    "charm_multi": {
        "name": "Charm AI — Multi-Reading Pack",
        "amount_inr": 399,
        "original_price_inr": 599,
        "amount_paise": 39900,
        "period": "10 Questions + Remedies",
        "questions_count": 10,
        "has_remedies": True,
        "popular": True,
        "category": "ai_credits",
        "description": "10 detailed question predictions with customized safe remedies for active decisions.",
        "features": ["10 In-Depth Question Predictions", "Customized 7-layer safe remedies", "Auspicious date selection & Muhurat", "Valid for 12 months"]
    },
    "charm_extended": {
        "name": "Charm AI — Extended Pack",
        "amount_inr": 699,
        "original_price_inr": 1299,
        "amount_paise": 69900,
        "period": "25 Questions + Roadmap",
        "questions_count": 25,
        "has_remedies": True,
        "category": "ai_credits",
        "description": "25 comprehensive question predictions with full transit radar and companion features.",
        "features": ["25 Deep Question Predictions", "Interactive chart companion & transit radar", "Multi-profile synastry consultations", "Downloadable consultation transcripts"]
    },
    # ── UNIFIED 1-ON-1 CONSULTATION ──────────────────────────────────────────
    "consultation_standard": {
        "name": "1-on-1 Expert Consultation",
        "amount_inr": 1050,
        "original_price_inr": 1499,
        "amount_paise": 105000,
        "period": "45-Minute Private Session",
        "questions_count": 0,
        "has_remedies": True,
        "category": "consultation",
        "description": "45-minute private 1-on-1 video/phone consultation with a certified senior numerologist.",
        "features": ["45-Minute Private 1-on-1 Consultation", "Birth Time Rectification (BTR) & Chart Audit", "Complimentary 12-Page Advanced PDF Dossier", "Audio recording & written consultation summary", "Free 1-time rescheduling up to 24h prior"]
    },

    "starter_5q": {
        "name":        "Starter — 5 Questions",
        "amount_inr":  95,
        "original_price_inr": 199,
        "amount_paise": 9500,          # Razorpay uses smallest currency unit (paise)
        "period":      "5 Questions",
        "questions_count": 5,
        "has_remedies": False,
        "description": "5 question predictions of any user queries",
        "features": [
            "5 In-depth Question Predictions",
            "ANVEIL EVERY CHARM Alignment & Timing",
            "Valid across Career, Love, Wealth & Health",
            "Instant Charm AI answers 24/7",
        ]
    },
    "growth_10q": {
        "name":        "Growth — 10 Questions + Remedies",
        "amount_inr":  399,
        "original_price_inr": 599,
        "amount_paise": 39900,
        "period":      "10 Questions + Remedies",
        "questions_count": 10,
        "has_remedies": True,
        "description": "10 questions predictions with customized remedies for all 10 questions",
        "features": [
            "10 In-depth Question Predictions",
            "Custom Remedies for all 10 questions",
            "Auspicious timing & lucky dates",
            "Gemstone & practical energy rituals",
            "Priority Charm AI response",
        ]
    },
    "complete_report": {
        "name":        "Complete Reports & Remedies",
        "amount_inr":  1050,
        "original_price_inr": 1299,
        "amount_paise": 105000,
        "period":      "Complete Access",
        "questions_count": 9999,
        "has_remedies": True,
        "description": "Complete destiny reports and comprehensive remedies",
        "features": [
            "Complete Personal Destiny Blueprint Report",
            "Comprehensive Multi-Layer Remedies",
            "Personalized Vedic Gemstone Prescription",
            "Annual Timing Forecast & Life Roadmap",
            "Unlimited Question Predictions with Remedies",
            "Downloadable PDF Personal Report",
        ]
    },
    # ── 1. NUMEROLOGY REPORT PACKAGES (3 TIERS) ─────────────────────────────
    "report_essential": {
        "name":        "Anveil my alignments",
        "amount_inr":  199,
        "original_price_inr": 399,
        "amount_paise": 19900,
        "period":      "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "report",
        "description": "A concise report presenting your calculated results, the method used and an initial interpretation of the key findings.",
        "features": [
            "3-Page Executive PDF Report",
            "Calculated Results & Method Used",
            "Key Findings Initial Interpretation",
            "Driver & Conductor Foundation",
            "Lo Shu 3x3 Grid Summary"
        ]
    },
    "report_master": {
        "name":        "Anveil my glowing charms",
        "amount_inr":  510,
        "original_price_inr": 1020,
        "amount_paise": 51000,
        "period":      "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "report",
        "description": "A more detailed report providing expanded interpretations, relevant number relationships and additional analysis supported by the selected product.",
        "features": [
            "12-Page Master Synthesis Dossier",
            "Expanded Interpretations & Number Relationships",
            "5-Year Numerology Dasha Dasha Timeline",
            "7-Layer Safe Planetary Remedies",
            "Chaldean Sound Frequency Analysis"
        ]
    },
    "report_divine": {
        "name":        "Anveil every charm",
        "amount_inr":  1050,
        "original_price_inr": 2100,
        "amount_paise": 105000,
        "period":      "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "report",
        "description": "An extensive report bringing together the supported calculations, detailed interpretations, relevant comparisons and personalised recommendations available for the selected product.",
        "features": [
            "32-Page Sovereign Executive Blueprint",
            "Complete Calculations & Detailed Interpretations",
            "Multi-Generation Compatibility & Comparisons",
            "Personalised Multi-Layer Recommendations",
            "10-Year Macro Planetary Timing Radar"
        ]
    },
    # ── 2. AI QUESTION CREDITS & SUBSCRIPTIONS ──────────────────────────────
    "ai_starter_5q": {
        "name":        "Charm AI — Starter Pack (5 Questions)",
        "amount_inr":  95,
        "original_price_inr": 199,
        "amount_paise": 9500,
        "period":      "5 Questions",
        "questions_count": 5,
        "has_remedies": False,
        "category":    "ai_credits",
        "description": "5 targeted Charm AI question predictions across Career, Love, Wealth or Health",
        "features": [
            "5 Targeted Charm AI Predictions",
            "Cross-engine consensus verification",
            "Valid across Career, Marriage, Wealth & Health",
            "Instant 24/7 grounded response"
        ]
    },
    "ai_growth_15q": {
        "name":        "Charm AI — Growth Pack (15 Questions + Remedies)",
        "amount_inr":  249,
        "original_price_inr": 499,
        "amount_paise": 24900,
        "period":      "15 Questions + Remedies",
        "questions_count": 15,
        "has_remedies": True,
        "category":    "ai_credits",
        "description": "15 deep question predictions with customized safe remedies and auspicious timing",
        "features": [
            "15 In-depth Question Predictions",
            "Customized 7-Layer Safe Remedies for each query",
            "Auspicious timing windows & lucky dates",
            "Priority Charm AI response speed"
        ]
    },
    "ai_power_35q": {
        "name":        "Charm AI — Power Pack (35 Questions + Auspicious Timing)",
        "amount_inr":  499,
        "original_price_inr": 899,
        "amount_paise": 49900,
        "period":      "35 Questions + Remedies",
        "questions_count": 35,
        "has_remedies": True,
        "category":    "ai_credits",
        "description": "35 comprehensive question predictions for active decision-makers making complex life pivots",
        "features": [
            "35 Comprehensive In-depth Predictions",
            "Full planetary transit & Dasha overlap analysis",
            "Personalized daily auspicious decision windows",
            "Rollover credits valid for 12 months"
        ]
    },
    "sub_monthly": {
        "name":        "Cosmic Timing Engine — Monthly Pass",
        "amount_inr":  149,
        "original_price_inr": 299,
        "amount_paise": 14900,
        "period":      "Monthly Recurring",
        "questions_count": 10,
        "has_remedies": True,
        "category":    "subscription",
        "description": "Continuous monthly transit alerts, monthly auspicious Muhurat calendar, and 10 monthly AI questions",
        "features": [
            "Weekly Gochar (Transit) alerts to WhatsApp/Email",
            "Monthly Auspicious Muhurat Action Calendar",
            "10 Monthly Charm AI questions (rollover enabled)",
            "20% discount on physical remedies & consultations"
        ]
    },
    "sub_annual": {
        "name":        "Cosmic Timing Engine — Annual VIP Pass",
        "amount_inr":  999,
        "original_price_inr": 1788,
        "amount_paise": 99900,
        "period":      "Annual Recurring (Save 44%)",
        "questions_count": 150,
        "has_remedies": True,
        "category":    "subscription",
        "description": "Complete 365-day planetary transit radar, monthly calendars, and 150 annual question credits",
        "features": [
            "365 Days of Personalized Planetary Transit Alerts",
            "12 Monthly Auspicious Muhurat Action Calendars",
            "150 Charm AI Question Credits",
            "Complimentary Master Synthesis PDF Report (₹510 value)",
            "Priority VIP customer support"
        ]
    },
    # ── 3. AI + REPORT INTERACTIVE COMBO ────────────────────────────────────
    "ai_report_combo": {
        "name":        "Interactive Charm AI + Master Report Combo",
        "amount_inr":  699,
        "original_price_inr": 1498,
        "amount_paise": 69900,
        "period":      "Report + Interactive Charm AI",
        "questions_count": 25,
        "has_remedies": True,
        "category":    "combo",
        "description": "35-Page Master PDF Report PLUS interactive conversational Charm AI loaded with your exact chart tokens",
        "features": [
            "35-40 Page Master Dual-System PDF Report (Instant download)",
            "Interactive Charm AI Chart Companion (Talk directly to your report)",
            "25 Pre-loaded questions to interrogate your chart and predictions",
            "Zero-hallucination answers bound strictly to your verified chart tokens",
            "Custom 7-Layer Safe Remedy Matrix"
        ]
    },
    # ── 4. PERSONAL CONSULTATION & SACRED GEOMETRY ADVISORY ─────────────────
    "advisory_personal_name": {
        "name":        "Personal Name Balancing & Spelling Calibration",
        "amount_inr":  1499,
        "original_price_inr": 2499,
        "amount_paise": 149900,
        "period":      "Advisory Dossier",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "advisory",
        "description": "Full Chaldean + Pythagorean vibration audit of legal and calling names with 3 optimal harmonized variations",
        "features": [
            "Legal Name vs Calling Name vibrational coherence audit",
            "Elimination of karmic debt compound numbers (13, 14, 16, 19, 28)",
            "3 Optimal Harmonized Spelling Variations",
            "Social signature, LinkedIn & email handle optimization guide",
            "Official gazette & affidavit spelling transition checklist"
        ]
    },
    "advisory_business_name": {
        "name":        "Commercial Entity & Brand Matrix",
        "amount_inr":  5999,
        "original_price_inr": 14000,
        "amount_paise": 599900,
        "period":      "Corporate Advisory",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "advisory",
        "description": "Full corporate GST registration alignment, trademark entity vibration, brand geometry, and multi-partner synastry audit",
        "features": [
            "Corporate Legal Name & Trade Name vibration audit",
            "Founder & Co-Founder Synergy Compatibility Matrix",
            "Incorporation & Launch Muhurat (3 high-probability dates)",
            "Bank Account & Invoicing numerical vibration audit",
            "Domain name & brand moniker numerical audit"
        ]
    },
    "advisory_brand_logo": {
        "name":        "Brand Logo Balancing & Sacred Geometry Harmony",
        "amount_inr":  9999,
        "original_price_inr": 15000,
        "amount_paise": 999900,
        "period":      "Executive Branding Dossier",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "advisory",
        "description": "5-Element sacred geometric vector audit, planetary color harmonization, upward trajectory verification, and 3 logo vectors",
        "features": [
            "5-Element Geometric Vector Energy Audit (Earth/Water/Fire/Air)",
            "Planetary Color Vector Harmonization aligned with Founders' charts",
            "Upward-right growth trajectory vector verification",
            "Yantra sacred geometry proportion alignment",
            "3 Finalized Balanced Vector Logo Concepts (SVG / AI / PNG)",
            "Complete Brand Sacred Geometry Guidelines PDF"
        ]
    },
    # ── 5. B2B SAAS SOFTWARE ACCESS & WHITELABEL ───────────────────────────
    "b2b_consultant_pro": {
        "name":        "B2B SaaS — Consultant Pro (Monthly)",
        "amount_inr":  2499,
        "original_price_inr": 4999,
        "amount_paise": 249900,
        "period":      "Monthly B2B SaaS",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "b2b",
        "description": "White-label calculation engine & branded PDF generation for professional astrologers and numerologists",
        "features": [
            "150 White-Label PDF Reports per month (Custom logo & branding)",
            "Sub-150ms deterministic Swiss Ephemeris & Numerology calculation",
            "Client management portal & historical chart database",
            "Overage: ₹15 per additional report"
        ]
    },
    "b2b_platform_growth": {
        "name":        "B2B SaaS — Platform Growth API (Monthly)",
        "amount_inr":  9999,
        "original_price_inr": 14999,
        "amount_paise": 999900,
        "period":      "Monthly API Access",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "b2b",
        "description": "High-volume REST API for matrimonial portals, dating apps, wellness startups, and HR recruiting platforms",
        "features": [
            "10,000 API calls per month included",
            "36-Point Ashtakoot Guna Milan + BNN Mars-Venus synergy endpoint",
            "Lo Shu compatibility & core matrix JSON response",
            "99.9% Uptime SLA with dedicated API key"
        ]
    },
    # Backwards-compatible aliases
    "starter": {
        "name":        "Starter — 5 Questions",
        "amount_inr":  95,
        "original_price_inr": 199,
        "amount_paise": 9500,
        "period":      "5 Questions",
        "questions_count": 5,
        "has_remedies": False,
        "description": "5 question predictions of any user queries",
        "features": ["5 In-depth Question Predictions", "ANVEIL EVERY CHARM Alignment & Timing"]
    },
    "growth": {
        "name":        "Growth — 10 Questions + Remedies",
        "amount_inr":  399,
        "original_price_inr": 599,
        "amount_paise": 39900,
        "period":      "10 Questions + Remedies",
        "questions_count": 10,
        "has_remedies": True,
        "description": "10 questions predictions with customized remedies for all 10 questions",
        "features": ["10 In-depth Question Predictions", "Custom Remedies for all 10 questions"]
    },
    "complete": {
        "name":        "Complete Reports & Remedies",
        "amount_inr":  1050,
        "original_price_inr": 1299,
        "amount_paise": 105000,
        "period":      "Complete Access",
        "questions_count": 9999,
        "has_remedies": True,
        "description": "Complete destiny reports and comprehensive remedies",
        "features": ["Complete Personal Destiny Blueprint Report", "Comprehensive Multi-Layer Remedies"]
    },
    "phone_consult": {
        "name":        "Phone Consultation",
        "amount_inr":  2499,
        "original_price_inr": 2499,
        "amount_paise": 249900,
        "period":      "one-time",
        "questions_count": 0,
        "has_remedies": True,
        "description": "45-minute personal numerology consultation via phone",
        "features": [
            "45-minute personal session",
            "WhatsApp confirmation within 2 hours",
            "Post-call remedy summary PDF",
        ]
    },
    "personal_consult": {
        "name":        "1-on-1 Master Personal Consultation",
        "amount_inr":  11400,
        "original_price_inr": 24000,
        "amount_paise": 1140000,
        "period":      "one-time (90 min)",
        "questions_count": 0,
        "has_remedies": True,
        "description": "90-minute exclusive 1-on-1 master session with Master Numerologist, complete life roadmap, birth epoch verification, and 30-day WhatsApp guidance",
        "features": [
            "90-minute private master consultation (Video or In-person)",
            "Birth Epoch Verification & deep multi-system chart synthesis",
            "Custom hand-crafted remedy plan, yantra & gemstone prescription",
            "30-day direct priority WhatsApp guidance with Master Numerologist",
            "Comprehensive Deluxe Destiny Dossier PDF report",
            "Full session recording & actionable milestone roadmap",
        ]
    },
    "vip_consult": {
        "name":        "1-on-1 Master Personal Consultation",
        "amount_inr":  11400,
        "original_price_inr": 24000,
        "amount_paise": 1140000,
        "period":      "one-time (90 min)",
        "questions_count": 0,
        "has_remedies": True,
        "description": "90-minute exclusive 1-on-1 master session with Master Numerologist",
        "features": [
            "90-minute private master consultation",
            "Complete chart synthesis & 30-day priority WhatsApp support",
        ]
    },
    "ai_growth_10q": {
        "name":        "Charm AI Growth Pack",
        "amount_inr":  399,
        "original_price_inr": 599,
        "amount_paise": 39900,
        "period":      "10 Questions + Remedies",
        "questions_count": 10,
        "has_remedies": True,
        "description": "10 questions predictions with customized remedies for all 10 questions",
        "features": ["10 In-depth Question Predictions", "Custom Remedies for all 10 questions"]
    },
    "sovereign_blueprint": {
        "name":        "Sovereign Life Blueprint",
        "amount_inr":  1050,
        "original_price_inr": 1299,
        "amount_paise": 105000,
        "period":      "Comprehensive Detailed Report",
        "questions_count": 9999,
        "has_remedies": True,
        "description": "Comprehensive 32-Page Detailed Life Blueprint Report & 10-Year Radar",
        "features": ["Complete Comprehensive Detailed Report (32 Pages)", "Calling Name vs Legal Name Harmonization", "10-Year Comprehensive Karmic Forecast"]
    },
    "master_consult": {
        "name":        "Bespoke VIP Consultation",
        "amount_inr":  11400,
        "original_price_inr": 24000,
        "amount_paise": 1140000,
        "period":      "90m Private Video Session",
        "questions_count": 0,
        "has_remedies": True,
        "description": "90-minute exclusive 1-on-1 master session with Master Numerologist, birth epoch verification, and 30-day WhatsApp guidance",
        "features": ["90m Private Video Session", "Birth Epoch Verification", "Custom Yantra Blueprint", "30 Days Priority WhatsApp Guidance"]
    },
    "bespoke_vip_consultation": {
        "name":        "Bespoke VIP Consultation",
        "amount_inr":  11400,
        "original_price_inr": 24000,
        "amount_paise": 1140000,
        "period":      "90m Private Video Session",
        "questions_count": 0,
        "has_remedies": True,
        "description": "90-minute exclusive 1-on-1 master session with Master Numerologist, birth epoch verification, and 30-day WhatsApp guidance",
        "features": ["90m Private Video Session", "Birth Epoch Verification", "Custom Yantra Blueprint", "30 Days Priority WhatsApp Guidance"]
    },
    # ── 6. LIFE RELATIONSHIP HARMONIC DOMAIN PACKAGES ──
    # Domain 1: Sacred Union & Spousal Bond (Harmonic Root 6 · Devotion & Opulence)
    "report_union_tripwire": {
        "name": "Marital Harmony Gap Unblocker",
        "amount_inr": 105,
        "original_price_inr": 330,
        "amount_paise": 10500,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "2-Page Quick Action Guide · Sacred Shagun Dakshina",
        "features": [
            "Thought-Action Relationship Plane Audit",
            "Immediate Spousal Harmony Checklist",
            "Sattvic Friday Attunement Ritual",
            "Lucky Direction & Color Vibration"
        ]
    },
    "report_union_master": {
        "name": "Sacred Union & Luxury Dossier",
        "amount_inr": 510,
        "original_price_inr": 1500,
        "amount_paise": 51000,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "12-Page Complete Dual-System Synthesis",
        "features": [
            "Full 12-Page Master Dossier with Gold Seals",
            "81-Pair Cosmic Synergy & Lo Shu 3x3 Grid",
            "Ishta Devata Sadhana & Consecrated Beej Mantra",
            "Annual Transit & Milestone Windows"
        ]
    },
    "report_union_sovereign": {
        "name": "Sovereign Couple Destiny Blueprint",
        "amount_inr": 5100,
        "original_price_inr": 10500,
        "amount_paise": 510000,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "35-Page Master Life & Marriage Synchronization",
        "features": [
            "Complete 35-Page Sovereign Life & Couple Blueprint",
            "Chaldean Legal & Calling Name Harmonization",
            "Dual Synastry Cross-Matching for Partners",
            "1-Year AI Question Credits Included"
        ]
    },
    # Domain 2: Commercial Velocity & Market Flow (Harmonic Root 5 · Commerce & Velocity)
    "report_commerce_tripwire": {
        "name": "Cash Flow Gap & Velocity Unblocker",
        "amount_inr": 149,
        "original_price_inr": 410,
        "amount_paise": 14900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "2-Page Rapid Financial Action Brief",
        "features": [
            "Missing Number 5 & Cash Drainage Audit",
            "Rapid Commercial Negotiation Timing Windows",
            "Wednesday Sattvic Green Attunement",
            "Desk Alignment for Financial Fluidity"
        ]
    },
    "report_commerce_master": {
        "name": "Commercial Mastery Dossier",
        "amount_inr": 599,
        "original_price_inr": 1499,
        "amount_paise": 59900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "12-Page Enterprise & Trade Synthesis",
        "features": [
            "Full 12-Page Master Dossier with Gold Seals",
            "Commercial Lo Shu Plane Alignment (4-5-6 & 2-5-8)",
            "Commercial Flow Beej Mantra & Consecrated Yantra Placement",
            "Annual Business Timing & Expansion Radar"
        ]
    },
    "report_commerce_sovereign": {
        "name": "Enterprise Scaling & Brand Matrix",
        "amount_inr": 5999,
        "original_price_inr": 14000,
        "amount_paise": 599900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "35-Page Full Commercial Architecture Blueprint",
        "features": [
            "Complete 35-Page Commercial Blueprint",
            "GST Entity Name & Brand Acoustic Sound Alignment",
            "Co-Founder & Key Investor Synergy Matrix",
            "1-Year AI Question Credits Included"
        ]
    },
    # Domain 3: Executive Authority & Career Sovereignty (Harmonic Root 1 · Executive Sovereignty)
    "report_authority_tripwire": {
        "name": "Career Authority Gap Unblocker",
        "amount_inr": 199,
        "original_price_inr": 370,
        "amount_paise": 19900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "2-Page Executive Elevation Brief",
        "features": [
            "Authority Alignment & Office Politics Neutralization",
            "Promotion & Performance Appraisal Windows",
            "Morning Solar Vitality & Water Consecration Guide",
            "Executive East Desk Facing Vector"
        ]
    },
    "report_authority_master": {
        "name": "Sovereign Leadership Dossier",
        "amount_inr": 550,
        "original_price_inr": 1450,
        "amount_paise": 55000,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "12-Page Executive Dual-System Synthesis",
        "features": [
            "Full 12-Page Master Dossier with Gold Seals",
            "81-Pair Cosmic Synergy & Lo Shu Will Plane",
            "Solar Gayatri & Authority Yantra Consecration",
            "5-Year Professional Career Dasha Radar"
        ]
    },
    "report_authority_sovereign": {
        "name": "Sovereign Identity & Name Rectification",
        "amount_inr": 5500,
        "original_price_inr": 10900,
        "amount_paise": 550000,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "35-Page Executive Life Transformation",
        "features": [
            "Complete 35-Page Sovereign Executive Blueprint",
            "Professional Name Spelling Rectification for Authority",
            "Public Stature & Government Career Roadmap",
            "1-Year AI Question Credits Included"
        ]
    },
    # Domain 4: Global Horizon & Relocation (Harmonic Root 5/6 · Global Passage)
    "report_relocation_tripwire": {
        "name": "International Visa & Travel Unblocker",
        "amount_inr": 149,
        "original_price_inr": 410,
        "amount_paise": 14900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "2-Page Foreign Movement Timing Guide",
        "features": [
            "Favorable Visa Lodgment & Submission Windows",
            "Compass Direction Alignment for Target Countries",
            "Travel Plane Neutralization for Delays",
            "Auspicious Departure Timing"
        ]
    },
    "report_relocation_master": {
        "name": "Global Settlement Dossier",
        "amount_inr": 510,
        "original_price_inr": 1500,
        "amount_paise": 51000,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "12-Page Overseas Relocation Synthesis",
        "features": [
            "Full 12-Page Master Dossier with Gold Seals",
            "Permanent Residency (PR) / Settlement Timeline",
            "Overseas Living & Relocation Vastu Vectors",
            "Annual International Opportunities Radar"
        ]
    },
    "report_relocation_sovereign": {
        "name": "Sovereign Global Migration Matrix",
        "amount_inr": 5100,
        "original_price_inr": 10500,
        "amount_paise": 510000,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "35-Page Full International Living Roadmap",
        "features": [
            "Complete 35-Page Sovereign Global Migration Matrix",
            "Passport Name Spelling & International Vibration",
            "Multi-Country Synastry & Relocation Mapping",
            "1-Year AI Question Credits Included"
        ]
    },
    # Domain 5: Higher Calling & Mentorship (Harmonic Root 3 · Higher Wisdom)
    "report_dharma_tripwire": {
        "name": "Dharma Compass & Purpose Unblocker",
        "amount_inr": 120,
        "original_price_inr": 390,
        "amount_paise": 12000,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "2-Page Life Calling & Clarity Guide",
        "features": [
            "Life Purpose & Core Natal Mission Alignment",
            "Spiritual Blockage & Confusion Neutralization",
            "Thursday Wisdom Sadhana & Yellow Attunement",
            "Wisdom Sanctuary & Meditation Orientation"
        ]
    },
    "report_dharma_master": {
        "name": "Sovereign Wisdom Dossier",
        "amount_inr": 570,
        "original_price_inr": 1200,
        "amount_paise": 57000,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "12-Page Soul Path & Sadhana Synthesis",
        "features": [
            "Full 12-Page Master Dossier with Gold Seals",
            "Thought & Spiritual Plane Lo Shu Integration",
            "Wisdom Beej Mantra & Consecrated Yantra Guide",
            "Ancestral Karma (Pitra) Balancing Protocol"
        ]
    },
    "report_dharma_sovereign": {
        "name": "Karmic Destiny & Life Blueprint",
        "amount_inr": 4800,
        "original_price_inr": 12000,
        "amount_paise": 480000,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "35-Page Full Spiritual Transformation",
        "features": [
            "Complete 35-Page Karmic Destiny Blueprint",
            "Spiritual Name Vibration & Acoustic Resonance",
            "Multi-Decade Soul Evolution & Dharma Timeline",
            "1-Year AI Question Credits Included"
        ]
    },

    # ── 7. SCREENSHOT-BASED REPORT CATALOGUE (18 PRODUCTS) ───────────────────
    # Group: Love and Marriage (Pricing Personality: 6)
    "report_love_style": {
        "name": "Love Style Report",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "icon": "💖",
        "description": "Explore your romantic expression, attachment archetype, and Venusian emotional harmony.",
        "features": [
            "Emotional & Romantic Frequency Analysis",
            "Venusian & Lunar Polarity Breakdown",
            "Love Attachment Style & Communication Needs",
            "Harmonizing Color & Crystal Recommendations"
        ]
    },
    "report_marriage": {
        "name": "Marriage Report",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "icon": "💍",
        "description": "Comprehensive marital alignment, timing windows, and domestic harmony blueprint.",
        "features": [
            "Marital Readiness & 7th House Axis Analysis",
            "Auspicious Marriage Timing & Dasha Windows",
            "Sacred Union Harmony & Long-term Bonding",
            "Marital Remedial Protocols (Vedic & Lo Shu)"
        ]
    },
    "report_ideal_partner": {
        "name": "Ideal Partner Report",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "icon": "🏹",
        "description": "Identify the psychological archetype, planetary ruler, and compatible vibration of your ideal partner.",
        "features": [
            "Soulmate Vibration & Karaka Significations",
            "Complementary Number Profiles (Driver & Conductor)",
            "Key Interpersonal Dynamics & Shared Values",
            "Red Flag Frequencies & Alignment Guidance"
        ]
    },
    "report_love_or_arrange": {
        "name": "Love or Arrange Exploration Report",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "icon": "⚖️",
        "description": "Evaluate classical indicators of self-chosen love vs traditional arranged marriage dynamics.",
        "features": [
            "5th vs 7th/9th House Influence Comparison",
            "Planetary Indicators for Self-Chosen vs Family Alliances",
            "Family Acceptance Potential & Parental Blessing Indicators",
            "Diplomatic Guidance for Navigating Marital Choices"
        ]
    },
    "report_spouse": {
        "name": "Spouse Personality & Life Alignment Report",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "icon": "👑",
        "description": "Detailed portrait of your future spouse's temperament, career inclination, and shared destiny.",
        "features": [
            "Spouse Temperament & Behavioral Archetype",
            "Likely Professional Domain & Social Standing",
            "Post-Marriage Fortune & Wealth Activation",
            "Harmonious Daily Habits & Relationship Care"
        ]
    },
    "report_in_laws": {
        "name": "In-Laws & Family Harmony Report",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Love and Marriage",
        "pricing_personality": 6,
        "icon": "🏡",
        "description": "Navigate relationships with extended family, in-laws, and domestic authority figures peacefully.",
        "features": [
            "In-Law Astrological House Influences (9th/10th from 7th)",
            "Potential Communication Friction Points & Solutions",
            "Vedic Vastu Directions for Family Harmony",
            "Boundary Setting & Diplomatic Grace Protocols"
        ]
    },

    # Group: Money (Pricing Personality: 1 or 6)
    "report_billionaire_potential": {
        "name": "Billionaire Potential & Wealth Blueprint",
        "amount_inr": 1499,
        "original_price_inr": 1999,
        "amount_paise": 149900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Money",
        "pricing_personality": 1,
        "icon": "💰",
        "description": "High-tier sovereign wealth architecture, multi-generational accumulation, and Dhana Yoga indicators.",
        "features": [
            "Dhana Yoga & Lakshmi Yoga Conjunction Audit",
            "Lo Shu Prosperity Plane (4-5-6) Golden Flow Evaluation",
            "High-Stakes Capital Deployment Windows",
            "Wealth Retention & Institutional Compounding Strategy"
        ]
    },
    "report_wealth": {
        "name": "Wealth & Abundance Report",
        "amount_inr": 699,
        "original_price_inr": 1299,
        "amount_paise": 69900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Money",
        "pricing_personality": 6,
        "icon": "💎",
        "description": "Practical financial liquidity, debt neutralization, and money vibration calibration.",
        "features": [
            "Personal Money Number & Cashflow Frequency",
            "Wealth Blockers & Leakage Identification",
            "Optimal Bank Account & Invoice Number Vibration",
            "Kuber Yantra & Directional Vastu Protocols"
        ]
    },

    # Group: Work (Pricing Personality: 1 or 5)
    "report_career": {
        "name": "Career Blueprint & Leadership Report",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Work",
        "pricing_personality": 1,
        "icon": "🎯",
        "description": "Comprehensive career trajectory, executive promotion timing, and corporate growth roadmap.",
        "features": [
            "10th House Institutional Authority Analysis",
            "Executive Leadership & Management Style",
            "Promotion & Band Advancement Timing Windows",
            "Workplace Friction Mitigation Strategies"
        ]
    },
    "report_business": {
        "name": "Business Alignment & Commercial Direction Report",
        "amount_inr": 1499,
        "original_price_inr": 1999,
        "amount_paise": 149900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Work",
        "pricing_personality": 1,
        "icon": "🏢",
        "description": "Evaluate commercial venture viability, market timing, founder archetype, and scalability.",
        "features": [
            "Founder Archetype & Industry Domain Synergy",
            "Auspicious Venture Incorporation Windows",
            "Partnership Synastry & Capital Risk Assessment",
            "Commercial Brand Name Numerical Balancing"
        ]
    },
    "report_job_or_business": {
        "name": "Job or Business Decision Dossier",
        "amount_inr": 699,
        "original_price_inr": 1299,
        "amount_paise": 69900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Work",
        "pricing_personality": 5,
        "icon": "🔄",
        "description": "Resolve the foundational dilemma: executive employment stability vs independent enterprise freedom.",
        "features": [
            "Service (6th House) vs Enterprise (7th/10th House) Balance",
            "Autonomy Readiness Score & Risk Tolerance Audit",
            "Optimal Transition Timing & Phased Pivoting Protocol",
            "Moonlighting & Side-Venture Safety Guidelines"
        ]
    },
    "report_govt_job": {
        "name": "Govt Job & Administrative Exam Alignment Report",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Work",
        "pricing_personality": 1,
        "icon": "🏛️",
        "description": "Assess Sun/Surya and Saturn authority indicators for public sector, civil service, and competitive exams.",
        "features": [
            "Sovereign Authority & Government Favor Indicators",
            "Competitive Examination Focus & Success Windows",
            "Judiciary, Defense, and Administrative Aptitude",
            "Sun Arghya & Gayatri Remedial Activation"
        ]
    },
    "report_first_job": {
        "name": "First Job & Graduate Career Starter Report",
        "amount_inr": 199,
        "original_price_inr": 399,
        "amount_paise": 19900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Work",
        "pricing_personality": 1,
        "icon": "🚀",
        "description": "Essential guidance for students, fresh graduates, and entry-level professionals embarking on work life.",
        "features": [
            "Natural Workplace Superpowers & First-Job Roles",
            "Interview Presentation & Resume Energy Alignment",
            "Overcoming Early Career Imposter Syndrome",
            "Auspicious Joining Dates & Morning Centering Habits"
        ]
    },
    "report_job_search": {
        "name": "Job Search & Career Transition Strategy Report",
        "amount_inr": 199,
        "original_price_inr": 399,
        "amount_paise": 19900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Work",
        "pricing_personality": 5,
        "icon": "🔍",
        "description": "Actionable tactical guide to accelerate pending interview callbacks, headhunter outreach, and offers.",
        "features": [
            "Active Dasha Timing for Applications & Interviews",
            "Resume Keyword Energy & Calling Signature",
            "Interview Day Planetary Hora Selection",
            "Stuck Momentum Grounding Rituals"
        ]
    },

    # Group: Self and Growth (Pricing Personality: 1 or 3)
    "report_intelligence": {
        "name": "Intelligence & Cognitive Mastery Report",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Self and Growth",
        "pricing_personality": 3,
        "icon": "🧠",
        "description": "Discover your unique intellectual wiring: strategic, analytical, creative, or intuitive cognition.",
        "features": [
            "Cognitive Modality & Mental Processing Speed",
            "Mercury-Jupiter Intellect Conjunction Dynamics",
            "Optimal Learning Environments & Study Hours",
            "Memory Enhancement & Mental Fatigue Clearing"
        ]
    },
    "report_life_guidance": {
        "name": "Life Guidance & Sovereign Purpose Dossier",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Self and Growth",
        "pricing_personality": 1,
        "icon": "🧭",
        "description": "Clear life direction, moral compass, and soul lesson navigation across your current decade.",
        "features": [
            "Soul Calling & Core Ethical Mission Blueprint",
            "Karmic Lessons & Repetitive Life Patterns",
            "Navigating Major Mid-Life & Saturnian Milestones",
            "Daily Centering & Spiritual Grounding Practices"
        ]
    },
    "report_personality": {
        "name": "Personality Archetype & Soul Expression Report",
        "amount_inr": 199,
        "original_price_inr": 399,
        "amount_paise": 19900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Self and Growth",
        "pricing_personality": 3,
        "icon": "✨",
        "description": "Deep dive into your outer projection, inner temperament, and unconscious psychological drivers.",
        "features": [
            "Driver/Conductor Behavioral Polarity Analysis",
            "Public Aura vs Private Self Dynamics",
            "Natural Charisma & Persuasion Strengths",
            "Blindspot Neutralization & Personal Poise"
        ]
    },
    "report_education": {
        "name": "Education & Academic Mastery Report",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "category_group": "Self and Growth",
        "pricing_personality": 3,
        "icon": "🎓",
        "description": "Academic stream selection, higher education timing, exam focus, and foreign study prospects.",
        "features": [
            "Auspicious Academic Disciplines & University Fields",
            "Foreign Education & Overseas Degree Prospects",
            "Exam Pacing & Retention Enhancement",
            "Saraswati Beej Mantra & Study Space Vastu"
        ]
    },

    # ── 8. REPORT BUNDLES (8 VALUE SETS) ──────────────────────────────────────
    "bundle_love_compatibility": {
        "name": "Love & Compatibility Set",
        "amount_inr": 1499,
        "original_price_inr": 1999,
        "amount_paise": 149900,
        "period": "Instant Bundle Access",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "pricing_personality": 6,
        "included_reports": ["report_love_style", "report_ideal_partner", "report_marriage"],
        "description": "Complete romantic journey package: Love Style, Ideal Partner profile, and Marriage timing blueprint.",
        "features": [
            "3 Comprehensive PDF Reports (Love Style, Ideal Partner, Marriage)",
            "Combined Venusian & Spousal Synastry Breakdown",
            "Save ₹500 off the bundle list price",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_marriage_family": {
        "name": "Marriage & Family Harmony Set",
        "amount_inr": 1499,
        "original_price_inr": 1999,
        "amount_paise": 149900,
        "period": "Instant Bundle Access",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "pricing_personality": 6,
        "included_reports": ["report_marriage", "report_spouse", "report_in_laws"],
        "description": "Total marital and domestic serenity package: Marriage readiness, Spouse personality, and In-laws harmony.",
        "features": [
            "3 Comprehensive PDF Reports (Marriage, Spouse, In-Laws)",
            "Extended Family Vastu & Communication Protocol",
            "Save ₹500 off the bundle list price",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_career_starter": {
        "name": "Career Starter Set",
        "amount_inr": 699,
        "original_price_inr": 1299,
        "amount_paise": 69900,
        "period": "Instant Bundle Access",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "pricing_personality": 1,
        "included_reports": ["report_first_job", "report_job_search", "report_career"],
        "description": "Essential stepping stones for early career professionals: First Job, Job Search tactics, and Career blueprint.",
        "features": [
            "3 Practical PDF Reports (First Job, Job Search, Career)",
            "Interview Timing & Resume Calibration Guides",
            "Save ₹600 (46% off) compared to bundle list price",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_career_decision": {
        "name": "Career Decision Set",
        "amount_inr": 1999,
        "original_price_inr": 2499,
        "amount_paise": 199900,
        "period": "Instant Bundle Access",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "pricing_personality": 1,
        "included_reports": ["report_career", "report_business", "report_job_or_business"],
        "description": "Definitive career crossroads package: Career leadership, Business venture feasibility, and Job vs Business.",
        "features": [
            "3 Comprehensive PDF Reports (Career, Business, Job or Business)",
            "Executive Transition & Corporate Autonomy Roadmap",
            "Save ₹500 off the bundle list price (Save ₹598 over individual offers)",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_money_wealth": {
        "name": "Money & Wealth Set",
        "amount_inr": 1999,
        "original_price_inr": 2499,
        "amount_paise": 199900,
        "period": "Instant Bundle Access",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "pricing_personality": 6,
        "included_reports": ["report_wealth", "report_billionaire_potential"],
        "description": "Total financial mastery package: Wealth cashflow management and Sovereign Billionaire Potential blueprint.",
        "features": [
            "2 Elite Financial PDF Reports (Wealth, Billionaire Potential)",
            "Dhana Yoga & Cashflow Leakage Remediation",
            "Save ₹500 off bundle list (Save ₹199 over individual offers)",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_self_discovery": {
        "name": "Self-Discovery Set",
        "amount_inr": 1499,
        "original_price_inr": 1999,
        "amount_paise": 149900,
        "period": "Instant Bundle Access",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "pricing_personality": 3,
        "included_reports": ["report_personality", "report_intelligence", "report_life_guidance"],
        "description": "Profound inner alignment package: Personality archetype, Cognitive intelligence, and Sovereign life guidance.",
        "features": [
            "3 In-Depth Personal PDF Reports (Personality, Intelligence, Life Guidance)",
            "Cognitive Wiring & Soul Purpose Alignment",
            "Save ₹500 off the bundle list price",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_learning_growth": {
        "name": "Learning & Growth Set",
        "amount_inr": 1499,
        "original_price_inr": 1999,
        "amount_paise": 149900,
        "period": "Instant Bundle Access",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "pricing_personality": 3,
        "included_reports": ["report_education", "report_intelligence", "report_personality"],
        "description": "Intellectual mastery package: Academic achievement, Intellectual aptitude, and Personality strengths.",
        "features": [
            "3 Focused Educational PDF Reports (Education, Intelligence, Personality)",
            "Study Vastu & Academic Timing Calendars",
            "Save ₹500 off the bundle list price",
            "Archival PDF download access in your account dashboard"
        ]
    },
    "bundle_complete_personal_insight": {
        "name": "Complete Personal Insight Set",
        "amount_inr": 2499,
        "original_price_inr": 3999,
        "amount_paise": 249900,
        "period": "All-Access Dossier Suite",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "pricing_personality": 3,
        "included_reports": [
            "report_love_style", "report_marriage", "report_ideal_partner", "report_love_or_arrange",
            "report_spouse", "report_in_laws", "report_billionaire_potential", "report_wealth",
            "report_career", "report_business", "report_job_or_business", "report_govt_job",
            "report_first_job", "report_job_search", "report_intelligence", "report_life_guidance",
            "report_personality", "report_education"
        ],
        "description": "All-inclusive master suite: Archival access to all Numeros Vision reports.",
        "features": [
            "All 18 Numeros Vision Personalized PDF Reports Included",
            "Love, Wealth, Work, and Self Growth full libraries",
            "Save ₹1,500 off bundle list (Huge savings over individual purchases)",
            "Archival access to your purchased editions"
        ]
    },

    # ── 9. CHARM AI CONVERSATIONAL PACKAGES (6 TIERS) ─────────────────────────
    "charm_quick_insight": {
        "name": "Charm AI — Quick Insight",
        "amount_inr": 199,
        "original_price_inr": 399,
        "amount_paise": 19900,
        "period": "1 Focused Question",
        "questions_count": 1,
        "has_remedies": True,
        "category": "charm_package",
        "pricing_personality": 1,
        "scope": "One clearly defined focused question and concise master consultation answer.",
        "description": "One targeted question prediction with instant grounded clarity and unblocking next steps.",
        "features": [
            "1 Focused Charm AI Master Consultation Turn",
            "Empathetic Golden Heart dialogue & diagnosis",
            "Grounding unblocking practical actions",
            "Valid across Career, Love, Wealth or Health"
        ]
    },
    "charm_focused_reading": {
        "name": "Charm AI — Focused Reading",
        "amount_inr": 399,
        "original_price_inr": 699,
        "amount_paise": 39900,
        "period": "4 Questions Allowance",
        "questions_count": 4,
        "has_remedies": True,
        "category": "charm_package",
        "pricing_personality": 3,
        "scope": "One topic with a defined follow-up allowance and structured summary.",
        "description": "Deep-dive inquiry into a single life challenge with up to 3 follow-up clarifying questions.",
        "features": [
            "4 Dedicated Charm AI Consultation Turns",
            "In-depth topic exploration with follow-up allowance",
            "Structured summary & timing window breakdown",
            "Custom 7-Layer safe lifestyle remedies"
        ]
    },
    "charm_consensus_reading": {
        "name": "Charm AI — Consensus Reading",
        "amount_inr": 699,
        "original_price_inr": 1299,
        "amount_paise": 69900,
        "period": "8 Questions + Cross-Verification",
        "questions_count": 8,
        "has_remedies": True,
        "category": "charm_package",
        "pricing_personality": 5,
        "scope": "One topic evaluated across eligible, enabled and validated traditions.",
        "description": "Rigorous cross-verification comparing Numerology Dasha against KP, Vedic Parashari, and BNN.",
        "features": [
            "8 In-depth Charm AI Consultation Turns",
            "Deterministic multi-system consensus evaluation",
            "Citations from verified Numeros Vision classical corpus",
            "Strict status badge (CORROBORATED / CONFLICTED / ONLY)"
        ]
    },
    "charm_personal_blueprint": {
        "name": "Charm AI — Personal Blueprint",
        "amount_inr": 1499,
        "original_price_inr": 1999,
        "amount_paise": 149900,
        "period": "20 Questions Allowance",
        "questions_count": 20,
        "has_remedies": True,
        "category": "charm_package",
        "pricing_personality": 1,
        "scope": "Multi-topic analysis using only actually supported features.",
        "description": "Full life-aspect exploration spanning career pivots, marital timing, and financial security.",
        "features": [
            "20 Comprehensive Charm AI Consultation Turns",
            "Multi-topic coverage (Career, Wealth, Relationships, Health)",
            "Annual Personal Year transit and hora timing radar",
            "Downloadable summary transcript of full consultation"
        ]
    },
    "charm_family_compatibility": {
        "name": "Charm AI — Family Compatibility",
        "amount_inr": 699,
        "original_price_inr": 1299,
        "amount_paise": 69900,
        "period": "8 Questions (Multi-Profile)",
        "questions_count": 8,
        "has_remedies": True,
        "category": "charm_package",
        "pricing_personality": 6,
        "scope": "Compatibility themes for user-supplied profiles with appropriate consent.",
        "description": "Interactive dual-profile synastry consultation exploring partner, family, or business synergy.",
        "features": [
            "8 Dual-Profile Charm AI Consultation Turns",
            "Driver/Conductor polarity and shared Lo Shu plane audit",
            "Interpersonal friction mitigation and communication advice",
            "Complies strictly with statutory DPDP 2023 consent"
        ]
    },
    "charm_career_business_direction": {
        "name": "Charm AI — Career & Business Direction",
        "amount_inr": 699,
        "original_price_inr": 1299,
        "amount_paise": 69900,
        "period": "8 Focused Career Turns",
        "questions_count": 8,
        "has_remedies": True,
        "category": "charm_package",
        "pricing_personality": 1,
        "scope": "Career/business exploration and practical next-step prompts.",
        "description": "Dedicated corporate and commercial guidance for job transitions, appraisal timing, or founder pivots.",
        "features": [
            "8 Strategic Career & Business Turns",
            "Acute execution window mapping (Pratyantardasha)",
            "3-point practical outreach & workspace grounding actions",
            "Zero ungrounded speculation or commercial guarantees"
        ]
    },
}

# ── Persistent verified-payment session store ──────────────────────────────
_verified_payments: dict = {}

# Cloud-Native Distributed Session Cache (Redis)
REDIS_URL = os.getenv("REDIS_URL")
_redis_client = None
if REDIS_URL:
    try:
        import redis
        _redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    except Exception:
        _redis_client = None

def _load_sessions():
    """Load persisted verified sessions from disk on startup."""
    global _verified_payments
    try:
        if os.path.exists(SESSIONS_FILE):
            with open(SESSIONS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    _verified_payments.update(data)
    except Exception:
        pass

def _save_sessions(session_token: Optional[str] = None):
    """Persist verified sessions to disk atomically and sync to Redis if available."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(SESSIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(_verified_payments, f, indent=2)
    except Exception:
        pass

    if _redis_client and session_token and session_token in _verified_payments:
        try:
            _redis_client.set(
                f"session:{session_token}",
                json.dumps(_verified_payments[session_token]),
                ex=86400 * 30  # 30-day session TTL
            )
        except Exception:
            pass

# Initialize on module import
_load_sessions()

def get_session_info(token: str) -> Optional[dict]:
    """Retrieve session info for a given premium/subscription token."""
    if not token:
        return None
    # Local QA test tokens — unconditionally rejected in production and preview
    if token in ("test_master_pass", "test_token", "demo_mode", "admin_test") or token.startswith("test_"):
        env_mode = os.getenv("ENVIRONMENT", "development").lower()
        if env_mode in ("production", "preview"):
            return None
        allow_test = (
            env_mode in ("development", "test", "local")
            or os.getenv("ALLOW_TEST_TOKENS", "false").lower() == "true"
        )
        if not allow_test:
            return None

        return {
            "token": token,
            "plan": "complete_report",
            "plan_name": "Complete Reports & Remedies (Test Access)",
            "questions_remaining": 9999,
            "has_remedies": True,
            "has_btr": True,
            "verified_at": int(time.time()),
            "status": "active"
        }
    if _redis_client:
        try:
            cached = _redis_client.get(f"session:{token}")
            if cached:
                return json.loads(cached)
        except Exception:
            pass
    return _verified_payments.get(token)

def consume_question(token: str) -> bool:
    """Consume 1 question from the quota if available and persist."""
    session = get_session_info(token)
    if not session:
        return False
    # If unlimited (complete plan has 9999)
    if session.get("questions_remaining", 0) > 0:
        session["questions_remaining"] -= 1
        _verified_payments[token] = session
        _save_sessions(token)
        return True
    return False

def record_question_history(token: str, question: str, answer_summary: str = "", topic: str = ""):
    """Record question and answer into session memory for multi-turn conversational context."""
    session = get_session_info(token)
    if not session:
        return
    if "question_history" not in session:
        session["question_history"] = []
    session["question_history"].append({
        "question": question,
        "topic": topic,
        "answer_summary": answer_summary[:300] if answer_summary else "",
        "timestamp": int(time.time())
    })
    _verified_payments[token] = session
    _save_sessions(token)

# ── Request models ─────────────────────────────────────────────────────────
class CreateOrderRequest(BaseModel):
    plan: Optional[str] = None
    plan_id: Optional[str] = None
    name: Optional[str] = ""
    customer_name: Optional[str] = ""
    email: Optional[str] = ""
    customer_email: Optional[str] = ""
    mobile: Optional[str] = ""
    customer_phone: Optional[str] = ""
    amount: Optional[int] = None
    amount_inr: Optional[int] = None
    currency: Optional[str] = "INR"
    receipt: Optional[str] = None

class VerifyPaymentRequest(BaseModel):
    razorpay_order_id:   Optional[str] = None
    razorpay_payment_id: Optional[str] = None
    razorpay_signature:  Optional[str] = None
    plan: Optional[str] = None
    plan_id: Optional[str] = None
    email: Optional[str] = ""
    customer_name: Optional[str] = ""
    customer_phone: Optional[str] = ""

class AlignmentGapRequest(BaseModel):
    driver: Optional[int] = 1
    conductor: Optional[int] = 1
    loshu_counts: Optional[Dict[str, int]] = None
    missing_numbers: Optional[List[int]] = None
    name_number: Optional[int] = None
    personal_year: Optional[int] = None
    active_dasha: Optional[str] = None
    current_plan: Optional[str] = "free"
    credits_remaining: Optional[int] = 0
    token: Optional[str] = None

class FunnelNextStepRequest(BaseModel):
    product_id: Optional[str] = "birth_number"
    calculation_completed: Optional[bool] = False
    free_result_available: Optional[bool] = False
    token: Optional[str] = None
    opted_out: Optional[bool] = False

class PriceValidationRequest(BaseModel):
    reference: Optional[int] = None
    offer: Optional[int] = None
    amount: Optional[int] = None

class FunnelEventRequest(BaseModel):
    event: str
    product_id: Optional[str] = None
    stage: Optional[str] = None
    session_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


PLAN_COVERAGE_HIERARCHY = {
    "complete_report": {
        "complete_report", "complete", "report_master", "report_essential", "report_divine",
        "starter_5q", "starter", "growth_10q", "growth", "free", "discovery"
    },
    "report_divine": {
        "report_divine", "report_master", "report_essential", "complete_report", "free", "discovery"
    },
    "report_master": {
        "report_master", "report_essential", "free", "discovery"
    },
    "report_essential": {
        "report_essential", "free", "discovery"
    },
    "growth_10q": {
        "growth_10q", "growth", "starter_5q", "starter", "free", "discovery"
    },
    "starter_5q": {
        "starter_5q", "starter", "free", "discovery"
    },
    "ai_power_35q": {
        "ai_power_35q", "ai_growth_15q", "ai_starter_5q", "free", "discovery"
    },
    "ai_growth_15q": {
        "ai_growth_15q", "ai_starter_5q", "free", "discovery"
    },
    "ai_starter_5q": {
        "ai_starter_5q", "free", "discovery"
    }
}


def check_report_access(
    requested_tier: str,
    token: Optional[str] = None,
    user_id: Optional[str] = None,
    request: Optional[Request] = None
) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
    """
    Gatekeeper for report tiers (Rules 2 & 3):
    1. Free tier is always accessible.
    2. Staging replica mode bypasses paywall for complete QA/QC testing.
    3. Paid tiers check active session token or registered user profile entitlements.
    4. If denied, generates personalized gap analysis and 'ANVEIL EVERY CHARM' CTA.
    """
    clean_tier = requested_tier.lower().strip()
    if clean_tier in ("free", "discovery"):
        return True, "free_tier", None

    # Check Staging Replica Mode bypass
    if request:
        headers = dict(request.headers)
        params = dict(request.query_params)
        if is_staging_bypass_authorized(headers, params, token):
            return True, "staging_replica_bypass", {"staging_mode": True}

    # Check Verified Payment Session
    session = get_session_info(token) if token else None
    if session:
        session_plan = session.get("plan", "")
        covered = PLAN_COVERAGE_HIERARCHY.get(session_plan, {session_plan})
        if clean_tier in covered or session_plan == clean_tier:
            return True, "session_authorized", session

    # Check Registered User Account Entitlements
    user = None
    if user_id:
        user = get_user_account_by_identifier(user_id)
    elif token and token in _ACTIVE_SESSIONS:
        auth_sess = _ACTIVE_SESSIONS[token]
        uid = auth_sess.get("user_id")
        user = _USER_ACCOUNTS.get(uid) if uid else None

    if user:
        unlocked = user.get("unlocked_reports", [])
        if clean_tier in unlocked:
            return True, "user_unlocked_report", user
        for plan in user.get("purchased_plans", []):
            covered = PLAN_COVERAGE_HIERARCHY.get(plan, {plan})
            if clean_tier in covered:
                return True, "user_purchased_plan_covered", user

    # Access Denied: User has not purchased this report tier
    d = user.get("driver_mulank", 1) if user else 1
    c = user.get("conductor_bhagyank", 1) if user else 1
    loshu = user.get("loshu_counts", {}) if user else {}
    missing = user.get("missing_numbers", []) if user else []

    gap_data = analyze_user_alignment_and_gaps(
        driver=d,
        conductor=c,
        loshu_counts=loshu,
        missing_numbers=missing,
        current_plan="free"
    )

    return False, "PAYMENT_REQUIRED", gap_data


# ── Endpoints ──────────────────────────────────────────────────────────────


@router.get("/pricing-catalog")
@api_router.get("/v1/pricing-catalog")
def get_pricing_catalog():
    """Returns authoritative server-side pricing catalog including feature_flags."""
    from app.config.pricing_config import export_pricing_catalog_json
    return json.loads(export_pricing_catalog_json())


class NotifyMeWaitlistRequest(BaseModel):
    email: str
    pack_id: Optional[str] = None
    sku_id: Optional[str] = None
    consent: bool = False
    purpose: Optional[str] = None
    consent_text: Optional[str] = None
    source_page: Optional[str] = "your_reading"


class NotifyMeDeleteRequest(BaseModel):
    email: str
    pack_id: Optional[str] = None
    sku_id: Optional[str] = None


def _normalize_notify_pack(pack_id: str) -> Optional[str]:
    from app.services.waitlist_service import normalize_waitlist_pack_id
    return normalize_waitlist_pack_id(pack_id)


@router.post("/waitlist/notify-me")
@api_router.post("/v1/waitlist/notify-me")
def register_notify_me_waitlist(req: NotifyMeWaitlistRequest):
    """
    Captures DPDP-consented launch notification requests for Advanced/Premium tiers.
    Stores email encrypted with AES-256-GCM (`ivHex:cipherHex`), explicit DPDP consent
    text, stated purpose ("tell me when this report is available"), and 12-month retention.
    Uses `email_sha256` strictly for de-duplication.
    """
    from app.services.waitlist_service import upsert_waitlist_record

    os.makedirs(DATA_DIR, exist_ok=True)
    waitlist_file = os.path.join(DATA_DIR, "waitlist_notify_me.jsonl")
    try:
        return upsert_waitlist_record(
            email=req.email,
            pack_id=req.pack_id or req.sku_id or "",
            consent=req.consent,
            purpose=req.purpose,
            consent_text=req.consent_text,
            source_page=req.source_page or "your_reading",
            storage_path=waitlist_file,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/waitlist/notify-me/delete")
@api_router.post("/v1/waitlist/notify-me/delete")
@router.delete("/waitlist/notify-me")
@api_router.delete("/v1/waitlist/notify-me")
def delete_notify_me_waitlist(req: NotifyMeDeleteRequest):
    """
    DPDP 2023 delete-on-request path: permanently erases stored encrypted email records
    matching the requester's email address (optionally scoped to a specific pack_id).
    """
    from app.services.waitlist_service import delete_waitlist_records

    os.makedirs(DATA_DIR, exist_ok=True)
    waitlist_file = os.path.join(DATA_DIR, "waitlist_notify_me.jsonl")
    try:
        return delete_waitlist_records(
            email=req.email,
            pack_id=req.pack_id or req.sku_id,
            storage_path=waitlist_file,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@api_router.get("/v1/public/loshu-teasers")
def get_public_loshu_teasers():
    """Serves sanitized, browser-safe Lo Shu curiosity teasers (zero paid report prose)."""
    teaser_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "static", "data", "loshu_public_teasers.json")
    )
    if not os.path.exists(teaser_path):
        raise HTTPException(status_code=404, detail="Public Lo Shu teaser slice not found.")
    with open(teaser_path, "r", encoding="utf-8") as fh:
        return json.load(fh)

@router.get("/plans")
def get_plans():
    """Return public pricing catalogue — no auth required."""
    # Exclude internal backwards-compatibility aliases
    excluded_aliases = {"starter", "growth", "complete", "vip_consult"}
    
    formatted_plans = {}
    for k, v in PLANS.items():
        if k in excluded_aliases:
            continue
        orig = v.get("original_price_inr", v["amount_inr"])
        offer = v["amount_inr"]
        formatted_plans[k] = {
            "name":               v["name"],
            "amount_inr":         offer,
            "original_price_inr": orig,
            "amount_paise":       v.get("amount_paise", offer * 100),
            "period":             v["period"],
            "questions_count":    v.get("questions_count", 0),
            "has_remedies":       v.get("has_remedies", False),
            "category":           v.get("category", "consultation"),
            "category_group":     v.get("category_group", ""),
            "pricing_personality": v.get("pricing_personality"),
            "list_price_root":    digit_root(orig) if orig > 0 else 0,
            "offer_price_root":   digit_root(offer) if offer > 0 else 0,
            "included_reports":   v.get("included_reports", []),
            "icon":               v.get("icon", "📜"),
            "scope":              v.get("scope", ""),
            "savings_inr":        orig - offer if orig > offer else 0,
            "discount_percent":   round(((orig - offer) / orig) * 100) if orig > offer else 0,
            "description":        v.get("description", ""),
            "features":           v.get("features", []),
        }

    return {
        "status": "success",
        "success": True,
        "plans": formatted_plans,
        "currency": "INR",
        "razorpay_key": RAZORPAY_KEY_ID,   # public key — safe to expose to frontend
    }


@router.post("/alignment-gap-analysis")
async def get_alignment_gap_analysis(req: AlignmentGapRequest, request: Request):
    """
    Rule 1 & 2: Deterministic Alignment & Gap Analysis Endpoint.
    Analyzes driver-conductor alignment, Lo Shu missing planes (Golden Plane 4-5-6),
    and generates personalized conversion hooks with 'ANVEIL EVERY CHARM' CTAs.
    """
    driver = req.driver or 1
    conductor = req.conductor or 1
    loshu_counts = req.loshu_counts or {}
    missing_numbers = req.missing_numbers or []
    current_plan = req.current_plan or "free"
    credits_remaining = req.credits_remaining or 0

    token = req.token or request.cookies.get("nv_user_session")
    if token and token in _ACTIVE_SESSIONS:
        sess = _ACTIVE_SESSIONS[token]
        user = _USER_ACCOUNTS.get(sess.get("user_id"))
        if user:
            driver = user.get("driver_mulank", driver)
            conductor = user.get("conductor_bhagyank", conductor)
            loshu_counts = user.get("loshu_counts", loshu_counts)
            missing_numbers = user.get("missing_numbers", missing_numbers)
            credits_remaining = user.get("charm_credits_remaining", credits_remaining)
            purchased = user.get("purchased_plans", [])
            current_plan = purchased[-1] if purchased else "free"

    analysis = analyze_user_alignment_and_gaps(
        driver=driver,
        conductor=conductor,
        loshu_counts=loshu_counts,
        missing_numbers=missing_numbers,
        name_number=req.name_number,
        personal_year=req.personal_year,
        active_dasha=req.active_dasha,
        current_plan=current_plan,
        credits_remaining=credits_remaining
    )
    return analysis


@api_router.get("/planner-2027/price")
def get_planner_2027_price_endpoint():
    """Returns server-side status for 2027 Planner (waitlist-only with zero price until PLANNER_2027_LIVE=true)."""
    from app.config.planner_2027_pricing import get_planner_2027_price
    return get_planner_2027_price()


@api_router.post("/planner-2027/order")
async def create_planner_2027_order_endpoint(request: Request):
    """Server-side guard blocking 2027 Planner order creation until statutory disclaimer is approved."""
    from app.config.planner_2027_pricing import is_planner_2027_live
    if not is_planner_2027_live():
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "code": "PLANNER_WAITLIST_ONLY",
                "error": "Coming soon, notify me. The 2027 Year Ahead Numerology Planner is currently waitlist-only until statutory disclaimer approval.",
                "waitlist_pack_id": "planner_2027",
            },
        )
    body = await request.json()
    order_req = CreateOrderRequest(
        plan="planner_2027",
        name=body.get("full_name") or body.get("name"),
        email=body.get("email"),
        mobile=body.get("phone") or body.get("mobile"),
    )
    return await create_order(order_req)


@router.post("/create-order")
async def create_order(req: CreateOrderRequest):
    """
    Razorpay Standard Web Checkout - Step 1: Create Order.
    Calls Razorpay Orders API: POST https://api.razorpay.com/v1/orders
    Validates minimum amount (>= 100 paise) and handles authentication / API errors.
    """
    from app.config.planner_2027_pricing import is_planner_2027_live

    plan_key = req.plan or req.plan_id or "report_basic"
    norm_pack = _normalize_notify_pack(plan_key)
    if norm_pack == "planner_2027" and not is_planner_2027_live():
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "code": "PLANNER_WAITLIST_ONLY",
                "detail": "Coming soon, notify me. The 2027 Year Ahead Numerology Planner is currently waitlist-only until statutory disclaimer approval.",
                "waitlist_pack_id": "planner_2027",
            },
        )
    if is_notify_me_higher_tiers_enabled() and norm_pack in ("report_advanced", "report_premium"):
        return JSONResponse(
            status_code=409,
            content={
                "success": False,
                "code": "TIER_WAITLIST_ONLY",
                "detail": "Coming soon, notify me. This report edition is currently waitlist-only; Anveil my alignments is open for immediate checkout."
            }
        )

    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    if not key_id or not key_secret:
        raise HTTPException(
            status_code=500,
            detail="Razorpay payment gateway credentials not configured in server environment."
        )

    plan_name = "Personal Numerology Report"
    plan_amount_paise = None
    plan_amount_inr = None

    # Authoritative Server-Side Product Pricing (never trust frontend amounts; resolves launch vs regular via env window)
    resolved_sku = resolve_sku_price(plan_key)
    if resolved_sku and resolved_sku.get("amount_inr") is not None:
        plan_amount_inr = int(resolved_sku["amount_inr"])
        plan_amount_paise = int(resolved_sku.get("amount_paise") or (plan_amount_inr * 100))
        plan_name = resolved_sku.get("name", plan_key)
    elif plan_key in PLANS:
        plan = PLANS[plan_key]
        plan_amount_inr = plan["amount_inr"]
        plan_amount_paise = plan.get("amount_paise", plan_amount_inr * 100)
        plan_name = plan["name"]
    else:
        plan_amount_inr = 399
        plan_amount_paise = 39900

    if plan_amount_paise < 100:
        raise HTTPException(status_code=400, detail="Amount must be at least 100 paise (₹1.00)")

    customer_name = req.name or req.customer_name or "Valued Seeker"
    customer_email = req.email or req.customer_email or ""
    customer_mobile = req.mobile or req.customer_phone or ""
    receipt = req.receipt or f"nv_{plan_key}_{int(time.time())}"
    currency = req.currency or "INR"

    # Call Razorpay Orders API via SDK
    try:
        import razorpay
        import razorpay.errors
        client = razorpay.Client(auth=(key_id, key_secret))
        order = client.order.create({
            "amount":          plan_amount_paise,
            "currency":        currency,
            "receipt":         receipt,
            "payment_capture": 1,
            "notes": {
                "plan":   plan_key,
                "name":   customer_name,
                "email":  customer_email,
                "mobile": customer_mobile,
            }
        })
        order_id = order["id"]
    except Exception as e:
        err_str = str(e).lower()
        if "auth" in err_str or "unauthorized" in err_str:
            raise HTTPException(status_code=401, detail=f"Razorpay authentication failed: {str(e)}")
        if "bad request" in err_str:
            raise HTTPException(status_code=400, detail=f"Razorpay rejected order parameters: {str(e)}")
        # If network error or mock fallback needed
        raise HTTPException(status_code=500, detail=f"Failed to create Razorpay order: {str(e)}")

    return {
        "order_id":    order_id,
        "amount":      plan_amount_paise,
        "amount_inr":  plan_amount_inr,
        "currency":    currency,
        "plan":        plan_key,
        "plan_name":   plan_name,
        "key_id":      key_id,
        "key":         key_id,
        "name":        customer_name,
        "email":       customer_email,
        "mobile":      customer_mobile,
        "receipt":     receipt
    }


@router.post("/create-order")
async def router_create_order(req: CreateOrderRequest):
    return await create_order(req)


@api_router.post("/create-order")
async def api_create_order(req: CreateOrderRequest):
    return await create_order(req)


@router.post("/verify")
async def verify_payment(req: VerifyPaymentRequest):
    """
    Razorpay Standard Web Checkout - Step 3: Verify Signature.
    Algorithm: HMAC-SHA256(order_id + "|" + payment_id, KEY_SECRET)
    Compares generated signature with razorpay_signature.
    Returns success only if signatures match.
    """
    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    if not key_id or not key_secret:
        raise HTTPException(
            status_code=500,
            detail="Razorpay payment gateway credentials not configured in server environment."
        )

    # Error handling: Missing required fields
    if not req.razorpay_order_id or not req.razorpay_payment_id or not req.razorpay_signature:
        raise HTTPException(
            status_code=400,
            detail="Missing required payment verification fields (razorpay_order_id, razorpay_payment_id, razorpay_signature)."
        )

    # Cryptographic HMAC-SHA256 signature verification
    msg = f"{req.razorpay_order_id}|{req.razorpay_payment_id}".encode()
    expected_signature = hmac.new(key_secret.encode(), msg, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(expected_signature, req.razorpay_signature):
        raise HTTPException(
            status_code=400,
            detail="Payment verification failed: Invalid signature. Order will NOT be marked as paid."
        )

    # Payment verified successfully — generate session token and unlock entitlements
    session_token = hashlib.sha256(
        f"{req.razorpay_payment_id}{key_secret}".encode()
    ).hexdigest()[:32]

    plan_key = req.plan or req.plan_id or "report_master"
    plan_info = PLANS.get(plan_key, {})
    q_count = plan_info.get("questions_count", 5)

    _verified_payments[session_token] = {
        "plan":                plan_key,
        "plan_name":           plan_info.get("name", "Charm AI"),
        "payment_id":          req.razorpay_payment_id,
        "order_id":            req.razorpay_order_id,
        "email":               req.email or "",
        "questions_count":     q_count,
        "questions_remaining": q_count,
        "has_remedies":        plan_info.get("has_remedies", False),
        "verified_at":         int(time.time()),
    }
    _save_sessions()

    # Synchronize entitlements with registered user account if present
    if req.email:
        if plan_key.startswith("bundle_"):
            for inc_rep in plan_info.get("included_reports", []):
                update_user_entitlements(
                    email_or_user_id=req.email,
                    plan_id=inc_rep,
                    credits_to_add=0,
                    unlocked_report=inc_rep
                )
        update_user_entitlements(
            email_or_user_id=req.email,
            plan_id=plan_key,
            credits_to_add=q_count if q_count < 9999 else 9999,
            unlocked_report=plan_key if (plan_key.startswith("report_") or plan_key.startswith("bundle_") or plan_key in ["complete_report", "starter_5q", "growth_10q"]) else None
        )

    # Persist to bookings log
    _persist_payment(req, session_token)

    # Automatically generate official invoice & dispatch email receipt
    generated_inv_id = None
    try:
        from app.api.billing import create_invoice_record, dispatch_invoice_notification, InvoiceCreateRequest
        import threading
        inv_name = getattr(req, 'customer_name', None) or (req.email.split('@')[0].replace('.', ' ').title() if req.email else 'Valued Seeker')
        inv_phone = getattr(req, 'customer_phone', '') or ''
        inv_req = InvoiceCreateRequest(
            order_id=req.razorpay_order_id,
            payment_id=req.razorpay_payment_id,
            customer_name=inv_name,
            customer_email=req.email or '',
            customer_phone=inv_phone,
            plan_id=plan_key,
            amount_inr=plan_info.get('amount_inr', 1050),
            payment_method='Razorpay Online Payment'
        )
        invoice_obj = create_invoice_record(inv_req)
        generated_inv_id = invoice_obj.get('invoice_id')
        threading.Thread(target=dispatch_invoice_notification, args=(invoice_obj,), daemon=True).start()
    except Exception as inv_err:
        print(f'[PAYMENT INVOICE GENERATION WARNING] {inv_err}')

    return {
        "status":              "success",
        "verified":            True,
        "message":             "Payment verified successfully.",
        "invoice_id":          generated_inv_id,
        "order_id":            req.razorpay_order_id,
        "payment_id":          req.razorpay_payment_id,
        "premium_token":       session_token,
        "plan":                plan_key,
        "plan_name":           plan_info.get("name", "Numeros Vision"),
        "unlocked_report":     plan_key
    }


@router.post("/verify-payment")
async def router_verify_payment(req: VerifyPaymentRequest):
    return await verify_payment(req)


@api_router.post("/verify-payment")
async def api_verify_payment(req: VerifyPaymentRequest):
    return await verify_payment(req)


@router.get("/status/{session_token}")
def check_status(session_token: str):
    """Check if a session token corresponds to a verified premium payment."""
    record = _verified_payments.get(session_token)
    if not record:
        return {"active": False}
    return {
        "active": True,
        "plan":   record["plan"],
        "email":  record.get("email", ""),
        "questions_remaining": record.get("questions_remaining", 0),
        "has_remedies": record.get("has_remedies", False),
    }


@router.post("/webhook")
async def razorpay_webhook(request: Request):
    """
    Razorpay Server-to-Server Webhook Handler.
    Handles 'payment.captured' and 'order.paid' events.
    Verifies X-Razorpay-Signature using RAZORPAY_WEBHOOK_SECRET.
    """
    raw_body = await request.body()
    signature = request.headers.get("X-Razorpay-Signature", "")

    # Verify signature if secret is configured and not default placeholder
    if RAZORPAY_WEBHOOK_SECRET not in ("REPLACE_ME_SECRET", "REPLACE_WITH_ACTUAL_RAZORPAY_KEY_SECRET"):
        expected_sig = hmac.new(
            RAZORPAY_WEBHOOK_SECRET.encode(),
            raw_body,
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(expected_sig, signature):
            raise HTTPException(status_code=400, detail="Invalid webhook signature")

    try:
        payload = json.loads(raw_body.decode("utf-8"))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")

    event = payload.get("event", "")

    if event in ("payment.captured", "order.paid"):
        payment_entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
        order_entity = payload.get("payload", {}).get("order", {}).get("entity", {})

        payment_id = payment_entity.get("id") or f"pay_wh_{int(time.time())}"
        order_id = payment_entity.get("order_id") or order_entity.get("id") or f"order_wh_{int(time.time())}"
        notes = payment_entity.get("notes") or order_entity.get("notes") or {}
        plan_id = notes.get("plan", "starter_5q")
        email = notes.get("email", "")

        # Provision session token
        session_token = hashlib.sha256(
            f"{payment_id}{RAZORPAY_KEY_SECRET}".encode()
        ).hexdigest()[:32]

        plan_info = PLANS.get(plan_id, {})
        q_count = plan_info.get("questions_count", 5)

        _verified_payments[session_token] = {
            "plan":                plan_id,
            "plan_name":           plan_info.get("name", "Charm AI"),
            "payment_id":          payment_id,
            "order_id":            order_id,
            "email":               email,
            "questions_count":     q_count,
            "questions_remaining": q_count,
            "has_remedies":        plan_info.get("has_remedies", False),
            "verified_at":         int(time.time()),
            "source":              "webhook",
        }
        _save_sessions()

        if email:
            if plan_id.startswith("bundle_"):
                for inc_rep in plan_info.get("included_reports", []):
                    update_user_entitlements(
                        email_or_user_id=email,
                        plan_id=inc_rep,
                        credits_to_add=0,
                        unlocked_report=inc_rep
                    )
            update_user_entitlements(
                email_or_user_id=email,
                plan_id=plan_id,
                credits_to_add=q_count if q_count < 9999 else 9999,
                unlocked_report=plan_id if (plan_id.startswith("report_") or plan_id.startswith("bundle_") or plan_id in ["complete_report", "starter_5q", "growth_10q"]) else None
            )

        # Log to data/payments.jsonl
        try:
            os.makedirs(DATA_DIR, exist_ok=True)
            with open(os.path.join(DATA_DIR, "payments.jsonl"), "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "token": session_token,
                    "plan": plan_id,
                    "payment_id": payment_id,
                    "order_id": order_id,
                    "email": email,
                    "source": "webhook",
                    "ts": int(time.time())
                }) + "\n")
        except Exception:
            pass

        return {
            "status": "success",
            "event": event,
            "session_token": session_token,
            "plan": plan_id
        }

    return {"status": "ignored", "event": event}


# ── Funnel & Customer Journey Endpoints (v1.5.0) ──────────────────────────

@router.get("/funnel/products")
def get_funnel_products():
    """Return unified product catalogue with approved funnel hooks, deliverables and CTAs."""
    return {
        "status": "success",
        "tagline": "ANVEIL EVERY CHARM",
        "currency": "INR",
        "products": PRODUCT_FUNNEL_CATALOG
    }


@router.post("/funnel/validate-price")
def validate_funnel_price(req: PriceValidationRequest):
    """
    Validates pricing against brand digit-root policy {1, 3, 5, 6}
    and verifies that offer price is strictly less than reference price.
    """
    if req.reference is not None and req.offer is not None:
        return validate_price_pair(req.reference, req.offer)
    if req.amount is not None:
        return validate_single_price(req.amount)
    raise HTTPException(status_code=400, detail="Must provide either 'amount' or both 'reference' and 'offer'")


@router.api_route("/funnel/next-step", methods=["GET", "POST"])
async def funnel_next_step(
    request: Request,
    product_id: Optional[str] = None,
    calculation_completed: Optional[bool] = None,
    free_result_available: Optional[bool] = None,
    token: Optional[str] = None,
    opted_out: Optional[bool] = None,
):
    """
    Determines seeker's next action in the 7-stage marketing funnel.
    Supports GET query parameters and POST JSON bodies.
    Enforces opt-out precedence and prevents duplicate report sales.
    """
    if request.method == "POST":
        try:
            body = await request.json()
            if isinstance(body, dict):
                product_id = body.get("product_id", product_id)
                calculation_completed = body.get("calculation_completed", calculation_completed)
                free_result_available = body.get("free_result_available", free_result_available)
                token = body.get("token", token)
                opted_out = body.get("opted_out", opted_out)
        except Exception:
            pass

    pid = product_id or "birth_number"
    calc_done = bool(calculation_completed)
    free_res = bool(free_result_available)
    is_opted_out = bool(opted_out)

    sess_token = token or request.cookies.get("nv_user_session") or request.headers.get("x-session-token")
    
    entitlements = []
    payment_status = None
    fulfilment_status = None

    if sess_token and sess_token in _verified_payments:
        rec = _verified_payments[sess_token]
        plan = rec.get("plan", "")
        entitlements.append(plan)
        payment_status = "CONFIRMED"
        fulfilment_status = "FULFILLED"

    context = JourneyContext(
        session_token=sess_token,
        user_opted_out_of_marketing=is_opted_out,
        calculation_completed=calc_done,
        free_result_available=free_res,
        payment_status=payment_status,
        fulfilment_status=fulfilment_status,
        current_entitlements=entitlements
    )

    step = get_next_step(
        user=None,
        product_id=pid,
        journey_context=context
    )
    return step


@router.post("/funnel/event")
async def capture_funnel_event(req: FunnelEventRequest, request: Request):
    """
    Captures privacy-minimised marketing funnel events.
    Rejects sensitive PII (DOB, mobile, credit card numbers).
    """
    sess_id = req.session_id or request.cookies.get("nv_user_session") or "anon"
    success = log_funnel_event(
        event_name=req.event,
        product_id=req.product_id,
        stage=req.stage,
        session_id=sess_id,
        metadata=req.metadata
    )
    return {
        "status": "success" if success else "ignored",
        "event": req.event,
        "logged": success
    }


# ── Internal helpers ───────────────────────────────────────────────────────

def _persist_payment(req: VerifyPaymentRequest, token: str):
    """Append verified payment to bookings.jsonl log."""
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
        record = {
            "token":      token,
            "plan":       req.plan,
            "payment_id": req.razorpay_payment_id,
            "order_id":   req.razorpay_order_id,
            "email":      req.email or "",
            "ts":         int(time.time()),
        }
        with open(os.path.join(DATA_DIR, "payments.jsonl"), "a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
    except Exception:
        pass  # Non-critical — don't block the user response
