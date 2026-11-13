import os

os.makedirs("knowledge/analysis", exist_ok=True)

# 1. consensus_matrix.csv
consensus_csv = """topic,chaldean_position,pythagorean_position,vedic_position,chinese_loshu_position,consensus_level,authority_policy
Number 1 Archetype,Sun / Leadership / Pioneer,Sun / Independent / Original,Sun / Authority / Mulank 1,Water / North / Career (Position 1),High,Single digit 1 uniformly signifies solar independence and origin
Number 2 Archetype,Moon / Sensitive / Partnership,Moon / Diplomatic / Peacemaker,Moon / Emotional / Mulank 2,Earth / SW / Relationships (Position 2),High,Single digit 2 uniformly signifies lunar receptivity and diplomacy
Number 3 Archetype,Jupiter / Creative / Expansion,Jupiter / Expressive / Social,Jupiter / Wisdom / Mulank 3,Wood / East / Family (Position 3),High,Single digit 3 uniformly signifies growth wisdom and expansion
Number 4 Archetype,Uranus (Rahu) / Distinct / Sudden,Earth / Builder / Order,Rahu / Structure / Mulank 4,Wood / SE / Wealth (Position 4),Partial,System-specific: Vedic treats as Rahu; Western as Builder/Uranus
Number 5 Archetype,Mercury / Dynamic / Travel / Speech,Mercury / Versatile / Freedom,Mercury / Balance / Mulank 5,Earth / Center / Tai Chi (Position 5),High,Single digit 5 uniformly signifies central balance commerce and speed
Number 6 Archetype,Venus / Harmony / Luxury / Family,Venus / Nurturer / Responsibility,Venus / Beauty / Mulank 6,Metal / NW / Helpful Friends (Position 6),High,Single digit 6 uniformly signifies Venusian aesthetics luxury and duty
Number 7 Archetype,Neptune (Ketu) / Mystic / Solitary,Seven / Spiritual / Analyst,Ketu / Occult / Mulank 7,Metal / West / Children & Joy (Position 7),High,Single digit 7 uniformly signifies analytical spirituality and depth
Number 8 Archetype,Saturn / Karmic / Endurance / Duty,Saturn / Material / Power / Executive,Saturn / Justice / Mulank 8,Earth / NE / Knowledge (Position 8),High,Single digit 8 uniformly signifies Saturnian executive karma and structure
Number 9 Archetype,Mars / Sacred / Humanitarian / End,Mars / Universal Love / Completion,Mars / Energy / Mulank 9,Fire / South / Fame (Position 9),High,Single digit 9 uniformly signifies Mars energy completion and courage
Personal Year Cycle,9-year cyclical vibration,9-year cyclical epicycle,9-year transit cycle,9-year Ki / Lo Shu epicycle,Full,Uniform 9-year cycle calculated d+m+target_year
"""

with open("knowledge/analysis/consensus_matrix.csv", "w", encoding="utf-8") as f:
    f.write(consensus_csv.strip() + "\n")
print("Wrote knowledge/analysis/consensus_matrix.csv")

# 2. unique_methods.csv
unique_csv = """tradition,unique_method,deterministic_logic,source_reference,application_scope
Chaldean,Compound Number Interpretation (10-100+),Preserves compound total as primary karmic vibration rather than reducing immediately,B1 and B2,Name analysis and business brand evaluation
Chaldean,Sacred Exclusion of 9 from Alphabet,Digit 9 is never mapped to letters A-Z; assigned only to compound sums,B2 Section 7,Chaldean name calculation
Pythagorean,Master Numbers 11 / 22 / 33,Halts reduction at 11 22 and 33 to preserve master vibration,B2 Section 3,Western life path and expression numbers
Pythagorean,Sequential 1-9 Alphabet Mapping,Strict sequential assignment of letters A through Z to digits 1 to 9,B2 Section 3,Western name numerology
Chinese (Lo Shu),3x3 Magic Square Spatial Grid,Places birth digits into fixed 4-9-2 / 3-5-7 / 8-1-6 square,B3 Chapter 2,Spatial harmony planes and missing number remedies
Chinese (Lo Shu),8 Planes of Strength & Weakness,Evaluates rows columns and diagonals for complete presence or absence,B3 Chapter 3,Constitutional balance and personality matrix
Vedic,Driver (Mulank) and Conductor (Bhagyank),Strict reduction of birth day (Mulank) and complete birth date (Bhagyank),B1 and B2,Core character destiny and 81 archetype combinations
Vedic / Nadi,Dasha-First Timing (Mahadasha / Antardasha),Chronological planetary ruler periods dictate career and life timing windows,B1 and B2,Career rectification and predictive forecast windows
"""

with open("knowledge/analysis/unique_methods.csv", "w", encoding="utf-8") as f:
    f.write(unique_csv.strip() + "\n")
print("Wrote knowledge/analysis/unique_methods.csv")

# 3. conflict_register.csv
conflict_csv = """conflict_id,topic,tradition_a,tradition_b,severity,resolution_policy
CONF-001,Letter Alphabet Mapping,Chaldean: A-Z mapped 1-8 (9 excluded),Pythagorean: A-Z mapped 1-9 sequentially,High,Strict Isolation: User or route explicitly selects tradition. Never blend mappings.
CONF-002,Compound Number Reduction,Chaldean: Retains compound number (e.g. 33 24 19) as primary meaning,Pythagorean/Vedic: Reduces immediately to single digit or Master Number,Medium,Dual Display: Display compound vibration first with reduction root as planetary governor.
CONF-003,Number 4 Planetary Ruler,Vedic: Rahu (North Node of Moon),Pythagorean/Western: Uranus / Sun harmonic,Medium,Tradition-labeled Findings: Clearly label Vedic as Rahu and Western as Uranus.
CONF-004,Number 7 Planetary Ruler,Vedic: Ketu (South Node of Moon),Pythagorean/Western: Neptune / Spiritual Analyst,Medium,Tradition-labeled Findings: Clearly label Vedic as Ketu and Western as Neptune.
CONF-005,Master Number Recognition,Pythagorean: Acknowledges 11 22 33 as unreduced master vibrations,Vedic: Reduces all compound dates to single digit 1-9,Low,Contextual Authority: Pythagorean reports retain 11/22/33; Vedic reports display root 2/4/6.
"""

with open("knowledge/analysis/conflict_register.csv", "w", encoding="utf-8") as f:
    f.write(conflict_csv.strip() + "\n")
print("Wrote knowledge/analysis/conflict_register.csv")

# 4. gap_register.csv
gap_csv = """gap_id,domain_topic,missing_evidence_description,target_tradition,status,mandatory_abstention_action
GAP-001,Scanned Book Body Pages,B1 B3 B4 B5 B6 are image scans without validated text layer,All Traditions,PENDING_OCR,Strictly block unreviewed pages from production RAG retrieval
GAP-002,Exact Birth Time Astrological Ascendant,User has not provided exact hour/minute or timezone of birth,Vedic / KP Astrology,INSUFFICIENT_EVIDENCE,Abstain from calculating Ascendant or KP cusp houses; rely on Driver/Conductor
GAP-003,Unapproved Sports Rahu/Ketu Hypothesis,Proposal associating sports endurance with Saturn 8 / Ketu 7 lacks validated canon,Vedic Modern,UNCONFIGURED,Do not deploy or assert in client recommendations; retain as DRAFT
GAP-004,Foreign Name Phonetics Non-Latin,Transliteration of non-Latin scripts (Devanagari Cyrillic Chinese) into English letters,Chaldean / Pythagorean,UNCONFIGURED,Require user-approved Romanized phonetic spelling; do not fabricate transliterations
GAP-005,Medical Outcome Predictions,Attributing specific diseases or medical diagnoses to missing numbers,All Traditions,PERMANENTLY_BLOCKED,Statutory abstention under Drugs and Magic Remedies Act 1954
"""

with open("knowledge/analysis/gap_register.csv", "w", encoding="utf-8") as f:
    f.write(gap_csv.strip() + "\n")
print("Wrote knowledge/analysis/gap_register.csv")

# 5. method_authority_registry.yaml
method_yaml = """# NUMEROS VISION — METHOD AUTHORITY & SYSTEM PRECEDENCE REGISTRY
# Version: 1.0.0
# Last Updated: 2026-10-29

domains:
  name_analysis_and_balancing:
    primary_authority: "Chaldean"
    secondary_authority: "Pythagorean"
    precedence_rule: "Chaldean compound numbers (1-100) govern name vibration and spelling harmony. Pythagorean expression number provides secondary Western archetype."
    isolated_mappings: true

  timing_and_forecast_windows:
    primary_authority: "Numerology Mahadasha (Vedic)"
    secondary_authority: "Bhrigu Nandi Nadi / Transit Cross-Check"
    precedence_rule: "Numerological Dasha cycles establish the primary chronological time window. Astrological transits provide independent cross-verification without altering primary windows."
    abstention_on_missing_birth_time: false

  core_personality_and_destiny:
    primary_authority: "Vedic Mulank & Bhagyank (81 Combinations)"
    secondary_authority: "Chaldean Birthday Profile"
    precedence_rule: "Day of birth (Mulank) and full date of birth (Bhagyank) dictate the 81 driver-conductor archetypes. Chaldean compound birthday vibrations provide specific character nuances."
    isolated_mappings: true

  spatial_and_elemental_harmony:
    primary_authority: "Chinese Lo Shu (3x3 Magic Square)"
    secondary_authority: "Vedic Panch Tattva (Five Elements)"
    precedence_rule: "The 3x3 Magic Square (4-9-2 / 3-5-7 / 8-1-6) governs spatial directions, missing number remedies (Poorak), and the 8 planes of strength and weakness."
    isolated_mappings: true

  business_planetary_archetypes:
    primary_authority: "Contextual Archetype Engine (Section 16)"
    secondary_authority: "Chaldean Business Name Vibration"
    precedence_rule: "Evaluate business via contextual causal chain: business activity -> product function -> customer outcome -> candidate planetary archetypes. Never judge a business name or color in isolation."
    isolated_mappings: true
"""

with open("knowledge/analysis/method_authority_registry.yaml", "w", encoding="utf-8") as f:
    f.write(method_yaml.strip() + "\n")
print("Wrote knowledge/analysis/method_authority_registry.yaml")
