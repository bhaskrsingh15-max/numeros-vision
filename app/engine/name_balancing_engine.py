"""
NV-004: NAME BALANCING ENGINE
Grounding: Classical Chaldean/Cheiro Numerology, Vedic Name Balancing, Lo Shu Integration.

Deterministic capabilities:
1. Segment Analysis: First name, middle name, last name totals & compound values.
2. Rule-by-rule evaluation:
   - First-name root vibration & compatibility
   - Full-name compound vibration (auspicious vs malefic/karmic compounds)
   - Compatibility of Full-name root and First-name root with Driver and Conductor
   - Lo Shu Grid integration: identify missing numbers filled without over-repetition
3. Candidate Generator: Compares original vs suggested spellings with pass/fail audit table.
4. Explanations of letter additions/subtractions, compound shifts, and vibrational harmony.
"""

from typing import Dict, Any, List, Optional, Set
import re
import sys
import os

# Ensure workspace root in path
workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from app.engine.cheiro_engine import (
    CHALDEAN_LETTER_VALUES,
    analyze_number,
    compute_reduction_path,
    CHEIRO_DATASET
)
from app.engine.number_characteristics_registry import (
    get_number_profile,
    get_relationship,
    PLANETARY_RULERS
)
from app.engine.enhanced_lo_shu_engine import (
    build_birth_date_grid,
    build_name_derived_grid,
    compare_name_change_grids
)


# Canonical Auspicious vs Challenging Cheiro Compounds
AUSPICIOUS_COMPOUNDS: Set[int] = {10, 14, 15, 19, 20, 21, 23, 24, 27, 30, 32, 33, 34, 37, 41, 42, 45, 46, 50}
CHALLENGING_COMPOUNDS: Set[int] = {11, 12, 13, 16, 18, 22, 26, 28, 29, 31, 35, 38, 43, 44, 48, 51, 52}

# Canonical Cheiro / Chaldean Sacred Benefic Roots (Only 1, 3, 5, 6 allowed for balanced names)
BENEFIC_ROOTS: Set[int] = {1, 3, 5, 6}


def get_anti_numbers_for(num: int) -> Set[int]:
    """Returns canonical anti/opposite numbers for a root number."""
    antis = set()
    if num == 1:
        antis.update({8})  # Sun vs Saturn arch-rivals
    elif num == 2:
        antis.update({4, 8, 9})  # Moon vs Rahu, Saturn, Mars
    elif num == 3:
        antis.update({6})  # Jupiter (Dev Guru) vs Venus (Daitya Guru)
    elif num == 4:
        antis.update({1, 2, 8, 9})  # Rahu
    elif num == 5:
        pass  # Mercury is universal neutral/friend
    elif num == 6:
        antis.update({3})  # Venus vs Jupiter
    elif num == 7:
        antis.update({8, 9})  # Ketu vs Saturn, Mars
    elif num == 8:
        antis.update({1, 2, 4, 8})  # Saturn vs Sun, Moon, Rahu
    elif num == 9:
        antis.update({2, 4})  # Mars vs Moon, Rahu
    return antis


def is_anti_combination(root: int, target: int) -> bool:
    """Returns True if root and target form an anti / opposite combination."""
    if (root == 3 and target == 6) or (root == 6 and target == 3):
        return True
    if (root == 1 and target == 8) or (root == 8 and target == 1):
        return True
    return root in get_anti_numbers_for(target) or target in get_anti_numbers_for(root)


# Letter values reference for quick inspection
LETTER_VIBRATION_GUIDE = {
    1: ["A", "I", "J", "Q", "Y"],  # Sun energy: Leadership, courage, vitality
    2: ["B", "C", "K", "R"],       # Moon energy: Creativity, sensitivity, imagination
    3: ["G", "L", "S"],            # Jupiter energy: Wisdom, expression, expansion
    4: ["D", "M", "T"],            # Rahu energy: Structure, diligence, sudden breakthroughs
    5: ["E", "H", "N", "X"],       # Mercury energy: Communication, versatility, commerce
    6: ["U", "V", "W"],            # Venus energy: Harmony, affection, luxury, attraction
    7: ["O", "Z"],                 # Ketu energy: Depth, intuition, research, mystery
    8: ["F", "P"]                  # Saturn energy: Endurance, material authority, discipline
}


def calculate_word_value(word: str) -> Dict[str, Any]:
    """Calculates Chaldean compound and root value for a single word/segment."""
    clean_word = "".join(c.upper() for c in word if c.isalpha())
    if not clean_word:
        return {
            "word": word,
            "clean_word": "",
            "letter_breakdown": [],
            "compound_sum": 0,
            "root_number": 0,
            "reduction_path": "0 -> 0",
            "planet": "None"
        }

    breakdown = [{"letter": c, "value": CHALDEAN_LETTER_VALUES.get(c, 0)} for c in clean_word]
    compound = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean_word)
    red_path, root = compute_reduction_path(compound)
    planet = PLANETARY_RULERS.get(root, {}).get("planet", "Unknown")

    return {
        "word": word,
        "clean_word": clean_word,
        "letter_breakdown": breakdown,
        "compound_sum": compound,
        "root_number": root,
        "reduction_path": red_path,
        "planet": planet
    }


def calculate_segment_values(full_name: str) -> Dict[str, Any]:
    """
    NV-004 Requirement: Segment analysis of full name.
    Analyzes first name, middle name (if present), and last name individually,
    plus overall full name totals.
    """
    words = [w.strip() for w in full_name.split() if w.strip()]
    if not words:
        return {"error": "Name must contain alphabetic characters."}

    segments = []
    for idx, w in enumerate(words):
        seg_data = calculate_word_value(w)
        if idx == 0:
            role = "First Name"
        elif idx == len(words) - 1:
            role = "Last Name / Surname"
        else:
            role = f"Middle Name {idx}"
        seg_data["role"] = role
        segments.append(seg_data)

    clean_full = "".join(c.upper() for c in full_name if c.isalpha())
    full_breakdown = [{"letter": c, "value": CHALDEAN_LETTER_VALUES.get(c, 0)} for c in clean_full]
    full_compound = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean_full)
    full_path, full_root = compute_reduction_path(full_compound)
    full_planet = PLANETARY_RULERS.get(full_root, {}).get("planet", "Unknown")

    first_segment = segments[0]
    last_segment = segments[-1] if len(segments) > 1 else None

    return {
        "full_name": full_name,
        "clean_full_name": clean_full,
        "letter_breakdown": full_breakdown,
        "full_compound": full_compound,
        "full_root": full_root,
        "full_reduction_path": full_path,
        "full_planet": full_planet,
        "segments": segments,
        "first_name_compound": first_segment["compound_sum"],
        "first_name_root": first_segment["root_number"],
        "first_name_planet": first_segment["planet"],
        "last_name_compound": last_segment["compound_sum"] if last_segment else None,
        "last_name_root": last_segment["root_number"] if last_segment else None
    }


def parse_dob(dob_str: str) -> Optional[tuple[int, int, int]]:
    """Parses various date string formats (YYYY-MM-DD, DD/MM/YYYY, DD-MM-YYYY) into (day, month, year)."""
    clean_str = dob_str.strip()
    match = re.search(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", clean_str)
    if match:
        return int(match.group(3)), int(match.group(2)), int(match.group(1))
    match2 = re.search(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{4})", clean_str)
    if match2:
        return int(match2.group(1)), int(match2.group(2)), int(match2.group(3))
    return None


def evaluate_name_lo_shu_diff(dob_str: str, full_name: str) -> Dict[str, Any]:
    """Evaluates how a name interacts with the birth-date Lo Shu grid."""
    parsed = parse_dob(dob_str)
    if not parsed:
        return {"error": "Invalid date format"}
    day, month, year = parsed

    birth_grid = build_birth_date_grid(day, month, year)
    name_grid = build_name_derived_grid(full_name)

    missing = set(birth_grid["missing_numbers"])
    name_counts = name_grid["digit_counts"]
    name_present = set(d for d in range(1, 10) if name_counts[d] > 0)

    filled = sorted(list(missing.intersection(name_present)))
    
    # Over repeated: present in birth >= 2 and added in name >= 2
    birth_repeated = set(birth_grid.get("repeated_numbers", {}).keys())
    over_repeated = [d for d in birth_repeated if name_counts[d] >= 2]

    return {
        "birth_missing": sorted(list(missing)),
        "missing_numbers_filled_by_name": filled,
        "over_repeated_added": over_repeated,
        "name_digits_present": sorted(list(name_present))
    }


def evaluate_name_rules(
    full_name: str,
    driver: int,
    conductor: int,
    dob_str: Optional[str] = None
) -> Dict[str, Any]:
    """
    Performs comprehensive Cheiro / Chaldean Canonical Name Vibration Evaluation:

    1. First-Name Root Vibration: Must sum to sacred benefic roots (1, 3, 5, 6 only).
    2. First-Name Anti / Opposite Check: Must avoid anti combinations with Driver & Conductor.
    3. Overall Name Root Vibration: Must sum to sacred benefic roots (1, 3, 5, 6 only).
    4. Overall Name Anti / Opposite Check: Must avoid anti combinations with Driver & Conductor.
    5. Full-Name Compound Auspiciousness & Karmic Filter (Cheiro canon).
    6. Lo Shu Grid integration (missing numbers filled, repeated numbers avoided).
    """
    seg = calculate_segment_values(full_name)
    if "error" in seg:
        return seg

    first_root = seg["first_name_root"]
    full_compound = seg["full_compound"]
    full_root = seg["full_root"]

    # Rule 1: First Name Root Sum Total (Must be in benefic roots 1, 3, 5, 6)
    rule1_pass = first_root in BENEFIC_ROOTS
    rule1_score = 20 if rule1_pass else 0
    if rule1_pass:
        rule1_desc = f"Primary segment resolves into an auspicious planetary frequency."
    else:
        rule1_desc = f"Primary segment exhibits vibrational resistance with benefic planetary channels."

    # Rule 2: First Name Anti / Opposite Check with Driver & Conductor
    anti_fn_driver = is_anti_combination(first_root, driver)
    anti_fn_cond = is_anti_combination(first_root, conductor)
    rule2_pass = not anti_fn_driver and not anti_fn_cond
    rule2_score = 20 if rule2_pass else 0
    if rule2_pass:
        rule2_desc = f"Primary segment has zero anti-planetary friction with birth Driver and Conductor."
    else:
        conflicts = []
        if anti_fn_driver:
            conflicts.append("Driver")
        if anti_fn_cond:
            conflicts.append("Conductor")
        rule2_desc = f"Primary segment creates anti-planetary friction with {' & '.join(conflicts)}."

    # Rule 3: Overall Name Root Sum Total (Must be in benefic roots 1, 3, 5, 6)
    rule3_pass = full_root in BENEFIC_ROOTS
    rule3_score = 20 if rule3_pass else 0
    if rule3_pass:
        rule3_desc = f"Overall name frequency resolves into an auspicious planetary channel."
    else:
        rule3_desc = f"Overall name frequency exhibits vibrational resistance with benefic planetary channels."

    # Rule 4: Overall Name Anti / Opposite Check with Driver & Conductor
    anti_full_driver = is_anti_combination(full_root, driver)
    anti_full_cond = is_anti_combination(full_root, conductor)
    rule4_pass = not anti_full_driver and not anti_full_cond
    rule4_score = 20 if rule4_pass else 0
    if rule4_pass:
        rule4_desc = f"Overall name has zero anti-planetary friction with birth Driver and Conductor."
    else:
        conflicts = []
        if anti_full_driver:
            conflicts.append("Driver")
        if anti_full_cond:
            conflicts.append("Conductor")
        rule4_desc = f"Overall name creates anti-planetary friction with {' & '.join(conflicts)}."

    # Rule 5: Full Name Compound Auspiciousness & Karmic Filter
    is_challenging = full_compound in CHALLENGING_COMPOUNDS
    is_auspicious = full_compound in AUSPICIOUS_COMPOUNDS and full_root in BENEFIC_ROOTS
    cheiro_profile = analyze_number(full_compound)
    archetype = cheiro_profile.get("input_compound_archetype", "Compound Vibration")

    if is_challenging:
        rule5_pass = False
        rule5_score = 0
        rule5_desc = "Compound vibration carries traditional karmic resistance warnings."
    elif is_auspicious:
        rule5_pass = True
        rule5_score = 15
        rule5_desc = "Compound vibration possesses an auspicious vibrational current."
    else:
        rule5_pass = True
        rule5_score = 10
        rule5_desc = "Compound vibration offers a neutral operational frequency."

    # Rule 6: Lo Shu Grid Integration (if DOB provided)
    rule6_score = 5
    rule6_pass = True
    rule6_desc = "Birth chart elemental balance evaluated."
    lo_shu_diff = None

    if dob_str:
        lo_shu_diff = evaluate_name_lo_shu_diff(dob_str, full_name)
        gaps_filled = lo_shu_diff.get("missing_numbers_filled_by_name", [])
        over_repeated = lo_shu_diff.get("over_repeated_added", [])

        if gaps_filled:
            rule6_score = 5
            rule6_desc = "Name vibration brings missing birth energies into active expression."
        if over_repeated:
            rule6_score = 0
            rule6_desc += " Note: Name vibration adds heavy planetary repetition."
            if len(over_repeated) > 1:
                rule6_pass = False

    total_score = min(max(rule1_score + rule2_score + rule3_score + rule4_score + rule5_score + rule6_score, 0), 100)

    # Definitive Alignment Flag:
    # Name is ALIGNED only if First Name & Overall Name roots are strictly in {1, 3, 5, 6},
    # have zero anti/opposite conflict with Driver & Conductor, and compound is free of karmic debts.
    is_aligned = bool(
        rule1_pass and
        rule2_pass and
        rule3_pass and
        rule4_pass and
        not is_challenging and
        (total_score >= 70)
    )

    if is_aligned:
        verdict = "Optimal Name Balance"
        recommendation = "Your current name spelling is harmonious and supportive with your birth Driver and Conductor matrix. No structural alteration required."
    else:
        verdict = "Name Misalignment Detected"
        recommendation = "Your current name spelling creates energetic friction with your birth matrix. Authentic name balancing is calibrated exclusively via a private 1-on-1 consultation."

    rules = [
        {"rule_id": "R1_PRIMARY_RESONANCE", "name": "Primary Acoustic Resonance", "passed": rule1_pass, "score": rule1_score, "max_score": 20, "details": rule1_desc},
        {"rule_id": "R2_PRIMARY_MATRIX", "name": "Primary Matrix Harmony", "passed": rule2_pass, "score": rule2_score, "max_score": 20, "details": rule2_desc},
        {"rule_id": "R3_FULL_RESONANCE", "name": "Overall Planetary Resonance", "passed": rule3_pass, "score": rule3_score, "max_score": 20, "details": rule3_desc},
        {"rule_id": "R4_FULL_MATRIX", "name": "Overall Matrix Harmony", "passed": rule4_pass, "score": rule4_score, "max_score": 20, "details": rule4_desc},
        {"rule_id": "R5_COMPOUND_VIBRATION", "name": "Compound Harmonic Frequency", "passed": rule5_pass, "score": rule5_score, "max_score": 15, "details": rule5_desc},
        {"rule_id": "R6_MATRIX_BALANCE", "name": "Elemental Energy Balancing", "passed": rule6_pass, "score": rule6_score, "max_score": 5, "details": rule6_desc}
    ]

    return {
        "full_name": full_name,
        "segment_analysis": seg,
        "rules": rules,
        "total_score": total_score,
        "is_aligned": is_aligned,
        "verdict": verdict,
        "recommendation": recommendation,
        "lo_shu_diff": lo_shu_diff
    }


def generate_spelling_candidates(
    original_name: str,
    driver: int,
    conductor: int,
    dob_str: Optional[str] = None,
    custom_candidates: Optional[List[str]] = None,
    max_candidates: int = 5
) -> List[Dict[str, Any]]:
    """
    Sacred Sanctuary Policy: Name balancing is NOT done automatically on the app.
    It is calibrated exclusively by Master Numerologists during 1-on-1 consultations.
    This function returns an empty list to protect sacred methodology from algorithmic misuse.
    """
    return []

    original_eval = evaluate_name_rules(original_name, driver, conductor, dob_str)
    orig_score = original_eval.get("total_score", 50)

    words = original_name.strip().split()
    if not words:
        return []

    first_name = words[0]
    rest_names = " ".join(words[1:]) if len(words) > 1 else ""

    candidates_to_test = []
    if custom_candidates:
        candidates_to_test.extend(custom_candidates)

    # Systematic numerological variations
    # 1. Double last vowel in first name
    vowels = "AEIOU"
    for idx in range(len(first_name) - 1, -1, -1):
        if first_name[idx].upper() in vowels:
            char = first_name[idx]
            cand = first_name[:idx] + char + first_name[idx:]
            cand_full = f"{cand} {rest_names}".strip()
            if cand_full != original_name and cand_full not in candidates_to_test:
                candidates_to_test.append(cand_full)
            break

    # 2. Add 'A' or 'I' (value 1 Sun) to first name ending
    for add_char in ["A", "I", "H", "N", "E"]:
        cand_full = f"{first_name}{add_char} {rest_names}".strip()
        if cand_full != original_name and cand_full not in candidates_to_test:
            candidates_to_test.append(cand_full)

    # 3. Double key consonants like 'R' (2), 'S' (3), 'N' (5)
    for c_idx, char in enumerate(first_name):
        if char.upper() in ["R", "N", "S", "K", "L"]:
            cand = first_name[:c_idx] + char + first_name[c_idx:]
            cand_full = f"{cand} {rest_names}".strip()
            if cand_full != original_name and cand_full not in candidates_to_test:
                candidates_to_test.append(cand_full)
            if len(candidates_to_test) >= 12:
                break

    evaluated_candidates = []
    for cand_name in candidates_to_test:
        c_eval = evaluate_name_rules(cand_name, driver, conductor, dob_str)
        if "error" in c_eval:
            continue

        c_score = c_eval["total_score"]
        c_comp = c_eval["segment_analysis"]["full_compound"]
        c_root = c_eval["segment_analysis"]["full_root"]

        # Explain letter modification
        diff_explanation = explain_spelling_diff(original_name, cand_name)

        evaluated_candidates.append({
            "candidate_name": cand_name,
            "full_compound": c_comp,
            "full_root": c_root,
            "first_name_root": c_eval["segment_analysis"]["first_name_root"],
            "compound_archetype": analyze_number(c_comp).get("input_compound_archetype", ""),
            "score": c_score,
            "score_delta": c_score - orig_score,
            "is_auspicious_compound": c_comp in AUSPICIOUS_COMPOUNDS,
            "passes_driver_compat": c_eval["rules"][0]["passed"],
            "passes_conductor_compat": c_eval["rules"][2]["passed"],
            "lo_shu_gaps_filled": (
                c_eval["lo_shu_diff"].get("missing_numbers_filled_by_name", [])
                if c_eval.get("lo_shu_diff") else []
            ),
            "verdict": c_eval["verdict"],
            "modification_rationale": diff_explanation,
            "detailed_rules": c_eval["rules"]
        })

    # Sort candidates by score descending, preferring auspicious compounds
    evaluated_candidates.sort(
        key=lambda x: (x["score"], 1 if x["is_auspicious_compound"] else 0, x["score_delta"]),
        reverse=True
    )

    return evaluated_candidates[:max_candidates]


def explain_spelling_diff(orig_name: str, new_name: str) -> str:
    """Explains why specific letters were added or altered in the spelling."""
    clean_orig = "".join(c.upper() for c in orig_name if c.isalpha())
    clean_new = "".join(c.upper() for c in new_name if c.isalpha())

    orig_val = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean_orig)
    new_val = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean_new)
    val_diff = new_val - orig_val

    added_letters = []
    # Simple count diff
    from collections import Counter
    orig_c = Counter(clean_orig)
    new_c = Counter(clean_new)

    for char, cnt in new_c.items():
        if cnt > orig_c.get(char, 0):
            added_letters.append(f"'{char}' (+{CHALDEAN_LETTER_VALUES.get(char, 0)})")

    if not added_letters:
        return f"Spelling adjusted to shift compound vibration from {orig_val} to {new_val}."

    letters_str = ", ".join(added_letters)
    return (
        f"Added {letters_str}, shifting name sum by {val_diff:+d} (from {orig_val} to {new_val}). "
        f"This transitions the energetic frequency toward a harmonious compound vibration."
    )


def generate_candidate_comparison_table(
    original_name: str,
    candidates: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Formats comparison table suitable for reporting and frontend display."""
    table = []
    for cand in candidates:
        table.append({
            "name": cand["candidate_name"],
            "compound": cand["full_compound"],
            "root": cand["full_root"],
            "archetype": cand["compound_archetype"],
            "score": cand["score"],
            "delta": f"{cand['score_delta']:+d}" if cand["score_delta"] != 0 else "0",
            "driver_compat": "Pass" if cand["passes_driver_compat"] else "Fail",
            "conductor_compat": "Pass" if cand["passes_conductor_compat"] else "Fail",
            "gaps_filled": ", ".join(map(str, cand["lo_shu_gaps_filled"])) if cand["lo_shu_gaps_filled"] else "None",
            "rationale": cand["modification_rationale"]
        })
    return table
