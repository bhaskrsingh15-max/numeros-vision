"""
Removes Over-CTA repetition from sample.html and other files.
Replaces repeated price tags in grid cells and stacked CTA bars with a single, elegant unlock path.
"""
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/sample.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Clean line 1748 & 1757
c = c.replace(
    '<div style="font-size:7px; color:#7A654D;">${label} · <span style="text-decoration:line-through; color:#8C827A; font-weight:normal;">₹2,100</span> <strong style="color:#8B6914;">₹1,050</strong></div>',
    '<div style="font-size:7px; color:#7A654D;">${label} · Missing</div>'
)

c = c.replace(
    '<div style="font-size:7px; color:#16835B; font-weight:700;">${label} · <span style="text-decoration:line-through; color:#8C827A; font-weight:normal;">₹999</span> ₹510</div>',
    '<div style="font-size:7px; color:#16835B; font-weight:700;">${label} · Active</div>'
)

# 2. Clean the 3 stacked CTA bars beneath the grid
old_stacked_ctas = """                  <div style="margin-bottom:4px; display:flex; flex-direction:column; gap:3px;">
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

new_single_cta = """                  <div style="margin-bottom:4px;">
                    <div onclick="showPaywallUnlockModal('master')" style="cursor:pointer; display:flex; align-items:center; justify-content:space-between; background:rgba(201,162,39,0.12); border:1px solid #8B6914; padding:5px 8px; border-radius:6px; transition:all 0.2s;">
                      <div>
                        <span style="font-weight:800; color:#8B6914; font-size:9.5px; display:block;">✦ Element Yogas: ${Math.round((alignedPlanes.length / 8) * 100)}% Active</span>
                        <span style="color:#7A654D; font-size:8px;">Missing [ ${missing.join(', ')} ] · Present [ ${present.join(', ')} ]</span>
                      </div>
                      <span style="background:#8B6914; color:#FFFFFF; padding:3px 8px; border-radius:4px; font-size:8.5px; font-weight:700;">
                        Unlock Complete Blueprint ➔
                      </span>
                    </div>
                  </div>"""

# Try with CRLF and LF
c = c.replace(old_stacked_ctas.replace('\r\n', '\n'), new_single_cta.replace('\r\n', '\n'))
c = c.replace(old_stacked_ctas, new_single_cta)

# 3. Clean second instance of renderLoShuCell (around line 2867 & 2876)
c = c.replace(
    '<div style="font-size:7px; color:#7A654D;">${label} · <span style="text-decoration:line-through; color:#8C827A; font-weight:normal;">₹2,100</span> <strong style="color:#8B6914;">₹1,050</strong></div>',
    '<div style="font-size:7px; color:#7A654D;">${label} · Missing</div>'
)
c = c.replace(
    '<div style="font-size:7px; color:#16835B; font-weight:700;">${label} · <span style="text-decoration:line-through; color:#8C827A; font-weight:normal;">₹999</span> ₹510</div>',
    '<div style="font-size:7px; color:#16835B; font-weight:700;">${label} · Active</div>'
)

# 4. Clean unlock modal to show 3 clean options instead of wall of text
old_modal_content = """      <div style="display:flex; flex-direction:column; gap:10px;">
        <a id="paywallModalCtaBtn" href="/pricing/" class="btn-gold" style="padding:14px 24px; font-size:0.95rem; font-weight:700; text-decoration:none; display:block; border-radius:10px; background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFFFF;">
          ANVEIL EVERY CHARM ✦ Unlock Full Dossier (From ₹199) →
        </a>
        <button onclick="closePaywallModal()" style="background:none; border:none; color:#7A654D; font-size:0.82rem; cursor:pointer; text-decoration:underline;">
          Continue Viewing Free Discovery Report (Pages 1–3)
        </button>
      </div>"""

new_modal_content = """      <!-- 3 Tier Clear Selection in Modal -->
      <div style="display:flex; flex-direction:column; gap:8px; margin-bottom:16px; text-align:left;">
        <a href="/checkout/?plan=report_divine" style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; border:2px solid #8B6914; background:#FFFDF7; border-radius:10px; text-decoration:none; color:#523E28;">
          <div>
            <div style="font-weight:800; font-size:0.88rem; color:#8B6914;">Diamond Sovereign Compendium (32 Pages)</div>
            <div style="font-size:0.75rem; color:#7A654D;">Full Missing Numbers Remedies, Name Correction &amp; Vastu</div>
          </div>
          <div style="text-align:right;">
            <div style="font-family:'Cinzel',serif; font-weight:900; font-size:1.1rem; color:#8B6914;">₹1,050</div>
            <div style="font-size:0.70rem; color:#8C827A; text-decoration:line-through;">₹2,100</div>
          </div>
        </a>
        <a href="/checkout/?plan=report_master" style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; border:1px solid #16835B; background:#FFFFFF; border-radius:10px; text-decoration:none; color:#523E28;">
          <div>
            <div style="font-weight:800; font-size:0.88rem; color:#16835B;">Gold Master Dossier (12 Pages)</div>
            <div style="font-size:0.75rem; color:#7A654D;">Present Numbers Harmonization, 5-Year Dasha &amp; Career</div>
          </div>
          <div style="text-align:right;">
            <div style="font-family:'Cinzel',serif; font-weight:900; font-size:1.1rem; color:#16835B;">₹510</div>
            <div style="font-size:0.70rem; color:#8C827A; text-decoration:line-through;">₹999</div>
          </div>
        </a>
        <a href="/checkout/?plan=report_basic" style="display:flex; justify-content:space-between; align-items:center; padding:10px 14px; border:1px solid rgba(201,162,39,0.4); background:#FFFFFF; border-radius:10px; text-decoration:none; color:#523E28;">
          <div>
            <div style="font-weight:800; font-size:0.88rem; color:#8B6914;">Silver Discovery Blueprint (3 Pages)</div>
            <div style="font-size:0.75rem; color:#7A654D;">Driver-Conductor Strengths &amp; Element Yogas Overview</div>
          </div>
          <div style="text-align:right;">
            <div style="font-family:'Cinzel',serif; font-weight:900; font-size:1.1rem; color:#8B6914;">₹199</div>
            <div style="font-size:0.70rem; color:#8C827A; text-decoration:line-through;">₹499</div>
          </div>
        </a>
      </div>

      <div style="display:flex; flex-direction:column; gap:8px;">
        <button onclick="closePaywallModal()" style="background:none; border:none; color:#7A654D; font-size:0.82rem; cursor:pointer; text-decoration:underline;">
          Continue Viewing Sample Preview
        </button>
      </div>"""

c = c.replace(old_modal_content.replace('\r\n', '\n'), new_modal_content.replace('\r\n', '\n'))
c = c.replace(old_modal_content, new_modal_content)

with open('app/static/sample.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("Successfully cleaned sample.html Over-CTA clutter.")
