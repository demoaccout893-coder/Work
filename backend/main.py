"""
Quantum Arbitrage Engine - Main Application Entry Point
Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.core.config import settings
from backend.core.logging_config import setup_logging
from backend.exchanges.adapter import ExchangeManager
from backend.services.market_engine import MarketDataEngine
from backend.services.arbitrage_engine import ArbitrageEngine
from backend.services.execution_engine import ExecutionEngine
from backend.services.risk_manager import RiskManager
from backend.services.portfolio_tracker import PortfolioTracker
from backend.services.ai_decision import AIDecisionEngine

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize components
exchange_manager = ExchangeManager()
market_engine = MarketDataEngine(exchange_manager)
risk_manager = RiskManager()
portfolio_tracker = PortfolioTracker(exchange_manager)
ai_engine = AIDecisionEngine()
arbitrage_engine = ArbitrageEngine(market_engine, exchange_manager)
execution_engine = ExecutionEngine(exchange_manager, risk_manager, portfolio_tracker)

app = FastAPI(
    title="Quantum Arbitrage Engine API",
    description="Institutional-Grade Multi-Exchange Arbitrage Trading Platform",
    version="2.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize all services on startup."""
    logger.info("🚀 Starting Quantum Arbitrage Engine...")
    
    # 1. Initialize Exchange Manager
    enabled_exchanges = settings.exchanges_list
    for name in enabled_exchanges:
        name_lower = name.lower()
        config = {
            'apiKey': getattr(settings, f"{name_lower}_api_key", ""),
            'secret': getattr(settings, f"{name_lower}_api_secret", ""),
        }
        # Add passphrase if available (for OKX/KuCoin)
        passphrase = getattr(settings, f"{name_lower}_passphrase", None)
        if passphrase:
            config['password'] = passphrase
            
        exchange_manager.add_exchange(name, config)
    
    await exchange_manager.initialize_all()
    
    # 2. Start Market Data Engine
    await market_engine.start()
    
    # 3. Start Portfolio Tracker
    await portfolio_tracker.start()
    
    # 4. Start Arbitrage Engine
    await arbitrage_engine.start()
    
    # 5. Start Execution Engine
    await execution_engine.start()
    
    logger.info("✅ All systems operational")

@app.on_event("shutdown")
async def shutdown_event():
    """Gracefully shut down all services."""
    logger.info("🛑 Shutting down Quantum Arbitrage Engine...")
    
    await execution_engine.stop()
    await arbitrage_engine.stop()
    await portfolio_tracker.stop()
    await market_engine.stop()
    await exchange_manager.close_all()
    
    logger.info("👋 Shutdown complete")

# --- API Endpoints ---

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version
    }

@app.get("/api/v1/market/prices")
async def get_market_prices():
    """Get all real-time prices from memory."""
    prices = await market_engine.get_all_prices()
    return {"prices": prices, "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/v1/arbitrage/opportunities")
async def get_opportunities(min_profit: float = 0.0):
    """Get active arbitrage opportunities."""
    opps = await arbitrage_engine.get_opportunities()
    filtered_opps = [o for o in opps if o['net_profit_pct'] >= min_profit]
    return {"opportunities": filtered_opps, "count": len(filtered_opps)}

@app.get("/api/v1/portfolio/metrics")
async def get_portfolio_metrics():
    """Get portfolio and P&L summary."""
    # Return demo metrics for dashboard display
    return {
        "daily_pnl_usd": 1250.50,
        "daily_pnl_pct": 1.25,
        "total_exposure_usd": 45000.00,
        "active_trades_count": 3,
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/admin/exchanges")
async def get_exchanges_status():
    """Get status of all exchange adapters."""
    adapters = exchange_manager.get_all_adapters()
    return {
        "exchanges": [
            {"name": a.name, "connected": a.is_connected, "private": a.use_private} 
            for a in adapters.values()
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/")
async def root():
    return {
        "message": "Quantum Arbitrage Engine API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)

from backend.routers import admin_settings  # adjust the import path

app.include_router(admin_settings.router)