# -*- coding: utf-8 -*-
import glob
import re
import os

charm_center_nav_item = '''    <a href="/charm_ai.html" class="nv-bottom-nav-item nv-bottom-nav-center" data-nav="charm" title="Charm AI Oracle">
      <div class="nv-bottom-center-btn">
        <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.2"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/></svg>
      </div>
      <span>Charm AI</span>
    </a>'''

def update_html_bottom_nav(content: str, filename: str) -> str:
    # Check if charm is already in bottom nav
    if 'data-nav="charm"' in content and 'nv-bottom-nav-center' in content:
        return content

    # Find the nav block
    m = re.search(r'(<nav class="nv-sticky-bottom-nav"[\s\S]*?</nav>)', content)
    if not m:
        return content
    
    old_nav = m.group(1)
    
    # We want to insert the charm center item right between Calculate and Reports
    # Calculate link pattern: <a href="/calculators/"[\s\S]*?</a>
    calc_match = re.search(r'(<a\s+href="[^"]*calculators[^"]*"[\s\S]*?</a>)', old_nav)
    if calc_match:
        calc_tag = calc_match.group(1)
        # Determine if this file is charm_ai.html
        is_charm_page = "charm_ai" in filename.lower()
        center_item = charm_center_nav_item
        if is_charm_page:
            center_item = center_item.replace('class="nv-bottom-nav-item nv-bottom-nav-center"', 'class="nv-bottom-nav-item nv-bottom-nav-center active"')
            
        replacement = calc_tag + "\n" + center_item
        new_nav = old_nav.replace(calc_tag, replacement, 1)
        return content.replace(old_nav, new_nav, 1)
    
    return content

def update_hamburger_charm_link(content: str) -> str:
    # Make Charm AI prominent in hamburger menu
    # Pattern: <li class="nv-nav-item"><a href="/#charm-ai" class="nv-nav-link">Charm AI</a></li>
    # or <li class="nv-nav-item"><a href="/charm_ai.html" ...
    old_pats = [
        r'<li class="nv-nav-item"><a href="/#charm-ai" class="nv-nav-link">Charm AI</a></li>',
        r'<li class="nv-nav-item"><a href="/#charm-ai" class="nv-nav-link active">Charm AI</a></li>',
        r'<li class="nv-nav-item"><a href="/charm_ai\.html" class="nv-nav-link">Charm AI</a></li>',
        r'<li class="nv-nav-item"><a href="/charm_ai\.html" class="nv-nav-link active">Charm AI</a></li>',
        r'<li class="nv-nav-item"><a href="/charm/" class="nv-nav-link">Charm AI</a></li>'
    ]
    
    replacement = '''<li class="nv-nav-item nv-nav-charm-highlight">
            <a href="/charm_ai.html" class="nv-nav-link" title="Charm AI Consultation Oracle" style="display:inline-flex; align-items:center; gap:8px;">
              <span style="color:#C9A227; font-size:1.05rem;">✨</span>
              <span style="font-weight:700;">Charm AI</span>
              <span class="nv-charm-tag" style="background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFDF7; font-size:0.62rem; font-weight:700; padding:2px 7px; border-radius:999px; letter-spacing:0.04em;">AI ORACLE</span>
            </a>
          </li>'''
    
    for pat in old_pats:
        if re.search(pat, content):
            return re.sub(pat, replacement, content, count=1)
    
    return content

files = glob.glob('app/static/*.html')
updated_bottom = 0
updated_drawer = 0

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        orig = fp.read()
    
    new_c = update_html_bottom_nav(orig, f)
    if new_c != orig:
        updated_bottom += 1
        
    final_c = update_hamburger_charm_link(new_c)
    if final_c != new_c:
        updated_drawer += 1
        
    if final_c != orig:
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(final_c)

print(f"Updated bottom nav in {updated_bottom} files.")
print(f"Updated hamburger menu in {updated_drawer} files.")
