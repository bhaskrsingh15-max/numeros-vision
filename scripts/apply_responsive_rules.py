import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. UPDATE roadmap_components.css
css_path = r"app\static\css\roadmap_components.css"
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace .nv-sticky-bottom-nav inside @media (max-width: 1199px)
old_bottom_nav_css = """@media (max-width: 1199px) {
  body {
    padding-bottom: 74px !important;
  }
  
  .nv-sticky-bottom-nav {
    display: flex !important;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    height: 64px;
    background: rgba(255, 253, 247, 0.97);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-top: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38));
    box-shadow: 0 -4px 22px rgba(82, 62, 40, 0.14);
    z-index: 99998;
    padding: 6px 8px calc(6px + env(safe-area-inset-bottom));
    justify-content: space-around;
    align-items: center;
    box-sizing: border-box;
  }

  .nv-bottom-nav-item,
  .nv-bottom-item {
    display: flex !important;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-decoration: none;
    color: #7A654D;
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    font-weight: 500;
    padding: 4px 6px;
    border-radius: 8px;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    min-width: 52px;
    min-height: 48px;
    background: none;
    border: none;
    cursor: pointer;
    touch-action: manipulation;
    -webkit-tap-highlight-color: rgba(201, 162, 39, 0.2);
    user-select: none;
    -webkit-user-select: none;
  }"""

new_bottom_nav_css = """@media (max-width: 1199px) {
  body {
    padding-bottom: calc(76px + env(safe-area-inset-bottom, 0px)) !important;
  }
  
  .nv-sticky-bottom-nav {
    display: flex !important;
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    width: 100%;
    min-height: 60px;
    height: auto;
    height: calc(60px + env(safe-area-inset-bottom, 0px));
    background: rgba(255, 253, 247, 0.98);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-top: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38));
    box-shadow: 0 -4px 24px rgba(82, 62, 40, 0.16);
    z-index: 99998;
    padding: 6px 12px calc(8px + env(safe-area-inset-bottom, 0px));
    justify-content: space-around;
    align-items: center;
    box-sizing: border-box;
  }

  .nv-bottom-nav-item,
  .nv-bottom-item {
    display: flex !important;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    flex: 1 1 0;
    max-width: 130px;
    text-decoration: none;
    color: #7A654D;
    font-family: 'Inter', sans-serif;
    font-size: 0.68rem;
    font-weight: 500;
    padding: 4px 6px;
    border-radius: 8px;
    transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    min-width: 48px;
    min-height: 44px;
    background: none;
    border: none;
    cursor: pointer;
    touch-action: manipulation;
    -webkit-tap-highlight-color: rgba(201, 162, 39, 0.2);
    user-select: none;
    -webkit-user-select: none;
    box-sizing: border-box;
  }"""

if old_bottom_nav_css.replace("\r\n", "\n") in css.replace("\r\n", "\n"):
    css = css.replace("\r\n", "\n").replace(old_bottom_nav_css.replace("\r\n", "\n"), new_bottom_nav_css.replace("\r\n", "\n"))
    print("Updated bottom nav in roadmap_components.css")
else:
    print("WARNING: old_bottom_nav_css pattern not matched directly in roadmap_components.css")

# Also update tablet dock media query in roadmap_components.css
old_tablet_dock = """/* Tablet floating dock layout (iPad Mini, iPad Air, Android Tabs 769px - 1199px) */
@media (min-width: 769px) and (max-width: 1199px) {
  .nv-sticky-bottom-nav {
    max-width: 640px !important;
    left: 50% !important;
    right: auto !important;
    transform: translateX(-50%) !important;
    border-radius: 18px 18px 0 0 !important;
    border-left: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38)) !important;
    border-right: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38)) !important;
  }
}"""

new_tablet_dock = """/* Tablet floating dock layout (iPad Mini, iPad Air, Android Tabs 600px - 1199px) */
@media (min-width: 600px) and (max-width: 1199px) {
  .nv-sticky-bottom-nav {
    max-width: 520px !important;
    left: 50% !important;
    right: auto !important;
    transform: translateX(-50%) !important;
    border-radius: 18px 18px 0 0 !important;
    border-left: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38)) !important;
    border-right: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38)) !important;
    box-shadow: 0 -4px 28px rgba(82, 62, 40, 0.18) !important;
  }
}"""

if old_tablet_dock.replace("\r\n", "\n") in css.replace("\r\n", "\n"):
    css = css.replace("\r\n", "\n").replace(old_tablet_dock.replace("\r\n", "\n"), new_tablet_dock.replace("\r\n", "\n"))
    print("Updated tablet dock in roadmap_components.css")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

# 2. UPDATE reports_catalogue.html WITH RESPONSIVE RULES & CLEAN CLASS
rc_path = r"app\static\reports_catalogue.html"
with open(rc_path, 'r', encoding='utf-8') as f:
    rc = f.read()

# Add responsive media queries to reports_catalogue.html if not present
responsive_css = """
    /* ── MOBILE & TABLET RESPONSIVE REFINEMENTS (320px to 1024px) ── */
    @media (max-width: 768px) {
      .catalogue-wrap {
        padding: 16px 14px calc(80px + env(safe-area-inset-bottom, 0px));
        max-width: 100%;
        overflow-x: hidden;
      }
      .reports-hero {
        padding: 28px 14px 22px;
        margin-bottom: 24px;
        border-radius: 16px;
      }
      .reports-h1 {
        font-size: clamp(1.85rem, 6.5vw, 2.4rem);
      }
      .reports-lead {
        font-size: 0.95rem;
        margin-bottom: 20px;
      }
      .hero-trust-bar {
        gap: 8px;
      }
      .trust-chip {
        font-size: 0.74rem;
        padding: 5px 10px;
      }
      .nv-cat-tabs {
        display: flex;
        flex-wrap: nowrap;
        overflow-x: auto;
        -webkit-overflow-scrolling: touch;
        justify-content: flex-start;
        padding: 4px 2px 14px;
        gap: 8px;
        scrollbar-width: none;
      }
      .nv-cat-tabs::-webkit-scrollbar {
        display: none;
      }
      .nv-cat-tab {
        white-space: nowrap;
        flex-shrink: 0;
        padding: 8px 16px;
        font-size: 0.82rem;
      }
      .reports-grid {
        grid-template-columns: 1fr !important;
        gap: 20px;
        margin-bottom: 36px;
      }
      .report-card {
        padding: 20px 16px;
        border-radius: 16px;
      }
      .report-card h3 {
        font-size: 1.15rem;
        min-height: auto;
      }
      .report-desc {
        font-size: 0.84rem;
        min-height: auto;
      }
      .tier-options-group {
        gap: 4px;
      }
      .tier-btn {
        padding: 6px 2px;
        font-size: 0.74rem;
      }
      .tier-btn small {
        font-size: 0.62rem;
      }
      .bundles-grid {
        grid-template-columns: 1fr !important;
        gap: 18px;
      }
      .bundle-card {
        padding: 20px 16px;
      }
      .nv-modal-window {
        padding: 24px 18px;
        border-radius: 18px;
        margin: 10px;
      }
    }

    @media (min-width: 769px) and (max-width: 1024px) {
      .reports-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 22px;
      }
      .bundles-grid {
        grid-template-columns: repeat(2, 1fr) !important;
        gap: 20px;
      }
    }
"""

if 'MOBILE & TABLET RESPONSIVE REFINEMENTS' not in rc:
    rc = rc.replace('</style>', responsive_css + '\n  </style>', 1)
    with open(rc_path, 'w', encoding='utf-8') as f:
        f.write(rc)
    print("Added responsive media queries to reports_catalogue.html")

print("Responsive rules update complete.")
