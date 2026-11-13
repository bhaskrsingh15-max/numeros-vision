import json
from datetime import datetime

profession_registry = {
    "version": "1.0.0",
    "updated_at": datetime.now().isoformat(),
    "primary_book_status": "MISSING_SOURCE",
    "missing_book_title": "Nadi Astrology & Professions by Classical Nadi Tradition",
    "note": "The dedicated monograph 'Nadi Astrology & Professions' has not been located in runtime or downloads. Per Section 6.5 of the Master Specification, detailed profession profiles are strictly PENDING. However, fundamental planetary archetype mappings from Chapter 8 (pp. 108-109) of 'Numeros Vision Classical Nadi Event System' are verified and structured below.",
    "verified_source_id": "Classical Nadi_2013_METHODOLOGY",
    "verified_chapter": "Chapter- 8: Career & Financial Prospects",
    "verified_pdf_page": 108,
    "verified_printed_page": 103,
    "archetypes": [
        {
            "category_id": "PROF-GOV-001",
            "category_name": "Government & Administration",
            "significator_planets": ["Sun", "Moon"],
            "houses": [2, 6, 10, 11],
            "exact_source_text": "Sun/ Moon - Government. In the DBA of either Sun or Moon natives get a government job.",
            "application_scope": "Public service, administrative examinations, civil governance, institutional leadership."
        },
        {
            "category_id": "PROF-UNI-002",
            "category_name": "Uniform & Defense Services",
            "significator_planets": ["Mars"],
            "houses": [2, 6, 10, 11],
            "exact_source_text": "Mars - Uniform.",
            "application_scope": "Armed forces, police services, security operations, surgical professions, mechanical disciplines."
        },
        {
            "category_id": "PROF-CORP-003",
            "category_name": "Corporate, Advisory & Commercial Enterprise",
            "significator_planets": ["Jupiter", "Mercury", "Venus"],
            "houses": [2, 7, 10, 11],
            "exact_source_text": "Jupiter/Mercury/Venus - Corporate world.",
            "application_scope": "Multinational corporate enterprise, finance, banking, chartered accountancy, consulting, media, creative communications."
        },
        {
            "category_id": "PROF-SM-004",
            "category_name": "Specialized Trades & Technical Establishments",
            "significator_planets": ["Saturn", "Rahu", "Ketu"],
            "houses": [2, 6, 10, 11],
            "exact_source_text": "Rahu/ Ketu/Sat -Small establishments.",
            "application_scope": "Specialized technical trades, independent fabrication, hardware systems, logistics, mineral and resource industries."
        }
    ]
}

with open('data/knowledge_base/nadi_profession_rules.json', 'w', encoding='utf-8') as f:
    json.dump(profession_registry, f, indent=2, ensure_ascii=False)

print("Successfully wrote data/knowledge_base/nadi_profession_rules.json")
