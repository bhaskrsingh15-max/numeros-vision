function generateFormat1Pages(client) {
      const { name, dob, gender, phone } = client;
      const [year, month, day] = dob.split('-');
      const driver = getDriver(day);
      const conductor = getConductor(dob);
      const kua = getKua(year, gender);
      const chaldean = getChaldean(name);
      const totalPages = 3;

      const dobDigits = dob.replace(/\D/g, '').split('').filter(d => d !== '0').map(Number);
      const counts = {};
      for (let i = 1; i <= 9; i++) counts[i] = 0;
      dobDigits.forEach(d => counts[d] = (counts[d] || 0) + 1);
      const missing = Object.keys(counts).filter(k => counts[k] === 0).map(Number);
      const planes = evaluatePlanes(counts);
      const myVastu = vastuVectors[String(kua)] || vastuVectors[1];

      const pages = [];

      // ── FORMAT 1: PAGE 1 (UNLOCKED: Foundational Identity & Lo Shu Grid) ──
      pages.push(`
        <div class="pdf-page" id="page-1">
          ${CORNERS}
          ${WATERMARK_SVG}
          ${renderPageHeader('Free Discovery Blueprint · Page 1 · Foundational Profile')}
          <div class="page-content">
            <div class="content-top-group" style="text-align:center;">
              <div style="font-family:'Cinzel Decorative','Cinzel',serif;font-size:11px;letter-spacing:0.2em;color:#8B6914;margin-bottom:4px;">✦ FREE CELESTIAL DISCOVERY BLUEPRINT ✦</div>
              <div style="font-family:'Cinzel',serif;font-size:26px;font-weight:900;color:#8B6914;letter-spacing:0.03em;" role="heading" aria-level="2">${name.toUpperCase()}</div>
              <div style="font-family:'Marcellus',serif;font-size:13px;color:#16835B;margin-bottom:8px;">Foundational Planetary Frequency &amp; Lo Shu Grid Matrix</div>

              <div style="display:flex;justify-content:center;margin-bottom:8px;">
                <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision" style="width:84px;height:84px;display:block;margin:0 auto;object-fit:contain;" />
              </div>

              <!-- 4 Vital Core Badges -->
              <div class="metric-pill-row">
                <div class="metric-pill">
                  <div class="metric-pill-label">Psychic (Mulank)</div>
                  <div class="metric-pill-val">${driver} · ${EMBEDDED_DATA.planets[String(driver)]}</div>
                </div>
                <div class="metric-pill">
                  <div class="metric-pill-label">Destiny (Bhagyank)</div>
                  <div class="metric-pill-val">${conductor} · ${EMBEDDED_DATA.planets[String(conductor)]}</div>
                </div>
                <div class="metric-pill">
                  <div class="metric-pill-label">Cosmic Vector</div>
                  <div class="metric-pill-val">${kua} (${myVastu.group})</div>
                </div>
                <div class="metric-pill">
                  <div class="metric-pill-label">Calling Name</div>
                  <div class="metric-pill-val">${chaldean.single} (${chaldean.compound})</div>
                </div>
              </div>
            </div>

            <!-- Client Coordinates -->
            <div class="report-card">
              <div class="card-title">✦ Verified Chart Coordinates</div>
              <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(130px, 1fr));gap:8px;font-size:11.5px;color:#523E28;">
                <div><strong>Full Name:</strong> ${name}</div>
                <div><strong>Date of Birth:</strong> ${dob}</div>
                <div><strong>Day Number:</strong> Day ${parseInt(day,10)}</div>
                <div><strong>Cosmic Archetype:</strong> ${EMBEDDED_DATA.planets[String(driver)]} Leadership</div>
                <div><strong>Access Level:</strong> Free Discovery Tier</div>
              </div>
            </div>

            <!-- Lo Shu Matrix Table -->
            <div style="text-align:center;">
              <div style="font-family:'Cinzel',serif;font-size:13px;font-weight:700;color:#8B6914;margin-bottom:4px;">Natal Lo Shu 3×3 Grid &amp; Elemental Frequencies</div>
              ${renderLoShuTable(counts)}
            </div>

            <!-- Unlocked Natal Gap Analysis & Lucky Charm Activation Hook -->
            ${renderNatalGapAnalysis(counts, missing, driver, conductor)}

            <!-- Current Age Number Vibrational Frequency Card -->
            ${renderAgeNumerologyCard(dob, missing)}
          </div>
          ${renderPageFooter(1, totalPages)}
        </div>
      `);

      // ── FORMAT 1: PAGE 2 (LOCKED TEASER: 8 Elemental Planes & Golden Raj Yogas) ──
      pages.push(`
        <div class="pdf-page" id="page-2">
          ${CORNERS}
          ${WATERMARK_SVG}
          ${renderPageHeader('Format 1 · Page 2 · 8 Elemental Planes & Raj Yogas (Locked)')}
          <div class="page-content" style="position:relative; overflow:hidden;">
            <div class="chapter-hero-title">8 Elemental Planes &amp; Hidden Raj Yogas</div>
            <div class="chapter-hero-subtitle">Cognitive, Will &amp; Action Balance · Sovereign Power Line Audit</div>

            <!-- Faint Blurred Silhouette of the deep content behind the lock -->
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

            <!-- Prominent High-Converting Curiosity Lock Card with Brand Tagline CTA -->
            <div class="report-locked-overlay">
              <div class="locked-badge-pill">🔒 Premium Chapter Locked</div>
              <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.65rem; color:#8B6914; margin:0 0 8px 0; font-weight:700;">
                Activate Your 8-Plane Elemental Strength &amp; Lucky Charm
              </h3>
              <p style="font-size:0.88rem; color:#6B5E4F; line-height:1.6; max-width:540px; margin:0 auto 12px;">
                Your natal chart contains potent alignments across the Thought, Will, and Action planes. Are your Golden 4-5-6 and Silver 2-5-8 lines fully active, partially dormant, or leaking vital wealth momentum?
              </p>

              <div class="locked-curiosity-box">
                <strong style="color:#8B6914; display:block; margin-bottom:4px;">✦ The Seeker's Curiosity Hook:</strong>
                Seekers with your Driver ${driver} and Conductor ${conductor} combination frequently experience hidden friction in capital retention and career leaps due to unsealed elemental leaks. Activate your personalized Lucky Charm and master dossier to reveal your exact percentage breakdown and energetic activations.
              </div>

              <div style="margin-top:16px;">
                <a href="/checkout/?plan=report_master" class="nv-btn-cta" style="padding:12px 26px; font-size:0.88rem; text-decoration:none; display:inline-flex; align-items:center; gap:8px;">
                  ANVEIL EVERY CHARM ✦ Activate Lucky Charm Dossier (₹510)
                </a>
              </div>
              <div style="margin-top:10px;">
                <a href="/checkout/?plan=report_divine" style="color:#8B6914; font-size:0.80rem; font-weight:600; text-decoration:underline;">
                  Or Reveal Complete 32-Page Sovereign Blueprint (₹1,050) →
                </a>
              </div>
              <span style="font-size:0.72rem; color:#7A654D; display:block; margin-top:10px;">
                Numeros Vision · ANVEIL EVERY CHARM · One-Time Investment · Instant Delivery
              </span>
            </div>
          </div>
          ${renderPageFooter(2, totalPages)}
        </div>
      `);

      // ── FORMAT 1: PAGE 3 (LOCKED TEASER: Missing Numbers & 7-Layer Holistic Remedies) ──
      pages.push(`
        <div class="pdf-page" id="page-3">
          ${CORNERS}
          ${WATERMARK_SVG}
          ${renderPageHeader('Format 1 · Page 3 · Karmic Missing Digits & Remedies (Locked)')}
          <div class="page-content" style="position:relative; overflow:hidden;">
            <div class="chapter-hero-title">Karmic Missing Numbers &amp; 7-Layer Cures</div>
            <div class="chapter-hero-subtitle">Vedic Elemental Voids, Safe Remedies &amp; Multi-Year Roadmap</div>

            <!-- Faint Blurred Silhouette of Remedies -->
            <div class="blurred-content-preview">
              <div class="report-card" style="margin-bottom:8px;">
                <div class="card-title">✦ Missing Karmic Digits: [ ${missing.join(', ') || 'None'} ]</div>
                <p class="body-p">Specific planetary gemstones and metal conduits to seal karmic debt without counter-productive frictions...</p>
              </div>
              <div class="report-card">
                <div class="card-title">🧭 Auspicious Directions &amp; Vastu Alignment</div>
                <p class="body-p">Desk facing and bedhead orientation for wealth compounding and serene nervous recovery...</p>
              </div>
            </div>

            <!-- Prominent High-Converting Curiosity Lock Card with Brand Tagline CTA -->
            <div class="report-locked-overlay">
              <div class="locked-badge-pill">🔒 Sacred Remedies &amp; Timelines Locked</div>
              <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.65rem; color:#8B6914; margin:0 0 8px 0; font-weight:700;">
                Activate Your Planetary Harmonization Remedies &amp; Lucky Charm
              </h3>
              <p style="font-size:0.88rem; color:#6B5E4F; line-height:1.6; max-width:540px; margin:0 auto 12px;">
                Your chart lacks digits <strong>[ ${missing.join(', ') || 'None'} ]</strong>. Activating wrong gemstones without planetary conflict neutralization can trigger unexpected delays. Discover your safe, tailored remedies.
              </p>

              <div class="locked-curiosity-box">
                <strong style="color:#8B6914; display:block; margin-bottom:4px;">✦ The Seeker's Curiosity Hook:</strong>
                Which specific days, colors, and sacred charitable acts neutralize your karmic debts? When does your next favorable expansion window open in 2026? Activate your full multi-year dasha radar and sacred beej mantra.
              </div>

              <div style="margin-top:16px;">
                <a href="/checkout/?plan=report_master" class="nv-btn-cta" style="padding:12px 26px; font-size:0.88rem; text-decoration:none; display:inline-flex; align-items:center; gap:8px;">
                  ANVEIL EVERY CHARM ✦ Activate Lucky Charm Dossier (₹510)
                </a>
              </div>
              <div style="margin-top:10px;">
                <a href="/checkout/?plan=report_divine" style="color:#8B6914; font-size:0.80rem; font-weight:600; text-decoration:underline;">
                  Or Reveal Complete 32-Page Sovereign Blueprint (₹1,050) →
                </a>
              </div>
              <span style="font-size:0.72rem; color:#7A654D; display:block; margin-top:10px;">
                Master Brand: Numeros Vision · Tagline: ANVEIL EVERY CHARM · 100% Classical Precision &amp; Security
              </span>
            </div>
          </div>
          ${renderPageFooter(3, totalPages)}
        </div>
      `);

      return pages;
    }

    // =========================================================================
    // FORMAT 2: MASTER DUAL-SYSTEM DOSSIER (12 PAGES)
    // Flagship comprehensive synthesis with 81-pair synergy & Lo Shu matrix
    // =========================================================================
    