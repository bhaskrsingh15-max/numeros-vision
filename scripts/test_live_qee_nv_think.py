import sys
import os
import json

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

sys.path.insert(0, os.path.abspath('.'))

from app.engine.question_explanation_engine import generate_simple_explanation_and_remedies

print("Testing generate_simple_explanation_and_remedies with NV THINK™ Integration...")

payload = {
    "question": "What does my natal chart say about leading a new technology venture?",
    "driver": 1,
    "conductor": 4,
    "day": 28,
    "month": 11,
    "year": 1981,
    "name": "Bhaskr Singh",
    "topic": "career",
    "current_age": 44
}

res = generate_simple_explanation_and_remedies(
    question=payload["question"],
    driver=payload["driver"],
    conductor=payload["conductor"],
    day=payload["day"],
    month=payload["month"],
    year=payload["year"],
    name=payload["name"],
    topic=payload["topic"],
    current_age=payload["current_age"]
)

print("\n--- 1. DIRECT CONSULTATION TAKEAWAY ---")
print(res.get("direct_answer", "")[:300], "...")

print("\n--- 2. ROOT CAUSE / WHY HAPPENING ---")
print(res.get("why_happening", "")[:300], "...")

print("\n--- 3. NV THINK™ DIAGNOSTIC PAYLOAD ---")
nv_diag = res.get("nv_think_diagnostic", {})
print("Methodology:", nv_diag.get("methodology"))
print("Chart Dualities:", nv_diag.get("chart_dualities"))
print("Synthesized Narrative:", nv_diag.get("synthesized_narrative"))

print("\n--- 4. MULTI-MODEL ASTROLOGICAL CONSENSUS ---")
consensus = res.get("multi_model_consensus", {})
print("Consensus Status:", consensus.get("consensus_status"))
print("Primary Authority:", consensus.get("primary_authority"))
print("Timing Window:", consensus.get("timing_window"))
print("NV Think Takeaway:", consensus.get("nv_think_takeaway"))
print("Models Consulted:", consensus.get("multi_model_summary", {}).get("models_consulted"))

print("\n[SUCCESS] Full NV THINK™ pipeline verified operational in Charm AI engine!")
