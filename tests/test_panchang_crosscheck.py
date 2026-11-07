import unittest
import json
import datetime
import math
import ephem

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

class TestPanchangFullYear(unittest.TestCase):
    def setUp(self):
        with open("data/panchang_2027_delhi.json", "r", encoding="utf-8") as f:
            self.panchang = json.load(f)
            self.days = self.panchang["days"]

    def test_total_365_days(self):
        self.assertEqual(len(self.days), 365, "Panchang must contain exactly 365 days")

    def test_independent_recomputation_365_days(self):
        """
        Independent re-computation for every single day:
        Compute sunrise instant S(D) for New Delhi and verify elongation matches tithi index.
        """
        delhi = ephem.Observer()
        delhi.lat = DELHI_LAT
        delhi.lon = DELHI_LON
        delhi.elevation = DELHI_ELEV

        current_date = datetime.date(2027, 1, 1)
        end_date = datetime.date(2027, 12, 31)
        disagreements = []

        while current_date <= end_date:
            d_str = current_date.strftime("%Y-%m-%d")
            stored = self.days[d_str]

            local_midnight_ist = datetime.datetime.combine(current_date, datetime.time(0, 0, 0))
            utc_search_start = local_midnight_ist - datetime.timedelta(hours=5, minutes=30)
            delhi.date = ephem.Date(utc_search_start)
            sun = ephem.Sun()
            rising_utc = delhi.next_rising(sun, start=ephem.Date(utc_search_start)).datetime()

            delhi.date = ephem.Date(rising_utc)
            sun_obs = ephem.Sun(delhi)
            moon_obs = ephem.Moon(delhi)
            diff = (ephem.Ecliptic(moon_obs).lon - ephem.Ecliptic(sun_obs).lon) % (2 * math.pi)
            diff_deg = math.degrees(diff)
            tithi_idx = int(diff_deg // 12)
            expected_tithi = TITHI_NAMES[tithi_idx]

            if stored["tithi_name"] != expected_tithi:
                disagreements.append((d_str, stored["tithi_name"], expected_tithi, diff_deg))

            current_date += datetime.timedelta(days=1)

        self.assertEqual(
            len(disagreements), 0,
            f"Found {len(disagreements)} disagreements across 365 days: {disagreements}"
        )
        print("\nPASS: 365-day astronomical tithi cross-check: 0 disagreements out of 365 days.")

if __name__ == '__main__':
    unittest.main()
