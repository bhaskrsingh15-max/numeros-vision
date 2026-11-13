import os
import sys
import json
import urllib.request
import re

# Load .env if present
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if os.path.exists(env_path):
    with open(env_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

api_key = os.getenv("FAST2SMS_API_KEY") or os.getenv("SMS_GATEWAY_API_KEY")

if not api_key:
    print("\n[ERROR] FAST2SMS_API_KEY is not found in your .env file.")
    print("Please add the following to your .env file:")
    print("  SMS_GATEWAY_PROVIDER=fast2sms")
    print("  FAST2SMS_API_KEY=your_actual_key_here\n")
    sys.exit(1)

if len(sys.argv) < 2:
    print("\nUsage: python scripts/test_fast2sms.py <10_DIGIT_INDIAN_MOBILE>")
    print("Example: python scripts/test_fast2sms.py 9876543210\n")
    sys.exit(1)

raw_phone = sys.argv[1]
clean_digits = re.sub(r"[^0-9]", "", raw_phone)
if len(clean_digits) < 10:
    print(f"\n[ERROR] Invalid mobile number: {raw_phone}. Must have at least 10 digits.")
    sys.exit(1)

mobile_10 = clean_digits[-10:]
test_otp = "789123"

print(f"\n--- FAST2SMS LIVE DISPATCH TEST ---")
print(f"Target Mobile: +91 {mobile_10}")
print(f"Test OTP Code: {test_otp}")
print(f"API Key: {api_key[:6]}...{api_key[-4:]}")
print("Dispatching via Quick OTP route...")

url = f"https://www.fast2sms.com/dev/bulkV2?authorization={api_key}&variables_values={test_otp}&route=otp&numbers={mobile_10}"
req = urllib.request.Request(url, headers={"cache-control": "no-cache"})

try:
    with urllib.request.urlopen(req, timeout=12) as resp:
        result = json.loads(resp.read().decode("utf-8"))
        print("\nFast2SMS API Response:")
        print(json.dumps(result, indent=2))
        if result.get("return") is True:
            print(f"\n[SUCCESS] Live SMS dispatched to +91 {mobile_10}!")
            print("Check your mobile phone now for the verification message.\n")
        else:
            print(f"\n[FAILED] Fast2SMS returned an error: {result.get('message')}\n")
except Exception as e:
    print(f"\n[EXCEPTION] Failed to connect to Fast2SMS: {e}\n")
