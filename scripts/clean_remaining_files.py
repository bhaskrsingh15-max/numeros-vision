import os
import re

REPLACEMENTS = [
    (re.compile(r"harish\s*Vedic Tradition\s*numerology\s*books?", re.IGNORECASE), "classical vedic numerology books"),
    (re.compile(r"numerology\s*with\s*tantra,\s*ayurveda,\s*and\s*astrology\s*by\s*harish\s*Vedic Tradition", re.IGNORECASE), "classical ayurvedic numerology reference"),
    (re.compile(r"umang\s*Classical Nadi\s*numerology\s*books?", re.IGNORECASE), "classical nadi astrology books"),
    (re.compile(r"umang\s*Classical Nadi", re.IGNORECASE), "Classical Nadi Tradition"),
    (re.compile(r"Classical Nadi", re.IGNORECASE), "Classical Nadi"),
    (re.compile(r"Classical Nadi\s*verma", re.IGNORECASE), "Classical Nadi Tradition"),
    (re.compile(r"Classical Nadi", re.IGNORECASE), "Classical Nadi"),
    (re.compile(r"chaitanyaa?\s*mis?s?ra", re.IGNORECASE), "Numeros Vision Classical Methodology"),
    (re.compile(r"harish\s*Vedic Tradition", re.IGNORECASE), "Classical Vedic Tradition"),
    (re.compile(r"Vedic Tradition", re.IGNORECASE), "Vedic Tradition"),
    (re.compile(r"vijaya\s*kumar", re.IGNORECASE), "Vedic Mathematical Tradition"),
    (re.compile(r"mari\s*silva", re.IGNORECASE), "Classical Astrological Framework"),
    (re.compile(r"yoga\s*mantra", re.IGNORECASE), "Classical Chaldean Tradition"),
    (re.compile(r"louis\s*hamon", re.IGNORECASE), "Classical Chaldean Author"),
]

files_to_clean = [
    "configuration/content-registry.json",
    "configuration/search_intent_and_30day_content_plan.csv",
    "data/answerthepublic_numerology_keywords_india.csv",
    "data/knowledge_base/numeros_vision_corpus.json",
    "IMPLEMENTATION_CHANGELOG.md",
]

# Also clean scripts/
for f in os.listdir("scripts"):
    if f.endswith(".py"):
        files_to_clean.append(os.path.join("scripts", f))

cleaned = 0
for path in files_to_clean:
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                content = fp.read()
            orig = content
            for pat, rep in REPLACEMENTS:
                content = pat.sub(rep, content)
            if content != orig:
                with open(path, "w", encoding="utf-8") as fp:
                    fp.write(content)
                cleaned += 1
                print(f"Cleaned {path}")
        except Exception as e:
            print(f"Error cleaning {path}: {e}")

print(f"Done cleaning {cleaned} files.")
