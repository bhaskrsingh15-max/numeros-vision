# -*- coding: utf-8 -*-
import os

path = os.path.join("app", "charm", "chat", "response_composer.py")
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old_fallback = '''        direct_text = consult_narrative.get("full_dialogue_text") or (
            f"Namaste {first_name} 🙏\\n\\n"
            f"**1. Career Takeaway:** {human_friendly.takeaway}\\n\\n"
            f"**2. Temporal Cycle Alignment:** {human_friendly.timing_status}\\n\\n"
            f"**3. Supported by Verified Data:** {human_friendly.supported_by_report}\\n\\n"
            f"**4. What Cannot Yet Be Concluded:** {human_friendly.unconcluded_aspects}\\n\\n"
            f"**5. Input & Calculation Trace:** {human_friendly.missing_inputs_explanation}\\n\\n"
            f"**6. Practical Next Steps:**\\n• " + "\\n• ".join(human_friendly.practical_actions) + f"\\n\\n"
            f"**7. Next Step:** {human_friendly.followup_question}"
        )'''

new_fallback = '''        direct_text = consult_narrative.get("full_dialogue_text") or (
            f"Namaste {first_name} 🙏\\n\\n"
            f"**1. Career & Personal Momentum:** {human_friendly.takeaway}\\n\\n"
            f"**2. Active Timing & Cycle:** {human_friendly.timing_status}\\n\\n"
            f"**3. Inborn Strengths & Direction:** {human_friendly.supported_by_report}\\n\\n"
            f"**4. Grounded Perspective:** {human_friendly.unconcluded_aspects}\\n\\n"
            f"**5. Practical Action Steps:**\\n• " + "\\n• ".join(human_friendly.practical_actions) + f"\\n\\n"
            f"**6. Next Reflection:** {human_friendly.followup_question}"
        )'''

# Also clean up the missing-input fallback text at lines 151-160
old_abstain = '''            direct_text = (
                f"Namaste {user_name} 🙏\\n\\n"
                f"**1. Career Takeaway:** {human_friendly.takeaway}\\n\\n"
                f"**2. Timing Status:** {human_friendly.timing_status}\\n\\n"
                f"**3. What Can Be Concluded:** {human_friendly.supported_by_report}\\n\\n"
                f"**4. What Cannot Be Concluded:** {human_friendly.unconcluded_aspects}\\n\\n"
                f"**5. Missing Requirements:** {human_friendly.missing_inputs_explanation}\\n\\n"
                f"**6. Practical Next Steps:**\\n• " + "\\n• ".join(human_friendly.practical_actions) + f"\\n\\n"
                f"**7. Next Step:** {human_friendly.followup_question}"
            )'''

new_abstain = '''            direct_text = (
                f"Namaste {user_name} 🙏\\n\\n"
                f"**1. Perspective:** {human_friendly.takeaway}\\n\\n"
                f"**2. Timing Status:** {human_friendly.timing_status}\\n\\n"
                f"**3. Current Findings:** {human_friendly.supported_by_report}\\n\\n"
                f"**4. Grounded Boundaries:** {human_friendly.unconcluded_aspects}\\n\\n"
                f"**5. Important Details:** {human_friendly.missing_inputs_explanation}\\n\\n"
                f"**6. Practical Next Steps:**\\n• " + "\\n• ".join(human_friendly.practical_actions) + f"\\n\\n"
                f"**7. Next Step:** {human_friendly.followup_question}"
            )'''

# Normalize newlines to \n for matching
text_normalized = text.replace('\r\n', '\n')
old_fallback_norm = old_fallback.replace('\r\n', '\n')
new_fallback_norm = new_fallback.replace('\r\n', '\n')
old_abstain_norm = old_abstain.replace('\r\n', '\n')
new_abstain_norm = new_abstain.replace('\r\n', '\n')

text_normalized = text_normalized.replace(old_fallback_norm, new_fallback_norm)
text_normalized = text_normalized.replace(old_abstain_norm, new_abstain_norm)

with open(path, "w", encoding="utf-8") as f:
    f.write(text_normalized)

print("SUCCESS: response_composer.py updated.")
