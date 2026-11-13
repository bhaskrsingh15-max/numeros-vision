import sys
import re

content = open("app/api/payments.py", encoding="utf-8").read()

# 1. Add import from pricing_config
if "from app.config.pricing_config import" not in content:
    content = content.replace(
        "from app.engine.funnel_service import (",
        "from app.config.pricing_config import resolve_sku_price, REPORT_TIERS, BUNDLES, CHARM_AI_PACKS, CONSULTATION_PACKS\nfrom app.engine.funnel_service import ("
    )

# 2. Add /pricing-catalog endpoint if not present
if '@router.get("/pricing-catalog")' not in content:
    endpoint_code = '''
@router.get("/pricing-catalog")
def get_pricing_catalog():
    """Returns authoritative server-side pricing catalog."""
    from app.config.pricing_config import export_pricing_catalog_json
    return json.loads(export_pricing_catalog_json())

'''
    content = content.replace('@router.get("/plans")', endpoint_code + '@router.get("/plans")')

# 3. Ensure create_order resolves price authoritatively
create_order_target = '''    plan_key = req.plan or req.plan_id or "starter_5q"
    if plan_key not in PLANS:
        raise HTTPException(status_code=400, detail=f"Unknown plan: {plan_key}")

    plan = PLANS[plan_key]'''

create_order_replacement = '''    plan_key = req.plan or req.plan_id or "report_basic"
    sku_resolved = resolve_sku_price(plan_key)
    if sku_resolved:
        plan_amount_paise = sku_resolved["amount_paise"]
        plan_amount_inr = sku_resolved["amount_inr"]
        plan_name = sku_resolved["name"]
    elif plan_key in PLANS:
        plan = PLANS[plan_key]
        plan_amount_paise = plan["amount_paise"]
        plan_amount_inr = plan["amount_inr"]
        plan_name = plan["name"]
    else:
        raise HTTPException(status_code=400, detail=f"Unknown plan: {plan_key}")'''

if create_order_target in content:
    content = content.replace(create_order_target, create_order_replacement)
    content = content.replace('plan["amount_paise"]', 'plan_amount_paise')
    content = content.replace('plan["amount_inr"]', 'plan_amount_inr')
    content = content.replace('plan["name"]', 'plan_name')

# 4. Add bundle SKUs to PLANS if missing
bundle_plans_code = '''    # ── UNIFIED STANDALONE REPORT TIERS ──────────────────────────────────────
    "report_basic": {
        "name": "Basic Report",
        "amount_inr": 199,
        "original_price_inr": 399,
        "amount_paise": 19900,
        "period": "3-Page Executive PDF",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "3-page focused report with core calculations, method note, and initial interpretation.",
        "features": ["3-Page Personalised PDF", "Driver & Conductor Calculations", "Lo Shu 3x3 Grid Matrix", "Chaldean Letter Breakdown", "Methodology & Limitations Note"]
    },
    "report_advanced": {
        "name": "Advanced Report",
        "amount_inr": 510,
        "original_price_inr": 999,
        "amount_paise": 51000,
        "period": "12-Page Master PDF",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "popular": True,
        "description": "12-page comprehensive master dossier with expanded analysis, comparisons, and safe remedies.",
        "features": ["12-Page Master Synthesis Dossier", "5-Year Vimshottari & Dasha Timeline", "Complete Lo Shu Plane Analysis", "Chaldean Sound Frequency Analysis", "7-Layer Safe Planetary Remedies"]
    },
    "report_premium": {
        "name": "Premium Dossier",
        "amount_inr": 1050,
        "original_price_inr": 1999,
        "amount_paise": 105000,
        "period": "32-Page Sovereign Blueprint",
        "questions_count": 0,
        "has_remedies": True,
        "category": "report",
        "description": "32-page sovereign executive dossier bringing together all supported calculations and technical appendix.",
        "features": ["32-Page Sovereign Master Dossier", "Dual-System Synthesis (Chaldean + Pythagorean)", "10-Year Macro Planetary Radar", "Multi-Factor Synastry & Compatibility", "Complete Mathematical Proofs Appendix"]
    },
    # ── UNIFIED MULTI-REPORT BUNDLES ─────────────────────────────────────────
    "starter_bundle": {
        "name": "Starter Bundle — 2 Basic Reports",
        "amount_inr": 349,
        "original_price_inr": 398,
        "amount_paise": 34900,
        "period": "2 Basic Reports",
        "questions_count": 0,
        "has_remedies": True,
        "category": "bundle",
        "description": "Two 3-page Basic reports of your choice across Love, Money, Work, or Growth.",
        "features": ["2 Complete Basic 3-Page Reports", "Save ₹49 (12% off standalone)", "Independent deterministic calculation traces", "Instant PDF downloads"]
    },
    "discovery_bundle": {
        "name": "Discovery Bundle — 3 Basic Reports",
        "amount_inr": 499,
        "original_price_inr": 597,
        "amount_paise": 49900,
        "period": "3 Basic Reports",
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
        "features": ["2 Complete 12-Page Advanced Reports (24 pages)", "1 Complete 3-Page Basic Report (3 pages)", "Save ₹220 (18% off standalone)", "Full Dasha timelines & 7-layer remedies"]
    },
    # ── UNIFIED CHARM AI PACKAGES ────────────────────────────────────────────
    "charm_single": {
        "name": "Charm AI — Single Reading",
        "amount_inr": 199,
        "original_price_inr": 399,
        "amount_paise": 19900,
        "period": "3 Questions + Timing",
        "questions_count": 3,
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
'''

if '"report_basic": {' not in content:
    content = content.replace('PLANS = {', 'PLANS = {\n' + bundle_plans_code)

open("app/api/payments.py", "w", encoding="utf-8").write(content)
print("Successfully updated app/api/payments.py with unified pricing architecture!")
