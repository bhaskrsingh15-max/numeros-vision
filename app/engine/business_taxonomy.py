"""
Numeros Vision — Hierarchical Business Taxonomy Engine
Defines the configurable business taxonomy, product functions, customer outcomes,
and operational parameters required by Section 2 and Section 16 of the Master Build Specification.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set, Any
import re


@dataclass
class TaxonomyNode:
    category_id: str
    name: str
    parent_id: Optional[str] = None
    description: str = ""
    keywords: List[str] = field(default_factory=list)
    product_functions: List[str] = field(default_factory=list)
    customer_outcomes: List[str] = field(default_factory=list)
    default_intensity: str = "moderate"
    regulatory_tier: str = "standard"


# Curated, approved taxonomy baseline
TAXONOMY_TREE: Dict[str, TaxonomyNode] = {
    # Sports & Athletics Domain
    "sports": TaxonomyNode(
        category_id="sports",
        name="Sports & Physical Performance",
        description="Activities, products, and services centered around physical exertion, athletic competition, and training.",
        keywords=["sport", "sports", "athletics", "athlete", "exercise", "fitness", "training", "workout"],
        product_functions=["physical_performance", "exercise_support", "athletic_conditioning"],
        customer_outcomes=["health", "fitness", "competition", "physical_agility"],
    ),
    "athletic_footwear": TaxonomyNode(
        category_id="athletic_footwear",
        name="Athletic Footwear & Performance Shoes",
        parent_id="sports",
        description="Footwear designed specifically for sports, running, training, and athletic movement.",
        keywords=["shoe", "shoes", "sneaker", "sneakers", "footwear", "cleats", "running shoes", "trainer", "trainers"],
        product_functions=["foot_protection", "traction", "cushioning", "speed_support", "endurance_running", "motion_guidance"],
        customer_outcomes=["speed", "endurance", "foot_support", "performance_amplification", "injury_prevention"],
        default_intensity="high_performance",
    ),
    "sportswear": TaxonomyNode(
        category_id="sportswear",
        name="Sportswear & Activewear",
        parent_id="sports",
        description="Apparel engineered for athletic activities and workouts.",
        keywords=["sportswear", "activewear", "apparel", "jersey", "shorts", "leggings", "compression"],
        product_functions=["moisture_wicking", "flexibility", "aerodynamics", "temperature_regulation"],
        customer_outcomes=["comfort_during_motion", "aerodynamic_efficiency", "athletic_aesthetic"],
    ),
    "endurance_sports": TaxonomyNode(
        category_id="endurance_sports",
        name="Endurance & Marathon Athletics",
        parent_id="sports",
        description="Long-duration physical activities demanding stamina and prolonged physical discipline.",
        keywords=["marathon", "triathlon", "cycling", "distance running", "stamina", "endurance"],
        product_functions=["aerobic_support", "pacing", "fatigue_mitigation", "hydration_ergonomics"],
        customer_outcomes=["endurance", "stamina", "discipline", "sustained_effort"],
        default_intensity="extreme_endurance",
    ),
    "team_sports": TaxonomyNode(
        category_id="team_sports",
        name="Team Sports & League Athletics",
        parent_id="sports",
        description="Collaborative competitive sports such as football, basketball, cricket, and rugby.",
        keywords=["team", "football", "basketball", "cricket", "soccer", "league", "club"],
        product_functions=["team_coordination", "tactical_play", "competitive_scoring"],
        customer_outcomes=["camaraderie", "competition", "victory", "team_cohesion"],
    ),
    "sports_equipment": TaxonomyNode(
        category_id="sports_equipment",
        name="Sports Gear & Hardware",
        parent_id="sports",
        description="Physical hardware and gear utilized in sporting activities.",
        keywords=["equipment", "gear", "ball", "bat", "racket", "helmet", "weights", "dumbbells"],
        product_functions=["ballistic_impact", "structural_durability", "precision_handling"],
        customer_outcomes=["precision", "safety", "impact_absorption", "score_enhancement"],
    ),
    "sports_coaching": TaxonomyNode(
        category_id="sports_coaching",
        name="Sports Coaching & Mentorship",
        parent_id="sports",
        description="Guidance and tactical training provided to athletes.",
        keywords=["coaching", "trainer", "mentor", "drills", "conditioning_coach"],
        product_functions=["instruction", "tactical_critique", "discipline_enforcement"],
        customer_outcomes=["mastery", "discipline", "skill_progression"],
    ),

    # Technology & Software
    "technology": TaxonomyNode(
        category_id="technology",
        name="Technology & Digital Systems",
        description="Digital software, hardware, cloud computing, and telecommunications.",
        keywords=["tech", "software", "app", "cloud", "ai", "hardware", "code", "digital"],
        product_functions=["data_processing", "automation", "connectivity", "computation"],
        customer_outcomes=["efficiency", "scalability", "speed", "automation"],
    ),

    # Hospitality & Food
    "hospitality_food": TaxonomyNode(
        category_id="hospitality_food",
        name="Hospitality, Dining & Food Service",
        description="Restaurants, culinary experiences, food production, and nourishment.",
        keywords=["restaurant", "food", "dining", "cafe", "culinary", "bakery", "beverage"],
        product_functions=["nourishment", "taste_satisfaction", "social_hospitality"],
        customer_outcomes=["delight", "sustenance", "relaxation", "social_connection"],
    ),

    # Finance & Investment
    "finance": TaxonomyNode(
        category_id="finance",
        name="Financial Services & Wealth Management",
        description="Banking, asset management, investment, insurance, and lending.",
        keywords=["bank", "finance", "investment", "wealth", "lending", "credit", "fintech"],
        product_functions=["wealth_preservation", "capital_growth", "risk_underwriting"],
        customer_outcomes=["financial_security", "yield", "liquidity", "trust"],
        regulatory_tier="heavily_regulated",
    ),

    # Children & Education
    "children_education": TaxonomyNode(
        category_id="children_education",
        name="Children, Early Learning & Toys",
        description="Childcare, pediatric goods, toys, and early childhood education.",
        keywords=["child", "children", "kids", "toy", "nursery", "preschool", "pediatric"],
        product_functions=["developmental_play", "safety", "nurturing", "curiosity_stimulation"],
        customer_outcomes=["joy", "cognitive_growth", "safety", "protection"],
    ),
}


class BusinessTaxonomyEngine:
    """
    Deterministic taxonomy classifier that maps free-form business descriptions
    into structured category nodes, product functions, and customer outcomes.
    """

    def __init__(self, taxonomy: Optional[Dict[str, TaxonomyNode]] = None):
        self.taxonomy = taxonomy or TAXONOMY_TREE

    def classify(self, business_name: str, description: str, hints: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Classifies business inputs into primary and secondary categories.
        Guarantees that ambiguous inputs return low confidence or UNKNOWN.
        """
        combined_text = f"{business_name} {description} {' '.join(hints or [])}".lower()
        tokens = set(re.findall(r"\b[a-z0-9_-]+\b", combined_text))

        matched_scores: Dict[str, int] = {}
        matched_functions: Set[str] = set()
        matched_outcomes: Set[str] = set()

        for node_id, node in self.taxonomy.items():
            score = 0
            # Direct category id match
            if node_id in tokens or node_id.replace("_", " ") in combined_text:
                score += 5

            # Keyword matching
            for kw in node.keywords:
                if kw in combined_text:
                    score += 2

            if score > 0:
                matched_scores[node_id] = score
                matched_functions.update(node.product_functions)
                matched_outcomes.update(node.customer_outcomes)

        if not matched_scores:
            return {
                "primary_category": "UNKNOWN",
                "secondary_categories": [],
                "confidence": 0.0,
                "confidence_label": "INSUFFICIENT_EVIDENCE",
                "product_functions": [],
                "customer_outcomes": [],
                "classification_evidence": "No matching taxonomy keywords identified in description.",
            }

        sorted_matches = sorted(matched_scores.items(), key=lambda x: x[1], reverse=True)
        primary_id = sorted_matches[0][0]
        top_score = sorted_matches[0][1]

        secondary_ids = [node_id for node_id, s in sorted_matches[1:] if s >= 2]

        confidence = min(1.0, top_score / 10.0)
        confidence_label = "HIGH" if confidence >= 0.7 else ("MODERATE" if confidence >= 0.4 else "LOW")

        primary_node = self.taxonomy[primary_id]

        return {
            "primary_category": primary_id,
            "primary_category_name": primary_node.name,
            "secondary_categories": secondary_ids,
            "confidence": confidence,
            "confidence_label": confidence_label,
            "product_functions": sorted(list(matched_functions)),
            "customer_outcomes": sorted(list(matched_outcomes)),
            "default_intensity": primary_node.default_intensity,
            "regulatory_tier": primary_node.regulatory_tier,
            "classification_evidence": f"Matched {len(sorted_matches)} categories based on explicit keyword correlations.",
        }

    def get_node(self, category_id: str) -> Optional[TaxonomyNode]:
        return self.taxonomy.get(category_id)
