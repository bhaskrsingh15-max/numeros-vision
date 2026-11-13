# reorder_report_cards.py
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    text = f.read()

old_pricing_grid = '''      <div class="pricing-grid">
        <!-- 1. Premium Numerology Report (32 Pages) -->
        <div class="price-card" style="box-shadow:0 6px 24px rgba(180,155,110,0.08);">
          <div>
            <span class="calc-tool-badge" style="background:rgba(22,131,91,0.12); color:#16835B;">32-Page Comprehensive Report</span>
            <h4 style="font-family:'Cormorant Garamond',serif; font-size:1.6rem; color:#16835B; margin:8px 0 0;">
              Premium Numerology Report
            </h4>
            <div class="price-val" style="font-size:2rem; color:var(--gold-dark, #8B6914); font-weight:700;">₹1,050</div>
            <div style="font-size:0.75rem; color:#7A654D; margin-bottom:4px;">Comprehensive 32-page PDF dossier ($28.00)</div>
            <div style="font-size:0.8rem; color:#7A654D; font-weight:600;">32 Pages · In-Depth Analysis &amp; 10-Year Radar</div>
            <ul class="price-feature-list">
              <li>32-Page Complete Life &amp; Destiny Report</li>
              <li>Calling Name vs Legal Name Harmonization</li>
              <li>10-Year Year-by-Year Planetary Dasha</li>
              <li>Full Lo Shu Grid &amp; Plane Synthesis</li>
              <li>Comprehensive Remedy &amp; Alignment Dossier</li>
            </ul>
          </div>
          <button class="btn-secondary-pearl" onclick="openCheckout('report_divine', 'Premium Numerology Report', 1050)" style="width:100%; justify-content:center;">
            ANVEIL EVERY CHARM ✦ Order Premium Report (₹1,050)
          </button>
        </div>

        <!-- 2. Advanced Numerology Report (12 Pages) -->
        <div class="price-card popular" style="border: 2px solid var(--gold-primary); box-shadow: 0 10px 36px rgba(201,162,39,0.24); transform: translateY(-4px);">
          <span class="popular-pill" style="letter-spacing:0.06em;">✦ Most Popular · Best Value ✦</span>
          <div>
            <span class="calc-tool-badge" style="background:rgba(201,162,39,0.18); color:var(--gold-dark);">12-Page Comprehensive Dossier</span>
            <h4 style="font-family:'Cormorant Garamond',serif; font-size:1.65rem; color:var(--gold-dark); margin:8px 0 0;">
              Advanced Numerology Report
            </h4>
            <div class="price-val" style="font-size:2.2rem; color:var(--gold-dark, #8B6914); font-weight:800;">₹510</div>
            <div style="font-size:0.75rem; color:#8B6914; font-weight:600; margin-bottom:4px;">Most popular 12-page roadmap ($14.00)</div>
            <div style="font-size:0.8rem; color:#7A654D; font-weight:600;">12 Pages · Full Trajectory &amp; 5-Year Dasha</div>
            <ul class="price-feature-list">
              <li>12-Page Comprehensive Life Dossier</li>
              <li>Dual Pythagorean &amp; Chaldean Synthesis</li>
              <li>Lo Shu 8-Plane Comprehensive Scan</li>
              <li>5-Year Month-by-Month Dasha Radar</li>
              <li>Safe Non-Fear Remedies &amp; Alignment Advice</li>
            </ul>
          </div>
          <button class="btn-primary-gold" onclick="openCheckout('report_master', 'Advanced Numerology Report', 510)" style="width:100%; justify-content:center; font-weight:700;">
            ANVEIL EVERY CHARM ✦ Order Advanced Report (₹510)
          </button>
        </div>

        <!-- 3. Basic Numerology Report (3 Pages) -->
        <div class="price-card" style="box-shadow:0 6px 20px rgba(180,155,110,0.06);">
          <div>
            <span class="calc-tool-badge">3-Page Executive Brief</span>
            <h4 style="font-family:'Cormorant Garamond',serif; font-size:1.6rem; color:var(--gold-dark); margin:8px 0 0;">
              Basic Numerology Report
            </h4>
            <div class="price-val" style="font-size:1.85rem; color:var(--gold-dark, #8B6914); font-weight:700;">₹199</div>
            <div style="font-size:0.75rem; color:#7A654D; margin-bottom:4px;">Personal 3-page summary ($5.00)</div>
            <ul class="price-feature-list">
              <li>3-Page Executive PDF Brief</li>
              <li>Driver &amp; Conductor Energy Analysis</li>
              <li>Lo Shu 3×3 Grid &amp; Missing Numbers</li>
              <li>Immediate 90-Day Focus Guidelines</li>
            </ul>
          </div>
          <button class="btn-secondary-pearl" onclick="openCheckout('report_essential', 'Basic Numerology Report', 199)" style="width:100%; justify-content:center;">
            ANVEIL EVERY CHARM ✦ Order Basic Report (₹199)
          </button>
        </div>
      </div>'''

new_pricing_grid = '''      <div class="pricing-grid">
        <!-- 1. Basic Report (3 Pages) -->
        <div class="price-card" style="box-shadow:0 6px 20px rgba(180,155,110,0.06);">
          <div>
            <span class="calc-tool-badge">Entry Tier · 3 Pages</span>
            <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.65rem; color:var(--gold-dark); margin:8px 0 0;">
              Basic Report
            </h3>
            <div class="price-val" style="font-size:1.95rem; color:var(--gold-dark, #8B6914); font-weight:700;">₹199</div>
            <div style="font-size:0.75rem; color:#7A654D; margin-bottom:4px;">Personal 3-page executive summary ($5.00)</div>
            <ul class="price-feature-list">
              <li>3-Page Personalised PDF Dossier</li>
              <li>Driver (Mulank) &amp; Conductor (Bhagyank) Core Matrix</li>
              <li>Lo Shu 3×3 Grid &amp; Missing Number Identifications</li>
              <li>Immediate 90-Day Focus Roadmap</li>
              <li>Classical Methodology &amp; Scope Note</li>
            </ul>
          </div>
          <button class="btn-secondary-pearl" onclick="openCheckout('report_essential', 'Basic Numerology Report', 199)" style="width:100%; justify-content:center;">
            Order Basic Report (₹199) ✦
          </button>
        </div>

        <!-- 2. Advanced Report (12 Pages) · Most Popular -->
        <div class="price-card popular" style="border: 2px solid var(--gold-primary); box-shadow: 0 10px 36px rgba(201,162,39,0.24); transform: translateY(-4px);">
          <span class="popular-pill" style="letter-spacing:0.06em;">✦ Most Popular · Best Value ✦</span>
          <div>
            <span class="calc-tool-badge" style="background:rgba(201,162,39,0.18); color:var(--gold-dark);">Master Tier · 12 Pages</span>
            <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.7rem; color:var(--gold-dark); margin:8px 0 0;">
              Advanced Report
            </h3>
            <div class="price-val" style="font-size:2.3rem; color:var(--gold-dark, #8B6914); font-weight:800;">₹510</div>
            <div style="font-size:0.75rem; color:#8B6914; font-weight:600; margin-bottom:4px;">Most popular 12-page roadmap ($14.00)</div>
            <div style="font-size:0.8rem; color:#7A654D; font-weight:600;">12 Pages · Full Trajectory &amp; 5-Year Dasha</div>
            <ul class="price-feature-list">
              <li>12-Page Comprehensive Master Synthesis Dossier</li>
              <li>Table of Contents &amp; Executive Summary</li>
              <li>Dual Pythagorean &amp; Chaldean Sound Synthesis</li>
              <li>Lo Shu 8-Plane Comprehensive Scan</li>
              <li>5-Year Month-by-Month Dasha Radar</li>
              <li>Safe Non-Fear Remedies &amp; Alignment Protocols</li>
            </ul>
          </div>
          <button class="btn-primary-gold" onclick="openCheckout('report_master', 'Advanced Numerology Report', 510)" style="width:100%; justify-content:center; font-weight:700;">
            Order Advanced Report (₹510) ✦
          </button>
        </div>

        <!-- 3. Premium Report (32 Pages) -->
        <div class="price-card" style="box-shadow:0 6px 24px rgba(180,155,110,0.08);">
          <div>
            <span class="calc-tool-badge" style="background:rgba(22,131,91,0.12); color:#16835B;">Sovereign Tier · 32 Pages</span>
            <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.65rem; color:#16835B; margin:8px 0 0;">
              Premium Report
            </h3>
            <div class="price-val" style="font-size:2rem; color:var(--gold-dark, #8B6914); font-weight:700;">₹1,050</div>
            <div style="font-size:0.75rem; color:#7A654D; margin-bottom:4px;">Complete 32-page sovereign blueprint ($28.00)</div>
            <div style="font-size:0.8rem; color:#7A654D; font-weight:600;">32 Pages · In-Depth Analysis &amp; 10-Year Radar</div>
            <ul class="price-feature-list">
              <li>32-Page Sovereign Master Dossier</li>
              <li>Calling Name vs Legal Name Acoustic Harmonization</li>
              <li>10-Year Year-by-Year Planetary Dasha Horizon</li>
              <li>Multi-System Synastry &amp; Spatial Alignment</li>
              <li>Comprehensive Gemstone &amp; Yantra Prescription</li>
              <li>Complete Mathematical Proofs Appendix</li>
            </ul>
          </div>
          <button class="btn-secondary-pearl" onclick="openCheckout('report_divine', 'Premium Numerology Report', 1050)" style="width:100%; justify-content:center;">
            Order Premium Report (₹1,050) ✦
          </button>
        </div>
      </div>

      <div style="text-align:center; margin-top:28px; margin-bottom:8px;">
        <a href="/reports_catalogue/" class="btn-secondary-pearl" style="display:inline-flex; align-items:center; gap:8px; padding:12px 28px; font-weight:600; text-decoration:none;">
          <span>Explore All 10 Specialised Reports in Catalogue</span>
          <span>→</span>
        </a>
      </div>'''

if old_pricing_grid in text:
    text = text.replace(old_pricing_grid, new_pricing_grid)
    with open('app/static/index.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Successfully updated pricing-grid: Basic -> Advanced -> Premium with H3 tags and Catalogue link")
else:
    print("Warning: old_pricing_grid not found")
