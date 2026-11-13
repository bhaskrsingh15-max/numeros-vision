import csv
import json
import os

csv_path = 'configuration/search_intent_and_30day_content_plan.csv'
seo_registry_path = 'configuration/seo-registry.json'
content_registry_path = 'configuration/content-registry.json'
calc_specs_path = 'configuration/calculation-specifications.json'

with open(csv_path, encoding='utf-8') as f:
    rows = list(csv.reader(f))

header = rows[33]
data = rows[34:]

pages = {}
clusters = {}

for r in data:
    if len(r) < 10:
        continue
    kw = r[0].strip()
    vol = int(r[1]) if r[1].isdigit() else 0
    cpc = float(r[2]) if r[2].replace('.', '', 1).isdigit() else 0.0
    intent = r[3].strip()
    content_type = r[4].strip()
    cluster = r[5].strip()
    language = r[6].strip()
    page_id = r[7].strip()
    url_slug = r[8].strip()
    tier = r[9].strip() if len(r) > 9 else ""

    if cluster not in clusters:
        clusters[cluster] = {
            'cluster_name': cluster,
            'total_keywords': 0,
            'total_volume': 0,
            'keywords': []
        }
    clusters[cluster]['total_keywords'] += 1
    clusters[cluster]['total_volume'] += vol
    clusters[cluster]['keywords'].append({'keyword': kw, 'volume': vol, 'intent': intent})

    if page_id and url_slug:
        if page_id not in pages:
            # Generate optimal title, meta description, and schema
            title_base = kw.title()
            pages[page_id] = {
                'page_id': page_id,
                'target_url': url_slug,
                'cluster': cluster,
                'content_type': content_type,
                'language': language or 'English',
                'primary_keyword': kw,
                'secondary_keywords': [],
                'volume_tier': tier,
                'monthly_search_volume': 0,
                'cpc_usd': cpc,
                'page_title': f"{title_base} | Numeros Vision",
                'meta_description': f"Calculate your {kw} accurately with Numeros Vision. Unveil deep personal insights, planetary alignments, and destiny patterns instantly.",
                'schema_type': "WebApplication" if "Calculator" in content_type else "Article",
                'target_intent': intent,
                'internal_links_inbound': [],
                'internal_links_outbound': ['/numerology-calculator-by-name/', '/free-numerology-calculator/', '/life-path-number-calculator/']
            }
        pages[page_id]['secondary_keywords'].append(kw)
        pages[page_id]['monthly_search_volume'] += vol

# Write SEO Registry
os.makedirs('configuration', exist_ok=True)
with open(seo_registry_path, 'w', encoding='utf-8') as f:
    json.dump({'pages': list(pages.values()), 'summary': {'total_pages': len(pages), 'total_clusters': len(clusters)}}, f, indent=2)

# Write Content Registry
with open(content_registry_path, 'w', encoding='utf-8') as f:
    json.dump({'clusters': list(clusters.values())}, f, indent=2)

# Write Calculation Specifications
calculation_specs = {
    "engine_version": "1.0.0",
    "systems": {
        "cheiro_chaldean": {
            "name": "Cheiro Chaldean Numerology",
            "description": "Ancient Chaldean sound-vibration system mapping letters A-Z to numbers 1-8. The sacred number 9 is excluded from direct letter assignment.",
            "letter_mapping": {
                "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 8, "G": 3,
                "H": 5, "I": 1, "J": 1, "K": 2, "L": 3, "M": 4, "N": 5,
                "O": 7, "P": 8, "Q": 1, "R": 2, "S": 3, "T": 4, "U": 6,
                "V": 6, "W": 6, "X": 5, "Y": 1, "Z": 7
            },
            "compound_numbers": {
                "10": {"meaning": "Wheel of Fortune - Honor, faith, success"},
                "11": {"meaning": "Master Number - High spiritual intuition, warning of hidden dangers"},
                "12": {"meaning": "Sacrifice and suffering - Victim of others' plans"},
                "13": {"meaning": "Regeneration and change - Power through upheaval"},
                "14": {"meaning": "Movement, danger from tempests/water, moderate commercial success"},
                "15": {"meaning": "Occult power, eloquence, harmony with art/music"},
                "16": {"meaning": "The Shattered Citadel - Fall from high position, sudden catastrophe"},
                "17": {"meaning": "The Star of the Magi - Immortality, spiritual peace, triumph over trials"},
                "18": {"meaning": "Spiritual upheaval, conflict, deception by friends"},
                "19": {"meaning": "The Prince of Heaven - Complete triumph, happiness, success"},
                "20": {"meaning": "The Awakening - Call to action for duty, spiritual renewal"},
                "21": {"meaning": "The Crown of the Magi - Complete victory, ultimate advancement"},
                "22": {"meaning": "Master Builder - Far-reaching vision, warning of illusion"},
                "23": {"meaning": "The Royal Star of the Lion - Protection from superiors, guaranteed success"},
                "24": {"meaning": "Assistance from high-ranking persons, romance, wealth"},
                "25": {"meaning": "Strength gained through experience and trials"},
                "26": {"meaning": "Disaster through partnership, heavy ruinous investments"},
                "27": {"meaning": "The Sceptre - High intellect, commander, successful enterprise"},
                "28": {"meaning": "The Trusting Lamb - Great promise followed by loss through trusting others"},
                "29": {"meaning": "Grave uncertainties, deception, betrayal in relationships"},
                "30": {"meaning": "Superior mental faculties, indifference to material accumulation"},
                "31": {"meaning": "Solitary thinker, intellectual isolation, self-contained"},
                "32": {"meaning": "Wide connections, popularity, power over groups"},
                "33": {"meaning": "Master Teacher - Universal compassion, supreme spiritual leadership"}
            }
        },
        "pythagorean": {
            "name": "Pythagorean (Western) Numerology",
            "description": "Cyclical 1-9 system based on the Latin alphabet sequence.",
            "letter_mapping": {
                "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8, "I": 9,
                "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "O": 6, "P": 7, "Q": 8, "R": 9,
                "S": 1, "T": 2, "U": 3, "V": 4, "W": 5, "X": 6, "Y": 7, "Z": 8
            },
            "master_numbers": [11, 22, 33]
        },
        "loshu_grid": {
            "name": "Lo Shu 3x3 Magic Square",
            "description": "Ancient Chinese magic square with row/col sums of 15.",
            "grid_positions": {
                "row_1": [4, 9, 2],
                "row_2": [3, 5, 7],
                "row_3": [8, 1, 6]
            },
            "planes": {
                "mental_plane": [4, 9, 2],
                "emotional_plane": [3, 5, 7],
                "practical_plane": [8, 1, 6],
                "thought_plane": [4, 3, 8],
                "will_plane": [9, 5, 1],
                "action_plane": [2, 7, 6],
                "raj_yoga_golden": [4, 5, 6],
                "raj_yoga_silver": [2, 5, 8]
            }
        },
        "planetary_rulers": {
            "1": {"planet": "Sun (Surya)", "day": "Sunday", "gemstone": "Ruby", "metal": "Gold", "color": "Golden Yellow / Orange"},
            "2": {"planet": "Moon (Chandra)", "day": "Monday", "gemstone": "Pearl", "metal": "Silver", "color": "White / Cream"},
            "3": {"planet": "Jupiter (Guru)", "day": "Thursday", "gemstone": "Yellow Sapphire", "metal": "Gold / Brass", "color": "Yellow"},
            "4": {"planet": "Rahu (Uranus)", "day": "Sunday", "gemstone": "Hessonite (Gomed)", "metal": "Alloy", "color": "Electric Blue / Grey"},
            "5": {"planet": "Mercury (Budha)", "day": "Wednesday", "gemstone": "Emerald", "metal": "Silver / Bronze", "color": "Emerald Green"},
            "6": {"planet": "Venus (Shukra)", "day": "Friday", "gemstone": "Diamond / White Sapphire", "metal": "Silver / Platinum", "color": "White / Light Blue"},
            "7": {"planet": "Ketu (Neptune)", "day": "Monday", "gemstone": "Cat's Eye (Lehsuniya)", "metal": "Alloy", "color": "Pale Green / Light Smoke"},
            "8": {"planet": "Saturn (Shani)", "day": "Saturday", "gemstone": "Blue Sapphire", "metal": "Iron", "color": "Dark Blue / Black"},
            "9": {"planet": "Mars (Mangal)", "day": "Tuesday", "gemstone": "Red Coral", "metal": "Copper", "color": "Red / Crimson"}
        }
    }
}

with open(calc_specs_path, 'w', encoding='utf-8') as f:
    json.dump(calculation_specs, f, indent=2)

print(f"Successfully generated:")
print(f"- {seo_registry_path} ({len(pages)} pages)")
print(f"- {content_registry_path} ({len(clusters)} clusters)")
print(f"- {calc_specs_path} (Full deterministic specifications)")
