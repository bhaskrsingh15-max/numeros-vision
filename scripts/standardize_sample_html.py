import os
import re

sample_path = 'app/static/sample.html'

with open(sample_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Format Switcher labels in JavaScript
text = text.replace(
    "brief: 'Format 1 (Executive Brief - 3 Pgs)',",
    "brief: 'Format 1: Foundational Blueprint (3 Pages)',"
)
text = text.replace(
    "master: 'Format 2 (Master Dossier - 12 Pgs)',",
    "master: 'Format 2: Master Dossier (12 Pages)',"
)
text = text.replace(
    "roadmap: 'Format 3 (Sovereign Blueprint - 32 Pgs / 21 Pgs)'",
    "roadmap: 'Format 3: Divine Sovereign Roadmap (32 Pages)'"
)

# 2. Update format switcher card HTML badges & descriptions
text = text.replace(
    '<div class="fmt-badge" style="background:rgba(201,162,39,0.15); color:#8B6914;">Format 1 · Free Discovery Preview</div>',
    '<div class="fmt-badge" style="background:rgba(201,162,39,0.15); color:#8B6914;">Format 1 · 3 Pages (Basic / Free)</div>'
)
text = text.replace(
    '<div class="fmt-name">Free Discovery Preview (Gated)</div>',
    '<div class="fmt-name">Foundational Blueprint (3 Pages)</div>'
)
text = text.replace(
    'Free Gated Teaser ➔',
    'View 3-Page Blueprint ➔'
)

text = text.replace(
    '<div class="fmt-badge" id="badgeFmt2">Format 2 · 12 Pages (Master)</div>',
    '<div class="fmt-badge" id="badgeFmt2">Format 2 · 12 Pages (Master)</div>'
)
text = text.replace(
    '<div class="fmt-name">Master Dual-System Dossier (12 Pages)</div>',
    '<div class="fmt-name">Master Numerology Dossier (12 Pages)</div>'
)

text = text.replace(
    'Format 3 · 21+ Pgs (Sovereign)',
    'Format 3 · 32 Pages (Sovereign)'
)
text = text.replace(
    'Sovereign Life-Path Roadmap (Full)',
    'Divine Sovereign Roadmap (32 Pages)'
)
text = text.replace(
    'Uncensored, hyper-detailed lifetime compendium: all 81 combos, full Vedic remedies, 10-yr radar, gemstone chemistry & master synastry.',
    'Full 32-page sovereign compendium: 30 standardized sections, Lo Shu matrix, 8 planes, 10-yr Dasha radar, personal calendar, sacred Yantras & mantras.'
)

# 3. Replace "Ch 0X" and "Ch X" in generateFormat2Pages
ch_replacements = [
    ("renderPageHeader('Ch 01 · Celestial Genesis')", "renderPageHeader('Section 01 · Celestial Genesis & Identity')"),
    ("renderPageHeader('Ch 02 · The Dual Pillars')", "renderPageHeader('Section 02 · Driver & Conductor Dual Pillars')"),
    ("renderPageHeader('Ch 03 · Cosmic Synergy')", "renderPageHeader('Section 03 · 81-Pair Cosmic Synergy Matrix')"),
    ("renderPageHeader('Ch 04 · Lo Shu Matrix')", "renderPageHeader('Section 04 · Natal Lo Shu Grid & 8 Planes')"),
    ("renderPageHeader('Ch 05 · Harmonized Remedies')", "renderPageHeader('Section 05 · Planetary Harmonization Remedies')"),
    ("renderPageHeader('Ch 06 · Name Vibration')", "renderPageHeader('Section 06 · Chaldean & Pythagorean Name Vibration')"),
    ("renderPageHeader('Ch 07 · Holistic Health')", "renderPageHeader('Section 07 · Health & Ayurvedic Chronobiology')"),
    ("renderPageHeader('Ch 08 · Career Blueprint')", "renderPageHeader('Section 08 · Career & Enterprise Roadmap')"),
    ("renderPageHeader('Ch 09 · Annual Cycle')", "renderPageHeader('Section 09 · Personal Year Calculator & 12 Months')"),
    ("renderPageHeader('Ch 10 · Angelic & Vastu Alignment')", "renderPageHeader('Section 10 · Spatial Vastu & Kua Vectors')"),
    ("renderPageHeader('Ch 11 · Mobile Frequency')", "renderPageHeader('Section 11 · Mobile & Digital Frequency Calibration')"),
    ("renderPageHeader('Ch 12 · Spiritual Alignment')", "renderPageHeader('Section 12 · Sacred Yantras & Sanskrit Mantras')"),
    ("Ch 1: Celestial Genesis & Identity", "Section 1: Celestial Genesis & Identity"),
    ("Ch 2: Driver & Conductor Dual Pillars", "Section 2: Driver & Conductor Dual Pillars"),
    ("Ch 3: 81-Pair Cosmic Synergy Matrix", "Section 3: 81-Pair Cosmic Synergy Matrix"),
    ("Ch 4: Sacred Lo Shu Grid & 8 Planes", "Section 4: Sacred Lo Shu Grid & 8 Planes"),
    ("Ch 5: Planetary Harmonization Remedies", "Section 5: Planetary Harmonization Remedies"),
    ("Ch 6: Chaldean Sacred Name Vibration", "Section 6: Chaldean Sacred Name Vibration"),
    ("Ch 7: Health & Body Chemistry", "Section 7: Health & Body Chemistry"),
    ("Ch 8: Career & Industry Roadmap", "Section 8: Career & Industry Roadmap"),
    ("Ch 9: Personal Year Calculator Cycle", "Section 9: Personal Year Calculator Cycle"),
    ("Ch 10: Angelic & Vastu Alignment", "Section 10: Angelic & Vastu Alignment"),
    ("Ch 11: Mobile Number Frequency", "Section 11: Mobile Number Frequency"),
    ("Ch 12: Spiritual Sadhana & Benediction", "Section 12: Spiritual Sadhana & Benediction")
]

for old_val, new_val in ch_replacements:
    text = text.replace(old_val, new_val)

print("Updated format switcher and Format 2 headers to Section structure.")

with open(sample_path, 'w', encoding='utf-8') as f:
    f.write(text)
