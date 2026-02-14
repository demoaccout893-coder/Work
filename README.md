# ⚡ Quantum Arbitrage Engine v2.0.0

**Institutional-Grade Multi-Exchange Cryptocurrency Arbitrage Trading Platform**

> Author: **HABIB-UR-REHMAN** — hassanbhatti2343@gmail.com

---

## Overview

Quantum Arbitrage Engine is a production-ready, real-time cryptocurrency arbitrage detection and execution platform. It connects to **7+ major exchanges** simultaneously, scans for cross-exchange price discrepancies, evaluates opportunities with an AI scoring engine, and can execute trades in monitor, semi-auto, or full-auto mode — all through a professional dark-themed dashboard.

### Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Exchange** | Connects to Binance, Kraken, Bybit, KuCoin, OKX, Gate.io, MEXC via ccxt |
| **Real-Time Prices** | Sub-3-second price updates across all exchanges and symbols |
| **Arbitrage Detection** | Cross-exchange spread scanning with fee-aware profit calculation |
| **AI Decision Engine** | Heuristic scoring model evaluates each opportunity (0–100%) |
| **Risk Management** | Kill switch, daily loss limits, exposure caps, concurrent trade limits |
| **Trade Execution** | Monitor-only, semi-auto (you approve), or full-auto modes |
| **Portfolio Tracking** | Real-time P&L, win rate, ROI, and balance tracking |
| **Professional Dashboard** | Dark-themed real-time UI with charts, tables, and admin panel |
| **REST API** | Full FastAPI backend with Swagger docs at `/docs` |
| **Database** | SQLite (async) for trade history, opportunities, risk events |
| **Security** | JWT authentication, encrypted API keys, bcrypt passwords |
| **Cross-Platform** | One-command startup on Windows, Linux, and macOS |

---

## Quick Start

### Prerequisites

- **Python 3.10+** (3.11 recommended)
- **pip** (Python package manager)
- Internet connection (for exchange APIs)

### 1. Clone or Extract

```bash
# If from zip:
unzip quantum_arbitrage_engine.zip
cd quantum_arbitrage_engine
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your exchange API keys (optional for monitor mode)
```

### 3. Start the Engine

**Linux / macOS:**
```bash
chmod +x scripts/start_linux.sh
./scripts/start_linux.sh
```

**Windows:**
```cmd
scripts\start_windows.bat
```

**Manual (any OS):**
```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate.bat   # Windows
pip install -r requirements.txt
python run.py
```

### 4. Open Dashboard

| Service | URL |
|---------|-----|
| **Dashboard** | http://localhost:3000 |
| **API** | http://localhost:8000 |
| **API Docs (Swagger)** | http://localhost:8000/docs |
| **API Docs (ReDoc)** | http://localhost:8000/redoc |

---

## Project Structure

```
quantum_arbitrage_engine/
├── backend/
│   ├── core/
│   │   ├── config.py          # All settings (from .env)
│   │   ├── database.py        # SQLAlchemy async engine
│   │   ├── security.py        # JWT, password hashing, encryption
│   │   └── logging_config.py  # Rotating file + console logging
│   ├── exchanges/
│   │   └── adapter.py         # Unified ccxt exchange adapter
│   ├── services/
│   │   ├── market_engine.py   # Real-time price aggregation
│   │   ├── arbitrage_engine.py# Opportunity detection
│   │   ├── execution_engine.py# Trade routing & execution
│   │   ├── risk_manager.py    # Risk limits & kill switch
│   │   ├── portfolio_tracker.py# P&L & balance tracking
│   │   └── ai_decision.py    # AI trade scoring
│   ├── models/
│   │   └── tables.py          # Database ORM models
│   ├── api/                   # API route modules
│   └── main.py                # FastAPI application
├── frontend/
│   ├── index.html             # Dashboard HTML
│   └── static/
│       ├── css/dashboard.css  # Professional dark theme
│       └── js/dashboard.js    # Real-time dashboard logic
├── config/                    # Additional config files
├── scripts/
│   ├── start_windows.bat      # Windows one-click start
│   └── start_linux.sh         # Linux/Mac one-click start
├── logs/                      # Application & trade logs
├── data/                      # SQLite database
├── backups/                   # Data backups
├── models/                    # AI/ML models
├── .env                       # Environment configuration
├── .env.example               # Configuration template
├── requirements.txt           # Python dependencies
├── run.py                     # Main entry point
├── serve_dashboard.py         # Dashboard HTTP server
└── README.md                  # This file
```

---

## Trading Modes

| Mode | Description |
|------|-------------|
| **Monitor** | Default. Detects opportunities but does NOT execute trades. Safe for learning. |
| **Semi-Auto** | AI filters and scores opportunities. You approve each trade via dashboard. |
| **Full-Auto** | AI decides and executes trades automatically. Requires API keys. |

Change mode via the Admin Panel in the dashboard, or set `TRADING_MODE` in `.env`.

---

## Exchange Setup

The engine works in **monitor mode** without any API keys — it uses public market data. To enable trading:

1. Create API keys on your exchange (with trading permissions)
2. Add them to `.env`:
   ```
   BINANCE_API_KEY=your_key_here
   BINANCE_API_SECRET=your_secret_here
   ```
3. Restart the engine
4. Change trading mode to `semi_auto` or `full_auto`

### Supported Exchanges

| Exchange | Status | Maker Fee | Taker Fee |
|----------|--------|-----------|-----------|
| Binance | ✅ Supported | 0.10% | 0.10% |
| Kraken | ✅ Supported | 0.16% | 0.26% |
| Bybit | ✅ Supported | 0.10% | 0.10% |
| KuCoin | ✅ Supported | 0.10% | 0.10% |
| OKX | ✅ Supported | 0.08% | 0.10% |
| Gate.io | ✅ Supported | 0.15% | 0.15% |
| MEXC | ✅ Supported | 0.00% | 0.10% |

---

## Risk Management

The engine includes institutional-grade risk controls:

- **Kill Switch** — Instantly halt all trading with one click
- **Daily Loss Limit** — Auto-stop when daily losses exceed threshold
- **Exposure Limit** — Cap total open position value
- **Position Size Limit** — Maximum size per trade
- **Concurrent Trade Limit** — Maximum simultaneous trades
- **Profit Threshold** — Minimum spread required to execute

All limits are configurable via the Admin Panel or `.env` file.

---

## API Reference

The full API is documented at `http://localhost:8000/docs` (Swagger UI).

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/system/info` | System information |
| GET | `/api/v1/system/stats` | All system statistics |
| GET | `/api/v1/market/prices` | All current prices |
| GET | `/api/v1/market/spreads` | Spread matrix |
| GET | `/api/v1/market/opportunities` | Active arbitrage opportunities |
| POST | `/api/v1/trading/execute` | Execute a trade |
| GET | `/api/v1/trading/history` | Trade history |
| GET | `/api/v1/risk/metrics` | Risk metrics |
| PUT | `/api/v1/risk/limits` | Update risk limits |
| POST | `/api/v1/risk/kill-switch/activate` | Activate kill switch |
| GET | `/api/v1/portfolio/metrics` | Portfolio metrics |
| GET | `/api/v1/exchanges` | Exchange status |

---

## Configuration Reference

All settings are in `.env`. Key parameters:

| Variable | Default | Description |
|----------|---------|-------------|
| `TRADING_MODE` | `monitor` | monitor / semi_auto / full_auto |
| `MIN_PROFIT_THRESHOLD_PCT` | `0.3` | Minimum profit % to flag opportunity |
| `MAX_DAILY_LOSS_USD` | `5000` | Daily loss limit before kill switch |
| `MAX_OPEN_EXPOSURE_USD` | `100000` | Maximum total exposure |
| `DEFAULT_TRADE_SIZE_USD` | `100` | Default trade size |
| `PRICE_UPDATE_INTERVAL` | `2.0` | Seconds between price updates |
| `TRACKED_SYMBOLS` | `BTC/USDT,...` | Comma-separated trading pairs |
| `ENABLED_EXCHANGES` | `binance,...` | Comma-separated exchange names |

---

## Security

- **JWT Authentication** for API access
- **bcrypt** password hashing
- **Fernet encryption** for stored API keys
- **CORS** configured for dashboard access
- **Rate limiting** via exchange adapters
- Never commit `.env` to version control

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No exchanges connected" | Check internet connection. Some exchanges may be geo-restricted. |
| "Module not found" | Run `pip install -r requirements.txt` |
| Port already in use | Change `API_PORT` or `DASHBOARD_PORT` in `.env` |
| No opportunities detected | Normal — arbitrage opportunities are rare. Lower `MIN_PROFIT_THRESHOLD_PCT`. |
| Exchange connection failed | Some exchanges block certain regions. Try a VPN or different exchange. |

---

## License

This project is proprietary software created by **HABIB-UR-REHMAN**.

---

## Author

**HABIB-UR-REHMAN**
Email: hassanbhatti2343@gmail.com

---

*Built with Python, FastAPI, ccxt, SQLAlchemy, and Chart.js*
