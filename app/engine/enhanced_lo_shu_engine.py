"""
NV-003: ENHANCED LO SHU GRID ANALYSIS ENGINE
Numeros Vision — ANVEIL EVERY CHARM

Extends the Lo Shu grid system with:
1. Birth-date Lo Shu Grid (pure DOB source)
2. Name-derived Lo Shu Grid (Chaldean letter source)
3. Combined overlay view with explicit source tagging
4. Before & After name-change comparison (added/removed occurrences, plane shifts)
5. Driver & Conductor overlay
6. Arrows of Strength & Weakness analysis
7. Configurable color palette for high-contrast accessibility
"""

from typing import Dict, Any, List, Optional, Set
from app.engine.lo_shu import analyze_lo_shu_grid
from app.engine.core_matrix_engine import calculate_chaldean_name

# Standard Lo Shu 3x3 positions:
# [4] [9] [2]  (Row 1: Mental Plane)
# [3] [5] [7]  (Row 2: Emotional Plane)
# [8] [1] [6]  (Row 3: Practical Plane)
# Col 1: Thought (4-3-8), Col 2: Will (9-5-1), Col 3: Action (2-7-6)
# Diag 1: Golden / Rajyog-1 (4-5-6), Diag 2: Silver / Rajyog-2 (2-5-8)

PLANES_SPEC = {
    "Mental Plane": {"digits": [4, 9, 2], "nature": "Intellect, logic, memory, and cognitive sharpness"},
    "Emotional Plane": {"digits": [3, 5, 7], "nature": "Intuition, empathy, feelings, and heart wisdom"},
    "Practical Plane": {"digits": [8, 1, 6], "nature": "Execution, organization, business acumen, and tangible results"},
    "Thought Plane": {"digits": [4, 3, 8], "nature": "Strategic planning, foresight, contemplation, and vision"},
    "Will Plane": {"digits": [9, 5, 1], "nature": "Determination, persistence, stamina, and willpower"},
    "Action Plane": {"digits": [2, 7, 6], "nature": "Speed of execution, physical dynamism, and practical action"},
    "Golden Plane (Rajyog-1)": {"digits": [4, 5, 6], "nature": "Comprehensive material success, fame, leadership, and prosperity"},
    "Silver Plane (Rajyog-2)": {"digits": [2, 5, 8], "nature": "Property stability, asset security, patience, and inner peace"}
}

ARROWS_OF_STRENGTH = {
    "Arrow of Intellect (4-9-2)": "Sharp intellect, exceptional retention, and fast analytical comprehension.",
    "Arrow of Spirituality (3-5-7)": "Deep emotional sensitivity, philosophical calm, and intuitive insight.",
    "Arrow of Practicality (8-1-6)": "Down-to-earth realism, organizational competence, and tangible execution.",
    "Arrow of Planning (4-3-8)": "Architectural mindset, strategic planning, and structural foresight.",
    "Arrow of Willpower (9-5-1)": "Steely tenacity, refusal to give up under pressure, and relentless drive.",
    "Arrow of Determination / Action (2-7-6)": "Immediate physical implementation, dynamism, and quick results.",
    "Arrow of Fortune / Supreme Success (4-5-6)": "Rare harmonious alignment supporting public prestige and commercial success.",
    "Arrow of Property & Stability (2-5-8)": "Natural capacity to acquire and preserve real estate, land, and tangible assets."
}

ARROWS_OF_WEAKNESS = {
    "Arrow of Poor Memory (Missing 4-9-2)": "Tendency toward mental fatigue; benefits from writing reminders and keeping calendars.",
    "Arrow of Emotional Sensitivity (Missing 3-5-7)": "Vulnerability to emotional suppression; benefits from creative arts and calm expression.",
    "Arrow of Impracticality (Missing 8-1-6)": "Tendency toward idealism without commercial grounding; benefits from structured budgets.",
    "Arrow of Disorganization (Missing 4-3-8)": "Scattered planning; benefits from breaking large projects into structured checklists.",
    "Arrow of Hesitation (Missing 9-5-1)": "Fluctuating willpower; benefits from accountability partners and morning focus routines.",
    "Arrow of Delay / Procrastination (Missing 2-7-6)": "Over-contemplating before taking action; benefits from quick, low-stakes physical starts.",
    "Arrow of Loss / Struggle (Missing 4-5-6)": "Hard work requires extra compounding; benefits from disciplined financial safety nets.",
    "Arrow of Instability (Missing 2-5-8)": "Property or emotional grounding fluctuations; benefits from staying rooted in consistent routines."
}


def build_birth_date_grid(day: int, month: int, year: int) -> Dict[str, Any]:
    """
    Constructs the pure birth-date Lo Shu grid from non-zero DDMMYYYY digits ONLY.
    Mulank (Driver), Bhagyank (Conductor), and Kua are NOT added to the grid.
    """
    from app.engine.digit_root import calc_bhagyank, calc_driver
    dob_digits = [int(d) for d in f"{day:02d}{month:02d}{year:04d}" if d != '0']

    driver = calc_driver(day)
    conductor = calc_bhagyank(day, month, year)

    counts: Dict[int, int] = {i: 0 for i in range(1, 10)}
    digit_sources: Dict[int, List[str]] = {i: [] for i in range(1, 10)}

    for d in dob_digits:
        counts[d] += 1
        digit_sources[d].append("dob_raw")
    
    # Evaluate Planes
    planes_eval = {}
    arrows_active = []
    arrows_weak = []
    
    for name, pspec in PLANES_SPEC.items():
        req = pspec["digits"]
        present = [d for d in req if counts[d] > 0]
        missing = [d for d in req if counts[d] == 0]
        pct = round((len(present) / len(req)) * 100)
        
        status = "COMPLETE" if pct == 100 else "PARTIAL" if pct > 0 else "EMPTY"
        planes_eval[name] = {
            "percentage": pct,
            "status": status,
            "present_digits": present,
            "missing_digits": missing,
            "nature": pspec["nature"]
        }
        
        if pct == 100:
            for arrow_name in ARROWS_OF_STRENGTH:
                if all(str(d) in arrow_name for d in req):
                    arrows_active.append({"arrow": arrow_name, "interpretation": ARROWS_OF_STRENGTH[arrow_name]})
        elif pct == 0:
            for arrow_name in ARROWS_OF_WEAKNESS:
                if all(str(d) in arrow_name for d in req):
                    arrows_weak.append({"arrow": arrow_name, "interpretation": ARROWS_OF_WEAKNESS[arrow_name]})
                    
    missing_numbers = [i for i in range(1, 10) if counts[i] == 0]
    repeated_numbers = {i: counts[i] for i in range(1, 10) if counts[i] > 1}
    
    return {
        "grid_type": "BIRTH_DATE_LO_SHU",
        "driver": driver,
        "conductor": conductor,
        "digit_counts": counts,
        "digit_sources": digit_sources,
        "missing_numbers": missing_numbers,
        "repeated_numbers": repeated_numbers,
        "planes": planes_eval,
        "arrows_of_strength": arrows_active,
        "arrows_of_weakness": arrows_weak,
        "grid_visual": [
            [counts[4], counts[9], counts[2]],
            [counts[3], counts[5], counts[7]],
            [counts[8], counts[1], counts[6]]
        ]
    }


def build_name_derived_grid(name: str) -> Dict[str, Any]:
    """
    Constructs the pure Name-derived Lo Shu grid using Chaldean letter mappings.
    Retains source tag 'name_letter' for every occurrence.
    """
    c_info = calculate_chaldean_name(name)
    breakdown = c_info.get("breakdown", [])
    
    counts: Dict[int, int] = {i: 0 for i in range(1, 10)}
    digit_sources: Dict[int, List[str]] = {i: [] for i in range(1, 10)}
    
    for item in breakdown:
        val = item.get("val", 0)
        char = item.get("char", "")
        if 1 <= val <= 9:
            counts[val] += 1
            digit_sources[val].append(f"letter_{char}")
            
    # Also add root number (reduced to 1-9 for Lo Shu grid placement)
    root = c_info.get("single_root", 1)
    while root > 9:
        root = sum(int(d) for d in str(root))
    counts[root] += 1
    digit_sources[root].append("name_root")

    
    missing_numbers = [i for i in range(1, 10) if counts[i] == 0]
    repeated_numbers = {i: counts[i] for i in range(1, 10) if counts[i] > 1}
    
    return {
        "grid_type": "NAME_DERIVED_LO_SHU",
        "name": name,
        "compound_sum": c_info.get("compound_sum"),
        "single_root": root,
        "digit_counts": counts,
        "digit_sources": digit_sources,
        "missing_numbers": missing_numbers,
        "repeated_numbers": repeated_numbers,
        "grid_visual": [
            [counts[4], counts[9], counts[2]],
            [counts[3], counts[5], counts[7]],
            [counts[8], counts[1], counts[6]]
        ]
    }


def compare_name_change_grids(
    day: int,
    month: int,
    year: int,
    original_name: str,
    proposed_name: str
) -> Dict[str, Any]:
    """
    Compares the name-derived grid before and after a proposed name modification.
    Strict non-negotiable rule: Never implies birth-date grid is altered.
    Only the name vibration layer changes.
    """
    birth_grid = build_birth_date_grid(day, month, year)
    orig_name_grid = build_name_derived_grid(original_name)
    prop_name_grid = build_name_derived_grid(proposed_name)
    
    orig_counts = orig_name_grid["digit_counts"]
    prop_counts = prop_name_grid["digit_counts"]
    
    added_occurrences = {}
    removed_occurrences = {}
    unchanged_occurrences = {}
    
    for d in range(1, 10):
        diff = prop_counts[d] - orig_counts[d]
        if diff > 0:
            added_occurrences[d] = diff
        elif diff < 0:
            removed_occurrences[d] = abs(diff)
        else:
            unchanged_occurrences[d] = prop_counts[d]
            
    # Check if proposed name fills missing numbers in birth chart
    birth_missing = set(birth_grid["missing_numbers"])
    prop_present = set(d for d in range(1, 10) if prop_counts[d] > 0)
    filled_gaps = sorted(list(birth_missing.intersection(prop_present)))
    
    # Check driver/conductor harmony with proposed name root
    driver = birth_grid["driver"]
    conductor = birth_grid["conductor"]
    prop_root = prop_name_grid["single_root"]
    
    from app.engine.number_characteristics_registry import get_relationship_status
    rel_driver = get_relationship_status(prop_root, driver)
    rel_conductor = get_relationship_status(prop_root, conductor)
    
    rules_satisfied = []
    rules_failed = []
    
    if rel_driver in ["FRIENDLY", "NEUTRAL"]:
        rules_satisfied.append(f"Name root {prop_root} harmonizes with Driver {driver} ({rel_driver}).")
    else:
        rules_failed.append(f"Name root {prop_root} creates contrast with Driver {driver} ({rel_driver}).")
        
    if rel_conductor in ["FRIENDLY", "NEUTRAL"]:
        rules_satisfied.append(f"Name root {prop_root} harmonizes with Conductor {conductor} ({rel_conductor}).")
    else:
        rules_failed.append(f"Name root {prop_root} creates contrast with Conductor {conductor} ({rel_conductor}).")
        
    if filled_gaps:
        rules_satisfied.append(f"Proposed spelling introduces harmonic support for missing birth energies: {filled_gaps}.")
        
    return {
        "original_name": original_name,
        "proposed_name": proposed_name,
        "original_root": orig_name_grid["single_root"],
        "proposed_root": prop_root,
        "original_compound": orig_name_grid["compound_sum"],
        "proposed_compound": prop_name_grid["compound_sum"],
        "added_occurrences": added_occurrences,
        "removed_occurrences": removed_occurrences,
        "unchanged_occurrences": unchanged_occurrences,
        "birth_missing_gaps_supported": filled_gaps,
        "driver_harmony": rel_driver,
        "conductor_harmony": rel_conductor,
        "rules_satisfied": rules_satisfied,
        "rules_failed": rules_failed,
        "notice": "A name change adjusts vibrational resonance; it does not alter your unchangeable birth-date grid."
    }
