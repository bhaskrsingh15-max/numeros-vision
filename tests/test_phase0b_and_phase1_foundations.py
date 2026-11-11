import os
import re
import unittest
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(ROOT, "dist_cloudflare_pages")
STATIC_DIR = os.path.join(ROOT, "app", "static")


class TestPhase0BAndPhase1Foundations(unittest.TestCase):
    """End-to-end verification of Phase 0B reconciliation and Phase 1 SEO/platform foundations."""

    def test_01_sitemap_index_and_all_child_urls_resolve_to_200_indexable_dist_files(self):
        idx_path = os.path.join(DIST_DIR, "sitemap.xml")
        self.assertTrue(os.path.exists(idx_path), "dist_cloudflare_pages/sitemap.xml missing")
        tree = ET.parse(idx_path)
        root = tree.getroot()
        self.assertTrue(root.tag.endswith("sitemapindex"), f"Expected <sitemapindex>, got {root.tag}")

        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        child_locs = [el.text.strip() for el in root.findall("sm:sitemap/sm:loc", ns)]
        self.assertEqual(
            child_locs,
            [
                "https://numerosvision.com/sitemap-calculators.xml",
                "https://numerosvision.com/sitemap-numbers.xml",
                "https://numerosvision.com/sitemap-2027.xml",
                "https://numerosvision.com/sitemap-reports.xml",
                "https://numerosvision.com/sitemap-blog.xml",
            ],
        )

        seen_urls = set()
        for child_url in child_locs:
            fname = child_url.split("/")[-1]
            cpath = os.path.join(DIST_DIR, fname)
            self.assertTrue(os.path.exists(cpath), f"Missing child sitemap in dist: {fname}")
            ctree = ET.parse(cpath)
            urls = [el.text.strip() for el in ctree.getroot().findall("sm:url/sm:loc", ns)]
            self.assertGreater(len(urls), 0, f"Empty child sitemap: {fname}")
            for u in urls:
                self.assertNotIn(u, seen_urls, f"Duplicate URL across child sitemaps: {u}")
                seen_urls.add(u)
                self.assertTrue(u.startswith("https://numerosvision.com/"))
                rel = u.replace("https://numerosvision.com/", "").strip("/")
                phys = os.path.join(DIST_DIR, "index.html") if not rel else os.path.join(DIST_DIR, *rel.split("/"), "index.html")
                self.assertTrue(os.path.exists(phys), f"Sitemap URL {u} has no physical 200 OK file at {phys}")
                with open(phys, "r", encoding="utf-8") as f:
                    html = f.read()
                self.assertIsNone(
                    re.search(r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex', html, re.I),
                    f"Sitemap URL {u} points to a noindex page!",
                )

    def test_02_charm_ai_public_overview_vs_noindex_chat_split(self):
        ov_path = os.path.join(DIST_DIR, "charm-ai", "index.html")
        chat_path = os.path.join(DIST_DIR, "charm-ai", "chat", "index.html")
        self.assertTrue(os.path.exists(ov_path))
        self.assertTrue(os.path.exists(chat_path))

        with open(ov_path, "r", encoding="utf-8") as f:
            ov_html = f.read()
        with open(chat_path, "r", encoding="utf-8") as f:
            chat_html = f.read()

        self.assertIn('<link rel="canonical" href="https://numerosvision.com/charm-ai/" />', ov_html)
        self.assertNotIn("noindex", ov_html.lower())
        self.assertIn("/charm-ai/chat/", ov_html)

        self.assertIn('<meta name="robots" content="noindex, nofollow" />', chat_html)
        self.assertNotIn('rel="canonical"', chat_html)

        with open(os.path.join(DIST_DIR, "robots.txt"), "r", encoding="utf-8") as f:
            robots = f.read()
        self.assertIn("Disallow: /charm-ai/chat/", robots)

    def test_03_og_default_1200x630_png_dimensions_and_zero_black(self):
        og_path = os.path.join(DIST_DIR, "assets", "brand", "og-default-1200x630.png")
        self.assertTrue(os.path.exists(og_path))
        self.assertLessEqual(os.path.getsize(og_path), 150 * 1024)
        with Image.open(og_path) as im:
            self.assertEqual(im.format, "PNG")
            self.assertEqual(im.size, (1200, 630))
            rgb = im.convert("RGB")
            extrema = rgb.getextrema()
            # Ensure zero pure #000000 pixel
            raw_bytes = rgb.tobytes()
            has_pure_black = any(
                raw_bytes[i] == 0 and raw_bytes[i + 1] == 0 and raw_bytes[i + 2] == 0
                for i in range(0, len(raw_bytes), 3)
            )
            self.assertFalse(has_pure_black, f"Found pure #000000 pixel in og-default-1200x630.png (extrema={extrema})")

    def test_04_repo_wide_zero_anviel_zero_bhaskar_zero_poppins_and_sw_asset_only(self):
        for scan_dir in (os.path.join(ROOT, "app"), os.path.join(ROOT, "pdf_service")):
            for dp, _, fns in os.walk(scan_dir):
                for fn in fns:
                    if fn.lower().endswith((".html", ".js", ".css", ".py", ".json", ".ts", ".txt", ".xml")):
                        fp = os.path.join(dp, fn)
                        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                            txt = f.read()
                        self.assertNotIn("ANVIEL", txt.upper(), f"Found legacy typo ANVIEL in {fp}")
                        self.assertNotIn("bhaskar", txt.lower(), f"Found legacy spelling Bhaskar in {fp}")

        with open(os.path.join(STATIC_DIR, "css", "theme.css"), "r", encoding="utf-8") as f:
            theme_css = f.read()
        self.assertNotIn("poppins", theme_css.lower())
        self.assertNotIn("dm+sans", theme_css.lower())

        with open(os.path.join(DIST_DIR, "sw.js"), "r", encoding="utf-8") as f:
            sw_txt = f.read()
        m = re.search(r"const\s+APP_SHELL\s*=\s*\[(.*?)\];", sw_txt, re.S)
        self.assertIsNotNone(m)
        for entry in re.findall(r"'([^']+)'", m.group(1)):
            self.assertFalse(entry.endswith("/"), f"HTML route '{entry}' must not be cached in sw.js APP_SHELL")

    def test_05_high_to_low_report_card_order_and_zero_prototypes(self):
        self.assertFalse(os.path.exists(os.path.join(STATIC_DIR, "journey_prototype.html")))
        self.assertFalse(os.path.exists(os.path.join(STATIC_DIR, "google_email_avatar")))

        for page_rel in ("your-reading/index.html", "pricing/index.html", "reports_catalogue/index.html"):
            with open(os.path.join(DIST_DIR, *page_rel.split("/")), "r", encoding="utf-8") as f:
                txt = f.read()
            self.assertIn("Anveil every charm", txt)
            self.assertIn("Anveil my glowing charms", txt)
            self.assertIn("Anveil my alignments", txt)
            self.assertLess(
                txt.index("Anveil every charm"),
                txt.index("Anveil my glowing charms"),
                f"Expected High-to-Low order (1050 before 510) in {page_rel}",
            )
            self.assertLess(
                txt.index("Anveil my glowing charms"),
                txt.index("Anveil my alignments"),
                f"Expected High-to-Low order (510 before 199) in {page_rel}",
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
