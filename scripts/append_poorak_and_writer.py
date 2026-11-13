# -*- coding: utf-8 -*-
"""
Helper to append Complementary Poorak engine and write_all_files to generate_all_master_registries.py
"""

code_to_append = '''

def get_complementary_poorak_data():
    """
    Master Complementary (Poorak / पूरक) Numbers Knowledge Base.
    Acts as the cosmic peacemaker and grid-completion harmonizer.
    """
    return {
        "master_poorak_map": {
            1: {"complementary": [9], "planet": "Mars (Mangal)", "role": "Provides executive courage, physical vitality, and fearless action to Sun's leadership."},
            2: {"complementary": [5, 7], "planet": "Mercury & Ketu", "role": "Mercury (5) provides rational communication and commercial stability to Moon's sensitivity; Ketu (7) provides intuitive spiritual alignment."},
            3: {"complementary": [5, 7], "planet": "Mercury & Ketu", "role": "Mercury (5) monetizes and commercially structures Jupiter's wisdom; Ketu (7) deepens divine esoteric research."},
            4: {"complementary": [8], "planet": "Saturn (Shani)", "role": "Provides grounded physical discipline, legal compliance, and structural stamina to Rahu's unconventional systems."},
            5: {"complementary": [1, 6], "planet": "Universal Master Key", "role": "Number 5 is the Universal Balancer (Mercury); neutral and friendly to all. Supported by Sun (1) for authority and Venus (6) for luxury."},
            6: {"complementary": [5], "planet": "Mercury (Budh)", "role": "Provides witty commercial networking and agile dealmaking to Venusian luxury and domestic aesthetics."},
            7: {"complementary": [3], "planet": "Jupiter (Guru)", "role": "Provides structured philosophical teaching, public mentorship, and ethical direction to Ketu's solitary insights."},
            8: {"complementary": [4, 5], "planet": "Rahu & Mercury", "role": "Rahu (4) provides unconventional system engineering; Mercury (5) provides commercial flexibility and diplomatic speed to Saturnian rigidity."},
            9: {"complementary": [1], "planet": "Sun (Surya)", "role": "Provides sovereign executive command, public status, and noble direction to Martian physical force and raw energy."}
        },
        "friction_pair_peacemakers": {
            "1_8": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 dissolves Sun-Saturn father-son friction with commerce, diplomacy, and neutral mental agility."},
            "8_1": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 dissolves Saturn-Sun authority deadlock through contractual flexibility and commercial compromise."},
            "2_4": {"poorak": 6, "peacemaker_planet": "Venus (Shukra)", "rationale": "Number 6 soothes Moon-Rahu eclipse anxiety through aesthetic beauty, domestic harmony, and gentle luxury."},
            "4_2": {"poorak": 6, "peacemaker_planet": "Venus (Shukra)", "rationale": "Number 6 softens Rahu-Moon mental turbulence with artistic grace and emotional reassurance."},
            "2_8": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 stabilizes Moon-Saturn Vish Yoga depression through active logical communication and commercial focus."},
            "8_2": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 overcomes Saturn-Moon chronic delays with energetic adaptability and social networking."},
            "2_9": {"poorak": 1, "peacemaker_planet": "Sun (Surya)", "rationale": "Number 1 brings noble sovereign harmony to Moon-Mars fire-water volatility, commanding mutual respect."},
            "9_2": {"poorak": 1, "peacemaker_planet": "Sun (Surya)", "rationale": "Number 1 grounds Mars-Moon emotional clashes through dignified executive purpose."},
            "3_6": {"poorak": 7, "peacemaker_planet": "Ketu (South Node)", "rationale": "Number 7 reconciles Dev Guru (3) and Daitya Guru (6) by transmuting luxury into sacred philanthropy and high healing insight."},
            "6_3": {"poorak": 7, "peacemaker_planet": "Ketu (South Node)", "rationale": "Number 7 harmonizes Venus-Jupiter 36 ka aankda through spiritual detachment and deep holistic research."},
            "4_4": {"poorak": 6, "peacemaker_planet": "Venus (Shukra)", "rationale": "Number 6 cools dual Rahu erratic disruptions with domestic peace, artistic elegance, and luxury comfort."},
            "4_8": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 breaks Rahu-Saturn dark karmic stagnation through light commercial movement and flexible trading."},
            "8_4": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 introduces agile communication to Saturn-Rahu heavy delays, unlocking contractual progress."},
            "4_9": {"poorak": 6, "peacemaker_planet": "Venus (Shukra)", "rationale": "Number 6 cools Rahu-Mars Angarak combative tension with diplomatic charm and aesthetic pacing."},
            "9_4": {"poorak": 6, "peacemaker_planet": "Venus (Shukra)", "rationale": "Number 6 tempers Mars-Rahu surgical aggression with peaceful luxury and balanced restraint."},
            "6_9": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 grounds Venus-Mars passion scandal risk through sharp intellect, witty communication, and objective logic."},
            "9_6": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 channels Mars-Venus volatile emotional friction into active commercial marketing and creative trade."},
            "7_7": {"poorak": 1, "peacemaker_planet": "Sun (Surya)", "rationale": "Number 1 gives a sovereign executive head and clear goal direction to dual headless Ketus."},
            "8_8": {"poorak": 5, "peacemaker_planet": "Mercury (Budh)", "rationale": "Number 5 relieves double Saturn heavy labor with commercial ease, trade agility, and intellectual joy."},
            "9_9": {"poorak": 1, "peacemaker_planet": "Sun (Surya)", "rationale": "Number 1 channels double Mars volcanic anger into righteous sovereign leadership and noble public service."}
        }
    }


def write_all_files():
    print("Beginning master file export...")
    subdates = get_subdates_data()
    dc81 = get_driver_conductor_81_data()
    hygiene = get_five_elements_hygiene_data()
    poorak_data = get_complementary_poorak_data()

    # 1. Write app/data/birth_subdates_registry.json
    os.makedirs("app/data", exist_ok=True)
    with open("app/data/birth_subdates_registry.json", "w", encoding="utf-8") as f:
        json.dump(subdates, f, indent=2, ensure_ascii=False)
    print("? Saved app/data/birth_subdates_registry.json (31 days)")

    # 2. Write data/knowledge_base/driver_conductor_81_rules.json
    os.makedirs("data/knowledge_base", exist_ok=True)
    with open("data/knowledge_base/driver_conductor_81_rules.json", "w", encoding="utf-8") as f:
        json.dump(dc81, f, indent=2, ensure_ascii=False)
    print("? Saved data/knowledge_base/driver_conductor_81_rules.json (81 rules)")

    # 3. Write app/engine/driver_conductor_81_engine.py
    engine_code = '''# -*- coding: utf-8 -*-
"""
DRIVER CONDUCTOR 81 COMBINATIONS DETERMINISTIC ENGINE
Numeros Vision — Master Knowledge Engine
100% Deterministic O(1) Lookup Authority for Driver-Conductor Synergies.
"""

from typing import Dict, Any, Optional
import json
import os

_RULES_CACHE: Optional[Dict[str, Any]] = None

def _load_rules() -> Dict[str, Any]:
    global _RULES_CACHE
    if _RULES_CACHE is None:
        path = os.path.join(os.path.dirname(__file__), "..", "..", "data", "knowledge_base", "driver_conductor_81_rules.json")
        path = os.path.normpath(path)
        with open(path, "r", encoding="utf-8") as f:
            _RULES_CACHE = json.load(f)
    return _RULES_CACHE

def lookup_driver_conductor_81(driver: int, conductor: int) -> Dict[str, Any]:
    """
    O(1) Fast lookup for Driver-Conductor synergy.
    Returns:
        - driver, conductor, key
        - driver_planet, conductor_planet, planet_combination
        - relationship_type ('Friendly', 'Neutral', 'Enemy')
        - star_rating (float 0.5 to 5.0)
        - star_display (e.g. '★★★★★ (5/5 Stars — Super Success)')
        - synergy_title, positive_traits, negative_traits, recommended_careers
        - warnings_and_cautions, harmonizing_poorak_number, fast_summary
    """
    rules = _load_rules()
    key = f"{driver}_{conductor}"
    if key in rules:
        return rules[key]
    
    # Fallback calculation if key missing
    return {
        "driver": driver, "conductor": conductor, "key": key,
        "driver_planet": "Unknown", "conductor_planet": "Unknown",
        "planet_combination": f"Driver {driver} - Conductor {conductor}",
        "relationship_type": "Neutral", "star_rating": 3.0,
        "star_display": "★★★☆☆ (3/5 Stars — Moderate Balance)",
        "synergy_title": f"{driver}-{conductor}: Synergy Profile",
        "positive_traits": ["Balanced determination", "Independent capability"],
        "negative_traits": ["Needs alignment"],
        "recommended_careers": ["General Business", "Administration"],
        "warnings_and_cautions": "Ensure regular balancing of Lo Shu Grid elements.",
        "harmonizing_poorak_number": 5,
        "fast_summary": f"Driver {driver} and Conductor {conductor} operate with moderate synergy; balance via Number 5."
    }
'''
    with open("app/engine/driver_conductor_81_engine.py", "w", encoding="utf-8") as f:
        f.write(engine_code)
    print("? Saved app/engine/driver_conductor_81_engine.py")

    # 4. Write app/engine/five_elements_hygiene_engine.py
    hygiene_code = '''# -*- coding: utf-8 -*-
"""
FIVE ELEMENTS (PANCH TATTVA) HYGIENE & BODYGUARDS ENGINE
Numeros Vision — Master Knowledge Engine
Authoritative implementation of Dr. Numeros Vision Classical Methodology's Panch Tattva Bodyguard Hygiene.
Non-negotiable Step 0 shielding required before gemstones or complex rituals.
"""

from typing import Dict, Any, List, Optional
import json

FIVE_ELEMENTS_HYGIENE = ''' + json.dumps(hygiene, indent=4, ensure_ascii=False) + '''

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
        "element": "Wood (Air/Space)", "numbers": [3, 4], "status": "URGENT_SHIELD" if wood_missing else "PROTECTIVE_CUSHION",
        "prescription": wood_item,
        "instruction": "Must touch physical skin continuously on wrist or neck.",
        "caution": "Avoid Tulsi if consuming non-vegetarian food; use Rudraksha or Sandalwood instead.",
        "benefits": "Protects vital aura, balances heart center, prevents energetic depletion."
    })
    
    # Earth (2, 5, 8)
    earth_missing = any(n in missing_numbers for n in [2, 5, 8])
    prescriptions.append({
        "element": "Earth", "numbers": [2, 5, 8], "status": "URGENT_SHIELD" if earth_missing else "PROTECTIVE_CUSHION",
        "prescription": "Natural Clear White Quartz (Sphatik) 10mm-12mm bead bracelet or mala",
        "instruction": "Wear on left wrist or around neck touching chest.",
        "properties": "Remains naturally cold even under direct sun; grounds electromagnetic stress.",
        "benefits": "Regulates blood pressure, soothes aggression, stabilizes mental over-thinking."
    })
    
    # Fire (9)
    fire_missing = 9 in missing_numbers
    prescriptions.append({
        "element": "Fire", "numbers": [9], "status": "URGENT_SHIELD" if fire_missing else "PROTECTIVE_CUSHION",
        "prescription": "Sacred Red Thread (Mauli / Kalawa) on right wrist + 15 min morning sunlight",
        "instruction": "Tie red cotton mauli on wrist; apply red tilak (Ashtagandha/Roli) on throat or third eye.",
        "color_clarity": "Element balancer, not a planet garment; safe for everyone regardless of birth numbers.",
        "benefits": "Kindles vital cellular energy, strengthens digestion (Agni), banishes lethargy."
    })
    
    # Water (1)
    water_missing = 1 in missing_numbers
    prescriptions.append({
        "element": "Water", "numbers": [1], "status": "URGENT_SHIELD" if water_missing else "PROTECTIVE_CUSHION",
        "prescription": "Drink water from a Pure Copper Bottle / Sipper in small mindful sips",
        "instruction": "Carry a 250ml-500ml copper bottle daily; offer morning water arghya to Sun.",
        "benefits": "Rehydrates 76% of body water constitution, flushes toxins, activates career flow."
    })
    
    # Metal / Air (6, 7)
    metal_missing = 6 in missing_numbers or 7 in missing_numbers
    prescriptions.append({
        "element": "Metal / Air", "numbers": [6, 7], "status": "URGENT_SHIELD" if metal_missing else "PROTECTIVE_CUSHION",
        "prescription": "Metallic chain watch (Silver for 7, Gold/Brass for 6, or Dual-Tone for both)",
        "instruction": "Wear metallic watch daily on wrist to act as a cosmic antenna.",
        "benefits": "Harmonizes nervous meridians, sharpens discernment, attracts supportive luxury networks."
    })
    
    return {
        "title": "Panch Tattva Five Elements Bodyguard Hygiene",
        "summary": "Non-negotiable elemental baseline required before gemstones or complex rituals.",
        "prescriptions": prescriptions
    }
'''
    with open("app/engine/five_elements_hygiene_engine.py", "w", encoding="utf-8") as f:
        f.write(hygiene_code)
    print("? Saved app/engine/five_elements_hygiene_engine.py")

    # 5. Write app/engine/complementary_poorak_engine.py
    poorak_code = '''# -*- coding: utf-8 -*-
"""
COMPLEMENTARY (POORAK / पूरक) NUMBERS ENGINE
Numeros Vision — Master Knowledge Engine
Calculates the harmonizing peacemaker number and Lo Shu grid completion anchor.
"""

from typing import Dict, Any, List, Optional
import json

POORAK_DATA = ''' + json.dumps(poorak_data, indent=4, ensure_ascii=False) + '''

def calculate_complementary_poorak(driver: int, conductor: int, missing_numbers: Optional[List[int]] = None) -> Dict[str, Any]:
    """
    Calculates the Poorak (Complementary / Harmonizing) Number:
    1. If Driver and Conductor have friction, identifies the specific peacemaker planet.
    2. If Driver and Conductor are friendly, identifies the prime missing number (5 or 6).
    3. Returns full ritual, colors, vastu direction, and daily practical action.
    """
    key = f"{driver}_{conductor}"
    friction_rules = POORAK_DATA["friction_pair_peacemakers"]
    master_map = POORAK_DATA["master_poorak_map"]
    
    planet_details = {
        1: {"planet": "Sun (Surya)", "element": "Water/Fire Core", "color": "Gold, Saffron, Amber", "direction": "North / East"},
        2: {"planet": "Moon (Chandra)", "element": "Earth/Water", "color": "Pearl White, Silver", "direction": "South-West / North-West"},
        3: {"planet": "Jupiter (Guru)", "element": "Wood", "color": "Yellow, Golden Yellow", "direction": "East / North-East"},
        4: {"planet": "Rahu (North Node)", "element": "Wood", "color": "Smoky Blue, Gray", "direction": "South-East"},
        5: {"planet": "Mercury (Budh)", "element": "Earth", "color": "Emerald Green, Mint", "direction": "Center (Brahma Sthana)"},
        6: {"planet": "Venus (Shukra)", "element": "Metal (Gold)", "color": "White, Cream, Rose Gold", "direction": "North-West"},
        7: {"planet": "Ketu (South Node)", "element": "Metal (Silver)", "color": "Silver, Smoky White", "direction": "West"},
        8: {"planet": "Saturn (Shani)", "element": "Earth", "color": "Navy Blue, Charcoal", "direction": "North-East / West"},
        9: {"planet": "Mars (Mangal)", "element": "Fire", "color": "Crimson Red, Maroon", "direction": "South"}
    }
    
    if key in friction_rules:
        item = friction_rules[key]
        p_num = item["poorak"]
        p_info = planet_details.get(p_num, planet_details[5])
        return {
            "poorak_number": p_num,
            "poorak_planet": p_info["planet"],
            "poorak_element": p_info["element"],
            "poorak_color": p_info["color"],
            "poorak_direction": p_info["direction"],
            "is_friction_resolution": True,
            "synergy_type": "Friction Peacemaker Bridge",
            "rationale": item["rationale"],
            "harmonizing_ritual": f"Activate Number {p_num} by incorporating {p_info['color'].split(',')[0]} accents and balancing the {p_info['direction']} sector of your primary room."
        }
    
    # Friendly or Neutral: Check missing numbers or master complementary
    if missing_numbers and 5 in missing_numbers:
        p_num = 5
        rationale = "Number 5 (Mercury) fills the central Earth anchor of your Lo Shu Grid, providing unshakable emotional stability and commercial compounding."
    elif missing_numbers and 6 in missing_numbers:
        p_num = 6
        rationale = "Number 6 (Venus) completes your luxury and supportive networks plane, attracting high-net-worth mentors and material comfort."
    else:
        # Pull from master poorak map
        comp_list = master_map.get(driver, {}).get("complementary", [5])
        p_num = comp_list[0] if isinstance(comp_list[0], int) else 5
        rationale = master_map.get(driver, {}).get("role", "Serves as the complementary cosmic amplifier for your Driver-Conductor alliance.")
    
    p_info = planet_details.get(p_num, planet_details[5])
    return {
        "poorak_number": p_num,
        "poorak_planet": p_info["planet"],
        "poorak_element": p_info["element"],
        "poorak_color": p_info["color"],
        "poorak_direction": p_info["direction"],
        "is_friction_resolution": False,
        "synergy_type": "Grid Completion & Cosmic Amplifier",
        "rationale": rationale,
        "harmonizing_ritual": f"Activate Number {p_num} by incorporating {p_info['color'].split(',')[0]} accents and balancing the {p_info['direction']} sector of your primary room."
    }
'''
    with open("app/engine/complementary_poorak_engine.py", "w", encoding="utf-8") as f:
        f.write(poorak_code)
    print("? Saved app/engine/complementary_poorak_engine.py")

    # 6. Update app/engine/number_characteristics_registry.py
    with open("app/engine/number_characteristics_registry.py", "r", encoding="utf-8") as f:
        reg_text = f.read()

    marker = "# ?? DR. Numeros Vision Classical Methodology DAY 6 CANONICAL SUB-DATE & NUMBER CHARACTERISTICS ????"
    idx = reg_text.find(marker)
    if idx != -1:
        base_code = reg_text[:idx]
    else:
        base_code = reg_text

    subdates_export_code = f"""# ?? DR. Numeros Vision Classical Methodology DAY 6 CANONICAL SUB-DATE & NUMBER CHARACTERISTICS ????
# Canonical sub-date registry populated deterministically from verified RAG literature.
# Defines Categories A (Good), B (Normal), C (Lower), D (Karmic Debt) for all 31 birth days.

STRENGTH_CATEGORY_DEFINITIONS = {{
    "A": {{
        "grade": "Category A — Good Strength (High Potency / Direct Manifestation)",
        "potency_range": "88% – 96% Intrinsic Ease",
        "definition": "High vibrational ease, strong inherent manifestation power, royal or visionary drive. Requires conscious humility to prevent ego friction.",
        "days": ["19(a)", "11(a)", "12(a)", "22(a)", "14(a)", "15(a)", "16(a)", "8(a)", "9(a)"]
    }},
    "B": {{
        "grade": "Category B — Normal Strength (Balanced / Steady Growth)",
        "potency_range": "72% – 84% Potency",
        "definition": "Balanced, workable potency. Success compounds through steady effort, disciplined partnership, and emotional grounding.",
        "days": ["1(b)", "10(b)", "2(b)", "20(b)", "21(b)", "31(b)", "23(b)", "6(b)", "25(b)", "17(b)", "27(b)"]
    }},
    "C": {{
        "grade": "Category C — Lower Strength (High Friction / Intensive Lesson)",
        "potency_range": "52% – 68% Direct Ease",
        "definition": "Challenging compound tension, contradictory planetary elements, or initial inertia. Demands patience, elemental remedies, and structured routine.",
        "days": ["28(c)", "29(c)", "3(c)", "30(c)", "4(c)", "5(c)", "24(c)", "7(c)", "26(c)", "18(c)"]
    }},
    "D": {{
        "grade": "Category D — Karmic Debt Transformation (Intense Crucible)",
        "potency_range": "58% Initial Ease jumping to 92% Post-Mastery",
        "definition": "Rigorous karmic crucible requiring physical discipline and perseverance without shortcuts. Turns trials into master-builder foundations.",
        "days": ["13(d)"]
    }}
}}

BIRTH_DAY_SUBDATE_REGISTRY = {json.dumps(subdates, indent=4, ensure_ascii=False)}
"""

    with open("app/engine/number_characteristics_registry.py", "w", encoding="utf-8") as f:
        f.write(base_code + subdates_export_code)
    print("? Updated app/engine/number_characteristics_registry.py with full 31 subdates")

    print("\\n??? ALL MASTER REGISTRIES SUCCESSFULLY BUILT! ???")


if __name__ == "__main__":
    write_all_files()
'''

with open('scripts/generate_all_master_registries.py', 'a', encoding='utf-8') as f:
    f.write(code_to_append)

print("Appended poorak and write_all_files to generate_all_master_registries.py")
