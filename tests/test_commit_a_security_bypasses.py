"""
COMMIT A Security Regression Suite:
1. Item 14 (`app/static/tools/logo-intelligence.html` & built `dist_cloudflare_pages/calculators/logo-intelligence/index.html`):
   - No `bypassLogoLockForTest`
   - No `Practitioner Test Mode`
   - No `?unlocked=true` / `get('unlocked')` / `isLogoKitUnlocked` / `executeActual*Download`
   - Zero HTML elements with duplicate `style=` attributes
2. Business Alignment (`app/static/tools/business-alignment.html` & built `dist_cloudflare_pages/calculators/business-alignment/index.html`):
   - No `toggleDossierUnlock` or `Practitioner Test Mode`
3. Server-side token & staging-bypass hardening (`app/api/payments.py`, `app/engine/monetization_alignment_engine.py`):
   - Hardcoded test tokens and staging headers/params are unconditionally rejected in `production` AND `preview` (even if `ALLOW_TEST_TOKENS=true` or `ALLOW_STAGING_TEST_BYPASS=true` is set), and rejected in `staging` unless explicitly authorized.
"""

import os
import pathlib
import re
import unittest

from app.api.payments import get_session_info
from app.engine.monetization_alignment_engine import is_staging_bypass_authorized

ROOT = pathlib.Path(__file__).resolve().parent.parent


class TestCommitASecurityBypasses(unittest.TestCase):

    def _assert_no_duplicate_style_attrs(self, html_text: str, label: str) -> None:
        tag_rx = re.compile(r"<[a-zA-Z0-9-]+(?:\s+[^>]*?)?>", re.DOTALL)
        style_attr_rx = re.compile(r"\bstyle\s*=", re.IGNORECASE)
        offenders = []
        for match in tag_rx.finditer(html_text):
            tag_str = match.group(0)
            if len(style_attr_rx.findall(tag_str)) > 1:
                offenders.append(tag_str[:160])
        self.assertEqual(offenders, [], f"Duplicate style= attributes in {label}: {offenders}")

    def test_logo_intelligence_client_bypasses_and_duplicate_style_removed(self):
        targets = [
            ROOT / "app" / "static" / "tools" / "logo-intelligence.html",
            ROOT / "dist_cloudflare_pages" / "calculators" / "logo-intelligence" / "index.html",
        ]
        forbidden_tokens = [
            "bypassLogoLockForTest",
            "Practitioner Test Mode",
            "get('unlocked')",
            'get("unlocked")',
            "unlocked=true",
            "isLogoKitUnlocked",
            "executeActualSvgDownload",
            "executeActualPngDownload",
            "executeActualJsonDownload",
        ]
        for path in targets:
            self.assertTrue(path.exists(), f"Missing file: {path}")
            html = path.read_text(encoding="utf-8")
            for tok in forbidden_tokens:
                self.assertNotIn(tok, html, f"Forbidden bypass token {tok!r} still present in {path}")
            self._assert_no_duplicate_style_attrs(html, str(path))

    def test_business_alignment_practitioner_bypass_removed(self):
        targets = [
            ROOT / "app" / "static" / "tools" / "business-alignment.html",
            ROOT / "dist_cloudflare_pages" / "calculators" / "business-alignment" / "index.html",
        ]
        for path in targets:
            self.assertTrue(path.exists(), f"Missing file: {path}")
            html = path.read_text(encoding="utf-8")
            self.assertNotIn("toggleDossierUnlock", html, f"toggleDossierUnlock still present in {path}")
            self.assertNotIn("Practitioner Test Mode", html, f"Practitioner Test Mode still present in {path}")

    def test_zero_unlock_or_test_token_bypasses_across_all_static_pages(self):
        static_dir = ROOT / "app" / "static"
        forbidden = ("unlocked=true", "Practitioner Test Mode", "bypassLogoLockForTest", "test_master_pass")
        for path in static_dir.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in (".html", ".js"):
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for tok in forbidden:
                self.assertNotIn(tok, text, f"Forbidden client bypass {tok!r} found in {path}")

    def test_server_test_tokens_and_staging_bypasses_fail_closed_in_prod_and_preview(self):
        saved = dict(os.environ)
        try:
            for locked_env in ("production", "preview"):
                os.environ["ENVIRONMENT"] = locked_env
                os.environ["ALLOW_TEST_TOKENS"] = "true"
                os.environ["ALLOW_STAGING_TEST_BYPASS"] = "true"

                self.assertIsNone(
                    get_session_info("test_master_pass"),
                    f"test_master_pass must be rejected in {locked_env}",
                )
                self.assertIsNone(
                    get_session_info("demo_mode"),
                    f"demo_mode must be rejected in {locked_env}",
                )
                self.assertFalse(
                    is_staging_bypass_authorized(
                        {"x-staging-test-bypass": "true", "host": "staging.numerosvision.com"},
                        {"staging_preview": "true"},
                        token="test_master_pass",
                    ),
                    f"is_staging_bypass_authorized must return False in {locked_env}",
                )

            # In non-local staging without explicit flags, auto-host bypass must also be rejected
            os.environ["ENVIRONMENT"] = "staging"
            os.environ.pop("ALLOW_TEST_TOKENS", None)
            os.environ.pop("ALLOW_STAGING_TEST_BYPASS", None)
            self.assertIsNone(get_session_info("test_master_pass"))
            self.assertFalse(
                is_staging_bypass_authorized(
                    {"host": "staging.numerosvision.com", "x-staging-test-bypass": "true"},
                    {"staging_preview": "true"},
                    token="test_master_pass",
                )
            )
        finally:
            os.environ.clear()
            os.environ.update(saved)


if __name__ == "__main__":
    unittest.main()
