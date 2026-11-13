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
    
    dist_prev = (e0 - prev_target) % 360
    dist_next = (next_target - e0) % 360
    
    target = prev_target if dist_prev < dist_next else next_target
    sign = -1.0 if dist_prev < dist_next else 1.0
    
    approx_minutes = min(dist_prev, dist_next) * (60.0 / 0.549) * sign
    t_current = rising_utc + datetime.timedelta(minutes=approx_minutes)
    
    for _ in range(6):
        e_curr = get_elongation_deg(t_current)
        err = (e_curr - target + 180) % 360 - 180
        e_step = get_elongation_deg(t_current + datetime.timedelta(seconds=60))
        rate_deg_per_sec = ((e_step - e_curr + 180) % 360 - 180) / 60.0
        delta_sec = err / rate_deg_per_sec
        t_current = t_current - datetime.timedelta(seconds=delta_sec)
        if abs(delta_sec) < 0.001:
            break
            
    diff_sec = (t_current - rising_utc).total_seconds()
    return diff_sec / 60.0

current_date = datetime.date(2027, 1, 1)
end_date = datetime.date(2027, 12, 31)

flagged = []

while current_date <= end_date:
    d_str = current_date.strftime("%Y-%m-%d")
    local_midnight_ist = datetime.datetime.combine(current_date, datetime.time(0, 0, 0))
    utc_search_start = local_midnight_ist - datetime.timedelta(hours=5, minutes=30)
    delhi.date = ephem.Date(utc_search_start)
    rising_utc = delhi.next_rising(ephem.Sun(), start=ephem.Date(utc_search_start)).datetime()
    
    mins = find_exact_boundary_minutes(rising_utc)
    abs_mins = abs(mins)
    if abs_mins <= 45.0:
        flagged.append((d_str, abs_mins, mins))
    current_date += datetime.timedelta(days=1)

print(f"Total days with |minutes| <= 45: {len(flagged)}")
for d_str, abs_m, raw_m in flagged:
    direction = "after sunrise" if raw_m > 0 else "before sunrise"
    print(f"  {d_str}: {abs_m:.1f} min ({direction})")
