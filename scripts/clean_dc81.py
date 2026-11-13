import json

with open('data/knowledge_base/driver_conductor_81_rules.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

# Update 7_7
if '7_7' in d:
    d['7_7']['planet_combination'] = "Ketu-Ketu (Dual Specialist / Deep Analytical Master)"
    d['7_7']['star_rating'] = 3.0
    d['7_7']['star_display'] = "★★★☆☆ (3/5 Stars — Specialized Analytical Depth)"
    d['7_7']['synergy_title'] = "7-7: The Deep Strategist & Specialized Innovator"
    d['7_7']['positive_traits'] = [
        "Exceptional investigative depth and analytical clarity",
        "High intuition and immunity to superficial marketing hype",
        "Profound mastery of complex systems and specialized domains",
        "Uncompromising integrity and focus on product quality"
    ]
    d['7_7']['negative_traits'] = [
        "Tendency to over-analyze before delegating operations",
        "Reluctance to engage in aggressive or flashy sales pitches",
        "Preference for independent autonomy over ambiguous partnerships"
    ]
    d['7_7']['recommended_careers'] = [
        "Deep Technology & Data Systems",
        "Fintech Architecture & Specialized Consulting",
        "Advanced Scientific & Market Research",
        "Strategic Intelligence & Forensic Auditing",
        "System Architecture & Higher Education"
    ]
    d['7_7']['warnings_and_cautions'] = (
        "Dual Number 7 excels through specialized technical and intellectual autonomy. "
        "When entering business or venture partnerships, ensure equity, governance, and daily operational responsibilities "
        "are backed by formal written contracts and balanced by strong commercial co-founders."
    )
    d['7_7']['fast_summary'] = (
        "Dual Number 7 brings monumental analytical acumen and specialized expertise; "
        "thrive in technology, research, and data systems; pair with strong commercial collaborators for business scale."
    )

# Update 4_7
if '4_7' in d:
    d['4_7']['planet_combination'] = "Rahu-Ketu (Vision Meets Specialized Execution)"
    d['4_7']['star_display'] = "★★★★☆ (4/5 Stars — Visionary Execution & High Innovation)"
    d['4_7']['synergy_title'] = "4-7: The Innovative Strategist & Market Architect"
    d['4_7']['positive_traits'] = [
        "Holistic system vision combined with specialized technical precision",
        "Innovative product architecture and data-driven marketing acumen",
        "Deep analytical problem-solving in complex industries",
        "High adaptability in international and digital markets"
    ]
    d['4_7']['recommended_careers'] = [
        "Product Strategy & High-Tech Growth",
        "Digital Enterprise & Global Systems",
        "Data Analytics & Market Intelligence",
        "Fintech & Specialized Consulting",
        "Media & Strategic Communications"
    ]
    d['4_7']['warnings_and_cautions'] = (
        "Number 4 systems architecture aligns seamlessly with Number 7 analytical depth, "
        "unlocking breakthrough innovation in tech, finance, and specialized consulting."
    )
    d['4_7']['fast_summary'] = (
        "Four stars: High synergy between overarching structural vision and technical execution; "
        "exceptional potential in enterprise technology, product growth, and analytics."
    )

# Update 5_5
if '5_5' in d:
    d['5_5']['warnings_and_cautions'] = (
        "Numeros Vision analysis highlights 5: God-gifted natural talent for business. "
        "With double 5, commercial success compounds rapidly when focus is maintained on core priorities."
    )

# Update 6_9
if '6_9' in d:
    d['6_9']['planet_combination'] = "Venus-Mars (Creative Drive & Passion Harmonization)"
    d['6_9']['star_display'] = "★★★☆☆ (3/5 Stars — Dynamic Vitality & Creative Drive)"
    d['6_9']['synergy_title'] = "6-9: The Dynamic Creative & High-Energy Leader"
    d['6_9']['negative_traits'] = [
        "Emotional intensity requiring clear boundaries",
        "Impulsive expenditures on creative passion projects"
    ]
    d['6_9']['warnings_and_cautions'] = (
        "Venus harmony pairs with Mars energy. Channel intense creative passion into structured artistic, "
        "athletic, or business ventures with clear boundaries and emotional pacing."
    )
    d['6_9']['fast_summary'] = (
        "Venus-Mars dynamic vitality; channels high creative charisma into media, arts, and enterprise "
        "when grounded with emotional maturity."
    )

# Update 9_6
if '9_6' in d:
    d['9_6']['planet_combination'] = "Mars-Venus (Creative Drive & Passion Harmonization)"
    d['9_6']['star_display'] = "★★★☆☆ (3/5 Stars — Dynamic Vitality & Creative Drive)"
    d['9_6']['synergy_title'] = "9-6: The Dynamic Creative & High-Energy Leader"
    d['9_6']['negative_traits'] = [
        "Emotional intensity requiring clear boundaries",
        "Impulsive expenditures on creative passion projects"
    ]
    d['9_6']['warnings_and_cautions'] = (
        "Mars drive pairs with Venus aesthetic harmony. Channel intense energy into structured creative "
        "and commercial initiatives with disciplined follow-through."
    )
    d['9_6']['fast_summary'] = (
        "Mars-Venus dynamic vitality; channels high creative charisma into media, arts, and enterprise "
        "when grounded with emotional maturity."
    )

# Update 7_9
if '7_9' in d:
    d['7_9']['planet_combination'] = "Ketu-Mars (Intuition & Dynamic Energy)"
    d['7_9']['star_display'] = "★★★☆☆ (3/5 Stars — Intuitive Focus & Physical Drive)"
    d['7_9']['synergy_title'] = "7-9: The Focused Specialist & Strategic Initiator"
    d['7_9']['positive_traits'] = [
        "Deep strategic focus",
        "High stamina and endurance",
        "Passionate defense of quality and integrity",
        "Surgical and technical precision"
    ]
    d['7_9']['negative_traits'] = [
        "Impatience when outcomes are delayed",
        "Need for deliberate emotional pacing"
    ]
    d['7_9']['recommended_careers'] = [
        "Technical Systems & Engineering",
        "Specialized Surgical or Medical Practice",
        "Strategic Risk Analysis & Security",
        "Sports Technology & Athletics",
        "Emergency Services & Critical Response"
    ]
    d['7_9']['warnings_and_cautions'] = (
        "Ketu analytical intuition combines with Mars dynamic courage. "
        "Channel this focused energy into disciplined technical projects, physical training, and strategic leadership."
    )
    d['7_9']['fast_summary'] = (
        "Dynamic intuition meets focused energy; excels in technical precision, strategic analysis, and crisis management."
    )

with open('data/knowledge_base/driver_conductor_81_rules.json', 'w', encoding='utf-8') as f:
    json.dump(d, f, indent=2, ensure_ascii=False)

print("Successfully sanitized driver_conductor_81_rules.json!")
