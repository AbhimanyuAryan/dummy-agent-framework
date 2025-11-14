@echo off
REM Quick start script for Gemini Agent on Windows

echo ============================================
echo Gemini Agent Framework - Quick Start
echo ============================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt -q
echo.

REM Check for .env file
if not exist ".env" (
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and add your API key
    echo.
    pause
    exit /b 1
)

REM Run test
echo Running installation test...
echo.
python test_setup.py

echo.
echo ============================================
echo Setup complete!
echo ============================================
echo.
echo To use the agent:
echo   1. python -m gemini_agent.cli
echo   2. python examples\simple_example.py
echo.

pause
