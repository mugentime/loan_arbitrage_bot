import asyncio
import logging
from .config import load_config
from .binance.client import BinanceClient
from .loan.monitor import LoanMonitor

logger = logging.getLogger(__name__)

async def main():
    """
    Main entry point for the loan arbitrage bot
    """
    try:
        # Load configuration
        config = load_config()
        
        # Initialize Binance client
        async with BinanceClient(config.binance) as client:
            # Initialize loan monitor
            monitor = LoanMonitor(config, client)
            
            # Start monitoring loans
            logger.info("Starting loan monitoring...")
            await monitor.monitor_loans()
    
    except KeyboardInterrupt:
        logger.info("Shutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    asyncio.run(main())