import os

def enrich_registry():
    path = os.path.join('app', 'engine', 'number_characteristics_registry.py')
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()

    # Find the start of BIRTH_DAY_SUBDATE_REGISTRY
    marker = '# ── DR. Numeros Vision Classical Methodology DAY 6 CANONICAL SUB-DATE & NUMBER CHARACTERISTICS ────'
    idx = text.find(marker)
    if idx == -1:
        print("Marker not found!")
        return

    base_code = text[:idx]

    enriched_registry_code = '''# ── DR. Numeros Vision Classical Methodology DAY 6 CANONICAL SUB-DATE & NUMBER CHARACTERISTICS ────
# Source: Master Numerology with Dr. Numeros Vision Classical Methodology - DAY 6 (Numeros Vision)
# Strength Categories:
#   Category A: Good Strength (High/Strongest Potency)
#   Category B: Normal Strength (Moderate / Balanced / Steady Potency)
#   Category C: Lower Strength (Challenging / Needs Remedial Support & Effort)
#   Category D: Karmic Debt (Intense Transformational Crucible)

STRENGTH_CATEGORY_DEFINITIONS = {
    "A": {
        "grade": "Category A",
        "title": "Good Strength (High Potency)",
        "badge_color": "#16835B",
        "description": "High planetary potency, active natural drive, and strong manifestation capability. Operates with direct momentum.",
        "guidance": "Channels commanding energy naturally. Balance with humility, patience, and collaborative listening to prevent ego friction."
    },
    "B": {
        "grade": "Category B",
        "title": "Normal Strength (Balanced Potency)",
        "badge_color": "#8B6914",
        "description": "Balanced, steady, and workable potency. Provides a reliable foundation that grows through regular routine.",
        "guidance": "Sustainable and stable. Steady compounding habits and clear focus allow you to achieve lasting milestones without erratic swings."
    },
    "C": {
        "grade": "Category C",
        "title": "Lower Strength (Requires Conscious Support)",
        "badge_color": "#7A654D",
        "description": "Lower initial potency or complex compound tension. Prone to early-life self-doubt, scattered energy, or friction.",
        "guidance": "Needs conscious remedial grounding and patience. Friction is not a roadblock; with structured lifestyle habits and elemental remedies, it builds deep resilience."
    },
    "D": {
        "grade": "Category D",
        "title": "Karmic Debt (Transformational Crucible)",
        "badge_color": "#523E28",
        "description": "Intense karmic testing. Demands hard labor, short-tempered patience, and structural reorganization.",
        "guidance": "Requires absolute discipline and ethical persistence. Overcoming early trials unlocks monumental, enduring achievements."
    }
}

BIRTH_DAY_SUBDATE_REGISTRY: Dict[int, Dict[str, Any]] = {
    # ── ROOT 1: SUN (SURYA) · King like, Authoritative, Pioneers, Royal, Trend setters, Leadership, Ego ──
    1: {
        "day": 1, "root": 1, "code": "1(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength",
        "planet": "Sun (Surya)", "is_karmic": False, "is_master": False,
        "keywords": ["King like", "Authoritative", "Pioneers", "Royal", "Trend setters", "Leadership", "Ego"],
        "essence": "Pure Solar vibration with balanced normal strength. Original creative pioneer, independent executive authority. Thrives when allowed to direct projects autonomously.",
        "humanized_reading": "Your birth day 1 grants you Category B (Normal Strength) solar energy: steady, natural leadership and sovereign self-respect. You lead best through practical example rather than forcing authority."
    },
    10: {
        "day": 10, "root": 1, "code": "10(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength (Karmic 10)",
        "planet": "Sun (Surya)", "is_karmic": True, "is_master": False,
        "keywords": ["King like", "Authoritative", "Pioneers", "Royal", "Trend setters", "Leadership", "Ego", "Karmic 10"],
        "essence": "Karmic Number 10 (Wheel of Fortune). Normal balanced solar strength amplified by Zero. Rises from grassroots to high executive authority; experiences cycles of sudden karmic elevation.",
        "humanized_reading": "Born on the 10th, you carry Category B (Normal Strength) with Karmic Number 10 resonance: you possess a natural royal aura and trend-setting instinct, rising through life's cyclical turns to claim honorable leadership."
    },
    19: {
        "day": 19, "root": 1, "code": "19(a)", "tier": "a",
        "strength_category": "A", "strength_title": "Category A — Good Strength (Karmic 19)",
        "planet": "Sun (Surya)", "is_karmic": True, "is_master": False,
        "keywords": ["King like", "Authoritative", "Pioneers", "Royal", "Trend setters", "Leadership", "Ego", "Karmic 19", "Alpha Power"],
        "essence": "Karmic Number 19 (Prince of Heaven). Sun (1) + Mars (9). Category A (Good Strength): supreme executive drive, fearless trendsetter, alpha leadership. Must temper fiery ego to sustain sovereign gains.",
        "humanized_reading": "Born on the 19th, you hold Category A (Good Strength) royal power: an intense combination of Sun and Mars giving you extraordinary executive ambition, pioneering courage, and sovereign authority."
    },
    28: {
        "day": 28, "root": 1, "code": "28(c)", "tier": "c",
        "strength_category": "C", "strength_title": "Category C — Lower Strength (Needs Patience)",
        "planet": "Sun (Surya)", "is_karmic": False, "is_master": False,
        "keywords": ["King like", "Authoritative", "Pioneers", "Royal", "Trend setters", "Leadership", "Ego", "Endurance"],
        "essence": "Moon (2) + Saturn (8) resolving into Sun (10=1). Category C (Lower Strength): early emotional friction and laborious struggle before solar authority blossoms. Endurance transforms early delays into lasting mastery.",
        "humanized_reading": "Born on the 28th, you operate under Category C (Lower Strength initially): the gentle Moon and strict Saturn require deep patience and emotional grounding. Your true royal leadership matures steadily with age and life experience."
    },

    # ── ROOT 2: MOON (CHANDRA) · Emotional, Gentle, Slow, Sensitive, Attractive, Intuitive, Sensitive mood swings ──
    2: {
        "day": 2, "root": 2, "code": "2(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength",
        "planet": "Moon (Chandra)", "is_karmic": False, "is_master": False,
        "keywords": ["Emotional", "Gentle", "Slow", "Sensitive", "Attractive", "Intuitive", "Sensitive mood swings"],
        "essence": "Pure Lunar vibration. Category B (Normal Strength): gentle emotional intelligence, attractive magnetism, peacemaking diplomacy. Requires supportive environments to navigate sensitive mood swings.",
        "humanized_reading": "Your birth day 2 grants you Category B (Normal Strength) lunar energy: deep empathy, charming gentleness, and natural intuition. You bring peace to tense environments through quiet understanding."
    },
    11: {
        "day": 11, "root": 2, "code": "11(a)", "tier": "a",
        "strength_category": "A", "strength_title": "Category A — Good Strength (Master Number 11)",
        "planet": "Moon (Chandra)", "is_karmic": False, "is_master": True,
        "keywords": ["Emotional", "Gentle", "Sensitive", "Attractive", "Intuitive", "Master Number 11", "Spiritual Vision", "Mood swings"],
        "essence": "Master Number 11 (The Spiritual Illuminator). Category A (Good Strength): double Sun (1-1) empowering Moon. Supreme intuitive vision, spiritual illumination, charismatic counselor. Can suffer from acute mood swings without daily grounding.",
        "humanized_reading": "Born on the 11th, you possess Category A (Good Strength) Master Number power: exceptional spiritual intuition, charismatic vision, and inspiring empathy. Daily grounding helps stabilize your sensitive emotional currents."
    },
    20: {
        "day": 20, "root": 2, "code": "20(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength",
        "planet": "Moon (Chandra)", "is_karmic": False, "is_master": False,
        "keywords": ["Emotional", "Gentle", "Slow", "Sensitive", "Attractive", "Intuitive", "Introspective"],
        "essence": "Moon (2) reinforced by Zero. Category B (Normal Strength): deep contemplative sensitivity, artistic imagination, gentle peacemaker. Flourishes in low-stress, emotionally safe spaces.",
        "humanized_reading": "Born on the 20th, you carry Category B (Normal Strength) lunar balance: quiet artistic sensitivity, compassionate listening, and emotional depth. You flourish when working at a steady, thoughtful pace."
    },
    29: {
        "day": 29, "root": 2, "code": "29(c)", "tier": "c",
        "strength_category": "C", "strength_title": "Category C — Lower Strength (High Emotional Swings)",
        "planet": "Moon (Chandra)", "is_karmic": False, "is_master": False,
        "keywords": ["Emotional", "Gentle", "Sensitive", "Attractive", "Intuitive", "Passionate", "Intense mood swings"],
        "essence": "Moon (2) + Mars (9) resolving into 11/2. Category C (Lower Strength initially): sharp clash between water and fire. High emotional intensity, passionate intuition, but vulnerable to acute mood swings and relationship friction.",
        "humanized_reading": "Born on the 29th, your Category C (Lower Strength initially) combines deep feeling with fiery impulse: managing sudden mood swings and grounding emotional passion allows your powerful intuition to shine brightly."
    },

    # ── ROOT 3: JUPITER (GURU) · Imaginative, Healer, Preacher, Spiritual, Religious, Counselor ──
    3: {
        "day": 3, "root": 3, "code": "3(c)", "tier": "c",
        "strength_category": "C", "strength_title": "Category C — Lower Strength (Scattered Focus)",
        "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
        "keywords": ["Imaginative", "Healer", "Preacher", "Spiritual", "Religious", "Counselor"],
        "essence": "Pure Jupiterian frequency. Category C (Lower Strength): vast creative imagination and spiritual depth, but can suffer from scattered focus or lack of commercial execution without structured boundaries.",
        "humanized_reading": "Born on the 3rd, you carry Category C creative Jupiter energy: highly imaginative, spiritual, and a natural counselor, but you need structured focus and grounding to turn brilliant ideas into tangible results."
    },
    12: {
        "day": 12, "root": 3, "code": "12(a)", "tier": "a",
        "strength_category": "A", "strength_title": "Category A — Good Strength (Executive Counselor)",
        "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
        "keywords": ["Imaginative", "Healer", "Preacher", "Spiritual", "Religious", "Counselor", "Diplomatic Speaker"],
        "essence": "Sun (1) + Moon (2) resolving into Jupiter (3). Category A (Good Strength): executive clarity blended with emotional diplomacy. Highly persuasive orator, ethical preacher, and trusted institutional advisor.",
        "humanized_reading": "Born on the 12th, you possess Category A (Good Strength) wisdom: a masterly blend of executive leadership (1) and empathetic diplomacy (2) that makes you a compelling preacher, healer, and advisor."
    },
    21: {
        "day": 21, "root": 3, "code": "21(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength (Crown of Magi)",
        "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
        "keywords": ["Imaginative", "Healer", "Preacher", "Spiritual", "Religious", "Counselor", "Crown of Magi"],
        "essence": "Moon (2) + Sun (1) resolving into Jupiter (3). Category B (Normal Strength): Crown of the Magi. Magnetic communicative grace, popular social charm, successful counselor and artistic creator.",
        "humanized_reading": "Born on the 21st, you hold Category B (Normal Strength) Jupiter charm: known classically as the Crown of the Magi, you express creative wisdom, social popularity, and inspiring counseling ability."
    },
    30: {
        "day": 30, "root": 3, "code": "30(c)", "tier": "c",
        "strength_category": "C", "strength_title": "Category C — Lower Strength (Philosophical Detachment)",
        "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
        "keywords": ["Imaginative", "Healer", "Preacher", "Spiritual", "Religious", "Counselor", "Philosophical"],
        "essence": "Jupiter (3) + Zero. Category C (Lower Strength): deep philosophical and spiritual contemplation, natural healer, but disfavors commercial pressure and requires external motivation to monetize gifts.",
        "humanized_reading": "Born on the 30th, you carry Category C introspective Jupiter strength: profound spiritual imagination, healing presence, and philosophical depth, best nurtured when freed from petty office politics."
    },

    # ── ROOT 4: RAHU · Disciplined, Organized, Short tempered, Rebellious, Abusive, Stubborn, Logical impulsive ──
    4: {
        "day": 4, "root": 4, "code": "4(c)", "tier": "c",
        "strength_category": "C", "strength_title": "Category C — Lower Strength (Frictional Rebelliousness)",
        "planet": "Rahu", "is_karmic": False, "is_master": False,
        "keywords": ["Disciplined", "Organized", "Short tempered", "Rebellious", "Abusive/Stubborn", "Logical impulsive"],
        "essence": "Pure Rahu frequency. Category C (Lower Strength): highly organized and disciplined, but vulnerable to short-tempered reactions, stubborn rebelliousness, and sudden impulsive resistance to traditional systems.",
        "humanized_reading": "Born on the 4th, you navigate Category C (Lower Strength in conventional setups): you are organized and disciplined, but short-tempered impatience or stubborn rebelliousness can cause friction unless channeled constructively."
    },
    13: {
        "day": 13, "root": 4, "code": "13(d)", "tier": "d",
        "strength_category": "D", "strength_title": "Category D — Karmic Debt Transformation",
        "planet": "Rahu", "is_karmic": True, "is_master": False,
        "keywords": ["Disciplined", "Organized", "Short tempered", "Rebellious", "Stubborn", "Logical impulsive", "Karmic 13"],
        "essence": "Karmic Debt Number 13 (The Karmic Architect). Sun (1) + Jupiter (3) under Rahu. Category D: heavy early trials, demanding hard labor, short-tempered impatience; transforms through relentless discipline into monumental success.",
        "humanized_reading": "Born on the 13th, you bear Category D (Karmic Debt Number 13): life tests you with demanding hard work and short-tempered friction, but your rigorous discipline ultimately builds unshakeable, monumental success."
    },
    22: {
        "day": 22, "root": 4, "code": "22(a)", "tier": "a",
        "strength_category": "A", "strength_title": "Category A — Good Strength (Master Builder)",
        "planet": "Rahu", "is_karmic": False, "is_master": True,
        "keywords": ["Disciplined", "Organized", "Master Number 22", "Master Builder", "Global Vision", "Systemic Scale"],
        "essence": "Master Number 22 (The Master Builder). Category A (Good Strength): double Moon (2-2) channeling Rahu. Extraordinary systemic mastery, organizes colossal enterprises, practical genius of international scale.",
        "humanized_reading": "Born on the 22nd, you hold Category A (Good Strength) Master Builder power: exceptional systemic discipline, visionary planning, and the capacity to manifest large-scale, enduring institutional projects."
    },
    31: {
        "day": 31, "root": 4, "code": "31(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength (Practical Visionary)",
        "planet": "Rahu", "is_karmic": False, "is_master": False,
        "keywords": ["Disciplined", "Organized", "Rebellious", "Logical impulsive", "Shrewd Strategist"],
        "essence": "Jupiter (3) + Sun (1) resolving into Rahu (4). Category B (Normal Strength): visionary strategic planner, highly methodical, rebellious against slow bureaucracy, builds enduring commercial structures.",
        "humanized_reading": "Born on the 31st, you carry Category B (Normal Strength) strategic drive: combining creative foresight (3) with executive initiative (1), you organize systems with practical, disciplined logic."
    },

    # ── ROOT 5: MERCURY (BUDH) · Happy go lucky, Lazy, Dark horse, Entertaining, Communicative ──
    5: {
        "day": 5, "root": 5, "code": "5(c)", "tier": "c",
        "strength_category": "C", "strength_title": "Category C — Lower Strength (Restless Inertia)",
        "planet": "Mercury (Budh)", "is_karmic": False, "is_master": False,
        "keywords": ["Happy go lucky", "Lazy", "Dark horse", "Entertaining", "Communicative"],
        "essence": "Pure Mercury. Category C (Lower Strength): jovial, happy-go-lucky charisma, but prone to bouts of laziness, procrastination, or restless hopping between ventures until forced to focus.",
        "humanized_reading": "Born on the 5th, you carry Category C (Lower Strength in steady routines): entertaining, communicative, and happy-go-lucky, you must guard against temporary laziness and restless boredom to unlock your true gifts."
    },
    14: {
        "day": 14, "root": 5, "code": "14(a)", "tier": "a",
        "strength_category": "A", "strength_title": "Category A — Good Strength (Karmic 14 / Dynamic Dark Horse)",
        "planet": "Mercury (Budh)", "is_karmic": True, "is_master": False,
        "keywords": ["Happy go lucky", "Dark horse", "Entertaining", "Communicative", "Karmic 14", "Adaptable"],
        "essence": "Karmic Debt Number 14 (The River of Change). Category A (Good Strength): Sun (1) + Rahu (4) under Mercury (5). Highly magnetic dark horse, brilliant communicator, rapid commercial adaptability when disciplined.",
        "humanized_reading": "Born on the 14th, you possess Category A (Good Strength) dynamic charm: a brilliant communicative dark horse with Karmic Number 14 versatility, capable of rapid commercial breakthroughs when focused."
    },
    23: {
        "day": 23, "root": 5, "code": "23(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength (Royal Star of Lion)",
        "planet": "Mercury (Budh)", "is_karmic": False, "is_master": False,
        "keywords": ["Happy go lucky", "Dark horse", "Entertaining", "Communicative", "Royal Star of Lion", "Supreme Charm"],
        "essence": "Moon (2) + Jupiter (3) resolving into Mercury (5). Category B (Normal Strength): Royal Star of the Lion. Highest commercial charm, effortless communication, captivating entertainer, attracts fortunate connections.",
        "humanized_reading": "Born on the 23rd, you hold Category B (Normal Strength) magnetic grace: classically called the Royal Star of the Lion, your entertaining communication and diplomatic warmth attract steady prosperity."
    },

    # ── ROOT 6: VENUS (SHUKRA) · Romantic, Communicator, Manipulative/Diplomatic, Family oriented, Shrewd ──
    6: {
        "day": 6, "root": 6, "code": "6(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength (Balanced Harmony)",
        "planet": "Venus (Shukra)", "is_karmic": False, "is_master": False,
        "keywords": ["Romantic", "Communicator", "Manipulative/Diplomatic", "Family oriented", "Shrewd"],
        "essence": "Pure Venusian luxury. Category B (Normal Strength): highly romantic, magnetic communicator, deeply family-oriented, shrewd aesthetic and commercial negotiator.",
        "humanized_reading": "Born on the 6th, you carry Category B (Normal Strength) Venusian grace: warm romance, strong family devotion, shrewd taste, and diplomatic charm that creates peaceful, beautiful surroundings."
    },
    15: {
        "day": 15, "root": 6, "code": "15(a)", "tier": "a",
        "strength_category": "A", "strength_title": "Category A — Good Strength (Magnetic Dealmaker)",
        "planet": "Venus (Shukra)", "is_karmic": False, "is_master": False,
        "keywords": ["Romantic", "Communicator", "Manipulative/Diplomatic", "Family oriented", "Shrewd", "Magnetic Charisma"],
        "essence": "Sun (1) + Mercury (5) resolving into Venus (6). Category A (Good Strength): hypnotic communicator, shrewd dealmaker, magnetic social standing, luxurious family lifestyle.",
        "humanized_reading": "Born on the 15th, you possess Category A (Good Strength) charisma: blending solar leadership (1) with mercantile wit (5), you are a shrewd, magnetic communicator and romantic provider."
    },
    24: {
        "day": 24, "root": 6, "code": "24(c)", "tier": "c",
        "strength_category": "C", "strength_title": "Category C — Lower Strength (Domestic Burden)",
        "planet": "Venus (Shukra)", "is_karmic": False, "is_master": False,
        "keywords": ["Romantic", "Communicator", "Family oriented", "Diplomatic", "Shrewd Caretaker"],
        "essence": "Moon (2) + Rahu (4) resolving into Venus (6). Category C (Lower Strength initially): heavy family responsibilities, prone to over-attachment, emotional manipulation, or domestic worry before finding peace.",
        "humanized_reading": "Born on the 24th, you navigate Category C (Lower Strength in domestic ease): deeply family-oriented and diplomatic, you often carry silent household burdens that require setting healthy emotional boundaries."
    },

    # ── ROOT 7: KETU · Low in confidence (youth), Inquisitive, Very good healer occult, Spiritual religious, Researcher, Introvert ──
    7: {
        "day": 7, "root": 7, "code": "7(c)", "tier": "c",
        "strength_category": "C", "strength_title": "Category C — Lower Strength (Early Self-Doubt)",
        "planet": "Ketu", "is_karmic": False, "is_master": False,
        "keywords": ["Low in confidence (youth)", "Inquisitive", "Very good healer occult", "Spiritual religious", "Researcher", "Introvert"],
        "essence": "Pure Ketu vibration. Category C (Lower Strength): deeply inquisitive and an exceptional occult healer, but prone to early low confidence, social introversion, and self-doubt before claiming wisdom.",
        "humanized_reading": "Born on the 7th, you operate under Category C (Lower Strength in youthful confidence): an inquisitive researcher, spiritual seeker, and occult healer, your confidence blossoms as you master your specialized craft."
    },
    16: {
        "day": 16, "root": 7, "code": "16(a)", "tier": "a",
        "strength_category": "A", "strength_title": "Category A — Good Strength (Karmic 16 / Awakened Healer)",
        "planet": "Ketu", "is_karmic": True, "is_master": False,
        "keywords": ["Inquisitive", "Very good healer occult", "Spiritual religious", "Researcher", "Introvert", "Karmic 16", "Shattered Citadel"],
        "essence": "Karmic Debt Number 16 (The Shattered Citadel). Category A (Good Strength): Sun (1) + Venus (6) under Ketu. Early disillusionments strip away superficial ego, unlocking extraordinary healing, occult mastery, and spiritual wisdom.",
        "humanized_reading": "Born on the 16th, you hold Category A (Good Strength) spiritual depth with Karmic 16 wisdom: early sudden awakenings purify your path, making you an exceptionally gifted occult researcher and intuitive healer."
    },
    25: {
        "day": 25, "root": 7, "code": "25(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength (Analytical Researcher)",
        "planet": "Ketu", "is_karmic": False, "is_master": False,
        "keywords": ["Inquisitive", "Very good healer occult", "Spiritual religious", "Researcher", "Introvert", "Analytical Insight"],
        "essence": "Moon (2) + Mercury (5) resolving into Ketu (7). Category B (Normal Strength): brilliant analytical intellect, intuitive researcher, gifted diagnostic counselor, quiet introspective strength.",
        "humanized_reading": "Born on the 25th, you carry Category B (Normal Strength) analytical insight: combining emotional empathy (2) with quick logic (5), you excel as an inquisitive researcher and spiritual problem-solver."
    },

    # ── ROOT 8: SATURN (SHANI) · Struggle, Laborious, Hardwork, Logical, Argumentative, Stubborn, Law, Finance ──
    8: {
        "day": 8, "root": 8, "code": "8(a)", "tier": "a",
        "strength_category": "A", "strength_title": "Category A — Good Strength (Enduring Resilience)",
        "planet": "Saturn (Shani)", "is_karmic": False, "is_master": False,
        "keywords": ["Struggle", "Laborious", "Hardwork", "Logical", "Argumentative", "Stubborn", "Law", "Finance"],
        "essence": "Pure Saturnian crucible. Category A (Good Strength): early struggle and laborious hard work forge an unshakeable logical mind, master of law, structural governance, and large-scale compounding finance.",
        "humanized_reading": "Born on the 8th, you possess Category A (Good Strength) Saturnian resilience: early struggle and laborious hard work sharpen your formidable logic, making you a master of law, finance, and compounding authority."
    },
    17: {
        "day": 17, "root": 8, "code": "17(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength (Star of the Magi)",
        "planet": "Saturn (Shani)", "is_karmic": False, "is_master": False,
        "keywords": ["Struggle", "Hardwork", "Logical", "Law", "Finance", "Star of Magi", "Enduring Victory"],
        "essence": "Star of the Magi. Sun (1) + Ketu (7) resolving into Saturn (8). Category B (Normal Strength): overcomes early karmic obstacles through spiritual insight; achieves monumental financial and institutional authority.",
        "humanized_reading": "Born on the 17th, you hold Category B (Normal Strength) Saturnian grace: classically revered as the Star of the Magi, your hard work and spiritual logic overcome all struggle to achieve enduring financial victory."
    },
    26: {
        "day": 26, "root": 8, "code": "26(c)", "tier": "c",
        "strength_category": "C", "strength_title": "Category C — Lower Strength (Laborious Burdens)",
        "planet": "Saturn (Shani)", "is_karmic": False, "is_master": False,
        "keywords": ["Struggle", "Laborious", "Hardwork", "Logical", "Family Duty", "Law", "Finance"],
        "essence": "Moon (2) + Venus (6) resolving into Saturn (8). Category C (Lower Strength initially): heavy family duties and partnership burdens; laborious struggle before financial stability crystallizes.",
        "humanized_reading": "Born on the 26th, you navigate Category C (Lower Strength in early ease): carrying heavy family duties and laborious financial responsibilities, your stubborn persistence ultimately secures solid material foundations."
    },

    # ── ROOT 9: MARS (MANGAL) · Unpredictable behaviour, Warrior rough n tough, Good humanitarian, Egotistic ──
    9: {
        "day": 9, "root": 9, "code": "9(a)", "tier": "a",
        "strength_category": "A", "strength_title": "Category A — Good Strength (Pure Warrior)",
        "planet": "Mars (Mangal)", "is_karmic": False, "is_master": False,
        "keywords": ["Unpredictable behaviour", "Warrior rough n tough", "Good humanitarian", "Egotistic"],
        "essence": "Pure Mars energy. Category A (Good Strength): fearless, rough-and-tough warrior, noble humanitarian protector, unpredictable high-voltage drive. Driven by courageous defense of others.",
        "humanized_reading": "Born on the 9th, you hold Category A (Good Strength) warrior power: rough-and-tough, noble humanitarian courage with high energetic passion. Channeling unpredictable temper into service makes you an unstoppable protector."
    },
    18: {
        "day": 18, "root": 9, "code": "18(c)", "tier": "c",
        "strength_category": "C", "strength_title": "Category C — Lower Strength (Severe Internal Conflict)",
        "planet": "Mars (Mangal)", "is_karmic": False, "is_master": False,
        "keywords": ["Unpredictable behaviour", "Warrior rough n tough", "Good humanitarian", "Egotistic", "Trials of Strength"],
        "essence": "Sun (1) + Saturn (8) resolving into Mars (9). Category C (Lower Strength initially): intense friction between solar executive pride and Saturnian delay. Severe trials of strength forge an invincible humanitarian.",
        "humanized_reading": "Born on the 18th, you navigate Category C (Lower Strength in peaceful flow): an intense clash between Sun (1) and Saturn (8) tests your patience, but facing these trials of strength shapes an invincible warrior for noble causes."
    },
    27: {
        "day": 27, "root": 9, "code": "27(b)", "tier": "b",
        "strength_category": "B", "strength_title": "Category B — Normal Strength (The Sceptre)",
        "planet": "Mars (Mangal)", "is_karmic": False, "is_master": False,
        "keywords": ["Warrior rough n tough", "Good humanitarian", "Intuitive Protector", "Commanding"],
        "essence": "The Sceptre. Moon (2) + Ketu (7) resolving into Mars (9). Category B (Normal Strength): intuitive spiritual warrior, rough-and-tough integrity, commanding protector, combines strategic wisdom with bold action.",
        "humanized_reading": "Born on the 27th, you carry Category B (Normal Strength) commanding integrity: classically known as The Sceptre, your intuitive wisdom and protective rough-and-tough courage earn deep respect."
    }
}
'''

    new_full_code = base_code + enriched_registry_code
    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_full_code)
    print("Successfully enriched app/engine/number_characteristics_registry.py with Category A/B/C/D strengths!")

if __name__ == '__main__':
    enrich_registry()
