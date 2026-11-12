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
                "https://numerosvision.com/sitemap-reports.xml",
                "https://numerosvision.com/sitemap-blog.xml",
            ],
        )
        self.assertFalse(
            os.path.exists(os.path.join(DIST_DIR, "sitemap-2027.xml")),
            "sitemap-2027.xml must remain excluded from dist until Planner disclaimer is approved",
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

        # Verify canonical /reports/ is in sitemap, while /cancel/, /year-2027/, and /reports_catalogue/ are excluded
        self.assertIn("https://numerosvision.com/reports/", seen_urls)
        self.assertNotIn("https://numerosvision.com/reports_catalogue/", seen_urls)
        self.assertNotIn("https://numerosvision.com/cancel/", seen_urls)
        self.assertNotIn("https://numerosvision.com/year-2027/", seen_urls)

        # Verify /cancel/ and /year-2027/ carry noindex meta directives
        for noidx_rel in ("cancel/index.html", "year-2027/index.html"):
            with open(os.path.join(DIST_DIR, *noidx_rel.split("/")), "r", encoding="utf-8") as f:
                nhtml = f.read()
            self.assertRegex(
                nhtml,
                r'<meta\s+name=["\']robots["\']\s+content=["\'][^"\']*noindex',
                f"Expected noindex meta tag on {noidx_rel}",
            )

        # Verify /dashboard/, /login/, /signup/ keep noindex meta tags AND have NO robots.txt Disallow
        with open(os.path.join(DIST_DIR, "robots.txt"), "r", encoding="utf-8") as f:
            robots_txt = f.read()
        for dropped_path, page_rel in [
            ("/dashboard/", "dashboard/index.html"),
            ("/login/", "login/index.html"),
            ("/signup/", "signup/index.html"),
        ]:
            self.assertNotIn(
                f"Disallow: {dropped_path}",
                robots_txt,
                f"robots.txt must not Disallow {dropped_path} until Search Console drops it",
            )
            with open(os.path.join(DIST_DIR, *page_rel.split("/")), "r", encoding="utf-8") as f:
                ahtml = f.read()
            self.assertIn('<meta name="robots" content="noindex, nofollow" />', ahtml)

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

    def test_04_repo_wide_zero_anviel_legal_vs_public_name_split_zero_poppins_and_sw_asset_only(self):
        legal_files_requiring_full_name = [
            os.path.join(STATIC_DIR, "privacy.html"),
            os.path.join(STATIC_DIR, "terms.html"),
            os.path.join(STATIC_DIR, "refund.html"),
            os.path.join(STATIC_DIR, "contact.html"),
            os.path.join(STATIC_DIR, "dashboard.html"),
            os.path.join(STATIC_DIR, "your-reading.html"),
            os.path.join(STATIC_DIR, "pricing.html"),
            os.path.join(STATIC_DIR, "js", "nv_consent.js"),
            os.path.join(STATIC_DIR, "_worker.js"),
            os.path.join(ROOT, "app", "api", "billing.py"),
            os.path.join(ROOT, "app", "services", "waitlist_service.py"),
        ]
        for lfp in legal_files_requiring_full_name:
            self.assertTrue(os.path.exists(lfp), f"Missing expected legal/compliance file: {lfp}")
            with open(lfp, "r", encoding="utf-8") as f:
                ltxt = f.read()
            self.assertIn(
                "Bhaskar Kumar Singh",
                ltxt,
                f"Expected legal/compliance identity 'Bhaskar Kumar Singh' in {lfp}",
            )

        for scan_dir in (os.path.join(ROOT, "app"), os.path.join(ROOT, "pdf_service")):
            for dp, _, fns in os.walk(scan_dir):
                for fn in fns:
                    if fn.lower().endswith((".html", ".js", ".css", ".py", ".json", ".ts", ".txt", ".xml")):
                        fp = os.path.join(dp, fn)
                        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                            txt = f.read()
                        self.assertNotIn("ANVIEL", txt.upper(), f"Found legacy typo ANVIEL in {fp}")
                        scrubbed = txt.replace("Bhaskar Kumar Singh", "")
                        self.assertNotIn(
                            "bhaskar",
                            scrubbed.lower(),
                            f"Found standalone legacy spelling 'Bhaskar' outside 'Bhaskar Kumar Singh' in {fp}",
                        )

        # Public numerologist surfaces must use 'Bhaskr Singh' and NOT expose alternateName on Person schema
        for pub_rel in ("index.html", "about/index.html", "llms.txt"):
            with open(os.path.join(DIST_DIR, *pub_rel.split("/")), "r", encoding="utf-8") as f:
                ptxt = f.read()
            self.assertIn("Bhaskr Singh", ptxt, f"Expected public numerologist name 'Bhaskr Singh' in {pub_rel}")
            self.assertNotIn("Bhaskar Kumar Singh", ptxt, f"Legal full name must not appear on public {pub_rel}")
            self.assertNotIn("alternateName", ptxt, f"Person schema must not include alternateName on {pub_rel}")

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
        deleted_prototypes = [
            "journey_prototype.html",
            "google_email_avatar/code.html",
            "google_email_avatar/screen.png",
            "google_email_avatar/stitch_ai_numerologist_chat_experience/code.html",
            "google_email_avatar/stitch_ai_numerologist_chat_experience/screen.png",
            "google_email_avatar/stitch_ai_numerologist_chat_experience_1/code.html",
            "google_email_avatar/stitch_ai_numerologist_chat_experience_1/screen.png",
            "google_email_avatar/stitch_ai_numerologist_chat_experience_2/code.html",
            "google_email_avatar/stitch_ai_numerologist_chat_experience_2/screen.png",
        ]
        for rel_proto in deleted_prototypes:
            self.assertFalse(os.path.exists(os.path.join(STATIC_DIR, *rel_proto.split("/"))))
            self.assertFalse(os.path.exists(os.path.join(DIST_DIR, *rel_proto.split("/"))))

        for scan_dir in (os.path.join(ROOT, "app"), DIST_DIR):
            for dp, _, fns in os.walk(scan_dir):
                for fn in fns:
                    if fn.lower().endswith((".html", ".js", ".css", ".py", ".json", ".xml", ".txt")):
                        fp = os.path.join(dp, fn)
                        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                            txt = f.read()
                        self.assertNotIn("journey_prototype", txt, f"Dangling reference to journey_prototype in {fp}")
                        self.assertNotIn("google_email_avatar", txt, f"Dangling reference to google_email_avatar in {fp}")
                        self.assertNotIn(
                            "stitch_ai_numerologist_chat_experience",
                            txt,
                            f"Dangling reference to stitch prototype in {fp}",
                        )

        for page_rel in ("your-reading/index.html", "pricing/index.html", "reports/index.html"):
            with open(os.path.join(DIST_DIR, *page_rel.split("/")), "r", encoding="utf-8") as f:
                txt = f.read()
            body_txt = txt[txt.index("<body"):]
            self.assertIn("Anveil every charm", body_txt)
            self.assertIn("Anveil my glowing charms", body_txt)
            self.assertIn("Anveil my alignments", body_txt)
            self.assertIn("Coming soon, notify me", body_txt)
            self.assertNotIn("Waitlist members get the launch price for 7 days when it opens", txt)
            self.assertLess(
                body_txt.index("Anveil every charm"),
                body_txt.index("Anveil my glowing charms"),
                f"Expected High-to-Low order (32p before 12p) in {page_rel}",
            )
            self.assertLess(
                body_txt.index("Anveil my glowing charms"),
                body_txt.index("Anveil my alignments"),
                f"Expected High-to-Low order (12p before 3p) in {page_rel}",
            )

    def test_06_launch_offer_env_only_single_source_and_waitlist_masking(self):
        from unittest.mock import patch
        from app.config.pricing_config import (
            LAUNCH_OFFER_ENDS_AT_DEFAULT,
            LAUNCH_OFFER_STARTED_AT_DEFAULT,
            WAITLIST_DISPLAY_LABEL,
            format_launch_offer_copy,
            resolve_launch_offer_state,
            resolve_sku_price,
        )

        self.assertIsNone(LAUNCH_OFFER_STARTED_AT_DEFAULT)
        self.assertIsNone(LAUNCH_OFFER_ENDS_AT_DEFAULT)
        self.assertEqual(WAITLIST_DISPLAY_LABEL, "Coming soon, notify me")

        # 1. When unset in env, launch offer is inactive/unconfigured and Basic shows regular ₹399
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("NV_LAUNCH_STARTS_AT", None)
            os.environ.pop("NV_LAUNCH_STARTED_AT", None)
            os.environ.pop("NV_LAUNCH_ENDS_AT", None)
            st_unset = resolve_launch_offer_state()
            self.assertFalse(st_unset["configured"])
            self.assertFalse(st_unset["active"])
            b_unset = resolve_sku_price("report_basic")
            self.assertEqual(b_unset["amount_inr"], 399)
            self.assertIsNone(b_unset["struck_mrp_inr"])
            self.assertEqual(format_launch_offer_copy("report_basic"), "")
            for wl_sku in ("report_advanced", "report_premium"):
                w_info = resolve_sku_price(wl_sku)
                self.assertTrue(w_info["waitlist_only"])
                self.assertIsNone(w_info["amount_inr"])
                self.assertIsNone(w_info["struck_mrp_inr"])
                self.assertEqual(w_info["display_price_label"], "Coming soon, notify me")
                self.assertEqual(format_launch_offer_copy(wl_sku), "")

        # 2. When 7x24h window is set via NV_LAUNCH_STARTS_AT & NV_LAUNCH_ENDS_AT:
        win_env = {
            "NV_LAUNCH_STARTS_AT": "2027-01-10T00:00:00+05:30",
            "NV_LAUNCH_ENDS_AT": "2027-01-17T00:00:00+05:30",
        }
        before_iso = "2027-01-12T12:00:00+05:30"
        after_iso = "2027-01-17T00:00:01+05:30"
        with patch.dict(os.environ, win_env, clear=False):
            self.assertTrue(resolve_launch_offer_state(now_iso=before_iso)["active"])
            self.assertFalse(resolve_launch_offer_state(now_iso=after_iso)["active"])
            b_act = resolve_sku_price("report_basic", now_iso=before_iso)
            b_exp = resolve_sku_price("report_basic", now_iso=after_iso)
            self.assertEqual(b_act["amount_inr"], 199)
            self.assertEqual(b_act["struck_mrp_inr"], 399)
            self.assertEqual(b_exp["amount_inr"], 399)
            self.assertIsNone(b_exp["struck_mrp_inr"])
            # Waitlist tiers STILL have zero launch price, struck price, or offer copy while notify_me_higher_tiers=true
            for wl_sku in ("report_advanced", "report_premium"):
                w_act = resolve_sku_price(wl_sku, now_iso=before_iso)
                self.assertIsNone(w_act["amount_inr"])
                self.assertIsNone(w_act["struck_mrp_inr"])
                self.assertEqual(w_act["display_price_label"], "Coming soon, notify me")
                self.assertEqual(format_launch_offer_copy(wl_sku, now_iso=before_iso), "")

    def test_07_plain_product_descriptors_zero_per_page_zero_tax_invoice_and_zero_hardcoded_nov_dates(self):
        for page_rel in ("your-reading/index.html", "pricing/index.html", "reports/index.html"):
            with open(os.path.join(DIST_DIR, *page_rel.split("/")), "r", encoding="utf-8") as f:
                txt = f.read()
            self.assertIn("Complete Numerology Report, 32 pages", txt, f"Missing 32-page plain descriptor in {page_rel}")
            self.assertIn("Advanced Numerology Report, 12 pages", txt, f"Missing 12-page plain descriptor in {page_rel}")
            self.assertIn("Basic Numerology Report, 3 pages", txt, f"Missing 3-page plain descriptor in {page_rel}")

        for scan_dir in (os.path.join(ROOT, "app"), DIST_DIR):
            for dp, _, fns in os.walk(scan_dir):
                for fn in fns:
                    if fn.lower().endswith((".html", ".js", ".py", ".json", ".ts", ".txt")):
                        fp = os.path.join(dp, fn)
                        with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                            txt = f.read()
                        self.assertIsNone(
                            re.search(r"₹\s*\d+\s*/\s*page", txt, re.I),
                            f"Found forbidden per-page price line in {fp}",
                        )
                        self.assertNotIn("per_page_inr", txt, f"Found legacy per_page_inr key in {fp}")
                        self.assertNotIn("tax invoice", txt.lower(), f"Found forbidden 'tax invoice' in {fp}")
                        self.assertNotIn("19 nov 2026", txt.lower(), f"Found hardcoded '19 Nov 2026' in {fp}")
                        self.assertNotIn("20 nov 2026", txt.lower(), f"Found hardcoded '20 Nov 2026' in {fp}")

    def test_08_homepage_menu_footer_and_llms_txt_link_straight_to_canonical_calculators(self):
        for check_path in (
            os.path.join(DIST_DIR, "index.html"),
            os.path.join(DIST_DIR, "llms.txt"),
            os.path.join(DIST_DIR, "llms-full.txt"),
            os.path.join(ROOT, "app", "templates", "master_header.html"),
            os.path.join(ROOT, "app", "templates", "master_footer.html"),
        ):
            with open(check_path, "r", encoding="utf-8") as f:
                txt = f.read()
            self.assertIn("/calculators/", txt)
            self.assertNotIn("/tools/", txt, f"Found non-canonical /tools/ link in {check_path}")
            self.assertNotIn("/charm_ai.html", txt, f"Found legacy /charm_ai.html link in {check_path}")
            self.assertNotIn("/privacy-policy/", txt, f"Found legacy /privacy-policy/ link in {check_path}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
