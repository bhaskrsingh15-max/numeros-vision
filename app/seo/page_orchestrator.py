"""
app.seo.page_orchestrator
End-to-end automation orchestrator that coordinates:
1. Topic competitor SERP analysis
2. Anti-penalty white-hat guardrail validation
3. Automated HTML generation (with AEO snippet bait & rich Schema.org JSON-LD)
4. File deployment & sitemap.xml synchronization
5. Dynamic route activation
"""

import os
import re
from typing import Dict, Any, List
from .competitor_analyzer import CompetitorSERPAnalyzer
from .anti_penalty_guardrails import AntiPenaltyGuardrailValidator
from .content_generator import AutomatedContentGenerator

STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))

class SEOPageOrchestrator:
    """End-to-end automation pipeline for creating and validating high-ranking pages."""

    @classmethod
    def publish_new_topic(cls, topic: str, target_keyword: str = "", category: str = "blog") -> Dict[str, Any]:
        """
        Orchestrates full workflow:
        Analyzes SERP -> Checks Anti-Penalty -> Generates HTML -> Saves File -> Updates Sitemap.
        """
        # 1. Competitor SERP Analysis
        blueprint = CompetitorSERPAnalyzer.analyze_topic(topic, target_keyword)
        slug = blueprint["slug"]

        # 2. Generate Content
        html_content = AutomatedContentGenerator.generate_html_page(blueprint)

        # 3. Anti-Penalty Validation
        is_compliant, issues, metrics = AntiPenaltyGuardrailValidator.validate_page_html(
            html_content, blueprint["target_keyword"]
        )

        if not is_compliant:
            return {
                "success": False,
                "error": "Failed Anti-Penalty Validation",
                "violations": issues,
                "metrics": metrics
            }

        # 4. Save to static folder
        target_dir = os.path.join(STATIC_DIR, category)
        os.makedirs(target_dir, exist_ok=True)
        filename = f"{slug}.html"
        file_path = os.path.join(target_dir, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        # 5. Sync with Sitemap
        page_url = f"https://numerosvision.com/{category}/{slug}"
        cls._add_to_sitemap(page_url)

        return {
            "success": True,
            "topic": topic,
            "slug": slug,
            "url": page_url,
            "file_path": file_path,
            "meta_title": blueprint["meta_title"],
            "meta_description": blueprint["meta_description"],
            "word_count": metrics.get("total_words", 0),
            "keyword_density": f"{metrics.get('keyword_density', 0)}%",
            "schemas_active": ["Article", "FAQPage", "BreadcrumbList"],
            "guardrail_status": "100% White-Hat Compliant",
            "warnings": [i for i in issues if "WARNING" in i]
        }

    @classmethod
    def _add_to_sitemap(cls, page_url: str):
        """Appends new page URL to sitemap.xml if not already present."""
        sitemap_path = os.path.join(STATIC_DIR, "sitemap.xml")
        if not os.path.exists(sitemap_path):
            return

        with open(sitemap_path, "r", encoding="utf-8") as f:
            content = f.read()

        if f"<loc>{page_url}</loc>" in content:
            return  # Already exists

        new_entry = f"""  <url>
    <loc>{page_url}</loc>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>"""

        if "</urlset>" in content:
            updated_content = content.replace("</urlset>", new_entry)
            with open(sitemap_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
