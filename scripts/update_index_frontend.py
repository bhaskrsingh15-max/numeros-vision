# -*- coding: utf-8 -*-
import os

path = os.path.join("app", "static", "index.html")
with open(path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update .calc-interactive-card width to 1060px for graceful page alignment
text = text.replace(
    '.calc-interactive-card {\n      background: #FFFFFF;\n      border: 1.5px solid var(--border-amber);\n      border-radius: 22px;\n      padding: clamp(22px, 4vw, 36px);\n      max-width: 860px;',
    '.calc-interactive-card {\n      background: #FFFFFF;\n      border: 1.5px solid var(--border-amber);\n      border-radius: 22px;\n      padding: clamp(24px, 4vw, 40px);\n      max-width: 1060px;'
)

# Also handle if already max-width: 860px or similar
text = text.replace('max-width: 860px;\n      margin: 0 auto 40px;', 'max-width: 1060px;\n      margin: 0 auto 40px;')
text = text.replace('.nv-explore-section {\n      margin: 44px auto 36px;\n      max-width: 860px;', '.nv-explore-section {\n      margin: 44px auto 36px;\n      max-width: 1060px;')
text = text.replace('.charm-ai-card {\n      background: #FFFFFF;\n      border: 1.5px solid var(--border-amber);\n      border-radius: 22px;\n      padding: 32px;\n      max-width: 840px;', '.charm-ai-card {\n      background: #FFFFFF;\n      border: 1.5px solid var(--border-amber);\n      border-radius: 22px;\n      padding: 32px;\n      max-width: 980px;')

# 2. Output Dashboard Layout: 3x3 Grid and Driver/Conductor side-by-side
old_results_html = '''        <!-- Dynamic Output Dashboard -->
        <div class="results-dashboard" id="birth-results" style="display:none;">
          <!-- Lo Shu 3x3 Grid Display (Primary Front-End Matrix) -->
          <div class="loshu-mini-wrap">
            <div class="matrix-box-label" style="font-size:1.05rem; font-weight:700; color:var(--gold-dark); margin-bottom:10px;">
              ✦ Your Energy Pattern (Ancient 3×3 Grid) ✦
            </div>
            <div class="loshu-mini-grid" id="loshu-grid-container">
              <!-- Grid populated via JS -->
            </div>
            <div id="loshu-summary-text" style="font-size:0.86rem; color:var(--text-muted); margin-top:14px; line-height:1.6;"></div>
          </div>

          <div class="matrix-output-grid">
            <div class="matrix-box">
              <div class="matrix-box-label">Natural Talent · Inner Drive (Mulank)</div>
              <div class="matrix-box-num" id="out-driver">-</div>
              <div class="matrix-box-planet" id="out-driver-planet">Ruling Planet</div>
              <div style="font-size:0.8rem; color:#7A654D; margin-top:6px;">Your inborn traits, decision temperament, and instinctive self.</div>
            </div>

            <div class="matrix-box">
              <div class="matrix-box-label">Life Purpose · Destiny Path (Bhagyank)</div>
              <div class="matrix-box-num" id="out-conductor">-</div>
              <div class="matrix-box-planet" id="out-conductor-planet">Destiny Trajectory</div>
              <div style="font-size:0.8rem; color:#7A654D; margin-top:6px;">Your overarching life lessons, outer path, and karmic trajectory.</div>
            </div>
          </div>
          <!-- Planetary Characteristics & Archetype Dossier (Canonical Registry) -->
          <div id="planet-characteristics-results"></div>'''

new_results_html = '''        <!-- Dynamic Output Dashboard -->
        <div class="results-dashboard" id="birth-results" style="display:none;">
          <!-- Lo Shu 3x3 Grid & Core Numbers Aligned Side-by-Side -->
          <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(320px, 1fr)); gap:24px; align-items:start; margin-bottom:24px;">
            <div class="loshu-mini-wrap" style="margin:0; background:#FAF6EE; border:1px solid rgba(201,162,39,0.3); border-radius:16px; padding:20px;">
              <div class="matrix-box-label" style="font-size:1.05rem; font-weight:700; color:var(--gold-dark); margin-bottom:12px;">
                ✦ Your Energy Pattern (Ancient 3×3 Grid) ✦
              </div>
              <div class="loshu-mini-grid" id="loshu-grid-container">
                <!-- Grid populated via JS -->
              </div>
              <div id="loshu-summary-text" style="font-size:0.86rem; color:var(--text-muted); margin-top:14px; line-height:1.6;"></div>
            </div>

            <div class="matrix-output-grid" style="margin:0; display:flex; flex-direction:column; gap:16px;">
              <div class="matrix-box" style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.3); border-radius:14px; padding:18px 20px;">
                <div class="matrix-box-label" style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#8B6914; font-weight:700;">Innate Talents · Inner Drive (Mulank)</div>
                <div class="matrix-box-num" id="out-driver" style="font-size:2.8rem; font-weight:800; color:#8B6914; margin:4px 0;">-</div>
                <div class="matrix-box-planet" id="out-driver-planet" style="font-size:1.05rem; font-weight:700; color:#523E28;">Ruling Planet</div>
                <div style="font-size:0.84rem; color:#7A654D; margin-top:6px; line-height:1.5;">Your inborn traits, decision temperament, and instinctive self.</div>
              </div>

              <div class="matrix-box" style="background:#FFFDF7; border:1px solid rgba(22,131,91,0.3); border-radius:14px; padding:18px 20px;">
                <div class="matrix-box-label" style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#16835B; font-weight:700;">Life Purpose · Destiny Path (Bhagyank)</div>
                <div class="matrix-box-num" id="out-conductor" style="font-size:2.8rem; font-weight:800; color:#16835B; margin:4px 0;">-</div>
                <div class="matrix-box-planet" id="out-conductor-planet" style="font-size:1.05rem; font-weight:700; color:#523E28;">Destiny Trajectory</div>
                <div style="font-size:0.84rem; color:#7A654D; margin-top:6px; line-height:1.5;">Your overarching life lessons, outer path, and karmic trajectory.</div>
              </div>
            </div>
          </div>
          <!-- Planetary Characteristics & Archetype Blueprint -->
          <div id="planet-characteristics-results"></div>'''

text = text.replace(old_results_html.replace('\r\n', '\n'), new_results_html.replace('\r\n', '\n'))

# 3. Remove auto-grant of test_master_pass
text = text.replace("if (!localStorage.getItem('nv_premium_token')) {\n          localStorage.setItem('nv_premium_token', 'test_master_pass');\n        }", "// User starts with default free tier")
text = text.replace("premium_token: localStorage.getItem('nv_premium_token') || 'test_master_pass'", "premium_token: localStorage.getItem('nv_premium_token') || ''")

# 4. Clean up sendChatMessage rendering: do NOT append redundant whyText or developer card, and gate remedies
old_extras = '''          let extrasHtml = '';
          if (whyText) {
            extrasHtml += `<div style="font-size:0.86rem; color:#523E28; line-height:1.6; margin-bottom:12px; background:#FAF6EE; padding:12px 14px; border-radius:10px; border-left:3.5px solid #C9A227; border:1px solid rgba(201,162,39,0.25);"><strong>Planetary Root Cause:</strong> ${whyText}</div>`;
          }
          if (charmCardHtml) extrasHtml += charmCardHtml;
          if (luckyHtml) extrasHtml += luckyHtml;
          if (remediesHtml) extrasHtml += remediesHtml;
          if (validationHtml) extrasHtml += validationHtml;'''

new_extras = '''          let extrasHtml = '';
          // Only append consecrated remedies if the user is a paid subscriber and remedies are returned
          if (data.is_premium && Array.isArray(data.remedies) && data.remedies.length > 0) {
            extrasHtml += remediesHtml;
          }
          if (validationHtml && !data.is_freemium_gate) extrasHtml += validationHtml;'''

text = text.replace(old_extras.replace('\r\n', '\n'), new_extras.replace('\r\n', '\n'))

with open(path, "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: index.html updated successfully.")
