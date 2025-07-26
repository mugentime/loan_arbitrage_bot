from loan_arbitrage_bot.loan_arbitrage_bot import run_bot

class MockBinanceClient:
    def __init__(self):
        self.actions = []

    def get_flexible_loans(self):
        return [
            {"orderId": "A1", "ltv": "0.80", "collateralAmount": "100", "collateralCoin": "ETH"},
            {"orderId": "B1", "ltv": "0.77", "collateralAmount": "100", "collateralCoin": "BTC"},
        ]

    def adjust_ltv(self, order_id, adjust_type, amount):
        print(f"adjust_ltv {adjust_type} {amount} on {order_id}")

    def place_market_order(self, symbol, side, quantity):
        print(f"{side} {quantity} of {symbol}")

    def get_price(self, symbol):
        return {"ETHUSDT": 3000, "BTCUSDT": 60000}[symbol]

from loan_arbitrage_bot import loan_arbitrage_bot, trade_executor
loan_arbitrage_bot.BinanceClient = MockBinanceClient  # Inject mock

if __name__ == "__main__":
    run_bot()
