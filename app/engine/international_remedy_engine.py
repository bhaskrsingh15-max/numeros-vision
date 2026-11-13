"""
app/engine/international_remedy_engine.py
=========================================
INTERNATIONAL & REST-OF-WORLD (NON-INDIA) PLANETARY NUMEROLOGY & REMEDY ENGINE
Numeros Vision — ANVEIL EVERY CHARM

Designed specifically for international seekers across the USA, UK, Canada, Australia,
Europe, Middle East, and worldwide (excluding domestic India).

Core Architectural Pillars:
1. English Name Acoustic Vibrations:
   - First Name (Spoken Frequency & Social Aura)
   - Middle Name (Harmonic Bridge & Ancestral Memory)
   - Last Name (Foundational Inheritance & Structure)
   - Professional Signature Calibration (Slant, Underline, Baseline flow)
   - Vowel Core (Soul Urge) vs Consonant Shield (Outer Expression)
2. Targeted Charitable Giving & Altruistic Donations:
   - Every planet is harmonized through specific non-profit causes, community giving,
     timing, and karmic intention.
3. Universal Contemplative Rituals & Inclusive Prayers:
   - Works respectfully across all faiths (Christian, Jewish, Universal Spiritual,
     Secular/Contemplative, Interfaith).
   - Solfeggio sound frequencies, morning light attunements, evening candle rituals,
     and dignified reflective affirmations.
4. Modern Lifestyle & Environmental Harmonizers:
   - Workspace orientation, color acoustics, gemstones, and natural metals.
"""

from typing import Dict, Any, List, Optional
import re

# ─────────────────────────────────────────────────────────────────────────────
# 1. PLANETARY ARCHETYPES (ENGLISH TERMINOLOGY FOR INTERNATIONAL USERS)
# ─────────────────────────────────────────────────────────────────────────────
INTERNATIONAL_PLANET_ARCHETYPES = {
    1: {
        "planet": "The Sun",
        "archetype": "The Sovereign Leader",
        "keyword": "Vision, Authority, Independence & Vitality",
        "description": "Governs personal autonomy, executive initiative, core vitality, and self-respect. In English names, solar resonance grants natural visibility and executive respect.",
        "element": "Fire / Solar Light",
        "day_of_power": "Sunday (Solar Morning)",
        "attuned_colors": "Warm Gold, Amber, Burnt Orange, Sunlit Yellow",
        "avoid_colors": "Jet Black, Murky Dull Blue",
        "harmonic_metal": "Warm Gold or Polished Copper",
        "healing_crystals": "Sunstone, Red Jasper, Clear Quartz",
        "solfeggio_freq": "528 Hz (Solar Vitality & DNA Awakening)",
        "cardinal_direction": "East (Direction of the Rising Dawn)"
    },
    2: {
        "planet": "The Moon",
        "archetype": "The Intuitive Diplomat",
        "keyword": "Empathy, Emotional Fluidity, Peace & Receptivity",
        "description": "Governs intuitive perception, mental tranquility, relationship diplomacy, and emotional balance. Promotes harmony in partnerships and creative arts.",
        "element": "Water / Lunar Glow",
        "day_of_power": "Monday (Evening Twilight or Full Moon)",
        "attuned_colors": "Luminous Pearl, Cream White, Soft Silver, Mist Grey",
        "avoid_colors": "Fiery Crimson, Stark Jet Black",
        "harmonic_metal": "Sterling Silver or Platinum",
        "healing_crystals": "Moonstone, Selenite, White Calcite",
        "solfeggio_freq": "432 Hz (Natural Harmony & Emotional Calming)",
        "cardinal_direction": "North-West (Flowing Evening Vector)"
    },
    3: {
        "planet": "Jupiter",
        "archetype": "The Wise Counselor",
        "keyword": "Wisdom, Ethical Expansion, Mentorship & Growth",
        "description": "Governs higher knowledge, strategic counsel, ethical wealth, education, and philosophical clarity. Attracts mentors and expansive opportunities.",
        "element": "Ether / Golden Air",
        "day_of_power": "Thursday (Midday Solar Zenith)",
        "attuned_colors": "Canary Yellow, Warm Saffron, Golden Ochre, Royal Purple",
        "avoid_colors": "Dark Slate Grey, Harsh Neon Pink",
        "harmonic_metal": "Yellow Gold or Pure Brass",
        "healing_crystals": "Citrine, Yellow Topaz, Golden Tiger's Eye",
        "solfeggio_freq": "639 Hz (Harmonious Community & Expansion)",
        "cardinal_direction": "North-East (Wisdom & Clarity Vector)"
    },
    4: {
        "planet": "Uranus / North Node",
        "archetype": "The Advanced Architect",
        "keyword": "Systemic Innovation, Global Vision & Unconventional Breakthroughs",
        "description": "Governs modern technical systems, digital innovation, architectural foresight, and breaking through outmoded conventions.",
        "element": "Earth / Structured Electricity",
        "day_of_power": "Wednesday & Saturday (Twilight)",
        "attuned_colors": "Electric Slate Blue, Charcoal Grey, Soft Silver, Forest Khaki",
        "avoid_colors": "Pure Pitch Black, Aggressive Bright Red",
        "harmonic_metal": "Sterling Silver or Solid Pewter",
        "healing_crystals": "Smoky Quartz, Labradorite, Black Tourmaline",
        "solfeggio_freq": "741 Hz (Problem Solving & Cellular Detoxing)",
        "cardinal_direction": "South-West (Structural Grounding Vector)"
    },
    5: {
        "planet": "Mercury",
        "archetype": "The Master Communicator",
        "keyword": "Commercial Velocity, Linguistic Fluency & Agility",
        "description": "Governs market speed, clear articulation, networking, commercial contracts, trade, and youthfulness. Keeps the mind swift, adaptable, and witty.",
        "element": "Earth & Quicksilver Air",
        "day_of_power": "Wednesday (Active Morning Commerce Hours)",
        "attuned_colors": "Emerald Green, Sage, Fresh Mint, Luminous Turquoise",
        "avoid_colors": "Aggressive Blood Red, Muddy Brown",
        "harmonic_metal": "Bronze or White Gold",
        "healing_crystals": "Green Aventurine, Green Jade, Malachite",
        "solfeggio_freq": "528 Hz (Clarity of Expression & Rapid Learning)",
        "cardinal_direction": "North (Commercial Flow & Intellect Vector)"
    },
    6: {
        "planet": "Venus",
        "archetype": "The Harmonizer of Abundance",
        "keyword": "Love, Aesthetic Discernment, Luxury & Material Ease",
        "description": "Governs creative arts, romantic fidelity, high aesthetic taste, material abundance, luxury assets, and charismatic charm.",
        "element": "Water & Refined Air",
        "day_of_power": "Friday (Evening Twilight)",
        "attuned_colors": "Rose Pink, Powder Blue, Diamond White, Champagne Cream",
        "avoid_colors": "Mustard Yellow, Dull Muddy Brown",
        "harmonic_metal": "White Gold, Rose Gold, or Silver",
        "healing_crystals": "Rose Quartz, Clear Optical Quartz, Opal",
        "solfeggio_freq": "639 Hz (Heart Chakra & Abundance Magnetism)",
        "cardinal_direction": "South-East (Comfort & Creative Warmth Vector)"
    },
    7: {
        "planet": "Neptune / South Node",
        "archetype": "The Contemplative Mystic",
        "keyword": "Intuition, Analytical Depth, Solitude & Spiritual Truth",
        "description": "Governs profound research, philosophical detachment, psychological insight, and scientific synthesis. Cuts through superficial illusions.",
        "element": "Water & Introspective Mist",
        "day_of_power": "Tuesday & Saturday (Quiet Evening)",
        "attuned_colors": "Seafoam Green, Soft Lavender, Dove Grey, Cloud White",
        "avoid_colors": "Heavy Jet Black, Harsh Maroon",
        "harmonic_metal": "Refined White Metal or Silver",
        "healing_crystals": "Cat's Eye Chrysoberyl, Tiger's Eye, Amethyst",
        "solfeggio_freq": "852 Hz (Intuitive Awakening & Inner Vision)",
        "cardinal_direction": "North-West (Introspective Clarity Vector)"
    },
    8: {
        "planet": "Saturn",
        "archetype": "The Master of Time & Scale",
        "keyword": "Discipline, Monumental Compounding, Endurance & Justice",
        "description": "Governs long-term patience, enterprise foundations, real estate, structural governance, and resilience through adversity.",
        "element": "Earth & Crystalline Stone",
        "day_of_power": "Saturday (Late Afternoon before Sunset)",
        "attuned_colors": "Deep Midnight Navy, Charcoal, Steel Grey, Rich Indigo",
        "avoid_colors": "Fiery Orange-Red, Canary Yellow",
        "harmonic_metal": "Hand-forged Iron or Darkened Titanium",
        "healing_crystals": "Blue Sapphire, Amethyst, Black Onyx",
        "solfeggio_freq": "396 Hz (Liberation from Fear & Grounded Stability)",
        "cardinal_direction": "West (Stability & Long-term Endurance Vector)"
    },
    9: {
        "planet": "Mars",
        "archetype": "The Protector & Pioneer",
        "keyword": "Courage, Decisive Action, Physical Power & Humanitarian Zeal",
        "description": "Governs bold initiative, physical stamina, leadership under fire, defending the vulnerable, and decisive goal execution.",
        "element": "Fire & Oceanic Iron",
        "day_of_power": "Tuesday (Morning Solar Surge)",
        "attuned_colors": "Crimson, Rich Coral, Ruby Red, Warm Terracotta",
        "avoid_colors": "Jet Black, Dark Murky Navy",
        "harmonic_metal": "Pure Copper or Rose Gold",
        "healing_crystals": "Red Coral, Carnelian, Bloodstone",
        "solfeggio_freq": "417 Hz (Undoing Stagnation & Activating Momentum)",
        "cardinal_direction": "South (Courage & Dynamic Action Vector)"
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# 2. PLANETARY CHARITABLE GIVING & TARGETED DONATIONS (INTERNATIONAL DANA)
# ─────────────────────────────────────────────────────────────────────────────
INTERNATIONAL_CHARITY_CATALOGUE = {
    1: {
        "cause_focus": "Vision Care, Veterans & Leadership Development",
        "recommended_giving": "Support blindness prevention charities (e.g. guide dogs, cataract surgery foundations) or veteran support programs. Alternatively, sponsor a youth leadership scholarship.",
        "everyday_act": "Offer a hot meal or cold water to someone in outdoor heat without drawing attention to yourself.",
        "timing": "Sundays between 9:00 AM and 11:30 AM (Solar Morning).",
        "karmic_intention": "Giving sight, honor, and warmth to those in the shadows; balances executive ego and opens doors to natural authority."
    },
    2: {
        "cause_focus": "Clean Water, Maternal Health & Orphanages",
        "recommended_giving": "Donate to global clean water initiatives (e.g. well drilling in arid communities) or women's shelters and maternal health clinics.",
        "everyday_act": "Distribute bottles of fresh drinking water or organic milk to caregivers, nursing mothers, or homeless individuals.",
        "timing": "Mondays in the evening or during the full moon window.",
        "karmic_intention": "Nurturing emotional shelter for mothers and children; soothes chronic anxiety and brings deep emotional tranquility."
    },
    3: {
        "cause_focus": "Libraries, Literacy & Educational Endowments",
        "recommended_giving": "Donate books to public libraries, sponsor school supplies for underprivileged children, or support ethical educational non-profits.",
        "everyday_act": "Buy a book of wisdom or educational tools for a curious young student or junior colleague.",
        "timing": "Thursdays at solar noon (12:00 PM - 1:30 PM).",
        "karmic_intention": "Spreading illumination and ethical knowledge; dissolves intellectual arrogance and attracts prosperous mentorship."
    },
    4: {
        "cause_focus": "Digital Inclusion, Leprosy / Chronic Illness & Homeless Shelters",
        "recommended_giving": "Donate refurbished laptops or tablets to underprivileged youth, or contribute to chronic pain, leprosy, or neurological research foundations.",
        "everyday_act": "Donate durable warm blankets, thermal socks, or umbrellas to local homeless shelters.",
        "timing": "Wednesdays or Saturdays at dusk.",
        "karmic_intention": "Shielding vulnerable outcasts and bridging technology gaps; clears mental fog and dissolves sudden unexpected setbacks."
    },
    5: {
        "cause_focus": "Environmental Conservation, Reforestation & Bird Sanctuaries",
        "recommended_giving": "Contribute to certified tree-planting foundations (e.g. urban green corridors) or wildlife and bird rehabilitation sanctuaries.",
        "everyday_act": "Scatter sunflower seeds or bird feed on a clean balcony or park terrace every morning.",
        "timing": "Wednesdays between 8:00 AM and 10:00 AM.",
        "karmic_intention": "Nourishing voice, flight, and green life; multiplies commercial opportunities and enhances persuasive clarity."
    },
    6: {
        "cause_focus": "Women's Rehabilitation, Art Endowments & Family Care",
        "recommended_giving": "Support domestic violence transition homes, women's entrepreneurship micro-loans, or youth fine arts and music academies.",
        "everyday_act": "Donate elegant clean clothing, high-quality toiletries, or healthy gourmet treats to elderly care residences.",
        "timing": "Fridays during sunset or early twilight.",
        "karmic_intention": "Fostering dignity, creative joy, and relational beauty; attracts harmonious partnerships and effortless material prosperity."
    },
    7: {
        "cause_focus": "Animal Rescue Shelters, Hospice Care & Silent Sanctuaries",
        "recommended_giving": "Donate to no-kill animal rescue shelters (especially stray dogs and neglected animals) or contemplative hospice palliative care programs.",
        "everyday_act": "Feed stray or shelter dogs with nutritious food; provide pet blankets to local rescue centers.",
        "timing": "Tuesdays or Saturdays in quiet evening hours.",
        "karmic_intention": "Showing mercy to voiceless creatures and souls in transition; cuts through worldly confusion and awakens intuitive foresight."
    },
    8: {
        "cause_focus": "Disability Support, Blue-Collar Labor Welfare & Homeless Warmth",
        "recommended_giving": "Contribute to vocational training for people with physical disabilities, blue-collar workers' relief funds, or chronic hunger kitchens.",
        "everyday_act": "Gift sturdy work boots, heavy jackets, or substantial hot meals to manual construction workers or municipal sanitation staff.",
        "timing": "Saturdays in the late afternoon before sunset.",
        "karmic_intention": "Honoring the silent backbone of society and lightening heavy burdens; transforms career delays into permanent monumental wealth."
    },
    9: {
        "cause_focus": "Blood Donation, Wounded First Responders & Burn Recovery",
        "recommended_giving": "Donate blood at a certified blood bank; contribute to firefighter/paramedic trauma funds or pediatric burn treatment hospitals.",
        "everyday_act": "Send emergency medical aid or sponsor physical therapy rehabilitation for someone recovering from an injury.",
        "timing": "Tuesdays between 11:00 AM and 2:00 PM.",
        "karmic_intention": "Offering life force to protect the wounded and defenseless; transmutes reactive anger into noble courage and enduring stamina."
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# 3. UNIVERSAL PRAYERS, CONTEMPLATIVE AFFIRMATIONS & RITUALS (REST OF WORLD)
# ─────────────────────────────────────────────────────────────────────────────
INTERNATIONAL_RITUALS_CATALOGUE = {
    1: {
        "prayer_name": "Solar Dawn Invocation of Purpose & Integrity",
        "prayer_text": "Divine Source of all Light, illuminate my mind with purposeful clarity today. Grant me the courage to lead with integrity, to speak with truth, and to warm the lives of those entrusted to my care. Free my heart from vanity, and let my work serve the greater good.",
        "candle_ritual": "Light a pure beeswax or golden-yellow candle facing East at dawn. Stand quietly for 3 minutes taking 7 deep diaphragmatic breaths, visualizing golden dawn light filling your chest.",
        "affirmation": "I stand rooted in quiet authority. My integrity is my shield, and my vision inspires positive action."
    },
    2: {
        "prayer_name": "Evening Lunar Benediction of Serenity & Intuition",
        "prayer_text": "Eternal Grace, quiet the storms of my mind tonight. Wash away the accumulated anxieties of the day, and restore peaceful harmony to my emotions. Let your gentle wisdom guide my intuition, and bless my relationships with deep empathy and understanding.",
        "candle_ritual": "Light a white or silver candle on Monday evening. Drink a glass of pure filtered water in silence while looking at the candle flame, setting the intention of emotional purity and restful sleep.",
        "affirmation": "My mind is peaceful as still water. I trust my inner guidance, and I nurture harmony in every encounter."
    },
    3: {
        "prayer_name": "Midday Wisdom & Abundance Thanksgiving",
        "prayer_text": "Sovereign Creator, fountain of all wisdom and prosperity, expand my understanding. Teach me to discern truth from illusion, and grant me the humility to remain a lifelong student. May the abundance I receive flow outward to uplift my family, colleagues, and community.",
        "candle_ritual": "Light an amber or deep yellow candle at Thursday midday. Spend 5 minutes reviewing one inspiring passage of wisdom or Scripture, holding gratitude for three living mentors who shaped your path.",
        "affirmation": "I am open to infinite wisdom and ethical prosperity. My knowledge expands, and my life is a channel of positive abundance."
    },
    4: {
        "prayer_name": "Twilight Alignment for Focus & Breakthrough",
        "prayer_text": "Architect of the Universe, ground my restless thoughts and focus my energies. Where there is confusion, bring clear order; where there is sudden disruption, reveal the hidden opportunity. Shield my mind from distraction and grant me the discipline to build lasting foundations.",
        "candle_ritual": "Light a blue or charcoal candle at Wednesday or Saturday twilight. Place a piece of smoky quartz or clear glass beside the flame. Write your single most important weekly goal and place it under the stone.",
        "affirmation": "I am grounded, steady, and clear. Sudden changes reveal higher paths, and my focus remains unbreakable."
    },
    5: {
        "prayer_name": "Morning Commerce & Persuasion Blessing",
        "prayer_text": "Gracious Creator, bless the words of my mouth and the works of my hands. Bestow clarity upon my negotiations, honesty upon my trade, and genuine goodwill in all my communications. Let my endeavors foster fruitful enterprise and mutual prosperity.",
        "candle_ritual": "Light a pale green candle on Wednesday morning before starting business communications. Take three deep breaths, visualize emerald light at your throat center, and mentally review your core conversations with calm confidence.",
        "affirmation": "My communication is clear, persuasive, and gracious. Opportunities flow easily, and my business thrives in honesty."
    },
    6: {
        "prayer_name": "Twilight Prayer of Sacred Harmony & Love",
        "prayer_text": "Divine Artist of the Cosmos, fill my home and heart with your peace. Heal any discord in my relationships, soften harsh words, and awaken sincere appreciation for the beauty that surrounds me. May love guide my decisions, and may elegance accompany my actions.",
        "candle_ritual": "Light a rose-pink or cream candle on Friday evening. Place fresh flowers or a natural floral essence in your room. Sit quietly for 5 minutes sending conscious blessings to your partner, family, and friendships.",
        "affirmation": "I radiate warmth, beauty, and gracious love. My relationships are harmonious, and my life attracts joyful abundance."
    },
    7: {
        "prayer_name": "Contemplative Prayer of Solitude & Insight",
        "prayer_text": "Omniscient Spirit, in the quiet sanctuary of my soul, I seek your presence. Still the noisy demands of the external world, and grant me insight into the deeper meaning of my journey. Cleanse my heart of hidden attachments, and guide my steps toward enduring truth.",
        "candle_ritual": "Light a lavender or white candle in a quiet, darkened room on Tuesday or Saturday evening. Sit in complete silence without digital devices for 10 minutes, practicing silent mindful breathing.",
        "affirmation": "I am centered in quiet truth. Beyond worldly noise, I hear the whispers of wisdom that direct my highest path."
    },
    8: {
        "prayer_name": "Saturday Prayer of Fortitude & Monumental Patience",
        "prayer_text": "Eternal Lord of Time and Justice, grant me the fortitude to endure, the patience to persist, and the wisdom to respect divine timing. Help me to shoulder my responsibilities without bitterness, and transform every delay into strength of character and enduring achievement.",
        "candle_ritual": "Light a deep navy or dark violet candle on Saturday late afternoon. Reflect on one past difficulty that ultimately made you stronger, giving thanks for the resilience you gained.",
        "affirmation": "I possess boundless endurance and steadfast faith. Through disciplined patience, I construct a legacy that stands the test of time."
    },
    9: {
        "prayer_name": "Morning Invocation of Courage & Protection",
        "prayer_text": "Almighty Protector, kindle within me righteous courage and unwavering stamina. Guard my loved ones from harm, keep my heart free from reckless wrath, and empower me to stand firmly for justice and truth. Let my strength be a refuge for the weak.",
        "candle_ritual": "Light a deep red or terracotta candle on Tuesday morning. Stand upright with shoulders back, taking 5 strong, energizing breaths while affirming physical health and courageous determination.",
        "affirmation": "I am courageous, resilient, and protective. My energy is guided by wisdom, and I conquer obstacles with purposeful resolve."
    }
}

# ─────────────────────────────────────────────────────────────────────────────
# 4. ENGLISH NAME ANALYSIS & SIGNATURE VIBRATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────
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

def analyze_english_name_acoustics(full_name: str) -> Dict[str, Any]:
    """
    Deconstructs English full names into First, Middle, and Last name acoustics,
    evaluating Chaldean compound numbers, soul urge (vowels), and professional signature rules.
    """
    parts = [p.strip() for p in re.split(r'\s+', full_name.strip()) if p.strip()]
    if not parts:
        parts = ["Friend"]

    from app.engine.digit_root import digit_root

    def calc_word(w: str) -> Dict[str, Any]:
        clean = re.sub(r'[^A-Za-z]', '', w).upper()
        comp = sum(CHALDEAN_MAP.get(c, 0) for c in clean)
        root = digit_root(comp)
        return {"word": w, "clean": clean, "compound": comp, "root": root}

    first_data = calc_word(parts[0])
    last_data = calc_word(parts[-1]) if len(parts) > 1 else first_data
    middle_data = [calc_word(p) for p in parts[1:-1]] if len(parts) > 2 else []

    # Vowels (Soul Urge) vs Consonants (Outer Personality)
    vowels = set("AEIOU")
    clean_all = re.sub(r'[^A-Za-z]', '', full_name).upper()
    vowel_sum = sum(CHALDEAN_MAP.get(c, 0) for c in clean_all if c in vowels)
    vowel_root = digit_root(vowel_sum)

    consonant_sum = sum(CHALDEAN_MAP.get(c, 0) for c in clean_all if c not in vowels)
    consonant_root = digit_root(consonant_sum)

    total_sum = sum(CHALDEAN_MAP.get(c, 0) for c in clean_all)
    total_root = digit_root(total_sum)

    signature_advice = (
        "Sign with an intentional 15-degree upward slope to activate continuous professional elevation. "
        "Keep the first letter distinct, elegant, and capitalized. Ensure your underline begins after the first initial "
        "and finishes with a clean forward stroke without striking through any descending letter stems."
    )

    return {
        "full_name": full_name,
        "first_name_acoustic": first_data,
        "last_name_acoustic": last_data,
        "middle_names": middle_data,
        "total_compound": total_sum,
        "total_root": total_root,
        "soul_urge_vowels": {"compound": vowel_sum, "root": vowel_root},
        "outer_personality_consonants": {"compound": consonant_sum, "root": consonant_root},
        "signature_guidance": signature_advice
    }

# ─────────────────────────────────────────────────────────────────────────────
# 5. MASTER DISPATCHER: GET INTERNATIONAL REMEDIES
# ─────────────────────────────────────────────────────────────────────────────
def get_international_planetary_remedies(
    driver: int,
    conductor: int,
    missing_numbers: List[int],
    name: str = "Seeker"
) -> Dict[str, Any]:
    """
    Generates culturally adapted, internationally resonant remedies for Rest-of-World seekers.
    Strictly focuses on:
    - English name acoustic balancing
    - Targeted non-profit donations & planetary charitable giving (Dana)
    - Inclusive universal prayers, Solfeggio sound tuning & contemplative candle rituals
    - Modern lifestyle & workspace harmonizers
    """
    d_arch = INTERNATIONAL_PLANET_ARCHETYPES.get(driver, INTERNATIONAL_PLANET_ARCHETYPES[1])
    c_arch = INTERNATIONAL_PLANET_ARCHETYPES.get(conductor, INTERNATIONAL_PLANET_ARCHETYPES[1])

    d_charity = INTERNATIONAL_CHARITY_CATALOGUE.get(driver, INTERNATIONAL_CHARITY_CATALOGUE[1])
    c_charity = INTERNATIONAL_CHARITY_CATALOGUE.get(conductor, INTERNATIONAL_CHARITY_CATALOGUE[1])

    d_ritual = INTERNATIONAL_RITUALS_CATALOGUE.get(driver, INTERNATIONAL_RITUALS_CATALOGUE[1])
    c_ritual = INTERNATIONAL_RITUALS_CATALOGUE.get(conductor, INTERNATIONAL_RITUALS_CATALOGUE[1])

    # Name acoustics
    name_analysis = analyze_english_name_acoustics(name)

    # Missing numbers international charity supports
    missing_supports = []
    for miss in missing_numbers[:3]:  # Top 3 missing energies
        if miss in INTERNATIONAL_PLANET_ARCHETYPES and miss in INTERNATIONAL_CHARITY_CATALOGUE:
            m_arch = INTERNATIONAL_PLANET_ARCHETYPES[miss]
            m_char = INTERNATIONAL_CHARITY_CATALOGUE[miss]
            missing_supports.append({
                "missing_number": miss,
                "planetary_energy": m_arch["planet"],
                "lifestyle_gap": f"Absence of Number {miss} ({m_arch['keyword']})",
                "charitable_remedy": m_char["recommended_giving"],
                "daily_act": m_char["everyday_act"],
                "color_tuning": m_arch["attuned_colors"]
            })

    return {
        "market": "INTERNATIONAL_REST_OF_WORLD",
        "client_name": name,
        "core_numbers": {
            "solar_driver": {"number": driver, "archetype": d_arch["archetype"], "planet": d_arch["planet"]},
            "destiny_conductor": {"number": conductor, "archetype": c_arch["archetype"], "planet": c_arch["planet"]}
        },
        "english_name_acoustics": name_analysis,
        "primary_charitable_giving": {
            "driver_charity": {
                "planet": d_arch["planet"],
                "timing": d_charity["timing"],
                "cause_focus": d_charity["cause_focus"],
                "recommended_action": d_charity["recommended_giving"],
                "everyday_generosity": d_charity["everyday_act"],
                "karmic_intention": d_charity["karmic_intention"]
            },
            "conductor_charity": {
                "planet": c_arch["planet"],
                "timing": c_charity["timing"],
                "cause_focus": c_charity["cause_focus"],
                "recommended_action": c_charity["recommended_giving"],
                "everyday_generosity": c_charity["everyday_act"],
                "karmic_intention": c_charity["karmic_intention"]
            }
        },
        "universal_contemplative_rituals": {
            "primary_prayer": {
                "title": d_ritual["prayer_name"],
                "prayer_text": d_ritual["prayer_text"],
                "candle_ceremony": d_ritual["candle_ritual"],
                "daily_affirmation": d_ritual["affirmation"],
                "sound_frequency": d_arch["solfeggio_freq"]
            },
            "destiny_prayer": {
                "title": c_ritual["prayer_name"],
                "prayer_text": c_ritual["prayer_text"],
                "candle_ceremony": c_ritual["candle_ritual"],
                "daily_affirmation": c_ritual["affirmation"],
                "sound_frequency": c_arch["solfeggio_freq"]
            }
        },
        "missing_frequency_charitable_bridges": missing_supports,
        "environmental_harmonizers": {
            "power_colors": d_arch["attuned_colors"],
            "colors_to_minimize": d_arch["avoid_colors"],
            "harmonic_metals": d_arch["harmonic_metal"],
            "healing_crystals": d_arch["healing_crystals"],
            "prime_day_of_action": d_arch["day_of_power"],
            "workspace_orientation": f"Face {d_arch['cardinal_direction']} for prime executive focus and decision-making."
        }
    }
