with open("app/api/payments.py", "r", encoding="utf-8") as f:
    text = f.read()

# Replace page counts in report_essential, report_master, report_divine
replacements = [
    ('"12-15 Page Executive PDF Report"', '"3-Page Executive PDF Report"'),
    ('basic Lo Shu 3x3 Grid, 1-year snapshot & primary color/gemstone guide', '3-page core overview: Driver & Conductor, Lo Shu 3x3 Grid, 1-year snapshot & primary gemstone guide'),
    ('"35-40 Page Master Synthesis Dossier"', '"12-Page Master Synthesis Dossier"'),
    ('Complete 35+ Page Dual-System Blueprint', 'Complete 12-Page Dual-System Blueprint'),
    ('"55-65 Page Sovereign Executive Blueprint"', '"32-Page Sovereign Executive Blueprint"'),
    ('Comprehensive 55+ Page Sovereign Blueprint', 'Comprehensive 32-Page Sovereign Blueprint'),
]

for old, new in replacements:
    assert old in text, f"Missing: {old}"
    text = text.replace(old, new, 1)

with open("app/api/payments.py", "w", encoding="utf-8") as f:
    f.write(text)

print("Updated app/api/payments.py with exact 3, 12, 32 page specifications!")
