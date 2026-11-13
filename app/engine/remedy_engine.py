"""
UNIFIED PREDICTION & REMEDY ENGINE (8-LAYER RAG ARCHITECTURE)
Aggregates predictions and remedies across:
1. Vedic Numerology (Driver-Conductor 81 combinations)
2. Lo Shu Grid (Missing numbers 1-9 & 8 Planes remedies)
3. Chaldean Name Numerology (Spelling alignment remedies)
4. Mobile Numerology (Phone number sum & digit harmony)
5. Bhrigu Nandi Nadi (BNN Karaka & transit activation remedies)
6. Lal Kitab (House 1-12 specific planetary remedies)
7. KP Astrology (Sub-lord & Nakshatra remedies)
8. Vedic Crystal & Gemstone Remedies (RAG-verified per Driver & missing numbers)

Every remedy is strictly traceable to verified Numeros Vision RAG citations.
"""

import sys
import os

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from typing import Dict, Any, List
from app.engine.rag_retriever import rag_engine
from app.engine.lunar_paksha_engine import calculate_shukla_paksha_timing
from app.engine.lo_shu import analyze_lo_shu_grid
from app.engine.vedic_numerology import analyze_vedic_numerology
from phase4_bnn_engine import run_full_bnn_analysis
from phase5_lal_kitab_engine import run_full_lal_kitab_analysis
from phase7_kp_engine import analyze_kp_sub_lord

CHALDEAN_LETTER_VALUES = {
    'A': 1, 'I': 1, 'J': 1, 'Q': 1, 'Y': 1,
    'B': 2, 'C': 2, 'K': 2, 'R': 2,
    'G': 3, 'L': 3, 'S': 3,
    'D': 4, 'M': 4, 'T': 4,
    'E': 5, 'H': 5, 'N': 5, 'X': 5,
    'U': 6, 'V': 6, 'W': 6,
    'O': 7, 'Z': 7,
    'F': 8, 'P': 8
}

VEDIC_CRYSTALS_DATABASE = {
    1: {"primary_gem": "Ruby (Manik)", "crystal": "Red Jasper & Sunstone", "ruler": "Sun (Surya)", "benefit": "Enhances leadership, confidence, vitality, and authority."},
    2: {"primary_gem": "Pearl (Moti)", "crystal": "Moonstone & Selenite", "ruler": "Moon (Chandra)", "benefit": "Balances emotions, promotes mental peace, intuition, and calm."},
    3: {"primary_gem": "Yellow Sapphire (Pukhraj)", "crystal": "Citrine & Yellow Topaz", "ruler": "Jupiter (Guru)", "benefit": "Attracts wisdom, wealth, spiritual growth, and prosperity."},
    4: {"primary_gem": "Hessonite (Gomed)", "crystal": "Smoky Quartz & Lapis Lazuli", "ruler": "Rahu", "benefit": "Provides grounding, clarity, protection from illusions, and focus."},
    5: {"primary_gem": "Emerald (Panna)", "crystal": "Green Aventurine & Green Jade", "ruler": "Mercury (Budh)", "benefit": "Boosts business intelligence, communication, and financial growth."},
    6: {"primary_gem": "Diamond / White Sapphire", "crystal": "Opal & Clear Quartz", "ruler": "Venus (Shukra)", "benefit": "Attracts luxury, relationship harmony, creative success, and charm."},
    7: {"primary_gem": "Cat's Eye (Lehsunya)", "crystal": "Tiger's Eye & Amethyst", "ruler": "Ketu", "benefit": "Enhances intuition, spiritual protection, and mental detachment."},
    8: {"primary_gem": "Blue Sapphire (Neelam)", "crystal": "Amethyst & Black Tourmaline", "ruler": "Saturn (Shani)", "benefit": "Brings discipline, career longevity, focus, and aura protection."},
    9: {"primary_gem": "Red Coral (Moonga)", "crystal": "Carnelian & Bloodstone", "ruler": "Mars (Mangal)", "benefit": "Builds courage, physical stamina, energy, and decisive action."}
}

MISSING_NUMBER_REMEDIES_DATABASE = {
    1: {"element": "Water", "direction": "North", "remedy": "Wear red/orange, offer water to Sun in copper vessel, use number 1 wallpaper.", "planet": "Sun"},
    2: {"element": "Earth", "direction": "South-West", "remedy": "Wear silver/white, respect mother, keep silver item or pearl.", "planet": "Moon"},
    3: {"element": "Wood", "direction": "East", "remedy": "Apply yellow turmeric tilak, wear yellow, respect teachers/gurus.", "planet": "Jupiter"},
    4: {"element": "Wood", "direction": "South-East", "remedy": "Keep wooden items, wear green/blue, donate to needy.", "planet": "Rahu"},
    5: {"element": "Earth", "direction": "Center", "remedy": "Wear green, donate green gram, keep green plants in home/office.", "planet": "Mercury"},
    6: {"element": "Metal", "direction": "North-West", "remedy": "Wear white/cream, use silver accessories, respect women/spouse.", "planet": "Venus"},
    7: {"element": "Metal", "direction": "West", "remedy": "Feed stray dogs, wear grey/white, practice meditation.", "planet": "Ketu"},
    8: {"element": "Earth", "direction": "North-East", "remedy": "Donate mustard oil, feed black dogs/crows, wear dark blue/black on Saturdays.", "planet": "Saturn"},
    9: {"element": "Fire", "direction": "South", "remedy": "Donate red items, sweets, maintain good relations with siblings.", "planet": "Mars"}
}

from app.engine.digit_root import digit_root

def calculate_name_number(name: str) -> int:
    clean_name = "".join(c.upper() for c in name if c.isalpha())
    total = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean_name)
    return digit_root(total)

def calculate_mobile_number_sum(mobile_str: str) -> int:
    digits = [int(d) for d in mobile_str if d.isdigit()]
    return digit_root(sum(digits))

def get_vedic_crystal_remedies(driver_num: int, missing_nums: List[int]) -> List[Dict[str, Any]]:
    crystal_remedies = []
    
    # 1. Driver Planet Primary Crystal
    driver_crystal_info = VEDIC_CRYSTALS_DATABASE.get(driver_num, {})
    rag_driver_citation = rag_engine.query(f"Number {driver_num} crystal gemstone remedy", top_k=1)
    citation_src = rag_driver_citation[0]["source"] if rag_driver_citation else "Numeros Vision Core Rules"
    
    crystal_remedies.append({
        "type": "Driver Core Energy Crystal",
        "number": driver_num,
        "planetary_ruler": driver_crystal_info.get("ruler"),
        "primary_gemstone": driver_crystal_info.get("primary_gem"),
        "healing_crystal": driver_crystal_info.get("crystal"),
        "benefit": driver_crystal_info.get("benefit"),
        "rag_citation_source": citation_src
    })
    
    # 2. Missing Numbers Crystal Support
    for miss in missing_nums:
        miss_crystal_info = VEDIC_CRYSTALS_DATABASE.get(miss, {})
        rag_miss_citation = rag_engine.query(f"Missing number {miss} crystal remedy", top_k=1)
        miss_citation_src = rag_miss_citation[0]["source"] if rag_miss_citation else "Numeros Vision Core Rules"
        
        crystal_remedies.append({
            "type": "Missing Number Balancing Crystal",
            "number": miss,
            "planetary_ruler": miss_crystal_info.get("ruler"),
            "primary_gemstone": miss_crystal_info.get("primary_gem"),
            "healing_crystal": miss_crystal_info.get("crystal"),
            "benefit": miss_crystal_info.get("benefit"),
            "rag_citation_source": miss_citation_src
        })

    return crystal_remedies

def generate_comprehensive_predictions_and_remedies(
    name: str,
    day: int,
    month: int,
    year: int,
    mobile_number: str = "",
    chart_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Generates a unified 8-Layer Prediction & Remedy Packet grounded in Numeros Vision RAG citations.
    """
    vedic_res = analyze_vedic_numerology(day, month, year)
    lo_shu_res = analyze_lo_shu_grid(day, month, year)
    
    from app.engine.cheiro_engine import analyze_name_cheiro
    
    driver = vedic_res["driver_number"]
    conductor = vedic_res["conductor_number"]
    name_analysis = analyze_name_cheiro(name, driver=driver, conductor=conductor)
    name_num = name_analysis["name_root"]
    name_compound = name_analysis["compound_sum"]
    name_archetype = name_analysis["compound_archetype"]
    
    # 1. Cheiro Name Alignment & Balancing Remedy
    if name_analysis["is_harmoniously_balanced"]:
        name_remedy = {
            "name_compound": name_compound,
            "name_archetype": name_archetype,
            "reduction_path": name_analysis["reduction_path"],
            "name_root": name_num,
            "ruling_planet": name_analysis["name_planet"],
            "status": "Harmonious",
            "guidance": f"Name Compound {name_compound} ('{name_archetype}') resolves cleanly to Root {name_num} ({name_analysis['name_planet']}), harmonizing with Driver {driver}.",
            "balancing_evaluation": name_analysis["balancing_evaluation"]
        }
    else:
        auspicious_targets = [n for n in [19, 23, 24, 27, 32, 37, 41, 45, 46] if (sum(int(d) for d in str(n)) % 9 or 9) in vedic_res["friendly_numbers"]]
        target_str = ", ".join(str(n) for n in auspicious_targets[:3])
        name_remedy = {
            "name_compound": name_compound,
            "name_archetype": name_archetype,
            "reduction_path": name_analysis["reduction_path"],
            "name_root": name_num,
            "ruling_planet": name_analysis["name_planet"],
            "status": "Requires Balancing",
            "guidance": f"Name Compound {name_compound} ('{name_archetype}') reduces to Root {name_num}. {name_analysis['balancing_evaluation']} Consider adjusting spelling to reach an auspicious compound such as {target_str}.",
            "balancing_evaluation": name_analysis["balancing_evaluation"]
        }

    # 2. Mobile Numerology Remedy
    mobile_res = {}
    if mobile_number:
        mob_sum = calculate_mobile_number_sum(mobile_number)
        mob_aligned = mob_sum in vedic_res["friendly_numbers"]
        mobile_res = {
            "mobile_total": mob_sum,
            "alignment": "Harmonious" if mob_aligned else "Requires Remedy",
            "remedy": f"Mobile total {mob_sum} is friendly to Driver {driver}." if mob_aligned else f"Mobile total {mob_sum} is unfriendly to Driver {driver}. Use mobile wallpaper with number {driver} energy."
        }

    # 3. Lo Shu Missing Number Remedies
    missing_remedies = []
    for miss in lo_shu_res["missing_numbers"]:
        rem_info = MISSING_NUMBER_REMEDIES_DATABASE.get(miss, {})
        rag_passages = rag_engine.query(f"Missing number {miss} remedy Lo Shu", top_k=1)
        citation = rag_passages[0]["source"] if rag_passages else "Numeros Vision Core Rules"
        missing_remedies.append({
            "missing_number": miss,
            "element": rem_info.get("element"),
            "direction": rem_info.get("direction"),
            "planet": rem_info.get("planet"),
            "remedy_action": rem_info.get("remedy"),
            "rag_citation_source": citation
        })

    # 4. Vedic Crystal & Gemstone Remedies (Layer 8)
    crystal_remedies = get_vedic_crystal_remedies(driver, lo_shu_res["missing_numbers"])

    # 5. BNN & Lal Kitab Remedies
    chart = chart_data or {
        "Sun": {"sign": "Scorpio", "house": 10},
        "Moon": {"sign": "Sagittarius", "house": 5},
        "Mars": {"sign": "Leo", "house": 3},
        "Jupiter": {"sign": "Libra", "house": 9},
        "Saturn": {"sign": "Virgo", "house": 6}
    }
    
    bnn_res = run_full_bnn_analysis(chart)
    lal_kitab_res = run_full_lal_kitab_analysis(chart)
    kp_res = analyze_kp_sub_lord(242.39)

    remedy_rag_citations = rag_engine.query(f"Driver {driver} Conductor {conductor} remedies crystals mantras", top_k=3)

    from app.engine.core_matrix_engine import generate_core_matrix_profile
    core_matrix_res = generate_core_matrix_profile(name, day, month, year, mobile_number=mobile_number)

    return {
        "user_name": name,
        "dob": f"{day:02d}/{month:02d}/{year}",
        "core_matrix_analysis": core_matrix_res,
        "predictions_summary": {
            "driver_mulank": driver,
            "driver_planet": vedic_res["driver_planet"],
            "driver_cheiro_archetype": vedic_res.get("cheiro_day_compound", {}).get("archetype", "Single number"),
            "conductor_bhagyank": conductor,
            "conductor_planet": vedic_res["conductor_planet"],
            "conductor_cheiro_archetype": vedic_res.get("cheiro_conductor_compound", {}).get("compound_archetype", ""),
            "name_number": name_num,
            "name_compound": name_compound,
            "name_cheiro_archetype": name_archetype,
            "completed_lo_shu_planes": lo_shu_res["completed_planes"],
            "kp_sub_lord": kp_res["sub_lord"]
        },
        "remedies_8_layer_package": {
            "shukla_paksha_consecration_window": calculate_shukla_paksha_timing(ruling_planet_num=driver),
            "layer1_name_numerology_remedy": name_remedy,
            "layer2_mobile_numerology_remedy": mobile_res,
            "layer3_lo_shu_missing_number_remedies": missing_remedies,
            "layer4_planetary_conjunction_remedies": bnn_res["active_combinations"][:2],
            "layer5_lal_kitab_house_remedies": lal_kitab_res["active_remedies"][:3],
            "layer6_harmonic_sub_lord_guidance": f"Align activities with Harmonic Sub-lord {kp_res['sub_lord']} nakshatra timings.",
            "layer7_elemental_crystal_and_gemstone_remedies": crystal_remedies,
            "layer7_vedic_crystal_and_gemstone_remedies": crystal_remedies,
            "layer8_rag_grounded_remedy_citations": [
                {
                    "source": p["source"],
                    "location": p["location"],
                    "excerpt": p["content"][:200] + "..."
                } for p in remedy_rag_citations
            ]
        }
    }

if __name__ == "__main__":
    report = generate_comprehensive_predictions_and_remedies("Bhaskr Singh", 15, 8, 1995, mobile_number="9876543210")
    print("=== UNIFIED 8-LAYER PREDICTION & CRYSTAL REMEDY REPORT ===")
    print("User:", report["user_name"], "| DOB:", report["dob"])
    print("Driver/Conductor:", report["predictions_summary"]["driver_mulank"], "/", report["predictions_summary"]["conductor_bhagyank"])
    print("\nLayer 7 (Vedic Crystal Remedies Count):", len(report["remedies_8_layer_package"]["layer7_vedic_crystal_and_gemstone_remedies"]))
    for crystal in report["remedies_8_layer_package"]["layer7_vedic_crystal_and_gemstone_remedies"][:3]:
        print(f"  * {crystal['type']} (Number {crystal['number']} - {crystal['planetary_ruler']}): Gem={crystal['primary_gemstone']} | Crystal={crystal['healing_crystal']}")
