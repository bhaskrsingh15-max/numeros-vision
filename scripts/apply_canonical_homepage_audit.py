# apply_canonical_homepage_audit.py
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Section 3: Merge Explore & Next Insight & Popular Calculators into single canonical H2 "Explore Numerology Calculators"
old_sec3 = '''      <!-- ── 3B. EXPLORE YOUR NUMEROLOGY (2x2 Grid) ── -->
      <div class="nv-explore-section">
        <div class="sec-header" style="margin-bottom: 20px; text-align: left;">
          <h3 class="nv-explore-section-title">
            Explore Your Numerology
          </h3>
        </div>

        <div class="nv-explore-grid">
          <!-- 1. Life Path -->
          <a href="/tools/life-path-calculator" class="nv-explore-card" title="Life Path Number Calculator">
            <div class="nv-explore-icon">✦</div>
            <div class="nv-explore-title">Life Path</div>
            <div class="nv-explore-sub">Explore your reading</div>
          </a>

          <!-- 2. Name Analysis -->
          <a href="/tools/name-balancing" class="nv-explore-card" title="Name Analysis & Balancing">
            <div class="nv-explore-icon">✦</div>
            <div class="nv-explore-title">Name Analysis</div>
            <div class="nv-explore-sub">Explore your reading</div>
          </a>

          <!-- 3. Lo Shu Grid -->
          <a href="/calculators/lo-shu-grid/" class="nv-explore-card" title="Lo Shu 3×3 Grid Calculator">
            <div class="nv-explore-icon">✦</div>
            <div class="nv-explore-title">Lo Shu Grid</div>
            <div class="nv-explore-sub">Explore your reading</div>
          </a>

          <!-- 4. Compatibility -->
          <a href="/tools/kundali-milan" class="nv-explore-card" title="Numerology & Synastry Compatibility">
            <div class="nv-explore-icon">✦</div>
            <div class="nv-explore-title">Compatibility</div>
            <div class="nv-explore-sub">Explore your reading</div>
          </a>
        </div>
      </div>

      <!-- ── 3C. YOUR NEXT INSIGHT (Personalised Reports Banner) ── -->
      <div class="nv-next-insight-section">
        <div class="sec-header" style="margin-bottom: 16px; text-align: left;">
          <h3 class="nv-next-insight-section-title">
            Your Next Insight
          </h3>
        </div>

        <div class="nv-next-insight-card">
          <div class="nv-next-insight-body">
            <h4 class="nv-next-insight-title">Personalised reports</h4>
            <p class="nv-next-insight-desc">
              Explore the report options that match your interests.
            </p>
            <a href="/reports_catalogue/" class="nv-next-insight-link">
              <span>View reports</span>
              <span>→</span>
            </a>
          </div>
        </div>
      </div>

      <!-- Popular Working Tools Directory -->
      <div class="sec-header" style="margin-bottom:30px;">
        <span class="sec-eyebrow">SUITE OF WORKING INSTRUMENTS</span>
        <h3 style="font-family:'Cormorant Garamond',serif; font-size:2rem; color:var(--gold-dark); margin:0;">
          Popular Numerology Calculators
        </h3>
      </div>'''

new_sec3 = '''      <!-- ── 3. EXPLORE NUMEROLOGY CALCULATORS ── -->
      <div class="sec-header" style="margin-top:44px; margin-bottom:28px;">
        <span class="sec-eyebrow">CURATED WORKING INSTRUMENTS · FREE DISCOVERY</span>
        <h2 class="sec-title">Explore Numerology Calculators</h2>
        <p class="sec-sub">
          Select a verified calculator below to explore specific facets of your birth chart, name harmony, or cycles. All initial calculations are 100% free and mathematically verified.
        </p>
      </div>

      <!-- Discovery Guide: Find the Right Starting Point -->
      <div class="nv-next-insight-card" style="margin-bottom:32px; background:linear-gradient(135deg, rgba(255,253,247,0.98), rgba(247,243,234,0.92)); border:1.5px solid var(--border-amber); border-radius:16px; padding:22px 26px; box-shadow:var(--shadow-amber);">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
          <div style="max-width:620px;">
            <div style="display:inline-flex; align-items:center; gap:6px; font-size:0.75rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase; letter-spacing:0.08em; margin-bottom:6px;">
              <span>✦</span> <span>Find the Right Starting Point</span>
            </div>
            <div style="font-family:'Cormorant Garamond',serif; font-size:1.45rem; color:var(--gold-dark); font-weight:700; margin-bottom:4px;">Not sure which calculator to explore first?</div>
            <p style="font-size:0.88rem; color:#7A654D; margin:0; line-height:1.5;">
              Start with your <strong>Birth Number (Mulank)</strong> and <strong>Life Path</strong> to understand your foundational mind and trajectory. When ready for comprehensive multi-year dasha forecasts, explore our personalised dossiers.
            </p>
          </div>
          <a href="/reports_catalogue/" class="btn-primary-gold" style="font-size:0.84rem; padding:10px 20px; white-space:nowrap; text-decoration:none;">
            <span>Browse Personalised Reports →</span>
          </a>
        </div>
      </div>'''

if old_sec3 in content:
    content = content.replace(old_sec3, new_sec3)
    print("Updated Section 3: Merged into canonical H2 'Explore Numerology Calculators'")
else:
    print("Warning: old_sec3 not found")

# 2. Update Section 6: Methodology section heading
old_sec6 = '''          <span class="sec-eyebrow">✦ ABOUT NUMEROS VISION · OUR APPROACH &amp; TRADITIONS ✦</span>
          <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.3rem; color:var(--gold-dark); margin:0 0 12px;">
            About Numeros Vision | Our Approach to Authentic Numerology
          </h2>'''

new_sec6 = '''          <span class="sec-eyebrow">✦ TRANSPARENT CALCULATION FRAMEWORK · MULTI-SYSTEM HARMONY ✦</span>
          <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.3rem; color:var(--gold-dark); margin:0 0 12px;">
            Deterministic Calculation &amp; Multi-System Methodology
          </h2>'''

if old_sec6 in content:
    content = content.replace(old_sec6, new_sec6)
    print("Updated Section 6: Methodology heading to 'Deterministic Calculation & Multi-System Methodology'")
else:
    print("Warning: old_sec6 not found")

# 3. Update Charm AI usage transparency note
old_charm_input = '''        <div class="chat-input-bar">
          <button class="chat-voice-btn" id="voice-btn" onclick="toggleVoiceInput()" title="Voice Input" aria-label="Voice Input">🎙</button>
          <input type="text" id="chat-input" placeholder="Ask Charm AI anything about your numbers..." onkeydown="if(event.key==='Enter') sendChatMessage();" />
          <button class="btn-primary-gold" onclick="sendChatMessage()" style="padding:14px 24px; border-radius:999px;">
            Send ✦
          </button>
        </div>'''

new_charm_input = '''        <div class="chat-input-bar">
          <button class="chat-voice-btn" id="voice-btn" onclick="toggleVoiceInput()" title="Voice Input" aria-label="Voice Input">🎙</button>
          <input type="text" id="chat-input" placeholder="Ask Charm AI anything about your numbers..." onkeydown="if(event.key==='Enter') sendChatMessage();" />
          <button class="btn-primary-gold" onclick="sendChatMessage()" style="padding:14px 24px; border-radius:999px;">
            Send ✦
          </button>
        </div>
        <div style="margin-top:14px; padding:10px 16px; background:rgba(201,162,39,0.06); border:1px solid rgba(201,162,39,0.22); border-radius:10px; font-size:0.80rem; color:#7A654D; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px;">
          <span>✦ <strong>Transparent Usage:</strong> 3 free exploratory inquiries included. Each question evaluates your verified chart against classical texts.</span>
          <a href="/pricing/#charm-ai" style="color:#8B6914; font-weight:700; text-decoration:underline;">Explore Charm AI Passes (from ₹199) →</a>
        </div>'''

if old_charm_input in content:
    content = content.replace(old_charm_input, new_charm_input)
    print("Updated Charm AI: Added transparent usage limits and pass links")
else:
    print("Warning: old_charm_input not found")

# 4. Update Section 8 (Reports & Pricing): Re-order to Basic -> Advanced -> Premium with H2 "Choose Your Personalised Report"
old_reports_header = '''        <span class="sec-eyebrow">AUTHENTIC PRODUCTS &amp; CONFIGURED PRICING</span>
        <h2 class="sec-title">Numerology Reports and Consultations</h2>
        <p class="sec-sub">
          Choose from instant conversational queries, comprehensive multi-page dossiers, or private consultations with verified masters.
        </p>'''

new_reports_header = '''        <span class="sec-eyebrow">STANDARDISED TIERS · 100% DETERMINISTIC DELIVERY</span>
        <h2 class="sec-title">Choose Your Personalised Report</h2>
        <p class="sec-sub">
          Clear, tiered deliverables tailored to your depth of inquiry. Every report is generated server-side using 100% deterministic classical calculations.
        </p>'''

if old_reports_header in content:
    content = content.replace(old_reports_header, new_reports_header)
    print("Updated Reports Section: Header to 'Choose Your Personalised Report'")
else:
    print("Warning: old_reports_header not found")

# 5. Update Section 9 (Sample Report Preview) Heading
old_sample_header = '''        <span class="sec-eyebrow">ILLUSTRATIVE SPECIMEN · TRANSPARENT QUALITY</span>

        <h2 class="sec-title">Preview an Authentic Numeros Vision Dossier</h2>'''

new_sample_header = '''        <span class="sec-eyebrow">ILLUSTRATIVE SPECIMEN · TRANSPARENT QUALITY</span>

        <h2 class="sec-title">Preview a Sample Report</h2>'''

if old_sample_header in content:
    content = content.replace(old_sample_header, new_sample_header)
    print("Updated Sample Preview Heading to 'Preview a Sample Report'")
else:
    print("Warning: old_sample_header not found")

# 6. Update Section 10 (Learning Centre) Heading
old_insights_header = '''        <span class="sec-eyebrow">WISDOM &amp; NUMERICAL PHILOSOPHY</span>

        <h2 class="sec-title">From the Numeros Vision Learning Centre</h2>'''

new_insights_header = '''        <span class="sec-eyebrow">WISDOM &amp; NUMERICAL PHILOSOPHY</span>

        <h2 class="sec-title">Learn About Numerology</h2>'''

if old_insights_header in content:
    content = content.replace(old_insights_header, new_insights_header)
    print("Updated Insights Heading to 'Learn About Numerology'")
else:
    print("Warning: old_insights_header not found")

# 7. Update Closing CTA Section: "Start with a Free Calculation"
old_closing_cta = '''      <span class="sec-eyebrow">✦ START WITH YOUR NUMBERS ✦</span>
      <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.4rem; color:var(--gold-dark); margin:8px 0 14px;">
        Begin with a Free Calculation
      </h2>'''

new_closing_cta = '''      <span class="sec-eyebrow">✦ START WITH YOUR NUMBERS ✦</span>
      <h2 style="font-family:'Cormorant Garamond',serif; font-size:2.4rem; color:var(--gold-dark); margin:8px 0 14px;">
        Start with a Free Calculation
      </h2>'''

if old_closing_cta in content:
    content = content.replace(old_closing_cta, new_closing_cta)
    print("Updated Closing CTA to 'Start with a Free Calculation'")
else:
    print("Warning: old_closing_cta not found")

# 8. Update Trust Section: "Privacy, Methodology and Responsible Guidance"
old_trust = '''      <span class="sec-eyebrow">ETHICAL COMPLIANCE &amp; DATA GOVERNANCE</span>

      <h3 style="font-family:'Cormorant Garamond',serif; font-size:2rem; color:var(--gold-dark); margin:6px 0 12px;">

        Dedicated to Privacy, Integrity, and Non-Exploitation

      </h3>'''

new_trust = '''      <span class="sec-eyebrow">ETHICAL COMPLIANCE &amp; DATA GOVERNANCE</span>

      <h2 class="sec-title" style="font-family:'Cormorant Garamond',serif; font-size:2.2rem; color:var(--gold-dark); margin:6px 0 12px;">

        Privacy, Methodology and Responsible Guidance

      </h2>'''

if old_trust in content:
    content = content.replace(old_trust, new_trust)
    print("Updated Trust Section to H2 'Privacy, Methodology and Responsible Guidance'")
else:
    print("Warning: old_trust not found")

with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Homepage canonical headings audit update completed successfully!")
