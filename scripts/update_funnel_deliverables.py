with open("app/static/js/funnel_journey.js", "r", encoding="utf-8") as f:
    text = f.read()

replacements = [
    ("'12-15 Page Executive PDF Dossier'", "'3-Page Executive PDF Dossier'"),
    ("'35-40 Page Master Synthesis Dossier'", "'12-Page Master Synthesis Dossier'"),
]

for old, new in replacements:
    assert old in text, f"Missing {old}"
    text = text.replace(old, new, 1)

with open("app/static/js/funnel_journey.js", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated funnel_journey.js deliverables successfully!")
