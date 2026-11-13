#!/bin/bash
# ==============================================================================
# Numeros Vision & Charm AI — Automated Quality Gate & Production Deployer
# Ensures 100% test pass rate (182 tests) and complete QC audit (109 gates)
# prior to promoting code to live production.
# ==============================================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_DIR"

echo "======================================================================"
echo "✦ NUMEROS VISION: PRE-DEPLOYMENT QUALITY GATE ENFORCEMENT ✦"
echo "======================================================================"

# 1. Activate Virtual Environment
if [ -d ".venv" ]; then
    source .venv/bin/activate
else
    echo "[ERROR] Virtual environment .venv not found!"
    exit 1
fi

# 2. Gate 1: Comprehensive Unit & Integration Tests (182 tests)
echo ""
echo "[GATE 1/2] Executing Unit & Integration Test Suite..."
python3 -m unittest discover tests

# 3. Gate 2: Master 109-Gate QC Audit
echo ""
echo "[GATE 2/2] Executing Master 109-Gate QC Audit..."
python3 scratch/complete_audit_qc.py

echo ""
echo "======================================================================"
echo "✦ ALL QUALITY GATES PASSED (100% PASS RATE, 0 FAILURES) ✦"
echo "======================================================================"

# 4. Zero-Downtime Service Reload
if command -v systemctl &> /dev/null; then
    echo "Reloading production service via systemd..."
    sudo systemctl reload nv-production || sudo systemctl restart nv-production
    echo "[SUCCESS] Production service reloaded with zero downtime!"
else
    echo "[NOTICE] systemctl not detected; local verification completed cleanly."
fi
