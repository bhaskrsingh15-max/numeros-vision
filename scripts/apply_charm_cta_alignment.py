import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. UPDATE roadmap_components.css
css_path = r"app\static\css\roadmap_components.css"
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace Block 1 (around line 810)
old_block1 = """.nv-charm-bot-launcher {
    bottom: calc(70px + 16px) !important;
  }"""

new_block1 = """.nv-charm-bot-launcher {
    bottom: calc(64px + env(safe-area-inset-bottom, 0px) + 16px) !important;
    right: 20px !important;
    z-index: 99990 !important;
  }"""

if old_block1 in css:
    css = css.replace(old_block1, new_block1, 1)
    print("Updated Block 1 in roadmap_components.css")
else:
    print("WARNING: Block 1 not found directly in roadmap_components.css")

# Replace Block 2 (base definition)
old_block2 = """.nv-charm-bot-launcher {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 990;"""

new_block2 = """.nv-charm-bot-launcher {
  position: fixed;
  bottom: 28px;
  right: 28px;
  z-index: 99990;"""

if old_block2 in css:
    css = css.replace(old_block2, new_block2, 1)
    print("Updated Block 2 in roadmap_components.css")
else:
    print("WARNING: Block 2 not found directly in roadmap_components.css")

# Replace Block 3 (mobile definition)
old_block3 = """/* Mobile Responsiveness */
@media (max-width: 600px) {
  .nv-charm-bot-launcher {
    bottom: 18px;
    right: 14px;
  }
  .nv-charm-bot-avatar-btn {
    width: 50px;
    height: 50px;
    border-radius: 16px;
  }
  .nv-charm-bot-close {
    width: 20px;
    height: 20px;
    font-size: 1rem;
    top: -4px;
    right: -4px;
  }
  .nv-charm-bot-tooltip {
    display: none; /* Hide hover tooltip on touch devices */
  }
}"""

new_block3 = """/* Mobile Responsiveness for Charm AI Launcher */
@media (max-width: 600px) {
  .nv-charm-bot-launcher {
    bottom: calc(64px + env(safe-area-inset-bottom, 0px) + 14px) !important;
    right: 14px !important;
    z-index: 99990 !important;
  }
  .nv-charm-bot-avatar-btn {
    width: 52px;
    height: 52px;
    border-radius: 16px;
  }
  .nv-charm-bot-close {
    width: 22px;
    height: 22px;
    font-size: 1.05rem;
    top: -5px;
    right: -5px;
  }
  .nv-charm-bot-tooltip {
    display: none !important; /* Hide hover tooltip on touch devices */
  }
}"""

if old_block3.replace("\r\n", "\n") in css.replace("\r\n", "\n"):
    css = css.replace("\r\n", "\n").replace(old_block3.replace("\r\n", "\n"), new_block3.replace("\r\n", "\n"))
    print("Updated Block 3 in roadmap_components.css")
else:
    print("WARNING: Block 3 not found directly in roadmap_components.css")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# 2. UPDATE index.html
index_path = r"app\static\index.html"
with open(index_path, 'r', encoding='utf-8') as f:
    idx = f.read()

# Add charm-usage-banner class to usage notice div
old_usage_div = '<div style="margin-top:14px; padding:10px 16px; background:rgba(201,162,39,0.06); border:1px solid rgba(201,162,39,0.22); border-radius:10px; font-size:0.80rem; color:#7A654D; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">'
new_usage_div = '<div class="charm-usage-banner" style="margin-top:14px; padding:10px 16px; background:rgba(201,162,39,0.06); border:1px solid rgba(201,162,39,0.22); border-radius:10px; font-size:0.80rem; color:#7A654D; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">'

if old_usage_div in idx:
    idx = idx.replace(old_usage_div, new_usage_div, 1)
    print("Added class charm-usage-banner to index.html")

# Add responsive CSS block to index.html
charm_responsive_css = """
    /* ── CHARM AI WORKSPACE RESPONSIVE ADAPTATION (ALL SCREENS & MOBILE) ── */
    @media (max-width: 768px) {
      .charm-ai-card {
        padding: 20px 14px !important;
        border-radius: 18px !important;
        margin: 0 auto;
        box-sizing: border-box;
      }
      .chat-box-window {
        height: 280px !important;
        padding: 14px !important;
        margin-bottom: 14px !important;
        border-radius: 14px !important;
      }
      .msg-bubble {
        max-width: 95% !important;
        padding: 12px 14px !important;
        font-size: 0.88rem !important;
      }
      .chat-suggestions {
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        gap: 6px !important;
        padding: 2px 2px 10px !important;
        margin-bottom: 12px !important;
        scrollbar-width: none !important;
      }
      .chat-suggestions::-webkit-scrollbar {
        display: none !important;
      }
      .chat-pill {
        white-space: nowrap !important;
        flex-shrink: 0 !important;
        padding: 6px 12px !important;
        font-size: 0.74rem !important;
      }
      .chat-input-bar {
        display: flex !important;
        align-items: center !important;
        gap: 8px !important;
        width: 100% !important;
        box-sizing: border-box !important;
      }
      .chat-input-bar input {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        padding: 12px 14px !important;
        font-size: 0.88rem !important;
        border-radius: 999px !important;
        box-sizing: border-box !important;
      }
      .chat-voice-btn {
        width: 42px !important;
        height: 42px !important;
        min-width: 42px !important;
        min-height: 42px !important;
        font-size: 1.1rem !important;
        flex-shrink: 0 !important;
        padding: 0 !important;
      }
      .chat-input-bar .btn-primary-gold,
      .chat-input-bar button.btn-primary-gold {
        padding: 12px 18px !important;
        font-size: 0.86rem !important;
        letter-spacing: 0.02em !important;
        white-space: nowrap !important;
        flex-shrink: 0 !important;
        min-width: 80px !important;
        justify-content: center !important;
        box-sizing: border-box !important;
      }
      .charm-usage-banner {
        flex-direction: column !important;
        align-items: flex-start !important;
        text-align: left !important;
        gap: 8px !important;
        padding: 10px 14px !important;
      }
      .charm-usage-banner a {
        display: inline-block !important;
        padding: 4px 0 !important;
      }
    }

    @media (max-width: 420px) {
      .chat-input-bar {
        gap: 6px !important;
      }
      .chat-input-bar input {
        padding: 10px 12px !important;
        font-size: 0.84rem !important;
      }
      .chat-input-bar .btn-primary-gold,
      .chat-input-bar button.btn-primary-gold {
        padding: 10px 14px !important;
        font-size: 0.80rem !important;
        min-width: 72px !important;
      }
      .chat-voice-btn {
        width: 38px !important;
        height: 38px !important;
        min-width: 38px !important;
        min-height: 38px !important;
      }
    }
"""

if 'CHARM AI WORKSPACE RESPONSIVE ADAPTATION' not in idx:
    idx = idx.replace('</style>', charm_responsive_css + '\n  </style>', 1)
    print("Added responsive Charm AI CSS to index.html")

with open(index_path, 'w', encoding='utf-8') as f:
    f.write(idx)

# 3. UPDATE charm_ai.html
charm_page_path = r"app\static\charm_ai.html"
with open(charm_page_path, 'r', encoding='utf-8') as f:
    cpage = f.read()

charm_page_responsive = """
    /* ── CHARM AI PAGE RESPONSIVE ADAPTATION (MOBILE & TABLET) ── */
    @media (max-width: 768px) {
      .ai-wrap {
        padding: 20px 14px calc(80px + env(safe-area-inset-bottom, 0px)) !important;
        max-width: 100% !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
      }
      .ai-hero {
        margin-bottom: 24px !important;
      }
      .ai-h1 {
        font-size: clamp(1.85rem, 6.5vw, 2.5rem) !important;
      }
      .ai-lead {
        font-size: 0.94rem !important;
      }
      .ai-console-card {
        padding: 20px 14px !important;
        border-radius: 16px !important;
        margin-bottom: 24px !important;
        box-sizing: border-box !important;
      }
      .ai-grid {
        grid-template-columns: 1fr !important;
        gap: 14px !important;
      }
      .ai-input-box input,
      .ai-input-box textarea {
        padding: 10px 12px !important;
        font-size: 0.88rem !important;
        box-sizing: border-box !important;
      }
      .btn-ai-ask {
        width: 100% !important;
        padding: 14px !important;
        font-size: 0.90rem !important;
        min-height: 48px !important;
        border-radius: 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        box-sizing: border-box !important;
      }
      .ai-status-row {
        flex-direction: column !important;
        align-items: flex-start !important;
        gap: 8px !important;
      }
      .ai-status-row button {
        padding: 4px 0 !important;
      }
      .ai-response-box {
        padding: 18px 14px !important;
        border-radius: 14px !important;
      }
    }
"""

if 'CHARM AI PAGE RESPONSIVE ADAPTATION' not in cpage:
    cpage = cpage.replace('</style>', charm_page_responsive + '\n  </style>', 1)
    print("Added responsive Charm AI CSS to charm_ai.html")

# Also add ai-status-row class to the status bar in charm_ai.html
old_status_div = '<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">'
new_status_div = '<div class="ai-status-row" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">'
if old_status_div in cpage:
    cpage = cpage.replace(old_status_div, new_status_div, 1)
    print("Added class ai-status-row to charm_ai.html")

with open(charm_page_path, 'w', encoding='utf-8') as f:
    f.write(cpage)

print("All Charm AI CTA alignment fixes applied successfully.")
