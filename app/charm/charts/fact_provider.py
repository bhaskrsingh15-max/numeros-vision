"""
app/charm/charts/fact_provider.py
==================================
Deterministic Planetary & Astronomical Fact Provider.
Complies with Section 5.2 of Master Specification v2.0.
"""

from datetime import date, datetime
import math
from typing import Dict, Any, List, Optional, Tuple
from pydantic import BaseModel, Field

# High-Precision Astronomical Reference Ephemeris Constants (Lahiri Chitra Paksha Ayanamsha)
AYANAMSHA_LAHIRI_2026 = 24.2250  # degrees

CITY_COORDINATES = {
    "delhi": (28.6139, 77.2090, "Asia/Kolkata"),
    "mumbai": (19.0760, 72.8777, "Asia/Kolkata"),
    "bangalore": (12.9716, 77.5946, "Asia/Kolkata"),
    "bengaluru": (12.9716, 77.5946, "Asia/Kolkata"),
    "hyderabad": (17.3850, 78.4867, "Asia/Kolkata"),
    "chennai": (13.0827, 80.2707, "Asia/Kolkata"),
    "kolkata": (22.5726, 88.3639, "Asia/Kolkata"),
    "pune": (18.5204, 73.8567, "Asia/Kolkata"),
    "dubai": (25.2048, 55.2708, "Asia/Dubai"),
    "london": (51.5074, -0.1278, "Europe/London"),
    "new york": (40.7128, -74.0060, "America/New_York"),
    "singapore": (1.3521, 103.8198, "Asia/Singapore")
}

# 2026 Real-Time Transit Coordinates (Degrees in Zodiac 0-360) with Vakri/Retrograde & Lordships
TRANSIT_POSITIONS_2026 = {
    "Saturn": {
        "sign": "Pisces (Meena)",
        "degree": 332.5,
        "house_from_aries": 12,
        "is_retrograde": False,
        "motion_state": "DIRECT (Margi)",
        "sign_lord": "Jupiter (Guru)",
        "nakshatra": "Uttara Bhadrapada",
        "ingress_epoch": "2025-03-29T18:30:00Z",
        "house_lord_activation": "Ruler of 10th and 11th natural houses; activates career discipline, structural reform, and institutional endurance."
    },
    "Jupiter": {
        "sign": "Taurus / Gemini (Vrishabha / Mithuna)",
        "degree": 58.2,
        "house_from_aries": 2,
        "is_retrograde": False,
        "motion_state": "DIRECT (Margi)",
        "sign_lord": "Venus / Mercury",
        "nakshatra": "Rohini / Mrigashira",
        "ingress_epoch": "2025-05-14T12:00:00Z",
        "house_lord_activation": "Ruler of 9th and 12th natural houses; activates higher knowledge, ethical finance, and international expansion."
    },
    "Rahu": {
        "sign": "Aquarius (Kumbha)",
        "degree": 314.0,
        "house_from_aries": 11,
        "is_retrograde": True,
        "motion_state": "RETROGRADE (Vakri)",
        "sign_lord": "Saturn (Shani)",
        "nakshatra": "Shatabhisha",
        "ingress_epoch": "2025-05-18T10:15:00Z",
        "house_lord_activation": "Amplifies non-linear technologies, artificial intelligence innovation, and unconventional networking channels."
    },
    "Ketu": {
        "sign": "Leo (Simha)",
        "degree": 134.0,
        "house_from_aries": 5,
        "is_retrograde": True,
        "motion_state": "RETROGRADE (Vakri)",
        "sign_lord": "Sun (Surya)",
        "nakshatra": "Purva Phalguni",
        "ingress_epoch": "2025-05-18T10:15:00Z",
        "house_lord_activation": "Surgical root-cause precision, inner contemplative detachment, and audit of institutional hierarchies."
    },
    "Sun": {
        "sign": "Libra (Tula)",
        "degree": 185.0,
        "house_from_aries": 7,
        "is_retrograde": False,
        "motion_state": "DIRECT (Margi)",
        "sign_lord": "Venus (Shukra)",
        "nakshatra": "Chitra / Swati",
        "ingress_epoch": "2026-10-17T06:00:00Z",
        "house_lord_activation": "Focuses executive energy on collaborative alliances, commercial partnerships, and contractual agreements."
    },
    "Mars": {
        "sign": "Cancer (Karka)",
        "degree": 98.4,
        "house_from_aries": 4,
        "is_retrograde": False,
        "motion_state": "DIRECT (Margi)",
        "sign_lord": "Moon (Chandra)",
        "nakshatra": "Pushya",
        "ingress_epoch": "2026-10-20T04:30:00Z",
        "house_lord_activation": "Drives internal operational restructuring and strategic defense of enterprise assets."
    },
    "Venus": {
        "sign": "Virgo (Kanya)",
        "degree": 162.1,
        "house_from_aries": 6,
        "is_retrograde": False,
        "motion_state": "DIRECT (Margi)",
        "sign_lord": "Mercury (Budh)",
        "nakshatra": "Hasta",
        "ingress_epoch": "2026-10-13T09:00:00Z",
        "house_lord_activation": "Meticulous design refinement, analytical aesthetic evaluation, and service-oriented relationship harmony."
    },
    "Mercury": {
        "sign": "Scorpio (Vrishchika)",
        "degree": 218.6,
        "house_from_aries": 8,
        "is_retrograde": False,
        "motion_state": "DIRECT (Margi)",
        "sign_lord": "Mars (Mangal)",
        "nakshatra": "Anuradha",
        "ingress_epoch": "2026-10-29T14:00:00Z",
        "house_lord_activation": "Deep diagnostic intelligence, investigative business analysis, and forensic risk assessments."
    }
}

# Classical Surya Siddhanta / Brihat Parashara Combustion Limits (Degrees from Sun)
COMBUSTION_LIMITS: Dict[str, Any] = {
    "Moon": 12.0,
    "Mars": 17.0,
    "Mercury": {"direct": 14.0, "retrograde": 12.0},
    "Jupiter": 11.0,
    "Venus": {"direct": 10.0, "retrograde": 8.0},
    "Saturn": 15.0
    # Rahu & Ketu do not combust; they eclipse luminaries
}


def calculate_angular_separation(deg1: float, deg2: float) -> float:
    """Calculates shortest angular separation between two zodiac degrees (0-360)."""
    diff = abs(deg1 - deg2) % 360.0
    return 360.0 - diff if diff > 180.0 else diff


def evaluate_planetary_combustion(
    planet_name: str,
    planet_deg: float,
    sun_deg: float,
    is_retrograde: bool = False
) -> Dict[str, Any]:
    """
    Computes deterministic planetary combustion (Astangata / Asta) relative to Sun.
    Surya Siddhanta Chapter 10 & Brihat Parashara Hora Shastra Chapter 3.
    """
    if planet_name in ("Sun", "Rahu", "Ketu"):
        return {
            "is_combust": False,
            "status": "EXEMPT",
            "combustion_state": "NOT_APPLICABLE",
            "angular_distance_from_sun": 0.0,
            "combustion_threshold": 0.0,
            "deep_combustion": False,
            "signification": "Luminaries / Nodes do not undergo combustion."
        }

    threshold_spec = COMBUSTION_LIMITS.get(planet_name)
    if isinstance(threshold_spec, dict):
        threshold = threshold_spec["retrograde"] if is_retrograde else threshold_spec["direct"]
    elif isinstance(threshold_spec, (int, float)):
        threshold = float(threshold_spec)
    else:
        threshold = 12.0

    angular_dist = round(calculate_angular_separation(planet_deg, sun_deg), 2)
    is_combust = angular_dist <= threshold
    deep_combust = bool(is_combust and angular_dist <= 1.0)

    state = "COMBUST (Astangata / Asta)" if is_combust else "CLEAR (Udaya)"
    short_status = "COMBUST (Astangata)" if is_combust else "CLEAR (Udaya)"
    signification = (
        f"{planet_name} is within {angular_dist}° of Sun (threshold {threshold}°); "
        f"physical significations internalized, advising contemplative inner pacing."
        if is_combust else
        f"{planet_name} is {angular_dist}° from Sun (exceeds {threshold}° threshold); "
        f"radiant outward expression (Udaya)."
    )

    return {
        "is_combust": is_combust,
        "status": short_status,
        "combustion_state": state,
        "angular_distance_from_sun": angular_dist,
        "combustion_threshold": threshold,
        "deep_combustion": deep_combust,
        "signification": signification
    }


class ChartFactSnapshot(BaseModel):
    snapshot_id: str
    target_date: str
    latitude: float
    longitude: float
    timezone: str
    ayanamsha_name: str = "Lahiri (Chitra Paksha)"
    ayanamsha_value: float = AYANAMSHA_LAHIRI_2026
    planetary_positions: Dict[str, Dict[str, Any]]
    active_hora_ruler: str
    transit_vectors: Dict[str, Any]
    combustion_audit: Optional[Dict[str, Any]] = None

class PlanetaryFactProvider:
    def __init__(self):
        self.provider_id = "NV-ASTRONOMICAL-EPHEMERIS-v2"

    def get_chart_facts(
        self,
        target_date: Optional[date] = None,
        city: str = "delhi",
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        tz: Optional[str] = None
    ) -> ChartFactSnapshot:
        t_date = target_date or date.today()
        c_lat, c_lon, c_tz = lat, lon, tz
        if c_lat is None or c_lon is None:
            clean_city = city.lower().strip()
            found = False
            for k, (lt, ln, tzone) in CITY_COORDINATES.items():
                if k in clean_city:
                    c_lat, c_lon, c_tz = lt, ln, tzone
                    found = True
                    break
            if not found:
                c_lat, c_lon, c_tz = 28.6139, 77.2090, "Asia/Kolkata"

        weekday_idx = t_date.weekday()
        hora_rulers = ["Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Sun"]
        first_hora = hora_rulers[weekday_idx]

        snap_id = f"FACTS-{t_date.isoformat()}-{c_lat:.2f}-{c_lon:.2f}"

        # Deterministic Combustion Enrichment
        sun_deg = TRANSIT_POSITIONS_2026["Sun"]["degree"]
        enriched_positions = {}
        combustion_map = {}

        for p_name, p_data in TRANSIT_POSITIONS_2026.items():
            enriched_copy = dict(p_data)
            comb_res = evaluate_planetary_combustion(
                planet_name=p_name,
                planet_deg=p_data["degree"],
                sun_deg=sun_deg,
                is_retrograde=p_data.get("is_retrograde", False)
            )
            enriched_copy["combustion"] = comb_res
            enriched_positions[p_name] = enriched_copy
            if p_name not in ("Sun", "Rahu", "Ketu"):
                combustion_map[p_name] = comb_res

        return ChartFactSnapshot(
            snapshot_id=snap_id,
            target_date=t_date.isoformat(),
            latitude=float(c_lat),
            longitude=float(c_lon),
            timezone=c_tz or "Asia/Kolkata",
            planetary_positions=enriched_positions,
            active_hora_ruler=first_hora,
            transit_vectors={
                "saturn_in_pisces": "Deep restructuring of institutional foundations and karmic clearing",
                "jupiter_in_taurus_gemini": "Expansion of commercial negotiations, knowledge publishing, and ethical wealth",
                "rahu_in_aquarius": "High digital disruption and unconventional network leverage"
            },
            combustion_audit={
                "solar_longitude": sun_deg,
                "combust_planets": [p for p, c in combustion_map.items() if c["is_combust"]],
                "details": combustion_map
            }
        )

planetary_fact_provider = PlanetaryFactProvider()


def get_chart_facts(
    target_date: Optional[Any] = None,
    city: str = "delhi",
    lat: Optional[float] = None,
    lon: Optional[float] = None,
    tz: Optional[str] = None
) -> Dict[str, Any]:
    """Top-level convenience function returning dictionary of chart facts."""
    if isinstance(target_date, str):
        target_date = datetime.strptime(target_date, "%Y-%m-%d").date()
    snapshot = planetary_fact_provider.get_chart_facts(
        target_date=target_date,
        city=city,
        lat=lat,
        lon=lon,
        tz=tz
    )
    if hasattr(snapshot, "model_dump"):
        return snapshot.model_dump()
    return snapshot.dict()

