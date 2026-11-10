import datetime
import random

# Implementation 1: Exact logic from index.html / your-reading.html
def calc_loshu_frontend(d: int, m: int, y: int):
    total_dob_digits = f"{d:02d}{m:02d}{y:04d}"
    counts = {n: 0 for n in range(1, 10)}
    for ch in total_dob_digits:
        if ch != '0':
            counts[int(ch)] += 1
    
    present = [n for n in range(1, 10) if counts[n] > 0]
    missing = [n for n in range(1, 10) if counts[n] == 0]
    
    planes_def = [
        ('Mental Plane', [4, 9, 2]),
        ('Emotional Plane', [3, 5, 7]),
        ('Practical Plane', [8, 1, 6]),
        ('Thought Plane', [4, 3, 8]),
        ('Will Plane', [9, 5, 1]),
        ('Action Plane', [2, 7, 6]),
        ('Golden Raj Yoga', [4, 5, 6]),
        ('Silver Raj Yoga', [2, 5, 8])
    ]
    
    planes = {}
    for name, digits in planes_def:
        cnt = sum(1 for dig in digits if counts[dig] > 0)
        pct = round((cnt / len(digits)) * 100)
        status = 'COMPLETE' if pct == 100 else ('ACTIVE' if pct > 33 else 'DORMANT')
        planes[name] = {'count': cnt, 'status': status}
        
    return counts, present, missing, planes

# Implementation 2: Logic from _worker.js viewFor
def calc_loshu_worker(d: int, m: int, y: int):
    total_dob_digits = f"{d:02d}{m:02d}{y:04d}"
    counts = {n: 0 for n in range(1, 10)}
    for ch in total_dob_digits:
        if ch != '0':
            counts[int(ch)] += 1
    
    present = [n for n in range(1, 10) if counts[n] > 0]
    missing = [n for n in range(1, 10) if counts[n] == 0]
    
    planes_def = [
        ('Mental Plane', [4, 9, 2]),
        ('Emotional Plane', [3, 5, 7]),
        ('Practical Plane', [8, 1, 6]),
        ('Thought Plane', [4, 3, 8]),
        ('Will Plane', [9, 5, 1]),
        ('Action Plane', [2, 7, 6]),
        ('Golden Raj Yoga', [4, 5, 6]),
        ('Silver Raj Yoga', [2, 5, 8])
    ]
    
    planes = {}
    for name, digits in planes_def:
        cnt = sum(1 for dig in digits if counts[dig] > 0)
        pct = round((cnt / len(digits)) * 100)
        status = 'COMPLETE' if pct == 100 else ('ACTIVE' if pct > 33 else 'DORMANT')
        planes[name] = {'count': cnt, 'status': status}
        
    return counts, present, missing, planes

def run_parity_test():
    random.seed(42)
    mismatches = 0
    start_date = datetime.date(1950, 1, 1)
    end_date = datetime.date(2025, 12, 31)
    total_days = (end_date - start_date).days

    test_dobs = [
        (28, 11, 1981), # Bhaskr Singh
        (29, 2, 2000),  # Leap year
        (1, 1, 2001),   # Edge 1
        (31, 12, 1999), # Edge 31
        (18, 10, 1990), # Alexander Vance
    ]

    for _ in range(195):
        rnd_day = start_date + datetime.timedelta(days=random.randint(0, total_days))
        test_dobs.append((rnd_day.day, rnd_day.month, rnd_day.year))

    for idx, (d, m, y) in enumerate(test_dobs, start=1):
        c1, p1, m1, pl1 = calc_loshu_frontend(d, m, y)
        c2, p2, m2, pl2 = calc_loshu_worker(d, m, y)
        
        if c1 != c2 or p1 != p2 or m1 != m2 or pl1 != pl2:
            mismatches += 1
            print(f"Mismatch at DOB {d:02d}-{m:02d}-{y}: {c1} vs {c2}")

    print(f"Parity test completed across {len(test_dobs)} DOBs. Total mismatches: {mismatches}")
    assert mismatches == 0, f"Expected 0 mismatches, got {mismatches}"

if __name__ == '__main__':
    run_parity_test()
