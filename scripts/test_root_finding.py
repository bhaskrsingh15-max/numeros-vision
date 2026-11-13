import datetime
import math
import ephem

DELHI_LAT = '28.6139'
DELHI_LON = '77.2090'
DELHI_ELEV = 216

delhi = ephem.Observer()
delhi.lat = DELHI_LAT
delhi.lon = DELHI_LON
delhi.elevation = DELHI_ELEV

def get_elongation_deg(utc_dt):
    delhi.date = ephem.Date(utc_dt)
    sun_obs = ephem.Sun(delhi)
    moon_obs = ephem.Moon(delhi)
    sun_ecl = ephem.Ecliptic(sun_obs)
    moon_ecl = ephem.Ecliptic(moon_obs)
    diff = (moon_ecl.lon - sun_ecl.lon) % (2 * math.pi)
    return math.degrees(diff)

def find_exact_boundary_minutes(rising_utc):
    e0 = get_elongation_deg(rising_utc)
    t_idx = int(e0 // 12)
    prev_target = (t_idx * 12) % 360
    next_target = ((t_idx + 1) * 12) % 360
    
    # Distance in degrees at sunrise
    dist_prev = (e0 - prev_target) % 360
    dist_next = (next_target - e0) % 360
    
    target = prev_target if dist_prev < dist_next else next_target
    sign = -1.0 if dist_prev < dist_next else 1.0
    
    # Root finding for elongation(t) - target == 0
    # Search in window [rising_utc - 12h, rising_utc + 12h]
    # Use secant method starting from linear estimate
    approx_minutes = min(dist_prev, dist_next) * (60.0 / 0.549) * sign
    t_current = rising_utc + datetime.timedelta(minutes=approx_minutes)
    
    for _ in range(5):
        e_curr = get_elongation_deg(t_current)
        err = (e_curr - target + 180) % 360 - 180  # in [-180, 180]
        # Rate of elongation change around t_current
        e_step = get_elongation_deg(t_current + datetime.timedelta(seconds=60))
        rate_deg_per_sec = ((e_step - e_curr + 180) % 360 - 180) / 60.0
        delta_sec = err / rate_deg_per_sec
        t_current = t_current - datetime.timedelta(seconds=delta_sec)
        if abs(delta_sec) < 0.01:
            break
            
    diff_sec = (t_current - rising_utc).total_seconds()
    minutes = diff_sec / 60.0
    return minutes

# Check 18 Jun, 19 Jun, 22 Jul
for d_str in ['2027-06-18', '2027-06-19', '2027-07-22']:
    dt = datetime.datetime.strptime(d_str, "%Y-%m-%d")
    local_midnight_ist = dt
    utc_search_start = local_midnight_ist - datetime.timedelta(hours=5, minutes=30)
    delhi.date = ephem.Date(utc_search_start)
    rising_utc = delhi.next_rising(ephem.Sun(), start=ephem.Date(utc_search_start)).datetime()
    m = find_exact_boundary_minutes(rising_utc)
    print(f"{d_str}: exact root-finding minutes = {abs(m):.2f} min (raw signed: {m:.2f} min)")
