/**
 * ============================================================
 * NUMEROS VISION — PROGRESSIVE WEB APP (PWA) INSTALL CONTROLLER
 * Brand: Numeros Vision · Tagline: Anveil Every Charm
 * Supports: Android, iOS, iPadOS, Chrome, Safari, Edge
 * Features: Non-intrusive smart banner, iOS visual guide modal,
 *           drawer menu integration, 7-day dismissal cooldown.
 * ============================================================
 */

(function () {
  'use strict';

  // ── 1. SERVICE WORKER REGISTRATION ──────────────────────────
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker
        .register('/sw.js', { scope: '/' })
        .then((reg) => {
          console.log('[PWA] ServiceWorker registered with scope:', reg.scope);
          // Check for updates
          if (reg.waiting) {
            console.log('[PWA] New version ready and waiting');
          }
        })
        .catch((err) => {
          console.warn('[PWA] ServiceWorker registration failed:', err);
        });
    });
  }

  // ── 2. ENVIRONMENT DETECTION ────────────────────────────────
  const isStandalone = () => {
    return (
      window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone === true ||
      document.referrer.includes('android-app://') ||
      window.location.search.includes('source=pwa')
    );
  };

  const isIos = () => {
    return (
      /iPad|iPhone|iPod/.test(navigator.userAgent) ||
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1)
    );
  };

  const isIpad = () => {
    return (
      (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1) ||
      /iPad/.test(navigator.userAgent)
    );
  };

  // Strictly identify real mobile and tablet devices
  const isMobileOrTablet = () => {
    if (isStandalone()) return false;
    const ua = navigator.userAgent || navigator.vendor || window.opera || '';
    const mobileRegex = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini|Mobile|mobile|CriOS/i;
    const isTouchMac = navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1; // iPadOS Safari
    if (mobileRegex.test(ua) || isTouchMac) {
      return true;
    }
    // Also check touch pointer and handheld viewport width
    if (window.innerWidth <= 1024 && (navigator.maxTouchPoints > 0 || window.matchMedia('(pointer: coarse)').matches)) {
      return true;
    }
    return false;
  };

  const isDesktop = () => !isMobileOrTablet();

  const isDismissed = () => {
    try {
      const until = localStorage.getItem('nv_pwa_dismissed_until');
      if (until && Date.now() < parseInt(until, 10)) {
        return true;
      }
    } catch (e) {
      // localStorage disabled or restricted
    }
    return false;
  };

  const isConsentPending = () => {
    try {
      return (
        !localStorage.getItem('nv_cookie_consent_v4') &&
        !localStorage.getItem('nv_cookie_consent')
      );
    } catch (e) {
      return false;
    }
  };

  const setDismissedCooldown = (days = 7) => {
    try {
      localStorage.setItem(
        'nv_pwa_dismissed_until',
        (Date.now() + days * 24 * 60 * 60 * 1000).toString()
      );
    } catch (e) {}
  };

  // State
  let deferredPrompt = null;
  let bannerInjected = false;
  let modalInjected = false;

  // ── 3. CAPTURE CHROMIUM INSTALL PROMPT ──────────────────────
  window.addEventListener('beforeinstallprompt', (e) => {
    // Prevent Chromium's default mini-infobar on desktop & mobile
    e.preventDefault();
    deferredPrompt = e;
    window.deferredPwaPrompt = e;

    // Strictly ONLY reveal install prompts on mobile and tablet devices!
    if (isMobileOrTablet()) {
      console.log('[PWA] Captured beforeinstallprompt event on mobile/tablet');
      showDrawerItem();
      scheduleSmartBanner();
    } else {
      console.log('[PWA] Desktop device detected; suppressing PWA install banner and navbar item');
      hidePwaBanner();
      hideDrawerItem();
    }
  });

  // Handle successful installation
  window.addEventListener('appinstalled', () => {
    console.log('[PWA] Application successfully installed to device!');
    deferredPrompt = null;
    window.deferredPwaPrompt = null;
    hidePwaBanner();
    hideDrawerItem();
    try {
      localStorage.setItem('nv_pwa_installed', 'true');
    } catch (e) {}
  });

  // ── 4. STYLES INJECTION ─────────────────────────────────────
  function injectPwaStyles() {
    if (document.getElementById('nv-pwa-styles')) return;

    const style = document.createElement('style');
    style.id = 'nv-pwa-styles';
    style.textContent = `
      /* ── PWA Floating Smart Banner (Mobile & Tablet ONLY) ── */
      #nv-pwa-banner {
        position: fixed;
        left: 50%;
        bottom: calc(72px + env(safe-area-inset-bottom, 0px) + 12px);
        transform: translate(-50%, 120%);
        width: calc(100% - 32px);
        max-width: 440px;
        box-sizing: border-box;
        margin: 0;
        background: rgba(255, 253, 247, 0.96);
        backdrop-filter: blur(14px);
        -webkit-backdrop-filter: blur(14px);
        border: 1.5px solid rgba(201, 162, 39, 0.45);
        border-radius: 20px;
        box-shadow: 0 12px 36px rgba(82, 62, 40, 0.18), 0 2px 8px rgba(201, 162, 39, 0.12);
        padding: 12px 14px;
        display: flex;
        align-items: center;
        gap: 12px;
        z-index: 100001;
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.35s ease;
        opacity: 0;
        pointer-events: none;
        font-family: var(--font-body);
      }
      #nv-pwa-banner.nv-pwa-visible {
        transform: translate(-50%, 0);
        opacity: 1;
        pointer-events: auto;
      }
      /* On Desktop (> 1024px), strictly hide and suppress PWA banner, modal & drawer items */
      @media (min-width: 1025px) {
        #nv-pwa-banner,
        #nv-pwa-ios-modal,
        .nv-pwa-menu-item,
        #nvPwaDrawerItem {
          display: none !important;
          visibility: hidden !important;
          pointer-events: none !important;
          opacity: 0 !important;
          height: 0 !important;
          margin: 0 !important;
          padding: 0 !important;
        }
      }
      .nv-pwa-icon-box {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: linear-gradient(135deg, #FFFDF7 0%, #F5E8C7 100%);
        border: 1px solid rgba(201, 162, 39, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        box-shadow: 0 2px 8px rgba(201, 162, 39, 0.2);
      }
      .nv-pwa-icon-box img {
        width: 28px;
        height: 28px;
        display: block;
      }
      .nv-pwa-info {
        flex: 1;
        min-width: 0;
      }
      .nv-pwa-title {
        font-family: var(--font-display);
        font-size: 0.88rem;
        font-weight: 700;
        color: #523E28;
        letter-spacing: 0.05em;
        line-height: 1.2;
        margin-bottom: 2px;
        display: flex;
        align-items: center;
        gap: 6px;
      }
      .nv-pwa-pill {
        font-family: var(--font-body);
        font-size: 0.6rem;
        font-weight: 700;
        background: #C9A227;
        color: #FFFFFF;
        padding: 1px 5px;
        border-radius: 4px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
      }
      .nv-pwa-desc {
        font-size: 0.72rem;
        color: #7A654D;
        line-height: 1.25;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .nv-pwa-actions {
        display: flex;
        align-items: center;
        gap: 6px;
        flex-shrink: 0;
      }
      .nv-pwa-btn-install {
        background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 999px;
        padding: 8px 14px;
        font-size: 0.76rem;
        font-weight: 700;
        letter-spacing: 0.03em;
        cursor: pointer;
        box-shadow: 0 3px 10px rgba(201, 162, 39, 0.35);
        transition: transform 0.2s, box-shadow 0.2s;
        display: flex;
        align-items: center;
        gap: 4px;
        white-space: nowrap;
      }
      .nv-pwa-btn-install:active {
        transform: scale(0.96);
      }
      .nv-pwa-btn-dismiss {
        background: transparent;
        border: none;
        color: #8C7B6B;
        font-size: 1.1rem;
        line-height: 1;
        width: 28px;
        height: 28px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: background 0.2s, color 0.2s;
        padding: 0;
      }
      .nv-pwa-btn-dismiss:hover {
        background: rgba(82, 62, 40, 0.08);
        color: #523E28;
      }

      /* ── iOS Instruction Modal ── */
      #nv-pwa-ios-modal {
        position: fixed;
        inset: 0;
        background: rgba(40, 30, 20, 0.65);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        z-index: 100005;
        display: flex;
        align-items: flex-end;
        justify-content: center;
        opacity: 0;
        pointer-events: none;
        transition: opacity 0.3s ease;
        padding: 16px;
        font-family: var(--font-body);
      }
      #nv-pwa-ios-modal.nv-modal-open {
        opacity: 1;
        pointer-events: auto;
      }
      .nv-ios-card {
        background: #FFFDF7;
        border: 1.5px solid rgba(201, 162, 39, 0.45);
        border-radius: 24px;
        width: 100%;
        max-width: 460px;
        padding: 24px 20px 20px;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.3);
        transform: translateY(40px);
        transition: transform 0.35s cubic-bezier(0.16, 1, 0.3, 1);
        text-align: center;
      }
      #nv-pwa-ios-modal.nv-modal-open .nv-ios-card {
        transform: translateY(0);
      }
      @media (min-width: 768px) {
        #nv-pwa-ios-modal {
          align-items: center;
        }
      }
      .nv-ios-seal {
        width: 52px;
        height: 52px;
        margin: 0 auto 12px;
        border-radius: 14px;
        background: linear-gradient(135deg, #FFFDF7 0%, #F5E8C7 100%);
        border: 1px solid rgba(201, 162, 39, 0.4);
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 14px rgba(201, 162, 39, 0.25);
      }
      .nv-ios-seal img {
        width: 34px;
        height: 34px;
      }
      .nv-ios-title {
        font-family: var(--font-display);
        font-size: 1.15rem;
        font-weight: 700;
        color: #523E28;
        letter-spacing: 0.04em;
        margin-bottom: 6px;
      }
      .nv-ios-subtitle {
        font-size: 0.82rem;
        color: #7A654D;
        margin-bottom: 20px;
        line-height: 1.4;
      }
      .nv-ios-steps {
        display: flex;
        flex-direction: column;
        gap: 12px;
        text-align: left;
        margin-bottom: 22px;
        background: #FAF6EE;
        border: 1px solid rgba(201, 162, 39, 0.25);
        border-radius: 16px;
        padding: 14px 16px;
      }
      .nv-ios-step {
        display: flex;
        align-items: center;
        gap: 12px;
      }
      .nv-step-num {
        width: 26px;
        height: 26px;
        border-radius: 50%;
        background: #C9A227;
        color: #FFFFFF;
        font-weight: 700;
        font-size: 0.75rem;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
      }
      .nv-step-text {
        font-size: 0.8rem;
        color: #523E28;
        line-height: 1.35;
      }
      .nv-step-text strong {
        color: #8B6914;
      }
      .nv-step-icon {
        display: inline-flex;
        vertical-align: middle;
        margin: 0 2px;
      }
      .nv-ios-close-btn {
        width: 100%;
        background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
        color: #FFFFFF;
        border: none;
        border-radius: 999px;
        padding: 12px 24px;
        font-size: 0.88rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(201, 162, 39, 0.35);
        transition: transform 0.2s, box-shadow 0.2s;
      }
      .nv-ios-close-btn:active {
        transform: scale(0.98);
      }
    `;
    document.head.appendChild(style);
  }

  // ── 5. SMART BANNER DOM INJECTION ───────────────────────────
  function ensureSmartBanner() {
    if (bannerInjected || document.getElementById('nv-pwa-banner')) return;

    injectPwaStyles();

    const banner = document.createElement('div');
    banner.id = 'nv-pwa-banner';
    banner.setAttribute('role', 'region');
    banner.setAttribute('aria-label', 'Install Numeros Vision Web App');

    banner.innerHTML = `
      <div class="nv-pwa-icon-box" aria-hidden="true">
        <img src="/logos/nv-logo-mark.svg" alt="" />
      </div>
      <div class="nv-pwa-info">
        <div class="nv-pwa-title">
          <span>NUMEROS VISION</span>
          <span class="nv-pwa-pill">App</span>
        </div>
        <div class="nv-pwa-desc">Instant offline speed &amp; full screen view</div>
      </div>
      <div class="nv-pwa-actions">
        <button type="button" class="nv-pwa-btn-install" id="nvPwaInstallBtn" onclick="window.triggerPwaInstall(event)">
          <span>Install</span>
          <span>✦</span>
        </button>
        <button type="button" class="nv-pwa-btn-dismiss" id="nvPwaDismissBtn" onclick="window.dismissPwaBanner(event)" aria-label="Dismiss banner">
          &times;
        </button>
      </div>
    `;

    document.body.appendChild(banner);
    bannerInjected = true;
  }

  // ── 6. iOS MODAL DOM INJECTION ──────────────────────────────
  function ensureIosModal() {
    if (modalInjected || document.getElementById('nv-pwa-ios-modal')) return;

    injectPwaStyles();

    const isTablet = isIpad();
    const toolbarLocation = isTablet ? 'top' : 'bottom';

    const modal = document.createElement('div');
    modal.id = 'nv-pwa-ios-modal';
    modal.setAttribute('role', 'dialog');
    modal.setAttribute('aria-modal', 'true');
    modal.setAttribute('aria-label', 'Install on iOS or iPad');

    modal.innerHTML = `
      <div class="nv-ios-card">
        <div class="nv-ios-seal">
          <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision Seal" />
        </div>
        <div class="nv-ios-title">Install Numeros Vision</div>
        <p class="nv-ios-subtitle">Add to your Home Screen for instant launch and offline access</p>
        
        <div class="nv-ios-steps">
          <div class="nv-ios-step">
            <span class="nv-step-num">1</span>
            <span class="nv-step-text">
              Tap the <strong>Share</strong> button 
              <span class="nv-step-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8B6914" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12v8a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-8"/><polyline points="16 6 12 2 8 6"/><line x1="12" y1="2" x2="12" y2="15"/></svg>
              </span>
              in Safari's ${toolbarLocation} toolbar.
            </span>
          </div>
          <div class="nv-ios-step">
            <span class="nv-step-num">2</span>
            <span class="nv-step-text">
              Scroll down and tap <strong>Add to Home Screen</strong>
              <span class="nv-step-icon">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8B6914" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"/><line x1="12" y1="8" x2="12" y2="16"/><line x1="8" y1="12" x2="16" y2="12"/></svg>
              </span>.
            </span>
          </div>
          <div class="nv-ios-step">
            <span class="nv-step-num">3</span>
            <span class="nv-step-text">
              Tap <strong>Add</strong> in the top-right corner to finish.
            </span>
          </div>
        </div>

        <button type="button" class="nv-ios-close-btn" onclick="window.closeIosPwaModal(event)">
          Got It, Thanks!
        </button>
      </div>
    `;

    // Close when tapping backdrop
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        window.closeIosPwaModal();
      }
    });

    document.body.appendChild(modal);
    modalInjected = true;
  }

  // ── 7. DRAWER ITEM VISIBILITY ───────────────────────────────
  function showDrawerItem() {
    // Strictly ONLY mobile and tablet drawer! Never show on desktop!
    if (isDesktop() || isStandalone()) {
      hideDrawerItem();
      return;
    }
    const drawerItem = document.getElementById('nvPwaDrawerItem');
    if (drawerItem) {
      drawerItem.style.display = 'block';
    }
  }

  function hideDrawerItem() {
    const drawerItem = document.getElementById('nvPwaDrawerItem');
    if (drawerItem) {
      drawerItem.style.display = 'none';
    }
  }

  // ── 8. BANNER SCHEDULING & CONTROLS ─────────────────────────
  function scheduleSmartBanner() {
    // Strictly ONLY mobile and tablet! Never show on desktop!
    if (isDesktop() || isStandalone() || isDismissed()) {
      hidePwaBanner();
      return;
    }

    // If cookie consent is pending, wait until user resolves consent first
    if (isConsentPending()) {
      window.addEventListener(
        'nv_consent_resolved',
        () => {
          setTimeout(scheduleSmartBanner, 2000);
        },
        { once: true }
      );
      return;
    }

    // Graceful delay (2.5 seconds) so the user sees page content first
    setTimeout(() => {
      if (isDesktop() || isStandalone() || isDismissed() || isConsentPending()) return;
      ensureSmartBanner();
      const banner = document.getElementById('nv-pwa-banner');
      if (banner) {
        banner.classList.add('nv-pwa-visible');
      }
    }, 2500);
  }

  function hidePwaBanner() {
    const banner = document.getElementById('nv-pwa-banner');
    if (banner) {
      banner.classList.remove('nv-pwa-visible');
      setTimeout(() => {
        if (banner.parentNode) banner.parentNode.removeChild(banner);
        bannerInjected = false;
      }, 400);
    }
  }

  // ── 9. PUBLIC TRIGGER METHODS ───────────────────────────────
  window.triggerPwaInstall = async function (e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }

    // A. Already in standalone mode
    if (isStandalone()) {
      alert('Numeros Vision is already installed and running as a native app on this device.');
      return;
    }

    // B. Chromium deferred prompt available
    if (deferredPrompt) {
      hidePwaBanner();
      deferredPrompt.prompt();
      const { outcome } = await deferredPrompt.userChoice;
      console.log('[PWA] User response to install prompt:', outcome);
      if (outcome === 'accepted') {
        hideDrawerItem();
      }
      deferredPrompt = null;
      window.deferredPwaPrompt = null;
      return;
    }

    // C. iOS / iPadOS Safari workflow
    if (isIos()) {
      hidePwaBanner();
      ensureIosModal();
      const modal = document.getElementById('nv-pwa-ios-modal');
      if (modal) {
        modal.classList.add('nv-modal-open');
      }
      return;
    }

    // D. Fallback for Desktop / browsers where beforeinstallprompt already expired or isn't triggered
    ensureIosModal();
    const modal = document.getElementById('nv-pwa-ios-modal');
    if (modal) {
      const title = modal.querySelector('.nv-ios-title');
      const subtitle = modal.querySelector('.nv-ios-subtitle');
      const steps = modal.querySelector('.nv-ios-steps');
      if (title) title.textContent = 'Install Numeros Vision App';
      if (subtitle) subtitle.textContent = 'Follow your browser options to install as a standalone app';
      if (steps) {
        steps.innerHTML = `
          <div class="nv-ios-step">
            <span class="nv-step-num">1</span>
            <span class="nv-step-text">Open browser menu (⋮, ⋯, or App Icon in address bar)</span>
          </div>
          <div class="nv-ios-step">
            <span class="nv-step-num">2</span>
            <span class="nv-step-text">Click <strong>"Install Numeros Vision"</strong> or <strong>"Add to Home Screen"</strong></span>
          </div>
          <div class="nv-ios-step">
            <span class="nv-step-num">3</span>
            <span class="nv-step-text">Confirm install for native desktop/tablet experience</span>
          </div>
        `;
      }
      modal.classList.add('nv-modal-open');
    }
  };

  window.dismissPwaBanner = function (e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    setDismissedCooldown(7);
    hidePwaBanner();
  };

  window.closeIosPwaModal = function (e) {
    if (e) {
      e.preventDefault();
      e.stopPropagation();
    }
    const modal = document.getElementById('nv-pwa-ios-modal');
    if (modal) {
      modal.classList.remove('nv-modal-open');
    }
  };

  // ── 10. INITIALIZATION ──────────────────────────────────────
  function initPwa() {
    // Desktop devices must NEVER show PWA banner or install drawer items
    if (isStandalone() || isDesktop()) {
      hideDrawerItem();
      hidePwaBanner();
      return;
    }

    // Proactively enable drawer install item and schedule smart banner on mobile & tablet
    showDrawerItem();
    scheduleSmartBanner();
  }

  // Handle dynamic screen resizing / orientation changes
  window.addEventListener('resize', () => {
    if (isDesktop()) {
      hidePwaBanner();
      hideDrawerItem();
    }
  });

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPwa);
  } else {
    initPwa();
  }
})();
