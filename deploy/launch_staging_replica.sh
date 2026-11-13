#!/bin/bash
# ==============================================================================
# NUMEROS VISION & CHARM AI — STAGING REPLICA PREVIEW LAUNCH SCRIPT (LINUX)
# Domain: staging.numerosvision.com / Port: 8001
# Mode: Full Functionality Replica Testing (Bypasses payment wall for QA/QC)
# ==============================================================================

export ENVIRONMENT=staging
export ALLOW_STAGING_TEST_BYPASS=true
export ALLOW_TEST_TOKENS=true

echo "=============================================================================="
echo "NUMEROS VISION: STAGING REPLICA PREVIEW LAUNCH"
echo "Host: 0.0.0.0 | Port: 8001 | Domain: staging.numerosvision.com"
echo "=============================================================================="

if [ -f ".venv/bin/python" ]; then
    PYTHON_BIN=.venv/bin/python
else
    PYTHON_BIN=python3
fi

$PYTHON_BIN -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --workers 2
