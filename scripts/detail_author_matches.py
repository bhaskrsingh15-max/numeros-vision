import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")

author_patterns = [
    r"chaitanyaa?\s+mis?s?ra",
    r"umang\s+Classical Nadi",
    r"Classical Nadi",
    r"Classical Nadi\s+verma",
    r"harish\s+Vedic Tradition",
    r"vijaya\s+kumar",
    r"mari\s+silva",
    r"yoga\s+mantra"
]

combined = re.compile("|".join(author_patterns), re.IGNORECASE)

active_dirs = ["app", "data/knowledge_base", "docs", "knowledge", "configuration", "tests"]

matching_files = {}

for ad in active_dirs:
    for root, dirs, files in os.walk(ad):
        for f in files:
            if f.endswith((".py", ".html", ".js", ".json", ".md", ".csv", ".yaml", ".yml")):
                p = os.path.join(root, f)
                try:
                    with open(p, "r", encoding="utf-8", errors="ignore") as fp:
                        lines = fp.readlines()
                    hits = []
                    for lno, l in enumerate(lines, 1):
                        if combined.search(l):
                            hits.append((lno, l.strip()[:100]))
                    if hits:
                        matching_files[p] = hits
                except Exception as e:
                    pass

print(f"Total matching active files: {len(matching_files)}")
for p, hits in sorted(matching_files.items()):
    print(f"\n--- {p} ({len(hits)} matches) ---")
    for lno, snippet in hits[:5]:
        print(f"  Line {lno}: {snippet}")
    if len(hits) > 5:
        print(f"  ... and {len(hits)-5} more matches")
