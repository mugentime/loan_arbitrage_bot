from typing import Dict, Any
import os
from dataclasses import dataclass
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class BinanceAPIConfig:
    api_key: str
    api_secret: str
    base_url: str = "https://api.binance.com"
    recv_window: int = 5000  # milliseconds
    max_retries: int = 3
    retry_delay: float = 1.0  # seconds

@dataclass
class LoanConfig:
    ltv_upper_bound: float = 0.79
    ltv_lower_bound: float = 0.77
    ltv_target: float = 0.78
    spread_threshold: float = 0.02
    max_slippage: float = 0.001
    monitoring_interval: int = 60  # seconds

@dataclass
class Config:
    binance: BinanceAPIConfig
    loan: LoanConfig
    environment: str = "production"

def load_config() -> Config:
    """
    Load configuration from environment variables.
    Returns:
        Config: Application configuration
    """
    try:
        binance_config = BinanceAPIConfig(
            api_key=os.environ["BINANCE_API_KEY"],
            api_secret=os.environ["BINANCE_API_SECRET"],
            recv_window=int(os.environ.get("BINANCE_RECV_WINDOW", "5000")),
            max_retries=int(os.environ.get("BINANCE_MAX_RETRIES", "3")),
            retry_delay=float(os.environ.get("BINANCE_RETRY_DELAY", "1.0")),
        )

        loan_config = LoanConfig(
            ltv_upper_bound=float(os.environ.get("LTV_UPPER_BOUND", "0.79")),
            ltv_lower_bound=float(os.environ.get("LTV_LOWER_BOUND", "0.77")),
            ltv_target=float(os.environ.get("LTV_TARGET", "0.78")),
            spread_threshold=float(os.environ.get("SPREAD_THRESHOLD", "0.02")),
            max_slippage=float(os.environ.get("MAX_SLIPPAGE", "0.001")),
            monitoring_interval=int(os.environ.get("MONITORING_INTERVAL", "60")),
        )

        config = Config(
            binance=binance_config,
            loan=loan_config,
            environment=os.environ.get("ENVIRONMENT", "production"),
        )

        logger.info("Configuration loaded successfully")
        return config

    except KeyError as e:
        logger.error(f"Missing required environment variable: {e}")
        raise
    except ValueError as e:
        logger.error(f"Invalid configuration value: {e}")
        raise