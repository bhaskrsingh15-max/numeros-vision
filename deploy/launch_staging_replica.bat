@echo off
REM ==============================================================================
REM NUMEROS VISION & CHARM AI — STAGING REPLICA PREVIEW LAUNCH SCRIPT
REM Domain: staging.numerosvision.com / Port: 8001
REM Mode: Full Functionality Replica Testing (Bypasses payment wall for QA/QC)
REM ==============================================================================

set ENVIRONMENT=staging
set ALLOW_STAGING_TEST_BYPASS=true
set ALLOW_TEST_TOKENS=true

echo [1/3] Setting Staging Replica Environment Variables...
echo   ENVIRONMENT=staging
echo   ALLOW_STAGING_TEST_BYPASS=true
echo   ALLOW_TEST_TOKENS=true

echo [2/3] Checking Python Virtual Environment...
if exist ".venv\Scripts\python.exe" (
    set PYTHON_BIN=.venv\Scripts\python.exe
) else (
    set PYTHON_BIN=python
)

echo [3/3] Launching Staging Replica ASGI Server...
echo   Host: 0.0.0.0
echo   Port: 8001
echo   URL:  http://127.0.0.1:8001
echo   Domain: http://staging.numerosvision.com:8001
echo ==============================================================================
echo [READY] Staging replica active. All reports and Charm AI unlocked for QA testing.
echo ==============================================================================

%PYTHON_BIN% -m uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
