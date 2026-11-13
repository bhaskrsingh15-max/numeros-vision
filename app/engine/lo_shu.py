from typing import Dict, Any, List
from app.engine.rag_retriever import rag_engine
from app.engine.rule_governance import rule_governance, RuleStatus
from app.engine.kua import (
    KUA_NEEDS_GENDER_TEXT,
    KUA_RULE_TEXT,
    calculate_kua_details,
    calculate_kua_number,
)

# Standard Lo Shu Grid positions
LO_SHU_GRID_TEMPLATE = [
    [4, 9, 2],
    [3, 5, 7],
    [8, 1, 6]
]

PLANES = {
    "Mental Plane (4-9-2)": [4, 9, 2],
    "Emotional Plane (3-5-7)": [3, 5, 7],
    "Practical Plane (8-1-6)": [8, 1, 6],
    "Thought Plane (4-3-8)": [4, 3, 8],
    "Will Plane (9-5-1)": [9, 5, 1],
    "Action Plane (2-7-6)": [2, 7, 6],
    "Golden Success Plane (4-5-6)": [4, 5, 6],
    "Silver Success Plane (2-5-8)": [2, 5, 8]
}

def analyze_lo_shu_grid(day: int, month: int, year: int) -> Dict[str, Any]:
    """
    Performs deterministic Lo Shu Grid construction and frequency counting.
    Grounds repetition analysis against the Day 7 Governed Rule Catalogue.
    """
    dob_str = f"{day:02d}{month:02d}{year}"
    digits = [int(d) for d in dob_str if d != '0']
    
    # Grid counts for numbers 1..9
    digit_counts = {num: digits.count(num) for num in range(1, 10)}
    
    # Check completed planes
    completed_planes = []
    incomplete_planes = []
    for plane_name, required_digits in PLANES.items():
        if all(digit_counts[d] > 0 for d in required_digits):
            completed_planes.append(plane_name)
        else:
            incomplete_planes.append(plane_name)

    missing_numbers = [num for num, count in digit_counts.items() if count == 0]
    present_numbers = [num for num, count in digit_counts.items() if count > 0]

    # Grounded RAG search for remedies on missing numbers
    remedy_passages = []
    if missing_numbers:
        missing_query = f"Missing numbers {' '.join(str(n) for n in missing_numbers)} remedies Lo Shu grid"
        remedy_passages = rag_engine.query(missing_query, top_k=3)

    # Day 7 Governed Repetition & Attribute Evaluation
    governed_evaluation = rule_governance.evaluate_grid_frequencies(digit_counts)

    return {
        "digit_counts": digit_counts,
        "grid_matrix": [
            [digit_counts[4], digit_counts[9], digit_counts[2]],
            [digit_counts[3], digit_counts[5], digit_counts[7]],
            [digit_counts[8], digit_counts[1], digit_counts[6]]
        ],
        "present_numbers": present_numbers,
        "missing_numbers": missing_numbers,
        "completed_planes": completed_planes,
        "incomplete_planes": incomplete_planes,
        "numeros_vision_remedies": remedy_passages,
        "repetition_analysis": governed_evaluation["evaluations"],
        "governed_rules_applied": True,
        "governance_version": governed_evaluation["governance_version"],
        "source_authority": governed_evaluation["source_authority"]
    }

def generate_loshu_grid_markdown(day: int, month: int, year: int) -> str:
    """
    Renders an authoritative, beautifully formatted ASCII Lo Shu Grid birth chart
    with elemental frequencies, repetition tiers, missing karmic voids, and completed planes.
    """
    grid_data = analyze_lo_shu_grid(day, month, year)
    counts = grid_data["digit_counts"]
    repetition_info = grid_data.get("repetition_analysis", {})
    
    def cell(num: int, elem: str) -> str:
        cnt = counts.get(num, 0)
        disp = f"{num} (x{cnt})" if cnt > 0 else "GAP"
        return f"{num} ({elem}): {disp}"

    c4 = cell(4, "Wood")
    c9 = cell(9, "Fire")
    c2 = cell(2, "Earth")
    c3 = cell(3, "Wood")
    c5 = cell(5, "Earth")
    c7 = cell(7, "Metal")
    c8 = cell(8, "Earth")
    c1 = cell(1, "Water")
    c6 = cell(6, "Metal")

    present_str = ", ".join(str(n) for n in grid_data["present_numbers"]) or "None"
    missing_str = ", ".join(str(n) for n in grid_data["missing_numbers"]) if grid_data["missing_numbers"] else "None (Complete Matrix)"
    completed_str = ", ".join(grid_data["completed_planes"]) if grid_data["completed_planes"] else "None (Requires remedial grounding)"
    
    # Documented Day 7 Repetition Tiers
    rep_md = []
    for num_str, info in repetition_info.items():
        freq = info.get("frequency", 0)
        if freq > 0:
            cat = info.get("repetition_category")
            attr = info.get("attribute", "")
            elem = info.get("element", "")
            rep_md.append(f"  • **Number {num_str} ({attr} · {elem}):** {freq} occurrence(s) → **{cat}** [{info.get('rule_id')}]")

    repetition_section = "\n".join(rep_md) if rep_md else "  • No active frequencies."

    gap_descriptions = {
        1: "Missing 1 (Water · Career & Initiative): Difficulty asserting individuality; hesitation in taking decisive leadership leaps.",
        2: "Missing 2 (Earth · Intuition & Partnership): Emotional impatience; relationship friction; feeling ungrounded in team dynamics.",
        3: "Missing 3 (Wood · Knowledge & Expression): Creative stagnation; public expression hesitation; under-leveraging personal expertise.",
        4: "Missing 4 (Wood · Rahu Vault & Discipline): Structural wealth leak; high revenue struggles to convert into permanent physical assets.",
        5: "Missing 5 (Earth · Cosmic Center / Brahmasthan): Severe instability in focus; career restlessness; emotional oscillation during stress.",
        6: "Missing 6 (Metal · Venus Luxury Vibration): Delayed comfort manifestation; working hard but experiencing friction in family harmony.",
        7: "Missing 7 (Metal · Ketu Wisdom & Research): Repeating old mistakes; feeling spiritually disconnected; lack of deep analytical anchoring.",
        8: "Missing 8 (Earth · Saturn Discipline & Perseverance): Impatience with long-term execution; episodic financial disruptions.",
        9: "Missing 9 (Fire · Mars Energy & Vitality): Low physical momentum; reluctance to stand in the spotlight; courage and drive void."
    }

    gaps_md = []
    for m in grid_data["missing_numbers"]:
        eval_res = rule_governance.get_missing_number_evaluation(m)
        elem = eval_res.get("element", "Unknown")
        impact = eval_res.get("impact", "")
        poorak = eval_res.get("poorak_complimentary_numbers", [])
        poorak_str = f" [Complimentary Poorak: {', '.join(str(p) for p in poorak)}]" if poorak else ""
        elem_rem = eval_res.get("element_remedy")
        yantra_rem = eval_res.get("yantra_remedy")
        
        rem_str = f" | Remedy: {elem_rem}" if elem_rem else ""
        if yantra_rem:
            rem_str += f" | Yantra: {yantra_rem}"
        
        gaps_md.append(f"  • **Missing {m} ({elem} Element):** {impact}{poorak_str}{rem_str}")

    gaps_section = "\n".join(gaps_md) if gaps_md else "  • All 9 single-digit numerical frequencies grounded in natal birth matrix."

    planes_md = []
    if 4 in grid_data["missing_numbers"] or 5 in grid_data["missing_numbers"] or 6 in grid_data["missing_numbers"]:
        planes_md.append("  • **Golden Prosperity Plane (4-5-6) Incomplete:** Revenue enters through Driver/Conductor but leaks before compounding.")
    if 2 in grid_data["missing_numbers"] or 5 in grid_data["missing_numbers"] or 8 in grid_data["missing_numbers"]:
        planes_md.append("  • **Silver Success Plane (2-5-8) Incomplete:** Periodic delays in property, real estate acquisitions and emotional grounding.")
    if 9 in grid_data["missing_numbers"] or 5 in grid_data["missing_numbers"] or 1 in grid_data["missing_numbers"]:
        planes_md.append("  • **Will & Persistence Plane (9-5-1) Disrupted:** Difficulty finishing ambitious multi-year projects.")

    planes_section = ("\n" + "\n".join(planes_md)) if planes_md else ""

    markdown = (
        f"### 🔲 Natal Lo Shu Grid Birth Chart ({day:02d}-{month:02d}-{year})\n\n"
        f"```\n"
        f"┌──────────────────────┬──────────────────────┬──────────────────────┐\n"
        f"│ {c4:<20} │ {c9:<20} │ {c2:<20} │\n"
        f"├──────────────────────┼──────────────────────┼──────────────────────┤\n"
        f"│ {c3:<20} │ {c5:<20} │ {c7:<20} │\n"
        f"├──────────────────────┼──────────────────────┼──────────────────────┤\n"
        f"│ {c8:<20} │ {c1:<20} │ {c6:<20} │\n"
        f"└──────────────────────┴──────────────────────┴──────────────────────┘\n"
        f"```\n\n"
        f"**✦ Natal Birth Chart Distribution:**\n"
        f"• **Present Elemental Frequencies:** [ {present_str} ]\n"
        f"• **Karmic Missing Digits (Gaps):** [ {missing_str} ]\n"
        f"• **Completed Elemental Planes:** {completed_str}\n\n"
        f"**✦ Governed Repetition Framework (Day 7 Verified Rules):**\n"
        f"{repetition_section}\n\n"
        f"**✦ Karmic Gap & Elemental Diagnosis:**\n"
        f"{gaps_section}"
        f"{planes_section}\n"
    )
    return markdown

if __name__ == "__main__":
    res = analyze_lo_shu_grid(15, 8, 1995)
    print("Lo Shu Grid Analysis:")
    print("Grid Counts:", res["digit_counts"])
    print("Repetition Analysis:", res["repetition_analysis"]["5"])
    print("Governed applied:", res["governed_rules_applied"])
