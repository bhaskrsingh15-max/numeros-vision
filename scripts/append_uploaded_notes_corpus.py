import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

corpus_path = r'data\knowledge_base\numeros_vision_corpus.json'
with open(corpus_path, 'r', encoding='utf-8') as f:
    corpus_dict = json.load(f)

passages = corpus_dict['passages']
print(f'Starting corpus size: {len(passages)} passages')
existing_ids = {p.get('id') for p in passages}

new_passages = []

# 1. Missing Numbers (SRC-ADV-PROF-NOTES)
with open(r'data\knowledge_base\missing_number_rules.json', 'r', encoding='utf-8') as f:
    missing_data = json.load(f)

for digit_str, data in missing_data['missing_number_impacts'].items():
    pid = f'PASSAGE-MISSING-NUM-{digit_str}'
    if pid not in existing_ids:
        text = (
            f"Missing Number {digit_str} ({data['element']} Element) in Lo Shu Grid: "
            f"Impact: {data['impact']} "
            f"Complimentary Poorak Numbers: {missing_data['complimentary_poorak_numbers'].get(digit_str, 'None')}. "
            f"Element Remedy: {data['remedy']} "
            f"Yantra Remedy: {data['yantra_remedy']}."
        )
        new_passages.append({
            "id": pid,
            "title": f"Missing Number {digit_str} Diagnosis & Verified Remedies",
            "text": text,
            "domain": "numerology",
            "system": "lo_shu",
            "source_id": "SRC-ADV-PROF-NOTES",
            "source_title": "Professional & Advance Numerology Study Notes (Numeros Vision)",
            "approval_status": "APPROVED",
            "governance_version": "1.0.0"
        })
        existing_ids.add(pid)

# Master key 5 rule
pid = 'PASSAGE-MASTER-KEY-5'
if pid not in existing_ids:
    mk = missing_data['master_key_rule_5']
    new_passages.append({
        "id": pid,
        "title": "Master Key Number 5 Rule for Missing Digits",
        "text": f"Number 5 is the Master Key in Lo Shu Grid numerology. {mk['description']}",
        "domain": "numerology",
        "system": "lo_shu",
        "source_id": "SRC-ADV-PROF-NOTES",
        "source_title": "Professional & Advance Numerology Study Notes (Numeros Vision)",
        "approval_status": "APPROVED",
        "governance_version": "1.0.0"
    })
    existing_ids.add(pid)

# 2. 81 Driver-Conductor Combinations (SRC-81-DC-DESTINY-GUIDE)
with open(r'data\knowledge_base\driver_conductor_81_rules.json', 'r', encoding='utf-8') as f:
    dc_data = json.load(f)

for key, dc in dc_data.items():
    pid = f"PASSAGE-DC-{key}"
    if pid not in existing_ids:
        text = (
            f"Driver {dc['driver']} ({dc['driver_planet']}) and Conductor {dc['conductor']} ({dc['conductor_planet']}) "
            f"Combination in Numerology ({dc['planet_combination']}): "
            f"Destiny Influence: {dc['destiny_influence']}. "
            f"Compatibility Rating: {dc['compatibility']}."
        )
        new_passages.append({
            "id": pid,
            "title": f"Driver {dc['driver']} + Conductor {dc['conductor']} ({dc['planet_combination']}) Destiny & Compatibility",
            "text": text,
            "domain": "numerology",
            "system": "chaldean_loshu_synthesis",
            "source_id": "SRC-81-DC-DESTINY-GUIDE",
            "source_title": "Driver – Conductor – Destiny Numerology Guide (81 Combinations)",
            "approval_status": "APPROVED",
            "governance_version": "1.0.0"
        })
        existing_ids.add(pid)

# 3. Numerological Mahadasha (SRC-NUMERO-MAHADASHA)
with open(r'data\knowledge_base\numerological_mahadasha_rules.json', 'r', encoding='utf-8') as f:
    md_data = json.load(f)

pid = "PASSAGE-NUMERO-MAHADASHA-CALCULATION"
if pid not in existing_ids:
    text = (
        "How to Calculate Numerological Mahadasha: "
        "The first Mahadasha starts at the Date of Birth with the King (Driver) Number. "
        "The initial duration equals the King Number in years (e.g. King 4 runs for 4 years). "
        "Subsequent Mahadashas follow the natural numerical planetary cycle: 1 (Sun, 1 yr) -> 2 (Moon, 2 yrs) -> "
        "3 (Jupiter, 3 yrs) -> 4 (Rahu, 4 yrs) -> 5 (Mercury, 5 yrs) -> 6 (Venus, 6 yrs) -> 7 (Ketu, 7 yrs) -> "
        "8 (Saturn, 8 yrs) -> 9 (Mars, 9 yrs), circulating indefinitely. "
        "Ratings: MD in Lo Shu grid (+1 score), MD compatibility with King number (+2 score for friendly, +1 for neutral, 0 for anti). "
        "Total score: 2.5-3.0 Excellent, 2.0-2.5 Average, below 2.0 Challenging."
    )
    new_passages.append({
        "id": pid,
        "title": "Numerological Mahadasha Calculation and Scoring Methodology",
        "text": text,
        "domain": "numerology",
        "system": "vedic_numerology_mahadasha",
        "source_id": "SRC-NUMERO-MAHADASHA",
        "source_title": "Calculating Mahadasha in Vedic Astrology & Numerology (Study Notes)",
        "approval_status": "APPROVED",
        "governance_version": "1.0.0"
    })
    existing_ids.add(pid)

# Life timing events
pid = "PASSAGE-NUMERO-TIMING-EVENTS"
if pid not in existing_ids:
    text = (
        "Crucial Life Event Timing via Personal Year (PY) and Numerological Mahadasha: "
        "Own House / Property Purchase: Personal Years 2, 5, 8, 9 (activated by Earth Plane 2-5-8 and Mars 9). "
        "Foreign Travel: Personal Years 5, 6 with King/PY compatibility >= 80% and 5/6 in Lo Shu grid (4 and 7 supporting). "
        "Job Promotion: Personal Years 1, 3, 5, 6 with King compatibility >= 60%. "
        "Job Termination Risk: Personal Year 9 or Anti Year where King/PY compatibility is below 20%. "
        "Children Conception/Birth: Personal Year 2 or Benefic Years (1, 3, 5, 6) with King/PY rating > 60%."
    )
    new_passages.append({
        "id": pid,
        "title": "Crucial Life Event Timing Rules in Numerology",
        "text": text,
        "domain": "numerology",
        "system": "vedic_numerology_mahadasha",
        "source_id": "SRC-NUMERO-MAHADASHA",
        "source_title": "Calculating Mahadasha in Vedic Astrology & Numerology (Study Notes)",
        "approval_status": "APPROVED",
        "governance_version": "1.0.0"
    })
    existing_ids.add(pid)

passages.extend(new_passages)
corpus_dict['passages'] = passages
corpus_dict['total_passages'] = len(passages)
corpus_dict['sources_count'] = 87

with open(corpus_path, 'w', encoding='utf-8') as f:
    json.dump(corpus_dict, f, indent=2, ensure_ascii=False)

print(f'Successfully added {len(new_passages)} new authoritative passages. Total corpus now: {len(passages)} passages.')
