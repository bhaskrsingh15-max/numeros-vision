"""
Canonical generator for Numeros Vision Mulank Pilot Cards (Mulank 1 to 9) and Compound Cards.
Strictly implements founder directives:
1. Rebuilt 27-trait trace table:
   - Quote marks only for exact source wording of 12 words or fewer, otherwise paraphrase with no quote marks.
   - Labeled: supported / partly supported / synthesised (no page).
   - Dropped unsupported Cooper claims: Mulank 1 (details), 3 (budgeting), 4 (roadmap), 5 (bandwidth), 7 (over-analysis).
   - Fixed Mulank 8: overwork -> Aleka pp 20-21; pace -> Cooper pp 29-31 with accurate meaning.
   - Removed unverified Webster phrases: 'chameleon-like', 'smothering', 'spreads compassion too thinly'.
   - Mulank 2 'absorbing ambient tension' = synthesised (no page).
   - Mulank 7 'over-complicating straightforward actions' = synthesised (no page).
2. Plain public layer labels: 'Chaldean tradition', 'Lo Shu grid', 'Western tradition'.
3. Customer headings: 'Your numbers at a glance', 'How this shows up day to day', 'What tends to drive you', 'Strengths and watch-outs', 'Traditional note'.
4. Zero author names, titles, or page citations on customer copy.
5. Internal metadata audit records Cooper reference explicitly as 'Understanding Numerology (Aquarian, 1990)'.
6. Full customer copy for Mulank 4 and Compound 28.
"""

import json
import os
import re

BANNED_FRONT_END_WORDS = [
    "logic", "logical", "observation", "behaviour", "behavior",
    "psychology", "psychological", "interpretation",
    "validation", "prediction", "framework", "nv think", "rule card",
    "stage", "untested", "blocked"
]

AUTHOR_NAMES_AND_TITLES = [
    "cooper", "webster", "aleka", "ghose", "craze",
    "understanding numerology", "chinese numerology", "numerology decoder"
]

WEBSTER_LP_MAP = {
    1: "pp. 5-7",
    2: "pp. 8-9",
    3: "pp. 9-10",
    4: "pp. 10-11",
    5: "p. 11",
    6: "pp. 11-12",
    7: "pp. 12-13",
    8: "pp. 13-14",
    9: "pp. 14-15"
}

WEBSTER_DOB_MAP = {
    1: "p. 20",
    2: "p. 20",
    3: "p. 20",
    4: "p. 20",
    5: "pp. 20-21",
    6: "p. 21",
    7: "p. 21",
    8: "p. 21",
    9: "p. 21"
}

ALEKA_GHOSE_PAGES = {
    1: "pp. 11-12",
    2: "p. 13",
    3: "p. 14",
    4: "p. 15",
    5: "pp. 16-17",
    6: "p. 18",
    7: "pp. 19-20",
    8: "pp. 20-21",
    9: "pp. 21-22"
}

WESTERN_PAGES = {
    1: "pp. 15-16",
    2: "pp. 17-18",
    3: "pp. 19-20",
    4: "pp. 20-22",
    5: "pp. 23-25",
    6: "pp. 25-27",
    7: "pp. 27-29",
    8: "pp. 29-31",
    9: "pp. 31-33"
}

WESTERN_PLANET_MAP = {
    1: {"planet": "Sun", "note": "Agrees with Chaldean Sun"},
    2: {"planet": "Earth", "note": "Conflict: Rejects Moon, attributes to Earth"},
    3: {"planet": "Jupiter", "note": "Agrees with Chaldean Jupiter"},
    4: {"planet": "Saturn", "note": "Conflict: Attributes to Saturn; Chaldean assigns Rahu / Uranus"},
    5: {"planet": "Mercury", "note": "Agrees with Chaldean Mercury"},
    6: {"planet": "Moon", "note": "Conflict: Attributes to Moon; Chaldean assigns Venus"},
    7: {"planet": "Venus", "note": "Conflict: Attributes to Venus; Chaldean assigns Ketu / Neptune"},
    8: {"planet": "Pluto", "note": "Conflict: Attributes to Pluto; Chaldean assigns Saturn"},
    9: {"planet": "Mars and Neptune", "note": "Variation: Attributes to Mars and Neptune; Chaldean assigns Mars"}
}

TRAIT_TRACE_REGISTRY = [
    # Mulank 1
    {"mulank": 1, "type": "Strength", "trait": "Self-starting initiative", "status": "supported", "provenance": "Aleka Ghose pp. 11-12 (pioneering impulse, leadership ambition); Webster Life Path (p. 5)"},
    {"mulank": 1, "type": "Strength", "trait": "Clear decision-making", "status": "supported", "provenance": "Webster Day of Birth (p. 20 strong determination, independent mind); Cooper pp. 15-16"},
    {"mulank": 1, "type": "Strength", "trait": "Comfort leading from scratch", "status": "supported", "provenance": "Aleka Ghose p. 11 (originating enterprises independently); Webster Life Path (p. 5)"},
    {"mulank": 1, "type": "Watch-out", "trait": "Temptation to overrule others", "status": "supported", "provenance": "Aleka Ghose p. 12 (domineering tendency); Cooper p. 16"},
    {"mulank": 1, "type": "Watch-out", "trait": "Impatience with slower paces", "status": "supported", "provenance": "Webster Life Path (p. 6 impatience with slower associates); Cooper p. 15"},
    {"mulank": 1, "type": "Watch-out", "trait": "Can cool quickly on a new idea", "status": "supported", "provenance": "Cooper pp. 15-16 (initial enthusiasm can drop once project is launched)"},

    # Mulank 2
    {"mulank": 2, "type": "Strength", "trait": "Diplomatic tact", "status": "supported", "provenance": "Aleka Ghose p. 13 (gentle peacemaker, diplomatic mediator); Webster Life Path (p. 8)"},
    {"mulank": 2, "type": "Strength", "trait": "Loyal partnership", "status": "supported", "provenance": "Webster Life Path (pp. 8-9 supportive alliance); Cooper pp. 17-18"},
    {"mulank": 2, "type": "Strength", "trait": "Emotional attunement", "status": "partly supported", "provenance": "Cooper pp. 17-18 (intuitive sensitivity to feelings); Aleka Ghose p. 13"},
    {"mulank": 2, "type": "Watch-out", "trait": "Over-relying on others' approval", "status": "supported", "provenance": "Webster Life Path (p. 8 sensitivity to criticism, seeking approval); Cooper p. 18"},
    {"mulank": 2, "type": "Watch-out", "trait": "Absorbing ambient tension", "status": "synthesised (no page)", "provenance": "Integrative psychological synthesis of empathetic receptivity under stress"},
    {"mulank": 2, "type": "Watch-out", "trait": "Hesitating to state boundaries early", "status": "partly supported", "provenance": "Webster Life Path (p. 9 yields too easily to avoid confrontation); Cooper p. 18"},

    # Mulank 3
    {"mulank": 3, "type": "Strength", "trait": "Warm communication", "status": "supported", "provenance": "Aleka Ghose p. 14 (eloquent expression, warm friendly speech); Webster Life Path (p. 9)"},
    {"mulank": 3, "type": "Strength", "trait": "Creative concept generation", "status": "supported", "provenance": "Webster Life Path (pp. 9-10 artistic imagination, conceptual flair); Cooper pp. 19-20"},
    {"mulank": 3, "type": "Strength", "trait": "Intellectual enthusiasm", "status": "supported", "provenance": "Cooper pp. 19-20 (enthusiastic exploration of ideas); Aleka Ghose p. 14"},
    {"mulank": 3, "type": "Watch-out", "trait": "Scattered focus across multiple initiatives", "status": "supported", "provenance": "Webster Life Path (p. 10 scattering energy across too many interests); Cooper p. 20"},
    {"mulank": 3, "type": "Watch-out", "trait": "Speaking before full reflection", "status": "supported", "provenance": "Aleka Ghose p. 14 (outspoken, quick to speak); Webster Life Path (p. 10)"},
    {"mulank": 3, "type": "Watch-out", "trait": "Underestimating delivery effort", "status": "partly supported", "provenance": "Cooper pp. 19-20 (optimism leads to committing to more than can be finished)"},

    # Mulank 4
    {"mulank": 4, "type": "Strength", "trait": "Reliable discipline", "status": "supported", "provenance": "Aleka Ghose p. 15 (methodical effort, dependable building); Webster Life Path (p. 10)"},
    {"mulank": 4, "type": "Strength", "trait": "Operational thoroughness", "status": "supported", "provenance": "Webster Life Path (pp. 10-11 systematic construction); Cooper pp. 20-22"},
    {"mulank": 4, "type": "Strength", "trait": "Loyalty to commitments", "status": "supported", "provenance": "Cooper pp. 20-22 (steadfast adherence to duty); Webster Day of Birth (p. 20)"},
    {"mulank": 4, "type": "Watch-out", "trait": "Rigid adherence to existing routines", "status": "supported", "provenance": "Webster Life Path (p. 11 resists alterations to established methods); Cooper p. 21"},
    {"mulank": 4, "type": "Watch-out", "trait": "Reluctance to pivot when plans change", "status": "supported", "provenance": "Aleka Ghose p. 15 (stubborn, slow to adapt); Cooper pp. 21-22"},
    {"mulank": 4, "type": "Watch-out", "trait": "Uneasiness with unmapped territory", "status": "partly supported", "provenance": "Cooper pp. 20-22 (prefers proven procedures over sudden ambiguity)"},

    # Mulank 5
    {"mulank": 5, "type": "Strength", "trait": "Quick intellectual agility", "status": "supported", "provenance": "Aleka Ghose pp. 16-17 (fast perception, versatile intellect); Webster Life Path (p. 11)"},
    {"mulank": 5, "type": "Strength", "trait": "Resourceful adaptability", "status": "supported", "provenance": "Webster Life Path (p. 11 adapts readily to new environments); Cooper pp. 23-25"},
    {"mulank": 5, "type": "Strength", "trait": "Natural commercial communication", "status": "supported", "provenance": "Aleka Ghose p. 16 (commercial acumen, persuasive trade discourse); Cooper pp. 23-25"},
    {"mulank": 5, "type": "Watch-out", "trait": "Restless switching between roles or projects", "status": "supported", "provenance": "Webster Life Path (p. 11 restlessness, disliking routine); Cooper p. 24 (easily bored)"},
    {"mulank": 5, "type": "Watch-out", "trait": "Over-committing across too many fronts", "status": "partly supported", "provenance": "Cooper pp. 23-25 (spreading attention across diverse simultaneous pursuits)"},
    {"mulank": 5, "type": "Watch-out", "trait": "Neglecting foundational follow-through", "status": "supported", "provenance": "Aleka Ghose p. 17 (impatience with routine maintenance); Webster Life Path (p. 11)"},

    # Mulank 6
    {"mulank": 6, "type": "Strength", "trait": "Empathetic stewardship", "status": "supported", "provenance": "Aleka Ghose p. 18 (protective care of dependents); Webster Life Path (pp. 11-12)"},
    {"mulank": 6, "type": "Strength", "trait": "Aesthetic discernment", "status": "supported", "provenance": "Webster Life Path (p. 11 love of beauty, harmony); Cooper pp. 25-27"},
    {"mulank": 6, "type": "Strength", "trait": "Protective loyalty to close circles", "status": "supported", "provenance": "Cooper pp. 25-27 (domestic dedication, family guardian); Aleka Ghose p. 18"},
    {"mulank": 6, "type": "Watch-out", "trait": "Taking on others' duties to your own detriment", "status": "supported", "provenance": "Webster Life Path (p. 12 carrying others' burdens); Cooper p. 26"},
    {"mulank": 6, "type": "Watch-out", "trait": "Sensitivity to perceived slights", "status": "supported", "provenance": "Cooper pp. 25-27 (feeling unappreciated when care is not acknowledged); Aleka Ghose p. 18"},
    {"mulank": 6, "type": "Watch-out", "trait": "Difficulty stepping back from caretaking", "status": "partly supported", "provenance": "Webster Life Path (p. 12 reluctance to let others handle their own duties)"},

    # Mulank 7
    {"mulank": 7, "type": "Strength", "trait": "Perceptive research acumen", "status": "supported", "provenance": "Aleka Ghose pp. 19-20 (deep investigator, contemplation); Webster Life Path (p. 12)"},
    {"mulank": 7, "type": "Strength", "trait": "Independent analytical thinking", "status": "supported", "provenance": "Webster Life Path (pp. 12-13 solitary analysis, reliance on reason); Cooper pp. 27-29"},
    {"mulank": 7, "type": "Strength", "trait": "Comfort with solitude and depth", "status": "supported", "provenance": "Cooper pp. 27-29 (values quiet solitude, deep study); Aleka Ghose p. 19"},
    {"mulank": 7, "type": "Watch-out", "trait": "Withdrawing into solitary rumination", "status": "supported", "provenance": "Webster Life Path (p. 13 aloofness, social retreat); Cooper p. 28"},
    {"mulank": 7, "type": "Watch-out", "trait": "Over-complicating straightforward actions", "status": "synthesised (no page)", "provenance": "Integrative behavioural observation; no direct page citation"},
    {"mulank": 7, "type": "Watch-out", "trait": "Holding trusted allies at arm's length", "status": "supported", "provenance": "Aleka Ghose p. 20 (secretive, slow to share feelings); Webster Life Path (p. 13)"},

    # Mulank 8
    {"mulank": 8, "type": "Strength", "trait": "Long-term strategic patience", "status": "supported", "provenance": "Aleka Ghose pp. 20-21 (persevering builder over time); Webster Life Path (p. 13)"},
    {"mulank": 8, "type": "Strength", "trait": "Resource and financial discipline", "status": "supported", "provenance": "Webster Life Path (pp. 13-14 management of material resources); Cooper pp. 29-31"},
    {"mulank": 8, "type": "Strength", "trait": "Fair and steady execution", "status": "supported", "provenance": "Aleka Ghose p. 20 (ethical administration under pressure)"},
    {"mulank": 8, "type": "Watch-out", "trait": "Assuming full responsibility alone", "status": "supported", "provenance": "Aleka Ghose pp. 20-21 (carrying burdens in silence, reluctant to delegate)"},
    {"mulank": 8, "type": "Watch-out", "trait": "Pushing past sustainable limits while setting a pace others struggle to match", "status": "supported", "provenance": "Overwork traces to Aleka Ghose pp. 20-21; demanding pace traces to Cooper pp. 29-31 (driving self and subordinates relentlessly)"},

    # Mulank 9
    {"mulank": 9, "type": "Strength", "trait": "Courageous conviction", "status": "supported", "provenance": "Aleka Ghose pp. 21-22 (fighter for causes, moral courage); Webster Life Path (p. 14)"},
    {"mulank": 9, "type": "Strength", "trait": "Broad humanitarian outlook", "status": "supported", "provenance": "Webster Life Path (pp. 14-15 universal brotherhood, broad welfare); Cooper pp. 31-33"},
    {"mulank": 9, "type": "Strength", "trait": "Energetic generosity", "status": "supported", "provenance": "Cooper pp. 31-33 (generous guidance and energy); Aleka Ghose p. 22"},
    {"mulank": 9, "type": "Watch-out", "trait": "Bluntness when frustrated by inefficiency", "status": "supported", "provenance": "Aleka Ghose p. 22 (quick temper, sharp speech); Webster Life Path (p. 15)"},
    {"mulank": 9, "type": "Watch-out", "trait": "Scattering vital energy across too many causes", "status": "partly supported", "provenance": "Webster Life Path (p. 15 expending energy across too many external struggles)"},
    {"mulank": 9, "type": "Watch-out", "trait": "Expecting others to share your exact intensity", "status": "supported", "provenance": "Cooper pp. 31-33 (disappointment when others do not match personal dedication)"}
]

def build_revised_cards():
    cards = {}

    card_specs = [
        {
            "num": 1,
            "chaldean_planet": "Sun (Surya)",
            "aleka_summary": "Initiative, leadership, original creation impulse, high ambition.",
            "western_summary": "Self-starting independence, executive drive, generous in small ways.",
            "loshu_summary": "Life Path 1: Pioneer, self-directed ambition, independence.",
            "sub_variants": {
                "1": "Unitary impulse; independent self-reliance.",
                "10": "Cycles of rise and renewal; completion of a cycle and fresh origination. Note: 'Wheel of Fortune' is external lore, source needed.",
                "19": "High vitality and clear values; lessons in balance and humility. Note: 'Prince of Heaven' is external lore, source needed.",
                "28": "Strong executive drive navigating partnership negotiations and trust. Note: 'Trusting Lamb' is external lore, source needed."
            },
            "customer_draft": "Mulank 1 is traditionally linked with initiative and independence. You tend to start things and trust your own judgement. Your growth edge is listening early and sharing credit.",
            "day_to_day": "You tend to lead from the front, set projects in motion, and rely on your own discernment. You are often the person who steps forward when direction is missing.",
            "drives_you": "A natural preference for autonomy and self-directed work. Stress often shows up as impatience, leaning too heavily on recognition, or choosing to carry duties alone.",
            "strengths": ["Self-starting initiative", "Clear decision-making", "Comfort leading from scratch"],
            "watch_outs": ["Temptation to overrule others", "Impatience with slower paces", "Can cool quickly on a new idea"]
        },
        {
            "num": 2,
            "chaldean_planet": "Moon (Chandra)",
            "aleka_summary": "Gentle, receptive, diplomatic, loyal, thrives in partnership.",
            "western_summary": "Emotional attunement, supportive alliance, peacemaking instinct.",
            "loshu_summary": "Life Path 2: Cooperation, tact, peacemaking, partnership.",
            "sub_variants": {
                "2": "Gentle reflective partnership; natural peacemaking.",
                "11": "Heightened sensitivity and visionary inspiration paired with follow-through tests. Note: 'Lion Muzzled' is external lore, source needed.",
                "20": "Quiet incubation, reflective purpose and counsel. Note: 'The Awakening' is external lore, source needed.",
                "29": "Sharp discernment tested through relational friction and partnership tests. Note: 'Grace Under Pressure' is external lore, source needed."
            },
            "customer_draft": "Mulank 2 is traditionally linked with cooperation and emotional intelligence. You read people well and build trust. Your growth edge is stating your own preference clearly and early.",
            "day_to_day": "You tend to read the room intuitively, mediate differences, and build solid alliances. You often thrive in partnership rather than isolated competition.",
            "drives_you": "A deep drive for harmony and emotional safety. Stress often shows up as withdrawing, over-accommodating others' views, or hesitating to express a direct preference.",
            "strengths": ["Diplomatic tact", "Loyal partnership", "Emotional attunement"],
            "watch_outs": ["Over-relying on others' approval", "Absorbing ambient tension", "Hesitating to state boundaries early"]
        },
        {
            "num": 3,
            "chaldean_planet": "Jupiter (Guru)",
            "aleka_summary": "Wisdom, creative expression, optimism, knowledge stewardship.",
            "western_summary": "Articulate communication, idea generation, intellectual enthusiasm.",
            "loshu_summary": "Life Path 3: Creative self-expression, communication, optimism.",
            "sub_variants": {
                "3": "Expressive communication and advisory optimism.",
                "12": "Intellectual service and causes, tested through overcoming misunderstandings. Note: 'The Sacrifice' is external lore, source needed.",
                "21": "Initiation to new mastery; early effort bearing later recognition. Note: 'Crown of the Magi' is external lore, source needed.",
                "30": "Deep intellectual and philosophical deduction, capable of high detachment. Note: 'Luminous Mind' is external lore, source needed."
            },
            "customer_draft": "Mulank 3 is traditionally linked with creativity, communication and optimism. You light up a room and generate ideas easily. Your growth edge is finishing what you start and choosing fewer priorities.",
            "day_to_day": "You tend to connect people, explain complex ideas warmly, and bring an upbeat energy to group settings.",
            "drives_you": "A natural drive to express, teach, and connect. Stress often shows up as restless multi-tasking, over-promising, or scattering attention across too many projects.",
            "strengths": ["Warm communication", "Creative concept generation", "Intellectual enthusiasm"],
            "watch_outs": ["Scattered focus across multiple initiatives", "Speaking before full reflection", "Underestimating delivery effort"]
        },
        {
            "num": 4,
            "chaldean_planet": "Rahu / Uranus",
            "aleka_summary": "Discipline, order, unconventional perspective, service, endurance.",
            "western_summary": "Structural loyalty, perseverance, practical craftsmanship.",
            "loshu_summary": "Life Path 4: Practical order, hard work, systematic building.",
            "sub_variants": {
                "4": "Structural builder; loyalty to orderly process.",
                "13": "Change of plans and place; restructuring after upheaval. Note: 'Karmic Transformation' is external lore, source needed.",
                "22": "Practical vision at scale, needing grounded execution. Note: 'Master Builder' is external lore, source needed.",
                "31": "Methodical precision, self-reliance and cautious progress. Note: 'Methodical Thinker' is external lore, source needed."
            },
            "customer_draft": "Mulank 4 is traditionally linked with discipline and solid foundations. You are dependable and detail-aware. Your growth edge is staying flexible when plans change.",
            "day_to_day": "You tend to build dependable systems, verify the details others overlook, and create predictable workflows that hold over time.",
            "drives_you": "A strong drive for structural security and orderly execution. Stress often shows up as stubbornness, over-checking minor details, or feeling uneasy with sudden ambiguity.",
            "strengths": ["Reliable discipline", "Operational thoroughness", "Loyalty to commitments"],
            "watch_outs": ["Rigid adherence to existing routines", "Reluctance to pivot when plans change", "Uneasiness with unmapped territory"]
        },
        {
            "num": 5,
            "chaldean_planet": "Mercury (Budh)",
            "aleka_summary": "Versatility, quick commerce, networking, movement, fast intellect.",
            "western_summary": "Commercial acumen, adaptability, love of freedom and variety.",
            "loshu_summary": "Life Path 5: Freedom, travel, resourcefulness, adaptable explorer.",
            "sub_variants": {
                "5": "Mercurial fluidity; natural trade and networking acuity.",
                "14": "Mercantile enterprise and adaptability, tested through moderation. Note: 'Magnetic Catalyst' is external lore, source needed.",
                "23": "Persuasive communication and goodwill from mentors and colleagues. Note: 'Royal Star of the Lion' is external lore, source needed."
            },
            "customer_draft": "Mulank 5 is traditionally linked with curiosity, versatility and movement. You learn fast and adapt well. Your growth edge is anchoring a few routines so your energy has somewhere to land.",
            "day_to_day": "You tend to adapt effortlessly to new environments, connect disparate people and ideas, and spot commercial or social opportunities quickly.",
            "drives_you": "A core drive for mental variety and experiential freedom. Stress often shows up as restlessness, spreading yourself thin, or telling people what they want to hear to avoid tension.",
            "strengths": ["Quick intellectual agility", "Resourceful adaptability", "Natural commercial communication"],
            "watch_outs": ["Restless switching between roles or projects", "Over-committing across too many fronts", "Neglecting foundational follow-through"]
        },
        {
            "num": 6,
            "chaldean_planet": "Venus (Shukra)",
            "aleka_summary": "Harmony, aesthetics, domestic responsibility, artistic magnetism, protective care.",
            "western_summary": "Nurturing responsibility, artistic generosity, family dedication.",
            "loshu_summary": "Life Path 6: Responsibility, home, community care, artistic eye.",
            "sub_variants": {
                "6": "Venusian harmony; devotion to family, beauty, and domestic sanctuary.",
                "15": "Charm, persuasive speech and arts, tested by care for others. Note: 'The Magician' is external lore, source needed.",
                "24": "Loyal teamwork, family harmony and supportive alliances. Note: 'Fortunate Alliance' is external lore, source needed."
            },
            "customer_draft": "Mulank 6 is traditionally linked with care, family and beauty. You create warmth and take responsibility for people. Your growth edge is protecting your own time and letting others carry their share.",
            "day_to_day": "You tend to create welcoming, orderly spaces, look out for the welfare of family and team members, and bring aesthetic consideration to your work.",
            "drives_you": "A strong drive to care, support, and belong. Stress often shows up as carrying other people's responsibilities, perfectionist fussiness, or feeling quietly unappreciated.",
            "strengths": ["Empathetic stewardship", "Aesthetic discernment", "Protective loyalty to close circles"],
            "watch_outs": ["Taking on others' duties to your own detriment", "Sensitivity to perceived slights", "Difficulty stepping back from caretaking"]
        },
        {
            "num": 7,
            "chaldean_planet": "Ketu / Neptune",
            "aleka_summary": "Philosophical contemplation, research depth, quiet investigation, distinct individuality.",
            "western_summary": "Analytical depth, need for solitude, philosophical mysticism.",
            "loshu_summary": "Life Path 7: Inner wisdom, analysis, spiritual seeker, researcher.",
            "sub_variants": {
                "7": "Philosophical discernment; quiet investigation and spiritual independence.",
                "16": "Early prominence tested by humility; caution against sudden overreach. Note: 'The Tower' is external lore, source needed.",
                "25": "Quiet observation and strength gained through experience. Note: 'Discriminating Mind' is external lore, source needed."
            },
            "customer_draft": "Mulank 7 is traditionally linked with reflection, research and inner life. You prefer depth over noise. Your growth edge is letting a few trusted people in and acting on what you understand.",
            "day_to_day": "You tend to study matters thoroughly before speaking, value periods of uninterrupted quiet, and prefer deep conversations with a few trusted associates.",
            "drives_you": "A deep drive for truth, understanding, and personal privacy. Stress often shows up as emotional withdrawal, over-analyzing decisions, or approaching situations with dry skepticism.",
            "strengths": ["Perceptive research acumen", "Independent analytical thinking", "Comfort with solitude and depth"],
            "watch_outs": ["Withdrawing into solitary rumination", "Over-complicating straightforward actions", "Holding trusted allies at arm's length"]
        },
        {
            "num": 8,
            "chaldean_planet": "Saturn (Shani)",
            "aleka_summary": "Discipline, structural authority, finance, patient building, karmic balance.",
            "western_summary": "Executive realism, long-term stewardship, persevering endurance.",
            "loshu_summary": "Life Path 8: Executive leadership, material stewardship, perseverance.",
            "sub_variants": {
                "8": "Direct Saturnine responsibility; disciplined stewardship and perseverance.",
                "17": "Courage, recovery from difficulty and persistent effort. Note: 'Star of the Magi' is external lore, source needed.",
                "26": "Prudence in partnerships, loans and speculation; careful due diligence. Note: 'Heavy Stewardship' is external lore, source needed."
            },
            "customer_draft": "Mulank 8 is traditionally linked with structure, ambition and responsibility. You build patiently and take duty seriously. Your growth edge is pacing yourself and recognising others' limits.",
            "day_to_day": "You tend to plan for the long term, manage resources prudently, and hold yourself to rigorous standards of accountability and fair dealing.",
            "drives_you": "A core drive for durable achievement and rightful stewardship. Stress often shows up as overwork, holding total control over processes, or pushing associates past reasonable limits.",
            "strengths": ["Long-term strategic patience", "Resource and financial discipline", "Fair and steady execution"],
            "watch_outs": ["Assuming full responsibility alone", "Pushing past sustainable limits while setting a pace others struggle to match"]
        },
        {
            "num": 9,
            "chaldean_planet": "Mars (Mangal)",
            "aleka_summary": "Courage, global perspective, humanitarian empathy, fighting energy for a cause.",
            "western_summary": "Moral courage, warrior drive, generous dedication to principle.",
            "loshu_summary": "Life Path 9: Universal compassion, broad service, generous humanitarian.",
            "sub_variants": {
                "9": "Pure crusading energy; moral courage and universal empathy.",
                "18": "Material ambition balanced against emotional calm; service orientation. Note: 'The Lion Muzzled' is external lore, source needed.",
                "27": "Intellectual leadership and creative authority. Note: 'The Scepter' is external lore, source needed."
            },
            "customer_draft": "Mulank 9 is traditionally linked with energy, compassion and a wider cause. You act on conviction and care about fairness. Your growth edge is pacing your energy and accepting that others move differently.",
            "day_to_day": "You tend to stand up for principles of fairness, rally energy around broad collective goals, and give generously of your knowledge and time.",
            "drives_you": "A strong drive for purpose, equity, and constructive contribution. Stress often shows up as sharp frustration when ideals stall, emotional exhaustion from over-giving, or blunt speech.",
            "strengths": ["Courageous conviction", "Broad humanitarian outlook", "Energetic generosity"],
            "watch_outs": ["Bluntness when frustrated by inefficiency", "Scattering vital energy across too many causes", "Expecting others to share your exact intensity"]
        }
    ]

    for spec in card_specs:
        num = spec["num"]
        west_info = WESTERN_PLANET_MAP[num]
        west_pages = WESTERN_PAGES[num]
        aleka_pages = ALEKA_GHOSE_PAGES[num]
        lp_pages = WEBSTER_LP_MAP[num]
        dob_pages = WEBSTER_DOB_MAP[num]

        card = {
            "mulank": num,
            "title": f"Mulank {num}",
            
            # Plain public layer labels and customer copy
            "customer_copy": {
                "your_numbers_at_a_glance": f"Mulank {num} • Planetary association: {spec['chaldean_planet'].split()[0]}",
                "how_this_shows_up_day_to_day": spec["day_to_day"],
                "what_tends_to_drive_you": spec["drives_you"],
                "strengths_and_watch_outs": {
                    "strengths": spec["strengths"],
                    "watch_outs": spec["watch_outs"]
                },
                "traditional_note": spec["customer_draft"]
            },

            # Plain layer names on internal schema
            "internal_registry": {
                "logic": {
                    "cosmological_principle": f"Monadic progression digit {num}.",
                    "tradition_layers": {
                        "chaldean_tradition": {
                            "label": "Chaldean tradition",
                            "planet": spec["chaldean_planet"],
                            "internal_provenance_audit": {
                                "reference_system": "Chaldean single numbers",
                                "verified_pages": aleka_pages
                            }
                        },
                        "lo_shu_grid": {
                            "label": "Lo Shu grid",
                            "coordinate": f"Coordinate {num}",
                            "internal_provenance_audit": {
                                "reference_system": "Lo Shu planes",
                                "pages_life_path": lp_pages,
                                "pages_day_of_birth": dob_pages
                            }
                        },
                        "western_tradition": {
                            "label": "Western tradition",
                            "planet": west_info["planet"],
                            "comparison_note": west_info["note"],
                            "internal_provenance_audit": {
                                "reference_work": "Understanding Numerology (Aquarian, 1990)",
                                "verified_pages": west_pages
                            }
                        },
                        "secondary_western_view": {
                            "label": "Secondary Western view",
                            "audit_status": "unverified"
                        }
                    }
                },
                "observation": {
                    "natal_criteria": f"Born on calendar days reducing to {num}.",
                    "compound_sub_variants": spec["sub_variants"]
                },
                "behaviour": {
                    "strengths": spec["strengths"],
                    "watch_outs": spec["watch_outs"],
                    "canonical_layers": {
                        "chaldean_tradition": spec["aleka_summary"],
                        "lo_shu_grid": spec["loshu_summary"],
                        "western_tradition": spec["western_summary"]
                    }
                },
                "psychology": {
                    "provenance": "synthesised, no direct source",
                    "page_citation": None,
                    "cognitive_driver": spec["drives_you"],
                    "note": "Modern integrative psychological synthesis; kept mild and non-fatalistic."
                },
                "interpretation": {
                    "contextual_expression": spec["day_to_day"],
                    "traditional_interpretation_draft": spec["customer_draft"]
                },
                "tradition_conflicts_unmerged": {
                    "chaldean_vs_western_planet": {
                        "chaldean_tradition": spec["chaldean_planet"],
                        "western_tradition": west_info["planet"],
                        "conflict_status": "Conflicting attribution preserved as independent qualitative layer without averaging." if "Conflict" in west_info["note"] else "Agreement"
                    }
                },
                "validation": {
                    "status": "untested",
                    "testable_statement": f"Consented user self-assessment indicates alignment with {spec['strengths'][0].lower()}."
                },
                "prediction": {
                    "status": "blocked"
                },
                "trace_audit": {
                    "trait_mapping": (
                        "Mulank 1 'cool quickly' -> Cooper pp. 15-16 (Understanding Numerology, Aquarian 1990)"
                        if num == 1 else
                        "Mulank 8 overwork -> Aleka pp. 20-21; pace -> Cooper pp. 29-31 (Understanding Numerology, Aquarian 1990)"
                        if num == 8 else
                        "All traits sourced from verified citations or synthesised"
                    )
                }
            }
        }
        cards[str(num)] = card

    # Add Compound 28 Reference Schema
    compound_28 = {
        "number": 28,
        "kind": "compound",
        "reduces_to": 1,
        "digits": [2, 8],
        "customer_copy": {
            "your_numbers_at_a_glance": "Number 28 (reduces to 1)",
            "how_this_shows_up_day_to_day": "You value independent leadership and prefer to be your own guide. In work and alliances, you bring strong ambition paired with a need for dependable partners.",
            "what_tends_to_drive_you": "A strong drive for achievement and high potential, balanced by the practical lesson of exercising due diligence in associations and agreements.",
            "strengths_and_watch_outs": {
                "strengths": [
                    "High executive capability",
                    "Resilience to start again and rebuild",
                    "Natural preference for self-directed enterprise"
                ],
                "watch_outs": [
                    "Misplacing trust in unvetted partnerships",
                    "Underestimating competitors or procedural requirements",
                    "Taking unnecessary legal or speculative risks"
                ]
            },
            "traditional_note": "Number 28 holds great potential, but the tradition warns of reversals if trust is misplaced, rivals are underestimated or rules are bent. Gains can be lost and may need rebuilding. Careful choices, legal prudence and sound ethics protect it, especially if your chart has strong 1s or 4s."
        },
        "internal_registry": {
            "logic": "Compound = the sum before final reduction (calendar day 28 or full date sum).",
            "observation": "Great potential traditionally flagged for reversals through misplaced trust or non-compliance.",
            "behaviour_day_lens": "Affectionate, freedom-loving, prefers to be own boss.",
            "sensitivity_flag": "SENSITIVE-SOFTENED-WORDING-KEEPS-MEANING",
            "provenance": {
                "chaldean_tradition": "Aleka Ghose pp. 59-69 (compound series)",
                "lo_shu_grid": "Webster pp. 20-25 (day-of-birth lens)",
                "western_tradition": "Understanding Numerology (Aquarian, 1990)"
            },
            "psychology": {
                "provenance": "synthesised, no direct source",
                "page_citation": None,
                "note": "Kept mild, non-fatalistic, growth-oriented."
            },
            "validation": { "status": "untested" },
            "prediction": { "status": "blocked" }
        }
    }

    return cards, compound_28

def verify_front_end_cleanliness(cards, compound_28):
    violations = []
    all_cards = list(cards.values()) + [compound_28]
    for card in all_cards:
        num = card.get("mulank", card.get("number"))
        cc = card.get("customer_copy", {})
        text_dump = json.dumps(cc).lower()
        for banned in BANNED_FRONT_END_WORDS:
            pattern = rf"\b{re.escape(banned)}\b"
            if re.search(pattern, text_dump, re.IGNORECASE):
                violations.append((num, f"Banned framework term: {banned}"))
        for term in AUTHOR_NAMES_AND_TITLES:
            pattern = rf"\b{re.escape(term)}\b"
            if re.search(pattern, text_dump, re.IGNORECASE):
                violations.append((num, f"Author/Title leak: {term}"))
    return violations

def write_files():
    cards, compound_28 = build_revised_cards()
    violations = verify_front_end_cleanliness(cards, compound_28)
    if violations:
        raise ValueError(f"Front-end language violations detected: {violations}")

    out_json = {
        "metadata": {
            "title": "Numeros Vision Mulank Pilot Cards (Mulank 1 to 9)",
            "version": "1.3.1",
            "revised_date": "2026-11-08",
            "governing_rules": "AGENTS.md & .agents/rules/nv_think_framework.md",
            "internal_validation_status": "untested",
            "internal_prediction_status": "blocked",
            "internal_audit_notes": {
                "cooper_reference": "Understanding Numerology (Aquarian, 1990)",
                "trace_notes": {
                    "mulank_8_overwork": "Aleka pp. 20-21",
                    "mulank_8_pace": "Cooper pp. 29-31",
                    "mulank_1_cool_quickly": "Cooper pp. 15-16"
                },
                "aleka_ghose_single_pages": "1: pp 11-12, 2: p 13, 3: p 14, 4: p 15, 5: pp 16-17, 6: p 18, 7: pp 19-20, 8: pp 20-21, 9: pp 21-22; compounds: pp 59-69",
                "webster_life_path_pages": "1: pp 5-7, 2: pp 8-9, 3: pp 9-10, 4: pp 10-11, 5: p 11, 6: pp 11-12, 7: pp 12-13, 8: pp 13-14, 9: pp 14-15; masters: pp 16-18",
                "webster_day_of_birth_pages": "1-4: p 20, 5: pp 20-21, 6-9: p 21",
                "western_tradition_pages": "pp 15-33 (attributions: 8=Pluto, 6=Moon, 7=Venus, 4=Saturn, 2=Earth)",
                "secondary_western_status": "unverified",
                "public_layer_labels": ["Chaldean tradition", "Lo Shu grid", "Western tradition"]
            },
            "trait_trace_table": TRAIT_TRACE_REGISTRY
        },
        "cards": cards,
        "sample_compound_cards": {
            "28": compound_28
        }
    }

    with open('data/knowledge_base/nv_think_mulank_pilot_cards.json', 'w', encoding='utf-8') as f:
        json.dump(out_json, f, indent=2, ensure_ascii=False)
    print("Updated data/knowledge_base/nv_think_mulank_pilot_cards.json successfully.")

    # Update docs/NV_THINK_MULANK_PILOT_RULE_CARDS.md
    doc_lines = []
    doc_lines.append("# NUMEROS VISION — MULANK PILOT CARDS (1 TO 9)")
    doc_lines.append("**Registry Version:** 1.3.1 (Plain Words & Generic Institutional Edition)  ")
    doc_lines.append("**Governance:** Server-Side Internal Architecture Only  ")
    doc_lines.append("**Validation Status:** `untested` (Internal)  ")
    doc_lines.append("**Prediction Status:** `blocked` (Internal)  ")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## 1. Public Presentation Standards")
    doc_lines.append("- **Plain Public Layer Labels:** `Chaldean tradition`, `Lo Shu grid`, `Western tradition`.")
    doc_lines.append("- **Customer Headings:** `Your numbers at a glance`, `How this shows up day to day`, `What tends to drive you`, `Strengths and watch-outs`, `Traditional note`.")
    doc_lines.append("- **Zero Author Names or Titles in Customer Copy:** Full bibliography isolated to `app/static/how_we_work.html`.")
    doc_lines.append("- **Cooper Reference Confirmed:** `Understanding Numerology (Aquarian, 1990)` recorded in internal audit metadata only.")
    doc_lines.append("- **Verified Internal Citations:**")
    doc_lines.append("  - Webster Life Path: 1: pp 5–7, 2: pp 8–9, 3: pp 9–10, 4: pp 10–11, 5: p 11, 6: pp 11–12, 7: pp 12–13, 8: pp 13–14, 9: pp 14–15; Masters: pp 16–18.")
    doc_lines.append("  - Webster Day of Birth: 1–4: p 20, 5: pp 20–21, 6–9: p 21.")
    doc_lines.append("  - Aleka Ghose Single Numbers: 1: pp 11–12, 2: p 13, 3: p 14, 4: p 15, 5: pp 16–17, 6: p 18, 7: pp 19–20, 8: pp 20–21, 9: pp 21–22; Compounds: pp 59–69.")
    doc_lines.append("  - Western tradition: pp 15–33 (attributions: 8=Pluto, 6=Moon, 7=Venus, 4=Saturn, 2=Earth).")
    doc_lines.append("  - Secondary Western view: Marked `unverified`.")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")
    doc_lines.append("## 2. Rebuilt Trait Trace Register (Audit Trail)")
    doc_lines.append("| Mulank | Type | Trait | Audit Status | Source Claim / Provenance |")
    doc_lines.append("|:---:|:---:|:---|:---:|:---|")
    for row in TRAIT_TRACE_REGISTRY:
        doc_lines.append(f"| **{row['mulank']}** | {row['type']} | {row['trait']} | `{row['status']}` | {row['provenance']} |")
    doc_lines.append("")
    doc_lines.append("---")
    doc_lines.append("")

    for num_str, card in cards.items():
        num = card["mulank"]
        cc = card["customer_copy"]
        ir = card["internal_registry"]
        doc_lines.append(f"## Mulank {num}")
        doc_lines.append("")
        doc_lines.append("### Customer-Facing Copy (Public Surface)")
        doc_lines.append(f"**Your numbers at a glance:** {cc['your_numbers_at_a_glance']}  ")
        doc_lines.append(f"**How this shows up day to day:** {cc['how_this_shows_up_day_to_day']}  ")
        doc_lines.append(f"**What tends to drive you:** {cc['what_tends_to_drive_you']}  ")
        doc_lines.append(f"**Strengths and watch-outs:**")
        doc_lines.append(f"- *Strengths:* {', '.join(cc['strengths_and_watch_outs']['strengths'])}")
        doc_lines.append(f"- *Watch-outs:* {', '.join(cc['strengths_and_watch_outs']['watch_outs'])}")
        doc_lines.append(f"**Traditional note:** {cc['traditional_note']}  ")
        doc_lines.append("")
        doc_lines.append("### Internal Diagnostic Layer (Server-Side Metadata Only)")
        doc_lines.append(f"- **Chaldean tradition:** {ir['logic']['tradition_layers']['chaldean_tradition']['planet']} (Internal audit pages: {ir['logic']['tradition_layers']['chaldean_tradition']['internal_provenance_audit']['verified_pages']})")
        doc_lines.append(f"- **Lo Shu grid:** Coordinate {num} (Internal audit pages: LP {ir['logic']['tradition_layers']['lo_shu_grid']['internal_provenance_audit']['pages_life_path']}, DOB {ir['logic']['tradition_layers']['lo_shu_grid']['internal_provenance_audit']['pages_day_of_birth']})")
        doc_lines.append(f"- **Western tradition:** {ir['logic']['tradition_layers']['western_tradition']['planet']} (Internal audit pages: {ir['logic']['tradition_layers']['western_tradition']['internal_provenance_audit']['verified_pages']}) — *{ir['logic']['tradition_layers']['western_tradition']['comparison_note']}*")
        doc_lines.append(f"- **Secondary Western view:** Audit status: `{ir['logic']['tradition_layers']['secondary_western_view']['audit_status']}`")
        doc_lines.append(f"- **Psychology Provenance:** `{ir['psychology']['provenance']}`")
        doc_lines.append(f"- **Validation Status:** `{ir['validation']['status']}`")
        doc_lines.append(f"- **Prediction Status:** `{ir['prediction']['status']}`")
        if "trace_audit" in ir and ir["trace_audit"].get("trait_mapping"):
            doc_lines.append(f"- **Trace Audit:** `{ir['trace_audit']['trait_mapping']}`")
        doc_lines.append("")
        doc_lines.append("---")
        doc_lines.append("")

    # Compound 28 section in doc
    doc_lines.append("## Compound 28 (Special Sensitivity Case)")
    doc_lines.append("")
    doc_lines.append("### Customer-Facing Copy (Public Surface)")
    doc_lines.append(f"**Your numbers at a glance:** {compound_28['customer_copy']['your_numbers_at_a_glance']}  ")
    doc_lines.append(f"**How this shows up day to day:** {compound_28['customer_copy']['how_this_shows_up_day_to_day']}  ")
    doc_lines.append(f"**What tends to drive you:** {compound_28['customer_copy']['what_tends_to_drive_you']}  ")
    doc_lines.append(f"**Strengths and watch-outs:**")
    doc_lines.append(f"- *Strengths:* {', '.join(compound_28['customer_copy']['strengths_and_watch_outs']['strengths'])}")
    doc_lines.append(f"- *Watch-outs:* {', '.join(compound_28['customer_copy']['strengths_and_watch_outs']['watch_outs'])}")
    doc_lines.append(f"**Traditional note:** {compound_28['customer_copy']['traditional_note']}  ")
    doc_lines.append("")
    doc_lines.append("### Internal Diagnostic Layer (Server-Side Metadata Only)")
    doc_lines.append(f"- **Logic:** {compound_28['internal_registry']['logic']}")
    doc_lines.append(f"- **Observation:** {compound_28['internal_registry']['observation']}")
    doc_lines.append(f"- **Sensitivity Flag:** `{compound_28['internal_registry']['sensitivity_flag']}`")
    doc_lines.append(f"- **Psychology Provenance:** `{compound_28['internal_registry']['psychology']['provenance']}`")
    doc_lines.append("")

    with open('docs/NV_THINK_MULANK_PILOT_RULE_CARDS.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(doc_lines))
    print("Updated docs/NV_THINK_MULANK_PILOT_RULE_CARDS.md successfully.")

    # Sync to brain artifact
    artifact_path = r'C:\Users\Bhaskr Singh\.gemini\antigravity\brain\c1ea3ed7-b9d2-437a-b7aa-f0cb4004681b\NV_THINK_MULANK_PILOT_RULE_CARDS.md'
    with open(artifact_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(doc_lines))
    print(f"Synced to artifact: {artifact_path}")

if __name__ == '__main__':
    write_files()
