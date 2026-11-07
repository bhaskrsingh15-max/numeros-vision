"""
NV-014 & NV-015: BUSINESS & BABY NAMING ENGINE
Grounding: Chaldean Name Numerology, Industry Sector Vibrations, Lo Shu Elemental Balance.

Deterministic capabilities:
1. NV-014 Business Name Analysis:
   - Full Chaldean brand name analysis (compound & root)
   - Owner Driver & Conductor compatibility
   - Industry sector vibration matching (Tech, Finance, Luxury, Health, Trade)
   - Multi-partner alignment matrix
   - Brand spelling candidate comparison & launch day timing.
2. NV-015 Baby Naming Workflow:
   - Curated classical and contemporary baby name repository
   - Filtering by gender, starting letter, root vibration, and compound auspiciousness
   - Automatic alignment with baby's Driver/Conductor and Lo Shu missing digits
   - Detailed phonetic and energetic impact profiles.
"""

from typing import Dict, Any, List, Optional, Set
import sys
import os

workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from app.engine.cheiro_engine import (
    CHALDEAN_LETTER_VALUES,
    analyze_number,
    compute_reduction_path
)
from app.engine.number_characteristics_registry import (
    get_number_profile,
    get_relationship,
    PLANETARY_RULERS
)
from app.engine.name_balancing_engine import (
    calculate_segment_values,
    AUSPICIOUS_COMPOUNDS,
    CHALLENGING_COMPOUNDS
)

# ── Industry Sector Ideal Number Profiles ─────────────────────────────────────
INDUSTRY_SECTOR_PROFILES: Dict[str, Dict[str, Any]] = {
    "technology": {
        "sector_name": "Technology, Software & AI",
        "favorable_roots": [1, 4, 5],
        "favorable_compounds": [19, 23, 32, 37, 41, 46],
        "rationale": "Requires Rahu innovation (4), Sun leadership (1), and Mercury agility (5)."
    },
    "finance": {
        "sector_name": "Banking, FinTech & Wealth Management",
        "favorable_roots": [3, 5, 8],
        "favorable_compounds": [15, 24, 32, 42, 50],
        "rationale": "Requires Jupiter trust (3), Mercury liquidity (5), and Saturnian institutional asset stability (8)."
    },
    "luxury": {
        "sector_name": "Fashion, Hospitality, Cosmetics & Luxury",
        "favorable_roots": [6, 5],
        "favorable_compounds": [15, 24, 33, 42, 51],
        "rationale": "Requires Venusian glamour and comfort (6) and Mercury commercial appeal (5)."
    },
    "healthcare": {
        "sector_name": "Healthcare, Pharmaceuticals & Wellness",
        "favorable_roots": [1, 2, 7, 9],
        "favorable_compounds": [19, 20, 25, 27, 34, 45],
        "rationale": "Requires Sun vitality (1), Moon care (2), Ketu research (7), and Mars surgical strength (9)."
    },
    "media": {
        "sector_name": "Media, Entertainment, PR & Marketing",
        "favorable_roots": [3, 5, 6],
        "favorable_compounds": [21, 23, 30, 32, 42],
        "rationale": "Requires Jupiter expression (3), Mercury communication (5), and Venus aesthetic charisma (6)."
    },
    "real_estate": {
        "sector_name": "Real Estate, Construction & Heavy Infrastructure",
        "favorable_roots": [8, 4, 2],
        "favorable_compounds": [20, 26, 31, 35, 44], # Note: 26/44 are traditional compounds; 35/44 must be carefully paired
        "favorable_compounds_safe": [24, 33, 42, 51],
        "rationale": "Demands Saturnian land endurance (8) and solid foundation building (4)."
    },
    "general_trade": {
        "sector_name": "E-Commerce, Logistics & General Trading",
        "favorable_roots": [5, 1],
        "favorable_compounds": [14, 23, 32, 41, 50],
        "rationale": "Demands Mercury's fast speed, distribution agility, and rapid cash circulation."
    }
}


# ── NV-014 Business Name Analysis ─────────────────────────────────────────────
def analyze_business_name(
    brand_name: str,
    owner_driver: int,
    owner_conductor: int,
    industry_category: str = "general_trade",
    partner_drivers: Optional[List[int]] = None
) -> Dict[str, Any]:
    """
    NV-014 Requirement: Business Name Analysis.
    Evaluates brand name against owner, partners, and industry classification.
    """
    clean_brand = "".join(c.upper() for c in brand_name if c.isalpha())
    letter_breakdown = [{c: CHALDEAN_LETTER_VALUES.get(c, 0)} for c in clean_brand]
    raw_compound = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean_brand)
    path, brand_root = compute_reduction_path(raw_compound)

    cheiro_info = analyze_number(raw_compound)
    archetype = cheiro_info.get("input_compound_archetype", "Commercial Matrix")

    # Industry evaluation
    ind_key = industry_category.lower().replace(" ", "_")
    ind_prof = INDUSTRY_SECTOR_PROFILES.get(ind_key, INDUSTRY_SECTOR_PROFILES["general_trade"])
    is_industry_favorable = brand_root in ind_prof["favorable_roots"]

    # Owner compatibility
    rel_d = get_relationship(brand_root, owner_driver)
    rel_c = get_relationship(brand_root, owner_conductor)

    owner_compat_score = 30 if rel_d["is_friendly"] else (20 if rel_d["is_neutral"] else 5)
    owner_compat_score += 30 if rel_c["is_friendly"] else (20 if rel_c["is_neutral"] else 5)

    # Compound score
    is_auspicious = raw_compound in AUSPICIOUS_COMPOUNDS
    is_challenging = raw_compound in CHALLENGING_COMPOUNDS
    compound_score = 30 if is_auspicious else (15 if not is_challenging else 0)

    industry_score = 10 if is_industry_favorable else 5

    total_score = min(owner_compat_score + compound_score + industry_score, 100)

    # Partner check
    partner_notes = []
    if partner_drivers:
        for p_idx, p_d in enumerate(partner_drivers, 1):
            p_rel = get_relationship(brand_root, p_d)
            partner_notes.append({
                "partner_number": p_idx,
                "partner_driver": p_d,
                "harmony_with_brand": p_rel["relationship"],
                "status": "Harmonious" if p_rel["is_friendly"] or p_rel["is_neutral"] else "Friction Warning"
            })

    if total_score >= 80:
        verdict = "Supreme Commercial Harmony"
        recommendation = "Brand name provides magnetic commercial momentum. Highly auspicious for launch."
    elif total_score >= 65:
        verdict = "Viable Commercial Vibration"
        recommendation = "Brand name is favorable; minor marketing tagline balancing can expand market reach."
    else:
        verdict = "Commercial Resistance / Name Tuning Advised"
        recommendation = "Brand compound or root creates energetic drag with owner or industry. Spelling adjustment advised."

    # Logo color and launch recommendations
    d_prof = get_number_profile(brand_root) or {}
    brand_planet = d_prof.get("planet", "Mercury")
    fav_days = d_prof.get("favourable_days", ["Wednesday", "Friday"])
    fav_colors = d_prof.get("favourable_colours", ["Green", "Gold", "White"])

    return {
        "brand_name": brand_name,
        "clean_name": clean_brand,
        "letter_breakdown": letter_breakdown,
        "brand_compound": raw_compound,
        "brand_root": brand_root,
        "reduction_path": path,
        "compound_archetype": archetype,
        "governing_planet": brand_planet,
        "industry_alignment": {
            "sector": ind_prof["sector_name"],
            "is_aligned": is_industry_favorable,
            "rationale": ind_prof["rationale"]
        },
        "owner_alignment": {
            "driver_harmony": rel_d["relationship"],
            "conductor_harmony": rel_c["relationship"]
        },
        "partner_alignments": partner_notes,
        "commercial_score": total_score,
        "verdict": verdict,
        "recommendation": recommendation,
        "branding_guidance": {
            "auspicious_logo_colors": fav_colors[:3],
            "favorable_launch_weekdays": fav_days,
            "marketing_tone": f"Reflects {brand_planet} traits: {d_prof.get('core_characteristics', 'Innovation and enterprise.')}"
        }
    }


# ── NV-015 Baby Naming Workflow ───────────────────────────────────────────────
# Curated approved baby name dataset
CURATED_BABY_NAMES = [
    # Boys
    {"name": "Aarav", "gender": "Boy", "origin": "Sanskrit", "meaning": "Peaceful wisdom, melodic sound"},
    {"name": "Advait", "gender": "Boy", "origin": "Sanskrit", "meaning": "Unique, non-dual, spiritual unity"},
    {"name": "Reyansh", "gender": "Boy", "origin": "Sanskrit", "meaning": "First ray of sunlight, divine essence"},
    {"name": "Vihaan", "gender": "Boy", "origin": "Sanskrit", "meaning": "Dawn of a new era, morning light"},
    {"name": "Dhruv", "gender": "Boy", "origin": "Sanskrit", "meaning": "Pole star, unshakeable and steadfast"},
    {"name": "Kabir", "gender": "Boy", "origin": "Indian/Arabic", "meaning": "Great leader, mystic poet"},
    {"name": "Ishaan", "gender": "Boy", "origin": "Sanskrit", "meaning": "Lord Shiva, northeast celestial guardian"},
    {"name": "Dev", "gender": "Boy", "origin": "Sanskrit", "meaning": "Divine, radiant spirit"},
    {"name": "Neil", "gender": "Boy", "origin": "Sanskrit/Gaelic", "meaning": "Sapphire blue, champion"},
    {"name": "Arjun", "gender": "Boy", "origin": "Sanskrit", "meaning": "Bright, white, heroic archer"},
    {"name": "Vivaan", "gender": "Boy", "origin": "Sanskrit", "meaning": "Full of life, ray of the rising sun"},
    {"name": "Rudra", "gender": "Boy", "origin": "Sanskrit", "meaning": "Mighty healer, Lord Shiva"},
    
    # Girls
    {"name": "Ananya", "gender": "Girl", "origin": "Sanskrit", "meaning": "Matchless, goddess Parvati"},
    {"name": "Aadhya", "gender": "Girl", "origin": "Sanskrit", "meaning": "First power, Adi Shakti"},
    {"name": "Diya", "gender": "Girl", "origin": "Sanskrit", "meaning": "Radiant lamp, bright illumination"},
    {"name": "Ira", "gender": "Girl", "origin": "Sanskrit", "meaning": "Wisdom, Saraswati, the nurturing Earth"},
    {"name": "Mira", "gender": "Girl", "origin": "Sanskrit", "meaning": "Devoted soul, ocean of grace"},
    {"name": "Navya", "gender": "Girl", "origin": "Sanskrit", "meaning": "Fresh, novel, worthy of praise"},
    {"name": "Tara", "gender": "Girl", "origin": "Sanskrit", "meaning": "Luminous star, savior"},
    {"name": "Saanvi", "gender": "Girl", "origin": "Sanskrit", "meaning": "Goddess Lakshmi, followed by prosperity"},
    {"name": "Kavya", "gender": "Girl", "origin": "Sanskrit", "meaning": "Poetic grace, literature in motion"},
    {"name": "Riya", "gender": "Girl", "origin": "Sanskrit", "meaning": "Graceful singer, graceful dancer"},
    {"name": "Zoya", "gender": "Girl", "origin": "Persian/Slavic", "meaning": "Alive, loving, light-hearted"},
    {"name": "Avani", "gender": "Girl", "origin": "Sanskrit", "meaning": "The gentle, fertile earth"},

    # Unisex
    {"name": "Arya", "gender": "Unisex", "origin": "Sanskrit", "meaning": "Noble, honorable, sage-like"},
    {"name": "Milan", "gender": "Unisex", "origin": "Sanskrit/Slavic", "meaning": "Graceful union, kind"},
    {"name": "Amrit", "gender": "Unisex", "origin": "Sanskrit", "meaning": "Immortal nectar, pure grace"}
]


def recommend_baby_names(
    baby_driver: int,
    baby_conductor: int,
    gender: Optional[str] = None,
    starting_letter: Optional[str] = None,
    missing_numbers_in_chart: Optional[List[int]] = None,
    max_results: int = 8
) -> List[Dict[str, Any]]:
    """
    NV-015 Requirement: Baby Naming Workflow.
    Evaluates curated names, calculating Chaldean values and selecting names that:
    1. Harmonize with baby's Driver & Conductor
    2. Possess auspicious Cheiro compound numbers
    3. Fill missing numbers in the baby's Lo Shu chart
    """
    gen_filter = gender.strip().lower() if gender else None
    start_filter = starting_letter.strip().upper() if starting_letter else None
    missing = set(missing_numbers_in_chart or [])

    d_prof = get_number_profile(baby_driver) or {}
    friendly_nums = set(d_prof.get("friendly_numbers", [1, 5, 6]))
    friendly_nums.add(baby_driver)
    friendly_nums.add(baby_conductor)

    scored_names = []

    for entry in CURATED_BABY_NAMES:
        name = entry["name"]
        entry_gen = entry["gender"].lower()

        # Filter gender
        if gen_filter and gen_filter != "all":
            if entry_gen != gen_filter and entry_gen != "unisex":
                continue

        # Filter starting letter
        if start_filter:
            if not name.upper().startswith(start_filter):
                continue

        clean = "".join(c.upper() for c in name if c.isalpha())
        compound = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean)
        path, root = compute_reduction_path(compound)

        is_auspicious = compound in AUSPICIOUS_COMPOUNDS
        is_challenging = compound in CHALLENGING_COMPOUNDS

        rel_d = get_relationship(root, baby_driver)
        rel_c = get_relationship(root, baby_conductor)

        score = 0
        if is_auspicious: score += 35
        elif not is_challenging: score += 20

        if rel_d["is_friendly"]: score += 25
        elif rel_d["is_neutral"]: score += 15

        if rel_c["is_friendly"]: score += 25
        elif rel_c["is_neutral"]: score += 15

        # Check Lo Shu missing number fill
        name_digits = set(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean)
        name_digits.add(root)
        gaps_filled = sorted(list(missing.intersection(name_digits)))

        if gaps_filled:
            score += min(len(gaps_filled) * 5, 15)

        cheiro_p = analyze_number(compound)

        scored_names.append({
            "name": name,
            "gender": entry["gender"],
            "origin": entry["origin"],
            "meaning": entry["meaning"],
            "compound_sum": compound,
            "compound_archetype": cheiro_p.get("input_compound_archetype", ""),
            "single_root": root,
            "root_planet": PLANETARY_RULERS.get(root, {}).get("planet", "Unknown"),
            "reduction_path": path,
            "driver_harmony": rel_d["relationship"],
            "conductor_harmony": rel_c["relationship"],
            "missing_chart_gaps_filled": gaps_filled,
            "suitability_score": score,
            "verdict": "Highly Recommended" if score >= 80 else ("Favorable" if score >= 60 else "Moderate")
        })

    # Sort descending by score
    scored_names.sort(key=lambda x: x["suitability_score"], reverse=True)
    return scored_names[:max_results]
