"""
app/engine/layer1_golden_snapshot.py
====================================
Deterministic Layer 1 surface extractor across all surfaces required by Sections 0, 2, 15 & 16:
  1. Free result page Layer 1 data
  2. Basic (3p), Advanced (12p), and Premium (32p) PDF extracted text & page SHA-256s
  3. Element counts, element gaps, and ranked element remedies
  4. Existing planet benefic/malefic & repetition evaluation outputs
  5. Existing 2027 Planner output
  6. Charm AI response contract & credit behaviour (in-process stubbed backend)
"""

import hashlib
import io
import json
import os
import re
from datetime import date
from pathlib import Path
from typing import Any, Dict, List

os.environ.setdefault("NV_DISABLE_LIVE_LLM", "true")

import pypdf

from app.engine.charm_oracle_synthesizer import classify_digit_degree
from app.engine.core_matrix_engine import (
    analyze_elements_balancing,
    analyze_repeat_numbers,
    assess_karmic_and_master,
)
from app.engine.digit_root import (
    calc_bhagyank,
    calc_driver,
    calc_loshu_dob_only,
    calc_personal_year,
)
from app.engine.kua import calculate_kua_details
from app.engine.rule_governance import rule_governance
from app.services.pdf_report_generator import CONTENT_LIB, generate_customised_pdf_report

GOLDEN_16_DOBS: List[Dict[str, Any]] = [
    {"id": "dob_01", "label": "Profile A", "day": 17, "month": 2, "year": 1963, "gender": "male"},
    {"id": "dob_02", "label": "Profile B", "day": 26, "month": 3, "year": 1980, "gender": "male"},
    {"id": "dob_03", "label": "Profile C", "day": 28, "month": 11, "year": 1981, "gender": "female"},
    {"id": "dob_04", "label": "Profile D", "day": 7, "month": 9, "year": 1980, "gender": "male"},
    {"id": "dob_05", "label": "Profile E", "day": 11, "month": 10, "year": 2011, "gender": "male"},
    {"id": "dob_06", "label": "Profile F", "day": 11, "month": 11, "year": 1981, "gender": "male"},
    {"id": "dob_07", "label": "Profile G", "day": 22, "month": 2, "year": 2002, "gender": "female"},
    {"id": "dob_08", "label": "Profile H", "day": 18, "month": 8, "year": 1980, "gender": "male"},
    {"id": "dob_09", "label": "Profile I", "day": 18, "month": 8, "year": 1988, "gender": "male"},
    {"id": "dob_10", "label": "Profile J", "day": 14, "month": 4, "year": 1944, "gender": "female"},
    {"id": "dob_11", "label": "Profile K", "day": 17, "month": 7, "year": 1970, "gender": "male"},
    {"id": "dob_12", "label": "Profile L", "day": 29, "month": 9, "year": 1999, "gender": "female"},
    {"id": "dob_13", "label": "Profile M", "day": 1, "month": 1, "year": 2000, "gender": "male"},
    {"id": "dob_14", "label": "Profile N", "day": 15, "month": 4, "year": 1996, "gender": "male"},
    {"id": "dob_15", "label": "Profile O", "day": 14, "month": 5, "year": 1986, "gender": "female"},
    {"id": "dob_16", "label": "Profile P", "day": 23, "month": 4, "year": 1985, "gender": "female"},
]

# Backward-compatible alias
GOLDEN_10_DOBS = GOLDEN_16_DOBS


def _norm_ws(text: str) -> str:
    return re.sub(r"\s+", " ", str(text or "")).strip()


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_ranked_5_element_remedies(counts: Dict[int, int], missing: List[int]) -> Dict[str, Any]:
    """Mirrors the exact existing Layer 1 5-Element Equilibrium & Ranked Habits logic."""
    wood_c = counts.get(3, 0) + counts.get(4, 0)
    fire_c = counts.get(9, 0)
    earth_c = counts.get(2, 0) + counts.get(5, 0) + counts.get(8, 0)
    metal_c = counts.get(6, 0) + counts.get(7, 0)
    water_c = counts.get(1, 0)

    def _state_and_remedy(elem_name: str, count: int):
        elem_data = CONTENT_LIB["topics"]["elements"][elem_name]["states"]
        if count == 0:
            return "Missing (0)", elem_data["missing"]["remedy"]
        if elem_name in ("Wood", "Earth", "Metal") and count == 1:
            return f"Low ({count})", elem_data["low"]["remedy"]
        if count > (3 if elem_name == "Earth" else 2):
            return f"Strong ({count})", elem_data["strong"]["remedy"]
        return f"Balanced ({count})", elem_data["balanced"]["remedy"]

    audit = {}
    for en, cv in (("Wood", wood_c), ("Fire", fire_c), ("Earth", earth_c), ("Metal", metal_c), ("Water", water_c)):
        st, rem = _state_and_remedy(en, cv)
        audit[en] = {"count": cv, "status": st, "remedy": rem}

    elem_counts = [
        ("Wood", wood_c, 3 in missing or 4 in missing),
        ("Fire", fire_c, 9 in missing),
        ("Earth", earth_c, 2 in missing or 5 in missing or 8 in missing),
        ("Metal", metal_c, 6 in missing or 7 in missing),
        ("Water", water_c, 1 in missing),
    ]
    ranked_elems = sorted(elem_counts, key=lambda x: (0 if x[2] else 1, x[1]))
    biggest_gap_elem = ranked_elems[0][0] if ranked_elems[0][2] else "Balanced"

    ranked_top3 = []
    for elem_name, c_val, is_gap in ranked_elems[:3]:
        rem_text = CONTENT_LIB["topics"]["elements"][elem_name]["states"][
            "missing" if is_gap else ("low" if c_val == 1 else "strong")
        ]["remedy"]
        ranked_top3.append(
            {
                "element": elem_name,
                "count": c_val,
                "has_open_digit": is_gap,
                "remedy": rem_text,
            }
        )

    return {
        "counts": {"Wood": wood_c, "Fire": fire_c, "Earth": earth_c, "Metal": metal_c, "Water": water_c},
        "audit": audit,
        "biggest_gap_element": biggest_gap_elem,
        "ranked_top3_remedies": ranked_top3,
    }


def extract_planet_repetition_snapshot(d: int, m: int, y: int, counts: Dict[int, int]) -> Dict[str, Any]:
    """Captures exact current planet repetition & benefic/malefic outputs (Section 2.b & 16.A)."""
    oracle_degrees = {}
    for dig in range(1, 10):
        c = counts.get(dig, 0)
        deg = classify_digit_degree(dig, c)
        oracle_degrees[str(dig)] = {
            "count": c,
            "degree": deg.get("degree"),
            "status": deg.get("status"),
            "narrative": deg.get("narrative"),
        }

    gov_eval = rule_governance.evaluate_grid_frequencies(counts)
    core_repeats = analyze_repeat_numbers(d, m, y)
    karmic_master = assess_karmic_and_master(d, m, y, "")

    return {
        "oracle_digit_degrees": oracle_degrees,
        "rule_governance_master_key_5_active": gov_eval.get("master_key_5_active"),
        "rule_governance_evaluations": {
            str(k): {
                "status": v.get("status"),
                "degree": v.get("degree"),
            }
            for k, v in gov_eval.get("digit_evaluations", {}).items()
        },
        "core_matrix_repeat_numbers": [
            {
                "number": item["number"],
                "frequency": item["frequency"],
                "planet": item["planet"],
                "type": item["type"],
            }
            for item in core_repeats.get("evaluations", [])
        ],
        "karmic_and_master_notes": karmic_master,
    }


def extract_pdf_pages_snapshot(
    label: str,
    day: int,
    month: int,
    year: int,
    gender: str,
    tier: str,
    include_full_text: bool = True,
) -> Dict[str, Any]:
    pdf_bytes, _ = generate_customised_pdf_report(
        name=label,
        day=day,
        month=month,
        year=year,
        tier=tier,
        gender=gender,
        purchase_year=2026,
        edition="india",
    )
    reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    pages_norm = [_norm_ws(pg.extract_text() or "") for pg in reader.pages]
    out: Dict[str, Any] = {
        "page_count": len(pages_norm),
        "pages_sha256": [_sha256(t) for t in pages_norm],
    }
    if include_full_text:
        out["pages_text"] = pages_norm
    return out


def capture_single_dob_snapshot(rec: Dict[str, Any]) -> Dict[str, Any]:
    from app.charm.chat.response_composer import charm_chat_orchestrator
    from app.engine.enhanced_lo_shu_engine import build_birth_date_grid
    from app.engine.lo_shu import analyze_lo_shu_grid
    from app.engine.planner_2027_engine import calculate_planner_2027

    d, m, y = rec["day"], rec["month"], rec["year"]
    gender = rec["gender"]
    label = rec["label"]

    # 1. Free result page Layer 1 data
    loshu_dob = calc_loshu_dob_only(d, m, y)
    kua_det = calculate_kua_details(y, gender)
    free_surface = {
        "driver": calc_driver(d),
        "conductor": calc_bhagyank(d, m, y),
        "kua": kua_det["kua_number"],
        "kua_display": kua_det["display"],
        "personal_year_2026": calc_personal_year(d, m, 2026),
        "loshu_counts": {str(k): v for k, v in loshu_dob["counts"].items()},
        "present_digits": loshu_dob["present"],
        "missing_digits": loshu_dob["missing"],
        "repeated_digits": {str(k): v for k, v in loshu_dob["repeated"].items()},
        "planes": {
            pid: {"fraction": p["fraction"], "is_complete": p["is_complete"]}
            for pid, p in loshu_dob["planes"].items()
        },
    }

    # 2. Element balancing Layer 1 outputs
    core_elem = analyze_elements_balancing(d, m, y)
    loshu_classic = analyze_lo_shu_grid(d, m, y)
    enhanced_grid = build_birth_date_grid(d, m, y)
    ranked_5_elem = extract_ranked_5_element_remedies(loshu_dob["counts"], loshu_dob["missing"])
    element_surface = {
        "core_matrix_elements": core_elem,
        "lo_shu_grid_counts": {str(k): v for k, v in loshu_classic["digit_counts"].items()},
        "lo_shu_completed_planes": loshu_classic["completed_planes"],
        "enhanced_grid_missing": enhanced_grid["missing_numbers"],
        "enhanced_grid_repeated": {str(k): v for k, v in enhanced_grid["repeated_numbers"].items()},
        "ranked_5_element_remedies": ranked_5_elem,
    }

    # 3. Existing Planet Repetition & Benefic/Malefic logic snapshot
    planet_logic_surface = extract_planet_repetition_snapshot(d, m, y, loshu_dob["counts"])

    # 4. PDFs (Basic 3p full text for all 16; Advanced 12p & Premium 32p hashes for all 16 + full text on first 2)
    keep_full_heavy = rec["id"] in ("dob_01", "dob_02")
    pdf_surface = {
        "basic_3p": extract_pdf_pages_snapshot(label, d, m, y, gender, "basic", include_full_text=True),
        "advanced_12p": extract_pdf_pages_snapshot(
            label, d, m, y, gender, "advanced", include_full_text=keep_full_heavy
        ),
        "premium_32p": extract_pdf_pages_snapshot(
            label, d, m, y, gender, "premium", include_full_text=keep_full_heavy
        ),
    }

    # 5. Existing 2027 Planner output
    dob_iso = f"{y:04d}-{m:02d}-{d:02d}"
    planner_res = calculate_planner_2027(full_name=label, dob_str=dob_iso)
    cal_by_date = {row["date"]: row for row in planner_res["full_calendar_365"]}
    sample_dates = ("2027-01-01", "2027-05-15", "2027-09-15", "2027-12-31")
    sample_scores = {
        d_iso: {
            "alignment_score": cal_by_date[d_iso]["alignment_score"],
            "tier": cal_by_date[d_iso]["tier"],
        }
        for d_iso in sample_dates
    }
    planner_surface = {
        "driver_mulank": planner_res["subject"]["driver_mulank"],
        "conductor_bhagyank": planner_res["subject"]["conductor_bhagyank"],
        "personal_year_2027": planner_res["subject"]["personal_year_2027"],
        "dob_digit_counts": {str(k): v for k, v in planner_res["dob_digit_counts"].items()},
        "tier_counts": planner_res["tier_counts"],
        "months_pm": [
            {
                "month_number": mo["month_number"],
                "month_name": mo["month_name"],
                "personal_month": mo["personal_month"],
                "average_alignment_score": mo["average_alignment_score"],
            }
            for mo in planner_res["months"]
        ],
        "sample_day_scores": sample_scores,
    }

    # 6. Charm AI response contract (stubbed deterministic turn)
    charm_turn = charm_chat_orchestrator.process_chat_turn(
        message="What does my career rhythm look like this year?",
        user_name="",
        day=d,
        month=m,
        year=y,
        conversation_id=f"SNAP-{rec['id']}",
        user_id=f"anon_snap_{rec['id']}",
    )
    charm_dump = charm_turn.model_dump()
    charm_surface = {
        "status": charm_dump["status"],
        "has_assistant_message_text": bool(charm_dump.get("assistant_message", {}).get("text")),
        "headline": charm_dump.get("human_friendly_summary", {}).get("headline", ""),
        "practical_next_steps_count": len(charm_dump.get("practical_next_steps", [])),
        "follow_up_question": charm_dump.get("follow_up_question", ""),
    }

    return {
        "meta": rec,
        "free_result_page": free_surface,
        "element_balancing": element_surface,
        "planet_repetition_logic": planet_logic_surface,
        "pdfs": pdf_surface,
        "planner_2027": planner_surface,
        "charm_ai": charm_surface,
    }


def capture_all_16_golden_snapshots() -> Dict[str, Any]:
    prev_flag = os.environ.get("NV_ENABLE_LAYERS_2_3")
    os.environ["NV_ENABLE_LAYERS_2_3"] = "0"
    try:
        records = [capture_single_dob_snapshot(rec) for rec in GOLDEN_16_DOBS]
    finally:
        if prev_flag is None:
            os.environ.pop("NV_ENABLE_LAYERS_2_3", None)
        else:
            os.environ["NV_ENABLE_LAYERS_2_3"] = prev_flag
    return {
        "version": "1.1.0",
        "flag_state_when_captured": "OFF",
        "dob_count": len(records),
        "snapshots": records,
    }


# Backward-compatible alias
capture_all_10_golden_snapshots = capture_all_16_golden_snapshots


if __name__ == "__main__":
    out_path = Path(__file__).resolve().parents[2] / "tests" / "fixtures" / "layer1_golden_snapshots_16_dobs.json"
    snap = capture_all_16_golden_snapshots()
    out_path.write_text(json.dumps(snap, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote {snap['dob_count']} golden snapshots to {out_path} ({out_path.stat().st_size} bytes)")
