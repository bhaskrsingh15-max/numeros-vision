import os
import re

def update_index_html():
    path = 'app/static/index.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    old_block = '''      <!-- Consultation Banner -->
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

    new_block = '''      <!-- Consultation Banner -->
      <div id="consultation" style="background:#FFFFFF; border:1.5px solid var(--border-amber); border-radius:20px; padding:36px; margin-top:32px; box-shadow:var(--shadow-amber); display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:20px;">
        <div style="max-width:640px;">
          <span class="sec-eyebrow">BESPOKE 1-ON-1 GUIDANCE · ENQUIRY-FIRST ADVISORY</span>
          <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.8rem; color:var(--gold-dark); margin:4px 0 8px;">
            Personalised One-on-One Consultation
          </h3>
          <p style="font-size:0.9rem; color:var(--text-muted); margin:0 0 10px; line-height:1.6;">
            Explore a one-to-one consultation to discuss your questions about numerology, name analysis, Lo Shu Grid interpretations, personal cycles or other supported areas. Share your requirements and questions with us. We will review your enquiry and contact you to discuss your requirements, the suitable consultation format, availability and applicable fee.
          </p>
          <div style="display:flex; gap:16px; flex-wrap:wrap; font-size:0.82rem; color:#7A654D; margin-top:8px;">
            <span>✦ Personal Numerology &amp; Cycles</span>
            <span>✦ Tailored Remedial Guidance</span>
            <span>✦ Scope &amp; Fee Discussed Personally</span>
            <span>✦ Zero Upfront Payment Obligation</span>
          </div>
        </div>
        <div style="display:flex; flex-direction:column; gap:10px; align-items:stretch; min-width:260px;">
          <a href="/consultation/" class="btn-primary-gold" style="justify-content:center; padding:14px 24px; font-weight:700; text-decoration:none; text-align:center;">
            Express My Interest ✦
          </a>
          <a href="/reports_catalogue/" class="btn-secondary-pearl" style="justify-content:center; font-size:0.82rem; padding:8px 16px; text-decoration:none; text-align:center;">
            View Standalone Reports Catalogue →
          </a>
        </div>
      </div>'''

    # Normalize CRLF
    content_norm = content.replace('\r\n', '\n')
    old_norm = old_block.replace('\r\n', '\n')
    new_norm = new_block.replace('\r\n', '\n')

    if old_norm in content_norm:
        content_norm = content_norm.replace(old_norm, new_norm, 1)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content_norm)
        print('Successfully updated index.html consultation banner!')
    else:
        print('WARNING: old_norm not found in index.html')

if __name__ == '__main__':
    update_index_html()

def update_pricing_html():
    path = 'app/static/pricing.html'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read().replace('\r\n', '\n')

    # 1. Header CTA
    content = content.replace(
        '<a href="/consultation/" class="nv-btn-cta">Book Consultation ✦</a>',
        '<a href="/consultation/" class="nv-btn-cta">Personal Consultation ✦</a>'
    )

    # 2. Table row
    old_row = '''            <tr>
              <td style="padding:14px 16px; font-weight:700; color:#2C2214;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="color:#8B6914;">👑</span> Bespoke VIP Consultation
                  <span style="font-size:0.65rem; background:#8B6914; color:#FFFFFF; padding:2px 6px; border-radius:4px; font-weight:700; text-transform:uppercase;">Royal</span>
                </div>
              </td>
              <td style="padding:14px 16px; color:#523E28;">45m Private Video Session + Direct Q&A + Remedial Plan</td>
              <td style="padding:14px 16px; font-weight:800; color:#8B6914; font-size:1.15rem;">₹1,050</td>
              <td style="padding:14px 16px; color:#7A654D;">One-Time</td>
              <td style="padding:14px 16px; text-align:right;">
                <a href="/#consultation" class="btn-gold-action" style="padding:6px 16px; font-size:0.78rem; text-decoration:none; display:inline-block; border-radius:8px; background:linear-gradient(135deg,#8B6914,#C9A227);">
                  Book VIP (₹1,050)
                </a>
              </td>
            </tr>'''

    new_row = '''            <tr>
              <td style="padding:14px 16px; font-weight:700; color:#2C2214;">
                <div style="display:flex; align-items:center; gap:8px;">
                  <span style="color:#8B6914;">👤</span> Personalised Consultation
                  <span style="font-size:0.65rem; background:#16835B; color:#FFFFFF; padding:2px 6px; border-radius:4px; font-weight:700; text-transform:uppercase;">Enquiry</span>
                </div>
              </td>
              <td style="padding:14px 16px; color:#523E28;">One-to-One Session · Scope, format and fee discussed personally</td>
              <td style="padding:14px 16px; font-weight:700; color:#8B6914; font-size:0.95rem;">Enquiry-Based</td>
              <td style="padding:14px 16px; color:#7A654D;">Bespoke</td>
              <td style="padding:14px 16px; text-align:right;">
                <a href="/consultation/" class="btn-gold-action" style="padding:6px 16px; font-size:0.78rem; text-decoration:none; display:inline-block; border-radius:8px; background:linear-gradient(135deg,#8B6914,#C9A227);">
                  Express My Interest →
                </a>
              </td>
            </tr>'''

    if old_row in content:
        content = content.replace(old_row, new_row, 1)
        print('Successfully updated pricing table row in pricing.html')
    else:
        print('WARNING: old_row not found in pricing.html')

    # 3. High-Ticket VIP Sessions Section
    old_card = '''        <!-- 1-on-1 VIP Master Session -->
        <div style="background:#FFFDF7; border:2px solid var(--gold); border-radius:14px; padding:24px; position:relative; display:flex; flex-direction:column; height:100%;">
          <div style="position:absolute;top:-11px;right:16px;background:var(--gold);color:#FFFDF7;font-size:0.64rem;font-weight:700;padding:3px 10px;border-radius:10px;text-transform:uppercase;letter-spacing:0.06em;font-family:'Cinzel',serif;">EXPERT CONSULTATION</div>
          <div class="harmonic-root-badge" id="vip-session-root">HARMONIC ROOT 6 · VENUS OPULENCE</div>
          <h4 style="font-family:'Cormorant Garamond',serif; font-size:1.45rem; color:#8B6914; margin:0 0 6px 0; min-height:44px; display:flex; align-items:center;">1-on-1 VIP Master Personal Session</h4>
          <div style="font-size:1.6rem; font-weight:700; color:#8B6914; margin-bottom:8px;" id="vip-session-price">₹1,050</div>
          <p style="font-size:0.83rem; color:#6B5E4F; line-height:1.6; margin-bottom:18px; flex:1;">
            Private 45-minute video session with senior numerologist, direct Q&A, and personalized remedial roadmap.
          </p>
          <div style="margin-top:auto; padding-top:14px;">
            <a href="/#consultation" class="btn-gold-action">Book Private Master Session →</a>
          </div>
        </div>'''

    new_card = '''        <!-- Personalised One-on-One Consultation -->
        <div style="background:#FFFDF7; border:2px solid var(--gold); border-radius:14px; padding:24px; position:relative; display:flex; flex-direction:column; height:100%;">
          <div style="position:absolute;top:-11px;right:16px;background:var(--gold);color:#FFFDF7;font-size:0.64rem;font-weight:700;padding:3px 10px;border-radius:10px;text-transform:uppercase;letter-spacing:0.06em;font-family:'Cinzel',serif;">ENQUIRY SERVICE</div>
          <div class="harmonic-root-badge" id="vip-session-root">ONE-ON-ONE ADVISORY</div>
          <h4 style="font-family:'Cormorant Garamond',serif; font-size:1.45rem; color:#8B6914; margin:0 0 6px 0; min-height:44px; display:flex; align-items:center;">Personalised One-on-One Consultation</h4>
          <div style="font-size:1.15rem; font-weight:700; color:#8B6914; margin-bottom:8px;" id="vip-session-price">Enquiry-Based Advisory</div>
          <p style="font-size:0.83rem; color:#6B5E4F; line-height:1.6; margin-bottom:18px; flex:1;">
            Explore a one-to-one consultation to discuss your questions about numerology, name analysis, Lo Shu Grid interpretations, personal cycles or other supported areas. Scope, fee and availability are discussed personally after reviewing your enquiry.
          </p>
          <div style="margin-top:auto; padding-top:14px;">
            <a href="/consultation/" class="btn-gold-action" style="text-decoration:none;">Express My Interest →</a>
          </div>
        </div>'''

    if old_card in content:
        content = content.replace(old_card, new_card, 1)
        print('Successfully updated VIP card in pricing.html')
    else:
        print('WARNING: old_card not found in pricing.html')

    # 4. JS renderPricing updates
    content = content.replace(
        "sessionEl.innerHTML = '₹1,050';",
        "sessionEl.innerHTML = 'Enquiry-Based Advisory';"
    )
    content = content.replace(
        "sessionEl.innerHTML = '$240.00 <span style=\"font-size:1rem;color:#9C8F80;text-decoration:line-through;font-weight:400;\">$510.00</span>';",
        "sessionEl.innerHTML = 'Enquiry-Based Advisory';"
    )

    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('pricing.html updated!')

if __name__ == '__main__':
    update_pricing_html()
