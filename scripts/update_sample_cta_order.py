# -*- coding: utf-8 -*-
import os, sys

path = 'app/static/sample.html'
with open(path, 'r', encoding='utf-8') as f:
    c = f.read()

target = """                  <div style="margin-bottom:4px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:4px;">
                    <span onclick="showPaywallUnlockModal('master')" style="cursor:pointer; display:inline-flex; align-items:center; gap:4px; background:rgba(22,131,91,0.08); border:1px solid #16835B; padding:3.5px 7px; border-radius:4px; color:#16835B; font-weight:800; font-size:9.5px; text-decoration:none;">
                      🔓 Active Charm Present @ 510 [ ${present.join(', ')} ] →
                    </span>
                    <span onclick="showPaywallUnlockModal('roadmap')" style="cursor:pointer; display:inline-flex; align-items:center; gap:4px; background:rgba(201,162,39,0.12); border:1px solid #8B6914; padding:3.5px 7px; border-radius:4px; color:#8B6914; font-weight:800; font-size:9.5px; text-decoration:none;">
                      🔒 Anveil Charm Missing @ 1050 [ ${missing.join(', ')} ] →
                    </span>
                  </div>"""

replacement = """                  <div style="margin-bottom:4px; display:flex; flex-direction:column; gap:3px;">
                    <!-- 1. 1050 First: Anveil Charm Missing Numbers -->
                    <span onclick="showPaywallUnlockModal('roadmap')" style="cursor:pointer; display:flex; align-items:center; justify-content:space-between; background:rgba(201,162,39,0.12); border:1px solid #8B6914; padding:3px 6px; border-radius:4px; color:#8B6914; font-weight:800; font-size:9px; text-decoration:none;">
                      <span>🔒 1. Anveil Charm Missing [ ${missing.join(', ')} ]</span>
                      <span>@ <span style="text-decoration:line-through; color:#8C827A; font-weight:normal;">₹2,100</span> 1050 →</span>
                    </span>

                    <!-- 2. 510 Second: Active Charm Present Numbers -->
                    <span onclick="showPaywallUnlockModal('master')" style="cursor:pointer; display:flex; align-items:center; justify-content:space-between; background:rgba(22,131,91,0.08); border:1px solid #16835B; padding:3px 6px; border-radius:4px; color:#16835B; font-weight:800; font-size:9px; text-decoration:none;">
                      <span>🔓 2. Active Charm Present [ ${present.join(', ')} ]</span>
                      <span>@ <span style="text-decoration:line-through; color:#8C827A; font-weight:normal;">₹999</span> 510 →</span>
                    </span>

                    <!-- 3. 199 Third: Anveil Element Yogas Charm (Single Percentage Number Only) -->
                    <span onclick="showPaywallUnlockModal('brief')" style="cursor:pointer; display:flex; align-items:center; justify-content:space-between; background:rgba(139,105,20,0.08); border:1px solid #8B6914; padding:3px 6px; border-radius:4px; color:#8B6914; font-weight:800; font-size:9px; text-decoration:none;">
                      <span>⚡ 3. Anveil Element Yogas Charm (${Math.round((alignedPlanes.length / 8) * 100)}% Active)</span>
                      <span>@ <span style="text-decoration:line-through; color:#8C827A; font-weight:normal;">₹499</span> 199 →</span>
                    </span>
                  </div>"""

if target in c:
    c = c.replace(target, replacement)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("SUCCESS: Updated CTA order in sample.html")
else:
    # Try normalizing line endings
    c_norm = c.replace('\r\n', '\n')
    target_norm = target.replace('\r\n', '\n')
    if target_norm in c_norm:
        c_norm = c_norm.replace(target_norm, replacement)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(c_norm)
        print("SUCCESS (normalized): Updated CTA order in sample.html")
    else:
        print("ERROR: Target block not found in sample.html")
