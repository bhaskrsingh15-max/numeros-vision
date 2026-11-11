# -*- coding: utf-8 -*-
"""
TWIN PARADOX & INPUT-OUTPUT ENGINE
Numeros Vision — Master Knowledge Engine (Day 8 Canon)
Resolves why identical birth charts yield divergent life paths through a rigorous 3-layer model:
Fixed Inputs -> Variable Inputs -> Observed Life Outcomes.
In strict compliance with Master AGENTS.md.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

from app.engine.core_matrix_engine import calculate_kua_number
from app.engine.name_balancing_engine import build_birth_date_grid, calculate_word_value
from app.engine.complementary_poorak_engine import evaluate_grid_complementary_support
from app.engine.profession_engine import recommend_professions


class TwinParadoxEngine:
    """
    Implements Numeros Vision Classical Methodology Day 8 Input-Output Framework for Twin Differentiation.
    
    Layer 1: Fixed Inputs (Birth Date, Time, Place)
             Produces 100% deterministic, identical foundational matrices for both individuals.
             
    Layer 2: Variable Inputs (Name, Education, Career, Decisions, Partner Synastry, Relocation)
             Introduces acoustic, energetic, and relational divergences.
             
    Layer 3: Observed Outcomes
             Captures experiential divergences without fabricating causal claims.
    """

    def analyze_twin_pair(
        self,
        birth_date: str,
        twin_a_inputs: Dict[str, Any],
        twin_b_inputs: Dict[str, Any],
        gender_a: str = "MALE",
        gender_b: str = "MALE",
        birth_time: Optional[str] = None,
        birth_place: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes comparative differential analysis for two individuals sharing identical birth data.
        """
        # ── LAYER 1: FIXED INPUT CALCULATIONS (GUARANTEED IDENTICAL) ──────────
        dt = datetime.strptime(birth_date, "%Y-%m-%d")
        shared_grid = build_birth_date_grid(dt.day, dt.month, dt.year)
        driver = shared_grid["driver"]
        conductor = shared_grid["conductor"]
        kua = calculate_kua_number(dt.year, gender_a)
        
        # Format grid counts for complementary evaluation
        grid_counts = shared_grid.get("digit_counts", {})
        grid_eval = evaluate_grid_complementary_support(grid_counts)
        
        # ── LAYER 2: VARIABLE INPUT ANALYSIS ──────────────────────────────────
        def _evaluate_profile(inputs: Dict[str, Any], gender: str) -> Dict[str, Any]:
            name = inputs.get("name", "")
            name_analysis = None
            if name:
                name_eval = calculate_word_value(name)
                name_analysis = {
                    "raw_name": name,
                    "compound_number": name_eval.get("compound_sum"),
                    "root_number": name_eval.get("root_number"),
                    "reduction_path": name_eval.get("reduction_path"),
                    "planet": name_eval.get("planet")
                }
            
            career = inputs.get("career_choice", "")
            recommended_careers = recommend_professions(
                driver=driver,
                conductor=conductor
            )
            
            partner_dob = inputs.get("partner_dob")
            partner_synastry = None
            if partner_dob:
                p_dt = datetime.strptime(partner_dob, "%Y-%m-%d")
                p_grid = build_birth_date_grid(p_dt.day, p_dt.month, p_dt.year)
                partner_synastry = {
                    "partner_driver": p_grid["driver"],
                    "partner_conductor": p_grid["conductor"],
                    "partner_kua": calculate_kua_number(p_dt.year, "female" if gender.upper() == "MALE" else "male"),
                    "notes": f"Partner introduces Driver {p_grid['driver']} and Conductor {p_grid['conductor']} into the seeker's dynamic."
                }
            
            return {
                "name": name,
                "name_analysis": name_analysis,
                "education_stream": inputs.get("education_stream", "Unspecified"),
                "career_choice": career,
                "recommended_careers": recommended_careers.get("top_recommendations", []),
                "partner_synastry": partner_synastry,
                "relocation_city": inputs.get("relocation_city", "Birth City")
            }

        profile_a = _evaluate_profile(twin_a_inputs, gender_a)
        profile_b = _evaluate_profile(twin_b_inputs, gender_b)
        
        # ── LAYER 3: DIVERGENCE SYNTHESIS ─────────────────────────────────────
        divergences = []
        
        # 1. Name Acoustic Divergence
        name_num_a = profile_a["name_analysis"].get("compound_number") if profile_a["name_analysis"] else None
        name_num_b = profile_b["name_analysis"].get("compound_number") if profile_b["name_analysis"] else None
        if name_num_a != name_num_b:
            divergences.append({
                "dimension": "Acoustic Name Vibration (Chaldean)",
                "twin_a_value": f"{profile_a['name']} (Compound {name_num_a})",
                "twin_b_value": f"{profile_b['name']} (Compound {name_num_b})",
                "impact": "Different name compounds activate different planetary secondary vibrations, altering public perception, social reception, and business branding."
            })
            
        # 2. Career Choice Divergence
        if profile_a["career_choice"] != profile_b["career_choice"]:
            divergences.append({
                "dimension": "Vocation & Commercial Archetype",
                "twin_a_value": profile_a["career_choice"],
                "twin_b_value": profile_b["career_choice"],
                "impact": "Choosing different fields engages different planetary karakas, resulting in divergent daily stressors and compounding career outcomes."
            })
            
        # 3. Partner & Relational Divergence
        if profile_a["partner_synastry"] or profile_b["partner_synastry"]:
            divergences.append({
                "dimension": "Partner Synastry & Interpersonal Grid",
                "twin_a_value": f"Partner DOB: {twin_a_inputs.get('partner_dob', 'None')}",
                "twin_b_value": f"Partner DOB: {twin_b_inputs.get('partner_dob', 'None')}",
                "impact": "Marriage and business partnerships superimpose a second Lo Shu grid over the native's chart, either mitigating missing planes or aggravating friction pairs."
            })
            
        # 4. Geographic Relocation Divergence
        if profile_a["relocation_city"] != profile_b["relocation_city"]:
            divergences.append({
                "dimension": "Geographic Orientation & Local Environment",
                "twin_a_value": profile_a["relocation_city"],
                "twin_b_value": profile_b["relocation_city"],
                "impact": "Relocation alters local cardinal alignments, atmospheric elements, and societal opportunity structures."
            })

        return {
            "system": "Numeros Vision Twin Paradox Multi-Layer Engine",
            "model_version": "1.0.0",
            "methodology_reference": "Day 8 Transcript — Input-Output Framework (Numeros Vision)",
            "layer_1_fixed_foundations": {
                "birth_date": birth_date,
                "recorded_birth_time": birth_time or "Shared/Recorded",
                "recorded_birth_place": birth_place or "Shared",
                "driver": driver,
                "conductor": conductor,
                "kua_number": kua,
                "lo_shu_grid_counts": grid_counts,
                "complementary_evaluations": grid_eval["evaluations"],
                "identity_note": "Identical birth data strictly yields identical core numerological arithmetic. The calculation engine never alters base numbers for shared dates."
            },
            "layer_2_variable_profiles": {
                "twin_a": profile_a,
                "twin_b": profile_b
            },
            "layer_3_observed_divergences": divergences,
            "governance_and_claim_status": {
                "instructor_claim": "The input-output model explains why identical twins experience divergent life outcomes despite having identical birth charts.",
                "scientific_disclaimer": "The instructor's proposition that numerology resolves the twin paradox is an interpretive educational framework, not an established empirical scientific conclusion. Numerological charts provide symbolic archetypes rather than causal determinism."
            }
        }
