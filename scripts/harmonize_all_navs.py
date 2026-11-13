import glob
import re

def harmonize_navs():
    # 1. Read canonical nav from index.html
    with open('app/static/index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()

    m = re.search(r'(<nav aria-label=["\']Main Navigation["\']>[\s\S]*?</nav>)', index_content)
    if not m:
        print("ERROR: Could not find canonical nav in index.html")
        return
    canonical_nav = m.group(1)

    files = glob.glob('app/static/**/*.html', recursive=True)
    print(f"Harmonizing nav across {len(files)} files...")

    updated = 0
    for file_path in files:
        if file_path.replace('\\', '/') == 'app/static/index.html':
            continue

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find any <nav> containing nvNavMenu
        nav_match = re.search(r'<nav\b[^>]*>[\s\S]*?<ul[^>]*id=["\']nvNavMenu["\'][\s\S]*?</ul>[\s\S]*?</nav>', content)
        if nav_match:
            old_nav = nav_match.group(0)
            if old_nav != canonical_nav:
                content = content[:nav_match.start()] + canonical_nav + content[nav_match.end():]
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                updated += 1
        else:
            print(f"Skipping (no nvNavMenu nav): {file_path}")

    print(f"Successfully harmonized nav in {updated} files.")

if __name__ == '__main__':
    harmonize_navs()
