import re

with open('app/engine/charm_oracle_synthesizer.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '        # ── 2. Cultural & Faith-Tailored Remedial Alignment ──'

replacement = '''        # ── 1.1 Multi-Dimensional Planetary Architecture ──
        sub_code = sub.get("code", f"{birth_day}")
        sub_cat = sub.get("strength_category", "B")
        sub_title = sub.get("strength_title", "Balanced")
        sub_score = sub.get("strength_potency_score", 80)
        sub_arch = sub.get("archetype", "Pioneer")
        sub_comp = sub.get("planetary_composition", "")

        stars_count = dc.get("star_rating", 4.0)
        stars_str = "★" * int(stars_count) + ("½" if (stars_count % 1) >= 0.5 else "")
        dc_rel = dc.get("relationship_type", "Harmonious")
        dc_pos = ", ".join(dc.get("positive_traits", [])[:3])
        dc_careers = ", ".join(dc.get("recommended_careers", [])[:3])
        dc_warn = dc.get("high_risk_warning", "")

        poorak_num = poorak.get("poorak_number", 5)
        poorak_planet = poorak.get("poorak_planet", "Mercury")
        poorak_role = poorak.get("rationale", "")
        poorak_ritual = poorak.get("harmonizing_ritual", "")

        # Repetition Degrees Highlights
        degree_highlights = []
        if pair_numbers:
            degree_highlights.append(f"Pair / Balanced (Peak Harmony): Numbers {pair_numbers}")
        if aggressive_numbers:
            degree_highlights.append(f"Exaggerated / High-Intensity: Numbers {aggressive_numbers}")
        if missing_numbers:
            degree_highlights.append(f"Missing (Karmic Void): Numbers {missing_numbers[:3]}")
        degree_str = " | ".join(degree_highlights) if degree_highlights else "Balanced Matrix"

        # Panch Tattva Elemental Hygiene
        hygiene_bullets = []
        for h in hygiene[:3]:
            hygiene_bullets.append(f"  • **{h['element']} ({h['governing_numbers']}):** Wear {h['remedy_item']} ({h['purpose']})")
        hygiene_str = "\\n".join(hygiene_bullets) if hygiene_bullets else "  • Wear Sphatik / Quartz or Rudraksha for foundational grounding."

        # ── 2. Cultural & Faith-Tailored Remedial Alignment ──'''

old_full_text = '''        full_text = (
            f"Namaste {first_name} 🙏\\n\\n"
            f"**1. What Your Numbers Reveal About '{topic_label}':**\\n"
            f"{diagnosis_text}\\n\\n"
            f"**2. Active Cycle & Timing Horizon:**\\n"
            f"{core_advice}\\n\\n"
            f"**3. Practical Steps to Accelerate Your Alignment:**\\n"
            + "\\n".join(f"• **Step {i+1}:** {step}" for i, step in enumerate(practical_steps)) + "\\n\\n"
            f"**4. Sacred Lifestyle & Faith Attunement ({faith.capitalize()} Tradition):**\\n"
            f"{faith_remedy}\\n\\n"
            f"{correlation_summary}"
            f"{curiosity_hook}"
        )'''

new_full_text = '''        full_text = (
            f"Namaste {first_name} 🙏\\n\\n"
            f"**1. What Your Numbers Reveal About '{topic_label}':**\\n"
            f"{diagnosis_text}\\n\\n"
            f"**2. Constitutional Architecture & Synergy Matrix:**\\n"
            f"• **Birth Sub-Date {birth_day} ({sub_code}):** **Category {sub_cat} ({sub_title})** with **{sub_score}% Intrinsic Potency**. Archetype: *{sub_arch}* ({sub_comp}).\\n"
            f"• **Driver {driver} & Conductor {conductor} Synergy:** {stars_str} **{stars_count}/5 Stars** ({dc_rel} Dynamics). Natural Gifts: {dc_pos}. Ideal Careers: {dc_careers}."
            + (f" ⚠️ *Notice:* {dc_warn}" if dc_warn else "") + "\\n"
            f"• **Complementary (Poorak / पूरक) Harmonizer:** **Number {poorak_num} ({poorak_planet})** acts as your cosmic peacemaker bridge. *{poorak_role}*\\n"
            f"• **Lo Shu Power Repetition:** {degree_str}\\n\\n"
            f"**3. Active Cycle & Timing Horizon:**\\n"
            f"{core_advice}\\n\\n"
            f"**4. Practical Steps to Accelerate Your Alignment:**\\n"
            + "\\n".join(f"• **Step {i+1}:** {step}" for i, step in enumerate(practical_steps)) + "\\n\\n"
            f"**5. Non-Negotiable Panch Tattva Bodyguard Hygiene (Physical Touch to Skin):**\\n"
            f"{hygiene_str}\\n"
            f"  *(Note: Natural wooden/crystal elements must touch your skin directly before applying any external rituals).*\\n\\n"
            f"**6. Sacred Lifestyle & Faith Attunement ({faith.capitalize()} Tradition):**\\n"
            f"{faith_remedy}\\n\\n"
            f"{correlation_summary}"
            f"{curiosity_hook}"
        )'''

if target in content:
    content = content.replace(target, replacement, 1)
    if old_full_text in content:
        content = content.replace(old_full_text, new_full_text, 1)
        with open('app/engine/charm_oracle_synthesizer.py', 'w', encoding='utf-8') as f:
            f.write(content)
        print('SUCCESS: Both replacements applied cleanly!')
    else:
        print('FAILED: old_full_text not matched')
else:
    print('FAILED: target not matched')
