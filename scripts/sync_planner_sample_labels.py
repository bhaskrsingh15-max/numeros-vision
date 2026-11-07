"""
NUMEROS VISION — SYNC PLANNER SAMPLE LABELS FROM GOLDEN SHEETS
==============================================================
Reads tests/golden_sheets.json and generates canonical sample labels
for the 2027 Year Ahead Planner sales page.
"""

import os
import json
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GOLDEN_PATH = os.path.join(ROOT, "tests", "golden_sheets.json")
HTML_PATH = os.path.join(ROOT, "app", "static", "year_2027.html")

def get_sample_labels():
    with open(GOLDEN_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    a = data["A"]
    b = data["B"]
    
    name_a = a["name"].title()
    label_a = f"Sample A: {name_a} (Mulank {a['mulank']}, Bhagyank {a['bhagyank']}, Personal Year {a['personal_year_2027']})"
    
    name_b = b["name"].title()
    label_b = f"Sample B: {name_b} (Mulank {b['mulank']}, Bhagyank {b['bhagyank']}, Personal Year {b['personal_year_2027']})"
    
    return label_a, label_b

if __name__ == "__main__":
    label_a, label_b = get_sample_labels()
    print(f"Sample A: {label_a}")
    print(f"Sample B: {label_b}")
