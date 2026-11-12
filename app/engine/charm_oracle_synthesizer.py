"""
app/engine/charm_oracle_synthesizer.py
======================================
MASTER CONVERSATIONAL SYNTHESIZER & CELESTIAL ORACLE FOR CHARM AI
Numeros Vision — "ANVEIL EVERY CHARM"

100% Deterministic Engine Authority:
- Implements Numeros Vision Classical Methodology 14 Classical Syllabus Topics:
  1. Planets (Power) -> Degree / Frequency of Repetition (1x Under, 2x Pair/Best, 3x Exaggerate, 4x Reactive, 5+ Volatile)
  2. Elements (Water, Earth, Wood, Metal, Fire) & Cardinal Directions
  3. Relationships (Love vs Arranged Marriage, Partner Compatibility & Harmony)
  4. Profession / Education / Career Alignments
  5. Partnership & Business Alignment
  6. Health, Vitality & Nervous Equilibrium
  7. Struggle vs Hidden Treasure (Raj Yogas: 4-5-6 Golden, 2-5-8 Silver, Planes)
  8. Colors, Days & Numbers (Friendly & Enemy Matrices)
  9. Foreign Settlement vs Homeland Stability
  10. Share Market, Stock Trading & Speculative Investments
  11. Child Conception / Progeny Blessings & Child Studies
  12. Good vs Bad attributes of numbers 1-9 (Communication, Intuition, Creativity, Discipline, Balance, Family, Healing/Occult, Finance, Aggression)
  13. Missing Lo Shu Numbers & Elemental Compensations
  14. Karmic Debt (13, 14, 16, 19) & Master Numbers (11, 22, 33)
  15. Name Balancing (Chaldean Acoustic Sum vs Driver/Conductor Harmony)
  16. Multi-Astrology Correlation (KP, Lal Kitab, Vedic Astro, BNN) with verified consensus level
  17. Geo-Aware, Culturally and Faith-Tailored Remedies (Hindu, Muslim, Christian, Sikh, Jain, Universal/Secular)
  18. Freemium Curiosity Hook & CTA ("ANVEIL EVERY CHARM")
"""

import re
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple
from app.engine.number_characteristics_registry import BIRTH_DAY_SUBDATE_REGISTRY
from app.engine.driver_conductor_81_engine import lookup_driver_conductor_81
from app.engine.five_elements_hygiene_engine import diagnose_user_elemental_hygiene
from app.engine.complementary_poorak_engine import calculate_complementary_poorak

# ── Planetary Baseline Rulers ────────────────────────────────────────────────
PLANETARY_INFO = {
    1: {"planet": "Sun (Surya)", "element": "Water", "direction": "North", "nature": "Executive will, leadership, pioneer, communication"},
    2: {"planet": "Moon (Chandra)", "element": "Earth", "direction": "South-West", "nature": "Intuition, sensitive power, empathy, diplomacy"},
    3: {"planet": "Jupiter (Guru)", "element": "Wood", "direction": "East", "nature": "Creativity, imagination power, wisdom, counseling"},
    4: {"planet": "Rahu (North Node)", "element": "Wood", "direction": "South-East", "nature": "Discipline, organized power, unconventional systems"},
    5: {"planet": "Mercury (Budh)", "element": "Earth", "direction": "Center", "nature": "Central balance, health, success, growth, commerce"},
    6: {"planet": "Venus (Shukra)", "element": "Metal (Gold)", "direction": "North-West", "nature": "Home, family, love relationships, luxury"},
    7: {"planet": "Ketu (South Node)", "element": "Metal (Silver)", "direction": "West", "nature": "Disappointments, healing, wisdom, spirituality, occult"},
    8: {"planet": "Saturn (Shani)", "element": "Earth", "direction": "North-East", "nature": "Money & finance management, compounding, endurance"},
    9: {"planet": "Mars (Mangal)", "element": "Fire", "direction": "South", "nature": "Aggression, ego, humanity, humility, protective drive"}
}

# ── Numeros Vision Classical Methodology Good vs Bad Number Attributes (Slide 3) ────────────
NUMBER_DUAL_ATTRIBUTES = {
    1: {
        "attribute": "Communication & Executive Leadership",
        "good": "Direct, clear, inspiring vision, articulate executive voice, decisive initiative, dignified self-respect",
        "bad": "Arrogant speech, interrupting others, dominating conversations, stubborn refusal to listen, ego clashes",
        "under": "Hesitation in public speaking, difficulty asserting authority, holding back honest thoughts",
        "exaggerated": "Overbearing directives, blunt aggression, demanding blind obedience"
    },
    2: {
        "attribute": "Intuition & Sensitive Power",
        "good": "Deep emotional intelligence, instinctual empathy, gentle diplomacy, creative harmony, marital warmth",
        "bad": "Hypersensitivity, mood swings, chronic self-doubt, emotional dependency, easily offended",
        "under": "Suppressed emotions, cold detachment, difficulty sensing partner or team sentiments",
        "exaggerated": "Emotional over-reaction, anxiety spirals, paralyzing fear of rejection"
    },
    3: {
        "attribute": "Creativity & Imagination Power",
        "good": "Expansive wisdom, compelling mentorship, visionary storytelling, artistic fluency, strategic counsel",
        "bad": "Scattered focus, superficial enthusiasm, lecturing rather than listening, unfinished projects",
        "under": "Creative blockages, fear of self-expression, difficulty trusting one's own intellect",
        "exaggerated": "Mental restlessness, exaggerating facts, patronizing attitude toward peers"
    },
    4: {
        "attribute": "Discipline & Organised Power",
        "good": "Systemic architecture, meticulous planning, high technical precision, unwavering reliability",
        "bad": "Rigid obstinacy, sudden volatile disruptions, obsession with trivial details, resistance to change",
        "under": "Chaotic disorganization, messy physical/digital desk, procrastination with timelines",
        "exaggerated": "Compulsive micromanagement, harsh skepticism, stress from minor deviations"
    },
    5: {
        "attribute": "Balance (Health, Wealth, Career & Relationships)",
        "good": "Harmonious central equilibrium, swift commercial adaptability, networking charisma, multi-domain agility",
        "bad": "Restlessness, gambling with impulsive risks, lack of follow-through, sensory over-indulgence",
        "under": "Loss of life balance, feeling torn between work and family, sluggish career progress",
        "exaggerated": "Chronic multitasking with zero depth, erratic lifestyle, constant changing of ventures"
    },
    6: {
        "attribute": "Home, Family & Love Relationships",
        "good": "Luxurious warmth, marital fidelity, aesthetic excellence, generous caretaking, high social standing",
        "bad": "Codependency, domestic friction, excessive status-seeking spending, smothering attachments",
        "under": "Strained home atmosphere, lack of comfort or aesthetic ease, relationship hesitation",
        "exaggerated": "Emotional manipulation within family, unrealistic perfectionist romantic expectations"
    },
    7: {
        "attribute": "Disappointments, Healing, Wisdom & Occult Depth",
        "good": "Profound research acumen, spiritual detachment, esoteric discernment, healing presence, truth-seeking",
        "bad": "Cynical withdrawal, feeling betrayed by loved ones, chronic disappointment, intellectual arrogance",
        "under": "Superficial outlook, lack of introspective discernment, trusting deceptive promises easily",
        "exaggerated": "Excessive isolation, paranoid secrecy, disconnect from mundane social responsibilities"
    },
    8: {
        "attribute": "Money & Finance Management",
        "good": "Monumental compounding wealth, financial prudence, institutional endurance, objective fairness",
        "bad": "Financial anxiety, trapping capital in illiquid deadlocks, feeling crushed by heavy labor, ruthlessness",
        "under": "Careless expenditure, financial leaks, difficulty organizing budgets or saving consistently",
        "exaggerated": "Cold materialism, hoarding out of fear of scarcity, severe workaholism damaging health"
    },
    9: {
        "attribute": "Aggression, Ego, Humanity & Humility",
        "good": "Selfless humanitarian leadership, noble courage, protective strength, energetic initiative",
        "bad": "Destructive temper tantrums, bruised ego, burning bridges in self-righteous fury, reckless haste",
        "under": "Lack of protective boundaries, passive acceptance of mistreatment, low physical stamina",
        "exaggerated": "Explosive rage, vindictive arguments, treating minor disagreements as personal warfare"
    }
}

# ── Numeros Vision Classical Methodology Degree Classification (Slide 4) ────────────────────
def classify_digit_degree(digit: int, count: int) -> Dict[str, Any]:
    dual = NUMBER_DUAL_ATTRIBUTES.get(digit, {})
    if count == 0:
        return {
            "degree_code": "MISSING",
            "degree_label": "Missing Number (Karmic Void)",
            "impact_grade": "DEFICIENT",
            "summary": f"Number {digit} is absent from your static birth matrix. Its core attribute ({dual.get('attribute', '')}) requires conscious remedial cultivation.",
            "manifestation": dual.get("under", "Needs active compensation")
        }
    elif count == 1:
        return {
            "degree_code": "UNDER",
            "degree_label": "One Time (Under / Developing Energy)",
            "impact_grade": "DEVELOPING",
            "summary": f"Present 1 time. The attribute of {dual.get('attribute', '')} is functional but gentle; requires conscious nurturing to reach peak expression.",
            "manifestation": dual.get("under", dual.get("good", ""))
        }
    elif count == 2:
        return {
            "degree_code": "PAIR",
            "degree_label": "Two Times / Pair (BEST — Peak Balanced Harmony)",
            "impact_grade": "OPTIMAL",
            "summary": f"Present 2 times (Pair). This is the best-performing and most harmonious energetic balance in classical canon.",
            "manifestation": dual.get("good", "")
        }
    elif count == 3:
        return {
            "degree_code": "EXAGGERATE",
            "degree_label": "Three Times (Exaggerated / Aggressive Intensity)",
            "impact_grade": "AMPLIFIED",
            "summary": f"Present 3 times. The energy of {dual.get('attribute', '')} is heavily amplified; prone to restlessness or friction unless grounded consciously.",
            "manifestation": dual.get("exaggerated", dual.get("bad", ""))
        }
    elif count == 4:
        return {
            "degree_code": "REACTIVE",
            "degree_label": "Four Times (Reactive Negative Zone)",
            "impact_grade": "HIGH_FRICTION",
            "summary": f"Present 4 times. Reaches the reactive negative zone. Causes extreme internal friction or volatility unless stabilized through elemental grounding.",
            "manifestation": dual.get("bad", "")
        }
    else:
        return {
            "degree_code": "VOLATILE",
            "degree_label": f"{count} Times (Over-Reactive / Volatile Zone)",
            "impact_grade": "EXTREME_IMBALANCE",
            "summary": f"Present {count} times. Over-saturated planetary power; requires urgent elemental balancing to prevent burnout or chronic friction.",
            "manifestation": dual.get("bad", "")
        }

# ── Lo Shu Planes Matrix ──────────────────────────────────────────────────────
LO_SHU_PLANES = [
    {"name": "Mental Plane (4-9-2)", "nums": [4, 9, 2], "gift": "Sharp memory, analytical acumen, and deep intellect."},
    {"name": "Emotional Plane (3-5-7)", "nums": [3, 5, 7], "gift": "Strong intuition, spiritual empathy, and heart-centered relationships."},
    {"name": "Practical Plane (8-1-6)", "nums": [8, 1, 6], "gift": "Material execution, practical business acumen, and grounding skills."},
    {"name": "Thought Plane (4-3-8)", "nums": [4, 3, 8], "gift": "Visionary strategic foresight, conceptual mastery, and deep planning."},
    {"name": "Will Plane (9-5-1)", "nums": [9, 5, 1], "gift": "Unshakeable persistence, dynamic leadership will, and goal completion."},
    {"name": "Action Plane (2-7-6)", "nums": [2, 7, 6], "gift": "Rapid execution, social responsiveness, and swift physical action."},
    {"name": "Golden Raj Yoga (4-5-6)", "nums": [4, 5, 6], "gift": "Golden success yoga: steady wealth accumulation, name fame, and executive authority."},
    {"name": "Silver Raj Yoga (2-5-8)", "nums": [2, 5, 8], "gift": "Silver success yoga: real estate prosperity, land ownership, and emotional resilience."}
]

# ── Chaldean Alphabet Values for Name Balancing ──────────────────────────────
CHALDEAN_MAP = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'K': 2, 'R': 2,
    'C': 3, 'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
}

def calculate_chaldean_name(name: str) -> Tuple[int, int]:
    clean = re.sub(r'[^A-Za-z]', '', name).upper()
    total = sum(CHALDEAN_MAP.get(ch, 0) for ch in clean)
    single = total
    while single > 9 and single not in (11, 22, 33):
        single = sum(int(d) for d in str(single))
    return total, single

def reduce_digit(n: int) -> int:
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n


def _base_1_to_9(n: int) -> int:
    val = abs(int(n))
    while val > 9:
        val = sum(int(d) for d in str(val))
    return val if 1 <= val <= 9 else 1


def _has_word(ql: str, terms: List[str]) -> bool:
    return any(re.search(r"\b" + re.escape(w) + r"\b", ql) for w in terms)

# ── Religion & Faith Detector ────────────────────────────────────────────────
def detect_faith_and_tradition(name: str, explicit_faith: Optional[str] = None) -> str:
    if explicit_faith:
        f = explicit_faith.lower()
        if "hindu" in f or "sanatan" in f or "vedic" in f: return "hindu"
        if "muslim" in f or "islam" in f: return "muslim"
        if "christ" in f: return "christian"
        if "sikh" in f: return "sikh"
        if "jain" in f: return "jain"
        if "secular" in f or "universal" in f: return "universal"

    nl = name.lower()
    words = set(re.findall(r'[a-z]+', nl))

    # Muslim names indicators (require whole word match or strong prefix)
    muslim_prefixes = ("mohd", "md", "syed", "sheikh", "abdul", "mohammed", "ahmad")
    muslim_words = {"khan", "ali", "ahmed", "hussain", "malik", "fatima", "zainab", "begum", "ansari", "shaikh", "qureshi", "rahman", "tariq", "salman", "zaheer", "farhan", "arshad"}
    if any(nl.startswith(prefix) for prefix in muslim_prefixes) or bool(words & muslim_words):
        return "muslim"

    # Christian names indicators (whole words only)
    christian_words = {"john", "joseph", "peter", "david", "mary", "fernandes", "dsouza", "pereira", "thomas", "mathew", "george", "rodrigues", "pinto", "paul", "michael", "lisa", "sarah", "james", "robert"}
    if bool(words & christian_words):
        return "christian"

    # Sikh names indicators
    if "singh" in words or "kaur" in words:
        sikh_first_names = {"gurpreet", "harpreet", "jaspreet", "manpreet", "amrit", "kuldeep", "daljit", "balwinder"}
        if bool(words & sikh_first_names):
            return "sikh"

    # Jain names indicators
    jain_words = {"jain", "shah", "mehta", "doshi"}
    if bool(words & jain_words) and not bool(words & {"singh", "sharma", "verma", "gupta"}):
        return "jain"

    # Default to Hindu / Sanatan for traditional Indian names, or universal if neutral
    return "hindu"

# ── Multi-Astrology Correlation Model ─────────────────────────────────────────
def calculate_multi_astrology_correlation(driver: int, conductor: int, personal_year: int) -> Dict[str, Any]:
    # KP Astrology logic:
    # 2, 6, 10, 11 significators for material/career success; 2, 7, 11 for marriage
    # High synergy when conductor is friendly to driver
    friendly_matrix = {
        1: [1, 2, 3, 5, 9],
        2: [1, 2, 3, 5],
        3: [1, 2, 3, 5, 9],
        4: [1, 5, 6, 7, 8],
        5: [1, 2, 3, 5, 6],
        6: [1, 4, 5, 6, 7],
        7: [1, 4, 5, 6, 7],
        8: [3, 5, 6, 7],
        9: [1, 2, 3, 5]
    }
    is_favorable = conductor in friendly_matrix.get(driver, [1, 5])
    
    kp_pct = 92 if is_favorable else 82
    bnn_pct = 90 if personal_year in (1, 3, 5, 6, 8) else 80
    vedic_pct = 88 if driver in (1, 3, 5, 9) else 84
    lal_kitab_pct = 86

    overall_consensus = round((kp_pct + bnn_pct + vedic_pct + lal_kitab_pct) / 4)

    return {
        "consensus_score_pct": overall_consensus,
        "kp_astrology": {
            "status": "CORROBORATED" if is_favorable else "COMPLEMENTARY_TENSION",
            "cuspal_note": "10th/11th Cuspal sub-lord corroborates structural progress with methodical discipline."
        },
        "bnn_nadi": {
            "status": "ALIGNED",
            "transit_note": f"Jupiter & Saturn transit rays support long-term compounding during Personal Year {personal_year}."
        },
        "vedic_astrology": {
            "status": "VALIDATED",
            "planetary_note": f"Natural karakas of Driver {driver} and Conductor {conductor} maintain active governance."
        },
        "lal_kitab": {
            "status": "STABILIZED",
            "karmic_note": "Lifestyle precautions safeguard against sudden expenditure or friction."
        }
    }

# ── Master Synthesizer Engine ─────────────────────────────────────────────────
class CharmOracleSynthesizer:
    def synthesize_consultation(
        self,
        name: str,
        day: int,
        month: int,
        year: int,
        question: str,
        is_premium: bool = False,
        explicit_faith: Optional[str] = None,
        event_family: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes complete multi-dimensional synthesis across all 18 classical parameters.
        """
        raw_name = (name or "").strip()
        if raw_name.lower() == "seeker":
            raw_name = ""
        user_name = raw_name
        first_name = user_name.split()[0].capitalize() if user_name else ""
        clean_q = (question or "").strip()
        ql = clean_q.lower()

        # 1. Deterministic Core Numbers (Caller validates DOB; clamp safely without hardcoded profile dates)
        d_val = max(1, min(31, int(day or 1)))
        m_val = max(1, min(12, int(month or 1)))
        y_val = max(1900, min(2100, int(year or 2000)))

        driver = reduce_digit(d_val)
        conductor = reduce_digit(d_val + m_val + y_val)
        driver_base = _base_1_to_9(driver)
        conductor_base = _base_1_to_9(conductor)
        
        current_year = datetime.now().year
        personal_year = _base_1_to_9(reduce_digit(d_val + m_val + current_year))

        is_karmic_debt = d_val in (13, 14, 16, 19)
        karmic_number = d_val if is_karmic_debt else None
        
        is_master_day = d_val in (11, 22)
        is_master_path = conductor in (11, 22, 33)

        # Name vibration
        chaldean_compound, chaldean_single = calculate_chaldean_name(user_name)
        name_harmonic = chaldean_single in (driver_base, conductor_base) or chaldean_single in (1, 3, 5, 6)

        # 2. Lo Shu Grid Construction & Digit Repetition Degree (Numeros Vision Classical Methodology Slide 4)
        dob_str = f"{d_val:02d}{m_val:02d}{y_val}"
        digit_counts = {i: 0 for i in range(1, 10)}
        for ch in dob_str:
            if ch != '0':
                digit_counts[int(ch)] += 1

        degrees_analysis = {}
        for num in range(1, 10):
            cnt = digit_counts[num]
            degrees_analysis[num] = classify_digit_degree(num, cnt)

        missing_numbers = [num for num, cnt in digit_counts.items() if cnt == 0]
        present_numbers = [num for num, cnt in digit_counts.items() if cnt > 0]
        pair_numbers = [num for num, cnt in digit_counts.items() if cnt == 2]
        under_numbers = [num for num, cnt in digit_counts.items() if cnt == 1]
        aggressive_numbers = [num for num, cnt in digit_counts.items() if cnt >= 3]

        # Planes & Yogas
        active_planes = []
        for plane in LO_SHU_PLANES:
            if all(digit_counts[num] > 0 for num in plane["nums"]):
                active_planes.append(plane)

        # 3. Topic Classification across 16 Specific Syllabus Domains
        topic_key, topic_label = self._classify_topic(ql, event_family=event_family)

        # 4. Faith & Cultural Detection
        faith = detect_faith_and_tradition(user_name, explicit_faith)

        # 5. Master Engines Calculations
        dc_81 = lookup_driver_conductor_81(driver_base, conductor_base)
        poorak_data = calculate_complementary_poorak(driver_base, conductor_base, missing_numbers)
        hygiene_items = diagnose_user_elemental_hygiene(present_numbers, missing_numbers)
        subdate_entry = BIRTH_DAY_SUBDATE_REGISTRY.get(d_val, {})
        astro_corr = calculate_multi_astrology_correlation(driver_base, conductor_base, personal_year)

        # 6. Build Humanized Master Consultation Dialogue
        consultation_dialogue = self._build_dialogue(
            first_name=first_name,
            birth_day=d_val,
            birth_month=m_val,
            birth_year=y_val,
            driver=driver,
            conductor=conductor,
            personal_year=personal_year,
            current_year=current_year,
            topic_key=topic_key,
            topic_label=topic_label,
            clean_q=clean_q,
            degrees_analysis=degrees_analysis,
            missing_numbers=missing_numbers,
            present_numbers=present_numbers,
            pair_numbers=pair_numbers,
            aggressive_numbers=aggressive_numbers,
            active_planes=active_planes,
            name_harmonic=name_harmonic,
            chaldean_compound=chaldean_compound,
            karmic_number=karmic_number,
            faith=faith,
            astro_corr=astro_corr,
            is_premium=is_premium,
            dc_81=dc_81,
            poorak_data=poorak_data,
            hygiene_items=hygiene_items,
            subdate_entry=subdate_entry
        )

        # Inject structured engine artifacts for O(1) downstream consumption
        consultation_dialogue["subdate_details"] = subdate_entry
        consultation_dialogue["dc_81_synergy"] = dc_81
        consultation_dialogue["poorak_data"] = poorak_data
        consultation_dialogue["elemental_hygiene"] = hygiene_items

        return consultation_dialogue

    def _classify_topic(self, ql: str, event_family: Optional[str] = None) -> Tuple[str, str]:
        fam = (event_family or "").strip().lower()
        if fam == "love":
            return "love_romance", "Love, Romance & Relationship Harmony"
        if fam == "marriage":
            if _has_word(ql, ["partner match", "matching", "compatibility", "gun milan", "kundali match", "partner compatibility"]):
                return "partner_matching", "Marriage Compatibility & Partner Alignment"
            return "marriage_union", "Marriage Timing & Spousal Harmony"
        if fam == "career":
            if _has_word(ql, ["business", "partnership", "startup", "venture", "firm", "founder", "freelance", "own company", "commercial"]):
                return "business_partnerships", "Business Alignment, Contracts & Partnerships"
            if _has_word(ql, ["stuck", "blocked", "lost opportunity", "lost job", "struggling in job", "delay in job", "career reset", "layoff"]):
                return "career_stuck", "Career Reset, Pacing & Practical Outreach"
            return "career_growth", "Career Direction, Promotion & Leadership"
        if fam in ("money", "wealth"):
            if _has_word(ql, ["share market", "stocks", "stock market", "trading", "mutual fund", "equity"]):
                return "share_market", "Long-Term Investment Discipline & Risk Pacing"
            return "wealth_finances", "Money Management, Debt Relief & Steady Savings"
        if fam in ("health_of_routine", "health"):
            return "health_of_routine", "Daily Routine, Sleep Rhythm & Energy Habits"
        if fam == "children":
            if _has_word(ql, ["conceive", "conception", "progeny", "santan", "pregnant", "pregnancy", "baby birth", "fertility", "have a baby", "baby name"]):
                return "child_conception", "Children, Family Readiness & Naming Alignment"
            return "child_studies", "Children, Parenting Warmth & Study Focus"
        if fam == "property":
            return "property_vastu", "Property, Home Address & Vastu Alignment"

        # Universal Obstacles
        if _has_word(ql, ["stuck everywhere", "blocked everywhere", "universal obstacle", "karmic block", "nothing working", "stuck in life", "problems everywhere"]) or \
           ("obstacle" in ql and _has_word(ql, ["everywhere", "all areas", "in everything"])) or \
           (_has_word(ql, ["wealth"]) and _has_word(ql, ["career"]) and _has_word(ql, ["marriage", "love"])):
            return "universal_obstacles", "Multi-Area Reset & Practical Grounding"

        # Children, Parenting, Conception & Studies
        if _has_word(ql, ["conceive", "conception", "progeny", "santan", "pregnant", "pregnancy", "baby birth", "fertility", "have a baby", "baby name"]):
            return "child_conception", "Children, Family Readiness & Naming Alignment"

        if _has_word(ql, ["child studies", "teen career", "studies", "exam", "education", "school", "college", "marks", "focus in study", "my child", "our child", "my son", "my daughter", "my kids", "parenting", "children"]):
            return "child_studies", "Children, Parenting Warmth & Study Focus"

        # Property, Home, Vehicle & Vastu (whole-word matching so 'car' never matches 'career')
        if _has_word(ql, ["property", "house", "home", "flat", "apartment", "plot", "land", "real estate", "makan", "zameen", "ghar", "vastu", "vehicle", "car", "relocation", "buy a home", "buy a house", "buy a flat", "address"]):
            return "property_vastu", "Property, Home Address & Vastu Alignment"

        # Partner Matching & Marriage Union (Distinct from Love/Dating)
        if _has_word(ql, ["partner match", "matching", "compatibility", "gun milan", "kundali match", "should i marry", "partner compatibility"]):
            return "partner_matching", "Marriage Compatibility & Partner Alignment"

        if _has_word(ql, ["marriage", "marry", "married", "husband", "wife", "spouse", "shaadi", "vivah", "wedding", "divorce", "marital", "engagement", "kundali", "matrimony"]):
            return "marriage_union", "Marriage Timing & Spousal Harmony"

        # Love, Romance & Dating
        if _has_word(ql, ["love", "romance", "romantic", "dating", "boyfriend", "girlfriend", "crush", "affection", "relationship", "partner", "breakup", "heartbreak", "soulmate"]):
            return "love_romance", "Love, Romance & Relationship Harmony"

        # Share Market & Savings Allocation
        if _has_word(ql, ["share market", "stocks", "stock market", "trading", "mutual fund", "equity"]):
            return "share_market", "Long-Term Investment Discipline & Risk Pacing"

        # Wealth, Money & Debt
        if _has_word(ql, ["money", "wealth", "finance", "financial", "debt", "loan", "bankrupt", "income", "salary", "savings", "budget", "expenses", "cashflow", "paisa", "dhan", "trapped money"]):
            return "wealth_finances", "Money Management, Debt Relief & Steady Savings"

        # Business & Partnerships
        if _has_word(ql, ["business", "partnership", "startup", "venture", "firm", "founder", "freelance", "own company", "commercial"]):
            return "business_partnerships", "Business Alignment, Contracts & Partnerships"

        # Career Stuck & Job Reset
        if _has_word(ql, ["stuck", "blocked", "lost opportunity", "lost job", "struggling in job", "delay in job", "career reset", "layoff"]):
            return "career_stuck", "Career Reset, Pacing & Practical Outreach"

        # Career Growth & Promotion
        if _has_word(ql, ["promotion", "growth", "new job", "senior role", "interview", "salary hike", "appraisal", "career", "job", "office", "role", "leadership", "profession", "work"]):
            return "career_growth", "Career Direction, Promotion & Leadership"

        # Daily Routine, Sleep & Non-Medical Energy Habits
        if _has_word(ql, ["routine", "habit", "habits", "health", "vitality", "wellness", "stress", "sleep", "fatigue", "burnout", "energy", "rest", "morning", "schedule", "circadian"]):
            return "health_of_routine", "Daily Routine, Sleep Rhythm & Energy Habits"

        # Foreign Travel & Relocation
        if _has_word(ql, ["foreign", "abroad", "visa", "overseas", "permanent residency", "settlement"]):
            return "foreign_relocation", "Relocation & Cross-Border Transition Timing"

        # Missing Numbers & Lo Shu Grid
        if _has_word(ql, ["missing number", "missing numbers", "lo shu grid", "elements", "loshu"]):
            return "missing_numbers", "Lo Shu Grid (Lo Shu Square) & Elemental Balance"

        # Repetition Degrees
        if _has_word(ql, ["repetitive", "repeat", "multiple times", "degree", "power of numbers"]):
            return "repetition_degree", "Repeated Digits & Balanced Expression"

        # Name Balancing
        if _has_word(ql, ["name spelling", "name balance", "change name", "chaldean name", "name harmony"]):
            return "name_balancing", "Calling Name Number & Chaldean Spelling Balance"

        # Default General Destiny
        return "general_destiny", "Personal Year Cycle & Core Numerology Overview"

    def _build_dialogue(
        self,
        first_name: str,
        birth_day: int,
        birth_month: int,
        birth_year: int,
        driver: int,
        conductor: int,
        personal_year: int,
        current_year: int,
        topic_key: str,
        topic_label: str,
        clean_q: str,
        degrees_analysis: Dict[int, Any],
        missing_numbers: List[int],
        present_numbers: List[int],
        pair_numbers: List[int],
        aggressive_numbers: List[int],
        active_planes: List[Dict[str, Any]],
        name_harmonic: bool,
        chaldean_compound: int,
        karmic_number: Optional[int],
        faith: str,
        astro_corr: Dict[str, Any],
        is_premium: bool,
        dc_81: Optional[Dict[str, Any]] = None,
        poorak_data: Optional[Dict[str, Any]] = None,
        hygiene_items: Optional[List[Dict[str, Any]]] = None,
        subdate_entry: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Creates authentic, deeply personalized, humanized numerology consultation.
        """
        d_base = _base_1_to_9(driver)
        c_base = _base_1_to_9(conductor)
        d_p = PLANETARY_INFO[d_base]["planet"]
        c_p = PLANETARY_INFO[c_base]["planet"]
        sub = subdate_entry or {}
        dc = dc_81 or {}
        poorak = poorak_data or {}
        hygiene = hygiene_items or []
        
        # Determine acute timing window for current cycle using deterministic Dasha & transit engine
        from app.charm.numerology.dasha_engine import NumerologyDashaEngine
        from app.engine.lunar_paksha_engine import calculate_shukla_paksha_timing
        from datetime import timedelta

        timing_window_str = ""
        try:
            d_engine = NumerologyDashaEngine()
            d_res = d_engine.evaluate_dasha_hierarchy(
                day=birth_day,
                month=birth_month,
                year=birth_year,
                target_date=datetime.now().date()
            )
            if d_res.primary_windows:
                p_win = d_res.primary_windows[0]
                t_today = datetime.now().date()
                w_start = p_win.start
                w_end = p_win.end
                if w_end <= w_start or w_end < t_today.isoformat():
                    w_start = t_today.isoformat()
                    w_end = (t_today + timedelta(days=90)).isoformat()
                timing_window_str = f"**{w_start}** to **{w_end}**"
        except Exception:
            pass

        if not timing_window_str:
            t_today = datetime.now().date()
            timing_window_str = f"**{t_today.isoformat()}** to **{(t_today + timedelta(days=90)).isoformat()}**"

        # Sacred Remedial Muhurta: Always begin remedies, gems, and mantras during Shukla Paksha
        shukla_info = calculate_shukla_paksha_timing(ruling_planet_num=d_base)
        shukla_guidance = shukla_info["guidance_narrative"]

        # ── 1. Topic-Specific Diagnostic Insight ──
        if topic_key == "love_romance":
            diagnosis_text = (
                f"In romantic connection and emotional bonding, your birth matrix pairs Mulank (Birth Day number) {driver} ({d_p}) "
                f"with Bhagyank (Life Path number) {conductor} ({c_p}). Mulank {driver} shapes how you express affection and listen ({NUMBER_DUAL_ATTRIBUTES[d_base]['good']}), "
                f"while Bhagyank {conductor} reflects what helps long-term emotional trust feel steady. "
            )
            if 2 in missing_numbers:
                diagnosis_text += "Because **Number 2 (Moon — Emotional Sensitivity)** is open in your Lo Shu Grid, romantic misunderstandings often arise when feelings are assumed rather than spoken gently. "
            elif 6 in pair_numbers:
                diagnosis_text += "With **Number 6 (Venus — Affection & Warmth)** balanced as a pair in your grid, you naturally create warmth, loyalty, and steady care in relationships. "
            core_advice = (
                f"During **Personal Year {personal_year}** (active window {timing_window_str}), romantic clarity improves through unhurried, honest conversation rather than rushing commitments under pressure."
            )
            practical_steps = [
                "Set aside one unhurried, screen-free conversation each week to share expectations openly and listen without interrupting.",
                "Notice whether you are matching actions with words before making major relationship promises.",
                "Keep evenings calm and uncluttered so emotional conversations happen when both people are rested."
            ]

        elif topic_key in ("marriage_union", "partner_matching"):
            diagnosis_text = (
                f"For marriage timing and spousal harmony, your chart pairs Mulank (Birth Day number) {driver} ({d_p}) "
                f"with Bhagyank (Life Path number) {conductor} ({c_p}). Mulank {driver} governs day-to-day domestic communication ({NUMBER_DUAL_ATTRIBUTES[d_base]['good']}), "
                f"while Bhagyank {conductor} shapes shared household responsibility and long-term partnership rhythm. "
            )
            if 6 in missing_numbers:
                diagnosis_text += "**Number 6 (Venus — Home & Spousal Harmony)** is open in your Lo Shu Grid, suggesting marriage decisions benefit from explicit alignment on family routines, finances, and mutual expectations beforehand. "
            elif 6 in pair_numbers:
                diagnosis_text += "Your grid holds **Number 6 as a balanced Pair**, supporting domestic loyalty, shared hospitality, and steady marital companionship. "
            core_advice = (
                f"Within **Personal Year {personal_year}**, your supportive Dasha window for marriage discussions and family alignment spans {timing_window_str}."
            )
            practical_steps = [
                "Discuss shared household priorities—living arrangements, finances, and family boundaries—calmly before fixing milestone dates.",
                "Schedule a weekly 30-minute spousal or partner check-in focused on practical mutual support rather than past grievances.",
                "Keep the South-West corner of your living or sleeping space tidy, warm, and free of work clutter."
            ]

        elif topic_key in ("career_growth", "career_stuck"):
            diagnosis_text = (
                f"Your professional blueprint combines the pioneering executive drive of Driver {driver} ({d_p}) "
                f"with the overarching karmic trajectory of Conductor {conductor} ({c_p}). "
                f"You are naturally wired for {NUMBER_DUAL_ATTRIBUTES[d_base]['attribute']}. "
            )
            if topic_key == "career_stuck":
                diagnosis_text += (
                    f"Please remember: feeling paused or sensing delayed recognition in 2026 is **not a personal failure**; "
                    f"it is a structural transit pause. Currently, you are traversing **Personal Year {personal_year}**, "
                    f"which acts as a celestial filter testing your operational foundations so you step into authentic, unshakeable authority rather than a fragile compromise."
                )
            else:
                diagnosis_text += (
                    f"In 2026, navigating **Personal Year {personal_year}**, your career momentum is actively preparing for an upward breakthrough. "
                    f"Your natural superpowers shine brightest when you operate with strategic autonomy rather than passive waiting."
                )

            if 1 in pair_numbers:
                diagnosis_text += " Your birth grid features **Number 1 as a balanced Pair**, confirming natural executive command and clear verbal authority when you back yourself. "
            elif 8 in aggressive_numbers:
                diagnosis_text += " With **Number 8 present 3 or more times**, Saturn's compounding power is intense—you will achieve great institutional scale, but early career milestones demand extraordinary perseverance before unlocking sudden massive rewards. "

            core_advice = (
                f"Your strongest acute breakthrough window runs from {timing_window_str}. "
                f"Use this preparatory phase to document your quantifiable business accomplishments, streamline your executive pitch, "
                f"and reach out directly to key industry decision-makers."
            )
            practical_steps = [
                "Document 3 quantifiable business achievements in clear metrics and update your professional summary.",
                "Conduct a 3-touchpoint outreach: message 3 former mentors or trusted executive contacts with a brief, value-focused note.",
                "Position your desk facing East or North while making high-stakes calls to harness solar clarity."
            ]

        elif topic_key in ("wealth_finances", "share_market"):
            diagnosis_text = (
                f"Your financial engine is anchored by Driver {driver} and Conductor {conductor}. "
                f"In classical Sankhya Shastra, wealth generation requires harmony between Number 1 (Initiative), Number 5 (Commercial Speed), and Number 8 (Compounding Stability). "
            )
            if 8 in missing_numbers:
                diagnosis_text += "Notice that **Number 8 (Saturn - Finance & Long-term Compounding)** is absent from your birth grid. This creates an energetic pattern where money flows in steadily, but financial leaks, impulsive expenditures, or lending to unreliable peers drains compounding savings unless strictly budgeted. "
            elif 8 in pair_numbers:
                diagnosis_text += "You possess **Number 8 in an auspicious Pair (Two Times)**, which Numeros Vision Classical Methodology identifies as the optimal wealth balance—bringing disciplined money management, enduring investments, and resilience through market cycles. "

            if topic_key == "share_market":
                diagnosis_text += (
                    "Regarding speculative equity or share trading: speculative success requires a strong 5 (Mercury - Market Wit) and 4 (Rahu - Sudden Insight). "
                    + ("Since you have Number 5 active, swift market adaptability supports structured swing trading, provided you avoid reckless intraday leverage." if 5 in present_numbers else "Since Number 5 is missing, pure speculative day-trading carries erratic volatility; you will build far greater enduring wealth through long-term index compounding, real estate, and blue-chip holdings.")
                )

            core_advice = (
                f"During **Personal Year {personal_year}**, focus on plugging silent monthly capital leaks and avoiding emotional debt guarantees. "
                f"Your numbers favor disciplined, compounding wealth accumulation over get-rich-quick gambles."
            )
            practical_steps = [
                "Conduct a ruthless audit of all recurring subscriptions and automated debits to eliminate hidden financial leakage.",
                "Never lend money on Saturdays or sign financial loan guarantees under emotional pressure.",
                "Keep your financial documents and primary cash ledger in the North or North-East sector of your home."
            ]

        elif topic_key in ("child_conception", "child_studies"):
            if topic_key == "child_conception":
                diagnosis_text = (
                    f"Child conception and progeny blessings in Vedic Numerology are governed by Number 2 (Chandra - Receptive Womb & Fluid Harmony), "
                    f"Number 3 (Guru/Jupiter - Divine Expansion & Seed Multiplication), and Number 6 (Venus - Vital Reproductive Fluid & Domestic Grace). "
                    f"Looking at your numbers (Driver {driver}, Conductor {conductor}): your cycle in Personal Year {personal_year} brings natural creative renewal. "
                )
                if 3 in missing_numbers or 2 in missing_numbers:
                    diagnosis_text += "With elemental wood (3) or lunar earth (2) in need of balancing in your grid, conception timing benefits greatly from conscious nervous system calming, eliminating chronic workplace stress, and aligning with fertile celestial lunar cycles. "
                core_advice = (
                    f"The most auspicious fertile window for divine progeny acceleration aligns between {timing_window_str}. "
                    f"Keep physical health, calm mental states, and spiritual harmony as your central daily focus."
                )
                practical_steps = [
                    "Maintain gentle, nourishing routines: consume warm soaked almonds and water stored in silver/copper vessels.",
                    "Spend 15 minutes each evening in quiet grounding with your spouse, free from digital screens and work stress."
                ]
            else:
                diagnosis_text = (
                    f"For academic focus, memory, and youth career direction: Number 3 (Jupiter - Wisdom & Retention), Number 5 (Mercury - Rapid Learning & Logic), "
                    f"and Number 4 (Rahu - Systemic Discipline) govern student success. "
                    f"Your child's chart reveals strong natural intelligence, but depending on the presence of Number 5 and 3, learning accelerates through interactive, visual methods rather than rigid rote memorization."
                )
                core_advice = "Create an organized, clutter-free study corner facing East or North-East to maximize concentration and memory retention."
                practical_steps = [
                    "Place the study desk facing North-East with a soft warm reading light to promote intellectual tranquility.",
                    "Break study intervals into focused 25-minute sprints followed by 5 minutes of mindful stretching."
                ]

        elif topic_key in ("business_partnerships",):
            diagnosis_text = (
                f"Entrepreneurial success and commercial expansion demand a dynamic synthesis of Driver {driver} ({d_p}) executive authority "
                f"and Conductor {conductor} ({c_p}) market reputation. "
            )
            if 5 in missing_numbers:
                diagnosis_text += "Because **Number 5 (Mercury - The Master Key of Commercial Balance)** is missing from your birth grid, running solo business operations can occasionally feel overwhelming or suffer from inconsistent client communication. You benefit immensely from partnering with an operationally agile, detail-oriented collaborator. "
            elif 5 in present_numbers:
                diagnosis_text += "With **Number 5 present in your grid**, you have natural commercial intuition, market networking ability, and the flexibility to pivot offerings to meet customer demand. "

            core_advice = (
                f"In 2026, traversing **Personal Year {personal_year}**, business initiatives thrive when backed by written legal contracts, clear partnership equity terms, and strong ethical governance. "
                f"Your most auspicious commercial launch and client expansion window unfolds from {timing_window_str}."
            )
            practical_steps = [
                "Ensure all business partnership terms, IP ownership, and profit splits are documented in formal written agreements.",
                "Focus marketing outreach on your top 20% highest-margin clients rather than spreading energy across unprofitable low-ticket offers.",
                "Place a healthy indoor green plant or green aventurine cluster on the North side of your business desk."
            ]

        elif topic_key in ("universal_obstacles",):
            greeting_inline = f"Namaste {first_name}" if first_name else "Namaste"
            diagnosis_text = (
                f"{greeting_inline} 🙏 Take a deep, reassuring breath. When obstacles seem to appear on all sides—in career, money, and personal peace—"
                f"it feels exhausting, but in authentic occult numerology, this is the classic signature of **Karmic Boundary Recalibration**. "
                f"Combining Driver {driver} ({d_p}) and Conductor {conductor} ({c_p}) in Personal Year {personal_year}: "
                f"your soul has outgrown old compromises. The friction you are experiencing is your planetary cycles forcefully shutting doors to outmoded, draining paths "
                f"so you can step into an unshakeable, higher tier of life."
            )
            if karmic_number:
                diagnosis_text += f" Moreover, your birth date carries **Karmic Debt Number {karmic_number}**, which indicates past-cycle lessons around patience, discipline, and emotional sovereignty that are reaching their final purification."
            core_advice = (
                f"The celestial turning point arrives between {timing_window_str}. "
                f"Stop fighting the current by making desperate moves. Instead, ground your energy, eliminate toxic draining habits, "
                f"and focus on simple, consistent daily spiritual and physical alignments."
            )
            practical_steps = [
                "Practice a strict 7-day energetic fast: avoid heated arguments, refrain from complaining about delays, and drink water from a copper vessel.",
                "Declutter your sleeping space: remove broken items, electronic clutter, and old unused shoes to clear heavy stagnant vibrations.",
                "Feed stray animals, birds, or cows once weekly on Saturday morning to neutralize heavy karmic friction."
            ]

        elif topic_key == "property_vastu":
            has_silver_plane = all(n in present_numbers for n in (2, 5, 8))
            diagnosis_text = (
                f"For property, home address, and Vastu alignment, classical Lo Shu analysis examines the Earth axis **2–5–8** alongside Mulank {driver} ({d_p}) and Bhagyank {conductor} ({c_p}). "
                + ("Your birth grid activates the **2–5–8 Earth Plane**, supporting steady real-estate planning and grounded household stability. "
                   if has_silver_plane else
                   "Because one or more Earth digits (**2, 5, or 8**) are open in your Lo Shu Grid, property purchases and moves go smoothest when backed by unhurried title verification and conservative EMI planning. ")
            )
            core_advice = (
                f"In **Personal Year {personal_year}**, your supportive Dasha window for shortlisting homes, checking flat/plot digits, or planning a move runs from {timing_window_str}."
            )
            practical_steps = [
                "Verify title deeds, RERA registration, and total monthly outgoings independently before paying any booking token.",
                "Check how a candidate flat or house number reduces to a single digit alongside Mulank " + str(driver) + " and Bhagyank " + str(conductor) + ".",
                "Keep the North-East and central area of your home bright, ventilated, and uncluttered."
            ]

        elif topic_key == "health_of_routine":
            diagnosis_text = (
                f"From a strictly non-medical daily-routine perspective, Mulank {driver} ({d_p}) and Bhagyank {conductor} ({c_p}) highlight how you pace work, rest, and focus. "
                f"(Note: Charm AI offers lifestyle rhythm suggestions only, never medical diagnosis or clinical advice.) "
                + ("With **Number 5 (Mercury — Central Balance)** open in your grid, irregular meal or sleep times quickly create mental fatigue. "
                   if 5 in missing_numbers else
                   "Your grid supports steady daily rhythm once waking, hydration, and screen cutoffs are kept consistent. ")
            )
            core_advice = (
                f"During **Personal Year {personal_year}** ({timing_window_str}), small, repeatable daily habits outperform intense short-lived overhauls."
            )
            practical_steps = [
                "Anchor a fixed wake-up time and get 10–15 minutes of natural morning daylight before checking messages.",
                "Use 45-minute focused work blocks followed by a 5-minute standing or hydration break.",
                "Switch off bright work screens 45 minutes before sleep to let mental restlessness settle."
            ]

        else: # general_destiny, foreign_relocation, missing_numbers, repetition_degree, name_balancing
            diagnosis_text = (
                f"Your core cosmic matrix combines **Driver {driver} ({d_p})** with **Conductor {conductor} ({c_p})**. "
                f"Driver {driver} represents your inborn decision temperament ({NUMBER_DUAL_ATTRIBUTES[d_base]['attribute']}), "
                f"while Conductor {conductor} guides your overarching life lessons and ultimate destination. "
                f"Currently in 2026, your cycle is energized by **Personal Year {personal_year}**, setting a pivotal stage for milestone transitions."
            )
            if active_planes:
                plane_names = [p["name"] for p in active_planes]
                diagnosis_text += f" Your Lo Shu Grid displays active harmonic presence in the **{' & '.join(plane_names)}**, providing you with exceptional foundational gifts ({active_planes[0]['gift']})."
            
            core_advice = (
                f"Your acute planetary window of alignment spans {timing_window_str}. "
                f"Aligning your daily habits, workspace direction, and ethical choices with this timing unlocks clear, friction-free momentum."
            )
            practical_steps = [
                f"Wear or surround yourself with your auspicious planetary colors: {self._get_favourable_colors(d_base)}.",
                f"Schedule major decisions and high-stakes conversations on your power day: {self._get_favourable_day(d_base)}.",
                "Align your working desk facing North or East to channel focused solar and commercial mental clarity."
            ]

        # ── 1.1 Inborn Character & Natural Alignment ──
        sub_arch = sub.get("archetype", "The Radiant Builder")
        sub_comp = sub.get("planetary_composition", f"Day {birth_day}")
        
        # Clean up subdate archetype and composition for conversational warmth
        clean_comp = re.sub(r'\(.*?Clash.*?\)', '', sub_comp).strip()
        if not clean_comp:
            clean_comp = f"Day {birth_day}"

        dc_pos = ", ".join(dc.get("positive_traits", [])[:3]) or "Clear decision-making, strategic vision, perseverance"
        dc_careers = ", ".join(dc.get("recommended_careers", [])[:3]) or "Leadership, Administration & Strategic Planning"

        poorak_num = poorak.get("poorak_number", 5)
        poorak_planet = poorak.get("poorak_planet", "Mercury")
        poorak_role = poorak.get("rationale", "")
        clean_poorak_role = poorak_role.replace("fills the central Earth anchor of your Lo Shu Grid, providing unshakable emotional stability", "provides steady grounding, mental flexibility, and ease of communication")

        # Repetition & Grid Balance Focus
        balance_focus = []
        if pair_numbers:
            balance_focus.append(f"Balanced Strengths: Number {', '.join(str(n) for n in pair_numbers)} (Steady harmony and focused flow)")
        if 5 in missing_numbers or 6 in missing_numbers:
            missing_names = []
            if 5 in missing_numbers: missing_names.append("Number 5 (Flexibility & Pacing)")
            if 6 in missing_numbers: missing_names.append("Number 6 (Harmony & Renewal)")
            balance_focus.append(f"Mindful Cultivation: {' & '.join(missing_names)} through calm daily habits")
        grid_balance_text = " | ".join(balance_focus) if balance_focus else "Your birth grid maintains an even, balanced distribution."

        # Gentle Daily Habits for Elemental Well-Being
        hygiene_list = hygiene.get("prescriptions", []) if isinstance(hygiene, dict) else (hygiene or [])
        hygiene_bullets = []
        for h in hygiene_list[:3]:
            elem = h.get('element', 'Earth')
            instr = h.get('instruction', '')
            instr_clean = instr.replace('Must touch physical skin continuously', 'Wear natural materials touching skin for grounding').replace('strictly avoid', 'mindfully balance')
            hygiene_bullets.append(f"  • **{elem} Alignment:** {h.get('prescription', '')} — *{instr_clean}*")
        hygiene_str = "\n".join(hygiene_bullets) if hygiene_bullets else "  • **Foundational Grounding:** Keep a natural wooden or clear quartz accessory nearby to stay centered during demanding days."

        # ── 2. Cultural & Faith-Tailored Remedial Alignment ──
        faith_remedy = self._get_faith_tailored_remedy(faith, driver, conductor, missing_numbers)

        # ── 3. Timing & Seasonal Context ──
        correlation_summary = (
            f"**Timing & Seasonal Context:**\n"
            f"Navigating Personal Year {personal_year} in 2026 creates favorable cyclical momentum for thoughtful planning and strategic progress. "
            f"Your active timing window ({timing_window_str}) particularly supports disciplined initiatives, professional outreach, and laying solid foundations for enduring success."
        )

        # ── 4. Humanized Birth Narrative (Zero Technical Jargon) ──
        birth_day_narrative = (
            sub.get("report_narrative") or
            sub.get("core_personality") or
            "You possess a natural gift for strategic foresight, personal resilience, and long-term mastery."
        )

        # Clean any stray internal calculation codes if present
        birth_day_narrative = re.sub(r'Category [A-D]|Graded Category|Intrinsic Potency|\d+%', '', birth_day_narrative).strip()
        birth_day_narrative = re.sub(r'\s{2,}', ' ', birth_day_narrative)

        # ── 5. Full Humanized Consultation Text ──
        steps_text = "\n".join(f"• **Step {i+1}:** {step}" for i, step in enumerate(practical_steps))
        greeting_header = f"Namaste {first_name} ✨" if first_name else "Namaste ✨"
        question_context_line = f"*Inquiry Focus: {clean_q}*\n\n" if clean_q else ""
        full_text = (
            f"{greeting_header}\n\n"
            f"{question_context_line}"
            f"**1. What Your Numbers Reveal About '{topic_label}':**\n"
            f"{diagnosis_text}\n\n"
            f"**2. Your Inborn Character & Life Dynamics:**\n"
            f"• **Born on Day {birth_day} • {sub_arch}:** {birth_day_narrative}\n"
            f"• **Inner Drive {driver} & Life Destiny {conductor}:** How your instinctive mindset meets your life path. Natural gifts include {dc_pos}. Thriving career paths often align with {dc_careers}.\n"
            f"• **Balancing Vibration (Number {poorak_num} • {poorak_planet}):** Acts as your natural harmonizing energy. {clean_poorak_role}\n"
            f"• **Elemental Balance Focus:** {grid_balance_text}\n\n"
            f"**3. Active Cycle & Timing Momentum:**\n"
            f"{core_advice}\n\n"
            f"**4. Practical Steps for Daily Progress:**\n"
            f"{steps_text}\n\n"
            f"**5. Natural Daily Rhythms & Elemental Well-Being:**\n"
            f"{hygiene_str}\n\n"
            f"**6. Daily Mindfulness & Centering ({faith.capitalize()} Tradition):**\n"
            f"{faith_remedy}\n\n"
            f"**7. Sacred Consecration Muhurta (Shukla Paksha Initiation Window):**\n"
            f"{shukla_guidance}\n\n"
            f"{correlation_summary}"
        )
        return {
            "status": "success",
            "topic_key": topic_key,
            "topic_display": topic_label,
            "driver": driver,
            "conductor": conductor,
            "personal_year": personal_year,
            "faith_detected": faith,
            "astro_consensus_pct": astro_corr["consensus_score_pct"],
            "timing_window": timing_window_str,
            "direct_answer": full_text,
            "humanized_consultation": full_text,
            "practical_actions": practical_steps,
            "faith_remedy": faith_remedy,
            "correlation_summary": correlation_summary,
            "shukla_paksha": shukla_info,
            "is_premium": is_premium
        }

    def _get_favourable_colors(self, num: int) -> str:
        color_map = {
            1: "Gold, Amber, Orange, Warm Yellow",
            2: "Pearl White, Cream, Silver, Light Grey",
            3: "Bright Yellow, Saffron, Amber, Gold",
            4: "Slate Blue, Electric Blue, Silver Grey",
            5: "Emerald Green, Turquoise, Fresh Mint",
            6: "Rose Pink, Cream White, Diamond White, Powder Blue",
            7: "Pastel Green, Light Grey, Lavender, White",
            8: "Dark Navy Blue, Charcoal Grey, Steel Grey",
            9: "Crimson Red, Coral, Warm Terracotta"
        }
        return color_map.get(_base_1_to_9(num), "Gold, White, Cream")

    def _get_favourable_day(self, num: int) -> str:
        day_map = {
            1: "Sunday", 2: "Monday", 3: "Thursday", 4: "Wednesday & Saturday",
            5: "Wednesday", 6: "Friday", 7: "Thursday & Monday", 8: "Saturday", 9: "Tuesday"
        }
        return day_map.get(_base_1_to_9(num), "Thursday & Sunday")

    def _get_faith_tailored_remedy(self, faith: str, driver: int, conductor: int, missing_nums: List[int]) -> str:
        d_base = _base_1_to_9(driver)
        d_p = PLANETARY_INFO[d_base]["planet"]

        if faith == "hindu":
            beej_mantras = {
                1: "Om Hram Hrim Hroum Sah Suryaya Namah (108 times at solar dawn with copper Arghya)",
                2: "Om Shram Shrim Shroum Sah Chandraya Namah (on Monday evenings, respect maternal figures)",
                3: "Om Gram Grim Groum Sah Gurave Namah (on Thursday midday, apply sandalwood tilak)",
                4: "Om Bhram Bhrim Bhroum Sah Rahave Namah (keep electricals clean, feed stray dogs on Saturday)",
                5: "Om Bram Brim Broum Sah Budhaya Namah (feed green fodder to cows on Wednesday, care for plants)",
                6: "Om Dram Drim Droum Sah Shukraya Namah (wear clean fragrant clothes on Friday, respect women)",
                7: "Om Sram Srim Sroum Sah Ketave Namah (feed sesame seeds or roti to black-and-white dogs)",
                8: "Om Pram Prim Proum Sah Shanaishcharaya Namah (light mustard oil lamp near Peepal on Saturday dusk)",
                9: "Om Kram Krim Kroum Sah Bhaumaya Namah (chant Hanuman Chalisa on Tuesday morning, physical exercise)"
            }
            return (
                f"• **Vedic Beej Mantra & Arghya:** Chant *{beej_mantras.get(d_base, beej_mantras[1])}*.\n"
                f"• **Elemental Balance:** Keep a natural brass or copper vessel in the North-East; offer pure water to the morning sun to vitalize your core {d_p} energy."
            )

        elif faith == "muslim":
            return (
                f"• **Sadaqah & Charitable Giving:** Practice voluntary Sadaqah on auspicious days ({self._get_favourable_day(d_base)}). Provide clean drinking water to travelers or feed birds and stray animals quietly without ostentation.\n"
                f"• **Elemental Harmonization:** Infuse your personal space with natural green plants and natural attar (pure non-alcoholic fragrance like rose or sandalwood) on Fridays to balance peaceful mental vibrations.\n"
                f"• **Contemplation:** Dedicate 10 minutes after morning prayers for quiet gratitude and reflection, facing East/North."
            )

        elif faith == "christian":
            return (
                f"• **Benevolent Almsgiving & Charity:** Donate warm meals, clean blankets, or school supplies to local children's homes or community shelters on {self._get_favourable_day(d_base)} mornings.\n"
                f"• **Contemplative Light:** Light a pure beeswax or white candle during morning personal prayer to invite divine clarity, focus, and peace.\n"
                f"• **Gratitude & Scripture:** Spend 10 minutes in morning contemplative scripture reflection and journaling your daily intentions."
            )

        elif faith == "sikh":
            return (
                f"• **Nishkam Seva:** Participate in voluntary Langar seva (cleaning, cooking, or serving water) at a Gurdwara on {self._get_favourable_day(driver)}.\n"
                f"• **Vand Chhako & Daan:** Share your earnings by feeding stray birds or helping someone in need with medicine or books.\n"
                f"• **Simran & Grounding:** Practice morning Naam Simran in a peaceful, naturally lit space facing East."
            )

        elif faith == "jain":
            return (
                f"• **Jiva Daya (Compassionate Protection):** Feed green grass to cows in a Gaushala or offer bird seeds and water on {self._get_favourable_day(driver)} mornings.\n"
                f"• **Ahimsa & Purity:** Practice mindful speech, avoid harsh criticism of peers, and wear serene white or natural cream cotton clothing on auspicious days.\n"
                f"• **Svadhyaya:** Spend 15 minutes in quiet self-study and meditation on universal equanimity (Samayika)."
            )

        else: # universal / secular
            return (
                f"• **Acoustic Solfeggio Therapy:** Listen to 528 Hz (Transformation & Solar Vitality) or 432 Hz (Emotional Equilibrium) soundscapes for 15 minutes each morning.\n"
                f"• **Circadian & Vastu Alignment:** Position your primary work desk facing North or East, and take a 10-minute walk under natural morning sunlight within 1 hour of waking.\n"
                f"• **Altruistic Micro-Acts:** Practice anonymous kindness once weekly on {self._get_favourable_day(driver)} by feeding birds or supporting an animal shelter."
            )

charm_oracle_synthesizer = CharmOracleSynthesizer()
