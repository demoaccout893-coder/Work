"""
Logging configuration for Quantum Arbitrage Engine.
Author: HABIB-UR-REHMAN <hassanbhatti2343@gmail.com>
"""

import logging
import logging.handlers
import os
from pathlib import Path
from backend.core.config import settings


def setup_logging():
    """Configure application-wide logging."""
    log_dir = Path(settings.log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)-30s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG if settings.debug else logging.INFO)
    console.setFormatter(fmt)

    # Rotating file handler (10 MB, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        settings.log_file, maxBytes=10_000_000, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(fmt)

    # Trade audit log
    trade_log_path = log_dir / "trades.log"
    trade_handler = logging.handlers.RotatingFileHandler(
        str(trade_log_path), maxBytes=10_000_000, backupCount=10, encoding="utf-8"
    )
    trade_handler.setLevel(logging.INFO)
    trade_handler.setFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(console)
    root.addHandler(file_handler)

    # Trade-specific logger
    trade_logger = logging.getLogger("trades")
    trade_logger.addHandler(trade_handler)

    # Suppress noisy libraries
    for lib in ["urllib3", "asyncio", "aiosqlite", "sqlalchemy.engine"]:
        logging.getLogger(lib).setLevel(logging.WARNING)

    logging.info("Logging initialized")
