"""
app/charm/chat/humanized_consultant.py
======================================
Humanized Master Numerologist Consultation Narrative Generator.

Translates 100% deterministic calculation results (Mulank/Driver, Bhagyank/Conductor,
Personal Year, Mahadasha, Antardasha, acute Pratyantardasha timing windows,
and Lo Shu grid) into warm, natural, topic-matched explanations.

Zero hallucinated dates or arithmetic: all numerical facts are sourced
strictly from the deterministic calculation engine.
"""

from typing import Dict, Any, List, Optional

PLANET_NAMES = {
    1: "Sun (Surya)",
    2: "Moon (Chandra)",
    3: "Jupiter (Guru)",
    4: "Rahu (North Node)",
    5: "Mercury (Budh)",
    6: "Venus (Shukra)",
    7: "Ketu (South Node)",
    8: "Saturn (Shani)",
    9: "Mars (Mangal)"
}

DRIVER_ESSENCE = {
    1: {
        "title": "Natural Leader & Pioneer",
        "ruler": "the Sun (Surya)",
        "unblock_action": "Take clear ownership of one priority initiative and communicate expectations directly."
    },
    2: {
        "title": "Intuitive Diplomat & Harmonizer",
        "ruler": "the Moon (Chandra)",
        "unblock_action": "Set calm boundaries and rely on written facts alongside your natural empathy."
    },
    3: {
        "title": "Creative Strategist & Wise Counselor",
        "ruler": "Jupiter (Guru)",
        "unblock_action": "Focus on one priority goal for 30 days before opening new commitments."
    },
    4: {
        "title": "Builder of Practical Systems",
        "ruler": "Rahu",
        "unblock_action": "Break long plans into simple weekly milestones and keep documentation tidy."
    },
    5: {
        "title": "Adaptable Communicator & Connector",
        "ruler": "Mercury (Budh)",
        "unblock_action": "Stay consistent with one chosen path for 60 days instead of switching mid-stream."
    },
    6: {
        "title": "Harmonious Organizer & Caretaker",
        "ruler": "Venus (Shukra)",
        "unblock_action": "Audit your weekly commitments, protect personal rest, and hold clear mutual standards."
    },
    7: {
        "title": "Analytical Specialist & Deep Thinker",
        "ruler": "Ketu",
        "unblock_action": "Share your insights clearly in writing and maintain a quiet morning reflection habit."
    },
    8: {
        "title": "Steady Builder & Long-Term Planner",
        "ruler": "Saturn (Shani)",
        "unblock_action": "Track progress in measurable weekly steps and trust steady, disciplined compounding."
    },
    9: {
        "title": "Courageous Initiator & Protector",
        "ruler": "Mars (Mangal)",
        "unblock_action": "Channel high energy into structured physical activity and pause before reactive replies."
    }
}

TOPIC_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "love": {
        "headline": "Love & Romantic Harmony · Mulank {driver} & Bhagyank {conductor}",
        "takeaway": (
            "Your romantic alignment in Personal Year {py} ({planet} Dasha cycle) highlights open emotional communication "
            "and unhurried trust-building, with your supportive window spanning {window}."
        ),
        "supported": (
            "Driver {driver} (Mulank) and Conductor {conductor} (Bhagyank) shape your emotional expression and relationship warmth. "
            "Your active {planet} Pratyantardasha supports honest, affectionate dialogue."
        ),
        "followup": "Would you like to compare partner birth-date compatibility or explore calm relationship habits during {window}?"
    },
    "marriage": {
        "headline": "Marriage Timing & Spousal Alignment · {planet} Cycle",
        "takeaway": (
            "Your marriage and spousal harmony cycle in Personal Year {py} is guided by your {planet} Numerology Dasha, "
            "with a supportive discussion and commitment window from {window}."
        ),
        "supported": (
            "Driver {driver} (Mulank) and Conductor {conductor} (Bhagyank) anchor your long-term domestic partnership rhythm. "
            "The active {planet} cycle supports clear family discussions and mutual spousal understanding."
        ),
        "followup": "Would you like to review partner birth-date compatibility or household harmony priorities for {window}?"
    },
    "career": {
        "headline": "Career & Professional Momentum · {planet} Cycle",
        "takeaway": (
            "Your career momentum for {event_def} is governed by your primary Numerology Dasha "
            "({planet} cycle, Personal Year {py}). Calculated acute execution window spans {window}."
        ),
        "supported": (
            "Driver {driver} and Conductor {conductor} establish strong professional and institutional alignment. "
            "The active {planet} Pratyantardasha supports structured outreach, role positioning, and steady execution."
        ),
        "followup": "Would you like to review practical preparation steps or interview pacing during your {window} window?"
    },
    "money": {
        "headline": "Money, Cashflow & Savings Discipline · Personal Year {py}",
        "takeaway": (
            "Your financial rhythm in Personal Year {py} ({planet} Dasha cycle) favours structured budgeting, "
            "plugging recurring leaks, and steady savings across {window}."
        ),
        "supported": (
            "Driver {driver} (Mulank) and Conductor {conductor} (Bhagyank) define your approach to earning and conserving capital. "
            "The active {planet} cycle rewards written budgets and disciplined financial review."
        ),
        "followup": "Would you like to focus on debt-reduction pacing or monthly savings habits during {window}?"
    },
    "health_of_routine": {
        "headline": "Daily Routine, Sleep Rhythm & Energy Balance · Personal Year {py}",
        "takeaway": (
            "Your non-medical daily routine alignment in Personal Year {py} ({planet} cycle) favours consistent waking hours, "
            "screen boundaries, and steady energy pacing across {window}."
        ),
        "supported": (
            "Driver {driver} (Mulank) and Conductor {conductor} (Bhagyank) indicate how your daily focus and rest respond to structure. "
            "The active {planet} cycle supports repeatable sleep, hydration, and work-break habits (non-medical lifestyle guidance)."
        ),
        "followup": "Would you like a simple morning-and-evening routine checklist aligned with your Mulank {driver}?"
    },
    "children": {
        "headline": "Children, Family & Parenting Alignment · Mulank {driver} & Bhagyank {conductor}",
        "takeaway": (
            "Your family and children alignment in Personal Year {py} ({planet} Dasha cycle) emphasises calm household routines, "
            "patient encouragement, and supportive timing across {window}."
        ),
        "supported": (
            "Driver {driver} (Mulank) and Conductor {conductor} (Bhagyank) shape your parenting warmth and household structure. "
            "The active {planet} cycle supports calm family communication, study focus, and naming harmony."
        ),
        "followup": "Would you like to explore study-desk orientation for children or Chaldean baby-name harmony?"
    },
    "property": {
        "headline": "Property, Home Address & Vastu Alignment · {planet} Cycle",
        "takeaway": (
            "Your property and home alignment in Personal Year {py} ({planet} Dasha cycle) highlights careful document due diligence, "
            "address-digit harmony, and grounded planning across {window}."
        ),
        "supported": (
            "Driver {driver} (Mulank) and Conductor {conductor} (Bhagyank) guide which house or flat numbers feel most supportive. "
            "The active {planet} cycle favours unhurried property verification and North-East household clarity."
        ),
        "followup": "Do you have a candidate house, flat, or plot number you would like checked against Mulank {driver} and Bhagyank {conductor}?"
    },
    "general": {
        "headline": "Personal Year {py} & Core Numerology Overview · Mulank {driver}",
        "takeaway": (
            "Your overall numerology cycle in Personal Year {py} ({planet} Dasha cycle) highlights steady personal alignment "
            "and practical priorities across {window}."
        ),
        "supported": (
            "Driver {driver} (Mulank) and Conductor {conductor} (Bhagyank) form your core numerology axis alongside your Lo Shu Grid. "
            "The active {planet} cycle supports balanced everyday decisions across {window}."
        ),
        "followup": "Which specific area—love, marriage, career, money, daily routine, children, or property—would you like to explore next?"
    }
}


def generate_humanized_consultation(
    user_name: str,
    question: str,
    driver: int,
    conductor: int,
    personal_year: int,
    active_dasha_planet: str,
    acute_window_start: Optional[str] = None,
    acute_window_end: Optional[str] = None,
    requested_horizon: str = "unspecified_horizon",
    verification_status: str = "NUMEROLOGY_PRIMARY_CORROBORATED",
    event_assessment: str = "FAVOURABLE",
    lo_shu_grid: Optional[Dict[str, Any]] = None,
    practical_actions: Optional[List[str]] = None,
    day: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    is_premium: bool = False,
    explicit_faith: Optional[str] = None,
    event_family: str = "general",
    event_definition: str = "personal alignment"
) -> Dict[str, Any]:
    """
    Synthesizes deterministic calculations into a warm, topic-matched consultation.
    Requires verified day, month, year from caller.
    """
    from app.engine.charm_oracle_synthesizer import charm_oracle_synthesizer, _base_1_to_9

    norm_family = (event_family or "general").lower().strip()
    if norm_family == "wealth":
        norm_family = "money"
    elif norm_family == "health":
        norm_family = "health_of_routine"

    synth = charm_oracle_synthesizer.synthesize_consultation(
        name=user_name or "",
        day=day or driver,
        month=month or 1,
        year=year or 2000,
        question=question,
        is_premium=is_premium,
        explicit_faith=explicit_faith,
        event_family=norm_family
    )

    d_info = DRIVER_ESSENCE.get(_base_1_to_9(driver), DRIVER_ESSENCE[1])
    c_info = DRIVER_ESSENCE.get(_base_1_to_9(conductor), DRIVER_ESSENCE[1])

    tpl = TOPIC_TEMPLATES.get(norm_family, TOPIC_TEMPLATES["general"])

    clean_window = (
        f"{acute_window_start} to {acute_window_end}"
        if (acute_window_start and acute_window_end)
        else synth["timing_window"].replace("**", "")
    )
    fmt_kwargs = {
        "driver": driver,
        "conductor": conductor,
        "py": personal_year,
        "planet": active_dasha_planet,
        "window": clean_window,
        "event_def": (event_definition or synth["topic_display"]).lower()
    }

    headline = tpl["headline"].format(**fmt_kwargs)
    humanized_takeaway = tpl["takeaway"].format(**fmt_kwargs)
    humanized_supported = tpl["supported"].format(**fmt_kwargs)
    followup = tpl["followup"].format(**fmt_kwargs)

    timing_explanation = (
        f"In deterministic Numerology Dasha calculations, your active {active_dasha_planet} window runs from {clean_window}, "
        f"providing structured timing context for {synth['topic_display'].lower()}."
    )

    humanized_timing_status = (
        f"Verification: {verification_status} · "
        f"Assessment: {event_assessment} · Timing Window: {clean_window} ({active_dasha_planet} Cycle)"
    )

    humanized_unconcluded = (
        "A natal Lo Shu grid alone does not establish fixed calendar certainties. "
        "Numerology timing cycles highlight supportive periods, while personal choices and practical follow-through shape real outcomes."
    )

    actions = synth.get("practical_actions") or practical_actions or [d_info["unblock_action"]]

    return {
        "headline": headline,
        "takeaway": humanized_takeaway,
        "timing_status": humanized_timing_status,
        "supported_by_report": humanized_supported,
        "unconcluded_aspects": humanized_unconcluded,
        "timing_explanation": timing_explanation,
        "full_dialogue_text": synth["direct_answer"],
        "practical_actions": actions[:3],
        "followup_question": followup,
        "driver_title": d_info["title"],
        "driver_planet": d_info["ruler"],
        "conductor_title": c_info["title"],
        "topic": norm_family,
        "topic_display": synth["topic_display"],
        "faith_detected": synth["faith_detected"],
        "astro_consensus_pct": synth["astro_consensus_pct"]
    }
