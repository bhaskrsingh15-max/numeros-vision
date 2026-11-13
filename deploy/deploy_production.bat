@echo off
REM ==============================================================================
REM NUMEROS VISION & CHARM AI — HASSLE-FREE WINDOWS PRODUCTION LAUNCH SCRIPT
REM ==============================================================================

echo [1/4] Checking Python Virtual Environment...
if exist ".venv\Scripts\python.exe" (
    set PYTHON_BIN=.venv\Scripts\python.exe
) else (
    set PYTHON_BIN=python
)

echo [2/4] Verifying Core Occult Engines and Enterprise Gateway...
%PYTHON_BIN% -c "from app.engine.enterprise_agent_gateway import EnterpriseAgentGateway; from app.engine.vedic_numerology import analyze_vedic_numerology; print('  [OK] Gateway and Occult Engines Verified.')"

echo [3/4] Launching High-Concurrency Production ASGI Server...
echo   Mode: Multi-Worker ASGI
echo   Port: 8000
echo   URL:  http://127.0.0.1:8000
echo ==============================================================================
%PYTHON_BIN% -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
