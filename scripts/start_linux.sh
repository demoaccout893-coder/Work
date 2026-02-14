#!/bin/bash
# ═══════════════════════════════════════════════════════════
#  Quantum Arbitrage Engine - Linux/Mac Startup Script
#  Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>
# ═══════════════════════════════════════════════════════════

set -e

echo ""
echo "  ======================================================"
echo "   Quantum Arbitrage Engine v2.0.0"
echo "   Author: HABIB-UR-REHMAN"
echo "  ======================================================"
echo ""

# Navigate to project root
cd "$(dirname "$0")/.."
PROJECT_DIR="$(pwd)"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "  [ERROR] Python 3 is not installed."
    echo "  Install: sudo apt install python3 python3-pip python3-venv"
    exit 1
fi

echo "  Python: $(python3 --version)"

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    echo "  [SETUP] Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "  [SETUP] Installing dependencies..."
pip install -r requirements.txt --quiet

# Create directories
mkdir -p logs data backups models

# Copy .env if not exists
if [ ! -f ".env" ]; then
    echo "  [SETUP] Creating .env from template..."
    cp .env.example .env
fi

echo ""
echo "  [START] Starting Quantum Arbitrage Engine..."
echo ""
echo "  API Server:    http://localhost:8000"
echo "  API Docs:      http://localhost:8000/docs"
echo "  Dashboard:     http://localhost:3000"
echo ""
echo "  Press Ctrl+C to stop"
echo ""

python3 run.py
