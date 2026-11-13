"""
NUMEROS VISION: MASTER CONTENT AND MONETISATION REGISTRY
Authoritative mapping for all 19 canonical routes:
- Route & canonical URL
- SEO Title & Meta Description
- Descriptive H1 & Introductory Copy
- Calculation Methods & Schemas
- Free Result Templates & Paid Report IDs
- CTA Labels & Internal Links
- Structured Data Schemas & Search Intent
"""

import json
from typing import Dict, Any, List

MASTER_PAGE_REGISTRY: Dict[str, Dict[str, Any]] = {
    "/": {
        "route": "/",
        "canonical_url": "https://numerosvision.com/",
        "page_title": "Numerology Calculators & Personalised Reports | Numeros Vision",
        "seo_title": "Numerology Calculators & Personalised Reports | Numeros Vision",
        "meta_description": "Explore birth-date, name and numerology calculators with personalised results, clear calculation methods and optional detailed reports.",
        "h1": "Explore Your Numbers, Names and Personal Numerology",
        "introductory_copy": "Numeros Vision brings numerology calculators, personalised interpretations and detailed reports together in one place. Explore what your birth date, name and selected numerology methods reveal within their respective calculation systems. Start with a free calculator, review your result and choose a detailed report if you want a deeper interpretation.",
        "primary_cta": {
            "text": "Try a Free Calculator",
            "url": "/numerology-calculators/"
        },
        "secondary_cta": {
            "text": "Explore Personalised Reports",
            "url": "/reports/"
        },
        "h2_sections": [
            {"title": "Find the Right Calculator", "desc": "Select from birth-date, name, Lo Shu Grid, or compatibility tools."},
            {"title": "Start with a Free Result", "desc": "Get deterministic mathematical calculations instantly with zero paywalls on baseline findings."},
            {"title": "Explore a Detailed Report", "desc": "Dive into deep multi-layer synthesis, 10-year Dasha timing maps, and custom planetary remedies."},
            {"title": "Understand the Calculation Method", "desc": "Transparent Chaldean, Pythagorean, Vedic, and Lo Shu mathematical frameworks."},
            {"title": "Frequently Asked Questions", "desc": "Common questions about numerological calculation methods and report deliverables."}
        ],
        "faqs": [
            {
                "q": "How does Numeros Vision calculate numerology results?",
                "a": "Numeros Vision uses 100% deterministic mathematical calculation engines based on authentic classical Chaldean, Pythagorean, Vedic, and Lo Shu systems. All calculations are executed on the server with zero artificial variance."
            },
            {
                "q": "What is the difference between free results and detailed reports?",
                "a": "Free calculator results display the exact mathematical reduction, root number, and foundational interpretation. Detailed paid reports provide 3 to 32 pages of deep multi-year timing roadmaps, compound matrix interactions, and safe planetary remedies."
            }
        ],
        "primary_keyword": "numerology calculators",
        "search_intent": "Informational / Commercial",
        "calculator_id": "all",
        "paid_report_id": "report_essential",
        "internal_links": [
            {"anchor": "All Numerology Calculators", "url": "/numerology-calculators/"},
            {"anchor": "Personalised Reports", "url": "/reports/"},
            {"anchor": "Calculation Methodology", "url": "/numerology-methodology/"},
            {"anchor": "Charm AI", "url": "/charm-ai/"}
        ],
        "structured_data_types": ["Organization", "WebSite", "SoftwareApplication"],
        "indexability": "index, follow"
    },
    "/numerology-calculators/": {
        "route": "/numerology-calculators/",
        "canonical_url": "https://numerosvision.com/numerology-calculators/",
        "page_title": "Free Numerology Calculators | Birth Date, Name & More",
        "seo_title": "Free Numerology Calculators | Birth Date, Name & More",
        "meta_description": "Choose a numerology calculator for your birth date, name, Lo Shu Grid, compatibility or other supported calculations.",
        "h1": "Choose Your Numerology Calculator",
        "introductory_copy": "Start with the question you want to explore. Choose a calculator, enter the required details and view your result before deciding whether you need a detailed report.",
        "primary_cta": {
            "text": "Calculate Free",
            "url": "#calculator-grid"
        },
        "secondary_cta": {
            "text": "Compare Reports",
            "url": "/reports/"
        },
        "h2_sections": [
            {"title": "Birth-Date Calculators", "desc": "Explore your Life Path, Mulank, and personal milestone cycles."},
            {"title": "Name & Sound Harmonization", "desc": "Chaldean, Pythagorean, and baby naming letter-value systems."},
            {"title": "Relationship & Compatibility", "desc": "Dual-chart harmony, element balance, and compound connection scores."},
            {"title": "Business & Environmental Alignment", "desc": "Brand name, mobile number, property, and directional compatibility."}
        ],
        "faqs": [
            {
                "q": "Are all calculators on this directory free to use?",
                "a": "Yes. Every verified calculator generates your complete mathematical calculation and foundational baseline interpretation at zero cost."
            }
        ],
        "primary_keyword": "free numerology calculators",
        "search_intent": "Informational / Navigational",
        "calculator_id": "directory",
        "paid_report_id": "report_essential",
        "internal_links": [
            {"anchor": "Birth Date Numerology", "url": "/birth-date-numerology/"},
            {"anchor": "Life Path Calculator", "url": "/life-path-number-calculator/"},
            {"anchor": "Name Numerology", "url": "/name-numerology-calculator/"},
            {"anchor": "Chaldean Numerology", "url": "/chaldean-numerology/"},
            {"anchor": "Lo Shu Grid", "url": "/lo-shu-grid-calculator/"},
            {"anchor": "Compatibility Calculator", "url": "/numerology-compatibility-calculator/"}
        ],
        "structured_data_types": ["BreadcrumbList", "CollectionPage"],
        "indexability": "index, follow"
    },
    "/birth-date-numerology/": {
        "route": "/birth-date-numerology/",
        "canonical_url": "https://numerosvision.com/birth-date-numerology/",
        "page_title": "Birth Date Numerology Calculator | Numeros Vision",
        "seo_title": "Birth Date Numerology Calculator | Numeros Vision",
        "meta_description": "Calculate the numerology numbers associated with your date of birth and explore a personalised interpretation.",
        "h1": "Birth Date Numerology Calculator",
        "introductory_copy": "Your date of birth is the starting point for several numerology calculations. Enter your birth date to calculate the numbers supported by this tool and review their interpretation under the selected method.",
        "primary_cta": {
            "text": "Calculate Birth Numbers",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Explore Your Detailed Birth-Date Report",
            "url": "/reports/#report-basic"
        },
        "h2_sections": [
            {"title": "What the Calculator Measures", "desc": "Calculates your Driver Number (Mulank) from your birth day and Conductor Number (Bhagyank) from full birth date."},
            {"title": "How the Calculation Works", "desc": "Reduces multi-digit calendar numbers to single root integers (1-9) or recognized master vibrations."},
            {"title": "What the Free Result Includes", "desc": "Exact root numbers, ruling planet associations, elemental affinities, and core trait summary."},
            {"title": "What a Detailed Report Adds", "desc": "Multi-tier 10-year Dasha timeline, missing Lo Shu number remedies, and safe gemstone prescriptions."}
        ],
        "faqs": [
            {
                "q": "What is the difference between Driver and Conductor numbers?",
                "a": "The Driver (Mulank) is derived solely from the day you were born and reflects your inner temperament. The Conductor (Bhagyank) is the sum of the entire date of birth (DD+MM+YYYY) and indicates life direction."
            }
        ],
        "primary_keyword": "birth date numerology calculator",
        "search_intent": "Informational / Transactional",
        "calculator_id": "birth_number",
        "paid_report_id": "report_essential",
        "internal_links": [
            {"anchor": "Life Path Calculator", "url": "/life-path-number-calculator/"},
            {"anchor": "Lo Shu Grid", "url": "/lo-shu-grid-calculator/"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/life-path-number-calculator/": {
        "route": "/life-path-number-calculator/",
        "canonical_url": "https://numerosvision.com/life-path-number-calculator/",
        "page_title": "Life Path Number Calculator | Calculate Your Number",
        "seo_title": "Life Path Number Calculator | Calculate Your Number",
        "meta_description": "Calculate your Life Path number from your birth date and explore its interpretation using the stated numerology method.",
        "h1": "Calculate Your Life Path Number",
        "introductory_copy": "Use your date of birth to calculate your Life Path number. Review the calculation and explore a concise interpretation before choosing whether to view a more detailed report.",
        "primary_cta": {
            "text": "Calculate Life Path Number",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Explore Your Detailed Life Path Report",
            "url": "/reports/#report-basic"
        },
        "h2_sections": [
            {"title": "Life Path Calculation Method", "desc": "Summing all digits of your full birth date (DD-MM-YYYY) and reducing strictly to a single digit from 1 to 9."},
            {"title": "Your Free Calculation Result", "desc": "Exact single-digit Life Path number (1–9), reduction steps, governing planetary archetype, and primary life lesson."},
            {"title": "Detailed Life Path Report Deliverables", "desc": "Career milestone timing, relationship dynamics with other Life Paths, and practical alignment steps."}
        ],
        "faqs": [
            {
                "q": "Are master numbers 11, 22, and 33 reduced to single digits?",
                "a": "Yes. Numeros Vision calculators and reports always reduce every derived number—including 11, 22, and 33—fully to a single digit from 1 to 9 (2, 4, and 6)."
            }
        ],
        "primary_keyword": "life path number calculator",
        "search_intent": "Informational / Transactional",
        "calculator_id": "life_path",
        "paid_report_id": "report_essential",
        "internal_links": [
            {"anchor": "Birth Date Numerology", "url": "/birth-date-numerology/"},
            {"anchor": "Compatibility Calculator", "url": "/numerology-compatibility-calculator/"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/name-numerology-calculator/": {
        "route": "/name-numerology-calculator/",
        "canonical_url": "https://numerosvision.com/name-numerology-calculator/",
        "page_title": "Name Numerology Calculator | Calculate Your Name Number",
        "seo_title": "Name Numerology Calculator | Calculate Your Name Number",
        "meta_description": "Calculate your name number using a stated numerology system and explore the result with an optional personalised report.",
        "h1": "Name Numerology Calculator",
        "introductory_copy": "Explore the number associated with a name using your chosen numerology method. Enter the name in the requested format and review the letter values and final calculation.",
        "primary_cta": {
            "text": "Calculate Name Number",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Explore Your Detailed Name Report",
            "url": "/reports/#report-master"
        },
        "h2_sections": [
            {"title": "Letter-Value Reduction Framework", "desc": "Every alphabet letter corresponds to a distinct vibrational integer according to classical tables."},
            {"title": "Free Name Analysis Output", "desc": "Full letter breakdown, compound sum, single-digit root, and vibrational harmony with your birth date."},
            {"title": "Detailed Name Balancing Report", "desc": "Alternative spelling adjustments, compound number destiny (10-99), and calling-name resonance."}
        ],
        "faqs": [
            {
                "q": "Should I use my legal name or calling name?",
                "a": "For complete legal destiny analysis, enter your official full birth name. For active social and professional resonance, analyze the daily calling name."
            }
        ],
        "primary_keyword": "name numerology calculator",
        "search_intent": "Informational / Commercial",
        "calculator_id": "name_numerology",
        "paid_report_id": "report_master",
        "internal_links": [
            {"anchor": "Chaldean Numerology", "url": "/chaldean-numerology/"},
            {"anchor": "Name Balancing", "url": "/tools/name-balancing"},
            {"anchor": "Business Name Numerology", "url": "/business-name-numerology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/chaldean-numerology/": {
        "route": "/chaldean-numerology/",
        "canonical_url": "https://numerosvision.com/chaldean-numerology/",
        "page_title": "Chaldean Numerology Calculator | Name Number Analysis",
        "seo_title": "Chaldean Numerology Calculator | Name Number Analysis",
        "meta_description": "Explore name numerology using the Chaldean system, with visible letter values, calculation steps and optional detailed analysis.",
        "h1": "Chaldean Numerology Calculator",
        "introductory_copy": "The Chaldean system assigns numerical values to letters according to its own mapping. Use this calculator to view a name's calculated number and understand how the selected mapping produces the result.",
        "primary_cta": {
            "text": "Calculate Chaldean Name",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Explore Your Chaldean Name Report",
            "url": "/reports/#report-master"
        },
        "h2_sections": [
            {"title": "The Chaldean Letter Mapping", "desc": "Letters A through Z mapped to values 1 through 8 (9 is considered sacred and held unassigned to letters)."},
            {"title": "Compound Numbers (10 to 99)", "desc": "The esoteric Chaldean compound meaning behind the final sum, representing inner hidden forces."},
            {"title": "Harmonizing Name with Driver and Conductor", "desc": "Validating whether the compound sum creates supportive harmony with your birth root numbers."}
        ],
        "faqs": [
            {
                "q": "Why is the number 9 omitted from Chaldean letter values?",
                "a": "In Chaldean tradition, 9 represents the divine circle of completion and is not mapped to individual letters, though it can emerge as a final sum."
            }
        ],
        "primary_keyword": "chaldean numerology calculator",
        "search_intent": "Informational / Commercial",
        "calculator_id": "chaldean_numerology",
        "paid_report_id": "report_master",
        "internal_links": [
            {"anchor": "Name Numerology", "url": "/name-numerology-calculator/"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"},
            {"anchor": "Compound Numbers Guide", "url": "/blog/chaldean-compound-numbers-meanings"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/lo-shu-grid-calculator/": {
        "route": "/lo-shu-grid-calculator/",
        "canonical_url": "https://numerosvision.com/lo-shu-grid-calculator/",
        "page_title": "Lo Shu Grid Calculator | Birth Date Number Grid",
        "seo_title": "Lo Shu Grid Calculator | Birth Date Number Grid",
        "meta_description": "Generate your Lo Shu Grid from your birth date and review its number distribution and interpretation.",
        "h1": "Lo Shu Grid Calculator",
        "introductory_copy": "The Lo Shu Grid organises eligible birth-date digits into a numerical grid. Generate your grid to see which numbers appear, how frequently they appear and which positions are empty under the configured rules.",
        "primary_cta": {
            "text": "Generate Lo Shu Grid",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Explore Your Detailed Lo Shu Report",
            "url": "/reports/#report-master"
        },
        "h2_sections": [
            {"title": "The 3x3 Magic Square Structure", "desc": "Grid arrangement 4-9-2 (top), 3-5-7 (middle), 8-1-6 (bottom), where every row, column, and diagonal sums to 15."},
            {"title": "The 8 Planes of Life", "desc": "Mental, Emotional, Practical horizontal planes; Thought, Will, Action vertical planes; Golden and Silver Yogas."},
            {"title": "Missing Number Balancers", "desc": "Physical, crystal, and directional remedies to balance empty sectors in your grid."}
        ],
        "faqs": [
            {
                "q": "What do repeated numbers in the Lo Shu grid indicate?",
                "a": "A number appearing multiple times highlights an amplified energy focal point, while empty positions indicate areas requiring conscious balancing."
            }
        ],
        "primary_keyword": "lo shu grid calculator",
        "search_intent": "Informational / Transactional",
        "calculator_id": "lo_shu_grid",
        "paid_report_id": "report_master",
        "internal_links": [
            {"anchor": "Birth Date Numerology", "url": "/birth-date-numerology/"},
            {"anchor": "Lo Shu 8 Planes Guide", "url": "/blog/lo-shu-grid-8-planes"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/numerology-compatibility-calculator/": {
        "route": "/numerology-compatibility-calculator/",
        "canonical_url": "https://numerosvision.com/numerology-compatibility-calculator/",
        "page_title": "Numerology Compatibility Calculator | Compare Two Profiles",
        "seo_title": "Numerology Compatibility Calculator | Compare Two Profiles",
        "meta_description": "Compare two profiles using the selected numerology compatibility method and review the calculation behind the result.",
        "h1": "Numerology Compatibility Calculator",
        "introductory_copy": "Compare two profiles using the numerology method available in this tool. Review the calculated values and understand which factors contribute to the compatibility result.",
        "primary_cta": {
            "text": "Calculate Compatibility",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Explore Your Detailed Compatibility Report",
            "url": "/reports/#report-master"
        },
        "h2_sections": [
            {"title": "Dual-Profile Planetary Matrix", "desc": "Comparing Driver, Conductor, and Life Path planetary rulers across natural friend, neutral, and friction matrices."},
            {"title": "The 5 Elements Interaction", "desc": "Analyzing elemental affinities (Wood, Fire, Earth, Metal, Water) between both partners."},
            {"title": "Practical Synergy Guidance", "desc": "Objective communication and milestone insights without deterministic outcome guarantees."}
        ],
        "faqs": [
            {
                "q": "Can numerology predict relationship success?",
                "a": "Numerology evaluates energetic and psychological compatibility traits. It highlights areas of natural ease and potential friction for conscious personal reflection, not absolute outcomes."
            }
        ],
        "primary_keyword": "numerology compatibility calculator",
        "search_intent": "Informational / Commercial",
        "calculator_id": "compatibility",
        "paid_report_id": "report_master",
        "internal_links": [
            {"anchor": "Life Path Calculator", "url": "/life-path-number-calculator/"},
            {"anchor": "Birth Date Numerology", "url": "/birth-date-numerology/"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/business-name-numerology/": {
        "route": "/business-name-numerology/",
        "canonical_url": "https://numerosvision.com/business-name-numerology/",
        "page_title": "Business Name Numerology Calculator | Name Analysis",
        "seo_title": "Business Name Numerology Calculator | Name Analysis",
        "meta_description": "Calculate a business name number using the selected numerology method and explore a detailed name-analysis report.",
        "h1": "Business Name Numerology Calculator",
        "introductory_copy": "A business name can be analysed numerically using a defined name-number system. Enter your proposed name and review the calculation, the selected method and the interpretation available through Numeros Vision.",
        "primary_cta": {
            "text": "Analyze Business Name",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Compare Your Business Name Options",
            "url": "/reports/#report-divine"
        },
        "h2_sections": [
            {"title": "Corporate Vibrational Archetypes", "desc": "Evaluating commercial names against founder birth numbers and industry sector planetary rulers."},
            {"title": "Commercial Causal Chain", "desc": "Analyzing business activity to product function to customer outcome to candidate planetary archetypes."},
            {"title": "Brand Alignment Dossier", "desc": "Side-by-side comparison of candidate names, root compound wealth numbers (1, 3, 5, 6), and brand color guidance."}
        ],
        "faqs": [
            {
                "q": "Which numbers are considered auspicious for business names?",
                "a": "Commercial naming typically favors root sums of 1 (leadership), 3 (expansion/knowledge), 5 (mercantile trade/agility), or 6 (luxury/Venusian appeal), aligned with the founder's Driver number."
            }
        ],
        "primary_keyword": "business name numerology calculator",
        "search_intent": "Commercial / Transactional",
        "calculator_id": "business_numerology",
        "paid_report_id": "report_divine",
        "internal_links": [
            {"anchor": "Chaldean Numerology", "url": "/chaldean-numerology/"},
            {"anchor": "Logo Intelligence", "url": "/tools/logo-intelligence"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/mobile-number-numerology/": {
        "route": "/mobile-number-numerology/",
        "canonical_url": "https://numerosvision.com/mobile-number-numerology/",
        "page_title": "Mobile Number Numerology Calculator | Number Analysis",
        "seo_title": "Mobile Number Numerology Calculator | Number Analysis",
        "meta_description": "Analyse a mobile number using a clearly stated numerology method and explore an optional detailed report.",
        "h1": "Mobile Number Numerology Calculator",
        "introductory_copy": "Explore a mobile number using the number-processing method stated by this calculator. Review the resulting total and interpretation, and decide whether a detailed analysis would be useful.",
        "primary_cta": {
            "text": "Audit Mobile Number",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Explore Your Detailed Number Analysis",
            "url": "/reports/#report-basic"
        },
        "h2_sections": [
            {"title": "Digit Sum & Adjacent Digit Pairs", "desc": "Calculating the total number reduction and checking for high-friction internal pairings."},
            {"title": "Privacy & Data Minimization", "desc": "Mobile numbers are processed transiently in memory for calculation and never stored in analytics or marketing lists."},
            {"title": "Optimizing Your Digital Touchpoint", "desc": "Identifying whether your active communication frequency aligns with your primary profession."}
        ],
        "faqs": [
            {
                "q": "Is my phone number saved when I check it?",
                "a": "No. In strict compliance with DPDP 2025 and data minimization standards, phone numbers entered are calculated in volatile memory and never persisted or shared."
            }
        ],
        "primary_keyword": "mobile number numerology calculator",
        "search_intent": "Informational / Commercial",
        "calculator_id": "mobile_numerology",
        "paid_report_id": "report_essential",
        "internal_links": [
            {"anchor": "Mobile Malefic Pairs Guide", "url": "/blog/mobile-numerology-malefic-pairs"},
            {"anchor": "Birth Date Numerology", "url": "/birth-date-numerology/"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/baby-name-numerology/": {
        "route": "/baby-name-numerology/",
        "canonical_url": "https://numerosvision.com/baby-name-numerology/",
        "page_title": "Baby Name Numerology Calculator | Compare Names",
        "seo_title": "Baby Name Numerology Calculator | Compare Names",
        "meta_description": "Calculate candidate baby-name numbers using the selected numerology system and compare their numerical results.",
        "h1": "Baby Name Numerology Calculator",
        "introductory_copy": "Explore candidate names through a clearly identified numerology method. Calculate each name consistently and compare the results to help organise your shortlist.",
        "primary_cta": {
            "text": "Evaluate Baby Names",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Compare Your Shortlisted Names",
            "url": "/reports/#report-master"
        },
        "h2_sections": [
            {"title": "Harmonizing Name with Date of Birth", "desc": "Calculating candidate spelling options that harmonize with the child's natural Driver and Conductor numbers."},
            {"title": "Ethical Presentation Standards", "desc": "Numeros Vision never makes deterministic fatalistic predictions regarding health or life longevity."},
            {"title": "Shortlist Organization", "desc": "Organizing family-selected names by syllable strength, compound vibration, and planetary affinity."}
        ],
        "faqs": [
            {
                "q": "How does baby naming numerology work with birth dates?",
                "a": "The child's birth date establishes immutable core planetary influences (Driver and Conductor). The name provides an adjustable sound vibration selected to support those natural traits."
            }
        ],
        "primary_keyword": "baby name numerology calculator",
        "search_intent": "Commercial / Transactional",
        "calculator_id": "baby_naming",
        "paid_report_id": "report_master",
        "internal_links": [
            {"anchor": "Name Numerology", "url": "/name-numerology-calculator/"},
            {"anchor": "Chaldean Numerology", "url": "/chaldean-numerology/"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/lucky-number-calculator/": {
        "route": "/lucky-number-calculator/",
        "canonical_url": "https://numerosvision.com/lucky-number-calculator/",
        "page_title": "Numerology Number Calculator | Explore Your Numbers",
        "seo_title": "Numerology Number Calculator | Explore Your Numbers",
        "meta_description": "Calculate selected numerology numbers from your birth date and explore how they are interpreted within the chosen system.",
        "h1": "Explore Your Numerology Numbers",
        "introductory_copy": "Calculate the numbers associated with your birth date and see how they are interpreted under the selected numerology framework. The result explains the method used rather than presenting a number as a guarantee of future outcomes.",
        "primary_cta": {
            "text": "Calculate Numbers",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Explore Your Personal Number Report",
            "url": "/reports/#report-basic"
        },
        "h2_sections": [
            {"title": "Mathematical Derivation of Harmonic Numbers", "desc": "Identifying friendly and supportive numerical frequencies based on classical ruler planetary relationships."},
            {"title": "Responsible Guidance", "desc": "Numbers represent focal energetic alignment for personal scheduling and focus, not magical fortune or gambling predictions."},
            {"title": "Auspicious Timing & Milestone Planning", "desc": "Understanding supportive calendar days and monthly cycles for initiating important projects."}
        ],
        "faqs": [
            {
                "q": "What makes a number 'lucky' in numerology?",
                "a": "A number is considered supportive when its governing planetary archetype shares a natural friendship matrix with your Driver and Conductor numbers."
            }
        ],
        "primary_keyword": "numerology number calculator",
        "search_intent": "Informational / Transactional",
        "calculator_id": "lucky_number",
        "paid_report_id": "report_essential",
        "internal_links": [
            {"anchor": "Birth Date Numerology", "url": "/birth-date-numerology/"},
            {"anchor": "Personal Year Calculator", "url": "/personal-year-numerology/"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/personal-year-numerology/": {
        "route": "/personal-year-numerology/",
        "canonical_url": "https://numerosvision.com/personal-year-numerology/",
        "page_title": "Personal Year Number Calculator | Numerology",
        "seo_title": "Personal Year Number Calculator | Numerology",
        "meta_description": "Calculate your personal-year number for the selected year and explore its interpretation using the stated method.",
        "h1": "Personal Year Number Calculator",
        "introductory_copy": "Calculate your personal-year number for a selected year and review its interpretation within the chosen numerology system. The calculation should use the date and year conventions configured in the application.",
        "primary_cta": {
            "text": "Calculate Personal Year",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Explore Your Detailed Personal Year Report",
            "url": "/reports/#report-master"
        },
        "h2_sections": [
            {"title": "The 9-Year Epicycle of Growth", "desc": "Summing your birth day, birth month, and the current universal calendar year to identify your active developmental theme."},
            {"title": "Yearly Themes (1 through 9)", "desc": "From Year 1 (seed planting / new beginnings) through Year 9 (culmination / release and completion)."},
            {"title": "Detailed Timing Roadmap", "desc": "Integrating Personal Year with your active Numerology Dasha Mahadasha and Antardasha timing windows."}
        ],
        "faqs": [
            {
                "q": "Does a Personal Year change on January 1st or on my birthday?",
                "a": "In traditional calendar numerology, the universal year transitions on January 1st, while your personal vibrational focus intensifies from your birthday."
            }
        ],
        "primary_keyword": "personal year number calculator",
        "search_intent": "Informational / Transactional",
        "calculator_id": "personal_year",
        "paid_report_id": "report_master",
        "internal_links": [
            {"anchor": "Blessing Years Timeline", "url": "/tools/blessing-years"},
            {"anchor": "Birth Date Numerology", "url": "/birth-date-numerology/"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/city-name-numerology/": {
        "route": "/city-name-numerology/",
        "canonical_url": "https://numerosvision.com/city-name-numerology/",
        "page_title": "City Name Numerology Calculator | Compare City Names",
        "seo_title": "City Name Numerology Calculator | Compare City Names",
        "meta_description": "Calculate city-name numbers using the selected numerology method and compare supported city-name results.",
        "h1": "City Name Numerology Calculator",
        "introductory_copy": "Explore city names through the selected numerology method. Calculate each name consistently and compare the resulting numbers and interpretations.",
        "primary_cta": {
            "text": "Analyze City Resonance",
            "url": "#city-form"
        },
        "secondary_cta": {
            "text": "Compare Your Selected Cities",
            "url": "/reports/#report-master"
        },
        "h2_sections": [
            {"title": "City Name Chaldean Reduction", "desc": "Evaluating municipal name vibrations (e.g. New York 39/12/3 Jupiter, London 24/6 Venus, Bengaluru 33/6 Venus)."},
            {"title": "Personal Harmony Matrix", "desc": "Cross-referencing city compound numbers against your personal Driver and Conductor numbers."},
            {"title": "Objective Method Scope", "desc": "City numerology provides linguistic and vibrational reflection; it does not claim objective geographic luck or replace economic factors."}
        ],
        "faqs": [
            {
                "q": "Does moving to a compatible city guarantee commercial success?",
                "a": "No. Numerology evaluates name vibration alignment with personal birth numbers. Real-world career growth depends on market demand, personal diligence, and practical execution."
            }
        ],
        "primary_keyword": "city name numerology calculator",
        "search_intent": "Informational / Commercial",
        "calculator_id": "city_numerology",
        "paid_report_id": "report_master",
        "internal_links": [
            {"anchor": "Worldwide City Hub", "url": "/local-hub"},
            {"anchor": "Name Numerology", "url": "/name-numerology-calculator/"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/numerology-direction-alignment/": {
        "route": "/numerology-direction-alignment/",
        "canonical_url": "https://numerosvision.com/numerology-direction-alignment/",
        "page_title": "Personal Number and Direction Analysis | Numeros Vision",
        "seo_title": "Personal Number and Direction Analysis | Numeros Vision",
        "meta_description": "Explore direction-related analysis using the method and inputs supported by the application.",
        "h1": "Explore Directional Alignment",
        "introductory_copy": "This tool evaluates direction-related inputs using its stated methodology. Review the inputs, calculation rules and interpretation before using the result as one perspective for personal reflection.",
        "primary_cta": {
            "text": "Evaluate Direction Alignment",
            "url": "#calculator-form"
        },
        "secondary_cta": {
            "text": "Explore Your Detailed Alignment Report",
            "url": "/reports/#report-master"
        },
        "h2_sections": [
            {"title": "Kua Number & Cardinal Planetary Directions", "desc": "Calculating your personal Kua number from birth year and gender to identify traditional auspicious compass orientations."},
            {"title": "Workplace & Desk Orientation", "desc": "Practical suggestions for desk orientation (East, North, Northeast) based on primary planetary ruler."},
            {"title": "Methodological Scope", "desc": "Provides architectural alignment perspectives without fabricating compass readings or claiming absolute Vastu remedies."}
        ],
        "faqs": [
            {
                "q": "How is the Kua number calculated?",
                "a": "The Kua number is derived from the lunar birth year and gender, mapping individuals to East or West group cardinal direction affinities."
            }
        ],
        "primary_keyword": "personal number and direction analysis",
        "search_intent": "Informational / Commercial",
        "calculator_id": "direction_alignment",
        "paid_report_id": "report_master",
        "internal_links": [
            {"anchor": "Kua Directions Guide", "url": "/blog/kua-number-auspicious-directions-and-career-feng-shui"},
            {"anchor": "Property Numerology", "url": "/tools/property-numerology"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/charm-ai/": {
        "route": "/charm-ai/",
        "canonical_url": "https://numerosvision.com/charm-ai/",
        "page_title": "Charm AI | Personalised Numerology Insights",
        "seo_title": "Charm AI | Personalised Numerology Insights",
        "meta_description": "Explore numerology questions and personalised interpretations using Charm AI and the methods supported by Numeros Vision.",
        "h1": "Explore Your Numerology Questions with Charm AI",
        "introductory_copy": "Charm AI helps you explore the calculations and interpretations available through Numeros Vision. Ask a question, review the explanation and explore a detailed report when you want additional analysis.",
        "primary_cta": {
            "text": "Ask Charm AI",
            "url": "#chat-input"
        },
        "secondary_cta": {
            "text": "Explore a Detailed Personal Report",
            "url": "/reports/"
        },
        "h2_sections": [
            {"title": "Supported Questions", "desc": "Inquire about career timing, life purpose, name compatibility, and planetary cycle milestones."},
            {"title": "Deterministic Engine Grounding", "desc": "Charm AI explains verified calculations; it never hallucinates numerological sums or overrides mathematical outputs."},
            {"title": "Privacy & Ephemeral Memory", "desc": "Conversations are private, session-scoped, and protected under statutory DPDP 2025 consent protocols."}
        ],
        "faqs": [
            {
                "q": "Can Charm AI calculate new numbers by itself?",
                "a": "No. 100% of calculations are performed by our deterministic Python calculation engine. Charm AI is strictly an interpretive guide explaining verified results."
            }
        ],
        "primary_keyword": "charm ai numerology insights",
        "search_intent": "Informational / Commercial",
        "calculator_id": "charm_ai",
        "paid_report_id": "starter_5q",
        "internal_links": [
            {"anchor": "All Calculators", "url": "/numerology-calculators/"},
            {"anchor": "Personalised Reports", "url": "/reports/"},
            {"anchor": "Methodology", "url": "/numerology-methodology/"}
        ],
        "structured_data_types": ["SoftwareApplication", "FAQPage"],
        "indexability": "index, follow"
    },
    "/reports/": {
        "route": "/reports/",
        "canonical_url": "https://numerosvision.com/reports/",
        "page_title": "Personalised Numerology Reports | Compare Report Options",
        "seo_title": "Personalised Numerology Reports | Compare Report Options",
        "meta_description": "Compare available numerology reports, understand what each includes and choose the level of detail that suits your needs.",
        "h1": "Choose Your Personalised Numerology Report",
        "introductory_copy": "Start with a free calculation, then choose a report if you want a more detailed interpretation. Each report should explain what it includes, which inputs it uses and what additional information it provides beyond the free result.",
        "primary_cta": {
            "text": "View Anveil my alignments",
            "url": "/pricing#basic"
        },
        "secondary_cta": {
            "text": "Explore Advanced Analysis",
            "url": "/pricing#advanced"
        },
        "h2_sections": [
            {"title": "Basic Numerology Report (3 Pages)", "desc": "Core Identity, Mulank & Bhagyank, basic Lo Shu 3x3 Grid, 1-year snapshot & primary color/gemstone guide."},
            {"title": "Advanced Numerology Report (12 Pages)", "desc": "A more detailed report providing expanded interpretations, relevant number relationships and additional analysis supported by the selected product."},
            {"title": "Premium Numerology Report (32 Pages)", "desc": "An extensive report bringing together the supported calculations, detailed interpretations, relevant comparisons and personalised recommendations available for the selected product."}
        ],
        "faqs": [
            {
                "q": "What are the verified page lengths of the report tiers?",
                "a": "Basic is 3 pages, Advanced is 12 pages, and Premium is 32 pages of focused, non-repetitive analysis grounded in authentic classical treatises."
            }
        ],
        "primary_keyword": "personalised numerology reports",
        "search_intent": "Commercial / Transactional",
        "calculator_id": "reports",
        "paid_report_id": "report_essential",
        "internal_links": [
            {"anchor": "Pricing and Plans", "url": "/pricing"},
            {"anchor": "Sample Report", "url": "/sample"},
            {"anchor": "All Calculators", "url": "/numerology-calculators/"}
        ],
        "structured_data_types": ["Product", "Offer", "CollectionPage"],
        "indexability": "index, follow"
    },
    "/numerology-methodology/": {
        "route": "/numerology-methodology/",
        "canonical_url": "https://numerosvision.com/numerology-methodology/",
        "page_title": "Numerology Methods & Calculation Rules | Numeros Vision",
        "seo_title": "Numerology Methods & Calculation Rules | Numeros Vision",
        "meta_description": "Learn how Numeros Vision calculates and interprets supported numerology results, including the methods used and their limitations.",
        "h1": "Understand How Your Numerology Results Are Calculated",
        "introductory_copy": "Numeros Vision aims to make its calculations transparent. Each tool should identify the numerology system it uses, show the relevant calculation steps and distinguish calculated values from interpretive commentary.",
        "primary_cta": {
            "text": "Try a Calculator",
            "url": "/numerology-calculators/"
        },
        "secondary_cta": {
            "text": "Explore Personalised Reports",
            "url": "/reports/"
        },
        "h2_sections": [
            {"title": "Supported Systems", "desc": "Mathematical foundations of Chaldean sound mapping, Pythagorean geometry, Vedic planetary friendship, and Lo Shu 3x3 grids."},
            {"title": "Separation of Math and Interpretation", "desc": "Every output clearly delineates deterministic calculations from historical symbolic associations."},
            {"title": "Anti-Hallucination Governance", "desc": "Zero AI fabrication of dates, lucky numbers, or life milestones. AI only formats validated outputs."}
        ],
        "faqs": [
            {
                "q": "Why do Chaldean and Pythagorean systems produce different numbers for the same name?",
                "a": "Chaldean uses an ancient 1-8 sound frequency matrix originating in Babylon, whereas Pythagorean uses sequential 1-9 Greek geometric letter indexing."
            }
        ],
        "primary_keyword": "numerology methodology",
        "search_intent": "Informational",
        "calculator_id": "methodology",
        "paid_report_id": "report_essential",
        "internal_links": [
            {"anchor": "All Calculators", "url": "/numerology-calculators/"},
            {"anchor": "Chaldean vs Pythagorean", "url": "/blog/chaldean-vs-pythagorean-numerology"},
            {"anchor": "Reports Catalogue", "url": "/reports/"}
        ],
        "structured_data_types": ["Article", "FAQPage"],
        "indexability": "index, follow"
    },
    "/insights/": {
        "route": "/insights/",
        "canonical_url": "https://numerosvision.com/insights/",
        "page_title": "Numerology Guides, Calculations & Insights | Numeros Vision",
        "seo_title": "Numerology Guides, Calculations & Insights | Numeros Vision",
        "meta_description": "Read concise guides to numerology calculations, name numbers, birth-date numbers and the methods used by Numeros Vision.",
        "h1": "Numerology Guides and Insights",
        "introductory_copy": "Explore how numerology calculations work, what different systems measure and how to interpret your results. Each guide connects to a relevant calculator so you can move from learning to a calculation of your own.",
        "primary_cta": {
            "text": "Explore All Guides",
            "url": "#guides-list"
        },
        "secondary_cta": {
            "text": "Try a Free Calculator",
            "url": "/numerology-calculators/"
        },
        "h2_sections": [
            {"title": "Core Educational Articles", "desc": "Deep dives into Life Path calculations, Chaldean compound numbers, and Lo Shu planes."},
            {"title": "Connecting Theory to Calculators", "desc": "Every insight links directly to its live deterministic calculator."},
            {"title": "Practical Lifestyle & Gemstone Harmonizers", "desc": "Authentic Vedic and crystal harmonizers based on classical compendiums."}
        ],
        "faqs": [
            {
                "q": "Are the numerology insights based on traditional texts?",
                "a": "Yes. Our guides reference authentic Chaldean records, Vedic classical treatises, and classical Lo Shu mathematical traditions."
            }
        ],
        "primary_keyword": "numerology guides and insights",
        "search_intent": "Informational",
        "calculator_id": "insights",
        "paid_report_id": "report_essential",
        "internal_links": [
            {"anchor": "How to Calculate Life Path", "url": "/blog/life-path-numbers-explained"},
            {"anchor": "Chaldean vs Pythagorean", "url": "/blog/chaldean-vs-pythagorean-numerology"},
            {"anchor": "Lo Shu 8 Planes", "url": "/blog/lo-shu-grid-8-planes"},
            {"anchor": "All Calculators", "url": "/numerology-calculators/"}
        ],
        "structured_data_types": ["CollectionPage", "FAQPage"],
        "indexability": "index, follow"
    }
}

def export_json(path="configuration/master_content_config.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(MASTER_PAGE_REGISTRY, f, indent=2, ensure_ascii=False)
    print(f"Exported master content registry with {len(MASTER_PAGE_REGISTRY)} canonical pages to {path}")

if __name__ == "__main__":
    export_json()
