import hmac
import hashlib
import time
from typing import Dict, Any
import requests
from urllib.parse import urlencode

from ..config import BinanceAPIConfig

class BinanceClient:
    def __init__(self, config: BinanceAPIConfig):
        self.config = config
        self.session = requests.Session()
        self.session.headers.update({
            'X-MBX-APIKEY': config.api_key,
            'Content-Type': 'application/json',
        })

    def _generate_signature(self, params: Dict[str, Any]) -> str:
        """
        Generate HMAC SHA256 signature for request authentication
        """
        query_string = urlencode(params)
        return hmac.new(
            self.config.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _add_signature(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add timestamp and signature to parameters
        """
        params['timestamp'] = int(time.time() * 1000)
        params['recvWindow'] = self.config.recv_window
        params['signature'] = self._generate_signature(params)
        return params

    async def get_flexible_loan_orders(self) -> Dict[str, Any]:
        """
        Fetch all active flexible loan orders
        """
        endpoint = f"{self.config.base_url}/sapi/v1/loan/flexible/ongoing/orders"
        params = self._add_signature({})
        
        response = self.session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()