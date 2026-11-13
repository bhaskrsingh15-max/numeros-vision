import json
import re

with open('app/static/pricing.html', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
with open('pricing_extracted_table.txt', 'w', encoding='utf-8') as out:
    for i, l in enumerate(lines[790:940], 791):
        out.write(f"{i}: {l}\n")

print("Wrote lines 791-940 to pricing_extracted_table.txt")
