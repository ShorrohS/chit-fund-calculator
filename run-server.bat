@echo off
REM ============================================
REM CHIT CALCULATOR - LOCAL SERVER STARTUP
REM ============================================
REM This batch script starts a local web server
REM for testing the Chit Fund Calculator
REM ============================================

echo.
echo ========================================
echo   Chit Fund Calculator Server
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo ✓ Python detected. Starting server...
    echo.
    echo ========================================
    echo   Server Information
    echo ========================================
    echo   Local:    http://localhost:8000
    echo   Stop:     Press Ctrl+C
    echo ========================================
    echo.
    echo Access the app in your browser!
    echo.
    python -m http.server 8000
) else (
    echo.
    echo ✗ Python is not installed or not in PATH
    echo.
    echo Please install Python and try again:
    echo 1. Download from: https://www.python.org
    echo 2. Run the installer
    echo 3. Check "Add Python to PATH"
    echo 4. Restart this script
    echo.
    pause
)
