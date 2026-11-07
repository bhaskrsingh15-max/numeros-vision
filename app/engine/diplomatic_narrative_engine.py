"""
DIPLOMATIC NARRATIVE & PRESENTATION HARMONIZER ENGINE
Numeros Vision — ANVEIL EVERY CHARM

PURPOSE:
Translates complex, technical multi-engine outputs (Vedic, BNN, KP, Lal Kitab, Lo Shu, Cheiro)
into simple, elegant, positive, diplomatic, and legally safe guidance for clients.

CORE ARCHITECTURAL RULES:
1. ZERO TECHNICAL JARGON:
   - Strips out internal engine names (BNN, KP, Lal Kitab, Swiss Ephemeris, Lo Shu, RAG, Mulank, Bhagyank, Nakshatras).
   - Uses generalized, universally understood terms: "Core Natural Frequency", "Life Direction Energy",
     "Current Planetary Phase", "Upcoming Growth Window", "Natural Energy Balance".
2. DIPLOMATIC PROBLEM FRAMING:
   - Never uses fatalistic, fearful, or negative doomspeak ("ruin", "failure", "bad luck", "curse", "divorce").
   - Frames friction as "temporary energetic blockages" or "restructuring phases".
   - Always follows challenges immediately with practical, empowering solutions (Networking for career,
     conservative holding for money, mindful communication for relationships, grounding routines for vitality).
3. LEGALLY SAFE WITHOUT DEFENSIVE DISCLAIMERS:
   - Never over-promises or guarantees outcomes ("guaranteed fix", "100% solved").
   - Uses supportive probabilistic phrasing: "These practices help harmonize energy flow",
     "helps remove subtle blockages and enhance your receptivity to upcoming opportunities".
   - Completely avoids ugly, trust-breaking disclaimers ("AI might be wrong", "entertainment only").
     The legal safety is embedded organically into the respectful, measured, and positive choice of words.
"""

import re
from typing import Dict, Any, List, Optional

# ── 1. OCCULT ASTROLOGY JARGON NORMALIZATION MAP (For User-Facing Cleanliness) ──
# Occult astrology methods run silently in backend AI Charm for cross-verification;
# user-facing reports retain 100% Pure Numerology terminology (Mulank, Bhagyank, Lo Shu, Chaldean).
JARGON_REPLACEMENTS = [
    # Occult Astrology Jargon Scrubbing
    (r"\bBhrigu Nandi Nadi\b", "Planetary Alignment System"),
    (r"\bBNN\b", "Planetary Energy"),
    (r"\bLal Kitab\b", "Traditional Remedial Balance"),
    (r"\bKP Astrology\b", "Precision Planetary Timing"),
    (r"\bKP Sub-Lord\b", "Precision Timing Indicator"),
    (r"\bSub-Lord\b", "Timing Indicator"),
    (r"\bNakshatras?\b", "Lunar Energy Zone"),
    (r"\bLagna\b", "Rising Profile"),
    (r"\bKundali\b", "Harmonic Chart"),
    (r"\bNavamsha\b", "Harmonic Divisional Matrix"),
    (r"\bNumerology Dasha Dasha\b", "Planetary Time Cycle"),
    (r"\bMahadashas?\b", "Major Energy Period"),
    (r"\bAntardashas?\b", "Active Sub-Phase"),
    (r"\bPratyantars?\b", "Refined Current Rhythm"),
    (r"\bDhana Yoga\b", "Wealth Compounding Alignment"),
    (r"\bYogakaraka\b", "Most Favorable Supportive Planet"),
    (r"\bDigbala\b", "Peak Natural Strength"),
    (r"\bMasnooi\b", "Combined Planetary Energy"),
    (r"\bAstrologer('s)?\b", "Numerologist"),
    (r"\bAstrological\b", "Numerological"),
    (r"\bAstrology\b", "Numerology"),
    (r"\bRAG\b", "Verified Knowledge Base"),
]

# ── 2. SENSITIVE WORDS SANITIZATION MAP (Replaces negative doomspeak with diplomatic alternatives) ──
SENSITIVE_WORDS_MAP = [
    (r"\bdisaster(s)?\b", "significant life pivot"),
    (r"\bruin\b", "financial restructuring"),
    (r"\bcurse(d)?\b", "unresolved energetic blockage"),
    (r"\bbad luck\b", "testing cycle requiring patience"),
    (r"\benemy numbers?\b", "contrasting frequencies requiring conscious balance"),
    (r"\bmalefic\b", "challenging or intense"),
    (r"\bpitfall\b", "area requiring mindful attention"),
    (r"\bdivorce\b", "deep relationship evaluation"),
    (r"\bdeadly\b", "demanding"),
    (r"\bfailure\b", "temporary delay"),
    (r"\bpoverty\b", "financial constriction"),
    (r"\bguaranteed?\b", "designed to support"),
    (r"\b100%\b", "optimally"),
]

def sanitize_text(text: str) -> str:
    """Removes technical jargon and fatalistic phrases, replacing them with diplomatic terms."""
    result = text
    for pattern, replacement in JARGON_REPLACEMENTS:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    for pattern, replacement in SENSITIVE_WORDS_MAP:
        result = re.sub(pattern, replacement, result, flags=re.IGNORECASE)
    return result


# ── 3. DOMAIN-SPECIFIC POSITIVE ACTIONABLE HARMONIZERS ─────────────────────────
DOMAIN_ACTION_GUIDANCE = {
    "career": {
        "theme": "Professional Flow & Vocational Timing",
        "blockage_framing": (
            "During this period, you may notice that certain career initiatives require extra patience or multiple follow-ups. "
            "This is not a sign of stagnation, but rather an energetic signal to refine systems, eliminate redundancies, and build solid foundations."
        ),
        "practical_solutions": [
            "Proactive Professional Networking: Reach out to trusted mentors, former colleagues, and strategic industry peers to exchange perspectives without immediate pressure.",
            "Documented Clear Agreements: Ensure all project expectations, responsibilities, and deliverables are set in writing rather than relying on informal verbal assurances.",
            "Strategic Skill Consolidation: Dedicate time to mastering one specialized tool or high-value capability that makes your work irreplaceable.",
            "Diplomatic Workpace Diplomacy: Maintain an adaptable, calm posture during team meetings, allowing your consistent deliverables to speak for your authority."
        ],
        "energy_enhancement": (
            "Aligning with your auspicious directional orientations and using supportive workspace elements helps dissolve subtle resistance, "
            "enhancing your natural clarity and opening channels for executive recognition."
        )
    },
    "wealth": {
        "theme": "Financial Stability & Wealth Preservation",
        "blockage_framing": (
            "The current energetic rhythm asks you to be a vigilant steward of your resources. "
            "While income pathways remain active, expenditures or sudden family obligations may test your reserves."
        ),
        "practical_solutions": [
            "Conservative Asset Anchoring: Whenever surplus liquid funds arrive, systematically move a designated portion into secure, compounding, long-term instruments before daily discretionary spending takes hold.",
            "Avoid High-Stakes Speculation: This phase favors steady, methodical compounding over risky shortcuts or untested investment schemes.",
            "Selective Financial Boundaries: Politely decline requests to co-sign obligations or extend emotional loans that could strain your cash reserves.",
            "Clear Budget Auditing: Review recurring subscriptions, overheads, and vendor contracts to tighten financial flow."
        ],
        "energy_enhancement": (
            "Integrating grounding earth and metallic accents in your primary financial corner supports wealth retention, "
            "helping anchor cash flow into lasting security."
        )
    },
    "marriage": {
        "theme": "Relationship Harmony & Emotional Alignment",
        "blockage_framing": (
            "Planetary cycles in this phase emphasize personal growth, which can occasionally bring differing expectations between partners into the open. "
            "This phase is designed to deepen mutual understanding rather than force immediate consensus."
        ),
        "practical_solutions": [
            "Active Empathetic Listening: Make conscious space for uninterrupted dialogue, listening to understand your partner's emotional state rather than reacting.",
            "De-escalate Ego Debates: When sensitive topics arise, choose gentle pauses over impulsive arguments, allowing calm perspectives to prevail.",
            "Shared Quality Rituals: Carve out small, simple weekly routines—such as a quiet walk in nature or sharing a wholesome meal—to nurture emotional warmth.",
            "Respecting Personal Space: Allow each partner healthy room for individual interests and self-reflection without viewing it as emotional distance."
        ],
        "energy_enhancement": (
            "Harmonizing your shared living space with soothing, natural colors and soft lighting creates an ambient sanctuary "
            "that naturally diffuses tension and encourages affectionate communication."
        )
    },
    "health": {
        "theme": "Vitality, Inner Calm & Physical Wellness",
        "blockage_framing": (
            "Your energetic chart indicates an active, high-processing mind that can occasionally create physical fatigue or digestive sensitivity. "
            "Your body is asking for rhythmic pacing rather than relentless exertion."
        ),
        "practical_solutions": [
            "Consistent Grounding Sleep Rhythm: Establish a digital-free wind-down routine 45 minutes before sleep to ease mental activity and restore deep rest.",
            "Mindful Hydration & Nutrition: Incorporate fresh, warm, easily digestible foods and stay well-hydrated throughout the day.",
            "Gentle Daily Movement: Practice daily morning stretching, gentle walking in morning sunlight, or mindful breathwork to release neck and back tension.",
            "Mental Decluttering: Spend 10 minutes journaling your thoughts or sitting in quiet meditation to reset your nervous system."
        ],
        "energy_enhancement": (
            "Working with natural crystals and natural sunlight acts as a gentle, non-invasive catalyst to replenish your vitality, "
            "supporting your body's natural resilience."
        )
    }
}


def create_diplomatic_narrative(
    user_name: str,
    topic: str,
    time_period_summary: str,
    blockage_notes: Optional[str] = None,
    supportive_remedies: Optional[List[Dict[str, Any]]] = None,
    favorable_window: Optional[str] = None
) -> Dict[str, Any]:
    """
    Synthesizes a complete, diplomatic, positive, and legally safe guidance narrative.
    
    Structure:
    1. Warm, dignified greeting acknowledging the client.
    2. Diplomatic assessment of the current time cycle (reframing friction as energetic calibration).
    3. Actionable strategic recommendations tailored to the domain (Networking, Budgeting, Calming Communication, Vitality).
    4. Practical, non-overpromising remedies (Colors, Spatial direction, Gemstone/Crystal energy, Daily habits).
    5. The upcoming favorable growth window and positive closing encouragement.
    """
    clean_name = user_name.strip().title() if user_name else "Friend"
    clean_topic = topic.lower().strip()
    if clean_topic not in DOMAIN_ACTION_GUIDANCE:
        clean_topic = "career" if "job" in clean_topic or "work" in clean_topic else "wealth" if "money" in clean_topic else "career"

    domain_data = DOMAIN_ACTION_GUIDANCE.get(clean_topic, DOMAIN_ACTION_GUIDANCE["career"])

    # 1. Warm Opening
    opening = (
        f"Welcome, {clean_name}. In exploring your personal energy cycles for {domain_data['theme']}, "
        f"the insights below highlight where natural momentum is currently flowing and where mindful adjustments can bring optimal ease."
    )

    # 2. Current Time Period Context (Diplomatically phrased)
    period_context = (
        f"Your current cycle is a meaningful phase of refinement. {domain_data['blockage_framing']} "
        f"{time_period_summary or 'Current alignments encourage consolidating your strengths before stepping into the next major expansion.'}"
    )

    # 3. Actionable Solutions (Tailored positive strategies)
    solutions_intro = "To smoothly navigate this phase and achieve your highest potential, the following practical strategies are recommended:"
    action_items = domain_data["practical_solutions"]

    # 4. Supportive Remedies (Gentle, supportive, non-guaranteed framing)
    remedy_intro = (
        "In addition to real-world action, integrating supportive subtle practices helps clear energetic bottlenecks "
        "and harmonize your natural field. Consider these time-tested lifestyle adjustments:"
    )

    formatted_remedies = []
    if supportive_remedies:
        for r in supportive_remedies[:4]:
            r_name = r.get("primary_gemstone") or r.get("healing_crystal") or r.get("remedy") or r.get("benefit", "")
            r_type = r.get("type", "Supportive Alignment")
            r_purpose = r.get("benefit", "Harmonizes natural vitality and focus")
            clean_r_type = sanitize_text(r_type)
            clean_r_purpose = sanitize_text(r_purpose)
            formatted_remedies.append(f"• {clean_r_type}: Utilizing {r_name} — {clean_r_purpose}.")
    else:
        formatted_remedies = [
            "• Natural Light & Spatial Orientation: Position your primary workspace facing an auspicious direction to enhance focus.",
            "• Color Frequency Alignment: Incorporate supportive tones such as soft gold, emerald green, and cream in your daily attire.",
            "• Calm Mindfulness Routine: Dedicate a few moments each morning to center your intentions before beginning external tasks."
        ]

    # 5. Upcoming Favorable Window
    growth_window_text = (
        f"Upcoming Momentum: {favorable_window or 'As your current cycle matures over the coming months, natural ease returns and doors open with greater fluidity.'} "
        f"The disciplined groundwork you establish today directly prepares you to capitalize on this upcoming favorable cycle."
    )

    # 6. Inspiring Closing
    closing = (
        "Remember, planetary cycles provide navigational insight and awareness—your conscious dedication, "
        "diplomacy, and positive choices remain the ultimate architects of your destiny."
    )

    full_narrative = (
        f"{opening}\n\n"
        f"### 1. Understanding Your Current Energy Phase\n{period_context}\n\n"
        f"### 2. Actionable Pathways for Progress\n{solutions_intro}\n" +
        "\n".join([f"• **{item.split(':')[0]}:**{':'.join(item.split(':')[1:])}" if ':' in item else f"• {item}" for item in action_items]) + "\n\n"
        f"### 3. Harmonizing Remedies & Subtle Practices\n{remedy_intro}\n" +
        "\n".join(formatted_remedies) + "\n\n"
        f"### 4. The Path Forward\n{growth_window_text}\n\n"
        f"{closing}"
    )

    # Sanitize final output to guarantee zero technical leaks or fatalistic terms
    clean_narrative = sanitize_text(full_narrative)

    return {
        "status": "success",
        "domain": clean_topic,
        "theme": domain_data["theme"],
        "client_name": clean_name,
        "diplomatic_report": clean_narrative
    }
