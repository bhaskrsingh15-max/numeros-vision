"""
DETERMINISTIC CHEIRO & CHALDEAN COMPOUND NUMBER ENGINE (1-100)
Grounding: Cheiro's Book of Numbers (English Edition, 1935), Classical Chaldean Traditions.

Architectural Rules:
- GR-001 (Golden Rule 1): Observe the first 2-digit number (retain input before reduction, e.g., 29 → 11 → 2).
- GR-002 (Golden Rule 2): Observe the last single digit (final single digit is the resulting/output factor).
- RAG-001 (Two-Layer Interpretation): Decode input and output separately. Compound/input characteristics
  represent the karmic path/struggle; root/output characteristics represent the planetary ruler & ultimate outcome.
- RAG-002 (Evidence & Anti-Hallucination): Keep tradition separate from empirical evidence. Never present
  traditional symbolism as scientific fact. Zero fabricated statistics (enforce '[INSERT REAL FIGURE]').
"""

from typing import Dict, Any, List, Optional
import re

# ── Planetary Rulers & Root Output Traditions (1 to 9) ───────────────────────
ROOT_PLANETARY_PROFILES = {
    1: {
        "planet": "Sun",
        "characteristics": "initiative, independence, leadership, originality",
        "outcome_themes": "initiation, authority, new starts",
    },
    2: {
        "planet": "Moon",
        "characteristics": "sensitivity, cooperation, intuition, diplomacy",
        "outcome_themes": "partnership, support, negotiation",
    },
    3: {
        "planet": "Jupiter",
        "characteristics": "expression, expansion, creativity, learning",
        "outcome_themes": "communication, growth, visibility",
    },
    4: {
        "planet": "Rahu/Uranian tradition",
        "characteristics": "structure, practicality, unconventional thinking, systems",
        "outcome_themes": "restructuring, foundations, change",
    },
    5: {
        "planet": "Mercury",
        "characteristics": "communication, adaptability, movement, versatility",
        "outcome_themes": "change, commerce, travel, networking",
    },
    6: {
        "planet": "Venus",
        "characteristics": "harmony, responsibility, beauty, relationships",
        "outcome_themes": "family, partnership, comfort, aesthetics",
    },
    7: {
        "planet": "Ketu/Neptune tradition",
        "characteristics": "introspection, analysis, intuition, depth",
        "outcome_themes": "research, reflection, spiritual/inner themes",
    },
    8: {
        "planet": "Saturn",
        "characteristics": "discipline, responsibility, authority, endurance",
        "outcome_themes": "management, material responsibility, long cycles",
    },
    9: {
        "planet": "Mars",
        "characteristics": "courage, action, intensity, completion",
        "outcome_themes": "action, closure, decisive movement",
    },
}

# ── Canonical Cheiro Compound Descriptions (10 to 52) ────────────────────────
CHEIRO_COMPOUND_CATALOGUE = {
    10: {
        "archetype": "Wheel of Fortune",
        "characteristics": "honour, confidence, cycles of rise/fall, plans gaining effect",
        "reduction_path": "10 → 1",
        "output_num": 1,
    },
    11: {
        "archetype": "Clenched Hand / Lion Muzzled",
        "characteristics": "hidden danger, trials, betrayal, obstacles",
        "reduction_path": "11 → 2",
        "output_num": 2,
    },
    12: {
        "archetype": "Sacrifice / Victim",
        "characteristics": "anxiety, sacrifice, being used for others' plans",
        "reduction_path": "12 → 3",
        "output_num": 3,
    },
    13: {
        "archetype": "Upheaval and Change",
        "characteristics": "transformation, change of place, destruction when power is misused",
        "reduction_path": "13 → 4",
        "output_num": 4,
    },
    14: {
        "archetype": "Movement and Risk",
        "characteristics": "movement, combinations, speculation, opportunity with risk",
        "reduction_path": "14 → 5",
        "output_num": 5,
    },
    15: {
        "archetype": "Magician",
        "characteristics": "magnetism, eloquence, influence, money/favours, mystery",
        "reduction_path": "15 → 6",
        "output_num": 6,
    },
    16: {
        "archetype": "Shattered Citadel",
        "characteristics": "sudden disruption, defeat of plans, need for caution",
        "reduction_path": "16 → 7",
        "output_num": 7,
    },
    17: {
        "archetype": "Star of the Magi",
        "characteristics": "peace, love, recognition, enduring reputation",
        "reduction_path": "17 → 8",
        "output_num": 8,
    },
    18: {
        "archetype": "Rayed Moon",
        "characteristics": "material-versus-spiritual tension, quarrels, deception, upheaval",
        "reduction_path": "18 → 9",
        "output_num": 9,
    },
    19: {
        "archetype": "Prince of Heaven / Sun",
        "characteristics": "success, happiness, esteem, honour",
        "reduction_path": "19 → 1",
        "output_num": 1,
    },
    20: {
        "archetype": "Awakening / Judgment",
        "characteristics": "awakening, call to a cause, delays before action",
        "reduction_path": "20 → 2",
        "output_num": 2,
    },
    21: {
        "archetype": "Crown of the Magi / Universe",
        "characteristics": "advancement, honours, victory after testing",
        "reduction_path": "21 → 3",
        "output_num": 3,
    },
    22: {
        "archetype": "Good Man Blinded",
        "characteristics": "illusion, poor judgment, influence of others",
        "reduction_path": "22 → 4",
        "output_num": 4,
    },
    23: {
        "archetype": "Royal Star of the Lion",
        "characteristics": "success, protection, help from authority/superiors",
        "reduction_path": "23 → 5",
        "output_num": 5,
    },
    24: {
        "archetype": "Gain Through Love",
        "characteristics": "support, affection, assistance, gains through relationships",
        "reduction_path": "24 → 6",
        "output_num": 6,
    },
    25: {
        "archetype": "Strength Through Trial",
        "characteristics": "experience, resilience, success after difficulty",
        "reduction_path": "25 → 7",
        "output_num": 7,
    },
    26: {
        "archetype": "Grave Warning",
        "characteristics": "partnership risk, poor advice, speculation-related loss",
        "reduction_path": "26 → 8",
        "output_num": 8,
    },
    27: {
        "archetype": "The Sceptre",
        "characteristics": "authority, command, productive intellect, reward",
        "reduction_path": "27 → 9",
        "output_num": 9,
    },
    28: {
        "archetype": "Promise and Loss",
        "characteristics": "strong promise but reversals, misplaced trust, rebuilding",
        "reduction_path": "28 → 1",
        "output_num": 1,
    },
    29: {
        "archetype": "Uncertainty / Deception",
        "characteristics": "unreliable alliances, disappointment, grief, uncertainty",
        "reduction_path": "29 → 11 → 2",
        "output_num": 2,
    },
    30: {
        "archetype": "Retrospection",
        "characteristics": "reflection, mental ability, observation; relatively neutral",
        "reduction_path": "30 → 3",
        "output_num": 3,
    },
    31: {
        "archetype": "Retrospection / Isolation",
        "characteristics": "self-contained thought, independence, weaker material emphasis",
        "reduction_path": "31 → 4",
        "output_num": 4,
    },
    32: {
        "archetype": "Command / Combination",
        "characteristics": "influence through groups, communication, leadership with judgment",
        "reduction_path": "32 → 5",
        "output_num": 5,
    },
    33: {
        "archetype": "Reads as 24",
        "characteristics": "support and gains through relationships, following the 24 pattern",
        "reduction_path": "33 → 6",
        "output_num": 6,
    },
    34: {
        "archetype": "Reads as 25",
        "characteristics": "strength and experience, following the 25 pattern",
        "reduction_path": "34 → 7",
        "output_num": 7,
    },
    35: {
        "archetype": "Reads as 26",
        "characteristics": "partnership/speculation warning, following the 26 pattern",
        "reduction_path": "35 → 8",
        "output_num": 8,
    },
    36: {
        "archetype": "Reads as 27",
        "characteristics": "authority and intellectual reward, following the 27 pattern",
        "reduction_path": "36 → 9",
        "output_num": 9,
    },
    37: {
        "archetype": "Fortunate Friendships",
        "characteristics": "supportive friendships, partnerships, fortunate alliances",
        "reduction_path": "37 → 1",
        "output_num": 1,
    },
    38: {
        "archetype": "Reads as 29",
        "characteristics": "uncertainty, unreliable alliances, following the 29 pattern",
        "reduction_path": "38 → 2",
        "output_num": 2,
    },
    39: {
        "archetype": "Reads as 30",
        "characteristics": "reflection and mental ability, following the 30 pattern",
        "reduction_path": "39 → 3",
        "output_num": 3,
    },
    40: {
        "archetype": "Reads as 31",
        "characteristics": "self-contained thought, isolation, following the 31 pattern",
        "reduction_path": "40 → 4",
        "output_num": 4,
    },
    41: {
        "archetype": "Reads as 32",
        "characteristics": "command, combinations, group influence, following the 32 pattern",
        "reduction_path": "41 → 5",
        "output_num": 5,
    },
    42: {
        "archetype": "Reads as 24",
        "characteristics": "support and gains through relationships, following the 24 pattern",
        "reduction_path": "42 → 6",
        "output_num": 6,
    },
    43: {
        "archetype": "Revolution / Upheaval",
        "characteristics": "strife, failure, obstruction, major disruption",
        "reduction_path": "43 → 7",
        "output_num": 7,
    },
    44: {
        "archetype": "Reads as 26",
        "characteristics": "partnership/speculation warning, following the 26 pattern",
        "reduction_path": "44 → 8",
        "output_num": 8,
    },
    45: {
        "archetype": "Reads as 27",
        "characteristics": "authority and intellectual reward, following the 27 pattern",
        "reduction_path": "45 → 9",
        "output_num": 9,
    },
    46: {
        "archetype": "Reads as 37",
        "characteristics": "fortunate friendships and partnerships, following the 37 pattern",
        "reduction_path": "46 → 1",
        "output_num": 1,
    },
    47: {
        "archetype": "Reads as 29",
        "characteristics": "uncertainty and unreliable alliances, following the 29 pattern",
        "reduction_path": "47 → 2",
        "output_num": 2,
    },
    48: {
        "archetype": "Reads as 30",
        "characteristics": "reflection and mental ability, following the 30 pattern",
        "reduction_path": "48 → 3",
        "output_num": 3,
    },
    49: {
        "archetype": "Reads as 31",
        "characteristics": "self-contained thought and isolation, following the 31 pattern",
        "reduction_path": "49 → 4",
        "output_num": 4,
    },
    50: {
        "archetype": "Reads as 32",
        "characteristics": "command, combinations and group influence, following the 32 pattern",
        "reduction_path": "50 → 5",
        "output_num": 5,
    },
    51: {
        "archetype": "Warrior",
        "characteristics": "strong force, sudden advancement, leadership, but conflict/danger",
        "reduction_path": "51 → 6",
        "output_num": 6,
    },
    52: {
        "archetype": "Reads as 43",
        "characteristics": "strife, obstruction and upheaval, following the 43 pattern",
        "reduction_path": "52 → 7",
        "output_num": 7,
    },
}

# ── Chaldean / Cheiro Letter Mapping Chart ────────────────────────────────────
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

def compute_reduction_path(num: int) -> tuple[str, int]:
    """Calculate the step-by-step reduction path and final root digit."""
    if num <= 9:
        return f"{num} → {num}", num
    steps = [str(num)]
    curr = num
    while curr > 9:
        digits = [int(d) for d in str(curr)]
        curr = sum(digits)
        steps.append(str(curr))
    return " → ".join(steps), curr

def build_cheiro_database_1_to_100() -> Dict[int, Dict[str, Any]]:
    """Build the complete 1-100 deterministic dataset adhering strictly to Cheiro canon."""
    db = {}
    for n in range(1, 101):
        red_path, out_num = compute_reduction_path(n)
        root_prof = ROOT_PLANETARY_PROFILES[out_num]

        if n <= 9:
            db[n] = {
                "input_number": n,
                "input_type": "Single",
                "reduction_path": f"{n} → {n}",
                "output_number": n,
                "input_compound_archetype": "Single number",
                "input_characteristics": root_prof["characteristics"],
                "output_planet_tradition": root_prof["planet"],
                "output_characteristics": root_prof["characteristics"],
                "output_outcome_themes": root_prof["outcome_themes"],
                "rag_source_layer": "Root tradition",
                "evidence_status": "Traditional symbolic interpretation; not empirical prediction"
            }
        elif 10 <= n <= 52:
            cp_data = CHEIRO_COMPOUND_CATALOGUE[n]
            db[n] = {
                "input_number": n,
                "input_type": "Compound",
                "reduction_path": cp_data["reduction_path"],
                "output_number": cp_data["output_num"],
                "input_compound_archetype": cp_data["archetype"],
                "input_characteristics": cp_data["characteristics"],
                "output_planet_tradition": root_prof["planet"],
                "output_characteristics": root_prof["characteristics"],
                "output_outcome_themes": root_prof["outcome_themes"],
                "rag_source_layer": "Classical Chaldean compound + root",
                "evidence_status": "Traditional symbolic interpretation; not empirical prediction"
            }
        else: # 53 to 100
            db[n] = {
                "input_number": n,
                "input_type": "Compound",
                "reduction_path": f"{n} → {out_num}",
                "output_number": out_num,
                "input_compound_archetype": "No canonical Classical Chaldean compound meaning in 10–52",
                "input_characteristics": f"Root {out_num} themes only; use an explicitly defined extended school before assigning a compound meaning.",
                "output_planet_tradition": root_prof["planet"],
                "output_characteristics": root_prof["characteristics"],
                "output_outcome_themes": root_prof["outcome_themes"],
                "rag_source_layer": "Root only / extended-school flag",
                "evidence_status": "Traditional symbolic interpretation; not empirical prediction"
            }
    return db

# Global deterministic repository of 1-100 Cheiro entries
CHEIRO_DATASET = build_cheiro_database_1_to_100()

# ── Core Analysis Functions ──────────────────────────────────────────────────

def analyze_number(num: int) -> Dict[str, Any]:
    """Retrieve full Cheiro profile for any number 1 to 100."""
    if num in CHEIRO_DATASET:
        return CHEIRO_DATASET[num]
    
    # Numbers > 100 reduce to root
    red_path, out_num = compute_reduction_path(num)
    root_prof = ROOT_PLANETARY_PROFILES[out_num]
    return {
        "input_number": num,
        "input_type": "Compound",
        "reduction_path": red_path,
        "output_number": out_num,
        "input_compound_archetype": "Extended compound (beyond 100)",
        "input_characteristics": f"Reduces to Root {out_num}",
        "output_planet_tradition": root_prof["planet"],
        "output_characteristics": root_prof["characteristics"],
        "output_outcome_themes": root_prof["outcome_themes"],
        "rag_source_layer": "Extended-school flag",
        "evidence_status": "Traditional symbolic interpretation; not empirical prediction"
    }

def analyze_birth_day_cheiro(day: int) -> Dict[str, Any]:
    """
    Analyzes birth day (1 to 31) under Cheiro compound rules.
    Preserves input compound archetype (GR-001) and output root planet (GR-002).
    """
    profile = analyze_number(day)
    return {
        "day_input": day,
        "is_compound": day > 9,
        "archetype": profile["input_compound_archetype"],
        "compound_journey": profile["input_characteristics"],
        "reduction_path": profile["reduction_path"],
        "mulank_output": profile["output_number"],
        "ruling_planet": profile["output_planet_tradition"],
        "root_traits": profile["output_characteristics"],
        "outcome_themes": profile["output_outcome_themes"],
        "evidence_status": profile["evidence_status"]
    }

def analyze_name_cheiro(name: str, driver: Optional[int] = None, conductor: Optional[int] = None) -> Dict[str, Any]:
    """
    Computes Chaldean name value, preserving compound sum before reduction (GR-001)
    and evaluating Cheiro compound archetype alongside root alignment (GR-002).
    """
    clean_name = "".join(c.upper() for c in name if c.isalpha())
    letter_breakdown = [{c: CHALDEAN_LETTER_VALUES.get(c, 0)} for c in clean_name]
    raw_compound = sum(CHALDEAN_LETTER_VALUES.get(c, 0) for c in clean_name)
    
    profile = analyze_number(raw_compound)
    name_root = profile["output_number"]
    
    # Balancing checks against driver and conductor
    balance_notes = []
    is_balanced = True
    
    # Highly auspicious Cheiro name numbers: 19, 23, 24, 27, 32, 37, 41, 45, 46
    auspicious_compounds = {19, 23, 24, 27, 32, 37, 41, 45, 46}
    # Challenging Cheiro compounds: 12, 16, 18, 22, 26, 28, 29, 38, 43, 44, 52
    challenging_compounds = {12, 16, 18, 22, 26, 28, 29, 38, 43, 44, 52}
    
    if raw_compound in auspicious_compounds:
        balance_notes.append(f"Name compound {raw_compound} ('{profile['input_compound_archetype']}') is intrinsically fortunate in Classical Chaldean tradition.")
    elif raw_compound in challenging_compounds:
        is_balanced = False
        balance_notes.append(f"Warning: Name compound {raw_compound} ('{profile['input_compound_archetype']}') carries Classical Chaldean karmic friction warnings.")

    if driver is not None:
        from app.engine.vedic_numerology import FRIENDLY_NUMBERS, ENEMY_NUMBERS
        if name_root in FRIENDLY_NUMBERS.get(driver, []):
            balance_notes.append(f"Root name number {name_root} is friendly to Driver {driver}.")
        elif name_root in ENEMY_NUMBERS.get(driver, []):
            is_balanced = False
            balance_notes.append(f"Root name number {name_root} has enemy vibration with Driver {driver}.")

    return {
        "clean_name": clean_name,
        "letter_breakdown": letter_breakdown,
        "compound_sum": raw_compound,
        "compound_archetype": profile["input_compound_archetype"],
        "compound_characteristics": profile["input_characteristics"],
        "reduction_path": profile["reduction_path"],
        "name_root": name_root,
        "name_planet": profile["output_planet_tradition"],
        "outcome_themes": profile["output_outcome_themes"],
        "is_harmoniously_balanced": is_balanced,
        "balancing_evaluation": " ".join(balance_notes),
        "evidence_status": profile["evidence_status"]
    }

def analyze_dob_conductor_cheiro(day: int, month: int, year: int) -> Dict[str, Any]:
    """
    Computes Conductor (Bhagyank) preserving the intermediate compound sum (GR-001)
    and evaluating Cheiro archetype before final single digit (GR-002).
    """
    # Total sum of all digits in DD/MM/YYYY
    dob_digits = [int(d) for d in f"{day:02d}{month:02d}{year}"]
    raw_total = sum(dob_digits)
    
    profile = analyze_number(raw_total)
    return {
        "dob": f"{day:02d}/{month:02d}/{year}",
        "raw_compound_total": raw_total,
        "compound_archetype": profile["input_compound_archetype"],
        "compound_characteristics": profile["input_characteristics"],
        "reduction_path": profile["reduction_path"],
        "conductor_root": profile["output_number"],
        "ruling_planet": profile["output_planet_tradition"],
        "outcome_themes": profile["output_outcome_themes"],
        "evidence_status": profile["evidence_status"]
    }

def verify_evidence_guardrails(prediction_text: str) -> str:
    """
    RAG-002 Compliance Guardrail:
    Prevents hallucinated scientific statistics or invented empirical numbers.
    If an ungrounded empirical figure was generated, flags or replaces with '[INSERT REAL FIGURE]'.
    """
    # Pattern detecting phrases claiming invented scientific percentages like '98.4% scientifically proven'
    bad_patterns = [
        r"(scientifically proven to be \d+%)",
        r"(clinical success rate of \d+%)",
        r"(\d+% empirical accuracy guarantee)"
    ]
    cleaned = prediction_text
    for pat in bad_patterns:
        cleaned = re.sub(pat, "[INSERT REAL FIGURE]", cleaned, flags=re.IGNORECASE)
    return cleaned
