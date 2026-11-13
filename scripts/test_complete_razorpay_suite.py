# scripts/test_complete_razorpay_suite.py
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import hmac
import hashlib
import json
import time

# Ensure environment variables are loaded
from dotenv import load_dotenv
load_dotenv(override=True)

import razorpay
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_tests():
    print("==================================================")
    print("RUNNING COMPLETE RAZORPAY INTEGRATION TEST SUITE")
    print("==================================================")

    # 1. Environment & SDK Check
    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")
    print(f"1. Razorpay Key ID: {key_id}")
    print(f"   Razorpay Secret Loaded: {'YES' if key_secret else 'NO'}")
    assert key_id, "RAZORPAY_KEY_ID must be set in .env"
    assert key_secret, "RAZORPAY_KEY_SECRET must be set in .env"

    # 2. Test Minimum Amount Validation (< 100 paise)
    print("\n2. Testing Minimum Amount Validation (< 100 paise):")
    res_min = client.post("/api/create-order", json={"amount": 50, "currency": "INR"})
    print(f"   Status Code: {res_min.status_code}")
    assert res_min.status_code == 400, f"Expected 400 for < 100 paise, got {res_min.status_code}"
    print("   [PASS] Rejected order with < 100 paise with HTTP 400.")

    # 3. Test POST /api/create-order (Standard Endpoint)
    print("\n3. Testing POST /api/create-order:")
    order_payload = {
        "amount": 105000, # paise (₹1,050)
        "currency": "INR",
        "receipt": f"test_rcpt_{int(time.time())}",
        "plan": "report_master",
        "customer_name": "Test Seeker",
        "customer_email": "seeker@example.com",
        "customer_phone": "+919876543210"
    }
    res_order = client.post("/api/create-order", json=order_payload)
    print(f"   Status Code: {res_order.status_code}")
    assert res_order.status_code == 200, f"Order creation failed: {res_order.text}"
    order_data = res_order.json()
    order_id = order_data["order_id"]
    print(f"   Razorpay Order ID returned: {order_id}")
    print(f"   Amount (paise): {order_data['amount']}")
    print(f"   Currency: {order_data['currency']}")
    assert order_id.startswith("order_"), f"Invalid order_id format: {order_id}"
    assert order_data["amount"] == 105000
    assert order_data["currency"] == "INR"
    print("   [PASS] Live Razorpay order successfully created on Razorpay API.")

    # 4. Test Missing Fields in Verification
    print("\n4. Testing Missing Fields in POST /api/verify-payment:")
    res_missing = client.post("/api/verify-payment", json={
        "razorpay_order_id": order_id
    })
    print(f"   Status Code: {res_missing.status_code}")
    assert res_missing.status_code == 400, f"Expected 400 for missing fields, got {res_missing.status_code}"
    print("   [PASS] Missing payment_id / signature rejected with HTTP 400.")

    # 5. Test Signature Tampering / Mismatch
    print("\n5. Testing Signature Mismatch in POST /api/verify-payment:")
    fake_payment_id = "pay_Tw4FakeTest123"
    fake_sig = "0000000000000000000000000000000000000000000000000000000000000000"
    res_mismatch = client.post("/api/verify-payment", json={
        "razorpay_order_id": order_id,
        "razorpay_payment_id": fake_payment_id,
        "razorpay_signature": fake_sig,
        "plan": "report_master",
        "email": "seeker@example.com"
    })
    print(f"   Status Code: {res_mismatch.status_code}")
    assert res_mismatch.status_code == 400, f"Expected 400 for bad signature, got {res_mismatch.status_code}"
    print(f"   Detail: {res_mismatch.json().get('detail')}")
    print("   [PASS] Tampered signature rejected with HTTP 400. Not marked as paid.")

    # 6. Test Valid HMAC-SHA256 Signature Verification
    print("\n6. Testing Valid HMAC-SHA256 Signature in POST /api/verify-payment:")
    valid_payment_id = f"pay_{order_id.replace('order_', '')}"
    msg = f"{order_id}|{valid_payment_id}".encode()
    valid_sig = hmac.new(key_secret.encode(), msg, hashlib.sha256).hexdigest()

    res_verify = client.post("/api/verify-payment", json={
        "razorpay_order_id": order_id,
        "razorpay_payment_id": valid_payment_id,
        "razorpay_signature": valid_sig,
        "plan": "report_master",
        "email": "seeker@example.com",
        "customer_name": "Test Seeker"
    })
    print(f"   Status Code: {res_verify.status_code}")
    assert res_verify.status_code == 200, f"Valid verification failed: {res_verify.text}"
    v_data = res_verify.json()
    print(f"   Verified: {v_data.get('verified')}")
    print(f"   Status: {v_data.get('status')}")
    print(f"   Generated Invoice ID: {v_data.get('invoice_id')}")
    print(f"   Unlocked Report: {v_data.get('unlocked_report')}")
    assert v_data.get("verified") is True
    assert v_data.get("status") == "success"
    assert v_data.get("invoice_id") is not None
    print("   [PASS] Valid HMAC-SHA256 signature verified and invoice generated.")

    # 7. Test Framework Aliases: POST /api/v1/payments/create-order and /verify
    print("\n7. Testing Aliases /api/v1/payments/create-order and /verify:")
    res_alias = client.post("/api/v1/payments/create-order", json={
        "amount": 51000,
        "currency": "INR",
        "receipt": f"test_alias_{int(time.time())}",
        "plan": "report_advanced"
    })
    assert res_alias.status_code == 200
    alias_order = res_alias.json()
    print(f"   Alias Order ID: {alias_order['order_id']}")

    alias_pay_id = f"pay_{alias_order['order_id'].replace('order_', '')}"
    alias_msg = f"{alias_order['order_id']}|{alias_pay_id}".encode()
    alias_sig = hmac.new(key_secret.encode(), alias_msg, hashlib.sha256).hexdigest()

    res_alias_verify = client.post("/api/v1/payments/verify", json={
        "razorpay_order_id": alias_order['order_id'],
        "razorpay_payment_id": alias_pay_id,
        "razorpay_signature": alias_sig,
        "plan": "report_advanced",
        "email": "alias_seeker@example.com"
    })
    assert res_alias_verify.status_code == 200
    print("   [PASS] Framework alias routes verified successfully.")

    print("\n==================================================")
    print("ALL 7 RAZORPAY INTEGRATION TESTS PASSED 100%!")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
