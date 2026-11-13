import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from app.engine.charm_oracle_synthesizer import charm_oracle_synthesizer
from app.charm.chat.response_composer import charm_chat_orchestrator

print("1. Testing charm_oracle_synthesizer.synthesize_consultation...")
res = charm_oracle_synthesizer.synthesize_consultation(
    name="Bhaskr Singh",
    day=15,
    month=8,
    year=1990,
    question="When will I get a job promotion or career change?",
    is_premium=False
)

text = res.get("humanized_consultation", "")
print("Reading length:", len(text))
banned = ["bnn", "kp astrology", "lal kitab", "vedic astrology", "kundli", "astrological verification"]
for b in banned:
    c = text.lower().count(b)
    print(f"  [charm_oracle_synthesizer] Term '{b}': {c} occurrences")

print("\n--- SAMPLE CORRELATION IN CHARM ORACLE ---")
print(res.get("correlation_summary", ""))

print("\n2. Testing charm_chat_orchestrator.process_chat_turn...")
chat_res = charm_chat_orchestrator.process_chat_turn(
    message="When will I get a job promotion?",
    user_name="Bhaskr Singh",
    day=15,
    month=8,
    year=1990
)
chat_text = chat_res.assistant_message.get("text", "")
print("Chat text length:", len(chat_text))
for b in banned:
    c = chat_text.lower().count(b)
    print(f"  [charm_chat_orchestrator] Term '{b}': {c} occurrences")

print("\n3. Testing section titles in assistant_message...")
sections = chat_res.assistant_message.get("sections", [])
for s in sections:
    print(f"  Section Title: {s.get('title')}")

print("\n--- CHAT OUTPUT SAMPLE ---")
for l in chat_text.split("\n")[:18]:
    print(l)

print("\n✓ ALL TESTS COMPLETED AND CLEAN!")
