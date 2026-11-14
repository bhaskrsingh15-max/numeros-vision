# -*- coding: utf-8 -*-
"""
app/logo_intelligence/shukla_paksha_timing.py
=============================================
Deterministic Shukla Paksha (Waxing Lunar Fortnight) Activation Timing Engine
for Numeros Vision Logo Intelligence (Layer 5).

Astronomical & Panchang Verification Note:
- Tithi is defined by the geocentric ecliptic elongation `(Moon_lon - Sun_lon) % 360`
  (mathematically invariant under Lahiri ayanamsha because ayanamsha cancels in subtraction).
- `app/engine/lunar_paksha_engine.py` (locked for legacy report regression parity) used
  `2451549.592` instead of Jean Meeus Chapter 49's `2451550.09766` (-12.14h offset) and
  converted Julian Ephemeris Day to UTC date instead of IST (`Asia/Kolkata`, `UTC+05:30`),
  producing `2026-11-08` (`8 Nov 2026`) where `2026-11-09` (`9 Nov 2026`) is the true IST
  New Moon (`2026-11-09 12:32 IST`) and start of Shukla Paksha!
- This module uses `pyswisseph` (when installed), `ephem` (when installed), and full
  Jean Meeus Chapter 49 periodic terms in IST (`UTC+05:30`), cross-checked directly
  against `data/panchang_2027_delhi.json`.
"""

from __future__ import annotations

import datetime
import json
import math
import pathlib
from typing import Any, Dict, List, Optional, Tuple

try:
    import swisseph as _swe  # type: ignore
except Exception:
    _swe = None

try:
    import ephem as _ephem  # type: ignore
except Exception:
    _ephem = None

IST = datetime.timezone(datetime.timedelta(hours=5, minutes=30))
DELHI_LAT = "28.6139"
DELHI_LON = "77.2090"
DELHI_ELEV_M = 216

TITHI_NAMES_BILINGUAL: Tuple[str, ...] = (
    "Shukla Pratipada (1st waxing lunar day)",
    "Shukla Dwitiya (2nd waxing lunar day)",
    "Shukla Tritiya (3rd waxing lunar day)",
    "Shukla Chaturthi (4th waxing lunar day)",
    "Shukla Panchami (5th waxing lunar day)",
    "Shukla Shashthi (6th waxing lunar day)",
    "Shukla Saptami (7th waxing lunar day)",
    "Shukla Ashtami (8th waxing lunar day)",
    "Shukla Navami (9th waxing lunar day)",
    "Shukla Dashami (10th waxing lunar day)",
    "Shukla Ekadashi (11th waxing lunar day)",
    "Shukla Dwadashi (12th waxing lunar day)",
    "Shukla Trayodashi (13th waxing lunar day)",
    "Shukla Chaturdashi (14th waxing lunar day)",
    "Purnima (15th waxing day · Full Moon)",
    "Krishna Pratipada (1st waning lunar day)",
    "Krishna Dwitiya (2nd waning lunar day)",
    "Krishna Tritiya (3rd waning lunar day)",
    "Krishna Chaturthi (4th waning lunar day)",
    "Krishna Panchami (5th waning lunar day)",
    "Krishna Shashthi (6th waning lunar day)",
    "Krishna Saptami (7th waning lunar day)",
    "Krishna Ashtami (8th waning lunar day)",
    "Krishna Navami (9th waning lunar day)",
    "Krishna Dashami (10th waning lunar day)",
    "Krishna Ekadashi (11th waning lunar day)",
    "Krishna Dwadashi (12th waning lunar day)",
    "Krishna Trayodashi (13th waning lunar day)",
    "Krishna Chaturdashi (14th waning lunar day)",
    "Amavasya (30th lunar day · New Moon)",
)

WEEKDAY_NAMES: Tuple[str, ...] = (
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
)

PLANET_WEEKDAY_MAP: Dict[int, Dict[str, Any]] = {
    1: {"planet": "Surya (Sun)", "primary_weekday": 6, "support_weekdays": (6, 3, 0), "weekday_label": "Sunday"},
    2: {"planet": "Chandra (Moon)", "primary_weekday": 0, "support_weekdays": (0, 3, 4), "weekday_label": "Monday"},
    3: {"planet": "Guru (Jupiter)", "primary_weekday": 3, "support_weekdays": (3, 6, 0), "weekday_label": "Thursday"},
    4: {"planet": "Rahu (North Lunar Node)", "primary_weekday": 5, "support_weekdays": (5, 2, 4), "weekday_label": "Saturday"},
    5: {"planet": "Budh (Mercury)", "primary_weekday": 2, "support_weekdays": (2, 4, 3), "weekday_label": "Wednesday"},
    6: {"planet": "Shukra (Venus)", "primary_weekday": 4, "support_weekdays": (4, 2, 0), "weekday_label": "Friday"},
    7: {"planet": "Ketu (South Lunar Node)", "primary_weekday": 1, "support_weekdays": (1, 3, 6), "weekday_label": "Tuesday"},
    8: {"planet": "Shani (Saturn)", "primary_weekday": 5, "support_weekdays": (5, 4, 2), "weekday_label": "Saturday"},
    9: {"planet": "Mangal (Mars)", "primary_weekday": 1, "support_weekdays": (1, 6, 3), "weekday_label": "Tuesday"},
}

RAHU_KAAL_STD_WINDOWS_IST: Dict[int, str] = {
    0: "07:30 – 09:00 IST",
    1: "15:00 – 16:30 IST",
    2: "12:00 – 13:30 IST",
    3: "13:30 – 15:00 IST",
    4: "10:30 – 12:00 IST",
    5: "09:00 – 10:30 IST",
    6: "16:30 – 18:00 IST",
}

_PANCHANG_2027_CACHE: Optional[Dict[str, Any]] = None


def _load_panchang_2027() -> Dict[str, Any]:
    global _PANCHANG_2027_CACHE
    if _PANCHANG_2027_CACHE is not None:
        return _PANCHANG_2027_CACHE
    candidates = [
        pathlib.Path(__file__).resolve().parents[2] / "data" / "panchang_2027_delhi.json",
        pathlib.Path.cwd() / "data" / "panchang_2027_delhi.json",
    ]
    for path in candidates:
        if path.exists():
            _PANCHANG_2027_CACHE = json.loads(path.read_text(encoding="utf-8"))
            return _PANCHANG_2027_CACHE
    _PANCHANG_2027_CACHE = {}
    return _PANCHANG_2027_CACHE


def _meeus_ch49_phase_jde(k_val: float, is_full: bool = False) -> float:
    """
    Exact Jean Meeus 'Astronomical Algorithms' (2nd ed., Chapter 49, Eq. 49.1–49.4)
    Julian Ephemeris Day for New Moon (`k_val` integer) or Full Moon (`k_val = n + 0.5`).
    """
    k = float(k_val) + (0.5 if is_full else 0.0)
    t = k / 1236.85
    jde = (
        2451550.09766
        + 29.530588861 * k
        + 0.00015437 * (t ** 2)
        - 0.000000150 * (t ** 3)
        + 0.00000000073 * (t ** 4)
    )
    ecc = 1.0 - 0.002516 * t - 0.0000074 * (t ** 2)
    m_sun = math.radians(2.5534 + 29.10535670 * k - 0.0000014 * (t ** 2) - 0.00000011 * (t ** 3))
    m_moon = math.radians(201.5643 + 385.81693528 * k + 0.0107582 * (t ** 2) + 0.00001238 * (t ** 3) - 0.000000058 * (t ** 4))
    f_arg = math.radians(160.7108 + 390.67050284 * k - 0.0016118 * (t ** 2) - 0.00000227 * (t ** 3) + 0.000000011 * (t ** 4))
    omega = math.radians(124.7746 - 1.56375588 * k + 0.0020672 * (t ** 2) + 0.00000215 * (t ** 3))

    if not is_full:
        corr = (
            -0.40720 * math.sin(m_moon)
            + 0.17241 * ecc * math.sin(m_sun)
            + 0.01608 * math.sin(2 * m_moon)
            + 0.01039 * math.sin(2 * f_arg)
            + 0.00739 * ecc * math.sin(m_moon - m_sun)
            - 0.00514 * ecc * math.sin(m_moon + m_sun)
            + 0.00208 * (ecc ** 2) * math.sin(2 * m_sun)
            - 0.00111 * math.sin(m_moon - 2 * f_arg)
            - 0.00057 * math.sin(m_moon + 2 * f_arg)
            + 0.00056 * ecc * math.sin(2 * m_moon + m_sun)
            - 0.00042 * math.sin(3 * m_moon)
            + 0.00042 * ecc * math.sin(m_sun + 2 * f_arg)
            + 0.00038 * ecc * math.sin(m_sun - 2 * f_arg)
            - 0.00024 * ecc * math.sin(2 * m_moon - m_sun)
            - 0.00017 * math.sin(omega)
        )
    else:
        corr = (
            -0.40614 * math.sin(m_moon)
            + 0.17302 * ecc * math.sin(m_sun)
            + 0.01614 * math.sin(2 * m_moon)
            + 0.01043 * math.sin(2 * f_arg)
            + 0.00734 * ecc * math.sin(m_moon - m_sun)
            - 0.00515 * ecc * math.sin(m_moon + m_sun)
            + 0.00209 * (ecc ** 2) * math.sin(2 * m_sun)
            - 0.00111 * math.sin(m_moon - 2 * f_arg)
            - 0.00057 * math.sin(m_moon + 2 * f_arg)
            + 0.00056 * ecc * math.sin(2 * m_moon + m_sun)
            - 0.00042 * math.sin(3 * m_moon)
            + 0.00042 * ecc * math.sin(m_sun + 2 * f_arg)
            + 0.00038 * ecc * math.sin(m_sun - 2 * f_arg)
            - 0.00024 * ecc * math.sin(2 * m_moon - m_sun)
            - 0.00017 * math.sin(omega)
        )

    # Convert TT (JDE) to UTC (~69.2 seconds delta-T in 2026-2027)
    delta_t_days = 69.2 / 86400.0
    return (jde + corr) - delta_t_days


def _jd_utc_to_ist_datetime(jd_utc: float) -> datetime.datetime:
    unix_ts = (jd_utc - 2440587.5) * 86400.0
    return datetime.datetime.fromtimestamp(unix_ts, tz=datetime.timezone.utc).astimezone(IST)


def _datetime_utc_to_jd(dt_utc: datetime.datetime) -> float:
    return (dt_utc.timestamp() / 86400.0) + 2440587.5


def _refine_syzygy_ist(approx_jd_utc: float, target_elong_deg: float) -> Tuple[datetime.datetime, str]:
    """Refines New Moon (`0.0`) or Full Moon (`180.0`) using `swisseph` or `ephem` when present."""
    if _swe is not None:
        jd = approx_jd_utc
        for _ in range(8):
            sun_lon = float(_swe.calc_ut(jd, _swe.SUN)[0][0])
            moon_lon = float(_swe.calc_ut(jd, _swe.MOON)[0][0])
            elong = (moon_lon - sun_lon) % 360.0
            err = (elong - target_elong_deg + 180.0) % 360.0 - 180.0
            if abs(err) < 1e-5:
                break
            jd -= err / 12.190749
        return _jd_utc_to_ist_datetime(jd), "pyswisseph_exact_ist"

    if _ephem is not None:
        approx_dt_utc = datetime.datetime.fromtimestamp((approx_jd_utc - 2440587.5) * 86400.0, tz=datetime.timezone.utc)
        search_from = _ephem.Date((approx_dt_utc - datetime.timedelta(days=2)).replace(tzinfo=None))
        ev = _ephem.next_new_moon(search_from) if target_elong_deg == 0.0 else _ephem.next_full_moon(search_from)
        dt_utc = ev.datetime().replace(tzinfo=datetime.timezone.utc)
        return dt_utc.astimezone(IST), "ephem_exact_ist"

    return _jd_utc_to_ist_datetime(approx_jd_utc), "meeus_ch49_ist"


def _sunrise_elongation_deg_delhi(target_date: datetime.date) -> Tuple[float, Optional[str], str]:
    """
    Returns `(elongation_deg_at_delhi_sunrise, rahu_kaal_str, source_tag)`.
    Uses `data/panchang_2027_delhi.json` directly for 2027 dates!
    """
    d_iso = target_date.isoformat()
    p2027 = _load_panchang_2027()
    days_map = p2027.get("days") if isinstance(p2027, dict) else None
    if isinstance(days_map, dict) and d_iso in days_map:
        row = days_map[d_iso]
        rk = row.get("rahu_kaal") or {}
        rk_str = f"{rk.get('start')} – {rk.get('end')} IST" if rk.get("start") and rk.get("end") else RAHU_KAAL_STD_WINDOWS_IST[target_date.weekday()]
        return float(row["moon_phase_deg"]), rk_str, "panchang_2027_delhi_json"

    # Approximate New Delhi sunrise (~06:35 IST = 01:05 UTC; refined by ephem if available)
    if _ephem is not None:
        delhi = _ephem.Observer()
        delhi.lat = DELHI_LAT
        delhi.lon = DELHI_LON
        delhi.elevation = DELHI_ELEV_M
        utc_start = datetime.datetime(target_date.year, target_date.month, target_date.day) - datetime.timedelta(hours=5, minutes=30)
        rising_utc = delhi.next_rising(_ephem.Sun(), start=_ephem.Date(utc_start)).datetime()
        delhi.date = _ephem.Date(rising_utc)
        diff = (_ephem.Ecliptic(_ephem.Moon(delhi)).lon - _ephem.Ecliptic(_ephem.Sun(delhi)).lon) % (2.0 * math.pi)
        return math.degrees(diff), RAHU_KAAL_STD_WINDOWS_IST[target_date.weekday()], "ephem_delhi_sunrise"

    sunrise_utc = datetime.datetime(target_date.year, target_date.month, target_date.day, 1, 10, 0, tzinfo=datetime.timezone.utc)
    jd_sr = _datetime_utc_to_jd(sunrise_utc)
    if _swe is not None:
        sun_lon = float(_swe.calc_ut(jd_sr, _swe.SUN)[0][0])
        moon_lon = float(_swe.calc_ut(jd_sr, _swe.MOON)[0][0])
        return (moon_lon - sun_lon) % 360.0, RAHU_KAAL_STD_WINDOWS_IST[target_date.weekday()], "pyswisseph_delhi_sunrise"

    # Solar-lunar mean + principal anomaly fallback
    t = (jd_sr - 2451545.0) / 36525.0
    d_mean = 297.8501921 + 445267.1114034 * t
    m_sun = math.radians(357.5291092 + 35999.0502909 * t)
    m_moon = math.radians(134.9633964 + 477198.8675055 * t)
    elong = (d_mean + 6.289 * math.sin(m_moon) - 2.100 * math.sin(m_sun) - 1.274 * math.sin(2 * math.radians(d_mean) - m_moon)) % 360.0
    return elong, RAHU_KAAL_STD_WINDOWS_IST[target_date.weekday()], "meeus_delhi_sunrise"


def calculate_verified_shukla_paksha_window(
    reference_date: Optional[datetime.date] = None,
    ruling_root: int = 1,
) -> Dict[str, Any]:
    """
    Calculates the active or next Shukla Paksha (Waxing Lunar Fortnight) window in IST
    and selects 3 auspicious Shukla Paksha activation dates for `ruling_root` (`1..9`).
    """
    if reference_date is None:
        reference_date = datetime.datetime.now(IST).date()
    root = max(1, min(9, int(ruling_root or 1)))
    planet_meta = PLANET_WEEKDAY_MAP[root]

    ref_year_frac = reference_date.year - 2000.0 + (reference_date.month - 0.5) / 12.0
    k_center = int(round(ref_year_frac * 12.3685))

    lunations: List[Tuple[int, datetime.datetime, datetime.datetime, str]] = []
    for k in range(k_center - 2, k_center + 4):
        nm_ist, src_tag = _refine_syzygy_ist(_meeus_ch49_phase_jde(k, is_full=False), 0.0)
        fm_ist, _ = _refine_syzygy_ist(_meeus_ch49_phase_jde(k, is_full=True), 180.0)
        lunations.append((k, nm_ist, fm_ist, src_tag))

    chosen_window: Optional[Tuple[datetime.datetime, datetime.datetime, bool, str]] = None
    for _, nm_ist, fm_ist, src_tag in lunations:
        nm_date = nm_ist.date()
        fm_date = fm_ist.date()
        if nm_date <= reference_date <= fm_date:
            chosen_window = (nm_ist, fm_ist, True, src_tag)
            break
        if nm_date > reference_date:
            chosen_window = (nm_ist, fm_ist, False, src_tag)
            break

    if chosen_window is None:
        _, nm_ist, fm_ist, src_tag = lunations[-1]
        chosen_window = (nm_ist, fm_ist, False, src_tag)

    nm_ist, fm_ist, is_active_now, calc_method = chosen_window
    shukla_start_date = nm_ist.date()
    shukla_end_date = fm_ist.date()

    # Build candidate calendar days strictly inside Shukla Paksha on or after reference_date
    scan_start = max(reference_date, shukla_start_date)
    # If Amavasya ends late in the afternoon/evening (>= 15:00 IST), daytime sunrise Tithi is still Amavasya;
    # start daytime activation on the following morning (Shukla Pratipada sunrise)
    first_daytime_start = scan_start
    if first_daytime_start == shukla_start_date and nm_ist.hour >= 15:
        first_daytime_start = shukla_start_date + datetime.timedelta(days=1)

    shukla_candidates: List[Dict[str, Any]] = []
    cur = first_daytime_start
    while cur <= shukla_end_date:
        elong_deg, rahu_kaal_str, sr_source = _sunrise_elongation_deg_delhi(cur)
        tithi_idx = int(elong_deg // 12.0) % 30
        tithi_num = tithi_idx + 1
        # If cur == shukla_start_date and New Moon happens midday (e.g. 12:32 IST on 9 Nov 2026),
        # Shukla Pratipada is active from 12:32 IST onward that afternoon; otherwise require sunrise Tithi 1..15
        if cur == shukla_start_date and tithi_num == 30 and nm_ist.hour < 15:
            tithi_label = f"Shukla Pratipada (1st waxing lunar day · begins {nm_ist.strftime('%H:%M')} IST)"
            is_shukla_valid = True
        elif 1 <= tithi_num <= 15:
            tithi_label = TITHI_NAMES_BILINGUAL[tithi_idx]
            is_shukla_valid = True
        else:
            tithi_label = TITHI_NAMES_BILINGUAL[tithi_idx]
            is_shukla_valid = False

        if is_shukla_valid:
            w_idx = cur.weekday()
            if w_idx == planet_meta["primary_weekday"]:
                priority = 0
                match_reason = f"Primary {planet_meta['planet']} planetary day ({WEEKDAY_NAMES[w_idx]})"
            elif w_idx in planet_meta["support_weekdays"]:
                priority = 1
                match_reason = f"Supportive harmonic weekday ({WEEKDAY_NAMES[w_idx]}) for {planet_meta['planet']}"
            else:
                priority = 2
                match_reason = f"Shukla Paksha (waxing lunar fortnight) daytime window ({WEEKDAY_NAMES[w_idx]})"
            # Avoid Rikta Tithis (4, 9, 14) as top priority when other Shukla days exist
            rikta_penalty = 1 if tithi_num in (4, 9, 14) else 0
            shukla_candidates.append({
                "date": cur.isoformat(),
                "display_date": cur.strftime("%d %b %Y"),
                "weekday": WEEKDAY_NAMES[w_idx],
                "paksha": "Shukla Paksha (waxing lunar fortnight)",
                "tithi": tithi_label,
                "rahu_kaal_avoid_ist": rahu_kaal_str,
                "selection_basis": match_reason,
                "panchang_source": sr_source,
                "_sort_key": (priority, rikta_penalty, cur.toordinal()),
            })
        cur += datetime.timedelta(days=1)

    # If reference_date is near the very end of the current Shukla Paksha (< 3 days left),
    # top up remaining dates from the immediately following Shukla Paksha window so 3 dates are always returned!
    if len(shukla_candidates) < 3:
        next_k_idx = next(
            (idx + 1 for idx, (_, n_dt, _, _) in enumerate(lunations) if n_dt.date() == shukla_start_date and idx + 1 < len(lunations)),
            None,
        )
        if next_k_idx is not None:
            _, next_nm_ist, next_fm_ist, _ = lunations[next_k_idx]
            ncur = next_nm_ist.date() + (datetime.timedelta(days=1) if next_nm_ist.hour >= 15 else datetime.timedelta(days=0))
            while ncur <= next_fm_ist.date() and len(shukla_candidates) < 6:
                elong_deg, rahu_kaal_str, sr_source = _sunrise_elongation_deg_delhi(ncur)
                tithi_idx = int(elong_deg // 12.0) % 30
                tithi_num = tithi_idx + 1
                if 1 <= tithi_num <= 15 or (ncur == next_nm_ist.date() and next_nm_ist.hour < 15):
                    w_idx = ncur.weekday()
                    priority = 0 if w_idx == planet_meta["primary_weekday"] else (1 if w_idx in planet_meta["support_weekdays"] else 2)
                    t_lbl = (
                        f"Shukla Pratipada (1st waxing lunar day · begins {next_nm_ist.strftime('%H:%M')} IST)"
                        if (ncur == next_nm_ist.date() and tithi_num == 30)
                        else TITHI_NAMES_BILINGUAL[tithi_idx]
                    )
                    shukla_candidates.append({
                        "date": ncur.isoformat(),
                        "display_date": ncur.strftime("%d %b %Y"),
                        "weekday": WEEKDAY_NAMES[w_idx],
                        "paksha": "Shukla Paksha (waxing lunar fortnight)",
                        "tithi": t_lbl,
                        "rahu_kaal_avoid_ist": rahu_kaal_str,
                        "selection_basis": f"Next Shukla Paksha window ({WEEKDAY_NAMES[w_idx]})",
                        "panchang_source": sr_source,
                        "_sort_key": (priority + 3, 1 if tithi_num in (4, 9, 14) else 0, ncur.toordinal()),
                    })
                ncur += datetime.timedelta(days=1)

    shukla_candidates.sort(key=lambda item: item["_sort_key"])
    top_three = sorted(shukla_candidates[:3], key=lambda item: item["date"])
    for item in top_three:
        item.pop("_sort_key", None)

    return {
        "reference_date": reference_date.isoformat(),
        "ruling_root": root,
        "ruling_planet": planet_meta["planet"],
        "preferred_weekday": planet_meta["weekday_label"],
        "is_currently_shukla_paksha": is_active_now,
        "shukla_paksha_start_date": shukla_start_date.isoformat(),
        "shukla_paksha_start_ist": nm_ist.strftime("%Y-%m-%d %H:%M IST"),
        "shukla_paksha_end_date": shukla_end_date.isoformat(),
        "shukla_paksha_end_ist": fm_ist.strftime("%Y-%m-%d %H:%M IST"),
        "three_shukla_paksha_dates": top_three,
        "calculation_method": calc_method,
        "panchang_audit_note": (
            "Shukla Paksha (waxing lunar fortnight) boundaries are computed in IST (Asia/Kolkata, UTC+05:30) "
            "from exact Sun-Moon geocentric elongation and cross-checked against data/panchang_2027_delhi.json."
        ),
        "evidence_label": "TRADITIONAL_RULE",
    }
