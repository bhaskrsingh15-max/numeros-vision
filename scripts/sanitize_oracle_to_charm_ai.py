import os
import re

def sanitize_file(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original = content

    # 1. Remove the AI ORACLE badge from desktop nav link
    # Pattern: <span class="nv-charm-tag"[^>]*>AI ORACLE</span>
    content = re.sub(
        r'\s*<span\s+class=["\']nv-charm-tag["\'][^>]*>AI ORACLE</span>',
        '',
        content,
        flags=re.IGNORECASE
    )

    # 2. Update title in desktop nav link
    content = re.sub(
        r'title=["\']Charm AI Consultation Oracle["\']',
        'title="Charm AI"',
        content,
        flags=re.IGNORECASE
    )

    # 3. Update bottom nav title
    content = re.sub(
        r'title=["\']Charm AI Oracle["\']',
        'title="Charm AI"',
        content,
        flags=re.IGNORECASE
    )

    # 4. Update author span in chat UI
    content = re.sub(
        r'<span\s+class=["\']ai-author-name["\']>Charm AI Oracle</span>',
        '<span class="ai-author-name">Charm AI</span>',
        content,
        flags=re.IGNORECASE
    )

    # 5. Update avatar alt text
    content = re.sub(
        r'alt=["\']Charm AI Oracle["\']',
        'alt="Charm AI"',
        content,
        flags=re.IGNORECASE
    )

    # 6. Specific text in index.html & sample2.html
    content = re.sub(
        r'<div id=["\']ai-oracle["\']><a href=["\']#ai-oracle["\'] style=["\']display:none;["\'] aria-hidden=["\']true["\']>AI Oracle</a></div>',
        '<div id="ai-oracle"><a href="#ai-oracle" style="display:none;" aria-hidden="true">Charm AI</a></div>',
        content,
        flags=re.IGNORECASE
    )
    content = re.sub(
        r'<span class=["\']cg-dropdown-title["\']>AI Kundli Oracle</span>',
        '<span class="cg-dropdown-title">Charm AI</span>',
        content,
        flags=re.IGNORECASE
    )

    # 7. JS / JSON / Python naming
    content = re.sub(
        r'name:\s*[\'"]Charm AI Oracle[\'"]',
        "name: 'Charm AI'",
        content
    )
    content = re.sub(
        r'"name":\s*"Charm AI Oracle"',
        '"name": "Charm AI"',
        content
    )
    content = re.sub(
        r'"tool_display_name":\s*"Charm AI Oracle"',
        '"tool_display_name": "Charm AI"',
        content
    )
    content = re.sub(
        r'"purpose":\s*"Experience conversational oracle intelligence with one free inquiry\."',
        '"purpose": "Experience conversational Charm AI intelligence with one free inquiry."',
        content
    )
    content = re.sub(
        r'Deterministic Oracle Standards',
        'Grounded Charm AI Standards',
        content
    )

    if content != original:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def run():
    modified_files = []
    target_dirs = ['app']
    for t_dir in target_dirs:
        for root, dirs, files in os.walk(t_dir):
            for file in files:
                if file.endswith(('.html', '.js', '.py', '.json', '.css')):
                    fp = os.path.join(root, file)
                    if sanitize_file(fp):
                        modified_files.append(fp)

    print(f"Sanitization complete. Total modified files: {len(modified_files)}")
    for mf in modified_files[:25]:
        print("  Modified:", mf)
    if len(modified_files) > 25:
        print(f"  ... and {len(modified_files) - 25} more files.")

if __name__ == '__main__':
    run()
