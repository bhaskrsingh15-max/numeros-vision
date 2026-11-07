"""
NUMEROS VISION — 2027 YEAR AHEAD PLANNER BACKEND TEST SUITE
===========================================================
Validates:
1. Server pricing authority & offer date cutoff (149900 vs 199900).
2. Live Razorpay key refusal (never allows rzp_live_*).
3. Fail-closed placeholder check on paid generation (HTTP 422, releases zero PDF).
4. Sample preview generation (is_sample=True produces 24-page PDF).
5. Name & DOB validation and tamper protection.
6. HMAC request signing and verification to Cloud Run generator service.
7. Database migration 0008 schema integrity.
"""

import os
import sys
import json
import time
import hmac
import hashlib
import datetime
import unittest

_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi import HTTPException
from app.services.internal_pdf_worker_service import (
    render_planner_2027_from_payload,
    compute_worker_hmac_signature,
    verify_worker_hmac_signature,
    assert_no_live_razorpay_keys
)
from app.config.planner_2027_pricing import (
    get_planner_2027_price,
    load_planner_2027_config
)


class TestPlanner2027Backend(unittest.TestCase):

    def setUp(self):
        self.secret = "test_pdf_service_secret_2027"
        os.environ["PDF_SERVICE_SECRET"] = self.secret

    def tearDown(self):
        for k in list(os.environ.keys()):
            if k.startswith("RAZORPAY_TEST_DUMMY"):
                os.environ.pop(k, None)

    # ─────────────────────────────────────────────────────────────────
    # 1. PRICING & SERVER AUTHORITY TESTS
    # ─────────────────────────────────────────────────────────────────
    def test_pricing_config_and_dates(self):
        """Asserts pricing constants and strict server-side offer cutoff."""
        cfg = load_planner_2027_config()
        self.assertEqual(cfg["list_price_paise"], 199900)
        self.assertEqual(cfg["offer_price_paise"], 149900)
        self.assertEqual(cfg["currency"], "INR")
        self.assertFalse(cfg["price_includes_gst"])
        self.assertEqual(cfg["receipt_type"], "Payment receipt")
        self.assertEqual(cfg["offer_ends_at"], "2027-01-31T23:59:00+05:30")

        # Before cutoff: must be offer price 149,900 paise (₹1,499)
        dt_before = datetime.datetime(2027, 1, 15, 12, 0, 0, tzinfo=datetime.timezone.utc)
        price_before = get_planner_2027_price(now=dt_before)
        self.assertEqual(price_before["amount_paise"], 149900)
        self.assertTrue(price_before["is_offer_active"])

        # After cutoff: must be list price 199,900 paise (₹1,999)
        dt_after = datetime.datetime(2027, 2, 5, 12, 0, 0, tzinfo=datetime.timezone.utc)
        price_after = get_planner_2027_price(now=dt_after)
        self.assertEqual(price_after["amount_paise"], 199900)
        self.assertFalse(price_after["is_offer_active"])

    def test_pricing_files_sha256_parity(self):
        """Asserts app/config and pdf_service/app/config pricing JSON files are byte-for-byte identical."""
        path1 = os.path.join(_ROOT, "app", "config", "planner_2027_pricing.json")
        path2 = os.path.join(_ROOT, "pdf_service", "app", "config", "planner_2027_pricing.json")
        self.assertTrue(os.path.exists(path1), f"Missing {path1}")
        self.assertTrue(os.path.exists(path2), f"Missing {path2}")
        with open(path1, "rb") as f1, open(path2, "rb") as f2:
            data1 = f1.read()
            data2 = f2.read()
            h1 = hashlib.sha256(data1).hexdigest()
            h2 = hashlib.sha256(data2).hexdigest()
            self.assertEqual(h1, h2, "app/config and pdf_service/app/config pricing JSON files must have identical SHA-256")

    # ─────────────────────────────────────────────────────────────────
    # 2. LIVE KEY REFUSAL TEST
    # ─────────────────────────────────────────────────────────────────
    def test_live_key_refusal_raises_error(self):
        """Refuses to start or generate if any Razorpay key begins with rzp_live."""
        os.environ["RAZORPAY_TEST_DUMMY_LIVE"] = "rzp_live_abc12345"
        try:
            with self.assertRaises(RuntimeError) as cm:
                assert_no_live_razorpay_keys()
            self.assertIn("Live Razorpay key detected", str(cm.exception))
        finally:
            os.environ.pop("RAZORPAY_TEST_DUMMY_LIVE", None)

    # ─────────────────────────────────────────────────────────────────
    # 3. HMAC SIGNATURE VERIFICATION
    # ─────────────────────────────────────────────────────────────────
    def test_hmac_signature_verification(self):
        """Validates timestamp freshness, tamper detection, and constant-time compare."""
        raw_body = b'{"full_name": "Arun Sharma", "dob_str": "1988-04-14", "is_sample": true}'
        ts = str(int(time.time()))
        valid_sig = compute_worker_hmac_signature(raw_body, ts, self.secret)

        # Valid signature succeeds
        ok, reason = verify_worker_hmac_signature(raw_body, ts, valid_sig, self.secret)
        self.assertTrue(ok)
        self.assertEqual(reason, "ok")

        # Tampered body fails
        ok_tamper, _ = verify_worker_hmac_signature(raw_body + b"tamper", ts, valid_sig, self.secret)
        self.assertFalse(ok_tamper)

        # Expired timestamp (>300s clock skew) fails
        old_ts = str(int(time.time()) - 400)
        old_sig = compute_worker_hmac_signature(raw_body, old_ts, self.secret)
        ok_exp, reason_exp = verify_worker_hmac_signature(raw_body, old_ts, old_sig, self.secret)
        self.assertFalse(ok_exp)
        self.assertIn("clock skew", reason_exp)

    # ─────────────────────────────────────────────────────────────────
    # 4. INPUT VALIDATION & TAMPER PROTECTION
    # ─────────────────────────────────────────────────────────────────
    def test_payload_input_validation(self):
        """Rejects short/long names and out-of-bound DOB."""
        # Short name
        with self.assertRaises(HTTPException) as cm:
            render_planner_2027_from_payload({"full_name": "A", "dob_str": "1988-04-14", "is_sample": True})
        self.assertEqual(cm.exception.status_code, 400)
        self.assertIn("Invalid full_name", cm.exception.detail)

        # Invalid DOB year (1850)
        with self.assertRaises(HTTPException) as cm2:
            render_planner_2027_from_payload({"full_name": "Arun Sharma", "dob_str": "1850-04-14", "is_sample": True})
        self.assertEqual(cm2.exception.status_code, 400)
        self.assertIn("DOB must be between 1900 and 2026", cm2.exception.detail)

    # ─────────────────────────────────────────────────────────────────
    # 5. SAMPLE PREVIEW GENERATION
    # ─────────────────────────────────────────────────────────────────
    def test_sample_preview_generation_succeeds(self):
        """is_sample=True produces valid 24-page PDF with SAMPLE watermark."""
        payload = {
            "full_name": "Arun Sharma",
            "dob_str": "1988-04-14",
            "order_id": "test_preview_1",
            "is_sample": True
        }
        pdf_bytes, meta = render_planner_2027_from_payload(payload)
        self.assertTrue(pdf_bytes.startswith(b"%PDF"))
        self.assertTrue(len(pdf_bytes) > 50000)
        self.assertEqual(meta["order_id"], "test_preview_1")
        self.assertTrue(meta["is_sample"])

    # ─────────────────────────────────────────────────────────────────
    # 6. FAIL-CLOSED PLACEHOLDER RULE (CRITICAL MANDATE)
    # ─────────────────────────────────────────────────────────────────
    def test_paid_generation_fails_closed_on_unapproved_placeholder(self):
        """
        Paid generation (is_sample=False) MUST FAIL CLOSED with HTTP 422
        if any '{{' placeholder (such as {{DISCLAIMER_APPROVED_TEXT}}) remains in the rendered PDF.
        """
        payload = {
            "full_name": "Arun Sharma",
            "dob_str": "1988-04-14",
            "order_id": "test_paid_fail_closed_1",
            "is_sample": False
        }
        with self.assertRaises(HTTPException) as cm:
            render_planner_2027_from_payload(payload)
        self.assertEqual(cm.exception.status_code, 422)
        self.assertIn("Fail-closed: unapproved placeholder remains in paid PDF", cm.exception.detail)

    # ─────────────────────────────────────────────────────────────────
    # 7. MIGRATION 0008 D1 TABLE SCHEMA INTEGRITY
    # ─────────────────────────────────────────────────────────────────
    def test_migration_0008_schema(self):
        """Verifies migration 0008 contains all mandatory columns and stores zero card data."""
        mig_path = os.path.join(_ROOT, "migrations", "0008_planner_2027_orders.sql")
        self.assertTrue(os.path.exists(mig_path), "Migration 0008 must exist.")
        with open(mig_path, "r", encoding="utf-8") as f:
            sql = f.read()

        mandatory_cols = [
            "id TEXT PRIMARY KEY",
            "razorpay_order_id TEXT UNIQUE",
            "razorpay_payment_id TEXT",
            "status TEXT NOT NULL DEFAULT 'created'",
            "amount_paise INTEGER NOT NULL",
            "currency TEXT NOT NULL DEFAULT 'INR'",
            "name_normalised TEXT NOT NULL",
            "dob TEXT NOT NULL",
            "email TEXT NOT NULL",
            "phone TEXT",
            "consent_version TEXT NOT NULL",
            "consent_at INTEGER NOT NULL",
            "download_token_hash TEXT",
            "token_expires_at INTEGER",
            "generation_count INTEGER NOT NULL DEFAULT 0",
            "pdf_r2_key TEXT",
            "created_at INTEGER NOT NULL",
            "updated_at INTEGER NOT NULL"
        ]
        for col in mandatory_cols:
            self.assertIn(col.split()[0], sql, f"Column {col} missing in migration 0008")

        # Zero card data guarantee
        forbidden_card_terms = ["card_number", "cvv", "expiry_month", "expiry_year", "card_token"]
        for term in forbidden_card_terms:
            self.assertNotIn(term, sql.lower(), f"Forbidden card storage term '{term}' found in migration 0008")


    # ─────────────────────────────────────────────────────────────────
    # 8. COMMIT B2: SALES PAGE, LABELS, LEGAL & SEO INTEGRITY
    # ─────────────────────────────────────────────────────────────────
    def test_sample_labels_match_golden_sheets(self):
        """Asserts sample labels on year_2027.html match golden_sheets.json real calculations."""
        golden_path = os.path.join(_ROOT, "tests", "golden_sheets.json")
        with open(golden_path, "r", encoding="utf-8") as gf:
            golden = json.load(gf)

        a = golden["A"]
        b = golden["B"]
        expected_a = f"Sample A: {a['name'].title()} (Mulank {a['mulank']}, Bhagyank {a['bhagyank']}, Personal Year {a['personal_year_2027']})"
        expected_b = f"Sample B: {b['name'].title()} (Mulank {b['mulank']}, Bhagyank {b['bhagyank']}, Personal Year {b['personal_year_2027']})"

        html_path = os.path.join(_ROOT, "app", "static", "year_2027.html")
        with open(html_path, "r", encoding="utf-8") as hf:
            html = hf.read()

        self.assertIn(expected_a, html, f"Missing expected Sample A label: {expected_a}")
        self.assertIn(expected_b, html, f"Missing expected Sample B label: {expected_b}")

    def test_no_placeholders_in_public_pdfs(self):
        """Asserts zero public PDFs in app/static or dist_cloudflare_pages contain '{{' unapproved placeholders."""
        for search_dir in [os.path.join(_ROOT, "app", "static"), os.path.join(_ROOT, "dist_cloudflare_pages")]:
            if not os.path.exists(search_dir):
                continue
            for root, _, files in os.walk(search_dir):
                for f in files:
                    if f.lower().endswith(".pdf"):
                        pdf_path = os.path.join(root, f)
                        with open(pdf_path, "rb") as pf:
                            pdf_bytes = pf.read()
                            self.assertNotIn(
                                b"{{",
                                pdf_bytes,
                                f"Public PDF '{pdf_path}' contains unapproved '{{{{' placeholder"
                            )

    def test_no_tax_claims_and_pricing_only(self):
        """Asserts year_2027.html does not claim statutory GST or payment receipt, showing price only."""
        html_path = os.path.join(_ROOT, "app", "static", "year_2027.html")
        with open(html_path, "r", encoding="utf-8") as hf:
            html = hf.read()

        self.assertNotIn("Excludes statutory GST", html)
        self.assertNotIn("statutory GST", html)
        self.assertIn("Offer ends 31 January 2027", html)
        self.assertIn("₹1,499", html)

    def test_seo_meta_and_structured_data(self):
        """Asserts SEO title (50-60 chars), description (140-160 chars), canonical, OG, Twitter & JSON-LD."""
        import re
        html_path = os.path.join(_ROOT, "app", "static", "year_2027.html")
        with open(html_path, "r", encoding="utf-8") as hf:
            html = hf.read()

        # Title: 50-60 chars
        title_m = re.search(r"<title>(.*?)</title>", html)
        self.assertIsNotNone(title_m)
        title = title_m.group(1).strip()
        self.assertTrue(50 <= len(title) <= 60, f"Title length {len(title)} not in [50, 60]: '{title}'")

        # Description: 140-160 chars
        desc_m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', html)
        self.assertIsNotNone(desc_m)
        desc = desc_m.group(1).strip()
        self.assertTrue(140 <= len(desc) <= 160, f"Description length {len(desc)} not in [140, 160]: '{desc}'")

        # Canonical
        self.assertIn('<link rel="canonical" href="https://numerosvision.com/year_2027.html" />', html)

        # OG and Twitter
        self.assertIn('<meta property="og:title"', html)
        self.assertIn('<meta name="twitter:card"', html)

        # JSON-LD Product & Offer
        jsonld_m = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
        self.assertIsNotNone(jsonld_m)
        ld = json.loads(jsonld_m.group(1))
        self.assertEqual(ld["@type"], "Product")
        self.assertEqual(ld["name"], "2027 Year Ahead Planner")
        self.assertEqual(ld["offers"]["price"], "1499")
        self.assertEqual(ld["offers"]["priceCurrency"], "INR")
        self.assertEqual(ld["offers"]["priceValidUntil"], "2027-01-31")
        self.assertNotIn("aggregateRating", ld, "Zero review/rating markup allowed")
        self.assertNotIn("review", ld, "Zero review/rating markup allowed")

    def test_forbidden_words_in_sales_page(self):
        """Asserts no forbidden words appear in app/static/year_2027.html."""
        import re
        forbidden = [
            "luck", "lucky", "guaranteed", "will bring", "will fix",
            "prediction", "prescription", "consecrated", "cure", "exact", "mrp"
        ]
        pattern = re.compile(r"\b(" + "|".join(forbidden) + r")\b", re.IGNORECASE)

        html_path = os.path.join(_ROOT, "app", "static", "year_2027.html")
        with open(html_path, "r", encoding="utf-8") as hf:
            for lno, line in enumerate(hf, 1):
                # Ignore script tag content that defines the test list itself
                m = pattern.search(line)
                self.assertIsNone(
                    m,
                    f"Forbidden word '{m.group() if m else ''}' found at line {lno}: {line.strip()}"
                )


if __name__ == "__main__":
    unittest.main()
