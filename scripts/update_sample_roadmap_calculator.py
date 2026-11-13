# scripts/update_sample_roadmap_calculator.py
with open('app/static/sample_roadmap.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the live sample box with the full interactive calculator and report specimen generator
old_section = """    <!-- ── 5. LIVE PERSONALIZED SAMPLE REPORT GENERATOR ── -->
    <section class="live-sample-box">
      <div style="text-align:center; margin-bottom:24px;">
        <span class="hero-eyebrow" style="background:#FFFFFF;">✦ INSTANT ON-DEMAND SAMPLE ENGINE ✦</span>
        <h3 style="font-family:'Cinzel',serif; font-size:1.6rem; color:var(--gold-dark); margin:8px 0 6px;">
          Generate Your Instant Personalized Sample PDF
        </h3>
        <p style="font-size:0.92rem; color:var(--ink-muted); margin:0;">
          Test our deterministic calculation engine with your own coordinates and download an authentic specimen PDF immediately.
        </p>
      </div>

      <form id="instantSampleForm" onsubmit="handleLiveSamplePdf(event)">
        <div class="live-form-grid">
          <div class="form-group">
            <label for="liveName">Full Legal Name</label>
            <input type="text" id="liveName" class="form-control" value="Aarav Sharma" required />
          </div>
          <div class="form-group">
            <label for="liveDob">Date of Birth</label>
            <input type="date" id="liveDob" class="form-control" value="1992-07-15" required />
          </div>
          <div class="form-group">
            <label for="liveTopic">Report Domain</label>
            <select id="liveTopic" class="form-control">
              <option value="vedic_destiny" selected>Vedic Destiny Blueprint</option>
              <option value="career_wealth_forecast">Career &amp; Wealth Timing</option>
              <option value="relationship_compatibility">Relationship Compatibility</option>
              <option value="business_brand_alignment">Business &amp; Brand Alignment</option>
              <option value="lo_shu_grid">Lo Shu Grid &amp; Rajyogs</option>
              <option value="core_blueprint">Personal Destiny Matrix</option>
            </select>
          </div>
          <div class="form-group">
            <label for="liveTier">Package Tier</label>
            <select id="liveTier" class="form-control">
              <option value="basic">Basic (3 Pages · ₹199)</option>
              <option value="advanced" selected>Advanced (12 Pages · ₹510)</option>
              <option value="premium">Premium (32 Pages · ₹1,050)</option>
            </select>
          </div>
        </div>

        <div style="text-align:center; margin-top:10px;">
          <button type="submit" id="livePdfBtn" class="btn-gold-primary" style="font-size:1rem; padding:13px 36px;">
            Compute Engine &amp; Download Personalized Sample PDF ✦
          </button>
          <div id="liveStatusText" style="font-size:0.85rem; color:var(--ink-muted); margin-top:10px;">
            100% deterministic calculation. Instant browser download. Zero AI arithmetic hallucinations.
          </div>
        </div>
      </form>
    </section>"""

new_section = """    <!-- ── 5. LIVE INTERACTIVE CALCULATOR & SAMPLE DOSSIER ENGINE ── -->
    <section class="live-sample-box" id="liveCalculatorSection">
      <div style="text-align:center; margin-bottom:24px;">
        <span class="hero-eyebrow" style="background:#FFFFFF;">✦ DETERMINISTIC CALCULATION ENGINE · LIVE SPECIMEN ✦</span>
        <h3 style="font-family:'Cinzel',serif; font-size:1.7rem; color:var(--gold-dark); margin:8px 0 6px;">
          Live Interactive Calculation Engine &amp; Sample Generator
        </h3>
        <p style="font-size:0.94rem; color:var(--ink-muted); margin:0 auto; max-width:680px;">
          Enter your name and date of birth below to compute your live Driver (Mulank), Conductor (Bhagyank), 3×3 Lo Shu Grid, and Silver/Golden Rajyogs in real-time. Download an authentic customized PDF report on the spot.
        </p>
      </div>

      <form id="instantSampleForm" onsubmit="event.preventDefault(); runLiveCalculation();">
        <div class="live-form-grid">
          <div class="form-group">
            <label for="liveName">Full Calling Name</label>
            <input type="text" id="liveName" class="form-control" value="Aarav Sharma" required oninput="runLiveCalculation()" />
          </div>
          <div class="form-group">
            <label for="liveDob">Date of Birth</label>
            <input type="date" id="liveDob" class="form-control" value="1992-07-15" required onchange="runLiveCalculation()" />
          </div>
          <div class="form-group">
            <label for="liveTopic">Report Domain</label>
            <select id="liveTopic" class="form-control" onchange="runLiveCalculation()">
              <option value="vedic_destiny" selected>Vedic Destiny Blueprint</option>
              <option value="career_wealth_forecast">Career &amp; Wealth Timing</option>
              <option value="relationship_compatibility">Relationship Compatibility</option>
              <option value="business_brand_alignment">Business &amp; Brand Alignment</option>
              <option value="lo_shu_grid">Lo Shu Grid &amp; Rajyogs</option>
              <option value="core_blueprint">Personal Destiny Matrix</option>
            </select>
          </div>
          <div class="form-group">
            <label for="liveTier">Package Tier</label>
            <select id="liveTier" class="form-control">
              <option value="basic">Basic (3 Pages · ₹199)</option>
              <option value="advanced" selected>Advanced (12 Pages · ₹510)</option>
              <option value="premium">Premium (32 Pages · ₹1,050)</option>
            </select>
          </div>
        </div>

        <div style="text-align:center; margin:16px 0 24px;">
          <button type="submit" id="liveCalcBtn" class="btn-gold-primary" style="font-size:1rem; padding:12px 32px;">
            Calculate Numbers &amp; Update Live Chart ✦
          </button>
        </div>
      </form>

      <!-- ── LIVE CALCULATION RESULTS DISPLAY PANEL ── -->
      <div id="liveCalcResultsPanel" style="background:#FFFFFF; border:1px solid var(--border-gold); border-radius:14px; padding:24px; box-shadow:0 6px 24px rgba(139,105,20,0.06);">
        
        <!-- Badges Row -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(180px, 1fr)); gap:14px; margin-bottom:24px;">
          <div style="background:#FFFDF7; border:1px solid var(--border-gold); border-radius:12px; padding:14px; text-align:center;">
            <div style="font-size:0.75rem; text-transform:uppercase; color:var(--ink-muted); font-weight:700; letter-spacing:0.04em;">Driver (Mulank)</div>
            <div id="resDriver" style="font-family:'Cinzel',serif; font-size:2.2rem; font-weight:700; color:var(--gold-dark); margin:4px 0;">6</div>
            <div id="resDriverPlanet" style="font-size:0.84rem; color:var(--emerald); font-weight:600;">Venus (Shukra)</div>
          </div>

          <div style="background:#FFFDF7; border:1px solid var(--border-gold); border-radius:12px; padding:14px; text-align:center;">
            <div style="font-size:0.75rem; text-transform:uppercase; color:var(--ink-muted); font-weight:700; letter-spacing:0.04em;">Conductor (Bhagyank)</div>
            <div id="resConductor" style="font-family:'Cinzel',serif; font-size:2.2rem; font-weight:700; color:var(--gold-dark); margin:4px 0;">7</div>
            <div id="resConductorPlanet" style="font-size:0.84rem; color:var(--gold-dark); font-weight:600;">Ketu (South Node)</div>
          </div>

          <div style="background:#FFFDF7; border:1px solid var(--border-gold); border-radius:12px; padding:14px; text-align:center;">
            <div style="font-size:0.75rem; text-transform:uppercase; color:var(--ink-muted); font-weight:700; letter-spacing:0.04em;">Chaldean Name Number</div>
            <div id="resNameCompound" style="font-family:'Cinzel',serif; font-size:2.2rem; font-weight:700; color:var(--gold-dark); margin:4px 0;">33 / 6</div>
            <div id="resNamePlanet" style="font-size:0.84rem; color:var(--gold-mid); font-weight:600;">Venus · Master Harmony</div>
          </div>

          <div style="background:#FFFDF7; border:1px solid var(--border-gold); border-radius:12px; padding:14px; text-align:center;">
            <div style="font-size:0.75rem; text-transform:uppercase; color:var(--ink-muted); font-weight:700; letter-spacing:0.04em;">Karmic Balance</div>
            <div id="resKarmicStatus" style="font-family:'Cinzel',serif; font-size:1.5rem; font-weight:700; color:var(--gold-dark); margin:10px 0 6px;">Harmonious</div>
            <div id="resKarmicDetail" style="font-size:0.8rem; color:var(--ink-muted);">D-6 &amp; C-7 Synthesized</div>
          </div>
        </div>

        <!-- 3x3 Grid & Planes Row -->
        <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(290px, 1fr)); gap:24px; margin-bottom:24px;">
          
          <!-- 3x3 Lo Shu Sacred Grid Box -->
          <div style="background:#FFFDF7; border:1px solid var(--border-gold); border-radius:12px; padding:20px; text-align:center;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
              <h4 style="font-family:'Cinzel',serif; font-size:1.05rem; color:var(--gold-dark); margin:0;">
                3×3 Lo Shu Sacred Square
              </h4>
              <span style="font-size:0.72rem; color:var(--emerald); background:rgba(22,131,91,0.1); padding:2px 8px; border-radius:12px; font-weight:700;">
                Deterministic
              </span>
            </div>

            <!-- 3x3 Grid Container -->
            <div id="resLoshuGrid" style="display:grid; grid-template-columns:repeat(3, 1fr); gap:8px; max-width:260px; margin:0 auto;">
              <!-- 4, 9, 2 -->
              <!-- 3, 5, 7 -->
              <!-- 8, 1, 6 -->
            </div>

            <div id="resFreqSummary" style="font-size:0.82rem; color:var(--ink-muted); margin-top:14px; line-height:1.5;"></div>
          </div>

          <!-- 8 Planes of Expression & Silver Rajyog Box -->
          <div style="background:#FFFDF7; border:1px solid var(--border-gold); border-radius:12px; padding:20px;">
            <h4 style="font-family:'Cinzel',serif; font-size:1.05rem; color:var(--gold-dark); margin:0 0 12px;">
              Planes of Expression &amp; Rajyogs
            </h4>
            <div id="resPlanesList" style="display:flex; flex-direction:column; gap:8px; max-height:260px; overflow-y:auto; padding-right:4px;">
              <!-- Planes populated via JavaScript -->
            </div>
          </div>
        </div>

        <!-- Remedies & Poorak Keys -->
        <div style="background:#F7F3EA; border-radius:12px; padding:18px 20px; margin-bottom:24px;">
          <h4 style="font-family:'Cinzel',serif; font-size:0.98rem; color:var(--gold-dark); margin:0 0 8px; display:flex; align-items:center; gap:8px;">
            <span>✦ Consecrated Remedies &amp; Poorak Keys:</span>
          </h4>
          <div id="resRemediesText" style="font-size:0.86rem; color:var(--ink-dark); line-height:1.6;">
            <!-- Dynamically populated -->
          </div>
        </div>

        <!-- Download Buttons -->
        <div style="text-align:center; border-top:1px solid rgba(201,162,39,0.25); padding-top:20px;">
          <div style="font-size:0.92rem; font-weight:700; color:var(--gold-dark); margin-bottom:12px;">
            ✦ Download Complete Verified PDF Report for This Calculated Profile:
          </div>
          <div style="display:flex; justify-content:center; gap:12px; flex-wrap:wrap;">
            <button onclick="downloadLiveCalculatedPdf('basic')" class="btn-pearl-secondary" style="font-size:0.88rem; padding:10px 20px;">
              Basic Report (3p · ₹199) 📄
            </button>
            <button onclick="downloadLiveCalculatedPdf('advanced')" class="btn-gold-primary" style="font-size:0.9rem; padding:10px 24px;">
              Advanced Report (12p · ₹510) ✦
            </button>
            <button onclick="downloadLiveCalculatedPdf('premium')" class="btn-pearl-secondary" style="font-size:0.88rem; padding:10px 20px;">
              Sovereign Dossier (32p · ₹1,050) 👑
            </button>
          </div>
          <div id="liveDownloadStatus" style="font-size:0.82rem; color:var(--ink-muted); margin-top:10px;"></div>
        </div>

      </div>
    </section>"""

assert old_section in text, "old_section not found in sample_roadmap.html"
text = text.replace(old_section, new_section)

with open('app/static/sample_roadmap.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Updated sample_roadmap.html markup with live calculation panel!")
