# -*- coding: utf-8 -*-
import json
import os

path = os.path.join("app", "data", "birth_subdates_registry.json")
with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Clean 28
if "28" in data:
    data["28"]["planetary_composition"] = "Moon (2) + Saturn (8) = 10 -> 1 (Intuitive Depth & Enduring Discipline)"
    data["28"]["strength_title"] = "The Tested Strategist · Enduring Mastery"

# Clean 18
if "18" in data:
    data["18"]["planetary_composition"] = "Sun (1) + Saturn (8) = 9 (Vision & Resilience)"
    data["18"]["strength_title"] = "The Purposeful Warrior · Noble Perseverance"
    if "charm_ai_dialogue" in data["18"]:
        data["18"]["charm_ai_dialogue"] = (
            "Day 18 brings you the mantle of the Purposeful Warrior. Sun (1) and Saturn (8) unite into Mars (9), "
            "forging immense stamina and noble perseverance. Choose your battles with wisdom, and your battle-tested leadership will triumph."
        )

# Clean all strength_title across all days 1-31 to ensure no Category A/B/C/D labels leak
for k, v in data.items():
    if isinstance(v, dict) and "strength_title" in v:
        title = v["strength_title"]
        if "Category " in title:
            # e.g. "Category C - Lower Strength (Tested Strategist / High Friction)" -> "The Tested Strategist · Enduring Mastery"
            clean = title.split("(", 1)[-1].replace(")", "").replace("Category ", "").strip()
            if "/" in clean:
                clean = clean.split("/")[0].strip()
            v["strength_title"] = clean

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("SUCCESS: birth_subdates_registry.json sanitized.")
