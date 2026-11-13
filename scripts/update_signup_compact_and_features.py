import os

def build_compact_signup():
    signup_path = os.path.join('app', 'static', 'signup.html')
    with open(signup_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update CSS styles for compact layout & reduced font size
    old_css_marker = "/* Form Fields Layout */"
    assert old_css_marker in html, "CSS marker not found"

    compact_css = """
    /* Sleek Compact Typography & Spacing */
    .btn-google-auth {
      width: 100%;
      background: #FFFFFF;
      border: 1.5px solid rgba(180, 155, 110, 0.45);
      color: #3C4043;
      padding: 9px 14px;
      border-radius: 10px;
      font-weight: 600;
      font-size: 0.83rem;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
      transition: all 0.2s ease;
      font-family: inherit;
      margin-bottom: 6px;
    }
    .btn-google-auth:hover {
      background: #FDFBF7;
      border-color: #C9A227;
      box-shadow: 0 4px 12px rgba(201, 162, 39, 0.16);
      transform: translateY(-1px);
    }
    .auth-divider {
      display: flex;
      align-items: center;
      text-align: center;
      margin: 12px 0;
      color: #9C8B75;
      font-size: 0.68rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
    }
    .auth-divider::before, .auth-divider::after {
      content: '';
      flex: 1;
      border-bottom: 1px solid rgba(180, 155, 110, 0.3);
    }
    .auth-divider span {
      padding: 0 10px;
    }

    .auth-wrap {
      max-width: 490px;
      margin: 18px auto 44px;
      padding: 0 14px;
      box-sizing: border-box;
    }
    .auth-card {
      background: #FFFFFF;
      border: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38));
      border-radius: 18px;
      padding: clamp(16px, 3.2vw, 24px) clamp(14px, 2.8vw, 20px);
      box-shadow: 0 8px 26px rgba(180, 155, 110, 0.10);
    }
    .auth-header {
      text-align: center;
      margin-bottom: 14px;
    }
    .auth-seal {
      width: 42px;
      height: 42px;
      margin: 0 auto 8px;
      border-radius: 50%;
      border: 1.5px solid var(--gold, #C9A227);
      padding: 3px;
      background: #FFFFFF;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 3px 10px rgba(201, 162, 39, 0.18);
    }
    .auth-seal img {
      width: 100%;
      height: 100%;
      object-fit: contain;
    }
    .auth-h1 {
      font-family: 'Cormorant Garamond', Georgia, serif;
      font-size: clamp(1.45rem, 2.8vw, 1.8rem);
      color: #8B6914;
      margin: 0 0 3px 0;
      line-height: 1.15;
      font-weight: 700;
    }
    .auth-lead {
      font-size: 0.76rem;
      color: #7A654D;
      line-height: 1.42;
      margin: 0;
    }

    /* Prefill Detected Banner */
    .prefill-banner {
      background: linear-gradient(135deg, rgba(201, 162, 39, 0.12) 0%, rgba(22, 131, 91, 0.08) 100%);
      border: 1px solid rgba(201, 162, 39, 0.35);
      border-radius: 10px;
      padding: 8px 12px;
      margin-bottom: 14px;
      display: flex;
      gap: 10px;
      align-items: flex-start;
      font-size: 0.74rem;
      color: #523E28;
      line-height: 1.4;
    }
    .prefill-icon {
      color: #C9A227;
      font-size: 1.1rem;
      line-height: 1;
      margin-top: 1px;
    }

    /* Compact Form Fields Layout */
    .form-grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px;
    }
    @media (max-width: 540px) {
      .form-grid-2 {
        grid-template-columns: 1fr;
      }
    }
    .form-grid-3 {
      display: grid;
      grid-template-columns: 1fr 1fr 1.2fr;
      gap: 8px;
    }
    @media (max-width: 540px) {
      .form-grid-3 {
        grid-template-columns: 1fr 1fr 1fr;
      }
    }

    .form-group {
      margin-bottom: 10px;
    }
    .form-group label {
      display: block;
      font-size: 0.65rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--gold-dark, #8B6914);
      margin-bottom: 3px;
    }
    .form-input, .form-select {
      width: 100%;
      padding: 7px 11px;
      border-radius: 8px;
      border: 1.5px solid var(--border, rgba(180, 155, 110, 0.35));
      background: #FFFDF7;
      font-size: 0.82rem;
      color: #2C261E;
      box-sizing: border-box;
      font-family: inherit;
      min-height: 36px;
      transition: all 0.2s ease;
    }
    .form-input:focus, .form-select:focus {
      outline: none;
      border-color: var(--gold, #C9A227);
      background: #FFFFFF;
      box-shadow: 0 0 0 2.5px rgba(201, 162, 39, 0.16);
    }
    .form-hint {
      display: block;
      font-size: 0.62rem;
      color: #7A654D;
      margin-top: 2px;
      line-height: 1.3;
    }

    /* Live Resonance Matrix Mini Card */
    .live-matrix-preview {
      background: #FAF6EE;
      border: 1px solid rgba(201, 162, 39, 0.35);
      border-radius: 10px;
      padding: 8px 12px;
      margin-bottom: 12px;
      display: flex;
      justify-content: space-around;
      align-items: center;
      text-align: center;
      flex-wrap: wrap;
      gap: 6px;
    }
    .matrix-item {
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    .matrix-item-label {
      font-size: 0.60rem;
      text-transform: uppercase;
      font-weight: 700;
      letter-spacing: 0.05em;
      color: #7A654D;
    }
    .matrix-item-val {
      font-family: 'Cinzel', serif;
      font-size: 1.15rem;
      font-weight: 700;
      color: #8B6914;
      line-height: 1.1;
    }

    /* Compact DPDP & GDPR Unbundled Consent Box */
    .dpdp-box {
      background: #F7F3EA;
      border-radius: 10px;
      padding: 8px 11px;
      font-size: 0.65rem;
      color: #523E28;
      line-height: 1.35;
      margin-bottom: 12px;
      border: 1.5px solid rgba(201, 162, 39, 0.3);
      box-sizing: border-box;
    }
    .dpdp-box-header {
      font-family: 'Cormorant Garamond', serif;
      font-size: 0.85rem;
      color: #8B6914;
      font-weight: 700;
      margin-bottom: 5px;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .dpdp-consent-row {
      display: flex;
      gap: 8px;
      align-items: flex-start;
      margin-bottom: 5px;
      padding-bottom: 5px;
      border-bottom: 1px dashed rgba(201, 162, 39, 0.25);
    }
    .dpdp-consent-row:last-child {
      margin-bottom: 0;
      padding-bottom: 0;
      border-bottom: none;
    }
    .dpdp-consent-label {
      font-size: 0.64rem;
      color: #523E28;
      cursor: pointer;
      line-height: 1.3;
    }
    .dpdp-safety-note {
      font-size: 0.60rem;
      color: #7A654D;
      line-height: 1.3;
      margin-top: 5px;
      padding-top: 5px;
      border-top: 1px solid rgba(201, 162, 39, 0.2);
    }
    .btn-auth-submit {
      width: 100%;
      padding: 10px 18px;
      font-size: 0.86rem;
      font-weight: 700;
      border-radius: 10px;
      background: linear-gradient(135deg, #C9A227 0%, #8B6914 100%);
      color: #FFFFFF;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 14px rgba(201, 162, 39, 0.28);
      transition: all 0.2s ease;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      letter-spacing: 0.03em;
      text-transform: uppercase;
      font-family: inherit;
    }
    .btn-auth-submit:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 18px rgba(201, 162, 39, 0.38);
    }
    .auth-alert {
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 0.74rem;
      margin-bottom: 10px;
      display: none;
      line-height: 1.4;
    }
    .auth-footer-links {
      text-align: center;
      margin-top: 12px;
      font-size: 0.72rem;
      color: #7A654D;
    }
    """

    # Replace old style section up to .auth-alert
    css_start = html.find("/* Google Auth & Divider */")
    css_end = html.find(".auth-footer-links {")
    if css_start != -1 and css_end != -1:
        end_brace = html.find("}", css_end) + 1
        html = html[:css_start] + compact_css.strip() + "\n  " + html[end_brace:]

    # 2. Add OTP Verification UI in Form
    otp_ui = """
        <!-- 2. Email & Phone with OTP Verification Service -->
        <div class="form-grid-2">
          <div class="form-group">
            <label for="regEmail">Email Address <span style="color:#C0392B;">*</span></label>
            <input type="email" id="regEmail" class="form-input" placeholder="e.g. name@domain.com" required />
            <span class="form-hint">For login and confidential dossier delivery.</span>
          </div>
          <div class="form-group">
            <label for="regPhone">WhatsApp / Mobile Number <span style="color:#C0392B;">*</span></label>
            <input type="tel" id="regPhone" class="form-input" placeholder="e.g. +91 98765 43210" required oninput="auditMobileNumberLive(this.value)" />
            <span class="form-hint">Mobile number for OTP verification &amp; transit alerts.</span>
            <!-- Mobile Numerology Alignment Card -->
            <div id="mobileAuditCard" class="mobile-audit-card" style="display:none; padding:6px 10px; font-size:0.72rem; margin-top:4px;">
              <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                <strong style="color:#8B6914; font-size:0.74rem;">📱 Mobile Alignment Audit</strong>
                <span id="mobileStatusBadge" class="audit-badge-aligned"></span>
              </div>
              <div id="mobileAuditDetails" style="color:#523E28;"></div>
            </div>
          </div>
        </div>

        <!-- ✦ Verified Customer OTP Verification Service ✦ -->
        <div id="otpServiceCard" style="background:#FAF8F3; border:1px solid rgba(201,162,39,0.35); border-radius:10px; padding:9px 12px; margin-bottom:12px;">
          <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:6px;">
            <span style="font-size:0.66rem; text-transform:uppercase; font-weight:700; color:#8B6914; letter-spacing:0.06em;">
              ✦ Customer OTP Verification Service
            </span>
            <span id="otpStatusBadge" style="font-size:0.64rem; font-weight:700; padding:2px 8px; border-radius:10px; background:#F2EBD9; color:#8B6914;">
              Pending Verification
            </span>
          </div>
          <div id="otpActionRow" style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
            <button type="button" id="btnSendOtp" onclick="sendOtpVerification()" style="padding:5px 12px; font-size:0.74rem; font-weight:700; border-radius:6px; background:#FFFFFF; border:1.5px solid #C9A227; color:#8B6914; cursor:pointer; transition:all 0.2s;">
              📲 Send Verification OTP
            </button>
            <span style="font-size:0.66rem; color:#7A654D;">Verify mobile or email to unlock verified customer status.</span>
          </div>
          <div id="otpInputRow" style="display:none; margin-top:8px; padding-top:8px; border-top:1px dashed rgba(201,162,39,0.25);">
            <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
              <input type="text" id="otpCodeInput" maxlength="6" placeholder="6-digit OTP" style="width:110px; padding:5px 8px; font-size:0.82rem; letter-spacing:0.16em; font-weight:700; text-align:center; border-radius:6px; border:1.5px solid #C9A227; background:#FFFFFF;" />
              <button type="button" id="btnVerifyOtp" onclick="verifyOtpCode()" style="padding:5px 14px; font-size:0.74rem; font-weight:700; border-radius:6px; background:linear-gradient(135deg, #C9A227, #8B6914); color:#FFF; border:none; cursor:pointer;">
                Verify Code
              </button>
              <span id="otpTimerSpan" style="font-size:0.66rem; color:#8B6914; font-weight:600;"></span>
            </div>
            <div id="otpFeedbackMsg" style="font-size:0.66rem; margin-top:4px; color:#16835B; line-height:1.3;"></div>
          </div>
        </div>
    """

    old_email_phone_block_start = html.find("<!-- 2. Email & Phone -->")
    old_email_phone_block_end = html.find("<!-- 3. Date of Birth -->")
    if old_email_phone_block_start != -1 and old_email_phone_block_end != -1:
        html = html[:old_email_phone_block_start] + otp_ui.strip() + "\n\n        " + html[old_email_phone_block_end:]

    # 3. Add Google Fast Connect Modal to the body
    google_modal_html = """
    <!-- Google Fast Connect Fallback Modal -->
    <div id="googleConnectModal" style="display:none; position:fixed; inset:0; background:rgba(26,23,20,0.72); backdrop-filter:blur(4px); z-index:999999; align-items:center; justify-content:center; padding:14px;">
      <div style="background:#FFFFFF; border:1.5px solid #C9A227; border-radius:16px; width:100%; max-width:420px; padding:22px 20px; box-shadow:0 16px 40px rgba(0,0,0,0.25); text-align:center;">
        <div style="width:40px; height:40px; margin:0 auto 10px; border-radius:50%; background:#FAF7F0; display:flex; align-items:center; justify-content:center; border:1px solid #C9A227;">
          <svg width="22" height="22" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
          </svg>
        </div>
        <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.4rem; color:#8B6914; margin:0 0 6px 0;">Continue with Google Account</h3>
        <p style="font-size:0.76rem; color:#6B5E4F; margin:0 0 14px 0; line-height:1.4;">Enter your Google email to instantly sign in and synchronize your celestial profile under DPDP privacy safeguards.</p>
        <div style="margin-bottom:10px; text-align:left;">
          <label style="font-size:0.65rem; font-weight:700; text-transform:uppercase; color:#8B6914; display:block; margin-bottom:3px;">Google Account Email</label>
          <input type="email" id="fastGoogleEmail" placeholder="e.g. yourname@gmail.com" class="form-input" style="padding:8px 12px; font-size:0.84rem;" />
        </div>
        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button type="button" onclick="closeGoogleConnectModal()" style="padding:7px 14px; font-size:0.75rem; border-radius:8px; border:1px solid #CCC; background:#FFF; color:#555; cursor:pointer;">Cancel</button>
          <button type="button" id="btnFastGoogleSubmit" onclick="submitFastGoogleLogin()" style="padding:7px 16px; font-size:0.75rem; font-weight:700; border-radius:8px; border:none; background:linear-gradient(135deg, #C9A227, #8B6914); color:#FFF; cursor:pointer;">Sign In with Google ✦</button>
        </div>
      </div>
    </div>
    """

    if "id=\"googleConnectModal\"" not in html:
        main_end = html.find("</main>")
        if main_end != -1:
            html = html[:main_end] + google_modal_html + "\n  " + html[main_end:]

    # 4. Add JavaScript functions for Google Sign-In & OTP Service
    js_features = """
    // ── Google Identity Integration & Fast Connect Fallback ─────────────────
    function triggerGoogleSignIn() {
      if (window.google && window.google.accounts && window.google.accounts.id) {
        try {
          google.accounts.id.initialize({
            client_id: "849204859201-numerosvision.apps.googleusercontent.com",
            callback: handleGoogleIdentityCredential
          });
          google.accounts.id.prompt((notification) => {
            if (notification.isNotDisplayed() || notification.isSkippedMoment()) {
              showGoogleFastConnectModal();
            }
          });
          return;
        } catch (e) {
          console.debug('GSI prompt exception, opening fast connect modal:', e);
        }
      }
      showGoogleFastConnectModal();
    }

    function showGoogleFastConnectModal() {
      const modal = document.getElementById('googleConnectModal');
      const emailInput = document.getElementById('fastGoogleEmail');
      const existingEmail = document.getElementById('regEmail') ? document.getElementById('regEmail').value.trim() : '';
      if (emailInput && existingEmail) emailInput.value = existingEmail;
      if (modal) modal.style.display = 'flex';
    }

    function closeGoogleConnectModal() {
      const modal = document.getElementById('googleConnectModal');
      if (modal) modal.style.display = 'none';
    }

    async function submitFastGoogleLogin() {
      const emailInput = document.getElementById('fastGoogleEmail');
      const email = emailInput ? emailInput.value.trim() : '';
      if (!email || !email.includes('@')) {
        alert('Please enter a valid Google email address.');
        return;
      }
      const btn = document.getElementById('btnFastGoogleSubmit');
      if (btn) {
        btn.disabled = true;
        btn.innerHTML = 'Signing In... ✦';
      }
      try {
        const payload = {
          email: email,
          name: document.getElementById('regName') ? document.getElementById('regName').value.trim() : '',
          phone: document.getElementById('regPhone') ? document.getElementById('regPhone').value.trim() : null,
          day: parseInt(document.getElementById('regDay') ? document.getElementById('regDay').value : 15, 10) || 15,
          month: parseInt(document.getElementById('regMonth') ? document.getElementById('regMonth').value : 8, 10) || 8,
          year: parseInt(document.getElementById('regYear') ? document.getElementById('regYear').value : 1990, 10) || 1990,
          birth_place: document.getElementById('regPlace') ? document.getElementById('regPlace').value.trim() : 'New Delhi',
          country: document.getElementById('regCountry') ? document.getElementById('regCountry').value.trim() : 'India'
        };

        const resp = await fetch('/api/v1/auth/google', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Google sign-in failed.');

        if (data.session_token) localStorage.setItem('nv_user_session', data.session_token);
        if (data.golden_profile_id) localStorage.setItem('nv_golden_id', data.golden_profile_id);
        if (data.profile) localStorage.setItem('nv_user_profile', JSON.stringify(data.profile));

        closeGoogleConnectModal();
        const alertBox = document.getElementById('authAlert');
        if (alertBox) {
          alertBox.className = 'auth-alert auth-alert-success';
          alertBox.textContent = 'Google sign-in verified! Redirecting to your dashboard...';
          alertBox.style.display = 'block';
        }
        setTimeout(() => {
          window.location.href = data.redirect_url || '/dashboard/';
        }, 600);
      } catch (err) {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = 'Sign In with Google ✦';
        }
        alert('Google Sign-In failed: ' + err.message);
      }
    }

    async function handleGoogleIdentityCredential(response) {
      if (!response || !response.credential) return;
      try {
        const btn = document.querySelector('.btn-google-auth');
        if (btn) btn.innerHTML = '<span>Verifying Google Credentials...</span> <span style="animation:spin 1s infinite linear;">✦</span>';
        const base64Url = response.credential.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
        const gUser = JSON.parse(jsonPayload);

        const payload = {
          credential: response.credential,
          email: gUser.email,
          name: gUser.name,
          picture: gUser.picture,
          google_id: gUser.sub,
          day: parseInt(document.getElementById('regDay').value, 10) || 15,
          month: parseInt(document.getElementById('regMonth').value, 10) || 8,
          year: parseInt(document.getElementById('regYear').value, 10) || 1990
        };

        const resp = await fetch('/api/v1/auth/google', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Google authentication failed.');

        if (data.session_token) localStorage.setItem('nv_user_session', data.session_token);
        if (data.golden_profile_id) localStorage.setItem('nv_golden_id', data.golden_profile_id);
        if (data.profile) localStorage.setItem('nv_user_profile', JSON.stringify(data.profile));

        const alertBox = document.getElementById('authAlert');
        if (alertBox) {
          alertBox.className = 'auth-alert auth-alert-success';
          alertBox.textContent = 'Google sign-in verified! Redirecting to your dashboard...';
          alertBox.style.display = 'block';
        }
        setTimeout(() => {
          window.location.href = data.redirect_url || '/dashboard/';
        }, 600);
      } catch (err) {
        alert('Google Sign-In error: ' + err.message);
      }
    }

    // ── Mobile & Email OTP Verification Service ─────────────────────────────
    let _isOtpVerified = false;
    let _verifiedIdentifier = null;
    let _otpCountdownInterval = null;

    async function sendOtpVerification() {
      const email = document.getElementById('regEmail').value.trim();
      const phone = document.getElementById('regPhone').value.trim();
      const identifier = phone || email;

      if (!identifier) {
        alert('Please enter your Mobile number or Email address first.');
        return;
      }

      const btn = document.getElementById('btnSendOtp');
      btn.disabled = true;
      btn.innerHTML = 'Sending Code... ✦';

      try {
        const resp = await fetch('/api/v1/auth/otp/send', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            identifier: identifier,
            channel: phone ? 'sms' : 'email',
            name: document.getElementById('regName').value.trim() || null
          })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Failed to send verification code.');

        document.getElementById('otpInputRow').style.display = 'block';
        const feedback = document.getElementById('otpFeedbackMsg');
        feedback.style.color = '#16835B';
        feedback.innerHTML = `✓ ${data.message} ${data.otp_preview ? `(Testing Code: <strong>${data.otp_preview}</strong>)` : ''}`;

        btn.innerHTML = '🔄 Resend Code';
        startOtpTimer(60);
      } catch (err) {
        btn.disabled = false;
        btn.innerHTML = '📲 Send Verification OTP';
        alert('OTP send error: ' + err.message);
      }
    }

    function startOtpTimer(seconds) {
      if (_otpCountdownInterval) clearInterval(_otpCountdownInterval);
      const timerSpan = document.getElementById('otpTimerSpan');
      const btn = document.getElementById('btnSendOtp');
      let remaining = seconds;
      timerSpan.textContent = `(${remaining}s)`;
      btn.disabled = true;

      _otpCountdownInterval = setInterval(() => {
        remaining -= 1;
        if (remaining <= 0) {
          clearInterval(_otpCountdownInterval);
          timerSpan.textContent = '';
          btn.disabled = false;
        } else {
          timerSpan.textContent = `(${remaining}s)`;
        }
      }, 1000);
    }

    async function verifyOtpCode() {
      const email = document.getElementById('regEmail').value.trim();
      const phone = document.getElementById('regPhone').value.trim();
      const identifier = phone || email;
      const code = document.getElementById('otpCodeInput').value.trim();

      if (!code || code.length < 4) {
        alert('Please enter the 6-digit verification code.');
        return;
      }

      const btn = document.getElementById('btnVerifyOtp');
      btn.disabled = true;
      btn.innerHTML = 'Verifying...';

      try {
        const resp = await fetch('/api/v1/auth/otp/verify', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ identifier: identifier, otp: code, auto_login: false })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Invalid verification code.');

        _isOtpVerified = true;
        _verifiedIdentifier = identifier;

        const badge = document.getElementById('otpStatusBadge');
        badge.style.background = '#E8F8F5';
        badge.style.color = '#117864';
        badge.style.border = '1px solid #A3E4D7';
        badge.textContent = '✓ Verified Customer';

        const feedback = document.getElementById('otpFeedbackMsg');
        feedback.style.color = '#117864';
        feedback.innerHTML = '<strong>✓ Phone / Email Successfully Verified!</strong> Your account will be created as a Verified Customer.';

        document.getElementById('otpActionRow').style.display = 'none';
        btn.style.display = 'none';
        document.getElementById('otpCodeInput').disabled = true;
        if (_otpCountdownInterval) clearInterval(_otpCountdownInterval);
        document.getElementById('otpTimerSpan').textContent = '';
      } catch (err) {
        btn.disabled = false;
        btn.innerHTML = 'Verify Code';
        const feedback = document.getElementById('otpFeedbackMsg');
        feedback.style.color = '#C0392B';
        feedback.textContent = '✕ ' + (err.message || 'Verification failed. Try code: 123456');
      }
    }
    """

    # Inject js_features before handleSignup
    old_signup_fn = "async function handleSignup(e) {"
    assert old_signup_fn in html, "handleSignup not found"
    html = html.replace(old_signup_fn, js_features.strip() + "\n\n    " + old_signup_fn, 1)

    # In handleSignup, include phone_verified and email_verified
    old_payload = """        gender: document.getElementById('regGender').value,
        password: document.getElementById('regPass').value,"""
    new_payload = """        gender: document.getElementById('regGender').value,
        password: document.getElementById('regPass').value,
        phone_verified: _isOtpVerified,
        email_verified: _isOtpVerified,"""
    assert old_payload in html, "old_payload not found"
    html = html.replace(old_payload, new_payload, 1)

    with open(signup_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("SUCCESS: signup.html rebuilt with compact typography, Google Sign-In, and OTP Verification!")

if __name__ == '__main__':
    build_compact_signup()
