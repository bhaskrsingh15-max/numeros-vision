import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# 1. Update app/charm/chat/response_composer.py
path_rc = os.path.join(BASE_DIR, "app", "charm", "chat", "response_composer.py")
with open(path_rc, "r", encoding="utf-8") as f:
    rc_text = f.read()

# Update direct_text section 2 title
rc_text = rc_text.replace(
    "**2. Timing Status & Verification:**",
    "**2. Temporal Cycle Alignment:**"
)

# Replace method_evidence_vm building
old_me_block = """        method_evidence_vm = []
        for ev in all_evaluations:
            cits = [
                {"sourceId": c["source_id"], "title": c["title"], "locator": c["locator"]}
                for c in ev.rule_evidence
            ]
            method_evidence_vm.append({
                "methodId": ev.method_id,
                "assessment": ev.assessment,
                "summary": ev.candidate_windows[0].get("label", "Evaluation complete") if ev.candidate_windows else "Not evaluated in consensus",
                "citations": cits
            })"""

new_me_block = """        METHOD_CLEAN_MAP = {
            "NUMEROLOGY_DASHA": "Primary Dasha Epicycle",
            "PYTHAGOREAN": "Pythagorean Harmonic Vibration",
            "VEDIC_NUMEROLOGY": "Vedic Planetary Numerology",
            "CHALDEAN_SOUND": "Chaldean Name Frequency",
            "KP_ASTROLOGY": "Dasha Temporal Rhythm",
            "BNN_ADAPTER": "Planetary Conjunction Dynamics",
            "BNN_ASTROLOGY": "Planetary Conjunction Dynamics",
            "VEDIC_ASTROLOGY": "Vedic Planetary Vibrations",
            "LAL_KITAB": "Harmonic Elemental Balance"
        }

        method_evidence_vm = []
        for ev in all_evaluations:
            if ev.method_id == "LAL_KITAB":
                continue  # Exclude non-numerology adapters
            
            cits = []
            for c in ev.rule_evidence:
                clean_title = (c.get("title", "")
                               .replace("Astrology", "Numerology")
                               .replace("Kundli", "Numerology Grid")
                               .replace("BNN", "Planetary Conjunctions")
                               .replace("KP", "Dasha Timing"))
                cits.append({"sourceId": c.get("source_id", ""), "title": clean_title, "locator": c.get("locator", "")})
            
            raw_summary = ev.candidate_windows[0].get("label", "Evaluation complete") if ev.candidate_windows else "Evaluation complete"
            clean_summary = (raw_summary
                             .replace("KP Astrology", "Dasha temporal cycle")
                             .replace("Bhrigu Nandi Nadi (BNN)", "Planetary conjunction vibration")
                             .replace("BNN", "Planetary Numerology")
                             .replace("Vedic Kundli", "Lo Shu vibrational grid")
                             .replace("Vedic astrology", "Vedic Numerology")
                             .replace("Lal Kitab", "Traditional balance")
                             .replace("astrology", "numerology")
                             .replace("Astrology", "Numerology"))

            method_evidence_vm.append({
                "methodId": METHOD_CLEAN_MAP.get(ev.method_id, ev.method_id.replace("_", " ")),
                "assessment": ev.assessment,
                "summary": clean_summary,
                "citations": cits
            })"""

if old_me_block in rc_text:
    rc_text = rc_text.replace(old_me_block, new_me_block)
    print("✓ Successfully sanitized method_evidence_vm in response_composer.py")
else:
    print("! Could not find exact old_me_block, checking...")

with open(path_rc, "w", encoding="utf-8") as f:
    f.write(rc_text)
print("✓ response_composer.py updated.")

# 2. Update practitioner.html
path_prac = os.path.join(BASE_DIR, "app", "static", "practitioner.html")
if os.path.exists(path_prac):
    with open(path_prac, "r", encoding="utf-8") as f:
        p_text = f.read()
    p_text = p_text.replace("Lead Astrologer / Practitioner Name", "Lead Numerologist / Practitioner Name")
    with open(path_prac, "w", encoding="utf-8") as f:
        f.write(p_text)
    print("✓ practitioner.html updated.")
