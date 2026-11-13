with open('app/engine/monetization_alignment_engine.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('"amount_inr": 249,', '"amount_inr": 199,')
text = text.replace('Recharge 15 Questions (₹249) ✨', 'Recharge 15 Questions (₹199) ✨')
text = text.replace('"entry_price_inr": 249,', '"entry_price_inr": 510,')
text = text.replace('"anchor_price_inr": 499,', '"anchor_price_inr": 999,')
text = text.replace('"recommended_plan": "ai_growth_15q",', '"recommended_plan": "report_master",')
text = text.replace(
    '"plan_name": "Charm AI Growth Pack (15 Questions + Full Remedies)",',
    '"plan_name": "Complete Life Dossier (12-Page Master Dossier & Full Remedies)",'
)

with open('app/engine/monetization_alignment_engine.py', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated monetization_alignment_engine.py successfully!")
