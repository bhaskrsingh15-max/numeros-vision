import os
import requests
import base64
import json
from dotenv import load_dotenv

load_dotenv('.env')

key_id = os.getenv('RAZORPAY_KEY_ID')
key_secret = os.getenv('RAZORPAY_KEY_SECRET')

print("Testing Razorpay Live API Connection...")
print(f"Key ID: {key_id}")
print(f"Key Secret: {'*' * (len(key_secret)-4) + key_secret[-4:] if key_secret else 'None'}")

if not key_id or not key_secret:
    print("ERROR: Razorpay keys not found in .env")
    exit(1)

# Test creating order for 199 INR (Basic Report)
auth_str = f"{key_id}:{key_secret}"
auth_header = f"Basic {base64.b64encode(auth_str.encode()).decode()}"

payload = {
    "amount": 19900,  # 199.00 INR in paise
    "currency": "INR",
    "receipt": f"test_rcpt_{int(os.times().elapsed * 1000)}",
    "notes": {
        "plan": "report_basic",
        "name": "Live Test Seeker",
        "email": "test@numerosvision.com"
    }
}

try:
    res = requests.post(
        "https://api.razorpay.com/v1/orders",
        headers={"Authorization": auth_header, "Content-Type": "application/json"},
        json=payload,
        timeout=10
    )
    print(f"Status Code: {res.status_code}")
    data = res.json()
    print("Response:")
    print(json.dumps(data, indent=2))
    
    if res.status_code == 200 and data.get("id"):
        print("\n✅ SUCCESS: Razorpay Order Created Successfully!")
        print(f"Order ID: {data.get('id')}")
        print(f"Amount: ₹{data.get('amount') / 100} ({data.get('currency')})")
    else:
        print("\n❌ Order creation failed:", data)
except Exception as e:
    print(f"\n❌ Network error: {e}")
