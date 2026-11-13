import json

with open('data/knowledge_base/nv_think_rule_cards_v0.1.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

lines = []
lines.append('# NV THINK™ — Complete Rule Cards Registry v0.1')
lines.append('**Registry:** `numeros_vision_rule_cards`  ')
lines.append('**Version:** `0.1-draft`  ')
lines.append('**Governance Status:** Internal Draft — Awaiting Final Founder Signoff  ')
lines.append('**Framework:** 7-Stage Logic-to-Psychology (`Logic → Observation → Behaviour → Psychology → Interpretation → Validation → Prediction`)  ')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## 1. Executive Summary & Inventory')
lines.append('')
lines.append(f'- **Single Cards (Mulank 1–9):** {len(d.get("single_cards", []))}')
lines.append(f'- **Master Number Cards (11, 22):** {len(d.get("master_cards", []))}')
lines.append(f'- **Compound Cards (10–52):** {len(d.get("compound_cards", []))}')
lines.append(f'- **Total Registered Cards:** {len(d.get("single_cards", [])) + len(d.get("master_cards", [])) + len(d.get("compound_cards", []))}')
lines.append('')
lines.append('### Strict Non-Negotiable Directives Enforced:')
lines.append('1. **Zero Certainty / Zero Superstition:** All draft interpretations strictly use softened probabilistic language (`traditionally linked with`, `tends to`, `growth edge is`).')
lines.append('2. **Validation Status:** Explicitly set to `untested` across all 54 cards.')
lines.append('3. **Prediction Status:** Explicitly set to `blocked` across all 54 cards.')
lines.append('4. **Sensitivity Guardrails:** All 8 sensitive compounds (`16, 18, 26, 28, 29, 40, 43, 48`) carry softened growth phrasing. Raw fatalistic warnings are strictly quarantined to internal provenance.')
lines.append('')
lines.append('---')
lines.append('')
lines.append('## 2. Mulank 1 to 9 (Single Digit Archetypes)')
lines.append('')
lines.append('| Mulank | Planetary Ruler | Strengths | Watch-Outs | Psychology / Stress Drive | Draft Customer Interpretation | Testable Survey Statement |')
lines.append('|---|---|---|---|---|---|---|')

for c in d.get('single_cards', []):
    num = c['number']
    planet = c['observation'].get('planet_chaldean_indian', '-')
    strengths = c['behaviour'].get('strengths', '-')
    watchouts = c['behaviour'].get('watch_outs', '-')
    psy = c.get('psychology', '-')
    draft = c.get('interpretation_draft', '-')
    survey = c.get('validation', {}).get('testable_statement', '-')
    lines.append(f'| **{num}** | {planet} | {strengths} | {watchouts} | {psy} | {draft} | {survey} |')

lines.append('')
lines.append('---')
lines.append('')
lines.append('## 3. Master Numbers (11 & 22)')
lines.append('')
lines.append('| Master | Reduces To | Traditional Archetype | Watch-Outs | Draft Customer Interpretation | Validation | Prediction |')
lines.append('|---|---|---|---|---|---|---|')

for c in d.get('master_cards', []):
    num = c['number']
    red = c.get('reduces_to', '-')
    obs = c.get('observation', '-')
    watchouts = c.get('behaviour_watch_outs', '-')
    draft = c.get('interpretation_draft', '-')
    val = c.get('validation', {}).get('status', 'untested')
    pred = c.get('prediction', {}).get('status', 'blocked')
    lines.append(f'| **{num}** | {red} | {obs} | {watchouts} | {draft} | `{val}` | `{pred}` |')

lines.append('')
lines.append('---')
lines.append('')
lines.append('## 4. Compound Numbers (10 to 52)')
lines.append('')
lines.append('| No. | Reduces | Traditional Archetype | Day Lens (Webster) | Draft Customer Interpretation | Sensitivity Flag |')
lines.append('|---|---|---|---|---|---|')

for c in d.get('compound_cards', []):
    num = c['number']
    red = c.get('reduces_to', '-')
    obs = c.get('observation', '-')
    day = c.get('behaviour_day_lens', '-')
    draft = c.get('interpretation_draft', '-')
    sens = c.get('sensitivity_flag', 'none')
    flag_badge = f'**`{sens}`**' if sens != 'none' else '`none`'
    lines.append(f'| **{num}** | {red} | {obs} | {day} | {draft} | {flag_badge} |')

lines.append('')

with open('docs/NV_THINK_RULE_CARDS_V0.1.md', 'w', encoding='utf-8') as out:
    out.write('\n'.join(lines))

print('Successfully generated docs/NV_THINK_RULE_CARDS_V0.1.md')
