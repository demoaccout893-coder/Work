#!/usr/bin/env python3
"""
Dashboard HTTP Server for Quantum Arbitrage Engine.
Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>

Serves the static HTML/JS/CSS dashboard on port 3000.
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

PORT = int(os.environ.get("DASHBOARD_PORT", 3000))
DASHBOARD_DIR = Path(__file__).parent / "frontend"


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(DASHBOARD_DIR), **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization")
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        super().end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "":
            self.path = "/index.html"
        super().do_GET()

    def log_message(self, format, *args):
        pass  # Suppress logs


def main():
    os.chdir(DASHBOARD_DIR)
    with socketserver.TCPServer(("0.0.0.0", PORT), DashboardHandler) as httpd:
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║     Quantum Arbitrage Engine - Dashboard Server              ║
║     Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>     ║
╠══════════════════════════════════════════════════════════════╣
║  Dashboard:  http://localhost:{PORT}                          ║
║  API:        http://localhost:8000/api/v1                     ║
║  API Docs:   http://localhost:8000/docs                      ║
╚══════════════════════════════════════════════════════════════╝
""")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\nDashboard server stopped")
            sys.exit(0)


if __name__ == "__main__":
    main()
