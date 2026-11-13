"""
app.seo.images.image_service
High-Level Image Production, Optimization, and Registration Service.

Orchestrates Sections 7.1, 7.2, and 7.5 of the Master Addendum:
- Evaluates image need per article topic
- Deterministic diagram generation
- Responsive optimization and WebP compression
- Media registry recording and provenance tracking
- Generates accessible HTML figure embed codes
"""

import os
import re
import logging
from typing import Dict, Any, List, Optional
from app.seo.images.diagram_renderer import DeterministicDiagramRenderer
from app.seo.images.image_optimizer import ImageOptimizer
from app.seo.images.media_registry import MediaRegistry

logger = logging.getLogger("image_service")

class ImageService:
    """End-to-end service for automated, deterministic, and optimized visual content production."""

    def __init__(self, output_dir: Optional[str] = None):
        if output_dir:
            self.output_dir = output_dir
        else:
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "static", "images", "seo"))
            self.output_dir = base_dir
        self.registry = MediaRegistry()

    def process_article_visual(
        self,
        topic: str,
        target_keyword: str,
        article_url: str,
        custom_alt_text: Optional[str] = None,
        is_hero: bool = True
    ) -> Dict[str, Any]:
        """
        Determines the appropriate deterministic diagram for an article,
        renders it, optimizes it into responsive WebP/PNG variants,
        and registers the asset with full provenance.
        """
        topic_lower = (topic + " " + target_keyword).lower()

        # 1. Deterministic Selection Workflow (Section 7.1)
        if "lo shu" in topic_lower or "magic square" in topic_lower or "grid" in topic_lower:
            diagram = DeterministicDiagramRenderer.render_lo_shu_grid(
                title=f"Lo Shu Grid Analysis: {target_keyword.title()}",
                subtitle="Traditional 3x3 Planetary Energy Planes & Numbers Matrix"
            )
            base_slug = f"lo-shu-grid-{re.sub(r'[^a-z0-9]+', '-', target_keyword.lower()).strip('-')}"
            purpose = "EXPLANATORY_DIAGRAM"
            alt_text = custom_alt_text or f"Lo Shu 3x3 Magic Square showing planetary energetic planes and numbers for {target_keyword}."
            caption = f"Figure: Deterministic 3x3 Lo Shu Energy Matrix and Planes for {target_keyword.title()}."

        elif "chaldean" in topic_lower or "alphabet" in topic_lower or "sound" in topic_lower or "name" in topic_lower:
            diagram = DeterministicDiagramRenderer.render_chaldean_sound_matrix(
                title=f"Chaldean Vibration Matrix: {target_keyword.title()}",
                subtitle="Canonical 1-8 Sound Numbers & Alphabetical Resonance"
            )
            base_slug = f"chaldean-sound-matrix-{re.sub(r'[^a-z0-9]+', '-', target_keyword.lower()).strip('-')}"
            purpose = "DATA_CHART"
            alt_text = custom_alt_text or f"Chaldean numerology sound and vibration matrix with numbers 1 to 8 and planetary rulers for {target_keyword}."
            caption = f"Figure: Canonical Chaldean 1 to 8 Sound Matrix and Letter Correspondences."

        elif "compound" in topic_lower or any(f"number {n}" in topic_lower for n in range(10, 100)):
            # Extract number if present
            num_match = re.search(r"\b(\d{2})\b", topic_lower)
            comp_num = int(num_match.group(1)) if num_match else 24
            root_num = (comp_num - 1) % 9 + 1
            diagram = DeterministicDiagramRenderer.render_compound_seal(
                compound_num=comp_num,
                root_num=root_num,
                title=f"Compound Vibration {comp_num}",
                archetype="Harmonic Synthesis",
                keywords=["Integrity", "Astral Equilibrium", "Leadership"]
            )
            base_slug = f"compound-number-{comp_num}-esoteric-seal"
            purpose = "EDUCATIONAL_ILLUSTRATION"
            alt_text = custom_alt_text or f"Esoteric seal for compound number {comp_num} reducing to root vibration {root_num}."
            caption = f"Figure: Esoteric Compound Seal for Number {comp_num} (Root {root_num})."

        else:
            # General numerology diagram (Planetary / Lo Shu)
            diagram = DeterministicDiagramRenderer.render_lo_shu_grid(
                title=f"Numeros Vision Planetary Matrix: {target_keyword.title()}",
                subtitle="Deterministic Traditional Numerology Framework"
            )
            base_slug = f"numerology-matrix-{re.sub(r'[^a-z0-9]+', '-', target_keyword.lower()).strip('-')}"
            purpose = "EXPLANATORY_DIAGRAM"
            alt_text = custom_alt_text or f"Numerology matrix and vibrational correspondence diagram for {target_keyword}."
            caption = f"Figure: Core Vibrational Correspondences for {target_keyword.title()}."

        # 2. Performance Optimization & Responsive Generation (Section 7.5)
        opt_result = ImageOptimizer.optimize_and_save_variants(
            image_bytes=diagram["webp_bytes"],
            seo_base_slug=base_slug,
            output_dir=self.output_dir,
            alt_text=alt_text,
            caption=caption,
            is_hero=is_hero
        )

        media_id = f"img_{base_slug}_{opt_result['content_hash'][:10]}"

        # 3. Registration in Media Registry (Section 7.3)
        registered_entry = self.registry.register_asset(
            media_id=media_id,
            seo_filename=opt_result["variants"]["hero"]["webp"]["filename"],
            image_purpose=purpose,
            associated_article_url=article_url,
            alt_text=alt_text,
            provenance="DETERMINISTIC_RENDERER",
            dimensions=opt_result["dimensions"],
            formats=["webp", "png"],
            content_hash=opt_result["content_hash"],
            published_variants=opt_result["variants"],
            caption=caption,
            credit="Numeros Vision Deterministic System",
            accessibility_reviewed=opt_result["alt_text_valid"]
        )

        return {
            "media_id": media_id,
            "status": "GENERATED_AND_REGISTERED",
            "diagram_type": diagram["diagram_type"],
            "image_purpose": purpose,
            "alt_text": alt_text,
            "alt_text_valid": opt_result["alt_text_valid"],
            "alt_text_issues": opt_result["alt_text_issues"],
            "budget_warnings": opt_result["budget_warnings"],
            "html_markup": opt_result["html_markup"],
            "hero_webp_url": opt_result["variants"]["hero"]["webp"]["rel_path"],
            "hero_png_url": opt_result["variants"]["hero"]["png"]["rel_path"],
            "content_hash": opt_result["content_hash"],
            "registry_entry": registered_entry
        }
