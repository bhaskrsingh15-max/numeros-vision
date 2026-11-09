"""
MONETIZATION ALIGNMENT & UPSELLING ENGINE — NUMEROS VISION
Tagline: ANVEIL EVERY CHARM

PURPOSE:
1. Deterministic Alignment & Gap Analysis:
   - Compares Driver (Mulank) vs Conductor (Bhagyank) harmony.
   - Audits Lo Shu 3x3 Grid for missing numbers and incomplete planes (Golden Plane 4-5-6, Will 9-5-1, etc.).
   - Evaluates Chaldean Name Vibration compatibility with Driver/Conductor.
   - Computes Alignment Grade: ALIGNED (80-100%), PARTIALLY ALIGNED (60-79%), FRICTION DETECTED (<60%).

2. Personalized Conversion Hooks & CTAs:
   - Reveals the exact energetic gaps (e.g. 1-8 Sun-Saturn polarity, missing 5-6 financial leaks).
   - Generates persuasive, dignified, non-coercive conversion hooks.
   - Employs brand tagline 'ANVEIL EVERY CHARM' in high-converting CTAs.

3. Credit Tracking & Upselling Pathways:
   - Monitors Charm AI question credits (Starter 5Q, Growth 10Q/15Q, Power 35Q).
   - Generates tailored recharge and upscaling hooks when credits reach zero.
   - Provides upgrade paths from tripwires (₹95, ₹105, ₹199) to Master (₹510) and Sovereign (₹1,050).

4. Staging Replica Testing Mode:
   - Detects staging environment or bypass tokens to grant full test access for QA/QC.
"""

from typing import Dict, Any, List, Optional
import os

# Harmonic & Polar Number Relationships (Vedic & Chaldean Occult Numerology)
FRIENDLY_PAIRS = {
    1: {1, 2, 3, 5, 9},
    2: {1, 2, 3, 5},
    3: {1, 2, 3, 5, 7, 9},
    4: {1, 5, 6, 7, 8},
    5: {1, 2, 3, 5, 6},
    6: {1, 5, 6, 7, 8},
    7: {1, 3, 4, 5, 6},
    8: {3, 5, 6, 7},
    9: {1, 2, 3, 5, 7, 9}
}

ENEMY_PAIRS = {
    1: {6, 8},          # Sun vs Venus/Saturn
    2: {4, 8, 9},       # Moon vs Rahu/Saturn/Mars
    3: {6},             # Jupiter vs Venus (Deva Guru vs Asura Guru)
    4: {2, 9},          # Rahu vs Moon/Mars
    5: set(),           # Mercury has no direct natural enemies in classical numerology
    6: {1, 3},          # Venus vs Sun/Jupiter
    7: {9},             # Ketu vs Mars
    8: {1, 2, 4, 9},    # Saturn vs Sun/Moon/Rahu/Mars
    9: {2, 4, 7, 8}     # Mars vs Moon/Rahu/Ketu/Saturn
}

# Lo Shu Grid Planes Definitions
LOSHU_PLANES = {
    "golden_prosperity_plane": {
        "numbers": {4, 5, 6},
        "name": "Golden Prosperity & Success Plane",
        "description": "Financial abundance, balance, commercial wisdom, and worldly stability.",
        "remedy_focus": "Mercury & Venus harmonizing remedies, Green Aventurine / Pyrite, North-East workspace decluttering."
    },
    "will_power_plane": {
        "numbers": {9, 5, 1},
        "name": "Will Power & Determination Plane",
        "description": "Persistence, executive decision-making, and perseverance against obstacles.",
        "remedy_focus": "Morning sunlight absorption, Surya Gayatri meditation, red/orange attunement."
    },
    "thought_planning_plane": {
        "numbers": {4, 3, 8},
        "name": "Thought & Conceptual Planning Plane",
        "description": "Visionary thinking, organizational foresight, and strategic blueprinting.",
        "remedy_focus": "Jupiter/Rahu balancing, blue sapphire/amethyst crystal placement, sandalwood aroma."
    },
    "action_execution_plane": {
        "numbers": {2, 7, 6},
        "name": "Action & Practical Manifestation Plane",
        "description": "Turning thoughts into tangible reality, swift project execution, and public charisma.",
        "remedy_focus": "Silver square grounding, Friday Venusian seva, purposeful task batching."
    },
    "mental_intellectual_plane": {
        "numbers": {4, 9, 2},
        "name": "Mental & Memory Plane",
        "description": "High IQ, analytical calculation, memory retention, and intellectual grasp.",
        "remedy_focus": "Mental clarity breathwork, brass bowl water energization, evening screen detachment."
    },
    "emotional_spiritual_plane": {
        "numbers": {3, 5, 7},
        "name": "Emotional & Intuitive Plane",
        "description": "Empathy, relational harmony, spiritual depth, and emotional equilibrium.",
        "remedy_focus": "Moonlight meditation, raw milk donation on Mondays, copper energizer."
    },
    "practical_grounding_plane": {
        "numbers": {8, 1, 6},
        "name": "Practical Grounding & Asset Plane",
        "description": "Real estate, material wealth, operational diligence, and physical stability.",
        "remedy_focus": "Mustard oil lamp on Saturdays, earth grounding (barefoot walking), iron/shungite shield."
    }
}


def analyze_user_alignment_and_gaps(
    driver: int,
    conductor: int,
    loshu_counts: Dict[str, int],
    missing_numbers: List[int],
    name_number: Optional[int] = None,
    personal_year: Optional[int] = None,
    active_dasha: Optional[str] = None,
    current_plan: Optional[str] = None,
    credits_remaining: int = 0
) -> Dict[str, Any]:
    """
    Deterministic evaluation of seeker cosmic alignment, identifying concrete gaps,
    generating personalized conversion hooks and CTAs with the official brand tagline.
    """
    d = int(driver) if driver else 1
    c = int(conductor) if conductor else 1

    # 1. Driver-Conductor Harmony
    is_friendly = c in FRIENDLY_PAIRS.get(d, set())
    is_enemy = c in ENEMY_PAIRS.get(d, set())

    alignment_score = 85
    alignment_status = "ALIGNED"
    alignment_summary = "Harmonious resonance between natural personality and life direction."
    polarity_notice = ""

    if is_enemy:
        alignment_score = 48
        alignment_status = "FRICTION_DETECTED"
        alignment_summary = f"Energetic tension between Driver {d} (Core Will) and Conductor {c} (Life Path)."
        polarity_notice = f"Your chart carries an active Root {d} vs Path {c} energetic polarity. Your internal drives and external destiny pull in contrasting directions, causing periodic self-doubt, career pivots, or delayed results."
    elif not is_friendly:
        alignment_score = 68
        alignment_status = "PARTIALLY_ALIGNED"
        alignment_summary = f"Neutral interaction between Driver {d} and Conductor {c}; requires conscious calibration."
        polarity_notice = f"Your Root {d} and Path {c} operate with neutral coordination. Without energetic grounding, routine efforts often require double the output for standard rewards."

    # 2. Audit Lo Shu Planes
    present_numbers = {int(k) for k, v in loshu_counts.items() if int(v) > 0}
    incomplete_planes = []
    complete_planes = []

    for plane_id, plane_data in LOSHU_PLANES.items():
        req = plane_data["numbers"]
        intersection = present_numbers.intersection(req)
        if len(intersection) == 3:
            complete_planes.append({
                "plane_id": plane_id,
                "name": plane_data["name"],
                "status": "COMPLETE",
                "strength": "High"
            })
        else:
            missing_in_plane = list(req - intersection)
            incomplete_planes.append({
                "plane_id": plane_id,
                "name": plane_data["name"],
                "missing_digits": sorted(missing_in_plane),
                "completion_ratio": f"{len(intersection)}/3",
                "description": plane_data["description"],
                "remedy_focus": plane_data["remedy_focus"]
            })

    # Golden Plane (4-5-6) specific check
    golden_plane_missing = sorted(list({4, 5, 6} - present_numbers))
    has_golden_gap = len(golden_plane_missing) > 0

    # 3. Identify Primary Detected Gaps
    detected_gaps = []

    if is_enemy:
        detected_gaps.append({
            "gap_code": "POLARITY_DRIVER_CONDUCTOR",
            "title": f"Polarity Between Driver {d} & Conductor {c}",
            "impact": "Inner drive and outer life path work at cross-purposes, creating friction in authority, career progress, and partnership stability.",
            "urgency": "High"
        })

    if has_golden_gap:
        detected_gaps.append({
            "gap_code": "GOLDEN_PROSPERITY_GAP",
            "title": f"Incomplete Golden Prosperity Plane (Missing: {', '.join(map(str, golden_plane_missing))})",
            "impact": "Financial leakages, difficulty retaining accumulated wealth, or instability during commercial expansion cycles.",
            "urgency": "High" if 5 in golden_plane_missing else "Medium"
        })

    if 5 in missing_numbers:
        detected_gaps.append({
            "gap_code": "CENTRAL_STABILITY_VOID",
            "title": "Missing Central Anchor Number 5 (Brahmasthan Void)",
            "impact": "Restlessness, sudden emotional swings, and challenges sustaining long-term consistency in one domain.",
            "urgency": "High"
        })

    if 6 in missing_numbers:
        detected_gaps.append({
            "gap_code": "VENUS_COMFORT_LEAK",
            "title": "Missing Luxury & Supportive Alliances Number 6",
            "impact": "Working hard but experiencing delayed comforts, strained spousal intimacy, or absence of influential mentors.",
            "urgency": "Medium"
        })

    if not detected_gaps:
        detected_gaps.append({
            "gap_code": "TIMING_CALIBRATION_NEED",
            "title": "Planetary Transit & Dasha Cycle Timing Alignment",
            "impact": "While core numbers are well-positioned, navigating personal year transits without exact auspicious timing windows leads to missed opportunities.",
            "urgency": "Medium"
        })

    # 4. Generate Personalized Conversion Hook & CTA with Brand Tagline
    primary_gap = detected_gaps[0]
    missing_str = ", ".join(map(str, sorted(missing_numbers))) if missing_numbers else "Subtle Elemental Alignment"
    
    # Personalized Hook Copy with Lucky Charm Gap Neutralization
    hook_narrative = (
        f"Your free diagnostic indicates an **{alignment_status.replace('_', ' ')}** matrix ({alignment_score}% Harmony). "
        f"{polarity_notice} "
        f"Critically, our natal Lo Shu grid audit detected: **{primary_gap['title']}**. "
        f"{primary_gap['impact']} "
        f"These energetic blockages cause vital momentum and wealth to leak away. "
        f"To seal these voids, your chart requires your consecrated **Personalized Lucky Charm** (Planetary Metal, Sacred Beej Sound Frequency, and Gemstone Vector). "
        f"Your bespoke Lucky Charm activation protocol and full remedial blueprint are compiled exclusively inside the Master Synthesis Dossier."
    )

    # Official Call-To-Action with Tagline & Lucky Charm Activation
    primary_cta = {
        "tagline": "ANVEIL EVERY CHARM",
        "full_tagline": "NUMEROS VISION · ANVEIL EVERY CHARM",
        "headline": "✦ ANVEIL EVERY CHARM — Activate Your Lucky Charm & Seal Gaps ✦",
        "subheadline": f"Harmonize your Driver {d}-Conductor {c} polarity and activate your personalized Lucky Charm & dual-system remedies.",
        "recommended_plan": "report_master",
        "recommended_plan_name": "Master Dual-System Synthesis Dossier",
        "amount_inr": 510,
        "original_price_inr": 999,
        "discount_percent": "49% OFF",
        "button_text": "ANVEIL EVERY CHARM ✦ Activate Lucky Charm Dossier (₹510)",
        "button_url": "/checkout/?plan=report_master",
        "starter_alternative": {
            "plan": "starter_5q",
            "name": "Starter 5-Question Pass",
            "amount_inr": 95,
            "button_text": "Start with 5 Questions (₹95)",
            "button_url": "/checkout/?plan=starter_5q"
        }
    }

    # 5. Upselling & Recharge Logic (Rule 2)
    credits_exhausted = (credits_remaining <= 0 and current_plan in ["starter_5q", "growth_10q", "ai_starter_5q", "ai_growth_15q"])
    upsell_package = None

    if credits_exhausted:
        upsell_package = {
            "is_credits_exhausted": True,
            "headline": "✦ Your Question Credits Have Concluded ✦",
            "message": "You have utilized your question predictions. Your chart still carries active milestone transit windows and golden plane opportunities waiting to be resolved.",
            "tagline_cta": "ANVEIL EVERY CHARM ✦ Recharge Your Predictions",
            "recharge_options": [
                {
                    "plan": "ai_growth_15q",
                    "name": "Growth Pass — 15 Questions + Full Remedies",
                    "amount_inr": 199,
                    "button_text": "Recharge 15 Questions (₹249) ✦"
                },
                {
                    "plan": "report_master",
                    "name": "Master Dual-System Synthesis Dossier (35 Pages)",
                    "amount_inr": 510,
                    "button_text": "Upgrade to Master Dossier (₹510) ✦"
                }
            ]
        }
    elif current_plan in ["report_essential", "starter_5q"]:
        # User bought small tier; upscale to master
        upsell_package = {
            "is_credits_exhausted": False,
            "headline": "✦ Complete Your Cosmic Matrix ✦",
            "message": "You have unlocked your foundational numbers, but your 5-Year Dasha Timeline and 7-Layer Consecrated Remedies remain veiled.",
            "tagline_cta": "ANVEIL EVERY CHARM ✦ Upgrade to Master Synthesis Dossier",
            "upgrade_plan": "report_master",
            "amount_inr": 510,
            "button_text": "ANVEIL EVERY CHARM ✦ Upgrade to Master (₹510)"
        }

    return {
        "status": "success",
        "alignment_status": alignment_status,
        "alignment_score": alignment_score,
        "alignment_summary": alignment_summary,
        "driver_number": d,
        "conductor_number": c,
        "is_friendly": is_friendly,
        "is_enemy": is_enemy,
        "detected_gaps": detected_gaps,
        "complete_planes_count": len(complete_planes),
        "incomplete_planes_count": len(incomplete_planes),
        "golden_plane_gap": golden_plane_missing,
        "hook_narrative": hook_narrative,
        "lucky_charm_hook": f"Your Lo Shu grid carries unsealed gaps in [{missing_str}]. To neutralize these voids, your chart requires your personalized consecrated Lucky Charm (Planetary Metal, Sacred Beej Sound Frequency, and Gemstone Vector).",
        "lucky_charm_solution_locked": True,
        "primary_cta": primary_cta,
        "credits_remaining": credits_remaining,
        "credits_exhausted": credits_exhausted,
        "upsell_package": upsell_package
    }


def is_staging_bypass_authorized(request_headers: Dict[str, str], query_params: Dict[str, str], token: Optional[str] = None) -> bool:
    """
    Rule 3: Determines if the caller is authorized for Staging Replica Preview mode.
    Strictly disallowed in production unless authorized staging header or token is present.
    """
    env = os.getenv("ENVIRONMENT", "development").lower()
    if env == "production":
        return False
    
    # 1. Master test tokens allow bypass in non-production
    if token in ("test_master_pass", "test_token", "staging_preview_token", "admin_test") or (token and token.startswith("test_")):
        if env != "production" or os.getenv("ALLOW_TEST_TOKENS", "false").lower() == "true":
            return True

    # 2. Check for explicit Staging host, header or query param
    host = request_headers.get("host", "").lower()
    is_staging_host = "staging.numerosvision.com" in host or host.endswith(":8001")
    staging_header = request_headers.get("x-staging-test-bypass", "").lower() in ("true", "1")
    staging_query = query_params.get("staging_preview", "").lower() in ("true", "1")

    if (is_staging_host or staging_header or staging_query or env == "staging") and (env != "production" or os.getenv("ALLOW_STAGING_TEST_BYPASS", "false").lower() == "true"):
        return True

    return False


TOOL_MONETIZATION_CONFIG: Dict[str, Dict[str, Any]] = {
    "business_alignment": {
        "tool_display_name": "Business Direction & Operating Alignment",
        "charm_tagline_action": "ANVEIL Your Business Charm",
        "lock_headline": "🔒 Unveil Your Complete Business Charm & Operational Blueprint",
        "curiosity_hook_template": (
            "Your enterprise '{entity_name}' vibrates at Chaldean Compound {compound} (Root {root}), indicating {status_clean} market resonance. "
            "However, your Founder Cosmic Synergy (Driver-Conductor match), 4 Calibrated Balanced Name Spellings, "
            "and Vastu Desk & Cash Inflow Directions remain veiled inside your complete executive dossier."
        ),
        "veiled_deliverables": [
            "Letter-by-Letter Acoustic Sound Frequency Matrix (Chaldean values 1–8)",
            "Founder-to-Brand Synergy Match % & Planetary Polarity Audit",
            "4 Auspicious Balanced Spelling Variations (Roots 1, 3, 5, 6) with Click-to-Adopt",
            "Vastu Desk Seating Orientation, Cash Sector & Auspicious Launch Muhurat Timing Windows"
        ],
        "recommended_plan": "report_master",
        "plan_name": "Executive Business Alignment Blueprint",
        "anchor_price_inr": 999,
        "entry_price_inr": 510,
        "discount_badge": "SAVE 49% · INSTANT Explore"
    },
    "logo_studio": {
        "tool_display_name": "Logo Studio & Brand Intelligence",
        "charm_tagline_action": "ANVEIL Your Brand Geometry Charm",
        "lock_headline": "🔒 Unveil Your Sacred Geometry Brand Kit & Production Vectors",
        "curiosity_hook_template": (
            "Your custom logo mark '{entity_name}' is harmonized with sacred geometry. "
            "To deploy your identity across trademark filings, high-end packaging, and digital signage, "
            "Explore Your zero-artifact mathematical vector suite with WCAG AAA certified color palettes."
        ),
        "veiled_deliverables": [
            "Pure Scalable Vector Graphics (SVG 1.1) in Horizontal, Stacked, and Badge lockups",
            "Ultra High-Resolution 4K Transparent PNGs for print, merchandise & app icons",
            "Certified Multi-Gate Independent Audit Manifest (100% OCR Exact Match)",
            "W3C & WCAG 2.1 AAA Contrast Ratio Legal Certification Report"
        ],
        "recommended_plan": "report_master",
        "plan_name": "Production Vector Identity Kit",
        "anchor_price_inr": 1499,
        "entry_price_inr": 510,
        "discount_badge": "SAVE 66% · INSTANT Explore"
    },
    "charm_ai": {
        "tool_display_name": "Charm AI",
        "charm_tagline_action": "ANVEIL Your Career & Destiny Charm",
        "lock_headline": "🔒 Unveil Your 5-Year Planetary Dasha Timeline & Consecrated Remedies",
        "curiosity_hook_template": (
            "Charm AI has mapped your natal coordinates. "
            "While your foundational takeaway is active, your high-probability career breakthrough milestone dates, "
            "karmic Lo Shu missing-digit neutralizers, and consecrated 7-layer Upay remedies remain veiled."
        ),
        "veiled_deliverables": [
            "Full 5-Year Numerology Dasha & Numerological Dasha Progression Timeline",
            "Natal Lo Shu Grid Missing Digit Neutralization Protocol",
            "Personalized Consecrated Gemstone, Beej Mantra & Crystal Prescription",
            "Daily & Monthly Auspicious Decision Windows (Muhurat Radar)"
        ],
        "recommended_plan": "report_master",
        "plan_name": "Complete Life Dossier (12-Page Master Dossier & Full Remedies)",
        "anchor_price_inr": 999,
        "entry_price_inr": 510,
        "discount_badge": "SAVE 50% · INSTANT Explore"
    },
    "life_path": {
        "tool_display_name": "Life Path Calculator",
        "charm_tagline_action": "ANVEIL Your Life Path Charm",
        "lock_headline": "🔒 Unveil Your 35-Page Master Dual-System Destiny Dossier",
        "curiosity_hook_template": (
            "Your Life Path is {root} ({status_clean}). "
            "Discover how your calling name, phone vibration, and current 2026 personal year cycle "
            "interact with your life path to either accelerate or stall your major life milestones."
        ),
        "veiled_deliverables": [
            "35-40 Page Master Dual-System Executive Dossier (PDF)",
            "Chaldean Legal vs Calling Name Harmony Verification",
            "BNN 1-5-9 Trines & 2-12 Wealth Vector Progression",
            "Complete 7-Layer Practical Remedial Upay Blueprint"
        ],
        "recommended_plan": "report_master",
        "plan_name": "Master Dual-System Synthesis Dossier",
        "anchor_price_inr": 999,
        "entry_price_inr": 510,
        "discount_badge": "SAVE 49% · INSTANT Explore"
    },
    "birth_number": {
        "tool_display_name": "Birth Number (Mulank) Calculator",
        "charm_tagline_action": "ANVEIL Your Driver Charm",
        "lock_headline": "🔒 Unveil Your Core Driver Polarity & Personalized Gemstone Prescription",
        "curiosity_hook_template": (
            "Your Core Driver (Mulank) is {root}. "
            "Uncover whether your Driver is in natural harmony or friction with your Conductor (Bhagyank), "
            "and activate your sacred planetary gemstone and color vectors."
        ),
        "veiled_deliverables": [
            "Driver (Mulank) vs Conductor (Bhagyank) Polarity Audit",
            "Auspicious Days, Harmonic Colors & Sacred Metal Prescription",
            "Karmic Debt Number check (13, 14, 16, 19)",
            "Personalized Lucky Charm Activation Protocol"
        ],
        "recommended_plan": "report_essential",
        "plan_name": "Essential Cosmic Blueprint",
        "anchor_price_inr": 399,
        "entry_price_inr": 199,
        "discount_badge": "SAVE 50% · INSTANT Explore"
    },
    "lo_shu_grid": {
        "tool_display_name": "Lo Shu 3×3 Magic Square",
        "charm_tagline_action": "ANVEIL Your Elemental Grid Charm",
        "lock_headline": "🔒 Unveil Your Missing Plane Remedies & Rajyog Wealth Diagonals",
        "curiosity_hook_template": (
            "Your natal Lo Shu grid has been mapped. "
            "To seal karmic energy leaks and activate your incomplete planes (Golden Prosperity 4-5-6, Will 9-5-1), "
            "Explore Your consecrated 5-element remedy blueprint."
        ),
        "veiled_deliverables": [
            "8 Elemental Planes Strength & Void Audit",
            "Consecrated Crystal & Sacred Yantra Placement Guide",
            "Golden (4-5-6) & Silver (2-5-8) Rajyog Abundance Activation",
            "Remedial Harmonization for Missing Digits"
        ],
        "recommended_plan": "report_master",
        "plan_name": "Master Dual-System Synthesis Dossier",
        "anchor_price_inr": 999,
        "entry_price_inr": 510,
        "discount_badge": "SAVE 49% · INSTANT Explore"
    },
    "name_numerology": {
        "tool_display_name": "Name Numerology & Balancing",
        "charm_tagline_action": "ANVEIL Your Name Charm",
        "lock_headline": "🔒 Unveil 3 Calibrated Balanced Spelling Variations & Calling Name Harmony",
        "curiosity_hook_template": (
            "Your name '{entity_name}' calculates to Compound {compound} (Root {root}). "
            "If your name carries subtle friction against your date of birth, Explore 3 calibrated spelling variations "
            "to channel magnetic prosperity and customer attraction."
        ),
        "veiled_deliverables": [
            "Full Legal Name vs Calling Name Vibrational Coherence Audit",
            "3 Optimal Harmonized Spelling Variations targeting Roots 1, 3, 5, 6",
            "Social Media Handle, Signature & Email Alignment Guide",
            "Official Gazette & Spelling Transition Practical Checklist"
        ],
        "recommended_plan": "report_master",
        "plan_name": "Master Dual-System Synthesis Dossier",
        "anchor_price_inr": 999,
        "entry_price_inr": 510,
        "discount_badge": "SAVE 49% · INSTANT Explore"
    }
}


def get_tool_monetization_payload(
    tool_key: str,
    entity_name: str = "Your Profile",
    compound: Optional[int] = None,
    root: Optional[int] = None,
    status: str = "ALIGNED",
    custom_context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Constructs the curiosity-based gating payload for any tool across Numeros Vision.
    Enforces master brand tagline 'ANVEIL EVERY CHARM', lock symbol, and price anchoring.
    """
    cfg = TOOL_MONETIZATION_CONFIG.get(tool_key, TOOL_MONETIZATION_CONFIG["business_alignment"])
    status_clean = status.replace("_", " ").title()
    compound_val = compound if compound is not None else 55
    root_val = root if root is not None else 1

    hook_text = cfg["curiosity_hook_template"].format(
        entity_name=entity_name,
        compound=compound_val,
        root=root_val,
        status_clean=status_clean
    )

    plan_key = cfg["recommended_plan"]
    entry_inr = cfg["entry_price_inr"]
    anchor_inr = cfg["anchor_price_inr"]
    tagline_action = cfg["charm_tagline_action"]

    return {
        "tool_key": tool_key,
        "tool_display_name": cfg["tool_display_name"],
        "master_tagline": "ANVEIL EVERY CHARM",
        "charm_tagline_action": tagline_action,
        "lock_icon": "🔒",
        "lock_headline": cfg["lock_headline"],
        "curiosity_hook": hook_text,
        "veiled_deliverables": cfg["veiled_deliverables"],
        "recommended_plan": plan_key,
        "plan_name": cfg["plan_name"],
        "anchor_price_inr": anchor_inr,
        "entry_price_inr": entry_inr,
        "discount_badge": cfg["discount_badge"],
        "button_text": f"🔒 {tagline_action} · Explore Report (₹{entry_inr}) ✦",
        "checkout_url": f"/checkout/?plan={plan_key}&tool={tool_key}",
        "guarantee_note": "100% Deterministic Engine Authority · Zero AI Hallucination · Statutory DPDP 2023 Consent"
    }
