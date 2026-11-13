import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('function calculateHeroProfile()')
print(text[idx1+1800:idx1+3200])

print("="*40)
idx2 = text.find('function initClientComponents()')
print(text[idx2-100:idx2+1800])
