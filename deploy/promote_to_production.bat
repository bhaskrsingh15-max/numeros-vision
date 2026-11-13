@echo off
REM ==============================================================================
REM Numeros Vision and Charm AI - Automated Quality Gate and Production Deployer
REM ==============================================================================

echo ======================================================================
echo NUMEROS VISION: PRE-DEPLOYMENT QUALITY GATE ENFORCEMENT
echo ======================================================================

REM 1. Activate Virtual Environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else (
    echo [ERROR] Virtual environment .venv not found!
    exit /b 1
)

REM 2. Gate 1: Comprehensive Unit and Integration Tests (182 tests)
echo.
echo [GATE 1/2] Executing Unit and Integration Test Suite...
python -m unittest discover tests
if %ERRORLEVEL% neq 0 (
    echo [CRITICAL ERROR] Unit test suite failed! Deployment aborted.
    exit /b %ERRORLEVEL%
)

REM 3. Gate 2: Master 109-Gate QC Audit
echo.
echo [GATE 2/2] Executing Master 109-Gate QC Audit...
python scratch\complete_audit_qc.py
if %ERRORLEVEL% neq 0 (
    echo [CRITICAL ERROR] Master QC Audit failed! Deployment aborted.
    exit /b %ERRORLEVEL%
)

echo.
echo ======================================================================
echo ALL QUALITY GATES PASSED (100 PERCENT PASS RATE, 0 FAILURES)
echo ======================================================================
echo [SUCCESS] Build verified and approved for production promotion!
