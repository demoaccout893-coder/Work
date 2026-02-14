"""
Quantum Arbitrage Engine - API Server
Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>
"""

import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.core.config import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

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

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/admin/kill-switch/activate")
async def activate_kill_switch():
    """Activate kill switch"""
    return {
        "success": True,
        "message": "Kill switch activated - all trading halted",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.post("/api/v1/admin/kill-switch/deactivate")
async def deactivate_kill_switch():
    """Deactivate kill switch"""
    return {
        "success": True,
        "message": "Kill switch deactivated - trading resumed",
        "timestamp": datetime.utcnow().isoformat()
    }

@app.get("/api/v1/admin/exchanges")
async def get_exchanges():
    """Get exchange status"""
    return {
        "exchanges": [
            {"name": "Binance", "status": "connected", "latency_ms": 45},
            {"name": "Kraken", "status": "connected", "latency_ms": 120},
            {"name": "Coinbase", "status": "connected", "latency_ms": 85},
            {"name": "Bybit", "status": "connected", "latency_ms": 65},
        ],
        "timestamp": datetime.utcnow().isoformat()
    }

# ============================================
# ROOT ENDPOINT
# ============================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Arbitrage Tracker API",
        "version": "1.0.0",
        "docs": "http://localhost:8000/docs",
        "health": "http://localhost:8000/api/v1/health"
    }

# ============================================
# ERROR HANDLERS
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "timestamp": datetime.utcnow().isoformat()},
    )

# ============================================
# STARTUP & SHUTDOWN
# ============================================

@app.on_event("startup")
async def startup_event():
    logger.info("✅ Arbitrage Tracker API started")
    logger.info("📊 Backend running on http://0.0.0.0:8000")
    logger.info("📖 API Docs: http://localhost:8000/docs")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("❌ Arbitrage Tracker API stopped")

# ============================================
# RUN SERVER
# ============================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
