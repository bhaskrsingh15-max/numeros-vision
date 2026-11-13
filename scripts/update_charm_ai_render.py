with open('app/static/charm_ai.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Locate the panel.innerHTML block
start_marker = "panel.innerHTML = `"
end_marker = "if (window.nvProfileSync && typeof window.nvProfileSync.renderSaveProfileCard === 'function') {"

start_pos = text.find(start_marker)
end_pos = text.find(end_marker)

if start_pos == -1 or end_pos == -1:
    print("Could not find markers in charm_ai.html")
    exit(1)

new_panel_render = """panel.innerHTML = `
          <div class="ai-msg-header">
            <div class="ai-avatar-wrap"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#FFFFFF" stroke-width="2.2" style="display:block;"><path d="m12 3-1.9 5.8a2 2 0 0 1-1.3 1.3L3 12l5.8 1.9a2 2 0 0 1 1.3 1.3L12 21l1.9-5.8a2 2 0 0 1 1.3-1.3L21 12l-5.8-1.9a2 2 0 0 1-1.3-1.3z"/></svg></div>
            <div style="display:flex; flex-direction:column; gap:2px; flex:1;">
              <div style="display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:6px;">
                <div style="display:flex; align-items:center; gap:6px;">
                  <span class="ai-author-name">Charm AI</span>
                  <span class="ai-verified-icon" title="Authentic Classical Numerology" aria-label="Verified" style="display:inline-flex; align-items:center; justify-content:center; width:18px; height:18px; border-radius:50%; background:#16835B; color:#FFFFFF; font-size:0.75rem; font-weight:800; line-height:1; box-shadow:0 1px 4px rgba(22,131,91,0.35);">✓</span>
                </div>
                <span style="font-size:0.70rem; font-weight:600; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif; color:#8B6914; background:rgba(201,162,39,0.12); border:1px solid rgba(201,162,39,0.28); border-radius:12px; padding:3px 10px;" data-trace-id="${traceId}" title="Audit Reference: ${traceId}">
                  ${topicTitle}
                </span>
              </div>
              <div class="ai-author-sub">Authentic Classical Synthesis • Verified Numerological Cycles</div>
            </div>
          </div>

          <!-- Grounded Dialogue Consultation (Zero Raw Code / Zero Markdown Artifacts) -->
          <div style="margin-bottom:20px; font-size:0.96rem; line-height:1.75; color:#523E28;">
            ${formatMarkdown(answer)}
          </div>

          <!-- CURIOSITY-BASED CONVERSION CARD (The Monetization Bridge — Master Pricing) -->
          <div class="charm-curiosity-card" style="margin-top:20px; margin-bottom:24px; background:linear-gradient(135deg, #FFFDF7 0%, #FAF6EE 100%); border:2px solid var(--gold, #C9A227); border-radius:16px; padding:24px 20px; text-align:center; box-shadow:0 6px 24px rgba(201,162,39,0.18);">
            <div style="display:inline-flex; align-items:center; justify-content:center; width:44px; height:44px; border-radius:50%; background:rgba(201,162,39,0.12); border:1.5px solid var(--gold, #C9A227); font-size:1.35rem; color:#8B6914; margin-bottom:10px;">
              ✦
            </div>
            <div style="font-family:'Cinzel', serif; font-size:0.72rem; letter-spacing:0.18em; text-transform:uppercase; color:var(--gold-dark, #8B6914); font-weight:700; margin-bottom:6px;">
              NUMEROS VISION • ANVEIL EVERY CHARM
            </div>
            <h4 style="font-family:'Cormorant Garamond', serif; font-size:1.6rem; font-weight:700; color:#523E28; margin:0 0 10px; line-height:1.25;">
              ANVEIL Your Karmic &amp; Destiny Charm — Explore Your Dasha Timeline &amp; Full Remedies
            </h4>
            <p style="font-size:0.88rem; color:var(--text-muted, #7A654D); line-height:1.65; max-width:660px; margin:0 auto 16px;">
              Unlock now and receive your complete personalized career acceleration blueprint: Complete 10-Year Career Progression Timeline, Peak High-Probability Career Golden Window, Full Vedic Astrological Gem &amp; Yantra Prescription, and Comprehensive 12-Page Personal Dossier with priority access to Charm AI VIP personal queue.
            </p>

            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(260px, 1fr)); gap:10px; text-align:left; max-width:680px; margin:0 auto 18px; background:#FFFFFF; border:1px solid rgba(201,162,39,0.28); border-radius:12px; padding:14px 18px; font-size:0.82rem; color:#523E28; font-weight:600;">
              <div>✦ 10-Year Vimshottari &amp; Numerology Dasha Progression Timeline</div>
              <div>✦ Monthly Breakthrough Corridors &amp; Peak Decision Dates</div>
              <div>✦ Personalized Consecrated Gemstone, Beej Mantra &amp; Yantra Prescription</div>
              <div>✦ Comprehensive 12-Page Personal Master Blueprint Dossier</div>
            </div>

            <!-- Centralized Master Pricing Display -->
            <div style="display:flex; align-items:center; justify-content:center; gap:12px; margin-bottom:16px; flex-wrap:wrap;">
              <span style="font-size:0.95rem; text-decoration:line-through; color:var(--text-muted, #7A654D);">MRP ₹999</span>
              <span style="font-family:'Cinzel', serif; font-size:1.65rem; font-weight:800; color:var(--gold-dark, #8B6914);">₹510</span>
              <span style="font-size:0.72rem; font-weight:700; color:#16835B; background:rgba(22,131,91,0.12); padding:3px 10px; border-radius:999px; text-transform:uppercase;">SPECIAL 49% LAUNCH DISCOUNT</span>
            </div>

            <!-- Primary and Secondary Actions -->
            <div style="display:flex; flex-direction:column; align-items:center; gap:12px; margin-bottom:12px;">
              <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap; width:100%;">
                <a href="/checkout/?plan=report_master&tool=charm-ai" style="display:inline-flex; align-items:center; justify-content:center; padding:13px 26px; background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFDF7; font-family:'Cinzel', serif; font-weight:700; font-size:0.86rem; letter-spacing:0.06em; border-radius:100px; text-decoration:none; box-shadow:0 4px 18px rgba(201,162,39,0.38); transition:all 0.2s ease;">
                  <span>✨ UNLOCK 10-YEAR ACCELERATION ROADMAP (12-PAGE DOSSIER — ₹510) ✨</span>
                </a>
                <a href="/checkout/?plan=report_basic&tool=charm-ai" style="display:inline-flex; align-items:center; justify-content:center; padding:11px 20px; background:#FFFDF7; border:1.5px solid rgba(201,162,39,0.45); color:#8B6914; font-weight:700; font-size:0.82rem; border-radius:100px; text-decoration:none;">
                  <span>⚡ Rapid Action Plan (3 Pages — ₹199)</span>
                </a>
              </div>
              <a href="/sample-report/" style="font-size:0.80rem; color:var(--text-muted, #7A654D); text-decoration:underline;">
                Or Preview Complete 72-Hour Free Silver Certificate &amp; Sample Dossier
              </a>
            </div>

            <div style="font-size:0.72rem; color:var(--text-muted, #7A654D); letter-spacing:0.04em;">
              Authentic Classical Numerology • Zero Fabricated Rules • 100% Confidential Report
            </div>
          </div>

          <!-- FREE NATAL LO SHU GRID BIRTH CHART (Crisp Expandable Accordion) -->
          <div style="margin-top:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center; background:#FFFDF7; border:1.5px solid rgba(201,162,39,0.35); border-radius:12px; padding:12px 18px; cursor:pointer;" onclick="const el = document.getElementById('aiLoShuGridContent'); el.style.display = el.style.display === 'none' ? 'block' : 'none';">
              <div style="display:flex; align-items:center; gap:8px;">
                <span style="color:#C9A227; font-size:1.15rem;">✦</span>
                <span style="font-family:'Cormorant Garamond',serif; font-size:1.25rem; font-weight:700; color:#8B6914;">
                  Read Your Natal Lo Shu Grid Matrix (Free Preview)
                </span>
              </div>
              <span style="font-size:0.80rem; color:#8B6914; font-weight:600;">▼ Click to View / Hide Grid</span>
            </div>
            <div id="aiLoShuGridContent" style="display:block; margin-top:10px;">
              ${loshuCardHtml}
            </div>
          </div>

          <!-- LUCKY HARMONIZERS CARD -->
          ${luckyHtml}

          ${whyText ? `
            <div style="font-size:0.88rem; color:#523E28; line-height:1.68; margin-top:16px; margin-bottom:16px; background:#FAF6EE; padding:14px 18px; border-radius:12px; border-left:4px solid #C9A227; border:1px solid rgba(201,162,39,0.22); box-shadow:0 2px 8px rgba(180,155,110,0.06);">
              <strong style="color:#8B6914;">Planetary Alignment &amp; Root Cause:</strong><br />
              ${whyText}
            </div>
          ` : ''}

          <!-- PROPRIETARY DETAILED DOSSIER MODULES -->
          <div class="gated-charm-wrap locked" id="gatedCharmDetailed_${traceId}">
            ${charmCardHtml}
            ${ageCardHtml}
            ${remediesHtml}
            ${validationHtml}
          </div>

          <div style="font-size:0.76rem; color:#7A654D; border-top:1px solid rgba(180,155,110,0.25); padding-top:12px; margin-top:18px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:8px;">
            <span>Profile: <strong>${name}</strong> (Born: ${day}-${month}-${year}) ${driverNum ? `• Driver ${driverNum} • Conductor ${conductorNum}` : ''}</span>
            <span>Classical Heritage Vault • Timeless Classical Heritage</span>
          </div>
          <div id="charmSaveProfileContainer" style="margin-top:14px;"></div>
        `;

        """

text = text[:start_pos] + new_panel_render + text[end_pos:]

with open('app/static/charm_ai.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated charm_ai.html render section successfully!")
