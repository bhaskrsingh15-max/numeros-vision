"""
ORCHESTRATOR: TOPIC ROUTING AND ENGINE SYNTHESIS LAYER
Vedic-LoShu-BNN-LalKitab Predictive Software

PURPOSE (Gap 3 fix from the architecture audit): given a user's free-text
question and their already-computed chart data (from phase1/phase2/phase3/
phase4/phase5), this layer decides WHICH engines are actually relevant to
the question, runs only those (cost control -- never runs all five engines
for a narrow question), and hands their outputs to phase6's correlation
engine for final synthesis.

This file does NOT call any AI model itself -- topic classification here is
simple keyword-based rule matching (cheap, deterministic, fast). A real
production version could swap this for a cheap small-LLM classifier later
if keyword coverage proves too narrow, without changing anything else in
the pipeline.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from phase2_d60_engine import run_full_d60_analysis
from phase4_bnn_engine import run_full_bnn_analysis, summarize_for_topic
from phase5_lal_kitab_engine import run_full_lal_kitab_analysis, summarize_for_topic as lal_kitab_summarize
from phase7_kp_engine import analyze_kp_sub_lord, absolute_longitude_to_nakshatra_and_degree, summarize_for_topic as kp_summarize
from phase6_correlation_engine import run_correlated_prediction
from phase8_btr_engine import run_full_btr_analysis


# ---------------------------------------------------------------------------
# STEP 1: TOPIC CLASSIFICATION (simple keyword rules, cheap and transparent)
# ---------------------------------------------------------------------------
TOPIC_KEYWORDS = {
    "career":   ["job", "career", "naukri", "business", "kaam", "promotion", "office", "profession"],
    "marriage": ["marriage", "shaadi", "vivah", "spouse", "wife", "husband", "partner"],
    "wealth":   ["money", "paisa", "wealth", "dhan", "income", "finance", "loan", "debt"],
    "health":   ["health", "sehat", "bimari", "illness", "disease", "surgery"],
    "property": ["property", "ghar", "house", "vehicle", "car", "makan", "zameen", "land"],
}

# Standard astronomical topocentric coordinate lookup table
CITY_COORDINATES = {
    "delhi": (28.6139, 77.2090, "Asia/Kolkata"),
    "new delhi": (28.6139, 77.2090, "Asia/Kolkata"),
    "mumbai": (19.0760, 72.8777, "Asia/Kolkata"),
    "bangalore": (12.9716, 77.5946, "Asia/Kolkata"),
    "bengaluru": (12.9716, 77.5946, "Asia/Kolkata"),
    "hyderabad": (17.3850, 78.4867, "Asia/Kolkata"),
    "chennai": (13.0827, 80.2707, "Asia/Kolkata"),
    "kolkata": (22.5726, 88.3639, "Asia/Kolkata"),
    "pune": (18.5204, 73.8567, "Asia/Kolkata"),
    "ahmedabad": (23.0225, 72.5714, "Asia/Kolkata"),
    "jaipur": (26.9124, 75.7873, "Asia/Kolkata"),
    "lucknow": (26.8467, 80.9462, "Asia/Kolkata"),
    "chandigarh": (30.7333, 76.7794, "Asia/Kolkata"),
    "patna": (25.5941, 85.1376, "Asia/Kolkata"),
    "varanasi": (25.3176, 82.9739, "Asia/Kolkata"),
    "bhopal": (23.2599, 77.4126, "Asia/Kolkata"),
    "indore": (22.7196, 75.8577, "Asia/Kolkata"),
    "nagpur": (21.1458, 79.0882, "Asia/Kolkata"),
    "dubai": (25.2048, 55.2708, "Asia/Dubai"),
    "london": (51.5074, -0.1278, "Europe/London"),
    "new york": (40.7128, -74.0060, "America/New_York"),
    "san francisco": (37.7749, -122.4194, "America/Los_Angeles"),
    "toronto": (43.6532, -79.3832, "America/Toronto"),
    "singapore": (1.3521, 103.8198, "Asia/Singapore"),
    "sydney": (-33.8688, 151.2093, "Australia/Sydney"),
}

def resolve_spatiotemporal_coords(place_name: str = "", lat: float = None, lon: float = None, tz: str = None):
    if lat is not None and lon is not None:
        return float(lat), float(lon), tz or "Asia/Kolkata"
    
    clean_place = (place_name or "").lower().strip()
    for city, (c_lat, c_lon, c_tz) in CITY_COORDINATES.items():
        if city in clean_place:
            return c_lat, c_lon, tz or c_tz
            
    # Default topocentric anchor: Delhi, India
    return 28.6139, 77.2090, tz or "Asia/Kolkata"

def classify_topic(question_text):
    text = question_text.lower()
    scores = {topic: 0 for topic in TOPIC_KEYWORDS}
    for topic, keywords in TOPIC_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[topic] += 1
    best_topic = max(scores, key=scores.get)
    if scores[best_topic] == 0:
        return "general"
    return best_topic


# ---------------------------------------------------------------------------
# STEP 2: ENGINE ROUTING -- decide which engines to actually run for a topic
# ---------------------------------------------------------------------------
# Cost-control principle: numerology and name_numerology are cheap to always
# include (pure arithmetic, near-zero cost); astrology and BNN require chart
# data already computed once at onboarding (reused, not recomputed); Lal
# Kitab is included only when its engine exists (Gap-4-safe placeholder).
ENGINES_PER_TOPIC = {
    "career":   ["numerology", "astrology", "bnn", "lal_kitab", "kp_astrology"],
    "marriage": ["numerology", "astrology", "name_numerology", "bnn", "lal_kitab", "kp_astrology"],
    "wealth":   ["numerology", "astrology", "bnn", "lal_kitab", "kp_astrology"],
    "health":   ["astrology", "bnn", "lal_kitab", "kp_astrology"],
    "property": ["astrology", "bnn", "lal_kitab", "kp_astrology"],
    "general":  ["numerology", "astrology"],
}


DEFAULT_CHART = {
    "Sun":     {"sign": "Scorpio",     "degree": 12.52, "retrograde": False, "house": 10},
    "Moon":    {"sign": "Sagittarius", "degree": 2.39,  "retrograde": False, "house": 5},
    "Mars":    {"sign": "Leo",         "degree": 27.70, "retrograde": False, "house": 3},
    "Mercury": {"sign": "Scorpio",     "degree": 5.75,  "retrograde": False, "house": 8},
    "Jupiter": {"sign": "Libra",       "degree": 6.67,  "retrograde": False, "house": 9},
    "Venus":   {"sign": "Sagittarius", "degree": 28.33, "retrograde": False, "house": 7},
    "Saturn":  {"sign": "Virgo",       "degree": 25.32, "retrograde": True,  "house": 6},
    "Rahu":    {"sign": "Cancer",      "degree": 1.36,  "retrograde": True,  "house": 3},
    "Ketu":    {"sign": "Capricorn",   "degree": 1.36,  "retrograde": True,  "house": 9},
}

# ---------------------------------------------------------------------------
# STEP 3: MAIN ENTRY POINT
# ---------------------------------------------------------------------------
def handle_question(question_text="", user_profile=None, current_age=None, **kwargs):
    """
    Unified entry point for orchestrating multi-system predictions.
    Supports both legacy dict signature `handle_question(question, user_profile, current_age)`
    and flexible keyword call `handle_question(question=..., name=..., dob=..., day=..., month=..., year=...)`.
    Automatically computes missing phase outputs deterministically without token burn.
    """
    clean_q = question_text or kwargs.get("question") or kwargs.get("question_text") or "general life guidance"
    profile = dict(user_profile) if isinstance(user_profile, dict) else {}
    
    # Merge additional kwargs into profile
    for k, v in kwargs.items():
        if k not in profile:
            profile[k] = v

    # Parse birth date if provided
    day = profile.get("day")
    month = profile.get("month")
    year = profile.get("year")
    dob_str = profile.get("dob") or kwargs.get("dob")
    if dob_str and (not day or not month or not year):
        try:
            import re
            parts = [int(p) for p in re.split(r'[/\-\.]', str(dob_str)) if p.isdigit()]
            if len(parts) >= 3:
                day, month, year = parts[0], parts[1], parts[2]
                if year < 100:
                    year += 1900
        except Exception:
            pass

    # Infer current age if not provided
    if current_age is None:
        current_age = profile.get("current_age") or kwargs.get("current_age")
        if current_age is None and year:
            current_age = max(1, 2026 - int(year))
        elif current_age is None:
            current_age = 35

    # 1. Auto-compute Phase 1 (Numerology) if not present
    if not profile.get("phase1_result") and day and month and year:
        try:
            from app.engine.vedic_numerology import analyze_vedic_numerology
            v_num = analyze_vedic_numerology(int(day), int(month), int(year))
            profile["phase1_result"] = {
                "driver": v_num.get("driver_number"),
                "conductor": v_num.get("conductor_number"),
                "driver_planet": v_num.get("driver_planet"),
                "conductor_planet": v_num.get("conductor_planet"),
                "friendly_numbers": v_num.get("friendly_numbers"),
                "enemy_numbers": v_num.get("enemy_numbers"),
            }
        except Exception:
            profile["phase1_result"] = {"driver": 1, "conductor": 1}

    # 2. Chart configuration (needed for D60, BNN, Lal Kitab)
    if not profile.get("chart"):
        profile["chart"] = profile.get("chart_data") or kwargs.get("chart") or kwargs.get("chart_data") or DEFAULT_CHART

    # 3. Auto-compute Phase 2 (Vedic D60 Karmic Roots) if not present or missing D60 metrics
    if profile.get("chart") and (not profile.get("phase2_result") or not profile["phase2_result"].get("karmic_strength_pct")):
        try:
            profile["phase2_result"] = run_full_d60_analysis(profile["chart"])
        except Exception:
            profile["phase2_result"] = {
                "rashi_vs_driver": "neutral",
                "nakshatra_vs_driver": "friend"
            }

    # 4. Auto-compute Phase 3 (Name Numerology) if not present
    client_name = profile.get("name") or kwargs.get("name") or "User"
    if not profile.get("phase3_result") and client_name:
        try:
            from app.engine.core_matrix_engine import calculate_chaldean_name
            c_name = calculate_chaldean_name(client_name)
            profile["phase3_result"] = {
                "name": client_name,
                "compound_sum": c_name.get("compound_sum"),
                "single_root": c_name.get("single_root"),
                "is_karmic": c_name.get("is_karmic", False)
            }
        except Exception:
            profile["phase3_result"] = {"name": client_name, "compound_sum": 15, "single_root": 6}

    # Auto-compute Lo Shu Grid (Core Birth Matrix) & Western Pythagorean if not present
    if not profile.get("phase_loshu_result") and day and month and year:
        try:
            from app.engine.lo_shu import analyze_lo_shu_grid
            profile["phase_loshu_result"] = analyze_lo_shu_grid(int(day), int(month), int(year))
        except Exception:
            pass

    if not profile.get("phase_pythagorean_result") and day and month and year:
        try:
            from app.engine.pythagorean_engine import analyze_pythagorean_full
            profile["phase_pythagorean_result"] = analyze_pythagorean_full(int(day), int(month), int(year), client_name)
        except Exception:
            pass

    topic = classify_topic(clean_q)
    engines_to_run = ENGINES_PER_TOPIC.get(topic, ["numerology", "astrology"])

    engine_kwargs = {}
    if "numerology" in engines_to_run:
        engine_kwargs["phase1_result"] = profile.get("phase1_result")
    if "astrology" in engines_to_run:
        engine_kwargs["phase2_result"] = profile.get("phase2_result")
    if "name_numerology" in engines_to_run:
        engine_kwargs["phase3_result"] = profile.get("phase3_result")
    if "bnn" in engines_to_run and profile.get("chart"):
        bnn_full = run_full_bnn_analysis(profile["chart"], current_age=current_age)
        engine_kwargs["phase4_result"] = summarize_for_topic(bnn_full, topic if topic != "general" else "career")
    if "lal_kitab" in engines_to_run and profile.get("chart"):
        lal_kitab_full = run_full_lal_kitab_analysis(profile["chart"])
        engine_kwargs["phase5_result"] = lal_kitab_summarize(lal_kitab_full, topic if topic != "general" else "career")

    if "kp_astrology" in engines_to_run and profile.get("chart", {}).get("Moon"):
        moon_data = profile["chart"]["Moon"]
        signs = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
                 "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
        sign_name = moon_data.get("sign", "Aries")
        sign_idx = signs.index(sign_name) if sign_name in signs else 0
        moon_absolute_longitude = sign_idx * 30 + moon_data.get("degree", 0.0)
        kp_full = analyze_kp_sub_lord(moon_absolute_longitude)
        engine_kwargs["phase7_result"] = kp_summarize(kp_full, topic if topic != "general" else "career")

    # Extract spatiotemporal astronomical coordinates
    birth_time = (
        profile.get("birth_time")
        or kwargs.get("birth_time")
        or profile.get("time")
        or kwargs.get("time")
        or "12:00"
    )
    place_name = (
        profile.get("place_name")
        or kwargs.get("place_name")
        or profile.get("place")
        or kwargs.get("place")
        or profile.get("city")
        or kwargs.get("city")
        or "Delhi, India"
    )
    raw_lat = profile.get("latitude") or kwargs.get("latitude") or profile.get("lat") or kwargs.get("lat")
    raw_lon = profile.get("longitude") or kwargs.get("longitude") or profile.get("lon") or kwargs.get("lon")
    raw_tz = profile.get("timezone") or kwargs.get("timezone") or profile.get("tz") or kwargs.get("tz")
    
    lat, lon, tz = resolve_spatiotemporal_coords(place_name, raw_lat, raw_lon, raw_tz)
    geo_context = {
        "birth_time": str(birth_time),
        "place_name": str(place_name),
        "latitude": round(float(lat), 4),
        "longitude": round(float(lon), 4),
        "timezone": str(tz)
    }

    engine_kwargs["chart"] = profile.get("chart")
    engine_kwargs["geo_context"] = geo_context
    result = run_correlated_prediction(topic, **engine_kwargs)
    result["classified_topic"] = topic
    result["engines_routed"] = engines_to_run
    result["profile_summary"] = {
        "name": client_name,
        "topic": topic,
        "current_age": current_age,
        "birth_time": geo_context["birth_time"],
        "place_name": geo_context["place_name"],
        "latitude": geo_context["latitude"],
        "longitude": geo_context["longitude"],
        "timezone": geo_context["timezone"]
    }
    return result


# ---------------------------------------------------------------------------
# STEP 4: BTR (BIRTH TIME RECTIFICATION) -- SEPARATE ENTRY POINT
# ---------------------------------------------------------------------------
def handle_btr_request(candidates_full, events):
    """
    candidates_full / events: same shape phase8_btr_engine.run_full_btr_analysis()
      expects -- see that function's own docstring for the full field list.
    """
    result = run_full_btr_analysis(candidates_full, events)
    result["request_type"] = "birth_time_rectification"
    return result


if __name__ == "__main__":
    import json

    user_profile = {
        "phase1_result": {"driver": 1, "conductor": 2, "relation": "friend"},
        "phase2_result": {"rashi_vs_driver": "neutral", "nakshatra_vs_driver": "friend"},
        "chart": {
            "Sun":     {"sign": "Scorpio",     "degree": 12.52, "retrograde": False},
            "Moon":    {"sign": "Sagittarius", "degree": 2.39,  "retrograde": False},
            "Mars":    {"sign": "Leo",         "degree": 27.70, "retrograde": False},
            "Mercury": {"sign": "Scorpio",     "degree": 5.75,  "retrograde": False},
            "Jupiter": {"sign": "Libra",       "degree": 6.67,  "retrograde": False},
            "Venus":   {"sign": "Sagittarius", "degree": 28.33, "retrograde": False},
            "Saturn":  {"sign": "Virgo",       "degree": 25.32, "retrograde": True},
            "Rahu":    {"sign": "Cancer",      "degree": 1.36,  "retrograde": True},
            "Ketu":    {"sign": "Capricorn",   "degree": 1.36,  "retrograde": True},
        },
    }

    question = "mera career kaisa rahega is saal"
    result = handle_question(question, user_profile, current_age=44)
    print(json.dumps(result, indent=2))

    print("\n\n=== ORCHESTRATOR-WIRED BTR REQUEST (real chart Sun/Moon) ===\n")
    from phase8_btr_engine import mahadasha_periods

    shared_mahadashas = mahadasha_periods("Ketu", 1981.911, balance_fraction_remaining=0.35)
    btr_events = [
        {"type": "job_start", "year": 2005.5},
        {"type": "marriage", "year": 2010.2},
        {"type": "child_birth", "year": 2013.7},
    ]
    btr_candidates = [
        {
            "label": "16:15 (recorded time)",
            "mahadasha_list": shared_mahadashas,
            "planet_houses": {"Surya": 10, "Shukra": 7, "Chandra": 5, "Guru": 9, "Mangal": 3, "Ketu": 9, "Shani": 6, "Rahu": 3, "Budh": 8},
            "house_lords": {7: "Shukra", 10: "Surya", 5: "Chandra", 6: "Budh", 8: "Mangal"},
            "sunrise_decimal_hours": 6 + 54/60,
            "birth_decimal_hours": 16 + 15/60,
            "sun_longitude_deg": 222.52,
            "moon_longitude_deg": 242.39,
            "lagna_longitude_deg": 15.0,
            "actual_gender": "male",
            "lagna_star_lord": "Mangal", "lagna_sub_lord": "Shukra",
            "ninth_star_lord": "Guru", "ninth_sub_lord": "Budh",
            "gender_house_lord_planet": "Mangal",
            "gender_house_lord_sign": "Leo",
            "gender_house_lord_nakshatra_lord": "Surya",
            "gender_house_lord_sign_lord": "Surya",
            "gender_house_lord_star_lord": "Surya",
            "gender_house_lord_conjoined_with": None,
            "moon_star_lord": "Ketu", "moon_sub_lord": "Ketu", "moon_sign_lord": "Guru",
        },
        {
            "label": "16:45 (30-min-later alternate)",
            "mahadasha_list": shared_mahadashas,
            "planet_houses": {"Surya": 10, "Shukra": 7, "Chandra": 5, "Guru": 9, "Mangal": 3, "Ketu": 9, "Shani": 6, "Rahu": 3, "Budh": 8},
            "house_lords": {7: "Shukra", 10: "Surya", 5: "Chandra", 6: "Budh", 8: "Mangal"},
            "sunrise_decimal_hours": 6 + 54/60,
            "birth_decimal_hours": 16 + 45/60,
            "sun_longitude_deg": 222.52,
            "moon_longitude_deg": 242.39,
            "lagna_longitude_deg": 22.0,
            "actual_gender": "male",
            "lagna_star_lord": "Mangal", "lagna_sub_lord": "Rahu",
            "ninth_star_lord": "Guru", "ninth_sub_lord": "Ketu",
            "gender_house_lord_planet": "Mangal",
            "gender_house_lord_sign": "Leo",
            "gender_house_lord_nakshatra_lord": "Surya",
            "gender_house_lord_sign_lord": "Surya",
            "gender_house_lord_star_lord": "Surya",
            "gender_house_lord_conjoined_with": None,
            "moon_star_lord": "Ketu", "moon_sub_lord": "Ketu", "moon_sign_lord": "Guru",
        },
    ]

    btr_result = handle_btr_request(btr_candidates, btr_events)
    print(json.dumps(btr_result, indent=2))
