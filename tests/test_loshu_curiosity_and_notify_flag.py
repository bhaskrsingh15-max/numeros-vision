import asyncio
import json
import os
import re
import unittest
from unittest.mock import patch
from fastapi import HTTPException

from app.api.payments import (
    CreateOrderRequest,
    NotifyMeWaitlistRequest,
    create_order,
    get_pricing_catalog,
    get_public_loshu_teasers,
    register_notify_me_waitlist,
)
from app.config.pricing_config import is_notify_me_higher_tiers_enabled

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "dist_cloudflare_pages")


class TestLoShuCuriosityAndNotifyMeFlag(unittest.TestCase):
    """Verifies Mockup A Lo Shu Curiosity Block rules, zero paid prose leaks, assets <=60KB, and Notify-Me flag."""

    def test_01_decorative_assets_budget_under_60kb(self):
        expected_assets = [
            "texture-pearl-gold.webp",
            "emblem-seal-lock.webp",
            "elem-wood.webp",
            "elem-fire.webp",
            "elem-earth.webp",
            "elem-metal.webp",
            "elem-water.webp",
        ]
        asset_dir = os.path.join(BASE_DIR, "app", "static", "assets", "loshu")
        for fname in expected_assets:
            fpath = os.path.join(asset_dir, fname)
            self.assertTrue(os.path.exists(fpath), f"Missing decorative asset: {fname}")
            size_bytes = os.path.getsize(fpath)
            self.assertLessEqual(
                size_bytes, 60 * 1024, f"Asset {fname} exceeds 60 KB budget ({size_bytes} bytes)"
            )

    def test_02_mockup_a_markup_no_prices_on_cells_reduced_motion_and_consent_gate(self):
        yr_path = os.path.join(BASE_DIR, "app", "static", "your-reading.html")
        with open(yr_path, "r", encoding="utf-8") as f:
            html = f.read()

        # Zero raw black #000000
        self.assertNotIn("#000000", html.upper())

        # Approved pattern label
        self.assertIn("Key Lo Shu Patterns:", html)

        # Reduced motion CSS + JS helper
        self.assertIn("@media (prefers-reduced-motion: reduce)", html)
        self.assertIn("prefersReducedMotion()", html)

        # Consent-gated analytics check
        self.assertIn("window.nvConsent.getStatus().analytics === true", html)
        self.assertIn("if (!hasAnalyticsConsent()) return;", html)

        # Extract #loshu-curiosity-card section and verify ZERO price strings or ₹ symbols inside it
        m = re.search(
            r'<section class="loshu-curiosity-card" id="loshu-curiosity-card".*?</section>',
            html,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(m, "Could not locate #loshu-curiosity-card section")
        curiosity_markup = m.group(0)
        self.assertNotIn("₹", curiosity_markup)
        for price_tok in ("199", "289", "489", "699", "1,050", "1050", "1,479", "1479"):
            self.assertNotIn(price_tok, curiosity_markup)

        # Verify cell template has zero ₹ symbols
        cell_tpl_match = re.search(
            r"LOSHU_CELL_ORDER\.map\(\(num, idx\) => \{.*?\}\)\.join", html, flags=re.DOTALL
        )
        self.assertIsNotNone(cell_tpl_match)
        self.assertNotIn("₹", cell_tpl_match.group(0))

        # Verify one three-card ladder with approved prices (199, 489, 1,050) and launch MRPs (289, 699, 1,479)
        self.assertIn('id="price-report_basic">₹199', html)
        self.assertIn('id="price-report_advanced">₹489', html)
        self.assertIn('id="price-report_premium">₹1,050', html)
        self.assertIn("Launch offer valid until 31 Jan 2027", html)

    def test_03_never_ship_paid_report_prose_to_browser(self):
        lib_path = os.path.join(BASE_DIR, "app", "data", "basic_report_content_library.json")
        with open(lib_path, "r", encoding="utf-8") as f:
            lib = json.load(f)

        paid_sentinels = []
        topics = lib.get("topics", {})
        for topic_name, topic_obj in topics.items():
            if topic_name == "loshu_curiosity_teasers":
                continue
            raw_json = json.dumps(topic_obj, ensure_ascii=False)
            for match in re.findall(r'"([^"]{65,})"', raw_json):
                paid_sentinels.append(match)

        self.assertGreater(len(paid_sentinels), 50, "Expected substantial paid sentinel strings")

        files_to_scan = [
            os.path.join(BASE_DIR, "app", "static", "data", "loshu_public_teasers.json"),
            os.path.join(BASE_DIR, "app", "static", "your-reading.html"),
        ]
        dist_yr = os.path.join(DIST_DIR, "your-reading", "index.html")
        if os.path.exists(dist_yr):
            files_to_scan.append(dist_yr)
        dist_teasers = os.path.join(DIST_DIR, "data", "loshu_public_teasers.json")
        if os.path.exists(dist_teasers):
            files_to_scan.append(dist_teasers)

        # Assert server-side library JSON is NOT inside dist_cloudflare_pages
        self.assertFalse(
            os.path.exists(os.path.join(DIST_DIR, "basic_report_content_library.json"))
        )
        self.assertFalse(
            os.path.exists(os.path.join(DIST_DIR, "data", "basic_report_content_library.json"))
        )

        for fpath in files_to_scan:
            with open(fpath, "r", encoding="utf-8") as fh:
                content = fh.read()
            for sentinel in paid_sentinels:
                self.assertNotIn(
                    sentinel,
                    content,
                    f"PAID CONTENT LEAK in {fpath}: {sentinel[:60]}...",
                )

    def test_04_notify_me_flag_off_by_default_and_enforced_when_enabled(self):
        # 1. Default must be strictly False
        with patch.dict(os.environ, {}, clear=False):
            os.environ.pop("NV_NOTIFY_ME_HIGHER_TIERS", None)
            self.assertFalse(is_notify_me_higher_tiers_enabled())
            cat_default = get_pricing_catalog()
            self.assertFalse(cat_default["feature_flags"]["notify_me_higher_tiers"])

        # 2. Public teasers endpoint returns safe public slice
        teasers = get_public_loshu_teasers()
        self.assertTrue(teasers.get("public_browser_safe"))
        self.assertEqual(len(teasers.get("digits", {})), 9)
        self.assertEqual(len(teasers.get("planes", {})), 8)

        # 3. Waitlist endpoint requires consent == True
        with self.assertRaises(HTTPException) as ctx_consent:
            register_notify_me_waitlist(
                NotifyMeWaitlistRequest(
                    email="seeker@example.com", sku_id="report_advanced", consent=False
                )
            )
        self.assertEqual(ctx_consent.exception.status_code, 400)

        # 4. Valid waitlist registration succeeds (supports both sku_id and pack_id)
        ok_resp = register_notify_me_waitlist(
            NotifyMeWaitlistRequest(
                email="seeker@example.com",
                sku_id="report_advanced",
                consent=True,
                source_page="your-reading",
            )
        )
        self.assertTrue(ok_resp["success"])
        self.assertEqual(ok_resp["status"], "registered")

        # 5. Invalid SKU rejected
        with self.assertRaises(HTTPException) as ctx_sku:
            register_notify_me_waitlist(
                NotifyMeWaitlistRequest(
                    email="seeker@example.com", sku_id="report_basic", consent=True
                )
            )
        self.assertEqual(ctx_sku.exception.status_code, 400)

        # 6. When NV_NOTIFY_ME_HIGHER_TIERS=true, create_order returns 409 TIER_WAITLIST_ONLY for Advanced/Premium
        def _run_sync_coro(coro):
            try:
                coro.send(None)
            except StopIteration as stop:
                return stop.value
            finally:
                coro.close()
            raise AssertionError("Expected synchronous return before any network await")

        with patch.dict(os.environ, {"NV_NOTIFY_ME_HIGHER_TIERS": "true"}):
            self.assertTrue(is_notify_me_higher_tiers_enabled())
            cat_on = get_pricing_catalog()
            self.assertTrue(cat_on["feature_flags"]["notify_me_higher_tiers"])

            for blocked_sku in ("report_advanced", "report_premium"):
                resp = _run_sync_coro(
                    create_order(
                        CreateOrderRequest(
                            plan=blocked_sku,
                            email="seeker@example.com",
                        )
                    )
                )
                self.assertEqual(resp.status_code, 409)
                payload = json.loads(resp.body.decode("utf-8"))
                self.assertEqual(payload["code"], "TIER_WAITLIST_ONLY")


if __name__ == "__main__":
    unittest.main(verbosity=2)
