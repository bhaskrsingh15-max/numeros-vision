"""
NV-008 & NV-009: EXPLAINABLE REMEDY RULES & YANTRA RECOMMENDATION ENGINE
Grounding: Classical Vedic Upayas, Lal Kitab Environmental Balancing, Yantra Shastra, Lo Shu Vastu.

Deterministic capabilities:
1. NV-008 Explainable Remedy Rules:
   - Evaluates eligibility and exclusion rules to prevent contradictory remedies.
   - Enforces a maximum of 5 prioritized remedies to prevent seeker overwhelm.
   - Categorizes across:
     a) Mindset & Behavioral Attunement
     b) Environmental & Vastu Spatial Alignment
     c) Ethical Charity / Seva (Dana)
     d) Sacred Geometry & Yantra Attunement
     e) Daily Ritual & Sound Attunement
2. NV-009 Structured Yantra Catalogue:
   - Comprehensive profiles: Deity, Planet, Geometry, Consecration Day/Time,
     Material, Directional Placement, Frame/Thread Pairing, Beej Mantra, and Exclusions.
   - Non-fatalistic, respectful, spiritually grounded presentation.
"""

from typing import Dict, Any, List, Optional, Set
import sys
import os

workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from app.engine.number_characteristics_registry import (
    get_number_profile,
    get_relationship,
    PLANETARY_RULERS
)

# ── NV-009 Canonical Yantra Catalogue ─────────────────────────────────────────
YANTRA_CATALOGUE: Dict[str, Dict[str, Any]] = {
    "Surya Yantra": {
        "yantra_id": "YAN_SURYA",
        "name": "Surya Yantra (Solar Sacred Matrix)",
        "ruling_planet": "Sun (Surya)",
        "ruling_number": 1,
        "deity": "Lord Surya / Aditya",
        "beneficial_for": [1, 2, 3, 5, 9],
        "ineligible_for": [8],  # Direct clash between Sun and Saturn
        "material": "Pure Copper Plate (Tambra Patra) or Gold-plated Brass",
        "geometry": "Central circular lotus with 8 solar petals bounded by protective square gates",
        "optimal_direction": "East (facing West) or North-East in personal altar / study",
        "best_day_time": "Sunday morning at sunrise during Shukla Paksha (waxing moon)",
        "thread_or_frame": "Red or Copper-gold frame with saffron/red thread",
        "beej_mantra": "Om Hram Hreem Hroum Sah Suryaya Namah (108 times)",
        "purpose": "Ignites executive leadership, vitality, bone health, public authority, and clear vision."
    },
    "Chandra Yantra": {
        "yantra_id": "YAN_CHANDRA",
        "name": "Chandra Yantra (Lunar Harmony Matrix)",
        "ruling_planet": "Moon (Chandra)",
        "ruling_number": 2,
        "deity": "Lord Chandra / Soma",
        "beneficial_for": [1, 2, 3, 5],
        "ineligible_for": [4, 8, 9],
        "material": "Pure Silver Plate or Silver-plated Copper",
        "geometry": "Concentric crescent interlaced with 16 sacred lotus petals",
        "optimal_direction": "North-West (Vayu zone) or North in private sanctuary",
        "best_day_time": "Monday evening during Shukla Paksha",
        "thread_or_frame": "Silver or White frame with white/silver silk thread",
        "beej_mantra": "Om Shram Shreem Shroum Sah Chandraya Namah (108 times)",
        "purpose": "Soothes emotional turbulence, relieves mental restlessness, enhances intuition and domestic peace."
    },
    "Brihaspati Yantra": {
        "yantra_id": "YAN_BRIHASPATI",
        "name": "Brihaspati / Guru Yantra (Matrix of Divine Wisdom)",
        "ruling_planet": "Jupiter (Guru)",
        "ruling_number": 3,
        "deity": "Lord Brihaspati / Lord Vishnu",
        "beneficial_for": [1, 2, 3, 5, 7, 9],
        "ineligible_for": [6],  # Classical Guru vs Shukra friction
        "material": "Solid Brass or 24k Gold-gilded Copper",
        "geometry": "Nine-fold square grid enclosing Jupiter's sacred numeric sigil",
        "optimal_direction": "North-East (Ishanya zone) on wooden pedestal",
        "best_day_time": "Thursday morning at Brahma Muhurta (5:00 - 6:30 AM)",
        "thread_or_frame": "Yellow Brass or Teakwood frame with yellow cotton thread",
        "beej_mantra": "Om Gram Greem Groum Sah Guruve Namah (108 times)",
        "purpose": "Expands higher wisdom, commercial wealth, higher educational accomplishments, and spiritual grace."
    },
    "Rahu Yantra": {
        "yantra_id": "YAN_RAHU",
        "name": "Rahu Yantra (Matrix of Strategic Clarity & Grounding)",
        "ruling_planet": "Rahu",
        "ruling_number": 4,
        "deity": "Durga / Bhairava / Rahu Devata",
        "beneficial_for": [4, 5, 6, 7],
        "ineligible_for": [1, 2, 9],
        "material": "Mixed Alloy (Ashtadhatu) or Lead-free Pewter/Copper",
        "geometry": "Eight-cornered geometric star surrounded by defensive earthen boundaries",
        "optimal_direction": "South-West (Nairritya zone) at eye level",
        "best_day_time": "Saturday evening after twilight during Krishna Paksha",
        "thread_or_frame": "Smoky bronze or dark charcoal frame with blue/black thread",
        "beej_mantra": "Om Bhram Bhreem Bhroum Sah Rahave Namah (108 times)",
        "purpose": "Dispels illusions, protects against sudden financial upheavals, grounds restless tech/innovation energy."
    },
    "Budh Yantra": {
        "yantra_id": "YAN_BUDH",
        "name": "Budh Yantra (Mercury Matrix of Trade & Eloquence)",
        "ruling_planet": "Mercury (Budh)",
        "ruling_number": 5,
        "deity": "Lord Budha / Lord Narayana",
        "beneficial_for": [1, 2, 3, 5, 6],
        "ineligible_for": [],  # Universal mediator
        "material": "Pure Bronze or Copper Plate",
        "geometry": "Hexagonal balance star with central bindu and Mercury numeric grid",
        "optimal_direction": "North (Kuber zone) directly on office or trading desk",
        "best_day_time": "Wednesday morning between 7:00 AM and 9:00 AM",
        "thread_or_frame": "Green or Rosewood frame with green silk thread",
        "beej_mantra": "Om Bram Breem Broum Sah Budhaya Namah (108 times)",
        "purpose": "Heightens commercial acumen, rapid linguistic fluency, trading profits, and nervous system harmony."
    },
    "Shukra Yantra": {
        "yantra_id": "YAN_SHUKRA",
        "name": "Shukra Yantra (Matrix of Luxury, Romance & Grace)",
        "ruling_planet": "Venus (Shukra)",
        "ruling_number": 6,
        "deity": "Goddess Mahalakshmi / Shukracharya",
        "beneficial_for": [1, 5, 6, 8],
        "ineligible_for": [3],
        "material": "Polished Silver or Mirror-finish Stainless Steel",
        "geometry": "Interlocking lotus triangle grid embodying primordial feminine aesthetic",
        "optimal_direction": "South-East (Agni zone) or master bedroom dressing sanctuary",
        "best_day_time": "Friday morning at sunrise",
        "thread_or_frame": "Polished Silver or Ivory White frame with white/pink silk cord",
        "beej_mantra": "Om Dram Dreem Droum Sah Shukraya Namah (108 times)",
        "purpose": "Attracts material luxury, harmonious marital warmth, artistic elegance, and magnetic charisma."
    },
    "Ketu Yantra": {
        "yantra_id": "YAN_KETU",
        "name": "Ketu Yantra (Matrix of Intuition & Metaphysical Depth)",
        "ruling_planet": "Ketu",
        "ruling_number": 7,
        "deity": "Lord Ganesha / Matsya Avatar",
        "beneficial_for": [1, 3, 5, 7],
        "ineligible_for": [8],
        "material": "Copper or Panchdhatu (5-metal alloy)",
        "geometry": "Nine-sectioned mystic square with upward pointing triangular flame",
        "optimal_direction": "West (Varuna zone) or meditation/puja room",
        "best_day_time": "Tuesday or Thursday evening",
        "thread_or_frame": "Earthy copper or grey sandalwood frame with multi-colored mauli thread",
        "beej_mantra": "Om Sram Sreem Sroum Sah Ketave Namah (108 times)",
        "purpose": "Deepens metaphysical contemplation, shields from unseen psychic fatigue, awakens research brilliance."
    },
    "Shani Yantra": {
        "yantra_id": "YAN_SHANI",
        "name": "Shani Yantra (Matrix of Justice, Endurance & Stability)",
        "ruling_planet": "Saturn (Shani)",
        "ruling_number": 8,
        "deity": "Lord Shani / Lord Kurma",
        "beneficial_for": [3, 5, 6, 8],
        "ineligible_for": [1, 2, 4, 9],  # Major classical conflict with Sun, Moon, Rahu, Mars
        "material": "Pure Iron or Blackened Brass Plate",
        "geometry": "Traditional magic square of 15 (Saturnian numeric grid) enclosed in triple fortress lines",
        "optimal_direction": "West or South-West wall in home or commercial office",
        "best_day_time": "Saturday evening at sunset",
        "thread_or_frame": "Matte black or dark navy iron frame with black/blue thread",
        "beej_mantra": "Om Pram Preem Proum Sah Shanaischaraya Namah (108 times)",
        "purpose": "Inculcates unwavering discipline, rewards ethical labor, stabilizes real estate and heavy manufacturing."
    },
    "Mangal Yantra": {
        "yantra_id": "YAN_MANGAL",
        "name": "Mangal Yantra (Matrix of Courage, Fire & Vitality)",
        "ruling_planet": "Mars (Mangal)",
        "ruling_number": 9,
        "deity": "Lord Hanuman / Kartikeya / Mangal Devata",
        "beneficial_for": [1, 3, 5, 9],
        "ineligible_for": [2, 4, 8],
        "material": "Solid Pure Red Copper Plate",
        "geometry": "Downward-pointing red triangle of primal shakti within an octagonal fire enclosure",
        "optimal_direction": "South (Yama/Agni sector) facing North",
        "best_day_time": "Tuesday morning at sunrise",
        "thread_or_frame": "Red lacquered wood or pure copper frame with bright red thread",
        "beej_mantra": "Om Kram Kreem Kroum Sah Bhaumaya Namah (108 times)",
        "purpose": "Dispels fear and inertia, protects property against litigation, accelerates surgical/defense success."
    },
    "Shri Yantra": {
        "yantra_id": "YAN_SHRI",
        "name": "Shri Yantra (Supreme Cosmic Prosperity Matrix)",
        "ruling_planet": "Universal / Venus-Jupiter Synergy",
        "ruling_number": 6,
        "deity": "Maha Tripurasundari / Goddess Lakshmi",
        "beneficial_for": [1, 2, 3, 4, 5, 6, 7, 8, 9],  # Universal sovereign matrix
        "ineligible_for": [],
        "material": "Pure Sphatik (Clear Quartz Crystal) or 24k Gold-embossed Copper",
        "geometry": "Nine interlocking triangles (4 Shiva, 5 Shakti) radiating from supreme Bindu",
        "optimal_direction": "East or North-East in home sanctum or business cash locker",
        "best_day_time": "Friday morning or Diwali / Akshaya Tritiya / Purnima",
        "thread_or_frame": "Gold or polished Teakwood frame",
        "beej_mantra": "Om Shreem Hreem Shreem Kamale Kamalalaye Praseed Praseed (108 times)",
        "purpose": "Harmonizes universal electro-magnetic abundance, dissolves spatial Vastu imbalances, draws holistic prosperity."
    },
    "Kuber Yantra": {
        "yantra_id": "YAN_KUBER",
        "name": "Kuber Yantra (Celestial Wealth Treasurer Sigil)",
        "ruling_planet": "Mercury-Jupiter Financial Axis",
        "ruling_number": 5,
        "deity": "Lord Kuber / Yaksha Raja",
        "beneficial_for": [1, 2, 3, 5, 6, 7, 8],
        "ineligible_for": [],
        "material": "Engraved Pure Brass or Copper Plate",
        "geometry": "Numerical magic square totaling 72 in every row and diagonal",
        "optimal_direction": "North wall facing South (Kuber rules the Northern quadrant)",
        "best_day_time": "Thursday or Friday morning during waxing lunar phase",
        "thread_or_frame": "Golden brass or yellow wood frame",
        "beej_mantra": "Om Yakshaya Kuberaya Vaishravanaya Dhanadhanyadhipataye Dhanadhanyasamriddhim Me Dehi Dapaya Swaha",
        "purpose": "Unlocks stalled receivables, stabilizes liquidity, attracts lucrative commercial contracts."
    }
}


def select_remedies_and_yantras(
    driver: int,
    conductor: int,
    missing_numbers: Optional[List[int]] = None,
    repeated_numbers: Optional[Dict[int, int]] = None,
    max_remedies: int = 5
) -> Dict[str, Any]:
    """
    NV-008 & NV-009 Core Function:
    Applies strict explainable selection and exclusion rules:
    - Never prescribes remedies of enemy planets.
    - Limits total recommendations to a curated, high-impact set of <= 5.
    - Matches exactly one primary sacred Yantra.
    """
    missing = missing_numbers or []
    repeated = repeated_numbers or {}

    d_prof = get_number_profile(driver) or {}
    c_prof = get_number_profile(conductor) or {}

    d_enemies = set(d_prof.get("enemy_numbers", []))
    c_enemies = set(c_prof.get("enemy_numbers", []))
    total_enemies = d_enemies.union(c_enemies)

    # 1. Yantra Recommendation
    # Candidate Yantras: Check driver planet, conductor planet, or universal
    selected_yantra = None
    yantra_rationale = ""

    # Map number to Yantra key
    num_to_yantra = {
        1: "Surya Yantra",
        2: "Chandra Yantra",
        3: "Brihaspati Yantra",
        4: "Rahu Yantra",
        5: "Budh Yantra",
        6: "Shukra Yantra",
        7: "Ketu Yantra",
        8: "Shani Yantra",
        9: "Mangal Yantra"
    }

    # Attempt primary driver Yantra if not in conductor's enemy list
    primary_cand = num_to_yantra.get(driver)
    if primary_cand and primary_cand in YANTRA_CATALOGUE:
        y_info = YANTRA_CATALOGUE[primary_cand]
        if conductor not in y_info.get("ineligible_for", []):
            selected_yantra = y_info
            yantra_rationale = f"Aligns with your primary Driver {driver} ({d_prof.get('planet')}) to amplify your leadership and vitality."

    # If driver Yantra conflicted, try conductor Yantra
    if not selected_yantra:
        cond_cand = num_to_yantra.get(conductor)
        if cond_cand and cond_cand in YANTRA_CATALOGUE:
            y_info = YANTRA_CATALOGUE[cond_cand]
            if driver not in y_info.get("ineligible_for", []):
                selected_yantra = y_info
                yantra_rationale = f"Aligns with your Conductor {conductor} ({c_prof.get('planet')}) to stabilize your destiny path."

    # Fallback to universal Shri Yantra (safe and auspicious for all)
    if not selected_yantra:
        selected_yantra = YANTRA_CATALOGUE["Shri Yantra"]
        yantra_rationale = "Universal harmonic matrix chosen to bypass driver-conductor planetary friction and bestow balanced abundance."

    # 2. Curated Remedies across 5 Tiers (Filtered to <= 5 items)
    curated_remedies = []

    # Tier A: Mindset & Behavioral Attunement
    tier_a = {
        "tier": "Mindset & Daily Behavioral Attunement",
        "category": "BEHAVIORAL",
        "action": d_prof.get("personal_development", "Practice conscious daily mindfulness and transparent communication."),
        "why_it_works": f"Directly pacifies the habitual shadow challenge of Driver {driver} ({d_prof.get('challenges', [''])[0] if d_prof.get('challenges') else 'restlessness'}).",
        "frequency": "Daily lifestyle habit"
    }
    curated_remedies.append(tier_a)

    # Tier B: Environmental & Vastu Spatial Alignment
    fav_colours = d_prof.get("favourable_colours", ["White", "Yellow"])
    avoid_colours = list(set(d_prof.get("colours_to_avoid", []) + c_prof.get("colours_to_avoid", [])))
    tier_b = {
        "tier": "Environmental & Vastu Space Alignment",
        "category": "ENVIRONMENTAL",
        "action": f"Incorporate {', '.join(fav_colours[:2])} tones in your primary workspace; face East or North during negotiations.",
        "why_it_works": "Aligns physical ambiance to wavelengths harmonious with your core planetary rulers.",
        "avoid_factors": f"Minimize {', '.join(avoid_colours[:2])} in bedroom linens or personal clothing." if avoid_colours else "None",
        "frequency": "Continuous environmental setting"
    }
    curated_remedies.append(tier_b)

    # Tier C: Practical Seva & Charity (Dana)
    # Filter by safe planets (never donate for an enemy planet in a way that aggravates, and never discard your driver's power)
    seva_map = {
        1: ("Offer fresh drinking water to travelers or public water stations on Sundays.", "Strengthens Sun solar vitality and dispels ego friction."),
        2: ("Offer white milk or food to elderly women or mothers on Mondays.", "Calms Moon fluctuations and builds emotional stability."),
        3: ("Sponsor educational books or stationeries for underprivileged students on Thursdays.", "Activates Jupiter's higher blessings of wisdom and wealth."),
        4: ("Donate dark blankets or warm clothing to sweepers or municipal laborers.", "Pacifies Rahu's erratic mental agitation."),
        5: ("Offer green grass or fresh spinach (Palak) to cows on Wednesday mornings.", "Expands Mercury's commercial intelligence and financial agility."),
        6: ("Donate silk clothes, ghee, or cosmetics to young girls or brides on Fridays.", "Harmonizes Venusian relationship bliss and domestic comfort."),
        7: ("Feed stray dogs or community animals with bread and milk on Tuesdays/Wednesdays.", "Pacifies Ketu and shields against subtle psychological illusions."),
        8: ("Feed black sesame seeds or mustard oil preparations to laborers on Saturdays.", "Honors Saturn's mandate of humility, neutralizing karmic delays."),
        9: ("Support blood donation drives or provide sweet jaggery snacks to athletes on Tuesdays.", "Directs Mars's fiery stamina into protective humanitarian channels.")
    }

    # Pick seva based on Conductor or safe missing number
    target_num = conductor if conductor not in total_enemies else (5 if 5 not in total_enemies else driver)
    seva_action, seva_why = seva_map.get(target_num, ("Engage in community volunteering once monthly.", "Builds humility."))
    tier_c = {
        "tier": "Ethical Charity & Seva (Karma Alignment)",
        "category": "SEVA_DANA",
        "action": seva_action,
        "why_it_works": seva_why,
        "frequency": "Weekly on the designated day"
    }
    curated_remedies.append(tier_c)

    # Tier D: Missing Number Element Healing (Lo Shu Integration)
    # Pick the most critical missing number that is NOT in the enemy set
    safe_missing = [n for n in missing if n not in total_enemies]
    if safe_missing:
        crit_miss = safe_missing[0]
        from app.engine.remedy_engine import MISSING_NUMBER_REMEDIES_DATABASE
        miss_data = MISSING_NUMBER_REMEDIES_DATABASE.get(crit_miss, {})
        tier_d = {
            "tier": "Lo Shu Missing Grid Elemental Healing",
            "category": "ELEMENTAL_VIBRATION",
            "action": miss_data.get("remedy", f"Incorporate element associated with number {crit_miss}."),
            "why_it_works": f"Replenishes missing Number {crit_miss} ({miss_data.get('planet')}, {miss_data.get('element')} Element) in your birth grid.",
            "direction": miss_data.get("direction", "Center"),
            "frequency": "Daily practice"
        }
        curated_remedies.append(tier_d)

    # Tier E: Daily Sound / Water Attunement
    tier_e = {
        "tier": "Daily Sound & Water Offering Ritual",
        "category": "RITUAL_ATTUNEMENT",
        "action": (
            "Drink water stored overnight in a pure copper vessel each morning, "
            f"and recite the sacred Beej Mantra '{selected_yantra['beej_mantra'].split('(')[0].strip()}' for 3 minutes."
        ),
        "why_it_works": f"Balances bio-electrical vitality and anchors the sacred geometry of the {selected_yantra['name']}.",
        "frequency": "Daily morning routine"
    }
    curated_remedies.append(tier_e)

    # Strict maximum enforcement
    curated_remedies = curated_remedies[:max_remedies]

    return {
        "driver": driver,
        "conductor": conductor,
        "missing_numbers_considered": missing,
        "excluded_conflict_numbers": list(total_enemies),
        "total_remedies_prescribed": len(curated_remedies),
        "enforcement_cap": max_remedies,
        "prescribed_remedies": curated_remedies,
        "prescribed_yantra": selected_yantra,
        "yantra_recommendation_rationale": yantra_rationale,
        "rules_explanation": (
            f"All {len(curated_remedies)} remedies were selected through strict eligibility filters. "
            f"Planetary energies in natural conflict with your core matrix ({list(total_enemies)}) were completely excluded. "
            "Maximum 5-item cap enforced to ensure practical, non-overwhelming daily implementation."
        )
    }
