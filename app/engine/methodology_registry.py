"""
NV-001: CALCULATION AND METHODOLOGY REGISTRY
Numeros Vision — ANVEIL EVERY CHARM

Formalizes the centralized registry of validated numerology and predictive methodologies.
Preserves all existing calculation formulas without alteration while providing
structured metadata, versioning, input requirements, and deterministic execution traces.
"""

from typing import Dict, Any, List, Optional, Callable
import datetime

# Import validated underlying calculation engines
from app.engine.vedic_numerology import (
    calculate_mulank,
    calculate_bhagyank,
    analyze_vedic_numerology,
    reduce_to_single_digit
)
from app.engine.core_matrix_engine import (
    calculate_chaldean_name,
    calculate_dasha_cycles,
    get_kua_profile,
    analyze_repeat_numbers,
    analyze_missing_numbers,
    analyze_elements_balancing,
    assess_karmic_and_master
)
from app.engine.lo_shu import analyze_lo_shu_grid
from app.engine.cheiro_engine import (
    analyze_number,
    analyze_birth_day_cheiro,
    analyze_name_cheiro,
    analyze_dob_conductor_cheiro
)
from phase4_bnn_engine import run_full_bnn_analysis
from phase5_lal_kitab_engine import run_full_lal_kitab_analysis
from phase7_kp_engine import analyze_kp_sub_lord
from phase8_btr_engine import run_full_btr_analysis
from app.engine.pythagorean_engine import analyze_pythagorean_full


METHODOLOGY_REGISTRY: Dict[str, Dict[str, Any]] = {
    "METH-VEDIC-001": {
        "methodology_id": "METH-VEDIC-001",
        "name": "Vedic Sankhya Shastra (Driver & Conductor)",
        "school": "Vedic Numerology",
        "version": "1.0.0",
        "effective_date": "2026-01-01",
        "reduction_convention": "Iterative single-digit sum (1-9)",
        "compound_handling": "Day compound preserved for Cheiro cross-check",
        "input_requirements": ["day", "month", "year"],
        "output_schema": {
            "driver_number": "int (1-9)",
            "conductor_number": "int (1-9)",
            "driver_planet": "str",
            "conductor_planet": "str",
            "friendly_numbers": "List[int]",
            "enemy_numbers": "List[int]"
        },
        "formula_reference": "app.engine.vedic_numerology.analyze_vedic_numerology",
        "fn": analyze_vedic_numerology,
        "status": "ACTIVE"
    },
    "METH-CHALDEAN-001": {
        "methodology_id": "METH-CHALDEAN-001",
        "name": "Classical Chaldean Name Vibration Analysis",
        "school": "Chaldean Numerology",
        "version": "1.0.0",
        "effective_date": "2026-01-01",
        "reduction_convention": "Chaldean sound frequency 1-8 table (9 excluded from alphabet)",
        "compound_handling": "Preserves compound numbers 10-52; reduces to single root 1-9",
        "input_requirements": ["name"],
        "output_schema": {
            "compound_sum": "int",
            "single_root": "int (1-9)",
            "is_karmic": "bool",
            "letter_breakdown": "List[Dict[str, int]]"
        },
        "formula_reference": "app.engine.core_matrix_engine.calculate_chaldean_name",
        "fn": calculate_chaldean_name,
        "status": "ACTIVE"
    },
    "METH-LOSHU-001": {
        "methodology_id": "METH-LOSHU-001",
        "name": "Ancient 3x3 Lo Shu Celestial Magic Square",
        "school": "Lo Shu Chinese Numerology",
        "version": "1.0.0",
        "effective_date": "2026-01-01",
        "reduction_convention": "Direct digit extraction from birth date and master numbers",
        "compound_handling": "Non-reduced digits mapped to fixed 3x3 positions",
        "input_requirements": ["day", "month", "year"],
        "output_schema": {
            "grid_counts": "Dict[int, int]",
            "completed_planes": "List[str]",
            "incomplete_planes": "List[str]",
            "missing_numbers": "List[int]"
        },
        "formula_reference": "app.engine.lo_shu.analyze_lo_shu_grid",
        "fn": analyze_lo_shu_grid,
        "status": "ACTIVE"
    },
    "METH-KUA-001": {
        "methodology_id": "METH-KUA-001",
        "name": "Numero-Vastu Directional Alignment",
        "school": "Cosmic Directional Science & Planetary Vastu",
        "version": "1.1.0",
        "effective_date": "2026-01-01",
        "reduction_convention": "Century-invariant 4-digit calendar birth year single-digit reduction x; Male: 11 - x, Female: 4 + x",
        "compound_handling": "Single digit Kua 1-9 (5 maps to 2 for male, 8 for female; missing gender returns Kua needs gender)",
        "input_requirements": ["year"],
        "optional_inputs": ["gender"],
        "output_schema": {
            "kua_number": "Optional[int]",
            "kua_display": "str",
            "group": "str (East Group / West Group)",
            "element": "str",
            "favorable_directions": "Dict[str, str]"
        },
        "formula_reference": "app.engine.core_matrix_engine.get_kua_profile",
        "fn": get_kua_profile,
        "status": "ACTIVE"
    },
    "METH-DASHA-001": {
        "methodology_id": "METH-DASHA-001",
        "name": "Vedic Dasha & Personal Time Period Cycles",
        "school": "Vedic Planetary Timing",
        "version": "1.0.0",
        "effective_date": "2026-01-01",
        "reduction_convention": "Cyclic 9-year progression + Mahadasha planetary rulership",
        "compound_handling": "Preserves current year, month, and day vibration",
        "input_requirements": ["day", "month", "year"],
        "output_schema": {
            "personal_year": "int",
            "personal_month": "int",
            "personal_day": "int",
            "mahadasha": "Dict[str, Any]"
        },
        "formula_reference": "app.engine.core_matrix_engine.calculate_dasha_cycles",
        "fn": calculate_dasha_cycles,
        "status": "ACTIVE"
    },
    "METH-BNN-001": {
        "methodology_id": "METH-BNN-001",
        "name": "Bhrigu Nandi Nadi (BNN) Planetary Alignment",
        "school": "Nadi Astrology",
        "version": "1.1.0",
        "effective_date": "2026-01-01",
        "reduction_convention": "1-5-9 Trinal Sambandha, 2-12 Stacking, 7th Opposition, 10th from Saturn",
        "compound_handling": "Absolute planetary longitudes and sign placements",
        "input_requirements": ["chart"],
        "output_schema": {
            "active_combinations": "List[Dict[str, Any]]",
            "tenth_from_saturn": "Dict[str, Any]",
            "transits_and_timing": "Dict[str, Any]"
        },
        "formula_reference": "phase4_bnn_engine.run_full_bnn_analysis",
        "fn": run_full_bnn_analysis,
        "status": "ACTIVE"
    },
    "METH-LALKITAB-001": {
        "methodology_id": "METH-LALKITAB-001",
        "name": "Lal Kitab House Placements & Awakening Ages",
        "school": "Lal Kitab Traditional Astrology",
        "version": "1.0.0",
        "effective_date": "2026-01-01",
        "reduction_convention": "Fixed house positions 1-12 without sign modifications",
        "compound_handling": "Masnooi artificial pairings and specific practical remedies",
        "input_requirements": ["chart"],
        "output_schema": {
            "lal_kitab_remedies": "List[Dict[str, Any]]",
            "house_positions": "Dict[str, int]"
        },
        "formula_reference": "phase5_lal_kitab_engine.run_full_lal_kitab_analysis",
        "fn": run_full_lal_kitab_analysis,
        "status": "ACTIVE"
    },
    "METH-KP-001": {
        "methodology_id": "METH-KP-001",
        "name": "KP Astrology Cuspal Sub-Lord & Nakshatra Precision",
        "school": "Krishnamurti Paddhati",
        "version": "1.0.0",
        "effective_date": "2026-01-01",
        "reduction_convention": "249 sub-lord divisions of 27 Nakshatras across 12 signs",
        "compound_handling": "Exact arc minute and second division",
        "input_requirements": ["moon_absolute_longitude"],
        "output_schema": {
            "kp_star_lord": "str",
            "kp_sub_lord": "str",
            "nakshatra_name": "str"
        },
        "formula_reference": "phase7_kp_engine.analyze_kp_sub_lord",
        "fn": analyze_kp_sub_lord,
        "status": "ACTIVE"
    },
    "METH-PYTH-001": {
        "methodology_id": "METH-PYTH-001",
        "name": "Western Pythagorean Numerology (Life Path & Expression)",
        "school": "Pythagorean Western Numerology",
        "version": "1.0.0",
        "effective_date": "2026-01-01",
        "reduction_convention": "Standard 1-9 Western table + 3-tier date reduction with Master Numbers 11/22/33 and Karmic Debts 13/14/16/19 preservation",
        "compound_handling": "Preserves compound and single root values with Western planetary symbolism",
        "input_requirements": ["day", "month", "year"],
        "optional_inputs": ["name"],
        "output_schema": {
            "life_path": "Dict[str, Any]",
            "birthday_number": "Dict[str, Any]",
            "name_numerology": "Optional[Dict[str, Any]]",
            "pinnacles_and_cycles": "Dict[str, Any]"
        },
        "formula_reference": "app.engine.pythagorean_engine.analyze_pythagorean_full",
        "fn": analyze_pythagorean_full,
        "status": "ACTIVE"
    }
}


def get_methodology(methodology_id: str) -> Optional[Dict[str, Any]]:
    """Retrieves methodology metadata by unique ID."""
    return METHODOLOGY_REGISTRY.get(methodology_id)


def list_methodologies() -> List[Dict[str, Any]]:
    """Returns a list of all active registered methodologies without internal function pointers."""
    result = []
    for m in METHODOLOGY_REGISTRY.values():
        item = {k: v for k, v in m.items() if k != "fn"}
        result.append(item)
    return result


def execute_methodology(methodology_id: str, inputs: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes a methodology deterministically through its validated formula function.
    Returns the exact calculation result annotated with execution metadata and trace reference.
    """
    meta = METHODOLOGY_REGISTRY.get(methodology_id)
    if not meta:
        raise ValueError(f"Unknown methodology ID: '{methodology_id}'.")
    
    fn = meta["fn"]
    
    # Normalize birth_year -> year alias if caller provided birth_year
    norm_inputs = dict(inputs)
    if "year" not in norm_inputs and "birth_year" in norm_inputs:
        norm_inputs["year"] = norm_inputs["birth_year"]

    # Map inputs according to requirements
    reqs = meta["input_requirements"]
    missing = [r for r in reqs if r not in norm_inputs]
    if missing:
        raise ValueError(f"Methodology '{methodology_id}' requires missing inputs: {missing}")
    
    call_args = [norm_inputs[r] for r in reqs]
    opt_reqs = meta.get("optional_inputs", [])
    for opt in opt_reqs:
        if opt in norm_inputs:
            call_args.append(norm_inputs[opt])
    output = fn(*call_args)
    
    return {
        "methodology_id": meta["methodology_id"],
        "methodology_name": meta["name"],
        "version": meta["version"],
        "school": meta["school"],
        "reduction_convention": meta["reduction_convention"],
        "executed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "is_deterministic": True,
        "result": output
    }
