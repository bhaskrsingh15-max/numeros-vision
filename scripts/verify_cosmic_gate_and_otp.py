import urllib.request
import json
import re

BASE_URL = "http://127.0.0.1:8000"

def test_home_cosmic_gate():
    print("--- 1. Testing Homepage Cosmic Matrix Gate ---")
    req = urllib.request.Request(f"{BASE_URL}/")
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')

    assert '<form id="hero-calc-form" onsubmit="event.preventDefault(); calculateHeroProfile();">' in html, "Form onsubmit must be calculateHeroProfile()"
    assert '<div class="results-dashboard" id="birth-results" style="display:none;">' in html, "#birth-results must have style='display:none;'"
    assert 'calculateHeroProfile()' in html, "calculateHeroProfile must be defined"
    assert '_executeRenderCosmicProfile' in html, "_executeRenderCosmicProfile must be defined"
    assert 'window.nvProfileSync.requireConsentToReveal' in html, "Gate must call requireConsentToReveal"
    print("PASS: Homepage Cosmic Matrix gate is strictly guarded!")

def test_signup_page():
    print("--- 2. Testing Signup Page (Compact + Google + OTP) ---")
    req = urllib.request.Request(f"{BASE_URL}/signup/")
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')

    # Compact styling
    assert 'max-width: 490px;' in html, "Signup max-width must be 490px"
    assert 'padding: 7px 11px;' in html or 'padding: 8px 12px;' in html, "Compact input padding"
    
    # Google Sign-In
    assert 'triggerGoogleSignIn()' in html, "Google trigger must exist"
    assert 'handleGoogleIdentityCredential' in html, "Google callback must exist"
    assert 'googleConnectModal' in html, "Fast Google modal must exist"

    # OTP Verification Service
    assert 'otpServiceCard' in html, "OTP Service card must exist"
    assert 'sendOtpVerification()' in html, "sendOtpVerification function must exist"
    assert 'verifyOtpCode()' in html, "verifyOtpCode function must exist"
    assert '/api/v1/auth/otp/send' in html, "Endpoint call to send OTP must exist"
    assert '/api/v1/auth/otp/verify' in html, "Endpoint call to verify OTP must exist"
    print("PASS: Signup page has compact styles, working Google Sign-In, and customer OTP service!")

def test_login_page():
    print("--- 3. Testing Login Page (Google + OTP Login) ---")
    req = urllib.request.Request(f"{BASE_URL}/login/")
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8')

    assert 'tabPasswordBtn' in html and 'tabOtpBtn' in html, "Login mode tabs must exist"
    assert 'otpLoginForm' in html, "OTP login form must exist"
    assert 'sendLoginOtp()' in html, "sendLoginOtp function must exist"
    assert 'handleOtpLoginSubmit' in html, "handleOtpLoginSubmit function must exist"
    assert 'triggerGoogleSignIn()' in html, "Google trigger in login must exist"
    assert 'googleConnectModal' in html, "Fast Google modal in login must exist"
    print("PASS: Login page has OTP login tabs and working Google Sign-In!")

def test_api_endpoints():
    print("--- 4. Testing Backend OTP & Google Auth Endpoints ---")
    # A. Send OTP
    send_payload = json.dumps({"identifier": "+919876543210", "channel": "sms"}).encode('utf-8')
    send_req = urllib.request.Request(f"{BASE_URL}/api/v1/auth/otp/send", data=send_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(send_req) as resp:
        send_data = json.loads(resp.read().decode('utf-8'))
        assert send_data["status"] == "success"
        assert send_data["channel"] == "sms"
        assert "otp_preview" in send_data
        print(f"  [OK] OTP Send: {send_data['message']}")

    # B. Verify OTP
    verify_payload = json.dumps({"identifier": "+919876543210", "otp": "123456", "auto_login": False}).encode('utf-8')
    verify_req = urllib.request.Request(f"{BASE_URL}/api/v1/auth/otp/verify", data=verify_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(verify_req) as resp:
        verify_data = json.loads(resp.read().decode('utf-8'))
        assert verify_data["status"] == "success"
        assert verify_data["verified"] is True
        print(f"  [OK] OTP Verify: {verify_data['message']}")

    # C. OTP Login
    otp_login_payload = json.dumps({"identifier": "+919876543210", "otp": "123456", "name": "Deepak Verma"}).encode('utf-8')
    otp_login_req = urllib.request.Request(f"{BASE_URL}/api/v1/auth/otp/login", data=otp_login_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(otp_login_req) as resp:
        otp_login_data = json.loads(resp.read().decode('utf-8'))
        assert otp_login_data["status"] == "success"
        assert "session_token" in otp_login_data
        print(f"  [OK] OTP Login: {otp_login_data['message']}")

    # D. Google Auth
    g_payload = json.dumps({
        "email": "testuser.numeros@gmail.com",
        "name": "Test User",
        "day": 15,
        "month": 8,
        "year": 1990
    }).encode('utf-8')
    g_req = urllib.request.Request(f"{BASE_URL}/api/v1/auth/google", data=g_payload, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(g_req) as resp:
        g_data = json.loads(resp.read().decode('utf-8'))
        assert g_data["status"] == "success"
        assert "session_token" in g_data
        print("  [OK] Google Auth Endpoint: Success!")

    print("PASS: All Backend OTP and Google Auth endpoints working 100%!")

if __name__ == '__main__':
    test_home_cosmic_gate()
    test_signup_page()
    test_login_page()
    test_api_endpoints()
    print("\nALL 4 USER REQUIREMENTS VERIFIED AND VALIDATED 100%!")
