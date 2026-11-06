import os
import re

def test_no_hardcoded_fast2sms_key():
    worker_path = os.path.join("app", "static", "_worker.js")
    with open(worker_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "fARs9PhAySOXBrH5" not in content, "Found hardcoded Fast2SMS key in _worker.js"
    assert "const FAST2SMS_API_KEY" not in content, "Found FAST2SMS_API_KEY constant in _worker.js"
    assert "env.FAST2SMS_API_KEY" in content, "env.FAST2SMS_API_KEY must be read from environment"

def test_no_session_otp_echo():
    worker_path = os.path.join("app", "static", "_worker.js")
    with open(worker_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "session_otp:" not in content, "Found session_otp echo in _worker.js response"

def test_no_hardcoded_razorpay_keys():
    worker_path = os.path.join("app", "static", "_worker.js")
    with open(worker_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "TwcQLlhj2djlqG" not in content, "Found hardcoded Razorpay Key ID in _worker.js"
    assert "1ULhquBIAgRpt7D3VrAU56hZ" not in content, "Found hardcoded Razorpay Secret in _worker.js"
    assert "Ir09f2ySb06fy5ujnZUe32B6" not in content, "Found hardcoded old Razorpay Secret in _worker.js"

def test_no_pay_bypass():
    worker_path = os.path.join("app", "static", "_worker.js")
    with open(worker_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "cleanPaymentId.startsWith('pay_')" not in content, "Found pay_ bypass in _worker.js"

def test_reports_moved_out_of_public_static():
    static_reports = os.path.join("app", "static", "reports")
    if os.path.exists(static_reports):
        pdfs = [f for f in os.listdir(static_reports) if f.endswith(".pdf")]
        assert len(pdfs) == 0, f"Found public PDFs in app/static/reports: {pdfs}"
    private_reports = os.path.join("app", "reports", "private")
    assert os.path.exists(private_reports), "app/reports/private directory must exist"
    private_pdfs = [f for f in os.listdir(private_reports) if f.endswith(".pdf")]
    assert len(private_pdfs) > 0, "PDFs must be safely moved to app/reports/private"

def test_sample_dossier_preserved():
    sample_path = os.path.join("app", "static", "samples", "Numeros_Vision_Sample_Excerpt_Alexander_Vance.pdf")
    assert os.path.exists(sample_path), "Fictional sample excerpt must exist in app/static/samples"
    assert os.path.getsize(sample_path) > 10000, "Sample excerpt must be non-empty"
    private_sample = os.path.join("app", "reports", "private", "Numeros_Vision_Sample_Dossier_Fictional.pdf")
    assert os.path.exists(private_sample), "Full 32-page sample must be quarantined in app/reports/private"

def test_tunnel_files_removed():
    assert not os.path.exists("LIVE_URL.txt"), "LIVE_URL.txt must be removed"
    assert not os.path.exists("SECONDARY_URL.txt"), "SECONDARY_URL.txt must be removed"
    assert not os.path.exists("SSH_LIVE_URL.txt"), "SSH_LIVE_URL.txt must be removed"

def test_login_no_sandbox_code():
    login_path = os.path.join("app", "static", "login.html")
    with open(login_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Testing Sandbox Code" not in content, "Found sandbox code print in login.html"

def test_generate_pdf_upgrading_response():
    worker_path = os.path.join("app", "static", "_worker.js")
    with open(worker_path, "r", encoding="utf-8") as f:
        content = f.read()
    assert "REPORT_GENERATION_UPGRADING" in content, "Must return upgrading status code for generate-pdf"
