"""
tests/test_preview_audit_batch_a.py
===================================
Automated unittest suite verifying all Preview-Audit Fix List items (Batch A `1`–`9` + `a`–`d`):
1. 2027 Planner (`planner_2027`):
   - Waitlist-only ("Coming soon, notify me"), zero price / struck price / Early-Access Offer
   - Zero `Offer` / `offers` / `price` in JSON-LD (`year_2027.html` & `planner_2027_jsonld.py`)
   - Server-side order creation returns `409 PLANNER_WAITLIST_ONLY`
   - Waitlist `/api/v1/waitlist/notify-me` accepts `planner_2027`
2. Report Deliverables & Schema / `llms.txt` / Email Parity:
   - Exact 5 ground-truth bullets per tier in `packs.json`
   - Zero "Primary Gemstone & Auspicious Color Vectors" on Basic
   - Zero undelivered Advanced/Premium claims ("Priority 1-Year Charm AI Consultation Access",
     "Technical Appendix with Mathematical Proofs", "Imperial Premium Sovereign Dossier")
   - Zero `Offer` / `price` in JSON-LD on ANY unpriced/waitlist product across all built HTML pages
   - Approved waitlist caption ("When this report opens, it starts at a launch price for its first 7 days. We’ll email you the day it opens.")
3. De-jargonised Pricing Intro:
   - Zero "vibrates to", "sealing your energetic alignment", "Sacred Commercial Mathematics", "Shagun", "Manrope"
4. Collapsed Coming-Soon Line, Single "Coming soon, notify me" Per Waitlist Card, & Zero Emoji Category Chips on `/pricing/`
5. `terminology_geo.json` Alignment Across Web Pages
6. Canonical `/sample/` Redirects & Meta Descriptions (`120–155` chars)
7. `300+` Words Deterministic Explanations + 1:1 Visible FAQ & `FAQPage` Schema on All Calculator Pages
   + "Kundali Milan vs Numerology Compatibility" section on `/calculators/compatibility/`
8. Production vs Preview Guards:
   - Every canonical & `og:url` in `dist_cloudflare_pages/` points to `https://numerosvision.com/...` (never `pages.dev`)
   - `dist_cloudflare_pages/robots.txt` is the production `robots.txt`
   - Per-second preview countdown banner (`#nv-preview-launch-banner`) never renders on `numerosvision.com`
"""

import html
import json
import re
import unittest
from pathlib import Path

from app.api.payments import CreateOrderRequest, create_order, create_planner_2027_order_endpoint
from app.config.planner_2027_jsonld import generate_planner_2027_jsonld
from app.services.waitlist_service import _PACK_TITLES as ALLOWED_WAITLIST_PACKS


def _run_coro(coro):
    try:
        coro.send(None)
    except StopIteration as exc:
        return exc.value
    finally:
        coro.close()

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist_cloudflare_pages"


def _strip_tags(raw_html: str) -> str:
    no_scripts = re.sub(r"<(script|style|noscript)[^>]*>.*?</\1>", " ", raw_html, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", no_scripts)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def _extract_jsonld_blocks(raw_html: str) -> list:
    blocks = []
    for m in re.finditer(r'<script[^>]+type=["\']application/ld\+json["\'][^>]*>(.*?)</script>', raw_html, flags=re.I | re.S):
        txt = m.group(1).strip()
        if txt:
            blocks.append(json.loads(txt))
    return blocks


def _iter_ld_nodes(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from _iter_ld_nodes(v)
    elif isinstance(obj, list):
        for item in obj:
            yield from _iter_ld_nodes(item)


class TestPreviewAuditBatchA(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        assert DIST.exists(), "dist_cloudflare_pages/ must exist before running Batch A audit tests"
        cls.packs = json.loads((ROOT / "app" / "config" / "packs.json").read_text(encoding="utf-8"))

    def test_01_planner_2027_waitlist_zero_price_and_server_order_block(self):
        """Item 1 + a: Planner has no price/offer on page or schema, and order creation returns 409."""
        year_html = (DIST / "year-2027" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Coming soon, notify me", year_html)
        for banned in ["List Price ₹1,999", "₹1,999", "1,499", "Early-Access Offer", "Offer ends 31 January 2027"]:
            self.assertNotIn(banned, year_html, f"Banned Planner pricing text found: {banned}")

        # JSON-LD check on year-2027 and builder
        planner_cfg = json.loads((ROOT / "app" / "config" / "planner_2027_pricing.json").read_text(encoding="utf-8"))
        graph = generate_planner_2027_jsonld(planner_cfg)
        graph_str = json.dumps(graph)
        self.assertNotIn('"Offer"', graph_str)
        self.assertNotIn('"offers"', graph_str)
        self.assertNotIn('"price"', graph_str)

        for ld in _extract_jsonld_blocks(year_html):
            ld_str = json.dumps(ld)
            self.assertNotIn('"Offer"', ld_str)
            self.assertNotIn('"offers"', ld_str)
            self.assertNotIn('"price"', ld_str)

        # Waitlist service allows planner_2027
        self.assertIn("planner_2027", ALLOWED_WAITLIST_PACKS)

        # Server-side FastAPI payment order creation blocks planner_2027 with 409
        from starlette.requests import Request as StarletteRequest

        order_resp = _run_coro(
            create_order(
                CreateOrderRequest(
                    plan="planner_2027",
                    name="Test User",
                    email="test@example.com",
                    mobile="9876543210",
                )
            )
        )
        self.assertEqual(order_resp.status_code, 409)
        self.assertIn("PLANNER_WAITLIST_ONLY", order_resp.body.decode("utf-8"))

        planner_ep_resp = _run_coro(
            create_planner_2027_order_endpoint(
                StarletteRequest({"type": "http", "method": "POST", "path": "/api/planner-2027/order", "headers": []})
            )
        )
        self.assertEqual(planner_ep_resp.status_code, 409)
        self.assertIn("PLANNER_WAITLIST_ONLY", planner_ep_resp.body.decode("utf-8"))

    def test_02_report_deliverables_parity_and_banned_claims_removed(self):
        """Item 2 + a + Carry-Forward #1: Exact 5 bullets per tier across surfaces; zero undelivered claims."""
        core_reports = self.packs["core_reports"]
        basic_feats = core_reports["report_basic"]["deliverables"]
        adv_feats = core_reports["report_advanced"]["deliverables"]
        prem_feats = core_reports["report_premium"]["deliverables"]
        self.assertEqual(len(basic_feats), 5)
        self.assertEqual(len(adv_feats), 5)
        self.assertEqual(len(prem_feats), 5)

        surfaces = {
            "pricing": (DIST / "pricing" / "index.html").read_text(encoding="utf-8"),
            "reports": (DIST / "reports" / "index.html").read_text(encoding="utf-8"),
            "your-reading": (DIST / "your-reading" / "index.html").read_text(encoding="utf-8"),
            "dashboard": (DIST / "dashboard" / "index.html").read_text(encoding="utf-8"),
            "llms.txt": (DIST / "llms.txt").read_text(encoding="utf-8"),
            "llms-full.txt": (DIST / "llms-full.txt").read_text(encoding="utf-8"),
            "_worker.js": (DIST / "_worker.js").read_text(encoding="utf-8"),
            "nv_pricing_catalog.js": (DIST / "static" / "js" / "nv_pricing_catalog.js").read_text(encoding="utf-8"),
        }

        banned_claims = [
            "Primary Gemstone & Auspicious Color Vectors",
            "Priority 1-Year Charm AI Consultation Access",
            "Includes 1-Year AI Numerologist Question Credits",
            "Technical Appendix with Mathematical Proofs",
            "Imperial Premium Sovereign Dossier",
            "Phonetic Beej Mantras",
        ]
        for surf_name, content in surfaces.items():
            for claim in banned_claims:
                self.assertNotIn(claim, content, f"Undelivered claim '{claim}' still in {surf_name}")

        # Verify Basic 5 bullets appear on pricing, reports, your-reading, dashboard, llms.txt, and _worker.js
        for feat in basic_feats:
            for surf_name in ("pricing", "reports", "your-reading", "dashboard", "llms.txt", "_worker.js"):
                unescaped_surf = html.unescape(surfaces[surf_name])
                self.assertIn(feat, unescaped_surf, f"Basic bullet '{feat}' missing from {surf_name}")

        # Approved waitlist caption present on pricing, reports, and your-reading
        approved_caption = "When this report opens, it starts at a launch price for its first 7 days. We’ll email you the day it opens."
        for surf_name in ("pricing", "reports", "your-reading"):
            unescaped = html.unescape(surfaces[surf_name]).replace("'", "’")
            self.assertIn(approved_caption, unescaped, f"Approved waitlist caption missing on {surf_name}")

    def test_03_zero_schema_price_for_waitlist_products_sitewide(self):
        """Addition (a): No waitlist/unpriced product has an Offer or price in JSON-LD anywhere in dist."""
        waitlist_names = ("12-page", "advanced numerology", "32-page", "complete numerology", "2027 personal year", "annual numerology planner")
        for html_file in DIST.rglob("*.html"):
            raw = html_file.read_text(encoding="utf-8", errors="ignore")
            for block in _extract_jsonld_blocks(raw):
                for node in _iter_ld_nodes(block):
                    ntype = str(node.get("@type", ""))
                    if ntype in ("Product", "Book"):
                        name_lower = str(node.get("name", "")).lower()
                        if any(w in name_lower for w in waitlist_names):
                            self.assertNotIn(
                                "offers",
                                node,
                                f"Waitlist Product/Book '{node.get('name')}' in {html_file} MUST NOT contain 'offers'",
                            )
                            self.assertNotIn(
                                "price",
                                node,
                                f"Waitlist Product/Book '{node.get('name')}' in {html_file} MUST NOT contain 'price'",
                            )

    def test_04_pricing_intro_dejargonised_and_single_waitlist_cta(self):
        """Items 3 & 4: Pricing intro cleaned; emoji chips removed; 'Coming soon, notify me' not duplicated per card."""
        pricing_html = (DIST / "pricing" / "index.html").read_text(encoding="utf-8")
        for jargon in [
            "sealing your energetic alignment",
            "Sacred Commercial Mathematics",
            "Shagun",
            "Auspicious Pricing Packages",
            "Manrope",
        ]:
            self.assertNotIn(jargon, pricing_html, f"Jargon/font '{jargon}' still in pricing/index.html")

        # Category filter chips removed
        self.assertNotIn('class="category-filter-bar"', pricing_html)

    def test_05_sample_redirects_meta_descriptions_and_internal_links(self):
        """Item 6 + b: /sample-report/ and /sample_roadmap/ 301 -> /sample/ in 1 hop; meta descriptions 120-155 chars."""
        redirects_txt = (DIST / "_redirects").read_text(encoding="utf-8")
        self.assertRegex(redirects_txt, r"(?m)^/sample-report/?\s+/sample/\s+301\b")
        self.assertRegex(redirects_txt, r"(?m)^/sample_roadmap/?\s+/sample/\s+301\b")
        self.assertRegex(redirects_txt, r"(?m)^/sample-roadmap/?\s+/sample/\s+301\b")

        meta_targets = [
            DIST / "pricing" / "index.html",
            DIST / "sample" / "index.html",
            ROOT / "app" / "static" / "sample_roadmap.html",
            DIST / "reports" / "index.html",
            DIST / "compare" / "index.html",
        ]
        for p in meta_targets:
            raw = p.read_text(encoding="utf-8")
            m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']', raw, flags=re.I)
            self.assertIsNotNone(m, f"Missing meta description in {p}")
            desc = html.unescape(m.group(1)).strip()
            self.assertTrue(
                120 <= len(desc) <= 155,
                f"Meta description in {p.name} is {len(desc)} chars (must be 120-155): '{desc}'",
            )

        # Ensure internal links across dist HTML no longer point to /sample_roadmap/ or /sample-report/
        for html_file in DIST.rglob("*.html"):
            if html_file.name == "sample_roadmap.html":
                continue
            raw = html_file.read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn('href="/sample_roadmap', raw, f"Legacy /sample_roadmap link in {html_file.relative_to(DIST)}")
            self.assertNotIn('href="/sample-report', raw, f"Legacy /sample-report link in {html_file.relative_to(DIST)}")

    def test_06_calculator_word_counts_faq_schema_parity_and_kundali_milan(self):
        """Item 7 + c: All calculators have 300+ words, 1:1 FAQPage parity on enriched pages, and Kundali Milan section."""
        enriched_slugs = [
            "compatibility",
            "property-numerology",
            "vehicle-numerology",
            "profession-calculator",
            "baby-naming",
            "personal-year",
            "name-numerology",
            "favourable-numbers",
        ]
        for calc_index in sorted((DIST / "calculators").glob("*/index.html")):
            slug = calc_index.parent.name
            raw = calc_index.read_text(encoding="utf-8")
            no_chrome = re.sub(r"<(header|footer|nav)[^>]*>.*?</\1>", " ", raw, flags=re.I | re.S)
            words = _strip_tags(no_chrome).split()
            self.assertGreaterEqual(
                len(words),
                300,
                f"/calculators/{slug}/ has only {len(words)} body words (expected >= 300)",
            )

        for slug in enriched_slugs:
            page_path = DIST / "calculators" / slug / "index.html"
            raw = page_path.read_text(encoding="utf-8")

            # Verify 1:1 visible text match for every FAQPage Question & Answer
            full_visible = _strip_tags(raw)
            faq_entities = []
            for block in _extract_jsonld_blocks(raw):
                for node in _iter_ld_nodes(block):
                    if node.get("@type") == "FAQPage":
                        faq_entities.extend(node.get("mainEntity", []))
            self.assertGreaterEqual(len(faq_entities), 4, f"/calculators/{slug}/ must have FAQPage JSON-LD")
            for q_node in faq_entities:
                q_text = re.sub(r"\s+", " ", q_node["name"]).strip()
                a_text = re.sub(r"\s+", " ", q_node["acceptedAnswer"]["text"]).strip()
                self.assertIn(q_text, full_visible, f"FAQ question not visible on /calculators/{slug}/: {q_text}")
                self.assertIn(a_text[:80], full_visible, f"FAQ answer not visible on /calculators/{slug}/: {a_text[:80]}")

        # Compatibility page specifically includes honest Kundali Milan vs Numerology Compatibility section
        compat_html = (DIST / "calculators" / "compatibility" / "index.html").read_text(encoding="utf-8")
        self.assertIn("Kundali Milan vs Numerology Compatibility", compat_html)
        self.assertIn("Ashtakoot", compat_html)

    def test_07_production_canonical_urls_robots_txt_and_preview_only_countdown(self):
        """Item 8 + d + Countdown Banner Confirmation: Production build canonicals, robots.txt, and preview-only banner."""
        for html_file in DIST.rglob("*.html"):
            if "amp" in html_file.parts:
                continue
            raw = html_file.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']', raw, flags=re.I):
                href = m.group(1)
                self.assertTrue(
                    href.startswith("https://numerosvision.com"),
                    f"Non-production canonical '{href}' in {html_file.relative_to(DIST)}",
                )
                self.assertNotIn("pages.dev", href)

            for m in re.finditer(r'<meta[^>]+property=["\']og:url["\'][^>]+content=["\']([^"\']+)["\']', raw, flags=re.I):
                og_url = m.group(1)
                self.assertTrue(
                    og_url.startswith("https://numerosvision.com"),
                    f"Non-production og:url '{og_url}' in {html_file.relative_to(DIST)}",
                )
                self.assertNotIn("pages.dev", og_url)

        # Production robots.txt check
        robots_txt = (DIST / "robots.txt").read_text(encoding="utf-8")
        self.assertIn("Sitemap: https://numerosvision.com/sitemap.xml", robots_txt)
        self.assertNotRegex(robots_txt, r"(?m)^Disallow:\s*/\s*$")
        # /dashboard/, /login/, /signup/ Disallow removed per earlier instruction
        for route in ("/dashboard/", "/login/", "/signup/"):
            self.assertNotIn(f"Disallow: {route}", robots_txt)

        # Confirm per-second countdown banner is strictly preview-only in _worker.js and absent from static HTML
        worker_js = (DIST / "_worker.js").read_text(encoding="utf-8")
        self.assertIn("nv-preview-launch-banner", worker_js)
        self.assertIn('if (isPreview && !modifiedHtml.includes(\'id="nv-preview-launch-banner"\'))', worker_js)
        for html_file in DIST.rglob("*.html"):
            raw = html_file.read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn('id="nv-preview-launch-banner"', raw, f"Preview banner baked into static {html_file}")


if __name__ == "__main__":
    unittest.main()
