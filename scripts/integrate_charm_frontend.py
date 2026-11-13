"""
scripts/integrate_charm_frontend.py
===================================
Applies the Charm AI Dasha-first prediction and deterministic consensus card
to app/static/charm_ai.html, respecting brand identity, color palette, and zero raw black.
"""

import os

def update_charm_frontend():
    file_path = os.path.join("app", "static", "charm_ai.html")
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 1. Update ai-grid to include optional astrological inputs (TOB & City)
    old_grid = """      <div class="ai-grid">
        <div class="ai-input-box">
          <label for="ai_user_name">Your Name</label>
          <input type="text" id="ai_user_name" value="Arjun Sharma" placeholder="Your name" />
        </div>
        <div class="ai-input-box">
          <label>Date of Birth (DD-MM-YYYY)</label>
          <div style="display:flex; gap:8px;">
            <input type="number" id="ai_day" value="15" min="1" max="31" placeholder="DD" style="width:30%;" />
            <input type="number" id="ai_month" value="8" min="1" max="12" placeholder="MM" style="width:30%;" />
            <input type="number" id="ai_year" value="1990" min="1900" max="2030" placeholder="YYYY" style="width:40%;" />
          </div>
        </div>
      </div>"""

    new_grid = """      <div class="ai-grid">
        <div class="ai-input-box">
          <label for="ai_user_name">Your Name</label>
          <input type="text" id="ai_user_name" value="Arjun Sharma" placeholder="Your name" />
        </div>
        <div class="ai-input-box">
          <label>Date of Birth (DD-MM-YYYY)</label>
          <div style="display:flex; gap:8px;">
            <input type="number" id="ai_day" value="15" min="1" max="31" placeholder="DD" style="width:30%;" />
            <input type="number" id="ai_month" value="8" min="1" max="12" placeholder="MM" style="width:30%;" />
            <input type="number" id="ai_year" value="1990" min="1900" max="2030" placeholder="YYYY" style="width:40%;" />
          </div>
        </div>
        <div class="ai-input-box">
          <label for="ai_tob">Time of Birth (Optional for Astrological Alignment)</label>
          <input type="time" id="ai_tob" value="10:30" />
        </div>
        <div class="ai-input-box">
          <label for="ai_city">Birth City (Optional for Topocentric Coordinates)</label>
          <input type="text" id="ai_city" value="New Delhi" placeholder="e.g. New Delhi, Mumbai, Bengaluru" />
        </div>
      </div>"""

    content = content.replace(old_grid.replace("\n", "\r\n"), new_grid.replace("\n", "\r\n"))
    content = content.replace(old_grid, new_grid)

    # 2. Update fetch call in submitToCharmAI to pass tob and city
    old_fetch_body = """            name: name,
            day: day,
            month: month,
            year: year,
            question: q,
            premium_token: premiumToken,
            user_id: 'test_user_' + (name.toLowerCase().replace(/[^a-z0-9]/g, '_'))"""

    new_fetch_body = """            name: name,
            day: day,
            month: month,
            year: year,
            tob: document.getElementById("ai_tob") ? document.getElementById("ai_tob").value : "10:30",
            pob: document.getElementById("ai_city") ? document.getElementById("ai_city").value.trim() : "New Delhi",
            city: document.getElementById("ai_city") ? document.getElementById("ai_city").value.trim() : "New Delhi",
            question: q,
            premium_token: premiumToken,
            user_id: 'test_user_' + (name.toLowerCase().replace(/[^a-z0-9]/g, '_'))"""

    content = content.replace(old_fetch_body.replace("\n", "\r\n"), new_fetch_body.replace("\n", "\r\n"))
    content = content.replace(old_fetch_body, new_fetch_body)

    # 3. Add charmCardHtml creation & insertion before loshuCardHtml
    old_loshu_insertion = """          ${loshuCardHtml}
          ${ageCardHtml}"""

    new_loshu_insertion = """          ${charmCardHtml}
          ${loshuCardHtml}
          ${ageCardHtml}"""

    content = content.replace(old_loshu_insertion.replace("\n", "\r\n"), new_loshu_insertion.replace("\n", "\r\n"))
    content = content.replace(old_loshu_insertion, new_loshu_insertion)

    # Also extract charmCardHtml right before panel.innerHTML
    old_driver_extract = """        const driverNum = data.driver_number || (data.consensus_report && data.consensus_report.vedic_numerology ? data.consensus_report.vedic_numerology.driver_number : '');
        const conductorNum = data.conductor_number || (data.consensus_report && data.consensus_report.vedic_numerology ? data.consensus_report.vedic_numerology.conductor_number : '');"""

    new_driver_extract = """        const charmCardHtml = renderCharmAiCard(data.charm_prediction);
        const driverNum = data.driver_number || (data.consensus_report && data.consensus_report.vedic_numerology ? data.consensus_report.vedic_numerology.driver_number : '');
        const conductorNum = data.conductor_number || (data.consensus_report && data.consensus_report.vedic_numerology ? data.consensus_report.vedic_numerology.conductor_number : '');"""

    content = content.replace(old_driver_extract.replace("\n", "\r\n"), new_driver_extract.replace("\n", "\r\n"))
    content = content.replace(old_driver_extract, new_driver_extract)

    # 4. Insert renderCharmAiCard and submitCharmOutcome functions
    charm_card_functions = """
    // ── CHARM AI DETERMINISTIC CONSENSUS & DASHA CARD RENDERER ──
    function renderCharmAiCard(charm) {
      if (!charm) return '';
      const statusLabels = {
        'NUMEROLOGY_PRIMARY_CORROBORATED': { bg: 'rgba(22,131,91,0.12)', border: '#16835B', text: '#16835B', label: '✓ High Multi-Method Corroboration' },
        'NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED': { bg: 'rgba(201,162,39,0.15)', border: '#C9A227', text: '#8B6914', label: '✦ Moderate Corroboration' },
        'NUMEROLOGY_PRIMARY_CONFLICTED': { bg: 'rgba(184,93,25,0.12)', border: '#B85D19', text: '#B85D19', label: '⚠️ Methodological Divergence' },
        'NUMEROLOGY_ONLY': { bg: 'rgba(139,105,20,0.12)', border: '#8B6914', text: '#8B6914', label: '✦ Numerology-First Focus' }
      };
      const vStatus = charm.verification_status || 'NUMEROLOGY_ONLY';
      const badge = statusLabels[vStatus] || statusLabels['NUMEROLOGY_ONLY'];

      const primaryWindows = charm.primary_windows || [];
      let windowsHtml = '';
      if (primaryWindows.length > 0) {
        windowsHtml = primaryWindows.map((w) => `
          <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.3); border-radius:8px; padding:10px 14px; margin-top:6px;">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:4px;">
              <span style="font-family:'Cinzel',serif; font-size:1.05rem; font-weight:700; color:#8B6914;">
                ${w.start} &nbsp;➔&nbsp; ${w.end}
              </span>
              <span style="font-size:0.68rem; font-weight:700; color:#16835B; background:rgba(22,131,91,0.1); padding:2px 8px; border-radius:6px;">
                ${w.ruling_planet || 'Planetary Ruler'}
              </span>
            </div>
            <div style="font-size:0.80rem; color:#523E28; margin-top:4px; font-weight:500;">
              ${w.label || ''}
            </div>
          </div>
        `).join('');
      }

      const methodsList = charm.method_evidence || [];
      const methodsHtml = methodsList.map(m => {
        const isGated = m.assessment === 'NOT_EVALUATED';
        const isSupport = m.assessment === 'SUPPORTS';
        const pillColor = isSupport ? '#16835B' : (isGated ? '#7A654D' : '#B85D19');
        const pillBg = isSupport ? 'rgba(22,131,91,0.1)' : (isGated ? 'rgba(122,101,77,0.1)' : 'rgba(184,93,25,0.1)');
        const citations = (m.citations || []).map(c => `<span style="display:block; font-size:0.72rem; color:#7A654D; margin-top:3px;">📜 <em>${c.title}</em> (${c.locator})</span>`).join('');
        return `
          <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.22); border-radius:8px; padding:10px 12px;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
              <strong style="font-size:0.82rem; color:#8B6914;">${(m.methodId || '').replace(/_/g, ' ')}</strong>
              <span style="font-size:0.66rem; font-weight:700; color:${pillColor}; background:${pillBg}; padding:2px 6px; border-radius:6px;">
                ${isGated ? 'Gated / In Review' : m.assessment}
              </span>
            </div>
            <div style="font-size:0.78rem; color:#523E28; line-height:1.45;">${m.summary || ''}</div>
            ${citations}
          </div>
        `;
      }).join('');

      const practicalSteps = charm.practical_steps || [];
      const practicalHtml = practicalSteps.map(p => `
        <div style="font-size:0.82rem; color:#523E28; margin-bottom:4px; line-height:1.5;">
          • <strong>Practical Action:</strong> ${p}
        </div>
      `).join('');

      const predId = charm.prediction_id || ('PRED-' + Date.now());

      return `
        <div style="margin-top:16px; background:#FFFFFF; border:1.5px solid rgba(201,162,39,0.38); border-radius:14px; padding:16px 20px; box-shadow:0 3px 12px rgba(180,155,110,0.08);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px; flex-wrap:wrap; gap:6px;">
            <div style="font-family:'Cormorant Garamond',serif; font-size:1.3rem; font-weight:700; color:#8B6914;">
              ✦ Numerology Dasha Event Timing &amp; Consensus Matrix
            </div>
            <span style="font-size:0.72rem; font-weight:700; color:${badge.text}; background:${badge.bg}; border:1px solid ${badge.border}; padding:3px 10px; border-radius:12px;">
              ${badge.label}
            </span>
          </div>

          <div style="font-size:0.85rem; color:#523E28; line-height:1.55; margin-bottom:10px;">
            ${charm.numerology_summary || ''}
          </div>

          <!-- Primary Event Windows -->
          <div style="background:#FAF6EE; border:1px solid rgba(201,162,39,0.25); border-radius:10px; padding:12px 14px; margin-bottom:12px;">
            <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#7A654D;">
              ✦ Primary Calculated Event Windows (Deterministic Dasha)
            </div>
            ${windowsHtml}
          </div>

          <!-- Corroboration Summary -->
          <div style="font-size:0.84rem; color:#523E28; line-height:1.55; margin-bottom:12px; background:#FFFDF7; padding:10px 14px; border-left:3px solid #C9A227; border-radius:6px;">
            <strong style="color:#8B6914;">Independent Method Corroboration:</strong> ${charm.corroboration_summary || ''}
          </div>

          <!-- Cross Method Breakdown -->
          <div style="margin-bottom:12px;">
            <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#7A654D; margin-bottom:6px;">
              ✦ Multi-Method Cross-Verification Analysis
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:8px;">
              ${methodsHtml}
            </div>
          </div>

          <!-- Practical Grounding Steps -->
          ${practicalHtml ? `
            <div style="margin-bottom:12px; background:#FAF6EE; border:1px solid rgba(201,162,39,0.2); border-radius:8px; padding:10px 14px;">
              <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#8B6914; margin-bottom:4px;">
                ✦ Practical Operational Steps (Grounding First)
              </div>
              ${practicalHtml}
            </div>
          ` : ''}

          <!-- Interactive Outcome Verification (Section 10/13) -->
          <div style="margin-top:14px; padding-top:10px; border-top:1px dashed rgba(201,162,39,0.3);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px; margin-bottom:6px;">
              <span style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#7A654D;">
                ✦ Calibrate Prediction Accuracy (Anonymous Verification)
              </span>
              <span style="font-size:0.68rem; font-family:monospace; color:#8B6914;">${predId}</span>
            </div>
            <div style="display:flex; gap:6px; flex-wrap:wrap; align-items:center;">
              <button type="button" onclick="submitCharmOutcome('${predId}', 'OCCURRED_WITHIN_WINDOW')" style="background:#16835B; color:#FFFFFF; border:none; border-radius:6px; padding:5px 9px; font-size:0.74rem; font-weight:600; cursor:pointer;">
                ✓ Manifested in Window
              </button>
              <button type="button" onclick="submitCharmOutcome('${predId}', 'OCCURRED_LATER')" style="background:#C9A227; color:#FFFFFF; border:none; border-radius:6px; padding:5px 9px; font-size:0.74rem; font-weight:600; cursor:pointer;">
                ~ Occurred Later
              </button>
              <button type="button" onclick="submitCharmOutcome('${predId}', 'DID_NOT_OCCUR_WITHIN_WINDOW')" style="background:none; border:1px solid #7A654D; color:#523E28; border-radius:6px; padding:4px 8px; font-size:0.74rem; cursor:pointer;">
                ✗ Did Not Occur
              </button>
              <button type="button" onclick="submitCharmOutcome('${predId}', 'UNSURE')" style="background:none; border:1px solid #C9A227; color:#8B6914; border-radius:6px; padding:4px 8px; font-size:0.74rem; cursor:pointer;">
                ⏳ Pending Window
              </button>
            </div>
            <div id="outcome_feedback_${predId}" style="margin-top:6px; font-size:0.74rem;"></div>
          </div>

          <div style="font-size:0.68rem; color:#7A654D; margin-top:10px; line-height:1.4;">
            <em>Statutory Notice: Numerology Dasha timing represents cyclical potential. In accordance with the Drugs and Magic Remedies Act 1954, insights are lifestyle and reflective attunements only.</em>
          </div>
        </div>
      `;
    }

    async function submitCharmOutcome(predId, status) {
      const feedbackEl = document.getElementById('outcome_feedback_' + predId);
      if (feedbackEl) feedbackEl.innerHTML = `<span style="color:#8B6914;">Recording calibration feedback...</span>`;
      try {
        const resp = await fetch('/api/charm/outcomes', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            prediction_id: predId,
            outcome_status: status,
            user_comment: 'Voluntary verification via Charm AI interface'
          })
        });
        const res = await resp.json();
        if (feedbackEl) {
          feedbackEl.innerHTML = `<span style="color:#16835B; font-weight:600;">✓ Verification recorded for empirical calibration (ID: ${res.outcome_id || 'OK'}). Thank you!</span>`;
        }
      } catch (e) {
        if (feedbackEl) {
          feedbackEl.innerHTML = `<span style="color:#A13030;">Could not save verification: ${e.message}</span>`;
        }
      }
    }
"""

    old_init = "    // Auto-run hydration on load"
    content = content.replace(old_init, charm_card_functions + "\n    // Auto-run hydration on load")

    # 5. Fix dangling code at lines 912-914
    dangling_code = """      var m = document.getElementById('nvNavMenu') || document.getElementById('nv-nav-menu') || document.querySelector('.nv-nav-menu');
      if (m) m.classList.toggle('active');
    }"""
    content = content.replace(dangling_code.replace("\n", "\r\n"), "")
    content = content.replace(dangling_code, "")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    print("Successfully integrated Charm AI frontend into app/static/charm_ai.html")

if __name__ == "__main__":
    update_charm_frontend()
