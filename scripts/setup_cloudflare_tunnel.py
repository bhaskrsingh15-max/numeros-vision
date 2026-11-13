# scripts/setup_cloudflare_tunnel.py
import os
import sys
import urllib.request

BIN_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bin")
os.makedirs(BIN_DIR, exist_ok=True)
TARGET_EXE = os.path.join(BIN_DIR, "cloudflared.exe")

URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"

if os.path.exists(TARGET_EXE) and os.path.getsize(TARGET_EXE) > 10000000:
    print(f"cloudflared.exe already exists at {TARGET_EXE} ({os.path.getsize(TARGET_EXE)} bytes)")
    sys.exit(0)

print(f"Downloading official Cloudflare tunnel binary from {URL} to {TARGET_EXE}...")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
req = urllib.request.Request(URL, headers=headers)

with urllib.request.urlopen(req) as resp, open(TARGET_EXE, 'wb') as out_file:
    data = resp.read()
    out_file.write(data)

print(f"Successfully downloaded cloudflared.exe! Size: {os.path.getsize(TARGET_EXE)} bytes.")
