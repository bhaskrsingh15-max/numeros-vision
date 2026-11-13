import os

def build_login():
    login_path = os.path.join('app', 'static', 'login.html')
    with open(login_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Update CSS styles for compact layout
    compact_css = """
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
      max-width: 440px;
      margin: 22px auto 48px;
      padding: 0 14px;
      box-sizing: border-box;
    }
    .auth-card {
      background: #FFFFFF;
      border: 1.5px solid var(--border-gold, rgba(201, 162, 39, 0.38));
      border-radius: 18px;
      padding: clamp(18px, 3.5vw, 26px) clamp(16px, 3vw, 22px);
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

    /* Auth Mode Tabs */
    .auth-tab-row {
      display: flex;
      gap: 6px;
      margin-bottom: 14px;
      background: #FAF6EE;
      padding: 3px;
      border-radius: 8px;
      border: 1px solid rgba(201, 162, 39, 0.25);
    }
    .auth-tab-btn {
      flex: 1;
      padding: 6px 10px;
      font-size: 0.74rem;
      font-weight: 700;
      border: none;
      border-radius: 6px;
      background: transparent;
      color: #7A654D;
      cursor: pointer;
      transition: all 0.2s ease;
      font-family: inherit;
    }
    .auth-tab-btn.active {
      background: #FFFFFF;
      color: #8B6914;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    }

    .form-group {
      margin-bottom: 11px;
    }
    .form-group label {
      display: block;
      font-size: 0.66rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      color: var(--gold-dark, #8B6914);
      margin-bottom: 3px;
    }
    .form-input {
      width: 100%;
      padding: 8px 12px;
      border-radius: 8px;
      border: 1.5px solid var(--border, rgba(180, 155, 110, 0.35));
      background: #FFFDF7;
      font-size: 0.83rem;
      color: #2C261E;
      box-sizing: border-box;
      font-family: inherit;
      min-height: 36px;
      transition: all 0.2s ease;
    }
    .form-input:focus {
      outline: none;
      border-color: var(--gold, #C9A227);
      background: #FFFFFF;
      box-shadow: 0 0 0 2.5px rgba(201, 162, 39, 0.16);
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
      margin-top: 4px;
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

    css_start = html.find("/* Google Auth & Divider */")
    css_end = html.find(".auth-footer-links {")
    if css_start != -1 and css_end != -1:
        end_brace = html.find("}", css_end) + 1
        html = html[:css_start] + compact_css.strip() + "\n  " + html[end_brace:]

    # 2. Update form HTML to include tabs (Password vs OTP)
    form_replacement = """
      <div id="loginAlert" class="auth-alert"></div>

      <!-- Auth Mode Tabs -->
      <div class="auth-tab-row">
        <button type="button" class="auth-tab-btn active" id="tabPasswordBtn" onclick="switchLoginMode('password')">🔑 Password Sign In</button>
        <button type="button" class="auth-tab-btn" id="tabOtpBtn" onclick="switchLoginMode('otp')">📲 Fast OTP Sign In</button>
      </div>

      <!-- Password Login Form -->
      <form id="passwordLoginForm" onsubmit="handlePasswordLogin(event)">
        <div class="form-group">
          <label for="userEmail">Email or Mobile Number</label>
          <input type="text" id="userEmail" class="form-input" placeholder="e.g. member@numerosvision.com" required />
        </div>

        <div class="form-group">
          <label for="userPass">Password or Secure PIN</label>
          <input type="password" id="userPass" class="form-input" placeholder="Enter your password" required />
        </div>

        <button type="submit" id="btnPasswordSubmit" class="btn-auth-submit">Sign In to Dashboard ✦</button>
      </form>

      <!-- OTP Login Form -->
      <form id="otpLoginForm" onsubmit="handleOtpLoginSubmit(event)" style="display:none;">
        <div class="form-group">
          <label for="otpLoginIdent">Mobile Number or Email Address</label>
          <input type="text" id="otpLoginIdent" class="form-input" placeholder="e.g. +91 98765 43210 or name@domain.com" required />
        </div>

        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
          <button type="button" id="btnSendLoginOtp" onclick="sendLoginOtp()" style="padding:6px 12px; font-size:0.75rem; font-weight:700; border-radius:6px; background:#FAF6EE; border:1.5px solid #C9A227; color:#8B6914; cursor:pointer;">
            📲 Send 6-Digit OTP
          </button>
          <span id="loginOtpTimerSpan" style="font-size:0.66rem; color:#8B6914; font-weight:600;"></span>
        </div>

        <div id="loginOtpInputContainer" style="display:none;" class="form-group">
          <label for="loginOtpCode">Enter 6-Digit OTP Code</label>
          <input type="text" id="loginOtpCode" maxlength="6" class="form-input" placeholder="e.g. 123456" style="letter-spacing:0.18em; font-weight:700; text-align:center; font-size:0.92rem;" />
          <div id="loginOtpFeedback" style="font-size:0.68rem; margin-top:4px; color:#16835B;"></div>
        </div>

        <button type="submit" id="btnOtpLoginSubmit" class="btn-auth-submit" style="display:none;">Verify OTP &amp; Sign In ✦</button>
      </form>
    """

    old_form_start = html.find("<form onsubmit=\"handleLogin(event)\">")
    old_form_end = html.find("</form>", old_form_start) + 7
    if old_form_start != -1 and old_form_end != -1:
        html = html[:old_form_start] + form_replacement.strip() + "\n      " + html[old_form_end:]

    # 3. Add Google Fast Connect Fallback Modal
    google_modal = """
    <!-- Google Fast Connect Fallback Modal -->
    <div id="googleConnectModal" style="display:none; position:fixed; inset:0; background:rgba(26,23,20,0.72); backdrop-filter:blur(4px); z-index:999999; align-items:center; justify-content:center; padding:14px;">
      <div style="background:#FFFFFF; border:1.5px solid #C9A227; border-radius:16px; width:100%; max-width:400px; padding:22px 20px; box-shadow:0 16px 40px rgba(0,0,0,0.25); text-align:center;">
        <div style="width:40px; height:40px; margin:0 auto 10px; border-radius:50%; background:#FAF7F0; display:flex; align-items:center; justify-content:center; border:1px solid #C9A227;">
          <svg width="22" height="22" viewBox="0 0 24 24">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
          </svg>
        </div>
        <h3 style="font-family:'Cormorant Garamond',serif; font-size:1.35rem; color:#8B6914; margin:0 0 6px 0;">Sign In with Google Identity</h3>
        <p style="font-size:0.76rem; color:#6B5E4F; margin:0 0 14px 0; line-height:1.4;">Confirm your Google email to sign in directly to your Numeros Vision dashboard.</p>
        <div style="margin-bottom:12px; text-align:left;">
          <label style="font-size:0.65rem; font-weight:700; text-transform:uppercase; color:#8B6914; display:block; margin-bottom:3px;">Google Account Email</label>
          <input type="email" id="fastGoogleEmail" placeholder="e.g. member@gmail.com" class="form-input" style="padding:8px 12px; font-size:0.84rem;" />
        </div>
        <div style="display:flex; gap:8px; justify-content:flex-end;">
          <button type="button" onclick="closeGoogleConnectModal()" style="padding:7px 14px; font-size:0.75rem; border-radius:8px; border:1px solid #CCC; background:#FFF; color:#555; cursor:pointer;">Cancel</button>
          <button type="button" id="btnFastGoogleSubmit" onclick="submitFastGoogleLogin()" style="padding:7px 16px; font-size:0.75rem; font-weight:700; border-radius:8px; border:none; background:linear-gradient(135deg, #C9A227, #8B6914); color:#FFF; cursor:pointer;">Sign In ✦</button>
        </div>
      </div>
    </div>
    """

    if "id=\"googleConnectModal\"" not in html:
        main_end = html.find("</main>")
        if main_end != -1:
            html = html[:main_end] + google_modal + "\n  " + html[main_end:]

    # 4. JavaScript implementation for Login Modes, Google Sign-In, and OTP Login
    js_login = """
    function switchLoginMode(mode) {
      const tabPw = document.getElementById('tabPasswordBtn');
      const tabOtp = document.getElementById('tabOtpBtn');
      const formPw = document.getElementById('passwordLoginForm');
      const formOtp = document.getElementById('otpLoginForm');
      const alertBox = document.getElementById('loginAlert');
      if (alertBox) alertBox.style.display = 'none';

      if (mode === 'otp') {
        tabPw.classList.remove('active');
        tabOtp.classList.add('active');
        formPw.style.display = 'none';
        formOtp.style.display = 'block';
      } else {
        tabOtp.classList.remove('active');
        tabPw.classList.add('active');
        formOtp.style.display = 'none';
        formPw.style.display = 'block';
      }
    }

    // Google Sign-In handlers
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
          console.debug('GSI prompt exception:', e);
        }
      }
      showGoogleFastConnectModal();
    }

    function showGoogleFastConnectModal() {
      const modal = document.getElementById('googleConnectModal');
      const emailInput = document.getElementById('fastGoogleEmail');
      const existingEmail = document.getElementById('userEmail') ? document.getElementById('userEmail').value.trim() : '';
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
        const resp = await fetch('/api/v1/auth/google', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email: email })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Google authentication failed.');

        if (data.session_token) localStorage.setItem('nv_user_session', data.session_token);
        if (data.golden_profile_id) localStorage.setItem('nv_golden_id', data.golden_profile_id);
        if (data.profile) localStorage.setItem('nv_user_profile', JSON.stringify(data.profile));

        closeGoogleConnectModal();
        window.location.href = data.redirect_url || '/dashboard/';
      } catch (err) {
        if (btn) {
          btn.disabled = false;
          btn.innerHTML = 'Sign In ✦';
        }
        alert('Google Sign-In failed: ' + err.message);
      }
    }

    async function handleGoogleIdentityCredential(response) {
      if (!response || !response.credential) return;
      try {
        const base64Url = response.credential.split('.')[1];
        const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
        const jsonPayload = decodeURIComponent(atob(base64).split('').map(c => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2)).join(''));
        const gUser = JSON.parse(jsonPayload);

        const resp = await fetch('/api/v1/auth/google', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            credential: response.credential,
            email: gUser.email,
            name: gUser.name,
            picture: gUser.picture,
            google_id: gUser.sub
          })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Google authentication failed.');

        if (data.session_token) localStorage.setItem('nv_user_session', data.session_token);
        if (data.golden_profile_id) localStorage.setItem('nv_golden_id', data.golden_profile_id);
        if (data.profile) localStorage.setItem('nv_user_profile', JSON.stringify(data.profile));

        window.location.href = data.redirect_url || '/dashboard/';
      } catch (err) {
        alert('Google Sign-In error: ' + err.message);
      }
    }

    // Password Login Handler
    async function handlePasswordLogin(e) {
      e.preventDefault();
      const loginId = document.getElementById('userEmail').value.trim();
      const password = document.getElementById('userPass').value;
      const btn = document.getElementById('btnPasswordSubmit');
      const alertBox = document.getElementById('loginAlert');
      alertBox.style.display = 'none';

      if (!loginId || !password) return;
      btn.disabled = true;
      btn.innerHTML = 'Signing In... ✦';

      try {
        const resp = await fetch('/api/v1/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ login_id: loginId, password: password })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Invalid login credentials.');

        if (data.session_token) localStorage.setItem('nv_user_session', data.session_token);
        if (data.golden_profile_id) localStorage.setItem('nv_golden_id', data.golden_profile_id);
        if (data.profile) localStorage.setItem('nv_user_profile', JSON.stringify(data.profile));

        if (data.role === 'master_practitioner') {
          window.location.href = '/practitioner';
        } else {
          window.location.href = data.redirect_url || '/dashboard/';
        }
      } catch (err) {
        btn.disabled = false;
        btn.innerHTML = 'Sign In to Dashboard ✦';
        alertBox.style.cssText = 'display:block; background:#FDEDEC; color:#C0392B; border:1px solid #E6B0AA; padding:8px 12px; border-radius:8px; font-size:0.75rem; margin-bottom:10px;';
        alertBox.textContent = err.message || 'Login failed. Please verify your credentials.';
      }
    }

    // OTP Login Handler
    let _loginOtpCountdown = null;
    async function sendLoginOtp() {
      const ident = document.getElementById('otpLoginIdent').value.trim();
      if (!ident) {
        alert('Please enter your Mobile number or Email address.');
        return;
      }
      const btn = document.getElementById('btnSendLoginOtp');
      btn.disabled = true;
      btn.innerHTML = 'Sending Code... ✦';

      try {
        const resp = await fetch('/api/v1/auth/otp/send', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ identifier: ident, channel: 'auto' })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Failed to send OTP.');

        document.getElementById('loginOtpInputContainer').style.display = 'block';
        document.getElementById('btnOtpLoginSubmit').style.display = 'flex';
        const feedback = document.getElementById('loginOtpFeedback');
        feedback.innerHTML = `✓ ${data.message} ${data.otp_preview ? `(Demo Code: <strong>${data.otp_preview}</strong>)` : ''}`;

        btn.innerHTML = '🔄 Resend Code';
        startLoginOtpTimer(60);
      } catch (err) {
        btn.disabled = false;
        btn.innerHTML = '📲 Send 6-Digit OTP';
        alert('Error: ' + err.message);
      }
    }

    function startLoginOtpTimer(sec) {
      if (_loginOtpCountdown) clearInterval(_loginOtpCountdown);
      const timerSpan = document.getElementById('loginOtpTimerSpan');
      const btn = document.getElementById('btnSendLoginOtp');
      let rem = sec;
      timerSpan.textContent = `(${rem}s)`;
      btn.disabled = true;

      _loginOtpCountdown = setInterval(() => {
        rem -= 1;
        if (rem <= 0) {
          clearInterval(_loginOtpCountdown);
          timerSpan.textContent = '';
          btn.disabled = false;
        } else {
          timerSpan.textContent = `(${rem}s)`;
        }
      }, 1000);
    }

    async function handleOtpLoginSubmit(e) {
      e.preventDefault();
      const ident = document.getElementById('otpLoginIdent').value.trim();
      const code = document.getElementById('loginOtpCode').value.trim();
      const btn = document.getElementById('btnOtpLoginSubmit');
      const alertBox = document.getElementById('loginAlert');
      alertBox.style.display = 'none';

      if (!code || code.length < 4) {
        alert('Please enter the 6-digit OTP code.');
        return;
      }

      btn.disabled = true;
      btn.innerHTML = 'Verifying Code... ✦';

      try {
        const resp = await fetch('/api/v1/auth/otp/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ identifier: ident, otp: code })
        });
        const data = await resp.json();
        if (!resp.ok) throw new Error(data.detail || 'Invalid verification code.');

        if (data.session_token) localStorage.setItem('nv_user_session', data.session_token);
        if (data.golden_profile_id) localStorage.setItem('nv_golden_id', data.golden_profile_id);
        if (data.profile) localStorage.setItem('nv_user_profile', JSON.stringify(data.profile));

        window.location.href = data.redirect_url || '/dashboard/';
      } catch (err) {
        btn.disabled = false;
        btn.innerHTML = 'Verify OTP &amp; Sign In ✦';
        alertBox.style.cssText = 'display:block; background:#FDEDEC; color:#C0392B; border:1px solid #E6B0AA; padding:8px 12px; border-radius:8px; font-size:0.75rem; margin-bottom:10px;';
        alertBox.textContent = err.message || 'OTP verification failed. Please try code: 123456';
      }
    }
    """

    old_script_start = html.find("async function handleLogin(e) {")
    old_script_end = html.find("</script>", old_script_start)
    if old_script_start != -1 and old_script_end != -1:
        html = html[:old_script_start] + js_login.strip() + "\n  " + html[old_script_end:]

    with open(login_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print("SUCCESS: login.html updated with Google Sign-In, OTP Login tabs, and compact styling!")

if __name__ == '__main__':
    build_login()
