import json
import time
import urllib.request
import urllib.error

ENDPOINT = "https://pdf-service-bnlqaldstq-el.a.run.app/internal/v1/render-pdf"

def send_request(headers, data_bytes):
    req = urllib.request.Request(ENDPOINT, data=data_bytes, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return 0, str(e)

print(f"Testing live Cloud Run PDF render endpoint: {ENDPOINT}\n")

sample_body = json.dumps({
    "job_id": "job_test_001",
    "pack_id": "report_basic",
    "view": {
        "user": {"name": "Test User"},
        "subject": {"name": "Test Subject", "dob": "1990-08-15"}
    }
}).encode("utf-8")

# 1. Unsigned request
status1, body1 = send_request({"Content-Type": "application/json"}, sample_body)
print(f"1. Unsigned Request:\n   Status Code: {status1}\n   Response: {body1.strip()}\n")

# 2. Wrong signature
now_ts = str(int(time.time()))
headers2 = {
    "Content-Type": "application/json",
    "X-NV-Timestamp": now_ts,
    "X-NV-Signature": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
status2, body2 = send_request(headers2, sample_body)
print(f"2. Wrong Signature:\n   Status Code: {status2}\n   Response: {body2.strip()}\n")

# 3. Expired timestamp (>300s skew)
expired_ts = str(int(time.time()) - 600)
headers3 = {
    "Content-Type": "application/json",
    "X-NV-Timestamp": expired_ts,
    "X-NV-Signature": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef"
}
status3, body3 = send_request(headers3, sample_body)
print(f"3. Expired Timestamp (10 mins old):\n   Status Code: {status3}\n   Response: {body3.strip()}\n")

# 4. Oversize body (>64KB limit)
big_body = json.dumps({
    "job_id": "job_test_big",
    "pack_id": "report_basic",
    "padding": "A" * 70000
}).encode("utf-8")
headers4 = {
    "Content-Type": "application/json",
    "Content-Length": str(len(big_body)),
    "X-NV-Timestamp": now_ts,
    "X-NV-Signature": "any_sig"
}
status4, body4 = send_request(headers4, big_body)
print(f"4. Oversize Body (Size: {len(big_body)} bytes > 65536 max):\n   Status Code: {status4}\n   Response: {body4.strip()}\n")
