import os

# Update ai-avatar-wrap in charm_ai.html and index.html
files_to_update = ['app/static/charm_ai.html', 'app/static/index.html']

old_avatar_style = '''.ai-avatar-wrap {
      width: 44px;
      height: 44px;
      border-radius: 50%;
      background: #FFFDF7;
      border: 1.8px solid #C9A227;
      box-shadow: 0 2px 10px rgba(201, 162, 39, 0.28);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      overflow: hidden;
      padding: 2px;
    }'''

new_avatar_style = '''.ai-avatar-wrap {
      width: 44px;
      height: 44px;
      border-radius: 50% !important;
      background: linear-gradient(135deg, #E2B84B 0%, #C9A227 45%, #8B6914 100%) !important;
      border: 2px solid #FFFDF7 !important;
      box-shadow: 0 4px 14px rgba(201, 162, 39, 0.45) !important;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      overflow: hidden;
      padding: 0 !important;
    }
    .ai-avatar-wrap svg {
      width: 22px;
      height: 22px;
      stroke: #FFFFFF;
      fill: none;
      display: block;
    }'''

for fp in files_to_update:
    if os.path.exists(fp):
        with open(fp, 'r', encoding='utf-8') as f:
            c = f.read()
        # Replace background and border in .ai-avatar-wrap
        c = c.replace('background: #FFFDF7;\n      border: 1.8px solid #C9A227;', 'background: linear-gradient(135deg, #E2B84B 0%, #C9A227 45%, #8B6914 100%);\n      border: 2px solid #FFFDF7;')
        c = c.replace('background: #FFFDF7;\r\n      border: 1.8px solid #C9A227;', 'background: linear-gradient(135deg, #E2B84B 0%, #C9A227 45%, #8B6914 100%);\r\n      border: 2px solid #FFFDF7;')
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        print(f"Updated {fp}")

# Also check theme.css if ai-avatar-wrap is there
theme_path = 'app/static/css/theme.css'
if os.path.exists(theme_path):
    with open(theme_path, 'r', encoding='utf-8') as f:
        tc = f.read()
    if '.ai-avatar-wrap' in tc:
        tc = tc.replace('background: #FFFDF7;\n  border: 1.8px solid #C9A227;', 'background: linear-gradient(135deg, #E2B84B 0%, #C9A227 45%, #8B6914 100%);\n  border: 2px solid #FFFDF7;')
        tc = tc.replace('background: #FFFDF7;\r\n  border: 1.8px solid #C9A227;', 'background: linear-gradient(135deg, #E2B84B 0%, #C9A227 45%, #8B6914 100%);\r\n  border: 2px solid #FFFDF7;')
        with open(theme_path, 'w', encoding='utf-8') as f:
            f.write(tc)
        print("Updated theme.css")
