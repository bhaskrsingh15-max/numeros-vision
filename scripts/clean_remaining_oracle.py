import os

# 1. Update sample2.html
with open('app/static/sample2.html', 'r', encoding='utf-8') as f:
    s2 = f.read()
s2 = s2.replace('href="/#ai-oracle"', 'href="/charm_ai.html"')
with open('app/static/sample2.html', 'w', encoding='utf-8') as f:
    f.write(s2)
print("sample2.html updated")

# 2. Update css comments
for css_file in ['app/static/css/roadmap_components.css', 'app/static/css/theme.css']:
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace('Charm AI Oracle', 'Charm AI').replace('AI Oracle', 'Charm AI')
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"{css_file} updated")

# 3. Update nav.js spy section
with open('app/static/js/nav.js', 'r', encoding='utf-8') as f:
    nav = f.read()
nav = nav.replace("['how-it-works', 'birth-profile', 'ai-oracle',", "['how-it-works', 'birth-profile', 'charm-ai', 'ai-oracle',")
with open('app/static/js/nav.js', 'w', encoding='utf-8') as f:
    f.write(nav)
print("nav.js updated")

# 4. Update logo-preview.html note
with open('app/static/logo-preview.html', 'r', encoding='utf-8') as f:
    lp = f.read()
lp = lp.replace('Zero "Oracle" on Frontend: Full removal of oracle terminology', 'Charm AI Uniformity: Complete standardization on Charm AI')
with open('app/static/logo-preview.html', 'w', encoding='utf-8') as f:
    f.write(lp)
print("logo-preview.html updated")

with open('app/static/logo-preview.html', 'r', encoding='utf-8') as f:
    text = f.read()
text = text.replace('Zero "Oracle" on Frontend:', 'Charm AI Standardization:')
with open('app/static/logo-preview.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated logo-preview.html directly")
