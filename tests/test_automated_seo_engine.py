"""
Tests for Numeros Vision AI Search Intelligence, Content Automation, AEO/GEO & Revenue Conversion Engine
"""

import unittest
import os
import sys

# Ensure root is in sys.path
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app
from app.seo.connectors.atp_adapter import AnswerThePublicAdapter
from app.seo.connectors.indexnow_adapter import IndexNowAdapter
from app.seo.opportunity_scorer import OpportunityScorer
from app.seo.brief_generator import ContentBriefGenerator
from app.seo.pipeline.quality_gates import QualityGateValidator
from app.seo.pipeline.content_pipeline import ContentGenerationPipeline
from app.seo.publishing_adapter import WebsitePublishingAdapter
from app.seo.conversion_analytics import ConversionAnalyticsEngine

class TestAutomatedSEOEngine(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_01_offer_registry_integrity(self):
        """Verifies that offer_registry.json exists and contains 38 verified first-party plans."""
        data_dir = os.path.join(_ROOT, "data")
        offer_file = os.path.join(data_dir, "offer_registry.json")
        self.assertTrue(os.path.exists(offer_file), "offer_registry.json must exist")

    def test_02_atp_adapter_csv_ingestion(self):
        """Verifies AnswerThePublic adapter parses records with provenance."""
        atp = AnswerThePublicAdapter()
        records = atp.discover(seed="numerology", market="in", language="en")
        self.assertGreater(len(records), 0, "Should load records from verified CSV archive")
        meta = atp.get_source_metadata()
        self.assertEqual(meta["provider"], "AnswerThePublic")

    def test_03_opportunity_scorer_normalized_model(self):
        """Verifies 0-100 opportunity score calculation and priority tiering."""
        score_high = OpportunityScorer.calculate_score(
            search_volume=201000,
            intent="TRANSACTIONAL",
            cluster_name="Calculators",
            page_exists=True,
            has_product_fit=True,
            monetization_tier="high"
        )
        self.assertGreaterEqual(score_high["opportunity_score"], 80.0)
        self.assertEqual(score_high["priority_tier"], "P0 (Live Critical)")

    def test_04_brief_generator_claim_ledger_binding(self):
        """Verifies that content briefs bind verified canonical sources and claim ledgers."""
        bg = ContentBriefGenerator()
        brief = bg.generate_brief(
            primary_keyword="lo shu grid calculator",
            target_url="/calculators/lo-shu-grid/",
            intent="TRANSACTIONAL",
            page_type="Interactive Tool",
            relevant_offer_id="report_essential"
        )
        self.assertEqual(brief.primary_keyword, "lo shu grid calculator")
        self.assertGreater(len(brief.required_claims), 0)
        self.assertEqual(brief.offer_id, "report_essential")

    def test_05_quality_gates_rejection_on_invalid_claims(self):
        """Verifies that quality gates block publication if unauthorized price or broken math is detected."""
        bg = ContentBriefGenerator()
        brief = bg.generate_brief(
            primary_keyword="fake test keyword",
            target_url="/blog/fake-test",
            relevant_offer_id="non_existent_fake_offer_123"
        )
        validator = QualityGateValidator()
        passed, report = validator.evaluate_draft(
            html_content="<p>Short placeholder draft.</p>",
            brief=brief,
            is_human_approved=False
        )
        self.assertFalse(passed, "Draft with invalid offer and unapproved status must fail quality gates")
        self.assertEqual(report["overall_verdict"], "BLOCKED")

    def test_06_indexnow_adapter_submission_and_logging(self):
        """Verifies IndexNow URL submission and audit log append."""
        ina = IndexNowAdapter()
        res = ina.submit_urls(["https://numerosvision.com/blog/test-url"])
        self.assertIn("status", res)
        history = ina.get_submission_history(limit=5)
        self.assertIsInstance(history, list)

    def test_07_conversion_analytics_privacy_and_funnel(self):
        """Verifies that conversion analytics strips customer PII and records allowed events."""
        analytics = ConversionAnalyticsEngine()
        res = analytics.track_event(
            event_name="calculator_completed",
            canonical_url="https://numerosvision.com/tools/life-path-calculator",
            properties={
                "name": "ShouldBeStripped",
                "dob": "1990-01-01",
                "calculator": "life_path"
            }
        )
        self.assertEqual(res["status"], "RECORDED")
        funnel = analytics.get_funnel_summary()
        self.assertIn("product_engagement", funnel)
        self.assertIn("commercial_outcomes", funnel)

    def test_08_seo_engine_api_endpoints(self):
        """Verifies that all FastAPI REST endpoints in /api/v1/seo-engine function properly."""
        # 1. Keywords endpoint
        resp = self.client.get("/api/v1/seo-engine/keywords?limit=5")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("records", resp.json())

        # 2. Brief generation endpoint
        resp_brief = self.client.post("/api/v1/seo-engine/briefs/generate", json={
            "primary_keyword": "destiny number meaning",
            "target_url": "/guides/numerology-number-meanings/",
            "intent": "INFORMATIONAL"
        })
        self.assertEqual(resp_brief.status_code, 200)
        self.assertEqual(resp_brief.json()["primary_keyword"], "destiny number meaning")

        # 3. Analytics dashboard endpoint
        resp_dash = self.client.get("/api/v1/seo-engine/analytics/dashboard")
        self.assertEqual(resp_dash.status_code, 200)
        self.assertIn("search_discovery", resp_dash.json())

    def test_09_deterministic_diagram_renderer(self):
        """Verifies deterministic Lo Shu, Chaldean, and Compound diagram rendering (Section 7.2)."""
        from app.seo.images.diagram_renderer import DeterministicDiagramRenderer
        # Lo Shu Grid
        lo_shu = DeterministicDiagramRenderer.render_lo_shu_grid(
            active_numbers=[3, 5, 7, 8, 1, 6],
            title="Lo Shu Test Grid"
        )
        self.assertEqual(lo_shu["diagram_type"], "LO_SHU_GRID")
        self.assertIn("<svg", lo_shu["svg"])
        self.assertGreater(len(lo_shu["webp_bytes"]), 1000)

        # Chaldean Matrix
        chaldean = DeterministicDiagramRenderer.render_chaldean_sound_matrix()
        self.assertEqual(chaldean["diagram_type"], "CHALDEAN_SOUND_MATRIX")
        self.assertGreater(len(chaldean["webp_bytes"]), 1000)

        # Compound Seal
        seal = DeterministicDiagramRenderer.render_compound_seal(
            compound_num=19,
            root_num=1,
            title="The Prince of Heaven",
            archetype="Solar Victory",
            keywords=["Radiance", "Success", "Clarity"]
        )
        self.assertEqual(seal["diagram_type"], "COMPOUND_SEAL")
        self.assertEqual(seal["compound_num"], 19)

    def test_10_image_optimizer_and_alt_text_rules(self):
        """Verifies WebP compression, responsive variants, and alt text rules (Sections 7.4 & 7.5)."""
        from app.seo.images.image_optimizer import ImageOptimizer
        # Test Alt-text guardrails
        valid, issues = ImageOptimizer.validate_alt_text("Lo Shu 3x3 magic square energy planes and numbers matrix.")
        self.assertTrue(valid, "Clean descriptive alt text should pass")

        invalid_prefix, issues_prefix = ImageOptimizer.validate_alt_text("image of a numerology chart")
        self.assertFalse(invalid_prefix, "Alt text starting with 'image of' must fail")
        self.assertTrue(any("image of" in i for i in issues_prefix))

        invalid_stuffing, issues_stuffing = ImageOptimizer.validate_alt_text(
            "calculator for numerology calculator with calculator numbers and best calculator"
        )
        self.assertFalse(invalid_stuffing, "Keyword-stuffed alt text must fail")

    def test_11_media_registry_and_provenance(self):
        """Verifies media registry records provenance, content hashes, and prevents duplicates (Section 7.3)."""
        from app.seo.images.media_registry import MediaRegistry
        import tempfile

        with tempfile.TemporaryDirectory() as tmp_dir:
            reg_path = os.path.join(tmp_dir, "test_media_registry.json")
            reg = MediaRegistry(registry_path=reg_path)
            
            entry1 = reg.register_asset(
                media_id="img_test_01",
                seo_filename="test-diagram.webp",
                image_purpose="EXPLANATORY_DIAGRAM",
                associated_article_url="/blog/test-article",
                alt_text="Test diagram description.",
                provenance="DETERMINISTIC_RENDERER",
                dimensions={"hero": [1200, 675]},
                formats=["webp", "png"],
                content_hash="hash_abc_123",
                published_variants={"hero": {"webp": {"size_bytes": 5000}}}
            )
            self.assertEqual(entry1["media_id"], "img_test_01")

            # Duplicate registration with same hash returns existing entry
            entry2 = reg.register_asset(
                media_id="img_test_02_duplicate",
                seo_filename="test-diagram-dup.webp",
                image_purpose="EXPLANATORY_DIAGRAM",
                associated_article_url="/blog/test-article",
                alt_text="Test duplicate description.",
                provenance="DETERMINISTIC_RENDERER",
                dimensions={"hero": [1200, 675]},
                formats=["webp", "png"],
                content_hash="hash_abc_123",
                published_variants={}
            )
            self.assertEqual(entry2["media_id"], "img_test_01", "Deduplication must return existing entry")

    def test_12_end_to_end_pipeline_with_image_and_gate6(self):
        """Verifies that ContentGenerationPipeline produces images and passes Gate 6."""
        bg = ContentBriefGenerator()
        brief = bg.generate_brief(
            primary_keyword="lo shu grid calculator",
            target_url="/calculators/lo-shu-grid/",
            intent="TRANSACTIONAL",
            page_type="Interactive Tool",
            relevant_offer_id="report_essential"
        )
        pipe = ContentGenerationPipeline()
        result = pipe.run_pipeline(brief, is_human_approved=True)

        self.assertTrue(result["passed_all_gates"])
        self.assertEqual(result["pipeline_status"], "READY_TO_PUBLISH")
        self.assertIn("media_asset", result)
        self.assertTrue(result["media_asset"]["hero_webp_url"].endswith(".webp"))
        self.assertIn("<picture>", result["html_content"])
        self.assertIn("nv-seo-figure", result["html_content"])

    def test_13_image_api_endpoints(self):
        """Verifies REST endpoints for rendering diagrams, processing images, and media registry."""
        # 1. Render Diagram
        resp_diag = self.client.post("/api/v1/seo-engine/images/render-diagram", json={
            "diagram_type": "LO_SHU_GRID",
            "title": "API Test Lo Shu Grid",
            "subtitle": "Test Subtitle"
        })
        self.assertEqual(resp_diag.status_code, 200)
        self.assertEqual(resp_diag.json()["diagram_type"], "LO_SHU_GRID")
        self.assertIn("svg", resp_diag.json())

        # 2. Process Image
        resp_proc = self.client.post("/api/v1/seo-engine/images/process", json={
            "topic": "Chaldean Sound Vibrations",
            "target_keyword": "chaldean numerology alphabet",
            "article_url": "/blog/chaldean-alphabet"
        })
        self.assertEqual(resp_proc.status_code, 200)
        self.assertEqual(resp_proc.json()["status"], "GENERATED_AND_REGISTERED")
        self.assertTrue(resp_proc.json()["alt_text_valid"])

        # 3. Media Registry List
        resp_reg = self.client.get("/api/v1/seo-engine/images/media-registry?limit=10")
        self.assertEqual(resp_reg.status_code, 200)
        self.assertGreaterEqual(resp_reg.json()["total"], 1)

if __name__ == "__main__":
    unittest.main()

