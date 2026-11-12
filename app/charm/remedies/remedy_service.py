"""
app/charm/remedies/remedy_service.py
====================================
Governed Remedies & Practical Alignment Service for Charm AI.
Complies with Section 8 of Master Specification v2.0:
- Grounding: Practical commercial and lifestyle actions FIRST.
- Safe crystals: Vibrational & elemental only, strictly excluding enemy gemstones.
- Consecrated Yantras: Authentic geometric alignment, placement direction, consecration timing.
- Compliance: Drugs and Magic Remedies (Objectionable Advertisements) Act 1954;
  no medical cures, no guaranteed financial windfalls, no fatalistic claims.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

from app.engine.remedy_rules_engine import YANTRA_CATALOGUE

# Classical Planetary Safe Vibrational Crystal Matrix (Section 8)
# Maps Driver/Ruling Planet to harmonious non-conflicting stones
SAFE_CRYSTAL_CATALOGUE: Dict[int, Dict[str, Any]] = {
    1: {
        "planet": "Sun (Surya)",
        "primary_crystals": ["Sunstone", "Carnelian", "Clear Quartz"],
        "incompatible_crystals": ["Blue Sapphire", "Black Tourmaline", "Lapis Lazuli"],
        "lifestyle_attunement": "Enhances personal leadership aura, sovereign decisiveness, and vitality."
    },
    2: {
        "planet": "Moon (Chandra)",
        "primary_crystals": ["Moonstone", "Selenite", "White Howlite"],
        "incompatible_crystals": ["Hessonite Garnet", "Black Obsidian", "Red Coral"],
        "lifestyle_attunement": "Harmonizes emotional fluctuations, supports sleep cycles, and intuitive clarity."
    },
    3: {
        "planet": "Jupiter (Brihaspati)",
        "primary_crystals": ["Citrine", "Yellow Aventurine", "Tiger Eye"],
        "incompatible_crystals": ["Diamond", "Clear Quartz Faceted", "Opal"],
        "lifestyle_attunement": "Expands strategic wisdom, optimistic mentorship, and entrepreneurial abundance."
    },
    4: {
        "planet": "Rahu",
        "primary_crystals": ["Smoky Quartz", "Labradorite", "Hematite"],
        "incompatible_crystals": ["Sunstone", "Ruby", "Pearl"],
        "lifestyle_attunement": "Grounds mental restlessness, clears digital overstimulation, and sharpens analytical depth."
    },
    5: {
        "planet": "Mercury (Budh)",
        "primary_crystals": ["Green Aventurine", "Green Jade", "Malachite"],
        "incompatible_crystals": ["Red Jasper", "Carnelian"],
        "lifestyle_attunement": "Fosters commercial negotiation skills, rapid linguistic fluency, and nervous system ease."
    },
    6: {
        "planet": "Venus (Shukra)",
        "primary_crystals": ["Rose Quartz", "Rhodonite", "Clear Optical Calcite"],
        "incompatible_crystals": ["Yellow Aventurine", "Citrine"],
        "lifestyle_attunement": "Cultivates relational warmth, aesthetic discernment, and luxury balance."
    },
    7: {
        "planet": "Ketu",
        "primary_crystals": ["Tiger Eye", "Turquoise", "Fluorite"],
        "incompatible_crystals": ["Pearl", "Moonstone"],
        "lifestyle_attunement": "Deepens introspection, metaphysical insight, and shields against subtle psychological fatigue."
    },
    8: {
        "planet": "Saturn (Shani)",
        "primary_crystals": ["Amethyst", "Blue Kyanite", "Black Tourmaline"],
        "incompatible_crystals": ["Sunstone", "Carnelian", "Red Coral"],
        "lifestyle_attunement": "Disciplines long-term focus, stabilizes perseverance, and dissolves haste."
    },
    9: {
        "planet": "Mars (Mangal)",
        "primary_crystals": ["Red Jasper", "Bloodstone", "Carnelian"],
        "incompatible_crystals": ["Emerald", "Green Aventurine"],
        "lifestyle_attunement": "Channels vital courage, physical stamina, and purposeful goal execution without anger."
    }
}

NUM_TO_YANTRA_KEY: Dict[int, str] = {
    1: "Surya Yantra",
    2: "Chandra Yantra",
    3: "Brihaspati Yantra",
    4: "Rahu Yantra",
    5: "Budh Yantra",
    6: "Shukra Yantra",
    7: "Ketu Yantra",
    8: "Shani Yantra",
    9: "Mangal Yantra"
}

class RemedyItem(BaseModel):
    remedy_id: str
    category: str = Field(..., description="PRACTICAL_ACTION, VIBRATIONAL_CRYSTAL, SACRED_YANTRA, LIFESTYLE_HORA")
    title: str
    description: str
    rationale: str
    cost_level: str = "FREE_OR_LOW_COST"
    is_optional: bool = True
    citation: Optional[str] = None
    safety_notes: List[str] = Field(default_factory=list)

class RemedyService:
    def get_governed_remedies(
        self,
        event_family: str,
        driver: int,
        conductor: int,
        event_assessment: str
    ) -> List[RemedyItem]:
        """
        Retrieves strictly approved, non-fatalistic, legally compliant remedies.
        Always presents practical commercial/lifestyle actions first.
        """
        remedies: List[RemedyItem] = []
        safe_driver = driver if 1 <= driver <= 9 else 1

        # 1. Mandatory Practical Action First (Section 8 Directive)
        practical_actions = {
            "career": RemedyItem(
                remedy_id="REM-PRACTICAL-CAREER-01",
                category="PRACTICAL_ACTION",
                title="Conduct a Milestone Portfolio & Skills Audit",
                description="Update your executive resume and portfolio to highlight quantifiable leadership outcomes. Schedule structured informational conversations with 2 trusted industry mentors.",
                rationale="Grounded action aligns with cosmic momentum; institutional appointments reward tangible demonstrated value.",
                cost_level="FREE",
                is_optional=False,
                citation="SRC-NV-003: Professional Practitioner Curriculum",
                safety_notes=["Practical career initiative; not a magical guarantee of hiring."]
            ),
            "wealth": RemedyItem(
                remedy_id="REM-PRACTICAL-WEALTH-01",
                category="PRACTICAL_ACTION",
                title="Establish a 90-Day Cash Flow Liquidity Reserve",
                description="Audit discretionary recurring expenses and maintain liquid operating reserves before committing to capital-intensive acquisitions.",
                rationale="Prudent financial governance anchors expansive Jupiter-Mercury vibrations into sustainable wealth.",
                cost_level="FREE",
                is_optional=False,
                citation="SRC-NV-005: 81-Matrix Planetary Dynamics",
                safety_notes=["Financial self-discipline; does not constitute speculative investment advice."]
            ),
            "marriage": RemedyItem(
                remedy_id="REM-PRACTICAL-REL-01",
                category="PRACTICAL_ACTION",
                title="Practice Empathetic Active Listening",
                description="Dedicate an uninterrupted 30-minute dialogue window weekly with your partner without digital screens to align shared values and long-term goals.",
                rationale="Venus-Moon relational harmony blossoms when emotional communication is held in clear, respectful space.",
                cost_level="FREE",
                is_optional=False,
                citation="SRC-NV-001: Institutional Brand Architecture",
                safety_notes=["Interpersonal relationship best practice."]
            ),
            "health": RemedyItem(
                remedy_id="REM-PRACTICAL-HLTH-01",
                category="PRACTICAL_ACTION",
                title="Circadian Solar Synchronization & Daily Walks",
                description="Walk barefoot on natural ground or absorb 15 minutes of gentle morning sunlight within one hour of dawn. Drink adequate water throughout the day.",
                rationale="Solar illumination balances the autonomic nervous system and grounds scattered planetary frequencies.",
                cost_level="FREE",
                is_optional=False,
                citation="SRC-NV-005: Planetary Dynamics",
                safety_notes=["Statutory Notice: For physical medical symptoms, always consult a licensed medical physician."]
            )
        }
        remedies.append(practical_actions.get(event_family, practical_actions["career"]))

        # 2. Vibrational Crystal Attunement (Safely filtered against planetary enemies)
        crystal_data = SAFE_CRYSTAL_CATALOGUE.get(safe_driver, SAFE_CRYSTAL_CATALOGUE[1])
        primary_crystals = crystal_data.get("primary_crystals", ["Clear Quartz"])
        remedies.append(RemedyItem(
            remedy_id=f"REM-CRYSTAL-{safe_driver}-01",
            category="VIBRATIONAL_CRYSTAL",
            title=f"Vibrational Crystal Attunement: {primary_crystals[0]} ({crystal_data.get('planet')})",
            description=f"Keep a natural tumbled {primary_crystals[0]} near your workspace or carry during key negotiations. Avoid clashing stones: {', '.join(crystal_data.get('incompatible_crystals', []))}.",
            rationale=crystal_data.get("lifestyle_attunement", "Harmonizes vibrational frequency."),
            cost_level="LOW_COST",
            is_optional=True,
            citation="SRC-NV-005: Planetary Crystal Resonance",
            safety_notes=[
                "Spiritual/vibrational tool only.",
                "Drugs and Magic Remedies Act 1954 Compliance: Not intended to cure, diagnose, or treat any disease."
            ]
        ))

        # 3. Sacred Yantra Spatial Attunement
        yantra_key = NUM_TO_YANTRA_KEY.get(safe_driver, "Surya Yantra")
        yantra_data = YANTRA_CATALOGUE.get(yantra_key, YANTRA_CATALOGUE.get("Surya Yantra", {}))
        remedies.append(RemedyItem(
            remedy_id=f"REM-YANTRA-{safe_driver}-01",
            category="SACRED_YANTRA",
            title=f"Consecrated {yantra_data.get('name', 'Sacred Geometric Yantra')}",
            description=f"Position on {yantra_data.get('material', 'pure metal plate')} in the {yantra_data.get('optimal_direction', 'East')} quadrant of your home or private office. Consecrate on {yantra_data.get('best_day_time', 'auspicious morning hours')}.",
            rationale=yantra_data.get('purpose', 'Traditional geometric matrix for focus and mental peace.'),
            cost_level="LOW_COST",
            is_optional=True,
            citation="SRC-NV-003: Sacred Yantra Geometry Treatise",
            safety_notes=["Traditional symbolic focal point for mindful contemplation."]
        ))

        return remedies

remedy_service = RemedyService()
