/**
 * NUMEROS VISION — UNIFIED MARKETING FUNNEL & CONVERSION FRAMEWORK (v2.1.0)
 * Brand Tagline: ANVEIL EVERY CHARM
 *
 * Synced with app/config/packs.json.
 * Enforces:
 *   - Strictly ZERO raw black #000000
 *   - All prices in theme gold (#8B6914)
 *   - Zero strike-through or fake anchor discounts
 *   - Canonical pack names, prices, and page counts from packs.json
 */

(function (window, document) {
  'use strict';

  const CATALOG = {
    birth_number: {
      id: 'birth_number',
      name: 'Birth Number Analysis',
      curiosity_hook: 'Want to Explore Your Number Further?',
      value_bridge: 'Your free calculation provides your foundational Driver (Mulank) frequency. Explore the complete dossier to understand planetary harmonics, career resonance, and personal year cycles.',
      primary_cta: 'View Anveil my alignments →',
      secondary_cta: 'Compare Report Packages',
      tertiary_link: 'Preview a Sample Report',
      plan_id: 'report_basic',
      plan_name: 'Anveil my alignments',
      price_inr: 199,
      root: 1,
      deliverables: [
        '3-Page Personalised Executive PDF',
        'Mulank (Driver) & Bhagyank (Conductor) Blueprint',
        'Lo Shu 3x3 Grid Matrix & Elemental Distribution',
        'Chaldean Single Root & Compound Letter Breakdown',
        '5-Element Balancing Actions'
      ]
    },
    life_path: {
      id: 'life_path',
      name: 'Life Path Calculator',
      curiosity_hook: 'Explore the Wider Life Path Picture',
      value_bridge: 'Pure calculation frequency reduces your birth epoch to your core Life Path. Explore the next layer to review element balancing and enabled numbers in depth.',
      primary_cta: 'Explore Anveil my glowing charms →',
      secondary_cta: 'Compare Report Packages',
      tertiary_link: 'Preview Sample Dossier',
      plan_id: 'report_advanced',
      plan_name: 'Anveil my glowing charms',
      price_inr: 510,
      root: 3,
      deliverables: [
        '12-Page Master Synthesis PDF Dossier',
        'Full Name vs Calling Name Chaldean Audit',
        'Complete Lo Shu Plane Analysis (Thought, Will, Action, Mental, Emotional)',
        'Enabled Numbers in Depth & Frequency Calibration',
        'Structured Cross-Factor Comparisons & Practical Guidance'
      ]
    },
    name_numerology: {
      id: 'name_numerology',
      name: 'Name Numerology',
      curiosity_hook: 'Review the Additional Number Breakdown',
      value_bridge: 'Your free result shows your single-digit expression number. The complete analysis evaluates full vs calling name harmony, compound number meaning, and element balancing.',
      primary_cta: 'View Anveil my alignments →',
      secondary_cta: 'Compare Report Packages',
      tertiary_link: 'How Name Balancing Works',
      plan_id: 'report_basic',
      plan_name: 'Anveil my alignments',
      price_inr: 199,
      root: 1,
      deliverables: [
        '3-Page Personalised Executive PDF',
        'Full Name Vibration vs Driver-Conductor Compatibility',
        'Chaldean Single Root & Compound Letter Breakdown',
        '5-Element Balancing Actions'
      ]
    },
    chaldean_name: {
      id: 'chaldean_name',
      name: 'Chaldean Name Numerology',
      curiosity_hook: 'Discover the Ancient Sound Frequencies',
      value_bridge: 'Chaldean numerology focuses on compound vibrations. Explore how your compound number interacts with your enabled chart numbers.',
      primary_cta: 'Explore Anveil my glowing charms →',
      secondary_cta: 'Compare Report Packages',
      tertiary_link: 'View Chaldean Methodology',
      plan_id: 'report_advanced',
      plan_name: 'Anveil my glowing charms',
      price_inr: 510,
      root: 3,
      deliverables: [
        '12-Page Master Synthesis PDF Dossier',
        'Chaldean Sound Frequency Analysis across all syllables',
        'Compound number symbolism & planetary ruler',
        'Enabled Numbers in Depth & Element Balancing'
      ]
    },
    lo_shu_grid: {
      id: 'lo_shu_grid',
      name: 'Lo Shu 3x3 Grid',
      curiosity_hook: 'Address Incomplete Energy Planes',
      value_bridge: 'Your free grid identifies present and missing numbers. The master report maps all 8 planes, element balancing, and enabled numbers in depth.',
      primary_cta: 'Explore Anveil my glowing charms →',
      secondary_cta: 'Preview the Detailed Grid Report',
      tertiary_link: 'Explore Plane Meanings',
      plan_id: 'report_advanced',
      plan_name: 'Anveil my glowing charms',
      price_inr: 510,
      root: 3,
      deliverables: [
        '12-Page Master Synthesis PDF Dossier',
        '8 Planes of Lo Shu comprehensive audit',
        'Central Brahmasthan Anchor Number 5 grounding protocol',
        'Element Balancing & Enabled Numbers in Depth'
      ]
    },
    mobile_numerology: {
      id: 'mobile_numerology',
      name: 'Mobile Number Numerology',
      curiosity_hook: 'Uncover Paired Digit Harmonics',
      value_bridge: 'Every mobile contact number emits repetitive frequencies. The full report audits all 9 adjacent pairs and evaluates alignment with your birth numbers.',
      primary_cta: 'Explore Anveil my glowing charms →',
      secondary_cta: 'View My Report Options',
      tertiary_link: 'Privacy & Data Masking Policy',
      plan_id: 'report_advanced',
      plan_name: 'Anveil my glowing charms',
      price_inr: 510,
      root: 3,
      deliverables: [
        '12-Page Master Synthesis PDF Dossier',
        'Complete 9-pair frequency audit (anti-pairs like 2-8, 4-8, 1-8)',
        'Commercial & wealth calling vibration assessment',
        'Zero PII retention policy guaranteed'
      ]
    },
    personal_year: {
      id: 'personal_year',
      name: 'Personal Year & Transit Engine',
      curiosity_hook: 'Map Your Foundational Alignment',
      value_bridge: 'Knowing your Personal Year number is step one. Explore your foundational Driver, Conductor, Lo Shu grid, and element balancing.',
      primary_cta: 'View Anveil my alignments →',
      secondary_cta: 'Compare Report Packages',
      tertiary_link: 'Review Forecast Methodology',
      plan_id: 'report_basic',
      plan_name: 'Anveil my alignments',
      price_inr: 199,
      root: 1,
      deliverables: [
        '3-Page Personalised Executive PDF',
        'Deterministic Mulank (Driver) & Bhagyank (Conductor) Calculations',
        'Lo Shu 3x3 Grid Matrix & Elemental Distribution',
        '5-Element Balancing Actions'
      ]
    },
    compatibility: {
      id: 'compatibility',
      name: 'Numerology Compatibility',
      curiosity_hook: 'Deepen Relational Synergy',
      value_bridge: 'Our free tool assesses Driver-Conductor natural harmony. The full relationship dossier explores elemental compatibility and constructive communication alignment.',
      primary_cta: 'Explore Anveil my glowing charms →',
      secondary_cta: 'Compare Report Packages',
      tertiary_link: 'View Synastry Principles',
      plan_id: 'report_advanced',
      plan_name: 'Anveil my glowing charms',
      price_inr: 510,
      root: 3,
      deliverables: [
        '12-Page Master Synthesis PDF Dossier',
        'Dual-Chart cross-synastry matrix',
        'Elemental compatibility (Fire, Water, Earth, Wood, Metal)',
        'Enabled Numbers in Depth & Practical Guidance'
      ]
    },
    business_direction: {
      id: 'business_direction',
      name: 'Business Direction & Entity Matrix',
      curiosity_hook: 'Align Corporate Brand with Market Timing',
      value_bridge: 'A business entity holds its own vibrational signature. Our sovereign blueprint validates trade name vibrations, founder synastry, and timing windows.',
      primary_cta: 'Explore Anveil every charm →',
      secondary_cta: 'Compare Business Options',
      tertiary_link: 'Corporate Confidentiality Terms',
      plan_id: 'report_premium',
      plan_name: 'Anveil every charm',
      price_inr: 1050,
      root: 6,
      deliverables: [
        '32-Page Sovereign Executive Master Blueprint PDF',
        'Corporate Legal Name & Trade Name vibration audit',
        'Founder & Co-Founder Synergy Compatibility Matrix',
        '10-Year Macro Planetary Timing Radar & Acute Execution Windows'
      ]
    },
    charm_ai: {
      id: 'charm_ai',
      name: 'Charm AI',
      curiosity_hook: 'Engage in Conversational Cosmic Counsel',
      value_bridge: 'Charm AI answers with authentic classical numerology synthesis. Start with 3 free questions after verified sign-up, or unlock 5 in-depth consultation questions for ₹199.',
      primary_cta: 'Explore Charm AI Starter Pack →',
      secondary_cta: 'Compare Charm AI Plans',
      tertiary_link: 'Review Classical Sources',
      plan_id: 'charm_single',
      plan_name: 'Charm AI Starter Pack',
      price_inr: 199,
      root: 1,
      deliverables: [
        '5 In-Depth Consultation Inquiries across any life area',
        'Acute execution timing windows (Hora & transit)',
        'Grounded non-fatalistic practical guidance',
        'Credits valid for 6 months'
      ]
    }
  };

  function trackEvent(eventName, productId, metadata) {
    try {
      if (localStorage.getItem('nv_marketing_opt_out') === 'true') return;
      if (typeof window.trackMarketingEvent === 'function') {
        window.trackMarketingEvent(eventName, { product_id: productId || 'unknown', ...(metadata || {}) });
      }
    } catch (e) {}
  }

  function isOptedOut() {
    return localStorage.getItem('nv_marketing_opt_out') === 'true';
  }

  function setOptOut(state) {
    if (state) {
      localStorage.setItem('nv_marketing_opt_out', 'true');
      trackEvent('marketing_opt_out', 'all');
    } else {
      localStorage.removeItem('nv_marketing_opt_out');
    }
  }

  function renderOfferBridge(container, options) {
    const el = typeof container === 'string' ? document.getElementById(container) : container;
    if (!el) return;

    if (isOptedOut()) {
      el.innerHTML = `
        <div style="background:var(--bg-card, #FFFDF7);border:1px dashed var(--border-gold, #C9A227);border-radius:12px;padding:14px 20px;text-align:center;margin-top:18px;">
          <p style="font-size:0.82rem;color:var(--text-muted, #7A654D);margin:0 0 6px 0;">
            ✦ Marketing prompts are paused. Your free calculation results are preserved.
          </p>
          <button type="button" id="btnResumeOffers" style="background:none;border:none;color:#8B6914;font-size:0.78rem;font-weight:600;cursor:pointer;text-decoration:underline;">
            Show personalized report options
          </button>
        </div>
      `;
      const resumeBtn = el.querySelector('#btnResumeOffers');
      if (resumeBtn) {
        resumeBtn.addEventListener('click', function() {
          setOptOut(false);
          renderOfferBridge(container, options);
        });
      }
      return;
    }

    const opts = options || {};
    const pid = opts.productId || 'life_path';
    const prod = CATALOG[pid] || CATALOG.life_path;
    const charmUrl = opts.askCharmUrl || `/charm-ai/?q=Tell+me+more+about+my+${encodeURIComponent(prod.name)}&auto=true`;

    const deliverablesHtml = prod.deliverables.map(d => `
      <li style="display:flex;align-items:flex-start;gap:8px;font-size:0.84rem;color:var(--text-primary, #523E28);line-height:1.55;margin-bottom:6px;">
        <span style="color:#16835B;font-weight:700;flex-shrink:0;">✓</span>
        <span>${d}</span>
      </li>
    `).join('');

    const html = `
      <div class="nv-funnel-offer-bridge" style="margin-top:24px;border:1.5px solid var(--border-gold, #C9A227);border-radius:18px;background:var(--bg-card, #FFFDF7);box-shadow:0 10px 32px rgba(180,155,110,0.1);overflow:hidden;position:relative;">
        <!-- Step 2: The Curiosity Bridge -->
        <div style="background:linear-gradient(135deg, rgba(201,162,39,0.08) 0%, rgba(22,131,91,0.04) 100%);padding:22px 24px;border-bottom:1px solid rgba(201,162,39,0.25);text-align:center;">
          <div style="display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;background:rgba(201,162,39,0.12);border:1.5px solid var(--gold, #C9A227);font-size:1.3rem;color:#8B6914;margin-bottom:8px;">
            🔒
          </div>
          <div style="font-size:0.70rem;letter-spacing:0.16em;text-transform:uppercase;color:#8B6914;font-weight:700;margin-bottom:4px;">
            NUMEROS VISION · ANVEIL EVERY CHARM
          </div>
          <h3 style="font-size:1.55rem;color:#523E28;margin:0 0 8px 0;font-weight:700;">
            Explore ${prod.plan_name}
          </h3>
          <p style="font-size:0.88rem;color:#7A654D;line-height:1.6;max-width:620px;margin:0 auto;">
            ${prod.value_bridge}
          </p>
        </div>

        <!-- Step 3: The Standard Upgrade Panel -->
        <div style="padding:22px 24px;">
          <div style="display:grid;grid-template-columns:1fr;gap:18px;">
            <div>
              <div style="font-size:0.74rem;letter-spacing:0.08em;text-transform:uppercase;color:#8B6914;font-weight:700;margin-bottom:10px;">
                Verified Inclusions in ${prod.plan_name}:
              </div>
              <ul style="list-style:none;padding:0;margin:0 0 16px 0;">
                ${deliverablesHtml}
              </ul>
            </div>

            <!-- Price & Action Area -->
            <div style="background:#F7F3EA;border:1px solid rgba(201,162,39,0.25);border-radius:14px;padding:16px 20px;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:14px;">
              <div>
                <div style="font-size:0.72rem;text-transform:uppercase;letter-spacing:0.08em;color:var(--text-muted, #7A654D);font-weight:600;margin-bottom:2px;">
                  Approved Single Investment
                </div>
                <div style="display:flex;align-items:baseline;gap:8px;">
                  <span style="font-size:1.6rem;font-weight:700;color:#8B6914;">
                    ₹${prod.price_inr.toLocaleString('en-IN')}
                  </span>
                </div>
                <div style="font-size:0.72rem;color:var(--text-muted, #7A654D);margin-top:2px;">
                  One-time purchase · Ready within minutes
                </div>
              </div>

              <!-- Primary CTA -->
              <div style="display:flex;flex-direction:column;gap:8px;min-width:240px;">
                <a href="/checkout/?plan=${prod.plan_id}&tool=${prod.id}" class="nv-funnel-btn-primary" data-product="${prod.id}" data-plan="${prod.plan_id}" style="display:inline-block;text-align:center;background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%);color:#FFFFFF;padding:12px 22px;border-radius:100px;font-weight:700;font-size:0.86rem;text-decoration:none;box-shadow:0 4px 14px rgba(139,105,20,0.25);transition:all 0.2s ease;">
                  🔒 Explore ${prod.plan_name} (₹${prod.price_inr.toLocaleString('en-IN')}) ✦
                </a>
              </div>
            </div>

            <!-- Secondary Actions & Reassurance Strip -->
            <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;padding-top:6px;border-top:1px solid rgba(201,162,39,0.15);">
              <div style="display:flex;gap:14px;flex-wrap:wrap;align-items:center;">
                <a href="/pricing/#plans" style="font-size:0.78rem;color:#8B6914;font-weight:600;text-decoration:underline;">
                  ${prod.secondary_cta}
                </a>
                <span style="font-size:0.75rem;color:var(--text-muted, #7A654D);">·</span>
                <a href="${charmUrl}" style="font-size:0.78rem;color:#16835B;font-weight:600;text-decoration:none;">
                  Ask Charm AI Free ✦
                </a>
                <span style="font-size:0.75rem;color:var(--text-muted, #7A654D);">·</span>
                <a href="/sample/" style="font-size:0.78rem;color:var(--text-muted, #7A654D);text-decoration:none;">
                  ${prod.tertiary_link}
                </a>
              </div>

              <div style="display:flex;align-items:center;gap:12px;">
                <span style="font-size:0.72rem;color:var(--text-muted, #7A654D);">
                  🔒 256-Bit Encrypted · Zero Dark Patterns
                </span>
                <button type="button" class="nv-funnel-opt-out" style="background:none;border:none;color:var(--text-muted, #7A654D);font-size:0.7rem;cursor:pointer;text-decoration:none;opacity:0.7;" title="Dismiss promotional offers">
                  Hide Offer ✕
                </button>
              </div>
            </div>

          </div>
        </div>
      </div>
    `;

    el.innerHTML = html;

    const primaryBtn = el.querySelector('.nv-funnel-btn-primary');
    if (primaryBtn) {
      primaryBtn.addEventListener('click', function () {
        trackEvent('checkout_started', prod.id, {
          plan_id: prod.plan_id,
          price_inr: prod.price_inr
        });
      });
    }

    const optOutBtn = el.querySelector('.nv-funnel-opt-out');
    if (optOutBtn) {
      optOutBtn.addEventListener('click', function () {
        setOptOut(true);
        renderOfferBridge(container, options);
      });
    }

    trackEvent('upgrade_panel_viewed', prod.id, {
      plan_id: prod.plan_id,
      price_inr: prod.price_inr
    });
  }

  window.nvFunnel = {
    renderOfferBridge: renderOfferBridge,
    trackEvent: trackEvent,
    isOptedOut: isOptedOut,
    setOptOut: setOptOut,
    CATALOG: CATALOG
  };

})(window, document);
