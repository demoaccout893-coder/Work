"""
SQLAlchemy ORM models for Quantum Arbitrage Engine (Advanced Version)
Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>
"""

from datetime import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, JSON,
    Numeric, Enum, ForeignKey, CheckConstraint, UniqueConstraint, Index
)
from sqlalchemy.orm import relationship
from backend.core.database import Base
import enum


# --- Enums for consistent status values ---
class TradeStatus(enum.Enum):
    PENDING = "pending"
    EXECUTING = "executing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class OpportunityStatus(enum.Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    EXECUTED = "executed"
    IGNORED = "ignored"


class RiskSeverity(enum.Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"


class Trade(Base):
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    trade_id = Column(String(64), unique=True, nullable=False, index=True)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True, index=True)
    symbol = Column(String(32), nullable=False, index=True)
    trade_type = Column(String(32), default="cross_exchange")  # cross_exchange, triangular

    # Exchange and order details
    buy_exchange = Column(String(32), nullable=False)
    sell_exchange = Column(String(32), nullable=False)
    buy_order_id = Column(String(128), nullable=True)          # exchange order ID
    sell_order_id = Column(String(128), nullable=True)
    buy_price = Column(Numeric(18, 8), nullable=False)
    sell_price = Column(Numeric(18, 8), nullable=False)
    quantity = Column(Numeric(18, 8), nullable=False)

    # Fees (can be in base or quote currency; we store numeric value and currency)
    buy_fee = Column(Numeric(18, 8), default=0.0)
    buy_fee_currency = Column(String(16), nullable=True)
    sell_fee = Column(Numeric(18, 8), default=0.0)
    sell_fee_currency = Column(String(16), nullable=True)

    # Profit calculations
    gross_profit = Column(Numeric(18, 8), default=0.0)
    net_profit = Column(Numeric(18, 8), default=0.0)
    profit_percent = Column(Numeric(10, 4), default=0.0)

    # Status and AI
    status = Column(Enum(TradeStatus), default=TradeStatus.PENDING, nullable=False)
    ai_score = Column(Numeric(5, 4), default=0.0)   # 0.0000 - 1.0000
    ai_recommendation = Column(String(32), default="")

    # Execution metrics
    execution_time_ms = Column(Integer, default=0)
    error_message = Column(Text, default="")

    # Additional metadata
    metadata_json = Column(JSON, default=dict)
    notes = Column(Text, default="")                # user notes

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    opportunity = relationship("Opportunity", back_populates="trades")

    # Constraints
    __table_args__ = (
        CheckConstraint('profit_percent >= -100', name='profit_percent_min'),
        CheckConstraint('ai_score >= 0 AND ai_score <= 1', name='ai_score_range'),
        Index('ix_trades_status_created', 'status', 'created_at'),
    )


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    opportunity_id = Column(String(64), unique=True, nullable=False, index=True)
    symbol = Column(String(32), nullable=False, index=True)
    arb_type = Column(String(32), default="cross_exchange")  # cross_exchange, triangular
    buy_exchange = Column(String(32), nullable=False)
    sell_exchange = Column(String(32), nullable=False)
    buy_price = Column(Numeric(18, 8), nullable=False)
    sell_price = Column(Numeric(18, 8), nullable=False)
    spread_pct = Column(Numeric(10, 4), nullable=False)
    net_profit_pct = Column(Numeric(10, 4), nullable=False)
    estimated_profit_usd = Column(Numeric(18, 2), default=0.0)

    # AI evaluation
    ai_score = Column(Numeric(5, 4), default=0.0)
    ai_recommendation = Column(String(32), default="")

    # Status tracking
    status = Column(Enum(OpportunityStatus), default=OpportunityStatus.ACTIVE, nullable=False)
    was_executed = Column(Boolean, default=False)

    # Detection time
    detected_at = Column(DateTime, default=datetime.utcnow, index=True)

    # Relationships
    trades = relationship("Trade", back_populates="opportunity")

    __table_args__ = (
        CheckConstraint('ai_score >= 0 AND ai_score <= 1', name='opp_ai_score_range'),
        Index('ix_opportunities_status_detected', 'status', 'detected_at'),
    )


class RiskEvent(Base):
    __tablename__ = "risk_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    event_type = Column(String(64), nullable=False)  # kill_switch, exposure_breach, loss_limit, etc.
    severity = Column(Enum(RiskSeverity), default=RiskSeverity.WARNING, nullable=False)
    message = Column(Text, nullable=False)
    details_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index('ix_risk_events_severity_created', 'severity', 'created_at'),
    )


class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    total_value_usd = Column(Numeric(18, 2), default=0.0)
    realized_pnl = Column(Numeric(18, 2), default=0.0)
    unrealized_pnl = Column(Numeric(18, 2), default=0.0)
    daily_pnl = Column(Numeric(18, 2), default=0.0)
    open_exposure = Column(Numeric(18, 2), default=0.0)
    balances_json = Column(JSON, default=dict)  # {exchange: {asset: amount}}
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

    __table_args__ = (
        Index('ix_portfolio_snapshots_created', 'created_at'),
    )


class ExchangeConfig(Base):
    __tablename__ = "exchange_configs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    exchange_name = Column(String(32), unique=True, nullable=False)
    enabled = Column(Boolean, default=True)

    # Encrypted fields – in practice use a custom type or encryption at application level
    api_key_encrypted = Column(Text, default="")
    api_secret_encrypted = Column(Text, default="")
    passphrase_encrypted = Column(Text, default="")

    # Fee structure
    maker_fee = Column(Numeric(8, 5), default=0.001)   # e.g., 0.001 = 0.1%
    taker_fee = Column(Numeric(8, 5), default=0.001)

    # Rate limiting and connection status
    rate_limit = Column(Integer, default=1200)          # requests per minute
    status = Column(String(16), default="disconnected")
    last_connected = Column(DateTime, nullable=True)

    # Additional configuration
    metadata_json = Column(JSON, default=dict)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('maker_fee >= 0 AND maker_fee <= 1', name='maker_fee_range'),
        CheckConstraint('taker_fee >= 0 AND taker_fee <= 1', name='taker_fee_range'),
    )


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

    __table_args__ = (
        Index('ix_audit_logs_user_created', 'user', 'created_at'),
    )