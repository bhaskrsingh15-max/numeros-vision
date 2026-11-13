import json

# 1. Update birth_subdates_registry.json
with open('app/data/birth_subdates_registry.json', 'r', encoding='utf-8') as f:
    registry = json.load(f)

if '16' in registry:
    registry['16']['strength_title'] = "The Strategic Awakener & Deep Visionary"
    registry['16']['archetype'] = "The Strategic Visionary & Healer of Truth"
    registry['16']['classical_symbol'] = "The Transformative Awakening (16)"
    registry['16']['planetary_composition'] = "Sun (1) + Venus (6) = 7 (Ketu Intuitive Wisdom)"
    registry['16']['strength_value_breakdown'] = (
        "Number 16 reflects deep intellectual foresight and personal resilience. "
        "The Sun (clarity) and Venus (harmony) resolve into Ketu (analytical specialization), "
        "equipping the native with profound problem-solving, strategic clarity, and endurance."
    )
    registry['16']['report_narrative'] = (
        "Born on the 16th, you walk a transformative path of profound insight and wisdom. "
        "The synthesis of executive focus and harmonious intuition clears the way for deep technical and analytical mastery."
    )
    registry['16']['charm_ai_dialogue'] = (
        "Day 16 gives you a sharp, intuitive mind and high strategic foresight! "
        "Combining the drive of the Sun with the balance of Venus, you have an exceptional capacity "
        "to see the core truth in complex situations."
    )

with open('app/data/birth_subdates_registry.json', 'w', encoding='utf-8') as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)

# 2. Update all number_characteristics.js files
js_paths = [
    'app/static/js/number_characteristics.js',
    'dist_cloudflare_pages/js/number_characteristics.js',
    'dist_cloudflare_pages/static/js/number_characteristics.js'
]

for p in js_paths:
    try:
        with open(p, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace Day 16 strings
        content = content.replace("Category A  Good Strength (Karmic 16 / Lightning Awakener)", "The Strategic Awakener & Deep Visionary")
        content = content.replace("Category A - Good Strength (Karmic 16 / Lightning Awakener)", "The Strategic Awakener & Deep Visionary")
        content = content.replace("The Shattered Citadel / Lightning Awakening (16)", "The Transformative Awakening (16)")
        content = content.replace("The Lightning Awakener & Healer of Truth", "The Strategic Visionary & Healer of Truth")
        content = content.replace("Sun (1) + Venus (6) = 7 (Ketu Spiritual Awakening)", "Sun (1) + Venus (6) = 7 (Ketu Intuitive Wisdom)")
        content = content.replace("Karmic Debt Number 16. The Sun (ego) and Venus (material attachment) are shattered by Ketu's lightning to forge the highest spiritual awakening and healing genius.", "Number 16 reflects deep intellectual foresight and personal resilience. The Sun (clarity) and Venus (harmony) resolve into Ketu (analytical specialization), equipping the native with profound problem-solving, strategic clarity, and endurance.")
        
        # Also clean 7_7 in JS
        content = content.replace("Solitary Academic Research, Occult & Esoteric Healing, Astrology & Palmistry Mastery", "Deep Technology & Data Systems, Fintech Architecture & Specialized Consulting, Advanced Scientific & Market Research")
        content = content.replace("Never do business in partnershiploss is 100% guaranteed. Never do risky business.", "Ensure business partnerships have clear governance and written contracts.")

        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {p}")
    except Exception as e:
        print(f"Error updating {p}: {e}")

print("Day 16 and 7_7 successfully sanitized across registries and JS bundles!")
