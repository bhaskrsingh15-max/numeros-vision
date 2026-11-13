with open('app/static/css/theme.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'charm-tab-sign' in line:
        for j in range(max(0, i-5), min(len(lines), i+30)):
            print(f'{j+1}: {lines[j].rstrip()}')
        break
