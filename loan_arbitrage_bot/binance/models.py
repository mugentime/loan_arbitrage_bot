from dataclasses import dataclass
from decimal import Decimal
from typing import List, Optional
from datetime import datetime

@dataclass
class FlexibleLoanOrder:
    orderId: str
    asset: str
    amount: Decimal
    timestamp: datetime
    status: str
    collateralAsset: str
    collateralAmount: Decimal
    currentLTV: Decimal

    @classmethod
    def from_dict(cls, data: dict) -> 'FlexibleLoanOrder':
        return cls(
            orderId=data['orderId'],
            asset=data['asset'],
            amount=Decimal(str(data['amount'])),
            timestamp=datetime.fromtimestamp(data['timestamp'] / 1000),
            status=data['status'],
            collateralAsset=data['collateralAsset'],
            collateralAmount=Decimal(str(data['collateralAmount'])),
            currentLTV=Decimal(str(data['currentLTV']))
        )