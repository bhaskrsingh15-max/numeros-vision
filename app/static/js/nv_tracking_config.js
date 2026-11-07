/**
 * ==============================================================================
 * NUMEROS VISION — MASTER TRACKING, PIXELS & ANALYTICS CONFIGURATION
 * ==============================================================================
 * 
 * Instructions:
 * Whenever you obtain your tracking IDs or pixels from Google, Meta, or Firebase,
 * simply paste them into the corresponding fields below (or set them in your server .env).
 * The tracking suite will automatically initialize and fire the appropriate events.
 * 
 * If a field is left empty (""), that specific tracker remains in safe standby mode
 * without firing any external network requests or generating console errors.
 */

window.NV_TRACKING_CONFIG = {
  // 1. Google Analytics 4 (GA4)
  // Format: "G-XXXXXXXXXX"
  // Source: Google Analytics -> Admin -> Data Streams -> Measurement ID
  ga4_measurement_id: "G-3Z2E6416W7",

  // 2. Google Ads (AdWords) Conversion & Remarketing
  // Format: "AW-XXXXXXXXXX"
  // Source: Google Ads -> Tools & Settings -> Conversions -> Tag setup
  google_ads_id: "",

  // Google Ads Conversion Labels (Optional: for tracking specific goals)
  // Conversion Label for Free Seeker Signup / Lead:
  google_ads_conversion_label_signup: "",

  // Conversion Label for Paid Reports / Consultation Purchase:
  google_ads_conversion_label_purchase: "",

  // 3. Meta (Facebook & Instagram) Pixel
  // Format: "123456789012345" (Numeric ID)
  // Source: Meta Events Manager -> Data Sources -> Pixel ID
  meta_pixel_id: "",

  // 4. Google Tag Manager (GTM) Container (Optional override)
  // Format: "GTM-XXXXXXX"
  // Source: tagmanager.google.com -> Container ID
  gtm_container_id: "GTM-KW6GQRVZ",

  // 5. Microsoft Clarity (Free Heatmaps, Scroll Maps & Session Recordings)
  // Format: "xxxxxxxxxx" (10-character project ID)
  // Source: clarity.microsoft.com -> Project Settings
  clarity_project_id: "",

  // 6. Firebase Web SDK & Analytics Configuration
  // Source: Firebase Console -> Project Settings -> General -> Your Apps -> Web App
  firebase: {
    apiKey: "",
    authDomain: "",
    projectId: "",
    storageBucket: "",
    messagingSenderId: "",
    appId: "",
    measurementId: ""
  },

  // 7. Advanced Diagnostics & Console Logging
  // Set to true while testing in staging to view live event payloads in DevTools
  debug_mode: false
};
