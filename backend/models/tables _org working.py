"""
SQLAlchemy ORM models for Quantum Arbitrage Engine.
Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, JSON, Enum as SAEnum
)
from backend.core.database import Base


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_id = Column(String(64), unique=True, nullable=False, index=True)
    symbol = Column(String(32), nullable=False, index=True)
    trade_type = Column(String(32), default="cross_exchange")  # cross_exchange, triangular
    buy_exchange = Column(String(32), nullable=False)
    sell_exchange = Column(String(32), nullable=False)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    quantity = Column(Float, nullable=False)
    buy_fee = Column(Float, default=0.0)
    sell_fee = Column(Float, default=0.0)
    gross_profit = Column(Float, default=0.0)
    net_profit = Column(Float, default=0.0)
    profit_percent = Column(Float, default=0.0)
    status = Column(String(32), default="pending")  # pending, executing, completed, failed, cancelled
    ai_score = Column(Float, default=0.0)
    ai_recommendation = Column(String(32), default="")
    execution_time_ms = Column(Float, default=0.0)
    error_message = Column(Text, default="")
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    opportunity_id = Column(String(64), unique=True, nullable=False)
    symbol = Column(String(32), nullable=False, index=True)
    arb_type = Column(String(32), default="cross_exchange")
    buy_exchange = Column(String(32), nullable=False)
    sell_exchange = Column(String(32), nullable=False)
    buy_price = Column(Float, nullable=False)
    sell_price = Column(Float, nullable=False)
    spread_pct = Column(Float, nullable=False)
    net_profit_pct = Column(Float, nullable=False)
    estimated_profit_usd = Column(Float, default=0.0)
    ai_score = Column(Float, default=0.0)
    ai_recommendation = Column(String(32), default="")
    was_executed = Column(Boolean, default=False)
    detected_at = Column(DateTime, default=datetime.utcnow, index=True)


class RiskEvent(Base):
    __tablename__ = "risk_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(64), nullable=False)  # kill_switch, exposure_breach, loss_limit, etc.
    severity = Column(String(16), default="WARNING")  # INFO, WARNING, CRITICAL
    message = Column(Text, nullable=False)
    details_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_value_usd = Column(Float, default=0.0)
    realized_pnl = Column(Float, default=0.0)
    unrealized_pnl = Column(Float, default=0.0)
    daily_pnl = Column(Float, default=0.0)
    open_exposure = Column(Float, default=0.0)
    balances_json = Column(JSON, default=dict)  # {exchange: {asset: amount}}
    created_at = Column(DateTime, default=datetime.utcnow, index=True)


class ExchangeConfig(Base):
    __tablename__ = "exchange_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange_name = Column(String(32), unique=True, nullable=False)
    enabled = Column(Boolean, default=True)
    api_key_encrypted = Column(Text, default="")
    api_secret_encrypted = Column(Text, default="")
    passphrase_encrypted = Column(Text, default="")
    maker_fee = Column(Float, default=0.001)
    taker_fee = Column(Float, default=0.001)
    rate_limit = Column(Integer, default=1200)
    status = Column(String(16), default="disconnected")
    last_connected = Column(DateTime, nullable=True)
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SystemSetting(Base):
    __tablename__ = "system_settings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(128), unique=True, nullable=False)
    value = Column(Text, nullable=False)
    description = Column(Text, default="")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String(128), nullable=False)
    user = Column(String(64), default="system")
    details = Column(Text, default="")
    ip_address = Column(String(45), default="")
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
