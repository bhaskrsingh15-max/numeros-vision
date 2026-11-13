import os
import re

# We want to replace the emoji spark icon in the desktop header nav with the official Charm AI logo icon
# Target pattern:
# <span style="color:#C9A227; font-size:1.05rem;">✨</span>
# Or any variant of ✨ next to Charm AI in the navbar

EMOJI_PATTERN = re.compile(
    r'<span\s+style=["\']color:#C9A227;\s*font-size:1\.05rem;["\']>[\s\S]*?</span>\s*<span\s+style=["\']font-weight:700;["\']>Charm AI</span>',
    re.IGNORECASE
)

REPLACEMENT = (
    '<img src="/logos/charm-bot-avatar.svg" alt="Charm AI" width="20" height="20" class="nv-charm-nav-icon" '
    'style="width:20px; height:20px; border-radius:50%; vertical-align:middle; display:inline-block; flex-shrink:0; box-shadow:0 2px 6px rgba(201,162,39,0.35);" /> '
    '<span style="font-weight:700;">Charm AI</span>'
)

def update_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    new_content, count = EMOJI_PATTERN.subn(REPLACEMENT, content)

    # Also check if there's any other ✨ immediately preceding Charm AI in nv-nav-charm-highlight
    if count == 0 and 'nv-nav-charm-highlight' in content:
        # Fallback regex for variations
        loose_pattern = re.compile(
            r'(<li\s+class=["\']nv-nav-item\s+nv-nav-charm-highlight["\'][\s\S]*?<a[^>]*>)[\s\S]*?(<span[^>]*>Charm AI</span>)',
            re.IGNORECASE
        )
        def loose_sub(m):
            prefix = m.group(1)
            return (
                f'{prefix}\n'
                f'              <img src="/logos/charm-bot-avatar.svg" alt="Charm AI" width="20" height="20" class="nv-charm-nav-icon" '
                f'style="width:20px; height:20px; border-radius:50%; vertical-align:middle; display:inline-block; flex-shrink:0; box-shadow:0 2px 6px rgba(201,162,39,0.35);" />\n'
                f'              <span style="font-weight:700;">Charm AI</span>'
            )
        new_content, count = loose_pattern.subn(loose_sub, content)

    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return count
    return 0

def run():
    modified = []
    for root, dirs, files in os.walk('app/static'):
        for f in files:
            if f.endswith('.html'):
                fp = os.path.join(root, f)
                c = update_file(fp)
                if c > 0:
                    modified.append((fp, c))

    print(f"Total modified HTML files: {len(modified)}")
    for fp, c in modified[:15]:
        print(f"  {fp} ({c} updates)")

if __name__ == '__main__':
    run()
