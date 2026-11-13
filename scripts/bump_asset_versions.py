import os
import re

def bump_versions(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original = content

    # Bump roadmap_components.css
    content = re.sub(
        r'roadmap_components\.css\?v=[0-9.]+',
        'roadmap_components.css?v=5.2.0',
        content
    )
    # If unversioned
    content = re.sub(
        r'roadmap_components\.css(?!\?)',
        'roadmap_components.css?v=5.2.0',
        content
    )

    # Bump theme.css
    content = re.sub(
        r'theme\.css\?v=[0-9.]+',
        'theme.css?v=5.2.0',
        content
    )

    # Bump nav.js
    content = re.sub(
        r'nav\.js\?v=[0-9.]+',
        'nav.js?v=5.2.0',
        content
    )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run():
    modified = 0
    for root, dirs, files in os.walk('app'):
        for f in files:
            if f.endswith('.html'):
                fp = os.path.join(root, f)
                if bump_versions(fp):
                    modified += 1
    print(f"Total HTML files with asset version bumped to 5.2.0: {modified}")

if __name__ == '__main__':
    run()
