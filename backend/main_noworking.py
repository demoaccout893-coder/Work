# ================================================
# Quantum Arbitrage Engine v4 - MAIN APPLICATION
# Author: HABIB-UR-REHMAN (HaSan__B_h_a_t_t_i)
# ================================================

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import json
from typing import List
from datetime import datetime

# Import your engines (adjust if paths differ)
from app.core.market_engine import market_engine
from app.core.arbitrage_engine import arbitrage_engine
from app.core.portfolio_tracker import portfolio_tracker
from app.core.execution_engine import execution_engine


# ==================================================
# APPLICATION LIFECYCLE
# ==================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 Starting Quantum Arbitrage Engine v4...")
    await market_engine.start()
    await arbitrage_engine.start()
    yield
    print("🛑 Shutting down Quantum Arbitrage Engine...")
    await market_engine.stop()


app = FastAPI(
    title="Quantum Arbitrage Engine v4",
    version="4.0.0",
    lifespan=lifespan
)

# ==================================================
# CORS FIX (CRITICAL FOR DASHBOARD)
# ==================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================================================
# REST ENDPOINTS
# ==================================================

@app.get("/api/v1/market/prices")
async def get_market_prices():
    return {
        "prices": market_engine.get_latest_prices(),
        "timestamp": datetime.utcnow()
    }


@app.get("/api/v1/market/opportunities")
async def get_opportunities():
    return arbitrage_engine.get_latest_opportunities()


@app.get("/api/v1/portfolio")
async def get_portfolio():
    return portfolio_tracker.get_metrics()


@app.get("/api/v1/system/status")
async def get_system_status():
    return {
        "execution_mode": execution_engine.mode,
        "connected_exchanges": list(market_engine.connected_exchanges),
        "timestamp": datetime.utcnow()
    }


# ==================================================
# WEBSOCKET MANAGER (FIXES 403 + DISCONNECTED)
# ==================================================

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()   # 🔥 CRITICAL FIX
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        dead_connections = []

        for connection in self.active_connections:
            try:
                await connection.send_text(json.dumps(message))
            except:
                dead_connections.append(connection)

        for dc in dead_connections:
            self.disconnect(dc)


manager = ConnectionManager()


# ==================================================
# FIXED WEBSOCKET ROUTE
# ==================================================

@app.websocket("/ws/market")
async def websocket_market(websocket: WebSocket):

    try:
        await manager.connect(websocket)

        while True:
            data = {
                "prices": market_engine.get_latest_prices(),
                "opportunities": arbitrage_engine.get_latest_opportunities(),
                "portfolio": portfolio_tracker.get_metrics(),
                "system": {
                    "execution_mode": execution_engine.mode,
                    "connected_exchanges": list(market_engine.connected_exchanges),
                },
                "timestamp": datetime.utcnow().isoformat()
            }

            await manager.broadcast(data)
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception as e:
        print("WebSocket error:", e)
        manager.disconnect(websocket)
