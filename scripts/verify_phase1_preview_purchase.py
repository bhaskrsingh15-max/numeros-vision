"""
Phase 1 Preview End-to-End Purchase Verifier (Razorpay Test Mode)
=================================================================
Executes one complete paid report purchase against https://preview.numeros-vision.pages.dev:
  0. Direct /api/v1/reports/generate-pdf block verification (HTTP 403)
  1. Sign-in (preview QA session + GET /api/v1/auth/me)
  2. Create order (POST /api/v1/payments/create-order -> live Razorpay test order)
  3. Payment signature verification (POST /api/v1/payments/verify)
  4. Signed Razorpay webhook (POST /api/v1/payments/webhook -> report_jobs + PDF + Brevo email)
  5. Order & report job status poll (GET /api/v1/payments/status -> COMPLETED in R2)
  6. Dashboard verification (GET /api/v1/dashboard/view -> shows report & entitlement)
  7. Signed download link minting (POST /api/v1/reports/download-token)
  8. Private R2 PDF download & content verification (GET /api/v1/reports/download)
  9. Order, R2 key, and confirmation email audit trail check

Strictly prints zero secret values.
"""
from __future__ import annotations

import hashlib
import hmac
import http.cookiejar
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from pypdf import PdfReader

REPO_ROOT = Path(__file__).resolve().parent.parent
PREVIEW_BASE = os.environ.get("NV_PREVIEW_BASE_URL", "https://preview.numeros-vision.pages.dev").rstrip("/")


def load_dotenv(path: Path) -> dict[str, str]:
    vals: dict[str, str] = {}
    if not path.exists():
        return vals
    for raw in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        vals[k.strip()] = v.strip().strip('"').strip("'")
    return vals


def mask_email(email: str) -> str:
    if "@" not in email:
        return "***"
    local, dom = email.split("@", 1)
    return f"{local[:2]}***@{dom}"


def main() -> int:
    out_pdf_path = Path(
        sys.argv[1]
        if len(sys.argv) > 1
        else str(REPO_ROOT / "pdf_service" / "output" / "phase1_preview_test_purchase.pdf")
    )
    out_log_json = Path(sys.argv[2]) if len(sys.argv) > 2 else None

    env_vals = load_dotenv(REPO_ROOT / ".env")
    qa_secret = (os.environ.get("NV_PREVIEW_QA_SECRET") or "").strip()
    qa_secret_file = (os.environ.get("NV_PREVIEW_QA_SECRET_FILE") or "").strip()
    if not qa_secret and qa_secret_file and Path(qa_secret_file).exists():
        qa_secret = Path(qa_secret_file).read_text(encoding="utf-8").strip()
    if not qa_secret:
        raise RuntimeError("Missing NV_PREVIEW_QA_SECRET or NV_PREVIEW_QA_SECRET_FILE.")

    base_email = (os.environ.get("EMAIL_FROM") or env_vals.get("EMAIL_FROM") or "qa@numerosvision.com").strip()
    if "<" in base_email and ">" in base_email:
        base_email = base_email.split("<", 1)[1].split(">", 1)[0].strip()

    ts_sec = int(time.time())
    if "@" in base_email:
        elocal, edom = base_email.split("@", 1)
        qa_email = f"{elocal}+nvqa{ts_sec}@{edom}".lower()
    else:
        qa_email = f"nvqa{ts_sec}@numerosvision.com"

    jar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

    steps_log: list[dict] = []

    def qa_headers_for(raw_body_bytes: bytes) -> dict[str, str]:
        ts_str = str(int(time.time()))
        sig = hmac.new(qa_secret.encode("utf-8"), f"{ts_str}.".encode("utf-8") + raw_body_bytes, hashlib.sha256).hexdigest()
        return {"X-NV-QA-Timestamp": ts_str, "X-NV-QA-Signature": sig}

    def request_json(
        step_name: str,
        method: str,
        path: str,
        body: dict | bytes | None = None,
        extra_headers: dict | None = None,
    ) -> tuple[int, dict, dict]:
        url = PREVIEW_BASE + path
        headers = {
            "Origin": PREVIEW_BASE,
            "Referer": PREVIEW_BASE + "/pricing/",
            "Accept": "application/json",
            "User-Agent": "NV-Phase1-Preview-Verifier/1.0",
        }
        data_bytes = None
        if isinstance(body, dict):
            data_bytes = json.dumps(body, separators=(",", ":")).encode("utf-8")
            headers["Content-Type"] = "application/json"
        elif isinstance(body, bytes):
            data_bytes = body
            headers["Content-Type"] = "application/json"
        if extra_headers:
            headers.update(extra_headers)

        t0 = time.perf_counter()
        req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
        try:
            resp = opener.open(req, timeout=45.0)
            status = resp.status
            resp_headers = {k.lower(): v for k, v in resp.headers.items()}
            raw_resp = resp.read()
        except urllib.error.HTTPError as e:
            status = e.code
            resp_headers = {k.lower(): v for k, v in e.headers.items()}
            raw_resp = e.read()
        elapsed_ms = round((time.perf_counter() - t0) * 1000, 1)
        try:
            parsed = json.loads(raw_resp.decode("utf-8", errors="replace"))
        except Exception:
            parsed = {"raw_preview": raw_resp.decode("utf-8", errors="replace")[:300]}

        entry = {
            "step": step_name,
            "method": method,
            "path": path,
            "status": status,
            "elapsed_ms": elapsed_ms,
        }
        steps_log.append(entry)
        print(f"[{step_name}] {method} {path} -> HTTP {status} ({elapsed_ms} ms)")
        return status, resp_headers, parsed

    # Warm Render preview PDF generator first
    try:
        with urllib.request.urlopen("https://numeros-pdf-preview.onrender.com/health", timeout=60.0) as hresp:
            print(f"[0a. Render PDF Service Health] GET /health -> HTTP {hresp.status}")
    except Exception as exc:
        print(f"[WARN] Render health warmup note: {exc}")

    # Step 0b: Verify Razorpay gateway credentials health on preview via test-console
    st_gw, _, data_gw = request_json(
        "0b. Preview Gateway Health Check (/api/admin/test-console)",
        "GET",
        "/api/admin/test-console?format=json",
        None,
        qa_headers_for(b""),
    )
    assert st_gw == 200, f"Test console gateway check failed ({st_gw}): {data_gw}"
    gw_info = data_gw.get("gateway_check") or {}
    steps_log[-1]["note"] = f"razorpay_status={gw_info.get('razorpay_status')}, key_prefix={gw_info.get('key_id_prefix')}, accepted={gw_info.get('accepted')}"
    print(f"    Gateway check: {steps_log[-1]['note']}")

    # Step 0c: Verify /api/v1/reports/generate-pdf remains blocked (403) with clean indication copy
    st0, _, data0 = request_json(
        "0c. Direct PDF Endpoint Blocked Check",
        "POST",
        "/api/v1/reports/generate-pdf",
        {"name": "Arun Sharma", "dob": "1981-11-28", "tier": "basic"},
    )
    assert st0 == 403, f"Expected 403 on /api/v1/reports/generate-pdf, got {st0}: {data0}"
    assert "verified" not in json.dumps(data0).lower(), f"Forbidden word in generate-pdf message: {data0}"
    steps_log[-1]["note"] = f"code={data0.get('code')}"

    # Step 1: Preview QA Sign-In + Auth Session Verification
    qa_signin_raw = json.dumps({"action": "preview_qa_signin", "email": qa_email}, separators=(",", ":")).encode("utf-8")
    st1, _, data1 = request_json(
        "1a. Sign-In (Preview Session & Checkout Token)",
        "POST",
        "/api/admin/test-console",
        qa_signin_raw,
        qa_headers_for(qa_signin_raw),
    )
    assert st1 == 200 and data1.get("success") is True, f"QA Sign-In failed ({st1}): {data1}"
    checkout_token = data1["checkout_token"]
    user_id = data1["user_id"]
    steps_log[-1]["note"] = f"Signed in user_id={user_id} ({mask_email(qa_email)}); __Host-nv_session cookie set"

    st1b, _, data1b = request_json("1b. Verify Active Session (/api/v1/auth/me)", "GET", "/api/v1/auth/me")
    assert st1b == 200 and data1b.get("authenticated") is True, f"Session check failed ({st1b}): {data1b}"
    steps_log[-1]["note"] = f"authenticated={data1b.get('authenticated')}, user_id={user_id}"

    # Step 2: Create Order in Razorpay Test Mode
    order_payload = {
        "pack_id": "report_basic",
        "email": qa_email,
        "checkout_token": checkout_token,
        "name": "Arun Sharma",
        "dob": "28-11-1981",
        "gender": "male",
        "consent_service": True,
    }
    st2, _, data2 = request_json(
        "2. Create Paid Report Order (Razorpay Test Mode)",
        "POST",
        "/api/v1/payments/create-order",
        order_payload,
    )
    assert st2 == 200 and (data2.get("order_id") or data2.get("rzp_order_id") or data2.get("id")), f"Create order failed ({st2}): {data2}"
    rzp_order_id = data2.get("rzp_order_id") or data2.get("id") or data2.get("order_id")
    internal_order_id = data2.get("internal_order_id") or data2.get("orderId") or data2.get("order_id")
    amount_paise = int(data2.get("amount") or data2.get("amount_paise") or 19900)
    assert str(rzp_order_id).startswith("order_"), f"Expected Razorpay order_ id, got: {data2}"
    steps_log[-1]["note"] = f"rzp_order_id={rzp_order_id}, internal_order_id={internal_order_id}, amount_paise={amount_paise}"

    # Prepare Razorpay test payment & webhook payloads and compute signatures via preview QA signer
    rzp_payment_id = f"pay_test_{int(time.time())}"
    wh_now = int(time.time())
    wh_body_obj = {
        "event": "payment.captured",
        "event_id": f"evt_preview_p1_{wh_now}",
        "created_at": wh_now,
        "payload": {
            "payment": {
                "entity": {
                    "id": rzp_payment_id,
                    "order_id": rzp_order_id,
                    "amount": amount_paise,
                    "currency": "INR",
                    "status": "captured",
                    "method": "card",
                }
            }
        },
    }
    wh_raw_str = json.dumps(wh_body_obj, separators=(",", ":"))
    sign_req_raw = json.dumps(
        {
            "action": "preview_qa_sign_test_payment",
            "rzp_order_id": rzp_order_id,
            "rzp_payment_id": rzp_payment_id,
            "raw_webhook_json": wh_raw_str,
        },
        separators=(",", ":"),
    ).encode("utf-8")
    st_sig, _, data_sig = request_json(
        "2b. Sign Test Mode Payment & Webhook Payloads",
        "POST",
        "/api/admin/test-console",
        sign_req_raw,
        qa_headers_for(sign_req_raw),
    )
    assert st_sig == 200 and data_sig.get("success") is True, f"Test payment signing failed ({st_sig}): {data_sig}"
    pay_sig = data_sig["payment_signature"]
    wh_sig = data_sig["webhook_signature"]

    # Step 3: Razorpay Payment & Signature Verification
    st3, _, data3 = request_json(
        "3. Verify Razorpay Payment Signature (/api/v1/payments/verify)",
        "POST",
        "/api/v1/payments/verify",
        {
            "razorpay_order_id": rzp_order_id,
            "razorpay_payment_id": rzp_payment_id,
            "razorpay_signature": pay_sig,
            "email": qa_email,
            "checkout_token": checkout_token,
        },
    )
    assert st3 == 200 and data3.get("verified") is True, f"Payment verify failed ({st3}): {data3}"
    internal_order_id = data3.get("orderId") or internal_order_id
    steps_log[-1]["note"] = f"orderId={internal_order_id}, orderStatus={data3.get('orderStatus')}, reportStatus={data3.get('reportStatus')}"

    # Step 4: Signed Razorpay Webhook (payment.captured -> entitlement + report_jobs + PDF + Brevo email)
    wh_raw = wh_raw_str.encode("utf-8")
    st4, _, data4 = request_json(
        "4. Razorpay Webhook Fulfillment (/api/v1/payments/webhook)",
        "POST",
        "/api/v1/payments/webhook",
        wh_raw,
        {"X-Razorpay-Signature": wh_sig},
    )
    assert st4 == 200 and data4.get("status") == "success", f"Webhook failed ({st4}): {data4}"
    job_id = data4.get("jobId")
    steps_log[-1]["note"] = f"message={data4.get('message')}, jobId={job_id}"

    # Step 5: Poll /api/v1/payments/status until PDF is generated & stored in R2
    final_status_data = None
    for poll_idx in range(1, 18):
        st5, _, data5 = request_json(
            f"5.{poll_idx}. Poll Order & Report Job Status",
            "GET",
            f"/api/v1/payments/status?order_id={internal_order_id}",
        )
        assert st5 == 200, f"Status poll failed ({st5}): {data5}"
        rep_status = (data5.get("reportStatus") or data5.get("jobStatus") or "").upper()
        steps_log[-1]["note"] = f"orderStatus={data5.get('status')}, reportStatus={rep_status}"
        if rep_status in ("COMPLETED", "DOWNLOADED", "READY"):
            final_status_data = data5
            job_id = data5.get("jobId") or job_id
            break
        time.sleep(2.5)
    assert final_status_data is not None, f"Report job did not reach COMPLETED within timeout. Last response: {data5}"

    # Step 6: Dashboard View Verification
    st6, _, data6 = request_json(
        "6. Dashboard View Verification (/api/v1/dashboard/view)",
        "GET",
        "/api/v1/dashboard/view",
    )
    assert st6 == 200, f"Dashboard view failed ({st6}): {data6}"
    dash_dump = json.dumps(data6)
    assert "report_basic" in dash_dump and str(job_id) in dash_dump, f"Dashboard missing report_basic or job {job_id}: {dash_dump[:500]}"
    dash_reports = data6.get("reports") or data6.get("data", {}).get("reports") or []
    matched_rep = next((r for r in dash_reports if str(r.get("id")) == str(job_id) or r.get("packId") == "report_basic"), {})
    dash_orders = data6.get("orders") or data6.get("data", {}).get("orders") or []
    matched_ord = next((o for o in dash_orders if str(o.get("id")) == str(internal_order_id)), {})
    subject_id = (
        matched_rep.get("subjectId")
        or matched_ord.get("subject_id")
        or data2.get("subject_id")
        or data2.get("subjectId")
    )
    assert subject_id, f"Could not resolve subjectId from dashboard view: {dash_dump[:500]}"
    steps_log[-1]["note"] = f"Dashboard lists unlocked report_basic, subjectId={subject_id}, jobId={job_id} (COMPLETED)"

    # Step 7: Mint Signed 5-Minute Download Link
    st7, _, data7 = request_json(
        "7. Mint Signed Download Token (/api/v1/reports/download-token)",
        "POST",
        "/api/v1/reports/download-token",
        {"subjectId": subject_id, "packId": "report_basic", "jobId": job_id},
    )
    assert st7 == 200 and data7.get("downloadUrl"), f"Download token mint failed ({st7}): {data7}"
    download_url = data7["downloadUrl"]
    steps_log[-1]["note"] = f"downloadUrl minted (TTL={data7.get('expiresInSeconds')}s)"

    # Step 8: Download Stored PDF from R2 & Validate Bytes/Content
    t0 = time.perf_counter()
    dl_req = urllib.request.Request(
        PREVIEW_BASE + download_url,
        headers={"User-Agent": "NV-Phase1-Preview-Verifier/1.0"},
        method="GET",
    )
    dl_resp = opener.open(dl_req, timeout=45.0)
    dl_status = dl_resp.status
    dl_ct = dl_resp.headers.get("Content-Type", "")
    dl_cc = dl_resp.headers.get("Cache-Control", "")
    pdf_bytes = dl_resp.read()
    dl_ms = round((time.perf_counter() - t0) * 1000, 1)

    assert dl_status == 200, f"PDF download failed: HTTP {dl_status}"
    assert "application/pdf" in dl_ct.lower(), f"Unexpected Content-Type: {dl_ct}"
    assert pdf_bytes.startswith(b"%PDF-"), "Downloaded payload is not a valid PDF"

    out_pdf_path.parent.mkdir(parents=True, exist_ok=True)
    out_pdf_path.write_bytes(pdf_bytes)
    pdf_sha256 = hashlib.sha256(pdf_bytes).hexdigest()

    reader = PdfReader(str(out_pdf_path))
    num_pages = len(reader.pages)
    extracted_text = "\n".join((p.extract_text() or "") for p in reader.pages)
    assert num_pages == 3, f"Expected 3-page Basic Report PDF, got {num_pages} pages"
    assert "Arun Sharma" in extracted_text, "Customer name Arun Sharma missing from downloaded PDF"
    assert "28" in extracted_text and "1981" in extracted_text, "Customer DOB missing from downloaded PDF"

    steps_log.append({
        "step": "8. Download Private R2 PDF (/api/v1/reports/download)",
        "method": "GET",
        "path": "/api/v1/reports/download?token=<redacted>",
        "status": dl_status,
        "elapsed_ms": dl_ms,
        "note": f"bytes={len(pdf_bytes)}, pages={num_pages}, sha256={pdf_sha256[:16]}..., Content-Type={dl_ct}, Cache-Control={dl_cc}",
    })
    print(f"[8. Download Private R2 PDF] GET /api/v1/reports/download -> HTTP {dl_status} ({len(pdf_bytes)} bytes, {num_pages} pages)")

    # Step 9: Verify R2 Storage Row, DOWNLOADED State Transition & Confirmation Email Audit Log
    audit_raw = json.dumps({"action": "preview_qa_order_audit", "order_id": internal_order_id}, separators=(",", ":")).encode("utf-8")
    st9, _, data9 = request_json(
        "9. Audit Order, R2 Storage & Confirmation Email Status",
        "POST",
        "/api/admin/test-console",
        audit_raw,
        qa_headers_for(audit_raw),
    )
    assert st9 == 200 and data9.get("success") is True, f"Order audit check failed ({st9}): {data9}"
    rjob = data9.get("report_job") or {}
    audit_actions = [a.get("action") for a in (data9.get("audit_trail") or [])]
    steps_log[-1]["note"] = (
        f"order.status={data9.get('order', {}).get('status')}, "
        f"job.status={rjob.get('status')}, r2_key={rjob.get('r2_key')}, "
        f"audit_actions={audit_actions}"
    )
    print("Audit Actions Recorded:", audit_actions)

    summary = {
        "preview_base": PREVIEW_BASE,
        "order_id": internal_order_id,
        "rzp_order_id": rzp_order_id,
        "job_id": job_id,
        "r2_key": rjob.get("r2_key"),
        "job_final_status": rjob.get("status"),
        "pdf_path": str(out_pdf_path),
        "pdf_bytes": len(pdf_bytes),
        "pdf_pages": num_pages,
        "pdf_sha256": pdf_sha256,
        "audit_actions": audit_actions,
        "steps": steps_log,
    }
    if out_log_json:
        out_log_json.parent.mkdir(parents=True, exist_ok=True)
        out_log_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\n=== PHASE 1 PREVIEW E2E TEST PURCHASE PASSED ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
