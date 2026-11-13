import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/pricing.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Remove artificial strike prices in JS plans
text = re.sub(r"strike:\s*'[₹\d,]+',\s*", "", text)
# Remove fake strike span tags
text = re.sub(r'\s*<span[^>]*style="[^"]*line-through[^"]*"[^>]*>₹[\d,]+</span>', '', text)
text = re.sub(r'<td style="[^"]*line-through[^"]*">₹[\d,]+</td>', '<td style="padding:14px 16px; color:#7A654D;">One-Time</td>', text)

with open('app/static/pricing.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Cleaned up artificial strike prices in pricing.html!")
