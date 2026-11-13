import re

with open('app/static/css/roadmap_components.css', 'r', encoding='utf-8') as f:
    css = f.read()

# 1. Update .nv-charm-bot-avatar-btn in base styles
old_btn = r'''\.nv-charm-bot-avatar-btn\s*\{[^}]*\}'''
new_btn = '''.nv-charm-bot-avatar-btn {
  width: 58px;
  height: 58px;
  border-radius: 50% !important;
  background: linear-gradient(135deg, #E2B84B 0%, #C9A227 45%, #8B6914 100%) !important;
  border: 2.5px solid #FFFDF7 !important;
  box-shadow: 0 6px 24px rgba(201, 162, 39, 0.48), 0 2px 8px rgba(30, 24, 16, 0.12) !important;
  padding: 0 !important;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  position: relative;
  text-decoration: none;
  flex-shrink: 0;
  overflow: visible;
}'''

css = re.sub(old_btn, new_btn, css, count=1)

# 2. Update .nv-charm-bot-avatar-btn img
old_img = r'''\.nv-charm-bot-avatar-btn img\s*\{[^}]*\}'''
new_img = '''.nv-charm-bot-avatar-btn img {
  width: 100%;
  height: 100%;
  border-radius: 50% !important;
  object-fit: cover;
  display: block;
}
.nv-charm-bot-avatar-btn svg {
  width: 28px;
  height: 28px;
  stroke: #FFFFFF;
  display: block;
}'''
css = re.sub(old_img, new_img, css, count=1)

# 3. Update aura pulse border-radius: 22px -> 50%
css = css.replace('border-radius: 22px;\n  border: 1.5px solid rgba(201, 162, 39, 0.5);', 'border-radius: 50% !important;\n  border: 1.5px solid rgba(201, 162, 39, 0.55);')
css = css.replace('border-radius: 22px;\r\n  border: 1.5px solid rgba(201, 162, 39, 0.5);', 'border-radius: 50% !important;\r\n  border: 1.5px solid rgba(201, 162, 39, 0.55);')

# 4. In mobile media query: border-radius: 16px -> 50%
css = css.replace('border-radius: 16px;', 'border-radius: 50% !important;')

# 5. Add .nv-charm-medallion-icon class
medallion_class = '''
/* Canonical Charm AI Medallion Icon for Desktop Nav & Drawers */
.nv-charm-medallion-icon {
  width: 24px;
  height: 24px;
  border-radius: 50% !important;
  background: linear-gradient(135deg, #E2B84B 0%, #C9A227 45%, #8B6914 100%);
  border: 1.8px solid #FFFDF7;
  box-shadow: 0 2px 8px rgba(201, 162, 39, 0.42);
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  vertical-align: middle;
}
.nv-charm-medallion-icon svg {
  width: 13px;
  height: 13px;
  stroke: #FFFFFF;
  fill: none;
  display: block;
}
'''
if '.nv-charm-medallion-icon' not in css:
    css += medallion_class

with open('app/static/css/roadmap_components.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated roadmap_components.css successfully!")
