"""
Search Opportunity Prioritizer
Implements Section 8 (Opportunity Prioritization Normalized Model)
"""

from typing import Dict, Any, Optional

class OpportunityScorer:
    """Calculates transparent 0-100 Opportunity Scores based on the 6 weighted dimensions."""

    WEIGHTS = {
        "demand_evidence": 0.25,
        "search_intent_fit": 0.20,
        "product_relevance": 0.20,
        "existing_authority": 0.15,
        "content_gap": 0.10,
        "conversion_relevance": 0.10
    }

    @classmethod
    def calculate_score(cls, 
                        search_volume: Optional[int], 
                        intent: str, 
                        cluster_name: str, 
                        page_exists: bool,
                        has_product_fit: bool,
                        monetization_tier: str = "medium") -> Dict[str, Any]:
        """
        Calculates normalized score. Returns breakdown and provisional flags.
        """
        is_provisional = False
        missing_fields = []

        # 1. Demand Evidence (0-100)
        if search_volume is None:
            demand_score = 30.0  # Conservative missing baseline
            is_provisional = True
            missing_fields.append("search_volume")
        elif search_volume > 50000:
            demand_score = 100.0
        elif search_volume > 10000:
            demand_score = 85.0
        elif search_volume > 2000:
            demand_score = 70.0
        elif search_volume > 500:
            demand_score = 50.0
        else:
            demand_score = 25.0

        # 2. Search Intent Fit (0-100)
        intent_lower = intent.lower()
        if "transactional" in intent_lower or "tool" in intent_lower:
            intent_score = 95.0
        elif "commercial" in intent_lower:
            intent_score = 90.0
        elif "mixed" in intent_lower:
            intent_score = 80.0
        elif "informational" in intent_lower:
            intent_score = 75.0
        else:
            intent_score = 40.0

        # 3. Product Relevance (0-100)
        product_score = 100.0 if has_product_fit else 50.0

        # 4. Existing Authority / Opportunity (0-100)
        # If page already exists, improving it has high authority leverage (85). If not, starting from 60.
        authority_score = 85.0 if page_exists else 60.0

        # 5. Content Gap (0-100)
        # If no page exists yet, content gap is high (90); if page exists, gap is moderate (50).
        gap_score = 90.0 if not page_exists else 50.0

        # 6. Conversion Relevance (0-100)
        if monetization_tier == "high":
            conversion_score = 95.0
        elif monetization_tier == "medium":
            conversion_score = 75.0
        else:
            conversion_score = 45.0

        # Calculate weighted composite
        composite_score = (
            cls.WEIGHTS["demand_evidence"] * demand_score +
            cls.WEIGHTS["search_intent_fit"] * intent_score +
            cls.WEIGHTS["product_relevance"] * product_score +
            cls.WEIGHTS["existing_authority"] * authority_score +
            cls.WEIGHTS["content_gap"] * gap_score +
            cls.WEIGHTS["conversion_relevance"] * conversion_score
        )

        return {
            "opportunity_score": round(composite_score, 1),
            "is_provisional": is_provisional,
            "missing_fields": missing_fields,
            "breakdown": {
                "demand_evidence": demand_score,
                "search_intent_fit": intent_score,
                "product_relevance": product_score,
                "existing_authority": authority_score,
                "content_gap": gap_score,
                "conversion_relevance": conversion_score
            },
            "priority_tier": "P0 (Live Critical)" if composite_score >= 80 else ("P1 (High Priority)" if composite_score >= 65 else "P2 (Secondary)")
        }
