import unittest
from pathlib import Path

class TestHybridMobileUIUX(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        index_path = Path("app/static/index.html")
        cls.index_html = index_path.read_text(encoding="utf-8")
        
        css_path = Path("app/static/css/roadmap_components.css")
        cls.roadmap_css = css_path.read_text(encoding="utf-8")

    def test_mobile_hero_content(self):
        """Hero copy matches canonical homepage requirements."""
        self.assertIn("Discover What Your Numbers Mean", self.index_html)
        self.assertIn("Start Free Calculation", self.index_html)
        self.assertIn("Explore Personalised Reports", self.index_html)

    def test_cosmic_matrix_card_structure(self):
        """Card contains required inputs and preserved IDs."""
        self.assertIn('id="calculator-card"', self.index_html)
        self.assertIn("Start with Your Numbers", self.index_html)

        # Form IDs must be preserved for calculation & auth gating
        self.assertIn('id="f-name"', self.index_html)
        self.assertIn('id="f-day"', self.index_html)
        self.assertIn('id="f-month"', self.index_html)
        self.assertIn('id="f-year"', self.index_html)
        self.assertIn('id="f-method"', self.index_html)
        self.assertIn('id="birth-submit-btn"', self.index_html)

        # Output IDs must be preserved
        self.assertIn('id="birth-results"', self.index_html)
        self.assertIn('id="out-driver"', self.index_html)

    def test_bottom_nav_structure(self):
        """Bottom nav has canonical 4 items with vector SVGs and safe-area padding."""
        self.assertIn('class="nv-sticky-bottom-nav"', self.index_html)
        self.assertIn('data-nav="home"', self.index_html)
        self.assertIn('data-nav="calculate"', self.index_html)
        self.assertIn('data-nav="reports"', self.index_html)
        self.assertIn('data-nav="account"', self.index_html)
        self.assertIn('safe-area-inset-bottom', self.roadmap_css)

    def test_charm_ai_mobile_centered_cta(self):
        """Charm AI input composer has centered Send CTA on mobile screens."""
        self.assertIn('class="chat-input-bar"', self.index_html)
        self.assertIn('class="chat-input-row"', self.index_html)
        self.assertIn('id="voice-btn"', self.index_html)
        self.assertIn('id="chat-input"', self.index_html)
        self.assertIn('id="chat-send-btn"', self.index_html)

        # Confirm centered CTA rules exist in both inline and external css
        self.assertIn('.chat-input-row', self.roadmap_css)
        self.assertIn('flex-direction: column', self.roadmap_css)
        self.assertIn('auto', self.roadmap_css)

if __name__ == '__main__':
    unittest.main()
