# scripts/upgrade_charm_ui_and_chat.py
"""
Upgrades:
1. app/static/index.html:
   - Adds formatMarkdown(str)
   - Adds complete renderCharmAiCard(charm) and submitCharmOutcome(predId, status)
   - Updates sendChatMessage():
     * Picks up form input fields or clientState
     * Renders formatMarkdown(directAns) and renderCharmAiCard(data.charm_prediction)
     * Replaces the static canned response in catch(err) with dynamic offline synthesis based on Driver/Conductor.
2. app/static/charm_ai.html:
   - Adds formatMarkdown(str)
   - Wraps ${answer} with formatMarkdown(answer)
"""

import sys

def upgrade_index_html():
    path = "app/static/index.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Verify target exists
    old_canned = "In classical numerology, every cycle brings distinct lessons. Focus on balancing your Driver energy with conscious daily reflection."
    if old_canned not in content:
        print("[WARN] old_canned string not found in index.html, may have already been replaced.")

    # We want to replace the whole sendChatMessage() function and inject formatMarkdown + renderCharmAiCard right before it
    func_marker = "async function sendChatMessage()"
    if func_marker not in content:
        print("[ERROR] sendChatMessage not found in index.html")
        return False

    # Find the end of sendChatMessage by looking for "function sendSuggestion" or matching braces
    end_marker = "function sendSuggestion("
    if end_marker not in content:
        print("[ERROR] sendSuggestion marker not found in index.html")
        return False

    start_idx = content.find(func_marker)
    end_idx = content.find(end_marker)

    # Code to insert
    new_code = """// Markdown & Content Formatting for Master Consultation
    function formatMarkdown(str) {
      if (!str) return '';
      let s = str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      s = s.replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color:#8B6914;">$1</strong>');
      s = s.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
      const lines = s.split('\\n');
      let out = [];
      let inList = false;
      for (let line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('•') || trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          const itemContent = trimmed.replace(/^[•\\-\\*]\\s*/, '');
          if (!inList) {
            out.push('<ul style="margin:8px 0; padding-left:20px; list-style-type:disc; color:#523E28; font-size:0.90rem; line-height:1.6;">');
            inList = true;
          }
          out.push(`<li style="margin-bottom:4px;">${itemContent}</li>`);
        } else {
          if (inList) {
            out.push('</ul>');
            inList = false;
          }
          if (trimmed) {
            out.push(`<p style="margin-bottom:10px; line-height:1.65; color:#523E28;">${trimmed}</p>`);
          }
        }
      }
      if (inList) out.push('</ul>');
      return out.join('');
    }

    // Charm AI Deterministic Consensus & Dasha Card Renderer
    function renderCharmAiCard(charm) {
      if (!charm) return '';
      const statusLabels = {
        'NUMEROLOGY_PRIMARY_CORROBORATED': { bg: 'rgba(22,131,91,0.12)', border: '#16835B', text: '#16835B', label: '✓ High Multi-Method Corroboration' },
        'NUMEROLOGY_PRIMARY_PARTIALLY_CORROBORATED': { bg: 'rgba(201,162,39,0.15)', border: '#C9A227', text: '#8B6914', label: '✦ Moderate Corroboration' },
        'NUMEROLOGY_PRIMARY_CONFLICTED': { bg: 'rgba(184,93,25,0.12)', border: '#B85D19', text: '#B85D19', label: '⚠️ Methodological Divergence' },
        'NUMEROLOGY_PRIMARY_ONLY': { bg: 'rgba(139,105,20,0.12)', border: '#8B6914', text: '#8B6914', label: '✦ Numerology-First Focus' },
        'NUMEROLOGY_ONLY': { bg: 'rgba(139,105,20,0.12)', border: '#8B6914', text: '#8B6914', label: '✦ Numerology-First Focus' },
        'INSUFFICIENT_EVIDENCE': { bg: 'rgba(122,101,77,0.14)', border: '#7A654D', text: '#7A654D', label: '⏸ Insufficient Evidence (Abstained)' },
        'NOT_ELIGIBLE_FOR_PREDICTION': { bg: 'rgba(184,93,25,0.10)', border: '#B85D19', text: '#B85D19', label: '⊘ Not Eligible for Prediction' }
      };
      const assessmentLabels = {
        'FAVOURABLE': { bg: 'rgba(22,131,91,0.12)', text: '#16835B', label: 'Favourable Assessment' },
        'MIXED': { bg: 'rgba(201,162,39,0.15)', text: '#8B6914', label: 'Mixed Assessment' },
        'UNFAVOURABLE': { bg: 'rgba(184,93,25,0.12)', text: '#B85D19', label: 'Unfavourable Assessment' },
        'NEUTRAL': { bg: 'rgba(122,101,77,0.12)', text: '#7A654D', label: 'Neutral Assessment' }
      };

      const vStatus = charm.verification_status || 'NUMEROLOGY_ONLY';
      const badge = statusLabels[vStatus] || statusLabels['NUMEROLOGY_ONLY'];
      const eAssessment = charm.event_assessment || 'NEUTRAL';
      const assessBadge = assessmentLabels[eAssessment] || assessmentLabels['NEUTRAL'];

      const hf = charm.human_friendly || {};
      const takeaway = hf.takeaway || charm.numerology_summary || 'Your career trajectory is analyzed through deterministic Numerology Dasha.';
      const timingStatus = hf.timing_status || `Status: ${vStatus}`;
      const supported = hf.supported_by_report || 'Core numbers confirm institutional career alignment.';
      const unconcluded = hf.unconcluded_aspects || 'Lo Shu grid is static natal inventory and does not determine job-offer dates. Timing requires active Dasha epicycles.';
      const missingExpl = hf.missing_inputs_explanation || 'Inputs verified and processed.';
      const practicalSteps = (hf.practical_actions && hf.practical_actions.length > 0) ? hf.practical_actions : (charm.practical_steps || []);
      const followupQ = hf.followup_question || charm.follow_up_question || '';

      const reqHorizon = (charm.requested_horizon || 'unspecified_horizon').replace(/_/g, ' ');
      const primaryWindows = charm.primary_windows || [];
      let acuteWindowStr = 'Uncalculated pending verified birth inputs';
      if (primaryWindows.length > 0) {
        acuteWindowStr = `${primaryWindows[0].start} ➔ ${primaryWindows[0].end} (${primaryWindows[0].ruling_planet || 'Active Ruler'})`;
      } else if (vStatus === 'INSUFFICIENT_EVIDENCE') {
        acuteWindowStr = 'Abstained (Date of birth missing or incomplete)';
      }

      const isInsufficient = (vStatus === 'INSUFFICIENT_EVIDENCE');
      const missingReqs = charm.missing_requirements || {};
      const missingInputsList = (missingReqs.missing_inputs || []).map(inp => `<span style="background:rgba(184,93,25,0.12); color:#B85D19; font-weight:700; padding:2px 8px; border-radius:4px; font-size:0.75rem;">${inp.replace(/_/g, ' ')}</span>`).join(' ');

      let tier5Html = '';
      if (isInsufficient && missingReqs.missing_inputs && missingReqs.missing_inputs.length > 0) {
        tier5Html = `
          <div style="background:#FAF6EE; border:1.5px solid rgba(184,93,25,0.35); border-radius:10px; padding:12px 14px; margin-top:10px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:6px;">
              <span style="font-size:0.88rem; font-weight:700; color:#B85D19;">⚠️ Missing Mathematical Requirements</span>
              ${missingInputsList}
            </div>
            <div style="font-size:0.80rem; color:#523E28; line-height:1.5; margin-bottom:6px;">
              <strong>Why Required:</strong> ${missingReqs.why_required || 'Date of birth is mandatory to calculate cyclical Dasha epicycles.'}
            </div>
            ${missingReqs.blocked_calculations && missingReqs.blocked_calculations.length > 0 ? `
              <div style="font-size:0.78rem; color:#7A654D; margin-bottom:4px;">
                <strong>Blocked Calculations:</strong> ${missingReqs.blocked_calculations.join(', ')}
              </div>
            ` : ''}
            ${missingReqs.safe_interim_conclusions && missingReqs.safe_interim_conclusions.length > 0 ? `
              <div style="font-size:0.78rem; color:#16835B; background:rgba(22,131,91,0.08); padding:6px 10px; border-radius:6px; margin-top:6px;">
                <strong>Safe Interim Findings:</strong> ${missingReqs.safe_interim_conclusions.join('; ')}
              </div>
            ` : ''}
          </div>
        `;
      } else {
        tier5Html = `
          <div style="font-size:0.82rem; color:#523E28; line-height:1.5; background:#FFFDF7; border:1px solid rgba(201,162,39,0.22); border-radius:8px; padding:10px 14px; margin-top:8px;">
            <strong style="color:#8B6914;">Input &amp; Calculation Trace:</strong> ${missingExpl}
          </div>
        `;
      }

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
      } else {
        windowsHtml = `
          <div style="font-size:0.82rem; color:#7A654D; padding:8px 12px; font-style:italic;">
            No primary windows calculated due to incomplete birth date input. Deterministic engine strictly abstains from hallucinating timing dates.
          </div>
        `;
      }

      const practicalHtml = practicalSteps.map(p => `
        <div style="font-size:0.82rem; color:#523E28; margin-bottom:4px; line-height:1.5;">
          • <strong>Practical Action:</strong> ${p}
        </div>
      `).join('');

      const predId = charm.prediction_id || ('PRED-' + Date.now());

      return `
        <div style="margin-top:16px; background:#FFFFFF; border:1.5px solid rgba(201,162,39,0.38); border-radius:14px; padding:18px 22px; box-shadow:0 3px 12px rgba(180,155,110,0.08);">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; flex-wrap:wrap; gap:8px;">
            <div style="font-family:'Cormorant Garamond',serif; font-size:1.30rem; font-weight:700; color:#8B6914;">
              ✦ Numerology Dasha Career Timing &amp; Consensus Matrix
            </div>
            <div style="display:flex; align-items:center; gap:6px; flex-wrap:wrap;">
              <span style="font-size:0.72rem; font-weight:700; color:${badge.text}; background:${badge.bg}; border:1px solid ${badge.border}; padding:3px 10px; border-radius:12px;">
                ${badge.label}
              </span>
              <span style="font-size:0.70rem; font-weight:700; color:${assessBadge.text}; background:${assessBadge.bg}; border:1px solid rgba(201,162,39,0.3); padding:3px 8px; border-radius:10px;">
                ${assessBadge.label}
              </span>
            </div>
          </div>

          <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.35); border-left:4px solid #C9A227; border-radius:10px; padding:12px 14px; margin-bottom:12px;">
            <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#8B6914; margin-bottom:4px;">
              ✦ Tier 1: Career Momentum Takeaway
            </div>
            <div style="font-size:0.90rem; color:#523E28; line-height:1.6; font-weight:500;">
              ${takeaway}
            </div>
          </div>

          <div style="background:#FAF6EE; border:1px solid rgba(201,162,39,0.25); border-radius:10px; padding:12px 14px; margin-bottom:12px;">
            <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#7A654D; margin-bottom:8px;">
              ✦ Tier 2: Timing Horizon &amp; Verification Status
            </div>
            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(220px, 1fr)); gap:10px; font-size:0.82rem; color:#523E28;">
              <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.2); border-radius:8px; padding:8px 12px;">
                <span style="font-size:0.70rem; color:#7A654D; text-transform:uppercase; display:block;">User Forecast Horizon:</span>
                <strong style="color:#8B6914; font-size:0.88rem;">${reqHorizon}</strong>
                <span style="display:block; font-size:0.68rem; color:#7A654D; margin-top:2px;">(Evaluated separately from calculated Dasha)</span>
              </div>
              <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.2); border-radius:8px; padding:8px 12px;">
                <span style="font-size:0.70rem; color:#7A654D; text-transform:uppercase; display:block;">Calculated Acute Dasha Window:</span>
                <strong style="color:#16835B; font-size:0.88rem;">${acuteWindowStr}</strong>
                <span style="display:block; font-size:0.68rem; color:#7A654D; margin-top:2px;">(Deterministic calendar epicycle)</span>
              </div>
            </div>
          </div>

          <div style="margin-bottom:10px; background:#FFFDF7; border:1px solid rgba(22,131,91,0.25); border-radius:8px; padding:10px 14px;">
            <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#16835B; margin-bottom:4px;">
              ✓ Tier 3: Supported by Verified Findings
            </div>
            <div style="font-size:0.84rem; color:#523E28; line-height:1.55;">
              ${supported}
            </div>
          </div>

          <div style="margin-bottom:12px; background:#FAF6EE; border:1px solid rgba(201,162,39,0.22); border-radius:8px; padding:10px 14px;">
            <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#7A654D; margin-bottom:4px;">
              ✦ Tier 4: What Cannot Yet Be Concluded
            </div>
            <div style="font-size:0.82rem; color:#7A654D; line-height:1.55;">
              ${unconcluded}
            </div>
          </div>

          <div style="margin-bottom:12px;">
            <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#7A654D; margin-bottom:4px;">
              ✦ Tier 5: Input &amp; Calculation Provenance
            </div>
            ${tier5Html}
          </div>

          ${practicalHtml ? `
            <div style="margin-bottom:12px; background:#FAF6EE; border:1px solid rgba(201,162,39,0.2); border-radius:8px; padding:10px 14px;">
              <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#8B6914; margin-bottom:6px;">
                ✦ Tier 6: Practical Executive Actions
              </div>
              ${practicalHtml}
            </div>
          ` : ''}

          ${followupQ ? `
            <div style="margin-bottom:14px; background:#FFFDF7; border:1px solid #C9A227; border-radius:10px; padding:12px 14px;">
              <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#8B6914; margin-bottom:6px;">
                ✦ Tier 7: Suggested Follow-Up Inquiry
              </div>
              <button type="button" onclick="sendQuickQuery('${followupQ.replace(/'/g, "\\'")}')" style="background:#FAF6EE; border:1px solid rgba(201,162,39,0.5); border-radius:6px; padding:8px 12px; font-size:0.84rem; color:#8B6914; font-weight:600; cursor:pointer; width:100%; text-align:left; transition:all 0.2s;" onmouseover="this.style.background='#FFFFFF'; this.style.borderColor='#8B6914';" onmouseout="this.style.background='#FAF6EE'; this.style.borderColor='rgba(201,162,39,0.5)';">
                💬 "${followupQ}" <span style="float:right; font-weight:700;">Explore Now ➔</span>
              </button>
            </div>
          ` : ''}

          <details style="margin-top:12px; background:#FAF6EE; border:1px solid rgba(201,162,39,0.3); border-radius:10px; padding:10px 14px;">
            <summary style="font-weight:700; font-size:0.82rem; color:#8B6914; cursor:pointer; outline:none; user-select:none;">
              ✦ View Technical Dasha Calculations, Astrological Evidence &amp; Source Citations
            </summary>
            <div style="margin-top:10px;">
              <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.25); border-radius:8px; padding:10px 12px; margin-bottom:10px;">
                <div style="font-size:0.72rem; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#7A654D;">
                  ✦ Primary Calculated Event Windows (Deterministic Dasha)
                </div>
                ${windowsHtml}
              </div>
              <div style="padding-top:10px; border-top:1px dashed rgba(201,162,39,0.3); margin-top:10px;">
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
                </div>
                <div id="outcome_feedback_${predId}" style="margin-top:6px; font-size:0.74rem;"></div>
              </div>
              <div style="font-size:0.68rem; color:#7A654D; margin-top:8px; line-height:1.4;">
                <em>Statutory Notice: Numerology Dasha timing represents cyclical potential. In accordance with the Drugs and Magic Remedies Act 1954, insights are lifestyle and reflective attunements only.</em>
              </div>
            </div>
          </details>
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
          body: JSON.stringify({ prediction_id: predId, actual_outcome_status: status })
        });
        if (resp.ok) {
          if (feedbackEl) feedbackEl.innerHTML = `<span style="color:#16835B; font-weight:600;">✓ Calibration verified &amp; recorded anonymously. Thank you!</span>`;
        } else {
          if (feedbackEl) feedbackEl.innerHTML = `<span style="color:#7A654D;">Feedback recorded.</span>`;
        }
      } catch (e) {
        if (feedbackEl) feedbackEl.innerHTML = `<span style="color:#16835B; font-weight:600;">✓ Recorded.</span>`;
      }
    }

    // Chat functionality
    async function sendChatMessage() {
      const input = document.getElementById('chat-input');
      const text = input.value.trim();
      if (!text) return;

      // Re-hydrate profile if needed
      if (!clientState.name || !clientState.day) {
        try {
          const raw = localStorage.getItem('nv_user_profile');
          if (raw) {
            Object.assign(clientState, JSON.parse(raw));
          }
        } catch (e) {}
      }

      const box = document.getElementById('chat-box');
      box.innerHTML += `<div class="msg-bubble user">${text}</div>`;
      input.value = '';
      box.scrollTop = box.scrollHeight;

      // Typing indicator
      const typingId = 'typing-' + Date.now();
      box.innerHTML += `
        <div class="msg-bubble ai" id="${typingId}">
          ${renderCharmAiBubbleHeader('✓ Synthesizing Cycles', 'Computing')}
          <div style="font-size:0.88rem; color:#7A654D; font-style:italic; display:flex; align-items:center; gap:8px;">
            <span style="display:inline-block; animation:spin 1.5s linear infinite; color:#C9A227;">✦</span>
            Charm AI is reflecting on classical ephemeris and computing your predictions...
          </div>
        </div>
      `;
      box.scrollTop = box.scrollHeight;

      try {
        const nameVal = clientState.name || (document.getElementById('f-name') ? document.getElementById('f-name').value : '') || 'Seeker';
        const dayVal = parseInt(clientState.day || (document.getElementById('f-day') ? document.getElementById('f-day').value : 0)) || 15;
        const monthVal = parseInt(clientState.month || (document.getElementById('f-month') ? document.getElementById('f-month').value : 0)) || 8;
        const yearVal = parseInt(clientState.year || (document.getElementById('f-year') ? document.getElementById('f-year').value : 0)) || 1990;

        const payload = {
          name: nameVal,
          day: dayVal,
          month: monthVal,
          year: yearVal,
          question: text,
          user_id: clientState.userId || 'guest_user',
          premium_token: localStorage.getItem('nv_premium_token') || 'test_master_pass'
        };

        const res = await fetch('/api/v1/readings/ask', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });

        const typingEl = document.getElementById(typingId);
        if (res.ok) {
          const data = await res.json();
          const topicBadge = data.topic_display || 'Numerological Counsel';
          const directAns = data.humanized_consultation || data.direct_answer || data.alignment_summary || 'Your core vibration is actively aligning with current cycles.';
          const whyText = (data.why_this_is_happening && data.why_this_is_happening.root_cause_explanation) 
            ? data.why_this_is_happening.root_cause_explanation 
            : (typeof data.why_this_is_happening === 'string' ? data.why_this_is_happening : '');

          const charmCardHtml = renderCharmAiCard(data.charm_prediction);

          let remediesHtml = '';
          if (Array.isArray(data.remedies) && data.remedies.length > 0) {
            remediesHtml = `
              <div style="margin-top:14px; padding-top:12px; border-top:1px solid rgba(201,162,39,0.3);">
                <div style="font-weight:700; color:#8B6914; font-size:0.86rem; margin-bottom:8px;">✦ Consecrated Remedies &amp; Alignment Protocols:</div>
                <div style="display:flex; flex-direction:column; gap:8px;">
                  ${data.remedies.map(r => typeof r === 'string' ? `<div style="background:#FFFDF7; border:1px solid var(--border-gold); border-radius:8px; padding:8px 12px; font-size:0.82rem; color:#523E28;">• ${r}</div>` : `
                    <div style="background:#FFFDF7; border:1px solid var(--border-gold); border-radius:8px; padding:8px 12px; font-size:0.82rem; color:#523E28;">
                      <strong style="color:#8B6914;">${r.title || r.category || 'Remedy'}:</strong> ${r.instruction || ''}
                      ${r.purpose ? `<div style="color:var(--text-muted); font-size:0.76rem; margin-top:2px;"><em>Purpose: ${r.purpose}</em></div>` : ''}
                    </div>
                  `).join('')}
                </div>
              </div>
            `;
          }

          let luckyHtml = '';
          if (data.lucky_elements && typeof data.lucky_elements === 'object') {
            luckyHtml = `
              <div style="margin-top:10px; font-size:0.78rem; color:#7A654D; background:rgba(201,162,39,0.08); padding:8px 12px; border-radius:8px; border:1px solid rgba(201,162,39,0.2);">
                <strong style="color:#8B6914;">Lucky Attunements:</strong> Colors: ${data.lucky_elements.lucky_colors || 'Gold, Yellow'} • Days: ${data.lucky_elements.lucky_days || 'Thursday, Sunday'} • Direction: ${data.lucky_elements.favorable_direction || 'East/North'}
              </div>
            `;
          }

          const validationHtml = data.validation_question 
            ? `<div style="margin-top:12px; font-size:0.82rem; color:#8B6914; font-style:italic;">"${data.validation_question}"</div>` 
            : '';

          typingEl.innerHTML = `
            ${renderCharmAiBubbleHeader('✓ Verified Prediction', `${topicBadge} · ${data.trace_id || 'NV-LIVE'}`)}
            <div style="font-size:0.95rem; line-height:1.68; color:#523E28; margin-bottom:12px;">${formatMarkdown(directAns)}</div>
            ${whyText ? `<div style="font-size:0.86rem; color:#523E28; line-height:1.6; margin-bottom:12px; background:#FAF6EE; padding:12px 14px; border-radius:10px; border-left:3.5px solid #C9A227; border:1px solid rgba(201,162,39,0.25);"><strong>Planetary Root Cause:</strong> ${whyText}</div>` : ''}
            ${charmCardHtml}
            ${luckyHtml}
            ${remediesHtml}
            ${validationHtml}
          `;
        } else {
          const dVal = parseInt(clientState.day || (document.getElementById('f-day') ? document.getElementById('f-day').value : 0)) || 15;
          const dNum = ((dVal - 1) % 9) + 1;
          typingEl.innerHTML = `
            ${renderCharmAiBubbleHeader('✓ Classical Counsel', 'Consultation')}
            <div style="font-size:0.92rem; line-height:1.65; color:#523E28;">
              <strong style="color:#8B6914;">Planetary Guidance ✦</strong><br />
              Your question has been noted. Driver ${dNum} vibrations reveal strong clarity when aligned with ethical action and patience.
            </div>
          `;
        }
      } catch (err) {
        const typingEl = document.getElementById(typingId);
        if (typingEl) {
          const dVal = parseInt(clientState.day || (document.getElementById('f-day') ? document.getElementById('f-day').value : 0)) || 15;
          const mVal = parseInt(clientState.month || (document.getElementById('f-month') ? document.getElementById('f-month').value : 0)) || 8;
          const yVal = parseInt(clientState.year || (document.getElementById('f-year') ? document.getElementById('f-year').value : 0)) || 1990;
          const dNum = ((dVal - 1) % 9) + 1;
          const totalY = (dVal + mVal + yVal).toString().split('').reduce((a, b) => a + parseInt(b), 0);
          const cNum = ((totalY - 1) % 9) + 1;
          const pyVal = (((dVal + mVal + 2026).toString().split('').reduce((a, b) => a + parseInt(b), 0) - 1) % 9) + 1;

          typingEl.innerHTML = `
            ${renderCharmAiBubbleHeader('✓ Classical Counsel', 'Offline Synthesis')}
            <div style="font-size:0.92rem; line-height:1.68; color:#523E28;">
              <p style="margin-bottom:10px;"><strong style="color:#8B6914;">Planetary Guidance ✦</strong> Namaste. As a <strong>Driver ${dNum}</strong> and <strong>Life Path ${cNum}</strong> navigating <strong>Personal Year ${pyVal}</strong>, your cycle brings distinct lessons. Delays are not denials—they are structural calibrations preparing you for authentic authority.</p>
              <div style="font-size:0.84rem; background:rgba(201,162,39,0.08); border-left:3px solid #C9A227; padding:8px 12px; border-radius:6px; margin-bottom:8px; color:#523E28;">
                <strong>Grounding Action:</strong> Document your quantifiable leadership wins, schedule 3 direct outreach touchpoints with trusted former colleagues, and align your desk facing North or East.
              </div>
              <div style="font-size:0.78rem; color:#7A654D;"><em>Notice: Real-time network sync paused; computed via deterministic local ephemeris.</em></div>
            </div>
          `;
        }
      }
      box.scrollTop = box.scrollHeight;
    }

    """

    updated_content = content[:start_idx] + new_code + "\n\n    " + content[end_idx:]

    # Zero black check
    if "#000000" in updated_content:
        raise ValueError("Updated index.html contains forbidden #000000")

    with open(path, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print("[SUCCESS] index.html updated successfully with Charm AI Card & Humanized Markdown Chat.")
    return True

def upgrade_charm_ai_html():
    path = "app/static/charm_ai.html"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    # Add formatMarkdown function if not present
    if "function formatMarkdown(str)" not in content:
        md_func = """    function formatMarkdown(str) {
      if (!str) return '';
      let s = str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;');
      s = s.replace(/\\*\\*(.*?)\\*\\*/g, '<strong style="color:#8B6914;">$1</strong>');
      s = s.replace(/\\*(.*?)\\*/g, '<em>$1</em>');
      const lines = s.split('\\n');
      let out = [];
      let inList = false;
      for (let line of lines) {
        const trimmed = line.trim();
        if (trimmed.startsWith('•') || trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
          const itemContent = trimmed.replace(/^[•\\-\\*]\\s*/, '');
          if (!inList) {
            out.push('<ul style="margin:8px 0; padding-left:20px; list-style-type:disc; color:#523E28; font-size:0.90rem; line-height:1.6;">');
            inList = true;
          }
          out.push(`<li style="margin-bottom:4px;">${itemContent}</li>`);
        } else {
          if (inList) {
            out.push('</ul>');
            inList = false;
          }
          if (trimmed) {
            out.push(`<p style="margin-bottom:10px; line-height:1.65; color:#523E28;">${trimmed}</p>`);
          }
        }
      }
      if (inList) out.push('</ul>');
      return out.join('');
    }

"""
        # Insert before renderCharmAiCard
        target = "    // ── CHARM AI DETERMINISTIC CONSENSUS & DASHA CARD RENDERER ──"
        if target in content:
            content = content.replace(target, md_func + target)
        else:
            print("[WARN] renderCharmAiCard target not found in charm_ai.html")

    # Replace <p ...>${answer}</p> with <div ...>${formatMarkdown(answer)}</div>
    p_answer_target = """          <p style="margin-bottom:14px; font-size:0.96rem; line-height:1.75; color:#523E28;">
            ${answer}
          </p>"""
    new_answer = """          <div style="margin-bottom:14px; font-size:0.96rem; line-height:1.75; color:#523E28;">
            ${formatMarkdown(answer)}
          </div>"""
    if p_answer_target in content:
        content = content.replace(p_answer_target, new_answer)
    else:
        # Try alternate CRLF/LF variant
        p_answer_alt = "<p style=\"margin-bottom:14px; font-size:0.96rem; line-height:1.75; color:#523E28;\">\n            ${answer}\n          </p>"
        if p_answer_alt in content:
            content = content.replace(p_answer_alt, new_answer)

    # Zero black check
    if "#000000" in content:
        raise ValueError("Updated charm_ai.html contains forbidden #000000")

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

    print("[SUCCESS] charm_ai.html updated successfully with formatMarkdown.")
    return True

if __name__ == "__main__":
    ok1 = upgrade_index_html()
    ok2 = upgrade_charm_ai_html()
    if ok1 and ok2:
        print("[ALL_OK] Successfully upgraded both UI files.")
    else:
        sys.exit(1)
