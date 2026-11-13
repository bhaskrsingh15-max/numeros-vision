"""
app/engine/indication_schema_and_loader.py
==========================================
Schema validation, plain-text file loaders (all imported entries marked DRAFT
and softened with Section 14.A vocabulary rules), DRAFT -> APPROVED promotion,
and the canonical `generate_missing_content_report()` audit.
"""

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from app.engine.digit_root import LO_SHU_EIGHT_PLANES
from app.engine.indication_validator import (
    check_text_language_and_remedy_rules,
    soften_shadow_text,
)

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_INDICATION_LIB_PATH = DATA_DIR / "indication_library.json"
DEFAULT_REMEDY_LIB_PATH = DATA_DIR / "remedy_library.json"
DEFAULT_NEIGHBOUR_REL_PATH = DATA_DIR / "neighbour_relations.json"

VALID_STATUSES = {"DRAFT", "APPROVED"}
VALID_DEPTHS = {1, 2, 3}
VALID_DIRECTIONAL_RELATIONS = {"friendly", "neutral", "enemy"}


def load_indication_library(path: Optional[Path] = None) -> Dict[str, Any]:
    target = Path(path) if path else DEFAULT_INDICATION_LIB_PATH
    with open(target, encoding="utf-8") as f:
        data = json.load(f)
    validate_indication_library_schema(data)
    return data


def load_remedy_library(path: Optional[Path] = None) -> Dict[str, Any]:
    target = Path(path) if path else DEFAULT_REMEDY_LIB_PATH
    with open(target, encoding="utf-8") as f:
        data = json.load(f)
    validate_remedy_library_schema(data)
    return data


def load_neighbour_relations(path: Optional[Path] = None) -> Dict[str, Any]:
    target = Path(path) if path else DEFAULT_NEIGHBOUR_REL_PATH
    with open(target, encoding="utf-8") as f:
        data = json.load(f)
    validate_neighbour_relations_schema(data)
    return data


def validate_indication_library_schema(data: Dict[str, Any]) -> None:
    """Raises `ValueError` if any entry violates schema, language, or harsh-vocabulary rules."""
    if not isinstance(data, dict):
        raise ValueError("Indication library root must be a JSON object.")
    for req_top in ("version", "philosophy_line", "default_footer", "health_safety_line", "entries"):
        if req_top not in data:
            raise ValueError(f"Missing top-level field `{req_top}` in indication_library.json.")

    seen_ids: Set[str] = set()
    seen_keys: Set[Tuple[str, str, int]] = set()
    for idx, entry in enumerate(data["entries"]):
        eid = entry.get("id")
        if not eid or not isinstance(eid, str):
            raise ValueError(f"Entry[{idx}] missing valid string `id`.")
        if eid in seen_ids:
            raise ValueError(f"Duplicate entry id `{eid}`.")
        seen_ids.add(eid)

        sig = entry.get("fact_signature")
        theme = entry.get("theme")
        depth = entry.get("depth")
        status = entry.get("status")
        source_tag = entry.get("source_tag")

        if not sig or not isinstance(sig, str):
            raise ValueError(f"Entry `{eid}` missing valid `fact_signature`.")
        if not theme or not isinstance(theme, str):
            raise ValueError(f"Entry `{eid}` missing valid `theme`.")
        if depth not in VALID_DEPTHS:
            raise ValueError(f"Entry `{eid}` has invalid depth `{depth}` (must be 1, 2, or 3).")
        if status not in VALID_STATUSES:
            raise ValueError(f"Entry `{eid}` has invalid status `{status}` (must be DRAFT or APPROVED).")
        if not source_tag or not isinstance(source_tag, str):
            raise ValueError(f"Entry `{eid}` missing `source_tag`.")

        combo_key = (sig, theme, depth)
        if combo_key in seen_keys:
            raise ValueError(f"Duplicate (fact_signature, theme, depth) key `{combo_key}` on `{eid}`.")
        seen_keys.add(combo_key)

        lv = entry.get("language_variants")
        if not isinstance(lv, dict) or "india" not in lv or "international" not in lv:
            raise ValueError(f"Entry `{eid}` must include both `india` and `international` language_variants.")

        for edition in ("india", "international"):
            block = lv[edition]
            for req_field in ("why_this_shows", "what_it_may_indicate", "be_mindful_of", "gentle_steps_practical"):
                if req_field not in block:
                    raise ValueError(f"Entry `{eid}` ({edition}) missing `{req_field}`.")
            if not isinstance(block["gentle_steps_practical"], list) or len(block["gentle_steps_practical"]) == 0:
                raise ValueError(f"Entry `{eid}` ({edition}) must provide at least one constructive practical step.")

            # Validate every text string in the block against language & remedy rules
            texts_to_scan = [
                block.get("why_this_shows", ""),
                block.get("what_it_may_indicate", ""),
                block.get("be_mindful_of", ""),
                block.get("growth_edge", ""),
                block.get("strength_it_comes_with", ""),
                block.get("positive_traits", ""),
                block.get("shadow_side", ""),
                block.get("key_focus", ""),
                *block.get("gentle_steps_practical", []),
            ]
            for txt in texts_to_scan:
                if txt:
                    violations = check_text_language_and_remedy_rules(str(txt))
                    if violations:
                        raise ValueError(f"Entry `{eid}` ({edition}) failed language/safety check: {violations}")


def validate_remedy_library_schema(data: Dict[str, Any]) -> None:
    """
    Validates `app/data/remedy_library.json` against Section 6, 18C & 19 rules:
    - Supports both the structured 9-planet array (`meta` + `planets[]` + `element_support`)
      and legacy planet-keyed dicts.
    - Strong stones (blue sapphire, cat's eye, hessonite) MUST carry practitioner caution.
    - Every gemstone entry MUST list `gentle_alternatives` and carry zero sales/health/wealth claims.
    - All remedy/habit/mantra/affirmation lines pass `check_text_language_and_remedy_rules`.
    """
    if not isinstance(data, dict) or "planets" not in data:
        raise ValueError("Remedy library must contain `planets`.")

    meta = data.get("meta", {})
    top_status = meta.get("status", data.get("status", "DRAFT"))
    if top_status not in VALID_STATUSES:
        raise ValueError(f"Remedy library meta.status `{top_status}` must be DRAFT or APPROVED.")

    raw_planets = data["planets"]
    planet_records: List[Dict[str, Any]] = []
    if isinstance(raw_planets, list):
        by_num = {int(p.get("number")): p for p in raw_planets if isinstance(p, dict) and p.get("number")}
        for n in range(1, 10):
            if n not in by_num:
                raise ValueError(f"Remedy library missing planet number `{n}`.")
            planet_records.append(by_num[n])
    elif isinstance(raw_planets, dict):
        for n in range(1, 10):
            if str(n) not in raw_planets:
                raise ValueError(f"Remedy library missing planet `{n}`.")
            rec = dict(raw_planets[str(n)])
            rec.setdefault("number", n)
            planet_records.append(rec)
    else:
        raise ValueError("`planets` must be a list or dict.")

    strong_stone_keywords = ("blue sapphire", "neelam", "cat's eye", "lehsunia", "hessonite", "gomed")

    for rec in planet_records:
        p_num = rec["number"]
        p_status = rec.get("status", top_status)
        if p_status not in VALID_STATUSES:
            raise ValueError(f"Planet `{p_num}` has invalid status `{p_status}`.")

        texts: List[str] = []
        if "items" in rec:
            if not isinstance(rec["items"], list) or len(rec["items"]) == 0:
                raise ValueError(f"Planet `{p_num}` must contain non-empty `items` list.")
            for item in rec["items"]:
                if not item.get("id") or not item.get("kind") or not item.get("text"):
                    raise ValueError(f"Planet `{p_num}` item missing id/kind/text: {item}")
                styles = item.get("styles", [])
                if not styles or not set(styles).issubset({"vedic", "universal", "western"}):
                    raise ValueError(f"Planet `{p_num}` item `{item.get('id')}` has invalid styles `{styles}`.")
                texts.append(str(item["text"]))

        gem = rec.get("gemstone")
        if isinstance(gem, dict):
            trad = str(gem.get("traditional") or "")
            alts = gem.get("gentle_alternatives") or []
            caution = str(gem.get("extra_caution") or "")
            if not trad or not isinstance(alts, list) or len(alts) == 0:
                raise ValueError(f"Planet `{p_num}` gemstone must include `traditional` and `gentle_alternatives`.")
            if any(sk in trad.lower() for sk in strong_stone_keywords):
                if "qualified practitioner" not in caution.lower():
                    raise ValueError(
                        f"Strong stone `{trad}` on planet `{p_num}` must carry 'consult a qualified practitioner' caution."
                    )
            texts.extend([trad, caution, *[str(a) for a in alts]])
        elif rec.get("gemstone_info"):
            gem_info = str(rec["gemstone_info"])
            if "qualified practitioner" not in gem_info.lower():
                raise ValueError(f"Planet `{p_num}` gemstone_info missing practitioner caution.")
            texts.append(gem_info)

        if rec.get("affirmation"):
            texts.append(str(rec["affirmation"]))

        for txt in texts:
            if txt:
                violations = check_text_language_and_remedy_rules(txt)
                if violations:
                    raise ValueError(f"Planet `{p_num}` remedy entry failed safety check: {violations} in `{txt}`")

    elem_support = data.get("element_support")
    if elem_support is not None:
        for req_el in ("Wood", "Fire", "Earth", "Metal", "Water"):
            if req_el not in elem_support:
                raise ValueError(f"`element_support` missing `{req_el}`.")
            el_obj = elem_support[req_el]
            for h in el_obj.get("habits", []):
                violations = check_text_language_and_remedy_rules(str(h))
                if violations:
                    raise ValueError(f"`element_support.{req_el}` habit failed safety check: {violations}")


def validate_neighbour_relations_schema(data: Dict[str, Any]) -> None:
    """Validates directional ordered neighbour relation table (`A->B`) and pair meanings."""
    if not isinstance(data, dict):
        raise ValueError("Neighbour relations root must be a JSON object.")
    ordered = data.get("ordered_relations", {})
    if not isinstance(ordered, dict):
        raise ValueError("`ordered_relations` must be a dict mapping 'A->B' to friendly/neutral/enemy.")
    for k, rel in ordered.items():
        if not re.match(r"^[1-9]->[1-9]$", str(k)):
            raise ValueError(f"Invalid ordered pair key `{k}` (expected 'A->B' with digits 1-9).")
        if rel not in VALID_DIRECTIONAL_RELATIONS:
            raise ValueError(f"Invalid relation `{rel}` for `{k}` (expected friendly, neutral, or enemy).")

    meanings = data.get("pair_meanings", {})
    if not isinstance(meanings, dict):
        raise ValueError("`pair_meanings` must be a dict.")
    for pk, m_obj in meanings.items():
        if not re.match(r"^[1-9]-[1-9]$", str(pk)):
            raise ValueError(f"Invalid pair meaning key `{pk}` (expected 'A-B').")
        for field in ("summary", "positive", "shadow"):
            if m_obj.get(field):
                violations = check_text_language_and_remedy_rules(str(m_obj[field]))
                if violations:
                    raise ValueError(f"Pair meaning `{pk}.{field}` failed language check: {violations}")


# ============================================================================
# PLAIN-TEXT FILE LOADERS (Section 3c, 10, 14.B — all marked status="DRAFT")
# ============================================================================


def parse_key_value_blocks(raw_text: str) -> List[Dict[str, str]]:
    """
    Parses human-authored text blocks separated by blank lines or `---`.
    Lines inside a block use `Key: Value` format.
    """
    blocks: List[Dict[str, str]] = []
    chunks = re.split(r"\n\s*---+\s*\n|\n\s*\n(?=[A-Za-z0-9_ ]+\s*:)", str(raw_text or "").strip())
    for chunk in chunks:
        lines = [ln.strip() for ln in chunk.splitlines() if ln.strip() and not ln.strip().startswith("#")]
        if not lines:
            continue
        record: Dict[str, str] = {}
        current_key: Optional[str] = None
        for ln in lines:
            m = re.match(r"^([A-Za-z0-9_ /-]+)\s*:\s*(.*)$", ln)
            if m:
                current_key = m.group(1).strip().lower().replace(" ", "_").replace("-", "_")
                record[current_key] = m.group(2).strip()
            elif current_key:
                record[current_key] = (record[current_key] + " " + ln).strip()
        if record:
            blocks.append(record)
    return blocks


def load_driver_conductor_text(raw_text: str, source_tag: str = "OWNER_TEXT_IMPORT") -> List[Dict[str, Any]]:
    """
    Loads Driver x Conductor (`1-1` .. `9-9`, ordered: first=Driver, second=Conductor) blocks,
    softens harsh vocabulary, validates schema/safety, and marks every entry `DRAFT`.
    Expected block keys:
        pair: 8-2
        why: ...
        strengths / what_it_may_indicate: ...
        growth_edge / weaknesses: ...
        be_mindful_of: ...
        advice / steps: step 1 ; step 2
    """
    entries: List[Dict[str, Any]] = []
    for rec in parse_key_value_blocks(raw_text):
        pair_raw = rec.get("pair", "")
        m = re.match(r"^([1-9])\s*[-x/_]\s*([1-9])$", pair_raw)
        if not m:
            raise ValueError(f"Invalid Driver x Conductor pair `{pair_raw}` (expected 'D-C' with 1..9).")
        d, c = int(m.group(1)), int(m.group(2))
        why = soften_shadow_text(rec.get("why") or f"Driver {d} paired with Conductor {c}.")
        indicate = soften_shadow_text(rec.get("what_it_may_indicate") or rec.get("strengths") or "")
        growth = soften_shadow_text(rec.get("growth_edge") or rec.get("weaknesses") or "")
        mindful = soften_shadow_text(rec.get("be_mindful_of") or growth or "balance and steady pacing.")
        steps_raw = rec.get("advice") or rec.get("steps") or ""
        steps = [soften_shadow_text(s.strip()) for s in re.split(r";|\|", steps_raw) if s.strip()]
        if not steps:
            raise ValueError(f"Driver x Conductor `{d}-{c}` must include at least one constructive advice/step.")

        variant = {
            "why_this_shows": why,
            "what_it_may_indicate": indicate,
            "growth_edge": growth,
            "be_mindful_of": mindful,
            "gentle_steps_practical": steps,
        }
        entry = {
            "id": f"ind_dc_{d}_{c}_d1",
            "fact_signature": f"dc:{d}_{c}",
            "category": "dc",
            "theme": "pair_dynamic",
            "depth": int(rec.get("depth", "1")),
            "source_tag": source_tag,
            "status": "DRAFT",
            "touches_health_or_safety": rec.get("touches_health_or_safety", "false").lower() == "true",
            "language_variants": {"india": dict(variant), "international": dict(variant)},
        }
        entries.append(entry)

    validate_indication_library_schema(
        {
            "version": "1.0.0",
            "philosophy_line": "Numbers are a guide, not a compulsion.",
            "default_footer": "Numerology is a reflective guide, not a prediction.",
            "health_safety_line": "Traditional practice, in addition to medical care and sensible safety.",
            "entries": entries,
        }
    )
    return entries


def load_neighbour_relations_text(
    raw_text: str,
    *,
    directional: bool = True,
) -> Dict[str, Any]:
    """
    Loads directional (`A->B: friendly|neutral|enemy`) or symmetric (`A-B: ...`) neighbour
    relation lines plus optional pair meanings (`A-B | positive: ... | shadow: ...`),
    validates against Section 14 rules, and keeps status `DRAFT` until approved.
    """
    ordered_relations: Dict[str, str] = {}
    pair_meanings: Dict[str, Dict[str, str]] = {}

    for raw_line in str(raw_text or "").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        m_dir = re.match(r"^([1-9])\s*->\s*([1-9])\s*:\s*(friendly|neutral|enemy)\b(.*)$", line, re.IGNORECASE)
        if m_dir:
            a, b, rel = m_dir.group(1), m_dir.group(2), m_dir.group(3).lower()
            ordered_relations[f"{a}->{b}"] = rel
            if not directional:
                ordered_relations[f"{b}->{a}"] = rel
            continue

        m_sym = re.match(r"^([1-9])\s*-\s*([1-9])\s*:\s*(friendly|neutral|enemy)\b(.*)$", line, re.IGNORECASE)
        if m_sym:
            a, b, rel, rest = m_sym.group(1), m_sym.group(2), m_sym.group(3).lower(), m_sym.group(4)
            ordered_relations[f"{a}->{b}"] = rel
            ordered_relations[f"{b}->{a}"] = rel
            if rest and "|" in rest:
                parts = [p.strip() for p in rest.split("|") if p.strip()]
                meaning_obj: Dict[str, str] = {}
                for p in parts:
                    if ":" in p:
                        mk, mv = p.split(":", 1)
                        meaning_obj[mk.strip().lower()] = soften_shadow_text(mv.strip())
                if meaning_obj:
                    canon = f"{min(int(a), int(b))}-{max(int(a), int(b))}"
                    pair_meanings[canon] = meaning_obj
            continue

        m_meaning = re.match(r"^meaning\s+([1-9])\s*-\s*([1-9])\s*:\s*(.+)$", line, re.IGNORECASE)
        if m_meaning:
            a, b, rest = int(m_meaning.group(1)), int(m_meaning.group(2)), m_meaning.group(3)
            canon = f"{min(a, b)}-{max(a, b)}"
            meaning_obj = {}
            for p in [seg.strip() for seg in rest.split("|") if seg.strip()]:
                if ":" in p:
                    mk, mv = p.split(":", 1)
                    meaning_obj[mk.strip().lower()] = soften_shadow_text(mv.strip())
            pair_meanings[canon] = meaning_obj
            continue

        raise ValueError(f"Unrecognized neighbour relation line: `{line}`")

    result = {
        "version": "1.0.0",
        "status": "DRAFT",
        "directional": directional,
        "combining_rule": {
            "both_friendly": "supportive",
            "any_enemy": "tension",
            "otherwise": "balanced or one-sided support",
        },
        "ordered_relations": ordered_relations,
        "pair_meanings": pair_meanings,
    }
    validate_neighbour_relations_schema(result)
    return result


# ============================================================================
# MISSING CONTENT AUDIT REPORT (Section 10)
# ============================================================================


def generate_missing_content_report(
    indication_lib: Optional[Dict[str, Any]] = None,
    remedy_lib: Optional[Dict[str, Any]] = None,
    neighbour_rel: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Lists every empty `fact_signature` and every `DRAFT` (unapproved) entry across:
      - 81 Driver x Conductor ordered pairs (`dc:1_1` .. `dc:9_9`, calling out 6-6, 7-7, 8-8, 9-8, 9-9)
      - 9 missing digits (`missing_digit:1` .. `9`)
      - 9 repeated digits (`repeated_digit:1_x2` .. `9_x2`)
      - 8 planes (`plane:thought`, `will`, `action`, `mental`, `emotional`, `practical`, `golden_raj_yoga`, `silver_raj_yoga`)
      - Personal Year (`1..9`), Personal Month (`1..9`), Personal Day (`1..9`), `gap_meets_cycle:1..9`
      - Name numbers (`name_number:1..9`)
      - Compound number notes (`10, 13, 14, 16, 19`, `29`)
      - 20 grid neighbour pairs & 72 ordered directional relations (`A->B`)
      - 9 planet remedy packs (`1..9`)
    """
    ind_data = indication_lib or load_indication_library()
    rem_data = remedy_lib or load_remedy_library()
    nei_data = neighbour_rel or load_neighbour_relations()

    by_sig: Dict[str, List[Dict[str, Any]]] = {}
    for entry in ind_data.get("entries", []):
        by_sig.setdefault(entry["fact_signature"], []).append(entry)

    def _audit_sigs(expected_sigs: List[str]) -> Dict[str, List[str]]:
        empty: List[str] = []
        draft_only: List[str] = []
        approved: List[str] = []
        for sig in expected_sigs:
            matches = by_sig.get(sig, [])
            if not matches:
                empty.append(sig)
            elif any(m.get("status") == "APPROVED" for m in matches):
                approved.append(sig)
            else:
                draft_only.append(sig)
        return {"empty": empty, "draft_only": draft_only, "approved": approved}

    dc_sigs = [f"dc:{d}_{c}" for d in range(1, 10) for c in range(1, 10)]
    missing_sigs = [f"missing_digit:{d}" for d in range(1, 10)]
    repeated_sigs = [f"repeated_digit:{d}_x2" for d in range(1, 10)]
    commanding_sigs = [f"commanding_planet:{d}" for d in range(1, 10)]
    plane_sigs = [f"plane:{p['id']}" for p in LO_SHU_EIGHT_PLANES]
    py_sigs = [f"personal_year:{d}" for d in range(1, 10)]
    pm_sigs = [f"personal_month:{d}" for d in range(1, 10)]
    pd_sigs = [f"personal_day:{d}" for d in range(1, 10)]
    gap_sigs = [f"gap_meets_cycle:{d}" for d in range(1, 10)]
    name_sigs = [f"name_number:{d}" for d in range(1, 10)]
    compound_sigs = [f"compound_note:{n}" for n in (10, 13, 14, 16, 19, 29)]

    raw_rem_planets = rem_data.get("planets", [])
    top_rem_status = rem_data.get("meta", {}).get("status", "DRAFT")
    if isinstance(raw_rem_planets, list):
        remedy_planets = {str(p["number"]): p for p in raw_rem_planets}
    else:
        remedy_planets = raw_rem_planets

    remedy_approved = [
        p for p, pk in remedy_planets.items() if pk.get("status", top_rem_status) == "APPROVED"
    ]
    remedy_draft = [
        p for p, pk in remedy_planets.items() if pk.get("status", top_rem_status) != "APPROVED"
    ]
    remedy_missing_mantra = [
        p
        for p, pk in remedy_planets.items()
        if not (
            pk.get("mantra")
            or any(it.get("kind") == "mantra" and it.get("text") for it in pk.get("items", []))
        )
    ]

    ordered_rels = nei_data.get("ordered_relations", {})
    expected_directional = [f"{a}->{b}" for a in range(1, 10) for b in range(1, 10) if a != b]
    missing_directional = [k for k in expected_directional if k not in ordered_rels]

    report = {
        "production_ready_approved_entries_count": sum(
            1 for e in ind_data.get("entries", []) if e.get("status") == "APPROVED"
        ),
        "draft_placeholder_entries_count": sum(
            1 for e in ind_data.get("entries", []) if e.get("status") == "DRAFT"
        ),
        "driver_x_conductor_81": {
            **_audit_sigs(dc_sigs),
            "flagged_owner_completion_pairs": ["dc:6_6", "dc:7_7", "dc:8_8", "dc:9_8", "dc:9_9"],
        },
        "missing_digits_1_to_9": _audit_sigs(missing_sigs),
        "repeated_digits_1_to_9": _audit_sigs(repeated_sigs),
        "commanding_planets_1_to_9": _audit_sigs(commanding_sigs),
        "eight_planes": _audit_sigs(plane_sigs),
        "personal_year_1_to_9": _audit_sigs(py_sigs),
        "personal_month_1_to_9": _audit_sigs(pm_sigs),
        "personal_day_1_to_9": _audit_sigs(pd_sigs),
        "gap_meets_cycle_1_to_9": _audit_sigs(gap_sigs),
        "name_numbers_1_to_9": _audit_sigs(name_sigs),
        "compound_notes": _audit_sigs(compound_sigs),
        "neighbour_relations": {
            "status": nei_data.get("status"),
            "configured_directional_pairs_count": len(ordered_rels),
            "missing_directional_pairs_count": len(missing_directional),
            "pending_contradictions": nei_data.get("pending_contradictions", []),
        },
        "planet_remedy_packs_1_to_9": {
            "approved_planets": remedy_approved,
            "draft_planets": remedy_draft,
            "planets_missing_exact_mantra_text": remedy_missing_mantra,
        },
        "footer_status": ind_data.get("footer_status", "PLACEHOLDER_AWAITING_OWNER_APPROVAL"),
    }
    return report
