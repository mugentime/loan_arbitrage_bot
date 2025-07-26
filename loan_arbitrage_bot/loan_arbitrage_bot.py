from loan_arbitrage_bot.ltv_utils import calculate_spread, is_within_band
from loan_arbitrage_bot.trade_executor import swap_collateral

class BinanceClient:
    def get_flexible_loans(self):
        return []

    def adjust_ltv(self, order_id, adjust_type, amount):
        pass

    def place_market_order(self, symbol, side, quantity):
        pass

    def get_price(self, symbol):
        return 1.0

def run_bot():
    TARGET_LTV = 0.78
    BAND = 0.01
    SPREAD_THRESHOLD = 0.02
    ADJUST_PERCENT = 0.02

    client = BinanceClient()
    loans = client.get_flexible_loans()

    if len(loans) < 2:
        print("Need at least two flexible loans.")
        return

    loan_a, loan_b = loans[0], loans[1]
    ltv_a = float(loan_a["ltv"])
    ltv_b = float(loan_b["ltv"])
    spread = calculate_spread(ltv_a, ltv_b)

    print(f"LTV A: {ltv_a:.2%}, LTV B: {ltv_b:.2%}, Spread: {spread:.2%}")

    if abs(spread) >= SPREAD_THRESHOLD:
        if spread > 0:
            print("Loan A underperforms, rebalancing from B → A")
            amount = float(loan_b["collateralAmount"]) * ADJUST_PERCENT
            from_coin = loan_b["collateralCoin"]
            to_coin = loan_a["collateralCoin"]
            acquired = swap_collateral(client, from_coin, to_coin, amount)
            client.adjust_ltv(loan_a["orderId"], "ADD", acquired)
            client.adjust_ltv(loan_b["orderId"], "REDUCE", amount)
        else:
            print("Loan B underperforms, rebalancing from A → B")
            amount = float(loan_a["collateralAmount"]) * ADJUST_PERCENT
            from_coin = loan_a["collateralCoin"]
            to_coin = loan_b["collateralCoin"]
            acquired = swap_collateral(client, from_coin, to_coin, amount)
            client.adjust_ltv(loan_b["orderId"], "ADD", acquired)
            client.adjust_ltv(loan_a["orderId"], "REDUCE", amount)
    else:
        for loan, name in zip([loan_a, loan_b], ["A", "B"]):
            ltv = float(loan["ltv"])
            order_id = loan["orderId"]
            amt = float(loan["collateralAmount"]) * ADJUST_PERCENT

            if not is_within_band(ltv, TARGET_LTV, BAND):
                if ltv > TARGET_LTV:
                    print(f"Loan {name}: High LTV ({ltv:.2%}), adding collateral.")
                    client.adjust_ltv(order_id, "ADD", amt)
                else:
                    print(f"Loan {name}: Low LTV ({ltv:.2%}), reducing collateral.")
                    client.adjust_ltv(order_id, "REDUCE", amt)
