with open('app/static/charm_ai.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Clean headline lead
text = text.replace(
    'Consult Charm AI, our specialized conversational assistant grounded in authentic classical numerology wisdom. Ask open questions about your career timing, relationship dynamics, or crystal remedies with mathematical traceability.',
    'Consult Charm AI, your trusted conversational numerology advisor. Ask open questions about your career timing, relationship harmony, or personal milestones with authentic classical wisdom.'
)

# 2. Clean city label
text = text.replace(
    'Birth City (Optional for Topocentric Coordinates)',
    'Birth City (Optional for Regional Alignment)'
)

# 3. Clean status row
text = text.replace(
    '✓ Test Master Pass Active · 9,999 Questions &amp; Full Remedies Unlocked',
    '✦ Complimentary Consultation Active · Free Deep Reading'
)

# 4. Clean up conversion card and move Lo Shu grid out of locked container
old_card_block = """          <div style="margin-bottom:14px; font-size:0.96rem; line-height:1.75; color:#523E28;">
            ${formatMarkdown(answer)}
          </div>

          ${whyText ? `
            <div style="font-size:0.88rem; color:#523E28; line-height:1.68; margin-bottom:14px; background:#FAF6EE; padding:14px 18px; border-radius:12px; border-left:4px solid #C9A227; border:1px solid rgba(201,162,39,0.22); box-shadow:0 2px 8px rgba(180,155,110,0.06);">
              <strong style="color:#8B6914;">Planetary Alignment &amp; Root Cause:</strong><br />
              ${whyText}
            </div>
          ` : ''}

          <!-- CURIOSITY-BASED CONVERSION CARD (The Monetization Bridge) -->
          <div class="charm-curiosity-card">
            <div style="display:inline-flex; align-items:center; justify-content:center; width:44px; height:44px; border-radius:50%; background:rgba(201,162,39,0.12); border:1.5px solid var(--gold, #C9A227); font-size:1.35rem; color:#8B6914; margin-bottom:10px;">
              🔒
            </div>
            <div style="font-family:'Cinzel', serif; font-size:0.70rem; letter-spacing:0.16em; text-transform:uppercase; color:var(--gold-dark, #8B6914); font-weight:700; margin-bottom:4px;">
              NUMEROS VISION · ANVEIL EVERY CHARM
            </div>
            <h4 style="font-family:'Cormorant Garamond', serif; font-size:1.5rem; font-weight:700; color:#523E28; margin:0 0 8px; line-height:1.25;">
              ANVEIL Your Career &amp; Destiny Charm — Explore 5-Year Dasha Timeline &amp; Full Remedies
            </h4>
            <p style="font-size:0.86rem; color:var(--text-muted, #7A654D); line-height:1.6; max-width:640px; margin:0 auto 16px;">
              Charm AI has mapped your natal coordinates. While your direct foundational takeaway is active, 
              your <strong>high-probability career breakthrough milestone dates</strong>, 
              <strong>natal Lo Shu missing-digit neutralizers</strong>, and 
              <strong>consecrated 7-layer Upay remedies</strong> remain veiled inside your private dossier.
            </p>

            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:8px; text-align:left; max-width:680px; margin:0 auto 16px; background:#FFFDF7; border:1px solid rgba(201,162,39,0.25); border-radius:10px; padding:12px 16px; font-size:0.80rem; color:#523E28; font-weight:600;">
              <div>✦ 5-Year Vimshottari &amp; Numerology Dasha Progression Timeline</div>
              <div>✦ Natal Lo Shu Grid Missing Digit Neutralization Protocol</div>
              <div>✦ Personalized Consecrated Gemstone, Beej Mantra &amp; Crystal Prescription</div>
              <div>✦ Daily &amp; Monthly Auspicious Decision Windows (Muhurat Radar)</div>
            </div>

            <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:14px; flex-wrap:wrap;">
              <span style="font-size:0.95rem; text-decoration:line-through; color:var(--text-muted, #7A654D);">₹499</span>
              <span style="font-family:'Cinzel', serif; font-size:1.5rem; font-weight:800; color:var(--gold-dark, #8B6914);">₹249</span>
              <span style="font-size:0.70rem; font-weight:700; color:#16835B; background:rgba(22,131,91,0.12); padding:2px 8px; border-radius:999px; text-transform:uppercase;">SAVE 50% · INSTANT ACCESS</span>
            </div>

            <div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
              <a href="/checkout/?plan=ai_growth_15q&tool=charm-ai" style="display:inline-flex; align-items:center; justify-content:center; padding:12px 24px; background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFDF7; font-family:'Cinzel', serif; font-weight:700; font-size:0.84rem; letter-spacing:0.06em; border-radius:8px; text-decoration:none; box-shadow:0 4px 16px rgba(201,162,39,0.35);">
                <span>🔒 ANVEIL Your Career Charm · Explore Remedies (₹249) ✦</span>
              </a>
              <button type="button" onclick="toggleCharmUnlock('gatedCharmDetailed_${traceId}', this)" style="display:inline-flex; align-items:center; justify-content:center; padding:12px 16px; background:#FFFDF7; border:1.5px solid rgba(201,162,39,0.35); color:#523E28; font-weight:600; font-size:0.80rem; border-radius:8px; cursor:pointer;">
                <span>👁️ Preview Complete Reading (Practitioner Test Mode)</span>
              </button>
            </div>

            <div style="font-size:0.70rem; color:var(--text-muted, #7A654D);">
              Authentic Classical Numerology · Pure Mathematical Precision · 100% Confidential & Private
            </div>
          </div>

          <!-- PROPRIETARY DOSSIER MODULES (Veiled behind frosted glassmorphism in Free Mode) -->
          <div class="gated-charm-wrap locked" id="gatedCharmDetailed_${traceId}">
            ${charmCardHtml}
            ${loshuCardHtml}
            ${ageCardHtml}
            ${luckyHtml}
            ${remediesHtml}
            ${validationHtml}
          </div>"""

new_card_block = """          <div style="margin-bottom:18px; font-size:0.96rem; line-height:1.75; color:#523E28;">
            ${formatMarkdown(answer)}
          </div>

          <!-- FREE NATAL LO SHU GRID BIRTH CHART (Always Crisp and Beautifully Visible) -->
          ${loshuCardHtml}

          <!-- LUCKY HARMONIZERS CARD -->
          ${luckyHtml}

          ${whyText ? `
            <div style="font-size:0.88rem; color:#523E28; line-height:1.68; margin-top:16px; margin-bottom:16px; background:#FAF6EE; padding:14px 18px; border-radius:12px; border-left:4px solid #C9A227; border:1px solid rgba(201,162,39,0.22); box-shadow:0 2px 8px rgba(180,155,110,0.06);">
              <strong style="color:#8B6914;">Planetary Alignment &amp; Root Cause:</strong><br />
              ${whyText}
            </div>
          ` : ''}

          <!-- CURIOSITY-BASED CONVERSION CARD (The Monetization Bridge) -->
          <div class="charm-curiosity-card" style="margin-top:24px;">
            <div style="display:inline-flex; align-items:center; justify-content:center; width:44px; height:44px; border-radius:50%; background:rgba(201,162,39,0.12); border:1.5px solid var(--gold, #C9A227); font-size:1.35rem; color:#8B6914; margin-bottom:10px;">
              ✦
            </div>
            <div style="font-family:'Cinzel', serif; font-size:0.70rem; letter-spacing:0.16em; text-transform:uppercase; color:var(--gold-dark, #8B6914); font-weight:700; margin-bottom:4px;">
              NUMEROS VISION · ANVEIL EVERY CHARM
            </div>
            <h4 style="font-family:'Cormorant Garamond', serif; font-size:1.5rem; font-weight:700; color:#523E28; margin:0 0 8px; line-height:1.25;">
              Explore Your Full 5-Year Dasha Timeline &amp; Consecrated Remedies
            </h4>
            <p style="font-size:0.86rem; color:var(--text-muted, #7A654D); line-height:1.6; max-width:640px; margin:0 auto 16px;">
              Your foundational reading and natal grid are active above. To explore your complete month-by-month timing windows, 
              personalized milestone dates, and consecrated lifestyle remedies, unlock your full Charm AI pass or complete dossier.
            </p>

            <div style="display:grid; grid-template-columns:repeat(auto-fit, minmax(240px, 1fr)); gap:8px; text-align:left; max-width:680px; margin:0 auto 16px; background:#FFFDF7; border:1px solid rgba(201,162,39,0.25); border-radius:10px; padding:12px 16px; font-size:0.80rem; color:#523E28; font-weight:600;">
              <div>✦ 5-Year Vimshottari &amp; Numerology Dasha Progression Timeline</div>
              <div>✦ Monthly Breakthrough Corridors &amp; Auspicious Decision Dates</div>
              <div>✦ Personalized Consecrated Gemstone, Beej Mantra &amp; Crystal Harmony</div>
              <div>✦ Complete 12-Page Personalised Blueprint Dossier</div>
            </div>

            <div style="display:flex; align-items:center; justify-content:center; gap:10px; margin-bottom:14px; flex-wrap:wrap;">
              <span style="font-size:0.95rem; text-decoration:line-through; color:var(--text-muted, #7A654D);">₹499</span>
              <span style="font-family:'Cinzel', serif; font-size:1.5rem; font-weight:800; color:var(--gold-dark, #8B6914);">₹249</span>
              <span style="font-size:0.70rem; font-weight:700; color:#16835B; background:rgba(22,131,91,0.12); padding:2px 8px; border-radius:999px; text-transform:uppercase;">SPECIAL INTRODUCTORY PASS</span>
            </div>

            <div style="display:flex; justify-content:center; gap:10px; flex-wrap:wrap; margin-bottom:10px;">
              <a href="/checkout/?plan=ai_growth_15q&tool=charm-ai" style="display:inline-flex; align-items:center; justify-content:center; padding:12px 24px; background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFDF7; font-family:'Cinzel', serif; font-weight:700; font-size:0.84rem; letter-spacing:0.06em; border-radius:8px; text-decoration:none; box-shadow:0 4px 16px rgba(201,162,39,0.35);">
                <span>✦ Unlock Full Charm AI Pass (₹249) →</span>
              </a>
              <button type="button" onclick="toggleCharmUnlock('gatedCharmDetailed_${traceId}', this)" style="display:inline-flex; align-items:center; justify-content:center; padding:12px 16px; background:#FFFDF7; border:1.5px solid rgba(201,162,39,0.35); color:#523E28; font-weight:600; font-size:0.80rem; border-radius:8px; cursor:pointer;">
                <span>👁️ View Extended Chronological Analysis ↓</span>
              </button>
            </div>

            <div style="font-size:0.70rem; color:var(--text-muted, #7A654D);">
              Authentic Classical Numerology · 100% Confidential, Ethical &amp; Private
            </div>
          </div>

          <!-- PROPRIETARY DETAILED DOSSIER MODULES -->
          <div class="gated-charm-wrap locked" id="gatedCharmDetailed_${traceId}">
            ${charmCardHtml}
            ${ageCardHtml}
            ${remediesHtml}
            ${validationHtml}
          </div>"""

# Normalize CRLF
text_norm = text.replace("\r\n", "\n")
old_card_norm = old_card_block.replace("\r\n", "\n")
new_card_norm = new_card_block.replace("\r\n", "\n")

if old_card_norm in text_norm:
    text_norm = text_norm.replace(old_card_norm, new_card_norm)
    print("SUCCESS: Card and Lo Shu grid repositioned!")
else:
    print("WARNING: Could not find exact old card block, checking substring...")
    # Find start and end
    s_idx = text_norm.find('<!-- CURIOSITY-BASED CONVERSION CARD')
    e_idx = text_norm.find('${validationHtml}\n          </div>')
    print(f"s_idx: {s_idx}, e_idx: {e_idx}")

with open('app/static/charm_ai.html', 'w', encoding='utf-8') as f:
    f.write(text_norm)
