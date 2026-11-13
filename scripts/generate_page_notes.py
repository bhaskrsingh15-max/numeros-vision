import os

books = [
    ("B1_you_and_your_name", "B1", "Numeros Vision Classical Sound and Name Compendium (2005)", 188, False, "Chaldean name numerology, sound and vibration rationale."),
    ("B2_chaldean_numerology", "B2", "Chaldean Numerology: Structured Learning Reference", 133, True, "Chaldean method with explicit comparisons to Pythagorean; 31-section index."),
    ("B3_chinese_numerology", "B3", "Numeros Vision Classical Nine-Square Lo Shu System (1998)", 276, False, "Chinese Lo Shu numerology, 3x3 Magic Square."),
    ("B4_numbers_meaning_magic", "B4", "Numeros Vision Planetary and Number Symbolism Archive", 116, False, "Historical esoteric symbolism and planetary associations."),
    ("B5_numerology_magic_numbers", "B5", "Numeros Vision Classical Numerology Manual (1945 Edition)", 200, False, "Historical mid-20th-century numerological treatment."),
    ("B6_understanding_numerology", "B6", "Understanding Numerology: The Power to Know Anybody", 148, False, "General modern introductory numerology.")
]

for folder, bid, title, pages, has_text, domain in books:
    bdir = os.path.join("knowledge", "books", folder)
    os.makedirs(bdir, exist_ok=True)
    fpath = os.path.join(bdir, "page_notes.md")
    
    status_text = "YES_SEARCHABLE" if has_text else "NO_IMAGE_SCAN"
    
    lines = [
        f"# {bid}: {title}",
        f"**Source ID**: `{bid}`  ",
        f"**Total PDF Pages**: {pages}  ",
        f"**Domain**: {domain}  ",
        f"**Text Status**: `{status_text}`  ",
        f"**Review Status**: `needs_review`  ",
        "",
        "## 1. Verified Source Observations",
    ]
    if bid == "B2":
        lines.extend([
            "- 31-Section Index Verified from machine-readable text layer:",
            "  1. Power of Numbers | 2. Chaldean Method | 3. Chaldean vs Pythagorean | 4. Meaning of Numbers",
            "  5. Core Numbers | 6. Birthdays | 7. Alphabet Mapping (A=1..Z=7, 9 excluded) | 8. Life Path",
            "  9. Growth Number | 10. Expression | 11. Single and Compound Numbers | 12. Heart Desire",
            "  13. Personality | 14. Maturity | 15. Attitude | 16. Balance | 17. Karmic Lessons",
            "  18. Challenges | 19. Home Number | 20. Hidden Passion | 21. Signature | 22-24. Personal Cycles",
            "  25-27. Pinnacles & Triple Cycles | 28-31. Practice Sheets & Aspects.",
            "- Compound totals (10-52+) are retained as meaningful vibration layers, not reduced immediately.",
            "- Calculation logic is deterministic and separate from interpretive prose."
        ])
    elif bid == "B3":
        lines.extend([
            "- Cover verified with 3x3 Lo Shu grid: 4-9-2 / 3-5-7 / 8-1-6.",
            "- Introductory pages describe Lo Shu chart construction, 8 planes, personal cycles, and arrows of strength/weakness."
        ])
    else:
        lines.extend([
            "- Scanned volume; title and introductory front matter verified from accessible cover/title pages.",
            "- Full body text is image-scanned; machine-readable text layer is not present."
        ])
    
    lines.extend([
        "",
        f"## 2. Page Review Register (Pages 1 to {pages})",
        "",
        "| Page Range | Content / Scope | OCR Confidence | Source Fidelity | Review Status | Notes |",
        "| :--- | :--- | :--- | :--- | :--- | :--- |"
    ])
    
    # Chunk into 10-page or section blocks for honest, structured tracking
    step = 10
    for p in range(1, pages + 1, step):
        p_end = min(p + step - 1, pages)
        rng = f"pp. {p}–{p_end}"
        if has_text:
            notes = "Digital text available; detailed semantic extraction and citation audit pending"
            ocr_conf = "High (Digital)"
        else:
            notes = "Scanned page; OCR verification pending — blocked from production RAG retrieval"
            ocr_conf = "Pending (Image)"
        lines.append(f"| {rng} | General Section Content | {ocr_conf} | High | `needs_review` | {notes} |")
    
    with open(fpath, "w", encoding="utf-8") as fp:
        fp.write("\n".join(lines) + "\n")
    print(f"Wrote {fpath}")
