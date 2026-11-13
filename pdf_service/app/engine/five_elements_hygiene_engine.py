# -*- coding: utf-8 -*-
"""
FIVE ELEMENTS (PANCH TATTVA) HYGIENE & BODYGUARDS ENGINE
Numeros Vision — Master Knowledge Engine
Authoritative implementation of Numeros Vision Classical Methodology Panch Tattva Bodyguard Hygiene.
Non-negotiable Step 0 shielding required before gemstones or complex rituals.
"""

from typing import Dict, Any, List, Optional

FIVE_ELEMENTS_HYGIENE = {
    "WOOD": {
        "element": "Wood",
        "tattva_hindi": "वृहस्पत / अन्तरिक्ष / वायु (Wood / Growth)",
        "associated_numbers": [
            3,
            4
        ],
        "governing_planets": [
            "Jupiter (Guru / Dev Guru)",
            "Rahu (North Node / Shadow Architect)"
        ],
        "governing_cardinal_directions": [
            "East (Jupiter)",
            "South-East (Rahu)"
        ],
        "vital_organs_and_aura": "Heart equilibrium, vital aura shielding, spiritual expansion, personal growth",
        "hygiene_prescription": {
            "core_rule": "Wear touching skin comfortably (as a bracelet, necklace, or mala) for natural grounding.",
            "item_options": [
                "Natural 5-Mukhi Rudraksha bracelet or mala (Universal, highly recommended)",
                "Tulsi mala or bracelet (FOR STRICT VEGETARIANS ONLY; do NOT wear if consuming non-vegetarian food)",
                "Natural sandalwood (Chandan) beads or wooden bangle"
            ],
            "dietary_diet_caveat": "Those following vegetarian traditions may prefer Tulsi, while natural Rudraksha or Sandalwood is universally suited for all.",
            "why_it_protects": "Supports natural energetic grounding and steady calm throughout busy workdays."
        }
    },
    "EARTH": {
        "element": "Earth",
        "tattva_hindi": "पृथ्वी (Earth / Stability)",
        "associated_numbers": [
            2,
            5,
            8
        ],
        "governing_planets": [
            "Moon (Chandra)",
            "Mercury (Budh)",
            "Saturn (Shani)"
        ],
        "governing_cardinal_directions": [
            "South-West (Moon)",
            "Center / Brahma Sthana (Mercury)",
            "North-East (Saturn)"
        ],
        "vital_organs_and_aura": "Blood pressure regulation, anger cooling, mental stability, decisive grounding, electromagnetic balance",
        "hygiene_prescription": {
            "core_rule": "Wear a natural Clear White Quartz (Sphatik / White Quartz) bracelet or mala (10mm to 12mm beads).",
            "properties": "Sphatik remains naturally icy-cold even under direct scorching sunlight, drawing electromagnetic heat out of the body.",
            "item_options": [
                "White Quartz (Sphatik) 10mm-12mm bead bracelet on left or right wrist",
                "Sphatik mala worn around the neck touching throat/chest chakra"
            ],
            "why_it_protects": "Soothes blood pressure, arrests volcanic aggression, grounds erratic overthinking, and restores earth stability."
        }
    },
    "FIRE": {
        "element": "Fire",
        "tattva_hindi": "अग्नि (Fire / Vitality)",
        "associated_numbers": [
            9
        ],
        "governing_planets": [
            "Mars (Mangal / Senapati)"
        ],
        "governing_cardinal_directions": [
            "South (Mars)"
        ],
        "vital_organs_and_aura": "Cellular vitality, digestive fire (Agni), courage, proactive initiative, immune resistance, Vitamin D synthesis",
        "hygiene_prescription": {
            "core_rule": "Tie a sacred red thread (Mauli / Kalawa) on right wrist; apply red tilak (Ashtagandha / Roli); receive morning sunlight.",
            "item_options": [
                "Sacred red cotton thread (Mauli / Kalawa) tied on wrist",
                "Red Ashtagandha / Roli tilak on forehead or throat chakra daily",
                "15 minutes of early morning natural sunlight exposure (Surya Arghya)"
            ],
            "color_caveat": "Even if red is technically not a personal lucky number color, the red thread on wrist is an ELEMENTAL balancer, not a planet garment, so it causes ZERO harm.",
            "why_it_protects": "Ignites vital stamina, balances inner digestive fire, and wards off lethargy and chronic procrastination."
        }
    },
    "WATER": {
        "element": "Water",
        "tattva_hindi": "जल (Water / Flow)",
        "associated_numbers": [
            1
        ],
        "governing_planets": [
            "Sun (Surya - Life Giver)"
        ],
        "governing_cardinal_directions": [
            "North (Water / Career)"
        ],
        "vital_organs_and_aura": "76% of physical body constitution, cellular hydration, lymphatic purification, kidney vitality, career momentum",
        "hygiene_prescription": {
            "core_rule": "Carry a pure Copper bottle or sipper (Tambe ka bartan) and drink water in small mindful sips throughout the day.",
            "item_options": [
                "Pure Copper water bottle / small sipper (250ml - 500ml) carried in daily bag",
                "Jal Arghya (offering water in copper lota to morning sun with a pinch of red kumkum)",
                "Two daily bathing rituals for aura cleansing"
            ],
            "hydration_protocol": "Sipping copper-infused water in controlled small amounts revitalizes cellular energy and strengthens the North-career axis.",
            "why_it_protects": "Prevents dehydration, flushes cellular toxins, and ensures unobstructed flow in career and life direction."
        }
    },
    "METAL_AIR": {
        "element": "Metal / Air",
        "tattva_hindi": "धातु / वायु (Metal / Prana / Cosmic Harmony)",
        "associated_numbers": [
            6,
            7
        ],
        "governing_planets": [
            "Venus (Gold Metal / Shukra)",
            "Ketu (Silver Metal / Ketu)"
        ],
        "governing_cardinal_directions": [
            "North-West (Venus)",
            "West (Ketu)"
        ],
        "vital_organs_and_aura": "Nervous transmission, prana breathing, aesthetic grace, strategic detachment, cosmic electromagnetic conductivity",
        "hygiene_prescription": {
            "core_rule": "Wear a high-quality metallic chain watch on the wrist (Silver for 7, Gold/Brass for 6, or Dual-Tone for both).",
            "metal_breakdown": {
                "number_7_ketu": "Silver metallic chain watch (Silver represents Ketu and lunar-mental clarity).",
                "number_6_venus": "Gold or brass metallic chain watch (Gold represents Venusian luxury, abundance, and grace).",
                "dual_balancing": "Dual-Tone (Silver + Gold) metallic watch is universally optimal if seeking balance of both aesthetics and research."
            },
            "why_it_protects": "Acts as an electromagnetic antenna, harmonizing subtle air and metal prana throughout the body's nervous meridian system."
        }
    }
}

def get_five_elements_hygiene() -> Dict[str, Any]:
    """Returns the full canonical 5 Elements Hygiene specifications."""
    return FIVE_ELEMENTS_HYGIENE

def diagnose_user_elemental_hygiene(
    present_numbers: List[int],
    missing_numbers: List[int],
    dietary_preference: str = "vegetarian"
) -> Dict[str, Any]:
    """
    Diagnoses personal elemental shielding.
    Whether numbers are present or absent, each element must be balanced:
    - Missing numbers MUST perform the hygiene remedy.
    - Present numbers receive an extra protective cushion.
    """
    prescriptions = []
    
    # Wood (3, 4)
    wood_missing = 3 in missing_numbers or 4 in missing_numbers
    is_non_veg = dietary_preference.lower() in ["non_vegetarian", "non-vegetarian", "non-veg", "nonveg"]
    wood_item = "Natural 5-Mukhi Rudraksha bracelet or sandalwood beads" if is_non_veg else "Natural Rudraksha or Tulsi mala/bracelet"
    prescriptions.append({
        "element": "Wood (Air/Space)", "numbers": [3, 4], "status": "RECOMMENDED" if wood_missing else "SUPPORTIVE",
        "prescription": wood_item,
        "instruction": "Wear comfortably on wrist or neck for calm focus.",
        "caution": "Select Rudraksha or Sandalwood for universal wear.",
        "benefits": "Protects vital aura, balances heart center, prevents energetic depletion."
    })
    
    # Earth (2, 5, 8)
    earth_missing = any(n in missing_numbers for n in [2, 5, 8])
    prescriptions.append({
        "element": "Earth", "numbers": [2, 5, 8], "status": "RECOMMENDED" if earth_missing else "SUPPORTIVE",
        "prescription": "Natural Clear White Quartz (Sphatik) 10mm-12mm bead bracelet or mala",
        "instruction": "Wear on left wrist or around neck touching chest.",
        "properties": "Remains naturally cold even under direct sun; grounds electromagnetic stress.",
        "benefits": "Regulates blood pressure, soothes aggression, stabilizes mental over-thinking."
    })
    
    # Fire (9)
    fire_missing = 9 in missing_numbers
    prescriptions.append({
        "element": "Fire", "numbers": [9], "status": "RECOMMENDED" if fire_missing else "SUPPORTIVE",
        "prescription": "Sacred Red Thread (Mauli / Kalawa) on right wrist + 15 min morning sunlight",
        "instruction": "Tie red cotton mauli on wrist; apply red tilak (Ashtagandha/Roli) on throat or third eye.",
        "color_clarity": "Element balancer, not a planet garment; safe for everyone regardless of birth numbers.",
        "benefits": "Kindles vital cellular energy, strengthens digestion (Agni), banishes lethargy."
    })
    
    # Water (1)
    water_missing = 1 in missing_numbers
    prescriptions.append({
        "element": "Water", "numbers": [1], "status": "RECOMMENDED" if water_missing else "SUPPORTIVE",
        "prescription": "Drink water from a Pure Copper Bottle / Sipper in small mindful sips",
        "instruction": "Carry a 250ml-500ml copper bottle daily; offer morning water arghya to Sun.",
        "benefits": "Rehydrates 76% of body water constitution, flushes toxins, activates career flow."
    })
    
    # Metal / Air (6, 7)
    metal_missing = 6 in missing_numbers or 7 in missing_numbers
    prescriptions.append({
        "element": "Metal / Air", "numbers": [6, 7], "status": "RECOMMENDED" if metal_missing else "SUPPORTIVE",
        "prescription": "Metallic chain watch (Silver for 7, Gold/Brass for 6, or Dual-Tone for both)",
        "instruction": "Wear metallic watch daily on wrist to act as a cosmic antenna.",
        "benefits": "Harmonizes nervous meridians, sharpens discernment, attracts supportive luxury networks."
    })
    
    return {
        "title": "Panch Tattva Five Elements Bodyguard Hygiene",
        "summary": "Non-negotiable elemental baseline required before gemstones or complex rituals.",
        "prescriptions": prescriptions
    }
