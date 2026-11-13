import os
import re

# 1. Desktop Nav Icon: replace <img> or ✨ with inline .nv-charm-medallion-icon
DESKTOP_ICON_SVG = (
    '<span class="nv-charm-medallion-icon" aria-hidden="true">'
    '<svg viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="#FFFFFF" stroke-width="2.4" style="display:block;">'
    '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/>'
    '</svg>'
    '</span>'
)

# 2. Scroll Floating Launcher in index.html: replace <img> with inline SVG
SCROLL_LAUNCHER_SVG = (
    '<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#FFFFFF" stroke-width="2.2" style="display:block;">'
    '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/>'
    '</svg>'
)

# 3. Chat Avatar SVG:
CHAT_AVATAR_SVG = (
    '<div class="ai-avatar-wrap">'
    '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#FFFFFF" stroke-width="2.2" style="display:block;">'
    '<path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/>'
    '</svg>'
    '</div>'
)

def update_html_file(fp):
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original = content

    # Replace <img src="/logos/charm-bot-avatar.svg" ... /> in nav link
    content = re.sub(
        r'<img\s+src=["\']/logos/charm-bot-avatar\.svg["\'][^>]*class=["\']nv-charm-nav-icon["\'][^>]*>',
        DESKTOP_ICON_SVG,
        content
    )

    # In case any file still had emoji
    content = re.sub(
        r'<span\s+style=["\']color:#C9A227;\s*font-size:1\.05rem;["\']>[\s\S]*?</span>\s*(<span\s+style=["\']font-weight:700;["\']>Charm AI</span>)',
        rf'{DESKTOP_ICON_SVG} \1',
        content
    )

    # If this is index.html, update the scroll launcher trigger
    if 'index.html' in fp:
        content = re.sub(
            r'<img\s+src=["\']/logos/charm-bot-avatar\.svg["\']\s+alt=["\']Ask Charm AI["\'][^>]*>',
            SCROLL_LAUNCHER_SVG,
            content
        )

    # Update chat avatars in charm_ai.html & index.html
    if 'charm_ai.html' in fp or 'index.html' in fp:
        content = re.sub(
            r'<div\s+class=["\']ai-avatar-wrap["\']>\s*<img\s+src=["\']/logos/charm-bot-avatar\.svg["\'][^>]*>\s*</div>',
            CHAT_AVATAR_SVG,
            content
        )

    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run():
    count = 0
    for root, dirs, files in os.walk('app'):
        for f in files:
            if f.endswith('.html'):
                fp = os.path.join(root, f)
                if update_html_file(fp):
                    count += 1
    print(f"Total HTML files updated with unified inline Charm AI logo: {count}")

if __name__ == '__main__':
    run()
