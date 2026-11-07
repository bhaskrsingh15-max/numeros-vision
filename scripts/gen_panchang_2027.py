#!/usr/bin/env python3
"""
PANCHANG 2027 GENERATOR (NEW DELHI, IST)
Numeros Vision · 2027 Year Ahead Planner
Produces data/panchang_2027_delhi.json and spot-check validation table.

Ayanamsha Note:
Tithi is defined strictly by the relative elongation between Moon and Sun:
Elongation = (Moon_lon - Sun_lon) % 360 degrees.
Because Ayanamsha is subtracted equally from both Moon and Sun:
(Moon_lon - Ayanamsha) - (Sun_lon - Ayanamsha) = Moon_lon - Sun_lon.
The relative elongation is mathematically invariant under Ayanamsha.
Calculation uses high-precision astronomical ephemeris (ephem / swisseph)
for New Delhi coordinates (28.6139° N, 77.2090° E, 216m elevation).
"""

import os
import json
import math
import datetime

try:
    import ephem
except ImportError:
    raise ImportError("ephem is required. Please install it with pip install ephem")

DELHI_LAT = '28.6139'
DELHI_LON = '77.2090'
DELHI_ELEV = 216

TITHI_NAMES = [
    'Shukla Pratipada', 'Shukla Dwitiya', 'Shukla Tritiya', 'Shukla Chaturthi', 'Shukla Panchami',
    'Shukla Shashthi', 'Shukla Saptami', 'Shukla Ashtami', 'Shukla Navami', 'Shukla Dashami',
    'Shukla Ekadashi', 'Shukla Dwadashi', 'Shukla Trayodashi', 'Shukla Chaturdashi', 'Purnima',
    'Krishna Pratipada', 'Krishna Dwitiya', 'Krishna Tritiya', 'Krishna Chaturthi', 'Krishna Panchami',
    'Krishna Shashthi', 'Krishna Saptami', 'Krishna Ashtami', 'Krishna Navami', 'Krishna Dashami',
    'Krishna Ekadashi', 'Krishna Dwadashi', 'Krishna Trayodashi', 'Krishna Chaturdashi', 'Amavasya'
]

WEEKDAY_NAMES = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Rahu Kaal 1/8th slot index for each weekday (0=Mon, 1=Tue, ..., 6=Sun)
# Standard Vedic Ashtama Bhaga:
# Mon: 2nd part (idx 1), Tue: 7th part (idx 6), Wed: 5th part (idx 4),
# Thu: 6th part (idx 5), Fri: 4th part (idx 3), Sat: 3rd part (idx 2), Sun: 8th part (idx 7)
RAHU_KAAL_SLOTS = {
    0: 1,  # Monday -> 2nd part
    1: 6,  # Tuesday -> 7th part
    2: 4,  # Wednesday -> 5th part
    3: 5,  # Thursday -> 6th part
    4: 3,  # Friday -> 4th part
    5: 2,  # Saturday -> 3rd part
    6: 7   # Sunday -> 8th part
}

def get_astronomical_moons_2027():
    start_date = ephem.Date('2027/01/01 00:00:00')
    end_date = ephem.Date('2028/01/01 00:00:00')

    full_moons = []
    cur = start_date
    while cur < end_date:
        fm = ephem.next_full_moon(cur)
        if fm >= end_date:
            break
        dt_utc = fm.datetime()
        dt_ist = dt_utc + datetime.timedelta(hours=5, minutes=30)
        full_moons.append({
            "utc": dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "ist": dt_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
            "date": dt_ist.strftime("%Y-%m-%d"),
            "time_ist": dt_ist.strftime("%H:%M")
        })
        cur = fm + 1

    new_moons = []
    cur = start_date
    while cur < end_date:
        nm = ephem.next_new_moon(cur)
        if nm >= end_date:
            break
        dt_utc = nm.datetime()
        dt_ist = dt_utc + datetime.timedelta(hours=5, minutes=30)
        new_moons.append({
            "utc": dt_utc.strftime("%Y-%m-%d %H:%M:%S UTC"),
            "ist": dt_ist.strftime("%Y-%m-%d %H:%M:%S IST"),
            "date": dt_ist.strftime("%Y-%m-%d"),
            "time_ist": dt_ist.strftime("%H:%M")
        })
        cur = nm + 1

    return full_moons, new_moons

def generate_panchang_2027():
    delhi = ephem.Observer()
    delhi.lat = DELHI_LAT
    delhi.lon = DELHI_LON
    delhi.elevation = DELHI_ELEV

    full_moons, new_moons = get_astronomical_moons_2027()
    fm_by_date = {fm["date"]: fm for fm in full_moons}
    nm_by_date = {nm["date"]: nm for nm in new_moons}

    calendar_data = {}
    current_date = datetime.date(2027, 1, 1)
    end_date = datetime.date(2027, 12, 31)

    while current_date <= end_date:
        d_str = current_date.strftime("%Y-%m-%d")
        # Search from local midnight IST (18:30:00 UTC of previous day) to ensure early summer sunrises (~05:23 IST)
        # are captured for the target day, avoiding the next-day offset bug
        local_midnight_ist = datetime.datetime.combine(current_date, datetime.time(0, 0, 0))
        utc_search_start = local_midnight_ist - datetime.timedelta(hours=5, minutes=30)
        delhi.date = ephem.Date(utc_search_start)

        sun = ephem.Sun()
        rising_utc = delhi.next_rising(sun, start=ephem.Date(utc_search_start)).datetime()
        setting_utc = delhi.next_setting(sun, start=rising_utc).datetime()

        rising_ist = rising_utc + datetime.timedelta(hours=5, minutes=30)
        setting_ist = setting_utc + datetime.timedelta(hours=5, minutes=30)

        # Sun & Moon positions at exact sunrise in New Delhi
        delhi.date = ephem.Date(rising_utc)
        sun_obs = ephem.Sun(delhi)
        moon_obs = ephem.Moon(delhi)

        sun_ecl = ephem.Ecliptic(sun_obs)
        moon_ecl = ephem.Ecliptic(moon_obs)

        diff = (moon_ecl.lon - sun_ecl.lon) % (2 * math.pi)
        diff_deg = math.degrees(diff)
        tithi_idx = int(diff_deg // 12)
        tithi_number = tithi_idx + 1  # 1 to 30
        tithi_name = TITHI_NAMES[tithi_idx]
        paksha = "Shukla" if tithi_number <= 15 else "Krishna"

        # Tithi boundary proximity (within 45 minutes of sunrise)
        # 1 tithi = 12 deg. Mean motion rate ~ 0.549 deg/hour => 60 / 0.549 min/deg
        rem_deg = diff_deg % 12
        dist_to_boundary_deg = min(rem_deg, 12.0 - rem_deg)
        minutes_to_boundary = dist_to_boundary_deg * (60.0 / 0.549)
        near_boundary = (minutes_to_boundary <= 45.0)

        # Rahu Kaal calculation (1/8th of daytime)
        day_seconds = (setting_ist - rising_ist).total_seconds()
        slot_seconds = day_seconds / 8.0
        w_idx = current_date.weekday()
        slot_idx = RAHU_KAAL_SLOTS[w_idx]

        rahu_start = rising_ist + datetime.timedelta(seconds=slot_idx * slot_seconds)
        rahu_end = rising_ist + datetime.timedelta(seconds=(slot_idx + 1) * slot_seconds)

        # Check if Rahu Kaal covers working morning (e.g., starts before 12:30 PM and ends after 10:00 AM)
        morning_rahu = (rahu_start.hour < 12)

        # Events on this day
        fm_event = fm_by_date.get(d_str)
        nm_event = nm_by_date.get(d_str)
        events = []
        if fm_event:
            events.append(f"Full Moon (Purnima) at {fm_event['time_ist']} IST")
        if nm_event:
            events.append(f"New Moon (Amavasya) at {nm_event['time_ist']} IST")

        # Exclusions for auspicious dates:
        # 1. Amavasya day (either sunrise tithi is Amavasya, or exact New Moon occurs)
        # 2. Morning Rahu Kaal covering significant morning working window
        is_amavasya = (tithi_number == 30 or bool(nm_event))
        is_purnima = (tithi_number == 15 or bool(fm_event))

        calendar_data[d_str] = {
            "date": d_str,
            "weekday": WEEKDAY_NAMES[w_idx],
            "day": current_date.day,
            "month": current_date.month,
            "year": 2027,
            "sunrise_ist": rising_ist.strftime("%H:%M:%S"),
            "sunset_ist": setting_ist.strftime("%H:%M:%S"),
            "sunrise_short": rising_ist.strftime("%H:%M"),
            "sunset_short": setting_ist.strftime("%H:%M"),
            "tithi_number": tithi_number,
            "tithi_name": tithi_name,
            "paksha": paksha,
            "near_boundary": near_boundary,
            "minutes_to_tithi_boundary": round(minutes_to_boundary, 1),
            "moon_phase_deg": round(diff_deg, 2),
            "rahu_kaal": {
                "start": rahu_start.strftime("%H:%M"),
                "end": rahu_end.strftime("%H:%M"),
                "is_morning": morning_rahu
            },
            "is_amavasya": is_amavasya,
            "is_purnima": is_purnima,
            "events": events
        }

        current_date += datetime.timedelta(days=1)

    output = {
        "metadata": {
            "title": "Panchang 2027 for New Delhi (IST)",
            "city": "New Delhi",
            "country": "India",
            "latitude": float(DELHI_LAT),
            "longitude": float(DELHI_LON),
            "elevation_meters": DELHI_ELEV,
            "timezone": "Asia/Kolkata (UTC+05:30)",
            "ayanamsa": "Lahiri Invariant (Relative Angular Elongation)",
            "verification_status": "UNVERIFIED — Pending Bhaskr's Confirmation against published Panchang",
            "total_days": len(calendar_data),
            "total_full_moons": len(full_moons),
            "total_new_moons": len(new_moons)
        },
        "full_moons_2027": full_moons,
        "new_moons_2027": new_moons,
        "days": calendar_data
    }

    os.makedirs("data", exist_ok=True)
    with open("data/panchang_2027_delhi.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Saved 365-day panchang to data/panchang_2027_delhi.json")
    return output

def build_spot_check_table(panchang_data):
    days = panchang_data["days"]
    full_moons = panchang_data["full_moons_2027"]
    new_moons = panchang_data["new_moons_2027"]

    spot_dates = set()

    # 1. First 3 days of each month (12 x 3 = 36 dates)
    for m in range(1, 13):
        for d in [1, 2, 3]:
            spot_dates.add(f"2027-{m:02d}-{d:02d}")

    # 2. Every Full Moon date
    for fm in full_moons:
        spot_dates.add(fm["date"])

    # 3. Every New Moon date
    for nm in new_moons:
        spot_dates.add(nm["date"])

    # 4. Mandatory spot assertion audit dates
    spot_dates.update([
        "2027-05-20", "2027-06-19", "2027-06-01", "2027-06-02",
        "2027-06-03", "2027-06-05", "2027-07-03", "2027-07-04"
    ])

    sorted_dates = sorted(list(spot_dates))

    lines = []
    lines.append("# PANCHANG 2027 SPOT-CHECK TABLE (NEW DELHI, IST)")
    lines.append("**Status**: `UNVERIFIED — Pending Bhaskr's Confirmation against published Panchang`")
    lines.append("**Location**: New Delhi (28.6139° N, 77.2090° E, 216m) · Timezone: IST (UTC+05:30)")
    lines.append(f"**Total Spot-Check Dates**: {len(sorted_dates)} dates (First 3 days of each month + all Full Moons + all New Moons)")
    lines.append("")
    lines.append("| Date | Weekday | Sunrise (IST) | Sunset (IST) | Tithi at Sunrise | Paksha | Near boundary | Rahu Kaal (IST) | Astronomical Event |")
    lines.append("| :--- | :--- | :---: | :---: | :--- | :--- | :---: | :---: | :--- |")

    for d in sorted_dates:
        row = days[d]
        events_str = "; ".join(row["events"]) if row["events"] else "-"
        rahu_str = f"{row['rahu_kaal']['start']} – {row['rahu_kaal']['end']}"
        near_str = "Yes" if row.get("near_boundary") else "-"
        lines.append(f"| {row['date']} | {row['weekday'][:3]} | {row['sunrise_short']} | {row['sunset_short']} | {row['tithi_name']} | {row['paksha']} | {near_str} | {rahu_str} | {events_str} |")

    table_md = "\n".join(lines)
    os.makedirs("docs", exist_ok=True)
    with open("docs/panchang_2027_spot_check.md", "w", encoding="utf-8") as f:
        f.write(table_md)
    print(f"Generated spot-check table with {len(sorted_dates)} dates at docs/panchang_2027_spot_check.md")
    return table_md

if __name__ == "__main__":
    data = generate_panchang_2027()
    table = build_spot_check_table(data)
    print("\n--- SAMPLE SPOT CHECK (FIRST 10 ROWS) ---")
    for l in table.splitlines()[6:18]:
        print(l)
