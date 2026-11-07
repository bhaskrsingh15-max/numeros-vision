"""
ZERO-COST LOCAL NARRATIVE & TEMPLATE SYNTHESIZER
Guarantees $0 operational cost by producing human-sounding, positively-framed
narrative explanations directly from RAG citations and deterministic consensus results,
without requiring paid external LLM API calls.
"""

from typing import Dict, Any

from app.engine.diplomatic_narrative_engine import sanitize_text, DOMAIN_ACTION_GUIDANCE
from app.engine.cheiro_engine import verify_evidence_guardrails

def synthesize_zero_cost_narrative(consensus_result: Dict[str, Any], classified_topic: str) -> str:
    """
    Generates a warm, dignified, and diplomatically phrased narrative explanation
    at ZERO token/API cost. Strips out raw technical jargon and provides
    constructive, positive action pathways (networking, budgeting, empathetic communication, grounding).
    """
    user_name = consensus_result.get("user_name", "Friend")
    vedic = consensus_result.get("vedic_numerology", {})
    lo_shu = consensus_result.get("lo_shu_grid", {})
    
    driver = vedic.get("driver_number", 1)
    driver_planet = vedic.get("driver_planet", "Sun")
    conductor = vedic.get("conductor_number", 1)
    conductor_planet = vedic.get("conductor_planet", "Sun")
    
    completed_planes = lo_shu.get("completed_planes", [])
    cheiro_name = consensus_result.get("cheiro_name_analysis", {})
    
    topic_key = classified_topic.lower().strip()
    if topic_key not in DOMAIN_ACTION_GUIDANCE:
        topic_key = "career" if any(w in topic_key for w in ["job", "work", "business"]) else "wealth" if any(w in topic_key for w in ["money", "finance"]) else "career"
    domain_info = DOMAIN_ACTION_GUIDANCE.get(topic_key, DOMAIN_ACTION_GUIDANCE["career"])

    narrative_paragraphs = []
    
    # 1. Warm Personal Greeting & Core Energetic Alignment
    greeting = (
        f"Welcome, {user_name}! In exploring your personal energy cycles for {domain_info['theme']}, "
        f"your foundational frequency is guided by the steady clarity of {driver_planet} energy (Root {driver}), "
        f"moving towards a life path inspired by {conductor_planet} qualities (Path {conductor}). "
        f"This combination reflects strong leadership potential paired with disciplined perseverance."
    )
    narrative_paragraphs.append(greeting)
    
    # 2. Name Vibration Harmony (Diplomatic & Supportive)
    if cheiro_name:
        name_arch = cheiro_name.get("compound_archetype", "Supportive Harmony")
        name_root = cheiro_name.get("name_root")
        if name_root in [1, 3, 5, 6]:
            name_text = (
                f"Your name frequency aligns gracefully with your birth vibrations, carrying the supportive qualities of "
                f"'{name_arch}'. This resonance naturally enhances ease of communication and expands your social circle."
            )
        else:
            name_text = (
                f"Your name frequency resonates with '{name_arch}'. While this brings deep determination and high standards, "
                f"introducing a slight harmonic calibration can help smoothen interactions and accelerate positive recognition."
            )
        narrative_paragraphs.append(name_text)
    
    # 3. Energy Matrix Natural Strengths
    if completed_planes:
        plane_labels = [p.replace("Plane", "Natural Flow").strip() for p in completed_planes]
        planes_str = ", ".join(plane_labels)
        plane_text = (
            f"Your personal energy matrix shows strong natural balance across {planes_str}. "
            f"These areas serve as your reliable anchors, giving you resilience when navigating complex situations."
        )
    else:
        plane_text = (
            "Your personal energy matrix reflects dynamic versatility, allowing you to adapt gracefully "
            "across multiple environments and learn through direct experience."
        )
    narrative_paragraphs.append(plane_text)
    
    # 4. Domain-Specific Guidance & Diplomatic Actionable Pathways
    domain_verdict = consensus_result.get("domain_verdicts", {}).get(classified_topic.title(), {})
    verdict_str = domain_verdict.get("verdict", "Favourable Growth")
    
    topic_guidance = (
        f"### Navigating Your Current Cycle: {domain_info['theme']}\n"
        f"{domain_info['blockage_framing']}\n\n"
        f"**Recommended Strategic Actions to Maximize Ease:**\n"
    )
    action_bullets = "\n".join([f"• {action}" for action in domain_info["practical_solutions"][:3]])
    topic_guidance += action_bullets
    narrative_paragraphs.append(topic_guidance)
    
    # 5. Harmonizing Practices (Non-overpromising, supportive)
    remedy_text = (
        f"### Supportive Energetic Practices\n"
        f"{domain_info['energy_enhancement']}\n"
        f"Incorporating supportive subtle habits—such as aligning your daily schedule with early morning light, "
        f"keeping a clean and organized workspace, and wearing uplifting natural tones—helps maintain steady momentum."
    )
    narrative_paragraphs.append(remedy_text)
    
    # 6. Inspiring Closing
    closing = (
        "Planetary cycles offer valuable navigational clarity. Your conscious commitment, thoughtful diplomacy, "
        "and purposeful daily actions remain the true champions of your ongoing success."
    )
    narrative_paragraphs.append(closing)
    
    raw_narrative = "\n\n".join(narrative_paragraphs)
    sanitized = sanitize_text(raw_narrative)
    return verify_evidence_guardrails(sanitized)

