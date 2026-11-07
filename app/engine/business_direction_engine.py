"""
Numeros Vision — Business Direction Intelligence & Existing Business Alignment Engine
Implements Sections 1.A and 1.B of the Master Build Specification:
- Startup package: founder profiling, commercial viability vs traditional alignment separation
- Operating business diagnostic: fixed vs changeable factors, practical business improvements first
- Letter-by-letter Chaldean acoustic analysis & word subtotal breakdown
- Compound number Cheiro reading & founder synergy harmony score
- Auspicious spelling balancing recommendations targeting roots 1, 3, 5, 6
- Comprehensive Vastu, stationery layout, and operational remedies
- Strict evidence labeling and non-guarantee disclosures
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Literal
import math

from app.engine.business_taxonomy import BusinessTaxonomyEngine
from app.engine.archetype_engine import ContextualArchetypeEngine
from app.engine.core_matrix_engine import (
    CHALDEAN_VALUES,
    calculate_chaldean_name,
    generate_core_matrix_profile,
    reduce_to_single_digit
)
from app.engine.number_characteristics_registry import get_number_profile
from app.engine.vedic_numerology import FRIENDLY_NUMBERS, ENEMY_NUMBERS

PLANET_NAMES = {
    1: "Sun (Surya)",
    2: "Moon (Chandra)",
    3: "Jupiter (Guru)",
    4: "Rahu (North Node)",
    5: "Mercury (Budh)",
    6: "Venus (Shukra)",
    7: "Ketu (South Node)",
    8: "Saturn (Shani)",
    9: "Mars (Mangal)"
}

CapitalBand = Literal["bootstrapped", "seed_10k_50k", "growth_50k_250k", "institutional_250k_plus"]
RiskTolerance = Literal["low", "moderate", "aggressive"]
OperatingPreference = Literal["hands_on_operations", "digital_remote", "hybrid_management"]


@dataclass
class FounderProfile:
    name: str
    skills: List[str]
    experience_years: int
    capital_band: CapitalBand
    location: str
    risk_tolerance: RiskTolerance
    operating_preference: OperatingPreference
    dob: Optional[str] = None  # YYYY-MM-DD
    birth_time_exact: bool = False
    co_founder_names: List[str] = field(default_factory=list)


@dataclass
class CandidateBusinessOption:
    idea_id: str
    name: str
    activity_description: str
    revenue_model: str  # e.g. "subscription", "ecommerce", "b2b_retainer", "brick_and_mortar"
    customer_segment: str
    delivery_channel: str
    regulatory_tier: str = "standard"  # "standard", "regulated", "heavily_regulated"
    estimated_startup_capital_required: CapitalBand = "seed_10k_50k"


@dataclass
class CommercialViabilityCheck:
    skill_match: bool
    capital_sufficient: bool
    operational_complexity: str  # "low", "moderate", "high"
    regulatory_feasibility: str
    findings: List[str]


@dataclass
class TraditionalAlignmentCheck:
    framework: str
    alignment_status: str  # "aligned", "partially_aligned", "mixed", "conflicted", "insufficient_evidence"
    candidate_archetypes: List[str]
    name_compound: int
    name_single: int
    reasons: List[str]
    conflicts: List[str]
    unknowns: List[str]
    letter_breakdown: List[Dict[str, Any]] = field(default_factory=list)
    compound_profile: Dict[str, Any] = field(default_factory=dict)
    founder_synergy: Dict[str, Any] = field(default_factory=dict)
    balanced_spelling_recommendations: List[Dict[str, Any]] = field(default_factory=list)
    vastu_and_operational_remedies: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StartupEvaluationResult:
    idea_id: str
    business_name: str
    commercial_viability: CommercialViabilityCheck
    traditional_alignment: TraditionalAlignmentCheck
    synthesis_recommendation: str
    next_steps: List[str]
    mandatory_disclaimer: str = (
        "Evidence Notice: Traditional numerology and astrology are symbolic interpretive systems. "
        "They do not scientifically prove, cause, or guarantee commercial success, market profitability, or business longevity."
    )


class BusinessDirectionEngine:
    """
    Evaluates new business direction (Startup Package) and audits existing businesses (Diagnostic).
    Strictly keeps practical business viability separate from traditional numerology/astrology.
    """

    def __init__(self):
        self.taxonomy = BusinessTaxonomyEngine()
        self.archetypes = ContextualArchetypeEngine()

    def build_acoustic_breakdown(self, name: str) -> Dict[str, Any]:
        """
        Breaks down every word and character into its exact Chaldean sound vibration.
        Computes word subtotals, full compound sum, and root planet.
        """
        words_data = []
        total_compound = 0

        for raw_word in name.split():
            clean_word = ''.join(c.upper() for c in raw_word if c.isalpha())
            if not clean_word:
                continue
            
            letter_list = []
            word_sum = 0
            for char in clean_word:
                val = CHALDEAN_VALUES.get(char, 0)
                word_sum += val
                letter_list.append({
                    "char": char,
                    "val": val,
                    "planet": PLANET_NAMES.get(val, "Neutral")
                })
            
            word_root = reduce_to_single_digit(word_sum)
            words_data.append({
                "word": raw_word,
                "clean_word": clean_word,
                "letters": letter_list,
                "compound": word_sum,
                "root": word_root,
                "root_planet": PLANET_NAMES.get(word_root, "Universal")
            })
            total_compound += word_sum

        if not words_data:
            return {
                "words": [],
                "total_compound": 0,
                "total_root": 0,
                "root_planet": "Unknown",
                "is_karmic": False,
                "is_master": False
            }

        total_root = reduce_to_single_digit(total_compound)
        return {
            "words": words_data,
            "total_compound": total_compound,
            "total_root": total_root,
            "root_planet": PLANET_NAMES.get(total_root, "Universal"),
            "is_karmic": total_compound in [13, 14, 16, 19, 28],
            "is_master": total_compound in [11, 22, 33] or total_root in [11, 22, 33]
        }

    def get_compound_profile_reading(self, compound: int, root: int) -> Dict[str, Any]:
        """
        Retrieves authentic Cheiro & Vedic compound reading from registry.
        """
        prof = get_number_profile(compound)
        if prof:
            return {
                "compound_number": compound,
                "root_number": root,
                "archetype_title": prof.get("archetype_title", f"Compound Vibration {compound}"),
                "core_characteristics": prof.get("core_characteristics", "Dynamic commercial momentum."),
                "planet": prof.get("planet", PLANET_NAMES.get(root, "Universal")),
                "strengths": prof.get("strengths", ["Executive drive", "Market resonance"]),
                "challenges": prof.get("challenges", ["Patience required during initial growth"]),
                "favourable_colours": prof.get("favourable_colours", ["Gold", "Pearl White"]),
                "favourable_days": prof.get("favourable_days", ["Wednesday", "Thursday"]),
                "methodology": "Classical Chaldean Acoustic Framework (METH-CHALDEAN-001)"
            }

        # For numbers > 52, channel through single root and compound reduction
        root_prof = get_number_profile(root)
        tens_digit = compound // 10
        units_digit = compound % 10
        p_tens = PLANET_NAMES.get(tens_digit, "Universal")
        p_units = PLANET_NAMES.get(units_digit, "Universal")

        title = f"High Compound Vibration {compound} (Root {root})"
        char_desc = f"Channels dual energies of {p_tens} ({tens_digit}) and {p_units} ({units_digit}) through reduced root {root} ({PLANET_NAMES.get(root, 'Universal')})."
        
        return {
            "compound_number": compound,
            "root_number": root,
            "archetype_title": title,
            "core_characteristics": char_desc,
            "planet": PLANET_NAMES.get(root, "Universal"),
            "strengths": root_prof.get("strengths", ["Endurance", "Systematic execution"]) if root_prof else ["Focus", "Resilience"],
            "challenges": root_prof.get("challenges", ["Rigidity", "Slow gestation"]) if root_prof else ["Initial friction"],
            "favourable_colours": root_prof.get("favourable_colours", ["Jupiter Gold", "Venus Pearl"]) if root_prof else ["#C9A227", "#FFFDF7"],
            "favourable_days": root_prof.get("favourable_days", ["Wednesday", "Friday"]) if root_prof else ["Wednesday"],
            "methodology": "Vedic Dual-Subtone Synthesis & Classical Chaldean Reduction"
        }

    def evaluate_founder_synergy(
        self,
        founder_dob: Optional[str],
        founder_name: str,
        business_root: int
    ) -> Dict[str, Any]:
        """
        Evaluates Founder Driver (Mulank) and Conductor (Bhagyank) harmony against the business name root.
        """
        if not founder_dob:
            return {
                "has_dob": False,
                "synergy_score": 50,
                "status": "INSUFFICIENT_EVIDENCE",
                "badge_label": "DOB Required For Synergy Audit",
                "driver": None,
                "conductor": None,
                "driver_planet": None,
                "conductor_planet": None,
                "business_root": business_root,
                "relationship_driver": "UNKNOWN",
                "relationship_conductor": "UNKNOWN",
                "analysis_summary": "Founder date of birth was not provided. Synergy calculation remains insufficient evidence."
            }

        try:
            parts = founder_dob.split("-")
            if len(parts) != 3:
                raise ValueError("Invalid date format")
            
            y, m, d = int(parts[0]), int(parts[1]), int(parts[2])
            driver = reduce_to_single_digit(d)
            all_digits_sum = sum(int(c) for c in f"{d}{m}{y}")
            conductor = reduce_to_single_digit(all_digits_sum)

            driver_planet = PLANET_NAMES.get(driver, "Sun")
            conductor_planet = PLANET_NAMES.get(conductor, "Jupiter")

            d_friends = FRIENDLY_NUMBERS.get(driver, [])
            d_enemies = ENEMY_NUMBERS.get(driver, [])
            c_friends = FRIENDLY_NUMBERS.get(conductor, [])
            c_enemies = ENEMY_NUMBERS.get(conductor, [])

            # Evaluate Driver harmony
            if business_root == driver:
                rel_d = "SAME_VIBRATION"
            elif business_root in d_friends:
                rel_d = "FRIENDLY"
            elif business_root in d_enemies:
                rel_d = "ENEMY_FRICTION"
            else:
                rel_d = "NEUTRAL"

            # Evaluate Conductor harmony
            if business_root == conductor:
                rel_c = "SAME_VIBRATION"
            elif business_root in c_friends:
                rel_c = "FRIENDLY"
            elif business_root in c_enemies:
                rel_c = "ENEMY_FRICTION"
            else:
                rel_c = "NEUTRAL"

            # Calculate deterministic synergy score (0 - 100%)
            score = 50
            if rel_d in ["SAME_VIBRATION", "FRIENDLY"]:
                score += 22
            elif rel_d == "ENEMY_FRICTION":
                score -= 25

            if rel_c in ["SAME_VIBRATION", "FRIENDLY"]:
                score += 20
            elif rel_c == "ENEMY_FRICTION":
                score -= 22

            if business_root in [1, 3, 5, 6]:
                score += 8  # Auspicious business vibration bonus

            # Clamp between 22 and 98
            score = max(22, min(98, score))

            if score >= 80:
                status_label = "Super Harmonious (Auspicious Synergy)"
                badge_type = "high_harmony"
            elif score >= 65:
                status_label = "Supportive Commercial Alignment"
                badge_type = "supportive"
            elif score >= 50:
                status_label = "Neutral Vibration (Conscious Effort Required)"
                badge_type = "neutral"
            else:
                status_label = "Karmic Friction Detected (Name Balancing Recommended)"
                badge_type = "friction"

            summary = (
                f"Founder Driver {driver} ({driver_planet}) and Conductor {conductor} ({conductor_planet}) "
                f"interact with Business Name Root {business_root} ({PLANET_NAMES.get(business_root, 'Universal')}). "
                f"Driver resonance is {rel_d.replace('_', ' ')} and Conductor resonance is {rel_c.replace('_', ' ')}."
            )

            return {
                "has_dob": True,
                "synergy_score": score,
                "status": status_label,
                "badge_label": status_label,
                "badge_type": badge_type,
                "driver": driver,
                "conductor": conductor,
                "driver_planet": driver_planet,
                "conductor_planet": conductor_planet,
                "business_root": business_root,
                "business_root_planet": PLANET_NAMES.get(business_root, "Universal"),
                "relationship_driver": rel_d,
                "relationship_conductor": rel_c,
                "analysis_summary": summary
            }

        except Exception as e:
            return {
                "has_dob": False,
                "synergy_score": 50,
                "status": "ERROR_PARSING_DOB",
                "badge_label": "DOB Parsing Error",
                "driver": None,
                "conductor": None,
                "analysis_summary": f"Could not parse founder birth date: {str(e)}"
            }

    def generate_balanced_spelling_recommendations(
        self,
        base_name: str,
        current_compound: int,
        current_root: int,
        target_roots: Optional[List[int]] = None
    ) -> List[Dict[str, Any]]:
        """
        Deterministically evaluates spelling variations targeting auspicious commercial roots (1, 3, 5, 6).
        Provides 3 to 5 tailored candidate names with resulting compound, root planet, and commercial rationale.
        """
        if target_roots is None:
            target_roots = [1, 3, 5, 6]

        words = base_name.strip().split()
        if not words:
            return []

        candidates = []
        tested_names = set()

        # Strategic brand descriptors
        brand_descriptors = ["Hub", "Global", "AI", "Digital", "Tech", "Labs", "Group", "Ventures", "Cloud", "Studio", "Pay"]

        # Strategy 1: Add strategic brand descriptor
        for desc in brand_descriptors:
            if desc.lower() in [w.lower() for w in words]:
                continue
            cand_name = f"{base_name} {desc}".strip()
            if cand_name.lower() in tested_names:
                continue
            tested_names.add(cand_name.lower())

            calc = calculate_chaldean_name(cand_name)
            c_comp = calc["compound_sum"]
            c_root = calc["single_root"]

            if c_root in target_roots and c_root != current_root:
                prof = get_number_profile(c_comp)
                title = prof.get("archetype_title", f"Root {c_root} ({PLANET_NAMES.get(c_root, '')})") if prof else f"Compound {c_comp} / Root {c_root}"
                
                # Assign domain benefit based on root
                if c_root == 1:
                    benefit = "Activates Sun authority, executive sovereignty, and bold market leadership."
                elif c_root == 3:
                    benefit = "Channels Jupiter wisdom, multi-market expansion, and scalable knowledge capital."
                elif c_root == 5:
                    benefit = "Unlocks Mercury high-velocity commerce, agile digital networking, and rapid sales conversion."
                else:  # 6
                    benefit = "Invokes Venus luxury appeal, customer loyalty retention, and opulent brand aesthetics."

                candidates.append({
                    "suggested_name": cand_name,
                    "compound": c_comp,
                    "root": c_root,
                    "root_planet": PLANET_NAMES.get(c_root, "Universal"),
                    "archetype_title": title,
                    "commercial_benefit": benefit,
                    "variation_type": "Brand Descriptor Harmonization"
                })
                if len(candidates) >= 4:
                    break

        # Strategy 2: Phonetic subtle letter calibrations if still under 4
        if len(candidates) < 4 and len(words) >= 1:
            first_w = words[0]
            rest_w = " ".join(words[1:]) if len(words) > 1 else ""

            for sfx in ["s", "z", "h", "e"]:
                cand_first = f"{first_w}{sfx}"
                cand_name = f"{cand_first} {rest_w}".strip()
                if cand_name.lower() in tested_names:
                    continue
                tested_names.add(cand_name.lower())

                calc = calculate_chaldean_name(cand_name)
                c_comp = calc["compound_sum"]
                c_root = calc["single_root"]

                if c_root in target_roots:
                    prof = get_number_profile(c_comp)
                    title = prof.get("archetype_title", f"Root {c_root}") if prof else f"Compound {c_comp}"
                    candidates.append({
                        "suggested_name": cand_name,
                        "compound": c_comp,
                        "root": c_root,
                        "root_planet": PLANET_NAMES.get(c_root, "Universal"),
                        "archetype_title": title,
                        "commercial_benefit": f"Harmonizes phonetic resonance directly into auspicious root {c_root} ({PLANET_NAMES.get(c_root, '')}).",
                        "variation_type": "Phonetic Calibration"
                    })
                    if len(candidates) >= 4:
                        break

        return candidates[:4]

    def generate_vastu_and_operational_remedies(
        self,
        business_root: int,
        category: str,
        founder_driver: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Compiles actionable physical, directional (Vastu), stationery, and timing remedies.
        Strictly zero expensive rituals or magical claims.
        """
        # 1. Orientation & Workspace Vastu
        if business_root in [1, 9]:
            seating_dir = "East (Surya Orientation)"
            desk_rationale = "Founder desk facing East to capture solar vitality, commanding authority, and executive clarity."
        elif business_root in [5, 6]:
            seating_dir = "North (Kuber & Mercury Orientation)"
            desk_rationale = "Founder desk facing North to activate commercial cash flow, agile client communications, and trade momentum."
        elif business_root == 3:
            seating_dir = "North-East (Ishanya Orientation)"
            desk_rationale = "Founder desk facing North-East to foster intellectual wisdom, strategic clarity, and ethical institutional scale."
        else:
            seating_dir = "East or North (Universal Clean Vector)"
            desk_rationale = "Align seating toward East or North; avoid sitting under exposed steel overhead beams or facing blank South walls."

        # 2. Approved Brand Colors
        if business_root == 1:
            palette = [
                {"name": "Jupiter Gold", "hex": "#C9A227", "role": "Primary Authority"},
                {"name": "Warm Amber", "hex": "#D97706", "role": "Secondary Vitality"},
                {"name": "Venus Pearl", "hex": "#FFFDF7", "role": "Background Clarity"}
            ]
        elif business_root == 3:
            palette = [
                {"name": "Saffron Gold", "hex": "#E2B84B", "role": "Primary Expansion"},
                {"name": "Sandalwood Ink", "hex": "#523E28", "role": "Secondary Wisdom"},
                {"name": "Venus Pearl", "hex": "#FFFDF7", "role": "Background Clarity"}
            ]
        elif business_root == 5:
            palette = [
                {"name": "Mercury Emerald", "hex": "#16835B", "role": "Primary Commerce"},
                {"name": "Jupiter Gold", "hex": "#C9A227", "role": "Secondary Prestige"},
                {"name": "Venus Pearl", "hex": "#FFFDF7", "role": "Background Clarity"}
            ]
        elif business_root == 6:
            palette = [
                {"name": "Jupiter Gold", "hex": "#C9A227", "role": "Primary Opulence"},
                {"name": "Rose Gold Tint", "hex": "#F7F3EA", "role": "Secondary Harmony"},
                {"name": "Sandalwood Accent", "hex": "#7A654D", "role": "Accent Typography"}
            ]
        else:
            palette = [
                {"name": "Jupiter Gold", "hex": "#C9A227", "role": "Primary Balance"},
                {"name": "Deep Navy Sapphire", "hex": "#1E3A8A", "role": "Secondary Trust"},
                {"name": "Venus Pearl", "hex": "#FFFDF7", "role": "Background Light"}
            ]

        # 3. Stationery & Visiting Card Geometry
        stationery_advice = [
            "Position brand emblem at Top-Left (Ascending Growth) or Top-Center (Sovereign Authority).",
            "Wordmark typography should use a confident serif (Cinzel) or clean sans-serif (Inter) with generous letter spacing (4px to 6px).",
            "Never place founder designation directly below folded lines or cut margins; preserve clear optical breathing space (minimum 15% padding).",
            "Visiting card layout: Use golden ratio (1:1.618) card proportions with theme gold or emerald embossed foil on ivory cardstock."
        ]

        # 4. Auspicious Launch & Contract Signing Windows
        timing_advice = {
            "favourable_weekdays": ["Wednesday (Commercial Speed)", "Thursday (Expansion & Scale)", "Friday (Customer Delight & Opulence)"],
            "muhurat_time_slots": ["09:30 AM – 11:30 AM (Solar & Mercurial Prana Window)", "02:30 PM – 04:00 PM (Afternoon Momentum Window)"],
            "contract_signing_rule": "Execute key customer agreements, partnership MoUs, and domain launches during the waxing moon phase (Shukla Paksha)."
        }

        # 5. Accounts & Cash Box Placement
        accounts_placement = {
            "zone": "North or North-East Sector",
            "direction_faced_when_opening": "North (Kuber Gateway)",
            "practical_guidance": "Keep financial ledgers, bank token authenticators, and cash drawers organized, clutter-free, and well-lit with warm white lighting."
        }

        return {
            "office_seating_orientation": {
                "direction": seating_dir,
                "rationale": desk_rationale
            },
            "brand_color_palette": palette,
            "stationery_and_visiting_card_guidelines": stationery_advice,
            "auspicious_timing_windows": timing_advice,
            "accounts_and_cash_zone": accounts_placement,
            "zero_cost_policy": "All remedies are practical architectural, optical, and operational adjustments. Numeros Vision strictly opposes charging for miracle items or mandatory curses."
        }

    def evaluate_startup_option(
        self,
        founder: FounderProfile,
        option: CandidateBusinessOption,
    ) -> StartupEvaluationResult:
        """
        Section 1.A: Evaluates a candidate startup idea comparing commercial viability
        against independent traditional numerology, acoustic letter breakdown, and archetype frameworks.
        """
        # 1. Classify activity via deterministic taxonomy
        tax_result = self.taxonomy.classify(option.name, option.activity_description)
        category = tax_result["primary_category"]

        # 2. Evidence-Based Commercial Viability Checks
        comm_findings = []

        # Skill match
        combined_text = f"{option.activity_description} {option.revenue_model}".lower()
        has_skill_match = any(s.lower() in combined_text for s in founder.skills) or founder.experience_years >= 5
        if has_skill_match:
            comm_findings.append(f"Founder skills and {founder.experience_years} years experience support operational requirements.")
        else:
            comm_findings.append("Skill gap identified: Founder background has limited direct overlap with proposed business activities.")

        # Capital sufficiency check
        capital_ranks = {"bootstrapped": 1, "seed_10k_50k": 2, "growth_50k_250k": 3, "institutional_250k_plus": 4}
        founder_cap_rank = capital_ranks.get(founder.capital_band, 1)
        req_cap_rank = capital_ranks.get(option.estimated_startup_capital_required, 2)
        capital_ok = founder_cap_rank >= req_cap_rank
        if capital_ok:
            comm_findings.append(f"Founder capital band ({founder.capital_band}) is sufficient for initial runway.")
        else:
            comm_findings.append(f"Capital constraint: Option typically requires {option.estimated_startup_capital_required}, exceeding current founder capital.")

        # Operational complexity
        if option.revenue_model in ["brick_and_mortar", "hardware_manufacturing"]:
            op_complexity = "high"
        elif option.revenue_model in ["ecommerce", "b2b_retainer"]:
            op_complexity = "moderate"
        else:
            op_complexity = "low"

        reg_feasibility = "Standard commercial registration required."
        if option.regulatory_tier == "heavily_regulated":
            reg_feasibility = "Strict statutory compliance and capital adequacy licensing mandatory before trading."

        comm_check = CommercialViabilityCheck(
            skill_match=has_skill_match,
            capital_sufficient=capital_ok,
            operational_complexity=op_complexity,
            regulatory_feasibility=reg_feasibility,
            findings=comm_findings,
        )

        # 3. Independent Traditional Numerology & Letter-by-Letter Acoustic Analysis
        acoustic = self.build_acoustic_breakdown(option.name)
        compound = acoustic["total_compound"]
        single = acoustic["total_root"]

        # Compound Profile Reading
        compound_profile = self.get_compound_profile_reading(compound, single)

        # Candidate Archetypes from Contextual Engine
        matched_archetypes = self.archetypes.evaluate_business_archetypes(
            category=category,
            product_functions=tax_result["product_functions"],
            customer_outcomes=tax_result["customer_outcomes"],
            allow_draft_rules=True,
        )
        arch_names = [a["archetype"] for a in matched_archetypes]

        # Founder Synergy Matrix
        founder_synergy = self.evaluate_founder_synergy(
            founder_dob=founder.dob,
            founder_name=founder.name,
            business_root=single
        )

        reasons = []
        conflicts = []
        unknowns = []

        if founder_synergy.get("has_dob"):
            d = founder_synergy["driver"]
            c = founder_synergy["conductor"]
            dp = founder_synergy["driver_planet"]
            cp = founder_synergy["conductor_planet"]
            reasons.append(f"Founder Driver {d} ({dp}) and Conductor {c} ({cp}) analyzed against business root {single} ({PLANET_NAMES.get(single, '')}).")
            reasons.append(f"Synergy Score: {founder_synergy['synergy_score']}% · {founder_synergy['status']}.")
            if single in [1, 3, 5, 6]:
                reasons.append(f"Business name root {single} is a recognized auspicious commercial harmony vibration (1, 3, 5, 6).")
        else:
            unknowns.append("No founder date of birth provided; founder-business compatibility marked INSUFFICIENT_EVIDENCE.")

        # Alignment status determination
        if not founder.dob:
            trad_status = "insufficient_evidence"
        elif founder_synergy.get("badge_type") == "friction" or (single in [4, 8] and "Saturn" not in arch_names):
            trad_status = "conflicted"
            conflicts.append(f"Name root {single} ({PLANET_NAMES.get(single, '')}) associates with heavy gestation periods and karmic lessons unless supported by industrial endurance archetypes.")
            if founder_synergy.get("badge_type") == "friction":
                conflicts.append("Founder Driver or Conductor carries anti/enemy tension with business root number.")
        elif single in [1, 3, 5, 6] and arch_names:
            trad_status = "aligned"
        else:
            trad_status = "partially_aligned"

        # Auspicious Balanced Spelling Suggestions
        balanced_spellings = self.generate_balanced_spelling_recommendations(
            base_name=option.name,
            current_compound=compound,
            current_root=single,
            target_roots=[1, 3, 5, 6]
        )

        # Vastu & Operational Remedies
        founder_d = founder_synergy.get("driver") if founder_synergy.get("has_dob") else None
        vastu_remedies = self.generate_vastu_and_operational_remedies(
            business_root=single,
            category=category,
            founder_driver=founder_d
        )

        trad_check = TraditionalAlignmentCheck(
            framework="Classical Chaldean + Vedic Planetary Archetypes",
            alignment_status=trad_status,
            candidate_archetypes=arch_names,
            name_compound=compound,
            name_single=single,
            reasons=reasons,
            conflicts=conflicts,
            unknowns=unknowns,
            letter_breakdown=acoustic.get("words", []),
            compound_profile=compound_profile,
            founder_synergy=founder_synergy,
            balanced_spelling_recommendations=balanced_spellings,
            vastu_and_operational_remedies=vastu_remedies,
        )

        # 4. Synthesis & Recommendations
        if comm_check.skill_match and comm_check.capital_sufficient:
            synthesis = "COMMERCIALLY_VIABLE"
            next_steps = [
                "Conduct customer discovery interviews with 15 target enterprise buyers.",
                "Check trademark registry for proposed wordmark spelling.",
                "Review balanced name spelling suggestions if targeting high-velocity retail scaling.",
                "Align corporate desk and brand color palette with recommended Vastu vectors.",
            ]
        else:
            synthesis = "COMMERCIAL_PREREQUISITES_REQUIRED"
            next_steps = [
                "Address identified capital or skill gaps before incorporating legal entity.",
                "Explore co-founder partnerships to mitigate operational complexity.",
                "Re-evaluate capital requirements with a phased MVP delivery channel.",
            ]

        return StartupEvaluationResult(
            idea_id=option.idea_id,
            business_name=option.name,
            commercial_viability=comm_check,
            traditional_alignment=trad_check,
            synthesis_recommendation=synthesis,
            next_steps=next_steps,
        )

    def diagnose_existing_business(
        self,
        legal_name: str,
        trading_name: str,
        products_services: str,
        current_constraints: List[str],
        performance_challenges: List[str],
        logo_color_preference: str = "#C9A227",
    ) -> Dict[str, Any]:
        """
        Section 1.B: Diagnostic for operating businesses that cannot change core activities.
        - Distinguishes fixed constraints from changeable factors.
        - Provides practical commercial improvements first.
        - Performs letter-by-letter acoustic analysis of both Legal and Trading names.
        - Evaluates compound and root harmony between Legal entity and Trading brand.
        - Generates auspicious brand spelling variations and zero-cost lifestyle/Vastu remedies.
        """
        # 1. Distinguish fixed vs changeable factors
        fixed_factors = []
        changeable_factors = []

        for c in current_constraints:
            c_lower = c.lower()
            if any(k in c_lower for k in ["lease", "license", "statutory", "core product", "equipment", "patent"]):
                fixed_factors.append(f"Fixed Constraint: {c}")
            else:
                changeable_factors.append(f"Changeable Factor: {c}")

        if not fixed_factors:
            fixed_factors.append("Core product category and statutory operating licenses remain fixed.")
        changeable_factors.extend([
            "Trading name spelling balancing and sub-brand architecture",
            "Logo color contrast, typography, and vector deliverable modernization",
            "Marketing messaging, customer onboarding flow, and conversion copy",
            "Desk seating orientation and financial ledger placement in office premises"
        ])

        # 2. Practical Business Improvements First
        practical_improvements = []
        for p in performance_challenges:
            p_lower = p.lower()
            if "cash flow" in p_lower or "revenue" in p_lower:
                practical_improvements.append("Audit payment collection cycles and renegotiate supplier credit terms from 30 to 60 days.")
            elif "customer" in p_lower or "retention" in p_lower:
                practical_improvements.append("Implement automated customer onboarding, automated post-purchase surveys, and NPS feedback loops.")
            elif "delay" in p_lower or "claim" in p_lower:
                practical_improvements.append("Standardize documentation checklists to reduce billing processing latency.")
            else:
                practical_improvements.append(f"Conduct root-cause operational analysis on: '{p}'.")

        if not practical_improvements:
            practical_improvements.append("Review unit economics and refine high-margin customer segments.")

        # 3. Traditional Name & Brand Balancing
        legal_breakdown = self.build_acoustic_breakdown(legal_name)
        trading_breakdown = self.build_acoustic_breakdown(trading_name)

        legal_comp = legal_breakdown["total_compound"]
        legal_single = legal_breakdown["total_root"]
        trading_comp = trading_breakdown["total_compound"]
        trading_single = trading_breakdown["total_root"]

        legal_profile = self.get_compound_profile_reading(legal_comp, legal_single)
        trading_profile = self.get_compound_profile_reading(trading_comp, trading_single)

        # Alignment between legal and trading name
        is_legal_harmonious = legal_single in [1, 3, 5, 6]
        is_trading_harmonious = trading_single in [1, 3, 5, 6]

        if is_trading_harmonious and is_legal_harmonious:
            brand_alignment_status = "SUPER_HARMONIOUS"
            rec_text = f"Both Trading Name ({trading_comp}/{trading_single}) and Legal Entity ({legal_comp}/{legal_single}) vibrate in auspicious harmony with expansive commercial planets."
        elif is_trading_harmonious and not is_legal_harmonious:
            brand_alignment_status = "PROTECTED_FRONTEND"
            rec_text = f"Trading name compound {trading_comp} (Root {trading_single}) effectively shields customer-facing brand from legal entity's foundational root {legal_single}. No frontend change needed."
        else:
            brand_alignment_status = "FRICTION_DETECTED"
            rec_text = f"Trading name compound {trading_comp} (Root {trading_single} - {PLANET_NAMES.get(trading_single, '')}) carries foundational lessons. Consider balancing spelling toward roots 1, 3, 5, or 6."

        brand_adjustments = {
            "legal_name_compound": legal_comp,
            "legal_name_root": legal_single,
            "legal_name_planet": PLANET_NAMES.get(legal_single, "Universal"),
            "trading_name_compound": trading_comp,
            "trading_name_root": trading_single,
            "trading_name_planet": PLANET_NAMES.get(trading_single, "Universal"),
            "brand_alignment_status": brand_alignment_status,
            "trading_name_recommendation": rec_text,
        }

        # Auspicious spelling alternatives for trading name if friction
        spelling_suggestions = self.generate_balanced_spelling_recommendations(
            base_name=trading_name,
            current_compound=trading_comp,
            current_root=trading_single,
            target_roots=[1, 3, 5, 6]
        )

        # Traditional Vastu and operational remedies
        vastu_remedies = self.generate_vastu_and_operational_remedies(
            business_root=trading_single,
            category="operating_business"
        )

        # Section 1.B & 4 Remedies with Cost/Risk Disclosure
        remedies = [
            {
                "remedy_type": "lifestyle_and_operational",
                "title": "East / North Workspace Orientation Alignment",
                "rationale": f"Traditional Vastu alignment to enhance clarity, solar leadership, and commercial trade focus for Root {trading_single}.",
                "cost_estimate": "$0.00 (Zero Cost)",
                "mandatory": False,
                "disclaimer": "Traditional symbolic practice; does not replace commercial execution.",
            },
            {
                "remedy_type": "brand_color_balancing",
                "title": "Jupiter Gold & Emerald Theme Integration",
                "rationale": "Introduce theme gold (#C9A227) and emerald (#16835B) into brand stationery to symbolize wisdom and clarity.",
                "cost_estimate": "$0.00 (Included in digital assets)",
                "mandatory": False,
                "disclaimer": "Aesthetic suggestion under Numeros Vision design system.",
            },
            {
                "remedy_type": "visiting_card_recalibration",
                "title": "Golden Ratio Stationery Re-Typesetting",
                "rationale": "Position brand mark in upper quadrant with generous optical clear space to project organizational stability.",
                "cost_estimate": "$0.00 (Digital re-export)",
                "mandatory": False,
                "disclaimer": "Visual design best practice conforming to WCAG 2.1 AAA contrast.",
            }
        ]

        return {
            "legal_name": legal_name,
            "trading_name": trading_name,
            "legal_breakdown": legal_breakdown.get("words", []),
            "trading_breakdown": trading_breakdown.get("words", []),
            "legal_profile": legal_profile,
            "trading_profile": trading_profile,
            "fixed_vs_changeable": {
                "fixed_constraints": fixed_factors,
                "changeable_factors": changeable_factors,
            },
            "practical_improvements_first": practical_improvements,
            "brand_and_name_adjustments": brand_adjustments,
            "balanced_spelling_recommendations": spelling_suggestions,
            "traditional_remedies": remedies,
            "vastu_and_operational_remedies": vastu_remedies,
            "statutory_notice": (
                "Statutory Disclosure: Traditional remedies and numerological balancing are optional symbolic cultural practices. "
                "Expensive gemstones, lucky charms, or mandatory rituals are never required by Numeros Vision and do not guarantee business turnaround."
            ),
        }
