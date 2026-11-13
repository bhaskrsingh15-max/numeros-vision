# update_consultation_page.py
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('app/static/consultation.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the 2 cards with the unified ₹1,050 offering
old_grid = '''    <div class="consult-grid">
      <!-- 45-min Phone Consultation -->
      <div class="consult-card">
        <div>
          <span style="font-size:0.76rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase; letter-spacing:0.1em; display:block; margin-bottom:8px;">FOCUSED STRATEGY SESSION</span>
          <h2>45-Minute Phone Consultation</h2>
          <div class="consult-price">₹2,499 <span style="font-size:0.85rem; color:#7A654D; font-family:'Inter',sans-serif; font-weight:400;">/ one-time</span></div>
          <p style="font-size:0.88rem; color:#7A654D; margin-bottom:16px;">
            A targeted session dedicated to resolving 2–3 immediate career, relationship, or name alignment decisions with a senior practitioner.
          </p>
          <ul class="consult-features">
            <li>45-Minute 1-on-1 voice session with Master Numerologist</li>
            <li>Birth details verification & celestial alignment review</li>
            <li>Detailed post-call remedy summary PDF delivered via email</li>
            <li>WhatsApp confirmation & slot scheduling within 2 hours</li>
          </ul>
        </div>
        <a href="/pricing/" class="nv-btn-cta" style="width:100%; text-align:center; justify-content:center;">Book 45-Min Session ✦</a>
      </div>

      <!-- 90-min Master Consultation -->
      <div class="consult-card" style="border-color:var(--gold); box-shadow:0 8px 32px rgba(201,162,39,0.18);">
        <div>
          <span style="font-size:0.76rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase; letter-spacing:0.1em; display:block; margin-bottom:8px;">VIP SOVEREIGN IMMERSION</span>
          <h2>1-on-1 Master Personal Consultation</h2>
          <div class="consult-price">₹11,400 <span style="font-size:0.85rem; color:#7A654D; font-family:'Inter',sans-serif; font-weight:400;">/ 90 min</span></div>
          <p style="font-size:0.88rem; color:#7A654D; margin-bottom:16px;">
            Our most comprehensive private session. Complete life roadmap, deep multi-system chart synthesis, customized yantra guidance, and 30-day priority WhatsApp support.
          </p>
          <ul class="consult-features">
            <li>90-Minute private master consultation (Video or In-person)</li>
            <li>Birth Epoch Verification & deep 6-system chart synthesis</li>
            <li>Custom hand-crafted remedy plan & crystal prescription</li>
            <li>30-Day direct priority WhatsApp guidance with practitioner</li>
            <li>Comprehensive Deluxe Destiny Dossier PDF included</li>
            <li>Full session recording & actionable milestone roadmap</li>
          </ul>
        </div>
        <a href="/pricing/" class="nv-btn-cta" style="width:100%; text-align:center; justify-content:center;">Book Master VIP Session ✦</a>
      </div>
    </div>'''

new_grid = '''    <div class="consult-grid" style="grid-template-columns: minmax(300px, 680px); justify-content: center;">
      <!-- Single Standard 45-min Expert Consultation -->
      <div class="consult-card" style="border: 2px solid var(--gold); box-shadow: 0 10px 36px rgba(201,162,39,0.18);">
        <div>
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
            <span style="font-size:0.76rem; font-weight:700; color:var(--gold-dark); text-transform:uppercase; letter-spacing:0.1em;">CERTIFIED SENIOR PRACTITIONER</span>
            <span style="font-size:0.72rem; background:rgba(201,162,39,0.15); color:#8B6914; padding:3px 10px; border-radius:12px; font-weight:700;">ANVEIL EVERY CHARM</span>
          </div>
          <h2 style="font-size:1.8rem; margin:6px 0 10px;">1-on-1 Expert Consultation</h2>
          <div class="consult-price" style="font-size:2.2rem; color:#8B6914; font-weight:800;">₹1,050 <span style="font-size:0.85rem; color:#7A654D; font-family:'Inter',sans-serif; font-weight:400;">/ 45-Minute Session</span></div>
          <p style="font-size:0.92rem; color:#7A654D; margin:12px 0 18px; line-height:1.6;">
            A private, focused video or phone consultation with a verified senior numerologist. Direct answers to your personal crossroads, birth time rectification (BTR), safe non-fear remedies, plus a complimentary 12-page Advanced Dossier.
          </p>
          <ul class="consult-features" style="line-height:1.8;">
            <li>✦ <strong>45-Minute Private Session:</strong> One-on-one Google Meet or Phone call</li>
            <li>✦ <strong>Deterministic Chart Audit:</strong> Birth Time Rectification &amp; Dasha cycle analysis</li>
            <li>✦ <strong>Complimentary Master Dossier:</strong> Free 12-Page Advanced PDF (₹510 value) included</li>
            <li>✦ <strong>Safe Remedies:</strong> Non-fear gemstones, yantras, name balancing &amp; spatial advice</li>
            <li>✦ <strong>Audio Recording:</strong> Complete session recording and written takeaway roadmap</li>
            <li>✦ <strong>Flexible Rescheduling:</strong> Free 1-time date change up to 24 hours in advance</li>
          </ul>
        </div>
        <div style="margin-top:24px; display:flex; flex-direction:column; gap:12px;">
          <a href="/#consultation" class="nv-btn-cta" style="width:100%; text-align:center; justify-content:center; padding:14px 24px; font-size:1rem; font-weight:700;">
            Book Consultation (₹1,050) ✦
          </a>
          <div style="text-align:center; font-size:0.82rem; color:#7A654D;">
            Looking for written reports instead? <a href="/reports_catalogue/" style="color:#8B6914; font-weight:600; text-decoration:underline;">Explore Reports Catalogue (from ₹199) →</a>
          </div>
        </div>
      </div>
    </div>'''

if old_grid in text:
    text = text.replace(old_grid, new_grid)
    with open('app/static/consultation.html', 'w', encoding='utf-8') as f:
        f.write(text)
    print('Successfully updated consultation.html to single ₹1,050 tier!')
else:
    print('old_grid not found in consultation.html')
