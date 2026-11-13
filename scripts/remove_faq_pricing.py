import os

files = [
    'app/static/pricing.html',
    'dist_cloudflare_pages/pricing.html',
    'dist_cloudflare_pages/pricing/index.html'
]

target_snippet = "Why do prices reduce to 1, 3, 5, or 6?"

for path in files:
    if not os.path.exists(path):
        print(f"Skipping {path} (does not exist)")
        continue
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    skip = False
    removed = False

    for i, line in enumerate(lines):
        if '<div class="faq-card">' in line and i + 1 < len(lines) and target_snippet in lines[i+1]:
            skip = True
            removed = True
            continue
        if skip:
            if '</div>' in line:
                skip = False
            continue
        new_lines.append(line)

    if removed:
        with open(path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Successfully removed FAQ entry from: {path}")
    else:
        print(f"Snippet not found in: {path}")
