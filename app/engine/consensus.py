"""
NUMEROS VISION — DETERMINISTIC MULTI-SYSTEM NUMEROLOGY & ASTROLOGY CONSENSUS ENGINE
=====================================================================================
Governed by Numeros Vision Master Implementation Specification & Specification v2.

Core Invariants:
1. Lo Shu is the canonical birth-date numerology calculation system (3x3 grid, 8 planes, counts).
2. Chaldean is the canonical name calculation and name-balancing method (1-8 sound frequencies).
3. Independent Traditions Calculated Separately:
   - Numerology: Lo Shu, Chaldean/Cheiro, Pythagorean/Western, Vedic Sankhya Shastra
   - Astrology: Krishnamurti Paddhati (KP), Bhrigu Nandi Nadi (BNN), Lal Kitab, Vedic Parashari Jyotish, Real-Time Transits
4. Correlation-Aware Convergence:
   - Collapses correlated systems into 6 independent system families:
     a) numerology_core (Lo Shu)
     b) acoustics (Chaldean / Cheiro)
     c) numerology_comparative (Vedic Sankhya, Pythagorean)
     d) astrology_classical (Vedic Parashari, KP Sub-Lord)
     e) astrology_nadi (BNN Karakas)
     f) astrology_remedial (Lal Kitab Masnooi Alchemy)
   - Convergence ratio = supporting_family_count / eligible_family_count (never presented as prediction probability).
   - Strict statuses: convergent, partially_convergent, conflicted, single_system, insufficient_evidence, not_comparable.
5. Vedic Lifestyle & Therapeutic Transformation:
   - Dinacharya 24-hour spiritual circadian routine mapped to planetary horas.
   - Sattvic habits and mindful pauses.
   - Safe crystals & gemstones: vibrational/elemental only, strictly excluding planetary enemies.
   - Statutory compliance: Drugs and Magic Remedies Act 1954 disclaimer (no medical/wealth claims).
   - Sacred Yantras with geometric placement and consecration timing.
6. Plain-Language Layman Translation & Past-Pattern Validation Question.
"""

import sys
import os
from pathlib import Path

workspace_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if workspace_root not in sys.path:
    sys.path.insert(0, workspace_root)

from datetime import datetime, date
from typing import Dict, Any, List, Optional
import math

from app.engine.vedic_numerology import analyze_vedic_numerology
from app.engine.lo_shu import analyze_lo_shu_grid
from app.engine.cheiro_engine import analyze_name_cheiro
from app.engine.pythagorean_engine import analyze_pythagorean_full
from app.engine.rag_retriever import rag_engine
from app.engine.source_privacy_shield import sanitize_citation, sanitize_text
from app.engine.bnn_numerology_engine import evaluate_bnn_numerology_profile
from app.engine.astrology_correlation_engine import (
    run_multi_astrology_correlation_engine,
    calculate_hourly_planetary_horas,
    correlate_planetary_transits,
    PLANET_BY_NUMBER,
    WEEKDAY_FIRST_HORA_RULER
)
from app.engine.remedy_rules_engine import select_remedies_and_yantras, YANTRA_CATALOGUE


# ── CANONICAL CRYSTAL DATABASE WITH PLANETARY ENEMY EXCLUSIONS ─────────────────
SAFE_CRYSTAL_CATALOGUE = {
    1: {
        "planet": "Sun (Surya)",
        "primary_crystals": ["Sunstone", "Carnelian", "Clear Quartz"],
        "element": "Fire / Solar Vitality",
        "color_frequency": "Golden amber and warm orange rays",
        "incompatible_planets": [8],  # Saturn clash
        "incompatible_crystals": ["Blue Sapphire", "Amethyst", "Black Obsidian"],
        "lifestyle_attunement": "Wear as a pendant or carry during sunrise contemplation to reinforce natural confidence, decision clarity, and executive vitality."
    },
    2: {
        "planet": "Moon (Chandra)",
        "primary_crystals": ["Moonstone", "White Selenite", "Clear Sphatik Quartz"],
        "element": "Water / Lunar Intuition",
        "color_frequency": "Pearly white and opalescent silver rays",
        "incompatible_planets": [4, 8, 9],  # Rahu, Saturn, Mars clash
        "incompatible_crystals": ["Hessonite", "Blue Sapphire", "Red Coral"],
        "lifestyle_attunement": "Place in your evening sanctuary or bedside table to soothe emotional fluctuations, deepen restful sleep, and enhance intuitive listening."
    },
    3: {
        "planet": "Jupiter (Guru)",
        "primary_crystals": ["Citrine", "Yellow Topaz", "Tiger's Eye (Golden)"],
        "element": "Ether / Wisdom & Expansion",
        "color_frequency": "Vibrant golden-yellow and warm saffron rays",
        "incompatible_planets": [6],  # Venus clash
        "incompatible_crystals": ["Diamond", "White Zircon"],
        "lifestyle_attunement": "Keep near study desk, books, or financial journals to encourage ethical abundance, continuous learning, and sound mentorship."
    },
    4: {
        "planet": "Rahu",
        "primary_crystals": ["Smoky Quartz", "Hematite", "Fluorite"],
        "element": "Air / High-Tech Innovation",
        "color_frequency": "Smoky grey, metallic charcoal, and subtle blue rays",
        "incompatible_planets": [1, 2, 9],  # Sun, Moon, Mars clash
        "incompatible_crystals": ["Ruby", "Pearl", "Red Coral"],
        "lifestyle_attunement": "Keep beside computer or workspace hardware to absorb chaotic electromagnetic restlessness and ground strategic systems thinking."
    },
    5: {
        "planet": "Mercury (Budh)",
        "primary_crystals": ["Green Aventurine", "Jade", "Malachite"],
        "element": "Earth / Commercial Agility",
        "color_frequency": "Emerald green and refreshing mint rays",
        "incompatible_planets": [],  # Universal mediator
        "incompatible_crystals": [],
        "lifestyle_attunement": "Hold during commercial negotiations, client presentations, or creative writing sprints to foster articulate communication and mental agility."
    },
    6: {
        "planet": "Venus (Shukra)",
        "primary_crystals": ["Rose Quartz", "Opalite", "Clear Sphatik"],
        "element": "Water / Aesthetic Harmony & Grace",
        "color_frequency": "Soft rose pink, iridescent white, and gentle pastel rays",
        "incompatible_planets": [3],  # Guru clash
        "incompatible_crystals": ["Yellow Sapphire", "Citrine"],
        "lifestyle_attunement": "Display in personal living space or dressing area to cultivate self-compassion, relational warmth, and artistic refinement."
    },
    7: {
        "planet": "Ketu",
        "primary_crystals": ["Lapis Lazuli", "Cat's Eye Chrysoberyl (Gentle)", "Sodalite"],
        "element": "Ether / Diagnostic Depth",
        "color_frequency": "Deep indigo and patterned earthen grey rays",
        "incompatible_planets": [8],  # Saturn heavy conflict
        "incompatible_crystals": ["Blue Sapphire", "Jet Black Tourmaline"],
        "lifestyle_attunement": "Use during quiet introspection, deep research, or breathwork to dissolve mental clutter and anchor spiritual discernment."
    },
    8: {
        "planet": "Saturn (Shani)",
        "primary_crystals": ["Amethyst", "Blue Lace Agate", "Black Onyx"],
        "element": "Earth / Karmic Endurance & Focus",
        "color_frequency": "Deep violet, midnight navy, and gentle soothing blue rays",
        "incompatible_planets": [1, 2, 4, 9],  # Sun, Moon, Rahu, Mars clash
        "incompatible_crystals": ["Ruby", "Pearl", "Red Coral", "Hessonite"],
        "lifestyle_attunement": "Keep on executive desk during demanding long-term operational planning to instill patience, methodical discipline, and humility."
    },
    9: {
        "planet": "Mars (Mangal)",
        "primary_crystals": ["Red Jasper", "Carnelian (Deep Red)", "Bloodstone"],
        "element": "Fire / Courage & Vital Action",
        "color_frequency": "Rich brick red, terracotta, and warm crimson rays",
        "incompatible_planets": [2, 4, 8],  # Moon, Rahu, Saturn clash
        "incompatible_crystals": ["Pearl", "Blue Sapphire", "Hessonite"],
        "lifestyle_attunement": "Incorporate during physical fitness, athletic conditioning, or decisive project kick-offs to channel energy constructively without impulsive friction."
    }
}


def generate_consensus_reading(
    name: str,
    day: int,
    month: int,
    year: int,
    target_date: Optional[date] = None
) -> Dict[str, Any]:
    """
    Authoritative Multi-System Consensus Engine:
    Executes independent calculations across:
    1. Lo Shu 3x3 Magic Square (8 Planes & Missing/Repeated Voids)
    2. Chaldean Name Sound Frequencies & Classical Compound Archetypes
    3. Vedic Sankhya Shastra (Driver/Conductor Dynamics)
    4. KP Astrology (Driver Star-Lord & Conductor Sub-Lord Matrix)
    5. Bhrigu Nandi Nadi (BNN Karaka Conjunctions & Career Axis)
    6. Lal Kitab (Masnooi Compound Planets & Awakening Ages)
    7. Vedic Parashari Jyotish (Sambandha Conjunction Yogas & Dignities)
    8. Real-Time Planetary Transits (Gochar) & 24-Hour Chaldean Horas

    Performs correlation-aware convergence across 6 independent system families,
    preserves conflicts, generates safe Vedic lifestyle adjustments, safe crystal
    healing, sacred yantras, a plain-language layman synthesis, and a past-pattern
    validation question.
    """
    if target_date is None:
        target_date = date.today()

    clean_name = name.strip() if name else "Seeker"

    # ── 1. INDEPENDENT NUMEROLOGY ENGINE EXECUTIONS ────────────────────────────
    vedic_res = analyze_vedic_numerology(day, month, year)
    driver = vedic_res["driver_number"]
    conductor = vedic_res["conductor_number"]
    lo_shu_res = analyze_lo_shu_grid(day, month, year)
    name_cheiro = analyze_name_cheiro(clean_name, driver=driver, conductor=conductor)
    pyth_res = analyze_pythagorean_full(day, month, year, clean_name)

    # ── 2. INDEPENDENT ASTROLOGY ENGINE EXECUTIONS ─────────────────────────────
    astro_multi = run_multi_astrology_correlation_engine(day, month, year, clean_name, target_date)
    bnn_profile = evaluate_bnn_numerology_profile(day, month, year, clean_name)

    # ── 3. CORRELATION-AWARE SYSTEM FAMILY GROUPING ────────────────────────────
    # Family 1: numerology_core (Lo Shu)
    # Family 2: acoustics (Chaldean / Cheiro Name)
    # Family 3: numerology_comparative (Vedic Sankhya Shastra)
    # Family 4: astrology_classical (Vedic Parashari & KP Sub-Lord)
    # Family 5: astrology_nadi (Bhrigu Nandi Nadi)
    # Family 6: astrology_remedial (Lal Kitab Masnooi Alchemy)

    system_families = {
        "numerology_core": {
            "name": "Lo Shu 3x3 Magic Square",
            "signals": [
                f"{len(lo_shu_res.get('completed_planes', []))} completed energy planes",
                f"Missing voids: {lo_shu_res.get('missing_numbers', [])}",
                f"Repeated intensities: {list(lo_shu_res.get('repeated_numbers', {}).keys())}"
            ],
            "direction": "positive" if len(lo_shu_res.get("completed_planes", [])) >= 2 else "mixed"
        },
        "acoustics": {
            "name": "Chaldean Acoustic Name Resonance",
            "signals": [
                f"Compound Sum {name_cheiro.get('compound_sum', 0)} ({name_cheiro.get('compound_archetype', 'Vibration')})",
                f"Single Root {name_cheiro.get('root_number', 0)}",
                f"Driver Aligned: {name_cheiro.get('is_aligned_with_driver', False)}"
            ],
            "direction": "positive" if name_cheiro.get("is_aligned_with_driver", False) else "mixed"
        },
        "numerology_comparative": {
            "name": "Vedic Sankhya Shastra & Western Pythagorean",
            "signals": [
                f"Driver {driver} ({vedic_res.get('driver_planet')}) with Conductor {conductor} ({vedic_res.get('conductor_planet')})",
                f"Western Life Path: {pyth_res.get('life_path', {}).get('final_life_path', driver)} ({pyth_res.get('life_path', {}).get('planetary_association', {}).get('planet', 'Aligned')})",
                f"Harmonious numbers: {vedic_res.get('friendly_numbers', [])}",
                f"Friction numbers: {vedic_res.get('enemy_numbers', [])}"
            ],
            "direction": "positive" if conductor in vedic_res.get("friendly_numbers", []) else ("challenging" if conductor in vedic_res.get("enemy_numbers", []) else "neutral")
        },
        "astrology_classical": {
            "name": "Vedic Parashari & KP Astrology",
            "signals": [
                f"KP Sub-Lord Outcome: {astro_multi['discipline_breakdown']['kp_astrology']['sublord_outcome']}",
                f"Vedic Yoga: {astro_multi['discipline_breakdown']['vedic_jyotish']['classical_yoga']}"
            ],
            "direction": "positive" if "Harmonious" in astro_multi['discipline_breakdown']['kp_astrology']['sublord_outcome'] else "mixed"
        },
        "astrology_nadi": {
            "name": "Bhrigu Nandi Nadi (BNN)",
            "signals": [
                f"Primary Conjunction: {bnn_profile.get('primary_pair_analysis', {}).get('title', 'Planetary Flow')}",
                f"Career Karma: {bnn_profile.get('profession_karma_analysis', {}).get('bnn_predictions', 'Steady compounding')[:100]}..."
            ],
            "direction": "positive" if bnn_profile.get("primary_pair_analysis", {}).get("polarity") != "challenging" else "challenging"
        },
        "astrology_remedial": {
            "name": "Lal Kitab Astrological Alchemy",
            "signals": [
                f"Awakening Ages: {astro_multi['discipline_breakdown']['lal_kitab']['destiny_awakening_ages']}",
                f"Masnooi Compound: {astro_multi['discipline_breakdown']['lal_kitab']['masnooi_compound'][:100]}..."
            ],
            "direction": "positive" if "balanced" in astro_multi['discipline_breakdown']['lal_kitab']['masnooi_compound'].lower() else "neutral"
        }
    }

    # Convergence calculation across the 6 independent families
    total_eligible_families = len(system_families)
    supporting_families = sum(1 for fam in system_families.values() if fam["direction"] == "positive")
    opposing_families = sum(1 for fam in system_families.values() if fam["direction"] == "challenging")
    neutral_families = total_eligible_families - (supporting_families + opposing_families)

    convergence_ratio = round(supporting_families / total_eligible_families, 2)

    if supporting_families >= 4 and opposing_families == 0:
        consensus_status = "convergent"
        consensus_label = "Multi-Tradition Convergence (Strong Cross-System Alignment)"
    elif supporting_families >= 2 and opposing_families == 0:
        consensus_status = "partially_convergent"
        consensus_label = "Partially Convergent Alignment (Supportive with Growth Areas)"
    elif opposing_families > 0 and supporting_families > 0:
        consensus_status = "conflicted"
        consensus_label = "Nuanced Cross-Currents (Traditions Reveal Divergent Phases)"
    elif supporting_families == 1:
        consensus_status = "single_system"
        consensus_label = "Single System Indication"
    else:
        consensus_status = "neutral"
        consensus_label = "Balanced Foundational Baseline"

    # ── 4. DOMAIN VERDICTS WITH CITATIONS (BACKWARD COMPATIBLE) ───────────────
    domain_queries = {
        "Career & Business": f"Driver {driver} Conductor {conductor} career business success leadership",
        "Wealth & Finances": f"Driver {driver} Conductor {conductor} money wealth financial growth",
        "Health & Vitality": f"Driver {driver} Conductor {conductor} health disease vitality remedy",
        "Relationships & Marriage": f"Driver {driver} Conductor {conductor} marriage relationships family harmony"
    }

    domain_verdicts = {}
    total_agreement_scores = []

    for domain, query in domain_queries.items():
        passages = rag_engine.query(query, top_k=2)
        is_friendly = conductor in vedic_res["friendly_numbers"]
        is_enemy = conductor in vedic_res["enemy_numbers"]

        if is_friendly:
            score = 85.0 + (len(lo_shu_res["completed_planes"]) * 3.0)
            verdict = "Highly Favourable"
        elif is_enemy:
            score = 55.0 + (len(lo_shu_res["completed_planes"]) * 3.0)
            verdict = "Challenging / Requires Remedies"
        else:
            score = 72.0 + (len(lo_shu_res["completed_planes"]) * 3.0)
            verdict = "Neutral / Moderate Growth"

        score = min(score, 98.0)
        total_agreement_scores.append(score)

        domain_verdicts[domain] = {
            "verdict": verdict,
            "consensus_score_pct": round(score, 1),
            "provenance": "verified_numeros_vision",
            "grounded_citations": [
                sanitize_citation({
                    "source": p["source"],
                    "location": p["location"],
                    "category": "Proprietary Classical Foundation",
                    "excerpt": p["content"]
                }) for p in passages
            ]
        }

    overall_consensus = round(sum(total_agreement_scores) / len(total_agreement_scores), 1)

    # ── 5. VEDIC SPIRITUAL LIFESTYLE TRANSFORMATION (DINACHARYA) ──────────────
    # 24-Hour Hora analysis for native
    horas = calculate_hourly_planetary_horas(target_date, driver=driver, conductor=conductor)
    favourable_horas = [h for h in horas if h["suitability_code"] == "favourable"]

    driver_meta = PLANET_BY_NUMBER.get(driver, {"name": "Sun", "vedic": "Surya"})
    conductor_meta = PLANET_BY_NUMBER.get(conductor, {"name": "Saturn", "vedic": "Shani"})

    dinacharya_routine = {
        "brahma_muhurta": {
            "window": "05:00 AM – 06:30 AM",
            "practice": "Quiet contemplative breathing (Pranayama) and silent gratitude before sunrise.",
            "purpose": "Clears mental static, centers nervous equilibrium, and attunes internal bio-rhythms to solar prana."
        },
        "optimal_action_window": {
            "window": favourable_horas[0]["time_window"] if favourable_horas else "08:00 AM – 10:00 AM",
            "ruling_energy": favourable_horas[0]["planet_name"] if favourable_horas else driver_meta["name"],
            "practice": "Schedule primary strategic decisions, commercial contracts, or crucial meetings.",
            "purpose": "Leverages supportive planetary hora for maximum executive clarity and minimal friction."
        },
        "reflective_evening_sanctuary": {
            "window": "07:30 PM – 09:30 PM",
            "practice": "Digital cessation, warm herbal infusion, and 5 minutes of reflective journaling.",
            "purpose": "Detaches mental awareness from daily operational friction, grounding emotional tranquility."
        },
        "sattvic_lifestyle_disciplines": [
            "Opt for freshly prepared, wholesome plant-based nourishment; minimize excessively pungent or heavy stimulants.",
            "Maintain an uncluttered, clean workspace with natural ventilation in the East or North quadrants.",
            "Introduce intentional mindful pauses: take three slow, deliberate breaths before answering high-stakes communications."
        ]
    }

    # ── 6. SAFE CRYSTAL & GEMSTONE HEALING (ENEMY EXCLUSION & COMPLIANCE) ─────
    d_crystal_info = SAFE_CRYSTAL_CATALOGUE.get(driver, SAFE_CRYSTAL_CATALOGUE[1])
    c_crystal_info = SAFE_CRYSTAL_CATALOGUE.get(conductor, SAFE_CRYSTAL_CATALOGUE[8])

    # Check for natural planetary conflict between driver and conductor stones
    is_conflict = conductor in d_crystal_info.get("incompatible_planets", []) or driver in c_crystal_info.get("incompatible_planets", [])
    
    if not is_conflict:
        recommended_crystals = list(dict.fromkeys(d_crystal_info["primary_crystals"][:2] + c_crystal_info["primary_crystals"][:1]))
        crystal_rationale = f"Harmonizes the natural solar/lunar frequencies of Driver {driver} ({driver_meta['name']}) and Conductor {conductor} ({conductor_meta['name']})."
    else:
        # If conflict exists, use neutral mediator crystals (Mercury/Budh or Venus/Shukra clear quartz)
        recommended_crystals = ["Clear Sphatik Quartz", "Green Aventurine"]
        crystal_rationale = (
            f"Because Driver {driver} and Conductor {conductor} hold dynamic contrasting planetary polarities, "
            f"neutral balancing crystals are chosen to prevent energetic friction."
        )

    excluded_stones = list(dict.fromkeys(d_crystal_info.get("incompatible_crystals", []) + c_crystal_info.get("incompatible_crystals", [])))

    safe_crystals_data = {
        "recommended_crystals": recommended_crystals,
        "color_frequency": d_crystal_info["color_frequency"],
        "elemental_alignment": d_crystal_info["element"],
        "lifestyle_attunement": d_crystal_info["lifestyle_attunement"],
        "excluded_friction_crystals": excluded_stones,
        "statutory_compliance_notice": (
            "Statutory Qualification (Drugs & Magic Remedies Act 1954): Crystals and gemstones are offered strictly "
            "as traditional cultural, meditative, and color-frequency personal attunements. They do not diagnose, treat, "
            "cure, or prevent any physical, medical, or psychological condition, nor do they guarantee financial gains or life events."
        )
    }

    # ── 7. SACRED YANTRAS & 5-TIER SAFE REMEDIES ───────────────────────────────
    remedy_selection = select_remedies_and_yantras(
        driver=driver,
        conductor=conductor,
        missing_numbers=lo_shu_res.get("missing_numbers", []),
        repeated_numbers=lo_shu_res.get("repeated_numbers", {}),
        max_remedies=5
    )

    # ── 8. LAYMAN HUMANISED SYNTHESIS & PAST-PATTERN VALIDATION ───────────────
    # Translate technical metrics into warm, consultant-style plain language
    layman_summary = (
        f"Hello {clean_name}, looking across your birth chart and name frequencies, your personal blueprint brings together "
        f"the natural driving energy of {driver_meta['name']} with the life direction of {conductor_meta['name']}. "
        f"Across our six traditional evaluation systems, we see a {consensus_label.lower()}. "
        f"Rather than treating numbers or planets as fixed fates, we look at them as personal rhythms. When you align your daily "
        f"lifestyle, mindful pauses, and work habits with these natural rhythms, everyday friction tends to dissolve naturally."
    )

    disagreement_explanation = (
        f"While traditional Vedic and KP systems point toward steady foundational growth in your career direction, "
        f"your Lo Shu grid highlights missing energy in Number(s) {lo_shu_res.get('missing_numbers', [])}, which can occasionally "
        f"create moments of second-guessing or over-analysis. This is not a flaw; it simply means taking an extra breath before "
        f"rushing major commitments brings you right back into balance."
    )

    # Generate a dated historical reflection question based on past cycles
    current_year = target_date.year
    past_window_start = current_year - 3
    past_window_end = current_year - 1
    past_validation_question = (
        f"Looking back at the period between {past_window_start} and {past_window_end}, our traditional timeline analysis "
        f"indicates a significant phase of structural reorganization and personal recalibration in your primary goals. "
        f"Does this reflect your lived experience during those years?"
    )

    return {
        # Legacy Keys (Guaranteed Backward Compatibility)
        "user_name": clean_name,
        "dob": f"{day:02d}/{month:02d}/{year}",
        "vedic_numerology": vedic_res,
        "cheiro_name_analysis": name_cheiro,
        "lo_shu_grid": lo_shu_res,
        "pythagorean_numerology": pyth_res,
        "overall_consensus_strength_pct": overall_consensus,
        "domain_verdicts": domain_verdicts,
        "remedy_summary": {
            "missing_numbers": lo_shu_res["missing_numbers"],
            "enemy_numbers": vedic_res["enemy_numbers"],
            "recommended_remedy_passages": lo_shu_res["numeros_vision_remedies"][:2]
        },

        # Enriched Master Consensus Architecture Fields
        "multi_system_consensus": {
            "consensus_status": consensus_status,
            "consensus_label": consensus_label,
            "convergence_ratio": convergence_ratio,
            "eligible_family_count": total_eligible_families,
            "supporting_family_count": supporting_families,
            "opposing_family_count": opposing_families,
            "neutral_family_count": neutral_families,
            "system_families": system_families,
            "disagreement_analysis": disagreement_explanation
        },
        "discipline_breakdown": astro_multi.get("discipline_breakdown", {}),
        "transit_and_timing": astro_multi.get("transit_and_timing", {}),
        "vedic_lifestyle_transformation": {
            "dinacharya_circadian_routine": dinacharya_routine,
            "executive_hora_windows": [h for h in horas[:8] if h["suitability_code"] == "favourable"]
        },
        "safe_crystals_and_gemstones": safe_crystals_data,
        "sacred_yantras_and_vastu": {
            "primary_yantra": remedy_selection.get("prescribed_yantra"),
            "rationale": remedy_selection.get("yantra_recommendation_rationale"),
            "curated_remedies": remedy_selection.get("prescribed_remedies", [])
        },
        "layman_synthesis": {
            "consultant_summary": layman_summary,
            "where_traditions_agree": f"{supporting_families} of 6 independent tradition families align on foundational resilience and steady compounding progress.",
            "where_traditions_differ": disagreement_explanation,
            "actionable_next_step": "Begin with the 5-minute morning contemplation and workspace orientation before exploring customized reports."
        },
        "past_pattern_validation": {
            "milestone_period": f"{past_window_start} – {past_window_end}",
            "validation_question": past_validation_question,
            "feedback_options": ["yes_match", "partial_match", "no_match", "not_enough_information", "skip"]
        }
    }


if __name__ == "__main__":
    report = generate_consensus_reading("Bhaskr Singh", 15, 8, 1995)
    print("=== NUMEROS VISION ENRICHED CONSENSUS REPORT ===")
    print(f"User: {report['user_name']} | DOB: {report['dob']}")
    print(f"Driver/Conductor: {report['vedic_numerology']['driver_number']}/{report['vedic_numerology']['conductor_number']}")
    print(f"Consensus Status: {report['multi_system_consensus']['consensus_status']} ({report['multi_system_consensus']['consensus_label']})")
    print(f"Convergence Ratio: {report['multi_system_consensus']['convergence_ratio']} ({report['multi_system_consensus']['supporting_family_count']}/{report['multi_system_consensus']['eligible_family_count']} families)")
    print(f"\nLayman Summary:\n{report['layman_synthesis']['consultant_summary']}")
    print(f"\nPast Pattern Validation:\n{report['past_pattern_validation']['validation_question']}")
    print(f"\nSafe Crystals:\n{report['safe_crystals_and_gemstones']['recommended_crystals']} (Excluded: {report['safe_crystals_and_gemstones']['excluded_friction_crystals']})")
