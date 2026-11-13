# -*- coding: utf-8 -*-
"""
tests/test_phase3_charm_ai.py
=============================
Phase 3 Acceptance & Deterministic Engine Test Suite for Charm AI:
1. Missing day/month/year, invalid calendar date (31 Feb 1990), or missing question -> HTTP 400 with friendly message.
   Zero fallback defaults ('Seeker', 'Is 2026 favorable...', 28/11/1981).
2. Deleted fixed template assertions: no 'early Q2 through late Q3', no 'East or South-East',
   no 'Gold, Warm Amber, and Forest Green', no 'career_event_assessment', no 'VERIFIED'.
3. Exact engine outputs for 28 Nov 1981:
   - driver: 1
   - conductor: 4
   - Lo Shu non-zero counts: 1:4, 2:1, 8:2, 9:1
4. Owner's Personal Year, Month, and Day formulas + accurate meanings (PY 9 never described as 'foundation').
5. Two different questions with two different birth dates produce clearly different, topic-isolated readings.
6. Dasha: omitted completely ('dasha' absent everywhere) unless calculated via pyswisseph (Lahiri ayanamsha)
   with valid birth_time + birth_place.
7. Remedies strictly in owner's order: element_balancing -> planet_remedies -> affirmation, tiered by package.
8. Working stage SSE events ('calculating', 'analysing', 'preparing_reading') emitted on /api/charm/chat/stream.
"""

from __future__ import annotations

import json
import os
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tests.zero_socket_asgi_client import ZeroSocketAsgiClient as TestClient

from app.services.charm_deterministic_service import (
    SWISSEPH_AVAILABLE,
    has_banned_copy,
)
from app.services.internal_engine_service import app as engine_app


class TestPhase3CharmAI(unittest.TestCase):
    def setUp(self) -> None:
        self._orig_env = dict(os.environ)
        os.environ["ENVIRONMENT"] = "preview"
        os.environ["CHARM_SERVICE_SECRET"] = "phase3_unit_test_secret_xyz"
        os.environ["NV_DISABLE_LIVE_LLM"] = "true"
        self.headers = {"X-NV-Charm-Secret": "phase3_unit_test_secret_xyz"}
        self.client = TestClient(engine_app)

    def tearDown(self) -> None:
        os.environ.clear()
        os.environ.update(self._orig_env)

    def test_01_missing_inputs_return_400(self) -> None:
        # Missing birth date completely
        r1 = self.client.post(
            "/api/charm/chat",
            json={"message": "How should I pace my career this year?"},
            headers=self.headers,
        )
        self.assertEqual(r1.status_code, 400)
        d1 = r1.json()
        self.assertEqual(d1["code"], "DOB_REQUIRED")
        self.assertIn("Date of Birth", d1["error"])

        # Partial birth date (missing year)
        r2 = self.client.post(
            "/api/charm/chat",
            json={"message": "How should I pace my career?", "day": 28, "month": 11},
            headers=self.headers,
        )
        self.assertEqual(r2.status_code, 400)

        # Invalid calendar date (31 Feb 1990)
        r3 = self.client.post(
            "/api/charm/chat",
            json={"message": "How should I pace my career?", "day": 31, "month": 2, "year": 1990},
            headers=self.headers,
        )
        self.assertEqual(r3.status_code, 400)
        self.assertEqual(r3.json()["code"], "INVALID_DOB")

        # Missing question
        r4 = self.client.post(
            "/api/charm/chat",
            json={"message": "   ", "day": 28, "month": 11, "year": 1981},
            headers=self.headers,
        )
        self.assertEqual(r4.status_code, 400)
        self.assertEqual(r4.json()["code"], "QUESTION_REQUIRED")

        # Stream endpoint also returns 400 on missing DOB
        r5 = self.client.post(
            "/api/charm/chat/stream",
            json={"message": "Marriage question"},
            headers=self.headers,
        )
        self.assertEqual(r5.status_code, 400)

    def test_02_28_nov_1981_engine_outputs_and_no_verified_or_legacy_template(self) -> None:
        resp = self.client.post(
            "/api/charm/chat",
            json={
                "message": "What do my numbers indicate for career and leadership responsibilities?",
                "day": 28,
                "month": 11,
                "year": 1981,
                "target_date": "2026-11-14",
            },
            headers=self.headers,
        )
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        raw_json = json.dumps(data, ensure_ascii=False)

        # Acceptance: 28 Nov 1981 -> driver 1, conductor 4, Lo Shu 1:4, 2:1, 8:2, 9:1
        eng = data["engine_outputs"]
        self.assertEqual(eng["driver"], 1)
        self.assertEqual(eng["conductor"], 4)
        self.assertEqual(eng["loshu_nonzero_counts"], {"1": 4, "2": 1, "8": 2, "9": 1})
        self.assertEqual(eng["driver_conductor_81"]["key"], "1_4")

        # Acceptance: No reply contains "VERIFIED" or any banned word / legacy template phrase
        self.assertNotIn("VERIFIED", raw_json.upper())
        self.assertFalse(has_banned_copy(data["assistant_message"]["text"]))
        self.assertNotIn("early Q2 through late Q3", raw_json)
        self.assertNotIn("East or South-East", raw_json)
        self.assertNotIn("Gold, Warm Amber, and Forest Green", raw_json)
        self.assertNotIn("career_event_assessment", raw_json)
        self.assertNotIn("Seeker", raw_json)

        # Without birth_time & birth_place, zero mention of dasha anywhere
        self.assertNotIn("dasha", raw_json.lower())

    def test_03_personal_year_month_day_formulas_and_py9_not_foundation(self) -> None:
        # 07-09-1980 on 2026-01-17 -> PY = digit_root(0+7+0+9+2+0+2+6=26)=8, PM = digit_root(8+1)=9, PD = digit_root(8+9+1+7+0+1+2+0+2+6=36)=9
        r_a = self.client.post(
            "/api/charm/chat",
            json={
                "message": "How should I manage my monthly money and savings budget?",
                "day": 7,
                "month": 9,
                "year": 1980,
                "target_date": "2026-01-17",
            },
            headers=self.headers,
        )
        self.assertEqual(r_a.status_code, 200)
        pc_a = r_a.json()["engine_outputs"]["personal_cycles"]
        self.assertEqual(pc_a["personal_year"], 8)
        self.assertEqual(pc_a["personal_month"], 9)
        self.assertEqual(pc_a["personal_day"], 9)

        # PY = 9 case: 09-09-1990 in 2026 -> 0+9+0+9+2+0+2+6 = 28 -> 1? Wait: 08-09-1990 in 2026 -> 8+9+2+0+2+6 = 27 -> PY = 9!
        r_py9 = self.client.post(
            "/api/charm/chat",
            json={
                "message": "What does my Personal Year indicate for career?",
                "day": 8,
                "month": 9,
                "year": 1990,
                "target_date": "2026-11-14",
            },
            headers=self.headers,
        )
        self.assertEqual(r_py9.status_code, 200)
        d_py9 = r_py9.json()
        self.assertEqual(d_py9["engine_outputs"]["personal_cycles"]["personal_year"], 9)
        self.assertNotIn("foundation", d_py9["engine_outputs"]["personal_cycles"]["personal_year_theme"].lower())
        self.assertNotIn("foundation", d_py9["assistant_message"]["text"].lower())
        self.assertIn("completion", d_py9["assistant_message"]["text"].lower())

    def test_04_two_different_questions_and_dobs_produce_distinct_topic_isolated_readings(self) -> None:
        r_marriage = self.client.post(
            "/api/charm/chat",
            json={
                "message": "How do my numbers shape marriage harmony and household communication?",
                "day": 14,
                "month": 7,
                "year": 1992,
                "target_date": "2026-11-14",
            },
            headers=self.headers,
        )
        r_property = self.client.post(
            "/api/charm/chat",
            json={
                "message": "What should I check before buying a flat or reviewing house numbers?",
                "day": 28,
                "month": 11,
                "year": 1981,
                "target_date": "2026-11-14",
            },
            headers=self.headers,
        )
        self.assertEqual(r_marriage.status_code, 200)
        self.assertEqual(r_property.status_code, 200)
        m_data = r_marriage.json()
        p_data = r_property.json()

        self.assertEqual(m_data["topic"], "marriage")
        self.assertEqual(p_data["topic"], "property")
        self.assertNotEqual(m_data["assistant_message"]["text"], p_data["assistant_message"]["text"])
        self.assertNotEqual(m_data["engine_outputs"]["driver"], p_data["engine_outputs"]["driver"])
        self.assertIn("marriage", m_data["assistant_message"]["text"].lower())
        self.assertNotIn("career", m_data["assistant_message"]["text"].lower())
        self.assertIn("property", p_data["assistant_message"]["text"].lower())

    def test_05_remedies_order_and_package_tiering_plus_lahiri_dasha(self) -> None:
        r_free = self.client.post(
            "/api/charm/chat",
            json={
                "message": "How can I keep steady career focus?",
                "day": 28,
                "month": 11,
                "year": 1981,
                "_charm_entitlement": "charm_free",
            },
            headers=self.headers,
        )
        r_prem = self.client.post(
            "/api/charm/chat",
            json={
                "message": "How can I keep steady career focus?",
                "day": 28,
                "month": 11,
                "year": 1981,
                "birth_time": "09:30",
                "birth_place": "New Delhi",
                "_charm_entitlement": "charm_premium",
            },
            headers=self.headers,
        )
        self.assertEqual(r_free.status_code, 200)
        self.assertEqual(r_prem.status_code, 200)
        d_free = r_free.json()
        d_prem = r_prem.json()

        self.assertEqual(d_free["remedies"]["order"], ["element_balancing", "planet_remedies", "affirmation"])
        self.assertEqual(d_prem["remedies"]["order"], ["element_balancing", "planet_remedies", "affirmation"])
        self.assertGreater(len(d_prem["remedies"]["planet_remedies"]), len(d_free["remedies"]["planet_remedies"]))

        # Verify order in rendered markdown text: Element Balancing before Planet Remedies before Affirmation
        txt = d_prem["assistant_message"]["text"]
        i_elem = txt.index("1. **Element Balancing:**")
        i_plan = txt.index("2. **Planet Remedies:**")
        i_aff = txt.index("3. **Affirmation:**")
        self.assertLess(i_elem, i_plan)
        self.assertLess(i_plan, i_aff)

        if SWISSEPH_AVAILABLE:
            self.assertIn("dasha", d_prem["engine_outputs"])
            self.assertIn("Lahiri", d_prem["engine_outputs"]["dasha"]["method"])
            self.assertNotIn("VERIFIED", json.dumps(d_prem).upper())

    def test_06_sse_stream_emits_working_stages_and_result(self) -> None:
        resp = self.client.post(
            "/api/charm/chat/stream",
            json={
                "message": "What do my numbers indicate for study and exam preparation?",
                "day": 19,
                "month": 5,
                "year": 1995,
            },
            headers=self.headers,
        )
        self.assertEqual(resp.status_code, 200)
        body_text = resp.text
        self.assertIn("event: stage", body_text)
        self.assertIn("calculating", body_text)
        self.assertIn("analysing", body_text)
        self.assertIn("preparing_reading", body_text)
        self.assertIn("event: result", body_text)
        self.assertNotIn("VERIFIED", body_text.upper())


if __name__ == "__main__":
    unittest.main()
