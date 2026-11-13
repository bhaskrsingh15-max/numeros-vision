import re

with open(r"app\static\tools\life-path-calculator.html", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'(<footer class="nv-footer">.*?</footer>)', text, re.DOTALL)
if m:
    print("Found footer, length:", len(m.group(1)))
    with open(r"scripts\footer_snippet.html", "w", encoding="utf-8") as f2:
        f2.write(m.group(1))
    print("Saved footer snippet.")
