class CryptoCurrency:
    def __init__(self, symbol, max_threshold, min_threshold):
        self.symbol = symbol
        self.max_threshold = max_threshold
        self.min_threshold = min_threshold
        self.current_price = None

    def update_price(self, price):
        self.current_price = price

    def is_above_max_threshold(self):
        return self.current_price >= self.max_threshold

    def is_below_min_threshold(self):
        return self.current_price <= self.min_threshold


class CryptoCurrencyTracker:
    def __init__(self):
        self.currencies = {}

    def add_currency(self, symbol, max_threshold, min_threshold):
        self.currencies[symbol] = CryptoCurrency(symbol, max_threshold, min_threshold)

    def update_prices(self, prices):
        for symbol, price in prices.items():
            if symbol in self.currencies:
                self.currencies[symbol].update_price(price)

    def check_thresholds(self):
        notifications = []
        for currency in self.currencies.values():
            if currency.is_above_max_threshold():
                notifications.append(
                    f"{currency.symbol} above max threshold: {currency.max_threshold}"
                )
            elif currency.is_below_min_threshold():
                notifications.append(
                    f"{currency.symbol} below min threshold: {currency.min_threshold}"
                )
        return notifications
