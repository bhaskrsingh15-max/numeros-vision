/**
 * Numeros Vision — Unified Cookie & Data Collection Consent Manager
 * Version: 2026.2.DPDP_GDPR
 *
 * Compliant with:
 * - India: Digital Personal Data Protection Act, 2023 (DPDP Act 2023, Sec 5, 6, 8, 9, 11-14)
 * - EU & UK: General Data Protection Regulation (GDPR / UK GDPR, Art 6, 7, ePrivacy Directive)
 * - US / California: California Consumer Privacy Act & Rights Act (CCPA / CPRA)
 *
 * Aesthetic: Venus Pearl (#FFFDF7) & Jupiter Gold (#C9A227, #8B6914) Luxury Design
 * Strictly zero pure black (#000000).
 */

(function () {
  'use strict';

  const CONSENT_STORAGE_KEY = 'nv_cookie_consent_v5';
  const CONSENT_LEGACY_KEY = 'nv_cookie_consent_v4';
  const IDENTITY_STORAGE_KEY = 'nv_client_identity_id';
  const POLICY_VERSION = '2026.2.DPDP_GDPR';

  // 1. Helper: Generate or retrieve persistent 1P client pseudonymous identity
  function getOrCreateIdentityId() {
    let id = localStorage.getItem(IDENTITY_STORAGE_KEY);
    if (!id) {
      id = 'nv_id_' + 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
      try {
        localStorage.setItem(IDENTITY_STORAGE_KEY, id);
      } catch (e) {}
    }
    return id;
  }

  // 2. Helper: Sync consent record asynchronously to Numeros Vision backend ledger
  function syncConsentToBackend(choices) {
    const identityId = getOrCreateIdentityId();
    const payload = {
      pseudonymous_id: identityId,
      choices: {
        essential: true,
        analytics: Boolean(choices.analytics),
        marketing: Boolean(choices.marketing)
      },
      banner_version: POLICY_VERSION,
      timestamp: Math.floor(Date.now() / 1000)
    };

    try {
      if (window.fetch) {
        fetch('/api/v1/privacy/consent', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        }).catch(function (err) {
          console.debug('[Consent Manager] Backend ledger sync notice:', err.message);
        });
      }
    } catch (e) {}
  }

  // 3. Inject CSS styles for the Consent Banner, Modal & Switches
  function ensureConsentStyles() {
    if (document.getElementById('nv-consent-styles')) return;

    const style = document.createElement('style');
    style.id = 'nv-consent-styles';
    style.textContent = `
      .nv-consent-banner {
        position: fixed;
        bottom: 24px;
        left: 24px;
        max-width: 520px;
        width: calc(100% - 48px);
        background: #FFFDF7;
        border: 1.5px solid rgba(201, 162, 39, 0.5);
        border-radius: 18px;
        padding: 22px 24px;
        box-shadow: 0 16px 48px rgba(180, 155, 110, 0.28), 0 4px 16px rgba(30, 24, 16, 0.08);
        z-index: 99999;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
        color: #523E28;
        display: none;
        opacity: 0;
        transform: translateY(16px);
        transition: opacity 0.35s ease, transform 0.35s ease;
      }
      .nv-consent-banner.visible {
        display: block !important;
        opacity: 1 !important;
        transform: translateY(0) !important;
      }
      .nv-consent-inner {
        display: flex;
        align-items: flex-start;
        gap: 14px;
      }
      .nv-consent-icon {
        font-size: 1.7rem;
        line-height: 1;
        flex-shrink: 0;
      }
      .nv-consent-content {
        flex: 1;
      }
      .nv-consent-title {
        margin: 0 0 6px 0;
        font-family: 'Cinzel', 'Cormorant Garamond', Georgia, serif;
        font-size: 1.15rem;
        font-weight: 700;
        color: #8B6914;
        letter-spacing: 0.03em;
      }
      .nv-consent-text {
        margin: 0 0 14px 0;
        font-size: 0.83rem;
        color: #523E28;
        line-height: 1.6;
      }
      .nv-consent-text a {
        color: #8B6914;
        font-weight: 600;
        text-decoration: underline;
        text-underline-offset: 2px;
      }
      .nv-consent-text a:hover {
        color: #C9A227;
      }
      .nv-consent-actions {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        align-items: center;
      }
      .nv-consent-btn-all {
        background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
        color: #FFFFFF !important;
        border: none;
        border-radius: 20px;
        padding: 8px 18px;
        font-size: 0.81rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(201, 162, 39, 0.28);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
      }
      .nv-consent-btn-all:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(201, 162, 39, 0.38);
      }
      .nv-consent-btn-essential {
        background: #FAF6EE;
        color: #523E28;
        border: 1px solid rgba(201, 162, 39, 0.45);
        border-radius: 20px;
        padding: 8px 14px;
        font-size: 0.81rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.15s ease;
      }
      .nv-consent-btn-essential:hover {
        background: #F2ECE0;
      }
      .nv-consent-link-pref {
        font-size: 0.78rem;
        color: #8B6914;
        font-weight: 600;
        text-decoration: underline;
        cursor: pointer;
        background: transparent;
        border: none;
        padding: 4px 6px;
      }
      .nv-consent-link-pref:hover {
        color: #C9A227;
      }
      .nv-consent-close {
        position: absolute;
        top: 12px;
        right: 14px;
        background: transparent;
        border: none;
        color: #7A654D;
        font-size: 1.3rem;
        line-height: 1;
        cursor: pointer;
        padding: 4px;
      }
      .nv-consent-close:hover {
        color: #8B6914;
      }

      /* Preferences Modal Styles */
      .nv-consent-modal-overlay {
        position: fixed;
        inset: 0;
        background: rgba(42, 32, 20, 0.65);
        backdrop-filter: blur(4px);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 100000;
        padding: 16px;
      }
      .nv-consent-modal-overlay.visible {
        display: flex !important;
      }
      .nv-consent-modal-card {
        background: #FFFDF7;
        border: 2px solid #C9A227;
        border-radius: 18px;
        max-width: 540px;
        width: 100%;
        padding: 26px 28px;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.25);
        color: #523E28;
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
      }
      .nv-consent-modal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 16px;
        border-bottom: 1px solid rgba(201, 162, 39, 0.25);
        padding-bottom: 12px;
      }
      .nv-consent-modal-title {
        font-family: 'Cinzel', Georgia, serif;
        font-size: 1.25rem;
        font-weight: 700;
        color: #8B6914;
        margin: 0;
      }
      .nv-consent-pref-group {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: 14px;
        padding: 14px 0;
        border-bottom: 1px solid rgba(201, 162, 39, 0.15);
      }
      .nv-consent-pref-info {
        flex: 1;
      }
      .nv-consent-pref-name {
        font-size: 0.92rem;
        font-weight: 700;
        color: #523E28;
        margin-bottom: 3px;
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .nv-consent-pref-desc {
        font-size: 0.78rem;
        color: #7A654D;
        line-height: 1.45;
      }

      /* Custom Accessible Switch */
      .nv-switch {
        position: relative;
        display: inline-block;
        width: 44px;
        height: 24px;
        flex-shrink: 0;
      }
      .nv-switch input {
        opacity: 0;
        width: 0;
        height: 0;
      }
      .nv-slider {
        position: absolute;
        cursor: pointer;
        inset: 0;
        background-color: #E2DACB;
        transition: 0.25s;
        border-radius: 24px;
      }
      .nv-slider:before {
        position: absolute;
        content: "";
        height: 18px;
        width: 18px;
        left: 3px;
        bottom: 3px;
        background-color: #FFFDF7;
        transition: 0.25s;
        border-radius: 50%;
        box-shadow: 0 1px 4px rgba(0,0,0,0.2);
      }
      .nv-switch input:checked + .nv-slider {
        background-color: #16835B;
      }
      .nv-switch input:checked + .nv-slider:before {
        transform: translateX(20px);
      }
      .nv-switch input:disabled + .nv-slider {
        background-color: #C9A227;
        opacity: 0.75;
        cursor: not-allowed;
      }

      @media (max-width: 600px) {
        .nv-consent-banner {
          left: 12px;
          bottom: 12px;
          width: calc(100% - 24px);
          padding: 16px 18px;
        }
        .nv-consent-modal-card {
          padding: 20px 18px;
        }
      }
    `;
    document.head.appendChild(style);
  }

  // 4. Create or Ensure the DOM elements for Banner & Preferences Modal
  function ensureConsentElements() {
    let banner = document.getElementById('nv-cookie-banner');
    if (!banner) {
      banner = document.createElement('aside');
      banner.id = 'nv-cookie-banner';
      banner.className = 'nv-consent-banner';
      banner.setAttribute('role', 'dialog');
      banner.setAttribute('aria-live', 'polite');
      banner.setAttribute('aria-label', 'Cookie and Privacy Consent Preferences');
      banner.innerHTML = `
        <button class="nv-consent-close" onclick="window.nvConsent.acceptChoice('essential')" aria-label="Close cookie notice" title="Dismiss cookie notice">&times;</button>
        <div class="nv-consent-inner">
          <div class="nv-consent-icon" aria-hidden="true">🛡️</div>
          <div class="nv-consent-content">
            <h4 class="nv-consent-title">Cookie &amp; Privacy Choices</h4>
            <p class="nv-consent-text">
              We process essential mathematical session coordinates and anonymous telemetry under the <strong>DPDP Act 2023 (India)</strong> and <strong>GDPR (EU/UK)</strong>. We strictly enforce zero third-party data broker sharing and zero cross-site advertising pixels.
              <a href="/cookie-policy/">Read Cookie Policy</a> • <a href="/privacy-policy/">Privacy Policy</a>.
            </p>
            <div class="nv-consent-actions">
              <button class="nv-consent-btn-all" onclick="window.nvConsent.acceptChoice('all')">Accept All ✦</button>
              <button class="nv-consent-btn-essential" onclick="window.nvConsent.acceptChoice('essential')">Essential Only</button>
              <button type="button" class="nv-consent-link-pref" onclick="window.nvConsent.openPreferences(event)">Customize Choices</button>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(banner);
    }

    let modal = document.getElementById('nv-consent-modal');
    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'nv-consent-modal';
      modal.className = 'nv-consent-modal-overlay';
      modal.setAttribute('role', 'dialog');
      modal.setAttribute('aria-modal', 'true');
      modal.setAttribute('aria-label', 'Privacy and Cookie Preferences');
      modal.innerHTML = `
        <div class="nv-consent-modal-card">
          <div class="nv-consent-modal-header">
            <h3 class="nv-consent-modal-title">Privacy &amp; Cookie Preferences</h3>
            <button type="button" onclick="window.nvConsent.closePreferences()" style="background:none; border:none; font-size:1.4rem; color:#7A654D; cursor:pointer;" aria-label="Close preferences">&times;</button>
          </div>
          <p style="font-size:0.80rem; color:#7A654D; line-height:1.5; margin:0 0 16px 0;">
            Manage how Numeros Vision uses cookies and telemetry. You can update or withdraw your choices at any time.
          </p>

          <!-- Group 1: Strictly Necessary -->
          <div class="nv-consent-pref-group">
            <div class="nv-consent-pref-info">
              <div class="nv-consent-pref-name">
                <span>🔒 Strictly Necessary</span>
                <span style="font-size:0.68rem; background:rgba(201,162,39,0.18); color:#8B6914; padding:2px 6px; border-radius:4px;">Always Active</span>
              </div>
              <div class="nv-consent-pref-desc">
                Essential for cryptographic session validation, report job rendering, secure checkout, and mathematical calculations. Cannot be disabled.
              </div>
            </div>
            <label class="nv-switch">
              <input type="checkbox" checked disabled />
              <span class="nv-slider"></span>
            </label>
          </div>

          <!-- Group 2: Analytics & Telemetry -->
          <div class="nv-consent-pref-group">
            <div class="nv-consent-pref-info">
              <div class="nv-consent-pref-name">
                <span>📊 Analytics &amp; Performance</span>
              </div>
              <div class="nv-consent-pref-desc">
                Helps us anonymously understand aggregate website traffic, page speed, and diagnostic reliability via Google Analytics.
              </div>
            </div>
            <label class="nv-switch">
              <input type="checkbox" id="nv-pref-analytics" />
              <span class="nv-slider"></span>
            </label>
          </div>

          <!-- Group 3: Marketing & Campaigns -->
          <div class="nv-consent-pref-group">
            <div class="nv-consent-pref-info">
              <div class="nv-consent-pref-name">
                <span>🎯 Marketing &amp; Conversions</span>
              </div>
              <div class="nv-consent-pref-desc">
                Evaluates advertising campaign performance. Personal chart computations and Date of Birth details are never shared with advertising networks.
              </div>
            </div>
            <label class="nv-switch">
              <input type="checkbox" id="nv-pref-marketing" />
              <span class="nv-slider"></span>
            </label>
          </div>

          <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px; margin-top:22px; padding-top:14px; border-top:1px solid rgba(201,162,39,0.2);">
            <button type="button" onclick="window.nvConsent.withdraw()" style="background:none; border:none; color:#A13030; font-size:0.78rem; text-decoration:underline; cursor:pointer;">
              Withdraw / Reject All Non-Essential
            </button>
            <div style="display:flex; gap:10px;">
              <button type="button" onclick="window.nvConsent.savePreferences()" class="nv-consent-btn-all" style="padding:8px 20px;">
                Save Choices ✦
              </button>
            </div>
          </div>
        </div>
      `;
      document.body.appendChild(modal);
    }
  }

  // 5. Dynamic Footer Cookie Preferences Link Injection
  function ensureFooterLink() {
    const footers = document.querySelectorAll('footer, .nv-footer');
    footers.forEach(footer => {
      if (footer.querySelector('.nv-cookie-pref-btn')) return;
      const linkWrap = footer.querySelector('nav, .nv-footer-links, .footer-links, div');
      if (linkWrap) {
        const btn = document.createElement('button');
        btn.type = 'button';
        btn.className = 'nv-cookie-pref-btn';
        btn.textContent = 'Cookie Preferences';
        btn.style.cssText = 'background:none; border:none; color:#8B6914; font-size:0.75rem; text-decoration:underline; cursor:pointer; padding:2px 6px; font-family:inherit;';
        btn.onclick = function (e) {
          window.nvConsent.reopen(e);
        };
        linkWrap.appendChild(btn);
      }
    });
  }

  // 5b. One-Time Legacy Storage Migration & Cache Scrub (PWA Hygiene)
  function runOneTimeLegacyStorageMigration() {
    var MIGRATION_FLAG = 'nv_storage_migrated_v5';
    try {
      if (localStorage.getItem(MIGRATION_FLAG)) return;
      var legacyPiiKeys = [
        'nv_user_dob', 'nv_user_name', 'nv_user_email', 'nv_user_phone',
        'nv_user_time', 'nv_user_city', 'nv_user_gender', 'nv_user_profile',
        'nv_cached_calc', 'nv_last_calculation', 'nv_calculation_id',
        'nv_active_profile', 'nv_user_profiles', 'nv_family_profiles',
        'nv_user_invoices', 'nv_consultation_enquiries', 'nv_contact_tickets',
        'nv_pending_subject', 'nv_cdp_events', 'nv_customer_segment',
        'nv_user_session', 'nv_user_tier', 'nv_paid_verified'
      ];
      legacyPiiKeys.forEach(function (k) {
        try { localStorage.removeItem(k); } catch (e) {}
        try { sessionStorage.removeItem(k); } catch (e) {}
      });

      // Clear legacy Service Worker caches (old API or report caches)
      if ('caches' in window) {
        caches.keys().then(function (keys) {
          keys.forEach(function (key) {
            if (key.indexOf('api') !== -1 || key.indexOf('charm') !== -1 || key.indexOf('report') !== -1 || key.indexOf('v5.5.0') !== -1) {
              caches.delete(key);
            }
          });
        }).catch(function () {});
      }
      localStorage.setItem(MIGRATION_FLAG, 'true');
    } catch (e) {}
  }

  // 6. Master Consent Controller API
  const nvConsent = {
    init: function () {
      runOneTimeLegacyStorageMigration();
      ensureConsentStyles();
      ensureConsentElements();
      ensureFooterLink();

      const saved = localStorage.getItem(CONSENT_STORAGE_KEY) || localStorage.getItem(CONSENT_LEGACY_KEY);
      if (!saved) {
        const banner = document.getElementById('nv-cookie-banner');
        if (banner) {
          setTimeout(function () {
            banner.style.display = 'block';
            banner.classList.add('visible');
          }, 350);
        }
      } else {
        try {
          const parsed = typeof saved === 'string' && saved.startsWith('{')
            ? JSON.parse(saved)
            : { essential: true, analytics: saved === 'all', marketing: saved === 'all' };
          nvConsent.dispatchChoices(parsed, false);
        } catch (e) {}
      }
    },

    acceptChoice: function (level) {
      const choices = {
        essential: true,
        analytics: level === 'all',
        marketing: level === 'all'
      };
      nvConsent.persistChoices(choices);
      nvConsent.hideBanner();
    },

    openPreferences: function (e) {
      if (e && e.preventDefault) e.preventDefault();
      ensureConsentStyles();
      ensureConsentElements();
      const status = nvConsent.getStatus();
      const anSwitch = document.getElementById('nv-pref-analytics');
      const mkSwitch = document.getElementById('nv-pref-marketing');
      if (anSwitch) anSwitch.checked = Boolean(status.analytics);
      if (mkSwitch) mkSwitch.checked = Boolean(status.marketing);

      const modal = document.getElementById('nv-consent-modal');
      if (modal) modal.classList.add('visible');
    },

    closePreferences: function () {
      const modal = document.getElementById('nv-consent-modal');
      if (modal) modal.classList.remove('visible');
    },

    savePreferences: function () {
      const anSwitch = document.getElementById('nv-pref-analytics');
      const mkSwitch = document.getElementById('nv-pref-marketing');
      const choices = {
        essential: true,
        analytics: Boolean(anSwitch && anSwitch.checked),
        marketing: Boolean(mkSwitch && mkSwitch.checked)
      };
      nvConsent.persistChoices(choices);
      nvConsent.closePreferences();
      nvConsent.hideBanner();
    },

    withdraw: function () {
      const choices = { essential: true, analytics: false, marketing: false };
      nvConsent.persistChoices(choices);
      nvConsent.closePreferences();
      nvConsent.hideBanner();
      // Remove device cookie upon withdrawal
      document.cookie = 'nv_dev_id=; path=/; max-age=0; SameSite=Lax';
    },

    persistChoices: function (choices) {
      try {
        localStorage.setItem(CONSENT_STORAGE_KEY, JSON.stringify(choices));
        localStorage.setItem(CONSENT_LEGACY_KEY, (choices.analytics && choices.marketing) ? 'all' : 'essential');
      } catch (e) {}

      syncConsentToBackend(choices);
      nvConsent.dispatchChoices(choices, true);
    },

    dispatchChoices: function (choices, userTriggered) {
      // 1. Google Consent Mode v2 synchronization
      if (typeof window.gtag === 'function') {
        window.gtag('consent', 'update', {
          'analytics_storage': choices.analytics ? 'granted' : 'denied',
          'ad_storage': choices.marketing ? 'granted' : 'denied',
          'ad_user_data': choices.marketing ? 'granted' : 'denied',
          'ad_personalization': choices.marketing ? 'granted' : 'denied'
        });
      }

      // 2. Meta Pixel synchronization
      if (typeof window.fbq === 'function') {
        window.fbq('consent', choices.marketing ? 'grant' : 'revoke');
      }

      // 3. Dispatch browser event
      window.dispatchEvent(new CustomEvent('nv_consent_resolved', {
        detail: {
          level: (choices.analytics && choices.marketing) ? 'all' : (choices.analytics ? 'analytics' : 'essential'),
          choices: choices,
          userTriggered: userTriggered
        }
      }));
    },

    hideBanner: function () {
      const banner = document.getElementById('nv-cookie-banner');
      if (banner) {
        banner.classList.remove('visible');
        setTimeout(function () {
          banner.style.display = 'none';
        }, 350);
      }
    },

    reopen: function (e) {
      if (e && e.preventDefault) e.preventDefault();
      nvConsent.openPreferences(e);
    },

    getStatus: function () {
      const raw = localStorage.getItem(CONSENT_STORAGE_KEY);
      if (raw && raw.startsWith('{')) {
        try {
          return JSON.parse(raw);
        } catch (e) {}
      }
      const legacy = localStorage.getItem(CONSENT_LEGACY_KEY);
      return {
        essential: true,
        analytics: legacy === 'all',
        marketing: legacy === 'all',
        hasConsented: Boolean(raw || legacy)
      };
    },

    // Privacy Hygiene: Cleans all stored personal telemetry and charts on device logout
    clearDevicePersonalData: function () {
      const piiKeys = [
        'nv_user_dob', 'nv_user_name', 'nv_user_email', 'nv_user_phone',
        'nv_user_time', 'nv_user_city', 'nv_user_gender', 'nv_user_profile',
        'nv_cached_calc', 'nv_last_calculation', 'nv_calculation_id',
        'nv_active_profile', 'nv_user_profiles', 'nv_family_profiles',
        'nv_user_invoices', 'nv_consultation_enquiries', 'nv_contact_tickets',
        'nv_pending_subject', 'nv_cdp_events', 'nv_customer_segment'
      ];
      piiKeys.forEach(k => {
        try { localStorage.removeItem(k); } catch (e) {}
        try { sessionStorage.removeItem(k); } catch (e) {}
      });

      // Clear Service Worker API & report caches
      if ('caches' in window) {
        caches.keys().then(keys => {
          keys.forEach(key => {
            if (key.includes('api') || key.includes('charm') || key.includes('report')) {
              caches.delete(key);
            }
          });
        }).catch(function () {});
      }
    }
  };

  // Expose globally
  window.nvConsent = nvConsent;
  window.initCookieConsent = nvConsent.init;
  window.acceptCookieConsent = nvConsent.acceptChoice;
  window.reopenCookieConsent = nvConsent.reopen;

  // Auto-init
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', nvConsent.init);
  } else {
    nvConsent.init();
  }
})();
