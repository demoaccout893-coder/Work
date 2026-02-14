"""
Exchange Adapter for Quantum Arbitrage Engine.
Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>

Handles multi-exchange connectivity using CCXT and CCXT.Pro.
Supports hybrid public/private access and real-time WebSocket streaming.
"""

import asyncio
import logging
import ccxt.pro as ccxtpro
import ccxt
from typing import Dict, List, Optional, Any, Callable

# Disable verbose logging for CCXT and other libraries
logging.getLogger('ccxt').setLevel(logging.WARNING)
logging.getLogger('ccxt.pro').setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

class ExchangeAdapter:
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.exchange_id = name.lower()
        self.markets = {}
        self.client = None
        self.public_client = None
        self.is_connected = False
        self.use_private = bool(config.get('apiKey') and config.get('secret'))

    async def connect(self):
        """Initialize both public and private clients."""
        try:
            # 1. Initialize Public Client (Always used for streaming)
            exchange_class = getattr(ccxtpro, self.exchange_id, None)
            if not exchange_class:
                logger.error(f"[{self.name}] Exchange not supported by CCXT.Pro")
                return

            self.public_client = exchange_class({
                'enableRateLimit': True,
                'options': {'defaultType': self.config.get('type', 'spot')}
            })
            
            # 2. Initialize Private Client (If credentials provided)
            if self.use_private:
                private_config = self.config.copy()
                private_config['enableRateLimit'] = True
                self.client = exchange_class(private_config)
                logger.info(f"[{self.name}] Private API enabled")
            else:
                self.client = self.public_client
                logger.info(f"[{self.name}] Using Public API only")

            # 3. Load Markets (Quietly and with timeout)
            try:
                self.markets = await asyncio.wait_for(self.public_client.load_markets(), timeout=15)
                self.is_connected = True
                logger.info(f"[{self.name}] Connected. Loaded {len(self.markets)} markets.")
            except Exception as e:
                logger.warning(f"[{self.name}] Load markets failed: {e}")
                self.is_connected = False
            
        except Exception as e:
            logger.error(f"[{self.name}] Connection failed: {e}")
            self.is_connected = False

    async def watch_tickers(self, symbols: List[str], callback: Callable):
        """Watch multiple tickers using public WebSocket stream."""
        if not self.public_client or not self.is_connected:
            return

        valid_symbols = [s for s in symbols if s in self.markets]
        if not valid_symbols:
            valid_symbols = symbols[:5]

        # Handle exchange-specific limitations
        if self.name.lower() == 'bybit':
            # Bybit limits watchTickers to 10 symbols per call
            valid_symbols = valid_symbols[:10]
        elif self.name.lower() in ['kraken', 'mexc']:
            # Fallback to watchTicker (singular) if watchTickers is not supported
            logger.info(f"[{self.name}] watchTickers not supported, falling back to individual watchTicker")
            tasks = [self._watch_single_ticker(s, callback) for s in valid_symbols[:5]]
            await asyncio.gather(*tasks)
            return

        logger.info(f"[{self.name}] Starting public stream for {len(valid_symbols)} symbols")
        
        while True:
            try:
                tickers = await self.public_client.watch_tickers(valid_symbols)
                for symbol, ticker in tickers.items():
                    await callback(ticker)
            except Exception as e:
                logger.error(f"[{self.name}] Stream error: {e}")
                await asyncio.sleep(5)

    async def _watch_single_ticker(self, symbol: str, callback: Callable):
        """Watch a single ticker as a fallback."""
        while True:
            try:
                ticker = await self.public_client.watch_ticker(symbol)
                await callback(ticker)
            except Exception as e:
                logger.error(f"[{self.name}] Single stream error for {symbol}: {e}")
                await asyncio.sleep(5)

    async def close(self):
        if self.public_client:
            await self.public_client.close()
        if self.client and self.client != self.public_client:
            await self.client.close()

class ExchangeManager:
    def __init__(self):
        self.adapters: Dict[str, ExchangeAdapter] = {}

    def add_exchange(self, name: str, config: Dict[str, Any]):
        adapter = ExchangeAdapter(name, config)
        self.adapters[name] = adapter

    async def initialize_all(self):
        for adapter in self.adapters.values():
            await adapter.connect()

    def get_adapter(self, name: str) -> Optional[ExchangeAdapter]:
        return self.adapters.get(name)

    def get_all_adapters(self) -> Dict[str, ExchangeAdapter]:
        return self.adapters

    async def close_all(self):
        tasks = [adapter.close() for adapter in self.adapters.values()]
        await asyncio.gather(*tasks)
