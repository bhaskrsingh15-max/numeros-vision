"""
DATA GENERATOR FOR PROFESSIONAL NUMEROLOGY 40 TOPICS
Generates data/knowledge_base/professional_numerology_rules.json
Covers Topics 1 to 41 from the reference image, strictly omitting Topic 39 (Hora prediction).
"""

import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

PROFESSIONAL_TOPICS = [
    {
        "topic_id": 1,
        "title": "Introduction to Professional Numbers Rules, Friendly, Neutral, Unfriendly Nos., Input / Output",
        "keywords": ["friendly numbers", "enemy numbers", "neutral numbers", "input output", "rules of numbers"],
        "rules": {
            "root_planets": {
                1: {"planet": "Sun", "friends": [1, 2, 3, 5, 9], "enemies": [8], "neutrals": [4, 6, 7]},
                2: {"planet": "Moon", "friends": [1, 2, 3, 5], "enemies": [8, 4, 9], "neutrals": [6, 7]},
                3: {"planet": "Jupiter", "friends": [1, 2, 3, 5, 7, 9], "enemies": [6], "neutrals": [4, 8]},
                4: {"planet": "Rahu", "friends": [1, 5, 6, 7, 8], "enemies": [2, 9, 4], "neutrals": [3]},
                5: {"planet": "Mercury", "friends": [1, 2, 3, 5, 6], "enemies": [], "neutrals": [4, 7, 8, 9]},
                6: {"planet": "Venus", "friends": [5, 6, 8, 4, 7], "enemies": [3], "neutrals": [1, 2, 9]},
                7: {"planet": "Ketu", "friends": [1, 3, 4, 5, 6], "enemies": [8], "neutrals": [2, 7, 9]},
                8: {"planet": "Saturn", "friends": [5, 6, 3], "enemies": [1, 2, 4, 8], "neutrals": [7, 9]},
                9: {"planet": "Mars", "friends": [1, 3, 5, 9], "enemies": [2, 4], "neutrals": [6, 7, 8]}
            },
            "input_output_rule": "GR-001 (Input 2-digit compound defines occult path/struggle) and GR-002 (Output single digit defines physical manifestation and ruling planet)."
        },
        "remedies": "Align all external vibrations (name, phone, house) to friendly numbers of Driver and Conductor; strictly avoid enemy numbers.",
        "sample_qa": {
            "q": "How do I know if my numbers are friendly or unfriendly?",
            "a": "Every planet has natural celestial friendships. For instance, Driver 1 (Sun) thrives with 1, 2, 3, 5, 9 but experiences severe friction with 8 (Saturn). A professional numerologist never forces an enemy number into name or contact vibrations."
        }
    },
    {
        "topic_id": 2,
        "title": "Mobile Numerology",
        "keywords": ["mobile number", "phone numerology", "sim card number", "lucky mobile number", "mobile total"],
        "rules": {
            "total_preference": {
                1: {"preferred_compounds": [46, 64, 37, 55], "purpose": "Job, Authority, Government favors, Fame, Politics, Leadership"},
                3: {"preferred_compounds": [66, 39, 30], "purpose": "Knowledge to conceive, Overall prosperity, Teaching, Good luck, Health"},
                5: {"preferred_compounds": [41, 32, 50, 59], "purpose": "Life balance, Business, Trade, Communication, Consistent money flow"},
                6: {"preferred_compounds": [42, 24, 33, 60], "purpose": "Luxury, Marriage harmony (42), Foreign travel/settlement (33), Relationship gains"}
            },
            "malefic_combinations_to_avoid": [
                {"pair": "14 / 41", "effect": "Attracts loan liabilities, legal notices, health issues, heavy unending hard work."},
                {"pair": "16 / 61", "effect": "Most negative for married life, spouse health troubles, restricted income."},
                {"pair": "18 / 81", "effect": "Very negative: severe friction between father & son, frequent job disruptions, government scrutiny."},
                {"pair": "26 / 62", "effect": "Break in education, mother-in-law conflict, diabetes or hormonal vulnerability."},
                {"pair": "28 / 82", "effect": "Vish Yog: heavy hospital expenditures, financial fluctuations, severe emotional grief."},
                {"pair": "34 / 43", "effect": "Breathing problems, neurological anxiety, limb numbness; avoid especially if birth chart has multiple 8s."},
                {"pair": "45 / 54", "effect": "Court cases, hospital visits, restricted life progress."},
                {"pair": "48 / 84", "effect": "Blood-related problems, incurable obstacles, sexual dissatisfaction."},
                {"pair": "68 / 86", "effect": "Eye troubles, organ vulnerabilities; avoid especially if birth date has multiple 1s."}
            ],
            "forbidden_repeating_digits": ["00", "000", "0000", "999", "888", "777", "444", "44", "222", "88", "22"]
        },
        "remedies": "Choose SIM cards totaling 5 (e.g. 41, 32), 6 (42 for relationships, 33 for travel), 1 (37 for alliances), or 3 (39 for prosperity). Avoid numbers with 14, 16, 18, 28, 48.",
        "sample_qa": {
            "q": "What mobile number total is best for money and business?",
            "a": "Mobile numbers totaling compound 41 or 32 (resolving to root 5) are premier for business expansion, financial flow, and trade. Ensure the phone number contains no 14, 18, 28, or 48 combinations."
        }
    },
    {
        "topic_id": 3,
        "title": "Pillars of Numerology",
        "keywords": ["numerology pillars", "driver conductor name kua", "core foundation numbers", "pillars"],
        "rules": {
            "five_pillars": [
                "1. Driver (Mulank) - Self, personality, psychological driver",
                "2. Conductor (Bhagyank) - Life destiny, karmic path, career opportunities",
                "3. Chaldean Name Number - Social projection, opportunities attractor, brand resonance",
                "4. Kua Number - Energy compass, environmental Vastu alignment, directional luck",
                "5. Lo Shu Grid - Internal elemental balance, innate talents, missing energy voids"
            ]
        },
        "remedies": "Synchronize all 5 pillars so they vibrate in friendly elemental frequencies rather than conflicting with one another.",
        "sample_qa": {
            "q": "What are the 5 pillars of professional numerology?",
            "a": "The 5 foundational pillars are Driver (Mulank), Conductor (Bhagyank), Name Number, Kua Number, and Lo Shu Grid Matrix. True destiny engineering requires harmony across all 5."
        }
    },
    {
        "topic_id": 4,
        "title": "Car & House Numerology",
        "keywords": ["vehicle numerology", "car number plate", "house numerology", "flat number numerology", "car number"],
        "rules": {
            "vehicle_rules": "Sum of all digits and letters on the number plate must reduce to a friendly number with the owner's Driver. Avoid total 4 (Rahu - accidents/breakdowns) and total 8 (Saturn - frequent delays/police fines) unless Driver is 8.",
            "house_rules": "House or apartment door number total should be friendly to the primary earner's Driver and Conductor. House 1 brings leadership; House 3 brings learning and family joy; House 5 brings lively movement and commerce; House 6 brings luxury, harmony, and celebration."
        },
        "remedies": "If house or car number is unfriendly, place a small correcting brass/copper numeric yantra or sticker to mathematically adjust the total vibration.",
        "sample_qa": {
            "q": "My car number adds up to 8 and I am Driver 1. Is that dangerous?",
            "a": "Yes. 1 (Sun) and 8 (Saturn) are arch enemies. A vehicle totaling 8 for Driver 1 attracts frequent mechanical faults, police penalties, or accidental scrapes. Remedy by placing a copper Sun symbol or corrective numeric sticker inside the vehicle."
        }
    },
    {
        "topic_id": 5,
        "title": "81 Types of Driver & Conductor",
        "keywords": ["81 driver conductor combinations", "d c combination", "driver conductor relationship", "81 combinations"],
        "rules": {
            "best_combinations": ["1-1", "1-2", "1-5", "1-6", "1-9", "3-3", "3-5", "5-5", "5-6", "6-6"],
            "anti_enemy_combinations": [
                {"pair": "1-8 / 8-1", "effect": "Sun-Saturn severe father-son struggle, delayed success, legal issues"},
                {"pair": "2-8 / 8-2", "effect": "Moon-Saturn Vish Yog, mental depression, emotional loneliness, heavy medical expense"},
                {"pair": "3-6 / 6-3", "effect": "Devaguru vs Asuraguru ego clash, marital friction, conflict between principles and luxury"}
            ],
            "opposite_combinations": [
                {"pair": "4-2 / 2-4", "effect": "Rahu-Moon emotional turbulence and psychic stress"},
                {"pair": "4-9 / 9-4", "effect": "Rahu-Mars aggression, impulsive anger, accident vulnerability"},
                {"pair": "9-9", "effect": "Double Mars excessive heat, high temper, impatience"}
            ],
            "struggle_egoist_combinations": [
                {"pair": "4-4", "effect": "Double Rahu extreme hard work, delays, mental illusions"},
                {"pair": "8-8", "effect": "Double Saturn slow growth, heavy burdens, endurance test"},
                {"pair": "2-9 / 9-2", "effect": "Moon-Mars emotional volatility, relationship clashes"},
                {"pair": "7-7", "effect": "Double Ketu over-detachment, isolation, ungrounded spirituality"}
            ]
        },
        "remedies": "For enemy or struggle combinations, implement Name Balancing to a neutralizer number (usually 5 for 1-8 and 2-8; 5 for 3-6) and wear the neutralizing crystal.",
        "sample_qa": {
            "q": "What happens if I have Driver 1 and Conductor 8?",
            "a": "Driver 1 (Sun) and Conductor 8 (Saturn) is an arch-enemy combination. It creates early-life struggle, friction with authority, and delayed recognition. To remedy, balance your Name to Compound 37 or 41 (Root 1/5) and avoid black colors on Sundays and Tuesdays."
        }
    },
    {
        "topic_id": 6,
        "title": "What Numbers 1-9 Signifies",
        "keywords": ["number 1 to 9 signification", "number meanings", "planetary vibrations", "number characteristics"],
        "rules": {
            1: "Sun: Leadership, authority, vitality, self-confidence, initiative, ego, administrative ability.",
            2: "Moon: Intuition, emotions, imagination, diplomacy, sensitivity, partnership, fluctuating mind.",
            3: "Jupiter: Wisdom, knowledge, creativity, expansion, spiritual guidance, speech, counselor.",
            4: "Rahu: Analytical intellect, unconventional thinking, sudden breakthroughs, discipline, technical prowess.",
            5: "Mercury: Balance, business intelligence, versatile communication, adaptability, commercial instinct.",
            6: "Venus: Love, beauty, luxury, domestic harmony, magnetism, arts, sensual fulfillment.",
            7: "Ketu: Spiritual depth, research, occult insight, detachment, intuitive brilliance, introspection.",
            8: "Saturn: Justice, discipline, perseverance, endurance, executive management, karma, long-term wealth.",
            9: "Mars: Courage, physical stamina, humanitarian vigor, military/police precision, decisive action."
        },
        "remedies": "Cultivate the positive traits of your Driver planet and perform grounding practices for over-activated planets.",
        "sample_qa": {
            "q": "What does Number 7 represent?",
            "a": "Number 7 is ruled by Ketu (Neptune tradition). It signifies analytical research, spiritual depth, mental introspection, and occult insight. Natives are deep thinkers who see beyond surface appearances."
        }
    },
    {
        "topic_id": 7,
        "title": "Impact of Repetitive Numbers (Nos 1-9)",
        "keywords": ["repetitive numbers", "repeating digits", "multiple 1s", "multiple 4s", "multiple 8s"],
        "rules": {
            "thumb_rule": "1 repetition is normal; 2 repetitions strengthen positive traits; 3 repetitions turn traits intense or rigid; 4+ repetitions indicate obsessive or problematic imbalances.",
            "details": {
                1: {"1x": "Introverted, difficulty expressing emotions", "2x": "Balanced communicator, self-assured", "3x": "Talkative, commanding", "4x+": "Egoistic, dominating, insensitive to others"},
                2: {"1x": "Sensitive, intuitive", "2x": "Highly empathetic, cooperative", "3x": "Hypersensitive, mood swings", "4x+": "Extreme emotional vulnerability, anxiety"},
                3: {"1x": "Good creative thinker", "2x": "Excellent writer/speaker", "3x": "Over-imaginative, day-dreamer", "4x+": "Scattered focus, ungrounded speech"},
                4: {"1x": "Practical and structured", "2x": "Hard working, meticulous", "3x": "Stubborn, obsessive over rules", "4x+": "Extreme struggle, rigidity, life resistance"},
                5: {"1x": "Balanced, friendly", "2x": "Dynamic, great salesmanship", "3x": "Restless, risk-prone, speech slips", "4x+": "Gambling tendency, emotional instability"},
                6: {"1x": "Caring, family-focused", "2x": "Artistic, romantic, aesthetic", "3x": "Over-protective, possessive in love", "4x+": "Excessive luxury spending, relationship drama"},
                7: {"1x": "Spiritual, curious", "2x": "Deep researcher, strong psychic sense", "3x": "Disappointed in relationships, isolation", "4x+": "Cynicism, complete emotional withdrawal"},
                8: {"1x": "Responsible, orderly", "2x": "Tenacious, executive power", "3x": "Workaholic, heavy financial/legal burdens", "4x+": "Severe hardships, ruthless materialism"},
                9: {"1x": "Courageous, helpful", "2x": "Strong humanitarian leader", "3x": "Hot-tempered, confrontational", "4x+": "Accident-prone, uncontrollable rage"}
            }
        },
        "remedies": "Do NOT wear gemstones of numbers that repeat 3 or more times. Wear crystals of missing balancing numbers to redistribute grid energy.",
        "sample_qa": {
            "q": "I have four 1s in my date of birth. What does it mean?",
            "a": "Having four 1s indicates excessive Sun energy. You may be highly ambitious but risk coming across as domineering or impatient. Do not wear ruby or excessive red. Practice calming water meditation and respect others' viewpoints."
        }
    },
    {
        "topic_id": 8,
        "title": "Impact of Missing Numbers",
        "keywords": ["missing numbers", "missing in loshu grid", "empty grid cells", "missing number remedies"],
        "rules": {
            1: "Difficulty in expressing self, low confidence in public speaking, dependent on others.",
            2: "Lack of empathy, blunt communication, difficulty understanding partner's feelings, coldness.",
            3: "Lack of creative vision, low self-discipline in studies, vulnerability to poor mentors.",
            4: "Lack of practical organization, messy workspace, financial instability, broken Thought plane.",
            5: "Lack of balance, instability in business, inability to hold money, poor communication.",
            6: "Lack of domestic peace, difficulties attracting luxury or supportive relationships.",
            7: "Lack of analytical depth, repeating past mistakes, spiritual disconnect.",
            8: "Lack of financial discipline, inability to manage large assets, poor long-term planning.",
            9: "Lack of courage, low stamina, leaving projects incomplete, lack of social passion."
        },
        "remedies": "Install missing number yantras, wear corresponding semi-precious crystals (not primary gems), use directional vastu remedies, and adopt daily behavioral habits.",
        "sample_qa": {
            "q": "What happens if Number 5 is missing in my Lo Shu grid?",
            "a": "5 represents the Earth center (Brahmasthan) of stability and business acumen. Missing 5 can cause fluctuations in career and difficulty retaining wealth. Remedy by keeping green plants in your environment, wearing green aventurine, and feeding cows on Wednesday."
        }
    },
    {
        "topic_id": 9,
        "title": "Complementary Nos & Master Key Number",
        "keywords": ["complementary numbers", "master key number", "grid compensator", "balancing key"],
        "rules": {
            "pairs": {
                1: [9],
                2: [5, 7],
                3: [5, 7],
                4: [8],
                5: ["Universal balance - partially 6"],
                6: [5],
                7: [2, 3],
                8: [4],
                9: [1]
            },
            "master_key_rule": "Number 5 acts as the Master Key number in professional numerology. Its presence supports all numbers, stabilizing the Will Plane (9-5-1), Emotional Plane (3-5-7), and Success Plane (4-5-6)."
        },
        "remedies": "Activate the complementary number through mobile sum, signature, or yantra when an essential number is missing from the birth chart.",
        "sample_qa": {
            "q": "What is the complementary number for 2?",
            "a": "The complementary numbers for 2 are 5 and 7. They provide the practical grounding (5) and deep intuition (7) needed to stabilize Moon's emotional fluctuations."
        }
    },
    {
        "topic_id": 10,
        "title": "Element Balancing",
        "keywords": ["element balancing", "five elements", "water wood fire earth metal", "loshu elements"],
        "rules": {
            "element_mapping": {
                "Water": {"numbers": [1], "direction": "North", "nature": "Career, opportunities, fluidity"},
                "Earth": {"numbers": [2, 5, 8], "directions": ["South-West (2)", "Center (5)", "North-East (8)"], "nature": "Stability, relationships, wisdom"},
                "Wood": {"numbers": [3, 4], "directions": ["East (3)", "South-East (4)"], "nature": "Growth, health, wealth accumulation"},
                "Metal": {"numbers": [6, 7], "directions": ["North-West (6)", "West (7)"], "nature": "Support, mentors, children, creativity"},
                "Fire": {"numbers": [9], "direction": "South", "nature": "Fame, reputation, passion, vitality"}
            },
            "cycles": "Water feeds Wood, Wood feeds Fire, Fire creates Earth, Earth bears Metal, Metal enriches Water."
        },
        "remedies": "Strengthen missing elements using the generating cycle; do not place conflicting elements (e.g. Fire in North Water zone).",
        "sample_qa": {
            "q": "How do I balance the Wood element if I lack 3 and 4 in my grid?",
            "a": "Wood governs the East and South-East. Introduce healthy green plants, bamboo stalks in water, wooden furniture, and light green decor in these zones."
        }
    },
    {
        "topic_id": 11,
        "title": "Favorable & Unfavorable Directions (Kua Numerology)",
        "keywords": ["kua number", "favorable directions", "unfavorable directions", "kua chart", "lucky directions"],
        "rules": {
            "male_formula": "Add digits of birth year, reduce to single digit. Kua = (11 - reduced_year) for born before 2000, or (10 - reduced_year) for born 2000 onwards.",
            "female_formula": "Add digits of birth year, reduce to single digit. Kua = (reduced_year + 4) for born before 2000, or (reduced_year + 6) for born 2000 onwards.",
            "kua_groups": {
                "East Group (1, 3, 4, 9)": "Favorable directions: North, South, East, South-East",
                "West Group (2, 5, 6, 7, 8)": "Favorable directions: West, North-West, South-West, North-East"
            }
        },
        "remedies": "Align study/work desk and sleep headboard to one of your 4 favorable Kua directions (Sheng Chi / Success or Tien Yi / Health).",
        "sample_qa": {
            "q": "Which direction should I face while working?",
            "a": "Identify your Kua number. East group (1, 3, 4, 9) should face North, South, East, or South-East. West group (2, 5, 6, 7, 8) should face West, North-West, South-West, or North-East for maximum productivity."
        }
    },
    {
        "topic_id": 12,
        "title": "Family Compatibility using Loshu Grid",
        "keywords": ["family compatibility", "loshu synastry", "grid comparison", "couple grid synergy"],
        "rules": {
            "synergy_rule": "When one partner's grid has numbers that the other partner lacks, they form an energetic bridge. For example, if the husband lacks 5 and 6 but the wife has them, the household gains stability and luxury through her presence.",
            "friction_rule": "If both partners lack 5 and 6, the marriage suffers from lack of emotional glue and financial anchor."
        },
        "remedies": "Install shared Yantras and Numero-Vastu corrections in common areas (living room, bedroom) to supply missing family numbers.",
        "sample_qa": {
            "q": "How does Lo Shu grid determine family harmony?",
            "a": "By comparing the grids of spouses, we see whether they complete each other's empty planes. A partner who brings in missing 5 and 6 brings stability and relationship warmth."
        }
    },
    {
        "topic_id": 13,
        "title": "Master Numbers (11, 22, 33)",
        "keywords": ["master numbers", "master number 11", "master number 22", "master number 33", "game changers"],
        "rules": {
            11: {"title": "The Master Visionary / Dreamer", "meaning": "High spiritual intuition, ideals; needs a pragmatic mentor or partner to manifest visions into reality."},
            22: {"title": "The Master Builder", "meaning": "Dreamer and doer; builds lasting institutions, monumental systems, creates own support matrix."},
            33: {"title": "The Master Teacher / Healer", "meaning": "Extremely rare; unconditional love, service to humanity, spiritual avatar energy."}
        },
        "remedies": "Ground high electrical nervous energy with silver, root-chakra meditation, and active humanitarian service.",
        "sample_qa": {
            "q": "Are master numbers always lucky?",
            "a": "Master numbers carry immense potential but also severe nervous tension and early-life testing. They act as game changers once the native learns discipline and emotional grounding."
        }
    },
    {
        "topic_id": 14,
        "title": "Karmic Numbers (10, 13, 14, 16, 19)",
        "keywords": ["karmic numbers", "karmic debt", "13 14 16 19", "karmic burden", "past life debt"],
        "rules": {
            10: "Clean slate karmic number: self-made, lacks initial family support, starts from zero.",
            13: "Karmic debt of lazy/destructive shortcuts: demands tireless ethical hard work; all work and no play until debt cleared.",
            14: "Karmic debt of abuse of freedom/hedonism: vulnerable to fraud, addictions, scams; demands moderation and strict self-control.",
            16: "Karmic debt of betrayal of love: brings sudden relationship breakups, divorce, shattered citadel; requires pure unselfish devotion.",
            19: "Karmic debt of abuse of power/tyranny: tests ego, sudden falls from high positions; requires selfless leadership and giving credit to others."
        },
        "remedies": "Perform specific seva (social service), daily affirmations, avoiding egoistic shortcuts, and feeding birds/cows.",
        "sample_qa": {
            "q": "What is the remedy for Karmic Number 16?",
            "a": "Karmic 16 ('The Shattered Citadel') tests ego in relationships. The remedy is absolute honesty in partnerships, avoiding pride, donating white items on Friday, and keeping a solid silver square to calm emotional turbulence."
        }
    },
    {
        "topic_id": 15,
        "title": "Maha Dasha Prediction - Future Trends",
        "keywords": ["maha dasha", "numerology dasha", "future trends", "planetary periods", "dasha cycle"],
        "rules": {
            "calculation": "Each planet rules a specific multi-year period in life (Sun 1 yr, Moon 2 yrs, Jupiter 3 yrs, Rahu 4 yrs, Mercury 5 yrs, Venus 6 yrs, Ketu 7 yrs, Saturn 8 yrs, Mars 9 yrs).",
            "prediction": "During friendly planetary dasha, opportunities flourish effortlessly; during enemy dasha, delays and obstacles arise."
        },
        "remedies": "Wear the mantra/yantra of the current governing Dasha planet to sail smoothly through karmic friction.",
        "sample_qa": {
            "q": "How does Numerology Dasha forecast career transitions?",
            "a": "By examining whether your current Maha Dasha planet is friendly or hostile to your Driver, we pinpoint optimal years for career jumps versus periods requiring consolidation."
        }
    },
    {
        "topic_id": 16,
        "title": "Universal Year Prediction",
        "keywords": ["universal year", "global year prediction", "universal year 2026", "world trends"],
        "rules": {
            "calculation": "Add all 4 digits of the calendar year. e.g., 2026 = 2 + 0 + 2 + 6 = 10 -> 1 (Sun Universal Year).",
            "meaning_2026": "Universal Year 1 signals global initiation, fresh political leadership, technological breakthroughs, and high independence."
        },
        "remedies": "Align personal endeavors with the Universal Year's global momentum.",
        "sample_qa": {
            "q": "What is the Universal Year for 2026?",
            "a": "2026 reduces to 1 (2+0+2+6 = 10 -> 1), ruled by the Sun. It brings a new 9-year cycle worldwide, favoring bold initiatives, leadership, and entrepreneurship."
        }
    },
    {
        "topic_id": 17,
        "title": "Prediction without DOB calculation (Prashna / Name)",
        "keywords": ["prediction without dob", "no date of birth", "prashna numerology", "name reading without dob"],
        "rules": {
            "methods": [
                "1. Chaldean Name Analysis - Full compound and root vibration reveals inner temperament and life path.",
                "2. Mobile Number Analysis - Current phone number digits indicate recent health, career, and marital state.",
                "3. Time of Query (Prashna) - Current hour and minute sum reveals immediate answer to burning question.",
                "4. Signature Analysis - Handwriting slant and strokes reveal financial health and psychological mindset."
            ]
        },
        "remedies": "When DOB is unknown, balance the full name to an auspicious compound (e.g. 37 or 41) and optimize the mobile number.",
        "sample_qa": {
            "q": "Can I get a reading if I don't know my exact birth date?",
            "a": "Yes! Professional numerologists use Chaldean Name vibrations, mobile number patterns, and signature analysis to diagnose your current life trends with remarkable accuracy."
        }
    },
    {
        "topic_id": 18,
        "title": "Personal Year Predictions 1 to 9",
        "keywords": ["personal year 1 to 9", "py prediction", "current personal year", "yearly cycle numerology"],
        "rules": {
            1: "Sun: Seed-planting year; start of new 9-year cycle, fresh ventures, high ambition, decisive execution.",
            2: "Moon: Root-growing year; consolidation, patience, teamwork, partnership, avoid rash solitary decisions.",
            3: "Jupiter: Sprouting year; self-expression, expansion, learning, travel, social success, creativity.",
            4: "Rahu: Plant strengthening; testing year, heavy disciplined hard work, build solid foundations, avoid illusions.",
            5: "Mercury: Flowering year; unexpected opportunities, commercial growth, freedom, travel, major transitions.",
            6: "Venus: Fruit-bearing year; home, family, marriage, domestic responsibilities, relationship bliss.",
            7: "Ketu: Pruning & reflection; spiritual pause, research, inner healing, avoid risky speculation.",
            8: "Saturn: Harvest year; material authority, business achievement, financial rewards for past 7 years' karma.",
            9: "Mars: Composting year; completion, letting go of outdated relationships/projects, charitable closure, preparation."
        },
        "remedies": "Honor the rhythm of the year: do not force expansion in PY 7 or 9; do not hesitate to launch in PY 1 or 5.",
        "sample_qa": {
            "q": "Is Personal Year 4 good for marriage?",
            "a": "Personal Year 4 is governed by Rahu and represents testing hard work. It is generally advised to delay major marriage commitments to Personal Year 5 or 6 unless charts show extraordinary benefic transits."
        }
    },
    {
        "topic_id": 19,
        "title": "Analysis of PY, PM, PD with DOB",
        "keywords": ["personal year formula", "personal month", "personal day", "py pm pd calculation"],
        "rules": {
            "py_formula": "Date of Birth + Month of Birth + Target Year (reduced to single digit).",
            "pm_formula": "Personal Year + Calendar Month (reduced to single digit).",
            "pd_formula": "Personal Month + Calendar Day (reduced to single digit)."
        },
        "remedies": "Pick high-stakes signing dates, property purchases, and job interviews on Personal Days friendly to your Driver.",
        "sample_qa": {
            "q": "How is Personal Year calculated?",
            "a": "Add your birth day + birth month + current calendar year digits. For example, born 15 August in 2026: 15 (6) + 8 + 2026 (1) = 6 + 8 + 1 = 15 -> 6. You are in Personal Year 6."
        }
    },
    {
        "topic_id": 20,
        "title": "Blood Remedies (Planet Balancing)",
        "keywords": ["blood remedy", "blood donation remedy", "anti month blood donation", "neutralize mars accidents"],
        "rules": {
            "principle": "In Vedic and professional numerology, Mars (9) and afflicted Rahu/Saturn (4, 8) govern blood, surgery, and accidental cuts. Willingly giving blood cleanses the karmic trigger for involuntary surgical bloodshed or accidents.",
            "process": "Donate blood at authorized medical camps quarterly, half-yearly, or during an 'anti-month' (when Personal Month is 9 or enemy to Driver). Always ensure medical eligibility."
        },
        "remedies": "Donate blood once or twice a year, or organize a blood donation drive. For those unable to donate medically, placing a copper coin in flowing water serves as a traditional alternative.",
        "sample_qa": {
            "q": "Why do numerologists recommend blood donation?",
            "a": "Blood donation is an ancient symbolic remedy to pacify aggressive Mars (9) and Rahu (4). Offering voluntary blood prevents involuntary accidents, surgeries, and blood-related ailments."
        }
    },
    {
        "topic_id": 21,
        "title": "Planet Balancing Selection",
        "keywords": ["planet balancing selection", "how to choose remedy planet", "which planet to balance"],
        "rules": {
            "rules_of_selection": [
                "1. Identify the core conflict: Is Driver clashing with Conductor? (e.g. 1-8, 2-8, 3-6)",
                "2. Identify missing critical numbers in Lo Shu grid (especially 5 for center balance, 6 for luxury/relationships)",
                "3. Select a neutral benefic mediator (e.g. 5 Mercury mediates Sun-Saturn 1-8; 5 also mediates 3-6)",
                "4. Never energize an arch-enemy planet directly (e.g., never give Ruby to Driver 8 or Blue Sapphire to Driver 1)."
            ]
        },
        "remedies": "Choose balancing remedies that strengthen the peacemaker planet without triggering enemy counter-reactions.",
        "sample_qa": {
            "q": "How do you select which planet to balance?",
            "a": "A master numerologist never blindly boosts every number. We identify the missing grid elements and introduce a harmonious mediator planet (like Mercury 5) to dissolve conflicts between Driver and Conductor."
        }
    },
    {
        "topic_id": 22,
        "title": "Planet Balancing 1-9 Remedies",
        "keywords": ["planet balancing remedies 1 to 9", "sun remedies", "saturn remedies", "mercury remedies", "rahu remedies"],
        "rules": {
            1: "Sun: Surya Arghya (offer water at sunrise in copper vessel), wake before sunrise, respect father, donate wheat/jaggery.",
            2: "Moon: Drink water from silver glass, seek mother's blessings, Shiva Panchamrit abhishek, donate milk/rice on Mondays.",
            3: "Jupiter: Apply saffron/turmeric tilak on forehead, Thursday fast, respect teachers/gurus, donate chana dal and bananas.",
            4: "Rahu: Keep a solid silver square in pocket, feed stray dogs/crows, donate black sesame, avoid dark blue/black.",
            5: "Mercury: Water green indoor plants, feed green fodder (Palak) to cows on Wednesday, write daily with green pen.",
            6: "Venus: Use pleasant non-alcoholic perfumes, respect women/spouse, donate white sweets on Friday, keep home fragrant.",
            7: "Ketu: Feed street dogs (especially black/white), visit Bhairav/Ganesh temple, donate blankets to needy.",
            8: "Saturn: Mustard oil massage on Saturdays, donate oil/iron, feed crows/black dogs, treat laborers and house-help with honor.",
            9: "Mars: Recite Hanuman Chalisa, donate sweets/red lentils on Tuesday, maintain cordial relations with siblings, blood donation."
        },
        "remedies": "Perform remedies consistently on the governing planetary weekday during Shukla Paksha.",
        "sample_qa": {
            "q": "What is the best remedy to strengthen Mercury (5)?",
            "a": "Feed green spinach to cows on Wednesday morning, write your goals in a green diary, and maintain indoor green plants. This enhances communication, business intellect, and financial stability."
        }
    },
    {
        "topic_id": 23,
        "title": "Yantras for Numerology",
        "keywords": ["yantras for numerology", "surya yantra", "budh yantra", "pyra yantra", "loshu yantras"],
        "rules": {
            "catalog": {
                "Surya Yantra": "For missing 1, weak confidence, leadership voids; use red thread.",
                "Budh Yantra": "For missing 5, commercial instability, lack of balance; use green thread.",
                "Pyra Yantra": "For missing 6, relationship voids, luxury attraction; use white thread.",
                "Surya-Budh Yantra (1-5)": "For missing 1 & 5; provides authority and business intelligence; red & green thread.",
                "Surya-Pyra Yantra (1-6)": "For missing 1 & 6; combines power with prosperity and luxury; red & white thread."
            }
        },
        "remedies": "Wear energized yantra around neck or place on North/East wall of home mandir.",
        "sample_qa": {
            "q": "When should a Surya-Budh Yantra be used?",
            "a": "When both 1 and 5 are missing or weak in your birth chart, Surya-Budh Yantra establishes leadership authority alongside business eloquence. Wear with red and green thread."
        }
    },
    {
        "topic_id": 24,
        "title": "Problem Based Remedies",
        "keywords": ["problem based remedies", "career stagnation remedy", "debt clearance remedy", "marriage delay remedy"],
        "rules": {
            "career_stagnation": "Surya Yantra + offering water to rising sun + clearing clutter from North zone.",
            "debt_and_loans": "Stop using mobile with 14/41; activate North-East corner with brass water vessel; feed cows green grass on Wednesday.",
            "delayed_marriage": "Wear Pyra Yantra + balance name to 24 or 42 + keep pair of rose quartz in South-West bedroom.",
            "frequent_illnesses": "Check Kua Tien Yi (Health) direction; keep brass idol of Dhanvantari or Nandi; perform quarterly blood donation.",
            "court_cases_and_enemies": "Solid silver square in wallet; Hanuman Chalisa on Tuesdays; pacify Rahu."
        },
        "remedies": "Diagnose root numeric cause first, then apply surgical remedy rather than generic rituals.",
        "sample_qa": {
            "q": "What is the remedy for heavy debt and loan liabilities?",
            "a": "Audit your mobile number to ensure no 14, 41, or 48 pairs exist. Balance your name to Compound 37 or 41, and feed green fodder to cows on Wednesday while keeping the North-East zone of your home impeccably clean."
        }
    },
    {
        "topic_id": 25,
        "title": "When to Start Remedies & Process",
        "keywords": ["when to start remedies", "remedy start timing", "shukla paksha", "muhurta for remedies", "43 days rule"],
        "rules": {
            "starting_window": "Always begin remedies during Shukla Paksha (waxing moon) on the weekday associated with the planet (Sun-Sunday, Moon-Monday, etc.).",
            "time_of_day": "Brahma Muhurta (4:00 AM - 6:00 AM) or during the planet's specific Hora.",
            "duration": "Follow the remedy unbroken for at least 43 consecutive days (or 90 days for deep karmic adjustments) to anchor the neuro-energetic vibration."
        },
        "remedies": "If broken midway, restart the 43-day cycle from the next favorable Shukla Paksha weekday.",
        "sample_qa": {
            "q": "Why is the 43-day period important in remedies?",
            "a": "43 days represents a full solar-planetary habituation cycle in Vedic numerology. Consistent daily practice over 43 days rewires your aura and neutralizes adverse karmic patterns."
        }
    },
    {
        "topic_id": 26,
        "title": "Bonus Topics: Child Conceive, Autism, Silver Square, Door Remedies & Relationships",
        "keywords": ["child conceive", "autism cases", "silver square benefits", "door remedies", "temporary permanent relationship", "male female birth"],
        "rules": {
            "child_conceive": "Check presence of 3 (Jupiter - Putrakaraka), 2 (Moon - womb), and 6 (Venus - vitality). Avoid planning conception during Personal Year 4 or 9. Favorable PYs are 2, 3, 6. Use mobile total 3 (66, 39, 30).",
            "autism_cases": "Mercury 5 affliction combined with Rahu/Ketu disruption; missing water/earth anchor. Remedy: Solid silver square with child, cow seva on Wednesday, green aventurine in study room, strictly avoid dark blue/black.",
            "silver_square": "Solid 99.9% pure silver square (1x1 inch) kept in pocket or worn in silver chain. Supreme remedy for pacifying Rahu (4), stabilizing Moon (2) emotions, clearing anxiety, and neutralizing Vish Yog (2-8).",
            "door_remedies": "Main door number plate should harmonize with head of family. Place brass Swastika, threshold brass strip to prevent energy leak, and mango leaf Toran.",
            "temporary_vs_permanent_relationship": "Permanent partnership requires >= 65% synastry with 5 and 6 present in both charts. Temporary relationships (work projects, contractual alliances) operate successfully on need-based functional harmony."
        },
        "remedies": "Apply solid silver square for anxiety/Rahu afflictions; adjust entrance door vibration; plan fertility in Jupiter/Venus cycles.",
        "sample_qa": {
            "q": "What are the benefits of keeping a silver square?",
            "a": "A solid silver square is a master remedy. Silver represents the calm, nurturing energy of the Moon, while the square structure provides Saturn's stabilizing boundary. It calms Rahu's erratic illusions, cures anxiety, and brings emotional peace."
        }
    },
    {
        "topic_id": 27,
        "title": "Choosing the Right Profession",
        "keywords": ["right profession", "career selection numerology", "best business as per driver", "career by date of birth"],
        "rules": {
            "sequence_of_choice": [
                "1. Driver decides core profession (e.g. 1 = Administration/Leadership, 5 = Trading/Finance).",
                "2. Ensure Driver and Conductor are not enemy numbers.",
                "3. Check completed Lo Shu planes (e.g. 4-5-6 Success Plane = Business/Entrepreneurship, 4-3-8 = Strategy/Planning).",
                "4. Consider friendly numbers present in the grid; avoid enemy-number industries."
            ],
            "careers_by_number": {
                1: "Government, Administration, CEO, Politics, Gold/Jewelry, Power positions",
                2: "Liquids, Dairy, Import/Export, Counseling, Psychology, Creative arts",
                3: "Education, Law, Consulting, Publishing, Religious institutions, Finance",
                4: "IT, Software, Analytics, Aviation, Import/Export, Research, Unconventional tech",
                5: "Banking, Stock Broking, Real Estate, Sales, Media, Public Relations, Commerce",
                6: "Luxury Goods, Fashion, Cosmetics, Interior Design, Hospitality, Entertainment",
                7: "Research, Occult Sciences, Cybersecurity, Pathology, Spiritual teaching",
                8: "Real Estate, Mining, Construction, Iron & Steel, Heavy Machinery, Law, Judiciary",
                9: "Defense, Police, Sports, Surgery, Engineering, Real Estate development, Fire/Energy"
            }
        },
        "remedies": "If currently in an enemy profession, build a secondary part-time venture in your friendly number field and balance your name.",
        "sample_qa": {
            "q": "I am Driver 5 and Conductor 6. What career suits me best?",
            "a": "5 (Mercury - commerce) and 6 (Venus - luxury) is one of the most prosperous combinations in numerology. You are naturally suited for luxury retail, high-end real estate, fashion business, media entrepreneurship, or financial consulting."
        }
    },
    {
        "topic_id": 28,
        "title": "Marriage & Business Compatibility",
        "keywords": ["marriage compatibility", "business partner compatibility", "scoring compatibility", "partner synastry"],
        "rules": {
            "scoring_weightage": [
                "Driver vs Driver both positive: 40%",
                "Male Driver stronger than Female: 10%",
                "Driver vs Driver neutral: 30%",
                "Driver vs Driver anti/enemy: 0% (incompatible irrespective of other points)",
                "Complementary pairings (2/9, 2/4, 4/4, 8/8): 20%"
            ],
            "benchmark_scores": {
                "Above 75%": "Excellent partnership",
                "65% to 75%": "Best match",
                "55% to 65%": "Good match",
                "50% to 55%": "Average; requires name balancing",
                "Below 50%": "Not recommended unless 5 & 6 are present in both grids"
            }
        },
        "remedies": "If score is between 50-65%, balance the marriage date and synchronize joint home names to a harmonious mediator.",
        "sample_qa": {
            "q": "Can two Driver 8s partner in business?",
            "a": "Two 8s create a double Saturn union. While both are dedicated, power struggles and rigid viewpoints can stall expansion. Partnership is possible only if one partner manages backend operations and both grids possess active 5 or 6 energy."
        }
    },
    {
        "topic_id": 29,
        "title": "Love & Arrange Marriage Indicators",
        "keywords": ["love marriage numerology", "arrange marriage", "marriage timing", "marriage type by numbers"],
        "rules": {
            "love_marriage_indicators": "Strong Venus (6), Mercury (5), Moon (2) and Ketu (7). Completed Emotional Plane (3-5-7) and Action Plane (2-7-6). Presence of mobile pairs 67, 76, 46, 64.",
            "arrange_marriage_indicators": "Dominant Sun (1), Rahu (4), Saturn (8). Strong Thought Plane (4-3-8) or Practical Plane (8-1-6). Traditional parental approval required to overcome hesitations."
        },
        "remedies": "For those seeking love marriage with parental support, wear Pyra Yantra and keep Rose Quartz in South-West zone.",
        "sample_qa": {
            "q": "Does my chart indicate a love or arranged marriage?",
            "a": "The presence of numbers 5, 6, and 2, along with active emotional planes (3-5-7), strongly predisposes natives toward love marriage. Prominent 1, 4, and 8 lean toward traditional arranged unions."
        }
    },
    {
        "topic_id": 30,
        "title": "Foreign Settlement",
        "keywords": ["foreign settlement", "settling abroad", "overseas travel numerology", "visa approval numbers"],
        "rules": {
            "foreign_numbers": "Numbers 5 (movement/travel), 6 (overseas luxury), and 7 (crossing waters/detachment from homeland).",
            "compound_33": "Mobile total or Name compound 33 is explicitly noted for Abroad / Foreign Travel.",
            "timing": "Personal Year 5 (change/transition) or Personal Year 7 (overseas exploration) provide premier windows for visa approvals."
        },
        "remedies": "Energize North-West (Vayudev / travel zone) with a silver wind chime (5 or 6 rods) and balance name to compound 33.",
        "sample_qa": {
            "q": "What numbers indicate settlement abroad?",
            "a": "Presence of 5, 6, and 7 in your Lo Shu grid, combined with an active North-West zone, strongly favors overseas settlement. Relocation frequently materializes during Personal Year 5 or 7."
        }
    },
    {
        "topic_id": 31,
        "title": "Name Balancing - Regional Name Balancing Part 1",
        "keywords": ["regional name balancing", "cultural name numerology", "surname balancing", "regional prefixes"],
        "rules": {
            "principle": "Regional and cultural surnames carry ancestral frequencies. Never alter the core cultural root unnecessarily. Adjust vowels (A, E, I, O, U) or duplicate benign consonants (e.g. adding 'H' or 'A') to reach the target compound without distorting pronunciation."
        },
        "remedies": "Preserve cultural heritage while mathematically steering the compound total to 19, 37, 41, or 46.",
        "sample_qa": {
            "q": "How is regional name balancing done without changing my official identity?",
            "a": "We subtly adjust intermediate letters (such as adding an extra 'A' or 'H') to tune the vibrational total to an auspicious Cheiro compound, preserving phonetic elegance and cultural roots."
        }
    },
    {
        "topic_id": 32,
        "title": "Name Balancing - Company & Products Part 2",
        "keywords": ["company name numerology", "brand name balancing", "business name numerology", "product naming"],
        "rules": {
            "corporate_compounds": {
                1: {"compounds": [19, 37, 46], "best_for": "Leadership brands, tech giants, conglomerates, luxury benchmarks"},
                5: {"compounds": [32, 41, 50], "best_for": "E-commerce, fast-moving retail, logistics, marketing, fintech"},
                6: {"compounds": [24, 33, 42], "best_for": "FMCG, beauty, fashion, hospitality, premium consumer products"},
                3: {"compounds": [21, 30], "best_for": "EdTech, consulting, financial advisory, legal firms"}
            }
        },
        "remedies": "Align corporate entity name to the founder's Driver/Conductor and the industry's ruling planet.",
        "sample_qa": {
            "q": "What is the best number for an e-commerce company name?",
            "a": "Compound 41 or 32 (Root 5) is ideal for e-commerce and commercial platforms. It stimulates rapid customer acquisition, flexible movement, and steady transaction volume."
        }
    },
    {
        "topic_id": 33,
        "title": "Name Balancing - Letter Section Part 3",
        "keywords": ["letter section", "cornerstone capstone", "first letter of name", "vowel consonant balance"],
        "rules": {
            "cornerstone": "The first letter of the first name represents how you approach new opportunities and hurdles.",
            "capstone": "The last letter of the first name represents how you conclude projects and handle completion.",
            "chaldean_values": "A,I,J,Q,Y=1; B,C,K,R=2; G,L,S=3; D,M,T=4; E,H,N,X=5; U,V,W=6; O,Z=7; F,P=8."
        },
        "remedies": "Ensure the cornerstone and capstone letters are harmonious with the person's Driver number.",
        "sample_qa": {
            "q": "Why does the first letter of a name matter?",
            "a": "In Chaldean letter analysis, the first letter is the Cornerstone. It sets your psychological attitude when meeting new opportunities and dictates your initial response to challenges."
        }
    },
    {
        "topic_id": 34,
        "title": "Implementing Balanced Name",
        "keywords": ["implement balanced name", "how to activate name change", "writing name 108 times", "name activation"],
        "rules": {
            "activation_process": [
                "1. Begin on a Shukla Paksha day matching the ruling planet of the new name compound.",
                "2. Write the new balanced name 21, 43, or 108 times daily in an unruled notebook using green or blue ink.",
                "3. Update email signature, visiting cards, social profiles, and WhatsApp handle.",
                "4. Pronounce the name with positive intention; legal name change in gazette/passport can follow as convenient."
            ]
        },
        "remedies": "Practice unbroken daily writing for at least 43 days to anchor the subconscious acoustic vibration.",
        "sample_qa": {
            "q": "Do I need to change my name in official documents immediately?",
            "a": "No. Name vibration operates psychologically and acoustically first. Writing it 108 times daily and adopting it in daily communications anchors 80% of the energetic benefit within 43 days."
        }
    },
    {
        "topic_id": 35,
        "title": "Share Market Investment & Business",
        "keywords": ["share market numerology", "stock market investment", "trading by date of birth", "shares as per driver"],
        "rules": {
            "trader_suitability": {
                "Driver 5": "Born stock market traders; high agility, quick profit booking, intraday trading natural talent.",
                "Driver 3": "Strategic wealth investors; excellent for long-term mutual funds, blue-chips, index funds.",
                "Driver 6": "Consumer luxury stocks, entertainment, lifestyle, media, FMCG portfolios.",
                "Driver 1": "Large-cap leaders, gold, government securities, sovereign bonds.",
                "Driver 8": "Iron, steel, mining, infrastructure, oil & gas; long-term only (avoid speculative day trading).",
                "Driver 4": "Tech, AI, electric vehicles, renewable energy; avoid leveraged futures/options due to sudden reversal risk."
            }
        },
        "remedies": "Driver 4 and 8 should avoid speculative intraday F&O. Keep green aventurine on trading desk to preserve analytical calm.",
        "sample_qa": {
            "q": "Can I do intraday stock trading if I am Driver 8?",
            "a": "Driver 8 is ruled by Saturn (slow, long-term karma). Intraday and speculative F&O trading often brings sudden capital erosion for Driver 8. You will thrive instead in long-term value investing in infrastructure, mining, or metal stocks."
        }
    },
    {
        "topic_id": 34,
        "title": "Health & Healing (Vedic Organ Mapping)",
        "keywords": ["health and healing", "health issues by number", "body parts numerology", "before 40 after 40"],
        "rules": {
            "age_framework": "Before age 40, health vulnerabilities predominantly reflect Driver number issues; after age 40, Conductor number health themes take dominance.",
            "organ_mapping": {
                1: {"issues": "Heart, blood pressure, eyesight, headaches", "diet": "Citrus, barley, ginger, honey; avoid late night heavy food"},
                2: {"issues": "Anemia, insomnia, asthma, digestive fluid balance", "diet": "Melons, cucumber, buttermilk, coconut water; avoid overthinking"},
                3: {"issues": "Liver, diabetes, joint stiffness, arterial health", "diet": "Fenugreek, turmeric, apples, wheat; avoid excess sweets"},
                4: {"issues": "Respiratory infections, kidney/urinary tract, sudden ailments", "diet": "Spinach, beetroot, leafy greens; avoid intoxicants and stale food"},
                5: {"issues": "Nervous strain, speech stamina, insomnia, skin allergies", "diet": "Walnuts, carrots, potatoes, herbal tea; adequate sleep essential"},
                6: {"issues": "Throat, ENT, hormonal imbalance, reproductive vitality", "diet": "Almonds, fresh fruits, light curd; avoid excessive oily/sweet feasts"},
                7: {"issues": "Skin perspiration, indigestion, bronchial sensitivity", "diet": "Fresh fruit juices, grapes, mushrooms, vitamin D; avoid overwork"},
                8: {"issues": "Joints, teeth, chronic backache, bowel sluggishness", "diet": "Mustard oil massage, buttermilk, high fiber; regular brisk walking"},
                9: {"issues": "Blood pressure, fevers, cuts, burns, hyper-acidity", "diet": "Coconut water, coriander, cooling melons; avoid hot red spices and alcohol"}
            }
        },
        "remedies": "Incorporate planetary dietary recommendations and maintain peaceful sleep.",
        "sample_qa": {
            "q": "Why do health issues change after age 40 in numerology?",
            "a": "Before 40, your physical body is powered primarily by your Driver (Mulank). After 40, your Conductor (Bhagyank) karmic dasha matures, making Conductor organ vulnerabilities more prominent."
        }
    },
    {
        "topic_id": 36,
        "title": "Numero-Vastu Directions for Success as per Vastu",
        "keywords": ["numero vastu", "vastu directions for success", "energising directions", "compass zones loshu"],
        "rules": {
            "directional_matrix": {
                "North (1)": "Water element; Career, wealth opportunities; energize with fountain or aquarium; blue wall.",
                "South-West (2)": "Earth element; Marriage, relationship stability; energize with yellow/golden lighting, Nandi idol, family photo in golden frame.",
                "East (3)": "Wood element; Health, ancestry, knowledge; energize with lush green plants, rising sun painting.",
                "South-East (4)": "Wood element; Cash flow, wealth accumulation; energize with red bulb or bamboo plant.",
                "Center (5)": "Earth element; Brahmasthan, life balance; keep light, open, uncluttered, yellow hues.",
                "North-West (6)": "Metal element; Helpful friends, banking support, travel; energize with metallic wind chimes.",
                "West (7)": "Metal element; Children, creativity, profits; energize with round silver items or white flowers.",
                "North-East (8)": "Earth/Water spiritual junction; Mental clarity, wisdom, vision; keep pure, Gangajal, mandir placement.",
                "South (9)": "Fire element; Fame, recognition, prestige; energize with red decor, bright lighting, awards display."
            }
        },
        "remedies": "Avoid water bodies in South Fire zone and avoid fire/kitchen in North-East spiritual zone.",
        "sample_qa": {
            "q": "How do I energize the North zone for new career opportunities?",
            "a": "North is governed by Water (Number 1). Keep it impeccably clean, introduce a small flowing water fountain or aerated aquarium, and use soft blue or off-white tones."
        }
    },
    {
        "topic_id": 37,
        "title": "Yantra according to Numerology - Remedies - Part 4",
        "keywords": ["yantra remedies part 4", "yantra energization", "consecration of yantra", "prana pratishtha"],
        "rules": {
            "consecration": "Yantras must be consecrated before wearing. Clean with raw milk and Gangajal, offer incense and flowers, chant the planetary seed mantra 108 times, and wear during the planet's auspicious Hora on Shukla Paksha.",
            "thread_pairing": "Surya Yantra with Red thread; Budh Yantra with Green thread; Pyra Yantra with White thread; Surya-Budh with Red & Green thread; Surya-Pyra with Red & White thread."
        },
        "remedies": "Re-energize the yantra on major festival nights (Diwali, Shivratri, Navratri, Purnima) with incense and mantra chanting.",
        "sample_qa": {
            "q": "How do I activate a numerology yantra before wearing?",
            "a": "Purify with Gangajal, place in front of a ghee lamp, chant the planetary beej mantra 108 times, and tie with the prescribed thread color on a Shukla Paksha morning."
        }
    },
    {
        "topic_id": 38,
        "title": "Yantra Making",
        "keywords": ["yantra making", "draw numerical yantra", "bhojpatra yantra", "magic square yantra"],
        "rules": {
            "materials": "Bhojpatra (birch bark) or pure copper plate; pen made of pomegranate twig (Anar ki kalam) or gold/copper stylus.",
            "ink": "Ashtagandha, saffron (Kesar), red sandalwood (Raktachandan), or camphor mixed with Gangajal.",
            "consecration_rule": "Inscribe the numerical 3x3 matrix in the traditional planetary sequence while mentally reciting the planetary mantra during an auspicious Muhurta."
        },
        "remedies": "Laminate the Bhojpatra yantra or seal in a silver/copper amulet (Taweez) to protect from moisture.",
        "sample_qa": {
            "q": "What is the proper way to make a numerology yantra?",
            "a": "Inscribe the 3x3 magic square on Bhojpatra using saffron ink and a pomegranate stylus during an auspicious planetary Hora, chanting the sacred root mantra throughout the process."
        }
    },
    {
        "topic_id": 40,
        "title": "Signature Analysis & Optimization",
        "keywords": ["signature numerology", "lucky signature", "signature analysis", "how to sign for success"],
        "rules": {
            "rules": [
                "1. Slant: Signature must rise at an upward angle of 15 to 30 degrees (signifies career rise, optimism, vitality).",
                "2. First letter: Must be distinctly larger than lowercase letters, clear and well-formed (healthy self-esteem).",
                "3. Stroke: Continuous, fluid stroke without sudden pen stops or hesitation.",
                "4. Underline: Single steady underline beneath the name, ending with two dots (creates a solid foundation and wealth preservation).",
                "5. Strict Don'ts: Never strike through your name (self-destructive); never allow the final stroke to droop downwards (declining fortune); never encircle your name in a closed ring (claustrophobic limitation)."
            ]
        },
        "remedies": "Practice your new rising signature 21 times every morning to train neuromuscular intention for prosperity.",
        "sample_qa": {
            "q": "Why should a signature slant upwards?",
            "a": "An ascending signature (15° to 30°) signals upward career momentum, positive self-drive, and resilience against setbacks. Downward signatures correlate with fatigue and missed opportunities."
        }
    },
    {
        "topic_id": 41,
        "title": "Important Points related to Reading / Consultation",
        "keywords": ["numerology consultation points", "ethics of reading", "client consultation guidelines", "consultation rules"],
        "rules": {
            "ethics_and_guidelines": [
                "1. Study the relationship of the Driver with the current Personal Year first, then Personal Month with Personal Year.",
                "2. Cross-reference completed Lo Shu planes with current Dasha before issuing timing predictions.",
                "3. Never induce fear or fatalistic doom. Present challenging numbers as opportunities for discipline and conscious remedy.",
                "4. Maintain strict client confidentiality and emotional empathy.",
                "5. Distinguish traditional symbolic insight from medical, legal, or psychological counsel; advise professional services where appropriate."
            ]
        },
        "remedies": "Always leave the client with clarity, actionable remedies, and positive empowerment.",
        "sample_qa": {
            "q": "What is the ethical code of a master numerologist?",
            "a": "A master numerologist empowers rather than frightens. We interpret numeric cycles as energetic weather forecasts, equipping the client with the right mental attitude and remedies to navigate any season with dignity."
        }
    }
]

def main():
    target_path = BASE_DIR / "data" / "knowledge_base" / "professional_numerology_rules.json"
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump({"total_topics": len(PROFESSIONAL_TOPICS), "topics": PROFESSIONAL_TOPICS}, f, indent=2, ensure_ascii=False)
    print(f"Successfully generated {len(PROFESSIONAL_TOPICS)} professional numerology topics in {target_path}")

if __name__ == "__main__":
    main()
