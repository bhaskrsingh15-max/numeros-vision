"""
Implement 13-Section Uniform English-Only Structure in package_report_generator.py
and align planetary_package_reports.py
"""
import os
import re

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def update_package_report_generator():
    filepath = os.path.join(ROOT_DIR, "app", "engine", "package_report_generator.py")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Define the Basic Numerology Report generation block
    basic_report_block = '''
    # ──────────────────────────────────────────────────────────────────────────
    # TIER: BASIC NUMEROLOGY REPORT (3 PAGES · ₹199 / $19)
    # Standard 13-Section English-Only Report Structure
    # ──────────────────────────────────────────────────────────────────────────
    elif clean_tier in ["report_essential", "essential", "basic", "basic_report"]:
        age_data = calculate_age_numerology(day, month, year)
        dob_digits = [int(d) for d in f"{day:02d}{month:02d}{year}" if d != "0"]
        loshu_counts = {i: dob_digits.count(i) for i in range(1, 10)}
        missing_nums = [i for i in range(1, 10) if loshu_counts[i] == 0]
        
        report_sections = [
            f"# Basic Numerology Report\\n**Prepared for:** {clean_name} | **Date of Birth:** {day:02d}-{month:02d}-{year} | **Report Length:** 3 Pages | **Edition:** Executive PDF Deliverable\\n",
            "## 1. Report Overview\\n"
            f"This Basic Numerology Report provides an executive summary of your calculated foundational numbers, "
            f"the classical calculation methods applied, and an initial interpretation of the key findings. "
            f"It is designed to give you clarity on your core energetic patterns and practical focus areas.",
            
            "## 2. Personal Details and Calculation Inputs\\n"
            f"• **Full Name:** {clean_name}\\n"
            f"• **Date of Birth:** {day:02d}-{month:02d}-{year}\\n"
            f"• **Recorded Birth Time:** {birth_time or '11:10 AM'}\\n"
            f"• **Birth City / Location:** {birth_city or 'Chennai'}\\n"
            f"• **Calculation Standard:** Classical Vedic (Mulank & Bhagyank) and Lo Shu Mathematical Matrix",
            
            "## 3. Calculation Method\\n"
            f"Your foundational calculations are generated deterministically using verified numerological principles:\\n"
            f"• **Driver (Mulank):** Derived from the calendar day of birth ({day:02d}) reduced to a single digit: Root {driver} ({driver_planet}).\\n"
            f"• **Conductor (Bhagyank / Life Path Number):** Derived from the complete date sum ({day:02d} + {month:02d} + {year}) reduced to a single digit: Path {conductor} ({conductor_planet}).\\n"
            f"• **Lo Shu Grid:** Mapping of birth digits into the ancient 3x3 magic square of Saturn to evaluate elemental balance and missing frequencies.",
            
            "## 4. Calculation Summary\\n"
            f"• **Driver Number:** {driver} ({driver_planet})\\n"
            f"• **Conductor Number:** {conductor} ({conductor_planet})\\n"
            f"• **Current Chronological Age Milestone:** {age_data['age_years']} Years Completed (Navigating Year {age_data['running_year']})\\n"
            f"• **Age Compound Number:** {age_data['compound_age']} ➔ Root {age_data['root_age']} ({age_data['root_planet']})\\n"
            f"• **Missing Numbers in Grid:** {', '.join(map(str, missing_nums)) if missing_nums else 'None'}",
            
            "## 5. Your Numerology Results\\n"
            f"Your core chart is anchored by Driver {driver} and Conductor {conductor}. "
            f"This harmonic pairing reflects disciplined craftsmanship, a natural standard for quality, and a commitment to enduring stability. "
            f"You perform best when actions are structured, clear, and grounded in long-term utility.\\n\\n"
            f"**Natal Lo Shu 3×3 Grid:**\\n" + generate_loshu_grid_markdown(day, month, year),
            
            "## 6. Detailed Interpretation\\n"
            f"### Primary Drive and Outer Action\\n"
            f"Governed by Driver {driver} ({driver_planet}), you initiate tasks with caution, thoroughness, and self-reliance. "
            f"You prefer verified facts over speculative promises and build your reputation on consistent follow-through.\\n\\n"
            f"### Life Path and Directional Guidance\\n"
            f"Your Conductor {conductor} ({conductor_planet}) shapes your broader life trajectory toward institutional or professional leadership. "
            f"You are guided to compound knowledge and resources patiently rather than chasing fleeting shortcuts.",
            
            "## 7. Key Findings\\n"
            f"1. **High Structural Stamina:** Strong capacity to navigate demanding multi-year responsibilities.\\n"
            f"2. **Deliberate Decision Pacing:** Your best choices occur when given time to deliberate without emotional haste.\\n"
            f"3. **Identified Missing Frequencies:** The absence of digits [ {', '.join(map(str, missing_nums)) if missing_nums else 'None'} ] points to temporary energy leaks that can be balanced through focused habits.",
            
            "## 8. Number Relationships and Patterns\\n"
            f"The interaction between Driver {driver} and Conductor {conductor} creates a reinforcing resonance. "
            f"Your inner desires and outer life opportunities work toward the same compounding objectives, minimizing internal contradiction. "
            f"Aligning your daily schedule with your core numbers enhances productivity.",
            
            "## 9. Strengths and Areas for Reflection\\n"
            f"• **Core Strengths:** Perseverance, organizational discipline, emotional resilience, strategic patience.\\n"
            f"• **Areas for Reflection:** Guard against over-rigidity, perfectionist delays, and keeping concerns unexpressed until tension builds up.",
            
            "## 10. Personalised Recommendations\\n"
            f"• **Auspicious Palette:** Deep navy, charcoal, silver, and soft cream.\\n"
            f"• **Productive Desk Facing:** Orient your primary workspace facing West or North.\\n"
            f"• **Weekly Balance Ritual:** Dedicate time each Saturday to organize your environment and review weekly progress calmly.",
            
            "## 11. Additional Analysis\\n"
            f"Your running chronological age reflects Compound {age_data['compound_age']} pointing to {age_data['root_planet']} (Root {age_data['root_age']}). "
            f"{age_data['input_characteristics']['description']} "
            f"This confirms that the present period rewards consolidation and systematic restructuring.",
            
            "## 12. Summary and Next Steps\\n"
            f"You possess the natural foundations to build enduring success. "
            f"To explore expanded 5-year planetary timelines, Chaldean sound frequency, and multi-layer remedies, "
            f"consider exploring the **Advanced Numerology Report (12 Pages)** or **Premium Numerology Report (32 Pages)**.",
            
            "## 13. Methodology and Limitations\\n"
            f"Calculations are based on traditional Vedic numerology and classical Lo Shu grid principles. "
            f"Numerological analysis provides navigational insight and energetic reflection; "
            f"it does not replace personal judgment, legal counsel, or medical advice."
        ]
        
        return _finalize_report_envelope({
            "tier": "report_essential",
            "tier_display": "Basic Numerology Report",
            "price_inr": 199,
            "profile": profile_summary,
            "pages_count": 3,
            "report_markdown": sanitize_text("\\n\\n".join(report_sections))
        }, clean_tier, clean_name, day, month, year, driver, conductor)
    '''

    # Define the Advanced Numerology Report generation block
    advanced_report_block = '''
    # ──────────────────────────────────────────────────────────────────────────
    # TIER: ADVANCED NUMEROLOGY REPORT (12 PAGES · ₹510 / $39)
    # Standard 13-Section English-Only Report Structure
    # ──────────────────────────────────────────────────────────────────────────
    elif clean_tier in ["report_master", "master", "advanced", "advanced_report"]:
        age_data = calculate_age_numerology(day, month, year)
        dob_digits = [int(d) for d in f"{day:02d}{month:02d}{year}" if d != "0"]
        loshu_counts = {i: dob_digits.count(i) for i in range(1, 10)}
        missing_nums = [i for i in range(1, 10) if loshu_counts[i] == 0]
        expl_career = generate_simple_explanation_and_remedies("Career stability and expansion", driver, conductor, name=clean_name, day=day, month=month, year=year)
        expl_wealth = generate_simple_explanation_and_remedies("Wealth retention and asset compounding", driver, conductor, name=clean_name, day=day, month=month, year=year)

        report_sections = [
            f"# Advanced Numerology Report\\n**Prepared for:** {clean_name} | **Date of Birth:** {day:02d}-{month:02d}-{year} | **Report Length:** 12 Pages | **Edition:** Master Synthesis Dossier\\n",
            "## 1. Report Overview\\n"
            f"Welcome, {clean_name}. This Advanced Numerology Report delivers a comprehensive dual-system synthesis combining "
            f"classical Vedic calculations, Chaldean sound frequency analysis, Bhrigu Nandi Nadi (BNN) trines, and the 5-Year Vimshottari Dasha timeline. "
            f"It provides expanded interpretations, number relationships, and actionable recommendations.",
            
            "## 2. Personal Details and Calculation Inputs\\n"
            f"• **Client Full Name:** {clean_name}\\n"
            f"• **Date of Birth:** {day:02d}-{month:02d}-{year}\\n"
            f"• **Birth Epoch Time:** {birth_time or '11:10 AM'}\\n"
            f"• **Birth Location:** {birth_city or 'Chennai'}\\n"
            f"• **Analysis Systems:** Vedic Numerology, Chaldean Syllable Analysis, Lo Shu Grid, BNN 1-5-9 Trines, 5-Year Vimshottari Timing",
            
            "## 3. Calculation Method\\n"
            f"This dossier applies a dual-engine mathematical process:\\n"
            f"• **Psychic Driver (Mulank):** Computed as single-digit root of day {day:02d}: {driver} ({driver_planet}).\\n"
            f"• **Destiny Conductor (Bhagyank):** Computed from full birth date sum: {conductor} ({conductor_planet}).\\n"
            f"• **Chaldean Sound Matrix:** Letter frequencies assigned according to the ancient Chaldean alphabet formula (A,I,J,Q,Y=1; B,K,R=2; C,G,L,S=3; D,M,T=4; E,H,N,X=5; U,V,W=6; O,Z=7; F,P=8).\\n"
            f"• **BNN Vector Dynamics:** 1-5-9 Dharma Trine, 2-10 Artha Trine, and 3-7-11 Kama Trine interactions.",
            
            "## 4. Calculation Summary\\n"
            f"• **Driver Number:** {driver} ({driver_planet})\\n"
            f"• **Conductor Number:** {conductor} ({conductor_planet})\\n"
            f"• **Lo Shu Grid Planes:** 8 Structural Planes Analyzed\\n"
            f"• **Age Milestone:** {age_data['age_years']} Years Completed (Year {age_data['running_year']}) | Compound {age_data['compound_age']} ➔ Root {age_data['root_age']} ({age_data['root_planet']})\\n"
            f"• **Missing Numbers:** [ {', '.join(map(str, missing_nums)) if missing_nums else 'None'} ]",
            
            "## 5. Your Numerology Results\\n"
            f"Your chart reflects an exceptional capacity for institutional leadership, executive responsibility, and long-term asset building. "
            f"The dual presence of {driver_planet} and {conductor_planet} grants you natural authority and disciplined execution.\\n\\n"
            f"**Natal Lo Shu 3×3 Grid:**\\n" + generate_loshu_grid_markdown(day, month, year),
            
            "## 6. Detailed Interpretation\\n"
            f"### Professional Arc and Executive Authority\\n"
            f"{expl_career['direct_answer']}\\n\\n"
            f"### Financial Retention and Asset Flow\\n"
            f"{expl_wealth['direct_answer']}\\n\\n"
            f"### Personal Year Trajectory\\n"
            f"You are navigating an essential consolidation window where methodical groundwork and eliminating liabilities yield compound returns.",
            
            "## 7. Key Findings\\n"
            f"1. **Strategic Compounding:** Your greatest successes come from steady craftsmanship rather than speculative pivots.\\n"
            f"2. **Communication Calibration:** Clarifying agreements in writing eliminates ambiguity and protects your professional energy.\\n"
            f"3. **Remedial Bridging:** Activating your primary favorable colors, metal resonance, and spatial orientations neutralizes identified grid voids.",
            
            "## 8. Number Relationships and Patterns\\n"
            f"The interaction between Driver {driver} and Conductor {conductor} forms a harmonious pillar. "
            f"Your inner drive matches your external circumstances, allowing steady accumulation of skills, reputation, and commercial credibility. "
            f"The BNN 1-5-9 vector indicates strong dharmic support when working ethically.",
            
            "## 9. Strengths and Areas for Reflection\\n"
            f"• **Strengths:** Executive stamina, unwavering perseverance, analytical depth, ethical craftsmanship.\\n"
            f"• **Areas for Reflection:** Guard against isolation under stress, excessive skepticism of new opportunities, and delays caused by perfectionism.",
            
            "## 10. Personalised Recommendations\\n"
            f"• **7-Layer Remedial Protocol:**\\n"
            f"  1. *Color Therapy:* Wear deep navy, charcoal, or cream on major meeting days.\\n"
            f"  2. *Spatial Alignment:* Position desk facing North or West for commercial clarity.\\n"
            f"  3. *Mindfulness Practice:* Dedicate 10 minutes each morning to quiet intention.\\n"
            f"  4. *Weekly Giving:* Offer selfless community service on Saturdays.\\n"
            f"  5. *Acoustic Sound:* Use grounding classical sound frequencies during focused work.",
            
            "## 11. Additional Analysis\\n"
            f"### 5-Year Vimshottari Timing Windows (2026–2030)\\n"
            f"• **Phase 1 (Consolidation & Groundwork):** Deepening expertise and upgrading systems.\\n"
            f"• **Phase 2 (Expansion & Visibility):** Professional recognition, network growth, and commercial unlock.\\n"
            f"• **Phase 3 (Harvest & Compounding):** Solidifying long-term investments and enjoying institutional authority.",
            
            "## 12. Summary and Next Steps\\n"
            f"Your Advanced Numerology Report establishes a clear, verified blueprint for sustained momentum. "
            f"For multi-decade timing maps, KP sub-lord significators, family synastry, and alternative name spelling calibrations, "
            f"explore the **Premium Numerology Report (32 Pages)**.",
            
            "## 13. Methodology and Limitations\\n"
            f"This analysis integrates Vedic numerological standards, Chaldean acoustic matrices, and Lo Shu grid systems. "
            f"All findings represent navigational guidance and symbolic insights; they do not constitute legal, medical, or financial warranties."
        ]

        if _is_international_client(birth_city):
            intl_sections = _build_international_report_sections(clean_name, driver, conductor, missing_nums)
            report_sections.extend(intl_sections)
            
        return _finalize_report_envelope({
            "tier": "report_master",
            "tier_display": "Advanced Numerology Report",
            "price_inr": 510,
            "profile": profile_summary,
            "pages_count": 12,
            "report_markdown": sanitize_text("\\n\\n".join(report_sections))
        }, clean_tier, clean_name, day, month, year, driver, conductor)
    '''

    # Insert basic and advanced blocks before complete report block
    target = '    # ── 1. NUMEROLOGY REPORT PACKAGES (3 TIERS)'
    if 'report_essential' not in content:
        content = content.replace(
            '    # ──────────────────────────────────────────────────────────────────────────\n    # TIER 1: FREE DISCOVERY READING',
            basic_report_block + '\n' + advanced_report_block + '\n    # ──────────────────────────────────────────────────────────────────────────\n    # TIER 1: FREE DISCOVERY READING'
        )

    # Update Complete Report / Premium report tier display and title
    content = content.replace('"tier_display": "Complete Personal Destiny Blueprint Report"', '"tier_display": "Premium Numerology Report"')
    content = content.replace('# The Complete Personal Destiny Blueprint', '# Premium Numerology Report')
    content = content.replace('**Edition:** Master Client Dossier', '**Report Length:** 32 Pages | **Edition:** Sovereign Executive Blueprint')

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated app/engine/package_report_generator.py successfully.")

def update_planetary_package_reports():
    filepath = os.path.join(ROOT_DIR, "app", "engine", "planetary_package_reports.py")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Standardize package tier titles to standard English naming
    content = content.replace("Format: 3-Page Action Plan", "Report Length: 3 Pages | Format: Basic Compatibility Report")
    content = content.replace("Format: 12-Page Master Dossier", "Report Length: 12 Pages | Format: Advanced Compatibility Report")
    content = content.replace("Format: 32-Page Sovereign Blueprint", "Report Length: 32 Pages | Format: Premium Compatibility Report")

    content = content.replace("Format: 3-Page Financial Action Plan", "Report Length: 3 Pages | Format: Basic Business Name Report")
    content = content.replace("Format: 12-Page Enterprise Dossier", "Report Length: 12 Pages | Format: Advanced Business Name Report")
    content = content.replace("Format: 32-Page Full Corporate Blueprint", "Report Length: 32 Pages | Format: Premium Business Name Report")

    content = content.replace("Format: 3-Page Executive Elevation Brief", "Report Length: 3 Pages | Format: Basic Life Path Report")
    content = content.replace("Format: 12-Page Executive Dual-System Synthesis", "Report Length: 12 Pages | Format: Advanced Life Path Report")
    content = content.replace("Format: 32-Page Executive Life Transformation", "Report Length: 32 Pages | Format: Premium Life Path Report")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated app/engine/planetary_package_reports.py successfully.")

if __name__ == "__main__":
    update_package_report_generator()
    update_planetary_package_reports()
