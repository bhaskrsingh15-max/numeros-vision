with open('app/templates/master_header.html', 'r', encoding='utf-8') as f:
    text = f.read()

target = '<li class="nv-nav-item"><a href="/#charm-ai" class="nv-nav-link">Charm AI</a></li>'
replacement = '''<li class="nv-nav-item nv-nav-charm-highlight">
            <a href="/charm_ai.html" class="nv-nav-link" title="Charm AI" style="display:inline-flex; align-items:center; gap:8px;">
              <img src="/logos/charm-bot-avatar.svg" alt="Charm AI" width="20" height="20" class="nv-charm-nav-icon" style="width:20px; height:20px; border-radius:50%; vertical-align:middle; display:inline-block; flex-shrink:0; box-shadow:0 2px 6px rgba(201,162,39,0.35);" />
              <span style="font-weight:700;">Charm AI</span>
            </a>
          </li>'''

text = text.replace(target, replacement)
with open('app/templates/master_header.html', 'w', encoding='utf-8') as f:
    f.write(text)
print("Updated master_header.html")
