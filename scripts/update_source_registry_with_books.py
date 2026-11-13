import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

fp = r'data\knowledge_base\source_registry.json'
with open(fp, 'r', encoding='utf-8') as f:
    registry = json.load(f)

sources = registry.get('sources', [])
print(f'Currently registered sources: {len(sources)}')

existing_ids = {s['source_id'] for s in sources}

new_sources = [
    {
        "source_id": "SRC-81-DC-DESTINY-GUIDE",
        "title": "Driver – Conductor – Destiny Numerology Guide (81 Combinations)",
        "author": "Professional Numerology Faculty",
        "year": 2024,
        "authority_tier": "TIER_1_CANONICAL",
        "category": "NUMEROLOGY_COMBINATIONS",
        "verified_file": "data/uploaded_books_and_notes/Driver Conductor Destiny 81 Combinations PDF Planets In Astrology Planets.pdf",
        "provenance": "Uploaded authoritative curriculum coursebook covering all 81 Driver-Conductor combinations",
        "approval_status": "APPROVED"
    },
    {
        "source_id": "SRC-81-DC-WISDOM",
        "title": "81 Driver-Conductor Combinations in Numerology (Wisdom Reference)",
        "author": "Professional Numerology Faculty",
        "year": 2024,
        "authority_tier": "TIER_1_CANONICAL",
        "category": "NUMEROLOGY_COMBINATIONS",
        "verified_file": "data/uploaded_books_and_notes/81 Driver-Conductor Combinations in Numerology PDF Planets In Astrology Wisdom.pdf",
        "provenance": "43-page comprehensive narrative guide on career, traits, and challenges for Driver-Conductor pairs",
        "approval_status": "APPROVED"
    },
    {
        "source_id": "SRC-ADV-PROF-NOTES",
        "title": "Professional & Advance Numerology Study Notes (Numeros Vision)",
        "author": "Numeros Vision Master Course",
        "year": 2024,
        "authority_tier": "TIER_1_CANONICAL",
        "category": "LO_SHU_GRID_ADVANCED",
        "verified_file": "data/uploaded_books_and_notes/ADVANCE & PROFESSIONAL COURSE - NOTES.pdf",
        "provenance": "Authoritative study notes detailing missing number impacts, poorak complimentary numbers, master key 5, and yantras",
        "approval_status": "APPROVED"
    },
    {
        "source_id": "SRC-NUMERO-MAHADASHA",
        "title": "Calculating Mahadasha in Vedic Astrology & Numerology (Study Notes)",
        "author": "Numeros Vision Faculty",
        "year": 2024,
        "authority_tier": "TIER_1_CANONICAL",
        "category": "DASHA_TIMING",
        "verified_file": "data/uploaded_books_and_notes/Calculating Mahadasha in Vedic Astrology PDF Planets In Astrology Self-Improvement.pdf",
        "provenance": "14-page methodology defining the exact cycle duration, start year, scoring criteria, and PY/PM timing synthesis",
        "approval_status": "APPROVED"
    },
    {
        "source_id": "SRC-TALKING-NUMBERS-BASIC",
        "title": "Basic Numerology Course - Talking Nummbers",
        "author": "Numeros Vision",
        "year": 2024,
        "authority_tier": "TIER_1_CANONICAL",
        "category": "FOUNDATIONAL_NUMEROLOGY",
        "verified_file": "data/uploaded_books_and_notes/Basic Numerology Course - Talking Nummbers.pdf",
        "provenance": "Foundational curriculum for Driver, Conductor, Kua, 8 Yogas, 3 Lotteries, and Anti/Opposite numbers",
        "approval_status": "APPROVED"
    },
    {
        "source_id": "SRC-NAME-NUMEROLOGY-194",
        "title": "Understanding Name Numerology Numbers Reference Guide",
        "author": "Astrological Numerology Scholars",
        "year": 2024,
        "authority_tier": "TIER_1_CANONICAL",
        "category": "CHALDEAN_NAME_ANALYSIS",
        "verified_file": "data/uploaded_books_and_notes/Understanding_Name_Numerology_Numbers___PDF.pdf",
        "provenance": "194-page comprehensive reference catalog for name numerology numbers and compound vibrations",
        "approval_status": "APPROVED"
    }
]

added_count = 0
for ns in new_sources:
    if ns['source_id'] not in existing_ids:
        sources.append(ns)
        existing_ids.add(ns['source_id'])
        added_count += 1
        sid = ns["source_id"]
        stitle = ns["title"]
        print(f'Added: {sid} - {stitle}')

registry['sources'] = sources
registry['total_sources'] = len(sources)

with open(fp, 'w', encoding='utf-8') as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)

print(f'Updated source_registry.json with {added_count} new canonical sources. Total sources now: {len(sources)}')
