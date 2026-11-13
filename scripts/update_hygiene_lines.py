with open('app/engine/charm_oracle_synthesizer.py', 'r', encoding='utf-8') as f:
    content = f.read()

target = '''        # Panch Tattva Elemental Hygiene
        hygiene_bullets = []
        for h in hygiene[:3]:
            hygiene_bullets.append(f"  • **{h['element']} ({h['governing_numbers']}):** Wear {h['remedy_item']} ({h['purpose']})")
        hygiene_str = "\\n".join(hygiene_bullets) if hygiene_bullets else "  • Wear Sphatik / Quartz or Rudraksha for foundational grounding."'''

replacement = '''        # Panch Tattva Elemental Hygiene
        hygiene_list = hygiene.get("prescriptions", []) if isinstance(hygiene, dict) else (hygiene or [])
        hygiene_bullets = []
        for h in hygiene_list[:4]:
            hygiene_bullets.append(f"  • **{h['element']} (Numbers {h['numbers']}):** {h['prescription']} — *{h['instruction']}*")
        hygiene_str = "\\n".join(hygiene_bullets) if hygiene_bullets else "  • Wear Sphatik / Quartz or Rudraksha for foundational grounding."'''

if target in content:
    content = content.replace(target, replacement, 1)
    with open('app/engine/charm_oracle_synthesizer.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS")
else:
    print("TARGET NOT FOUND")
