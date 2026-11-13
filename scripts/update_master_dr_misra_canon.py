import os
import sys

def update_canon():
    reg_path = os.path.join('app', 'engine', 'number_characteristics_registry.py')
    with open(reg_path, 'r', encoding='utf-8') as f:
        code = f.read()

    subdate_registry_code = '''
# ── DR. Numeros Vision Classical Methodology DAY 6 CANONICAL SUB-DATE & NUMBER CHARACTERISTICS ────
# Source: Master Numerology with Dr. Numeros Vision Classical Methodology - DAY 6 (Numeros Vision)
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
'''

    if 'BIRTH_DAY_SUBDATE_REGISTRY' not in code:
        code += subdate_registry_code
        with open(reg_path, 'w', encoding='utf-8') as f:
            f.write(code)
        print('Successfully added BIRTH_DAY_SUBDATE_REGISTRY to number_characteristics_registry.py')
    else:
        print('BIRTH_DAY_SUBDATE_REGISTRY already present')

if __name__ == '__main__':
    update_canon()
