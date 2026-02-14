#!/usr/bin/env python3
"""
Quantum Arbitrage Engine - Main Entry Point
Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>

Starts both the API server and the Dashboard server.
"""

import asyncio
import multiprocessing
import os
import sys
import signal
import time
from pathlib import Path

# Ensure project root is in path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))
os.chdir(PROJECT_ROOT)

# Create required directories
for d in ["logs", "data", "backups", "models"]:
    (PROJECT_ROOT / d).mkdir(exist_ok=True)


def run_api_server():
    """Run the FastAPI backend server."""
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=os.environ.get("API_HOST", "0.0.0.0"),
        port=int(os.environ.get("API_PORT", 8000)),
        reload=False,
        log_level="info",
        access_log=True,
    )


def run_dashboard_server():
    """Run the static dashboard server."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("serve_dashboard", PROJECT_ROOT / "serve_dashboard.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.main()


def main():
    print(r"""
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║          ⚡ QUANTUM ARBITRAGE ENGINE v2.0.0 ⚡                   ║
    ║                                                                  ║
    ║   Institutional-Grade Multi-Exchange Arbitrage Trading Platform   ║
    ║                                                                  ║
    ║   Author:  HABIB-UR-REHMAN                                       ║
    ║   Email:   hassanbhatti2343@gmail.com                            ║
    ║                                                                  ║
    ╠══════════════════════════════════════════════════════════════════╣
    ║                                                                  ║
    ║   API Server:    http://localhost:8000                            ║
    ║   API Docs:      http://localhost:8000/docs                      ║
    ║   Dashboard:     http://localhost:3000                            ║
    ║                                                                  ║
    ║   Press Ctrl+C to stop all services                              ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """)

    # Start API server in a process
    api_process = multiprocessing.Process(target=run_api_server, daemon=True)
    api_process.start()

    # Give API server time to start
    time.sleep(2)

    # Start dashboard server in a process
    dashboard_process = multiprocessing.Process(target=run_dashboard_server, daemon=True)
    dashboard_process.start()

    def shutdown(sig, frame):
        print("\n\n    Shutting down Quantum Arbitrage Engine...")
        api_process.terminate()
        dashboard_process.terminate()
        api_process.join(timeout=5)
        dashboard_process.join(timeout=5)
        print("    Shutdown complete. Goodbye!")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    try:
        while True:
            time.sleep(1)
            if not api_process.is_alive():
                print("    ⚠ API server stopped unexpectedly. Restarting...")
                api_process = multiprocessing.Process(target=run_api_server, daemon=True)
                api_process.start()
            if not dashboard_process.is_alive():
                print("    ⚠ Dashboard server stopped unexpectedly. Restarting...")
                dashboard_process = multiprocessing.Process(target=run_dashboard_server, daemon=True)
                dashboard_process.start()
    except KeyboardInterrupt:
        shutdown(None, None)


if __name__ == "__main__":
    main()
