import re

path = r'C:\Users\Bhaskr Singh\.gemini\antigravity\brain\c1ea3ed7-b9d2-437a-b7aa-f0cb4004681b\loshu_dual_charm_monetization_demo.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

# Remove the header-sub-tag
c = re.sub(r'<div class="header-sub-tag[^"]*">[\s\S]*?<\/div>\s*', '', c)

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)

print('Removed header-sub-tag from loshu demo.')
