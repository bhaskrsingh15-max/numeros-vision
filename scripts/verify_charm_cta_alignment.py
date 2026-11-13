import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== 1. VERIFYING ROADMAP_COMPONENTS.CSS LAUNCHER ALIGNMENT ===")
with open(r"app\static\css\roadmap_components.css", "r", encoding="utf-8") as f:
    css = f.read()

# Check desktop position
m_desk = re.search(r'\.nv-charm-bot-launcher\s*\{[^}]*bottom:\s*28px[^}]*z-index:\s*99990', css)
print("Desktop bottom: 28px, z-index: 99990:", bool(m_desk))

# Check tablet / ipad max-width 1199px position
m_tab = re.search(r'@media\s*\(max-width:\s*1199px\)[^\{]*\{.*?\.nv-charm-bot-launcher\s*\{[^}]*safe-area-inset-bottom[^}]*z-index:\s*99990', css, re.DOTALL)
print("Tablet/iPad bottom above bottom nav with safe-area:", bool(m_tab))

# Check mobile max-width 600px position
m_mob = re.search(r'@media\s*\(max-width:\s*600px\)[^\{]*\{.*?\.nv-charm-bot-launcher\s*\{[^}]*safe-area-inset-bottom[^}]*right:\s*14px', css, re.DOTALL)
print("Mobile (<=600px) bottom above bottom nav, right 14px:", bool(m_mob))

# Ensure old bottom 18px right 14px without safe-area is GONE
m_bad = re.search(r'bottom:\s*18px;\s*right:\s*14px;', css)
print("Old unaligned bottom 18px removed:", m_bad is None)

print("\n=== 2. VERIFYING INDEX.HTML CHARM WORKSPACE ALIGNMENT ===")
with open(r"app\static\index.html", "r", encoding="utf-8") as f:
    idx = f.read()

m_idx_resp = 'CHARM AI WORKSPACE RESPONSIVE ADAPTATION' in idx
print("index.html has responsive Charm AI styles:", m_idx_resp)

m_input_flex = '.chat-input-bar input' in idx and 'min-width: 0' in idx
print("index.html chat input has min-width: 0 flexbox safety:", m_input_flex)

m_pills_scroll = '.chat-suggestions' in idx and 'overflow-x: auto' in idx
print("index.html chat suggestions swipeable on mobile:", m_pills_scroll)

m_banner_class = 'class="charm-usage-banner"' in idx
print("index.html usage banner has responsive class:", m_banner_class)

print("\n=== 3. VERIFYING CHARM_AI.HTML PAGE ALIGNMENT ===")
with open(r"app\static\charm_ai.html", "r", encoding="utf-8") as f:
    cpage = f.read()

m_cpage_resp = 'CHARM AI PAGE RESPONSIVE ADAPTATION' in cpage
print("charm_ai.html has responsive page styles:", m_cpage_resp)

m_ask_btn = '.btn-ai-ask' in cpage and 'min-height: 48px' in cpage
print("charm_ai.html Ask button has 48px mobile touch target:", m_ask_btn)

m_status_row = 'class="ai-status-row"' in cpage
print("charm_ai.html status row has responsive class:", m_status_row)
