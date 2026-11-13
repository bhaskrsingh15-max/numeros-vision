# scripts/start_server.py
import os
import sys
import uvicorn

try:
    sys.stdout.reconfigure(line_buffering=True)
except Exception:
    pass

# Ensure project root is in sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if __name__ == "__main__":
    print(f"Launching Numeros Vision Uvicorn Server from root: {PROJECT_ROOT}...", flush=True)
    from app.main import app
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
