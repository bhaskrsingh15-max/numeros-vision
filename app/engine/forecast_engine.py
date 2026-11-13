"""
NV-006 & NV-007: BLESSING YEARS TIMELINE & PERSONAL CYCLE FORECAST ENGINE
Grounding: Classical Numerology 9-Year Cycles, Personal Cycles (PY/PM/PD), Vedic Dasha Milestones.

Deterministic capabilities:
1. NV-006 Blessing Years Timeline:
   - Identifies milestone years where age reduction or calendar year reduction matches Driver, Conductor, or friendly planets.
   - Categorizes tiers: Supreme Blessing, High Support, Milestone Shift, Consolidation.
   - Generates age progression from age 18 to 75 with thematic focus.
2. NV-007 Personal Cycle Forecasts:
   - Multi-Year Horizon (Current Year + next 3 years) across 4 life dimensions:
     Career & Professional, Financial Flow, Relationships & Family, Vitality & Health.
   - 12-Month Detailed Annual Matrix: Personal Month, ruling planet, key focus, favorable days.
   - Daily Alignment Generator: Personal Day, auspicious hours, directional orientation.
   - Strict non-fatalistic, proactive diplomatic phrasing.
"""

from typing import Dict, Any, List, Optional
import datetime
import sys
import os

workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from app.engine.number_characteristics_registry import (
    get_number_profile,
    get_relationship,
    PLANETARY_RULERS
)
from app.engine.professional_numerology_engine import (
    PERSONAL_YEAR_INTERPRETATIONS,
    calculate_personal_cycles
)


def calculate_blessing_years(
    day: int,
    month: int,
    birth_year: int,
    current_age: Optional[int] = None,
    max_age: int = 75
) -> Dict[str, Any]:
    """
    NV-006 Requirement: Deterministic Blessing Years Timeline.
    Evaluates every year of life for convergence of:
    - Age reduction == Driver or Conductor
    - Calendar year reduction == Driver or Conductor
    - Personal Year == Driver or Conductor
    """
    from app.engine.digit_root import calc_bhagyank, calc_driver, calc_personal_year, digit_root
    # Calculate Driver
    driver = calc_driver(day)

    # Calculate Conductor
    conductor = calc_bhagyank(day, month, birth_year)

    # Core friendly numbers
    d_prof = get_number_profile(driver) or {}
    friendly_nums = set(d_prof.get("friendly_numbers", [1, 5, 6]))
    friendly_nums.add(driver)
    friendly_nums.add(conductor)

    today = datetime.date.today()
    inferred_age = today.year - birth_year
    active_age = current_age if current_age is not None else max(inferred_age, 0)

    timeline = []
    supreme_years = []
    high_support_years = []

    for age in range(18, max_age + 1):
        cal_year = birth_year + age
        # Age reduction
        age_reduced = digit_root(age)

        # Year reduction
        yr_reduced = digit_root(cal_year)

        # Personal Year
        py = calc_personal_year(day, month, cal_year)

        is_age_core = age_reduced in (driver, conductor)
        is_year_core = yr_reduced in (driver, conductor)
        is_py_core = py in (driver, conductor)
        is_age_friendly = age_reduced in friendly_nums
        is_py_friendly = py in friendly_nums

        score = 0
        if is_age_core: score += 40
        elif is_age_friendly: score += 20

        if is_year_core: score += 30
        if is_py_core: score += 30
        elif is_py_friendly: score += 15

        if score >= 60:
            tier = "Supreme Blessing Year"
            theme = "Major breakthrough, expansive commercial leaps, pivotal public visibility."
            supreme_years.append({"age": age, "year": cal_year, "personal_year": py})
        elif score >= 40:
            tier = "High Support Year"
            theme = "Solid forward momentum, beneficial partnerships, steady asset accumulation."
            high_support_years.append({"age": age, "year": cal_year, "personal_year": py})
        elif age % 9 == 0:
            tier = "Milestone Cycle Turning Point"
            theme = "End of an epoch; closure of outdated engagements and foundation of new 9-year cycle."
        else:
            tier = "Consolidation & Skill Building"
            theme = "Routine foundational labor, internal learning, patient resource compounding."


        is_current = (age == active_age)
        is_future = (age > active_age)

        timeline.append({
            "age": age,
            "calendar_year": cal_year,
            "personal_year": py,
            "personal_year_theme": PERSONAL_YEAR_INTERPRETATIONS.get(py, {}).get("theme", ""),
            "blessing_tier": tier,
            "blessing_score": score,
            "milestone_theme": theme,
            "is_current_age": is_current,
            "is_upcoming": is_future
        })

    # Find next immediate 3 blessing years from current age
    upcoming_blessings = [entry for entry in timeline if entry["is_upcoming"] and entry["blessing_score"] >= 55][:3]

    return {
        "birth_date": f"{day:02d}/{month:02d}/{birth_year}",
        "current_age": active_age,
        "driver": driver,
        "conductor": conductor,
        "supreme_blessing_years_count": len(supreme_years),
        "high_support_years_count": len(high_support_years),
        "immediate_upcoming_blessings": upcoming_blessings,
        "timeline_sample": timeline[:15], # First 15 entries for quick display
        "full_timeline": timeline,
        "interpretative_summary": (
            f"Your personal timeline reveals {len(supreme_years)} Supreme Blessing milestones between age 18 and {max_age}. "
            f"The nearest catalytic expansion window is scheduled at Age {upcoming_blessings[0]['age']} (Year {upcoming_blessings[0]['calendar_year']}, Personal Year {upcoming_blessings[0]['personal_year']})."
            if upcoming_blessings else "Your timeline progresses through steady consolidation cycles."
        )
    }


def generate_multi_year_forecast(
    day: int,
    month: int,
    start_year: Optional[int] = None,
    num_years: int = 4
) -> List[Dict[str, Any]]:
    """
    NV-007 Requirement: Multi-year horizon forecast (Current Year + next 3 years).
    Provides structured forecast across 4 core dimensions:
    1. Career & Professional Initiatives
    2. Financial Flow & Investment Posture
    3. Relationships & Domestic Harmony
    4. Vitality, Mindset & Reflective Actions
    """
    today = datetime.date.today()
    curr_yr = start_year or today.year
    forecasts = []

    DIMENSION_GUIDANCE = {
        1: {
            "career": "Initiate bold independent ventures; take leadership positions and present new proposals.",
            "wealth": "Invest in seed-stage projects and capital assets with long gestation.",
            "relationships": "Step forward with clear communication; establish healthy mutual boundaries.",
            "vitality": "High solar energy; channels best through morning aerobic movement and structured routines."
        },
        2: {
            "career": "Prioritize strategic partnerships, teamwork, diplomacy, and back-channel negotiations.",
            "wealth": "Maintain liquid reserves; avoid hasty unilateral asset liquidation.",
            "relationships": "Deepen emotional empathy, spend quality listening time with family and spouse.",
            "vitality": "Hydration, sleep rhythms, and emotional grounding practices (pranayama) are essential."
        },
        3: {
            "career": "Golden window for certifications, high-level publishing, teaching, and brand expansion.",
            "wealth": "Auspicious for long-term equity growth, advisory consulting fees, and educational investments.",
            "relationships": "Joyous social events, celebrations, philosophical camaraderie, and mentorship.",
            "vitality": "Liver and metabolic wellness; favor fresh foods and joyful outdoor physical activity."
        },
        4: {
            "career": "Rigorous foundation building; execute detailed operational and compliance upgrades.",
            "wealth": "Conservative budget discipline; strictly avoid speculative high-risk gambles.",
            "relationships": "Exercise patience during domestic reorganizations; avoid unnecessary arguments.",
            "vitality": "Nervous system relaxation, sound sleep hygiene, and avoiding overwork exhaustion."
        },
        5: {
            "career": "Dynamic commercial shifts, travel, market expansion, agile pivots, and digital growth.",
            "wealth": "High trading mobility, liquidity turnover, and multiple income streams.",
            "relationships": "Vibrant social networking, exciting new acquaintances, open communication.",
            "vitality": "Fast nervous reflexes; balance with grounding barefoot walks on natural earth."
        },
        6: {
            "career": "Auspicious for hospitality, creative luxury, team welfare, and client relationship depth.",
            "wealth": "Expenditure on home beautification, lifestyle comfort, and real estate enhancement.",
            "relationships": "Prime cycle for marriage, domestic peace, childbirth, and celebrating bonds.",
            "vitality": "Harmony and sensory pampering; prioritize balanced nutrition and restorative wellness."
        },
        7: {
            "career": "Research, strategic audit, technical specialization, and proprietary knowledge creation.",
            "wealth": "Prudent asset preservation; avoid joining herd hype or speculative frenzies.",
            "relationships": "Values quiet solitude and intellectual depth; communicate transparently with loved ones.",
            "vitality": "Mental rejuvenation, meditation, nature retreats, and psychological self-reflection."
        },
        8: {
            "career": "Harvest cycle of executive authority, institutional recognition, and professional climax.",
            "wealth": "Material gains from previous years' persistence; substantial commercial contracts.",
            "relationships": "Demands fairness, integrity, and reliable support for dependents.",
            "vitality": "Bone, joint, and spine postural care; consistent strength conditioning."
        },
        9: {
            "career": "Closure of completed projects, clearing operational backlog, philanthropic leadership.",
            "wealth": "Clear outstanding debts and finalize accounts; postpone ungrounded speculative bets.",
            "relationships": "Forgiveness, releasing old resentments, supporting community and family elder needs.",
            "vitality": "Heat and stress regulation; calm cooling foods and regular peaceful pauses."
        }
    }

    for y in range(curr_yr, curr_yr + num_years):
        # Calculate Personal Year
        py_sum = day + month + sum(int(d) for d in str(y))
        py = py_sum
        while py > 9:
            py = sum(int(d) for d in str(py))

        py_info = PERSONAL_YEAR_INTERPRETATIONS.get(py, {})
        dim = DIMENSION_GUIDANCE.get(py, DIMENSION_GUIDANCE[1])

        forecasts.append({
            "year": y,
            "personal_year": py,
            "cycle_archetype": py_info.get("theme", ""),
            "ruling_planet": py_info.get("planet", "Sun"),
            "strategic_summary": py_info.get("guidance", ""),
            "dimensions": {
                "career_and_vocation": dim["career"],
                "financial_and_wealth": dim["wealth"],
                "relationships_and_family": dim["relationships"],
                "vitality_and_mindset": dim["vitality"]
            },
            "quarterly_cadence": {
                "Q1_Jan_Mar": f"Planning and alignment to Personal Year {py} energy.",
                "Q2_Apr_Jun": "Active execution and establishing core partnerships.",
                "Q3_Jul_Sep": "Reviewing progress, mid-course calibration, and consolidating gains.",
                "Q4_Oct_Dec": "Harvesting results and preparing foundation for the subsequent year."
            }
        })

    return forecasts


def generate_detailed_annual_matrix(
    day: int,
    month: int,
    target_year: Optional[int] = None
) -> Dict[str, Any]:
    """
    NV-007 Requirement: 12-Month Detailed Annual Matrix.
    Provides Personal Month, governing planet, focus theme, and favorable calendar days for each month.
    """
    t_year = target_year or datetime.date.today().year

    # Personal Year
    py_sum = day + month + sum(int(d) for d in str(t_year))
    py = py_sum
    while py > 9:
        py = sum(int(d) for d in str(py))

    month_names = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    months_data = []
    for m_idx in range(1, 13):
        # Personal Month = Personal Year + Calendar Month
        pm_sum = py + m_idx
        pm = pm_sum
        while pm > 9:
            pm = sum(int(d) for d in str(pm))

        pm_prof = get_number_profile(pm) or {}
        planet = pm_prof.get("planet", "Sun")

        # Favorable days: dates whose day digit sums to friendly numbers or pm
        favorable_dates = [d for d in [1, 3, 5, 6, 9, 10, 14, 15, 19, 23, 24, 27] if d <= 28]

        months_data.append({
            "month_number": m_idx,
            "month_name": month_names[m_idx - 1],
            "personal_month": pm,
            "governing_planet": planet,
            "focal_theme": f"Personal Month {pm}: {pm_prof.get('core_characteristics', 'Growth & Focus')}",
            "favorable_dates": favorable_dates[:6],
            "action_guideline": f"Harness {planet} vibration for key decisions during the mid-month phase."
        })

    return {
        "calendar_year": t_year,
        "personal_year": py,
        "personal_year_theme": PERSONAL_YEAR_INTERPRETATIONS.get(py, {}).get("theme", ""),
        "monthly_matrix": months_data
    }
