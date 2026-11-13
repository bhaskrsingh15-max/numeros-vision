# -*- coding: utf-8 -*-
with open('app/static/css/roadmap_components.css', 'r', encoding='utf-8') as f:
    text = f.read()

old_center_css = """  /* Floating Center Highlighted Action (Baby Naming) */
  .nv-bottom-nav-center {
    position: relative;
    top: -10px;
  }

  .nv-bottom-center-btn {
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 18px rgba(201, 162, 39, 0.45);
    border: 2px solid #FFFDF7;
    transition: all 0.25s ease;
  }

  .nv-bottom-center-btn svg {
    width: 20px;
    height: 20px;
    stroke: #FFFFFF;
    margin-bottom: 0;
  }

  .nv-bottom-nav-center:hover .nv-bottom-center-btn,
  .nv-bottom-nav-center:active .nv-bottom-center-btn {
    transform: scale(1.08);
    box-shadow: 0 8px 24px rgba(201, 162, 39, 0.6);
  }

  .nv-bottom-nav-center span {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--gold-dark, #8B6914);
    margin-top: 2px;
  }"""

new_center_css = """  /* Floating Center Highlighted Action (Charm AI Oracle) */
  .nv-bottom-nav-center {
    position: relative;
    top: -12px;
  }

  .nv-bottom-center-btn {
    width: 46px;
    height: 46px;
    border-radius: 50%;
    background: linear-gradient(135deg, #E2B84B 0%, #C9A227 45%, #8B6914 100%);
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 18px rgba(201, 162, 39, 0.45);
    border: 2.5px solid #FFFDF7;
    transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
  }

  .nv-bottom-center-btn svg {
    width: 22px;
    height: 22px;
    stroke: #FFFFFF;
    margin-bottom: 0;
  }

  .nv-bottom-nav-center:hover .nv-bottom-center-btn,
  .nv-bottom-nav-center:active .nv-bottom-center-btn {
    transform: scale(1.1);
    box-shadow: 0 8px 24px rgba(201, 162, 39, 0.65);
  }

  .nv-bottom-nav-center.active .nv-bottom-center-btn {
    border-color: #FFFDF7;
    box-shadow: 0 0 0 3px rgba(201, 162, 39, 0.5), 0 8px 24px rgba(201, 162, 39, 0.65);
    transform: scale(1.08);
  }

  .nv-bottom-nav-center span {
    font-size: 0.65rem;
    font-weight: 700;
    color: var(--gold-dark, #8B6914);
    margin-top: 3px;
    letter-spacing: 0.02em;
  }

  /* Mobile Hamburger Drawer Charm AI Highlight */
  .nv-nav-charm-highlight .nv-nav-link {
    color: var(--gold-dark, #8B6914) !important;
    font-weight: 700 !important;
  }
  .nv-nav-charm-highlight .nv-nav-link:hover,
  .nv-nav-charm-highlight .nv-nav-link:active {
    background: rgba(201, 162, 39, 0.12) !important;
  }"""

old_crlf = old_center_css.replace('\n', '\r\n')
new_crlf = new_center_css.replace('\n', '\r\n')

if old_crlf in text:
    text = text.replace(old_crlf, new_crlf, 1)
    print("SUCCESS: Updated roadmap_components.css (CRLF)")
elif old_center_css in text:
    text = text.replace(old_center_css, new_center_css, 1)
    print("SUCCESS: Updated roadmap_components.css (LF)")
else:
    print("Warning: old_center_css not found")

with open('app/static/css/roadmap_components.css', 'w', encoding='utf-8') as f:
    f.write(text)
