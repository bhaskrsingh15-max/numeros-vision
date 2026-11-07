"""
NV-005: PROFESSION RECOMMENDATION ENGINE
Grounding: Classical Numerology Archetypes, Vedic Numerology, Bhrigu Nandi Nadi (BNN) Saturn Karmakaraka, KP 10th Cusp.

Deterministic capabilities:
1. Unified Career Taxonomy mapped across:
   - Driver (Mulank): Personal working style, innate skills, frontline role.
   - Conductor (Bhagyank): Long-term career destiny, organizational scale, ultimate peak.
   - BNN Saturn Conjunction: Karmakaraka profession imprint (Saturn + Driver/Conductor).
   - Core Matrix & Lo Shu: Practical plane (8-1-6) and Thought plane (4-3-8) presence.
2. Traceable Synthesis & Conflict Disclosure:
   - Synthesizes divergent energies (e.g., Driver 1 vs Conductor 8).
   - Transparently discloses conflicts without confusing the seeker.
3. Business vs Employment Suitability:
   - Independent Entrepreneurship vs Structured Corporate vs Professional Practice.
4. Concrete Output Schema:
   - Primary Careers, Secondary/Pivot Careers, Optimal Work Environments,
     Business/Employment Suitability Scores, Sectors of Resistance, and Stock Market/Finance alignment.
5. Strict Non-Aptitude Qualification (Legal & Ethical compliance).
"""

from typing import Dict, Any, List, Optional
import sys
import os

workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from app.engine.number_characteristics_registry import (
    get_number_profile,
    get_relationship,
    PLANETARY_RULERS
)
from app.engine.bnn_numerology_engine import get_bnn_numerology_pair
from app.engine.professional_numerology_engine import analyze_share_market_profile


# Detailed Career Affinities by Root Number (1 to 9)
CAREER_TAXONOMY: Dict[int, Dict[str, Any]] = {
    1: {
        "archetype": "Pioneering Leader & Executive",
        "primary_fields": [
            "Corporate Leadership & C-Suite Management",
            "Public Administration & Civil Services (IAS/IPS)",
            "Entrepreneurship & Startup Founding",
            "Surgical Medicine & Cardiology",
            "Gold, Jewelry & High-Value Asset Trade",
            "Defense & Military Strategy"
        ],
        "secondary_fields": ["Government Liaison", "Political Strategy", "Patent Law", "Renewable Energy"],
        "work_style": "High autonomy, executive command, decisive vision; struggles in subservient or micromanaged roles.",
        "business_affinity": 85,
        "corporate_employment_affinity": 70,
        "partnership_affinity": 45,
        "unfavorable_sectors": ["Routine clerking", "Passive retail support", "Subservient intermediate agencies"]
    },
    2: {
        "archetype": "Diplomat, Nurturer & Creative Strategist",
        "primary_fields": [
            "Psychology, Counselling & Mental Wellness",
            "FMCG, Dairy, Food Processing & Beverage Industry",
            "Human Resources & Talent Development",
            "Diplomacy, International Relations & Negotiation",
            "Water Resources, Marine Logistics & Maritime Trade",
            "Creative Arts, Scriptwriting & Visual Design"
        ],
        "secondary_fields": ["Hospitality Management", "Pediatric Medicine", "Interior Architecture", "Public Relations"],
        "work_style": "Collaborative, empathetic, harmonious; flourishes in supportive partnership and peaceful environments.",
        "business_affinity": 55,
        "corporate_employment_affinity": 85,
        "partnership_affinity": 90,
        "unfavorable_sectors": ["High-conflict combat litigation", "Aggressive debt collection", "High-stress speculative trading"]
    },
    3: {
        "archetype": "Wisdom Guide, Scholar & Macro Strategist",
        "primary_fields": [
            "Higher Education, University Professorship & Research",
            "Banking, High Finance, Asset Management & Chartered Accountancy",
            "Judiciary, Legal Advisory & Constitutional Law",
            "Publishing, Journalism & Mass Communication",
            "Spiritual Guidance, Philosophy & Institutional Advisory",
            "Corporate Training, Coaching & EdTech Leadership"
        ],
        "secondary_fields": ["Cross-border Trade Consulting", "Religious Trusts", "Philanthropy", "Curriculum Design"],
        "work_style": "Expansive, ethical, knowledge-driven; excels where wisdom, teaching, and structured authority are valued.",
        "business_affinity": 75,
        "corporate_employment_affinity": 80,
        "partnership_affinity": 70,
        "unfavorable_sectors": ["Shady speculative ventures", "Gambling operations", "Monotonous manual labor"]
    },
    4: {
        "archetype": "System Architect, Technologist & Disruptor",
        "primary_fields": [
            "Software Engineering, AI & Deep Tech Architecture",
            "Civil Engineering, Construction & Macro-Infrastructure",
            "Aviation, Aerospace & Space Technology",
            "Cybersecurity, Cryptography & Systems Auditing",
            "Data Analytics, Logistics & Supply Chain Optimization",
            "Unconventional Media, Digital Marketing & Disruption"
        ],
        "secondary_fields": ["Automotive Engineering", "Forensic Accounting", "Telecommunications", "Renewable Power Grids"],
        "work_style": "Analytical, methodical, unconventional; excels at organizing complex data and finding non-linear solutions.",
        "business_affinity": 75,
        "corporate_employment_affinity": 80,
        "partnership_affinity": 55,
        "unfavorable_sectors": ["Rigid traditional bureaucracies", "Vague emotional counseling", "Unstructured artistic hobbies"]
    },
    5: {
        "archetype": "Master Communicator, Trader & Commercial Polymath",
        "primary_fields": [
            "Commercial Trading, Export-Import & Global Arbitrage",
            "FinTech, Stock Brokerage & Financial Engineering",
            "Marketing, Brand Strategy, Advertising & Media",
            "Travel, Tourism, Aviation & International Business",
            "Public Relations, Event Management & Entertainment",
            "Technology Sales, Business Development & Venture Brokering"
        ],
        "secondary_fields": ["Journalism", "Telecommunications", "Language Translation", "Real Estate Brokering"],
        "work_style": "Agile, versatile, quick-witted, travel-friendly; suffocates in rigid, static, repetitive desk routines.",
        "business_affinity": 95,
        "corporate_employment_affinity": 75,
        "partnership_affinity": 80,
        "unfavorable_sectors": ["Static isolated laboratory research", "Monotonous data entry", "Slow-moving archival administration"]
    },
    6: {
        "archetype": "Aesthetician, Luxurian & Harmonizer",
        "primary_fields": [
            "Luxury Goods, Fashion Design & Haute Couture",
            "Hospitality, Fine Dining, Hotels & Premium Tourism",
            "Entertainment, Cinema, Performing Arts & Media Production",
            "Cosmetics, Dermatology, Aesthetics & Wellness Spas",
            "Interior Architecture, High-End Real Estate & Staging",
            "Jewelry, Diamond Merchanting & Fine Crafts"
        ],
        "secondary_fields": ["Automotive Styling", "Event Production", "Family Counselling", "Culinary Arts"],
        "work_style": "Refined, sensory, charming, values-driven; flourishes where beauty, comfort, and gracious hospitality are paramount.",
        "business_affinity": 85,
        "corporate_employment_affinity": 70,
        "partnership_affinity": 85,
        "unfavorable_sectors": ["Grimy heavy industrial waste handling", "High-stress conflict litigation", "Severe austere isolation"]
    },
    7: {
        "archetype": "Deep Researcher, Analyst & Metaphysician",
        "primary_fields": [
            "Scientific Research, Biotechnology & Pharmaceutical Labs",
            "Intelligence Services, Data Investigation & Cryptanalysis",
            "Astrology, Metaphysics, Occult Sciences & Spiritual Healing",
            "Philosophy, Theology, Advanced Mathematics & Theoretical Physics",
            "Quality Assurance, Forensic Pathology & Diagnostic Radiology",
            "Niche Technical Consulting & High-Level Advisory"
        ],
        "secondary_fields": ["Archival Curation", "Archaeology", "Specialized Programming", "Psychiatry"],
        "work_style": "Introspective, solitary, intensely deep, analytical; demands intellectual freedom away from shallow politics.",
        "business_affinity": 60,
        "corporate_employment_affinity": 75,
        "partnership_affinity": 40,
        "unfavorable_sectors": ["High-pressure door-to-door retail", "Shallow public entertainment", "Noisy aggressive sales pits"]
    },
    8: {
        "archetype": "Executive Authority, Industrialist & Karmic Judge",
        "primary_fields": [
            "Heavy Industry, Manufacturing, Steel & Mining Operations",
            "Real Estate Development, Land Acquisition & Infrastructure",
            "Judiciary, Corporate Law, Compliance & Labor Arbitration",
            "Government Administration, Municipal Governance & Public Works",
            "Institutional Finance, Banking Auditing & Distressed Asset Recovery",
            "Oil, Natural Gas, Energy Exploration & Heavy Machinery"
        ],
        "secondary_fields": ["Logistics Hubs", "Security Contracting", "Orthopedic Surgery", "Agriculture Management"],
        "work_style": "Authoritative, resilient, long-term oriented, demanding; builds enduring institutions through persistent labor.",
        "business_affinity": 90,
        "corporate_employment_affinity": 85,
        "partnership_affinity": 60,
        "unfavorable_sectors": ["Frivolous pop trends", "Unregulated rapid speculation", "Superficial short-term glamour"]
    },
    9: {
        "archetype": "Dynamic Warrior, Surgeon & Humanitarian Crusader",
        "primary_fields": [
            "Military Operations, Police Command & Homeland Defense",
            "Emergency Medicine, General Surgery & Paramedic Sciences",
            "Sports Management, Athletics, Martial Arts & Fitness Industry",
            "Heavy Engineering, Metallurgy, Fire Safety & Defense Equipment",
            "Humanitarian NGOs, Global Disaster Relief & Social Activism",
            "Construction Project Management & Real Estate Execution"
        ],
        "secondary_fields": ["Pharmaceutical Chemistry", "Culinary Fire Operations", "Mining Technology", "Crisis Management"],
        "work_style": "Energetic, courageous, mission-driven, urgent; needs tangible challenges and righteous purpose.",
        "business_affinity": 75,
        "corporate_employment_affinity": 80,
        "partnership_affinity": 50,
        "unfavorable_sectors": ["Sedentary paperwork", "Submissive retail clerks", "Ambiguous passive bureaucracies"]
    }
}


def recommend_professions(
    driver: int,
    conductor: int,
    saturn_conjunction_override: Optional[int] = None,
    kp_tenth_sub_lord: Optional[str] = None
) -> Dict[str, Any]:
    """
    NV-005 Requirement: Unified Profession Recommendation Engine.
    Synthesizes Driver, Conductor, BNN Saturn Karmakaraka, and optional KP 10th sub-lord.
    Discloses synergies or contrasts transparently.
    """
    d_prof = CAREER_TAXONOMY.get(driver, CAREER_TAXONOMY[1])
    c_prof = CAREER_TAXONOMY.get(conductor, CAREER_TAXONOMY[1])

    # Check harmony between Driver and Conductor
    rel = get_relationship(driver, conductor)
    is_harmonic = rel["status"] == "FRIENDLY"
    is_neutral = rel["status"] == "NEUTRAL"
    is_conflict = rel["status"] == "ENEMY"

    # Primary Careers: Intersection + top Driver/Conductor picks
    driver_primary = set(d_prof["primary_fields"])
    conductor_primary = set(c_prof["primary_fields"])
    common_fields = list(driver_primary.intersection(conductor_primary))

    combined_primary = []
    # Add common first
    combined_primary.extend(common_fields)
    # Then interleave driver (personal style) and conductor (long-term trajectory)
    for p in d_prof["primary_fields"]:
        if p not in combined_primary:
            combined_primary.append(p)
    for p in c_prof["primary_fields"]:
        if p not in combined_primary:
            combined_primary.append(p)

    primary_recommendations = combined_primary[:6]
    secondary_recommendations = list(dict.fromkeys(d_prof["secondary_fields"] + c_prof["secondary_fields"]))[:5]

    # BNN Saturn Karma Analysis
    saturn_ref = saturn_conjunction_override if saturn_conjunction_override else conductor
    bnn_pair = get_bnn_numerology_pair(8, saturn_ref)
    bnn_professions = bnn_pair.get("professions", [])

    # Suitability Scores
    biz_score = round((d_prof["business_affinity"] * 0.4) + (c_prof["business_affinity"] * 0.6))
    corp_score = round((d_prof["corporate_employment_affinity"] * 0.4) + (c_prof["corporate_employment_affinity"] * 0.6))
    part_score = round((d_prof["partnership_affinity"] * 0.5) + (c_prof["partnership_affinity"] * 0.5))

    # Synthesis & Conflict Disclosure
    if is_conflict:
        synthesis_mode = "Bifurcated Career Archetype / Dual Engine"
        conflict_explanation = (
            f"Driver {driver} ({PLANETARY_RULERS.get(driver, {}).get('planet')}) and Conductor {conductor} "
            f"({PLANETARY_RULERS.get(conductor, {}).get('planet')}) hold opposing energetic frequencies ({rel['relationship']}). "
            f"This does not prevent success; rather, it creates a powerful two-tier professional path: your personal working style "
            f"({d_prof['work_style']}) operates most effectively when channeled into the institutional domain of your Conductor ({c_prof['archetype']})."
        )
    elif is_harmonic:
        synthesis_mode = "Harmonious Unified Engine"
        conflict_explanation = (
            f"Driver {driver} and Conductor {conductor} share natural planetary harmony ({rel['relationship']}). "
            f"Your personal working instincts naturally propel you toward your life path destination, creating rapid compounding in your chosen vocation."
        )
    else:
        synthesis_mode = "Complementary Dual Engine"
        conflict_explanation = (
            f"Driver {driver} and Conductor {conductor} maintain a neutral relationship. "
            f"Your personal working style and destiny trajectory complement each other without friction, giving you versatility across multiple professional domains."
        )

    # Share Market Profile Integration
    share_market_data = analyze_share_market_profile(driver, conductor)

    # Unfavorable sectors
    unfavorable = list(dict.fromkeys(d_prof["unfavorable_sectors"] + c_prof["unfavorable_sectors"]))

    # KP Sub-lord contextual note if provided
    kp_note = None
    if kp_tenth_sub_lord:
        kp_note = (
            f"KP 10th Cuspal Sub-Lord is attuned to '{kp_tenth_sub_lord}'. "
            f"Align primary career execution with the signification and sign placement of {kp_tenth_sub_lord}."
        )

    return {
        "driver": driver,
        "conductor": conductor,
        "driver_archetype": d_prof["archetype"],
        "conductor_archetype": c_prof["archetype"],
        "relationship_dynamic": rel["relationship"],
        "synthesis_mode": synthesis_mode,
        "synthesis_disclosure": conflict_explanation,
        "primary_recommended_professions": primary_recommendations,
        "secondary_pivot_professions": secondary_recommendations,
        "bnn_saturn_karma_professions": bnn_professions,
        "optimal_work_style": f"Personal: {d_prof['work_style']} | Destiny Scale: {c_prof['work_style']}",
        "suitability_matrix": {
            "independent_business_and_founding": {
                "score_pct": biz_score,
                "status": "Highly Recommended" if biz_score >= 80 else ("Viable" if biz_score >= 60 else "Caution Recommended")
            },
            "structured_corporate_employment": {
                "score_pct": corp_score,
                "status": "Highly Recommended" if corp_score >= 80 else ("Viable" if corp_score >= 60 else "Caution Recommended")
            },
            "commercial_partnerships": {
                "score_pct": part_score,
                "status": "Highly Recommended" if part_score >= 80 else ("Viable" if part_score >= 60 else "Caution Recommended")
            }
        },
        "unfavorable_sectors_to_avoid": unfavorable,
        "share_market_and_investment": share_market_data,
        "kp_tenth_sub_lord_note": kp_note,
        "statutory_qualification": (
            "Professional recommendations represent archetypal and astrological energetic affinities. "
            "They do not constitute vocational aptitude testing, educational admission guarantees, or financial advice."
        )
    }
