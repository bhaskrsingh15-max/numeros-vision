"""
Global English-Only Report Naming Standard Implementation
Numeros Vision — Master Update Script
"""
import os
import re
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def update_payments():
    filepath = os.path.join(ROOT_DIR, "app", "api", "payments.py")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Update report_essential
    content = re.sub(
        r'"report_essential":\s*\{[^}]*?"name":\s*"[^"]*"[^}]*?"description":\s*"[^"]*"[^}]*?"features":\s*\[[^\]]*?\]',
        '''"report_essential": {
        "name":        "Basic Numerology Report",
        "amount_inr":  199,
        "original_price_inr": 399,
        "amount_paise": 19900,
        "period":      "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "report",
        "description": "A concise report presenting your calculated results, the method used and an initial interpretation of the key findings.",
        "features": [
            "3-Page Executive PDF Report",
            "Calculated Results & Method Used",
            "Key Findings Initial Interpretation",
            "Driver & Conductor Foundation",
            "Lo Shu 3x3 Grid Summary"
        ]''',
        content
    )

    # Update report_master
    content = re.sub(
        r'"report_master":\s*\{[^}]*?"name":\s*"[^"]*"[^}]*?"description":\s*"[^"]*"[^}]*?"features":\s*\[[^\]]*?\]',
        '''"report_master": {
        "name":        "Advanced Numerology Report",
        "amount_inr":  510,
        "original_price_inr": 999,
        "amount_paise": 51000,
        "period":      "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "report",
        "description": "A more detailed report providing expanded interpretations, relevant number relationships and additional analysis supported by the selected product.",
        "features": [
            "12-Page Master Synthesis Dossier",
            "Expanded Interpretations & Number Relationships",
            "5-Year Vimshottari Dasha Timeline",
            "7-Layer Safe Planetary Remedies",
            "Chaldean Sound Frequency Analysis"
        ]''',
        content
    )

    # Update report_divine
    content = re.sub(
        r'"report_divine":\s*\{[^}]*?"name":\s*"[^"]*"[^}]*?"description":\s*"[^"]*"[^}]*?"features":\s*\[[^\]]*?\]',
        '''"report_divine": {
        "name":        "Premium Numerology Report",
        "amount_inr":  1050,
        "original_price_inr": 1999,
        "amount_paise": 105000,
        "period":      "Instant Download",
        "questions_count": 0,
        "has_remedies": True,
        "category":    "report",
        "description": "An extensive report bringing together the supported calculations, detailed interpretations, relevant comparisons and personalised recommendations available for the selected product.",
        "features": [
            "32-Page Sovereign Executive Blueprint",
            "Complete Calculations & Detailed Interpretations",
            "Multi-Generation Compatibility & Comparisons",
            "Personalised Multi-Layer Recommendations",
            "10-Year Macro Planetary Timing Radar"
        ]''',
        content
    )

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated app/api/payments.py successfully.")

def update_funnel_service():
    filepath = os.path.join(ROOT_DIR, "app", "engine", "funnel_service.py")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace plan_name occurrences
    content = content.replace('"plan_name": "Essential Cosmic Blueprint"', '"plan_name": "Basic Numerology Report"')
    content = content.replace('"plan_name": "Master Dual-System Synthesis Dossier"', '"plan_name": "Advanced Numerology Report"')
    content = content.replace('"plan_name": "Complete Reports & Remedies Dossier"', '"plan_name": "Premium Numerology Report"')

    # Replace secondary_cta to 'Compare Report Packages'
    content = re.sub(r'"secondary_cta":\s*"(?:Compare Personal Reports|Compare All Plans|Compare Name Options|Compare Name Analysis Options|Compare Timing Options|Compare Timing Report Options|Preview Compatibility Report|Preview the Compatibility Report|Preview the Detailed Grid Report)"', '"secondary_cta": "Compare Report Packages"', content)

    # Standardize primary CTAs
    content = content.replace('"primary_cta": "Explore My Birth Number Report"', '"primary_cta": "View Basic Report"')
    content = content.replace('"primary_cta": "Get My Full Life Path Report"', '"primary_cta": "Explore Advanced Analysis"')
    content = content.replace('"primary_cta": "Explore My Full Name Analysis"', '"primary_cta": "View Basic Report"')
    content = content.replace('"primary_cta": "See the Compound Number Breakdown"', '"primary_cta": "Explore Advanced Analysis"')
    content = content.replace('"primary_cta": "Explore My Complete Grid Report"', '"primary_cta": "Explore Advanced Analysis"')
    content = content.replace('"primary_cta": "Get the Detailed Pair Analysis"', '"primary_cta": "Explore Advanced Analysis"')
    content = content.replace('"primary_cta": "Explore My Personal Year Report"', '"primary_cta": "View Basic Report"')
    content = content.replace('"primary_cta": "Explore the Full Compatibility Report"', '"primary_cta": "Explore Advanced Analysis"')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated app/engine/funnel_service.py successfully.")

def update_funnel_journey_js():
    filepath = os.path.join(ROOT_DIR, "app", "static", "js", "funnel_journey.js")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace("plan_name: 'Essential Cosmic Blueprint'", "plan_name: 'Basic Numerology Report'")
    content = content.replace("plan_name: 'Master Dual-System Synthesis Dossier'", "plan_name: 'Advanced Numerology Report'")
    content = content.replace("plan_name: 'Complete Reports & Remedies Dossier'", "plan_name: 'Premium Numerology Report'")

    content = content.replace("primary_cta: 'Explore My Birth Number Report →'", "primary_cta: 'View Basic Report →'")
    content = content.replace("primary_cta: 'Get My Full Life Path Report →'", "primary_cta: 'Explore Advanced Analysis →'")
    content = content.replace("primary_cta: 'Explore My Full Name Analysis →'", "primary_cta: 'View Basic Report →'")
    content = content.replace("primary_cta: 'See the Compound Number Breakdown →'", "primary_cta: 'Explore Advanced Analysis →'")
    content = content.replace("primary_cta: 'Explore My Complete Grid Report →'", "primary_cta: 'Explore Advanced Analysis →'")
    content = content.replace("primary_cta: 'Get the Detailed Pair Analysis →'", "primary_cta: 'Explore Advanced Analysis →'")
    content = content.replace("primary_cta: 'Explore My Personal Year Report →'", "primary_cta: 'View Basic Report →'")
    content = content.replace("primary_cta: 'Explore the Full Compatibility Report →'", "primary_cta: 'Explore Advanced Analysis →'")

    content = re.sub(r"secondary_cta:\s*'(?:Compare Personal Reports|Compare All Plans|Compare Name Options|Compare Timing Options|Preview Compatibility Report)'", "secondary_cta: 'Compare Report Packages'", content)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated app/static/js/funnel_journey.js successfully.")

def update_master_content_config():
    filepath = os.path.join(ROOT_DIR, "app", "configuration", "master_content_config.py")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    content = content.replace('"Basic Report (3 Pages)"', '"Basic Numerology Report (3 Pages)"')
    content = content.replace('"Advanced Report (12 Pages)"', '"Advanced Numerology Report (12 Pages)"')
    content = content.replace('"Premium Report (32 Pages)"', '"Premium Numerology Report (32 Pages)"')

    content = content.replace('"Master Dual-System Synthesis (Chaldean + BNN + 5-Year Vimshottari Dasha + 7-Layer Safe Remedies)."', '"A more detailed report providing expanded interpretations, relevant number relationships and additional analysis supported by the selected product."')
    content = content.replace('"Divine Sovereign Life Roadmap with KP Sub-Lord significators, 10-Year Macro Timing Map & Family Compatibility."', '"An extensive report bringing together the supported calculations, detailed interpretations, relevant comparisons and personalised recommendations available for the selected product."')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    json_path = os.path.join(ROOT_DIR, "configuration", "master_content_config.json")
    if os.path.exists(json_path):
        with open(json_path, "r", encoding="utf-8") as f:
            jcontent = f.read()
        jcontent = jcontent.replace('"Basic Report (3 Pages)"', '"Basic Numerology Report (3 Pages)"')
        jcontent = jcontent.replace('"Advanced Report (12 Pages)"', '"Advanced Numerology Report (12 Pages)"')
        jcontent = jcontent.replace('"Premium Report (32 Pages)"', '"Premium Numerology Report (32 Pages)"')
        jcontent = jcontent.replace('"Master Dual-System Synthesis (Chaldean + BNN + 5-Year Vimshottari Dasha + 7-Layer Safe Remedies)."', '"A more detailed report providing expanded interpretations, relevant number relationships and additional analysis supported by the selected product."')
        jcontent = jcontent.replace('"Divine Sovereign Life Roadmap with KP Sub-Lord significators, 10-Year Macro Timing Map & Family Compatibility."', '"An extensive report bringing together the supported calculations, detailed interpretations, relevant comparisons and personalised recommendations available for the selected product."')
        with open(json_path, "w", encoding="utf-8") as f:
            f.write(jcontent)
    print("Updated master_content_config successfully.")

if __name__ == "__main__":
    update_payments()
    update_funnel_service()
    update_funnel_journey_js()
    update_master_content_config()
