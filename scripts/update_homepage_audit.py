# update_homepage_audit.py
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Hero section
old_hero_actions = '''      <div class="hero-actions">
        <a href="#calculator-card" class="btn-primary-gold">
          <span>Calculate My Numbers Free</span>
          <span>✦</span>
        </a>
        <a href="#plans" class="btn-secondary-pearl">
          <span>Explore Numerology Reports</span>
          <span>→</span>
        </a>
      </div>'''

new_hero_actions = '''      <div class="hero-actions">
        <a href="#calculator-card" class="btn-primary-gold">
          <span>Start Free Calculation</span>
          <span>✦</span>
        </a>
        <a href="/reports_catalogue/" class="btn-secondary-pearl">
          <span>Explore Personalised Reports</span>
          <span>→</span>
        </a>
      </div>

      <!-- Editorial Metric Trust Cards (Orchestrix & Atelier Inspired) -->
      <div class="hero-trust-metrics" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(200px, 1fr)); gap:16px; max-width:960px; margin:44px auto 0; text-align:left;">
        <div style="background:rgba(255,253,247,0.92); border:1px solid rgba(201,162,39,0.3); border-radius:12px; padding:16px 20px; box-shadow:0 4px 16px rgba(201,162,39,0.06);">
          <div style="font-family:'Cinzel',serif; font-size:1.5rem; font-weight:700; color:var(--gold-dark);">100%</div>
          <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#8B6914; font-weight:700; margin-top:2px;">Deterministic Engine</div>
          <p style="font-size:0.78rem; color:#7A654D; margin:4px 0 0; line-height:1.4;">Zero AI hallucination in numbers. Classical formulas calculated mathematically.</p>
        </div>
        <div style="background:rgba(255,253,247,0.92); border:1px solid rgba(201,162,39,0.3); border-radius:12px; padding:16px 20px; box-shadow:0 4px 16px rgba(201,162,39,0.06);">
          <div style="font-family:'Cinzel',serif; font-size:1.5rem; font-weight:700; color:var(--gold-dark);">10+</div>
          <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#8B6914; font-weight:700; margin-top:2px;">Specialised Topics</div>
          <p style="font-size:0.78rem; color:#7A654D; margin:4px 0 0; line-height:1.4;">Dedicated reports for Career, Marriage, Business, Real Estate, Health &amp; more.</p>
        </div>
        <div style="background:rgba(255,253,247,0.92); border:1px solid rgba(201,162,39,0.3); border-radius:12px; padding:16px 20px; box-shadow:0 4px 16px rgba(201,162,39,0.06);">
          <div style="font-family:'Cinzel',serif; font-size:1.5rem; font-weight:700; color:var(--gold-dark);">3 Tiers</div>
          <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#8B6914; font-weight:700; margin-top:2px;">Unified Pricing</div>
          <p style="font-size:0.78rem; color:#7A654D; margin:4px 0 0; line-height:1.4;">Basic ₹199 (3p), Advanced ₹510 (12p), and Premium ₹1,050 (32p).</p>
        </div>
        <div style="background:rgba(255,253,247,0.92); border:1px solid rgba(201,162,39,0.3); border-radius:12px; padding:16px 20px; box-shadow:0 4px 16px rgba(201,162,39,0.06);">
          <div style="font-family:'Cinzel',serif; font-size:1.5rem; font-weight:700; color:var(--gold-dark);">9 Traditions</div>
          <div style="font-size:0.75rem; text-transform:uppercase; letter-spacing:0.08em; color:#8B6914; font-weight:700; margin-top:2px;">Cross-Synthesized</div>
          <p style="font-size:0.78rem; color:#7A654D; margin:4px 0 0; line-height:1.4;">Chaldean, Vedic, Pythagorean, Lo Shu, Western, Tamil, Kabbalah &amp; Chinese.</p>
        </div>
      </div>'''

if old_hero_actions in content:
    content = content.replace(old_hero_actions, new_hero_actions)
    print('Updated Hero Actions & Trust Cards')
else:
    print('Warning: old_hero_actions not found')

# 2. Update Consultation Banner
old_consultation = '''      <!-- Consultation Banner -->
      <div id="consultation" style="background:#FFFFFF; border:1.5px solid var(--border-amber); border-radius:20px; padding:36px; margin-top:32px; box-shadow:var(--shadow-amber); display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:20px;">
        <div style="max-width:600px;">
          <span class="sec-eyebrow">BESPOKE 1-ON-1 GUIDANCE</span>
          <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.8rem; color:var(--gold-dark); margin:4px 0 8px;">
            1-on-1 Astrologer Consultation (<span style="color:#8B6914; font-weight:700;">₹1,499</span>)
          </h3>
          <p style="font-size:0.9rem; color:var(--text-muted); margin:0 0 10px; line-height:1.6;">
            A private 45-minute audio/video session with a verified master numerologist. Receive direct answers to your personal crossroads, birth time calibration, and consecrated remedy guidance.
          </p>
          <p style="font-size:0.84rem; color:#8B6914; margin:0; line-height:1.5; font-weight:600;">
            👑 <strong>Bespoke VIP Consultation</strong> (<span style="color:#8B6914; font-weight:700;">₹11,400</span>): 90-minute private video session with founder, Birth Time Rectification (BTR), bespoke gemstone suitability &amp; 30-day priority WhatsApp guidance.
          </p>
        </div>
        <div style="display:flex; flex-direction:column; gap:10px; align-items:stretch;">
          <button class="btn-primary-gold" onclick="openCheckout('personal_consult', '1-on-1 Astrologer Consultation', 1499)">
            Book Consultation (₹1,499) ⚚
          </button>
          <button class="btn-secondary-pearl" onclick="openCheckout('personal_consult', 'Bespoke VIP Consultation', 11400)" style="font-size:0.8rem; padding:8px 16px;">
            Book Bespoke VIP Consultation (₹11,400)
          </button>
        </div>
      </div>'''

new_consultation = '''      <!-- Consultation Banner -->
      <div id="consultation" style="background:#FFFFFF; border:1.5px solid var(--border-amber); border-radius:20px; padding:36px; margin-top:32px; box-shadow:var(--shadow-amber); display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:20px;">
        <div style="max-width:640px;">
          <span class="sec-eyebrow">BESPOKE 1-ON-1 GUIDANCE</span>
          <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.8rem; color:var(--gold-dark); margin:4px 0 8px;">
            1-on-1 Expert Consultation (<span style="color:#8B6914; font-weight:700;">₹1,050</span>)
          </h3>
          <p style="font-size:0.9rem; color:var(--text-muted); margin:0 0 10px; line-height:1.6;">
            A private 45-minute video or phone session with a certified senior numerologist. Receive direct answers to your personal crossroads, birth time rectification, custom remedial protocols, plus a complimentary 12-page Advanced Dossier (₹510 value).
          </p>
          <div style="display:flex; gap:16px; flex-wrap:wrap; font-size:0.82rem; color:#7A654D; margin-top:8px;">
            <span>✦ 45-Min Private Session</span>
            <span>✦ Full Chart &amp; Dasha Audit</span>
            <span>✦ Free 12-Page Master Dossier</span>
            <span>✦ Audio Recording Included</span>
          </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:10px; align-items:stretch; min-width:260px;">
          <button class="btn-primary-gold" onclick="openCheckout('consultation_standard', '1-on-1 Expert Consultation', 1050)" style="justify-content:center; padding:14px 24px; font-weight:700;">
            Book Consultation (₹1,050) ⚚
          </button>
          <a href="/reports_catalogue/" class="btn-secondary-pearl" style="justify-content:center; font-size:0.82rem; padding:8px 16px;">
            View All Reports Catalogue →
          </a>
        </div>
      </div>'''

if old_consultation in content:
    content = content.replace(old_consultation, new_consultation)
    print('Updated Consultation Banner to Single ₹1,050')
else:
    print('Warning: old_consultation not found')

# 3. Update Calculator card sub
old_sub = '''        <p class="sec-sub">
          Enter your birth details below. Our deterministic calculation engine computes your Driver (Mulank), Conductor (Bhagyank/Life Path), and 3×3 Lo Shu grid.
        </p>'''

new_sub = '''        <p class="sec-sub">
          Enter your birth details below. Our deterministic calculation engine computes your Driver (Mulank), Conductor (Bhagyank/Life Path), and 3×3 Lo Shu grid. Free instant calculations provide core metrics; in-depth dasha timelines, name balancing, and personalized remedies are delivered in our downloadable reports.
        </p>'''

if old_sub in content:
    content = content.replace(old_sub, new_sub)
    print('Updated Calculator Subtitle')
else:
    print('Warning: old_sub not found')

with open('app/static/index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print('Finished updating index.html')
