"""
app/engine/indications_engine.py
================================
Additive Deterministic Reasoning, Neighbour Relations (Layers 2 & 3),
4-Step Remedies, 2027 Month-by-Month Care Guide, and Section 19 Server-Side
Affirmation & Manifestation Entitlement Engine.

GOVERNING RULES (Sections 0, 2, 14, 15, 16, 18C, 19):
- Reuses existing calculation, element balancing, and planet repetition modules
  without modifying or replacing any Layer 1 output.
- Guarded behind `NV_ENABLE_LAYERS_2_3` (default OFF / "0").
- Only `APPROVED` library entries render when `ENVIRONMENT == "production"`.
- Never infers religion from name, language, or location.
"""

import calendar
import hashlib
import json
import os
from datetime import date
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from app.engine.charm_oracle_synthesizer import classify_digit_degree
from app.engine.core_matrix_engine import (
    analyze_elements_balancing,
    analyze_repeat_numbers,
    assess_karmic_and_master,
    calculate_chaldean_name,
)
from app.engine.digit_root import (
    LO_SHU_EIGHT_PLANES,
    PLANET_MAP_1_TO_9,
    calc_bhagyank,
    calc_compound_steps,
    calc_driver,
    calc_loshu_dob_only,
    calc_personal_day,
    calc_personal_month,
    calc_personal_year,
    sum_digits_str,
)
from app.engine.indication_schema_and_loader import (
    load_indication_library,
    load_neighbour_relations,
    load_remedy_library,
)
from app.engine.indication_validator import (
    DEFAULT_FOOTER,
    HEALTH_SAFETY_LINE,
    PHILOSOPHY_LINE,
    REMEDY_EFFORT_LINE,
    detect_event_prediction_question,
    soften_shadow_text,
)
from app.engine.kua import calculate_kua_details
from app.engine.layer1_golden_snapshot import extract_ranked_5_element_remedies
from app.engine.rule_governance import rule_governance

# Exact 20 adjacent horizontal, vertical, and diagonal pairs on 4 9 2 / 3 5 7 / 8 1 6 (Section 4 & 14.B)
LO_SHU_20_NEIGHBOUR_PAIRS: Tuple[Tuple[int, int, str], ...] = (
    # Across (6)
    (4, 9, "across"),
    (9, 2, "across"),
    (3, 5, "across"),
    (5, 7, "across"),
    (8, 1, "across"),
    (1, 6, "across"),
    # Down (6)
    (4, 3, "down"),
    (3, 8, "down"),
    (9, 5, "down"),
    (5, 1, "down"),
    (2, 7, "down"),
    (7, 6, "down"),
    # Diagonal (8)
    (4, 5, "diagonal"),
    (2, 5, "diagonal"),
    (8, 5, "diagonal"),
    (6, 5, "diagonal"),
    (9, 3, "diagonal"),
    (9, 7, "diagonal"),
    (1, 3, "diagonal"),
    (1, 7, "diagonal"),
)

# Adjacency map per cell (1..9) derived directly from the 20 neighbour pairs
CELL_NEIGHBOURS: Dict[int, Tuple[int, ...]] = {
    d: tuple(
        sorted(
            {
                (b if a == d else a)
                for a, b, _ in LO_SHU_20_NEIGHBOUR_PAIRS
                if a == d or b == d
            }
        )
    )
    for d in range(1, 10)
}

ELEMENT_DIGITS: Dict[str, Tuple[int, ...]] = {
    "Wood": (3, 4),
    "Fire": (9,),
    "Earth": (2, 5, 8),
    "Metal": (6, 7),
    "Water": (1,),
}

DIGIT_TO_ELEMENT: Dict[int, str] = {
    1: "Water",
    2: "Earth",
    3: "Wood",
    4: "Wood",
    5: "Earth",
    6: "Metal",
    7: "Metal",
    8: "Earth",
    9: "Fire",
}

PLANET_CHARACTER_MODIFIERS: Dict[int, Dict[str, str]] = {
    1: {
        "planet": "Sun",
        "sanskrit": "Surya",
        "character": "strong, clear-headed and, traditionally, steadying when circumstances are demanding",
        "high_repeat_ lean": "benefic_protective_with_control_watch",
        "growth_edge": "A tendency to carry too much alone or to resist advice",
        "strength": "Leadership, clarity and steadying presence",
        "practical_step": "Practise listen-first routines, early morning sunlight and one weekly day to delegate.",
    },
    2: {
        "planet": "Moon",
        "sanskrit": "Chandra",
        "character": "sensitive, cooperative and emotionally perceptive",
        "high_repeat_lean": "sensitive_overthinking_watch",
        "growth_edge": "A tendency to absorb others' moods or hesitate when feelings run high",
        "strength": "Empathy, diplomacy and calm care",
        "practical_step": "Keep a regular sleep schedule and pause before replying in sensitive conversations.",
    },
    3: {
        "planet": "Jupiter",
        "sanskrit": "Guru",
        "character": "wise, principle-led and oriented toward learning and counsel",
        "high_repeat_lean": "benefic_counsel_with_overcommitment_watch",
        "growth_edge": "A tendency to take on too many advisory commitments or sound overly firm",
        "strength": "Wisdom, structured thinking and mentorship",
        "practical_step": "Keep ten minutes of daily study and align commitments with written priorities.",
    },
    4: {
        "planet": "Rahu",
        "sanskrit": "Rahu (North Node)",
        "character": "structured, unconventional and intense when repeated",
        "high_repeat_lean": "malefic_intense_when_repeated",
        "growth_edge": "A pull toward rigid systems or sudden shifts in plans under pressure",
        "strength": "Practical problem-solving, order and technical focus",
        "practical_step": "Declutter one space each week and keep paperwork and commitments neatly documented.",
    },
    5: {
        "planet": "Mercury",
        "sanskrit": "Budh",
        "character": "adaptable, communicative and central to grid balance",
        "high_repeat_lean": "restless_pacing_watch",
        "growth_edge": "A tendency toward mental restlessness or switching priorities too quickly",
        "strength": "Adaptability, clear communication and commercial agility",
        "practical_step": "Write down key decisions and practise five minutes of slow breathing daily.",
    },
    6: {
        "planet": "Venus",
        "sanskrit": "Shukra",
        "character": "warm, family-minded and appreciative of harmony and comfort",
        "high_repeat_lean": "benefic_harmony_with_overgiving_watch",
        "growth_edge": "A tendency to over-extend for others' comfort or spend impulsively on ease",
        "strength": "Warmth, stewardship and relationship care",
        "practical_step": "Balance care for family with clear household budgets and personal rest.",
    },
    7: {
        "planet": "Ketu",
        "sanskrit": "Ketu (South Node)",
        "character": "introspective, analytical and intense when repeated",
        "high_repeat_lean": "malefic_intense_when_repeated",
        "growth_edge": "A wish to step back into quiet isolation or over-analyse relationships",
        "strength": "Deep research, intuition and calm discernment",
        "practical_step": "Take ten minutes of screen-free quiet daily while staying warmly connected with loved ones.",
    },
    8: {
        "planet": "Saturn",
        "sanskrit": "Shani",
        "character": "heavy, slow, accountable and enduring when repeated",
        "high_repeat_lean": "malefic_heavy_when_repeated",
        "growth_edge": "A tendency toward heavy self-pressure, slow pacing or carrying work without rest",
        "strength": "Endurance, fairness and long-term discipline",
        "practical_step": "Keep a fixed daily routine, finish one small task without delay, and protect scheduled rest.",
    },
    9: {
        "planet": "Mars",
        "sanskrit": "Mangal",
        "character": "energetic, courageous and quick-moving when repeated",
        "high_repeat_lean": "malefic_fiery_when_repeated",
        "growth_edge": "A short fuse under pressure and needs care with haste and safety",
        "strength": "Courage, initiative and decisive follow-through",
        "practical_step": "Channel energy through regular exercise and slow down deliberately during travel and debates.",
    },
}

MONTH_NAMES_1_TO_12: Tuple[str, ...] = tuple(calendar.month_name[1:13])


def is_layers_2_3_enabled(explicit_flag: Optional[bool] = None) -> bool:
    """Feature gate for additive Layers 2 & 3, Indication Cards, Care Guide & Section 19 blocks."""
    if explicit_flag is not None:
        return bool(explicit_flag)
    val = (os.getenv("NV_ENABLE_LAYERS_2_3") or "0").strip().lower()
    return val in {"1", "true", "yes", "on"}


def format_planet_term(digit: int, edition: str = "india") -> str:
    """Applies geo terminology rule: India = Indian term first; International = Western term first."""
    meta = PLANET_MAP_1_TO_9[digit]
    if str(edition or "india").lower() == "international":
        return meta["international"]
    return meta["india"]


def detect_commanding_planet(
    counts: Dict[int, int],
    *,
    min_top_count: int = 4,
    max_other_count: int = 2,
) -> Dict[str, Any]:
    """
    Section 3.3 & Section 16.B.3 Commanding-Planet Detector (DOB digits only):
    Default rule: `top_count >= 4` and `all other digits <= 2`; ties are co-commanders.
    """
    if not counts:
        return {"has_commander": False, "commanders": [], "top_count": 0, "others_max": 0}
    top_count = max(counts.values())
    if top_count < min_top_count:
        return {"has_commander": False, "commanders": [], "top_count": top_count, "others_max": top_count}

    leaders = sorted([d for d, c in counts.items() if c == top_count])
    others_max = max([c for d, c in counts.items() if d not in leaders], default=0)
    if others_max > max_other_count:
        return {
            "has_commander": False,
            "commanders": [],
            "top_count": top_count,
            "others_max": others_max,
        }

    commander_details = []
    for d in leaders:
        mod = PLANET_CHARACTER_MODIFIERS[d]
        benefic_lean = d in (1, 3, 5, 6)
        malefic_lean = d in (4, 7, 8, 9) or top_count >= 4
        commander_details.append(
            {
                "digit": d,
                "count": top_count,
                "planet": mod["planet"],
                "sanskrit": mod["sanskrit"],
                "benefic_lean": benefic_lean,
                "malefic_lean": malefic_lean,
                "character_note": mod["character"],
                "growth_edge": mod["growth_edge"],
                "strength": mod["strength"],
                "practical_step": mod["practical_step"],
            }
        )

    return {
        "has_commander": True,
        "is_co_commanders": len(leaders) > 1,
        "commanders": commander_details,
        "top_count": top_count,
        "others_max": others_max,
    }


def classify_reference_repetition_stage(digit: int, count: int) -> str:
    """Section 3.4 & 16.B.4 canonical reference stage label alongside existing outputs."""
    if count <= 0:
        return "missing"
    if count == 1:
        return "baseline"
    if count == 2:
        return "strong_and_balanced"
    if count == 3:
        return "turning_point"
    if count in (4, 5):
        return "high"
    return "extreme"


def evaluate_neighbour_relations_layer2_and_3(
    counts: Dict[int, int],
    missing_digits: Sequence[int],
    element_audit: Dict[str, Any],
    neighbour_config: Optional[Dict[str, Any]] = None,
    *,
    allow_draft: bool = True,
) -> Dict[str, Any]:
    """
    Evaluates:
      - Layer 2: Only the 20 adjacent Lo Shu pairs where BOTH digits are present in `counts`.
        Uses ONLY supplied `ordered_relations` (`A->B` and `B->A`).
        Combining rule: both `friendly` -> `supportive`; any `enemy` -> `tension`;
        otherwise -> `balanced or one-sided support`.
      - Layer 3: Combined gap-neighbour reading for every missing digit and every element gap
        from Layer 1, without altering Layer 1 counts or ranked element remedies.
    """
    cfg = neighbour_config if neighbour_config is not None else load_neighbour_relations()
    status = cfg.get("status", "UNCONFIGURED_AWAITING_OWNER_TABLE")
    ordered_rels: Dict[str, str] = cfg.get("ordered_relations", {}) or {}
    pair_meanings: Dict[str, Dict[str, str]] = cfg.get("pair_meanings", {}) or {}

    if not allow_draft and status != "APPROVED":
        ordered_rels = {}
        pair_meanings = {}

    active_pairs: List[Dict[str, Any]] = []
    for a, b, direction_kind in LO_SHU_20_NEIGHBOUR_PAIRS:
        if counts.get(a, 0) > 0 and counts.get(b, 0) > 0:
            ab = ordered_rels.get(f"{a}->{b}")
            ba = ordered_rels.get(f"{b}->{a}")
            canon_key = f"{min(a, b)}-{max(a, b)}"
            meaning = pair_meanings.get(canon_key) or pair_meanings.get(f"{a}-{b}") or {}

            if ab and ba:
                if ab == "friendly" and ba == "friendly":
                    combined = "supportive"
                elif ab == "enemy" or ba == "enemy":
                    combined = "tension"
                else:
                    combined = "balanced or one-sided support"
                configured = True
            else:
                combined = "unconfigured"
                configured = False

            rec: Dict[str, Any] = {
                "pair": f"{a}-{b}",
                "digits": [a, b],
                "adjacency": direction_kind,
                "configured": configured,
                "a_to_b": ab,
                "b_to_a": ba,
                "combined_relation": combined,
                "fact_id": f"L2:neighbour:{a}_{b}:{combined}",
            }
            if meaning.get("positive"):
                rec["positive"] = meaning["positive"]
            if meaning.get("shadow"):
                rec["shadow"] = meaning["shadow"]
            active_pairs.append(rec)

    # Layer 3: Combined Gap-Neighbour Reading (never modifies Layer 1)
    missing_gap_readings: List[Dict[str, Any]] = []
    for m_dig in missing_digits:
        adj_present = [nb for nb in CELL_NEIGHBOURS[m_dig] if counts.get(nb, 0) > 0]
        supporting: List[int] = []
        tension_against: List[int] = []
        neutral_or_mixed: List[int] = []
        unconfigured_neighbours: List[int] = []

        for nb in adj_present:
            rel_nb_to_gap = ordered_rels.get(f"{nb}->{m_dig}")
            rel_gap_to_nb = ordered_rels.get(f"{m_dig}->{nb}")
            if rel_nb_to_gap is None and rel_gap_to_nb is None:
                unconfigured_neighbours.append(nb)
            elif rel_nb_to_gap == "enemy" or rel_gap_to_nb == "enemy":
                tension_against.append(nb)
            elif rel_nb_to_gap == "friendly" and (rel_gap_to_nb in ("friendly", None)):
                supporting.append(nb)
            else:
                neutral_or_mixed.append(nb)

        missing_gap_readings.append(
            {
                "missing_digit": m_dig,
                "planet": PLANET_MAP_1_TO_9[m_dig]["english"],
                "element": DIGIT_TO_ELEMENT[m_dig],
                "present_adjacent_neighbours": adj_present,
                "supporting_neighbours": supporting,
                "tension_neighbours": tension_against,
                "neutral_neighbours": neutral_or_mixed,
                "unconfigured_neighbours": unconfigured_neighbours,
                "evidence_ids": [f"L1:missing_digit:{m_dig}"]
                + [f"L2:adj_present:{nb}->{m_dig}" for nb in adj_present],
            }
        )

    element_gap_readings: List[Dict[str, Any]] = []
    for elem_name, elem_digits in ELEMENT_DIGITS.items():
        elem_info = element_audit.get("audit", {}).get(elem_name, {})
        is_gap = any(d in missing_digits for d in elem_digits) or elem_info.get("count", 0) == 0
        if is_gap:
            adj_set: Set[int] = set()
            for ed in elem_digits:
                for nb in CELL_NEIGHBOURS[ed]:
                    if nb not in elem_digits and counts.get(nb, 0) > 0:
                        adj_set.add(nb)
            element_gap_readings.append(
                {
                    "element": elem_name,
                    "layer1_status": elem_info.get("status", "Missing (0)"),
                    "missing_digits_in_element": [d for d in elem_digits if d in missing_digits],
                    "present_surrounding_digits": sorted(adj_set),
                    "evidence_ids": [f"L1:element_gap:{elem_name}"]
                    + [f"L2:surrounding_present:{nb}" for nb in sorted(adj_set)],
                }
            )

    return {
        "layer_2_neighbour_relations": {
            "table_status": status if (allow_draft or status == "APPROVED") else "UNCONFIGURED_PRODUCTION",
            "active_present_pairs_count": len(active_pairs),
            "configured_pairs_count": sum(1 for p in active_pairs if p["configured"]),
            "pairs": active_pairs,
        },
        "layer_3_combined_gap_neighbour_reading": {
            "missing_digit_context": missing_gap_readings,
            "element_gap_context": element_gap_readings,
        },
    }


def _select_library_entry(
    entries_by_sig: Dict[str, List[Dict[str, Any]]],
    signature: str,
    *,
    allow_draft: bool,
) -> Optional[Dict[str, Any]]:
    candidates = entries_by_sig.get(signature, [])
    for c in candidates:
        if c.get("status") == "APPROVED" or (allow_draft and c.get("status") == "DRAFT"):
            return c
    return None


def _resolve_allowed_styles(edition: str = "india", user_remedy_style: Optional[str] = None) -> List[str]:
    """
    Never infers religion from name, language, or location.
    Uses explicit `user_remedy_style` when chosen; otherwise edition defaults per Section 18C:
      - India edition: `["vedic", "universal", "western"]`
      - International edition: `["universal", "western"]`
    """
    if user_remedy_style:
        s = user_remedy_style.strip().lower()
        if s in {"vedic", "universal", "western"}:
            return [s, "universal"] if s != "universal" else ["universal"]
    if str(edition or "india").lower() == "international":
        return ["universal", "western"]
    return ["vedic", "universal", "western"]


def format_planet_remedy_pack(
    planet_num: int,
    remedy_lib: Dict[str, Any],
    *,
    tier: str = "advanced",
    edition: str = "india",
    user_remedy_style: Optional[str] = None,
    allow_draft: bool = True,
) -> Optional[Dict[str, Any]]:
    """
    Formats a single planet remedy pack from `app/data/remedy_library.json`:
    - Respects `APPROVED` vs `DRAFT`.
    - Filters items by `allowed_styles`.
    - Never includes mantras or gemstones in `basic` or `free`.
    - Formats gemstones as `"traditionally associated, optional"` + gentle alternatives +
      strong-stone practitioner caution (`blue sapphire`, `cat's eye`, `hessonite`).
    """
    top_status = remedy_lib.get("meta", {}).get("status", "DRAFT")
    raw_planets = remedy_lib.get("planets", [])
    by_num = (
        {int(p["number"]): p for p in raw_planets}
        if isinstance(raw_planets, list)
        else {int(k): v for k, v in raw_planets.items()}
    )
    pack = by_num.get(planet_num)
    if not pack:
        return None
    p_status = pack.get("status", top_status)
    if not allow_draft and p_status != "APPROVED":
        return None

    is_basic_or_free = str(tier).lower() in {"free", "basic", "report_basic"}
    allowed_styles = set(_resolve_allowed_styles(edition, user_remedy_style))

    selected_items: List[Dict[str, str]] = []
    touches_health_safety = planet_num == 9
    for item in pack.get("items", []):
        kind = item.get("kind", "habit")
        if is_basic_or_free and kind in {"mantra", "vedic_practice"}:
            continue
        item_styles = set(item.get("styles", []))
        if not (item_styles & allowed_styles):
            continue
        selected_items.append({"id": item["id"], "kind": kind, "text": item["text"]})
        low = item["text"].lower()
        if any(w in low for w in ("blood bank", "seatbelt", "helmet", "health check-up", "hospital")):
            touches_health_safety = True

    gemstone_block: Optional[Dict[str, Any]] = None
    gem = pack.get("gemstone")
    if not is_basic_or_free and isinstance(gem, dict):
        trad = gem.get("traditional", "")
        alts = gem.get("gentle_alternatives", [])
        caution = gem.get("extra_caution")
        note = f"{trad} (traditionally associated, optional; gentle alternatives: {', '.join(alts)})."
        if caution:
            note = f"{note} {caution}"
        gemstone_block = {
            "traditional": trad,
            "gentle_alternatives": alts,
            "caution": caution,
            "display_note": note,
        }

    return {
        "planet_number": planet_num,
        "planet": pack.get("planet", PLANET_MAP_1_TO_9[planet_num]["english"]),
        "day": pack.get("day", ""),
        "colours": pack.get("colours", []),
        "items": selected_items,
        "gemstone_info": gemstone_block,
        "affirmation": pack.get("affirmation", ""),
        "touches_health_or_safety": touches_health_safety,
        "health_safety_line": HEALTH_SAFETY_LINE if touches_health_safety else None,
        "effort_line": REMEDY_EFFORT_LINE,
        "status": p_status,
    }


def build_2027_care_guide(
    day: int,
    month: int,
    target_year: int,
    missing_digits: Sequence[int],
    commanders: Sequence[Dict[str, Any]],
    entries_by_sig: Dict[str, List[Dict[str, Any]]],
    remedy_lib: Dict[str, Any],
    *,
    edition: str = "india",
    tier: str = "advanced",
    user_remedy_style: Optional[str] = None,
    allow_draft: bool = True,
) -> Dict[str, Any]:
    """
    Section 7: 2027 Month-by-Month Care Guide per DOB.
    Computes Personal Year and all 12 Personal Months, attaches care areas,
    previous-month `start_before` note, logic links (`gap_meets_cycle`,
    `commanding_planet_meets_cycle`), matching planet remedy pack, and Indication Card.
    """
    py = calc_personal_year(day, month, target_year)
    ed_key = "international" if str(edition).lower() == "international" else "india"
    commander_digits = {c["digit"] for c in commanders}
    missing_set = set(missing_digits)

    months_out: List[Dict[str, Any]] = []
    for m_idx in range(1, 13):
        pm = calc_personal_month(py, m_idx)
        m_name = MONTH_NAMES_1_TO_12[m_idx - 1]
        prev_month_name = MONTH_NAMES_1_TO_12[11] if m_idx == 1 else MONTH_NAMES_1_TO_12[m_idx - 2]
        prev_year_suffix = f" {target_year - 1}" if m_idx == 1 else ""
        start_before = f"Start before: {prev_month_name}{prev_year_suffix}"

        is_gap_meets_cycle = pm in missing_set
        is_cmd_meets_cycle = pm in commander_digits
        is_demanding_planet = pm in (4, 8, 9, 7)
        needs_extra_care = is_gap_meets_cycle or is_cmd_meets_cycle or pm in (4, 8, 9)

        sig = f"gap_meets_cycle:{pm}" if is_gap_meets_cycle else f"personal_month:{pm}"
        entry = _select_library_entry(entries_by_sig, sig, allow_draft=allow_draft)
        if entry is None:
            entry = _select_library_entry(entries_by_sig, f"personal_month:{pm}", allow_draft=allow_draft)

        evidence_ids = [
            f"cycle:py_{target_year}:{py}",
            f"cycle:pm_{target_year}_{m_idx:02d}:{pm}",
        ]
        if is_gap_meets_cycle:
            evidence_ids.append(f"link:gap_meets_cycle:{pm}")
            evidence_ids.append(f"loshu:missing:{pm}")
        if is_cmd_meets_cycle:
            evidence_ids.append(f"link:commanding_planet_meets_cycle:{pm}")

        planet_label = format_planet_term(pm, edition)
        rem_pack = (
            None
            if str(tier).lower() in {"free", "basic", "report_basic"}
            else format_planet_remedy_pack(
                pm,
                remedy_lib,
                tier=tier,
                edition=edition,
                user_remedy_style=user_remedy_style,
                allow_draft=allow_draft,
            )
        )

        if entry is not None:
            lv = entry["language_variants"][ed_key]
            care_areas = entry.get("care_areas", ["relationships", "money"])
            why_text = lv["why_this_shows"]
            indicate_text = lv["what_it_may_indicate"]
            mindful_text = lv["be_mindful_of"]
            growth_edge = lv.get("growth_edge") or (
                f"{PLANET_CHARACTER_MODIFIERS[pm]['growth_edge']} when Personal Month {pm} ({PLANET_MAP_1_TO_9[pm]['english']}) is active, "
                f"paired with {PLANET_CHARACTER_MODIFIERS[pm]['strength'].lower()} — begin steady habits in {prev_month_name}."
                if (needs_extra_care or is_demanding_planet)
                else ""
            )
            steps = list(lv["gentle_steps_practical"])
            touches_hs = bool(entry.get("touches_health_or_safety")) or (
                rem_pack is not None and rem_pack.get("touches_health_or_safety", False)
            )
        else:
            care_areas = []
            why_text = ""
            indicate_text = ""
            mindful_text = ""
            growth_edge = ""
            steps = []
            touches_hs = False

        # Attach traditionally suggested practices from remedy pack in Advanced/Premium/Planner
        remedy_lines: List[str] = []
        if rem_pack:
            for it in rem_pack["items"][:4]:
                remedy_lines.append(it["text"])
            if rem_pack.get("gemstone_info"):
                remedy_lines.append(rem_pack["gemstone_info"]["display_note"])

        your_numbers_line = (
            f"Personal Year {py} ({PLANET_MAP_1_TO_9[py]['english']}) · "
            f"{m_name} {target_year} is Personal Month {pm} ({planet_label})"
            + (f" · Digit {pm} is missing from your birth-date grid" if is_gap_meets_cycle else "")
            + (f" · Digit {pm} commands your birth-date grid" if is_cmd_meets_cycle else "")
        )

        month_flags: List[str] = []
        if is_gap_meets_cycle:
            month_flags.append("gap_meets_cycle")
        if is_cmd_meets_cycle:
            month_flags.append("commanding_planet_meets_cycle")

        months_out.append(
            {
                "month_number": m_idx,
                "month_name": m_name,
                "year": target_year,
                "personal_year": py,
                "personal_month": pm,
                "planet_number": pm,
                "planet_label": planet_label,
                "needs_extra_care": needs_extra_care,
                "gap_meets_cycle": is_gap_meets_cycle,
                "commanding_planet_meets_cycle": is_cmd_meets_cycle,
                "flags": month_flags,
                "care_areas": care_areas,
                "start_before": start_before,
                "start_before_month": prev_month_name,
                "evidence_ids": evidence_ids,
                "card": {
                    "title": f"{m_name} {target_year} — Personal Month {pm} ({planet_label})",
                    "your_numbers": your_numbers_line,
                    "why_this_shows": why_text,
                    "what_it_may_indicate": indicate_text,
                    "growth_edge": growth_edge,
                    "be_mindful_of": mindful_text,
                    "gentle_steps": steps,
                    "traditional_practices": remedy_lines,
                    "remedy_effort_line": REMEDY_EFFORT_LINE if (steps or remedy_lines) else "",
                    "health_safety_line": HEALTH_SAFETY_LINE if touches_hs else "",
                    "footer": DEFAULT_FOOTER,
                }
                if entry is not None
                else None,
                "remedy_pack": rem_pack,
            }
        )

    priority_care_months = [m for m in months_out if m["needs_extra_care"] and m["card"] is not None]
    teaser_month = priority_care_months[0] if priority_care_months else (months_out[0] if months_out else None)
    free_teaser = None
    if teaser_month and teaser_month.get("card"):
        free_teaser = {
            "month_number": teaser_month["month_number"],
            "month_name": teaser_month["month_name"],
            "year": target_year,
            "personal_year": py,
            "personal_month": teaser_month["personal_month"],
            "planet_label": teaser_month["planet_label"],
            "care_areas": teaser_month["care_areas"],
            "start_before": teaser_month["start_before"],
            "your_numbers": teaser_month["card"]["your_numbers"],
            "why_this_shows": teaser_month["card"]["why_this_shows"],
            "what_it_may_indicate": teaser_month["card"]["what_it_may_indicate"],
            "growth_edge": teaser_month["card"]["growth_edge"],
            "be_mindful_of": teaser_month["card"]["be_mindful_of"],
            "footer": DEFAULT_FOOTER,
            # Zero remedy text on the free teaser month per Section 7 & 10
        }

    return {
        "year": target_year,
        "personal_year": py,
        "personal_year_planet": format_planet_term(py, edition),
        "months": months_out,
        "priority_care_months": [
            {
                "month_number": m["month_number"],
                "month_name": m["month_name"],
                "personal_month": m["personal_month"],
                "planet_label": m["planet_label"],
                "gap_meets_cycle": m["gap_meets_cycle"],
                "start_before": m["start_before"],
            }
            for m in priority_care_months
        ],
        "free_teaser_month": free_teaser,
    }


PACKAGE_ENTITLEMENT_SPECS: Dict[str, Dict[str, str]] = {
    "free": {"canonical_tier": "free", "affirmation_level": "general", "manifestation_level": "none"},
    "basic": {"canonical_tier": "basic", "affirmation_level": "general", "manifestation_level": "none"},
    "report_basic": {"canonical_tier": "basic", "affirmation_level": "general", "manifestation_level": "none"},
    "advanced": {"canonical_tier": "advanced", "affirmation_level": "personalised", "manifestation_level": "year"},
    "report_advanced": {"canonical_tier": "advanced", "affirmation_level": "personalised", "manifestation_level": "year"},
    "premium": {"canonical_tier": "premium", "affirmation_level": "monthly_personalised", "manifestation_level": "full"},
    "report_premium": {"canonical_tier": "premium", "affirmation_level": "monthly_personalised", "manifestation_level": "full"},
    "planner_2027": {"canonical_tier": "planner_2027", "affirmation_level": "monthly_personalised", "manifestation_level": "full"},
    "year_2027": {"canonical_tier": "planner_2027", "affirmation_level": "monthly_personalised", "manifestation_level": "full"},
    "charm_free": {"canonical_tier": "charm_free", "affirmation_level": "general_on_request", "manifestation_level": "none"},
    "charm_paid": {"canonical_tier": "charm_paid", "affirmation_level": "personalised_topic", "manifestation_level": "current_month"},
    "charm_pass": {"canonical_tier": "charm_paid", "affirmation_level": "personalised_topic", "manifestation_level": "current_month"},
    "charm_premium": {"canonical_tier": "charm_premium", "affirmation_level": "monthly_personalised", "manifestation_level": "full"},
}


def resolve_package_entitlement(tier: Optional[str]) -> Dict[str, str]:
    """Resolves any package/pass identifier to its canonical Section 19 server-side entitlement spec."""
    norm = str(tier or "free").strip().lower()
    return dict(PACKAGE_ENTITLEMENT_SPECS.get(norm, PACKAGE_ENTITLEMENT_SPECS["free"]))


def build_affirmation_and_manifestation(
    *,
    driver: int,
    conductor: int,
    personal_year: int,
    current_personal_month: int,
    commanders: Sequence[Dict[str, Any]],
    missing_digits: Sequence[int],
    care_guide_2027: Dict[str, Any],
    remedy_lib: Dict[str, Any],
    entitlement_tier: str,
    topic: Optional[str] = None,
    requested_on_demand: bool = False,
    allow_draft: bool = True,
) -> Dict[str, Any]:
    """
    Section 19 SERVER-SIDE Entitlement Matrix for Affirmation & Manifestation.
    Entitlement tiers:
      - `free`
      - `basic` / `report_basic`
      - `advanced` / `report_advanced`
      - `premium` / `report_premium`
      - `planner_2027` / `year_2027`
      - `charm_free`
      - `charm_paid`
      - `charm_premium` (Premium or 2027 Planner owner inside Charm AI)
    Never returns blurred or fake paid content; requests above entitlement receive the highest
    allowed version plus an honest plain-language note.
    """
    top_status = remedy_lib.get("meta", {}).get("status", "DRAFT")
    if not allow_draft and top_status != "APPROVED":
        return {
            "entitlement_tier": entitlement_tier,
            "status": "OMITTED_UNAPPROVED_IN_PRODUCTION",
            "affirmation_level": "none",
            "affirmation": None,
            "monthly_affirmations": None,
            "manifestation_level": "none",
            "manifestation": None,
            "upgrade_note": None,
        }

    raw_planets = remedy_lib.get("planets", [])
    planets_by_num = (
        {int(p["number"]): p for p in raw_planets}
        if isinstance(raw_planets, list)
        else {int(k): v for k, v in raw_planets.items()}
    )

    general_affirmation = planets_by_num[driver]["affirmation"]
    py_aff = planets_by_num[personal_year]["affirmation"]
    pm_aff = planets_by_num[current_personal_month]["affirmation"]
    cmd_digit = commanders[0]["digit"] if commanders else None
    key_missing = missing_digits[0] if missing_digits else None

    topic_clean = (topic or "steady personal growth").strip().lower().replace("_", " ")
    personalised_parts = [py_aff]
    if cmd_digit and cmd_digit != personal_year:
        personalised_parts.append(planets_by_num[cmd_digit]["affirmation"])
    elif key_missing and key_missing != personal_year:
        personalised_parts.append(planets_by_num[key_missing]["affirmation"])
    personalised_affirmation = " ".join(personalised_parts)

    # Monthly personalised affirmations (12 months of 2027)
    monthly_affirmations: List[Dict[str, Any]] = []
    monthly_intentions: List[Dict[str, Any]] = []
    for m_obj in care_guide_2027.get("months", []):
        pm_num = m_obj["personal_month"]
        m_name = m_obj["month_name"]
        p_rec = planets_by_num[pm_num]
        themes_str = ", ".join(p_rec.get("themes", [])[:2]) or "steady focus"
        m_aff = f"{p_rec['affirmation']} ({m_name} · Personal Month {pm_num} {p_rec['planet']})"
        monthly_affirmations.append(
            {
                "month_number": m_obj["month_number"],
                "month_name": m_name,
                "personal_month": pm_num,
                "planet": p_rec["planet"],
                "affirmation": m_aff,
            }
        )
        first_habit = p_rec["items"][0]["text"] if p_rec.get("items") else "Keep one steady daily routine."
        monthly_intentions.append(
            {
                "month_number": m_obj["month_number"],
                "month_name": m_name,
                "personal_month": pm_num,
                "care_start_before": m_obj["start_before"],
                "month_intention": f"In {m_name}, I set clear, calm goals around {themes_str} and prepare from {m_obj['start_before_month']}.",
                "weekly_action": first_habit,
                "review_prompt": f"At the end of each week in {m_name}, which small habit helped me stay steady around {themes_str}?",
            }
        )

    py_planet = planets_by_num[personal_year]["planet"]
    py_themes = ", ".join(planets_by_num[personal_year].get("themes", [])[:3])
    year_theme = f"Personal Year {personal_year} ({py_planet}): steady focus on {py_themes}"
    intention_sentence = (
        f"Through Personal Year {personal_year}, I choose consistent daily habits around {py_themes}, "
        f"reviewing my progress calmly without rushing."
    )
    quarterly_focus = [
        {
            "quarter": "Q1 (Jan–Mar)",
            "focus": f"Set clear routines across Personal Months {care_guide_2027['months'][0]['personal_month']}, {care_guide_2027['months'][1]['personal_month']} and {care_guide_2027['months'][2]['personal_month']}.",
        },
        {
            "quarter": "Q2 (Apr–Jun)",
            "focus": f"Pace commitments steadily across Personal Months {care_guide_2027['months'][3]['personal_month']}, {care_guide_2027['months'][4]['personal_month']} and {care_guide_2027['months'][5]['personal_month']}.",
        },
        {
            "quarter": "Q3 (Jul–Sep)",
            "focus": f"Review records and relationships across Personal Months {care_guide_2027['months'][6]['personal_month']}, {care_guide_2027['months'][7]['personal_month']} and {care_guide_2027['months'][8]['personal_month']}.",
        },
        {
            "quarter": "Q4 (Oct–Dec)",
            "focus": f"Consolidate steady habits across Personal Months {care_guide_2027['months'][9]['personal_month']}, {care_guide_2027['months'][10]['personal_month']} and {care_guide_2027['months'][11]['personal_month']}.",
        },
    ]

    pm_planet_rec = planets_by_num[current_personal_month]
    pm_themes = ", ".join(pm_planet_rec.get("themes", [])[:2]) or topic_clean
    current_month_manifestation = {
        "month_theme": f"Personal Month {current_personal_month} ({pm_planet_rec['planet']}): {pm_themes}",
        "month_intention": f"This month, I focus steady effort on {topic_clean} and {pm_themes} one practical step at a time.",
        "weekly_action": pm_planet_rec["items"][0]["text"],
        "review_prompt": f"Which practical choice this week supported calm progress in {topic_clean}?",
    }

    norm = str(entitlement_tier or "free").strip().lower()

    if norm in {"free"}:
        return {
            "entitlement_tier": "free",
            "affirmation_level": "general",
            "affirmation": general_affirmation,
            "monthly_affirmations": None,
            "manifestation_level": "none",
            "manifestation": None,
            "upgrade_note": "A personalised version is included in Anveil My Glowing Charms (Advanced) and Complete Numerology Report.",
        }

    if norm in {"basic", "report_basic"}:
        return {
            "entitlement_tier": "report_basic",
            "affirmation_level": "general",
            "affirmation": general_affirmation,
            "monthly_affirmations": None,
            "manifestation_level": "none",
            "manifestation": None,
            "upgrade_note": "A personalised version is included in Anveil My Glowing Charms (Advanced).",
        }

    if norm in {"advanced", "report_advanced"}:
        return {
            "entitlement_tier": "report_advanced",
            "affirmation_level": "personalised",
            "affirmation": personalised_affirmation,
            "monthly_affirmations": None,
            "manifestation_level": "year",
            "manifestation": {
                "year_theme": year_theme,
                "intention_sentence": intention_sentence,
                "quarterly_focus": quarterly_focus,
            },
            "upgrade_note": "Monthly personalised affirmations and full month-by-month manifestation are included in Complete Numerology Report (32 pages).",
        }

    if norm in {"premium", "report_premium", "planner_2027", "year_2027", "charm_premium"}:
        return {
            "entitlement_tier": norm,
            "affirmation_level": "monthly_personalised",
            "affirmation": personalised_affirmation,
            "monthly_affirmations": monthly_affirmations,
            "manifestation_level": "full",
            "manifestation": {
                "year_theme": year_theme,
                "intention_sentence": intention_sentence,
                "quarterly_focus": quarterly_focus,
                "monthly_intentions": monthly_intentions,
                "weekly_action": monthly_intentions[0]["weekly_action"] if monthly_intentions else "",
                "review_prompt": "Each Sunday evening, note one habit you kept, one area needing calmer pacing next week, and your start-before preparation for the coming month.",
            },
            "upgrade_note": None,
        }

    if norm in {"charm_free"}:
        return {
            "entitlement_tier": "charm_free",
            "affirmation_level": "general" if requested_on_demand else "none",
            "affirmation": general_affirmation if requested_on_demand else None,
            "monthly_affirmations": None,
            "manifestation_level": "none",
            "manifestation": None,
            "upgrade_note": (
                "A personalised version is included in the Charm AI Pass."
                if requested_on_demand
                else None
            ),
        }

    if norm in {"charm_paid", "charm_pass"}:
        topic_aff = f"{pm_aff} {planets_by_num[driver]['affirmation']}"
        return {
            "entitlement_tier": "charm_paid",
            "affirmation_level": "personalised_topic",
            "affirmation": topic_aff,
            "monthly_affirmations": None,
            "manifestation_level": "current_month" if requested_on_demand else "none",
            "manifestation": current_month_manifestation if requested_on_demand else None,
            "upgrade_note": "Full 12-month affirmations and manifestation are included in Complete Numerology Report and the 2027 Year Ahead Planner.",
        }

    # Default safest fallback -> free entitlement
    return {
        "entitlement_tier": "free",
        "affirmation_level": "general",
        "affirmation": general_affirmation,
        "monthly_affirmations": None,
        "manifestation_level": "none",
        "manifestation": None,
        "upgrade_note": "A personalised version is included in Anveil My Glowing Charms (Advanced).",
    }


def build_ordered_remedies(
    *,
    counts: Dict[int, int],
    missing_digits: Sequence[int],
    planes: Dict[str, Any],
    commanders: Sequence[Dict[str, Any]],
    ranked_5_element_remedies: Dict[str, Any],
    care_guide_2027: Dict[str, Any],
    affirmation_manifestation: Dict[str, Any],
    entries_by_sig: Dict[str, List[Dict[str, Any]]],
    remedy_lib: Dict[str, Any],
    tier: str = "advanced",
    edition: str = "india",
    user_remedy_style: Optional[str] = None,
    allow_draft: bool = True,
) -> Dict[str, Any]:
    """
    Fixed-order additive remedies (Sections 6, 15, 16.B.7, 18C & 19):
      1. `step_1_plane_balance`: Incomplete energy plane habits (everyone; habits only in Basic).
      2. `step_2_element_balance`: Existing ranked 5-element balance remedies (unchanged) +
         optional `element_support` extra next to them (never replacing them; no gems in Basic).
      3. `step_3_planet_practices`: Separate labelled block `"Traditionally Suggested Planetary Practices"`
         for malefic-leaning repeated planets (`count >= 3`) and key missing planets.
         Omitted completely (`None`) when nothing applies or unapproved in production — never filler;
         never shown in Basic 3-page PDF.
      4. `step_4_timing_start_before`: Start-before preparation notes from the 2027 Care Guide.
      Plus `manifestation_block` attached from Section 19 server-side entitlement matrix.
    """
    ed_key = "international" if str(edition).lower() == "international" else "india"
    is_basic_or_free = str(tier).lower() in {"free", "basic", "report_basic"}

    # Step 1: Plane-balance practices for incomplete planes
    plane_balance_items: List[Dict[str, Any]] = []
    for p_spec in LO_SHU_EIGHT_PLANES:
        pid = p_spec["id"]
        p_state = planes.get(pid, {})
        if not p_state.get("is_complete", False):
            entry = _select_library_entry(entries_by_sig, f"plane:{pid}", allow_draft=allow_draft)
            if entry:
                lv = entry["language_variants"][ed_key]
                plane_balance_items.append(
                    {
                        "plane_id": pid,
                        "plane_name": p_spec["name"],
                        "digits": list(p_spec["digits"]),
                        "fraction": p_state.get("fraction", "0/3"),
                        "habit": lv["gentle_steps_practical"][0],
                        "fact_id": f"link:plane_incomplete:{pid}",
                    }
                )

    # Step 2: Existing ranked 5-element remedies (100% unchanged) + optional element_support extra
    top_rem_status = remedy_lib.get("meta", {}).get("status", "DRAFT")
    raw_elem_support = remedy_lib.get("element_support", {}) if (allow_draft or top_rem_status == "APPROVED") else {}
    element_support_extras: List[Dict[str, Any]] = []
    for r_item in ranked_5_element_remedies.get("ranked_top3_remedies", []):
        if r_item.get("has_open_digit") and r_item["element"] in raw_elem_support:
            es = raw_elem_support[r_item["element"]]
            extra_obj: Dict[str, Any] = {
                "element": r_item["element"],
                "colours": es.get("colours", []),
                "habits": es.get("habits", []),
            }
            if not is_basic_or_free:
                extra_obj["gems_info_optional"] = [
                    f"{g} (traditionally associated, optional)"
                    for g in es.get("gems_as_commonly_taught", [])
                ]
            element_support_extras.append(extra_obj)

    # Step 3: Separate Planet Practices block (never in Basic/Free; omitted if empty)
    planet_practices_block: Optional[Dict[str, Any]] = None
    if not is_basic_or_free:
        target_planets: List[Tuple[int, str]] = []
        seen_p: Set[int] = set()
        # Malefic-leaning or high-concentration repeated planets (count >= 3)
        for d in range(1, 10):
            c = counts.get(d, 0)
            if c >= 3 and (d in {4, 7, 8, 9} or c >= 4):
                target_planets.append((d, f"repeated_{c}x"))
                seen_p.add(d)
        # Key missing planets (up to 3 so block stays focused and personal)
        for md in missing_digits[:3]:
            if md not in seen_p:
                target_planets.append((md, "missing_from_grid"))
                seen_p.add(md)

        packs = []
        for p_num, reason in target_planets:
            formatted = format_planet_remedy_pack(
                p_num,
                remedy_lib,
                tier=tier,
                edition=edition,
                user_remedy_style=user_remedy_style,
                allow_draft=allow_draft,
            )
            if formatted and formatted.get("items"):
                formatted["selection_reason"] = reason
                packs.append(formatted)

        if packs:
            planet_practices_block = {
                "heading": "Traditionally Suggested Planetary Practices",
                "framing_note": (
                    "Habits and practices traditionally suggested to support calm, steady choices "
                    f"linked to your planets and months. {REMEDY_EFFORT_LINE}"
                ),
                "planets": packs,
            }

    # Step 4: Timing ("start before" notes from 2027 Care Guide)
    timing_notes = [
        {
            "month_name": m["month_name"],
            "personal_month": m["personal_month"],
            "planet_label": m["planet_label"],
            "start_before": m["start_before"],
        }
        for m in care_guide_2027.get("priority_care_months", [])
    ]

    return {
        "order": [
            "step_1_plane_balance",
            "step_2_element_balance",
            "step_3_planet_practices",
            "step_4_timing_start_before",
        ],
        "step_1_plane_balance": plane_balance_items,
        "step_2_element_balance": {
            "existing_ranked_element_remedies": ranked_5_element_remedies,
            "optional_element_support_extra": element_support_extras,
        },
        "step_3_planet_practices": planet_practices_block,
        "step_4_timing_start_before": timing_notes,
        "affirmation_and_manifestation": affirmation_manifestation,
    }


def compute_full_indications_bundle(
    *,
    day: int,
    month: int,
    year: int,
    gender: Optional[str] = "male",
    calling_name: str = "",
    target_year: int = 2026,
    care_guide_year: int = 2027,
    reference_date: Optional[date] = None,
    edition: str = "india",
    tier: str = "free",
    entitlement_tier: Optional[str] = None,
    user_remedy_style: Optional[str] = None,
    topic: Optional[str] = None,
    requested_affirmation_on_demand: bool = False,
    neighbour_config_override: Optional[Dict[str, Any]] = None,
    allow_draft: Optional[bool] = None,
) -> Dict[str, Any]:
    """
    Executes the fixed 8-step reasoning order (Section 3 & Section 16.B):
      1. Foundation
      2. Lo Shu (Layer 1)
      3. Commanding planet(s)
      4. Repetition effect per planet (existing software logic + reference stage)
      5. Existing element balance (Layer 1) + Neighbour relations (Layers 2 & 3)
      6. Cycles (Personal Year / Month / Day + 2027 Care Guide)
      7. Remedies in fixed order + Section 19 Server-Side Affirmation & Manifestation
      8. Structured Indication Cards & PII-free ReadingPlan for Section 9/17 Explanation
    """
    if allow_draft is None:
        allow_draft = os.getenv("ENVIRONMENT", "local").strip().lower() != "production"

    ref_dt = reference_date or date(target_year, 11, 12)
    ed_key = "international" if str(edition).lower() == "international" else "india"
    eff_entitlement = entitlement_tier or tier

    ind_lib = load_indication_library()
    rem_lib = load_remedy_library()
    entries_by_sig: Dict[str, List[Dict[str, Any]]] = {}
    for e in ind_lib.get("entries", []):
        entries_by_sig.setdefault(e["fact_signature"], []).append(e)

    # ── STEP 1: FOUNDATION ──
    driver = calc_driver(day)
    conductor = calc_bhagyank(day, month, year)
    kua_det = calculate_kua_details(year, gender) if gender else {"kua_number": None, "display": "Needs gender"}
    dob_digits_sum = sum_digits_str(f"{day:02d}{month:02d}{year:04d}")
    conductor_steps = calc_compound_steps(dob_digits_sum)
    day_steps = calc_compound_steps(day)
    karmic_master = assess_karmic_and_master(day, month, year, calling_name or "")

    name_number: Optional[int] = None
    name_compound: Optional[int] = None
    if calling_name and calling_name.strip():
        ch_res = calculate_chaldean_name(calling_name.strip())
        name_number = ch_res.get("single_digit")
        name_compound = ch_res.get("compound_number")

    master_path_note: Optional[str] = None
    for intermediate in conductor_steps["steps"][:-1]:
        if intermediate in (11, 22, 33):
            master_path_note = f"passes through {intermediate} on the way to {conductor}"
            break

    karmic_notes: List[int] = []
    for kn in (13, 14, 16, 19):
        if day == kn or dob_digits_sum == kn or name_compound == kn:
            karmic_notes.append(kn)

    foundation = {
        "driver": driver,
        "driver_planet": format_planet_term(driver, edition),
        "conductor": conductor,
        "conductor_planet": format_planet_term(conductor, edition),
        "kua": kua_det.get("kua_number"),
        "kua_display": kua_det.get("display"),
        "name_number": name_number,
        "name_compound": name_compound,
        "conductor_compound": dob_digits_sum,
        "conductor_reduction_path": " -> ".join(str(s) for s in conductor_steps["steps"]),
        "day_compound": day if day >= 10 else None,
        "master_path_note": master_path_note,
        "karmic_notes": karmic_notes,
        "existing_karmic_master_assessment": karmic_master,
    }

    # ── STEP 2: LO SHU (LAYER 1 — DOB DIGITS ONLY) ──
    loshu = calc_loshu_dob_only(day, month, year)
    counts = loshu["counts"]
    present_digits = loshu["present"]
    missing_digits = loshu["missing"]
    repeated_digits = loshu["repeated"]
    planes = loshu["planes"]

    # ── STEP 3: COMMANDING PLANET(S) ──
    commanding = detect_commanding_planet(counts)

    # ── STEP 4: REPETITION EFFECT PER PLANET (EXISTING LOGIC + REFERENCE STAGES) ──
    repetition_by_planet: Dict[str, Any] = {}
    gov_freq = rule_governance.evaluate_grid_frequencies(counts)
    core_rep = analyze_repeat_numbers(day, month, year)
    core_rep_by_num = {item["number"]: item for item in core_rep.get("evaluations", [])}

    for dig in range(1, 10):
        c = counts.get(dig, 0)
        oracle_deg = classify_digit_degree(dig, c)
        stage = classify_reference_repetition_stage(dig, c)
        mod = PLANET_CHARACTER_MODIFIERS[dig]
        repetition_by_planet[str(dig)] = {
            "digit": dig,
            "planet": mod["planet"],
            "count": c,
            "reference_stage": stage,
            "oracle_degree": oracle_deg.get("degree", "MISSING"),
            "oracle_status": oracle_deg.get("status", "DEFICIENT"),
            "rule_governance_degree": (gov_freq.get("evaluations") or {}).get(str(dig), {}).get("repetition_category", "MISSING"),
            "core_matrix_type": core_rep_by_num.get(dig, {}).get("type", "Missing"),
            "character_modifier": mod["character"],
            "malefic_leaning": bool(c >= 3 and (dig in {4, 7, 8, 9} or c >= 4)),
            "benefic_leaning": bool(c in (1, 2) or (c >= 3 and dig == 1)),
        }

    # ── STEP 5: EXISTING ELEMENT BALANCE (LAYER 1) + NEIGHBOUR RELATIONS (LAYERS 2 & 3) ──
    core_elements = analyze_elements_balancing(day, month, year)
    ranked_5_elem = extract_ranked_5_element_remedies(counts, missing_digits)
    neighbours_l2_l3 = evaluate_neighbour_relations_layer2_and_3(
        counts,
        missing_digits,
        ranked_5_elem,
        neighbour_config=neighbour_config_override,
        allow_draft=allow_draft,
    )

    # ── STEP 6: CYCLES & LOGIC LINKS ──
    py_cur = calc_personal_year(day, month, ref_dt.year)
    pm_cur = calc_personal_month(py_cur, ref_dt.month)
    pd_cur = calc_personal_day(py_cur, pm_cur, ref_dt.day, ref_dt.month, ref_dt.year)

    care_guide_2027 = build_2027_care_guide(
        day,
        month,
        care_guide_year,
        missing_digits,
        commanding["commanders"],
        entries_by_sig,
        rem_lib,
        edition=edition,
        tier=tier,
        user_remedy_style=user_remedy_style,
        allow_draft=allow_draft,
    )

    # Deterministic Facts & Logic Links (with IDs — Section 9 & 16.C)
    facts_by_id: Dict[str, Dict[str, Any]] = {
        f"foundation:driver:{driver}": {"type": "driver", "value": driver, "planet": PLANET_MAP_1_TO_9[driver]["english"]},
        f"foundation:conductor:{conductor}": {"type": "conductor", "value": conductor, "planet": PLANET_MAP_1_TO_9[conductor]["english"]},
        f"pair:dc:{driver}_{conductor}": {"type": "pair_dynamic", "driver": driver, "conductor": conductor},
        f"cycle:py_{ref_dt.year}:{py_cur}": {"type": "personal_year", "year": ref_dt.year, "value": py_cur},
        f"cycle:pm_{ref_dt.year}_{ref_dt.month:02d}:{pm_cur}": {"type": "personal_month", "month": ref_dt.month, "value": pm_cur},
        f"cycle:pd_{ref_dt.isoformat()}:{pd_cur}": {"type": "personal_day", "value": pd_cur},
        f"cycle:py_{care_guide_year}:{care_guide_2027['personal_year']}": {
            "type": "personal_year",
            "year": care_guide_year,
            "value": care_guide_2027["personal_year"],
        },
    }
    if kua_det.get("kua_number"):
        facts_by_id[f"foundation:kua:{kua_det['kua_number']}"] = {"type": "kua", "value": kua_det["kua_number"]}
    if name_number:
        facts_by_id[f"foundation:name_number:{name_number}"] = {"type": "name_number", "value": name_number}
    if dob_digits_sum >= 10:
        facts_by_id[f"note:compound_note:{dob_digits_sum}"] = {
            "type": "compound_note",
            "compound": dob_digits_sum,
            "reduces_to": conductor,
        }
    if master_path_note:
        facts_by_id[f"note:master_path_note:{conductor}"] = {"type": "master_path_note", "note": master_path_note}
    for kn in karmic_notes:
        facts_by_id[f"note:karmic_note:{kn}"] = {"type": "karmic_note", "number": kn}

    logic_links: List[Dict[str, Any]] = []

    # Commanding planet links
    for cmd in commanding["commanders"]:
        cid = f"link:commanding_planet:{cmd['digit']}_x{cmd['count']}"
        facts_by_id[cid] = cmd
        logic_links.append({"id": cid, "kind": "commanding_planet", "digit": cmd["digit"], "count": cmd["count"]})
        if cmd["benefic_lean"]:
            bl_id = f"link:commanding_planet_benefic_lean:{cmd['digit']}"
            facts_by_id[bl_id] = {"digit": cmd["digit"], "note": "Traditionally steadying strength"}
            logic_links.append({"id": bl_id, "kind": "commanding_planet_benefic_lean", "digit": cmd["digit"]})
        if cmd["malefic_lean"]:
            ml_id = f"link:commanding_planet_malefic_lean:{cmd['digit']}"
            facts_by_id[ml_id] = {"digit": cmd["digit"], "growth_edge": cmd["growth_edge"]}
            logic_links.append({"id": ml_id, "kind": "commanding_planet_malefic_lean", "digit": cmd["digit"]})

    # Planet repeated stage & missing links
    for dig in range(1, 10):
        c = counts.get(dig, 0)
        stage = classify_reference_repetition_stage(dig, c)
        if c == 0:
            mid = f"link:planet_missing:{dig}"
            facts_by_id[mid] = {"digit": dig, "planet": PLANET_MAP_1_TO_9[dig]["english"]}
            logic_links.append({"id": mid, "kind": "planet_missing", "digit": dig})
        else:
            sid = f"link:planet_repeated_stage:{dig}:{stage}:{c}"
            facts_by_id[sid] = {"digit": dig, "count": c, "stage": stage}
            logic_links.append({"id": sid, "kind": "planet_repeated_stage", "digit": dig, "count": c, "stage": stage})

    if driver in missing_digits:
        md_id = f"link:missing_driver:{driver}"
        facts_by_id[md_id] = {"driver": driver}
        logic_links.append({"id": md_id, "kind": "missing_driver", "digit": driver})

    if name_number is not None:
        nk = "name_agrees_driver" if name_number == driver else "name_differs_driver"
        nid = f"link:{nk}:{name_number}_{driver}"
        facts_by_id[nid] = {"name_number": name_number, "driver": driver}
        logic_links.append({"id": nid, "kind": nk, "name_number": name_number, "driver": driver})

    # Plane links
    for p_spec in LO_SHU_EIGHT_PLANES:
        pid = p_spec["id"]
        pst = planes[pid]
        if pst["is_complete"]:
            pl_id = f"link:plane_complete_intensifies:{pid}"
            facts_by_id[pl_id] = {"plane": pid, "digits": list(p_spec["digits"])}
            logic_links.append({"id": pl_id, "kind": "plane_complete_intensifies", "plane": pid})
        else:
            pl_id = f"link:plane_incomplete:{pid}"
            facts_by_id[pl_id] = {"plane": pid, "fraction": pst["fraction"]}
            logic_links.append({"id": pl_id, "kind": "plane_incomplete", "plane": pid, "fraction": pst["fraction"]})

    # Neighbour links
    for np in neighbours_l2_l3["layer_2_neighbour_relations"]["pairs"]:
        if np["configured"]:
            facts_by_id[np["fact_id"]] = np
            logic_links.append(
                {
                    "id": np["fact_id"],
                    "kind": f"neighbour_{np['combined_relation'].split()[0]}",
                    "pair": np["pair"],
                    "combined_relation": np["combined_relation"],
                }
            )

    # Gap meets cycle & Commanding planet meets cycle
    if py_cur in missing_digits:
        gid = f"link:gap_meets_cycle:py:{py_cur}"
        facts_by_id[gid] = {"cycle": "personal_year", "digit": py_cur}
        logic_links.append({"id": gid, "kind": "gap_meets_cycle", "digit": py_cur, "cycle": "personal_year"})
    if pm_cur in missing_digits:
        gid = f"link:gap_meets_cycle:pm:{pm_cur}"
        facts_by_id[gid] = {"cycle": "personal_month", "digit": pm_cur}
        logic_links.append({"id": gid, "kind": "gap_meets_cycle", "digit": pm_cur, "cycle": "personal_month"})

    for cmd in commanding["commanders"]:
        if cmd["digit"] in (py_cur, pm_cur):
            cid = f"link:commanding_planet_meets_cycle:{cmd['digit']}"
            facts_by_id[cid] = {"digit": cmd["digit"], "py": py_cur, "pm": pm_cur}
            logic_links.append({"id": cid, "kind": "commanding_planet_meets_cycle", "digit": cmd["digit"]})

    # Determine whether profile has ANY tension fact (Section 8 & 14.A)
    has_tension = bool(
        missing_digits
        or any(counts.get(d, 0) >= 3 for d in range(1, 10))
        or any(p["is_complete"] for p in planes.values())
        or any(
            np["combined_relation"] == "tension"
            for np in neighbours_l2_l3["layer_2_neighbour_relations"]["pairs"]
        )
        or py_cur in (4, 7, 8, 9)
        or pm_cur in (4, 7, 8, 9)
    )

    # ── STEP 7: SECTION 19 AFFIRMATION/MANIFESTATION + FIXED-ORDER REMEDIES ──
    aff_man = build_affirmation_and_manifestation(
        driver=driver,
        conductor=conductor,
        personal_year=care_guide_2027["personal_year"],
        current_personal_month=pm_cur,
        commanders=commanding["commanders"],
        missing_digits=missing_digits,
        care_guide_2027=care_guide_2027,
        remedy_lib=rem_lib,
        entitlement_tier=eff_entitlement,
        topic=topic,
        requested_on_demand=requested_affirmation_on_demand,
        allow_draft=allow_draft,
    )

    remedies = build_ordered_remedies(
        counts=counts,
        missing_digits=missing_digits,
        planes=planes,
        commanders=commanding["commanders"],
        ranked_5_element_remedies=ranked_5_elem,
        care_guide_2027=care_guide_2027,
        affirmation_manifestation=aff_man,
        entries_by_sig=entries_by_sig,
        remedy_lib=rem_lib,
        tier=tier,
        edition=edition,
        user_remedy_style=user_remedy_style,
        allow_draft=allow_draft,
    )

    # ── STEP 8: INDICATION CARDS (Free / Basic / Commanding / Complete Planes / Pair) ──
    cards: List[Dict[str, Any]] = []

    # Card A: Commanding Planet card when active (e.g., 11-10-2011 Sun x5)
    if commanding["has_commander"]:
        cmd = commanding["commanders"][0]
        c_entry = _select_library_entry(entries_by_sig, f"commanding_planet:{cmd['digit']}", allow_draft=allow_draft)
        present_desc = ", ".join(f"{d} (x{counts[d]})" if counts[d] > 1 else f"{d} (once)" for d in present_digits)
        missing_desc = ", ".join(str(d) for d in missing_digits) if missing_digits else "None"
        if c_entry:
            lv = c_entry["language_variants"][ed_key]
            why_s = lv["why_this_shows"]
            ind_s = lv["what_it_may_indicate"]
            ge_s = lv.get("growth_edge") or cmd["growth_edge"]
            mind_s = lv["be_mindful_of"]
            steps_s = list(lv["gentle_steps_practical"])
        elif allow_draft:
            why_s = f"{cmd['digit']} ({format_planet_term(cmd['digit'], edition)}) repeats {cmd['count']} times and leads the birth-date grid."
            ind_s = f"Strong {cmd['strength'].lower()}, modified by {cmd['character_note']}."
            ge_s = f"{cmd['growth_edge']} when {cmd['digit']} repeats {cmd['count']} times, paired with {cmd['strength'].lower()}."
            mind_s = "pacing solo effort, listening to counsel and keeping incomplete planes balanced."
            steps_s = [
                "Start with plane-balance habits for your incomplete planes first.",
                cmd["practical_step"],
            ]
        else:
            why_s = ""
            ind_s = ""
            ge_s = ""
            mind_s = ""
            steps_s = []

        if why_s:
            cards.append(
                {
                    "card_id": f"commanding_planet_{cmd['digit']}",
                    "kind": "commanding_planet",
                    "title": f"Commanding Planet — {format_planet_term(cmd['digit'], edition)} ({cmd['digit']} x{cmd['count']})",
                    "your_numbers": f"Present in grid: {present_desc} · Missing: {missing_desc}",
                    "evidence_ids": [
                        f"link:commanding_planet:{cmd['digit']}_x{cmd['count']}",
                        f"link:planet_repeated_stage:{cmd['digit']}:{classify_reference_repetition_stage(cmd['digit'], cmd['count'])}:{cmd['count']}",
                    ],
                    "why_this_shows": why_s,
                    "what_it_may_indicate": ind_s,
                    "growth_edge": ge_s,
                    "be_mindful_of": mind_s,
                    "gentle_steps": steps_s,
                    "remedy_effort_line": REMEDY_EFFORT_LINE,
                    "footer": DEFAULT_FOOTER,
                }
            )

    # Card B: Complete Plane(s) card (with optional neighbour tension/support note when present)
    for p_spec in LO_SHU_EIGHT_PLANES:
        pid = p_spec["id"]
        if planes[pid]["is_complete"]:
            p_entry = _select_library_entry(entries_by_sig, f"plane:{pid}", allow_draft=allow_draft)
            if p_entry:
                lv = p_entry["language_variants"][ed_key]
                p_digits = set(p_spec["digits"])
                in_plane_neighbours = [
                    np
                    for np in neighbours_l2_l3["layer_2_neighbour_relations"]["pairs"]
                    if np["configured"] and set(np["digits"]).issubset(p_digits)
                ]
                extra_neighbour_note = ""
                ev_ids = [f"link:plane_complete_intensifies:{pid}"]
                for np in in_plane_neighbours:
                    ev_ids.append(np["fact_id"])
                    if np["combined_relation"] == "tension":
                        extra_neighbour_note += (
                            f" Inside this plane, {np['pair'].replace('-', ' and ')} are in a tension relation, "
                            f"so authority and duty may sometimes pull in different directions."
                        )
                    elif np["combined_relation"] == "supportive":
                        extra_neighbour_note += (
                            f" Inside this plane, {np['pair'].replace('-', ' and ')} mutually support steady execution."
                        )
                cards.append(
                    {
                        "card_id": f"complete_plane_{pid}",
                        "kind": "complete_plane",
                        "title": f"{p_spec['name']} ({'-'.join(str(x) for x in p_spec['digits'])}) — Complete (3/3)",
                        "your_numbers": f"Digits {', '.join(str(x) for x in p_spec['digits'])} are all present in your birth-date grid.",
                        "evidence_ids": ev_ids,
                        "why_this_shows": lv["why_this_shows"],
                        "what_it_may_indicate": (lv["what_it_may_indicate"] + extra_neighbour_note).strip(),
                        "growth_edge": (
                            f"{lv.get('shadow_side', 'Holding on too tightly under pressure')} "
                            f"(complete {'-'.join(str(x) for x in p_spec['digits'])} plane), paired with "
                            f"{lv.get('positive_traits', 'steady capability').lower()} — {lv['gentle_steps_practical'][0].lower()}"
                        ),
                        "be_mindful_of": lv["be_mindful_of"],
                        "gentle_steps": list(lv["gentle_steps_practical"]),
                        "remedy_effort_line": REMEDY_EFFORT_LINE,
                        "footer": DEFAULT_FOOTER,
                    }
                )

    # Card C: Primary Foundation & Personal Year Indication Card (ensures every profile has a clear primary card when entries exist)
    dc_entry = _select_library_entry(entries_by_sig, f"dc:{driver}_{conductor}", allow_draft=allow_draft)
    py_entry = _select_library_entry(entries_by_sig, f"personal_year:{py_cur}", allow_draft=allow_draft)
    primary_entry = dc_entry or py_entry
    if primary_entry is not None:
        lv = primary_entry["language_variants"][ed_key]
        ev_ids = [
            f"foundation:driver:{driver}",
            f"foundation:conductor:{conductor}",
            f"cycle:py_{ref_dt.year}:{py_cur}",
        ]
        if master_path_note:
            ev_ids.append(f"note:master_path_note:{conductor}")
        ge_line = ""
        if has_tension:
            if missing_digits:
                first_m = missing_digits[0]
                ge_line = (
                    f"{PLANET_CHARACTER_MODIFIERS[driver]['growth_edge']} while digit {first_m} "
                    f"({PLANET_MAP_1_TO_9[first_m]['english']}) is open in your grid, paired with "
                    f"{PLANET_CHARACTER_MODIFIERS[driver]['strength'].lower()} — {lv['gentle_steps_practical'][0]}"
                )
            else:
                ge_line = (
                    f"{PLANET_CHARACTER_MODIFIERS[driver]['growth_edge']}, paired with "
                    f"{PLANET_CHARACTER_MODIFIERS[driver]['strength'].lower()} — {lv['gentle_steps_practical'][0]}"
                )
        num_parts = [
            f"Driver {driver} ({format_planet_term(driver, edition)})",
            f"Conductor {conductor} ({format_planet_term(conductor, edition)})",
            f"{ref_dt.year} Personal Year {py_cur} ({format_planet_term(py_cur, edition)})",
        ]
        if master_path_note:
            num_parts.append(f"Path note: {master_path_note}")
        cards.insert(
            0,
            {
                "card_id": f"foundation_{driver}_{conductor}_py_{py_cur}",
                "kind": "foundation_overview",
                "title": f"Personalised Indication — Driver {driver} · Conductor {conductor} · Personal Year {py_cur}",
                "your_numbers": " · ".join(num_parts),
                "evidence_ids": ev_ids,
                "why_this_shows": lv["why_this_shows"],
                "what_it_may_indicate": lv["what_it_may_indicate"],
                "growth_edge": ge_line,
                "be_mindful_of": lv["be_mindful_of"],
                "gentle_steps": list(lv["gentle_steps_practical"]),
                "remedy_effort_line": REMEDY_EFFORT_LINE,
                "footer": DEFAULT_FOOTER,
            },
        )

    # Build PII-free ReadingPlan for Section 9 & Section 17 (`Write` + `Check` stages)
    allowed_numbers: Set[str] = {
        str(driver),
        str(conductor),
        str(py_cur),
        str(pm_cur),
        str(pd_cur),
        str(ref_dt.year),
        str(care_guide_year),
        str(care_guide_2027["personal_year"]),
        *[str(d) for d in present_digits],
        *[str(d) for d in missing_digits],
        *[str(c) for c in counts.values() if c > 0],
        "1",
        "2",
        "3",
        "4",
        "5",
        "8",
        "9",
        "32",
        "12",
        "90",
    }
    if kua_det.get("kua_number"):
        allowed_numbers.add(str(kua_det["kua_number"]))
    if name_number:
        allowed_numbers.add(str(name_number))
    if dob_digits_sum >= 10:
        allowed_numbers.add(str(dob_digits_sum))
    for s in conductor_steps["steps"]:
        allowed_numbers.add(str(s))
    for kn in karmic_notes:
        allowed_numbers.add(str(kn))
    for m_obj in care_guide_2027["months"]:
        allowed_numbers.add(str(m_obj["personal_month"]))

    ent_canonical = resolve_package_entitlement(eff_entitlement)["canonical_tier"]
    visible_cards = cards[:1] if ent_canonical == "free" else cards

    allowed_planets: Set[int] = {
        driver,
        conductor,
        py_cur,
        pm_cur,
        pd_cur,
        care_guide_2027["personal_year"],
        *present_digits,
    }
    if kua_det.get("kua_number") in range(1, 10):
        allowed_planets.add(int(kua_det["kua_number"]))
    if name_number in range(1, 10):
        allowed_planets.add(int(name_number))
    if has_tension and missing_digits:
        allowed_planets.add(int(missing_digits[0]))
    if ent_canonical in {"premium", "planner_2027", "charm_premium"}:
        allowed_planets.update(missing_digits)

    allowed_months: Set[str] = {m.lower() for m in MONTH_NAMES_1_TO_12}

    remedy_blob_parts: List[str] = []
    for p_item in remedies["step_1_plane_balance"]:
        remedy_blob_parts.append(p_item["habit"])
    for e_item in ranked_5_elem.get("ranked_top3_remedies", []):
        remedy_blob_parts.append(e_item["remedy"])
    if remedies["step_3_planet_practices"]:
        for pk in remedies["step_3_planet_practices"]["planets"]:
            for it in pk.get("items", []):
                remedy_blob_parts.append(it["text"])
            if pk.get("gemstone_info"):
                remedy_blob_parts.append(pk["gemstone_info"]["display_note"])
    for m_obj in care_guide_2027["months"]:
        if m_obj.get("card"):
            remedy_blob_parts.extend(m_obj["card"].get("traditional_practices", []))

    reading_plan = {
        "entitlement_tier": str(eff_entitlement or ent_canonical),
        "philosophy_line": PHILOSOPHY_LINE,
        "footer": DEFAULT_FOOTER,
        "health_safety_line": HEALTH_SAFETY_LINE,
        "remedy_effort_line": REMEDY_EFFORT_LINE,
        "has_tension": has_tension,
        "facts": facts_by_id,
        "logic_links": logic_links,
        "cards": visible_cards,
        "care_guide_priority_months": care_guide_2027["priority_care_months"],
        "remedy_order": remedies["order"],
        "affirmation_level": aff_man["affirmation_level"],
        "manifestation_level": aff_man["manifestation_level"],
        "validator_constraints": {
            "supplied_fact_ids": sorted(facts_by_id.keys()),
            "allowed_numbers": sorted(allowed_numbers),
            "allowed_planets": sorted(allowed_planets),
            "allowed_months": sorted(allowed_months),
            "allowed_remedy_text_blob": " ".join(remedy_blob_parts),
        },
    }
    plan_hash = hashlib.sha256(
        json.dumps(reading_plan, sort_keys=True, ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    reading_plan["plan_hash"] = plan_hash

    return {
        "reasoning_order": [
            "1_foundation",
            "2_lo_shu_layer_1",
            "3_commanding_planet",
            "4_repetition_effects",
            "5_elements_and_neighbours",
            "6_cycles_and_care_guide",
            "7_ordered_remedies_and_manifestation",
            "8_indication_cards_and_explanation_plan",
        ],
        "foundation": foundation,
        "lo_shu_layer_1": loshu,
        "commanding_planet": commanding,
        "repetition_by_planet": repetition_by_planet,
        "element_balance_layer_1": {
            "core_matrix_elements": core_elements,
            "ranked_5_element_remedies": ranked_5_elem,
        },
        **neighbours_l2_l3,
        "cycles": {
            "label": "Personal Year / Month / Day",
            "reference_date": ref_dt.isoformat(),
            "personal_year": py_cur,
            "personal_month": pm_cur,
            "personal_day": pd_cur,
            "care_guide_2027": care_guide_2027,
        },
        "remedies": remedies,
        "affirmation_and_manifestation": aff_man,
        "indication_cards": visible_cards,
        "has_tension": has_tension,
        "reading_plan": reading_plan,
    }


def answer_charm_indication_or_care_question(
    question: str,
    bundle: Dict[str, Any],
    *,
    edition: str = "india",
) -> Optional[Dict[str, Any]]:
    """
    Deterministic library-backed composer for Charm AI timing / care-months /
    remedies / affirmation / manifestation questions (Sections 9, 10, 16.D & 19).
    Also enforces event-prediction refusal (`0` credits deducted).
    """
    refusal = detect_event_prediction_question(question)
    if refusal:
        topic_key, refusal_text = refusal
        return {
            "kind": "REFUSED_PREDICTION",
            "topic": topic_key,
            "headline": "Reflective Guidance Boundary",
            "text": refusal_text,
            "next_steps": [
                "Ask what your numbers may indicate for communication, pacing or daily habits in this area."
            ],
            "follow_up_question": f"What do my numbers indicate for steady habits in {topic_key} this year?",
        }

    q_low = str(question or "").lower()
    cg = bundle["cycles"]["care_guide_2027"]
    fnd = bundle["foundation"]
    loshu = bundle["lo_shu_layer_1"]
    aff_man = bundle["affirmation_and_manifestation"]

    # 1. Care months in 2027 (Section 9 / worked example 4)
    if ("2027" in q_low and any(w in q_low for w in ("care", "month", "months", "mindful", "watch"))) or (
        "which months" in q_low and "care" in q_low
    ):
        py27 = cg["personal_year"]
        months_by_num = {m["month_number"]: m for m in cg["months"]}
        care_months = [m for m in cg["months"] if m["needs_extra_care"] and m.get("card")]
        lines = [
            f"**Your numbers:** 2027 is your **Personal Year {py27}** ({cg['personal_year_planet']}). "
            f"Present grid digits: {', '.join(str(d) for d in loshu['present'])}; "
            f"open (missing) grid digits: {', '.join(str(d) for d in loshu['missing']) or 'none'}.",
        ]
        steps: List[str] = []
        touches_hs = False
        for cm in care_months[:4]:
            card = cm["card"]
            gap_tag = (
                f" — digit {cm['personal_month']} is missing from your birth-date grid, and the cycle brings it forward"
                if cm["gap_meets_cycle"]
                else ""
            )
            lines.append(
                f"• **{cm['month_name']} 2027 — Personal Month {cm['personal_month']} ({cm['planet_label']})**{gap_tag}: "
                f"{card['what_it_may_indicate']} Be mindful of {card['be_mindful_of']} ({cm['start_before']})."
            )
            if card["gentle_steps"]:
                steps.append(f"{cm['month_name']} ({cm['start_before']}): {card['gentle_steps'][0]}")
            if card.get("health_safety_line"):
                touches_hs = True

        lines.append(f"**Growth edge:** Pace busy months early rather than reacting under last-minute pressure.")
        lines.append(REMEDY_EFFORT_LINE)
        if touches_hs:
            lines.append(HEALTH_SAFETY_LINE)
        lines.append(DEFAULT_FOOTER)

        return {
            "kind": "ANSWERED_CARE_GUIDE",
            "topic": "general",
            "headline": f"2027 Care Months — Personal Year {py27}",
            "text": "\n\n".join(lines),
            "next_steps": steps[:3] or ["Prepare calm routines in the month before each demanding Personal Month."],
            "follow_up_question": "Which daily habits help balance my incomplete Lo Shu planes this year?",
        }

    # 2. Affirmation / Manifestation request (Section 19)
    if any(w in q_low for w in ("affirmation", "manifest", "manifestation", "intention")):
        lines = [
            f"**Your numbers:** Driver {fnd['driver']} ({fnd['driver_planet']}), "
            f"Conductor {fnd['conductor']} ({fnd['conductor_planet']}), "
            f"Personal Year {bundle['cycles']['personal_year']}.",
        ]
        if aff_man.get("affirmation"):
            lbl = "Personalised Affirmation" if "personalised" in aff_man["affirmation_level"] else "General Affirmation"
            lines.append(f"**{lbl}:** \"{aff_man['affirmation']}\"")
        if aff_man.get("manifestation"):
            man = aff_man["manifestation"]
            if "month_intention" in man:
                lines.append(f"**Current-Month Intention ({man['month_theme']}):** {man['month_intention']}")
                lines.append(f"**Weekly Action:** {man['weekly_action']}")
                lines.append(f"**Review Prompt:** {man['review_prompt']}")
            elif "year_theme" in man:
                lines.append(f"**Year Theme:** {man['year_theme']}")
                lines.append(f"**Intention:** {man['intention_sentence']}")
        if aff_man.get("upgrade_note"):
            lines.append(aff_man["upgrade_note"])
        lines.append(REMEDY_EFFORT_LINE)
        lines.append(DEFAULT_FOOTER)

        return {
            "kind": "ANSWERED_AFFIRMATION_MANIFESTATION",
            "topic": "general",
            "headline": "Affirmation & Intention Guide",
            "text": "\n\n".join(lines),
            "next_steps": [
                "Repeat your affirmation calmly in the morning and pair it with one steady daily habit.",
                "Review your progress once a week without rushing.",
            ],
            "follow_up_question": "Which months should I take extra care in 2027?",
        }

    return None
