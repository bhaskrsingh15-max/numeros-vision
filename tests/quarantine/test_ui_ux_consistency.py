import unittest
import glob
import os

class TestUIUXConsistency(unittest.TestCase):
    def setUp(self):
        self.files = [f for f in glob.glob('app/static/**/*.html', recursive=True) if 'amp' not in f]

    def test_all_pages_have_master_header(self):
        missing = []
        for fpath in self.files:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if 'class="nv-header"' not in content and "class='nv-header'" not in content:
                missing.append(fpath)
        self.assertEqual(len(missing), 0, f"Pages missing nv-header: {missing}")

    def test_all_pages_have_master_footer(self):
        missing = []
        for fpath in self.files:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if 'class="nv-footer"' not in content and "class='nv-footer'" not in content:
                missing.append(fpath)
        self.assertEqual(len(missing), 0, f"Pages missing nv-footer: {missing}")

    def test_all_pages_have_roadmap_components_css(self):
        missing = []
        for fpath in self.files:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if 'roadmap_components.css' not in content:
                missing.append(fpath)
        self.assertEqual(len(missing), 0, f"Pages missing roadmap_components.css: {missing}")

    def test_all_pages_have_canonical_logo(self):
        missing = []
        for fpath in self.files:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if 'nv-logo-mark.svg' not in content:
                missing.append(fpath)
        self.assertEqual(len(missing), 0, f"Pages missing nv-logo-mark.svg: {missing}")

    def test_all_pages_have_correct_brand_text(self):
        missing = []
        for fpath in self.files:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if 'NUMEROS VISION' not in content or 'ANVEIL EVERY CHARM' not in content:
                missing.append(fpath)
        self.assertEqual(len(missing), 0, f"Pages missing NUMEROS VISION or ANVEIL EVERY CHARM: {missing}")

    def test_no_statutory_disclaimer_in_any_page(self):
        violations = []
        for fpath in self.files:
            with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            if 'Statutory Ethical Disclaimer: Numeros Vision interpretations' in content or 'nv-footer-disclaimer-box' in content:
                violations.append(fpath)
        self.assertEqual(len(violations), 0, f"Pages still containing statutory disclaimer box: {violations}")

    def test_canonical_container_spacing_in_theme_css(self):
        with open('app/static/css/theme.css', 'r', encoding='utf-8', errors='ignore') as f:
            css = f.read()
        self.assertIn('--nv-container-max: 1240px', css)
        self.assertIn('--nv-container-reading: 880px', css)
        self.assertIn('--nv-container-pad: clamp(16px, 3.5vw, 24px)', css)
        self.assertIn('--nv-section-py: clamp(48px, 6vw, 76px)', css)
        self.assertIn('max-width: var(--nv-container-max, 1240px) !important;', css)

if __name__ == '__main__':
    unittest.main()
