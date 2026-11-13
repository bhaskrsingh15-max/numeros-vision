import re

with open('app/engine/charm_oracle_synthesizer.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern matching from '# ── 4. Freemium Curiosity Hook' to '{curiosity_hook}"\n        )'
old_block_pattern = re.compile(
    r'[ \t]*# ── 4\. Freemium Curiosity Hook & CTA ──.*?'
    r'f"\{curiosity_hook\}"\s*\n\s*\)',
    re.DOTALL
)

def replacer(match):
    return '''        # ── 4. Humanized Birth Narrative (Zero Technical Jargon) ──
        birth_day_narrative = (
            sub.get("report_narrative") or
            sub.get("core_personality") or
            "You possess a natural gift for strategic foresight, personal resilience, and long-term mastery."
        )

        # Clean any stray internal calculation codes if present
        birth_day_narrative = re.sub(r'Category [A-D]|Graded Category|Intrinsic Potency|\\d+%', '', birth_day_narrative).strip()
        birth_day_narrative = re.sub(r'\\s{2,}', ' ', birth_day_narrative)

        # ── 5. Full Humanized Consultation Text ──
        steps_text = "\\n".join(f"• **Step {i+1}:** {step}" for i, step in enumerate(practical_steps))
        full_text = (
            f"Namaste {first_name} ✨\\n\\n"
            f"**1. What Your Numbers Reveal About '{topic_label}':**\\n"
            f"{diagnosis_text}\\n\\n"
            f"**2. Your Inborn Character & Life Dynamics:**\\n"
            f"• **Born on Day {birth_day} • {sub_arch}:** {birth_day_narrative}\\n"
            f"• **Inner Drive {driver} & Life Destiny {conductor}:** How your instinctive mindset meets your life path. Natural gifts include {dc_pos}. Thriving career paths often align with {dc_careers}.\\n"
            f"• **Balancing Vibration (Number {poorak_num} • {poorak_planet}):** Acts as your natural harmonizing energy. {clean_poorak_role}\\n"
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
        )'''

updated, count = old_block_pattern.subn(replacer, content, count=1)
if count == 1:
    with open('app/engine/charm_oracle_synthesizer.py', 'w', encoding='utf-8') as f:
        f.write(updated)
    print("SUCCESS: Updated charm_oracle_synthesizer.py cleanly.")
else:
    print(f"FAILED: Match count = {count}")
