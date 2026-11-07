"""
NV-002: NUMBER CHARACTERISTICS REGISTRY
Numeros Vision — ANVEIL EVERY CHARM

Single source of truth for characteristics, planetary rulers, strengths,
challenges, behavioural tendencies, profession mappings, friendly/enemy/neutral
relationships, and favourable attunements across numbers 1 through 9,
master numbers (11, 22, 33), and compound numbers (10 to 52).
Ensures zero contradiction across all downstream modules.
"""

from typing import Dict, Any, List, Optional
from app.engine.cheiro_engine import CHEIRO_DATASET

NUMBER_REGISTRY: Dict[int, Dict[str, Any]] = {
    1: {
        "number": 1,
        "root_number": 1,
        "type": "Single Digit / Root",
        "planet": "Sun (Surya)",
        "alternative_planet": "Apollo / Solar Force",
        "element": "Fire",
        "core_characteristics": "Pioneering, original, authoritative, self-reliant, ambitious, and executive-minded.",
        "strengths": ["Visionary leadership", "Independent initiative", "Unwavering willpower", "Executive decision-making", "Courage under pressure"],
        "challenges": ["Impatience", "Tendency toward stubbornness or ego battles", "Difficulty delegating routine tasks", "Dominating presence"],
        "behavioural_tendencies": "Direct, purposeful, energetic, prefers initiating over maintaining, thrives in autonomous roles.",
        "communication_tendencies": "Clear, authoritative, assertive, concise, prefers giving directives over listening to prolonged debates.",
        "leadership_tendencies": "Natural executive; sets clear direction and expects high standards of loyalty and execution from peers.",
        "creativity_and_analytical": "Original conceptual thinker; invents novel frameworks rather than copying existing templates.",
        "relationship_interpretations": "Generous and fiercely protective, but requires mutual respect and personal space to operate.",
        "career_associations": [
            "Executive Management", "Public Governance & Civil Services", "Entrepreneurship & Founders",
            "Institutional Directorship", "Defense & Military Leadership", "Surgical Medicine", "Jewelry & Gold Trade"
        ],
        "business_interpretations": "Thrives when holding majority authority or acting as primary strategic visionary; disfavors restrictive micro-partnerships.",
        "financial_themes": "Attracts resources through bold commercial initiatives; must practice conservative asset retention to avoid speculative overreach.",
        "personal_development": "Cultivate active empathetic listening and patience with slower-paced colleagues to multiply influence.",
        "friendly_numbers": [1, 2, 3, 5, 9],
        "neutral_numbers": [4, 6, 7],
        "enemy_numbers": [8],
        "favourable_days": ["Sunday", "Monday"],
        "favourable_colours": ["Gold", "Orange", "Copper", "Warm Yellow", "Bright Amber"],
        "colours_to_avoid": ["Black", "Dark Navy", "Dark Grey"],
        "remedy_references": [
            "Offer pure water to the rising Sun in a copper vessel daily.",
            "Incorporate natural copper or gold accessories.",
            "Practice 10 minutes of morning solar light alignment."
        ],
        "yantra_references": ["Surya Yantra", "Gayatri Yantra"],
        "methodology_id": "METH-VEDIC-001",
        "evidence_category": "Standard Classical Canon",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    2: {
        "number": 2,
        "root_number": 2,
        "type": "Single Digit / Root",
        "planet": "Moon (Chandra)",
        "alternative_planet": "Diana / Lunar Force",
        "element": "Water",
        "core_characteristics": "Intuitive, diplomatic, empathetic, adaptable, harmonizing, and deeply perceptive.",
        "strengths": ["Deep emotional intelligence", "Peacemaking diplomacy", "Psychological intuition", "Collaborative grace", "Aesthetic appreciation"],
        "challenges": ["Mood fluctuations", "Hesitation in conflict", "Sensitivity to criticism", "Tendency to over-absorb environmental stress"],
        "behavioural_tendencies": "Supportive, considerate, values gentle pacing, seeks peaceful consensus, thrives in harmonious spaces.",
        "communication_tendencies": "Gentle, persuasive, empathetic, listens deeply before responding, avoids aggressive confrontation.",
        "leadership_tendencies": "Quiet diplomacy; influences through coalition-building, empathy, and subtle interpersonal alignment.",
        "creativity_and_analytical": "Imaginative, artistic, poetic, possesses a keen sense of rhythm, design, and emotional aesthetics.",
        "relationship_interpretations": "Devoted, loving, and deeply loyal; thrives in safe, emotionally reciprocal partnerships.",
        "career_associations": [
            "Psychology & Counseling", "Diplomacy & Public Relations", "Hospitality & Gastronomy",
            "Maritime & Water Industries", "Fine Arts & Music", "Healthcare & Nursing", "Human Resources"
        ],
        "business_interpretations": "Flourishes in partnerships, collaborative joint ventures, and customer-facing service businesses.",
        "financial_themes": "Steady fluid income; benefits from automated, disciplined savings to balance fluctuating emotional spending.",
        "personal_development": "Build emotional boundaries; avoid absorbing external worries and practice grounded self-affirmation.",
        "friendly_numbers": [1, 2, 3, 5],
        "neutral_numbers": [6, 7],
        "enemy_numbers": [4, 8, 9],
        "favourable_days": ["Monday", "Sunday"],
        "favourable_colours": ["White", "Silver", "Cream", "Pearl", "Pale Green"],
        "colours_to_avoid": ["Dark Red", "Black", "Dark Blue"],
        "remedy_references": [
            "Respect and honor maternal figures.",
            "Keep a solid silver item or wear natural pearl/moonstone.",
            "Drink water from a silver cup or keep silver coin in wallet."
        ],
        "yantra_references": ["Chandra Yantra", "Shiva Yantra"],
        "methodology_id": "METH-VEDIC-001",
        "evidence_category": "Standard Classical Canon",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    3: {
        "number": 3,
        "root_number": 3,
        "type": "Single Digit / Root",
        "planet": "Jupiter (Guru)",
        "alternative_planet": "Jove / Sagittarian Wisdom",
        "element": "Wood / Ether",
        "core_characteristics": "Expansive, wise, communicative, optimistic, philosophical, and knowledge-seeking.",
        "strengths": ["Vast intellectual capacity", "Inspirational mentorship", "Creative communication", "Moral integrity", "Broad vision"],
        "challenges": ["Scattering focus across too many interests", "Occasional dogmatism", "Overextending commitments", "Impatience with small details"],
        "behavioural_tendencies": "Generous, curious, teacher-like presence, naturally uplifting, drawn to higher learning.",
        "communication_tendencies": "Articulate, expressive, storytelling-driven, enthusiastic, naturally instructive.",
        "leadership_tendencies": "Mentorship leadership; motivates through knowledge, inspiring values, and long-term ethical purpose.",
        "creativity_and_analytical": "High linguistic and conceptual synthesis; connects disparate ideas into unified theories.",
        "relationship_interpretations": "Joyful, generous, and intellectually engaging; values shared philosophical or cultural growth.",
        "career_associations": [
            "Higher Education & University Teaching", "Management Consulting", "Legal Advisory & Judiciary",
            "Publishing & Authorship", "Financial Planning & Wealth Strategy", "Spiritual Counseling", "Public Speaking"
        ],
        "business_interpretations": "Excels in educational platforms, intellectual property, professional consulting, and advisory boards.",
        "financial_themes": "Strong wealth attraction capacity; must balance broad generosity with rigorous budgeting boundaries.",
        "personal_development": "Prioritize depth over breadth; master one core discipline before initiating multiple new branches.",
        "friendly_numbers": [1, 2, 3, 5, 7, 9],
        "neutral_numbers": [8],
        "enemy_numbers": [6],
        "favourable_days": ["Thursday", "Tuesday"],
        "favourable_colours": ["Bright Yellow", "Golden Yellow", "Amber", "Saffron", "Cream"],
        "colours_to_avoid": ["Harsh Pink", "Dark Blue", "Muddy Brown"],
        "remedy_references": [
            "Apply saffron or yellow turmeric tilak on forehead.",
            "Respect teachers, mentors, and elders.",
            "Donate yellow lentils (Chana dal) or books to students on Thursdays."
        ],
        "yantra_references": ["Brihaspati Yantra", "Saraswati Yantra"],
        "methodology_id": "METH-VEDIC-001",
        "evidence_category": "Standard Classical Canon",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    4: {
        "number": 4,
        "root_number": 4,
        "type": "Single Digit / Root",
        "planet": "Rahu (North Node)",
        "alternative_planet": "Uranus / Grounded Builder",
        "element": "Wood / Earth",
        "core_characteristics": "Unconventional, analytical, technologically sharp, disciplined, disruptive, and determined.",
        "strengths": ["Pattern recognition", "Structural architecture", "Innovative disruption", "Perseverance in adversity", "Deep technical mastery"],
        "challenges": ["Sudden unpredictable delays", "Skepticism", "Internal restlessness", "Resistance to conventional restrictions"],
        "behavioural_tendencies": "Systematic yet rebellious, questions status quo, focuses on structural efficiency, intensely focused.",
        "communication_tendencies": "Analytical, incisive, factual, sometimes blunt or contrarian, disdains superficial small talk.",
        "leadership_tendencies": "Architectural leadership; builds scalable frameworks, challenges inefficiency, commands through technical rigor.",
        "creativity_and_analytical": "Exceptional problem-solving, debugging, reverse engineering, and large-scale structural design.",
        "relationship_interpretations": "Fiercely loyal to those who respect their autonomy; can take time to open up emotionally.",
        "career_associations": [
            "Software Architecture & AI", "Civil & Mechanical Engineering", "Data Analytics & Cryptography",
            "Real Estate & Construction", "Research & Forensics", "Aviation & Electronics", "Strategic Auditing"
        ],
        "business_interpretations": "Thrives in modern technology, high-scale digital platforms, unconventional niches, and infrastructure.",
        "financial_themes": "Sudden financial shifts; requires conservative liquid safety nets and avoidance of speculative gambling.",
        "personal_development": "Maintain grounded daily morning routines and mindful speech to prevent misunderstandings with colleagues.",
        "friendly_numbers": [1, 5, 6, 7],
        "neutral_numbers": [3],
        "enemy_numbers": [2, 8, 9],
        "favourable_days": ["Wednesday", "Saturday", "Sunday"],
        "favourable_colours": ["Electric Blue", "Grey", "Khaki", "Silver", "Smoky Blue"],
        "colours_to_avoid": ["Black", "Fiery Red", "Dark Charcoal"],
        "remedy_references": [
            "Keep a solid silver square piece in wallet or pocket.",
            "Donate to underprivileged workers or support community sanitation initiatives.",
            "Avoid wearing dark black clothing on critical meeting days."
        ],
        "yantra_references": ["Rahu Yantra", "Ganesha Yantra"],
        "methodology_id": "METH-VEDIC-001",
        "evidence_category": "Standard Classical Canon",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    5: {
        "number": 5,
        "root_number": 5,
        "type": "Single Digit / Root",
        "planet": "Mercury (Budh)",
        "alternative_planet": "Hermes / Commercial Speed",
        "element": "Earth",
        "core_characteristics": "Versatile, commercial, quick-witted, communicative, adaptable, and networking-oriented.",
        "strengths": ["Rapid intellectual adaptability", "Commercial acumen", "Effortless networking", "Multitasking agility", "Youthful vitality"],
        "challenges": ["Restlessness", "Impulsive decisions", "Easily bored by repetitive routine", "Scattered energy"],
        "behavioural_tendencies": "Brisk, sociable, inquisitive, constantly exploring new ideas, hates feeling trapped in static environments.",
        "communication_tendencies": "Witty, persuasive, charming, rapid-fire conversationalist, highly responsive on digital channels.",
        "leadership_tendencies": "Agile leadership; empowers decentralized teams, drives commercial partnerships, adapts swiftly to market changes.",
        "creativity_and_analytical": "Commercial creativity, rapid data synthesis, copywriting, trading strategy, and business diplomacy.",
        "relationship_interpretations": "Charming, lively, and engaging; requires intellectual stimulation, humor, and freedom in relationships.",
        "career_associations": [
            "Commercial Trading & Brokerage", "Digital Marketing & Media", "Journalism & Mass Communication",
            "E-commerce & Retail", "Public Relations & Event Management", "Software Development", "Travel & Tourism"
        ],
        "business_interpretations": "Natural merchant; excels in high-turnover businesses, affiliate networks, digital products, and trading.",
        "financial_themes": "Multiple active revenue streams; needs disciplined long-term capital lock-ins to prevent premature liquidation.",
        "personal_development": "Cultivate stillness and physical grounding; finish ongoing projects before launching exciting new concepts.",
        "friendly_numbers": [1, 2, 3, 5, 6],
        "neutral_numbers": [7, 8, 9],
        "enemy_numbers": [],
        "favourable_days": ["Wednesday", "Friday"],
        "favourable_colours": ["Emerald Green", "Light Green", "Mint", "Turquoise", "Cream"],
        "colours_to_avoid": ["Harsh Red", "Dark Muddy Brown"],
        "remedy_references": [
            "Keep live green indoor plants in home and workspace.",
            "Donate green gram (moong dal) or feed green fodder to cows on Wednesdays.",
            "Incorporate green aventurine or emerald in jewelry."
        ],
        "yantra_references": ["Budh Yantra", "Kuber Yantra"],
        "methodology_id": "METH-VEDIC-001",
        "evidence_category": "Standard Classical Canon",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    6: {
        "number": 6,
        "root_number": 6,
        "type": "Single Digit / Root",
        "planet": "Venus (Shukra)",
        "alternative_planet": "Aphrodite / Luxe & Harmony",
        "element": "Metal / Air",
        "core_characteristics": "Harmonious, aesthetic, magnetic, luxury-oriented, responsible, and relationship-centric.",
        "strengths": ["Aesthetic excellence", "Relationship stewardship", "Diplomatic charm", "Luxury branding acumen", "Nurturing generosity"],
        "challenges": ["Excessive compromise to avoid tension", "Vulnerability to flattery", "Overspending on aesthetic luxuries", "Possessiveness"],
        "behavioural_tendencies": "Graceful, hospitable, seeks beauty and order, dedicated to family comfort, drawn to fine quality.",
        "communication_tendencies": "Warm, tactful, soothing, persuasive, values tone and emotional decorum.",
        "leadership_tendencies": "Empathetic servant leadership; builds high-morale teams, curates brand prestige, leads with quiet charisma.",
        "creativity_and_analytical": "High sensory and aesthetic sensibility, interior styling, fashion design, musical harmony, and luxury design.",
        "relationship_interpretations": "Deeply devoted, affectionate, and romantic; seeks lifelong stability, mutual devotion, and domestic harmony.",
        "career_associations": [
            "Luxury Goods & Fashion Design", "Interior Architecture & Aesthetics", "Hospitality & Premium Dining",
            "Media Production & Entertainment", "Corporate Banking & Wealth Advisory", "Cosmetics & Wellness", "Relationship Counseling"
        ],
        "business_interpretations": "Excels in consumer luxury, lifestyle brands, high-ticket services, and aesthetic experiences.",
        "financial_themes": "Strong natural abundance frequency; benefits from partnering with practical accountants to govern expenses.",
        "personal_development": "Learn to say 'no' comfortably without guilt; maintain personal boundaries in both business and family.",
        "friendly_numbers": [5, 6, 8],
        "neutral_numbers": [1, 2, 4, 7],
        "enemy_numbers": [3],
        "favourable_days": ["Friday", "Wednesday"],
        "favourable_colours": ["Soft Pink", "Diamond White", "Cream", "Light Sky Blue", "Pastel Shades"],
        "colours_to_avoid": ["Dark Yellow", "Muddy Brown", "Jet Black"],
        "remedy_references": [
            "Respect women and spouse; maintain clean, sweet-smelling living spaces.",
            "Use natural floral perfumes (sandalwood or rose).",
            "Wear white clothes on Friday and donate white sweets or curd to needy."
        ],
        "yantra_references": ["Shukra Yantra", "Shri Yantra"],
        "methodology_id": "METH-VEDIC-001",
        "evidence_category": "Standard Classical Canon",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    7: {
        "number": 7,
        "root_number": 7,
        "type": "Single Digit / Root",
        "planet": "Ketu (South Node)",
        "alternative_planet": "Neptune / Spiritual Mystic",
        "element": "Metal / Water",
        "core_characteristics": "Introspective, analytical, spiritual, research-driven, intuitive, and philosophical.",
        "strengths": ["Deep investigative research", "Spiritual discernment", "Intuitive foresight", "Technical skepticism", "Calm solitary focus"],
        "challenges": ["Tendency toward aloof detachment", "Overthinking", "Restlessness with social superficiality", "Cynicism"],
        "behavioural_tendencies": "Quiet, observant, values personal solitude, dislikes crowded spaces, drawn to esoteric mysteries.",
        "communication_tendencies": "Selective, thoughtful, speaks only when substantively necessary, concise, insightful.",
        "leadership_tendencies": "Thought leadership; guides through specialized technical mastery, research excellence, and strategic foresight.",
        "creativity_and_analytical": "Unmatched depth in data mining, spiritual synthesis, philosophy, auditing, and occult/scientific studies.",
        "relationship_interpretations": "Needs a partner who respects their need for quiet solitude; deeply faithful when authentic trust is established.",
        "career_associations": [
            "Data Science & Cryptography", "Specialized Medical Research", "Philosophy & Metaphysics",
            "Technical Auditing & Quality Assurance", "Forensics & Intelligence", "Authorship & Editorial", "Aviation & Astrology"
        ],
        "business_interpretations": "Best suited for specialized R&D boutiques, algorithmic software, consulting think tanks, and advisory.",
        "financial_themes": "Indifferent to superficial wealth displays; must intentionally anchor assets in secure real property.",
        "personal_development": "Balance intellectual retreat with compassionate everyday engagement; avoid cynical withdrawal.",
        "friendly_numbers": [1, 3, 4, 5],
        "neutral_numbers": [2, 6],
        "enemy_numbers": [8],
        "favourable_days": ["Thursday", "Monday", "Tuesday"],
        "favourable_colours": ["Pastel Green", "Light Grey", "Lavender", "White", "Smoky Brown"],
        "colours_to_avoid": ["Jet Black", "Dark Navy"],
        "remedy_references": [
            "Feed stray dogs or birds daily.",
            "Practice silent breathwork or meditation in nature.",
            "Keep cat's eye, tiger's eye, or amethyst stone."
        ],
        "yantra_references": ["Ketu Yantra", "Matsya Yantra"],
        "methodology_id": "METH-VEDIC-001",
        "evidence_category": "Standard Classical Canon",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    8: {
        "number": 8,
        "root_number": 8,
        "type": "Single Digit / Root",
        "planet": "Saturn (Shani)",
        "alternative_planet": "Chronos / Karmic Judge",
        "element": "Earth",
        "core_characteristics": "Disciplined, persevering, structured, resilient, pragmatic, and compounding-oriented.",
        "strengths": ["Unshakeable endurance", "Mastery of long-term compounding", "Organizational stamina", "Impartial justice", "Institutional stewardship"],
        "challenges": ["Initial career delays", "Heavy early burdens", "Tendency toward pessimism or rigidity", "Reluctance to celebrate small wins"],
        "behavioural_tendencies": "Methodical, deliberate, works steadily through adversity, values tangible proof over promises.",
        "communication_tendencies": "Measured, serious, factual, low emotional display, emphasizes accountability.",
        "leadership_tendencies": "Institutional leadership; builds robust operational infrastructure, manages complex organizations with unbending discipline.",
        "creativity_and_analytical": "Operational optimization, supply chain efficiency, large-scale financial structuring, and structural engineering.",
        "relationship_interpretations": "Cautious entering relationships; once committed, exhibits rock-solid loyalty and enduring support.",
        "career_associations": [
            "Heavy Industry & Infrastructure", "Corporate Law & Compliance", "Operations & Supply Chain Management",
            "Mining, Metallurgy & Real Estate", "Accountancy & Auditing", "Civil Administration", "Institutional Banking"
        ],
        "business_interpretations": "Dominates asset-heavy industries, manufacturing, legal firms, long-cycle compounding, and governance.",
        "financial_themes": "Accumulates substantial wealth in mature years through patient compounding and frugal operational discipline.",
        "personal_development": "Celebrate incremental milestones; soften daily communication with warmth and empathetic understanding.",
        "friendly_numbers": [5, 6],
        "neutral_numbers": [3, 7],
        "enemy_numbers": [1, 2, 4, 8],
        "favourable_days": ["Saturday", "Wednesday", "Friday"],
        "favourable_colours": ["Dark Blue", "Navy Blue", "Charcoal", "Steel Grey", "Black (used mindfully)"],
        "colours_to_avoid": ["Bright Red", "Pure Golden Yellow"],
        "remedy_references": [
            "Support elderly, disabled, or labor-class individuals selflessly.",
            "Donate mustard oil, black sesame, or iron items on Saturdays.",
            "Feed black dogs or crows on Saturday mornings."
        ],
        "yantra_references": ["Shani Yantra", "Hanuman Yantra"],
        "methodology_id": "METH-VEDIC-001",
        "evidence_category": "Standard Classical Canon",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    9: {
        "number": 9,
        "root_number": 9,
        "type": "Single Digit / Root",
        "planet": "Mars (Mangal)",
        "alternative_planet": "Ares / Fiery Warrior",
        "element": "Fire",
        "core_characteristics": "Dynamic, courageous, humanitarian, passionate, decisive, and fiercely energetic.",
        "strengths": ["Boundless physical energy", "Protective valor", "Speed of execution", "Philanthropic compassion", "Decisive breakthrough power"],
        "challenges": ["Quick temper", "Impatience with weakness", "Risk of physical burnout", "Impulsive confrontations"],
        "behavioural_tendencies": "Bold, direct, thrives in active environments, champions the underdog, requires physical outlets for stamina.",
        "communication_tendencies": "Passionate, commanding, candid, speaks without filters, rallies others behind noble causes.",
        "leadership_tendencies": "Heroic frontline leadership; leads from the front lines in crises, inspires courage through personal example.",
        "creativity_and_analytical": "Direct visual and spatial impact, technical combat tactics, sports strategy, and transformative initiatives.",
        "relationship_interpretations": "Warm, passionate, and fiercely devoted; can be intense, needing a partner who values strength and honesty.",
        "career_associations": [
            "Armed Forces & Police Leadership", "Emergency & Trauma Medicine / Surgery", "Sports & Athletic Coaching",
            "Real Estate & Construction", "Manufacturing & Heavy Machinery", "Humanitarian NGOs", "Disaster Management"
        ],
        "business_interpretations": "Flourishes in fast-paced operational businesses, property development, defense supply, and health technology.",
        "financial_themes": "Earns rapidly through high energy; must guard against impulsive spending or aggressive speculative investments.",
        "personal_development": "Pause before responding in moments of anger; channel fire energy into vigorous exercise and selfless service.",
        "friendly_numbers": [1, 3, 5, 9],
        "neutral_numbers": [7],
        "enemy_numbers": [2, 4],
        "favourable_days": ["Tuesday", "Sunday"],
        "favourable_colours": ["Red", "Crimson", "Rose", "Coral", "Maroon"],
        "colours_to_avoid": ["Black", "Dark Navy", "Dark Green in Business"],
        "remedy_references": [
            "Maintain warm, respectful relations with siblings and colleagues.",
            "Donate blood or support emergency relief causes.",
            "Offer sweet items or donate red lentils (Masoor dal) on Tuesdays."
        ],
        "yantra_references": ["Mangal Yantra", "Bagalamukhi Yantra"],
        "methodology_id": "METH-VEDIC-001",
        "evidence_category": "Standard Classical Canon",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    # Master Numbers
    11: {
        "number": 11,
        "root_number": 2,
        "type": "Master Vibration (11/2)",
        "planet": "Moon / Neptune Hybrid",
        "element": "Water / Light",
        "core_characteristics": "Visionary illumination, spiritual intuition, magnetic inspiration, and profound empathy.",
        "strengths": ["Spiritual clarity", "High sensory antenna", "Inspirational charisma", "Connecting physical to metaphysical"],
        "challenges": ["Nervous tension", "Over-stimulation", "Self-doubt before stepping into leadership"],
        "friendly_numbers": [1, 2, 7],
        "enemy_numbers": [4, 8],
        "favourable_days": ["Monday", "Thursday"],
        "favourable_colours": ["Silver", "White", "Pale Violet"],
        "yantra_references": ["Shiva Yantra", "Chandra Yantra"],
        "methodology_id": "METH-CHALDEAN-001",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    22: {
        "number": 22,
        "root_number": 4,
        "type": "Master Builder (22/4)",
        "planet": "Rahu / Uranus Global",
        "element": "Earth / Structure",
        "core_characteristics": "Master architect, converting visionary dreams into enduring physical reality on a global scale.",
        "strengths": ["Macro-scale systems building", "Practical idealism", "Massive organizational capacity"],
        "challenges": ["Overwhelming weight of global responsibility", "Fear of failure", "Impatience with small minds"],
        "friendly_numbers": [1, 5, 6],
        "enemy_numbers": [2, 8],
        "favourable_days": ["Saturday", "Wednesday"],
        "favourable_colours": ["Cobalt Blue", "Platinum", "Electric Navy"],
        "yantra_references": ["Vishwakarma Yantra", "Ganesha Yantra"],
        "methodology_id": "METH-CHALDEAN-001",
        "version": "1.0.0",
        "status": "APPROVED"
    },
    33: {
        "number": 33,
        "root_number": 6,
        "type": "Master Teacher (33/6)",
        "planet": "Venus / Jupiter Divine Love",
        "element": "Ether / Heart",
        "core_characteristics": "Universal compassion, selfless mentorship, uplifting humanity through wisdom, healing, and art.",
        "strengths": ["Transformative healing presence", "Selfless devotion", "Masterful guidance of communities"],
        "challenges": ["Martyrdom complex", "Neglecting personal needs for others", "Emotional exhaustion"],
        "friendly_numbers": [3, 6, 9],
        "enemy_numbers": [3],
        "favourable_days": ["Friday", "Thursday"],
        "favourable_colours": ["Diamond White", "Golden Rose", "Sky Azure"],
        "yantra_references": ["Shri Yantra", "Maha Mrityunjaya Yantra"],
        "methodology_id": "METH-CHALDEAN-001",
        "version": "1.0.0",
        "status": "APPROVED"
    }
}


def get_number_profile(num: int) -> Optional[Dict[str, Any]]:
    """Retrieves full number characteristics profile from the registry."""
    if num in NUMBER_REGISTRY:
        return NUMBER_REGISTRY[num]
    
    # Check Cheiro compound dataset for 10-52
    if 10 <= num <= 52 and num in CHEIRO_DATASET:
        cheiro_info = CHEIRO_DATASET[num]
        root = cheiro_info.get("output_number") or cheiro_info.get("output_num") or sum(int(d) for d in str(num))
        while root > 9:
            root = sum(int(d) for d in str(root))
        root_profile = NUMBER_REGISTRY.get(root, {})
        arch = cheiro_info.get("input_compound_archetype") or cheiro_info.get("archetype") or f"Compound {num}"
        char_desc = cheiro_info.get("input_characteristics") or cheiro_info.get("characteristics") or ""
        
        return {
            "number": num,
            "root_number": root,
            "type": f"Compound Archetype: {arch}",
            "planet": root_profile.get("planet"),
            "core_characteristics": char_desc,
            "archetype_title": arch,
            "strengths": root_profile.get("strengths", []),
            "challenges": root_profile.get("challenges", []),
            "friendly_numbers": root_profile.get("friendly_numbers", []),
            "enemy_numbers": root_profile.get("enemy_numbers", []),
            "favourable_colours": root_profile.get("favourable_colours", []),
            "favourable_days": root_profile.get("favourable_days", []),
            "yantra_references": root_profile.get("yantra_references", []),
            "methodology_id": "METH-CHEIRO-001",
            "version": "1.0.0",
            "status": "APPROVED"
        }
    
    # Generic reduction fallback for > 52
    root = sum(int(d) for d in str(num))
    while root > 9:
        root = sum(int(d) for d in str(root))
    return NUMBER_REGISTRY.get(root)


def get_relationship_status(num1: int, num2: int) -> str:
    """
    Returns 'FRIENDLY', 'ENEMY', or 'NEUTRAL' relationship between two root numbers.
    Guarantees deterministic, unified output across all engines.
    """
    # Reduce to roots
    r1 = num1 if num1 <= 9 else sum(int(d) for d in str(num1))
    while r1 > 9: r1 = sum(int(d) for d in str(r1))
    
    r2 = num2 if num2 <= 9 else sum(int(d) for d in str(num2))
    while r2 > 9: r2 = sum(int(d) for d in str(r2))
    
    p1 = NUMBER_REGISTRY.get(r1)
    if not p1:
        return "NEUTRAL"
    
    if r2 in p1.get("friendly_numbers", []):
        return "FRIENDLY"
    elif r2 in p1.get("enemy_numbers", []):
        return "ENEMY"
    else:
        return "NEUTRAL"


def get_relationship(num1: int, num2: int) -> Dict[str, Any]:
    """Convenience helper returning structured relationship dict."""
    status = get_relationship_status(num1, num2)
    # Map to Title Case (Friend, Enemy, Neutral)
    label = "Friend" if status == "FRIENDLY" else ("Enemy" if status == "ENEMY" else "Neutral")
    return {
        "num1": num1,
        "num2": num2,
        "status": status,
        "relationship": label,
        "is_friendly": status == "FRIENDLY",
        "is_enemy": status == "ENEMY",
        "is_neutral": status == "NEUTRAL"
    }


PLANETARY_RULERS = {
    n: {"planet": NUMBER_REGISTRY[n]["planet"], "element": NUMBER_REGISTRY[n].get("element", "")}
    for n in range(1, 10) if n in NUMBER_REGISTRY
}


# ── Numeros Vision Classical Methodology DAY 6 CANONICAL SUB-DATE & NUMBER CHARACTERISTICS ────
# Source: Master Numerology with Numeros Vision Classical Methodology - DAY 6 (Numeros Vision)
BIRTH_DAY_SUBDATE_REGISTRY: Dict[int, Dict[str, Any]] = {
    # ── ROOT 1: SUN (SURYA) ───────────────────────────────────────────────────
    1: {
        "day": 1, "root": 1, "code": "1(b)", "tier": "b",
        "planet": "Sun (Surya)", "is_karmic": False, "is_master": False,
        "keywords": ["King like", "Authoritative", "Pioneers", "Royal", "Trend setters", "Leadership", "Ego"],
        "essence": "Pure Solar vibration. Natural executive authority, original creative pioneer, sovereign trendsetter. Thrives in autonomous leadership roles."
    },
    10: {
        "day": 10, "root": 1, "code": "10(b)", "tier": "b",
        "planet": "Sun (Surya)", "is_karmic": True, "is_master": False,
        "keywords": ["King like", "Authoritative", "Pioneers", "Royal", "Trend setters", "Leadership", "Ego", "Karmic 10"],
        "essence": "Karmic Number 10 (Wheel of Fortune). Zero-amplified Solar power. Rises from grassroots to high executive authority; cycles of sudden karmic elevation."
    },
    19: {
        "day": 19, "root": 1, "code": "19(a)", "tier": "a",
        "planet": "Sun (Surya)", "is_karmic": True, "is_master": False,
        "keywords": ["King like", "Authoritative", "Pioneers", "Royal", "Trend setters", "Leadership", "Ego", "Karmic 19", "Alpha Power"],
        "essence": "Karmic Number 19 (Prince of Heaven). Sun (1) + Mars (9). Highest executive drive, intense royal ambition, fearless trendsetter. Must master ego patience to retain sovereign gains."
    },
    28: {
        "day": 28, "root": 1, "code": "28(c)", "tier": "c",
        "planet": "Sun (Surya)", "is_karmic": False, "is_master": False,
        "keywords": ["King like", "Authoritative", "Pioneers", "Royal", "Trend setters", "Leadership", "Ego", "Endurance"],
        "essence": "Moon (2) + Saturn (8) resolving into Sun (10=1). Emotional resilience and structural labor; early career struggle transforms into formidable, enduring executive leadership."
    },

    # ── ROOT 2: MOON (CHANDRA) ────────────────────────────────────────────────
    2: {
        "day": 2, "root": 2, "code": "2(b)", "tier": "b",
        "planet": "Moon (Chandra)", "is_karmic": False, "is_master": False,
        "keywords": ["Emotional", "Gentle", "Slow", "Sensitive", "Attractive", "Intuitive", "Sensitive mood swings"],
        "essence": "Pure Lunar vibration. Deep emotional empathy, attractive magnetic gentleness, intuitive diplomacy. Requires supportive environments to counter sensitive mood swings."
    },
    11: {
        "day": 11, "root": 2, "code": "11(a)", "tier": "a",
        "planet": "Moon (Chandra)", "is_karmic": False, "is_master": True,
        "keywords": ["Emotional", "Gentle", "Sensitive", "Attractive", "Intuitive", "Master Number 11", "Spiritual Vision", "Mood swings"],
        "essence": "Master Number 11 (The Spiritual Illuminator). Double Sun (1-1) channeling Moon. High spiritual vision, intense intuition, charismatic counselor. Can suffer from acute mood swings without daily grounding."
    },
    20: {
        "day": 20, "root": 2, "code": "20(b)", "tier": "b",
        "planet": "Moon (Chandra)", "is_karmic": False, "is_master": False,
        "keywords": ["Emotional", "Gentle", "Slow", "Sensitive", "Attractive", "Intuitive", "Introspective"],
        "essence": "Moon (2) reinforced by Zero. Deep contemplative sensitivity, gentle peacemaker, artistic and poetic imagination. Flourishes in low-stress, emotionally safe spaces."
    },
    29: {
        "day": 29, "root": 2, "code": "29(c)", "tier": "c",
        "planet": "Moon (Chandra)", "is_karmic": False, "is_master": False,
        "keywords": ["Emotional", "Gentle", "Sensitive", "Attractive", "Intuitive", "Passionate", "Intense mood swings"],
        "essence": "Moon (2) + Mars (9) resolving into 11/2. High emotional intensity, passionate intuition, fiercely protective. Emotional volatility and sudden mood swings require disciplined mindfulness."
    },

    # ── ROOT 3: JUPITER (GURU) ────────────────────────────────────────────────
    3: {
        "day": 3, "root": 3, "code": "3(c)", "tier": "c",
        "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
        "keywords": ["Imaginative", "Healer", "Preacher", "Spiritual", "Religious", "Counselor"],
        "essence": "Pure Jupiterian wisdom. Expansive creative imagination, inspirational storyteller, natural counselor and teacher. Uplifts others through moral and spiritual guidance."
    },
    12: {
        "day": 12, "root": 3, "code": "12(a)", "tier": "a",
        "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
        "keywords": ["Imaginative", "Healer", "Preacher", "Spiritual", "Religious", "Counselor", "Diplomatic Speaker"],
        "essence": "Sun (1) + Moon (2) resolving into Jupiter (3). Executive clarity blended with emotional diplomacy. Highly persuasive orator, ethical preacher, and trusted institutional counselor."
    },
    21: {
        "day": 21, "root": 3, "code": "21(b)", "tier": "b",
        "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
        "keywords": ["Imaginative", "Healer", "Preacher", "Spiritual", "Religious", "Counselor", "Crown of Magi"],
        "essence": "Moon (2) + Sun (1) resolving into Jupiter (3). The Crown of the Magi. Magnetic communicative grace, popular social standing, successful counselor and artistic creator."
    },
    30: {
        "day": 30, "root": 3, "code": "30(c)", "tier": "c",
        "planet": "Jupiter (Guru)", "is_karmic": False, "is_master": False,
        "keywords": ["Imaginative", "Healer", "Preacher", "Spiritual", "Religious", "Counselor", "Philosophical"],
        "essence": "Jupiter (3) + Zero. High philosophical and spiritual contemplation, deep healer, visionary artist. Disfavors petty commercial materialism."
    },

    # ── ROOT 4: RAHU (NORTH NODE) ─────────────────────────────────────────────
    4: {
        "day": 4, "root": 4, "code": "4(c)", "tier": "c",
        "planet": "Rahu", "is_karmic": False, "is_master": False,
        "keywords": ["Disciplined", "Organized", "Short tempered", "Rebellious", "Abusive/Stubborn", "Logical impulsive"],
        "essence": "Pure Rahu frequency. Highly organized systems architect, rigorous discipline, unconventional problem-solver. Prone to sudden impatience, stubborn rebelliousness, or impulsive outbursts."
    },
    13: {
        "day": 13, "root": 4, "code": "13(d)", "tier": "d",
        "planet": "Rahu", "is_karmic": True, "is_master": False,
        "keywords": ["Disciplined", "Organized", "Short tempered", "Rebellious", "Stubborn", "Logical impulsive", "Karmic 13"],
        "essence": "Karmic Debt Number 13 (The Karmic Architect). Sun (1) + Jupiter (3) under Rahu. Heavy early trials, demanding hard labor, short-tempered impatience; transforms through relentless discipline into monumental success."
    },
    22: {
        "day": 22, "root": 4, "code": "22(a)", "tier": "a",
        "planet": "Rahu", "is_karmic": False, "is_master": True,
        "keywords": ["Disciplined", "Organized", "Master Number 22", "Master Builder", "Global Vision", "Systemic Scale"],
        "essence": "Master Number 22 (The Master Builder). Double Moon (2-2) channeling Rahu. Extraordinary systemic mastery, organizes colossal enterprises, practical genius of international scale."
    },
    31: {
        "day": 31, "root": 4, "code": "31(b)", "tier": "b",
        "planet": "Rahu", "is_karmic": False, "is_master": False,
        "keywords": ["Disciplined", "Organized", "Rebellious", "Logical impulsive", "Shrewd Strategist"],
        "essence": "Jupiter (3) + Sun (1) resolving into Rahu (4). Visionary strategic planner, highly methodical, rebellious against slow bureaucracy, builds enduring commercial structures."
    },

    # ── ROOT 5: MERCURY (BUDH) ────────────────────────────────────────────────
    5: {
        "day": 5, "root": 5, "code": "5(c)", "tier": "c",
        "planet": "Mercury (Budh)", "is_karmic": False, "is_master": False,
        "keywords": ["Happy go lucky", "Lazy", "Dark horse", "Entertaining", "Communicative"],
        "essence": "Pure Mercury. Jovial, happy-go-lucky charisma, swift commercial communication, entertaining presence. Can show temporary laziness or procrastination until sudden dark-horse breakthroughs."
    },
    14: {
        "day": 14, "root": 5, "code": "14(a)", "tier": "a",
        "planet": "Mercury (Budh)", "is_karmic": True, "is_master": False,
        "keywords": ["Happy go lucky", "Dark horse", "Entertaining", "Communicative", "Karmic 14", "Adaptable"],
        "essence": "Karmic Debt Number 14 (The River of Change). Sun (1) + Rahu (4) under Mercury (5). Highly magnetic dark horse, brilliant communicator. Must balance love of freedom with emotional self-control."
    },
    23: {
        "day": 23, "root": 5, "code": "23(b)", "tier": "b",
        "planet": "Mercury (Budh)", "is_karmic": False, "is_master": False,
        "keywords": ["Happy go lucky", "Dark horse", "Entertaining", "Communicative", "Royal Star of Lion", "Supreme Charm"],
        "essence": "Moon (2) + Jupiter (3) resolving into Mercury (5). Royal Star of the Lion. Highest commercial charm, effortless communication, captivating entertainer, unfailingly attracts high patronage."
    },

    # ── ROOT 6: VENUS (SHUKRA) ────────────────────────────────────────────────
    6: {
        "day": 6, "root": 6, "code": "6(b)", "tier": "b",
        "planet": "Venus (Shukra)", "is_karmic": False, "is_master": False,
        "keywords": ["Romantic", "Communicator", "Manipulative/Diplomatic", "Family oriented", "Shrewd"],
        "essence": "Pure Venusian luxury. Highly romantic, magnetic communicator, deeply family-oriented, shrewd aesthetic and commercial negotiator. Masters social diplomacy."
    },
    15: {
        "day": 15, "root": 6, "code": "15(a)", "tier": "a",
        "planet": "Venus (Shukra)", "is_karmic": False, "is_master": False,
        "keywords": ["Romantic", "Communicator", "Manipulative/Diplomatic", "Family oriented", "Shrewd", "Magnetic Charisma"],
        "essence": "Sun (1) + Mercury (5) resolving into Venus (6). Hypnotic communicator, shrewd dealmaker, magnetic social standing, luxurious family lifestyle."
    },
    24: {
        "day": 24, "root": 6, "code": "24(c)", "tier": "c",
        "planet": "Venus (Shukra)", "is_karmic": False, "is_master": False,
        "keywords": ["Romantic", "Communicator", "Family oriented", "Diplomatic", "Shrewd Caretaker"],
        "essence": "Moon (2) + Rahu (4) resolving into Venus (6). Deep domestic devotion, shrewd protector of family interests, diplomatic mediator in partnerships."
    },

    # ── ROOT 7: KETU (SOUTH NODE) ─────────────────────────────────────────────
    7: {
        "day": 7, "root": 7, "code": "7(c)", "tier": "c",
        "planet": "Ketu", "is_karmic": False, "is_master": False,
        "keywords": ["Low in confidence (youth)", "Inquisitive", "Very good healer occult", "Spiritual religious", "Researcher", "Introvert"],
        "essence": "Pure Ketu vibration. Deeply inquisitive, introspective researcher, exceptional occult and spiritual healer. Overcomes early lack of confidence to become profound truth-seeker."
    },
    16: {
        "day": 16, "root": 7, "code": "16(a)", "tier": "a",
        "planet": "Ketu", "is_karmic": True, "is_master": False,
        "keywords": ["Inquisitive", "Very good healer occult", "Spiritual religious", "Researcher", "Introvert", "Karmic 16", "Shattered Citadel"],
        "essence": "Karmic Debt Number 16 (The Shattered Citadel). Sun (1) + Venus (6) under Ketu. Early disillusionments strip away false ego, unlocking extraordinary healing, occult mastery, and spiritual wisdom."
    },
    25: {
        "day": 25, "root": 7, "code": "25(b)", "tier": "b",
        "planet": "Ketu", "is_karmic": False, "is_master": False,
        "keywords": ["Inquisitive", "Very good healer occult", "Spiritual religious", "Researcher", "Introvert", "Analytical Insight"],
        "essence": "Moon (2) + Mercury (5) resolving into Ketu (7). Brilliant analytical intellect, deep intuitive researcher, gifted occult diagnostic counselor, quiet introspective strength."
    },

    # ── ROOT 8: SATURN (SHANI) ────────────────────────────────────────────────
    8: {
        "day": 8, "root": 8, "code": "8(a)", "tier": "a",
        "planet": "Saturn (Shani)", "is_karmic": False, "is_master": False,
        "keywords": ["Struggle", "Laborious", "Hardwork", "Logical", "Argumentative", "Stubborn", "Law", "Finance"],
        "essence": "Pure Saturnian crucible. Early struggle, laborious hard work, highly logical and argumentative mind, master of law, structural governance, and large-scale compounding finance."
    },
    17: {
        "day": 17, "root": 8, "code": "17(b)", "tier": "b",
        "planet": "Saturn (Shani)", "is_karmic": False, "is_master": False,
        "keywords": ["Struggle", "Hardwork", "Logical", "Law", "Finance", "Star of Magi", "Enduring Victory"],
        "essence": "Star of the Magi. Sun (1) + Ketu (7) resolving into Saturn (8). Overcomes early karmic obstacles through spiritual insight; achieves monumental financial and institutional authority."
    },
    26: {
        "day": 26, "root": 8, "code": "26(c)", "tier": "c",
        "planet": "Saturn (Shani)", "is_karmic": False, "is_master": False,
        "keywords": ["Struggle", "Laborious", "Hardwork", "Logical", "Family Duty", "Law", "Finance"],
        "essence": "Moon (2) + Venus (6) resolving into Saturn (8). Heavy family and partnership duties; laborious financial perseverance culminates in solid material and real estate foundations."
    },

    # ── ROOT 9: MARS (MANGAL) ─────────────────────────────────────────────────
    9: {
        "day": 9, "root": 9, "code": "9(a)", "tier": "a",
        "planet": "Mars (Mangal)", "is_karmic": False, "is_master": False,
        "keywords": ["Unpredictable behaviour", "Warrior rough n tough", "Good humanitarian", "Egotistic"],
        "essence": "Pure Mars energy. Fearless, rough-and-tough warrior, unpredictable outbursts, noble humanitarian protector. Driven by high passion and righteous defense of others."
    },
    18: {
        "day": 18, "root": 9, "code": "18(c)", "tier": "c",
        "planet": "Mars (Mangal)", "is_karmic": False, "is_master": False,
        "keywords": ["Unpredictable behaviour", "Warrior rough n tough", "Good humanitarian", "Egotistic", "Trials of Strength"],
        "essence": "Sun (1) + Saturn (8) resolving into Mars (9). Intense conflict between executive will and karmic trials. Warrior resilience forged in adversity; champions massive humanitarian causes."
    },
    27: {
        "day": 27, "root": 9, "code": "27(b)", "tier": "b",
        "planet": "Mars (Mangal)", "is_karmic": False, "is_master": False,
        "keywords": ["Warrior rough n tough", "Good humanitarian", "Intuitive Protector", "Commanding"],
        "essence": "The Sceptre. Moon (2) + Ketu (7) resolving into Mars (9). Intuitive spiritual warrior, rough-and-tough integrity, commanding protector, combines strategic detachment with bold action."
    }
}
# ?? Numeros Vision Classical Methodology DAY 6 CANONICAL SUB-DATE & NUMBER CHARACTERISTICS ????
# Canonical sub-date registry loaded deterministically from app/data/birth_subdates_registry.json.
# Defines Categories A (Good), B (Normal), C (Lower), D (Karmic Debt) for all 31 birth days.

STRENGTH_CATEGORY_DEFINITIONS = {
    "A": {
        "grade": "Category A — Good Strength (High Potency / Direct Manifestation)",
        "potency_range": "88% – 96% Intrinsic Ease",
        "definition": "High vibrational ease, strong inherent manifestation power, royal or visionary drive. Requires conscious humility to prevent ego friction.",
        "days": ["19(a)", "11(a)", "12(a)", "22(a)", "14(a)", "15(a)", "16(a)", "8(a)", "9(a)"]
    },
    "B": {
        "grade": "Category B — Normal Strength (Balanced / Steady Growth)",
        "potency_range": "72% – 84% Potency",
        "definition": "Balanced, workable potency. Success compounds through steady effort, disciplined partnership, and emotional grounding.",
        "days": ["1(b)", "10(b)", "2(b)", "20(b)", "21(b)", "31(b)", "23(b)", "6(b)", "25(b)", "17(b)", "27(b)"]
    },
    "C": {
        "grade": "Category C — Lower Strength (High Friction / Intensive Lesson)",
        "potency_range": "52% – 68% Direct Ease",
        "definition": "Challenging compound tension, contradictory planetary elements, or initial inertia. Demands patience, elemental remedies, and structured routine.",
        "days": ["28(c)", "29(c)", "3(c)", "30(c)", "4(c)", "5(c)", "24(c)", "7(c)", "26(c)", "18(c)"]
    },
    "D": {
        "grade": "Category D — Karmic Debt Transformation (Intense Crucible)",
        "potency_range": "58% Initial Ease jumping to 92% Post-Mastery",
        "definition": "Rigorous karmic crucible requiring physical discipline and perseverance without shortcuts. Turns trials into master-builder foundations.",
        "days": ["13(d)"]
    }
}

import json as _json
import os as _os

def _load_subdates_registry():
    _p = _os.path.join(_os.path.dirname(__file__), "..", "data", "birth_subdates_registry.json")
    _p = _os.path.normpath(_p)
    with open(_p, "r", encoding="utf-8") as _f:
        _d = _json.load(_f)
    return {int(k): v for k, v in _d.items()}

BIRTH_DAY_SUBDATE_REGISTRY = _load_subdates_registry()
