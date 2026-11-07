/**
 * ==============================================================================
 * NUMEROS VISION — MASTER TRACKING, PIXELS & ANALYTICS SUITE
 * ==============================================================================
 * Supports:
 * - Google Analytics 4 (GA4) with Google Consent Mode v2
 * - Google Ads (AdWords) Conversion Tracking & Remarketing
 * - Meta Pixel (Facebook & Instagram) with Data Processing Options & Consent
 * - Firebase Analytics (Web SDK v10 compat)
 * - Microsoft Clarity (Heatmaps & Session Recordings)
 * - Google Tag Manager (GTM)
 * - CDP Identity Graph & First-Party UTM Attribution
 * 
 * DPDP Act 2023 & GDPR Compliant: Defaults to Consent-Denied until statutory
 * marketing consent is confirmed.
 */

(function () {
  'use strict';

  // Telemetry Allowlist (Strict Allowlist — DPDP Act 2023 & GDPR Privacy Compliance)
  // Only explicitly designated telemetry and attribution dimensions are permitted.
  const ALLOWED_TELEMETRY_KEYS = new Set([
    'event', 'page_path', 'page_title', 'timestamp',
    'calculator_name', 'topic', 'plan_id', 'lead_type', 'method', 'cta_location', 'ref',
    'value', 'currency', 'transaction_id', 'content_name', 'items', 'item_name', 'price', 'quantity',
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'gclid', 'fbclid', 'wbraid', 'gbraid', 'ttclid', 'msclkid',
    'device_id', 'device_type', 'is_pwa', 'app_platform'
  ]);

  function sanitizeTelemetryPayload(obj) {
    if (!obj || typeof obj !== 'object') return obj;
    if (Array.isArray(obj)) {
      return obj
        .map(sanitizeTelemetryPayload)
        .filter(function (item) { return item !== null && item !== undefined; });
    }
    const clean = {};
    for (const [key, val] of Object.entries(obj)) {
      const lowerKey = key.toLowerCase();
      // Strict ALLOWLIST: Any key not explicitly in ALLOWED_TELEMETRY_KEYS is dropped immediately
      if (!ALLOWED_TELEMETRY_KEYS.has(lowerKey)) continue;

      // Secondary value-level privacy verification: drop any string value matching email, phone, or date pattern
      if (typeof val === 'string') {
        const trimmed = val.trim();
        if (/@[\w.-]+\.\w+/.test(trimmed)) continue;
        if (/^\+?[0-9\s-]{10,15}$/.test(trimmed)) continue;
        // Strict Calendar / Birth Date Rejection (YYYY-MM-DD, YYYY/MM/DD, DD-MM-YYYY, DD/MM/YYYY, DDMMYYYY, YYYYMMDD)
        if (/^\d{4}[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])$/.test(trimmed)) continue;
        if (/^(0[1-9]|[12]\d|3[01])[-/](0[1-9]|1[0-2])[-/]\d{4}$/.test(trimmed)) continue;
        if (/^(0[1-9]|[12]\d|3[01])(0[1-9]|1[0-2])\d{4}$/.test(trimmed)) continue;
        if (/^\d{4}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$/.test(trimmed)) continue;
      }
      if (typeof val === 'object' && val !== null) {
        clean[key] = sanitizeTelemetryPayload(val);
      } else {
        clean[key] = val;
      }
    }
    return clean;
  }

  // 1. DataLayer & Global Stubs
  window.dataLayer = window.dataLayer || [];
  // Google Tag Manager (v5) Mobile Native Bridges (Android & iOS)
  // Forwards web dataLayer events into native Firebase Analytics & GTM v5 runtimes
  const originalDataLayerPush = window.dataLayer.push.bind(window.dataLayer);
  window.dataLayer.push = function() {
    const sanitizedArgs = [];
    for (let i = 0; i < arguments.length; i++) {
      const item = arguments[i];
      if (item && typeof item === 'object') {
        const cleanItem = sanitizeTelemetryPayload(item);
        const eventName = cleanItem.event || cleanItem[0] || 'dataLayer_push';
        // 1. Android GTM v5 Bridge
        if (window.AndroidBridge && typeof window.AndroidBridge.logEvent === 'function') {
          try {
            window.AndroidBridge.logEvent(String(eventName), JSON.stringify(cleanItem));
          } catch (e) {
            console.debug('[AndroidBridge] GTM event forward error:', e);
          }
        }
        sanitizedArgs.push(cleanItem);
      } else {
        sanitizedArgs.push(item);
      }
    }
    return originalDataLayerPush.apply(window.dataLayer, sanitizedArgs);
  };
  window.gtag = window.gtag || function () {
    const cleanArgs = [];
    for (let i = 0; i < arguments.length; i++) {
      const a = arguments[i];
      if (typeof a === 'object' && a !== null) {
        const item = sanitizeTelemetryPayload(a);
        if (typeof item === 'object' && item !== null) {
          delete item.user_id;
          delete item.golden_profile_id;
        }
        cleanArgs.push(item);
      } else {
        cleanArgs.push(a);
      }
    }
    window.dataLayer.push(cleanArgs);
  };

  // Google Consent Mode v2 Defaults:
  // Operational analytics enabled for first-party anonymous site traffic measurement
  // Advertising pixels (ad_storage, ad_user_data, ad_personalization) remain denied until explicit marketing consent
  window.gtag('consent', 'default', {
    'ad_storage': 'denied',
    'ad_user_data': 'denied',
    'ad_personalization': 'denied',
    'analytics_storage': 'denied',
    'wait_for_update': 500
  });
  window.gtag('js', new Date());

  // Meta Pixel Stub with Automatic Telemetry Sanitizer (Guaranteed 100% User/Chart Free)
  if (!window.fbq) {
    const fbq = function () {
      const cleanArgs = [];
      for (let i = 0; i < arguments.length; i++) {
        const a = arguments[i];
        if (typeof a === 'object' && a !== null) {
          const item = sanitizeTelemetryPayload(a);
          if (typeof item === 'object' && item !== null) {
            delete item.user_id;
            delete item.golden_profile_id;
          }
          cleanArgs.push(item);
        } else {
          cleanArgs.push(a);
        }
      }
      fbq.callMethod ? fbq.callMethod.apply(fbq, cleanArgs) : fbq.queue.push(cleanArgs);
    };
    if (!window._fbq) window._fbq = fbq;
    fbq.push = fbq;
    fbq.loaded = true;
    fbq.version = '2.0';
    fbq.queue = [];
    window.fbq = fbq;
  }
  // Meta Pixel default consent state: revoke until marketing consent
  window.fbq('consent', 'revoke');

  // 2. UTM Extraction & Attribution Helpers
  const UTM_PARAMS = [
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'gclid', 'fbclid', 'wbraid', 'gbraid', 'ttclid', 'msclkid'
  ];

  function getOrCreateDeviceId() {
    let deviceId = localStorage.getItem('nv_device_id');
    if (!deviceId) {
      deviceId = 'nv_dev_' + 'xxxxxxxxxxxx4xxxyxxxxxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
      });
      try {
        localStorage.setItem('nv_device_id', deviceId);
        // Cookie set by server Set-Cookie header only after analytics consent
      } catch (e) {}
    }
    return deviceId;
  }

  function detectDeviceType() {
    const ua = navigator.userAgent || '';
    const width = window.innerWidth || screen.width;
    if (/(ipad|tablet|(android(?!.*mobile))|(windows(?!.*phone)(.*touch))|kindle|playbook|silk)/i.test(ua) || (width >= 768 && width <= 1024)) return 'tablet';
    if (/(android.*mobile|iphone|ipod|blackberry|iemobile|opera mini)/i.test(ua) || width < 768) return 'mobile';
    return 'desktop';
  }

  function getStoredAttribution() {
    const params = {
      utm_source: 'direct',
      utm_medium: 'none',
      utm_campaign: 'organic_web'
    };
    try {
      const urlParams = new URLSearchParams(window.location.search);
      UTM_PARAMS.forEach(k => {
        const val = urlParams.get(k);
        if (val) params[k] = val.trim();
      });

      if (params.utm_source !== 'direct' || params.gclid || params.fbclid) {
        sessionStorage.setItem('nv_last_touch_utm', JSON.stringify(params));
        if (!localStorage.getItem('nv_first_touch_utm')) {
          localStorage.setItem('nv_first_touch_utm', JSON.stringify(params));
        }
      } else {
        const sess = sessionStorage.getItem('nv_last_touch_utm');
        if (sess) Object.assign(params, JSON.parse(sess));
      }
    } catch (e) {}

    params.device_id = getOrCreateDeviceId();
    params.device_type = detectDeviceType();
    
    // Automatic PWA Installed App Detection
    const isStandalone = (window.matchMedia && window.matchMedia('(display-mode: standalone)').matches) || window.navigator.standalone === true;
    params.is_pwa = isStandalone;
    params.app_platform = isStandalone ? 'pwa_app' : 'web_browser';
    if (isStandalone && (params.utm_source === 'direct' || !params.utm_source)) {
      params.utm_source = 'pwa_app';
      params.utm_medium = 'app_standalone';
      params.utm_campaign = 'installed_pwa_session';
    }
    return params;
  }

  // 3. Dynamic Script Loader Helper
  function loadScript(src, id, async) {
    if (id && document.getElementById(id)) return;
    const s = document.createElement('script');
    if (id) s.id = id;
    s.src = src;
    s.async = async !== false;
    document.head.appendChild(s);
  }

  // 4. Configuration Resolution & Tracker Initializer
  let _trackingConfig = Object.assign({
    ga4_measurement_id: 'G-3Z2E6416W7'
  }, window.NV_TRACKING_CONFIG || {});
  if (!_trackingConfig.ga4_measurement_id || _trackingConfig.ga4_measurement_id.trim() === '') {
    _trackingConfig.ga4_measurement_id = 'G-3Z2E6416W7';
  }
  let _isInitialized = false;

  async function resolveConfigAndInit() {
    const consent = checkAndApplyConsent();
    if (!consent.hasAnalytics && !consent.hasMarketing) {
      return; // Gate third-party trackers behind explicit user consent
    }
    if (_isInitialized) return;

    // Static Tracking Configuration Resolution
    _trackingConfig = Object.assign({ ga4_measurement_id: 'G-3Z2E6416W7' }, window.NV_TRACKING_CONFIG || {});

    _trackingConfig = _trackingConfig || {};
    const cfg = _trackingConfig;

    // A. Initialize Google Tag (GA4 and/or Google Ads)
    const gTagId = cfg.ga4_measurement_id || cfg.google_ads_id || null;
    if (gTagId) {
      loadScript(`https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(gTagId)}`, 'nv-gtag-script');
      if (cfg.ga4_measurement_id) {
        window.gtag('config', cfg.ga4_measurement_id, {
          send_page_view: true,
          cookie_flags: 'SameSite=Lax;Secure'
        });
      }
      if (cfg.google_ads_id && cfg.google_ads_id !== cfg.ga4_measurement_id) {
        window.gtag('config', cfg.google_ads_id);
      }
    }

    // B. Initialize Meta Pixel
    if (cfg.meta_pixel_id) {
      loadScript('https://connect.facebook.net/en_US/fbevents.js', 'nv-meta-pixel-script');
      window.fbq('init', cfg.meta_pixel_id);
      window.fbq('track', 'PageView');
    }

    // Clarity Removed per CDP & Privacy Directive

    // D. Initialize Google Tag Manager (Optional)
    if (cfg.gtm_container_id) {
      (function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
      new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
      j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
      'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
      })(window,document,'script','dataLayer',cfg.gtm_container_id);
    }

    // Firebase Web Analytics Removed per CDP & Privacy Directive

    _isInitialized = true;
    checkAndApplyConsent();
  }

  // 5. Consent Synchronization Engine (DPDP Act 2023 / GDPR)
  function checkAndApplyConsent() {
    let hasAnalytics = false;
    let hasMarketing = false;

    try {
      const v5 = localStorage.getItem('nv_cookie_consent_v5');
      if (v5 && v5.startsWith('{')) {
        const parsed = JSON.parse(v5);
        hasAnalytics = Boolean(parsed.analytics);
        hasMarketing = Boolean(parsed.marketing);
      } else {
        const v4 = localStorage.getItem('nv_cookie_consent_v4') || localStorage.getItem('nv_cookie_consent');
        hasAnalytics = v4 === 'all';
        hasMarketing = v4 === 'all';
      }
      const userProfile = localStorage.getItem('nv_user_profile');
      if (userProfile) {
        const u = JSON.parse(userProfile);
        if (u.consent_marketing === true) hasMarketing = true;
      }
    } catch (e) {}

    // 1. Update Google Consent Mode v2
    if (typeof window.gtag === 'function') {
      window.gtag('consent', 'update', {
        'analytics_storage': hasAnalytics ? 'granted' : 'denied',
        'ad_storage': hasMarketing ? 'granted' : 'denied',
        'ad_user_data': hasMarketing ? 'granted' : 'denied',
        'ad_personalization': hasMarketing ? 'granted' : 'denied'
      });
    }

    // 2. Grant or Revoke Meta Pixel Consent
    if (typeof window.fbq === 'function') {
      window.fbq('consent', hasMarketing ? 'grant' : 'revoke');
    }

    return { hasAnalytics, hasMarketing };
  }

  // Listen to cookie consent banner resolution
  window.addEventListener('nv_consent_resolved', function (e) {
    const c = checkAndApplyConsent();
    if (c.hasAnalytics) {
      resolveConfigAndInit();
      nvTrack.pageView();
    }
  });

  // 6. Master Event Dispatcher API
  const nvTrack = {
    // A. Page View
    pageView: function (pagePath, pageTitle) {
      const attr = getStoredAttribution();
      let rawPath = pagePath || (window.location.pathname + (window.location.search || ''));
      let cleanPath = rawPath;
      try {
        if (cleanPath.includes('?')) {
          const [pathPart, queryPart] = cleanPath.split('?');
          const pairs = queryPart.split('&').filter(function (p) {
            const k = (p.split('=')[0] || '').trim().toLowerCase();
            return ALLOWED_TELEMETRY_KEYS.has(k);
          });
          cleanPath = pathPart + (pairs.length ? '?' + pairs.join('&') : '');
        }
      } catch (e) {}

      const payload = sanitizeTelemetryPayload({
        page_path: cleanPath,
        page_title: pageTitle || document.title,
        ...attr
      });

      if (typeof window.gtag === 'function') {
        window.gtag('event', 'page_view', payload);
      }
      if (typeof window.fbq === 'function') {
        window.fbq('track', 'PageView', payload);
      }

    },

    // B. Calculator Interaction / Diagnostic
    calculatorUsed: function (toolName, details) {
      const attr = getStoredAttribution();
      const payload = sanitizeTelemetryPayload({
        calculator_name: toolName || 'lo_shu_grid',
        timestamp: new Date().toISOString(),
        ...attr,
        ...(details || {})
      });

      if (typeof window.gtag === 'function') {
        window.gtag('event', 'calculator_used', payload);
      }
      if (typeof window.fbq === 'function') {
        window.fbq('trackCustom', 'CalculatorUsed', payload);
      }

    },

    // C. Free Seeker Signup / Lead Generation
    freeSignup: function (userData) {
      const attr = getStoredAttribution();
      const payload = sanitizeTelemetryPayload({
        method: userData?.source || 'free_calculator_gate',
        value: 0.0,
        currency: 'INR',
        ...attr
      });

      // 1. Google Analytics 4
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'sign_up', payload);
      }

      // 2. Google Ads Conversion (if label configured)
      if (typeof window.gtag === 'function' && _trackingConfig && _trackingConfig.google_ads_id && _trackingConfig.google_ads_conversion_label_signup) {
        window.gtag('event', 'conversion', {
          'send_to': `${_trackingConfig.google_ads_id}/${_trackingConfig.google_ads_conversion_label_signup}`,
          'value': 1.0,
          'currency': 'INR'
        });
      }

      // 3. Meta Pixel (Lead & CompleteRegistration)
      if (typeof window.fbq === 'function') {
        window.fbq('track', 'Lead', payload);
        window.fbq('track', 'CompleteRegistration', payload);
      }





      if (_trackingConfig && _trackingConfig.debug_mode) {
        console.info('[NV Tracking] Free Signup / Lead Tracked Across All Pixels:', payload);
      }
    },

    // D. Initiate Checkout
    initiateCheckout: function (planName, amount, details) {
      const attr = getStoredAttribution();
      const payload = sanitizeTelemetryPayload({
        content_name: planName || 'Numeros Vision Report',
        value: parseFloat(amount) || 0.0,
        currency: 'INR',
        ...attr,
        ...(details || {})
      });

      if (typeof window.gtag === 'function') {
        window.gtag('event', 'begin_checkout', {
          items: [{ item_name: planName, price: payload.value }],
          value: payload.value,
          currency: 'INR'
        });
      }

      if (typeof window.fbq === 'function') {
        window.fbq('track', 'InitiateCheckout', payload);
      }


    },

    // E. Paid Purchase / Report Order Completion
    paidPurchase: function (orderId, planName, amount, currency, details) {
      const attr = getStoredAttribution();
      const val = parseFloat(amount) || 0.0;
      const curr = currency || 'INR';

      const payload = sanitizeTelemetryPayload({
        transaction_id: orderId || 'order_' + Date.now(),
        content_name: planName || 'Numerology Report',
        value: val,
        currency: curr,
        ...attr,
        ...(details || {})
      });

      // 1. Google Analytics 4
      if (typeof window.gtag === 'function') {
        window.gtag('event', 'purchase', {
          transaction_id: payload.transaction_id,
          value: val,
          currency: curr,
          items: [{ item_name: planName, price: val, quantity: 1 }]
        });
      }

      // 2. Google Ads Conversion (if label configured)
      if (typeof window.gtag === 'function' && _trackingConfig && _trackingConfig.google_ads_id && _trackingConfig.google_ads_conversion_label_purchase) {
        window.gtag('event', 'conversion', {
          'send_to': `${_trackingConfig.google_ads_id}/${_trackingConfig.google_ads_conversion_label_purchase}`,
          'value': val,
          'currency': curr,
          'transaction_id': payload.transaction_id
        });
      }

      // 3. Meta Pixel (Purchase event with conversion value)
      if (typeof window.fbq === 'function') {
        window.fbq('track', 'Purchase', {
          value: val,
          currency: curr,
          content_name: planName,
          content_type: 'product'
        });
      }





      if (_trackingConfig && _trackingConfig.debug_mode) {
        console.info('[NV Tracking] Paid Purchase Tracked Across All Pixels:', payload);
      }
    },

    // F. Charm AI Consultation
    charmAiQuery: function (topic) {
      const attr = getStoredAttribution();
      const payload = { topic: topic || 'general', ...attr };

      if (typeof window.gtag === 'function') {
        window.gtag('event', 'charm_ai_query', payload);
      }

    },

    // G. WhatsApp / Contact Click
    whatsAppClick: function (ctaLocation) {
      const attr = getStoredAttribution();
      const payload = { method: 'whatsapp', cta_location: ctaLocation || 'floating_button', ...attr };

      if (typeof window.gtag === 'function') {
        window.gtag('event', 'contact', payload);
      }
      if (typeof window.fbq === 'function') {
        window.fbq('track', 'Contact', payload);
      }
    }
  };

  // Expose universal tracking APIs
  window.nvTrack = nvTrack;

  // Backward compatibility with previous function signatures
  window.trackMarketingEvent = function (eventName, eventData) {
    if (eventName === 'PageView') nvTrack.pageView();
    else if (eventName === 'Lead') nvTrack.freeSignup(eventData);
    else if (eventName === 'InitiateCheckout') nvTrack.initiateCheckout(eventData?.content_name, eventData?.value, eventData);
    else if (eventName === 'Purchase') nvTrack.paidPurchase(eventData?.transaction_id, eventData?.content_name, eventData?.value, eventData?.currency, eventData);
    else if (eventName === 'Contact') nvTrack.whatsAppClick(eventData?.cta_location);
    else {
      if (typeof window.gtag === 'function') window.gtag('event', eventName, eventData);
      if (typeof window.fbq === 'function') window.fbq('trackCustom', eventName, eventData);
    }
  };

  window.trackLead = function (type, details) { nvTrack.freeSignup({ lead_type: type, ...details }); };
  window.trackInitiateCheckout = function (name, amt) { nvTrack.initiateCheckout(name, amt); };
  window.trackPurchase = function (orderId, name, amt) { nvTrack.paidPurchase(orderId, name, amt); };
  window.trackWhatsAppClick = function (loc) { nvTrack.whatsAppClick(loc); };

  // 7. Auto-Enhance WhatsApp Links with UTM Referral Context
  function enhanceWhatsAppLinks() {
    const attr = getStoredAttribution();
    const refTag = ` (Ref: ${attr.utm_source || 'direct'}/${attr.utm_campaign || 'web'})`;

    document.querySelectorAll('a[href*="wa.me"], a[href*="whatsapp.com"]').forEach(link => {
      link.addEventListener('click', function () {
        nvTrack.whatsAppClick(this.getAttribute('data-cta') || 'body_link');
      });

      try {
        const href = link.getAttribute('href');
        if (href && href.includes('text=') && !href.includes('Ref:')) {
          link.setAttribute('href', href + encodeURIComponent(refTag));
        }
      } catch (e) {}
    });
  }

  // 8. Auto-Inject UTM Hidden Fields in Forms
  function autoInjectFormUTMs() {
    document.querySelectorAll('form').forEach(form => {
      form.addEventListener('submit', function () {
        const attr = getStoredAttribution();
        Object.keys(attr).forEach(k => {
          if (!form.querySelector(`input[name="${k}"]`)) {
            const h = document.createElement('input');
            h.type = 'hidden';
            h.name = k;
            h.value = attr[k];
            form.appendChild(h);
          }
        });
      });
    });
  }

  // 9. Startup
  function init() {
    resolveConfigAndInit();
    enhanceWhatsAppLinks();
    autoInjectFormUTMs();
    const c = checkAndApplyConsent();
    if (c.hasAnalytics) nvTrack.pageView();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
