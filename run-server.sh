#!/bin/bash

# ============================================
# CHIT CALCULATOR - LOCAL SERVER STARTUP
# ============================================
# This script starts a local web server
# for testing the Chit Fund Calculator
# ============================================

echo ""
echo "========================================"
echo "  Chit Fund Calculator Server"
echo "========================================"
echo ""

# Check if Python 3 is installed
if command -v python3 &> /dev/null; then
    echo "✓ Python 3 detected. Starting server..."
    echo ""
    echo "========================================"
    echo "  Server Information"
    echo "========================================"
    echo "  Local:    http://localhost:8000"
    echo "  Stop:     Press Ctrl+C"
    echo "========================================"
    echo ""
    echo "Access the app in your browser!"
    echo ""
    python3 -m http.server 8000
# Check if Python 2 is installed
elif command -v python &> /dev/null; then
    echo "✓ Python detected. Starting server..."
    echo ""
    echo "========================================"
    echo "  Server Information"
    echo "========================================"
    echo "  Local:    http://localhost:8000"
    echo "  Stop:     Press Ctrl+C"
    echo "========================================"
    echo ""
    echo "Access the app in your browser!"
    echo ""
    python -m SimpleHTTPServer 8000
else
    echo ""
    echo "✗ Python is not installed"
    echo ""
    echo "Please install Python first:"
    echo "  macOS:   brew install python3"
    echo "  Ubuntu:  sudo apt-get install python3"
    echo "  Other:   https://www.python.org"
    echo ""
fi
