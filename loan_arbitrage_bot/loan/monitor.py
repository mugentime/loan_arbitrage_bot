import logging
from typing import List, Dict, Any
import asyncio
from decimal import Decimal

from ..binance.client import BinanceClient
from ..binance.models import FlexibleLoanOrder
from ..config import Config

logger = logging.getLogger(__name__)

class LoanMonitor:
    def __init__(self, config: Config, client: BinanceClient):
        self.config = config
        self.client = client

    async def get_active_loans(self) -> List[FlexibleLoanOrder]:
        """
        Fetch and parse active flexible loan orders
        """
        try:
            response = await self.client.get_flexible_loan_orders()
            loans = [FlexibleLoanOrder.from_dict(loan) for loan in response]
            logger.info(f"Found {len(loans)} active flexible loans")
            return loans
        except Exception as e:
            logger.error(f"Error getting active loans: {e}")
            raise

    async def monitor_loans(self):
        """
        Main monitoring loop for flexible loans
        """
        while True:
            try:
                loans = await self.get_active_loans()
                
                # Process each loan
                for loan in loans:
                    if loan.currentLTV > self.config.loan.ltv_upper_bound:
                        logger.warning(f"Loan {loan.orderId} LTV ({loan.currentLTV}) above upper bound")
                        # TODO: Implement collateral addition
                    elif loan.currentLTV < self.config.loan.ltv_lower_bound:
                        logger.warning(f"Loan {loan.orderId} LTV ({loan.currentLTV}) below lower bound")
                        # TODO: Implement collateral removal

            except Exception as e:
                logger.error(f"Error in loan monitoring loop: {e}")
            
            await asyncio.sleep(self.config.loan.monitoring_interval)