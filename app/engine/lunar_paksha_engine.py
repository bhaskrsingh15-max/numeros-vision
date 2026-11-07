"""
app/engine/lunar_paksha_engine.py
==================================
Deterministic Astronomical Lunar Paksha (Tithi & Phase) Calculation Engine.
Calculates Shukla Paksha (Waxing Moon) and Krishna Paksha (Waning Moon) windows
for any given calendar date using high-precision Jean Meeus astronomical algorithms.
Provides authoritative Vedic guidance for commencing numerological, gemstone,
mantra, and environmental remedies.
"""

import math
import datetime
from typing import Dict, Any, Optional

WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# Planetary Day Associations for Remedial Initiation (0=Monday, 6=Sunday)
PLANET_DAY_MAP = {
    1: {"planet": "Sun (Surya)", "weekday_idx": 6, "weekday_name": "Sunday"},
    2: {"planet": "Moon (Chandra)", "weekday_idx": 0, "weekday_name": "Monday"},
    3: {"planet": "Jupiter (Brihaspati / Guru)", "weekday_idx": 3, "weekday_name": "Thursday"},
    4: {"planet": "Rahu", "weekday_idx": 5, "weekday_name": "Saturday"},
    5: {"planet": "Mercury (Budh)", "weekday_idx": 2, "weekday_name": "Wednesday"},
    6: {"planet": "Venus (Shukra)", "weekday_idx": 4, "weekday_name": "Friday"},
    7: {"planet": "Ketu", "weekday_idx": 1, "weekday_name": "Tuesday"},
    8: {"planet": "Saturn (Shani)", "weekday_idx": 5, "weekday_name": "Saturday"},
    9: {"planet": "Mars (Mangal)", "weekday_idx": 1, "weekday_name": "Tuesday"}
}

def _meeus_phase_jde(k_val: float, is_full: bool = False) -> float:
    """Computes Julian Ephemeris Date for lunation k using Jean Meeus' periodic perturbations."""
    T = k_val / 1236.85
    base_jde = 2451549.592 + 29.53058867 * k_val + 0.0001178 * (T**2) - 0.000000155 * (T**3)
    E = 1 - 0.002516 * T - 0.0000074 * (T**2)
    M = math.radians(2.5534 + 29.10535669 * k_val - 0.0000218 * (T**2))
    Mprime = math.radians(201.5643 + 385.81693528 * k_val + 0.0107438 * (T**2))
    F = math.radians(160.7108 + 390.67050274 * k_val - 0.0016341 * (T**2))

    if not is_full:
        corr = (
            -0.40720 * math.sin(Mprime)
            + 0.17241 * E * math.sin(M)
            + 0.01608 * math.sin(2 * Mprime)
            - 0.01041 * math.sin(2 * F)
            + 0.00739 * E * math.sin(Mprime - M)
        )
    else:
        corr = (
            -0.40614 * math.sin(Mprime)
            + 0.17302 * E * math.sin(M)
            + 0.01614 * math.sin(2 * Mprime)
            - 0.01043 * math.sin(2 * F)
            + 0.00734 * E * math.sin(Mprime - M)
        )
    return base_jde + corr

def _jde_to_date(jde: float) -> datetime.date:
    """Converts a Julian Ephemeris Date to UTC calendar date."""
    epoch = datetime.datetime(2000, 1, 1, 12, 0, 0, tzinfo=datetime.timezone.utc)
    days = jde - 2451545.0
    dt = epoch + datetime.timedelta(days=days)
    return dt.date()

def _find_next_weekday(start_date: datetime.date, target_weekday_idx: int) -> datetime.date:
    """Finds the next occurring date matching the target weekday index (0=Monday, 6=Sunday)."""
    days_ahead = target_weekday_idx - start_date.weekday()
    if days_ahead < 0:
        days_ahead += 7
    return start_date + datetime.timedelta(days=days_ahead)

def calculate_shukla_paksha_timing(
    reading_date: Optional[datetime.date] = None,
    ruling_planet_num: Optional[int] = 2
) -> Dict[str, Any]:
    """
    Evaluates whether `reading_date` falls in Shukla Paksha or Krishna Paksha.
    Returns exact start/end dates for the active or next Shukla Paksha,
    along with the specific recommended weekday to commence remedies.
    """
    if reading_date is None:
        reading_date = datetime.date.today()

    # Lunation estimate relative to Jan 2000
    ref_year_diff = reading_date.year - 2000 + (reading_date.month - 1) / 12.0
    k_est = int(ref_year_diff * 12.3685)

    # Search through nearby lunations to find the bounding New Moons
    candidate_new_moons = []
    for k in range(k_est - 2, k_est + 4):
        nm_date = _jde_to_date(_meeus_phase_jde(float(k), is_full=False))
        fm_date = _jde_to_date(_meeus_phase_jde(float(k) + 0.5, is_full=True))
        candidate_new_moons.append((k, nm_date, fm_date))

    # Identify where reading_date sits
    active_nm = None
    active_fm = None
    next_nm = None
    next_fm = None

    for i in range(len(candidate_new_moons) - 1):
        k_curr, nm_curr, fm_curr = candidate_new_moons[i]
        k_next, nm_next, fm_next = candidate_new_moons[i+1]
        if nm_curr <= reading_date < nm_next:
            active_nm = nm_curr
            active_fm = fm_curr
            next_nm = nm_next
            next_fm = fm_next
            break

    if not active_nm:
        # Fallback to candidate 0
        active_nm = candidate_new_moons[0][1]
        active_fm = candidate_new_moons[0][2]
        next_nm = candidate_new_moons[1][1]
        next_fm = candidate_new_moons[1][2]

    is_currently_shukla = (active_nm <= reading_date <= active_fm)

    p_info = PLANET_DAY_MAP.get(ruling_planet_num or 2, PLANET_DAY_MAP[2])
    target_weekday_idx = p_info["weekday_idx"]
    target_weekday_name = p_info["weekday_name"]
    planet_name = p_info["planet"]

    if is_currently_shukla:
        current_phase = "Shukla Paksha (Waxing Moon / Bright Fortnight)"
        shukla_start = active_nm
        shukla_end = active_fm
        # Seeker can start on the next auspicious weekday during this current Shukla Paksha
        first_remedy_date = _find_next_weekday(reading_date, target_weekday_idx)
        if first_remedy_date > shukla_end:
            # If the next weekday exceeds current Purnima, wrap to next Shukla Paksha
            shukla_start = next_nm
            shukla_end = next_fm
            first_remedy_date = _find_next_weekday(next_nm, target_weekday_idx)
            is_currently_shukla = False

    if not is_currently_shukla:
        current_phase = "Krishna Paksha (Waning Moon / Dark Fortnight)"
        shukla_start = next_nm
        shukla_end = next_fm
        first_remedy_date = _find_next_weekday(next_nm, target_weekday_idx)

    # Build humanized classical narrative
    if is_currently_shukla:
        guidance_text = (
            f"**Auspicious Initiation Window (Active Shukla Paksha):**\n"
            f"You are currently taking your reading during the sacred **Shukla Paksha (Waxing Moon Phase: {shukla_start.strftime('%B %d, %Y')} to {shukla_end.strftime('%B %d, %Y')} — Purnima)**. "
            f"In classical Vedic tradition, when the Moon is waxing, all energized gemstones, yantras, and mindful habits compound with maximum constructive vitality. "
            f"You can begin this remedy **immediately on the next auspicious {target_weekday_name} ({first_remedy_date.strftime('%B %d, %Y')})** during this active window."
        )
    else:
        guidance_text = (
            f"**Auspicious Initiation Window (Upcoming Shukla Paksha):**\n"
            f"Currently, the lunar cycle is in **Krishna Paksha (Waning Moon phase)**. "
            f"In classical Sankhya Shastra and Vedic Jyotish, remedies, crystal energization, and mantra sadhanas "
            f"should strictly begin during **Shukla Paksha (Waxing Moon / Bright Fortnight)** so your intentions grow with the expanding lunar light. "
            f"Your next ideal Shukla Paksha begins on **{shukla_start.strftime('%B %d, %Y')}** (Pratipada) "
            f"and culminates on **{shukla_end.strftime('%B %d, %Y')}** (Purnima / Full Moon). "
            f"Plan to formally commence this remedy on the first auspicious **{target_weekday_name} ({first_remedy_date.strftime('%B %d, %Y')})** falling within this upcoming window."
        )

    return {
        "status": "CURRENT_SHUKLA" if is_currently_shukla else "UPCOMING_SHUKLA",
        "is_currently_shukla": is_currently_shukla,
        "current_lunar_phase": current_phase,
        "shukla_window_start": shukla_start.isoformat(),
        "shukla_window_end": shukla_end.isoformat(),
        "recommended_first_date": first_remedy_date.isoformat(),
        "recommended_weekday": target_weekday_name,
        "planetary_ruler": planet_name,
        "guidance_narrative": guidance_text
    }

if __name__ == "__main__":
    t = datetime.date(2026, 10, 30)
    print("Testing for today 2026-10-30:")
    res = calculate_shukla_paksha_timing(t, ruling_planet_num=2)
    print(res["guidance_narrative"])
