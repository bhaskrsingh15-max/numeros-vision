from app.engine.international_remedy_engine import get_international_planetary_remedies, analyze_english_name_acoustics
"""
QUESTION EXPLANATION & REMEDIES ENGINE
Numeros Vision — ANVEIL EVERY CHARM

Generates:
1. Direct, clear answers to user questions (Career, Marriage, Wealth, Health, Property, Life Path).
2. Simple, plain-English explanations of WHY this situation/friction/support is happening
   based on the user's Driver (Mulank) and Conductor (Bhagyank) numbers.
3. Practical, actionable remedies (Daily Habits, Colors, Charity, Gemstones/Sacred Geometry).
"""

from typing import Dict, Any, List, Optional
import re
from app.engine.source_privacy_shield import (
    mask_source_name,
    sanitize_location,
    sanitize_text,
    sanitize_citation,
)

# ── Planetary Rulers & Core Vibrations ─────────────────────────────────────────
PLANETARY_INFO = {
    1: {"planet": "Sun (Surya)", "nature": "Leadership, executive ambition, independent will, authority, self-respect"},
    2: {"planet": "Moon (Chandra)", "nature": "Emotions, intuition, mental peace, diplomacy, sensitivity, fluidity"},
    3: {"planet": "Jupiter (Guru)", "nature": "Wisdom, expansion, learning, counseling, respect, moral integrity"},
    4: {"planet": "Rahu (North Node)", "nature": "Sudden shifts, unconventional thinking, technical acumen, unexpected delays, restlessness"},
    5: {"planet": "Mercury (Budh)", "nature": "Communication, commerce, adaptability, quick wit, networking, analytical speed"},
    6: {"planet": "Venus (Shukra)", "nature": "Luxury, beauty, relationships, artistic harmony, material comfort, charisma"},
    7: {"planet": "Ketu (South Node)", "nature": "Research, spiritual depth, detachment, intuition, unconventional paths, introspection"},
    8: {"planet": "Saturn (Shani)", "nature": "Discipline, karmic testing, slow steady compounding, perseverance, justice, heavy labor"},
    9: {"planet": "Mars (Mangal)", "nature": "High energy, courage, physical stamina, humanitarian drive, quick temper, assertiveness"}
}

# ── Topic Friendly Numbers & Friction Taxonomy ────────────────────────────────
# ── Topic Friendly Numbers & Friction Taxonomy ────────────────────────────────
TOPIC_FRIENDLY_NUMBERS = {
    "education": {1, 3, 5, 6, 7},
    "career":   {1, 3, 5, 8, 9},
    "marriage": {2, 3, 5, 6},
    "wealth":   {1, 3, 5, 6},
    "health":   {1, 2, 3, 5},
    "property": {4, 6, 8, 9},
    "general":  {1, 3, 5, 6, 9}
}

ENEMY_PAIRS = {
    (1, 8), (8, 1),
    (2, 8), (8, 2),
    (2, 4), (4, 2),
    (2, 9), (9, 2),
    (3, 6), (6, 3),
    (4, 9), (9, 4),
    (7, 8), (8, 7)
}

# ── Lucky Attunements per Driver Number ───────────────────────────────────────
LUCKY_DATA = {
    1: {"colors": "Gold, Orange, Copper, Warm Yellow", "days": "Sunday", "avoid": "Black, Dark Blue", "metal_gem": "Ruby or Sunstone in Copper/Gold", "direction": "East"},
    2: {"colors": "White, Cream, Silver, Pearl", "days": "Monday", "avoid": "Dark Red, Black", "metal_gem": "Pearl or Moonstone in Silver", "direction": "North-West"},
    3: {"colors": "Bright Yellow, Golden, Amber", "days": "Thursday", "avoid": "Dark Blue, Harsh Pink", "metal_gem": "Yellow Sapphire or Citrine in Brass/Gold", "direction": "North-East"},
    4: {"colors": "Electric Blue, Grey, Khaki, Silver", "days": "Wednesday & Saturday", "avoid": "Black, Fiery Red", "metal_gem": "Solid Silver Square or Hessonite", "direction": "South-West"},
    5: {"colors": "Emerald Green, Light Blue, Turquoise", "days": "Wednesday", "avoid": "Harsh Red", "metal_gem": "Emerald or Green Aventurine in Silver/Gold", "direction": "North"},
    6: {"colors": "Soft Pink, Cream, Diamond White, Light Blue", "days": "Friday", "avoid": "Yellow, Muddy Brown", "metal_gem": "Diamond, Opal, or Clear Quartz in Silver", "direction": "South-East"},
    7: {"colors": "Pastel Green, Light Grey, Lavender, White", "days": "Thursday & Monday", "avoid": "Jet Black, Dark Brown", "metal_gem": "Cat's Eye or Tiger's Eye in Silver", "direction": "North-West"},
    8: {"colors": "Dark Blue, Navy, Charcoal, Grey", "days": "Saturday", "avoid": "Bright Red, Pure Yellow", "metal_gem": "Blue Sapphire, Amethyst, or Iron Ring", "direction": "West"},
    9: {"colors": "Red, Crimson, Rose, Coral", "days": "Tuesday", "avoid": "Black, Dark Navy", "metal_gem": "Red Coral or Carnelian in Copper/Silver", "direction": "South"}
}

def _classify_topic(question: str) -> str:
    ql = question.lower()
    ql = re.sub(r'\b(carrier|carrer)\b', 'career', ql)

    # 1. Universal Obstacles Everywhere
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

def generate_simple_explanation_and_remedies(
    question: str,
    driver: int,
    conductor: int,
    name: str = "",
    current_age: Optional[int] = None,
    day: Optional[int] = None,
    month: Optional[int] = None,
    year: Optional[int] = None,
    topic: Optional[str] = None,
    country: Optional[str] = "IN",
    is_international: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Produces:
    1. Direct prediction answer to what was asked.
    2. Simple, plain-English 'Why This Is Happening' explanation based on Core Matrix Numerology.
    3. Actionable step-by-step remedies across Core Matrix, Dasha, Elements Balancing, and Missing Numbers.
    """
    from app.engine.diplomatic_narrative_engine import sanitize_text

    if not topic:
        topic = _classify_topic(question)
    first_name = (name.split()[0] if name else "You").capitalize()
    if is_international is None:
        is_international = bool(country and country.strip().upper() not in ["IN", "INDIA"])
    
    d_info = PLANETARY_INFO.get(driver, {"planet": "Universal", "nature": "Balanced energy"})
    c_info = PLANETARY_INFO.get(conductor, {"planet": "Destiny", "nature": "Life direction"})
    lucky = LUCKY_DATA.get(driver, LUCKY_DATA[1])

    is_enemy = (driver, conductor) in ENEMY_PAIRS
    friendly_set = TOPIC_FRIENDLY_NUMBERS.get(topic, {1, 3, 5, 6, 9})
    has_affinity = (driver in friendly_set) or (conductor in friendly_set)
    is_aligned = has_affinity and not is_enemy

    # ── Multi-Engine Occult Astrological Consensus Initialization ──────────
    from app.engine.core_matrix_engine import generate_core_matrix_profile
    from app.engine.bnn_numerology_engine import evaluate_bnn_numerology_profile, BNN_PAIR_DATABASE
    from app.engine.unified_planetary_numerology_engine import evaluate_unified_planetary_numerology
    from app.engine.lo_shu import analyze_lo_shu_grid

    core_matrix = None
    bnn_profile = None
    unified_multi_system = None
    lo_shu_analysis = None

    eff_day = day or driver
    eff_month = month or (((conductor - driver) % 12) or 1)
    eff_year = year or 1990

    try:
        core_matrix = generate_core_matrix_profile(name, eff_day, eff_month, eff_year, current_age=current_age)
        bnn_profile = evaluate_bnn_numerology_profile(eff_day, eff_month, eff_year, name)
        unified_multi_system = evaluate_unified_planetary_numerology(eff_day, eff_month, eff_year, name)
        lo_shu_analysis = analyze_lo_shu_grid(eff_day, eff_month, eff_year)
    except Exception:
        pass

    # Extract BNN Conjunction Pair & Predictions
    bnn_pair_data = BNN_PAIR_DATABASE.get((driver, conductor)) or BNN_PAIR_DATABASE.get((conductor, driver)) or {}
    bnn_title = bnn_pair_data.get("title", f"{d_info['planet']} - {c_info['planet']}")
    bnn_archetype = bnn_pair_data.get("archetype", "Planetary Alignment")
    bnn_preds = bnn_pair_data.get("bnn_predictions", "")

    # Extract Lo Shu Numbers, Missing Elements & Repetitions
    raw_missing = lo_shu_analysis.get("missing_numbers", []) if lo_shu_analysis else []
    # Core fix: Driver and Conductor numbers can NEVER be considered missing in a person's matrix!
    missing_numbers = [n for n in raw_missing if n != driver and n != conductor]
    counts_map = lo_shu_analysis.get("counts", {}) if lo_shu_analysis else {}
    repetitive_numbers = [n for n, c in counts_map.items() if c > 1]

    # Calculate Personal Year for 2026
    if day and month:
        raw_py = day + month + 2 + 0 + 2 + 6
        while raw_py > 9:
            raw_py = sum(int(d) for d in str(raw_py))
        personal_year = raw_py
    else:
        personal_year = ((driver + conductor) % 9) or 9

    # ── Grounded Multi-Hop Agentic RAG Knowledge Base Retrieval (10,826 Passages) ──
    from app.engine.rag_retriever import rag_engine

    rag_context = rag_engine.query_multihop(
        user_question=question,
        driver=driver,
        conductor=conductor,
        topic=topic,
        current_age=current_age
    )
    rag_predictions = rag_context.get("fused_passages", [])[:3]
    rag_remedies = rag_context.get("hops", {}).get("hop4_remedies", [])[:2]
    rag_samples = rag_context.get("hops", {}).get("hop2_domain_intent", [])[:1]

    # ── Multi-Engine Consensus Synthesis: Root Cause, Validation & Bridge ──
    why_happening = ""
    direct_answer = ""
    validation_question = ""
    permission_prompt = ""
    remedies = []

    lo_shu_note = ""
    if 5 in missing_numbers:
        lo_shu_note += " Your matrix shows an absence of central Number 5 (Mercury Earth balance), creating sudden pacing shifts where projects stall just before locking in."
    if 6 in missing_numbers:
        lo_shu_note += " Missing Number 6 (Venus harmony) indicates you often carry high responsibilities without receiving effortless material or relationship ease in return."
    if repetitive_numbers:
        rep_str = ", ".join(f"Number {n} (×{counts_map[n]})" for n in repetitive_numbers)
        lo_shu_note += f" Furthermore, repetitive activations of {rep_str} heighten energetic intensity and demand disciplined patience."

    bnn_note = f" In Planetary Vibrational Science, your Driver-Conductor conjunction operates as '{bnn_title}' ({bnn_archetype}). {bnn_preds}" if bnn_preds else ""

    if topic == "education":
        is_child = (current_age is not None and current_age < 18) or any(w in question.lower() for w in ["child", "daughter", "son", "kid", "teen", "teenager", "teenage", "girl", "boy"])
        pronoun_subj = "she" if any(w in question.lower() for w in ["her", "she", "daughter", "girl"]) else ("he" if any(w in question.lower() for w in ["his", "he", "son", "boy"]) else "you")
        pronoun_poss = "her" if pronoun_subj == "she" else ("his" if pronoun_subj == "he" else "your")
        pronoun_obj = "her" if pronoun_subj == "she" else ("him" if pronoun_subj == "he" else "you")
        name_ref = first_name if first_name not in ["Seeker", "You", "Friend"] else (pronoun_subj.capitalize() if pronoun_subj != "you" else "Seeker")

        why_happening = (
            f"Her foundational energetic matrix combines Birth Number / Driver {driver} ({d_info['planet']}) "
            f"with Life Path / Conductor {conductor} ({c_info['planet']}). In classical Sankhya Shastra and Planetary Numerology, this forms the auspicious "
            f"Budh-Shukra 'Lakshmi-Narayan Yoga' (Creative Grace paired with Sharp Intellectual Agility). "
            f"{bnn_note}{lo_shu_note} In 2026, {pronoun_subj} is moving through Personal Year {personal_year} (Mercury vibration), "
            f"an active cognitive expansion cycle that heightens curiosity, rapid learning absorption, and verbal expression. "
            f"However, missing numbers in the Lo Shu grid (specifically Numbers 3 and 4) indicate that while mental grasping speed is high, "
            f"monotonous repetitive drills and rigid rote memorization quickly trigger restlessness."
        )

        direct_answer = (
            f"**1. Luminous Natural Strengths & Academic Flow:**\n"
            f"• **Learning Modality:** {name_ref} is an **intuitive, visual, and experiential learner**. Rather than dry textbook recitation, {pronoun_subj} excels when concepts are presented visually, creatively, or through interactive projects and storytelling.\n"
            f"• **Cognitive Agility & Grasping Speed:** Mental processing speed is remarkably quick when {pronoun_subj} feels curious and respected. Complex ideas are absorbed rapidly through conceptual immersion.\n"
            f"• **Creative Aesthetics:** Possesses a natural instinct for order, harmony, and creative presentation, often making class projects, writing, or designs stand out effortlessly.\n\n"
            f"**2. Gentle Shadow Traits & Learning Vulnerabilities (Empathetic Growth Pointers):**\n"
            f"• **Monotony Fatigue (Pacing RESTLESSNESS):** When forced into dry, repetitive memorization or rigid drills, mental stamina dips quickly. This is not a lack of talent or intelligence — it is simply an active, multi-dimensional intellect asking for meaningful engagement.\n"
            f"• **Heightened Sensitivity to Emotional Tone:** Under harsh criticism or high-pressure environments, {pronoun_subj} may quietly withdraw or lose enthusiasm. Emotional security directly governs academic confidence.\n\n"
            f"**3. Mindful Precautions & Practical Study Guardrails:**\n"
            f"• **Structured Pomodoro Rhythm:** Adopt 25-minute concentrated study blocks followed by a 5-minute creative breather (doodling, movement, or water). Never force prolonged 3-hour unbroken desk marathons.\n"
            f"• **Milestone-Based Encouragement:** Celebrate steady consistency rather than perfection. Visual progress trackers (colored sticky notes, milestone charts) dramatically boost retention.\n\n"
            f"**4. Teenage Prospects & Vocational Streams (Classes 10–12 & Higher Education):**\n"
            f"• **Upper School Streams:** The 6-5 synergy unites Commercial acumen, Analytical reasoning, and Aesthetic flair. Ideal academic streams include **Commerce with Applied Mathematics or Economics**, **Humanities with Media/Psychology/Design**, or **Creative Technology / Digital Architecture**.\n"
            f"• **Long-term Career Horizons:** Well-suited for high-value modern vocations: Luxury Brand Strategy, Creative Direction & Digital Media, Commercial Law / Corporate Communications, Spatial & Environmental Design, or Fintech Strategy."
        )

        validation_question = (
            f"Does this resonance match what you have observed in {pronoun_poss} learning style? Specifically, have you noticed that {pronoun_subj} grasps complex concepts almost instantly when visually or creatively engaged, but shows restlessness or loss of interest when subjected to monotonous, rigid drills?"
        )

        permission_prompt = (
            f"If this aligns with {pronoun_poss} nature, would you like me to Explore the consecrated student remedies, study desk Vastu orientation, and parental guidance alignment protocols?"
        )

        remedies = [
            {
                "category": "Study Zone Vastu Alignment",
                "title": "North / East Study Vector",
                "instruction": f"Orient {pronoun_poss} study desk facing North (Mercury vector for intellect and analytical speed) or East (Sun vector for mental clarity). Keep the desk organized, clutter-free, and well-lit with natural warm light.",
                "purpose": "Grounds scattered mental vibrations and activates high cognitive retention."
            },
            {
                "category": "Vibrational Color Therapy",
                "title": "Mercury & Venus Study Accents",
                "instruction": f"Incorporate pastel green, soft emerald, cream, or light turquoise into {pronoun_poss} study stationery, desk mat, or notebook covers. Avoid jet black or dark navy in the primary study space.",
                "purpose": "Harmonizes the intellect with Mercury 5 and soothes exam anxiety."
            },
            {
                "category": "Elemental Wood Balancing",
                "title": "Living Plant / Wooden Desk Accessory",
                "instruction": f"Place a small, healthy green plant (like money plant or jade) or a natural wooden pen-stand in the North-East corner of {pronoun_poss} study room.",
                "purpose": "Balances the missing Number 3 (Wood element) to reinforce academic discipline and memory stamina."
            },
            {
                "category": "Pre-Study Centering Ritual",
                "title": "2-Minute Breath Centering",
                "instruction": "Before opening study materials, spend 2 minutes sitting upright, taking 5 slow deep breaths while softly visualizing an emerald green or golden light.",
                "purpose": "Clears mental noise and aligns the left and right hemispheres of the brain for rapid learning."
            },
            {
                "category": "Parental Guidance Protocol",
                "title": "Visual Encouragement Strategy",
                "instruction": f"Acknowledge creative effort and problem-solving milestones visually. Avoid comparative criticism with peers, as Driver 6 carries heightened sensitivity to aesthetic and emotional tone.",
                "purpose": "Builds self-efficacy and prevents psychological friction during adolescent transitions."
            }
        ]

    elif topic == "career":
        if is_enemy or (driver in [1, 8] and conductor in [1, 8]):
            why_happening = (
                f"Your core natural energy combines Driver {driver} ({d_info['planet']}) with Conductor {conductor} ({c_info['planet']}). "
                f"During this calibration phase, progress requires extra strategic networking, documented agreements, and disciplined compounding. "
                f"{bnn_note}{lo_shu_note} You are currently in Personal Year {personal_year}, an active foundation-building phase designed to build unshakeable authority rather than taking rushed shortcuts."
            )
            direct_answer = (
                f"**1. Luminous Natural Strengths & Professional Authority:**\n"
                f"• **Executive Tenacity & Depth:** {first_name}, your matrix carries profound discipline, meticulous execution, and deep endurance. You excel at taking complex, demanding initiatives and steering them to completion where others lose patience.\n"
                f"• **Strategic Vision:** You possess the rare ability to build for the long horizon, foreseeing organizational and structural needs well before they become evident.\n\n"
                f"**2. Gentle Shadow Traits & Career Vulnerabilities (Empathetic Counseling Guidance):**\n"
                f"• **Subtle Resistance to Rushed Timelines:** Because your standards are exceptionally high, you may experience silent frustration when peers or management move abruptly without adequate planning. This can sometimes be perceived as reserve or hesitancy.\n"
                f"• **Carrying Solitary Burdens:** A natural inclination to take full ownership may tempt you to handle high workloads alone rather than delegating smoothly, risking periodic mental fatigue.\n\n"
                f"**3. Mindful Precautions & Strategic Career Guardrails:**\n"
                f"• **Documented Clarity:** Anchor all critical project deliverables, KPIs, and agreements in written form to ensure your leadership contributions are unambiguously visible.\n"
                f"• **Diplomatic Patience:** Treat unexpected timeline pauses as tactical pauses for refinement rather than setbacks; favorable recognition solidifies as you maintain consistent quality."
            )
            validation_question = (
                "Does this resonance match what you have been experiencing over recent months? Specifically, have you observed that despite your strong dedication and executive competence, official recognitions, title promotions, or management decisions have faced unexpected delays or sudden structural pivots?"
            )
        elif driver == 4 or conductor == 4:
            why_happening = (
                f"Your personal matrix carries Driver {driver} ({d_info['planet']}) and Conductor {conductor} ({c_info['planet']}), generating unconventional, high-velocity vision. "
                f"{bnn_note}{lo_shu_note} By centering your focus on one structured initiative at a time and anchoring into Personal Year {personal_year}, you transform restless momentum into tangible authority."
            )
            direct_answer = (
                f"**1. Luminous Natural Strengths & Innovation Flow:**\n"
                f"• **Unconventional Problem-Solving:** {first_name}, you have a sharp, non-linear intellect capable of spotting opportunities, architectural flaws, and market shifts that traditional frameworks miss entirely.\n"
                f"• **High-Velocity Adaptability:** Thrives in dynamic, modern, and transformative sectors (technology, strategic advisory, research, media).\n\n"
                f"**2. Gentle Shadow Traits & Career Vulnerabilities (Empathetic Counseling Guidance):**\n"
                f"• **Vision Ahead of Institutional Timelines:** Because your concepts often live 6 to 12 months ahead of conventional environments, you may experience impatience or friction with bureaucratic hierarchies that move too slowly.\n"
                f"• **Multi-Directional Energy Scatter:** An abundance of ideas can sometimes dilute day-to-day completion if too many initiatives are started simultaneously.\n\n"
                f"**3. Mindful Precautions & Strategic Career Guardrails:**\n"
                f"• **The Single-Flagship Discipline:** Channel your inventive power into one primary high-impact project at a time before branching out into adjacent ventures.\n"
                f"• **Translational Diplomacy:** Frame innovative proposals in simple, metrics-driven terms that traditional decision-makers can easily digest and approve."
            )
            validation_question = (
                "Does this resonance align with your experience? Have you observed that your ideas are often ahead of current institutional timelines, leading to friction with conventional management methods?"
            )
        else:
            why_happening = (
                f"Your natural energetic frequency carries Driver {driver} ({d_info['planet']}) and Conductor {conductor} ({c_info['planet']}), establishing favorable career momentum. "
                f"{bnn_note}{lo_shu_note} Aligning your daily routine with Personal Year {personal_year} priorities allows your natural leadership qualities to be recognized and rewarded."
            )
            direct_answer = (
                f"**1. Luminous Natural Strengths & Professional Momentum:**\n"
                f"• **Natural Charisma & Persuasive Alignment:** {first_name}, your matrix carries effortless relational warmth and professional magnetism. People naturally gravitate toward your counsel, leadership, and aesthetic or strategic judgement.\n"
                f"• **Balanced Execution:** You possess a harmonious blend of creative imagination and practical follow-through, making you an invaluable asset in cross-functional or leadership roles.\n\n"
                f"**2. Gentle Shadow Traits & Career Vulnerabilities (Empathetic Counseling Guidance):**\n"
                f"• **Over-Accommodating Demands:** Because you naturally value harmony and goodwill, you may occasionally hesitate to set firm boundaries, absorbing extra team responsibilities that do not directly advance your personal goals.\n"
                f"• **Sensory & Mental Saturation:** High social and professional interactions can leave your battery drained if you skip dedicated quiet time.\n\n"
                f"**3. Mindful Precautions & Strategic Career Guardrails:**\n"
                f"• **Boundary Architecture:** Clarify your core deliverables early and protect your prime creative hours from non-essential meetings.\n"
                f"• **Proactive Self-Advocacy:** Present your measurable achievements regularly to senior stakeholders rather than waiting for quiet recognition."
            )
            validation_question = (
                "Does this resonance match what you have been feeling? Have you felt an increasing momentum pushing you toward greater independence, new responsibilities, and strategic clarity?"
            )

        permission_prompt = (
            "Do you want to overcome this friction and harmonize your planetary career timeline? Can I suggest consecrated remedies and timeline windows for you?"
        )

        # Career Remedies
        remedies = [
            {
                "category": "Daily Professional Ritual",
                "title": "Morning Clarity Attunement",
                "instruction": f"Spend 10 minutes facing {lucky['direction']} every morning before looking at digital screens. Write your top 3 daily priorities in a dedicated notebook using blue or green ink.",
                "purpose": "Grounds scattered mental vibrations and activates focused execution energy."
            },
            {
                "category": "Color Vibration",
                "title": f"Auspicious Attire on {lucky['days']}",
                "instruction": f"Wear {lucky['colors']} during critical interviews, negotiations, or client pitches. Strictly avoid {lucky['avoid']} on important career days.",
                "purpose": f"Harmonizes your aura with {d_info['planet']} to command natural authority."
            },
            {
                "category": "Sacred Balancing Remedy",
                "title": "Copper / Silver Energy Harmonizer",
                "instruction": (
                    "Drink your morning water from a pure copper vessel (if Driver 1, 3, 9) or a pure silver vessel/glass (if Driver 2, 4, 7). Keep a clean, clutter-free desk facing East or North."
                ),
                "purpose": "Clears energetic blockage in the workspace and dissolves bureaucratic friction."
            },
            {
                "category": "Pacification Charity",
                "title": "Weekly Energy Balance Charity",
                "instruction": f"On {lucky['days']}, feed birds with mixed grains or offer food to those in need without boasting.",
                "purpose": "Neutralizes planetary friction and invites auspicious karma into your career path."
            }
        ]

    elif topic == "marriage":
        if is_enemy:
            why_happening = (
                f"Your Driver {driver} ({d_info['planet']}) and Conductor {conductor} ({c_info['planet']}) carry contrasting emotional rhythms. "
                f"{bnn_note}{lo_shu_note} One part of your nature seeks emotional softness and reassurance, while another demands stubborn control or independence. "
                f"In relationships, this creates communication misalignments where loving intentions are expressed harshly, "
                f"or small misunderstandings turn into prolonged emotional distance."
            )
            direct_answer = (
                f"**1. Luminous Natural Strengths & Emotional Devotion:**\n"
                f"• **Deep Loyalty & Genuine Care:** {first_name}, beneath the surface, your capacity for steadfast loyalty and authentic protection in a relationship is profound. When committed, you stand firmly by your partner through thick and thin.\n"
                f"• **High Standards of Integrity:** You hold sacred values around truthfulness, mutual respect, and family dignity.\n\n"
                f"**2. Gentle Shadow Traits & Relationship Vulnerabilities (Empathetic Compassion):**\n"
                f"• **Contrasting Emotional Rhythms:** One facet of your nature craves warmth and reassurance, while another retreats into self-protective independence when stressed. Loving intentions can occasionally be spoken with unintentional sharpness.\n"
                f"• **Unspoken Expectations:** Bottling up subtle grievances until they spill over under fatigue can create unnecessary emotional distance.\n\n"
                f"**3. Mindful Precautions & Communication Guardrails:**\n"
                f"• **The 'Pause Before Reacting' Rule:** When emotional tension rises, step away for 15 minutes before replying. Softening your vocal tone transforms difficult discussions into moments of deeper bonding.\n"
                f"• **Sanctuary Spaces:** Keep the bedroom strictly free of work conversations, financial audits, or unresolved debates."
            )
            validation_question = (
                "Does this resonance match what you have observed in your relationship? Specifically, have small misunderstandings, unspoken expectations, or words exchanged under fatigue led to temporary emotional distance or hesitation to communicate openly?"
            )
        else:
            why_happening = (
                f"Your relationship vibrations are fundamentally warm between Driver {driver} and Conductor {conductor}. "
                f"{bnn_note}{lo_shu_note} External fatigue and timing pressures have created temporary emotional distance, but harmonizing your living space will quickly restore warmth."
            )
            direct_answer = (
                f"**1. Luminous Natural Strengths & Relationship Affinity:**\n"
                f"• **Natural Empathy & Affection:** {first_name}, your relationship energy is warm, considerate, and receptive. You possess a natural gift for nurturing comfort, mutual trust, and joyful shared experiences.\n"
                f"• **Aesthetic & Domestic Harmony:** You instinctively know how to make a living space feel like a welcoming sanctuary.\n\n"
                f"**2. Gentle Shadow Traits & Relationship Vulnerabilities (Empathetic Compassion):**\n"
                f"• **Absorbing Partner Stress:** Because your emotional antenna is sensitive, you easily absorb your partner's external worries (work stress, family duties), confusing their temporary distraction with emotional cooling.\n"
                f"• **Routine Fatigue:** A lack of novel, lighthearted shared dates can let daily domestic routines feel heavier than they truly are.\n\n"
                f"**3. Mindful Precautions & Communication Guardrails:**\n"
                f"• **Dedicated Couple Micro-Rituals:** Schedule a weekly walk or shared tea without smartphones to reconnect intimately.\n"
                f"• **Separation of Burdens:** Remember that your partner's workplace stress is external to the sacred space of your relationship."
            )
            validation_question = (
                "Does this resonance align with what you've observed? Have external timing pressures, career schedules, and family obligations been the primary friction rather than a lack of affection?"
            )

        permission_prompt = (
            "Do you want to overcome this relationship friction and restore deep harmony? Can I suggest consecrated Venusian remedies, space neutralization, and auspicious timing for you?"
        )

        # Marriage Remedies
        remedies = [
            {
                "category": "Relationship Harmony Ritual",
                "title": "Friday Venus Attunement",
                "instruction": "Wear soft white, cream, or pastel pink on Fridays. Use natural floral fragrance or sandalwood attar on your pulse points.",
                "purpose": "Activates gentle Venusian charm and dissolves conversational sharpness."
            },
            {
                "category": "Living Space Remedy",
                "title": "South-West Earth Element Harmonization",
                "instruction": "Place a framed happy photograph of you and your partner in the South-West corner of your bedroom. Remove sharp metal objects, mirrors facing the bed, and clutter from this corner.",
                "purpose": "Stabilizes relationship foundations and promotes deep marital bonding."
            },
            {
                "category": "Elemental Harmonic Remedy",
                "title": "Sweet Donation / Sugar Offering",
                "instruction": "Offer white sweets or kheer to young girls or cows on Friday mornings with a sincere prayer for peace.",
                "purpose": "Soothes relationship friction and invites harmonious, loving vibrations."
            }
        ]

    elif topic == "health":
        why_happening = (
            f"Your Driver {driver} ({d_info['planet']}) governs your active vitality, while Conductor {conductor} ({c_info['planet']}) governs your deep nervous recovery. "
            f"{bnn_note}{lo_shu_note} Why you experience fatigue or restless sleep: your mind operates at a higher speed than your physical body can regenerate. "
            f"You carry unresolved mental to-do lists into your rest periods, which depletes your nervous system and causes energetic burnout."
        )
        direct_answer = (
            f"**1. Luminous Natural Vitality & Energy Dynamics:**\n"
            f"• **High Mental Drive & Resilient Core:** {first_name}, your baseline constitutional vitality has strong self-healing capabilities when supported with regular, rhythmic habits.\n"
            f"• **Quick Recuperation:** When you give yourself proper restorative downtime, your vitality rebounds much faster than average.\n\n"
            f"**2. Gentle Shadow Traits & Recovery Vulnerabilities (Gentle Wellness Pointers):**\n"
            f"• **High-RPM Mental Overdrive:** Your mind operates at a faster speed than your physical nervous system can digest. Carrying unfinished tasks or subconscious mental lists into the evening directly disrupts REM sleep quality.\n"
            f"• **Irregular Hydration & Meal Pacing:** When deeply engaged in creative or intellectual focus, you may delay water intake or skip meals, leading to sudden afternoon energy crashes or mild digestive acidity.\n\n"
            f"**3. Mindful Precautions & Daily Rest Guardrails:**\n"
            f"• **Digital Sun-Downing:** Disconnect from bright digital screens at least 45 minutes before sleep to allow melatonin release.\n"
            f"• **Rhythmic Hydration:** Start your morning with warm water from a silver or copper vessel, and avoid heavy caffeinated stimulants after 4 PM."
        )
        validation_question = (
            "Does this align with your daily rhythm? Specifically, have you noticed a pattern of mental over-activity at night or waking fatigue, where your mental stamina wants to sprint but your physical body asks for deep rest?"
        )
        permission_prompt = (
            "Do you want to overcome this fatigue and revitalize your physical core? Can I suggest consecrated vitality recovery rituals and elemental grounding for you?"
        )

        # Health Remedies
        remedies = [
            {
                "category": "Nervous System Recovery",
                "title": "Evening Screen Detox & Grounding",
                "instruction": "Turn off screens at least 45 minutes before sleep. Wash your feet with lukewarm water and a pinch of rock salt before getting into bed.",
                "purpose": "Discharges static electromagnetic stress and induces deep restorative REM sleep."
            },
            {
                "category": "Vedic Hydration Remedy",
                "title": "Silver / Copper Vessel Water",
                "instruction": "Keep drinking water overnight in a pure silver tumbler (calms anxiety and body heat) or copper jug (builds cellular immunity) and drink the first glass upon waking.",
                "purpose": "Balances bodily humors (Vata/Pitta/Kapha) and supports physical rejuvenation."
            },
            {
                "category": "Daily Vitality Ritual",
                "title": "Morning Sunlight Surya Arghya",
                "instruction": "Spend 10 to 15 minutes in early morning sunrise light. Take slow, deep breaths, visualizing clean golden vitality revitalizing every organ.",
                "purpose": "Charges your solar vitality and banishes chronic sluggishness."
            }
        ]

    elif topic == "wealth":
        why_happening = (
            f"Your Driver {driver} ({d_info['planet']}) gives you strong earning capability, but your Conductor {conductor} ({c_info['planet']}) "
            f"influences how capital is retained and multiplied. "
            f"{bnn_note}{lo_shu_note} Energetic friction in North (Mercury/Opportunity) or South-East (Venus/Cash Flow) sectors causes money to enter, "
            f"while unexpected obligations or delayed receivables rapidly siphon it away."
        )
        direct_answer = (
            f"**1. Luminous Natural Strengths & Wealth Generation:**\n"
            f"• **Strong Earning Magnetism:** {first_name}, you possess strong instincts for identifying lucrative opportunities, negotiating value, and generating capital through your skills or enterprise.\n"
            f"• **Generous Karmic Flow:** You have an open, magnanimous heart with wealth, which naturally keeps universal circulation active.\n\n"
            f"**2. Gentle Shadow Traits & Capital Outflow Vulnerabilities (Constructive Guidance):**\n"
            f"• **Subtle Outflow Leaks:** While income flows consistently, unexpected domestic obligations, impulse purchases during emotional fatigue, or delayed receivables can make it feel like capital evaporates before it accumulates.\n"
            f"• **Hesitation in Follow-ups:** You may sometimes feel awkward about following up assertively on money owed to you by friends, clients, or relatives.\n\n"
            f"**3. Mindful Precautions & Wealth Guardrails:**\n"
            f"• **The Automated Retention Firewall:** Divert a fixed percentage (15–20%) of incoming income immediately into automated, locked savings or asset instruments before touching discretionary funds.\n"
            f"• **Clean Space Attunement:** Remove all clutter, non-functional electronics, and unpaid bills from the North and South-East sectors of your home or workspace."
        )
        validation_question = (
            "Does this reflect your financial reality over recent months? Specifically, have you observed that while income opportunities arise, unexpected outflows, delayed payments, or timing friction have made it difficult to retain capital comfortably?"
        )
        permission_prompt = (
            "Do you want to overcome this financial leakage and activate steady abundance? Can I suggest consecrated wealth-attunement remedies and timing windows for you?"
        )

        # Wealth Remedies
        remedies = [
            {
                "category": "Wealth Magnetism Ritual",
                "title": "Orderly Cash & Wallet Attunement",
                "instruction": "Keep your wallet neat, organized, and free of old receipts or unpaid bills. Keep a crisp green currency note or a small silver coin inside that you never spend.",
                "purpose": "Aligns the law of attraction: money flows where order and respect exist."
            },
            {
                "category": "Directional Energy Remedy",
                "title": "North & North-East Water Element Clearing",
                "instruction": "Ensure the North and North-East corners of your home or office are bright, clean, and uncluttered. You may place a small healthy green money plant in a blue or green pot in the North.",
                "purpose": "Activates continuous opportunity flow (Kuber direction) and removes financial stagnation."
            },
            {
                "category": "Vedic Abundance Charity",
                "title": "Weekly Giving Channel",
                "instruction": f"On {lucky['days']}, donate a small fixed sum (e.g. ₹21, ₹51, or ₹101) to a trusted cause or feed street animals.",
                "purpose": "Maintains the continuous inflow-outflow karmic current of abundance."
            }
        ]

    elif topic == "career_stuck":
        why_happening = (
            f"You are navigating a temporary structural pause between your Driver {driver} ({d_info['planet']}) "
            f"and Conductor {conductor} ({c_info['planet']}). In classical planetary numerology cycles, career stagnation or unexpected career pauses are "
            f"governed by Saturn (Karma Karaka) testing your foundational resilience and Mercury (Opportunity alignment). {bnn_note}{lo_shu_note} "
            f"In 2026, you are moving through Personal Year {personal_year}. This pause is not a dead end — it is a vital celestial filter "
            f"dissolving an unsustainable role to reposition you for long-term authority and higher compensation."
        )
        direct_answer = (
            f"**1. Luminous Natural Strengths & Latent Resilience:**\n"
            f"• **Executive Endurance:** {first_name}, you possess an undeniable capacity to handle complex responsibilities. The skills, domain knowledge, and dedication you accumulated have not disappeared; they are being preserved for a higher-leverage role.\n"
            f"• **Strategic Adaptability:** You have the intellectual clarity to reinvent your value proposition when given focused, disciplined direction.\n\n"
            f"**2. Gentle Shadow Traits & Stagnation Vulnerabilities (Empathetic Counseling Guidance):**\n"
            f"• **The Panic Compromise Trap:** Under the emotional pressure of career delays or job loss, you may feel tempted to accept low-ball offers or toxic work environments. Rushing into misaligned roles only restarts the friction cycle.\n"
            f"• **Subconscious Self-Doubt:** Rejection loops can cause you to question your worth rather than recognizing that organizational restructurings are impersonal macroeconomic cycles.\n\n"
            f"**3. Mindful Precautions & Professional Healing Guardrails:**\n"
            f"• **Targeted High-Leverage Outreaches:** Limit job applications to 3 deeply customized, relationship-driven introductions per week rather than blindly submitting hundreds of generic portal applications.\n"
            f"• **Daily Momentum Anchor:** Maintain a strict 9:00 AM professional start time every weekday (exercise, skill sharpening, outreach) to protect your aura from lethargy and despair."
        )
        validation_question = (
            "Does this resonance match what you have observed in your job search? Have you noticed that despite your strong credentials and honest efforts, interviews or decision-makers have gone unexpectedly silent or stalled at the final round?"
        )
        permission_prompt = (
            "Do you want to break this career block and activate an auspicious job transition? Can I suggest consecrated Saturn-Mercury remedies and timing windows for you?"
        )
        remedies = [
            {
                "category": "Career Opportunity Activation",
                "title": "North Vector Desk & Workspace Alignment",
                "instruction": "Place your study or work laptop facing North (Mercury/Kubera opportunity channel). Keep a small bowl of clean water with green leaves or a money plant in the North corner.",
                "purpose": "Clears energetic blockage in professional pipelines and attracts active recruiter calls."
            },
            {
                "category": "Karmic Obstacle Pacification",
                "title": "Saturday Shani Karma Offering",
                "instruction": "On Saturday evenings before sunset, feed street dogs with bread dipped in a few drops of mustard oil, or offer food to laborers without seeking praise.",
                "purpose": "Neutralizes career delays governed by Saturn and accelerates professional breakthrough."
            },
            {
                "category": "Solar Authority Ritual",
                "title": "Morning Surya Arghya Attunement",
                "instruction": "Offer fresh water from a pure copper vessel toward the morning sunrise while standing upright. Take 3 deep breaths, visualizing yourself seated in your ideal leadership role.",
                "purpose": "Ignites royal solar charisma (Surya) to command respect and stand out in executive interviews."
            }
        ]

    elif topic == "child_conception":
        why_happening = (
            f"In classical Sankhya Shastra and Planetary Numerology, child conception and family harmony blessings are primarily governed "
            f"by Jupiter (Guru — Jeeva Karaka) and Venus/Moon (Creative vital essence and domestic nurturing). "
            f"Your Driver {driver} ({d_info['planet']}) and Conductor {conductor} ({c_info['planet']}) reveal strong underlying vitality, "
            f"but {bnn_note}{lo_shu_note} subtle elemental imbalances (such as missing Number 3 Wood element or Number 2 Water element) "
            f"create pacing friction where physical over-exertion and mental anticipation generate internal heat, delaying natural biological receptivity."
        )
        direct_answer = (
            f"**1. Luminous Natural Vitality & Parental Affinity:**\n"
            f"• **Generous Nurturing Heart:** {first_name}, you and your partner possess a rich, expansive capacity for parental love, protection, and moral guidance. The soul seeking descent into your home is drawn by your integrity.\n"
            f"• **Constitutional Self-Healing:** The underlying physical core is resilient when freed from excessive psychological tension.\n\n"
            f"**2. Gentle Shadow Traits & Conception Vulnerabilities (Gentle Wellness Pointers):**\n"
            f"• **The Calendar Anxiety Cycle:** Converting intimate bonding into a scheduled, high-pressure medical calendar elevates cortisol, which energetically constricts the subtle energy channels (Nadis) responsible for conception.\n"
            f"• **Absorbing Family Pressure:** Well-meaning questions from elders or relatives create subconscious guilt, which depletes the feminine water and masculine solar vitality.\n\n"
            f"**3. Mindful Precautions & Progeny Guardrails:**\n"
            f"• **Sanctuary Bedroom Rule:** Keep the master bedroom strictly free of conception calendars, test kits, or medical discussions. Treat your room as a joyous sanctuary of love and relaxation.\n"
            f"• **21-Day Couple Unwinding:** Dedicate 21 consecutive days to evening walks, gentle hydration, and lighthearted shared humor to soothe the nervous system."
        )
        validation_question = (
            "Does this resonance match what you have experienced? Have you noticed that anticipation, outside family expectations, and calendar scheduling have introduced subtle emotional stress, turning a natural blessing into a source of worry?"
        )
        permission_prompt = (
            "Do you want to harmonize your parental planetary cycles and invite auspicious progeny blessings? Can I suggest consecrated Jupiter-Venus remedies and bedroom Vastu protocols for you?"
        )
        remedies = [
            {
                "category": "Progeny Elemental Alignment",
                "title": "East / North-East Wood Element Activation",
                "instruction": "Place a healthy, flourishing green plant or a natural wooden flute in the East sector of your living room. Keep this area bright, fresh, and clutter-free.",
                "purpose": "Activates Jupiter's Jeeva (Life-force) vibration for healthy conception and family expansion."
            },
            {
                "category": "Karmic Progeny Charity",
                "title": "Thursday Guru Cow Feeding",
                "instruction": "On Thursday mornings, feed indigenous cows with soaked yellow chana dal, a pinch of turmeric, and a piece of jaggery wrapped in wheat dough.",
                "purpose": "Invites the compassionate blessings of Jupiter (Guru) for healthy progeny and marital peace."
            },
            {
                "category": "Bedroom Vastu Harmonization",
                "title": "South-West Master Bedroom Grounding",
                "instruction": "Ensure your master bed has a solid wooden headboard oriented toward South or East. Remove mirrors reflecting the bed, and introduce warm earth colors (peach, light yellow, cream).",
                "purpose": "Stabilizes the Earth element to create a deeply secure, peaceful womb environment."
            }
        ]

    elif topic == "partner_matching":
        why_happening = (
            f"Evaluating life partner compatibility through classical Sankhya Shastra, Lo Shu grid completeness, and planetary conjunction harmonies. "
            f"Your foundational Driver {driver} ({d_info['planet']}) and Conductor {conductor} ({c_info['planet']}) determine your emotional core "
            f"and lifelong destiny direction. {bnn_note}{lo_shu_note} "
            f"True cosmic compatibility is not about identical personalities — it is about complementary planes where one partner's natural numbers "
            f"complete the missing planes of the other, creating mutual protection and harmonious compounding."
        )
        direct_answer = (
            f"**1. Luminous Compatibility Factors & Mutual Synergy:**\n"
            f"• **Complementary Gifts:** {first_name}, your natural gifts of dedication and perception seek a partner who brings balancing grounding and emotional tenderness. When aligned, your combined matrix creates strong material security and mutual respect.\n"
            f"• **Shared Core Values:** Longevity in your union thrives on transparent communication, shared financial principles, and mutual family honor.\n\n"
            f"**2. Gentle Shadow Traits & Interpersonal Vulnerabilities (Empathetic Counseling Guidance):**\n"
            f"• **Contrasting Pacing Habits:** Differing natural tempos (one partner moving rapidly while the other prefers careful deliberation) can be mistaken for disinterest if expectations are not spoken softly.\n"
            f"• **Pride in Arguments:** Under stress, stubborn defense of personal viewpoints can delay easy compromises.\n\n"
            f"**3. Mindful Precautions & Marriage Guardrails:**\n"
            f"• **Transparent Financial Alignment:** Discuss long-term asset planning and family obligations candidly before tying commitments.\n"
            f"• **Emotional Softening:** Practice active listening without planning your rebuttal while the other person is speaking."
        )
        validation_question = (
            "Does this resonance match your experience in relationships? Have you observed that while there is strong attraction and respect, differences in decision-making speed or emotional expression have required conscious patience?"
        )
        permission_prompt = (
            "Do you want to harmonize your partnership vibrations and identify the most auspicious marriage timing window? Can I suggest consecrated Venusian remedies and living space alignments?"
        )
        remedies = [
            {
                "category": "Relationship Harmony Ritual",
                "title": "Friday Venus Attunement",
                "instruction": "Wear pastel pink, cream, or soft white on Fridays. Keep a small natural rose quartz crystal or fresh white flowers in the South-West sector of your room.",
                "purpose": "Activates gentle Venusian charm and dissolves conversational sharpness between partners."
            },
            {
                "category": "Living Space Remedy",
                "title": "South-West Earth Element Stabilization",
                "instruction": "Keep the South-West corner of your bedroom heavy, uncluttered, and warm. Avoid water features, aquariums, or blue decor in this corner.",
                "purpose": "Stabilizes marital bonds and protects the union against outside family interference."
            }
        ]

    elif topic == "business_partnership":
        why_happening = (
            f"Commercial partnerships are governed by Mercury (Budha — Trade & Negotiation), Saturn (Shani — Legal binding & Delivery), "
            f"and Sun (Surya — Executive command). Your Driver {driver} ({d_info['planet']}) and Conductor {conductor} ({c_info['planet']}) "
            f"bring distinct commercial strengths. {bnn_note}{lo_shu_note} "
            f"Friction in business partnerships almost always arises when informal personal friendship is allowed to blur documented financial responsibilities."
        )
        direct_answer = (
            f"**1. Luminous Commercial Strengths & Enterprise Synergy:**\n"
            f"• **Strategic Breadth:** {first_name}, you have a sharp eye for value creation, market positioning, and structured delivery.\n"
            f"• **Commercial Network Value:** Your ability to build trusted client relationships provides an enduring competitive advantage.\n\n"
            f"**2. Gentle Shadow Traits & Partnership Vulnerabilities (Empathetic Counseling Guidance):**\n"
            f"• **The Informal Agreement Blindspot:** Relying on verbal goodwill or informal handshakes because you consider the partner a friend creates unspoken resentment when workload distribution becomes uneven.\n"
            f"• **Hesitation in Audit Follow-ups:** Delaying difficult financial check-ins out of politeness invites cash-flow confusion.\n\n"
            f"**3. Mindful Precautions & Commercial Guardrails:**\n"
            f"• **Written Operating Agreements:** Ensure equity splits, capital contribution deadlines, IP ownership, and exit clauses are documented by a neutral legal advisor.\n"
            f"• **Distinct Spheres of Authority:** Define who owns Sales vs Operations vs Finance so decisions never paralyze the business."
        )
        validation_question = (
            "Does this reflect your partnership dynamics? Have you observed that while the business vision is promising, unclear boundaries around daily duties or financial accountability have created subtle operational friction?"
        )
        permission_prompt = (
            "Do you want to harmonize your business partnership and protect commercial profits? Can I suggest consecrated Budha remedies and office Vastu orientations for you?"
        )
        remedies = [
            {
                "category": "Commercial Flow Activation",
                "title": "North & North-West Trade Alignment",
                "instruction": "Place your primary desk or meeting table facing North. Ensure the North-West sector (supportive networks and trade banking) is well-lit and clutter-free.",
                "purpose": "Attracts high-value contracts and ensures smooth bank liquidity."
            },
            {
                "category": "Mercury Trade Pacification",
                "title": "Wednesday Green Donation",
                "instruction": "Donate green pens, notebooks, or study materials to deserving students on Wednesday mornings.",
                "purpose": "Strengthens Mercury (Budha) for intellectual sharpness and conflict-free business negotiations."
            }
        ]

    elif topic == "wealth_obstacles":
        why_happening = (
            f"In classical numerology, financial blockages, trapped funds, and sudden debt are governed by imbalances between "
            f"Driver {driver} ({d_info['planet']}) and Conductor {conductor} ({c_info['planet']}), compounded by {bnn_note}{lo_shu_note} "
            f"When the central Number 5 (stability) or Number 4 (structure) is deficient, or the North (Water/Kubera) or South-East (Fire/Venus) "
            f"sectors are energetically obstructed, money enters the matrix but drains rapidly through unexpected emergency obligations."
        )
        direct_answer = (
            f"**1. Luminous Earning Capability & Value Creation:**\n"
            f"• **Inherent Earning Magnetism:** {first_name}, you possess strong natural capability to generate capital and negotiate commercial value.\n"
            f"• **Resourcefulness Under Pressure:** When focused, your ability to create multiple revenue streams is formidable.\n\n"
            f"**2. Gentle Shadow Traits & Capital Outflow Vulnerabilities (Constructive Wealth Guidance):**\n"
            f"• **The Emotional Giving Leak:** A generous or trusting heart often prompts you to lend money to relatives or acquaintances without formal documentation, resulting in trapped, unrecoverable capital.\n"
            f"• **Impulse Discharges Under Fatigue:** Subconscious emotional stress can trigger retail therapy or impulsive purchases that dismantle savings.\n\n"
            f"**3. Mindful Precautions & Debt Clearance Guardrails:**\n"
            f"• **The Automated 20% Retention Firewall:** The instant any payment lands in your account, automatically divert 20% into an inaccessible, locked savings or debt-amortization instrument.\n"
            f"• **Zero Unwritten Loans:** Implement a strict personal rule: never lend money you cannot comfortably afford to gift as charity."
        )
        validation_question = (
            "Does this reflect your financial experience over recent months? Have you observed that despite your strong earning efforts, unexpected family expenses, trapped receivables, or sudden outflow leaks have made it difficult to build a lasting cushion?"
        )
        permission_prompt = (
            "Do you want to plug these wealth leakages and restore sovereign abundance? Can I suggest consecrated Kubera remedies and financial Vastu clearings for you?"
        )
        remedies = [
            {
                "category": "Kubera Opportunity Flow",
                "title": "North Sector Water Energy Clearing",
                "instruction": "Ensure the North sector of your home or office is immaculately clean. Place a clear glass bowl of clean water with a single green leaf or fresh white petals in the North, refreshed daily.",
                "purpose": "Clears energetic blockage in Kubera's wealth channel and dissolves financial stagnation."
            },
            {
                "category": "Venusian Cashflow Blessing",
                "title": "Friday Curd & White Offering",
                "instruction": "Donate fresh curd, white rice, or milk-based sweets to elders or cows on Friday mornings with a sincere prayer for steady abundance.",
                "purpose": "Invites the benevolent grace of Venus (Shukra) to steady liquid cash-flow and protect retained capital."
            }
        ]

    elif topic == "property":
        why_happening = (
            f"Property acquisition, land, home construction, and fixed assets are governed by Mars (Mangal — Bhoomi Karaka), "
            f"Saturn (Shani — Land foundations & structural permanence), and Venus (Shukra — Domestic luxury & comfort). "
            f"Your Driver {driver} ({d_info['planet']}) and Conductor {conductor} ({c_info['planet']}) reveal your material asset capacity. "
            f"{bnn_note}{lo_shu_note} In 2026, you are navigating Personal Year {personal_year}. When spatial Vastu friction occurs in the South (Mars/Stability) "
            f"or South-West (Earth foundation), property deals face paperwork delays, registry obstacles, or unexpected construction stalls."
        )
        direct_answer = (
            f"**1. Luminous Material Strengths & Asset Accumulation:**\n"
            f"• **Long-Term Asset Instinct:** {first_name}, you have a grounded capacity to visualize real estate value and build lasting physical roots.\n"
            f"• **Enduring Ownership:** Real estate and fixed assets compound steadily for you once the foundational paperwork is stabilized.\n\n"
            f"**2. Gentle Shadow Traits & Property Vulnerabilities (Constructive Vastu Guidance):**\n"
            f"• **Impatience with Legal Titling:** Rushing into property agreements without third-party title deed verification can lock capital in administrative limbo.\n"
            f"• **Emotional Over-Extension:** Falling in love with an aesthetic home while stretching financial reserves beyond safe leverage limits causes unnecessary domestic stress.\n\n"
            f"**3. Mindful Precautions & Asset Guardrails:**\n"
            f"• **Mandatory 30-Year Title Search:** Verify all land registry documents through an independent property attorney before advancing token deposits.\n"
            f"• **Auspicious Execution Timing:** Finalize registries and possession ceremonies during your favorable planetary hours on {lucky['days']}."
        )
        validation_question = (
            "Does this resonance match your property trajectory? Specifically, have you experienced unexpected timeline delays, documentation friction, or contractor stalls when trying to finalize property, land, or home renovation plans?"
        )
        permission_prompt = (
            "Do you want to dissolve these property delays and activate auspicious land blessings? Can I suggest consecrated Bhoomi Vastu remedies and directional alignments for you?"
        )
        remedies = [
            {
                "category": "Bhoomi Vastu Harmonization",
                "title": "South-West Earth Element Stabilization",
                "instruction": "Place a solid terracotta, stone, or clay artifact in the South-West corner of your primary residence. Ensure this corner is heavy and stable.",
                "purpose": "Grounds the Earth element (Prithvi) to secure property ownership and prevent litigation."
            },
            {
                "category": "Mars Asset Pacification",
                "title": "Tuesday Jaggery Offering",
                "instruction": "On Tuesday mornings, offer jaggery and roasted chickpeas (chana) to monkeys or donate red lentils (masoor dal) to those in need.",
                "purpose": "Invites the protective strength of Mars (Bhoomi Karaka) to remove construction roadblocks."
            }
        ]

    elif topic == "universal_obstacles":
        why_happening = (
            f"When obstacles appear simultaneously across career, wealth, health, and relationships, you are moving through what classical Sankhya Shastra "
            f"and classical numerology traditions term the **Karmic Pivot Window**. Your Driver {driver} ({d_info['planet']}) and Conductor {conductor} ({c_info['planet']}) "
            f"are experiencing a synchronized energetic reset. {bnn_note}{lo_shu_note} In Personal Year {personal_year}, the universe temporarily "
            f"pauses superficial external momentum to burn away outdated habits, toxic associations, and ungrounded ambitions. "
            f"This universal resistance is not a curse or permanent misfortune — it is an intensive sacred restructuring designed to forge unshakeable inner sovereignty."
        )
        direct_answer = (
            f"**1. Luminous Inner Fortitude & Hidden Mastery:**\n"
            f"• **Unbreakable Core Resilience:** {first_name}, your matrix carries profound spiritual depth and stamina. The very fact that you are standing through multi-directional pressure proves that your constitutional endurance is immense.\n"
            f"• **Approaching Breakthrough:** Universal resets always precede significant, long-term phase shifts; once alignment is restored, momentum returns with compounded force.\n\n"
            f"**2. Gentle Shadow Traits & Universal Fatigue Vulnerabilities (Empathetic Counseling Guidance):**\n"
            f"• **Fighting the Current (Force Fatigue):** Trying to kick open 10 doors at once while the celestial tide is in a pause phase only drains your vital energy, resulting in physical exhaustion and mental despair.\n"
            f"• **The Isolation Trap:** Feeling that nobody understands your struggle can tempt you to withdraw into solitary bitterness, cutting off supportive universal synchronicities.\n\n"
            f"**3. Mindful Precautions & Karmic Pivot Guardrails:**\n"
            f"• **The Single-Vector Protocol:** Stop battling everything at once. Choose ONE life pillar (health or basic daily routine) to stabilize this week, letting the others pause temporarily without self-judgment.\n"
            f"• **Daily Energy Shield:** Begin each day with 10 minutes of silent breathwork facing East before touching any digital device."
        )
        validation_question = (
            "Does this deep resonance match what you have been feeling? Have you felt as though invisible resistance has appeared simultaneously across career, relationships, and finances, creating a profound inner exhaustion and an undeniable pull for a complete life reset?"
        )
        permission_prompt = (
            "Do you want to dissolve this multi-system friction and activate divine support? Can I suggest consecrated all-round harmonizing rituals, Brahmasthan space clearing, and auspicious timing for you?"
        )
        remedies = [
            {
                "category": "Master Space Harmonization",
                "title": "Brahmasthan (Center of Home) Clearing",
                "instruction": "Identify the geographical center of your living space. Ensure this area is completely free of heavy clutter, dustbins, dark storage boxes, or non-functional items. Keep it bright, open, and lightly fragrant.",
                "purpose": "Activates the central energetic vortex of your home, dissolving universal stagnation across all life areas."
            },
            {
                "category": "Master Planetary Pacification",
                "title": "Saturday Peepal Tree Diya & Charity",
                "instruction": "On Saturday evening after sunset, light a mustard oil earthen lamp (diya) near a Peepal tree or feed black street dogs with bread dipped in milk or oil without seeking recognition.",
                "purpose": "Pacifies karmic Saturnian debts and clears invisible roadblocks across career and finances."
            },
            {
                "category": "Solar Vitality & Hope Activation",
                "title": "Morning Surya Arghya & Gayatri Centering",
                "instruction": "Stand facing the morning sun for 7 minutes. Offer fresh water from a clean vessel, taking 7 slow deep breaths while visualizing golden light clearing every shadow of doubt from your heart.",
                "purpose": "Restores radiant solar vitality, dispels psychic despair, and anchors unwavering faith."
            }
        ]

    else: # general / destiny
        why_happening = (
            f"You are experiencing a natural recalibration between your outer personality (Driver {driver}, {d_info['planet']}) "
            f"and your deeper life path (Conductor {conductor}, {c_info['planet']}). "
            f"{bnn_note}{lo_shu_note} In Personal Year {personal_year}, old habitual patterns are falling away to create space for your authentic destiny. "
            f"The resistance you feel is not a permanent stop — it is a signal to realign your daily habits with your core purpose."
        )
        direct_answer = (
            f"**1. Luminous Natural Strengths & Destiny Flow:**\n"
            f"• **Intuitive Inner Guidance:** {first_name}, your core vibration is naturally attuned to higher clarity, integrity, and self-determination. You have a quiet inner compass that knows the right path forward.\n"
            f"• **Resilience Through Cycles:** You possess the fortitude to reinvent yourself and turn life transitions into permanent stepping stones of wisdom.\n\n"
            f"**2. Gentle Shadow Traits & Energetic Blindspots (Warm Mentorship):**\n"
            f"• **Over-Analyzing Transitions:** During transitional cycles (such as Personal Year {personal_year}), you may experience mental restlessness or second-guess your direction when immediate results are not instantly visible.\n"
            f"• **Distraction Friction:** Entertaining too many opinions from well-meaning friends or relatives can cloud your authentic instinct.\n\n"
            f"**3. Mindful Precautions & Alignment Guardrails:**\n"
            f"• **Morning Silent Centering:** Dedicate 10 minutes each morning in quiet reflection facing your lucky direction before engaging with the outside world.\n"
            f"• **Decisive Simplification:** Prune unnecessary commitments and align your daily schedule with your single most vital life objective."
        )
        validation_question = (
            "Does this resonance match what you have felt in your personal trajectory over recent months? Specifically, have you felt that an old way of operating is no longer serving you, creating a strong internal pull for a decisive reset?"
        )
        permission_prompt = (
            "Do you want to overcome this uncertainty and align with your authentic life path? Can I suggest consecrated remedies and timeline windows for you?"
        )

        # General Remedies
        remedies = [
            {
                "category": "Personal Grounding Ritual",
                "title": "Daily Centering & Morning Intention",
                "instruction": f"Begin each morning by sitting quietly facing {lucky['direction']} for 5 minutes. State your core intention clearly in present tense.",
                "purpose": "Attunes your conscious mind with your core destiny frequency."
            },
            {
                "category": "Color & Aura Shield",
                "title": "Aura Protection Attire",
                "instruction": f"Incorporate {lucky['colors']} into your daily wardrobe or accessories, especially on {lucky['days']}.",
                "purpose": "Strengthens your personal energetic field against psychic fatigue and self-doubt."
            },
            {
                "category": "Karmic Balance Charity",
                "title": "Selfless Kindness",
                "instruction": "Perform one anonymous act of kindness or feed street animals once a week without seeking praise.",
                "purpose": "Dissolves subconscious karmic knots and invites universal support."
            }
        ]

    # 2. Add Practical Physical Action Remedy
    if unified_multi_system and unified_multi_system.get("remedies"):
        for u_rem in unified_multi_system["remedies"][:2]:
            remedies.append({
                "category": "Physical Grounding Practice",
                "title": u_rem.get("title", "Harmonizing Action"),
                "instruction": u_rem.get("action", ""),
                "purpose": "Provides direct, concrete physical action to align vibrational frequencies."
            })

    # 3. Add element remedy if deficient
    if core_matrix and core_matrix.get("elements_balancing", {}).get("deficient"):
        def_item = core_matrix["elements_balancing"]["element_remedies"][0]
        remedies.append({
            "category": f"Natural Element Balancing ({def_item['element']})",
            "title": f"Balancing {def_item['element']} Element",
            "instruction": def_item["balancing_remedy"],
            "purpose": f"Restores equilibrium for {def_item['qualities']}."
        })
    # 4. Add missing number remedy
    if core_matrix and core_matrix.get("missing_numbers_remedies"):
        miss_first = core_matrix["missing_numbers_remedies"][0]
        remedies.append({
            "category": "Energy Field Harmonization",
            "title": f"Harmonizing {miss_first['planet']} Energy Frequency",
            "instruction": miss_first["remedy"],
            "purpose": f"Activates the {miss_first['direction']} direction and balances natural energy flow."
        })

    # 5. Add Kua Directional Alignment Remedy
    if core_matrix:
        kua_p = core_matrix["core_numbers"].get("kua_profile", {})
        if kua_p:
            remedies.append({
                "category": "Spatial Direction Alignment",
                "title": f"Auspicious Direction: {kua_p.get('wealth_direction')}",
                "instruction": f"Orient your office desk facing {kua_p.get('wealth_direction')} for professional focus, and sleep with head toward {kua_p.get('health_direction')} for vitality.",
                "purpose": "Harnesses natural environmental energy for steady productivity."
            })

        # 6. Add Poorak (Complementary / Harmonizing) Number Remedy
        poorak_p = core_matrix.get("poorak_number_analysis")
        if poorak_p:
            remedies.append({
                "category": "Complementary Harmonic Bridge",
                "title": f"Harmonizing Bridge Frequency ({poorak_p['poorak_planet']})",
                "instruction": f"{poorak_p['harmonizing_ritual']} {poorak_p['rationale']}",
                "purpose": "Bridges energetic tension and stabilizes personal vitality."
            })

    alignment_status = "ALIGNED" if is_aligned else "NOT ALIGNED"
    alignment_grade = "High Natural Resonance (78% – 92%)" if is_aligned else "Refinement & Calibration Phase (68% – 76%)"
    alignment_summary = (
        f"{first_name}, your personal energy cycles indicate {'high natural harmony and positive flow' if is_aligned else 'a transitional calibration phase'} "
        f"in {topic.capitalize()} at this stage. By applying the recommended focus strategies and supportive lifestyle practices below, you smoothly dissolve subtle blockages and enhance your receptivity to upcoming opportunities."
    )

    why_happening_dict = {
        "core_numbers": f"Core Energy: {driver} ({d_info['planet']}) · Life Direction: {conductor} ({c_info['planet']})",
        "core_energies": f"Core Day Energy: {driver} ({d_info['planet']}) · Life Path Direction: {conductor} ({c_info['planet']})",
        "root_cause_explanation": why_happening,
        "validation_question": validation_question,
        "permission_prompt": permission_prompt,
        "bnn_conjunction": bnn_title,
        "bnn_archetype": bnn_archetype,
        "lo_shu_missing_numbers": missing_numbers,
        "lo_shu_repetitive_numbers": repetitive_numbers,
        "personal_year": personal_year,
        "elemental_dynamic": f"Core Energy {driver} interacting with Life Path {conductor}"
    }

    if bnn_profile:
        prim_p = bnn_profile.get("primary_pair_analysis", {})
        why_happening_dict["planetary_alignment_flow"] = prim_p.get("title", "")
        why_happening_dict["core_archetype"] = prim_p.get("archetype", "")
        why_happening_dict["potential_trajectory"] = prim_p.get("bnn_predictions", "")
        if bnn_profile.get("compound_day_analysis"):
            why_happening_dict["compound_day_trajectory"] = bnn_profile["compound_day_analysis"].get("bnn_predictions", "")
        if bnn_profile.get("profession_karma_analysis"):
            why_happening_dict["career_alignment_trajectory"] = bnn_profile["profession_karma_analysis"].get("bnn_predictions", "")

    if unified_multi_system:
        why_happening_dict["classical_harmonic_alignment"] = unified_multi_system["vedic_jyotish_analysis"].get("yoga_name", "")
        why_happening_dict["classical_timing_insight"] = unified_multi_system["vedic_jyotish_analysis"].get("prediction", "")
        why_happening_dict["subtle_timing_verdict"] = unified_multi_system["kp_sublord_analysis"].get("verdict", "")
        why_happening_dict["subtle_timing_focus"] = unified_multi_system["kp_sublord_analysis"].get("fruit", "")
        why_happening_dict["integrated_energy_frequency"] = f"{unified_multi_system['lal_kitab_analysis'].get('masnooi_planet')} (Vibration {unified_multi_system['lal_kitab_analysis'].get('masnooi_number')})"

    if lo_shu_analysis:
        why_happening_dict["matrix_completed_planes"] = lo_shu_analysis.get("completed_planes", [])
        why_happening_dict["matrix_refinement_areas"] = lo_shu_analysis.get("missing_numbers", [])
    if core_matrix:
        if core_matrix.get("core_numbers", {}).get("kua_profile"):
            k_prof = core_matrix["core_numbers"]["kua_profile"]
            why_happening_dict["spatial_orientation"] = f"Group: {k_prof['energy_group']} · Prosperity: {k_prof['wealth_direction']} · Vitality: {k_prof['health_direction']}"
        if core_matrix.get("poorak_number_analysis"):
            why_happening_dict["harmonic_bridge"] = f"{core_matrix['poorak_number_analysis']['poorak_planet']} Bridge · {core_matrix['poorak_number_analysis']['rationale']}"
        if core_matrix.get("vastu_directional_synthesis"):
            why_happening_dict["environmental_synthesis"] = core_matrix["vastu_directional_synthesis"]

    # ── Real-Time Planetary Transit (Gochar) Active Convergence ──────────────
    try:
        from app.engine.astrology_correlation_engine import correlate_planetary_transits
        py_calc = (driver + (month or 1) + 2026) % 9 or 9
        transit_synthesis = correlate_planetary_transits(driver, conductor, py_calc)
        if transit_synthesis and "transit_convergence_summary" in transit_synthesis:
            why_happening_dict["active_celestial_transit"] = transit_synthesis["transit_convergence_summary"]
    except Exception:
        pass

    # ── Grounded Book & Compendium Citations (Strict Privacy Shield Applied) ──
    citations = []
    for rp in rag_predictions:
        citations.append(sanitize_citation({
            "source": rp.get("source", ""),
            "location": rp.get("location", ""),
            "category": "Proprietary Classical Foundation",
            "excerpt": rp.get("content", "")
        }))
    for rr in rag_remedies:
        citations.append(sanitize_citation({
            "source": rr.get("source", ""),
            "location": rr.get("location", ""),
            "category": "Proprietary Harmonization Protocols",
            "excerpt": rr.get("content", "")
        }))
    for rs in rag_samples:
        citations.append(sanitize_citation({
            "source": rs.get("source", ""),
            "location": rs.get("location", ""),
            "category": "Clinical Diagnostic Architecture",
            "excerpt": rs.get("content", "")
        }))

    if rag_predictions:
        first_pred = sanitize_text(rag_predictions[0].get("content", "").replace("\n", " ").strip())
        if len(first_pred) > 280:
            first_pred = first_pred[:280] + "..."
        why_happening_dict["classical_scriptural_grounding"] = first_pred
        why_happening_dict["grounded_source"] = f"{mask_source_name(rag_predictions[0].get('source', ''))} · {sanitize_location(rag_predictions[0].get('location', ''))}"

    # Grounded Compendium Remedy addition (Proprietary Privacy Shield Applied)
    for rr in rag_remedies:
        c_text = sanitize_text(rr.get("content", "").strip())
        if c_text and len(c_text) > 40:
            clean_instr = c_text.replace("\n", " ").strip()
            if len(clean_instr) > 240:
                clean_instr = clean_instr[:240] + "..."
            remedies.append({
                "category": "Classical Compendium Attunement",
                "title": "Numeros Vision Planetary Harmonization Protocol",
                "instruction": clean_instr,
                "purpose": "Planetary harmonization from verified classical treatises and remedy compendiums."
            })
            break

    res_data = {
        "direct_answer": direct_answer,
        "why_this_is_happening": why_happening_dict,
        "validation_question": validation_question,
        "permission_prompt": permission_prompt,
        "can_suggest_remedies": True,
        "remedies": remedies,
        "grounded_citations": citations,
        "lucky_elements": {
            "lucky_colors": lucky["colors"],
            "lucky_days": lucky["days"],
            "favorable_direction": lucky["direction"],
            "avoid_colors": lucky["avoid"],
            "sacred_metal_or_gem": lucky["metal_gem"],
            "safe_healing_crystals": [c.strip() for c in lucky["metal_gem"].replace(" or ", ",").replace(" in ", ",").split(",") if c.strip()][:3],
            "statutory_compliance_notice": "Statutory Qualification (Drugs & Magic Remedies Act 1954): Crystals and lifestyle practices are traditional cultural attunements, not medical cures or financial guarantees."
        },
        "vedic_lifestyle_guidance": {
            "dinacharya_focus": f"Begin your morning during Brahma Muhurta (5:00-6:30 AM) with mindful contemplation facing {lucky['direction']}.",
            "mindful_pause": f"Take 3 conscious breaths before high-stakes communications to ground Driver {driver} planetary energy.",
            "sattvic_discipline": "Incorporate pure, freshly prepared nutrition and maintain clean, decluttered workspace energy."
        },
        "topic": topic,
        "alignment_status": alignment_status,
        "alignment_grade": alignment_grade,
        "alignment_summary": alignment_summary
    }
    if is_international:
        intl_data = get_international_planetary_remedies(driver, conductor, missing_numbers, name or first_name)
        res_data["international_harmonization"] = intl_data
        # Replace or prepend remedies with international charitable giving and universal contemplative prayers
        d_char = intl_data["primary_charitable_giving"]["driver_charity"]
        prayer = intl_data["universal_contemplative_rituals"]["primary_prayer"]
        sig = intl_data["english_name_acoustics"]
        env = intl_data["environmental_harmonizers"]
        intl_remedies = [
            {
                "category": "Targeted Planetary Charity (Dana)",
                "title": f"Altruistic Giving for {d_char['planet']}",
                "instruction": f"On {d_char['timing']}, {d_char['recommended_action']} Intention: \"{d_char['karmic_intention']}\"",
                "purpose": "Directly harmonizes planetary friction through selfless community contribution."
            },
            {
                "category": "Universal Contemplative Prayer",
                "title": prayer["title"],
                "instruction": f"{prayer['candle_ceremony']} Meditate on the affirmation: \"{prayer['daily_affirmation']}\"",
                "purpose": "Grounds mental restlessness and aligns your heart with divine peace."
            },
            {
                "category": "English Name Signature Calibration",
                "title": "Acoustic Signature Elevation",
                "instruction": sig["signature_guidance"],
                "purpose": "Harmonizes spoken and written frequency for continuous professional elevation."
            },
            {
                "category": "Solfeggio Sound Frequency Tuning",
                "title": f"{env['prime_day_of_action']} Frequency Attunement",
                "instruction": f"Listen to {prayer['sound_frequency']} during morning contemplation or deep work. {env['workspace_orientation']}",
                "purpose": "Clears mental noise and aligns neural pathways for decision-making clarity."
            }
        ]
        res_data["remedies"] = intl_remedies + remedies[:2]
    if core_matrix:
        res_data["core_matrix_analysis"] = core_matrix
    if bnn_profile:
        res_data["planetary_profile_analysis"] = bnn_profile
    if lo_shu_analysis:
        res_data["energy_matrix_analysis"] = lo_shu_analysis
    if "transit_synthesis" in locals() and transit_synthesis:
        res_data["celestial_transits"] = transit_synthesis

    # NV THINK™: Logic-to-Psychology Framework & Multi-Model Consensus Integration
    try:
        from app.engine.nv_psychology_engine import nv_think_engine
        active_planes_list = lo_shu_analysis.get("active_planes", []) if lo_shu_analysis else []
        res_data["nv_think_diagnostic"] = nv_think_engine.evaluate_chart_synthesis(
            driver=driver,
            conductor=conductor,
            loshu_counts=counts_map,
            active_planes=active_planes_list,
            missing_numbers=missing_numbers,
            user_environment="Corporate / Professional Consultation Context"
        )
        res_data["multi_model_consensus"] = nv_think_engine.correlate_charm_ai_consensus(
            numerology_dasha={"active_dasha": d_info["planet"], "acute_window": f"Personal Year {personal_year} (2026-2027)"},
            vedic_factors={"favorable": is_aligned, "subperiod_lord": c_info["planet"]},
            kp_factors={"houses": [2, 6, 10, 11] if is_aligned else [6, 8, 12]},
            bnn_factors={"conjunction": bnn_title},
            seeker_question=question
        )
    except Exception as nv_err:
        logger.warning(f"NV THINK™ integration note: {nv_err}")

    def _sanitize_recursively(obj):
        if isinstance(obj, str):
            return sanitize_text(obj)
        elif isinstance(obj, list):
            return [_sanitize_recursively(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: _sanitize_recursively(v) for k, v in obj.items()}
        return obj

    return _sanitize_recursively(res_data)
