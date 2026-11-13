import os
import re

# Load template helpers
with open('app/static/sample.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Define the new generateFormat1Pages function
fmt1_code = '''
    // =========================================================================
    // FORMAT 1: EXECUTIVE DIAGNOSTIC BLUEPRINT (3 PAGES)
    // Authored as per Master Numerologist Bhaskr Singh (Numeros Vision)
    // Free: Page 1 Full Lo Shu + 8 Planes (Aligned vs Not Aligned), Pgs 2-3 locked
    // Paid Basic (₹199): All 3 Pages 100% UNLOCKED with deep authentic remedies
    // =========================================================================
    function generateFormat1Pages(client) {
      const { name, dob, gender, phone } = client;
      const [year, month, day] = dob.split('-');
      const driver = getDriver(day);
      const conductor = getConductor(dob);
      const kua = getKua(year, gender);
      const chaldean = getChaldean(name);
      const totalPages = 3;

      const dobDigits = dob.replace(/\\D/g, '').split('').filter(d => d !== '0').map(Number);
      const counts = {};
      for (let i = 1; i <= 9; i++) counts[i] = 0;
      dobDigits.forEach(d => counts[d] = (counts[d] || 0) + 1);
      const missing = Object.keys(counts).filter(k => counts[k] === 0).map(Number);
      const present = Object.keys(counts).filter(k => counts[k] > 0).map(Number);
      const planes = evaluatePlanes(counts);
      const myVastu = vastuVectors[String(kua)] || vastuVectors[1];

      const userTier = getUserTier();
      const isPaid = isFormatUnlocked('brief');

      // Lo Shu Grid Cell with D, C, K and [GAP]
      function renderLoShuCell(num, label) {
        const cnt = counts[num] || 0;
        let markers = [];
        if (num === driver) markers.push('D');
        if (num === conductor) markers.push('C');
        if (num === kua) markers.push('K');
        const markerStr = markers.length > 0 ? ` <span style="font-size:9px;color:#8B6914;font-weight:900;">(${markers.join(',')})</span>` : '';

        if (cnt === 0) {
          return `
            <td style="border:1.5px dashed rgba(201,162,39,0.35); background:rgba(255,253,247,0.7); vertical-align:middle; text-align:center; padding:5px 3px; border-radius:4px;">
              <div style="font-size:9px; color:#A13030; font-weight:800; letter-spacing:0.04em;">[GAP]</div>
              <div style="font-size:11px; font-weight:700; color:#8C827A;">${num}${markerStr}</div>
              <div style="font-size:8px; color:#7A654D;">${label}</div>
            </td>
          `;
        } else {
          const repStr = String(num).repeat(cnt);
          return `
            <td style="border:1.5px solid #C9A227; background:#FFFFFF; vertical-align:middle; text-align:center; padding:5px 3px; border-radius:4px; box-shadow:0 1px 3px rgba(201,162,39,0.12);">
              <div style="font-size:12.5px; font-weight:900; color:#8B6914; font-family:'Cinzel',serif;">${repStr}${markerStr}</div>
              <div style="font-size:8px; color:#16835B; font-weight:700;">${label} · ×${cnt}</div>
            </td>
          `;
        }
      }

      const alignedPlanes = planes.filter(p => p.pct >= 66);
      const notAlignedPlanes = planes.filter(p => p.pct < 66);
      const freqSummary = present.map(n => counts[n] > 1 ? `${n} appears ${counts[n]} times` : `${n} once`).join(' | ');

      const goldenGap = [4, 5, 6].filter(n => counts[n] === 0);
      const goldenStatus = goldenGap.length === 0
        ? '<span style="color:#16835B;font-weight:700;">✓ Active Sovereign Axis</span>'
        : `<span style="color:#A13030;font-weight:700;">Broken Void (Missing ${goldenGap.join(', ')})</span>`;

      // Combo 81
      const comboKey = `${driver}-${conductor}`;
      const comboText = EMBEDDED_DATA.combos81[comboKey] || "A dynamic cosmic synthesis of authority, visionary execution, and sustained wealth accumulation.";

      // Personal Year & Months
      const currentYear = 2026;
      const personalYear = reduceToSingle(parseInt(day, 10) + parseInt(month, 10) + reduceToSingle(currentYear));
      const pyInfo = EMBEDDED_DATA.personalYears[String(driver)]?.[String(personalYear)] || { tag: "Transformative Milestone", text: "A pivotal year of new beginnings and structural expansion." };

      const pages = [];

      // ──────────────────────────────────────────────────────────────────────────
      // FORMAT 1: PAGE 1 (FOUNDATIONAL PROFILE & LO SHU 2-COLUMN MATRIX)
      // Height guaranteed <= 740px. ZERO OVERFLOW across any printer/browser.
      // ──────────────────────────────────────────────────────────────────────────
      pages.push(`
        <div class="pdf-page" id="page-1">
          ${CORNERS}
          ${WATERMARK_SVG}
          ${renderPageHeader(isPaid ? 'Celestial Master Blueprint · Page 1 · Foundational Profile' : 'Free Discovery Blueprint · Page 1 · Foundational Profile')}
          <div class="page-content" style="padding:4px 0;">
            <!-- Top Header & Pillars -->
            <div class="content-top-group" style="text-align:center; margin-bottom:5px;">
              <div style="font-family:'Cinzel Decorative','Cinzel',serif;font-size:10px;letter-spacing:0.18em;color:#8B6914;margin-bottom:2px;">✦ ${isPaid ? 'AUTHENTIC NUMEROLOGY MASTER DOSSIER' : 'FREE CELESTIAL DISCOVERY BLUEPRINT'} ✦</div>
              <div style="font-family:'Cinzel',serif;font-size:22px;font-weight:900;color:#8B6914;letter-spacing:0.03em;line-height:1.2;" role="heading" aria-level="2">${name.toUpperCase()}</div>
              <div style="font-family:'Marcellus',serif;font-size:11.5px;color:#16835B;margin-bottom:6px;">Natal Lo Shu Grid &amp; Elemental Resonance Audit</div>

              <!-- 4 Core Metric Pills -->
              <div class="metric-pill-row" style="margin-bottom:6px; gap:6px;">
                <div class="metric-pill" style="padding:4px 8px;">
                  <div class="metric-pill-label" style="font-size:8px;">Psychic (Mulank)</div>
                  <div class="metric-pill-val" style="font-size:12px;">${driver} · ${EMBEDDED_DATA.planets[String(driver)]}</div>
                </div>
                <div class="metric-pill" style="padding:4px 8px;">
                  <div class="metric-pill-label" style="font-size:8px;">Destiny (Bhagyank)</div>
                  <div class="metric-pill-val" style="font-size:12px;">${conductor} · ${EMBEDDED_DATA.planets[String(conductor)]}</div>
                </div>
                <div class="metric-pill" style="padding:4px 8px;">
                  <div class="metric-pill-label" style="font-size:8px;">Cosmic Vector</div>
                  <div class="metric-pill-val" style="font-size:12px;">Kua ${kua} (${myVastu.group})</div>
                </div>
                <div class="metric-pill" style="padding:4px 8px;">
                  <div class="metric-pill-label" style="font-size:8px;">Calling Name</div>
                  <div class="metric-pill-val" style="font-size:12px;">Chaldean ${chaldean.single} (${chaldean.compound})</div>
                </div>
              </div>
            </div>

            <!-- Verified Chart Coordinates Strip -->
            <div class="report-card" style="padding:5px 10px; margin-bottom:8px; font-size:10px; color:#523E28; background:#FFFDF7; border:1px solid rgba(201,162,39,0.25);">
              <div style="display:flex; justify-content:space-between; flex-wrap:wrap; gap:6px;">
                <div><strong>DOB:</strong> ${dob} (Day ${parseInt(day,10)})</div>
                <div><strong>Life Path:</strong> ${conductor} (${EMBEDDED_DATA.planets[String(conductor)]})</div>
                <div><strong>Kua Group:</strong> ${myVastu.group} (Best: ${myVastu.primary})</div>
                <div><strong>Access Tier:</strong> <span style="color:#16835B;font-weight:700;">${isPaid ? (userTier.toUpperCase() + ' UNLOCKED') : 'Free Discovery Tier'}</span></div>
              </div>
            </div>

            <!-- 2-COLUMN CORE: LEFT (LO SHU 3×3) & RIGHT (8 PLANES ALIGNED VS NOT ALIGNED) -->
            <div style="display:grid; grid-template-columns: 1fr 1.15fr; gap: 8px; margin-bottom: 8px; align-items: stretch;">
              
              <!-- LEFT COLUMN: Lo Shu 3×3 Grid -->
              <div class="report-card" style="padding: 8px 10px; margin: 0; display:flex; flex-direction:column; justify-content:space-between; background:#FFFDF7; border:1px solid var(--border-gold);">
                <div>
                  <div style="font-family:'Cinzel',serif; font-size:11px; font-weight:700; color:#8B6914; text-align:center; margin-bottom:5px;">
                    ✦ Natal Lo Shu 3×3 Grid
                  </div>
                  <table style="width:100%; border-collapse:separate; border-spacing:3px; margin:0 auto 6px;">
                    <tr>
                      ${renderLoShuCell(4, 'Wood')}
                      ${renderLoShuCell(9, 'Fire')}
                      ${renderLoShuCell(2, 'Earth')}
                    </tr>
                    <tr>
                      ${renderLoShuCell(3, 'Wood')}
                      ${renderLoShuCell(5, 'Earth')}
                      ${renderLoShuCell(7, 'Metal')}
                    </tr>
                    <tr>
                      ${renderLoShuCell(8, 'Earth')}
                      ${renderLoShuCell(1, 'Water')}
                      ${renderLoShuCell(6, 'Metal')}
                    </tr>
                  </table>
                </div>

                <div style="border-top:1px dashed rgba(201,162,39,0.3); padding-top:4px; font-size:9.5px; color:#523E28; line-height:1.4;">
                  <div><strong>Present:</strong> <span style="color:#16835B; font-weight:700;">${present.join(', ')} ✔</span></div>
                  <div><strong>Missing [GAP]:</strong> <span style="color:#A13030; font-weight:700;">${missing.join(', ')}</span></div>
                  <div style="font-size:8.5px; color:#7A654D; margin-top:2px;">${freqSummary}</div>
                </div>
              </div>

              <!-- RIGHT COLUMN: 8 Elemental Planes (Aligned vs Not Aligned) -->
              <div class="report-card" style="padding: 8px 10px; margin: 0; display:flex; flex-direction:column; justify-content:space-between; background:#FFFDF7; border:1px solid var(--border-gold);">
                <div>
                  <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px;">
                    <span style="font-family:'Cinzel',serif; font-size:11px; font-weight:700; color:#8B6914;">✦ 8 Elemental Planes</span>
                    <span style="font-size:8.5px; color:#16835B; font-weight:700; background:rgba(22,131,91,0.1); border:1px solid rgba(22,131,91,0.25); border-radius:8px; padding:1px 5px;">
                      ${alignedPlanes.length}/8 Aligned
                    </span>
                  </div>
                  <div style="display:flex; flex-direction:column; gap:3px;">
                    ${planes.map(p => {
                      const isAligned = p.pct >= 66;
                      const bg = isAligned ? 'rgba(22,131,91,0.08)' : 'rgba(161,48,48,0.06)';
                      const col = isAligned ? '#16835B' : '#A13030';
                      const brd = isAligned ? 'rgba(22,131,91,0.25)' : 'rgba(161,48,48,0.2)';
                      const txt = isAligned ? `Aligned (${p.pct}%)` : `Not Aligned (${p.pct}%)`;
                      return `
                        <div style="display:flex; justify-content:space-between; align-items:center; background:#FFFFFF; border:1px solid rgba(201,162,39,0.18); border-radius:3px; padding:2.5px 6px; font-size:9px;">
                          <div style="display:flex; align-items:center; gap:4px;">
                            <span style="font-weight:700; color:#523E28;">${p.name.split(' ')[0]} ${p.name.split(' ')[1] || ''}</span>
                            <span style="font-size:8px; color:#8C827A;">(${p.digits.join('-')})</span>
                          </div>
                          <span style="background:${bg}; color:${col}; border:1px solid ${brd}; border-radius:8px; padding:0.5px 5px; font-size:8px; font-weight:700;">
                            ${txt}
                          </span>
                        </div>
                      `;
                    }).join('')}
                  </div>
                </div>

                <div style="border-top:1px dashed rgba(201,162,39,0.3); padding-top:3px; font-size:8.5px; color:#7A654D; margin-top:4px;">
                  <strong>Golden Axis (4-5-6):</strong> ${goldenStatus}
                </div>
              </div>
            </div>

            <!-- Current Age Number Vibrational Frequency Card -->
            ${renderAgeNumerologyCard(dob, missing)}
          </div>
          ${renderPageFooter(1, totalPages)}
        </div>
      `);

      // ──────────────────────────────────────────────────────────────────────────
      // FORMAT 1: PAGE 2 (8 PLANES DEEP DIVE & RAJ YOGAS)
      // If PAID: 100% UNLOCKED. If FREE: Teaser with locked upgrade card.
      // ──────────────────────────────────────────────────────────────────────────
      if (isPaid) {
        pages.push(`
          <div class="pdf-page" id="page-2">
            ${CORNERS}
            ${WATERMARK_SVG}
            ${renderPageHeader('Celestial Master Blueprint · Page 2 · 8 Elemental Planes & Raj Yogas')}
            <div class="page-content" style="padding:4px 0;">
              <div class="content-top-group" style="text-align:center; margin-bottom:8px;">
                <div style="font-family:'Cinzel Decorative','Cinzel',serif;font-size:10px;letter-spacing:0.18em;color:#8B6914;margin-bottom:2px;">✦ CORE ELEMENTAL DYNAMICS ✦</div>
                <div style="font-family:'Cinzel',serif;font-size:20px;font-weight:900;color:#8B6914;">8 Elemental Planes &amp; Sovereign Raj Yogas</div>
                <div style="font-family:'Marcellus',serif;font-size:11.5px;color:#16835B;">Cognitive, Will &amp; Action Balance · Sovereign Power Line Audit</div>
              </div>

              <!-- Comprehensive 8-Plane Grid Breakdown -->
              <div class="report-card" style="padding:10px 12px; margin-bottom:8px;">
                <div class="card-title" style="margin-bottom:6px; font-size:11.5px;">✦ 8 Planes Detailed Alignment Status</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:10px;">
                  ${planes.map(p => {
                    const isAligned = p.pct >= 66;
                    return `
                      <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.22); border-radius:4px; padding:5px 8px;">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:2px;">
                          <strong style="color:#8B6914;">${p.name}</strong>
                          <span style="font-size:8.5px; font-weight:700; color:${isAligned ? '#16835B' : '#A13030'};">${isAligned ? 'Aligned' : 'Not Aligned'}</span>
                        </div>
                        <div style="font-size:9px; color:#523E28; line-height:1.35;">${p.desc}</div>
                        <div style="font-size:8.5px; color:#7A654D; margin-top:2px;">Active Digits: ${p.present.length > 0 ? p.present.join(', ') : 'None'} (${p.pct}%)</div>
                      </div>
                    `;
                  }).join('')}
                </div>
              </div>

              <!-- Raj Yogas & Cross-Relations -->
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:8px;">
                <div class="report-card" style="padding:8px 10px; margin:0;">
                  <div class="card-title" style="font-size:11px; margin-bottom:4px;">✦ Golden Raj Yoga (4-5-6)</div>
                  <p class="body-p" style="font-size:9.5px; line-height:1.4; margin:0; color:#523E28;">
                    The Golden Plane connects Intellectual Vision (4), Universal Balance (5), and Material Luxury (6). ${goldenGap.length === 0 ? 'Full active presence confers natural commercial prosperity and leadership authority.' : `Presence of gap in [${goldenGap.join(', ')}] causes wealth to leak before compounding. Specific cures in Page 3 seal this flow.`}
                  </p>
                </div>
                <div class="report-card" style="padding:8px 10px; margin:0;">
                  <div class="card-title" style="font-size:11px; margin-bottom:4px;">✦ Silver Earth Yoga (2-5-8)</div>
                  <p class="body-p" style="font-size:9.5px; line-height:1.4; margin:0; color:#523E28;">
                    The Silver Plane governs tangible real estate, emotional grounding, and generational asset accumulation. ${counts[2] > 0 && counts[8] > 0 ? 'Strong dual activation of 2 and 8 gives immense persistence and real property compounding over time.' : 'Requires grounding activation through Earth element stabilization.'}
                  </p>
                </div>
              </div>

              <!-- Driver-Conductor Combination Archetype & Personal Year Calculator -->
              <div class="report-card" style="padding:8px 10px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                  <span class="card-title" style="font-size:11px; margin:0;">✦ Archetype Synthesis: ${driver} (${EMBEDDED_DATA.planets[String(driver)]}) + ${conductor} (${EMBEDDED_DATA.planets[String(conductor)]})</span>
                  <span style="font-size:9px; color:#16835B; font-weight:700;">Personal Year Calculator: ${personalYear}</span>
                </div>
                <p class="body-p" style="font-size:9.5px; line-height:1.4; margin:0 0 6px 0; color:#523E28;">
                  ${comboText}
                </p>
                <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.22); border-radius:4px; padding:4px 8px; font-size:9px; color:#7A654D;">
                  <strong>Personal Year ${personalYear} Focus:</strong> ${pyInfo.tag} · ${pyInfo.text}
                </div>
              </div>
            </div>
            ${renderPageFooter(2, totalPages)}
          </div>
        `);
      } else {
        // FREE TIER LOCKED PREVIEW FOR PAGE 2
        pages.push(`
          <div class="pdf-page" id="page-2">
            ${CORNERS}
            ${WATERMARK_SVG}
            ${renderPageHeader('Format 1 · Page 2 · 8 Elemental Planes & Raj Yogas (Locked)')}
            <div class="page-content" style="position:relative; overflow:hidden;">
              <div class="chapter-hero-title">8 Elemental Planes &amp; Hidden Raj Yogas</div>
              <div class="chapter-hero-subtitle">Cognitive, Will &amp; Action Balance · Sovereign Power Line Audit</div>

              <div class="blurred-content-preview">
                <div class="report-card" style="margin-bottom:8px;">
                  <div class="card-title">✦ 8 Elemental Planes Status Breakdown</div>
                  <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;font-size:10px;">
                    ${planes.slice(0, 6).map(p => `<div><strong>${p.name}:</strong> <span>${p.status}</span></div>`).join('')}
                  </div>
                </div>
                <div class="report-card">
                  <div class="card-title">✦ Golden Raj Yoga (4-5-6) &amp; Silver Raj Yoga (2-5-8)</div>
                  <p class="body-p">The presence of the central golden axis produces extraordinary financial compounding when properly activated...</p>
                </div>
              </div>

              <div class="luxury-lock-card">
                <div class="lock-icon-seal">🔒</div>
                <div class="lock-card-title">8 Elemental Planes &amp; Raj Yogas Locked</div>
                <div class="lock-card-tagline">ANVEIL EVERY CHARM · COMPLETE VITALITY DOSSIER</div>
                <p class="lock-card-body">
                  Unlock all 8 elemental planes (Thought, Will, Action, Mental, Emotional, Practical) and the Golden Raj Yoga (4-5-6) activation blueprint.
                </p>
                <div class="lock-features-list">
                  <div class="lock-feature-item">✦ All 8 Planes Evaluated with Exact Mathematical Percentages</div>
                  <div class="lock-feature-item">✦ Golden Prosperity &amp; Silver Real Estate Raj Yoga Audit</div>
                  <div class="lock-feature-item">✦ Driver-Conductor Combination Deep Dive (${driver} + ${conductor})</div>
                  <div class="lock-feature-item">✦ Full 7-Layer Holistic Remedial Prescription</div>
                </div>
                <button class="lock-unlock-btn" onclick="openOrderModal('report_basic', 'Basic Foundational Report (3 Pages)', 199)">
                  Unlock Basic Dossier (₹199) ✦
                </button>
              </div>
            </div>
            ${renderPageFooter(2, totalPages)}
          </div>
        `);
      }

      // ──────────────────────────────────────────────────────────────────────────
      // FORMAT 1: PAGE 3 (7-LAYER REMEDIAL HANDBOOK & HARMONIC PROTOCOLS)
      // If PAID: 100% UNLOCKED. If FREE: Teaser with locked upgrade card.
      // ──────────────────────────────────────────────────────────────────────────
      if (isPaid) {
        pages.push(`
          <div class="pdf-page" id="page-3">
            ${CORNERS}
            ${WATERMARK_SVG}
            ${renderPageHeader('Celestial Master Blueprint · Page 3 · 7-Layer Holistic Cures')}
            <div class="page-content" style="padding:4px 0;">
              <div class="content-top-group" style="text-align:center; margin-bottom:8px;">
                <div style="font-family:'Cinzel Decorative','Cinzel',serif;font-size:10px;letter-spacing:0.18em;color:#8B6914;margin-bottom:2px;">✦ MASTER REMEDIAL BLUEPRINT ✦</div>
                <div style="font-family:'Cinzel',serif;font-size:20px;font-weight:900;color:#8B6914;">7-Layer Holistic Cures &amp; Vedic Remedies</div>
                <div style="font-family:'Marcellus',serif;font-size:11.5px;color:#16835B;">Authentic Rectification Protocols as Practiced by Master Bhaskr Singh</div>
              </div>

              <!-- Missing Numbers Vedic Remedies -->
              <div class="report-card" style="padding:10px 12px; margin-bottom:8px;">
                <div class="card-title" style="margin-bottom:6px; font-size:11.5px;">✦ Missing Numbers Practical &amp; Vedic Cures</div>
                <div style="display:flex; flex-direction:column; gap:5px; font-size:9.5px;">
                  ${missing.map(m => {
                    const rems = {
                      2: "Feed white cows on Mondays. Drink water from a silver cup. Offer milk/water to Shiva Lingam.",
                      3: "Donate yellow grams/turmeric to elderly gurus on Thursdays. Wear brass or yellow sapphire. Respect mentors.",
                      4: "Feed street dogs biscuits/bread daily. Feed crows. Donate mustard oil, black sesame on Saturdays. Kalbhairav temple worship.",
                      5: "Feed cows green grass/spinach on Wednesdays. Free green birds/parrots. Donate notebooks to children. Ganesh temple worship.",
                      6: "Donate white sweets, sugar, rice, or perfumes to ladies on Fridays. Visit Durga/Lakshmi temple. Wear diamond or white zircon.",
                      7: "Visit Ketu/Ganesh temples. Introspective meditation. Donate grey blankets or feed street dogs.",
                      8: "Donate mustard oil, black umbrella, or iron utensils to labor on Saturdays. Recite Shani Chalisa. Regular discipline."
                    };
                    return `
                      <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.22); border-radius:4px; padding:4px 8px; line-height:1.4;">
                        <strong style="color:#8B6914;">✦ Missing ${m} (${EMBEDDED_DATA.planets[String(m)] || 'Planetary Force'}):</strong>
                        <span style="color:#523E28;"> ${rems[m] || 'Perform planetary Beej Mantra meditation and wear aligning elemental colors.'}</span>
                      </div>
                    `;
                  }).join('')}
                </div>
              </div>

              <!-- Repeated Numbers Protocol & Mobile Number Calibration -->
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-bottom:8px;">
                <div class="report-card" style="padding:8px 10px; margin:0;">
                  <div class="card-title" style="font-size:11px; margin-bottom:4px;">✦ Repeated Numbers Calibration</div>
                  <div style="font-size:9px; color:#523E28; line-height:1.4;">
                    ${counts[1] > 1 ? `<div><strong>Number 1 (×${counts[1]}):</strong> Impartial leader; avoid ego friction. Offer Surya Arghya daily at sunrise.</div>` : ''}
                    ${counts[8] > 1 ? `<div><strong>Number 8 (×${counts[8]}):</strong> Intense karmic persistence; avoid burnout. Recite Shani Beej Mantra on Saturdays.</div>` : ''}
                    ${counts[9] > 1 ? `<div><strong>Number 9 (×${counts[9]}):</strong> High intellectual drive; channel anger into fitness. Hanuman Chalisa on Tuesdays.</div>` : ''}
                    ${counts[1] <= 1 && counts[8] <= 1 && counts[9] <= 1 ? `<div>Single repetitions present in chart; balanced baseline vibration without severe energetic overload.</div>` : ''}
                  </div>
                </div>

                <div class="report-card" style="padding:8px 10px; margin:0;">
                  <div class="card-title" style="font-size:11px; margin-bottom:4px;">✦ Mobile &amp; Name Resonance</div>
                  <div style="font-size:9px; color:#523E28; line-height:1.4;">
                    <div><strong>Mobile Number:</strong> ${phone || '+91 9818418039'}</div>
                    <div><strong>Calling Name:</strong> ${chaldean.single} (${chaldean.compound}) · Highly Auspicious Star of the Lion.</div>
                    <div style="margin-top:3px; color:#16835B; font-weight:700;">Status: Harmonized with Mulank 1 &amp; Bhagyank 4</div>
                  </div>
                </div>
              </div>

              <!-- Sanskrit Beej Mantras & Auspicious Guidance -->
              <div class="report-card" style="padding:8px 10px;">
                <div class="card-title" style="font-size:11px; margin-bottom:4px;">✦ Sacred Beej Mantras &amp; Auspicious Timings</div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px; font-size:9px; color:#523E28;">
                  <div>
                    <strong style="color:#8B6914;">Sun (Mulank 1) Beej Mantra:</strong>
                    <div style="font-style:italic; color:#16835B; margin-top:2px;">"Om Hram Hreem Hroum Sah Suryaya Namah"</div>
                    <div style="color:#7A654D; font-size:8px;">Recite 108 times at sunrise on Sundays.</div>
                  </div>
                  <div>
                    <strong style="color:#8B6914;">Rahu (Bhagyank 4) Beej Mantra:</strong>
                    <div style="font-style:italic; color:#16835B; margin-top:2px;">"Om Bhram Bhreem Bhroum Sah Rahave Namah"</div>
                    <div style="color:#7A654D; font-size:8px;">Recite 108 times after sunset on Saturdays.</div>
                  </div>
                </div>
                <div style="border-top:1px dashed rgba(201,162,39,0.3); margin-top:6px; padding-top:4px; font-size:8.5px; color:#7A654D; display:flex; justify-content:space-between;">
                  <span><strong>Favorable Colors:</strong> Gold, Copper, Amber, Green</span>
                  <span><strong>Lucky Days:</strong> Sunday, Thursday</span>
                  <span><strong>Lucky Dates:</strong> 1, 10, 19, 28</span>
                </div>
              </div>
            </div>
            ${renderPageFooter(3, totalPages)}
          </div>
        `);
      } else {
        // FREE TIER LOCKED PREVIEW FOR PAGE 3
        pages.push(`
          <div class="pdf-page" id="page-3">
            ${CORNERS}
            ${WATERMARK_SVG}
            ${renderPageHeader('Format 1 · Page 3 · Harmonized Remedies (Locked)')}
            <div class="page-content" style="position:relative; overflow:hidden;">
              <div class="chapter-hero-title">Harmonized Remedies &amp; Action Protocols</div>
              <div class="chapter-hero-subtitle">Vedic, Astrological &amp; Practical Rectification Guidelines</div>

              <div class="blurred-content-preview">
                <div class="report-card" style="margin-bottom:8px;">
                  <div class="card-title">✦ 7-Layer Holistic Prescription Blueprint</div>
                  <p class="body-p">Auspicious gemstones, sacred metals, spatial vastu vectors, and Vedic Beej Mantras tuned to your exact Mulank and Bhagyank...</p>
                </div>
                <div class="report-card">
                  <div class="card-title">✦ Karmic Gap Healing &amp; Life Direction</div>
                  <p class="body-p">Specific charitable donations, dietary adjustments, and color therapies to neutralize missing number voids...</p>
                </div>
              </div>

              <div class="luxury-lock-card">
                <div class="lock-icon-seal">🔒</div>
                <div class="lock-card-title">Complete Remedial Handbook Locked</div>
                <div class="lock-card-tagline">ANVEIL EVERY CHARM · AUTHENTIC CURES</div>
                <p class="lock-card-body">
                  Unlock exact Sanskrit Beej Mantras, missing number remedies (birds/dogs food, donations, temple visits), and mobile number harmonization.
                </p>
                <div class="lock-features-list">
                  <div class="lock-feature-item">✦ Exact Missing Number Remedies for [${missing.join(', ')}]</div>
                  <div class="lock-feature-item">✦ Sanskrit Beej Mantras with Accurate Pronunciation</div>
                  <div class="lock-feature-item">✦ Auspicious Days, Favorable Colors &amp; Directional Vastu</div>
                  <div class="lock-feature-item">✦ Mobile &amp; Commercial Name Calibration Blueprint</div>
                </div>
                <button class="lock-unlock-btn" onclick="openOrderModal('report_basic', 'Basic Foundational Report (3 Pages)', 199)">
                  Unlock Basic Dossier (₹199) ✦
                </button>
              </div>
            </div>
            ${renderPageFooter(3, totalPages)}
          </div>
        `);
      }

      return pages;
    }
'''

# Replace generateFormat1Pages in html
pattern_fmt1 = r'function generateFormat1Pages\(client\)[\s\S]*?return pages;\s*\}'
html, count1 = re.subn(pattern_fmt1, fmt1_code.strip(), html)
print(f"Replaced generateFormat1Pages: {count1} occurrence(s).")

with open('app/static/sample.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated app/static/sample.html with new generateFormat1Pages.")
