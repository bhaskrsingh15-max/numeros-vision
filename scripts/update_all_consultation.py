import os
import glob
import re

def update_all_consultation_references():
    print("=== STARTING COMPREHENSIVE CONSULTATION MONETISATION UPDATE ===")

    # 1. Update app/static/index.html
    idx_path = 'app/static/index.html'
    if os.path.exists(idx_path):
        with open(idx_path, 'r', encoding='utf-8') as f:
            c = f.read().replace('\r\n', '\n')
        # Ensure consultation banner CTA points to /consultation/ and has no price
        c = re.sub(
            r'Book Consultation \(₹1,050\)[^<]*',
            'Express My Interest ✦',
            c
        )
        c = re.sub(
            r'1-on-1 Expert Consultation \(<span style="color:#8B6914; font-weight:700;">₹1,050</span>\)',
            'Personalised One-on-One Consultation',
            c
        )
        with open(idx_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Updated index.html")

    # 2. Update app/static/pricing.html
    pricing_path = 'app/static/pricing.html'
    if os.path.exists(pricing_path):
        with open(pricing_path, 'r', encoding='utf-8') as f:
            c = f.read().replace('\r\n', '\n')

        # Header CTA
        c = c.replace(
            '<a href="/consultation/" class="nv-btn-cta">Book Consultation ✦</a>',
            '<a href="/consultation/" class="nv-btn-cta">Personal Consultation ✦</a>'
        )

        # Meta description and schema
        c = c.replace(
            'Transparent fee schedule and consultation packages for Numeros Vision services.',
            'Transparent fee schedule for standalone reports and enquiry-based personalised consultations for Numeros Vision services.'
        )

        # Table row
        c = re.sub(
            r'<tr>\s*<td[^>]*>\s*<div[^>]*>\s*<span[^>]*>👑</span>\s*Bespoke VIP Consultation[\s\S]*?</tr>',
            '''<tr>
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
            </tr>''',
            c,
            flags=re.MULTILINE
        )

        # High-Ticket VIP Sessions Section card
        c = re.sub(
            r'<!-- 1-on-1 VIP Master Session -->[\s\S]*?<!-- Supported Payment Modes -->',
            '''<!-- Personalised One-on-One Consultation -->
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
        </div>
      </div>
    </div>

    <!-- Supported Payment Modes -->''',
            c
        )

        # Update JS renderPricing
        c = c.replace(
            "sessionEl.innerHTML = '₹1,050';",
            "sessionEl.innerHTML = 'Enquiry-Based Advisory';"
        )
        c = c.replace(
            "sessionEl.innerHTML = '$240.00 <span style=\"font-size:1rem;color:#9C8F80;text-decoration:line-through;font-weight:400;\">$510.00</span>';",
            "sessionEl.innerHTML = 'Enquiry-Based Advisory';"
        )
        # Update DOMAIN_DATA vip prices
        c = c.replace(
            "tripwire: { name: '1-on-1 Consultation Call (45m)', price: '₹199', note: 'Direct Private Audio/Video Call with Senior Numerologist' },",
            "tripwire: { name: 'Personalised One-on-One Consultation', price: 'Enquiry', note: 'Scope, fee and availability discussed personally' },"
        )
        c = c.replace(
            "sovereign: { name: 'VIP Master Consultation Session', price: '₹1,050', note: '60-min Deep-Dive with Founder + Comprehensive Detailed Report' }",
            "sovereign: { name: 'Personalised Consultation Advisory', price: 'Enquiry', note: 'Direct advisory with scope and fee discussed personally' }"
        )
        c = c.replace(
            "tripwire: { name: '1-on-1 Consultation Call (45m)', price: '$49.00', strike: '$99.00', note: 'Direct Private Audio/Video Call with Senior Numerologist' },",
            "tripwire: { name: 'Personalised One-on-One Consultation', price: 'Enquiry', strike: '', note: 'Scope, fee and availability discussed personally' },"
        )
        c = c.replace(
            "sovereign:{ name: 'VIP Master Consultation Session', price: '$240.00', strike: '$510.00', note: '60-min Deep-Dive with Founder + Comprehensive Detailed Report' }",
            "sovereign:{ name: 'Personalised Consultation Advisory', price: 'Enquiry', strike: '', note: 'Direct advisory with scope and fee discussed personally' }"
        )

        with open(pricing_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Updated pricing.html")

    # 3. Update app/static/reports_catalogue.html
    rep_path = 'app/static/reports_catalogue.html'
    if os.path.exists(rep_path):
        with open(rep_path, 'r', encoding='utf-8') as f:
            c = f.read().replace('\r\n', '\n')

        old_rep_card = '''        <div class="bundle-card featured">
          <div>
            <span class="report-category-pill" style="margin-bottom:12px; display:inline-block; background:rgba(22,131,91,0.12); color:var(--emerald);">Human Expert</span>
            <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:0 0 8px; font-size:1.25rem;">1-on-1 Certified Video Consultation</h3>
            <p style="font-size:0.88rem; color:var(--ink-muted); margin-bottom:16px;">45-minute private confidential consultation with a senior Numeros Vision certified practitioner.</p>
            <ul class="deliverables-list">
              <li>Live verification of birth time and planetary charts</li>
              <li>Personalized answers to career, marriage, and family questions</li>
              <li>Custom safe gemstone and acoustic name rectification advice</li>
              <li>Full recording + post-call PDF summary included</li>
            </ul>
          </div>
          <div>
            <div class="card-price-display">
              <span class="price-amount">₹1,050</span>
              <span class="price-pages-tag">45 Minutes · Google Meet</span>
            </div>
            <a href="/consultation/" class="btn-gold-primary" style="width:100%; box-sizing:border-box;">Book 1-on-1 Session ✦</a>
          </div>
        </div>'''

        new_rep_card = '''        <div class="bundle-card featured">
          <div>
            <span class="report-category-pill" style="margin-bottom:12px; display:inline-block; background:rgba(22,131,91,0.12); color:var(--emerald);">Enquiry-Based Advisory</span>
            <h3 style="font-family:'Cinzel',serif; color:var(--gold-dark); margin:0 0 8px; font-size:1.25rem;">Personalised One-on-One Consultation</h3>
            <p style="font-size:0.88rem; color:var(--ink-muted); margin-bottom:16px;">Direct private advisory with a verified numerologist to discuss your questions about personal numerology, name analysis, Lo Shu Grid interpretations, or personal cycles.</p>
            <ul class="deliverables-list">
              <li>Review of your specific questions, requirements, and life context</li>
              <li>Discussion of suitable consultation format, scope, and availability</li>
              <li>Transparent fee communicated personally after enquiry review</li>
              <li>Submitting an enquiry expresses interest only with zero payment obligation</li>
            </ul>
          </div>
          <div>
            <div class="card-price-display">
              <span class="price-amount" style="font-size:1.15rem; color:var(--gold-dark);">Enquiry-Based</span>
              <span class="price-pages-tag">Scope &amp; Fee Discussed Personally</span>
            </div>
            <a href="/consultation/" class="btn-gold-primary" style="width:100%; box-sizing:border-box; text-decoration:none; display:inline-block; text-align:center;">Express My Interest ✦</a>
          </div>
        </div>'''

        if old_rep_card in c:
            c = c.replace(old_rep_card, new_rep_card, 1)
            print("Updated reports_catalogue.html consultation card")
        else:
            print("WARNING: old_rep_card not matched directly, checking regex")
            c = re.sub(
                r'<div class="bundle-card featured">\s*<div>\s*<span[^>]*>Human Expert</span>[\s\S]*?Book 1-on-1 Session ✦</a>\s*</div>\s*</div>',
                new_rep_card.strip(),
                c
            )
            print("Applied regex update to reports_catalogue.html")

        with open(rep_path, 'w', encoding='utf-8') as f:
            f.write(c)

    # 4. Update tools/name-balancing.html
    nb_path = 'app/static/tools/name-balancing.html'
    if os.path.exists(nb_path):
        with open(nb_path, 'r', encoding='utf-8') as f:
            c = f.read().replace('\r\n', '\n')
        c = c.replace(
            '📞 Book 1-on-1 Name Balancing Consultation (₹1,050) →',
            '📞 Personalised One-on-One Consultation · Express Interest →'
        )
        c = c.replace(
            'href="/#consultation"',
            'href="/consultation/"'
        )
        c = c.replace(
            'Private 45-minute live consultation with Master Numerologist · Tailored Auspicious Spelling Variations Aligned to Your Unique Birth Blueprint · Signature Calibration · Daily Writing Attunement Protocol',
            'Personalised advisory to discuss name spelling variations, signature calibration, and personal cycles. Scope, availability and fee discussed personally after enquiry review.'
        )
        with open(nb_path, 'w', encoding='utf-8') as f:
            f.write(c)
        print("Updated tools/name-balancing.html")

    # 5. Update blog & amp articles
    blog_files = glob.glob('app/static/blog/*.html') + glob.glob('app/static/amp/blog/*.html')
    for bp in blog_files:
        with open(bp, 'r', encoding='utf-8') as f:
            c = f.read()
        changed = False
        if '1-on-1 Consultation (₹1,050)' in c:
            c = c.replace('1-on-1 Consultation (₹1,050)', 'One-on-One Consultation')
            changed = True
        if '1-on-1 Master Session (₹1,050)' in c:
            c = c.replace('1-on-1 Master Session (₹1,050)', 'One-on-One Consultation')
            changed = True
        if 'Consultation (₹1,050)' in c:
            c = c.replace('Consultation (₹1,050)', 'One-on-One Consultation')
            changed = True
        if changed:
            with open(bp, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Updated blog file: {bp}")

    print("=== FINISHED COMPREHENSIVE CONSULTATION MONETISATION UPDATE ===")

if __name__ == '__main__':
    update_all_consultation_references()

def clean_remaining_consultation_mentions():
    print("=== CLEANING REMAINING CONSULTATION FEE MENTIONS ===")

    # 1. pricing.html meta description
    with open('app/static/pricing.html', 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace(
        'bundles, Charm AI passes, and 1-on-1 consultations.',
        'bundles, Charm AI passes, and enquiry-based one-on-one consultations.'
    )
    c = c.replace(
        'astrology consultation fee, sacred pricing, ',
        ''
    )
    with open('app/static/pricing.html', 'w', encoding='utf-8') as f:
        f.write(c)

    # 2. cdp.html internal simulator
    with open('app/static/cdp.html', 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace(
        '<option value="2499">₹2,499 (1-on-1 Consultation Client)</option>',
        '<option value="2499">1-on-1 Consultation Enquiry Client</option>'
    )
    with open('app/static/cdp.html', 'w', encoding='utf-8') as f:
        f.write(c)

    # 3. Blog files regex replacement
    blog_files = glob.glob('app/static/blog/*.html') + glob.glob('app/static/amp/blog/*.html')
    for bp in blog_files:
        with open(bp, 'r', encoding='utf-8') as f:
            c = f.read()
        # Replace any 📞 Book 1-on-1 ... Session (₹1,050)
        c_new = re.sub(
            r'📞\s*(?:Book\s*)?1-on-1\s*[^<]*?(?:Session|Consultation)\s*(?:&amp;[^<]*?)?\(₹1,050\)',
            '📞 One-on-One Consultation',
            c
        )
        if c_new != c:
            with open(bp, 'w', encoding='utf-8') as f:
                f.write(c_new)
            print(f"Cleaned blog: {bp}")

    print("=== FINISHED CLEANING REMAINING MENTIONS ===")

if __name__ == '__main__':
    clean_remaining_consultation_mentions()
