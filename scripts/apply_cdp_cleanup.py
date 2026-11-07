import os
import re

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# -------------------------------------------------------------
# 1. Clean app/static/js/marketing-analytics.js
# -------------------------------------------------------------
ma_path = os.path.join(BASE_DIR, "app", "static", "js", "marketing-analytics.js")
with open(ma_path, "r", encoding="utf-8") as f:
    ma_code = f.read().replace("\r\n", "\n")

# 1a. Strict Allowlist for sanitizeTelemetryPayload
old_pii = """  // PII & Numerological Chart Data Filter (DPDP Act 2023 & GDPR Privacy Compliance)
  const RESTRICTED_PII_KEYS = new Set([
    'dob', 'birth_date', 'birthdate', 'birth_time', 'birth_place', 'birth_city',
    'city', 'place', 'location', 'name', 'full_name', 'first_name', 'last_name', 'user_name',
    'email', 'phone', 'mobile', 'driver', 'conductor', 'driver_mulank', 'conductor_bhagyank',
    'mulank', 'bhagyank', 'destiny', 'lifepath', 'life_path', 'kua', 'loshu', 'grid', 'chart',
    'pan', 'card_number', 'cvv'
  ]);

  function sanitizeTelemetryPayload(obj) {
    if (!obj || typeof obj !== 'object') return obj;
    if (Array.isArray(obj)) return obj.map(sanitizeTelemetryPayload);
    const clean = {};
    for (const [key, val] of Object.entries(obj)) {
      const lowerKey = key.toLowerCase();
      if (RESTRICTED_PII_KEYS.has(lowerKey)) continue;
      if (typeof val === 'string') {
        if (/@[\w.-]+\.\w+/.test(val)) continue;
        if (/^\+?[0-9\s-]{10,15}$/.test(val.trim())) continue;
        if (/^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/.test(val.trim())) continue;
      }
      if (typeof val === 'object' && val !== null) {
        clean[key] = sanitizeTelemetryPayload(val);
      } else {
        clean[key] = val;
      }
    }
    return clean;
  }"""

new_pii = """  // Telemetry Allowlist (Strict Allowlist — DPDP Act 2023 & GDPR Privacy Compliance)
  // Only explicitly designated telemetry and attribution dimensions are permitted.
  const ALLOWED_TELEMETRY_KEYS = new Set([
    'event', 'page_path', 'page_title', 'timestamp',
    'calculator_name', 'topic', 'plan_id', 'lead_type', 'method', 'cta_location', 'ref',
    'value', 'currency', 'transaction_id', 'content_name', 'items', 'item_name', 'price', 'quantity',
    'user_id', 'golden_profile_id',
    'utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content',
    'gclid', 'fbclid', 'wbraid', 'gbraid', 'ttclid', 'msclkid',
    'gaid', 'idfa', 'idfv', 'device_id', 'device_type', 'is_pwa', 'app_platform'
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
        if (/@[\w.-]+\.\w+/.test(val)) continue;
        if (/^\+?[0-9\s-]{10,15}$/.test(val.trim())) continue;
        if (/^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$/.test(val.trim())) continue;
      }
      if (typeof val === 'object' && val !== null) {
        clean[key] = sanitizeTelemetryPayload(val);
      } else {
        clean[key] = val;
      }
    }
    return clean;
  }"""

assert old_pii in ma_code, "old_pii not found"
ma_code = ma_code.replace(old_pii, new_pii, 1)

# 1b. Config fetch replacement
old_cfg = """    // Check if configuration is provided in window or needs backend fetch
    if (!_trackingConfig || (!(_trackingConfig.ga4_measurement_id || _trackingConfig.meta_pixel_id || _trackingConfig.google_ads_id))) {
      try {
        const resp = await fetch('/api/v1/cdp/config/analytics');
        if (resp.ok) {
          const data = await resp.json();
          if (data && data.config) {
            _trackingConfig = Object.assign({}, _trackingConfig || {}, data.config);
            window.NV_TRACKING_CONFIG = _trackingConfig;
          }
        }
      } catch (e) {
        console.debug('[NV Tracking] Config fetch notice:', e);
      }
    }"""
new_cfg = "    // Static Tracking Configuration Resolution\n    _trackingConfig = Object.assign({ ga4_measurement_id: 'G-3Z2E6416W7' }, window.NV_TRACKING_CONFIG || {});"
assert old_cfg in ma_code, "old_cfg not found"
ma_code = ma_code.replace(old_cfg, new_cfg, 1)

# 1c. Clarity removal
old_clarity = """    // C. Initialize Microsoft Clarity
    if (cfg.clarity_project_id) {
      (function(c,l,a,r,i,t,y){
        c[a]=c[a]||function(){(c[a].q=c[a].q||[]).push(arguments)};
        t=l.createElement(r);t.async=1;t.src="https://www.clarity.ms/tag/"+i;
        y=l.getElementsByTagName(r)[0];y.parentNode.insertBefore(t,y);
      })(window, document, "clarity", "script", cfg.clarity_project_id);
    }"""
assert old_clarity in ma_code, "old_clarity not found"
ma_code = ma_code.replace(old_clarity, "    // Clarity Removed per CDP & Privacy Directive", 1)

# 1d. Firebase removal
old_firebase = """    // E. Initialize Firebase Web Analytics (Optional)
    if (cfg.firebase && cfg.firebase.apiKey && cfg.firebase.projectId) {
      loadScript('https://www.gstatic.com/firebasejs/10.8.0/firebase-app-compat.js', 'nv-firebase-app', false);
      setTimeout(function () {
        loadScript('https://www.gstatic.com/firebasejs/10.8.0/firebase-analytics-compat.js', 'nv-firebase-analytics', false);
        setTimeout(function () {
          try {
            if (window.firebase && !window.firebase.apps.length) {
              window.firebase.initializeApp(cfg.firebase);
              window.nvFirebaseAnalytics = window.firebase.analytics();
            }
          } catch (e) {
            console.debug('[NV Tracking] Firebase init notice:', e);
          }
        }, 300);
      }, 200);
    }"""
assert old_firebase in ma_code, "old_firebase not found"
ma_code = ma_code.replace(old_firebase, "    // Firebase Web Analytics Removed per CDP & Privacy Directive", 1)

# 1e. Remove nvFirebaseAnalytics calls
old_fb_log = """      if (window.nvFirebaseAnalytics) {
        window.nvFirebaseAnalytics.logEvent('page_view', payload);
      }"""
ma_code = ma_code.replace(old_fb_log, "")

old_fb_calc = """      if (window.nvFirebaseAnalytics) {
        window.nvFirebaseAnalytics.logEvent('calculator_used', payload);
      }"""
ma_code = ma_code.replace(old_fb_calc, "")

old_fb_signup = """      // 4. Firebase Analytics
      if (window.nvFirebaseAnalytics) {
        window.nvFirebaseAnalytics.logEvent('sign_up', payload);
      }"""
ma_code = ma_code.replace(old_fb_signup, "")

old_fb_checkout = """      if (window.nvFirebaseAnalytics) {
        window.nvFirebaseAnalytics.logEvent('begin_checkout', payload);
      }"""
ma_code = ma_code.replace(old_fb_checkout, "")

old_fb_purchase = """      // 4. Firebase Analytics
      if (window.nvFirebaseAnalytics) {
        window.nvFirebaseAnalytics.logEvent('purchase', payload);
      }"""
ma_code = ma_code.replace(old_fb_purchase, "")

old_fb_charm = """      if (window.nvFirebaseAnalytics) {
        window.nvFirebaseAnalytics.logEvent('charm_ai_query', payload);
      }"""
ma_code = ma_code.replace(old_fb_charm, "")

# 1f. Remove CDP capture in freeSignup
old_cdp_free = """      // 5. Ingest into internal CDP
      try {
        fetch('/api/v1/cdp/capture', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            name: userData?.name || null,
            email: userData?.email || null,
            phone: userData?.phone || null,
            device_id: attr.device_id,
            device_type: attr.device_type,
            utm_source: attr.utm_source,
            utm_medium: attr.utm_medium,
            utm_campaign: attr.utm_campaign,
            category: 'free_signup'
          })
        }).catch(function () {});
      } catch (e) {}"""
assert old_cdp_free in ma_code, "old_cdp_free not found"
ma_code = ma_code.replace(old_cdp_free, "", 1)

# 1g. Remove CDP capture in paidPurchase
old_cdp_paid = """      // 5. Ingest into internal CDP with spend update
      try {
        fetch('/api/v1/cdp/capture', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            device_id: attr.device_id,
            device_type: attr.device_type,
            total_spend_inr: val,
            category: 'paid_report_purchase'
          })
        }).catch(function () {});
      } catch (e) {}"""
assert old_cdp_paid in ma_code, "old_cdp_paid not found"
ma_code = ma_code.replace(old_cdp_paid, "", 1)

# 1h. In pageView, enforce ALLOWED_TELEMETRY_KEYS on query parameters
ma_code = ma_code.replace("!RESTRICTED_PII_KEYS.has(k)", "ALLOWED_TELEMETRY_KEYS.has(k)")

with open(ma_path, "w", encoding="utf-8") as f:
    f.write(ma_code)
print(f"Updated {ma_path} cleanly.")
