def swap_collateral(client, from_coin, to_coin, amount_from):
    symbol_sell = f"{from_coin}USDT"
    symbol_buy = f"{to_coin}USDT"

    price_from = client.get_price(symbol_sell)
    usdt_obtained = amount_from * price_from

    price_to = client.get_price(symbol_buy)
    amount_to = usdt_obtained / price_to

    client.place_market_order(symbol_sell, "SELL", amount_from)
    client.place_market_order(symbol_buy, "BUY", round(amount_to, 6))

    return round(amount_to, 6)
