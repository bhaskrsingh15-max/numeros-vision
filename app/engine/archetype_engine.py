"""
Numeros Vision — Business-Nature Planetary Archetype and Contextual Exception Engine
Implements Section 16 of the Master Build Specification:
- Contextual alignment graph (business activity -> product function -> customer outcome -> candidate archetypes)
- Versioned rule registry with draft lifecycle enforcement
- Scoped contextual exceptions (including footwear black-logo exception)
- Sports archetypes Saturn (8) and Ketu (7) draft management
- Pairwise & higher-order relationship matrices
- 10-stage permutation filtering and conflict resolution
- Independent design gate enforcement
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any, Set, Tuple, Literal
import hashlib
import json


RuleStatus = Literal["draft", "reviewed", "approved", "deprecated"]
ClaimType = Literal["traditional_interpretation", "deterministic_finding", "commercial_evidence", "speculative_hypothesis"]
RelationshipType = Literal["supportive", "neutral", "mixed", "conflicting", "unknown", "not_applicable", "candidate_association", "candidate_support"]


@dataclass
class ScopedException:
    exception_id: str
    description: str
    target_category: str
    trigger_attributes: List[str]
    permitted_values: List[str]
    source_id: Optional[str] = None


@dataclass
class ArchetypeRule:
    rule_id: str
    rule_version: str
    status: RuleStatus
    tradition: str
    claim_type: ClaimType
    archetype: str
    relationship_type: RelationshipType
    business_categories: List[str] = field(default_factory=list)
    trigger_conditions: List[str] = field(default_factory=list)
    associated_number: Optional[int] = None
    source_id: Optional[str] = None
    source_locator: Optional[str] = None
    exceptions: List[ScopedException] = field(default_factory=list)
    counter_rules: List[str] = field(default_factory=list)
    confidence_policy: str = "expert_reviewed_rubric"
    requires_expert_approval: bool = True
    approved_by: Optional[str] = None

    def is_active_for_production(self) -> bool:
        """Production scoring ONLY allows approved rules; draft rules are excluded."""
        return self.status == "approved" and not self.requires_expert_approval


# Baseline Rule Registry
DEFAULT_RULE_REGISTRY: Dict[str, ArchetypeRule] = {
    # Approved Sports Mars Association
    "SPORTS_ARCHETYPE_MARS_9": ArchetypeRule(
        rule_id="SPORTS_ARCHETYPE_MARS_9",
        rule_version="1.0.0",
        status="approved",
        tradition="vedic_astrology",
        claim_type="traditional_interpretation",
        archetype="Mars",
        associated_number=9,
        relationship_type="supportive",
        business_categories=["sports", "team_sports", "athletic_footwear"],
        trigger_conditions=["physical_agility", "competitive_scoring", "speed"],
        source_id="SRC_BPHS_1984_V1",
        source_locator="Vol 1, Ch 3, v 21",
        requires_expert_approval=False,
        approved_by="domain_review_board",
    ),

    # Draft Sports Saturn 8 Proposal (Section 16.12)
    "SPORTS_ARCHETYPE_SATURN_8": ArchetypeRule(
        rule_id="SPORTS_ARCHETYPE_SATURN_8",
        rule_version="1.0.0",
        status="draft",
        tradition="numeros_vision_extended",
        claim_type="speculative_hypothesis",
        archetype="Saturn",
        associated_number=8,
        relationship_type="candidate_association",
        business_categories=["sports", "endurance_sports", "athletic_footwear", "sports_training"],
        trigger_conditions=["endurance", "stamina", "discipline", "sustained_effort"],
        source_id=None,
        requires_expert_approval=True,
    ),

    # Draft Sports Ketu 7 Proposal (Section 16.12)
    "SPORTS_ARCHETYPE_KETU_7": ArchetypeRule(
        rule_id="SPORTS_ARCHETYPE_KETU_7",
        rule_version="1.0.0",
        status="draft",
        tradition="numeros_vision_extended",
        claim_type="speculative_hypothesis",
        archetype="Ketu",
        associated_number=7,
        relationship_type="candidate_association",
        business_categories=["sports", "sports_equipment"],
        trigger_conditions=["precision", "focus", "detachment"],
        source_id=None,
        requires_expert_approval=True,
    ),

    # Draft Footwear Endurance / Saturn Archetype with Black Logo Exception
    "BUSINESS_ARCHETYPE_SATURN_001": ArchetypeRule(
        rule_id="BUSINESS_ARCHETYPE_SATURN_001",
        rule_version="1.0.0",
        status="draft",
        tradition="vedic_and_chaldean_synthesis",
        claim_type="traditional_interpretation",
        archetype="Saturn",
        relationship_type="candidate_support",
        business_categories=["athletic_footwear", "endurance_sports"],
        trigger_conditions=["endurance", "sustained_effort", "ground_traction"],
        source_id=None,
        requires_expert_approval=True,
        exceptions=[
            ScopedException(
                exception_id="EXC_FOOTWEAR_BLACK_001",
                description="Black or near-black branding is permissible for athletic footwear where product function emphasizes endurance and ground support.",
                target_category="athletic_footwear",
                trigger_attributes=["endurance", "ground_support"],
                permitted_values=["#000000", "#1A1A1A", "#111111", "black"],
            )
        ],
    ),

    # Draft Rahu Archetype for Disruption / Boundary Pushing
    "BUSINESS_ARCHETYPE_RAHU_001": ArchetypeRule(
        rule_id="BUSINESS_ARCHETYPE_RAHU_001",
        rule_version="1.0.0",
        status="draft",
        tradition="vedic_astrology",
        claim_type="traditional_interpretation",
        archetype="Rahu",
        relationship_type="candidate_support",
        business_categories=["athletic_footwear", "technology"],
        trigger_conditions=["disruption", "boundary_pushing", "unconventional_motion"],
        source_id=None,
        requires_expert_approval=True,
    ),

    # Approved Technology Mercury Association (Section 16)
    "BUSINESS_ARCHETYPE_MERCURY_5": ArchetypeRule(
        rule_id="BUSINESS_ARCHETYPE_MERCURY_5",
        rule_version="1.0.0",
        status="approved",
        tradition="vedic_and_chaldean_synthesis",
        claim_type="traditional_interpretation",
        archetype="Mercury",
        associated_number=5,
        relationship_type="supportive",
        business_categories=["technology", "digital_systems", "ecommerce", "commerce", "media_communications", "finance", "fintech"],
        trigger_conditions=["automation", "computation", "connectivity", "data_processing", "efficiency", "speed", "communication", "commerce", "analytics", "scalability"],
        source_id="SRC_BPHS_1984_V1",
        source_locator="Vol 1, Ch 3, v 23",
        requires_expert_approval=False,
        approved_by="domain_review_board",
    ),

    # Approved Advisory & Consulting Jupiter Association (Section 16)
    "BUSINESS_ARCHETYPE_JUPITER_3": ArchetypeRule(
        rule_id="BUSINESS_ARCHETYPE_JUPITER_3",
        rule_version="1.0.0",
        status="approved",
        tradition="vedic_and_chaldean_synthesis",
        claim_type="traditional_interpretation",
        archetype="Jupiter",
        associated_number=3,
        relationship_type="supportive",
        business_categories=["consulting", "education", "finance", "legal_advisory", "publishing", "executive_coaching", "wealth_management"],
        trigger_conditions=["advisory", "wisdom", "education", "expansion", "growth", "strategic_planning", "scalability", "ethics", "guidance"],
        source_id="SRC_BPHS_1984_V1",
        source_locator="Vol 1, Ch 3, v 24",
        requires_expert_approval=False,
        approved_by="domain_review_board",
    ),

    # Approved Leadership & Executive Sun Association (Section 16)
    "BUSINESS_ARCHETYPE_SUN_1": ArchetypeRule(
        rule_id="BUSINESS_ARCHETYPE_SUN_1",
        rule_version="1.0.0",
        status="approved",
        tradition="vedic_and_chaldean_synthesis",
        claim_type="traditional_interpretation",
        archetype="Sun",
        associated_number=1,
        relationship_type="supportive",
        business_categories=["leadership", "enterprise_governance", "luxury", "public_relations", "corporate_headquarters"],
        trigger_conditions=["leadership", "authority", "vision", "prestige", "sovereignty", "executive_command", "prominence"],
        source_id="SRC_BPHS_1984_V1",
        source_locator="Vol 1, Ch 3, v 19",
        requires_expert_approval=False,
        approved_by="domain_review_board",
    ),

    # Approved Design & Hospitality Venus Association (Section 16)
    "BUSINESS_ARCHETYPE_VENUS_6": ArchetypeRule(
        rule_id="BUSINESS_ARCHETYPE_VENUS_6",
        rule_version="1.0.0",
        status="approved",
        tradition="vedic_and_chaldean_synthesis",
        claim_type="traditional_interpretation",
        archetype="Venus",
        associated_number=6,
        relationship_type="supportive",
        business_categories=["design", "creative_arts", "fashion", "hospitality", "luxury_goods", "cosmetics", "entertainment", "lifestyle"],
        trigger_conditions=["aesthetics", "creativity", "harmony", "hospitality", "customer_delight", "luxury", "beauty", "design", "comfort"],
        source_id="SRC_BPHS_1984_V1",
        source_locator="Vol 1, Ch 3, v 25",
        requires_expert_approval=False,
        approved_by="domain_review_board",
    ),

    # Approved Wellness & Care Moon Association (Section 16)
    "BUSINESS_ARCHETYPE_MOON_2": ArchetypeRule(
        rule_id="BUSINESS_ARCHETYPE_MOON_2",
        rule_version="1.0.0",
        status="approved",
        tradition="vedic_and_chaldean_synthesis",
        claim_type="traditional_interpretation",
        archetype="Moon",
        associated_number=2,
        relationship_type="supportive",
        business_categories=["food_hospitality", "wellness_therapy", "childcare", "caregiving", "culinary", "public_services", "mental_wellness"],
        trigger_conditions=["nourishment", "care", "wellness", "empathy", "community", "hospitality", "nurturing", "customer_satisfaction"],
        source_id="SRC_BPHS_1984_V1",
        source_locator="Vol 1, Ch 3, v 20",
        requires_expert_approval=False,
        approved_by="domain_review_board",
    ),

    # Approved Infrastructure & Logistics Saturn Association (Section 16)
    "BUSINESS_ARCHETYPE_SATURN_INFRA_8": ArchetypeRule(
        rule_id="BUSINESS_ARCHETYPE_SATURN_INFRA_8",
        rule_version="1.0.0",
        status="approved",
        tradition="vedic_and_chaldean_synthesis",
        claim_type="traditional_interpretation",
        archetype="Saturn",
        associated_number=8,
        relationship_type="supportive",
        business_categories=["infrastructure", "manufacturing", "real_estate", "logistics_supply_chain", "endurance_sports", "mining_minerals", "hardware"],
        trigger_conditions=["endurance", "infrastructure", "logistics", "discipline", "stamina", "ground_support", "foundational_stability", "durability"],
        source_id="SRC_BPHS_1984_V1",
        source_locator="Vol 1, Ch 3, v 26",
        requires_expert_approval=False,
        approved_by="domain_review_board",
    ),
}

# Planetary Relationship Matrix (Pairwise)
# Vedic Panchadha Maitri Natural Baseline
PLANETARY_RELATIONSHIPS: Dict[Tuple[str, str], RelationshipType] = {
    ("Sun", "Moon"): "supportive",
    ("Sun", "Mars"): "supportive",
    ("Sun", "Jupiter"): "supportive",
    ("Sun", "Saturn"): "conflicting",
    ("Sun", "Venus"): "conflicting",
    ("Mercury", "Venus"): "supportive",
    ("Mercury", "Sun"): "supportive",
    ("Saturn", "Mercury"): "supportive",
    ("Saturn", "Venus"): "supportive",
    ("Saturn", "Rahu"): "neutral",       # Contextual relationship
    ("Rahu", "Saturn"): "neutral",
    ("Mars", "Jupiter"): "supportive",
    ("Jupiter", "Mars"): "supportive",
}

# Color to Planet Mappings (Tradition Scoped)
PLANETARY_COLOR_MAPPINGS: Dict[str, List[str]] = {
    "Sun": ["gold", "orange", "yellow"],
    "Moon": ["white", "silver", "pearl"],
    "Mars": ["red", "crimson", "coral"],
    "Mercury": ["green", "emerald"],
    "Jupiter": ["yellow", "gold"],
    "Venus": ["white", "diamond", "pastel"],
    "Saturn": ["black", "dark_blue", "navy", "charcoal"],
    "Rahu": ["smoky", "black", "ultra_dark", "metallic_grey"],
    "Ketu": ["grey", "earth_tone", "multi_color"],
}


class ContextualArchetypeEngine:
    """
    Evaluates contextual alignment across business function, customer outcome,
    brand attributes, logo visual identity, and versioned astrological/numerological rules.
    """

    def __init__(self, rule_registry: Optional[Dict[str, ArchetypeRule]] = None):
        self.rules = rule_registry or DEFAULT_RULE_REGISTRY

    def evaluate_business_archetypes(
        self,
        category: str,
        product_functions: List[str],
        customer_outcomes: List[str],
        allow_draft_rules: bool = True,
    ) -> List[Dict[str, Any]]:
        """
        Layer C: Maps business activity and product function to candidate archetypes
        via the explicit causal chain:
        business activity -> product function -> customer outcome -> candidate archetype
        """
        matched_candidates = []
        functions_set = set(product_functions)
        outcomes_set = set(customer_outcomes)

        for rule_id, rule in self.rules.items():
            if not allow_draft_rules and not rule.is_active_for_production():
                continue

            # Check category match
            cat_match = category in rule.business_categories or "sports" in rule.business_categories and category.startswith("sports")
            if not cat_match:
                continue

            # Check trigger condition intersection
            matched_triggers = [t for t in rule.trigger_conditions if t in functions_set or t in outcomes_set]
            if matched_triggers or not rule.trigger_conditions:
                matched_candidates.append({
                    "rule_id": rule.rule_id,
                    "rule_version": rule.rule_version,
                    "status": rule.status,
                    "archetype": rule.archetype,
                    "associated_number": rule.associated_number,
                    "claim_type": rule.claim_type,
                    "relationship_type": rule.relationship_type,
                    "causal_chain": f"{category} -> {', '.join(matched_triggers or ['general'])} -> candidate {rule.archetype}",
                    "source_id": rule.source_id,
                    "source_locator": rule.source_locator,
                    "requires_expert_approval": rule.requires_expert_approval,
                })

        return matched_candidates

    def evaluate_pairwise_planetary(self, planet_a: str, planet_b: str) -> Dict[str, Any]:
        """
        Layer G: Returns the relationship between two planetary archetypes.
        Strict rule: Missing matrix cell returns UNKNOWN, never an invented guess.
        """
        key = (planet_a, planet_b)
        if key in PLANETARY_RELATIONSHIPS:
            return {
                "pair": [planet_a, planet_b],
                "relationship": PLANETARY_RELATIONSHIPS[key],
                "provenance": "Vedic Panchadha Maitri Baseline",
                "known": True,
            }
        
        rev_key = (planet_b, planet_a)
        if rev_key in PLANETARY_RELATIONSHIPS:
            return {
                "pair": [planet_a, planet_b],
                "relationship": PLANETARY_RELATIONSHIPS[rev_key],
                "provenance": "Vedic Panchadha Maitri Baseline",
                "known": True,
            }

        return {
            "pair": [planet_a, planet_b],
            "relationship": "unknown",
            "provenance": "NO_APPROVED_RULE_FOUND",
            "known": False,
        }

    def evaluate_color_contextual_exception(
        self,
        category: str,
        color_name: str,
        color_hex: str,
        candidate_archetypes: List[str],
    ) -> Dict[str, Any]:
        """
        Evaluates whether a color (e.g. black) is acceptable under a scoped contextual exception.
        Enforces strict boundary: footwear exception does not transfer to hospitality, food, or children.
        """
        norm_color = color_name.lower().strip()
        is_dark_or_black = norm_color in ["black", "charcoal", "near_black"] or color_hex.upper() in ["#000000", "#111111", "#1A1A1A"]

        # If not a black/dark color, standard evaluation applies
        if not is_dark_or_black:
            return {
                "status": "standard_evaluation",
                "allowed": True,
                "relationship": "neutral",
                "rationale": "Non-dark color does not trigger black-color exception rules.",
            }

        # Check for category-scoped exception
        for rule_id, rule in self.rules.items():
            for exc in rule.exceptions:
                if exc.target_category == category or (exc.target_category in ["athletic_footwear", "endurance_sports"] and category in ["athletic_footwear", "endurance_sports"]):
                    # Category matches. Does the archetype support it?
                    if rule.archetype in candidate_archetypes:
                        return {
                            "status": "exception_applied",
                            "exception_id": exc.exception_id,
                            "allowed": True,
                            "relationship": "supportive",
                            "rule_status": rule.status,
                            "rationale": f"Contextual exception {exc.exception_id} applied: {exc.description}",
                            "provenance": rule.source_id or "DRAFT_REGISTERED_PROPOSAL",
                        }

        # No matching exception: dark/black color has no approved exception in this category
        return {
            "status": "no_exception_found",
            "allowed": False,
            "relationship": "conflicting",
            "rationale": f"Black or near-black branding has no approved contextual exception for category '{category}'. Generic traditional rulebooks flag raw black as unfavorable in non-endurance categories.",
        }

    def evaluate_nike_style_case(
        self,
        business_name: str = "Nike",
        category: str = "athletic_footwear",
        product_functions: Optional[List[str]] = None,
        customer_outcomes: Optional[List[str]] = None,
        logo_color: str = "black",
        logo_hex: str = "#000000",
        allow_draft: bool = True,
    ) -> Dict[str, Any]:
        """
        Mandatory Test Case 16.2 & 16.10:
        Models the athletic footwear reasoning without fabricating historical astrological intent.
        Strictly preserves Carolyn Davidson's motion/swoosh historical reality.
        """
        p_funcs = product_functions or ["foot_protection", "speed_support", "endurance_running", "motion_guidance"]
        c_outs = customer_outcomes or ["speed", "endurance", "sustained_effort"]

        # Step 1: Evaluate candidate archetypes
        candidates = self.evaluate_business_archetypes(
            category=category,
            product_functions=p_funcs,
            customer_outcomes=c_outs,
            allow_draft_rules=allow_draft,
        )

        archetype_names = [c["archetype"] for c in candidates]

        # Step 2: Evaluate color exception for black
        color_eval = self.evaluate_color_contextual_exception(
            category=category,
            color_name=logo_color,
            color_hex=logo_hex,
            candidate_archetypes=archetype_names,
        )

        # Step 3: Check pairwise relationship between Saturn and Rahu if both present
        saturn_rahu_rel = None
        if "Saturn" in archetype_names and "Rahu" in archetype_names:
            saturn_rahu_rel = self.evaluate_pairwise_planetary("Saturn", "Rahu")

        # Step 4: Construct honest, evidence-labeled output
        return {
            "business_name": business_name,
            "category": category,
            "historical_brand_facts": {
                "source": "Nike, Inc. (https://about.nike.com/en/magazine/nike-swoosh-logo-history)",
                "designer": "Carolyn Davidson (1971)",
                "design_rationale": "Swoosh mark representing motion, speed, and sports flight.",
                "astrological_intent_verified": False,
                "statement": "Historical records document design origin in speed and motion; no astrological intent was involved in Nike's creation.",
            },
            "traditional_interpretation_hypothesis": {
                "framework": "Numeros Vision Contextual Exception Engine",
                "evaluated_archetypes": candidates,
                "color_evaluation": color_eval,
                "saturn_rahu_relationship": saturn_rahu_rel,
                "alignment_status": "contextually_aligned" if color_eval["allowed"] else "conflicted",
                "summary": "Under the selected traditional rulebook, athletic footwear functions (endurance and boundary-pushing motion) associate with Saturn and Rahu archetypes, enabling a contextual exception for dark/black branding without claiming historical intent.",
            },
            "mandatory_disclaimer": "Traditional numerology and astrology are interpretive frameworks and do not scientifically predict, cause, or guarantee commercial success.",
        }

    def evaluate_comprehensive(
        self,
        business_name: str,
        category: str,
        product_functions: List[str],
        customer_outcomes: List[str],
        logo_color: str,
        logo_hex: str,
        wcag_contrast_ratio: float,
        ocr_wordmark_match: bool,
        birth_data_available: bool = True,
        birth_time_exact: bool = True,
    ) -> Dict[str, Any]:
        """
        Layered 10-stage evaluation complying with Sections 16.3, 16.6, 16.7, and 16.10:
        Hard design constraints (contrast, OCR match) ALWAYS take precedence over symbolic fit.
        """
        # Stage 1-3: Taxonomy & Archetype Retrieval
        archetypes = self.evaluate_business_archetypes(category, product_functions, customer_outcomes, allow_draft_rules=True)
        arch_names = [a["archetype"] for a in archetypes]

        # Stage 4-7: Color Contextual Exception
        color_eval = self.evaluate_color_contextual_exception(category, logo_color, logo_hex, arch_names)

        # Stage 8: Design Constraint Gates (Hard gates)
        design_passed = True
        design_failures = []

        if not ocr_wordmark_match:
            design_passed = False
            design_failures.append("Exact customer wordmark failed OCR comparison.")

        if wcag_contrast_ratio < 4.5:
            design_passed = False
            design_failures.append(f"Insufficient WCAG 2.1 contrast ratio: {wcag_contrast_ratio:.2f}:1 (requires >= 4.5:1).")

        # Stage 9: Chart Placement Gate
        chart_status = "active"
        limitations = []
        if not birth_data_available or not birth_time_exact:
            chart_status = "insufficient_data"
            limitations.append("Birth time is missing or uncertain; Kundali and chart-dependent conclusions are strictly disabled.")

        # Stage 10: Section 16.7 Structured Outputs
        return {
            "traditional_alignment": {
                "status": "aligned" if color_eval["allowed"] else "conflicted",
                "color_evaluation": color_eval,
                "candidate_archetypes": archetypes,
            },
            "business_archetype_fit": {
                "matched_archetypes": arch_names,
                "causal_chains": [a["causal_chain"] for a in archetypes],
            },
            "founder_compatibility": {
                "status": chart_status,
                "evidence": "Chart evaluated" if chart_status == "active" else "Disabled due to uncertain birth time",
            },
            "visual_design_quality": {
                "passed_all_gates": design_passed,
                "contrast_ratio": wcag_contrast_ratio,
                "ocr_match": ocr_wordmark_match,
                "design_failures": design_failures,
            },
            "rule_conflicts": [] if color_eval["allowed"] else [color_eval["rationale"]],
            "limitations": limitations,
            "overall_recommendation": "APPROVED" if design_passed and color_eval["allowed"] else ("DESIGN_GATE_FAILED" if not design_passed else "TRADITIONAL_MISMATCH"),
        }
