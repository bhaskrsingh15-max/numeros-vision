import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/pricing.html', 'r', encoding='utf-8') as f:
    pricing_content = f.read()

# Replace green button border in pricing.html with theme gold
old_gold_btn = r'\.btn-gold-action\s*\{[^}]+\}'
new_gold_btn = '''.btn-gold-action {
      background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
      color: #FFFFFF !important;
      border: 1.5px solid #8B6914;
      text-decoration: none;
      padding: 13px 20px;
      font-family: 'Inter', sans-serif;
      font-size: 0.85rem;
      font-weight: 700;
      text-align: center;
      border-radius: 999px;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 16px rgba(201, 162, 39, 0.32);
      transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
      box-sizing: border-box;
      width: 100%;
      line-height: 1.3;
    }
    .btn-gold-action:hover {
      background: linear-gradient(135deg, #E2B84B 0%, #C9A227 100%);
      color: #FFFFFF !important;
      border-color: #C9A227;
      box-shadow: 0 8px 26px rgba(201, 162, 39, 0.45);
      transform: translateY(-2px);
    }
    .btn-gold-action:active {
      transform: scale(0.98);
    }
    .tier-card.featured .btn-gold-action {
      background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
      border: 1.5px solid #8B6914;
      color: #FFFFFF !important;
      box-shadow: 0 6px 20px rgba(201, 162, 39, 0.38);
    }
    .tier-card.featured .btn-gold-action:hover {
      background: linear-gradient(135deg, #E2B84B 0%, #C9A227 100%);
      box-shadow: 0 10px 30px rgba(201, 162, 39, 0.50);
    }'''

pricing_updated = re.sub(r'/\* Unified Price Bottom Call to Action.*?\.tier-card\.featured \.btn-gold-action:hover\s*\{[^}]+\}', new_gold_btn, pricing_content, flags=re.DOTALL)

# Also ensure .btn-ghost-action is rounded pill and theme aligned
old_ghost_btn = r'\.btn-ghost-action\s*\{[^}]+\}\s*\.btn-ghost-action:hover\s*\{[^}]+\}'
new_ghost_btn = '''.btn-ghost-action {
      background: #FFFFFF;
      border: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38));
      color: #8B6914 !important;
      text-decoration: none;
      padding: 11px 18px;
      font-family: 'Inter', sans-serif;
      font-size: 0.82rem;
      font-weight: 600;
      text-align: center;
      border-radius: 999px;
      letter-spacing: 0.04em;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      transition: all 0.2s ease;
      box-sizing: border-box;
      width: 100%;
    }
    .btn-ghost-action:hover {
      background: #F7F3EA;
      border-color: #C9A227;
      color: #8B6914 !important;
      transform: translateY(-1px);
    }'''

pricing_updated = re.sub(old_ghost_btn, new_ghost_btn, pricing_updated)

with open('app/static/pricing.html', 'w', encoding='utf-8') as f:
    f.write(pricing_updated)

print("Updated pricing.html styling successfully!")
