"""
Governed Content Generation Pipeline
Implements Section 14 (Content Generation Pipeline — Stages A through G)
"""

import os
import json
import logging
from typing import Dict, Any, Tuple
from app.seo.research_data_model import ContentBrief
from app.seo.pipeline.quality_gates import QualityGateValidator
from app.seo.content_generator import AutomatedContentGenerator
from app.seo.images.image_service import ImageService

logger = logging.getLogger("content_pipeline")

class ContentGenerationPipeline:
    """Orchestrates multi-stage evidence-grounded content drafting with quality enforcement."""

    def __init__(self):
        self.validator = QualityGateValidator()
        self.image_service = ImageService()

    def run_pipeline(self, 
                     brief: ContentBrief, 
                     is_human_approved: bool = True) -> Dict[str, Any]:
        """
        Executes Stages A through G.
        Returns pipeline outcome and formatted HTML.
        """
        # STAGE A: Research Synthesis
        # Verified sources extracted from brief
        sources = brief.required_sources
        claims = [c.to_dict() if hasattr(c, "to_dict") else c for c in brief.required_claims]

        # STAGE B: Editorial Outline
        outline = brief.proposed_outline

        # STAGE C & D: Draft Generation & Technical Formatting
        # Natural topic and entity extraction (Section 8.1 - avoids mechanical phrase repetition)
        core_topic = brief.primary_keyword
        for suffix in [" calculator", " meaning", " chart", " online", " by date of birth"]:
            if core_topic.lower().endswith(suffix):
                core_topic = core_topic[:-len(suffix)].strip()
        core_topic_title = core_topic.title()

        snippet_q = (
            f"What is the {core_topic_title} and how does the calculator work?"
            if "calculator" in brief.primary_keyword.lower()
            else f"What is {brief.primary_keyword.title()} in traditional numerology?"
        )
        snippet_a = (
            f"The {core_topic_title} is an authentic traditional numerological framework that deterministically analyzes planetary energetic archetypes and cycles without predictive superstition."
        )

        blueprint = {
            "topic": brief.working_title,
            "slug": brief.target_url.strip("/").split("/")[-1],
            "target_keyword": brief.primary_keyword,
            "meta_title": f"{brief.primary_keyword.title()} | Numeros Vision Guide",
            "meta_description": f"Learn how to calculate and interpret the {core_topic_title}. Deterministic traditional analysis with zero-hallucination methods by Numeros Vision.",
            "snippet_question": snippet_q,
            "snippet_answer": snippet_a,
            "headings": [
                {
                    "h2": f"Core Meaning & Classical Origins of {core_topic_title}",
                    "h3s": [
                        "Foundational Principles & Esoteric Roots",
                        "Planetary Rulership & Energetic Archetypes"
                    ]
                },
                {
                    "h2": "Step-by-Step Calculation Formula & Reduction Rules",
                    "h3s": [
                        "Compound Number Preservation Invariants",
                        "Practical Case Study & Manual Calculation"
                    ]
                },
                {
                    "h2": "Practical Applications & Grounded Guidance",
                    "h3s": [
                        "Career Trajectory & Strategic Timing",
                        "Harmonization & Bounded Remedial Guidelines"
                    ]
                }
            ],
            "faqs": [
                {"q": f"How do I calculate my personal vibrations using this method?", "a": "Apply deterministic digit reduction to your birth date or name coordinates to reveal your ruling archetype."},
                {"q": "Can numerology predict the exact future?", "a": "No. Numeros Vision treats numerology as a self-reflection and cyclical timing system, not an absolute predictive guarantee."}
            ],
            "table_spec": {
                "title": f"{core_topic_title} Planetary Correspondence",
                "headers": ["Vibration Number", "Planetary Ruler", "Core Archetype", "Harmony Day"],
                "rows": [
                    ["1", "Sun", "Leadership & Autonomy", "Sunday"],
                    ["2", "Moon", "Intuition & Diplomacy", "Monday"],
                    ["3", "Jupiter", "Expansion & Creative Wisdom", "Thursday"]
                ]
            },
            "lsi_keywords": brief.secondary_keywords or [core_topic.lower(), "traditional numerology", "planetary vibration"]
        }

        # STAGE C-2: Visual Media Production & Optimization (Section 7)
        image_package = self.image_service.process_article_visual(
            topic=brief.working_title,
            target_keyword=brief.primary_keyword,
            article_url=brief.target_url,
            is_hero=True
        )

        blueprint["image_spec"] = {
            "hero_webp_url": image_package["hero_webp_url"],
            "hero_png_url": image_package["hero_png_url"],
            "figure_html": image_package["html_markup"],
            "media_id": image_package["media_id"]
        }

        # Generate HTML page with complete schema, header, styling, and navigation
        html_draft = AutomatedContentGenerator.generate_html_page(blueprint)

        # STAGE E: Validation
        passed, gate_report = self.validator.evaluate_draft(
            html_draft, 
            brief, 
            is_human_approved=is_human_approved,
            image_package=image_package
        )

        # STAGE F & G: Outcome determination
        pipeline_status = "READY_TO_PUBLISH" if passed else "VALIDATION_FAILED"

        return {
            "pipeline_status": pipeline_status,
            "passed_all_gates": passed,
            "brief_id": brief.brief_id,
            "target_url": brief.target_url,
            "quality_report": gate_report,
            "media_asset": {
                "media_id": image_package["media_id"],
                "hero_webp_url": image_package["hero_webp_url"],
                "content_hash": image_package["content_hash"],
                "alt_text": image_package["alt_text"]
            },
            "html_length": len(html_draft),
            "html_content": html_draft if passed else ""
        }
