import re

def update_sync_js():
    path = 'app/static/js/nv_profile_sync.js'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find start and end of ensureUnlockModal
    idx1 = content.find('function ensureUnlockModal()')
    idx2 = content.find('  // 4. Toggle between Signup and Login')
    if idx1 == -1 or idx2 == -1:
        print("ERROR: could not locate ensureUnlockModal in nv_profile_sync.js")
        return

    new_ensure_code = """function ensureUnlockModal() {
    if (document.getElementById('nv-consent-unlock-overlay')) return;

    if (!document.getElementById('nv-unlock-modal-styles')) {
      const styleEl = document.createElement('style');
      styleEl.id = 'nv-unlock-modal-styles';
      styleEl.textContent = `
        #nv-consent-unlock-overlay {
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
        #nv-consent-unlock-card,
        #nv-consent-unlock-card * {
          box-sizing: border-box !important;
        }
        #nv-consent-unlock-card {
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
        #nv-consent-unlock-card::-webkit-scrollbar {
          width: 5px !important;
        }
        #nv-consent-unlock-card::-webkit-scrollbar-track {
          background: #FAF6EE !important;
          border-radius: 4px !important;
        }
        #nv-consent-unlock-card::-webkit-scrollbar-thumb {
          background: #C9A227 !important;
          border-radius: 4px !important;
        }
        #nv-consent-unlock-card label {
          text-transform: none !important;
          letter-spacing: normal !important;
          font-weight: 400 !important;
          margin-bottom: 0 !important;
        }
        #nv-consent-unlock-card .nv-form-label {
          display: block !important;
          font-size: 0.72rem !important;
          font-weight: 700 !important;
          color: #523E28 !important;
          text-transform: uppercase !important;
          letter-spacing: 0.04em !important;
          margin-bottom: 4px !important;
        }
        #nv-consent-unlock-card input[type="text"],
        #nv-consent-unlock-card input[type="email"],
        #nv-consent-unlock-card input[type="tel"],
        #nv-consent-unlock-card input[type="password"],
        #nv-consent-unlock-card input[type="number"],
        #nv-consent-unlock-card select {
          width: 100% !important;
          padding: 8px 10px !important;
          border: 1px solid #D6C7B2 !important;
          border-radius: 8px !important;
          font-size: 0.85rem !important;
          background: #FFFFFF !important;
          color: #2C261E !important;
          font-family: inherit !important;
          transition: border-color 0.2s ease !important;
        }
        #nv-consent-unlock-card input:focus,
        #nv-consent-unlock-card select:focus {
          border-color: #C9A227 !important;
          outline: none !important;
        }
        #nv-consent-unlock-card .nv-consent-card {
          background: rgba(201,162,39,0.07) !important;
          border: 1px solid rgba(201,162,39,0.32) !important;
          border-radius: 10px !important;
          padding: 10px 12px !important;
          margin-bottom: 14px !important;
        }
        #nv-consent-unlock-card .nv-consent-row {
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
        #nv-consent-unlock-card .nv-consent-row:last-child {
          margin-bottom: 0 !important;
        }
        #nv-consent-unlock-card .nv-consent-row input[type="checkbox"] {
          width: 15px !important;
          height: 15px !important;
          margin-top: 2px !important;
          flex-shrink: 0 !important;
          accent-color: #8B6914 !important;
          cursor: pointer !important;
        }
        #nv-consent-unlock-card .nv-consent-row span {
          font-size: 0.72rem !important;
          line-height: 1.4 !important;
          text-transform: none !important;
          letter-spacing: normal !important;
          font-weight: 400 !important;
          color: #523E28 !important;
          flex: 1 !important;
        }
        #nv-consent-unlock-card .nv-consent-row strong {
          font-weight: 700 !important;
          color: #8B6914 !important;
        }
      `;
      document.head.appendChild(styleEl);
    }

    const overlay = document.createElement('div');
    overlay.id = 'nv-consent-unlock-overlay';

    overlay.innerHTML = `
      <div id="nv-consent-unlock-card">
        <button onclick="window.nvProfileSync.closeUnlockModal()" type="button" style="position:absolute; top:12px; right:14px; background:none; border:none; font-size:1.4rem; color:#8B6914; cursor:pointer; line-height:1;" aria-label="Close">✕</button>

        <!-- Brand Header -->
        <div style="text-align:center; margin-bottom:14px;">
          <img src="/logos/nv-logo-mark.svg" alt="Numeros Vision" style="width:34px; height:34px; margin:0 auto 6px; display:block; filter:drop-shadow(0 2px 6px rgba(201,162,39,0.35));" />
          <div style="font-family:'Cinzel',serif; font-size:0.7rem; letter-spacing:0.12em; color:#8B6914; font-weight:700;">NUMEROS VISION · ANVEIL EVERY CHARM</div>
          <h3 id="nv-modal-heading" style="font-family:'Cormorant Garamond',serif; font-size:1.6rem; color:#1A1714; margin:4px 0 3px; font-weight:700;">
            ✦ Unlock Your Free Calculation ✦
          </h3>
          <p id="nv-modal-sub" style="font-size:0.8rem; color:#6B5E4F; margin:0; line-height:1.45;">
            Create your free profile with DPDP statutory consent to reveal your results and save your personal chart.
          </p>
        </div>

        <!-- Live Calculation Chip Preview -->
        <div id="nv-calc-preview-chip" style="background:#FAF6EE; border:1px solid #C9A227; border-radius:10px; padding:7px 12px; margin-bottom:14px; font-size:0.78rem; color:#523E28; display:flex; align-items:center; justify-content:space-between; gap:8px;">
          <span id="nv-preview-chip-dob">📅 Date of Birth: 15-08-1990</span>
          <span style="color:#16835B; font-weight:700; font-size:0.72rem; text-transform:uppercase;">✓ Calculated</span>
        </div>

        <!-- Alert Box -->
        <div id="nv-unlock-alert" style="display:none; padding:9px 12px; border-radius:8px; font-size:0.8rem; margin-bottom:12px; line-height:1.4;"></div>

        <!-- SIGNUP FORM (Default) -->
        <form id="nv-unlock-signup-form" onsubmit="window.nvProfileSync.handleUnlockSignup(event)">
          <div style="margin-bottom:10px;">
            <label class="nv-form-label">Full Calling Name *</label>
            <input type="text" id="nv-unlock-name" required placeholder="Enter your full name" />
          </div>

          <div style="margin-bottom:10px;">
            <label class="nv-form-label">Email Address *</label>
            <input type="email" id="nv-unlock-email" required placeholder="name@example.com" />
          </div>

          <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:10px;">
            <div>
              <label class="nv-form-label">WhatsApp / Mobile</label>
              <input type="tel" id="nv-unlock-phone" placeholder="+91 98765 43210" />
            </div>
            <div>
              <label class="nv-form-label">Password *</label>
              <input type="password" id="nv-unlock-password" required minlength="6" placeholder="Min 6 characters" />
            </div>
          </div>

          <!-- Time of Birth (AM/PM) -->
          <div style="margin-bottom:10px;">
            <label class="nv-form-label">Time of Birth (Hour, Minute, AM/PM)</label>
            <div style="display:grid; grid-template-columns:1fr 1fr 1.2fr; gap:8px;">
              <select id="nv-unlock-time-hour">
                <option value="">Hour</option>
                <option value="1">01</option><option value="2">02</option>
                <option value="3">03</option><option value="4">04</option>
                <option value="5">05</option><option value="6">06</option>
                <option value="7">07</option><option value="8">08</option>
                <option value="9">09</option><option value="10">10</option>
                <option value="11">11</option><option value="12" selected>12</option>
              </select>
              <select id="nv-unlock-time-minute">
                <option value="0">00</option><option value="5">05</option>
                <option value="10">10</option><option value="15">15</option>
                <option value="20">20</option><option value="25">25</option>
                <option value="30" selected>30</option><option value="35">35</option>
                <option value="40">40</option><option value="45">45</option>
                <option value="50">50</option><option value="55">55</option>
              </select>
              <select id="nv-unlock-time-period">
                <option value="AM">AM</option>
                <option value="PM" selected>PM</option>
              </select>
            </div>
            <span style="font-size:0.68rem; color:#7A654D; display:block; margin-top:2px;">Enables precise planetary ascendant &amp; KP sub-lord cusps.</span>
          </div>

          <!-- Place of Birth & Country -->
          <div style="display:grid; grid-template-columns:1.2fr 1fr; gap:10px; margin-bottom:10px;">
            <div>
              <label class="nv-form-label">Place of Birth *</label>
              <input type="text" id="nv-unlock-place" required placeholder="City / Town" oninput="window.nvProfileSync.onUnlockCityInput(this.value)" />
            </div>
            <div>
              <label class="nv-form-label">Country *</label>
              <input type="text" id="nv-unlock-country" required value="India" placeholder="Country" />
            </div>
          </div>

          <!-- Coordinates & Timezone Card -->
          <div style="background:#FAF6EE; border:1px solid rgba(201,162,39,0.3); border-radius:10px; padding:8px 10px; margin-bottom:12px;">
            <div style="font-size:0.68rem; text-transform:uppercase; font-weight:700; color:#8B6914; letter-spacing:0.05em; margin-bottom:5px; display:flex; justify-content:space-between; align-items:center;">
              <span>✦ Coordinates &amp; Timezone</span>
              <span id="nv-unlock-coord-badge" style="font-size:0.65rem; color:#16835B; font-weight:600; text-transform:none;">Auto-resolved</span>
            </div>
            <div style="display:grid; grid-template-columns:1fr 1fr 1.4fr; gap:6px;">
              <div>
                <label style="display:block; font-size:0.63rem; font-weight:700; color:#7A654D; text-transform:uppercase; margin-bottom:2px;">Latitude</label>
                <input type="number" step="0.0001" id="nv-unlock-latitude" value="28.6139" placeholder="28.6139" style="padding:6px 7px !important; font-size:0.78rem !important;" />
              </div>
              <div>
                <label style="display:block; font-size:0.63rem; font-weight:700; color:#7A654D; text-transform:uppercase; margin-bottom:2px;">Longitude</label>
                <input type="number" step="0.0001" id="nv-unlock-longitude" value="77.2090" placeholder="77.2090" style="padding:6px 7px !important; font-size:0.78rem !important;" />
              </div>
              <div>
                <label style="display:block; font-size:0.63rem; font-weight:700; color:#7A654D; text-transform:uppercase; margin-bottom:2px;">Timezone</label>
                <select id="nv-unlock-timezone" style="padding:6px 5px !important; font-size:0.75rem !important;">
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
              <input type="checkbox" id="nv-unlock-consent-storage" required checked />
              <span><strong>Statutory DPDP Consent (Required):</strong> I explicitly consent to Numeros Vision computing and storing my birth matrix under the Digital Personal Data Protection (DPDP) Act 2023.</span>
            </label>
            <label class="nv-consent-row">
              <input type="checkbox" id="nv-unlock-consent-marketing" checked />
              <span>Send personal milestone transit alerts via WhatsApp/Email.</span>
            </label>
          </div>

          <button type="submit" id="nv-unlock-submit-btn" style="width:100%; padding:11px; border-radius:10px; background:linear-gradient(135deg, #C9A227 0%, #8B6914 100%); color:#FFFFFF; border:none; font-weight:700; font-size:0.88rem; text-transform:uppercase; letter-spacing:0.04em; cursor:pointer; box-shadow:0 4px 14px rgba(201,162,39,0.35);">
            ✦ Consent &amp; Show Free Results ✦
          </button>

          <div style="text-align:center; margin-top:12px; font-size:0.78rem; color:#6B5E4F;">
            Already have an account? <a href="#" onclick="window.nvProfileSync.toggleUnlockMode('login'); return false;" style="color:#8B6914; font-weight:700; text-decoration:none;">Sign In to Reveal</a>
          </div>
        </form>

        <!-- LOGIN FORM (Hidden by default) -->
        <form id="nv-unlock-login-form" style="display:none;" onsubmit="window.nvProfileSync.handleUnlockLogin(event)">
          <div style="margin-bottom:12px;">
            <label class="nv-form-label">Email or Mobile *</label>
            <input type="text" id="nv-login-id" required placeholder="Enter your email or phone" />
          </div>

          <div style="margin-bottom:14px;">
            <label class="nv-form-label">Password *</label>
            <input type="password" id="nv-login-password" required placeholder="Your password" />
          </div>

          <button type="submit" id="nv-login-submit-btn" style="width:100%; padding:11px; border-radius:10px; background:linear-gradient(135deg, #16835B 0%, #0E5A3E 100%); color:#FFFFFF; border:none; font-weight:700; font-size:0.88rem; text-transform:uppercase; letter-spacing:0.04em; cursor:pointer; box-shadow:0 4px 14px rgba(22,131,91,0.3);">
            ✦ Sign In &amp; Show Free Results ✦
          </button>

          <div style="text-align:center; margin-top:12px; font-size:0.78rem; color:#6B5E4F;">
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

"""

    content = content[:idx1] + new_ensure_code + content[idx2:]
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: nv_profile_sync.js updated cleanly.")

if __name__ == '__main__':
    update_sync_js()
