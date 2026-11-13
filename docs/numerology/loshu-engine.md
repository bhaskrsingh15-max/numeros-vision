# Numeros Vision — Lo Shu Core Engine Contract
**Document Type:** Engine Specification
**Engine Module:** `app/engine/lo_shu.py` & `app/engine/enhanced_lo_shu_engine.py`

## 1. Canonical 3x3 Grid Arrangement
```text
+---+---+---+
| 4 | 9 | 2 |
+---+---+---+
| 3 | 5 | 7 |
+---+---+---+
| 8 | 1 | 6 |
+---+---+---+
```

## 2. Invariants & Calculation Rules
- **Digit Extraction:** All non-zero digits from Day, Month, and Year are placed into the grid.
- **Handling of Zero:** 0 is treated as a neutral cosmic void/potential; it is not placed in the 1-9 cells.
- **Counts:** Each number 1-9 has an exact frequency count. Absence (count = 0) indicates a missing planetary void; count = 1 indicates baseline presence; count = 2 indicates intensified strength; count >= 3 indicates concentrated intensity requiring grounding.
- **Planes of Expression:**
  - Horizontal: Mental (4-9-2), Emotional (3-5-7), Practical (8-1-6).
  - Vertical: Thought/Planning (4-3-8), Willpower (9-5-1), Action/Execution (2-7-6).
  - Diagonal: Golden Success (4-5-6), Silver Determination (2-5-8).
