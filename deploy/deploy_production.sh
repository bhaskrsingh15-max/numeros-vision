#!/usr/bin/env bash
# ==============================================================================
# NUMEROS VISION & CHARM AI — HASSLE-FREE LINUX / CLOUD PRODUCTION DEPLOY SCRIPT
# ==============================================================================
set -e

echo "=== [1/4] Pre-Flight System Check ==="
python3 --version || { echo "Python 3 is required."; exit 1; }

echo "=== [2/4] Setting up Virtual Environment & Dependencies ==="
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt || pip install fastapi "uvicorn[standard]" gunicorn pydantic jinja2 requests httpx numpy redis

echo "=== [3/4] Verifying Enterprise Agent Gateway & Engines ==="
python3 -c "
from app.engine.enterprise_agent_gateway import EnterpriseAgentGateway
from app.engine.vedic_numerology import analyze_vedic_numerology
print('  [SUCCESS] Enterprise Gateway & Occult Calculation Engines Verified.')
"

echo "=== [4/4] Starting Gunicorn Multi-Worker Production ASGI Server ==="
exec gunicorn -c deploy/gunicorn_conf.py app.main:app
