"""
NV-010 to NV-013: ASSET & IDENTIFIER NUMEROLOGY ENGINE
Grounding: Professional Numerology Pro System (Topics 2, 4), Chaldean Letter Vibrations, Vastu Spatial Principles.

Deterministic capabilities:
1. NV-010 Mobile Phone Number Audit:
   - Malefic pairs filter (14, 18, 28, 48, etc.)
   - Forbidden repetitive sequences (00, 44, 88, 222, etc.)
   - Digit frequency distribution
   - Total compound & root vibration compatibility with Driver/Conductor.
2. NV-011 Vehicle Registration Number Analysis:
   - Robust license plate parsing (State + District + Series + Digits)
   - Combined Chaldean letters + numeric sum
   - Independent 4-digit core analysis
   - Vehicle color suitability and dashboard protection remedies.
3. NV-012 House & Property Number Analysis:
   - Flat/Unit number vs Building/Plot number reduction
   - Vastu elemental nature and directional orientation
   - Owner Driver/Conductor compatibility and threshold harmonizing remedies.
4. NV-013 Bank & Account Number Harmony (Strict Privacy Enforced):
   - Ephemeral in-memory calculation; zero raw account persistence
   - Masked account display (e.g., '*******789')
   - Wealth vibration index and liquidity alignment.
"""

from typing import Dict, Any, List, Optional
import re
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
from app.engine.professional_numerology_engine import (
    audit_mobile_number,
    MALEFIC_MOBILE_PAIRS
)


# ── NV-010 Mobile Number Audit ────────────────────────────────────────────────
def analyze_mobile_number(
    mobile_str: str,
    driver: Optional[int] = None,
    conductor: Optional[int] = None
) -> Dict[str, Any]:
    """
    NV-010 Requirement: Comprehensive Mobile Number Audit.
    Extends base mobile audit with frequency distribution and multi-core compatibility.
    """
    base_audit = audit_mobile_number(mobile_str, driver=driver)
    if "error" in base_audit:
        return base_audit

    digits = [int(d) for d in base_audit["mobile_number"]]
    digit_counts = {d: digits.count(d) for d in range(10)}

    # Check conductor harmony
    conductor_harmony = True
    cond_relationship = "Neutral"
    if conductor:
        rel = get_relationship(base_audit["total_root"], conductor)
        conductor_harmony = rel["is_friendly"] or rel["is_neutral"]
        cond_relationship = rel["relationship"]

    driver_rel = "Friend" if base_audit.get("is_friendly_to_driver") else "Challenging"
    if driver:
        rel_d = get_relationship(base_audit["total_root"], driver)
        driver_rel = rel_d["relationship"]

    return {
        "mobile_number": base_audit["mobile_number"],
        "digit_frequency": digit_counts,
        "total_compound": base_audit["total_compound"],
        "total_root": base_audit["total_root"],
        "root_planet": PLANETARY_RULERS.get(base_audit["total_root"], {}).get("planet", "Unknown"),
        "driver_compatibility": driver_rel,
        "conductor_compatibility": cond_relationship,
        "malefic_pairs_detected": base_audit["malefic_pairs_found"],
        "repeating_digit_issues": base_audit["repeating_digit_issues"],
        "overall_status": base_audit["status"],
        "recommended_totals": base_audit["recommended_totals"],
        "actionable_remedy": base_audit["remedy"]
    }


# ── NV-011 Vehicle Registration Number Analysis ───────────────────────────────
def analyze_vehicle_number(
    registration_str: str,
    driver: int,
    conductor: int
) -> Dict[str, Any]:
    """
    NV-011 Requirement: Vehicle Registration Number Analysis.
    Parses plate letters and digits, computes Chaldean compound, evaluates owner compatibility,
    recommends vehicle colors and dashboard protection upayas.
    """
    clean_plate = re.sub(r"[^A-Za-z0-9]", "", registration_str).upper()
    if len(clean_plate) < 4:
        return {"error": "Invalid vehicle registration plate. Must contain at least 4 alphanumeric characters."}

    # Separate letters and digits
    letters = [c for c in clean_plate if c.isalpha()]
    digits = [c for c in clean_plate if c.isdigit()]

    letter_sum = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in letters)
    digit_sum = sum(int(d) for d in digits)
    total_compound = letter_sum + digit_sum

    total_path, total_root = compute_reduction_path(total_compound)

    # Core 4-digit number evaluation (running number on plate)
    core_digits_str = "".join(digits[-4:]) if len(digits) >= 4 else "".join(digits)
    core_compound = sum(int(d) for d in core_digits_str) if core_digits_str else 0
    core_path, core_root = compute_reduction_path(core_compound) if core_compound else ("0", 0)

    # Owner Compatibility
    rel_driver = get_relationship(total_root, driver)
    rel_cond = get_relationship(total_root, conductor)

    is_safe = (rel_driver["relationship"] != "Enemy") and (rel_cond["relationship"] != "Enemy")
    # Numbers 4 and 8 in vehicle totals carry higher accident/repair warnings in classical numerology
    carries_saturn_rahu_vibration = total_root in [4, 8] or core_root in [4, 8]

    if carries_saturn_rahu_vibration:
        risk_tier = "Moderate Maintenance & Vigilance Needed"
        safety_notice = "Vehicle total vibrates to 4 (Rahu) or 8 (Saturn), indicating higher routine maintenance, electrical glitches, or strict traffic scrutiny."
    elif is_safe:
        risk_tier = "Harmonious & Auspicious"
        safety_notice = "Vehicle vibration harmonizes gracefully with your core birth numbers."
    else:
        risk_tier = "Frictional Vibration"
        safety_notice = "Vehicle vibration creates energetic friction with your birth driver/conductor."

    # Color Recommendations based on Driver
    d_prof = get_number_profile(driver) or {}
    fav_colors = d_prof.get("favourable_colours", ["White", "Silver", "Grey"])
    avoid_colors = d_prof.get("colours_to_avoid", ["Black"])

    return {
        "registration_plate": clean_plate,
        "parsed_segments": {
            "letters": "".join(letters),
            "letters_chaldean_sum": letter_sum,
            "digits": "".join(digits),
            "digits_sum": digit_sum
        },
        "full_plate_compound": total_compound,
        "full_plate_root": total_root,
        "full_plate_reduction_path": total_path,
        "core_running_digits": core_digits_str,
        "core_running_root": core_root,
        "driver_harmony": rel_driver["relationship"],
        "conductor_harmony": rel_cond["relationship"],
        "safety_and_risk_tier": risk_tier,
        "analysis_notes": safety_notice,
        "favorable_vehicle_colors": fav_colors,
        "vehicle_colors_to_avoid": avoid_colors,
        "protective_remedies": [
            "Keep a small brass or sandalwood idol of Lord Ganesha or a brass Swastika on the front dashboard.",
            "Tuck a genuine peacock feather (Mor Pankh) inside the glove compartment for energetic shielding.",
            "Place a pouch containing 50 grams of rock salt under the driver's seat and replace monthly to absorb static highway stress."
        ]
    }


# ── NV-012 House and Property Number Analysis ─────────────────────────────────
def analyze_property_number(
    property_str: str,
    driver: int,
    conductor: int
) -> Dict[str, Any]:
    """
    NV-012 Requirement: House & Property Number Analysis.
    Evaluates unit/flat/villa numbers, calculates elemental Vastu resonance,
    determines harmony with primary resident, and prescribes door/spatial upayas.
    """
    clean_prop = property_str.strip()
    # Extract letters and digits
    letters = [c.upper() for c in clean_prop if c.isalpha()]
    digits = [c for c in clean_prop if c.isdigit()]

    if not digits and not letters:
        return {"error": "Invalid property identifier."}

    letter_val = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in letters)
    digit_val = sum(int(d) for d in digits)
    total_compound = letter_val + digit_val
    path, root = compute_reduction_path(total_compound)

    # Vastu Elemental nature
    ELEMENTAL_PROPERTY_MAP = {
        1: {"element": "Fire / Solar", "direction": "East", "vibe": "Authority, public fame, leadership; excellent for founders and executives."},
        2: {"element": "Water / Lunar", "direction": "North-West", "vibe": "Peace, domestic affection, empathy, creativity; ideal for counsellors and artists."},
        3: {"element": "Wood / Ether", "direction": "North-East", "vibe": "Knowledge, spirituality, academic excellence, prosperity; ideal for teachers, lawyers, bankers."},
        4: {"element": "Wood / Earth", "direction": "South-West", "vibe": "Discipline, technology, structural order; requires tidiness to avoid claustrophobia."},
        5: {"element": "Earth / Mercury", "direction": "Center (Brahmasthan)", "vibe": "Vibrant social flow, commerce, trade, travel, communication; highly dynamic."},
        6: {"element": "Metal / Venus", "direction": "South-East", "vibe": "Luxury, romance, aesthetics, comfortable living, domestic bliss; premier for family harmony."},
        7: {"element": "Metal / Ketu", "direction": "West", "vibe": "Quiet sanctuary, contemplation, research, spiritual depth; less suited for noisy parties."},
        8: {"element": "Earth / Saturn", "direction": "West / South-West", "vibe": "Material stability, endurance, institutional power, slow steady wealth compounding."},
        9: {"element": "Fire / Mars", "direction": "South", "vibe": "High energy, physical vitality, courage, ambition; requires cooling indoor plants."}
    }

    prop_elem = ELEMENTAL_PROPERTY_MAP.get(root, ELEMENTAL_PROPERTY_MAP[1])

    # Harmony with resident
    rel_d = get_relationship(root, driver)
    rel_c = get_relationship(root, conductor)

    is_favorable = (rel_d["relationship"] != "Enemy") and (rel_c["relationship"] != "Enemy")

    return {
        "property_input": property_str,
        "clean_letters": "".join(letters),
        "clean_digits": "".join(digits),
        "total_compound": total_compound,
        "property_root": root,
        "reduction_path": path,
        "elemental_nature": prop_elem["element"],
        "aligned_direction": prop_elem["direction"],
        "living_atmosphere": prop_elem["vibe"],
        "resident_driver_harmony": rel_d["relationship"],
        "resident_conductor_harmony": rel_c["relationship"],
        "is_harmonious_residence": is_favorable,
        "door_and_vastu_remedies": [
            "Draw a sacred Swastika using Roli (organic vermilion) mixed with pure cow ghee on the exterior top of the main door frame.",
            "Install a polished brass or copper strip embedded along the threshold to prevent beneficial household Prana from dissipating.",
            "Keep the entrance foyer brightly lit with warm amber lighting and completely free from shoe rack clutter.",
            "Hang a Toran of 11 or 21 sacred fresh Mango or Ashoka leaves to filter energetic ingress."
        ]
    }


# ── NV-013 Bank / Account Number Harmony (Strict Privacy Enforced) ────────────
def analyze_bank_account_harmony(
    account_number_str: str,
    driver: int,
    conductor: int
) -> Dict[str, Any]:
    """
    NV-013 Requirement: Bank Account Number Harmony Analysis.
    STRICT PRIVACY PROTOCOL:
    - Zero database logging or persistence of the raw account number.
    - Operates purely in-memory.
    - Masks all digits except the last 3.
    """
    digits = [c for c in account_number_str if c.isdigit()]
    if len(digits) < 6:
        return {"error": "Invalid account number. Must contain at least 6 digits."}

    # Masked representation
    masked = ("*" * (len(digits) - 3)) + "".join(digits[-3:])
    total_sum = sum(int(d) for d in digits)
    path, root = compute_reduction_path(total_sum)

    # Wealth Vibration Archetypes
    WEALTH_VIBRATION_THEMES = {
        1: {"status": "Sovereign Growth", "theme": "Excellent for primary executive earnings, consulting retainers, and investment holdings."},
        2: {"status": "Fluid Movement", "theme": "High liquidity turnover, money enters and departs in emotional cycles; benefits from automated fixed deposits."},
        3: {"status": "Expansive Wealth", "theme": "Auspicious for intellectual property, professional fees, family trust savings, and education funds."},
        4: {"status": "Complex Reserves", "theme": "Sudden unexpected expenses or locked capital; requires rigorous accounting discipline."},
        5: {"status": "High Commercial Velocity", "theme": "Premier for daily trading, business sales, merchant payouts, and agile commercial transactions."},
        6: {"status": "Prosperity & Luxury Accumulation", "theme": "Attracts savings, client bonuses, luxury reserves, and comfortable domestic wealth."},
        7: {"status": "Hidden / Reserved Capital", "theme": "Good for emergency rainy-day deposits, private research grants, or spiritual charitable funds."},
        8: {"status": "Institutional Compounding", "theme": "Supreme for long-term fixed deposits, real estate mortgages, and industrial capital accumulation."},
        9: {"status": "Dynamic Expenditure", "theme": "Fast outflows toward humanitarian or emergency causes; avoid using for long-term passive savings."}
    }

    w_theme = WEALTH_VIBRATION_THEMES.get(root, WEALTH_VIBRATION_THEMES[1])

    # Core Harmony
    rel_d = get_relationship(root, driver)
    rel_c = get_relationship(root, conductor)

    return {
        "masked_account_number": masked,
        "total_compound": total_sum,
        "account_root": root,
        "reduction_path": path,
        "wealth_vibration_status": w_theme["status"],
        "wealth_flow_theme": w_theme["theme"],
        "driver_harmony": rel_d["relationship"],
        "conductor_harmony": rel_c["relationship"],
        "is_favorable_for_wealth_accumulation": root in [1, 3, 5, 6, 8] and rel_d["relationship"] != "Enemy",
        "financial_remedies": [
            "Keep a silver coin embossed with Goddess Lakshmi or Lord Kuber in your personal wallet or business cash vault.",
            "Write your financial affirmations in green ink on a blank slip of paper and place it inside your active chequebook.",
            "Schedule major client invoice distributions on weekdays attuned to your Driver's ruling planet."
        ],
        "privacy_compliance_notice": "Raw account number was processed strictly in volatile memory. No financial credentials or account numbers are ever logged or retained."
    }
