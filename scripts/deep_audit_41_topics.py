import os
import sys
import json
import re
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
BASE_DIR = Path(__file__).resolve().parent.parent

# Read professional numerology rules
rules_path = BASE_DIR / "data" / "knowledge_base" / "professional_numerology_rules.json"
with open(rules_path, "r", encoding="utf-8") as f:
    kb_data = json.load(f)

kb_topics = {}
for t in kb_data.get("topics", []):
    tid = t.get("topic_id")
    title = t.get("title", "")
    if tid == 34 and "Health" in title:
        kb_topics["34b"] = t
    else:
        kb_topics[str(tid)] = t

# Read all python engines
engine_dir = BASE_DIR / "app" / "engine"
engine_texts = {}
for py_file in engine_dir.glob("*.py"):
    with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
        engine_texts[py_file.name] = f.read()

# Read all test files
tests_dir = BASE_DIR / "tests"
test_texts = {}
for py_file in tests_dir.glob("*.py"):
    with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
        test_texts[py_file.name] = f.read()

# Read API routers
api_dir = BASE_DIR / "app" / "api"
api_texts = {}
for py_file in api_dir.glob("*.py"):
    with open(py_file, "r", encoding="utf-8", errors="ignore") as f:
        api_texts[py_file.name] = f.read()

# Read static HTML pages
static_dir = BASE_DIR / "app" / "static"
html_files = [f.name for f in static_dir.glob("*.html")]

# Map topics from slide
slide_topics = [
    ("1", "Introduction to Professional Numbers Rules, Friendly, Neutral, Unfriendly Nos., Input / Output"),
    ("2", "Mobile Numerology"),
    ("3", "Pillars"),
    ("4", "Car & House Numerology"),
    ("5", "81 Types of Driver & Conductor"),
    ("6", "What Numbers 1-9 Signifies"),
    ("7", "Impact of Repetitive Numbers (Nos 1-9)"),
    ("8", "Impact of Missing Numbers"),
    ("9", "Complementary Nos & Master Key Number"),
    ("10", "Element Balancing"),
    ("11", "Favorable & Unfavorable Directions"),
    ("12", "Family Compatibility using Loshu Grid"),
    ("13", "Master Numbers"),
    ("14", "Karmic Numbers"),
    ("15", "Maha Dasha Prediction - Future Trends - Personal Year, Personal Month, Personal Day Prediction"),
    ("16", "Universal Year Prediction"),
    ("17", "Prediction without DOB calculation"),
    ("18", "Personal Year Predictions 1 to 9"),
    ("19", "Analysis of PY, PM, PD with DOB"),
    ("20", "Blood Remedies"),
    ("21", "Planet Balancing Selection"),
    ("22", "Planet Balancing 1-9 Remedies"),
    ("23", "Yantras for Numerology"),
    ("24", "Problem based remedies"),
    ("25", "When to Start Remedies & Process"),
    ("26", "Bonus Queries: Child Conceive, Male/Female Birth, Autism Cases, Compatibility Challenges, Temporary/Permanent Relationship, Door Remedies, Silver Square"),
    ("27", "Choosing the Right Profession"),
    ("28", "Marriage & Business Compatibility"),
    ("29", "Love & Arrange Marriage"),
    ("30", "Foreign Settlement"),
    ("31", "Name Balancing - Regional Name Balancing Part 1"),
    ("32", "Name Balancing - Company & Products Part 2"),
    ("33", "Name Balancing - Letter Section Part 3"),
    ("34", "Implementing Balanced Name"),
    ("35", "Share Market Investment & Business"),
    ("34b", "Health & Healing"),
    ("36", "Numero-Vastu Directions for Success as per Vastu"),
    ("37", "Yantra according to Numerology - Remedies - Part 4"),
    ("38", "Yantra Making"),
    ("39", "Prediction by Pyramid Method / Hora Prediction"),
    ("40", "Signature"),
    ("41", "Important Points related to reading / Consultation"),
]

print(f"Total Slide Topics: {len(slide_topics)}")

results = []
for tid, title in slide_topics:
    in_kb = tid in kb_topics
    kb_obj = kb_topics.get(tid, {})
    kb_title = kb_obj.get("title", "") if in_kb else "NOT IN KB"
    
    # Check engines
    matched_engines = []
    for ename, etext in engine_texts.items():
        # Look for topic mentions or specific keywords
        if f"Topic {tid}" in etext or f"topic_{tid}" in etext:
            matched_engines.append(ename)
            
    # Check tests
    matched_tests = []
    for tname, ttext in test_texts.items():
        if f"Topic {tid}" in ttext or f"topic_{tid}" in ttext:
            matched_tests.append(tname)

    results.append({
        "topic_id": tid,
        "slide_title": title,
        "in_kb": in_kb,
        "kb_title": kb_title,
        "matched_engines": matched_engines,
        "matched_tests": matched_tests
    })

print(json.dumps(results[:15], indent=2))
