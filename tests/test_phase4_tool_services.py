# -*- coding: utf-8 -*-
"""
tests/test_phase4_tool_services.py
==================================
Unit & ASGI contract tests for Phase 4 Deterministic Tool Services (`numeros-engine`).
Verifies:
1. Shared-secret header authentication (`X-NV-Engine-Secret`).
2. All 10 endpoints return HTTP 200 with deterministic known-answer outputs.
3. Empty and invalid inputs across all 10 endpoints return HTTP 400 with plain messages.
4. Every result carries explicit provenance labels (`calculated`, `traditional rule`, `not configured`).
5. Single-digit 1..9 reduction everywhere (no 11, 22, 33 roots) and compliant pricing (510->6, 1020->3).
6. Zero forbidden words (`verified`, `validated`, `certified`, `authentic`, `guaranteed`, `legal certification`).
"""

from __future__ import annotations

import json
import os
import re
import unittest
from typing import Any, Dict

from app.engine.digit_root import digit_root
from app.services.internal_engine_service import app
from tests.zero_socket_asgi_client import ZeroSocketAsgiClient

FORBIDDEN_WORDS_RE = re.compile(
    r"\b(verified|validated|certified|authentic|guaranteed|guarantee|guarantees|legal\s+certification)\b",
    re.IGNORECASE,
)

ALLOWED_PROVENANCE_BASES = {"calculated", "traditional rule", "not configured"}


class Phase4ToolServicesTests(unittest.TestCase):
    def setUp(self) -> None:
        self._prev_env = os.environ.get("ENVIRONMENT")
        self._prev_secret = os.environ.get("ENGINE_SERVICE_SECRET")
        self._prev_local = os.environ.get("NV_ALLOW_UNAUTHENTICATED_LOCAL")
        os.environ["ENVIRONMENT"] = "preview"
        os.environ["ENGINE_SERVICE_SECRET"] = "test_phase4_engine_secret_hex"
        os.environ["NV_ALLOW_UNAUTHENTICATED_LOCAL"] = "false"
        self.client = ZeroSocketAsgiClient(app)
        self.headers = {"X-NV-Engine-Secret": "test_phase4_engine_secret_hex"}

    def tearDown(self) -> None:
        for k, prev in (
            ("ENVIRONMENT", self._prev_env),
            ("ENGINE_SERVICE_SECRET", self._prev_secret),
            ("NV_ALLOW_UNAUTHENTICATED_LOCAL", self._prev_local),
        ):
            if prev is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = prev

    def _assert_clean_and_provenanced(self, payload: Dict[str, Any]) -> None:
        serialized = json.dumps(payload, ensure_ascii=False)
        m = FORBIDDEN_WORDS_RE.search(serialized)
        self.assertIsNone(m, f"Forbidden word '{m.group(0) if m else ''}' found in payload: {serialized[:400]}")
        prov = payload.get("provenance_lines")
        self.assertIsInstance(prov, list)
        self.assertGreaterEqual(len(prov), 2)
        for row in prov:
            self.assertIn(row.get("basis"), ALLOWED_PROVENANCE_BASES)
            self.assertTrue(row.get("label"))
            self.assertTrue(row.get("detail"))

    def test_00_engine_secret_enforcement(self) -> None:
        r_missing = self.client.post("/api/v2/numerology/name/balance", json={"full_name": "Arjun", "dob_str": "1981-11-28"})
        self.assertEqual(r_missing.status_code, 403)
        r_wrong = self.client.post(
            "/api/v2/numerology/name/balance",
            json={"full_name": "Arjun", "dob_str": "1981-11-28"},
            headers={"X-NV-Engine-Secret": "wrong_secret"},
        )
        self.assertEqual(r_wrong.status_code, 403)

    def test_01_name_balance_known_and_400(self) -> None:
        # 28 Nov 1981 -> Driver 1, Conductor 4; 'DE WOW WAFEL' -> Chaldean 51 -> Root 6
        r = self.client.post(
            "/api/v2/numerology/name/balance",
            json={"full_name": "DE WOW WAFEL", "dob_str": "1981-11-28"},
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        data = r.json()
        self._assert_clean_and_provenanced(data)
        self.assertEqual(data["calculated_driver"], 1)
        self.assertEqual(data["calculated_conductor"], 4)
        seg = data["current_name_evaluation"]["segment_analysis"]
        self.assertEqual(seg["full_compound"], 51)
        self.assertEqual(seg["full_root"], 6)
        self.assertIn("is_aligned", data)

        # Empty / invalid -> 400
        self.assertEqual(self.client.post("/api/v2/numerology/name/balance", json={}, headers=self.headers).status_code, 400)
        self.assertEqual(
            self.client.post(
                "/api/v2/numerology/name/balance",
                json={"full_name": "12345", "dob_str": "1981-11-28"},
                headers=self.headers,
            ).status_code,
            400,
        )
        self.assertEqual(
            self.client.post(
                "/api/v2/numerology/name/balance",
                json={"full_name": "Arjun", "dob_str": "1981-02-31"},
                headers=self.headers,
            ).status_code,
            400,
        )

    def test_02_synastry_known_and_400(self) -> None:
        # 29 Nov 1991 (sum 33 -> Bhagyank 6, never 33) + 28 Nov 1981 (Driver 1, Bhagyank 4)
        r = self.client.post(
            "/api/v2/numerology/relationships/synastry",
            json={
                "person1_name": "Arjun Sharma",
                "p1_day": 28,
                "p1_month": 11,
                "p1_year": 1981,
                "person2_name": "Meera Nair",
                "p2_day": 29,
                "p2_month": 11,
                "p2_year": 1991,
            },
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        data = r.json()
        self._assert_clean_and_provenanced(data)
        rep = data["synastry_report"]
        self.assertEqual(rep["person_1"]["driver"], 1)
        self.assertEqual(rep["person_1"]["conductor"], 4)
        self.assertEqual(rep["person_2"]["driver"], 2)  # 2+9=11 -> 2 (never 11)
        self.assertEqual(rep["person_2"]["conductor"], 6)  # 33 -> 6 (never 33)
        self.assertEqual(rep["compatibility_score_pct"], rep["compatibility_score_percentage"])
        self.assertEqual(rep["overall_verdict"], rep["verdict"])
        self.assertTrue(rep["communication_dynamic"])

        self.assertEqual(
            self.client.post("/api/v2/numerology/relationships/synastry", json={}, headers=self.headers).status_code, 400
        )

    def test_03_mobile_known_and_400(self) -> None:
        # 9876543210 -> sum 45 -> root 9; without driver/conductor -> 'not configured'
        r = self.client.post(
            "/api/v2/numerology/assets/mobile",
            json={"mobile_number": "9876543210"},
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        data = r.json()
        self._assert_clean_and_provenanced(data)
        audit = data["mobile_audit"]
        self.assertEqual(audit["total_compound"], 45)
        self.assertEqual(audit["total_root"], 9)
        self.assertEqual(audit["driver_compatibility"], "not configured")
        self.assertEqual(audit["conductor_compatibility"], "not configured")

        # With driver=1, conductor=4 -> evaluated
        r2 = self.client.post(
            "/api/v2/numerology/assets/mobile",
            json={"mobile_number": "9876543210", "driver": 1, "conductor": 4},
            headers=self.headers,
        )
        self.assertEqual(r2.status_code, 200)
        self.assertNotEqual(r2.json()["mobile_audit"]["driver_compatibility"], "not configured")

        self.assertEqual(self.client.post("/api/v2/numerology/assets/mobile", json={}, headers=self.headers).status_code, 400)
        self.assertEqual(
            self.client.post("/api/v2/numerology/assets/mobile", json={"mobile_number": "123"}, headers=self.headers).status_code,
            400,
        )

    def test_04_vehicle_known_and_400(self) -> None:
        # MH12AB1234 -> M(4)+H(5)+A(1)+B(2)=12, digits 1+2+1+2+3+4=13 -> total 25 -> root 7; running 1234 -> 10 -> 1
        r = self.client.post(
            "/api/v2/numerology/assets/vehicle",
            json={"registration_plate": "MH 12 AB 1234", "driver": 1, "conductor": 4},
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        data = r.json()
        self._assert_clean_and_provenanced(data)
        v = data["vehicle_audit"]
        self.assertEqual(v["full_plate_compound"], 25)
        self.assertEqual(v["full_plate_root"], 7)
        self.assertEqual(v["core_running_root"], 1)

        # Compound 22 test: KA01AA5600 -> K(2)+A(1)+A(1)+A(1)=5, digits 0+1+5+6+0+0=12 (17); let's test plate summing to 22 -> root 4
        # M(4)+H(5)+0+2+A(1)+A(1)+5+4=22 -> root 4 (never 22!)
        r22 = self.client.post(
            "/api/v2/numerology/assets/vehicle",
            json={"registration_plate": "MH02AA5400", "driver": 1, "conductor": 4},
            headers=self.headers,
        )
        self.assertEqual(r22.status_code, 200)
        self.assertEqual(r22.json()["vehicle_audit"]["full_plate_compound"], 22)
        self.assertEqual(r22.json()["vehicle_audit"]["full_plate_root"], 4)

        self.assertEqual(self.client.post("/api/v2/numerology/assets/vehicle", json={}, headers=self.headers).status_code, 400)

    def test_05_property_known_and_400(self) -> None:
        # B-402 -> B(2) + 4 + 0 + 2 = 8 -> root 8
        r = self.client.post(
            "/api/v2/numerology/assets/property",
            json={"property_identifier": "B-402", "driver": 1, "conductor": 4},
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        data = r.json()
        self._assert_clean_and_provenanced(data)
        p = data["property_audit"]
        self.assertEqual(p["property_root"], 8)
        self.assertEqual(p["property_root_number"], 8)
        self.assertIn("Saturn", p["planet_association"])
        self.assertTrue(p["resident_compatibility"])
        self.assertTrue(p["vastu_sector"])

        self.assertEqual(self.client.post("/api/v2/numerology/assets/property", json={}, headers=self.headers).status_code, 400)

    def test_06_blessing_years_known_and_400(self) -> None:
        r = self.client.post(
            "/api/v2/numerology/forecast/blessing-years",
            json={"day": 28, "month": 11, "year": 1981},
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        data = r.json()
        self._assert_clean_and_provenanced(data)
        by = data["blessing_years"]
        self.assertEqual(by["driver"], 1)
        self.assertEqual(by["conductor"], 4)
        for row in by["full_timeline"]:
            self.assertGreaterEqual(row["personal_year"], 1)
            self.assertLessEqual(row["personal_year"], 9)

        self.assertEqual(
            self.client.post("/api/v2/numerology/forecast/blessing-years", json={}, headers=self.headers).status_code, 400
        )

    def test_07_baby_naming_known_and_400(self) -> None:
        r = self.client.post(
            "/api/v2/numerology/naming/baby",
            json={"baby_driver": 1, "baby_conductor": 5, "gender": "Boy", "starting_letter": "A"},
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        data = r.json()
        self._assert_clean_and_provenanced(data)
        recs = data["baby_name_recommendations"]
        self.assertGreaterEqual(len(recs), 1)
        for rec in recs:
            self.assertTrue(rec["name"].startswith("A"))
            self.assertGreaterEqual(rec["single_root"], 1)
            self.assertLessEqual(rec["single_root"], 9)

        # Unconfigured starting letter 'X' -> empty list + catalog_status='not configured' (never invented names)
        rx = self.client.post(
            "/api/v2/numerology/naming/baby",
            json={"baby_driver": 1, "baby_conductor": 5, "gender": "Boy", "starting_letter": "X"},
            headers=self.headers,
        )
        self.assertEqual(rx.status_code, 200)
        self.assertEqual(rx.json()["baby_name_recommendations"], [])
        self.assertEqual(rx.json()["catalog_status"], "not configured")

        self.assertEqual(self.client.post("/api/v2/numerology/naming/baby", json={}, headers=self.headers).status_code, 400)

    def test_08_professions_recommend_known_and_400(self) -> None:
        r = self.client.post(
            "/api/v2/numerology/professions/recommend",
            json={"driver": 1, "conductor": 4},
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        data = r.json()
        self._assert_clean_and_provenanced(data)
        rec = data["recommendations"]
        self.assertEqual(rec["driver"], 1)
        self.assertEqual(rec["conductor"], 4)
        self.assertIn("suitability_matrix", rec)
        self.assertEqual(rec["kp_tenth_sub_lord_status"], "not configured")

        self.assertEqual(
            self.client.post("/api/v2/numerology/professions/recommend", json={}, headers=self.headers).status_code, 400
        )

    def test_09_business_existing_diagnose_known_and_400(self) -> None:
        r = self.client.post(
            "/api/v1/business/existing-diagnose",
            json={
                "legal_name": "Apex Consulting Private Limited",
                "trading_name": "DE WOW WAFEL",
                "products_services": "Artisanal Belgian waffles and specialty beverages",
                "performance_challenges": ["seasonal footfall", "supplier cash flow"],
                "current_constraints": ["retail store lease", "food safety license"],
                "logo_color_preference": "#C9A227",
            },
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        data = r.json()
        self._assert_clean_and_provenanced(data)
        for req_key in (
            "diagnosis_verdict",
            "legal_breakdown",
            "trading_breakdown",
            "constraints_analysis",
            "brand_and_name_adjustments",
            "practical_improvements_first",
            "traditional_remedies",
            "vastu_and_operational_remedies",
            "protection_layer_status",
            "protection_summary",
            "monetization_gate",
        ):
            self.assertIn(req_key, data)
        self.assertEqual(data["brand_and_name_adjustments"]["trading_name_compound"], 51)
        self.assertEqual(data["brand_and_name_adjustments"]["trading_name_root"], 6)
        mg = data["monetization_gate"]
        self.assertIn(digit_root(mg["entry_price_inr"]), {1, 3, 5, 6})
        self.assertIn(digit_root(mg["anchor_price_inr"]), {1, 3, 5, 6})
        self.assertEqual(mg["checkout_url"], "/pricing/")

        self.assertEqual(
            self.client.post("/api/v1/business/existing-diagnose", json={}, headers=self.headers).status_code, 400
        )

    def test_10_business_startup_evaluate_known_and_400(self) -> None:
        r = self.client.post(
            "/api/v1/business/startup-evaluate",
            json={
                "idea_name": "DE WOW WAFEL",
                "founder_name": "Bhaskr Singh",
                "founder_dob": "1981-11-28",
                "activity_description": "Artisanal dessert cafes and packaged gourmet waffle mixes",
                "customer_segment": "Urban families and students",
                "delivery_channel": "Retail & Direct Delivery",
                "revenue_model": "direct_retail",
                "capital_band": "seed_10k_50k",
                "location": "New Delhi",
                "experience_years": 8,
                "skills": ["operations", "food retail", "branding"],
                "operating_preference": "hands_on_operations",
                "risk_tolerance": "moderate",
            },
            headers=self.headers,
        )
        self.assertEqual(r.status_code, 200, r.text)
        data = r.json()
        self._assert_clean_and_provenanced(data)
        self.assertIn("commercial_viability", data)
        self.assertIn("traditional_alignment", data)
        self.assertEqual(data["traditional_alignment"]["name_compound"], 51)
        self.assertEqual(data["traditional_alignment"]["name_single"], 6)
        mg = data["monetization_gate"]
        self.assertIn(digit_root(mg["entry_price_inr"]), {1, 3, 5, 6})
        self.assertIn(digit_root(mg["anchor_price_inr"]), {1, 3, 5, 6})

        self.assertEqual(
            self.client.post("/api/v1/business/startup-evaluate", json={}, headers=self.headers).status_code, 400
        )


if __name__ == "__main__":
    unittest.main()
