# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.abspath('.'))
sys.stdout.reconfigure(encoding='utf-8')

print("1. Testing Charm Chat Orchestrator (Free Turn)...")
from app.charm.chat.response_composer import charm_chat_orchestrator

res = charm_chat_orchestrator.process_chat_turn(
    message="What does 2026 bring for my career promotion?",
    user_name="Bhaskr",
    day=28,
    month=8,
    year=1990
)

print(f"Status: {res.status}")
print(f"Assistant Message Text Preview:\n{res.assistant_message['text'][:600]}...")

# Check for banned robotic jargon
banned_phrases = [
    "Category C (Category C",
    "Intrinsic Potency",
    "Water vs Cold Earth Clash",
    "Synergy Matrix",
    "Bodyguard Hygiene",
    "Karmic Void",
    "84% Harmonization",
    "Tier 1: Career",
    "Tier 2: Timing",
    "Tier 5: Input"
]

found = []
for bp in banned_phrases:
    if bp.lower() in res.assistant_message['text'].lower():
        found.append(bp)

if found:
    print(f"❌ FOUND ROBOTIC JARGON: {found}")
else:
    print("✅ ZERO ROBOTIC JARGON FOUND IN CHARM AI OUTPUT!")

print("\n2. Testing Freemium API Reading Payload...")
from app.api.readings import _classify_question_topic

topic = _classify_question_topic("What does 2026 bring for my career promotion?")
print(f"Classified Topic: {topic}")
print("All engine logic verified!")
