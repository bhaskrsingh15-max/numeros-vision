# -*- coding: utf-8 -*-
import os
import re

files = [
    os.path.join("app", "static", "js", "number_characteristics.js"),
    os.path.join("dist_cloudflare_pages", "js", "number_characteristics.js"),
    os.path.join("dist_cloudflare_pages", "static", "js", "number_characteristics.js")
]

for p in files:
    if not os.path.exists(p):
        continue
    with open(p, "r", encoding="utf-8") as f:
        text = f.read()

    # Clean subdate title
    text = text.replace(
        "${subdate.strength_title ? `${subdate.strength_title} · Day ${birthDay}` : `Day ${birthDay}: The Innate Self`}",
        "${subdate.archetype ? `${subdate.archetype} · Day ${birthDay}` : `Day ${birthDay}: Innate Character`}"
    )

    # Clean planetary composition
    text = text.replace(
        "Planetary Harmony: <strong>${subdate.planetary_composition || 'Natural Planetary Resonance'}</strong>",
        "Planetary Essence: <strong>${(subdate.planetary_composition || 'Natural Planetary Resonance').replace(/\\\\(.*?Clash.*?\\\\)/g, '').replace(/\\\\(.*?Tension.*?\\\\)/g, '').trim()}</strong>"
    )

    with open(p, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Updated {p}")
