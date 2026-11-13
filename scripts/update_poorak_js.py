# -*- coding: utf-8 -*-
with open('app/static/js/number_characteristics.js', 'r', encoding='utf-8') as f:
    text = f.read()

old_block = '''  "master_poorak_map": {
    "1": {
      "complementary": [
        9
      ],
      "planet": "Mars (Mangal)",
      "role": "Provides executive courage, physical vitality, and fearless action to Sun's leadership."
    },
    "2": {
      "complementary": [
        5,
        7
      ],
      "planet": "Mercury & Ketu",
      "role": "Mercury (5) provides rational communication and commercial stability to Moon's sensitivity; Ketu (7) provides intuitive spiritual alignment."
    },
    "3": {
      "complementary": [
        5,
        7
      ],
      "planet": "Mercury & Ketu",
      "role": "Mercury (5) monetizes and commercially structures Jupiter's wisdom; Ketu (7) deepens divine esoteric research."
    },
    "4": {
      "complementary": [
        8
      ],
      "planet": "Saturn (Shani)",
      "role": "Provides grounded physical discipline, legal compliance, and structural stamina to Rahu's unconventional systems."
    },
    "5": {
      "complementary": [
        1,
        6
      ],
      "planet": "Universal Master Key",
      "role": "Number 5 is the Universal Balancer (Mercury); neutral and friendly to all. Supported by Sun (1) for authority and Venus (6) for luxury."
    },
    "6": {
      "complementary": [
        5
      ],
      "planet": "Mercury (Budh)",
      "role": "Provides witty commercial networking and agile dealmaking to Venusian luxury and domestic aesthetics."
    },
    "7": {
      "complementary": [
        3
      ],
      "planet": "Jupiter (Guru)",
      "role": "Provides structured philosophical teaching, public mentorship, and ethical direction to Ketu's solitary insights."
    },
    "8": {
      "complementary": [
        4,
        5
      ],
      "planet": "Rahu & Mercury",
      "role": "Rahu (4) provides unconventional system engineering; Mercury (5) provides commercial flexibility and diplomatic speed to Saturnian rigidity."
    },
    "9": {
      "complementary": [
        1
      ],
      "planet": "Sun (Surya)",
      "role": "Provides sovereign executive command, public status, and noble direction to Martian physical force and raw energy."
    }
  }'''

new_block = '''  "master_poorak_map": {
    "1": {
      "complementary": [9],
      "planet": "Mars (Mangal)",
      "role": "Authority supported by a commander or trusted executor (courage, physical action, military execution)."
    },
    "2": {
      "complementary": [3, 7],
      "planet": "Jupiter & Ketu",
      "role": "Mind and decision-making supported by knowledge/pedagogy (3) and spiritual thinking/intuition (7)."
    },
    "3": {
      "complementary": [7],
      "planet": "Ketu (South Node)",
      "role": "Knowledge, education, wisdom and spirituality supported by deep research and esoteric insight."
    },
    "4": {
      "complementary": [8],
      "planet": "Saturn (Shani)",
      "role": "Discipline and time-related discipline (laborious stamina, legal rigor). Limited strictly to discipline; does not replace Rahu's unconventional systems."
    },
    "5": {
      "complementary": [6],
      "planet": "Venus (Shukra)",
      "role": "Balance and relationship-related support, family stability, and supportive social luxury."
    },
    "6": {
      "complementary": [5],
      "planet": "Mercury (Budh)",
      "role": "Provides witty commercial networking, agile dealmaking, and relationship balance (Day 8: 5 supports 6)."
    },
    "7": {
      "complementary": [3],
      "planet": "Jupiter (Guru)",
      "role": "Knowledge, wisdom, and positive fulfillment (mentorship, ethical grounding, public guidance)."
    },
    "8": {
      "complementary": [4, 5],
      "planet": "Rahu & Mercury",
      "role": "Discipline supported by 4; money management and balance supported by 5."
    },
    "9": {
      "complementary": [1],
      "planet": "Sun (Surya)",
      "role": "Execution and leadership supported by the king or authority figure (sovereign direction, administrative status)."
    }
  }'''

old_crlf = old_block.replace('\n', '\r\n')
new_crlf = new_block.replace('\n', '\r\n')

if old_crlf in text:
    text = text.replace(old_crlf, new_crlf)
    print("SUCCESS: Replaced CRLF block")
elif old_block in text:
    text = text.replace(old_block, new_block)
    print("SUCCESS: Replaced LF block")
else:
    print("ERROR: old_block not found in file")

with open('app/static/js/number_characteristics.js', 'w', encoding='utf-8') as f:
    f.write(text)
