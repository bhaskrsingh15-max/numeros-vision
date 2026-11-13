import os
import re
import json

# Define exact replacements for codebase and documentation
# Mapping tuple: (compiled_regex, replacement_string)

REPLACEMENTS = [
    # Dr. Numeros Vision Classical Methodology variants
    (re.compile(r"Dr\.\s*Chaitanyaa?\s*Mis?s?ra('s)?", re.IGNORECASE), "Numeros Vision Classical Methodology"),
    (re.compile(r"Chaitanyaa?\s*Mis?s?ra('s)?", re.IGNORECASE), "Numeros Vision Classical Methodology"),
    (re.compile(r"Dr\.\s*Misra('s)?\s*taxonomy", re.IGNORECASE), "our classical taxonomy"),
    (re.compile(r"Dr\.\s*Misra\s*highlights", re.IGNORECASE), "Numeros Vision analysis highlights"),
    (re.compile(r"Dr\.\s*Misra\s*warns", re.IGNORECASE), "Classical analysis cautions"),
    (re.compile(r"Dr\.\s*Misra\s*notes", re.IGNORECASE), "Classical analysis notes"),
    (re.compile(r"Dr\.\s*Misra\s*explicitly\s*states", re.IGNORECASE), "Classical analysis emphasizes"),
    (re.compile(r"Dr\.\s*Misra", re.IGNORECASE), "Numeros Vision"),
    (re.compile(r"SRC-DR-CHAITANYAA-MISRA-DAY6-DAY7-LECTURE", re.IGNORECASE), "SRC-NV-CLASSICAL-ARCHIVE"),
    (re.compile(r"Day 6 Numeros Vision Canon \(Dr\. Numeros Vision Classical Methodology\)", re.IGNORECASE), "Day 6 Numeros Vision Canon (Numeros Vision)"),

    # Classical Nadi Tradition variants
    (re.compile(r"Umang\s*Classical Nadi('s)?", re.IGNORECASE), "Numeros Vision Classical Archive"),
    (re.compile(r"Classical Nadi_2013_METHODOLOGY", re.IGNORECASE), "NV_NADI_PREDICTIVE_METHODOLOGY"),
    (re.compile(r"Classical Nadi\s*2013\s*ed\.", re.IGNORECASE), "Classical Nadi Methodology"),
    (re.compile(r"Classical Nadi", re.IGNORECASE), "Classical Nadi"),

    # Classical Nadi Tradition / Kpastrologer variants
    (re.compile(r"Classical Nadi\s*Verma", re.IGNORECASE), "Numeros Vision Classical Archive"),
    (re.compile(r"VERMA_NADI_COMBINATIONS", re.IGNORECASE), "NV_NADI_COMBINATIONS"),
    (re.compile(r"www\.Kpastrologer\s*\.co\.in", re.IGNORECASE), ""),
    (re.compile(r"Kpastrologer", re.IGNORECASE), "Classical Nadi Archive"),
    (re.compile(r"Instagram,\s*Youtube-\s*Classical NadiAstrology", re.IGNORECASE), ""),
    (re.compile(r"Classical NadiAstrology", re.IGNORECASE), ""),

    # Classical Vedic Tradition / Vedic Mathematical Tradition / Classical Astrological Framework / Classical Chaldean Tradition
    (re.compile(r"Harish\s*Vedic Tradition('s)?", re.IGNORECASE), "Classical Vedic Tradition"),
    (re.compile(r"Vijaya\s*Kumar('s)?", re.IGNORECASE), "Vedic Mathematical Tradition"),
    (re.compile(r"Mari\s*Silva('s)?", re.IGNORECASE), "Classical Astrological Framework"),
    (re.compile(r"Yoga\s*Mantra", re.IGNORECASE), "Classical Chaldean Tradition"),
]

# Active directories to sanitize
TARGET_DIRS = [
    "app",
    "data/knowledge_base",
    "docs",
    "knowledge",
    "dist_cloudflare_pages",
    "tests"
]

total_replacements = 0
modified_files = []

for td in TARGET_DIRS:
    for root, dirs, files in os.walk(td):
        for f in files:
            if f.endswith((".py", ".html", ".js", ".json", ".md", ".csv", ".yaml", ".yml")):
                # Skip binary-like or backup files
                if "bak" in f.lower() or "version_copy" in root:
                    continue
                path = os.path.join(root, f)
                try:
                    with open(path, "r", encoding="utf-8", errors="ignore") as fp:
                        content = fp.read()
                    
                    orig_content = content
                    for pattern, repl in REPLACEMENTS:
                        content = pattern.sub(repl, content)
                    
                    if content != orig_content:
                        with open(path, "w", encoding="utf-8") as fp:
                            fp.write(content)
                        modified_files.append(path)
                        total_replacements += 1
                except Exception as e:
                    print(f"Error processing {path}: {e}")

print(f"Sanitization complete! Modified {len(modified_files)} active files.")
for mf in modified_files[:20]:
    print(f"  - {mf}")
if len(modified_files) > 20:
    print(f"  ... and {len(modified_files)-20} more files.")
