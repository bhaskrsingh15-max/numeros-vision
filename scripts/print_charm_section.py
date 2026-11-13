import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open(r"app\static\index.html", "r", encoding="utf-8") as f:
    text = f.read()

m = re.search(r'(<section[^>]*id="charm-ai"[^>]*>.*?</section>)', text, re.DOTALL)
if m:
    print("=== #charm-ai FULL SECTION ===")
    print(m.group(1))

m2 = re.search(r'([^\n]*nv-charm-bot-launcher.*?</(?:div|button|a)>)', text, re.DOTALL)
if m2:
    print("\n=== nv-charm-bot-launcher HTML ===")
    print(m2.group(1)[:1500])
