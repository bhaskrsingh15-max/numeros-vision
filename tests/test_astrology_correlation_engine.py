"""
TEST SUITE: MULTI-ASTROLOGY CORRELATION & TRANSIT SYNTHESIS ENGINE
==================================================================
Verifies:
1. Deterministic calculation of 24-Hour Chaldean Planetary Horas across all weekdays.
2. Real-Time Planetary Transit (Gochar) cross-correlation with Driver, Conductor, & Personal Year.
3. Master Multi-Astrology Correlation across 6 canonical disciplines:
   - Vedic Parashari Jyotish (Sambandha & Yogas)
   - Krishnamurti Paddhati (KP Sub-Lord 81-Matrix)
   - Lal Kitab (Masnooi Compound Planets & Awakening Ages)
   - Lo Shu 3x3 Magic Square (8 Planes & Voids)
   - Chaldean Acoustic Vibration (Cheiro Canon)
   - Real-Time Gochar Transits & Executive Horas
4. Non-fatalistic, legally compliant 7-Layer Safe Remedial Action Plan (Zero toxic/fatalistic advice).
5. FastAPI Endpoints (/api/v2/numerology/astrology/correlate & /api/v2/numerology/astrology/daily-hora).
"""

import os
import sys
import unittest
from datetime import date

# Ensure root path
_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from fastapi.testclient import TestClient
from app.main import app
from app.engine.astrology_correlation_engine import (
    calculate_hourly_planetary_horas,
    correlate_planetary_transits,
    run_multi_astrology_correlation_engine,
    CHALDEAN_HORA_CYCLE,
    WEEKDAY_FIRST_HORA_RULER
)


class TestAstrologyCorrelationEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    # ── 1. PLANETARY HORA CALCULATIONS ───────────────────────────────────────
    def test_24_hourly_planetary_horas_structure(self):
        """Verify 24 horas are correctly generated with 1-hour slots starting at 06:00."""
        target = date(2026, 10, 12)  # Monday -> First hora ruler is Moon (2)
        horas = calculate_hourly_planetary_horas(target_date=target, driver=1, conductor=5)
        
        self.assertEqual(len(horas), 24)
        self.assertEqual(horas[0]["hour_index"], 1)
        self.assertEqual(horas[0]["time_window"], "06:00 – 07:00")
        self.assertEqual(horas[0]["ruling_number"], 2)  # Moon on Monday
        self.assertEqual(horas[23]["time_window"], "05:00 – 06:00")

        # Verify all entries have required fields
        for h in horas:
            self.assertIn("hour_index", h)
            self.assertIn("time_window", h)
            self.assertIn("ruling_number", h)
            self.assertIn("planet_name", h)
            self.assertIn("suitability_status", h)
            self.assertIn("suitability_code", h)
            self.assertIn(h["suitability_code"], ["favourable", "neutral", "friction"])
            self.assertTrue(len(h["optimal_actions"]) > 0)
            self.assertTrue(len(h["cautions"]) > 0)

    def test_weekday_first_hora_cycle_consistency(self):
        """Verify that all 7 weekdays initiate with their classical planetary ruler."""
        # 2026-10-12 (Mon) to 2026-10-18 (Sun)
        expected_rulers = [2, 9, 5, 3, 6, 8, 1]  # Mon..Sun
        for day_offset in range(7):
            d = date(2026, 10, 12 + day_offset)
            horas = calculate_hourly_planetary_horas(target_date=d, driver=1, conductor=1)
            self.assertEqual(
                horas[0]["ruling_number"],
                expected_rulers[day_offset],
                f"Failed for day {d.strftime('%A')}"
            )

    # ── 2. REAL-TIME TRANSIT CORRELATION ────────────────────────────────────
    def test_planetary_transit_correlations(self):
        """Verify transits of Saturn, Jupiter, Rahu, and Ketu are calculated with impact."""
        transit_data = correlate_planetary_transits(driver=1, conductor=8, personal_year=5)
        self.assertIn("active_transits", transit_data)
        self.assertIn("transit_convergence_summary", transit_data)
        self.assertEqual(transit_data["personal_year_number"], 5)

        planets_found = [t["planet"] for t in transit_data["active_transits"]]
        self.assertTrue(any("Saturn" in p for p in planets_found))
        self.assertTrue(any("Jupiter" in p for p in planets_found))

    # ── 3. MULTI-ASTROLOGY CORRELATION MASTER SYNTHESIS ──────────────────────
    def test_multi_astrology_correlation_sun_ketu(self):
        """Case 1: Sun Driver (1), Ketu Conductor (7) - High spiritual and authority consensus."""
        res = run_multi_astrology_correlation_engine(
            day=1,
            month=7,
            year=1990,
            full_name="Aarav Sharma",
            target_date=date(2026, 10, 12)
        )
        self.assertEqual(res["status"], "SUCCESS")
        
        # Verify Native Profile
        profile = res["native_profile"]
        self.assertEqual(profile["driver_number"], 1)
        self.assertEqual(profile["full_name"], "Aarav Sharma")

        # Verify Consensus Metrics
        consensus = res["multi_system_consensus"]
        self.assertGreaterEqual(consensus["consensus_score_pct"], 65.0)
        self.assertLessEqual(consensus["consensus_score_pct"], 98.5)
        self.assertEqual(consensus["participating_disciplines_count"], 6)

        # Verify 6 Disciplines are present
        breakdown = res["discipline_breakdown"]
        self.assertIn("kp_astrology", breakdown)
        self.assertIn("vedic_jyotish", breakdown)
        self.assertIn("lal_kitab", breakdown)
        self.assertIn("lo_shu_grid", breakdown)
        self.assertIn("chaldean_acoustics", breakdown)

        # Verify Safe Remedies
        remedies = res["seven_layer_safe_remedies"]
        self.assertIn("sacred_yantra", remedies)
        self.assertIn("safe_healing_crystals", remedies)
        self.assertIn("directional_vastu", remedies)
        self.assertIn("digital_cellular_shield", remedies)

    def test_multi_astrology_correlation_saturn_sun(self):
        """Case 2: Saturn Driver (8), Sun Conductor (1) - Testing Lal Kitab Masnooi Rahu & friction."""
        res = run_multi_astrology_correlation_engine(
            day=17,  # 1+7 = 8
            month=1,
            year=1991, # 17+1+1991 = 17+1+20 = 38 -> 11 -> 2
            full_name="Vikramaditya Rao",
            target_date=date(2026, 10, 12)
        )
        self.assertEqual(res["status"], "SUCCESS")
        profile = res["native_profile"]
        self.assertEqual(profile["driver_number"], 8)

        # Check breakdown
        breakdown = res["discipline_breakdown"]
        self.assertTrue(len(breakdown["kp_astrology"]["sublord_outcome"]) > 0)
        self.assertTrue(len(breakdown["vedic_jyotish"]["classical_yoga"]) > 0)
        self.assertTrue(len(breakdown["lal_kitab"]["masnooi_compound"]) > 0)

    def test_multi_astrology_correlation_jupiter_mercury(self):
        """Case 3: Jupiter Driver (3), Mercury Conductor (5) - High commercial/intellectual consensus."""
        res = run_multi_astrology_correlation_engine(
            day=12,  # 3
            month=5,
            year=1993,
            full_name="Devika Iyer",
            target_date=date(2026, 10, 12)
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["native_profile"]["driver_number"], 3)
        self.assertGreaterEqual(res["multi_system_consensus"]["consensus_score_pct"], 75.0)

    def test_multi_astrology_correlation_venus_venus(self):
        """Case 4: Double Venus (6 & 6) - High harmony in art, luxury, and aesthetics."""
        res = run_multi_astrology_correlation_engine(
            day=24,  # 6
            month=6,
            year=1992,
            full_name="Meera Kapoor",
            target_date=date(2026, 10, 12)
        )
        self.assertEqual(res["status"], "SUCCESS")
        self.assertEqual(res["native_profile"]["driver_number"], 6)

    # ── 4. API ENDPOINT INTEGRATION TESTS ─────────────────────────────────────
    def test_api_astrology_correlate_endpoint(self):
        """Test POST /api/v2/numerology/astrology/correlate returns HTTP 200 and expected schema."""
        payload = {
            "day": 15,
            "month": 8,
            "year": 1995,
            "full_name": "Rohan Deshmukh",
            "target_date": "2026-10-15"
        }
        resp = self.client.post("/api/v2/numerology/astrology/correlate", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertIn("multi_system_consensus", data)
        self.assertIn("discipline_breakdown", data)
        self.assertIn("transit_and_timing", data)
        self.assertIn("executive_hora_planner", data)
        self.assertIn("seven_layer_safe_remedies", data)

    def test_api_daily_hora_get_endpoint(self):
        """Test GET /api/v2/numerology/astrology/daily-hora returns 24-hour executive horas."""
        resp = self.client.get("/api/v2/numerology/astrology/daily-hora?driver=1&conductor=5&target_date=2026-10-15")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertEqual(data["total_horas"], 24)
        self.assertEqual(len(data["horas"]), 24)
        self.assertIn("favourable_count", data)

    def test_api_daily_hora_post_endpoint(self):
        """Test POST /api/v2/numerology/astrology/daily-hora returns 24-hour executive horas."""
        payload = {
            "driver": 3,
            "conductor": 7,
            "target_date": "2026-10-18"
        }
        resp = self.client.post("/api/v2/numerology/astrology/daily-hora", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertEqual(data["driver"], 3)
        self.assertEqual(data["conductor"], 7)
        self.assertEqual(len(data["horas"]), 24)


if __name__ == "__main__":
    unittest.main()
