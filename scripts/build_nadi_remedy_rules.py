import json
from datetime import datetime

remedy_registry = {
    "version": "1.0.0",
    "updated_at": datetime.now().isoformat(),
    "primary_source": "Numeros Vision Classical Nadi Event System (Classical Nadi Tradition 2013 ed., Chapter 16)",
    "pdf_pages": "228-233",
    "printed_pages": "223-228",
    "governance_directives": [
        "No fear-based remedies or diagnosis of curses.",
        "No compulsory purchases, commercial rituals, or claims of guaranteed outcomes.",
        "Free and low-cost practical reflection alternatives must accompany all traditional references.",
        "Medical, psychiatric, and financial issues must be directed to qualified licensed professionals."
    ],
    "remedies": [
        {
            "remedy_id": "REM-MNT-001",
            "category": "Mantra Meditation",
            "tradition": "Vedic / Nadi Traditional",
            "pdf_page": 230,
            "printed_page": 225,
            "condition": "Adopted strictly when the active Mahadasha or Bhukti lord requires harmonic balancing.",
            "source_instruction": "Mantras are to be adopted as a remedial measure only in such cases where the Dasa of a particular planet is in operation.",
            "practical_alternative": "Daily 10-minute mindfulness breathing, vocal concentration, or structured quiet reflection.",
            "cost_level": "free",
            "requires_purchase": False,
            "safety_profile": "Safe, non-invasive, no physical side effects."
        },
        {
            "remedy_id": "REM-FST-002",
            "category": "Intermittent Fasting & Dietary Discipline",
            "tradition": "Nadi Traditional / Ayurvedic Balance",
            "pdf_page": 230,
            "printed_page": 225,
            "condition": "Used for metabolic reset and cultivating willpower.",
            "source_instruction": "Fasting a day in a month is good for health.",
            "practical_alternative": "Hydration discipline, balanced mindful eating, or intermittent fasting under medical advice.",
            "cost_level": "free",
            "requires_purchase": False,
            "safety_profile": "Medical waiver required: Individuals with diabetes, eating disorders, or chronic illness must consult their doctor first."
        },
        {
            "remedy_id": "REM-GEM-003",
            "category": "Gemstone Calibration & Discontinuation Rule",
            "tradition": "Nadi Traditional Gemology",
            "pdf_page": 232,
            "printed_page": 227,
            "condition": "Recommended only for specific temporary objectives with mandatory discontinuation.",
            "source_instruction": "The Stone should be discontinued once he gets the job. He should recommend the discontinuance of the Stone immediately otherwise continuous use will create obstacles for the native to get married because the combination for no marriage is 1,6,10.",
            "numerology_weight_calibration": {
                "birth_dates_1_2_4_7": "4.25 or 7.25 ratti",
                "birth_dates_4_5_8": "4.25, 5.25 or 8.25 ratti",
                "birth_dates_3_6_9": "3.25, 6.25 or 9.25 ratti"
            },
            "practical_alternative": "Color therapy, wearing clothing of corresponding harmonic shades, or setting digital wallpapers with resonant colors.",
            "cost_level": "variable",
            "requires_purchase": True,
            "safety_profile": "Mandatory safety limit: Must be used with defined end date to avoid unintended house disruption."
        },
        {
            "remedy_id": "REM-ATT-004",
            "category": "Integrity Pledge & Positive Conduct",
            "tradition": "Philosophical Nadi Reflection",
            "pdf_page": 229,
            "printed_page": 224,
            "condition": "Universal foundational remedy for any challenging planetary period.",
            "source_instruction": "Pooja cannot undo wrongs committed. While pooja one can pledge in front of almighty that he will keep his positive approach towards life and that is what will help in making his life more easy, more simple and more peaceful.",
            "practical_alternative": "Gratitude journaling, community volunteer service, ethical accountability, and personal reflection.",
            "cost_level": "free",
            "requires_purchase": False,
            "safety_profile": "Universally safe, high psychological resilience value."
        }
    ]
}

with open('data/knowledge_base/nadi_remedy_rules.json', 'w', encoding='utf-8') as f:
    json.dump(remedy_registry, f, indent=2, ensure_ascii=False)

print("Successfully wrote data/knowledge_base/nadi_remedy_rules.json")
