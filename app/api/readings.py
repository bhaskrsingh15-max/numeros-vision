import os
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from app.engine.consensus import generate_consensus_reading
from app.engine.remedy_engine import generate_comprehensive_predictions_and_remedies
from app.engine.lo_shu import analyze_lo_shu_grid, generate_loshu_grid_markdown
from app.engine.core_matrix_engine import calculate_age_numerology
from app.engine.ai_cost_and_security import sanitize_user_input, check_and_meter_usage, apply_ai_disclosure
from app.engine.question_explanation_engine import generate_simple_explanation_and_remedies
from app.engine.source_privacy_shield import sanitize_citation, sanitize_payload
from orchestrator import handle_question, handle_btr_request

router = APIRouter(prefix="/api/v1/readings", tags=["Readings"])

class FreeReadingRequest(BaseModel):
    name: str = Field(..., description="User full name")
    day: int = Field(..., ge=1, le=31, description="Day of birth (1-31)")
    month: int = Field(..., ge=1, le=12, description="Month of birth (1-12)")
    year: int = Field(..., ge=1900, le=2100, description="Year of birth (YYYY)")
    user_id: Optional[str] = Field(None, description="User ID for usage metering")
    birth_time: Optional[str] = Field("12:00", description="Birth time in HH:MM format (e.g. 16:15 or 04:15 PM)")
    place_name: Optional[str] = Field("Delhi, India", description="Birth city/place name")
    latitude: Optional[float] = Field(None, description="Birth latitude in degrees (-90.0 to 90.0)")
    longitude: Optional[float] = Field(None, description="Birth longitude in degrees (-180.0 to 180.0)")
    timezone: Optional[str] = Field("Asia/Kolkata", description="Timezone name or UTC offset")

class RemedyRequest(FreeReadingRequest):
    mobile_number: Optional[str] = Field("", description="Optional mobile number for mobile numerology check")
    chart_data: Optional[Dict[str, Any]] = Field(None, description="Optional planetary house placements")

class OpenEndedQuestionRequest(BaseModel):
    question: str = Field(..., description="Open-ended question in natural language")
    name: Optional[str] = Field("", description="User full name (optional)")
    day: Optional[int] = Field(None, ge=1, le=31, description="Day of birth (1-31)")
    month: Optional[int] = Field(None, ge=1, le=12, description="Month of birth (1-12)")
    year: Optional[int] = Field(None, ge=1900, le=2100, description="Year of birth (YYYY)")
    user_id: Optional[str] = Field(None, description="User ID for usage metering")
    birth_time: Optional[str] = Field("12:00", description="Birth time in HH:MM format (e.g. 16:15 or 04:15 PM)")
    place_name: Optional[str] = Field("Delhi, India", description="Birth city/place name")
    latitude: Optional[float] = Field(None, description="Birth latitude in degrees (-90.0 to 90.0)")
    longitude: Optional[float] = Field(None, description="Birth longitude in degrees (-180.0 to 180.0)")
    timezone: Optional[str] = Field("Asia/Kolkata", description="Timezone name or UTC offset")
    chart_data: Optional[Dict[str, Any]] = Field(None, description="Optional raw planetary chart data")
    current_age: Optional[int] = Field(None, description="Optional user current age")
    premium_token: Optional[str] = Field(None, description="Optional paid subscription token")
    action: Optional[str] = Field(None, description="Optional conversational action: 'diagnose' or 'reveal_remedies'")
    context: Optional[Dict[str, Any]] = Field(None, description="Optional context object containing profile data")

import re
from typing import Tuple

def extract_dob_from_text(text: str) -> Optional[Tuple[int, int, int]]:
    """
    Parses DD-MM-YYYY, DD/MM/YYYY, DD.MM.YYYY, YYYY-MM-DD, or DD Month YYYY from free text.
    Returns (day, month, year) if valid, else None.
    """
    # 1. DD-MM-YYYY or DD/MM/YYYY or DD.MM.YYYY
    m = re.search(r'\b(\d{1,2})[-/\.](\d{1,2})[-/\.](\d{4})\b', text)
    if m:
        d, mo, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
        if 1 <= d <= 31 and 1 <= mo <= 12 and 1900 <= y <= 2100:
            return d, mo, y

    # 2. YYYY-MM-DD
    m_iso = re.search(r'\b(\d{4})[-/\.](\d{1,2})[-/\.](\d{1,2})\b', text)
    if m_iso:
        y, mo, d = int(m_iso.group(1)), int(m_iso.group(2)), int(m_iso.group(3))
        if 1 <= d <= 31 and 1 <= mo <= 12 and 1900 <= y <= 2100:
            return d, mo, y

    # 3. DD Month YYYY
    months_map = {
        'jan': 1, 'january': 1, 'feb': 2, 'february': 2, 'mar': 3, 'march': 3,
        'apr': 4, 'april': 4, 'may': 5, 'jun': 6, 'june': 6, 'jul': 7, 'july': 7,
        'aug': 8, 'august': 8, 'sep': 9, 'september': 9, 'oct': 10, 'october': 10,
        'nov': 11, 'november': 11, 'dec': 12, 'december': 12
    }
    m_word = re.search(r'\b(\d{1,2})(?:st|nd|rd|th)?\s+([A-Za-z]+)\s+(\d{4})\b', text)
    if m_word:
        d = int(m_word.group(1))
        mo_str = m_word.group(2).lower()
        y = int(m_word.group(3))
        if mo_str in months_map and 1 <= d <= 31 and 1900 <= y <= 2100:
            return d, months_map[mo_str], y

    return None

def _classify_question_topic(question: str) -> str:
    ql = question.lower()
    ql = re.sub(r'\b(carrier|carrer)\b', 'career', ql)

    # 1. Universal Obstacles Everywhere (stuck in multiple areas / all-round blockage)
    if (
        re.search(r'\b(obstacle|obstacles|stuck|blocked|problem|problems)\b.*?\b(everywhere|all sides|all areas|in everything)\b', ql) or
        re.search(r'\b(everywhere|all areas)\b.*?\b(obstacle|obstacles|stuck|blocked)\b', ql) or
        ("wealth" in ql and "career" in ql and ("marriage" in ql or "love" in ql)) or
        any(w in ql for w in ["stuck everywhere", "blocked everywhere", "universal obstacle", "karmic block", "stuck in life", "nothing working"])
    ):
        return "universal_obstacles"

    # 2. Child Conception & Progeny Blessings
    if (
        any(re.search(r'\b' + re.escape(w) + r'\b', ql) for w in [
            "conceive", "conception", "baby", "pregnant", "pregnancy", "progeny", "santan",
            "child birth", "fertility", "conceiving", "baccha", "bacha"
        ]) or
        ("child" in ql and any(w in ql for w in ["blessing", "blessings", "conceive", "birth", "fertility"]))
    ):
        return "child_conception"

    # 3. Life Partner Matching & Compatibility
    if (
        any(re.search(r'\b' + re.escape(w) + r'\b', ql) for w in [
            "partner match", "matching", "compatibility", "gun milan", "kundali match",
            "should i marry", "partner compatibility", "arranged marriage match", "horoscope match"
        ]) or
        ("match" in ql and any(w in ql for w in ["partner", "marriage", "kundali", "chart"]))
    ):
        return "partner_matching"

    # 4. Career Stuck, Job Loss, Unemployment & Layoffs
    if (
        re.search(r'\b(lost|lose|loss of|stuck in|stuck)\b.*?\b(job|career|work|naukri)\b', ql) or
        re.search(r'\b(career|job)\b.*?\b(stuck|pause|blocked|lost|loss)\b', ql) or
        any(w in ql for w in [
            "layoff", "laid off", "unemployed", "fired", "jobless", "career stuck",
            "loss of job", "lost job", "job loss", "no job", "interview rejected", "lost opportunity"
        ])
    ):
        return "career_stuck"

    # 5. Business Ventures & Partnership Issues
    if any(re.search(r'\b' + re.escape(w) + r'\b', ql) for w in [
        "partnership", "business partner", "partner dispute", "new venture with partner",
        "shared business", "trade dispute", "partnership issue", "patrenrship"
    ]):
        return "business_partnership"

    # 6. Wealth Obstacles, Debt, Financial Loss & Trapped Capital
    if (
        any(re.search(r'\b' + re.escape(w) + r'\b', ql) for w in [
            "debt", "loan", "debts", "karz", "financial crisis", "paisa doob", "wealth obstacle"
        ]) or
        re.search(r'\b(money|wealth|funds|capital)\b.*?\b(stuck|lost|trapped|drain|crisis|loss|obstacle)\b', ql)
    ):
        return "wealth_obstacles"

    # 7. Education / Studies / Teenage learning
    if any(re.search(r'\b' + re.escape(w) + r'\b', ql) for w in [
        "study", "studies", "education", "student", "learning", "school", "college",
        "teenage", "exams", "exam", "marks", "grade", "grades", "subject", "stream",
        "shiksha", "padhai", "academic", "academics", "child education"
    ]):
        return "education"

    # 8. Wealth & Finances & Investments
    elif any(re.search(r'\b' + re.escape(w) + r'\b', ql) for w in [
        "money", "wealth", "finance", "rich", "income", "salary",
        "investment", "invest", "investing", "shares", "share", "stock", "stocks", "crypto", "cryptocurrency",
        "paisa", "dhan", "trading", "mutual fund"
    ]):
        return "wealth"

    # 9. Love, Marriage & Relationships
    elif any(re.search(r'\b' + re.escape(w) + r'\b', ql) for w in [
        "marriage", "love", "relationship", "partner", "husband", "wife", "divorce",
        "dating", "shaadi", "vivah", "pyar", "spouse", "love life"
    ]):
        return "marriage"

    # 10. Career & Professional Growth
    elif any(re.search(r'\b' + re.escape(w) + r'\b', ql) for w in [
        "career", "job", "work", "business", "promotion", "profession", "boss",
        "interview", "startup", "office", "naukri", "vyapar", "kaam", "karobar",
        "trade", "market"
    ]):
        return "career"

    # 11. Health & Vitality
    elif any(re.search(r'\b' + re.escape(w) + r'\b', ql) for w in [
        "health", "illness", "disease", "body", "surgery", "mental", "stress",
        "sleep", "sehat", "bimari", "pain", "fatigue", "doctor", "treatment", "cure", "medicine", "tired", "insomnia"
    ]):
        return "health"

    # 12. Property & Assets
    elif any(re.search(r'\b' + re.escape(w) + r'\b', ql) for w in [
        "property", "house", "home", "land", "flat", "vehicle", "car", "makan", "zameen", "ghar", "vastu", "plot"
    ]):
        return "property"

    return "general"

TOPIC_FRIENDS = {
    "education":            {1, 3, 5, 6, 7},
    "career":               {1, 3, 5, 8, 9},
    "career_stuck":         {1, 3, 5, 8, 9},
    "marriage":             {2, 3, 6},
    "partner_matching":     {2, 3, 6},
    "child_conception":     {2, 3, 5, 6, 7},
    "business_partnership": {1, 3, 5, 6},
    "wealth":               {1, 5, 6},
    "wealth_obstacles":     {1, 5, 6, 8},
    "health":               {1, 2, 7},
    "property":             {4, 6, 8, 9},
    "universal_obstacles":  {1, 3, 5, 6, 8, 9},
    "general":              {1, 3, 5, 6, 9}
}

ENEMY_PAIRS = {
    (1, 8), (8, 1),
    (2, 8), (8, 2),
    (3, 6), (6, 3),
    (4, 8), (8, 4),
    (1, 4), (4, 1),
}

@router.post("/free")
def get_free_reading(req: FreeReadingRequest):
    try:
        report = generate_consensus_reading(req.name, req.day, req.month, req.year)
        response = {
            "status": "success",
            "tier": "free",
            "data": report
        }
        return apply_ai_disclosure(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/remedies")
def get_unified_7_layer_remedies(req: RemedyRequest):
    """
    Unified 7-Layer Predictions & Remedies endpoint:
    Core Matrix, Lo Shu Missing Numbers, Name Numerology, Mobile Numerology, Planetary Conjunctions, Lal Kitab & Harmonic Matrix.
    100% deterministic with grounded RAG citations.
    """
    try:
        remedy_report = generate_comprehensive_predictions_and_remedies(
            name=req.name,
            day=req.day,
            month=req.month,
            year=req.year,
            mobile_number=req.mobile_number or "",
            chart_data=req.chart_data
        )
        response = {
            "status": "success",
            "tier": "full_remedies",
            "data": remedy_report
        }
        return apply_ai_disclosure(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ask")
@router.post("/question")
def ask_question(req: OpenEndedQuestionRequest, request: Request = None):
    try:
        # Context extraction fallback for flexible frontend submissions
        if req.context and isinstance(req.context, dict):
            if (not req.name or req.name.strip().lower() == "seeker") and req.context.get("name"):
                req.name = str(req.context["name"])
            if req.context.get("day"):
                try: req.day = int(req.context["day"])
                except Exception: pass
            if req.context.get("month"):
                try: req.month = int(req.context["month"])
                except Exception: pass
            if req.context.get("year"):
                try: req.year = int(req.context["year"])
                except Exception: pass
        if req.name and req.name.strip().lower() == "seeker":
            req.name = ""

        clean_q = sanitize_user_input(req.question)

        # Detect and extract Date of Birth directly from user question if present
        dob_extracted = extract_dob_from_text(clean_q)
        if dob_extracted:
            req.day, req.month, req.year = dob_extracted
            req.current_age = max(1, 2026 - req.year)

        from app.api.charm_ai import resolve_or_create_visitor_identity
        resolved_uid = (req.user_id or "").strip()
        if not resolved_uid or resolved_uid == "guest_user":
            if request is not None:
                _, vis_hash, _ = resolve_or_create_visitor_identity(request)
                resolved_uid = f"anon_{vis_hash[:16]}"
            else:
                resolved_uid = "anon_visitor"
        req.user_id = resolved_uid

        if not (req.day and req.month and req.year):
            from app.charm.chat.response_composer import charm_chat_orchestrator
            abstain_turn = charm_chat_orchestrator.process_chat_turn(
                message=clean_q,
                user_name=req.name or "",
                day=None,
                month=None,
                year=None,
                user_id=resolved_uid,
            )
            return apply_ai_disclosure(abstain_turn.model_dump())

        # ── Enterprise Agentic AI Safety & Traceability Perimeter ──
        from app.engine.enterprise_agent_gateway import EnterpriseAgentGateway
        gateway_audit = EnterpriseAgentGateway.process_turn(
            user_prompt=clean_q,
            topic=_classify_question_topic(clean_q),
            user_id=resolved_uid
        )
        if gateway_audit.get("intercepted"):
            cb_status = gateway_audit.get("circuit_breaker", {}).get("status")
            return apply_ai_disclosure({
                "status": "success",
                "phase": "security_intercepted" if cb_status == "INTERCEPTED_PROMPT_INJECTION" else "crisis_intercepted",
                "is_freemium_gate": False,
                "is_premium": False,
                "trace_id": gateway_audit.get("trace_id"),
                "governing_policy": "/disclaimer",
                "question": clean_q,
                "direct_answer": gateway_audit.get("response"),
                "statutory_notice": gateway_audit.get("statutory_notice"),
                "remedies": []
            })
        
        # Check if user has an active paid subscription or test mode access
        from app.api.payments import get_session_info, consume_question
        from app.engine.monetization_alignment_engine import is_staging_bypass_authorized, analyze_user_alignment_and_gaps
        
        session = get_session_info(req.premium_token) if req.premium_token else None

        # Rule 3: Staging Replica Mode check
        is_staging_testing = False
        if request:
            is_staging_testing = is_staging_bypass_authorized(dict(request.headers), dict(request.query_params), req.premium_token)
        elif req.premium_token:
            is_staging_testing = is_staging_bypass_authorized({}, {}, req.premium_token)

        if is_staging_testing and not session:
            session = {
                "plan": "complete_report",
                "plan_name": "Complete Reports & Remedies (Staging Replica Preview)",
                "questions_remaining": 9999,
                "has_remedies": True,
                "status": "staging_active"
            }

        has_active_credit = bool(session and session.get("questions_remaining", 0) > 0)

        # Detect Astrotalk 2-step conversational state: Diagnosis vs Remedy Confirmation
        is_remedy_confirmation = bool(
            req.action == "reveal_remedies" or
            clean_q.lower().strip() in [
                "yes", "yes please", "reveal remedies", "suggest remedies", "show remedies",
                "how to fix", "remedies", "yes suggest remedies", "yes, suggest remedies",
                "yes reveal remedies", "yes, reveal remedies", "upay", "upaye",
                "yes please suggest remedies", "please suggest remedies", "yes suggest",
                "yes, reveal", "suggest me remedies", "can you suggest remedies", "suggest upay"
            ] or
            clean_q.lower().startswith("yes, reveal consecrated remedies") or
            clean_q.lower().startswith("reveal consecrated remedies") or
            clean_q.lower().startswith("yes, suggest remedies")
        )

        consensus_report = generate_consensus_reading(req.name, req.day, req.month, req.year)
        driver = consensus_report["vedic_numerology"]["driver_number"]
        conductor = consensus_report["vedic_numerology"]["conductor_number"]
        lo_shu_data = analyze_lo_shu_grid(req.day, req.month, req.year)
        loshu_chart_md = generate_loshu_grid_markdown(req.day, req.month, req.year)
        age_data = calculate_age_numerology(req.day, req.month, req.year, missing_numbers=lo_shu_data.get("missing_numbers", []))
        topic = _classify_question_topic(clean_q)
        topic_label = {
            "education":            "Education, Studies & Teenage Career Trajectory",
            "career":               "Career & Professional Trajectory",
            "career_stuck":         "Career Break, Job Search & Professional Healing",
            "marriage":             "Love, Marriage & Relationship Harmony",
            "partner_matching":     "Life Partner Matching & Cosmic Synergy",
            "child_conception":     "Child Conception, Progeny Blessings & Parental Harmony",
            "business_partnership": "Business Ventures & Partnership Synergy",
            "wealth":               "Wealth, Finances & Prosperity Accumulation",
            "wealth_obstacles":     "Debt Relief, Capital Unblocking & Financial Healing",
            "health":               "Vitality, Health Recovery & Nervous System Equilibrium",
            "property":             "Home, Property, Land & Spatial Vastu Alignment",
            "universal_obstacles":  "Universal Stagnation & Karmic Obstacle Clearing",
            "general":              "Life Path, Destiny Timing & Spiritual Alignment"
        }.get(topic, "Life Path & Destiny Timing")

        expl = generate_simple_explanation_and_remedies(
            clean_q,
            driver,
            conductor,
            name=req.name,
            current_age=req.current_age,
            day=req.day,
            month=req.month,
            year=req.year,
            topic=topic
        )

        paywall_spec = {
            "title": "ANVEIL EVERY CHARM to Access Full Answers",
            "subtitle": "Choose your personalized blueprint or Charm AI pass:",
            "plans": [
                {
                    "id": "rapid_action",
                    "name": "Rapid Action Plan (3-Page Executive PDF)",
                    "amount_inr": 199,
                    "original_price_inr": 399,
                    "questions_count": 5,
                    "has_remedies": True,
                    "description": "3-page targeted action plan with 2-Year Dasha Timeline & Gem/Yantra remedies"
                },
                {
                    "id": "complete_report",
                    "name": "Complete Life Dossier (12-Page Master PDF)",
                    "amount_inr": 510,
                    "original_price_inr": 999,
                    "questions_count": 15,
                    "has_remedies": True,
                    "popular": True,
                    "description": "12-page comprehensive master dossier with 10-Year Dasha, Lo Shu planes, and remedies"
                },
                {
                    "id": "imperial_blueprint",
                    "name": "Imperial Life Blueprint (32-Page Sovereign Dossier)",
                    "amount_inr": 1050,
                    "original_price_inr": 1999,
                    "questions_count": 9999,
                    "has_remedies": True,
                    "description": "32-page dual-system master blueprint with lifetime milestone roadmaps"
                },
                {
                    "id": "starter_5q",
                    "name": "Starter — 5 Questions Pass",
                    "amount_inr": 95,
                    "original_price_inr": 199,
                    "questions_count": 5,
                    "has_remedies": False,
                    "description": "5 Question Predictions across Career, Wealth, Love & Life timing"
                }
            ]
        }

        # ── ASTROTALK STEP 2: REMEDY CONFIRMATION HANDLER ────────────────────────
        if is_remedy_confirmation:
            if has_active_credit:
                consume_question(req.premium_token)
                rem_session = get_session_info(req.premium_token)
                remaining_q = rem_session.get("questions_remaining", 0) if rem_session else 0
                first_name = (req.name.split()[0] if req.name else "You").capitalize()
                remedy_response = {
                    "status": "success",
                    "phase": "remedies_revealed",
                    "is_freemium_gate": False,
                    "is_premium": True,
                    "trace_id": gateway_audit.get("trace_id"),
                    "governing_policy": "/disclaimer",
                    "plan": session.get("plan", "starter_5q"),
                    "plan_name": session.get("plan_name", "Charm AI"),
                    "questions_remaining": remaining_q,
                    "has_remedies": True,
                    "question": clean_q,
                    "classified_topic": topic,
                    "topic_display": topic_label,
                    "direct_answer": f"Namaste {first_name} 🙏 Your consecrated remedies, multi-layer rituals, and elemental attunements are detailed below. Follow these sacred protocols to neutralize friction and harmonize your {topic_label.split('&')[0].strip()} timeline.\n\n" + loshu_chart_md,
                    "loshu_grid": lo_shu_data,
                    "loshu_grid_markdown": loshu_chart_md,
                "charm_prediction": charm_prediction,
                "age_numerology": age_data,
            "age_numerology": age_data,
                "age_numerology": age_data,
                    "age_numerology": age_data,
                    "remedies": expl["remedies"],
                    "lucky_elements": expl["lucky_elements"],
                    "vedic_lifestyle_guidance": expl.get("vedic_lifestyle_guidance", {}),
                    "consultative_next_prompt": "Would you like me to inspect your upcoming milestone timeline (Dasha cycle) or analyze another life area?"
                }
                return apply_ai_disclosure(remedy_response)
            else:
                first_name = (req.name.split()[0] if req.name else "You").capitalize()
                locked_response = {
                    "status": "success",
                    "phase": "remedies_locked",
                    "is_freemium_gate": True,
                    "is_premium": False,
                    "trace_id": gateway_audit.get("trace_id"),
                    "governing_policy": "/disclaimer",
                    "question": clean_q,
                    "classified_topic": topic,
                    "topic_display": topic_label,
                    "direct_answer": f"Namaste {first_name} 🙏 To anveil your personalized consecrated remedies, multi-layer rituals, and exact planetary milestone windows, activate a Charm AI Question Pass or access your Full Master Dossier. ANVEIL EVERY CHARM.",
                    "remedies": [],
                    "remedies_gated": True,
                    "paywall": paywall_spec
                }
                return apply_ai_disclosure(locked_response)

        # ── ASTROTALK STEP 1: INITIAL QUERY DIAGNOSIS (FREE & PAID) ──────────────
        alignment_status = expl["alignment_status"]
        alignment_grade = expl["alignment_grade"]
        alignment_score = 86 if alignment_status == "ALIGNED" else 45
        alignment_summary = expl["alignment_summary"]

        from app.charm.chat.response_composer import charm_chat_orchestrator
        charm_turn = charm_chat_orchestrator.process_chat_turn(
            message=clean_q,
            user_name=req.name or "",
            day=req.day,
            month=req.month,
            year=req.year,
            user_id=req.user_id or "anon_visitor",
            tob=getattr(req, "tob", None),
            pob=getattr(req, "pob", None) or getattr(req, "city", None),
            loshu_grid=lo_shu_data
        )
        charm_prediction = charm_turn.prediction

        if not has_active_credit:
            freemium_response = {
                "status": "success" if charm_turn.status == "ANSWERED" else charm_turn.status,
                "phase": "diagnosis",
                "is_freemium_gate": True,
                "is_premium": False,
                "trace_id": gateway_audit.get("trace_id"),
                "governing_policy": "/disclaimer",
                "question": clean_q,
                "classified_topic": charm_turn.topic,
                "topic": charm_turn.topic,
                "topic_display": topic_label,
                "alignment_status": alignment_status,
                "alignment_grade": alignment_grade,
                "alignment_score": alignment_score,
                "alignment_summary": alignment_summary,
                "assistant_message": charm_turn.assistant_message,
                "human_friendly_summary": charm_turn.human_friendly_summary,
                "practical_next_steps": charm_turn.practical_next_steps,
                "follow_up_question": charm_turn.follow_up_question,
                "consensus_status": charm_turn.consensus_status,
                "direct_answer": (charm_turn.assistant_message.get("text") if (charm_turn and charm_turn.assistant_message and charm_turn.assistant_message.get("text")) else (expl["direct_answer"] + "\n\n" + loshu_chart_md)),
                "humanized_consultation": (charm_turn.assistant_message.get("text") if (charm_turn and charm_turn.assistant_message and charm_turn.assistant_message.get("text")) else expl["direct_answer"]),
                "loshu_grid": lo_shu_data,
                "loshu_grid_markdown": loshu_chart_md,
                "charm_prediction": charm_prediction,
                "age_numerology": age_data,
                "why_this_is_happening": None,
                "validation_question": expl.get("validation_question", ""),
                "permission_prompt": expl.get("permission_prompt", ""),
                "can_suggest_remedies": False,
                "remedies_gated": True,
                "remedies": [],
                "lucky_elements": expl.get("lucky_elements", {}),
                "vedic_lifestyle_guidance": {},
                "core_matrix_analysis": None,
                "grounded_citations": [],
                "driver_number": driver,
                "conductor_number": conductor,
                "preview_notice": "Your foundational numerology reading is complete. To anveil personalized consecrated remedies and multi-year timeline forecasts, choose a Charm AI pass.",
                "paywall": paywall_spec
            }
            return apply_ai_disclosure(freemium_response)

        # ── PAID SUBSCRIBER PATH ──────────────────────────────────────────────────
        if not check_and_meter_usage(req.user_id, estimated_tokens=1000, plan="premium"):
            raise HTTPException(status_code=429, detail="Credit limit reached. Please renew subscription.")

        context_history = session.get("question_history", []) if session else []
        user_profile = {
            "phase1_result": {
                "driver": driver,
                "conductor": conductor
            },
            "phase2_result": {"rashi_vs_driver": "neutral"},
            "context_history": context_history[-3:] if context_history else [],
            "chart": req.chart_data or {
                "Sun":     {"sign": "Scorpio",     "degree": 12.52, "retrograde": False},
                "Moon":    {"sign": "Sagittarius", "degree": 2.39,  "retrograde": False},
                "Mars":    {"sign": "Leo",         "degree": 27.70, "retrograde": False},
                "Mercury": {"sign": "Scorpio",     "degree": 5.75,  "retrograde": False},
                "Jupiter": {"sign": "Libra",       "degree": 6.67,  "retrograde": False},
                "Venus":   {"sign": "Sagittarius", "degree": 28.33, "retrograde": False},
                "Saturn":  {"sign": "Virgo",       "degree": 25.32, "retrograde": True},
                "Rahu":    {"sign": "Cancer",      "degree": 1.36,  "retrograde": True},
                "Ketu":    {"sign": "Capricorn",   "degree": 1.36,  "retrograde": True},
            }
        }
        
        orchestrator_output = handle_question(
            clean_q,
            user_profile,
            current_age=req.current_age or 30,
            birth_time=req.birth_time,
            place_name=req.place_name,
            latitude=req.latitude,
            longitude=req.longitude,
            timezone=req.timezone
        )
        
        # ── Professional Numerology Engine Enrichment (40 Syllabus Topics) ─────
        from app.engine.professional_numerology_engine import (
            audit_mobile_number,
            calculate_personal_cycles,
            analyze_kua_and_directions,
            analyze_share_market_profile,
            get_bonus_query_solution
        )
        from app.engine.rag_retriever import rag_engine

        prof_insights = {}
        ql = clean_q.lower()

        if any(w in ql for w in ["phone", "mobile", "sim"]):
            mob_digits = "".join(c for c in clean_q if c.isdigit())
            if len(mob_digits) >= 10:
                prof_insights["mobile_analysis"] = audit_mobile_number(mob_digits, driver=driver)

        if any(w in ql for w in ["stock", "share", "market", "trade", "trading", "invest", "nifty", "equity"]):
            prof_insights["share_market_guidance"] = analyze_share_market_profile(driver, conductor)

        if any(w in ql for w in ["child", "conceive", "pregnant", "pregnancy", "baby", "autism", "neuro", "silver square", "door", "blood"]):
            prof_insights["specialized_solution"] = get_bonus_query_solution(clean_q)

        if any(w in ql for w in ["year", "timing", "when", "future", "month", "prediction", "2026", "2025"]):
            prof_insights["personal_cycles"] = calculate_personal_cycles(req.day, req.month)

        if any(w in ql for w in ["vastu", "direction", "facing", "desk", "room", "kua"]):
            prof_insights["numero_vastu"] = analyze_kua_and_directions(gender=getattr(req, "gender", None), birth_year=req.year)

        rag_passages = rag_engine.query(clean_q, top_k=3)
        citations = [
            sanitize_citation({
                "source": p["source"],
                "location": p["location"],
                "category": "Proprietary Classical Foundation",
                "excerpt": p["content"]
            })
            for p in rag_passages
        ]

        orchestrator_output["professional_syllabus_insights"] = prof_insights
        orchestrator_output["rag_grounded_citations"] = citations

        # Enrich with simple direct answer and plain-English why-it-is-happening explanation
        expl_data = expl
        orchestrator_output["direct_answer"] = expl_data["direct_answer"]
        orchestrator_output["why_this_is_happening"] = expl_data["why_this_is_happening"]
        orchestrator_output["lucky_elements"] = expl_data["lucky_elements"]
        orchestrator_output["alignment_status"] = expl_data["alignment_status"]
        orchestrator_output["alignment_grade"] = expl_data["alignment_grade"]
        orchestrator_output["topic_display"] = topic_label

        # High-stakes topics consultation recommendation (Enquiry-First Model)
        if any(w in ql for w in ["child", "conceive", "autism", "divorce", "court", "lawsuit", "dispute", "partner"]):
            orchestrator_output["master_consultation_option"] = {
                "title": "1-on-1 Master Personal Consultation",
                "duration": "Private Master Session",
                "benefit": "Private multi-chart synthesis, Birth Epoch Verification, custom yantra preparation, and tailored practitioner guidance.",
                "booking_url": "/consultation/"
            }

        if has_active_credit and req.premium_token:
            consume_question(req.premium_token)
            session = get_session_info(req.premium_token)

        plan_code = session.get("plan", "starter_5q") if session else "starter_5q"
        has_remedies = session.get("has_remedies", False) if session else False
        remaining = session.get("questions_remaining", 0) if session else 0

        # If user bought 5 questions (no remedies included in ₹95 plan), redact remedies
        if not has_remedies:
            orchestrator_output["remedies"] = []
            orchestrator_output["gemstone_remedies"] = []
            if "specialized_solution" in prof_insights and "remedies" in prof_insights["specialized_solution"]:
                prof_insights["specialized_solution"]["remedies"] = ["Remedies locked. Upgrade to Growth (₹399) or Complete (₹1,050) to access full remedies."]
        else:
            if not orchestrator_output.get("remedies"):
                orchestrator_output["remedies"] = [
                    f"{r['title']}: {r['instruction']}" for r in expl_data["remedies"]
                ]

        # Check credits exhaustion & upscale triggers (Rule 2)
        credits_exhausted = (remaining == 0 and has_active_credit)
        dob_str = f"{req.day:02d}{req.month:02d}{req.year:04d}"
        loshu_counts = {str(i): dob_str.count(str(i)) for i in range(1, 10)}
        missing_nums = [i for i, c in loshu_counts.items() if c == 0]

        gap_data = analyze_user_alignment_and_gaps(
            driver=driver,
            conductor=conductor,
            loshu_counts=loshu_counts,
            missing_numbers=missing_nums,
            current_plan=plan_code,
            credits_remaining=remaining
        )

        response = {
            "status": "success",
            "phase": "diagnosis",
            "is_freemium_gate": False,
            "is_premium": True,
            "trace_id": gateway_audit.get("trace_id"),
            "governing_policy": "/disclaimer",
            "plan": plan_code,
            "plan_name": session.get("plan_name", "Charm AI"),
            "questions_remaining": remaining,
            "credits_exhausted": credits_exhausted,
            "has_remedies": has_remedies,
            "question": clean_q,
            "direct_answer": (charm_turn.assistant_message.get("text") if (charm_turn and charm_turn.assistant_message and charm_turn.assistant_message.get("text")) else (expl_data["direct_answer"] + "\n\n" + loshu_chart_md)),
            "humanized_consultation": (charm_turn.assistant_message.get("text") if (charm_turn and charm_turn.assistant_message and charm_turn.assistant_message.get("text")) else expl_data["direct_answer"]),
            "loshu_grid": lo_shu_data,
            "loshu_grid_markdown": loshu_chart_md,
            "age_numerology": age_data,
            "why_this_is_happening": expl_data["why_this_is_happening"],
            "validation_question": expl_data.get("validation_question", ""),
            "permission_prompt": expl_data.get("permission_prompt", ""),
            "can_suggest_remedies": True,
            "remedies": expl_data["remedies"] if has_remedies else [],
            "lucky_elements": expl_data["lucky_elements"],
            "classified_topic": orchestrator_output["classified_topic"],
            "topic_display": topic_label,
            "engines_routed": orchestrator_output["engines_routed"],
            "consensus_report": consensus_report,
            "charm_prediction": charm_prediction,
            "synthesis_result": orchestrator_output,
            "alignment_gap_analysis": gap_data
        }

        if credits_exhausted or remaining <= 0:
            response["upsell_package"] = gap_data.get("upsell_package")
            response["tagline_cta"] = gap_data.get("primary_cta", {}).get("button_text")
        if has_active_credit and req.premium_token:
            from app.api.payments import record_question_history
            record_question_history(
                req.premium_token,
                clean_q,
                expl_data.get("direct_answer", ""),
                orchestrator_output.get("classified_topic", "")
            )

        return apply_ai_disclosure(response)

    except HTTPException:
        raise
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class PackageReportRequest(BaseModel):
    name: str = Field(..., description="User full name")
    day: int = Field(..., ge=1, le=31, description="Day of birth (1-31)")
    month: int = Field(..., ge=1, le=12, description="Month of birth (1-12)")
    year: int = Field(..., ge=1900, le=2100, description="Year of birth (YYYY)")
    tier: str = Field("complete", description="Package tier: free, starter_5q, growth_10q, complete_report, report_master, report_divine, master_consultation")
    birth_time: Optional[str] = Field("11:10 AM", description="Birth time (HH:MM AM/PM)")
    birth_city: Optional[str] = Field("Chennai", description="Birth city/place")
    questions: Optional[list] = Field(None, description="Optional custom questions for starter or growth tiers")
    premium_token: Optional[str] = Field(None, description="Optional paid subscription or session token")
    user_id: Optional[str] = Field(None, description="Optional registered user account identifier")


@router.post("/package-report")
def get_package_report(req: PackageReportRequest, request: Request = None):
    """
    Returns full, package-wise detailed client reports:
    - free (Discovery Blueprint): Includes Alignment Status (ALIGNED/NOT ALIGNED), detected gaps & 'ANVEIL EVERY CHARM' CTA.
    - Paid tiers (starter_5q, growth_10q, complete_report, report_master, report_divine, etc.):
      Protected by check_report_access(). Returns 402 with gap analysis and upgrade hook if unpaid.
    - Staging replica mode: Bypasses paywall when x-staging-test-bypass header or staging_preview param is present.
    """
    from app.api.payments import check_report_access
    from app.engine.monetization_alignment_engine import analyze_user_alignment_and_gaps
    from app.engine.core_matrix_engine import calculate_driver, calculate_conductor

    # Calculate Driver & Conductor
    d = calculate_driver(req.day)
    c = calculate_conductor(req.day, req.month, req.year)
    dob_str = f"{req.day:02d}{req.month:02d}{req.year:04d}"
    loshu_counts = {str(i): dob_str.count(str(i)) for i in range(1, 10)}
    missing_numbers = [i for i, cnt in loshu_counts.items() if cnt == 0]

    # Rule 2 & 3: Check Report Access Permissions
    has_access, reason, access_data = check_report_access(
        requested_tier=req.tier,
        token=req.premium_token,
        user_id=req.user_id,
        request=request
    )

    if not has_access:
        gap_analysis = analyze_user_alignment_and_gaps(
            driver=d,
            conductor=c,
            loshu_counts=loshu_counts,
            missing_numbers=missing_numbers,
            current_plan="free"
        )
        raise HTTPException(
            status_code=402,
            detail={
                "status": "payment_required",
                "access_granted": False,
                "requested_tier": req.tier,
                "reason": reason,
                "message": f"Access to '{req.tier}' requires an active subscription or verified payment.",
                "alignment_analysis": gap_analysis,
                "hook_narrative": gap_analysis.get("hook_narrative"),
                "primary_cta": gap_analysis.get("primary_cta"),
                "tagline": "ANVEIL EVERY CHARM"
            }
        )

    try:
        from app.engine.package_report_generator import generate_package_report
        report = generate_package_report(
            name=req.name,
            day=req.day,
            month=req.month,
            year=req.year,
            package_tier=req.tier,
            birth_time=req.birth_time,
            birth_city=req.birth_city,
            user_questions=req.questions
        )

        gap_analysis = analyze_user_alignment_and_gaps(
            driver=d,
            conductor=c,
            loshu_counts=loshu_counts,
            missing_numbers=missing_numbers,
            current_plan=req.tier
        )

        report["alignment_analysis"] = gap_analysis
        report["access_status"] = {
            "authorized": True,
            "reason": reason,
            "tier": req.tier,
            "is_staging_preview": bool(access_data and access_data.get("staging_mode"))
        }

        return apply_ai_disclosure(report)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


class ResonanceFeedbackRequest(BaseModel):
    trace_id: Optional[str] = Field("NV-LIVE", description="Trace ID of the prediction turn")
    user_id: Optional[str] = Field("guest_seeker", description="User ID or session identifier")
    rating: str = Field("accurate", description="'accurate', 'partial', or 'mismatch'")
    topic: Optional[str] = Field("general", description="Classified topic of the reading")
    driver: Optional[int] = Field(None, description="Driver number (Mulank)")
    conductor: Optional[int] = Field(None, description="Conductor number (Bhagyank)")
    feedback_text: Optional[str] = Field("", description="Optional user commentary")
    question: Optional[str] = Field("", description="User question text")


@router.post("/resonance")
def submit_resonance_feedback(req: ResonanceFeedbackRequest):
    """
    Records seeker resonance feedback to build the continuous learning database,
    cross-verifying predictions and measuring live accuracy percentages.
    """
    try:
        from app.engine.charm_resonance_engine import charm_resonance
        result = charm_resonance.record_resonance(
            trace_id=req.trace_id,
            user_id=req.user_id,
            rating=req.rating,
            topic=req.topic,
            driver=req.driver,
            conductor=req.conductor,
            feedback_text=req.feedback_text,
            question=req.question
        )
        return apply_ai_disclosure(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resonance/stats")
def get_resonance_analytics():
    """
    Returns live verified prediction accuracy metrics and topic performance.
    """
    try:
        from app.engine.charm_resonance_engine import charm_resonance
        return charm_resonance.get_resonance_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/resonance/training-dataset")
def export_training_dataset(limit: int = 200):
    """
    Exports high-resonance prediction-feedback pairs for fine-tuning custom Charm AI agents.
    """
    try:
        from app.engine.charm_resonance_engine import charm_resonance
        return charm_resonance.export_training_dataset(limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


