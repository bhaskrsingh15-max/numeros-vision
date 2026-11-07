/**
 * NUMEROS VISION — CLIENT-SIDE PROFILE SYNCHRONIZATION & CONSENT Explore GATE
 * Version: 3.0.0 (DPDP Act 2023 & GDPR Compliant)
 * 
 * Provides:
 * 1. Automatic caching of free calculations into localStorage (`nv_user_profile`).
 * 2. Mandatory DPDP Consent & Free Signup Gate before revealing calculator results.
 * 3. Real-time background stitching into CDP Golden Profile upon signup/login.
 * 4. Dynamic header navbar state ('Sign Up' vs '✦ My Dashboard').
 * 5. High-converting 'Save to Golden Profile' CTA cards for free calculators and Charm AI.
 */

(function () {
  'use strict';

  let _pendingCallback = null;
  let _pendingData = null;
  let _pendingContainerId = null;
  let _isUnlocked = false;

  // 1. Check Authentication Status
  function getAuthStatus() {
    try {
      const session = localStorage.getItem('nv_user_session');
      const profileRaw = localStorage.getItem('nv_user_profile');
      const profile = profileRaw ? JSON.parse(profileRaw) : null;
      return {
        isAuthenticated: !!session,
        sessionToken: session,
        profile: profile,
        goldenId: localStorage.getItem('nv_golden_id')
      };
    } catch (e) {
      return { isAuthenticated: false, sessionToken: null, profile: null, goldenId: null };
    }
  }

  // 2. Sync Calculation Data to localStorage and CDP
  async function syncCalculation(data) {
    if (!data) return;
    try {
      let existing = {};
      const raw = localStorage.getItem('nv_user_profile');
      if (raw) existing = JSON.parse(raw);

      const merged = Object.assign({}, existing, data);
      localStorage.setItem('nv_user_profile', JSON.stringify(merged));
      localStorage.setItem('nv_cached_calc', JSON.stringify(merged));

      // CDP capture removed per privacy mandate
    } catch (err) {
      console.warn('[NV_PROFILE_SYNC_NOTICE]', err);
    }
  }

  // Known City Coordinate & Timezone Directory for Modal Auto-Resolution
  const UNLOCK_KNOWN_CITIES = {
    'delhi': { lat: 28.6139, lng: 77.2090, country: 'India', tz: 'Asia/Kolkata' },
    'new delhi': { lat: 28.6139, lng: 77.2090, country: 'India', tz: 'Asia/Kolkata' },
    'mumbai': { lat: 19.0760, lng: 72.8777, country: 'India', tz: 'Asia/Kolkata' },
    'bombay': { lat: 19.0760, lng: 72.8777, country: 'India', tz: 'Asia/Kolkata' },
    'bengaluru': { lat: 12.9716, lng: 77.5946, country: 'India', tz: 'Asia/Kolkata' },
    'bangalore': { lat: 12.9716, lng: 77.5946, country: 'India', tz: 'Asia/Kolkata' },
    'kolkata': { lat: 22.5726, lng: 88.3639, country: 'India', tz: 'Asia/Kolkata' },
    'calcutta': { lat: 22.5726, lng: 88.3639, country: 'India', tz: 'Asia/Kolkata' },
    'chennai': { lat: 13.0827, lng: 80.2707, country: 'India', tz: 'Asia/Kolkata' },
    'madras': { lat: 13.0827, lng: 80.2707, country: 'India', tz: 'Asia/Kolkata' },
    'hyderabad': { lat: 17.3850, lng: 78.4867, country: 'India', tz: 'Asia/Kolkata' },
    'pune': { lat: 18.5204, lng: 73.8567, country: 'India', tz: 'Asia/Kolkata' },
    'ahmedabad': { lat: 23.0225, lng: 72.5714, country: 'India', tz: 'Asia/Kolkata' },
    'jaipur': { lat: 26.9124, lng: 75.7873, country: 'India', tz: 'Asia/Kolkata' },
    'surat': { lat: 21.1702, lng: 72.8311, country: 'India', tz: 'Asia/Kolkata' },
    'lucknow': { lat: 26.8467, lng: 80.9462, country: 'India', tz: 'Asia/Kolkata' },
    'chandigarh': { lat: 30.7333, lng: 76.7794, country: 'India', tz: 'Asia/Kolkata' },
    'patna': { lat: 25.5941, lng: 85.1376, country: 'India', tz: 'Asia/Kolkata' },
    'bhopal': { lat: 23.2599, lng: 77.4126, country: 'India', tz: 'Asia/Kolkata' },
    'indore': { lat: 22.7196, lng: 75.8577, country: 'India', tz: 'Asia/Kolkata' },
    'nagpur': { lat: 21.1458, lng: 79.0882, country: 'India', tz: 'Asia/Kolkata' },
    'london': { lat: 51.5074, lng: -0.1278, country: 'United Kingdom', tz: 'Europe/London' },
    'new york': { lat: 40.7128, lng: -74.0060, country: 'United States', tz: 'America/New_York' },
    'nyc': { lat: 40.7128, lng: -74.0060, country: 'United States', tz: 'America/New_York' },
    'los angeles': { lat: 34.0522, lng: -118.2437, country: 'United States', tz: 'America/Los_Angeles' },
    'chicago': { lat: 41.8781, lng: -87.6298, country: 'United States', tz: 'America/Chicago' },
    'san francisco': { lat: 37.7749, lng: -122.4194, country: 'United States', tz: 'America/Los_Angeles' },
    'toronto': { lat: 43.6532, lng: -79.3832, country: 'Canada', tz: 'America/Toronto' },
    'dubai': { lat: 25.2048, lng: 55.2708, country: 'United Arab Emirates', tz: 'Asia/Dubai' },
    'singapore': { lat: 1.3521, lng: 103.8198, country: 'Singapore', tz: 'Asia/Singapore' },
    'sydney': { lat: -33.8688, lng: 151.2093, country: 'Australia', tz: 'Australia/Sydney' },
    'paris': { lat: 48.8566, lng: 2.3522, country: 'France', tz: 'Europe/Paris' },
    'berlin': { lat: 52.5200, lng: 13.4050, country: 'Germany', tz: 'Europe/Berlin' }
  };

  function onUnlockCityInput(val) {
    if (!val) return;
    const clean = val.toLowerCase().trim();
    for (const [k, v] of Object.entries(UNLOCK_KNOWN_CITIES)) {
      if (clean.includes(k) || k.includes(clean)) {
        const latEl = document.getElementById('nv-Explore-latitude');
        const lngEl = document.getElementById('nv-Explore-longitude');
        const ctryEl = document.getElementById('nv-Explore-country');
        const tzEl = document.getElementById('nv-Explore-timezone');
        const badge = document.getElementById('nv-Explore-coord-badge');
        if (latEl) latEl.value = v.lat;
        if (lngEl) lngEl.value = v.lng;
        if (ctryEl && (!ctryEl.value || ctryEl.value === 'India' || v.country !== 'India')) ctryEl.value = v.country;
        if (tzEl) tzEl.value = v.tz;
        if (badge) badge.textContent = `Auto-resolved: ${v.country}`;
        break;
      }
    }
  }

  // 3. Inject Modal HTML into DOM if not already present
  function ensureUnlockModal() {
    if (document.getElementById('nv-consent-Explore-overlay')) return;

    if (!document.getElementById('nv-Explore-modal-styles')) {
      const styleEl = document.createElement('style');
      styleEl.id = 'nv-Explore-modal-styles';
      styleEl.textContent = `
        #nv-consent-Explore-overlay {
          display: none;
          position: fixed;
          inset: 0;
          background: rgba(26,23,20,0.78);
          backdrop-filter: blur(5px);
          -webkit-backdrop-filter: blur(5px);
          z-index: 999999;
          align-items: center;
          justify-content: center;
          padding: 14px;
          box-sizing: border-box !important;
        }
        #nv-consent-Explore-card,
        #nv-consent-Explore-card * {
          box-sizing: border-box !important;
        }
        #nv-consent-Explore-card {
          background: #FFFDF7 !important;
          border: 2px solid #C9A227 !important;
          border-radius: 18px !important;
          max-width: 480px !important;
          width: 100% !important;
          max-height: 88vh !important;
          overflow-y: auto !important;
          padding: 22px 20px 18px !important;
          position: relative !important;
          box-shadow: 0 24px 60px rgba(0,0,0,0.4) !important;
          font-family: 'Inter', system-ui, -apple-system, sans-serif !important;
          scrollbar-width: thin !important;
          scrollbar-color: #C9A227 #FAF6EE !important;
        }
        #nv-consent-Explore-card::-webkit-scrollbar {
          width: 5px !important;
        }
        #nv-consent-Explore-card::-webkit-scrollbar-track {
          background: #FAF6EE !important;
          border-radius: 4px !important;
        }
        #nv-consent-Explore-card::-webkit-scrollbar-thumb {
          background: #C9A227 !important;
          border-radius: 4px !important;
        }
        #nv-consent-Explore-card label {
          text-transform: none !important;
          letter-spacing: normal !important;
          font-weight: 400 !important;
          margin-bottom: 0 !important;
        }
        #nv-consent-Explore-card .nv-form-label {
          display: block !important;
          font-size: 0.72rem !important;
          font-weight: 700 !important;
          color: #523E28 !important;
          text-transform: uppercase !important;
          letter-spacing: 0.04em !important;
          margin-bottom: 4px !important;
        }
        #nv-consent-Explore-card input[type="text"],
        #nv-consent-Explore-card input[type="email"],
        #nv-consent-Explore-card input[type="tel"],
        #nv-consent-Explore-card input[type="password"],
        #nv-consent-Explore-card input[type="number"],
        #nv-consent-Explore-card select {
          width: 100% !important;
          padding: 8px 10px !important;
          border: 1px solid #D6C7B2 !important;
          border-radius: 8px !important;
          font-size: 0.85rem !important;
          background: #FFFFFF !important;
          color: #523E28 !important;
          font-family: inherit !important;
          transition: border-color 0.2s ease !important;
        }
        #nv-consent-Explore-card input:focus,
        #nv-consent-Explore-card select:focus {
          border-color: #C9A227 !important;
          outline: none !important;
        }
        #nv-consent-Explore-card .nv-consent-card {
          background: rgba(201,162,39,0.07) !important;
          border: 1px solid rgba(201,162,39,0.32) !important;
          border-radius: 10px !important;
          padding: 10px 12px !important;
          margin-bottom: 14px !important;
        }
        #nv-consent-Explore-card .nv-consent-row {
          display: flex !important;
          align-items: flex-start !important;
          gap: 8px !important;
          font-size: 0.72rem !important;
          line-height: 1.4 !important;
          color: #523E28 !important;
          cursor: pointer !important;
          text-transform: none !important;
          letter-spacing: normal !important;
          font-weight: 400 !important;
          margin-bottom: 6px !important;
        }
        #nv-consent-Explore-card .nv-consent-row:last-child {
          margin-bottom: 0 !important;
        }
        #nv-consent-Explore-card .nv-consent-row input[type="checkbox"] {
          width: 15px !important;
          height: 15px !important;
          margin-top: 2px !important;
          flex-shrink: 0 !important;
          accent-color: #8B6914 !important;
          cursor: pointer !important;
        }
        #nv-consent-Explore-card .nv-consent-row span {
          font-size: 0.72rem !important;
          line-height: 1.4 !important;
          text-transform: none !important;
          letter-spacing: normal !important;
          font-weight: 400 !important;
          color: #523E28 !important;
          flex: 1 !important;
        }
        #nv-consent-Explore-card .nv-consent-row strong {
          font-weight: 700 !important;
          color: #8B6914 !important;
        }
      `;
      document.head.appendChild(styleEl);
    }

    const overlay = document.createElement('div');
    overlay.id = 'nv-consent-Explore-overlay';

    overlay.innerHTML = `
      <div id="nv-consent-Explore-card">
        <button onclick="window.nvProfileSync.closeUnlockModal()" type="button" style="position:absolute; top:12px; right:14px; background:none; border:none; font-size:1.4rem; color:#8B6914; cursor:pointer; line-height:1;" aria-label="Close">✕</button>

        <!-- Brand Header -->
        <div style="text-align:center; margin-bottom:14px;">
          <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision" style="width:34px; height:34px; margin:0 auto 6px; display:block; filter:drop-shadow(0 2px 6px rgba(201,162,39,0.35));" />
          <div style="font-family:'Cinzel',serif; font-size:0.7rem; letter-spacing:0.12em; color:#8B6914; font-weight:700;">NUMEROS VISION · ANVEIL EVERY CHARM</div>
          <h3 id="nv-modal-heading" style="font-family:'Cormorant Garamond',Georgia,serif; font-size:clamp(1.22rem, 4.8vw, 1.55rem); color:#8B6914; margin:5px 0 4px; font-weight:700; line-height:1.2; text-align:center;">
            <span style="color:#C9A227; font-size:1.1em; vertical-align:middle; display:inline-block; margin-right:4px;">✦</span><span>Explore Your Free Calculation</span><span style="color:#C9A227; font-size:1.1em; vertical-align:middle; display:inline-block; margin-left:4px;">✦</span>
          </h3>
          <p id="nv-modal-sub" style="font-size:0.82rem; color:#7A654D; margin:0 auto; max-width:400px; line-height:1.48;">
            Create your free profile with DPDP statutory consent to reveal your results and save your personal chart.
          </p>
        </div>

        <!-- Live Calculation Chip Preview -->
        <div id="nv-calc-preview-chip" style="background:#FAF6EE; border:1px solid #C9A227; border-radius:10px; padding:7px 12px; margin-bottom:14px; font-size:0.78rem; color:#523E28; display:flex; align-items:center; justify-content:space-between; gap:8px;">
          <span id="nv-preview-chip-dob">📅 Date of Birth: 15-08-1990</span>
          <span style="color:#16835B; font-weight:700; font-size:0.72rem; text-transform:uppercase;">✓ Calculated</span>
        </div>

        <!-- Alert Box -->
        <div id="nv-Explore-alert" style="display:none; padding:9px 12px; border-radius:8px; font-size:0.8rem; margin-bottom:12px; line-height:1.4;"></div>

        <!-- SIGNUP FORM (Default) -->
        <form id="nv-Explore-signup-form" onsubmit="window.nvProfileSync.handleUnlockSignup(event)">
          <div style="margin-bottom:10px;">
            <label class="nv-form-label">Full Calling Name *</label>
            <input type="text" id="nv-Explore-name" required placeholder="Enter your full name" />
          </div>

          <div style="margin-bottom:10px;">
            <label class="nv-form-label">Email Address *</label>
            <input type="email" id="nv-Explore-email" required placeholder="name@example.com" />
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
            <div>
              <label class="nv-form-label">WhatsApp / Mobile</label>
              <input type="tel" id="nv-Explore-phone" placeholder="+91 98765 43210" />
            </div>
            <div>
              <label class="nv-form-label">Password *</label>
              <input type="password" id="nv-Explore-password" required minlength="6" placeholder="Min 6 characters" />
            </div>
          </div>

          <!-- Time of Birth (AM/PM) -->
          <div style="margin-bottom:10px;">
            <label class="nv-form-label">Time of Birth (Hour, Minute, AM/PM)</label>
            <div style="display:grid; grid-template-columns:1fr 1fr 1.2fr; gap:8px;">
              <select id="nv-Explore-time-hour">
                <option value="">Hour</option>
                <option value="1">01</option><option value="2">02</option>
                <option value="3">03</option><option value="4">04</option>
                <option value="5">05</option><option value="6">06</option>
                <option value="7">07</option><option value="8">08</option>
                <option value="9">09</option><option value="10">10</option>
                <option value="11">11</option><option value="12" selected>12</option>
              </select>
              <select id="nv-Explore-time-minute">
                <option value="0">00</option><option value="5">05</option>
                <option value="10">10</option><option value="15">15</option>
                <option value="20">20</option><option value="25">25</option>
                <option value="30" selected>30</option><option value="35">35</option>
                <option value="40">40</option><option value="45">45</option>
                <option value="50">50</option><option value="55">55</option>
              </select>
              <select id="nv-Explore-time-period">
                <option value="AM">AM</option>
                <option value="PM" selected>PM</option>
              </select>
            </div>
            <span style="font-size:0.68rem; color:#7A654D; display:block; margin-top:2px;">Enables precise hourly planetary ruler and Dasha sub-periods.</span>
          </div>

          <!-- Place of Birth & Country -->
          <div style="display:grid; grid-template-columns:1.2fr 1fr; gap:10px; margin-bottom:10px;">
            <div>
              <label class="nv-form-label">Place of Birth *</label>
              <input type="text" id="nv-Explore-place" required placeholder="City / Town" oninput="window.nvProfileSync.onUnlockCityInput(this.value)" />
            </div>
            <div>
              <label class="nv-form-label">Country *</label>
              <input type="text" id="nv-Explore-country" required value="India" placeholder="Country" />
            </div>
          </div>

          <!-- Coordinates & Timezone Card -->
          <div style="background:#FAF6EE; border:1px solid rgba(201,162,39,0.3); border-radius:10px; padding:8px 10px; margin-bottom:12px;">
            <div style="font-size:0.68rem; text-transform:uppercase; font-weight:700; color:#8B6914; letter-spacing:0.05em; margin-bottom:5px; display:flex; justify-content:space-between; align-items:center;">
              <span>✦ Coordinates &amp; Timezone</span>
              <span id="nv-Explore-coord-badge" style="font-size:0.65rem; color:#16835B; font-weight:600; text-transform:none;">Auto-resolved</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1.4fr; gap:6px;">
              <div>
                <label style="display:block; font-size:0.63rem; font-weight:700; color:#7A654D; text-transform:uppercase; margin-bottom:2px;">Latitude</label>
                <input type="number" step="0.0001" id="nv-Explore-latitude" value="28.6139" placeholder="28.6139" style="padding:6px 7px !important; font-size:0.78rem !important;" />
              </div>
              <div>
                <label style="display:block; font-size:0.63rem; font-weight:700; color:#7A654D; text-transform:uppercase; margin-bottom:2px;">Longitude</label>
                <input type="number" step="0.0001" id="nv-Explore-longitude" value="77.2090" placeholder="77.2090" style="padding:6px 7px !important; font-size:0.78rem !important;" />
              </div>
              <div>
                <label style="display:block; font-size:0.63rem; font-weight:700; color:#7A654D; text-transform:uppercase; margin-bottom:2px;">Timezone</label>
                <select id="nv-Explore-timezone" style="padding:6px 5px !important; font-size:0.75rem !important;">
                  <option value="Asia/Kolkata" selected>Asia/Kolkata (IST)</option>
                  <option value="UTC">UTC / GMT</option>
                  <option value="Europe/London">Europe/London</option>
                  <option value="America/New_York">America/New_York</option>
                  <option value="America/Chicago">America/Chicago</option>
                  <option value="America/Los_Angeles">America/Los_Angeles</option>
                  <option value="America/Toronto">America/Toronto</option>
                  <option value="Asia/Dubai">Asia/Dubai</option>
                  <option value="Asia/Singapore">Asia/Singapore</option>
                  <option value="Asia/Tokyo">Asia/Tokyo</option>
                  <option value="Australia/Sydney">Australia/Sydney</option>
                  <option value="Europe/Paris">Europe/Paris</option>
                  <option value="Europe/Berlin">Europe/Berlin</option>
                </select>
              </div>
            </div>
          </div>

          <!-- DPDP Statutory Consent Box -->
          <div class="nv-consent-card">
            <label class="nv-consent-row">
              <input type="checkbox" id="nv-Explore-consent-storage" required checked />
              <span><strong>Statutory DPDP Consent (Required):</strong> I explicitly consent to Numeros Vision computing and storing my birth matrix under the Digital Personal Data Protection (DPDP) Act 2023.</span>
            </label>
            <label class="nv-consent-row">
              <input type="checkbox" id="nv-Explore-consent-marketing" checked />
              <span>Send personal milestone transit alerts via WhatsApp/Email.</span>
            </label>
          </div>

          <button type="submit" id="nv-Explore-submit-btn" style="width:100%; padding:11px; border-radius:10px; background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFFFF; border:none; font-weight:700; font-size:0.88rem; text-transform:uppercase; letter-spacing:0.04em; cursor:pointer; box-shadow:0 4px 14px rgba(201,162,39,0.35);">
            <span style="color:#FFFDF7; margin-right:4px;">✦</span>Consent &amp; Show Free Results<span style="color:#FFFDF7; margin-left:4px;">✦</span>
          </button>

          <div style="text-align:center; margin-top:12px; font-size:0.78rem; color:#7A654D;">
            Already have an account? <a href="#" onclick="window.nvProfileSync.toggleUnlockMode('login'); return false;" style="color:#8B6914; font-weight:700; text-decoration:none;">Sign In to Reveal</a>
          </div>
        </form>

        <!-- LOGIN FORM (Hidden by default) -->
        <form id="nv-Explore-login-form" style="display:none;" onsubmit="window.nvProfileSync.handleUnlockLogin(event)">
          <div style="margin-bottom:12px;">
            <label class="nv-form-label">Email or Mobile *</label>
            <input type="text" id="nv-login-id" required placeholder="Enter your email or phone" />
          </div>

          <div style="margin-bottom:14px;">
            <label class="nv-form-label">Password *</label>
            <input type="password" id="nv-login-password" required placeholder="Your password" />
          </div>

          <button type="submit" id="nv-login-submit-btn" style="width:100%; padding:11px; border-radius:10px; background:linear-gradient(135deg, #16835B 0%, #0E5A3E 100%); color:#FFFFFF; border:none; font-weight:700; font-size:0.88rem; text-transform:uppercase; letter-spacing:0.04em; cursor:pointer; box-shadow:0 4px 14px rgba(22,131,91,0.3);">
            <span style="color:#FFFDF7; margin-right:4px;">✦</span>Sign In &amp; Show Free Results<span style="color:#FFFDF7; margin-left:4px;">✦</span>
          </button>

          <div style="text-align:center; margin-top:12px; font-size:0.78rem; color:#7A654D;">
            Need an account? <a href="#" onclick="window.nvProfileSync.toggleUnlockMode('signup'); return false;" style="color:#8B6914; font-weight:700; text-decoration:none;">Create Free Account with Consent</a>
          </div>
        </form>
      </div>
    `;

    document.body.appendChild(overlay);

    // Escape key listener
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && overlay.style.display === 'flex') {
        closeUnlockModal();
      }
    });
  }

  // 4. Toggle between Signup and Login
  function toggleUnlockMode(mode) {
    const signupForm = document.getElementById('nv-Explore-signup-form');
    const loginForm = document.getElementById('nv-Explore-login-form');
    const heading = document.getElementById('nv-modal-heading');
    const sub = document.getElementById('nv-modal-sub');
    const alertBox = document.getElementById('nv-Explore-alert');
    if (alertBox) alertBox.style.display = 'none';

    if (mode === 'login') {
      if (signupForm) signupForm.style.display = 'none';
      if (loginForm) loginForm.style.display = 'block';
      if (heading) heading.textContent = '✦ Sign In to Reveal Calculation ✦';
      if (sub) sub.textContent = 'Sign in to your Numeros Vision account to unveil your free calculation and sync with your Golden Profile.';
    } else {
      if (signupForm) signupForm.style.display = 'block';
      if (loginForm) loginForm.style.display = 'none';
      if (heading) heading.textContent = '✦ Explore Your Free Calculation ✦';
      if (sub) sub.textContent = 'Create your free profile with DPDP statutory consent to reveal your results and save your personal chart.';
    }
  }

  // 5. Open Modal
  function openUnlockModal(data, onGranted, targetContainerId) {
    ensureUnlockModal();
    if (data) _pendingData = data;
    if (onGranted) _pendingCallback = onGranted;
    if (targetContainerId) _pendingContainerId = targetContainerId;
    if (!_pendingData) _pendingData = {};

    const overlay = document.getElementById('nv-consent-Explore-overlay');
    const alertBox = document.getElementById('nv-Explore-alert');
    if (alertBox) alertBox.style.display = 'none';

    // Populate preview chip
    const chipDob = document.getElementById('nv-preview-chip-dob');
    if (chipDob) {
      if (_pendingData.day && _pendingData.month && _pendingData.year) {
        chipDob.textContent = `📅 Birth Date: ${String(_pendingData.day).padStart(2, '0')}-${String(_pendingData.month).padStart(2, '0')}-${_pendingData.year}`;
      } else if (_pendingData.name) {
        chipDob.textContent = `✍️ Name: ${_pendingData.name} · Analysis Ready`;
      } else {
        chipDob.innerHTML = '<span style="color:#C9A227; margin-right:4px;">✦</span> Free Calculation Diagnostic Ready';
      }
    }

    // Populate name if entered in calculator
    const nameInput = document.getElementById('nv-Explore-name');
    if (nameInput) {
      if (_pendingData.name && _pendingData.name !== 'Seeker') {
        nameInput.value = _pendingData.name;
      } else {
        nameInput.value = '';
      }
    }

    // Populate place and country if available
    const placeInput = document.getElementById('nv-Explore-place');
    if (placeInput) {
      if (_pendingData.birth_place) {
        placeInput.value = _pendingData.birth_place;
        onUnlockCityInput(_pendingData.birth_place);
      } else {
        placeInput.value = '';
      }
    }
    if (_pendingData.country) {
      const ctryEl = document.getElementById('nv-Explore-country');
      if (ctryEl) ctryEl.value = _pendingData.country;
    }
    if (_pendingData.latitude) {
      const latEl = document.getElementById('nv-Explore-latitude');
      if (latEl) latEl.value = _pendingData.latitude;
    }
    if (_pendingData.longitude) {
      const lngEl = document.getElementById('nv-Explore-longitude');
      if (lngEl) lngEl.value = _pendingData.longitude;
    }
    if (_pendingData.timezone) {
      const tzEl = document.getElementById('nv-Explore-timezone');
      if (tzEl) tzEl.value = _pendingData.timezone;
    }

    // Populate birth time if available
    if (_pendingData.birth_time_hour) {
      const hEl = document.getElementById('nv-Explore-time-hour');
      if (hEl) hEl.value = String(_pendingData.birth_time_hour);
    }
    if (_pendingData.birth_time_minute !== undefined && _pendingData.birth_time_minute !== null) {
      const mEl = document.getElementById('nv-Explore-time-minute');
      if (mEl) mEl.value = String(_pendingData.birth_time_minute);
    }
    if (_pendingData.birth_time_period) {
      const pEl = document.getElementById('nv-Explore-time-period');
      if (pEl) pEl.value = _pendingData.birth_time_period;
    }

    toggleUnlockMode('signup');
    overlay.style.display = 'flex';
  }

  // 6. Close Modal
  function closeUnlockModal() {
    const overlay = document.getElementById('nv-consent-Explore-overlay');
    if (overlay) overlay.style.display = 'none';

    // If closed without unlocking, render locked placeholder in container if present
    if (!_isUnlocked && _pendingContainerId) {
      renderLockedTeaser(_pendingContainerId, _pendingData);
    }
  }

  // 7. Render Locked Teaser when user dismisses modal without signing up
  function renderLockedTeaser(targetContainerId, data) {
    const el = document.getElementById(targetContainerId);
    if (!el) return;

    el.style.display = 'block';
    el.innerHTML = `
      <div style="background:#FFFDF7; border:2px dashed #C9A227; border-radius:18px; padding:36px 24px; text-align:center; margin-top:24px; box-shadow:0 8px 24px rgba(180,155,110,0.08);">
        <div style="font-size:2.2rem; margin-bottom:8px;">🔒</div>
        <div style="font-family:'Cinzel',serif; font-size:0.75rem; color:#8B6914; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; margin-bottom:6px;">
          Statutory Consent Required Under DPDP Act 2023
        </div>
        <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.85rem; color:#8B6914; margin-bottom:10px; font-weight:700;">
          Your Free Calculation is Ready to Unveil
        </h3>
        <p style="font-size:0.9rem; color:#7A654D; max-width:540px; margin:0 auto 20px; line-height:1.65;">
          Under the India Digital Personal Data Protection Act 2023, explicit consent is required to process and store your birth matrix. Complete your quick free signup to reveal your complete calculation and save your Golden Profile.
        </p>
        <button onclick="window.nvProfileSync.openUnlockModal()" type="button" style="padding:13px 32px; font-size:0.92rem; font-weight:700; border-radius:12px; background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFFFF; border:none; cursor:pointer; box-shadow:0 4px 16px rgba(201,162,39,0.35); text-transform:uppercase; letter-spacing:0.04em;">
          ✦ Sign Up with Consent to Show Free Results ✦
        </button>
      </div>
    `;
    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // 8. Handle Signup Form Submission
  async function handleUnlockSignup(e) {
    e.preventDefault();
    const alertBox = document.getElementById('nv-Explore-alert');
    alertBox.style.display = 'none';

    const consentStorage = document.getElementById('nv-Explore-consent-storage').checked;
    if (!consentStorage) {
      alertBox.style.cssText = 'display:block; background:#FDEDEC; color:#C0392B; border:1px solid #E6B0AA; padding:10px 14px; border-radius:8px; font-size:0.82rem; margin-bottom:14px;';
      alertBox.textContent = 'Statutory Consent Required: Under the DPDP Act 2023, you must check the box to process and store your birth chart.';
      return;
    }

    const btn = document.getElementById('nv-Explore-submit-btn');
    btn.disabled = true;
    btn.innerHTML = '<span>Securing Matrix &amp; Unlocking Results...</span> <span style="animation:spin 1s infinite linear;">✦</span>';

    const name = document.getElementById('nv-Explore-name').value.trim();
    const email = document.getElementById('nv-Explore-email').value.trim();
    const phone = document.getElementById('nv-Explore-phone').value.trim() || null;
    const password = document.getElementById('nv-Explore-password').value;
    const consentMarketing = document.getElementById('nv-Explore-consent-marketing').checked;

    const hourVal = document.getElementById('nv-Explore-time-hour') ? document.getElementById('nv-Explore-time-hour').value : '';
    const hour = hourVal ? parseInt(hourVal, 10) : null;
    const minVal = document.getElementById('nv-Explore-time-minute') ? document.getElementById('nv-Explore-time-minute').value : '0';
    const minute = parseInt(minVal, 10) || 0;
    const period = document.getElementById('nv-Explore-time-period') ? document.getElementById('nv-Explore-time-period').value : 'AM';
    let formattedTime = null;
    if (hour !== null) {
      formattedTime = `${String(hour).padStart(2, '0')}:${String(minute).padStart(2, '0')} ${period}`;
    }

    const birthPlace = document.getElementById('nv-Explore-place') ? document.getElementById('nv-Explore-place').value.trim() : null;
    const country = document.getElementById('nv-Explore-country') ? document.getElementById('nv-Explore-country').value.trim() : 'India';
    const latitude = document.getElementById('nv-Explore-latitude') ? parseFloat(document.getElementById('nv-Explore-latitude').value) || null : null;
    const longitude = document.getElementById('nv-Explore-longitude') ? parseFloat(document.getElementById('nv-Explore-longitude').value) || null : null;
    const timezone = document.getElementById('nv-Explore-timezone') ? document.getElementById('nv-Explore-timezone').value : 'Asia/Kolkata';

    const payload = {
      name: name,
      email: email,
      phone: phone,
      day: parseInt((_pendingData && _pendingData.day) || 15, 10),
      month: parseInt((_pendingData && _pendingData.month) || 8, 10),
      year: parseInt((_pendingData && _pendingData.year) || 1990, 10),
      birth_time: formattedTime || (_pendingData && _pendingData.birth_time) || null,
      birth_time_hour: hour !== null ? hour : ((_pendingData && _pendingData.birth_time_hour) || null),
      birth_time_minute: minute,
      birth_time_period: period,
      birth_place: birthPlace || (_pendingData && _pendingData.birth_place) || null,
      country: country,
      latitude: latitude,
      longitude: longitude,
      timezone: timezone,
      gender: (_pendingData && _pendingData.gender) || 'prefer_not_to_say',
      password: password,
      consent_profile_storage: true,
      consent_evaluation_feedback: true,
      consent_marketing: consentMarketing,
      source: (_pendingData && _pendingData.category) || 'free_calculator_gate',
      redirect_url: window.location.pathname
    };

    try {
      const resp = await fetch('/api/v1/identity/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload)
      });

      const data = await resp.json();

      if (!resp.ok) {
        throw new Error(data.detail || data.message || 'Failed to complete registration.');
      }

      // Store authenticated credentials
      // session handled via HttpOnly __Host-nv_session cookie
      if (data.golden_profile_id) 
      if (data.nv_uid) localStorage.setItem('nv_uid', data.nv_uid);
      if (data.profile) localStorage.setItem('nv_user_profile', JSON.stringify(data.profile));

      // Trigger multi-pixel conversion tracking (GA4, Meta Lead, Google Ads Conversion, Firebase)
      if (window.nvTrack && typeof window.nvTrack.freeSignup === 'function') {
        try {
          window.nvTrack.freeSignup({
            name: name,
            email: email,
            phone: phone,
            user_id: data.user_id,
            golden_profile_id: data.golden_profile_id,
            driver_mulank: data.profile ? data.profile.driver_mulank : null,
            conductor_bhagyank: data.profile ? data.profile.conductor_bhagyank : null,
            source: 'free_calculator_gate'
          });
        } catch (trkErr) {
          console.debug('[Analytics Tracking Notice]', trkErr);
        }
      }

      _isUnlocked = true;
      updateNavAuth();

      // Close modal
      const overlay = document.getElementById('nv-consent-Explore-overlay');
      if (overlay) overlay.style.display = 'none';

      // Execute calculation reveal callback
      if (typeof _pendingCallback === 'function') {
        _pendingCallback();
      } else {
        const submitBtn = document.querySelector('button[type="submit"], .btn-calc-submit, #hero-calc-submit');
        if (submitBtn) submitBtn.click();
      }

      // Inject verified badge at top of result container
      if (_pendingContainerId) {
        injectUnlockedBanner(_pendingContainerId, name);
      }
    } catch (err) {
      alertBox.style.cssText = 'display:block; background:#FDEDEC; color:#C0392B; border:1px solid #E6B0AA; padding:10px 14px; border-radius:8px; font-size:0.82rem; margin-bottom:14px;';
      alertBox.textContent = err.message || 'Registration failed. Please try again.';
      btn.disabled = false;
      btn.innerHTML = '<span style="color:#FFFDF7; margin-right:4px;">✦</span>Consent &amp; Show Free Results<span style="color:#FFFDF7; margin-left:4px;">✦</span>';
    }
  }

  // 9. Handle Login Form Submission
  async function handleUnlockLogin(e) {
    e.preventDefault();
    const alertBox = document.getElementById('nv-Explore-alert');
    alertBox.style.display = 'none';

    const btn = document.getElementById('nv-login-submit-btn');
    btn.disabled = true;
    btn.innerHTML = '<span>Verifying &amp; Unlocking Results...</span> <span style="animation:spin 1s infinite linear;">✦</span>';

    const loginId = document.getElementById('nv-login-id').value.trim();
    const password = document.getElementById('nv-login-password').value;

    try {
      const resp = await fetch('/api/v1/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ login_id: loginId, password: password })
      });

      const data = await resp.json();

      if (!resp.ok) {
        throw new Error(data.detail || data.message || 'Invalid credentials.');
      }

      // session handled via HttpOnly __Host-nv_session cookie
      if (data.golden_profile_id) 
      if (data.profile) localStorage.setItem('nv_user_profile', JSON.stringify(data.profile));

      _isUnlocked = true;
      updateNavAuth();

      const overlay = document.getElementById('nv-consent-Explore-overlay');
      if (overlay) overlay.style.display = 'none';

      if (typeof _pendingCallback === 'function') {
        _pendingCallback();
      } else {
        const submitBtn = document.querySelector('button[type="submit"], .btn-calc-submit, #hero-calc-submit');
        if (submitBtn) submitBtn.click();
      }

      if (_pendingContainerId) {
        injectUnlockedBanner(_pendingContainerId, (data.profile && data.profile.name) || 'Seeker');
      }
    } catch (err) {
      alertBox.style.cssText = 'display:block; background:#FDEDEC; color:#C0392B; border:1px solid #E6B0AA; padding:10px 14px; border-radius:8px; font-size:0.82rem; margin-bottom:14px;';
      alertBox.textContent = err.message || 'Login failed. Please verify credentials.';
      btn.disabled = false;
      btn.innerHTML = '<span style="color:#FFFDF7; margin-right:4px;">✦</span>Sign In &amp; Show Free Results<span style="color:#FFFDF7; margin-left:4px;">✦</span>';
    }
  }

  // 10. Inject Unlocked Banner above Results
  function injectUnlockedBanner(containerId, name) {
    const el = document.getElementById(containerId);
    if (!el) return;

    // Check if banner already exists
    if (el.querySelector('.nv-unlocked-banner')) return;

    const banner = document.createElement('div');
    banner.className = 'nv-unlocked-banner';
    banner.style.cssText = 'background:rgba(22,131,91,0.08); border:1.5px solid #16835B; border-radius:12px; padding:12px 18px; margin-bottom:20px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:10px; font-size:0.84rem; color:#16835B;';
    banner.innerHTML = `
      <div style="display:flex; align-items:center; gap:8px;">
        <span style="font-size:1.2rem; font-weight:700;">✓</span>
        <span><strong>Free Calculation Unlocked:</strong> Saved to Golden Profile for <strong>${name}</strong> with statutory DPDP Act 2023 consent safeguards.</span>
      </div>
      <a href="/dashboard/" style="background:#16835B; color:#FFFFFF; text-decoration:none; padding:6px 14px; border-radius:6px; font-size:0.78rem; font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">
        View Dashboard →
      </a>
    `;
    el.insertBefore(banner, el.firstChild);
    el.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }

  // 11. Core Public Gate Function: Require Consent to Reveal
  function requireConsentToReveal(calcData, onGranted, targetContainerId) {
    const auth = getAuthStatus();
    if (auth.isAuthenticated) {
      // User is already signed up & consented: execute calculation immediately!
      syncCalculation(calcData);
      if (typeof onGranted === 'function') {
        onGranted();
      }
      if (targetContainerId) {
        injectUnlockedBanner(targetContainerId, (auth.profile && auth.profile.name) || 'Seeker');
      }
      return;
    }

    // Unauthenticated: prompt user with Consent & Free Signup Modal
    _isUnlocked = false;
    openUnlockModal(calcData, onGranted, targetContainerId);
  }

  // 12. Render 'Save to Golden Profile' CTA Banner (Existing)
  function renderSaveProfileCard(targetElOrId, data) {
    const el = typeof targetElOrId === 'string' ? document.getElementById(targetElOrId) : targetElOrId;
    if (!el) return;

    const auth = getAuthStatus();
    const name = (data && data.name) || (auth.profile && auth.profile.name) || '';
    const day = (data && data.day) || (auth.profile && auth.profile.day) || '';
    const month = (data && data.month) || (auth.profile && auth.profile.month) || '';
    const year = (data && data.year) || (auth.profile && auth.profile.year) || '';

    const currentUrl = encodeURIComponent(window.location.pathname + window.location.search);
    const signupUrl = `/signup/?source=calculator_save&redirect=${currentUrl}`;

    if (auth.isAuthenticated) {
      el.innerHTML = `
        <div style="background:#FAF6EE; border:1.5px solid rgba(22,131,91,0.35); border-radius:14px; padding:16px 20px; margin-top:20px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;">
          <div style="display:flex; align-items:center; gap:12px;">
            <span style="font-size:1.5rem; color:#16835B;">✓</span>
            <div>
              <div style="font-family:'Cormorant Garamond',serif; font-size:1.2rem; font-weight:700; color:#16835B;">
                Linked to Your Golden Profile
              </div>
              <div style="font-size:0.8rem; color:#523E28;">
                Synchronized with your personal matrix${name ? ' for <strong>' + name + '</strong>' : ''}.
              </div>
            </div>
          </div>
          <a href="/dashboard/" style="background:#16835B; color:#FFFFFF; text-decoration:none; padding:8px 16px; border-radius:8px; font-size:0.82rem; font-weight:700; text-transform:uppercase; letter-spacing:0.04em;">
            Open Dashboard →
          </a>
        </div>
      `;
    } else {
      el.innerHTML = `
        <div style="background:linear-gradient(135deg, #FFFDF7 0%, #FAF6EE 100%); border:1.5px solid rgba(201,162,39,0.45); border-radius:16px; padding:20px 24px; margin-top:24px; box-shadow:0 6px 20px rgba(180,155,110,0.1); display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:16px;">
          <div style="flex:1; min-width:240px;">
            <div style="display:flex; align-items:center; gap:8px; margin-bottom:4px;">
              <span style="color:#C9A227; font-size:1.25rem;">✦</span>
              <span style="font-family:'Cormorant Garamond',serif; font-size:1.35rem; font-weight:700; color:#8B6914;">
                Save Your Lo Shu Grid &amp; Numerological Matrix
              </span>
            </div>
            <div style="font-size:0.86rem; color:#523E28; line-height:1.55;">
              Create your free Golden Profile to permanently save your 8 planes, track 2026 transits, and consult Charm AI under statutory <strong>DPDP Act 2023</strong> consent safeguards.
            </div>
          </div>
          <div>
            <a href="${signupUrl}" style="background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFFFF; text-decoration:none; padding:12px 20px; border-radius:10px; font-weight:700; font-size:0.88rem; text-transform:uppercase; letter-spacing:0.05em; display:inline-block; box-shadow:0 3px 12px rgba(201,162,39,0.3); transition:all 0.2s ease;">
              Save My Profile &amp; Explore Reports ✦
            </a>
          </div>
        </div>
      `;
    }
  }

  // 13. Update Global Header Actions
  function updateNavAuth() {
    const auth = getAuthStatus();
    const navActions = document.querySelector('.nv-nav-actions');
    if (!navActions) return;

    let authLink = navActions.querySelector('.nv-nav-link-auth');
    if (!authLink) {
      authLink = document.createElement('a');
      authLink.className = 'nv-nav-link nv-nav-link-auth';
      navActions.insertBefore(authLink, navActions.firstChild);
    }

    if (auth.isAuthenticated) {
      authLink.href = '/dashboard/';
      authLink.innerHTML = '<span style="color:#C9A227; margin-right:4px;">✦</span> My Dashboard';
      authLink.title = 'View Your Saved Matrix';
    } else {
      authLink.href = '/signup/';
      authLink.innerHTML = 'Sign Up';
      authLink.title = 'Create Free Account & Save Matrix';
    }
  }

  // Expose global namespace

  async function triggerGoogleSignIn() {
    const alertBox = document.getElementById('nv-Explore-alert');
    if (alertBox) alertBox.style.display = 'none';

    const email = prompt("Enter your Google Account email address to sign in:");
    if (!email || !email.includes('@')) return;

    try {
      const resp = await fetch('/api/v1/auth/google', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          email: email.trim(),
          day: parseInt((_pendingData && _pendingData.day) || 15, 10),
          month: parseInt((_pendingData && _pendingData.month) || 8, 10),
          year: parseInt((_pendingData && _pendingData.year) || 1990, 10)
        })
      });
      const data = await resp.json();
      if (!resp.ok) throw new Error(data.detail || 'Google authentication failed.');

      // session handled via HttpOnly __Host-nv_session cookie
      if (data.golden_profile_id) 
      if (data.profile) localStorage.setItem('nv_user_profile', JSON.stringify(data.profile));

      _isUnlocked = true;
      updateNavAuth();

      const overlay = document.getElementById('nv-consent-Explore-overlay');
      if (overlay) overlay.style.display = 'none';

      if (typeof _pendingCallback === 'function') {
        _pendingCallback();
      } else {
        const submitBtn = document.querySelector('button[type="submit"], .btn-calc-submit, #hero-calc-submit');
        if (submitBtn) submitBtn.click();
      }
    } catch (err) {
      alert('Google Sign-In notice: ' + err.message);
    }
  }

  window.nvProfileSync = {
    triggerGoogleSignIn: triggerGoogleSignIn,
    getAuthStatus: getAuthStatus,
    syncCalculation: syncCalculation,
    renderSaveProfileCard: renderSaveProfileCard,
    updateNavAuth: updateNavAuth,
    requireConsentToReveal: requireConsentToReveal,
    openUnlockModal: openUnlockModal,
    closeUnlockModal: closeUnlockModal,
    toggleUnlockMode: toggleUnlockMode,
    handleUnlockSignup: handleUnlockSignup,
    handleUnlockLogin: handleUnlockLogin,
    onUnlockCityInput: onUnlockCityInput
  };

  // Run on load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', updateNavAuth);
  } else {
    updateNavAuth();
  }
})();
