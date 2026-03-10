@echo off
REM ============================================
REM Chit Fund Calculator - Streamlit Launcher
REM ============================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo   Chit Fund Calculator (Python/Streamlit)
echo ========================================
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0

echo Starting Streamlit server...
echo.

REM Run Streamlit
cd /d "%SCRIPT_DIR%"

REM Check if venv exists
if exist ".venv\Scripts\streamlit.exe" (
    echo ✓ Virtual environment found
    echo.
    echo ========================================
    echo   Server Information
    echo ========================================
    echo   URL:  http://localhost:8501
    echo   Stop: Press Ctrl+C in terminal
    echo ========================================
    echo.
    echo Opening browser... Please wait (10 seconds)
    timeout /t 3 /nobreak
    
    REM Try to open browser (Windows)
    start http://localhost:8501
    
    REM Start Streamlit
    .\.venv\Scripts\streamlit.exe run streamlit_app.py --logger.level=error
) else (
    echo ✗ Virtual environment not found!
    echo.
    echo Please run: python -m venv .venv
    echo Then: .\.venv\Scripts\pip install pandas numpy plotly streamlit
    echo.
    pause
)
