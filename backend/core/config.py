"""
Configuration management for Quantum Arbitrage Engine.
"""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "Quantum Arbitrage Engine"
    app_version: str = "2.0.0"
    environment: str = "development"
    debug: bool = True
    
    # Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    dashboard_port: int = 3000
    
    # Authentication
    jwt_secret_key: str = "your-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    admin_username: str = "admin"
    admin_password: str = "admin123"
    
    # Database
    database_url: str = "sqlite+aiosqlite:///./qae.db"
    
    # Exchange API Keys
    binance_api_key: str = ""
    binance_api_secret: str = ""
    
    kraken_api_key: str = ""
    kraken_api_secret: str = ""
    
    bybit_api_key: str = ""
    bybit_api_secret: str = ""
    
    kucoin_api_key: str = ""
    kucoin_api_secret: str = ""
    kucoin_passphrase: str = ""
    
    okx_api_key: str = ""
    okx_api_secret: str = ""
    okx_passphrase: str = ""
    
    gate_api_key: str = ""
    gate_api_secret: str = ""
    
    mexc_api_key: str = ""
    mexc_api_secret: str = ""
    
    # Trading
    trading_mode: str = "monitor"
    min_profit_threshold_pct: float = 0.3
    max_slippage_pct: float = 0.1
    order_timeout_seconds: int = 30
    default_trade_size_usd: float = 100.0
    
    # Risk Management
    max_daily_loss_usd: float = 5000.0
    max_open_exposure_usd: float = 100000.0
    max_position_size_usd: float = 10000.0
    max_concurrent_trades: int = 5
    initial_capital_usd: float = 50000.0
    
    # Market Data
    tracked_symbols: str = "BTC/USDT,ETH/USDT"
    enabled_exchanges: str = "binance,kraken"
    price_update_interval: float = 2.0
    opportunity_scan_interval: float = 1.0
    
    @property
    def symbols_list(self) -> List[str]:
        return [s.strip() for s in self.tracked_symbols.split(",") if s.strip()]
    
    @property
    def exchanges_list(self) -> List[str]:
        return [e.strip() for e in self.enabled_exchanges.split(",") if e.strip()]
    
    @property
    def market_data_update_interval(self) -> float:
        return self.price_update_interval

    # Telegram Bot
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    enable_telegram_alerts: bool = False
    
    # Email Alerts
    enable_email_alerts: bool = False
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    alert_email: str = ""
    
    # Logging
    log_level: str = "INFO"
    log_file: str = "./logs/qae.log"
    
    # AI Configuration
    ai_model_path: str = "./models/trade_filter_model.pkl"
    ai_decision_threshold: float = 0.7
    
    # WebSocket Configuration
    ws_reconnect_delay: int = 5
    ws_max_retries: int = 3
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = "ignore"


# Global settings instance
settings = Settings()
