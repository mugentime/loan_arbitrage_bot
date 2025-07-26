class BinanceAPIError(Exception):
    """Base exception for Binance API errors"""
    pass

class BinanceRequestError(BinanceAPIError):
    """Exception raised for errors in API requests"""
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Binance API request failed: {status_code} - {message}")

class BinanceAuthError(BinanceAPIError):
    """Exception raised for authentication errors"""
    pass

class ConfigurationError(Exception):
    """Exception raised for configuration errors"""
    pass

class LoanMonitorError(Exception):
    """Base exception for loan monitoring errors"""
    pass