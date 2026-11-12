"""
app/charm/intent/event_intent_service.py
=========================================
Intent Parsing & Event Definition Service for Charm AI.
Complies with Section 4 (Step 1, Step 2) and Section 6 of
the Gap-Analysis Rectification Specification, with full topic routing across
love, marriage, career, money, health_of_routine, children, property, general,
and honest unsupported-topic detection.
"""

import re
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

UNSUPPORTED_PATTERNS = [
    r"\b(lottery|jackpot|gambling|casino|betting|roulette|satta|matka|horse\s+racing)\b",
    r"\b(which\s+stock\s+to\s+buy|exact\s+stock|stock\s+tip|stock\s+tips|crypto\s+price|bitcoin\s+price|intraday\s+tip|multibagger\s+stock)\b",
    r"\b(cancer|tumor|tumour|diabetes|heart\s+attack|stroke|kidney\s+failure|surgery|operation|medication|prescription|dosage|antibiotic|diagnose\s+my|medical\s+diagnosis|cure\s+my|clinical\s+treatment|hiv|covid)\b",
    r"\b(when\s+will\s+i\s+die|date\s+of\s+death|death\s+date|death\s+prediction|lifespan|how\s+long\s+will\s+i\s+live)\b",
    r"\b(court\s+verdict|lawsuit|litigation\s+verdict|criminal\s+case\s+verdict|judge\s+ruling|bail\s+guarantee)\b",
]

EVENT_TAXONOMY = {
    "career": {
        "keywords": [
            "job", "career", "promotion", "business", "vocation", "profession",
            "boss", "interview", "startup", "office", "naukri", "vyapar",
            "senior", "appointment", "switch", "pivot", "role", "leadership",
            "position", "work", "firm", "company", "employment", "hire", "hiring",
            "promote", "promoted", "director", "raise", "increment", "appraisal", "layoff"
        ],
        "event_types": [
            "new_job_or_senior_role",
            "promotion",
            "career_change",
            "business_venture",
            "executive_appointment"
        ]
    },
    "marriage": {
        "keywords": [
            "marriage", "marry", "married", "husband", "wife", "spouse",
            "shaadi", "vivah", "wedding", "marital", "engagement", "fiance",
            "fiancee", "kundali", "arranged marriage", "bridal", "groom"
        ],
        "event_types": [
            "marriage_timing", "spousal_harmony", "arranged_or_love_union"
        ]
    },
    "love": {
        "keywords": [
            "love", "romance", "romantic", "dating", "boyfriend", "girlfriend",
            "crush", "affection", "relationship", "partner", "breakup", "heartbreak",
            "chemistry", "soulmate"
        ],
        "event_types": [
            "romantic_alignment", "relationship_harmony", "partner_meeting"
        ]
    },
    "money": {
        "keywords": [
            "money", "wealth", "finance", "financial", "income", "salary",
            "savings", "investment", "debt", "loan", "paisa", "dhan",
            "cashflow", "budget", "expenses", "prosperity"
        ],
        "event_types": [
            "financial_stability", "capital_gain", "debt_clearance", "savings_discipline"
        ]
    },
    "health_of_routine": {
        "keywords": [
            "routine", "habit", "habits", "sleep", "energy", "vitality",
            "wellness", "sehat", "stress", "fatigue", "burnout", "rest",
            "waking", "morning", "circadian", "stamina", "balance", "schedule"
        ],
        "event_types": [
            "daily_routine_balance", "sleep_and_energy_rhythm", "stress_reduction"
        ]
    },
    "children": {
        "keywords": [
            "child", "children", "baby", "kids", "kid", "son", "daughter",
            "parenting", "conceive", "conception", "progeny", "santan",
            "pregnancy", "pregnant", "studies", "school", "exam", "newborn"
        ],
        "event_types": [
            "children_and_family_harmony", "child_education_focus", "progeny_timing"
        ]
    },
    "property": {
        "keywords": [
            "property", "house", "home", "land", "flat", "apartment", "plot",
            "vehicle", "car", "makan", "zameen", "ghar", "vastu", "relocation",
            "address", "rent", "real estate"
        ],
        "event_types": [
            "property_purchase", "relocation", "home_vastu_alignment"
        ]
    },
    "general": {
        "keywords": ["life", "destiny", "timing", "cycle", "future", "numbers", "charm", "overview", "personal year", "loshu"],
        "event_types": ["annual_forecast", "destiny_milestone", "dasha_alignment"]
    }
}

class EventIntent(BaseModel):
    event_definition_id: str
    event_family: str = Field(..., description="love, marriage, career, money, health_of_routine, children, property, general, unsupported")
    event_type: str = Field(..., description="Specific event type")
    event_definition: str = Field(..., description="Human-readable event description")
    goal_or_problem: str
    requested_horizon: str = Field("unspecified_horizon", description="User's requested forecast window, separated from calculated timing")
    available_inputs: List[str] = Field(default_factory=list)
    missing_inputs: List[str] = Field(default_factory=list)
    required_rules: List[str] = Field(default_factory=list)
    blocked_calculations: List[str] = Field(default_factory=list)
    safe_interim_conclusions: List[str] = Field(default_factory=list)
    needs_clarification: bool = False
    clarification_question: Optional[str] = None
    provenance_notes: List[str] = Field(default_factory=list)

class EventIntentService:
    def is_unsupported_query(self, question: str) -> Optional[str]:
        ql = (question or "").strip().lower()
        for pat in UNSUPPORTED_PATTERNS:
            m = re.search(pat, ql)
            if m:
                return m.group(0)
        return None

    def parse_intent(self, question: str, profile_facts: Dict[str, Any]) -> EventIntent:
        clean_q = (question or "").strip()
        ql = clean_q.lower()

        # 1. Parse Requested Forecast Horizon (explicitly separate from calculated timing)
        requested_horizon = "unspecified_horizon"
        if re.search(r'\b(6|six)\s*(month|months|mo)\b', ql) or "half year" in ql:
            requested_horizon = "6_months"
        elif re.search(r'\b(3|three)\s*(month|months|quarter)\b', ql):
            requested_horizon = "3_months"
        elif re.search(r'\b(1|one|12)\s*(year|years|months|yr)\b', ql) or "2026" in ql or "2027" in ql or "this year" in ql:
            requested_horizon = "12_months"
        elif re.search(r'\b(2|two|24)\s*(years|months|yrs)\b', ql):
            requested_horizon = "24_months"

        # 2. Check Unsupported Scope First (Medical / Gambling / Legal Verdict / Death)
        unsupported_match = self.is_unsupported_query(ql)
        if unsupported_match:
            has_dob = bool(profile_facts.get("day") and profile_facts.get("month") and profile_facts.get("year"))
            avail = ["birth_date"] if has_dob else []
            return EventIntent(
                event_definition_id="EVT-UNSUPPORTED-OUT_OF_SCOPE",
                event_family="unsupported",
                event_type="out_of_scope_inquiry",
                event_definition="Topic outside deterministic numerology scope",
                goal_or_problem=clean_q,
                requested_horizon=requested_horizon,
                available_inputs=avail,
                missing_inputs=[],
                required_rules=[],
                blocked_calculations=["Out-of-scope domain (medical, gambling/speculative picks, legal verdict, or lifespan)"],
                safe_interim_conclusions=[
                    "Charm AI covers personal timing and daily habits across love, marriage, career, money discipline, daily routine, family/children, and property.",
                    "It does not provide medical diagnoses, gambling/stock picks, legal verdicts, or lifespan predictions."
                ],
                needs_clarification=False,
                clarification_question=None,
                provenance_notes=[f"Matched unsupported domain indicator: {unsupported_match}"]
            )

        # 3. Identify Event Family with Multi-Phrase Priority Disambiguation
        matched_family = "general"
        if any(p in ql for p in ["daily routine", "sleep routine", "morning routine", "health of routine", "sleep schedule", "work-life balance", "energy routine"]):
            matched_family = "health_of_routine"
        elif any(p in ql for p in ["buy a house", "buy a home", "buy a flat", "new house", "new flat", "house number", "flat number", "property numerology", "vehicle number"]):
            matched_family = "property"
        elif any(p in ql for p in ["our child", "my child", "my son", "my daughter", "my kids", "have a baby", "baby name", "child studies"]):
            matched_family = "children"
        elif any(re.search(r'\b' + re.escape(k) + r'\b', ql) for k in ["marriage", "marry", "married", "husband", "wife", "spouse", "shaadi", "vivah", "wedding", "marital", "engagement", "kundali"]):
            matched_family = "marriage"
        elif any(re.search(r'\b' + re.escape(k) + r'\b', ql) for k in ["love", "romance", "romantic", "dating", "boyfriend", "girlfriend", "crush", "soulmate", "breakup", "heartbreak"]):
            matched_family = "love"
        else:
            highest_score = 0
            priority_order = ["children", "property", "health_of_routine", "money", "marriage", "love", "career", "general"]
            for family in priority_order:
                data = EVENT_TAXONOMY[family]
                score = sum(1 for kw in data["keywords"] if re.search(r'\b' + re.escape(kw) + r'\b', ql))
                if score > highest_score:
                    highest_score = score
                    matched_family = family

        # 4. Disambiguate Specific Event Type
        if matched_family == "career":
            if any(k in ql for k in ["promotion", "promoted", "promote", "hike", "appraisal", "increment", "level up"]):
                matched_type = "promotion"
            elif any(k in ql for k in ["change career", "career switch", "switch career", "new profession", "different field", "switch fields"]):
                matched_type = "career_change"
            elif any(k in ql for k in ["senior", "leadership", "executive", "director", "head", "lead", "job", "role", "naukri", "interview"]):
                matched_type = "new_job_or_senior_role"
            elif any(k in ql for k in ["business", "startup", "venture", "freelance", "founder", "own firm", "company"]):
                matched_type = "business_venture"
            elif any(k in ql for k in ["change", "switch", "pivot"]):
                matched_type = "career_change"
            else:
                matched_type = "new_job_or_senior_role"
        else:
            event_types = EVENT_TAXONOMY[matched_family]["event_types"]
            matched_type = event_types[0]
            for et in event_types:
                words = et.split("_")
                if any(w in ql for w in words if len(w) > 3):
                    matched_type = et
                    break

        # 5. Input & Evidence Validation
        available = []
        missing = []
        blocked = []
        provenance = []

        if profile_facts.get("name"):
            available.append("user_name")

        has_day = bool(profile_facts.get("day"))
        has_month = bool(profile_facts.get("month"))
        has_year = bool(profile_facts.get("year"))

        if has_day and has_month and has_year:
            available.append("birth_date")
            provenance.append("User-supplied Date of Birth (pending practitioner verification)")
        else:
            missing.append("birth_date")
            blocked.append("Deterministic Numerology Dasha timing calculation")
            blocked.append("Acute Pratyantardasha window estimation")

        if profile_facts.get("loshu_grid") or profile_facts.get("digit_counts"):
            available.append("user_supplied_loshu")
            provenance.append("User-supplied Lo Shu numbers retained as static natal inventory (does not establish Dasha timing)")

        if profile_facts.get("tob"):
            available.append("time_of_birth")
        if profile_facts.get("pob") or profile_facts.get("city"):
            available.append("city_of_birth")

        # 6. Formulate Human-Readable Event Definition
        definition_map = {
            "new_job_or_senior_role": "Transition into a new job or senior institutional leadership appointment",
            "promotion": "Institutional promotion, band advancement, or executive authority expansion",
            "career_change": "Strategic career pivot into a new operational domain",
            "business_venture": "Commercial venture expansion and independent market agility",
            "romantic_alignment": "Romantic harmony, emotional communication, and dating compatibility",
            "relationship_harmony": "Mutual affection, emotional balance, and relationship trust",
            "partner_meeting": "Meeting a compatible romantic partner and building steady connection",
            "marriage_timing": "Marriage timing window, family alignment, and long-term spousal union",
            "spousal_harmony": "Spousal communication, domestic warmth, and shared household peace",
            "arranged_or_love_union": "Evaluating self-chosen versus family-introduced marriage alignment",
            "financial_stability": "Cashflow discipline, structured savings, and long-term financial steadiness",
            "capital_gain": "Financial milestone and steady capital accumulation",
            "debt_clearance": "Structured debt reduction and monthly cashflow recovery",
            "savings_discipline": "Plugging recurring leaks and building long-term financial reserves",
            "daily_routine_balance": "Daily routine structure, circadian rest, and non-medical energy pacing",
            "sleep_and_energy_rhythm": "Consistent sleep schedule, morning grounding, and steady focus blocks",
            "stress_reduction": "Calm daily pacing, screen boundaries, and nervous-system rest habits",
            "children_and_family_harmony": "Parenting warmth, family communication, and household routine for children",
            "child_education_focus": "Supportive study environment, focus sprints, and encouragement for children",
            "progeny_timing": "Family readiness, calm household rhythm, and supportive timing cycles",
            "property_purchase": "Home, flat, or land evaluation, address compatibility, and purchase timing",
            "relocation": "Moving house, city transition, and settling into a harmonious space",
            "home_vastu_alignment": "Directional desk/room orientation and practical household Vastu balance",
            "annual_forecast": "Personal Year cycle, core numbers, and balanced milestone planning",
            "destiny_milestone": "Mulank, Bhagyank, and Lo Shu alignment across the current Personal Year",
            "dasha_alignment": "Active Numerology Dasha cycle and grounded everyday priorities"
        }
        event_definition = definition_map.get(matched_type, f"Event timing and planetary alignment for {matched_family}")
        event_id = f"EVT-{matched_family.upper()}-{matched_type.upper()}"

        # 7. Safe Interim Conclusions when data is partial
        interim = []
        if "birth_date" not in available:
            interim.append("Static natal frequency insights can be reviewed once birth date is confirmed.")
            interim.append("No specific event dates or favourable months can responsibly be calculated without a verified birth date.")
        else:
            interim.append("Birth date confirmed; timing calculations ready for deterministic evaluation.")

        # 8. Single Concise Clarification Question
        needs_clarification = len(missing) > 0
        clarification_q = None
        if "birth_date" in missing:
            clarification_q = "Please enter your Date of Birth (Day, Month, Year) first so Charm AI can calculate your numbers and timing window."

        required_rules = [
            "SRC-NV-001: Numerology Dasha 9-Year Epicycle Rules",
            f"SRC-NV-003: Deterministic {matched_family.replace('_', ' ').title()} Alignment Rules"
        ]

        return EventIntent(
            event_definition_id=event_id,
            event_family=matched_family,
            event_type=matched_type,
            event_definition=event_definition,
            goal_or_problem=clean_q,
            requested_horizon=requested_horizon,
            available_inputs=available,
            missing_inputs=missing,
            required_rules=required_rules,
            blocked_calculations=blocked,
            safe_interim_conclusions=interim,
            needs_clarification=needs_clarification,
            clarification_question=clarification_q,
            provenance_notes=provenance
        )

event_intent_service = EventIntentService()
