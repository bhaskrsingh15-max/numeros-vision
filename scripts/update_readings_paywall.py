with open('app/api/readings.py', 'r', encoding='utf-8') as f:
    text = f.read()

old_paywall = """        paywall_spec = {
            "title": "ANVEIL EVERY CHARM to Access Full Answers",
            "subtitle": "Choose a Charm AI pass to access deep predictions, timelines, and personalized remedies:",
            "plans": [
                {
                    "id": "starter_5q",
                    "name": "Starter — 5 Questions",
                    "amount_inr": 95,
                    "original_price_inr": 199,
                    "questions_count": 5,
                    "has_remedies": False,
                    "description": "5 Question Predictions for any questions you ask"
                },
                {
                    "id": "growth_10q",
                    "name": "Growth — 10 Questions + Remedies",
                    "amount_inr": 399,
                    "original_price_inr": 599,
                    "questions_count": 10,
                    "has_remedies": True,
                    "popular": True,
                    "description": "10 Questions Predictions + Full Remedies for all 10 questions"
                },
                {
                    "id": "complete_report",
                    "name": "Complete Reports & Remedies",
                    "amount_inr": 1050,
                    "original_price_inr": 1299,
                    "questions_count": 9999,
                    "has_remedies": True,
                    "description": "Complete Personal Destiny Blueprint Report + All Multi-Layer Remedies"
                },
                {
                    "id": "master_consultation",
                    "name": "1-on-1 Master Personal Consultation",
                    "amount_inr": 1499,
                    "original_price_inr": 2999,
                    "questions_count": 9999,
                    "has_remedies": True,
                    "description": "Private 1-on-1 Consultation with Birth Time Rectification & Custom Yantras"
                }
            ]
        }"""

new_paywall = """        paywall_spec = {
            "title": "ANVEIL EVERY CHARM to Access Full Answers",
            "subtitle": "Choose your personalized blueprint or Charm AI pass:",
            "plans": [
                {
                    "id": "rapid_action",
                    "name": "Rapid Action Plan (3-Page Executive PDF)",
                    "amount_inr": 199,
                    "original_price_inr": 399,
                    "questions_count": 5,
                    "has_remedies": True,
                    "description": "3-page targeted action plan with 2-Year Dasha Timeline & Gem/Yantra remedies"
                },
                {
                    "id": "complete_report",
                    "name": "Complete Life Dossier (12-Page Master PDF)",
                    "amount_inr": 510,
                    "original_price_inr": 999,
                    "questions_count": 15,
                    "has_remedies": True,
                    "popular": True,
                    "description": "12-page comprehensive master dossier with 10-Year Dasha, Lo Shu planes, and remedies"
                },
                {
                    "id": "imperial_blueprint",
                    "name": "Imperial Life Blueprint (32-Page Sovereign Dossier)",
                    "amount_inr": 1050,
                    "original_price_inr": 1999,
                    "questions_count": 9999,
                    "has_remedies": True,
                    "description": "32-page dual-system master blueprint with lifetime milestone roadmaps"
                },
                {
                    "id": "starter_5q",
                    "name": "Starter — 5 Questions Pass",
                    "amount_inr": 95,
                    "original_price_inr": 199,
                    "questions_count": 5,
                    "has_remedies": False,
                    "description": "5 Question Predictions across Career, Wealth, Love & Life timing"
                }
            ]
        }"""

if old_paywall in text:
    text = text.replace(old_paywall, new_paywall)
    with open('app/api/readings.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated paywall_spec in readings.py successfully!")
else:
    print("Could not find exact old_paywall in readings.py, checking with regex...")
    import re
    text = re.sub(
        r'paywall_spec\s*=\s*\{[\s\S]*?\}\s*\]\s*\}',
        new_paywall.strip(),
        text,
        count=1
    )
    with open('app/api/readings.py', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated paywall_spec in readings.py via regex!")
