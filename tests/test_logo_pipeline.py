"""
Unit tests for Google Nano Banana Logo Pipeline:
- GoogleImageProvider adapter & circuit breakers
- VectorRenderer pure SVG generation
- LogoValidator independent multi-gate validation
"""

import unittest
from app.services.image_provider import GoogleImageProvider, ImageGenerationRequest
from app.services.vector_renderer import VectorRenderer
from app.services.logo_validator import LogoValidator, calculate_contrast_ratio, hex_to_rgb


class TestLogoPipeline(unittest.TestCase):
    def setUp(self):
        self.provider = GoogleImageProvider(mock_mode=True, max_daily_budget_usd=1.00)

    def test_image_provider_mock_generation(self):
        """Image provider generates valid PNG bytes, sets metadata, and accounts for cost."""
        req = ImageGenerationRequest(
            job_id="test_job_001",
            prompt="Professional logo for AURA PEAK",
            output_count=1,
        )
        result = self.provider.generate_image(req)
        self.assertEqual(result.provider, "mock")
        self.assertEqual(result.model_id, "imagen-3.0-generate-002")
        self.assertEqual(len(result.outputs), 1)
        self.assertEqual(result.outputs[0].mime_type, "image/png")
        self.assertGreater(len(result.outputs[0].image_bytes), 500)
        self.assertEqual(result.estimated_cost_cents, 3)

    def test_image_provider_budget_circuit_breaker(self):
        """Provider raises RuntimeError when daily budget limit is reached."""
        small_budget_provider = GoogleImageProvider(mock_mode=True, max_daily_budget_usd=0.05)
        # 1 image = 3 cents (allowed)
        req = ImageGenerationRequest(job_id="job_1", prompt="Logo 1", output_count=1)
        small_budget_provider.generate_image(req)
        # 2nd image = 3 cents -> cumulative 6 cents > 5 cents budget -> must raise!
        with self.assertRaises(RuntimeError) as ctx:
            small_budget_provider.generate_image(req)
        self.assertIn("BUDGET_EXHAUSTED", str(ctx.exception))

    def test_vector_renderer_pure_svg_output(self):
        """VectorRenderer produces pure, valid SVG markup containing exact wordmark."""
        svg = VectorRenderer.render_svg(
            exact_wordmark="AURA PEAK",
            symbol_type="ascending_peak",
            primary_hex="#C9A227",
            variant="horizontal_lockup",
        )
        self.assertTrue(svg.startswith("<svg"))
        self.assertTrue(svg.endswith("</svg>"))
        self.assertIn("AURA PEAK", svg)
        self.assertIn("viewBox=\"0 0 1200 400\"", svg)
        self.assertNotIn(".png", svg.lower())  # Never rename raster!

    def test_logo_validator_svg_gate_pass(self):
        """LogoValidator confirms valid SVG with exact wordmark and contrast."""
        svg = VectorRenderer.render_svg(
            exact_wordmark="KINETIC STEP",
            symbol_type="geometric_star",
            primary_hex="#523E28",
            bg_hex="#FFFDF7",
            variant="stacked_lockup",
        )
        validation = LogoValidator.validate_svg(
            svg_content=svg,
            expected_wordmark="KINETIC STEP",
            target_palette_hex=["#523E28", "#FFFDF7"],
            require_contrast=4.5,
        )
        self.assertTrue(validation["passed"])
        self.assertTrue(validation["ocr_wordmark_match"])
        self.assertGreater(validation["contrast_ratio"], 4.5)

    def test_logo_validator_svg_gate_mismatched_wordmark(self):
        """LogoValidator detects misspelled or missing wordmark in SVG."""
        svg = VectorRenderer.render_svg(
            exact_wordmark="DIFFERENT NAME",
            symbol_type="geometric_star",
        )
        validation = LogoValidator.validate_svg(
            svg_content=svg,
            expected_wordmark="EXPECTED BRAND",
            target_palette_hex=["#C9A227"],
        )
        self.assertFalse(validation["passed"])
        self.assertFalse(validation["ocr_wordmark_match"])
        self.assertIn("Wordmark verification failed", validation["errors"][0])

    def test_wcag_contrast_formula(self):
        """Calculates WCAG 2.1 contrast ratio accurately (black on white = 21:1)."""
        black = hex_to_rgb("#000000")
        white = hex_to_rgb("#FFFFFF")
        ratio = calculate_contrast_ratio(black, white)
        self.assertAlmostEqual(ratio, 21.0, places=1)


if __name__ == "__main__":
    unittest.main()
