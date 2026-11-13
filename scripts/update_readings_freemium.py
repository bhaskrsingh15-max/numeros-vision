# -*- coding: utf-8 -*-
import os

path = os.path.join("app", "api", "readings.py")
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

old_block = '''        if not has_active_credit:
            freemium_response = {
                "status": "success",
                "phase": "diagnosis",
                "is_freemium_gate": True,
                "is_premium": False,
                "trace_id": gateway_audit.get("trace_id"),
                "governing_policy": "/disclaimer",
                "question": clean_q,
                "classified_topic": topic,
                "topic_display": topic_label,
                "alignment_status": alignment_status,
                "alignment_grade": alignment_grade,
                "alignment_score": alignment_score,
                "alignment_summary": alignment_summary,
                "direct_answer": (charm_turn.assistant_message.get("text") if (charm_turn and charm_turn.assistant_message and charm_turn.assistant_message.get("text")) else (expl["direct_answer"] + "\\n\\n" + loshu_chart_md)),
                "humanized_consultation": (charm_turn.assistant_message.get("text") if (charm_turn and charm_turn.assistant_message and charm_turn.assistant_message.get("text")) else expl["direct_answer"]),
                "loshu_grid": lo_shu_data,
                "loshu_grid_markdown": loshu_chart_md,
                "charm_prediction": charm_prediction,
                "age_numerology": age_data,
            "age_numerology": age_data,
                "age_numerology": age_data,
                "why_this_is_happening": expl["why_this_is_happening"],
                "validation_question": expl.get("validation_question", ""),
                "permission_prompt": expl.get("permission_prompt", ""),
                "can_suggest_remedies": True,
                "remedies_gated": True,
                "remedies": expl["remedies"],
                "lucky_elements": expl["lucky_elements"],
                "vedic_lifestyle_guidance": expl.get("vedic_lifestyle_guidance", {}),
                "core_matrix_analysis": expl.get("core_matrix_analysis"),
                "grounded_citations": expl.get("grounded_citations", []),
                "driver_number": driver,
                "conductor_number": conductor,
                "preview_notice": "Your multi-engine occult diagnosis is complete. To anveil consecrated remedies and continuous question predictions, choose a Charm AI pass.",
                "paywall": paywall_spec
            }
            return apply_ai_disclosure(freemium_response)'''

new_block = '''        if not has_active_credit:
            freemium_response = {
                "status": "success",
                "phase": "diagnosis",
                "is_freemium_gate": True,
                "is_premium": False,
                "trace_id": gateway_audit.get("trace_id"),
                "governing_policy": "/disclaimer",
                "question": clean_q,
                "classified_topic": topic,
                "topic_display": topic_label,
                "alignment_status": alignment_status,
                "alignment_grade": alignment_grade,
                "alignment_score": alignment_score,
                "alignment_summary": alignment_summary,
                "direct_answer": (charm_turn.assistant_message.get("text") if (charm_turn and charm_turn.assistant_message and charm_turn.assistant_message.get("text")) else (expl["direct_answer"] + "\\n\\n" + loshu_chart_md)),
                "humanized_consultation": (charm_turn.assistant_message.get("text") if (charm_turn and charm_turn.assistant_message and charm_turn.assistant_message.get("text")) else expl["direct_answer"]),
                "loshu_grid": lo_shu_data,
                "loshu_grid_markdown": loshu_chart_md,
                "charm_prediction": None,
                "age_numerology": age_data,
                "why_this_is_happening": None,
                "validation_question": expl.get("validation_question", ""),
                "permission_prompt": expl.get("permission_prompt", ""),
                "can_suggest_remedies": False,
                "remedies_gated": True,
                "remedies": [],
                "lucky_elements": expl.get("lucky_elements", {}),
                "vedic_lifestyle_guidance": {},
                "core_matrix_analysis": None,
                "grounded_citations": [],
                "driver_number": driver,
                "conductor_number": conductor,
                "preview_notice": "Your foundational numerology reading is complete. To anveil personalized consecrated remedies and multi-year timeline forecasts, choose a Charm AI pass.",
                "paywall": paywall_spec
            }
            return apply_ai_disclosure(freemium_response)'''

text_norm = text.replace('\r\n', '\n')
old_block_norm = old_block.replace('\r\n', '\n')
new_block_norm = new_block.replace('\r\n', '\n')

if old_block_norm in text_norm:
    text_norm = text_norm.replace(old_block_norm, new_block_norm)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text_norm)
    print("SUCCESS: readings.py updated.")
else:
    print("ERROR: old_block not found in readings.py")
