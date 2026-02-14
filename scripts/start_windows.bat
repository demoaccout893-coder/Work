@echo off
SETLOCAL EnableDelayedExpansion

REM ═══════════════════════════════════════════════════════════
REM  Quantum Arbitrage Engine - Windows Startup Script
REM  Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>
REM ═══════════════════════════════════════════════════════════

title Quantum Arbitrage Engine v2.0.0

echo.
echo  ======================================================
echo   Quantum Arbitrage Engine v2.0.0
echo   Author: HABIB-UR-REHMAN
echo  ======================================================
echo.

cd /d "%~dp0.."

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo  [ERROR] Python is not installed or not in PATH.
    echo  Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

REM Create virtual environment if not exists
if not exist "venv" (
    echo  [SETUP] Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo  [SETUP] Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo  [SETUP] Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install dependencies
echo  [SETUP] Installing dependencies (this may take a minute)...
pip install -r requirements.txt

REM Create directories
if not exist "logs" mkdir logs
if not exist "data" mkdir data
if not exist "backups" mkdir backups
if not exist "models" mkdir models

REM Copy .env if not exists
if not exist ".env" (
    echo  [SETUP] Creating .env from template...
    copy .env.example .env
)

echo.
echo  [START] Starting Quantum Arbitrage Engine...
echo.
echo  API Server:    http://localhost:8000
echo  API Docs:      http://localhost:8000/docs
echo  Dashboard:     http://localhost:3000
echo.
echo  Press Ctrl+C to stop
echo.

REM Set PYTHONPATH to current directory to ensure backend module is found
set PYTHONPATH=%PYTHONPATH%;%CD%

python run.py

pause
