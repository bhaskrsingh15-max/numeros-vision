with open('app/static/index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
removed = False
for line in lines:
    if '/static/js/nv_profile_sync.js' in line and 'defer' in line:
        removed = True
        continue
    new_lines.append(line)

if removed:
    with open('app/static/index.html', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    print("SUCCESS: Removed duplicate defer script tag from index.html")
else:
    print("Line not found")
