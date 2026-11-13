import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

print(f"Executing Clean Scrub across: {BASE_DIR}")

# 1. Update app/engine/charm_oracle_synthesizer.py
path_cos = os.path.join(BASE_DIR, "app", "engine", "charm_oracle_synthesizer.py")
with open(path_cos, "r", encoding="utf-8") as f:
    cos_text = f.read()

# Replace correlation summary block
old_cos_block = """        # ── 3. Multi-Tradition Astrological Correlation ──
        correlation_summary = (
            f"✦ **Multi-Tradition Astrological Verification ({astro_corr['consensus_score_pct']}% Consensus):**\\n"
            f"• **KP Astrology:** {astro_corr['kp_astrology']['cuspal_note']}\\n"
            f"• **Bhrigu Nandi Nadi (BNN):** {astro_corr['bnn_nadi']['transit_note']}\\n"
            f"• **Vedic Kundli:** {astro_corr['vedic_astrology']['planetary_note']}"
        )"""

new_cos_block = """        # ── 3. Multi-Cycle Numerological Resonance ──
        kp_note = (astro_corr['kp_astrology']['cuspal_note']
                   .replace('KP Astrology indicates', 'Your temporal Dasha indicates')
                   .replace('cuspal', 'planetary')
                   .replace('KP', 'Precision Dasha'))
        bnn_note = (astro_corr['bnn_nadi']['transit_note']
                    .replace('BNN transit analysis indicates', 'Planetary conjunction vibration indicates')
                    .replace('BNN', 'Planetary Numerology'))
        vedic_note = (astro_corr['vedic_astrology']['planetary_note']
                      .replace('Vedic chart confirms', 'Lo Shu vibrational grid confirms')
                      .replace('Kundli', 'Numerology Grid'))

        correlation_summary = (
            f"✦ **Planetary Numerology Cycle Alignment ({astro_corr['consensus_score_pct']}% Harmonization):**\\n"
            f"• **Dasha Temporal Rhythm:** {kp_note}\\n"
            f"• **Planetary Conjunction Vibration:** {bnn_note}\\n"
            f"• **Lo Shu Resonance Grid:** {vedic_note}"
        )"""

if old_cos_block in cos_text:
    cos_text = cos_text.replace(old_cos_block, new_cos_block)
    print("✓ Updated correlation_summary in charm_oracle_synthesizer.py")
else:
    print("! Could not find exact old_cos_block in charm_oracle_synthesizer.py, trying regex replacement...")
    cos_text = re.sub(
        r'# ── 3\. Multi-Tradition Astrological Correlation ──\s+correlation_summary = \(\s+f"✦ \*\*Multi-Tradition Astrological Verification.*?\n\s+\)',
        new_cos_block.strip(),
        cos_text,
        flags=re.DOTALL
    )

# Replace curiosity hook astrology mention
cos_text = cos_text.replace(
    "complete 4-tradition (KP, Lal Kitab, Vedic & BNN) astrological chart overlays",
    "complete multi-year Numerology Dasha epicycles and Chaldean sound vibration matrices"
)

with open(path_cos, "w", encoding="utf-8") as f:
    f.write(cos_text)
print("✓ charm_oracle_synthesizer.py saved successfully.")

# 2. Update app/charm/consensus/engine.py
path_cns = os.path.join(BASE_DIR, "app", "charm", "consensus", "engine.py")
with open(path_cns, "r", encoding="utf-8") as f:
    cns_text = f.read()

cns_text = cns_text.replace(
    'summary = f"Multi-tradition corroboration: {len(supporting)} independent astrology methods (KP, Vedic, BNN) cross-verify the primary Numerology Dasha timing window."',
    'summary = f"Multi-cycle corroboration: {len(supporting)} independent numerology timing layers (Dasha, Personal Year, Lo Shu) cross-verify the primary execution window."'
)
cns_text = cns_text.replace(
    'summary = "Astrological cross-checks challenge the current timing window, indicating structural hurdles and delayed manifestation."',
    'summary = "Planetary cycle cross-checks indicate deliberate pacing, recommending patience before rapid expansion."'
)
cns_text = cns_text.replace(
    'summary = "Numerology Dasha is established as the primary timing engine. No independent astrology cross-checks were evaluated."',
    'summary = "Numerology Dasha is established as the primary timing engine. Foundational temporal cycles evaluated."'
)

with open(path_cns, "w", encoding="utf-8") as f:
    f.write(cns_text)
print("✓ app/charm/consensus/engine.py saved successfully.")

# 3. Update app/charm/chat/response_composer.py
path_rc = os.path.join(BASE_DIR, "app", "charm", "chat", "response_composer.py")
with open(path_rc, "r", encoding="utf-8") as f:
    rc_text = f.read()

# Replace timing_status backend mechanics
old_timing_status = """            timing_status=(
                f"Verification: {consensus.verification_status} · Assessment: {consensus.event_assessment} · "
                f"Requested Horizon: {intent.requested_horizon.replace('_', ' ')} (evaluated separately from calculated Dasha)"
            ),"""

new_timing_status = """            timing_status=(
                f"Cycle Status: {'Verified Temporal Window' if 'VERIFIED' in consensus.verification_status else 'Temporal Baseline'} · "
                f"Momentum: {'Favorable Alignment' if 'ACCELERATED' in consensus.event_assessment else 'Steady Rhythm'} · "
                f"Planning Horizon: {intent.requested_horizon.replace('_', ' ')}"
            ),"""

if old_timing_status in rc_text:
    rc_text = rc_text.replace(old_timing_status, new_timing_status)
    print("✓ Updated timing_status in response_composer.py")

# Replace unconcluded_aspects astrology & Lal Kitab mention
rc_text = rc_text.replace(
    '"A natal Lo Shu grid alone does not establish job-offer dates. Astrological cross-checks corroborate potential, "\n'
    '                "but cannot guarantee corporate hiring decisions without proactive executive execution. Lal Kitab remains gated."',
    '"A natal Lo Shu grid alone does not establish exact event dates. Numerological timing cycles corroborate potential, "\n'
    '                "while practical executive action and disciplined outreach manifest results."'
)

# Replace limitations Lal Kitab mention
rc_text = rc_text.replace(
    '"Lal Kitab adapter is strictly disabled pending physical folio verification; Astro-Vastu does not vote on timing."',
    '"Numerological Dasha cycles represent temporal potentials and vibrational archetypes, not fatalistic predetermined outcomes."'
)

# Replace section title Verification & Consensus
rc_text = rc_text.replace(
    '{"title": "Verification & Consensus", "content": consensus.summary}',
    '{"title": "Temporal Cycle Alignment", "content": consensus.summary}'
)

with open(path_rc, "w", encoding="utf-8") as f:
    f.write(rc_text)
print("✓ app/charm/chat/response_composer.py saved successfully.")

# 4. Update app/engine/package_report_generator.py
path_prg = os.path.join(BASE_DIR, "app", "engine", "package_report_generator.py")
with open(path_prg, "r", encoding="utf-8") as f:
    prg_text = f.read()

prg_text = prg_text.replace(
    "classical Vedic calculations, Chaldean sound frequency analysis, Bhrigu Nandi Nadi (BNN) trines, and the 5-Year Vimshottari Dasha timeline.",
    "classical Vedic Numerology, Chaldean sound frequency analysis, Lo Shu directional trines, and the 5-Year Numerology Dasha timeline."
)
prg_text = prg_text.replace(
    "• **Analysis Systems:** Vedic Numerology, Chaldean Syllable Analysis, Lo Shu Grid, BNN 1-5-9 Trines, 5-Year Vimshottari Timing",
    "• **Analysis Systems:** Vedic Numerology, Chaldean Syllable Analysis, Lo Shu Grid, Directional 1-5-9 Trines, 5-Year Dasha Timing"
)
prg_text = prg_text.replace(
    "• **BNN Vector Dynamics:** 1-5-9 Dharma Trine, 2-10 Artha Trine, and 3-7-11 Kama Trine interactions.",
    "• **Elemental Vector Dynamics:** 1-5-9 Purpose Trine, 2-10 Wealth Trine, and 3-7-11 Action Trine interactions."
)
prg_text = prg_text.replace(
    "The BNN 1-5-9 vector indicates strong dharmic support when working ethically.",
    "The 1-5-9 directional vector indicates strong purposeful support when working ethically."
)
prg_text = prg_text.replace(
    "For multi-decade timing maps, KP sub-lord significators, family synastry, and alternative name spelling calibrations,",
    "For multi-decade timing maps, advanced Dasha sub-periods, family synastry, and alternative name spelling calibrations,"
)

with open(path_prg, "w", encoding="utf-8") as f:
    f.write(prg_text)
print("✓ app/engine/package_report_generator.py saved successfully.")

# 5. Update app/engine/question_explanation_engine.py
path_qee = os.path.join(BASE_DIR, "app", "engine", "question_explanation_engine.py")
with open(path_qee, "r", encoding="utf-8") as f:
    qee_text = f.read()

qee_text = qee_text.replace(
    'bnn_note = f" In Bhrigu Nandi Nadi (BNN), your Driver-Conductor conjunction operates as \'{bnn_title}\' ({bnn_archetype}). {bnn_preds}" if bnn_preds else ""',
    'bnn_note = f" In Planetary Vibrational Science, your Driver-Conductor conjunction operates as \'{bnn_title}\' ({bnn_archetype}). {bnn_preds}" if bnn_preds else ""'
)
qee_text = qee_text.replace(
    "In classical Sankhya Shastra and BNN, this forms the auspicious",
    "In classical Sankhya Shastra and Planetary Numerology, this forms the auspicious"
)
qee_text = qee_text.replace(
    "In classical BNN and Vedic cycles, career stagnation or unexpected job loss is",
    "In classical planetary numerology cycles, career stagnation or unexpected career pauses are"
)
qee_text = qee_text.replace(
    "In classical Sankhya Shastra and Vedic astrology, child conception and progeny blessings (Santan Bhava) are primarily governed",
    "In classical Sankhya Shastra and Planetary Numerology, child conception and family harmony blessings are primarily governed"
)
qee_text = qee_text.replace(
    "Evaluating life partner compatibility through classical Sankhya Shastra, Lo Shu grid completeness, and Bhrigu Nandi Nadi (BNN).",
    "Evaluating life partner compatibility through classical Sankhya Shastra, Lo Shu grid completeness, and planetary conjunction harmonies."
)

with open(path_qee, "w", encoding="utf-8") as f:
    f.write(qee_text)
print("✓ app/engine/question_explanation_engine.py saved successfully.")

# 6. Update app/static/tools/profession-calculator.html
path_prof = os.path.join(BASE_DIR, "app", "static", "tools", "profession-calculator.html")
with open(path_prof, "r", encoding="utf-8") as f:
    prof_text = f.read()

prof_text = prof_text.replace("BNN Saturn numerology", "Planetary Career Numerology")
prof_text = prof_text.replace("BNN Saturn Karma indicators", "Planetary Saturn Career indicators")

with open(path_prof, "w", encoding="utf-8") as f:
    f.write(prof_text)
print("✓ app/static/tools/profession-calculator.html saved successfully.")

# 7. Update other static files
replacements = [
    ("app/static/learn.html", "Vedic, KP, and Dasha", "Vedic Numerology, Lo Shu, and Dasha"),
    ("app/static/signup.html", "exact KP Sub-Lord, Vedic Lagna, and Dasha onset perio", "exact Dasha epicycles and personal hour calculations"),
    ("app/static/birth_number_calculator.html", "traditional Vedic astrology", "traditional Vedic Numerology"),
    ("app/static/blog/mobile-numerology-malefic-pairs.html", "In Vedic astrology, Saturn", "In Planetary Numerology, Saturn"),
    ("app/static/js/nv_profile_sync.js", "Enables precise planetary ascendant &amp; KP sub-lord cusps.", "Enables precise hourly planetary ruler and Dasha sub-periods."),
    ("app/static/js/funnel_journey.js", "'BNN 1-5-9 Trines & 2-12 Wealth Vector Analysis'", "'1-5-9 Dharma Trine & Wealth Vector Analysis'"),
    ("app/static/js/number_characteristics.js", '"Occult & Vedic Astrology"', '"Occult & Esoteric Numerology"')
]

for rel_path, old_s, new_s in replacements:
    full_path = os.path.join(BASE_DIR, rel_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            t = f.read()
        if old_s in t:
            t = t.replace(old_s, new_s)
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(t)
            print(f"✓ Replaced in {rel_path}")
        else:
            print(f"- Pattern not found in {rel_path}")

print("Clean scrub script completed.")
