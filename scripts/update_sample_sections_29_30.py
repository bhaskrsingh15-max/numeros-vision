import re

print("--- Updating app/static/sample.html ---")

with open('app/static/sample.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update TOC on Page 2
old_toc_29_30 = '"Sec 29: Annual Executive Self-Audit", "Sec 30: Mathematical Appendix & Governance"'
new_toc_29_30 = '"Sec 29: 4-Stage Pinnacle Cycles & Life Challenges", "Sec 30: Vastu Dosha as per Missing Numbers & Cures"'

if old_toc_29_30 in html:
    html = html.replace(old_toc_29_30, new_toc_29_30)
    print("TOC on Page 2 updated successfully!")
else:
    print("WARNING: old_toc_29_30 not found")

# 2. Update Sections 29 and 30 in sectionsData
old_sections_29_30 = '''        {
          num: 29, title: "Annual Executive Self-Audit & Framework", p: 31,
          content: `
            <div class="report-card">
              <div class="card-title">✦ Contemplative Executive Review</div>
              <p class="body-p">Every year on your birthday (${day}-${month}), conduct an audit of your elemental planes and missing number remedies. Ensure charitable donations have been completed.</p>
            </div>
          `
        },
        {
          num: 30, title: "Mathematical Appendix & Calculation Governance", p: 32,
          content: `
            <div class="report-card">
              <div class="card-title">✦ Mathematical Proofs &amp; Engine Provenance</div>
              <div style="font-size:9.5px;color:#523E28;line-height:1.45;">
                <div><strong>Driver Calculation:</strong> Day ${day} → ${driver}</div>
                <div><strong>Conductor Calculation:</strong> Sum(${dob.replace(/-/g, '+')}) → ${conductor}</div>
                <div><strong>Kua Calculation:</strong> 11 - (Sum of Year ${year}) → ${kua}</div>
                <div><strong>Name Calculation:</strong> Chaldean ${name} → ${chaldean.single} (${chaldean.compound})</div>
              </div>
              <div style="margin-top:10px;font-size:8.5px;color:#7A654D;text-align:center;">
                Master Numerologist Bhaskr Singh · Numeros Vision (+91 9818418039)<br>
                Numeros Vision © 2026 · All Rights Reserved
              </div>
            </div>
          `
        }'''

new_sections_29_30 = '''        {
          num: 29, title: "4-Stage Pinnacle Cycles & Life Challenge Numbers", p: 31,
          content: `
            <div class="report-card">
              <div class="card-title">✦ 4-Stage Pinnacle (Peak Opportunity) Cycles</div>
              <p class="body-p">In classical Pythagorean-Chaldean numerology, your life trajectory is governed by 4 distinct epochs of destiny. Derived from your birth day (${day}), month (${month}), and year (${year}):</p>
              <table style="width:100%; border-collapse:collapse; margin:8px 0 12px 0; font-size:10px;">
                <thead>
                  <tr style="background:#F7F3EA; color:#8B6914; border-bottom:1.5px solid #C9A227;">
                    <th style="padding:6px; text-align:left;">Pinnacle Epoch</th>
                    <th style="padding:6px; text-align:center;">Age Span</th>
                    <th style="padding:6px; text-align:center;">Vibration</th>
                    <th style="padding:6px; text-align:left;">Governing Archetype &amp; Opportunity</th>
                  </tr>
                </thead>
                <tbody style="color:#523E28;">
                  <tr style="border-bottom:1px solid rgba(201,162,39,0.2);">
                    <td style="padding:5px 6px; font-weight:700;">First Pinnacle (P1)</td>
                    <td style="padding:5px 6px; text-align:center;">Age 0 – 32</td>
                    <td style="padding:5px 6px; text-align:center; font-weight:800; color:#8B6914;">Number 3</td>
                    <td style="padding:5px 6px;">Jupiter: Creative self-expression, communication mastery &amp; intellectual foundation</td>
                  </tr>
                  <tr style="border-bottom:1px solid rgba(201,162,39,0.2);">
                    <td style="padding:5px 6px; font-weight:700;">Second Pinnacle (P2)</td>
                    <td style="padding:5px 6px; text-align:center;">Age 33 – 41</td>
                    <td style="padding:5px 6px; text-align:center; font-weight:800; color:#8B6914;">Number 2</td>
                    <td style="padding:5px 6px;">Moon: Strategic partnerships, executive diplomacy &amp; emotional maturity</td>
                  </tr>
                  <tr style="border-bottom:1px solid rgba(201,162,39,0.2); background:rgba(22,131,91,0.08);">
                    <td style="padding:5px 6px; font-weight:700; color:#16835B;">Third Pinnacle (P3) ★</td>
                    <td style="padding:5px 6px; text-align:center; font-weight:700; color:#16835B;">Age 42 – 50</td>
                    <td style="padding:5px 6px; text-align:center; font-weight:800; color:#16835B;">Number 5</td>
                    <td style="padding:5px 6px; font-weight:600; color:#16835B;">Mercury: Commercial scaling, media innovation, programmatic adtech &amp; freedom (CURRENT)</td>
                  </tr>
                  <tr>
                    <td style="padding:5px 6px; font-weight:700;">Fourth Pinnacle (P4)</td>
                    <td style="padding:5px 6px; text-align:center;">Age 51+</td>
                    <td style="padding:5px 6px; text-align:center; font-weight:800; color:#8B6914;">Number 3</td>
                    <td style="padding:5px 6px;">Jupiter: Institutional mentorship, sovereign board leadership &amp; enduring legacy</td>
                  </tr>
                </tbody>
              </table>

              <div class="card-title" style="margin-top:12px;">✦ The 4 Karmic Life Challenge Numbers</div>
              <table style="width:100%; border-collapse:collapse; margin:8px 0 0 0; font-size:10px;">
                <thead>
                  <tr style="background:#F7F3EA; color:#8B6914; border-bottom:1.5px solid #C9A227;">
                    <th style="padding:6px; text-align:left;">Challenge Epoch</th>
                    <th style="padding:6px; text-align:center;">Age Span</th>
                    <th style="padding:6px; text-align:center;">Number</th>
                    <th style="padding:6px; text-align:left;">Karmic Lesson &amp; Sovereign Mastery</th>
                  </tr>
                </thead>
                <tbody style="color:#523E28;">
                  <tr style="border-bottom:1px solid rgba(201,162,39,0.2);">
                    <td style="padding:5px 6px; font-weight:700;">First Challenge (C1)</td>
                    <td style="padding:5px 6px; text-align:center;">Age 0 – 32</td>
                    <td style="padding:5px 6px; text-align:center; font-weight:800; color:#A13030;">Number 1</td>
                    <td style="padding:5px 6px;">Sun: Overcoming early self-doubt and establishing sovereign individual autonomy</td>
                  </tr>
                  <tr style="border-bottom:1px solid rgba(201,162,39,0.2);">
                    <td style="padding:5px 6px; font-weight:700;">Second Challenge (C2)</td>
                    <td style="padding:5px 6px; text-align:center;">Age 33 – 41</td>
                    <td style="padding:5px 6px; text-align:center; font-weight:800; color:#16835B;">Number 0</td>
                    <td style="padding:5px 6px;">The Choice Challenge: Rare epoch of absolute free will, heightened intuition &amp; self-direction</td>
                  </tr>
                  <tr style="border-bottom:1px solid rgba(201,162,39,0.2); background:rgba(201,162,39,0.08);">
                    <td style="padding:5px 6px; font-weight:700; color:#8B6914;">Major Lifetime (C3) ★</td>
                    <td style="padding:5px 6px; text-align:center; font-weight:700; color:#8B6914;">Lifetime</td>
                    <td style="padding:5px 6px; text-align:center; font-weight:800; color:#8B6914;">Number 1</td>
                    <td style="padding:5px 6px; font-weight:600;">Sun: Leading teams with magnetic warmth without triggering ego friction with partners</td>
                  </tr>
                  <tr>
                    <td style="padding:5px 6px; font-weight:700;">Fourth Challenge (C4)</td>
                    <td style="padding:5px 6px; text-align:center;">Age 51+</td>
                    <td style="padding:5px 6px; text-align:center; font-weight:800; color:#A13030;">Number 1</td>
                    <td style="padding:5px 6px;">Sun: Sustaining visionary authority while cultivating successor leadership</td>
                  </tr>
                </tbody>
              </table>
            </div>
          `
        },
        {
          num: 30, title: "Vastu Dosha as per Missing Numbers & Spatial Corrections", p: 32,
          content: `
            <div class="report-card">
              <div class="card-title">✦ Directional Lo Shu Spatial Analysis &amp; Cures</div>
              <p class="body-p">Every digit in your Lo Shu matrix governs a specific directional sector of your residence and workspace. The missing numbers in your chart create spatial imbalances (Vastu Doshas) that require physical corrections:</p>
              
              <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px;">
                <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.3); border-radius:8px; padding:8px 10px;">
                  <div style="font-weight:700; font-size:10px; color:#8B6914; display:flex; justify-content:space-between;">
                    <span>South-West (SW) · Missing 2</span>
                    <span style="color:#A13030;">Earth Dosha</span>
                  </div>
                  <div style="font-size:9px; color:#523E28; margin-top:3px; line-height:1.4;">
                    <strong>Vulnerability:</strong> Relationship volatility, emotional restlessness, partnership instability.<br>
                    <strong>Spatial Cure:</strong> Place heavy brass artefacts, a yellow earth ceramic bowl, or warm yellow night lamp in the SW corner. Avoid water elements.
                  </div>
                </div>

                <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.3); border-radius:8px; padding:8px 10px;">
                  <div style="font-weight:700; font-size:10px; color:#8B6914; display:flex; justify-content:space-between;">
                    <span>East (E) · Missing 3</span>
                    <span style="color:#A13030;">Wood Dosha</span>
                  </div>
                  <div style="font-size:9px; color:#523E28; margin-top:3px; line-height:1.4;">
                    <strong>Vulnerability:</strong> Delays in social recognition, hurdles in accessing high-level mentorship.<br>
                    <strong>Spatial Cure:</strong> Mount a polished Brass Surya on the East wall. Keep lush green plants (money plant or bamboo) in the East zone.
                  </div>
                </div>

                <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.3); border-radius:8px; padding:8px 10px;">
                  <div style="font-weight:700; font-size:10px; color:#8B6914; display:flex; justify-content:space-between;">
                    <span>South-East (SE) · Missing 4</span>
                    <span style="color:#A13030;">Fire Cashflow</span>
                  </div>
                  <div style="font-size:9px; color:#523E28; margin-top:3px; line-height:1.4;">
                    <strong>Vulnerability:</strong> Rapid liquid capital leaks, cashflow friction (partially mitigated by Conductor 4).<br>
                    <strong>Spatial Cure:</strong> Install an electric camphor diffuser or a soft red/green lamp in the SE corner to stimulate steady financial velocity.
                  </div>
                </div>

                <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.3); border-radius:8px; padding:8px 10px;">
                  <div style="font-weight:700; font-size:10px; color:#8B6914; display:flex; justify-content:space-between;">
                    <span>Center · Missing 5</span>
                    <span style="color:#A13030;">Brahmasthan</span>
                  </div>
                  <div style="font-size:9px; color:#523E28; margin-top:3px; line-height:1.4;">
                    <strong>Vulnerability:</strong> Loss of core commercial stability and sudden strategic disorientation.<br>
                    <strong>Spatial Cure:</strong> Keep the geometric center of your office completely open and free from heavy pillars or dark furniture. Place a brass crystal lotus.
                  </div>
                </div>

                <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.3); border-radius:8px; padding:8px 10px;">
                  <div style="font-weight:700; font-size:10px; color:#8B6914; display:flex; justify-content:space-between;">
                    <span>North-West (NW) · Missing 6</span>
                    <span style="color:#A13030;">Metal Dosha</span>
                  </div>
                  <div style="font-size:9px; color:#523E28; margin-top:3px; line-height:1.4;">
                    <strong>Vulnerability:</strong> Delayed banking support, unreliable vendor partnerships, international blocks.<br>
                    <strong>Spatial Cure:</strong> Suspend a 6-rod hollow metallic wind chime on the NW wall. Keep silver coins in a brass bowl in the NW quadrant.
                  </div>
                </div>

                <div style="background:#FFFDF7; border:1px solid rgba(201,162,39,0.3); border-radius:8px; padding:8px 10px;">
                  <div style="font-weight:700; font-size:10px; color:#8B6914; display:flex; justify-content:space-between;">
                    <span>West (W) · Missing 7</span>
                    <span style="color:#A13030;">Metal Focus</span>
                  </div>
                  <div style="font-size:9px; color:#523E28; margin-top:3px; line-height:1.4;">
                    <strong>Vulnerability:</strong> Mental restlessness, over-analysis, delayed project completion.<br>
                    <strong>Spatial Cure:</strong> Install a round white metal artefact or consecrated brass Ketu/Ganesh Yantra on the West wall. Decorate in pearl white.
                  </div>
                </div>
              </div>
            </div>
          `
        }'''

if old_sections_29_30 in html:
    html = html.replace(old_sections_29_30, new_sections_29_30)
    print("Sections 29 and 30 in sample.html replaced successfully!")
else:
    print("WARNING: old_sections_29_30 not found in sample.html")

# 3. Add beforeprint and afterprint event listeners
print_js_snippet = '''
  // Forcefully suppress all navigation and chrome during Vector Print
  window.addEventListener('beforeprint', function() {
    document.querySelectorAll('.nv-sticky-bottom-nav, nav, header, footer:not(.page-footer), #nvReportPaywallModal, .report-hero-section, .viewer-toolbar, .generator-card, .comparison-section').forEach(function(el) {
      el.setAttribute('data-print-prev-display', el.style.display || '');
      el.style.setProperty('display', 'none', 'important');
      el.style.setProperty('visibility', 'hidden', 'important');
    });
  });
  window.addEventListener('afterprint', function() {
    document.querySelectorAll('.nv-sticky-bottom-nav, nav, header, footer:not(.page-footer), #nvReportPaywallModal, .report-hero-section, .viewer-toolbar, .generator-card, .comparison-section').forEach(function(el) {
      var prev = el.getAttribute('data-print-prev-display');
      if (prev !== null && prev !== '') {
        el.style.display = prev;
        el.removeAttribute('data-print-prev-display');
      } else {
        el.style.removeProperty('display');
      }
      el.style.removeProperty('visibility');
    });
  });
'''

if 'window.addEventListener(\'beforeprint\'' not in html:
    html = html.replace('function closePaywallModal() {', print_js_snippet + '\n    function closePaywallModal() {')
    print("Added beforeprint and afterprint event listeners to sample.html!")

# 4. Clean up any remaining "chapter" mentions in user-facing strings
html = html.replace('PREMIUM SOVEREIGN CHAPTER LOCKED', 'PREMIUM SOVEREIGN SECTION LOCKED')
html = html.replace('32-chapter sovereign roadmap', '32-section sovereign roadmap')
html = html.replace('32-chapter life roadmap', '32-section life roadmap')
html = html.replace('12-chapter synthesis', '12-section synthesis')

with open('app/static/sample.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved app/static/sample.html successfully!")
