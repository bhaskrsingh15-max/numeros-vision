# -*- coding: utf-8 -*-
"""
tests/test_phase5_logo_intelligence.py
======================================
End-to-end unit & FastAPI integration suite for Phase 5 Logo Intelligence.
"""

from __future__ import annotations

import base64
import datetime
import io
import json
import os
import pathlib
import re
import unittest

from fastapi.testclient import TestClient
from PIL import Image, ImageDraw
import pymupdf

from app.engine.digit_root import digit_root
from app.logo_intelligence.shukla_paksha_timing import calculate_verified_shukla_paksha_window
from app.services.internal_engine_service import app

REPO_ROOT = pathlib.Path(__file__).resolve().parents[1]
FIXTURES_DIR = REPO_ROOT / "tests" / "fixtures" / "logo_10_samples"
ENGINE_SECRET = "test-phase5-engine-secret"

FORBIDDEN_COPY_RE = re.compile(
    r"\b(verified|validated|certified|authentic|guaranteed|guarantee|guarantees|legal\s+certification)\b",
    re.IGNORECASE,
)


class Phase5LogoIntelligenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        os.environ["ENGINE_SERVICE_SECRET"] = ENGINE_SECRET
        os.environ["CHARM_SERVICE_SECRET"] = "test-phase5-charm-secret"
        os.environ["ENVIRONMENT"] = "preview"
        cls.client = TestClient(app)
        cls.headers = {"X-NV-Engine-Secret": ENGINE_SECRET}

    def _assert_zero_forbidden_words(self, obj: object) -> None:
        raw = json.dumps(obj, ensure_ascii=False)
        m = FORBIDDEN_COPY_RE.search(raw)
        self.assertIsNone(m, f"Forbidden copy word found in payload: {m.group(0) if m else ''}")

    def test_01_auth_and_empty_input_validation(self) -> None:
        r_unauth = self.client.post("/api/v1/logo/preview", json={"business_name": "TEST"})
        self.assertEqual(r_unauth.status_code, 403)

        for ep in ("/api/v1/logo/preview", "/api/v1/logo/analyze-existing", "/api/v1/logo/five-layer-evaluate"):
            r_empty = self.client.post(ep, json={}, headers=self.headers)
            self.assertEqual(r_empty.status_code, 400, f"Expected 400 on empty input for {ep}")

    def test_02_de_wow_wafel_compound_51_root_6_and_png_ocr(self) -> None:
        r_prev = self.client.post(
            "/api/v1/logo/preview",
            json={
                "business_name": "DE WOW WAFEL",
                "symbol_concept": "sacred_lotus",
                "primary_color": "#16835B",
                "accent_color": "#8B6914",
                "bg_color": "#FFFDF7",
            },
            headers=self.headers,
        )
        self.assertEqual(r_prev.status_code, 200)
        body = r_prev.json()
        self.assertEqual(body["name_numerology"]["compound_number"], 51)
        self.assertEqual(body["name_numerology"]["root_number"], 6)
        self._assert_zero_forbidden_words(body)

        # Also test PNG upload OCR on `09_de_wow_wafel_demo.png`
        png_bytes = (FIXTURES_DIR / "09_de_wow_wafel_demo.png").read_bytes()
        r_png = self.client.post(
            "/api/v1/logo/analyze-existing",
            files={"file": ("09_de_wow_wafel_demo.png", png_bytes, "image/png")},
            headers=self.headers,
        )
        self.assertEqual(r_png.status_code, 200)
        png_body = r_png.json()
        self.assertEqual(png_body["upload_reading"]["extracted_text"], "DE WOW WAFEL")
        self.assertGreaterEqual(png_body["upload_reading"]["text_confidence"], 0.75)
        self.assertEqual(png_body["four_results"]["name_intelligence"]["compound_number"], 51)
        self.assertEqual(png_body["four_results"]["name_intelligence"]["root_number"], 6)

    def test_03_gold_c9a227_on_fffdf7_measures_2_38_and_fails(self) -> None:
        r_prev = self.client.post(
            "/api/v1/logo/preview",
            json={
                "business_name": "AURA PEAK",
                "symbol_concept": "ascending_peak",
                "primary_color": "#C9A227",
                "accent_color": "#C9A227",
                "bg_color": "#FFFDF7",
            },
            headers=self.headers,
        )
        self.assertEqual(r_prev.status_code, 200)
        body = r_prev.json()
        self.assertEqual(body["contrast_ratio"], 2.38)
        self.assertFalse(body["contrast_passed"])
        gate_map = {g["gate_id"]: g for g in body["hard_gates"]}
        self.assertFalse(gate_map["contrast_threshold"]["passed"])

    def test_04_stencil_cut_letter_svg_fails_nothing_cut_gate(self) -> None:
        svg_4 = (FIXTURES_DIR / "04_apex_stencil_cut_letters.svg").read_text(encoding="utf-8")
        r = self.client.post(
            "/api/v1/logo/analyze-existing",
            json={"svg_content": svg_4, "business_name": "APEX FORGE"},
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200)
        body = r.json()
        gate_map = {g["gate_id"]: g for g in body["hard_gates"]}
        self.assertFalse(gate_map["nothing_cut"]["passed"])

    def test_05_all_10_real_logos_end_to_end_and_deterministic(self) -> None:
        sample_files = sorted(FIXTURES_DIR.glob("[0-9][0-9]_*"))
        self.assertEqual(len(sample_files), 10)

        for fp in sample_files:
            raw = fp.read_bytes()
            if fp.suffix.lower() == ".svg":
                payload = {"svg_content": raw.decode("utf-8")}
            else:
                payload = {"image_base64": base64.b64encode(raw).decode("ascii"), "filename": fp.name}

            r1 = self.client.post("/api/v1/logo/analyze-existing", json=payload, headers=self.headers)
            r2 = self.client.post("/api/v1/logo/analyze-existing", json=payload, headers=self.headers)
            self.assertEqual(r1.status_code, 200, f"Failed on {fp.name}: {r1.text}")
            self.assertEqual(r1.json(), r2.json(), f"Non-deterministic output on {fp.name}")
            data = r1.json()
            self.assertEqual(len(data["hard_gates"]), 9)
            self.assertEqual(
                set(data["four_results"].keys()),
                {"visual_quality", "brand_fit", "name_intelligence", "traditional_alignment"},
            )
            self.assertNotIn("overall_score", data)
            self.assertNotIn("blended_score", data)
            self._assert_zero_forbidden_words(data)

            # Specific fixture edge assertions
            gmap = {g["gate_id"]: g for g in data["hard_gates"]}
            if fp.name == "03_aura_peak_gold_low_contrast.svg":
                self.assertEqual(data["measurable_findings"]["wcag_contrast_estimate"], 2.38)
                self.assertFalse(gmap["contrast_threshold"]["passed"])
            elif fp.name == "04_apex_stencil_cut_letters.svg":
                self.assertFalse(gmap["nothing_cut"]["passed"])
            elif fp.name == "05_fake_vector_raster_and_script.svg":
                self.assertFalse(data["measurable_findings"]["is_vector"])
                self.assertFalse(gmap["vector_integrity"]["passed"])
            elif fp.name == "10_tiny_32px_favicon.png":
                self.assertFalse(gmap["app_icon_legibility"]["passed"])

    def test_06_jpeg_and_pdf_uploads_plus_user_confidence_override(self) -> None:
        # 1. JPEG upload
        img = Image.new("RGB", (600, 300), (255, 253, 247))
        draw = ImageDraw.Draw(img)
        draw.rectangle((80, 80, 200, 200), fill=(82, 62, 40))
        jpg_buf = io.BytesIO()
        img.save(jpg_buf, format="JPEG", quality=95)
        r_jpg = self.client.post(
            "/api/v1/logo/analyze-existing",
            files={"file": ("brand_test.jpg", jpg_buf.getvalue(), "image/jpeg")},
            data={"confirmed_text": "SURYA KRAFT", "confirmed_primary_color": "#523E28"},
            headers=self.headers,
        )
        self.assertEqual(r_jpg.status_code, 200)
        jbody = r_jpg.json()
        self.assertEqual(jbody["upload_reading"]["format"], "JPEG")
        self.assertEqual(jbody["upload_reading"]["extracted_text"], "SURYA KRAFT")
        self.assertEqual(jbody["upload_reading"]["text_confidence"], 1.0)
        self.assertTrue(jbody["upload_reading"]["user_corrected"])

        # 2. Pure vector PDF upload
        pdf_doc = pymupdf.open()
        page = pdf_doc.new_page(width=600, height=300)
        page.draw_rect(pymupdf.Rect(0, 0, 600, 300), color=None, fill=(1.0, 0.992, 0.968))
        page.draw_circle(pymupdf.Point(120, 150), 55, color=(0.086, 0.514, 0.357), width=6)
        page.insert_text(pymupdf.Point(210, 162), "DE WOW WAFEL", fontsize=32, color=(0.086, 0.514, 0.357))
        pdf_bytes = pdf_doc.tobytes()
        pdf_doc.close()

        r_pdf = self.client.post(
            "/api/v1/logo/analyze-existing",
            files={"file": ("de_wow_wafel.pdf", pdf_bytes, "application/pdf")},
            headers=self.headers,
        )
        self.assertEqual(r_pdf.status_code, 200)
        pbody = r_pdf.json()
        self.assertEqual(pbody["upload_reading"]["format"], "PDF")
        self.assertEqual(pbody["upload_reading"]["extracted_text"], "DE WOW WAFEL")
        self.assertEqual(pbody["four_results"]["name_intelligence"]["compound_number"], 51)
        self.assertEqual(pbody["four_results"]["name_intelligence"]["root_number"], 6)

    def test_07_partner_reconciliation_consent_and_charm_non_interference(self) -> None:
        # Missing consent with DOB -> 400
        r_noconsent = self.client.post(
            "/api/v1/logo/five-layer-evaluate",
            json={"business_name": "PRANA LABS", "owner_dob": "1981-11-28", "dpdp_consent": False},
            headers=self.headers,
        )
        self.assertEqual(r_noconsent.status_code, 400)

        # > 4 active partners -> 400
        r_too_many = self.client.post(
            "/api/v1/logo/five-layer-evaluate",
            json={
                "business_name": "PRANA LABS",
                "owner_dob": "1981-11-28",
                "dpdp_consent": True,
                "partners": [{"name": f"P{i}", "dob": "1990-01-01"} for i in range(5)],
            },
            headers=self.headers,
        )
        self.assertEqual(r_too_many.status_code, 400)

        # Owner + 4 active partners + Charm astrology non-interference check
        base_req = {
            "business_name": "DE WOW WAFEL",
            "business_category": "hospitality_food",
            "business_activity": "Artisan freshly baked waffles and beverages",
            "product_function": "Warm gourmet dessert hospitality",
            "customer_outcome": "Joyful family dining warmth",
            "market_region": "INDIA",
            "price_position": "mid",
            "brand_stage": "startup",
            "brand_personality": ["care", "warmth", "modern"],
            "owner_name": "Owner One",
            "owner_dob": "1981-11-28",  # Driver 1, Conductor 4 (never 22!)
            "partners": [
                {"name": "Partner A", "dob": "1991-11-29"},  # Driver 2, Conductor 6 (never 11/33!)
                {"name": "Partner B", "dob": "1988-05-14"},  # Driver 5, Conductor 9
                {"name": "Partner C", "dob": "1992-07-14"},  # Driver 5, Conductor 6
                {"name": "Partner D", "dob": "1985-03-21"},  # Driver 3, Conductor 2
            ],
            "dpdp_consent": True,
            "reference_date": "2026-11-08",
        }
        r_no_astro = self.client.post("/api/v1/logo/five-layer-evaluate", json=base_req, headers=self.headers)
        self.assertEqual(r_no_astro.status_code, 200)
        b1 = r_no_astro.json()

        with_astro = dict(base_req, owner_birth_time="09:30", owner_birth_lat=28.6139, owner_birth_lon=77.2090)
        r_astro = self.client.post("/api/v1/logo/five-layer-evaluate", json=with_astro, headers=self.headers)
        self.assertEqual(r_astro.status_code, 200)
        b2 = r_astro.json()

        # Verify 1..9 single-digit reduction on 28 Nov 1981 & 29 Nov 1991
        profs = b1["layers"]["layer2_partner_profiles"]["profiles"]
        self.assertEqual(len(profs), 5)
        self.assertEqual(profs[0]["driver_number"], 1)
        self.assertEqual(profs[0]["conductor_number"], 4)
        self.assertEqual(profs[1]["driver_number"], 2)
        self.assertEqual(profs[1]["conductor_number"], 6)

        # Verify Charm label is strictly one of the two allowed values and NEVER alters palette/gates/SVG
        self.assertEqual(b1["layers"]["layer3_reconciliation"]["charm_basis_label"], "numerology basis only")
        self.assertIn(
            b2["layers"]["layer3_reconciliation"]["charm_basis_label"],
            {"both systems agree", "numerology basis only"},
        )
        self.assertEqual(
            b1["layers"]["layer3_reconciliation"]["reconciled_palette"],
            b2["layers"]["layer3_reconciliation"]["reconciled_palette"],
        )
        self.assertEqual(b1["svg"], b2["svg"])

        # Verify excluded enemy colours are excluded from reconciled foreground
        rec_pal = b1["layers"]["layer3_reconciliation"]["reconciled_palette"]
        excluded = set(b1["layers"]["layer3_reconciliation"]["partner_colour_matrix"]["excluded_enemy_families"])
        self.assertNotIn(rec_pal["primary"]["colour_family"], excluded)
        self.assertNotIn(rec_pal["accent"]["colour_family"], excluded)

    def test_08_shukla_paksha_nov_2026_verified_9_nov_and_compliant_prices(self) -> None:
        win = calculate_verified_shukla_paksha_window(datetime.date(2026, 11, 8), ruling_root=6)
        self.assertEqual(win["shukla_paksha_start_date"], "2026-11-09")
        self.assertEqual(len(win["three_shukla_paksha_dates"]), 3)
        for dt_item in win["three_shukla_paksha_dates"]:
            self.assertGreaterEqual(dt_item["date"], "2026-11-09")
            self.assertLessEqual(dt_item["date"], win["shukla_paksha_end_date"])
            self.assertIn("Shukla Paksha", dt_item["paksha"])

        r = self.client.post(
            "/api/v1/logo/preview",
            json={"business_name": "DE WOW WAFEL"},
            headers=self.headers,
        )
        tiers = r.json()["paid_tiers"]
        self.assertEqual([t["tier_id"] for t in tiers], ["deep_audit", "rework", "new_logo", "startup_pack"])
        for t in tiers:
            self.assertIn(digit_root(t["offer_price_inr"]), {1, 3, 5, 6})
            self.assertIn(digit_root(t["list_price_inr"]), {1, 3, 5, 6})
            self.assertTrue(t["owner_review_required"])


if __name__ == "__main__":
    unittest.main()
