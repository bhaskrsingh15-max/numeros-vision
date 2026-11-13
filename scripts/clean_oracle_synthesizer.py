# -*- coding: utf-8 -*-
import os

path = os.path.join("app", "engine", "charm_oracle_synthesizer.py")
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# Target the entire block from # ── 1.1 Inborn Character & Natural Alignment ── to the return statement
start_marker = "# ── 1.1 Inborn Character & Natural Alignment ──"
end_marker = "return {"

clean_block = '''# ── 1.1 Inborn Character & Natural Alignment ──
        sub_arch = sub.get("archetype", "The Radiant Builder")
        sub_comp = sub.get("planetary_composition", f"Day {birth_day}")
        
        # Clean up subdate archetype and composition for conversational warmth
        clean_comp = re.sub(r'\\(.*?Clash.*?\\)', '', sub_comp).strip()
        if not clean_comp:
            clean_comp = f"Day {birth_day}"

        dc_pos = ", ".join(dc.get("positive_traits", [])[:3]) or "Clear decision-making, strategic vision, perseverance"
        dc_careers = ", ".join(dc.get("recommended_careers", [])[:3]) or "Leadership, Administration & Strategic Planning"

        poorak_num = poorak.get("poorak_number", 5)
        poorak_planet = poorak.get("poorak_planet", "Mercury")
        poorak_role = poorak.get("rationale", "")
        clean_poorak_role = poorak_role.replace("fills the central Earth anchor of your Lo Shu Grid, providing unshakable emotional stability", "provides steady grounding, mental flexibility, and ease of communication")

        # Repetition & Grid Balance Focus
        balance_focus = []
        if pair_numbers:
            balance_focus.append(f"Balanced Strengths: Number {', '.join(str(n) for n in pair_numbers)} (Steady harmony and focused flow)")
        if 5 in missing_numbers or 6 in missing_numbers:
            missing_names = []
            if 5 in missing_numbers: missing_names.append("Number 5 (Flexibility & Pacing)")
            if 6 in missing_numbers: missing_names.append("Number 6 (Harmony & Renewal)")
            balance_focus.append(f"Mindful Cultivation: {' & '.join(missing_names)} through calm daily habits")
        grid_balance_text = " | ".join(balance_focus) if balance_focus else "Your birth grid maintains an even, balanced distribution."

        # Gentle Daily Habits for Elemental Well-Being
        hygiene_list = hygiene.get("prescriptions", []) if isinstance(hygiene, dict) else (hygiene or [])
        hygiene_bullets = []
        for h in hygiene_list[:3]:
            elem = h.get('element', 'Earth')
            instr = h.get('instruction', '')
            instr_clean = instr.replace('Must touch physical skin continuously', 'Wear natural materials touching skin for grounding').replace('strictly avoid', 'mindfully balance')
            hygiene_bullets.append(f"  • **{elem} Alignment:** {h.get('prescription', '')} — *{instr_clean}*")
        hygiene_str = "\\n".join(hygiene_bullets) if hygiene_bullets else "  • **Foundational Grounding:** Keep a natural wooden or clear quartz accessory nearby to stay centered during demanding days."

        # ── 2. Cultural & Faith-Tailored Remedial Alignment ──
        faith_remedy = self._get_faith_tailored_remedy(faith, driver, conductor, missing_numbers)

        # ── 3. Timing & Seasonal Context ──
        correlation_summary = (
            f"**Timing & Seasonal Context:**\\n"
            f"Navigating Personal Year {personal_year} in 2026 creates favorable cyclical momentum for thoughtful planning and strategic progress. "
            f"Your active timing window ({timing_window_str}) particularly supports disciplined initiatives, professional outreach, and laying solid foundations for enduring success."
        )

        # ── 4. Freemium Curiosity Hook & CTA ──
        if not is_premium:
            curiosity_hook = (
                f"\\n\\n---\\n"
                f"### ✦ ANVEIL EVERY CHARM ✦\\n"
                f"*Your foundational reading reveals the overarching rhythms of your chart. To explore your complete multi-year milestone timeline, "
                f"favorable monthly decision windows, in-depth Dasha cycles, and personalized consecrated rituals, choose an option below:*\\n\\n"
                f"<div style=\\"display:flex; gap:10px; flex-wrap:wrap; margin-top:12px;\\">\\n"
                f"<a href=\\"/pricing/#charm-ai\\" class=\\"btn-primary-gold\\" style=\\"display:inline-block; padding:9px 20px; font-size:0.84rem; text-decoration:none; border-radius:8px;\\">Anveil Full Charm AI Pass (from ₹199) →</a>\\n"
                f"<a href=\\"/reports_catalogue/\\" class=\\"btn-secondary-amber\\" style=\\"display:inline-block; padding:9px 20px; font-size:0.84rem; text-decoration:none; border-radius:8px;\\">Explore 12-Page Personalised Blueprint (₹510) →</a>\\n"
                f"</div>"
            )
        else:
            curiosity_hook = (
                f"\\n\\n---\\n"
                f"### ✦ PERSONALIZED DOSSIER DETAILS ✦\\n"
                f"**Multi-Year Timing Window:** You are navigating a key growth corridor spanning {timing_window_str}. "
                f"Maintain consistent focus on your core priorities and daily grounding habits to maximize this favorable momentum."
            )

        # ── 5. Full Humanized Consultation Text ──
        steps_text = "\\n".join(f"• **Step {i+1}:** {step}" for i, step in enumerate(practical_steps))
        full_text = (
            f"Namaste {first_name} 🙏\\n\\n"
            f"**1. What Your Numbers Reveal About '{topic_label}':**\\n"
            f"{diagnosis_text}\\n\\n"
            f"**2. Your Inborn Character & Life Dynamics:**\\n"
            f"• **Born on Day {birth_day} · {sub_arch}:** You possess a natural gift for strategic foresight and endurance. In our classical database, this birth day reflects a capacity to turn complex responsibilities and early trials into enduring, long-term mastery.\\n"
            f"• **Inner Drive {driver} & Life Destiny {conductor}:** How your instinctive mindset meets your life path. Natural gifts include {dc_pos}. Thriving career paths often align with {dc_careers}.\\n"
            f"• **Balancing Vibration (Number {poorak_num} · {poorak_planet}):** Acts as your natural harmonizing energy. {clean_poorak_role}\\n"
            f"• **Elemental Balance Focus:** {grid_balance_text}\\n\\n"
            f"**3. Active Cycle & Timing Momentum:**\\n"
            f"{core_advice}\\n\\n"
            f"**4. Practical Steps for Daily Progress:**\\n"
            f"{steps_text}\\n\\n"
            f"**5. Natural Daily Rhythms & Elemental Well-Being:**\\n"
            f"{hygiene_str}\\n\\n"
            f"**6. Daily Mindfulness & Centering ({faith.capitalize()} Tradition):**\\n"
            f"{faith_remedy}\\n\\n"
            f"{correlation_summary}"
            f"{curiosity_hook}"
        )

        '''

start_idx = text.find(start_marker)
end_idx = text.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    new_text = text[:start_idx] + clean_block + text[end_idx:]
    with open(path, "w", encoding="utf-8") as f:
        f.write(new_text)
    print("SUCCESS")
else:
    print(f"Markers not found: start={start_idx}, end={end_idx}")
