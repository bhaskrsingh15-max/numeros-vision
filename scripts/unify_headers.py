import os
import glob
import re

def main():
    files = glob.glob('app/static/**/*.html', recursive=True)
    print(f"Scanning {len(files)} files...")

    # Pattern for stray About at the end of nav menu
    # Matches:
    # <!-- 7. About -->
    # <li class="nv-nav-item"><a href="/about/" class="nv-nav-link">About</a></li>
    # (with variations of whitespace)
    
    stray_about_pattern = re.compile(
        r'\s*<!--\s*7\.\s*About\s*-->\s*<li\s+class=["\']nv-nav-item["\']>\s*<a\s+href=["\']/about/["\']\s+class=["\']nv-nav-link["\']>About</a>\s*</li>',
        re.MULTILINE
    )

    # In case there is no comment:
    # <li class="nv-nav-item"><a href="/about/" class="nv-nav-link">About</a></li> right after Contact Us
    stray_about_pattern2 = re.compile(
        r'(<li\s+class=["\']nv-nav-item["\']>\s*<a\s+href=["\']/contact/["\'][^>]*>Contact Us</a>\s*</li>)\s*(<!--[^>]*-->)?\s*<li\s+class=["\']nv-nav-item["\']>\s*<a\s+href=["\']/about/["\'][^>]*>About</a>\s*</li>',
        re.MULTILINE
    )

    # Standard PWA Drawer Item HTML to ensure mobile/tablet menu parity
    pwa_drawer_item = """
          <!-- 7. PWA Download / Install App on Mobile & Tablet ONLY -->
          <li class="nv-nav-item nv-pwa-menu-item" id="nvPwaDrawerItem" style="display:none; margin: 8px 0; width: 100%; box-sizing: border-box;">
            <button type="button" class="nv-nav-link nv-pwa-install-trigger-btn" onclick="triggerPwaInstall(event)" style="background: rgba(201,162,39,0.12); border: 1.5px solid rgba(201,162,39,0.38); border-radius: 999px; padding: 10px 18px; font-weight: 600; color: #8B6914; display: flex; align-items: center; justify-content: space-between; width: 100%; cursor: pointer; text-align: left; box-sizing: border-box;">
              <span style="display: flex; align-items: center; gap: 8px;">
                <span class="nv-sub-icon" style="font-size: 1.15rem;">📲</span>
                <span>Install / Download App</span>
              </span>
              <span class="nv-sub-tag" style="background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color: #fff; font-size: 0.65rem; padding: 2px 7px; border-radius: 6px; font-weight: 700; text-transform: uppercase;">PWA</span>
            </button>
          </li>"""

    updated_count = 0
    pwa_added_count = 0

    for file_path in files:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        orig = content
        
        # 1. Remove stray about at end of nav
        if stray_about_pattern.search(content):
            content = stray_about_pattern.sub('', content)
        elif stray_about_pattern2.search(content):
            content = stray_about_pattern2.sub(r'\1', content)

        # 2. If nvPwaDrawerItem is missing in nvNavMenu, add it before </ul>
        if 'id="nvNavMenu"' in content and 'id="nvPwaDrawerItem"' not in content:
            # Insert before the closing </ul> of nvNavMenu
            nav_match = re.search(r'(<ul[^>]*id=["\']nvNavMenu["\'][\s\S]*?)(</ul>)', content)
            if nav_match:
                prefix = nav_match.group(1).rstrip()
                suffix = nav_match.group(2)
                # replace only this instance
                content = content[:nav_match.start()] + prefix + pwa_drawer_item + '\n        ' + suffix + content[nav_match.end():]
                pwa_added_count += 1

        if content != orig:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            updated_count += 1

    print(f"Updated {updated_count} files (PWA drawer added to {pwa_added_count} files).")

if __name__ == '__main__':
    main()
