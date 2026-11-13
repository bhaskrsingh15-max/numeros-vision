import os, sys
sys.stdout.reconfigure(encoding='utf-8')

count = 0
for root, dirs, files in os.walk('app'):
    # prune big or cache dirs
    dirs[:] = [d for d in dirs if d not in ('__pycache__', 'reports', 'pdf', 'logs', 'cache')]
    for f in files:
        if f.endswith(('.py', '.html', '.json', '.js', '.md', '.txt')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                modified = False
                for term in ['Vimshottari / Numerology Dasha', 'Vimshottari Numerology Dasha', 'Vishmottari Numerology Dasha', 'Vimshottari Dasha', 'Vishmottari Dasha', 'Vimshottari', 'vishmottari', 'vimshottari', 'Vishmottari']:
                    if term in content:
                        print(f"Replacing '{term}' in {p}")
                        if 'Numerology Dasha' in term:
                            content = content.replace(term, 'Numerology Dasha Timing')
                        elif term.lower() in ('vimshottari', 'vishmottari'):
                            content = content.replace(term, 'Numerology Dasha')
                        modified = True
                if modified:
                    with open(p, 'w', encoding='utf-8') as fp:
                        fp.write(content)
                    count += 1
            except Exception as e:
                print(f"Error on {p}: {e}")

print(f"Total files updated in app: {count}")
